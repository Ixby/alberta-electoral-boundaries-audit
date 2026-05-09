"""Short-bursts targeted gerrymander: maximise UCP seats@50/50 within ReCom.

Tests whether a non-neutral but legal procedure can reach the minority's
seats@50/50 territory. Method: Cannon, Goldbloom-Helzner, Gupta, Matthews,
Suwal (2022) "Voting Rights, Markov Chains, and Optimization by Short
Bursts." Take the standard ReCom MCMC chain, run for short bursts of N
steps, pick the most UCP-favouring partition seen in the burst, restart
the next burst from that partition.

The neutral 2M ensemble's max seats@50/50 was 51.72%. The minority's
defensible 89-of-89 reading is 52.8%. If the targeted procedure reaches
or exceeds the minority's value, it confirms the framing "the minority
sits in a place a non-neutral procedure could find on purpose." If it
does not, the finding becomes "the minority is somewhere even targeted
procedures struggle to reach."
"""

# Version: 0.1 series  (last updated 2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

import sys

sys.path.insert(0, "analysis/scripts")
import time
import json
from pathlib import Path
from functools import partial

import numpy as np
import pandas as pd

from mcmc_ensemble import (
    build_va_graph,
    initial_assignment_2019,
    seat_results,
)
from gerrychain import Graph, Partition, MarkovChain, accept, constraints, updaters
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part, bipartition_tree

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = REPO_data_loader._resolve_path("data")
OUT_LOG = REPO_ROOT / "analysis" / "reports" / "v0_1_targeted_burst.log"
OUT_TRACE = OUT_DIR / "targeted_burst_trace.csv"
OUT_BEST = OUT_DIR / "targeted_burst_best.json"

POP_DEVIATION = 0.25  # same as ensemble
BURST_LENGTH = 50  # steps per burst (Cannon et al. typical)
N_BURSTS = 800  # 800 * 50 = 40k total steps; ~5-10 min wall time
SEED = 137


def _ts():
    return time.strftime("%H:%M:%S")


def score(partition):
    # Gemini Code Audit Finding: CRITICAL - explicit key alignment to prevent dict iteration order bugs
    keys = list(partition.parts.keys())
    ucp = np.array([partition["ucp"][k] for k in keys], dtype=float)
    ndp = np.array([partition["ndp"][k] for k in keys], dtype=float)
    s = seat_results(ucp, ndp)
    return s["seats_at_50_50"], s


def main():
    print(f"[{_ts()}] short-bursts targeted gerrymander start", flush=True)
    print(
        f"  burst length = {BURST_LENGTH}, n_bursts = {N_BURSTS}, "
        f"total steps = {BURST_LENGTH * N_BURSTS}",
        flush=True,
    )
    print(f"  seed = {SEED}, pop_deviation = +/-{POP_DEVIATION:.0%}", flush=True)

    rng = np.random.default_rng(SEED)  # noqa: F841
    np.random.seed(SEED)  # gerrychain-compat: seeds legacy RNG
    import random as _random

    _random.seed(SEED)  # gerrychain-compat: seeds global Python random

    va, graph = build_va_graph()
    print(
        f"  graph built: {len(graph.nodes())} nodes, {len(graph.edges())} edges",
        flush=True,
    )

    assignment = initial_assignment_2019(va)
    num_dist = len(set(assignment.values()))
    total_pop = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
    ideal_pop = total_pop / num_dist
    print(
        f"  starting assignment: {num_dist} districts, ideal pop {ideal_pop:,.0f}",
        flush=True,
    )

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
        print(
            f"  2019 seed exceeds +/-{POP_DEVIATION:.0%}; regenerating tight seed",
            flush=True,
        )
        rng = np.random.default_rng(42)  # noqa: F841
        np.random.seed(42)  # gerrychain-compat: seeds legacy RNG
        _random.seed(42)  # gerrychain-compat: seeds global Python random
        new_assignment = recursive_tree_part(
            graph,
            parts=list(range(num_dist)),
            pop_target=ideal_pop,
            pop_col="pop_2021",
            epsilon=POP_DEVIATION / 2.0,
            node_repeats=5,
            method=partial(bipartition_tree, max_attempts=50000),
        )
        rng = np.random.default_rng(SEED)  # noqa: F841
        np.random.seed(SEED)  # gerrychain-compat: seeds legacy RNG
        _random.seed(SEED)  # gerrychain-compat: seeds global Python random
        seed_part = Partition(graph, new_assignment, my_updaters)
        seed_pops = list(seed_part["population"].values())
        seed_max_dev = max(abs(p - ideal_pop) for p in seed_pops) / ideal_pop
        print(f"  tight seed pop dev = {seed_max_dev:.2%}", flush=True)

    pop_constraint = constraints.within_percent_of_ideal_population(
        seed_part, POP_DEVIATION
    )
    proposal = partial(
        recom,
        pop_col="pop_2021",
        pop_target=ideal_pop,
        epsilon=POP_DEVIATION / 2.0,
        node_repeats=2,
    )

    current = seed_part
    cur_score, cur_metrics = score(current)
    print(
        f"  initial seats@50/50 = {cur_score:.4f}  (ucp_seats={cur_metrics['ucp_seats']}/{cur_metrics['n_districts']})",
        flush=True,
    )

    best_score = cur_score
    best_metrics = cur_metrics
    trace = []
    t_start = time.time()

    for burst_i in range(N_BURSTS):
        chain = MarkovChain(
            proposal=proposal,
            constraints=[pop_constraint],
            accept=accept.always_accept,
            initial_state=current,
            total_steps=BURST_LENGTH,
        )

        burst_best_score = cur_score
        burst_best_part = current
        for part in chain:
            s_score, s_metrics = score(part)
            if s_score > burst_best_score:
                burst_best_score = s_score
                burst_best_part = part
                if s_score > best_score:
                    best_score = s_score
                    best_metrics = s_metrics

        current = burst_best_part
        cur_score = burst_best_score
        trace.append(
            {
                "burst": burst_i,
                "best_so_far": best_score,
                "burst_best": burst_best_score,
            }
        )

        if (burst_i + 1) % 25 == 0 or burst_i == 0:
            elapsed = time.time() - t_start
            steps_done = (burst_i + 1) * BURST_LENGTH
            rate = steps_done / elapsed if elapsed > 0 else 0
            eta_s = (N_BURSTS - burst_i - 1) * BURST_LENGTH / rate if rate > 0 else 0
            print(
                f"[{_ts()}] burst {burst_i+1}/{N_BURSTS}  "
                f"best so far = {best_score:.4f}  "
                f"({steps_done:,} steps, {rate:.1f} steps/s, eta {eta_s/60:.1f} min)",
                flush=True,
            )

    elapsed = time.time() - t_start
    print(f"[{_ts()}] done in {elapsed:.1f}s ({elapsed/60:.2f} min)", flush=True)
    print(f"  BEST seats@50/50: {best_score:.4f}", flush=True)
    print(f"  BEST metrics: {best_metrics}", flush=True)

    pd.DataFrame(trace).to_csv(OUT_TRACE, index=False)
    with open(OUT_BEST, "w") as f:
        json.dump(
            {
                "best_seats_at_50_50": best_score,
                "best_metrics": {
                    k: float(v) if isinstance(v, (int, float)) else v
                    for k, v in best_metrics.items()
                },
                "n_bursts": N_BURSTS,
                "burst_length": BURST_LENGTH,
                "total_steps": N_BURSTS * BURST_LENGTH,
                "elapsed_seconds": elapsed,
                "seed": SEED,
                "pop_deviation": POP_DEVIATION,
            },
            f,
            indent=2,
        )
    print(f"  wrote {OUT_TRACE.name} and {OUT_BEST.name}", flush=True)


if __name__ == "__main__":
    main()
