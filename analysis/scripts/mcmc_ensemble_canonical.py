"""
mcmc_ensemble_canonical.py
--------------------------
100k ReCom MCMC ensemble re-run against official Elections Alberta canonical
shapefiles (ea_majority_2026_eds.gpkg / ea_minority_2026_eds.gpkg).

Replaces the v0_10 DPG-based ensemble for all Lane-1 percentile placements.
Official geometry supersedes all DPG-derived files per 2026-05-07 directive.

Why rerun:
  The 100k pre-registered ensemble was run against v0_10 topological DPG
  geometry. Canonical shapefiles produce different VA-to-ED assignments and
  different ED vote totals, which shift the real-map metric values and
  therefore their ensemble percentile placements.

Differences from mcmc_ensemble_250k.py:
  - MAJ/MIN paths point to data/shapefiles/canonical/
  - score_exogenous_map called with id_col="EDName2025"
  - Output suffixed _canonical instead of _250k
  - Default n_steps=100000 (pre-registered ensemble size)
  - Checkpoint dir: simulation_checkpoints_canonical

Outputs
-------
  data/simulated_ensemble_raw_samples_canonical.csv
  data/simulation_real_map_scores_canonical.json
  data/simulated_ensemble_percentiles_canonical.csv
  data/simulation_convergence_diagnostics_canonical.json
  data/maps/mcmc/ensemble_distribution_canonical_{metric}.svg
  data/maps/mcmc/running_mean_canonical_{metric}.svg

Usage
-----
    python analysis/scripts/mcmc_ensemble_canonical.py [--n-steps 100000]

Backward dependencies:
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/canonical/ea_minority_2026_eds.gpkg
  data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg (or 2023_votes)
  analysis/scripts/mcmc_ensemble.py (build_va_graph, run_ensemble, seat_results)
  analysis/scripts/drand_seed.py

Forward dependencies:
  analysis/reports/joint_outlier_score_summary.md (Channel 1 update)
  analysis/reports/post_audit_recompute_deltas.md (canonical delta)
"""
from __future__ import annotations


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mcmc_ensemble import (
    build_va_graph,
    initial_assignment_2019,
    score_exogenous_map,
    run_ensemble,
    seat_results,
    pct_rank,
    plot_metric,
    autocorrelation_ess,
    plot_running_mean,
)

ROOT = HERE.parent.parent
DATA = data_loader._resolve_path("data")
MAPS = data_loader._resolve_path("data") / "maps" / "mcmc"
MAPS.mkdir(parents=True, exist_ok=True)

# Official Elections Alberta canonical shapefiles — supersede all DPG files.
MAJ_CANONICAL = DATA / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg"
MIN_CANONICAL = DATA / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"
CANONICAL_NAME_COL = "EDName2025"

SAMPLES_CSV     = DATA / "simulated_ensemble_raw_samples_canonical.csv"
SCORES_JSON     = DATA / "simulation_real_map_scores_canonical.json"
PERCENTILES_CSV = DATA / "simulated_ensemble_percentiles_canonical.csv"
CONVERGENCE_JSON = DATA / "simulation_convergence_diagnostics_canonical.json"
CHECKPOINT_DIR  = DATA / "simulation_checkpoints_canonical"

METRIC_KEYS = [
    "efficiency_gap", "mean_median", "declination", "seats_at_50_50",
    "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030",
]


def _run_chain_chunked(args):
    chain_idx, n_steps_total, base_seed, pop_deviation, chain_csv_path, chunk_size = args
    import random as _random
    import numpy as _np

    chain_csv_path = Path(chain_csv_path)
    chain_csv_path.parent.mkdir(parents=True, exist_ok=True)

    if chain_csv_path.exists():
        n_done = len(pd.read_csv(chain_csv_path))
    else:
        n_done = 0

    if n_done >= n_steps_total:
        print(f"  [chain {chain_idx}] already complete ({n_done}) -- skipping", flush=True)
        return str(chain_csv_path)

    chunks_done = n_done // chunk_size
    n_chunks = (n_steps_total + chunk_size - 1) // chunk_size
    print(f"  [chain {chain_idx}] {n_done}/{n_steps_total} done; resuming chunk {chunks_done}/{n_chunks}", flush=True)

    va, graph = build_va_graph()
    current_state = initial_assignment_2019(va)

    chain_seed = (base_seed * 100_000 + chain_idx * 1_000) % (2**32)
    _np.random.seed(chain_seed)
    _random.seed(chain_seed)

    t_chain = time.time()
    for chunk_idx in range(chunks_done, n_chunks):
        chunk_steps = min(chunk_size, n_steps_total - chunk_idx * chunk_size)
        t0 = time.time()
        rows, current_state = run_ensemble(
            graph, current_state, chunk_steps,
            pop_deviation=pop_deviation, verbose=False,
            return_final_partition=True, seed=chain_seed,
        )
        for r in rows:
            r["chain"] = chain_idx
            r["chunk"] = chunk_idx
        write_header = (not chain_csv_path.exists()) or chain_csv_path.stat().st_size == 0
        pd.DataFrame(rows).to_csv(chain_csv_path, mode="a", header=write_header, index=False)
        print(
            f"  [chain {chain_idx}] chunk {chunk_idx+1}/{n_chunks} "
            f"({len(rows)} samples, {time.time()-t0:.0f}s) -> {chain_csv_path.name}",
            flush=True,
        )

    print(f"  [chain {chain_idx}] done in {time.time()-t_chain:.0f}s", flush=True)
    return str(chain_csv_path)


def main(
    n_steps: int = 100_000,
    seed: int = None,
    pop_deviation: float = 0.25,
    n_chains: int = 4,
    chunk_size: int = 5000,
):
    from drand_seed import get_canonical_seed
    # Salt intentionally kept as "mcmc_ensemble_250k" for historical continuity:
    # the canonical 100k ensemble was seeded from this salt to preserve chain-of-
    # custody with the earlier DPG 250k run. Changing the salt would break
    # reproducibility of the pre-registered ensemble (OSF reg qsgy8).
    seed = seed if seed is not None else get_canonical_seed("mcmc_ensemble_250k")

    # va_pop_from_das.csv may have been moved to data/outputs/ during cleanup.
    # build_va_graph() expects it at DATA/va_pop_from_das.csv — create a symlink
    # or copy if it's only in the outputs subfolder.
    pop_cache_expected = DATA / "va_pop_from_das.csv"
    pop_cache_alternate = DATA / "outputs" / "va_pop_from_das.csv"
    if not pop_cache_expected.exists() and pop_cache_alternate.exists():
        import shutil
        shutil.copy2(pop_cache_alternate, pop_cache_expected)
        print(f"  copied va_pop_from_das.csv from outputs/ to data/", flush=True)

    np.random.seed(seed)
    import random as _random
    _random.seed(seed)

    t_start = time.time()
    n_steps_per_chain = (n_steps + n_chains - 1) // n_chains
    actual_total = n_steps_per_chain * n_chains

    print(f"[{time.strftime('%H:%M:%S')}] MCMC canonical ensemble starting", flush=True)
    print(f"  substrate: official Elections Alberta canonical shapefiles", flush=True)
    print(f"  n_steps={n_steps}, n_chains={n_chains}, steps/chain={n_steps_per_chain}", flush=True)
    print(f"  base_seed={seed}, pop_deviation=+/-{pop_deviation:.0%}", flush=True)

    # Verify canonical shapefiles exist
    for p in (MAJ_CANONICAL, MIN_CANONICAL):
        if not p.exists():
            raise FileNotFoundError(f"Canonical shapefile missing: {p}")
    print(f"  majority:  {MAJ_CANONICAL.name}", flush=True)
    print(f"  minority:  {MIN_CANONICAL.name}", flush=True)

    va, graph = build_va_graph()

    # Score 2019 enacted baseline (VA self-assignment)
    agg_2019 = (
        va.groupby("parent_ed_2019")
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    m_2019 = seat_results(agg_2019["ucp"].values, agg_2019["ndp"].values)
    m_2019.update({"source": "2019_enacted_VA_agg", "coverage_vas": len(va),
                   "coverage_vas_total": len(va), "coverage_pct": 1.0})

    # Score canonical real maps with correct column name
    m_maj = score_exogenous_map(va, MAJ_CANONICAL, id_col=CANONICAL_NAME_COL)
    m_min = score_exogenous_map(va, MIN_CANONICAL, id_col=CANONICAL_NAME_COL)

    print()
    print("  --- Real-map scores (canonical, pre-ensemble) ---", flush=True)
    for name, m in [("2019 enacted", m_2019), ("majority 2026 canonical", m_maj),
                    ("minority 2026 canonical", m_min)]:
        print(
            f"    {name}: seats={m.get('ucp_seats','?')}/{m.get('n_districts','?')}  "
            f"EG={m['efficiency_gap']:+.4f}  MM={m['mean_median']:+.4f}  "
            f"decl={m['declination']:+.4f}  s50={m['seats_at_50_50']:.3f}  "
            f"cov={m.get('coverage_pct',1.0):.2%}",
            flush=True,
        )

    print()
    print(f"[{time.strftime('%H:%M:%S')}] launching {n_chains} chains...", flush=True)

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    chain_paths = [CHECKPOINT_DIR / f"chain{i}_samples.csv" for i in range(n_chains)]
    work_items = [
        (i, n_steps_per_chain, seed, pop_deviation, str(chain_paths[i]), chunk_size)
        for i in range(n_chains)
    ]

    del graph
    del va

    with ProcessPoolExecutor(max_workers=n_chains) as ex:
        for completed in ex.map(_run_chain_chunked, work_items):
            print(f"  -> ready: {Path(completed).name}", flush=True)

    parts = [pd.read_csv(p) for p in chain_paths if p.exists()]
    if not parts:
        raise RuntimeError("All chain CSVs missing.")
    df = pd.concat(parts, ignore_index=True)
    df.to_csv(SAMPLES_CSV, index=False)
    print(f"  wrote {SAMPLES_CSV.name} ({len(df)} samples)", flush=True)

    # Convergence diagnostics
    print()
    print("  --- Convergence diagnostics ---", flush=True)
    conv = {}
    for key in METRIC_KEYS:
        diag = autocorrelation_ess(df[key].values)
        conv[key] = diag
        print(
            f"    {key:<18s} n={diag['n']}  tau={diag['tau']:.2f}  "
            f"n_eff={diag['n_eff']:.0f}  rho1={diag['rho_lag_1']:+.3f}",
            flush=True,
        )
        plot_running_mean(key, df[key].values, MAPS / f"running_mean_canonical_{key}.svg", key)
    with open(CONVERGENCE_JSON, "w", encoding="utf-8") as f:
        json.dump(conv, f, indent=2, default=float)

    # Percentiles and outlier flags
    real_maps = {
        "2019 enacted":           m_2019,
        "majority 2026 canonical": m_maj,
        "minority 2026 canonical": m_min,
    }
    summary = []
    for key in METRIC_KEYS:
        real_vals = {k: v.get(key, float("nan")) for k, v in real_maps.items()}
        plot_metric(key, key, df[key].values, real_vals,
                    MAPS / f"ensemble_distribution_canonical_{key}.svg")
        for map_name, val in real_vals.items():
            pr = pct_rank(df[key].dropna().values, val) if not np.isnan(val) else float("nan")
            summary.append({
                "metric": key, "map": map_name, "value": val, "percentile": pr,
                "ensemble_p5":  float(np.nanpercentile(df[key], 5)),
                "ensemble_p50": float(np.nanpercentile(df[key], 50)),
                "ensemble_p95": float(np.nanpercentile(df[key], 95)),
            })

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(PERCENTILES_CSV, index=False)

    print()
    print("  --- Percentile placements (canonical) ---", flush=True)
    with pd.option_context("display.float_format", "{:+.4f}".format, "display.width", 160):
        print(summary_df.to_string(index=False))

    real_json = {
        "2019_enacted":     m_2019,
        "majority_2026":    m_maj,
        "minority_2026":    m_min,
        "majority_source":  str(MAJ_CANONICAL.name),
        "minority_source":  str(MIN_CANONICAL.name),
        "name_col":         CANONICAL_NAME_COL,
        "n_steps":          int(actual_total),
        "seed":             int(seed),
    }
    with open(SCORES_JSON, "w", encoding="utf-8") as f:
        json.dump(real_json, f, indent=2, default=float)
    print(f"  wrote {SCORES_JSON.name}", flush=True)

    flags = [r for r in summary if not np.isnan(r["percentile"])
             and (r["percentile"] >= 95 or r["percentile"] <= 5)]
    if flags:
        print()
        print("  *** OUTLIER FLAGS (>=95th or <=5th pct) ***", flush=True)
        for fl in flags:
            print(f"    {fl['map']:<48s} {fl['metric']:<18s} val={fl['value']:+.4f}  p={fl['percentile']:.1f}")

    print()
    print(f"[{time.strftime('%H:%M:%S')}] done in {time.time()-t_start:.0f}s total", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-steps",     type=int,   default=100_000)
    parser.add_argument("--n-chains",    type=int,   default=4)
    parser.add_argument("--chunk-size",  type=int,   default=5000)
    parser.add_argument("--seed",        type=int,   default=None)
    parser.add_argument("--pop-deviation", type=float, default=0.25)
    args = parser.parse_args()
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    main(
        n_steps=args.n_steps,
        seed=args.seed,
        pop_deviation=args.pop_deviation,
        n_chains=args.n_chains,
        chunk_size=args.chunk_size,
    )
