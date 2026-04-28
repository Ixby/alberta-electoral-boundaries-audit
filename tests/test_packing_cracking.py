import os
import pytest
import sys

# Add analysis/scripts to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analysis', 'scripts')))
from packing_cracking_analysis import validate_2026_estimate

def test_validate_2026_estimate_success():
    # Provide exactly 89 dummy EDs with total votes around 1.7M, and NDP share around 45%
    dummy_eds = [{'ed': f'ED{i}', 'ndp': 9000, 'ucp': 10000} for i in range(89)]
    # total votes = 89 * 19000 = 1,691,000. NDP = 89*9000 = 801,000. Share = 47.3%
    ok, msg = validate_2026_estimate(dummy_eds, "Test Estimate")
    assert ok is True
    assert msg == "PASS"

def test_validate_2026_estimate_wrong_count():
    dummy_eds = [{'ed': f'ED{i}', 'ndp': 9000, 'ucp': 10000} for i in range(88)]
    ok, msg = validate_2026_estimate(dummy_eds, "Test Estimate")
    assert ok is False
    assert "FAIL" in msg
    assert "has 88 EDs, expected 89" in msg

def test_validate_2026_estimate_wrong_totals():
    # Only 89 * 1900 = 169k votes (fails 1.6M - 1.8M gate)
    dummy_eds = [{'ed': f'ED{i}', 'ndp': 900, 'ucp': 1000} for i in range(89)]
    ok, msg = validate_2026_estimate(dummy_eds, "Test Estimate")
    assert ok is False
    assert "FAIL" in msg
    assert "outside plausible range" in msg
