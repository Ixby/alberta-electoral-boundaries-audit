"""
v0_1_build_canonical_shapefiles.py
====================================
Builds authoritative canonical 89-ED GeoPackages for majority and minority maps.

For EDs where v7 produced null geometries due to overlap (two 2026 EDs sharing
one 2019 parent polygon), resolves the boundary using:

  1. Population-calibrated parametric sweep — finds the split-line orientation
     and position that best matches the commission's published population ratio
     between the two child EDs, using VA vote counts as a population proxy.

  2. Town-cluster assignment (Highwood only) — classifies VAs by nearest named
     town to handle the irregular multi-anchor Highwood split.

  3. Road-snap (best-effort) — snaps the best-fit split line to the nearest OSM
     rural road to exploit the Alberta land-use pattern where commission
     boundaries follow road allowances.

All other EDs use the priority hierarchy from the plan:
  v7 non-null > v6 minority (minority only) > 2019-direct > 2019-blend

Outputs:
  data/v0_1_canonical_majority_2026_eds.gpkg
  data/v0_1_canonical_minority_2026_eds.gpkg
  analysis/methodology/canonical_shapefile_log.md
"""
# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import math
import os
import sys
from collections import defaultdict
from datetime import datetime
from typing import Optional

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import split as shapely_split, unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(ROOT, 'data')
ANALYSIS_DIR = os.path.join(ROOT, 'analysis')
WORK_CRS = 3401  # Alberta 10-TM Forest

# ─── Population targets from commission report ────────────────────────────────

MAJ_POP = {
    'Airdrie-West': 48_145,
    'Cochrane-Springbank': 56_487,
    'High River-Vulcan-Siksika': 53_351,
    'Okotoks-Diamond Valley': 55_284,
    'St. Albert-Sturgeon': 54_214,
    'Leduc-Devon': 56_572,
}

# Overlap pairs: two 2026 EDs sharing one 2019 parent polygon
# Format: parent_2019 -> [(ed_a, ed_b), target_ratio_for_a]
MAJORITY_OVERLAP_PAIRS = {
    'Airdrie-Cochrane': (
        ['Airdrie-West', 'Cochrane-Springbank'],
        MAJ_POP['Airdrie-West'] / (MAJ_POP['Airdrie-West'] + MAJ_POP['Cochrane-Springbank']),
    ),
    'Highwood': (
        ['High River-Vulcan-Siksika', 'Okotoks-Diamond Valley'],
        MAJ_POP['High River-Vulcan-Siksika'] / (MAJ_POP['High River-Vulcan-Siksika'] + MAJ_POP['Okotoks-Diamond Valley']),
    ),
}

# Town centroids (EPSG:3401 approx) used for cluster approach in Highwood
# High River ~(79500, 5618500), Vulcan ~(105000, 5616000), Siksika far E
# Okotoks ~(63000, 5630000), Diamond Valley ~(48000, 5622000)
HIGHWOOD_CLUSTERS = {
    'Okotoks-Diamond Valley': [(63_000, 5_630_000), (48_000, 5_622_000)],
    'High River-Vulcan-Siksika': [(79_500, 5_618_500), (105_000, 5_616_000)],
}
AIRDRIE_CLUSTERS = {
    'Airdrie-West': [(52_000, 5_682_000)],       # Airdrie city centre (approx)
    'Cochrane-Springbank': [(34_000, 5_672_000)],  # Cochrane town centre (approx)
}

# ─── Parametric sweep ─────────────────────────────────────────────────────────

def split_polygon_by_line(polygon: Polygon, line: LineString) -> tuple[Polygon, Polygon]:
    """Split polygon by line; return (left/lower side, right/upper side)."""
    try:
        result = shapely_split(polygon, line)
        geoms = list(result.geoms) if hasattr(result, 'geoms') else [result]
        if len(geoms) < 2:
            return None, None
        # Sort by centroid x so 'a' is consistently left/west
        geoms.sort(key=lambda g: g.centroid.x)
        return geoms[0], geoms[-1]
    except Exception:
        return None, None


def make_split_line(angle_deg: float, position: float, bbox: tuple) -> LineString:
    """
    Create a split line through the bbox at the given angle (degrees from E)
    and position (0=one edge, 1=opposite edge along the perpendicular).

    The line is long enough to fully cross the bbox.
    """
    minx, miny, maxx, maxy = bbox
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2
    diag = math.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2) * 1.5

    rad = math.radians(angle_deg)
    # Normal direction
    nx, ny = math.sin(rad), -math.cos(rad)
    # Perpendicular direction (along the line)
    dx, dy = math.cos(rad), math.sin(rad)

    # Offset the centre by the position parameter
    perp_range = diag
    offset = (position - 0.5) * perp_range
    px = cx + nx * offset
    py = cy + ny * offset

    # Build a line crossing the entire bbox
    p1 = (px - dx * diag, py - dy * diag)
    p2 = (px + dx * diag, py + dy * diag)
    return LineString([p1, p2])


def classify_vas_by_line(
    va_centroids_xy: np.ndarray,
    angle_deg: float,
    position: float,
    bbox: tuple,
) -> np.ndarray:
    """
    Return boolean array: True = VA centroid is on the 'A' side of the split line.
    'A' side = lower-left side (smaller projection onto the normal direction).
    """
    minx, miny, maxx, maxy = bbox
    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2
    diag = math.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2) * 1.5

    rad = math.radians(angle_deg)
    nx, ny = math.sin(rad), -math.cos(rad)
    offset = (position - 0.5) * diag

    # Reference point on the line
    px = cx + nx * offset
    py = cy + ny * offset

    # Projection of each centroid onto the normal
    proj = (va_centroids_xy[:, 0] - px) * nx + (va_centroids_xy[:, 1] - py) * ny
    return proj < 0


def parametric_sweep(
    va_subset: gpd.GeoDataFrame,
    parent_polygon: Polygon,
    target_ratio: float,
    n_angles: int = 8,
    n_positions: int = 40,
    log: list = None,
) -> tuple[Optional[LineString], float, float, str]:
    """
    Sweep split lines across the parent polygon; return the line that best
    matches target_ratio using VA votes as population proxy.

    Returns (best_line, achieved_ratio, best_score, description).
    """
    if len(va_subset) == 0:
        return None, 0.0, 1.0, 'no VAs in parent'

    centroids = np.array([(g.centroid.x, g.centroid.y) for g in va_subset.geometry])
    total_votes = (va_subset['va_ndp'] + va_subset['va_ucp'] + va_subset['va_other']).values
    total = total_votes.sum()
    if total == 0:
        return None, 0.0, 1.0, 'zero vote total'

    bbox = parent_polygon.bounds  # minx, miny, maxx, maxy

    # Angles: 0=N-S, 45=NE-SW, 90=E-W, 135=NW-SE, etc.
    angles = np.linspace(0, 180, n_angles, endpoint=False)
    positions = np.linspace(0.1, 0.9, n_positions)

    best_score = 1.0
    best_line = None
    best_ratio = 0.0
    best_desc = ''

    for angle in angles:
        for pos in positions:
            mask = classify_vas_by_line(centroids, angle, pos, bbox)
            votes_a = total_votes[mask].sum()
            ratio = votes_a / total if total > 0 else 0
            score = abs(ratio - target_ratio)
            if score < best_score:
                best_score = score
                best_ratio = ratio
                best_line = make_split_line(angle, pos, bbox)
                best_desc = f'angle={angle:.0f}° pos={pos:.2f}'

    if log is not None:
        log.append(f'    sweep: best_score={best_score:.4f}, achieved_ratio={best_ratio:.3f}, '
                   f'target={target_ratio:.3f}, {best_desc}')

    return best_line, best_ratio, best_score, best_desc


# ─── Town-cluster approach (Highwood) ─────────────────────────────────────────

def classify_by_nearest_town(
    va_subset: gpd.GeoDataFrame,
    cluster_centres: dict,  # ed_name -> [(x, y), ...]
) -> dict:
    """
    Classify each VA by which ED's town centres are closest.
    Returns dict: ed_name -> GeoDataFrame subset.
    """
    ed_names = list(cluster_centres.keys())
    centroids = np.array([(g.centroid.x, g.centroid.y) for g in va_subset.geometry])

    # For each VA, compute minimum distance to any town in each cluster
    min_dist = {ed: np.inf * np.ones(len(va_subset)) for ed in ed_names}
    for ed, towns in cluster_centres.items():
        for tx, ty in towns:
            dist = np.sqrt((centroids[:, 0] - tx) ** 2 + (centroids[:, 1] - ty) ** 2)
            min_dist[ed] = np.minimum(min_dist[ed], dist)

    # Assign each VA to the ED with the nearest town centre
    assignments = {}
    for i in range(len(va_subset)):
        nearest_ed = min(ed_names, key=lambda ed: min_dist[ed][i])
        assignments.setdefault(nearest_ed, [])
        assignments[nearest_ed].append(i)

    return {ed: va_subset.iloc[idxs] for ed, idxs in assignments.items()}


def hull_from_vas(va_subset: gpd.GeoDataFrame, parent_polygon: Polygon) -> Polygon:
    """Union VA polygons and intersect with parent polygon."""
    if len(va_subset) == 0:
        return Polygon()
    union = unary_union(va_subset.geometry)
    return union.intersection(parent_polygon)


# ─── Road-snap (best-effort via OSM) ──────────────────────────────────────────

def road_snap(
    split_line: LineString,
    parent_polygon: Polygon,
    buffer_m: float = 5000,
    log: list = None,
) -> LineString:
    """
    Attempt to snap the split line to the nearest OSM road within buffer_m.
    Extends the road's direction into a full crossing line so it can split
    the parent polygon.
    Returns the original line if OSM is unavailable or no road is found.
    """
    try:
        import osmnx as ox
        import pyproj

        bbox_geom = split_line.buffer(buffer_m).intersection(parent_polygon)
        minx, miny, maxx, maxy = bbox_geom.bounds  # EPSG:3401

        # Convert from EPSG:3401 to WGS84 for osmnx
        transformer = pyproj.Transformer.from_crs(3401, 4326, always_xy=True)
        # always_xy=True: transform(x, y) -> (lon, lat)
        lon_w, lat_s = transformer.transform(minx, miny)
        lon_e, lat_n = transformer.transform(maxx, maxy)

        # osmnx v2 bbox=(left, bottom, right, top) = (west, south, east, north)
        G = ox.graph_from_bbox(
            bbox=(lon_w, lat_s, lon_e, lat_n),
            network_type='all',
            retain_all=False,
            simplify=True,
        )
        edges = ox.graph_to_gdfs(G, nodes=False)
        edges_proj = edges.to_crs(epsg=3401)

        # Find the edge closest to the split line midpoint
        split_mid = split_line.interpolate(0.5, normalized=True)
        edges_proj['dist_to_split'] = edges_proj.geometry.distance(split_mid)
        nearest = edges_proj.nsmallest(1, 'dist_to_split').iloc[0]
        snap_dist = nearest['dist_to_split']

        if snap_dist > buffer_m:
            if log:
                log.append(f'    road-snap: nearest road {snap_dist:.0f} m > buffer {buffer_m:.0f} m, no snap')
            return split_line

        road_geom = nearest.geometry
        coords = list(road_geom.coords)
        if len(coords) < 2:
            if log:
                log.append('    road-snap: degenerate road edge, skipping')
            return split_line

        # Use first and last coord to get road direction; extend to span parent polygon
        x0, y0 = coords[0]
        x1, y1 = coords[-1]
        dx = x1 - x0
        dy = y1 - y0
        length = math.sqrt(dx * dx + dy * dy)
        if length < 1:
            return split_line
        dx /= length
        dy /= length

        # Anchor at the nearest point on the road to the split-line midpoint
        nearest_pt = road_geom.interpolate(road_geom.project(split_mid))
        ax, ay = nearest_pt.x, nearest_pt.y

        # Extend the line well past the parent polygon bounds
        diag = math.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2) * 2
        extended = LineString([
            (ax - dx * diag, ay - dy * diag),
            (ax + dx * diag, ay + dy * diag),
        ])

        if log:
            log.append(f'    road-snap: found road at {snap_dist:.0f} m, extended to crossing line '
                       f'(direction {math.degrees(math.atan2(dy, dx)):.0f}°)')
        return extended

    except ImportError:
        if log:
            log.append('    road-snap: osmnx not available, skipping')
    except Exception as e:
        if log:
            log.append(f'    road-snap: failed ({e}), skipping')
    return split_line


# ─── Sensitivity analysis ─────────────────────────────────────────────────────

def sensitivity_analysis(
    va_subset: gpd.GeoDataFrame,
    parent_polygon: Polygon,
    target_ratio: float,
    envelope_tol: float = 0.05,
    n_angles: int = 8,
    n_positions: int = 40,
) -> dict:
    """
    Find all (angle, pos) pairs within envelope_tol of target_ratio.
    Return vote-total range for side-A across that envelope.
    """
    if len(va_subset) == 0:
        return {}

    centroids = np.array([(g.centroid.x, g.centroid.y) for g in va_subset.geometry])
    total_votes = (va_subset['va_ndp'] + va_subset['va_ucp'] + va_subset['va_other']).values
    total = total_votes.sum()
    bbox = parent_polygon.bounds
    angles = np.linspace(0, 180, n_angles, endpoint=False)
    positions = np.linspace(0.1, 0.9, n_positions)

    envelope_ratios = []
    for angle in angles:
        for pos in positions:
            mask = classify_vas_by_line(centroids, angle, pos, bbox)
            ratio = total_votes[mask].sum() / total if total > 0 else 0
            if abs(ratio - target_ratio) <= envelope_tol:
                envelope_ratios.append(ratio)

    if not envelope_ratios:
        return {'n_in_envelope': 0}
    return {
        'n_in_envelope': len(envelope_ratios),
        'ratio_min': min(envelope_ratios),
        'ratio_max': max(envelope_ratios),
        'ratio_mean': np.mean(envelope_ratios),
    }


# ─── Main canonical builder ───────────────────────────────────────────────────

def load_data():
    va = gpd.read_file(os.path.join(DATA_DIR, 'va_polygons_with_2023_votes.gpkg'))
    va = va.to_crs(epsg=WORK_CRS)

    eds_2019 = gpd.read_file(
        os.path.join(DATA_DIR, 'alberta_2019_eds', 'EDS_ENACTED_BILL33_15DEC2017.shp')
    )
    # Already EPSG:3401

    v7_maj = gpd.read_file(os.path.join(DATA_DIR, 'v0_1_derived_v7_majority_2026_eds.gpkg'))
    v7_min = gpd.read_file(os.path.join(DATA_DIR, 'v0_1_derived_v7_minority_2026_eds.gpkg'))
    v6_min = gpd.read_file(os.path.join(DATA_DIR, 'v0_1_refined_v6_minority_2026_eds.gpkg'))

    for gdf in [v7_maj, v7_min, v6_min]:
        if gdf.crs and gdf.crs.to_epsg() != WORK_CRS:
            gdf = gdf.to_crs(epsg=WORK_CRS)

    eds_2019_lookup = dict(zip(eds_2019['EDName2017'], eds_2019['geometry']))

    maj_pop = pd.read_csv(os.path.join(DATA_DIR, 'majority_2026_populations.csv'))
    maj_pop_lookup = dict(zip(maj_pop['ed_name'], maj_pop['population']))

    return va, eds_2019_lookup, v7_maj, v7_min, v6_min, maj_pop_lookup


MAJORITY_FALLBACK = {
    'Calgary-Confluence':            ('Calgary-Buffalo',             'direct'),
    'Calgary-Nose Creek':            ('Calgary-Beddington',          'direct'),
    'Edmonton-Windermere':           ('Edmonton-South West',         'direct'),
    'Airdrie-East':                  ('Airdrie-East',                'direct'),
    'Barrhead-Westlock-Athabasca':   ('Athabasca-Barrhead-Westlock', 'direct'),
    'Canmore-Banff':                 ('Banff-Kananaskis',            'direct'),
    'Chestermere-Strathmore':        ('Chestermere-Strathmore',      'direct'),
    'Cold Lake-Bonnyville-St. Paul': ('Bonnyville-Cold Lake-St. Paul','direct'),
    'Fort McMurray-Lac La Biche':    ('Fort McMurray-Lac La Biche',  'direct'),
    'Medicine Hat-Brooks':           ('Brooks-Medicine Hat',         'direct'),
    'Mountain View-Kneehill':        ('Olds-Didsbury-Three Hills',   'direct'),
    'Stony Plain-Drayton Valley':    ('Drayton Valley-Devon',        'direct'),
    'Sylvan Lake-Innisfail':         ('Innisfail-Sylvan Lake',       'direct'),
    'Taber-Cardston':                ('Taber-Warner',                'direct'),
    # Blend cases where 2019 name = 2026 name (treated as direct)
    'Lethbridge-East':               ('Lethbridge-East',             'direct'),
    'Lethbridge-West':               ('Lethbridge-West',             'direct'),
    # True blend fallbacks (2019 parent overcovers)
    'St. Albert-Sturgeon':           ('Morinville-St. Albert',       'blend'),
    'Leduc-Devon':                   ('Leduc-Beaumont',              'blend'),
}

MINORITY_FALLBACK = {
    'Calgary-Airdrie':              ('Airdrie-Cochrane',     'split'),
    'Calgary-McCall-Bhullar':       ('Calgary-McCall',       'direct'),
    'Calgary-North West-Bearspaw':  ('Calgary-North West',   'blend'),
    "Calgary-West-Tsuut'ina":       ('Calgary-West',         'blend'),
    'St. Albert-Sturgeon':          ('Morinville-St. Albert','blend'),
}


def resolve_overlap_pair(
    parent_name: str,
    ed_names: list,
    target_ratio: float,
    va: gpd.GeoDataFrame,
    eds_2019_lookup: dict,
    log: list,
    use_cluster: bool = False,
    cluster_centres: dict = None,
) -> dict:
    """
    Resolve two 2026 EDs that share one 2019 parent polygon.
    Returns dict: ed_name -> (polygon, tier, note, sensitivity_info).
    """
    parent_polygon = eds_2019_lookup.get(parent_name)
    if parent_polygon is None:
        log.append(f'  ERROR: {parent_name} not found in 2019 lookup')
        return {ed: (None, 'unresolvable', 'parent not found', {}) for ed in ed_names}

    va_sub = va[va['parent_ed_2019'] == parent_name].copy()
    log.append(f'\n  Resolving {parent_name} -> {ed_names}')
    log.append(f'    VAs: {len(va_sub)}, target_ratio(A): {target_ratio:.3f}')

    if use_cluster and cluster_centres:
        # Town-cluster approach
        log.append('    Using town-cluster approach')
        clusters = classify_by_nearest_town(va_sub, cluster_centres)
        results = {}
        for i, ed in enumerate(ed_names):
            va_cluster = clusters.get(ed, va_sub.iloc[:0])
            poly = hull_from_vas(va_cluster, parent_polygon)
            votes_a = (va_cluster['va_ndp'] + va_cluster['va_ucp'] + va_cluster['va_other']).sum()
            total_v = (va_sub['va_ndp'] + va_sub['va_ucp'] + va_sub['va_other']).sum()
            achieved = votes_a / total_v if total_v > 0 else 0
            log.append(f'    {ed}: {len(va_cluster)} VAs, achieved_ratio={achieved:.3f}')
            results[ed] = (poly, 'C-sweep-cluster', f'Town-cluster from {parent_name}; VA ratio {achieved:.3f}', {})

        # Run parametric sweep as validation/fallback
        best_line, achieved, score, desc = parametric_sweep(
            va_sub, parent_polygon, target_ratio, log=log
        )
        log.append(f'    Parametric sweep (validation): score={score:.4f}, ratio={achieved:.3f}')

        # Use cluster if it achieves a better population ratio
        cluster_ed_a = ed_names[0]
        va_a = clusters.get(cluster_ed_a, va_sub.iloc[:0])
        total_v = (va_sub['va_ndp'] + va_sub['va_ucp'] + va_sub['va_other']).sum()
        cluster_ratio = (va_a['va_ndp'] + va_a['va_ucp'] + va_a['va_other']).sum() / total_v if total_v > 0 else 0
        cluster_score = abs(cluster_ratio - target_ratio)

        if cluster_score <= score:
            log.append(f'    Cluster approach wins (score {cluster_score:.4f} <= sweep {score:.4f})')
            return results
        else:
            log.append(f'    Sweep wins (score {score:.4f} < cluster {cluster_score:.4f}); falling back to sweep')
            # Fall through to sweep-based split below

    # Parametric sweep
    best_line, achieved, score, desc = parametric_sweep(
        va_sub, parent_polygon, target_ratio, n_angles=12, n_positions=50, log=log
    )

    if best_line is None:
        log.append(f'    WARN: sweep produced no line, using parent polygon fallback')
        return {ed: (parent_polygon, 'C-2019-blend', f'Fallback: {parent_name} (sweep failed)', {})
                for ed in ed_names}

    # Road-snap
    snapped_line = road_snap(best_line, parent_polygon, buffer_m=5000, log=log)

    # Split parent polygon
    poly_a, poly_b = split_polygon_by_line(parent_polygon, snapped_line)
    if poly_a is None:
        # Try with un-snapped line
        poly_a, poly_b = split_polygon_by_line(parent_polygon, best_line)
    if poly_a is None:
        log.append(f'    WARN: polygon split failed, using parent polygon fallback')
        return {ed: (parent_polygon, 'C-2019-blend', f'Fallback: {parent_name} (split failed)', {})
                for ed in ed_names}

    # Check which split_polygon side matches ed_names[0]
    # The side with the lower x-centroid is poly_a (west side)
    # For Airdrie-West, Airdrie is north/east of Cochrane... use vote ratio to decide
    va_in_a = va_sub[va_sub.geometry.centroid.within(poly_a)]
    ratio_a = (va_in_a['va_ndp'] + va_in_a['va_ucp'] + va_in_a['va_other']).sum() / \
              (va_sub['va_ndp'] + va_sub['va_ucp'] + va_sub['va_other']).sum()

    if abs(ratio_a - target_ratio) < abs((1 - ratio_a) - target_ratio):
        # poly_a corresponds to ed_names[0]
        poly_map = {ed_names[0]: poly_a, ed_names[1]: poly_b}
        note_a = f'Sweep-split from {parent_name}; ratio {ratio_a:.3f} (target {target_ratio:.3f})'
        note_b = f'Sweep-split from {parent_name}; ratio {1-ratio_a:.3f} (target {1-target_ratio:.3f})'
    else:
        # poly_b corresponds to ed_names[0]
        poly_map = {ed_names[0]: poly_b, ed_names[1]: poly_a}
        note_a = f'Sweep-split from {parent_name}; ratio {1-ratio_a:.3f} (target {target_ratio:.3f})'
        note_b = f'Sweep-split from {parent_name}; ratio {ratio_a:.3f} (target {1-target_ratio:.3f})'

    # Sensitivity analysis
    sens = sensitivity_analysis(va_sub, parent_polygon, target_ratio)
    log.append(f'    Sensitivity: {sens}')

    return {
        ed_names[0]: (poly_map[ed_names[0]], 'C-sweep', note_a, sens),
        ed_names[1]: (poly_map[ed_names[1]], 'C-sweep', note_b, {}),
    }


def build_canonical(v7: gpd.GeoDataFrame, fallback_map: dict, eds_2019_lookup: dict,
                    va: gpd.GeoDataFrame, v6_lookup: dict, map_label: str, log: list,
                    overlap_resolutions: dict) -> gpd.GeoDataFrame:
    """Build canonical GeoDataFrame from v7 + resolved overlaps + fallbacks."""
    if v7.crs and v7.crs.to_epsg() != WORK_CRS:
        v7 = v7.to_crs(epsg=WORK_CRS)

    rows = []
    for _, row in v7.iterrows():
        name = row['name_2026']
        geom = row.geometry
        tier = row.get('tier_2026', '')
        source = 'v7'

        # Check if this ED is part of an overlap resolution
        if name in overlap_resolutions:
            geom, tier, note, _ = overlap_resolutions[name]
            source = 'sweep'
        elif geom is None or (hasattr(geom, 'is_empty') and geom.is_empty):
            # Try v6 minority lookup
            if name in v6_lookup:
                geom = v6_lookup[name]
                tier = 'C-v6-fallback'
                source = 'v6'
                note = 'v6 minority 70-ED file'
            elif name in fallback_map:
                parent, rel = fallback_map[name]
                geom = eds_2019_lookup.get(parent)
                tier = f'C-2019-{rel}'
                source = '2019-parent'
                note = f'2019 parent: {parent} ({rel})'
            else:
                tier = 'unresolvable'
                source = 'unresolvable'
                note = 'No fallback defined'
        else:
            note = ''

        rows.append({
            'name_2026': name,
            'map': map_label,
            'canon_tier': tier if tier else 'unknown',
            'canon_source': source,
            'canon_note': note,
            'geometry': geom,
        })

    gdf = gpd.GeoDataFrame(rows, crs=f'EPSG:{WORK_CRS}')
    return gdf


def main():
    log = [f'# Canonical shapefile build log', f'Date: {datetime.now().isoformat()}', '']

    print('Loading data...')
    va, eds_2019_lookup, v7_maj, v7_min, v6_min, maj_pop_lookup = load_data()

    v6_min_lookup = dict(zip(v6_min['name_2026'], v6_min['geometry']))

    # ── Resolve majority overlap pairs ────────────────────────────────────────
    log.append('\n## Majority overlap pair resolution')
    overlap_resolutions_maj = {}

    for parent_name, (ed_names, target_ratio) in MAJORITY_OVERLAP_PAIRS.items():
        use_cluster = (parent_name == 'Highwood')
        cluster_centres = HIGHWOOD_CLUSTERS if parent_name == 'Highwood' else AIRDRIE_CLUSTERS

        resolved = resolve_overlap_pair(
            parent_name, ed_names, target_ratio, va, eds_2019_lookup, log,
            use_cluster=use_cluster, cluster_centres=cluster_centres,
        )
        overlap_resolutions_maj.update(resolved)

    # ── Build majority canonical ───────────────────────────────────────────────
    log.append('\n## Building majority canonical')
    maj_gdf = build_canonical(
        v7_maj, MAJORITY_FALLBACK, eds_2019_lookup, va, {}, 'majority', log,
        overlap_resolutions_maj
    )

    # ── Build minority canonical ───────────────────────────────────────────────
    log.append('\n## Building minority canonical')
    min_gdf = build_canonical(
        v7_min, MINORITY_FALLBACK, eds_2019_lookup, va, v6_min_lookup, 'minority', log,
        {}
    )

    # ── Summary stats ─────────────────────────────────────────────────────────
    for label, gdf in [('Majority', maj_gdf), ('Minority', min_gdf)]:
        null_count = gdf.geometry.isna().sum()
        log.append(f'\n### {label} summary')
        log.append(f'  Total EDs: {len(gdf)}, null geometry: {null_count}')
        for src, cnt in gdf['canon_source'].value_counts().items():
            log.append(f'  {src}: {cnt}')
        for tier, cnt in gdf['canon_tier'].value_counts().items():
            log.append(f'  tier {tier}: {cnt}')

    # ── Verify no overlapping polygons ────────────────────────────────────────
    log.append('\n## Overlap check (majority)')
    sweep_eds = maj_gdf[maj_gdf['canon_source'] == 'sweep']
    if len(sweep_eds) == 4:
        pairs = list(sweep_eds['name_2026'])
        for i in range(len(pairs)):
            for j in range(i+1, len(pairs)):
                g1 = sweep_eds[sweep_eds['name_2026'] == pairs[i]].geometry.iloc[0]
                g2 = sweep_eds[sweep_eds['name_2026'] == pairs[j]].geometry.iloc[0]
                if g1 and g2 and not g1.is_empty and not g2.is_empty:
                    overlap = g1.intersection(g2).area / 1e6
                    log.append(f'  {pairs[i]} ∩ {pairs[j]}: {overlap:.2f} km²')

    # ── Write outputs ─────────────────────────────────────────────────────────
    out_maj = os.path.join(DATA_DIR, 'v0_1_canonical_majority_2026_eds.gpkg')
    out_min = os.path.join(DATA_DIR, 'v0_1_canonical_minority_2026_eds.gpkg')
    maj_gdf.to_file(out_maj, driver='GPKG')
    min_gdf.to_file(out_min, driver='GPKG')
    print(f'Written: {out_maj}')
    print(f'Written: {out_min}')

    log_path = os.path.join(ANALYSIS_DIR, 'canonical_shapefile_log.md')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log))
    print(f'Log: {log_path}')

    # Final checks
    maj_null = maj_gdf.geometry.isna().sum()
    min_null = min_gdf.geometry.isna().sum()
    print(f'\nFinal null counts: majority={maj_null}, minority={min_null}')
    sweep_count = (maj_gdf['canon_source'] == 'sweep').sum()
    print(f'Sweep-resolved overlap EDs: {sweep_count} (expected 4)')

    if maj_null > 0:
        print('WARNING: majority has null geometries')
    if min_null > 0:
        print('WARNING: minority has null geometries')


if __name__ == '__main__':
    main()
