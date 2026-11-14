"""Regression tests for the 2026-11-10 infrastructure fixes.

Covers, on synthetic inputs (no committed data needed):
  - pct_rank counts near-equal values as ties (the CSV float-parsing bug);
  - autocorrelation_ess reports whether its lag cap bound, and has an
    uncapped option;
  - packing_cracking_analysis keeps fractional voting-area votes unless the
    legacy flag is set;
  - third_party_sensitivity takes "other" votes from total_valid_votes;
  - run_audit.py's name checks test the name column;
  - verify_joint_empirical_bound builds its notes from computed values.

Run from the repo root:
    python -m pytest tests/test_infra_fixes.py -v

Forward dependencies: none
Backward dependencies: analysis/scripts/{mcmc_ensemble, simulation_multichain_ensemble,
    packing_cracking_analysis, third_party_sensitivity, verify_joint_empirical_bound}.py,
    run_audit.py
"""
from __future__ import annotations

import ast
import io
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
sys.path.insert(0, str(ROOT / "analysis" / "utils"))

from mcmc_ensemble import PCT_RANK_TIE_ATOL, autocorrelation_ess, pct_rank  # noqa: E402


# ── pct_rank: ties survive a CSV round trip ──────────────────────────────────

def _through_default_csv_parser(values: np.ndarray) -> np.ndarray:
    buf = io.StringIO()
    pd.DataFrame({"v": values}).to_csv(buf, index=False)
    buf.seek(0)
    return pd.read_csv(buf)["v"].to_numpy()


def test_default_parser_really_misparses_some_seat_shares():
    """The premise of the bug: for some k/87 the default parser returns a float
    that is not the one written. If this ever stops being true the tolerance is
    still harmless, but the regression tests below would no longer exercise it."""
    written = np.array([k / 87 for k in range(88)])
    parsed = _through_default_csv_parser(written)
    off = np.nonzero(parsed != written)[0]
    if len(off) == 0:
        pytest.skip("this pandas version parses every k/87 exactly")
    assert np.abs(parsed - written).max() < 1e-15
    assert 40 in off  # the 2019 map's 40/87


@pytest.mark.parametrize("n", [87, 89, 91])
def test_pct_rank_midrank_for_every_seat_share_after_csv_round_trip(n):
    """For every k/n: a block of plans at exactly that seat share, read back
    from CSV, must be counted as tied with the map's own k/n."""
    for k in range(n + 1):
        ensemble = np.array([(k - 1) / n] * 30 + [k / n] * 50 + [(k + 1) / n] * 20)
        parsed = _through_default_csv_parser(ensemble)
        # midrank: 30 below, 50 tied, of 100
        assert pct_rank(parsed, k / n) == pytest.approx(55.0, abs=1e-12), (k, n)


def test_pct_rank_exact_equality_rule_shows_the_bug():
    """atol=0 is the old rule. On a mis-parsed value it finds no ties and puts
    the map at one end of its tie block."""
    k, n = 40, 87
    ensemble = np.array([(k - 1) / n] * 30 + [k / n] * 50 + [(k + 1) / n] * 20)
    parsed = _through_default_csv_parser(ensemble)
    if (parsed == ensemble).all():
        pytest.skip("this pandas version parses 40/87 exactly")
    assert pct_rank(parsed, k / n, atol=0.0) in (30.0, 80.0)
    assert pct_rank(parsed, k / n) == pytest.approx(55.0)


def test_pct_rank_matches_scipy_midrank_on_exact_values():
    from scipy.stats import percentileofscore

    rng = np.random.default_rng(0)
    values = rng.integers(0, 20, size=500) / 20.0
    for x in (0.0, 0.25, 0.5, 0.95, 2.0, -1.0):
        assert pct_rank(values, x) == pytest.approx(percentileofscore(values, x, kind="mean"))


def test_pct_rank_tolerance_does_not_merge_distinct_continuous_values():
    """Distinct plans' continuous metrics can sit within 1e-9 of a map's value
    (one does, at 6e-10, on the canonical ensemble). They are not ties."""
    assert PCT_RANK_TIE_ATOL <= 1e-11
    x = -0.007671760176883757
    values = np.array([x - 6.1e-10, x + 3.4e-8, x - 1.0, x + 1.0])
    assert pct_rank(values, x) == pytest.approx(50.0)  # 2 below, 0 tied, of 4
    # scaled for large values: population MAD near 3,000 persons
    big = 2826.8945263667047
    assert pct_rank(np.array([big + 8.7e-4, big - 8.7e-4]), big) == pytest.approx(50.0)
    assert pct_rank(np.array([big * (1 + 1e-15), big - 1.0]), big) == pytest.approx(75.0)


def test_pct_rank_nan_contract_unchanged():
    assert np.isnan(pct_rank(np.array([]), 0.5))
    assert np.isnan(pct_rank(np.array([0.1, 0.2]), float("nan")))
    assert pct_rank(np.array([0.1, np.nan, 0.3]), 0.2) == pytest.approx(50.0)


# ── autocorrelation_ess: explicit cap, cap_bound, uncapped option ────────────

def _ar1(n: int, phi: float, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    e = rng.standard_normal(n)
    x = np.empty(n)
    x[0] = e[0]
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def test_ess_default_result_is_unchanged_and_reports_cap_not_bound():
    """A fast-mixing chain: the sum stops well before the cap. The default
    result equals the pre-change formula computed here independently."""
    x = _ar1(5_000, 0.5)
    r = autocorrelation_ess(x)
    xc = x - x.mean()
    var0 = xc @ xc / len(x)
    tau = 1.0
    used = None
    for k in range(1, 1251):
        rho = (xc[:-k] @ xc[k:]) / len(x) / var0
        if rho <= 0:
            used = k - 1
            break
        tau += 2 * rho
    assert r["tau"] == pytest.approx(tau, rel=1e-12)
    assert r["n_eff"] == pytest.approx(len(x) / tau, rel=1e-12)
    assert r["max_lag_used"] == used
    assert r["lag_cap"] == 1250  # min(n // 4, 2000)
    assert r["cap_bound"] is False
    # theory: tau = (1 + phi) / (1 - phi) = 3
    assert r["tau"] == pytest.approx(3.0, rel=0.35)
    # the documented default cap for long chains
    from mcmc_ensemble import ESS_DEFAULT_LAG_CAP
    assert ESS_DEFAULT_LAG_CAP == 2000


def test_ess_cap_bound_is_reported_when_the_cap_stops_the_sum():
    """A slow chain with a small cap: the cap binds, n_eff is an upper bound."""
    x = _ar1(50_000, 0.999, seed=1)
    capped = autocorrelation_ess(x, max_lag=200)
    assert capped["cap_bound"] is True
    assert capped["max_lag_used"] == capped["lag_cap"] == 200
    free = autocorrelation_ess(x, uncapped=True)
    assert free["cap_bound"] is False
    assert free["max_lag_used"] > 200
    assert free["tau"] > capped["tau"]
    assert free["n_eff"] < capped["n_eff"]


def test_ess_uncapped_equals_capped_when_cap_does_not_bind():
    """The FFT path and the lag loop are the same estimator."""
    x = _ar1(5_000, 0.8, seed=2)
    capped = autocorrelation_ess(x)
    free = autocorrelation_ess(x, uncapped=True)
    assert capped["cap_bound"] is False
    assert free["max_lag_used"] == capped["max_lag_used"]
    assert free["tau"] == pytest.approx(capped["tau"], rel=1e-9)
    assert free["rho_lag_1"] == pytest.approx(capped["rho_lag_1"], rel=1e-9)
    assert free["lag_cap"] == len(x) - 1


def test_ess_rejects_max_lag_with_uncapped():
    with pytest.raises(ValueError):
        autocorrelation_ess(np.arange(10.0), max_lag=5, uncapped=True)


def test_ess_degenerate_inputs_carry_the_new_keys():
    for x in (np.array([1.0, 2.0]), np.ones(100)):
        r = autocorrelation_ess(x)
        assert np.isnan(r["n_eff"]) and r["cap_bound"] is False and r["lag_cap"] == 0


def test_multichain_copy_agrees_and_reports_cap_bound():
    """simulation_multichain_ensemble.py keeps its own copy (size_matched_results.py
    executes it from source); both must agree and both must report cap_bound."""
    src = (ROOT / "analysis" / "scripts" / "simulation_multichain_ensemble.py").read_text(encoding="utf-8")
    start = src.index("def autocorrelation_ess")
    ns = {"np": np}
    exec(src[start:src.index("\ndef ", start + 10)], ns)  # the extraction size_matched_results.py uses
    other = ns["autocorrelation_ess"]
    for x, lag in ((_ar1(5_000, 0.5, seed=3), None), (_ar1(5_000, 0.99, seed=4), 50)):
        a, b = autocorrelation_ess(x, max_lag=lag), other(x, max_lag=lag)
        assert a["n_eff"] == pytest.approx(b["n_eff"], rel=1e-12)
        assert a["cap_bound"] == b["cap_bound"]
        assert a["lag_cap"] == b["lag_cap"]
    assert other(_ar1(5_000, 0.99, seed=4), max_lag=50)["cap_bound"] is True


# ── packing_cracking_analysis: fractional votes are kept ─────────────────────

def test_va_votes_are_not_truncated_by_default():
    from packing_cracking_analysis import _prepare_va_votes

    raw = pd.DataFrame({"va_ndp": [58.0, 132.5, np.nan, 0.5], "va_ucp": [14.5, 0.25, 7.0, np.nan]})
    kept = _prepare_va_votes(raw.copy())
    assert kept["va_ndp"].tolist() == [58.0, 132.5, 0.0, 0.5]
    assert kept["va_ucp"].tolist() == [14.5, 0.25, 7.0, 0.0]
    assert kept["va_ndp"].sum() == pytest.approx(191.0)

    legacy = _prepare_va_votes(raw.copy(), legacy_int_votes=True)
    assert legacy["va_ndp"].tolist() == [58, 132, 0, 0]
    assert legacy["va_ucp"].tolist() == [14, 0, 7, 0]
    assert legacy["va_ndp"].sum() < kept["va_ndp"].sum()


def test_spatial_join_scorer_truncation_is_optional():
    """score_map_by_spatial_join truncates district totals by default (what its
    other callers' committed outputs were produced with) and keeps fractions
    when asked."""
    import geopandas as gpd
    from shapely.geometry import box

    import packing_cracking_analysis as pca

    va = gpd.GeoDataFrame(
        {"va_ndp": [10.5, 20.25, 5.5], "va_ucp": [1.75, 2.5, 3.5]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(2, 0, 3, 1)], crs="EPSG:3400",
    )
    eds = gpd.GeoDataFrame({"name": ["West", "East"]}, geometry=[box(0, 0, 2, 1), box(2, 0, 3, 1)], crs="EPSG:3400")
    real_read = gpd.read_file
    gpd.read_file = lambda *a, **k: eds.copy()
    try:
        truncated = {r["ed"]: r for r in pca.score_map_by_spatial_join(va, Path("unused.gpkg"), "name")}
        exact = {r["ed"]: r for r in pca.score_map_by_spatial_join(
            va, Path("unused.gpkg"), "name", truncate_district_totals=False)}
    finally:
        gpd.read_file = real_read
    assert (truncated["West"]["ndp"], truncated["West"]["ucp"]) == (30, 4)
    assert (exact["West"]["ndp"], exact["West"]["ucp"]) == (30.75, 4.25)
    assert (exact["East"]["ndp"], exact["East"]["ucp"]) == (5.5, 3.5)


# ── third_party_sensitivity: "other" comes from total_valid_votes ────────────

def test_third_party_other_votes_use_total_valid(tmp_path):
    """A division whose candidate columns omit a candidate (as three do in the
    committed CSV) still gets its full third-party vote."""
    import third_party_sensitivity as tps

    csv = tmp_path / "results.csv"
    csv.write_text(
        "ed_name,region,cand_1,cand_2,cand_3,cand_4,cand_5,cand_6,"
        "votes_1,votes_2,votes_3,votes_4,votes_5,votes_6,total_valid_votes\n"
        "Full,Calgary,A (NDP),B (UCP),C (GPA),,,,100,200,30,,,,330\n"
        "Short,Edmonton,A (NDP),B (UCP),,,,,400,300,,,,,713\n",
        encoding="utf-8",
    )
    rows = {r["ed"]: r for r in tps.load_with_other(csv)}
    assert (rows["Full"]["ndp"], rows["Full"]["ucp"], rows["Full"]["other"]) == (100, 200, 30)
    assert rows["Short"]["other"] == 13  # not 0: the omitted candidate's 13 votes

    bad = tmp_path / "bad.csv"
    bad.write_text(
        "ed_name,region,cand_1,cand_2,cand_3,votes_1,votes_2,votes_3,total_valid_votes\n"
        "Bad,Calgary,A (NDP),B (UCP),C (GPA),100,200,30,300\n", encoding="utf-8")
    with pytest.raises(Exception):
        tps.load_with_other(bad)


def test_third_party_total_on_committed_csv():
    """58,611 other votes on the committed file (58,232 from the candidate columns alone)."""
    import third_party_sensitivity as tps

    rows = tps.load_with_other()
    assert len(rows) == 87
    assert sum(r["ndp"] for r in rows) == 777_404
    assert sum(r["ucp"] for r in rows) == 928_900
    assert sum(r["other"] for r in rows) == 58_611


# ── run_audit.py: checks 3 and 4 test the name column ────────────────────────

def _run_audit_functions() -> dict:
    """run_audit.py is a script that runs on import; pull out its helper
    functions and constants without executing the audit."""
    tree = ast.parse((ROOT / "run_audit.py").read_text(encoding="utf-8"))
    keep = [n for n in tree.body
            if isinstance(n, ast.FunctionDef)
            or (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "NAME_COLUMNS")]
    ns: dict = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), "run_audit.py", "exec"), ns)
    return ns


def test_run_audit_name_checks_use_the_official_name_column():
    ns = _run_audit_functions()
    official = pd.DataFrame({"EDNum2025": [1, 2, 3], "EDName2025": ["A", "B", "B "], "PopCensus": [1, 2, 3]})
    assert ns["name_column"](official) == "EDName2025"
    # a duplicate name is caught even though the district numbers are unique
    assert ns["duplicate_names"](official) == {"B": 2}
    blanks = pd.DataFrame({"EDNum2025": [1, 2, 3], "EDName2025": ["A", None, "  "]})
    assert ns["blank_names"](blanks) == (1, 1)
    clean = pd.DataFrame({"EDNum2025": [1, 2], "EDName2025": ["A", "B"]})
    assert ns["duplicate_names"](clean) == {} and ns["blank_names"](clean) == (0, 0)


def test_run_audit_name_checks_fail_without_a_name_column():
    ns = _run_audit_functions()
    no_names = pd.DataFrame({"EDNum2025": [1, 2], "PopCensus": [5, 6]})
    assert ns["name_column"](no_names) is None
    with pytest.raises(KeyError):
        ns["duplicate_names"](no_names)
    with pytest.raises(KeyError):
        ns["blank_names"](no_names)


# ── verify_joint_empirical_bound: notes come from computed values ────────────

def test_joint_verification_notes_are_built_from_values():
    import verify_joint_empirical_bound as v
    from scipy.stats import chi2

    for d2 in (7.7364, 13.1648, 33.6385):
        assert v.chi2_sf_df4(d2) == pytest.approx(chi2.sf(d2, 4), rel=1e-12)

    maps = {
        "minority": {"plans_at_or_beyond": 0, "empirical_tail_fraction": 0.0,
                     "parametric_chi2_4_p": v.chi2_sf_df4(33.6385)},
        "majority": {"plans_at_or_beyond": 102111, "empirical_tail_fraction": 0.1011,
                     "parametric_chi2_4_p": v.chi2_sf_df4(7.7364)},
        "enacted": {"plans_at_or_beyond": 12370, "empirical_tail_fraction": 0.01224752,
                    "parametric_chi2_4_p": v.chi2_sf_df4(13.1648)},
    }
    notes = " ".join(v.build_notes(maps, 4372.3, 3 / 4372.3, 1_010_000, any_cap_bound=False))
    assert "8.84e-07" in notes and "1.40e-06" not in notes
    assert "n_eff = 4,372" in notes and "6.86e-04" in notes
    assert "0.1017 parametric vs 0.1011 empirical" in notes
    assert "0.0105 vs 0.0122" in notes
    assert "lag cap" not in notes

    # the notes follow the inputs, not a literal
    maps["majority"]["empirical_tail_fraction"] = 0.2
    changed = " ".join(v.build_notes(maps, 1000.0, 3 / 1000.0, 1_010_000, any_cap_bound=True))
    assert "0.2000 empirical" in changed and "n_eff = 1,000" in changed and "3.00e-03" in changed
    assert "lag cap" in changed


# ── joint_outlier_score_canonical: Hotelling factor option ───────────────────

def test_hotelling_exact_factor_is_optional_and_default_unchanged():
    import joint_outlier_score_canonical as j
    from scipy import stats

    d, p, n = 5.7999, 4, 1413
    default_p, default_f = j.mahalanobis_pvalue_neff_adjusted(d, p, n_eff=n)
    assert default_f == pytest.approx((n - p) / (p * (n + 1)) * d * d, rel=1e-12)
    assert default_p == pytest.approx(1.11e-6, rel=5e-3)  # the published n_eff-adjusted figure
    exact_p, exact_f = j.mahalanobis_pvalue_neff_adjusted(d, p, n_eff=n, exact_factor=True)
    assert exact_f == pytest.approx((n - p) * n / (p * (n - 1) * (n + 1)) * d * d, rel=1e-12)
    assert exact_p == pytest.approx(float(stats.f.sf(exact_f, p, n - p)), rel=1e-12)
    assert exact_p < default_p and exact_p == pytest.approx(default_p, rel=0.02)


# ── drain_phase_b_canonical: (b+1)/(B+1) and the recorded seed ───────────────

def test_drain_null_p_values():
    import drain_phase_b_canonical as d

    null = np.arange(1, 10_001) / 1e4
    lowest = d.two_tailed_p(null, 0.0)          # no draw as low as the observed score
    assert lowest["p_two_tailed"] == 0.0
    assert lowest["p_two_tailed_plus_one"] == pytest.approx(2 / 10_001)
    one = d.two_tailed_p(null, 1e-4)            # one draw at or below
    assert one["p_two_tailed"] == pytest.approx(0.0002)
    assert one["p_two_tailed_plus_one"] == pytest.approx(4 / 10_001)
    middle = d.two_tailed_p(null, 0.5)
    assert middle["p_two_tailed"] == 1.0 and middle["p_two_tailed_plus_one"] == 1.0


def test_drain_committed_output_seed_is_recorded():
    """The committed JSON's seed is the constant the script documents."""
    import json

    import drain_phase_b_canonical as d

    committed = json.loads((ROOT / "findings" / "drain_label_shuffle_null_canonical.json").read_text(encoding="utf-8"))
    assert committed["seed"] == d.COMMITTED_OUTPUT_SEED == 460508741
    assert committed["salt"] == d.SALT


# ── szat: the registered p is one-tailed in effect ───────────────────────────

def test_szat_centred_two_sided_p():
    import szat

    rng = np.random.default_rng(0)
    null = 0.02 + 0.008 * rng.standard_normal(10_000)   # centred near half the observed score
    observed = 0.04
    b_registered = int((np.abs(null) >= abs(observed)).sum())
    p_centred, b_centred = szat.centred_two_sided_p(null, observed)
    assert int((null <= -observed).sum()) == 0            # the lower region is unreachable
    assert b_centred >= b_registered                      # the centred test also counts the low tail
    assert p_centred == pytest.approx((b_centred + 1) / 10_001)

    samples = ROOT / "data" / "szat_bootstrap_eg_samples.npy"
    if samples.exists():
        eg_maj, eg_min = 0.0009823668405000681, 0.04019385991913548
        scores = np.load(samples) - eg_maj
        score = eg_min - eg_maj
        assert int((np.abs(scores) >= abs(score)).sum()) == 24     # the registered count
        assert int((scores <= -score).sum()) == 0
        p, b = szat.centred_two_sided_p(scores, score)
        assert b == 134 and p == pytest.approx(135 / 10_001)


# ── lfs_guard ────────────────────────────────────────────────────────────────

def test_lfs_guard_detects_pointers_and_missing_files(tmp_path):
    sys.path.insert(0, str(ROOT / "tests"))
    from lfs_guard import first_unavailable, unavailable_reason

    real = tmp_path / "real.gpkg"
    real.write_bytes(b"SQLite format 3\x00" + b"\x00" * 100)
    pointer = tmp_path / "pointer.gpkg"
    pointer.write_text("version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 5\n", encoding="utf-8")
    assert unavailable_reason(real) is None
    assert "Git LFS pointer" in unavailable_reason(pointer)
    assert "not present" in unavailable_reason(tmp_path / "absent.gpkg")
    assert first_unavailable(real) is None
    assert first_unavailable(real, pointer) == unavailable_reason(pointer)


# ── check_provenance: a missing listed file fails ────────────────────────────

def test_check_provenance_fails_on_a_missing_file(tmp_path):
    import hashlib
    import json

    import check_provenance as cp

    good = tmp_path / "outputs" / "good.json"
    good.parent.mkdir()
    good.write_text('{"a": 1}\n', encoding="utf-8")
    sha = hashlib.sha256(good.read_bytes()).hexdigest()
    manifest = tmp_path / "manifest.json"

    manifest.write_text(json.dumps({"outputs/good.json": {"sha256": sha}}), encoding="utf-8")
    assert cp.verify_provenance(manifest) is True

    manifest.write_text(json.dumps({"outputs/good.json": {"sha256": sha},
                                    "outputs/gone.json": {"sha256": "0" * 64}}), encoding="utf-8")
    with pytest.raises(SystemExit):
        cp.verify_provenance(manifest)
    assert cp.verify_provenance(manifest, allow_missing=True) is True

    manifest.write_text(json.dumps({"outputs/good.json": {"sha256": "0" * 64}}), encoding="utf-8")
    with pytest.raises(SystemExit):
        cp.verify_provenance(manifest)

    pointer = tmp_path / "outputs" / "big.gpkg"
    pointer.write_text("version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 5\n", encoding="utf-8")
    manifest.write_text(json.dumps({"outputs/big.gpkg": {"sha256": "0" * 64}}), encoding="utf-8")
    assert cp.verify_provenance(manifest) is True  # skipped, not failed


def test_committed_provenance_manifest_passes():
    import check_provenance as cp

    assert cp.verify_provenance(ROOT / "data" / "provenance_manifest.json") is True


# ── submission_sentiment_llm_full: failures are not marked done ──────────────

def test_llm_scan_failed_call_is_not_recorded_as_done():
    import submission_sentiment_llm_full as m

    kind, row = m.record_outcome("EBC-2025-2-0001", {}, 0, "2026-01-01T00:00:00")
    assert kind == "failure" and "rows_emitted" not in row
    kind, row = m.record_outcome("EBC-2025-2-0002", {"cfg": {"classification": "Unrelated"}}, 0, "t")
    assert kind == "progress" and row["rows_emitted"] == 0
    assert m.FAILURES_CSV != m.PROGRESS_CSV


# ── generate_report_numbers: the neutral envelope comes from the chains ──────

def test_neutral_seat_envelope_reads_chain_files(tmp_path):
    import generate_report_numbers as g

    (tmp_path / "chain0_samples.csv").write_text("seats_at_50_50,chain\n0.4,0\n0.5,0\n", encoding="utf-8")
    (tmp_path / "chain1_samples.csv").write_text("seats_at_50_50,chain\n0.45,1\n", encoding="utf-8")
    assert g.neutral_seat_envelope(tmp_path) == {
        "neutral_envelope_low": "40.00%", "neutral_envelope_high": "50.00%", "neutral_median_seats": "45.00%"}
    # with no chain files the fallback literals are the committed ensemble's values
    assert g.neutral_seat_envelope(tmp_path / "none")["neutral_envelope_high"] == "51.72%"


# ── build_va_pop: the committed population weights are reproducible ──────────

def test_va_population_file_is_reproduced_by_its_build_script():
    """data/va_pop_from_das.csv, the population every ensemble balances on,
    is reproduced by analysis/scripts/build_va_pop.py (about 8 s; needs two
    Git LFS files and skips without them)."""
    sys.path.insert(0, str(ROOT / "tests"))
    from lfs_guard import first_unavailable

    import build_va_pop as b

    reason = first_unavailable(b.DA_GPKG, b.VA_GPKG, b.DA_POP, b.OUT)
    if reason:
        pytest.skip(reason)
    built = b.build()
    assert len(built) == 4765
    assert b.compare(built) < b.TOLERANCE
    assert built["pop_2021"].sum() == pytest.approx(4_262_567.24, abs=0.01)
    # the second copy under data/outputs/ is the same file
    assert (ROOT / "data" / "outputs" / "va_pop_from_das.csv").read_bytes() == b.OUT.read_bytes()
