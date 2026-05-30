"""
tests/test_proportionality_deviation.py — Unit tests for the renamed
`proportionality_deviation()` and related metrics in
analysis/scripts/extended_partisan_metrics.py.

These tests lock in two properties that were the reason for the stage-4q
rename from `partisan_gini`:

  1. proportionality_deviation measures the area between the seats-votes
     curve and the 1:1 proportionality line s(v) = v — NOT between the
     curve and its mirror-image symmetry curve (which would be the
     King 1989 / Gelman & King 1994 Partisan Gini).
  2. Positive return = the map gives the first party (UCP) more seats
     than proportional across the swing range.

Also pins the other inexpensive metrics in the same module:
  - partisan_bias: signed gap between UCP seat share at v=0.5 and 0.5
  - lopsided_margins: Welch t-test on win margins by party
  - responsiveness: numerical derivative of seats-votes curve at v=0.5

Forward dependencies: none
Backward dependencies: analysis/scripts/extended_partisan_metrics.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import types

import numpy as np
import pytest


def _load_module():
    """Load extended_partisan_metrics.py without triggering its main()."""
    script_path = (
        pathlib.Path(__file__).resolve().parents[1]
        / "analysis"
        / "scripts"
        / "extended_partisan_metrics.py"
    )
    # The script imports `data_loader` at module load via a sys.path hack;
    # stub it to avoid touching the filesystem when running these unit tests.
    if "data_loader" not in sys.modules:
        stub = types.ModuleType("data_loader")
        stub._resolve_path = lambda p: pathlib.Path(p)  # type: ignore[attr-defined]
        stub.FINDINGS = pathlib.Path("/tmp")  # type: ignore[attr-defined]
        sys.modules["data_loader"] = stub
    spec = importlib.util.spec_from_file_location("_epm_for_tests", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


epm = _load_module()


# ── partisan_bias ─────────────────────────────────────────────────────────────


class TestPartisanBias:
    def test_symmetric_distribution_centred_on_05_is_zero_bias(self):
        # UCP shares perfectly symmetric around 0.5 — uniform swing to
        # v=0.5 leaves a 50/50 split of districts ⇒ seat share 0.5 ⇒ bias 0.
        shares = np.array([0.4, 0.45, 0.5, 0.55, 0.6])
        bias = epm.partisan_bias(shares)
        assert bias == pytest.approx(0.0, abs=1e-12)

    def test_packed_minority_signature_is_negative_bias(self):
        # All UCP wins are by huge margins, all NDP wins are narrow — when
        # swung to v=0.5 the UCP wins fewer seats than proportional.
        shares = np.array([0.20, 0.30, 0.40, 0.49, 0.49, 0.95, 0.95])
        bias = epm.partisan_bias(shares)
        # UCP-favorable side would be > 0; this layout disadvantages UCP.
        assert bias < 0

    def test_packed_majority_signature_is_positive_bias(self):
        # All UCP wins are by narrow margins, NDP wins by landslides ⇒
        # under uniform swing to v=0.5 the UCP wins more than half the seats.
        shares = np.array([0.05, 0.05, 0.51, 0.51, 0.60, 0.70, 0.80])
        bias = epm.partisan_bias(shares)
        assert bias > 0


# ── lopsided_margins (Wang 2016) ──────────────────────────────────────────────


class TestLopsidedMargins:
    def test_returns_nan_when_one_party_has_fewer_than_3_wins(self):
        # Need ≥3 wins on each side to run a t-test.
        shares = np.array([0.6, 0.6, 0.6, 0.6, 0.4, 0.4])  # only 2 NDP wins
        t, p = epm.lopsided_margins(shares)
        assert np.isnan(t)
        assert np.isnan(p)

    def test_returns_real_numbers_when_both_parties_have_3_plus_wins(self):
        shares = np.array([0.6, 0.7, 0.8, 0.3, 0.4, 0.45])
        t, p = epm.lopsided_margins(shares)
        assert np.isfinite(t)
        assert 0.0 <= p <= 1.0

    def test_positive_t_when_ucp_wins_by_larger_margins(self):
        # UCP wins clustered at 0.80–0.95 (margin ≥ 0.30 above 0.5);
        # NDP wins clustered at 0.45–0.49 (margin ≤ 0.05 below 0.5).
        shares = np.array([0.80, 0.85, 0.90, 0.95, 0.45, 0.47, 0.48, 0.49])
        t, _ = epm.lopsided_margins(shares)
        assert t > 0

    def test_negative_t_when_ndp_wins_by_larger_margins(self):
        shares = np.array([0.05, 0.10, 0.15, 0.20, 0.51, 0.53, 0.54, 0.55])
        t, _ = epm.lopsided_margins(shares)
        assert t < 0


# ── proportionality_deviation (the renamed metric) ───────────────────────────


class TestProportionalityDeviation:
    def test_perfectly_proportional_map_returns_near_zero(self):
        # Constructing a vote distribution whose seats-votes curve hugs s=v
        # is non-trivial in a small sample, but a near-uniform spread of
        # vote shares should yield a small area between curve and line.
        shares = np.linspace(0.05, 0.95, 25)
        pd = epm.proportionality_deviation(shares)
        # Tighter than 0.1 is "small" given the metric is bounded in [-0.6, 0.6].
        assert abs(pd) < 0.1

    def test_winners_take_all_packed_for_ucp_is_positive(self):
        # All vote shares strongly favour UCP wins; the seats-votes curve
        # sits above the proportionality line across the swing range.
        shares = np.array([0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90])
        pd = epm.proportionality_deviation(shares)
        assert pd > 0

    def test_distribution_favouring_ndp_yields_negative_deviation(self):
        shares = np.array([0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40])
        pd = epm.proportionality_deviation(shares)
        assert pd < 0


# ── responsiveness ────────────────────────────────────────────────────────────


class TestResponsiveness:
    def test_returns_finite_real_number(self):
        shares = np.array([0.30, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70])
        r = epm.responsiveness(shares)
        assert np.isfinite(r)

    def test_responsiveness_is_non_negative_for_typical_curves(self):
        # A monotone non-decreasing seats-votes curve should have a
        # non-negative slope at the v=0.5 inflection point.
        shares = np.array([0.30, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70])
        r = epm.responsiveness(shares)
        assert r >= 0
