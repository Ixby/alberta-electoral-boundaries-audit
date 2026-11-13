#!/usr/bin/env python3
"""s15_distances.py -- the s.15(2)(b) distance for the special districts, on the audit's own road model.

EXPLORATORY. Computed after the fact for the 2026-11-10 audit. Not a registered test.

EBCA s.15(2)(b): "the distance from the Legislature Building in Edmonton to the nearest
boundary of the proposed electoral division by the most direct highway route is more than
150 kilometres". The audit's road model is committed (analysis/scripts/s152_criteria.py over
data/osm/alberta_osm_highways.gpkg), so the distance can be computed for each district as drawn.

Method (the s152_criteria.py method, applied to the official district polygons): build a graph
from every line in the OpenStreetMap highways extract (vertices snapped to 1 m, edge weight =
length in EPSG:3400), start at the vertex nearest the Legislature Building (the same
coordinates as s152_criteria.py), run Dijkstra, and take the smallest road distance to any
road vertex that lies inside the district. Because roads enter a district across its boundary,
this is the model's distance to the nearest boundary by road, to within one vertex spacing.

Three figures are given for each district:
  road_km_to_nearest_vertex_inside  the method above, on the official polygon
  road_km_from_committed_va_file    the smallest road_km in data/outputs/s152_va_criteria.csv over
                                    the voting areas whose representative point is in the district
                                    (the audit's existing per-voting-area output; a cross-check)
  straight_line_km                  Legislature to the polygon, as the crow flies: no route can be shorter

Also checked: which minority district holds the Town of Rimbey, since the report uses Rimbey's
road distance as a stand-in for Rocky Mountain House-Banff Park's nearest boundary.

Inputs : data/osm/alberta_osm_highways.gpkg, data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg,
         data/shapefiles/canonical/va_2023_election_day_votes.gpkg, data/outputs/s152_va_criteria.csv,
         data/shapefiles/reference/alberta_2021_csds.gpkg      (.gpkg files are Git LFS objects)
Output : findings/audit_2026-11-10/s15_distances.json
Run    : python findings/audit_2026-11-10/s15_distances.py   (no network, no randomness; ~1 min)
"""
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from shapely.geometry import Point
from shapely.ops import nearest_points

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().with_suffix(".json")
LEGISLATURE = (-113.506611, 53.533694)  # lon, lat; as in analysis/scripts/s152_criteria.py
CRS = 3400
LIMIT_KM = 150.0
SPECIAL = {
    "majority": ["Central Peace-Notley", "Lesser Slave Lake", "Canmore-Banff"],
    "minority": ["Central Peace-Notley", "Lesser Slave Lake", "Rocky Mountain House-Banff Park"],
}
PUBLISHED = {  # reports/academic/report_academic.md s.5.1.4, "Criteria met (of 5)"
    ("majority", "Central Peace-Notley"): "5", ("majority", "Lesser Slave Lake"): "4", ("majority", "Canmore-Banff"): "3",
    ("minority", "Central Peace-Notley"): "5", ("minority", "Lesser Slave Lake"): "4",
    ("minority", "Rocky Mountain House-Banff Park"): "4 or 5 (b borderline)",
}


def road_graph():
    roads = gpd.read_file(ROOT / "data/osm/alberta_osm_highways.gpkg").to_crs(CRS).explode(index_parts=False)
    coords, src, dst, w = {}, [], [], []

    def nid(xy):
        key = (round(xy[0]), round(xy[1]))
        if key not in coords:
            coords[key] = len(coords)
        return coords[key]

    for geom in roads.geometry:
        pts = list(geom.coords)
        for a, b in zip(pts[:-1], pts[1:]):
            i, j = nid(a), nid(b)
            if i != j:
                src.append(i)
                dst.append(j)
                w.append(float(np.hypot(b[0] - a[0], b[1] - a[1])))
    n = len(coords)
    m = coo_matrix((w + w, (src + dst, dst + src)), shape=(n, n)).tocsr()
    xy = np.array(list(coords.keys()), float)
    leg = gpd.GeoSeries([Point(LEGISLATURE)], crs=4326).to_crs(CRS).iloc[0]
    start = int(np.argmin(np.hypot(xy[:, 0] - leg.x, xy[:, 1] - leg.y)))
    snap_m = float(np.hypot(xy[start, 0] - leg.x, xy[start, 1] - leg.y))
    dist = dijkstra(m, indices=start) + snap_m
    verts = gpd.GeoDataFrame({"d_km": dist / 1000.0}, geometry=gpd.points_from_xy(xy[:, 0], xy[:, 1]), crs=CRS)
    info = {"vertices": int(n), "segments": int(len(w)), "legislature_snap_m": round(snap_m, 1),
            "vertices_unreachable": int((~np.isfinite(dist)).sum())}
    return verts[np.isfinite(verts["d_km"])], leg, info


def ll(p):
    q = gpd.GeoSeries([p], crs=CRS).to_crs(4326).iloc[0]
    return [round(q.y, 4), round(q.x, 4)]


def main():
    verts, leg, info = road_graph()
    va = gpd.read_file(ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg").to_crs(CRS)
    va_km = pd.read_csv(ROOT / "data/outputs/s152_va_criteria.csv").set_index("node")["road_km"]
    assert len(va) == len(va_km) == 4765
    rep = gpd.GeoDataFrame({"road_km": va_km.reindex(range(len(va))).values}, geometry=va.geometry.representative_point(), crs=CRS)
    csd = gpd.read_file(ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(CRS)
    rimbey = csd[(csd.CSDNAME == "Rimbey") & (csd.CSDTYPE == "T")].geometry.iloc[0]
    rim_v = verts[verts.within(rimbey)]
    out = {
        "status": "EXPLORATORY - computed after the fact for the 2026-11-10 audit; not a registered test",
        "statute": "EBCA s.15(2)(b): more than 150 km from the Legislature Building to the nearest boundary of the division by the most direct highway route",
        "road_model": dict(info, source="data/osm/alberta_osm_highways.gpkg", method="analysis/scripts/s152_criteria.py road_km(), applied to official district polygons",
                           legislature_lon_lat=list(LEGISLATURE)),
        "districts": {},
    }
    rim_home = {}
    for mkey, names in SPECIAL.items():
        ed = gpd.read_file(ROOT / f"data/shapefiles/canonical/ea_{mkey}_2026_eds.gpkg").to_crs(CRS)
        rim_home[mkey] = {
            "district_holding_most_of_the_town": ed.EDName2025.iloc[int(ed.geometry.intersection(rimbey).area.values.argmax())],
            "share_of_town_area_in_it_pct": round(100 * float(ed.geometry.intersection(rimbey).area.max() / rimbey.area), 1)}
        out["districts"][mkey] = {}
        for name in names:
            poly = ed.loc[ed.EDName2025 == name, "geometry"].iloc[0]
            inside = verts[verts.within(poly)]
            i = inside["d_km"].idxmin()
            vin = rep[rep.within(poly)]
            b = nearest_points(poly, leg)[0]
            d = float(inside.loc[i, "d_km"])
            out["districts"][mkey][name] = {
                "road_km_to_nearest_vertex_inside": round(d, 1),
                "entry_point_lat_lon": ll(inside.loc[i, "geometry"]),
                "road_vertices_inside": int(len(inside)),
                "road_km_from_committed_va_file": round(float(vin["road_km"].min()), 1),
                "voting_areas_inside": int(len(vin)),
                "straight_line_km": round(float(poly.distance(leg)) / 1000.0, 1),
                "straight_line_nearest_point_lat_lon": ll(b),
                "criterion_b_met_on_road_model": bool(d > LIMIT_KM),
                "margin_km": round(d - LIMIT_KM, 1),
                "criteria_met_as_published": PUBLISHED[(mkey, name)],
            }
    out["rimbey_check"] = {
        "why": "The report puts Rocky Mountain House-Banff Park's nearest boundary 'at about 143-145 km using Rimbey as a proxy'.",
        "town_of_rimbey_is_in": rim_home,
        "rimbey_in_minority_rocky_mountain_house_banff_park": bool(
            rim_home["minority"]["district_holding_most_of_the_town"] == "Rocky Mountain House-Banff Park"),
        "road_km_to_rimbey_on_this_model": round(float(rim_v["d_km"].min()), 1) if len(rim_v) else None,
    }
    d = out["districts"]
    rmh, lsl_min, lsl_maj = d["minority"]["Rocky Mountain House-Banff Park"], d["minority"]["Lesser Slave Lake"], d["majority"]["Lesser Slave Lake"]
    out["summary"] = {
        "rocky_mountain_house_banff_park_minority_km": rmh["road_km_to_nearest_vertex_inside"],
        "rocky_mountain_house_banff_park_meets_b": rmh["criterion_b_met_on_road_model"],
        "lesser_slave_lake_km": {"majority": lsl_maj["road_km_to_nearest_vertex_inside"], "minority": lsl_min["road_km_to_nearest_vertex_inside"]},
        "lesser_slave_lake_meets_b": {"majority": lsl_maj["criterion_b_met_on_road_model"], "minority": lsl_min["criterion_b_met_on_road_model"]},
        "reading": "On the audit's own road model the minority's Rocky Mountain House-Banff Park is beyond 150 km (criterion (b) met, not "
                   "borderline), and Lesser Slave Lake is within 150 km on both maps (criterion (b) not met). The published counts "
                   "treat them the other way round: (b) is hedged for the first and credited for the second.",
        "what_this_does_not_change": "Whether each district still has at least three of the five criteria depends on the other four "
                                     "criteria, which this script does not recompute.",
    }
    out["limits"] = [
        "A model, not a surveyed highway route: shortest path over an OpenStreetMap extract of highways (about 41,500 km of road, "
        "no road names or classes in the file, no one-way rules). Local roads are not in it. If local roads counted as a 'highway route', "
        "a district whose nearest corner has no highway could be closer than the model says: Rocky Mountain House-Banff Park is only "
        "about 105 km away in a straight line, so its 165 km rests on the road model. Lesser Slave Lake is under 150 km on the model "
        "and no reading that adds roads can lengthen a shortest path.",
        "Distance is to the first road vertex inside the district, so it overstates the distance to the boundary line by up to one vertex spacing.",
        "The straight-line figure is a floor for any route; where it is already over 150 km the answer does not depend on the road model.",
        "The Legislature's coordinates and the 1 m vertex snap are those of s152_criteria.py.",
    ]
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for mkey in d:
        for name, r in d[mkey].items():
            print(f"{mkey:9s} {name:34s} road {r['road_km_to_nearest_vertex_inside']:6.1f} km  (VA file {r['road_km_from_committed_va_file']:6.1f})  "
                  f"straight {r['straight_line_km']:6.1f}  (b) met: {r['criterion_b_met_on_road_model']}  entry {r['entry_point_lat_lon']}")
    print(json.dumps(out["rimbey_check"]))


if __name__ == "__main__":
    main()
