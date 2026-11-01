# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
airdrie_city_limit_anchoring.py
-------------------------------

How much of each Airdrie district's boundary follows Airdrie's city limit, on
Elections Alberta's official 2026 boundaries.

This remeasures `data/outputs/airdrie_quadrant_anchoring.csv`, which was made
on pre-canonical (DPG v0_9/v0_10) geometry by `airdrie_quadrant_anchoring.py`
(v0.9, removed in 5c056ae5; recover it with
`git show 5c056ae5^:analysis/scripts/airdrie_quadrant_anchoring.py`). That
file gave Calgary-Foothills-Airdrie West 0 % city-limit anchoring.

Method A (primary) is that script's measurement, unchanged:
  * walk each district's boundary at 50 m vertex spacing;
  * a vertex is on a substrate when it lies within 500 m of it;
  * a segment counts for a substrate when both its end vertices are on it;
  * substrates in priority order: Airdrie's city limit (2021 CSD 4806021
    boundary), then major OSM highways within 20 km of the city
    (`data/osm/alberta_osm_highways.gpkg`, the file the v0.9 run used);
    the rest is "neither".
Only the inputs change: official boundaries instead of DPG geometry.

Method B (check) is the S3 anchoring rule in `score_anchoring.py`, restricted
to Airdrie's city limit: a segment counts when its head vertex lies within
500 m, and only contiguous runs of at least 1 km count (the 2026-06-12 run
filter).

Method C (check) is the plain shared border: the length of the district's
boundary lying within 20 m of the city limit.

Districts measured: every district holding any Airdrie residents in
`data/outputs/airdrie_split_shares_2026-10-31.json` (correction C45); their
Airdrie residents and shares are copied from that file.

Backward: data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg,
  data/shapefiles/reference/alberta_2021_csds.gpkg,
  data/osm/alberta_osm_highways.gpkg,
  data/outputs/airdrie_split_shares_2026-10-31.json,
  analysis/scripts/score_anchoring.py (Method B rule)
Forward: data/outputs/airdrie_city_limit_anchoring_2026-11-01.csv

Usage
  python analysis/scripts/airdrie_city_limit_anchoring.py [--out PATH]
"""
import argparse
import json
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import linemerge, unary_union
from shapely.strtree import STRtree

REPO = Path(__file__).resolve().parents[2]
MAPS = {
    "majority_2026": "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
    "minority_2026": "data/shapefiles/canonical/ea_minority_2026_eds.gpkg",
}
NAME = "EDName2025"
CSD_GPKG = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"
HIGHWAYS_GPKG = REPO / "data/osm/alberta_osm_highways.gpkg"
SHARES_JSON = REPO / "data/outputs/airdrie_split_shares_2026-10-31.json"
AIRDRIE_CSDUID = "4806021"
WORK_CRS = 3401          # NAD83 / Alberta 10-TM (Forest), metres; as the v0.9 run
SNAP_TOL_M = 500.0       # v0.9 run and score_anchoring.py
VERTEX_DENSIFY_M = 50.0  # v0.9 run and score_anchoring.py
MIN_RUN_M = 1000.0       # score_anchoring.py run filter (Method B)
SHARED_TOL_M = 20.0      # Method C
STUDY_BUFFER_M = 20_000.0  # v0.9: 15 km study box plus 5 km highway buffer
DEFAULT_OUT = REPO / "data/outputs/airdrie_city_limit_anchoring_2026-11-01.csv"


def lines_of(geom):
    if geom.geom_type == "MultiLineString":
        geom = linemerge(geom)
    if geom.geom_type == "LineString":
        return [geom]
    out = []
    for g in getattr(geom, "geoms", []):
        if g.geom_type == "LineString":
            out.append(g)
        elif g.geom_type == "MultiLineString":
            out.extend(g.geoms)
    return out


def densify(ring, step):
    line = LineString(ring.coords)
    n = max(int(np.ceil(line.length / step)), 8)
    return [line.interpolate(d).coords[0] for d in np.linspace(0.0, line.length, n + 1)[:-1]]


def near(pt, lines, tree, tol):
    idx = tree.query(pt.buffer(tol))
    return any(pt.distance(lines[int(i)]) <= tol for i in idx)


def rings(geom):
    polys = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
    for p in polys:
        yield p.exterior
        yield from p.interiors


def measure(geom, substrates):
    """Method A (both end vertices, priority order) and Method B (head vertex,
    runs >= 1 km) for substrate 0 (the city limit)."""
    perim = 0.0
    anchored = [0.0] * len(substrates)
    free = 0.0
    city_runs = 0.0
    for ring in rings(geom):
        coords = densify(ring, VERTEX_DENSIFY_M)
        flags = [[near(Point(c), lines, tree, SNAP_TOL_M) for (lines, tree) in substrates]
                 for c in coords]
        run = 0.0
        for i in range(len(coords)):
            j = (i + 1) % len(coords)
            seg = float(np.hypot(coords[j][0] - coords[i][0], coords[j][1] - coords[i][1]))
            perim += seg
            for s in range(len(substrates)):
                if flags[i][s] and flags[j][s]:
                    anchored[s] += seg
                    break
            else:
                free += seg
            # Method B, as score_anchoring._measure_ring (no wrap-around join)
            if flags[i][0]:
                run += seg
            else:
                if run >= MIN_RUN_M:
                    city_runs += run
                run = 0.0
        if run >= MIN_RUN_M:
            city_runs += run
    return perim, anchored, free, city_runs


def main(out):
    warnings.filterwarnings("ignore")
    csd = gpd.read_file(CSD_GPKG).to_crs(epsg=WORK_CRS)
    airdrie = csd[csd["CSDUID"].astype(str) == AIRDRIE_CSDUID].geometry.iloc[0]
    city_lines = lines_of(airdrie.boundary)
    hw = gpd.read_file(HIGHWAYS_GPKG).to_crs(epsg=WORK_CRS)
    minx, miny, maxx, maxy = airdrie.bounds
    b = STUDY_BUFFER_M
    hw = hw.cx[minx - b:maxx + b, miny - b:maxy + b]
    hw_lines = lines_of(unary_union(list(hw.geometry)))
    substrates = [(city_lines, STRtree(city_lines)), (hw_lines, STRtree(hw_lines))]
    city_limit = MultiLineString(city_lines)
    shares = json.loads(SHARES_JSON.read_text())["maps"]

    rows = []
    for plan, path in MAPS.items():
        eds = gpd.read_file(REPO / path).to_crs(epsg=WORK_CRS).set_index(NAME)
        for d in shares[plan.split("_")[0]]["districts"]:
            geom = eds.loc[d["district"], "geometry"]
            perim, (city_m, hw_m), free_m, runs_m = measure(geom, substrates)
            shared_m = geom.boundary.intersection(city_limit.buffer(SHARED_TOL_M)).length
            rows.append({
                "map": plan,
                "district": d["district"],
                "perimeter_km": perim / 1000,
                "city_limit_km": city_m / 1000,
                "highway_km": hw_m / 1000,
                "neither_km": free_m / 1000,
                "city_limit_pct": 100 * city_m / perim,
                "highway_pct": 100 * hw_m / perim,
                "neither_pct": 100 * free_m / perim,
                "city_limit_runs_1km_km": runs_m / 1000,
                "city_limit_runs_1km_pct": 100 * runs_m / perim,
                "shared_border_20m_km": shared_m / 1000,
                "airdrie_residents_2021": d["airdrie_residents"],
                "share_of_airdrie_pct": 100 * d["share_of_airdrie_held"],
                "share_of_district_airdrie_pct": 100 * d["share_of_district_airdrie"],
            })
    df = pd.DataFrame(rows)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, float_format="%.3f")
    print(df.drop(columns=["map"]).to_string(index=False, float_format=lambda v: f"{v:.2f}"))
    print(f"\nAirdrie city limit (2021 CSD): {city_limit.length / 1000:.2f} km")
    print(f"wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    main(ap.parse_args().out)
