"""
Alberta Electoral Boundaries — Rigorous Packing/Cracking Analysis
==================================================================
v0.1 — April 22, 2026

Computes the four canonical academic tests for partisan gerrymandering 
(Stephanopoulos & McGhee 2014; McDonald & Best 2015) on:
  - 2019 boundaries (currently in force) under 2023 vote shares
  - Minority 2026 proposal (estimated) under 2023 vote shares

Tests:
  B1: Vote distribution histogram
  B2: Efficiency gap
  B3: Mean-median difference
  B4: Seats-votes curve under uniform swing

Inputs:
  v0_1_alberta_2023_results.csv      — 87 EDs, candidate-level 2023 totals
  v0_1_minority_2026_populations.csv — 89 minority-proposed EDs

Outputs:
  Console summary of all four tests for both map proposals plus a
  side-by-side comparison.

Limits:
  - Without proposed boundary shapefiles, minority hybrid EDs are 
    estimated by blending the urban core's 2023 vote with rural averages.
  - Rural blend uses a 70/30 (urban/rural) weighting and a 33.5% NDP / 
    66.5% UCP rural baseline. This is conservative — actual rural areas 
    the minority absorbs (Bearspaw, Springbank, Cochrane town, Chestermere) 
    are wealthier UCP strongholds, not average rural Alberta.
  - Test B5 (Markov Chain Monte Carlo ensemble comparison via GerryChain) 
    requires shapefiles ABEBC has not released. Not run.
  - Majority 2026 plan not included — requires extraction of majority's 
    per-ED populations from Appendix B (pp. 87–266) of the report PDF.
"""

import csv
import statistics
from typing import Dict, List, Tuple


def load_2023_results(path: str = None) -> List[Dict]:
    if path is None:
        import os
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(here, '..', 'data', 'v0_1_alberta_2023_results.csv'),
            os.path.join(here, 'v0_1_alberta_2023_results.csv'),
            'v0_1_alberta_2023_results.csv',
            os.path.join('data', 'v0_1_alberta_2023_results.csv'),
        ]
        for c in candidates:
            if os.path.exists(c):
                path = c
                break
        if path is None:
            raise FileNotFoundError('Could not find v0_1_alberta_2023_results.csv')
    """Load 87 EDs, return list of dicts with NDP and UCP vote totals."""
    out = []
    with open(path) as f:
        for r in csv.DictReader(f):
            ndp = ucp = 0
            for i in range(1, 7):
                cand = r.get(f'cand_{i}', '')
                votes = r.get(f'votes_{i}', '')
                if not cand or not votes:
                    continue
                try:
                    votes = int(votes)
                except ValueError:
                    continue
                if cand.endswith('(NDP)'):
                    ndp = votes
                elif cand.endswith('(UCP)'):
                    ucp = votes
            if (ndp + ucp) == 0:
                continue
            out.append({
                'ed': r['ed_name'], 'region': r['region'],
                'ndp': ndp, 'ucp': ucp,
            })
    return out


def compute_metrics(districts: List[Dict], label: str) -> Dict:
    """Run the four canonical tests and print results.
    
    districts: list of dicts with keys 'ed', 'ndp', 'ucp'
    """
    n = len(districts)
    total_ndp = sum(d['ndp'] for d in districts)
    total_ucp = sum(d['ucp'] for d in districts)
    total = total_ndp + total_ucp
    prov_ndp = total_ndp / total
    
    n_ndp_wins = sum(1 for d in districts if d['ndp'] > d['ucp'])
    n_ucp_wins = n - n_ndp_wins
    
    # B1: Vote distribution histogram
    margins = [(d['ndp'] - d['ucp']) / (d['ndp'] + d['ucp']) * 100 for d in districts]
    bins = [(-100,-25), (-25,-15), (-15,-10), (-10,-5), (-5,0), 
            (0,5), (5,10), (10,15), (15,25), (25,100)]
    bin_counts = [sum(1 for m in margins if lo <= m < hi) for lo, hi in bins]
    
    # B2: Efficiency gap
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
    eg = (ndp_wasted - ucp_wasted) / total
    
    # B3: Mean-median
    shares = [d['ndp'] / (d['ndp'] + d['ucp']) for d in districts]
    mn = statistics.mean(shares)
    md = statistics.median(shares)
    mm_gap = mn - md
    
    # B4: Seats-votes at 50/50 (uniform swing)
    swing = 0.5 - prov_ndp
    swung_shares = [s + swing for s in shares]
    ndp_at_50 = sum(1 for s in swung_shares if s > 0.5)
    ucp_at_50 = n - ndp_at_50
    
    # Print
    print(f"\n{'='*60}\n  {label}\n{'='*60}")
    print(f"  Districts: {n}")
    print(f"  Province two-party: NDP {prov_ndp*100:.2f}%, UCP {(1-prov_ndp)*100:.2f}%")
    print(f"  Actual seats: NDP {n_ndp_wins}, UCP {n_ucp_wins}")
    print(f"\n  B1: Vote distribution (margin in two-party share)")
    labels = ['UCP +25%+','UCP 15-25','UCP 10-15','UCP 5-10','UCP 0-5',
              'NDP 0-5','NDP 5-10','NDP 10-15','NDP 15-25','NDP +25%+']
    for label_i, count in zip(labels, bin_counts):
        print(f"    {label_i:>12s}: {'█' * count} {count}")
    print(f"\n  B2: Efficiency gap = {eg*100:+.2f}%  "
          f"({'within' if abs(eg) < 0.07 else 'EXCEEDS'} 7% threshold)")
    print(f"  B3: Mean-median gap (NDP) = {mm_gap*100:+.2f} pp  "
          f"({'within' if abs(mm_gap) < 0.03 else 'EXCEEDS'} 3 pp threshold)")
    print(f"  B4: At 50/50 vote: NDP {ndp_at_50}, UCP {ucp_at_50} "
          f"(asymmetry: {abs(ndp_at_50-ucp_at_50)} seats)")
    
    return {
        'label': label, 'n': n, 'prov_ndp': prov_ndp,
        'ndp_seats': n_ndp_wins, 'ucp_seats': n_ucp_wins,
        'eg': eg, 'mm_gap': mm_gap,
        'ndp_at_50': ndp_at_50, 'ucp_at_50': ucp_at_50,
        'bin_counts': bin_counts,
    }


def estimate_minority_2026(dists_2019: List[Dict], 
                           rural_ndp_share: float = 0.335,
                           urban_weight: float = 0.7) -> List[Dict]:
    """Estimate minority 2026 ED-level vote totals.
    
    Pure renames use the existing 2019 ED's totals directly.
    Hybrids blend the urban core's vote with a rural baseline.
    Edmonton's inner-core 6→5 merger combines two existing EDs.
    """
    by_name = {d['ed']: d for d in dists_2019}
    
    def get(ed_name):
        return by_name.get(ed_name)
    
    def rural_blend(urban_ed_name, urban_w=urban_weight):
        """Blend urban ED with rural average to simulate hybrid."""
        base = get(urban_ed_name)
        if not base:
            return None
        urban_total = base['ndp'] + base['ucp']
        urban_ndp_share = base['ndp'] / urban_total
        rural_w = 1 - urban_w
        blended = urban_w * urban_ndp_share + rural_w * rural_ndp_share
        new_total = urban_total * (urban_w + rural_w * 0.7)  # rural turnout slightly lower
        return {
            'ndp': int(new_total * blended),
            'ucp': int(new_total * (1 - blended)),
        }
    
    estimates = {}
    
    # Calgary direct renames
    direct_calgary = {
        'Calgary-Acadia': 'Calgary-Acadia',
        'Calgary-Beddington': 'Calgary-Beddington',
        'Calgary-Buffalo': 'Calgary-Buffalo',
        'Calgary-Cross': 'Calgary-Cross',
        'Calgary-Currie': 'Calgary-Currie',
        'Calgary-East': 'Calgary-East',
        'Calgary-Edgemont': 'Calgary-Edgemont',
        'Calgary-Elbow': 'Calgary-Elbow',
        'Calgary-Falconridge': 'Calgary-Falconridge',
        'Calgary-Fish Creek': 'Calgary-Fish Creek',
        'Calgary-Glenmore': 'Calgary-Glenmore',
        'Calgary-Hays': 'Calgary-Hays',
        'Calgary-Klein': 'Calgary-Klein',
        'Calgary-Lougheed': 'Calgary-Lougheed',
        'Calgary-McCall-Bhullar': 'Calgary-Bhullar-McCall',
        'Calgary-Mountain View': 'Calgary-Mountain View',
        'Calgary-North': 'Calgary-North',
        'Calgary-North East': 'Calgary-North East',
        'Calgary-South East': 'Calgary-South East',
        'Calgary-Varsity': 'Calgary-Varsity',
    }
    for new_ed, base_ed in direct_calgary.items():
        b = get(base_ed)
        if b:
            estimates[new_ed] = {'ndp': b['ndp'], 'ucp': b['ucp']}
    
    # Calgary hybrids
    calgary_hybrids = {
        'Calgary-Bow-Springbank':           ('Calgary-Bow', 0.75),
        'Calgary-De Winton':                 ('Calgary-Fish Creek', 0.5),
        'Calgary-Foothills-Airdrie West':    ('Calgary-Foothills', 0.7),
        'Calgary-Nolan Hill-Cochrane':       ('Calgary-Edgemont', 0.55),
        'Calgary-North West-Bearspaw':       ('Calgary-North West', 0.85),
        'Calgary-Peigan-Chestermere':        ('Calgary-Peigan', 0.7),
        "Calgary-West-Tsuut'ina":            ('Calgary-West', 0.85),
    }
    for new_ed, (base_ed, w) in calgary_hybrids.items():
        r = rural_blend(base_ed, w)
        if r:
            estimates[new_ed] = r
    
    # Calgary-Airdrie: half of Airdrie-Cochrane
    ac = get('Airdrie-Cochrane')
    if ac:
        estimates['Calgary-Airdrie'] = {'ndp': ac['ndp']//2, 'ucp': ac['ucp']//2}
    
    # Calgary-South ≈ Calgary-Shaw (renamed)
    sh = get('Calgary-Shaw')
    if sh:
        estimates['Calgary-South'] = {'ndp': sh['ndp'], 'ucp': sh['ucp']}
    
    # Edmonton direct renames + windermere
    direct_edmonton = {
        'Edmonton-Beverly-Clareview': 'Edmonton-Beverly-Clareview',
        'Edmonton-Castledowns': 'Edmonton-Castle Downs',
        'Edmonton-City Centre': 'Edmonton-City Centre',
        'Edmonton-Decore': 'Edmonton-Decore',
        'Edmonton-Ellerslie': 'Edmonton-Ellerslie',
        'Edmonton-Gold Bar': 'Edmonton-Gold Bar',
        'Edmonton-Highlands-Norwood': 'Edmonton-Highlands-Norwood',
        'Edmonton-Manning': 'Edmonton-Manning',
        'Edmonton-McClung': 'Edmonton-McClung',
        'Edmonton-Meadows': 'Edmonton-Meadows',
        'Edmonton-Mill Woods': 'Edmonton-Mill Woods',
        'Edmonton-North West': 'Edmonton-North West',
        'Edmonton-Rutherford': 'Edmonton-Rutherford',
        'Edmonton-South': 'Edmonton-South',
        'Edmonton-Strathcona': 'Edmonton-Strathcona',
        'Edmonton-West Henday': 'Edmonton-West Henday',
        'Edmonton-Whitemud': 'Edmonton-Whitemud',
        'Edmonton-Windermere': 'Edmonton-South West',
    }
    for new_ed, base_ed in direct_edmonton.items():
        b = get(base_ed)
        if b:
            estimates[new_ed] = {'ndp': b['ndp'], 'ucp': b['ucp']}
    
    # Edmonton-Glenora-Riverview: merger of Glenora + most of Riverview
    g = get('Edmonton-Glenora'); r = get('Edmonton-Riverview')
    if g and r:
        estimates['Edmonton-Glenora-Riverview'] = {
            'ndp': g['ndp'] + int(r['ndp']*0.6),
            'ucp': g['ucp'] + int(r['ucp']*0.6),
        }
    
    # Edmonton hybrids
    edmonton_hybrids = {
        'Edmonton-Beaumont':     ('Edmonton-South', 0.6),
        'Edmonton-Enoch-Devon':  ('Edmonton-West Henday', 0.5),
        'Edmonton-Spruce Grove': ('Edmonton-West Henday', 0.4),
    }
    for new_ed, (base_ed, w) in edmonton_hybrids.items():
        rb = rural_blend(base_ed, w)
        if rb:
            estimates[new_ed] = rb
    
    # Rest of Alberta direct renames
    rest_direct = {
        'Airdrie East': 'Airdrie-East',
        'Barrhead-Westlock-Athabasca': 'Athabasca-Barrhead-Westlock',
        'Camrose': 'Camrose',
        'Canmore-Kananaskis': 'Banff-Kananaskis',
        'Cold Lake-Bonnyville-St. Paul': 'Bonnyville-Cold Lake-St. Paul',
        'Central Peace-Notley': 'Central Peace-Notley',
        'Chestermere-Strathmore': 'Chestermere-Strathmore',
        'Drumheller-Stettler': 'Drumheller-Stettler',
        'Fort McMurray-Lac La Biche': 'Fort McMurray-Lac La Biche',
        'Fort McMurray-Wood Buffalo': 'Fort McMurray-Wood Buffalo',
        'Fort Saskatchewan-Vegreville': 'Fort Saskatchewan-Vegreville',
        'Grande Prairie': 'Grande Prairie',
        'Grande Prairie-Wapiti': 'Grande Prairie-Wapiti',
        'Highwood': 'Highwood',
        'Lac Ste. Anne-Parkland': 'Lac Ste. Anne-Parkland',
        'Leduc': 'Leduc-Beaumont',
        'Lesser Slave Lake': 'Lesser Slave Lake',
        'Lloydminster-Wainwright': 'Vermilion-Lloydminster-Wainwright',
        'Medicine Hat-Brooks': 'Brooks-Medicine Hat',
        'Medicine Hat-Cypress': 'Cypress-Medicine Hat',
        'Olds-Three Hills-Didsbury': 'Olds-Didsbury-Three Hills',
        'Peace River': 'Peace River',
        'Rocky Mountain House-Banff Park': 'Rimbey-Rocky Mountain House-Sundre',
        'Sherwood Park': 'Sherwood Park',
        'St. Albert': 'St. Albert',
        'Stony Plain-Drayton Valley': 'Drayton Valley-Devon',
        'Sherwood Park-Strathcona': 'Strathcona-Sherwood Park',
        'West Yellowhead': 'West Yellowhead',
        'Wetaskawin-Ponoka-Maskwacis': 'Maskwacis-Wetaskiwin',
    }
    for new_ed, base_ed in rest_direct.items():
        b = get(base_ed)
        if b:
            estimates[new_ed] = {'ndp': b['ndp'], 'ucp': b['ucp']}
    
    # Rest of Alberta hybrids/restructures
    rest_hybrids = {
        'St. Albert-Sturgeon':                       ('Morinville-St. Albert', 0.7),
        'Lethbridge-Fort MacLeod-Crowsnest Pass':    ('Lethbridge-West', 0.55),
        'Lethbridge-Cardston':                       ('Lethbridge-West', 0.4),
        'Lethbridge-Little Bow':                     ('Lethbridge-East', 0.45),
        'Lethbridge-Taber-Warner':                   ('Taber-Warner', 0.5),
        'Red Deer-Lacombe':                          ('Lacombe-Ponoka', 0.4),
        'Red Deer-Innisfail':                        ('Innisfail-Sylvan Lake', 0.4),
    }
    for new_ed, (base_ed, w) in rest_hybrids.items():
        rb = rural_blend(base_ed, w)
        if rb:
            estimates[new_ed] = rb
    
    # Red Deer split into 4 hybrids — Blackfalds and Sylvan Lake combine RD halves with adjacent
    rd_n = get('Red Deer-North'); rd_s = get('Red Deer-South')
    lp = get('Lacombe-Ponoka'); isl = get('Innisfail-Sylvan Lake')
    if rd_n and lp:
        estimates['Red Deer-Blackfalds'] = {
            'ndp': int(rd_n['ndp']*0.5) + int(lp['ndp']*0.2),
            'ucp': int(rd_n['ucp']*0.5) + int(lp['ucp']*0.2),
        }
    if rd_s and isl:
        estimates['Red Deer-Sylvan Lake'] = {
            'ndp': int(rd_s['ndp']*0.5) + int(isl['ndp']*0.3),
            'ucp': int(rd_s['ucp']*0.5) + int(isl['ucp']*0.3),
        }
    
    # Convert to district list
    return [{'ed': k, 'ndp': v['ndp'], 'ucp': v['ucp']} for k, v in estimates.items()]


def main():
    dists_2019 = load_2023_results()
    
    # Compute rural baseline for blending
    rural = [d for d in dists_2019 if d['region'] == 'Rest of Alberta']
    rural_ndp = sum(d['ndp'] for d in rural) / sum(d['ndp']+d['ucp'] for d in rural)
    print(f"Rural Alberta baseline NDP two-party: {rural_ndp*100:.1f}%")
    
    m_2019 = compute_metrics(dists_2019, "2019 BOUNDARIES (CURRENT) under 2023 vote shares")
    
    minority_dists = estimate_minority_2026(dists_2019, rural_ndp_share=rural_ndp)
    print(f"\nMinority 2026: {len(minority_dists)} of 89 EDs estimated")
    m_min = compute_metrics(minority_dists, "MINORITY 2026 PROPOSAL (estimated) under 2023 vote shares")
    
    print(f"\n{'='*60}\n  COMPARISON\n{'='*60}")
    print(f"  Metric                | 2019    | Minority | Shift")
    print(f"  Efficiency gap        | {m_2019['eg']*100:+.2f}% | {m_min['eg']*100:+.2f}%   | {(m_min['eg']-m_2019['eg'])*100:+.2f} pp")
    print(f"  Mean-median (NDP)     | {m_2019['mm_gap']*100:+.2f}pp | {m_min['mm_gap']*100:+.2f}pp  | {(m_min['mm_gap']-m_2019['mm_gap'])*100:+.2f} pp")
    print(f"  NDP seats at 50/50    | {m_2019['ndp_at_50']:>7d} | {m_min['ndp_at_50']:>8d} | {m_min['ndp_at_50']-m_2019['ndp_at_50']:+d}")
    print(f"  Sim seats (NDP/UCP)   | {m_2019['ndp_seats']}/{m_2019['ucp_seats']}   | {m_min['ndp_seats']}/{m_min['ucp_seats']}    |")


if __name__ == '__main__':
    main()
