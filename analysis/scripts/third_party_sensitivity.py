"""
third_party_sensitivity.py

D1 fix: Third-party vote sensitivity analysis.

Alberta 2023 had 58,232 votes for non-NDP/non-UCP candidates (3.3% of valid
two-party votes). The main analysis drops these. This script runs three
allocation rules to test whether the partisan asymmetry finding holds:

  Rule A (drop):     current behavior — two-party only
  Rule B (pro_rate): allocate other × ndp/(ndp+ucp) to NDP, remainder to UCP
  Rule C (trailing): allocate all other votes to the trailing party per ED

If minority EG < majority EG (more UCP-favoured) under all three rules, D1 is
closed. Results saved to data/outputs/third_party_sensitivity_results.csv.

Dependencies:
  Forward:  (consumed by report/D1 analysis)
  Backward: analysis/scripts/packing_cracking_analysis.py, analysis/utils/eg_utils.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from packing_cracking_analysis import (
    MAJORITY_2026_MAPPING,
    MINORITY_2026_MAPPING,
    estimate_2026,
    compute_metrics,
    _find_data,
)
from eg_utils import InsufficientDataError

OUTPUT_CSV = ROOT / "data" / "outputs" / "third_party_sensitivity_results.csv"

RULES = [
    ("drop",     "A — Drop (current)"),
    ("pro_rate", "B — Pro-rate"),
    ("trailing", "C — Trailing party"),
]


def load_with_other() -> list[dict]:
    """Load ED-level 2023 results, capturing other/third-party votes separately."""
    out = []
    with open(_find_data("alberta_2023_results.csv")) as f:
        for r in csv.DictReader(f):
            ndp = ucp = other = 0
            for i in range(1, 7):
                cand = r.get(f"cand_{i}", "") or ""
                votes_str = r.get(f"votes_{i}", "") or ""
                if not cand or not votes_str:
                    continue
                try:
                    votes = int(votes_str)
                except ValueError:
                    continue
                cu = cand.strip().upper()
                if "INDEPENDENT" in cu:
                    other += votes
                    continue
                is_ndp = re.search(
                    r"(\(NDP\)$|\bNDP$|ALBERTA NDP|NEW DEMOCRATIC PARTY)", cu
                )
                is_ucp = re.search(
                    r"(\(UCP\)$|\bUCP$|UNITED CONSERVATIVE PARTY)", cu
                )
                if is_ndp:
                    ndp = votes
                elif is_ucp:
                    ucp = votes
                else:
                    other += votes
            if not (ndp + ucp > 0):
                raise InsufficientDataError(
                    f"Failed to parse votes for ED: {r['ed_name']}. NDP={ndp}, UCP={ucp}"
                )
            out.append({
                "ed": r["ed_name"],
                "region": r["region"],
                "ndp": ndp,
                "ucp": ucp,
                "other": other,
            })
    return out


def apply_rule(dists: list[dict], rule: str) -> list[dict]:
    """Return ED list with ndp/ucp adjusted per allocation rule. Drops 'other'."""
    out = []
    for d in dists:
        ndp, ucp, other = d["ndp"], d["ucp"], d["other"]
        if rule == "drop":
            pass
        elif rule == "pro_rate":
            total = ndp + ucp
            ndp = round(ndp + other * ndp / total)
            ucp = round(ucp + other * ucp / total)
        elif rule == "trailing":
            if ndp <= ucp:
                ndp += other
            else:
                ucp += other
        out.append({"ed": d["ed"], "region": d["region"], "ndp": ndp, "ucp": ucp})
    return out


def _validate(estimates: list[dict], label: str) -> tuple[bool, str]:
    n = len(estimates)
    total = sum(d["ndp"] + d["ucp"] for d in estimates)
    total_ndp = sum(d["ndp"] for d in estimates)
    # Allow 1.86M upper bound to accommodate other-vote absorption (+3.3%)
    if n != 89:
        return False, f"FAIL: {label} has {n} EDs, expected 89"
    if not (1_500_000 <= total <= 1_860_000):
        return False, f"FAIL: {label} total {total:,} outside plausible range"
    ndp_share = total_ndp / total if total else 0
    if not (0.38 <= ndp_share <= 0.55):
        return False, f"FAIL: {label} NDP share {ndp_share:.3f} out of range"
    return True, "PASS"


def main() -> None:
    print("=" * 72)
    print("  D1: Third-Party Vote Sensitivity Analysis")
    print("  Rules: (A) Drop  (B) Pro-rate  (C) Trailing-party")
    print("=" * 72)

    raw = load_with_other()
    total_other = sum(d["other"] for d in raw)
    total_2p = sum(d["ndp"] + d["ucp"] for d in raw)
    print(f"\nOther/third-party votes: {total_other:,}  "
          f"({total_other / (total_2p + total_other) * 100:.2f}% of valid)")
    print(f"EDs with third-party: {sum(1 for d in raw if d['other'] > 0)}/87")

    results: dict[str, dict] = {}

    for rule_id, rule_label in RULES:
        dists = apply_rule(raw, rule_id)

        rural = [d for d in dists if d["region"] == "Rest of Alberta"]
        rural_ndp = (
            sum(d["ndp"] for d in rural)
            / sum(d["ndp"] + d["ucp"] for d in rural)
        )

        m_2019 = compute_metrics(dists, f"2019 [{rule_id}]", verbose=False)

        maj = estimate_2026(dists, MAJORITY_2026_MAPPING, rural_ndp)
        ok, msg = _validate(maj, f"Majority [{rule_id}]")
        if not ok:
            print(f"  Gate FAIL [{rule_id}] majority: {msg}")
            continue
        m_maj = compute_metrics(maj, f"Majority [{rule_id}]", verbose=False)

        minr = estimate_2026(dists, MINORITY_2026_MAPPING, rural_ndp)
        ok, msg = _validate(minr, f"Minority [{rule_id}]")
        if not ok:
            print(f"  Gate FAIL [{rule_id}] minority: {msg}")
            continue
        m_min = compute_metrics(minr, f"Minority [{rule_id}]", verbose=False)

        results[rule_id] = {
            "label": rule_label,
            "2019": m_2019,
            "majority": m_maj,
            "minority": m_min,
            "rural_ndp": rural_ndp,
        }

    if not results:
        print("ERROR: no rules produced valid estimates.")
        sys.exit(1)

    # Results table
    print("\n" + "=" * 72)
    print("  RESULTS TABLE — B2 (EG), B3 (mean-median), B4 (seats@50/50), B6 (decl.)")
    print("=" * 72)
    hdr = f"  {'Rule':<26} | {'Map':<10} | {'EG%':>7} | {'MM pp':>7} | {'@50/50':>6} | {'Decl.':>7}"
    sep = f"  {'-'*26}-+-{'-'*10}-+-{'-'*7}-+-{'-'*7}-+-{'-'*6}-+-{'-'*7}"
    print(hdr)
    print(sep)
    for rule_id, rule_label in RULES:
        if rule_id not in results:
            continue
        r = results[rule_id]
        first = True
        for map_key, map_label in [("2019", "2019"), ("majority", "Majority"), ("minority", "Minority")]:
            m = r[map_key]
            lbl = rule_label if first else ""
            first = False
            print(
                f"  {lbl:<26} | {map_label:<10} | {m['eg'] * 100:+7.3f} | "
                f"{m['mm_gap'] * 100:+7.3f} | {m['ndp_at_50']:>6d} | "
                f"{m['declination']:+7.4f}"
            )
        print(sep)

    # Direction check
    print("\n" + "=" * 72)
    print("  D1 DIRECTION CHECK: minority EG < majority EG (more UCP-favoured)?")
    print("=" * 72)
    all_consistent = True
    for rule_id, rule_label in RULES:
        if rule_id not in results:
            all_consistent = False
            continue
        r = results[rule_id]
        delta = r["minority"]["eg"] - r["majority"]["eg"]
        consistent = delta < 0
        if not consistent:
            all_consistent = False
        status = "CONSISTENT" if consistent else "*** FLIPPED ***"
        print(f"  {rule_label}: minority - majority EG = {delta * 100:+.4f} pp  [{status}]")

    verdict = (
        "CLOSED — asymmetry direction holds across all three rules."
        if all_consistent
        else "OPEN  — direction reverses under at least one rule."
    )
    print(f"\n  D1 VERDICT: {verdict}")

    # Save CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "rule", "map",
        "eg_pct", "mm_gap_pp", "ndp_at_50", "ucp_at_50", "declination",
        "rural_ndp_pct", "ndp_seats", "ucp_seats",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for rule_id, rule_label in RULES:
            if rule_id not in results:
                continue
            r = results[rule_id]
            for map_key in ["2019", "majority", "minority"]:
                m = r[map_key]
                w.writerow({
                    "rule":         rule_label,
                    "map":          map_key,
                    "eg_pct":       round(m["eg"] * 100, 4),
                    "mm_gap_pp":    round(m["mm_gap"] * 100, 4),
                    "ndp_at_50":    m["ndp_at_50"],
                    "ucp_at_50":    m["ucp_at_50"],
                    "declination":  round(m["declination"], 6),
                    "rural_ndp_pct": round(r["rural_ndp"] * 100, 4),
                    "ndp_seats":    m["ndp_seats"],
                    "ucp_seats":    m["ucp_seats"],
                })
    print(f"\n  Output: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
