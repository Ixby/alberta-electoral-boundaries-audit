"""
v0_1_dpg_perfecter.py
=====================
Three-phase DPG improvement pipeline producing v0_8 canonical shapefiles.

Phase 1 — Topology cleanup
    Resolve overlaps by canon_source precedence. For each pair (i, j) where i has
    higher tier: if they overlap, clip j by i. Anti-erasure: if clipping would remove
    >90% of j, keep original (tolerate small residual overlap rather than erasure).
    Algorithm is O(n²) over pairs — for n=89 EDs this is ~3,900 pair tests, each a
    two-polygon operation with GEOS bounding-box pre-filter.

Phase 2 — Edge snapping (nearest-neighbour welding)
    Close sliver gaps between adjacent EDs. Two EDs that are "close but not touching"
    should share exactly the same boundary. Process EDs in tier order (highest first).
    For each ED, find all adjacent EDs within snap_tolerance and snap this ED's
    geometry to the union of those neighbours. Uses shapely.snap() which modifies
    only the source geometry — higher-tier neighbours are never disturbed.

    snap tolerance = 500 m (matches ±500 m perimeter precision for Tier-C v7 polygons).

Phase 3 — Gap fill
    After cleanup + snapping, compute the residual gap (provincial boundary minus ED
    union). Each gap polygon is assigned to the adjacent ED with the longest shared
    border (or nearest centroid as fallback).

Validation gates:
    • No-overlap: every pair post-cleanup has intersection area < 1 m²
    • No-erasure: no ED falls below 10% of original area
    • Full-coverage: gap area after fill < 0.001% of provincial area
    • Name preservation: output has same 89 ED names as input

Backward:
    data/shapefiles/derived/v0_7_canonical_majority_2026_eds.gpkg
    data/shapefiles/derived/v0_7_canonical_minority_2026_eds.gpkg
    data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
Forward:
    Run #4 MCMC, MAUP v3, updated compactness metrics
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import os
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union, snap

warnings.filterwarnings("ignore")

# Cap workers — shapely 2.x releases the GIL for GEOS calls, so threading
# scales reasonably up to ~10 on a 16-core box (the remaining cores absorb
# Python-level overhead in shapely wrappers + room for OS/IO). Override via
# DPG_WORKERS env var if needed.
WORKERS = int(os.environ.get("DPG_WORKERS", min(10, (os.cpu_count() or 4))))

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"

VA_PATH = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
MAJ_V7  = DATA / "shapefiles" / "derived" / "v0_7_canonical_majority_2026_eds.gpkg"
MIN_V7  = DATA / "shapefiles" / "derived" / "v0_7_canonical_minority_2026_eds.gpkg"
MAJ_V8  = DATA / "shapefiles" / "derived" / "v0_8_canonical_majority_2026_eds.gpkg"
MIN_V8  = DATA / "shapefiles" / "derived" / "v0_8_canonical_minority_2026_eds.gpkg"

SNAP_TOLERANCE = 500   # metres
ANTI_ERASURE   = 0.10  # keep original if clipping would remove >90%

TIER_RANK = {
    "da-anchored":            5,
    "municipal-anchored":     4,
    "osm-municipal-buffered": 3,
    "sweep":                  2,
    "v7":                     1,
}


def _clean(geom):
    if not geom.is_valid:
        geom = geom.buffer(0)
    return geom


# ---------------------------------------------------------------------------
# Phase 1 — Pairwise overlap resolution
# ---------------------------------------------------------------------------

def _ts() -> str:
    return time.strftime("%H:%M:%S")


def topology_cleanup(eds: gpd.GeoDataFrame, label: str) -> gpd.GeoDataFrame:
    print(f"[{_ts()}] [{label}] Phase 1 start (topology cleanup)", flush=True)
    t0 = time.time()
    eds = eds.copy()
    if "canon_source" not in eds.columns:
        eds["canon_source"] = "v7"

    eds["__rank"] = eds["canon_source"].map(lambda s: TIER_RANK.get(s, 1))
    # Sort descending so index 0 = highest tier (processes wins first in pair loop)
    eds = eds.sort_values("__rank", ascending=False).reset_index(drop=True)

    new_geoms = [_clean(row.geometry) for _, row in eds.iterrows()]
    n = len(eds)
    overlap_count = 0

    # O(n²) pairwise; GEOS bounding-box pre-filter inside .intersects() keeps it fast
    for i in range(n):
        rank_i = eds.at[i, "__rank"]
        geom_i = new_geoms[i]

        for j in range(i + 1, n):
            rank_j = eds.at[j, "__rank"]
            geom_j = new_geoms[j]

            # Determine winner (higher tier wins; ties go to larger area)
            if rank_i > rank_j:
                wi, li = i, j
            elif rank_j > rank_i:
                wi, li = j, i
            else:
                wi, li = (i, j) if geom_i.area >= geom_j.area else (j, i)

            geom_w = new_geoms[wi]
            geom_l = new_geoms[li]

            if not geom_w.intersects(geom_l):
                continue

            overlap = geom_w.intersection(geom_l)
            if overlap.is_empty or overlap.area <= 1.0:
                continue

            overlap_count += 1
            candidate = _clean(geom_l.difference(geom_w))

            if not candidate.is_empty and candidate.area >= ANTI_ERASURE * geom_l.area:
                new_geoms[li] = candidate
            # else: anti-erasure — keep original (tolerate small residual overlap)

    eds["geometry"] = new_geoms
    eds = eds.drop(columns=["__rank"])
    eds = eds.sort_values("name_2026").reset_index(drop=True)
    print(f"[{_ts()}] [{label}] Phase 1 done in {time.time()-t0:.1f}s "
          f"— {overlap_count} overlapping pairs resolved", flush=True)
    return eds


# ---------------------------------------------------------------------------
# Phase 2 — Edge snapping (nearest-neighbour welding)
# ---------------------------------------------------------------------------

def edge_snap(eds: gpd.GeoDataFrame, label: str,
              tolerance: float = SNAP_TOLERANCE) -> gpd.GeoDataFrame:
    """
    For each ED (processed lowest-tier first), snap it to all adjacent higher-tier
    EDs within `tolerance`. shapely.snap() modifies only the source geometry — the
    higher-tier reference is never changed.

    Safety check: after snapping, if an ED's area changes by more than SNAP_AREA_WARN
    (5%), emit a warning. A large area change suggests a false weld — the snap pulled
    an edge that was 'close but not supposed to touch', distorting the polygon. In
    that case the snap is reverted for that ED and noted.
    """
    SNAP_AREA_WARN = 0.05  # flag if area changes by >5% from snapping

    print(f"[{_ts()}] [{label}] Phase 2 start (edge snap, tol={tolerance}m)", flush=True)
    t0 = time.time()
    eds = eds.copy()
    if "canon_source" not in eds.columns:
        eds["canon_source"] = "v7"

    eds["__rank"] = eds["canon_source"].map(lambda s: TIER_RANK.get(s, 1))
    # Process lowest tier first so they snap to already-snapped neighbours
    order = eds["__rank"].argsort().values   # ascending = lowest first
    eds_ord = eds.iloc[order].copy().reset_index(drop=True)

    new_geoms = [_clean(row.geometry) for _, row in eds_ord.iterrows()]
    n = len(eds_ord)
    snap_count = 0
    revert_count = 0

    # Pre-compute bounds for bbox pre-filter (avoids expensive exact distance on far-away pairs)
    all_bounds = [g.bounds for g in new_geoms]  # (minx, miny, maxx, maxy)

    for i in range(n):
        rank_i = eds_ord.at[i, "__rank"]
        geom_i = new_geoms[i]
        orig_area = geom_i.area
        bi = all_bounds[i]
        # Expanded bbox: any ED within tolerance of geom_i must overlap this box
        exp = (bi[0] - tolerance, bi[1] - tolerance,
               bi[2] + tolerance, bi[3] + tolerance)

        # Collect all strictly higher-tier neighbours within tolerance
        ref_parts = []
        for j in range(n):
            if j == i:
                continue
            rank_j = eds_ord.at[j, "__rank"]
            if rank_j <= rank_i:
                continue   # only snap to strictly higher-tier neighbours
                           # same-tier gaps are handled by Phase 3 gap-fill
            # Bounding-box pre-filter: skip if definitely too far
            bj = all_bounds[j]
            if bj[2] < exp[0] or bj[0] > exp[2] or bj[3] < exp[1] or bj[1] > exp[3]:
                continue
            # Exact distance check only for bbox candidates
            geom_j = new_geoms[j]
            if geom_i.distance(geom_j) < tolerance:
                ref_parts.append(geom_j)

        if not ref_parts:
            continue

        # Sequential pairwise snapping — avoids slow unary_union of all neighbours.
        # Each snap moves the ED geometry incrementally toward each higher-tier boundary.
        geom_curr = geom_i
        for ref in ref_parts:
            s = snap(geom_curr, ref, tolerance)
            if s.is_valid and not s.is_empty:
                geom_curr = s

        area_change = abs(geom_curr.area - orig_area) / orig_area if orig_area > 0 else 0
        if area_change > SNAP_AREA_WARN:
            name = eds_ord.at[i, "name_2026"] if "name_2026" in eds_ord.columns else str(i)
            print(f"  [WARN] {label}: snap reverted for {name} — area change "
                  f"{area_change*100:.1f}% > {SNAP_AREA_WARN*100:.0f}% threshold "
                  f"(possible false weld)", flush=True)
            revert_count += 1
            continue   # revert: keep original

        new_geoms[i] = geom_curr
        snap_count += 1

    eds_ord["geometry"] = new_geoms
    eds_ord = eds_ord.drop(columns=["__rank"])
    eds_ord = eds_ord.sort_values("name_2026").reset_index(drop=True)
    print(f"[{_ts()}] [{label}] Phase 2 done in {time.time()-t0:.1f}s "
          f"— {snap_count} EDs snapped, {revert_count} reverted "
          f"(tol={tolerance:.0f}m)", flush=True)
    return eds_ord


def final_precision_pass(eds: gpd.GeoDataFrame, label: str,
                         tolerance: float = 1.0) -> gpd.GeoDataFrame:
    """
    Final 1m snap pass to close floating-point artefacts left after gap-fill.
    At this point all major gaps are filled — this pass only moves vertices by
    ≤1m, ensuring shared boundaries are topologically exact (identical float
    coordinates) rather than just close. No area-change check needed since
    ≤1m displacement on provincial-scale polygons is negligible.

    Parallelised: each ED's snap result depends only on the *original* (pre-pass)
    neighbour geometries to within 1m, so we read from a snapshot and write to a
    private slot. Loses propagation that the serial version had (snap to j seeing
    j's snap to k), but at ≤1m tolerance on provincial-scale polygons this is
    negligible — the convergence is local, not global.
    """
    print(f"[{_ts()}] [{label}] Phase 4 start (1m precision pass, {WORKERS} workers)",
          flush=True)
    t_start = time.time()
    eds = eds.copy()
    geoms = [_clean(row.geometry) for _, row in eds.iterrows()]
    n = len(geoms)

    # Pre-compute bounding boxes for cheap pair pre-filter
    bounds = [g.bounds for g in geoms]

    def _snap_one(i: int):
        g = geoms[i]
        bi = bounds[i]
        # Expanded bbox to filter neighbour candidates
        exp = (bi[0] - tolerance, bi[1] - tolerance,
               bi[2] + tolerance, bi[3] + tolerance)
        for j in range(n):
            if j == i:
                continue
            bj = bounds[j]
            if bj[2] < exp[0] or bj[0] > exp[2] or bj[3] < exp[1] or bj[1] > exp[3]:
                continue
            if g.distance(geoms[j]) < tolerance:
                snapped = snap(g, geoms[j], tolerance)
                if snapped.is_valid and not snapped.is_empty:
                    g = snapped
        return i, g

    new_geoms = list(geoms)
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fut in as_completed(ex.submit(_snap_one, i) for i in range(n)):
            i, g = fut.result()
            new_geoms[i] = g

    eds["geometry"] = new_geoms
    print(f"[{_ts()}] [{label}] Phase 4 done in {time.time()-t_start:.1f}s "
          f"({WORKERS} workers, {n} EDs processed)", flush=True)
    return eds


# ---------------------------------------------------------------------------
# Phase 3 — Gap fill
# ---------------------------------------------------------------------------

def gap_fill(eds: gpd.GeoDataFrame, provincial_boundary,
             label: str) -> gpd.GeoDataFrame:
    """
    Assign gap territory to the nearest ED using GeoPandas spatial index.

    For large numbers of gap polygons (which occur when DPGs undercover ~10%
    of provincial area), boundary-intersection assignment is O(n_gaps × n_eds)
    and takes hours. Instead we use gdf.sindex.nearest() which is O(n_gaps log n_eds)
    via R-tree, dropping runtime from hours to seconds.

    For small gap counts (< 200) we still use boundary-intersection as it is
    geometrically more accurate (assigns each gap to the ED it actually shares
    a border with, not just the nearest centroid).
    """
    BOUNDARY_THRESHOLD = 200   # switch to spatial-index for large gap counts

    print(f"[{_ts()}] [{label}] Phase 3 start (gap fill)", flush=True)
    t0 = time.time()
    eds = eds.copy()
    eds_union = unary_union(eds.geometry.tolist())
    gap = provincial_boundary.difference(eds_union)

    if gap.is_empty:
        print(f"[{_ts()}] [{label}] Phase 3 done in {time.time()-t0:.1f}s "
              f"— no gaps, full coverage", flush=True)
        return eds

    gap_area_km2 = gap.area / 1e6
    if isinstance(gap, MultiPolygon):
        gap_polys = [g for g in gap.geoms if g.area > 1]
    elif isinstance(gap, Polygon):
        gap_polys = [gap] if gap.area > 1 else []
    else:
        try:
            gap_polys = [g for g in gap.geoms if g.area > 1]
        except Exception:
            gap_polys = [gap]

    print(f"  [{label}] Phase 3: {len(gap_polys)} gap polygons, "
          f"{gap_area_km2:.2f} km²", flush=True)

    if not gap_polys:
        return eds

    new_geoms = eds.geometry.tolist()

    if len(gap_polys) >= BOUNDARY_THRESHOLD:
        # Fast path: spatial index nearest-ED assignment
        # Build a GeoDataFrame of ED centroids for sindex.nearest()
        ed_gdf = eds.copy()
        ed_gdf["__idx"] = np.arange(len(eds))
        # sindex.nearest returns index of nearest geometry for each query
        gap_centroids = gpd.GeoDataFrame(
            geometry=[g.centroid for g in gap_polys], crs=eds.crs
        )
        # nearest() returns array of positional indices into ed_gdf
        nearest_idx = ed_gdf.sindex.nearest(gap_centroids.geometry)
        # nearest_idx shape may be (2, n) in newer geopandas — take the second row
        if hasattr(nearest_idx, 'shape') and nearest_idx.ndim == 2:
            nearest_idx = nearest_idx[1]

        # Batch: collect all gap polys per ED, then union once per ED
        buckets: dict[int, list] = {}
        for gap_i, ed_pos in enumerate(nearest_idx):
            ed_i = int(ed_gdf.iloc[int(ed_pos)]["__idx"])
            buckets.setdefault(ed_i, []).append(gap_polys[gap_i])

        for ed_i, polys in buckets.items():
            combined = unary_union([new_geoms[ed_i]] + polys)
            new_geoms[ed_i] = _clean(combined)

        print(f"[{_ts()}] [{label}] Phase 3 done in {time.time()-t0:.1f}s "
              f"— {len(gap_polys)} gaps ({gap_area_km2:.0f} km²) assigned "
              f"to {len(buckets)} EDs via spatial index", flush=True)

    else:
        # Accurate path: boundary-intersection assignment
        for gap_poly in gap_polys:
            best_idx, best_shared = None, 0.0
            for i, geom in enumerate(new_geoms):
                try:
                    inter = gap_poly.boundary.intersection(geom.boundary)
                    shared = inter.length if inter is not None else 0.0
                except Exception:
                    shared = 0.0
                if shared > best_shared:
                    best_shared = shared
                    best_idx = i
            if best_idx is None:
                gap_c = gap_poly.centroid
                dists = [gap_c.distance(g.centroid) for g in new_geoms]
                best_idx = int(np.argmin(dists))
            new_geoms[best_idx] = _clean(new_geoms[best_idx].union(gap_poly))
        print(f"[{_ts()}] [{label}] Phase 3 done in {time.time()-t0:.1f}s "
              f"— {len(gap_polys)} gaps ({gap_area_km2:.0f} km²) assigned "
              f"via boundary-intersection", flush=True)

    eds["geometry"] = new_geoms
    return eds


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(eds: gpd.GeoDataFrame, original: gpd.GeoDataFrame,
             provincial_boundary, label: str):
    geoms = eds.geometry.tolist()
    names = eds["name_2026"].tolist()
    n = len(geoms)

    # No-erasure
    orig_areas = {row.name_2026: row.geometry.area for _, row in original.iterrows()}
    for row in eds.itertuples():
        orig = orig_areas.get(row.name_2026, 0)
        ratio = row.geometry.area / orig if orig > 0 else 1.0
        if ratio < ANTI_ERASURE:
            print(f"  [FAIL] {label}: {row.name_2026} area ratio {ratio:.3f}")

    # No-overlap (O(n²) for n=89 is fine)
    overlap_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            inter = geoms[i].intersection(geoms[j])
            if inter.area > 1.0:
                overlap_pairs += 1
                if overlap_pairs <= 3:
                    print(f"  [WARN] {label}: residual overlap "
                          f"{names[i]} ∩ {names[j]} = {inter.area/1e6:.4f} km²")
    if overlap_pairs == 0:
        print(f"  [PASS] {label}: no overlaps", flush=True)
    else:
        print(f"  [WARN] {label}: {overlap_pairs} residual overlap pairs", flush=True)

    # Full-coverage
    eds_union = unary_union(geoms)
    residual = provincial_boundary.difference(eds_union)
    pct = (residual.area / provincial_boundary.area) * 100
    if pct > 0.001:
        print(f"  [WARN] {label}: {pct:.4f}% uncovered ({residual.area/1e6:.2f} km²)",
              flush=True)
    else:
        print(f"  [PASS] {label}: coverage gap < 0.001%", flush=True)

    # Name preservation
    if set(eds["name_2026"]) == set(original["name_2026"]):
        print(f"  [PASS] {label}: all 89 ED names preserved", flush=True)
    else:
        diff = set(eds["name_2026"]).symmetric_difference(set(original["name_2026"]))
        print(f"  [FAIL] {label}: name mismatch — {diff}", flush=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_map(v7_path: Path, v8_path: Path, provincial_boundary,
                label: str) -> gpd.GeoDataFrame:
    t0 = time.time()
    print(f"\n[{_ts()}] === {label} START ===", flush=True)
    original = gpd.read_file(v7_path)
    if original.crs.to_epsg() != 3401:
        original = original.to_crs("EPSG:3401")
    print(f"  loaded {len(original)} EDs | "
          f"canon_source: {original['canon_source'].value_counts().to_dict() if 'canon_source' in original.columns else 'N/A'}",
          flush=True)

    # Per-phase checkpoint files: write after each phase completes so a crash
    # in any later phase can resume from the last completed checkpoint instead
    # of redoing work. Slug-safe filename derived from the v8 final name.
    plan_slug = v8_path.stem.replace("v0_8_canonical_", "")
    ckpt_dir = v8_path.parent / "_perfecter_checkpoints"
    ckpt_dir.mkdir(exist_ok=True)
    ckpt = {
        1: ckpt_dir / f"{plan_slug}_phase1.gpkg",
        2: ckpt_dir / f"{plan_slug}_phase2.gpkg",
        3: ckpt_dir / f"{plan_slug}_phase3.gpkg",
    }

    def _save_ckpt(eds, phase):
        eds.to_file(ckpt[phase], driver="GPKG")
        print(f"  [checkpoint] wrote {ckpt[phase].name}", flush=True)

    # Resume detection: pick the highest-numbered checkpoint that exists.
    last_done = max((ph for ph, p in ckpt.items() if p.exists()), default=0)
    if last_done > 0:
        print(f"  [resume] phase-{last_done} checkpoint exists → "
              f"loading and continuing from phase {last_done + 1}", flush=True)
        eds = gpd.read_file(ckpt[last_done])
    else:
        eds = original.copy()

    if last_done < 1:
        eds = topology_cleanup(eds, label)
        _save_ckpt(eds, 1)
    if last_done < 2:
        eds = edge_snap(eds, label, tolerance=SNAP_TOLERANCE)
        _save_ckpt(eds, 2)
    if last_done < 3:
        eds = gap_fill(eds, provincial_boundary, label)
        _save_ckpt(eds, 3)

    eds = final_precision_pass(eds, label, tolerance=1.0)
    validate(eds, original, provincial_boundary, label)

    eds.to_file(v8_path, driver="GPKG")
    print(f"[{_ts()}] [{label}] wrote {v8_path.name}  "
          f"(plan total {time.time()-t0:.1f}s)", flush=True)

    # Clean up checkpoints once final write succeeds
    for p in ckpt.values():
        if p.exists():
            p.unlink()
    try:
        ckpt_dir.rmdir()  # only succeeds if empty
    except OSError:
        pass

    return eds


def main():
    skip_existing = "--skip-existing" in sys.argv
    t0 = time.time()
    print(f"[{_ts()}] [dpg_perfecter] v0_7 → v0_8 pipeline START", flush=True)
    print(f"  snap tolerance: {SNAP_TOLERANCE} m  |  anti-erasure: {ANTI_ERASURE*100:.0f}%  |  workers: {WORKERS}",
          flush=True)
    if skip_existing:
        print("  --skip-existing: will skip any plan whose v0_8 output already exists",
              flush=True)

    print("\nLoading VA polygons for provincial boundary...", flush=True)
    va = gpd.read_file(VA_PATH)
    if va.crs.to_epsg() != 3401:
        va = va.to_crs("EPSG:3401")
    provincial_boundary = unary_union(va.geometry.tolist())
    print(f"  provincial boundary: {provincial_boundary.area/1e9:.1f} × 10³ km²",
          flush=True)

    for v7_path, v8_path, label in [
        (MAJ_V7, MAJ_V8, "majority 2026"),
        (MIN_V7, MIN_V8, "minority 2026"),
    ]:
        if skip_existing and v8_path.exists():
            print(f"\n=== {label} === SKIPPED ({v8_path.name} already exists)", flush=True)
            continue
        process_map(v7_path, v8_path, provincial_boundary, label)

    print(f"\n[{_ts()}] [dpg_perfecter] DONE — pipeline total {time.time()-t0:.1f}s",
          flush=True)
    print(f"  outputs: {MAJ_V8.name}, {MIN_V8.name}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
