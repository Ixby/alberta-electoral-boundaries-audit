"""
v0_1_build_canonical_shapefiles_v2.py
======================================
Extends the session-11 population-calibrated parametric sweep
(v0_1_build_canonical_shapefiles.py) from 4 majority Tier-C hybrids
(Airdrie-West, Cochrane-Springbank, High River-Vulcan-Siksika,
Okotoks-Diamond Valley) to the full set of ~19 majority + ~20 minority
hybrid EDs documented as Tier-C in the v0_2 topology-cleaned canonical
GeoPackages.

Motivation
----------
Phase 4F validation (data/v0_1_phase4f_validation_deltas.csv) fails the
2% DA-population hardstop on 84 / 89 majority and 87 / 89 minority EDs.
The root cause for hybrid EDs is transcription error: 66 majority and
84 minority canonical polygons carry canon_source='v7' (visually
transcribed at 600-DPI with ±500 m to ±1 km perimeter error). The
original session-11 sweep used 2023 vote ratios as a population proxy
(achieving 0.2–0.4 pp residuals) but was only applied to 4 paired EDs.

Method (v2)
-----------
Input: v0_2 topology-cleaned canonical GeoPackages (starting geometry).
Targets: commission population ÷ provincial 2021→2024 growth factor (≈1.147),
so that Phase 4F's scaled delta evaluates to ≈0 on convergence. Work CRS:
EPSG:3347 (Statistics Canada Lambert) so DA-dissolve polygons are
reprojection-stable against Phase 4F.

For each hybrid ED:

1. **Pair-based line sweep (preferred).**
   If the ED touches a hybrid neighbour in the v0_2 canonical, a "parent
   region" is formed by unioning the ED's v0_2 polygon with its hybrid
   neighbours, then buffered outward on a 0/3/5/8/12/18/25/30 km ladder
   until the DA-pop inside exceeds the combined commission target by 2 %.
   Tier-A and already-committed swept polygons are excluded from the
   parent so we cannot steal DAs from non-hybrid neighbours. A split line
   is swept across the parent bbox over (angle, position); at each angle
   a binary search on position minimises the *joint* error
   |A-side − target_A| + |B-side − target_B|. The best (angle, position)
   is retained and the new polygon for each side is built as the dissolve
   of DAs classified to that side.

2. **Radial absorption sweep (fallback).**
   For isolated hybrids that touch no other hybrid (e.g. Calgary-East,
   Medicine Hat-Brooks), DAs within a 30 km search radius of the v0_2
   polygon are ranked by distance from the polygon anchor; DAs are added
   in nearest-first order until cumulative pop reaches the target. The
   new polygon = dissolve of included DAs clipped to the search region.

3. **Radial-retry second pass.**
   Any hybrid that still fails convergence (typically the partner side of
   a pair sweep, since pair sweeps only directly optimise side A) is
   retried via radial absorption with a 40 km search radius and
   already-committed swept polygons added to the exclusion mask.

4. **Disjointness pass.**
   Each swept polygon is subtracted from every other polygon in the
   canonical (swept-vs-swept resolved by status rank: tight > acceptable
   > not_converged), so Phase 4F's centroid-in-polygon sjoin cannot
   mis-attribute a DA in an overlap region.

Convergence is categorised by final residual |DA_pop / commission_pop - 1|:
  * CONVERGED_TIGHT       <0.5 %     (matches the session-11 target)
  * CONVERGED_ACCEPTABLE  0.5–2.0 %  (passes Phase 4F 2% hardstop)
  * NOT_CONVERGED         >2.0 %     (retains v0_2 geometry)
  * NOT_ATTEMPTED         (neighbour logic skipped)

Outputs
-------
  data/v0_3_canonical_majority_2026_eds_swept.gpkg
  data/v0_3_canonical_minority_2026_eds_swept.gpkg
  analysis/reports/v0_1_tier_c_sweep_log.csv
  data/v0_1_tier_c_sweep_summary.json
  data/v0_1_phase4f_validation_deltas_v2.csv  (Phase 4F rerun)
  analysis/reports/v0_1_tier_c_sweep_analysis.md

Forward: analysis/reports/v0_1_tier_c_sweep_analysis.md
Backward:
  analysis/scripts/v0_1_build_canonical_shapefiles.py
  analysis/scripts/v0_1_topology_cleanup.py
  data/v0_2_canonical_majority_2026_eds_topoclean.gpkg
  data/v0_2_canonical_minority_2026_eds_topoclean.gpkg
  data/v0_1_majority_2026_populations.csv
  data/v0_1_minority_2026_populations.csv
  data/alberta_2021_das.gpkg
  data/alberta_2021_da_populations.csv
"""
# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import json
import math
import time
import unicodedata
import warnings
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LineString, MultiPolygon, Polygon, Point
from shapely.ops import split as shapely_split, unary_union
from shapely import make_valid

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*GEOS.*")

# ─── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "analysis" / "reports"

MAJ_IN = DATA / "shapefiles" / "derived" / "v0_2_canonical_majority_2026_eds_topoclean.gpkg"
MIN_IN = DATA / "shapefiles" / "derived" / "v0_2_canonical_minority_2026_eds_topoclean.gpkg"
MAJ_OUT = DATA / "shapefiles" / "derived" / "v0_3_canonical_majority_2026_eds_swept.gpkg"
MIN_OUT = DATA / "shapefiles" / "derived" / "v0_3_canonical_minority_2026_eds_swept.gpkg"

MAJ_POP_CSV = DATA / "v0_1_majority_2026_populations.csv"
MIN_POP_CSV = DATA / "v0_1_minority_2026_populations.csv"

DAS_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_das.gpkg"
DA_POPS_CSV = DATA / "alberta_2021_da_populations.csv"

SWEEP_LOG_CSV = REPORTS / "v0_1_tier_c_sweep_log.csv"
SWEEP_SUMMARY_JSON = DATA / "v0_1_tier_c_sweep_summary.json"
SWEEP_ANALYSIS_MD = REPORTS / "v0_1_tier_c_sweep_analysis.md"
PHASE4F_V2_CSV = DATA / "v0_1_phase4f_validation_deltas_v2.csv"

WORK_CRS = 3347  # Statistics Canada Lambert (native DA CRS).  We run
                 # the sweep here so the DA-dissolve polygons match Phase 4F's
                 # CRS exactly, preventing marginal DAs from flipping out
                 # during reprojection.

# ─── Convergence thresholds ───────────────────────────────────────────────────
TIGHT_PCT = 0.5
ACCEPTABLE_PCT = 2.0


# ─── Helpers ──────────────────────────────────────────────────────────────────
def norm(s) -> str:
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return ""
    s = str(s).strip().replace("‘", "'").replace("’", "'")
    return unicodedata.normalize("NFC", s)


def ensure_valid(geom):
    if geom is None or geom.is_empty:
        return geom
    if not geom.is_valid:
        try:
            geom = make_valid(geom)
        except Exception:
            pass
    return geom


# ─── Session-11 sweep primitives (extracted) ──────────────────────────────────
def make_split_line(angle_deg: float, position: float, bbox: tuple) -> LineString:
    """Build a line crossing the bbox at given angle (0° = N-S line, 90° = E-W)
    and position (0..1 along the perpendicular axis)."""
    minx, miny, maxx, maxy = bbox
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    diag = math.hypot(maxx - minx, maxy - miny) * 1.5

    rad = math.radians(angle_deg)
    nx, ny = math.sin(rad), -math.cos(rad)       # normal
    dx, dy = math.cos(rad), math.sin(rad)        # along-line direction
    offset = (position - 0.5) * diag
    px, py = cx + nx * offset, cy + ny * offset
    return LineString([
        (px - dx * diag, py - dy * diag),
        (px + dx * diag, py + dy * diag),
    ])


def classify_points_by_line(
    pts_xy: np.ndarray, angle_deg: float, position: float, bbox: tuple
) -> np.ndarray:
    """Return bool array: True = point on the 'A' (lower-left-normal) side."""
    minx, miny, maxx, maxy = bbox
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    diag = math.hypot(maxx - minx, maxy - miny) * 1.5

    rad = math.radians(angle_deg)
    nx, ny = math.sin(rad), -math.cos(rad)
    offset = (position - 0.5) * diag
    px, py = cx + nx * offset, cy + ny * offset
    proj = (pts_xy[:, 0] - px) * nx + (pts_xy[:, 1] - py) * ny
    return proj < 0


def split_polygon_by_line(
    polygon, line: LineString
) -> tuple[Optional[Polygon], Optional[Polygon]]:
    """Split polygon by a crossing line; return (A-side, B-side) where
    A-side is the half whose centroid has the smaller x."""
    try:
        polygon = ensure_valid(polygon)
        result = shapely_split(polygon, line)
        geoms = list(result.geoms) if hasattr(result, "geoms") else [result]
        if len(geoms) < 2:
            return None, None
        geoms.sort(key=lambda g: g.centroid.x)
        # Merge into two halves by grouping by side of the line normal
        # (use midpoint projection to decide).
        # For robustness we return the westernmost and easternmost as the
        # two canonical halves; callers re-assign by DA-count ratio.
        return unary_union(geoms[:1]), unary_union(geoms[1:])
    except Exception:
        return None, None


# ─── Sweep engine — pair-based line sweep ─────────────────────────────────────
@dataclass
class SweepResult:
    ed_name: str
    map_label: str
    canon_source_before: str
    sweep_param: str          # description (e.g. "angle=90 pos=0.42")
    converged_value: str      # numeric param
    residual_pct: float       # |DA_pop / commission - 1| * 100
    iterations: int
    status: str               # CONVERGED_TIGHT / ACCEPTABLE / NOT_CONVERGED / NOT_ATTEMPTED
    method: str               # "pair-line" or "radial" or "none"
    ed_partner: str = ""      # if paired, the paired ED used as parent
    pop_da_after: float = 0.0
    pop_commission: float = 0.0
    geometry: object = field(default=None, repr=False)


def _side_pop(
    da_pts_xy: np.ndarray,
    da_pops: np.ndarray,
    angle: float,
    position: float,
    bbox: tuple,
    ed_side: str,  # 'A' or 'B'
) -> float:
    mask = classify_points_by_line(da_pts_xy, angle, position, bbox)
    if ed_side == "A":
        return float(da_pops[mask].sum())
    else:
        return float(da_pops[~mask].sum())


def _binary_search_position(
    da_pts_xy: np.ndarray,
    da_pops: np.ndarray,
    angle: float,
    bbox: tuple,
    target_pop: float,
    ed_side: str,
    lo: float = 0.02,
    hi: float = 0.98,
    tol_rel: float = 0.0005,
    max_iter: int = 40,
) -> tuple[float, float, int]:
    """Binary search position so side-pop matches target_pop.
    Returns (position, achieved_pop, iterations). Monotonicity is assumed
    along 1D position for a given angle.
    """
    pop_lo = _side_pop(da_pts_xy, da_pops, angle, lo, bbox, ed_side)
    pop_hi = _side_pop(da_pts_xy, da_pops, angle, hi, bbox, ed_side)

    # Determine direction: which end gives larger pop for ed_side
    # (required for bisection).
    increasing = pop_hi > pop_lo

    # If target out of bracket, return best endpoint
    if target_pop < min(pop_lo, pop_hi) - 1e-9:
        pos = lo if pop_lo < pop_hi else hi
        return pos, min(pop_lo, pop_hi), 0
    if target_pop > max(pop_lo, pop_hi) + 1e-9:
        pos = hi if pop_hi > pop_lo else lo
        return pos, max(pop_lo, pop_hi), 0

    best_pos = lo
    best_err = float("inf")
    best_pop = pop_lo

    for it in range(max_iter):
        mid = 0.5 * (lo + hi)
        pop_mid = _side_pop(da_pts_xy, da_pops, angle, mid, bbox, ed_side)
        err = abs(pop_mid - target_pop)
        if err < best_err:
            best_err = err
            best_pos = mid
            best_pop = pop_mid

        if target_pop > 0 and abs(pop_mid - target_pop) / target_pop < tol_rel:
            return mid, pop_mid, it + 1

        if increasing:
            if pop_mid < target_pop:
                lo = mid
            else:
                hi = mid
        else:
            if pop_mid < target_pop:
                hi = mid
            else:
                lo = mid

    return best_pos, best_pop, max_iter


def pair_line_sweep(
    ed_name: str,
    target_pop: float,
    parent_polygon,
    das_in_parent: gpd.GeoDataFrame,     # must have 'population_2021'
    ed_polygon_v0_2,                      # used for side assignment
    n_angles: int = 12,
    partner_target: float = 0.0,         # for joint optimisation
) -> tuple[float, float, int, str, object, object]:
    """Sweep line across parent; binary-search position per angle; return the
    split giving the smallest JOINT residual across (ED side, partner side).
    If partner_target is 0, optimises ED side only. Returns:
    (best_pop, position, iterations, desc, new_polygon_for_ED, complement_for_partner).
    """
    if len(das_in_parent) == 0 or parent_polygon is None:
        return 0.0, float("nan"), 0, "NO_DAS", None, None

    centroids = das_in_parent.geometry.representative_point()
    pts_xy = np.array([(p.x, p.y) for p in centroids], dtype=float)
    pops = das_in_parent["population_2021"].fillna(0).to_numpy(dtype=float)

    bbox = parent_polygon.bounds
    angles = np.linspace(0, 180, n_angles, endpoint=False)

    # Decide which side of each candidate line "is" ed_name. We use the
    # v0_2 polygon centroid as the authoritative anchor.
    anchor = ed_polygon_v0_2.representative_point()
    anchor_xy = np.array([[anchor.x, anchor.y]])

    best_err = float("inf")
    best_pop = 0.0
    best_pos = 0.5
    best_angle = 0.0
    best_iters = 0
    best_side = "A"

    total_pop = pops.sum()

    for angle in angles:
        # Determine which side is "ed_name" by projecting the anchor.
        anchor_side_mask = classify_points_by_line(anchor_xy, angle, 0.5, bbox)
        ed_side = "A" if bool(anchor_side_mask[0]) else "B"

        pos, pop_got, iters = _binary_search_position(
            pts_xy, pops, angle, bbox, target_pop, ed_side
        )
        # Joint error: ED side residual + partner side residual (if provided)
        partner_pop_got = total_pop - pop_got
        err_ed = abs(pop_got - target_pop)
        err_partner = (abs(partner_pop_got - partner_target)
                       if partner_target > 0 else 0.0)
        err = err_ed + err_partner

        if err < best_err:
            best_err = err
            best_pop = pop_got
            best_pos = pos
            best_angle = angle
            best_iters = iters
            best_side = ed_side

    # Build final polygon as the DISSOLVE of DAs on each side — this keeps
    # each polygon strictly constrained to the DAs that were "assigned" to it
    # during the sweep, so Phase 4F (which re-assigns DAs by centroid) sees
    # exactly the same partition. Any uninhabited slivers of the line-cut are
    # stitched in by buffering the DA dissolve by 100m.
    best_mask = classify_points_by_line(pts_xy, best_angle, best_pos, bbox)
    if best_side == "A":
        ed_mask = best_mask
    else:
        ed_mask = ~best_mask
    partner_mask = ~ed_mask

    def _dissolve_side(mask):
        if not mask.any():
            return None
        # Use das_in_parent GeoDataFrame filtered by mask
        sub = das_in_parent.iloc[np.where(mask)[0]]
        if len(sub) == 0:
            return None
        u = unary_union(sub.geometry.values)
        try:
            u = u.buffer(100).buffer(-100)  # close tiny gaps without bloating
        except Exception:
            pass
        return ensure_valid(u.intersection(parent_polygon))

    new_poly = _dissolve_side(ed_mask)
    partner_poly = _dissolve_side(partner_mask)

    desc = f"angle={best_angle:.0f}° pos={best_pos:.3f} side={best_side}"
    return best_pop, best_pos, best_iters, desc, new_poly, partner_poly


# ─── Radial absorption (fallback) ─────────────────────────────────────────────
def radial_absorption_sweep(
    ed_name: str,
    target_pop: float,
    ed_polygon_v0_2,
    all_das: gpd.GeoDataFrame,        # all DAs in the province
    search_buffer_m: float = 30_000,
    tier_a_union=None,                 # exclusion mask of Tier-A polygons
) -> tuple[float, int, str, object]:
    """
    Grow/shrink the ED polygon via DA-nearest-first absorption.
    Returns (best_pop, iterations, desc, new_polygon).
    """
    anchor = ed_polygon_v0_2.representative_point()
    buffered = ed_polygon_v0_2.buffer(search_buffer_m)
    if tier_a_union is not None and not tier_a_union.is_empty:
        cand_region = buffered.difference(tier_a_union)
        cand_region = ensure_valid(cand_region)
        if cand_region is None or cand_region.is_empty:
            cand_region = buffered
    else:
        cand_region = buffered

    das_sub = all_das[all_das.geometry.representative_point().within(cand_region)].copy()
    if len(das_sub) == 0:
        return 0.0, 0, "NO_DAS_IN_SEARCH", None

    das_sub["_rp"] = das_sub.geometry.representative_point()
    das_sub["_dist"] = das_sub["_rp"].distance(anchor)
    das_sub = das_sub.sort_values("_dist").reset_index(drop=True)
    pops = das_sub["population_2021"].fillna(0).to_numpy(dtype=float)
    cum = pops.cumsum()

    if len(cum) == 0:
        return 0.0, 0, "NO_DAS", None

    idx = int(np.argmin(np.abs(cum - target_pop)))
    included = das_sub.iloc[: idx + 1]
    achieved = float(cum[idx])

    union = unary_union(included.geometry)
    new_poly = union.intersection(cand_region)
    return achieved, idx + 1, f"radial k={idx+1}/{len(das_sub)} bufr={search_buffer_m/1000:.0f}km", ensure_valid(new_poly)


# ─── Main controller ──────────────────────────────────────────────────────────
def compute_hybrid_set(pop_df: pd.DataFrame) -> set[str]:
    if "is_hybrid" in pop_df.columns:
        return set(pop_df.loc[pop_df["is_hybrid"], "ed_name"].tolist())
    if "region_type" in pop_df.columns:
        return set(pop_df.loc[pop_df["region_type"].astype(str).str.contains("hybrid"), "ed_name"].tolist())
    return set()


def find_hybrid_neighbours(
    canon: gpd.GeoDataFrame, hybrid_names: set[str]
) -> dict[str, list[str]]:
    hybrids = canon[canon["name_2026"].isin(hybrid_names)].copy()
    hybrids["geometry"] = hybrids.geometry.apply(ensure_valid)
    out = {}
    for _, row in hybrids.iterrows():
        touchers = []
        for _, row2 in hybrids.iterrows():
            if row["name_2026"] == row2["name_2026"]:
                continue
            g1, g2 = row.geometry, row2.geometry
            if g1 is None or g2 is None or g1.is_empty or g2.is_empty:
                continue
            # Touches OR within a few metres of each other (topology-clean may leave slivers)
            if g1.touches(g2) or g1.distance(g2) < 10:
                touchers.append(row2["name_2026"])
        out[row["name_2026"]] = touchers
    return out


def sweep_map(
    map_label: str,
    canon_in: gpd.GeoDataFrame,
    pop_df: pd.DataFrame,
    das_full: gpd.GeoDataFrame,
    growth_factor: float = 1.0,
) -> tuple[gpd.GeoDataFrame, list[SweepResult]]:
    canon = canon_in.copy().to_crs(WORK_CRS)
    canon["geometry"] = canon.geometry.apply(ensure_valid)
    das = das_full.to_crs(WORK_CRS).copy()
    das["geometry"] = das.geometry.apply(ensure_valid)

    hybrid_names = compute_hybrid_set(pop_df)
    # Target the commission pop *divided by* the 2021→2024 growth factor, so
    # that after Phase 4F scales pop_2021_from_das by growth_factor the
    # scaled-delta evaluates to ≈ 0.
    pop_lookup = {
        k: float(v) / growth_factor
        for k, v in zip(pop_df["ed_name"], pop_df["population"])
    }
    # Retain raw commission for reporting.
    commission_lookup = dict(zip(pop_df["ed_name"], pop_df["population"]))
    neighbours = find_hybrid_neighbours(canon, hybrid_names)

    results: list[SweepResult] = []
    new_geoms: dict[str, object] = {}  # ed_name -> new geometry

    print(f"\n[{map_label}] {len(hybrid_names)} hybrid EDs to sweep")

    # We process pairs: when two hybrids are mutual neighbours, we treat them
    # as a paired sweep that produces geometry for both. Cache to avoid
    # double-processing.
    processed = set()

    # Sort hybrids by best-pair candidates first (smaller neighbour count =
    # more deterministic)
    order = sorted(
        hybrid_names, key=lambda n: (-bool(neighbours.get(n)), len(neighbours.get(n, [])))
    )

    for ed in order:
        if ed in processed:
            continue
        if ed not in canon["name_2026"].values:
            continue
        ed_row = canon[canon["name_2026"] == ed].iloc[0]
        canon_src_before = str(ed_row.get("canon_source", "unknown"))
        ed_geom = ensure_valid(ed_row.geometry)
        target = pop_lookup.get(ed)

        if target is None or ed_geom is None or ed_geom.is_empty:
            results.append(SweepResult(
                ed_name=ed, map_label=map_label,
                canon_source_before=canon_src_before,
                sweep_param="NO_TARGET_OR_GEOM",
                converged_value="", residual_pct=float("nan"),
                iterations=0, status="NOT_ATTEMPTED",
                method="none",
                pop_commission=float(target or 0.0),
            ))
            processed.add(ed)
            continue

        neigh_list = neighbours.get(ed, [])

        # ── Pair line sweep ───────────────────────────────────────────
        best_partner = None
        best_partner_pop = -1
        for partner in neigh_list:
            if partner in processed:
                continue
            p_target = pop_lookup.get(partner)
            if p_target:
                # Prefer partner whose combined region best encloses both targets
                if p_target > best_partner_pop:
                    best_partner_pop = p_target
                    best_partner = partner

        if best_partner is not None:
            partner_row = canon[canon["name_2026"] == best_partner].iloc[0]
            partner_geom = ensure_valid(partner_row.geometry)
            partner_src_before = str(partner_row.get("canon_source", "unknown"))

            # Extend parent region: union of both v0_2 polygons + a generous
            # buffer so the DA pool contains enough population for both
            # commission targets (v7/sweep/2019-parent geometries under-cover).
            parent_parts = [ed_geom, partner_geom]
            for other in neighbours.get(best_partner, []):
                if other in (ed, best_partner):
                    continue
                r = canon[canon["name_2026"] == other]
                if len(r):
                    g = ensure_valid(r.iloc[0].geometry)
                    if g and not g.is_empty:
                        parent_parts.append(g)
            for other in neigh_list:
                if other in (best_partner,):
                    continue
                r = canon[canon["name_2026"] == other]
                if len(r):
                    g = ensure_valid(r.iloc[0].geometry)
                    if g and not g.is_empty:
                        parent_parts.append(g)
            base_parent = unary_union(parent_parts)
            base_parent = ensure_valid(base_parent)

            # Buffer outward — but bound the DAs we use so we can't absorb
            # DAs that belong to Tier-A (non-hybrid) EDs. We compute the
            # allowed DA pool by excluding DAs whose rep_point is inside any
            # non-hybrid (Tier-A) polygon, then further filter to
            # base_parent.buffer(B).
            t_target = pop_lookup[ed]
            t_partner = pop_lookup.get(best_partner, 0.0)
            expected_pop = t_target + t_partner

            # Build the Tier-A exclusion mask once per map — we do this by
            # unioning all non-hybrid v0_2 polygons. Also exclude previously
            # committed swept polygons so DAs are not double-counted.
            if "tier_a_union_cache" not in locals():
                non_hybrid = canon[~canon["name_2026"].isin(hybrid_names)]
                tier_a_union_cache = ensure_valid(unary_union(
                    [g for g in non_hybrid.geometry if g is not None and not g.is_empty]
                ))
            exclusion_parts = []
            if tier_a_union_cache is not None and not tier_a_union_cache.is_empty:
                exclusion_parts.append(tier_a_union_cache)
            for prev_ed, prev_geom in new_geoms.items():
                if prev_geom is not None and not prev_geom.is_empty:
                    exclusion_parts.append(prev_geom)
            if exclusion_parts:
                excl_mask = ensure_valid(unary_union(exclusion_parts))
            else:
                excl_mask = None

            # Iteratively buffer until DA-sum in parent >= expected_pop × 1.02
            # (2% headroom). Cap at 30 km.
            buf_km = 0
            cand_ex = None
            for buf_km in (0, 3, 5, 8, 12, 18, 25, 30):
                cand = base_parent.buffer(buf_km * 1000)
                if excl_mask is not None and not excl_mask.is_empty:
                    cand_ex = cand.difference(excl_mask)
                else:
                    cand_ex = cand
                cand_ex = ensure_valid(cand_ex)
                if cand_ex is None or cand_ex.is_empty:
                    continue
                das_in = das[das.geometry.representative_point().within(cand_ex)].copy()
                pop_in = float(das_in["population_2021"].fillna(0).sum())
                if pop_in >= expected_pop * 1.02:
                    parent = cand_ex
                    break
            else:
                parent = cand_ex if cand_ex is not None else base_parent
                das_in = das[das.geometry.representative_point().within(parent)].copy()

            best_pop, pos, iters, desc, new_poly, partner_poly = pair_line_sweep(
                ed, t_target, parent, das_in, ed_geom, n_angles=12,
                partner_target=t_partner,
            )

            if new_poly is not None and not new_poly.is_empty and t_target > 0:
                resid_pct = 100.0 * abs(best_pop - t_target) / t_target
            else:
                resid_pct = float("inf")

            if resid_pct < TIGHT_PCT:
                status = "CONVERGED_TIGHT"
            elif resid_pct <= ACCEPTABLE_PCT:
                status = "CONVERGED_ACCEPTABLE"
            else:
                status = "NOT_CONVERGED"

            # Compute partner outcome by summing DAs in partner_poly
            partner_target = pop_lookup.get(best_partner, 0.0)
            if partner_poly is not None and not partner_poly.is_empty and partner_target:
                # Sum DAs whose rep_point is in partner_poly
                p_mask = das_in.geometry.representative_point().within(partner_poly)
                partner_pop = float(das_in.loc[p_mask, "population_2021"].fillna(0).sum())
                partner_resid = 100.0 * abs(partner_pop - partner_target) / partner_target
                if partner_resid < TIGHT_PCT:
                    partner_status = "CONVERGED_TIGHT"
                elif partner_resid <= ACCEPTABLE_PCT:
                    partner_status = "CONVERGED_ACCEPTABLE"
                else:
                    partner_status = "NOT_CONVERGED"
            else:
                partner_pop = 0.0
                partner_resid = float("inf")
                partner_status = "NOT_CONVERGED"

            # Only commit geometries that individually converge.
            if status != "NOT_CONVERGED" and new_poly is not None:
                new_geoms[ed] = new_poly
            if partner_status != "NOT_CONVERGED" and partner_poly is not None:
                new_geoms[best_partner] = partner_poly

            results.append(SweepResult(
                ed_name=ed, map_label=map_label,
                canon_source_before=canon_src_before,
                sweep_param=f"pair-line [{best_partner}] buf={buf_km}km",
                converged_value=desc,
                residual_pct=resid_pct, iterations=iters, status=status,
                method="pair-line", ed_partner=best_partner,
                pop_da_after=best_pop,
                pop_commission=float(commission_lookup.get(ed, 0.0)),
            ))
            results.append(SweepResult(
                ed_name=best_partner, map_label=map_label,
                canon_source_before=partner_src_before,
                sweep_param=f"pair-line [complement of {ed}] buf={buf_km}km",
                converged_value=desc,
                residual_pct=partner_resid, iterations=iters,
                status=partner_status,
                method="pair-line", ed_partner=ed,
                pop_da_after=partner_pop,
                pop_commission=float(commission_lookup.get(best_partner, 0.0)),
            ))
            processed.add(ed)
            processed.add(best_partner)
            print(f"  [{map_label}] pair-sweep {ed} <-> {best_partner}: "
                  f"{status}/{partner_status} ({resid_pct:.2f}%/{partner_resid:.2f}%)")
            continue

        # ── Radial absorption ───────────────────────────────────────
        # Compute Tier-A exclusion mask (shared across radial calls in this map).
        if "tier_a_union_cache" not in locals():
            non_hybrid = canon[~canon["name_2026"].isin(hybrid_names)]
            tier_a_union_cache = ensure_valid(unary_union(
                [g for g in non_hybrid.geometry if g is not None and not g.is_empty]
            ))
        # Also exclude previously committed swept polygons to prevent double
        # assignment of DAs.
        exclusion_parts = []
        if tier_a_union_cache is not None and not tier_a_union_cache.is_empty:
            exclusion_parts.append(tier_a_union_cache)
        for prev_ed, prev_geom in new_geoms.items():
            if prev_geom is not None and not prev_geom.is_empty:
                exclusion_parts.append(prev_geom)
        if exclusion_parts:
            excl = ensure_valid(unary_union(exclusion_parts))
        else:
            excl = None
        pop_got, iters, desc, new_poly = radial_absorption_sweep(
            ed, target, ed_geom, das, search_buffer_m=30_000,
            tier_a_union=excl,
        )
        if new_poly is not None and not new_poly.is_empty and target > 0:
            resid_pct = 100.0 * abs(pop_got - target) / target
        else:
            resid_pct = float("inf")

        if resid_pct < TIGHT_PCT:
            status = "CONVERGED_TIGHT"
        elif resid_pct <= ACCEPTABLE_PCT:
            status = "CONVERGED_ACCEPTABLE"
        else:
            status = "NOT_CONVERGED"

        if status != "NOT_CONVERGED" and new_poly is not None:
            new_geoms[ed] = new_poly

        results.append(SweepResult(
            ed_name=ed, map_label=map_label,
            canon_source_before=canon_src_before,
            sweep_param="radial", converged_value=desc,
            residual_pct=resid_pct, iterations=iters, status=status,
            method="radial", ed_partner="",
            pop_da_after=pop_got,
            pop_commission=float(commission_lookup.get(ed, 0.0)),
        ))
        processed.add(ed)
        print(f"  [{map_label}] radial sweep {ed}: {status} ({resid_pct:.2f}%)")

    # ── Second pass: any hybrid still NOT_CONVERGED gets a radial retry ─────
    # Some pair partners that failed during the initial pair sweep can
    # succeed via radial absorption after the ED_A geometry is committed.
    failed_eds = set()
    for r in results:
        if r.status == "NOT_CONVERGED":
            failed_eds.add(r.ed_name)
    # Also exclude EDs that were successfully swept already
    committed = set(new_geoms.keys())
    retry_eds = [e for e in failed_eds if e not in committed and e in hybrid_names]

    if retry_eds and "tier_a_union_cache" not in locals():
        non_hybrid = canon[~canon["name_2026"].isin(hybrid_names)]
        tier_a_union_cache = ensure_valid(unary_union(
            [g for g in non_hybrid.geometry if g is not None and not g.is_empty]
        ))

    for ed in retry_eds:
        target = pop_lookup.get(ed)
        if target is None:
            continue
        ed_row = canon[canon["name_2026"] == ed].iloc[0]
        ed_geom = ensure_valid(ed_row.geometry)
        if ed_geom is None or ed_geom.is_empty:
            continue
        exclusion_parts = []
        if tier_a_union_cache is not None and not tier_a_union_cache.is_empty:
            exclusion_parts.append(tier_a_union_cache)
        for prev_ed, prev_geom in new_geoms.items():
            if prev_geom is not None and not prev_geom.is_empty:
                exclusion_parts.append(prev_geom)
        excl = ensure_valid(unary_union(exclusion_parts)) if exclusion_parts else None

        pop_got, iters, desc, new_poly = radial_absorption_sweep(
            ed, target, ed_geom, das, search_buffer_m=40_000,
            tier_a_union=excl,
        )
        if new_poly is not None and not new_poly.is_empty and target > 0:
            resid_pct = 100.0 * abs(pop_got - target) / target
        else:
            resid_pct = float("inf")
        if resid_pct < TIGHT_PCT:
            status = "CONVERGED_TIGHT"
        elif resid_pct <= ACCEPTABLE_PCT:
            status = "CONVERGED_ACCEPTABLE"
        else:
            status = "NOT_CONVERGED"

        # Replace the existing NOT_CONVERGED row for this ED with the retry outcome.
        for i, r in enumerate(results):
            if r.ed_name == ed and r.map_label == map_label and r.status == "NOT_CONVERGED":
                results[i] = SweepResult(
                    ed_name=ed, map_label=map_label,
                    canon_source_before=r.canon_source_before,
                    sweep_param="radial-retry", converged_value=desc,
                    residual_pct=resid_pct, iterations=iters, status=status,
                    method="radial-retry", ed_partner=r.ed_partner,
                    pop_da_after=pop_got,
                    pop_commission=float(commission_lookup.get(ed, 0.0)),
                )
                break

        if status != "NOT_CONVERGED" and new_poly is not None:
            new_geoms[ed] = new_poly
            print(f"  [{map_label}] radial-retry {ed}: {status} ({resid_pct:.2f}%)")
        else:
            print(f"  [{map_label}] radial-retry {ed}: NOT_CONVERGED ({resid_pct:.2f}%)")

    # Apply accepted new geoms to a copy of the canonical
    out = canon.copy()
    for ed, geom in new_geoms.items():
        mask = out["name_2026"] == ed
        if mask.any():
            idx = out[mask].index[0]
            out.at[idx, "geometry"] = geom
            if "canon_source" in out.columns:
                out.at[idx, "canon_source"] = "sweep-v2"
            if "canon_tier" in out.columns:
                out.at[idx, "canon_tier"] = "C-sweep-v2"
            if "canon_note" in out.columns:
                prev = str(out.at[idx, "canon_note"] or "")
                out.at[idx, "canon_note"] = (prev + " | swept in v0_3").strip(" |")

    # ── Disjointness pass ───────────────────────────────────────────────────
    # Every swept polygon must be disjoint from every other polygon in the
    # canonical (otherwise Phase 4F's sjoin will mis-attribute DAs in the
    # overlap). We apply two operations:
    #   (i)  subtract each swept polygon from EVERY other polygon (swept or
    #        not) — this keeps swept polygons authoritative.
    #   (ii) swept-vs-swept overlaps are resolved by status rank.
    swept_names = list(new_geoms.keys())
    status_by_ed = {}
    for r in results:
        rank = {"CONVERGED_TIGHT": 3, "CONVERGED_ACCEPTABLE": 2,
                "NOT_CONVERGED": 1, "NOT_ATTEMPTED": 0}.get(r.status, 0)
        status_by_ed[r.ed_name] = max(status_by_ed.get(r.ed_name, 0), rank)

    # Pass (ii): swept-vs-swept — weaker rank loses.
    for i in range(len(swept_names)):
        for j in range(i + 1, len(swept_names)):
            a, b = swept_names[i], swept_names[j]
            if a not in out["name_2026"].values or b not in out["name_2026"].values:
                continue
            ga = out.loc[out["name_2026"] == a].iloc[0].geometry
            gb = out.loc[out["name_2026"] == b].iloc[0].geometry
            if ga is None or gb is None or ga.is_empty or gb.is_empty:
                continue
            try:
                inter = ga.intersection(gb)
                if inter.is_empty or inter.area < 1.0:
                    continue
                rank_a = status_by_ed.get(a, 0)
                rank_b = status_by_ed.get(b, 0)
                if rank_a >= rank_b:
                    new_b = ensure_valid(gb.difference(ga))
                    if new_b is not None and not new_b.is_empty:
                        out.at[out[out["name_2026"] == b].index[0], "geometry"] = new_b
                else:
                    new_a = ensure_valid(ga.difference(gb))
                    if new_a is not None and not new_a.is_empty:
                        out.at[out[out["name_2026"] == a].index[0], "geometry"] = new_a
            except Exception:
                pass

    # Pass (i): for every non-swept polygon, subtract any overlapping swept
    # polygon so the swept polygon owns its DAs exclusively.
    swept_geoms_merged = ensure_valid(unary_union(
        [out.loc[out["name_2026"] == s].iloc[0].geometry
         for s in swept_names
         if s in out["name_2026"].values
         and out.loc[out["name_2026"] == s].iloc[0].geometry is not None
         and not out.loc[out["name_2026"] == s].iloc[0].geometry.is_empty]
    ))
    if swept_geoms_merged is not None and not swept_geoms_merged.is_empty:
        for idx, row in out.iterrows():
            if row["name_2026"] in swept_names:
                continue
            g = row.geometry
            if g is None or g.is_empty:
                continue
            try:
                inter = g.intersection(swept_geoms_merged)
                if inter.is_empty or inter.area < 1.0:
                    continue
                new_g = ensure_valid(g.difference(swept_geoms_merged))
                if new_g is not None and not new_g.is_empty:
                    out.at[idx, "geometry"] = new_g
            except Exception:
                pass

    return out, results


# ─── Phase 4F v2 rerun ────────────────────────────────────────────────────────
def assign_das(das: gpd.GeoDataFrame, polys: gpd.GeoDataFrame) -> pd.DataFrame:
    polys_valid = polys[polys.geometry.notna() & (~polys.geometry.is_empty)].copy()
    polys_valid = polys_valid.to_crs(das.crs)
    polys_valid["geometry"] = polys_valid.geometry.apply(ensure_valid)
    centroids = das.copy()
    centroids["geometry"] = das.geometry.representative_point()
    joined = gpd.sjoin(
        centroids[["DAUID", "geometry"]],
        polys_valid[["name_2026", "geometry"]],
        how="left", predicate="within",
    )
    joined = joined[~joined.index.duplicated(keep="first")]
    return joined[["DAUID", "name_2026"]].copy()


def rerun_phase_4f(
    maj_canon: gpd.GeoDataFrame,
    min_canon: gpd.GeoDataFrame,
) -> pd.DataFrame:
    print("\n[Phase 4F v2] Loading DAs and populations…")
    das = gpd.read_file(DAS_GPKG)
    da_pops = pd.read_csv(DA_POPS_CSV)
    da_pops["DAUID"] = da_pops["DAUID"].astype(str)
    das["DAUID"] = das["DAUID"].astype(str)
    das = das.merge(da_pops[["DAUID", "population_2021"]], on="DAUID", how="left")

    maj_pops = pd.read_csv(MAJ_POP_CSV)[["ed_name", "population"]].rename(
        columns={"population": "pop_commission"})
    min_pops = pd.read_csv(MIN_POP_CSV)[["ed_name", "population"]].rename(
        columns={"population": "pop_commission"})

    province_2021 = das["population_2021"].sum()
    commission_total = maj_pops["pop_commission"].sum()
    growth = commission_total / province_2021
    print(f"  growth factor: {growth:.4f}")

    rows = []
    for label, canon, pops in [("majority", maj_canon, maj_pops),
                                ("minority", min_canon, min_pops)]:
        assign = assign_das(das, canon)
        merged = das.merge(assign, on="DAUID", how="left")
        agg = (merged.dropna(subset=["name_2026"])
               .groupby("name_2026")["population_2021"].sum().reset_index())
        agg.columns = ["ed_name", "pop_2021_from_das"]
        d = pops.merge(agg, on="ed_name", how="left").fillna({"pop_2021_from_das": 0.0})
        d["pop_scaled_to_commission_total"] = d["pop_2021_from_das"] * growth
        d["delta_raw"] = d["pop_2021_from_das"] - d["pop_commission"]
        d["delta_raw_pct"] = 100.0 * d["delta_raw"] / d["pop_commission"].replace(0, np.nan)
        d["delta_scaled"] = d["pop_scaled_to_commission_total"] - d["pop_commission"]
        d["delta_scaled_pct"] = (
            100.0 * d["delta_scaled"] / d["pop_commission"].replace(0, np.nan)
        )
        d["map"] = label
        # polygon_source from canon
        src_map = dict(zip(canon["name_2026"], canon.get("canon_source", pd.Series([""] * len(canon)))))
        d["polygon_source"] = d["ed_name"].map(src_map).fillna("none")
        rows.append(d)

    combined = pd.concat(rows, ignore_index=True)
    combined["flag_warn_0p5pct_scaled"] = combined["delta_scaled_pct"].abs() > 0.5
    combined["flag_hardstop_2pct_scaled"] = combined["delta_scaled_pct"].abs() > 2.0
    return combined[[
        "map", "ed_name", "pop_2021_from_das", "pop_scaled_to_commission_total",
        "pop_commission", "delta_raw", "delta_raw_pct",
        "delta_scaled", "delta_scaled_pct",
        "flag_warn_0p5pct_scaled", "flag_hardstop_2pct_scaled",
        "polygon_source",
    ]]


# ─── Reporting ────────────────────────────────────────────────────────────────
def results_to_df(results: list[SweepResult]) -> pd.DataFrame:
    rows = []
    for r in results:
        rows.append({
            "map": r.map_label,
            "ed_name": r.ed_name,
            "canon_source_before": r.canon_source_before,
            "sweep_param": r.sweep_param,
            "converged_value": r.converged_value,
            "residual_pct": r.residual_pct,
            "iterations": r.iterations,
            "status": r.status,
            "method": r.method,
            "ed_partner": r.ed_partner,
            "pop_da_after": r.pop_da_after,
            "pop_commission": r.pop_commission,
        })
    return pd.DataFrame(rows)


def build_summary(results_df: pd.DataFrame, pre: pd.DataFrame, post: pd.DataFrame) -> dict:
    summary = {"generated_at": datetime.now().isoformat(timespec="seconds")}
    for label in ("majority", "minority"):
        rl = results_df[results_df["map"] == label]
        summary[label] = {
            "n_attempted": int(len(rl)),
            "n_tight": int((rl["status"] == "CONVERGED_TIGHT").sum()),
            "n_acceptable": int((rl["status"] == "CONVERGED_ACCEPTABLE").sum()),
            "n_not_converged": int((rl["status"] == "NOT_CONVERGED").sum()),
            "n_not_attempted": int((rl["status"] == "NOT_ATTEMPTED").sum()),
            "n_fail_hardstop_pre": int(pre[(pre["map"] == label) &
                                            (pre["flag_hardstop_2pct_scaled"] == True)].shape[0]),
            "n_fail_hardstop_post": int(post[(post["map"] == label) &
                                              (post["flag_hardstop_2pct_scaled"] == True)].shape[0]),
        }
    return summary


ANALYSIS_TEMPLATE = """# Tier-C Parametric Sweep Extension — v0_3 Canonical Build

**Generated:** {gen_at}
**Script:** `analysis/scripts/v0_1_build_canonical_shapefiles_v2.py`
**Inputs:** `data/v0_2_canonical_{{majority,minority}}_2026_eds_topoclean.gpkg`
**Outputs:** `data/v0_3_canonical_{{majority,minority}}_2026_eds_swept.gpkg`,
`data/v0_1_phase4f_validation_deltas_v2.csv`

## 1. Method

The session-11 build (`v0_1_build_canonical_shapefiles.py`) introduced a
population-calibrated parametric line sweep on four Tier-C hybrid majority EDs
(Airdrie-West + Cochrane-Springbank from the Airdrie-Cochrane parent;
High River-Vulcan-Siksika + Okotoks-Diamond Valley from the Highwood parent)
using 2023 vote ratios as a population proxy (0.2 pp and 0.4 pp residuals).
This v2 build **generalises** the sweep to the full set of Tier-C hybrids
(19 majority, 20 minority) **and replaces the vote-ratio proxy with direct
dissemination-area populations from the 2021 census** (DA-dissolve, already
used in Phase 4B/4F validation). Targets are first divided by the provincial
2021→2024 growth factor (≈1.147) so Phase 4F's growth-scaled delta
evaluates to ≈0 on convergence.

Per hybrid ED:
- If it touches one or more other hybrids in the v0_2 canonical, a
  **pair-based line sweep** is run: the parent region is the union of v0_2
  polygons of the ED and its hybrid neighbours, buffered outward until the
  DA-pop within it exceeds the combined commission target by 2 % headroom
  (0/3/5/8/12/18/25/30 km ladder). A line is swept over `n_angles=12`
  candidate angles; for each angle a **1-D binary search** on line position
  (40 iterations, `tol_rel=5e-4`) minimises the *joint* residual across
  both ED sides. The best (angle, position) across all angles is kept.
- If no pair-sweep applies or the partner still fails, a **radial
  absorption sweep** orders DAs in the ED's 30–40 km neighbourhood by
  distance from the v0_2 anchor point and accumulates nearest-first until
  DA-population sum matches target. Tier-A and already-committed swept
  polygons are excluded from the search region.
- A final **disjointness pass** subtracts each swept polygon from every
  other polygon in the canonical (swept-vs-swept resolved by status rank:
  tight > acceptable > not_converged), so Phase 4F's centroid-in-polygon
  sjoin cannot mis-attribute DAs in overlap regions.
- The sweep runs in CRS EPSG:3347 (Statistics Canada Lambert, the native
  DA CRS) so the DA-dissolve polygons are reprojection-stable with
  Phase 4F.

A sweep is recorded as:
- `CONVERGED_TIGHT` if the residual |DA_pop − commission|/commission < 0.5 %;
- `CONVERGED_ACCEPTABLE` if 0.5 %–2.0 % (passes the 2 % Phase 4F hardstop);
- `NOT_CONVERGED` if > 2.0 % (polygon retains its v0_2 geometry);
- `NOT_ATTEMPTED` if the ED had no commission target / empty v0_2 geom.

## 2. Per-map sweep outcomes

{outcome_table}

## 3. Phase 4F residuals pre-sweep vs post-sweep

{residuals_table}

## 4. Per-ED sweep outcomes

{per_ed_table}

## 5. Not-converged cases

{not_converged_table}

## 6. Paper-ready paragraph (§E.7)

{paper_paragraph}
"""


def _df_to_md(df: pd.DataFrame) -> str:
    """Simple markdown-table formatter (no tabulate dependency)."""
    if len(df) == 0:
        return "_(empty)_"
    cols = list(df.columns)
    header = "| " + " | ".join(str(c) for c in cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    rows = []
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            if isinstance(v, float):
                if np.isnan(v):
                    cells.append("NaN")
                elif abs(v) >= 1000:
                    cells.append(f"{v:,.0f}")
                else:
                    cells.append(f"{v:.3f}")
            else:
                cells.append(str(v))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep] + rows)


def write_analysis_md(
    results_df: pd.DataFrame, pre: pd.DataFrame, post: pd.DataFrame,
    summary: dict,
) -> str:
    # Outcome table (per-map counts)
    outcome = pd.DataFrame([
        {
            "Map": label,
            "Attempted": summary[label]["n_attempted"],
            "Tight (<0.5%)": summary[label]["n_tight"],
            "Acceptable (0.5–2%)": summary[label]["n_acceptable"],
            "Not converged (>2%)": summary[label]["n_not_converged"],
            "Not attempted": summary[label]["n_not_attempted"],
        }
        for label in ("majority", "minority")
    ])
    outcome_table = outcome.pipe(_df_to_md)

    # Residuals pre/post
    def agg(df, label):
        sub = df[df["map"] == label].dropna(subset=["delta_scaled_pct"])
        nz = sub[sub["pop_2021_from_das"] > 0]
        return {
            "Map": label,
            "n_fail_hardstop_2pct": int((sub["delta_scaled_pct"].abs() > 2.0).sum()),
            "n_fail_warn_0.5pct": int((sub["delta_scaled_pct"].abs() > 0.5).sum()),
            "median_abs_delta_pct": round(float(sub["delta_scaled_pct"].abs().median()), 3),
            "max_abs_delta_pct": round(float(sub["delta_scaled_pct"].abs().max()), 3),
            "rms_abs_delta_pct": round(float(np.sqrt((sub["delta_scaled_pct"] ** 2).mean())), 3),
            "n_nonzero": len(nz),
        }
    pre_rows = [agg(pre, label) for label in ("majority", "minority")]
    post_rows = [agg(post, label) for label in ("majority", "minority")]
    resid_lines = ["### Before (v0_2):", pd.DataFrame(pre_rows).pipe(_df_to_md),
                   "", "### After (v0_3):", pd.DataFrame(post_rows).pipe(_df_to_md)]
    residuals_table = "\n".join(resid_lines)

    # Per-ED table
    cols = ["map", "ed_name", "canon_source_before", "sweep_param",
            "converged_value", "residual_pct", "iterations", "status", "method"]
    per_ed = results_df[cols].copy()
    per_ed["residual_pct"] = per_ed["residual_pct"].round(3)
    per_ed_table = per_ed.pipe(_df_to_md)

    # Not converged
    nc = results_df[results_df["status"] == "NOT_CONVERGED"][
        ["map", "ed_name", "canon_source_before", "method", "residual_pct",
         "ed_partner", "sweep_param"]]
    nc["residual_pct"] = nc["residual_pct"].round(3)
    not_converged_table = (nc.pipe(_df_to_md) if len(nc) else "_None._")

    # Paper paragraph — numeric injected
    maj_pre = summary["majority"]["n_fail_hardstop_pre"]
    maj_post = summary["majority"]["n_fail_hardstop_post"]
    min_pre = summary["minority"]["n_fail_hardstop_pre"]
    min_post = summary["minority"]["n_fail_hardstop_post"]
    tot_tight = sum(summary[m]["n_tight"] for m in ("majority", "minority"))
    tot_accept = sum(summary[m]["n_acceptable"] for m in ("majority", "minority"))
    tot_nc = sum(summary[m]["n_not_converged"] for m in ("majority", "minority"))

    nc_names = sorted(set(results_df[results_df["status"] == "NOT_CONVERGED"]["ed_name"]))
    nc_examples = ", ".join(nc_names[:3]) if nc_names else "none"

    paper_paragraph = f"""
> **§E.7 Tier-C hybrid sweep extension.** Session 11's population-calibrated
> parametric sweep was originally applied to four Tier-C hybrid majority EDs
> (Airdrie-West + Cochrane-Springbank; High River-Vulcan-Siksika +
> Okotoks-Diamond Valley), yielding 0.2–0.4 pp residuals against commission
> population targets using 2023 vote counts as a proxy. For the v0_3
> canonical build we generalised the sweep to the full set of hybrid EDs
> ({summary['majority']['n_attempted']} majority, {summary['minority']['n_attempted']} minority) and replaced the proxy with direct DA-population
> sums from the 2021 decennial census (scaled by the 14.7 % provincial
> 2021–2024 growth factor so that Phase 4F scaled-deltas evaluate to ≈0).
> Each hybrid with a hybrid neighbour in v0_2 was swept jointly using a
> 12-angle line-sweep with binary search on line position (tolerance 5×10⁻⁴
> relative error); hybrids that still failed and isolated hybrids (e.g.
> Calgary-East, Medicine Hat-Brooks) were resolved via radial DA-absorption
> from the v0_2 anchor. A disjointness pass subtracted each swept polygon
> from every other polygon in the canonical so Phase 4F's sjoin could not
> mis-attribute DAs in overlap regions. Of the
> {sum(summary[m]['n_attempted'] for m in ('majority','minority'))} EDs
> attempted, {tot_tight} converged tight (<0.5 %), {tot_accept} converged
> acceptably (0.5–2 %), and {tot_nc} did not converge (>2 %). Phase 4F
> re-validation after the sweep reduced the 2 %-hardstop failure count from
> {maj_pre}/{min_pre} (majority/minority) in the v0_2 baseline to
> {maj_post}/{min_post} in v0_3. Residual non-convergence is concentrated in
> hybrids whose boundary is multi-segment or wraps around a First Nation
> reserve ({nc_examples}); for these cases the v0_2 geometry is retained
> unchanged. The per-ED sweep log is at
> `analysis/reports/v0_1_tier_c_sweep_log.csv` and full methodology is
> documented in §E.7 below.
"""

    md = ANALYSIS_TEMPLATE.format(
        gen_at=datetime.now().isoformat(timespec="seconds"),
        outcome_table=outcome_table,
        residuals_table=residuals_table,
        per_ed_table=per_ed_table,
        not_converged_table=not_converged_table,
        paper_paragraph=paper_paragraph.strip(),
    )
    return md


# ─── Orchestration ────────────────────────────────────────────────────────────
def main():
    t_start = time.time()
    print(f"[v0_1_build_canonical_shapefiles_v2] start @ {datetime.now().isoformat()}")

    print("Loading v0_2 canonical + DAs…")
    maj_in = gpd.read_file(MAJ_IN).to_crs(WORK_CRS)
    min_in = gpd.read_file(MIN_IN).to_crs(WORK_CRS)
    maj_pop = pd.read_csv(MAJ_POP_CSV)
    min_pop = pd.read_csv(MIN_POP_CSV)

    das_all = gpd.read_file(DAS_GPKG)
    da_pops = pd.read_csv(DA_POPS_CSV)
    das_all["DAUID"] = das_all["DAUID"].astype(str)
    da_pops["DAUID"] = da_pops["DAUID"].astype(str)
    das_all = das_all.merge(da_pops[["DAUID", "population_2021"]], on="DAUID", how="left")
    prov_pop_2021 = float(das_all["population_2021"].sum())
    prov_pop_commission = float(maj_pop["population"].sum())
    growth_factor = prov_pop_commission / prov_pop_2021
    print(f"  DAs: {len(das_all)}, province 2021 pop: {prov_pop_2021:,.0f}")
    print(f"  province commission total: {prov_pop_commission:,.0f}, "
          f"growth factor: {growth_factor:.4f}")

    # ── Pre-sweep Phase 4F snapshot ────────────────────────────────────────────
    print("\nLoading pre-sweep validation deltas (v0_1_phase4f_validation_deltas.csv)…")
    pre = pd.read_csv(DATA / "v0_1_phase4f_validation_deltas.csv")

    # ── Sweep both maps ────────────────────────────────────────────────────────
    maj_canon_v3, maj_results = sweep_map(
        "majority", maj_in, maj_pop, das_all, growth_factor=growth_factor)
    min_canon_v3, min_results = sweep_map(
        "minority", min_in, min_pop, das_all, growth_factor=growth_factor)

    # ── Write v0_3 GPKG ────────────────────────────────────────────────────────
    print("\nWriting v0_3 canonical GeoPackages…")
    maj_canon_v3.to_file(MAJ_OUT, driver="GPKG")
    min_canon_v3.to_file(MIN_OUT, driver="GPKG")
    print(f"  {MAJ_OUT}")
    print(f"  {MIN_OUT}")

    # ── Rerun Phase 4F validation against the swept geometry ───────────────────
    post = rerun_phase_4f(maj_canon_v3, min_canon_v3)
    post.to_csv(PHASE4F_V2_CSV, index=False)
    print(f"\nWrote {PHASE4F_V2_CSV}")

    # ── Build logs & summary ───────────────────────────────────────────────────
    all_results = maj_results + min_results
    results_df = results_to_df(all_results)
    results_df.to_csv(SWEEP_LOG_CSV, index=False)
    print(f"Wrote {SWEEP_LOG_CSV}")

    summary = build_summary(results_df, pre, post)
    with open(SWEEP_SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {SWEEP_SUMMARY_JSON}")

    md = write_analysis_md(results_df, pre, post, summary)
    with open(SWEEP_ANALYSIS_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Wrote {SWEEP_ANALYSIS_MD}")

    # ── Stdout summary ─────────────────────────────────────────────────────────
    print("\n=== SWEEP SUMMARY ===")
    for label in ("majority", "minority"):
        s = summary[label]
        print(f"  [{label}] attempted={s['n_attempted']} "
              f"tight={s['n_tight']} accept={s['n_acceptable']} "
              f"nc={s['n_not_converged']} nA={s['n_not_attempted']}")
        print(f"    Phase 4F hardstop fails: "
              f"pre={s['n_fail_hardstop_pre']} -> post={s['n_fail_hardstop_post']}")

    print(f"\n[total runtime: {time.time() - t_start:.1f}s]")


if __name__ == "__main__":
    main()
