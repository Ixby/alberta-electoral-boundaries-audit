"""
v0_1_338canada_reallocate.py
Track J, Phases 2-3.

Phase 2: cross-validate 338Canada per-riding central projections against the
audit's 2019-map projection (which is simply the 2023 two-party UCP share per
2019 ED, since the audit uses 2023 vote data as the base).

Phase 3: reallocate 338 shares through the hybrid crosswalks (majority and
minority) to produce per-2026-ED projected seat winners. The reallocation
mirrors the audit's methodology by mapping 2026 EDs to their 2019 source
ED(s) using the same MAJORITY_2026_MAPPING / MINORITY_2026_MAPPING dicts
in analysis/v0_2_packing_cracking_analysis.py.

Dependencies:
  data/v0_1_338canada_per_riding_87seat.csv  (from v0_1_338canada_scraper.py)
  data/v0_1_alberta_2023_results.csv         (audit's 2023 baseline)
  data/v0_1_alberta_2019_populations.csv     (weights for merges)
  analysis/v0_2_packing_cracking_analysis.py (mapping dicts + loader)

Outputs:
  data/v0_1_338canada_reallocated_majority.csv
  data/v0_1_338canada_reallocated_minority.csv
  (Phase 2 comparison and summary counts print to stdout and are captured
   in v0_1_338canada_riding_level.md.)
"""

from __future__ import annotations
import csv
import os
import sys
import statistics
from typing import Dict, List, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT_ROOT = os.path.dirname(HERE)
DATA = os.path.join(AUDIT_ROOT, 'data')
ANALYSIS = os.path.join(AUDIT_ROOT, 'analysis')

sys.path.insert(0, ANALYSIS)
from v0_2_packing_cracking_analysis import (  # noqa: E402
    MAJORITY_2026_MAPPING, MINORITY_2026_MAPPING, URBAN_WEIGHT_DEFAULT,
    load_2023_results,
)


def load_338() -> Dict[str, Dict]:
    """Return {district: {ucp_share, ndp_share, ucp_win, ndp_win, lead}}."""
    out = {}
    with open(os.path.join(DATA, 'v0_1_338canada_per_riding_87seat.csv'),
              encoding='utf-8') as f:
        for r in csv.DictReader(f):
            out[r['district']] = {
                'ucp_share': float(r['ucp_share']),
                'ndp_share': float(r['ndp_share']),
                'ucp_win': float(r['ucp_win_prob']) if r['ucp_win_prob'] else float('nan'),
                'ndp_win': float(r['ndp_win_prob']) if r['ndp_win_prob'] else float('nan'),
                'lead': r['leading_party'],
            }
    return out


def load_2019_populations() -> Dict[str, int]:
    out = {}
    with open(os.path.join(DATA, 'v0_1_alberta_2019_populations.csv'),
              encoding='utf-8') as f:
        for r in csv.DictReader(f):
            out[r['ed_name']] = int(r['population_2017_report'])
    return out


# ---------------------------------------------------------------------
# Phase 2: compare 338 central UCP share to audit's 2023 UCP two-party share
# ---------------------------------------------------------------------

def audit_two_party_ucp(dists_2019: List[Dict]) -> Dict[str, float]:
    """Audit's implicit 2019-map projection: per-ED UCP two-party share in %."""
    out = {}
    for d in dists_2019:
        tt = d['ndp'] + d['ucp']
        if tt == 0:
            continue
        out[d['ed']] = 100.0 * d['ucp'] / tt
    return out


def phase2_compare(t338: Dict, audit_ucp: Dict) -> Tuple[List[Dict], Dict]:
    """Return (per-row list, summary dict)."""
    # 338 share is UCP-of-all-parties; audit is UCP-of-two-party. Normalize
    # 338 to UCP-of-two-party to compare like with like.
    rows = []
    for district, sh in t338.items():
        if district not in audit_ucp:
            rows.append({'district': district, 'audit_ucp_pct': None,
                         'ucp_338_raw': sh['ucp_share'],
                         'ucp_338_two_party': None,
                         'delta': None, 'note': 'no audit match'})
            continue
        tp_ucp_338 = 100.0 * sh['ucp_share'] / (sh['ucp_share'] + sh['ndp_share'])
        audit_pct = audit_ucp[district]
        rows.append({
            'district': district,
            'audit_ucp_pct': round(audit_pct, 2),
            'ucp_338_raw': sh['ucp_share'],
            'ucp_338_two_party': round(tp_ucp_338, 2),
            'delta': round(tp_ucp_338 - audit_pct, 2),
            'note': '',
        })
    paired = [r for r in rows if r['audit_ucp_pct'] is not None]
    a = [r['audit_ucp_pct'] for r in paired]
    b = [r['ucp_338_two_party'] for r in paired]
    n = len(a)
    ma, mb = statistics.mean(a), statistics.mean(b)
    # Pearson r
    num = sum((a[i]-ma)*(b[i]-mb) for i in range(n))
    den = (sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b)) ** 0.5
    r = num / den if den else float('nan')
    mae = sum(abs(a[i]-b[i]) for i in range(n)) / n
    bias = sum(b[i]-a[i] for i in range(n)) / n  # 338 - audit
    summary = {'n': n, 'pearson_r': r, 'mae': mae, 'mean_bias_338_minus_audit': bias,
               'mean_audit': ma, 'mean_338_tp': mb}
    return rows, summary


# ---------------------------------------------------------------------
# Phase 3: reallocate 338 shares to 2026 EDs through the audit's mapping
# ---------------------------------------------------------------------

def reallocate_338(t338: Dict, mapping: Dict, pop: Dict[str, int],
                   rural_ucp_share: float) -> List[Dict]:
    """For each 2026 ED in the mapping, reallocate 338's central UCP / NDP
    shares through the audit's crosswalk.

    Mapping spec mirrors v0_2_packing_cracking_analysis:
      ('direct', ed2019)            -> copy 338's UCP/NDP from ed2019
      ('blend', ed2019, urban_w)    -> urban_w * 338(ed2019) + (1-urban_w) * rural baseline
      ('merge', [eds], [weights])   -> population-weighted mean of 338(eds) using 2019 pops * given weights
      ('split', ed2019, urban_w, f) -> treat as single-source, apply blend (f drops out
                                       in share space since we're not tracking vote totals).
    """
    out = []
    for new_ed, spec in mapping.items():
        kind = spec[0]
        if kind == 'direct':
            src = spec[1]
            s = t338.get(src)
            if not s:
                out.append({'ed': new_ed, 'ucp': None, 'ndp': None,
                            'kind': 'direct', 'sources': src,
                            'note': f'338 missing source {src}'})
                continue
            out.append({'ed': new_ed, 'ucp': s['ucp_share'], 'ndp': s['ndp_share'],
                        'kind': 'direct', 'sources': src, 'note': ''})
        elif kind == 'blend':
            src, urban_w = spec[1], spec[2]
            s = t338.get(src)
            if not s:
                out.append({'ed': new_ed, 'ucp': None, 'ndp': None,
                            'kind': 'blend', 'sources': src,
                            'note': f'338 missing source {src}'})
                continue
            rural_w = 1 - urban_w
            ucp = urban_w * s['ucp_share'] + rural_w * rural_ucp_share
            # Keep NDP proportional inside the two-party space
            urban_ndp = s['ndp_share']
            urban_tp_ucp = s['ucp_share'] / (s['ucp_share'] + s['ndp_share']) if (s['ucp_share']+s['ndp_share'])>0 else 0.5
            # Rural: use 338 rural average for NDP too (computed in main from rest-of-AB)
            # Actually, we pass rural_ucp_share only; reconstruct rural_ndp = 100 - rural_ucp - rural_other
            # Simpler: treat rural baseline as two-party, so NDP_rural = (1 - urban_tp_ucp_rural) * 100 *
            # normalization -> but we don't have rural NDP explicitly. We rely on caller to pass a
            # matched rural_ndp_share.
            # Use 1:1 map: rural_ndp from caller. We extend the signature via closure below.
            raise RuntimeError("blend path requires rural_ndp_share; see main()")
        elif kind == 'merge':
            eds, weights = spec[1], spec[2]
            shares = []
            ws = []
            missing = []
            for ed, w in zip(eds, weights):
                s = t338.get(ed)
                if not s:
                    missing.append(ed)
                    continue
                pop_w = pop.get(ed, 50000) * w  # pop * given weight
                shares.append(s)
                ws.append(pop_w)
            if missing or not shares:
                out.append({'ed': new_ed, 'ucp': None, 'ndp': None,
                            'kind': 'merge', 'sources': '|'.join(eds),
                            'note': f'338 missing source(s): {missing}'})
                continue
            wsum = sum(ws)
            ucp = sum(s['ucp_share'] * w for s, w in zip(shares, ws)) / wsum
            ndp = sum(s['ndp_share'] * w for s, w in zip(shares, ws)) / wsum
            out.append({'ed': new_ed, 'ucp': ucp, 'ndp': ndp,
                        'kind': 'merge', 'sources': '|'.join(eds), 'note': ''})
        elif kind == 'split':
            src = spec[1]
            s = t338.get(src)
            if not s:
                out.append({'ed': new_ed, 'ucp': None, 'ndp': None,
                            'kind': 'split', 'sources': src,
                            'note': f'338 missing source {src}'})
                continue
            # In share space, the split fraction doesn't change the share —
            # we're projecting a fraction of the electorate with the same
            # share. Skip the blend step here (treat urban_w=1.0 — split
            # takes half the urban core; reallocation in the audit blends
            # with rural baseline, but that is a modeling choice tied to
            # vote-total projection. For share-level reallocation we flag
            # this and copy the source share with an uncertainty note.)
            out.append({'ed': new_ed, 'ucp': s['ucp_share'], 'ndp': s['ndp_share'],
                        'kind': 'split', 'sources': src,
                        'note': 'split treated as share-copy; caveat in MD'})
    return out


def reallocate_338_v2(t338: Dict, mapping: Dict, pop: Dict[str, int],
                      rural_ucp: float, rural_ndp: float) -> List[Dict]:
    """Second-pass reallocator that handles 'blend' with an explicit
    rural_ndp share so both UCP and NDP stay consistent.
    """
    out = []
    for new_ed, spec in mapping.items():
        kind = spec[0]
        sources = ''
        note = ''
        ucp = ndp = None
        if kind == 'direct':
            sources = spec[1]
            s = t338.get(sources)
            if s:
                ucp, ndp = s['ucp_share'], s['ndp_share']
            else:
                note = f'338 missing source {sources}'
        elif kind == 'blend':
            sources = spec[1]
            s = t338.get(sources)
            urban_w = spec[2]
            if s:
                rural_w = 1 - urban_w
                ucp = urban_w * s['ucp_share'] + rural_w * rural_ucp
                ndp = urban_w * s['ndp_share'] + rural_w * rural_ndp
            else:
                note = f'338 missing source {sources}'
        elif kind == 'merge':
            eds, weights = spec[1], spec[2]
            sources = '|'.join(eds)
            shares = []
            ws = []
            miss = []
            for ed, w in zip(eds, weights):
                s = t338.get(ed)
                if not s:
                    miss.append(ed)
                    continue
                shares.append(s)
                ws.append(pop.get(ed, 50000) * w)
            if not miss and shares:
                wsum = sum(ws)
                ucp = sum(s['ucp_share'] * w for s, w in zip(shares, ws)) / wsum
                ndp = sum(s['ndp_share'] * w for s, w in zip(shares, ws)) / wsum
            else:
                note = f'338 missing source(s): {miss}'
        elif kind == 'split':
            sources = spec[1]
            s = t338.get(sources)
            urban_w = spec[2]
            if s:
                rural_w = 1 - urban_w
                ucp = urban_w * s['ucp_share'] + rural_w * rural_ucp
                ndp = urban_w * s['ndp_share'] + rural_w * rural_ndp
                note = 'split: share-level blend; excludes fractional turnout'
            else:
                note = f'338 missing source {sources}'
        row = {'ed': new_ed, 'kind': kind, 'sources': sources, 'note': note,
               'ucp_share': round(ucp, 3) if ucp is not None else '',
               'ndp_share': round(ndp, 3) if ndp is not None else '',
               'winner': '', 'margin': ''}
        if ucp is not None and ndp is not None:
            if ucp > ndp:
                row['winner'] = 'UCP'
                row['margin'] = round(ucp - ndp, 2)
            else:
                row['winner'] = 'NDP'
                row['margin'] = round(ndp - ucp, 2)
        out.append(row)
    return out


def write_csv(path: str, rows: List[Dict]) -> None:
    cols = ['ed', 'kind', 'sources', 'ucp_share', 'ndp_share',
            'winner', 'margin', 'note']
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main():
    t338 = load_338()
    pop = load_2019_populations()

    dists_2019 = load_2023_results()
    audit_ucp = audit_two_party_ucp(dists_2019)

    # Rural baseline for 338 shares: mean over rest-of-AB 2019 EDs.
    rural_names = {d['ed'] for d in dists_2019 if d['region'] == 'Rest of Alberta'}
    rural_338 = [t338[n] for n in rural_names if n in t338]
    rural_ucp = statistics.mean(r['ucp_share'] for r in rural_338)
    rural_ndp = statistics.mean(r['ndp_share'] for r in rural_338)
    print(f"338 rural-Alberta baseline: UCP {rural_ucp:.2f}%, NDP {rural_ndp:.2f}% "
          f"(n={len(rural_338)} EDs)")

    # -----------------------------------------------------------------
    # PHASE 2
    # -----------------------------------------------------------------
    rows, summary = phase2_compare(t338, audit_ucp)
    print("\n=== PHASE 2: 338 (two-party UCP %) vs audit (2023 two-party UCP %) ===")
    print(f"  n paired EDs:          {summary['n']}")
    print(f"  Pearson r:             {summary['pearson_r']:.4f}")
    print(f"  Mean absolute error:   {summary['mae']:.2f} pp")
    print(f"  Mean bias (338-audit): {summary['mean_bias_338_minus_audit']:+.2f} pp")
    print(f"  Mean audit UCP:        {summary['mean_audit']:.2f}%")
    print(f"  Mean 338 (2-party):    {summary['mean_338_tp']:.2f}%")

    # Top-10 biggest disagreements
    paired = [r for r in rows if r['delta'] is not None]
    paired.sort(key=lambda r: abs(r['delta']), reverse=True)
    print("\n  Top-10 largest |delta| (338 two-party UCP% minus audit 2023 UCP%):")
    for r in paired[:10]:
        print(f"    {r['district']:45s} audit={r['audit_ucp_pct']:6.2f}  "
              f"338_tp={r['ucp_338_two_party']:6.2f}  delta={r['delta']:+6.2f}")

    # -----------------------------------------------------------------
    # PHASE 3
    # -----------------------------------------------------------------
    print("\n=== PHASE 3: reallocate 338 shares through hybrid crosswalks ===")

    maj_rows = reallocate_338_v2(t338, MAJORITY_2026_MAPPING, pop,
                                 rural_ucp, rural_ndp)
    min_rows = reallocate_338_v2(t338, MINORITY_2026_MAPPING, pop,
                                 rural_ucp, rural_ndp)

    write_csv(os.path.join(DATA, 'v0_1_338canada_reallocated_majority.csv'),
              maj_rows)
    write_csv(os.path.join(DATA, 'v0_1_338canada_reallocated_minority.csv'),
              min_rows)

    for label, rs in (('MAJORITY', maj_rows), ('MINORITY', min_rows)):
        ucp_seats = sum(1 for r in rs if r['winner'] == 'UCP')
        ndp_seats = sum(1 for r in rs if r['winner'] == 'NDP')
        blank = sum(1 for r in rs if not r['winner'])
        print(f"\n  {label} proposal ({len(rs)} EDs total):")
        print(f"    UCP wins: {ucp_seats}")
        print(f"    NDP wins: {ndp_seats}")
        print(f"    No-data rows: {blank}")

    # -----------------------------------------------------------------
    # Compare to audit B1 central (hard-coded from audit output):
    # v0_2_packing_cracking_analysis.py produces:
    #   Majority 2026: UCP 38, NDP 51
    #   Minority 2026: UCP 37, NDP 52
    # -----------------------------------------------------------------
    audit_maj = {'UCP': 38, 'NDP': 51}
    audit_min = {'UCP': 37, 'NDP': 52}
    print("\n=== DELTA vs audit B1 central (338-reallocated minus audit 2023 projection) ===")
    ucp_338_maj = sum(1 for r in maj_rows if r['winner'] == 'UCP')
    ndp_338_maj = sum(1 for r in maj_rows if r['winner'] == 'NDP')
    ucp_338_min = sum(1 for r in min_rows if r['winner'] == 'UCP')
    ndp_338_min = sum(1 for r in min_rows if r['winner'] == 'NDP')
    print(f"  Majority: 338 UCP {ucp_338_maj} vs audit {audit_maj['UCP']} "
          f"(delta {ucp_338_maj - audit_maj['UCP']:+d}), "
          f"NDP {ndp_338_maj} vs audit {audit_maj['NDP']} "
          f"(delta {ndp_338_maj - audit_maj['NDP']:+d})")
    print(f"  Minority: 338 UCP {ucp_338_min} vs audit {audit_min['UCP']} "
          f"(delta {ucp_338_min - audit_min['UCP']:+d}), "
          f"NDP {ndp_338_min} vs audit {audit_min['NDP']} "
          f"(delta {ndp_338_min - audit_min['NDP']:+d})")

    # Largest per-riding margins in 338 reallocation -> most "safe" seats
    # And flag close races.
    print("\n  Majority 2026: 5 smallest margins (most likely to flip under uncertainty):")
    sorted_maj = sorted([r for r in maj_rows if r['margin'] != ''],
                        key=lambda r: r['margin'])
    for r in sorted_maj[:5]:
        print(f"    {r['ed']:45s} winner={r['winner']} margin={r['margin']:5.2f} "
              f"(UCP {r['ucp_share']:.1f} / NDP {r['ndp_share']:.1f})")

    print("\n  Minority 2026: 5 smallest margins:")
    sorted_min = sorted([r for r in min_rows if r['margin'] != ''],
                        key=lambda r: r['margin'])
    for r in sorted_min[:5]:
        print(f"    {r['ed']:45s} winner={r['winner']} margin={r['margin']:5.2f} "
              f"(UCP {r['ucp_share']:.1f} / NDP {r['ndp_share']:.1f})")


if __name__ == '__main__':
    main()
