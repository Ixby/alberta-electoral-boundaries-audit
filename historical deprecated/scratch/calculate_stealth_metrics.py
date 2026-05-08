import warnings
import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(
    "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
)
VA_VOTES_PATH = (
    ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
)
EDS_2019_PATH = (
    ROOT
    / "data"
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)
EDS_MIN_PATH = (
    ROOT
    / "data"
    / "shapefiles"
    / "derived"
    / "v0_10_topological_minority_2026_eds.gpkg"
)
EDS_MAJ_PATH = (
    ROOT
    / "data"
    / "shapefiles"
    / "derived"
    / "v0_10_topological_majority_2026_eds.gpkg"
)


def calculate_idv(eds_path, map_name, va_df):
    print(f"\nAnalyzing {map_name} Map...")
    eds = gpd.read_file(eds_path).to_crs(3401)
    name_col = (
        [c for c in eds.columns if "name" in c.lower()][0]
        if [c for c in eds.columns if "name" in c.lower()]
        else eds.columns[0]
    )
    eds = eds[[name_col, "geometry"]].rename(columns={name_col: "ed_name"})

    # Spatial join VA to EDs
    joined = gpd.sjoin(va_df, eds, how="inner", predicate="within")

    results = []
    for district, group in joined.groupby("ed_name"):
        # Filter out tiny slivers or empty VAs
        valid_vas = group[group["total_votes"] > 10].copy()
        if len(valid_vas) < 5:
            continue

        p95 = valid_vas["density_km2"].quantile(0.95)
        p05 = valid_vas["density_km2"].quantile(0.05)

        # Prevent division by zero
        p05 = max(p05, 0.01)

        idv = p95 / p05
        results.append(
            {"district": district, "p95_density": p95, "p05_density": p05, "idv": idv}
        )

    df = pd.DataFrame(results).sort_values("idv", ascending=False)

    print(f"--- Top 5 Highest IDV Districts (The 'Stealth Drains') ---")
    for _, row in df.head(5).iterrows():
        print(f"District: {row['district'].upper()}")
        print(f"  -> Top 5% Urban Density: {row['p95_density']:,.0f} voters/km²")
        print(f"  -> Bottom 5% Rural Density: {row['p05_density']:,.0f} voters/km²")
        print(f"  => Internal Density Variance (IDV): {row['idv']:,.1f}x difference")
        print()


if __name__ == "__main__":
    print("Loading Voting Area base geometries...")
    va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
    va["total_votes"] = va["va_ucp"].fillna(0) + va["va_ndp"].fillna(0)
    va["area_km2"] = va.geometry.area / 1e6
    va["density_km2"] = va["total_votes"] / va["area_km2"]

    # Use centroid for cleaner spatial joins to districts
    va_centroids = va.copy()
    va_centroids["geometry"] = va_centroids.geometry.centroid

    calculate_idv(EDS_2019_PATH, "2019 Baseline", va_centroids)
    calculate_idv(EDS_MAJ_PATH, "2026 Majority", va_centroids)
    calculate_idv(EDS_MIN_PATH, "2026 Minority", va_centroids)
