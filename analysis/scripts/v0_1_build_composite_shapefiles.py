"""
v0_1_build_composite_shapefiles.py
===================================
Builds best-available 89-ED GeoPackages for both maps by merging:

  Priority (majority):  v7 non-null  >  2019 parent polygon
  Priority (minority):  v7 non-null  >  v6 minority (70-ED)  >  2019 parent polygon

For null EDs in v7, the 2019 parent polygon is used as a fallback.  For
'direct'/'rename' relationships this is territory-exact.  For 'blend'/'split'
relationships the 2019 polygon over-covers the 2026 ED by definition (the 2026
ED is a subset of the 2019 parent).  The fallback tier is recorded as
'C-fallback-2019-direct' or 'C-fallback-2019-blend' accordingly.

Outputs:
  data/v0_1_composite_majority_2026_eds.gpkg
  data/v0_1_composite_minority_2026_eds.gpkg
  analysis/methodology/v0_1_composite_shapefiles_log.md
"""

import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union
import os, sys
from datetime import datetime

WORK_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(WORK_DIR, 'data')
ANALYSIS_DIR = os.path.join(WORK_DIR, 'analysis')

# ─── 2019 parent polygon fallback mappings ────────────────────────────────────
# Format: 2026_ed_name -> (2019_parent_name_or_list, relationship_type)
# relationship_type: 'direct' = territory-exact rename/reuse
#                    'blend'  = 2026 is subset of 2019 parent (over-covers)
#                    'split'  = 2026 is split of 2019 parent (over-covers)

MAJORITY_NULL_FALLBACK = {
    'Calgary-Confluence':            ('Calgary-Buffalo',            'direct'),
    'Calgary-Nose Creek':            ('Calgary-Beddington',         'direct'),
    'Edmonton-Windermere':           ('Edmonton-South West',        'direct'),
    'Airdrie-East':                  ('Airdrie-East',               'direct'),
    'Airdrie-West':                  ('Airdrie-Cochrane',           'blend'),
    'Barrhead-Westlock-Athabasca':   ('Athabasca-Barrhead-Westlock','direct'),
    'Canmore-Banff':                 ('Banff-Kananaskis',           'direct'),
    'Chestermere-Strathmore':        ('Chestermere-Strathmore',     'direct'),
    'Cochrane-Springbank':           ('Airdrie-Cochrane',           'blend'),
    'Cold Lake-Bonnyville-St. Paul': ('Bonnyville-Cold Lake-St. Paul','direct'),
    'Fort McMurray-Lac La Biche':    ('Fort McMurray-Lac La Biche', 'direct'),
    'High River-Vulcan-Siksika':     ('Highwood',                   'blend'),
    'Leduc-Devon':                   ('Leduc-Beaumont',             'blend'),
    'Lethbridge-East':               ('Lethbridge-East',            'blend'),
    'Lethbridge-West':               ('Lethbridge-West',            'blend'),
    'Medicine Hat-Brooks':           ('Brooks-Medicine Hat',        'direct'),
    'Mountain View-Kneehill':        ('Olds-Didsbury-Three Hills',  'direct'),
    'Okotoks-Diamond Valley':        ('Highwood',                   'blend'),
    'St. Albert-Sturgeon':           ('Morinville-St. Albert',      'blend'),
    'Stony Plain-Drayton Valley':    ('Drayton Valley-Devon',       'direct'),
    'Sylvan Lake-Innisfail':         ('Innisfail-Sylvan Lake',      'direct'),
    'Taber-Cardston':                ('Taber-Warner',               'direct'),
}

MINORITY_NULL_FALLBACK = {
    'Calgary-Airdrie':               ('Airdrie-Cochrane',           'split'),
    'Calgary-McCall-Bhullar':        ('Calgary-McCall',             'direct'),
    'Calgary-North West-Bearspaw':   ('Calgary-North West',         'blend'),
    "Calgary-West-Tsuut'ina":        ('Calgary-West',               'blend'),
    'St. Albert-Sturgeon':           ('Morinville-St. Albert',      'blend'),
}

# ─── Load base files ──────────────────────────────────────────────────────────

def load_2019_lookup():
    """Return dict {ed_name: geometry} in EPSG:3401."""
    shp = os.path.join(DATA_DIR, 'alberta_2019_eds',
                       'EDS_ENACTED_BILL33_15DEC2017.shp')
    gdf = gpd.read_file(shp)
    # CRS is already EPSG:3401
    return dict(zip(gdf['EDName2017'], gdf['geometry']))

def load_v6_minority_lookup():
    """Return dict {name_2026: geometry} from v6 70-ED minority file."""
    gdf = gpd.read_file(os.path.join(DATA_DIR,
                        'v0_1_refined_v6_minority_2026_eds.gpkg'))
    if gdf.crs and gdf.crs.to_epsg() != 3401:
        gdf = gdf.to_crs(epsg=3401)
    return dict(zip(gdf['name_2026'], gdf['geometry']))

def build_fallback_geom(ed_name, fallback_map, lookup_2019):
    """
    Return (geometry, fallback_tier, fallback_note) for a null v7 ED.
    geometry may be None if 2019 parent not found either.
    """
    if ed_name not in fallback_map:
        return None, 'unresolvable', f'No fallback defined for {ed_name}'
    parent, rel = fallback_map[ed_name]
    # parent is always a single 2019 ED name here
    if parent not in lookup_2019:
        return None, 'unresolvable', f'2019 parent {parent!r} not found'
    geom = lookup_2019[parent]
    tier = f'C-fallback-2019-{rel}'
    note = f'2019 parent: {parent} ({rel})'
    return geom, tier, note

# ─── Composite builder ────────────────────────────────────────────────────────

def build_composite(v7_path, fallback_map, label, v6_lookup=None):
    """
    Build composite 89-ED GeoDataFrame.
    Returns (gdf, log_lines).
    """
    gdf = gpd.read_file(v7_path)
    if gdf.crs and gdf.crs.to_epsg() != 3401:
        gdf = gdf.to_crs(epsg=3401)

    lookup_2019 = load_2019_lookup()

    log = []
    sources = []
    fallback_tiers = []
    fallback_notes = []

    null_count = 0
    resolved_v6 = 0
    resolved_2019 = 0
    unresolvable = []

    for idx, row in gdf.iterrows():
        name = row['name_2026']
        geom = row['geometry']

        if geom is not None and not (hasattr(geom, 'is_empty') and geom.is_empty):
            # v7 has a valid geometry
            sources.append('v7')
            fallback_tiers.append(row.get('tier_2026', 'unknown'))
            fallback_notes.append('')
            continue

        null_count += 1

        # Try v6 minority first (if provided)
        if v6_lookup and name in v6_lookup:
            geom_v6 = v6_lookup[name]
            if geom_v6 is not None:
                gdf.at[idx, 'geometry'] = geom_v6
                sources.append('v6-minority')
                fallback_tiers.append('C-v6-fallback')
                fallback_notes.append('v6 minority 70-ED file')
                resolved_v6 += 1
                log.append(f'  {name}: resolved from v6 minority')
                continue

        # Try 2019 parent
        geom_2019, tier, note = build_fallback_geom(name, fallback_map, lookup_2019)
        if geom_2019 is not None:
            gdf.at[idx, 'geometry'] = geom_2019
            sources.append('2019-parent')
            fallback_tiers.append(tier)
            fallback_notes.append(note)
            resolved_2019 += 1
            log.append(f'  {name}: resolved from 2019 ({note})')
        else:
            sources.append('unresolvable')
            fallback_tiers.append('unresolvable')
            fallback_notes.append(note)
            unresolvable.append(name)
            log.append(f'  {name}: UNRESOLVABLE — {note}')

    gdf['composite_source'] = sources
    gdf['composite_tier'] = fallback_tiers
    gdf['composite_note'] = fallback_notes

    summary = [
        f'\n=== {label} ===',
        f'  Total EDs: {len(gdf)}',
        f'  From v7 (primary): {len(gdf) - null_count}',
        f'  From v6 minority: {resolved_v6}',
        f'  From 2019 parent: {resolved_2019}',
        f'  Unresolvable: {len(unresolvable)}',
    ]
    if unresolvable:
        summary.append(f'  Unresolvable EDs: {unresolvable}')
    summary.extend(log)
    return gdf, summary

# ─── Compute summary stats ────────────────────────────────────────────────────

def summarize(gdf, label):
    lines = [f'\n--- {label} summary ---']
    null_remaining = gdf.geometry.isna().sum()
    lines.append(f'  Null geometries remaining: {null_remaining}')
    src_counts = gdf['composite_source'].value_counts()
    for src, cnt in src_counts.items():
        lines.append(f'  {src}: {cnt}')
    tier_counts = gdf['composite_tier'].value_counts()
    for tier, cnt in tier_counts.items():
        lines.append(f'  tier {tier}: {cnt}')
    return lines

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    log_lines = [
        '# Composite shapefile build log',
        f'Date: {datetime.now().isoformat()}',
        '',
        'Builds best-available 89-ED GeoPackages from v7 + 2019 parent fallbacks.',
        '',
    ]

    # ── Majority ──────────────────────────────────────────────────────────────
    print('Building majority composite...')
    maj_gdf, maj_log = build_composite(
        v7_path=os.path.join(DATA_DIR, 'v0_1_derived_v7_majority_2026_eds.gpkg'),
        fallback_map=MAJORITY_NULL_FALLBACK,
        label='Majority',
        v6_lookup=None,
    )
    log_lines.extend(maj_log)
    log_lines.extend(summarize(maj_gdf, 'Majority'))

    out_maj = os.path.join(DATA_DIR, 'v0_1_composite_majority_2026_eds.gpkg')
    maj_gdf.to_file(out_maj, driver='GPKG')
    print(f'  Written: {out_maj}')
    log_lines.append(f'\nOutput: {out_maj}')

    # ── Minority ──────────────────────────────────────────────────────────────
    print('Building minority composite...')
    v6_minority_lookup = load_v6_minority_lookup()

    min_gdf, min_log = build_composite(
        v7_path=os.path.join(DATA_DIR, 'v0_1_derived_v7_minority_2026_eds.gpkg'),
        fallback_map=MINORITY_NULL_FALLBACK,
        label='Minority',
        v6_lookup=v6_minority_lookup,
    )
    log_lines.extend(min_log)
    log_lines.extend(summarize(min_gdf, 'Minority'))

    out_min = os.path.join(DATA_DIR, 'v0_1_composite_minority_2026_eds.gpkg')
    min_gdf.to_file(out_min, driver='GPKG')
    print(f'  Written: {out_min}')
    log_lines.append(f'\nOutput: {out_min}')

    # ── Write log ─────────────────────────────────────────────────────────────
    log_path = os.path.join(ANALYSIS_DIR, 'v0_1_composite_shapefiles_log.md')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    print(f'  Log: {log_path}')

    # ── Verify null counts ────────────────────────────────────────────────────
    maj_null = maj_gdf.geometry.isna().sum()
    min_null = min_gdf.geometry.isna().sum()
    print(f'\nFinal null counts: majority={maj_null}, minority={min_null}')

    if maj_null > 0 or min_null > 0:
        print('WARNING: some EDs remain unresolvable')
        sys.exit(1)
    else:
        print('All 89 EDs resolved for both maps.')

if __name__ == '__main__':
    main()
