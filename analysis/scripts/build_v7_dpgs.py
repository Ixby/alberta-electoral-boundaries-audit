"""
v0_1_build_v7_dpgs.py — Build v0_7 canonical DPGs (full 89-ED coverage)
=========================================================================
v0_6 had 77 EDs because:
  (a) v0_4 municipal anchoring produced null geometries for 12 EDs per map,
  (b) v0_6 boundary propagation read from v0_4, silently dropping those 12.

v0_7 fixes both:
  1. Reads v0_5 (da_anchored) as input — 5 remaining null-geom EDs per map,
     not 12, because v0_5 recovered 7.
  2. For the 5 still-null EDs, falls back to v0_3 (swept) geometry — topologically
     valid, zero snapping applied, with anchored_pct set to 0.
  3. Runs the same confidence-propagation algorithm used by v0_6, but on all 89
     EDs and using new_total_anchored_pct (CSD + DA combined) as the confidence
     signal rather than CSD-only municipal_anchored_pct.

This produces a complete, province-wide set of shapefiles for both proposed maps.

Outputs:
  data/shapefiles/derived/v0_7_canonical_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_7_canonical_minority_2026_eds.gpkg
  analysis/reports/v0_1_build_v7_log.csv
  analysis/reports/v0_1_build_v7_summary.json

Forward:
  analysis/scripts/v0_1_mcmc_ensemble.py  (Run #3 — v0_7 geometries)
Backward:
  data/shapefiles/derived/v0_5_canonical_majority_2026_eds_da_anchored.gpkg
  data/shapefiles/derived/v0_5_canonical_minority_2026_eds_da_anchored.gpkg
  data/shapefiles/derived/v0_3_canonical_majority_2026_eds_swept.gpkg
  data/shapefiles/derived/v0_3_canonical_minority_2026_eds_swept.gpkg
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely import make_valid
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Point, Polygon
from shapely.ops import unary_union

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

ROOT  = Path(__file__).resolve().parent.parent.parent
DATA  = ROOT / "data" / "shapefiles" / "derived"
RPTS  = ROOT / "analysis" / "reports"

# Inputs
MAJ_V5 = DATA / "v0_5_canonical_majority_2026_eds_da_anchored.gpkg"
MIN_V5 = DATA / "v0_5_canonical_minority_2026_eds_da_anchored.gpkg"
MAJ_V3 = DATA / "v0_3_canonical_majority_2026_eds_swept.gpkg"
MIN_V3 = DATA / "v0_3_canonical_minority_2026_eds_swept.gpkg"

# Outputs
MAJ_OUT = DATA / "v0_7_canonical_majority_2026_eds.gpkg"
MIN_OUT = DATA / "v0_7_canonical_minority_2026_eds.gpkg"
LOG_CSV  = RPTS / "v0_1_build_v7_log.csv"
SUM_JSON = RPTS / "v0_1_build_v7_summary.json"

# Propagation config — same as v0_6
PROPAGATE_TOL_M       = 200.0
PCT_THRESHOLD         = 10.0
BUFFER_M              = 1.0
MAX_PASSES            = 5
ADJACENCY_MIN_LEN_M   = 10.0
PCT_COL               = "new_total_anchored_pct"   # CSD + DA combined
CRS                   = "EPSG:3401"


# ---------------------------------------------------------------------------
# Geometry helpers (identical to v0_6)
# ---------------------------------------------------------------------------

def _extract_lines(geom) -> list:
    if geom is None or geom.is_empty:
        return []
    t = geom.geom_type
    if t in ("LineString", "LinearRing"):
        return [geom]
    if t == "MultiLineString":
        return list(geom.geoms)
    if t == "GeometryCollection":
        out = []
        for g in geom.geoms:
            out.extend(_extract_lines(g))
        return out
    return []


def _snap_vertices(ring_coords: np.ndarray, donor_line, shared_line,
                   tol: float) -> tuple[np.ndarray, int]:
    new_coords = ring_coords.copy()
    n = 0
    for i, (x, y) in enumerate(ring_coords):
        pt = Point(x, y)
        if shared_line.distance(pt) <= tol:
            nearest = donor_line.interpolate(donor_line.project(pt))
            new_coords[i, 0] = nearest.x
            new_coords[i, 1] = nearest.y
            n += 1
    return new_coords, n


def _rebuild_polygon(original: Polygon, new_ext: np.ndarray) -> Polygon:
    holes = [list(ir.coords) for ir in original.interiors]
    try:
        p = Polygon(new_ext.tolist(), holes)
    except Exception:
        p = original
    return make_valid(p)


# ---------------------------------------------------------------------------
# Step 1: fill null geometries from v0_3 fallback
# ---------------------------------------------------------------------------

def fill_nulls_from_v3(v5: gpd.GeoDataFrame, v3: gpd.GeoDataFrame,
                        label: str) -> gpd.GeoDataFrame:
    """
    For each row in v5 with null geometry, substitute the v0_3 swept geometry.
    Sets new_total_anchored_pct to 0 for fallback rows (no anchoring applied).
    Adds a boolean column v3_fallback for transparency.
    """
    gdf = v5.copy()
    if PCT_COL not in gdf.columns:
        gdf[PCT_COL] = 0.0
    gdf["v3_fallback"] = False

    v3_lookup = dict(zip(v3["name_2026"], v3.geometry))
    null_mask = gdf.geometry.isna() | gdf.geometry.is_empty

    n_filled = 0
    still_null = []
    for idx in gdf[null_mask].index:
        name = gdf.at[idx, "name_2026"]
        fallback_geom = v3_lookup.get(name)
        if fallback_geom is not None and not fallback_geom.is_empty:
            gdf.at[idx, "geometry"] = make_valid(fallback_geom)
            gdf.at[idx, PCT_COL] = 0.0   # v0_3 has no anchoring quality
            gdf.at[idx, "v3_fallback"] = True
            n_filled += 1
            print(f"  [{label}] v0_3 fallback applied: {name}")
        else:
            still_null.append(name)

    if still_null:
        print(f"  [{label}] WARNING: {len(still_null)} ED(s) still null after "
              f"v0_3 fallback — dropping: {still_null}")
        gdf = gdf[~(gdf.geometry.isna() | gdf.geometry.is_empty)].copy()

    print(f"  [{label}] Null fill: {n_filled} recovered, "
          f"{len(still_null)} unrecoverable, {len(gdf)} EDs retained.")
    return gdf.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Step 2: multi-pass confidence propagation
# ---------------------------------------------------------------------------

def _propagation_pass(gdf: gpd.GeoDataFrame,
                      pass_num: int) -> tuple[gpd.GeoDataFrame, list[dict], int]:
    log_rows: list[dict] = []
    n = len(gdf)

    left_df = gpd.GeoDataFrame(
        {"_lid": np.arange(n),
         "name_2026": gdf["name_2026"].values,
         PCT_COL: gdf[PCT_COL].values},
        geometry=gdf.geometry.values, crs=gdf.crs,
    )
    right_df = gpd.GeoDataFrame(
        {"_rid": np.arange(n),
         "name_2026": gdf["name_2026"].values,
         PCT_COL: gdf[PCT_COL].values},
        geometry=[g.buffer(BUFFER_M) for g in gdf.geometry.values], crs=gdf.crs,
    )

    joined = gpd.sjoin(left_df, right_df, how="inner", predicate="intersects")
    pairs  = joined[joined["_lid"] < joined["_rid"]].copy()

    geoms = gdf.geometry.values.copy()
    events = 0

    for _, row in pairs.iterrows():
        i, j = int(row["_lid"]), int(row["_rid"])
        pct_a = float(row[f"{PCT_COL}_left"])
        pct_b = float(row[f"{PCT_COL}_right"])

        if pct_a >= pct_b:
            donor_idx, recv_idx = i, j
            donor_pct, recv_pct = pct_a, pct_b
            donor_geom, recv_geom = geoms[i], geoms[j]
            donor_name = row["name_2026_left"]
            recv_name  = row["name_2026_right"]
        else:
            donor_idx, recv_idx = j, i
            donor_pct, recv_pct = pct_b, pct_a
            donor_geom, recv_geom = geoms[j], geoms[i]
            donor_name = row["name_2026_right"]
            recv_name  = row["name_2026_left"]

        if donor_pct - recv_pct < PCT_THRESHOLD:
            continue

        try:
            shared = donor_geom.intersection(recv_geom)
        except Exception:
            continue

        lines = _extract_lines(shared)
        if not lines:
            continue
        total_len = sum(ln.length for ln in lines)
        if total_len < ADJACENCY_MIN_LEN_M:
            continue

        shared_line = unary_union(lines) if len(lines) > 1 else lines[0]

        try:
            donor_boundary = donor_geom.boundary
        except Exception:
            continue

        # Unwrap receiver to a single Polygon for rebuilding
        recv_for_rebuild = recv_geom
        if recv_geom.geom_type == "MultiPolygon":
            recv_for_rebuild = max(recv_geom.geoms, key=lambda g: g.area)
        elif recv_geom.geom_type == "GeometryCollection":
            polys = [g for g in recv_geom.geoms if g.geom_type in ("Polygon", "MultiPolygon")]
            if not polys:
                continue
            recv_for_rebuild = max(polys, key=lambda g: g.area)
            if recv_for_rebuild.geom_type == "MultiPolygon":
                recv_for_rebuild = max(recv_for_rebuild.geoms, key=lambda g: g.area)

        if recv_for_rebuild.geom_type != "Polygon":
            continue

        ext = np.array(list(recv_for_rebuild.exterior.coords), dtype=float)
        try:
            new_ext, n_snapped = _snap_vertices(ext, donor_boundary, shared_line, PROPAGATE_TOL_M)
        except Exception:
            continue

        if n_snapped == 0:
            continue

        try:
            new_recv = _rebuild_polygon(recv_for_rebuild, new_ext)
        except Exception:
            continue

        if new_recv is None or new_recv.is_empty or not new_recv.is_valid:
            new_recv = make_valid(new_recv) if new_recv is not None else recv_geom

        geoms[recv_idx] = new_recv
        events += 1

        log_rows.append({
            "pass": pass_num,
            "donor": donor_name,
            "receiver": recv_name,
            "donor_pct": round(donor_pct, 2),
            "receiver_pct": round(recv_pct, 2),
            "pct_diff": round(donor_pct - recv_pct, 2),
            "shared_length_m": round(total_len, 1),
            "vertices_snapped": n_snapped,
        })

    out = gdf.copy()
    out["geometry"] = list(geoms)
    return out, log_rows, events


def propagate(gdf: gpd.GeoDataFrame, label: str) -> tuple[gpd.GeoDataFrame, list[dict], dict]:
    pct_before = gdf[PCT_COL].mean()
    all_logs: list[dict] = []

    print(f"\n[{label}] Propagating — {len(gdf)} EDs, mean {PCT_COL}={pct_before:.1f}%")

    for pass_num in range(1, MAX_PASSES + 1):
        gdf, logs, events = _propagation_pass(gdf, pass_num)
        all_logs.extend(logs)
        snapped = sum(r["vertices_snapped"] for r in logs)
        print(f"  Pass {pass_num}: {events} pair(s), {snapped} vertices snapped")
        if events == 0:
            print(f"  Converged after {pass_num} pass(es).")
            break
    else:
        print(f"  Reached MAX_PASSES={MAX_PASSES}.")

    gdf["geometry"] = gdf["geometry"].apply(lambda g: make_valid(g) if g is not None else g)

    total_km = sum(r["shared_length_m"] for r in all_logs) / 1000.0
    stats = {
        "label": label,
        "n_eds": len(gdf),
        "n_v3_fallback": int(gdf.get("v3_fallback", pd.Series(False)).sum()),
        "passes_run": max((r["pass"] for r in all_logs), default=0),
        "total_pairs_propagated": len(all_logs),
        "total_shared_boundary_improved_km": round(total_km, 3),
        "mean_anchored_pct_before": round(float(pct_before), 4),
    }
    print(f"  [{label}] Done: {len(all_logs)} pair-passes, {total_km:.2f} km improved.")
    return gdf, all_logs, stats


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    t0 = time.time()
    RPTS.mkdir(parents=True, exist_ok=True)

    print(f"[v0_7 builder] Loading inputs...")
    maj_v3 = gpd.read_file(MAJ_V3).to_crs(CRS)
    min_v3 = gpd.read_file(MIN_V3).to_crs(CRS)

    all_logs: list[dict] = []
    all_stats: list[dict] = []

    for label, path_v5, path_v3, path_out in [
        ("majority", MAJ_V5, MAJ_V3, MAJ_OUT),
        ("minority", MIN_V5, MIN_V3, MIN_OUT),
    ]:
        print(f"\n{'='*60}")
        print(f"[{label}] Loading v0_5: {path_v5.name}")
        gdf = gpd.read_file(path_v5)
        if gdf.crs is None or gdf.crs.to_epsg() != 3401:
            gdf = gdf.to_crs(CRS)

        if PCT_COL not in gdf.columns:
            raise ValueError(f"Column '{PCT_COL}' missing from {path_v5.name}")

        v3_ref = gpd.read_file(path_v3).to_crs(CRS)

        # Step 1: fill nulls
        n_null_before = int(gdf.geometry.isna().sum())
        print(f"  {n_null_before} null-geometry ED(s) in v0_5 — applying v0_3 fallback...")
        gdf = fill_nulls_from_v3(gdf, v3_ref, label)

        # Step 2: propagate
        gdf_out, logs, stats = propagate(gdf, label)
        all_logs.extend(logs)
        all_stats.append(stats)

        print(f"  Writing {path_out.name} ({len(gdf_out)} EDs)...")
        gdf_out.to_file(path_out, driver="GPKG")
        print(f"  Written: {path_out}")

    # Log CSV
    if all_logs:
        pd.DataFrame(all_logs).to_csv(LOG_CSV, index=False)
        print(f"\nLog CSV: {LOG_CSV}")

    # Summary JSON
    elapsed = round(time.time() - t0, 1)
    summary = {
        "elapsed_seconds": elapsed,
        "propagate_tol_m": PROPAGATE_TOL_M,
        "pct_threshold": PCT_THRESHOLD,
        "pct_col_used": PCT_COL,
        "max_passes": MAX_PASSES,
        "maps": all_stats,
    }
    with open(SUM_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary JSON: {SUM_JSON}")
    print(f"\n[v0_7 builder] Done in {elapsed:.1f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
