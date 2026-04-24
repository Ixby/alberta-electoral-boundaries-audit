"""v0.1 MCMC ensemble gerrymandering test — 100k publication-grade run.

Purpose
-------
Follow-up to v0_1_mcmc_ensemble.py (10k preliminary run). This script runs
a 100,000-step ReCom chain from the 2019 enacted Alberta ED seed, scores
each sample on four partisan-bias metrics, and computes convergence
diagnostics (effective sample size per metric, running-mean trace plots).

It writes to _100k-suffixed outputs so the 10k artifacts survive.

Outputs
-------
- data/v0_1_mcmc_ensemble_samples_100k.csv
- data/v0_1_mcmc_real_map_scores_100k.json
- data/v0_1_mcmc_ensemble_percentiles_100k.csv
- data/v0_1_mcmc_convergence_diagnostics_100k.json
- maps/mcmc/ensemble_distribution_100k_{metric}.png
- maps/mcmc/running_mean_100k_{metric}.png

Usage
-----
    python analysis/v0_1_mcmc_ensemble_100k.py [--n-steps 100000]

Forward: analysis/v0_1_mcmc_100k_and_full_coverage.md
Backward:
  data/va_polygons_with_2023_votes.gpkg
  data/va_pop_from_das.csv
  data/v0_1_approximate_majority_2026_eds.gpkg
  data/v0_1_refined_v6_minority_2026_eds.gpkg
  gerrychain, geopandas, matplotlib, numpy, pandas
"""
from __future__ import annotations

import os
import sys
import time
import json
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Reuse all functions from the sibling script
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v0_1_mcmc_ensemble import (
    build_va_graph,
    initial_assignment_2019,
    score_exogenous_map,
    run_ensemble,
    seat_results,
    pct_rank,
    plot_metric,
    MAJ_PATH,
    MIN_V6_PATH,
    MIN_V5_PATH,
)

ROOT = HERE.parent
DATA = ROOT / "data"
MAPS = ROOT / "maps" / "mcmc"
MAPS.mkdir(parents=True, exist_ok=True)

SAMPLES_CSV_100K = DATA / "v0_1_mcmc_ensemble_samples_100k.csv"
SCORES_JSON_100K = DATA / "v0_1_mcmc_real_map_scores_100k.json"
PERCENTILES_CSV_100K = DATA / "v0_1_mcmc_ensemble_percentiles_100k.csv"
CONVERGENCE_JSON_100K = DATA / "v0_1_mcmc_convergence_diagnostics_100k.json"


# ---- convergence diagnostics -----------------------------------------------

def autocorrelation_ess(x: np.ndarray, max_lag: int | None = None) -> dict:
    """Compute integrated autocorrelation time and effective sample size.

    Uses the standard n_eff = n / tau formula where
    tau = 1 + 2 * sum_{k=1..M} rho_k  (Geyer initial positive sequence).

    We truncate the sum at the first lag where rho_k <= 0 (Geyer 1992).
    """
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 4:
        return {"n": int(n), "tau": float("nan"), "n_eff": float("nan"),
                "max_lag_used": 0}

    x_centered = x - x.mean()
    var0 = np.dot(x_centered, x_centered) / n
    if var0 == 0 or not np.isfinite(var0):
        return {"n": int(n), "tau": float("nan"), "n_eff": float("nan"),
                "max_lag_used": 0}

    if max_lag is None:
        max_lag = min(n // 4, 2000)

    # FFT-based autocovariance is faster for long chains
    # but a simple lag loop is fine at O(n * max_lag) when max_lag is bounded.
    acf = np.empty(max_lag + 1, dtype=float)
    acf[0] = 1.0
    for k in range(1, max_lag + 1):
        cov = np.dot(x_centered[:-k], x_centered[k:]) / n
        acf[k] = cov / var0

    # Geyer initial positive sequence: truncate at first k where acf[k] <= 0
    tau = 1.0
    used_lag = max_lag
    for k in range(1, max_lag + 1):
        if acf[k] <= 0:
            used_lag = k - 1
            break
        tau += 2.0 * acf[k]

    n_eff = n / tau if tau > 0 else float("nan")
    return {
        "n": int(n),
        "tau": float(tau),
        "n_eff": float(n_eff),
        "max_lag_used": int(used_lag),
        "rho_lag_1": float(acf[1]) if max_lag >= 1 else float("nan"),
        "rho_lag_10": float(acf[10]) if max_lag >= 10 else float("nan"),
        "rho_lag_100": float(acf[100]) if max_lag >= 100 else float("nan"),
    }


def plot_running_mean(metric_key: str, values: np.ndarray, out_path: Path,
                      label: str):
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    if len(v) == 0:
        return
    idx = np.arange(1, len(v) + 1)
    rmean = np.cumsum(v) / idx

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(idx, rmean, color="#1f2937", linewidth=1.0)
    ax.axhline(v.mean(), linestyle="--", color="#888", linewidth=0.8,
               label=f"final mean = {v.mean():+.5f}")
    ax.set_xlabel("Sample index")
    ax.set_ylabel(f"Running mean of {label}")
    ax.set_title(f"Running mean — {label}  (100k ReCom samples, seed 42)")
    ax.grid(axis="both", linestyle=":", linewidth=0.5, alpha=0.6)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)


# ---- main -------------------------------------------------------------------

def main(n_steps: int = 100000, seed: int = 42, thin_every: int | None = None):
    np.random.seed(seed)
    import random as _random
    _random.seed(seed)

    t_start = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] 100k ensemble run starting — n_steps={n_steps}, seed={seed}")

    va, graph = build_va_graph()

    # -- Initial 2019 assignment
    assignment = initial_assignment_2019(va)
    districts_2019 = set(assignment.values())
    print(f"  2019 baseline districts (from parent_ed_2019): {len(districts_2019)}")

    # -- Real-map scores
    agg = va.groupby("parent_ed_2019").agg(
        ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum")
    ).reset_index()
    m_2019 = seat_results(agg["ucp"].values, agg["ndp"].values)
    m_2019["source"] = "2019_enacted_VA_agg"
    m_2019["coverage_vas"] = int(len(va))
    m_2019["coverage_vas_total"] = int(len(va))
    m_2019["coverage_pct"] = 1.0
    m_2019["votes_coverage_pct"] = 1.0

    m_maj = score_exogenous_map(va, MAJ_PATH)
    if MIN_V6_PATH.exists():
        m_min = score_exogenous_map(va, MIN_V6_PATH)
        min_label = "minority 2026 v6 (approx)"
    else:
        m_min = score_exogenous_map(va, MIN_V5_PATH)
        min_label = "minority 2026 v5 (approx)"

    print()
    print("  --- Real-map scores (pre-ensemble) ---")
    for name, m in [("2019 enacted", m_2019), ("majority 2026 approx", m_maj), (min_label, m_min)]:
        print(f"    {name}: seats={m['ucp_seats']}/{m['n_districts']}  "
              f"EG={m['efficiency_gap']:+.4f}  MM={m['mean_median']:+.4f}  "
              f"decl={m['declination']:+.4f}  s50={m['seats_at_50_50']:.3f}  "
              f"ucp_share={m['ucp_vote_share']:.3f}  cov={m['coverage_pct']:.2%}")

    # -- Run chain
    print()
    print(f"[{time.strftime('%H:%M:%S')}] running ReCom chain ({n_steps} steps)...")
    rows = run_ensemble(graph, assignment, n_steps)
    df = pd.DataFrame(rows)
    df.to_csv(SAMPLES_CSV_100K, index=False)
    print(f"  wrote {SAMPLES_CSV_100K} ({len(df)} samples) in {time.time()-t_start:.0f}s total")

    # -- Optional thinning
    df_full = df
    df_thin = None
    if thin_every and thin_every > 1:
        df_thin = df.iloc[::thin_every].copy()
        print(f"  thinned to every {thin_every} -> {len(df_thin)} samples")

    # -- Convergence diagnostics on full chain
    print()
    print("  --- Convergence diagnostics (full 100k) ---")
    metrics_config = [
        ("efficiency_gap", "Efficiency gap (UCP-favoured if positive)"),
        ("mean_median", "Mean-median (UCP share; UCP-favoured if positive)"),
        ("declination", "Declination (UCP-favoured if positive)"),
        ("seats_at_50_50", "UCP seat share at 50/50 vote (uniform swing)"),
    ]
    conv = {}
    for key, label in metrics_config:
        diag = autocorrelation_ess(df_full[key].values)
        conv[key] = diag
        print(f"    {key:<18s} n={diag['n']}  tau={diag['tau']:.2f}  "
              f"n_eff={diag['n_eff']:.0f}  rho1={diag['rho_lag_1']:+.3f}  "
              f"rho10={diag['rho_lag_10']:+.3f}  rho100={diag['rho_lag_100']:+.3f}  "
              f"max_lag={diag['max_lag_used']}")
        plot_running_mean(
            key, df_full[key].values,
            MAPS / f"running_mean_100k_{key}.png",
            label,
        )

    with open(CONVERGENCE_JSON_100K, "w", encoding="utf-8") as f:
        json.dump(conv, f, indent=2, default=float)
    print(f"  wrote {CONVERGENCE_JSON_100K}")

    # -- Per-metric plots + percentiles on FULL 100k
    real_maps = {
        "2019 enacted": m_2019,
        "majority 2026 (approx)": m_maj,
        min_label: m_min,
    }

    summary = []
    for key, label in metrics_config:
        real_vals = {k: v.get(key, float("nan")) for k, v in real_maps.items()}
        plot_metric(key, label, df_full[key].values, real_vals,
                    MAPS / f"ensemble_distribution_100k_{key}.png")
        for map_name, val in real_vals.items():
            pr = pct_rank(df_full[key].dropna().values, val) if not np.isnan(val) else float("nan")
            summary.append({
                "metric": key,
                "map": map_name,
                "value": val,
                "percentile": pr,
                "ensemble_p5": float(np.nanpercentile(df_full[key], 5)),
                "ensemble_p50": float(np.nanpercentile(df_full[key], 50)),
                "ensemble_p95": float(np.nanpercentile(df_full[key], 95)),
            })

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(PERCENTILES_CSV_100K, index=False)
    print(f"  wrote {PERCENTILES_CSV_100K}")

    print()
    print("  --- Per-metric percentiles (real maps vs 100k ensemble) ---")
    with pd.option_context("display.float_format", "{:+.4f}".format,
                           "display.max_rows", None,
                           "display.width", 160):
        print(summary_df.to_string(index=False))

    # -- Persist scores JSON
    real_json = {
        "2019_enacted": m_2019,
        "majority_2026_approx": m_maj,
        "minority_2026_approx": m_min,
        "minority_source": min_label,
        "n_steps": int(n_steps),
        "seed": int(seed),
        "thin_every": int(thin_every) if thin_every else None,
    }
    with open(SCORES_JSON_100K, "w", encoding="utf-8") as f:
        json.dump(real_json, f, indent=2, default=float)
    print(f"  wrote {SCORES_JSON_100K}")

    # Flag outliers
    flags = []
    for row in summary:
        if np.isnan(row["percentile"]):
            continue
        if row["percentile"] >= 95 or row["percentile"] <= 5:
            flags.append(row)
    if flags:
        print()
        print("  *** OUTLIER FLAGS (>=95th or <=5th percentile) ***")
        for fl in flags:
            print(f"    {fl['map']:<32s} {fl['metric']:<18s} value={fl['value']:+.4f}  p={fl['percentile']:.1f}")

    print()
    print(f"[{time.strftime('%H:%M:%S')}] done. total wall time {time.time()-t_start:.0f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-steps", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--thin-every", type=int, default=None,
                        help="Optional thinning factor (e.g., 10). Default: no thinning.")
    args = parser.parse_args()
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    main(n_steps=args.n_steps, seed=args.seed, thin_every=args.thin_every)
