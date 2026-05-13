"""Efficiency-gap baseline for historical Alberta elections (integer-threshold form).

Uses the discrete wasted-vote formulation:

    threshold = (ndp_votes + rbc_votes) // 2 + 1

This is intentionally NOT unified with ``eg_utils.py``, which uses the
continuous threshold (``total / 2``). See ``eg_utils.py`` line 9 for the
documented split. Party abbreviation "RBC" = right-bloc conservative (historical
naming convention used across 2015–2023 Alberta elections).

Backward:
  data/2023_results.xlsx
  data/2015_results.xlsx
Forward:
  findings/historical_eg_baseline.md
"""
from __future__ import annotations

from typing import Any, Dict, List


def compute_eg(districts: List[Dict[str, Any]], label: str) -> Dict[str, Any]:
    """Compute the efficiency gap for a single election cycle.

    Parameters
    ----------
    districts : list of dicts, each with keys:
        - ``ndp``           : NDP vote count (int or float)
        - ``rbc``           : Right-bloc conservative vote count
        - ``actual_winner`` : "NDP" or "RBC"
    label : str — human-readable label for this calculation (not used in math).

    Returns
    -------
    dict with:
        ``code_eg_pct``   : EG × 100, rounded to 4 decimal places.
                            Positive → NDP structural disadvantage.
        ``ndp_wins``      : seats won by NDP (from ``actual_winner`` labels)
        ``rbc_wins``      : seats won by RBC

    Raises
    ------
    ValueError : if ``districts`` is empty.
    """
    if not districts:
        raise ValueError(f"compute_eg({label!r}): district list is empty")

    ndp_wasted_total = 0
    rbc_wasted_total = 0
    total_2p = 0
    ndp_wins = 0
    rbc_wins = 0

    for d in districts:
        ndp = d["ndp"]
        rbc = d["rbc"]
        winner = d["actual_winner"]
        total = ndp + rbc
        threshold = total // 2 + 1

        if winner == "NDP":
            ndp_wasted = ndp - threshold
            rbc_wasted = rbc
            ndp_wins += 1
        else:
            rbc_wasted = rbc - threshold
            ndp_wasted = ndp
            rbc_wins += 1

        ndp_wasted_total += ndp_wasted
        rbc_wasted_total += rbc_wasted
        total_2p += total

    code_eg = (ndp_wasted_total - rbc_wasted_total) / total_2p
    return {
        "code_eg_pct": round(code_eg * 100, 4),
        "ndp_wins": ndp_wins,
        "rbc_wins": rbc_wins,
    }
