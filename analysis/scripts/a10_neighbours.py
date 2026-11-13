# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a10_neighbours.py
-----------------

Amendment 10, piece D: read what each Appendix 8 page prints about its NEIGHBOURS, so the
assembled map can be snapped and checked against the pages themselves.

For every page with a ground transform (p, c in edNN.json["diagnostics"]):
  (i)  neighbour_eds   the district numbers printed in grey on the page (labels such as
                       "58 / Cochrane"), excluding the page's own number;
  (ii) boundaries      the polylines of district boundaries drawn on the page, transformed to
                       EPSG:3400 with the page's own transform (V1._apply(pts, p[0], p[1], p[2:], c)).

Boundary stroke style (found on ED 5 and ED 23, tuning pages, 2026-11-03): a grey stroke,
RGB (0.41, 0.41, 0.41), 1.84 pt, solid. It lies a median 1 m from the true boundaries of the
page's own district and its neighbours and every one of its points lies within 30 m of them
(100% on both pages); no other stroke style does (best other: 45% within 30 m). It also retraces
the page's own outline, so each polyline carries own_frac, the share of its length within
OWN_TOL_M of the page's placed outline (1.0 = the page's own edge, 0.0 = a pure neighbour edge).

Neighbour labels are grey (0x4e4e4e on city pages, 0x828282 on most rural pages; the design note's
0x828282 alone misses every city page). The same colours carry survey-grid numbers and place
names, so a number is a label only when it is a line of its own in a text block that goes on
with at least one alphabetic line of the same colour (the district name, often wrapped), and the
printed name is compared with the App. 7 name of that number (name_ok).

Usage:
  python a10_neighbours.py OUT_DIR [ED ...]            write edNN_neighbours.json / .gpkg
  python a10_neighbours.py OUT_DIR --check [--known tuning|fixed] [--out check.json]
      for every placed page, each polyline's median distance to the union of (its own placed
      outline + the known districts' boundaries + the other placed outlines)
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("STEPB_V3_CALIBRATION_RUN", "1")  # reads sample pages' text and strokes only

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import a9_stepb_reconstruct_v3 as V3  # noqa: E402  (page access, transform)

V1 = V3.V1

LABEL_COLOURS = (0x4E4E4E, 0x828282)  # grey text of neighbour labels (city pages, rural pages)
STROKE_RGB = 0.41                     # boundary stroke colour, all three channels
STROKE_RGB_TOL = 0.015                # colour tolerance (PyMuPDF rounds to 2 places)
STROKE_WIDTH = 1.84                   # boundary stroke width, pt
STROKE_WIDTH_TOL = 0.03               # width tolerance, pt
SAMPLE_STEP_PT = 3.0                  # page-point step when densifying strokes for the distance check
OWN_TOL_M = 30.0                      # own_frac: a polyline point this close to the page's outline is "own"
REF_STEP_M = 10.0                     # distance check: reference boundaries are sampled at this step
CHECK_STEP_M = 25.0                   # distance check: ground sampling step along a polyline
NEAR_M = 30.0                         # distance check: "near a reference" threshold
MIN_NAME_KEY = 3                      # name_ok needs at least this many letters of printed name
HEADER_PT, FOOTER_PT = 66.0, 730.0    # city names above/below these page y's are title and footer text
CITIES = ("Calgary", "Edmonton", "St. Albert", "Red Deer", "Lethbridge", "Medicine Hat", "Grande Prairie",
          "Airdrie", "Sherwood Park", "Fort McMurray")  # a city name stands for all its districts


def _key(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("’", "'"))


def _app7_names():
    import a7_stepb_calibrate as C
    import pandas as pd
    a = pd.read_csv(C.APP7).set_index("ed_number")
    return {int(e): _key(r.district) for e, r in a.iterrows()}


# ---- (i) neighbour numbers ---------------------------------------------------------------------

def neighbour_labels(n, names=None):
    """Printed neighbour labels of page n: list of dicts {ed, text, name_ok, size}, one per label.
    The number is either a line of its own or the start of a line ("5 Calgary-"); the name is the rest
    of that line plus the following lines of the block in the same colour."""
    names = _app7_names() if names is None else names
    out = []
    for b in V3._page(n).get_text("dict")["blocks"]:
        lines = b.get("lines", [])
        for i, ln in enumerate(lines):
            sp = ln["spans"]
            if not sp or sp[0]["color"] not in LABEL_COLOURS:
                continue
            m = re.fullmatch(r"\s*(\d{1,2})\s*(.*?)\s*", "".join(x["text"] for x in sp))
            if not m or not 1 <= int(m.group(1)) <= 91 or int(m.group(1)) == n:
                continue
            ed = int(m.group(1))
            rest = ([m.group(2)] if m.group(2) else []) + [
                x["text"].strip() for l2 in lines[i + 1:] for x in l2["spans"] if x["color"] == sp[0]["color"]]
            if not any(re.search(r"[A-Za-z]", r) for r in rest):
                continue  # a survey-grid number (digits only after it)
            name = " ".join(r for r in rest if re.search(r"[A-Za-z]", r))
            k = _key(name)
            words = [_key(w) for w in re.split(r"[\s\-]+", name) if len(_key(w)) >= MIN_NAME_KEY]
            ok = len(k) >= MIN_NAME_KEY and (names[ed].startswith(k) or k.startswith(names[ed])
                                             or (words and all(w in names[ed] for w in words)))  # "Banff-Diamond"
            out.append({"ed": ed, "text": name, "name_ok": bool(ok), "size": round(sp[0]["size"], 1)})
    return out


def city_labels(n):
    """City names printed on the page in ANY colour, font or size (a city's districts are shown under the
    city name): every line, or whole block, whose letters-only text equals a name in CITIES, outside the
    page's own title (colour 0x93241a) and the header and footer bands. Returns (names, styles):
    canonical names, sorted, and one {city, text, colour, size, font, bbox} per hit."""
    keys = {re.sub(r"[^a-z]", "", c.lower()): c for c in CITIES}
    hits = {}
    for b in V3._page(n).get_text("dict")["blocks"]:
        lines = [l for l in b.get("lines", []) if l["spans"]]
        cands = [[l] for l in lines] + ([lines] if len(lines) > 1 else [])
        for grp in cands:
            sp = grp[0]["spans"][0]
            txt = " ".join("".join(x["text"] for x in l["spans"]).strip() for l in grp)
            c = keys.get(re.sub(r"[^a-z]", "", txt.lower()))
            y0, y1 = min(l["bbox"][1] for l in grp), max(l["bbox"][3] for l in grp)
            if c and sp["color"] != 0x93241A and y0 >= HEADER_PT and y1 <= FOOTER_PT:
                hits[(c, round(grp[0]["bbox"][0]), round(y0))] = {
                    "city": c, "text": txt, "colour": hex(sp["color"]), "size": round(sp["size"], 1),
                    "font": sp["font"], "bbox": [round(v) for v in grp[0]["bbox"]]}
    styles = sorted(hits.values(), key=lambda h: (h["city"], h["bbox"]))
    return sorted({h["city"] for h in styles}), styles


# ---- (ii) boundary polylines -------------------------------------------------------------------

def _is_boundary_style(x):
    col, w = x.get("color"), x.get("width")
    if x["type"] not in ("s", "fs") or not col or w is None:
        return False
    return (max(col) - min(col) <= 0.03 and abs(col[0] - STROKE_RGB) <= STROKE_RGB_TOL
            and abs(w - STROKE_WIDTH) <= STROKE_WIDTH_TOL and not x.get("dashes", "[] 0").startswith("[ "))


def boundary_polylines(n, p, c):
    """Boundary strokes of page n as ground-coordinate arrays (vertices in EPSG:3400)."""
    out = []
    for x in V3._page(n).get_drawings():
        if not _is_boundary_style(x):
            continue
        for a in V1._flat(x["items"]):
            g = V1._apply(np.asarray(a, float), p[0], p[1], p[2:], c)
            if len(g) >= 2 and np.hypot(*(g[0] - g[-1])) + np.ptp(g, axis=0).sum() > 0:
                out.append(g)
    return out


def _densify(g, step):
    from shapely.geometry import LineString
    ls = LineString(g)
    n = max(2, int(ls.length / step) + 1)
    return np.array([ls.interpolate(d).coords[0] for d in np.linspace(0, ls.length, n)])


def own_fraction(lines, own_poly, tol=OWN_TOL_M):
    """Per polyline, the share of its length within tol of the page's own placed outline."""
    if own_poly is None:
        return [None] * len(lines)
    import shapely
    ob = own_poly.boundary
    out = []
    for g in lines:
        d = _densify(g, 5.0)
        out.append(float((shapely.distance(shapely.points(d), ob) <= tol).mean()))
    return out


# ---- per-directory driver ----------------------------------------------------------------------

def run_page(out_dir, ed, names, own_poly, labels_only=False):
    """Write edNN_neighbours.json (always) and edNN_neighbours.gpkg (only with a transform)."""
    import geopandas as gpd
    from shapely.geometry import LineString
    out_dir = Path(out_dir)
    j = json.loads((out_dir / f"ed{ed:02d}.json").read_text(encoding="utf-8"))
    d = j.get("diagnostics") or {}
    has_tf = "p" in d and "c" in d
    labels = neighbour_labels(ed, names)
    cities, city_styles = city_labels(ed)
    old = out_dir / f"ed{ed:02d}_neighbours.json"
    fields = dict(neighbour_eds=sorted({x["ed"] for x in labels}),
                  labels=[x["text"] for x in labels] + [c for c in cities],  # printed names + cities, as a10_assemble reads
                  numbered_labels=labels, city_labels=cities, city_label_styles=city_styles,
                  name_mismatches=[x for x in labels if not x["name_ok"]])
    if labels_only and old.exists():  # refresh the label fields, keep the polylines already written
        rec = json.loads(old.read_text(encoding="utf-8"))
        rec.update(fields)
        old.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
        return rec
    lines = boundary_polylines(ed, d["p"], np.array(d["c"])) if has_tf else []
    own = own_fraction(lines, own_poly)
    rec = {"ed": ed, **fields,
           "boundary_style": {"rgb": STROKE_RGB, "width_pt": STROKE_WIDTH} if has_tf else None,
           "n_polylines": len(lines) if has_tf else None,
           "length_km": float(sum(LineString(g).length for g in lines) / 1000.0) if has_tf else None}
    old.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    if has_tf:
        if lines:
            gdf = gpd.GeoDataFrame({"ed": [ed] * len(lines), "own_frac": own,
                                    "geometry": [LineString(g) for g in lines]}, crs=3400)
        else:
            gdf = gpd.GeoDataFrame({"ed": [], "own_frac": []}, geometry=[], crs=3400)
        gdf.to_file(out_dir / f"ed{ed:02d}_neighbours.gpkg", driver="GPKG")
    return rec


def run(out_dir, eds=None, labels_only=False):
    import a10_assemble as A
    polys, pages = A.load_pages(out_dir, with_rejected=False)
    names = _app7_names()
    done, skipped = [], []
    for ed in sorted(pages) if not eds else sorted(eds):
        rec = run_page(out_dir, ed, names, polys.get(ed), labels_only)
        if rec is None:
            skipped.append(ed)
            print(f"ED {ed:2d}  no transform, skipped", flush=True)
            continue
        done.append(rec)
        bad = rec["name_mismatches"]
        print(f"ED {ed:2d}  neighbours {rec['neighbour_eds']}  cities {rec['city_labels']}  polylines {rec['n_polylines']} "
              f"({rec['length_km'] or 0:.1f} km)" + (f"  NAME-MISMATCH {[(x['ed'], x['text']) for x in bad]}" if bad else ""),
              flush=True)
    return done, skipped


# ---- the distance check ------------------------------------------------------------------------

def check(out_dir, known_which=None):
    import geopandas as gpd
    from scipy.spatial import cKDTree
    import a10_assemble as A
    polys, pages = A.load_pages(out_dir, with_rejected=False)
    refs, ref_ed = [], []
    for ed, g in polys.items():  # includes each page's own outline, as specified
        refs.append(g.boundary); ref_ed.append(("placed", ed))
    if known_which:
        app7 = A.load_app7()
        for nm, g in A.known_districts(known_which, app7).items():
            refs.append(g.boundary); ref_ed.append(("known", nm))
    pts = []
    for r in refs:  # reference boundaries as points every REF_STEP_M (nearest-point error <= REF_STEP_M / 2)
        for ls in getattr(r, "geoms", [r]):
            pts.append(_densify(np.array(ls.coords), REF_STEP_M))
    tree = cKDTree(np.vstack(pts))
    rows = []
    for ed in sorted(polys):
        f = Path(out_dir) / f"ed{ed:02d}_neighbours.gpkg"
        if not f.exists():
            continue
        gdf = gpd.read_file(f)
        for g, of in zip(gdf.geometry, gdf.own_frac):
            d = _densify(np.array(g.coords), CHECK_STEP_M)
            dist = tree.query(d)[0]
            rows.append({"ed": ed, "length_m": float(g.length), "own_frac": None if (of is None or of != of) else float(of),
                         "median_m": float(np.median(dist)), "share_near": float((dist <= NEAR_M).mean())})
    if not rows:
        return {"n_polylines": 0}
    med = np.array([r["median_m"] for r in rows]); L = np.array([r["length_m"] for r in rows])
    near = np.array([r["share_near"] for r in rows])
    q = lambda a, p: float(np.percentile(a, p))
    res = {
        "references": {"placed_outlines": len(polys), "known": 0 if not known_which else len([1 for r in ref_ed if r[0] == "known"])},
        "n_polylines": len(rows), "total_length_km": float(L.sum() / 1000),
        "median_of_medians_m": q(med, 50), "p25_m": q(med, 25), "p75_m": q(med, 75), "p90_m": q(med, 90), "max_m": float(med.max()),
        "share_polylines_median_le_30m": float((med <= NEAR_M).mean()),
        "length_weighted_share_points_le_30m": float((near * L).sum() / L.sum()),
        "rows": rows,
    }
    nb = np.array([r["own_frac"] is not None and r["own_frac"] < 0.5 for r in rows])
    if nb.any():  # polylines that are mostly NOT the page's own edge: the informative part
        res["neighbour_only"] = {"n_polylines": int(nb.sum()), "length_km": float(L[nb].sum() / 1000),
                                 "median_of_medians_m": q(med[nb], 50), "p90_m": q(med[nb], 90),
                                 "share_polylines_median_le_30m": float((med[nb] <= NEAR_M).mean()),
                                 "length_weighted_share_points_le_30m": float((near[nb] * L[nb]).sum() / L[nb].sum())}
    byed = {}
    for r in rows:
        byed.setdefault(r["ed"], []).append(r)
    res["per_page"] = {str(ed): {"n": len(v), "length_km": sum(x["length_m"] for x in v) / 1000,
                                 "share_points_le_30m": sum(x["share_near"] * x["length_m"] for x in v) / sum(x["length_m"] for x in v)}
                       for ed, v in byed.items()}
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out_dir")
    ap.add_argument("eds", nargs="*", type=int)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--known", choices=["tuning", "fixed"])
    ap.add_argument("--out")
    ap.add_argument("--labels-only", action="store_true", help="refresh neighbour labels, keep written polylines")
    a = ap.parse_args()
    if a.check:
        res = check(a.out_dir, a.known)
        if a.out:
            Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items() if k not in ("rows", "per_page")})
    else:
        run(a.out_dir, a.eds or None, a.labels_only)


if __name__ == "__main__":
    main()
