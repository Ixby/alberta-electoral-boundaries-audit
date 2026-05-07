"""Pytest suite for extended partisan symmetry metrics.

Tests calculations for Partisan Bias, Lopsided Margins (t-test),
Responsiveness, and Partisan Gini against synthetic arrays of
vote shares to ensure statistical correctness.

Run from the repo root:
    python -m pytest tests/test_extended_metrics.py -v
"""

import sys
import math
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from extended_partisan_metrics import (
    partisan_bias,
    lopsided_margins,
    partisan_gini,
    responsiveness,
)

# ============================================================
# Extended partisan metric tests
# ============================================================


def test_partisan_bias_symmetric():
    """A perfectly tied 50/50 map should yield 0.0 partisan bias."""
    ucp_shares = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
    assert partisan_bias(ucp_shares) == 0.0


def test_partisan_bias_asymmetric():
    """A map where UCP gets 44% of votes but 20% of seats at a 50% swing
    should have a known bias of -0.3.
    """
    ucp_shares = np.array([0.6, 0.4, 0.4, 0.4, 0.4])
    assert math.isclose(partisan_bias(ucp_shares), -0.3, abs_tol=1e-5)


def test_lopsided_margins_packed():
    """UCP wins by 90% (heavy packing), NDP wins by 55% (narrow).
    This packing signal should produce a significant t-test result.
    """
    ucp_shares = np.array([0.9, 0.9, 0.9, 0.45, 0.45, 0.45])
    t, p = lopsided_margins(ucp_shares)
    assert t > 0
    assert p < 0.05


def test_lopsided_margins_symmetric():
    """Perfectly symmetric wins for both sides should yield t=0.0."""
    symmetric_shares = np.array([0.55, 0.60, 0.65, 0.35, 0.40, 0.45])
    t_sym, p_sym = lopsided_margins(symmetric_shares)
    assert math.isclose(t_sym, 0.0, abs_tol=1e-5)
    assert math.isclose(p_sym, 1.0, abs_tol=1e-5)


def test_lopsided_margins_insufficient_data():
    """Not enough wins for one party to compute variance should return NaN."""
    sweep = np.array([0.6, 0.6, 0.6, 0.6])
    t, p = lopsided_margins(sweep)
    assert math.isnan(t)
    assert math.isnan(p)


def test_responsiveness():
    """A highly competitive map where all seats flip on a tiny swing
    should yield high responsiveness (steep curve slope).
    """
    shares = np.array([0.5] * 10)
    resp = responsiveness(shares)
    assert math.isclose(resp, 50.0, abs_tol=1e-5)


def test_partisan_gini_symmetric():
    """A map with symmetric vote distributions should have a 0.0 Gini coefficient."""
    shares = np.array([0.6, 0.4])
    gini = partisan_gini(shares)
    assert math.isclose(gini, 0.0, abs_tol=1e-2)


def test_partisan_gini_biased():
    """Asymmetrical safe seats vs narrow losses should successfully compute Gini."""
    shares = np.array([0.6, 0.6, 0.49])
    gini = partisan_gini(shares)
    assert not math.isnan(gini)
