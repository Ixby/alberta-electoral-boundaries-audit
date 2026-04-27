"""Polsby-Popper compactness for the Python ReCom verification subset.

Computes per-plan PP for each of the 10,000 saved partition assignments in
data/v0_1_mcmc_verification_assignments.npz, using the cut-edge trick so
we don't have to do 870,000 polygon dissolves.

For each VA we precompute:
  - own area
  - own external perimeter (the part of the VA boundary that is NOT
    shared with any other VA — i.e. the province / no-neighbour edge)
  - per-neighbour shared-edge lengths

For each saved partition:
  - district area = sum(VA areas)
  - district perimeter = sum(VA external boundary contributions) +
    sum(shared-edge lengths to OTHER-district neighbours)
  - PP per district = 4 * pi * area / perimeter^2
  - mean PP across districts is the per-plan summary

Output: data/v0_1_python_recom_polsby_popper.csv with one row per plan.

This pairs with the R `redist` SMC compactness output for the
falsification tests proposed by the PO ("the mechanism is the geometry").
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
from shapely.ops import unary_union
import warnings
warnings.simplefilter("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
VA_GPKG = ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
NPZ = ROOT / "data" / "v0_1_mcmc_verification_assignments.npz"
METRICS_CSV = ROOT / "data" / "v0_1_mcmc_verification_metrics.csv"
OUT_CSV = ROOT / "data" / "v0_1_python_recom_polsby_popper.csv"


def main() -> int:
    print(f"[pp] loading VA polygons from {VA_GPKG}")
    va = gpd.read_file(VA_GPKG).to_crs(3401)
    n_va = len(va)
    print(f"[pp] {n_va} VAs")

    # Pre-compute per-VA area + per-VA total-boundary length
    va_area = va.geometry.area.values
    va_perim = va.geometry.length.values

    # Build shared-edge length per (i, j) neighbour pair via spatial-join
    # of VA boundaries against each other. Uses sindex for speed.
    print(f"[pp] computing shared-boundary edge lengths...")
    t0 = time.time()
    sindex = va.sindex
    shared_len = {}  # (i, j) with i < j -> shared edge length (metres)
    boundaries = [g.boundary for g in va.geometry]
    for i, geom_i in enumerate(va.geometry):
        if i % 500 == 0:
            print(f"  va {i}/{n_va} ({time.time()-t0:.0f}s)", flush=True)
        candidates = list(sindex.intersection(geom_i.bounds))
        for j in candidates:
            if j <= i:
                continue
            inter = boundaries[i].intersection(boundaries[j])
            if inter.is_empty:
                continue
            try:
                L = inter.length
            except Exception:
                L = 0.0
            if L > 0.0:
                shared_len[(i, j)] = float(L)
    print(f"[pp] computed {len(shared_len)} shared edges in {time.time()-t0:.0f}s")

    # Build per-VA shared-with-others-total length so we can derive
    # external (non-shared) perimeter as: external = total - sum_shared
    shared_sum = np.zeros(n_va, dtype=float)
    for (i, j), L in shared_len.items():
        shared_sum[i] += L
        shared_sum[j] += L
    external_perim = va_perim - shared_sum
    # Numerical noise: clip negatives to zero
    external_perim = np.maximum(external_perim, 0.0)

    # Index-form neighbour list for fast iteration in the per-plan loop
    neigh_pairs = list(shared_len.items())  # [((i, j), L), ...]
    pairs_arr = np.array([k for k, _ in neigh_pairs], dtype=np.int64)
    pairs_len = np.array([v for _, v in neigh_pairs], dtype=float)
    print(f"[pp] {len(pairs_arr)} neighbour pairs serialised")

    # Load saved per-plan assignments (verification subset)
    print(f"[pp] loading {NPZ}")
    npz = np.load(NPZ)
    assignments = npz["assignments"]  # shape (N_PLANS, n_va), int8
    va_ids = npz["va_ids"]
    N_PLANS = assignments.shape[0]
    print(f"[pp] {N_PLANS} plans, {assignments.shape[1]} VAs each")

    # The npz va_ids array gives the column ordering used when saving
    # the assignments. We need to map each assignment column to the
    # corresponding row in the va frame. Assume va is in row order by
    # OBJECTID and va_ids matches that ordering 1:1; if not, the
    # rendered assignment column j corresponds to va.iloc[ va_ids[j] ].
    # In practice the verification subset was saved with sorted graph
    # node ids; for the canonical Alberta gpkg this matches the row
    # order. Verify by length match.
    if assignments.shape[1] != n_va:
        raise RuntimeError(f"VA count mismatch: assignments has "
                           f"{assignments.shape[1]} columns, VA frame has {n_va}")

    # Per-plan computation
    # district area = sum(va_area where assignment == d)
    # district perim = sum(external_perim where assignment == d) +
    #                  sum(pairs_len for pairs (i,j) where a[i] != a[j])
    # Then per-district PP = 4*pi*A/P^2; mean across districts.
    print(f"[pp] computing Polsby-Popper for {N_PLANS} plans...")
    t0 = time.time()
    pp_per_plan = np.zeros(N_PLANS, dtype=float)
    pp_min_per_plan = np.zeros(N_PLANS, dtype=float)

    for p_idx in range(N_PLANS):
        if p_idx % 500 == 0:
            elapsed = time.time() - t0
            rate = (p_idx + 1) / elapsed if elapsed > 0 else 0
            eta = (N_PLANS - p_idx - 1) / rate if rate > 0 else 0
            print(f"  plan {p_idx}/{N_PLANS} ({rate:.0f}/s, eta {eta:.0f}s)",
                  flush=True)
        a = assignments[p_idx].astype(np.int32)
        # Per-district area + external-perim sums via bincount
        # (length = max(a)+1)
        n_dist = int(a.max()) + 1
        area = np.bincount(a, weights=va_area, minlength=n_dist)
        perim = np.bincount(a, weights=external_perim, minlength=n_dist)
        # Cut edges: vectorised over the neighbour-pair array
        i_arr, j_arr = pairs_arr[:, 0], pairs_arr[:, 1]
        ai = a[i_arr]
        aj = a[j_arr]
        cut_mask = ai != aj
        if cut_mask.any():
            cut_i = ai[cut_mask]
            cut_j = aj[cut_mask]
            cut_L = pairs_len[cut_mask]
            np.add.at(perim, cut_i, cut_L)
            np.add.at(perim, cut_j, cut_L)
        # Polsby-Popper per district
        # Skip zero-area districts to avoid divide-by-zero
        valid = (area > 0) & (perim > 0)
        if not valid.any():
            pp_per_plan[p_idx] = float("nan")
            pp_min_per_plan[p_idx] = float("nan")
            continue
        pp = np.full(n_dist, np.nan)
        pp[valid] = 4.0 * math.pi * area[valid] / (perim[valid] ** 2)
        pp_per_plan[p_idx] = float(np.nanmean(pp))
        pp_min_per_plan[p_idx] = float(np.nanmin(pp))

    elapsed = time.time() - t0
    print(f"[pp] done in {elapsed:.0f}s ({N_PLANS/elapsed:.0f} plans/s)")

    # Cross-reference with the saved metrics CSV so we have
    # (plan_idx, seats@50/50, polsby_popper) per row.
    metrics = pd.read_csv(METRICS_CSV)
    out = pd.DataFrame({
        "step": np.arange(N_PLANS),
        "seats_at_50_50": metrics["seats_at_50_50"].values[:N_PLANS]
                          if "seats_at_50_50" in metrics.columns
                          else np.full(N_PLANS, np.nan),
        "polsby_popper_mean": pp_per_plan,
        "polsby_popper_min": pp_min_per_plan,
    })
    out.to_csv(OUT_CSV, index=False)
    print(f"[pp] wrote {OUT_CSV.relative_to(ROOT)}")

    print()
    print("=== Distribution summary ===")
    print(f"  PP mean   median: {np.nanmedian(pp_per_plan):.4f}")
    print(f"  PP mean   p5:     {np.nanpercentile(pp_per_plan, 5):.4f}")
    print(f"  PP mean   p95:    {np.nanpercentile(pp_per_plan, 95):.4f}")

    # Falsification Test #2 prep — Python ReCom side
    if "seats_at_50_50" in metrics.columns:
        s50 = metrics["seats_at_50_50"].values[:N_PLANS]
        high = s50 >= 0.4831
        print()
        print("Falsification Test #2 (Python ReCom side):")
        print(f"  N plans with s50 >= 0.4831: {high.sum()} of {N_PLANS}")
        if high.sum() > 0:
            print(f"  Mean PP among high-s50 plans: {np.nanmean(pp_per_plan[high]):.4f}")
            print(f"  Mean PP among other plans:    {np.nanmean(pp_per_plan[~high]):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
