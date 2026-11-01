# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
cracking_signature_rescore.py
-----------------------------

Rescores the registered cracking-signature test (academic report §5.3.2) on
Elections Alberta's official 2026 boundaries, criterion by criterion, with
the rule unchanged.

The registered rule (v1.2 audit prompt, "Cracking signature detection",
commit 249cff7d; threshold row 12 of preregistration/thresholds.md):
  C1  the community is divided across N districts, N above the number a
      single-centre-of-gravity assignment gives;
  C2  in each of those N districts the community's voters are a minority;
  C3  the community could be held in a single district within +/-25% of the
      provincial average.
  All three met: signature detected. C1 and C2 met but the community too
  large for one district: "forced by population". Otherwise not detected.

Facts come from airdrie_split_shares.py's method (2021 census DAs over the
official boundaries; DA in the community when its representative point lies
in the community's 2021 CSD; cut DAs shared by area), run for each community.
  N (by territory)  districts holding any of the community's residents
  N (by people)     districts holding >= 2% of them (Amendment 5, Part 17 piece rule)
  minimum           ceil(population / (1.25 x average)), the population-
                    dictated minimum (Amendment 5, Part 17); 2 for Airdrie, as the
                    report's "centre-of-gravity minimum"
  C2 is tested on every district with residents and, separately, on the
                    pieces holding >= 2%; both are reported.
  C3 (registered)   0.75 x average <= population <= 1.25 x average
  C3 (restated)     the 2026-06-12 reading in §5.3.2, written for Airdrie:
                    feasible at the 2-district minimum, i.e. population
                    <= 2 x 1.25 x average; for a community that fits one
                    district or is too small for one, the registered reading
Average = 54,929 (the commission's 4,888,723 / 89, as used in §5.3.2).

Scored here because §5.3.2 scored them: Airdrie (minority, majority),
Cochrane (minority, majority), Chestermere (majority). Chestermere on the
minority map is computed for reference only: §5.3.2 does not score it, but
the site cites §5.3.2 for it.

Backward: analysis/scripts/airdrie_split_shares.py (method and functions),
  data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg,
  data/shapefiles/reference/alberta_2021_{das,csds}.gpkg,
  data/reference/alberta_2021_{da,csd}_populations.csv
Forward: data/outputs/cracking_signature_rescore_2026-10-31.json

Usage
  python analysis/scripts/cracking_signature_rescore.py [--out PATH]
"""
import argparse
import json
import math
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import airdrie_split_shares as splits  # noqa: E402

REPO = splits.REPO
AVERAGE = 54929
LOW, HIGH = round(AVERAGE * 0.75), round(AVERAGE * 1.25)  # 41,197 and 68,661
COMMUNITIES = {"Airdrie": "4806021", "Cochrane": "4806019", "Chestermere": "4806017"}
SCORED_IN_REPORT = {("Airdrie", "minority"), ("Airdrie", "majority"),
                    ("Cochrane", "minority"), ("Cochrane", "majority"),
                    ("Chestermere", "majority")}
# Later vintages cited in §5.3.2 (Airdrie municipal censuses, July 2024 and April 2025)
OTHER_VINTAGES = {"Airdrie": {"2024_municipal": 85805, "2025_municipal": 90044}}
DEFAULT_OUT = REPO / "data/outputs/cracking_signature_rescore_2026-10-31.json"


def score(name, plan, m, pop, official):
    rows = m["districts"]
    pieces = [r for r in rows if r["piece_2pct"]]
    minimum = math.ceil(pop / HIGH)
    n_any, n_pieces = len(rows), len(pieces)
    c1 = n_pieces > minimum
    c2_pieces = all(r["share_of_district_airdrie"] < 0.5 for r in pieces)
    c2_all = all(r["share_of_district_airdrie"] < 0.5 for r in rows)
    c3_reg = LOW <= pop <= HIGH
    # the restatement was written for a community too large for one district;
    # for any other community it is the registered reading
    c3_restated = pop <= 2 * HIGH if pop > HIGH else c3_reg
    if c1 and c2_pieces and c3_reg:
        result = "detected"
    elif c1 and c2_pieces and pop > HIGH:
        result = "forced by population"
    else:
        result = "not detected"
    out = {
        "scored_in_section_5_3_2": (name, plan) in SCORED_IN_REPORT,
        "population_2021": pop,
        "minimum_districts": minimum,
        "districts_by_territory": n_any,
        "districts_by_people_2pct": n_pieces,
        "C1_split_above_minimum": c1,
        "C1_note": f"{n_pieces} piece(s) holding >= 2% ({n_any} with any residents) vs minimum {minimum}",
        "C2_minority_in_every_piece": c2_pieces,
        "C2_minority_in_every_district_with_residents": c2_all,
        "C2_majority_in": [r["district"] for r in rows if r["share_of_district_airdrie"] >= 0.5],
        "C3_registered_one_district_within_band": c3_reg,
        "C3_band": [LOW, HIGH],
        "C3_restated_two_district_minimum": c3_restated,
        "result_by_registered_rule": result,
        "result_if_C3_read_as_restated": ("detected" if c1 and c2_pieces and c3_restated
                                          else result),
        "cracking_adjacent_pattern_C1_C2_not_C3": c1 and c2_pieces and not c3_reg,
        "districts": [{
            "district": r["district"],
            "residents": r["airdrie_residents"],
            "share_of_community": r["share_of_airdrie_held"],
            "share_of_district": r["share_of_district_airdrie"],
            "district_pop_2021_da": r["district_pop_2021_da"],
            "district_pop_official": r["district_pop_official"],
            "rep_point_residents": r["check_rep_point_airdrie_residents"],
            "rests_only_on_cut_das": r["rests_only_on_cut_das"],
            "residents_by_csd_top3": r["residents_by_csd_top3"],
        } for r in rows],
    }
    for label, v in OTHER_VINTAGES.get(name, {}).items():
        out[f"C3_registered_at_{label}"] = LOW <= v <= HIGH
        out[f"C3_restated_at_{label}"] = v <= 2 * HIGH if v > HIGH else LOW <= v <= HIGH
    # Majority districts: the floor share if all of the district's growth to the
    # official (2024-basis) total fell outside the community
    for d in out["districts"]:
        if d["share_of_district"] >= 0.5:
            d["share_floor_if_all_growth_outside"] = round(d["residents"] / d["district_pop_official"], 4)
    return out


def main(out):
    warnings.filterwarnings("ignore")
    csd_pop = pd.read_csv(REPO / "data/reference/alberta_2021_csd_populations.csv").set_index("ALT_GEO_CODE")
    result = {
        "script": "analysis/scripts/cracking_signature_rescore.py",
        "rule": ("v1.2 audit prompt 'Cracking signature detection' (commit 249cff7d): detected iff "
                 "C1 and C2 and C3; C1 and C2 with the community too large for one district = "
                 "'forced by population'. C3 threshold: preregistration/thresholds.md row 12."),
        "average": AVERAGE,
        "communities": {},
    }
    eds = {plan: gpd.read_file(REPO / path) for plan, path in splits.MAPS.items()}
    crs = eds["majority"].crs
    for name, code in COMMUNITIES.items():
        da, pt, shape = splits.load_das(crs, code)
        pop = int(csd_pop.loc[int(code), "population_2021"])
        result["communities"][name] = {"csduid": code, "maps": {}}
        for plan in ("minority", "majority"):
            m = splits.split_map(da, pt, eds[plan], shape)
            assert m["airdrie_total_2021_da"] == pop, (name, m["airdrie_total_2021_da"], pop)
            result["communities"][name]["maps"][plan] = score(name, plan, m, pop, eds[plan])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    for name, c in result["communities"].items():
        for plan, s in c["maps"].items():
            tag = "" if s["scored_in_section_5_3_2"] else "  (reference only)"
            print(f"\n{name} / {plan}{tag}: {s['result_by_registered_rule']}"
                  f"  [C1 {s['C1_split_above_minimum']}, C2 {s['C2_minority_in_every_piece']}, "
                  f"C3 reg {s['C3_registered_one_district_within_band']}, "
                  f"C3 restated {s['C3_restated_two_district_minimum']}]  {s['C1_note']}")
            for d in s["districts"]:
                print(f"    {d['district']:34s} {d['residents']:7,} {d['share_of_community']:7.1%} "
                      f"of community  {d['share_of_district']:6.1%} of district")
    print(f"\nwrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    main(ap.parse_args().out)
