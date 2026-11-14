# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
near_line_vas.py
----------------

Amendment 10, extra check: the voting areas (VAs) whose representative point lies near a changed line.

A VA goes to the district holding its representative point, so only a VA whose point sits within the line's
error of a changed line could be assigned the wrong way. For every VA whose point is within NEAR_M of a
changed district's boundary (not the province's edge), this lists every drawing of that line on the PDF:
  - the page polygon of each placed district on either side (edNN.gpkg): is the point inside it?
  - the grey neighbour lines on every page (edNN_neighbours.gpkg) passing within NEAR_M of the point,
    with the point's distance to them;
each with its page's scale (metres per point, from the page fit) and the drawing grid on the ground
(GRID_PT points of page coordinate, the step the map's vertices are stored on). The verdict:
  settled    every polygon drawing agrees with the assignment, and the point lies at least 3 grid steps
             from the nearest drawing on the finest-scale page that draws the line
  review     otherwise
Population only; no votes. Reporting only.

Usage: python -W ignore findings/a10_dev/near_line_vas.py PAGES_DIR SNAP_DIR OUT_JSON
"""
import json
import sys

sys.path.insert(0, "analysis/scripts")
import geopandas as gpd  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import shapely  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

import a10_assemble as A  # noqa: E402

NEAR_M = 100.0
GRID_PT = 0.092
PAGES, SNAP, OUT = sys.argv[1:4]

va, _ = A.C.me.build_va_graph(verbose=False)
va = va[[c for c in va.columns if c in ("OBJECTID", "VA_NUMBER", "pop_2021", "geometry")]].to_crs(3400)
rp = va.geometry.representative_point()
asg = pd.read_csv(f"{SNAP}/va_assignment.csv")
with open(f"{SNAP}/report.json", encoding="utf-8") as f:
    rep = json.load(f)
src = {r["ed"]: r["source"] for r in rep["districts"]}
d = gpd.read_file(f"{SNAP}/districts.gpkg")
geom = dict(zip(d.ed, d.geometry))
prov = unary_union(list(geom.values())).boundary.buffer(5)
lines = unary_union([geom[e].boundary for e, s in src.items() if s != "known"]).difference(prov)
dist = np.asarray(shapely.distance(rp.values, lines))


def page(ed):
    try:
        with open(f"{PAGES}/ed{ed:02d}.json", encoding="utf-8") as f:
            j = json.load(f)
        return (j.get("diagnostics") or {}).get("s")
    except FileNotFoundError:
        return None


poly = {e: gpd.read_file(f"{PAGES}/ed{e:02d}.gpkg").to_crs(3400).union_all() for e, s in src.items() if s == "placed"}
grey = {}
for e in src:
    try:
        g = gpd.read_file(f"{PAGES}/ed{e:02d}_neighbours.gpkg").to_crs(3400)
        grey[e] = unary_union(list(g.geometry))
    except Exception:
        pass

rows = []
for i in np.flatnonzero(dist < NEAR_M):
    p, c = rp.iloc[i], int(asg.ed.iloc[i])
    others = sorted(((float(geom[e].distance(p)), e) for e in geom if e != c))[:1]
    o = others[0][1]
    draws = []
    for e in (c, o):
        if e in poly:
            s = page(e)
            inside = bool(poly[e].contains(p))
            draws.append({"page": e, "kind": "polygon", "scale_m_per_pt": s, "grid_m": GRID_PT * s if s else None,
                          "point_inside": inside, "agrees": inside == (e == c),
                          "distance_m": round(float(poly[e].boundary.distance(p)), 1)})
    for e, gl in grey.items():
        dd = float(gl.distance(p))
        if dd < NEAR_M:
            s = page(e)
            draws.append({"page": e, "kind": "grey line", "scale_m_per_pt": s, "grid_m": GRID_PT * s if s else None,
                          "distance_m": round(dd, 1)})
    scaled = [x for x in draws if x["grid_m"]]
    finest = min(scaled, key=lambda x: x["grid_m"]) if scaled else None
    settled = all(x.get("agrees", True) for x in draws) and finest is not None and finest["distance_m"] >= 3 * finest["grid_m"]
    rows.append({"OBJECTID": int(asg.OBJECTID.iloc[i]), "VA_NUMBER": str(asg.VA_NUMBER.iloc[i]), "assigned_ed": c,
                 "other_ed": o, "pop_2021": float(va.pop_2021.iloc[i]), "point_to_final_line_m": round(float(dist[i]), 1),
                 "finest_page": finest and finest["page"], "finest_grid_m": finest and round(finest["grid_m"], 2),
                 "verdict": "settled" if settled else "review", "drawings": draws})
    print(rows[-1]["OBJECTID"], c, o, rows[-1]["point_to_final_line_m"], rows[-1]["verdict"],
          [(x["page"], x["kind"][0], x["distance_m"], x.get("agrees")) for x in draws])
summary = {"near_m": NEAR_M, "n": len(rows), "settled": sum(r["verdict"] == "settled" for r in rows),
           "review": sum(r["verdict"] == "review" for r in rows),
           "pop_review": sum(r["pop_2021"] for r in rows if r["verdict"] == "review")}
print(summary)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump({"pages": PAGES, "snap": SNAP, "summary": summary, "vas": rows}, f, indent=1)
