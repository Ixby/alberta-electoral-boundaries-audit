"""
T2 — Per-ED Area Fidelity

For each of the 89 EDs in each map, computes:
  area_error = (official_area - dpg_area) / official_area

The official shapefile includes PopCensus — this lets us also check whether
the commission-stated population is consistent with the area-matched DPG ED.

Pass threshold: mean absolute error < 1%; no single ED > 3%.
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

DPG_MAJ = REPO / "data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg"
DPG_MIN = REPO / "data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg"
OFF_MAJ = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
OUT = ROOT / "outputs/t2_area_fidelity.csv"
OUT.parent.mkdir(exist_ok=True)


def max_overlap_match(dpg_gdf, off_gdf):
    """
    Returns a DataFrame with columns:
      dpg_name | official_name | official_EDNum | dpg_area_m2 | off_area_m2 |
      area_error_pct | official_pop | official_km2
    """
    rows = []
    for _, dpg_row in dpg_gdf.iterrows():
        dpg_name = dpg_row["name_2026"].strip()
        intersections = off_gdf.copy()
        intersections["iarea"] = off_gdf.geometry.intersection(dpg_row.geometry).area
        best_idx = intersections["iarea"].idxmax()
        best = off_gdf.loc[best_idx]

        dpg_area = dpg_row.geometry.area
        off_area = best.geometry.area
        err_pct = 100 * (off_area - dpg_area) / off_area if off_area > 0 else np.nan

        rows.append(
            {
                "map": None,
                "dpg_name": dpg_name,
                "official_name": best["EDName2025"],
                "official_ed_num": best["EDNum2025"],
                "dpg_area_km2": round(dpg_area / 1e6, 4),
                "official_area_km2": round(off_area / 1e6, 4),
                "area_error_pct": round(err_pct, 3),
                "area_error_abs_pct": round(abs(err_pct), 3),
                "official_pop": best["PopCensus"],
                "official_km2_attr": best["Km2"],
            }
        )
    return pd.DataFrame(rows)


def run_map(label, dpg_path, off_path):
    print(f"\n=== {label} ===")
    dpg = gpd.read_file(dpg_path).to_crs("EPSG:3400")
    off = gpd.read_file(off_path).to_crs("EPSG:3400")

    df = max_overlap_match(dpg, off)
    df["map"] = label

    mean_abs = df["area_error_abs_pct"].mean()
    max_abs = df["area_error_abs_pct"].max()
    over3 = (df["area_error_abs_pct"] > 3).sum()

    print(f"  Mean absolute area error: {mean_abs:.3f}%")
    print(
        f"  Max absolute area error:  {max_abs:.3f}%  ({df.loc[df['area_error_abs_pct'].idxmax(), 'dpg_name']})"
    )
    print(f"  EDs with error > 3%:      {over3}")
    print(f"  T2 PASS threshold:        mean < 1%, no ED > 3%")
    t2_pass = mean_abs < 1.0 and max_abs <= 3.0
    print(f"  T2 RESULT:                {'PASS' if t2_pass else 'FAIL'}")
    if over3:
        worst = df[df["area_error_abs_pct"] > 3][
            ["dpg_name", "official_name", "area_error_pct", "area_error_abs_pct"]
        ].sort_values("area_error_abs_pct", ascending=False)
        print("  Worst offenders (top 10):")
        print(worst.head(10).to_string(index=False))

    df["t2_pass"] = t2_pass
    return df


def main():
    rows_maj = run_map("majority", DPG_MAJ, OFF_MAJ)
    rows_min = run_map("minority", DPG_MIN, OFF_MIN)
    combined = pd.concat([rows_maj, rows_min], ignore_index=True)
    combined.to_csv(OUT, index=False)
    print(f"\nSaved -> {OUT}")


if __name__ == "__main__":
    main()
