"""Court-defensibility forensic verification subset.

Runs a 10,000-step ReCom chain with the same configuration as the
authoritative 2,000,000-step run, but serializes the FULL partition
assignment for every step alongside the metric scores. Output is a
byte-verifiable spot-check sample: a hostile expert can pick any of
the 10,000 saved partitions, recompute its metrics from scratch, and
confirm they match what the script wrote.

Storage estimate: 4,765 voting areas × 2 bytes (district id, int16) ×
10,000 steps = 95.3 MB raw partition data, plus metrics CSV
(~600 KB). Total compressed (zstd or LZMA) ~10-20 MB.

This subset does NOT replace the 2M-run as the audit's authoritative
ensemble. It is a forensic verification artefact: the full 2M run's
metric record is preserved as per-chain CSVs; this subset additionally
preserves the per-step ASSIGNMENTS for a smaller sample so any reader
can recompute metrics and confirm them byte-for-byte.

Usage:
    python analysis/scripts/v0_1_mcmc_verification_subset.py
"""
# Version: 0.1 series  (last updated 2026-04-26)

import sys
sys.path.insert(0, 'analysis/scripts')
import time
import json
from pathlib import Path
from functools import partial

import numpy as np
import pandas as pd

from mcmc_ensemble import (
    build_va_graph, initial_assignment_2019, seat_results,
)
from gerrychain import Graph, Partition, MarkovChain, accept, constraints, updaters
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part, bipartition_tree

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = REPO_ROOT / "data"
OUT_METRICS = OUT_DIR / "simulation_verification_metrics.csv"
OUT_ASSIGNMENTS = OUT_DIR / "verification_assignments_raw.npz"
OUT_META = OUT_DIR / "mcmc_verification_meta.json"
OUT_LOG = REPO_ROOT / "analysis" / "reports" / "v0_1_mcmc_verification_subset.log"

from drand_seed import get_canonical_seed

N_STEPS = 10_000
POP_DEVIATION = 0.25
SEED = get_canonical_seed("mcmc_verification_subset")


def _ts():
    return time.strftime("%H:%M:%S")


def main():
    print(f"[{_ts()}] verification subset start", flush=True)
    print(f"  n_steps={N_STEPS}, seed={SEED}, pop_deviation=+/-{POP_DEVIATION:.0%}", flush=True)
    print(f"  output: assignments=npz int16 array, metrics=csv, meta=json", flush=True)

    np.random.seed(SEED)
    import random as _random
    _random.seed(SEED)

    va, graph = build_va_graph()
    n_va = len(graph.nodes())
    print(f"  graph: {n_va} VAs, {len(graph.edges())} edges", flush=True)

    # Stable VA ordering — required to make the assignment array
    # comparable across runs and reconstructable.
    va_ids = sorted(graph.nodes())
    va_id_to_idx = {vid: i for i, vid in enumerate(va_ids)}

    assignment = initial_assignment_2019(va)
    num_dist = len(set(assignment.values()))
    total_pop = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
    ideal_pop = total_pop / num_dist
    print(f"  starting: {num_dist} districts, ideal pop {ideal_pop:,.0f}", flush=True)

    # District-name → integer mapping. initial_assignment_2019() returns string
    # ED names (e.g. "Calgary-Bow"), but we serialise the per-step assignment
    # vector as int16 for compactness. The mapping is preserved in the meta
    # JSON so a verifier can reconstruct the integer-to-name map and rebuild
    # any saved Partition exactly.
    unique_districts = sorted(set(assignment.values()))
    if len(unique_districts) > 32767:
        raise ValueError(
            f"int16 cannot encode {len(unique_districts)} districts; widen dtype"
        )
    dist_to_int = {name: i for i, name in enumerate(unique_districts)}
    int_to_dist = {i: name for name, i in dist_to_int.items()}

    my_updaters = {
        "population": updaters.Tally("pop_2021", alias="population"),
        "ucp": updaters.Tally("va_ucp", alias="ucp"),
        "ndp": updaters.Tally("va_ndp", alias="ndp"),
        "cut_edges": updaters.cut_edges,
    }
    seed_part = Partition(graph, assignment, my_updaters)
    seed_pops = list(seed_part["population"].values())
    seed_max_dev = max(abs(p - ideal_pop) for p in seed_pops) / ideal_pop
    if seed_max_dev > POP_DEVIATION:
        print(f"  2019 seed exceeds +/-{POP_DEVIATION:.0%}; regenerating tight seed", flush=True)
        np.random.seed(SEED + 999)
        _random.seed(SEED + 999)
        new_assignment = recursive_tree_part(
            graph, parts=list(range(num_dist)),
            pop_target=ideal_pop, pop_col="pop_2021",
            epsilon=POP_DEVIATION / 2.0, node_repeats=5,
            method=partial(bipartition_tree, max_attempts=50000),
        )
        np.random.seed(SEED)
        _random.seed(SEED)
        seed_part = Partition(graph, new_assignment, my_updaters)
        seed_pops = list(seed_part["population"].values())
        seed_max_dev = max(abs(p - ideal_pop) for p in seed_pops) / ideal_pop
        print(f"  tight seed pop dev = {seed_max_dev:.2%}", flush=True)

    pop_constraint = constraints.within_percent_of_ideal_population(seed_part, POP_DEVIATION)
    proposal = partial(
        recom, pop_col="pop_2021", pop_target=ideal_pop,
        epsilon=POP_DEVIATION / 2.0, node_repeats=2,
    )

    chain = MarkovChain(
        proposal=proposal,
        constraints=[pop_constraint],
        accept=accept.always_accept,
        initial_state=seed_part,
        total_steps=N_STEPS,
    )

    # Pre-allocate assignment array: shape (n_steps, n_va), dtype int16
    assignment_arr = np.zeros((N_STEPS, n_va), dtype=np.int16)
    metrics_rows = []
    t_start = time.time()

    for step_i, partition in enumerate(chain):
        # Serialise this step's assignment via the int mapping (district names
        # are strings, but the array is int16 for compactness).
        for vid in va_ids:
            assignment_arr[step_i, va_id_to_idx[vid]] = dist_to_int[partition.assignment[vid]]

        # Explicit key alignment: gerrychain Tally updaters are independent
        # dicts and their iteration order is not contractually identical.
        # Indexing by the same key list guarantees ucp[i] and ndp[i] refer
        # to the same district.
        keys = list(partition.parts.keys())
        ucp = np.array([partition["ucp"][k] for k in keys], dtype=float)
        ndp = np.array([partition["ndp"][k] for k in keys], dtype=float)
        m = seat_results(ucp, ndp)
        metrics_rows.append({
            "step": step_i,
            "efficiency_gap": m["efficiency_gap"],
            "mean_median": m["mean_median"],
            "declination": m["declination"],
            "seats_at_50_50": m["seats_at_50_50"],
            "ucp_seats": m["ucp_seats"],
            "n_districts": m["n_districts"],
            "ucp_vote_share": m["ucp_vote_share"],
        })

        if (step_i + 1) % 1000 == 0:
            elapsed = time.time() - t_start
            rate = (step_i + 1) / elapsed
            eta = (N_STEPS - step_i - 1) / rate
            print(f"[{_ts()}] step {step_i+1}/{N_STEPS}  "
                  f"({rate:.1f} steps/s, eta {eta:.0f}s)", flush=True)

    elapsed = time.time() - t_start
    print(f"[{_ts()}] chain complete in {elapsed:.1f}s ({elapsed/60:.2f} min)", flush=True)

    # Save outputs
    pd.DataFrame(metrics_rows).to_csv(OUT_METRICS, index=False)
    print(f"  wrote {OUT_METRICS.name} ({OUT_METRICS.stat().st_size/1024:.1f} KB)", flush=True)

    np.savez_compressed(
        OUT_ASSIGNMENTS,
        assignments=assignment_arr,
        va_ids=np.array(va_ids, dtype=np.int64),
    )
    print(f"  wrote {OUT_ASSIGNMENTS.name} ({OUT_ASSIGNMENTS.stat().st_size/1024/1024:.2f} MB)", flush=True)

    meta = {
        "n_steps": N_STEPS,
        "n_va": n_va,
        "n_districts": num_dist,
        "seed": SEED,
        "pop_deviation": POP_DEVIATION,
        "elapsed_seconds": elapsed,
        "purpose": "Court-defensibility forensic spot-check. Each row in the metrics CSV corresponds to one row in the assignments array; both are indexed by step. To verify any step's metrics: load the assignment vector for that step, map ints back to ED names via int_to_district, reconstruct a Partition, recompute metrics, confirm they match.",
        "verify_command": "python -c 'import numpy as np, json; d = np.load(\"data/verification_assignments_raw.npz\"); m = json.load(open(\"data/mcmc_verification_meta.json\")); print(\"assignments shape:\", d[\"assignments\"].shape, \"districts:\", len(m[\"int_to_district\"]))'",
        "int_to_district": int_to_dist,
        "outputs": {
            "metrics_csv": str(OUT_METRICS.name),
            "assignments_npz": str(OUT_ASSIGNMENTS.name),
            "meta_json": str(OUT_META.name),
        }
    }
    with open(OUT_META, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  wrote {OUT_META.name}", flush=True)

    print(f"\n  total elapsed: {elapsed:.1f}s", flush=True)
    print(f"  artefact storage:", flush=True)
    print(f"    metrics: {OUT_METRICS.stat().st_size/1024:.1f} KB", flush=True)
    print(f"    assignments: {OUT_ASSIGNMENTS.stat().st_size/1024/1024:.2f} MB", flush=True)


if __name__ == "__main__":
    main()
