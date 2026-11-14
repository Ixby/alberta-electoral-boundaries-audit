# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
description_check.py
--------------------

Amendment 10, extra check 4b: the report's written boundary descriptions
(findings/a10_dev/boundary_descriptions.md) against the assembled real map. Reporting only; no partisan measure.

For each described changed district with a full ring (ED 71 Lethbridge, the metes-and-bounds ring; ED 40, 46,
48, 49, 62, 79, 85, the prose rings) each description clause that names a side and a feature is a STRETCH:
  side     a compass sector of the district's outer boundary: samples every 100 m whose outward normal (taken over
           +-400 m of boundary) points within 50 degrees of N / E / S / W AND that lie in the outer 30% of the
           district's bounding box on that side (so a notch or a staircase edge inside the district does not count
           as its 'east side'); holes and parts under 1% of the largest part are ignored;
  feature  the geometry the clause names, built only from sources already in the repo:
             csd       2021 census subdivision limits (data/shapefiles/reference/alberta_2021_csds.gpkg),
             route     National Road Network edition 17.0 segments with that RTNUMBER1
                       (data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg, built by build_nrn_extract.py),
             expressway the unnumbered NRN Expressway/Highway segments (Whitemud Drive west of Highway 2 carries no route
                       number in the NRN), only those within 2 km of the district,
             arterial  any NRN road of class Expressway/Highway, Arterial or Collector (used where a clause names a
                       street the sources cannot name, so it tests only 'the boundary runs along a main road'),
             river     OSM waterway lines (data/osm/alberta_osm_rivers.gpkg, UNNAMED: any waterway qualifies),
             province  the outer limit of the union of the census subdivisions (the B.C. and Saskatchewan borders).
  measure  distance from each sample to the feature: median, 90th percentile, share within 200 m, and every run of
           consecutive samples over 200 m that lasts at least 1 km, quoted with the clause that assigned it. Also
           follow_km_all_sides: how much of the WHOLE district boundary (every side) lies within 200 m of the feature,
           against the length of the side the clause assigned it, so a side mis-sorted by the compass sector is visible.
Clauses whose feature the sources cannot hold (street names, creek names, railway, watersheds, a reserve not in the
files, 'south of Lac La Biche') are listed as not checkable, with the reason. A proximity clause ('just east of')
is measured against a 5 km tolerance, not 200 m, and is labelled so.

Usage: python findings/a10_dev/description_check.py --snap C:/tmp/a10test/snap_fixed --tag fixed
Writes findings/a10_dev/description_check_<tag>.json. EPSG:3400. Deterministic.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import shapely
from pyproj import Transformer
from shapely.geometry import LineString
from shapely.strtree import STRtree

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
CSD = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"
NRN = REPO / "data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg"
RIV = REPO / "data/osm/alberta_osm_rivers.gpkg"
STEP = 100.0       # boundary sampling step (m)
SMOOTH = 400.0     # normal taken from the boundary points this far either side (m)
OUTER = 0.30       # a sample belongs to a side only if it lies in the outer share of the bounding box on that side
SECTOR = 50.0      # a sample belongs to a side when its outward bearing is within this of the compass point (degrees)
TOL = 200.0        # a stretch is off when further than this from its feature (m)
RUN_MIN = 1000.0   # runs over TOL shorter than this are not listed (m)
PROX_TOL = 5000.0  # tolerance for proximity clauses (m)
BEARING = {"N": 0.0, "E": 90.0, "S": 180.0, "W": 270.0}
ARTERIAL = {"Expressway / Highway", "Arterial", "Collector"}
TO_LL = Transformer.from_crs(3400, 4326, always_xy=True)

# clause table. id = passage id in boundary_descriptions.md; text = the clause as the report words it (quoted from that file).
# feature = (kind, args); 'any' of several kinds are unioned. tol None -> TOL.
D = {
    71: {"name": "Lethbridge", "completeness": "FULL RING (metes-and-bounds M1 + prose summary B01)", "stretches": [
        {"id": "B01", "side": "N", "text": "on the north by Highway 3", "feature": [("route", ["3"])]},
        {"id": "B01/M1", "side": "S", "text": "bounded on the south by the Oldman River in West Lethbridge and the city limits east of the river",
         "feature": [("river", None), ("csd", ["Lethbridge"])]},
        {"id": "B01", "side": "E", "text": "On the eastern side the electoral boundary heads down Mayor Magrath to South Parkside Drive and then east to Highway 4 ... and then south along the Lethbridge's eastern city limits",
         "feature": [("route", ["5", "4"]), ("csd", ["Lethbridge"])]},
        {"id": "B01", "side": "W", "text": "It's bounded on the west by Metis Trail West", "feature": [("arterial", None)],
         "note": "street name not in the sources: tests only that the boundary runs along a main road"}],
     "not_checkable": [
         ("M1", "Westside Drive, Garry Drive, Metis Trail W., Whoop Up Drive, McMaster Blvd, Mount Burke Blvd, Rocky Mountain Blvd, Sunridge Blvd, South Parkside Drive, Mayor Magrath Drive as separate waypoints", "the NRN extract keeps ROADCLASS and RTNUMBER1 only, no street names; Mayor Magrath Drive (Highway 5) and Highways 3 and 4 are the only waypoints a route number resolves"),
         ("B01", "southeast along the railway tracks / back up north to take in the Research and Development Centre", "no railway or facility layer in the repo")]},
    40: {"name": "Edmonton-Meadows", "completeness": "full prose ring", "stretches": [
        {"id": "B14", "side": "N", "text": "Its northern boundary is still Whitemud Drive or Highway 14 ... and 38th Avenue N.W.", "feature": [("route", ["14"]), ("expressway", None)]},
        {"id": "B14", "side": "S", "text": "Its southern boundary is still Anthony Henday Drive and 16A Avenue N.W.", "feature": [("route", ["216"])]},
        {"id": "B14", "side": "E", "text": "(eastern edge) bordering Edmonton's eastern city limits", "feature": [("csd", ["Edmonton"])]},
        {"id": "B14", "side": "W", "text": "Its western boundary is still 34th [Street N.W.]", "feature": [("arterial", None)],
         "note": "street name not in the sources: tests only that the boundary runs along a main road"}],
     "not_checkable": [("B14", "38th Avenue N.W., 16A Avenue N.W., 34th Street N.W. by name", "no street names in the NRN extract")]},
    46: {"name": "Edmonton-Strathcona", "completeness": "full prose ring (east edge cut off in the text layer)", "stretches": [
        {"id": "B16", "side": "S", "text": "bounded on the south by Whitemud Drive", "feature": [("route", ["14"]), ("expressway", None)]},
        {"id": "B16", "side": "N", "text": "on the north by the North Saskatchewan River", "feature": [("river", None)]},
        {"id": "B16", "side": "W", "text": "on the west, by Whitemud Creek", "feature": [("river", None)],
         "note": "waterways are unnamed in the OSM layer: tests only that the boundary runs along a mapped waterway"},
        {"id": "B16", "side": "E", "text": "and on the east by Gateway Boulevard, 99th Street", "feature": [("route", ["2"])],
         "note": "the passage is cut off after '99th Street'; Gateway Boulevard is Highway 2"}],
     "not_checkable": [("B16", "the east edge after '99th Street'", "text cut off in the text layer")]},
    48: {"name": "Edmonton-Whitemud", "completeness": "full prose ring", "stretches": [
        {"id": "C19", "side": "S", "text": "all areas south of Anthony Henday Drive are recommended to be removed [south edge = the Henday]", "feature": [("route", ["216"])]},
        {"id": "C19", "side": "N", "text": "[Whitemud Creek] north to the River [North Saskatchewan]", "feature": [("river", None)]},
        {"id": "C19", "side": "W", "text": "[north and west edges: the North Saskatchewan River]", "feature": [("river", None)]},
        {"id": "C19", "side": "E", "text": "the advisory panel recommends it follow Whitemud Creek north to the River", "feature": [("river", None)],
         "note": "waterways are unnamed in the OSM layer: tests only that the boundary runs along a mapped waterway"}],
     "not_checkable": [("C19", "Rabbit Hill Road limit and Whitemud Drive", "no street names in the NRN extract")]},
    49: {"name": "Edmonton-Windermere", "completeness": "full prose ring", "stretches": [
        {"id": "B15", "side": "E", "text": "It is bounded on the east by Whitemud Creek", "feature": [("river", None)],
         "note": "waterways are unnamed in the OSM layer: tests only that the boundary runs along a mapped waterway"},
        {"id": "B15", "side": "S", "text": "between the City's southern boundary (Highway 19 to Devon) and Anthony Henday Drive", "feature": [("csd", ["Edmonton"]), ("route", ["19"])]},
        {"id": "B15", "side": "N", "text": "[north edge] Anthony Henday Drive at its northern end", "feature": [("route", ["216"])]},
        {"id": "C17", "side": "W", "text": "moving the western boundary of the electoral division east to the North Saskatchewan River", "feature": [("river", None)]}],
     "not_checkable": [("C18", "Chappelle Link S.W. between 28th and 41st Avenue S.W.; the Chappelle Gardens addition", "no street or neighbourhood names in the sources")]},
    62: {"name": "Fort McMurray-Lac La Biche", "completeness": "full prose ring (rough: 'Roughly speaking')", "stretches": [
        {"id": "B06", "side": "W", "text": "Fort McMurray-Lac La Biche's western boundary is the Athabasca River", "feature": [("river", None)],
         "note": "waterways are unnamed in the OSM layer: tests only that the boundary runs along a mapped waterway"},
        {"id": "B06", "side": "N", "text": "Its northern boundary is the Athabasca and Clearwater Rivers", "feature": [("river", None)],
         "note": "waterways are unnamed in the OSM layer: tests only that the boundary runs along a mapped waterway"},
        {"id": "B06", "side": "E", "text": "Its eastern boundary is the Saskatchewan border and the Cold Lake Air Weapons Range", "feature": [("province", None)]}],
     "not_checkable": [("B06", "the Cold Lake Air Weapons Range part of the east edge", "no range boundary in the repo (the Saskatchewan border part is checked)"),
                       ("B06", "its southern boundary is south of Lac La Biche / Smoky Lake County out", "too vague: no line named")]},
    79: {"name": "Morinville-Sturgeon", "completeness": "full prose ring (north edge cut off in the text layer)", "stretches": [
        {"id": "B04", "side": "S", "text": "Its southern boundary is the City of Edmonton and the southern border of Sturgeon County", "feature": [("csd", ["Edmonton", "Sturgeon County"])]},
        {"id": "B04", "side": "E", "text": "Its eastern boundary is the North Saskatchewan River", "feature": [("river", None)]},
        {"id": "B04", "side": "W", "text": "Its western boundary is the western boundary of Sturgeon County", "feature": [("csd", ["Sturgeon County"])]},
        {"id": "B04", "side": "N", "text": "the electoral division's northern boundary is roughly the northern boundary of Sturgeon County", "feature": [("csd", ["Sturgeon County"])]}],
     "not_checkable": [("B03", "push the boundary ... west to parallel Highway 779; Alexander reserve left out; Pine Sands in", "'parallel' gives no line; the reserve and Pine Sands are not in the files"),
                       ("C06", "the St. Albert border moved to the Sturgeon River within St. Albert", "no river names or St. Albert wards in the sources")]},
    85: {"name": "Rocky Mountain House-Sundre", "completeness": "full prose ring", "stretches": [
        {"id": "B17", "side": "W", "text": "Its western boundary follows the B.C. Border north to the Brazeau River", "feature": [("province", None)]},
        {"id": "B17", "side": "N", "text": "the northern boundary of Clearwater County which is recommended to form the northern boundary of the electoral division as well", "feature": [("csd", ["Clearwater County"])]},
        {"id": "B17", "side": "E", "text": "Its eastern boundary is roughly a north-south line just east of the Highway 22 corridor", "feature": [("route", ["22"])],
         "tol": PROX_TOL, "rule": "proximity (5 km): the clause says 'roughly ... just east of', not 'along'"}],
     "not_checkable": [("B17", "its southern boundary meanders west along a watershed northwest of Cochrane", "no watershed layer in the repo"),
                       ("B17", "then northeast along the Brazeau River to the northern boundary of Clearwater County", "waterways are unnamed in the OSM layer and the clause covers a short stretch inside the north-west corner")]},
}


def chunks(lines, step=24):
    out = []
    for ln in lines:
        c = shapely.get_coordinates(ln)
        for i in range(0, max(len(c) - 1, 0), step):
            out.append(LineString(c[i:i + step + 1]))
    return np.array(out, dtype=object)


def parts(g):
    return [p for p in shapely.get_parts(g) if p.geom_type in ("LineString", "LinearRing") and not p.is_empty]


def dist_to(lines, pts):
    """Distance from each point to the nearest of the lines, and the nearest point (nan when there are none)."""
    ch = chunks(lines)
    out, xy = np.full(len(pts), np.nan), np.full((len(pts), 2), np.nan)
    if not len(ch):
        return out, xy
    t = STRtree(ch)
    ii, dd = t.query_nearest(pts, max_distance=2e5, return_distance=True, all_matches=False)
    out[ii[0]] = dd
    xy[ii[0]] = shapely.get_coordinates(shapely.get_point(shapely.shortest_line(pts[ii[0]], ch[ii[1]]), -1))
    return out, xy


def ring_samples(geom):
    """Samples every STEP m along the exterior rings of the real parts: (points, outward bearing deg, ring id, step along ring)."""
    polys = [p for p in shapely.get_parts(geom) if p.geom_type == "Polygon"]
    big = max(p.area for p in polys)
    P, B, R, S = [], [], [], []
    for k, p in enumerate(p for p in polys if p.area >= 0.01 * big):
        ring = p.exterior if shapely.is_ccw(p.exterior) else LineString(list(p.exterior.coords)[::-1])
        L = ring.length
        n = max(8, int(round(L / STEP)))
        s = np.arange(n) * L / n
        at = lambda d: shapely.get_coordinates(shapely.line_interpolate_point(ring, np.mod(d, L)))  # noqa: E731
        d = at(s + SMOOTH) - at(s - SMOOTH)
        nx, ny = d[:, 1], -d[:, 0]            # right of travel = outward for a counter-clockwise ring
        P.append(shapely.line_interpolate_point(ring, s)), B.append(np.degrees(np.arctan2(nx, ny)) % 360)
        R.append(np.full(n, k)), S.append(np.full(n, L / n))
    return np.concatenate(P), np.concatenate(B), np.concatenate(R), np.concatenate(S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snap", default="C:/tmp/a10test/snap_fixed")
    ap.add_argument("--tag", default="fixed")
    ap.add_argument("--out", default=str(OUT_DIR))
    a = ap.parse_args()
    t0 = time.time()
    log = lambda m: print(f"[{time.time() - t0:.0f}s] {m}", flush=True)  # noqa: E731
    dist = gpd.read_file(Path(a.snap) / "districts.gpkg").to_crs(3400).set_index("ed")
    csd = gpd.read_file(CSD).to_crs(3400)
    csd_line = {n: parts(shapely.boundary(shapely.union_all(list(csd[csd.CSDNAME == n].geometry)))) for n in
                ["Edmonton", "Lethbridge", "Sturgeon County", "Clearwater County"]}
    province = parts(shapely.boundary(shapely.union_all(list(csd.geometry))))
    riv = gpd.read_file(RIV).to_crs(3400)
    riv_geoms = np.asarray(riv.geometry.values, dtype=object)
    riv_tree = STRtree(riv_geoms)
    log("layers loaded")
    res = {}
    for ed, spec in D.items():
        g = dist.geometry.loc[ed]
        b = g.bounds
        bb = (b[0] - 15000, b[1] - 15000, b[2] + 15000, b[3] + 15000)
        nrn = gpd.read_file(NRN, bbox=bb)
        nrn["RTNUMBER1"] = nrn.RTNUMBER1.astype(str)
        rv = [p for x in riv_geoms[riv_tree.query(shapely.box(*bb))] for p in parts(x)]

        def feat(kind, arg):
            if kind == "csd":
                return [p for n in arg for p in csd_line[n]]
            if kind == "route":
                return [p for x in nrn[nrn.RTNUMBER1.isin(arg)].geometry for p in parts(x)]
            if kind == "expressway":
                ex = nrn[(nrn.ROADCLASS == "Expressway / Highway") & (nrn.RTNUMBER1 == "None")]
                return [p for x in ex.geometry if shapely.distance(x, g) <= 2000 for p in parts(x)]
            if kind == "arterial":
                return [p for x in nrn[nrn.ROADCLASS.isin(ARTERIAL)].geometry for p in parts(x)]
            if kind == "river":
                return rv
            if kind == "province":
                return province
            raise ValueError(kind)

        P, B, R, S = ring_samples(g)
        out_st, pooled = [], []
        for st in spec["stretches"]:
            sel = np.abs((B - BEARING[st["side"]] + 180) % 360 - 180) <= SECTOR
            px, py = shapely.get_x(P), shapely.get_y(P)
            sel &= {"E": px >= b[2] - OUTER * (b[2] - b[0]), "W": px <= b[0] + OUTER * (b[2] - b[0]),
                    "N": py >= b[3] - OUTER * (b[3] - b[1]), "S": py <= b[1] + OUTER * (b[3] - b[1])}[st["side"]]
            lines = [p for kind, arg in st["feature"] for p in feat(kind, arg)]
            d, q = dist_to(lines, P[sel]) if sel.any() else (np.array([]), np.zeros((0, 2)))
            tol = st.get("tol", TOL)
            d_all, _ = dist_to(lines, P)
            rec = {"clause": st["id"], "text": st["text"], "side": st["side"], "rule": st.get("rule", f"within {int(TOL)} m"),
                   "feature": [f"{k}:{'/'.join(a_) if a_ else '-'}" for k, a_ in st["feature"]], "feature_lines": len(lines)}
            if st.get("note"):
                rec["note"] = st["note"]
            if not len(d) or not np.isfinite(d).any():
                rec.update({"checked": False, "reason": "no samples on that side" if not len(d) else "no feature geometry within reach"})
                out_st.append(rec)
                continue
            ok = np.isfinite(d)
            if st.get("tol") is None:
                pooled.append(d[ok])
            idx = np.flatnonzero(sel)
            seg = S[sel]
            rec.update({"checked": True, "n_samples": int(ok.sum()), "length_km": round(float(seg[ok].sum() / 1000), 1),
                        "median_m": round(float(np.median(d[ok])), 1), "p90_m": round(float(np.percentile(d[ok], 90)), 1),
                        "share_within_tol": round(float((d[ok] <= tol).mean()), 4), "tol_m": tol,
                        "follow_km_all_sides": round(float(S[np.isfinite(d_all) & (d_all <= tol)].sum() / 1000), 1),
                        "side_length_km": round(float(seg[ok].sum() / 1000), 1)})
            if st.get("tol") == PROX_TOL:   # proximity clause: also the signed east-west offset (positive = boundary east of the route)
                dx = shapely.get_x(P[sel])[ok] - q[ok, 0]
                rec["median_east_offset_m"] = round(float(np.median(dx)), 0)
                rec["share_east_of_route"] = round(float((dx > 0).mean()), 4)
            # runs of consecutive over-tolerance samples on one ring, at least RUN_MIN long
            runs = []
            bad = (d > tol) & ok
            if bad.any():
                k = 0
                n_ = len(d)
                while k < n_:
                    if bad[k]:
                        j = k
                        while j + 1 < n_ and bad[j + 1] and idx[j + 1] == idx[j] + 1 and R[idx[j + 1]] == R[idx[j]]:
                            j += 1
                        ln = float(seg[k:j + 1].sum())
                        if ln >= RUN_MIN:
                            mid = P[idx[(k + j) // 2]]
                            lon, lat = TO_LL.transform(mid.x, mid.y)
                            runs.append({"length_km": round(ln / 1000, 1), "max_distance_m": round(float(d[k:j + 1].max()), 0),
                                         "median_distance_m": round(float(np.median(d[k:j + 1])), 0),
                                         "at_x_y_epsg3400": [round(mid.x), round(mid.y)], "at_lon_lat": [round(lon, 4), round(lat, 4)]})
                        k = j + 1
                    else:
                        k += 1
            runs.sort(key=lambda r: -r["length_km"])
            rec["runs_over_tol_ge_1km"] = runs[:8]
            rec["n_runs_over_tol_ge_1km"] = len(runs)
            rec["length_in_runs_km"] = round(sum(r["length_km"] for r in runs), 1)
            out_st.append(rec)
        chk = [s for s in out_st if s.get("checked")]
        res[str(ed)] = {"ed": ed, "name": spec["name"], "source": dist.source.loc[ed], "area_km2": round(g.area / 1e6, 1),
                        "description": spec["completeness"], "stretches_checked": len(chk), "stretches": out_st,
                        "not_checkable": [{"clause": c, "what": w, "reason": r} for c, w, r in spec["not_checkable"]],
                        "median_distance_all_checked_samples_m": round(float(np.median(np.concatenate(pooled))), 1) if pooled else None,
                        "median_of_stretch_medians_m": round(float(np.median([s["median_m"] for s in chk])), 1) if chk else None,
                        "stretches_with_run_over_tol": [{"side": s["side"], "clause": s["clause"], "text": s["text"], "runs": s["runs_over_tol_ge_1km"]}
                                                        for s in chk if s["runs_over_tol_ge_1km"]]}
        log(f"ED {ed} {spec['name']}: {len(chk)} stretches checked, median of medians {res[str(ed)]['median_of_stretch_medians_m']} m, "
            f"{len(res[str(ed)]['stretches_with_run_over_tol'])} with runs over tolerance")
    allchk = [s for r in res.values() for s in r["stretches"] if s.get("checked")]
    summary = {"districts": len(res), "stretches_checked": len(allchk),
               "stretches_not_checkable": sum(len(r["not_checkable"]) for r in res.values()),
               "median_of_stretch_medians_m": round(float(np.median([s["median_m"] for s in allchk])), 1),
               "stretches_with_share_within_tol_ge_90pct": sum(1 for s in allchk if s["share_within_tol"] >= 0.9),
               "stretches_with_run_over_tol": sum(1 for s in allchk if s["runs_over_tol_ge_1km"])}
    out = {"snap": a.snap, "constants": {"STEP_m": STEP, "SMOOTH_m": SMOOTH, "SECTOR_deg": SECTOR, "OUTER_share": OUTER, "TOL_m": TOL, "RUN_MIN_m": RUN_MIN, "PROX_TOL_m": PROX_TOL},
           "limits": ["no street, creek, railway or watershed names exist in the repo's data; clauses that need them are listed under not_checkable "
                      "or tested only for 'runs along a main road' / 'runs along a mapped waterway'",
                      "OSM waterways are unnamed and dense in rural areas, so a river clause passes easily in the north and west",
                      "municipal limits are the 2021 census subdivisions, not the 2025-26 limits"],
           "summary": summary, "districts": res, "seconds": round(time.time() - t0, 1)}
    (Path(a.out) / f"description_check_{a.tag}.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    log("wrote description_check_%s.json" % a.tag)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
