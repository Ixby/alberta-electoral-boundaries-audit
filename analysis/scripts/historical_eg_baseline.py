"""Efficiency-gap baseline for historical Alberta elections (integer-threshold form).

Uses the discrete wasted-vote formulation:

    threshold = (opposition_votes + incumbent_votes) // 2 + 1

This is intentionally NOT unified with ``eg_utils.py``, which uses the
continuous threshold (``total / 2``). See ``eg_utils.py`` line 9 for the
documented split.

Input dicts use generic role keys (``"opposition"`` / ``"incumbent"``) so
this function is not tied to any specific Alberta party abbreviation. The
``opp_label`` parameter names which ``actual_winner`` value means the
opposition won; it defaults to the ``parties.opposition`` entry in
``config.yaml`` ("NDP" for the Alberta 2026 audit).

Backward:
  # REVIEW: pure function — no file I/O; inputs passed by caller
Forward:
  # REVIEW: pure function — no file I/O; outputs returned to caller
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))
from data_loader import get_party_labels


def compute_eg(
    districts: List[Dict[str, Any]],
    label: str,
    opp_label: Optional[str] = None,
) -> Dict[str, Any]:
    """Compute the efficiency gap for a single election cycle.

    Parameters
    ----------
    districts : list of dicts, each with keys:
        - ``opposition``    : opposition-party vote count (int or float)
        - ``incumbent``     : incumbent-party vote count
        - ``actual_winner`` : string matching ``opp_label`` when the
                              opposition won, anything else when the
                              incumbent won
    label : str — human-readable label for this calculation (not used in math).
    opp_label : str, optional — the ``actual_winner`` string that indicates an
        opposition win. Defaults to ``parties.opposition`` from ``config.yaml``
        (``"NDP"`` for the Alberta 2026 audit). Pass explicitly in tests that
        do not use the repo config.

    Returns
    -------
    dict with:
        ``code_eg_pct``        : EG × 100, rounded to 4 decimal places.
                                 Positive → opposition structural disadvantage.
        ``opposition_wins``    : seats won by the opposition party.
        ``incumbent_wins``     : seats won by the incumbent party.

    Raises
    ------
    ValueError : if ``districts`` is empty.
    """
    if not districts:
        raise ValueError(f"compute_eg({label!r}): district list is empty")

    if opp_label is None:
        opp_label = get_party_labels()["opposition"]

    opp_wasted_total = 0
    inc_wasted_total = 0
    total_2p = 0
    opposition_wins = 0
    incumbent_wins = 0

    for d in districts:
        opp = d["opposition"]
        inc = d["incumbent"]
        winner = d["actual_winner"]
        total = opp + inc
        threshold = total // 2 + 1

        if winner == opp_label:
            opp_wasted = opp - threshold
            inc_wasted = inc
            opposition_wins += 1
        else:
            inc_wasted = inc - threshold
            opp_wasted = opp
            incumbent_wins += 1

        opp_wasted_total += opp_wasted
        inc_wasted_total += inc_wasted
        total_2p += total

    code_eg = (opp_wasted_total - inc_wasted_total) / total_2p
    return {
        "code_eg_pct": round(code_eg * 100, 4),
        "opposition_wins": opposition_wins,
        "incumbent_wins": incumbent_wins,
    }
