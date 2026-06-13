# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
"""
_forest_recom_validation.py — correctness/feasibility validation of the
Forest-ReCom spanning method (Method B, multi-root Wilson USF).

This is SOFTWARE QA, not the pre-registered Phase A scientific run. It does
not touch the OSF commitment. It answers three questions before any official
run is filed:

  1. CORRECTNESS  — does the sampler produce exactly two contiguous,
     population-balanced districts each step? (Chain advances under a
     contiguity + ±deviation constraint set; final partition asserted valid.)
  2. FEASIBILITY  — acceptance rate, mean internal attempts per accepted
     proposal, and per-step wall time (can a 100k Phase A run finish?).
  3. BEHAVIOUR    — does Forest-ReCom produce LESS-compact plans than standard
     ReCom (more cut edges)? If not, the swap is not really changing the
     spanning-structure weighting and the check would be vacuous.

Run: python analysis/scripts/_forest_recom_validation.py [--steps N]
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from functools import partial
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from gerrychain import MarkovChain, Partition, accept, constraints, updaters
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part, bipartition_tree

from mcmc_ensemble import build_va_graph, initial_assignment_2019
import forest_recom_ensemble as fre

POP_DEV = 0.25
SEED = 20260613


def build_seed_partition(graph, assignment, ideal_pop, my_updaters):
    part = Partition(graph, assignment, my_updaters)
    max_dev = max(abs(p - ideal_pop) for p in part["population"].values()) / ideal_pop
    if max_dev <= POP_DEV:
        return part
    print(f"  2019 seed max dev {max_dev:.2%} > ±{POP_DEV:.0%}; building tight seed...", flush=True)
    np.random.seed(SEED)
    random.seed(SEED)
    new_assign = recursive_tree_part(
        graph, parts=list(range(len(set(assignment.values())))),
        pop_target=ideal_pop, pop_col="pop_2021", epsilon=POP_DEV / 2.0,
        node_repeats=5, method=partial(bipartition_tree, max_attempts=50000),
    )
    return Partition(graph, new_assign, my_updaters)


def run_chain(proposal, seed_part, n_steps, ideal_pop, label):
    pop_constraint = constraints.within_percent_of_ideal_population(seed_part, POP_DEV)
    chain = MarkovChain(
        proposal=proposal,
        constraints=[pop_constraint, constraints.contiguous],
        accept=accept.always_accept,
        initial_state=seed_part,
        total_steps=n_steps,
    )
    cut_edges = []
    advances = 0
    prev_assign = dict(seed_part.assignment)
    t0 = time.time()
    for part in chain:
        cut_edges.append(len(part["cut_edges"]))
        if dict(part.assignment) != prev_assign:
            advances += 1
            prev_assign = dict(part.assignment)
    elapsed = time.time() - t0
    # Assert final partition validity (contiguity + balance) independently.
    final = part
    max_dev = max(abs(p - ideal_pop) for p in final["population"].values()) / ideal_pop
    contig_ok = all(
        len(list(__import__("networkx").connected_components(
            final.graph.subgraph([n for n in final.graph if final.assignment[n] == d]))) ) == 1
        for d in set(final.assignment.values())
    )
    print(f"  [{label}] {n_steps} steps in {elapsed:.1f}s ({elapsed/n_steps*1000:.0f} ms/step); "
          f"advances={advances}; final max pop-dev={max_dev:.2%}; all-districts-contiguous={contig_ok}",
          flush=True)
    return {
        "label": label, "n_steps": n_steps, "elapsed_s": elapsed,
        "ms_per_step": elapsed / n_steps * 1000, "advances": advances,
        "final_max_pop_dev": max_dev, "all_contiguous": contig_ok,
        "mean_cut_edges": float(np.mean(cut_edges)),
        "median_cut_edges": float(np.median(cut_edges)),
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=300)
    args = ap.parse_args()

    print("[forest-validation] building VA graph + tight 87-district seed...", flush=True)
    va, graph = build_va_graph(verbose=False)
    assignment = initial_assignment_2019(va)
    num_dist = len(set(assignment.values()))
    ideal_pop = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes()) / num_dist
    my_updaters = {
        "population": updaters.Tally("pop_2021", alias="population"),
        "cut_edges": updaters.cut_edges,
    }
    seed_part = build_seed_partition(graph, assignment, ideal_pop, my_updaters)
    print(f"  seed: {num_dist} districts, ideal pop {ideal_pop:,.0f}", flush=True)

    # Standard ReCom (tree weighting) — baseline
    random.seed(SEED); np.random.seed(SEED)
    std_proposal = partial(recom, pop_col="pop_2021", pop_target=ideal_pop,
                           epsilon=POP_DEV, node_repeats=2)
    print("\n=== standard ReCom (spanning-tree, baseline) ===", flush=True)
    std = run_chain(std_proposal, seed_part, args.steps, ideal_pop, "tree")

    # Forest ReCom (Method B) — the swap
    random.seed(SEED); np.random.seed(SEED)
    fre._forest_spanning_method.stats = {"calls": 0, "accepts": 0, "reselects": 0, "attempts": 0}
    forest_proposal = partial(recom, pop_col="pop_2021", pop_target=ideal_pop,
                              epsilon=POP_DEV, node_repeats=2,
                              method=partial(fre._forest_spanning_method,
                                             allow_pair_reselection=True, max_attempts=5000))
    print("\n=== Forest-ReCom (spanning-forest, Method B) ===", flush=True)
    forest = run_chain(forest_proposal, seed_part, args.steps, ideal_pop, "forest")
    st = fre._forest_spanning_method.stats
    acc_rate = st["accepts"] / max(st["calls"], 1)
    attempts_per_accept = st["attempts"] / max(st["accepts"], 1)
    print(f"  method stats: calls={st['calls']} accepts={st['accepts']} "
          f"reselects={st['reselects']} | accept-rate/call={acc_rate:.3f} | "
          f"mean attempts/accept={attempts_per_accept:.1f}", flush=True)

    # Verdicts
    print("\n=== VALIDATION VERDICT ===", flush=True)
    correctness = (std["all_contiguous"] and forest["all_contiguous"]
                   and forest["final_max_pop_dev"] <= POP_DEV and forest["advances"] > 0)
    less_compact = forest["mean_cut_edges"] > std["mean_cut_edges"]
    feasible = forest["ms_per_step"] < 2000  # < 2s/step => 100k in < ~56h single-core; parallel OK
    print(f"  CORRECTNESS  : {'PASS' if correctness else 'FAIL'} "
          f"(forest advances={forest['advances']}, contiguous={forest['all_contiguous']}, "
          f"max dev={forest['final_max_pop_dev']:.2%})", flush=True)
    print(f"  BEHAVIOUR    : {'PASS' if less_compact else 'FAIL'} "
          f"(forest cut-edges {forest['mean_cut_edges']:.0f} "
          f"{'>' if less_compact else '<='} tree {std['mean_cut_edges']:.0f} "
          f"=> forest is {'less' if less_compact else 'NOT less'} compact)", flush=True)
    print(f"  FEASIBILITY  : {'PASS' if feasible else 'CONCERN'} "
          f"(forest {forest['ms_per_step']:.0f} ms/step; {attempts_per_accept:.1f} attempts/accept)",
          flush=True)
    overall = "PASS — sampler is correct and behaves as a forest sampler" if (correctness and less_compact) \
        else "REVIEW — see failed checks above"
    print(f"\n  OVERALL: {overall}", flush=True)
    return 0 if (correctness and less_compact) else 1


if __name__ == "__main__":
    sys.exit(main())
