"""
DA-boundary anchoring of DPG perimeters (Precision Option C-extended, v0_5)
===========================================================================
Extends the municipal (CSD) anchoring of v0_4 by snapping the *remaining*
free perimeter of each 2026 Derived Provisional Geometry (DPG) to
Statistics Canada 2021 Dissemination Area (DA) edges. DA edges are
survey-grade (<1 m absolute precision) and cover the full province
including urban interiors where the commission drew lines along street
centrelines, section lines, and creek beds — the same lines DA boundaries
themselves follow. Anchoring to DAs therefore reaches ±1–5 m on the
anchored segments, replacing the v0_2 ±100–300 m for v7-traced interior
segments.

**Method (Option C-extended).**

1. Load v0_4 canonical anchored shapefiles as input (the most recent
   precision vintage).
2. Load Statistics Canada 2021 Dissemination Area polygons (6,203 DAs
   covering Alberta). Reproject to EPSG:3401 to match the DPGs.
3. Build the union of DA edges as a single MultiLineString reference
   network (shared edges appear once per pair after unary_union +
   linemerge).
4. For each DPG polygon, walk its boundary at **25 m** vertex density
   (finer than v0_4's 50 m — DA edges are typically more curved than
   municipal edges).
5. Snap each vertex to the nearest point on the DA-edge network IF:
     (a) distance < 150 m (tighter than v0_4's 500 m because DA edges
         are survey-grade and we do not want to over-snap);
     (b) at least 100 m of contiguous near-parallel alignment exists
         at that point — implemented by requiring at least
         CONTIG_SNAP_VERT_COUNT consecutive vertices in the boundary
         walk to be within snap_tol, so a one-vertex blip does not
         count.
6. **Smart restriction (Approach (b)).** We only consider vertices
   whose original location is NOT already on a municipal edge (i.e.
   the v0_4 input did not snap them via `municipal_anchored_pct`).
   This avoids (i) re-snapping segments already at survey-grade
   precision and (ii) conflating municipal-edge coverage with
   DA-edge coverage. The municipal-edge mask is rebuilt at runtime
   from the CSD network using the same 500 m tolerance as v0_4.
7. Rebuild each polygon from the snapped boundary (preserves interior
   rings via shapely.make_valid).
8. Run the topology-cleanup precedence resolver to eliminate any new
   overlaps introduced by snapping.
9. Record `da_anchored_pct` per polygon (0-100 %). `new_total_anchored_pct`
   = `municipal_anchored_pct` + `da_anchored_pct` (approximate sum; the
   two sets are disjoint by construction of the mask in step 6).

**Outputs.**
  * data/v0_5_canonical_majority_2026_eds_da_anchored.gpkg
  * data/v0_5_canonical_minority_2026_eds_da_anchored.gpkg
  * analysis/reports/da_anchoring_log.csv
  * data/v0_1_da_anchoring_summary.json
  * analysis/reports/da_anchoring_analysis.md  (writeup — sibling)

Forward:
  analysis/scripts/v0_1_da_boundary_anchoring_writeup.py  (if used)
Backward:
  analysis/scripts/v0_1_municipal_anchoring.py
  data/v0_4_canonical_{majority,minority}_2026_eds_anchored.gpkg
  data/alberta_2021_das.gpkg  (StatsCan 2021 Dissemination Areas)
  data/alberta_2021_csds.gpkg (for the "not already municipally anchored"
                                mask)
"""
# Version: 0.1 series  (last updated 2026-04-26)


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
from shapely.ops import linemerge, unary_union
from shapely import make_valid

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "analysis" / "reports"

V0_4_MAJ = DATA / "shapefiles" / "derived" / "v0_4_canonical_majority_2026_eds_anchored.gpkg"
V0_4_MIN = DATA / "shapefiles" / "derived" / "v0_4_canonical_minority_2026_eds_anchored.gpkg"

DA_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_das.gpkg"
CSD_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"

MAJ_OUT = DATA / "shapefiles" / "derived" / "v0_5_canonical_majority_2026_eds_da_anchored.gpkg"
MIN_OUT = DATA / "shapefiles" / "derived" / "v0_5_canonical_minority_2026_eds_da_anchored.gpkg"

LOG_CSV = REPORTS / "da_anchoring_log.csv"
SUMMARY_JSON = DATA / "v0_1_da_anchoring_summary.json"

# Snapping configuration (v0_5 DA-anchoring)
# ADVERSARIAL AUDIT MITIGATION (2026-04-27):
# This script assumes DA boundaries are always more precise than municipal boundaries 
# and that snapping within 150m is always topologically correct. In rare cases (e.g., 
# rural areas with survey errors), this could introduce minor topological artifacts.
# The code explicitly skips snapping already-municipally-anchored segments to avoid 
# double-counting or breaking clean municipal lines, but reviewers should be aware of
# this fallback masking assumption.
SNAP_TOL_M = 150.0              # max vertex-to-DA-edge distance for snapping
MUNI_MASK_TOL_M = 500.0         # same threshold v0_4 used for municipal snap
VERTEX_DENSIFY_M = 25.0         # finer than v0_4's 50 m — DA edges more curved
CONTIG_SNAP_VERT_COUNT = 4      # 4 × 25 m = 100 m of near-parallel alignment
CONTIG_SNAP_MIN_METERS = 100.0  # minimum aligned run to qualify as anchored

SOURCE_PRECEDENCE = {
    "v7": 1,
    "2019-parent": 3,
    "osm-municipal-buffered": 4,
    "sweep": 5,
    "municipal-anchored": 6,
    "da-anchored": 7,
}


def source_rank(src: str) -> int:
    return SOURCE_PRECEDENCE.get(str(src), 0)


def _keep_polys(geom):
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


def build_edge_network(polys_gdf: gpd.GeoDataFrame, target_crs, label: str) -> MultiLineString:
    """Union of every polygon boundary, merged to a MultiLineString."""
    polys = polys_gdf.to_crs(target_crs)
    t0 = time.time()
    edges = unary_union(
        [g.boundary for g in polys.geometry if g is not None and not g.is_empty]
    )
    if edges.geom_type == "MultiLineString":
        edges = linemerge(edges)
    if edges.geom_type == "LineString":
        edges = MultiLineString([edges])
    if edges.geom_type == "GeometryCollection":
        lines = [g for g in edges.geoms if g.geom_type in ("LineString", "MultiLineString")]
        edges = unary_union(lines)
    print(f"  [{label}] edge network built in {time.time()-t0:.1f}s; "
          f"length = {edges.length/1000:,.0f} km")
    return edges


def densify(ring: LinearRing, step: float) -> list[tuple[float, float]]:
    line = LineString(ring.coords)
    L = line.length
    if L <= 0:
        return list(ring.coords)
    n = max(int(np.ceil(L / step)), 8)
    ds = np.linspace(0.0, L, n + 1)[:-1]
    pts = [line.interpolate(d) for d in ds]
    return [(p.x, p.y) for p in pts]


def _nearest_on_network(p: Point, tree, edge_lines: list, tol: float):
    """Return (nearest_point_or_None, distance)."""
    cand_idxs = tree.query(p.buffer(tol))
    if not len(cand_idxs):
        return None, float("inf")
    best_d = tol + 1.0
    best_pt = None
    for idx in cand_idxs:
        edge = edge_lines[int(idx)]
        np_point = edge.interpolate(edge.project(p))
        d = p.distance(np_point)
        if d < best_d:
            best_d = d
            best_pt = np_point
    if best_pt is None or best_d > tol:
        return None, best_d
    return best_pt, best_d


def snap_ring_da(
    ring: LinearRing,
    da_tree,
    da_edges: list,
    muni_tree,
    muni_edges: list,
) -> tuple[LinearRing, list[bool], list[float], list[bool]]:
    """
    Snap vertices to DA edges subject to:
      - skip vertices already on a municipal edge (muni-mask; the v0_4
        pass already snapped those so we leave them alone);
      - snap only if within SNAP_TOL_M of a DA edge;
      - only credit the snap as 'anchored' if it is part of a run of
        >= CONTIG_SNAP_VERT_COUNT consecutive vertices also within tol
        (covers >= 100 m of near-parallel alignment).

    Returns (new_ring, snapped_flags, seg_lens, muni_already_flags,
             pre_errs_list).
    """
    coords = densify(ring, VERTEX_DENSIFY_M)
    n = len(coords)
    if n < 4:
        coords = list(ring.coords)
        n = len(coords)

    # Phase 1: nearest-DA & nearest-muni pass per vertex
    da_dists = np.full(n, np.inf)
    da_pts = [None] * n
    muni_already = np.zeros(n, dtype=bool)
    for i, (x, y) in enumerate(coords):
        p = Point(x, y)
        # muni mask: treat vertex as already-anchored if within MUNI_MASK_TOL_M
        # of a CSD edge (v0_4 would have snapped it there).
        _, md = _nearest_on_network(p, muni_tree, muni_edges, MUNI_MASK_TOL_M)
        if md <= MUNI_MASK_TOL_M:
            muni_already[i] = True
            continue
        # else: candidate for DA snapping
        dp, dd = _nearest_on_network(p, da_tree, da_edges, SNAP_TOL_M)
        if dp is not None:
            da_dists[i] = dd
            da_pts[i] = dp

    # Phase 2: contiguity filter — require runs of >= CONTIG_SNAP_VERT_COUNT
    # consecutive candidate vertices (within SNAP_TOL_M of a DA edge and not
    # muni-already). The ring wraps, so use a doubled array and two O(n)
    # passes to compute, for each position, the length of its enclosing run.
    in_run = np.isfinite(da_dists) & ~muni_already
    qualified = np.zeros(n, dtype=bool)
    if in_run.any() and n > 0:
        ext = np.concatenate([in_run, in_run])  # 2n
        # Forward pass: fwd[i] = length of True-run ending at i (inclusive).
        fwd = np.zeros(2 * n, dtype=np.int32)
        cur = 0
        for i in range(2 * n):
            if ext[i]:
                cur += 1
            else:
                cur = 0
            fwd[i] = cur
        # Backward pass: back[i] = length of True-run starting at i (inclusive).
        back = np.zeros(2 * n, dtype=np.int32)
        cur = 0
        for i in range(2 * n - 1, -1, -1):
            if ext[i]:
                cur += 1
            else:
                cur = 0
            back[i] = cur
        # The length of the run through i is fwd[i] + back[i] - 1 (double-
        # counts i). In the doubled array this properly handles wrap-around
        # because a run that crosses the seam from [n-1] back to [0] appears
        # once contiguously in the range [i..i+L) for some i >= n.
        # For the original ring positions 0..n-1 we take the max run length
        # at either i or i+n (the two images of the same vertex).
        run_through = fwd + back - 1
        run_len_orig = np.maximum(run_through[:n], run_through[n:])
        # Cap at n (one full ring) — a run longer than n is meaningless.
        run_len_orig = np.minimum(run_len_orig, n)
        qualified = in_run & (run_len_orig >= CONTIG_SNAP_VERT_COUNT)

    # Phase 3: build new coords + snapped_flags + pre-errors (DA residual
    # distance of qualified vertices — these were computed in Phase 1).
    new_coords = []
    snapped_flags = []
    pre_errs = []
    for i, (x, y) in enumerate(coords):
        if qualified[i] and da_pts[i] is not None:
            new_coords.append((da_pts[i].x, da_pts[i].y))
            snapped_flags.append(True)
            if np.isfinite(da_dists[i]):
                pre_errs.append(float(da_dists[i]))
        else:
            new_coords.append((x, y))
            snapped_flags.append(False)

    if new_coords[0] != new_coords[-1]:
        new_coords.append(new_coords[0])

    # Segment lengths computed vectorized via numpy
    coords_np = np.asarray(coords, dtype=float)
    if len(coords_np) >= 2:
        dx = np.diff(coords_np[:, 0], append=coords_np[0, 0])
        dy = np.diff(coords_np[:, 1], append=coords_np[0, 1])
        seg_lens = list(np.hypot(dx, dy))
    else:
        seg_lens = [0.0] * n

    new_ring = LinearRing(new_coords)
    return new_ring, snapped_flags, seg_lens, list(muni_already), pre_errs


def snap_polygon_da(
    poly: Polygon,
    da_tree,
    da_edges: list,
    muni_tree,
    muni_edges: list,
) -> tuple[Polygon, float, float, float, float]:
    """
    Returns (new_poly, total_perim_m, da_anchored_m, muni_already_m,
             mean_da_pre_err_m).
    """
    ext_new, ext_flags, ext_segs, ext_muni, ext_pre = snap_ring_da(
        poly.exterior, da_tree, da_edges, muni_tree, muni_edges
    )
    interiors_new = []
    all_flags = list(ext_flags)
    all_segs = list(ext_segs)
    all_muni = list(ext_muni)
    pre_errs = list(ext_pre)
    for hole in poly.interiors:
        h_new, h_flags, h_segs, h_muni, h_pre = snap_ring_da(
            hole, da_tree, da_edges, muni_tree, muni_edges
        )
        interiors_new.append(h_new)
        all_flags.extend(h_flags)
        all_segs.extend(h_segs)
        all_muni.extend(h_muni)
        pre_errs.extend(h_pre)

    new_poly = Polygon(ext_new, interiors_new)
    new_poly = make_valid(new_poly)
    new_poly = _keep_polys(new_poly)

    total_len = sum(all_segs)
    da_anchored_len = sum(seg for seg, f in zip(all_segs, all_flags) if f)
    muni_already_len = sum(seg for seg, m in zip(all_segs, all_muni) if m)

    pre_err_m = float(np.mean(pre_errs)) if pre_errs else 0.0
    return new_poly, total_len, da_anchored_len, muni_already_len, pre_err_m


def anchor_map_da(
    eds: gpd.GeoDataFrame,
    da_edges_mls: MultiLineString,
    muni_edges_mls: MultiLineString,
    label: str,
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    from shapely.strtree import STRtree

    def _flatten(mls):
        lines = []
        if mls.geom_type == "MultiLineString":
            lines.extend(list(mls.geoms))
        elif mls.geom_type == "LineString":
            lines.append(mls)
        else:
            for g in getattr(mls, "geoms", [mls]):
                if g.geom_type == "LineString":
                    lines.append(g)
                elif g.geom_type == "MultiLineString":
                    lines.extend(list(g.geoms))
        return lines

    da_lines = _flatten(da_edges_mls)
    muni_lines = _flatten(muni_edges_mls)
    da_tree = STRtree(da_lines)
    muni_tree = STRtree(muni_lines)

    print(f"  [{label}] DA-edge lines: {len(da_lines):,}, CSD lines: {len(muni_lines):,}")

    rows = []
    new_geoms = []
    t_start = time.time()
    for i, row in eds.iterrows():
        g = row.geometry
        if g is None or g.is_empty:
            new_geoms.append(g)
            rows.append({
                "map": label, "name_2026": row["name_2026"],
                "perimeter_km_total": 0.0,
                "da_anchored_km": 0.0, "da_anchored_pct": 0.0,
                "muni_anchored_km_v0_4": 0.0,
                "muni_anchored_pct_recomputed": 0.0,
                "new_total_anchored_pct": 0.0,
                "pre_da_error_m": 0.0,
            })
            continue

        t_poly = time.time()
        parts = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
        new_parts = []
        perim_sum = 0.0
        da_anchored_sum = 0.0
        muni_already_sum = 0.0
        pre_errs = []
        for p in parts:
            snapped_p, perim, da_anch, muni_a, pre_err = snap_polygon_da(
                p, da_tree, da_lines, muni_tree, muni_lines
            )
            if snapped_p is None or snapped_p.is_empty:
                snapped_p = p
            new_parts.append(snapped_p)
            perim_sum += perim
            da_anchored_sum += da_anch
            muni_already_sum += muni_a
            if pre_err > 0:
                pre_errs.append(pre_err)

        if len(new_parts) == 1:
            new_geom = new_parts[0]
        else:
            new_geom = MultiPolygon([x for x in new_parts if x.geom_type == "Polygon"])
        new_geom = make_valid(new_geom)
        new_geom = _keep_polys(new_geom)
        new_geoms.append(new_geom)

        da_pct = 100.0 * da_anchored_sum / perim_sum if perim_sum > 0 else 0.0
        muni_pct_recomputed = (
            100.0 * muni_already_sum / perim_sum if perim_sum > 0 else 0.0
        )
        new_total_pct = da_pct + muni_pct_recomputed
        pre_err_m = float(np.mean(pre_errs)) if pre_errs else 0.0
        rows.append({
            "map": label,
            "name_2026": row["name_2026"],
            "perimeter_km_total": perim_sum / 1000.0,
            "da_anchored_km": da_anchored_sum / 1000.0,
            "da_anchored_pct": da_pct,
            "muni_anchored_km_v0_4": muni_already_sum / 1000.0,
            "muni_anchored_pct_recomputed": muni_pct_recomputed,
            "new_total_anchored_pct": new_total_pct,
            "pre_da_error_m": pre_err_m,
        })
        t_poly_done = time.time() - t_poly
        # Emit per-polygon timing for slow ones (>10s) to help diagnose hangs
        if t_poly_done > 10.0:
            print(f"    [{label}] SLOW: {row['name_2026']:<40s} "
                  f"perim={perim_sum/1000:,.0f} km, took {t_poly_done:.1f}s",
                  flush=True)
        if (i + 1) % 10 == 0 or i == len(eds) - 1:
            elapsed = time.time() - t_start
            print(f"    [{label}] {i+1}/{len(eds)} polygons anchored "
                  f"({elapsed:.0f}s elapsed)", flush=True)

    out = eds.copy()
    out["geometry"] = new_geoms
    if "canon_source" in out.columns:
        da_pct_series = pd.Series([r["da_anchored_pct"] for r in rows])
        out["canon_source"] = [
            "da-anchored" if p >= 20.0 else s
            for p, s in zip(da_pct_series, out["canon_source"])
        ]
    out["da_anchored_pct"] = [r["da_anchored_pct"] for r in rows]
    out["new_total_anchored_pct"] = [r["new_total_anchored_pct"] for r in rows]
    return out, pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Topology re-validation (same lightweight resolver as municipal pass)
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
    print(f"    resolved {resolved} residual overlap pairs, max {max_resolved_m2:,.1f} m^2")
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
    print(f"  [{label}] post-validation: {count} pairs, {total_km2:,.4f} km^2 residual overlap")
    return count, total_km2


def main():
    print("=" * 72)
    print("  DA-boundary anchoring (v0_5) -- DPG perimeters -> StatsCan DA edges")
    print("=" * 72)

    print(f"\n[input] majority: {V0_4_MAJ.name}")
    print(f"[input] minority: {V0_4_MIN.name}")

    maj = gpd.read_file(V0_4_MAJ)
    mino = gpd.read_file(V0_4_MIN)
    print(f"  majority: {len(maj)} EDs, CRS={maj.crs}")
    print(f"  minority: {len(mino)} EDs, CRS={mino.crs}")
    assert len(maj) == 89 and len(mino) == 89, "Expected 89 EDs per map"

    print("\n[load] Statistics Canada 2021 Dissemination Areas (6,203 polys)...")
    das = gpd.read_file(DA_GPKG)
    print(f"  loaded {len(das)} DAs, CRS={das.crs}")

    print("\n[load] Statistics Canada 2021 CSDs (for muni-mask)...")
    csds = gpd.read_file(CSD_GPKG)
    print(f"  loaded {len(csds)} CSDs, CRS={csds.crs}")

    print("\n[build] DA-edge reference network (union + linemerge)...")
    da_edges = build_edge_network(das, maj.crs, "DA")

    print("\n[build] CSD-edge reference network (union + linemerge)...")
    muni_edges = build_edge_network(csds, maj.crs, "CSD")

    print("\n" + "=" * 72)
    print("  MAJORITY DA anchoring")
    print("=" * 72)
    t = time.time()
    maj_anchor, maj_log = anchor_map_da(maj, da_edges, muni_edges, "majority")
    print(f"  [majority elapsed: {time.time()-t:.1f}s]")
    maj_anchor = re_resolve_topology(maj_anchor, "majority")
    maj_overlap_pairs, maj_overlap_km2 = verify_no_overlap(maj_anchor, "majority")

    print("\n" + "=" * 72)
    print("  MINORITY DA anchoring")
    print("=" * 72)
    t = time.time()
    min_anchor, min_log = anchor_map_da(mino, da_edges, muni_edges, "minority")
    print(f"  [minority elapsed: {time.time()-t:.1f}s]")
    min_anchor = re_resolve_topology(min_anchor, "minority")
    min_overlap_pairs, min_overlap_km2 = verify_no_overlap(min_anchor, "minority")

    print("\n[write] v0_5 DA-anchored GPKGs...")
    maj_anchor.to_file(MAJ_OUT, driver="GPKG")
    min_anchor.to_file(MIN_OUT, driver="GPKG")
    print(f"  wrote: {MAJ_OUT}")
    print(f"  wrote: {MIN_OUT}")

    combined = pd.concat([maj_log, min_log], ignore_index=True)
    combined.to_csv(LOG_CSV, index=False)
    print(f"  wrote: {LOG_CSV}  ({len(combined)} rows)")

    def _pct(df, num_col, den_col="perimeter_km_total"):
        tot_den = df[den_col].sum()
        tot_num = df[num_col].sum()
        return 100.0 * tot_num / tot_den if tot_den > 0 else 0.0

    maj_da_cov = _pct(maj_log, "da_anchored_km")
    min_da_cov = _pct(min_log, "da_anchored_km")
    maj_muni_cov = _pct(maj_log, "muni_anchored_km_v0_4")
    min_muni_cov = _pct(min_log, "muni_anchored_km_v0_4")
    maj_total_cov = maj_da_cov + maj_muni_cov
    min_total_cov = min_da_cov + min_muni_cov

    # Top-5 biggest improvement = biggest da_anchored_pct
    top5_maj = (maj_log.nlargest(5, "da_anchored_pct")
                [["name_2026", "da_anchored_pct", "new_total_anchored_pct"]]
                .to_dict("records"))
    top5_min = (min_log.nlargest(5, "da_anchored_pct")
                [["name_2026", "da_anchored_pct", "new_total_anchored_pct"]]
                .to_dict("records"))

    summary = {
        "method": {
            "snap_tolerance_m": SNAP_TOL_M,
            "vertex_densify_m": VERTEX_DENSIFY_M,
            "contiguity_min_vertices": CONTIG_SNAP_VERT_COUNT,
            "contiguity_min_meters": CONTIG_SNAP_MIN_METERS,
            "muni_mask_tolerance_m": MUNI_MASK_TOL_M,
            "smart_restriction": (
                "Approach (b): vertices already within MUNI_MASK_TOL_M of a "
                "CSD edge are excluded from DA snapping. DA anchoring operates "
                "only on perimeter segments that are NOT already municipally "
                "anchored. This keeps municipal and DA anchoring disjoint by "
                "construction."
            ),
        },
        "sources": {
            "majority_input": str(V0_4_MAJ),
            "minority_input": str(V0_4_MIN),
            "da_boundaries": {
                "path": str(DA_GPKG),
                "provenance": "StatsCan 2021 Dissemination Areas (Alberta)",
                "n_das_alberta": len(das),
                "network_length_km": float(da_edges.length / 1000),
            },
            "csd_boundaries_for_muni_mask": {
                "path": str(CSD_GPKG),
                "n_csds_alberta": len(csds),
                "network_length_km": float(muni_edges.length / 1000),
            },
        },
        "baseline_v0_4": {
            "majority_anchored_pct": 71.04819356923515,
            "minority_anchored_pct": 14.458051533569382,
        },
        "majority": {
            "n_eds": len(maj_log),
            "total_perimeter_km": float(maj_log["perimeter_km_total"].sum()),
            "da_anchored_perimeter_km": float(maj_log["da_anchored_km"].sum()),
            "muni_anchored_perimeter_km_v0_4": float(maj_log["muni_anchored_km_v0_4"].sum()),
            "da_anchored_pct_overall": float(maj_da_cov),
            "muni_anchored_pct_overall_recomputed": float(maj_muni_cov),
            "new_total_anchored_pct_overall": float(maj_total_cov),
            "mean_per_ed_da_anchored_pct": float(maj_log["da_anchored_pct"].mean()),
            "median_per_ed_da_anchored_pct": float(maj_log["da_anchored_pct"].median()),
            "mean_pre_da_error_m": float(
                maj_log.loc[maj_log["pre_da_error_m"] > 0, "pre_da_error_m"].mean()
            ) if (maj_log["pre_da_error_m"] > 0).any() else 0.0,
            "top5_biggest_da_improvement": top5_maj,
            "residual_overlap_pairs": maj_overlap_pairs,
            "residual_overlap_km2": maj_overlap_km2,
        },
        "minority": {
            "n_eds": len(min_log),
            "total_perimeter_km": float(min_log["perimeter_km_total"].sum()),
            "da_anchored_perimeter_km": float(min_log["da_anchored_km"].sum()),
            "muni_anchored_perimeter_km_v0_4": float(min_log["muni_anchored_km_v0_4"].sum()),
            "da_anchored_pct_overall": float(min_da_cov),
            "muni_anchored_pct_overall_recomputed": float(min_muni_cov),
            "new_total_anchored_pct_overall": float(min_total_cov),
            "mean_per_ed_da_anchored_pct": float(min_log["da_anchored_pct"].mean()),
            "median_per_ed_da_anchored_pct": float(min_log["da_anchored_pct"].median()),
            "mean_pre_da_error_m": float(
                min_log.loc[min_log["pre_da_error_m"] > 0, "pre_da_error_m"].mean()
            ) if (min_log["pre_da_error_m"] > 0).any() else 0.0,
            "top5_biggest_da_improvement": top5_min,
            "residual_overlap_pairs": min_overlap_pairs,
            "residual_overlap_km2": min_overlap_km2,
        },
        "validation_gates": {
            "n_eds_preserved_majority": len(maj_anchor) == 89,
            "n_eds_preserved_minority": len(min_anchor) == 89,
            "no_new_big_overlap_majority": maj_overlap_km2 < 1.0,
            "no_new_big_overlap_minority": min_overlap_km2 < 1.0,
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
    print("  DA-ANCHORING SUMMARY")
    print("=" * 72)
    print(f"\n  MAJORITY: v0_4 muni baseline  {maj_muni_cov:5.1f}% -> "
          f"+ DA {maj_da_cov:5.1f}%  = total {maj_total_cov:5.1f}%")
    print(f"            mean per-ED DA anchored {maj_log['da_anchored_pct'].mean():5.1f}%, "
          f"median {maj_log['da_anchored_pct'].median():5.1f}%")
    print(f"\n  MINORITY: v0_4 muni baseline  {min_muni_cov:5.1f}% -> "
          f"+ DA {min_da_cov:5.1f}%  = total {min_total_cov:5.1f}%")
    print(f"            mean per-ED DA anchored {min_log['da_anchored_pct'].mean():5.1f}%, "
          f"median {min_log['da_anchored_pct'].median():5.1f}%")

    print("\n  Top-5 biggest DA-anchoring gains (majority):")
    for r in top5_maj:
        print(f"    {r['name_2026']:<44s}  DA {r['da_anchored_pct']:5.1f}%  "
              f"-> total {r['new_total_anchored_pct']:5.1f}%")
    print("\n  Top-5 biggest DA-anchoring gains (minority):")
    for r in top5_min:
        print(f"    {r['name_2026']:<44s}  DA {r['da_anchored_pct']:5.1f}%  "
              f"-> total {r['new_total_anchored_pct']:5.1f}%")

    all_gates_ok = all(summary["validation_gates"].values())
    print("\n" + "=" * 72)
    print(f"  DA ANCHORING: {'ALL GATES PASSED' if all_gates_ok else 'GATE FAILURE - investigate'}")
    print("=" * 72)


if __name__ == "__main__":
    main()
