# Version: v0.9
"""v0.1 MCMC ensemble — 250k corrected run against v0_9 topological substrate.

Replaces every prior Lane-1 ensemble in the audit. Per PO directive
(2026-04-26): everything before v0_9 is deprecated. This run is the
canonical Lane-1 reference under the corrected `seat_results()`
(Two-Party share, post-commit 3484351 in mcmc_ensemble.py) on the v0_9
topological substrate.

Differences from `mcmc_ensemble_250k_v0_8.py`:
  - Loads the v0_9 topological GPKGs (no fallback — v0_9 is canonical).
  - Outputs and checkpoint dir suffixed `_v0_9` instead of `_v0_8`.

`seat_results` and `run_ensemble` are imported, not reimplemented, so the
Two-Party fix and restored full-graph seed regen come along for free.

Outputs
-------
- data/simulated_ensemble_raw_samples_250k.csv
- data/simulation_real_map_scores_250k.json
- data/simulated_ensemble_percentiles_250k.csv
- data/simulation_convergence_diagnostics_250k.json
- data/maps/mcmc/ensemble_distribution_250k_v0_9_{metric}.png
- data/maps/mcmc/running_mean_250k_v0_9_{metric}.png

Usage
-----
    python analysis/scripts/mcmc_ensemble_250k.py [--n-steps 250000]

Forward: analysis/methodology/v0_1_mcmc_v0_9_corrected.md
Backward:
  data/va_polygons_with_2023_votes.gpkg
  data/shapefiles/derived/v0_9_topological_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_9_topological_minority_2026_eds.gpkg
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
  gerrychain, geopandas, matplotlib, numpy, pandas
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

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
)
from mcmc_ensemble_100k import autocorrelation_ess, plot_running_mean

ROOT = HERE.parent.parent
DATA = ROOT / "data"
MAPS = ROOT / "data" / "maps" / "mcmc"
MAPS.mkdir(parents=True, exist_ok=True)

# v0_9 topological substrate — canonical per PO directive (2026-04-26).
# No fallback: if these are missing, the run fails fast.
MAJ_V9_PATH = DATA / "shapefiles" / "derived" / "v0_9_topological_majority_2026_eds.gpkg"
MIN_V9_PATH = DATA / "shapefiles" / "derived" / "v0_9_topological_minority_2026_eds.gpkg"

SAMPLES_CSV = DATA / "simulated_ensemble_raw_samples_250k.csv"
SCORES_JSON = DATA / "simulation_real_map_scores_250k.json"
PERCENTILES_CSV = DATA / "simulated_ensemble_percentiles_250k.csv"
CONVERGENCE_JSON = DATA / "simulation_convergence_diagnostics_250k.json"
CHECKPOINT_DIR = DATA / "mcmc_checkpoints_250k_v0_9"


def _run_chain_chunked(args):
    """Worker: runs one chain in checkpointed chunks, carrying state across chunks.

    The chain state (final Partition) is threaded from one chunk to the next
    via run_ensemble's return_final_partition flag, so the chain advances
    continuously across chunk boundaries. The CSV is appended after each
    chunk — on crash, we lose at most `chunk_size` samples.

    Resume caveat: if a partial CSV exists, the chain restarts from the 2019
    baseline (the in-memory Partition is gone). This means resume produces a
    discontinuity at the resume point. For the headline ensemble we re-run
    from scratch (delete CSVs first) to guarantee continuous chains.

    Rebuilding the graph per worker (~15s) is cheaper than pickling the
    4,765-node NetworkX graph + Partition across the process boundary.
    """
    chain_idx, n_steps_total, base_seed, pop_deviation, chain_csv_path, chunk_size = args
    import random as _random
    import numpy as _np

    chain_csv_path = Path(chain_csv_path)
    chain_csv_path.parent.mkdir(parents=True, exist_ok=True)

    # Resume detection
    if chain_csv_path.exists():
        existing = pd.read_csv(chain_csv_path)
        n_done = len(existing)
        del existing
    else:
        n_done = 0

    if n_done >= n_steps_total:
        print(f"  [chain {chain_idx}] already complete ({n_done} samples) — skipping",
              flush=True)
        return str(chain_csv_path)

    chunks_done = n_done // chunk_size
    n_chunks = (n_steps_total + chunk_size - 1) // chunk_size
    print(f"  [chain {chain_idx}] {n_done}/{n_steps_total} done; "
          f"resuming from chunk {chunks_done}/{n_chunks}", flush=True)
    if chunks_done > 0:
        print(f"  [chain {chain_idx}] WARNING: resume after crash restarts "
              f"chain from 2019 baseline (state discontinuity at sample "
              f"{chunks_done * chunk_size}). For headline ensemble, delete "
              f"CSV and re-run from chunk 0 for continuous chain.",
              flush=True)

    # Build graph once per worker
    va, graph = build_va_graph()
    # Chain state is carried across chunks so the chain advances continuously
    # rather than resetting to the 2019 baseline at every chunk boundary.
    # First chunk receives a dict assignment; subsequent chunks receive the
    # final Partition from the previous chunk via return_final_partition=True.
    current_state = initial_assignment_2019(va)

    # Seed RNG ONCE at the start of the chain (not per-chunk) so the chain
    # consumes a single continuous stream of random numbers — matching the
    # statistical assumptions of the Markov chain. Per-chunk reseeding
    # (the prior pattern) created an artificial periodicity in the RNG
    # phase space every `chunk_size` steps. Resume-from-crash already has
    # an explicit state discontinuity (logged above), so per-chunk
    # determinism wasn't delivering what it appeared to anyway.
    chain_seed = base_seed * 100_000 + chain_idx * 1_000
    _np.random.seed(chain_seed)
    _random.seed(chain_seed)

    t_chain_start = time.time()
    for chunk_idx in range(chunks_done, n_chunks):
        chunk_steps = min(chunk_size, n_steps_total - chunk_idx * chunk_size)
        t_chunk = time.time()
        rows, current_state = run_ensemble(
            graph, current_state, chunk_steps,
            pop_deviation=pop_deviation, verbose=False,
            return_final_partition=True, seed=chain_seed,
        )
        for r in rows:
            r["chain"] = chain_idx
            r["chunk"] = chunk_idx
        # Append (write header on first chunk only; if file is empty/non-existent
        # we always write the header)
        write_header = (not chain_csv_path.exists()) or chain_csv_path.stat().st_size == 0
        pd.DataFrame(rows).to_csv(
            chain_csv_path, mode='a', header=write_header, index=False
        )
        print(f"  [chain {chain_idx}] chunk {chunk_idx+1}/{n_chunks} "
              f"({len(rows)} samples in {time.time()-t_chunk:.0f}s) → {chain_csv_path.name}",
              flush=True)

    print(f"  [chain {chain_idx}] complete in {time.time()-t_chain_start:.0f}s",
          flush=True)
    return str(chain_csv_path)


def _select_v9(plan: str):
    """v0_9 only — no fallback. Per PO directive: everything before v0_9 is deprecated."""
    if plan == "majority":
        if not MAJ_V9_PATH.exists():
            raise FileNotFoundError(
                f"v0_9 majority GPKG missing: {MAJ_V9_PATH}. "
                "v0_9 is canonical per PO directive — no fallback."
            )
        return MAJ_V9_PATH, "majority 2026 v0_9 topological"
    else:
        if not MIN_V9_PATH.exists():
            raise FileNotFoundError(
                f"v0_9 minority GPKG missing: {MIN_V9_PATH}. "
                "v0_9 is canonical per PO directive — no fallback."
            )
        return MIN_V9_PATH, "minority 2026 v0_9 topological"


def main(n_steps: int = 250000, seed: int = None, pop_deviation: float = 0.25,
         n_chains: int = 4, chunk_size: int = 5000):
    from drand_seed import get_canonical_seed
    seed = seed if seed is not None else get_canonical_seed("mcmc_ensemble_250k")
    np.random.seed(seed)
    import random as _random
    _random.seed(seed)

    t_start = time.time()
    n_steps_per_chain = (n_steps + n_chains - 1) // n_chains
    actual_total = n_steps_per_chain * n_chains
    label_run = f"250k v0_9 corrected ensemble (Two-Party share + topological substrate)"
    print(f"[{time.strftime('%H:%M:%S')}] {label_run} starting", flush=True)
    print(f"  n_steps requested={n_steps}, n_chains={n_chains}, "
          f"steps/chain={n_steps_per_chain}, total={actual_total}", flush=True)
    print(f"  chunk_size={chunk_size} samples (checkpoint granularity)", flush=True)
    print(f"  base_seed={seed}, pop_deviation=±{pop_deviation:.0%}", flush=True)
    print(f"  checkpoint dir: {CHECKPOINT_DIR}", flush=True)

    va, graph = build_va_graph()

    assignment = initial_assignment_2019(va)
    districts_2019 = set(assignment.values())
    print(f"  2019 baseline districts: {len(districts_2019)}", flush=True)

    agg = va.groupby("parent_ed_2019").agg(
        ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum")
    ).reset_index()
    m_2019 = seat_results(agg["ucp"].values, agg["ndp"].values)
    m_2019["source"] = "2019_enacted_VA_agg"
    m_2019["coverage_vas"] = int(len(va))
    m_2019["coverage_vas_total"] = int(len(va))
    m_2019["coverage_pct"] = 1.0
    m_2019["votes_coverage_pct"] = 1.0

    maj_path, maj_label = _select_v9("majority")
    min_path, min_label = _select_v9("minority")
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
    print(f"[{time.strftime('%H:%M:%S')}] launching {n_chains} parallel chains × "
          f"{n_steps_per_chain} steps with checkpointed chunks...", flush=True)

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    chain_paths = [CHECKPOINT_DIR / f"chain{i}_samples.csv" for i in range(n_chains)]
    work_items = [
        (i, n_steps_per_chain, seed, pop_deviation,
         str(chain_paths[i]), chunk_size)
        for i in range(n_chains)
    ]

    # Free the parent's heavy graph before spawning workers — each worker rebuilds
    # its own. Saves a few hundred MB of RSS shared into each child on Windows.
    del graph
    del va

    with ProcessPoolExecutor(max_workers=n_chains) as ex:
        for completed_path in ex.map(_run_chain_chunked, work_items):
            print(f"  -> chain file ready: {Path(completed_path).name}", flush=True)

    # Concatenate per-chain CSVs into the canonical samples file
    parts = [pd.read_csv(p) for p in chain_paths if p.exists()]
    if not parts:
        raise RuntimeError("All chain CSVs missing — nothing to concatenate.")
    df = pd.concat(parts, ignore_index=True)
    df.to_csv(SAMPLES_CSV, index=False)
    print(f"  wrote {SAMPLES_CSV.name} ({len(df)} samples from {n_chains} chains) "
          f"in {time.time()-t_start:.0f}s total", flush=True)

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
            MAPS / f"running_mean_250k_v0_9_{key}.png",
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
                    MAPS / f"ensemble_distribution_250k_v0_9_{key}.png")
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
    parser.add_argument("--n-steps", type=int, default=250000,
                        help="Total samples across all chains (default: 250000)")
    parser.add_argument("--n-chains", type=int, default=4,
                        help="Number of parallel chains (default: 4)")
    parser.add_argument("--chunk-size", type=int, default=5000,
                        help="Checkpoint granularity in samples per chunk (default: 5000)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Base seed; defaults to drand canonical seed if omitted")
    parser.add_argument("--pop-deviation", type=float, default=0.25)
    args = parser.parse_args()
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    main(n_steps=args.n_steps, seed=args.seed, pop_deviation=args.pop_deviation,
         n_chains=args.n_chains, chunk_size=args.chunk_size)
