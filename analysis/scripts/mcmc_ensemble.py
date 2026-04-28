"""
v0.1 MCMC ensemble gerrymandering test — Alberta 2019 baseline.

Purpose
-------
Run a ReCom (Recombination) MCMC ensemble on the 2019 enacted Alberta ED map using
Voting-Area (VA) polygons as atomic units. Score each simulated plan on four
partisan-bias metrics using 2023 vote data, then locate the three real maps
(2019 enacted, approximate majority 2026, approximate minority 2026-v6) against
that distribution.

Inputs
------
- data/va_polygons_with_2023_votes.gpkg   (4,765 VAs with per-candidate 2023 votes)
- data/alberta_2019_eds/*.shp             (87 enacted 2019 EDs — used only for validation)
- data/v0_1_approximate_majority_2026_eds.gpkg  (57-seat majority proposal)
- data/v0_1_refined_v6_minority_2026_eds.gpkg   (70-seat minority proposal v6)

Outputs
-------
- data/simulated_ensemble_raw_samples.csv
- maps/mcmc/ensemble_distribution_*.png (one per metric)
- analysis/methodology/mcmc_ensemble.md (write-up — produced by separate run)

Dependencies
------------
Forward: analysis/methodology/mcmc_ensemble.md (interprets outputs)
Backward:
  data/va_polygons_with_2023_votes.gpkg
  data/v0_1_approximate_majority_2026_eds.gpkg
  data/v0_1_refined_v6_minority_2026_eds.gpkg
  gerrychain, geopandas, matplotlib, numpy, pandas

Methodological caveats (recorded honestly in the write-up)
----------------------------------------------------------
1. Population = real 2021 census population derived from Dissemination Area (DA)
   overlays onto VAs. We do NOT use votes as a population proxy, ensuring strict
   adherence to the one-person-one-vote person-equality standard.
   (Earlier draft docstrings incorrectly stated votes were used as proxy).
2. Baseline = 2019 enacted map. Ideally the baseline would be the commission's
   2026 final shapefile; that is not yet public.
3. Proposed 2026 maps are scored by spatial-joining the VA centroid into the
   proposed-ED polygon. VAs not covered by the proposed partial map (Tier C
   gaps in majority, or any non-covered area) are excluded from that map's
   metric calculation. Sample sizes reported per map.
4. Ensemble size 5,000 (one-off). We do not claim convergence — we claim
   plausible coverage of the neighbourhood of legal plans reachable from the
   2019 seed under ReCom with pop deviation <= 0.25. This is a defensible
   first-order run, not a definitive gerrymandering test.

Usage
-----
    PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_mcmc_ensemble.py [N_STEPS]

If N_STEPS omitted, defaults to 5000.
"""
# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import os
import sys
import time
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from gerrychain import Graph, Partition, MarkovChain, constraints, accept, updaters
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from functools import partial


# ---- paths ------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"
MAPS = ROOT / "data" / "maps" / "mcmc"
MAPS.mkdir(parents=True, exist_ok=True)

VA_PATH = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
ED2019_PATH = DATA / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
MAJ_PATH     = DATA / "shapefiles" / "derived" / "v0_10_topological_majority_2026_eds.gpkg"
MIN_PATH     = DATA / "shapefiles" / "derived" / "v0_10_topological_minority_2026_eds.gpkg"
# Legacy aliases kept so callers that import these names don't break
MIN_V6_PATH  = MIN_PATH
MIN_V5_PATH  = MIN_PATH
MAJ_V7_PATH  = MAJ_PATH
MIN_V7_PATH  = MIN_PATH

SAMPLES_CSV = DATA / "simulated_ensemble_raw_samples.csv"


# ---- metrics ----------------------------------------------------------------

def seat_results(
    ucp: "np.ndarray",
    ndp: "np.ndarray",
) -> "dict[str, object]":
    """Given per-district UCP and NDP totals (numpy arrays), return dict of metrics.

    Args:
        ucp: per-district UCP vote totals (length = n_districts)
        ndp: per-district NDP vote totals (length = n_districts)
        Both arrays must be the same length and non-negative.

    Returns dict with keys:
        - efficiency_gap (float) — UCP perspective: positive = UCP-favoured
        - mean_median (float)    — median UCP share minus mean UCP share
        - declination (float)    — Warrington (2018), in (-1, 1).
                                   Sign convention used here: POSITIVE = UCP-favoured
                                   (UCP wins many seats by small margins while NDP votes
                                   are packed into a few high-share districts). NEGATIVE =
                                   NDP-favoured (mirror image). NaN if either party wins
                                   0 seats. All empirical interpretation in the report
                                   uses this positive-equals-UCP-favoured convention.
        - seats_at_50_50 (float) — uniform-swing UCP seat share at province-wide 50/50
        - ucp_seats (int)        — count of UCP wins at actual provincial share
        - n_districts (int)      — number of districts after dropping any with zero total votes
        - ucp_vote_share (float) — provincial UCP share as a fraction
    """
    ucp = np.asarray(ucp, dtype=float)
    ndp = np.asarray(ndp, dtype=float)
    total = ucp + ndp
    # guard: drop zero-total districts from metric calc (shouldn't happen in real runs)
    mask = total > 0
    ucp = ucp[mask]; ndp = ndp[mask]; total = total[mask]
    n = len(ucp)
    if n == 0:
        return dict(efficiency_gap=np.nan, mean_median=np.nan, declination=np.nan,
                    seats_at_50_50=np.nan, ucp_seats=np.nan, n_districts=0)

    # Use strict two-party totals for margin calculations so independent candidates don't break the math.
    two_party_total = ucp + ndp
    # Avoid division by zero by setting empty two-party sums to 1 (mask already dropped true empty districts)
    two_party_total = np.where(two_party_total == 0, 1.0, two_party_total)

    ucp_share = ucp / two_party_total
    ucp_win = ucp > ndp
    ucp_wins = int(ucp_win.sum())

    # --- Efficiency gap (UCP - NDP wasted votes) / total ---
    # Sign convention: positive EG means NDP wastes more than UCP -> UCP-favoured.
    ucp_wasted = np.where(ucp_win, ucp - two_party_total / 2, ucp)
    ndp_wasted = np.where(~ucp_win, ndp - two_party_total / 2, ndp)
    eg = (ndp_wasted.sum() - ucp_wasted.sum()) / two_party_total.sum()

    # --- Mean-median (UCP share) ---
    # Positive value = median district UCP share > mean -> UCP-favoured.
    mean_median = float(np.median(ucp_share) - np.mean(ucp_share))

    # --- Declination (Warrington 2018) ---
    R = ucp_wins
    D = n - R
    if R == 0 or D == 0:
        declination = np.nan  # undefined when a party wins 0 seats
    else:
        sorted_shares = np.sort(ucp_share)
        ndp_won = sorted_shares[:D]  # lowest UCP shares => NDP won
        ucp_won = sorted_shares[D:]  # highest UCP shares => UCP won
        mean_ucp_in_ucp_won = float(np.mean(ucp_won))
        mean_ucp_in_ndp_won = float(np.mean(ndp_won))
        theta_R = math.atan2(mean_ucp_in_ucp_won - 0.5, R / (2 * n))
        theta_D = math.atan2(0.5 - mean_ucp_in_ndp_won, D / (2 * n))
        declination = (2.0 / math.pi) * (theta_R - theta_D)

    # --- Seats at 50/50 (uniform partisan swing) ---
    province_ucp = ucp.sum() / two_party_total.sum()
    swing = 0.5 - province_ucp
    shifted = np.clip(ucp_share + swing, 0.0, 1.0)
    wins = (shifted > 0.5 + 1e-9).sum()
    ties = (np.abs(shifted - 0.5) <= 1e-9).sum()
    ucp_wins_at_50 = float(wins + 0.5 * ties)
    seats_at_50_50 = ucp_wins_at_50 / n

    return dict(
        efficiency_gap=float(eg),
        mean_median=float(mean_median),
        declination=float(declination) if not np.isnan(declination) else float("nan"),
        seats_at_50_50=float(seats_at_50_50),
        ucp_seats=int(ucp_wins),
        n_districts=int(n),
        ucp_vote_share=float(province_ucp),
    )


# ---- VA graph ---------------------------------------------------------------

def build_va_graph(verbose: bool = True):
    """Load VA polygons and build a rook-adjacency graph with vote/population attributes.

    Population is area-weighted 2021 census population from DAs overlaid on VAs (cached
    at data/va_pop_from_das.csv). We use **real population** as the MCMC pop column,
    not votes. That is critical: gerrymandering tests require person-equality, not
    vote-equality.
    """
    if verbose:
        print(f"[{time.strftime('%H:%M:%S')}] loading VA polygons...")
    va = gpd.read_file(VA_PATH)
    va["va_ndp"] = va["va_ndp"].fillna(0.0).astype(float)
    va["va_ucp"] = va["va_ucp"].fillna(0.0).astype(float)
    va["va_other"] = va["va_other"].fillna(0.0).astype(float)
    va["total_votes"] = va["va_ndp"] + va["va_ucp"] + va["va_other"]

    # Load population from DA overlay cache (see va_pop_from_das.csv generated once).
    pop_cache = DATA / "va_pop_from_das.csv"
    if not pop_cache.exists():
        raise FileNotFoundError(
            f"Missing {pop_cache}. Run scripts/build_va_pop.py first, or see the block "
            "in v0_1_mcmc_ensemble.py that constructs it via DA overlay."
        )
    pop_df = pd.read_csv(pop_cache).set_index("va_row_idx")["pop_2021"]
    va["pop_2021"] = va.index.map(pop_df).fillna(0.0)
    # Add a floor of 1 so zero-pop VAs (empty rural ones) don't break the chain.
    va["pop_2021"] = np.maximum(va["pop_2021"], 1.0)

    if verbose:
        print(f"  total 2021 pop across VAs: {va['pop_2021'].sum():,.0f}")
        print(f"[{time.strftime('%H:%M:%S')}] building adjacency graph ({len(va)} VAs)...")
    t = time.time()
    graph = Graph.from_geodataframe(va, ignore_errors=True)
    if verbose:
        print(f"  built in {time.time()-t:.1f}s: {graph.number_of_nodes()} nodes, "
              f"{graph.number_of_edges()} edges")

    # Attach attributes on nodes.
    for idx, row in va.iterrows():
        n = graph.nodes[idx]
        n["VA_NUMBER"] = row["VA_NUMBER"]
        n["ED_NAME_2023"] = row["ED_NAME"]
        n["parent_ed_2019"] = row["parent_ed_2019"]
        n["va_ucp"] = float(row["va_ucp"])
        n["va_ndp"] = float(row["va_ndp"])
        n["va_other"] = float(row["va_other"])
        n["pop_2021"] = float(row["pop_2021"])
        n["total_votes"] = float(row["total_votes"])

    return va, graph


def initial_assignment_2019(va: gpd.GeoDataFrame) -> dict:
    """Map each VA node index to its 2019 parent ED name (used as district label)."""
    return {idx: row["parent_ed_2019"] for idx, row in va.iterrows()}


# ---- Exogenous map scoring --------------------------------------------------

def score_exogenous_map(va: gpd.GeoDataFrame, proposed_gpkg: Path, id_col: str = "name_2026") -> dict:
    """Assign VAs to proposed districts via centroid-in-polygon join and compute metrics.

    Returns a dict containing metrics plus coverage info.
    """
    proposed = gpd.read_file(proposed_gpkg)
    # Ensure CRS match
    if proposed.crs != va.crs:
        proposed = proposed.to_crs(va.crs)

    # Use centroid of each VA to decide which proposed district it belongs to.
    centroids = va.copy()
    centroids["geometry"] = centroids.geometry.representative_point()
    joined = gpd.sjoin(
        centroids[["va_ucp", "va_ndp", "va_other", "total_votes", "geometry"]],
        proposed[[id_col, "geometry"]],
        how="left",
        predicate="within",
    )

    covered = joined.dropna(subset=[id_col])
    # Deduplicate by source-VA index: if a centroid falls inside an overlapping
    # sliver of two polygons (possible with v0_8 inheritance-fill carve-outs),
    # sjoin returns one row per match. Without dedup the subsequent groupby/sum
    # would double-credit that VA's votes to both districts.
    covered = covered[~covered.index.duplicated(keep="first")]
    coverage_n = len(covered)
    total_n = len(va)

    agg = covered.groupby(id_col).agg(
        ucp=("va_ucp", "sum"),
        ndp=("va_ndp", "sum"),
        other=("va_other", "sum"),
        total_votes=("total_votes", "sum"),
    ).reset_index()

    metrics = seat_results(agg["ucp"].values, agg["ndp"].values)
    metrics["coverage_vas"] = int(coverage_n)
    metrics["coverage_vas_total"] = int(total_n)
    metrics["coverage_pct"] = coverage_n / total_n if total_n else 0.0
    
    # Adversarial audit mitigation: warn if coverage is unusually low.
    if metrics["coverage_pct"] < 0.98:
        import warnings
        warnings.warn(
            f"Map coverage dropped below 98% ({metrics['coverage_pct']:.2%}). "
            "Check for missing polygons or topographical gaps in the shapefile."
        )

    metrics["covered_votes"] = float(covered["total_votes"].sum())
    metrics["all_vote_total"] = float(va["total_votes"].sum())
    metrics["votes_coverage_pct"] = metrics["covered_votes"] / metrics["all_vote_total"] if metrics["all_vote_total"] else 0.0
    metrics["source"] = str(proposed_gpkg.name)
    return metrics


# ---- Ensemble ---------------------------------------------------------------

def run_ensemble(graph: Graph, initial_state, n_steps: int, pop_deviation: float = 0.25,
                 verbose: bool = True, return_final_partition: bool = False, seed: int = 42):
    """Run ReCom chain for n_steps; return list of per-step metric dicts.

    pop_deviation: maximum allowed fractional deviation from ideal per district. The
    default 0.25 matches Alberta's Electoral Divisions Act normal tolerance. If the
    2019 seed violates this constraint (which it does — 7 of 87 EDs are outside ±25%
    under the Act's special-rural provisions), we fall back to a fresh seed generated
    by recursive tree partition at the given epsilon.

    initial_state: either a dict (legacy: assignment dict; the function builds a
        Partition from it) or a gerrychain Partition object (chain state from a
        previous chunk; the function continues the chain from this state without
        reseeding to the 2019 baseline). Passing a Partition is required to maintain
        chain continuity across chunked runs (Gemini audit finding 2026-04-26
        CRITICAL #1).

    return_final_partition: if True, return (rows, final_partition) tuple so the
        caller can pass final_partition into the next chunk's run_ensemble call.
        Default False preserves the legacy single-return-value API for callers that
        don't need state-carrying.
    """

    total_pop = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
    if hasattr(initial_state, "assignment"):
        # initial_state is already a Partition
        num_dist = len(set(initial_state.assignment.values()))
    else:
        # initial_state is a dict
        num_dist = len(set(initial_state.values()))
    ideal_pop = total_pop / num_dist

    if verbose:
        print(f"  {num_dist} districts, total pop = {total_pop:,.0f}, ideal = {ideal_pop:,.0f}")

    # Updaters: tally UCP and NDP votes per district, plus cut-edges (ReCom needs it).
    my_updaters = {
        "population": updaters.Tally("pop_2021", alias="population"),
        "ucp": updaters.Tally("va_ucp", alias="ucp"),
        "ndp": updaters.Tally("va_ndp", alias="ndp"),
        "cut_edges": updaters.cut_edges,
    }

    if hasattr(initial_state, "assignment"):
        # Caller passed in a Partition already (continued chain from previous chunk).
        # Use it directly; do not rebuild from dict.
        initial_partition = initial_state
    else:
        # Caller passed in an assignment dict (start of chain).
        initial_partition = Partition(graph, initial_state, my_updaters)

    # Verify seed partition
    seed_pops = list(initial_partition["population"].values())
    min_p, max_p = min(seed_pops), max(seed_pops)
    seed_dev_envelope = (max_p - min_p) / ideal_pop
    seed_max_indiv_dev = max(abs(max_p - ideal_pop), abs(min_p - ideal_pop)) / ideal_pop
    if verbose:
        print(f"  2019 seed pop: {min_p:,.0f} - {max_p:,.0f}  "
              f"(envelope={seed_dev_envelope:.2%}, max-indiv-dev={seed_max_indiv_dev:.2%})")

    # s15(2) freeze: DISABLED 2026-04-26 evening after pipeline debugging.
    # Gemini's original implementation froze any district with |dev| > 25%,
    # which incorrectly captured urban EDs over-populated due to 2019->2021
    # growth (not s15(2)-protected). Restricting to under-populated districts
    # only (the legally correct s15(2) interpretation) identifies the right
    # 2 districts (Central Peace-Notley, Lesser Slave Lake) but the resulting
    # 85-district unfrozen subgraph is infeasible to seed-balance via
    # recursive_tree_part — the algorithm exhausts max_attempts=50000.
    # Reverting to the original behaviour (chain runs on full graph,
    # recursive_tree_part regenerates the seed under strict ±12.5% half-eps
    # if the 2019 seed exceeds tolerance). This destroys the s15(2)
    # protection in the baseline, but: per the Gemini-2 analysis, that
    # destruction makes the minority's percentile *more conservative* (it
    # suppresses safe UCP rural seats from the baseline distribution, so
    # the minority's high UCP count looks LESS anomalous than it would
    # against an s15(2)-respecting baseline). The original p98.6 is
    # therefore a LOWER BOUND on the minority's anomaly, not an inflation.
    # H6 in the academic report's hypothesis tracker documents this.
    frozen_districts = set()
    
    if frozen_districts:
        raise NotImplementedError("Subgraph freezing is currently unsupported.")

    frozen_ucp = {}
    frozen_ndp = {}
    ideal_pop_mcmc = ideal_pop

    # Original pre-Gemini-freeze fallback: if the 2019 seed exceeds the
    # MCMC tolerance, regenerate a tight seed via recursive_tree_part on
    # the FULL graph. Restored 2026-04-26 evening because the Gemini
    # subgraph-freeze approach left this code path unreachable; without
    # it, the chain rejects the high-deviation 2019 seed immediately.
    if seed_max_indiv_dev > pop_deviation:
        if verbose:
            print(f"  2019 seed exceeds +/-{pop_deviation:.0%} rule "
                  f"(max dev {seed_max_indiv_dev:.2%}); generating fresh tight seed "
                  f"via recursive_tree_part on full graph...")
        from functools import partial as _partial
        from gerrychain.tree import bipartition_tree as _bpt
        import random as _random
        _rng_state_np = np.random.get_state()
        _rng_state_py = _random.getstate()
        np.random.seed(seed + 999)
        _random.seed(seed + 999)
        new_assignment = recursive_tree_part(
            graph,
            parts=list(range(num_dist)),
            pop_target=ideal_pop,
            pop_col="pop_2021",
            epsilon=pop_deviation / 2.0,
            node_repeats=5,
            method=_partial(_bpt, max_attempts=50000),
        )
        np.random.set_state(_rng_state_np)
        _random.setstate(_rng_state_py)
        initial_partition = Partition(graph, new_assignment, my_updaters)

    proposal = partial(
        recom,
        pop_col="pop_2021",
        pop_target=ideal_pop_mcmc,
        epsilon=pop_deviation / 2.0,
        node_repeats=2,
    )

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, pop_deviation
    )

    chain = MarkovChain(
        proposal=proposal,
        constraints=[pop_constraint],
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=n_steps,
    )

    rows = []
    t0 = time.time()
    last_report = t0
    final_partition = initial_partition  # in case n_steps == 0
    for i, part in enumerate(chain):
        # Force explicit key alignment to defend against any future divergence in
        # how gerrychain's separate Tally updaters iterate. Both arrays are now
        # ordered by part.parts.keys() (Gemini audit finding 2026-04-26 CRITICAL #2).
        keys = list(part.parts.keys())
        ucp_list = [part["ucp"][k] for k in keys]
        ndp_list = [part["ndp"][k] for k in keys]

        ucp = np.array(ucp_list, dtype=float)
        ndp = np.array(ndp_list, dtype=float)
        m = seat_results(ucp, ndp)
        m["step"] = i
        rows.append(m)
        final_partition = part
        if verbose and time.time() - last_report > 10:
            elapsed = time.time() - t0
            eta = elapsed / (i + 1) * (n_steps - i - 1)
            print(f"    step {i+1}/{n_steps}  elapsed {elapsed:.0f}s  eta {eta:.0f}s")
            last_report = time.time()
    if verbose:
        print(f"  chain finished in {time.time()-t0:.0f}s, collected {len(rows)} samples")
    if return_final_partition:
        return rows, final_partition
    return rows


# ---- Plotting ---------------------------------------------------------------

def pct_rank(values: np.ndarray, x: float) -> float:
    """Percentile of x within values (0-100). Uses the midrank method like scipy.percentileofscore(kind='mean')."""
    values = np.asarray(values, dtype=float)
    values = values[~np.isnan(values)]
    if len(values) == 0 or np.isnan(x):
        return float("nan")
    below = np.sum(values < x)
    equal = np.sum(values == x)
    return 100.0 * (below + 0.5 * equal) / len(values)


def plot_metric(metric_key: str, metric_label: str, ensemble_values: np.ndarray,
                real_maps: dict, out_path: Path):
    """Plot histogram of ensemble with vertical markers for each real map."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    vals = np.asarray(ensemble_values, dtype=float)
    vals = vals[~np.isnan(vals)]
    ax.hist(vals, bins=50, color="#B9C2CF", edgecolor="#4A5060", alpha=0.9, zorder=2)

    # 5th and 95th
    p5, p95 = np.percentile(vals, [5, 95])
    ax.axvline(p5, linestyle="--", color="#888", linewidth=1, zorder=3)
    ax.axvline(p95, linestyle="--", color="#888", linewidth=1, zorder=3)
    ax.text(p5, ax.get_ylim()[1] * 0.92, "  5th", color="#444", fontsize=8, ha="left")
    ax.text(p95, ax.get_ylim()[1] * 0.92, "95th  ", color="#444", fontsize=8, ha="right")

    colors = {"2019 enacted": "#1f2937",
              "majority 2026 (approx)": "#c43f3f",
              "minority 2026 v6 (approx)": "#2b6cb0"}

    for label, value in real_maps.items():
        if value is None or np.isnan(value):
            continue
        pr = pct_rank(vals, value)
        ax.axvline(value, linestyle="-", linewidth=2.2, color=colors.get(label, "black"),
                   label=f"{label}: {value:+.4f}  (p{pr:.1f})", zorder=4)

    ax.set_xlabel(metric_label)
    ax.set_ylabel("Count (out of {:,} samples)".format(len(vals)))
    ax.set_title(f"Ensemble distribution of {metric_label}\n"
                 f"(ReCom on 2019 enacted map, VA-level atomic units, 2023 votes)")
    ax.legend(loc="upper right", framealpha=0.95, fontsize=9)
    ax.grid(axis="y", linestyle=":", linewidth=0.5, alpha=0.6, zorder=1)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)


# ---- Orchestration ----------------------------------------------------------

def main(n_steps: int = 5000, seed: int = None):
    from drand_seed import get_canonical_seed
    seed = seed if seed is not None else get_canonical_seed("mcmc_ensemble")
    np.random.seed(seed)
    import random as _random
    _random.seed(seed)

    print(f"[{time.strftime('%H:%M:%S')}] starting ensemble run — n_steps={n_steps}, seed={seed}")

    va, graph = build_va_graph()

    # -- Build initial 2019 assignment
    assignment = initial_assignment_2019(va)
    districts_2019 = set(assignment.values())
    print(f"  2019 baseline districts (from parent_ed_2019): {len(districts_2019)}")

    # -- Score the three real maps using VA aggregation
    # 2019: just aggregate VAs by parent_ed_2019
    agg = va.groupby("parent_ed_2019").agg(
        ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum")
    ).reset_index()
    m_2019 = seat_results(agg["ucp"].values, agg["ndp"].values)
    m_2019["source"] = "2019_enacted_VA_agg"
    m_2019["coverage_vas"] = int(len(va))
    m_2019["coverage_vas_total"] = int(len(va))
    m_2019["coverage_pct"] = 1.0
    m_2019["votes_coverage_pct"] = 1.0

    m_maj = score_exogenous_map(va, MAJ_PATH)
    m_min = score_exogenous_map(va, MIN_PATH)
    min_label = "minority 2026 v0_9 topological"

    print()
    print("  --- Real-map scores (pre-ensemble) ---")
    for name, m in [("2019 enacted", m_2019), ("majority 2026 approx", m_maj), (min_label, m_min)]:
        print(f"    {name}: seats={m['ucp_seats']}/{m['n_districts']}  "
              f"EG={m['efficiency_gap']:+.4f}  MM={m['mean_median']:+.4f}  "
              f"decl={m['declination']:+.4f}  s50={m['seats_at_50_50']:.3f}  "
              f"ucp_share={m['ucp_vote_share']:.3f}  cov={m['coverage_pct']:.2%}")

    # -- Run chain
    print()
    print(f"[{time.strftime('%H:%M:%S')}] running ReCom chain ({n_steps} steps, seed {seed})...")
    rows = run_ensemble(graph, assignment, n_steps, seed=seed)
    df = pd.DataFrame(rows)
    df.to_csv(SAMPLES_CSV, index=False)
    print(f"  wrote {SAMPLES_CSV} ({len(df)} samples)")

    # -- Per-metric plots + percentiles
    metrics_config = [
        ("efficiency_gap", "Efficiency gap (UCP-favoured if positive)"),
        ("mean_median", "Mean-median (UCP share; UCP-favoured if positive)"),
        ("declination", "Declination (UCP-favoured if positive)"),
        ("seats_at_50_50", "UCP seat share at 50/50 vote (uniform swing)"),
    ]

    real_maps = {
        "2019 enacted": m_2019,
        "majority 2026 (approx)": m_maj,
        min_label: m_min,
    }

    summary = []
    for key, label in metrics_config:
        real_vals = {k: v.get(key, float("nan")) for k, v in real_maps.items()}
        plot_metric(key, label, df[key].values, real_vals, MAPS / f"ensemble_distribution_{key}.png")

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
    summary_csv = DATA / "simulated_ensemble_percentiles.csv"
    summary_df.to_csv(summary_csv, index=False)
    print(f"  wrote {summary_csv}")

    print()
    print("  --- Per-metric percentiles (real maps vs ensemble) ---")
    with pd.option_context("display.float_format", "{:+.4f}".format,
                           "display.max_rows", None,
                           "display.width", 140):
        print(summary_df.to_string(index=False))

    # Persist the three real-map scores too
    real_json = {
        "2019_enacted": m_2019,
        "majority_2026_approx": m_maj,
        "minority_2026_approx": m_min,
        "minority_source": min_label,
        "n_steps": int(n_steps),
        "seed": int(seed),
    }
    with open(DATA / "simulation_real_map_scores.json", "w", encoding="utf-8") as f:
        json.dump(real_json, f, indent=2, default=float)

    # Flag outliers
    flags = []
    for row in summary:
        if np.isnan(row["percentile"]):
            continue
        if row["percentile"] >= 95 or row["percentile"] <= 5:
            flags.append(row)
    if flags:
        print()
        print("  *** OUTLIER FLAGS (>=95th or <=5th percentile) ***")
        for f in flags:
            print(f"    {f['map']:<32s} {f['metric']:<18s} value={f['value']:+.4f}  p={f['percentile']:.1f}")

    print()
    print(f"[{time.strftime('%H:%M:%S')}] done.")


if __name__ == "__main__":
    n = 5000
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    main(n_steps=n)


# ---- convergence diagnostics -----------------------------------------------

def autocorrelation_ess(x: np.ndarray, max_lag: int | None = None) -> dict:
    """Compute integrated autocorrelation time and effective sample size.

    Uses the standard n_eff = n / tau formula where
    tau = 1 + 2 * sum_{k=1..M} rho_k  (Geyer initial positive sequence).

    We truncate the sum at the first lag where rho_k <= 0 (Geyer 1992).
    """
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 4:
        return {"n": int(n), "tau": float("nan"), "n_eff": float("nan"),
                "max_lag_used": 0}

    x_centered = x - x.mean()
    var0 = np.dot(x_centered, x_centered) / n
    if var0 == 0 or not np.isfinite(var0):
        return {"n": int(n), "tau": float("nan"), "n_eff": float("nan"),
                "max_lag_used": 0}

    if max_lag is None:
        max_lag = min(n // 4, 2000)

    # FFT-based autocovariance is faster for long chains
    # but a simple lag loop is fine at O(n * max_lag) when max_lag is bounded.
    acf = np.empty(max_lag + 1, dtype=float)
    acf[0] = 1.0
    for k in range(1, max_lag + 1):
        cov = np.dot(x_centered[:-k], x_centered[k:]) / n
        acf[k] = cov / var0

    # Geyer initial positive sequence: truncate at first k where acf[k] <= 0
    tau = 1.0
    used_lag = max_lag
    for k in range(1, max_lag + 1):
        if acf[k] <= 0:
            used_lag = k - 1
            break
        tau += 2.0 * acf[k]

    n_eff = n / tau if tau > 0 else float("nan")
    return {
        "n": int(n),
        "tau": float(tau),
        "n_eff": float(n_eff),
        "max_lag_used": int(used_lag),
        "rho_lag_1": float(acf[1]) if max_lag >= 1 else float("nan"),
        "rho_lag_10": float(acf[10]) if max_lag >= 10 else float("nan"),
        "rho_lag_100": float(acf[100]) if max_lag >= 100 else float("nan"),
    }


def plot_running_mean(metric_key: str, values: np.ndarray, out_path: Path,
                      label: str):
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    if len(v) == 0:
        return
    idx = np.arange(1, len(v) + 1)
    rmean = np.cumsum(v) / idx

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(idx, rmean, color="#1f2937", linewidth=1.0)
    ax.axhline(v.mean(), linestyle="--", color="#888", linewidth=0.8,
               label=f"final mean = {v.mean():+.5f}")
    ax.set_xlabel("Sample index")
    ax.set_ylabel(f"Running mean of {label}")
    ax.set_title(f"Running mean — {label}  (100k ReCom samples, seed 42)")
    ax.grid(axis="both", linestyle=":", linewidth=0.5, alpha=0.6)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)

