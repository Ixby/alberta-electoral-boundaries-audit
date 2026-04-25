"""Adjacency Structure Analysis (Test B1)
=========================================

Builds an ED adjacency graph for each map (2019, Majority 2026, Minority 2026)
and runs three structural tests:

  B1a — Queen-contiguity gate: is the ED graph fully connected (every ED
        reachable from every other via shared boundaries)?  A disconnected
        graph means a group of EDs is spatially isolated from the rest.

  B1b — Airdrie multi-split: how many EDs contain part of the city of
        Airdrie?  The pre-registration (2026-04-23) flags a 4-way split as
        a potential cracking signal.

  B1c — Neighbor-count distribution: per-ED count of adjacent EDs.

Outputs:
  analysis/reports/v0_1_adjacency_analysis.csv
      per-ED rows: map, name, neighbor_count, touches_airdrie,
                   airdrie_fragment_area_pct
  data/v0_1_adjacency_summary.json
      per-map: mean_neighbor_count, fully_connected, airdrie_ed_count,
               airdrie_split_exceeds_4

Author: v0.1 audit pipeline — Test B1. Generated 2026-04-24.

Forward deps:
  - analysis/reports/v0_1_adjacency_analysis.csv consumed by
    report_academic.md §B (adjacency structural findings)
  - data/v0_1_adjacency_summary.json consumed by summary dashboard

Backward deps:
  - data/shapefiles/derived/v0_3_canonical_majority_2026_eds_swept.gpkg
  - data/shapefiles/derived/v0_3_canonical_minority_2026_eds_swept.gpkg
  - data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
  - data/shapefiles/reference/alberta_2021_csds.gpkg  (Airdrie CSD boundary)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx

ROOT = Path(__file__).resolve().parent.parent.parent  # .../alberta_audit
DATA = ROOT / "data"
REPORTS = ROOT / "analysis" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Buffer used for adjacency detection (metres, projected CRS EPSG:3347 /
# EPSG:3401).  The v0.3 swept substrate may have small topological gaps
# (~10–200 m) at shared edges introduced by the clip-and-sweep process.
# 200 m bridges these while staying well below the smallest ED diameter.
ADJACENCY_BUFFER_M = 200.0

# Area overlap threshold (fraction of ED area) required for Airdrie
# intersection to count as "the ED contains part of Airdrie" rather than
# just a slipper boundary touch.
AIRDRIE_OVERLAP_MIN_FRAC = 0.001  # 0.1 % of ED area

# Airdrie split threshold flagged in pre-registration
AIRDRIE_SPLIT_FLAG_COUNT = 4


# ---------------------------------------------------------------------------
# Shapefile / layer definitions
# ---------------------------------------------------------------------------

MAPS = {
    "2019": {
        "path": DATA / "shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp",
        "name_col": "EDName2017",
        "target_crs": "EPSG:3347",
    },
    "majority_2026": {
        "path": DATA / "shapefiles/derived/v0_3_canonical_majority_2026_eds_swept.gpkg",
        "name_col": "name_2026",
        "target_crs": None,  # already EPSG:3347
    },
    "minority_2026": {
        "path": DATA / "shapefiles/derived/v0_3_canonical_minority_2026_eds_swept.gpkg",
        "name_col": "name_2026",
        "target_crs": None,
    },
}

CSD_PATH = DATA / "shapefiles/reference/alberta_2021_csds.gpkg"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_map(cfg: dict) -> gpd.GeoDataFrame:
    """Load an ED shapefile/geopackage and reproject if needed."""
    gdf = gpd.read_file(cfg["path"])
    if cfg.get("target_crs"):
        gdf = gdf.to_crs(cfg["target_crs"])
    # Ensure geometry is valid
    gdf["geometry"] = gdf.geometry.buffer(0)
    return gdf


def build_adjacency_graph(
    gdf: gpd.GeoDataFrame, name_col: str, buffer_m: float
) -> Tuple[nx.Graph, gpd.GeoDataFrame]:
    """Build an undirected adjacency graph for an ED layer.

    Two EDs are adjacent if their buffered geometries intersect AND they are
    not the same polygon.

    Returns (G, buffered_gdf).
    """
    buffered = gdf.copy()
    buffered["geometry"] = buffered.geometry.buffer(buffer_m)

    G = nx.Graph()
    names = list(gdf[name_col])
    G.add_nodes_from(names)

    # Spatial self-join: find all (i, j) pairs whose buffers intersect
    joined = gpd.sjoin(
        buffered[[name_col, "geometry"]],
        buffered[[name_col, "geometry"]],
        how="inner",
        predicate="intersects",
    )
    # Drop self-matches
    left_col = name_col + "_left"
    right_col = name_col + "_right"
    joined = joined[joined[left_col] != joined[right_col]]

    for _, row in joined.iterrows():
        G.add_edge(row[left_col], row[right_col])

    return G, buffered


def airdrie_overlap(
    gdf: gpd.GeoDataFrame,
    name_col: str,
    airdrie_geom,
    min_frac: float,
) -> pd.DataFrame:
    """Return per-ED Airdrie overlap statistics.

    Columns: ed_name, touches_airdrie, airdrie_fragment_area_pct
    """
    rows = []
    airdrie_area = airdrie_geom.area

    for _, ed in gdf.iterrows():
        inter = ed.geometry.intersection(airdrie_geom)
        inter_area = inter.area if not inter.is_empty else 0.0
        ed_area = ed.geometry.area if ed.geometry.area > 0 else 1.0

        # touches_airdrie: overlap covers at least min_frac of the ED
        overlap_frac_ed = inter_area / ed_area
        touches = bool(overlap_frac_ed >= min_frac)

        # What fraction of Airdrie's area falls in this ED
        airdrie_frac = (inter_area / airdrie_area * 100.0) if airdrie_area > 0 else 0.0

        rows.append(
            {
                "ed_name": ed[name_col],
                "touches_airdrie": touches,
                "airdrie_fragment_area_pct": round(airdrie_frac, 3),
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------


def analyse_map(
    map_label: str,
    cfg: dict,
    airdrie_poly,
) -> Tuple[pd.DataFrame, dict]:
    """Run B1a / B1b / B1c for one map.

    Returns (per_ed_df, summary_dict).
    """
    print(f"\n{'='*60}")
    print(f"Map: {map_label}")
    print(f"{'='*60}")

    gdf = load_map(cfg)
    name_col = cfg["name_col"]
    n_eds = len(gdf)
    print(f"  Loaded {n_eds} EDs")

    # --- B1a: connectivity gate ---
    G, buffered_gdf = build_adjacency_graph(gdf, name_col, ADJACENCY_BUFFER_M)
    connected_components = list(nx.connected_components(G))
    fully_connected = len(connected_components) == 1

    if fully_connected:
        print(f"  B1a — Contiguity gate: PASS (single connected component)")
    else:
        print(f"  B1a — Contiguity gate: FAIL ({len(connected_components)} components)")
        for i, comp in enumerate(connected_components, 1):
            if len(comp) < 6:
                print(f"    Component {i}: {sorted(comp)}")
            else:
                sample = sorted(comp)[:3]
                print(f"    Component {i} ({len(comp)} EDs): {sample} …")

    # --- B1c: neighbor count per ED ---
    neighbor_counts = {ed: G.degree(ed) for ed in G.nodes()}

    # --- B1b: Airdrie split ---
    # Reproject Airdrie to match ED CRS
    airdrie_reproj = airdrie_poly.to_crs(gdf.crs)
    airdrie_geom = airdrie_reproj.geometry.union_all()

    airdrie_df = airdrie_overlap(gdf, name_col, airdrie_geom, AIRDRIE_OVERLAP_MIN_FRAC)
    airdrie_eds = airdrie_df[airdrie_df["touches_airdrie"]]
    airdrie_count = len(airdrie_eds)
    airdrie_flag = airdrie_count >= AIRDRIE_SPLIT_FLAG_COUNT

    print(f"  B1b — Airdrie EDs: {airdrie_count}  "
          f"({'FLAG: meets pre-registration cracking threshold' if airdrie_flag else 'below 4-way threshold'})")
    if airdrie_count > 0:
        for _, r in airdrie_eds.sort_values("airdrie_fragment_area_pct", ascending=False).iterrows():
            print(f"    {r['ed_name']:45s}  {r['airdrie_fragment_area_pct']:6.2f}% of Airdrie")

    # --- B1c summary ---
    deg_values = [neighbor_counts[ed] for ed in G.nodes()]
    mean_nc = float(np.mean(deg_values))
    print(f"  B1c — Neighbor count: mean={mean_nc:.2f}, "
          f"min={min(deg_values)}, max={max(deg_values)}")

    # --- Build per-ED output DataFrame ---
    per_ed_rows = []
    for _, ed in gdf.iterrows():
        ed_name = ed[name_col]
        nc = neighbor_counts.get(ed_name, 0)
        airdrie_row = airdrie_df[airdrie_df["ed_name"] == ed_name]
        ta = bool(airdrie_row["touches_airdrie"].values[0]) if len(airdrie_row) else False
        ap = float(airdrie_row["airdrie_fragment_area_pct"].values[0]) if len(airdrie_row) else 0.0
        per_ed_rows.append(
            {
                "map": map_label,
                "name": ed_name,
                "neighbor_count": nc,
                "touches_airdrie": ta,
                "airdrie_fragment_area_pct": ap,
            }
        )

    per_ed_df = pd.DataFrame(per_ed_rows)

    summary = {
        "map": map_label,
        "n_eds": n_eds,
        "mean_neighbor_count": round(mean_nc, 3),
        "min_neighbor_count": int(min(deg_values)),
        "max_neighbor_count": int(max(deg_values)),
        "n_components": len(connected_components),
        "fully_connected": fully_connected,
        "airdrie_ed_count": airdrie_count,
        "airdrie_split_exceeds_4": airdrie_flag,
        "airdrie_eds": sorted(airdrie_eds["ed_name"].tolist()),
    }

    return per_ed_df, summary


def main() -> None:
    # Load Airdrie CSD polygon
    csd = gpd.read_file(CSD_PATH)
    airdrie_csd = csd[csd["CSDNAME"] == "Airdrie"].copy()
    if len(airdrie_csd) == 0:
        print("ERROR: Airdrie not found in CSD layer.", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded Airdrie CSD boundary (CRS: {airdrie_csd.crs})")

    all_rows: List[pd.DataFrame] = []
    all_summaries = []

    for map_label, cfg in MAPS.items():
        per_ed_df, summary = analyse_map(map_label, cfg, airdrie_csd)
        all_rows.append(per_ed_df)
        all_summaries.append(summary)

    # --- Write outputs ---
    out_csv = REPORTS / "v0_1_adjacency_analysis.csv"
    combined = pd.concat(all_rows, ignore_index=True)
    combined.to_csv(out_csv, index=False)
    print(f"\nWrote {len(combined)} rows to {out_csv}")

    out_json = DATA / "v0_1_adjacency_summary.json"
    with open(out_json, "w") as fh:
        json.dump(all_summaries, fh, indent=2, default=str)
    print(f"Wrote summary to {out_json}")

    # --- Print adjacency matrix summary ---
    print("\n" + "=" * 60)
    print("ADJACENCY MATRIX SUMMARY")
    print("=" * 60)
    print(f"{'Map':<20s} {'N EDs':>6s} {'Mean N':>8s} {'Connected':>12s} {'Airdrie EDs':>13s} {'Flag 4+':>9s}")
    print("-" * 72)
    for s in all_summaries:
        flag_str = "YES" if s["airdrie_split_exceeds_4"] else "no"
        conn_str = "YES" if s["fully_connected"] else "NO"
        print(
            f"{s['map']:<20s} {s['n_eds']:>6d} {s['mean_neighbor_count']:>8.2f} "
            f"{conn_str:>12s} {s['airdrie_ed_count']:>13d} {flag_str:>9s}"
        )

    print("\n" + "=" * 60)
    print("AIRDRIE SPLIT FINDING")
    print("=" * 60)
    for s in all_summaries:
        print(f"\n  {s['map']}: {s['airdrie_ed_count']} EDs contain part of Airdrie")
        if s["airdrie_eds"]:
            for ed in s["airdrie_eds"]:
                print(f"    - {ed}")
        if s["airdrie_split_exceeds_4"]:
            print(f"  *** PRE-REGISTRATION FLAG: Airdrie split >= {AIRDRIE_SPLIT_FLAG_COUNT} (cracking signal) ***")

    # --- Contiguity gate summary ---
    print("\n" + "=" * 60)
    print("CONTIGUITY GATE RESULTS")
    print("=" * 60)
    for s in all_summaries:
        verdict = "PASS" if s["fully_connected"] else f"FAIL ({s['n_components']} components)"
        print(f"  {s['map']:<20s}: {verdict}")


if __name__ == "__main__":
    main()
