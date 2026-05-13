"""
mcmc_anchoring_ensemble.py
--------------------------
Mini-ensemble for municipal-boundary anchoring via CSD edge-crossing metric.

This implements the "municipal anchoring departure" channel registered in OSF s58a6
but not executed in the Section C run (which lacked per-plan anchoring capture).

Metric definition (edge-crossing approximation):
  For each plan in the ensemble, compute:
    csd_anchoring = |{cut edges that cross a CSD boundary}| / |all cut edges|
  A CSD-crossing cut edge connects two VAs in DIFFERENT CSDs. A high value means
  district boundaries align with CSD divisions (anchored). A low value means
  boundaries cut through CSDs (unanchored).

Seed derivation (same drand beacon as Section C, OSF s58a6):
  beacon randomness: 5b893b864ba71c70cfd0d0bb3b5549730eaeb282ea1140cf3d72a3167934a9a8
  salt: "alberta-audit-anchoring-ensemble"
  seed: 80780579

Null hypothesis: both real maps score within the ensemble distribution on
  csd_anchoring (no evidence of anomalous anchoring behaviour).
Pass threshold: csd_anchoring percentile outside [5, 95] triggers a flag.
Predicted direction (minority map): lower anchoring fraction than ensemble
  median (pre-registered direction consistent with existing geometric result).

Runtime: ~10 min for 10,000 plans (2 chains × 5,000) on a modern laptop.

Usage:
    python analysis/scripts/mcmc_anchoring_ensemble.py [--n-steps 5000]

Outputs:
    data/outputs/csd_anchoring_ensemble.csv   -- per-plan anchoring fractions
    data/outputs/csd_anchoring_results.json   -- real-map scores and percentiles
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from mcmc_ensemble import build_va_graph, initial_assignment_2019  # noqa: E402

try:
    from gerrychain import Graph, MarkovChain, Partition, updaters, accept
    from gerrychain.proposals import recom
    from gerrychain.tree import bipartition_tree as _bpt_global, recursive_tree_part
    from functools import partial
    GERRYCHAIN_OK = True
except ImportError:
    GERRYCHAIN_OK = False

DATA = ROOT / "data"
CSD_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
ASSIGNMENT_CSV = DATA / "outputs" / "assignment_va_to_2026_canonical.csv"
MAJ_GPKG = DATA / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg"
MIN_GPKG = DATA / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"

ANCHORING_CSV = DATA / "outputs" / "csd_anchoring_ensemble.csv"
RESULTS_JSON = DATA / "outputs" / "csd_anchoring_results.json"

SEED = 80780579  # derived from drand round 6099592 salt "alberta-audit-anchoring-ensemble"
POP_DEVIATION = 0.25
N_CHAINS = 2


def derive_seed(chain_idx: int, base: int = SEED) -> int:
    return (base * 100_000 + chain_idx * 1_000) % (2**32)


def assign_csd_to_vas(va: gpd.GeoDataFrame, csds: gpd.GeoDataFrame) -> pd.Series:
    """Return Series: va index -> CSDUID (NaN if centroid not inside any CSD)."""
    if csds.crs != va.crs:
        csds = csds.to_crs(va.crs)
    centroids = va.copy()
    centroids["geometry"] = centroids.geometry.centroid
    joined = gpd.sjoin(
        centroids[["geometry"]],
        csds[["CSDUID", "geometry"]],
        how="left",
        predicate="within",
    )
    # Deduplicate if centroid falls on a boundary
    joined = joined[~joined.index.duplicated(keep="first")]
    return joined["CSDUID"]


def build_csd_crossing_edges(graph, csd_series: pd.Series) -> frozenset:
    """Return frozenset of (u, v) edge tuples where u and v are in different CSDs.
    Edges are stored as (min, max) pairs to make lookup direction-agnostic.
    """
    crossing = set()
    for u, v in graph.edges():
        csd_u = csd_series.get(u)
        csd_v = csd_series.get(v)
        if pd.notna(csd_u) and pd.notna(csd_v) and csd_u != csd_v:
            crossing.add((min(u, v), max(u, v)))
    return frozenset(crossing)


def real_map_anchoring(graph, crossing: frozenset,
                       assignment_col: str, assignment_df: pd.DataFrame) -> float:
    """Compute CSD anchoring fraction for one real map.

    Uses OBJECTID as the join key. OBJECTID is 1-indexed and sequential in the
    canonical VA shapefile, so graph node id = OBJECTID - 1.

    assignment_col: 'ed_2026_maj' or 'ed_2026_min'
    assignment_df: the canonical assignment CSV (must have OBJECTID column)
    """
    # Build graph node index → ED mapping (OBJECTID - 1 = node index)
    node_to_ed: dict[int, str] = {}
    for _, row in assignment_df.iterrows():
        node_id = int(row["OBJECTID"]) - 1  # 1-indexed → 0-indexed
        ed = row[assignment_col]
        if pd.notna(ed):
            node_to_ed[node_id] = str(ed)

    # Identify cut edges among assigned nodes
    cut_edges = []
    for u, v in graph.edges():
        ed_u = node_to_ed.get(u)
        ed_v = node_to_ed.get(v)
        if ed_u is not None and ed_v is not None and ed_u != ed_v:
            cut_edges.append((min(u, v), max(u, v)))

    if not cut_edges:
        return float("nan")

    csd_crossing_cut = sum(1 for e in cut_edges if e in crossing)
    return csd_crossing_cut / len(cut_edges)


def run_anchoring_chain(
    graph, initial_state, n_steps: int, csd_crossing: frozenset,
    chain_idx: int, seed: int, pop_deviation: float,
) -> list[float]:
    """Run one MCMC chain and return per-step csd_anchoring fractions."""
    import random as _random
    import numpy as _np

    _np.random.seed(seed)
    _random.seed(seed)

    total_pop = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
    num_dist = len(set(initial_state.values()))
    ideal_pop = total_pop / num_dist

    # CSD anchoring is computed from cut_edges outside the updater system
    # to avoid GerryChain version-specific __getitem__ issues.
    my_updaters = {
        "population": updaters.Tally("pop_2021", alias="population"),
        "cut_edges": updaters.cut_edges,
    }

    # Check if initial seed satisfies the population constraint.
    # The 2019 seed often violates ±25% due to 2019->2021 growth.
    # Use the same fallback as run_ensemble: generate a fresh seed via
    # recursive_tree_part.
    seed_partition = Partition(graph, initial_state, my_updaters)
    seed_pops = list(seed_partition["population"].values())
    seed_max_dev = max(abs(p - ideal_pop) / ideal_pop for p in seed_pops)
    if seed_max_dev > pop_deviation:
        import random as _r
        # Try multiple seed offsets — recursive_tree_part can fail on complex geometries
        new_assignment = None
        for _offset in range(0, 20000, 1000):
            try:
                _np.random.seed(seed + 999 + _offset)
                _r.seed(seed + 999 + _offset)
                new_assignment = recursive_tree_part(
                    graph,
                    parts=list(range(num_dist)),
                    pop_target=ideal_pop,
                    pop_col="pop_2021",
                    epsilon=pop_deviation,
                    node_repeats=5,
                    method=partial(_bpt_global, max_attempts=50000),
                )
                break
            except RuntimeError:
                continue
        if new_assignment is None:
            raise RuntimeError(
                "recursive_tree_part failed for all seed offsets. "
                "Try a different base seed or increase max_attempts."
            )
        _np.random.seed(seed)
        _r.seed(seed)
        initial_partition = Partition(graph, new_assignment, my_updaters)
    else:
        initial_partition = seed_partition

    def pop_constraint(partition):
        ideal = ideal_pop
        for part_id, pop in partition["population"].items():
            dev = abs(pop - ideal) / ideal
            if dev > pop_deviation:
                return False
        return True

    _recom_method = partial(_bpt_global, allow_pair_reselection=True)
    proposal = partial(
        recom,
        pop_col="pop_2021",
        pop_target=ideal_pop,
        epsilon=pop_deviation / 2.0,
        node_repeats=2,
        method=_recom_method,
    )

    chain = MarkovChain(
        proposal=proposal,
        constraints=[pop_constraint],
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=n_steps,
    )

    results = []
    t0 = time.time()
    for step, part in enumerate(chain):
        cut = part["cut_edges"]
        if cut:
            n_crossing = sum(
                1 for u, v in cut
                if (min(u, v), max(u, v)) in csd_crossing
            )
            anchoring = n_crossing / len(cut)
        else:
            anchoring = 0.0
        results.append(anchoring)

        if (step + 1) % 500 == 0:
            elapsed = time.time() - t0
            rate = (step + 1) / elapsed
            remaining = (n_steps - step - 1) / rate
            print(
                f"  [chain {chain_idx}] step {step+1}/{n_steps} "
                f"({rate:.1f} steps/s, ~{remaining:.0f}s remaining)",
                flush=True,
            )

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-steps", type=int, default=5000,
                        help="Steps per chain (default 5000; 2 chains = 10000 total)")
    args = parser.parse_args()

    if not GERRYCHAIN_OK:
        print("ERROR: gerrychain not available. Install with: pip install gerrychain")
        sys.exit(1)

    print("=" * 60)
    print("Municipal Anchoring Ensemble (OSF s58a6 pending channel)")
    print(f"Seed: {SEED} | Chains: {N_CHAINS} | Steps/chain: {args.n_steps}")
    print("=" * 60)

    # --- Build VA graph ---
    print("\nBuilding VA adjacency graph...")
    va, graph = build_va_graph(verbose=True)
    print(f"Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")

    # --- Assign CSDs ---
    print("\nAssigning CSDs to VAs via centroid spatial join...")
    csds = gpd.read_file(CSD_GPKG)
    csd_series = assign_csd_to_vas(va, csds)
    n_assigned = csd_series.notna().sum()
    print(f"  {n_assigned}/{len(va)} VAs assigned to a CSD "
          f"({csd_series.nunique()} unique CSDs)")

    # --- Pre-compute CSD-crossing edges ---
    print("Pre-computing CSD-crossing edges...")
    crossing = build_csd_crossing_edges(graph, csd_series)
    total_edges = graph.number_of_edges()
    print(f"  {len(crossing)}/{total_edges} edges cross a CSD boundary "
          f"({100*len(crossing)/total_edges:.1f}%)")

    # --- Score real maps ---
    print("\nScoring real maps...")
    assignment_df = pd.read_csv(ASSIGNMENT_CSV)

    maj_score = real_map_anchoring(graph, crossing, "ed_2026_maj", assignment_df)
    min_score = real_map_anchoring(graph, crossing, "ed_2026_min", assignment_df)
    print(f"  Majority 2026 CSD anchoring: {maj_score:.4f} ({100*maj_score:.2f}%)")
    print(f"  Minority 2026 CSD anchoring: {min_score:.4f} ({100*min_score:.2f}%)")

    # --- Run ensemble chains ---
    initial_state = initial_assignment_2019(va)
    all_samples = []

    for chain_idx in range(N_CHAINS):
        chain_seed = derive_seed(chain_idx)
        print(f"\nRunning chain {chain_idx} (seed={chain_seed}, {args.n_steps} steps)...")
        chain_results = run_anchoring_chain(
            graph, initial_state, args.n_steps, crossing,
            chain_idx, chain_seed, POP_DEVIATION,
        )
        all_samples.extend(chain_results)
        print(f"  Chain {chain_idx} done: mean={np.mean(chain_results):.4f}, "
              f"std={np.std(chain_results):.4f}")

    # --- Compute percentiles ---
    dist = np.array(all_samples)
    maj_ptile = float(np.mean(dist <= maj_score) * 100.0)
    min_ptile = float(np.mean(dist <= min_score) * 100.0)

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Ensemble: {len(dist):,} plans | "
          f"median={np.median(dist):.4f} | p5={np.percentile(dist,5):.4f} | "
          f"p95={np.percentile(dist,95):.4f}")
    print(f"\nMajority 2026: {maj_score:.4f} -> p{maj_ptile:.2f}")
    print(f"Minority 2026: {min_score:.4f} -> p{min_ptile:.2f}")

    maj_flag = maj_ptile <= 5 or maj_ptile >= 95
    min_flag = min_ptile <= 5 or min_ptile >= 95
    print(f"\nMajority outlier (p<=5 or p>=95): {'YES ***' if maj_flag else 'no'}")
    print(f"Minority outlier (p<=5 or p>=95): {'YES ***' if min_flag else 'no'}")

    # --- Save outputs ---
    samples_df = pd.DataFrame({"csd_anchoring": dist,
                                "chain": ([0]*args.n_steps + [1]*args.n_steps)[:len(dist)]})
    samples_df.to_csv(ANCHORING_CSV, index=False)
    print(f"\nEnsemble samples -> {ANCHORING_CSV.relative_to(ROOT)}")

    results = {
        "seed": SEED,
        "n_plans": len(dist),
        "n_chains": N_CHAINS,
        "n_steps_per_chain": args.n_steps,
        "ensemble_median": float(np.median(dist)),
        "ensemble_p5": float(np.percentile(dist, 5)),
        "ensemble_p95": float(np.percentile(dist, 95)),
        "majority_2026": {
            "csd_anchoring": maj_score,
            "percentile": maj_ptile,
            "outlier": maj_flag,
        },
        "minority_2026": {
            "csd_anchoring": min_score,
            "percentile": min_ptile,
            "outlier": min_flag,
        },
        "csd_crossing_edges": len(crossing),
        "total_edges": total_edges,
        "n_vas_with_csd": int(n_assigned),
    }
    with open(RESULTS_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results -> {RESULTS_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
