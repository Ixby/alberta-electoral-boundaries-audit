"""Tests for canonical seed reproducibility and joint outlier score functions.

Phase B: drand_seed.py — the pre-registered MCMC seed.
Phase D: joint_outlier_score_canonical.py — Mahalanobis, Fisher, and percentile
         functions used to produce the composite duck score.

These tests confirm the canonical calling convention (id_col='EDName2025') and
that the joint outlier math is correct against synthetic distributions.

Run from the repo root:
    python -m pytest tests/test_drand_and_canonical.py -v
"""

import sys
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from drand_seed import get_canonical_seed
from joint_outlier_score_canonical import (
    N_EFF_CONSERVATIVE,
    ensemble_marginal_percentile,
    fisher_combine,
    mahalanobis_pvalue,
    mahalanobis_pvalue_neff_adjusted,
)


# ============================================================
# Phase B: drand_seed — canonical seed determinism
# ============================================================


def test_drand_seed_deterministic():
    """Same salt always returns the same seed."""
    assert get_canonical_seed("chain-0") == get_canonical_seed("chain-0")


def test_drand_seed_in_32bit_range():
    """Seed must be a valid 32-bit unsigned integer."""
    seed = get_canonical_seed("")
    assert isinstance(seed, int)
    assert 0 <= seed < 2**32


def test_drand_seed_different_salts_differ():
    """Distinct salts produce distinct seeds."""
    assert get_canonical_seed("chain-0") != get_canonical_seed("chain-1")


def test_drand_seed_empty_and_nonempty_differ():
    """Empty salt and any non-empty salt must produce different seeds."""
    assert get_canonical_seed("") != get_canonical_seed("szat-bootstrap")


def test_drand_seed_szat_bootstrap_stable():
    """The SZAT bootstrap seed is pre-registered and must not change."""
    s1 = get_canonical_seed("szat-bootstrap")
    s2 = get_canonical_seed("szat-bootstrap")
    assert s1 == s2
    assert 0 <= s1 < 2**32


def test_drand_seed_canonical_round_constant():
    """The canonical drand round must match the pre-registered value."""
    from drand_seed import CANONICAL_ROUND
    assert CANONICAL_ROUND == 5500000


# ============================================================
# Phase B: score_exogenous_map canonical id_col convention
# ============================================================


def test_score_exogenous_map_accepts_edname2025():
    """score_exogenous_map must work with id_col='EDName2025' (canonical call)."""
    import geopandas as gpd
    from shapely.geometry import Point, Polygon

    from mcmc_ensemble import score_exogenous_map

    va = gpd.GeoDataFrame(
        {
            "va_ucp": [60.0],
            "va_ndp": [40.0],
            "va_other": [0.0],
            "total_votes": [100.0],
        },
        geometry=[Point(5, 5).buffer(0.5)],
        crs="EPSG:3401",
    )
    proposed = gpd.GeoDataFrame(
        {"EDName2025": ["TestED-A"]},
        geometry=[Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])],
        crs="EPSG:3401",
    )
    with tempfile.TemporaryDirectory() as td:
        gpkg = Path(td) / "canonical.gpkg"
        proposed.to_file(gpkg, driver="GPKG")
        result = score_exogenous_map(va, gpkg, id_col="EDName2025")

    assert result["coverage_vas"] == 1
    assert result["coverage_pct"] == pytest.approx(1.0)


# ============================================================
# Phase D: mahalanobis_pvalue
# ============================================================


def test_mahalanobis_at_mean_has_distance_near_zero():
    """Observed point at the ensemble mean → Mahalanobis distance ≈ 0, p ≈ 1."""
    rng = np.random.default_rng(42)
    data = rng.standard_normal((2000, 2))
    df = pd.DataFrame(data, columns=["a", "b"])
    obs = {"a": float(data[:, 0].mean()), "b": float(data[:, 1].mean())}
    d, p, _ = mahalanobis_pvalue(df, obs, ["a", "b"])
    assert d < 0.1
    assert p > 0.80


def test_mahalanobis_extreme_outlier_has_small_p():
    """Point 8 sigma from mean → p ≈ 0."""
    rng = np.random.default_rng(42)
    data = rng.standard_normal((2000, 2))
    df = pd.DataFrame(data, columns=["a", "b"])
    obs = {"a": 8.0, "b": 8.0}
    _, p, _ = mahalanobis_pvalue(df, obs, ["a", "b"])
    assert p < 0.001


def test_mahalanobis_returns_mean_vector():
    """Third return value must be the column means of the ensemble."""
    rng = np.random.default_rng(42)
    data = rng.standard_normal((1000, 2))
    df = pd.DataFrame(data, columns=["x", "y"])
    _, _, mu = mahalanobis_pvalue(df, {"x": 0.0, "y": 0.0}, ["x", "y"])
    assert abs(mu[0] - data[:, 0].mean()) < 1e-10
    assert abs(mu[1] - data[:, 1].mean()) < 1e-10


# ============================================================
# Phase D: mahalanobis_pvalue_neff_adjusted (Hotelling T²)
# ============================================================


def test_neff_adjusted_more_conservative_than_chi2():
    """Hotelling T² p-value must be >= chi-squared p-value at same distance."""
    rng = np.random.default_rng(42)
    data = rng.standard_normal((2000, 4))
    df = pd.DataFrame(data, columns=["a", "b", "c", "d"])
    obs = {"a": 2.5, "b": 2.5, "c": 2.5, "d": 2.5}
    d, p_chi2, _ = mahalanobis_pvalue(df, obs, ["a", "b", "c", "d"])
    p_adj, _ = mahalanobis_pvalue_neff_adjusted(d, p_metrics=4, n_eff=N_EFF_CONSERVATIVE)
    assert p_adj >= p_chi2


def test_neff_adjusted_converges_to_chi2_at_large_n():
    """As n_eff → ∞ the Hotelling adjustment converges to chi-squared."""
    d = 3.0
    p_adj_large, _ = mahalanobis_pvalue_neff_adjusted(d, p_metrics=4, n_eff=1_000_000)
    from scipy import stats
    p_chi2 = float(stats.chi2.sf(d**2, df=4))
    assert abs(p_adj_large - p_chi2) < 0.001


# ============================================================
# Phase D: ensemble_marginal_percentile
# ============================================================


def test_marginal_percentile_uniform_upper_tail():
    """Uniform[0,1]: upper-tail percentile at 0.9 ≈ 0.10."""
    rng = np.random.default_rng(42)
    df = pd.DataFrame({"x": rng.uniform(0, 1, 20_000)})
    pct = ensemble_marginal_percentile(df, "x", 0.9, upper_tail=True)
    assert abs(pct - 0.10) < 0.02


def test_marginal_percentile_uniform_lower_tail():
    """Uniform[0,1]: lower-tail percentile at 0.1 ≈ 0.10."""
    rng = np.random.default_rng(42)
    df = pd.DataFrame({"x": rng.uniform(0, 1, 20_000)})
    pct = ensemble_marginal_percentile(df, "x", 0.1, upper_tail=False)
    assert abs(pct - 0.10) < 0.02


def test_marginal_percentile_at_max_is_zero():
    """Observed value at or above max of ensemble → upper-tail p ≈ 0."""
    df = pd.DataFrame({"x": np.arange(1000, dtype=float)})
    pct = ensemble_marginal_percentile(df, "x", 999.0, upper_tail=True)
    assert pct <= 1 / 1000 + 1e-9


# ============================================================
# Phase D: fisher_combine
# ============================================================


def test_fisher_combine_two_weak_signals():
    """Two p=0.1 tests: combined p should be smaller than either individual p."""
    _, p_combined = fisher_combine([0.1, 0.1])
    assert p_combined < 0.1


def test_fisher_combine_two_strong_signals():
    """Two p=0.01 tests: combined p much smaller than 0.01."""
    _, p_combined = fisher_combine([0.01, 0.01])
    assert p_combined < 0.005


def test_fisher_combine_returns_statistic_and_pvalue():
    """Return value is (T, p) where T > 0 and 0 < p <= 1."""
    T, p = fisher_combine([0.05, 0.05])
    assert T > 0
    assert 0 < p <= 1


def test_fisher_combine_null_results_remain_non_significant():
    """Two p=0.5 tests: combined p should still be > 0.05."""
    _, p_combined = fisher_combine([0.5, 0.5])
    assert p_combined > 0.05


def test_fisher_combine_four_channels_matches_formula():
    """Verify Fisher statistic: T = -2 * sum(ln(p_i))."""
    p_vals = [0.05, 0.10, 0.20, 0.30]
    T, _ = fisher_combine(p_vals)
    expected_T = -2.0 * sum(np.log(p) for p in p_vals)
    assert abs(T - expected_T) < 1e-10
