import os
import sys
import math
from pathlib import Path
import geopandas as gpd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from tests.test_neighbour_drain import compute_neighbour_drain
from tests.test_compactness_weighted import calculate_compactness_weighted_eg
from tests.test_chen_rodden_decomposition import decompose_bias

# Import the single source of truth for test configurations
from analysis.scripts.test_config import MAP_PLANS, DATA_DIR

def build_adjacency_matrix(gdf, id_col):
    adjacency = {}
    for index, row in gdf.iterrows():
        neighbors = gdf[gdf.geometry.touches(row.geometry)][id_col].tolist()
        adjacency[row[id_col]] = neighbors
    return adjacency

def aggregate_votes(va, eds, id_col):
    # Ensure matching CRS
    if eds.crs != va.crs:
        eds = eds.to_crs(va.crs)
        
    joined = gpd.sjoin(
        va[["va_ucp", "va_ndp", "geometry"]],
        eds[[id_col, "geometry"]],
        how="left",
        predicate="within",
    )
    agg = (
        joined.groupby(id_col)
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    return agg

def evaluate_map(plan_name, path, id_col, va):
    print(f"\n{'='*50}\nEVALUATING: {plan_name}\n{'='*50}")
    
    if not path.exists():
        print(f"File not found: {path}. Skipping.")
        return

    eds = gpd.read_file(path)
    print(f"Loaded {len(eds)} districts from {path.name}.")

    # 1. Vote shares
    print("Aggregating vote shares...")
    agg_votes = aggregate_votes(va, eds, id_col)
    
    ed_data = {}
    ed_results_list = []
    for _, row in agg_votes.iterrows():
        ed_name = row[id_col]
        ndp = row["ndp"]
        ucp = row["ucp"]
        ed_data[ed_name] = {"ndp": ndp, "ucp": ucp}
        ed_results_list.append({"ed": ed_name, "ndp": ndp, "ucp": ucp})

    # 2. Adjacency for neighbour drain
    print("Building adjacency matrix...")
    adj_matrix = build_adjacency_matrix(eds, id_col)
    
    print("\n--- Test 6.1: Neighbour-Drain Adjacency ---")
    signals = compute_neighbour_drain(ed_data, adj_matrix, surplus_threshold=0.15, margin_threshold=0.05)
    print(f"Detected {len(signals)} packed-to-cracked neighbour couples.")
    for x, y in signals[:5]:
        print(f"  {x} (packed) -> {y} (cracked)")

    # 3. Compactness weighted EG
    print("\n--- Test 6.4: Compactness-Weighted Efficiency Gap ---")
    ed_shapes = {row[id_col]: row.geometry for _, row in eds.iterrows()}
    cw_eg = calculate_compactness_weighted_eg(ed_results_list, ed_shapes)
    print(f"Compactness-weighted EG: {cw_eg:+.4f}")
    
    # Calculate actual Efficiency Gap (standard unweighted)
    total_votes = sum([ed["ndp"] + ed["ucp"] for ed in ed_results_list])
    wasted_ndp, wasted_ucp = 0, 0
    for ed in ed_results_list:
        total = ed["ndp"] + ed["ucp"]
        if total == 0: continue
        if ed["ndp"] > ed["ucp"]:
            wasted_ndp += ed["ndp"] - (total / 2)
            wasted_ucp += ed["ucp"]
        else:
            wasted_ucp += ed["ucp"] - (total / 2)
            wasted_ndp += ed["ndp"]
    
    actual_eg = (wasted_ucp - wasted_ndp) / total_votes if total_votes > 0 else 0
    
    print("\n--- Test 6.5: Absolute-Level Decomposition ---")
    # Using known constraint bound baseline (approx -0.0210)
    decomp = decompose_bias(eg_actual=actual_eg, eg_neutral_median=-0.0210)
    print(f"Geography Component: {decomp['geography']:+.4f}")
    print(f"Drawing Component (Gerrymander): {decomp['drawing']:+.4f}")

def main():
    print("Loading official VA voting data...")
    va_path = DATA_DIR / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
    va = gpd.read_file(va_path)
    
    # Iterate dynamically through all configured plans from the source of truth
    for plan in MAP_PLANS:
        evaluate_map(plan["name"], plan["path"], plan["id_col"], va)

if __name__ == "__main__":
    main()
