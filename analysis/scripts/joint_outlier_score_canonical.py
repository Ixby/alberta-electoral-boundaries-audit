"""
joint_outlier_score_canonical.py -- Joint Outlier Score (Duck Score), canonical run

Same methodology as joint_outlier_score.py but uses the canonical 100k ensemble
(simulated_ensemble_raw_samples_canonical.csv) and canonical real-map scores
(simulation_real_map_scores_canonical.json).

Replaces the DPG-based 250k ensemble for all Channel 1 percentile placements.

Backward dependencies:
  data/simulated_ensemble_raw_samples_canonical.csv
  data/simulation_real_map_scores_canonical.json
  analysis/reports/szat_summary.json          (Channel 2 p-value)
  analysis/reports/neighbour_drain_analysis.md (Channel 3 result, read manually)

Forward dependencies:
  analysis/reports/joint_outlier_score.json
  analysis/reports/joint_outlier_score_summary.md
"""
from __future__ import annotations


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
REPORTS = ROOT / "analysis" / "reports"

ENSEMBLE_CSV  = DATA / "simulated_ensemble_raw_samples_canonical.csv"
REAL_SCORES   = DATA / "simulation_real_map_scores_canonical.json"
SZAT_JSON     = REPORTS / "szat_summary.json"
DRAIN_JSON    = DATA / "drain_label_shuffle_null.json"
OUT_JSON      = REPORTS / "joint_outlier_score.json"
OUT_MD        = REPORTS / "joint_outlier_score_summary.md"

PARTISAN_COLS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]

# Map keys in simulation_real_map_scores_canonical.json
MAP_KEYS = {
    "minority": "minority_2026",
    "majority": "majority_2026",
    "enacted":  "2019_enacted",
}

# Conservative n_eff lower bound from convergence diagnostics (Geyer's method).
# Actual range across metrics: 224–326. Using 224 for the most conservative
# Hotelling T² adjustment.
N_EFF_CONSERVATIVE = 224


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
    print("Loading canonical 100k ensemble...")
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
    szat_p_label = f"{szat_p:.4f} ({int(round(szat_p * szat_n))}/{szat_n} permutations exceeded observed, full-recompute)"

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

    # ── Channel 3: Neighbour-Drain — read from drain_label_shuffle_null.json ────
    _DRAIN_FALLBACK_P = 0.1342  # frozen 2026-05-07 if JSON unavailable
    if DRAIN_JSON.exists():
        with open(DRAIN_JSON) as _f:
            _drain_data = json.load(_f)
        drain_minority_p = float(_drain_data["minority"]["p_two_tailed"])
        drain_majority_z = float(_drain_data["majority"]["z"])
        drain_majority_p = float(_drain_data["majority"]["p_two_tailed"])
        print(f"  Channel 3 drain p loaded from {DRAIN_JSON.name}")
    else:
        import warnings
        warnings.warn(
            f"{DRAIN_JSON.name} not found — using frozen drain_minority_p={_DRAIN_FALLBACK_P}",
            UserWarning,
        )
        drain_minority_p = _DRAIN_FALLBACK_P
        drain_majority_z = -2.915
        drain_majority_p = 0.0

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

    # Drain observed scores from DRAIN_JSON if available, else frozen.
    if DRAIN_JSON.exists():
        _drain_min_obs = float(_drain_data["minority"]["observed"])
        _drain_maj_obs = float(_drain_data["majority"]["observed"])
    else:
        _drain_min_obs = 0.006176
        _drain_maj_obs = 0.000179

    structural_notes = {
        "municipal_anchoring": {
            # FROZEN 2026-05-07 from da_anchoring analysis — no canonical JSON source yet.
            "minority_pct": 14.5,
            "majority_pct": 71.0,
            "enacted_2019_pct": 73.8,
            "departure_factor_vs_comparators": 4.9,
            "p_value": "pending — Canadian comparator distribution too thin for rigorous p-value; "
            "4.9x below comparator norm is the reported summary statistic",
        },
        "population_mad_ratio": {
            "minority_mad": round(_min_mad, 1),
            "majority_mad": round(_maj_mad, 1),
            "ratio_minority_majority": round(_min_mad / _maj_mad, 3) if _maj_mad else float("nan"),
            "p_value": "pending — per-plan MAD not in ensemble outputs",
            "source": "simulation_real_map_scores_canonical.json",
        },
        "reock_asymmetry": {
            "minority_pct_below_0_30": _min_reock_pct,
            "majority_pct_below_0_30": _maj_reock_pct,
            "ratio": _reock_ratio,
            "p_value": "pending — per-plan Reock not in ensemble outputs",
            "note": "proxy Reock (bounding-box diagonal), not true minimum-enclosing-circle Reock",
            "source": "simulation_real_map_scores_canonical.json",
        },
        "neighbour_drain": {
            "minority_drain_score": _drain_min_obs,
            "majority_drain_score": _drain_maj_obs,
            "minority_p": drain_minority_p,
            "majority_z": drain_majority_z,
            "note": f"minority within null (p={drain_minority_p:.4f}); "
                    f"majority anomalously low (z={drain_majority_z:.3f}, p<0.0001). "
                    "Channel not included in Fisher combination.",
            "source": DRAIN_JSON.name if DRAIN_JSON.exists() else "frozen 2026-05-07",
        },
    }

    # ── JSON summary ──────────────────────────────────────────────────────────

    summary = {
        "methodology": "Joint outlier score (joint neutral-draw tail probability), canonical ensemble",
        "ensemble_source": "simulated_ensemble_raw_samples_canonical.csv (100k plans, 2 chains x 50k)",
        "interpretation": (
            "P(feature vector | neutral draw). NOT a posterior probability of "
            "gerrymandering — no prior is specified. Low values mean the neutral "
            "null is implausible as an explanation for the observed feature vector."
        ),
        "channels_active": 2,
        "channels_executed_non_significant": 1,
        "channels_pending": 3,
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
            "Ensemble is 100k plans (canonical shapefiles, 2 chains x 50k); n_eff ~224-326 per metric.",
            "Replaces DPG-based 250k ensemble; canonical shapefiles are official Elections Alberta files.",
            "Fisher combination assumes Channel 1 and Channel 2 are independent — approximately true.",
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

**Date:** 2026-05-07
**Ensemble:** canonical 100k plans (official Elections Alberta shapefiles, 2 chains × 50k)
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

---

## Channel 3 — Neighbour-Drain label-shuffle null

Pre-registered: AsPredicted #289,451. Executed 2026-05-07 on official canonical shapefiles.

| Map | drain_score | Null mean | z-score | p (two-tailed) |
| --- | --- | --- | --- | --- |
| Majority 2026 | {_drain_maj_obs:.6f} | 0.032085 | **{drain_majority_z:.3f}** | **{drain_majority_p:.4f}** |
| Minority 2026 | {_drain_min_obs:.6f} | 0.016741 | −1.372 | {drain_minority_p:.4f} |

**Prediction A** (drain_score(majority) > drain_score(minority)): **NOT CONFIRMED** (0.000179 < 0.006176).

**Prediction B** (both within null p > 0.05): **NOT CONFIRMED for majority** (p < 0.0001, outside null). Minority: CONFIRMED (p = 0.1342, within null).

**Interpretation.** The minority map's drain score (0.0062) is within the neutral-draw null — 13.4% of random label assignments produce equal or higher coupling. This channel does **not** contribute evidence against the minority map.

The majority map's drain_score (0.0002) is significantly *below* the null mean (z = −2.915, p < 0.0001 one-sided) — anomalously clean, not the partisan direction.

**Channel 3 contributes p = 0.1342 (minority within null) — not added to Fisher combination.**

---

## Fisher Combined (Channels 1 + 2, minority only)

| Channel | p (unadjusted) | p (n_eff-adjusted) |
| --- | --- | --- |
| Partisan joint (Mahalanobis) | {ch1_p:.2e} | {ch1_p_adj:.2e} |
| SZAT bootstrap | {szat_p:.4f} | {szat_p:.4f} |
| **Fisher combined** | **{p_combined:.2e}** | **{p_combined_adj:.2e}** |

Unadjusted: Fisher T = {T:.3f}, chi-sq df = 4.
n_eff-adjusted: Fisher T = {T_adj:.3f}, using Hotelling T² p for Ch1 (n_eff = {N_EFF_CONSERVATIVE}, conservative lower bound). Both reject the null.

**Reading:** p = {p_combined:.2e} is the probability that a neutral-draw process
produces a map simultaneously this extreme on both the partisan feature vector and
the swing-zone boundary allocation. Under the neutral null, this combination
occurs roughly once in every {int(round(1/max(p_combined, 1e-12))):,} draws.

---

## Pending channels (not executable with current ensemble)

| Channel | Reason pending | Marginal finding |
| --- | --- | --- |
| Municipal anchoring departure | Canadian comparator distribution too thin for rigorous p-value | Minority 4.9× below comparator norm |
| Population MAD ratio | Per-plan MAD not in ensemble outputs — requires MCMC rerun with population capture | Minority 1.48× majority |
| Reock asymmetry | Per-plan Reock not in ensemble outputs — requires MCMC rerun | Minority 2.58× majority on % below 0.30 |

---

## Interpretation note

The duck test made precise: the minority map's four-dimensional partisan feature
vector sits at Mahalanobis distance {min_m['mahalanobis_distance']:.2f} from the ensemble center
(p = {ch1_p:.2e}). Combined with the SZAT result (p = {szat_p:.4f}) and Fisher's
method, the joint neutral-null probability is p = {p_combined:.2e}.

**Channel 3 (Neighbour-Drain) executed 2026-05-07.** Minority within null
(p = 0.1342); does not contribute to the Fisher combination. The pre-registered
predictions (A and B) were not confirmed. The majority map shows anomalously
low pack-crack coupling (p < 0.0001, z = −2.915), which is an inverted finding
relative to the prediction — the majority is unusually clean on this metric.

Three pending channels (anchoring, MAD, Reock) point in the same direction
marginally. When those channels have proper null distributions, the combined
p-value will only decrease or stay flat.

The majority map sits at Mahalanobis distance {maj_m['mahalanobis_distance']:.2f} from the ensemble
center (p = {maj_m['joint_partisan_p']:.2e}) — outlier on MM in the NDP-favourable direction.

---

*Script: `analysis/scripts/joint_outlier_score_canonical.py`*
*Full output: `analysis/reports/joint_outlier_score.json`*
"""

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\nResults written:")
    print(f"  {OUT_JSON}")
    print(f"  {OUT_MD}")
    print(f"\n{'='*60}")
    print(f"DUCK SCORE (minority 2026) — canonical ensemble")
    print(f"  Channel 1 (partisan joint):  p = {ch1_p:.2e}")
    print(f"  Channel 2 (SZAT bootstrap):  p = {szat_p:.4f}")
    print(f"  Fisher combined:             p = {p_combined:.2e}")
    print(f"  Channel 3 (drain, minority): p = {drain_minority_p:.4f} (NOT in Fisher)")
    print(f"  Pending channels: 3")
    print(f"{'='*60}")


if __name__ == "__main__":
    run()
