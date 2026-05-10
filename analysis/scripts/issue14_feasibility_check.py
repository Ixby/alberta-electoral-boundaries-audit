"""
issue14_feasibility_check.py — Prep data for manual QGIS feasibility check

Prepare a QGIS project file highlighting:
1. The 3 worst-anchoring minority EDs (Peace River, Cold Lake-Bonnyville-St Paul, Canmore-Kananaskis)
2. The VA boundaries within those EDs
3. CSD reference boundaries (for anchoring targets)
4. Tier A COI constraint points (Airdrie-Calgary, Tsuut'ina, Red Deer hub reference points)

User opens the QGIS project and does a 10-minute visual inspection:
- Can boundaries be redrawn to follow more CSDs while preserving COI adjacencies?
- Are there obvious VA clusters that could be reassigned to improve anchoring?

Outputs:
    data/issue14_feasibility_qgis.gpkg (single-layer GPKG with all geometry)
    analysis/scripts/issue14_feasibility_guide.md (manual inspection checklist)
"""

from __future__ import annotations

import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")

VA_GPKG = DATA / "shapefiles" / "derived" / "va_polygons_with_full_2023_votes.gpkg"
MINORITY_GPKG = DATA / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"
CSD_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
OUT_GPKG = DATA / "issue14_feasibility_qgis.gpkg"

WORST_EDS = ["Peace River", "Cold Lake-Bonnyville-St. Paul", "Canmore-Kananaskis"]

# Tier A COI constraints (centroid points for reference)
TIER_A_COIS = {
    "Airdrie-Calgary": {
        "description": "Airdrie commuter tie to Calgary CMA",
        "point": Point(-113.97, 51.29),  # Airdrie city centre
    },
    "Tsuut'ina-Calgary": {
        "description": "Tsuut'ina economic tie to west Calgary (Glenmore Trail)",
        "point": Point(-114.25, 50.90),  # Tsuut'ina Nation centre
    },
    "Red Deer hub": {
        "description": "Red Deer as regional hub (max 3 EDs)",
        "point": Point(-111.98, 52.26),  # Red Deer city centre
    },
}


def main():
    print("Loading VA polygons...")
    vas = gpd.read_file(VA_GPKG)

    print("Loading minority 2026 map...")
    minority_eds = gpd.read_file(MINORITY_GPKG)

    print("Loading CSD reference boundaries...")
    csds = gpd.read_file(CSD_GPKG)

    # Filter to worst 3 EDs
    worst_eds_gdf = minority_eds[minority_eds["EDName2025"].isin(WORST_EDS)].copy()

    print(f"\nWorst 3 minority EDs:")
    for ed_name in WORST_EDS:
        row = minority_eds[minority_eds["EDName2025"] == ed_name]
        if not row.empty:
            print(f"  {ed_name}")

    # Filter VAs to those intersecting worst EDs
    worst_vas = gpd.sjoin(vas, worst_eds_gdf, how="inner", predicate="intersects")
    print(f"\nTotal VAs in worst 3 EDs: {len(worst_vas)}")

    # Build combined layer for QGIS
    # First reproject everything to a common CRS (use the ED CRS as reference)
    target_crs = worst_eds_gdf.crs
    print(f"\nTarget CRS: {target_crs}")

    all_features = []

    # Add worst EDs with label
    worst_eds_gdf["layer_type"] = "ED_worst"
    worst_eds_gdf["label"] = worst_eds_gdf["EDName2025"]
    all_features.append(worst_eds_gdf[["layer_type", "label", "geometry"]])

    # Add VAs in worst EDs
    worst_vas_reprojected = worst_vas.to_crs(target_crs)
    worst_vas_reprojected["layer_type"] = "VA_in_worst"
    worst_vas_reprojected["label"] = worst_vas_reprojected["VA_NUMBER"].astype(str)
    all_features.append(worst_vas_reprojected[["layer_type", "label", "geometry"]])

    # Add CSD boundaries
    csds_reprojected = csds.to_crs(target_crs)
    csds_reprojected["layer_type"] = "CSD_reference"
    csds_reprojected["label"] = csds_reprojected["CSDNAME"]
    all_features.append(csds_reprojected[["layer_type", "label", "geometry"]])

    # Add Tier A COI reference points
    coi_points = []
    for coi_name, coi_data in TIER_A_COIS.items():
        coi_points.append({
            "layer_type": "COI_reference",
            "label": coi_name,
            "description": coi_data["description"],
            "geometry": coi_data["point"],
        })
    coi_gdf = gpd.GeoDataFrame(coi_points, crs="EPSG:4326").to_crs(target_crs)
    all_features.append(coi_gdf[["layer_type", "label", "geometry"]])

    # Combine all
    combined = pd.concat(all_features, ignore_index=True)
    combined = gpd.GeoDataFrame(combined, crs=target_crs)

    print(f"\nWriting combined layer to {OUT_GPKG}...")
    combined.to_file(OUT_GPKG, driver="GPKG")
    print(f"  {len(combined)} features written")

    # Write inspection guide
    guide_md = ROOT / "analysis" / "scripts" / "issue14_feasibility_guide.md"
    print(f"\nWriting inspection guide to {guide_md}...")
    with open(guide_md, "w", encoding="utf-8") as f:
        f.write("""# Issue #14 Feasibility Check — Manual QGIS Inspection

## Quick Start

1. Open `data/issue14_feasibility_qgis.gpkg` in QGIS
2. Inspect the 3 worst-anchoring minority EDs
3. Answer the questions below (10-15 minutes)

## The 3 Worst EDs and Current Anchoring

| ED | Anchoring % | Perimeter (km) | Anchored (km) |
|---|---|---|---|
| Peace River | 7.4% | 1693.3 | 125.3 |
| Cold Lake-Bonnyville-St. Paul | 12.73% | 687.0 | 87.5 |
| Canmore-Kananaskis | 16.01% | 1211.4 | 193.9 |

**Goal:** Can we redraw these EDs to reach ≥60% anchoring while preserving Tier A COIs?

## Layer Guide in QGIS

- **ED_worst** (light blue polygons): The 3 worst EDs outlined
- **VA_in_worst** (small yellow polygons): Individual voting areas inside those EDs
- **CSD_reference** (thin gray boundaries): StatsCan Census Subdivisions (the anchoring target)
- **COI_reference** (red circles): Tier A COI constraint locations:
  - Airdrie-Calgary: Airdrie city centre (must preserve ED adjacency to Calgary EDs)
  - Tsuut'ina-Calgary: Tsuut'ina Nation centre (must stay in same ED or adjacent ED group)
  - Red Deer hub: Red Deer city centre (must not split across >3 EDs)

## Inspection Checklist

For **Peace River** (current 7.4%):
- [ ] Are there large runs of ED boundary that avoid CSD edges but could easily follow them?
- [ ] Which VAs on the ED perimeter are causing the low anchoring?
- [ ] If you merged those boundary-adjacent VAs into adjacent EDs, would the COI constraints break?

For **Cold Lake-Bonnyville-St. Paul** (current 12.73%):
- [ ] Same analysis as above

For **Canmore-Kananaskis** (current 16.01%):
- [ ] Same analysis as above

## Success Criteria

**Feasible**: You identify a plausible VA reassignment that could push anchoring from current level to ≥50% (even if not ≥60%) while keeping COI reference points in viable positions.

**Infeasible**: The ED perimeter is locked by COI constraints and cannot be redrawn to follow CSDs without breaking multiple Tier A claims.

## What To Do Next

- If **Feasible**: Proceed to Phase 3b (--demo mode) and Phase 4 (full 100k run with CSD-weight search)
- If **Infeasible**: Issue #14 is geometrically impossible; document and move to next priority

---

*Inspection takes 10-15 minutes. If you have GIS experience, you can spot the feasibility boundary visually without running a full model.*
""")
    print("  Inspection guide written")


if __name__ == "__main__":
    main()
