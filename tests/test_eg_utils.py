"""
tests/test_eg_utils.py — Unit tests for analysis/utils/eg_utils.py.

Forward dependencies: none
Backward dependencies: eg_utils.py
"""
from __future__ import annotations

import pytest
import pandas as pd

from analysis.utils.eg_utils import (
    InsufficientDataError,
    _ed_waste,
    compute_eg,
)


# ── _ed_waste ──────────────────────────────────────────────────────────────────

class TestEdWaste:
    def test_zero_total_returns_zero_pair(self):
        assert _ed_waste(0.0, 0.0) == (0.0, 0.0)

    def test_ndp_landslide_loser_wastes_all(self):
        ndp_w, ucp_w = _ed_waste(80.0, 20.0)
        # NDP wins: surplus above threshold (50) wasted; UCP wastes all 20
        assert ndp_w == pytest.approx(30.0)
        assert ucp_w == pytest.approx(20.0)

    def test_ucp_landslide_loser_wastes_all(self):
        ndp_w, ucp_w = _ed_waste(20.0, 80.0)
        assert ndp_w == pytest.approx(20.0)
        assert ucp_w == pytest.approx(30.0)

    def test_tie_treated_as_ndp_win(self):
        # ndp == ucp → NDP wins by convention (ndp >= ucp)
        ndp_w, ucp_w = _ed_waste(50.0, 50.0)
        # threshold = 50; NDP wins with 0 surplus, UCP wastes all 50
        assert ndp_w == pytest.approx(0.0)
        assert ucp_w == pytest.approx(50.0)

    def test_ndp_narrow_win_no_negative_waste(self):
        ndp_w, ucp_w = _ed_waste(51.0, 49.0)
        assert ndp_w == pytest.approx(1.0)
        assert ucp_w == pytest.approx(49.0)
        assert ndp_w >= 0.0
        assert ucp_w >= 0.0

    def test_fractional_votes_continuous_threshold(self):
        # threshold = (30.5 + 10.5) / 2 = 20.5
        ndp_w, ucp_w = _ed_waste(30.5, 10.5)
        assert ndp_w == pytest.approx(30.5 - 20.5)
        assert ucp_w == pytest.approx(10.5)

    @pytest.mark.parametrize("ndp,ucp", [
        (0.0, 100.0),
        (100.0, 0.0),
        (1.0, 1.0),
        (0.001, 999.999),
    ])
    def test_winner_wastes_surplus_loser_wastes_all(self, ndp, ucp):
        ndp_w, ucp_w = _ed_waste(ndp, ucp)
        total = ndp + ucp
        threshold = total / 2
        assert ndp_w >= 0.0
        assert ucp_w >= 0.0
        if ndp >= ucp:  # NDP wins
            assert ndp_w == pytest.approx(max(0.0, ndp - threshold))
            assert ucp_w == pytest.approx(ucp)
        else:           # UCP wins
            assert ndp_w == pytest.approx(ndp)
            assert ucp_w == pytest.approx(max(0.0, ucp - threshold))


# ── compute_eg ─────────────────────────────────────────────────────────────────

class TestComputeEg:
    def _df(self, rows: list[tuple[float, float]]) -> pd.DataFrame:
        return pd.DataFrame(rows, columns=["ndp", "ucp"])

    def test_missing_ndp_column_raises(self):
        df = pd.DataFrame({"ucp": [100.0]})
        with pytest.raises(InsufficientDataError, match="ndp"):
            compute_eg(df)

    def test_missing_ucp_column_raises(self):
        df = pd.DataFrame({"ndp": [100.0]})
        with pytest.raises(InsufficientDataError, match="ucp"):
            compute_eg(df)

    def test_all_zero_votes_returns_zero(self):
        df = self._df([(0.0, 0.0), (0.0, 0.0)])
        assert compute_eg(df) == 0.0

    def test_perfectly_efficient_two_eds(self):
        # One NDP win (60/40), one UCP win (40/60) — symmetric waste cancels
        df = self._df([(60.0, 40.0), (40.0, 60.0)])
        eg = compute_eg(df)
        # NDP district: ndp_w=10, ucp_w=40. UCP district: ndp_w=40, ucp_w=10.
        # EG = (50 - 50) / 200 = 0.0
        assert eg == pytest.approx(0.0)

    def test_ndp_wins_all_negative_eg(self):
        # NDP wins every seat → NDP wastes less → EG = (wn-wu)/total < 0 (NDP-favoured)
        df = self._df([(51.0, 49.0)] * 5)
        eg = compute_eg(df)
        assert eg < 0.0

    def test_ucp_wins_all_positive_eg(self):
        # UCP wins every seat → UCP wastes less → EG = (wn-wu)/total > 0 (UCP-favoured)
        df = self._df([(49.0, 51.0)] * 5)
        eg = compute_eg(df)
        assert eg > 0.0

    def test_result_in_minus_one_to_one(self):
        import random
        rng = random.Random(0)
        rows = [(rng.uniform(0, 1000), rng.uniform(0, 1000)) for _ in range(87)]
        df = self._df(rows)
        eg = compute_eg(df)
        assert -1.0 <= eg <= 1.0

    def test_custom_column_names(self):
        # "left" (ndp_col) wins 60/40 → ndp wastes less → EG < 0
        df = pd.DataFrame({"left": [60.0], "right": [40.0]})
        eg = compute_eg(df, ndp_col="left", ucp_col="right")
        assert eg < 0.0
