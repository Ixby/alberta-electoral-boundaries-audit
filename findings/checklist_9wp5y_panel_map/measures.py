# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
measures.py
-----------
The numbers behind the OSF 9wp5y checklist scoring of the panel's map
(findings/checklist_9wp5y_panel_map.md). Read-only; writes measures.json beside it.

- Calgary zone gap (S1a, W2): the registered Zone A / Zone B name lists, copied
  from the OSF-archived electoral_forensics_population.py (SHA-256 860e2aa7...),
  on the panel's stated populations (App. 7). Names in neither list are reported.
- Edmonton river partition (S2a): south = the interim report's south-of-river
  divisions as named in App. 7, plus Edmonton-Nisku; north = the rest. Also the
  largest gap any split of the 21 divisions into two zones of 3 or more could give.
- City pieces (S1b, S2b): on the reconstructed map (provisional), for every city
  or town of 8,000 or more (2021): districts holding any of its 2021 land, and
  districts holding 2% or more of its 2021 people (DAs shared by area; the
  piece rule of Amendment 5, Part 17).
- Protected land (S1c, S2c, S3): share of each low-population division's area in
  the 2021 census subdivisions that are national or provincial parks
  (Improvement Districts 4, 9, 12, 13, 24, 25 and Kananaskis). Wilderness
  areas and other parks are not census subdivisions and are not counted. The
  same measure is run on the two commission maps as a check.

Backward: data/iap/iap_app7_populations.csv, data/iap/abebc_interim_edmonton_south.csv,
  findings/a10_stepb_run/districts_real_map.gpkg (the assembled reconstruction),
  data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg,
  data/shapefiles/reference/alberta_2021_{das,csds}.gpkg,
  data/reference/alberta_2021_{da,csd}_populations.csv
Forward: findings/checklist_9wp5y_panel_map.md
"""
import json
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

ZONE_A = {"Calgary-Beddington", "Calgary-Bhullar-McCall", "Calgary-Buffalo", "Calgary-Confluence",
          "Calgary-Cross", "Calgary-Currie", "Calgary-East", "Calgary-Edgemont", "Calgary-Falconridge",
          "Calgary-Falconridge-Conrich", "Calgary-Foothills", "Calgary-Foothills-Airdrie West",
          "Calgary-Greenway", "Calgary-Klein", "Calgary-McCall", "Calgary-McCall-Bhullar",
          "Calgary-Mountain View", "Calgary-Nolan Hill-Cochrane", "Calgary-North", "Calgary-North East",
          "Calgary-North West", "Calgary-North West-Bearspaw", "Calgary-Nose Creek", "Calgary-Nose Hill",
          "Calgary-Skyview", "Calgary-Symons Valley", "Calgary-Varsity", "Calgary-Airdrie"}
ZONE_B = {"Calgary-Acadia", "Calgary-Bow", "Calgary-Bow-Springbank", "Calgary-De Winton", "Calgary-Elbow",
          "Calgary-Fish Creek", "Calgary-Glenmore", "Calgary-Glenmore-Tsuut'ina", "Calgary-Hays",
          "Calgary-Lougheed", "Calgary-McKenzie", "Calgary-Peigan", "Calgary-Peigan-Chestermere",
          "Calgary-Shaw", "Calgary-South", "Calgary-South East", "Calgary-West", "Calgary-West-Elbow Valley",
          "Calgary-West-Tsuut'ina"}
PARK_CSDS = ["4803003", "4815032", "4815037", "4810068", "4816051", "4814028", "4815013"]
LOW = ["Central Peace-Notley", "Lesser Slave Lake", "Rocky Mountain House-Sundre",
       "Rocky Mountain House-Banff Park", "Canmore-Banff", "Banff-Canmore-Diamond Valley",
       "Lac Ste. Anne"]


def mean(xs):
    return sum(xs) / len(xs)


def zones(pop):
    cal = {d: p for d, p in pop.items() if d.startswith("Calgary")}
    a = [p for d, p in cal.items() if d in ZONE_A]
    b = [p for d, p in cal.items() if d in ZONE_B]
    un = sorted(d for d in cal if d not in ZONE_A and d not in ZONE_B)
    out = {"n_a": len(a), "n_b": len(b), "mean_a": round(mean(a)), "mean_b": round(mean(b)),
           "gap_pct_a_vs_b": round((mean(a) - mean(b)) / mean(b) * 100, 2), "unclassified": un}
    for d in un:  # by the registered geographic rule a west/south district would be Zone B
        b2 = b + [cal[d]]
        out[f"gap_pct_with_{d}_in_b"] = round((mean(a) - mean(b2)) / mean(b2) * 100, 2)
    return out


def edmonton(pop):
    south = set(pd.read_csv(REPO / "data/iap/abebc_interim_edmonton_south.csv")["app7_division"].dropna())
    ed = sorted(d for d in pop if d.startswith("Edmonton"))
    s = [d for d in ed if d in south or d == "Edmonton-Nisku"]
    n = [d for d in ed if d not in s]
    ms, mn = mean([pop[d] for d in s]), mean([pop[d] for d in n])
    v = sorted(pop[d] for d in ed)
    bound = max((mean(v[k:]) - mean(v[:k])) / mean(v[:k]) * 100 for k in range(3, len(v) - 2))
    return {"south": s, "north": n, "mean_south": round(ms), "mean_north": round(mn),
            "gap_pct_north_vs_south": round((mn - ms) / ms * 100, 2),
            "largest_gap_any_two_zones_of_3_or_more": round(bound, 2)}


def city_pieces(eds, name):
    csd = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(3401)
    cp = pd.read_csv(REPO / "data/reference/alberta_2021_csd_populations.csv").set_index("ALT_GEO_CODE")["population_2021"]
    csd["pop21"] = csd["CSDUID"].astype(int).map(cp)
    cities = csd[csd["CSDTYPE"].isin(["CY", "T"]) & (csd["pop21"] >= 8000)]
    da = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_das.gpkg").to_crs(3401)
    pops = pd.read_csv(REPO / "data/reference/alberta_2021_da_populations.csv").set_index("DGUID")
    da["pop"] = da["DGUID"].map(pops["population_2021"]).fillna(0.0)
    pt = da[["DGUID", "geometry"]].copy()
    pt["geometry"] = da.geometry.representative_point()
    inc = gpd.sjoin(pt, cities[["CSDUID", "geometry"]], how="inner", predicate="within")
    o = gpd.overlay(da[["DGUID", "pop", "geometry"]], eds[[name, "geometry"]], how="intersection",
                    keep_geom_type=True)
    o["a"] = o.area
    o["p"] = o["pop"] * o["a"] / o.groupby("DGUID")["a"].transform("sum")
    o = o.merge(inc[["DGUID", "CSDUID"]], on="DGUID")
    rows = []
    for _, c in cities.iterrows():
        land = eds.geometry.intersection(c.geometry).area / 1e6
        terr = {eds[name].iloc[i]: round(float(a), 3) for i, a in enumerate(land) if a > 0}
        g = o[o["CSDUID"] == c["CSDUID"]].groupby(name)["p"].sum()
        rows.append({"csd": c["CSDNAME"], "type": c["CSDTYPE"], "pop2021": int(c["pop21"]),
                     "districts_by_territory": len(terr),
                     "districts_2pct_people": int((g / g.sum() >= 0.02).sum()) if g.sum() else 0,
                     "territory_km2": dict(sorted(terr.items(), key=lambda x: -x[1])),
                     "people": {k: round(float(v)) for k, v in g.sort_values(ascending=False).items() if v >= 1}})
    return sorted(rows, key=lambda r: (-r["districts_by_territory"], r["csd"]))


def protected(eds, name):
    csd = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(3401)
    parks = csd[csd["CSDUID"].astype(str).isin(PARK_CSDS)]
    out = {}
    for _, r in eds[eds[name].isin(LOW)].iterrows():
        g = r.geometry
        parts = {p["CSDNAME"]: round(g.intersection(p.geometry).area / g.area * 100, 2)
                 for _, p in parks.iterrows() if g.intersection(p.geometry).area / g.area > 0.0005}
        out[r[name]] = {"area_km2": round(g.area / 1e6), "park_csd_share_pct": parts,
                        "total_pct": round(sum(parts.values()), 2)}
    return out


def main():
    app7 = pd.read_csv(REPO / "data/iap/iap_app7_populations.csv")
    pop = dict(zip(app7["district"], app7["population"]))
    panel = gpd.read_file(REPO / "findings/a10_stepb_run/districts_real_map.gpkg").to_crs(3401)
    res = {"calgary_zones_panel_stated": zones(pop), "edmonton_panel_stated": edmonton(pop),
           "city_pieces_panel_reconstruction": city_pieces(panel, "district"),
           "protected_share": {"panel_reconstruction": protected(panel, "district")}}
    for m in ["majority", "minority"]:
        eds = gpd.read_file(REPO / f"data/shapefiles/canonical/ea_{m}_2026_eds.gpkg").to_crs(3401)
        res["protected_share"][m] = protected(eds, "EDName2025")
    (HERE / "measures.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
    print(json.dumps({k: v for k, v in res.items() if k != "city_pieces_panel_reconstruction"},
                     indent=1, ensure_ascii=False))
    for r in res["city_pieces_panel_reconstruction"]:
        if r["districts_by_territory"] >= 3 or r["districts_2pct_people"] >= 3 or r["csd"] in ("Airdrie", "Cochrane"):
            print(r["csd"], r["districts_by_territory"], r["districts_2pct_people"], r["people"])


if __name__ == "__main__":
    main()
