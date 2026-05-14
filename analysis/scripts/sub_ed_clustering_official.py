#!/usr/bin/env python
"""
Sub-ED Clustering Analysis (Implementation)
Calculates spatial clustering of the hybrid (fractured) districts in the official map.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
import geopandas as gpd
import numpy as np
from pathlib import Path
from shapely.geometry import Point

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
OFFICIAL_MINORITY = DATA_DIR / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"

def main():
    raise NotImplementedError(
        "STUB — DO NOT RUN. This script classifies 'hybrid' (city-rural fractured) "
        "districts using Polsby-Popper < 0.25 as a proxy. That proxy is wrong: "
        "a long thin rural ED may score PP < 0.25 without being a city-rural hybrid; "
        "a compact hybrid ED may score PP > 0.25. The proxy conflates compactness with "
        "hybrid status. Real hybrid classification requires matching EDs against the "
        "commission's narrative classification or a spatial overlay with municipal "
        "boundaries. The clustering and flagging output from this script is based on "
        "a methodologically unjustified proxy and must not be cited."
    )
    if not OFFICIAL_MINORITY.exists():
        print(f"ERROR: Official shapefile not found at {OFFICIAL_MINORITY}")
        return
        
    print(f"Loading official minority boundaries from {OFFICIAL_MINORITY.name}...")
    gdf = gpd.read_file(OFFICIAL_MINORITY)
    
    # Identify "hybrid" fractured districts. For this implementation, we look for
    # districts that are highly non-compact (a proxy for fractured hybrids).
    gdf['polsby_popper'] = (4 * np.pi * gdf.geometry.area) / (gdf.geometry.length ** 2)
    hybrids = gdf[gdf['polsby_popper'] < 0.25] # Bottom tier compactness
    
    print(f"Identified {len(hybrids)} structurally fractured 'hybrid' EDs.")
    
    if len(hybrids) < 2:
        print("Not enough hybrids to compute clustering.")
        return
        
    # Compute pairwise centroid distances
    centroids = hybrids.geometry.centroid.tolist()
    names = hybrids['EDName2025'].tolist()
    
    clustered_pairs = 0
    total_pairs = 0
    threshold_m = 30000 # 30km clustering threshold for urban/suburban rings
    
    for i in range(len(centroids)):
        for j in range(i + 1, len(centroids)):
            total_pairs += 1
            dist = centroids[i].distance(centroids[j])
            if dist < threshold_m:
                clustered_pairs += 1
                
    clustering_score = clustered_pairs / total_pairs
    print(f"Spatial Clustering Score: {clustering_score:.2%} of pairs are within {threshold_m/1000}km of each other.")
    if clustering_score > 0.5:
        print("FLAG: Hybrid districts are highly concentrated regionally (weaponized clustering).")
    else:
        print("Hybrid districts are dispersed naturally across the province.")

if __name__ == "__main__":
    main()
