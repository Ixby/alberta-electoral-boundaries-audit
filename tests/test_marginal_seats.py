"""Pytest suite for marginal seats and uniform partisan swing.

Tests the margin calculations and uniform shift logic used to find
tipping-point districts.

Run from the repo root:
    python -m pytest tests/test_marginal_seats.py -v
"""

import sys
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from marginal_seats_analysis import (
    compute_margins,
    apply_uniform_swing,
    bucket_marginals,
)


def test_compute_margins(sample_ed_results):
    """Test two-party margin calculation."""
    enr = compute_margins(sample_ed_results)
    assert len(enr) == 4
    assert enr[0]["winner"] == "NDP"
    # The compute_margins logic returns margin as: (winner_votes / total) - 0.5
    assert math.isclose(enr[0]["margin"], 0.2, abs_tol=1e-5)
    assert math.isclose(enr[0]["abs_margin_pp"], 20.0, abs_tol=1e-5)
    
    assert enr[3]["winner"] == "UCP"
    assert math.isclose(enr[3]["margin"], -0.3, abs_tol=1e-5) # 80/100 - 0.5 = 0.3, but negative for UCP
    assert math.isclose(enr[3]["abs_margin_pp"], 30.0, abs_tol=1e-5)


def test_bucket_marginals():
    """Test bucket filtering for close races."""
    enr = [
        {"margin": 0.02},  # 2 pp NDP win
        {"margin": -0.04},  # 4 pp UCP win
        {"margin": 0.10},  # 10 pp NDP win
    ]
    res = bucket_marginals(enr, 5.0)
    assert len(res) == 2


def test_apply_uniform_swing():
    """Test uniform shift logic that flips seats."""
    enr = [
        {"ed": "ED1", "region": "A", "winner": "NDP", "ndp_share": 0.52},
        {"ed": "ED2", "region": "A", "winner": "NDP", "ndp_share": 0.60},
    ]
    # Swing 3 points to UCP (subtracts 0.03 from NDP share)
    res = apply_uniform_swing(enr, 3.0)
    assert res["before"] == (2, 0)
    assert res["after"] == (1, 1)

    flips = res["flips"]
    assert len(flips) == 1
    assert flips[0]["ed"] == "ED1"
    assert flips[0]["new_winner"] == "UCP"
