"""
v6 output writer: merges v6 polygons into v5 (minority) and approximate
(majority) baseline files, produces impact CSV and log JSON.
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

from shape_refinement_v6 import (
    ROOT, DATA_DIR, ANALYSIS_DIR, AREA_CRS, WORK_CRS,
)


def write_outputs(results: dict[str, Polygon], log: dict):
    """Merge v6 polygons into v5 minority + approximate majority.

    - Minority: load v5, overwrite the 3 Tier C polygons with v6 versions.
    - Majority: load approximate (Tier A only), append v6 polygons for Tier C.
      Note: the full majority 89-row file requires merging from population file.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ---------- MINORITY ----------
    v5_min = gpd.read_file(DATA_DIR / "v0_1_refined_v5_minority_2026_eds.gpkg").to_crs(AREA_CRS)
    rows = []
    for _, r in v5_min.iterrows():
        name = r["name_2026"]
        if name in results and name in ("Calgary-De Winton", "Calgary-South", "Edmonton-Windermere"):
            # Replace geometry with v6
            new_r = r.copy()
            new_r.geometry = results[name]
            new_r["v6_method"] = "pixel-exact-hsv-v6"
            new_r["tier"] = "C-v6-pixel-exact"
            rows.append(new_r)
        else:
            new_r = r.copy()
            new_r["v6_method"] = "carried-forward-from-v5"
            rows.append(new_r)

    v6_min = gpd.GeoDataFrame(rows, geometry="geometry", crs=AREA_CRS)
    # Add missing column if not present
    if "v6_method" not in v6_min.columns:
        v6_min["v6_method"] = "carried-forward-from-v5"
    v6_min_out_path = DATA_DIR / "v0_1_refined_v6_minority_2026_eds.gpkg"
    # Reproject back to working CRS for consistency with v5
    v6_min_wc = v6_min.to_crs(WORK_CRS)
    v6_min_wc.to_file(v6_min_out_path, driver="GPKG")
    print(f"[WRITE] {v6_min_out_path.name}: {len(v6_min_wc)} rows "
          f"({sum(1 for _, r in v6_min.iterrows() if r.get('v6_method') == 'pixel-exact-hsv-v6')} v6 polygons)")

    # ---------- MAJORITY ----------
    approx_maj = gpd.read_file(DATA_DIR / "v0_1_approximate_majority_2026_eds.gpkg").to_crs(AREA_CRS)
    # Get population file to know all 89 majority EDs
    pop = pd.read_csv(DATA_DIR / "v0_1_majority_2026_populations.csv")
    # Build rows: start from approx (57 Tier A), add v6 polygons for matched Tier C
    rows = []
    seen = set()
    for _, r in approx_maj.iterrows():
        name = r["name_2026"]
        new_r = r.copy()
        new_r["v6_method"] = "carried-forward-from-approx-v0_1"
        rows.append(new_r)
        seen.add(name)

    # Add v6 majority polygons
    v6_majority_targets = {
        "Calgary-East", "Calgary-Falconridge-Conrich",
        "Calgary-Glenmore-Tsuut'ina", "Calgary-West-Elbow Valley",
        "Edmonton-Beaumont", "Edmonton-Enoch",
    }
    for name in v6_majority_targets:
        if name in results:
            seen.add(name)
            # Build a row that mirrors approx schema
            new_r = {c: None for c in approx_maj.columns}
            new_r["name_2026"] = name
            new_r["tier"] = "C-v6-pixel-exact"
            new_r["confidence"] = "low-visually-transcribed-v6"
            new_r["parents_2019"] = ""
            new_r["note"] = "v6 pixel-exact from commission thumbnail"
            new_r["v6_method"] = "pixel-exact-hsv-v6"
            new_r["geometry"] = results[name]
            rows.append(new_r)

    # For remaining Tier C EDs (rural, not in thumbnails), write NULL geometry
    for _, pr in pop.iterrows():
        if pr["ed_name"] not in seen:
            new_r = {c: None for c in approx_maj.columns}
            new_r["name_2026"] = pr["ed_name"]
            new_r["tier"] = "C-null"
            new_r["confidence"] = "null-no-thumbnail-coverage"
            new_r["parents_2019"] = ""
            new_r["note"] = f"Tier C majority — not vectorised in v6 (rural, not in city thumbnail)"
            new_r["v6_method"] = "null-escalated-in-methodology"
            new_r["geometry"] = None  # NULL geometry
            rows.append(new_r)

    # Normalise rows: convert any dict rows to pd.Series aligned to approx_maj columns
    cols = list(approx_maj.columns) + ["v6_method"]
    # Ensure unique columns (in case v6_method already exists)
    seen_cols = set(); cols = [c for c in cols if not (c in seen_cols or seen_cols.add(c))]
    normed = []
    for r in rows:
        if isinstance(r, dict):
            normed.append(pd.Series({c: r.get(c) for c in cols}))
        else:
            d = {c: r.get(c) for c in cols}
            normed.append(pd.Series(d))
    v6_maj = gpd.GeoDataFrame(normed, geometry="geometry", crs=AREA_CRS)
    v6_maj_out_path = DATA_DIR / "v0_1_refined_v6_majority_2026_eds.gpkg"
    # To_crs with None geom rows is fine
    v6_maj_wc = v6_maj.to_crs(WORK_CRS)
    v6_maj_wc.to_file(v6_maj_out_path, driver="GPKG")
    print(f"[WRITE] {v6_maj_out_path.name}: {len(v6_maj)} rows "
          f"({sum(1 for _, r in v6_maj.iterrows() if r.get('v6_method') == 'pixel-exact-hsv-v6')} v6 polygons)")

    # ---------- IMPACT CSV ----------
    impact_rows = []
    # Minority: v5 vs v6 per Tier C target
    for name in ["Calgary-De Winton", "Calgary-South", "Edmonton-Windermere"]:
        v5_sub = v5_min[v5_min["name_2026"] == name]
        v6_sub = v6_min[v6_min["name_2026"] == name]
        v5_area = v5_sub.geometry.iloc[0].area / 1e6 if not v5_sub.empty else None
        v6_area = v6_sub.geometry.iloc[0].area / 1e6 if (not v6_sub.empty and v6_sub.geometry.iloc[0] is not None) else None
        impact_rows.append({
            "map": "minority",
            "ed_name": name,
            "v5_area_km2": round(v5_area, 2) if v5_area else None,
            "v6_area_km2": round(v6_area, 2) if v6_area else None,
            "delta_km2": round(v6_area - v5_area, 2) if v5_area and v6_area else None,
            "delta_pct": round((v6_area - v5_area) / v5_area * 100, 1) if v5_area and v6_area else None,
        })
    # Majority: v6 new (no v5 baseline for these)
    for name in sorted(v6_majority_targets):
        v6_sub = v6_maj[v6_maj["name_2026"] == name]
        v6_area = v6_sub.geometry.iloc[0].area / 1e6 if (not v6_sub.empty and v6_sub.geometry.iloc[0] is not None) else None
        impact_rows.append({
            "map": "majority",
            "ed_name": name,
            "v5_area_km2": None,  # no v5 for majority Tier C
            "v6_area_km2": round(v6_area, 2) if v6_area else None,
            "delta_km2": None,
            "delta_pct": None,
        })

    impact_df = pd.DataFrame(impact_rows)
    impact_csv_path = DATA_DIR / "v0_1_boundary_refinement_impact_v6.csv"
    impact_df.to_csv(impact_csv_path, index=False)
    print(f"[WRITE] {impact_csv_path.name}: {len(impact_df)} rows")

    # ---------- LOG JSON ----------
    log_path = ANALYSIS_DIR / "v0_1_shape_refinement_v6_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, default=str)
    print(f"[WRITE] {log_path.name}")
