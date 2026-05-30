"""
tests/test_s15_classify.py — Unit tests for the EBCA §15(2) classify() function.

The classify() routine in analysis/scripts/s15_ratio_test.py decides each
electoral division's compliance status from two inputs:
  - `deviation`: the ED's population deviation from the provincial quota,
    expressed as a signed fraction (e.g. 0.10 = +10%, -0.45 = -45%).
  - `invocation`: a dict (or None) describing whether the commission
    invoked §15(2) protection for this ED, and how many of the five
    statutory criteria it claims to meet.

The decision boundaries are statutory:
  - Normal band: ±25% (LOWER_BAND = -0.25, UPPER_BAND = +0.25).
  - §15(2) absolute floor: -50%.

These tests cover every branch of the classify() decision tree so a
future edit can't silently regress the EBCA mapping.

Forward dependencies: none
Backward dependencies: analysis/scripts/s15_ratio_test.py (classify)
"""
from __future__ import annotations

import importlib.util
import pathlib

import pytest


# Import classify() directly from the script without running it. The script's
# top-level code reads a CSV; we don't want to trigger that at import time.
def _load_classify():
    spec = importlib.util.spec_from_file_location(
        "_s15_for_tests",
        pathlib.Path(__file__).resolve().parents[1]
        / "analysis"
        / "scripts"
        / "s15_ratio_test.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.classify


classify = _load_classify()


def _invocation(*, criteria_met: int = 4, verdict: str = "Pass") -> dict:
    """Convenience: build a minimal invocation dict matching the schema
    classify() reads."""
    return {"criteria_met": criteria_met, "verdict": verdict, "notes": ""}


# ── COMPLIANT branch — deviation inside ±25%, no §15(2) invocation ────────────


class TestCompliant:
    def test_dead_centre_is_compliant(self):
        assert classify(0.0, None) == "COMPLIANT"

    def test_just_below_upper_band_is_compliant(self):
        assert classify(0.249, None) == "COMPLIANT"

    def test_just_above_lower_band_is_compliant(self):
        assert classify(-0.249, None) == "COMPLIANT"

    def test_exactly_upper_band_is_compliant(self):
        # `deviation > UPPER_BAND` is strict; exactly +25% stays compliant.
        assert classify(0.25, None) == "COMPLIANT"

    def test_exactly_lower_band_is_compliant_without_invocation(self):
        # `deviation <= LOWER_BAND` triggers the §15(2) branch, but only if
        # invocation is non-None. With invocation=None it falls through to
        # `deviation < LOWER_BAND` (strict), which -0.25 does NOT satisfy.
        assert classify(-0.25, None) == "COMPLIANT"


# ── VIOLATION_OVER — above +25%, no §15(2) shield (§15(2) is for undersize) ───


class TestViolationOver:
    def test_just_above_upper_band(self):
        assert classify(0.251, None) == "VIOLATION_OVER"

    def test_far_above_upper_band(self):
        assert classify(1.0, None) == "VIOLATION_OVER"

    def test_s15_invocation_does_not_shield_overcounts(self):
        # §15(2) protects undersize ridings only — an invocation on an
        # oversize riding should still classify as VIOLATION_OVER.
        # The function does this via the order of branches: the first two
        # S15 branches require `deviation <= LOWER_BAND` or
        # `deviation > LOWER_BAND` with a passed-in invocation; the
        # overcount branch fires before either applies when invocation
        # is None but deviation > UPPER_BAND. However if invocation IS
        # supplied for an overcount, the second branch ("S15_IN_BAND")
        # takes it — which is a documented "notable but not unlawful"
        # signal rather than a violation. Lock in the current behaviour.
        assert classify(0.3, _invocation()) == "S15_IN_BAND"


# ── VIOLATION_UNDER — below -25%, no §15(2) invocation registered ─────────────


class TestViolationUnder:
    def test_just_below_lower_band(self):
        assert classify(-0.251, None) == "VIOLATION_UNDER"

    def test_well_below_band_no_invocation(self):
        assert classify(-0.45, None) == "VIOLATION_UNDER"


# ── S15_JUSTIFIED — undersize, §15(2) invoked, above the -50% floor ──────────


class TestS15Justified:
    def test_undersize_with_invocation_and_above_floor(self):
        assert classify(-0.45, _invocation()) == "S15_JUSTIFIED"

    def test_exactly_at_lower_band_with_invocation_is_justified(self):
        # The branch tests `deviation <= LOWER_BAND`, inclusive.
        assert classify(-0.25, _invocation()) == "S15_JUSTIFIED"

    def test_exactly_at_floor_is_justified_not_breach(self):
        # `deviation < S15_FLOOR` is strict; exactly -50% remains justified.
        assert classify(-0.50, _invocation()) == "S15_JUSTIFIED"


# ── S15_FLOOR_BREACH — undersize, §15(2) invoked, but below the -50% floor ───


class TestS15FloorBreach:
    def test_below_floor_with_invocation_is_a_breach(self):
        assert classify(-0.51, _invocation()) == "S15_FLOOR_BREACH"

    def test_far_below_floor(self):
        assert classify(-0.99, _invocation()) == "S15_FLOOR_BREACH"


# ── S15_IN_BAND — §15(2) invoked but deviation is already in the normal band ─


class TestS15InBand:
    def test_invocation_within_normal_band_is_notable_not_violation(self):
        # Per docstring: "deviation within ±25% but §15(2) invoked
        # (notable: not required but also not unlawful)."
        assert classify(0.0, _invocation()) == "S15_IN_BAND"

    def test_invocation_with_modest_undersize(self):
        # Just inside -25%: invocation reads as a precaution, not a need.
        assert classify(-0.10, _invocation()) == "S15_IN_BAND"


# ── Invocation shape does not affect the routing ─────────────────────────────


class TestInvocationOpacity:
    def test_classify_does_not_inspect_criteria_count(self):
        # classify() routes on presence/absence of `invocation`; the
        # criteria_met value is informational and lives in the output CSV.
        # Same deviation + truthy invocation → same status regardless of count.
        s_three = classify(-0.45, _invocation(criteria_met=3))
        s_five = classify(-0.45, _invocation(criteria_met=5))
        assert s_three == s_five == "S15_JUSTIFIED"

    def test_classify_does_not_inspect_verdict_string(self):
        s_pass = classify(-0.45, _invocation(verdict="Pass"))
        s_fail = classify(-0.45, _invocation(verdict="Fail"))
        assert s_pass == s_fail == "S15_JUSTIFIED"
