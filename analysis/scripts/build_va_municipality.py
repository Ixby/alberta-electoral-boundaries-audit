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
