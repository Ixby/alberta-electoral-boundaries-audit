import warnings
import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

warnings.filterwarnings('ignore')

ROOT = Path("C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit")
VA_VOTES_PATH = ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
EDS_2019_PATH = ROOT / "data" / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
EDS_MIN_PATH = ROOT / "data" / "shapefiles" / "derived" / "v0_10_topological_minority_2026_eds.gpkg"
EDS_MAJ_PATH = ROOT / "data" / "shapefiles" / "derived" / "v0_10_topological_majority_2026_eds.gpkg"
PROOFS_DIR = ROOT / "scratch" / "xray_proofs"

os.makedirs(PROOFS_DIR, exist_ok=True)

NDP_COLOR = '#f37021'
UCP_COLOR = '#003f72'

def load_data():
    eds_2019 = gpd.read_file(EDS_2019_PATH).to_crs(3401)
    name_col = [c for c in eds_2019.columns if 'name' in c.lower()][0] if [c for c in eds_2019.columns if 'name' in c.lower()] else eds_2019.columns[0]
    eds_2019 = eds_2019[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_2019['name'] = eds_2019['name'].str.upper().str.strip()

    eds_min = gpd.read_file(EDS_MIN_PATH).to_crs(3401)
    name_col = [c for c in eds_min.columns if 'name' in c.lower()][0]
    eds_min = eds_min[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_min['name'] = eds_min['name'].str.upper().str.strip()

    eds_maj = gpd.read_file(EDS_MAJ_PATH).to_crs(3401)
    name_col = [c for c in eds_maj.columns if 'name' in c.lower()][0]
    eds_maj = eds_maj[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_maj['name'] = eds_maj['name'].str.upper().str.strip()
    
    va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
    va_pts = gpd.GeoDataFrame(
        {"va_ucp": va["va_ucp"].fillna(0), "va_ndp": va["va_ndp"].fillna(0)},
        geometry=va.geometry.centroid,
        crs=3401
    )
    va_pts['total'] = va_pts['va_ucp'] + va_pts['va_ndp']
    va_pts = va_pts[va_pts['total'] > 0]
    # Assign winning color to the point
    va_pts['color'] = va_pts.apply(lambda r: NDP_COLOR if r['va_ndp'] > r['va_ucp'] else UCP_COLOR, axis=1)
    
    return eds_2019, eds_min, eds_maj, va_pts

def get_events(eds_2019, eds_2026, va_pts, map_label):
    crosswalk = gpd.overlay(eds_2019.rename(columns={'name':'name_2019'}), eds_2026.rename(columns={'name':'name_2026'}), how='intersection')
    crosswalk['area_m2'] = crosswalk.geometry.area
    crosswalk = crosswalk[crosswalk['area_m2'] > 100000].copy()
    crosswalk['slice_id'] = range(len(crosswalk))
    
    joined = gpd.sjoin(va_pts, crosswalk[['slice_id', 'geometry']], how='inner', predicate='within')
    slice_votes = joined.groupby('slice_id').agg(ucp_votes=('va_ucp', 'sum'), ndp_votes=('va_ndp', 'sum')).reset_index()
    crosswalk = crosswalk.merge(slice_votes, on='slice_id', how='left').fillna(0)
    crosswalk['total_votes'] = crosswalk['ucp_votes'] + crosswalk['ndp_votes']
    crosswalk = crosswalk[crosswalk['total_votes'] > 2000].copy()
    
    events = []
    
    # 1. Cracking
    splits = crosswalk.groupby('name_2019').size()
    cracked = splits[splits >= 3].index
    for district in cracked:
        slices = crosswalk[crosswalk['name_2019'] == district]
        if slices['total_votes'].sum() >= 10000:
            events.append({
                'type': 'Cracking', 'map_label': map_label, 'target_2019': district,
                'pieces': slices['name_2026'].tolist()
            })
            
    # 2. Packing
    districts_2026 = crosswalk.groupby('name_2026').agg(
        total_votes=('total_votes', 'sum'), ucp=('ucp_votes', 'sum'), 
        ndp=('ndp_votes', 'sum'), sources=('name_2019', 'nunique')
    ).reset_index()
    
    for _, row in districts_2026.iterrows():
        if row['total_votes'] < 15000: continue
        margin = max(row['ucp']/row['total_votes'], row['ndp']/row['total_votes'])
        if row['sources'] >= 2 and margin > 0.62:
            donor_slices = crosswalk[crosswalk['name_2026'] == row['name_2026']]
            donors = donor_slices[donor_slices['total_votes'] > 1000]['name_2019'].tolist()
            events.append({
                'type': 'Packing', 'map_label': map_label, 'target_2026': row['name_2026'],
                'donors': donors
            })
            
    # 3. Draining
    eds_2026['area_2026'] = eds_2026.geometry.area
    cw_area = crosswalk.merge(eds_2026[['name', 'area_2026']].rename(columns={'name':'name_2026'}), on='name_2026')
    cw_area['density'] = cw_area['total_votes'] / cw_area['area_m2']
    cw_area['score'] = cw_area['density'] * cw_area['area_2026']
    drains = cw_area.sort_values('score', ascending=False).head(5)
    for _, row in drains.iterrows():
        events.append({
            'type': 'Draining', 'map_label': map_label, 'target_2019': row['name_2019'],
            'recipient_2026': row['name_2026']
        })
        
    return events

def plot_va_dots(ax, boundary_poly, va_pts):
    pts_in = va_pts[va_pts.geometry.within(boundary_poly)]
    if not pts_in.empty:
        # Scale dots by total votes, alpha blending to show density
        sizes = (pts_in['total'] / pts_in['total'].max() * 150).clip(lower=10)
        pts_in.plot(ax=ax, color=pts_in['color'], markersize=sizes, alpha=0.5, edgecolor='none')
    return pts_in

def get_net_margin(pts):
    if pts.empty: return 0, "Tie"
    ucp = pts['va_ucp'].sum()
    ndp = pts['va_ndp'].sum()
    margin = abs(ucp - ndp)
    lean = "UCP" if ucp > ndp else "NDP"
    return margin, lean

def render_xray_event(event, eds_2019, eds_2026, va_pts):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 11))
    fig.patch.set_facecolor('#ffffff')
    for ax in [ax1, ax2]: 
        ax.set_facecolor('#f0f2f5')
        ax.axis('off')
    
    etype = event['type']
    mlabel = event['map_label']
    
    # Mapline coloring
    border_color = '#6b21a8' if mlabel == 'Minority' else '#166534'
    
    if etype == 'Cracking' or etype == 'Draining':
        target_poly = eds_2019[eds_2019['name'] == event['target_2019']].geometry.iloc[0]
        title_target = event['target_2019']
    else: # Packing
        target_poly = eds_2026[eds_2026['name'] == event['target_2026']].geometry.iloc[0]
        title_target = event['target_2026']
        
    # Get bounds slightly larger than target
    bbox = target_poly.buffer(5000) 
    
    # ---------------------------------------------
    # PANEL 1: The Scene of the Crime (2019 X-Ray)
    # ---------------------------------------------
    ax1.set_title("Panel 1: The Source (2019 Baseline)", fontsize=22, weight='bold', pad=15)
    
    # Plot light context
    context = eds_2019[eds_2019.intersects(bbox)]
    context.plot(ax=ax1, facecolor='none', edgecolor='#cccccc', linewidth=1)
    
    # If Cracking/Draining, plot the 2019 target
    if etype in ['Cracking', 'Draining']:
        target_shape = eds_2019[eds_2019['name'] == event['target_2019']]
        target_shape.plot(ax=ax1, facecolor='none', edgecolor='black', linewidth=4)
        # Plot Dots
        pts1 = plot_va_dots(ax1, target_poly, va_pts)
        margin1, lean1 = get_net_margin(pts1)
        
        # Overlay the aggressive 2026 cut lines
        if etype == 'Cracking':
            cutters = eds_2026[eds_2026['name'].isin(event['pieces'])]
            gpd.clip(cutters, target_shape).plot(ax=ax1, facecolor='none', edgecolor=border_color, linewidth=5, linestyle='--')
        else:
            swallower = eds_2026[eds_2026['name'] == event['recipient_2026']]
            gpd.clip(swallower, target_shape).plot(ax=ax1, facecolor='none', edgecolor=border_color, linewidth=5, linestyle='--')
            
    elif etype == 'Packing':
        # The target is the 2026 Sink. We show the 2019 donors.
        donors = eds_2019[eds_2019['name'].isin(event['donors'])]
        donors.plot(ax=ax1, facecolor='none', edgecolor='black', linewidth=3)
        pts1_frames = []
        for _, r in donors.iterrows():
            pts_d = plot_va_dots(ax1, r.geometry, va_pts)
            pts1_frames.append(pts_d)
        if pts1_frames: pts1 = pd.concat(pts1_frames)
        else: pts1 = pd.DataFrame()
        margin1, lean1 = get_net_margin(pts1)
        
        # Overlay the new 2026 boundary that scoops them up
        target_shape = eds_2026[eds_2026['name'] == title_target]
        target_shape.plot(ax=ax1, facecolor='none', edgecolor=border_color, linewidth=5, linestyle='--')

    ax1.set_xlim(bbox.bounds[0], bbox.bounds[2])
    ax1.set_ylim(bbox.bounds[1], bbox.bounds[3])

    # ---------------------------------------------
    # PANEL 2: The Washout Effect (2026 X-Ray)
    # ---------------------------------------------
    ax2.set_title(f"Panel 2: The Washout (2026 {mlabel})", fontsize=22, weight='bold', pad=15)
    
    # Plot light context
    context2 = eds_2026[eds_2026.intersects(bbox)]
    context2.plot(ax=ax2, facecolor='none', edgecolor='#cccccc', linewidth=1)
    
    if etype == 'Cracking':
        cutters = eds_2026[eds_2026['name'].isin(event['pieces'])]
        cutters.plot(ax=ax2, facecolor='none', edgecolor=border_color, linewidth=4)
        pts2_frames = []
        for _, r in cutters.iterrows():
            pts_d = plot_va_dots(ax2, r.geometry, va_pts)
            pts2_frames.append(pts_d)
        if pts2_frames: pts2 = pd.concat(pts2_frames)
        else: pts2 = pd.DataFrame()
        margin2, lean2 = get_net_margin(pts2)
        
    elif etype == 'Draining':
        swallower = eds_2026[eds_2026['name'] == event['recipient_2026']]
        swallower.plot(ax=ax2, facecolor='none', edgecolor=border_color, linewidth=4)
        # We need to expand bounds to show the whole swallower
        sw_bbox = swallower.geometry.iloc[0].buffer(1000)
        ax2.set_xlim(sw_bbox.bounds[0], sw_bbox.bounds[2])
        ax2.set_ylim(sw_bbox.bounds[1], sw_bbox.bounds[3])
        pts2 = plot_va_dots(ax2, swallower.geometry.iloc[0], va_pts)
        margin2, lean2 = get_net_margin(pts2)
        
    elif etype == 'Packing':
        target_shape = eds_2026[eds_2026['name'] == title_target]
        target_shape.plot(ax=ax2, facecolor='none', edgecolor=border_color, linewidth=4)
        pts2 = plot_va_dots(ax2, target_poly, va_pts)
        margin2, lean2 = get_net_margin(pts2)

    if etype != 'Draining':
        ax2.set_xlim(bbox.bounds[0], bbox.bounds[2])
        ax2.set_ylim(bbox.bounds[1], bbox.bounds[3])

    # Add Text Box in Center
    clean_title = f"{mlabel}_{etype}_{title_target.replace(' ', '_').replace('/', '_')}"
    fig.suptitle(f"Partisan X-Ray: {etype} of {title_target}", fontsize=30, weight='bold', y=1.05)
    
    impact_text = (
        f"NET PARTISAN IMPACT\n"
        f"-------------------\n"
        f"Source Area Lean: +{margin1:,.0f} {lean1}\n"
        f"Resulting Area Lean: +{margin2:,.0f} {lean2}"
    )
    fig.text(0.5, 0.05, impact_text, ha='center', va='center', fontsize=20, weight='bold', 
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1', linewidth=2))
             
    # Legend
    ndp_patch = mpatches.Patch(color=NDP_COLOR, label='NDP Voter Cluster')
    ucp_patch = mpatches.Patch(color=UCP_COLOR, label='UCP Voter Cluster')
    border_line = plt.Line2D([0], [0], color=border_color, linewidth=4, linestyle='--', label=f'2026 {mlabel} Map Cut-Lines')
    fig.legend(handles=[ndp_patch, ucp_patch, border_line], loc='upper right', fontsize=14, bbox_to_anchor=(0.95, 1.0))

    plt.tight_layout(rect=[0, 0.1, 1, 1])
    outpath = PROOFS_DIR / f"{clean_title}.svg"
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Generated X-Ray proof: {outpath.name}")

if __name__ == "__main__":
    print("Loading data for Partisan X-Rays...")
    eds_2019, eds_min, eds_maj, va_pts = load_data()
    
    print("Analyzing Minority Map events...")
    min_events = get_events(eds_2019, eds_min, va_pts, "Minority")
    
    print("Analyzing Majority Map events...")
    maj_events = get_events(eds_2019, eds_maj, va_pts, "Majority")
    
    all_events = min_events + maj_events
    
    # Deduplicate events
    seen = set()
    unique_events = []
    for e in all_events:
        target = e.get('target_2019') or e.get('target_2026')
        key = f"{e['map_label']}_{e['type']}_{target}"
        if key not in seen:
            seen.add(key)
            unique_events.append(e)
            
    print(f"Rendering {len(unique_events)} Partisan X-Rays...")
    for e in unique_events:
        m = eds_min if e['map_label'] == 'Minority' else eds_maj
        render_xray_event(e, eds_2019, m, va_pts)
    
    print("Done generating X-Ray Proofs!")
