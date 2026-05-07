"""
s15_ratio_test.py — EBCA §15 population deviation compliance test

Computes deviation from the provincial quota for every ED in both maps,
then classifies each ED against the §15(1) normal band and §15(2) exception.

Outputs: analysis/reports/s15_deviation_compliance.csv

§15(1) normal band: ±25% of provincial quota
§15(2) floor:       −50% (absolute statutory minimum even with exception)
§15(2) trigger:     >25% under quota; requires ≥3 of 5 criteria

§15(2) invocations registered here are from s15_2_reaudit.md (2026-04-23),
with criterion counts corrected against the King's Printer RSA 2000 c. E-3
consolidation 2024-12-05:
  criterion (a): area >20,000 km² OR surveyed area >15,000 km²
  criterion (b): >150 km from Legislature Building by most direct highway route
  criterion (c): no town in the ED with population exceeding 8,000
  criterion (d): contains an Indian reserve or a Metis settlement
  criterion (e): coterminous with a boundary of the Province of Alberta

Classifications written to the output:
  COMPLIANT        — within ±25%
  S15_JUSTIFIED    — outside ±25% (undercount only), §15(2) invoked with ≥3/5
                     criteria, deviation above the −50% floor
  S15_FLOOR_BREACH — §15(2) invoked but deviation exceeds −50% statutory floor
  VIOLATION_OVER   — deviation > +25%; no §15(2) justification for overcounts
  VIOLATION_UNDER  — deviation < −25%; no registered §15(2) invocation
  S15_IN_BAND      — deviation within ±25% but §15(2) invoked (notable: not
                     required but also not unlawful)
"""

import csv
import os

INPUT_CSV = os.path.join(
    os.path.dirname(__file__), "..", "reports", "population_consistency.csv"
)
OUTPUT_CSV = os.path.join(
    os.path.dirname(__file__), "..", "reports", "s15_deviation_compliance.csv"
)

# §15(2) invocations as registered. Source: s15_2_reaudit.md §4.
# Keys are (map, ed_name) tuples matching the ed_name column in the input CSV.
# Values: (criteria_met_of_5, verdicted_by_reaudit)
S15_INVOCATIONS: dict[tuple[str, str], dict] = {
    ("majority_2026", "Central Peace-Notley"): {
        "criteria_met": 5,
        "verdict": "Pass",
        "notes": "5/5; all criteria met per commission report p. 236",
    },
    ("majority_2026", "Lesser Slave Lake"): {
        "criteria_met": 4,
        "verdict": "Pass",
        "notes": "4/5; (e) fails, commission p. 248 confirms four criteria",
    },
    ("majority_2026", "Canmore-Banff"): {
        "criteria_met": 3,
        "verdict": "Pass",
        "notes": (
            "3/5; (a) likely fails, (c) fails (Canmore 15,990; Banff 8,305), "
            "(b)+(d)+(e) pass; minimum statutory threshold"
        ),
    },
    ("minority_2026", "Central Peace-Notley"): {
        "criteria_met": 5,
        "verdict": "Pass",
        "notes": "5/5; boundaries essentially identical to majority",
    },
    ("minority_2026", "Lesser Slave Lake"): {
        "criteria_met": 4,
        "verdict": "Pass",
        "notes": "4/5; (e) fails; same as majority",
    },
    ("minority_2026", "Rocky Mountain House-Banff Park"): {
        "criteria_met": 5,
        "verdict": "Pass",
        "notes": (
            "5/5; (a) Clearwater County 18,692 km² + extensions; "
            "(b) Rocky Mountain House 215 km from Legislature; "
            "(c) largest town 6,765 (Rocky Mountain House); "
            "(d) five reserves named at commission p. 352; "
            "(e) NP extension reaches BC border. "
            "Passes 4/5 even without NP extension."
        ),
    },
}

# EBCA §15(2) allows a maximum of 4 EDs to invoke the exception per map.
MAX_S15_INVOCATIONS_PER_MAP = 4

# Normal band limits (§15(1))
UPPER_BAND = 0.25   # +25%
LOWER_BAND = -0.25  # −25%

# Absolute floor (§15(2))
S15_FLOOR = -0.50   # −50%


def load_populations(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_quota(rows: list[dict], map_id: str) -> float:
    pops = [
        float(r["commission_pop"])
        for r in rows
        if r["map"] == map_id and r.get("commission_pop", "").strip()
    ]
    if len(pops) != 89:
        raise ValueError(
            f"Map '{map_id}' has {len(pops)} EDs with valid commission_pop; expected 89. "
            "Check input CSV for missing or duplicate rows."
        )
    return sum(pops) / 89


def classify(deviation: float, invocation: dict | None) -> str:
    if invocation is not None and deviation <= LOWER_BAND:
        if deviation < S15_FLOOR:
            return "S15_FLOOR_BREACH"
        return "S15_JUSTIFIED"
    if invocation is not None and deviation > LOWER_BAND:
        return "S15_IN_BAND"
    if deviation > UPPER_BAND:
        return "VIOLATION_OVER"
    if deviation < LOWER_BAND:
        return "VIOLATION_UNDER"
    return "COMPLIANT"


def run() -> None:
    rows = load_populations(INPUT_CSV)

    # Statutory test applies to 2026 maps only; 2019 has 87 EDs and a
    # different quota structure — excluded from this compliance run.
    map_ids = [m for m in sorted({r["map"] for r in rows}) if m.endswith("_2026")]
    results = []

    for map_id in map_ids:
        quota = compute_quota(rows, map_id)
        map_rows = [r for r in rows if r["map"] == map_id]

        invocation_count = sum(
            1 for key in S15_INVOCATIONS if key[0] == map_id
        )
        if invocation_count > MAX_S15_INVOCATIONS_PER_MAP:
            raise ValueError(
                f"Map '{map_id}' has {invocation_count} §15(2) invocations "
                f"registered; §15(2) permits at most {MAX_S15_INVOCATIONS_PER_MAP}."
            )

        for row in map_rows:
            commission_pop = float(row["commission_pop"])
            deviation = (commission_pop - quota) / quota
            key = (map_id, row["ed_name"])
            invocation = S15_INVOCATIONS.get(key)
            status = classify(deviation, invocation)

            results.append({
                "map": map_id,
                "ed_name": row["ed_name"],
                "commission_pop": int(commission_pop),
                "provincial_quota": round(quota, 1),
                "deviation_pct": round(deviation * 100, 2),
                "lower_band_pct": round(LOWER_BAND * 100, 1),
                "upper_band_pct": round(UPPER_BAND * 100, 1),
                "s15_invoked": "Y" if invocation else "N",
                "s15_criteria_met": invocation["criteria_met"] if invocation else "",
                "s15_verdict": invocation["verdict"] if invocation else "",
                "classification": status,
                "flag": "FLAG" if status not in ("COMPLIANT", "S15_JUSTIFIED", "S15_IN_BAND") else "",
                "notes": invocation["notes"] if invocation else "",
            })

    fieldnames = [
        "map", "ed_name", "commission_pop", "provincial_quota",
        "deviation_pct", "lower_band_pct", "upper_band_pct",
        "s15_invoked", "s15_criteria_met", "s15_verdict",
        "classification", "flag", "notes",
    ]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Summary to stdout
    from collections import Counter
    counts = Counter(r["classification"] for r in results)
    flags = [r for r in results if r["flag"] == "FLAG"]

    print(f"Output: {OUTPUT_CSV}")
    print(f"\nClassification counts across {len(results)} ED-map rows:")
    for cls, n in sorted(counts.items()):
        print(f"  {cls:<20} {n}")

    print(f"\n{'Flagged EDs' if flags else 'No flagged EDs'}:")
    for r in flags:
        print(
            f"  [{r['map']}] {r['ed_name']:50s} "
            f"{r['deviation_pct']:+.1f}%  {r['classification']}"
        )

    # Verify §15(2) invocations are within 4-per-map cap and below the floor
    for map_id in map_ids:
        in_band_invocations = [
            r for r in results
            if r["map"] == map_id and r["s15_invoked"] == "Y"
            and r["classification"] == "S15_IN_BAND"
        ]
        if in_band_invocations:
            print(f"\nNotable — §15(2) invoked within normal band ({map_id}):")
            for r in in_band_invocations:
                print(f"  {r['ed_name']:50s} {r['deviation_pct']:+.1f}%")


if __name__ == "__main__":
    run()
