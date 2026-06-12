# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
score_anchoring.py — Lane-2 Dangerzone metric #1 (municipal anchoring %)
========================================================================

Lane 2 (Structural), Ancillary: Municipal-boundary anchoring fraction
Standalone — result feeds §5.8.5 and §6 structural synthesis

Wraps the operational definition documented in
`analysis/scripts/municipal_anchoring.py` (and validated against 2019 in
`analysis/scripts/municipal_anchoring_2019_baseline.py`) as a
single-input CLI scoring function suitable for batch evaluation across the
100,000-plan ReCom ensemble.

Operational definition (held identical to the audit's anchoring runs). The
scorer is substrate-agnostic: it computes anchored % from whatever shapefile
you point it at. Reference values produced by this methodology, for the
records:

  * **Canonical (current, post-2026-05-06 official EA shapefiles):**
    majority 80.0 % / minority 72.0 % / 2019 enacted ≈ 75 %, all within
    the 70-85 % Canadian comparator norm.
  * **DPG-era (RETRACTED on canonical recomputation; kept here for
    trail-of-work transparency):** majority 71.0 % / minority 14.5 % /
    2019 enacted 75.2 %. The DPG-era 4.9× asymmetry did not survive
    canonical geometry — see README §"What the audit finds" and
    methods-paper §7.1, Stage 9.

The script logic below is unchanged across the DPG → canonical transition;
only the inputs differ. The operational steps are:

  1. Load the input shapefile/GPKG (any polygon layer, any CRS).
  2. Load the StatsCan 2021 CSD boundaries (the audit's AMA-equivalent
     gazette reference layer at
     `data/shapefiles/reference/alberta_2021_csds.gpkg`); reproject to
     match the input CRS; union all CSD boundaries into one
     MultiLineString edge network.
  3. For every polygon in the input, walk its boundary at 50m vertex
     spacing (VERTEX_DENSIFY_M); for each densified vertex, snap to the
     nearest CSD edge if the edge is within 500m (SNAP_TOL_M); otherwise
     leave the vertex on its original DPG location.
  4. Sum the original-densified segment length whose head-vertex was
     snapped — that is the "anchored" perimeter of the polygon.
  5. Sum across all polygons. Return:
        anchored_pct = 100.0 * total_anchored_m / total_perimeter_m
     printed to stdout as a single floating-point number with one
     decimal place. Identical formula to the headline `_pct_coverage`
     in `municipal_anchoring.py:609`.

Parameters held identical across DPG-era and canonical runs:
    SNAP_TOL_M           = 500.0    (matches DPG ±500m error budget; tolerable
                                     on canonical because canonical edges fall
                                     well within the same band)
    VERTEX_DENSIFY_M     = 50.0
    USE_DA_SUPPLEMENT    = False    (no-DA-supplement run, matches both the
                                     retracted DPG-era headline and the
                                     canonical headline)
    No topology re-resolve pass — we are computing a metric, not
    producing a v0_4 GPKG.

CLI:
    python analysis/scripts/score_anchoring.py --shapefile PATH

Output:
    A single line on stdout: anchored_pct as a float (e.g. "80.0").

Forward:
    findings/dangerzone_metric_definitions.md
    analysis/scripts/score_hybridization.py
Backward:
    analysis/scripts/municipal_anchoring.py
    analysis/scripts/municipal_anchoring_2019_baseline.py
    data/shapefiles/reference/alberta_2021_csds.gpkg
"""
from __future__ import annotations

# Version: 0.9 (2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import argparse
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
from shapely.geometry import LinearRing, LineString, MultiLineString, Point
from shapely.ops import linemerge, unary_union
from shapely.strtree import STRtree

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
CSD_GPKG = data_loader._resolve_path("data") / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"

# Held identical across DPG-era (retracted 71.0 / 14.5 / 75.2) and canonical
# (current 80.0 / 72.0 / ~75) runs — scorer is substrate-agnostic.
SNAP_TOL_M: float = 500.0
VERTEX_DENSIFY_M: float = 50.0


def _normalise_edges(edges) -> MultiLineString:
    if edges.geom_type == "MultiLineString":
        edges = linemerge(edges)
    if edges.geom_type == "LineString":
        edges = MultiLineString([edges])
    if edges.geom_type == "GeometryCollection":
        lines = [
            g for g in edges.geoms if g.geom_type in ("LineString", "MultiLineString")
        ]
        edges = unary_union(lines)
    return edges


def _load_csd_edges(target_crs) -> MultiLineString:
    csd = gpd.read_file(CSD_GPKG).to_crs(target_crs)
    csd_edges = unary_union(
        [g.boundary for g in csd.geometry if g is not None and not g.is_empty]
    )
    return _normalise_edges(csd_edges)


def _densify(ring: LinearRing, step: float) -> list[tuple[float, float]]:
    line = LineString(ring.coords)
    L = line.length
    if L <= 0:
        return list(ring.coords)
    n = max(int(np.ceil(L / step)), 8)
    ds = np.linspace(0.0, L, n + 1)[:-1]
    return [(line.interpolate(d).x, line.interpolate(d).y) for d in ds]


def _measure_ring(
    ring: LinearRing,
    edge_lines: list,
    tree: STRtree,
    snap_tol: float,
) -> tuple[float, float]:
    """Return (perim_m, anchored_m) for a single ring."""
    coords = _densify(ring, VERTEX_DENSIFY_M)
    if len(coords) < 4:
        coords = list(ring.coords)
    snapped_flags: list[bool] = []
    for x, y in coords:
        p = Point(x, y)
        cand_idxs = tree.query(p.buffer(snap_tol))
        snapped = False
        if len(cand_idxs):
            nearest_d = snap_tol + 1.0
            for idx in cand_idxs:
                edge = edge_lines[int(idx)]
                np_pt = edge.interpolate(edge.project(p))
                d = p.distance(np_pt)
                if d < nearest_d:
                    nearest_d = d
            if nearest_d <= snap_tol:
                snapped = True
        snapped_flags.append(snapped)

    # Per-segment perimeter and "raw anchored" (no contiguity filter)
    perim = 0.0
    anchored_raw = 0.0
    seg_lengths: list[float] = []
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        seg = float(np.hypot(x2 - x1, y2 - y1))
        seg_lengths.append(seg)
        perim += seg
        if snapped_flags[i]:
            anchored_raw += seg

    # Contiguous-≥1km filter (T4.10-anchor landed 2026-06-12 per T1.7 R2 Ref #10):
    # the report definition requires anchored runs to be ≥ MIN_RUN_M of contiguous
    # snapped segments. Accumulate run lengths; only count runs that clear the floor.
    MIN_RUN_M = 1000.0
    anchored_filtered = 0.0
    run = 0.0
    for flag, seg in zip(snapped_flags, seg_lengths):
        if flag:
            run += seg
        else:
            if run >= MIN_RUN_M:
                anchored_filtered += run
            run = 0.0
    # Final run check (wraps around the ring; close it)
    if run >= MIN_RUN_M:
        anchored_filtered += run

    return perim, anchored_filtered


def score_anchoring(shapefile_or_gdf) -> float:
    """Compute the province-wide municipal-anchored-perimeter percentage.

    Accepts either a path (str/Path) to a shapefile/GPKG, or an already-loaded
    GeoDataFrame. Callers that have already pre-processed `eds` (reprojected,
    filtered) should pass the GeoDataFrame so this function honours the
    preprocessing instead of re-reading the file from disk.
    """
    if isinstance(shapefile_or_gdf, gpd.GeoDataFrame):
        eds = shapefile_or_gdf
        source_desc = f"<GeoDataFrame n={len(eds)}>"
    else:
        shapefile_path = Path(shapefile_or_gdf)
        eds = gpd.read_file(shapefile_path)
        source_desc = str(shapefile_path)
    if eds.crs is None:
        raise ValueError(f"{source_desc} has no CRS; cannot project to CSD layer")
    edges = _load_csd_edges(eds.crs)

    # Build STRtree once over individual line strings
    edge_lines: list = []
    if edges.geom_type == "MultiLineString":
        edge_lines.extend(list(edges.geoms))
    elif edges.geom_type == "LineString":
        edge_lines.append(edges)
    else:
        for g in getattr(edges, "geoms", [edges]):
            if g.geom_type == "LineString":
                edge_lines.append(g)
            elif g.geom_type == "MultiLineString":
                edge_lines.extend(list(g.geoms))
    tree = STRtree(edge_lines)

    total_perim = 0.0
    total_anchored = 0.0
    for geom in eds.geometry:
        if geom is None or geom.is_empty:
            continue
        if geom.geom_type == "MultiPolygon":
            parts = list(geom.geoms)
        elif geom.geom_type == "Polygon":
            parts = [geom]
        else:
            parts = [g for g in getattr(geom, "geoms", []) if g.geom_type == "Polygon"]
        for poly in parts:
            p, a = _measure_ring(poly.exterior, edge_lines, tree, SNAP_TOL_M)
            total_perim += p
            total_anchored += a
            for hole in poly.interiors:
                p, a = _measure_ring(hole, edge_lines, tree, SNAP_TOL_M)
                total_perim += p
                total_anchored += a

    if total_perim <= 0:
        return 0.0
    return 100.0 * total_anchored / total_perim


def main():
    ap = argparse.ArgumentParser(
        description="Compute municipal-anchoring % for a single map shapefile"
    )
    ap.add_argument(
        "--shapefile",
        required=True,
        type=Path,
        help="Path to .shp or .gpkg containing electoral-division polygons",
    )
    args = ap.parse_args()
    if not args.shapefile.exists():
        print(f"ERROR: shapefile not found: {args.shapefile}", file=sys.stderr)
        sys.exit(2)
    if not CSD_GPKG.exists():
        print(f"ERROR: CSD reference layer missing: {CSD_GPKG}", file=sys.stderr)
        sys.exit(2)
    pct = score_anchoring(args.shapefile)
    print(f"{pct:.1f}")


if __name__ == "__main__":
    main()
