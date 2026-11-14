# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Statistics Canada 2021 (Open Government Licence), Government of Alberta (Open Government Licence – Alberta)
"""
placements_all.py
-----------------
Entry: 2026-11-10 21:28 Alberta time · claude-opus-5-5 · medium

Which district holds each First Nations reserve and each Métis settlement in Alberta, on the
2019 map, the two commission maps and the panel's map (reconstruction, provisional). Used to
check each public submission's request against each final map (submissions.md). Descriptive
only; not registered. Read-only; writes placements_all.json and placements_all.csv.

Reserves: every 2021 census subdivision of type IRI (83). Métis settlements: the Government of
Alberta boundaries (8 settlements, 10 polygons, merged by name). The census file does not carry
the settlements. Share of land in each district; under 1% is ignored, as in measures.py.

Backward: data/shapefiles/reference/alberta_2021_csds.gpkg,
  data/shapefiles/reference/metis_settlements_dl/metis_settlements_goa.geojson,
  data/reference/alberta_2021_csd_populations.csv, and the four maps in measures.MAPS.
Forward: findings/reserves_by_map/submissions.md
"""
import csv
import hashlib
import json
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
STAMP = "2026-11-10 21:28 Alberta time · claude-opus-5-5 · medium"
MAPS = {
    "2019": ("data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp", "EDName2017"),
    "commission_majority": ("data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
    "commission_minority": ("data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025"),
    "panel_reconstruction": ("findings/a10_stepb_run/districts_real_map.gpkg", "district"),
}
CSD = "data/shapefiles/reference/alberta_2021_csds.gpkg"
METIS = "data/shapefiles/reference/metis_settlements_dl/metis_settlements_goa.geojson"
POP = "data/reference/alberta_2021_csd_populations.csv"


def sha(p):
    return hashlib.sha256((REPO / p).read_bytes()).hexdigest()


def main():
    csd = gpd.read_file(REPO / CSD).to_crs(3401)
    pop = pd.read_csv(REPO / POP).set_index("ALT_GEO_CODE")["population_2021"]
    res = csd[csd["CSDTYPE"] == "IRI"][["CSDUID", "CSDNAME", "geometry"]].copy()
    res["kind"] = "reserve"
    res["population_2021"] = [None if pd.isna(pop.get(int(u))) else int(pop.get(int(u))) for u in res["CSDUID"]]
    ms = gpd.read_file(REPO / METIS).to_crs(3401).dissolve(by="METIS_NAME").reset_index()
    ms = gpd.GeoDataFrame({"CSDUID": "", "CSDNAME": ms["METIS_NAME"] + " Métis Settlement",
                           "geometry": ms.geometry, "kind": "metis_settlement",
                           "population_2021": None}, crs=ms.crs)
    places = pd.concat([res, ms], ignore_index=True)
    maps = {m: gpd.read_file(REPO / f).to_crs(3401) for m, (f, _) in MAPS.items()}
    out = []
    for _, r in places.iterrows():
        row = {"place": r["CSDNAME"], "kind": r["kind"], "csduid": str(r["CSDUID"]),
               "population_2021": None if pd.isna(r["population_2021"]) else int(r["population_2021"]), "land_km2": round(r.geometry.area / 1e6, 1), "maps": {}}
        for m, (_, col) in MAPS.items():
            e = maps[m]
            hit = e[e.intersects(r.geometry)]
            shares = {}
            for _, d in hit.iterrows():
                a = r.geometry.intersection(d.geometry).area / r.geometry.area
                if a >= 0.01:
                    shares[d[col]] = round(a * 100, 1)
            row["maps"][m] = dict(sorted(shares.items(), key=lambda x: -x[1]))
        out.append(row)
    out.sort(key=lambda x: (x["kind"], x["place"]))
    meta = {"entry": STAMP, "script": "findings/reserves_by_map/placements_all.py",
            "inputs": {p: sha(p) for p in [CSD, METIS, POP] + [f for f, _ in MAPS.values()]},
            "rule": "share of each place's land in each district; under 1% ignored"}
    json.dump({"meta": meta, "places": out}, open(HERE / "placements_all.json", "w"), indent=1, ensure_ascii=False)
    with open(HERE / "placements_all.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["place", "kind", "csduid", "population_2021", "land_km2"] + [f"{m}_district" for m in MAPS] + [f"{m}_split" for m in MAPS])
        for x in out:
            main_d = [next(iter(x["maps"][m]), "") for m in MAPS]
            split = ["; ".join(f"{d} {s}%" for d, s in x["maps"][m].items()) if len(x["maps"][m]) > 1 else "" for m in MAPS]
            w.writerow([x["place"], x["kind"], x["csduid"], x["population_2021"] if x["population_2021"] is not None else "", x["land_km2"]] + main_d + split)
    print(len(out), "places")


if __name__ == "__main__":
    main()
