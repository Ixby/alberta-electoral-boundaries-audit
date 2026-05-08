"""
score_natural_anchoring.py — Lane-2 secondary check (natural anchoring %)
=========================================================================
Companion / counterfactual to `analysis/scripts/score_anchoring.py`.

The headline Lane-2 finding is that the 2026 minority map anchors only 14.5%
of its perimeter to StatsCan 2021 CSD edges, vs. 71.0% (2026 majority) and
75.2% (2019 enacted). A hostile-witness counter is "the minority map didn't
abandon anchoring; it anchored to highways, rivers, and county lines instead
of municipal CSD borders, so the 14.5% number is a measurement failure, not
a map failure." This script tests that counter directly by re-running the
identical snap-tolerance method against a *different* edge substrate built

import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

from physical and administrative features other than CSDs:

    * Highways  — OSM ways tagged highway in {motorway, trunk, primary,
                  secondary}. Matches the major-road classes already used
                  for OSM road-snapping in
                  analysis/methodology/shape_refinement.md (the audit's
                  v0_1 Track Y refinement). Tertiary is excluded because
                  intra-city street grids would inflate every map's score
                  uniformly and add no discriminatory power.
    * Rivers    — OSM ways tagged waterway=river. Excludes streams,
                  canals, ditches.
    * Counties  — Alberta Municipal Affairs publishes a county / MD layer
                  separate from StatCan CSDs. AMA distributes via AltaLIS
                  (non-anonymous registration; no stable URL — same blocker
                  documented in municipal_anchoring.py:15-24). Not included
                  in this run; documented as a residual caveat. Note that
                  Alberta's MD/county/SM jurisdictions ARE present in the
                  StatsCan 2021 CSD layer used by the headline run as types
                  MD/SM/SA, so any "county-line anchoring" the minority map
                  performs is already captured in the 14.5% number — this
                  is a meaningful caveat for the hostile-witness reading.

CLI:
    python analysis/scripts/score_natural_anchoring.py \\
        --shapefile PATH \\
        --features highways,rivers \\
        [--out-csv PATH] [--out-json PATH] [--label LABEL] [--name-col COL]

Output schema matches score_anchoring.py / municipal_anchoring.py exactly:
    Per-ED CSV columns:  map, name, perimeter_km_total, perimeter_km_anchored,
                         anchored_pct
    Provincial JSON:     method{snap_tolerance_m, vertex_densify_m, features},
                         sources{...}, totals{n_eds, total_perimeter_km,
                         anchored_perimeter_km, anchored_pct_overall,
                         mean_per_ed_anchored_pct, median_per_ed_anchored_pct},
                         top5_most_anchored, bottom5_least_anchored

Parameters held identical to the headline CSD run:
    SNAP_TOL_M        = 500.0   (matches DPG +/-500m error budget)
    VERTEX_DENSIFY_M  = 50.0

Forward:
    analysis/reports/natural_anchoring_secondary_check.md
Backward:
    analysis/scripts/_fetch_osm_natural.py  (OSM data fetch + cache)
    analysis/scripts/score_anchoring.py     (CSD comparator)
    data/osm/alberta_osm_highways.gpkg
    data/osm/alberta_osm_rivers.gpkg
"""
from __future__ import annotations

# Version: 0.9 (2026-04-26)


import argparse
import json
import sys
import time
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LinearRing, LineString, MultiLineString, Point
from shapely.ops import linemerge, unary_union
from shapely.strtree import STRtree

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
OSM_DIR = DATA / "osm"

OSM_HIGHWAYS_GPKG = OSM_DIR / "alberta_osm_highways.gpkg"
OSM_RIVERS_GPKG = OSM_DIR / "alberta_osm_rivers.gpkg"

# Held identical to the headline CSD run (score_anchoring.py)
SNAP_TOL_M: float = 500.0
VERTEX_DENSIFY_M: float = 50.0

# Highway classes pulled by _fetch_osm_natural.py
HIGHWAY_CLASSES = {"motorway", "trunk", "primary", "secondary"}


# ---------------------------------------------------------------------------
# OSM ingestion
# ---------------------------------------------------------------------------


def load_highway_lines() -> gpd.GeoDataFrame:
    if not OSM_HIGHWAYS_GPKG.exists():
        raise FileNotFoundError(
            f"Missing {OSM_HIGHWAYS_GPKG}. Run "
            f"analysis/scripts/_fetch_osm_natural.py first."
        )
    gdf = gpd.read_file(OSM_HIGHWAYS_GPKG)
    print(
        f"  [osm] {len(gdf):,} highway ways loaded "
        f"(classes={sorted(HIGHWAY_CLASSES)})"
    )
    return gdf


def load_river_lines() -> gpd.GeoDataFrame:
    if not OSM_RIVERS_GPKG.exists():
        raise FileNotFoundError(
            f"Missing {OSM_RIVERS_GPKG}. Run "
            f"analysis/scripts/_fetch_osm_natural.py first."
        )
    gdf = gpd.read_file(OSM_RIVERS_GPKG)
    print(f"  [osm] {len(gdf):,} river ways loaded (waterway=river)")
    return gdf


# ---------------------------------------------------------------------------
# Edge network construction
# ---------------------------------------------------------------------------


def _normalise_edges(edges) -> MultiLineString:
    if edges.geom_type == "MultiLineString":
        edges = linemerge(edges)
    if edges.geom_type == "LineString":
        edges = MultiLineString([edges])
    if edges.geom_type == "GeometryCollection":
        ls = [
            g for g in edges.geoms if g.geom_type in ("LineString", "MultiLineString")
        ]
        edges = unary_union(ls)
    return edges


def build_natural_edges(target_crs, features: list[str]) -> MultiLineString:
    """Union of natural-anchoring features in `features`, projected to
    target_crs and normalised to a MultiLineString."""
    pieces = []
    if "highways" in features:
        gdf = load_highway_lines().to_crs(target_crs)
        pieces.append(unary_union(list(gdf.geometry)))
    if "rivers" in features:
        gdf = load_river_lines().to_crs(target_crs)
        pieces.append(unary_union(list(gdf.geometry)))
    if "counties" in features:
        # AMA county/MD layer not available on disk — see module docstring.
        # Keep the option name in the CLI so future PRs can wire this in
        # without breaking call sites; for now emit a clear warning.
        print(
            "  [warn] counties feature requested but no AMA county/MD shapefile "
            "is on disk; skipping. See score_natural_anchoring.py docstring "
            "for sourcing notes.",
            file=sys.stderr,
        )
    if not pieces:
        raise ValueError(f"No features produced edges; got --features={features!r}")
    return _normalise_edges(unary_union(pieces))


# ---------------------------------------------------------------------------
# Snap-and-measure (identical formula to score_anchoring.py)
# ---------------------------------------------------------------------------


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

    perim = 0.0
    anchored = 0.0
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        seg = float(np.hypot(x2 - x1, y2 - y1))
        perim += seg
        if snapped_flags[i]:
            anchored += seg
    return perim, anchored


def score_map(
    eds: gpd.GeoDataFrame,
    edges: MultiLineString,
    name_col: str,
    label: str,
) -> tuple[pd.DataFrame, dict]:
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
    print(f"  [{label}] natural-edge network: {len(edge_lines):,} LineStrings")

    rows = []
    for i, row in eds.reset_index(drop=True).iterrows():
        g = row.geometry
        ed_name = row[name_col]
        if g is None or g.is_empty:
            rows.append(
                {
                    "map": label,
                    "name": ed_name,
                    "perimeter_km_total": 0.0,
                    "perimeter_km_anchored": 0.0,
                    "anchored_pct": 0.0,
                }
            )
            continue

        if g.geom_type == "MultiPolygon":
            parts = list(g.geoms)
        elif g.geom_type == "Polygon":
            parts = [g]
        else:
            parts = [s for s in getattr(g, "geoms", []) if s.geom_type == "Polygon"]

        perim_sum = 0.0
        anchored_sum = 0.0
        for poly in parts:
            p, a = _measure_ring(poly.exterior, edge_lines, tree, SNAP_TOL_M)
            perim_sum += p
            anchored_sum += a
            for hole in poly.interiors:
                p, a = _measure_ring(hole, edge_lines, tree, SNAP_TOL_M)
                perim_sum += p
                anchored_sum += a

        pct = 100.0 * anchored_sum / perim_sum if perim_sum > 0 else 0.0
        rows.append(
            {
                "map": label,
                "name": ed_name,
                "perimeter_km_total": perim_sum / 1000.0,
                "perimeter_km_anchored": anchored_sum / 1000.0,
                "anchored_pct": pct,
            }
        )
        if (i + 1) % 15 == 0:
            print(f"    [{label}] {i+1}/{len(eds)} polygons measured")

    log = pd.DataFrame(rows)
    tot_perim = float(log["perimeter_km_total"].sum())
    tot_anchored = float(log["perimeter_km_anchored"].sum())
    overall = 100.0 * tot_anchored / tot_perim if tot_perim > 0 else 0.0

    top5 = log.nlargest(5, "anchored_pct")[["name", "anchored_pct"]].to_dict("records")
    bot5 = log.nsmallest(5, "anchored_pct")[["name", "anchored_pct"]].to_dict("records")

    summary = {
        "n_eds": int(len(log)),
        "total_perimeter_km": tot_perim,
        "anchored_perimeter_km": tot_anchored,
        "anchored_pct_overall": overall,
        "mean_per_ed_anchored_pct": float(log["anchored_pct"].mean()),
        "median_per_ed_anchored_pct": float(log["anchored_pct"].median()),
        "top5_most_anchored": top5,
        "bottom5_least_anchored": bot5,
    }
    return log, summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _autodetect_name_col(eds: gpd.GeoDataFrame) -> str:
    for cand in ("name_2026", "EDName2017", "ED_NAME", "name", "ENG_NAME"):
        if cand in eds.columns:
            return cand
    raise ValueError(
        f"Could not autodetect ED name column from {list(eds.columns)}; "
        f"pass --name-col"
    )


def main():
    ap = argparse.ArgumentParser(
        description=(
            "Score province-wide natural-anchoring % of an electoral map "
            "against OSM highways and/or rivers."
        )
    )
    ap.add_argument(
        "--shapefile",
        required=True,
        type=Path,
        help=".shp or .gpkg with electoral-division polygons",
    )
    ap.add_argument(
        "--features",
        default="highways,rivers",
        help="Comma-separated subset of {highways,rivers,counties}. "
        "Default: highways,rivers (counties unavailable on disk).",
    )
    ap.add_argument(
        "--name-col", default=None, help="ED name column; autodetected if omitted."
    )
    ap.add_argument(
        "--label",
        default=None,
        help="Map label for output rows; defaults to shapefile stem.",
    )
    ap.add_argument(
        "--out-csv",
        type=Path,
        default=None,
        help="Per-ED CSV output. Defaults to data/v0_9_natural_anchoring_<label>.csv",
    )
    ap.add_argument(
        "--out-json",
        type=Path,
        default=None,
        help="Provincial summary JSON. Defaults alongside CSV.",
    )
    args = ap.parse_args()

    if not args.shapefile.exists():
        print(f"ERROR: shapefile not found: {args.shapefile}", file=sys.stderr)
        sys.exit(2)
    features = [f.strip().lower() for f in args.features.split(",") if f.strip()]
    valid = {"highways", "rivers", "counties"}
    if not features or any(f not in valid for f in features):
        print(
            f"ERROR: --features must be subset of {valid}; got {features}",
            file=sys.stderr,
        )
        sys.exit(2)

    label = args.label or args.shapefile.stem
    out_csv = args.out_csv or (DATA / f"v0_9_natural_anchoring_{label}.csv")
    out_json = args.out_json or out_csv.with_suffix(".json")

    print("=" * 72)
    print(f"  Natural-anchoring scoring: {label}")
    print(f"  features = {features}")
    print("=" * 72)

    print(f"\n[input] {args.shapefile}")
    eds = gpd.read_file(args.shapefile)
    if eds.crs is None:
        raise ValueError(f"{args.shapefile} has no CRS")
    name_col = args.name_col or _autodetect_name_col(eds)
    print(f"  {len(eds)} EDs, CRS={eds.crs}, name_col={name_col}")

    print(f"\n[edges] building natural-anchoring edge network in {eds.crs}")
    t0 = time.time()
    edges = build_natural_edges(eds.crs, features)
    print(
        f"  edges built in {time.time()-t0:.1f}s; "
        f"total length = {edges.length/1000:,.0f} km"
    )

    print(f"\n[score] {label}")
    t = time.time()
    log, summary = score_map(eds, edges, name_col, label)
    print(f"  [{label} elapsed: {time.time()-t:.1f}s]")

    log.to_csv(out_csv, index=False)
    print(f"\n  wrote: {out_csv}  ({len(log)} rows)")

    full_summary = {
        "method": {
            "snap_tolerance_m": SNAP_TOL_M,
            "vertex_densify_m": VERTEX_DENSIFY_M,
            "features": features,
            "highway_classes": (
                sorted(HIGHWAY_CLASSES) if "highways" in features else []
            ),
            "parity_note": (
                "Snap tolerance and vertex densification held identical to "
                "score_anchoring.py (the audit's headline CSD-anchoring run "
                "that produced 71.0% / 14.5% / 75.2%)."
            ),
        },
        "sources": {
            "input": {
                "path": str(args.shapefile),
                "label": label,
                "n_eds": int(len(eds)),
                "name_column": name_col,
            },
            "highways": {
                "path": str(OSM_HIGHWAYS_GPKG),
                "provenance": "OpenStreetMap via Overpass API (motorway|trunk|primary|secondary)",
                "fetcher": "analysis/scripts/_fetch_osm_natural.py",
                "used": "highways" in features,
            },
            "rivers": {
                "path": str(OSM_RIVERS_GPKG),
                "provenance": "OpenStreetMap via Overpass API (waterway=river)",
                "fetcher": "analysis/scripts/_fetch_osm_natural.py",
                "used": "rivers" in features,
            },
            "counties": {
                "path": None,
                "provenance": (
                    "Alberta Municipal Affairs county/MD layer is distributed "
                    "via AltaLIS (non-anonymous registration; no stable URL). "
                    "Not on disk; not included in this run. Note that AB MD/SM/SA "
                    "jurisdictions are already covered in the StatCan 2021 CSD "
                    "layer used by score_anchoring.py, so any 'county-line' "
                    "anchoring the minority map performs is captured by the "
                    "headline 14.5% number."
                ),
                "used": False,
            },
        },
        "totals": summary,
        "outputs": {"log_csv": str(out_csv), "summary_json": str(out_json)},
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(full_summary, indent=2, default=str))
    print(f"  wrote: {out_json}")

    print("\n" + "=" * 72)
    print(
        f"  {label}: {summary['anchored_pct_overall']:5.1f}% of total perimeter "
        f"anchored to natural features ({'+'.join(features)})"
    )
    print(
        f"           mean per-ED {summary['mean_per_ed_anchored_pct']:5.1f}%, "
        f"median {summary['median_per_ed_anchored_pct']:5.1f}%"
    )
    print("=" * 72)
    print("\n  Top-5 most-anchored:")
    for r in summary["top5_most_anchored"]:
        print(f"    {r['name']:<44s}  {r['anchored_pct']:5.1f}%")
    print("\n  Bottom-5 least-anchored:")
    for r in summary["bottom5_least_anchored"]:
        print(f"    {r['name']:<44s}  {r['anchored_pct']:5.1f}%")


if __name__ == "__main__":
    main()
