"""Which electoral divisions hold each municipality, on each official map.

Overlays 2021 census dissemination areas (population) on the two official
Elections Alberta 2026 layers and reports, for each municipality named in the
codebook, the share of its 2021 population that falls in each division
(DA assigned by representative point). Used to state precisely what each
final map does in each coded configuration.

Usage: python3 00_geometry_check.py SHAPEFILE_ROOT DA_PROFILE_CSV > geometry_check.txt
  SHAPEFILE_ROOT = data/shapefiles (the large-file objects must be present)
  DA_PROFILE_CSV = data/census_2021/alberta_da_profile.csv (pop_2021 by DAUID)
"""
import sys
import warnings

import geopandas as gpd
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = sys.argv[1].rstrip("/")
PLACES = ["Airdrie", "Cochrane", "Chestermere", "Red Deer", "Sylvan Lake",
          "Blackfalds", "Innisfail", "Lacombe", "Penhold", "St. Albert",
          "Morinville", "Lethbridge", "Coaldale", "Clearwater County",
          "Rocky Mountain House", "Sundre", "Cremona", "Banff",
          "Improvement District No.  9 Banff", "Improvement District No. 9 Banff",
          "Canmore", "Jasper", "Bighorn No. 8", "Olds", "Didsbury", "Carstairs",
          "Crossfield", "Beiseker", "Irricana", "Three Hills", "Trochu",
          "Mountain View County", "Rocky View County", "Kneehill County",
          "Slave Lake", "Swan Hills", "High Prairie", "Big Lakes County",
          "Lesser Slave River No.124", "Beaumont", "Okotoks", "Rimbey",
          "Sturgeon County", "Red Deer County", "Lacombe County",
          "Lethbridge County", "Strathmore"]

csd = gpd.read_file(f"{ROOT}/reference/alberta_2021_csds.gpkg")
da = gpd.read_file(f"{ROOT}/reference/alberta_2021_das.gpkg")
print("# CSD columns", csd.columns.tolist(), file=sys.stderr)
print("# DA columns", da.columns.tolist(), file=sys.stderr)
name_col = next(c for c in csd.columns if c.upper() in ("CSDNAME", "CSD_NAME", "NAME"))
pop = pd.read_csv(sys.argv[2], dtype={"DAUID": str})[["DAUID", "pop_2021"]]
da = da.merge(pop, on="DAUID", how="left").fillna({"pop_2021": 0})
pop_col = "pop_2021"
maps = {
    "majority": gpd.read_file(f"{ROOT}/canonical/ea_majority_2026_eds.gpkg"),
    "minority": gpd.read_file(f"{ROOT}/canonical/ea_minority_2026_eds.gpkg"),
}
da = da.to_crs(3400)
csd = csd.to_crs(3400)
pts = da.copy()
pts["geometry"] = da.representative_point()
pts = gpd.sjoin(pts, csd[[name_col, "geometry"]], predicate="within").drop(columns="index_right")
for label, eds in maps.items():
    eds = eds.to_crs(3400)
    ed_col = next(c for c in eds.columns if "name" in c.lower())
    j = gpd.sjoin(pts, eds[[ed_col, "geometry"]], predicate="within")
    print(f"\n===== {label} map =====")
    for place in PLACES:
        sub = j[j[name_col] == place]
        if sub.empty:
            continue
        tot = sub[pop_col].astype(float).sum()
        g = sub.groupby(ed_col)[pop_col].apply(lambda s: s.astype(float).sum()).sort_values(ascending=False)
        parts = "; ".join(f"{k} {v:,.0f} ({v / tot:.0%})" for k, v in g.items())
        print(f"{place} [2021 pop {tot:,.0f}]: {parts}")
