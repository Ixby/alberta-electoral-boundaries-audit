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

    # Harness wired 2026-07-10 (gate previously raised NotImplementedError;
    # _forest_spanning_method itself was already implemented). Mirrors
    # mcmc_ensemble_canonical.py's per-chain chunked loop with two deliberate
    # differences only: (1) proposal_method=_forest_spanning_method is passed
    # through run_ensemble's new parameter; (2) chain seeds use the prereg
    # §6.4 chain salts f"{PREREG_SALT}_chain_{i}". Fail-loud on partial-chain
    # resume, per the chain-1 duplication lesson
    # (findings/ensemble_chain1_duplication_note.md).
    from mcmc_ensemble import run_ensemble
    import pandas as pd
    import random as _random

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    chunk_size = 5_000
    steps_per_chain = args.n_steps // args.n_chains

    va, graph = build_va_graph(verbose=False)
    initial = initial_assignment_2019(va)

    chain_frames = []
    for chain_idx in range(args.n_chains):
        chain_salt = f"{PREREG_SALT}_chain_{chain_idx}"
        chain_seed = get_canonical_seed(chain_salt)
        chain_csv = CHECKPOINT_DIR / f"chain{chain_idx}_samples.csv"
        n_done = len(pd.read_csv(chain_csv)) if chain_csv.exists() else 0
        if n_done >= steps_per_chain:
            print(f"  [chain {chain_idx}] complete ({n_done}) — skipping")
            chain_frames.append(pd.read_csv(chain_csv).assign(chain=chain_idx))
            continue
        if n_done > 0:
            raise RuntimeError(
                f"[chain {chain_idx}] partial chain ({n_done} rows) at {chain_csv} — "
                f"partition checkpointing is not implemented; resuming would replay "
                f"from the seed (the chain-1 duplication failure mode). Delete the "
                f"partial CSV to rerun this chain from scratch."
            )
        print(f"  [chain {chain_idx}] salt={chain_salt!r} seed={chain_seed}")
        np.random.seed(chain_seed)
        _random.seed(chain_seed)
        _random_mod.seed(chain_seed)  # module RNG driving the forest sampler

        state = initial
        n_chunks = (steps_per_chain + chunk_size - 1) // chunk_size
        t_chain = time.time()
        for chunk_idx in range(n_chunks):
            chunk_steps = min(chunk_size, steps_per_chain - chunk_idx * chunk_size)
            rows, state = run_ensemble(
                graph, state, chunk_steps,
                pop_deviation=0.25, verbose=False,
                return_final_partition=True, seed=chain_seed,
                proposal_method=_forest_spanning_method,
            )
            for r in rows:
                r["chain"] = chain_idx
                r["chunk"] = chunk_idx
            write_header = (not chain_csv.exists()) or chain_csv.stat().st_size == 0
            pd.DataFrame(rows).to_csv(chain_csv, mode="a", header=write_header, index=False)
            s = _forest_spanning_method.stats
            print(
                f"  [chain {chain_idx}] chunk {chunk_idx + 1}/{n_chunks} "
                f"({time.time() - t_chain:,.0f}s elapsed; forest stats: "
                f"{s['accepts']:,} accepts / {s['calls']:,} calls / "
                f"{s['reselects']:,} reselects)",
                flush=True,
            )
        chain_frames.append(pd.read_csv(chain_csv).assign(chain=chain_idx))

    # ── Pool, drop burn-in, write outputs (prereg §6.4–§6.6) ─────────────────
    pooled = pd.concat(chain_frames, ignore_index=True)
    pooled.to_csv(SAMPLES_CSV, index=False)
    print(f"  wrote {SAMPLES_CSV.name} ({len(pooled):,} rows incl. burn-in)")

    burn = PHASE_A_BURN_IN_PER_CHAIN
    kept = pd.concat(
        [g.iloc[burn:] for _, g in pooled.groupby("chain")], ignore_index=True
    )
    print(f"  burn-in dropped: {burn:,}/chain -> {len(kept):,} reporting rows")

    metrics = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]

    conv = {}
    for m in metrics:
        conv[m] = autocorrelation_ess(kept[m].dropna().values)
    with open(CONVERGENCE_JSON, "w", encoding="utf-8") as f:
        json.dump(conv, f, indent=2, default=float)
    print(f"  wrote {CONVERGENCE_JSON.name}")

    # Real-map scores are ensemble-independent (same shapefiles, same
    # seat_results); recomputed here through the identical scoring path so
    # this artifact stands alone.
    real = {}
    for label, gpkg in (("majority_2026", MAJ_CANONICAL), ("minority_2026", MIN_CANONICAL)):
        real[label] = score_exogenous_map(va, gpkg, id_col=CANONICAL_NAME_COL)
    with open(SCORES_JSON, "w", encoding="utf-8") as f:
        json.dump(real, f, indent=2, default=float)
    print(f"  wrote {SCORES_JSON.name}")

    rows_out = []
    for label in ("majority_2026", "minority_2026"):
        for m in metrics:
            val = float(real[label][m])
            pct = float((kept[m] < val).mean() * 100)
            rows_out.append({
                "metric": m, "map": label, "value": val, "percentile": pct,
                "ensemble_p5": float(np.nanpercentile(kept[m], 5)),
                "ensemble_p50": float(np.nanpercentile(kept[m], 50)),
                "ensemble_p95": float(np.nanpercentile(kept[m], 95)),
            })
    pd.DataFrame(rows_out).to_csv(PERCENTILES_CSV, index=False)
    print(f"  wrote {PERCENTILES_CSV.name}")

    print()
    print("Execution log for OSF append (prereg §8.4):")
    print(f"  registration: {args.osf_registration_id}")
    print(f"  base salt/seed: {PREREG_SALT!r} / {seed}")
    for m in metrics:
        print(f"  {m}: n_eff={conv[m]['n_eff']:.0f} tau={conv[m]['tau']:.0f}")
    minority_pcts = {r['metric']: r['percentile'] for r in rows_out if r['map'] == 'minority_2026'}
    print(f"  minority percentiles (Phase A forest null): "
          + ", ".join(f"{m}=p{p:.2f}" for m, p in minority_pcts.items()))
    print()
    print("Next: write findings/forest_recom_robustness.md within 7 days (prereg §8.1)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
