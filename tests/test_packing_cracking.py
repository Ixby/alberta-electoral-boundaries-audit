"""Pytest suite for packing and cracking logic.

Tests the estimation constraints and gating for the 2026 UCP/NDP
vote estimates to ensure basic data validity (e.g. correct number
of districts and plausible vote totals).

Run from the repo root:
    python -m pytest tests/test_packing_cracking.py -v
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from packing_cracking_analysis import validate_2026_estimate

# ============================================================
# Packing & cracking data validation tests
# ============================================================


def test_validate_2026_estimate_success():
    """A valid estimate array of 89 EDs with correct total votes should pass."""
    dummy_eds = [{"ed": f"ED{i}", "ndp": 9000, "ucp": 10000} for i in range(89)]
    ok, msg = validate_2026_estimate(dummy_eds, "Test Estimate")
    assert ok is True
    assert msg == "PASS"


def test_validate_2026_estimate_wrong_count():
    """An array with fewer than 89 EDs should fail validation."""
    dummy_eds = [{"ed": f"ED{i}", "ndp": 9000, "ucp": 10000} for i in range(88)]
    ok, msg = validate_2026_estimate(dummy_eds, "Test Estimate")
    assert ok is False
    assert "FAIL" in msg
    assert "has 88 EDs, expected 89" in msg


def test_validate_2026_estimate_wrong_totals():
    """An array where total votes fall wildly outside the ~1.7M plausible range should fail."""
    # Only 89 * 1900 = 169k votes (fails 1.6M - 1.8M gate)
    dummy_eds = [{"ed": f"ED{i}", "ndp": 900, "ucp": 1000} for i in range(89)]
    ok, msg = validate_2026_estimate(dummy_eds, "Test Estimate")
    assert ok is False
    assert "FAIL" in msg
    assert "outside plausible range" in msg
