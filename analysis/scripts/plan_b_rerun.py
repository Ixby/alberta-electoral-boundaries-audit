"""
Plan B re-run of the five justification tests.

Under Plan A (2021 Census, legally compliant with Act s.12(3)), the audit
found all five contested configurations unforced by population math.

Plan B uses the commission's stated working basis -- TBF 2024 mid-year
estimates, refreshed here to 2025 Regional Dashboard values where available.
The provincial quota changes: Plan A (2021 Census total 4,262,635 / 89 EDs
as if the 2026 map had been drawn then) vs. Plan B (commission's own figure
4,888,723 / 89 = 54,929; floor 41,197; ceiling 68,661).

We use the commission's own quota (54,929, floor 41,197, ceiling 68,661)
because that is what the commission and both minority and majority report
tables measure against. Plan B pushes individual municipal components
forward to their 2025 TBF values and checks whether each test still reaches
the same verdict.
"""

# Version: 0.1 series  (last updated 2026-04-26)

import os
import sys

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

import pandas as pd

REPO = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
DATA = os.path.join(REPO, "data")

# Commission's stated quota (from both majority and minority reports)
QUOTA = 54929
FLOOR = 41197  # -25%
CEILING = 68661  # +25%



def run():
    plan_b = pd.read_csv(os.path.join(DATA, "alberta_population_plan_b.csv"))


    def pop_latest(name):
        """Return the latest-available population for a municipality name.

        Prefers TBF regional dashboard (2025) over municipal census figures
        except for Airdrie where we keep both and default to TBF 2025.
        """
        rows = plan_b[plan_b["municipality"] == name]
        if rows.empty:
            raise KeyError(name)
        # Prefer TBF regional dashboard rows
        tbf = rows[rows["pop_latest_source"] == "TBF_regional_dashboard"]
        if not tbf.empty:
            return int(tbf.iloc[0]["pop_latest_value"])
        return int(rows.iloc[0]["pop_latest_value"])


    def fmt(n):
        return f"{n:,}"


    def deviation(pop):
        return (pop - QUOTA) / QUOTA * 100


    results = {}

    # ----- Test 1: Olds-Three Hills-Didsbury rural catchment -----
    rural_members = [
        "Mountain View County",
        "Kneehill County",
        "Olds",
        "Didsbury",
        "Carstairs",
        "Three Hills",
        "Trochu",
        "Cremona",
        "Linden",
        "Acme",
        "Beiseker",
    ]
    total_plan_b = sum(pop_latest(m) for m in rural_members)
    test1_verdict = (
        "FAIL" if total_plan_b >= FLOOR else "PASS (population forces extension)"
    )
    results["Test 1 Olds-3H-Didsbury"] = {
        "plan_b_sum": total_plan_b,
        "floor": FLOOR,
        "deviation_pct": round(deviation(total_plan_b), 2),
        "verdict": test1_verdict,
        "plan_a_sum": 43691,
        "plan_a_verdict": "FAIL",
    }

    print("\n=== Test 1: Olds-Three Hills-Didsbury rural catchment ===")
    for m in rural_members:
        print(f"  {m}: {fmt(pop_latest(m))}")
    print(f"  Plan B sum:          {fmt(total_plan_b)}  ({deviation(total_plan_b):+.2f}%)")
    print(f"  Floor:               {fmt(FLOOR)}")
    print(f"  Plan A (2021) sum:   {fmt(43691)} (Plan A verdict: FAIL)")
    print(f"  Plan B verdict:      {test1_verdict}")

    # ----- Test 2: Rocky Mountain House-Banff Park rural catchment -----
    # Natural catchment: Clearwater + Rocky Mountain House + Caroline
    # (Caroline absent from Plan B; use 2021 value 470 unchanged)
    rmh_members = [
        "Clearwater County",
        "Rocky Mountain House",
        "Sundre",
        "Rimbey",
        "Ponoka County",
    ]
    rmh_sum = sum(pop_latest(m) for m in rmh_members) + 470  # Caroline Village (stale)
    test2_pop_verdict = (
        "Plan B: still below floor; NP extension does not close gap"
        if rmh_sum < FLOOR
        else "Plan B: rural catchment now above floor; NP extension no longer forced"
    )
    results["Test 2 RMH-Banff-Park (population)"] = {
        "plan_b_sum": rmh_sum,
        "floor": FLOOR,
        "deviation_pct": round(deviation(rmh_sum), 2),
        "verdict": test2_pop_verdict,
        "plan_a_sum": 34240,
        "plan_a_verdict": (
            "FAIL on area (2019 ED already >20,000 km²); pop deficit real "
            "either way, so NP extension is not load-bearing"
        ),
    }
    print("\n=== Test 2: Rocky Mountain House-Banff Park rural catchment ===")
    for m in rmh_members:
        print(f"  {m}: {fmt(pop_latest(m))}")
    print(f"  Caroline (2021 stale): 470")
    print(f"  Plan B rural sum:    {fmt(rmh_sum)}  ({deviation(rmh_sum):+.2f}%)")
    print(f"  Floor:               {fmt(FLOOR)}")
    print(f"  Plan A (2021) sum:   {fmt(34240)}")
    print(f"  Plan B pop verdict:  {test2_pop_verdict}")
    print(
        "  Note: the area test (Bill 33 predecessor ED = 24,468 km² > 20,000) "
        "is unchanged by population data; it still FAILs the 'NP extension needed' claim."
    )

    # ----- Test 3: Airdrie split -----
    airdrie_tbf = pop_latest("Airdrie")  # 92,544 (2025)
    airdrie_mun = 85805  # 2024 municipal census
    # 2-way minority split of Airdrie alone:
    two_way_tbf = airdrie_tbf / 2
    two_way_mun = airdrie_mun / 2
    # With rural make-up to reach 41,197 floor:
    rv_topup_tbf = max(0, FLOOR - two_way_tbf)
    rv_topup_mun = max(0, FLOOR - two_way_mun)
    rocky_view = pop_latest("Rocky View County")
    # What a 4-way split would need:
    four_way_tbf = airdrie_tbf / 4
    four_way_mun = airdrie_mun / 4
    rv_topup_4way_tbf = FLOOR - four_way_tbf
    rv_topup_4way_mun = FLOOR - four_way_mun
    results["Test 3 Airdrie 4-way"] = {
        "airdrie_tbf_2025": airdrie_tbf,
        "airdrie_munc_2024": airdrie_mun,
        "2-way_half_tbf": int(two_way_tbf),
        "2-way_half_munc": int(two_way_mun),
        "rv_topup_per_half_tbf": int(rv_topup_tbf),
        "rv_topup_per_half_munc": int(rv_topup_mun),
        "plan_a_verdict": "FAIL (2-way sufficient; 4,147 rural top-up per half)",
        "plan_b_verdict": (
            "FAIL (2-way sufficient under Plan B too; Airdrie now 92.5k so "
            "each half is 46.3k, well above floor with no rural top-up required)"
        ),
    }
    print("\n=== Test 3: Airdrie 4-way split ===")
    print(f"  Airdrie TBF 2025:              {fmt(airdrie_tbf)}")
    print(f"  Airdrie municipal census 2024: {fmt(airdrie_mun)}")
    print(
        f"  2-way split (TBF):             {two_way_tbf:,.0f} per half "
        f"(deviation {deviation(two_way_tbf):+.2f}%)"
    )
    print(
        f"  2-way split (munc):            {two_way_mun:,.0f} per half "
        f"(deviation {deviation(two_way_mun):+.2f}%)"
    )
    print(f"  Rural top-up needed per half (TBF):  {rv_topup_tbf:,.0f}")
    print(f"  Rural top-up needed per half (munc): {rv_topup_mun:,.0f}")
    print(f"  Available from Rocky View County:    {fmt(rocky_view)}")
    print(
        f"  4-way split (TBF) per quarter:       {four_way_tbf:,.0f} (needs {rv_topup_4way_tbf:,.0f} rural each)"
    )
    print(f"  Plan A verdict: FAIL (unforced)")
    print(
        f"  Plan B verdict: FAIL (strongly unforced; under Plan B, each half of a 2-way split is already above floor)"
    )

    # ----- Test 4: Red Deer 4 districts -----
    rd_tbf = pop_latest("Red Deer")  # 115,409 (2025)
    # Minimum districts at ceiling:
    import math

    min_dists_tbf = math.ceil(rd_tbf / CEILING)
    results["Test 4 Red Deer 4-way"] = {
        "red_deer_tbf_2025": rd_tbf,
        "red_deer_2021": 100844,
        "min_districts_tbf": min_dists_tbf,
        "plan_a_min": 2,
        "plan_a_verdict": "FAIL (2 achieved; 4 unforced)",
        "plan_b_verdict": (
            f"{'FAIL' if min_dists_tbf <= 2 else 'PARTIAL — 2-way no longer fits'} "
            f"({min_dists_tbf} district minimum under Plan B)"
        ),
    }
    print("\n=== Test 4: Red Deer 4 districts ===")
    print(f"  Red Deer TBF 2025:  {fmt(rd_tbf)}")
    print(f"  Red Deer 2021:      {fmt(100844)}")
    print(f"  Minimum districts at ceiling ({fmt(CEILING)}): {min_dists_tbf}")
    print(f"  Plan A verdict:     FAIL (2 is minimum; achieved)")
    print(f"  Plan B verdict:     {results['Test 4 Red Deer 4-way']['plan_b_verdict']}")
    if min_dists_tbf == 2:
        half = rd_tbf / 2
        print(
            f"  Note: even at 2025 TBF 115,409, a 2-way split averages {half:,.0f} "
            f"per district — within +/-25% band."
        )

    # ----- Test 5: Chestermere split -----
    chest = pop_latest("Chestermere")  # 31,671
    strath = pop_latest("Strathmore")  # 16,416
    wheatland = pop_latest("Wheatland County")  # 10,150
    natural = chest + strath + wheatland
    results["Test 5 Chestermere split"] = {
        "chestermere_tbf_2025": chest,
        "strathmore_tbf_2025": strath,
        "wheatland_tbf_2025": wheatland,
        "natural_sum": natural,
        "deviation_pct": round(deviation(natural), 2),
        "plan_a_sum": 45240,
        "plan_a_verdict": "FAIL (natural pairing at 45,240 is within band)",
        "plan_b_verdict": (
            "FAIL"
            if FLOOR <= natural <= CEILING
            else "PARTIAL (natural pairing now outside +/-25%)"
        ),
    }
    print("\n=== Test 5: Chestermere split ===")
    print(f"  Chestermere:       {fmt(chest)}")
    print(f"  Strathmore:        {fmt(strath)}")
    print(f"  Wheatland County:  {fmt(wheatland)}")
    print(f"  Natural sum:       {fmt(natural)}  ({deviation(natural):+.2f}%)")
    print(f"  Plan A (2021) sum: {fmt(45240)} (FAIL verdict)")
    print(f"  Plan B verdict:    {results['Test 5 Chestermere split']['plan_b_verdict']}")

    # ----- A1 MAD recompute -----
    # Plan A uses commission's own 2026 tables (already 2024 TBF-derived).
    # Plan B *is* that same data — both reports are already built on TBF 2024.
    # So A1 is unchanged under a Plan B retrofit of 2025 values.
    # We note this in the report; do not rerun A1.

    # ----- A2 Calgary zone gap -----
    # Calgary 2024 Civic Census does not exist (program cancelled 2020, resumes 2027).
    # StatsCan CSD-level Calgary TBF estimate is ~1.6M (2025), but there is NO
    # ward-level or community-level 2024 breakdown available for aggregation to
    # commission EDs. Plan B for A2 is therefore BLOCKED at the sub-CSD level.

    print("\n=== A1 / A2 notes ===")
    print("  A1 MAD is computed directly from the commission's own 2026 ED-level")
    print("  population tables. Those tables ARE the TBF July 2024 estimate, so")
    print("  Plan A and Plan B are literally identical at the ED level. The")
    print("  audit's A1 finding (minority MAD 4,707 vs majority 3,180) is the")
    print("  2024 TBF result under the commission's stated basis.")
    print("")
    print("  A2 BLOCKED under Plan B: Calgary's Civic Census was cancelled in")
    print("  2020 and is not scheduled to resume until 2027. No 2024 or 2025")
    print("  ward-level or community-level Calgary population count exists.")
    print("  Plan B can therefore only reaffirm the Plan A A2 finding; it")
    print("  cannot independently test it with fresher sub-CSD Calgary data.")

    print("\n=== Summary ===")
    for k, v in results.items():
        print(f"\n{k}:")
        for kk, vv in v.items():
            print(f"  {kk}: {vv}")


if __name__ == "__main__":
    run()
