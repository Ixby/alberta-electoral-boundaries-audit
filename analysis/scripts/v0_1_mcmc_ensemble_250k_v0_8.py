"""v0.1 MCMC ensemble — 250k rigorous run against v0_8 DPGs.

Follow-up to v0_1_mcmc_ensemble_100k.py. This script runs a 250,000-step
ReCom chain from the 2019 enacted Alberta ED seed, scores each sample on
four partisan-bias metrics, and computes convergence diagnostics. It uses
the v0_8 refined GPKGs (or canonical fallback) for the 2026 maps.

Outputs
-------
- data/v0_1_mcmc_ensemble_samples_250k_v0_8.csv
- data/v0_1_mcmc_real_map_scores_250k_v0_8.json
- data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv
- data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.json
- data/maps/mcmc/ensemble_distribution_250k_v0_8_{metric}.png
- data/maps/mcmc/running_mean_250k_v0_8_{metric}.png

Usage
-----
    python analysis/scripts/v0_1_mcmc_ensemble_250k_v0_8.py [--n-steps 250000]

Forward: analysis/methodology/v0_1_mcmc_v0_8_rigorous.md
Backward:
  data/va_polygons_with_2023_votes.gpkg
  data/shapefiles/derived/v0_8_refined_*_2026_eds.gpkg (preferred)
  data/shapefiles/derived/v0_8_canonical_*_2026_eds.gpkg (fallback)
  gerrychain, geopandas, matplotlib, numpy, pandas
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
    MAJ_V7_PATH,
    MIN_V7_PATH,
    MAJ_V8_PATH,
    MIN_V8_PATH,
    MAJ_V8_CANON_PATH,
    MIN_V8_CANON_PATH,
)
from v0_1_mcmc_ensemble_100k import autocorrelation_ess, plot_running_mean

ROOT = HERE.parent.parent
DATA = ROOT / "data"
MAPS = ROOT / "data" / "maps" / "mcmc"
MAPS.mkdir(parents=True, exist_ok=True)

SAMPLES_CSV = DATA / "v0_1_mcmc_ensemble_samples_250k_v0_8.csv"
SCORES_JSON = DATA / "v0_1_mcmc_real_map_scores_250k_v0_8.json"
PERCENTILES_CSV = DATA / "v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv"
CONVERGENCE_JSON = DATA / "v0_1_mcmc_convergence_diagnostics_250k_v0_8.json"


def _select_v8_or_v7(plan: str):
    if plan == "majority":
        if MAJ_V8_PATH.exists():
            return MAJ_V8_PATH, "majority 2026 v8 refined (89 EDs)"
        if MAJ_V8_CANON_PATH.exists():
            return MAJ_V8_CANON_PATH, "majority 2026 v8 canonical (89 EDs)"
        return MAJ_V7_PATH, "majority 2026 v7 (89 EDs)"
    else:
        if MIN_V8_PATH.exists():
            return MIN_V8_PATH, "minority 2026 v8 refined (89 EDs)"
        if MIN_V8_CANON_PATH.exists():
            return MIN_V8_CANON_PATH, "minority 2026 v8 canonical (89 EDs)"
        return MIN_V7_PATH, "minority 2026 v7 (89 EDs)"


def main(n_steps: int = 250000, seed: int = 42, pop_deviation: float = 0.25):
    np.random.seed(seed)
    import random as _random
    _random.seed(seed)

    t_start = time.time()
    label_run = f"250k v0_8 rigorous ensemble"
    print(f"[{time.strftime('%H:%M:%S')}] {label_run} starting — "
          f"n_steps={n_steps}, seed={seed}, pop_deviation=±{pop_deviation:.0%}")

    va, graph = build_va_graph()

    assignment = initial_assignment_2019(va)
    districts_2019 = set(assignment.values())
    print(f"  2019 baseline districts: {len(districts_2019)}")

    agg = va.groupby("parent_ed_2019").agg(
        ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum")
    ).reset_index()
    m_2019 = seat_results(agg["ucp"].values, agg["ndp"].values)
    m_2019["source"] = "2019_enacted_VA_agg"
    m_2019["coverage_vas"] = int(len(va))
    m_2019["coverage_vas_total"] = int(len(va))
    m_2019["coverage_pct"] = 1.0
    m_2019["votes_coverage_pct"] = 1.0

    maj_path, maj_label = _select_v8_or_v7("majority")
    min_path, min_label = _select_v8_or_v7("minority")
    print(f"  using majority: {maj_path.name}")
    print(f"  using minority: {min_path.name}")
    m_maj = score_exogenous_map(va, maj_path)
    m_min = score_exogenous_map(va, min_path)

    print()
    print("  --- Real-map scores (pre-ensemble) ---")
    for name, m in [("2019 enacted", m_2019), (maj_label, m_maj), (min_label, m_min)]:
        print(f"    {name}: seats={m['ucp_seats']}/{m['n_districts']}  "
              f"EG={m['efficiency_gap']:+.4f}  MM={m['mean_median']:+.4f}  "
              f"decl={m['declination']:+.4f}  s50={m['seats_at_50_50']:.3f}  "
              f"ucp_share={m['ucp_vote_share']:.3f}  cov={m['coverage_pct']:.2%}")

    print()
    print(f"[{time.strftime('%H:%M:%S')}] running ReCom chain ({n_steps} steps)...")
    rows = run_ensemble(graph, assignment, n_steps, pop_deviation=pop_deviation)
    df = pd.DataFrame(rows)
    df.to_csv(SAMPLES_CSV, index=False)
    print(f"  wrote {SAMPLES_CSV.name} ({len(df)} samples) in {time.time()-t_start:.0f}s total")

    print()
    print("  --- Convergence diagnostics (full 250k) ---")
    metrics_config = [
        ("efficiency_gap", "Efficiency gap (UCP-favoured if positive)"),
        ("mean_median", "Mean-median (UCP share; UCP-favoured if positive)"),
        ("declination", "Declination (UCP-favoured if positive)"),
        ("seats_at_50_50", "UCP seat share at 50/50 vote (uniform swing)"),
    ]
    conv = {}
    for key, label in metrics_config:
        diag = autocorrelation_ess(df[key].values)
        conv[key] = diag
        print(f"    {key:<18s} n={diag['n']}  tau={diag['tau']:.2f}  "
              f"n_eff={diag['n_eff']:.0f}  rho1={diag['rho_lag_1']:+.3f}  "
              f"rho10={diag['rho_lag_10']:+.3f}  rho100={diag['rho_lag_100']:+.3f}")
        plot_running_mean(
            key, df[key].values,
            MAPS / f"running_mean_250k_v0_8_{key}.png",
            label,
        )

    with open(CONVERGENCE_JSON, "w", encoding="utf-8") as f:
        json.dump(conv, f, indent=2, default=float)
    print(f"  wrote {CONVERGENCE_JSON.name}")

    real_maps = {
        "2019 enacted": m_2019,
        maj_label: m_maj,
        min_label: m_min,
    }

    summary = []
    for key, label in metrics_config:
        real_vals = {k: v.get(key, float("nan")) for k, v in real_maps.items()}
        plot_metric(key, label, df[key].values, real_vals,
                    MAPS / f"ensemble_distribution_250k_v0_8_{key}.png")
        for map_name, val in real_vals.items():
            pr = pct_rank(df[key].dropna().values, val) if not np.isnan(val) else float("nan")
            summary.append({
                "metric": key,
                "map": map_name,
                "value": val,
                "percentile": pr,
                "ensemble_p5": float(np.nanpercentile(df[key], 5)),
                "ensemble_p50": float(np.nanpercentile(df[key], 50)),
                "ensemble_p95": float(np.nanpercentile(df[key], 95)),
            })

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(PERCENTILES_CSV, index=False)
    print(f"  wrote {PERCENTILES_CSV.name}")

    print()
    print("  --- Per-metric percentiles (real maps vs 250k ensemble) ---")
    with pd.option_context("display.float_format", "{:+.4f}".format,
                           "display.max_rows", None,
                           "display.width", 160):
        print(summary_df.to_string(index=False))

    real_json = {
        "2019_enacted": m_2019,
        "majority_2026": m_maj,
        "majority_source": maj_label,
        "minority_2026": m_min,
        "minority_source": min_label,
        "n_steps": int(n_steps),
        "seed": int(seed),
    }
    with open(SCORES_JSON, "w", encoding="utf-8") as f:
        json.dump(real_json, f, indent=2, default=float)
    print(f"  wrote {SCORES_JSON.name}")

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
            print(f"    {fl['map']:<48s} {fl['metric']:<18s} value={fl['value']:+.4f}  p={fl['percentile']:.1f}")

    print()
    print(f"[{time.strftime('%H:%M:%S')}] done. total wall time {time.time()-t_start:.0f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-steps", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pop-deviation", type=float, default=0.25)
    args = parser.parse_args()
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    main(n_steps=args.n_steps, seed=args.seed, pop_deviation=args.pop_deviation)
