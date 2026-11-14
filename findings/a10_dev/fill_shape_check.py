# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
fill_shape_check.py
-------------------

Amendment 10, extra check: do the hole-filled districts have their own page's shape?

A filled district (Edmonton-Windermere, Edmonton-Meadows on the real map) was built from the voting areas
its neighbours left, because its page fit was rejected for overlapping known districts. Its page polygon
(edNN.gpkg) sits wherever that rejected fit put it, but a wrong placement keeps the drawn shape. This fits
the page polygon onto the filled district by a quarter-turn rotation, a uniform scale (set by the area
ratio) and a shift (coarse-to-fine search), and reports overlap (IoU) and the boundary distance. Geometry
only. Reporting only.

Usage: python -W ignore findings/a10_dev/fill_shape_check.py PAGES_DIR SNAP_DIR OUT_JSON ED [ED ...]
"""
import json
import sys

import geopandas as gpd
import numpy as np
from shapely import affinity

PAGES, SNAP, OUT = sys.argv[1:4]
EDS = [int(x) for x in sys.argv[4:]]


def iou(a, b):
    return a.intersection(b).area / a.union(b).area


d = gpd.read_file(f"{SNAP}/districts.gpkg")
rows = []
for ed in EDS:
    fill = d[d.ed == ed].geometry.iloc[0]
    pg = gpd.read_file(f"{PAGES}/ed{ed:02d}.gpkg").to_crs(3400).union_all()
    best = None
    for rot in (0, 90, 180, 270):
        q = affinity.rotate(pg, rot, origin="centroid")
        f = (fill.area / q.area) ** 0.5
        q = affinity.scale(q, f, f, origin="centroid")
        q = affinity.translate(q, fill.centroid.x - q.centroid.x, fill.centroid.y - q.centroid.y)
        for step in (400, 100, 25):
            bx, by, bi = 0.0, 0.0, iou(q, fill)
            for dx in np.linspace(-2 * step, 2 * step, 5):
                for dy in np.linspace(-2 * step, 2 * step, 5):
                    v = iou(affinity.translate(q, dx, dy), fill)
                    if v > bi:
                        bx, by, bi = dx, dy, v
            q = affinity.translate(q, bx, by)
        v = iou(q, fill)
        if best is None or v > best[1]:
            best = (rot, v, q, f)
    rot, v, q, f = best
    b = fill.boundary
    dist = np.array([q.boundary.distance(b.interpolate(i * 25)) for i in range(int(b.length / 25))])
    rows.append({"ed": ed, "district": d[d.ed == ed].district.iloc[0], "rotation_deg": rot, "scale": round(f, 4),
                 "iou": round(v, 4), "boundary_median_m": round(float(np.median(dist)), 1),
                 "boundary_p95_m": round(float(np.percentile(dist, 95)), 1),
                 "stored_fit_centroid_offset_km": round(pg.centroid.distance(fill.centroid) / 1e3, 2)})
    print(rows[-1])
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump({"pages": PAGES, "snap": SNAP, "districts": rows}, fh, indent=1)
