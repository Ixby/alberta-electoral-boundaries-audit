"""Tests for historical EG baseline and Canadian base rate computation.

Phase E: guards two supporting analytical claims:
  - historical_eg_baseline.compute_eg(): the EG formula applied to 2015/2019/2023
    Alberta elections establishes the province-specific historical reference range.
  - canadian_base_rate_compute.Cycle: the proxy EG-asymmetry calculation used to
    situate Alberta 2026 against other Canadian redistribution cycles.

All tests are pure-function (no file I/O) and run in milliseconds.

Run from the repo root:
    python -m pytest tests/test_cross_election_baseline.py -v
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from historical_eg_baseline import compute_eg
from canadian_base_rate_compute import Cycle


# ============================================================
# historical_eg_baseline.compute_eg
# Uses integer threshold: tt // 2 + 1 (discrete wasted-vote form)
# Sign: code_eg = (NDP_wasted - RBC_wasted) / total_2p
#   positive → NDP structural disadvantage
#   negative → RBC structural disadvantage
# ============================================================


def test_eg_symmetric_two_districts():
    """Mirror-image two-district map: EG = 0 exactly.

    D1: NDP 60, RBC 40 (NDP wins); thr=51; ndp_w=9, rbc_w=40
    D2: NDP 40, RBC 60 (RBC wins); thr=51; ndp_w=40, rbc_w=9
    EG = (9+40 - 40+9) / 200 = 0
    Note: compute_eg returns code_eg_pct (already × 100, rounded to 4dp).
    """
    districts = [
        {"ndp": 60, "rbc": 40, "actual_winner": "NDP"},
        {"ndp": 40, "rbc": 60, "actual_winner": "RBC"},
    ]
    result = compute_eg(districts, "symmetric")
    assert result["code_eg_pct"] == pytest.approx(0.0)


def test_eg_packed_ndp_is_positive():
    """NDP packing: one safe NDP seat, two narrow RBC wins → positive EG."""
    districts = [
        {"ndp": 80, "rbc": 20, "actual_winner": "NDP"},
        {"ndp": 45, "rbc": 55, "actual_winner": "RBC"},
        {"ndp": 45, "rbc": 55, "actual_winner": "RBC"},
    ]
    result = compute_eg(districts, "packed_ndp")
    assert result["code_eg_pct"] > 0


def test_eg_packed_rbc_is_negative():
    """RBC packing: one safe RBC seat, two narrow NDP wins → negative EG."""
    districts = [
        {"ndp": 55, "rbc": 45, "actual_winner": "NDP"},
        {"ndp": 55, "rbc": 45, "actual_winner": "NDP"},
        {"ndp": 20, "rbc": 80, "actual_winner": "RBC"},
    ]
    result = compute_eg(districts, "packed_rbc")
    assert result["code_eg_pct"] < 0


def test_eg_formula_exact_three_districts():
    """Verify exact arithmetic on a known three-district case.

    D1: NDP 60, RBC 40, NDP wins; thr=100//2+1=51; ndp_w=9,  rbc_w=40
    D2: NDP 40, RBC 60, RBC wins; thr=51;            ndp_w=40, rbc_w=9
    D3: NDP 40, RBC 60, RBC wins; thr=51;            ndp_w=40, rbc_w=9
    total_2p = 300
    code_eg = (9+40+40 - 40+9+9) / 300 = 31/300
    code_eg_pct = round(31/300 * 100, 4) = 10.3333
    """
    districts = [
        {"ndp": 60, "rbc": 40, "actual_winner": "NDP"},
        {"ndp": 40, "rbc": 60, "actual_winner": "RBC"},
        {"ndp": 40, "rbc": 60, "actual_winner": "RBC"},
    ]
    result = compute_eg(districts, "formula")
    assert result["code_eg_pct"] == pytest.approx(31 / 300 * 100, rel=1e-3)


def test_eg_raises_on_empty_input():
    """Empty district list → no valid votes → ValueError."""
    with pytest.raises(ValueError):
        compute_eg([], "empty")


def test_eg_returns_dict_with_required_keys():
    """Result dict must include code_eg_pct and vote/win counts."""
    districts = [
        {"ndp": 60, "rbc": 40, "actual_winner": "NDP"},
        {"ndp": 40, "rbc": 60, "actual_winner": "RBC"},
    ]
    result = compute_eg(districts, "keys_check")
    assert "code_eg_pct" in result
    assert "ndp_wins" in result
    assert "rbc_wins" in result


def test_eg_winner_counts_correct():
    """Win counts match the actual_winner labels."""
    districts = [
        {"ndp": 60, "rbc": 40, "actual_winner": "NDP"},
        {"ndp": 55, "rbc": 45, "actual_winner": "NDP"},
        {"ndp": 30, "rbc": 70, "actual_winner": "RBC"},
    ]
    result = compute_eg(districts, "win_counts")
    assert result["ndp_wins"] == 2
    assert result["rbc_wins"] == 1


# ============================================================
# canadian_base_rate_compute.Cycle
# ============================================================


def test_cycle_seat_share_asymmetry_formula():
    """seat_share_asymmetry_pp = seat_flips / seats_total * 100."""
    c = Cycle(
        jurisdiction="Test", cycle_year="2026",
        map_a_label="A", map_b_label="B",
        seats_total=89, seat_flips_estimate=1,
    )
    assert c.seat_share_asymmetry_pp == pytest.approx(1 / 89 * 100)


def test_cycle_eg_asymmetry_proxy_deflator():
    """EG proxy applies 0.455× deflator to the seat-share asymmetry.

    1 flip / 89 seats = 1.1236 pp seat share; × 0.455 ≈ 0.5112 pp EG.
    This matches the audit's measured 0.51 pp EG asymmetry for Alberta 2026.
    """
    c = Cycle(
        jurisdiction="Alberta_provincial", cycle_year="2026",
        map_a_label="commission_majority", map_b_label="commission_minority",
        seats_total=89, seat_flips_estimate=1,
    )
    expected = (1 / 89 * 100) * 0.455
    assert c.eg_asymmetry_proxy_pp == pytest.approx(expected, rel=1e-6)


def test_cycle_zero_flips_gives_zero_asymmetry():
    """Zero seat flips → 0 pp EG asymmetry."""
    c = Cycle(
        jurisdiction="Test", cycle_year="2022",
        map_a_label="A", map_b_label="B",
        seats_total=37, seat_flips_estimate=0,
    )
    assert c.seat_share_asymmetry_pp == pytest.approx(0.0)
    assert c.eg_asymmetry_proxy_pp == pytest.approx(0.0)


def test_cycle_none_flips_returns_none():
    """When seat_flips_estimate is None, both properties return None."""
    c = Cycle(
        jurisdiction="Test", cycle_year="2023",
        map_a_label="A", map_b_label="B",
        seats_total=93, seat_flips_estimate=None,
    )
    assert c.seat_share_asymmetry_pp is None
    assert c.eg_asymmetry_proxy_pp is None


def test_cycle_three_flips_scales_linearly():
    """Three flips in a 90-seat chamber: 3/90*100 * 0.455 pp."""
    c = Cycle(
        jurisdiction="Test", cycle_year="2024",
        map_a_label="A", map_b_label="B",
        seats_total=90, seat_flips_estimate=3,
    )
    expected = 3 / 90 * 100 * 0.455
    assert c.eg_asymmetry_proxy_pp == pytest.approx(expected, rel=1e-6)


def test_cycle_low_high_bounds_present():
    """Low and high bound properties are available when set."""
    c = Cycle(
        jurisdiction="Test", cycle_year="2026",
        map_a_label="A", map_b_label="B",
        seats_total=89, seat_flips_estimate=1,
        seat_flips_low=1, seat_flips_high=3,
    )
    assert c.eg_asymmetry_low_pp == pytest.approx(1 / 89 * 100 * 0.455, rel=1e-6)
    assert c.eg_asymmetry_high_pp == pytest.approx(3 / 89 * 100 * 0.455, rel=1e-6)
