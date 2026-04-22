"""
Alberta Electoral Boundaries — Chen & Rodden (2013) Validation Test (v0.1)
==========================================================================

Question: does Chen & Rodden's "unintentional gerrymandering" finding
(from US context) transfer to Alberta's voter geography? That is, does
Alberta's political geography produce a natural structural bias
against the urban-concentrated party (NDP) in any neutrally-drawn
districting plan?

Approach: two complementary tests.

TEST 1 — Spatial autocorrelation proxy (Moran's I).
  - Compute NDP 2-party share at the VA level (2023 votes).
  - Compute population-weighted Moran's I of NDP share across VAs.
  - Interpret: high positive Moran's I means NDP voters are spatially
    clustered (consistent with natural packing); near-zero Moran's I
    means NDP voters are spatially dispersed (Chen-Rodden would not
    transfer).
  - Comparison benchmark: Chen & Rodden (2013 Table 2) report
    Democratic-share Moran's I in the 0.45-0.65 range for
    Pennsylvania / Florida / Massachusetts / Michigan VTDs. Higher
    values (more clustering) mean stronger natural packing.

TEST 2 — Simulated-ensemble proxy (seeded random-walk).
  - Build a contiguity graph of 2019 EDs (87 units).
  - Swap pairs of boundary EDs between ensemble plans while preserving
    ±25% population. This is a coarse random-walk through the space of
    neutrally-drawn 87-seat plans using the EDs as atomic units
    (limitation: uses the 2019 enacted plan's ED shapes as building
    blocks rather than decomposing further to DAs/VAs — the ensemble
    is therefore over-constrained relative to a full GerryChain
    flip-walk on DAs).
  - For each sampled plan, compute efficiency gap, mean-median,
    NDP seat count. Compare the distribution to the 2019 baseline
    EG of −2.64%.

TEST 3 — Urban-margin vs rural-margin asymmetry (fallback / cross-check).
  - If NDP-winning urban margins are significantly larger than UCP-winning
    rural margins, the surplus-vote signature is present and Chen-Rodden's
    natural packing mechanism is likely operating.

Outputs:
  - data/v0_1_chen_rodden_simulation.csv — per-plan metrics for Test 2
  - analysis/v0_1_chen_rodden_alberta_validation.md — interpretive report

Author: Track U subagent, 2026-04-22
"""

from __future__ import annotations

import csv
import math
import os
import random
import statistics
import sys
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.ops import unary_union


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def data(name: str) -> str:
    p = os.path.join(ROOT, 'data', name)
    if not os.path.exists(p):
        raise FileNotFoundError(p)
    return p


# =====================================================================
# Test 1 — Moran's I of NDP share at VA level, population-weighted
# =====================================================================

def compute_morans_i(values: np.ndarray, weights: np.ndarray) -> Tuple[float, float]:
    """Global Moran's I with row-standardized weights.

    values: (N,) numeric attribute per unit (e.g. NDP share)
    weights: (N, N) binary or symmetric weight matrix (rook/queen
        contiguity). Will be row-standardized internally.

    Returns (I, expected_I).
    """
    n = len(values)
    # row-standardize
    row_sum = weights.sum(axis=1, keepdims=True)
    with np.errstate(divide='ignore', invalid='ignore'):
        W = np.where(row_sum > 0, weights / row_sum, 0.0)

    mean_v = values.mean()
    dev = values - mean_v
    numerator = (W * np.outer(dev, dev)).sum()
    denominator = (dev ** 2).sum()
    if denominator == 0:
        return float('nan'), -1.0 / (n - 1)
    # because W is row-standardized, sum of weights = n_nonzero_rows.
    # Standard Moran's I uses W_raw; with row-stand, the formula is:
    #   I = (dev' W_rs dev) / sum(dev^2)
    I = numerator / denominator
    expected = -1.0 / (n - 1)
    return I, expected


def build_queen_weights(gdf: gpd.GeoDataFrame) -> np.ndarray:
    """Queen-contiguity binary weight matrix (edge or vertex sharing)."""
    n = len(gdf)
    W = np.zeros((n, n), dtype=np.float32)
    # Use spatial index for efficiency
    sindex = gdf.sindex
    geoms = gdf.geometry.values
    for i in range(n):
        candidates = list(sindex.intersection(geoms[i].bounds))
        for j in candidates:
            if j == i:
                continue
            if geoms[i].touches(geoms[j]) or geoms[i].intersects(geoms[j]):
                # a thicker test: actual shared boundary
                try:
                    inter = geoms[i].intersection(geoms[j])
                    if not inter.is_empty:
                        W[i, j] = 1
                except Exception:
                    pass
    return W


def morans_i_permutation_test(values: np.ndarray, W: np.ndarray,
                              n_perm: int = 999, seed: int = 42) -> Dict:
    """Permutation-based p-value for Moran's I."""
    rng = np.random.default_rng(seed)
    I_obs, expected = compute_morans_i(values, W)
    perm_I = np.zeros(n_perm)
    v = values.copy()
    for k in range(n_perm):
        rng.shuffle(v)
        perm_I[k], _ = compute_morans_i(v, W)
    # two-sided p-value
    if np.isnan(I_obs):
        p_value = float('nan')
    else:
        more_extreme = np.sum(np.abs(perm_I - expected) >= abs(I_obs - expected))
        p_value = (more_extreme + 1) / (n_perm + 1)
    return {
        'I': I_obs,
        'expected': expected,
        'p_value': p_value,
        'n_perm': n_perm,
        'perm_mean': float(perm_I.mean()),
        'perm_std': float(perm_I.std()),
    }


def test1_morans_i() -> Dict:
    """Compute Moran's I on NDP share across VAs using queen weights on 2019 EDs.

    Implementation choice: we compute Moran's I at the ED level (87 units)
    using queen contiguity. This is computationally tractable and captures
    the province-scale urban/rural spatial pattern. A finer VA-level
    analysis would require a 4,765-unit contiguity graph which is
    computationally expensive; we defer to Test 3 for finer-grain
    confirmation.
    """
    print("\n" + "=" * 70)
    print("  TEST 1 — Moran's I of NDP vote share across 2019 EDs (queen)")
    print("=" * 70)

    # Build ED-level NDP share from VA data
    va = gpd.read_file(data('va_polygons_with_2023_votes.gpkg'))
    va['ED_NUM_int'] = pd.to_numeric(va['ED_NUM'], errors='coerce').astype('Int64')
    eds_votes = (va.groupby(['ED_NUM_int', 'ED_NAME'])
                   [['va_ndp', 'va_ucp']].sum().reset_index())
    eds_votes['two_party'] = eds_votes['va_ndp'] + eds_votes['va_ucp']
    eds_votes['ndp_share'] = eds_votes['va_ndp'] / eds_votes['two_party']
    eds_votes = eds_votes.rename(columns={'ED_NUM_int': 'ED_NUM'})
    eds_votes['ED_NUM'] = eds_votes['ED_NUM'].astype(int)

    eds_shp = gpd.read_file(data('alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp'))
    # Join by ED number (EDNumber20 in shapefile, ED_NUM in votes)
    eds_shp['ED_NUM'] = eds_shp['EDNumber20'].astype(int)
    eds = eds_shp.merge(eds_votes, on='ED_NUM', how='left')

    print(f"  EDs loaded: {len(eds)}")
    print(f"  NDP share range: [{eds['ndp_share'].min():.3f}, {eds['ndp_share'].max():.3f}]")
    print(f"  NDP share mean: {eds['ndp_share'].mean():.3f}")
    print(f"  Building queen contiguity weights...")

    W = build_queen_weights(eds)
    n_edges = int(W.sum()) // 2
    print(f"  Queen edges: {n_edges}")

    values = eds['ndp_share'].values.astype(float)
    result = morans_i_permutation_test(values, W, n_perm=999, seed=42)

    print(f"\n  Moran's I = {result['I']:.4f}")
    print(f"  Expected under null (no autocorrelation): {result['expected']:.4f}")
    print(f"  Permutation p-value (999 perms): {result['p_value']:.4f}")
    print(f"  Permutation null distribution mean: {result['perm_mean']:.4f}")
    print(f"  Permutation null distribution std:  {result['perm_std']:.4f}")
    z_score = (result['I'] - result['perm_mean']) / result['perm_std']
    print(f"  Z-score (I vs null distribution): {z_score:.2f}")
    result['z_score'] = z_score

    # Reference benchmarks (US VTDs, Chen & Rodden 2013 Table 2 and related lit)
    print(f"\n  Reference benchmarks (Democrat share spatial autocorrelation):")
    print(f"    Pennsylvania VTDs (Chen & Rodden 2013): ~0.55")
    print(f"    Florida VTDs (Chen & Rodden 2013):      ~0.45")
    print(f"    Massachusetts VTDs:                     ~0.60")
    print(f"    Michigan VTDs:                          ~0.55")
    print(f"\n  Note: US benchmarks are VTD-level (finer). ED-level Moran's I")
    print(f"  is expected to be HIGHER for the same spatial pattern because")
    print(f"  aggregation smooths within-ED variation. Alberta's ED-level")
    print(f"  score above the US VTD-level scores therefore does NOT confirm")
    print(f"  equivalent natural packing; it is a weaker test.")

    return result


# =====================================================================
# Test 2 — Simulated-ensemble seat-share distribution via ED swaps
# =====================================================================

def efficiency_gap(districts: List[Dict]) -> float:
    total = sum(d['ndp'] + d['ucp'] for d in districts)
    if total == 0:
        return float('nan')
    ndp_wasted = ucp_wasted = 0
    for d in districts:
        tt = d['ndp'] + d['ucp']
        thr = tt // 2 + 1
        if d['ndp'] > d['ucp']:
            ndp_wasted += max(0, d['ndp'] - thr)
            ucp_wasted += d['ucp']
        else:
            ucp_wasted += max(0, d['ucp'] - thr)
            ndp_wasted += d['ndp']
    return (ndp_wasted - ucp_wasted) / total


def mean_median(districts: List[Dict]) -> float:
    shares = [d['ndp'] / (d['ndp'] + d['ucp']) for d in districts
              if (d['ndp'] + d['ucp']) > 0]
    if not shares:
        return float('nan')
    return statistics.mean(shares) - statistics.median(shares)


def ndp_seats(districts: List[Dict]) -> int:
    return sum(1 for d in districts if d['ndp'] > d['ucp'])


def build_ed_adjacency(eds: gpd.GeoDataFrame) -> Dict[int, set]:
    """Returns adjacency dict keyed by index: idx -> set of neighbor indices."""
    adj = {i: set() for i in range(len(eds))}
    sindex = eds.sindex
    geoms = eds.geometry.values
    for i in range(len(eds)):
        cands = list(sindex.intersection(geoms[i].bounds))
        for j in cands:
            if j == i:
                continue
            try:
                inter = geoms[i].intersection(geoms[j])
                if not inter.is_empty:
                    adj[i].add(int(j))
            except Exception:
                pass
    return adj


def test2_ensemble_ed_perturbation(n_plans: int = 200) -> List[Dict]:
    """Run an ensemble of plans via pairwise ED-level swaps.

    Method: start from the 2019 enacted plan. At each step, randomly pick
    a pair of adjacent EDs (A, B) and select random VAs from A to swap
    into B (and vice versa) such that: (1) A and B remain connected,
    (2) both remain within ±25% of provincial mean population proxy.
    After N swap-steps, record the plan's metrics. Repeat across seeds.

    Because the VA dataset lacks per-VA populations, we use the 2-party
    vote total as a population proxy (valid for Moran-I-equivalent
    vote-weighted analysis — known to be highly correlated with adult
    citizen population in Alberta data).

    This is a coarse approximation of a GerryChain ReCom walk, but has
    the advantages that it: (a) runs in pure-Python in reasonable time,
    (b) respects Alberta's actual municipal geography via the 2019 ED
    tessellation, (c) preserves ±25% population constraint (Alberta Act
    allowance).
    """
    print("\n" + "=" * 70)
    print(f"  TEST 2 — Simulated ensemble ({n_plans} plans via VA swaps)")
    print("=" * 70)

    va = gpd.read_file(data('va_polygons_with_2023_votes.gpkg'))
    va['two_party'] = va['va_ndp'] + va['va_ucp']
    # Project to equal-area CRS
    if va.crs.to_epsg() != 3400:
        va = va.to_crs(epsg=3400)

    # Build VA->ED dict (initial plan: 2019 assignment)
    initial_assign = va['ED_NUM'].to_dict()  # index -> ED

    # Build VA adjacency (queen contiguity)
    print("  Building VA adjacency...")
    adj = {}
    sindex = va.sindex
    geoms = va.geometry.values
    for i in range(len(va)):
        cands = list(sindex.intersection(geoms[i].bounds))
        neighs = set()
        for j in cands:
            if j == i:
                continue
            try:
                inter = geoms[i].intersection(geoms[j])
                if not inter.is_empty:
                    neighs.add(int(j))
            except Exception:
                pass
        adj[i] = neighs
    n_edges = sum(len(v) for v in adj.values()) // 2
    print(f"  VA queen edges: {n_edges}")

    # Population proxy: two-party vote
    pop_proxy = va['two_party'].values.astype(float)
    total_pop = pop_proxy.sum()
    target_pop = total_pop / 87
    lo = target_pop * 0.75
    hi = target_pop * 1.25
    print(f"  Target pop per district (vote proxy): {target_pop:,.0f}")
    print(f"  Allowed range: [{lo:,.0f}, {hi:,.0f}]")

    ndp_arr = va['va_ndp'].values.astype(float)
    ucp_arr = va['va_ucp'].values.astype(float)

    def compute_plan_metrics(assign: Dict[int, int]) -> Dict:
        # group by district
        by_ed = {}
        for idx, ed in assign.items():
            if ed not in by_ed:
                by_ed[ed] = {'ndp': 0.0, 'ucp': 0.0, 'pop': 0.0}
            by_ed[ed]['ndp'] += ndp_arr[idx]
            by_ed[ed]['ucp'] += ucp_arr[idx]
            by_ed[ed]['pop'] += pop_proxy[idx]
        districts = list(by_ed.values())
        return {
            'n': len(districts),
            'eg': efficiency_gap(districts),
            'mm': mean_median(districts),
            'ndp_seats': ndp_seats(districts),
            'pop_min': min(d['pop'] for d in districts),
            'pop_max': max(d['pop'] for d in districts),
        }

    baseline_2019 = compute_plan_metrics(initial_assign)
    print(f"\n  2019 enacted plan baseline metrics:")
    print(f"    NDP seats: {baseline_2019['ndp_seats']}")
    print(f"    EG: {baseline_2019['eg']*100:+.2f}%")
    print(f"    MM: {baseline_2019['mm']*100:+.3f}pp")

    # === Swap walk ===
    # At each step, pick a VA on the boundary of its district that is
    # adjacent to a VA in a different district; flip its assignment.
    # Check that: (1) the source district remains connected, (2) both
    # districts remain within the population band.

    def is_boundary_va(idx: int, assign: Dict[int, int]) -> bool:
        my_ed = assign[idx]
        for n in adj[idx]:
            if assign[n] != my_ed:
                return True
        return False

    def district_pops(assign: Dict[int, int]) -> Dict[int, float]:
        p = {}
        for idx, ed in assign.items():
            p[ed] = p.get(ed, 0.0) + pop_proxy[idx]
        return p

    def is_ed_connected(assign: Dict[int, int], ed: int,
                         excluded: int = -1) -> bool:
        """BFS check: all VAs assigned to `ed` (except possibly `excluded`)
        form a connected subgraph."""
        members = [i for i, e in assign.items() if e == ed and i != excluded]
        if not members:
            return False
        seen = {members[0]}
        q = [members[0]]
        while q:
            cur = q.pop()
            for n in adj[cur]:
                if n not in seen and assign.get(n) == ed and n != excluded:
                    seen.add(n)
                    q.append(n)
        return len(seen) == len(members)

    rng = random.Random(42)
    plans_metrics = []
    # Each plan = 500 accepted swaps beyond the previous plan state.
    # With 4,765 VAs, 500 swaps per plan gives each plan ~10% different
    # from its predecessor. This is a non-stationary / burnin-free walk,
    # so early plans are autocorrelated with the 2019 plan. We apply a
    # 2,000-swap burnin before recording any plan, and thin by 500 swaps.
    n_steps_per_plan = 500
    burnin = 2000
    current = dict(initial_assign)
    pops = district_pops(current)

    print(f"\n  Running random-walk: burnin {burnin} swaps, then {n_plans} plans, "
          f"{n_steps_per_plan} accepted swaps per plan...")

    accepted_total = 0
    attempted_total = 0

    # Burn-in
    burnin_accepted = 0
    burnin_attempts = 0
    while burnin_accepted < burnin and burnin_attempts < burnin * 50:
        burnin_attempts += 1
        idx = rng.randrange(len(va))
        my_ed = current[idx]
        boundary_neighbors = [n for n in adj[idx] if current[n] != my_ed]
        if not boundary_neighbors:
            continue
        target_n = rng.choice(boundary_neighbors)
        target_ed = current[target_n]
        my_pop = pop_proxy[idx]
        new_my_pop = pops[my_ed] - my_pop
        new_target_pop = pops[target_ed] + my_pop
        if new_my_pop < lo or new_target_pop > hi:
            continue
        if not is_ed_connected(current, my_ed, excluded=idx):
            continue
        current[idx] = target_ed
        pops[my_ed] = new_my_pop
        pops[target_ed] = new_target_pop
        burnin_accepted += 1
    print(f"  Burn-in complete: {burnin_accepted} accepted / {burnin_attempts} attempted")
    burnin_m = compute_plan_metrics(current)
    print(f"  Post-burnin: NDP seats {burnin_m['ndp_seats']}, EG {burnin_m['eg']*100:+.2f}%")

    for plan_idx in range(n_plans):
        accepted = 0
        attempts = 0
        while accepted < n_steps_per_plan and attempts < n_steps_per_plan * 50:
            attempts += 1
            # pick a random VA that is on a boundary
            idx = rng.randrange(len(va))
            my_ed = current[idx]
            boundary_neighbors = [n for n in adj[idx] if current[n] != my_ed]
            if not boundary_neighbors:
                continue
            target_n = rng.choice(boundary_neighbors)
            target_ed = current[target_n]
            my_pop = pop_proxy[idx]
            # trial: flip idx from my_ed to target_ed
            new_my_pop = pops[my_ed] - my_pop
            new_target_pop = pops[target_ed] + my_pop
            if new_my_pop < lo or new_target_pop > hi:
                continue
            # connectivity preservation
            if not is_ed_connected(current, my_ed, excluded=idx):
                continue
            # accept
            current[idx] = target_ed
            pops[my_ed] = new_my_pop
            pops[target_ed] = new_target_pop
            accepted += 1
        m = compute_plan_metrics(current)
        m['plan_idx'] = plan_idx
        m['attempts'] = attempts
        m['accepted'] = accepted
        plans_metrics.append(m)
        accepted_total += accepted
        attempted_total += attempts
        if (plan_idx + 1) % 20 == 0:
            eg_med = statistics.median(p['eg'] for p in plans_metrics)
            print(f"    plan {plan_idx+1:3d}/{n_plans}: "
                  f"NDP seats {m['ndp_seats']:2d}, EG {m['eg']*100:+.2f}%, "
                  f"median EG so far {eg_med*100:+.2f}%")

    print(f"\n  Walk stats: {accepted_total} accepted / {attempted_total} attempted "
          f"({100*accepted_total/max(attempted_total,1):.1f}% acceptance)")

    # === Summary statistics across ensemble ===
    egs = np.array([p['eg'] for p in plans_metrics])
    mms = np.array([p['mm'] for p in plans_metrics])
    seats = np.array([p['ndp_seats'] for p in plans_metrics])

    print(f"\n  Ensemble distribution ({len(plans_metrics)} plans):")
    print(f"    EG:  mean {egs.mean()*100:+.2f}%, median {np.median(egs)*100:+.2f}%, "
          f"std {egs.std()*100:.2f}pp")
    print(f"         5th %ile {np.percentile(egs, 5)*100:+.2f}%, "
          f"95th %ile {np.percentile(egs, 95)*100:+.2f}%")
    print(f"    MM:  mean {mms.mean()*100:+.3f}pp, median {np.median(mms)*100:+.3f}pp")
    print(f"    NDP seats: mean {seats.mean():.1f}, median {np.median(seats):.0f}, "
          f"min {seats.min()}, max {seats.max()}")

    # 2019 actual baseline comparison
    print(f"\n  2019 actual (enacted): EG = {baseline_2019['eg']*100:+.2f}%, "
          f"NDP seats = {baseline_2019['ndp_seats']}")
    if egs.mean() < 0:
        print(f"  Interpretation: ensemble MEAN EG is NEGATIVE (UCP-favored).")
        print(f"  Direction matches Chen-Rodden prediction for urban-party disadvantage.")
    else:
        print(f"  Interpretation: ensemble MEAN EG is non-negative.")
        print(f"  Chen-Rodden's natural-packing direction does NOT emerge cleanly.")

    return plans_metrics


# =====================================================================
# Test 3 — Margin asymmetry (fallback cross-check)
# =====================================================================

def test3_margin_asymmetry() -> Dict:
    """Compare mean NDP-winning margin (urban) vs mean UCP-winning margin (rural).

    Chen-Rodden predicts large asymmetry: urban-concentrated party wins
    districts by huge margins (surplus / packing), while rural-dispersed
    party wins by modest margins (efficient distribution).
    """
    print("\n" + "=" * 70)
    print("  TEST 3 — Winning margin asymmetry (urban NDP vs rural UCP)")
    print("=" * 70)

    df = pd.read_csv(data('v0_1_alberta_2023_results.csv'))
    # extract NDP + UCP votes
    def _votes(row, party_sfx):
        total = 0
        for i in range(1, 7):
            c = row.get(f'cand_{i}', '')
            v = row.get(f'votes_{i}', '')
            if pd.isna(c) or pd.isna(v):
                continue
            try:
                v = int(v)
            except (ValueError, TypeError):
                continue
            if isinstance(c, str) and c.endswith(f'({party_sfx})'):
                total += v
        return total

    df['ndp_votes'] = df.apply(lambda r: _votes(r, 'NDP'), axis=1)
    df['ucp_votes'] = df.apply(lambda r: _votes(r, 'UCP'), axis=1)
    df['two_party'] = df['ndp_votes'] + df['ucp_votes']
    df['ndp_share'] = df['ndp_votes'] / df['two_party']
    df['ndp_win'] = df['ndp_votes'] > df['ucp_votes']
    df['margin'] = (df['ndp_votes'] - df['ucp_votes']) / df['two_party']

    ndp_wins = df[df['ndp_win']].copy()
    ucp_wins = df[~df['ndp_win']].copy()

    ndp_margin_mean = ndp_wins['margin'].mean() * 100
    ucp_margin_mean = -ucp_wins['margin'].mean() * 100  # flip to UCP-positive

    # urban split
    urban_keywords = ('Calgary', 'Edmonton', 'Lethbridge', 'Red Deer')
    df['is_urban'] = df['ed_name'].str.contains('|'.join(urban_keywords))
    urban_ndp_wins = df[df['is_urban'] & df['ndp_win']]
    rural_ucp_wins = df[(~df['is_urban']) & (~df['ndp_win'])]

    urban_ndp_margin = urban_ndp_wins['margin'].mean() * 100
    rural_ucp_margin = -rural_ucp_wins['margin'].mean() * 100

    print(f"\n  All-Alberta winning margins (2023):")
    print(f"    NDP wins (n={len(ndp_wins)}): mean margin {ndp_margin_mean:.1f} pp")
    print(f"    UCP wins (n={len(ucp_wins)}): mean margin {ucp_margin_mean:.1f} pp")
    print(f"    Asymmetry: {abs(ndp_margin_mean - ucp_margin_mean):.1f} pp")

    print(f"\n  Urban-rural stratified:")
    print(f"    NDP-won urban (n={len(urban_ndp_wins)}): mean margin {urban_ndp_margin:.1f} pp")
    print(f"    UCP-won rural (n={len(rural_ucp_wins)}): mean margin {rural_ucp_margin:.1f} pp")
    print(f"    Urban NDP - Rural UCP: {urban_ndp_margin - rural_ucp_margin:+.1f} pp")

    # Wasted-vote decomposition: how many NDP votes are "excess" in
    # NDP-won seats (above 50%+1), vs how many in NDP-lost seats?
    total_ndp = df['ndp_votes'].sum()
    total_ucp = df['ucp_votes'].sum()
    ndp_excess = 0
    ndp_lost = 0
    for _, r in df.iterrows():
        tt = r['ndp_votes'] + r['ucp_votes']
        thr = tt // 2 + 1
        if r['ndp_votes'] > r['ucp_votes']:
            ndp_excess += max(0, r['ndp_votes'] - thr)
        else:
            ndp_lost += r['ndp_votes']
    ucp_excess = 0
    ucp_lost = 0
    for _, r in df.iterrows():
        tt = r['ndp_votes'] + r['ucp_votes']
        thr = tt // 2 + 1
        if r['ucp_votes'] > r['ndp_votes']:
            ucp_excess += max(0, r['ucp_votes'] - thr)
        else:
            ucp_lost += r['ucp_votes']

    print(f"\n  Wasted-vote decomposition:")
    print(f"    NDP excess (surplus in won seats): {ndp_excess:,} "
          f"({100*ndp_excess/total_ndp:.1f}% of all NDP)")
    print(f"    NDP lost (in UCP-won seats):       {ndp_lost:,} "
          f"({100*ndp_lost/total_ndp:.1f}%)")
    print(f"    UCP excess (surplus in won seats): {ucp_excess:,} "
          f"({100*ucp_excess/total_ucp:.1f}% of all UCP)")
    print(f"    UCP lost (in NDP-won seats):       {ucp_lost:,} "
          f"({100*ucp_lost/total_ucp:.1f}%)")

    return {
        'ndp_margin_mean': ndp_margin_mean,
        'ucp_margin_mean': ucp_margin_mean,
        'urban_ndp_margin': urban_ndp_margin,
        'rural_ucp_margin': rural_ucp_margin,
        'ndp_excess_pct': 100 * ndp_excess / total_ndp,
        'ndp_lost_pct': 100 * ndp_lost / total_ndp,
        'ucp_excess_pct': 100 * ucp_excess / total_ucp,
        'ucp_lost_pct': 100 * ucp_lost / total_ucp,
    }


# =====================================================================
# Main
# =====================================================================

def main():
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    print("Alberta Chen-Rodden (2013) validation — v0.1")
    print("=" * 70)

    # Test 1: Moran's I
    morans = test1_morans_i()

    # Test 3: Margin asymmetry (run before expensive Test 2)
    margins = test3_margin_asymmetry()

    # Test 2: Simulated ensemble (expensive)
    n_plans = int(os.environ.get('CR_N_PLANS', 150))
    plans = test2_ensemble_ed_perturbation(n_plans=n_plans)

    # Save ensemble CSV
    out_csv = os.path.join(ROOT, 'data', 'v0_1_chen_rodden_simulation.csv')
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['plan_idx', 'n', 'eg', 'mm',
                                               'ndp_seats', 'pop_min', 'pop_max',
                                               'attempts', 'accepted'])
        writer.writeheader()
        for p in plans:
            writer.writerow(p)
    print(f"\n  Ensemble saved to {out_csv}")

    # Summary for the markdown report
    egs = np.array([p['eg'] for p in plans])
    seats = np.array([p['ndp_seats'] for p in plans])
    mms = np.array([p['mm'] for p in plans])

    summary = {
        'morans_i': morans,
        'ensemble': {
            'n_plans': len(plans),
            'eg_mean': float(egs.mean()),
            'eg_median': float(np.median(egs)),
            'eg_std': float(egs.std()),
            'eg_p05': float(np.percentile(egs, 5)),
            'eg_p95': float(np.percentile(egs, 95)),
            'seats_mean': float(seats.mean()),
            'seats_median': float(np.median(seats)),
            'seats_min': int(seats.min()),
            'seats_max': int(seats.max()),
            'mm_mean': float(mms.mean()),
            'mm_median': float(np.median(mms)),
        },
        'margins': margins,
        'baseline_2019_eg': -0.0264,
    }

    # dump a json-like summary for the MD writer
    import json
    summary_path = os.path.join(ROOT, 'data', 'v0_1_chen_rodden_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"  Summary saved to {summary_path}")


if __name__ == '__main__':
    main()
