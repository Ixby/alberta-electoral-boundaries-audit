import warnings
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from pathlib import Path

warnings.filterwarnings('ignore')

ROOT = Path("C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit")
EDS_2019_PATH = ROOT / "data" / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
EDS_MIN_PATH = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_minority_2026_eds.gpkg"
OUT_PATH = ROOT / "scratch" / "crosswalk_proof.png"

def render_proof():
    print("Loading geographic data...")
    eds_2019 = gpd.read_file(EDS_2019_PATH).to_crs(3401)
    name_col_2019 = [c for c in eds_2019.columns if 'name' in c.lower()][0] if [c for c in eds_2019.columns if 'name' in c.lower()] else eds_2019.columns[0]
    eds_2019 = eds_2019[[name_col_2019, 'geometry']].rename(columns={name_col_2019: 'name_2019'})
    eds_2019['name_lower'] = eds_2019['name_2019'].str.lower().str.strip()
    
    eds_2026 = gpd.read_file(EDS_MIN_PATH).to_crs(3401)
    name_col_2026 = [c for c in eds_2026.columns if 'name' in c.lower()][0]
    eds_2026 = eds_2026[[name_col_2026, 'geometry']].rename(columns={name_col_2026: 'name_2026'})
    eds_2026['name_lower'] = eds_2026['name_2026'].str.lower().str.strip()

    # Create the figure - Light Mode
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 10))
    fig.patch.set_facecolor('white')
    fig.suptitle('The Anatomy of a Gerrymander: Cracking, Draining, and Packing', fontsize=28, color='black', y=1.05, weight='bold')

    for ax in [ax1, ax2, ax3]:
        ax.set_facecolor('white')
        ax.axis('off')

    # ---------------------------------------------------------
    # PANEL 1: CRACKING
    # ---------------------------------------------------------
    ax1.set_title("1. CRACKING", fontsize=22, color='#b30000', pad=20, weight='bold')
    
    # Base 2019 district
    cracked_2019 = eds_2019[eds_2019['name_lower'] == 'strathcona-sherwood park']
    cracked_2019.plot(ax=ax1, color='#ffcccc', edgecolor='red', linewidth=2)
    
    # Intersecting 2026 districts
    intersecting_2026_names = ['sherwood park-strathcona', 'stony plain-drayton valley', 'edmonton-gold bar']
    intersect_2026 = eds_2026[eds_2026['name_lower'].isin(intersecting_2026_names)]
    
    # Clip 2026 geometries to the 2019 boundary for clean visualization
    cracked_clip = gpd.clip(intersect_2026, cracked_2019)
    cracked_clip.plot(ax=ax1, facecolor='none', edgecolor='black', linewidth=4, linestyle='--')
    
    # Legend & Annotations
    ax1.text(0.5, -0.15, "The 2019 'Strathcona-Sherwood Park' district\nis shattered by three new 2026 boundaries,\ndiluting its voting power.", 
             ha='center', va='center', transform=ax1.transAxes, color='black', fontsize=16)
    
    red_patch = mpatches.Patch(color='#ffcccc', ec='red', label='Original 2019 District')
    dash_line = mlines.Line2D([], [], color='black', linestyle='--', linewidth=3, label='New 2026 District Borders')
    ax1.legend(handles=[red_patch, dash_line], loc='lower right', fontsize=12)

    # ---------------------------------------------------------
    # PANEL 2: DRAINING 
    # ---------------------------------------------------------
    ax2.set_title("2. DRAINING (Hub-and-Spoke)", fontsize=22, color='#005a9c', pad=20, weight='bold')
    
    # Base 2019 district
    drain_2019 = eds_2019[eds_2019['name_lower'] == 'edmonton-south west']
    drain_2019.plot(ax=ax2, color='#cce5ff', edgecolor='#005a9c', linewidth=2)
    
    # The massive 2026 district swallowing it
    swallower_2026 = eds_2026[eds_2026['name_lower'] == 'stony plain-drayton valley']
    
    # Clip the massive 2026 boundary to the 2019 urban district
    drain_clip = gpd.clip(swallower_2026, drain_2019)
    drain_clip.plot(ax=ax2, color='#ffcc99', edgecolor='orange', linewidth=4, hatch='///')
    swallower_outline = gpd.clip(swallower_2026, drain_2019.buffer(5000)) # show a bit outside
    swallower_outline.plot(ax=ax2, facecolor='none', edgecolor='orange', linewidth=3, linestyle='-.')

    ax2.text(0.5, -0.15, "A dense slice of 'Edmonton-South West' (2019)\nis stripped out of the city and swallowed by the\nmassive rural 'Stony Plain-Drayton Valley' (2026).", 
             ha='center', va='center', transform=ax2.transAxes, color='black', fontsize=16)
             
    blue_patch = mpatches.Patch(color='#cce5ff', ec='#005a9c', label='2019 Urban District')
    orange_patch = mpatches.Patch(color='#ffcc99', ec='orange', hatch='///', label='Drained Slice (Attached to Rural)')
    ax2.legend(handles=[blue_patch, orange_patch], loc='lower right', fontsize=12)

    # ---------------------------------------------------------
    # PANEL 3: PACKING
    # ---------------------------------------------------------
    ax3.set_title("3. PACKING (The Vote Sink)", fontsize=22, color='#006400', pad=20, weight='bold')
    
    # Base 2026 District
    sink_2026 = eds_2026[eds_2026['name_lower'] == 'stony plain-drayton valley']
    sink_2026.plot(ax=ax3, facecolor='none', edgecolor='black', linewidth=5)
    
    # The 3 donor 2019 districts
    donor_names = ['drayton valley-devon', 'edmonton-south west', 'strathcona-sherwood park']
    donors_2019 = eds_2019[eds_2019['name_lower'].isin(donor_names)]
    
    # Clip donors to the 2026 sink
    sink_clip = gpd.clip(donors_2019, sink_2026)
    
    colors = ['#ffcccc', '#cce5ff', '#e5ccff']
    labels = ['From: Drayton Valley (Rural Base)', 'From: Edmonton SW (Drained)', 'From: Strathcona (Cracked)']
    patches = []
    
    for idx, (i, row) in enumerate(sink_clip.iterrows()):
        gpd.GeoSeries([row.geometry]).plot(ax=ax3, color=colors[idx % len(colors)], edgecolor='gray', linewidth=1)
        patches.append(mpatches.Patch(color=colors[idx % len(colors)], label=labels[idx % len(labels)]))

    ax3.text(0.5, -0.15, "The new 'Stony Plain-Drayton Valley' (65% UCP)\nVote Sink is artificially engineered by combining the\ncracked and drained pieces from Panels 1 & 2.", 
             ha='center', va='center', transform=ax3.transAxes, color='black', fontsize=16)

    ax3.legend(handles=patches, loc='lower right', fontsize=12, title="2019 Donor Districts")

    # Create a nice layout
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25) # Leave room for the text captions
    
    print(f"Saving high-resolution proof to {OUT_PATH}")
    plt.savefig(OUT_PATH, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == "__main__":
    render_proof()
