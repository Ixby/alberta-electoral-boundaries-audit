# Version: v0.2
"""
november_tripwires.py
====================================
Pre-registered automated checks for the November 91-seat map.
This script measures the exact Modus Operandi (MO) observed in the 
2026 minority commission map to detect whether the Lunty committee 
has deployed the same 'Surgical Fortification' tactics.

Tripwires:
1. Mid-Sized City Integrity (The Drain Pattern)
"""

import os
import math
import numpy as np
import pandas as pd
import geopandas as gpd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')

def run_tripwires(eds_gdf_path, cities_gdf_path=None):
    print("=" * 60)
    print("  NOVEMBER 91-SEAT MAP TRIPWIRES")
    print("=" * 60)
    
    eds = gpd.read_file(eds_gdf_path)
    # Ensure a projected CRS for accurate area/perimeter calculations
    if eds.crs is None or eds.crs.is_geographic:
        print("Warning: Map is not projected. Reprojecting to Alberta 10-TM for area calculations.")
        eds = eds.to_crs(epsg=3401) # Alberta 10-TM
    elif eds.crs.to_epsg() != 3401:
        raise ValueError(f"Expected shapefile to be in Alberta 10-TM (EPSG:3401), but found EPSG:{eds.crs.to_epsg()}. November map must use authoritative CRS.")
    
    print(f"Loaded {len(eds)} Electoral Districts.")

    # ---------------------------------------------------------
    # TRIPWIRE 1: Mid-Sized City Integrity (The Drain Pattern)
    # ---------------------------------------------------------
    print("\n[Tripwire 1: The Drain Pattern (City Splitting)]")
    
    if cities_gdf_path and os.path.exists(cities_gdf_path):
        cities = gpd.read_file(cities_gdf_path)
        cities = cities.to_crs(eds.crs)
        
        # We only care about mid-sized target cities (e.g. Red Deer, Lethbridge, Airdrie, St. Albert)
        target_cities = ['Red Deer', 'Lethbridge', 'Airdrie', 'St. Albert', 'Medicine Hat']
        # Use substring matching to avoid failing on "City of Red Deer" or "Red Deer (CY)"
        cities = cities[cities['name'].str.contains('|'.join(target_cities), case=False, na=False)]
        
        # 2023 Population estimates for dynamic calculation
        city_populations = {
            'Red Deer': 100844,
            'Lethbridge': 101482,
            'Airdrie': 80649,
            'St. Albert': 68232,
            'Medicine Hat': 63260
        }
        
        for _, city in cities.iterrows():
            city_geom = city.geometry
            city_name = city['name']
            
            # Find all EDs that intersect the city
            intersections = eds[eds.geometry.intersects(city_geom)].copy()
            
            # Filter out tiny slivers (e.g. boundary floating point overlaps)
            # Only count if the ED contains > 2% of the city's area
            intersections['overlap_area'] = intersections.geometry.intersection(city_geom).area
            intersections['overlap_pct'] = intersections['overlap_area'] / city_geom.area
            valid_splits = intersections[intersections['overlap_pct'] > 0.02]
            
            num_splits = len(valid_splits)
            
            # Mathematical baseline: Population dictates # of seats. 
            # Alberta's 91-seat average electoral quotient is ~51,648.
            clean_name = next((t for t in target_cities if t.lower() in city_name.lower()), city_name)
            pop = city_populations.get(clean_name, 50000)
            expected_seats = math.ceil(pop / 51648.0)
            
            if num_splits > expected_seats:
                print(f"  [RED ALERT] {city_name} is split into {num_splits} districts (Expected: {expected_seats}).")
                for _, ed_row in valid_splits.iterrows():
                    ed_name = ed_row.get('name_2026', ed_row.get('ed_name', 'Unknown'))
                    print(f"    - {ed_name} captures {ed_row['overlap_pct']*100:.1f}% of the city.")
            else:
                print(f"  [PASS] {city_name} is kept intact ({num_splits} districts).")
    else:
        print("  (Skipping Mid-Sized City Integrity: No cities reference file provided.)")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="November 91-Seat Map Tripwire Checks")
    parser.add_argument('--shapefile', type=str, required=True, help="Path to the November 91-seat GPKG or Shapefile")
    parser.add_argument('--cities', type=str, default=os.path.join(ROOT, 'data', 'shapefiles', 'reference', 'alberta_2021_csds.gpkg'), help="Path to reference cities GPKG")
    args = parser.parse_args()
    
    if not os.path.exists(args.shapefile):
        print(f"Error: Shapefile not found at {args.shapefile}")
    else:
        run_tripwires(eds_gdf_path=args.shapefile, cities_gdf_path=args.cities)
