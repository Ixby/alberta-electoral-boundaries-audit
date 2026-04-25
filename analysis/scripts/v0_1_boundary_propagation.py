"""
Boundary Confidence Propagation — Share high-confidence segments across ED pairs
================================================================================
When building electoral district (ED) shapefiles from raster maps, some boundary
segments are traced with high confidence (e.g., they snap to a known municipal
boundary) while adjacent segments on neighbouring EDs are fuzzy. Because ED
boundaries must match their neighbours exactly, we can use the high-confidence
version of a shared segment to fix the low-confidence version.

**Algorithm.**

1. Load v0_4 anchored GeoPackages (which carry `municipal_anchored_pct` per ED —
   higher = more confident in that polygon's boundary geometry).
2. For each pair of adjacent EDs (A, B) that share a boundary segment:
   a. Compute the shared boundary: A.geometry.intersection(B.geometry) →
      LineString or MultiLineString.
   b. Identify the "donor" (higher anchored_pct) and "receiver" (lower).
   c. If donor_pct > receiver_pct + PCT_THRESHOLD (default 10 pp), snap the
      receiver's boundary vertices that fall along the shared segment to the
      nearest point on the donor's corresponding segment, within
      PROPAGATE_TOL_M = 200 m.
   d. Rebuild the receiver's polygon from the snapped boundary.
3. Run multiple passes (up to MAX_PASSES = 5) until convergence (no more
   propagation events).
4. Call make_valid() on all geometries, then emit v0_6 GeoPackages.

**Snapping detail.**  For each vertex of the receiver polygon that lies within
PROPAGATE_TOL_M of the shared boundary line, we find the nearest point on the
donor's corresponding boundary LineString and move that vertex there. Vertices
farther than PROPAGATE_TOL_M keep their original position.

**Adjacency detection.**  A spatial join with predicate='intersects' on a 1 m
buffer is used to find neighbour pairs, then the actual shared boundary is
computed via geometric intersection and filtered to linear geometry (length > 0).

**Outputs.**
  data/shapefiles/derived/v0_6_canonical_majority_2026_eds_propagated.gpkg
  data/shapefiles/derived/v0_6_canonical_minority_2026_eds_propagated.gpkg
  analysis/reports/v0_1_boundary_propagation_log.csv  (per-pair detail)
  analysis/reports/v0_1_boundary_propagation_summary.json

Forward:
  analysis/scripts/v0_1_phase_4c_va_attribution_maup_v2.py  (consumes derived
      geometries for MAUP area-weighted attribution)
Backward:
  analysis/scripts/v0_1_municipal_anchoring.py
  data/shapefiles/derived/v0_4_canonical_majority_2026_eds_anchored.gpkg
  data/shapefiles/derived/v0_4_canonical_minority_2026_eds_anchored.gpkg
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely import make_valid
from shapely.geometry import (
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.ops import unary_union

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "analysis" / "reports"

MAJ_IN = DATA / "shapefiles" / "derived" / "v0_4_canonical_majority_2026_eds_anchored.gpkg"
MIN_IN = DATA / "shapefiles" / "derived" / "v0_4_canonical_minority_2026_eds_anchored.gpkg"

MAJ_OUT = DATA / "shapefiles" / "derived" / "v0_6_canonical_majority_2026_eds_propagated.gpkg"
MIN_OUT = DATA / "shapefiles" / "derived" / "v0_6_canonical_minority_2026_eds_propagated.gpkg"

LOG_CSV = REPORTS / "v0_1_boundary_propagation_log.csv"
SUMMARY_JSON = REPORTS / "v0_1_boundary_propagation_summary.json"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROPAGATE_TOL_M = 200.0   # max vertex-to-donor-boundary distance for snapping
PCT_THRESHOLD   = 10.0    # donor must exceed receiver by this many pct points
BUFFER_M        = 1.0     # buffer used to detect adjacency via spatial join
MAX_PASSES      = 5       # convergence cap
ADJACENCY_MIN_LENGTH_M = 10.0  # minimum shared-boundary length to attempt propagation

CRS = "EPSG:3401"         # Alberta 10-TM Forest — projected, metres

# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _extract_lines(geom) -> list:
    """Return a flat list of LineString / LinearRing objects from any geometry."""
    if geom is None or geom.is_empty:
        return []
    gtype = geom.geom_type
    if gtype in ("LineString", "LinearRing"):
        return [geom]
    if gtype == "MultiLineString":
        return list(geom.geoms)
    if gtype == "GeometryCollection":
        out = []
        for g in geom.geoms:
            out.extend(_extract_lines(g))
        return out
    return []


def _snap_vertices_to_line(ring_coords: np.ndarray,
                            donor_line,
                            shared_line,
                            tol: float) -> tuple[np.ndarray, int]:
    """
    For each vertex in ring_coords that lies within `tol` metres of shared_line,
    project it onto donor_line (nearest point) and move it there.

    Returns (new_coords, n_snapped).
    """
    new_coords = ring_coords.copy()
    n_snapped = 0
    for i, (x, y) in enumerate(ring_coords):
        pt = Point(x, y)
        dist_to_shared = shared_line.distance(pt)
        if dist_to_shared <= tol:
            # Find nearest point on the donor boundary
            nearest = donor_line.interpolate(donor_line.project(pt))
            new_coords[i, 0] = nearest.x
            new_coords[i, 1] = nearest.y
            n_snapped += 1
    return new_coords, n_snapped


def _rebuild_polygon(original: Polygon, new_exterior_coords: np.ndarray) -> Polygon:
    """Rebuild a polygon with a replacement exterior ring, preserving interior rings."""
    new_shell = new_exterior_coords.tolist()
    holes = [list(ir.coords) for ir in original.interiors]
    try:
        rebuilt = Polygon(new_shell, holes)
    except Exception:
        rebuilt = original
    return make_valid(rebuilt)


def _polygon_exterior_coords(geom) -> np.ndarray:
    """Return exterior ring coordinates as (N, 2) float64 array."""
    if geom.geom_type == "MultiPolygon":
        # Use the largest component
        largest = max(geom.geoms, key=lambda g: g.area)
        geom = largest
    return np.array(list(geom.exterior.coords), dtype=float)


# ---------------------------------------------------------------------------
# Core: single-pass propagation over one GeoDataFrame
# ---------------------------------------------------------------------------

def _propagation_pass(gdf: gpd.GeoDataFrame,
                      pass_num: int,
                      pct_col: str = "municipal_anchored_pct"
                      ) -> tuple[gpd.GeoDataFrame, list[dict], int]:
    """
    Run one propagation pass over gdf.

    Returns:
        updated gdf, list of log-row dicts, total snapped-vertex count
    """
    log_rows: list[dict] = []
    total_snapped = 0
    propagation_events = 0

    # Build a buffered copy for adjacency detection.
    # Use explicit integer positional index so naming is unambiguous after sjoin.
    n = len(gdf)
    left_df = gpd.GeoDataFrame(
        {"_lid": np.arange(n),
         "name_2026": gdf["name_2026"].values,
         pct_col: gdf[pct_col].values},
        geometry=gdf.geometry.values,
        crs=gdf.crs,
    )
    right_df = gpd.GeoDataFrame(
        {"_rid": np.arange(n),
         "name_2026": gdf["name_2026"].values,
         pct_col: gdf[pct_col].values},
        geometry=[g.buffer(BUFFER_M) for g in gdf.geometry.values],
        crs=gdf.crs,
    )

    # Spatial join: find all pairs (left, right) whose extents touch/overlap
    joined = gpd.sjoin(left_df, right_df, how="inner", predicate="intersects")
    # joined has columns: _lid, name_2026_left, {pct_col}_left, _rid, name_2026_right, {pct_col}_right

    # Keep only A < B pairs to avoid double-processing and self-pairs
    pairs = joined[joined["_lid"] < joined["_rid"]].copy()

    # Work on a mutable copy of geometries indexed by original iloc position
    geoms = gdf.geometry.values.copy()   # numpy array of shapely geoms
    pcts  = gdf[pct_col].values.copy()   # numpy array of float

    pct_left_col  = f"{pct_col}_left"
    pct_right_col = f"{pct_col}_right"

    for _, row in pairs.iterrows():
        i = int(row["_lid"])
        j = int(row["_rid"])

        geom_a = geoms[i]
        geom_b = geoms[j]
        pct_a  = float(row[pct_left_col])
        pct_b  = float(row[pct_right_col])

        # Identify donor / receiver
        if pct_a >= pct_b:
            donor_idx, recv_idx = i, j
            donor_pct, recv_pct = pct_a, pct_b
            donor_geom, recv_geom = geom_a, geom_b
            donor_name = row["name_2026_left"]
            recv_name  = row["name_2026_right"]
        else:
            donor_idx, recv_idx = j, i
            donor_pct, recv_pct = pct_b, pct_a
            donor_geom, recv_geom = geom_b, geom_a
            donor_name = row["name_2026_right"]
            recv_name  = row["name_2026_left"]

        # Apply threshold
        if donor_pct - recv_pct < PCT_THRESHOLD:
            continue

        # Compute shared boundary
        try:
            shared = donor_geom.intersection(recv_geom)
        except Exception:
            continue

        lines = _extract_lines(shared)
        if not lines:
            continue

        total_shared_length = sum(ln.length for ln in lines)
        if total_shared_length < ADJACENCY_MIN_LENGTH_M:
            continue

        # Merge shared lines into one reference geometry for proximity queries
        shared_line = unary_union(lines) if len(lines) > 1 else lines[0]

        # Donor boundary (full exterior ring as LineString for projection)
        try:
            donor_boundary = donor_geom.boundary   # LinearRing or MultiLineString
        except Exception:
            continue

        # Snap receiver exterior ring vertices
        recv_geom_for_rebuild = recv_geom
        if recv_geom.geom_type == "MultiPolygon":
            recv_geom_for_rebuild = max(recv_geom.geoms, key=lambda g: g.area)
        elif recv_geom.geom_type == "GeometryCollection":
            # Extract largest polygon component
            polys = [g for g in recv_geom.geoms
                     if g.geom_type in ("Polygon", "MultiPolygon")]
            if not polys:
                continue
            recv_geom_for_rebuild = max(polys, key=lambda g: g.area)
            if recv_geom_for_rebuild.geom_type == "MultiPolygon":
                recv_geom_for_rebuild = max(recv_geom_for_rebuild.geoms, key=lambda g: g.area)

        if recv_geom_for_rebuild.geom_type != "Polygon":
            continue

        ext_coords = np.array(list(recv_geom_for_rebuild.exterior.coords), dtype=float)

        try:
            new_coords, n_snapped = _snap_vertices_to_line(
                ext_coords, donor_boundary, shared_line, PROPAGATE_TOL_M
            )
        except Exception:
            continue

        if n_snapped == 0:
            continue

        try:
            new_recv = _rebuild_polygon(recv_geom_for_rebuild, new_coords)
        except Exception:
            continue

        if new_recv is None or new_recv.is_empty or not new_recv.is_valid:
            new_recv = make_valid(new_recv) if new_recv is not None else recv_geom

        geoms[recv_idx] = new_recv
        propagation_events += 1
        total_snapped += n_snapped

        log_rows.append({
            "pass": pass_num,
            "donor": donor_name,
            "receiver": recv_name,
            "donor_pct": round(donor_pct, 2),
            "receiver_pct": round(recv_pct, 2),
            "pct_diff": round(donor_pct - recv_pct, 2),
            "shared_length_m": round(total_shared_length, 1),
            "vertices_snapped": n_snapped,
        })

    # Rebuild GDF with updated geometries
    out = gdf.copy()
    out["geometry"] = list(geoms)

    return out, log_rows, propagation_events


# ---------------------------------------------------------------------------
# High-level: multi-pass propagation + final make_valid
# ---------------------------------------------------------------------------

def propagate(gdf: gpd.GeoDataFrame,
              label: str,
              pct_col: str = "municipal_anchored_pct"
              ) -> tuple[gpd.GeoDataFrame, list[dict], dict]:
    """
    Run up to MAX_PASSES propagation rounds on gdf.

    Returns:
        (final_gdf, all_log_rows, stats_dict)
    """
    pct_before = gdf[pct_col].mean()
    all_logs: list[dict] = []

    print(f"\n[{label}] Starting propagation — {len(gdf)} EDs, "
          f"mean {pct_col}={pct_before:.2f}%")

    for pass_num in range(1, MAX_PASSES + 1):
        gdf, log_rows, events = _propagation_pass(gdf, pass_num, pct_col)
        all_logs.extend(log_rows)
        snapped_total = sum(r["vertices_snapped"] for r in log_rows)
        print(f"  Pass {pass_num}: {events} pair(s) propagated, "
              f"{snapped_total} vertices snapped")
        if events == 0:
            print(f"  Converged after {pass_num} pass(es).")
            break
    else:
        print(f"  Reached MAX_PASSES={MAX_PASSES} without full convergence.")

    # Final make_valid sweep
    gdf["geometry"] = gdf["geometry"].apply(lambda g: make_valid(g) if g is not None else g)

    # Recompute a simple proxy for anchored_pct improvement:
    # We cannot rerun the full anchoring pipeline here, so we report the
    # pct column unchanged (it reflects the *input* anchoring quality).
    # What we do report is total boundary length improved.
    total_shared_km = sum(r["shared_length_m"] for r in all_logs) / 1000.0
    total_pairs     = len(all_logs)
    passes_run      = max((r["pass"] for r in all_logs), default=0)

    stats = {
        "label": label,
        "n_eds": len(gdf),
        "passes_run": passes_run,
        "total_pairs_propagated": total_pairs,
        "total_shared_boundary_improved_km": round(total_shared_km, 3),
        "mean_anchored_pct_before": round(pct_before, 4),
        # pct_after is the same column value (unchanged — quality metric reflects
        # pre-propagation anchoring; would require re-running municipal_anchoring
        # to update). We note this explicitly in the summary.
        "mean_anchored_pct_after_note": (
            "municipal_anchored_pct unchanged — reflects v0_4 input quality. "
            "Run v0_1_municipal_anchoring.py on v0_6 output to recompute."
        ),
    }

    print(f"  [{label}] Done: {total_pairs} pair-passes, "
          f"{total_shared_km:.2f} km of shared boundary improved.")

    return gdf, all_logs, stats


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    t0 = time.time()
    REPORTS.mkdir(parents=True, exist_ok=True)

    all_log_rows: list[dict] = []
    all_stats: list[dict] = []

    for label, path_in, path_out in [
        ("majority", MAJ_IN, MAJ_OUT),
        ("minority", MIN_IN, MIN_OUT),
    ]:
        print(f"\n{'='*60}")
        print(f"Loading {label}: {path_in.name}")
        gdf = gpd.read_file(path_in)

        if gdf.crs is None or gdf.crs.to_epsg() != 3401:
            gdf = gdf.to_crs(CRS)

        # Ensure pct column exists
        pct_col = "municipal_anchored_pct"
        if pct_col not in gdf.columns:
            raise ValueError(f"Column '{pct_col}' not found in {path_in}")

        # Drop null/empty geometries (cannot be processed)
        n_before = len(gdf)
        gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
        gdf = gdf.reset_index(drop=True)
        n_dropped = n_before - len(gdf)
        if n_dropped:
            print(f"  Dropped {n_dropped} null/empty geometry row(s).")

        gdf_out, logs, stats = propagate(gdf, label, pct_col)
        all_log_rows.extend(logs)
        all_stats.append(stats)

        print(f"  Writing {path_out.name} ...")
        gdf_out.to_file(path_out, driver="GPKG")
        print(f"  Written: {path_out}")

    # Write log CSV
    if all_log_rows:
        log_df = pd.DataFrame(all_log_rows)
        log_df.to_csv(LOG_CSV, index=False)
        print(f"\nLog CSV: {LOG_CSV}  ({len(log_df)} rows)")
    else:
        print("\nNo propagation events — log CSV not written.")

    # Write summary JSON
    elapsed = round(time.time() - t0, 1)
    summary = {
        "elapsed_seconds": elapsed,
        "propagate_tol_m": PROPAGATE_TOL_M,
        "pct_threshold": PCT_THRESHOLD,
        "max_passes": MAX_PASSES,
        "buffer_adjacency_m": BUFFER_M,
        "maps": all_stats,
    }
    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary JSON: {SUMMARY_JSON}")

    # Console report
    print("\n" + "=" * 60)
    print("BOUNDARY PROPAGATION SUMMARY")
    print("=" * 60)
    for s in all_stats:
        print(f"\n  Map: {s['label']}")
        print(f"    EDs: {s['n_eds']}")
        print(f"    Passes run: {s['passes_run']}")
        print(f"    Pairs propagated: {s['total_pairs_propagated']}")
        print(f"    Shared boundary improved: {s['total_shared_boundary_improved_km']:.2f} km")
        print(f"    Mean anchored_pct (input v0_4): {s['mean_anchored_pct_before']:.2f}%")
    print(f"\n  Total elapsed: {elapsed}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
