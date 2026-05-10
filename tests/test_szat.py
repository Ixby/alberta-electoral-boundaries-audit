"""Tests for szat.py — Swing-Zone Allocation Test core functions.

The SZAT result (p = 0.0024) is one of the three primary statistical findings
in the audit. These tests verify the wasted-vote math and EG composition logic
against hand-computed reference cases.

All functions tested here are pure (no shapefile dependency) so tests are fast.

Run from the repo root:
    python -m pytest tests/test_szat.py -v
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from analysis.utils.eg_utils import _ed_waste, compute_eg
from szat import va_eg_contribution


# ============================================================
# _ed_waste — per-district wasted vote allocation
# Sign convention: continuous threshold = total / 2
# ============================================================


def test_ed_waste_ndp_wins():
    """NDP wins: wastes only surplus above threshold; UCP wastes all votes."""
    w_ndp, w_ucp = _ed_waste(ndp=70.0, ucp=30.0)
    # threshold = 100/2 = 50; NDP surplus = 70-50 = 20
    assert w_ndp == pytest.approx(20.0)
    assert w_ucp == pytest.approx(30.0)


def test_ed_waste_ucp_wins():
    """UCP wins: wastes only surplus; NDP wastes all."""
    w_ndp, w_ucp = _ed_waste(ndp=30.0, ucp=70.0)
    assert w_ndp == pytest.approx(30.0)
    assert w_ucp == pytest.approx(20.0)


def test_ed_waste_exact_tie_ndp_declared_winner():
    """Tie (ndp == ucp): >= comparison awards NDP the win.
    NDP wastes 0 surplus votes; UCP wastes all."""
    w_ndp, w_ucp = _ed_waste(ndp=50.0, ucp=50.0)
    assert w_ndp == pytest.approx(0.0)  # max(0, 50-50) = 0
    assert w_ucp == pytest.approx(50.0)


def test_ed_waste_zero_votes():
    """Zero turnout district: both wasted totals are 0."""
    w_ndp, w_ucp = _ed_waste(ndp=0.0, ucp=0.0)
    assert w_ndp == 0.0
    assert w_ucp == 0.0


def test_ed_waste_landslide_ndp():
    """NDP landslide: large surplus; UCP fully wasted."""
    w_ndp, w_ucp = _ed_waste(ndp=90.0, ucp=10.0)
    assert w_ndp == pytest.approx(40.0)  # 90 - 50
    assert w_ucp == pytest.approx(10.0)


# ============================================================
# compute_eg — map-level efficiency gap
# Uses continuous threshold (total / 2), not integer
# ============================================================


def _df(*rows):
    """Build a minimal vote DataFrame: [(ndp, ucp), ...]"""
    return pd.DataFrame(
        [{"ed_name": f"ED{i}", "ndp": float(r[0]), "ucp": float(r[1])}
         for i, r in enumerate(rows)]
    )


def test_compute_eg_symmetric_two_district():
    """Symmetric map (mirror-image results): EG = 0."""
    # ED0: NDP 60, UCP 40 (NDP wins, threshold=50): wasted_ndp=10, wasted_ucp=40
    # ED1: NDP 40, UCP 60 (UCP wins, threshold=50): wasted_ndp=40, wasted_ucp=10
    # EG = (10+40 - 40+10) / 200 = 0
    df = _df((60, 40), (40, 60))
    assert compute_eg(df) == pytest.approx(0.0)


def test_compute_eg_packed_ndp_positive():
    """Classic packing: NDP packed into safe seat, UCP wins two narrow.
    EG positive = NDP structural disadvantage."""
    # ED0: NDP 80, UCP 20 (NDP wins, threshold=50): wasted_ndp=30, wasted_ucp=20
    # ED1: NDP 45, UCP 55 (UCP wins, threshold=50): wasted_ndp=45, wasted_ucp=5
    # ED2: NDP 45, UCP 55: wasted_ndp=45, wasted_ucp=5
    # EG = (30+45+45 - 20+5+5) / 300 = (120-30)/300 = 0.3
    df = _df((80, 20), (45, 55), (45, 55))
    assert compute_eg(df) == pytest.approx(0.3)


def test_compute_eg_packed_ucp_negative():
    """Reversed packing: UCP packed into safe seat, NDP wins two narrow.
    EG negative = UCP structural disadvantage."""
    df = _df((55, 45), (55, 45), (20, 80))
    assert compute_eg(df) < 0


def test_compute_eg_all_ndp_wins():
    """All EDs won by NDP with same margin — all UCP votes wasted."""
    df = _df((60, 40), (60, 40), (60, 40))
    # Each ED: threshold=50, wasted_ndp=10, wasted_ucp=40
    # EG = (30 - 120) / 300 = -90/300 = -0.3
    assert compute_eg(df) == pytest.approx(-0.3)


def test_compute_eg_zero_total_returns_zero():
    """All-zero votes: EG = 0 (guard against divide-by-zero)."""
    df = _df((0, 0), (0, 0))
    assert compute_eg(df) == pytest.approx(0.0)


# ============================================================
# va_eg_contribution — per-VA proportional EG attribution
# ============================================================


def test_va_contribution_zero_provincial_total():
    """total_prov = 0 → contribution = 0 (guard against divide-by-zero)."""
    assert va_eg_contribution(50, 50, 100, 100, 0) == 0.0


def test_va_contribution_ndp_wins_ed():
    """NDP wins the ED; VA contributes proportionally to NDP surplus waste.

    ed_ndp=70, ed_ucp=30, total=100, threshold=50, surplus=20
    va_ndp=35 (half of ed): w_ndp = (35/70)*20 = 10; w_ucp = 15 (all VA UCP)
    contribution = (10 - 15) / 100 = -0.05
    """
    result = va_eg_contribution(
        va_ndp=35.0, va_ucp=15.0, ed_ndp=70.0, ed_ucp=30.0, total_prov=100.0
    )
    assert result == pytest.approx(-0.05)


def test_va_contribution_ucp_wins_ed():
    """UCP wins the ED; VA contributes proportionally to UCP surplus waste.

    ed_ndp=30, ed_ucp=70, total=100, threshold=50, surplus=20
    va_ucp=35 (half of ed): w_ucp = (35/70)*20 = 10; w_ndp = 15 (all VA NDP)
    contribution = (15 - 10) / 100 = 0.05
    """
    result = va_eg_contribution(
        va_ndp=15.0, va_ucp=35.0, ed_ndp=30.0, ed_ucp=70.0, total_prov=100.0
    )
    assert result == pytest.approx(0.05)


def test_va_contribution_zero_ed_votes():
    """ED with zero votes: contribution = 0."""
    assert va_eg_contribution(0, 0, 0, 0, 100) == 0.0
