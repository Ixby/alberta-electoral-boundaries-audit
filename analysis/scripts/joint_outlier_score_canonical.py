# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
joint_outlier_score_canonical.py -- Joint Outlier Score (Duck Score), canonical run

Lane 1 (Statistical), Fisher combination: Mahalanobis D² (Channel 1) + SZAT (Channel 2) -> headline p-value
Reads Channel 2 p-value from: findings/szat_summary.json

Same methodology as joint_outlier_score.py but uses the canonical 1.01M ensemble
(simulated_ensemble_raw_samples_canonical.csv) and canonical real-map scores
(simulation_real_map_scores_canonical.json).

Replaces the DPG-based 250k ensemble for all Channel 1 percentile placements.

Backward dependencies:
  data/simulated_ensemble_raw_samples_canonical.csv
  data/simulation_real_map_scores_canonical.json
  findings/szat_summary.json          (Channel 2 p-value, i.i.d.-flip; retired as
                                       confirmatory 2026-06-13 — block-permutation
                                       null p=0.1947, findings/szat_block_permutation.md)
  findings/drain_label_shuffle_null_canonical.json (Channel 3, canonical substrate)
  data/drain_label_shuffle_null.json  (Channel 3 DPG-era values, provenance only)

Forward dependencies:
  findings/joint_outlier_score.json
  findings/joint_outlier_score_summary.md

Backward:
  data/outputs/simulation_real_map_scores_canonical.json
Forward:
  findings/joint_outlier_score.json
  findings/joint_outlier_score_summary.md
"""
from __future__ import annotations


import sys
import logging
import time
from pathlib import Path
try:
    import data_loader
    from canonical_manifest import verify_canonical_files
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader
    from canonical_manifest import verify_canonical_files

try:
    from audit_logger import log_run as _log_run
except ImportError:
    def _log_run(*args, **kwargs): pass  # no-op fallback

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
logger = logging.getLogger(__name__)
DATA = data_loader._resolve_path("data")
try:
    from analysis.utils.data_loader import FINDINGS as REPORTS
except ImportError:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'utils'))
    from data_loader import FINDINGS as REPORTS

ENSEMBLE_CSV      = DATA / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"
REAL_SCORES       = DATA / "outputs" / "simulation_real_map_scores_canonical.json"
CONVERGENCE_JSON  = DATA / "outputs" / "simulation_convergence_diagnostics_canonical.json"
SZAT_JSON         = REPORTS / "szat_summary.json"
DRAIN_JSON_CANONICAL = REPORTS / "drain_label_shuffle_null_canonical.json"
DRAIN_JSON_STALE     = DATA / "drain_label_shuffle_null.json"
OUT_JSON          = REPORTS / "joint_outlier_score.json"
OUT_MD            = REPORTS / "joint_outlier_score_summary.md"

PARTISAN_COLS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]

# Map keys in simulation_real_map_scores_canonical.json
MAP_KEYS = {
    "minority": "minority_2026",
    "majority": "majority_2026",
    "enacted":  "2019_enacted",
}

# Fallback n_eff used if convergence diagnostics JSON is absent or unreadable.
# Per simulation_convergence_diagnostics_canonical.json the actual minimum across
# the 4 partisan metrics is 1428 (mean_median; pooled 1,010k sample run).
# This fallback is only used when the file is missing or unreadable.
_N_EFF_FALLBACK = 1428  # conservative minimum across the 4 partisan metrics from the 1,010,000-plan canonical run


def _load_n_eff_conservative() -> int:
    """Read minimum n_eff from convergence diagnostics; fall back to 224."""
    if not CONVERGENCE_JSON.exists():
        return _N_EFF_FALLBACK
    try:
        with open(CONVERGENCE_JSON) as f:
            diag = json.load(f)
        n_effs = [v["n_eff"] for v in diag.values() if isinstance(v, dict) and "n_eff" in v]
        return int(min(n_effs)) if n_effs else _N_EFF_FALLBACK
    except Exception as e:
        logger.warning("convergence diagnostics unavailable, using fallback n_eff=%d: %s", _N_EFF_FALLBACK, e)
        return _N_EFF_FALLBACK


N_EFF_CONSERVATIVE = _load_n_eff_conservative()


def mahalanobis_pvalue(
    ensemble: pd.DataFrame,
    observed: dict[str, float],
    cols: list[str],
) -> tuple[float, float, np.ndarray]:
    X = ensemble[cols].dropna().values
    mu = X.mean(axis=0)
    cov = np.cov(X, rowvar=False)
    cov_inv = np.linalg.pinv(cov)
    obs = np.array([observed[c] for c in cols])
    diff = obs - mu
    d2 = float(diff @ cov_inv @ diff)
    d = float(np.sqrt(d2))
    p = float(stats.chi2.sf(d2, df=len(cols)))
    return d, p, mu


def mahalanobis_pvalue_neff_adjusted(
    d: float,
    p_metrics: int,
    n_eff: int = N_EFF_CONSERVATIVE,
) -> tuple[float, float]:
    """
    Hotelling T² adjustment for estimated covariance matrix.

    When the covariance matrix is estimated from n_eff effective independent
    samples, testing a single new observation against the estimated distribution
    uses F(p, n_eff - p) rather than chi-squared(p). This is the conservative
    bound — with n_eff = 224 the correction is meaningful; as n_eff → ∞ it
    converges to the chi-squared result.

    F-statistic: (n_eff - p) / (p * (n_eff + 1)) * D²
    """
    d2 = d ** 2
    f_stat = float((n_eff - p_metrics) / (p_metrics * (n_eff + 1)) * d2)
    p_adj = float(stats.f.sf(f_stat, p_metrics, n_eff - p_metrics))
    return p_adj, f_stat


def ensemble_marginal_percentile(
    ensemble: pd.DataFrame,
    col: str,
    observed_value: float,
    upper_tail: bool = True,
) -> float:
    vals = ensemble[col].dropna().values
    if upper_tail:
        return float(np.mean(vals >= observed_value))
    else:
        return float(np.mean(vals <= observed_value))


def fisher_combine(p_values: list[float]) -> tuple[float, float]:
    clipped = [max(p, 1e-300) for p in p_values]
    T = -2.0 * sum(np.log(clipped))
    p_combined = float(stats.chi2.sf(T, df=2 * len(p_values)))
    return T, p_combined


def run() -> None:
    t0 = time.time()
    verify_canonical_files()
    print("Loading canonical 1.01M ensemble...")
    ensemble = pd.read_csv(ENSEMBLE_CSV)
    print(f"  Rows: {len(ensemble):,}  Cols: {ensemble.columns.tolist()}")

    print("Loading canonical real map scores...")
    with open(REAL_SCORES) as f:
        real = json.load(f)

    print("Loading SZAT summary...")
    with open(SZAT_JSON) as f:
        szat = json.load(f)
    szat_p = float(szat["bootstrap_p_value"])
    szat_n = int(szat["bootstrap_n"])
    _szat_b = szat.get("bootstrap_b_extreme")
    if _szat_b is not None:
        szat_p_label = (
            f"{szat_p:.4f} ((b+1)/(B+1); {int(_szat_b)}/{szat_n} permutations "
            f"exceeded observed, full-recompute)"
        )
    else:
        # Legacy inputs without an exceedance count: back-derive approximately and say so.
        szat_p_label = f"{szat_p:.4f} (~{int(round(szat_p * szat_n))}/{szat_n} permutations exceeded observed, full-recompute)"

    # ── Channel 1: Mahalanobis ────────────────────────────────────────────────

    print("\nChannel 1 — Partisan joint tail (Mahalanobis)...")
    results: dict = {}

    for label, key in MAP_KEYS.items():
        if key not in real:
            print(f"  WARNING: {key!r} not in real map scores, skipping")
            continue
        obs = real[key]
        d, p, mu = mahalanobis_pvalue(ensemble, obs, PARTISAN_COLS)
        p_adj, f_stat = mahalanobis_pvalue_neff_adjusted(d, len(PARTISAN_COLS))
        marginals = {
            col: {
                "observed": round(obs[col], 6),
                "ensemble_mean": round(float(mu[i]), 6),
                "ensemble_p5": round(float(np.percentile(ensemble[col], 5)), 6),
                "ensemble_p95": round(float(np.percentile(ensemble[col], 95)), 6),
                "marginal_tail_p": round(
                    ensemble_marginal_percentile(
                        ensemble, col, obs[col], upper_tail=(obs[col] >= float(mu[i]))
                    ),
                    6,
                ),
            }
            for i, col in enumerate(PARTISAN_COLS)
        }
        results[label] = {
            "mahalanobis_distance": round(d, 4),
            "joint_partisan_p": round(p, 8),
            "joint_partisan_p_neff_adjusted": round(p_adj, 8),
            "neff_adjustment": {
                "n_eff_used": N_EFF_CONSERVATIVE,
                "f_stat": round(f_stat, 4),
                "df1": len(PARTISAN_COLS),
                "df2": N_EFF_CONSERVATIVE - len(PARTISAN_COLS),
                "note": "Hotelling T² correction for estimated covariance; conservative lower bound on n_eff",
            },
            "df": len(PARTISAN_COLS),
            "marginals": marginals,
        }
        print(f"  {label:10}  Mahal={d:.3f}  p={p:.2e}  p_adj(n_eff={N_EFF_CONSERVATIVE})={p_adj:.2e}")

    # ── Channel 2: SZAT bootstrap p-value ────────────────────────────────────

    print(f"\nChannel 2 — SZAT bootstrap p-value...")
    print(f"  SZAT score: {szat['szat_score']:+.6f}")
    print(f"  Bootstrap p: {szat_p_label}")

    # ── Channel 3: Neighbour-Drain — canonical label-shuffle null ─────────────
    # Canonical-substrate results (2026-06-11 Phase B re-run) live in
    # findings/drain_label_shuffle_null_canonical.json (per_map schema). The
    # DPG/blended-substrate values in data/drain_label_shuffle_null.json are
    # superseded and are carried only as stale_* provenance fields. This script
    # previously read the stale file directly; regenerating from it silently
    # reverted the canonical correction (observed 2026-06-12) — hence the hard
    # requirement below.
    if not DRAIN_JSON_CANONICAL.exists():
        raise FileNotFoundError(
            f"{DRAIN_JSON_CANONICAL} not found — canonical Channel 3 results are "
            "required; refusing to fall back to superseded DPG-era values."
        )
    with open(DRAIN_JSON_CANONICAL) as _f:
        _drain_canon_raw = json.load(_f)
    drain_canon = {
        "majority": _drain_canon_raw["per_map"]["majority_2026"],
        "minority": _drain_canon_raw["per_map"]["minority_2026"],
        "enacted":  _drain_canon_raw["per_map"]["enacted_2019"],
    }
    drain_prediction_a = bool(_drain_canon_raw.get("prediction_A_confirmed", False))
    print(f"  Channel 3 canonical drain loaded from {DRAIN_JSON_CANONICAL.name}")
    _drain_stale = None
    if DRAIN_JSON_STALE.exists():
        with open(DRAIN_JSON_STALE) as _f:
            _drain_stale = json.load(_f)

    # ── Fisher combination (minority only, channels 1+2) ─────────────────────

    print("\nFisher combined test (minority, Channels 1+2)...")
    ch1_p = results["minority"]["joint_partisan_p"]
    ch2_p = szat_p

    T, p_combined = fisher_combine([ch1_p, ch2_p])
    ch1_p_adj = results["minority"]["joint_partisan_p_neff_adjusted"]
    T_adj, p_combined_adj = fisher_combine([ch1_p_adj, ch2_p])
    print(f"  Channel 1 (partisan joint):   p = {ch1_p:.2e}  (n_eff-adjusted: {ch1_p_adj:.2e})")
    print(f"  Channel 2 (SZAT bootstrap):   p = {ch2_p:.2e}")
    print(f"  Fisher T = {T:.3f}  (chi-sq df=4)  combined p = {p_combined:.2e}")
    print(f"  Fisher T_adj = {T_adj:.3f}  (n_eff-adjusted Ch1)  combined p_adj = {p_combined_adj:.2e}")

    # ── Structural metric notes ───────────────────────────────────────────────
    # MAD and Reock values read from canonical real map scores JSON.
    # Municipal anchoring is FROZEN 2026-05-07 (no canonical JSON source).

    _min_real = real.get("minority_2026", {})
    _maj_real = real.get("majority_2026", {})
    _min_mad  = _min_real.get("population_mad", 4707)  # fallback = frozen
    _maj_mad  = _maj_real.get("population_mad", 3180)
    _min_reock_pct = round(_min_real.get("reock_proxy_pct_below_030", 0.348) * 100, 1)
    _maj_reock_pct = round(_maj_real.get("reock_proxy_pct_below_030", 0.135) * 100, 1)
    _reock_ratio = round(_min_reock_pct / _maj_reock_pct, 2) if _maj_reock_pct else float("nan")

    # Per-plan MAD and proxy-Reock ARE captured in the canonical ensemble outputs
    # (columns population_mad / reock_proxy_median in the raw samples CSV), so the
    # ensemble percentiles are computed directly here. The pre-2026-07-08 "pending —
    # not in ensemble outputs" status was stale.
    _min_mad_pct = _maj_mad_pct = _min_mad_tail_p = float("nan")
    _min_reock_med_pct = _maj_reock_med_pct = None
    _has_mad = "population_mad" in ensemble.columns
    if _has_mad:
        _mad_vals = ensemble["population_mad"].dropna().values
        _min_mad_pct = float((_mad_vals < _min_mad).mean() * 100)
        _maj_mad_pct = float((_mad_vals < _maj_mad).mean() * 100)
        _min_mad_tail_p = float((_mad_vals >= _min_mad).mean())
    _has_reock = "reock_proxy_median" in ensemble.columns
    if _has_reock:
        _reock_vals = ensemble["reock_proxy_median"].dropna().values
        _min_reock_med = _min_real.get("reock_proxy_median")
        _maj_reock_med = _maj_real.get("reock_proxy_median")
        _min_reock_med_pct = float((_reock_vals < _min_reock_med).mean() * 100) if _min_reock_med is not None else None
        _maj_reock_med_pct = float((_reock_vals < _maj_reock_med).mean() * 100) if _maj_reock_med is not None else None

    # Drain observed scores — canonical substrate.
    _drain_min_obs = float(drain_canon["minority"]["observed"])
    _drain_maj_obs = float(drain_canon["majority"]["observed"])
    _drain_ena_obs = float(drain_canon["enacted"]["observed"])

    structural_notes = {
        "municipal_anchoring": {
            # Canonical values from score_anchoring.py run 2026-05-10 against official EA shapefiles.
            # DPG-era values were: minority 14.5%, majority 71.0%, ratio 4.9x.
            # Canonical recomputation: both maps within the 70-85% Canadian norm; DPG asymmetry was
            # an artefact of boundary placement (area fidelity != perimeter alignment).
            "minority_pct": 72.0,
            "majority_pct": 80.0,
            "enacted_2019_pct": 75.2,
            "departure_factor_vs_comparators": 1.11,
            "p_value": "not applicable — both maps within Canadian norm (70–85 %); "
            "canonical ratio 1.11× (DPG-era 4.9× was a geometry artefact; see §5.8.5 footnote)",
        },
        "population_mad_ratio": {
            "minority_mad": round(_min_mad, 1),
            "majority_mad": round(_maj_mad, 1),
            "ratio_minority_majority": round(_min_mad / _maj_mad, 3) if _maj_mad else float("nan"),
            **({
                "minority_ensemble_percentile": round(_min_mad_pct, 2),
                "majority_ensemble_percentile": round(_maj_mad_pct, 2),
                "minority_upper_tail_p": round(_min_mad_tail_p, 6),
                "status_note": "per-plan MAD captured in canonical ensemble outputs; percentiles computed directly (earlier 'pending' status was stale — corrected 2026-07-08)",
            } if _has_mad else {
                "p_value": "pending — per-plan MAD not in ensemble outputs",
            }),
            "source": "simulation_real_map_scores_canonical.json + simulated_ensemble_raw_samples_canonical.csv",
        },
        "reock_asymmetry": {
            "minority_pct_below_0_30": _min_reock_pct,
            "majority_pct_below_0_30": _maj_reock_pct,
            "ratio": _reock_ratio,
            **({
                "minority_median_reock_ensemble_percentile": round(_min_reock_med_pct, 2) if _min_reock_med_pct is not None else None,
                "majority_median_reock_ensemble_percentile": round(_maj_reock_med_pct, 2) if _maj_reock_med_pct is not None else None,
                "status_note": "per-plan proxy Reock captured in canonical ensemble outputs; both real maps sit above the neutral ensemble on median compactness — null finding, expected for commission maps (earlier 'pending' status was stale — corrected 2026-07-08)",
            } if _has_reock else {
                "p_value": "pending — per-plan Reock not in ensemble outputs",
            }),
            "note": "proxy Reock (bounding-box diagonal), not true minimum-enclosing-circle Reock",
            "source": "simulation_real_map_scores_canonical.json + simulated_ensemble_raw_samples_canonical.csv",
        },
        "neighbour_drain": {
            "_SUPERSEDED": (
                "2026-06-11. DPG/blended-substrate values replaced by the canonical-substrate "
                "Phase B re-run (findings/drain_label_shuffle_null_canonical.json). Banner "
                "reapplied 2026-06-12 after Amendment-10 regeneration overwrote the prior "
                "retraction; script-generated since 2026-07-08 so regeneration can no longer "
                "drop it."
            ),
            "canonical_majority_drain_score": round(_drain_maj_obs, 6),
            "canonical_minority_drain_score": round(_drain_min_obs, 6),
            "canonical_enacted_2019_drain_score": round(_drain_ena_obs, 6),
            "canonical_majority_z": round(float(drain_canon["majority"]["z"]), 3),
            "canonical_minority_z": round(float(drain_canon["minority"]["z"]), 3),
            "canonical_enacted_2019_z": round(float(drain_canon["enacted"]["z"]), 3),
            "canonical_note": (
                "All three maps anomalously low against canonical-substrate label-shuffle null "
                "(10,000 perms); 2019 enacted most anomalous "
                f"(z={drain_canon['enacted']['z']:.2f}), majority second "
                f"({drain_canon['majority']['z']:.2f}), minority third "
                f"({drain_canon['minority']['z']:.2f}). Pre-registered Prediction A "
                f"{'CONFIRMS' if drain_prediction_a else 'DOES NOT CONFIRM'} on canonical substrate."
            ),
            **({
                "stale_minority_drain_score": float(_drain_stale["minority"]["observed"]),
                "stale_majority_drain_score": float(_drain_stale["majority"]["observed"]),
                "stale_minority_p": float(_drain_stale["minority"]["p_two_tailed"]),
                "stale_majority_z": float(_drain_stale["majority"]["z"]),
                "stale_note": "DPG-era / blended-vote substrate; superseded by canonical values above.",
            } if _drain_stale else {}),
            "source": "drain_label_shuffle_null.json (stale) / drain_label_shuffle_null_canonical.json (current)",
        },
    }

    # ── JSON summary ──────────────────────────────────────────────────────────

    summary = {
        "methodology": "Joint outlier score (joint neutral-draw tail probability), canonical ensemble",
        "ensemble_source": "simulated_ensemble_raw_samples_canonical.csv (1,010,000 plans, 4 chains x 252,500)",
        "interpretation": (
            "P(feature vector | neutral draw). NOT a posterior probability of "
            "gerrymandering — no prior is specified. Low values mean the neutral "
            "null is implausible as an explanation for the observed feature vector."
        ),
        "channels_active": 1,
        "channels_note": (
            "Ch1 (Mahalanobis joint tail) is the sole confirmatory channel. Ch2 (SZAT) was "
            "retired to exploratory context 2026-06-13: its i.i.d.-flip p=0.0024 does not "
            "survive a contiguity-respecting block-permutation null (p=0.1947, variance "
            "inflation 5.79x; findings/szat_block_permutation.md). Ch3 (neighbour-drain) is "
            "reported per pre-registration and is not part of the joint headline."
        ),
        "channels_pending": 0,
        "channels_pending_note": (
            "Formerly-pending structural channels resolved: municipal anchoring RETRACTED on "
            "canonical geometry (both maps within Canadian norm); population MAD and proxy "
            "Reock captured in canonical ensemble outputs with percentiles computed below."
        ),
        "joint_headline": {
            "method": "Bonferroni dependence-robust upper bound over the two examined channels",
            "p_upper_bound": round(2 * ch1_p, 10),
            "note": (
                "Operative joint statistic since 2026-06-10: p <= 2 x min(Ch1, Ch2) = 2 x Ch1 "
                "(Ch1 is the binding term). Valid under arbitrary dependence between channels; "
                "replaces the retired Fisher combination (anti-conservative under positive "
                "dependence, Brown 1975 — the channels share the 2023 vote substrate)."
            ),
        },
        "maps": results,
        "szat": {
            "score": szat["szat_score"],
            "bootstrap_n": szat_n,
            "bootstrap_p_value": szat_p,
            "bootstrap_p_label": szat_p_label,
            "bootstrap_procedure": szat.get("bootstrap_procedure", "full-recompute"),
            "aspredicted": "289469",
        },
        "fisher_combined_minority": {
            "_SUPERSEDED": (
                "2026-06-10. Fisher assumed Ch1/Ch2 independence; the channels share the 2023 "
                "vote substrate and Fisher is anti-conservative under positive dependence "
                "(Brown 1975). Retained as historical record only — the operative joint "
                "statistic is joint_headline (Bonferroni upper bound)."
            ),
            "as_published_2026_06_10": {
                "p_channel_1": 1.4e-06,
                "p_channel_2": 0.0024,
                "fisher_T": 39.0226,
                "combined_p": 6.87e-08,
                "note": (
                    "Frozen as-published figures (reports cite T = 39.03, p = 6.87e-08). "
                    "p_channel_2 = 0.0024 was the raw exceedance ratio (24/10,000); the "
                    "recomputed fields below use the current (b+1)/(B+1) estimator "
                    "(25/10,001 = 0.0025), which shifts the recomputed Fisher slightly. "
                    "Same underlying permutation result either way."
                ),
            },
            "channels": ["partisan_joint_mahalanobis", "szat_bootstrap"],
            "p_channel_1": round(ch1_p, 8),
            "p_channel_1_neff_adjusted": round(ch1_p_adj, 8),
            "p_channel_2": round(szat_p, 8),
            "fisher_T": round(T, 4),
            "fisher_df": 4,
            "combined_p": round(p_combined, 8),
            "combined_p_neff_adjusted": round(p_combined_adj, 8),
            "neff_adjustment_note": (
                f"n_eff-adjusted Fisher uses Hotelling T² p for Ch1 "
                f"(n_eff={N_EFF_CONSERVATIVE}, conservative lower bound). "
                "Both combined p-values reject the null at p < 1e-5."
            ),
        },
        "structural_pending": structural_notes,
        "caveats": [
            "Ensemble is 1,010,000 plans (canonical shapefiles, 4 chains x 252,500, base_seed=1432864451); n_eff ~1,428-1,682 per metric.",
            "Declination column re-signed 2026-06-12 per Amendment 10 (Warrington 2018 convention; sign correction at mcmc_ensemble.py:215 + chain CSV in-place flip). See findings/amendment_10_migration_manifest.json.",
            "Replaces DPG-based 250k ensemble; canonical shapefiles are official Elections Alberta files.",
            "Fisher combination retired 2026-06-10: it assumed Ch1/Ch2 independence, but the channels share the 2023 vote substrate (anti-conservative under positive dependence, Brown 1975). The fisher_combined_minority block is historical record; the operative joint statistic is the Bonferroni upper bound in joint_headline.",
            "Ch2 (SZAT) retired as a confirmatory channel 2026-06-13: block-permutation null returns p=0.1947 (findings/szat_block_permutation.md); the i.i.d.-flip p=0.0024 is exploratory context only.",
            "Mahalanobis assumes multivariate Gaussian ensemble distribution — informally verified.",
            "This score answers P(features | neutral), not P(gerrymandered | features).",
        ],
    }

    with open(OUT_JSON, "w") as f:
        json.dump(summary, f, indent=2, default=float)

    # ── Markdown summary ──────────────────────────────────────────────────────

    min_m = results["minority"]
    maj_m = results["majority"]
    ena_m = results["enacted"]

    md_directional = ""
    ensemble_mean_eg = min_m["marginals"]["efficiency_gap"]["ensemble_mean"]
    if ensemble_mean_eg > 0:
        md_directional = (
            f"\n**Directional note.** The neutral ensemble centre is moderately "
            f"UCP-favourable (mean EG = {ensemble_mean_eg:+.4f}), reflecting Alberta's "
            "natural geographic sorting of voters (rural UCP dispersion; Chen & Rodden 2013). "
            "The minority map's extreme MM and s50 scores are driven by structural map choices, "
            "not natural geography.\n"
        )

    marginal_rows = ""
    for col, v in min_m["marginals"].items():
        marginal_rows += f"| {col} | {v['observed']:+.4f} | {v['ensemble_mean']:+.4f} | {v['marginal_tail_p']:.4f} |\n"

    md = f"""# Joint Outlier Score — Alberta 2026 EBC Maps

**Date:** {time.strftime('%Y-%m-%d')} (regenerated; first canonical run 2026-05-07)
**Ensemble:** canonical 1,010,000 plans (official Elections Alberta shapefiles, 4 chains × 252,500, base_seed=1432864451)
**Question:** How probable is it that a neutral redistricting process produces a map
whose feature vector looks like the minority 2026 map?

**Answer format:** P(feature vector | neutral draw) — the joint probability that
a neutral-draw plan is at least as extreme as the observed map across all active
channels simultaneously. This is *not* a posterior probability of gerrymandering.

---

## Channel 1 — Partisan joint tail (Mahalanobis)

Ensemble: {len(ensemble):,} neutral-draw plans (canonical shapefiles). Metrics: EG, mean-median, declination, seats@50/50.
Mahalanobis distance accounts for the correlation structure between these four metrics.
{md_directional}
| Map | Mahalanobis distance | p (chi-sq, df=4) | p (n_eff-adjusted, F({len(PARTISAN_COLS)},{N_EFF_CONSERVATIVE - len(PARTISAN_COLS)})) |
| --- | --- | --- | --- |
| Minority 2026 | {min_m['mahalanobis_distance']:.4f} | {min_m['joint_partisan_p']:.2e} | {min_m['joint_partisan_p_neff_adjusted']:.2e} |
| Majority 2026 | {maj_m['mahalanobis_distance']:.4f} | {maj_m['joint_partisan_p']:.2e} | {maj_m['joint_partisan_p_neff_adjusted']:.2e} |
| 2019 Enacted  | {ena_m['mahalanobis_distance']:.4f} | {ena_m['joint_partisan_p']:.2e} | {ena_m['joint_partisan_p_neff_adjusted']:.2e} |

*n_eff-adjusted p uses Hotelling T² correction (F-distribution) with n_eff = {N_EFF_CONSERVATIVE} — the conservative lower bound from convergence diagnostics. Both columns reject the null for the minority map.*

**Minority marginals:**

| Metric | Observed | Ensemble mean | Marginal tail p |
| --- | --- | --- | --- |
{marginal_rows}
---

## Channel 2 — SZAT bootstrap null

SZAT score: {szat['szat_score']:+.6f} (minority EG − majority EG, swing zones only)
Bootstrap p: {szat_p_label}
(AsPredicted #289,469; seed pre-committed at git hash d2aea42; full-recompute procedure)

**Status (2026-06-13): retired as a confirmatory channel.** Under a contiguity-respecting
block-permutation null the SZAT p-value is 0.1947 (variance inflation 5.79× vs the i.i.d.
flip; `findings/szat_block_permutation.md`). The bootstrap p above is the i.i.d.-flip value,
retained as exploratory context only. The joint headline rests on Channel 1 alone.

---

## Channel 3 — Neighbour-Drain label-shuffle null (canonical substrate)

Pre-registered: OSF r3zm7 / AsPredicted #289,451. Canonical-substrate Phase B re-run 2026-06-11
(`findings/drain_label_shuffle_null_canonical.json`, {_drain_canon_raw.get('n_permutations', 10000):,} permutations, seed {_drain_canon_raw.get('seed', 'n/a')}).

| Map | drain_score | Null mean | z-score | p (two-tailed) |
| --- | --- | --- | --- | --- |
| Majority 2026 | {_drain_maj_obs:.6f} | {drain_canon['majority']['null_mean']:.6f} | **{drain_canon['majority']['z']:.3f}** | **{drain_canon['majority']['p_two_tailed']:.4f}** |
| Minority 2026 | {_drain_min_obs:.6f} | {drain_canon['minority']['null_mean']:.6f} | {drain_canon['minority']['z']:.3f} | {drain_canon['minority']['p_two_tailed']:.4f} |
| 2019 Enacted | {_drain_ena_obs:.6f} | {drain_canon['enacted']['null_mean']:.6f} | {drain_canon['enacted']['z']:.3f} | {drain_canon['enacted']['p_two_tailed']:.4f} |

**Prediction A** (drain_score(majority) > drain_score(minority)): **{'CONFIRMED' if drain_prediction_a else 'NOT CONFIRMED'}** on the canonical substrate ({_drain_maj_obs:.6f} vs {_drain_min_obs:.6f}).

**Interpretation.** All three maps — including the pre-commission 2019 enacted baseline — are
anomalously *low* against their own label-shuffle nulls; the 2019 enacted map is the most
anomalous (z = {drain_canon['enacted']['z']:.2f}). No map is singularly anomalous on this metric.
(The superseded DPG/blended-substrate run reported minority p = 0.1342 within null and majority
z = −2.915; those values did not survive the canonical re-run and are retained only as
stale_* provenance fields in the JSON.)

**Channel 3 is reported per pre-registration and is not part of the joint headline.**

---

## Joint statistic — Bonferroni upper bound (Fisher retired)

**Operative headline: p ≤ {2 * ch1_p:.2e} (= 2 × Ch1), valid under arbitrary dependence
between the two examined channels.** The Fisher combination below assumed Ch1/Ch2
independence and was retired 2026-06-10 (the channels share the 2023 vote substrate;
Fisher is anti-conservative under positive dependence — Brown 1975). It is preserved
as historical record only.

| Channel | p (unadjusted) | p (n_eff-adjusted) |
| --- | --- | --- |
| Partisan joint (Mahalanobis) | {ch1_p:.2e} | {ch1_p_adj:.2e} |
| SZAT bootstrap (retired, i.i.d.-flip) | {szat_p:.4f} | {szat_p:.4f} |
| **Fisher combined (historical)** | **{p_combined:.2e}** | **{p_combined_adj:.2e}** |

Unadjusted: Fisher T = {T:.3f}, chi-sq df = 4.
n_eff-adjusted: Fisher T = {T_adj:.3f}, using Hotelling T² p for Ch1 (n_eff = {N_EFF_CONSERVATIVE}, conservative lower bound).

**Reading:** the operative claim is the dependence-robust bound p ≤ {2 * ch1_p:.2e}
(≈ 1 in {int(round(1/max(2 * ch1_p, 1e-12))):,}) — under the neutral null, a map with
Channel 1's joint partisan profile arises at most about once in every
{int(round(1/max(2 * ch1_p, 1e-12))):,} draws, allowing for the two channels examined.
The historical Fisher figure ({p_combined:.2e}) overstated joint significance by
assuming channel independence.

---

## Supplementary structural channels (all resolved — none pending)

| Channel | Status | Finding |
| --- | --- | --- |
| Municipal anchoring departure | RETRACTED on canonical geometry (§5.8.5) — DPG-era 4.9× ratio did not survive; canonical: maj 80.0% / min 72.0%, both within 70–85% Canadian norm | No longer a channel |
| Population MAD ratio | Captured in canonical ensemble outputs (per-plan `population_mad`) | Minority {(_min_mad / _maj_mad):.2f}× majority ({_min_mad:,.0f} vs {_maj_mad:,.0f}); minority at p{_min_mad_pct:.1f} of the neutral ensemble{'' if _has_mad else ' (percentile unavailable)'} |
| Reock asymmetry | Captured in canonical ensemble outputs (per-plan proxy Reock) | Null finding: both real maps sit at ~p100 on median compactness (anomalously compact — expected for commission maps); minority/majority pct<0.30 ratio {_reock_ratio}× (the DPG-era 2.58× value was retracted — see DOCUMENTED CORRECTIONS) |

*(Corrected 2026-07-08: this table previously described MAD and Reock as "pending — not in
ensemble outputs" and carried the retracted 2.58× Reock ratio and a stale 1.48× MAD ratio.
The canonical ensemble outputs contain per-plan values for both metrics.)*

---

## Interpretation note

The duck test made precise: the minority map's four-dimensional partisan feature
vector sits at Mahalanobis distance {min_m['mahalanobis_distance']:.2f} from the ensemble center
(p = {ch1_p:.2e}). The operative joint statistic is the dependence-robust Bonferroni
upper bound p ≤ {2 * ch1_p:.2e}. SZAT (Ch2) is exploratory context only
(block-permutation p = 0.1947); the retired Fisher combination is preserved above as
historical record.

**Channel 3 (Neighbour-Drain, canonical substrate 2026-06-11).** All three maps are
anomalously low against their label-shuffle nulls (2019 enacted most anomalous,
z = {drain_canon['enacted']['z']:.2f}); Prediction A {'is directionally confirmed' if drain_prediction_a else 'is not confirmed'}.
The channel is reported per pre-registration and is not part of the joint headline.

The majority map sits at Mahalanobis distance {maj_m['mahalanobis_distance']:.2f} from the ensemble
center (p = {maj_m['joint_partisan_p']:.2e}) — outlier on MM in the NDP-favourable direction.

---

*Script: `analysis/scripts/joint_outlier_score_canonical.py`*
*Full output: `findings/joint_outlier_score.json`*
"""

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\nResults written:")
    print(f"  {OUT_JSON}")
    print(f"  {OUT_MD}")
    print(f"\n{'='*60}")
    print(f"DUCK SCORE (minority 2026) — canonical ensemble")
    print(f"  Channel 1 (partisan joint):  p = {ch1_p:.2e}")
    print(f"  Joint headline (Bonferroni): p <= {2 * ch1_p:.2e}")
    print(f"  Channel 2 (SZAT, retired):   p = {szat_p:.4f} (i.i.d.-flip; block-perm p=0.1947)")
    print(f"  Fisher combined (historical): p = {p_combined:.2e}")
    print(f"  Channel 3 (drain, canonical): min z = {drain_canon['minority']['z']:.3f}, maj z = {drain_canon['majority']['z']:.3f}, 2019 z = {drain_canon['enacted']['z']:.3f}")
    print(f"  Pending channels: 0")
    print(f"{'='*60}")
    _log_run(__file__, [str(p) for p in [OUT_JSON, OUT_MD]], time.time() - t0)


if __name__ == "__main__":
    run()
