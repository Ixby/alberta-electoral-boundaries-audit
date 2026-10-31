# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
s15_2_criteria.py
-----------------

EBCA s.15(2) criteria (a)-(e) for any district plan built from VAs, per
Amendment 21. The same per-VA table drives the s.15(2) neutral-map set and
the scoring of real maps.

  (a) area       sum of the district's VA areas (equal-area projection)
                 > 20,000 km2. The 15,000 km2 surveyed-area limb has no
                 province-wide source here and is treated as not met.
  (b) distance   shortest route on the OSM highway layer (motorway, trunk,
                 primary, secondary) from the node nearest the Legislature
                 Building to the nearest point where a highway reaches the
                 district's boundary (or a highway node inside it) > 150 km.
                 A district no highway reaches meets (b). Amendment 23.
  (c) town       no "town" over 8,000 people (2021 census) holds >= 2% of its
                 population in the district. Towns: CSD types CY and T, and
                 each specialized municipality's urban service area (its DAs
                 at >= 400 people per km2), except Crowsnest Pass (s.15(3)).
                 --town-reading status: towns are CSD type T only, the legal
                 town status; cities and urban service areas do not count.
                 Diagnostic only (Amendment 25, withdrawn); not a registered
                 reading.
  (d) reserve    the district holds >= 10% of the area of an Indian reserve
                 (NRCan Aboriginal Lands, legal boundaries) or a Metis
                 settlement (Government of Alberta layer).
  (e) border     the district's VAs share >= 1 km of edge with the
                 provincial boundary (VA edge within 100 m of the outline).

Usage
  python analysis/scripts/s15_2_criteria.py --va-table OUT.csv [--town-reading status]
  python analysis/scripts/s15_2_criteria.py --score [--out results.json] [--town-reading status]
"""
import argparse
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from shapely.geometry import Point
from shapely.ops import unary_union

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))
import mcmc_ensemble as me  # noqa: E402

CSD = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"
CSD_POP = REPO / "data/reference/alberta_2021_csd_populations.csv"
DA = REPO / "data/shapefiles/reference/alberta_2021_das.gpkg"
DA_POP = REPO / "data/reference/alberta_2021_da_populations.csv"
OSM = REPO / "data/osm/alberta_osm_highways.gpkg"
RESERVES = REPO / "data/shapefiles/reference/aboriginal_lands_nrcan_dl/aboriginal_lands_alberta.geojson"
METIS = REPO / "data/shapefiles/reference/metis_settlements_dl/metis_settlements_goa.geojson"
MAPS = {"majority_2026": REPO / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
        "minority_2026": REPO / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg"}
LEGISLATURE = (-113.5068, 53.5336)  # lon, lat; Alberta Legislature Building
WORK = "EPSG:3400"  # Alberta 10-TM (metres): distances and lengths
EQAREA = "ESRI:102001"  # Canada Albers equal-area: areas
AREA_KM2, DIST_KM, TOWN_POP = 20_000, 150, 8_000
TOWN_SHARE, RESERVE_SHARE, BORDER_KM = 0.02, 0.10, 1.0


def road_km(vas):
    """Per VA: highway distance (km) from the Legislature to the nearest point where a highway
    crosses into the VA, or to a highway node inside it. A district's distance is the minimum over
    its VAs: the first point a shortest route reaches inside the district lies on its boundary."""
    h = gpd.read_file(OSM).to_crs(WORK)
    keys, edges = {}, []
    for geom in h.geometry:
        for line in getattr(geom, "geoms", [geom]):
            xy = np.round(np.asarray(line.coords)[:, :2], 2)
            ids = [keys.setdefault((x, y), len(keys)) for x, y in xy]
            seg = np.hypot(*np.diff(xy, axis=0).T)
            edges += list(zip(ids[:-1], ids[1:], seg))
    n = len(keys)
    a, b, w = map(np.asarray, zip(*edges))
    a, b = a.astype(int), b.astype(int)
    g = coo_matrix((w, (a, b)), shape=(n, n)).tocsr()
    xy = np.array(list(keys))
    src = gpd.GeoSeries([Point(LEGISLATURE)], crs=4326).to_crs(WORK).iloc[0]
    start = int(np.argmin(np.hypot(xy[:, 0] - src.x, xy[:, 1] - src.y)))
    d = dijkstra(g, directed=False, indices=start)
    geo = vas.geometry.values
    best = np.full(len(vas), np.inf)
    pi, vi = shapely.STRtree(geo).query(shapely.points(xy), predicate="within")
    np.minimum.at(best, vi, d[pi])
    segs = shapely.linestrings(np.stack([xy[a], xy[b]], axis=1))
    bnd = shapely.boundary(geo)
    si, bi = shapely.STRtree(bnd).query(segs, predicate="intersects")
    for e, v, cut in zip(si, bi, shapely.intersection(segs[si], bnd[bi])):
        u, t = a[e], b[e]
        for p in shapely.get_parts(cut):
            if shapely.get_type_id(p) != 0:  # points only; a segment lying along a boundary has its ends checked
                continue
            px, py = shapely.get_x(p), shapely.get_y(p)
            dp = min(d[u] + np.hypot(px - xy[u, 0], py - xy[u, 1]), d[t] + np.hypot(px - xy[t, 0], py - xy[t, 1]))
            best[v] = min(best[v], dp)
    return pd.Series(best / 1000.0, index=vas.index)

def towns(vas, pts, reading="purposive"):
    """Per VA: the town it belongs to (by representative point), and each town's 2021 population.
    reading "purposive" (Amendment 21): cities, towns and urban service areas; "status"
    (diagnostic only; Amendment 25 withdrawn): towns by legal status (CSD type T) only."""
    csd = gpd.read_file(CSD).to_crs(WORK)
    pop = pd.read_csv(CSD_POP).set_index("DGUID")["population_2021"]
    csd["pop"] = csd["DGUID"].map(pop)
    types = ["CY", "T"] if reading == "purposive" else ["T"]
    t = csd[csd["CSDTYPE"].isin(types)][["CSDNAME", "pop", "geometry"]].rename(columns={"CSDNAME": "town"})
    if reading == "status":
        t = t[t["pop"] > TOWN_POP]
        j = gpd.sjoin(pts[["geometry"]], t[["town", "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
        return j["town"].fillna(""), t.set_index("town")["pop"].to_dict()
    da = gpd.read_file(DA).to_crs(WORK)
    da["pop"] = da["DGUID"].map(pd.read_csv(DA_POP).set_index("DGUID")["population_2021"]).fillna(0)
    da["dens"] = da["pop"] / da["LANDAREA"].where(da["LANDAREA"] > 0)
    da_pts = da.assign(geometry=da.geometry.representative_point())  # DAs nest in CSDs
    usa = []
    for _, sm in csd[(csd["CSDTYPE"] == "SM") & (csd["CSDNAME"] != "Crowsnest Pass")].iterrows():  # s.15(3)
        dense = da[da_pts.within(sm.geometry) & (da["dens"] >= 400)]
        if len(dense):
            usa.append({"town": f"{sm['CSDNAME']} (urban service area)", "pop": float(dense["pop"].sum()),
                        "geometry": unary_union(dense.geometry)})
    if usa:
        t = pd.concat([t, gpd.GeoDataFrame(usa, crs=WORK)], ignore_index=True)
    t = t[t["pop"] > TOWN_POP]
    j = gpd.sjoin(pts[["geometry"]], t[["town", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    return j["town"].fillna(""), t.set_index("town")["pop"].to_dict()


def reserves(vas):
    """Per VA: {reserve or settlement: overlap area km2}, and each one's total area."""
    r = gpd.read_file(RESERVES).to_crs(WORK)
    r = r[r["distributionType"] == "IR"][["adminAreaNameEng", "geometry"]].rename(columns={"adminAreaNameEng": "name"})
    m = gpd.read_file(METIS).to_crs(WORK)[["METIS_NAME", "geometry"]].rename(columns={"METIS_NAME": "name"})
    m["name"] = m["name"] + " (Metis settlement)"
    r = pd.concat([r, m], ignore_index=True).dissolve(by="name").reset_index()
    total = (r.set_index("name").geometry.area / 1e6).to_dict()
    ov = gpd.overlay(vas[["geometry"]].reset_index(names="va"), r, how="intersection", keep_geom_type=True)
    ov["km2"] = ov.geometry.area / 1e6
    per = ov[ov["km2"] > 0].groupby("va").apply(lambda d: dict(zip(d["name"], d["km2"])), include_groups=False)
    return per.reindex(vas.index), total


def border_km(vas):
    """Per VA: km of its edge within 100 m of the provincial outline (exterior of the CSD union)."""
    csd = gpd.read_file(CSD).to_crs(WORK)
    outline = unary_union(csd.geometry.buffer(50)).buffer(-50)
    ext = max(getattr(outline, "geoms", [outline]), key=lambda p: p.area).exterior.buffer(100)
    return vas.geometry.boundary.intersection(ext).length / 1000.0


def va_table(reading="purposive"):
    va, graph = me.build_va_graph(verbose=False)
    nodes = sorted(graph.nodes())
    vas = va.loc[nodes, ["geometry", "pop_2021"]].to_crs(WORK)
    pts = vas.copy()
    pts["geometry"] = vas.geometry.representative_point()
    tab = pd.DataFrame(index=vas.index)
    tab["pop"] = vas["pop_2021"]
    tab["area_km2"] = vas.to_crs(EQAREA).geometry.area / 1e6
    tab["road_km"] = road_km(vas)
    tab["town"], town_pop = towns(vas, pts, reading)
    tab["reserves"], res_area = reserves(vas)
    tab["border_km"] = border_km(vas)
    return tab, town_pop, res_area, va


def criteria(tab, labels, town_pop, res_area):
    """Per district: (a)-(e) met or not, the count, and the evidence."""
    df = tab.assign(d=np.asarray(labels))
    tpop = df[df["town"] != ""].groupby("town")["pop"].sum()
    out = {}
    for d, g in df.groupby("d"):
        held = g[g["town"] != ""].groupby("town")["pop"].sum()
        big = sorted(t for t, p in held.items() if p >= TOWN_SHARE * tpop[t])
        res = {}
        for r in g["reserves"].dropna():
            for k, v in r.items():
                res[k] = res.get(k, 0.0) + v
        held_res = sorted(k for k, v in res.items() if v >= RESERVE_SHARE * res_area[k])
        c = {"a": bool(g["area_km2"].sum() > AREA_KM2),
             "b": bool(g["road_km"].min() > DIST_KM),
             "c": not big,
             "d": bool(held_res),
             "e": bool(g["border_km"].sum() >= BORDER_KM)}
        out[d] = {**c, "n": sum(c.values()), "pop": float(g["pop"].sum()),
                  "area_km2": round(float(g["area_km2"].sum())), "road_km": round(float(g["road_km"].min()), 1),
                  "towns_over_8000": big, "reserves_held": held_res,
                  "border_km": round(float(g["border_km"].sum()), 1)}
    return out


def assign(pts, gpkg, col="EDName2025"):
    g = gpd.read_file(gpkg).to_crs(pts.crs)
    j = gpd.sjoin(pts[["geometry"]], g[[col, "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    return j[col].fillna("__unassigned__")


def score(tab, town_pop, res_area, va):
    pts = va.loc[tab.index, ["geometry"]].to_crs(WORK)
    pts["geometry"] = pts.geometry.representative_point()
    res = {"2019_enacted": criteria(tab, va.loc[tab.index, "parent_ed_2019"].to_numpy(), town_pop, res_area)}
    for name, f in MAPS.items():
        res[name] = criteria(tab, assign(pts, f).to_numpy(), town_pop, res_area)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--va-table", help="write the per-VA table here")
    ap.add_argument("--score", action="store_true", help="score the 2019, majority and minority maps")
    ap.add_argument("--out")
    ap.add_argument("--town-reading", choices=["purposive", "status"], default="purposive",
                    help="s.15(2)(c): purposive = cities count as towns (Amendment 21); status = legal towns only (diagnostic; Amendment 25 withdrawn)")
    a = ap.parse_args()
    tab, town_pop, res_area, va = va_table(a.town_reading)
    print(f"{len(town_pop)} towns over 8,000: " + ", ".join(f"{t} {p:,.0f}" for t, p in sorted(town_pop.items(), key=lambda x: -x[1])))
    print(f"{len(res_area)} reserves/settlements; VAs no highway reaches: {int(np.isinf(tab['road_km']).sum())}")
    if a.va_table:
        t = tab.copy()
        t["reserves"] = t["reserves"].apply(lambda r: json.dumps(r) if isinstance(r, dict) else "")
        t.to_csv(a.va_table, index_label="node")
    if a.score:
        res = score(tab, town_pop, res_area, va)
        if a.out:
            Path(a.out).write_text(json.dumps(res, indent=1, default=float))
        for m, ds in res.items():
            avg = sum(v["pop"] for v in ds.values()) / len(ds)
            print(f"\n{m}: districts meeting >= 3 criteria, with population vs average")
            for d, v in sorted(ds.items(), key=lambda x: x[1]["pop"]):
                if v["n"] >= 3 or v["pop"] < 0.75 * avg:
                    flags = "".join(k for k in "abcde" if v[k])
                    print(f"  {d:42s} {v['n']}/5 [{flags:5s}] {100 * (v['pop'] / avg - 1):+6.1f}%  "
                          f"area {v['area_km2']:,} road {v['road_km']} border {v['border_km']}  "
                          f"towns {v['towns_over_8000']}  reserves {len(v['reserves_held'])}")
