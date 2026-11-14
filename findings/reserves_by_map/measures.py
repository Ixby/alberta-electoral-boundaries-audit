# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain), Statistics Canada 2021 (Open Government Licence) | https://ixby.github.io
"""
measures.py
-----------
Where the Blackfoot (Siksika, Kainai, Piikani), Stoney Nakoda and Tsuut'ina reserves fall on the
2019 map, the two commission maps and the panel's map (reconstruction, provisional), and how the
voting places on those reserves voted in the 2026 referendum (Question 10), against the rest of
the same 2019 division. Descriptive only, exploratory, not registered. Read-only; writes measures.json.

1. Placement: share of each reserve's land (2021 census subdivisions of type IRI) in each district.
   A district holding under 1% of a reserve's land is ignored. That is below the reconstruction's
   edge error.
2. Referendum: election-day results by voting place, for the four 2019 divisions that hold these
   reserves (inputs/referendum2026_q10_ed*.xlsx, downloaded from officialresults.elections.ab.ca on
   2026-11-10, Question 10 only). The referendum's voting-area numbers do not match the 2023
   voting-area polygons, so on-reserve voting places are named in RESERVE_PLACES, each with how its
   location was established. Advance, mobile and special ballots are reported by voting place or
   division and cannot be placed on or off a reserve, so they are left out of both sides.

Backward: data/shapefiles/reference/alberta_2021_csds.gpkg, data/reference/alberta_2021_csd_populations.csv,
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp,
  data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg,
  findings/a10_stepb_run/districts_real_map.gpkg, findings/reserves_by_map/inputs/*.xlsx
Forward: findings/reserves_by_map/README.md
"""
import hashlib
import json
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
from _xlsx import rows  # noqa: E402

RESERVES = {  # CSDUID: (nation, reserve)
    "4805802": ("Siksika (Blackfoot)", "Siksika 146"),
    "4803802": ("Kainai (Blackfoot)", "Blood 148"),
    "4803803": ("Kainai (Blackfoot)", "Blood 148A"),
    "4803801": ("Piikani (Blackfoot)", "Piikani 147"),
    "4803805": ("Piikani (Blackfoot)", "Peigan Timber Limit B"),
    "4815802": ("Stoney Nakoda", "Stoney 142, 143, 144 (Morley)"),
    "4815815": ("Stoney Nakoda", "Stoney 142B"),
    "4806803": ("Stoney Nakoda", "Eden Valley 216"),
    "4809810": ("Stoney Nakoda", "Big Horn 144A"),
    "4806804": ("Tsuut'ina", "Tsuut'ina 145"),
}
MAPS = {
    "2019": ("data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp", "EDName2017"),
    "commission_majority": ("data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
    "commission_minority": ("data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025"),
    "panel_reconstruction": ("findings/a10_stepb_run/districts_real_map.gpkg", "district"),
}
# (2019 ED number, voting place name as printed): (nation, how the location was established)
RESERVE_PLACES = {
    (54, "Siksika Piiksapi Memorial Arbour"): ("Siksika (Blackfoot)", "named for Siksika"),
    (54, "Siksika Deerfoot Sportplex"): ("Siksika (Blackfoot)", "named for Siksika"),
    (54, "Kainai Multi Purpose Building"): ("Kainai (Blackfoot)", "named for Kainai"),
    (54, "Lavern Community Hall"): ("Kainai (Blackfoot)", "Levern is a community on the Blood reserve"),
    (54, "Moses Lake Gym"): ("Kainai (Blackfoot)", "Moses Lake is a community on the Blood reserve"),
    (73, "Piikani Nation Community Hall"): ("Piikani (Blackfoot)", "named for Piikani"),
    (73, "Multipurpose Sprung Building"): ("Stoney Nakoda", "Bearspaw First Nation's Sprung building at Eden Valley (opened May 2025)"),
    (50, "Stoney Nakoda"): ("Stoney Nakoda", "named for Stoney Nakoda (Morley)"),
    (50, "Chief Goodstoney Rodeo Centre - Buffalo Room"): ("Stoney Nakoda", "at Morley"),
    (80, "Big Horn Firehall"): ("Stoney Nakoda", "named for Big Horn 144A"),
}
# On Tsuut'ina land but not counted as a reserve community: Redwood Meadows is a townsite on
# Tsuut'ina 145 whose residents are mostly leaseholders, not members. Reported separately.
MIXED_PLACES = {(50, "Redwood House"): ("Tsuut'ina land (Redwood Meadows townsite)", "leasehold townsite on Tsuut'ina 145")}
EDS = {50: "Banff-Kananaskis", 54: "Cardston-Siksika", 73: "Livingstone-Macleod", 80: "Rimbey-Rocky Mountain House-Sundre"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def placement():
    csd = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(3401)
    pop = pd.read_csv(REPO / "data/reference/alberta_2021_csd_populations.csv").set_index("ALT_GEO_CODE")["population_2021"]
    res = csd[csd["CSDUID"].astype(str).isin(RESERVES)].copy()
    out = []
    maps = {m: gpd.read_file(REPO / f).to_crs(3401) for m, (f, _) in MAPS.items()}
    for _, r in res.iterrows():
        nation, name = RESERVES[str(r["CSDUID"])]
        p = pop.get(int(r["CSDUID"]))
        row = {"nation": nation, "reserve": name, "csduid": str(r["CSDUID"]),
               "population_2021": None if pd.isna(p) else int(p), "land_km2": round(r.geometry.area / 1e6, 1), "maps": {}}
        for m, (_, col) in MAPS.items():
            e = maps[m]
            shares = {}
            for _, d in e.iterrows():
                a = r.geometry.intersection(d.geometry).area / r.geometry.area
                if a >= 0.01:
                    shares[d[col]] = round(a * 100, 1)
            row["maps"][m] = dict(sorted(shares.items(), key=lambda x: -x[1]))
        out.append(row)
    out.sort(key=lambda x: (x["nation"], x["reserve"]))
    nations = {}
    for m in MAPS:
        for n in sorted({x["nation"].split(" (")[0] if "Blackfoot" not in x["nation"] else "Blackfoot Confederacy (Alberta)" for x in out}):
            ds = set()
            for x in out:
                key = "Blackfoot Confederacy (Alberta)" if "Blackfoot" in x["nation"] else x["nation"]
                if key == n and (x["population_2021"] or 0) + (1 if x["population_2021"] is None else 0) > 0:
                    ds |= {d for d, s in x["maps"][m].items() if s >= 50}
            nations.setdefault(n, {})[m] = sorted(ds)
    return out, nations


def referendum():
    places, ed_rest = [], {}
    for ed in EDS:
        f = HERE / f"inputs/referendum2026_q10_ed{ed}.xlsx"
        rest = {"option1": 0, "option2": 0, "electors": 0}
        for r in rows(f):
            if len(r) < 7 or r[2] != "Election Day":
                continue
            name, elect, o1, o2 = r[1], float(r[3] or 0), float(r[4] or 0), float(r[5] or 0)
            key = (ed, name)
            if key in RESERVE_PLACES or key in MIXED_PLACES:
                nation, how = RESERVE_PLACES.get(key) or MIXED_PLACES[key]
                places.append({"ed2019": EDS[ed], "voting_area": r[0], "voting_place": name, "nation": nation,
                               "located_by": how, "on_reserve_community": key in RESERVE_PLACES,
                               "electors_on_list": int(elect), "remain": int(o1), "begin_separation_process": int(o2),
                               "remain_pct": round(100 * o1 / (o1 + o2), 1) if o1 + o2 else None})
            else:
                rest["option1"] += o1
                rest["option2"] += o2
                rest["electors"] += elect
        t = rest["option1"] + rest["option2"]
        ed_rest[EDS[ed]] = {"remain": int(rest["option1"]), "begin_separation_process": int(rest["option2"]),
                            "remain_pct": round(100 * rest["option1"] / t, 1)}
    by_nation = {}
    for p in places:
        if not p["on_reserve_community"]:
            continue
        b = by_nation.setdefault(p["nation"], {"remain": 0, "begin_separation_process": 0})
        b["remain"] += p["remain"]
        b["begin_separation_process"] += p["begin_separation_process"]
    for b in by_nation.values():
        t = b["remain"] + b["begin_separation_process"]
        b["remain_pct"] = round(100 * b["remain"] / t, 1) if t else None
    return places, by_nation, ed_rest


def main():
    place, nations = placement()
    vp, by_nation, ed_rest = referendum()
    res = {"meta": {"status": "exploratory, descriptive, not registered",
                    "panel_map": "reconstruction (provisional until the official file is posted)",
                    "referendum_source": "https://officialresults.elections.ab.ca/orPollResultsReferendum2026.cfm?EventID=202610&ED=NN&MODE=exED, downloaded 2026-11-10 21:01 Alberta time",
                    "inputs": {str(p.relative_to(REPO)).replace("\\", "/"): sha(p) for p in sorted((HERE / "inputs").glob("*.xlsx"))}},
           "placement": place, "districts_holding_each_nation": nations,
           "referendum_q10_on_reserve_places": vp, "referendum_q10_by_nation": by_nation,
           "referendum_q10_rest_of_division_election_day": ed_rest}
    (HERE / "measures.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("districts_holding_each_nation", "referendum_q10_by_nation", "referendum_q10_rest_of_division_election_day")}, indent=1, ensure_ascii=False))
    for p in vp:
        print(p["ed2019"], p["voting_place"], p["electors_on_list"], p["remain"], p["begin_separation_process"], p["remain_pct"])


if __name__ == "__main__":
    main()
