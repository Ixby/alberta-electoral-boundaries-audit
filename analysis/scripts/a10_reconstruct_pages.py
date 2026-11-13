# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a10_reconstruct_pages.py
------------------------

Amendment 10, page runner: panel map pages -> one polygon file and one diagnostics file per page.

Runs the frozen version 3 procedure (a9_stepb_reconstruct_v3.reconstruct) on each requested
Appendix 8 page and saves what it finds, so that the assembly (a10_assemble.py) and the scorers
can work from files and never need to re-run a page. Nothing here changes the procedure: the
polygon is exactly what V3.reconstruct returns, including its acceptance rule.

For each ED n (file stem "edNN", two digits) in OUT_DIR:
  edNN.gpkg  the reconstructed polygon, EPSG:3400, one row, columns ed + geometry.
             Written only when the page was placed (V3.reconstruct returned without raising).
  Also written, flagged polygon_status "rejected", when the fit is rejected by the acceptance rule
  (the json's "error" is then set); polygon_status is "accepted" or "none" otherwise.
  edNN.json  {"ed", "title", "anchors", "hits", "window", "all_hits", "all_hits_window",
             "diagnostics", "error", "sec"}, always written, last.
             title        the page's own red title text;
             anchors      CSD names found in that title (V1._window). When the title names no
                          CSD, V1._window falls back to the densest cluster of CSD names on the
                          page, so an anchor is a title match only if its name is in the title;
             hits         the CSD names V1._window keeps (anchors plus nearby name matches);
             window       [minx, miny, maxx, maxy] in EPSG:3400 of the hits' envelope buffered by
                          V1.P["window_buf"] (the search window V1 would use), or null for no hits;
             all_hits     every CSD name found anywhere in the page text, with no title anchor and
                          no distance cluster (V1._window drops far hits; if its anchor is a
                          wrong fallback, the clustered window misses the district);
             all_hits_window  the same buffered envelope over all_hits, or null for none;
             diagnostics  V3.last_info without "layers" ({} when the procedure raised before
                          it had a fit; V3.last_info is cleared before every page so a
                          failed page never reports the previous page's numbers);
             error        repr of the exception, or null when placed.

Restartable: an ED whose json already exists is skipped (delete its files to redo it). The json
is written last and atomically, so a run killed mid-page leaves no json and the page is redone.
Deterministic. The sample-leakage guard is lifted for this process only
(STEPB_V3_CALIBRATION_RUN=1), because this script is the registered run.

Run it with the pinned interpreter (PyMuPDF 2.1); other versions read the PDF differently.
Heavy: a page takes 2 to 15 minutes. Run long batches detached, not in a foreground shell.

Usage: python -W ignore analysis/scripts/a10_reconstruct_pages.py OUT_DIR ED [ED ...]
"""
import json
import os
import re
import sys
import time
from pathlib import Path

os.environ["STEPB_V3_CALIBRATION_RUN"] = "1"  # set before the import: V3._guard reads it per call

import geopandas as gpd  # noqa: E402
import numpy as np  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a9_stepb_reconstruct_v3 as V3  # noqa: E402

V1 = V3.V1
CRS = 3400


def _jsonable(v):
    """json default: numpy scalars and arrays (V3.last_info holds both)."""
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        return float(v)
    if isinstance(v, np.ndarray):
        return v.tolist()
    return str(v)


def _write_atomic(path, text):
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def _short(x, nd=4):
    return round(x, nd) if isinstance(x, float) else x


def all_hits(txt):
    """Every CSD (name, geometry) whose name (4+ characters) occurs in the page text, matched exactly as
    V1._window matches them, but with no title anchor and no distance cluster filter."""
    g = V1._csd()
    blob = " | ".join(V1._norm(t) for t in txt)
    return [(nmo, geom) for nm, geom, nmo in zip(g.nm, g.geometry, g.CSDNAME)
            if len(nm) >= 4 and re.search(r"(^|[ |])" + re.escape(nm) + r"($|[ |])", blob)]


def rebuild(n, info):
    """Page polygon -> EPSG:3400 from a fit's p and c, the construction at the end of V3.reconstruct."""
    p, c = np.array(info["p"], float), np.array(info["c"], float)
    poly = V1._evenodd_polygon(V3.R2.extract_page(n)[0])
    geoms = [poly] if poly.geom_type == "Polygon" else list(poly.geoms)
    return unary_union([Polygon(V1._apply(np.array(g.exterior.coords), p[0], p[1], p[2:], c),
                                [V1._apply(np.array(h.coords), p[0], p[1], p[2:], c) for h in g.interiors]).buffer(0)
                        for g in geoms])


def window_bounds(hits):
    """The window V1 searches: hits' envelope buffered by window_buf, as [minx, miny, maxx, maxy]; None if no hits."""
    if not hits:
        return None
    return [float(v) for v in unary_union([h[1] for h in hits]).envelope.buffer(V1.P["window_buf"]).bounds]


def run_page(n, out_dir):
    """Reconstruct page n and write edNN.gpkg (if placed) and edNN.json. Returns the json record."""
    t0 = time.time()
    rec = {"ed": n, "title": None, "anchors": [], "hits": [], "window": None, "all_hits": [],
           "all_hits_window": None, "polygon_status": "none", "diagnostics": {}, "error": None,
           "sec": None}
    stem = out_dir / f"ed{n:02d}"
    for stale in (stem.with_suffix(".gpkg"), out_dir / f"ed{n:02d}.tmp.gpkg"):
        stale.unlink(missing_ok=True)  # a failed redo must not leave the last run's polygon to be loaded as placed
    V3.last_info = {}  # V3.reconstruct sets it only after georeference; never inherit the last page's
    try:
        _outline, _roads, _muni, txt, title = V3.R2.extract_page(n)
        hits, anchors = V1._window(txt, title)
        rec["title"] = title
        rec["anchors"] = [str(a) for a in anchors]
        rec["hits"] = [str(h[0]) for h in hits]
        rec["window"] = window_bounds(hits)
        ah = all_hits(txt)
        rec["all_hits"] = [str(h[0]) for h in ah]
        rec["all_hits_window"] = window_bounds(ah)
    except Exception as e:  # the anchors are advisory; a page whose text cannot be read still gets a go
        rec["anchors_error"] = repr(e)
    g = None
    try:
        g = V3.reconstruct(n)
        if g is None or g.is_empty:
            raise RuntimeError("reconstruction is empty")
    except Exception as e:  # a failed page is a result, never retried by hand
        rec["error"] = repr(e)
        g = None
        info = V3.last_info
        if "fit below the acceptance rule" in str(e) and "p" in info and "c" in info:
            try:  # rejected fit: keep its polygon (flagged), for the merged-hole split
                g = rebuild(n, info)
                rec["polygon_status"] = "rejected"
            except Exception as e2:
                rec["polygon_error"] = repr(e2)
    rec["diagnostics"] = {k: v for k, v in V3.last_info.items() if k != "layers"}
    if g is not None and rec["error"] is None:
        rec["polygon_status"] = "accepted"
    if g is not None:
        tmp = out_dir / f"ed{n:02d}.tmp.gpkg"
        gpd.GeoDataFrame({"ed": [n]}, geometry=[g], crs=CRS).to_file(tmp, driver="GPKG", layer=f"ed{n:02d}")
        os.replace(tmp, stem.with_suffix(".gpkg"))
    rec["sec"] = round(time.time() - t0, 1)
    _write_atomic(stem.with_suffix(".json"), json.dumps(rec, indent=1, default=_jsonable) + "\n")
    return rec, g


def main(argv):
    if len(argv) < 3:
        print(__doc__.split("Usage:")[-1].strip())
        return 2
    out_dir = Path(argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    eds = []
    for a in argv[2:]:
        n = int(a)
        if n not in eds:
            eds.append(n)
    for n in eds:
        if (out_dir / f"ed{n:02d}.json").exists():
            print(f"ED {n:02d} skipped (ed{n:02d}.json exists)", flush=True)
            continue
        rec, g = run_page(n, out_dir)
        d = rec["diagnostics"]
        if rec["error"] is None:
            print(f"ED {n:02d} placed  area_km2={_short(g.area / 1e6)} med_m={_short(d.get('med_dist_m'))} "
                  f"in60={_short(d.get('in60'))} pts={d.get('n_layer_pts')} prior={d.get('prior')} "
                  f"anchors={len(rec['anchors'])} sec={rec['sec']}", flush=True)
        else:
            print(f"ED {n:02d} FAILED  {rec['error']} anchors={len(rec['anchors'])} sec={rec['sec']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
