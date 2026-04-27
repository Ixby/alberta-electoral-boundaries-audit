"""
build_airdrie_visual_teardown.py
================================
Visual teardown of the Airdrie 4-way split to counter the "highway anchoring" defense.
Plots the 2026 Majority map vs the 2026 Minority map over the Airdrie municipal envelope and OSM highways.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "shapefiles"
OUTPUT_DIR = ROOT / "analysis" / "reports"

def load_data():
    print("Loading datasets...")
    # Load Airdrie CSD
    csd = gpd.read_file(DATA_DIR / "reference" / "alberta_2021_csds.gpkg")
    airdrie = csd[csd.CSDNAME == "Airdrie"].to_crs(epsg=3401)
    
    # Bounding box with a 5km buffer
    bbox = airdrie.buffer(5000).total_bounds
    
    # Load highways and clip to bbox
    highways = gpd.read_file(ROOT / "data" / "osm" / "alberta_osm_highways.gpkg").to_crs(epsg=3401)
    # The GPKG already only contains motorway/trunk/primary/secondary from the OSM query
    major_hwys = highways.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    
    # Load majority and minority maps
    maj_map = gpd.read_file(DATA_DIR / "derived" / "v0_9_topological_majority_2026_eds.gpkg").to_crs(epsg=3401)
    maj_map = maj_map.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    min_map = gpd.read_file(DATA_DIR / "derived" / "v0_9_topological_minority_2026_eds.gpkg").to_crs(epsg=3401)
    min_map = min_map.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    
    return airdrie, major_hwys, maj_map, min_map, bbox

def plot_teardown(airdrie, major_hwys, maj_map, min_map, bbox):
    print("Generating visualization...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), dpi=150)
    plt.suptitle("Airdrie Partition: Majority (2 EDs) vs Minority (4 EDs)", fontsize=18, fontweight='bold', y=0.98)
    
    for idx, (ax, ed_map, title) in enumerate(zip(axes, [maj_map, min_map], ["Majority Recommendation (2-way split)", "Minority Recommendation (4-way split)"])):
        ax.set_title(title, fontsize=14, pad=10)
        
        # 1. Plot Airdrie CSD filled (light yellow/gray)
        airdrie.plot(ax=ax, color="#FFFACD", edgecolor="black", linewidth=2, linestyle="--", alpha=0.6, zorder=1)
        
        # 2. Plot Highways
        major_hwys.plot(ax=ax, color="darkred", linewidth=1.5, alpha=0.8, zorder=2)
        
        # 3. Plot ED boundaries (thick lines)
        ed_map.boundary.plot(ax=ax, color="#2c3e50", linewidth=3, zorder=3)
        
        # 4. Color the EDs lightly so we can see the fracture
        cmap = plt.get_cmap("Pastel1")
        for i, (_, row) in enumerate(ed_map.iterrows()):
            color = cmap(i % 9)
            gpd.GeoSeries([row.geometry]).plot(ax=ax, color=color, alpha=0.3, zorder=0)
            
            # Label ED
            # We intersect with the buffered Airdrie polygon to ensure the label is placed near Airdrie
            intersection = row.geometry.intersection(airdrie.unary_union.buffer(2000))
            if not intersection.is_empty:
                # Use a representative point to guarantee it's inside the polygon
                centroid = intersection.representative_point()
                ax.text(centroid.x, centroid.y, row['name_2026'].replace('-', '\n'), 
                        fontsize=9, fontweight='bold', ha='center', va='center',
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2), zorder=4)

        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])
        ax.axis("off")
        
    # Custom Legend
    legend_elements = [
        Patch(facecolor='#FFFACD', edgecolor='black', linestyle='--', label='Airdrie City Limits'),
        Line2D([0], [0], color='#2c3e50', lw=3, label='Electoral Division Boundary'),
        Line2D([0], [0], color='darkred', lw=1.5, label='Major Highways (e.g. QEII)')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=12, bbox_to_anchor=(0.5, 0.02))
    
    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    out_path = OUTPUT_DIR / "airdrie_four_way_split_teardown.png"
    plt.savefig(out_path)
    print(f"Saved visualization to {out_path}")

if __name__ == "__main__":
    airdrie, major_hwys, maj_map, min_map, bbox = load_data()
    plot_teardown(airdrie, major_hwys, maj_map, min_map, bbox)
