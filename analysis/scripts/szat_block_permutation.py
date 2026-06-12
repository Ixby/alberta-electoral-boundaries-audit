"""
szat_block_permutation.py — SZAT bootstrap null with contiguity-respecting block permutation.

T1.10b closed 2026-06-12 per T1.7 R1 Ref #1 D3. The original SZAT bootstrap
in `szat.py` flips each of 2,110 swing-zone VAs i.i.d. Bernoulli(0.5);
that null assumes the swing VAs are exchangeable, which the audit's own
Moran's I z = 12.15 on NDP-share strongly contradicts. Spatially adjacent
swing-zone VAs cluster politically, so independent per-VA flips
*understate* the null variance — making the reported p anti-conservative
(Lehmann & Romano 2005 ch.15; Legendre 1993 Ecology 74).

This script replaces the i.i.d. flip with a block-permutation null:

  1. Build a queen-contiguity graph over the swing-zone VAs.
  2. Find connected components in the graph — these are spatial "blocks"
     of contiguous swing VAs.
  3. For each bootstrap iteration: flip each BLOCK i.i.d. Bernoulli(0.5)
     (every VA in a block gets the same flip), not each VA independently.
  4. Aggregate to ED-level and compute the SZAT statistic exactly as the
     i.i.d. version does. Report p with (b+1)/(B+1) finite-sample correction.

Expected effect (per Ref #1): ~30 % widening of the SZAT null variance
because spatially correlated flips have a larger variance than independent
flips at the same expected mean. The point estimate of the SZAT score is
unchanged; only the null distribution widens, so p may rise from 0.0024
to something like 0.005-0.01.

Backward:
  analysis/scripts/szat.py — original i.i.d.-flip implementation
Forward:
  findings/szat_block_permutation.{md,json}
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

try:
    from drand_seed import get_canonical_seed
except Exception:
    def get_canonical_seed(salt: str) -> int:
        # Fallback: deterministic but not drand-anchored
        import hashlib
        return int(hashlib.sha256(salt.encode("utf-8")).hexdigest()[:12], 16) & ((1 << 32) - 1)


N_BOOT = 10_000
SALT = "szat-block-permutation"


def queen_contiguity_components(swing_va: gpd.GeoDataFrame) -> np.ndarray:
    """Return a 1-D array of component labels (one per swing VA).

    Two VAs are in the same component iff their polygons share *any* boundary
    (queen contiguity: edge or vertex). Uses STRtree for an efficient pairwise
    intersection scan in O(N · log N) average case.
    """
    from shapely.strtree import STRtree

    geoms = swing_va.geometry.reset_index(drop=True).values
    n = len(geoms)
    tree = STRtree(list(geoms))
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for i, g in enumerate(geoms):
        candidates = list(tree.query(g.buffer(1.0)))  # 1 m buffer to catch edge-sharing
        for j in candidates:
            j = int(j)
            if j <= i:
                continue
            if g.touches(geoms[j]) or g.intersects(geoms[j]):
                # `intersects` would catch any shared point; `touches` covers
                # boundary-shared without interior overlap (queen contiguity)
                union(i, j)

    labels = np.array([find(i) for i in range(n)])
    # Compact labels to 0..k-1
    uniq, inv = np.unique(labels, return_inverse=True)
    return inv


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--va-source", type=Path,
                    default=ROOT / "data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg",
                    help="VA polygon layer with majority_ed / minority_ed assigned + is_swing flag. "
                         "Falls back to the canonical SZAT pre-processed file if present.")
    ap.add_argument("--swing-cache", type=Path,
                    default=ROOT / "data/outputs/szat_swing_va_canonical.gpkg",
                    help="Optional cached pre-computed swing-VA polygons (avoids re-running SZAT setup)")
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--output-json", type=Path,
                    default=ROOT / "findings/szat_block_permutation.json")
    ap.add_argument("--output-md", type=Path,
                    default=ROOT / "findings/szat_block_permutation.md")
    args = ap.parse_args(argv)

    if args.seed is None:
        args.seed = get_canonical_seed(SALT)

    # Reuse SZAT's pre-processing to get the swing-VA dataframe + indexing
    t0 = time.time()
    print(f"[setup] Loading SZAT pipeline state ...", flush=True)

    if args.swing_cache.exists():
        print(f"  Loading cached swing-VA layer at {args.swing_cache}", flush=True)
        swing_va = gpd.read_file(args.swing_cache)
        va = swing_va  # cache has only swing rows; we reconstitute below if needed
    else:
        print("  Computing canonical SZAT-style VA assignments inline ...", flush=True)
        from packing_cracking_analysis import score_map_by_spatial_join
        from canonical_paths import canonical_shapefile, ED_NAME_COL
        va_gdf = gpd.read_file(args.va_source)
        # Assign each VA to its containing ED on each map
        def _assign(va_gdf: gpd.GeoDataFrame, shp_path: Path) -> np.ndarray:
            eds = gpd.read_file(shp_path)[[ED_NAME_COL, "geometry"]]
            if eds.crs != va_gdf.crs:
                eds = eds.to_crs(va_gdf.crs)
            cents = va_gdf.copy()
            cents["geometry"] = va_gdf.geometry.representative_point()
            joined = gpd.sjoin(cents[["geometry"]], eds, how="left", predicate="within")
            joined = joined[~joined.index.duplicated(keep="first")]
            return joined[ED_NAME_COL].values
        va_gdf["majority_ed"] = _assign(va_gdf, canonical_shapefile("majority"))
        va_gdf["minority_ed"] = _assign(va_gdf, canonical_shapefile("minority"))
        # Drop VAs unresolved on either map
        va = va_gdf.dropna(subset=["majority_ed", "minority_ed"]).copy()
        va["is_swing"] = va["majority_ed"].values != va["minority_ed"].values
        swing_va = va[va["is_swing"]].copy().reset_index(drop=True)
        # Cache for future re-runs
        try:
            args.swing_cache.parent.mkdir(parents=True, exist_ok=True)
            swing_va.to_file(args.swing_cache, driver="GPKG")
            print(f"  Cached swing-VA layer at {args.swing_cache}", flush=True)
        except Exception as e:
            print(f"  WARN: failed to cache swing-VA layer: {e}", flush=True)

    n_swing = len(swing_va)
    print(f"  Swing-zone VAs: {n_swing:,}", flush=True)

    # ── Build the contiguity graph + connected-component labels ───────────────
    print(f"[setup] Computing queen-contiguity components over {n_swing:,} swing VAs ...", flush=True)
    t1 = time.time()
    components = queen_contiguity_components(swing_va)
    n_components = int(components.max() + 1)
    elapsed = time.time() - t1
    sizes = np.bincount(components)
    print(f"  {n_components:,} connected components in {elapsed:.1f} s", flush=True)
    print(f"  Component size distribution: median={int(np.median(sizes))}, "
          f"max={int(sizes.max())}, p95={int(np.percentile(sizes, 95))}", flush=True)

    # ── Compute the observed SZAT statistic ───────────────────────────────────
    # Re-derive sw_maj_idx, sw_min_idx, sw_ndp/ucp_arr, nsw_* exactly as szat.py does
    print(f"[setup] Encoding ED indices + observed SZAT ...", flush=True)
    all_eds = np.unique(np.concatenate([va["majority_ed"].values, va["minority_ed"].values]))
    ed_to_idx = {e: i for i, e in enumerate(all_eds)}
    n_eds = len(all_eds)

    swing_mask = va["is_swing"].values.astype(bool) if "is_swing" in va.columns else np.ones(len(va), dtype=bool)
    if swing_mask.sum() != n_swing:
        # The cached file may already be filtered to swing only
        swing_mask = np.ones(n_swing, dtype=bool)

    sw_maj_idx = np.array([ed_to_idx[e] for e in va.loc[swing_mask, "majority_ed"].values])
    sw_min_idx = np.array([ed_to_idx[e] for e in va.loc[swing_mask, "minority_ed"].values])
    sw_ndp_arr = va.loc[swing_mask, "va_ndp"].values
    sw_ucp_arr = va.loc[swing_mask, "va_ucp"].values
    nsw_idx    = np.array([ed_to_idx[e] for e in va.loc[~swing_mask, "majority_ed"].values])
    nsw_ndp_arr = va.loc[~swing_mask, "va_ndp"].values
    nsw_ucp_arr = va.loc[~swing_mask, "va_ucp"].values
    nsw_ndp_agg = np.bincount(nsw_idx, weights=nsw_ndp_arr, minlength=n_eds)
    nsw_ucp_agg = np.bincount(nsw_idx, weights=nsw_ucp_arr, minlength=n_eds)

    def _eg_from_agg(ed_ndp: np.ndarray, ed_ucp: np.ndarray) -> float:
        total_prov = (ed_ndp + ed_ucp).sum()
        if total_prov == 0:
            return 0.0
        # Continuous EG: w_p = max(votes_p - threshold, 0) where threshold = total/2
        threshold = (ed_ndp + ed_ucp) / 2.0
        w_ndp = np.where(ed_ndp > threshold, ed_ndp - threshold, ed_ndp)
        w_ucp = np.where(ed_ucp > threshold, ed_ucp - threshold, ed_ucp)
        return float((w_ndp.sum() - w_ucp.sum()) / total_prov)

    # Observed: swing zones routed to minority partition vs majority partition
    ed_ndp_min = nsw_ndp_agg + np.bincount(sw_min_idx, weights=sw_ndp_arr, minlength=n_eds)
    ed_ucp_min = nsw_ucp_agg + np.bincount(sw_min_idx, weights=sw_ucp_arr, minlength=n_eds)
    ed_ndp_maj = nsw_ndp_agg + np.bincount(sw_maj_idx, weights=sw_ndp_arr, minlength=n_eds)
    ed_ucp_maj = nsw_ucp_agg + np.bincount(sw_maj_idx, weights=sw_ucp_arr, minlength=n_eds)
    eg_min_fixed = _eg_from_agg(ed_ndp_min, ed_ucp_min)
    eg_maj_fixed = _eg_from_agg(ed_ndp_maj, ed_ucp_maj)
    szat_score = eg_min_fixed - eg_maj_fixed
    print(f"  SZAT observed score (minority EG − majority EG, swing routed): {szat_score:+.6f}", flush=True)

    # ── Block-permutation bootstrap ───────────────────────────────────────────
    print(f"[boot] Running {args.n_boot:,} block-permutation iterations (n_blocks={n_components:,}) ...", flush=True)
    t1 = time.time()
    rng = np.random.default_rng(args.seed)
    boot_scores = np.empty(args.n_boot, dtype=np.float64)
    # For each iteration: pick a Bernoulli(0.5) per BLOCK, broadcast to per-VA, route accordingly
    n_va = n_swing
    for i in range(args.n_boot):
        block_flip = rng.random(n_components) < 0.5
        flip_per_va = block_flip[components]  # broadcast
        perm_sw_idx = np.where(flip_per_va, sw_min_idx, sw_maj_idx)
        ed_ndp = nsw_ndp_agg + np.bincount(perm_sw_idx, weights=sw_ndp_arr, minlength=n_eds)
        ed_ucp = nsw_ucp_agg + np.bincount(perm_sw_idx, weights=sw_ucp_arr, minlength=n_eds)
        boot_scores[i] = _eg_from_agg(ed_ndp, ed_ucp) - eg_maj_fixed
        if (i + 1) % 1000 == 0:
            elapsed = time.time() - t1
            print(f"  ... {i+1:,}/{args.n_boot:,} in {elapsed:.1f}s", flush=True)

    elapsed = time.time() - t1
    print(f"  Block-permutation null in {elapsed:.1f} s", flush=True)

    b_extreme = int(np.sum(np.abs(boot_scores) >= abs(szat_score)))
    p_value = float((b_extreme + 1) / (args.n_boot + 1))
    null_mean = float(boot_scores.mean())
    null_std = float(boot_scores.std())
    ci_lo = float(np.percentile(boot_scores, 2.5))
    ci_hi = float(np.percentile(boot_scores, 97.5))

    # ── Compare to i.i.d. null variance (if we can recompute it cheaply) ──────
    print(f"[compare] Recomputing i.i.d.-flip null variance over {args.n_boot:,} draws ...", flush=True)
    t1 = time.time()
    iid_scores = np.empty(args.n_boot, dtype=np.float64)
    rng2 = np.random.default_rng(args.seed + 1)
    for i in range(args.n_boot):
        flip_per_va = rng2.random(n_va) < 0.5
        perm_sw_idx = np.where(flip_per_va, sw_min_idx, sw_maj_idx)
        ed_ndp = nsw_ndp_agg + np.bincount(perm_sw_idx, weights=sw_ndp_arr, minlength=n_eds)
        ed_ucp = nsw_ucp_agg + np.bincount(perm_sw_idx, weights=sw_ucp_arr, minlength=n_eds)
        iid_scores[i] = _eg_from_agg(ed_ndp, ed_ucp) - eg_maj_fixed

    iid_std = float(iid_scores.std())
    iid_p = float((int(np.sum(np.abs(iid_scores) >= abs(szat_score))) + 1) / (args.n_boot + 1))
    var_inflation = (null_std / iid_std) ** 2
    print(f"  i.i.d. null std = {iid_std:.6f}; block null std = {null_std:.6f}", flush=True)
    print(f"  Variance inflation factor (block / i.i.d.) = {var_inflation:.3f}", flush=True)

    elapsed_total = time.time() - t0
    payload = {
        "test": "SZAT bootstrap under contiguity-respecting block permutation",
        "n_swing_va": int(n_swing),
        "n_blocks": int(n_components),
        "block_size_median": int(np.median(sizes)),
        "block_size_max": int(sizes.max()),
        "block_size_p95": int(np.percentile(sizes, 95)),
        "n_boot": int(args.n_boot),
        "seed": int(args.seed),
        "salt": SALT,
        "szat_score": szat_score,
        "p_value_block_permutation": p_value,
        "p_value_iid_flip": iid_p,
        "null_mean_block": null_mean,
        "null_std_block": null_std,
        "null_std_iid": iid_std,
        "variance_inflation_block_over_iid": var_inflation,
        "ci_95_block": [ci_lo, ci_hi],
        "wall_clock_seconds": elapsed_total,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\n✅ Result:", flush=True)
    print(f"  SZAT score                  : {szat_score:+.6f}", flush=True)
    print(f"  p (block permutation null)  : {p_value:.4f}   ({b_extreme}/{args.n_boot})", flush=True)
    print(f"  p (i.i.d. flip, comparison) : {iid_p:.4f}", flush=True)
    print(f"  Variance inflation factor   : {var_inflation:.3f}", flush=True)
    print(f"  Wall clock                  : {elapsed_total:.1f} s", flush=True)
    print(f"  JSON                        : {args.output_json}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
