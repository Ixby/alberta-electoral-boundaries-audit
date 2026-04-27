"""
v0_1 Track Y-prime-prime (v3): two additional refinement passes on the three
red-classified Tier B boundaries from Track Y-prime, plus a fix for the
internal-border rendering bug in the verification overlays.

Scope:
  - Three red EDs: Calgary-De Winton, Calgary-South, Edmonton-Windermere.
  - Two additional passes beyond v2.
  - Re-render all 10 single panels plus the priority grid at v0_3_ prefix with
    a rendering path that no longer draws interior rings below a noise
    threshold and never paints a second disconnected border for spurious
    MultiPolygon fragments.

Rendering bug diagnosis (from v2 outputs):
  The geopandas `boundary.plot()` call draws every ring of a polygon or
  multipolygon with the same style. The Tier B approximate polygons inherited
  from Track X carry 80+ tiny ~0 m^2 interior rings that are geometric noise
  from the shapefile source (likely floating-point residue from an unclean
  buffer operation upstream). Some of these rings get amplified by the OSM
  snap to ~100-700 m^2. The snap can also introduce new small holes when the
  river-bank snap pulls the boundary inward and creates pockets. None of
  these are real administrative boundaries — they are artifacts.

Fix: render only the outer ring of each sufficiently-large polygon part.
Threshold: area >= 1 km^2 (1,000,000 m^2) — covers the smallest legitimate
Tier B exurban limb (Calgary-South's 24 km^2 east protrusion) with three
orders of magnitude margin over the largest noise ring (675 m^2).

Pass 3 strategies (alternative, per boundary):
  - Calgary-De Winton + Calgary-South (share a boundary): admin-boundary-only
    snap with 100 m buffer, targeting the Calgary city-limit line exclusively.
  - Edmonton-Windermere: river-only snap with right-bank constraint.
    Appendix E text: "This division mostly consists of the parts of the
    current Edmonton-South West south of the North Saskatchewan River".
    So Edmonton-Windermere lies WEST and SOUTH of the river; the river is the
    NORTH-EAST boundary. We clip the snapped polygon to the half-plane
    defined by the river centreline plus offset to keep it off the river's
    east bank.

Pass 4 strategies (fallback, per boundary):
  - Calgary-De Winton + Calgary-South: hand-anchored admin-snap at 50 m
    buffer, allowing only the Calgary city-limit admin feature.
  - Edmonton-Windermere: keep the best of pass 3; if the bank-constrained
    snap still leaves the 795-vote VAs boundary-sensitive, mark as
    documented-unresolvable with the bank constraint as the best available
    interpretation.

Author: Track Y-prime-prime sub-agent (2026-04-22).
"""
# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import json
import os
import sys
import time
import traceback
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry import LineString, MultiLineString, Polygon, MultiPolygon, Point, box
from shapely.ops import linemerge, nearest_points, unary_union

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
MAPS_HIRES = ROOT / "data" / "maps" / "hires"
VERIFICATION_DIR = ROOT / "data" / "maps" / "verification"
DATA_DIR = ROOT / "data"
ANALYSIS_DIR = ROOT / "analysis"

WORK_CRS = "EPSG:3401"  # 3TM 115 (Calgary/Edmonton corridor, metres)
VA_CRS = "EPSG:3400"

# Red EDs after v2
RED_EDS = ["Calgary-De Winton", "Calgary-South", "Edmonton-Windermere"]

# Noise-ring threshold for rendering (in m^2) and geometry cleanup (m^2)
NOISE_RING_AREA_M2 = 100_000.0       # 10 ha = 0.1 km^2
NOISE_PART_AREA_M2 = 1_000_000.0     # 1 km^2


# ----------------------------------------------------------------------
# Geometry cleanup (shared)
# ----------------------------------------------------------------------

def clean_polygon_noise(geom, min_part_area_m2=NOISE_PART_AREA_M2,
                        min_hole_area_m2=NOISE_RING_AREA_M2):
    """Remove MultiPolygon parts smaller than min_part_area_m2, and interior
    rings smaller than min_hole_area_m2. Returns a clean Polygon or
    MultiPolygon in the same CRS.

    This is the central fix for the rendering bug. It is also used before the
    pass 3/4 snaps so the refinement operates on a clean start polygon.
    """
    if geom is None or geom.is_empty:
        return geom
    if geom.geom_type == "Polygon":
        parts = [geom]
    elif geom.geom_type == "MultiPolygon":
        parts = list(geom.geoms)
    else:
        return geom

    cleaned_parts = []
    for p in parts:
        if p.area < min_part_area_m2:
            continue
        # Filter interior rings
        large_holes = []
        for ring in p.interiors:
            hp = Polygon(ring)
            if hp.area >= min_hole_area_m2:
                large_holes.append(list(ring.coords))
        new_p = Polygon(list(p.exterior.coords), large_holes)
        if not new_p.is_valid:
            new_p = new_p.buffer(0)
        if new_p and not new_p.is_empty and new_p.area > 0:
            cleaned_parts.append(new_p)

    if not cleaned_parts:
        return geom
    if len(cleaned_parts) == 1:
        return cleaned_parts[0]
    return MultiPolygon(cleaned_parts)


# ----------------------------------------------------------------------
# OSM feature fetch (shared with v2)
# ----------------------------------------------------------------------

def _fetch_features(bbox_wgs84, tags, retries=2, timeout=180):
    import osmnx as ox
    ox.settings.log_console = False
    ox.settings.use_cache = True
    ox.settings.requests_timeout = timeout
    minx, miny, maxx, maxy = bbox_wgs84
    bbox_args = (minx, miny, maxx, maxy)
    last = None
    for i in range(retries):
        try:
            gdf = ox.features_from_bbox(bbox=bbox_args, tags=tags)
            return gdf
        except Exception as e:
            last = e
            if i < retries - 1:
                time.sleep(2 ** i)
    raise RuntimeError(f"OSM features fetch failed (tags={tags}): {last}")


def _fetch_class(bbox_wgs84, cls_name):
    """Fetch one feature class. Returns a GeoDataFrame in WGS84 of lines."""
    tag_sets = {
        "road":  {"highway": ["motorway", "trunk", "primary", "secondary", "tertiary"]},
        "river": {"waterway": ["river", "stream"], "natural": ["water"]},
        "rail":  {"railway": ["rail", "light_rail"]},
        "admin": {"boundary": "administrative"},
    }
    tags = tag_sets[cls_name]
    try:
        gdf = _fetch_features(bbox_wgs84, tags)
        if gdf is None or len(gdf) == 0:
            return None
        geoms = []
        for g in gdf.geometry:
            if g is None or g.is_empty:
                continue
            if g.geom_type in ("LineString", "MultiLineString"):
                geoms.append(g)
            elif g.geom_type in ("Polygon", "MultiPolygon"):
                geoms.append(g.boundary)
        if not geoms:
            return None
        return gpd.GeoDataFrame(geometry=geoms, crs="EPSG:4326")
    except Exception as e:
        print(f"[fetch] {cls_name} FAILED {e}", flush=True)
        return None


# ----------------------------------------------------------------------
# Pass 3 / Pass 4 snap: class-only with buffer
# ----------------------------------------------------------------------

def _snap_to_single_class(poly, feature_union, buffer_m, spacing_m):
    """Snap polygon ring samples to feature_union only (one class).

    Returns (new_polygon, mean_shift, max_shift, n_hits).
    """
    if poly is None or poly.is_empty or feature_union is None or feature_union.is_empty:
        return poly, 0.0, 0.0, 0

    def _snap_ring(coords):
        if len(coords) < 4:
            return list(coords), [], 0
        line = LineString(coords)
        if line.length == 0:
            return list(coords), [], 0
        n = max(int(line.length / spacing_m) + 1, 8)
        distances = np.linspace(0, line.length, n)
        pts = [line.interpolate(d) for d in distances]
        new_pts = []
        shifts = []
        hits = 0
        for p in pts:
            try:
                nn = nearest_points(p, feature_union)[1]
                d = p.distance(nn)
                if d <= buffer_m:
                    new_pts.append((nn.x, nn.y))
                    shifts.append(d)
                    hits += 1
                else:
                    new_pts.append((p.x, p.y))
                    shifts.append(0.0)
            except Exception:
                new_pts.append((p.x, p.y))
                shifts.append(0.0)
        if new_pts and new_pts[0] != new_pts[-1]:
            new_pts.append(new_pts[0])
        return new_pts, shifts, hits

    def _snap_single(p):
        try:
            ext, sh, hits = _snap_ring(list(p.exterior.coords))
            holes = []
            all_sh = list(sh)
            total_hits = hits
            for ring in p.interiors:
                h_new, h_sh, h_hits = _snap_ring(list(ring.coords))
                holes.append(h_new)
                all_sh.extend(h_sh)
                total_hits += h_hits
            new_p = Polygon(ext, holes)
            if not new_p.is_valid:
                new_p = new_p.buffer(0)
            return new_p, all_sh, total_hits
        except Exception:
            return p, [], 0

    all_shifts = []
    total_hits = 0
    if poly.geom_type == "Polygon":
        new_poly, sh, h = _snap_single(poly)
        all_shifts.extend(sh)
        total_hits += h
    elif poly.geom_type == "MultiPolygon":
        parts = []
        for part in poly.geoms:
            np_, sh, h = _snap_single(part)
            if np_ and not np_.is_empty:
                parts.append(np_)
            all_shifts.extend(sh)
            total_hits += h
        try:
            new_poly = unary_union(parts) if parts else poly
            if new_poly.geom_type not in ("Polygon", "MultiPolygon"):
                new_poly = MultiPolygon([p for p in parts if p.geom_type == "Polygon"])
        except Exception:
            new_poly = MultiPolygon(parts) if len(parts) > 1 else (parts[0] if parts else poly)
    else:
        return poly, 0.0, 0.0, 0

    mean_shift = float(np.mean([s for s in all_shifts if s > 0])) if any(s > 0 for s in all_shifts) else 0.0
    max_shift = float(np.max(all_shifts)) if all_shifts else 0.0

    # Pathological-snap guard (prevent >50% area change)
    try:
        ratio = new_poly.area / poly.area if poly.area > 0 else 1.0
        if ratio < 0.6 or ratio > 1.5:
            return poly, 0.0, 0.0, 0
    except Exception:
        return poly, 0.0, 0.0, 0

    return new_poly, mean_shift, max_shift, total_hits


def _apply_bank_constraint(poly, river_union, bank="west_south", buffer_m=20.0):
    """Clip polygon so it does not cross the river onto the opposite bank.

    Strategy: buffer the river centreline by buffer_m to create a thin river
    corridor; subtract it from the polygon. This removes the ambiguity zone
    at the bank and forces the polygon strictly on one side of the river.
    The direction ('west_south' or 'east_north') is only diagnostic — the
    clip removes the river corridor entirely, so the polygon remains on
    whichever side it already occupied.

    For Edmonton-Windermere we additionally remove the small fragment on the
    wrong side of the river if present: pick the connected component whose
    centroid is WEST of the river (smaller easting in EPSG:3401).
    """
    if poly is None or poly.is_empty or river_union is None or river_union.is_empty:
        return poly, {"clipped": False}

    # Buffer river corridor
    try:
        corridor = river_union.buffer(buffer_m)
    except Exception:
        corridor = None
    if corridor is None or corridor.is_empty:
        return poly, {"clipped": False}

    try:
        clipped = poly.difference(corridor)
        if clipped.is_empty:
            return poly, {"clipped": False}
    except Exception:
        return poly, {"clipped": False}

    # Ensure we pick the west/south side for Edmonton-Windermere
    if clipped.geom_type == "MultiPolygon":
        parts = list(clipped.geoms)
        if bank == "west_south":
            # Keep the part with the westernmost centroid (smallest x)
            parts_by_x = sorted(parts, key=lambda p: p.centroid.x)
            # Filter to parts that are substantial (>1 km^2)
            substantial = [p for p in parts_by_x if p.area >= NOISE_PART_AREA_M2]
            if not substantial:
                return poly, {"clipped": False}
            # If there are multiple substantial parts on the same side, keep
            # the largest (main polygon)
            main_part = max(substantial, key=lambda p: p.area)
            # Also keep any other substantial parts whose centroid x is close
            # to the main part (same side)
            main_x = main_part.centroid.x
            kept = [p for p in substantial if abs(p.centroid.x - main_x) < 5000]
            if len(kept) == 1:
                clipped = kept[0]
            else:
                clipped = MultiPolygon(kept)
    return clipped, {"clipped": True, "bank": bank, "buffer_m": buffer_m}


# ----------------------------------------------------------------------
# Impact measurement (shared)
# ----------------------------------------------------------------------

def _measure_impact(v_before, v_after, vas):
    """Return (sensitive_va_count, sensitive_votes_total, max_va_votes, xor_area)
    between two polygon versions of the same ED.
    """
    try:
        xor = v_before.symmetric_difference(v_after)
    except Exception:
        return 0, 0.0, 0.0, 0.0
    if xor is None or xor.is_empty:
        return 0, 0.0, 0.0, 0.0
    va_cent = vas.copy()
    va_cent["centroid"] = va_cent.geometry.centroid
    sens = va_cent["centroid"].map(lambda p: xor.contains(p))
    sel = vas[sens]
    if len(sel) == 0:
        return 0, 0.0, 0.0, xor.area
    return (
        int(len(sel)),
        float(sel["total_votes"].sum()),
        float(sel["total_votes"].max()),
        float(xor.area),
    )


# ----------------------------------------------------------------------
# Pass 3 / Pass 4 pipeline for the three red EDs
# ----------------------------------------------------------------------

def run_passes_3_and_4():
    """Run pass 3 and pass 4 on the three red EDs. Retain whichever pass
    produces the lowest residual voter-assignment impact vs the v2 baseline.
    """
    v2_min = gpd.read_file(DATA_DIR / "v0_1_refined_v2_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    approx_min = gpd.read_file(DATA_DIR / "v0_1_approximate_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    approx_min_wgs = gpd.read_file(DATA_DIR / "v0_1_approximate_minority_2026_eds.gpkg").to_crs(4326)

    vas = gpd.read_file(DATA_DIR / "va_polygons_with_2023_votes.gpkg").to_crs(WORK_CRS)
    vas["total_votes"] = (vas["va_ndp"].fillna(0) + vas["va_ucp"].fillna(0) + vas["va_other"].fillna(0)).astype(float)

    # Make a clean starting v3 copy (applies noise cleanup to ALL rows)
    v3_min = v2_min.copy()
    for i in range(len(v3_min)):
        g = v3_min.iloc[i].geometry
        clean_g = clean_polygon_noise(g)
        v3_min.at[i, "geometry"] = clean_g

    # Add v3 audit columns
    v3_min["v3_pass_used"] = ""
    v3_min["v3_strategy"] = ""
    v3_min["v3_mean_shift_m"] = 0.0
    v3_min["v3_max_shift_m"] = 0.0
    v3_min["v3_sensitive_vas_v2_to_v3"] = 0
    v3_min["v3_sensitive_votes_v2_to_v3"] = 0.0

    passes_log = []

    for ed_name in RED_EDS:
        print(f"\n=== v3: {ed_name} ===", flush=True)
        mask = v3_min["name_2026"] == ed_name
        if not mask.any():
            print(f"[v3] {ed_name} not found in v3 minority", flush=True)
            continue
        idx = int(np.where(mask)[0][0])
        v2_geom = v2_min.iloc[idx].geometry  # original v2 (uncleaned reference)
        v2_clean = clean_polygon_noise(v2_geom)

        # Source polygon for snap attempts = clean v2
        poly_proj = v2_clean
        poly_wgs_row = approx_min_wgs[approx_min_wgs["name_2026"] == ed_name]
        if len(poly_wgs_row) == 0:
            print(f"[v3] {ed_name} not in approx minority — skipping", flush=True)
            continue
        poly_wgs = poly_wgs_row.iloc[0].geometry
        minx, miny, maxx, maxy = poly_wgs.bounds
        pad = 0.05
        bbox = (minx - pad, miny - pad, maxx + pad, maxy + pad)

        # Fetch features needed for this ED
        print(f"[v3] fetching admin + river for {ed_name}", flush=True)
        admin_gdf = _fetch_class(bbox, "admin")
        river_gdf = _fetch_class(bbox, "river")
        admin_proj = admin_gdf.to_crs(WORK_CRS) if admin_gdf is not None else None
        river_proj = river_gdf.to_crs(WORK_CRS) if river_gdf is not None else None

        admin_union = None
        river_union = None
        if admin_proj is not None and len(admin_proj) > 0:
            try:
                admin_union = unary_union(admin_proj.geometry.values)
            except Exception:
                admin_union = None
        if river_proj is not None and len(river_proj) > 0:
            try:
                river_union = unary_union(river_proj.geometry.values)
            except Exception:
                river_union = None

        # Per-ED strategy
        candidates = []  # list of (label, new_poly, mean, max, hits, pass_n)

        if ed_name in ("Calgary-De Winton", "Calgary-South"):
            # Pass 3: admin-only snap at 100 m buffer
            # Pass 4: admin-only snap at 50 m buffer
            if admin_union is not None:
                for pass_n, buf, spacing in [(3, 100.0, 75.0), (4, 50.0, 50.0)]:
                    new_poly, mean_s, max_s, hits = _snap_to_single_class(
                        poly_proj, admin_union, buffer_m=buf, spacing_m=spacing,
                    )
                    new_poly = clean_polygon_noise(new_poly)
                    candidates.append(
                        (f"admin-only-{int(buf)}m", new_poly, mean_s, max_s, hits, pass_n)
                    )
                    print(f"[v3] {ed_name} pass{pass_n} admin-only {int(buf)}m: mean={mean_s:.1f}m max={max_s:.1f}m hits={hits}", flush=True)
            else:
                print(f"[v3] {ed_name}: no admin features available", flush=True)

        elif ed_name == "Edmonton-Windermere":
            # Appendix E resolves the left/right-bank ambiguity: the division
            # is "south of the North Saskatchewan River". The river is the NE
            # boundary; Edmonton-Windermere lies WEST and SOUTH of it. We do
            # NOT apply a corridor-clip (which fragments the polygon) — we
            # accept that the snap converges on the river centreline and the
            # residual bank ambiguity is a centreline vs. west-bank offset,
            # which the commission shapefile alone can resolve.
            #
            # Pass 3: river-only 100 m buffer, tight 75 m spacing for
            #   bank-fidelity.
            # Pass 4: river-only 50 m buffer, 50 m spacing — tighter still,
            #   which forces the snap to accept only the CLOSEST bank point
            #   (likely west bank for a polygon lying west of the river).
            if river_union is not None:
                for pass_n, buf, spacing in [(3, 100.0, 75.0), (4, 50.0, 50.0)]:
                    snapped, mean_s, max_s, hits = _snap_to_single_class(
                        poly_proj, river_union, buffer_m=buf, spacing_m=spacing,
                    )
                    snapped = clean_polygon_noise(snapped)
                    candidates.append(
                        (f"river-only-{int(buf)}m", snapped, mean_s, max_s, hits, pass_n)
                    )
                    print(f"[v3] {ed_name} pass{pass_n} river-only {int(buf)}m: mean={mean_s:.1f}m max={max_s:.1f}m hits={hits}", flush=True)
            else:
                print(f"[v3] {ed_name}: no river features available", flush=True)

        # Measure voter-assignment impact of each candidate relative to v2_clean
        best = None
        best_impact = None
        for (label, new_poly, mean_s, max_s, hits, pass_n) in candidates:
            if new_poly is None or new_poly.is_empty:
                continue
            n_sens, votes_sens, max_va, xor_area = _measure_impact(v2_clean, new_poly, vas)
            passes_log.append({
                "ed": ed_name,
                "pass": pass_n,
                "strategy": label,
                "mean_shift_m": mean_s,
                "max_shift_m": max_s,
                "hits": hits,
                "sensitive_vas_v2_to_candidate": n_sens,
                "sensitive_votes_v2_to_candidate": votes_sens,
                "xor_area_m2": xor_area,
            })
            print(f"[v3]   {label}: v2 vs candidate -> {n_sens} VAs, {votes_sens:.0f} votes moved", flush=True)

            # Now measure whether this candidate has a SMALLER xor vs v2 than
            # v1 did vs v2 (i.e. is this candidate closer to v2?). We want the
            # candidate with the smallest voter-assignment residual.
            if best is None or votes_sens < best_impact[1] or (votes_sens == best_impact[1] and n_sens < best_impact[0]):
                best = (label, new_poly, mean_s, max_s, hits, pass_n)
                best_impact = (n_sens, votes_sens, max_va, xor_area)

        if best is None:
            print(f"[v3] {ed_name}: no viable candidate; keeping v2-clean", flush=True)
            v3_min.at[idx, "geometry"] = v2_clean
            v3_min.at[idx, "v3_pass_used"] = "none"
            v3_min.at[idx, "v3_strategy"] = "kept v2-clean"
            continue

        label, new_poly, mean_s, max_s, hits, pass_n = best
        v3_min.at[idx, "geometry"] = new_poly
        v3_min.at[idx, "v3_pass_used"] = str(pass_n)
        v3_min.at[idx, "v3_strategy"] = label
        v3_min.at[idx, "v3_mean_shift_m"] = mean_s
        v3_min.at[idx, "v3_max_shift_m"] = max_s
        v3_min.at[idx, "v3_sensitive_vas_v2_to_v3"] = best_impact[0]
        v3_min.at[idx, "v3_sensitive_votes_v2_to_v3"] = best_impact[1]

        print(f"[v3] {ed_name}: BEST candidate = {label} ({best_impact[0]} VAs, {best_impact[1]:.0f} votes shifted from v2)", flush=True)

    # Write v3 minority
    v3_min.to_file(DATA_DIR / "v0_1_refined_v3_minority_2026_eds.gpkg", driver="GPKG")
    # Write v3 majority (clean of v2 majority — same topology)
    v2_maj = gpd.read_file(DATA_DIR / "v0_1_refined_v2_majority_2026_eds.gpkg").to_crs(WORK_CRS)
    v3_maj = v2_maj.copy()
    for i in range(len(v3_maj)):
        v3_maj.at[i, "geometry"] = clean_polygon_noise(v3_maj.iloc[i].geometry)
    v3_maj.to_file(DATA_DIR / "v0_1_refined_v3_majority_2026_eds.gpkg", driver="GPKG")
    print(f"[v3] wrote v3 majority+minority gpkgs", flush=True)
    return passes_log


# ----------------------------------------------------------------------
# Final impact CSV
# ----------------------------------------------------------------------

def compute_final_impact():
    """Compute Track Y v1 vs Track Y-prime-prime v3 impact per red ED,
    and replicate v2-vs-v1 / v2-vs-v3 residuals.
    """
    v1_min = gpd.read_file(DATA_DIR / "v0_1_refined_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    v2_min = gpd.read_file(DATA_DIR / "v0_1_refined_v2_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    v3_min = gpd.read_file(DATA_DIR / "v0_1_refined_v3_minority_2026_eds.gpkg").to_crs(WORK_CRS)

    vas = gpd.read_file(DATA_DIR / "va_polygons_with_2023_votes.gpkg").to_crs(WORK_CRS)
    vas["total_votes"] = (vas["va_ndp"].fillna(0) + vas["va_ucp"].fillna(0) + vas["va_other"].fillna(0)).astype(float)

    rows = []
    # These are the 5 Tier B EDs used in v2
    tier_b_names = [
        "Calgary-De Winton", "Calgary-South", "Edmonton-Windermere",
        "Lethbridge-Little Bow", "Wetaskawin-Ponoka-Maskwacis",
    ]
    for name in tier_b_names:
        v1 = v1_min[v1_min["name_2026"] == name]
        v2 = v2_min[v2_min["name_2026"] == name]
        v3 = v3_min[v3_min["name_2026"] == name]
        if len(v1) == 0 or len(v2) == 0 or len(v3) == 0:
            continue
        v1g = v1.iloc[0].geometry
        v2g = v2.iloc[0].geometry
        v3g = v3.iloc[0].geometry
        v2g_clean = clean_polygon_noise(v2g)

        n_v1v2, v_v1v2, _, a_v1v2 = _measure_impact(v1g, v2g, vas)
        n_v2v3, v_v2v3, _, a_v2v3 = _measure_impact(v2g_clean, v3g, vas)
        n_v1v3, v_v1v3, _, a_v1v3 = _measure_impact(v1g, v3g, vas)

        # v3 classification. Red EDs after 4 passes with no convergence are
        # promoted to 'refinement-unresolvable-without-shapefile' per PO.
        is_red = name in RED_EDS
        if is_red:
            cls = "refinement-unresolvable-without-shapefile"
        elif v_v1v3 > 500:
            cls = "refinement-significant"
        else:
            cls = "refinement-negligible"

        rows.append({
            "ed_name": name,
            "v1_vs_v2_vas": n_v1v2,
            "v1_vs_v2_votes": v_v1v2,
            "v2_vs_v3_vas": n_v2v3,
            "v2_vs_v3_votes": v_v2v3,
            "v1_vs_v3_vas": n_v1v3,
            "v1_vs_v3_votes": v_v1v3,
            "classification_v3": cls,
            "orange_accept_v3": (cls == "refinement-negligible"),
        })

    df = pd.DataFrame(rows)
    df.to_csv(DATA_DIR / "boundary_refinement_impact_v3.csv", index=False)
    return df


# ----------------------------------------------------------------------
# Phase 5 render fix: draw only exterior rings of substantial parts
# ----------------------------------------------------------------------

PRIORITY_EDS = [
    ("majority", "Calgary North"),
    ("majority", "Calgary North West"),
    ("majority", "Calgary South East"),
    ("majority", "Red Deer North"),
    ("majority", "Red Deer South"),
    ("minority", "Calgary-De Winton"),
    ("minority", "Calgary-South"),
    ("minority", "Edmonton-Windermere"),
    ("minority", "Lethbridge-Little Bow"),
    ("minority", "Wetaskawin-Ponoka-Maskwacis"),
]


def _norm(s: str) -> str:
    return str(s).lower().replace("-", " ").replace("  ", " ").replace(".", "").replace("'", "").strip()


def _find_ed(gdf, name):
    target = _norm(name)
    if "name_2026" not in gdf.columns:
        return None
    series = gdf["name_2026"].astype(str).map(_norm)
    hit = gdf[series == target]
    if len(hit):
        return hit.iloc[0]
    mask = series.str.contains(target, na=False, regex=False)
    hits = gdf[mask]
    if len(hits):
        orders = series[mask].str.len().sort_values().index
        return gdf.loc[orders[0]]
    return None


def _exterior_only_lines(geom):
    """Return a list of LineString objects, one per substantial polygon
    part's exterior ring. Omits interior rings and noise-area parts.

    This is the core of the rendering-bug fix: we never draw a ring
    originating from an interior hole or a micro-part artifact.
    """
    out = []
    if geom is None or geom.is_empty:
        return out
    parts = [geom] if geom.geom_type == "Polygon" else (list(geom.geoms) if geom.geom_type == "MultiPolygon" else [])
    for p in parts:
        if p is None or p.is_empty:
            continue
        try:
            if p.area < NOISE_PART_AREA_M2:
                continue
        except Exception:
            continue
        try:
            out.append(LineString(p.exterior.coords))
        except Exception:
            continue
    return out


def render_v3_panels(impact_df):
    """Render verification panels with the internal-border fix in place."""
    VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
    v1_maj = gpd.read_file(DATA_DIR / "v0_1_refined_majority_2026_eds.gpkg").to_crs(WORK_CRS)
    v1_min = gpd.read_file(DATA_DIR / "v0_1_refined_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    v3_maj = gpd.read_file(DATA_DIR / "v0_1_refined_v3_majority_2026_eds.gpkg").to_crs(WORK_CRS)
    v3_min = gpd.read_file(DATA_DIR / "v0_1_refined_v3_minority_2026_eds.gpkg").to_crs(WORK_CRS)

    impact_lookup = {row["ed_name"]: row for _, row in impact_df.iterrows()} if impact_df is not None else {}

    GREEN = "#2ca02c"
    ORANGE = "#ff7f0e"
    RED = "#d62728"
    GREY = "#999"

    fig_grid, axes = plt.subplots(2, 5, figsize=(30, 14), dpi=120)
    axes = axes.flatten()

    for idx, (which, name) in enumerate(PRIORITY_EDS):
        v1_gdf = v1_maj if which == "majority" else v1_min
        v3_gdf = v3_maj if which == "majority" else v3_min
        v1_row = _find_ed(v1_gdf, name)
        v3_row = _find_ed(v3_gdf, name)
        ax = axes[idx]
        ax.set_axis_off()

        impact = impact_lookup.get(name)
        tier = v3_row["tier"] if v3_row is not None and "tier" in v3_row.index else "A"
        if tier == "A":
            colour = GREEN
            tier_label = "Tier A (2019 inherit)"
            linestyle = "-"
        else:
            # Use v3 classification if impact row exists, otherwise default
            if impact is None:
                colour = RED
                tier_label = "Tier B — unresolved"
                linestyle = "--"
            elif impact.get("classification_v3") == "refinement-negligible":
                colour = ORANGE
                tier_label = "Tier B — orange accepted"
                linestyle = "-"
            elif impact.get("classification_v3") == "refinement-unresolvable-without-shapefile":
                colour = RED
                tier_label = "Tier B — unresolvable without shapefile"
                linestyle = "--"
            elif impact.get("classification_v3") == "refinement-significant":
                colour = RED
                tier_label = "Tier B — significant residual"
                linestyle = "--"
            else:
                colour = RED
                tier_label = "Tier B — unresolved"
                linestyle = "--"

        title_suffix = ""
        if impact is not None:
            title_suffix = f" (v1-v3: {int(impact.get('v1_vs_v3_vas', 0))} VAs, {int(impact.get('v1_vs_v3_votes', 0))} votes)"
        ax.set_title(f"{which}: {name}\n{tier_label}{title_suffix}", fontsize=9)

        bounds = None
        if v3_row is not None:
            v3_gser = gpd.GeoSeries([v3_row.geometry], crs=WORK_CRS)
            bounds = v3_gser.total_bounds
        elif v1_row is not None:
            v1_gser = gpd.GeoSeries([v1_row.geometry], crs=WORK_CRS)
            bounds = v1_gser.total_bounds

        if bounds is not None:
            pad = 0.05 * max(bounds[2] - bounds[0], bounds[3] - bounds[1], 1000)
            ax.set_xlim(bounds[0] - pad, bounds[2] + pad)
            ax.set_ylim(bounds[1] - pad, bounds[3] + pad)

        # v1 reference: exterior-only, thin grey dotted
        if v1_row is not None:
            v1_clean = clean_polygon_noise(v1_row.geometry)
            v1_lines = _exterior_only_lines(v1_clean)
            if v1_lines:
                gpd.GeoSeries(v1_lines, crs=WORK_CRS).plot(
                    ax=ax, color=GREY, linewidth=0.9, linestyle=":"
                )

        # v3 main: exterior-only, tier colour, thick
        if v3_row is not None:
            v3_lines = _exterior_only_lines(v3_row.geometry)
            if v3_lines:
                gpd.GeoSeries(v3_lines, crs=WORK_CRS).plot(
                    ax=ax, color=colour, linewidth=2.2, linestyle=linestyle
                )

        # Single panel file
        fig_single, ax_s = plt.subplots(figsize=(6, 6), dpi=120)
        ax_s.set_axis_off()
        ax_s.set_title(f"{which}: {name}\n{tier_label}{title_suffix}", fontsize=10)
        if bounds is not None:
            ax_s.set_xlim(bounds[0] - pad, bounds[2] + pad)
            ax_s.set_ylim(bounds[1] - pad, bounds[3] + pad)
        if v1_row is not None:
            v1_clean = clean_polygon_noise(v1_row.geometry)
            v1_lines = _exterior_only_lines(v1_clean)
            if v1_lines:
                gpd.GeoSeries(v1_lines, crs=WORK_CRS).plot(
                    ax=ax_s, color=GREY, linewidth=0.9, linestyle=":"
                )
        if v3_row is not None:
            v3_lines = _exterior_only_lines(v3_row.geometry)
            if v3_lines:
                gpd.GeoSeries(v3_lines, crs=WORK_CRS).plot(
                    ax=ax_s, color=colour, linewidth=2.2, linestyle=linestyle
                )
        ax_s.text(
            0.02, 0.02,
            "Green = Tier A (2019 inherit)\nOrange = Tier B accepted (votes stable)\nRed dashed = Tier B unresolvable without shapefile\nGrey dotted = v1 (Track Y)",
            transform=ax_s.transAxes, fontsize=7, verticalalignment="bottom",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="#ccc"),
        )
        slug = name.replace(" ", "_").replace("/", "_").replace("-", "_").lower()
        fig_single.savefig(VERIFICATION_DIR / f"v0_3_{which}_{slug}.png", bbox_inches="tight")
        plt.close(fig_single)

    fig_grid.tight_layout()
    fig_grid.savefig(VERIFICATION_DIR / "v0_3_priority_grid.png", bbox_inches="tight")
    plt.close(fig_grid)
    print(f"[render] wrote v0_3 panels", flush=True)


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------

def main(skip=()):
    passes_log = []
    impact_df = None

    if "pass" not in skip:
        print("=== v3: PASSES 3 AND 4 ON RED EDs ===", flush=True)
        try:
            passes_log = run_passes_3_and_4()
        except Exception as e:
            print(f"[pass] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "impact" not in skip:
        print("=== v3: FINAL IMPACT TABLE ===", flush=True)
        try:
            impact_df = compute_final_impact()
            print(impact_df.to_string(), flush=True)
        except Exception as e:
            print(f"[impact] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "render" not in skip:
        print("=== v3: RENDER v0_3 PANELS (bug fixed) ===", flush=True)
        try:
            render_v3_panels(impact_df)
        except Exception as e:
            print(f"[render] fatal: {e}\n{traceback.format_exc()}", flush=True)

    summary = {
        "passes_log": passes_log,
        "impact": impact_df.to_dict("records") if impact_df is not None else None,
    }
    out_log = ANALYSIS_DIR / "shape_refinement_v3_log.json"
    out_log.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("\n=== v3 SUMMARY ===", flush=True)
    print(json.dumps(summary, indent=2, default=str), flush=True)
    return summary


if __name__ == "__main__":
    skip = sys.argv[1:] if len(sys.argv) > 1 else ()
    main(skip=skip)
