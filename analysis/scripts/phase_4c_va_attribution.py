"""
Phase 4C — Measured VA-level vote attribution for 2026 ED maps
==============================================================
Replaces the v0.2 proportional-estimate (70/30 blend) approach with
spatially-measured VA-level assignment. Each of 4,765 VAs is assigned
to its correct 2026 ED in both the majority and minority maps, then
votes are aggregated at VA resolution.

Assignment method hierarchy (per map):
  1. Spatial: VA centroid falls inside a 2026 ED polygon from
     approximate/refined shapefiles. Highest confidence.
  2. Candidate: VA is flagged with a specific 2026 ED candidate in
     hybrid_adjacent_vas.csv. Used when spatial fails.
  3. Crosswalk: VA's parent 2019 ED maps 1:1 to a 2026 ED via the
     inverted v0.2 mapping. Used when spatial and candidate both fail.
  4. Default-split: For 2019 EDs that split into multiple 2026 EDs,
     unflagged VAs go to the "default" (first-listed) 2026 ED.

Inputs:
  data/va_polygons_with_2023_votes.gpkg
  data/hybrid_adjacent_vas.csv
  data/v0_1_approximate_majority_2026_eds.gpkg
  data/v0_1_refined_v4_minority_2026_eds.gpkg

Outputs:
  analysis/phase_4c_va_to_2026_assignments.csv
  analysis/phase_4c_2026_synthetic_totals.csv
"""
# Version: 0.1 series  (last updated 2026-04-26)


import os
import sys
import csv
import math
import statistics
import warnings
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.errors import GEOSException

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*GEOSException.*')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
# Import the v0.2 mappings to invert them
sys.path.insert(0, HERE)
from v0_2_packing_cracking_analysis import MAJORITY_2026_MAPPING, MINORITY_2026_MAPPING


# =====================================================================
# 1. Build reverse crosswalks from v0.2 mappings
# =====================================================================

def invert_mapping(mapping):
    """
    Invert a 2026->2019 mapping to get 2019->list[2026].
    Each 2019 ED may map to multiple 2026 EDs (splits).
    """
    reverse = {}
    for ed_2026, spec in mapping.items():
        kind = spec[0]
        if kind in ('direct', 'blend', 'split'):
            parent = spec[1]
            reverse.setdefault(parent, []).append(ed_2026)
        elif kind == 'merge':
            for parent in spec[1]:
                reverse.setdefault(parent, []).append(ed_2026)
    return reverse

MAJ_REVERSE = invert_mapping(MAJORITY_2026_MAPPING)
MIN_REVERSE = invert_mapping(MINORITY_2026_MAPPING)

# Expected ED counts
EXPECTED_MAJORITY_N = len(MAJORITY_2026_MAPPING)  # 89
EXPECTED_MINORITY_N = len(MINORITY_2026_MAPPING)  # 89


# =====================================================================
# 2. Load data
# =====================================================================

def load_va_polygons():
    path = os.path.join(ROOT, 'data', 'va_polygons_with_2023_votes.gpkg')
    va = gpd.read_file(path)
    va['va_id'] = va['parent_ed_2019'] + '|' + va['VA_NUMBER'].astype(str).str.zfill(3)
    return va

def load_flagged_vas():
    path = os.path.join(ROOT, 'data', 'hybrid_adjacent_vas.csv')
    return pd.read_csv(path)

def load_2026_shapefiles():
    maj_path = os.path.join(ROOT, 'data', 'v0_1_canonical_majority_2026_eds.gpkg')
    min_path = os.path.join(ROOT, 'data', 'v0_1_canonical_minority_2026_eds.gpkg')
    return gpd.read_file(maj_path), gpd.read_file(min_path)


# =====================================================================
# 3. Assignment logic — spatial-first
# =====================================================================

def assign_vas_spatial_first(va_gdf, flagged_df, eds_2026_gdf,
                             reverse_map, forward_map,
                             candidate_col, map_label):
    """
    Assign each VA to a 2026 ED using a spatial-first strategy.

    1. Spatial: centroid-in-polygon against the 2026 shapefile
    2. Candidate: use the flagged VA's candidate column
    3. Crosswalk: use the reverse mapping (2019 -> first 2026 target)

    Returns (assignments_df, stats_dict).
    """
    # Build flagged lookup
    flagged_set = set(flagged_df['va_id'].tolist())
    flagged_candidates = {}
    for _, row in flagged_df.iterrows():
        cand = row[candidate_col]
        if pd.notna(cand):
            flagged_candidates[row['va_id']] = [c.strip() for c in str(cand).split(';')]

    # Compute VA centroids
    va_centroids = va_gdf.copy()
    va_centroids['centroid'] = va_centroids.geometry.centroid
    va_centroids_gdf = va_centroids.set_geometry('centroid')

    # Spatial join: which 2026 ED contains each VA centroid?
    print(f"  Performing spatial join ({len(va_centroids_gdf)} VAs x {len(eds_2026_gdf)} EDs)...")
    joined = gpd.sjoin(
        va_centroids_gdf[['va_id', 'parent_ed_2019', 'va_ndp', 'va_ucp', 'va_other', 'centroid']],
        eds_2026_gdf[['name_2026', 'geometry']],
        how='left',
        predicate='within'
    )

    # Handle VAs that matched multiple 2026 EDs (shouldn't happen with non-overlapping polygons,
    # but clean up just in case)
    # Keep the first match per VA
    joined = joined.drop_duplicates(subset='va_id', keep='first')

    # Build spatial assignment lookup
    spatial_assignments = {}
    for _, row in joined.iterrows():
        if pd.notna(row.get('name_2026')):
            spatial_assignments[row['va_id']] = {
                'ed': row['name_2026'],
                'tier': row.get('canon_tier', row.get('tier', 'A')),
            }

    # All expected 2026 ED names
    expected_eds = set(forward_map.keys())

    # Build a "direct override" set: 2019 parent EDs that map 1:1 (exclusively)
    # to a same-named 2026 ED via 'direct' mapping. For these, the crosswalk is
    # authoritative — a pixel-extraction boundary shift should not reassign VAs
    # whose 2019 territory is definitionally the same as the 2026 territory.
    # Only applies when the 2019 parent maps to exactly ONE 2026 ED; if it feeds
    # multiple 2026 EDs (split/rename+new), spatial must distinguish between them.
    parent_ed_count = {}  # count how many 2026 EDs each 2019 parent feeds
    for ed_2026, spec in forward_map.items():
        if spec[0] in ('direct', 'blend', 'split'):
            parent_ed_count.setdefault(spec[1], []).append(ed_2026)
        elif spec[0] == 'merge':
            for p in spec[1]:
                parent_ed_count.setdefault(p, []).append(ed_2026)

    direct_override = {}  # parent_2019 -> ed_2026
    for ed_2026, spec in forward_map.items():
        if spec[0] == 'direct' and spec[1] == ed_2026:
            parent = spec[1]
            if len(parent_ed_count.get(parent, [])) == 1:
                direct_override[parent] = ed_2026

    # Now assign each VA
    results = []
    stats = {'spatial': 0, 'candidate': 0, 'crosswalk': 0, 'nearest_ed': 0, 'unresolved': 0}

    for idx, va_row in va_gdf.iterrows():
        va_id = va_row['va_id']
        parent = va_row['parent_ed_2019']
        ndp = va_row['va_ndp']
        ucp = va_row['va_ucp']
        other = va_row['va_other']

        assigned = None
        method = None
        confidence = 'high'

        # Method 0: Direct-rename override (crosswalk beats spatial)
        # When the 2019 parent name == 2026 ED name (territory-identical rename),
        # trust the crosswalk over spatial — a pixel-extraction boundary shift
        # in the canonical file can cause VAs to fall in the wrong polygon.
        if parent in direct_override:
            assigned = direct_override[parent]
            method = 'crosswalk'
            confidence = 'high'

        # Method 1: Spatial (only for non-direct or unresolved direct cases)
        if assigned is None and va_id in spatial_assignments:
            sp = spatial_assignments[va_id]
            assigned = sp['ed']
            method = 'spatial'
            if sp['tier'] == 'C-approximated':
                confidence = 'deferred_tierC'
            elif sp['tier'] == 'B':
                confidence = 'medium'
            else:
                confidence = 'high'

        # Method 2: Candidate from flagged VAs
        if assigned is None and va_id in flagged_candidates:
            candidates = flagged_candidates[va_id]
            # Pick the first candidate that's a valid 2026 ED
            for c in candidates:
                if c in expected_eds:
                    assigned = c
                    method = 'candidate'
                    confidence = 'medium'
                    break

        # Method 3: Crosswalk (reverse map)
        if assigned is None:
            targets = reverse_map.get(parent, [])
            if len(targets) == 1:
                assigned = targets[0]
                method = 'crosswalk'
                confidence = 'high'
            elif len(targets) > 1:
                # Split case — assign to first target (default)
                assigned = targets[0]
                method = 'crosswalk_split_default'
                confidence = 'medium'
            # else: fall through to nearest-ED below

        # Method 4: Nearest-ED geographic fallback
        # Fires when spatial, candidate, and crosswalk all fail (e.g. VA's 2019
        # parent ED name doesn't appear in any 2026 ED's crosswalk entry, and
        # the centroid missed all 2026 canonical polygons).
        if assigned is None:
            va_geom = va_gdf.loc[idx, 'geometry']
            cent = va_geom.centroid if va_geom and not va_geom.is_empty else None
            if cent is not None:
                dists = eds_2026_gdf.geometry.distance(cent)
                nearest_idx = dists.idxmin()
                assigned = eds_2026_gdf.loc[nearest_idx, 'name_2026']
                method = 'nearest_ed'
                confidence = 'low'
            else:
                assigned = parent
                method = 'unresolved'
                confidence = 'low'

        stats[method if method in stats else 'unresolved'] += 1

        results.append({
            'va_id': va_id, 'parent_ed_2019': parent,
            'assigned_2026': assigned,
            'va_ndp': ndp, 'va_ucp': ucp, 'va_other': other,
            'assignment_method': method,
            'confidence': confidence,
        })

    # Report
    print(f"\n  {map_label.upper()} assignment breakdown:")
    for k, v in sorted(stats.items()):
        if v > 0:
            print(f"    {k:<25s}: {v:>5d}")
    print(f"    {'TOTAL':<25s}: {len(results):>5d}")

    # Check how many unique 2026 EDs we got
    result_df = pd.DataFrame(results)
    unique_eds = result_df['assigned_2026'].nunique()
    print(f"\n  Unique 2026 EDs assigned: {unique_eds} (expected: {len(expected_eds)})")

    # Report missing and extra EDs
    actual_eds = set(result_df['assigned_2026'].unique())
    missing = expected_eds - actual_eds
    extra = actual_eds - expected_eds
    if missing:
        print(f"  Missing 2026 EDs (no VAs assigned):")
        for e in sorted(missing):
            print(f"    {e}")
    if extra:
        print(f"  Extra EDs (not in expected set):")
        for e in sorted(extra):
            count = (result_df['assigned_2026'] == e).sum()
            print(f"    {e} ({count} VAs)")

    return result_df, stats


# =====================================================================
# 4. Aggregation and metrics
# =====================================================================

def aggregate_by_ed(assignments_df):
    grouped = assignments_df.groupby('assigned_2026').agg(
        ndp=('va_ndp', 'sum'),
        ucp=('va_ucp', 'sum'),
        other=('va_other', 'sum'),
        n_vas=('va_id', 'count'),
    ).reset_index()
    grouped.rename(columns={'assigned_2026': 'ed_2026'}, inplace=True)
    return grouped


def compute_metrics(districts_df, label, verbose=True):
    n = len(districts_df)
    total_ndp = districts_df['ndp'].sum()
    total_ucp = districts_df['ucp'].sum()
    total = total_ndp + total_ucp
    prov_ndp = total_ndp / total

    n_ndp_wins = int((districts_df['ndp'] > districts_df['ucp']).sum())
    n_ucp_wins = n - n_ndp_wins

    margins = ((districts_df['ndp'] - districts_df['ucp']) /
               (districts_df['ndp'] + districts_df['ucp']) * 100).tolist()
    bins = [(-100,-25), (-25,-15), (-15,-10), (-10,-5), (-5,0),
            (0,5), (5,10), (10,15), (15,25), (25,100)]
    bin_counts = [sum(1 for m in margins if lo <= m < hi) for lo, hi in bins]

    # B2: Efficiency gap
    ndp_wasted = ucp_wasted = 0
    for _, d in districts_df.iterrows():
        tt = d['ndp'] + d['ucp']
        thr = tt // 2 + 1
        if d['ndp'] > d['ucp']:
            ndp_wasted += max(0, d['ndp'] - thr)
            ucp_wasted += d['ucp']
        else:
            ucp_wasted += max(0, d['ucp'] - thr)
            ndp_wasted += d['ndp']
    eg = (ndp_wasted - ucp_wasted) / total

    # B3: Mean-median
    shares = (districts_df['ndp'] / (districts_df['ndp'] + districts_df['ucp'])).tolist()
    mn = statistics.mean(shares)
    md = statistics.median(shares)
    mm_gap = mn - md

    # B4: 50/50 uniform swing
    swing = 0.5 - prov_ndp
    swung = [s + swing for s in shares]
    ndp_at_50 = sum(1 for s in swung if s > 0.5)
    ucp_at_50 = n - ndp_at_50

    # B6: Declination
    ndp_won_shares = [s for s in shares if s > 0.5]
    ucp_won_shares = [s for s in shares if s < 0.5]
    if ndp_won_shares and ucp_won_shares:
        mean_ndp_won = statistics.mean(ndp_won_shares)
        mean_ucp_won = statistics.mean(ucp_won_shares)
        theta_ndp = math.atan2(mean_ndp_won - 0.5, n_ndp_wins / n)
        theta_ucp = math.atan2(0.5 - mean_ucp_won, n_ucp_wins / n)
        declination = (theta_ndp - theta_ucp) * 2 / math.pi
    else:
        declination = float('nan')

    if verbose:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")
        print(f"  Districts: {n}")
        print(f"  Province two-party: NDP {prov_ndp*100:.2f}%, UCP {(1-prov_ndp)*100:.2f}%")
        print(f"  Actual seats: NDP {n_ndp_wins}, UCP {n_ucp_wins}")
        labels_list = ['UCP +25%+','UCP 15-25','UCP 10-15','UCP 5-10','UCP 0-5',
                       'NDP 0-5','NDP 5-10','NDP 10-15','NDP 15-25','NDP +25%+']
        print(f"\n  B1: Vote distribution (margin in two-party share)")
        for lbl, count in zip(labels_list, bin_counts):
            print(f"    {lbl:>12s}: {'#' * count} {count}")
        print(f"\n  B2: Efficiency gap = {eg*100:+.2f}%  "
              f"({'within' if abs(eg) < 0.07 else 'EXCEEDS'} 7% threshold)")
        print(f"  B3: Mean-median (NDP) = {mm_gap*100:+.2f} pp  "
              f"({'within' if abs(mm_gap) < 0.03 else 'EXCEEDS'} 3 pp threshold)")
        print(f"  B4: At 50/50 vote: NDP {ndp_at_50}, UCP {ucp_at_50} "
              f"(asymmetry: {abs(ndp_at_50-ucp_at_50)} seats)")
        dec_str = f"{declination:+.4f}" if declination == declination else "N/A"
        print(f"  B6: Declination (Warrington 2018) = {dec_str}  "
              f"(negative = pro-UCP, positive = pro-NDP)")

    return {
        'label': label, 'n': n, 'prov_ndp': prov_ndp,
        'ndp_seats': n_ndp_wins, 'ucp_seats': n_ucp_wins,
        'eg': eg, 'mm_gap': mm_gap,
        'ndp_at_50': ndp_at_50, 'ucp_at_50': ucp_at_50,
        'bin_counts': bin_counts,
        'declination': declination,
    }


# =====================================================================
# 5. Monte Carlo CI
# =====================================================================

def monte_carlo_ci(assignments_df, n_draws=2000, seed=42):
    """
    Monte Carlo CI on VA-resolution data.
    Per-draw: apply a random uniform swing to each ED's NDP share
    (ED-level, not VA-level, since VAs within an ED move together),
    then re-compute metrics.
    """
    rng = np.random.default_rng(seed)

    # Aggregate to ED level first
    ed_data = assignments_df.groupby('assigned_2026').agg(
        ndp=('va_ndp', 'sum'),
        ucp=('va_ucp', 'sum'),
    ).reset_index()

    ed_ndp = ed_data['ndp'].values.astype(float)
    ed_ucp = ed_data['ucp'].values.astype(float)
    ed_total = ed_ndp + ed_ucp
    ed_share = np.where(ed_total > 0, ed_ndp / ed_total, 0.5)
    n_eds = len(ed_data)

    eg_draws = []
    mm_draws = []
    n50_draws = []
    dec_draws = []

    for _ in range(n_draws):
        # Global uniform swing: Uniform(-0.05, +0.05)
        swing = rng.uniform(-0.05, 0.05)
        # Per-ED noise: Normal(0, 0.02) — captures local variation
        noise = rng.normal(0, 0.02, n_eds)
        swung_share = np.clip(ed_share + swing + noise, 0.01, 0.99)

        swung_ndp = ed_total * swung_share
        swung_ucp = ed_total * (1 - swung_share)
        total = ed_total.sum()
        prov_ndp_share = swung_ndp.sum() / total

        ndp_wins = int((swung_ndp > swung_ucp).sum())
        ucp_wins = n_eds - ndp_wins

        # EG
        ndp_wasted = 0.0
        ucp_wasted = 0.0
        for k in range(n_eds):
            thr = ed_total[k] / 2 + 1
            if swung_ndp[k] > swung_ucp[k]:
                ndp_wasted += max(0, swung_ndp[k] - thr)
                ucp_wasted += swung_ucp[k]
            else:
                ucp_wasted += max(0, swung_ucp[k] - thr)
                ndp_wasted += swung_ndp[k]
        eg = (ndp_wasted - ucp_wasted) / total
        eg_draws.append(eg)

        # Mean-median
        shares_list = swung_share.tolist()
        mn = statistics.mean(shares_list)
        md = statistics.median(shares_list)
        mm_draws.append(mn - md)

        # NDP at 50/50
        swing_50 = 0.5 - prov_ndp_share
        swung_50 = swung_share + swing_50
        n50 = int((swung_50 > 0.5).sum())
        n50_draws.append(n50)

        # Declination
        ndp_won = [s for s in shares_list if s > 0.5]
        ucp_won = [s for s in shares_list if s < 0.5]
        if ndp_won and ucp_won:
            theta_n = math.atan2(statistics.mean(ndp_won) - 0.5, ndp_wins / n_eds)
            theta_u = math.atan2(0.5 - statistics.mean(ucp_won), ucp_wins / n_eds)
            dec_draws.append((theta_n - theta_u) * 2 / math.pi)

    def ci(vals):
        s = sorted(vals)
        lo = s[int(len(s) * 0.025)]
        hi = s[int(len(s) * 0.975)]
        return lo, hi

    eg_ci = ci(eg_draws)
    mm_ci = ci(mm_draws)
    n50_ci = ci(n50_draws)
    dec_ci = ci(dec_draws) if dec_draws else (float('nan'), float('nan'))
    eg_neg_pct = sum(1 for e in eg_draws if e < 0) / len(eg_draws) * 100

    return {
        'eg_ci': eg_ci, 'mm_ci': mm_ci, 'n50_ci': n50_ci, 'dec_ci': dec_ci,
        'eg_neg_pct': eg_neg_pct, 'n_draws': n_draws,
        'eg_median': statistics.median(eg_draws),
        'mm_median': statistics.median(mm_draws),
    }


# =====================================================================
# Main
# =====================================================================

def main():
    print("=" * 60)
    print("  Phase 4C — VA-level measured vote attribution")
    print("  Spatial-first assignment (replaces v0.2 70/30 blend)")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    va = load_va_polygons()
    flagged = load_flagged_vas()
    maj_eds, min_eds = load_2026_shapefiles()
    print(f"  {len(va)} VAs, {len(flagged)} flagged")
    print(f"  Majority shapefile: {len(maj_eds)} EDs")
    print(f"  Minority shapefile: {len(min_eds)} EDs")

    # Ensure CRS match
    if maj_eds.crs != va.crs:
        maj_eds = maj_eds.to_crs(va.crs)
    if min_eds.crs != va.crs:
        min_eds = min_eds.to_crs(va.crs)

    # Stage 3: Assign VAs
    print("\n" + "=" * 60)
    print("  STAGE 3: VA assignment to 2026 EDs")
    print("=" * 60)

    print("\n  --- MAJORITY ---")
    maj_assignments, maj_stats = assign_vas_spatial_first(
        va, flagged, maj_eds, MAJ_REVERSE, MAJORITY_2026_MAPPING,
        'majority_hybrid_candidate', 'majority')

    print("\n  --- MINORITY ---")
    min_assignments, min_stats = assign_vas_spatial_first(
        va, flagged, min_eds, MIN_REVERSE, MINORITY_2026_MAPPING,
        'minority_hybrid_candidate', 'minority')

    # Stage 4: Write assignments CSV
    print("\n" + "=" * 60)
    print("  STAGE 4: Write VA assignments")
    print("=" * 60)

    combined = maj_assignments[['va_id', 'parent_ed_2019', 'va_ndp', 'va_ucp', 'va_other']].copy()
    combined['assigned_2026_majority'] = maj_assignments['assigned_2026']
    combined['maj_method'] = maj_assignments['assignment_method']
    combined['maj_confidence'] = maj_assignments['confidence']
    combined['assigned_2026_minority'] = min_assignments['assigned_2026']
    combined['min_method'] = min_assignments['assignment_method']
    combined['min_confidence'] = min_assignments['confidence']

    out_path = os.path.join(HERE, 'phase_4c_va_to_2026_assignments.csv')
    combined.to_csv(out_path, index=False)
    print(f"  Written: {out_path} ({len(combined)} rows)")

    # Stage 5: Aggregate
    print("\n" + "=" * 60)
    print("  STAGE 5: 2026 ED synthetic vote totals")
    print("=" * 60)

    maj_totals = aggregate_by_ed(maj_assignments)
    min_totals = aggregate_by_ed(min_assignments)

    print(f"\n  Majority: {len(maj_totals)} unique 2026 EDs")
    print(f"    NDP: {maj_totals['ndp'].sum():,.1f}  UCP: {maj_totals['ucp'].sum():,.1f}")
    print(f"  Minority: {len(min_totals)} unique 2026 EDs")
    print(f"    NDP: {min_totals['ndp'].sum():,.1f}  UCP: {min_totals['ucp'].sum():,.1f}")

    # Write synthetic totals
    totals_path = os.path.join(HERE, 'phase_4c_2026_synthetic_totals.csv')
    maj_out = maj_totals.copy(); maj_out['map'] = 'majority'
    min_out = min_totals.copy(); min_out['map'] = 'minority'
    pd.concat([maj_out, min_out]).to_csv(totals_path, index=False)
    print(f"  Written: {totals_path}")

    # Vote conservation check
    va_ndp = va['va_ndp'].sum()
    va_ucp = va['va_ucp'].sum()
    print(f"\n  Vote conservation:")
    print(f"    VA substrate:  NDP={va_ndp:,.1f}  UCP={va_ucp:,.1f}")
    print(f"    Majority sum:  NDP={maj_totals['ndp'].sum():,.1f}  UCP={maj_totals['ucp'].sum():,.1f}")
    print(f"    Minority sum:  NDP={min_totals['ndp'].sum():,.1f}  UCP={min_totals['ucp'].sum():,.1f}")
    drift = max(abs(va_ndp - maj_totals['ndp'].sum()),
                abs(va_ucp - maj_totals['ucp'].sum()),
                abs(va_ndp - min_totals['ndp'].sum()),
                abs(va_ucp - min_totals['ucp'].sum()))
    print(f"    Max drift: {drift:.1f}  {'PASS' if drift < 1.0 else 'WARNING'}")

    # Stage 6: Metrics
    print("\n" + "=" * 60)
    print("  STAGE 6: Packing/cracking metrics (VA resolution)")
    print("=" * 60)

    # 2019 baseline
    baseline = va.groupby('parent_ed_2019').agg(
        ndp=('va_ndp', 'sum'), ucp=('va_ucp', 'sum'),
        other=('va_other', 'sum'), n_vas=('va_id', 'count'),
    ).reset_index()
    baseline.rename(columns={'parent_ed_2019': 'ed_2026'}, inplace=True)

    m_2019 = compute_metrics(baseline, "2019 BOUNDARIES (VA-aggregated baseline)")
    m_maj = compute_metrics(maj_totals, "MAJORITY 2026 (Phase 4C measured)")
    m_min = compute_metrics(min_totals, "MINORITY 2026 (Phase 4C measured)")

    # Three-way comparison table
    print("\n" + "=" * 60)
    print("  THREE-MAP COMPARISON (Phase 4C)")
    print("=" * 60)
    print(f"  {'Metric':<22s} | {'2019':>7s} | {'Majority':>8s} | {'Minority':>8s}")
    print(f"  {'-'*22}-+-{'-'*7}-+-{'-'*8}-+-{'-'*8}")
    print(f"  {'Districts':<22s} | {m_2019['n']:>7d} | {m_maj['n']:>8d} | {m_min['n']:>8d}")
    print(f"  {'Seats NDP/UCP':<22s} | {m_2019['ndp_seats']}/{m_2019['ucp_seats']:>4d} | {m_maj['ndp_seats']}/{m_maj['ucp_seats']:>5d} | {m_min['ndp_seats']}/{m_min['ucp_seats']:>5d}")
    print(f"  {'B2 Efficiency gap':<22s} | {m_2019['eg']*100:+6.2f}% | {m_maj['eg']*100:+7.2f}% | {m_min['eg']*100:+7.2f}%")
    print(f"  {'B3 Mean-median':<22s} | {m_2019['mm_gap']*100:+6.2f}pp| {m_maj['mm_gap']*100:+7.2f}pp| {m_min['mm_gap']*100:+7.2f}pp")
    print(f"  {'B4 NDP @ 50/50':<22s} | {m_2019['ndp_at_50']:>7d} | {m_maj['ndp_at_50']:>8d} | {m_min['ndp_at_50']:>8d}")
    print(f"  {'B6 Declination':<22s} | {m_2019['declination']:+7.4f} | {m_maj['declination']:+8.4f} | {m_min['declination']:+8.4f}")

    delta_maj = m_maj['eg'] - m_2019['eg']
    delta_min = m_min['eg'] - m_2019['eg']
    asym = delta_min - delta_maj
    print(f"\n  Delta from 2019 EG: majority {delta_maj*100:+.2f}pp, minority {delta_min*100:+.2f}pp")
    print(f"  Minority-Majority asymmetry: {asym*100:+.2f}pp")

    # Stage 7: Monte Carlo
    print("\n" + "=" * 60)
    print("  STAGE 7: Monte Carlo CIs (2,000 draws)")
    print("=" * 60)

    print("\n  Majority 2026...")
    mc_maj = monte_carlo_ci(maj_assignments, n_draws=2000, seed=42)
    print(f"    EG 95% CI: [{mc_maj['eg_ci'][0]*100:+.2f}%, {mc_maj['eg_ci'][1]*100:+.2f}%]")
    print(f"    EG median: {mc_maj['eg_median']*100:+.2f}%")
    print(f"    Mean-median 95% CI: [{mc_maj['mm_ci'][0]*100:+.2f}pp, {mc_maj['mm_ci'][1]*100:+.2f}pp]")
    print(f"    NDP@50/50 95% CI: [{mc_maj['n50_ci'][0]}, {mc_maj['n50_ci'][1]}]")
    print(f"    Declination 95% CI: [{mc_maj['dec_ci'][0]:+.4f}, {mc_maj['dec_ci'][1]:+.4f}]")
    print(f"    EG negative (pro-UCP) in {mc_maj['eg_neg_pct']:.1f}% of draws")

    print("\n  Minority 2026...")
    mc_min = monte_carlo_ci(min_assignments, n_draws=2000, seed=42)
    print(f"    EG 95% CI: [{mc_min['eg_ci'][0]*100:+.2f}%, {mc_min['eg_ci'][1]*100:+.2f}%]")
    print(f"    EG median: {mc_min['eg_median']*100:+.2f}%")
    print(f"    Mean-median 95% CI: [{mc_min['mm_ci'][0]*100:+.2f}pp, {mc_min['mm_ci'][1]*100:+.2f}pp]")
    print(f"    NDP@50/50 95% CI: [{mc_min['n50_ci'][0]}, {mc_min['n50_ci'][1]}]")
    print(f"    Declination 95% CI: [{mc_min['dec_ci'][0]:+.4f}, {mc_min['dec_ci'][1]:+.4f}]")
    print(f"    EG negative (pro-UCP) in {mc_min['eg_neg_pct']:.1f}% of draws")

    # Direction consistency comparison
    print(f"\n  Direction consistency:")
    print(f"    Majority EG negative: {mc_maj['eg_neg_pct']:.1f}% of draws")
    print(f"    Minority EG negative: {mc_min['eg_neg_pct']:.1f}% of draws")

    print("\n\nPhase 4C complete.")
    return m_2019, m_maj, m_min, mc_maj, mc_min


if __name__ == '__main__':
    main()
