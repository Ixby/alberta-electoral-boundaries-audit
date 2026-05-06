"""
T3 — Geometric Boundary Displacement

For each matched ED pair (DPG vs official), computes:
  - Hausdorff distance (metres) — worst-case boundary displacement
  - Mean boundary displacement — average distance between boundary lines,
    estimated by densifying both boundaries and computing mean nearest-neighbour

Pass threshold: mean Hausdorff < 500 m across all EDs; no ED > 2000 m.

Note: Hausdorff is computed in EPSG:3400 (NAD83 / Alberta 10-TM), which is
a metre-unit projected CRS. No reprojection needed.
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import MultiLineString
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

DPG_MAJ = REPO / "data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg"
DPG_MIN = REPO / "data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg"
OFF_MAJ = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
OUT     = ROOT / "outputs/t3_displacement_per_ed.csv"
OUT.parent.mkdir(exist_ok=True)

DENSIFY_SPACING = 200  # metres — interpolate boundary points every 200 m


def densify_boundary(geom, spacing=DENSIFY_SPACING):
    """Return an array of (x, y) points along the exterior at ~spacing metres."""
    from shapely.geometry import MultiPolygon, Polygon
    if isinstance(geom, MultiPolygon):
        rings = [p.exterior for p in geom.geoms]
    else:
        rings = [geom.exterior]
    pts = []
    for ring in rings:
        length = ring.length
        n = max(2, int(length / spacing))
        for i in range(n):
            pt = ring.interpolate(i * length / n)
            pts.append((pt.x, pt.y))
    return np.array(pts)


def mean_boundary_displacement(geom_a, geom_b):
    """Mean nearest-neighbour distance from densified boundary A to B."""
    from scipy.spatial import cKDTree
    pts_a = densify_boundary(geom_a)
    pts_b = densify_boundary(geom_b)
    if len(pts_a) == 0 or len(pts_b) == 0:
        return np.nan
    tree = cKDTree(pts_b)
    dists, _ = tree.query(pts_a, k=1)
    return float(np.mean(dists))


def run_map(label, dpg_path, off_path):
    print(f"\n=== {label} ===")
    dpg = gpd.read_file(dpg_path).to_crs("EPSG:3400")
    off = gpd.read_file(off_path).to_crs("EPSG:3400")

    rows = []
    for _, dpg_row in dpg.iterrows():
        dpg_name = dpg_row["name_2026"].strip()
        # Match to official by max overlap
        off_copy = off.copy()
        off_copy["iarea"] = off.geometry.intersection(dpg_row.geometry).area
        best_idx = off_copy["iarea"].idxmax()
        best = off.loc[best_idx]

        try:
            hausdorff = dpg_row.geometry.hausdorff_distance(best.geometry)
        except Exception:
            hausdorff = np.nan

        try:
            mean_disp = mean_boundary_displacement(dpg_row.geometry, best.geometry)
        except Exception:
            mean_disp = np.nan

        rows.append({
            "map": label,
            "dpg_name": dpg_name,
            "official_name": best["EDName2025"],
            "hausdorff_m": round(hausdorff, 1) if not np.isnan(hausdorff) else None,
            "mean_displacement_m": round(mean_disp, 1) if not np.isnan(mean_disp) else None,
        })

    df = pd.DataFrame(rows)

    mean_h = df["hausdorff_m"].mean()
    max_h  = df["hausdorff_m"].max()
    over2k = (df["hausdorff_m"] > 2000).sum()

    print(f"  Mean Hausdorff:       {mean_h:.1f} m")
    print(f"  Max Hausdorff:        {max_h:.1f} m  ({df.loc[df['hausdorff_m'].idxmax(), 'dpg_name']})")
    print(f"  EDs with Hausdorff > 2 km: {over2k}")
    print(f"  Mean boundary disp:   {df['mean_displacement_m'].mean():.1f} m")
    print(f"  T3 PASS threshold:    mean Hausdorff < 500 m, no ED > 2000 m")
    t3_pass = mean_h < 500 and max_h <= 2000
    print(f"  T3 RESULT:            {'PASS' if t3_pass else 'FAIL'}")

    if over2k:
        worst = df[df["hausdorff_m"] > 2000][["dpg_name","official_name","hausdorff_m"]].sort_values("hausdorff_m", ascending=False)
        print("  Worst offenders (top 10):")
        print(worst.head(10).to_string(index=False))

    df["t3_pass"] = t3_pass
    return df


def main():
    try:
        from scipy.spatial import cKDTree
    except ImportError:
        print("WARNING: scipy not available — mean_displacement will be skipped")

    rows_maj = run_map("majority", DPG_MAJ, OFF_MAJ)
    rows_min = run_map("minority", DPG_MIN, OFF_MIN)
    combined = pd.concat([rows_maj, rows_min], ignore_index=True)
    combined.to_csv(OUT, index=False)
    print(f"\nSaved -> {OUT}")


if __name__ == "__main__":
    main()
