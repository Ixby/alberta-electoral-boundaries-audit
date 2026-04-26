"""Fuzz the 6 missing minority-map EDs to bracket the seats@50/50 finding."""
# Version: 0.1 series  (last updated 2026-04-26)

import sys
sys.path.insert(0, 'analysis/scripts')
import geopandas as gpd
import numpy as np
import pandas as pd
from pathlib import Path

DERIVED = Path('data/shapefiles/derived')
REF = Path('data/shapefiles/reference')

va = gpd.read_file(DERIVED / 'va_polygons_with_2023_votes.gpkg')
centroids = va.copy()
centroids['geometry'] = centroids.geometry.representative_point()

minority = gpd.read_file(DERIVED / 'v0_8_full_refined_minority_2026_eds.gpkg').to_crs(va.crs)
joined = gpd.sjoin(centroids[['va_ucp', 'va_ndp', 'geometry']],
                   minority[['name_2026', 'geometry']],
                   how='left', predicate='within')
covered = joined.dropna(subset=['name_2026'])
# Gemini Code Audit Finding: HIGH - missing deduplication for overlapping polygon slivers
covered = covered[~covered.index.duplicated(keep="first")]
agg = covered.groupby('name_2026').agg(ucp=('va_ucp', 'sum'),
                                         ndp=('va_ndp', 'sum')).reset_index()
covered_eds = set(agg['name_2026'])
all_eds = list(minority['name_2026'])
missing_eds = [e for e in all_eds if e not in covered_eds]

en19 = gpd.read_file(REF / 'alberta_2019_eds').to_crs(va.crs)
joined19 = gpd.sjoin(centroids[['va_ucp', 'va_ndp', 'geometry']],
                     en19[['EDName2017', 'geometry']],
                     how='left', predicate='within')
agg19 = joined19.dropna(subset=['EDName2017']).groupby('EDName2017').agg(
    ucp=('va_ucp', 'sum'), ndp=('va_ndp', 'sum')).reset_index()
votes_19 = {r['EDName2017']: (r['ucp'], r['ndp']) for _, r in agg19.iterrows()}

crosswalk = {
    'Calgary-Airdrie':         'Airdrie-East',
    'Calgary-Fish Creek':      'Calgary-Fish Creek',
    'Chestermere-Strathmore':  'Chestermere-Strathmore',
    'Edmonton-Manning':        'Edmonton-Manning',
    'Edmonton-McClung':        'Edmonton-McClung',
    'Edmonton-Rutherford':     'Edmonton-Rutherford',
}


def seats_at_50_50(ucp_arr, ndp_arr):
    total = ucp_arr + ndp_arr
    ucp_share_d = np.where(total > 0, ucp_arr / total, 0.5)
    global_share = ucp_arr.sum() / total.sum()
    shift = 0.5 - global_share
    shifted = np.clip(ucp_share_d + shift, 0, 1)
    return float((shifted > 0.5).sum() / len(ucp_arr)), int((shifted > 0.5).sum()), len(ucp_arr)


def efficiency_gap(ucp_arr, ndp_arr):
    total = ucp_arr + ndp_arr
    won = ucp_arr > ndp_arr
    wasted_ucp = np.where(won, ucp_arr - (total / 2 + 1), ucp_arr)
    wasted_ndp = np.where(won, ndp_arr, ndp_arr - (total / 2 + 1))
    return float((wasted_ndp.sum() - wasted_ucp.sum()) / total.sum())


def add_rows(base_df, rows):
    return pd.concat([base_df, pd.DataFrame(rows)], ignore_index=True)


print('=' * 78)
print('FUZZING SCENARIOS — minority map seats@50/50 under different fill strategies')
print('=' * 78)
print()
print(f'Missing EDs (6): {missing_eds}')
print('Simulation 2M ceiling = 51.72% UCP seats at 50/50 (the out-of-distribution line)')
print('Current 83-of-89 reading: 54.22% (45 of 83) UCP seats at 50/50')
print()

scenarios = []

# A: Inherited 2019 polygon votes (most defensible)
rows_a = []
for ed_2026, ed_2019 in crosswalk.items():
    if ed_2019 in votes_19:
        ucp_v, ndp_v = votes_19[ed_2019]
        rows_a.append({'name_2026': ed_2026, 'ucp': ucp_v, 'ndp': ndp_v})
agg_a = add_rows(agg, rows_a)
ucp_a = agg_a['ucp'].values
ndp_a = agg_a['ndp'].values
s50, seats, n = seats_at_50_50(ucp_a, ndp_a)
eg = efficiency_gap(ucp_a, ndp_a)
scenarios.append(('A. Inherited 2019 polygons (most defensible)', s50, seats, n, eg))

# B: Worst case for finding (all 6 missing → strongly NDP)
median_total = (agg['ucp'].values + agg['ndp'].values).mean()
rows_b = [{'name_2026': ed, 'ucp': median_total * 0.40,
           'ndp': median_total * 0.60} for ed in missing_eds]
agg_b = add_rows(agg, rows_b)
ucp_b = agg_b['ucp'].values
ndp_b = agg_b['ndp'].values
s50, seats, n = seats_at_50_50(ucp_b, ndp_b)
eg = efficiency_gap(ucp_b, ndp_b)
scenarios.append(('B. All 6 missing assumed strongly NDP-leaning (40/60)', s50, seats, n, eg))

# C: Best case for finding (all 6 missing → strongly UCP)
rows_c = [{'name_2026': ed, 'ucp': median_total * 0.60,
           'ndp': median_total * 0.40} for ed in missing_eds]
agg_c = add_rows(agg, rows_c)
ucp_c = agg_c['ucp'].values
ndp_c = agg_c['ndp'].values
s50, seats, n = seats_at_50_50(ucp_c, ndp_c)
eg = efficiency_gap(ucp_c, ndp_c)
scenarios.append(('C. All 6 missing assumed strongly UCP-leaning (60/40)', s50, seats, n, eg))

# D: Regional-median attribution
calgary_eds = [e for e in agg['name_2026'] if 'Calgary' in e or 'Chestermere' in e or 'Airdrie' in e]
edmonton_eds = [e for e in agg['name_2026'] if 'Edmonton' in e or 'St. Albert' in e]
calgary_share = (agg[agg['name_2026'].isin(calgary_eds)]['ucp'].sum() /
                 (agg[agg['name_2026'].isin(calgary_eds)]['ucp'].sum() +
                  agg[agg['name_2026'].isin(calgary_eds)]['ndp'].sum()))
edmonton_share = (agg[agg['name_2026'].isin(edmonton_eds)]['ucp'].sum() /
                  (agg[agg['name_2026'].isin(edmonton_eds)]['ucp'].sum() +
                   agg[agg['name_2026'].isin(edmonton_eds)]['ndp'].sum()))
print(f'Calgary regional UCP share: {calgary_share*100:.1f}%')
print(f'Edmonton regional UCP share: {edmonton_share*100:.1f}%')
print()

rows_d = []
for ed in missing_eds:
    if 'Calgary' in ed or 'Chestermere' in ed:
        share = calgary_share
    else:
        share = edmonton_share
    rows_d.append({'name_2026': ed, 'ucp': median_total * share,
                   'ndp': median_total * (1 - share)})
agg_d = add_rows(agg, rows_d)
ucp_d = agg_d['ucp'].values
ndp_d = agg_d['ndp'].values
s50, seats, n = seats_at_50_50(ucp_d, ndp_d)
eg = efficiency_gap(ucp_d, ndp_d)
scenarios.append(('D. Regional-median attribution (Calgary -> Calgary share, Edmonton -> Edmonton share)',
                  s50, seats, n, eg))

# E: Random resampling from existing distribution (10,000 trials)
np.random.seed(42)
existing_shares = agg['ucp'].values / (agg['ucp'].values + agg['ndp'].values).clip(min=1)
existing_totals = agg['ucp'].values + agg['ndp'].values
results_e = []
egs_e = []
for trial in range(10000):
    agg_e_ucp = list(agg['ucp'].values)
    agg_e_ndp = list(agg['ndp'].values)
    for _ in missing_eds:
        idx = np.random.randint(len(existing_shares))
        sh = existing_shares[idx]
        tot = existing_totals[idx]
        agg_e_ucp.append(sh * tot)
        agg_e_ndp.append((1 - sh) * tot)
    arr_u = np.array(agg_e_ucp)
    arr_n = np.array(agg_e_ndp)
    s50, _, _ = seats_at_50_50(arr_u, arr_n)
    results_e.append(s50)
    egs_e.append(efficiency_gap(arr_u, arr_n))
results_e = np.array(results_e)
egs_e = np.array(egs_e)

print()
print('=' * 78)
print(f'{"Scenario":75s} | s@50  | UCP/n   | EG')
print('=' * 78)
for name, s50, seats, n, eg in scenarios:
    print(f'{name:75s} | {s50*100:>5.2f}% | {seats:>3d}/{n:<3d} | {eg*100:+5.2f}%')
print()
print(f'E. Random-resample 10,000 trials: ')
print(f'   mean s@50 = {results_e.mean()*100:.2f}%   p5 = {np.percentile(results_e, 5)*100:.2f}%   p50 = {np.percentile(results_e, 50)*100:.2f}%   p95 = {np.percentile(results_e, 95)*100:.2f}%')
print(f'   min = {results_e.min()*100:.2f}%   max = {results_e.max()*100:.2f}%')
print(f'   trials above 51.72% ceiling: {(results_e > 0.5172).sum():,} of 10,000 = {(results_e > 0.5172).mean()*100:.2f}%')
print(f'   trials above 50%: {(results_e > 0.50).sum():,} of 10,000 = {(results_e > 0.50).mean()*100:.2f}%')
print(f'   mean EG = {egs_e.mean()*100:+.2f}%   p5 = {np.percentile(egs_e, 5)*100:+.2f}%   p95 = {np.percentile(egs_e, 95)*100:+.2f}%')
print()
print(f'Simulation ceiling (2M ensemble max): 51.72% UCP seats at 50/50')
print()
print(f'Of the 4 explicit scenarios above the 51.72% ceiling: {sum(1 for _,s,_,_,_ in scenarios if s > 0.5172)}/{len(scenarios)}')
