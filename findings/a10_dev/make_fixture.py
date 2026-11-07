# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
make_fixture.py
---------------

Amendment 10, development fixture: a page directory in the format of
analysis/scripts/a10_reconstruct_pages.py (edNN.gpkg + edNN.json per ED), built from results
that already exist, so the assembly and the scorer can be tested without a seven-hour run.

It runs no reconstruction. It uses only:
  sample EDs (34)   findings/a9_stepb_calibration.json. A placed ED's polygon is rebuilt from its
                    saved transform (v3_diagnostics[ed]["p"], ["c"]) and the page outline, by the
                    construction in V3.reconstruct; 57, 66 and 82 get a json with the error and
                    no gpkg.
  changed EDs (35)  findings/a9_stepb_v3_dev/poly/edNN.gpkg (development polygons, copied) with diagnostics
                    from findings/a9_stepb_v3_dev/results.json. An ED whose saved diagnostics fail
                    V3's acceptance rule (ED 63) gets a json with the error and no gpkg.
  all_hits          all_hits = every CSD name found anywhere in the page text (no title anchor, no
                    distance cluster; matched as V1._window matches), all_hits_window = its window.
  anchors, hits,    every ED, V1._window(txt, title) on V3.R2.extract_page(n). One PDF page each.
  window            hits = the CSD names it keeps; window = the hits' envelope buffered by
                    V1.P["window_buf"], [minx, miny, maxx, maxy] in EPSG:3400 (null for no hits).
  copy check        each copied development polygon is also rebuilt from its saved transform
                    (results.json p, c) and compared with the copy: the folder is old (v2/lab),
                    so this proves the polygon and the diagnostics beside it come from one fit.

Each json also carries "source" (where the numbers came from), an extra key a real run does not
write; the diagnostics hold only the keys V3.last_info holds (development-only add-ons dropped).

Ends by checking the fixture: file counts, the copy check above (IoU > 0.9999, failures named by
ED), and the rebuilt polygon of every placed sample ED against the commission majority's official
geometry (stored IoU vs rebuilt IoU, and ED 2 > 0.999). Exits 1 if any check fails.

Usage: python -W ignore findings/a10_dev/make_fixture.py FIXTURE_DIR
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import unary_union

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import a9_stepb_reconstruct_v3 as V3  # noqa: E402  (only extract_page and constants; no guard is hit)
import a7_stepb_calibrate as C  # noqa: E402  (MAJ, APP7, norm)

V1 = V3.V1
CRS = 3400
A9_CALIBRATION = REPO / "findings" / "a9_stepb_calibration.json"
A9_DEV_RESULTS = REPO / "findings" / "a9_stepb_v3_dev" / "results.json"
A7_SAMPLE = REPO / "findings" / "a7_stepb_sample.json"
DEV_POLY = REPO / "findings/a9_stepb_v3_dev/poly"  # development polygons of the changed pages (column ed)
DEV_ONLY_KEYS = {"sec", "iou", "haus_km", "ats_med", "n_ats", "muni_vs_ats_m", "layers"}  # not in V3.last_info
IOU_TOL = 1e-6  # rebuilt IoU vs the IoU stored by the a9 run
COPY_MIN_IOU = 0.9999  # copied development polygon vs the same fit rebuilt from its saved transform
ED2_MIN_IOU = 0.999  # Calgary-Beddington


def all_hits(txt):
    """Every CSD (name, geometry) whose name (4+ characters) occurs in the page text, matched exactly as
    V1._window matches them, but with no title anchor and no distance cluster filter."""
    g = V1._csd()
    blob = " | ".join(V1._norm(t) for t in txt)
    return [(nmo, geom) for nm, geom, nmo in zip(g.nm, g.geometry, g.CSDNAME)
            if len(nm) >= 4 and re.search(r"(^|[ |])" + re.escape(nm) + r"($|[ |])", blob)]


def window_bounds(hits):
    """Hits' envelope buffered by V1.P["window_buf"], [minx, miny, maxx, maxy]; None if no hits."""
    if not hits:
        return None
    return [float(v) for v in unary_union([h[1] for h in hits]).envelope.buffer(V1.P["window_buf"]).bounds]


def write_json(path, rec):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, indent=1) + "\n")


def clean(diag):
    return {k: v for k, v in diag.items() if k not in DEV_ONLY_KEYS}


def passes_rule(d):
    return bool(d["n_layer_pts"] >= V3.ACCEPT_MIN_PTS and d["med_dist_m"] <= V3.ACCEPT_MED_M
                and d["in60"] >= V3.ACCEPT_IN60)


def rule_error(d):
    """The message V3.reconstruct raises, in the repr form a10_reconstruct_pages.py writes."""
    return repr(RuntimeError(f"fit below the acceptance rule ({d['n_layer_pts']} matched points, median "
                             f"{d['med_dist_m']:.1f} m, within 60 m {d['in60']:.2f})"))


def rebuild(poly, p, c):
    """Page polygon -> EPSG:3400, the construction at the end of V3.reconstruct."""
    p = np.array(p, float)
    c = np.array(c, float)
    geoms = [poly] if poly.geom_type == "Polygon" else list(poly.geoms)
    return unary_union([Polygon(V1._apply(np.array(g.exterior.coords), p[0], p[1], p[2:], c),
                                [V1._apply(np.array(h.coords), p[0], p[1], p[2:], c) for h in g.interiors]).buffer(0)
                        for g in geoms])


def save_gpkg(path, n, geom):
    gpd.GeoDataFrame({"ed": [n]}, geometry=[geom], crs=CRS).to_file(path, driver="GPKG")


def main(argv):
    if len(argv) != 2:
        print(__doc__.split("Usage:")[-1].strip())
        return 2
    out = Path(argv[1])
    out.mkdir(parents=True, exist_ok=True)
    a9 = json.loads(A9_CALIBRATION.read_text(encoding="utf-8"))
    dev = json.loads(A9_DEV_RESULTS.read_text(encoding="utf-8"))
    s7 = json.loads(A7_SAMPLE.read_text(encoding="utf-8"))
    sample = sorted(int(x) for x in a9["sample"])
    changed = sorted(int(x) for x in s7["changed"])
    assert len(sample) == 34 and len(changed) == 35 and not set(sample) & set(changed)
    rows = {int(r["ed"]): r for r in a9["districts"]}
    stored_iou = {n: rows[n]["iou"] for n in sample if "iou" in rows[n]}
    rebuilt = {}
    copy_iou = {}
    n_gpkg = {"sample": 0, "changed": 0, "rejected": 0}

    for n in sample + changed:
        outline, _roads, _muni, txt, title = V3.R2.extract_page(n)
        hits, anchors = V1._window(txt, title)
        ah = all_hits(txt)
        rec = {"ed": n, "title": title, "anchors": [str(x) for x in anchors], "hits": [str(h[0]) for h in hits],
               "window": window_bounds(hits), "all_hits": [str(h[0]) for h in ah],
               "all_hits_window": window_bounds(ah), "polygon_status": "none", "diagnostics": {}, "error": None, "sec": None}
        gpkg = out / f"ed{n:02d}.gpkg"
        if gpkg.exists():
            gpkg.unlink()
        if n in sample:
            row = rows[n]
            rec["sec"] = row.get("sec")
            rec["source"] = "findings/a9_stepb_calibration.json"
            diag = a9["v3_diagnostics"][str(n)]
            rec["diagnostics"] = clean(diag)
            if "error" in row:
                rec["error"] = row["error"]
                if "p" in diag:  # fit rejected by the rule: the polygon is still saved
                    save_gpkg(gpkg, n, rebuild(V1._evenodd_polygon(outline), diag["p"], diag["c"]))
                    rec["polygon_status"] = "rejected"
                    n_gpkg["rejected"] += 1
            else:
                poly = V1._evenodd_polygon(outline)
                assert np.allclose(np.array(poly.centroid.coords[0]), diag["c"]), n
                assert passes_rule(diag), n
                rebuilt[n] = rebuild(poly, diag["p"], diag["c"])
                save_gpkg(gpkg, n, rebuilt[n])
                rec["polygon_status"] = "accepted"
                n_gpkg["sample"] += 1
        else:
            diag = dev[str(n)]
            rec["sec"] = diag.get("sec")
            rec["source"] = "findings/a9_stepb_v3_dev/results.json + findings/a9_stepb_v3_dev/poly"
            rec["diagnostics"] = clean(diag)
            if not passes_rule(diag):
                rec["error"] = rule_error(diag)
                save_gpkg(gpkg, n, rebuild(V1._evenodd_polygon(outline), diag["p"], diag["c"]))
                rec["polygon_status"] = "rejected"
                n_gpkg["rejected"] += 1
            else:
                src = DEV_POLY / f"ed{n}.gpkg"
                g = gpd.read_file(src)
                assert len(g) == 1 and list(g["ed"]) == [n] and g.crs.to_epsg() == CRS, src
                save_gpkg(gpkg, n, g.geometry.iloc[0])  # same geometry, normalised file name
                n_gpkg["changed"] += 1
                rec["polygon_status"] = "accepted"
                chk = rebuild(V1._evenodd_polygon(outline), diag["p"], diag["c"])
                copy_iou[n] = g.geometry.iloc[0].intersection(chk).area / g.geometry.iloc[0].union(chk).area
        write_json(out / f"ed{n:02d}.json", rec)
        print(f"ED {n:02d} {'sample ' if n in sample else 'changed'} "
              f"{'gpkg' if gpkg.exists() else 'NO gpkg'} anchors={len(rec['anchors'])}"
              f"{'  error=' + rec['error'] if rec['error'] else ''}", flush=True)

    # --- checks -------------------------------------------------------------------------------
    n_json = len(list(out.glob("ed[0-9][0-9].json")))
    n_all_gpkg = len([f for f in out.glob("ed[0-9][0-9].gpkg")])
    print(f"\nfiles: sample gpkg {n_gpkg['sample']}, changed gpkg {n_gpkg['changed']}, "
          f"gpkg total {n_all_gpkg}, json {n_json}")
    assert (n_gpkg["sample"], n_gpkg["changed"], n_gpkg["rejected"], n_json) == (31, 34, 2, 69), (n_gpkg, n_json)
    assert n_all_gpkg == 67, n_all_gpkg  # 65 accepted + rejected-fit polygons of 82 and 63
    bad = {n: round(v, 6) for n, v in copy_iou.items() if not v > COPY_MIN_IOU}
    print(f"copy check, {len(copy_iou)} changed EDs: min IoU {min(copy_iou.values()):.6f}; "
          f"{'all > ' + str(COPY_MIN_IOU) if not bad else 'MISMATCH ' + str(bad)}")
    if bad:
        return 1

    app7 = pd.read_csv(C.APP7).set_index("ed_number")
    maj = gpd.read_file(C.MAJ).to_crs(CRS)
    maj["key"] = maj.EDName2025.map(C.norm)
    worst = 0.0
    for n, g in sorted(rebuilt.items()):
        tr = maj.loc[maj.key == C.norm(app7.loc[n, "district"]), "geometry"].union_all()
        iou = g.intersection(tr).area / g.union(tr).area
        worst = max(worst, abs(iou - stored_iou[n]))
        if n == 2:
            print(f"ED 2 {app7.loc[n, 'district']}: IoU vs official {iou:.6f}")
            assert iou > ED2_MIN_IOU, iou
    print(f"rebuilt IoU vs stored a9 IoU, {len(rebuilt)} placed sample EDs: max abs difference {worst:.2e}")
    assert worst < IOU_TOL, worst
    print("fixture OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
