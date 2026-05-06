"""
T-B — VA Misassignment Classification

For each VA polygon in the DPG, determines:
  - Which ED it is assigned to in v0_10 (DPG assignment)
  - Which ED contains its centroid in the official shapefile (oracle assignment)

If they differ, the VA is a candidate misassignment.
If the VA centroid straddles or is near the official boundary, it may be a
Type B (precision) case rather than a genuine misassignment.

Classification:
  correct    : DPG and official agree (centroid-in-polygon match)
  misassigned: DPG and official disagree — VA centroid in wrong ED in DPG
  boundary   : VA centroid within 200 m of official boundary — ambiguous

Output:
  outputs/tb_va_misassignment_map.csv
  outputs/tb_misassignment_summary.csv (per-ED rework priority list)

This output drives the v11 rework prioritization.
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

VA_PATH  = REPO / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
DPG_MAJ  = REPO / "data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg"
DPG_MIN  = REPO / "data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg"
OFF_MAJ  = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN  = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
OUT_VA   = ROOT / "outputs/tb_va_misassignment_map.csv"
OUT_SUM  = ROOT / "outputs/tb_misassignment_summary.csv"
OUT_VA.parent.mkdir(exist_ok=True)

BOUNDARY_BUFFER_M = 200  # VAs within this distance of official boundary = "boundary" class


def classify_misassignments(label, dpg_path, off_path, va_gdf):
    print(f"\n=== {label} ===")
    dpg = gpd.read_file(dpg_path).to_crs("EPSG:3400")
    off = gpd.read_file(off_path).to_crs("EPSG:3400")
    va  = va_gdf.copy()

    dpg["_name"] = dpg["name_2026"].str.strip()

    # Assign VAs via centroid-in-polygon for DPG
    print("  Assigning VAs to DPG EDs...")
    va_centroids = va.copy()
    va_centroids.geometry = va.geometry.centroid

    dpg_join = gpd.sjoin(
        va_centroids[["geometry"]],
        dpg[["geometry", "_name"]],
        how="left", predicate="within"
    )
    missed = dpg_join[dpg_join["_name"].isna()].index
    if len(missed):
        nearest = gpd.sjoin_nearest(
            va_centroids.loc[missed, ["geometry"]],
            dpg[["geometry", "_name"]],
            how="left"
        )
        dpg_join.loc[missed, "_name"] = nearest["_name"].values
    va["dpg_ed"] = dpg_join["_name"].values

    # Assign VAs via centroid-in-polygon for official
    print("  Assigning VAs to official EDs...")
    off_join = gpd.sjoin(
        va_centroids[["geometry"]],
        off[["geometry", "EDName2025"]],
        how="left", predicate="within"
    )
    missed_off = off_join[off_join["EDName2025"].isna()].index
    if len(missed_off):
        nearest_off = gpd.sjoin_nearest(
            va_centroids.loc[missed_off, ["geometry"]],
            off[["geometry", "EDName2025"]],
            how="left"
        )
        off_join.loc[missed_off, "EDName2025"] = nearest_off["EDName2025"].values
    va["official_ed"] = off_join["EDName2025"].values

    # Build official boundary network for proximity check
    print("  Building official boundary for proximity classification...")
    from shapely.ops import unary_union
    off_boundary = unary_union([g.boundary for g in off.geometry])
    off_boundary_buf = off_boundary.buffer(BOUNDARY_BUFFER_M)

    # Classify each VA
    print("  Classifying VAs...")
    rows = []
    for idx, va_row in va.iterrows():
        dpg_ed     = va_row["dpg_ed"]
        official_ed = va_row["official_ed"]
        va_area    = va_row.geometry.area

        if dpg_ed == official_ed:
            status = "correct"
        else:
            # Check if centroid is near official boundary
            centroid = va_row.geometry.centroid
            near_boundary = centroid.within(off_boundary_buf)
            if near_boundary:
                status = "boundary"
            else:
                status = "misassigned"

        rows.append({
            "map": label,
            "va_idx": idx,
            "va_area_km2": round(va_area / 1e6, 4),
            "dpg_ed": dpg_ed,
            "official_ed": official_ed,
            "status": status,
        })

    df = pd.DataFrame(rows)

    n_correct     = (df["status"] == "correct").sum()
    n_misassigned = (df["status"] == "misassigned").sum()
    n_boundary    = (df["status"] == "boundary").sum()
    total         = len(df)

    print(f"\n  Total VAs:            {total}")
    print(f"  Correct:              {n_correct} ({100*n_correct/total:.1f}%)")
    print(f"  Misassigned (clear):  {n_misassigned} ({100*n_misassigned/total:.1f}%)")
    print(f"  Near boundary (ambig):{n_boundary} ({100*n_boundary/total:.1f}%)")

    # Per-ED rework summary (sorted by n_misassigned desc = priority)
    miss_df = df[df["status"] == "misassigned"]
    summary_rows = []

    for ed_name in off["EDName2025"].unique():
        # VAs officially belonging to this ED that are misassigned in DPG (under-claim)
        under = miss_df[(miss_df["official_ed"] == ed_name) & (miss_df["dpg_ed"] != ed_name)]
        # VAs in DPG assigned to this ED that belong elsewhere (over-claim)
        over  = miss_df[(miss_df["dpg_ed"] == ed_name) & (miss_df["official_ed"] != ed_name)]

        summary_rows.append({
            "map": label,
            "ed_name": ed_name,
            "n_underclaim_vas": len(under),
            "n_overclaim_vas": len(over),
            "n_total_rework": len(under) + len(over),
            "underclaim_area_km2": round(under["va_area_km2"].sum(), 4),
            "overclaim_area_km2": round(over["va_area_km2"].sum(), 4),
        })

    summary = pd.DataFrame(summary_rows).sort_values("n_total_rework", ascending=False)

    print(f"\n  Top 10 EDs by rework VA count:")
    print(summary.head(10)[["ed_name","n_underclaim_vas","n_overclaim_vas","n_total_rework"]].to_string(index=False))

    return df, summary


def main():
    print("Loading VA polygons...")
    va = gpd.read_file(VA_PATH).to_crs("EPSG:3400")
    print(f"  {len(va)} VAs loaded")

    all_va_rows = []
    all_summary = []

    va_maj, sum_maj = classify_misassignments("majority", DPG_MAJ, OFF_MAJ, va)
    all_va_rows.append(va_maj)
    all_summary.append(sum_maj)

    va_min, sum_min = classify_misassignments("minority", DPG_MIN, OFF_MIN, va)
    all_va_rows.append(va_min)
    all_summary.append(sum_min)

    pd.concat(all_va_rows, ignore_index=True).to_csv(OUT_VA, index=False)
    pd.concat(all_summary, ignore_index=True).to_csv(OUT_SUM, index=False)

    print(f"\nSaved -> {OUT_VA}")
    print(f"Saved -> {OUT_SUM}")


if __name__ == "__main__":
    main()
