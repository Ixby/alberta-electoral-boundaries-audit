# Alberta Electoral Boundary Audit — Recommendation 5 zones for the map explorer
# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain); Statistics Canada 2021 CSDs; OSM | https://ixby.github.io
#
# Builds viewer/static/mapdata/lunty_bounds.json: the four areas that the
# commission chair's Recommendation 5 (Justice Dallas Miller, Addendum to the
# Majority Report, final report pp. 66-67) names. The November 2026 committee
# map is scored against these (academic report §7.2, test X1). R5 is quoted in
# full in findings/chair_recommendation_5_analysis.md. Its base map is the
# MAJORITY map: "The rest of the province as we propose must be maintained to
# the extent possible." Every district set below is read off that map.
#
#   a  "have no impact on any electoral division in Airdrie or containing
#      territory south of Airdrie's southernmost border, with the exception of
#      Drumheller-Stettler"
#      -> majority EDs whose name contains "Airdrie", or whose southernmost
#         point lies south of the City of Airdrie's southernmost point
#         (2021 CSD, compared in latitude), minus Drumheller-Stettler.
#   b  "have no impact on any electoral division north of the North
#      Saskatchewan River in Edmonton"
#   c  "result in all electoral divisions south of the North Saskatchewan
#      River in Edmonton reverting to the map outlined in the interim report"
#      -> "Edmonton-" EDs, split by which bank holds most of their area. The
#         river is the longest OSM river line through the City of Edmonton.
#         The interim (October 2025) map itself is not in this repository, so
#         zone c marks WHERE the reversion applies, not what it reverts to.
#   d  "consider restoring an electoral division mostly consisting of
#      Clearwater County and western Mountain View County as an electoral
#      division with s. 15(2) status"
#      -> Clearwater County plus the part of Mountain View County that sat in
#         the 2019 Rimbey-Rocky Mountain House-Sundre division (which held
#         99.9% of Clearwater County and the western 31.7% of Mountain View
#         County), clipped off any district in a or b. APPROXIMATE: R5
#         names an area, not a boundary. It lies wholly north of Airdrie.
#
# R5 restores TWO divisions but names a place for only one (d). The second has
# no zone because R5 gives it none.
#
# Output coordinates: EPSG:3401, origin-shifted to the explorer's space
# (docs/data/map_meta.json), matching every other mapdata/*.json layer.
import json
from pathlib import Path

import geopandas as gpd
from shapely.geometry import LineString, Point, box
from shapely.ops import linemerge, split, unary_union

REPO = Path(__file__).resolve().parents[2]
meta = json.loads((REPO / "docs" / "data" / "map_meta.json").read_text())
ox, oy = meta["origin_x"], meta["origin_y"]
SIMPLIFY_M = 150  # same tolerance as the previous single-zone build

maj = gpd.read_file(REPO / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg")
csd = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg")
e19 = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp")
NAME = "EDName2025"


def csd_geom(name, crs):
    return csd[csd["CSDNAME"] == name].to_crs(crs).geometry.iloc[0]


# ── (a) Airdrie and everything south of it, except Drumheller-Stettler ──────
maj_ll = maj.to_crs(4326)
airdrie_south = csd_geom("Airdrie", 4326).bounds[1]
in_a = maj_ll[NAME].str.contains("Airdrie") | (maj_ll.geometry.bounds["miny"] < airdrie_south)
eds_a = sorted(n for n in maj_ll.loc[in_a, NAME] if n != "Drumheller-Stettler")
assert "Drumheller-Stettler" in set(maj_ll.loc[in_a, NAME]), "R5(a)'s named exception should fall in the zone"

# ── (b)/(c) Edmonton, split at the North Saskatchewan ──────────────────────
m3400 = maj.to_crs(3400)
edm = csd_geom("Edmonton", 3400)
riv = gpd.read_file(REPO / "data/osm/alberta_osm_rivers.gpkg", bbox=(-113.9, 53.3, -113.1, 53.8)).to_crs(3400)
riv = riv[riv.intersects(edm.buffer(2000))]
merged = linemerge(unary_union(list(riv.geometry)))
nsr = max(getattr(merged, "geoms", [merged]), key=lambda g: g.intersection(edm).length)
edmonton = m3400[m3400[NAME].str.startswith("Edmonton-")]
frame = box(*unary_union(list(edmonton.geometry)).buffer(5000).bounds)


def extend(p, q, d=60_000):
    dx, dy = p[0] - q[0], p[1] - q[1]
    n = (dx * dx + dy * dy) ** 0.5
    return (p[0] + dx / n * d, p[1] + dy / n * d)


c = list(nsr.coords)
cut = LineString([extend(c[0], c[5])] + c + [extend(c[-1], c[-6])])
halves = list(split(frame, cut).geoms)
assert len(halves) == 2, "river line should cut the Edmonton frame in two"
north = next(h for h in halves if h.contains(Point(frame.centroid.x, frame.bounds[3] - 100)))
eds_b, eds_c, straddlers = [], [], []
for _, r in edmonton.iterrows():
    share = r.geometry.intersection(north).area / r.geometry.area
    (eds_b if share > 0.5 else eds_c).append(r[NAME])
    if 0.05 < share < 0.95:
        straddlers.append({"name": r[NAME], "north_share": round(share, 3)})
eds_b.sort()
eds_c.sort()

# ── (d) Clearwater County + western Mountain View County ────────────────────
rmh = e19[e19["EDName2017"] == "Rimbey-Rocky Mountain House-Sundre"].to_crs(3400).geometry.iloc[0]
mv = csd_geom("Mountain View County", 3400)
zone_d = unary_union([csd_geom("Clearwater County", 3400), mv.intersection(rmh)])


def union_of(names):
    return unary_union(list(m3400[m3400[NAME].isin(names)].geometry))


def rings(geom3400):
    g = gpd.GeoSeries([geom3400], crs=3400).to_crs(3401).iloc[0].simplify(SIMPLIFY_M)
    polys = list(getattr(g, "geoms", [g]))
    polys = [p for p in polys if p.area > 1e6]  # drop sub-km² union slivers
    return [[[round(x - ox, 1), round(y - oy, 1)] for x, y in p.exterior.coords] for p in polys]


def pin(geom3400, lonlat=None):
    """Explorer-space position for the zone's explanatory pin. An explicit
    lon/lat keeps big zones' pins clear of the flag pins around Calgary."""
    if lonlat:
        p = gpd.GeoSeries([Point(*lonlat)], crs=4326).to_crs(3400).iloc[0]
        assert geom3400.contains(p), f"pin {lonlat} must sit inside its zone"
    else:
        p = geom3400.representative_point()
    q = gpd.GeoSeries([p], crs=3400).to_crs(3401).iloc[0]
    return [round(q.x - ox, 1), round(q.y - oy, 1)]


geom_a, geom_b, geom_c = union_of(eds_a), union_of(eds_b), union_of(eds_c)
# County lines and ED lines are different datasets and disagree by slivers
# (Clearwater County grazes Canmore-Banff by ~1 km²). Clip d so the restore
# zone can never overlap a district R5 says to leave alone.
zone_d = zone_d.difference(unary_union([geom_a, geom_b]))
zones = [
    {"id": "r5-a", "cond": "a", "kind": "locked", "eds": eds_a,
     "rings": rings(geom_a), "pin": pin(geom_a, (-113.05, 50.45))},
    {"id": "r5-b", "cond": "b", "kind": "locked", "eds": eds_b,
     "rings": rings(geom_b), "pin": pin(geom_b, (-113.50, 53.60))},
    {"id": "r5-c", "cond": "c", "kind": "revert", "eds": eds_c,
     "rings": rings(geom_c), "pin": pin(geom_c, (-113.47, 53.44))},
    {"id": "r5-d", "cond": "d", "kind": "restore", "eds": [],
     "rings": rings(zone_d), "pin": pin(zone_d)},
]
data = {
    "source": "Chair's Addendum Recommendation 5, commission final report pp. 66-67; "
              "district sets read off the majority 2026 map. Built by analysis/scripts/build_lunty_bounds.py.",
    "zones": zones,
    # Edmonton EDs with more than 5% of their area on each bank; each is filed
    # in b or c by the bank that holds most of it.
    "river_straddlers": straddlers,
}
out = REPO / "viewer" / "static" / "mapdata" / "lunty_bounds.json"
out.write_text(json.dumps(data, ensure_ascii=False))
for z in zones:
    print(f"{z['id']}: {len(z['eds'])} EDs, {len(z['rings'])} ring(s), "
          f"{sum(len(r) for r in z['rings'])} pts")
print(f"straddling the river: {straddlers}")
dl = gpd.GeoSeries([zone_d], crs=3400).to_crs(4326).iloc[0]
print(f"zone d southern edge {dl.bounds[1]:.4f}N vs Airdrie's southern limit {airdrie_south:.4f}N")
assert dl.bounds[1] > airdrie_south, "the restore zone must sit north of Airdrie (R5(a))"
assert zone_d.intersection(unary_union([geom_a, geom_b])).area < 1.0, "restore zone overlaps a no-change district"
print(f"Wrote {out}")
