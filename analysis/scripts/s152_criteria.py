# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 CSDs | Government of Alberta
#       Metis Settlement polygons (OGL-Alberta) | OpenStreetMap highways (ODbL)
"""
s152_criteria.py
----------------

Per-VA inputs for the EBCA s.15(2) criteria, so a district's criteria are sums
and counts over its VAs (Amendment 17, set D; governance/GOVERNANCE-s15-2-chain-model.md).

s.15(2): for no more than 4 divisions, if the Commission is of the opinion that
at least 3 of these exist, the division may be as much as 50% below average:
  (a) area > 20,000 km2 (the 15,000 km2 surveyed-area limb has no data: not modelled)
  (b) > 150 km from the Legislature Building to the nearest boundary of the
      division by the most direct highway route -> OSM road-network distance from
      the Legislature to the nearest road vertex inside each VA; a division is
      far when every VA is beyond 150 km
  (c) no town (municipal status town, CSD type T) of more than 8,000 people
      in the division; a town counts if any of its VAs is in the division;
      town population = sum of its VAs' 2021 population
  (d) contains an Indian reserve (2021 CSD types IRI, S-E, plus NRCan CLSS
      "Aboriginal Lands" legislative boundaries for Alberta) or Metis settlement
      (GoA polygons) -> VA overlaps one by >= 1% of the VA's or the reserve's area
  (e) part of the boundary coterminous with the provincial boundary -> VA shares
      >= 100 m with an exterior ring of the union of all VAs (lake holes excluded)

Usage:  python analysis/scripts/s152_criteria.py    (writes data/outputs/s152_va_criteria.csv)
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from shapely.geometry import Point

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))
import mcmc_ensemble as me  # noqa: E402

CSD_GPKG = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"
METIS = REPO / "data/shapefiles/reference/metis_settlements_dl/metis_settlements_goa.geojson"
ABLANDS = REPO / "data/shapefiles/reference/aboriginal_lands_nrcan_dl/aboriginal_lands_alberta.geojson"
ROADS = REPO / "data/osm/alberta_osm_highways.gpkg"
OUT = REPO / "data/outputs/s152_va_criteria.csv"
LEGISLATURE = (-113.506611, 53.533694)  # lon, lat; Wikipedia "Alberta Legislature Building"
CRS = 3400
TOWN_LIMIT = 8_000


def road_km(va):
    """Network distance (km) from the Legislature to the nearest road vertex in each VA."""
    roads = gpd.read_file(ROADS).to_crs(CRS).explode(index_parts=False)
    coords, src, dst, w = {}, [], [], []

    def nid(xy):
        key = (round(xy[0]), round(xy[1]))  # 1 m snap joins lines that share a vertex
        if key not in coords:
            coords[key] = len(coords)
        return coords[key]

    for geom in roads.geometry:
        pts = list(geom.coords)
        for a, b in zip(pts[:-1], pts[1:]):
            i, j = nid(a), nid(b)
            if i != j:
                src.append(i); dst.append(j); w.append(float(np.hypot(b[0] - a[0], b[1] - a[1])))
    n = len(coords)
    m = coo_matrix((w + w, (src + dst, dst + src)), shape=(n, n)).tocsr()
    xy = np.array(list(coords.keys()), float)
    leg = gpd.GeoSeries([Point(LEGISLATURE)], crs=4326).to_crs(CRS).iloc[0]
    start = int(np.argmin(np.hypot(xy[:, 0] - leg.x, xy[:, 1] - leg.y)))
    snap_m = float(np.hypot(xy[start, 0] - leg.x, xy[start, 1] - leg.y))
    dist = dijkstra(m, indices=start) + snap_m
    verts = gpd.GeoDataFrame({"d": dist}, geometry=gpd.points_from_xy(xy[:, 0], xy[:, 1]), crs=CRS)
    verts = verts[np.isfinite(verts["d"])]
    j = gpd.sjoin(verts, va[["geometry"]], how="inner", predicate="within")
    inside = j.groupby("index_right")["d"].min()
    out = pd.Series(np.nan, index=va.index)
    out.loc[inside.index] = inside
    # VAs with no reachable road vertex inside: nearest reachable vertex + straight gap
    miss = out.index[out.isna()]
    if len(miss):
        near = gpd.sjoin_nearest(va.loc[miss, ["geometry"]], verts, how="left", distance_col="gap")
        near = near[~near.index.duplicated(keep="first")]
        out.loc[miss] = near["d"] + near["gap"]
    print(f"road network: {n:,} vertices, {len(w):,} segments; Legislature snapped {snap_m:.0f} m; "
          f"{len(miss)} VAs without an inside road vertex", flush=True)
    return out / 1000.0


def provincial_border(va, min_m=100.0):
    """True where a VA shares >= min_m of boundary with the province's outer edge.
    Uses only the exterior rings of the VA union: gerrychain's boundary_node also
    marks VAs on interior holes (lakes such as Lesser Slave Lake), which are not
    the provincial boundary."""
    from shapely.geometry import MultiLineString
    from shapely.ops import unary_union

    u = unary_union(list(va.geometry.buffer(0)))
    polys = [u] if u.geom_type == "Polygon" else list(u.geoms)
    edge = MultiLineString([list(p.exterior.coords) for p in polys])
    return pd.Series([g.boundary.intersection(edge).length >= min_m for g in va.geometry], index=va.index)


def overlaps(va, polys):
    """True where a VA overlaps any polygon by >= 1% of the VA's or the polygon's area."""
    polys = polys.reset_index(drop=True)
    polys["parea"] = polys.area
    x = gpd.overlay(va[["geometry"]].assign(vid=va.index, varea=va.area), polys[["geometry", "parea"]],
                    how="intersection", keep_geom_type=True)
    x["a"] = x.area
    hit = x[(x["a"] >= 0.01 * x["varea"]) | (x["a"] >= 0.01 * x["parea"])]["vid"].unique()
    return pd.Series(va.index.isin(hit), index=va.index)


def build():
    va, graph = me.build_va_graph(verbose=False)
    va = va.to_crs(CRS)
    nodes = sorted(graph.nodes())
    va = va.loc[nodes]
    df = pd.DataFrame(index=va.index)
    df["area_km2"] = [graph.nodes[n]["va_area"] / 1e6 for n in nodes]
    df["border"] = provincial_border(va)

    csd = gpd.read_file(CSD_GPKG).to_crs(CRS)
    pts = va.copy(); pts["geometry"] = va.geometry.representative_point()
    j = gpd.sjoin(pts[["geometry"]], csd[["CSDUID", "CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(va.index)
    pop = pd.Series([graph.nodes[n]["pop_2021"] for n in nodes], index=va.index)
    town = j["CSDTYPE"].eq("T")
    tpop = pop[town].groupby(j.loc[town, "CSDUID"]).sum()
    big = set(tpop[tpop > TOWN_LIMIT].index)
    df["big_town"] = town & j["CSDUID"].isin(big)
    df["town_name"] = np.where(df["big_town"], j["CSDNAME"], "")

    reserves = csd[csd["CSDTYPE"].isin(["IRI", "S-É"])][["geometry"]]
    clss = gpd.read_file(ABLANDS).to_crs(CRS)[["geometry"]]  # NRCan legislative reserve boundaries
    metis = gpd.read_file(METIS).to_crs(CRS)[["geometry"]]
    df["reserve_or_metis"] = overlaps(va, pd.concat([reserves, clss, metis], ignore_index=True))
    df["road_km"] = road_km(va)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index_label="node")
    big_names = sorted(set(df.loc[df["big_town"], "town_name"]))
    print(f"wrote {OUT} ({len(df)} VAs); towns > {TOWN_LIMIT:,}: {len(big_names)}: {', '.join(big_names)}")
    print(f"border VAs {int(df['border'].sum())}; reserve/Metis VAs {int(df['reserve_or_metis'].sum())}; "
          f"road_km range {df['road_km'].min():.1f}-{df['road_km'].max():.1f}")
    return df


def district_criteria(df, mask):
    """Criteria for the division made of VAs where mask is True."""
    sub = df[mask]
    c = {
        "a_area": bool(sub["area_km2"].sum() > 20_000),
        "b_far": bool(sub["road_km"].min() > 150),
        "c_no_big_town": bool(not sub["big_town"].any()),
        "d_reserve_metis": bool(sub["reserve_or_metis"].any()),
        "e_border": bool(sub["border"].any()),
    }
    c["n_met"] = sum(c.values())
    return c


if __name__ == "__main__":
    build()
