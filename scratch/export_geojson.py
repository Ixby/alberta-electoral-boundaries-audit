import warnings
import os
import json
import geopandas as gpd
import pandas as pd
from pathlib import Path

warnings.filterwarnings('ignore')

ROOT = Path("C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit")
VA_VOTES_PATH = ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
EDS_2019_PATH = ROOT / "data" / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
EDS_MIN_PATH = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_minority_2026_eds.gpkg"
EDS_MAJ_PATH = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_majority_2026_eds.gpkg"
WEB_DATA_DIR = ROOT / "interactive_proofs" / "public" / "data"

os.makedirs(WEB_DATA_DIR, exist_ok=True)

def load_data():
    eds_2019 = gpd.read_file(EDS_2019_PATH).to_crs(4326)
    name_col = [c for c in eds_2019.columns if 'name' in c.lower()][0] if [c for c in eds_2019.columns if 'name' in c.lower()] else eds_2019.columns[0]
    eds_2019 = eds_2019[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_2019['name'] = eds_2019['name'].str.title().str.strip()

    eds_min = gpd.read_file(EDS_MIN_PATH).to_crs(4326)
    name_col = [c for c in eds_min.columns if 'name' in c.lower()][0]
    eds_min = eds_min[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_min['name'] = eds_min['name'].str.title().str.strip()

    eds_maj = gpd.read_file(EDS_MAJ_PATH).to_crs(4326)
    name_col = [c for c in eds_maj.columns if 'name' in c.lower()][0]
    eds_maj = eds_maj[[name_col, 'geometry']].rename(columns={name_col: 'name'})
    eds_maj['name'] = eds_maj['name'].str.title().str.strip()
    
    eds_2019_proj = eds_2019.to_crs(3401)
    eds_min_proj = eds_min.to_crs(3401)
    eds_maj_proj = eds_maj.to_crs(3401)
    
    va = gpd.read_file(VA_VOTES_PATH).to_crs(4326)
    va_pts = gpd.GeoDataFrame(
        {"va_ucp": va["va_ucp"].fillna(0), "va_ndp": va["va_ndp"].fillna(0)},
        geometry=va.geometry.centroid,
        crs=4326
    )
    va_pts['total'] = va_pts['va_ucp'] + va_pts['va_ndp']
    va_pts = va_pts[va_pts['total'] > 0]
    va_pts['party'] = va_pts.apply(lambda r: 'NDP' if r['va_ndp'] > r['va_ucp'] else 'UCP', axis=1)
    
    va_pts_proj = gpd.GeoDataFrame(va_pts.drop(columns='geometry'), geometry=va.geometry.centroid.to_crs(3401), crs=3401)
    
    return eds_2019, eds_min, eds_maj, va_pts, eds_2019_proj, eds_min_proj, eds_maj_proj, va_pts_proj

def get_events(eds_2019_proj, eds_2026_proj, va_pts_proj, map_label):
    crosswalk = gpd.overlay(eds_2019_proj.rename(columns={'name':'name_2019'}), eds_2026_proj.rename(columns={'name':'name_2026'}), how='intersection')
    crosswalk['area_m2'] = crosswalk.geometry.area
    crosswalk = crosswalk[crosswalk['area_m2'] > 100000].copy()
    crosswalk['slice_id'] = range(len(crosswalk))
    
    joined = gpd.sjoin(va_pts_proj, crosswalk[['slice_id', 'geometry']], how='inner', predicate='within')
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
            
    eds_2026_proj['area_2026'] = eds_2026_proj.geometry.area
    cw_area = crosswalk.merge(eds_2026_proj[['name', 'area_2026']].rename(columns={'name':'name_2026'}), on='name_2026')
    cw_area['density'] = cw_area['total_votes'] / cw_area['area_m2']
    cw_area['score'] = cw_area['density'] * cw_area['area_2026']
    drains = cw_area.sort_values('score', ascending=False).head(5)
    for _, row in drains.iterrows():
        events.append({'type': 'Draining', 'map_label': map_label, 'target_2019': row['name_2019'], 'recipient_2026': row['name_2026']})
        
    return events

def calc_stats(pts):
    if pts.empty: return {"ucp":0, "ndp":0, "margin":0, "winner":"N/A", "safety":"N/A", "total":0}
    ucp = pts['va_ucp'].sum()
    ndp = pts['va_ndp'].sum()
    total = ucp + ndp
    if total == 0: return {"ucp":0, "ndp":0, "margin":0, "winner":"N/A", "safety":"N/A", "total":0}
    ucp_pct = (ucp / total) * 100
    ndp_pct = (ndp / total) * 100
    margin = abs(ucp_pct - ndp_pct)
    winner = "UCP" if ucp > ndp else "NDP"
    if margin > 15: safety = "Safe Seat"
    elif margin > 5: safety = "Lean"
    else: safety = "Competitive Toss-Up"
    return {"ucp": ucp_pct, "ndp": ndp_pct, "margin": margin, "winner": winner, "safety": safety, "total": total}

if __name__ == "__main__":
    print("Loading and projecting data...")
    eds_2019, eds_min, eds_maj, va_pts, eds_2019_proj, eds_min_proj, eds_maj_proj, va_pts_proj = load_data()
    min_events = get_events(eds_2019_proj, eds_min_proj, va_pts_proj, "Minority")
    maj_events = get_events(eds_2019_proj, eds_maj_proj, va_pts_proj, "Majority")
    all_events = min_events + maj_events
    
    seen, unique_events = set(), []
    for e in all_events:
        target = e.get('target_2019') or e.get('target_2026')
        key = f"{e['map_label']}_{e['type']}_{target}"
        if key not in seen:
            seen.add(key)
            unique_events.append(e)
            
    print(f"Exporting {len(unique_events)} events to Web JSON...")
    
    export_data = []
    
    for e in unique_events:
        m_2026 = eds_min if e['map_label'] == 'Minority' else eds_maj
        
        etype = e['type']
        title_target = e.get('target_2019') or e.get('target_2026')
        title = f"How They Changed {title_target}"
        
        if etype in ['Cracking', 'Draining']:
            target_poly = eds_2019[eds_2019['name'] == e['target_2019']].geometry.iloc[0]
        else:
            target_poly = m_2026[m_2026['name'] == e['target_2026']].geometry.iloc[0]
            
        # Get bounding box (in 4326)
        bounds = target_poly.bounds
        
        # Calculate stats for the Old Map (pts within target_poly)
        pts_old = va_pts[va_pts.geometry.within(target_poly)]
        old_stats = calc_stats(pts_old)
        
        # Calculate stats for the New Map
        if etype == 'Cracking':
            pts2_frames = []
            for piece in e['pieces']:
                recip = m_2026[m_2026['name'] == piece].geometry.iloc[0]
                pts2_frames.append(va_pts[va_pts.geometry.within(recip)])
            pts_new = pd.concat(pts2_frames) if pts2_frames else pd.DataFrame()
            desc = "Cracking: Dividing a cohesive community across multiple districts to dilute their voting power."
            voter_impact = f"If you lived in {title_target}, your neighborhood was shattered across {len(e['pieces'])} different boundaries."
        elif etype == 'Draining':
            swallower = m_2026[m_2026['name'] == e['recipient_2026']].geometry.iloc[0]
            bounds = swallower.bounds # Expand bounds for draining
            pts_new = va_pts[va_pts.geometry.within(swallower)]
            desc = "Draining: Detaching a dense urban neighborhood and submerging it into a massive rural periphery."
            voter_impact = f"If you lived in {title_target}, your urban voting power was completely drained into the massive {e['recipient_2026']} periphery."
        else:
            pts_new = va_pts[va_pts.geometry.within(target_poly)]
            desc = "Packing: Artificially concentrating targeted voter blocs from multiple districts to engineer a safe seat."
            voter_impact = f"If you lived in {title_target}, your new district was artificially packed with voters from {len(e['donors'])} different districts to guarantee a predetermined outcome."
            
        new_stats = calc_stats(pts_new)
        
        event_id = f"{e['map_label']}_{etype}_{title_target.replace(' ', '_').replace('/', '_')}"
        
        export_data.append({
            "id": event_id,
            "type": etype,
            "title": title,
            "desc": desc,
            "voter_impact": voter_impact,
            "bounds": bounds,
            "old_stats": old_stats,
            "new_stats": new_stats,
            "target": title_target,
            "map_label": e['map_label']
        })
        
        # We also need to save the specific geometries for this event
        # Actually, saving intersections might be computationally heavy, we will just save the base geojson 
        ctx_2019 = eds_2019[eds_2019.geometry.intersects(target_poly)]
        ctx_2026 = m_2026[m_2026.geometry.intersects(target_poly)]
        
        ctx_2019.to_file(WEB_DATA_DIR / f"{event_id}_2019.geojson", driver="GeoJSON")
        ctx_2026.to_file(WEB_DATA_DIR / f"{event_id}_2026.geojson", driver="GeoJSON")
        
        bounds_poly = target_poly
        if etype == 'Draining': bounds_poly = swallower
        
        pts_export = va_pts[va_pts.geometry.within(bounds_poly)]
        pts_export.to_file(WEB_DATA_DIR / f"{event_id}_dots.geojson", driver="GeoJSON")
        
    with open(WEB_DATA_DIR / "events.json", "w") as f:
        json.dump(export_data, f, indent=2)
        
    print("Done!")
