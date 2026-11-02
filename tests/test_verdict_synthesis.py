"""Partisan-lane flags in verdict_synthesis.py fire only in the UCP direction (spec section 3)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis" / "scripts"))
import verdict_synthesis as vs  # noqa: E402


def marg(obs, mean, tail_p):
    return {"observed": obs, "ensemble_mean": mean, "marginal_tail_p": tail_p}


def joint(eg, mm, decl, s50):
    return {"maps": {"candidate": {"marginals": {
        "efficiency_gap": marg(*eg), "mean_median": marg(*mm),
        "declination": marg(*decl), "seats_at_50_50": marg(*s50)}}}}


def test_low_tail_does_not_fire():
    # The majority commission map: mean-median at about p1, below the ensemble mean.
    # The old rule read 1 - 0.01 = 0.99 and fired P2 in the UCP direction.
    v, d = vs.partisan_verdict_from_joint(joint((0.001, 0.02, 0.4), (-0.036, -0.01, 0.01),
                                                (-0.027, 0.0, 0.22), (0.46, 0.45, 0.21)))
    assert d["flags"] == {"P1_EG": False, "P2_MM": False, "P3_DECL": False, "P4_S50": False}
    assert v == "absent"


def test_high_tail_fires():
    # The minority commission map: three metrics above p95 in the UCP direction.
    v, d = vs.partisan_verdict_from_joint(joint((0.040, 0.02, 0.055), (0.010, -0.01, 0.0),
                                                (0.077, 0.0, 0.012), (0.517, 0.45, 0.0)))
    assert d["n_flags"] == 3 and v == "present"


def test_explicit_percentile_is_used():
    j = joint((0.0, 0.0, 0.5), (0.0, 0.0, 0.5), (0.0, 0.0, 0.5), (0.0, 0.0, 0.5))
    for k in ("mean_median", "seats_at_50_50"):
        j["maps"]["candidate"]["marginals"][k]["ucp_direction_percentile"] = 0.97
    v, d = vs.partisan_verdict_from_joint(j)
    assert d["flags"]["P2_MM"] and d["flags"]["P4_S50"] and v == "present"


def test_ndp_declination_tail_reported_not_counted():
    j = joint((0.0, 0.0, 0.5), (0.0, 0.0, 0.5), (-0.1, 0.0, 0.01), (0.0, 0.0, 0.5))
    v, d = vs.partisan_verdict_from_joint(j)
    assert d["P3_ndp_direction_tail"] and not d["flags"]["P3_DECL"]


def test_missing_candidate_is_an_error_not_absent():
    with pytest.raises(SystemExit):
        vs.partisan_verdict_from_joint({"maps": {}})
    with pytest.raises(SystemExit):
        vs.partisan_verdict_from_joint({})
