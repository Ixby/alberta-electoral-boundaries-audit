"""
Ecological Inference Substrate Builder (Spatial Crosswalk)

This script performs Area-Weighted Interpolation to force Statistics Canada 
Dissemination Area (DA) demographic data onto Elections Alberta Voting Area (VA) 
polygons by calculating the fractional overlap of their geometries.

Output is a CSV containing both demographic percentages and voting data per VA, 
which can be directly fed into the Duncan & Davis EI Bounds test.
"""

import warnings
from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np

# Suppress geometry warnings during overlay
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    data_dir = root_dir / "data"
    raw_csv = data_dir / "raw/98-401-X2021024_English_CSV_data.csv"
    
    if not raw_csv.exists():
        print(f"Error: {raw_csv} not found.")
        return

    print("1. Parsing Statistics Canada Demographic Data (this may take a minute)...")
    chunk_iter = pd.read_csv(
        raw_csv, 
        encoding='utf-8', 
        encoding_errors='ignore', 
        chunksize=250000, 
        usecols=['GEO_LEVEL', 'GEO_NAME', 'CHARACTERISTIC_NAME', 'C1_COUNT_TOTAL']
    )
    
    dfs = []
    target_characteristics = [
        'Population, 2021', 
        'Total visible minority population',
        'Total - Indigenous identity for the population in private households'
    ]
    
    for chunk in chunk_iter:
        # Filter strictly for Dissemination Areas in Alberta (starts with 48)
        da_mask = (chunk['GEO_LEVEL'] == 'Dissemination area') & (chunk['GEO_NAME'].astype(str).str.startswith('48'))
        chunk = chunk[da_mask]
        
        char_mask = chunk['CHARACTERISTIC_NAME'].isin(target_characteristics)
        dfs.append(chunk[char_mask])
        
    demo = pd.concat(dfs)
    
    # Pivot to make characteristics into columns
    print("   Pivoting demographic data...")
    pivoted = demo.pivot_table(
        index='GEO_NAME', 
        columns='CHARACTERISTIC_NAME', 
        values='C1_COUNT_TOTAL', 
        aggfunc='first'
    ).reset_index()
    
    # Clean up column names
    pivoted = pivoted.rename(columns={
        'GEO_NAME': 'DAUID',
        'Population, 2021': 'da_pop_total',
        'Total visible minority population': 'da_visible_min',
        'Total - Indigenous identity for the population in private households': 'da_indigenous'
    })
    
    # Convert DAUID to string to ensure safe merging
    pivoted['DAUID'] = pivoted['DAUID'].astype(str)
    
    # Fill NaN with 0 for counts
    for col in ['da_pop_total', 'da_visible_min', 'da_indigenous']:
        if col in pivoted.columns:
            pivoted[col] = pd.to_numeric(pivoted[col], errors='coerce').fillna(0)
        else:
            pivoted[col] = 0

    print("2. Loading spatial geometries...")
    va_path = data_dir / "shapefiles/derived/va_polygons_with_2023_votes.gpkg"
    da_path = data_dir / "shapefiles/reference/alberta_2021_das.gpkg"
    
    va_gdf = gpd.read_file(va_path)
    da_gdf = gpd.read_file(da_path)
    
    # Ensure DAUID is string
    da_gdf['DAUID'] = da_gdf['DAUID'].astype(str)
    
    print("3. Merging demographics onto DA geometries...")
    da_joined = da_gdf.merge(pivoted, on='DAUID', how='left')
    
    # Ensure they share the same CRS (Elections Alberta standard: EPSG:3400)
    print("4. Standardizing projections (EPSG:3400)...")
    va_gdf = va_gdf.to_crs(epsg=3400)
    da_joined = da_joined.to_crs(epsg=3400)
    
    # Pre-calculate original DA area
    da_joined['da_orig_area'] = da_joined.geometry.area
    
    print("5. Performing Area-Weighted Spatial Overlay (Intersection)...")
    intersection = gpd.overlay(va_gdf, da_joined, how='intersection')
    
    # Calculate overlap area and weight
    intersection['intersect_area'] = intersection.geometry.area
    intersection['weight'] = intersection['intersect_area'] / intersection['da_orig_area']
    
    # Clamp weight between 0 and 1 to prevent rounding artifacts
    intersection['weight'] = intersection['weight'].clip(0, 1)
    
    print("6. Apportioning demographic populations from DAs to VAs...")
    intersection['va_pop_total_est'] = intersection['da_pop_total'] * intersection['weight']
    intersection['va_visible_min_est'] = intersection['da_visible_min'] * intersection['weight']
    intersection['va_indigenous_est'] = intersection['da_indigenous'] * intersection['weight']
    
    print("7. Aggregating partial VA pieces back into whole VAs...")
    # The VA unique identifier depends on the column in Elections Alberta file
    # We will use 'VAArea_ID' or fallback to the index if needed.
    va_id_col = 'VAArea_ID' if 'VAArea_ID' in intersection.columns else intersection.columns[0]
    
    # We want to sum the estimated populations, but keep the actual vote counts
    agg_dict = {
        'va_pop_total_est': 'sum',
        'va_visible_min_est': 'sum',
        'va_indigenous_est': 'sum',
    }
    
    # Keep the voting columns (they shouldn't be summed as they are duplicated on every split)
    vote_cols = [c for c in va_gdf.columns if c.lower().startswith('va_')]
    for vc in vote_cols:
        if vc not in agg_dict:
            agg_dict[vc] = 'first'
            
    final_substrate = intersection.groupby(va_id_col).agg(agg_dict).reset_index()
    
    # Calculate percentages for the Duncan & Davis bounds
    final_substrate['pct_visible_min'] = np.where(final_substrate['va_pop_total_est'] > 0, 
                                                  final_substrate['va_visible_min_est'] / final_substrate['va_pop_total_est'], 0)
    final_substrate['pct_indigenous'] = np.where(final_substrate['va_pop_total_est'] > 0, 
                                                 final_substrate['va_indigenous_est'] / final_substrate['va_pop_total_est'], 0)
    
    output_path = data_dir / "outputs/ei_substrate_2023.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    final_substrate.to_csv(output_path, index=False)
    print(f"\n[SUCCESS] Master EI Substrate built and saved to: {output_path}")
    print("This file contains demographic crosswalks + voting totals ready for the Duncan & Davis EI Bounds test.")

if __name__ == "__main__":
    main()
