"""
T-A — Sub-VA Ceiling Estimation

Estimates the theoretical maximum IoU achievable by any VA-resolution DPG
reconstruction. For each official ED polygon, determines what fraction of its
area consists of VAs that are fully contained inside vs VAs that straddle the
official boundary.

ceiling_IoU = sum(area of fully-contained VAs) / official_ed_area

If the ceiling is >=75%, most of the observed ~37% IoU deficit is attributable
to VA misassignment (correctable), not sub-VA precision limits (irreducible).

Pre-registered hypothesis H2: mean ceiling IoU >= 75% for majority reconstructed EDs.
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

VA_PATH  = REPO / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
OFF_MAJ  = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN  = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
OUT      = ROOT / "outputs/ta_va_ceiling.csv"
OUT.parent.mkdir(exist_ok=True)

CONTAINED_THRESHOLD = 0.95  # VA is "fully inside" if >=95% of its area is in the ED


def ceiling_for_map(label, off_path, va_gdf):
    print(f"\n=== {label} ===")
    off = gpd.read_file(off_path).to_crs("EPSG:3400")
    va  = va_gdf.copy()

    rows = []
    total_eds = len(off)

    for i, (_, ed_row) in enumerate(off.iterrows()):
        if i % 10 == 0:
            print(f"  Processing ED {i+1}/{total_eds}...")

        ed_geom     = ed_row.geometry
        ed_name     = ed_row["EDName2025"]
        ed_area     = ed_geom.area

        # Candidate VAs: those that intersect this ED
        candidates  = va[va.geometry.intersects(ed_geom)]
        if candidates.empty:
            rows.append({
                "map": label, "ed_name": ed_name,
                "official_area_km2": round(ed_area / 1e6, 4),
                "ceiling_iou_pct": 0.0,
                "n_full_vas": 0, "n_partial_vas": 0,
                "full_va_area_km2": 0.0, "partial_va_area_km2": 0.0,
            })
            continue

        full_va_area    = 0.0
        partial_va_area = 0.0
        n_full          = 0
        n_partial       = 0

        for _, va_row in candidates.iterrows():
            va_geom  = va_row.geometry
            va_area  = va_geom.area
            if va_area == 0:
                continue

            try:
                inter_area = va_geom.intersection(ed_geom).area
            except Exception:
                continue

            contained_pct = inter_area / va_area

            if contained_pct >= CONTAINED_THRESHOLD:
                full_va_area += va_area
                n_full += 1
            else:
                partial_va_area += inter_area
                n_partial += 1

        # Ceiling: fully-contained VAs contribute their full area;
        # partial VAs contribute only what's inside the ED boundary.
        # This is the best a VA-resolution method can do.
        ceiling_area = full_va_area + partial_va_area
        ceiling_iou  = 100.0 * ceiling_area / ed_area if ed_area > 0 else 0.0

        rows.append({
            "map": label,
            "ed_name": ed_name,
            "official_area_km2": round(ed_area / 1e6, 4),
            "ceiling_iou_pct": round(ceiling_iou, 2),
            "n_full_vas": n_full,
            "n_partial_vas": n_partial,
            "full_va_area_km2": round(full_va_area / 1e6, 4),
            "partial_va_area_km2": round(partial_va_area / 1e6, 4),
        })

    df = pd.DataFrame(rows)

    mean_ceiling = df["ceiling_iou_pct"].mean()
    min_ceiling  = df["ceiling_iou_pct"].min()
    below_75     = (df["ceiling_iou_pct"] < 75).sum()
    below_50     = (df["ceiling_iou_pct"] < 50).sum()

    print(f"\n  Mean ceiling IoU:        {mean_ceiling:.1f}%")
    print(f"  Min ceiling IoU:         {min_ceiling:.1f}%  ({df.loc[df['ceiling_iou_pct'].idxmin(), 'ed_name']})")
    print(f"  EDs with ceiling < 75%:  {below_75}")
    print(f"  EDs with ceiling < 50%:  {below_50}")
    print(f"  H2 pre-registered:       mean ceiling >= 75%")
    h2_pass = mean_ceiling >= 75.0
    print(f"  H2 RESULT:               {'SUPPORTED' if h2_pass else 'NOT SUPPORTED'}")

    return df


def main():
    print("Loading VA polygons...")
    va = gpd.read_file(VA_PATH).to_crs("EPSG:3400")
    print(f"  {len(va)} VAs loaded")

    rows_maj = ceiling_for_map("majority", OFF_MAJ, va)
    rows_min = ceiling_for_map("minority", OFF_MIN, va)
    combined = pd.concat([rows_maj, rows_min], ignore_index=True)
    combined.to_csv(OUT, index=False)
    print(f"\nSaved -> {OUT}")


if __name__ == "__main__":
    main()
