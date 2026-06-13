# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
local_perturbation_chain.py — Issue #13 local-perturbation null
=================================================================

Named retractor for retraction condition 2.3A in
preregistration/retraction_conditions.md:

  "If a local-perturbation null (single-VA swaps only, contiguity preserved)
  shows the audit's Lane-1 outlier flags fire for ≥ 5% of perturbed minority
  variants, the headline Lane-1 result is retracted."

The full canonical 1.01M ReCom ensemble is the headline null. The local-
perturbation chain is a *complementary* null at the opposite end of the
neutrality spectrum: minimal, structure-preserving variations of the real
minority map that test whether the metric outliers are robust to "tiny
unintended differences" rather than to wholesale neutral redrawing. If the
flags fire for many neighborhoods of the real map, that suggests the outlier
status is fragile.

Construction
------------
1. Start from the canonical minority map (89 EDs).
2. For each VA at an ED boundary, propose moving it to the neighboring ED.
3. Reject the proposal if it violates contiguity OR pushes either ED outside
   the ±25% population deviation envelope.
4. Accept N = 10,000 accepted single-VA swaps as the chain.
5. Score every accepted variant on the four partisan-bias metrics + Mahalanobis
   joint distance vs the canonical 1.01M ensemble distribution.

Inputs
------
--shapefile PATH      Start shapefile (default: canonical minority).
--votes PATH          VA-level vote shapefile (default: canonical).
--n-perturbations N   Number of accepted single-VA swaps (default: 10,000).
--pop-tolerance F     Per-ED population deviation envelope (default: 0.25).
--ensemble PATH       Canonical ensemble for percentile placement.
--seed N              drand-pinned base seed (REQUIRED for retraction-grade run).
--output PATH         JSON output path.

Output
------
JSON with:
  {
    "n_perturbations_accepted": int,
    "n_perturbations_attempted": int,
    "acceptance_rate": float,
    "perturbation_metric_distribution": {EG: [...], MM: [...], decl: [...], s50: [...]},
    "fraction_perturbations_with_at_least_one_flag_at_p95": float,
    "retraction_condition_2_3_a_fired": bool,    # True iff fraction >= 0.05
    "real_map_metrics": {...},
    "seed": int,
  }

Retraction rule (frozen):
  retraction_condition_2_3_a_fired = (
    fraction_perturbations_with_at_least_one_flag_at_p95 >= 0.05
  )

If True, the audit retracts the Lane-1 headline per
preregistration/retraction_conditions.md §2.3.

Status: IMPLEMENTED (Issue #13)
---------------------------------
single_va_swap() implemented 2026-06-13.
Wire-in points marked with TODO(issue-13) are now wired.
The framework reuses:
  - analysis/scripts/mcmc_ensemble.py::build_va_graph (start state)
  - analysis/scripts/mcmc_ensemble.py::seat_results (metric computation)
  - analysis/scripts/constraint_enforcing_ensemble.py::assign_from_canonical
  - data/simulation_checkpoints_canonical/chain*_samples.csv (percentile placement)

Design notes (single_va_swap):
  - Population check is DIRECTIONAL (docstring spec), not symmetric absolute.
    This handles pre-existing s.15(2) special-rural districts (e.g., Central
    Peace-Notley, Lesser Slave Lake) that start below ideal*(1-tol). A
    symmetric check would incorrectly block every move touching those districts.
    Rule: reject only if the donor would drop BELOW ideal*(1-tol) OR the
    recipient would RISE ABOVE ideal*(1+tol). Districts already outside their
    bound can still move in the permissible direction.
  - Connectivity check uses nx.is_connected() on the donor subgraph after
    removing the proposed node. Guard for a 1-node donor (empty after removal)
    which would raise NetworkXPointlessConcept — reject explicitly.
  - Recipient connectivity is trivially guaranteed: the proposed node is
    adjacent to a node already in the recipient district.
  - partition.flip({v: new_district}) is used for incremental updates so
    population/cut_edges updaters are maintained without full reconstruction.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))


# ----- Retraction threshold (frozen 2026-06-10) -----
RETRACTION_FRACTION_THRESHOLD = 0.05
P95_TAIL_THRESHOLD = 0.95
DEFAULT_N_PERTURBATIONS = 10_000
DEFAULT_POP_TOLERANCE = 0.25


def single_va_swap(graph, partition, rng, pop_tolerance=DEFAULT_POP_TOLERANCE):
    """One step of the local-perturbation chain.

    Proposal (edge-uniform kernel):
      1. Choose a random cut edge uniformly from partition.cut_edges.
      2. Randomly orient it: v is the node to move, u is the neighbor
         in the destination district.
      3. Propose moving v from its current district to u's district.

    Note: this is EDGE-uniform, not VA-uniform. VAs with more cross-district
    neighbours are more likely to be selected as the node to move. This matches
    the gerrychain-idiomatic `propose_random_flip` kernel and is appropriate
    for an always-accept null; the stationary distribution is not being
    targeted, so the kernel's non-uniform selection over VAs is not a bias
    concern. The original stub docstring said "VA-uniform" but the pre-registered
    spec for Issue #13 does not pin this choice — edge-uniform is implemented
    here and documented explicitly.

    Acceptance:
      - Reject if moving breaks contiguity of the source ED (the donating ED).
      - Reject if the destination ED's population would exceed ideal × (1 + tol).
      - Reject if the source ED's population would drop below ideal × (1 - tol).
      - Accept otherwise (always-accept within valid moves).

    Population check is DIRECTIONAL: a district already below ideal*(1-tol) can
    still accept incoming VAs (it just cannot donate further and dip lower). This
    is required because the minority canonical map contains s.15(2) special-rural
    districts already below the normal ±25% envelope (min deviation confirmed at
    −41.1% in smoke test). A symmetric ±25% absolute check would freeze those
    districts entirely and silently distort the null distribution.

    Returns: (accepted: bool, new_partition).
    """
    cut_edges = list(partition.cut_edges)
    if not cut_edges:
        # No boundary — nothing to propose
        return False, partition

    # Sample a random boundary edge then orient it: v is the node to move,
    # u is the neighbor in the destination district.
    # Use rng.integers to index into the list — avoids numpy coercing a list
    # of 2-tuples into a 2D array (which rng.choice would do).
    idx = int(rng.integers(len(cut_edges)))
    edge = cut_edges[idx]
    v, u = edge[0], edge[1]

    # With 50% probability, swap orientation so we don't systematically bias
    # toward one endpoint ordering that gerrychain happens to store first.
    if rng.integers(2) == 1:
        v, u = u, v

    donor_district = partition.assignment[v]
    recipient_district = partition.assignment[u]

    # Sanity: they should be in different districts (they're a cut edge)
    if donor_district == recipient_district:
        return False, partition

    # ── Population check (directional) ──────────────────────────────────────
    # Compute ideal from the partition's population tally (avoids iterating all
    # 4765 graph nodes on every proposal; the Tally updater already has the sums).
    n_districts = len(partition.parts)
    total_pop = sum(partition["population"].values())
    ideal = total_pop / n_districts

    va_pop = graph.nodes[v]["pop_2021"]
    donor_pop_after = partition["population"][donor_district] - va_pop
    recipient_pop_after = partition["population"][recipient_district] + va_pop

    # Donor dropping too low?
    if donor_pop_after < ideal * (1.0 - pop_tolerance):
        return False, partition

    # Recipient rising too high?
    if recipient_pop_after > ideal * (1.0 + pop_tolerance):
        return False, partition

    # ── Connectivity check (donor only) ─────────────────────────────────────
    # Recipient is trivially connected: v is adjacent to u which is already
    # in the recipient district.
    donor_nodes = set(partition.parts[donor_district]) - {v}

    if len(donor_nodes) == 0:
        # Single-node donor — moving v would create an empty district.
        # Reject: empty districts are invalid.
        return False, partition

    donor_subgraph = graph.subgraph(donor_nodes)
    if not nx.is_connected(donor_subgraph):
        return False, partition

    # ── Accept: apply the flip ───────────────────────────────────────────────
    new_partition = partition.flip({v: recipient_district})
    return True, new_partition


def _build_minority_partition(graph, va):
    """Assign VAs to canonical minority map districts and build a Partition."""
    # Import here to keep the top-level namespace clean
    sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
    from constraint_enforcing_ensemble import assign_from_canonical
    from gerrychain import Partition, updaters as gc_updaters

    ed_assign = assign_from_canonical(va, "minority")
    # assign_from_canonical returns a Series indexed by va DataFrame index
    init_assign = {idx: ed for idx, ed in ed_assign.items() if not _isnan(ed)}

    my_updaters = {
        "population": gc_updaters.Tally("pop_2021", alias="population"),
        "ucp": gc_updaters.Tally("va_ucp", alias="ucp"),
        "ndp": gc_updaters.Tally("va_ndp", alias="ndp"),
        "cut_edges": gc_updaters.cut_edges,
    }
    return Partition(graph, init_assign, my_updaters)


def _isnan(x):
    try:
        import math
        return math.isnan(x)
    except (TypeError, ValueError):
        return x is None or str(x).lower() in ("nan", "none", "")


def _run_smoke_test(graph, va, n_steps=200, seed=None, pop_tolerance=DEFAULT_POP_TOLERANCE):
    """Build a minority-map partition and run n_steps swap proposals.

    Used by main() in dev mode when --dry-run is given or shapefiles are absent.
    Returns (n_accepted, n_attempted, acceptance_rate).
    """
    rng = np.random.default_rng(seed)

    print(f"[smoke] Building minority canonical partition ...", flush=True)
    partition = _build_minority_partition(graph, va)

    # Diagnostic: verify population distribution
    pops = list(partition["population"].values())
    n_districts = len(pops)
    total_pop = sum(pops)
    ideal = total_pop / n_districts
    min_dev = min(p / ideal - 1 for p in pops)
    max_dev = max(p / ideal - 1 for p in pops)
    print(
        f"[smoke] {n_districts} districts; ideal={ideal:,.0f}; "
        f"pop deviation range [{min_dev:+.1%}, {max_dev:+.1%}]",
        flush=True,
    )
    if min_dev < -(pop_tolerance + 0.01):
        print(
            f"[smoke] NOTE: s.15(2) districts present below -{pop_tolerance:.0%} "
            f"(min={min_dev:+.1%}). Directional population check is mandatory.",
            flush=True,
        )

    n_cut = len(partition.cut_edges)
    print(f"[smoke] {n_cut} cut edges on minority map boundary.", flush=True)

    n_accepted = 0
    n_attempted = 0
    t0 = time.time()
    for _ in range(n_steps):
        accepted, partition = single_va_swap(graph, partition, rng, pop_tolerance)
        n_attempted += 1
        if accepted:
            n_accepted += 1

    rate = n_accepted / n_attempted if n_attempted else float("nan")
    elapsed = time.time() - t0
    print(
        f"[smoke] {n_accepted}/{n_attempted} accepted ({rate:.1%}) "
        f"in {elapsed:.2f}s ({n_attempted/elapsed:.0f} proposals/s)",
        flush=True,
    )
    return n_accepted, n_attempted, rate


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--shapefile", type=Path,
                    default=ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg")
    ap.add_argument("--votes", type=Path,
                    default=ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg")
    ap.add_argument("--n-perturbations", type=int, default=DEFAULT_N_PERTURBATIONS)
    ap.add_argument("--pop-tolerance", type=float, default=DEFAULT_POP_TOLERANCE)
    ap.add_argument("--ensemble", type=Path,
                    default=ROOT / "data/simulation_checkpoints_canonical")
    ap.add_argument("--seed", type=int, required=False,
                    help="drand-pinned base seed (REQUIRED for retraction-grade run).")
    ap.add_argument("--output", type=Path,
                    default=ROOT / "findings/local_perturbation_chain.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="Run a 200-step smoke test only (no full scored run).")
    args = ap.parse_args(argv)

    if args.seed is None:
        print(
            "WARN: --seed not provided. Retraction-grade runs require a drand-pinned seed "
            "filed in preregistration/seed_commitments.md. Proceeding in dev mode.",
            file=sys.stderr,
        )

    print(f"[local-perturbation chain] Issue #13 — single_va_swap() implemented.")
    print(f"  start shapefile: {args.shapefile.name}")
    print(f"  n_perturbations: {args.n_perturbations}")
    print(f"  pop_tolerance:   ±{args.pop_tolerance*100:.0f}%")
    print(f"  seed:            {args.seed}")
    print(f"  dry_run:         {args.dry_run}", flush=True)

    # Load graph (needed for both smoke test and full run)
    sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
    from mcmc_ensemble import build_va_graph

    print(f"\n[setup] Loading VA graph ...", flush=True)
    va, graph = build_va_graph(verbose=True)

    if args.dry_run:
        print(f"\n[dry-run] Running 200-step smoke test of single_va_swap() ...", flush=True)
        n_acc, n_att, rate = _run_smoke_test(
            graph, va, n_steps=200, seed=args.seed, pop_tolerance=args.pop_tolerance
        )
        result = {
            "_mode": "dry-run",
            "smoke_test_accepted": n_acc,
            "smoke_test_attempted": n_att,
            "smoke_test_acceptance_rate": rate,
            "seed": args.seed,
            "pop_tolerance": args.pop_tolerance,
            "executed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2))
        print(f"\nDry-run complete. Wrote smoke-test result to {args.output}")
        return 0

    # ── Full scored run ───────────────────────────────────────────────────────
    # METHODOLOGY NOTE (open for pre-registration owner to resolve before
    # retraction-grade run):
    #
    # 1. Flagging is UPPER-TAIL only (metric >= p95). The canonical ensemble
    #    scores use >=95th OR <=5th as the two-tailed convention. The retraction
    #    key name "..._at_p95" implies upper-tail; confirmed by the construction
    #    description ("outlier flags fire") but not explicitly stated in the
    #    frozen retraction-condition text. If the owner intends two-tailed,
    #    change the `flagged` predicate below to include `<= p5`.
    #
    # 2. Ensemble p95 thresholds are derived HERE from the raw checkpoint CSVs
    #    in data/simulation_checkpoints_canonical/chain*_samples.csv. The
    #    committed, reproducibility-frozen output is
    #    data/outputs/simulated_ensemble_percentiles_canonical.csv. For a
    #    retraction-grade run, prefer reading from that committed file so
    #    the threshold is verifiably identical to what the headline finding
    #    used. The checkpoint-CSV approach is used here because the percentiles
    #    CSV is indexed differently; this should be reconciled before the
    #    pre-registered run.
    #
    # 3. The full scored path (below the dry-run branch) was not end-to-end
    #    tested in development (2026-06-13). Only `--dry-run` was exercised.
    #    Run with --n-perturbations 5 before committing to a full retraction
    #    run to confirm end-to-end correctness.
    print(f"\n[setup] Building minority canonical partition ...", flush=True)
    rng = np.random.default_rng(args.seed)
    partition = _build_minority_partition(graph, va)

    # Compute ideal for population gate
    n_districts = len(partition.parts)
    total_pop = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
    ideal = total_pop / n_districts

    # Score real minority map
    from mcmc_ensemble import seat_results
    keys = list(partition.parts.keys())
    real_ucp = np.array([partition["ucp"][k] for k in keys], dtype=float)
    real_ndp = np.array([partition["ndp"][k] for k in keys], dtype=float)
    real_metrics = seat_results(real_ucp, real_ndp)
    print(f"  Real minority map: {real_metrics}", flush=True)

    # Load ensemble percentile thresholds if available
    ens_thresholds = {}
    if args.ensemble.exists():
        import pandas as pd
        chain_csvs = sorted(args.ensemble.glob("chain*_samples.csv"))
        if chain_csvs:
            dfs = [pd.read_csv(p) for p in chain_csvs]
            ens_df = pd.concat(dfs, ignore_index=True)
            for col in ("efficiency_gap", "mean_median", "declination", "seats_at_50_50"):
                if col in ens_df.columns:
                    ens_thresholds[col] = float(np.nanpercentile(ens_df[col], 95))
            print(f"  Loaded ensemble p95 thresholds: {ens_thresholds}", flush=True)
        else:
            print(f"  WARN: No chain CSVs found in {args.ensemble}; "
                  f"cannot score perturbations against ensemble p95.", flush=True)
    else:
        print(f"  WARN: Ensemble dir not found: {args.ensemble}; "
              f"skipping ensemble-relative scoring.", flush=True)

    # ── Perturbation loop ─────────────────────────────────────────────────────
    metric_dist = {
        "efficiency_gap": [],
        "mean_median": [],
        "declination": [],
        "seats_at_50_50": [],
    }
    n_accepted = 0
    n_attempted = 0
    n_flagged = 0  # plans with ≥1 metric flag at p95

    print(f"\n[chain] Running up to {args.n_perturbations} accepted swaps ...", flush=True)
    t0 = time.time()
    last_report = t0

    while n_accepted < args.n_perturbations:
        accepted, partition = single_va_swap(
            graph, partition, rng, args.pop_tolerance
        )
        n_attempted += 1

        if not accepted:
            continue

        n_accepted += 1

        # Score this accepted variant
        keys = list(partition.parts.keys())
        ucp_arr = np.array([partition["ucp"][k] for k in keys], dtype=float)
        ndp_arr = np.array([partition["ndp"][k] for k in keys], dtype=float)
        m = seat_results(ucp_arr, ndp_arr)

        for col in metric_dist:
            metric_dist[col].append(m.get(col, float("nan")))

        # Check p95 flag against ensemble thresholds
        if ens_thresholds:
            flagged = any(
                not np.isnan(m.get(col, float("nan")))
                and m.get(col, float("nan")) >= ens_thresholds[col]
                for col in ens_thresholds
            )
            if flagged:
                n_flagged += 1

        now = time.time()
        if now - last_report > 30:
            rate_acc = n_accepted / (now - t0)
            eta = (args.n_perturbations - n_accepted) / rate_acc if rate_acc > 0 else float("nan")
            acc_rate = n_accepted / n_attempted if n_attempted else float("nan")
            print(
                f"  {n_accepted}/{args.n_perturbations} accepted "
                f"(attempt rate={acc_rate:.1%}, eta {eta/60:.1f} min)",
                flush=True,
            )
            last_report = now

    elapsed = time.time() - t0
    acceptance_rate = n_accepted / n_attempted if n_attempted else float("nan")
    fraction_flagged = n_flagged / n_accepted if n_accepted and ens_thresholds else float("nan")
    retraction_fired = (
        (fraction_flagged >= RETRACTION_FRACTION_THRESHOLD)
        if not np.isnan(fraction_flagged)
        else None
    )

    print(f"\n[result] {n_accepted} accepted in {n_attempted} attempts "
          f"({acceptance_rate:.1%}) in {elapsed:.0f}s", flush=True)
    if ens_thresholds:
        print(f"[result] fraction with >=1 p95 flag: {fraction_flagged:.3%}")
        print(f"[result] retraction condition 2.3A fired: {retraction_fired}")

    result = {
        "n_perturbations_accepted": n_accepted,
        "n_perturbations_attempted": n_attempted,
        "acceptance_rate": float(acceptance_rate),
        "perturbation_metric_distribution": {
            k: [float(x) for x in v] for k, v in metric_dist.items()
        },
        "fraction_perturbations_with_at_least_one_flag_at_p95": (
            float(fraction_flagged) if not np.isnan(fraction_flagged) else None
        ),
        "retraction_condition_2_3_a_fired": retraction_fired,
        "real_map_metrics": {k: (float(v) if not np.isnan(v) else None)
                             for k, v in real_metrics.items()},
        "ensemble_p95_thresholds_used": ens_thresholds,
        "seed": args.seed,
        "pop_tolerance": args.pop_tolerance,
        "_retraction_rule_frozen": (
            "Lane-1 headline is retracted if "
            f">= {RETRACTION_FRACTION_THRESHOLD*100:.0f}% of accepted perturbations "
            f"produce >= 1 metric flag at p>={P95_TAIL_THRESHOLD*100:.0f} against the "
            f"canonical 1,010,000-plan ReCom ensemble."
        ),
        "executed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(f"\nWrote output to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
