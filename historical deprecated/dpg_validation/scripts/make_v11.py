"""
make_v11.py — Construct v11 DPG GeoPackages for majority and minority maps

Methodology:
  The T-A diagnostic confirmed that official Elections Alberta shapefiles
  were built by dissolving VA polygons (ceiling IoU ~100%). Therefore, the
  correct v11 VA-to-ED assignment can be determined objectively by spatial
  join: for each VA centroid, find which official ED contains it.

  v11 geometry = dissolve(VA polygons grouped by official-sjoin assignment)

  This produces geometry that should approach the T-A ceiling (~100% IoU)
  because both v11 and official are VA-polygon dissolves, differing only
  in how many VAs are assigned to each ED.

Protocol (per experiment plan):
  - Source VA polygons: read-only (va_polygons_with_2023_votes.gpkg)
  - Official shapefiles: read-only reference geometry, not modified
  - All assignments logged to v11_va_assignment_log.csv
  - Reason code: OFFICIAL_SJOIN (automated, from official boundary sjoin)

Outputs:
  data/shapefiles/derived/v11_majority_2026_eds.gpkg
  data/shapefiles/derived/v11_minority_2026_eds.gpkg
  dpg_validation/outputs/v11_va_assignment_log.csv
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

VA_PATH = REPO / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
DPG_MAJ = REPO / "data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg"
DPG_MIN = REPO / "data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg"
OFF_MAJ = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"

OUT_MAJ = REPO / "data/shapefiles/derived/v11_majority_2026_eds.gpkg"
OUT_MIN = REPO / "data/shapefiles/derived/v11_minority_2026_eds.gpkg"
OUT_LOG = ROOT / "outputs/v11_va_assignment_log.csv"
OUT_LOG.parent.mkdir(exist_ok=True)


def assign_vas_to_eds(va_gdf, off_gdf, label):
    """Return VA GeoDataFrame with 'v11_ed' column set from official sjoin."""
    va = va_gdf.copy()
    centroids = va.copy()
    centroids.geometry = va.geometry.centroid

    joined = gpd.sjoin(
        centroids[["geometry"]],
        off_gdf[["geometry", "EDName2025"]],
        how="left",
        predicate="within",
    )

    missed = joined[joined["EDName2025"].isna()].index
    if len(missed):
        print(f"  {label}: {len(missed)} VA centroids outside all EDs — using nearest")
        nearest = gpd.sjoin_nearest(
            centroids.loc[missed, ["geometry"]],
            off_gdf[["geometry", "EDName2025"]],
            how="left",
        )
        joined.loc[missed, "EDName2025"] = nearest["EDName2025"].values

    va["v11_ed"] = joined["EDName2025"].values
    return va


def build_v11_geometry(va_assigned, label):
    """Dissolve VA polygons grouped by v11_ed assignment. Returns GeoDataFrame."""
    print(f"  {label}: dissolving {len(va_assigned)} VAs into EDs...")
    dissolved = (
        va_assigned[["geometry", "v11_ed"]]
        .dissolve(by="v11_ed")
        .reset_index()
        .rename(columns={"v11_ed": "EDName2025"})
    )
    dissolved["name_2026"] = dissolved["EDName2025"]
    print(f"  {label}: {len(dissolved)} EDs produced")
    return dissolved


def compute_iou(v11_gdf, off_gdf, label):
    """Quick IoU check: v11 vs official, using max-overlap matching."""
    v11 = v11_gdf.copy()
    off = off_gdf.copy()

    ious = []
    for _, off_row in off.iterrows():
        off_name = off_row["EDName2025"]
        # Find v11 ED with most overlap
        intersections = v11.geometry.intersection(off_row.geometry)
        areas = intersections.area
        best_idx = areas.idxmax()
        best_v11 = v11.loc[best_idx]

        union_area = off_row.geometry.union(best_v11.geometry).area
        inter_area = areas[best_idx]
        iou = inter_area / union_area if union_area > 0 else 0
        ious.append(
            {
                "official_ed": off_name,
                "v11_ed": best_v11["EDName2025"],
                "name_match": off_name == best_v11["EDName2025"],
                "iou": round(iou * 100, 2),
            }
        )

    df = pd.DataFrame(ious)
    mean_iou = df["iou"].mean()
    min_iou = df["iou"].min()
    n_low = (df["iou"] < 90).sum()
    print(f"\n  {label} v11 IoU vs official:")
    print(f"    Mean IoU:        {mean_iou:.1f}%")
    print(
        f"    Min IoU:         {min_iou:.1f}%  ({df.loc[df['iou'].idxmin(),'official_ed']})"
    )
    print(f"    EDs < 90% IoU:   {n_low}")
    print(f"    Name mismatches: {(~df['name_match']).sum()}")
    return df


def build_assignment_log(va_assigned, dpg_gdf, label):
    """Compare v11 assignments to v0_10 assignments; log every VA."""
    dpg = dpg_gdf.copy()
    dpg["_dpg_name"] = dpg["name_2026"].str.strip()

    centroids = va_assigned.copy()
    centroids.geometry = va_assigned.geometry.centroid

    dpg_join = gpd.sjoin(
        centroids[["geometry"]],
        dpg[["geometry", "_dpg_name"]],
        how="left",
        predicate="within",
    )
    missed = dpg_join[dpg_join["_dpg_name"].isna()].index
    if len(missed):
        nearest = gpd.sjoin_nearest(
            centroids.loc[missed, ["geometry"]],
            dpg[["geometry", "_dpg_name"]],
            how="left",
        )
        dpg_join.loc[missed, "_dpg_name"] = nearest["_dpg_name"].values

    rows = []
    for idx, row in va_assigned.iterrows():
        old_ed = dpg_join.loc[idx, "_dpg_name"] if idx in dpg_join.index else None
        new_ed = row["v11_ed"]
        changed = old_ed != new_ed
        rows.append(
            {
                "map": label,
                "va_idx": idx,
                "old_ed": old_ed,
                "new_ed": new_ed,
                "changed": changed,
                "reason_code": "OFFICIAL_SJOIN" if changed else "UNCHANGED",
                "raster_evidence_note": "",
                "confidence": "high" if changed else "n/a",
                "reviewer": "automated",
            }
        )

    log_df = pd.DataFrame(rows)
    n_changed = log_df["changed"].sum()
    print(f"  {label}: {n_changed}/{len(log_df)} VA assignments changed from v0_10")
    return log_df


def main():
    print("Loading VA polygons...")
    va = gpd.read_file(VA_PATH).to_crs("EPSG:3400")
    print(f"  {len(va)} VAs loaded")

    print("\nLoading DPG v0_10 substrates (for change log)...")
    dpg_maj = gpd.read_file(DPG_MAJ).to_crs("EPSG:3400")
    dpg_min = gpd.read_file(DPG_MIN).to_crs("EPSG:3400")

    print("\nLoading official shapefiles...")
    off_maj = gpd.read_file(OFF_MAJ).to_crs("EPSG:3400")
    off_min = gpd.read_file(OFF_MIN).to_crs("EPSG:3400")

    all_logs = []

    for label, dpg, off, out_path in [
        ("majority", dpg_maj, off_maj, OUT_MAJ),
        ("minority", dpg_min, off_min, OUT_MIN),
    ]:
        print(f"\n=== {label} ===")

        print("  Assigning VAs to official EDs via centroid sjoin...")
        va_assigned = assign_vas_to_eds(va, off, label)

        v11_gdf = build_v11_geometry(va_assigned, label)
        v11_gdf.to_file(out_path, driver="GPKG")
        print(f"  Saved -> {out_path}")

        iou_df = compute_iou(v11_gdf, off, label)

        log_df = build_assignment_log(va_assigned, dpg, label)
        all_logs.append(log_df)

    pd.concat(all_logs, ignore_index=True).to_csv(OUT_LOG, index=False)
    print(f"\nAssignment log saved -> {OUT_LOG}")
    print("\nmake_v11 complete.")


if __name__ == "__main__":
    main()
