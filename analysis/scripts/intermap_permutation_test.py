"""
intermap_permutation_test.py
----------------------------
Permutation test for the directional inter-map partisan-bias claim.

Tests whether the minority and majority commission proposals differ in their
joint partisan-metric position by more than randomly drawn pairs of constraint-
legal neutral maps from the canonical MCMC ensemble.

Two versions:

  Version A (EG-only, one-tailed):
    T_A = EG(minority) - EG(majority)
    Null distribution: {EG(i) - EG(j)} for N_PAIRS random ordered pairs
    p = P(EG_diff >= T_A) over random pairs — one-tailed, direction pre-specified
    Prediction before running: likely does not reach p < 0.05. Ensemble EG SD
    is ~1-2 pp in an 89-seat system, so the typical |random-pair EG gap| of
    sqrt(2)*SD exceeds the 1.42 pp observed difference.

  Version B (Mahalanobis joint, one-tailed in distance):
    T_B = sqrt((v_min - v_maj)^T Sigma^{-1} (v_min - v_maj))
    where v = [efficiency_gap, mean_median, declination, seats_at_50_50]
    and Sigma is the ensemble covariance matrix.
    Null distribution: {D(i, j)} for N_PAIRS random pairs
    p = P(D_pair >= T_B) over random pairs — uses all 4 partisan metrics jointly.
    More powerful than Version A; direction is post-hoc verified (all 4 metrics
    should show minority more UCP-favorable for the vector to be interpretable).

EG sign convention (per szat.py, McGhee / Stephanopoulos 2014):
  positive EG = more NDP votes wasted than UCP (UCP structural advantage)
  T_A = EG(minority) - EG(majority) > 0 means minority is more UCP-favorable

Pre-registration: OSF yvc7g (https://osf.io/yvc7g), committed at git ba0e686.
See TODO.md "Inter-Map Comparison Permutation Test (Ch1-COMP)" for full spec.

Backward dependencies:
  data/simulated_ensemble_raw_samples_canonical.csv
  data/simulation_real_map_scores_canonical.json

Forward dependencies:
  analysis/reports/intermap_permutation_test_results.json
  analysis/reports/intermap_permutation_test_results.md
"""

from __future__ import annotations

import json
import logging
import sys
import warnings
from pathlib import Path

try:
    import data_loader
    from canonical_manifest import verify_canonical_files
    from drand_seed import get_canonical_seed, CANONICAL_ROUND, CANONICAL_RANDOMNESS
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import data_loader
    from canonical_manifest import verify_canonical_files
    from drand_seed import get_canonical_seed, CANONICAL_ROUND, CANONICAL_RANDOMNESS

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
REPORTS = ROOT / "analysis" / "reports"

ENSEMBLE_CSV = DATA / "simulated_ensemble_raw_samples_canonical.csv"
REAL_SCORES  = DATA / "simulation_real_map_scores_canonical.json"
OUT_JSON     = REPORTS / "intermap_permutation_test_results.json"
OUT_MD       = REPORTS / "intermap_permutation_test_results.md"

PARTISAN_COLS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]

# Keys in simulation_real_map_scores_canonical.json
_MINORITY_KEY = "minority_2026"
_MAJORITY_KEY = "majority_2026"

N_PAIRS = 10_000

# RNG seed derived from Cloudflare League of Entropy drand beacon, round 5500000,
# salt "ch1-comp". Verifiable at https://drand.cloudflare.com/public/5500000.
# Derived seed: SHA256(randomness_hex + "ch1-comp")[:4] = 0x6cb0fce5 = 1823538405.
_DRAND_SALT = "ch1-comp"
RNG_SEED = get_canonical_seed(_DRAND_SALT)  # 1823538405


# ── Core statistics ───────────────────────────────────────────────────────────

def _build_covariance(X: np.ndarray) -> np.ndarray:
    """Ensemble covariance (columns = metrics). Uses pseudoinverse for stability."""
    return np.cov(X, rowvar=False)


def _mahalanobis_distance(d: np.ndarray, cov_inv: np.ndarray) -> float:
    """Mahalanobis norm of difference vector d under precision matrix cov_inv."""
    return float(np.sqrt(d @ cov_inv @ d))


def run_version_a(
    ensemble_eg: np.ndarray,
    t_obs: float,
    rng: np.random.Generator,
) -> dict:
    """
    EG-only one-tailed permutation test.

    H0: minority - majority EG <= typical random-pair EG gap
    H1: minority - majority EG > 95th percentile of random-pair gaps (one-tailed)

    Null constructed by sampling N_PAIRS random pairs from the ensemble and
    computing EG(i) - EG(j) with random ordering. The null is symmetric around 0
    by construction; p_one_tailed = P(diff >= t_obs).
    """
    n = len(ensemble_eg)
    idx_i = rng.integers(0, n, size=N_PAIRS)
    idx_j = rng.integers(0, n, size=N_PAIRS)

    diffs = ensemble_eg[idx_i] - ensemble_eg[idx_j]  # random ordering → symmetric null

    p_one_tailed = float(np.mean(diffs >= t_obs))
    p_two_tailed = float(np.mean(np.abs(diffs) >= abs(t_obs)))

    null_sd   = float(np.std(diffs))
    null_p95  = float(np.percentile(diffs, 95))
    null_p025 = float(np.percentile(diffs, 2.5))
    null_p975 = float(np.percentile(diffs, 97.5))
    z_obs     = t_obs / null_sd if null_sd > 0 else float("nan")

    return {
        "observed_eg_diff_pp": round(t_obs * 100, 4),
        "null_sd_pp": round(null_sd * 100, 4),
        "null_p95_pp": round(null_p95 * 100, 4),
        "null_95pct_interval_pp": [round(null_p025 * 100, 4), round(null_p975 * 100, 4)],
        "z_score": round(z_obs, 4),
        "p_one_tailed": round(p_one_tailed, 6),
        "p_two_tailed": round(p_two_tailed, 6),
        "n_pairs": N_PAIRS,
        "significant_at_005_one_tailed": p_one_tailed < 0.05,
        "significant_at_005_two_tailed": p_two_tailed < 0.05,
        "interpretation": (
            f"Observed minority-majority EG gap = {t_obs*100:+.2f} pp. "
            f"Null 95th percentile = {null_p95*100:.2f} pp. "
            f"One-tailed p = {p_one_tailed:.4f}."
        ),
    }


def run_version_b(
    X: np.ndarray,
    v_min: np.ndarray,
    v_maj: np.ndarray,
    rng: np.random.Generator,
) -> dict:
    """
    Mahalanobis joint one-tailed permutation test (all 4 partisan metrics).

    H0: ||Sigma^{-1/2}(v_min - v_maj)|| <= typical random-pair Mahalanobis distance
    H1: T_B > 95th percentile of random-pair Mahalanobis distances

    Null: Mahalanobis distance between N_PAIRS random pairs, using ensemble
    covariance Sigma. This is always non-negative, so the test is one-tailed
    in distance (equivalent to a two-tailed directional test in metric space).
    """
    cov     = _build_covariance(X)
    cov_inv = np.linalg.pinv(cov)

    d_obs = v_min - v_maj
    t_obs = _mahalanobis_distance(d_obs, cov_inv)

    n = len(X)
    idx_i = rng.integers(0, n, size=N_PAIRS)
    idx_j = rng.integers(0, n, size=N_PAIRS)

    null_dists = np.array([
        _mahalanobis_distance(X[i] - X[j], cov_inv)
        for i, j in zip(idx_i, idx_j)
    ])

    p = float(np.mean(null_dists >= t_obs))
    null_p95  = float(np.percentile(null_dists, 95))
    null_mean = float(np.mean(null_dists))
    null_sd   = float(np.std(null_dists))

    # Per-metric breakdown: direction check
    metric_deltas = {
        col: {
            "minority": round(float(v_min[i]), 6),
            "majority": round(float(v_maj[i]), 6),
            "delta": round(float(d_obs[i]), 6),
            "minority_more_ucp_favorable": bool(d_obs[i] > 0),
        }
        for i, col in enumerate(PARTISAN_COLS)
    }
    n_metrics_same_direction = sum(
        1 for v in metric_deltas.values() if v["minority_more_ucp_favorable"]
    )

    return {
        "observed_mahalanobis_distance": round(t_obs, 6),
        "null_mean_distance": round(null_mean, 6),
        "null_sd_distance": round(null_sd, 6),
        "null_p95_distance": round(null_p95, 6),
        "p_one_tailed": round(p, 6),
        "significant_at_005": p < 0.05,
        "n_pairs": N_PAIRS,
        "metrics_minority_more_ucp_favorable": n_metrics_same_direction,
        "metric_deltas": metric_deltas,
        "interpretation": (
            f"Observed inter-map Mahalanobis distance = {t_obs:.4f}. "
            f"Null 95th percentile = {null_p95:.4f}. "
            f"p = {p:.4f}. "
            f"{n_metrics_same_direction}/4 metrics point minority more UCP-favorable."
        ),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def run() -> None:
    verify_canonical_files()

    print("Loading ensemble...")
    ensemble = pd.read_csv(ENSEMBLE_CSV)
    missing  = [c for c in PARTISAN_COLS if c not in ensemble.columns]
    if missing:
        raise ValueError(f"Ensemble CSV missing columns: {missing}")
    X = ensemble[PARTISAN_COLS].dropna().values
    print(f"  {len(X):,} rows x {len(PARTISAN_COLS)} metrics")

    print("Loading real map scores...")
    with open(REAL_SCORES) as f:
        real = json.load(f)
    if _MINORITY_KEY not in real or _MAJORITY_KEY not in real:
        raise ValueError(
            f"Real map scores JSON missing '{_MINORITY_KEY}' or '{_MAJORITY_KEY}'. "
            f"Keys present: {list(real.keys())}"
        )
    v_min = np.array([real[_MINORITY_KEY][c] for c in PARTISAN_COLS])
    v_maj = np.array([real[_MAJORITY_KEY][c] for c in PARTISAN_COLS])

    eg_col  = PARTISAN_COLS.index("efficiency_gap")
    eg_min  = v_min[eg_col]
    eg_maj  = v_maj[eg_col]
    t_a_obs = eg_min - eg_maj  # positive = minority more UCP-favorable

    print(f"\nObserved values:")
    for i, col in enumerate(PARTISAN_COLS):
        print(f"  {col:20}  minority={v_min[i]:+.6f}  majority={v_maj[i]:+.6f}  delta={v_min[i]-v_maj[i]:+.6f}")
    print(f"\n  EG sign convention: positive = UCP structural advantage")
    print(f"  T_A (EG diff) = {t_a_obs*100:+.4f} pp")

    rng = np.random.default_rng(RNG_SEED)

    print(f"\nRunning Version A (EG-only, {N_PAIRS:,} pairs)...")
    result_a = run_version_a(X[:, eg_col], t_a_obs, rng)
    sig_a = "SIGNIFICANT" if result_a["significant_at_005_one_tailed"] else "not significant"
    print(f"  p (one-tailed) = {result_a['p_one_tailed']:.4f}  [{sig_a} at p<0.05]")
    print(f"  Null 95th pct  = {result_a['null_p95_pp']:+.2f} pp  (observed = {result_a['observed_eg_diff_pp']:+.2f} pp)")

    print(f"\nRunning Version B (Mahalanobis joint, {N_PAIRS:,} pairs)...")
    result_b = run_version_b(X, v_min, v_maj, rng)
    sig_b = "SIGNIFICANT" if result_b["significant_at_005"] else "not significant"
    print(f"  p              = {result_b['p_one_tailed']:.4f}  [{sig_b} at p<0.05]")
    print(f"  Null 95th pct  = {result_b['null_p95_distance']:.4f}  (observed = {result_b['observed_mahalanobis_distance']:.4f})")
    print(f"  Direction check: {result_b['metrics_minority_more_ucp_favorable']}/4 metrics show minority more UCP-favorable")

    # ── Contextual comparison: each map's individual Mahalanobis distance ─────
    mu  = X.mean(axis=0)
    cov = np.cov(X, rowvar=False)
    cov_inv = np.linalg.pinv(cov)

    d_min_vs_null = v_min - mu
    d_maj_vs_null = v_maj - mu
    D_min = _mahalanobis_distance(d_min_vs_null, cov_inv)
    D_maj = _mahalanobis_distance(d_maj_vs_null, cov_inv)
    p_min_chi2 = float(stats.chi2.sf(D_min ** 2, df=len(PARTISAN_COLS)))
    p_maj_chi2 = float(stats.chi2.sf(D_maj ** 2, df=len(PARTISAN_COLS)))

    context = {
        "minority_vs_ensemble": {
            "mahalanobis_distance": round(D_min, 4),
            "p_chi2": round(p_min_chi2, 8),
            "note": "Ch1 result (minority absolute position vs neutral ensemble)",
        },
        "majority_vs_ensemble": {
            "mahalanobis_distance": round(D_maj, 4),
            "p_chi2": round(p_maj_chi2, 8),
            "note": "Ch1 result (majority absolute position vs neutral ensemble)",
        },
        "intermap_distance": {
            "mahalanobis_distance": result_b["observed_mahalanobis_distance"],
            "p": result_b["p_one_tailed"],
            "note": "Version B result (minority vs majority, comparison test)",
        },
    }

    print(f"\nContextual comparison:")
    print(f"  Minority vs ensemble:  D={D_min:.4f}  p={p_min_chi2:.2e}  (Ch1 absolute-position test)")
    print(f"  Majority vs ensemble:  D={D_maj:.4f}  p={p_maj_chi2:.2e}  (Ch1 absolute-position test)")
    print(f"  Minority vs majority:  D={result_b['observed_mahalanobis_distance']:.4f}  p={result_b['p_one_tailed']:.4f}  (Version B comparison test)")

    # ── Output ────────────────────────────────────────────────────────────────
    REPORTS.mkdir(parents=True, exist_ok=True)

    output = {
        "description": "Inter-map partisan-bias comparison permutation test",
        "n_pairs": N_PAIRS,
        "rng_seed": RNG_SEED,
        "rng_provenance": {
            "source": "Cloudflare League of Entropy drand beacon",
            "round": CANONICAL_ROUND,
            "randomness_hex": CANONICAL_RANDOMNESS,
            "salt": _DRAND_SALT,
            "derived_seed": RNG_SEED,
            "verify_url": f"https://drand.cloudflare.com/public/{CANONICAL_ROUND}",
            "note": "SHA256(randomness_hex + salt)[:4] as uint32. Pre-dates analysis run.",
        },
        "ensemble_n": len(X),
        "partisan_cols": PARTISAN_COLS,
        "minority_key": _MINORITY_KEY,
        "majority_key": _MAJORITY_KEY,
        "eg_sign_convention": "positive = more NDP wasted (UCP structural advantage); per szat.py",
        "hypothesis": {
            "H0": (
                "The minority-majority commission proposals differ in their partisan-metric "
                "position by no more than randomly drawn pairs of neutral constraint-legal maps."
            ),
            "H1": (
                "The minority-majority gap exceeds the 95th percentile of random-pair distances "
                "(one-tailed, direction pre-specified: minority more UCP-favorable)."
            ),
            "pre_commitment": "Report regardless of direction per TODO.md Ch1-COMP specification.",
        },
        "version_a_eg_only": result_a,
        "version_b_mahalanobis_joint": result_b,
        "context_absolute_positions": context,
        "verdict": _make_verdict(result_a, result_b),
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=float)

    _write_md(output, result_a, result_b, context, D_min, p_min_chi2, D_maj, p_maj_chi2)

    print(f"\nResults written:")
    print(f"  {OUT_JSON}")
    print(f"  {OUT_MD}")


def _make_verdict(result_a: dict, result_b: dict) -> dict:
    sig_a = result_a["significant_at_005_one_tailed"]
    sig_b = result_b["significant_at_005"]

    if sig_a and sig_b:
        claim = "SUPPORTED at classical threshold on both versions."
        paper = (
            "The directional inter-map comparison reaches p < 0.05 on both the "
            "EG-only (Version A) and Mahalanobis joint (Version B) tests. Add to "
            "§5.4 as Ch1-COMP."
        )
    elif sig_b:
        claim = "SUPPORTED at classical threshold on Mahalanobis joint test (Version B) only."
        paper = (
            "The directional inter-map comparison reaches p < 0.05 on the "
            "Mahalanobis joint test (Version B) but not the EG-only test (Version A). "
            "Report Version B in §5.4 as Ch1-COMP; note Version A does not clear threshold."
        )
    elif sig_a:
        claim = "SUPPORTED at classical threshold on EG-only test (Version A) only."
        paper = (
            "Unexpected: EG-only test reaches p < 0.05 but Mahalanobis joint does not. "
            "Investigate before reporting — this outcome was not predicted and suggests "
            "the multi-metric signal may be diverging in direction."
        )
    else:
        claim = "NOT SUPPORTED at classical threshold on either version (pre-committed null result)."
        paper = (
            "Neither Version A nor Version B clears p < 0.05. Report as pre-committed null: "
            "the inter-map directional comparison does not reach classical significance given "
            "the 89-seat EG standard error. The partisan-difference claim rests on directional "
            "sensitivity consistency (lower bound > 0 across all draws) and on each map's "
            "individual ensemble position rather than a formally significant inter-map gap."
        )

    return {"claim": claim, "paper_impact": paper}


def _write_md(
    output: dict,
    result_a: dict,
    result_b: dict,
    context: dict,
    D_min: float,
    p_min: float,
    D_maj: float,
    p_maj: float,
) -> None:
    v = output["verdict"]
    sig_a_label = "**p < 0.05 — SIGNIFICANT**" if result_a["significant_at_005_one_tailed"] else f"p = {result_a['p_one_tailed']:.4f} — not significant"
    sig_b_label = "**p < 0.05 — SIGNIFICANT**" if result_b["significant_at_005"] else f"p = {result_b['p_one_tailed']:.4f} — not significant"

    metric_rows = ""
    for col, m in result_b["metric_deltas"].items():
        direction = "minority > majority (more UCP-favorable)" if m["minority_more_ucp_favorable"] else "majority > minority"
        metric_rows += (
            f"| {col} | {m['minority']:+.4f} | {m['majority']:+.4f} | "
            f"{m['delta']:+.4f} | {direction} |\n"
        )

    md = f"""# Inter-Map Comparison Permutation Test (Ch1-COMP)

**Script:** `analysis/scripts/intermap_permutation_test.py`
**Ensemble:** `simulated_ensemble_raw_samples_canonical.csv` ({output['ensemble_n']:,} plans)
**RNG seed:** {output['rng_seed']} (fixed; document in output for reproducibility)
**N pairs:** {output['n_pairs']:,}

---

## Hypotheses

**H₀:** The minority and majority commission proposals differ in their joint partisan-metric
position by no more than randomly drawn pairs of constraint-legal neutral maps.

**H₁:** The minority-majority gap exceeds the 95th percentile of random-pair distances
(one-tailed, direction pre-specified: minority more UCP-favorable).

**Pre-commitment:** Result reported regardless of direction per TODO.md Ch1-COMP specification.

---

## Version A — EG-Only (one-tailed)

| | Value |
|---|---|
| Observed EG(minority) − EG(majority) | {result_a['observed_eg_diff_pp']:+.2f} pp |
| Null SD (random pairs) | {result_a['null_sd_pp']:.2f} pp |
| Null 95th percentile | {result_a['null_p95_pp']:+.2f} pp |
| z-score | {result_a['z_score']:.3f} |
| **p (one-tailed)** | **{result_a['p_one_tailed']:.4f}** |
| p (two-tailed) | {result_a['p_two_tailed']:.4f} |
| Result | {sig_a_label} |

*EG sign convention: positive = more NDP votes wasted (UCP structural advantage).*

---

## Version B — Mahalanobis Joint (one-tailed in distance)

Metrics: efficiency\\_gap, mean\\_median, declination, seats\\_at\\_50\\_50.
Covariance matrix Σ estimated from the {output['ensemble_n']:,}-plan ensemble.

| | Value |
|---|---|
| Observed Mahalanobis distance | {result_b['observed_mahalanobis_distance']:.4f} |
| Null mean distance (random pairs) | {result_b['null_mean_distance']:.4f} |
| Null SD | {result_b['null_sd_distance']:.4f} |
| Null 95th percentile | {result_b['null_p95_distance']:.4f} |
| **p** | **{result_b['p_one_tailed']:.4f}** |
| Result | {sig_b_label} |

**Per-metric breakdown:**

| Metric | Minority | Majority | Delta | Direction |
|---|---|---|---|---|
{metric_rows}
{result_b['metrics_minority_more_ucp_favorable']}/4 metrics show minority more UCP-favorable.

---

## Contextual Comparison (Absolute Positions)

| Test | Map | Mahalanobis D | p |
|---|---|---|---|
| Ch1 (vs ensemble) | Minority | {D_min:.4f} | {p_min:.2e} |
| Ch1 (vs ensemble) | Majority | {D_maj:.4f} | {p_maj:.2e} |
| Ch1-COMP (vs each other) | Minority vs Majority | {result_b['observed_mahalanobis_distance']:.4f} | {result_b['p_one_tailed']:.4f} |

The Ch1 absolute-position result (minority p = {p_min:.2e}) remains the primary significance
finding. Ch1-COMP tests the *comparison* — whether the two maps differ more than random neutral
pairs, not whether either is an outlier in the ensemble.

---

## Verdict

**{v['claim']}**

{v['paper_impact']}

---

*Generated by `analysis/scripts/intermap_permutation_test.py`*
*Full output: `analysis/reports/intermap_permutation_test_results.json`*
"""

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md)


if __name__ == "__main__":
    run()
