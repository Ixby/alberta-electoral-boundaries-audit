"""
constraint_enforcing_ensemble.py — ReCom adapted to cover what the canonical
ensemble was missing (T1.4 + T1.11, 2026-06-13).

Three adaptations relative to mcmc_ensemble.py's canonical run:

1. FULL ±25% PROPOSAL EPSILON (T1.11). The canonical run set
   `epsilon = pop_deviation / 2.0` in the ReCom proposal, exploring only
   ±12.5% — half the documented legal space. This script uses
   `epsilon = pop_deviation` (the full ±25% the Electoral Divisions Act
   permits as the normal tolerance).

2. s.15(2) TIER VIA FREEZE-FROM-REAL-SEED (T1.4 partial). The EBCA s.15(2)
   permits up to 4 districts as much as 50% below average. The canonical
   ensemble could not reach that tier (its uniform constraint floor was −25%),
   and the audit's earlier freeze attempt (H6) failed because
   `recursive_tree_part` could not seed-balance the unfrozen 85-district
   subgraph from scratch. The fix implemented here: SEED FROM THE REAL
   COMMISSION MAP (majority canonical assignment via spatial join), identify
   the s.15(2) districts in the seed (population below 0.75 × ideal), REMOVE
   their VAs from the graph, and run ReCom on the remaining ~86 districts.
   Because the seed comes from a real feasible map, no fresh seeding is needed
   — the known infeasibility is bypassed entirely. The frozen districts'
   votes/populations are added back as constants when computing per-plan
   metrics, so every sampled plan is a *complete* 89-district plan in which
   the 3 protected districts are held at their commission-drawn boundaries.

3. MUNICIPAL-SPLIT TALLY (T1.4 partial, soft constraint OFF by default).
   Each VA is tagged with its 2021 CSD (city/town) via spatial join at graph
   build time. A per-plan updater counts how many multi-VA municipalities are
   split across ≥2 districts. By default the count is *recorded* per plan
   (so the real maps' split counts can be percentile-placed) rather than
   *constrained*, because hard-constraining splits would need a calibrated
   threshold the audit has not pre-registered. Pass --max-splits N to enforce.

Output: data/outputs/constraint_enforcing_ensemble_<steps>.csv with the same
metric columns as the canonical chain CSVs (Warrington-signed declination)
plus `municipal_splits`, and a JSON summary with real-map percentile
placements against this constrained ensemble vs the unconstrained canonical.

Usage:
  python analysis/scripts/constraint_enforcing_ensemble.py --steps 100000 --seed-salt constraint-ensemble-v1
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from functools import partial
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from gerrychain import Graph, MarkovChain, Partition, accept, constraints, updaters
from gerrychain.proposals import recom
from gerrychain.tree import bipartition_tree as _bpt

from mcmc_ensemble import build_va_graph, seat_results, score_exogenous_map
from canonical_paths import canonical_shapefile, ED_NAME_COL

try:
    from drand_seed import get_canonical_seed
except Exception:
    def get_canonical_seed(salt: str) -> int:
        import hashlib
        return int(hashlib.sha256(salt.encode()).hexdigest()[:12], 16) & ((1 << 32) - 1)

CSD_PATH = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
OUT_DIR = ROOT / "data/outputs"


def assign_from_canonical(va: gpd.GeoDataFrame, plan: str) -> pd.Series:
    """Assign each VA to its containing ED on the given canonical map."""
    eds = gpd.read_file(canonical_shapefile(plan))[[ED_NAME_COL, "geometry"]]
    if eds.crs != va.crs:
        eds = eds.to_crs(va.crs)
    cents = va.copy()
    cents["geometry"] = va.geometry.representative_point()
    joined = gpd.sjoin(cents[["geometry"]], eds, how="left", predicate="within")
    joined = joined[~joined.index.duplicated(keep="first")]
    ser = joined[ED_NAME_COL]
    if ser.isna().any():
        # Nearest fallback for the handful of unresolved centroids
        unresolved = ser.isna()
        nearest = gpd.sjoin_nearest(
            cents.loc[unresolved.values][["geometry"]], eds, how="left")
        nearest = nearest[~nearest.index.duplicated(keep="first")]
        ser.loc[unresolved] = nearest[ED_NAME_COL].values
    return ser


def tag_csd(va: gpd.GeoDataFrame) -> pd.Series:
    """Tag each VA with its containing 2021 CSD name (for municipal-split tally)."""
    csds = gpd.read_file(CSD_PATH)
    name_col = next((c for c in ("CSDNAME", "name", "NAME", "csd_name") if c in csds.columns), None)
    if name_col is None:
        raise RuntimeError(f"CSD layer columns: {csds.columns.tolist()} — no name column found")
    csds = csds[[name_col, "geometry"]].rename(columns={name_col: "csd"})
    if csds.crs != va.crs:
        csds = csds.to_crs(va.crs)
    cents = va.copy()
    cents["geometry"] = va.geometry.representative_point()
    joined = gpd.sjoin(cents[["geometry"]], csds, how="left", predicate="within")
    joined = joined[~joined.index.duplicated(keep="first")]
    return joined["csd"].fillna("(rural-unincorporated)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--steps", type=int, default=100_000)
    ap.add_argument("--pop-deviation", type=float, default=0.25)
    ap.add_argument("--seed-salt", type=str, default="constraint-ensemble-v1")
    ap.add_argument("--seed-map", type=str, default="majority",
                    choices=("majority", "minority"),
                    help="Real commission map to seed from (and whose s.15(2) districts to freeze)")
    ap.add_argument("--max-splits", type=int, default=None,
                    help="If set, hard-constrain municipal split count to <= N")
    ap.add_argument("--out-prefix", type=str, default=None)
    args = ap.parse_args(argv)

    seed = get_canonical_seed(args.seed_salt)
    rng_label = f"salt={args.seed_salt!r} -> seed={seed}"
    print(f"[setup] {rng_label}", flush=True)

    t0 = time.time()
    va, graph = build_va_graph(verbose=True)

    # ── Seed from the real commission map ─────────────────────────────────────
    print(f"[seed] Assigning VAs to {args.seed_map} canonical map ...", flush=True)
    ed_assign = assign_from_canonical(va, args.seed_map)
    va["seed_ed"] = ed_assign.values

    # ── Identify s.15(2) districts in the seed ────────────────────────────────
    pop_by_ed = va.groupby("seed_ed")["pop_2021"].sum()
    n_districts_total = len(pop_by_ed)
    ideal = pop_by_ed.sum() / n_districts_total
    s15_2 = pop_by_ed[pop_by_ed < 0.75 * ideal]
    print(f"[freeze] {n_districts_total} districts; ideal pop = {ideal:,.0f}", flush=True)
    print(f"[freeze] s.15(2) districts (< 75% of ideal): {list(s15_2.index)}", flush=True)
    for name, p in s15_2.items():
        print(f"    {name}: {p:,.0f} ({100*(p/ideal-1):+.1f}%)", flush=True)

    frozen_eds = set(s15_2.index)
    frozen_mask = va["seed_ed"].isin(frozen_eds).values
    n_frozen_vas = int(frozen_mask.sum())
    print(f"[freeze] Freezing {n_frozen_vas} VAs in {len(frozen_eds)} districts", flush=True)

    # Frozen-district constants for metric computation
    frozen_stats = va.loc[frozen_mask].groupby("seed_ed").agg(
        ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"), pop=("pop_2021", "sum"))

    # ── Municipal tags ─────────────────────────────────────────────────────────
    print(f"[csd] Tagging VAs with 2021 CSDs ...", flush=True)
    va["csd"] = tag_csd(va).values
    multi_va_csds = va.groupby("csd").size()
    multi_va_csds = set(multi_va_csds[multi_va_csds >= 2].index) - {"(rural-unincorporated)"}
    print(f"[csd] {len(multi_va_csds)} multi-VA municipalities tracked for split tally", flush=True)

    # ── Build the unfrozen subgraph ────────────────────────────────────────────
    keep_nodes = [n for n in graph.nodes() if not frozen_mask[n]]
    sub = graph.subgraph(keep_nodes).copy()
    # Attach csd attribute for the updater
    for n in sub.nodes():
        sub.nodes[n]["csd"] = va.loc[n, "csd"]
    print(f"[graph] Unfrozen subgraph: {sub.number_of_nodes()} nodes, "
          f"{sub.number_of_edges()} edges", flush=True)

    # Initial assignment on the subgraph from the seed map
    init_assign = {n: va.loc[n, "seed_ed"] for n in sub.nodes()}
    n_unfrozen_districts = len(set(init_assign.values()))
    sub_total_pop = sum(sub.nodes[n]["pop_2021"] for n in sub.nodes())
    sub_ideal = sub_total_pop / n_unfrozen_districts
    print(f"[graph] {n_unfrozen_districts} unfrozen districts; sub-ideal pop = {sub_ideal:,.0f}", flush=True)

    # Verify seed feasibility at the FULL epsilon
    seed_pops = pd.Series(init_assign).map(
        lambda ed: None)  # placeholder; compute below
    pops = {}
    for n, ed in init_assign.items():
        pops[ed] = pops.get(ed, 0.0) + sub.nodes[n]["pop_2021"]
    worst = max(abs(p / sub_ideal - 1) for p in pops.values())
    print(f"[seed] Worst unfrozen-district deviation in seed: {100*worst:.1f}% "
          f"(must be <= {100*args.pop_deviation:.0f}% + slack)", flush=True)

    my_updaters = {
        "population": updaters.Tally("pop_2021", alias="population"),
        "ucp": updaters.Tally("va_ucp", alias="ucp"),
        "ndp": updaters.Tally("va_ndp", alias="ndp"),
        "cut_edges": updaters.cut_edges,
    }

    initial_partition = Partition(sub, init_assign, my_updaters)

    # ── ReCom proposal at FULL epsilon (T1.11 fix) ────────────────────────────
    _recom_method = partial(_bpt, allow_pair_reselection=True)
    proposal = partial(
        recom,
        pop_col="pop_2021",
        pop_target=sub_ideal,
        epsilon=args.pop_deviation,  # FULL ±25% — the T1.11 correction
        node_repeats=2,
        method=_recom_method,
    )

    # Population constraint at the same epsilon (with seed slack if needed)
    eps_constraint = max(args.pop_deviation, worst + 0.01)
    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, eps_constraint)

    chain_constraints = [pop_constraint]

    def count_municipal_splits(partition) -> int:
        """Count multi-VA municipalities split across >= 2 unfrozen districts."""
        csd_to_districts = {}
        for node, dist in partition.assignment.items():
            csd = sub.nodes[node]["csd"]
            if csd in multi_va_csds:
                csd_to_districts.setdefault(csd, set()).add(dist)
        return sum(1 for s in csd_to_districts.values() if len(s) >= 2)

    if args.max_splits is not None:
        chain_constraints.append(lambda p: count_municipal_splits(p) <= args.max_splits)
        print(f"[constraint] Hard municipal-split cap: {args.max_splits}", flush=True)

    import random
    random.seed(seed)
    np.random.seed(seed & 0x7FFFFFFF)

    chain = MarkovChain(
        proposal=proposal,
        constraints=chain_constraints,
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=args.steps,
    )

    # ── Run + collect ──────────────────────────────────────────────────────────
    frozen_ucp = frozen_stats["ucp"].values
    frozen_ndp = frozen_stats["ndp"].values

    print(f"[chain] Running {args.steps:,} steps at FULL epsilon={args.pop_deviation} ...", flush=True)
    rows = []
    t1 = time.time()
    for i, part in enumerate(chain):
        ucp_arr = np.array(list(part["ucp"].values()))
        ndp_arr = np.array(list(part["ndp"].values()))
        # Reattach frozen districts as constants → complete 89-district plan
        full_ucp = np.concatenate([ucp_arr, frozen_ucp])
        full_ndp = np.concatenate([ndp_arr, frozen_ndp])
        m = seat_results(full_ucp, full_ndp)
        m["step"] = i
        m["municipal_splits"] = count_municipal_splits(part)
        rows.append(m)
        if (i + 1) % 5000 == 0:
            el = time.time() - t1
            rate = (i + 1) / el
            eta = (args.steps - i - 1) / rate
            print(f"  step {i+1:,}/{args.steps:,}  ({rate:.0f}/s, ETA {eta/60:.1f} min)", flush=True)

    df = pd.DataFrame(rows)
    prefix = args.out_prefix or f"constraint_enforcing_{args.steps//1000}k"
    out_csv = OUT_DIR / f"{prefix}_samples.csv"
    df.to_csv(out_csv, index=False, float_format="%.17g")
    print(f"[out] {out_csv} ({len(df):,} rows)", flush=True)

    # ── Score real maps against this constrained ensemble ────────────────────
    print(f"[score] Scoring real maps ...", flush=True)
    real = {}
    for plan in ("majority", "minority"):
        m = score_exogenous_map(va, canonical_shapefile(plan), id_col=ED_NAME_COL)
        real[plan] = m

    def pct(arr, x):
        return float(100.0 * ((arr < x).sum() + 0.5 * (np.abs(arr - x) < 1e-12).sum()) / len(arr))

    summary = {
        "test": "Constraint-enforcing ReCom ensemble (T1.4 partial + T1.11)",
        "adaptations": [
            f"FULL epsilon = {args.pop_deviation} in proposal (canonical run used epsilon/2 = ±12.5%)",
            f"s.15(2) freeze-from-real-seed: {sorted(frozen_eds)} held at commission boundaries",
            "municipal-split count tallied per plan (not constrained)" if args.max_splits is None
            else f"municipal-split count hard-capped at {args.max_splits}",
        ],
        "seed_map": args.seed_map,
        "n_steps": args.steps,
        "seed": seed,
        "salt": args.seed_salt,
        "frozen_districts": {k: float(v) for k, v in s15_2.items()},
        "ensemble_stats": {
            c: {"mean": float(df[c].mean()), "p5": float(np.percentile(df[c], 5)),
                "p95": float(np.percentile(df[c], 95))}
            for c in ("efficiency_gap", "mean_median", "declination", "seats_at_50_50", "municipal_splits")
        },
        "real_map_percentiles": {
            plan: {
                c: {"value": float(real[plan][c]), "percentile": pct(df[c].values, real[plan][c])}
                for c in ("efficiency_gap", "mean_median", "declination", "seats_at_50_50")
            }
            for plan in ("majority", "minority")
        },
        "wall_clock_seconds": time.time() - t0,
    }
    out_json = OUT_DIR / f"{prefix}_summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[out] {out_json}", flush=True)

    print("\n=== Real-map percentiles vs CONSTRAINED ensemble ===", flush=True)
    for plan in ("majority", "minority"):
        for c in ("efficiency_gap", "mean_median", "declination", "seats_at_50_50"):
            v = summary["real_map_percentiles"][plan][c]
            print(f"  {plan:9s} {c:16s} {v['value']:+.4f}  p{v['percentile']:.2f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
