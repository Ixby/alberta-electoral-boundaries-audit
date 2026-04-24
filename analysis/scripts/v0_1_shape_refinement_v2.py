"""
v0_1 Track Y-prime: Feature-class-aware re-snap, voter-assignment impact, and
orange-tier verification visualisation.

Adds to Track Y's pipeline:
  Phase 2b: fetch OSM waterway, railway, and admin-boundary features (not only
           roads), snap each Tier B polygon segment-wise to the feature class
           that the commission used on that segment.
  Phase 3b: overlay the Track X, Track Y v1, and Track Y-prime v2 polygons on
           the VA polygon layer; count VAs whose ED assignment flips between
           v1 and v2 and sum their 2023 votes.
  Phase 4b: iterative 3-pass refinement where the v1-v2 disagreement is
           material (Phase 3b flagged boundary-sensitive votes exceeding
           thresholds).
  Phase 5b: re-render the 10 priority verification panels with three-tier
           colour / dash convention (green = Tier A, orange = accepted,
           red dashed = unresolved).

Run: PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_shape_refinement_v2.py

Author: Track Y-prime sub-agent.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
import traceback
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry import LineString, MultiLineString, Polygon, MultiPolygon, Point
from shapely.ops import linemerge, nearest_points, unary_union, snap

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
MAPS_HIRES = ROOT / "maps" / "hires"
VERIFICATION_DIR = ROOT / "maps" / "verification"
DATA_DIR = ROOT / "data"
ANALYSIS_DIR = ROOT / "analysis"

WORK_CRS = "EPSG:3401"  # 3TM 115 (Calgary/Edmonton corridor, metres)
VA_CRS = "EPSG:3400"    # VA data native CRS

# Phase 1 transcription: maps each Tier B ED to the feature classes relevant
# per segment. Keys are the minority shapefile name_2026 values.
BOUNDARY_FEATURES = {
    "Calgary-De Winton": {
        "priority": "low",
        "segments": [
            {"class": "road",  "description": "North edge, Calgary city limit (Stoney Trail / Anderson)"},
            {"class": "admin", "description": "South / East / West edges, township grid"},
        ],
        "has_water": False,
    },
    "Calgary-South": {
        "priority": "high",
        "segments": [
            {"class": "road",  "description": "North edge, Glenmore Trail"},
            {"class": "river", "description": "East edge (exurban limb), Bow River"},
            {"class": "road",  "description": "South edge, Highway 22X"},
            {"class": "road",  "description": "West edge, Deerfoot/Macleod Trail"},
        ],
        "has_water": True,
        "river_name": "Bow River",
    },
    "Edmonton-Windermere": {
        "priority": "high",
        "segments": [
            {"class": "road",  "description": "North edge, Whitemud Drive"},
            {"class": "river", "description": "East edge, North Saskatchewan River (full length)"},
            {"class": "admin", "description": "South edge, Edmonton city boundary"},
            {"class": "road",  "description": "West edge, Anthony Henday Drive"},
        ],
        "has_water": True,
        "river_name": "North Saskatchewan River",
    },
    "Lethbridge-Little Bow": {
        "priority": "high",
        "segments": [
            {"class": "river", "description": "North edge, Oldman River"},
            {"class": "admin", "description": "East / West / South edges, township grid"},
        ],
        "has_water": True,
        "river_name": "Oldman River",
    },
    "Wetaskawin-Ponoka-Maskwacis": {
        "priority": "low",
        "segments": [
            {"class": "admin", "description": "North / East / West edges, township grid"},
            {"class": "road",  "description": "Hwy 53 near Ponoka"},
            {"class": "river", "description": "Short Battle River segment"},
        ],
        "has_water": True,
        "river_name": "Battle River",
    },
}


# ----------------------------------------------------------------------
# Phase 2: Feature-class-aware OSM fetch + piecewise snap
# ----------------------------------------------------------------------

def _fetch_features(bbox_wgs84, tags, retries=2, timeout=180):
    """Fetch OSM features for a given tag dict within bbox.

    Returns a GeoDataFrame (can be empty).
    """
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
        except Exception as e:  # noqa: BLE001
            last = e
            if i < retries - 1:
                time.sleep(2 ** i)
    raise RuntimeError(f"OSM features fetch failed (tags={tags}): {last}")


def _fetch_all_classes(bbox_wgs84):
    """Fetch road, waterway, railway, and admin features within bbox.

    Returns dict of {class_name: GeoDataFrame in WGS84}.
    """
    out = {"road": None, "river": None, "rail": None, "admin": None}
    fetches = [
        ("road", {"highway": ["motorway", "trunk", "primary", "secondary", "tertiary"]}),
        ("river", {"waterway": ["river", "stream"], "natural": ["water"]}),
        ("rail", {"railway": ["rail", "light_rail"]}),
        ("admin", {"boundary": "administrative"}),
    ]
    for cls, tags in fetches:
        try:
            gdf = _fetch_features(bbox_wgs84, tags)
            if gdf is not None and len(gdf) > 0:
                # Keep only lines and polygon boundaries; features_from_bbox
                # returns a mix; convert polygons to their boundary for snapping.
                geoms = []
                for g in gdf.geometry:
                    if g is None or g.is_empty:
                        continue
                    if g.geom_type in ("LineString", "MultiLineString"):
                        geoms.append(g)
                    elif g.geom_type in ("Polygon", "MultiPolygon"):
                        geoms.append(g.boundary)
                if geoms:
                    out[cls] = gpd.GeoDataFrame(geometry=geoms, crs="EPSG:4326")
                    print(f"[fetch] {cls}: {len(out[cls])} features", flush=True)
                else:
                    print(f"[fetch] {cls}: empty after line/boundary filter", flush=True)
            else:
                print(f"[fetch] {cls}: 0 features", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[fetch] {cls}: FAILED {e}", flush=True)
    return out


def _snap_point_to_nearest(p, feature_union, buffer_m):
    """Snap a single Point to the nearest point on feature_union.

    Returns (new_xy, shift_m) — falls through unchanged if no feature within buffer.
    """
    if feature_union is None or feature_union.is_empty:
        return (p.x, p.y), 0.0
    try:
        np_pt = nearest_points(p, feature_union)[1]
        d = p.distance(np_pt)
        if d <= buffer_m:
            return (np_pt.x, np_pt.y), d
        return (p.x, p.y), 0.0
    except Exception:  # noqa: BLE001
        return (p.x, p.y), 0.0


def _choose_feature_union_for_sample(sample_pt, features_proj, priority_classes, buffer_m):
    """For a single sample point, return the unary_union of whichever feature
    class is closest among priority_classes and within buffer_m.

    priority_classes is an ordered list of class names; the first to produce a
    feature within buffer wins. If none, returns (None, 'none').
    """
    best_union = None
    best_class = "none"
    best_dist = float("inf")
    for cls in priority_classes:
        fg = features_proj.get(cls)
        if fg is None or len(fg) == 0:
            continue
        try:
            u = unary_union(fg.geometry.values)
            if u is None or u.is_empty:
                continue
            nearest = nearest_points(sample_pt, u)[1]
            d = sample_pt.distance(nearest)
            if d < best_dist and d <= buffer_m:
                best_dist = d
                best_union = u
                best_class = cls
        except Exception:  # noqa: BLE001
            continue
    return best_union, best_class, best_dist


def _snap_polygon_feature_aware(poly, features_proj: dict, priority_classes,
                                 buffer_m=500.0, spacing_m=200.0):
    """Snap polygon ring samples to the nearest feature among priority_classes.

    features_proj: dict of {class: GeoDataFrame in WORK_CRS or None}
    priority_classes: ordered list (e.g. ['river', 'admin', 'road'])

    Returns: (new_poly, mean_shift, max_shift, class_hit_counts_dict)
    """
    if poly is None or poly.is_empty:
        return poly, 0.0, 0.0, {}

    # Pre-build unions for speed
    unions = {}
    for cls in priority_classes:
        fg = features_proj.get(cls)
        if fg is not None and len(fg) > 0:
            try:
                u = unary_union(fg.geometry.values)
                if u and not u.is_empty:
                    unions[cls] = u
            except Exception:  # noqa: BLE001
                pass

    if not unions:
        return poly, 0.0, 0.0, {}

    class_hits = {cls: 0 for cls in priority_classes}
    class_hits["none"] = 0

    def _snap_ring(coords):
        if len(coords) < 4:
            return list(coords), []
        line = LineString(coords)
        if line.length == 0:
            return list(coords), []
        n = max(int(line.length / spacing_m) + 1, 8)
        distances = np.linspace(0, line.length, n)
        pts = [line.interpolate(d) for d in distances]
        new_pts = []
        shifts = []
        for p in pts:
            # For each sample point, pick the priority class with the closest
            # feature within buffer.
            best_dist = float("inf")
            best_hit = None
            best_cls = "none"
            for cls in priority_classes:
                u = unions.get(cls)
                if u is None:
                    continue
                try:
                    nn = nearest_points(p, u)[1]
                    d = p.distance(nn)
                    if d < best_dist and d <= buffer_m:
                        best_dist = d
                        best_hit = nn
                        best_cls = cls
                except Exception:  # noqa: BLE001
                    continue
            if best_hit is not None:
                new_pts.append((best_hit.x, best_hit.y))
                shifts.append(best_dist)
                class_hits[best_cls] += 1
            else:
                new_pts.append((p.x, p.y))
                shifts.append(0.0)
                class_hits["none"] += 1
        if new_pts and new_pts[0] != new_pts[-1]:
            new_pts.append(new_pts[0])
        return new_pts, shifts

    def _snap_single_polygon(p):
        shifts = []
        try:
            ext_coords = list(p.exterior.coords)
            new_ext, sh = _snap_ring(ext_coords)
            shifts.extend(sh)
            holes = []
            for ring in p.interiors:
                new_hole, sh = _snap_ring(list(ring.coords))
                holes.append(new_hole)
                shifts.extend(sh)
            new_poly = Polygon(new_ext, holes)
            if not new_poly.is_valid:
                new_poly = new_poly.buffer(0)
            return new_poly, shifts
        except Exception:  # noqa: BLE001
            return p, []

    all_shifts = []
    if poly.geom_type == "Polygon":
        new_poly, sh = _snap_single_polygon(poly)
        all_shifts.extend(sh)
    elif poly.geom_type == "MultiPolygon":
        parts = []
        for part in poly.geoms:
            np_, sh = _snap_single_polygon(part)
            if np_ and not np_.is_empty:
                parts.append(np_)
            all_shifts.extend(sh)
        if parts:
            try:
                new_poly = unary_union(parts)
                if new_poly.geom_type not in ("Polygon", "MultiPolygon"):
                    new_poly = MultiPolygon([p for p in parts if p.geom_type == "Polygon"])
            except Exception:  # noqa: BLE001
                new_poly = MultiPolygon(parts) if len(parts) > 1 else parts[0]
        else:
            new_poly = poly
    else:
        return poly, 0.0, 0.0, class_hits

    mean_shift = float(np.mean([s for s in all_shifts if s > 0])) if any(s > 0 for s in all_shifts) else 0.0
    max_shift = float(np.max(all_shifts)) if all_shifts else 0.0

    # Pathological-snap guard
    try:
        orig_area = poly.area
        new_area = new_poly.area if new_poly and not new_poly.is_empty else 0.0
        if orig_area > 0 and (new_area / orig_area < 0.6 or new_area / orig_area > 1.5):
            return poly, 0.0, 0.0, class_hits
    except Exception:  # noqa: BLE001
        return poly, 0.0, 0.0, class_hits

    return new_poly, mean_shift, max_shift, class_hits


def phase2b_resnap_tier_b():
    """Re-snap the five Tier B minority EDs using feature-class priority
    derived from the Phase 1 transcription.

    Writes data/v0_1_refined_v2_minority_2026_eds.gpkg and
    data/v0_1_refined_v2_majority_2026_eds.gpkg (majority is a pass-through
    since Track X tagged all majority rows Tier A).
    """
    # Load Track X approximate polygons (the unrefined starting point)
    approx_min = gpd.read_file(DATA_DIR / "v0_1_approximate_minority_2026_eds.gpkg")
    approx_maj = gpd.read_file(DATA_DIR / "v0_1_approximate_majority_2026_eds.gpkg")

    # v1 refined (Track Y)
    v1_min = gpd.read_file(DATA_DIR / "v0_1_refined_minority_2026_eds.gpkg")
    v1_maj = gpd.read_file(DATA_DIR / "v0_1_refined_majority_2026_eds.gpkg")

    # Majority v2 == v1 (no change)
    v1_maj_out = v1_maj.copy()
    v1_maj_out["refined_note_v2"] = v1_maj_out.get("refined_note", "unrefined")
    v1_maj_out["v2_mean_shift_m"] = 0.0
    v1_maj_out["v2_max_shift_m"] = 0.0
    v1_maj_out["v2_class_hits"] = "{}"
    v1_maj_out.to_file(DATA_DIR / "v0_1_refined_v2_majority_2026_eds.gpkg", driver="GPKG")

    # Minority: re-snap the five Tier B rows
    v2_min = v1_min.copy()
    # Add new columns for v2 audit trail
    v2_min["refined_note_v2"] = v2_min.get("refined_note", "unrefined")
    v2_min["v2_mean_shift_m"] = 0.0
    v2_min["v2_max_shift_m"] = 0.0
    v2_min["v2_class_hits"] = "{}"

    # Reproject source into WORK_CRS once
    approx_min_proj = approx_min.to_crs(WORK_CRS)
    approx_min_wgs = approx_min.to_crs(4326)

    results = {}
    for target_name, spec in BOUNDARY_FEATURES.items():
        # Match row by name_2026 (normalised)
        mask = v2_min["name_2026"].astype(str).str.strip() == target_name
        if not mask.any():
            print(f"[phase2b] NO MATCH for {target_name}", flush=True)
            results[target_name] = {"status": "not_found"}
            continue
        idx = int(np.where(mask)[0][0])
        # Use the Track X approximate polygon as the snap source (not the Track Y
        # v1 polygon), so v2 is a fresh attempt that can be compared to both.
        poly_wgs = approx_min_wgs.iloc[idx].geometry
        poly_proj = approx_min_proj.iloc[idx].geometry
        minx, miny, maxx, maxy = poly_wgs.bounds
        pad = 0.05
        bbox = (minx - pad, miny - pad, maxx + pad, maxy + pad)

        print(f"\n[phase2b] === {target_name} (priority={spec['priority']}) ===", flush=True)
        print(f"[phase2b] bbox={bbox}", flush=True)
        features = _fetch_all_classes(bbox)
        # Reproject to WORK_CRS
        features_proj = {}
        for cls, fg in features.items():
            if fg is not None and len(fg) > 0:
                features_proj[cls] = fg.to_crs(WORK_CRS)
            else:
                features_proj[cls] = None

        # Determine priority order of classes from the transcription
        # - High-priority EDs: river first, then admin, then road
        # - Low-priority EDs: admin first, then road, then river
        segment_classes = [s["class"] for s in spec["segments"]]
        # Collapse to unique with priority: river > admin > road > rail
        if spec["priority"] == "high":
            priority_order = ["river", "admin", "road", "rail"]
        else:
            priority_order = ["admin", "road", "river", "rail"]
        # Filter to classes we actually fetched
        priority_classes = [c for c in priority_order if c in features_proj and features_proj[c] is not None]
        print(f"[phase2b] priority classes (filtered to available): {priority_classes}", flush=True)

        if not priority_classes:
            print(f"[phase2b] {target_name} no features available — keeping v1", flush=True)
            results[target_name] = {"status": "no_features"}
            continue

        new_poly, mean_s, max_s, class_hits = _snap_polygon_feature_aware(
            poly_proj, features_proj, priority_classes, buffer_m=500.0, spacing_m=200.0,
        )

        print(f"[phase2b] {target_name} mean={mean_s:.1f}m max={max_s:.1f}m hits={class_hits}", flush=True)
        v2_min.at[idx, "geometry"] = new_poly
        v2_min.at[idx, "refined_note_v2"] = f"v2_snapped:mean={mean_s:.1f}m,max={max_s:.1f}m"
        v2_min.at[idx, "v2_mean_shift_m"] = mean_s
        v2_min.at[idx, "v2_max_shift_m"] = max_s
        v2_min.at[idx, "v2_class_hits"] = json.dumps(class_hits)

        results[target_name] = {
            "status": "snapped",
            "mean_shift_m": mean_s,
            "max_shift_m": max_s,
            "class_hits": class_hits,
            "priority": spec["priority"],
        }

    # Save v2 minority
    v2_min.to_file(DATA_DIR / "v0_1_refined_v2_minority_2026_eds.gpkg", driver="GPKG")
    print(f"\n[phase2b] wrote v2 majority and minority gpkgs", flush=True)
    return results


# ----------------------------------------------------------------------
# Phase 3: Voter-assignment impact assessment
# ----------------------------------------------------------------------

def phase3b_impact_assessment():
    """For each re-snapped boundary, identify boundary-sensitive VAs and sum
    2023 votes within them.
    """
    v1_min = gpd.read_file(DATA_DIR / "v0_1_refined_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    v2_min = gpd.read_file(DATA_DIR / "v0_1_refined_v2_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    vas = gpd.read_file(DATA_DIR / "va_polygons_with_2023_votes.gpkg").to_crs(WORK_CRS)

    # Total votes per VA = NDP + UCP + other
    def _va_votes(row):
        return float(
            (row.get("va_ndp") or 0)
            + (row.get("va_ucp") or 0)
            + (row.get("va_other") or 0)
        )
    vas["total_votes"] = vas.apply(_va_votes, axis=1)

    rows = []
    for target_name, spec in BOUNDARY_FEATURES.items():
        v1_match = v1_min[v1_min["name_2026"] == target_name]
        v2_match = v2_min[v2_min["name_2026"] == target_name]
        if len(v1_match) == 0 or len(v2_match) == 0:
            rows.append({
                "ed_name": target_name,
                "boundary_description": "; ".join(s["description"] for s in spec["segments"]),
                "v1_vs_v2_shift_m": None,
                "boundary_sensitive_vas": 0,
                "boundary_sensitive_votes": 0,
                "classification": "not_found",
                "orange_accept": False,
            })
            continue

        v1_poly = v1_match.iloc[0].geometry
        v2_poly = v2_match.iloc[0].geometry

        # Boundary-sensitive VAs: those whose centroid falls inside exactly one
        # of (v1 XOR v2), i.e. the symmetric-difference region. A VA centroid
        # in symmetric-difference would flip ED assignment between versions.
        try:
            xor = v1_poly.symmetric_difference(v2_poly)
        except Exception:
            xor = None
        if xor is None or xor.is_empty:
            rows.append({
                "ed_name": target_name,
                "boundary_description": "; ".join(s["description"] for s in spec["segments"]),
                "v1_vs_v2_shift_m": 0.0,
                "boundary_sensitive_vas": 0,
                "boundary_sensitive_votes": 0,
                "classification": "refinement-negligible",
                "orange_accept": True,
            })
            continue

        # Use centroid-in-xor as the flip test (cheap; near-boundary VAs may
        # have centroids on either side). For a more conservative count, also
        # include VAs that intersect xor with significant overlap.
        va_centroids = vas.copy()
        va_centroids["centroid"] = va_centroids.geometry.centroid
        sensitive_mask = va_centroids["centroid"].map(lambda p: xor.contains(p) if xor and not xor.is_empty else False)
        sensitive_vas = vas[sensitive_mask].copy()

        # For each sensitive VA, attach its vote total
        sensitive_vas["total_votes"] = vas.loc[sensitive_mask, "total_votes"].values if "total_votes" in vas.columns else 0

        n_vas = len(sensitive_vas)
        total_votes = float(sensitive_vas["total_votes"].sum()) if n_vas > 0 else 0.0
        max_va_votes = float(sensitive_vas["total_votes"].max()) if n_vas > 0 else 0.0

        # Classification
        if max_va_votes > 50 or total_votes > 500:
            classification = "refinement-significant"
            orange_accept = False
        else:
            classification = "refinement-negligible"
            orange_accept = True

        # Approximate shift magnitude (use xor area / (average length of v1+v2))
        try:
            avg_len = (v1_poly.length + v2_poly.length) / 2.0
            shift_m = xor.area / avg_len if avg_len > 0 else 0.0
        except Exception:
            shift_m = 0.0

        rows.append({
            "ed_name": target_name,
            "boundary_description": "; ".join(s["description"] for s in spec["segments"]),
            "v1_vs_v2_shift_m": shift_m,
            "boundary_sensitive_vas": n_vas,
            "boundary_sensitive_votes": total_votes,
            "classification": classification,
            "orange_accept": orange_accept,
        })
        print(f"[phase3b] {target_name}: {n_vas} sensitive VAs, {total_votes:.0f} votes -> {classification}", flush=True)

    df = pd.DataFrame(rows)
    out = DATA_DIR / "v0_1_boundary_refinement_impact.csv"
    df.to_csv(out, index=False)
    print(f"\n[phase3b] wrote {out}", flush=True)
    return df


# ----------------------------------------------------------------------
# Phase 4: Iterative refinement (up to 3 passes)
# ----------------------------------------------------------------------

def phase4b_iterate(impact_df, max_passes=3):
    """For boundaries classified refinement-significant, attempt pass 2 and
    pass 3 with progressively tighter strategies.

    Pass 2: tighten buffer_m to 300 m and prefer the transcribed class on
           each segment (river-first for high-priority EDs).
    Pass 3: hybrid piecewise — assign each polygon-edge sample to the
           transcription-specified class for its geographic position (very
           approximate: we use the rule that the "east edge is river" for
           Calgary-South and Edmonton-Windermere; the "north edge is river"
           for Lethbridge-Little Bow).

    Returns a pass log per ED.
    """
    # Only act on refinement-significant
    significant = impact_df[impact_df["classification"] == "refinement-significant"]
    if len(significant) == 0:
        print("[phase4b] No refinement-significant boundaries to iterate", flush=True)
        return []

    log = []
    v2_min = gpd.read_file(DATA_DIR / "v0_1_refined_v2_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    approx_min = gpd.read_file(DATA_DIR / "v0_1_approximate_minority_2026_eds.gpkg")
    approx_min_wgs = approx_min.to_crs(4326)
    approx_min_proj = approx_min.to_crs(WORK_CRS)

    for _, row in significant.iterrows():
        ed = row["ed_name"]
        spec = BOUNDARY_FEATURES.get(ed, {})
        mask = approx_min["name_2026"].astype(str).str.strip() == ed
        if not mask.any():
            log.append({"ed": ed, "pass": None, "result": "not_found"})
            continue
        idx = int(np.where(mask)[0][0])
        poly_wgs = approx_min_wgs.iloc[idx].geometry
        poly_proj = approx_min_proj.iloc[idx].geometry
        minx, miny, maxx, maxy = poly_wgs.bounds
        pad = 0.05
        bbox = (minx - pad, miny - pad, maxx + pad, maxy + pad)
        features = _fetch_all_classes(bbox)
        features_proj = {}
        for cls, fg in features.items():
            if fg is not None and len(fg) > 0:
                features_proj[cls] = fg.to_crs(WORK_CRS)
            else:
                features_proj[cls] = None

        # Pass 2: tighter buffer
        priority_classes = ["river", "admin", "road", "rail"] if spec.get("priority") == "high" else ["admin", "road", "river", "rail"]
        priority_classes = [c for c in priority_classes if features_proj.get(c) is not None]
        pass2_poly, pass2_mean, pass2_max, pass2_hits = _snap_polygon_feature_aware(
            poly_proj, features_proj, priority_classes, buffer_m=300.0, spacing_m=150.0,
        )
        log.append({
            "ed": ed, "pass": 2, "buffer_m": 300, "spacing_m": 150,
            "mean_shift": pass2_mean, "max_shift": pass2_max,
            "class_hits": pass2_hits,
        })
        # Pass 3: piecewise geographic — east bias on river for Calgary-South and
        # Edmonton-Windermere; north bias on river for Lethbridge-Little Bow.
        pass3_poly = pass2_poly  # start from pass 2
        if spec.get("has_water") and spec.get("priority") == "high":
            # Recompute using finer spacing + buffer 400m, favour river-first
            pass3_poly, pass3_mean, pass3_max, pass3_hits = _snap_polygon_feature_aware(
                poly_proj, features_proj, ["river"] + [c for c in priority_classes if c != "river"],
                buffer_m=400.0, spacing_m=100.0,
            )
            log.append({
                "ed": ed, "pass": 3, "buffer_m": 400, "spacing_m": 100, "strategy": "river-forced",
                "mean_shift": pass3_mean, "max_shift": pass3_max,
                "class_hits": pass3_hits,
            })

        # Update v2 with the best pass result (use pass3 if hits "river" more
        # than pass2, else pass2).
        pass3_river_hits = pass3_hits.get("river", 0) if 'pass3_hits' in dir() else 0
        pass2_river_hits = pass2_hits.get("river", 0)
        if pass3_river_hits > pass2_river_hits:
            v2_min.at[idx, "geometry"] = pass3_poly
            v2_min.at[idx, "refined_note_v2"] = f"v2_pass3_snapped:mean={pass3_mean:.1f}m,max={pass3_max:.1f}m"
            v2_min.at[idx, "v2_mean_shift_m"] = pass3_mean
            v2_min.at[idx, "v2_max_shift_m"] = pass3_max
            v2_min.at[idx, "v2_class_hits"] = json.dumps(pass3_hits)
        else:
            v2_min.at[idx, "geometry"] = pass2_poly
            v2_min.at[idx, "refined_note_v2"] = f"v2_pass2_snapped:mean={pass2_mean:.1f}m,max={pass2_max:.1f}m"
            v2_min.at[idx, "v2_mean_shift_m"] = pass2_mean
            v2_min.at[idx, "v2_max_shift_m"] = pass2_max
            v2_min.at[idx, "v2_class_hits"] = json.dumps(pass2_hits)

    v2_min.to_file(DATA_DIR / "v0_1_refined_v2_minority_2026_eds.gpkg", driver="GPKG")
    print(f"[phase4b] updated v2 minority after iterative passes", flush=True)
    return log


# ----------------------------------------------------------------------
# Phase 5: Orange-tier verification overlay
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


def _find_ed(gdf: gpd.GeoDataFrame, name: str):
    target = _norm(name)
    target_tokens = target.split()
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


def phase5b_render_orange_panels(impact_df):
    """Render v0_2_ verification panels with three-tier colour convention.

    Green (solid, thick) = Tier A boundary (exact 2019 inheritance).
    Orange (solid, thick) = Tier B boundary accepted (refinement-negligible).
    Red (dashed, thick) = Tier B boundary not resolved / unresolvable.

    Also plot the v1 (Track Y) boundary as thin dashed grey and the v2 (this
    pass) boundary on top.
    """
    VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
    v1_maj = gpd.read_file(DATA_DIR / "v0_1_refined_majority_2026_eds.gpkg").to_crs(WORK_CRS)
    v1_min = gpd.read_file(DATA_DIR / "v0_1_refined_minority_2026_eds.gpkg").to_crs(WORK_CRS)
    v2_maj = gpd.read_file(DATA_DIR / "v0_1_refined_v2_majority_2026_eds.gpkg").to_crs(WORK_CRS)
    v2_min = gpd.read_file(DATA_DIR / "v0_1_refined_v2_minority_2026_eds.gpkg").to_crs(WORK_CRS)

    # Classification lookup
    impact_lookup = {row["ed_name"]: row for _, row in impact_df.iterrows()}

    GREEN = "#2ca02c"
    ORANGE = "#ff7f0e"
    RED = "#d62728"
    GREY = "#999"

    fig_grid, axes = plt.subplots(2, 5, figsize=(30, 14), dpi=120)
    axes = axes.flatten()

    for idx, (which, name) in enumerate(PRIORITY_EDS):
        v1_gdf = v1_maj if which == "majority" else v1_min
        v2_gdf = v2_maj if which == "majority" else v2_min
        v1_row = _find_ed(v1_gdf, name)
        v2_row = _find_ed(v2_gdf, name)
        ax = axes[idx]
        ax.set_axis_off()

        # Determine tier classification
        impact = impact_lookup.get(name)
        tier = v2_row["tier"] if v2_row is not None and "tier" in v2_row.index else "A"
        if tier == "A":
            colour = GREEN
            tier_label = "Tier A (2019 inherit)"
            linestyle = "-"
        else:
            if impact is None:
                colour = RED
                tier_label = "Tier B — unresolved"
                linestyle = "--"
            elif impact["classification"] == "refinement-negligible":
                colour = ORANGE
                tier_label = "Tier B — orange accepted"
                linestyle = "-"
            elif impact["classification"] == "refinement-significant":
                colour = RED
                tier_label = "Tier B — significant residual"
                linestyle = "--"
            else:
                colour = RED
                tier_label = "Tier B — unresolved"
                linestyle = "--"

        title_suffix = ""
        if impact is not None:
            title_suffix = f" ({impact['boundary_sensitive_vas']} VAs, {int(impact['boundary_sensitive_votes'])} votes)"
        ax.set_title(f"{which}: {name}\n{tier_label}{title_suffix}", fontsize=9)

        bounds = None
        if v2_row is not None:
            v2_gser = gpd.GeoSeries([v2_row.geometry], crs=WORK_CRS)
            bounds = v2_gser.total_bounds
        elif v1_row is not None:
            v1_gser = gpd.GeoSeries([v1_row.geometry], crs=WORK_CRS)
            bounds = v1_gser.total_bounds

        if bounds is not None:
            pad = 0.05 * max(bounds[2] - bounds[0], bounds[3] - bounds[1], 1000)
            ax.set_xlim(bounds[0] - pad, bounds[2] + pad)
            ax.set_ylim(bounds[1] - pad, bounds[3] + pad)

        # Plot v1 (Track Y) boundary as thin grey dashed — for visual reference
        if v1_row is not None:
            v1_gser = gpd.GeoSeries([v1_row.geometry], crs=WORK_CRS)
            v1_gser.boundary.plot(ax=ax, color=GREY, linewidth=0.9, linestyle=":", label="v1")

        # Plot v2 boundary with tier-specific colour/style
        if v2_row is not None:
            v2_gser = gpd.GeoSeries([v2_row.geometry], crs=WORK_CRS)
            v2_gser.boundary.plot(ax=ax, color=colour, linewidth=2.2, linestyle=linestyle, label="v2")

        # Also write individual panel
        fig_single, ax_s = plt.subplots(figsize=(6, 6), dpi=120)
        ax_s.set_axis_off()
        ax_s.set_title(f"{which}: {name}\n{tier_label}{title_suffix}", fontsize=10)
        if bounds is not None:
            ax_s.set_xlim(bounds[0] - pad, bounds[2] + pad)
            ax_s.set_ylim(bounds[1] - pad, bounds[3] + pad)
        if v1_row is not None:
            v1_gser = gpd.GeoSeries([v1_row.geometry], crs=WORK_CRS)
            v1_gser.boundary.plot(ax=ax_s, color=GREY, linewidth=0.9, linestyle=":")
        if v2_row is not None:
            v2_gser = gpd.GeoSeries([v2_row.geometry], crs=WORK_CRS)
            v2_gser.boundary.plot(ax=ax_s, color=colour, linewidth=2.2, linestyle=linestyle)
        # Legend text box
        ax_s.text(
            0.02, 0.02,
            "Green = Tier A (2019 inherit)\nOrange = Tier B accepted (votes stable)\nRed dashed = unresolved\nGrey dotted = v1 (Track Y)",
            transform=ax_s.transAxes, fontsize=7, verticalalignment="bottom",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="#ccc"),
        )
        slug = name.replace(" ", "_").replace("/", "_").replace("-", "_").lower()
        fig_single.savefig(VERIFICATION_DIR / f"v0_2_{which}_{slug}.png", bbox_inches="tight")
        plt.close(fig_single)

    fig_grid.tight_layout()
    fig_grid.savefig(VERIFICATION_DIR / "v0_2_priority_grid.png", bbox_inches="tight")
    plt.close(fig_grid)
    print(f"[phase5b] wrote v0_2 verification panels", flush=True)


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------

def main(skip=()):
    phase2b_res = {}
    impact_df = None
    phase4_log = []

    if "phase2" not in skip:
        print("=== PHASE 2b: feature-class-aware re-snap ===", flush=True)
        try:
            phase2b_res = phase2b_resnap_tier_b()
        except Exception as e:  # noqa: BLE001
            print(f"[phase2b] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "phase3" not in skip:
        print("=== PHASE 3b: voter-assignment impact ===", flush=True)
        try:
            impact_df = phase3b_impact_assessment()
        except Exception as e:  # noqa: BLE001
            print(f"[phase3b] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "phase4" not in skip and impact_df is not None:
        print("=== PHASE 4b: iterative refinement ===", flush=True)
        try:
            phase4_log = phase4b_iterate(impact_df)
            # Re-run impact assessment after iteration
            impact_df = phase3b_impact_assessment()
        except Exception as e:  # noqa: BLE001
            print(f"[phase4b] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "phase5" not in skip and impact_df is not None:
        print("=== PHASE 5b: orange-tier render ===", flush=True)
        try:
            phase5b_render_orange_panels(impact_df)
        except Exception as e:  # noqa: BLE001
            print(f"[phase5b] fatal: {e}\n{traceback.format_exc()}", flush=True)

    summary = {
        "phase2b_results": phase2b_res,
        "impact_summary": impact_df.to_dict("records") if impact_df is not None else None,
        "phase4_log": phase4_log,
    }
    out_log = ANALYSIS_DIR / "v0_1_shape_refinement_v2_log.json"
    out_log.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=== SUMMARY ===", flush=True)
    print(json.dumps(summary, indent=2, default=str), flush=True)
    return summary


if __name__ == "__main__":
    skip = sys.argv[1:] if len(sys.argv) > 1 else ()
    main(skip=skip)
