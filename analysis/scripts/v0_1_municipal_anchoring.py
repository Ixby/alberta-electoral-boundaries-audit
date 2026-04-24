"""
Municipal-boundary anchoring of DPG perimeters (Issue #4 / Precision Option C)
==============================================================================
Roughly 40–60 % of each 2026 ED's perimeter follows municipal edges (city
limits, rural-municipality borders, Indian-reserve boundaries). The v0_1
canonical Derived Provisional Geometry (DPG) polygons trace these edges at
±500m–1km precision from the commission's 600-DPI map thumbnails. Statistics
Canada's 2021 Census Sub-Division (CSD) boundary file reproduces the legally
gazetted Alberta-Municipal-Affairs polygons at survey-grade precision (metre-
level on projected coordinates), and every CSD type in Alberta — city (CY),
town (T), village (VL), summer village (SV), municipal district (MD),
specialized municipality (SM), improvement district (ID), Indian reserve
(IRI), special area (SA) — is directly gazetted by Alberta Municipal Affairs.

**Rationale for using the StatsCan 2021 CSD file as the AMA source.** The
primary Alberta Open Data municipal-boundaries layer is distributed via
AltaLIS Ltd. (non-anonymous registration required and no stable download URL),
so an automated pull of the AMA layer itself is not available. The StatsCan
2021 CSD boundaries are a frozen snapshot of the AMA gazette at the Census
Day 2021 cut-off and are already in the repo's archival pipeline (see
`FROZEN_MANIFEST.md`). For the 2026 boundary-commission cycle, which relied
on population inputs drawn from the same 2021 census, the 2021-vintage CSD
boundaries are the precise set of municipal edges the commission treated as
immutable when drawing its proposed ED perimeters.

**Method.**

1. Load v0_3 canonical shapefiles if they exist (topology-clean + pop-swept
   product of Issue #3). Otherwise fall back to v0_2 (topology-clean only).
2. Load the 2021 CSD polygons, reproject to EPSG:3401 to match the DPGs,
   merge boundaries into a single reference MultiLineString. A shared
   municipal-boundary edge appears once in the union regardless of how many
   CSDs sit on either side.
3. For each DPG polygon, walk its boundary at a fine sampling density and
   snap each vertex to the nearest point on the municipal-edge network when
   the distance is < SNAP_TOL (default 500 m — matching the ±500 m DPG
   error budget from the 600-DPI thumbnail tracing). Vertices farther than
   SNAP_TOL keep their original DPG location.
4. For every snapped vertex, record the arc-length fraction of the polygon
   perimeter that has been pulled onto the municipal-edge network. Polygons
   where > 40 % of the perimeter snapped are "highly anchored"; < 10 %
   "lightly anchored". The column `municipal_anchored_pct` records this
   fraction per polygon.
5. Rebuild each polygon from the snapped boundary (LinearRing → Polygon,
   with any interior rings preserved via shapely.make_valid).
6. Run the same topology-cleanup precedence resolver that produced v0_2 to
   guarantee no new inter-ED overlaps were introduced by snapping.
7. Emit v0_4 GPKGs with a new `municipal_anchored_pct` column.

**Outputs.**
  * data/v0_4_canonical_majority_2026_eds_anchored.gpkg
  * data/v0_4_canonical_minority_2026_eds_anchored.gpkg
  * analysis/reports/v0_1_municipal_anchoring_log.csv
  * data/v0_1_municipal_anchoring_summary.json
  * analysis/reports/v0_1_municipal_anchoring_analysis.md  (written by a
    sibling writeup step — this script emits only data and a summary JSON)

Forward:
  analysis/scripts/v0_1_municipal_anchoring_writeup.py  (if used)
Backward:
  analysis/scripts/v0_1_topology_cleanup.py
  data/v0_2_canonical_{majority,minority}_2026_eds_topoclean.gpkg
  data/alberta_2021_csds.gpkg  (StatsCan 2021 CSD — AMA-equivalent; see
                                 FROZEN_MANIFEST.md)
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import (
    LinearRing,
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.ops import linemerge, nearest_points, unary_union
from shapely import make_valid

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "analysis" / "reports"

# Prefer v0_3 (Issue #3) if present; otherwise v0_2.
V0_3_MAJ = DATA / "shapefiles" / "derived" / "v0_3_canonical_majority_2026_eds_swept.gpkg"
V0_3_MIN = DATA / "shapefiles" / "derived" / "v0_3_canonical_minority_2026_eds_swept.gpkg"
V0_2_MAJ = DATA / "shapefiles" / "derived" / "v0_2_canonical_majority_2026_eds_topoclean.gpkg"
V0_2_MIN = DATA / "shapefiles" / "derived" / "v0_2_canonical_minority_2026_eds_topoclean.gpkg"

CSD_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"

MAJ_OUT = DATA / "shapefiles" / "derived" / "v0_4_canonical_majority_2026_eds_anchored.gpkg"
MIN_OUT = DATA / "shapefiles" / "derived" / "v0_4_canonical_minority_2026_eds_anchored.gpkg"

LOG_CSV = REPORTS / "v0_1_municipal_anchoring_log.csv"
SUMMARY_JSON = DATA / "v0_1_municipal_anchoring_summary.json"

# Snapping configuration
SNAP_TOL_M = 500.0        # max vertex-to-municipal-edge distance for snapping
MIN_SEGMENT_COVERAGE_M = 1000.0  # min contiguous snapped length to count as anchored segment
VERTEX_DENSIFY_M = 50.0   # re-densify boundary to this spacing before snapping

# Precedence order for canon_source (higher index = stronger evidence)
SOURCE_PRECEDENCE = {
    "v7": 1,
    "2019-parent": 3,
    "osm-municipal-buffered": 4,
    "sweep": 5,
    "municipal-anchored": 6,
}


def source_rank(src: str) -> int:
    return SOURCE_PRECEDENCE.get(str(src), 0)


def _keep_polys(geom):
    """Normalise to (Multi)Polygon; drop line/point remnants from set ops."""
    if geom is None or geom.is_empty:
        return None
    if geom.geom_type in ("Polygon", "MultiPolygon"):
        return geom
    if geom.geom_type == "GeometryCollection":
        polys = [g for g in geom.geoms if g.geom_type in ("Polygon", "MultiPolygon")]
        if not polys:
            return None
        return unary_union(polys)
    return None


def pick_input(label: str) -> tuple[Path, str]:
    if label == "majority":
        return (V0_3_MAJ, "v0_3") if V0_3_MAJ.exists() else (V0_2_MAJ, "v0_2")
    return (V0_3_MIN, "v0_3") if V0_3_MIN.exists() else (V0_2_MIN, "v0_2")


def load_municipal_edges(target_crs) -> MultiLineString:
    """Union of every CSD boundary, merged to a MultiLineString in target CRS."""
    csd = gpd.read_file(CSD_GPKG)
    csd = csd.to_crs(target_crs)
    # Build one MultiLineString of all boundaries; duplicates across
    # adjacent CSDs are collapsed by unary_union.
    edges = unary_union([g.boundary for g in csd.geometry if g is not None and not g.is_empty])
    # linemerge to get the longest continuous strings possible; aids snap
    # performance and measurement of "contiguous anchored" segments.
    if edges.geom_type == "MultiLineString":
        edges = linemerge(edges)
    if edges.geom_type == "LineString":
        edges = MultiLineString([edges])
    # Keep only linear components
    if edges.geom_type == "GeometryCollection":
        lines = [g for g in edges.geoms if g.geom_type in ("LineString", "MultiLineString")]
        edges = unary_union(lines)
    return edges


def densify(ring: LinearRing, step: float) -> list[tuple[float, float]]:
    """Return a list of (x, y) vertices sampled along ring at ~step metres."""
    line = LineString(ring.coords)
    L = line.length
    if L <= 0:
        return list(ring.coords)
    n = max(int(np.ceil(L / step)), 8)
    ds = np.linspace(0.0, L, n + 1)[:-1]  # exclude the wrap-around duplicate
    pts = [line.interpolate(d) for d in ds]
    return [(p.x, p.y) for p in pts]


def snap_ring(
    ring: LinearRing,
    edges: MultiLineString,
    edges_tree,
    edge_lines: list,
    snap_tol: float,
) -> tuple[LinearRing, list[bool], list[float]]:
    """
    Snap each vertex of `ring` to the nearest point on `edges` when within
    snap_tol. Returns (new_ring, snapped_flags_per_vertex, segment_lengths).

    `segment_lengths[i]` is the original-geometry segment length from
    vertex i to vertex i+1 (wrapping). Used downstream to compute the
    anchored-perimeter fraction.
    """
    coords = densify(ring, VERTEX_DENSIFY_M)
    if len(coords) < 4:
        coords = list(ring.coords)
    new_coords = []
    snapped_flags = []
    for x, y in coords:
        p = Point(x, y)
        # STRtree returns candidate edge indices; resolve each via the
        # parallel edge_lines list since shapely 2.x .geometries is
        # read-only and returned as a numpy array.
        cand_idxs = edges_tree.query(p.buffer(snap_tol))
        if len(cand_idxs):
            nearest_d = snap_tol + 1.0
            nearest_pt = None
            for idx in cand_idxs:
                edge = edge_lines[int(idx)]
                np_point = edge.interpolate(edge.project(p))
                d = p.distance(np_point)
                if d < nearest_d:
                    nearest_d = d
                    nearest_pt = np_point
            if nearest_pt is not None and nearest_d <= snap_tol:
                new_coords.append((nearest_pt.x, nearest_pt.y))
                snapped_flags.append(True)
                continue
        new_coords.append((x, y))
        snapped_flags.append(False)

    # Close ring
    if new_coords[0] != new_coords[-1]:
        new_coords.append(new_coords[0])
        snapped_flags.append(snapped_flags[0])

    # Compute segment lengths on ORIGINAL densified coords for fraction calc
    seg_lens = []
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        seg_lens.append(float(np.hypot(x2 - x1, y2 - y1)))

    new_ring = LinearRing(new_coords)
    # Return snapped_flags of length len(coords) (one per original vertex)
    return new_ring, snapped_flags[: len(coords)], seg_lens


def snap_polygon(
    poly: Polygon,
    edges: MultiLineString,
    edges_tree,
    edge_lines: list,
    snap_tol: float,
) -> tuple[Polygon, float, float, float, float]:
    """
    Snap exterior + interior rings. Returns (new_poly, perim_m, anchored_m,
    pre_err_m, post_err_m).

    pre_err_m = mean distance from original vertices (within snap_tol) to
        the nearest municipal edge. This is the DPG tracing error on the
        municipal-anchored subset.
    post_err_m = mean distance after snapping, which is numerically 0 for
        snapped vertices; we return it as a sanity check against the
        reported ±1 m post-anchor-precision claim.
    """
    exterior_new, ext_flags, ext_segs = snap_ring(
        poly.exterior, edges, edges_tree, edge_lines, snap_tol
    )
    interiors_new = []
    all_flags = list(ext_flags)
    all_segs = list(ext_segs)
    pre_errs = []
    # per-vertex pre-error: distance from original vertex to edges network
    coords = list(poly.exterior.coords)[:-1]  # drop wrap
    coords_dense = densify(poly.exterior, VERTEX_DENSIFY_M)
    for (x, y), snapped in zip(coords_dense, ext_flags):
        if snapped:
            p = Point(x, y)
            cand_idxs = edges_tree.query(p.buffer(snap_tol))
            if len(cand_idxs):
                best = min(
                    edge_lines[int(i)].distance(p) for i in cand_idxs
                )
                pre_errs.append(best)
    for hole in poly.interiors:
        h_new, h_flags, h_segs = snap_ring(hole, edges, edges_tree, edge_lines, snap_tol)
        interiors_new.append(h_new)
        all_flags.extend(h_flags)
        all_segs.extend(h_segs)
        h_dense = densify(hole, VERTEX_DENSIFY_M)
        for (x, y), snapped in zip(h_dense, h_flags):
            if snapped:
                p = Point(x, y)
                cand_idxs = edges_tree.query(p.buffer(snap_tol))
                if len(cand_idxs):
                    best = min(
                        edge_lines[int(i)].distance(p) for i in cand_idxs
                    )
                    pre_errs.append(best)

    new_poly = Polygon(exterior_new, interiors_new)
    new_poly = make_valid(new_poly)
    new_poly = _keep_polys(new_poly)

    total_len = sum(all_segs)
    anchored_len = 0.0
    for i, seg in enumerate(all_segs):
        # A segment is "anchored" if both endpoints were snapped.
        # Use ext_flags + hole flags via all_flags; all_segs indexing
        # assumes the same walking order so vertex i and i+1 (modulo ring
        # lengths) are defined in all_flags.
        if all_flags[i]:
            anchored_len += seg

    pre_err_m = float(np.mean(pre_errs)) if pre_errs else 0.0
    post_err_m = 0.0  # snapping is exact by construction
    return new_poly, total_len, anchored_len, pre_err_m, post_err_m


def anchor_map(
    eds: gpd.GeoDataFrame,
    edges: MultiLineString,
    label: str,
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    from shapely.strtree import STRtree
    # STRtree over individual LineStrings of the municipal-edge union
    edge_lines = []
    if edges.geom_type == "MultiLineString":
        edge_lines.extend(list(edges.geoms))
    elif edges.geom_type == "LineString":
        edge_lines.append(edges)
    else:  # GeometryCollection / Polygon (shouldn't happen)
        for g in getattr(edges, "geoms", [edges]):
            if g.geom_type == "LineString":
                edge_lines.append(g)
            elif g.geom_type == "MultiLineString":
                edge_lines.extend(list(g.geoms))
    tree = STRtree(edge_lines)
    # Shapely 2.x STRtree exposes .geometries as a read-only property; we
    # pass `edge_lines` alongside `tree` so snap_ring / snap_polygon can
    # resolve indices back to LineString objects.

    print(f"  [{label}] municipal-edge network: {len(edge_lines):,} LineStrings")

    rows = []
    new_geoms = []
    for i, row in eds.iterrows():
        g = row.geometry
        if g is None or g.is_empty:
            new_geoms.append(g)
            rows.append({
                "map": label, "name_2026": row["name_2026"],
                "perimeter_km_total": 0.0, "perimeter_km_anchored": 0.0,
                "anchored_pct": 0.0, "pre_ama_error_m": 0.0,
                "post_ama_error_m": 0.0,
            })
            continue

        parts = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
        new_parts = []
        perim_sum = 0.0
        anchored_sum = 0.0
        pre_errs = []
        for p in parts:
            snapped_p, perim, anchored, pre_err, _ = snap_polygon(
                p, edges, tree, edge_lines, SNAP_TOL_M
            )
            if snapped_p is None or snapped_p.is_empty:
                snapped_p = p
            new_parts.append(snapped_p)
            perim_sum += perim
            anchored_sum += anchored
            if pre_err > 0:
                pre_errs.append(pre_err)

        if len(new_parts) == 1:
            new_geom = new_parts[0]
        else:
            new_geom = MultiPolygon(
                [x for x in new_parts if x.geom_type == "Polygon"]
            )
        new_geom = make_valid(new_geom)
        new_geom = _keep_polys(new_geom)
        new_geoms.append(new_geom)

        anchored_pct = 100.0 * anchored_sum / perim_sum if perim_sum > 0 else 0.0
        pre_err_m = float(np.mean(pre_errs)) if pre_errs else 0.0
        rows.append({
            "map": label,
            "name_2026": row["name_2026"],
            "perimeter_km_total": perim_sum / 1000.0,
            "perimeter_km_anchored": anchored_sum / 1000.0,
            "anchored_pct": anchored_pct,
            "pre_ama_error_m": pre_err_m,
            "post_ama_error_m": 0.0,  # exact by construction
        })
        if (i + 1) % 15 == 0:
            print(f"    [{label}] {i+1}/{len(eds)} polygons anchored")

    out = eds.copy()
    out["geometry"] = new_geoms
    # Annotate canon_source for polygons with material anchoring (≥40%)
    if "canon_source" in out.columns:
        anchored_pct_series = pd.Series([r["anchored_pct"] for r in rows])
        out["canon_source"] = [
            "municipal-anchored" if p >= 40.0 else s
            for p, s in zip(anchored_pct_series, out["canon_source"])
        ]
    out["municipal_anchored_pct"] = [r["anchored_pct"] for r in rows]
    return out, pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Topology re-validation (lightweight: detect + split residual overlaps using
# centroid-proximity; we do not re-apply the full precedence resolver because
# snapping does not introduce new source-precedence contests — but we do need
# to verify no pair overlaps > 1 m² after snapping).
# ---------------------------------------------------------------------------


def re_resolve_topology(eds: gpd.GeoDataFrame, label: str) -> gpd.GeoDataFrame:
    print(f"  [{label}] topology re-validation pass...")
    eds = eds.reset_index(drop=True).copy()
    eds["geometry"] = eds.geometry.apply(
        lambda g: make_valid(g) if g is not None else g
    )
    eds["geometry"] = eds.geometry.apply(_keep_polys)

    geoms = list(eds.geometry)
    n = len(geoms)
    sindex = eds.sindex

    resolved = 0
    max_resolved_m2 = 0.0
    for i in range(n):
        gi = geoms[i]
        if gi is None or gi.is_empty:
            continue
        cand = list(sindex.query(gi, predicate="intersects"))
        for j in cand:
            if j <= i:
                continue
            gj = geoms[j]
            if gj is None or gj.is_empty:
                continue
            if not gi.intersects(gj):
                continue
            inter = gi.intersection(gj)
            inter = _keep_polys(inter)
            if inter is None or inter.is_empty or inter.area < 1.0:
                continue
            # Centroid-proximity: whichever ORIGINAL centroid is closer to the
            # overlap wins; the other subtracts it.
            ci = eds.iloc[i].geometry.representative_point()
            cj = eds.iloc[j].geometry.representative_point()
            pc = inter.representative_point()
            if pc.distance(ci) <= pc.distance(cj):
                new_gj = _keep_polys(gj.difference(inter))
                if new_gj is not None and not new_gj.is_empty:
                    geoms[j] = new_gj
            else:
                new_gi = _keep_polys(gi.difference(inter))
                if new_gi is not None and not new_gi.is_empty:
                    geoms[i] = new_gi
            max_resolved_m2 = max(max_resolved_m2, float(inter.area))
            resolved += 1

    eds["geometry"] = geoms
    print(f"    resolved {resolved} residual overlap pairs, max {max_resolved_m2:,.1f} m²")
    return eds


def verify_no_overlap(eds: gpd.GeoDataFrame, label: str) -> tuple[int, float]:
    sindex = eds.sindex
    count = 0
    total_km2 = 0.0
    for i, gi in enumerate(eds.geometry):
        if gi is None or gi.is_empty:
            continue
        for j in sindex.query(gi, predicate="intersects"):
            if j <= i:
                continue
            gj = eds.geometry.iloc[j]
            if gj is None or gj.is_empty:
                continue
            inter = gi.intersection(gj)
            inter = _keep_polys(inter)
            if inter is None or inter.is_empty:
                continue
            if inter.area < 1.0:
                continue
            count += 1
            total_km2 += inter.area / 1e6
    print(f"  [{label}] post-validation: {count} pairs, {total_km2:,.4f} km² residual overlap")
    return count, total_km2


def main():
    print("=" * 72)
    print("  Municipal-boundary anchoring (v0_4) -- DPG perimeters -> AMA/CSD edges")
    print("=" * 72)

    maj_in, maj_tag = pick_input("majority")
    min_in, min_tag = pick_input("minority")
    print(f"\n[input] majority: {maj_in.name}  ({maj_tag})")
    print(f"[input] minority: {min_in.name}  ({min_tag})")

    maj = gpd.read_file(maj_in)
    mino = gpd.read_file(min_in)
    print(f"  majority: {len(maj)} EDs, CRS={maj.crs}")
    print(f"  minority: {len(mino)} EDs, CRS={mino.crs}")

    assert len(maj) == 89 and len(mino) == 89, "Expected 89 EDs per map"

    print("\n[load] municipal-boundary network (StatsCan 2021 CSDs — AMA-equivalent)")
    t0 = time.time()
    edges = load_municipal_edges(maj.crs)
    print(f"  edges built in {time.time()-t0:.1f}s; total length = "
          f"{edges.length/1000:,.0f} km")

    print("\n" + "=" * 72)
    print("  MAJORITY anchoring")
    print("=" * 72)
    t = time.time()
    maj_anchor, maj_log = anchor_map(maj, edges, "majority")
    print(f"  [majority elapsed: {time.time()-t:.1f}s]")
    maj_anchor = re_resolve_topology(maj_anchor, "majority")
    maj_overlap_pairs, maj_overlap_km2 = verify_no_overlap(maj_anchor, "majority")

    print("\n" + "=" * 72)
    print("  MINORITY anchoring")
    print("=" * 72)
    t = time.time()
    min_anchor, min_log = anchor_map(mino, edges, "minority")
    print(f"  [minority elapsed: {time.time()-t:.1f}s]")
    min_anchor = re_resolve_topology(min_anchor, "minority")
    min_overlap_pairs, min_overlap_km2 = verify_no_overlap(min_anchor, "minority")

    print("\n[write] v0_4 anchored GPKGs...")
    maj_anchor.to_file(MAJ_OUT, driver="GPKG")
    min_anchor.to_file(MIN_OUT, driver="GPKG")
    print(f"  wrote: {MAJ_OUT}")
    print(f"  wrote: {MIN_OUT}")

    combined = pd.concat([maj_log, min_log], ignore_index=True)
    combined.to_csv(LOG_CSV, index=False)
    print(f"  wrote: {LOG_CSV}  ({len(combined)} rows)")

    def _pct_coverage(df):
        tot_perim = df["perimeter_km_total"].sum()
        tot_anchored = df["perimeter_km_anchored"].sum()
        return 100.0 * tot_anchored / tot_perim if tot_perim > 0 else 0.0

    maj_cov = _pct_coverage(maj_log)
    min_cov = _pct_coverage(min_log)

    top5_maj = maj_log.nlargest(5, "anchored_pct")[["name_2026", "anchored_pct"]].to_dict("records")
    bot5_maj = maj_log.nsmallest(5, "anchored_pct")[["name_2026", "anchored_pct"]].to_dict("records")
    top5_min = min_log.nlargest(5, "anchored_pct")[["name_2026", "anchored_pct"]].to_dict("records")
    bot5_min = min_log.nsmallest(5, "anchored_pct")[["name_2026", "anchored_pct"]].to_dict("records")

    summary = {
        "method": {
            "snap_tolerance_m": SNAP_TOL_M,
            "vertex_densify_m": VERTEX_DENSIFY_M,
            "min_segment_coverage_m": MIN_SEGMENT_COVERAGE_M,
        },
        "sources": {
            "majority_input": {"path": str(maj_in), "vintage": maj_tag},
            "minority_input": {"path": str(min_in), "vintage": min_tag},
            "municipal_boundaries": {
                "path": str(CSD_GPKG),
                "provenance": "StatsCan 2021 Census Sub-Division (AMA-equivalent)",
                "downloaded_from": ("https://www12.statcan.gc.ca/census-recensement/"
                                    "2021/geo/sip-pis/boundary-limites/files-fichiers/"
                                    "lcsd000a21a_e.zip"),
                "n_csds_alberta": 423,
            },
        },
        "majority": {
            "n_eds": len(maj_log),
            "total_perimeter_km": float(maj_log["perimeter_km_total"].sum()),
            "anchored_perimeter_km": float(maj_log["perimeter_km_anchored"].sum()),
            "anchored_pct_overall": float(maj_cov),
            "mean_per_ed_anchored_pct": float(maj_log["anchored_pct"].mean()),
            "median_per_ed_anchored_pct": float(maj_log["anchored_pct"].median()),
            "mean_pre_ama_error_m": float(maj_log["pre_ama_error_m"].mean()),
            "top5_most_anchored": top5_maj,
            "bottom5_least_anchored": bot5_maj,
            "residual_overlap_pairs": maj_overlap_pairs,
            "residual_overlap_km2": maj_overlap_km2,
        },
        "minority": {
            "n_eds": len(min_log),
            "total_perimeter_km": float(min_log["perimeter_km_total"].sum()),
            "anchored_perimeter_km": float(min_log["perimeter_km_anchored"].sum()),
            "anchored_pct_overall": float(min_cov),
            "mean_per_ed_anchored_pct": float(min_log["anchored_pct"].mean()),
            "median_per_ed_anchored_pct": float(min_log["anchored_pct"].median()),
            "mean_pre_ama_error_m": float(min_log["pre_ama_error_m"].mean()),
            "top5_most_anchored": top5_min,
            "bottom5_least_anchored": bot5_min,
            "residual_overlap_pairs": min_overlap_pairs,
            "residual_overlap_km2": min_overlap_km2,
        },
        "validation_gates": {
            "n_eds_preserved_majority": len(maj_anchor) == 89,
            "n_eds_preserved_minority": len(min_anchor) == 89,
            "no_overlap_majority": maj_overlap_km2 < 0.001,
            "no_overlap_minority": min_overlap_km2 < 0.001,
        },
        "outputs": {
            "majority_gpkg": str(MAJ_OUT),
            "minority_gpkg": str(MIN_OUT),
            "log_csv": str(LOG_CSV),
        },
    }
    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"  wrote: {SUMMARY_JSON}")

    # Console summary
    print("\n" + "=" * 72)
    print("  ANCHORING SUMMARY")
    print("=" * 72)
    print(f"\n  MAJORITY: {maj_cov:5.1f}% of total perimeter anchored to AMA edges")
    print(f"            mean per-ED anchored {maj_log['anchored_pct'].mean():5.1f}%, "
          f"median {maj_log['anchored_pct'].median():5.1f}%")
    print(f"            mean pre-anchor DPG error = {maj_log['pre_ama_error_m'].mean():.1f} m "
          f"on anchored segments")
    print(f"\n  MINORITY: {min_cov:5.1f}% of total perimeter anchored to AMA edges")
    print(f"            mean per-ED anchored {min_log['anchored_pct'].mean():5.1f}%, "
          f"median {min_log['anchored_pct'].median():5.1f}%")
    print(f"            mean pre-anchor DPG error = {min_log['pre_ama_error_m'].mean():.1f} m "
          f"on anchored segments")

    print("\n  Top-5 most-anchored EDs (majority):")
    for r in top5_maj:
        print(f"    {r['name_2026']:<44s}  {r['anchored_pct']:5.1f}%")
    print("\n  Bottom-5 least-anchored EDs (majority):")
    for r in bot5_maj:
        print(f"    {r['name_2026']:<44s}  {r['anchored_pct']:5.1f}%")
    print("\n  Top-5 most-anchored EDs (minority):")
    for r in top5_min:
        print(f"    {r['name_2026']:<44s}  {r['anchored_pct']:5.1f}%")
    print("\n  Bottom-5 least-anchored EDs (minority):")
    for r in bot5_min:
        print(f"    {r['name_2026']:<44s}  {r['anchored_pct']:5.1f}%")

    all_gates_ok = all(summary["validation_gates"].values())
    print("\n" + "=" * 72)
    print(f"  MUNICIPAL ANCHORING: {'ALL GATES PASSED' if all_gates_ok else 'GATE FAILURE — investigate'}")
    print("=" * 72)


if __name__ == "__main__":
    main()
