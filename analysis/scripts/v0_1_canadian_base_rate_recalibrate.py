"""
Canadian inter-map EG asymmetry base rate — T3.3 recalibration (2026-04-23).

Purpose.
  The original n=7 distribution in v0_1_canadian_base_rate_computed.md
  INCLUDES Alberta 2025-26 as both the anchor case and a member of the
  comparator distribution used to rank it. That is circular. Gemini's
  red-team Phase E.2 flagged this. This script recomputes the
  positioning without the circularity.

Two approaches:
  A. Exclude Alberta 2025-26 from the distribution; report the
     percentile of Alberta 2025-26's 0.51 pp against the n=6 sample
     of OTHER Canadian cycles.
  B. Ordinal ranking among non-zero-asymmetry cycles only.

Also reports the compression factor re-calibration question: the
0.455 deflator was fit to Alberta 2025-26 alone, so the EG-proxy
values are themselves partially co-calibrated with the anchor. We
report both the EG-proxy distribution (carrying the 0.455 factor) and
the raw seat-share-asymmetry distribution (which is closed-form exact
and factor-free).

forward_dependencies:
  - analysis/methodology/v0_1_canadian_base_rate_computed.md (receives a new "Recalibration" section)
  - report_academic.md §5.2.1 (the paper-facing paragraph is updated)
backward_dependencies:
  - analysis/scripts/v0_1_canadian_base_rate_compute.py (original n=7 writeup)
  - data/v0_1_canadian_redistribution_base_rate.csv (source data)
"""
from __future__ import annotations

import csv
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV_PATH = os.path.join(REPO_ROOT, "data", "v0_1_canadian_redistribution_base_rate.csv")


# The seven comparable cycles as reconstructed from
# v0_1_canadian_base_rate_computed.md §3.1. Seat-share asymmetry is the
# closed-form exact inter-map EG delta under constant-votes (no 0.455
# multiplier). EG-proxy values apply the 0.455 factor; Alberta 2025-26's
# EG-proxy is the audit's measured 0.51 pp by construction.
CYCLES = [
    # (name, seats, delta_s, eg_proxy_pp, seat_share_asym_pp)
    ("Alberta 2025-26",             89, 1, 0.51, 1.12),  # anchor, audit-measured
    ("Federal 2022 (AB)",           37, 0, 0.00, 0.00),
    ("British Columbia 2023",       93, 0, 0.00, 0.00),
    ("Saskatchewan 2022",           61, 0, 0.00, 0.00),
    ("Alberta 2017",                87, 1, 0.52, 1.15),
    ("Alberta 2010",                87, 0, 0.00, 0.00),
    ("Manitoba 2018",               57, 1, 0.80, 1.75),
]
ANCHOR_NAME = "Alberta 2025-26"
ANCHOR_EG = 0.51
ANCHOR_EG_HIGH = 1.60
ANCHOR_SEAT_SHARE = 1.12


def percentile_rank(value: float, sample: list[float], kind: str = "weak") -> float:
    """
    Percentile rank of `value` against `sample`.

    kind="weak":   percentage of sample points <= value.
    kind="strict": percentage of sample points < value.
    kind="mean":   mean of weak and strict (scipy's 'mean' convention).
    """
    n = len(sample)
    if n == 0:
        return float("nan")
    below = sum(1 for v in sample if v < value)
    at_or_below = sum(1 for v in sample if v <= value)
    if kind == "weak":
        return 100.0 * at_or_below / n
    if kind == "strict":
        return 100.0 * below / n
    if kind == "mean":
        return 100.0 * (below + at_or_below) / (2 * n)
    raise ValueError(kind)


def summarise(label: str, sample: list[float]) -> None:
    if not sample:
        print(f"  (empty sample for {label})")
        return
    print(f"  n        = {len(sample)}")
    print(f"  mean     = {statistics.mean(sample):.3f} pp")
    print(f"  median   = {statistics.median(sample):.3f} pp")
    print(f"  min      = {min(sample):.3f} pp")
    print(f"  max      = {max(sample):.3f} pp")
    if len(sample) > 1:
        print(f"  pstdev   = {statistics.pstdev(sample):.3f} pp")


def main() -> None:
    print("=" * 72)
    print("T3.3 Canadian comparator base-rate recalibration (2026-04-23)")
    print("=" * 72)
    print()
    print("Original claim (v0_1_canadian_base_rate_computed.md §5.1):")
    print(f"  Alberta 2025-26 at p71 of n=7 distribution (INCLUDES anchor).")
    print(f"  Circularity: anchor is in the distribution used to rank it,")
    print(f"  and the 0.455 compression factor is fit to the anchor.")
    print()

    # ----------------------------------------------------------------
    # Approach A: exclude Alberta 2025-26 from the distribution
    # ----------------------------------------------------------------
    print("-" * 72)
    print("APPROACH A — exclude Alberta 2025-26 from the comparator distribution")
    print("-" * 72)

    comparator_eg = [eg for (n, _s, _ds, eg, _ssa) in CYCLES if n != ANCHOR_NAME]
    comparator_ss = [ssa for (n, _s, _ds, _eg, ssa) in CYCLES if n != ANCHOR_NAME]

    print()
    print("Comparator distribution (EG-proxy pp, n=6, Alberta 2025-26 excluded):")
    summarise("EG-proxy", comparator_eg)
    print()
    print(f"  Sorted: {sorted(comparator_eg)}")
    print()
    print("Comparator distribution (seat-share asymmetry pp, n=6, factor-free):")
    summarise("seat-share", comparator_ss)
    print()
    print(f"  Sorted: {sorted(comparator_ss)}")
    print()

    # Rank Alberta against comparator
    for kind in ("weak", "strict", "mean"):
        p_eg_low = percentile_rank(ANCHOR_EG, comparator_eg, kind=kind)
        p_eg_high = percentile_rank(ANCHOR_EG_HIGH, comparator_eg, kind=kind)
        p_ss = percentile_rank(ANCHOR_SEAT_SHARE, comparator_ss, kind=kind)
        print(f"  {kind:>6} percentile of Alberta 0.51 pp (EG) vs n=6 comparator: {p_eg_low:5.1f}%")
        print(f"  {kind:>6} percentile of Alberta 1.60 pp (EG high) vs n=6 comparator: {p_eg_high:5.1f}%")
        print(f"  {kind:>6} percentile of Alberta 1.12 pp (seat-share) vs n=6 comparator: {p_ss:5.1f}%")
        print()

    # Count cycles at/above Alberta in comparator
    at_or_above_eg = sum(1 for v in comparator_eg if v >= ANCHOR_EG)
    below_eg = sum(1 for v in comparator_eg if v < ANCHOR_EG)
    print(f"  Of the n=6 comparator cycles:")
    print(f"    {below_eg} fall strictly below Alberta 2025-26's 0.51 pp "
          f"(all four zero-asymmetry cycles).")
    print(f"    {at_or_above_eg} fall at or above (Alberta 2017 at 0.52 pp, Manitoba 2018 at 0.80 pp).")
    print(f"    Alberta 2025-26's 0.51 pp is the SECOND-LOWEST non-zero value in the original n=7;")
    print(f"    excluded, it becomes a new observation between 0.00 and 0.52.")
    print()

    # ----------------------------------------------------------------
    # Approach B: ordinal ranking among non-zero cycles
    # ----------------------------------------------------------------
    print("-" * 72)
    print("APPROACH B — ordinal ranking among non-zero-asymmetry cycles")
    print("-" * 72)
    print()

    nonzero = [(n, eg) for (n, _s, _ds, eg, _ssa) in CYCLES if eg > 0]
    nonzero.sort(key=lambda x: x[1])
    print("Non-zero-asymmetry cycles in the n=7 sample (low to high):")
    for i, (n, eg) in enumerate(nonzero, 1):
        marker = "  <-- anchor" if n == ANCHOR_NAME else ""
        print(f"  {i}. {n:<30}  EG-proxy = {eg:.2f} pp{marker}")
    print()
    nonzero_excl = [(n, eg) for (n, eg) in nonzero if n != ANCHOR_NAME]
    print("Excluding the anchor, ordinal position of Alberta 2025-26 (0.51 pp) among other non-zero:")
    others = [(n, eg) for (n, eg) in nonzero_excl]
    others_sorted = sorted(others, key=lambda x: x[1])
    print(f"  Other non-zero cycles: {[(n, eg) for (n, eg) in others_sorted]}")
    below_anchor = [n for (n, eg) in others if eg < ANCHOR_EG]
    above_anchor = [n for (n, eg) in others if eg > ANCHOR_EG]
    print(f"  Strictly below 0.51 pp: {below_anchor}")
    print(f"  Strictly above 0.51 pp: {above_anchor}")
    print()
    print("  Framing: 'Alberta 2025-26 (0.51 pp) falls between Alberta 2017 (0.52 pp)")
    print("  and the zero cluster; Manitoba 2018 (0.80 pp) remains the Canadian maximum.'")
    print()

    # ----------------------------------------------------------------
    # Sanity check: reproduce the original n=7 p71 claim
    # ----------------------------------------------------------------
    print("-" * 72)
    print("SANITY CHECK — reproduce the original n=7 'p71' claim")
    print("-" * 72)
    print()
    full_eg = [eg for (_n, _s, _ds, eg, _ssa) in CYCLES]
    p_full = percentile_rank(ANCHOR_EG, full_eg, kind="weak")
    print(f"  Weak percentile of 0.51 against full n=7 including anchor: {p_full:.1f}%")
    print(f"  (5 of 7 cycles fall at or below 0.51 -> 5/7 = 71.4%; matches the writeup.)")
    print()


if __name__ == "__main__":
    main()
