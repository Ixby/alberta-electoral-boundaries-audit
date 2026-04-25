"""v0_1_justification_tests.py

Verification pipeline for testable justifications advanced for contested
electoral divisions in the 2026 Alberta Electoral Boundaries Commission
minority (and in one case majority) reports.

Budget: 25k tokens, 40 min wall clock, no git commits.

Depends on:
    data/alberta_2021_csds.gpkg
    data/alberta_2021_csd_populations.csv
    data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
    data/v0_1_minority_2026_populations.csv
    data/v0_1_majority_2026_populations.csv

Outputs:
    data/v0_1_justification_test_inputs.csv   (intermediate tables)
    analysis/reports/v0_1_justification_tests_findings.md (written verdicts)

Run:
    python analysis/scripts/v0_1_justification_tests.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import geopandas as gpd


# Script lives at <repo>/analysis/scripts/, so parents[2] = <repo>
REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"

# Provincial quota reference (54,929 avg) and +/-25% window
QUOTA_AVG = 54_929
QUOTA_MIN = round(QUOTA_AVG * 0.75)   # 41,197
QUOTA_MAX = round(QUOTA_AVG * 1.25)   # 68,661


def load_csd_populations() -> pd.DataFrame:
    pop = pd.read_csv(DATA / "alberta_2021_csd_populations.csv")
    return pop


def load_csd_geo() -> gpd.GeoDataFrame:
    g = gpd.read_file(DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg")
    return g


def load_minority() -> pd.DataFrame:
    return pd.read_csv(DATA / "v0_1_minority_2026_populations.csv")


def load_majority() -> pd.DataFrame:
    return pd.read_csv(DATA / "v0_1_majority_2026_populations.csv")


def load_2019_eds() -> gpd.GeoDataFrame:
    return gpd.read_file(DATA / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp")


# ---------------------------------------------------------------------------
# Test 1 : Does Olds-Three Hills-Didsbury need the Airdrie slice?
# ---------------------------------------------------------------------------
def test_1_olds_airdrie(pop: pd.DataFrame) -> dict:
    """Sum of Mountain View, Kneehill + small-town CSDs in the Olds district."""
    names = [
        "Olds, Town (T)",
        "Didsbury, Town (T)",
        "Three Hills, Town (T)",
        "Carstairs, Town (T)",
        "Cremona, Village (VL)",
        "Beiseker, Village (VL)",          # technically Rocky View adjacent
        "Linden, Village (VL)",
        "Acme, Village (VL)",
        "Trochu, Town (T)",
        "Mountain View County, Municipal district (MD)",
        "Kneehill County, Municipal district (MD)",
    ]
    sub = pop[pop["GEO_NAME"].isin(names)][["GEO_NAME", "population_2021"]].copy()
    total = int(sub["population_2021"].sum())
    verdict = "FAIL (minority justification unsupported)" if total >= QUOTA_MIN \
        else "PASS (Airdrie slice required)"
    return {
        "test": "T1_olds_three_hills_didsbury",
        "included": sub.to_dict(orient="records"),
        "total_pop": total,
        "quota_min": QUOTA_MIN,
        "quota_max": QUOTA_MAX,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Test 2 : Does Rocky Mountain House-Banff Park need the NP extension?
# ---------------------------------------------------------------------------
def test_2_rmh_np(pop: pd.DataFrame, eds_2019: gpd.GeoDataFrame) -> dict:
    # Area of the 2019 predecessor
    row = eds_2019[eds_2019["EDName2017"] == "Rimbey-Rocky Mountain House-Sundre"].iloc[0]
    km2_2019 = float(row["Km2"])

    # Population of the natural rural catchment WITHOUT Banff NP
    names = [
        "Clearwater County, Municipal district (MD)",
        "Rocky Mountain House, Town (T)",
        "Caroline, Village (VL)",
        "Sundre, Town (T)",
        "Rimbey, Town (T)",
        "Ponoka County, Municipal district (MD)",
    ]
    sub = pop[pop["GEO_NAME"].isin(names)][["GEO_NAME", "population_2021"]].copy()
    total_pop = int(sub["population_2021"].sum())

    # Verdicts
    meets_area_without_np = km2_2019 > 20_000
    meets_pop_without_np = total_pop >= QUOTA_MIN
    verdict_area = (
        "FAIL (NP extension not needed for area criterion)"
        if meets_area_without_np
        else "PASS (NP extension required for area)"
    )
    verdict_pop = (
        "FAIL (district is viable without NP for population)"
        if meets_pop_without_np
        else "PASS (NP extension required for population)"
    )
    return {
        "test": "T2_rmh_np_extension",
        "km2_2019_predecessor": km2_2019,
        "area_threshold": 20_000,
        "included_pop_rows": sub.to_dict(orient="records"),
        "total_pop_no_np": total_pop,
        "verdict_area": verdict_area,
        "verdict_pop": verdict_pop,
    }


# ---------------------------------------------------------------------------
# Test 3 : Airdrie 4-way split arithmetic
# ---------------------------------------------------------------------------
def test_3_airdrie_split(pop: pd.DataFrame) -> dict:
    airdrie_pop = int(
        pop.loc[pop["GEO_NAME"] == "Airdrie, City (CY)", "population_2021"].iloc[0]
    )

    # 1-way: fits?
    fits_1way = airdrie_pop <= QUOTA_MAX
    # 2-way: each half ~ airdrie_pop/2; must pair with non-Airdrie to reach QUOTA_MIN
    half = airdrie_pop / 2
    non_airdrie_per_half = max(0, QUOTA_MIN - half)
    # 4-way: each quarter ~ airdrie_pop/4
    quarter = airdrie_pop / 4
    non_airdrie_per_quarter = max(0, QUOTA_MIN - quarter)

    verdict = (
        "FAIL (4-way split is unforced by population)"
        if half <= QUOTA_MAX and not fits_1way
        else ("FAIL (1 district fits, no split forced)" if fits_1way
              else "PASS (more splits required)")
    )
    return {
        "test": "T3_airdrie_split",
        "airdrie_pop": airdrie_pop,
        "quota_min": QUOTA_MIN,
        "quota_max": QUOTA_MAX,
        "fits_single_district": fits_1way,
        "half_if_2way_split": half,
        "non_airdrie_needed_per_half": non_airdrie_per_half,
        "quarter_if_4way_split": quarter,
        "non_airdrie_needed_per_quarter": non_airdrie_per_quarter,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Test 4 : Red Deer: 2 vs 4 districts
# ---------------------------------------------------------------------------
def test_4_red_deer(pop: pd.DataFrame,
                     majority: pd.DataFrame,
                     minority: pd.DataFrame) -> dict:
    rd_pop = int(pop.loc[pop["GEO_NAME"] == "Red Deer, City (CY)", "population_2021"].iloc[0])
    min_districts = -(-rd_pop // QUOTA_MAX)  # ceiling division
    # Majority 2-district composition
    maj_rd = majority[majority["ed_name"].isin(["Red Deer-North", "Red Deer-South"])].copy()
    # Minority 4-district composition
    min_rd = minority[minority["ed_name"].isin([
        "Red Deer-Blackfalds", "Red Deer-Innisfail",
        "Red Deer-Lacombe", "Red Deer-Sylvan Lake"
    ])].copy()

    # In 4-way split each piece gets ~rd_pop/4 Red Deer population; rest must
    # come from rural.
    quarter = rd_pop / 4
    non_rd_per_quarter = max(0, QUOTA_MIN - quarter)

    verdict = (
        "FAIL (4 Red Deer districts are unforced by population)"
        if min_districts <= 2
        else "PASS"
    )
    return {
        "test": "T4_red_deer",
        "red_deer_pop": rd_pop,
        "quota_max": QUOTA_MAX,
        "min_districts_required": min_districts,
        "majority_districts": maj_rd.to_dict(orient="records"),
        "minority_districts": min_rd.to_dict(orient="records"),
        "quarter_of_red_deer": quarter,
        "non_rd_needed_per_quarter": non_rd_per_quarter,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Test 5 : Chestermere split — is the Calgary slice necessary?
# ---------------------------------------------------------------------------
def test_5_chestermere(pop: pd.DataFrame, minority: pd.DataFrame) -> dict:
    ches_pop = int(pop.loc[pop["GEO_NAME"] == "Chestermere, City (CY)", "population_2021"].iloc[0])
    strat_pop = int(pop.loc[pop["GEO_NAME"] == "Strathmore, Town (T)", "population_2021"].iloc[0])
    wheatland_pop = int(pop.loc[pop["GEO_NAME"] == "Wheatland County, Municipal district (MD)",
                                "population_2021"].iloc[0])

    natural_pair = ches_pop + strat_pop + wheatland_pop

    # Minority Calgary-Peigan-Chestermere total population
    cpc = int(minority.loc[minority["ed_name"] == "Calgary-Peigan-Chestermere",
                           "population"].iloc[0])
    # Calgary-Peigan 2019 predecessor has tight Calgary-only boundaries;
    # the question is how much of Chestermere is absorbed.
    # The minority CSV shows Calgary-Peigan-Chestermere = 52,639; Chestermere-Strathmore = 52,982.
    ches_strat = int(minority.loc[minority["ed_name"] == "Chestermere-Strathmore",
                                  "population"].iloc[0])

    # If Chestermere-Strathmore already exists in minority plan (52,982),
    # and Chestermere + Strathmore + Wheatland = natural_pair, then the
    # Calgary-Peigan-Chestermere district pulls Chestermere voters it does not need.

    natural_pair_fits = QUOTA_MIN <= natural_pair <= QUOTA_MAX

    verdict = (
        "FAIL (Chestermere split into Calgary is unforced; natural pair with "
        "Strathmore + Wheatland is population-viable)"
        if natural_pair_fits
        else "PASS"
    )
    return {
        "test": "T5_chestermere_split",
        "chestermere_pop": ches_pop,
        "strathmore_pop": strat_pop,
        "wheatland_pop": wheatland_pop,
        "natural_pair_total": natural_pair,
        "calgary_peigan_chestermere_minority_pop": cpc,
        "chestermere_strathmore_minority_pop": ches_strat,
        "natural_pair_within_25pct": natural_pair_fits,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------
def _flatten_for_csv(results: list[dict]) -> pd.DataFrame:
    rows = []
    for r in results:
        test = r["test"]
        for k, v in r.items():
            if k == "test":
                continue
            if isinstance(v, list):
                for idx, row in enumerate(v):
                    if isinstance(row, dict):
                        for kk, vv in row.items():
                            rows.append({"test": test, "key": f"{k}[{idx}].{kk}", "value": vv})
                    else:
                        rows.append({"test": test, "key": f"{k}[{idx}]", "value": row})
            else:
                rows.append({"test": test, "key": k, "value": v})
    return pd.DataFrame(rows)


def run_all() -> list[dict]:
    pop = load_csd_populations()
    majority = load_majority()
    minority = load_minority()
    eds_2019 = load_2019_eds()

    results = [
        test_1_olds_airdrie(pop),
        test_2_rmh_np(pop, eds_2019),
        test_3_airdrie_split(pop),
        test_4_red_deer(pop, majority, minority),
        test_5_chestermere(pop, minority),
    ]
    return results


def main():
    results = run_all()
    for r in results:
        print(r["test"])
        for k, v in r.items():
            if k == "test":
                continue
            if isinstance(v, list):
                print(f"  {k}:")
                for row in v:
                    print(f"    {row}")
            else:
                print(f"  {k}: {v}")
        print()

    df = _flatten_for_csv(results)
    out_csv = DATA / "v0_1_justification_test_inputs.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"Wrote {out_csv} ({len(df)} rows)")


if __name__ == "__main__":
    main()
