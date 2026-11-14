# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Statistics Canada 2021 (Open Government Licence), Elections Alberta
"""
count.py
--------
Entry: 2026-11-13 05:00 Alberta time · claude-fable-5-2 · low

How many ridings on each map have a majority of residents living in an urban municipality?
Checks a public claim that 82% of Albertans, in urban centres, are represented by 42% of the
seats on the 91-riding map. Descriptive, exploratory, not registered. Says nothing about why
any line was drawn. Read-only; writes count.json.

Method: each 2021 dissemination area (with its 2021 population) is placed in the municipality
and in the riding that hold its representative point. Two definitions of urban are reported:
  cities_only      census subdivisions of type CY
  cities_and_towns types CY and T, plus Strathcona County and Wood Buffalo, whose urban service
                   areas (Sherwood Park, Fort McMurray) are not separate census subdivisions.
                   This counts the rural parts of those two as urban, so it overstates a little.
Neither is Statistics Canada's "population centre" measure (the usual source of an 82% figure);
the two bracket it. A riding is urban-majority when over half its residents are urban.

Backward: data/shapefiles/reference/alberta_2021_{das,csds}.gpkg,
  data/reference/alberta_2021_da_populations.csv, the four maps in MAPS.
Forward: findings/urban_majority_ridings/README.md
"""
import hashlib
import json
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
STAMP = "2026-11-13 05:00 Alberta time · claude-fable-5-2 · low"
DAS = "data/shapefiles/reference/alberta_2021_das.gpkg"
CSDS = "data/shapefiles/reference/alberta_2021_csds.gpkg"
POP = "data/reference/alberta_2021_da_populations.csv"
MAPS = {
    "map_2019": ("data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp", "EDName2017"),
    "commission_majority": ("data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
    "commission_minority": ("data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025"),
    "panel_reconstruction_v3": ("data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg", None),
}
SPECIAL = {"Strathcona County", "Wood Buffalo"}


def sha(p):
    return hashlib.sha256((REPO / p).read_bytes()).hexdigest()


def main():
    da = gpd.read_file(REPO / DAS).to_crs(3401)
    pop = pd.read_csv(REPO / POP, dtype={"DAUID": str})
    pop["DAUID"] = pop["DAUID"].astype(str).str[-8:]
    da = da.merge(pop[["DAUID", "population_2021"]], on="DAUID", how="left")
    pts = gpd.GeoDataFrame(da[["DAUID", "population_2021"]], geometry=da.geometry.representative_point(), crs=da.crs)
    csd = gpd.read_file(REPO / CSDS).to_crs(3401)[["CSDNAME", "CSDTYPE", "geometry"]]
    pts = gpd.sjoin(pts, csd, how="left", predicate="within").drop(columns="index_right")
    total = float(pts["population_2021"].sum())
    defs = {"cities_only": pts["CSDTYPE"].eq("CY"),
            "cities_and_towns": pts["CSDTYPE"].isin(["CY", "T"]) | pts["CSDNAME"].isin(SPECIAL)}
    out = {"population_2021_placed": total, "definitions": {}}
    for name, urb in defs.items():
        res = {"urban_share_of_population": float(pts.loc[urb, "population_2021"].sum() / total), "maps": {}}
        for m, (f, col) in MAPS.items():
            e = gpd.read_file(REPO / f).to_crs(3401)
            col = col or ("district" if "district" in e.columns else [c for c in e.columns if c != "geometry"][0])
            j = gpd.sjoin(pts.assign(urban=urb), e[[col, "geometry"]], how="left", predicate="within")
            g = j.groupby(col).apply(lambda d: d.loc[d["urban"], "population_2021"].sum() / d["population_2021"].sum())
            n = int(len(g))
            res["maps"][m] = {"ridings": n, "urban_majority": int((g > 0.5).sum()),
                              "urban_majority_share_of_seats": float((g > 0.5).sum() / n),
                              "at_least_90_percent_urban": int((g >= 0.9).sum()),
                              "at_most_10_percent_urban": int((g <= 0.1).sum()),
                              "mixed_10_to_90_percent": int(((g > 0.1) & (g < 0.9)).sum()),
                              "unplaced_population": float(j.loc[j[col].isna(), "population_2021"].sum())}
        out["definitions"][name] = res
    out["meta"] = {"entry": STAMP, "script": "findings/urban_majority_ridings/count.py",
                   "status": "exploratory, not registered",
                   "inputs": {p: sha(p) for p in [DAS, CSDS, POP] + [f for f, _ in MAPS.values()]}}
    json.dump(out, open(HERE / "count.json", "w"), indent=1)
    print(json.dumps(out["definitions"], indent=1))


if __name__ == "__main__":
    main()
