#!/usr/bin/env python3
"""calgary_zone_recode.py -- the Calgary zone gap under the committed lists and under the stated rule.

EXPLORATORY. Computed after the fact for the 2026-11-10 audit. Not a registered test.

The Calgary test (A2) splits Calgary's districts into Zone A (north / east / central) and
Zone B (south / west) and compares their average populations. The report states the rule as:
Zone A = districts "whose territorial centroid lies north or east of a dividing line running
along the Bow River through downtown and then southeast along Deerfoot Trail". The committed
lists (CALGARY_ZONE_A / _B in analysis/scripts/electoral_forensics_population.py) were drawn
up by name and do not follow that rule everywhere. This script applies the rule literally to
the official boundary files and reports the gap under each coding, for both commission maps.

Codings
  committed_lists      the lists as committed (read from the script's source, not retyped).
  published_3_recode   the report's own partial recode (minority only: Calgary-Buffalo and
                       Calgary-Currie to Zone B, Calgary-Peigan-Chestermere to Zone A).
  literal_bow_to_crossing    the line follows the Bow River downstream until the river first
                       crosses Deerfoot Trail (about 51.009 N), then follows Deerfoot south.
  literal_handoff_at_nearest_approach  the line leaves the Bow where the river, coming east
                       past downtown, first stops closing on Deerfoot Trail (about 51.044 N,
                       near the zoo, about 115 m from the freeway) and follows Deerfoot from there.
  literal_nolan_hill_cochrane_in_a   (minority only) as literal, but Calgary-Nolan Hill-Cochrane
                       kept in Zone A. This equals the auditors' scratch recode of five districts.
The rule is silent on two things, and each matters for exactly one district:
  * where the line passes from the river to the freeway. The two hand-off readings differ only
    for a centroid in the strip between the river and the freeway south of the zoo (about 5 km
    of river, at most about 650 m wide). The majority map's Calgary-Confluence centroid is in it.
  * what the line does west of the city. Followed up the Bow, it puts the centroid of the
    minority map's Calgary-Nolan Hill-Cochrane (which lies west of Cochrane, 3 km south of the
    river) in Zone B, although the district's Calgary part is in the far north-west.

Geometry (all committed; the .gpkg files are Git LFS objects, so `git lfs pull` first)
  districts  data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg; centroid = the
             polygon's geometric centroid, EPSG:3400.
  Deerfoot   data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg, RTNUMBER1 == "2" (Highway 2,
             which is Deerfoot Trail through Calgary), ramps and service lanes dropped. Its
             easting at a given northing is the mean easting of the carriageways there.
  Bow River  data/osm/alberta_osm_rivers.gpkg. The file has no names, so the Bow is identified
             by position: the one river line that passes within 300 m of both Bowness
             (51.092 N, 114.190 W) and Prince's Island (51.055 N, 114.070 W).
  population data/reference/{majority,minority}_2026_populations.csv (the commission's tables,
             the figures the published 12.2% uses).
Zone B is the set of centroids inside the region south-west of the dividing line.

Output: findings/audit_2026-11-10/calgary_zone_recode.json and calgary_zone_recode_districts.csv
Run   : python findings/audit_2026-11-10/calgary_zone_recode.py   (no network, no randomness)
"""
import ast
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import substring, unary_union

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SRC_LISTS = ROOT / "analysis/scripts/electoral_forensics_population.py"
WINDOW_LL = (-114.75, 50.75, -113.70, 51.35)  # lon/lat window around Calgary
ANCHORS_LL = {"Bowness": (-114.190, 51.092), "Prince's Island": (-114.070, 51.055)}
STEP = 25.0  # metres, sampling step along the lines


def norm(name):
    return name.replace("Mountainview", "Mountain View")


def committed_lists():
    tree = ast.parse(SRC_LISTS.read_text(encoding="utf-8"))
    got = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") in ("CALGARY_ZONE_A", "CALGARY_ZONE_B"):
            got[node.targets[0].id] = set(ast.literal_eval(node.value))
    return got["CALGARY_ZONE_A"], got["CALGARY_ZONE_B"]


def build_lines():
    win = gpd.GeoSeries([box(*WINDOW_LL)], crs=4326).to_crs(3400)
    wb = tuple(win.total_bounds)
    # Deerfoot Trail = Highway 2, carriageways only
    nrn = gpd.read_file(ROOT / "data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg", bbox=wb)
    h2 = nrn[(nrn.RTNUMBER1.astype(str) == "2") & (~nrn.ROADCLASS.isin(["Ramp", "Service Lane"]))]
    H = unary_union(h2.geometry.values)
    y0, y1 = H.bounds[1], H.bounds[3]

    def deerfoot_x(y):
        hit = H.intersection(LineString([(wb[0] - 1e5, y), (wb[2] + 1e5, y)]))
        if hit.is_empty:
            return None
        xs = [g.x for g in getattr(hit, "geoms", [hit]) if g.geom_type == "Point"]
        return float(np.mean(xs)) if xs else None

    # Bow River: the unnamed line that passes both anchors
    riv = gpd.read_file(ROOT / "data/osm/alberta_osm_rivers.gpkg", bbox=WINDOW_LL).to_crs(3400)
    anchors = gpd.GeoSeries([Point(*v) for v in ANCHORS_LL.values()], crs=4326).to_crs(3400)
    near = np.all([riv.distance(a).values < 300 for a in anchors], axis=0)
    assert near.sum() == 1, "expected exactly one river line through both anchors"
    bow = riv.geometry.values[near][0]
    c = np.array(bow.coords)
    if c[0][0] > c[-1][0]:  # orient west -> east (downstream)
        bow = LineString(c[::-1])
    # first crossing of Deerfoot going downstream
    cross = bow.intersection(H)
    s_cross = min(bow.project(g) for g in getattr(cross, "geoms", [cross]))
    # Hand-off by nearest approach: going downstream from Prince's Island, the first point where the
    # river stops closing on Deerfoot (first minimum of the river-to-freeway distance, taken over
    # a +/-300 m window, sampled every STEP metres).
    s_start = bow.project(anchors.iloc[1])
    ss = np.arange(s_start, s_cross - 100.0, STEP)
    dist = np.array([H.distance(bow.interpolate(s)) for s in ss])
    w = int(300 / STEP)
    i_near = next(i for i in range(w, len(ss) - w) if dist[i] <= dist[i - w:i + w + 1].min())
    return {"H": H, "deerfoot_x": deerfoot_x, "deerfoot_y_range": (y0, y1), "bow": bow, "s_cross": float(s_cross),
            "s_near": float(ss[i_near]), "d_near": float(dist[i_near]), "n_h2_segments": int(len(h2))}


def zone_b_region(L, s_handoff):
    """Polygon south-west of: Bow (west end -> hand-off), then Deerfoot south from the hand-off's northing."""
    bow = L["bow"]
    upper = substring(bow, 0.0, s_handoff)
    pts = list(upper.coords)
    yh = pts[-1][1]
    y_south = L["deerfoot_y_range"][0]
    for y in np.arange(yh, y_south, -STEP):
        x = L["deerfoot_x"](y)
        if x is not None:
            pts.append((x, float(y)))
    xw, yw = pts[0]
    far_w, far_s = xw - 50_000.0, y_south - 50_000.0
    pts += [(pts[-1][0], far_s), (far_w, far_s), (far_w, yw)]
    poly = Polygon(pts)
    if not poly.is_valid:
        poly = poly.buffer(0)
    return poly


def gap_stats(df, zone_col, prov_mean):
    a, b = df[df[zone_col] == "A"], df[df[zone_col] == "B"]
    ma, mb = float(a.population.mean()), float(b.population.mean())
    return {"n_zone_a": int(len(a)), "mean_zone_a": round(ma, 1), "n_zone_b": int(len(b)), "mean_zone_b": round(mb, 1),
            "gap_persons": round(ma - mb, 1), "gap_pct": round(100.0 * (ma - mb) / mb, 3),
            "zone_a_excess_over_provincial_mean_pct": round(100.0 * (ma / prov_mean - 1.0), 3),
            "zone_b_excess_over_provincial_mean_pct": round(100.0 * (mb / prov_mean - 1.0), 3)}


def main():
    ZA, ZB = committed_lists()
    L = build_lines()
    bow, H = L["bow"], L["H"]
    regions = {"literal_bow_to_crossing": zone_b_region(L, L["s_cross"]),
               "literal_handoff_at_nearest_approach": zone_b_region(L, L["s_near"])}
    to_ll = lambda p: [round(v, 4) for v in gpd.GeoSeries([p], crs=3400).to_crs(4326).iloc[0].coords[0]][::-1]
    strip = regions["literal_handoff_at_nearest_approach"].difference(regions["literal_bow_to_crossing"])
    rows, results = [], {}
    for mkey in ("majority", "minority"):
        ed = gpd.read_file(ROOT / f"data/shapefiles/canonical/ea_{mkey}_2026_eds.gpkg").to_crs(3400)
        pop = pd.read_csv(ROOT / f"data/reference/{mkey}_2026_populations.csv")
        pop["ed_name"] = pop["ed_name"].map(norm)
        prov_mean = float(pop.population.sum()) / len(pop)
        cal = pop[pop.ed_name.str.startswith("Calgary")].copy()
        g = ed.set_index(ed.EDName2025.map(norm)).geometry
        assert set(cal.ed_name) <= set(g.index), set(cal.ed_name) - set(g.index)
        cal["committed_lists"] = ["A" if n in ZA or n.replace("Mountain View", "Mountainview") in ZA
                                  else "B" if n in ZB else "?" for n in cal.ed_name]
        assert (cal.committed_lists != "?").all()
        cal["published_3_recode"] = cal["committed_lists"]
        if mkey == "minority":
            cal.loc[cal.ed_name.isin(["Calgary-Buffalo", "Calgary-Currie"]), "published_3_recode"] = "B"
            cal.loc[cal.ed_name == "Calgary-Peigan-Chestermere", "published_3_recode"] = "A"
        cen = {n: g[n].centroid for n in cal.ed_name}
        for name, reg in regions.items():
            cal[name] = ["B" if reg.contains(cen[n]) else "A" for n in cal.ed_name]
        # distances for the table
        upper = substring(bow, 0.0, L["s_cross"])
        ll = [to_ll(cen[n]) for n in cal.ed_name]
        cal["centroid_lat"], cal["centroid_lon"] = [v[0] for v in ll], [v[1] for v in ll]
        cal["km_east_of_deerfoot"] = [round((cen[n].x - L["deerfoot_x"](cen[n].y)) / 1000.0, 2) for n in cal.ed_name]
        cal["km_to_nearest_deerfoot_carriageway"] = [round(cen[n].distance(H) / 1000.0, 2) for n in cal.ed_name]
        cal["km_to_bow_upstream_of_crossing"] = [round(cen[n].distance(upper) / 1000.0, 2) for n in cal.ed_name]
        cal["in_strip_between_bow_and_deerfoot"] = [bool(strip.contains(cen[n])) for n in cal.ed_name]
        codings = ["committed_lists", "published_3_recode", "literal_bow_to_crossing", "literal_handoff_at_nearest_approach"]
        cal["literal_nolan_hill_cochrane_in_a"] = cal["literal_bow_to_crossing"]
        if mkey == "minority":
            assert (cal.literal_bow_to_crossing == cal.literal_handoff_at_nearest_approach).all()
            cal.loc[cal.ed_name == "Calgary-Nolan Hill-Cochrane", "literal_nolan_hill_cochrane_in_a"] = "A"
            codings.append("literal_nolan_hill_cochrane_in_a")
        results[mkey] = {
            "n_calgary_districts": int(len(cal)), "provincial_mean_population": round(prov_mean, 1),
            "codings": {c: gap_stats(cal, c, prov_mean) for c in codings},
            "districts_whose_zone_differs_from_committed": {
                c: {n: f"{a}->{b}" for n, a, b in zip(cal.ed_name, cal.committed_lists, cal[c]) if a != b}
                for c in codings[1:]},
            "districts_in_strip": list(cal.ed_name[cal.in_strip_between_bow_and_deerfoot]),
        }
        for r in cal.itertuples():
            rows.append({"map": mkey, "district": r.ed_name, "population": int(r.population),
                         "centroid_lat": r.centroid_lat, "centroid_lon": r.centroid_lon,
                         "km_east_of_deerfoot": r.km_east_of_deerfoot,
                         "km_to_nearest_deerfoot_carriageway": r.km_to_nearest_deerfoot_carriageway,
                         "km_to_bow_upstream_of_crossing": r.km_to_bow_upstream_of_crossing,
                         "in_strip_between_bow_and_deerfoot": r.in_strip_between_bow_and_deerfoot,
                         "zone_committed_lists": r.committed_lists, "zone_published_3_recode": r.published_3_recode,
                         "zone_literal_bow_to_crossing": r.literal_bow_to_crossing,
                         "zone_literal_handoff_at_nearest_approach": r.literal_handoff_at_nearest_approach,
                         "zone_literal_nolan_hill_cochrane_in_a": r.literal_nolan_hill_cochrane_in_a})
    # the April 24 "2x" rule: PASSING if minority zone-gap <= 2 x majority zone-gap
    rule = {}
    pairs = {"committed_lists": ("committed_lists", "committed_lists"),
             "published_3_recode": ("published_3_recode", "published_3_recode"),
             "literal: Confluence A (bow_to_crossing), Nolan Hill-Cochrane B": ("literal_bow_to_crossing", "literal_bow_to_crossing"),
             "literal: Confluence B (handoff_at_nearest_approach), Nolan Hill-Cochrane B": ("literal_handoff_at_nearest_approach", "literal_bow_to_crossing"),
             "literal: Confluence A, Nolan Hill-Cochrane A (auditors' five-district recode)": ("literal_bow_to_crossing", "literal_nolan_hill_cochrane_in_a"),
             "literal: Confluence B, Nolan Hill-Cochrane A": ("literal_handoff_at_nearest_approach", "literal_nolan_hill_cochrane_in_a")}
    for name, (cmaj, cmin) in pairs.items():
        gmaj = results["majority"]["codings"][cmaj]["gap_pct"]
        gmin = results["minority"]["codings"][cmin]["gap_pct"]
        rule[name] = {
            "majority_coding": cmaj, "minority_coding": cmin,
            "majority_gap_pct": gmaj, "minority_gap_pct": gmin,
            "magnitudes": {"twice_majority": round(2 * abs(gmaj), 3),
                           "minority_exceeds_twice_majority": bool(abs(gmin) > 2 * abs(gmaj)),
                           "margin_pts": round(abs(gmin) - 2 * abs(gmaj), 3)},
            "signed_as_written": {"twice_majority": round(2 * gmaj, 3), "minority_exceeds_twice_majority": bool(gmin > 2 * gmaj)},
            "public_report_measure": {
                "zone_a_excess_majority_pct": results["majority"]["codings"][cmaj]["zone_a_excess_over_provincial_mean_pct"],
                "zone_a_excess_minority_pct": results["minority"]["codings"][cmin]["zone_a_excess_over_provincial_mean_pct"],
                "minority_above_5pct": bool(results["minority"]["codings"][cmin]["zone_a_excess_over_provincial_mean_pct"] > 5.0)},
        }
    out = {
        "status": "EXPLORATORY - computed after the fact for the 2026-11-10 audit; not a registered test",
        "rule_as_stated": "Zone A: centroid north or east of a line along the Bow River through downtown, then southeast along Deerfoot Trail. Zone B: south or west of it.",
        "april_24_rule": "A2 passes if the minority's zone gap is no more than twice the majority's (v0_1_null_hypothesis_and_exoneration_criteria.md, commit fa10c8a0). 'Fires' below means the minority's gap is more than twice the majority's.",
        "line_construction": {
            "highway_2_carriageway_segments": L["n_h2_segments"],
            "bow_first_crosses_deerfoot_at_lat_lon": to_ll(bow.interpolate(L["s_cross"])),
            "bow_nearest_approach_before_crossing_at_lat_lon": to_ll(bow.interpolate(L["s_near"])),
            "bow_nearest_approach_distance_m": round(L["d_near"], 1),
            "strip_between_the_two_readings_km2": round(strip.area / 1e6, 3),
            "strip_length_along_river_km": round((L["s_cross"] - L["s_near"]) / 1000.0, 2),
        },
        "summary": {
            "minority_gap_pct": {"committed_lists": results["minority"]["codings"]["committed_lists"]["gap_pct"],
                                 "published_3_recode": results["minority"]["codings"]["published_3_recode"]["gap_pct"],
                                 "literal": results["minority"]["codings"]["literal_bow_to_crossing"]["gap_pct"],
                                 "literal_nolan_hill_cochrane_in_a": results["minority"]["codings"]["literal_nolan_hill_cochrane_in_a"]["gap_pct"]},
            "majority_gap_pct": {"committed_lists": results["majority"]["codings"]["committed_lists"]["gap_pct"],
                                 "literal_confluence_in_a": results["majority"]["codings"]["literal_bow_to_crossing"]["gap_pct"],
                                 "literal_confluence_in_b": results["majority"]["codings"]["literal_handoff_at_nearest_approach"]["gap_pct"]},
            "two_times_rule_fires_on_magnitudes": {k: v["magnitudes"]["minority_exceeds_twice_majority"] for k, v in rule.items()},
            "two_times_rule_fires_signed": {k: v["signed_as_written"]["minority_exceeds_twice_majority"] for k, v in rule.items()},
            "minority_zone_a_above_5pct_of_provincial_mean_under_every_coding": bool(all(
                c["zone_a_excess_over_provincial_mean_pct"] > 5.0 for c in results["minority"]["codings"].values())),
            "the_two_districts_at_issue": "Calgary-Hays and Calgary-South East: coded Zone B in the committed lists and left there by the "
                                          "published recode; their centroids are east of Deerfoot Trail on both maps, so the stated rule puts them in Zone A.",
        },
        "maps": results,
        "april_24_two_times_rule": rule,
        "limits": [
            "The stated rule does not say where the line passes from the river to the freeway; two readings are given. "
            "They differ only for Calgary-Confluence on the majority map.",
            "The stated rule does not say what the line does west of the city. Followed up the Bow it moves the minority's "
            "Calgary-Nolan Hill-Cochrane to Zone B; a variant keeps it in Zone A.",
            "A centroid is one point: Calgary-Confluence's is about 100 m from Deerfoot Trail, and hybrid districts that reach outside the city are coded by where their centroid falls.",
            "The Bow River is identified by position in an unnamed OpenStreetMap extract, and Deerfoot Trail as Highway 2 in the National Road Network file.",
            "Populations are the commission's own tables, as in the published figure. District counts and means move with every recode because whole districts change zone.",
            "This does not address how the committed lists were first chosen (audit finding structural-lane-1).",
        ],
    }
    (HERE / "calgary_zone_recode.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    pd.DataFrame(rows).to_csv(HERE / "calgary_zone_recode_districts.csv", index=False, lineterminator="\n")
    print(json.dumps(out["line_construction"]))
    for m in results:
        for c, s in results[m]["codings"].items():
            print(m, c, s["n_zone_a"], s["mean_zone_a"], s["n_zone_b"], s["mean_zone_b"], s["gap_pct"], s["zone_a_excess_over_provincial_mean_pct"])
        print(" ", results[m]["districts_whose_zone_differs_from_committed"], results[m]["districts_in_strip"])
    for k, v in rule.items():
        print(k, v["minority_gap_pct"], "vs 2x", v["magnitudes"]["twice_majority"], "fires:", v["magnitudes"]["minority_exceeds_twice_majority"],
              "| signed fires:", v["signed_as_written"]["minority_exceeds_twice_majority"])


if __name__ == "__main__":
    main()
