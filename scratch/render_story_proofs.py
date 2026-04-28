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
EDS_MIN_PATH = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_minority_2026_eds.gpkg"
EDS_MAJ_PATH = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_majority_2026_eds.gpkg"
PROOFS_DIR = ROOT / "scratch" / "story_proofs"

os.makedirs(PROOFS_DIR, exist_ok=True)

NDP_COLOR = '#f37021'
UCP_COLOR = '#003f72'
HIGHLIGHT_COLORS = ['#fbbf24', '#34d399', '#f472b6', '#38bdf8'] # Amber, Emerald, Pink, Sky

def load_data():
    eds_2019 = gpd.read_file(EDS_2019_PATH).to_crs(3401)
    name_col = [c for c in eds_2019.columns if 'name' in c.lower()][0] if [c for c in eds_2019.columns if 'name' in c.lower()] else eds_2019.columns[0]
    eds_2019 = eds_2019[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_2019['name'] = eds_2019['name'].str.title().str.strip() 

    eds_min = gpd.read_file(EDS_MIN_PATH).to_crs(3401)
    name_col = [c for c in eds_min.columns if 'name' in c.lower()][0]
    eds_min = eds_min[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_min['name'] = eds_min['name'].str.title().str.strip()

    eds_maj = gpd.read_file(EDS_MAJ_PATH).to_crs(3401)
    name_col = [c for c in eds_maj.columns if 'name' in c.lower()][0]
    eds_maj = eds_maj[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_maj['name'] = eds_maj['name'].str.title().str.strip()
    
    va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
    va_pts = gpd.GeoDataFrame(
        {"va_ucp": va["va_ucp"].fillna(0), "va_ndp": va["va_ndp"].fillna(0)},
        geometry=va.geometry.centroid,
        crs=3401
    )
    va_pts['total'] = va_pts['va_ucp'] + va_pts['va_ndp']
    va_pts = va_pts[va_pts['total'] > 0]
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
    
    splits = crosswalk.groupby('name_2019').size()
    cracked = splits[splits >= 3].index
    for district in cracked:
        slices = crosswalk[crosswalk['name_2019'] == district]
        if slices['total_votes'].sum() >= 10000:
            events.append({'type': 'Cracking', 'map_label': map_label, 'target_2019': district, 'pieces': slices['name_2026'].tolist()})
            
    districts_2026 = crosswalk.groupby('name_2026').agg(
        total_votes=('total_votes', 'sum'), ucp=('ucp_votes', 'sum'), 
        ndp=('ndp_votes', 'sum'), sources=('name_2019', 'nunique')).reset_index()
    
    for _, row in districts_2026.iterrows():
        if row['total_votes'] < 15000: continue
        margin = max(row['ucp']/row['total_votes'], row['ndp']/row['total_votes'])
        if row['sources'] >= 2 and margin > 0.62:
            donor_slices = crosswalk[crosswalk['name_2026'] == row['name_2026']]
            donors = donor_slices[donor_slices['total_votes'] > 1000]['name_2019'].tolist()
            events.append({'type': 'Packing', 'map_label': map_label, 'target_2026': row['name_2026'], 'donors': donors})
            
    eds_2026['area_2026'] = eds_2026.geometry.area
    cw_area = crosswalk.merge(eds_2026[['name', 'area_2026']].rename(columns={'name':'name_2026'}), on='name_2026')
    cw_area['density'] = cw_area['total_votes'] / cw_area['area_m2']
    cw_area['score'] = cw_area['density'] * cw_area['area_2026']
    drains = cw_area.sort_values('score', ascending=False).head(5)
    for _, row in drains.iterrows():
        events.append({'type': 'Draining', 'map_label': map_label, 'target_2019': row['name_2019'], 'recipient_2026': row['name_2026']})
        
    return events

def plot_va_dots(ax, boundary_poly, va_pts, highlight_poly=None):
    pts_in = va_pts[va_pts.geometry.within(boundary_poly)]
    if not pts_in.empty:
        sizes = (pts_in['total'] / pts_in['total'].max() * 150).clip(lower=10)
        
        if highlight_poly is not None:
            pts_focus = pts_in[pts_in.geometry.within(highlight_poly)]
            pts_fade = pts_in[~pts_in.geometry.within(highlight_poly)]
            if not pts_fade.empty:
                pts_fade.plot(ax=ax, color='#e2e8f0', markersize=sizes.loc[pts_fade.index], alpha=0.3, edgecolor='none')
            if not pts_focus.empty:
                pts_focus.plot(ax=ax, color=pts_focus['color'], markersize=sizes.loc[pts_focus.index]*1.2, alpha=0.9, edgecolor='none')
        else:
            pts_in.plot(ax=ax, color=pts_in['color'], markersize=sizes, alpha=0.6, edgecolor='none')
            
    return pts_in

def add_power_bar(ax, pts, title):
    if pts.empty: return
    ucp = pts['va_ucp'].sum()
    ndp = pts['va_ndp'].sum()
    total = ucp + ndp
    if total == 0: return
    
    ucp_pct = (ucp / total) * 100
    ndp_pct = (ndp / total) * 100
    
    ax.axis('off')
    
    bar_height = 0.6
    ax.barh([0], [ndp_pct], color=NDP_COLOR, height=bar_height, left=0)
    ax.barh([0], [ucp_pct], color=UCP_COLOR, height=bar_height, left=ndp_pct)
    
    if ndp_pct > 15:
        ax.text(ndp_pct / 2, 0, f"NDP {ndp_pct:.0f}%", color='white', weight='bold', fontsize=20, va='center', ha='center')
    if ucp_pct > 15:
        ax.text(ndp_pct + (ucp_pct / 2), 0, f"UCP {ucp_pct:.0f}%", color='white', weight='bold', fontsize=20, va='center', ha='center')
    
    margin = abs(ucp_pct - ndp_pct)
    winner = "UCP" if ucp > ndp else "NDP"
    if margin > 15: safety = "Safe Seat"
    elif margin > 5: safety = "Lean"
    else: safety = "Competitive Toss-Up"
    
    stats_text = f"{title}\n{winner} Wins by {margin:.0f}% ({safety})"
    ax.set_title(stats_text, fontsize=20, weight='bold', color='#1e293b', pad=15)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)

def get_margin_from_pts(pts):
    if pts.empty: return 0
    ucp = pts['va_ucp'].sum()
    ndp = pts['va_ndp'].sum()
    total = ucp + ndp
    if total == 0: return 0
    return (ucp / total * 100) - (ndp / total * 100) # Positive = UCP favored

def get_intersection(base_gdf, base_name, overlay_gdf, overlay_name):
    g1 = base_gdf[base_gdf['name'] == base_name]
    g2 = overlay_gdf[overlay_gdf['name'] == overlay_name]
    return gpd.clip(g1, g2)

def render_story_event(event, eds_2019, eds_2026, va_pts, index, total_events):
    fig = plt.figure(figsize=(26, 17))
    fig.patch.set_facecolor('#ffffff')
    
    gs = fig.add_gridspec(2, 2, height_ratios=[6, 1], hspace=0.3, wspace=0.1)
    ax_map1 = fig.add_subplot(gs[0, 0])
    ax_map2 = fig.add_subplot(gs[0, 1])
    ax_bar1 = fig.add_subplot(gs[1, 0])
    ax_bar2 = fig.add_subplot(gs[1, 1])
    
    for ax in [ax_map1, ax_map2, ax_bar1, ax_bar2]: ax.axis('off')
    
    etype = event['type']
    mlabel = event['map_label']
    border_color = '#000000'
    
    if etype in ['Cracking', 'Draining']:
        target_poly = eds_2019[eds_2019['name'] == event['target_2019']].geometry.iloc[0]
        title_target = event['target_2019']
    else:
        target_poly = eds_2026[eds_2026['name'] == event['target_2026']].geometry.iloc[0]
        title_target = event['target_2026']
        
    bbox = target_poly.buffer(5000) 
    
    if etype == 'Cracking':
        definition = "CRACKING: Dividing a cohesive community across multiple districts to dilute their voting power."
        voter_impact = f"If you lived in {title_target}, your neighborhood was shattered across {len(event['pieces'])} different boundaries."
    elif etype == 'Draining':
        definition = "DRAINING: Detaching an urban neighborhood and submerging it into a massive rural periphery."
        voter_impact = f"If you lived in {title_target}, your urban voting power was drained into the {event['recipient_2026']} periphery."
    else:
        definition = "PACKING: Artificially concentrating targeted voter blocs from multiple districts to engineer a safe seat."
        voter_impact = f"If you lived in {title_target}, your new district was packed with voters from {len(event['donors'])} different areas."

    ax_map1.set_title("2019 Boundaries (Current)", fontsize=26, weight='bold', pad=15)
    ax_map2.set_title("Proposed Boundaries", fontsize=26, weight='bold', pad=15)
    
    context = eds_2019[eds_2019.intersects(bbox)]
    context.plot(ax=ax_map1, facecolor='none', edgecolor='#e2e8f0', linewidth=1)
    
    pts1_frames = []
    carveout_patches = [] 
    displaced_voters = 0
    
    if etype == 'Cracking':
        target_shape = eds_2019[eds_2019['name'] == event['target_2019']]
        target_shape.plot(ax=ax_map1, facecolor='none', edgecolor='#64748b', linewidth=4)
        
        all_intersections = []
        for i, piece in enumerate(event['pieces']):
            intersect = get_intersection(eds_2019, event['target_2019'], eds_2026, piece)
            c = HIGHLIGHT_COLORS[i % len(HIGHLIGHT_COLORS)]
            intersect.plot(ax=ax_map1, facecolor='none', edgecolor=c, linewidth=4, hatch='///')
            all_intersections.append(intersect.geometry.iloc[0])
            carveout_patches.append(mpatches.Patch(facecolor='none', edgecolor=c, hatch='///', label=f"Transferred to {piece}"))
            
            p = va_pts[va_pts.geometry.within(intersect.geometry.iloc[0])]
            displaced_voters += p['total'].sum() if not p.empty else 0
            
        if all_intersections:
            combined_focus = gpd.GeoSeries(all_intersections).unary_union
            plot_va_dots(ax_map1, target_poly, va_pts, highlight_poly=combined_focus)
        
        pts1_frames = [va_pts[va_pts.geometry.within(target_poly)]]
        
    elif etype == 'Draining':
        target_shape = eds_2019[eds_2019['name'] == event['target_2019']]
        target_shape.plot(ax=ax_map1, facecolor='none', edgecolor='#64748b', linewidth=4)
        
        intersect = get_intersection(eds_2019, event['target_2019'], eds_2026, event['recipient_2026'])
        c = HIGHLIGHT_COLORS[0]
        intersect.plot(ax=ax_map1, facecolor='none', edgecolor=c, linewidth=4, hatch='///')
        carveout_patches.append(mpatches.Patch(facecolor='none', edgecolor=c, hatch='///', label=f"Transferred Area"))
        
        plot_va_dots(ax_map1, target_poly, va_pts, highlight_poly=intersect.geometry.iloc[0])
        pts1_frames = [va_pts[va_pts.geometry.within(target_poly)]]
        
        p = va_pts[va_pts.geometry.within(intersect.geometry.iloc[0])]
        displaced_voters = p['total'].sum() if not p.empty else 0
            
    elif etype == 'Packing':
        for i, donor in enumerate(event['donors']):
            donor_shape = eds_2019[eds_2019['name'] == donor]
            donor_shape.plot(ax=ax_map1, facecolor='none', edgecolor='#64748b', linewidth=2)
            plot_va_dots(ax_map1, donor_shape.geometry.iloc[0], va_pts)
            
            intersect = get_intersection(eds_2019, donor, eds_2026, title_target)
            c = HIGHLIGHT_COLORS[i % len(HIGHLIGHT_COLORS)]
            intersect.plot(ax=ax_map1, facecolor='none', edgecolor=c, linewidth=4, hatch='///')
            carveout_patches.append(mpatches.Patch(facecolor='none', edgecolor=c, hatch='///', label=f"Sourced from {donor}"))
            
            p = va_pts[va_pts.geometry.within(intersect.geometry.iloc[0])]
            pts1_frames.append(p)
            displaced_voters += p['total'].sum() if not p.empty else 0

    if etype == 'Draining':
        swallower = eds_2026[eds_2026['name'] == event['recipient_2026']]
        matched_bbox = swallower.geometry.iloc[0].buffer(2000)
    else:
        matched_bbox = bbox
        
    ax_map1.set_xlim(matched_bbox.bounds[0], matched_bbox.bounds[2])
    ax_map1.set_ylim(matched_bbox.bounds[1], matched_bbox.bounds[3])
    
    pts1 = pd.concat(pts1_frames) if pts1_frames else pd.DataFrame()
    add_power_bar(ax_bar1, pts1, "2023 Result (Current)")
    old_margin = get_margin_from_pts(pts1)

    # ---------------------------------------------
    # PANEL 2
    # ---------------------------------------------
    context2 = eds_2026[eds_2026.intersects(matched_bbox)]
    context2.plot(ax=ax_map2, facecolor='none', edgecolor='#e2e8f0', linewidth=1)
    
    pts2_frames = []
    
    if etype == 'Cracking':
        for i, piece in enumerate(event['pieces']):
            recipient = eds_2026[eds_2026['name'] == piece]
            recipient.plot(ax=ax_map2, facecolor='none', edgecolor=border_color, linewidth=2)
            plot_va_dots(ax_map2, recipient.geometry.iloc[0], va_pts)
            
            intersect = get_intersection(eds_2019, event['target_2019'], eds_2026, piece)
            c = HIGHLIGHT_COLORS[i % len(HIGHLIGHT_COLORS)]
            intersect.plot(ax=ax_map2, facecolor='none', edgecolor=c, linewidth=4, hatch='///')
            pts2_frames.append(va_pts[va_pts.geometry.within(recipient.geometry.iloc[0])])
            
    elif etype == 'Draining':
        swallower = eds_2026[eds_2026['name'] == event['recipient_2026']]
        swallower.plot(ax=ax_map2, facecolor='none', edgecolor=border_color, linewidth=4)
        
        cx, cy = swallower.geometry.iloc[0].centroid.x, swallower.geometry.iloc[0].centroid.y
        ax_map2.text(cx, cy, event['recipient_2026'].upper(), color='#000000', fontsize=20, weight='bold', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.85, edgecolor='#cbd5e1', pad=8, boxstyle='round,pad=0.3'))
        
        plot_va_dots(ax_map2, swallower.geometry.iloc[0], va_pts)
        
        intersect = get_intersection(eds_2019, event['target_2019'], eds_2026, event['recipient_2026'])
        intersect.plot(ax=ax_map2, facecolor='none', edgecolor=HIGHLIGHT_COLORS[0], linewidth=4, hatch='///')
        pts2_frames.append(va_pts[va_pts.geometry.within(swallower.geometry.iloc[0])])
        
    elif etype == 'Packing':
        target_shape = eds_2026[eds_2026['name'] == title_target]
        target_shape.plot(ax=ax_map2, facecolor='none', edgecolor=border_color, linewidth=4)
        plot_va_dots(ax_map2, target_poly, va_pts)
        
        for i, donor in enumerate(event['donors']):
            intersect = get_intersection(eds_2019, donor, eds_2026, title_target)
            c = HIGHLIGHT_COLORS[i % len(HIGHLIGHT_COLORS)]
            intersect.plot(ax=ax_map2, facecolor='none', edgecolor=c, linewidth=4, hatch='///')
            
        pts2_frames.append(va_pts[va_pts.geometry.within(target_poly)])

    ax_map2.set_xlim(matched_bbox.bounds[0], matched_bbox.bounds[2])
    ax_map2.set_ylim(matched_bbox.bounds[1], matched_bbox.bounds[3])

    pts2 = pd.concat(pts2_frames) if pts2_frames else pd.DataFrame()
    add_power_bar(ax_bar2, pts2, "Projected Result (Proposed)")
    new_margin = get_margin_from_pts(pts2)

    # ADDING THE SEVERITY INDICATORS

    # Voters Displaced Badge (Placed centrally on the arrow)
    fig.add_artist(mpatches.ConnectionPatch(
        xyA=(1.05, 0.5), xyB=(-0.05, 0.5), coordsA='axes fraction', coordsB='axes fraction',
        axesA=ax_map1, axesB=ax_map2, arrowstyle="-|>", lw=14, color='#0f172a'))
        
    fig.text(0.5, 0.60, f"Voters Displaced: {int(displaced_voters):,}", ha='center', va='center', 
             fontsize=18, weight='bold', color='white', 
             bbox=dict(facecolor='#0f172a', edgecolor='none', pad=8, boxstyle='round,pad=0.5'))

    # Net Partisan Swing Badge (Placed between the power bars)
    net_swing = new_margin - old_margin
    if abs(net_swing) > 0.5:
        swing_party = "UCP" if net_swing > 0 else "NDP"
        swing_color = UCP_COLOR if net_swing > 0 else NDP_COLOR
        fig.text(0.5, 0.17, f"NET SWING: {abs(net_swing):.1f}-Point {swing_party} Shift", ha='center', va='center', 
                 fontsize=20, weight='bold', color=swing_color, 
                 bbox=dict(facecolor='white', edgecolor=swing_color, pad=8, boxstyle='round,pad=0.5', linewidth=3))

    # Legend
    legend_handles = [
        mpatches.Patch(color=NDP_COLOR, label='NDP Voters'), 
        mpatches.Patch(color=UCP_COLOR, label='UCP Voters')
    ] + carveout_patches
    fig.legend(handles=legend_handles, loc='lower center', ncol=min(len(legend_handles), 5), fontsize=16, frameon=False, bbox_to_anchor=(0.5, 0.05))

    # Footer
    fig.text(0.5, 0.02, f"Forensic Evidence: Event {index} of {total_events} documented boundary manipulations.", ha='center', fontsize=14, color='#64748b', style='italic')

    plt.tight_layout(rect=[0, 0.10, 1, 0.80])

    fig.suptitle(f"How They Changed {title_target}", fontsize=38, weight='bold', y=0.96)
    fig.text(0.5, 0.90, definition, ha='center', va='center', fontsize=22, weight='bold', color='#dc2626')
    fig.text(0.5, 0.86, f"\"{voter_impact}\"", ha='center', va='center', fontsize=24, style='italic', color='#1e293b')
    
    clean_title = f"{mlabel}_{etype}_{title_target.replace(' ', '_').replace('/', '_')}"
    outpath_svg = PROOFS_DIR / f"{clean_title}.svg"
    outpath_pdf = PROOFS_DIR / f"{clean_title}.pdf"
    plt.savefig(outpath_svg, format='svg', bbox_inches='tight')
    plt.savefig(outpath_pdf, format='pdf', bbox_inches='tight')
    plt.close()
    print(f"Generated Vector V2 proofs: {clean_title}")

if __name__ == "__main__":
    print("Loading data for V2 Flow Infographics...")
    eds_2019, eds_min, eds_maj, va_pts = load_data()
    min_events = get_events(eds_2019, eds_min, va_pts, "Minority")
    maj_events = get_events(eds_2019, eds_maj, va_pts, "Majority")
    all_events = min_events + maj_events
    
    seen, unique_events = set(), []
    for e in all_events:
        target = e.get('target_2019') or e.get('target_2026')
        key = f"{e['map_label']}_{e['type']}_{target}"
        if key not in seen:
            seen.add(key)
            unique_events.append(e)
            
    total = len(unique_events)
    print(f"Rendering {total} V2 Infographics...")
    for idx, e in enumerate(unique_events, start=1):
        m = eds_min if e['map_label'] == 'Minority' else eds_maj
        render_story_event(e, eds_2019, m, va_pts, idx, total)
    
    print("Done! V2 layout fully rendered.")
