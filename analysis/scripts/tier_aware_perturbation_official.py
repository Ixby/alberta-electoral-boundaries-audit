#!/usr/bin/env python
"""
Tier-Aware DPG-Perturbation CI (Implementation)
Applies Tier-based margin of errors to the official v11 shapefiles.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
import geopandas as gpd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
OFFICIAL_MINORITY = DATA_DIR / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"

def main():
    if not OFFICIAL_MINORITY.exists():
        print(f"ERROR: Official shapefile not found at {OFFICIAL_MINORITY}")
        return
        
    print(f"Loading official minority boundaries from {OFFICIAL_MINORITY.name}...")
    gdf = gpd.read_file(OFFICIAL_MINORITY)
    
    # In a full run, we would intersect these lines with the 2019 enacted map
    # to classify segments as Tier A (0m uncertainty) vs Tier C (300m).
    # Since we lack the explicit topological intersection cache here, we assign
    # conservative estimations for the boundaries.
    
    # Mocking the tier classification based on area heuristics for now
    total_bias_shifts = []
    rng = np.random.default_rng(42)
    
    for _ in range(500):
        shift = 0
        for idx, row in gdf.iterrows():
            # If area is huge, it's likely rural (often Tier A / intact from 2019)
            if row.geometry.area > 500000000:
                shift += rng.normal(0, 0) # Tier A
            else:
                shift += rng.normal(0, 300) # Tier C (urban fractured)
        total_bias_shifts.append(shift)
        
    p05, p95 = np.percentile(total_bias_shifts, [5, 95])
    print(f"Tier-Aware Perturbation complete.")
    print(f"90% CI for boundary uncertainty shift: [{p05:+.2f}, {p95:+.2f}] (synthetic proxy)")

if __name__ == "__main__":
    main()
