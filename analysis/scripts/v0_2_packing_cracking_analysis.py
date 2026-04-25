"""
Alberta Electoral Boundaries — Packing/Cracking Analysis (v0.2)
===============================================================
Symmetric three-map version. Fixes the v0.1 script's Class-A bias issues:

  A1: v0.1 computed B1-B4 only for 2019 and minority 2026. Majority 2026
      was asserted in reports without reproducible provenance. v0.2 adds
      estimate_majority_2026() so all three maps are computable from
      checked-in data.

  A2: v0.1 docstring described rural blending as "conservative" (a
      direction-loaded term presupposing the finding) and characterized
      specific rural areas as "UCP strongholds". v0.2 uses neutral
      descriptive language. The runtime-computed rural NDP share stands
      as empirical — the framing of what that share means is moved to
      the section MD and written as an observation, not a pre-committed
      interpretation.

Tests computed (Stephanopoulos & McGhee 2014; McDonald & Best 2015):

  B1: Vote distribution histogram by ED margin
  B2: Efficiency gap = (W_NDP - W_UCP) / N
  B3: Mean-median difference in NDP vote share
  B4: Seats-votes curve at 50/50 under uniform swing

Inputs:
  data/v0_1_alberta_2023_results.csv      — 87 EDs, candidate-level 2023
  data/v0_1_majority_2026_populations.csv — 89 majority EDs
  data/v0_1_minority_2026_populations.csv — 89 minority EDs

Methodology note on 2026 attribution:

  Neither 2026 proposal has released polygon shapefiles yet. 2023 votes
  must be attributed to 2026 EDs via name-based or blended approximation
  rather than measured via spatial join. This script applies the same
  blending rule symmetrically to both 2026 proposals:

    - Direct rename: the 2026 ED covers approximately the same territory
      as a 2019 ED (possibly with minor boundary shifts). Use the 2019
      ED's votes directly.

    - Hybrid: the 2026 ED combines an urban core (2019 ED) with a rural
      or suburban absorption. Blend 2019 urban-core votes with the
      2023-observed Rest-of-Alberta baseline using urban_weight = 0.70.
      This 70/30 urban/rural weight is applied identically to both maps
      so any magnitude comparison between them is apples-to-apples.

  Where a 2026 ED is a reorganization of 2019 EDs (splitting an urban
  into two halves, merging two urban EDs, etc.), the mapping is explicit
  in the MAJORITY_2026_MAPPING / MINORITY_2026_MAPPING dictionaries
  below.

  Limits:
    - 70/30 is a modeling choice. Sensitivity testing under alternative
      weights (60/40, 80/20) is included at the end of main() and
      reported in the output.
    - Phase 4C measured attribution (when executed) replaces this
      approximation entirely. Results from this script are intermediate
      estimates suitable for direction-of-shift analysis; magnitude
      precision requires the measured version.
"""

import csv
import statistics
import os
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------

def _find_data(filename: str) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    # Script lives at <repo>/analysis/scripts/, so '../../data' = <repo>/data
    for p in [os.path.join(here, '..', '..', 'data', filename),
              os.path.join(here, '..', 'data', filename),
              os.path.join(here, 'data', filename),
              os.path.join('data', filename),
              filename]:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(filename)


def load_2023_results() -> List[Dict]:
    """Load 87 EDs with 2023 NDP+UCP totals per ED, plus region."""
    out = []
    with open(_find_data('v0_1_alberta_2023_results.csv')) as f:
        for r in csv.DictReader(f):
            ndp = ucp = 0
            for i in range(1, 7):
                cand = r.get(f'cand_{i}', '') or ''
                votes = r.get(f'votes_{i}', '') or ''
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
            if ndp + ucp == 0:
                continue
            out.append({
                'ed': r['ed_name'], 'region': r['region'],
                'ndp': ndp, 'ucp': ucp,
            })
    return out


# ---------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------

def compute_metrics(districts: List[Dict], label: str, *, verbose: bool = True) -> Dict:
    n = len(districts)
    total_ndp = sum(d['ndp'] for d in districts)
    total_ucp = sum(d['ucp'] for d in districts)
    total = total_ndp + total_ucp
    prov_ndp = total_ndp / total

    n_ndp_wins = sum(1 for d in districts if d['ndp'] > d['ucp'])
    n_ucp_wins = n - n_ndp_wins

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

    # B4: 50/50 uniform swing
    swing = 0.5 - prov_ndp
    swung = [s + swing for s in shares]
    ndp_at_50 = sum(1 for s in swung if s > 0.5)
    ucp_at_50 = n - ndp_at_50

    # B6: Declination (Warrington 2018)
    # Measure asymmetry in winning-district distributions by computing
    # the angle between two reference points (mean NDP-won share, mean
    # UCP-won share) relative to the 50/50 line, normalized to [-1, 1].
    ndp_won_shares = [s for s in shares if s > 0.5]
    ucp_won_shares = [s for s in shares if s < 0.5]
    if ndp_won_shares and ucp_won_shares:
        import math
        mean_ndp_won = statistics.mean(ndp_won_shares)
        mean_ucp_won = statistics.mean(ucp_won_shares)
        # Declination formula: angle between vectors (n_ndp_wins/n, mean_ndp_won - 0.5)
        # and (n_ucp_wins/n, 0.5 - mean_ucp_won), normalized by pi/2.
        # Positive = pro-NDP; negative = pro-UCP.
        theta_ndp = math.atan2(mean_ndp_won - 0.5, n_ndp_wins / n)
        theta_ucp = math.atan2(0.5 - mean_ucp_won, n_ucp_wins / n)
        declination = (theta_ndp - theta_ucp) * 2 / math.pi
    else:
        declination = float('nan')  # one party swept

    if verbose:
        print(f"\n{'='*60}\n  {label}\n{'='*60}")
        print(f"  Districts: {n}")
        print(f"  Province two-party: NDP {prov_ndp*100:.2f}%, UCP {(1-prov_ndp)*100:.2f}%")
        print(f"  Actual seats: NDP {n_ndp_wins}, UCP {n_ucp_wins}")
        labels = ['UCP +25%+','UCP 15-25','UCP 10-15','UCP 5-10','UCP 0-5',
                  'NDP 0-5','NDP 5-10','NDP 10-15','NDP 15-25','NDP +25%+']
        print(f"\n  B1: Vote distribution (margin in two-party share)")
        for lbl, count in zip(labels, bin_counts):
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


# ---------------------------------------------------------------------
# 2026 ED estimation — symmetric blending rule
# ---------------------------------------------------------------------

# Each 2026 ED maps to either:
#   ('direct', '<2019 ED name>')             -> use 2019 votes directly
#   ('blend', '<2019 ED name>', urban_weight) -> blend with rural baseline
#   ('merge', ['<2019 ED 1>', '<2019 ED 2>'], [w1, w2])
#       -> combine two 2019 EDs with given weights (urban+urban merge)
#   ('split', '<2019 ED>', urban_weight, split_fraction)
#       -> take a fraction of a 2019 ED, then apply blending
#
# urban_weight = 0.85 for all non-special blends (applied symmetrically).
# Derived from commission-published population targets: for each hybrid ED,
# parent_2019_pop / total_2026_pop. Majority hybrid mean = 0.876, minority
# mean = 0.830. Flat 0.85 is the best single-value estimate. Prior value 0.70
# was arbitrary. Sensitivity analysis covers 0.70 / 0.85 / 0.90.

URBAN_WEIGHT_DEFAULT = 0.85

MAJORITY_2026_MAPPING = {
    # Calgary direct renames (cover same urban neighborhood)
    'Calgary-Acadia':           ('direct', 'Calgary-Acadia'),
    'Calgary-Beddington':       ('direct', 'Calgary-Beddington'),
    'Calgary-Bhullar-McCall':   ('direct', 'Calgary-Bhullar-McCall'),
    'Calgary-Bow':              ('direct', 'Calgary-Bow'),
    'Calgary-Buffalo':          ('direct', 'Calgary-Buffalo'),
    'Calgary-Confluence':       ('direct', 'Calgary-Buffalo'),  # new central ED
    'Calgary-Cross':            ('direct', 'Calgary-Cross'),
    'Calgary-Currie':           ('direct', 'Calgary-Currie'),
    'Calgary-Edgemont':         ('direct', 'Calgary-Edgemont'),
    'Calgary-Elbow':            ('direct', 'Calgary-Elbow'),
    'Calgary-Fish Creek':       ('direct', 'Calgary-Fish Creek'),
    'Calgary-Hays':             ('direct', 'Calgary-Hays'),
    'Calgary-Klein':            ('direct', 'Calgary-Klein'),
    'Calgary-Lougheed':         ('direct', 'Calgary-Lougheed'),
    'Calgary-McKenzie':         ('direct', 'Calgary-Hays'),  # SE area
    'Calgary-Mountain View':    ('direct', 'Calgary-Mountain View'),
    'Calgary-North':            ('direct', 'Calgary-North'),
    'Calgary-North East':       ('direct', 'Calgary-North East'),
    'Calgary-North West':       ('direct', 'Calgary-North West'),
    'Calgary-Nose Creek':       ('direct', 'Calgary-Beddington'),
    'Calgary-Shaw':             ('direct', 'Calgary-Shaw'),
    'Calgary-South East':       ('direct', 'Calgary-South East'),
    'Calgary-Symons Valley':    ('direct', 'Calgary-North West'),
    'Calgary-Varsity':          ('direct', 'Calgary-Varsity'),

    # Calgary hybrids (urban core + rural/suburban absorption)
    'Calgary-East':                ('blend', 'Calgary-East', URBAN_WEIGHT_DEFAULT),
    'Calgary-Falconridge-Conrich': ('blend', 'Calgary-Falconridge', URBAN_WEIGHT_DEFAULT),
    'Calgary-Glenmore-Tsuut\'ina': ('blend', 'Calgary-Glenmore', URBAN_WEIGHT_DEFAULT),
    'Calgary-West-Elbow Valley':   ('blend', 'Calgary-West', URBAN_WEIGHT_DEFAULT),

    # Edmonton direct renames
    'Edmonton-Beverly-Clareview': ('direct', 'Edmonton-Beverly-Clareview'),
    'Edmonton-Castle Downs':      ('direct', 'Edmonton-Castle Downs'),
    'Edmonton-City Centre':       ('direct', 'Edmonton-City Centre'),
    'Edmonton-Decore':            ('direct', 'Edmonton-Decore'),
    'Edmonton-Ellerslie':         ('direct', 'Edmonton-Ellerslie'),
    'Edmonton-Gold Bar':          ('direct', 'Edmonton-Gold Bar'),
    'Edmonton-Highlands-Norwood': ('direct', 'Edmonton-Highlands-Norwood'),
    'Edmonton-Manning':           ('direct', 'Edmonton-Manning'),
    'Edmonton-McClung':           ('direct', 'Edmonton-McClung'),
    'Edmonton-Meadows':           ('direct', 'Edmonton-Meadows'),
    'Edmonton-Mill Woods':        ('direct', 'Edmonton-Mill Woods'),
    'Edmonton-North West':        ('direct', 'Edmonton-North West'),
    'Edmonton-Rutherford':        ('direct', 'Edmonton-Rutherford'),
    'Edmonton-South':             ('direct', 'Edmonton-South'),
    'Edmonton-Strathcona':        ('direct', 'Edmonton-Strathcona'),
    'Edmonton-West Henday':       ('direct', 'Edmonton-West Henday'),
    'Edmonton-Whitemud':          ('direct', 'Edmonton-Whitemud'),
    'Edmonton-Windermere':        ('direct', 'Edmonton-South West'),
    'Edmonton-Glenora-Riverview': ('merge', ['Edmonton-Glenora', 'Edmonton-Riverview'], [1.0, 0.4]),

    # Edmonton hybrids
    # Edmonton-Beaumont draws from Leduc-Beaumont 2019 (City of Beaumont is in
    # that district; Edmonton-South 2026 is an identical rename of Edmonton-South
    # 2019, so no territory crosses over).
    'Edmonton-Beaumont':          ('blend', 'Leduc-Beaumont', URBAN_WEIGHT_DEFAULT),
    'Edmonton-Enoch':             ('blend', 'Edmonton-West Henday', URBAN_WEIGHT_DEFAULT),

    # Rest-of-province direct renames
    'Barrhead-Westlock-Athabasca': ('direct', 'Athabasca-Barrhead-Westlock'),
    'Camrose':                     ('direct', 'Camrose'),
    'Canmore-Banff':               ('direct', 'Banff-Kananaskis'),
    'Central Peace-Notley':        ('direct', 'Central Peace-Notley'),
    'Drumheller-Stettler':         ('direct', 'Drumheller-Stettler'),
    'Fort Saskatchewan-Vegreville':('direct', 'Fort Saskatchewan-Vegreville'),
    'Grande Prairie':              ('direct', 'Grande Prairie'),
    'Grande Prairie-Wapiti':       ('direct', 'Grande Prairie-Wapiti'),
    'Lacombe-Clearwater':          ('direct', 'Lacombe-Ponoka'),
    'Livingstone-Macleod':         ('direct', 'Livingstone-Macleod'),
    'Lesser Slave Lake':           ('direct', 'Lesser Slave Lake'),
    'Lloydminster-Wainwright':     ('direct', 'Vermilion-Lloydminster-Wainwright'),
    'Mountain View-Kneehill':      ('direct', 'Olds-Didsbury-Three Hills'),
    'Peace River':                 ('direct', 'Peace River'),
    'Red Deer-North':              ('direct', 'Red Deer-North'),
    'Red Deer-South':              ('direct', 'Red Deer-South'),
    'Sherwood Park':               ('direct', 'Sherwood Park'),
    'Spruce Grove':                ('direct', 'Spruce Grove-Stony Plain'),
    'St. Albert':                  ('direct', 'St. Albert'),
    'Strathcona-Sherwood Park':    ('direct', 'Strathcona-Sherwood Park'),
    'Sylvan Lake-Innisfail':       ('direct', 'Innisfail-Sylvan Lake'),
    'Taber-Cardston':              ('direct', 'Taber-Warner'),
    'West Yellowhead':             ('direct', 'West Yellowhead'),
    'Wetaskiwin-Ponoka-Maskwacis': ('direct', 'Maskwacis-Wetaskiwin'),

    # Rest-of-province hybrids
    # Mappings verified against Appendix C hybrid crosswalk (pg 269) where
    # applicable. See data/v0_1_majority_hybrid_crosswalk.csv for the
    # authoritative list. Corrections from earlier guesses:
    #   Airdrie-East: Appendix C says current Airdrie-East -> proposed
    #     Airdrie-East (direct rename, not a blend).
    #   Medicine Hat-Brooks: current Brooks-Medicine Hat -> proposed
    #     Medicine Hat-Brooks (direct rename; was 'blend' before).
    'Airdrie-East':               ('direct', 'Airdrie-East'),
    'Airdrie-West':               ('blend', 'Airdrie-Cochrane', URBAN_WEIGHT_DEFAULT),
    'Chestermere-Strathmore':     ('direct', 'Chestermere-Strathmore'),
    'Cochrane-Springbank':        ('blend', 'Airdrie-Cochrane', URBAN_WEIGHT_DEFAULT),
    'Cold Lake-Bonnyville-St. Paul': ('direct', 'Bonnyville-Cold Lake-St. Paul'),
    'Fort McMurray-Lac La Biche': ('direct', 'Fort McMurray-Lac La Biche'),
    'Fort McMurray-Wood Buffalo': ('direct', 'Fort McMurray-Wood Buffalo'),
    'High River-Vulcan-Siksika':  ('blend', 'Highwood', URBAN_WEIGHT_DEFAULT),
    'Leduc-Devon':                ('blend', 'Leduc-Beaumont', URBAN_WEIGHT_DEFAULT),
    'Lethbridge-East':            ('blend', 'Lethbridge-East', URBAN_WEIGHT_DEFAULT),
    'Lethbridge-West':            ('blend', 'Lethbridge-West', URBAN_WEIGHT_DEFAULT),
    'Medicine Hat-Brooks':        ('direct', 'Brooks-Medicine Hat'),
    'Medicine Hat-Cypress':       ('direct', 'Cypress-Medicine Hat'),
    'Okotoks-Diamond Valley':     ('blend', 'Highwood', URBAN_WEIGHT_DEFAULT),
    'St. Albert-Sturgeon':        ('blend', 'Morinville-St. Albert', URBAN_WEIGHT_DEFAULT),
    'Stony Plain-Drayton Valley': ('direct', 'Drayton Valley-Devon'),
}

MINORITY_2026_MAPPING = {
    # Calgary direct renames
    'Calgary-Acadia':           ('direct', 'Calgary-Acadia'),
    'Calgary-Beddington':       ('direct', 'Calgary-Beddington'),
    'Calgary-Buffalo':          ('direct', 'Calgary-Buffalo'),
    'Calgary-Cross':            ('direct', 'Calgary-Cross'),
    'Calgary-Currie':           ('direct', 'Calgary-Currie'),
    'Calgary-East':             ('direct', 'Calgary-East'),
    'Calgary-Edgemont':         ('direct', 'Calgary-Edgemont'),
    'Calgary-Elbow':            ('direct', 'Calgary-Elbow'),
    'Calgary-Falconridge':      ('direct', 'Calgary-Falconridge'),
    'Calgary-Fish Creek':       ('direct', 'Calgary-Fish Creek'),
    'Calgary-Glenmore':         ('direct', 'Calgary-Glenmore'),
    'Calgary-Hays':             ('direct', 'Calgary-Hays'),
    'Calgary-Klein':            ('direct', 'Calgary-Klein'),
    'Calgary-Lougheed':         ('direct', 'Calgary-Lougheed'),
    'Calgary-McCall-Bhullar':   ('direct', 'Calgary-Bhullar-McCall'),
    'Calgary-Mountain View':    ('direct', 'Calgary-Mountain View'),
    'Calgary-North':            ('direct', 'Calgary-North'),
    'Calgary-North East':       ('direct', 'Calgary-North East'),
    'Calgary-South East':       ('direct', 'Calgary-South East'),
    'Calgary-Varsity':          ('direct', 'Calgary-Varsity'),

    # Calgary hybrids
    'Calgary-Bow-Springbank':           ('blend', 'Calgary-Bow', URBAN_WEIGHT_DEFAULT),
    'Calgary-De Winton':                ('blend', 'Calgary-Fish Creek', URBAN_WEIGHT_DEFAULT),
    'Calgary-Foothills-Airdrie West':   ('blend', 'Calgary-Foothills', URBAN_WEIGHT_DEFAULT),
    'Calgary-Nolan Hill-Cochrane':      ('blend', 'Calgary-Edgemont', URBAN_WEIGHT_DEFAULT),
    'Calgary-North West-Bearspaw':      ('blend', 'Calgary-North West', URBAN_WEIGHT_DEFAULT),
    'Calgary-Peigan-Chestermere':       ('blend', 'Calgary-Peigan', URBAN_WEIGHT_DEFAULT),
    'Calgary-West-Tsuut\'ina':          ('blend', 'Calgary-West', URBAN_WEIGHT_DEFAULT),
    'Calgary-Airdrie':                  ('split', 'Airdrie-Cochrane', URBAN_WEIGHT_DEFAULT, 0.5),
    'Calgary-South':                    ('direct', 'Calgary-Shaw'),

    # Edmonton direct renames
    'Edmonton-Beverly-Clareview': ('direct', 'Edmonton-Beverly-Clareview'),
    'Edmonton-Castledowns':       ('direct', 'Edmonton-Castle Downs'),
    'Edmonton-City Centre':       ('direct', 'Edmonton-City Centre'),
    'Edmonton-Decore':            ('direct', 'Edmonton-Decore'),
    'Edmonton-Ellerslie':         ('direct', 'Edmonton-Ellerslie'),
    'Edmonton-Gold Bar':          ('direct', 'Edmonton-Gold Bar'),
    'Edmonton-Highlands-Norwood': ('direct', 'Edmonton-Highlands-Norwood'),
    'Edmonton-Manning':           ('direct', 'Edmonton-Manning'),
    'Edmonton-McClung':           ('direct', 'Edmonton-McClung'),
    'Edmonton-Meadows':           ('direct', 'Edmonton-Meadows'),
    'Edmonton-Mill Woods':        ('direct', 'Edmonton-Mill Woods'),
    'Edmonton-North West':        ('direct', 'Edmonton-North West'),
    'Edmonton-Rutherford':        ('direct', 'Edmonton-Rutherford'),
    'Edmonton-South':             ('direct', 'Edmonton-South'),
    'Edmonton-Strathcona':        ('direct', 'Edmonton-Strathcona'),
    'Edmonton-West Henday':       ('direct', 'Edmonton-West Henday'),
    'Edmonton-Whitemud':          ('direct', 'Edmonton-Whitemud'),
    'Edmonton-Windermere':        ('direct', 'Edmonton-South West'),
    'Edmonton-Glenora-Riverview': ('merge', ['Edmonton-Glenora', 'Edmonton-Riverview'], [1.0, 0.6]),

    # Edmonton hybrids
    # Edmonton-Beaumont draws from Leduc-Beaumont 2019 (City of Beaumont);
    # Edmonton-South 2026 is an identical rename with no territory split.
    'Edmonton-Beaumont':     ('blend', 'Leduc-Beaumont', URBAN_WEIGHT_DEFAULT),
    'Edmonton-Enoch-Devon':  ('blend', 'Edmonton-West Henday', URBAN_WEIGHT_DEFAULT),
    'Edmonton-Spruce Grove': ('blend', 'Spruce Grove-Stony Plain', URBAN_WEIGHT_DEFAULT),

    # Rest-of-province direct renames
    'Airdrie East':                           ('direct', 'Airdrie-Cochrane'),
    'Barrhead-Westlock-Athabasca':            ('direct', 'Athabasca-Barrhead-Westlock'),
    'Camrose':                                 ('direct', 'Camrose'),
    'Canmore-Kananaskis':                      ('direct', 'Banff-Kananaskis'),
    'Central Peace-Notley':                    ('direct', 'Central Peace-Notley'),
    'Chestermere-Strathmore':                  ('direct', 'Chestermere-Strathmore'),
    'Cold Lake-Bonnyville-St. Paul':           ('direct', 'Bonnyville-Cold Lake-St. Paul'),
    'Drumheller-Stettler':                     ('direct', 'Drumheller-Stettler'),
    'Fort McMurray-Lac La Biche':              ('direct', 'Fort McMurray-Lac La Biche'),
    'Fort McMurray-Wood Buffalo':              ('direct', 'Fort McMurray-Wood Buffalo'),
    'Fort Saskatchewan-Vegreville':            ('direct', 'Fort Saskatchewan-Vegreville'),
    'Grande Prairie':                          ('direct', 'Grande Prairie'),
    'Grande Prairie-Wapiti':                   ('direct', 'Grande Prairie-Wapiti'),
    'Highwood':                                ('direct', 'Highwood'),
    'Lac Ste. Anne-Parkland':                  ('direct', 'Lac Ste. Anne-Parkland'),
    'Leduc':                                   ('direct', 'Leduc-Beaumont'),
    'Lesser Slave Lake':                       ('direct', 'Lesser Slave Lake'),
    'Lloydminster-Wainwright':                 ('direct', 'Vermilion-Lloydminster-Wainwright'),
    'Medicine Hat-Brooks':                     ('direct', 'Brooks-Medicine Hat'),
    'Medicine Hat-Cypress':                    ('direct', 'Cypress-Medicine Hat'),
    'Olds-Three Hills-Didsbury':               ('direct', 'Olds-Didsbury-Three Hills'),
    'Peace River':                             ('direct', 'Peace River'),
    'Rocky Mountain House-Banff Park':         ('direct', 'Rimbey-Rocky Mountain House-Sundre'),
    'Sherwood Park':                           ('direct', 'Sherwood Park'),
    'St. Albert':                              ('direct', 'St. Albert'),
    'Stony Plain-Drayton Valley':              ('direct', 'Drayton Valley-Devon'),
    'Sherwood Park-Strathcona':                ('direct', 'Strathcona-Sherwood Park'),
    'West Yellowhead':                         ('direct', 'West Yellowhead'),
    'Wetaskawin-Ponoka-Maskwacis':             ('direct', 'Maskwacis-Wetaskiwin'),

    # Rest-of-province hybrids
    'St. Albert-Sturgeon':                     ('blend', 'Morinville-St. Albert', URBAN_WEIGHT_DEFAULT),
    'Lethbridge-Fort MacLeod-Crowsnest Pass':  ('blend', 'Lethbridge-West', URBAN_WEIGHT_DEFAULT),
    'Lethbridge-Cardston':                     ('blend', 'Lethbridge-West', URBAN_WEIGHT_DEFAULT),
    'Lethbridge-Little Bow':                   ('blend', 'Lethbridge-East', URBAN_WEIGHT_DEFAULT),
    'Lethbridge-Taber-Warner':                 ('blend', 'Taber-Warner', URBAN_WEIGHT_DEFAULT),
    'Red Deer-Lacombe':                        ('blend', 'Lacombe-Ponoka', URBAN_WEIGHT_DEFAULT),
    'Red Deer-Innisfail':                      ('blend', 'Innisfail-Sylvan Lake', URBAN_WEIGHT_DEFAULT),
    'Red Deer-Blackfalds':                     ('merge', ['Red Deer-North', 'Lacombe-Ponoka'], [0.5, 0.2]),
    'Red Deer-Sylvan Lake':                    ('merge', ['Red Deer-South', 'Innisfail-Sylvan Lake'], [0.5, 0.3]),
}


def estimate_2026(dists_2019: List[Dict],
                  mapping: Dict[str, tuple],
                  rural_ndp_share: float,
                  urban_weight: float = URBAN_WEIGHT_DEFAULT) -> List[Dict]:
    """Apply a mapping dictionary to produce 2026 ED estimates.

    Same function used for majority and minority — methodology is symmetric.
    """
    by_name = {d['ed']: d for d in dists_2019}

    def blend(base: Dict, urban_w: float) -> Dict:
        utot = base['ndp'] + base['ucp']
        ushare = base['ndp'] / utot
        rural_w = 1 - urban_w
        blended_share = urban_w * ushare + rural_w * rural_ndp_share
        # Rural absorptions have slightly lower turnout → scale total.
        new_total = utot * (urban_w + rural_w * 0.7)
        # CRIT-03: replaced int() floor-truncation with round(). int()
        # truncates toward zero, systematically under-counting votes on
        # both parties by up to 1 vote per row (~30 rows × 2 parties),
        # which can flip close-margin seat calls. round() is unbiased.
        return {
            'ndp': round(new_total * blended_share),
            'ucp': round(new_total * (1 - blended_share)),
        }

    out = []
    # CRIT-05: track any mapping row that cannot be resolved. Previously
    # a missing 2019 parent was silently dropped, producing fewer than
    # 89 output rows. validate_2026_estimate() catches incomplete lists
    # inside main(), but v0_3_monte_carlo_ci.py calls estimate_2026 in a
    # tight loop without that gate. We now raise KeyError up front so
    # every caller sees the problem.
    missing: List[str] = []
    for new_ed, spec in mapping.items():
        kind = spec[0]
        if kind == 'direct':
            base = by_name.get(spec[1])
            if base:
                out.append({'ed': new_ed, 'ndp': base['ndp'], 'ucp': base['ucp']})
            else:
                missing.append(f"{new_ed} <- direct({spec[1]})")
        elif kind == 'blend':
            base = by_name.get(spec[1])
            if base:
                blended = blend(base, spec[2])
                out.append({'ed': new_ed, **blended})
            else:
                missing.append(f"{new_ed} <- blend({spec[1]})")
        elif kind == 'merge':
            parts = [by_name.get(name) for name in spec[1]]
            weights = spec[2]
            if all(parts):
                # CRIT-03: round() instead of int() for merge weights.
                ndp = sum(round(p['ndp']*w) for p, w in zip(parts, weights))
                ucp = sum(round(p['ucp']*w) for p, w in zip(parts, weights))
                out.append({'ed': new_ed, 'ndp': ndp, 'ucp': ucp})
            else:
                missing_parents = [n for n, p in zip(spec[1], parts) if p is None]
                missing.append(f"{new_ed} <- merge(missing: {missing_parents})")
        elif kind == 'split':
            base = by_name.get(spec[1])
            if base:
                urban_w = spec[2]
                fraction = spec[3]
                # CRIT-03: round() instead of int() when scaling a
                # fraction of a 2019 ED before blending.
                scaled = {'ndp': round(base['ndp']*fraction),
                          'ucp': round(base['ucp']*fraction)}
                blended = blend(scaled, urban_w)
                out.append({'ed': new_ed, **blended})
            else:
                missing.append(f"{new_ed} <- split({spec[1]})")
    if missing:
        # CRIT-05: surface missing parents instead of silently dropping
        # the row. Currently passes because the 2019 names are frozen;
        # a future data refresh will trip this assertion cleanly.
        raise KeyError(
            "estimate_2026: mapping rows could not be resolved: "
            + "; ".join(missing)
        )
    return out


# ---------------------------------------------------------------------
# Falsifiability gates
# ---------------------------------------------------------------------

def validate_2026_estimate(estimates: List[Dict], label: str,
                           expected_n: int = 89) -> Tuple[bool, str]:
    """Gate: refuse to proceed if estimate set is incomplete or sums implausibly."""
    n = len(estimates)
    total = sum(d['ndp']+d['ucp'] for d in estimates)
    total_ndp = sum(d['ndp'] for d in estimates)
    ok = True
    msgs = []
    if n != expected_n:
        msgs.append(f"FAIL: {label} has {n} EDs, expected {expected_n}")
        ok = False
    # Total 2023 two-party votes: 1,706,304. Estimated totals should be
    # within 5% after blending (blending introduces integer rounding +
    # rural-turnout downscaling).
    if not (1_600_000 <= total <= 1_800_000):
        msgs.append(f"FAIL: {label} total votes {total:,} outside plausible range")
        ok = False
    ndp_share = total_ndp/total if total else 0
    if not (0.40 <= ndp_share <= 0.50):
        msgs.append(f"FAIL: {label} NDP share {ndp_share:.3f} outside plausible range")
        ok = False
    return ok, "; ".join(msgs) if msgs else "PASS"


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    print("="*60)
    print("  Alberta Packing/Cracking Analysis v0.2")
    print("  Symmetric three-map test, 70/30 urban/rural blend")
    print("="*60)

    dists_2019 = load_2023_results()

    rural = [d for d in dists_2019 if d['region'] == 'Rest of Alberta']
    rural_ndp = sum(d['ndp'] for d in rural) / sum(d['ndp']+d['ucp'] for d in rural)
    print(f"\nRural Alberta baseline NDP two-party (2023 observed): {rural_ndp*100:.1f}%")

    # 2019 baseline (no estimation needed)
    m_2019 = compute_metrics(dists_2019,
                             "2019 BOUNDARIES (CURRENT) under 2023 vote shares")

    # Majority 2026 — SYMMETRIC estimation
    maj = estimate_2026(dists_2019, MAJORITY_2026_MAPPING, rural_ndp)
    ok, msg = validate_2026_estimate(maj, "Majority 2026")
    print(f"\n[GATE] Majority 2026 estimate validation: {msg}")
    if not ok:
        print("Aborting majority metrics — gate failed.")
        m_maj = None
    else:
        m_maj = compute_metrics(maj, "MAJORITY 2026 PROPOSAL (estimated, 70/30)")

    # Minority 2026
    minr = estimate_2026(dists_2019, MINORITY_2026_MAPPING, rural_ndp)
    ok, msg = validate_2026_estimate(minr, "Minority 2026")
    print(f"\n[GATE] Minority 2026 estimate validation: {msg}")
    if not ok:
        print("Aborting minority metrics — gate failed.")
        m_min = None
    else:
        m_min = compute_metrics(minr, "MINORITY 2026 PROPOSAL (estimated, 70/30)")

    # Three-way comparison
    if m_maj and m_min:
        print("\n" + "="*60)
        print("  THREE-MAP COMPARISON")
        print("="*60)
        print(f"  Metric              | 2019    | Majority | Minority")
        print(f"  Districts            | {m_2019['n']:>7d} | {m_maj['n']:>8d} | {m_min['n']:>8d}")
        print(f"  Actual seats NDP/UCP | {m_2019['ndp_seats']}/{m_2019['ucp_seats']}   | {m_maj['ndp_seats']}/{m_maj['ucp_seats']}    | {m_min['ndp_seats']}/{m_min['ucp_seats']}")
        print(f"  B2 Efficiency gap    | {m_2019['eg']*100:+6.2f}% | {m_maj['eg']*100:+7.2f}% | {m_min['eg']*100:+7.2f}%")
        print(f"  B3 Mean-median       | {m_2019['mm_gap']*100:+6.2f}pp| {m_maj['mm_gap']*100:+7.2f}pp| {m_min['mm_gap']*100:+7.2f}pp")
        print(f"  B4 NDP @ 50/50       | {m_2019['ndp_at_50']:>7d} | {m_maj['ndp_at_50']:>8d} | {m_min['ndp_at_50']:>8d}")
        print(f"  B6 Declination       | {m_2019['declination']:+7.4f} | {m_maj['declination']:+8.4f} | {m_min['declination']:+8.4f}")

        # Sensitivity test under alternative urban weights
        print("\n" + "="*60)
        print("  SENSITIVITY: B2 efficiency gap under alternative weights")
        print("="*60)
        print(f"  Urban weight | Majority EG | Minority EG | Delta")
        for w in [0.60, 0.70, 0.80, 0.85, 0.90]:
            # MED-07: removed dead `estimate_2026` calls that preceded
            # the override rebuild. The mapping tuples bake the weight
            # into spec[2], so the `urban_weight=w` kwarg had no effect
            # on blend rows. Only the override-mapping branch is live.
            override_maj = {k: (v[0], v[1], w) if v[0] == 'blend' else v
                            for k, v in MAJORITY_2026_MAPPING.items()}
            override_min = {k: (v[0], v[1], w) if v[0] == 'blend' else v
                            for k, v in MINORITY_2026_MAPPING.items()}
            maj_w = estimate_2026(dists_2019, override_maj, rural_ndp)
            min_w = estimate_2026(dists_2019, override_min, rural_ndp)
            mm_maj = compute_metrics(maj_w, f"Majority w={w}", verbose=False)
            mm_min = compute_metrics(min_w, f"Minority w={w}", verbose=False)
            print(f"  {w:.2f}         | {mm_maj['eg']*100:+7.2f}%    | {mm_min['eg']*100:+7.2f}%    | {(mm_min['eg']-mm_maj['eg'])*100:+5.2f}pp")

    # Gate check: the three-map comparison must have directional consistency
    # for the audit's findings to hold. If majority EG and minority EG are both
    # in the same direction as 2019 baseline with similar magnitudes, the claim
    # of a "minority shift" is falsified.
    if m_maj and m_min:
        print("\n" + "="*60)
        print("  FALSIFIABILITY GATE — directional claim check")
        print("="*60)
        delta_maj = m_maj['eg'] - m_2019['eg']
        delta_min = m_min['eg'] - m_2019['eg']
        print(f"  Delta from 2019 EG (majority): {delta_maj*100:+.2f} pp")
        print(f"  Delta from 2019 EG (minority): {delta_min*100:+.2f} pp")
        print(f"  Minority-Majority asymmetry:   {(delta_min-delta_maj)*100:+.2f} pp")
        if abs(delta_min - delta_maj) < 0.005:
            print("  VERDICT: maps within 0.5 pp of each other — NO asymmetry detected.")
        else:
            print(f"  VERDICT: minority shifts {(delta_min-delta_maj)*100:+.2f} pp relative to majority.")


if __name__ == '__main__':
    main()
