"""
T1 — Vote Attribution Equivalence

For each VA polygon, determine which 2026 ED it falls in under the DPG vs the
official shapefile. Misassigned VAs carry real 2023 votes. Computes:
  - Count and share of VAs misassigned (majority and minority separately)
  - Total votes on misassigned VAs
  - Net partisan swing from mismatch (NDP/UCP delta on efficiency gap proxy)

Pass threshold: <= 2% of VAs misassigned; net partisan swing < 0.1 pp EG proxy.
"""

import sys
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
OUT = ROOT / "outputs/t1_misassignment_report.csv"
OUT.parent.mkdir(exist_ok=True)


def assign_va_to_ed(va_gdf, ed_gdf, ed_name_col):
    """Return a Series mapping va index → ED name, using centroid-in-polygon."""
    centroids = va_gdf.copy()
    centroids.geometry = va_gdf.geometry.centroid
    joined = gpd.sjoin(
        centroids[["geometry", "va_ndp", "va_ucp"]],
        ed_gdf[["geometry", ed_name_col]],
        how="left",
        predicate="within",
    )
    # Fall back to nearest for any that missed
    missed = joined[joined[ed_name_col].isna()].index
    if len(missed):
        nearest = gpd.sjoin_nearest(
            centroids.loc[missed, ["geometry"]],
            ed_gdf[["geometry", ed_name_col]],
            how="left",
        )
        joined.loc[missed, ed_name_col] = nearest[ed_name_col].values
    return joined[ed_name_col]


def dpg_name_series(dpg_gdf):
    """Extract clean name_2026 (the reliable column) from DPG."""
    return dpg_gdf["name_2026"].str.strip()


def max_overlap_name_map(dpg_gdf, off_gdf, off_name_col):
    """
    Build a dict: dpg_name_2026 → official EDName
    by finding the official polygon with the largest intersection area
    for each DPG polygon.
    """
    dpg_proj = dpg_gdf.copy()
    off_proj = off_gdf.copy()
    mapping = {}
    for _, dpg_row in dpg_proj.iterrows():
        dpg_name = dpg_row["name_2026"].strip()
        intersections = off_proj.copy()
        intersections["iarea"] = off_proj.geometry.intersection(dpg_row.geometry).area
        best = intersections.loc[intersections["iarea"].idxmax(), off_name_col]
        mapping[dpg_name] = best
    return mapping


def efficiency_gap(ndp, ucp):
    total_votes = sum(ndp) + sum(ucp)
    if total_votes == 0:
        return np.nan
    wasted_ndp = sum(
        (ndp_i - (ndp_i + ucp_i) / 2) if ndp_i > ucp_i else ndp_i
        for ndp_i, ucp_i in zip(ndp, ucp)
    )
    wasted_ucp = sum(
        (ucp_i - (ndp_i + ucp_i) / 2) if ucp_i > ndp_i else ucp_i
        for ndp_i, ucp_i in zip(ndp, ucp)
    )
    return (wasted_ndp - wasted_ucp) / total_votes


def run_map(label, dpg_path, off_path, off_name_col, va_gdf):
    print(f"\n=== {label} ===")
    dpg = gpd.read_file(dpg_path).to_crs("EPSG:3400")
    off = gpd.read_file(off_path).to_crs("EPSG:3400")

    dpg["_dpg_name"] = dpg["name_2026"].str.strip()

    # Assign VAs using centroids against DPG
    va_dpg_assign = assign_va_to_ed(va_gdf, dpg, "_dpg_name")
    # Assign VAs using centroids against official
    va_off_assign = assign_va_to_ed(va_gdf, off, off_name_col)

    # Build name map DPG → official for comparison
    name_map = max_overlap_name_map(dpg, off, off_name_col)

    # Translate DPG assignments to official name space
    va_dpg_as_official = va_dpg_assign.map(name_map)

    total_vas = len(va_gdf)
    mismatch_mask = va_dpg_as_official != va_off_assign
    n_mismatch = mismatch_mask.sum()
    pct_mismatch = 100 * n_mismatch / total_vas

    mismatch_ndp = va_gdf.loc[mismatch_mask, "va_ndp"].sum()
    mismatch_ucp = va_gdf.loc[mismatch_mask, "va_ucp"].sum()
    total_ndp = va_gdf["va_ndp"].sum()
    total_ucp = va_gdf["va_ucp"].sum()

    print(f"  Total VAs:            {total_vas}")
    print(f"  Misassigned VAs:      {n_mismatch} ({pct_mismatch:.2f}%)")
    print(f"  Votes on misassigned: NDP={mismatch_ndp:,}  UCP={mismatch_ucp:,}")
    print(f"  Total votes:          NDP={total_ndp:,}  UCP={total_ucp:,}")
    print(
        f"  Mismatch vote share:  {100*(mismatch_ndp+mismatch_ucp)/(total_ndp+total_ucp):.2f}%"
    )

    # EG under DPG assignment vs official assignment
    def agg_votes(assignment):
        df = va_gdf.copy()
        df["_ed"] = assignment
        agg = df.groupby("_ed")[["va_ndp", "va_ucp"]].sum().reset_index()
        return agg["va_ndp"].tolist(), agg["va_ucp"].tolist()

    ndp_dpg, ucp_dpg = agg_votes(va_dpg_as_official)
    ndp_off, ucp_off = agg_votes(va_off_assign)
    eg_dpg = efficiency_gap(ndp_dpg, ucp_dpg)
    eg_off = efficiency_gap(ndp_off, ucp_off)
    eg_delta = abs(eg_dpg - eg_off) * 100

    print(f"  EG (DPG assignment):  {eg_dpg*100:+.3f}%")
    print(f"  EG (official):        {eg_off*100:+.3f}%")
    print(f"  EG delta:             {eg_delta:.3f} pp")
    print(f"  T1 PASS threshold:    <= 2% mismatch, < 0.1 pp EG swing")
    t1_pass = pct_mismatch <= 2.0 and eg_delta < 0.1
    print(f"  T1 RESULT:            {'PASS' if t1_pass else 'FAIL'}")

    return {
        "map": label,
        "total_vas": total_vas,
        "misassigned_vas": n_mismatch,
        "pct_misassigned": round(pct_mismatch, 3),
        "mismatch_ndp_votes": int(mismatch_ndp),
        "mismatch_ucp_votes": int(mismatch_ucp),
        "eg_dpg_pct": round(eg_dpg * 100, 4),
        "eg_official_pct": round(eg_off * 100, 4),
        "eg_delta_pp": round(eg_delta, 4),
        "t1_pass": t1_pass,
    }


def main():
    print("Loading VA polygons...")
    va = gpd.read_file(VA_PATH).to_crs("EPSG:3400")
    if "va_ndp" not in va.columns or "va_ucp" not in va.columns:
        sys.exit(
            "ERROR: va_polygons_with_2023_votes.gpkg missing va_ndp/va_ucp columns"
        )

    rows = []
    rows.append(run_map("majority", DPG_MAJ, OFF_MAJ, "EDName2025", va))
    rows.append(run_map("minority", DPG_MIN, OFF_MIN, "EDName2025", va))

    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print(f"\nSaved -> {OUT}")


if __name__ == "__main__":
    main()
