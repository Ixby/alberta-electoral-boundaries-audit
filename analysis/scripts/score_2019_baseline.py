"""
score_2019_baseline.py
-----------------------
Scores the 2019 enacted Alberta electoral map against the canonical 250k
MCMC ensemble. Outputs Mahalanobis D² (joint-tail test) plus per-metric
percentile placements for all metrics where 2019 data exists.

Metrics scored
--------------
  Partisan (from simulation_real_map_scores_canonical.json, pre-computed):
    efficiency_gap, mean_median, declination, seats_at_50_50
  Joint (computed here):
    Mahalanobis D² over [EG, MM, Declination, S50], p-value from chi2(4)
  Population:
    population_mad — computed from alberta_2019_populations.csv;
    NOTE: 2019 map has 87 EDs; canonical ensemble is 89-seat.  Quota
    denominators differ, so ensemble percentile placement is reported with
    a caveat.  Raw MAD is the primary comparable statistic.
  Compactness:
    reock_proxy_median, reock_proxy_pct_below_030 — 2019 shapefile not
    yet loaded for Reock computation; these are flagged as N/A.

Inputs
------
  data/simulated_ensemble_raw_samples_canonical.csv
  data/simulation_real_map_scores_canonical.json
  data/reference/alberta_2019_populations.csv
  data/simulated_ensemble_percentiles_canonical.csv

Outputs
-------
  data/outputs/score_2019_baseline.json
  (printed summary to stdout)

Usage
-----
    python analysis/scripts/score_2019_baseline.py

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

DATA = data_loader._resolve_path("data")
REFERENCE = DATA.parent / "data" / "reference"
if not REFERENCE.exists():
    REFERENCE = DATA / "reference"

SAMPLES_CSV = DATA / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"
SCORES_JSON = DATA / "outputs" / "simulation_real_map_scores_canonical.json"
PERCENTILES_CSV = DATA / "outputs" / "simulated_ensemble_percentiles_canonical.csv"
POP_2019_CSV = REFERENCE / "alberta_2019_populations.csv"
OUT_JSON = DATA / "outputs" / "score_2019_baseline.json"

MAHAL_METRICS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]


def pct_rank(arr: np.ndarray, val: float) -> float:
    """Percentile rank of val in arr (fraction below × 100)."""
    return float(np.mean(arr < val) * 100)


def mahalanobis_score(
    samples: pd.DataFrame, metric_keys: list[str], x: np.ndarray
) -> dict:
    """
    Compute Mahalanobis D² and chi2 p-value for vector x given ensemble samples.

    Uses the empirical covariance matrix of metric_keys columns from samples.
    p-value: fraction of ensemble samples with D² >= D²(x).
    Also reports chi2(k) approximation p-value.
    """
    X = samples[metric_keys].dropna().values
    mu = X.mean(axis=0)
    cov = np.cov(X.T)
    cov_inv = np.linalg.inv(cov)

    diff = x - mu
    d2_x = float(diff @ cov_inv @ diff)

    # Empirical p-value: fraction of ensemble maps more extreme than x
    diffs_ens = X - mu
    d2_ens = np.einsum("ij,jk,ik->i", diffs_ens, cov_inv, diffs_ens)
    p_empirical = float(np.mean(d2_ens >= d2_x))

    # Chi-squared approximation (asymptotic; valid for large n)
    k = len(metric_keys)
    p_chi2 = float(1 - stats.chi2.cdf(d2_x, df=k))

    return {
        "d2": round(d2_x, 4),
        "p_empirical": round(p_empirical, 6),
        "p_chi2": round(p_chi2, 6),
        "mean_vector": mu.tolist(),
        "n_ensemble": int(len(X)),
        "k_metrics": k,
    }


def compute_2019_pop_mad(pop_csv: Path, n_seats: int = 87) -> dict:
    """
    Compute population MAD for the 2019 map.

    Uses population_2017_report column (EBC-reported 2017 populations).
    Quota = sum / n_seats (statutory standard).
    MAD = median absolute deviation from quota.
    """
    df = pd.read_csv(pop_csv)
    pops = df["population_2017_report"].values
    total = float(pops.sum())
    quota = total / n_seats
    deviations = np.abs(pops - quota)
    mad = float(np.median(deviations))
    mean_abs_dev = float(np.mean(deviations))
    max_dev = float(deviations.max())
    max_dev_pct = float(deviations.max() / quota * 100)
    min_dev = float(deviations.min())

    return {
        "n_seats": n_seats,
        "total_population": total,
        "quota": round(quota, 2),
        "population_mad": round(mad, 2),
        "mean_abs_deviation": round(mean_abs_dev, 2),
        "max_abs_deviation": round(max_dev, 2),
        "max_deviation_pct": round(max_dev_pct, 2),
        "min_abs_deviation": round(min_dev, 2),
        "note": (
            "2019 map has 87 EDs; canonical ensemble is 89-seat. "
            "Quota denominators differ — ensemble percentile placement not valid. "
            "Raw MAD reported for cross-map comparison only."
        ),
    }


def main():
    print("Loading canonical ensemble samples...", flush=True)
    samples = pd.read_csv(SAMPLES_CSV)
    print(f"  {len(samples):,} samples loaded", flush=True)

    print("Loading canonical real-map scores...", flush=True)
    with open(SCORES_JSON, encoding="utf-8") as f:
        scores_json = json.load(f)

    print("Loading canonical percentiles...", flush=True)
    pct_df = pd.read_csv(PERCENTILES_CSV)

    # ── 2019 enacted metric vector ─────────────────────────────────────────────
    m_2019 = scores_json["2019_enacted"]
    x_2019 = np.array([m_2019[k] for k in MAHAL_METRICS])

    print(f"\n2019 enacted metric vector:")
    for k, v in zip(MAHAL_METRICS, x_2019):
        print(f"  {k:<22s} {v:+.6f}")

    # ── Per-metric percentile placement (from pre-computed CSV) ───────────────
    print("\nPer-metric percentile placements (from canonical percentiles CSV):")
    metric_summary = {}
    for key in MAHAL_METRICS:
        row = pct_df[
            (pct_df["metric"] == key) & (pct_df["map"] == "2019 enacted")
        ]
        if len(row) == 0:
            print(f"  {key:<22s}  NOT FOUND in percentiles CSV — computing...")
            arr = samples[key].dropna().values
            val = m_2019.get(key, float("nan"))
            pr = pct_rank(arr, val) if not np.isnan(val) else float("nan")
            metric_summary[key] = {
                "value": round(val, 6),
                "percentile": round(pr, 4),
                "source": "computed",
            }
        else:
            r = row.iloc[0]
            print(
                f"  {key:<22s}  val={r['value']:+.6f}  "
                f"p{r['percentile']:.2f}  "
                f"[p5={r['ensemble_p5']:+.4f} "
                f"p50={r['ensemble_p50']:+.4f} "
                f"p95={r['ensemble_p95']:+.4f}]"
            )
            metric_summary[key] = {
                "value": round(float(r["value"]), 6),
                "percentile": round(float(r["percentile"]), 4),
                "ensemble_p5": round(float(r["ensemble_p5"]), 6),
                "ensemble_p50": round(float(r["ensemble_p50"]), 6),
                "ensemble_p95": round(float(r["ensemble_p95"]), 6),
                "source": "canonical_percentiles_csv",
            }

    # Also score population_mad and reock against 2019 (N/A for 2019 in canonical CSV)
    # population_mad: we'll compute from reference CSV and note incomparability
    # reock: not available for 2019 shapefile — mark N/A
    metric_summary["population_mad"] = {"value": None, "percentile": None,
                                        "note": "see pop_2019 section below"}
    metric_summary["reock_proxy_median"] = {"value": None, "percentile": None,
                                            "note": "2019 shapefile Reock not computed"}
    metric_summary["reock_proxy_pct_below_030"] = {"value": None, "percentile": None,
                                                    "note": "2019 shapefile Reock not computed"}

    # ── Mahalanobis joint test ─────────────────────────────────────────────────
    print("\nComputing Mahalanobis D² for 2019 enacted...", flush=True)
    mahal_2019 = mahalanobis_score(samples, MAHAL_METRICS, x_2019)
    print(f"  D²            = {mahal_2019['d2']:.4f}")
    print(f"  p (empirical) = {mahal_2019['p_empirical']:.6f}  "
          f"({mahal_2019['p_empirical']*100:.2f}% of ensemble maps more extreme)")
    print(f"  p (chi2 approx) = {mahal_2019['p_chi2']:.6f}")

    # Compare to majority and minority
    m_maj = scores_json["majority_2026"]
    m_min = scores_json["minority_2026"]
    x_maj = np.array([m_maj[k] for k in MAHAL_METRICS])
    x_min = np.array([m_min[k] for k in MAHAL_METRICS])

    mahal_maj = mahalanobis_score(samples, MAHAL_METRICS, x_maj)
    mahal_min = mahalanobis_score(samples, MAHAL_METRICS, x_min)

    print(f"\nMahalanobis comparison (all three maps):")
    print(f"  {'Map':<28s}  {'D²':>8s}  {'p_empirical':>12s}  {'p_chi2':>10s}")
    print(f"  {'2019 enacted':<28s}  {mahal_2019['d2']:>8.4f}  "
          f"{mahal_2019['p_empirical']:>12.6f}  {mahal_2019['p_chi2']:>10.6f}")
    print(f"  {'majority 2026 (canonical)':<28s}  {mahal_maj['d2']:>8.4f}  "
          f"{mahal_maj['p_empirical']:>12.6f}  {mahal_maj['p_chi2']:>10.6f}")
    print(f"  {'minority 2026 (canonical)':<28s}  {mahal_min['d2']:>8.4f}  "
          f"{mahal_min['p_empirical']:>12.6f}  {mahal_min['p_chi2']:>10.6f}")

    # ── 2019 Population MAD ────────────────────────────────────────────────────
    print("\nComputing 2019 Population MAD...", flush=True)
    pop_2019 = compute_2019_pop_mad(POP_2019_CSV, n_seats=87)
    print(f"  Seats:         {pop_2019['n_seats']}")
    print(f"  Total pop:     {pop_2019['total_population']:,.0f}")
    print(f"  Quota:         {pop_2019['quota']:,.2f}")
    print(f"  Population MAD: {pop_2019['population_mad']:,.2f}")
    print(f"  Max deviation:  {pop_2019['max_abs_deviation']:,.2f} "
          f"({pop_2019['max_deviation_pct']:.1f}%)")
    print(f"  {pop_2019['note']}")

    # Compare to 2026 maps (same quota denominator issue; note separately)
    mad_maj = scores_json["majority_2026"].get("population_mad", None)
    mad_min = scores_json["minority_2026"].get("population_mad", None)
    print(f"\nPopulation MAD comparison (raw, different denominators):")
    print(f"  2019 enacted (87 seats, 2017 pops):  {pop_2019['population_mad']:>10,.2f}")
    print(f"  majority 2026 (89 seats):             {mad_maj if mad_maj else 'N/A':>10}")
    print(f"  minority 2026 (89 seats):             {mad_min if mad_min else 'N/A':>10}")

    # ── Direction-of-travel summary ────────────────────────────────────────────
    print("\n" + "="*70)
    print("DIRECTION-OF-TRAVEL SUMMARY")
    print("="*70)
    print(f"{'Metric':<22}  {'2019 enacted':>14}  {'maj 2026':>10}  {'min 2026':>10}")
    print("-"*60)
    metric_labels = {
        "efficiency_gap": "EG",
        "mean_median": "MM",
        "declination": "Declination",
        "seats_at_50_50": "Seats@50/50",
    }
    for key in MAHAL_METRICS:
        v19 = metric_summary[key]["value"]
        p19 = metric_summary[key]["percentile"]
        vmaj = m_maj.get(key)
        vmaj_pct = pct_df[(pct_df["metric"]==key) & (pct_df["map"]=="majority 2026 canonical")]
        vmin = m_min.get(key)
        vmin_pct = pct_df[(pct_df["metric"]==key) & (pct_df["map"]=="minority 2026 canonical")]

        pmaj = float(vmaj_pct.iloc[0]["percentile"]) if len(vmaj_pct) > 0 else float("nan")
        pmin = float(vmin_pct.iloc[0]["percentile"]) if len(vmin_pct) > 0 else float("nan")

        print(f"  {metric_labels.get(key, key):<20}  "
              f"p{p19:5.1f}  "
              f"p{pmaj:5.1f}  "
              f"p{pmin:5.1f}")

    print(f"\n  Mahalanobis D²:")
    print(f"  {'2019 enacted':<20}  D²={mahal_2019['d2']:.2f}  "
          f"p={mahal_2019['p_empirical']:.4f}")
    print(f"  {'majority 2026':<20}  D²={mahal_maj['d2']:.2f}  "
          f"p={mahal_maj['p_empirical']:.6f}")
    print(f"  {'minority 2026':<20}  D²={mahal_min['d2']:.2f}  "
          f"p={mahal_min['p_empirical']:.6f}")

    # ── Write output JSON ──────────────────────────────────────────────────────
    out = {
        "description": (
            "2019 enacted Alberta electoral map scored against canonical 250k "
            "MCMC ensemble. Partisan metrics from simulation_real_map_scores_canonical.json. "
            "Mahalanobis D² computed from ensemble empirical covariance."
        ),
        "ensemble_n": len(samples),
        "metric_vector_2019": {k: v for k, v in zip(MAHAL_METRICS, x_2019.tolist())},
        "per_metric": metric_summary,
        "mahalanobis": {
            "2019_enacted": mahal_2019,
            "majority_2026_canonical": mahal_maj,
            "minority_2026_canonical": mahal_min,
            "metric_keys": MAHAL_METRICS,
        },
        "population_mad_2019": pop_2019,
        "population_mad_2026": {
            "majority": mad_maj,
            "minority": mad_min,
            "note": "2026 values from simulation_real_map_scores_canonical.json (89-seat quota)",
        },
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nOutput written: {OUT_JSON}")


if __name__ == "__main__":
    main()
