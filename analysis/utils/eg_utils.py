"""
eg_utils.py — Wasted-vote efficiency gap (continuous-threshold variant).

This module implements the EG formula used by szat.py and szat_validate.py,
where the winning threshold is total / 2 (continuous). This is appropriate for
VA-level analyses where vote totals are aggregated from fractional assignments.

The integer-majority variant (threshold = total // 2 + 1) used by
chen_rodden_alberta.py, historical_eg_baseline.py, and overlap_zone_diagnostic.py
is intentionally NOT unified here — see REMEDIATION_LOG.md 2026-05-09 for the
reasoning. Those implementations serve different data contexts and are kept local.

Forward dependencies: none
Backward dependencies: szat.py, szat_validate.py
"""
from __future__ import annotations

import logging

import pandas as pd

__all__ = [
    "GeometryError",
    "InsufficientDataError",
    "_ed_waste",
    "compute_eg",
]

logger = logging.getLogger(__name__)


class GeometryError(ValueError):
    """Raised when a spatial geometry operation fails."""


class InsufficientDataError(ValueError):
    """Raised when required columns or data are missing."""


def _ed_waste(ndp: float, ucp: float) -> tuple[float, float]:
    """Return (ndp_wasted, ucp_wasted) for one electoral district.

    Uses continuous threshold = total / 2. Returns (0.0, 0.0) for zero total.
    Ties (ndp == ucp) are treated as NDP wins (ndp >= ucp condition).
    """
    total = ndp + ucp
    if total == 0:
        return 0.0, 0.0
    threshold = total / 2
    if ndp >= ucp:
        return max(0.0, ndp - threshold), ucp
    return ndp, max(0.0, ucp - threshold)


def compute_eg(
    ed_votes: pd.DataFrame,
    ndp_col: str = "ndp",
    ucp_col: str = "ucp",
) -> float:
    """Compute provincial efficiency gap from per-ED vote totals.

    Returns (wasted_NDP - wasted_UCP) / total_provincial in [-1, 1].
    Raises InsufficientDataError if required columns are missing.
    Returns 0.0 if all districts have zero votes.
    """
    missing = [c for c in (ndp_col, ucp_col) if c not in ed_votes.columns]
    if missing:
        raise InsufficientDataError(f"compute_eg: missing columns {missing}")

    total_prov = (ed_votes[ndp_col] + ed_votes[ucp_col]).sum()
    if total_prov == 0:
        return 0.0

    wn = wu = 0.0
    for _, row in ed_votes.iterrows():
        dn, du = _ed_waste(float(row[ndp_col]), float(row[ucp_col]))
        wn += dn
        wu += du
    return (wn - wu) / total_prov
