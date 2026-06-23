# Alberta Electoral Boundary Audit — per-VA municipality (for search disambiguation)
#
# Derives a municipality label per VA, aligned to the explorer's VA id order
# (build_cover._prepare_map_data("minority"), same ordering build_explorer_tiles
# uses for va_props). Municipality = "Calgary"/"Edmonton" when the VA centroid
# falls inside those cities' neighbourhood polygons, else the nearest CGNDB
# populated place (the town/village/county that disambiguates rural communities).
#
# Writes viewer/static/mapdata/va_muni.json: a JSON array indexed by VA id.
# Reuses the same C:\tmp geocoding caches as community_names() in the tiler.
import json, sys, os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cover
import geopandas as gpd
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "viewer" / "static" / "mapdata" / "va_muni.json"

eds, name_col, va_render, va_ed_map = build_cover._prepare_map_data("minority")
cent = gpd.GeoDataFrame(geometry=list(va_render.geometry.centroid), crs=3401)
n = len(cent)
print(f"VAs={n}")


def within_flags(poly_path, layer):
    """True/False per VA: centroid within any polygon of the given city layer."""
    g = gpd.read_file(poly_path).set_crs(4326, allow_override=True).to_crs(3401)
    j = gpd.sjoin(cent, g[["geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].sort_index()
    return j["index_right"].notna().tolist()


in_cal = within_flags(r"C:\tmp\calgary_comm.json", "calgary")
in_edm = within_flags(r"C:\tmp\edmonton_nbhd.json", "edmonton")

# Nearest CGNDB populated place → rural / town municipality.
POP = {"City", "Town", "Village", "Summer Village", "Hamlet", "Locality",
       "First Nation Administrative Location", "Indian Reserve", "Municipal District", "County"}
cgn = pd.read_csv(r"C:\tmp\cgn_ab\cgn_ab_csv_eng.csv")
cgn = cgn[cgn["Generic Term"].isin(POP)]
gn = gpd.GeoDataFrame(cgn, geometry=gpd.points_from_xy(cgn["Longitude"], cgn["Latitude"]), crs=4326).to_crs(3401)
nj = gpd.sjoin_nearest(cent, gn[["Geographical Name", "geometry"]], how="left")
nj = nj[~nj.index.duplicated(keep="first")].sort_index()
nearest = list(nj["Geographical Name"].fillna(""))

muni = []
for i in range(n):
    if i < len(in_cal) and in_cal[i]:
        muni.append("Calgary")
    elif i < len(in_edm) and in_edm[i]:
        muni.append("Edmonton")
    else:
        muni.append(str(nearest[i]) if i < len(nearest) else "")

OUT.write_text(json.dumps(muni))
print(f"Wrote {OUT}")
print(f"  Calgary={muni.count('Calgary')} Edmonton={muni.count('Edmonton')} "
      f"other={sum(1 for m in muni if m and m not in ('Calgary', 'Edmonton'))} blank={muni.count('')}")

# ── Per-place geometry: centroid + radius, for the distinct community marker ──
# Keyed by (community, municipality) — the same distinct-place key the JS index
# builder uses — so each community search hit can draw a center point and a ring
# scaled to the place's extent (not the whole ED). Origin-shifted to the deck
# coordinate space; radius is half the bbox max dimension, in metres.
va_props = json.loads((REPO / "viewer" / "static" / "mapdata" / "va_props.json").read_text())
community = [str(p.get("community", "")).strip() for p in va_props]
meta = json.loads((REPO / "docs" / "data" / "map_meta.json").read_text())
ox, oy = meta["origin_x"], meta["origin_y"]
cx_arr = list(cent.geometry.x)
cy_arr = list(cent.geometry.y)
bounds = va_render.geometry.bounds  # DataFrame: minx, miny, maxx, maxy
groups = {}
for i in range(n):
    c = community[i] if i < len(community) else ""
    if not c:
        continue
    key = c + "|" + muni[i]
    b = bounds.iloc[i]
    g = groups.get(key)
    if g is None:
        g = {"sx": 0.0, "sy": 0.0, "k": 0, "minx": b.minx, "miny": b.miny, "maxx": b.maxx, "maxy": b.maxy}
        groups[key] = g
    g["sx"] += cx_arr[i]
    g["sy"] += cy_arr[i]
    g["k"] += 1
    g["minx"] = min(g["minx"], b.minx); g["miny"] = min(g["miny"], b.miny)
    g["maxx"] = max(g["maxx"], b.maxx); g["maxy"] = max(g["maxy"], b.maxy)
geom = {}
for key, g in groups.items():
    ccx = round(g["sx"] / g["k"] - ox, 2)
    ccy = round(g["sy"] / g["k"] - oy, 2)
    crad = round(max(g["maxx"] - g["minx"], g["maxy"] - g["miny"]) / 2, 1)
    geom[key] = [ccx, ccy, crad]
GEOM_OUT = REPO / "viewer" / "static" / "mapdata" / "community_geom_2019.json"
GEOM_OUT.write_text(json.dumps(geom, separators=(",", ":")))
print(f"Wrote {GEOM_OUT}: {len(geom)} places")
