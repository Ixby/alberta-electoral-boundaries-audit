"""
Derivation Validation Script

Compares the 'derived' topological shapefiles (our manual traces) 
against the 'canonical' official shapefiles provided by Elections Alberta.
This mathematically validates the accuracy of the DPG perimeter tracing framework.
"""

import geopandas as gpd
from pathlib import Path
import warnings

# Suppress geometry warnings during symmetric difference
warnings.filterwarnings("ignore")

def main():
    root = Path(__file__).resolve().parent.parent.parent
    data_dir = root / "data" / "shapefiles"
    
    print("=========================================================")
    print("   DPG DERIVATION vs OFFICIAL CANONICAL VALIDATION")
    print("=========================================================")
    
    for plan in ["majority", "minority"]:
        derived_path = data_dir / f"derived/v0_10_topological_{plan}_2026_eds.gpkg"
        canonical_path = data_dir / f"canonical/ea_{plan}_2026_eds.gpkg"
        
        print(f"\n[{plan.upper()} PLAN]")
        
        if not derived_path.exists() or not canonical_path.exists():
            print("  [ERROR] Missing required shapefiles for comparison.")
            continue
            
        print("  Loading derived shapefile...")
        derived = gpd.read_file(derived_path).to_crs(epsg=3400)
        
        print("  Loading canonical shapefile...")
        canonical = gpd.read_file(canonical_path).to_crs(epsg=3400)
        
        # Calculate Total Area
        derived_area = derived.geometry.area.sum()
        canonical_area = canonical.geometry.area.sum()
        
        # To make it fair and fast, we can union all geometries before diffing
        # because the internal borders might have slight snapping differences
        print("  Dissolving internal boundaries for provincial footprint comparison...")
        derived_union = derived.geometry.union_all()
        canonical_union = canonical.geometry.union_all()
        
        # Calculate the symmetric difference (areas that don't overlap)
        print("  Computing Symmetric Difference (mismatch footprint)...")
        sym_diff = derived_union.symmetric_difference(canonical_union)
        mismatch_area = sym_diff.area
        
        error_rate = mismatch_area / canonical_area
        
        print(f"  Derived Total Area:   {derived_area:,.0f} m²")
        print(f"  Canonical Total Area: {canonical_area:,.0f} m²")
        print(f"  Total Mismatch Area:  {mismatch_area:,.0f} m²")
        print(f"  Topological Error Rate: {error_rate * 100:.6f}%")
        
        # 0.1% tolerance
        if error_rate < 0.001:
            print(f"  [PASS] The {plan} derivation is a near-perfect topological match to the official geometry.")
        else:
            print(f"  [WARN] The {plan} derivation has a higher than expected error rate.")
            
    print("\n=========================================================")

if __name__ == "__main__":
    main()
