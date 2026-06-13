# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
szat.py — Swing-Zone Allocation Test

Lane 1 (Statistical), Channel 2 (standalone): Swing-Zone Allocation Test
Precursor: phase4c_canonical_attribution uses the same VA representative_point assignment method
Feeds: joint_outlier_score_canonical (Channel 2 p-value input for Fisher combination)

Decomposes the efficiency-gap difference between the minority and majority
2026 Alberta Electoral Boundary Commission maps into the specific boundary
choices (swing zones) that drive it.

A swing zone is a Voting Area whose centroid falls in a different ED under
the minority map than under the majority map. Only the 2026 canonical
Elections Alberta shapefiles are used; all DPG-derived shapefiles are
deprecated as of 2026-05-06.

Methodology: analysis/methodology/szat_proposal.md

Inputs
------
data/shapefiles/canonical/ea_majority_2026_eds.gpkg
data/shapefiles/canonical/ea_minority_2026_eds.gpkg
data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg

Outputs
-------
findings/szat_results.csv      — per-VA swing-zone table
findings/szat_summary.json     — map-level summary + bootstrap

EG sign convention (McGhee / Stephanopoulos 2014, U. Chi. L. Rev. 82(2)):
  positive EG = more NDP votes wasted than UCP (UCP structural advantage)
  negative EG = more UCP votes wasted than NDP (NDP structural advantage)
  SZAT_score = EG_minority − EG_majority
    positive SZAT = minority map's swing-zone choices worsen NDP efficiency
    negative SZAT = minority map's swing-zone choices improve NDP efficiency

Bootstrap seed: get_canonical_seed("szat-bootstrap") from drand_seed.py.
Fallback seed 20260506 used if drand_seed is unavailable.

Backward:
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/canonical/ea_minority_2026_eds.gpkg
  data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg
  analysis/scripts/drand_seed.py

Forward:
  findings/szat_results.csv
  findings/szat_summary.json
"""
from __future__ import annotations


import argparse
import json
import sys
import time
import warnings
from pathlib import Path

try:
    import data_loader
    from canonical_manifest import verify_canonical_files
    from eg_utils import compute_eg, InsufficientDataError
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader
    from canonical_manifest import verify_canonical_files
    from eg_utils import compute_eg, InsufficientDataError

try:
    from audit_logger import log_run as _log_run
except ImportError:
    def _log_run(*args, **kwargs): pass  # no-op fallback

import geopandas as gpd
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
try:
    from analysis.utils.data_loader import FINDINGS as REPORTS
except ImportError:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'utils'))
    from data_loader import FINDINGS as REPORTS
REPORTS.mkdir(parents=True, exist_ok=True)

VA_FILE = DATA / "shapefiles" / "derived" / "va_polygons_with_full_2023_votes.gpkg"
MAJ_FILE = DATA / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg"
MIN_FILE = DATA / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"

N_BOOT = 10_000

# EDs whose swing-zone contributions are reported individually in the summary
# because they motivated this test (population_deviation_reaudit.md §1.3).
FOCAL_EDS = {
    "Canmore-Banff",
    "Canmore-Kananaskis",
    "Rocky Mountain House-Banff Park",
}


# ── Region classifier ──────────────────────────────────────────────────────────


def _region(ed_name: str) -> str:
    if ed_name.startswith(("Calgary-", "Calgary–")):
        return "Calgary"
    if ed_name.startswith(("Edmonton-", "Edmonton–")):
        return "Edmonton"
    if ed_name in {
        "Canmore-Banff",
        "Canmore-Kananaskis",
        "Rocky Mountain House-Banff Park",
        "Lacombe-Clearwater",
        "Rimbey-Rocky Mountain House-Sundre",
        "Banff-Kananaskis",
    }:
        return "Mountain-West"
    return "Rest of Alberta"


def va_eg_contribution(
    va_ndp: float,
    va_ucp: float,
    ed_ndp: float,
    ed_ucp: float,
    total_prov: float,
) -> float:
    """
    Proportional EG contribution of a single VA to its assigned ED.

    Winner's wasted votes are allocated proportionally across VAs in that
    ED (each VA contributed va_winner / ed_winner fraction of the winners'
    total); all loser votes in the VA are fully wasted.
    """
    if total_prov == 0 or (ed_ndp + ed_ucp) == 0:
        return 0.0

    ed_total = ed_ndp + ed_ucp
    threshold = ed_total / 2

    if ed_ndp >= ed_ucp:  # NDP wins this ED
        w_ndp = (va_ndp / ed_ndp) * max(0.0, ed_ndp - threshold) if ed_ndp > 0 else 0.0
        w_ucp = va_ucp
    else:  # UCP wins this ED
        w_ucp = (va_ucp / ed_ucp) * max(0.0, ed_ucp - threshold) if ed_ucp > 0 else 0.0
        w_ndp = va_ndp

    return (w_ndp - w_ucp) / total_prov


# ── Spatial join ───────────────────────────────────────────────────────────────


def _assign(va_gdf: gpd.GeoDataFrame, ed_gdf: gpd.GeoDataFrame) -> pd.Series:
    """
    Centroid-in-polygon assignment of VAs to EDs.
    Falls back to nearest-ED for centroids that fall outside all EDs
    (topology gaps, boundary slivers).
    Returns a Series indexed like va_gdf with EDName2025 values.
    """
    # Use representative_point() (guaranteed inside polygon) rather than true
    # centroid, matching mcmc_ensemble.py's score_exogenous_map().  Consistent
    # centroid method is required so VA→ED assignments agree between the two
    # scripts; true centroid can fall outside concave VAs.
    centroids = va_gdf[["geometry"]].copy()
    centroids["geometry"] = va_gdf.geometry.representative_point()

    joined = gpd.sjoin(
        centroids, ed_gdf[["EDName2025", "geometry"]], how="left", predicate="within"
    )

    unresolved_mask = joined["EDName2025"].isna()
    n_unresolved = int(unresolved_mask.sum())

    if n_unresolved > 0:
        nearest = gpd.sjoin_nearest(
            centroids.loc[unresolved_mask.values],
            ed_gdf[["EDName2025", "geometry"]],
            how="left",
        )
        joined.loc[unresolved_mask.values, "EDName2025"] = nearest["EDName2025"].values
        print(f"    Nearest-ED fallback applied to {n_unresolved} centroids")

    return joined["EDName2025"]


# ── Block-permutation null ─────────────────────────────────────────────────────


def _build_swing_adjacency(va_gdf_swing: gpd.GeoDataFrame) -> dict[int, list[int]]:
    """Build a queen-contiguity adjacency graph over the swing-zone VA rows.

    Parameters
    ----------
    va_gdf_swing : GeoDataFrame
        Subset of the VA GeoDataFrame corresponding to swing-zone rows only,
        with a positional integer index (0 … n_swing-1).

    Returns
    -------
    adj : dict[int, list[int]]
        Mapping from positional index i -> list of positional indices j that
        share a boundary or vertex (queen contiguity).  Self-loops excluded.
    """
    n = len(va_gdf_swing)
    geoms = va_gdf_swing.geometry.values
    sindex = va_gdf_swing.sindex
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for i in range(n):
        candidates = list(sindex.intersection(geoms[i].bounds))
        for j in candidates:
            if j <= i:
                continue
            try:
                inter = geoms[i].intersection(geoms[j])
                if not inter.is_empty:
                    adj[i].append(j)
                    adj[j].append(i)
            except Exception:
                pass
    return adj


def _greedy_blocks(adj: dict[int, list[int]], n: int, block_size: int,
                   rng: np.random.Generator) -> list[int]:
    """Assign each swing-zone VA to a block label using a greedy BFS approach.

    Starting from a random unvisited seed, BFS expands until the block reaches
    `block_size` members, then a new seed is chosen.  The resulting blocks are
    geographically compact and of approximately equal size.

    Parameters
    ----------
    adj : adjacency dict from _build_swing_adjacency
    n : total number of swing-zone VAs
    block_size : target number of VAs per block
    rng : seeded numpy Generator for reproducibility

    Returns
    -------
    block_labels : list[int] of length n — block index for each VA (0-indexed)
    """
    order = rng.permutation(n)  # randomise seed order
    block_labels = [-1] * n
    block_id = 0
    visited = [False] * n

    for seed in order:
        if visited[seed]:
            continue
        # BFS from this seed
        queue = [seed]
        members: list[int] = []
        visited[seed] = True
        head = 0
        while head < len(queue) and len(members) < block_size:
            cur = queue[head]
            head += 1
            members.append(cur)
            for nb in adj[cur]:
                if not visited[nb] and len(members) < block_size:
                    visited[nb] = True
                    queue.append(nb)
        for m in members:
            block_labels[m] = block_id
        block_id += 1

    # Any remaining unvisited nodes (isolated, or left over) get their own blocks
    for i in range(n):
        if block_labels[i] == -1:
            block_labels[i] = block_id
            block_id += 1

    return block_labels


def block_permutation_null(
    va_gdf: gpd.GeoDataFrame,
    va: pd.DataFrame,
    swing_mask: np.ndarray,
    sw_maj_idx: np.ndarray,
    sw_min_idx: np.ndarray,
    sw_ndp_arr: np.ndarray,
    sw_ucp_arr: np.ndarray,
    nsw_ndp_agg: np.ndarray,
    nsw_ucp_agg: np.ndarray,
    n_eds: int,
    eg_maj_fixed: float,
    total_prov: float,
    n_boot: int = 10_000,
    seed: int = None,
    block_size: int = 5,
) -> np.ndarray:
    """Block-permutation null distribution for the SZAT statistic.

    Addresses spatial non-exchangeability (T1.10b): the 2,110 swing-zone VAs
    are clustered politically (Moran's I z = 12.15 on NDP-share), so i.i.d.
    per-VA Bernoulli flips understate null variance.  This function groups
    adjacent swing-zone VAs into contiguous blocks of `block_size` using BFS
    over a queen-contiguity graph, then flips each block as a unit (Bernoulli
    0.5).  All VAs within a flipped block move together from majority_ed to
    minority_ed (or vice versa), preserving local spatial structure.

    The (b+1)/(B+1) finite-sample correction is applied in the caller
    (run_permutation_test), matching T1.10 closure convention.

    Parameters
    ----------
    va_gdf : GeoDataFrame aligned to the post-dropna `va` DataFrame (same order)
    va : DataFrame of VA rows (output of the main assignment + swing-zone step)
    swing_mask : bool array (len = len(va)) — True for swing-zone rows
    sw_maj_idx, sw_min_idx : integer ED indices for each swing VA
    sw_ndp_arr, sw_ucp_arr : vote totals for each swing VA
    nsw_ndp_agg, nsw_ucp_agg : pre-aggregated non-swing contributions (constant)
    n_eds : total number of EDs in the union
    eg_maj_fixed : observed EG of majority map (fixed reference)
    total_prov : provincial two-party total
    n_boot : number of permutation draws (default 10,000)
    seed : RNG seed (canonical drand-derived integer)
    block_size : target VAs per block (default 5)

    Returns
    -------
    boot_scores : np.ndarray of shape (n_boot,) — SZAT_perm = EG_perm - eg_maj_fixed
    """
    rng = np.random.default_rng(seed)

    # Build adjacency over swing-zone VA geometries only.
    # va_gdf must be aligned to the same row order as va (post-dropna).
    swing_indices = np.where(swing_mask)[0]
    va_gdf_swing = va_gdf.iloc[swing_indices].reset_index(drop=True)
    adj = _build_swing_adjacency(va_gdf_swing)

    n_swing = len(swing_indices)
    block_labels = _greedy_blocks(adj, n_swing, block_size, rng)
    n_blocks = max(block_labels) + 1

    print(
        f"  [block-permutation] {n_swing} swing VAs -> {n_blocks} blocks "
        f"(target block_size={block_size}, mean={n_swing/n_blocks:.1f})"
    )

    def _eg_from_agg(ed_ndp: np.ndarray, ed_ucp: np.ndarray) -> float:
        ed_total = ed_ndp + ed_ucp
        threshold = ed_total / 2.0
        ndp_wins = ed_ndp >= ed_ucp
        w_ndp = np.where(ndp_wins, np.maximum(0.0, ed_ndp - threshold), ed_ndp)
        w_ucp = np.where(ndp_wins, ed_ucp, np.maximum(0.0, ed_ucp - threshold))
        return (w_ndp.sum() - w_ucp.sum()) / total_prov

    block_labels_arr = np.array(block_labels, dtype=np.int32)  # (n_swing,)
    boot_scores = np.empty(n_boot)

    for i in range(n_boot):
        # Flip each block independently — Bernoulli(0.5) per block
        block_flip = rng.random(n_blocks) < 0.5  # True -> use minority_ed
        va_flip = block_flip[block_labels_arr]   # broadcast to VA level
        perm_sw_idx = np.where(va_flip, sw_min_idx, sw_maj_idx)
        ed_ndp = nsw_ndp_agg + np.bincount(perm_sw_idx, weights=sw_ndp_arr, minlength=n_eds)
        ed_ucp = nsw_ucp_agg + np.bincount(perm_sw_idx, weights=sw_ucp_arr, minlength=n_eds)
        boot_scores[i] = _eg_from_agg(ed_ndp, ed_ucp) - eg_maj_fixed

    return boot_scores


def run_permutation_test(
    swing_mask: np.ndarray,
    sw_maj_idx: np.ndarray,
    sw_min_idx: np.ndarray,
    sw_ndp_arr: np.ndarray,
    sw_ucp_arr: np.ndarray,
    nsw_ndp_agg: np.ndarray,
    nsw_ucp_agg: np.ndarray,
    n_eds: int,
    eg_maj_fixed: float,
    total_prov: float,
    szat_score: float,
    n_boot: int,
    seed: int,
    use_block_permutation: bool = False,
    va_gdf: gpd.GeoDataFrame = None,
    va: pd.DataFrame = None,
    block_size: int = 5,
) -> tuple[np.ndarray, float, float, float]:
    """Run the SZAT permutation test and return (boot_scores, p_value, ci_lo, ci_hi).

    Supports two null distributions:
      use_block_permutation=False (default, pre-registered i.i.d. null):
        Each swing-zone VA is independently flipped Bernoulli(0.5).
        Anti-conservative when spatial autocorrelation is present (T1.10b).
      use_block_permutation=True (T1.10b block-permutation null):
        Swing-zone VAs are grouped into contiguous blocks via queen contiguity;
        each block is flipped as a unit.  Corrects for spatial clustering.

    The (b+1)/(B+1) finite-sample correction is applied in both paths.
    """
    n_swing_boot = int(swing_mask.sum())

    def _eg_from_agg(ed_ndp: np.ndarray, ed_ucp: np.ndarray) -> float:
        ed_total = ed_ndp + ed_ucp
        threshold = ed_total / 2.0
        ndp_wins = ed_ndp >= ed_ucp
        w_ndp = np.where(ndp_wins, np.maximum(0.0, ed_ndp - threshold), ed_ndp)
        w_ucp = np.where(ndp_wins, ed_ucp, np.maximum(0.0, ed_ucp - threshold))
        return (w_ndp.sum() - w_ucp.sum()) / total_prov

    if use_block_permutation:
        if va_gdf is None or va is None:
            raise ValueError("va_gdf and va must be provided for block permutation")
        boot_scores = block_permutation_null(
            va_gdf=va_gdf,
            va=va,
            swing_mask=swing_mask,
            sw_maj_idx=sw_maj_idx,
            sw_min_idx=sw_min_idx,
            sw_ndp_arr=sw_ndp_arr,
            sw_ucp_arr=sw_ucp_arr,
            nsw_ndp_agg=nsw_ndp_agg,
            nsw_ucp_agg=nsw_ucp_agg,
            n_eds=n_eds,
            eg_maj_fixed=eg_maj_fixed,
            total_prov=total_prov,
            n_boot=n_boot,
            seed=seed,
            block_size=block_size,
        )
    else:
        rng = np.random.default_rng(seed)
        boot_scores = np.empty(n_boot)
        for i in range(n_boot):
            flip = rng.random(n_swing_boot) < 0.5
            perm_sw_idx = np.where(flip, sw_min_idx, sw_maj_idx)
            ed_ndp = nsw_ndp_agg + np.bincount(perm_sw_idx, weights=sw_ndp_arr, minlength=n_eds)
            ed_ucp = nsw_ucp_agg + np.bincount(perm_sw_idx, weights=sw_ucp_arr, minlength=n_eds)
            boot_scores[i] = _eg_from_agg(ed_ndp, ed_ucp) - eg_maj_fixed

    # (b+1)/(B+1) finite-sample correction (T1.10 closure 2026-06-12)
    b_extreme = int(np.sum(np.abs(boot_scores) >= abs(szat_score)))
    p_value = float((b_extreme + 1) / (n_boot + 1))
    ci_lo = float(np.percentile(boot_scores, 2.5))
    ci_hi = float(np.percentile(boot_scores, 97.5))
    return boot_scores, p_value, ci_lo, ci_hi


# ── Main ───────────────────────────────────────────────────────────────────────


def run() -> None:
    t0 = time.time()
    parser = argparse.ArgumentParser(description="Swing-Zone Allocation Test")
    parser.add_argument(
        "--full-votes", action="store_true",
        help="Use full-vote columns (va_ucp_full/va_ndp_full) instead of election-day."
    )
    parser.add_argument(
        "--va-file", type=str, default=None,
        help="Override default VA file path (e.g., canonical va_2023_election_day_votes.gpkg)."
    )
    parser.add_argument(
        "--n-boot", type=int, default=None,
        help=f"Override number of permutation draws (default: module constant N_BOOT={N_BOOT:,})."
    )
    parser.add_argument(
        "--use-block-permutation", action="store_true",
        help=(
            "Use contiguity-block null (T1.10b) instead of i.i.d. per-VA flips. "
            "Groups adjacent swing-zone VAs into blocks of --block-size and flips "
            "each block as a unit, correcting for spatial autocorrelation."
        )
    )
    parser.add_argument(
        "--block-size", type=int, default=5,
        help="Target VAs per block for --use-block-permutation (default: 5)."
    )
    args = parser.parse_args()

    ucp_col = "va_ucp_full" if args.full_votes else "va_ucp"
    ndp_col = "va_ndp_full" if args.full_votes else "va_ndp"
    substrate_label = "full (advance+election-day; ~1,544k)" if args.full_votes else "election-day (~896k)"

    va_path = Path(args.va_file) if args.va_file else VA_FILE
    if args.va_file:
        substrate_label += f" [canonical VA: {va_path.name}]"

    suffix = "_full_votes" if args.full_votes else ""
    if args.va_file:
        suffix += "_canonical_va"
    out_csv = REPORTS / f"szat_results{suffix}.csv"
    out_json = REPORTS / f"szat_summary{suffix}.json"

    verify_canonical_files()
    print("Loading shapefiles...")
    va_gdf = gpd.read_file(va_path)
    maj_gdf = gpd.read_file(MAJ_FILE)
    min_gdf = gpd.read_file(MIN_FILE)

    for gdf in (maj_gdf, min_gdf):
        if gdf.crs != va_gdf.crs:
            gdf.to_crs(va_gdf.crs, inplace=True)

    print(
        f"  VAs: {len(va_gdf)}, majority EDs: {len(maj_gdf)}, minority EDs: {len(min_gdf)}"
    )

    print("Assigning VA centroids -> majority EDs...")
    majority_ed = _assign(va_gdf, maj_gdf)
    print("Assigning VA centroids -> minority EDs...")
    minority_ed = _assign(va_gdf, min_gdf)

    unresolved = int(majority_ed.isna().sum() + minority_ed.isna().sum())

    va = pd.DataFrame(
        {
            "va_id": va_gdf["ED_NAME"].astype(str)
            + "|"
            + va_gdf["VA_NUMBER"].astype(str),
            "parent_ed_2019": va_gdf["ED_NAME"].astype(str),
            "va_ndp": va_gdf[ndp_col].fillna(0.0).astype(float),
            "va_ucp": va_gdf[ucp_col].fillna(0.0).astype(float),
            "va_other": va_gdf["va_other"].fillna(0.0).astype(float),
            "majority_ed": majority_ed.values,
            "minority_ed": minority_ed.values,
        }
    )

    va = va.dropna(subset=["majority_ed", "minority_ed"])
    va["is_swing"] = va["majority_ed"] != va["minority_ed"]

    n_swing = int(va["is_swing"].sum())
    print(f"  Swing zones: {n_swing} / {len(va)}")
    # 2110 validated with canonical shapefiles + va_polygons_with_full_2023_votes.gpkg
    # using representative_point(). Update if shapefiles change.
    if n_swing != 2110:
        raise ValueError(
            f"Expected 2110 swing VAs against canonical shapefiles, got {n_swing}. "
            "Check shapefile version — canonical pair: "
            "ea_majority_2026_eds.gpkg / ea_minority_2026_eds.gpkg with "
            "va_polygons_with_full_2023_votes.gpkg. "
            "Also confirm centroid method: representative_point() is now canonical."
        )

    # Provincial vote totals (NDP + UCP only; consistent with EG convention)
    total_prov = float((va["va_ndp"] + va["va_ucp"]).sum())

    # ── ED-level vote aggregation for each map ─────────────────────────────────

    def _ed_totals(df: pd.DataFrame, ed_col: str) -> pd.DataFrame:
        g = df.groupby(ed_col, as_index=False).agg(
            ndp=("va_ndp", "sum"),
            ucp=("va_ucp", "sum"),
        )
        return g.rename(columns={ed_col: "ed_name"})

    maj_totals = _ed_totals(va, "majority_ed")
    min_totals = _ed_totals(va, "minority_ed")

    eg_maj = compute_eg(maj_totals)
    eg_min = compute_eg(min_totals)
    szat_score = eg_min - eg_maj

    print(f"\nEG majority:                 {eg_maj:+.6f}")
    print(f"EG minority:                 {eg_min:+.6f}")
    print(f"SZAT score (min - maj):      {szat_score:+.6f}")

    # ── Per-VA EG contributions ────────────────────────────────────────────────

    maj_lookup = maj_totals.set_index("ed_name")[["ndp", "ucp"]].to_dict("index")
    min_lookup = min_totals.set_index("ed_name")[["ndp", "ucp"]].to_dict("index")

    def _contrib(row: pd.Series, ed_col: str, lookup: dict) -> float:
        ed = row[ed_col]
        ed_data = lookup.get(ed, {"ndp": 0.0, "ucp": 0.0})
        return va_eg_contribution(
            row["va_ndp"],
            row["va_ucp"],
            ed_data["ndp"],
            ed_data["ucp"],
            total_prov,
        )

    va["eg_contrib_majority"] = va.apply(
        lambda r: _contrib(r, "majority_ed", maj_lookup), axis=1
    )
    va["eg_contrib_minority"] = va.apply(
        lambda r: _contrib(r, "minority_ed", min_lookup), axis=1
    )
    va["delta_eg"] = va["eg_contrib_minority"] - va["eg_contrib_majority"]
    va["region"] = va["majority_ed"].apply(_region)

    # Validate regional classification is exhaustive
    _valid_regions = {"Calgary", "Edmonton", "Mountain-West", "Rest of Alberta"}
    _assigned = set(va["region"].unique())
    if not (_assigned <= _valid_regions):
        raise InsufficientDataError(f"Unknown region labels: {_assigned - _valid_regions}")
    _all_eds = set(va["majority_ed"].unique())
    _covered = set(va["majority_ed"])
    if _covered != _all_eds:
        raise InsufficientDataError("Some EDs missing from regional assignment")
    _rest_eds = sorted(va.loc[va["region"] == "Rest of Alberta", "majority_ed"].unique())
    print(f"  Rest of Alberta EDs ({len(_rest_eds)}): {_rest_eds}")

    # ── Regional and focal breakdown ───────────────────────────────────────────

    swing_va = va[va["is_swing"]]

    regional: dict[str, float] = {
        r: float(swing_va.loc[swing_va["region"] == r, "delta_eg"].sum())
        for r in ("Calgary", "Edmonton", "Rest of Alberta", "Mountain-West")
    }

    focal_contribution = float(
        swing_va.loc[
            swing_va["majority_ed"].isin(FOCAL_EDS)
            | swing_va["minority_ed"].isin(FOCAL_EDS),
            "delta_eg",
        ].sum()
    )

    print("\nRegional SZAT breakdown (swing zones only):")
    for region, val in sorted(regional.items()):
        print(f"  {region:<22} {val:+.6f}")
    print(f"  {'Canmore/RMH focal EDs':<22} {focal_contribution:+.6f}")

    # ── Bootstrap significance test (full-recompute, pre-registered procedure) ──
    # Pre-registered in szat_prereg_draft.md: for each permutation, each swing-zone
    # VA is randomly assigned to majority_ed or minority_ed (Bernoulli 0.5);
    # non-swing VAs keep majority_ed; EG recomputed from scratch.
    # SZAT_perm = EG(perm_minority) - EG(majority_fixed)
    # Replaces earlier additive-delta approximation (captured only direct swing
    # effects = 54.9% of score; anti-conservative vs the pre-registered null).
    #
    # T1.10b (2026-06-13): block-permutation null available via
    # --use-block-permutation.  Permutes contiguous blocks of swing-zone VAs
    # (queen-contiguity graph) rather than individual VAs, correcting for the
    # spatial autocorrelation documented in Moran's I z = 12.15.

    n_boot = args.n_boot if args.n_boot is not None else N_BOOT
    null_label = "block-permutation (T1.10b)" if args.use_block_permutation else "i.i.d. per-VA flip (pre-registered)"
    print(f"\nBootstrapping ({n_boot:,} permutations, {null_label})...")

    sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
    from drand_seed import get_canonical_seed  # fails loudly if missing — no fallback

    seed = get_canonical_seed("szat-bootstrap")
    seed_source = "drand_seed.get_canonical_seed"

    print(f"  Seed: {seed} ({seed_source})")

    # Pre-encode ED names to integer indices for fast bincount aggregation
    all_eds_union = np.unique(
        np.concatenate([va["majority_ed"].values, va["minority_ed"].values])
    )
    ed_to_idx = {e: i for i, e in enumerate(all_eds_union)}
    n_eds = len(all_eds_union)

    swing_mask = va["is_swing"].values.astype(bool)
    sw_maj_idx = np.array([ed_to_idx[e] for e in va.loc[swing_mask, "majority_ed"].values])
    sw_min_idx = np.array([ed_to_idx[e] for e in va.loc[swing_mask, "minority_ed"].values])
    sw_ndp_arr = va.loc[swing_mask, "va_ndp"].values
    sw_ucp_arr = va.loc[swing_mask, "va_ucp"].values
    nsw_idx    = np.array([ed_to_idx[e] for e in va.loc[~swing_mask, "majority_ed"].values])
    nsw_ndp_arr = va.loc[~swing_mask, "va_ndp"].values
    nsw_ucp_arr = va.loc[~swing_mask, "va_ucp"].values

    # Non-swing contributions are constant across all permutations
    nsw_ndp_agg = np.bincount(nsw_idx, weights=nsw_ndp_arr, minlength=n_eds)
    nsw_ucp_agg = np.bincount(nsw_idx, weights=nsw_ucp_arr, minlength=n_eds)

    eg_maj_fixed = eg_maj  # majority map is the fixed reference

    # Align va_gdf to the post-dropna va index for block permutation geometry access.
    # va was constructed from va_gdf rows and then dropna'd; track which va_gdf rows
    # survived so the block-permutation adjacency graph uses the correct geometries.
    va_gdf_aligned = va_gdf.iloc[va.index].reset_index(drop=True)
    va_reset = va.reset_index(drop=True)

    boot_scores, p_value, ci_lo, ci_hi = run_permutation_test(
        swing_mask=va_reset["is_swing"].values.astype(bool),
        sw_maj_idx=sw_maj_idx,
        sw_min_idx=sw_min_idx,
        sw_ndp_arr=sw_ndp_arr,
        sw_ucp_arr=sw_ucp_arr,
        nsw_ndp_agg=nsw_ndp_agg,
        nsw_ucp_agg=nsw_ucp_agg,
        n_eds=n_eds,
        eg_maj_fixed=eg_maj_fixed,
        total_prov=total_prov,
        szat_score=szat_score,
        n_boot=n_boot,
        seed=seed,
        use_block_permutation=args.use_block_permutation,
        va_gdf=va_gdf_aligned if args.use_block_permutation else None,
        va=va_reset if args.use_block_permutation else None,
        block_size=args.block_size,
    )

    b_extreme = int(np.sum(np.abs(boot_scores) >= abs(szat_score)))

    boot_eg_raw = boot_scores + eg_maj_fixed
    np.save(DATA / "szat_bootstrap_eg_samples.npy", boot_eg_raw)
    print(f"  Bootstrap EG samples saved: {len(boot_eg_raw)} draws")

    print(f"  p-value (two-tailed):        {p_value:.4f} (b+1)/(B+1) on {b_extreme}/{n_boot}")
    print(f"  Null 95% interval:           [{ci_lo:+.6f}, {ci_hi:+.6f}]")
    print(f"  Observed SZAT score:         {szat_score:+.6f}")
    print(f"  Null type:                   {null_label}")

    # ── Outputs ────────────────────────────────────────────────────────────────

    out = va[
        [
            "va_id",
            "parent_ed_2019",
            "majority_ed",
            "minority_ed",
            "is_swing",
            "va_ndp",
            "va_ucp",
            "va_other",
            "eg_contrib_majority",
            "eg_contrib_minority",
            "delta_eg",
            "region",
        ]
    ].copy()
    out["is_swing"] = out["is_swing"].astype(int)
    out.to_csv(out_csv, index=False, float_format="%.6f")

    summary = {
        "substrate": substrate_label,
        "szat_score": round(szat_score, 6),
        "eg_majority": round(eg_maj, 6),
        "eg_minority": round(eg_min, 6),
        "swing_zone_count": n_swing,
        "total_va_count": int(len(va)),
        "unresolved_count": unresolved,
        "bootstrap_p_value": round(p_value, 4),
        "bootstrap_n": n_boot,
        "bootstrap_null_type": null_label,
        "bootstrap_block_size": args.block_size if args.use_block_permutation else None,
        "bootstrap_seed": seed,
        "bootstrap_ci_95": [round(ci_lo, 6), round(ci_hi, 6)],
        "regional_breakdown": {k: round(v, 6) for k, v in regional.items()},
        "canmore_rmh_contribution": round(focal_contribution, 6),
        "canonical_shapefiles": {
            "majority": str(MAJ_FILE.relative_to(ROOT)),
            "minority": str(MIN_FILE.relative_to(ROOT)),
        },
    }
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults written:")
    print(f"  {out_csv}")
    print(f"  {out_json}")
    _log_run(__file__, [str(p) for p in [out_csv, out_json]], time.time() - t0)


if __name__ == "__main__":
    run()
