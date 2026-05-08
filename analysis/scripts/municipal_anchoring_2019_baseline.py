# Version: v0.9
from __future__ import annotations
"""
2019 baseline municipal-boundary anchoring (Lane 2 historical comparator)
==========================================================================
Companion to `analysis/scripts/municipal_anchoring.py`. Runs the *identical*
snap-to-CSD-edge methodology against the 2019 enacted Alberta electoral-
division shapefile, producing a province-wide anchoring percentage that the
2026 majority (71.0 %) and minority (14.5 %) numbers can be compared to.

**Why a separate script.** `municipal_anchoring.py` hardcodes 2026 v0_3/v0_2
DPG inputs and a `name_2026` column. The 2019 shapefile uses `EDName2017`
and a different vintage entirely, so we copy the helpers and parametrize the
inputs/columns rather than retrofit the 2026 script.

**Methodology parity.**
  * Same snap tolerance (500 m), vertex densify (50 m), min anchored
    segment (1 km).
  * Same StatsCan 2021 CSD reference layer (the 2026 audit's headline
    71.0 % / 14.5 % numbers used the 2021 CSDs as the AMA-equivalent
    gazette; using the same reference for 2019 isolates the *map's* anchoring
    from any drift in the municipal layer between vintages).
  * `USE_DA_SUPPLEMENT = False`: the report's headline 2026 numbers
    (71.0 % / 14.5 %) come from a no-DA-supplement run; the DA-supplemented
    re-run produced 83.4 % / 36.8 % (see v0_1_municipal_anchoring_summary.json).
    We match the headline methodology so the 2019 number drops directly
    into the comparison table.
  * No topology re-resolve pass (the 2019 shapefile is the legally enacted
    map; vertex snapping inside the 500 m tolerance does not produce
    overlap pairs that need adjudication, and we are computing a metric
    not producing a v0_4 GPKG).

**Outputs.**
  * data/2019_municipal_anchoring.csv          (per-ED, 87 rows)
  * data/2019_municipal_anchoring_summary.json (matches 2026 schema)

Forward:
  analysis/reports/municipal_anchoring_analysis.md  (verdict section)
Backward:
  analysis/scripts/municipal_anchoring.py
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
  data/shapefiles/reference/alberta_2021_csds.gpkg
"""

# Version: 0.9 (2026-04-26)



import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


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
DATA = data_loader._resolve_path("data")

EDS_2019_SHP = (
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)
CSD_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
DA_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_das.gpkg"

OUT_CSV = DATA / "2019_municipal_anchoring.csv"
OUT_SUMMARY = DATA / "2019_municipal_anchoring_summary.json"

# Methodology — held identical to the 2026 headline run
SNAP_TOL_M = 500.0
DA_SNAP_TOL_M = 150.0
MIN_SEGMENT_COVERAGE_M = 1000.0
VERTEX_DENSIFY_M = 50.0
USE_DA_SUPPLEMENT = False  # match the 2026 headline (71.0 % / 14.5 %)


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


def load_municipal_edges(target_crs) -> MultiLineString:
    csd = gpd.read_file(CSD_GPKG).to_crs(target_crs)
    csd_edges = unary_union(
        [g.boundary for g in csd.geometry if g is not None and not g.is_empty]
    )
    print(f"  [edges] CSD boundaries loaded: {len(csd):,} polygons")
    all_geoms = [csd_edges]

    if USE_DA_SUPPLEMENT and DA_GPKG.exists():
        da = gpd.read_file(DA_GPKG).to_crs(target_crs)
        da_edges = unary_union(
            [g.boundary for g in da.geometry if g is not None and not g.is_empty]
        )
        print(f"  [edges] DA boundaries loaded: {len(da):,} polygons (supplement)")
        all_geoms.append(da_edges)

    edges = _normalise_edges(unary_union(all_geoms))
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


def snap_ring(ring, edges, edges_tree, edge_lines, snap_tol):
    coords = densify(ring, VERTEX_DENSIFY_M)
    if len(coords) < 4:
        coords = list(ring.coords)
    new_coords = []
    snapped_flags = []
    for x, y in coords:
        p = Point(x, y)
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

    if new_coords[0] != new_coords[-1]:
        new_coords.append(new_coords[0])
        snapped_flags.append(snapped_flags[0])

    seg_lens = []
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        seg_lens.append(float(np.hypot(x2 - x1, y2 - y1)))

    new_ring = LinearRing(new_coords)
    return new_ring, snapped_flags[: len(coords)], seg_lens


def snap_polygon(poly, edges, edges_tree, edge_lines, snap_tol):
    exterior_new, ext_flags, ext_segs = snap_ring(
        poly.exterior, edges, edges_tree, edge_lines, snap_tol
    )
    interiors_new = []
    all_flags = list(ext_flags)
    all_segs = list(ext_segs)
    pre_errs = []
    coords_dense = densify(poly.exterior, VERTEX_DENSIFY_M)
    for (x, y), snapped in zip(coords_dense, ext_flags):
        if snapped:
            p = Point(x, y)
            cand_idxs = edges_tree.query(p.buffer(snap_tol))
            if len(cand_idxs):
                best = min(edge_lines[int(i)].distance(p) for i in cand_idxs)
                pre_errs.append(best)
    for hole in poly.interiors:
        h_new, h_flags, h_segs = snap_ring(
            hole, edges, edges_tree, edge_lines, snap_tol
        )
        interiors_new.append(h_new)
        all_flags.extend(h_flags)
        all_segs.extend(h_segs)
        h_dense = densify(hole, VERTEX_DENSIFY_M)
        for (x, y), snapped in zip(h_dense, h_flags):
            if snapped:
                p = Point(x, y)
                cand_idxs = edges_tree.query(p.buffer(snap_tol))
                if len(cand_idxs):
                    best = min(edge_lines[int(i)].distance(p) for i in cand_idxs)
                    pre_errs.append(best)

    new_poly = Polygon(exterior_new, interiors_new)
    new_poly = make_valid(new_poly)
    new_poly = _keep_polys(new_poly)

    total_len = sum(all_segs)
    anchored_len = 0.0
    for i, seg in enumerate(all_segs):
        if all_flags[i]:
            anchored_len += seg

    pre_err_m = float(np.mean(pre_errs)) if pre_errs else 0.0
    return new_poly, total_len, anchored_len, pre_err_m, 0.0


def anchor_map(eds, edges, name_col, label):
    from shapely.strtree import STRtree

    edge_lines = []
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
    print(f"  [{label}] municipal-edge network: {len(edge_lines):,} LineStrings")

    rows = []
    for i, row in eds.iterrows():
        g = row.geometry
        ed_name = row[name_col]
        if g is None or g.is_empty:
            rows.append(
                {
                    "map": label,
                    "name_2019": ed_name,
                    "perimeter_km_total": 0.0,
                    "perimeter_km_anchored": 0.0,
                    "anchored_pct": 0.0,
                    "pre_ama_error_m": 0.0,
                    "post_ama_error_m": 0.0,
                }
            )
            continue

        if g.geom_type == "MultiPolygon":
            parts = list(g.geoms)
        elif g.geom_type == "GeometryCollection":
            parts = [s for s in g.geoms if s.geom_type == "Polygon"] + [
                sp for s in g.geoms if s.geom_type == "MultiPolygon" for sp in s.geoms
            ]
        else:
            parts = [g]

        perim_sum = 0.0
        anchored_sum = 0.0
        pre_errs = []
        for p in parts:
            _, perim, anchored, pre_err, _ = snap_polygon(
                p, edges, tree, edge_lines, SNAP_TOL_M
            )
            perim_sum += perim
            anchored_sum += anchored
            if pre_err > 0:
                pre_errs.append(pre_err)

        anchored_pct = 100.0 * anchored_sum / perim_sum if perim_sum > 0 else 0.0
        rows.append(
            {
                "map": label,
                "name_2019": ed_name,
                "perimeter_km_total": perim_sum / 1000.0,
                "perimeter_km_anchored": anchored_sum / 1000.0,
                "anchored_pct": anchored_pct,
                "pre_ama_error_m": float(np.mean(pre_errs)) if pre_errs else 0.0,
                "post_ama_error_m": 0.0,
            }
        )
        if (i + 1) % 10 == 0:
            print(f"    [{label}] {i+1}/{len(eds)} polygons anchored")

    return pd.DataFrame(rows)


def main():
    print("=" * 72)
    print("  2019 BASELINE municipal-boundary anchoring (Lane 2 historical)")
    print("=" * 72)
    print(f"  USE_DA_SUPPLEMENT = {USE_DA_SUPPLEMENT}  (matches 2026 headline run)")
    print(f"  SNAP_TOL_M = {SNAP_TOL_M}")
    print()

    eds = gpd.read_file(EDS_2019_SHP)
    print(f"[input] 2019 enacted shapefile: {EDS_2019_SHP.name}")
    print(f"  {len(eds)} EDs, CRS={eds.crs}")
    name_col = "EDName2017"
    assert name_col in eds.columns, f"Expected name column {name_col}"

    print("\n[load] municipal-boundary network (StatsCan 2021 CSDs — AMA-equivalent)")
    t0 = time.time()
    edges = load_municipal_edges(eds.crs)
    print(
        f"  edges built in {time.time()-t0:.1f}s; total length = "
        f"{edges.length/1000:,.0f} km"
    )

    print("\n" + "=" * 72)
    print("  2019 anchoring")
    print("=" * 72)
    t = time.time()
    log = anchor_map(eds, edges, name_col, "2019")
    print(f"  [2019 elapsed: {time.time()-t:.1f}s]")

    log.to_csv(OUT_CSV, index=False)
    print(f"\n  wrote: {OUT_CSV}  ({len(log)} rows)")

    tot_perim = float(log["perimeter_km_total"].sum())
    tot_anchored = float(log["perimeter_km_anchored"].sum())
    overall_pct = 100.0 * tot_anchored / tot_perim if tot_perim > 0 else 0.0

    top10 = log.nlargest(10, "anchored_pct")[
        ["name_2019", "anchored_pct", "perimeter_km_total"]
    ].to_dict("records")
    bot10 = log.nsmallest(10, "anchored_pct")[
        ["name_2019", "anchored_pct", "perimeter_km_total"]
    ].to_dict("records")
    top5 = log.nlargest(5, "anchored_pct")[["name_2019", "anchored_pct"]].to_dict(
        "records"
    )
    bot5 = log.nsmallest(5, "anchored_pct")[["name_2019", "anchored_pct"]].to_dict(
        "records"
    )

    summary = {
        "method": {
            "snap_tolerance_m": SNAP_TOL_M,
            "da_snap_tol_m_reference": DA_SNAP_TOL_M,
            "vertex_densify_m": VERTEX_DENSIFY_M,
            "min_segment_coverage_m": MIN_SEGMENT_COVERAGE_M,
            "da_supplemented": USE_DA_SUPPLEMENT and DA_GPKG.exists(),
            "parity_note": (
                "Methodology held identical to the 2026 headline run that "
                "produced the 71.0 % majority / 14.5 % minority numbers in "
                "municipal_anchoring_analysis.md. USE_DA_SUPPLEMENT=False."
            ),
        },
        "sources": {
            "input": {
                "path": str(EDS_2019_SHP),
                "vintage": "2019_enacted_bill33_15dec2017",
                "n_eds": len(eds),
                "name_column": name_col,
            },
            "municipal_boundaries": {
                "path": str(CSD_GPKG),
                "provenance": "StatsCan 2021 Census Sub-Division (AMA-equivalent)",
                "downloaded_from": (
                    "https://www12.statcan.gc.ca/census-recensement/"
                    "2021/geo/sip-pis/boundary-limites/files-fichiers/"
                    "lcsd000a21a_e.zip"
                ),
                "n_csds_alberta": 423,
            },
        },
        "2019": {
            "n_eds": len(log),
            "total_perimeter_km": tot_perim,
            "anchored_perimeter_km": tot_anchored,
            "anchored_pct_overall": overall_pct,
            "mean_per_ed_anchored_pct": float(log["anchored_pct"].mean()),
            "median_per_ed_anchored_pct": float(log["anchored_pct"].median()),
            "mean_pre_ama_error_m": float(log["pre_ama_error_m"].mean()),
            "top5_most_anchored": top5,
            "bottom5_least_anchored": bot5,
            "top10_most_anchored": top10,
            "bottom10_least_anchored": bot10,
        },
        "comparison_to_2026": {
            "_2019_overall_pct": overall_pct,
            "_2026_majority_overall_pct_headline": 71.0,
            "_2026_minority_overall_pct_headline": 14.5,
            "_2026_headline_source": "analysis/reports/municipal_anchoring_analysis.md",
        },
        "outputs": {
            "log_csv": str(OUT_CSV),
            "summary_json": str(OUT_SUMMARY),
        },
    }
    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"  wrote: {OUT_SUMMARY}")

    print("\n" + "=" * 72)
    print("  2019 BASELINE SUMMARY")
    print("=" * 72)
    print(f"\n  2019 enacted: {overall_pct:5.1f}% of total perimeter anchored")
    print(
        f"                mean per-ED anchored {log['anchored_pct'].mean():5.1f}%, "
        f"median {log['anchored_pct'].median():5.1f}%"
    )
    print(
        f"                total perimeter {tot_perim:,.0f} km, "
        f"anchored {tot_anchored:,.0f} km"
    )
    print()
    print(f"  Comparison to 2026 headline numbers:")
    print(f"    2019 enacted     : {overall_pct:5.1f}%")
    print(
        f"    2026 majority    :  71.0 %  (delta vs 2019: {71.0 - overall_pct:+5.1f} pp)"
    )
    print(
        f"    2026 minority    :  14.5 %  (delta vs 2019: {14.5 - overall_pct:+5.1f} pp)"
    )

    print("\n  Top-10 most-anchored 2019 EDs:")
    for r in top10:
        print(f"    {r['name_2019']:<44s}  {r['anchored_pct']:5.1f}%")
    print("\n  Bottom-10 least-anchored 2019 EDs:")
    for r in bot10:
        print(f"    {r['name_2019']:<44s}  {r['anchored_pct']:5.1f}%")

    print("\n" + "=" * 72)
    print("  2019 BASELINE COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
