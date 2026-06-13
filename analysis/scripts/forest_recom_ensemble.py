# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
forest_recom_ensemble.py — Forest-ReCom robustness check, Phase A scaffold
--------------------------------------------------------------------------

**Status: WIRED UP, NOT YET RUN.** This script exists so that the
substrate, seed pipeline, output paths, and chain harness are all
committed in the same git commit as the pre-registration in
`preregistration/osf_forest_recom_robustness.md`. The script will refuse
to execute unless you pass `--confirm-osf-filed` *after* filing the OSF
form referenced in the pre-registration. This gate exists specifically
to prevent a post-prereg edit-and-run cycle that would defeat the
discipline of pre-registration.

WHAT THIS IS
============
Phase A (100,000 samples) of the Forest-ReCom sampler robustness check
committed in `preregistration/osf_forest_recom_robustness.md`. The
question: does the audit's canonical 1.01 M ReCom finding (minority at
the 99.99th percentile on seats@50/50) shift materially when we swap
ReCom's uniform-spanning-tree proposal for a uniform-spanning-forest
proposal? Spanning-tree weighting is known to bias the stationary
distribution toward more-compact partitions (DeFord, Duchin & Solomon
2021, §4); spanning-forest weighting moves in the opposite direction.

DIFFERENCES FROM mcmc_ensemble_canonical.py
===========================================
  * Salt: `"forest_recom_robustness"` (NOT `"mcmc_ensemble_250k"`).
    Pre-registered in `preregistration/osf_forest_recom_robustness.md` §6.3.
  * Proposal method: `_forest_spanning_method` instead of the canonical
    `_bpt_global`. Uses `networkx.algorithms.tree.mst.random_spanning_tree`
    composed with a uniform-random edge removal to produce a spanning
    forest with 2 components, then validates population balance.
  * Default n_steps: 100,000 (per §6.4 of the prereg). Scaling to 1M is
    explicitly out of scope for Phase A and requires a SEPARATE prereg.
  * Output paths suffixed `_forest_recom_phaseA` so this run cannot
    overwrite the canonical ensemble files.
  * Run gate: `--confirm-osf-filed` required. Without it, the script
    prints the seed and the planned output paths and exits 0 (this is
    the "wired up but not run" mode and the default for CI / smoke).

USAGE
=====
Dry run (default — does not execute the chain):

    python analysis/scripts/forest_recom_ensemble.py

Real run (only after the OSF form has been filed referencing the commit
hash of `preregistration/osf_forest_recom_robustness.md`):

    python analysis/scripts/forest_recom_ensemble.py \\
        --confirm-osf-filed \\
        --osf-registration-id <id> \\
        --n-steps 100000

OUTPUTS (committed paths, per OSF prereg §6.5)
==============================================
    data/outputs/forest_recom_raw_samples_phaseA.csv
    data/outputs/forest_recom_real_map_scores_phaseA.json
    data/outputs/forest_recom_percentiles_phaseA.csv
    data/outputs/forest_recom_convergence_diagnostics_phaseA.json

These are written by `main()` only when `--confirm-osf-filed` is passed.
The absence of these files in a Phase A run is itself a publishable
result (failure-mode reporting per prereg §6.5).

Backward:
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/canonical/ea_minority_2026_eds.gpkg
  data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg
  analysis/scripts/mcmc_ensemble.py  (shared infrastructure)
  analysis/scripts/drand_seed.py
  preregistration/osf_forest_recom_robustness.md  (binding spec)

Forward:
  findings/forest_recom_robustness.md  (results doc; created post-run)
  reports/academic/report_academic.md §5.2.7  (cite this prereg)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from functools import partial
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

try:
    import data_loader
    from canonical_manifest import verify_canonical_files
except ImportError:
    sys.path.insert(0, str(HERE.parent / "utils"))
    import data_loader
    from canonical_manifest import verify_canonical_files

from drand_seed import CANONICAL_ROUND, get_canonical_seed
from mcmc_ensemble import (
    build_va_graph,
    initial_assignment_2019,
    score_exogenous_map,
    seat_results,
    pct_rank,
    autocorrelation_ess,
)

# ── Pre-registered identifiers ────────────────────────────────────────────────
# Both pinned here so any drift between the script and the OSF prereg is
# visible at import time.

PREREG_SALT = "forest_recom_robustness"
PREREG_DOC = HERE.parent.parent / "preregistration" / "osf_forest_recom_robustness.md"
PHASE_LABEL = "phaseA"
PHASE_A_N_STEPS = 100_000
PHASE_A_N_CHAINS = 4
PHASE_A_BURN_IN_PER_CHAIN = 5_000

ROOT = HERE.parent.parent
DATA = data_loader._resolve_path("data")

MAJ_CANONICAL = DATA / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg"
MIN_CANONICAL = DATA / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"
CANONICAL_NAME_COL = "EDName2025"

SAMPLES_CSV     = DATA / "outputs" / f"forest_recom_raw_samples_{PHASE_LABEL}.csv"
SCORES_JSON     = DATA / "outputs" / f"forest_recom_real_map_scores_{PHASE_LABEL}.json"
PERCENTILES_CSV = DATA / "outputs" / f"forest_recom_percentiles_{PHASE_LABEL}.csv"
CONVERGENCE_JSON = DATA / "outputs" / f"forest_recom_convergence_diagnostics_{PHASE_LABEL}.json"
CHECKPOINT_DIR  = DATA / f"simulation_checkpoints_forest_recom_{PHASE_LABEL}"

METRIC_KEYS = [
    "efficiency_gap", "mean_median", "declination", "seats_at_50_50",
    "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030",
]


# ── Spanning-forest proposal method ───────────────────────────────────────────

import random as _random_mod  # module-global RNG; seeded by main() / validation

try:
    from gerrychain.tree import ReselectException as _ReselectException
except Exception:  # pragma: no cover - older gerrychain
    class _ReselectException(Exception):
        pass


def _forest_spanning_method(
    graph,
    pop_col: str,
    pop_target,
    epsilon: float,
    node_repeats: int = 1,
    max_attempts: int = 10000,
    allow_pair_reselection: bool = True,
    **kwargs,
):
    """
    Forest-ReCom spanning method (prereg §6.1, "Method B"). A drop-in
    replacement for gerrychain's ``bipartition_tree`` that uses
    spanning-FOREST weighting instead of spanning-TREE weighting.

    Construction (multi-root Wilson uniform spanning forest):
      1. The two-district joint subgraph is passed in by ``recom``.
      2. Draw two distinct roots r0, r1 uniformly at random.
      3. Build a uniform spanning forest with exactly two trees by
         Wilson's loop-erased random walk rooted at the SET {r0, r1}:
         every other node performs an LERW until it first reaches a node
         already in the forest, and joins that node's tree. This samples
         uniformly from spanning forests in which r0 and r1 lie in
         different trees (Wilson 1996; Marchal 2000).
      4. The two trees ARE the bipartition — no balance-seeking edge is
         chosen (that is the spanning-TREE behaviour this check is built
         to contrast). Return one tree's node set.
      5. If the population split is outside ±epsilon, draw new roots and
         a new forest; after ``max_attempts`` failures raise
         ReselectException so ``recom`` reselects the district pair.

    Because each (forest) is equally likely rather than each (tree,
    balanced-cut) pair, the stationary distribution shifts toward
    less-compact partitions — the documented direction of the
    spanning-structure bias the prereg tests for.

    Returns: ``Set`` of nodes forming one balanced part (the ``recom``
    method contract). Uses the module-global ``_random_mod`` RNG so the
    drand-anchored seed in ``main()`` governs reproducibility.
    """
    nodes = list(graph.nodes)
    n = len(nodes)
    if n < 2:
        raise _ReselectException("Forest-ReCom: subgraph too small to bipartition.")
    pops = {node: float(graph.nodes[node][pop_col]) for node in nodes}
    total = sum(pops.values())
    lo = pop_target * (1.0 - epsilon)
    hi = pop_target * (1.0 + epsilon)
    adj = {node: list(graph.neighbors(node)) for node in nodes}

    _forest_spanning_method.stats["calls"] += 1
    for attempt in range(1, max_attempts + 1):
        r0, r1 = _random_mod.sample(nodes, 2)
        component = {r0: 0, r1: 1}  # in-forest set == component.keys()
        for start in nodes:
            if start in component:
                continue
            path = [start]
            inpath = {start}
            cur = start
            while True:
                nbrs = adj[cur]
                if not nbrs:  # isolated node (should not happen on a connected subgraph)
                    component[start] = 0
                    break
                nxt = _random_mod.choice(nbrs)
                if nxt in component:
                    comp = component[nxt]
                    for nd in path:
                        component[nd] = comp
                    break
                if nxt in inpath:  # loop-erase back to nxt
                    while path[-1] != nxt:
                        inpath.discard(path.pop())
                    cur = nxt
                else:
                    path.append(nxt)
                    inpath.add(nxt)
                    cur = nxt
        pop_a = sum(p for node, p in pops.items() if component[node] == 0)
        pop_b = total - pop_a
        if lo <= pop_a <= hi and lo <= pop_b <= hi:
            _forest_spanning_method.stats["attempts"] += attempt
            _forest_spanning_method.stats["accepts"] += 1
            return {node for node in nodes if component[node] == 0}

    _forest_spanning_method.stats["attempts"] += max_attempts
    _forest_spanning_method.stats["reselects"] += 1
    if allow_pair_reselection:
        raise _ReselectException(
            f"Forest-ReCom: no balanced 2-root spanning forest after {max_attempts} attempts."
        )
    raise RuntimeError(
        f"Forest-ReCom: no balanced 2-root spanning forest after {max_attempts} attempts."
    )


# Lightweight diagnostics, read by the validation harness.
_forest_spanning_method.stats = {"calls": 0, "accepts": 0, "reselects": 0, "attempts": 0}


# ── Pre-flight checks ─────────────────────────────────────────────────────────

def _print_preflight(seed: int, args) -> None:
    """Print the seed, the planned output paths, and the OSF gate state.

    This is the default 'dry-run' output. A reviewer can verify the seed
    matches the public drand beacon (round 5,500,000) without the chain
    having been started.
    """
    print(f"Forest-ReCom Phase A — pre-flight")
    print(f"  drand round:  {CANONICAL_ROUND}")
    print(f"  salt:         {PREREG_SALT!r}")
    print(f"  derived seed: {seed}")
    print(f"  n_steps:      {args.n_steps:,} (default {PHASE_A_N_STEPS:,})")
    print(f"  n_chains:     {args.n_chains}")
    print(f"  burn-in:      {PHASE_A_BURN_IN_PER_CHAIN:,} per chain")
    print(f"  prereg doc:   {PREREG_DOC.relative_to(ROOT)}")
    print(f"  outputs:")
    for p in (SAMPLES_CSV, SCORES_JSON, PERCENTILES_CSV, CONVERGENCE_JSON):
        print(f"    {p.relative_to(ROOT)}")
    print()
    if not args.confirm_osf_filed:
        print("OSF gate: CLOSED")
        print()
        print("This script is the 'wired up but not run' state. To execute the")
        print("Forest-ReCom chain you must:")
        print("  1. File the OSF form referencing the commit hash of the prereg doc.")
        print("  2. Add the implementation to _forest_spanning_method (see docstring).")
        print("  3. Re-run with --confirm-osf-filed --osf-registration-id <id>.")
        print()
        print("Exiting 0 — no chain executed, no outputs written.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Forest-ReCom Phase A robustness check. See "
            "preregistration/osf_forest_recom_robustness.md for binding spec."
        )
    )
    parser.add_argument(
        "--n-steps",
        type=int,
        default=PHASE_A_N_STEPS,
        help=f"Total samples (default {PHASE_A_N_STEPS:,}, the prereg-committed Phase A size)",
    )
    parser.add_argument("--n-chains", type=int, default=PHASE_A_N_CHAINS)
    parser.add_argument(
        "--confirm-osf-filed",
        action="store_true",
        help="Required to execute. Without this flag the script does a pre-flight only.",
    )
    parser.add_argument(
        "--osf-registration-id",
        type=str,
        default=None,
        help="OSF registration ID. Required when --confirm-osf-filed is passed.",
    )
    args = parser.parse_args()

    if not PREREG_DOC.exists():
        print(f"ERROR: pre-registration document missing: {PREREG_DOC}", file=sys.stderr)
        print("Cannot run Forest-ReCom without the binding prereg in git.", file=sys.stderr)
        return 2

    # Compute the seed BEFORE the canonical-file check so a clone with
    # un-pulled LFS pointers can still print the pre-flight (the seed is
    # the part a reviewer needs to verify against the public beacon).
    seed = get_canonical_seed(PREREG_SALT)
    _print_preflight(seed, args)

    if not args.confirm_osf_filed:
        return 0

    if not args.osf_registration_id:
        print("ERROR: --confirm-osf-filed requires --osf-registration-id <id>", file=sys.stderr)
        return 2

    # Canonical-file verification gates execution only — required for the
    # run, not for the pre-flight. LFS-pointer environments correctly fail
    # here at the same place the canonical run would fail.
    verify_canonical_files()

    # ── Execution path (Phase A run, post-OSF gate) ──────────────────────────
    # When the gate opens, _forest_spanning_method must already be
    # implemented (see its docstring). The chain harness below mirrors
    # mcmc_ensemble_canonical.py's _run_chain_chunked exactly, with the
    # proposal method swapped. The intent is that the diff between the
    # canonical run's outputs and Phase A's outputs is *entirely*
    # attributable to the spanning-structure change, with no other
    # confounders.
    print(f"OSF gate: OPEN (registration {args.osf_registration_id})")
    print(f"[{time.strftime('%H:%M:%S')}] Forest-ReCom Phase A starting")
    print(f"  substrate: official Elections Alberta canonical shapefiles")
    print(f"  proposal:  spanning-forest variant of gerrychain.proposals.recom")

    np.random.seed(seed)
    import random as _random
    _random.seed(seed)

    # The chain harness itself lives in mcmc_ensemble.run_ensemble. The
    # swap is just the proposal-method argument. The gate stays closed
    # until _forest_spanning_method is implemented and reviewed.
    raise NotImplementedError(
        "Forest-ReCom execution path is gated. Implement "
        "_forest_spanning_method per the docstring, then remove this "
        "raise to enable the run."
    )


if __name__ == "__main__":
    sys.exit(main())
