"""
v0_1_338canada_historical.py
Track AA: historical 338Canada Alberta projections — pipeline.

Pulls the full historical time-series embedded in 338Canada's Alberta landing
page (77 snapshots from 2020-02-23 to 2026-04-12), tests 338's pre-2023-election
accuracy against the actual 2023 Statement of Vote, and tests whether the
audit's 1-seat minority-vs-majority asymmetry is stable across a sample of
those historical snapshots.

Phases:
  1. Pull landing-page time-series (aggregate UCP / NDP / seat / majority
     probability at each of 77 dates).
  2. Identify the closest pre-2023-election snapshot (last snapshot dated on
     or before 2023-05-29) and compare its provincial projection to the
     2023 actual result.
  3. Per-riding scrape at three selected historical dates (pre-2023, late-2024,
     mid-2025) via the Wayback Machine if reachable; otherwise document the
     gap.
  4. Run each obtainable per-riding snapshot through the majority and
     minority hybrid crosswalks (reusing v0_1_338canada_reallocate.py) and
     record the seat-count asymmetry.

Outputs:
  data/v0_1_338canada_historical_snapshots.csv
  data/v0_1_338_historical/alberta_landing_raw.html   (cache)
  data/v0_1_338_historical/*.html                     (per-riding caches)

Usage:
  PYTHONIOENCODING=utf-8 python analysis/v0_1_338canada_historical.py
"""

from __future__ import annotations
import csv
import io
import json
import os
import re
import statistics
import sys
import time
import urllib.request
from typing import Dict, List, Tuple, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT_ROOT = os.path.dirname(HERE)
DATA = os.path.join(AUDIT_ROOT, 'data')
HIST_DIR = os.path.join(DATA, 'v0_1_338_historical')
os.makedirs(HIST_DIR, exist_ok=True)

UA = "Mozilla/5.0 (research; Alberta boundaries audit, v0_1)"
ALBERTA_URL = "https://338canada.com/alberta/"

# Key anchor dates for per-riding reconstruction via Wayback.
# Hand-picked to cover pre-2023, mid-cycle, and recent.
WAYBACK_TARGETS = [
    ("2023-05-28", "pre-2023-election (final pre-vote projection)"),
    ("2024-07-07", "mid-cycle 2024"),
    ("2025-09-28", "fall 2025"),
]


def fetch_cached(url: str, cache_path: str, force: bool = False) -> str:
    if (not force) and os.path.exists(cache_path):
        with open(cache_path, encoding='utf-8') as f:
            return f.read()
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"__FETCH_ERROR__ {type(e).__name__}: {e}"
    with open(cache_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html


# ---------------------------------------------------------------------
# Phase 1: extract 77-point aggregate series from current landing page
# ---------------------------------------------------------------------

def extract_landing_series(html: str) -> Dict:
    """Parse the 11 stacked blocks + x-axis dates. Return dict keyed by
    snapshot_date with aggregate values.
    """
    # X-axis: ISO dates array immediately before 'rangeOptions'
    m = re.search(
        r"(\[\s*(?:'\d{4}-\d{2}-\d{2}'\s*,?\s*){3,}\s*\])\s*,\s*\n?\s*rangeOptions",
        html,
        re.DOTALL,
    )
    if not m:
        raise RuntimeError("landing: x-axis array not found")
    xarr_raw = m.group(1)
    dates = re.findall(r"'(\d{4}-\d{2}-\d{2})'", xarr_raw)

    # Find all party blocks (key, label, values) in order. 11 expected.
    blocks = re.findall(
        r"key:\s*'([^']+)'[^}]*?label:\s*'([^']+)'[^}]*?values:\s*\[([\-\d\.,\s]+)\]",
        html,
        re.DOTALL,
    )
    parsed: List[Tuple[str, str, List[float]]] = []
    for key, label, vals in blocks:
        v = [float(x) for x in vals.split(',') if x.strip()]
        if len(v) != len(dates):
            # Skip blocks that don't match the x-axis length (e.g., smaller
            # per-party history that isn't the main time-series)
            continue
        parsed.append((key, label, v))

    # First 5 party blocks = vote share; next 2 = seat counts; next 4 =
    # majority / plurality probabilities.
    # Map by order (robust to re-matching duplicate keys):
    if len(parsed) < 7:
        raise RuntimeError(f"landing: expected >=7 full-length blocks, got {len(parsed)}")

    share_labels = ['UCP_share', 'NDP_share', 'PTPA_share', 'GPA_share', 'REP_share']
    seat_labels = ['UCP_seats', 'NDP_seats']
    prob_labels = ['UCPMAJ', 'UCPmin', 'NDPMAJ', 'NDPmin']

    series_by_label: Dict[str, List[float]] = {}
    idx = 0
    for lbl in share_labels:
        if idx >= len(parsed):
            break
        series_by_label[lbl] = parsed[idx][2]
        idx += 1
    for lbl in seat_labels:
        if idx >= len(parsed):
            break
        series_by_label[lbl] = parsed[idx][2]
        idx += 1
    for lbl in prob_labels:
        if idx >= len(parsed):
            break
        series_by_label[lbl] = parsed[idx][2]
        idx += 1

    out = {'dates': dates, 'series': series_by_label, 'n_snapshots': len(dates)}
    return out


def write_historical_aggregate_csv(landing: Dict, path: str) -> None:
    dates = landing['dates']
    s = landing['series']
    cols = ['snapshot_date', 'ucp_share', 'ndp_share', 'ptpa_share',
            'gpa_share', 'rep_share', 'ucp_seats', 'ndp_seats',
            'ucp_majority_prob', 'ucp_plurality_prob',
            'ndp_majority_prob', 'ndp_plurality_prob']
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for i, d in enumerate(dates):
            row = [d]
            for k in ('UCP_share', 'NDP_share', 'PTPA_share', 'GPA_share',
                      'REP_share', 'UCP_seats', 'NDP_seats',
                      'UCPMAJ', 'UCPmin', 'NDPMAJ', 'NDPmin'):
                if k in s:
                    row.append(round(s[k][i], 3))
                else:
                    row.append('')
            w.writerow(row)


# ---------------------------------------------------------------------
# Phase 2: pre-2023 aggregate validation against 2023 actuals
# ---------------------------------------------------------------------

def alberta_2023_actual_aggregate() -> Dict[str, float]:
    """Compute provincial UCP / NDP two-party vote share from the audit's
    2023 per-ED CSV.
    """
    path = os.path.join(DATA, 'v0_1_alberta_2023_results.csv')
    ucp = ndp = 0
    total = 0
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            u = float(r.get('ucp', 0) or 0)
            n = float(r.get('ndp', 0) or 0)
            ucp += u
            ndp += n
            total += u + n
    return {
        'ucp_actual_tp': 100.0 * ucp / (ucp + ndp),
        'ndp_actual_tp': 100.0 * ndp / (ucp + ndp),
        'ucp_votes': ucp, 'ndp_votes': ndp,
    }


def alberta_2023_actual_seats() -> Dict[str, int]:
    """Compute actual 2023 UCP/NDP seat counts from the per-ED CSV
    (winner determined by max(ucp, ndp) per ED).
    """
    path = os.path.join(DATA, 'v0_1_alberta_2023_results.csv')
    ucp = ndp = 0
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            u = float(r.get('ucp', 0) or 0)
            n = float(r.get('ndp', 0) or 0)
            if u > n:
                ucp += 1
            elif n > u:
                ndp += 1
    return {'ucp_seats': ucp, 'ndp_seats': ndp}


# ---------------------------------------------------------------------
# Phase 3: Wayback per-riding pull
# ---------------------------------------------------------------------

def wayback_closest(url: str, yyyymmdd: str) -> Optional[str]:
    """Query Wayback CDX API for the closest snapshot to the date, return
    full Wayback URL to the capture, or None.
    """
    api = (f"http://archive.org/wayback/available?url={urllib.request.quote(url)}"
           f"&timestamp={yyyymmdd}")
    req = urllib.request.Request(api, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"  wayback query failed for {url} {yyyymmdd}: {e}", file=sys.stderr)
        return None
    snap = data.get('archived_snapshots', {}).get('closest', {})
    if snap.get('available') and snap.get('url'):
        return snap['url']
    return None


def wayback_pull_aggregate(date_iso: str) -> Optional[Dict]:
    """Pull the Alberta landing page from Wayback for a given target date
    and extract aggregate projection at that snapshot.

    Returns dict with ucp_share, ndp_share, ucp_seats, ndp_seats, wayback_url,
    actual_snapshot_date (as encoded by Wayback timestamp).
    """
    yyyymmdd = date_iso.replace('-', '')
    # Prefer ~midday
    wb_url = wayback_closest(ALBERTA_URL, yyyymmdd + '120000')
    if not wb_url:
        return None
    # Parse the actual snapshot date out of the Wayback URL
    ts_m = re.search(r'/web/(\d{4})(\d{2})(\d{2})', wb_url)
    actual_date = None
    if ts_m:
        actual_date = f"{ts_m.group(1)}-{ts_m.group(2)}-{ts_m.group(3)}"
    # Cache
    safe = date_iso.replace('-', '')
    cache = os.path.join(HIST_DIR, f'alberta_wayback_{safe}.html')
    html = fetch_cached(wb_url, cache)
    if html.startswith('__FETCH_ERROR__'):
        return {'wayback_url': wb_url, 'actual_date': actual_date,
                'error': html}
    try:
        parsed = extract_landing_series(html)
    except Exception as e:
        return {'wayback_url': wb_url, 'actual_date': actual_date,
                'error': f'parse failed: {e}'}
    # Take the LAST point of each series (the snapshot that was current
    # at capture time)
    s = parsed['series']
    return {
        'target_date': date_iso,
        'wayback_url': wb_url,
        'actual_date': actual_date,
        'snapshot_date_in_page': parsed['dates'][-1] if parsed['dates'] else None,
        'ucp_share': round(s.get('UCP_share', [float('nan')])[-1], 3) if 'UCP_share' in s else None,
        'ndp_share': round(s.get('NDP_share', [float('nan')])[-1], 3) if 'NDP_share' in s else None,
        'ucp_seats': round(s.get('UCP_seats', [float('nan')])[-1], 1) if 'UCP_seats' in s else None,
        'ndp_seats': round(s.get('NDP_seats', [float('nan')])[-1], 1) if 'NDP_seats' in s else None,
        'ucp_maj_prob': round(s.get('UCPMAJ', [float('nan')])[-1], 2) if 'UCPMAJ' in s else None,
        'ndp_maj_prob': round(s.get('NDPMAJ', [float('nan')])[-1], 2) if 'NDPMAJ' in s else None,
    }


def wayback_pull_per_riding(date_iso: str, ridings_index: List[Dict],
                             max_ridings: int = 87) -> Optional[List[Dict]]:
    """Pull per-riding pages from Wayback for a target date. Returns a list
    of per-riding dicts with ucp_share and ndp_share, or None if unreachable.

    NOTE: Wayback coverage of /alberta/NNNNe.htm is spotty — many riding
    pages have never been archived on specific dates. We return whatever
    we can obtain and log a gap count.
    """
    yyyymmdd = date_iso.replace('-', '')
    rows: List[Dict] = []
    hit = miss = 0
    for i, r in enumerate(ridings_index[:max_ridings]):
        code = r['code']
        riding = r['riding']
        url = f"https://338canada.com/alberta/{code}e.htm"
        wb = wayback_closest(url, yyyymmdd + '120000')
        if not wb:
            rows.append({'district': riding, 'code': code,
                         'ucp_share': None, 'ndp_share': None,
                         'wayback_url': '', 'note': 'no wayback'})
            miss += 1
            continue
        cache = os.path.join(HIST_DIR, f'riding_{code}_{yyyymmdd}.html')
        html = fetch_cached(wb, cache)
        if html.startswith('__FETCH_ERROR__'):
            rows.append({'district': riding, 'code': code,
                         'ucp_share': None, 'ndp_share': None,
                         'wayback_url': wb, 'note': html[:80]})
            miss += 1
            continue
        # Reuse the scraper's logic: find UCP and NDP shares (last point)
        try:
            parties = _parse_riding_html(html)
            ucp_share = parties.get('UCP', {}).get('share')
            ndp_share = parties.get('NDP', {}).get('share')
            if ucp_share is None or ndp_share is None:
                rows.append({'district': riding, 'code': code,
                             'ucp_share': None, 'ndp_share': None,
                             'wayback_url': wb, 'note': 'parse missing UCP/NDP'})
                miss += 1
            else:
                rows.append({'district': riding, 'code': code,
                             'ucp_share': round(ucp_share, 3),
                             'ndp_share': round(ndp_share, 3),
                             'wayback_url': wb, 'note': ''})
                hit += 1
        except Exception as e:
            rows.append({'district': riding, 'code': code,
                         'ucp_share': None, 'ndp_share': None,
                         'wayback_url': wb, 'note': f'parse error: {e}'})
            miss += 1
        # Wayback rate-limiting is generous but still polite to pause.
        time.sleep(0.1)
        if (i + 1) % 15 == 0:
            print(f"  wayback {date_iso}: {i+1}/{len(ridings_index[:max_ridings])} "
                  f"(hit={hit}, miss={miss})", file=sys.stderr)
    return rows


def _parse_riding_html(html: str) -> Dict[str, Dict[str, float]]:
    """Mirror of v0_1_338canada_scraper.parse_page, simplified for this
    historical-only pipeline.
    """
    PARTY_WITH_MOE_RE = re.compile(
        r"key:\s*'([^']+)',[^}]*?values:\s*\[\s*([\-\d\.\s,]+)\],\s*moe:\s*\[\s*([\-\d\.\s,]+)\]",
        re.DOTALL,
    )
    out: Dict[str, Dict[str, float]] = {}
    for key, vals, _moes in PARTY_WITH_MOE_RE.findall(html):
        v = [float(x) for x in vals.split(',') if x.strip()]
        if v and key not in out:
            out[key] = {'share': v[-1]}
    return out


# ---------------------------------------------------------------------
# Phase 4: reallocate historical per-riding shares through audit crosswalks
# ---------------------------------------------------------------------

def load_audit_machinery():
    """Import the audit's mapping dicts and population loader. Defer the
    import here to keep this module independently runnable even when the
    audit's Phase-3 dependencies are absent.
    """
    sys.path.insert(0, os.path.join(AUDIT_ROOT, 'analysis'))
    from v0_2_packing_cracking_analysis import (  # type: ignore
        MAJORITY_2026_MAPPING, MINORITY_2026_MAPPING, load_2023_results,
    )
    return MAJORITY_2026_MAPPING, MINORITY_2026_MAPPING, load_2023_results


def reallocate_snapshot(t338: Dict[str, Dict], mapping: Dict,
                         pop: Dict[str, int],
                         rural_ucp: float, rural_ndp: float) -> List[Dict]:
    """Same reallocation logic as v0_1_338canada_reallocate.reallocate_338_v2
    but local (avoids circular dependency).
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
            if s and s.get('ucp_share') is not None:
                ucp, ndp = s['ucp_share'], s['ndp_share']
            else:
                note = f'missing source {sources}'
        elif kind == 'blend':
            sources = spec[1]
            s = t338.get(sources)
            urban_w = spec[2]
            if s and s.get('ucp_share') is not None:
                rural_w = 1 - urban_w
                ucp = urban_w * s['ucp_share'] + rural_w * rural_ucp
                ndp = urban_w * s['ndp_share'] + rural_w * rural_ndp
            else:
                note = f'missing source {sources}'
        elif kind == 'merge':
            eds, weights = spec[1], spec[2]
            sources = '|'.join(eds)
            shares = []
            ws = []
            miss = []
            for ed, w in zip(eds, weights):
                s = t338.get(ed)
                if not s or s.get('ucp_share') is None:
                    miss.append(ed)
                    continue
                shares.append(s)
                ws.append(pop.get(ed, 50000) * w)
            if not miss and shares:
                wsum = sum(ws)
                ucp = sum(s['ucp_share'] * w for s, w in zip(shares, ws)) / wsum
                ndp = sum(s['ndp_share'] * w for s, w in zip(shares, ws)) / wsum
            else:
                note = f'missing: {miss}'
        elif kind == 'split':
            sources = spec[1]
            s = t338.get(sources)
            urban_w = spec[2]
            if s and s.get('ucp_share') is not None:
                rural_w = 1 - urban_w
                ucp = urban_w * s['ucp_share'] + rural_w * rural_ucp
                ndp = urban_w * s['ndp_share'] + rural_w * rural_ndp
            else:
                note = f'missing source {sources}'
        winner = ''
        if ucp is not None and ndp is not None:
            winner = 'UCP' if ucp > ndp else ('NDP' if ndp > ucp else 'TIE')
        out.append({'ed': new_ed, 'kind': kind, 'sources': sources,
                    'ucp': round(ucp, 3) if ucp is not None else '',
                    'ndp': round(ndp, 3) if ndp is not None else '',
                    'winner': winner, 'note': note})
    return out


# ---------------------------------------------------------------------
# Phase 2b: pre-2023 PER-RIDING validation (only if wayback succeeds
# for 2023-05-28 target)
# ---------------------------------------------------------------------

def load_2023_actual_per_riding() -> Dict[str, Dict]:
    path = os.path.join(DATA, 'v0_1_alberta_2023_results.csv')
    out = {}
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            u = float(r.get('ucp', 0) or 0)
            n = float(r.get('ndp', 0) or 0)
            if u + n == 0:
                continue
            out[r['ed']] = {
                'ucp': u, 'ndp': n,
                'ucp_pct_tp': 100.0 * u / (u + n),
                'ndp_pct_tp': 100.0 * n / (u + n),
                'region': r.get('region', ''),
            }
    return out


def per_riding_validation(pre23_rows: List[Dict], actuals: Dict[str, Dict]) -> Dict:
    """Compare pre-election 338 per-riding (two-party) projection vs 2023
    actual two-party vote.
    """
    pairs = []
    for r in pre23_rows:
        d = r.get('district')
        if d not in actuals:
            continue
        if r.get('ucp_share') is None or r.get('ndp_share') is None:
            continue
        u338 = r['ucp_share']
        n338 = r['ndp_share']
        if u338 + n338 <= 0:
            continue
        u_tp_338 = 100.0 * u338 / (u338 + n338)
        u_actual = actuals[d]['ucp_pct_tp']
        pairs.append({'ed': d, 'region': actuals[d]['region'],
                      'ucp_338_tp': u_tp_338,
                      'ucp_actual_tp': u_actual,
                      'error': u_tp_338 - u_actual})
    if not pairs:
        return {'n': 0}
    a = [p['ucp_actual_tp'] for p in pairs]
    b = [p['ucp_338_tp'] for p in pairs]
    n = len(a)
    ma, mb = statistics.mean(a), statistics.mean(b)
    num = sum((a[i]-ma)*(b[i]-mb) for i in range(n))
    den = (sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b)) ** 0.5
    r = num / den if den else float('nan')
    mae = sum(abs(p['error']) for p in pairs) / n
    bias = sum(p['error'] for p in pairs) / n
    # Regional breakdown
    by_region: Dict[str, List[float]] = {}
    for p in pairs:
        by_region.setdefault(p['region'], []).append(p['error'])
    regional = {r: {'n': len(v),
                    'mae': sum(abs(x) for x in v) / len(v),
                    'bias': sum(v) / len(v)}
                for r, v in by_region.items()}
    pairs.sort(key=lambda p: abs(p['error']), reverse=True)
    return {
        'n': n, 'pearson_r': r, 'mae': mae, 'bias_338_minus_actual': bias,
        'regional': regional,
        'top_errors': pairs[:15],
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    print("=== TRACK AA — 338Canada Historical Pipeline ===\n")

    # ---- Phase 1: landing-page time-series ----
    print("Phase 1: pulling Alberta landing page and extracting 77-point time-series.")
    landing_cache = os.path.join(HIST_DIR, 'alberta_landing_raw.html')
    html = fetch_cached(ALBERTA_URL, landing_cache)
    if html.startswith('__FETCH_ERROR__'):
        print(f"  FAIL: {html}")
        return
    try:
        landing = extract_landing_series(html)
    except Exception as e:
        print(f"  parse FAIL: {e}")
        return
    print(f"  snapshots in series: {landing['n_snapshots']}")
    print(f"  series: {list(landing['series'].keys())}")
    print(f"  date range: {landing['dates'][0]} to {landing['dates'][-1]}")
    out_csv = os.path.join(DATA, 'v0_1_338canada_historical_snapshots.csv')
    write_historical_aggregate_csv(landing, out_csv)
    print(f"  wrote {out_csv}")

    # ---- Phase 2a: aggregate pre-2023 validation ----
    print("\nPhase 2a: aggregate pre-2023 validation.")
    dates = landing['dates']
    s = landing['series']
    # Last snapshot on or before 2023-05-29 (election day)
    pre_idx = None
    for i, d in enumerate(dates):
        if d <= '2023-05-29':
            pre_idx = i
    if pre_idx is None:
        print("  no pre-election snapshot found in landing series.")
    else:
        pre_date = dates[pre_idx]
        ucp_pre = s['UCP_share'][pre_idx]
        ndp_pre = s['NDP_share'][pre_idx]
        ucp_seats_pre = s.get('UCP_seats', [None]*len(dates))[pre_idx]
        ndp_seats_pre = s.get('NDP_seats', [None]*len(dates))[pre_idx]
        actual = alberta_2023_actual_aggregate()
        seats_actual = alberta_2023_actual_seats()
        # Convert 338's all-party share to two-party
        u_tp_338 = 100.0 * ucp_pre / (ucp_pre + ndp_pre)
        n_tp_338 = 100.0 * ndp_pre / (ucp_pre + ndp_pre)
        print(f"  pre-election snapshot: {pre_date}")
        print(f"  338 vote share (all-party):  UCP {ucp_pre:.2f}%  NDP {ndp_pre:.2f}%")
        print(f"  338 vote share (two-party):  UCP {u_tp_338:.2f}%  NDP {n_tp_338:.2f}%")
        print(f"  2023 actual (two-party):     UCP {actual['ucp_actual_tp']:.2f}%  "
              f"NDP {actual['ndp_actual_tp']:.2f}%")
        print(f"  error (338 - actual):        UCP {u_tp_338 - actual['ucp_actual_tp']:+.2f} pp  "
              f"NDP {n_tp_338 - actual['ndp_actual_tp']:+.2f} pp")
        if ucp_seats_pre is not None:
            print(f"  338 seat projection:         UCP {ucp_seats_pre:.1f}  NDP {ndp_seats_pre:.1f}")
            print(f"  2023 actual seats:           UCP {seats_actual['ucp_seats']}  "
                  f"NDP {seats_actual['ndp_seats']}")

    # ---- Phase 2b: wayback aggregate time-series check ----
    print("\nPhase 2b: Wayback aggregate pulls at chosen anchor dates.")
    wb_agg_rows = []
    for date_iso, desc in WAYBACK_TARGETS:
        print(f"  wayback: {date_iso} ({desc})")
        r = wayback_pull_aggregate(date_iso)
        if not r:
            print(f"    unreachable / no capture")
            wb_agg_rows.append({'target_date': date_iso, 'desc': desc,
                                 'status': 'no capture'})
            continue
        if 'error' in r:
            print(f"    error: {r['error'][:120]}")
            wb_agg_rows.append({'target_date': date_iso, 'desc': desc,
                                 'status': r['error'][:120]})
            continue
        row = {'target_date': date_iso, 'desc': desc,
               'actual_date': r.get('actual_date'),
               'snapshot_in_page': r.get('snapshot_date_in_page'),
               'ucp_share': r.get('ucp_share'),
               'ndp_share': r.get('ndp_share'),
               'ucp_seats': r.get('ucp_seats'),
               'ndp_seats': r.get('ndp_seats'),
               'ucp_maj_prob': r.get('ucp_maj_prob'),
               'ndp_maj_prob': r.get('ndp_maj_prob'),
               'status': 'ok'}
        wb_agg_rows.append(row)
        print(f"    actual_capture={row['actual_date']}  "
              f"page_last={row['snapshot_in_page']}")
        print(f"    UCP share={row['ucp_share']}  NDP share={row['ndp_share']}  "
              f"UCP seats={row['ucp_seats']}  NDP seats={row['ndp_seats']}")

    with open(os.path.join(HIST_DIR, 'wayback_aggregate_pulls.json'),
              'w', encoding='utf-8') as f:
        json.dump(wb_agg_rows, f, indent=2)

    # ---- Phase 3: per-riding pulls at same anchors ----
    print("\nPhase 3: per-riding Wayback pulls (this is the expensive step).")
    ridings_index_path = os.path.join(DATA, 'v0_1_338canada_ridings_index.csv')
    if not os.path.exists(ridings_index_path):
        print(f"  no ridings index at {ridings_index_path}; skipping per-riding phase.")
        return
    with open(ridings_index_path, encoding='utf-8') as f:
        ridings_index = list(csv.DictReader(f))
    print(f"  riding count: {len(ridings_index)}")

    # To stay in time/token budget, we sample 20 ridings per target date.
    SAMPLE_N = 20
    # Stratified sample: 7 Edmonton + 7 Calgary + 6 rest
    edm = [r for r in ridings_index if r.get('region') == 'Edmonton'][:7]
    cal = [r for r in ridings_index if r.get('region') == 'Calgary'][:7]
    rest = [r for r in ridings_index
            if r.get('region') not in ('Edmonton', 'Calgary')][:6]
    sample = edm + cal + rest
    print(f"  stratified sample size: {len(sample)} "
          f"(Edmonton {len(edm)}, Calgary {len(cal)}, rest {len(rest)})")

    per_riding_results: Dict[str, List[Dict]] = {}
    for date_iso, desc in WAYBACK_TARGETS:
        print(f"\n  --- {date_iso} ({desc}) ---")
        rows = wayback_pull_per_riding(date_iso, sample, max_ridings=len(sample))
        per_riding_results[date_iso] = rows or []
        hit = sum(1 for r in rows if r.get('ucp_share') is not None) if rows else 0
        miss = sum(1 for r in rows if r.get('ucp_share') is None) if rows else 0
        print(f"    per-riding hit={hit} miss={miss}")

    # Save the raw per-riding table
    with open(os.path.join(HIST_DIR, 'per_riding_wayback.json'), 'w',
              encoding='utf-8') as f:
        json.dump(per_riding_results, f, indent=2)

    # ---- Phase 2b (per-riding accuracy) for pre-2023 sample ----
    pre_sample = per_riding_results.get('2023-05-28', [])
    pre_hits = [r for r in pre_sample if r.get('ucp_share') is not None]
    if pre_hits:
        print(f"\nPhase 2b per-riding: {len(pre_hits)} pre-2023 ridings with data.")
        actuals = load_2023_actual_per_riding()
        v = per_riding_validation(pre_hits, actuals)
        if v.get('n', 0) > 0:
            print(f"  n paired:      {v['n']}")
            print(f"  Pearson r:     {v['pearson_r']:.4f}")
            print(f"  MAE:           {v['mae']:.2f} pp")
            print(f"  mean bias:     {v['bias_338_minus_actual']:+.2f} pp (338 - actual)")
            for reg, vs in v['regional'].items():
                print(f"  region={reg}: n={vs['n']} mae={vs['mae']:.2f} "
                      f"bias={vs['bias']:+.2f}")
            print(f"  top-5 errors:")
            for p in v['top_errors'][:5]:
                print(f"    {p['ed']:45s} 338={p['ucp_338_tp']:6.2f}  "
                      f"actual={p['ucp_actual_tp']:6.2f}  err={p['error']:+6.2f}")
            with open(os.path.join(HIST_DIR, 'pre2023_per_riding_validation.json'),
                      'w', encoding='utf-8') as f:
                json.dump(v, f, indent=2)
    else:
        print("\nPhase 2b per-riding: no pre-2023 riding pages obtained from Wayback.")

    # ---- Phase 4: reallocate each obtained per-riding snapshot ----
    # Only ridings sampled are reallocatable; for fair comparison we note
    # that this is a SAMPLED stability test, not a full 87-riding re-run.
    print("\nPhase 4: reallocate each per-riding snapshot through the audit's "
          "majority and minority crosswalks — sampled-subset stability check.")
    try:
        MAJ, MIN, load_2023 = load_audit_machinery()
    except Exception as e:
        print(f"  could not import audit mapping: {e}")
        return

    # Population loader (for merge rule)
    pops = {}
    with open(os.path.join(DATA, 'v0_1_alberta_2019_populations.csv'),
              encoding='utf-8') as f:
        for r in csv.DictReader(f):
            pops[r['ed_name']] = int(r['population_2017_report'])

    # For the CURRENT (2026-04-12) snapshot we already have the full 87-riding
    # data in data/v0_1_338canada_per_riding_87seat.csv. Reallocate that for
    # baseline comparison.
    current_t338: Dict[str, Dict] = {}
    with open(os.path.join(DATA, 'v0_1_338canada_per_riding_87seat.csv'),
              encoding='utf-8') as f:
        for r in csv.DictReader(f):
            current_t338[r['district']] = {
                'ucp_share': float(r['ucp_share']),
                'ndp_share': float(r['ndp_share']),
            }
    dists_2019 = load_2023()
    rural_names = {d['ed'] for d in dists_2019 if d['region'] == 'Rest of Alberta'}
    rural_ucp_cur = statistics.mean(current_t338[n]['ucp_share']
                                     for n in rural_names if n in current_t338)
    rural_ndp_cur = statistics.mean(current_t338[n]['ndp_share']
                                     for n in rural_names if n in current_t338)
    print(f"\n  current (2026-04-12) rural baseline: "
          f"UCP {rural_ucp_cur:.2f}% NDP {rural_ndp_cur:.2f}%")
    maj_cur = reallocate_snapshot(current_t338, MAJ, pops,
                                   rural_ucp_cur, rural_ndp_cur)
    min_cur = reallocate_snapshot(current_t338, MIN, pops,
                                   rural_ucp_cur, rural_ndp_cur)
    ucp_maj_cur = sum(1 for r in maj_cur if r['winner'] == 'UCP')
    ndp_maj_cur = sum(1 for r in maj_cur if r['winner'] == 'NDP')
    ucp_min_cur = sum(1 for r in min_cur if r['winner'] == 'UCP')
    ndp_min_cur = sum(1 for r in min_cur if r['winner'] == 'NDP')
    print(f"  current: majority UCP/NDP = {ucp_maj_cur}/{ndp_maj_cur}; "
          f"minority = {ucp_min_cur}/{ndp_min_cur}")
    print(f"  current min-vs-maj asymmetry: "
          f"UCP {ucp_min_cur - ucp_maj_cur:+d}, NDP {ndp_min_cur - ndp_maj_cur:+d}")

    # For historical snapshots, we have only a 20-riding sample. We cannot
    # produce a defensible full-87 reallocation from 20 ridings. Document
    # the gap instead.
    stability_table = [{'snapshot_date': '2026-04-12 (current, full 87)',
                        'maj_ucp': ucp_maj_cur, 'maj_ndp': ndp_maj_cur,
                        'min_ucp': ucp_min_cur, 'min_ndp': ndp_min_cur,
                        'min_minus_maj_ucp': ucp_min_cur - ucp_maj_cur,
                        'min_minus_maj_ndp': ndp_min_cur - ndp_maj_cur,
                        'n_ridings_observed': len(current_t338),
                        'source': 'current scrape'}]

    for date_iso, desc in WAYBACK_TARGETS:
        rows = per_riding_results.get(date_iso, [])
        hits = [r for r in rows if r.get('ucp_share') is not None]
        n_obs = len(hits)
        if n_obs < len(sample) * 0.8:
            # Not enough coverage to reallocate defensibly.
            stability_table.append({
                'snapshot_date': f'{date_iso} (sample, {n_obs}/{len(sample)})',
                'maj_ucp': '', 'maj_ndp': '', 'min_ucp': '', 'min_ndp': '',
                'min_minus_maj_ucp': '', 'min_minus_maj_ndp': '',
                'n_ridings_observed': n_obs,
                'source': f'wayback {date_iso}, insufficient coverage'})
            continue
        # Build a t338 dict from hits for the sampled EDs and use the CURRENT
        # snapshot's rural baseline as a fallback for unsampled EDs, because
        # the audit's crosswalk expects all 87 2019 EDs as sources. This is
        # an approximation — we flag it in the report.
        partial = dict(current_t338)  # start from current snapshot
        for h in hits:
            partial[h['district']] = {'ucp_share': h['ucp_share'],
                                       'ndp_share': h['ndp_share']}
        # Rural baseline for rest-of-Alberta from partial
        rural_ucp_h = statistics.mean(partial[n]['ucp_share']
                                       for n in rural_names if n in partial)
        rural_ndp_h = statistics.mean(partial[n]['ndp_share']
                                       for n in rural_names if n in partial)
        maj_h = reallocate_snapshot(partial, MAJ, pops, rural_ucp_h, rural_ndp_h)
        min_h = reallocate_snapshot(partial, MIN, pops, rural_ucp_h, rural_ndp_h)
        ucp_maj_h = sum(1 for r in maj_h if r['winner'] == 'UCP')
        ndp_maj_h = sum(1 for r in maj_h if r['winner'] == 'NDP')
        ucp_min_h = sum(1 for r in min_h if r['winner'] == 'UCP')
        ndp_min_h = sum(1 for r in min_h if r['winner'] == 'NDP')
        stability_table.append({
            'snapshot_date': f'{date_iso} (hybrid: {n_obs} sampled + '
                             f'{len(current_t338) - n_obs} current)',
            'maj_ucp': ucp_maj_h, 'maj_ndp': ndp_maj_h,
            'min_ucp': ucp_min_h, 'min_ndp': ndp_min_h,
            'min_minus_maj_ucp': ucp_min_h - ucp_maj_h,
            'min_minus_maj_ndp': ndp_min_h - ndp_maj_h,
            'n_ridings_observed': n_obs,
            'source': f'wayback {date_iso} (partial; unsampled EDs filled '
                      f'from current 2026-04-12 snapshot)'})
        print(f"\n  {date_iso}: maj {ucp_maj_h}/{ndp_maj_h}, "
              f"min {ucp_min_h}/{ndp_min_h}, "
              f"asymmetry UCP {ucp_min_h - ucp_maj_h:+d} NDP {ndp_min_h - ndp_maj_h:+d}")

    # Write stability table
    stab_path = os.path.join(HIST_DIR, 'stability_table.csv')
    cols = list(stability_table[0].keys())
    with open(stab_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(stability_table)
    print(f"\n  wrote stability table: {stab_path}")

    # ---- Dump the landing-page-derived time-series stability probe ----
    # We can ALSO run a simpler, lighter stability check purely on 338's
    # provincial UCP/NDP SHARE over time (no per-riding needed). For each
    # of 77 snapshots, apply a uniform swing to the current per-riding
    # snapshot and re-call each seat. This tests: does the 1-seat asymmetry
    # survive under different province-wide vote levels?
    print("\nPhase 4b: Uniform-swing stability probe — 77 snapshots, uniform "
          "swing applied to the current per-riding base.")
    dates = landing['dates']
    s = landing['series']
    # Current provincial 338 baseline (two-party %)
    cur_ucp_all = statistics.mean(current_t338[d]['ucp_share'] for d in current_t338)
    cur_ndp_all = statistics.mean(current_t338[d]['ndp_share'] for d in current_t338)
    cur_ucp_tp = 100.0 * cur_ucp_all / (cur_ucp_all + cur_ndp_all)
    # For each snapshot, compute province-wide two-party UCP shift vs current.
    sweep_rows = []
    for i, d in enumerate(dates):
        u = s['UCP_share'][i]; n = s['NDP_share'][i]
        if u + n == 0:
            continue
        snap_ucp_tp = 100.0 * u / (u + n)
        delta_ucp = snap_ucp_tp - cur_ucp_tp  # pp
        # Uniform swing on each current per-riding pair (two-party view):
        # new_ucp_tp = current_ucp_tp + delta_ucp, clipped to [0,100]
        sim_t338 = {}
        for ed, row in current_t338.items():
            cu = row['ucp_share']; cn = row['ndp_share']
            if cu + cn <= 0:
                continue
            cur_tp = 100.0 * cu / (cu + cn)
            new_tp = max(0.0, min(100.0, cur_tp + delta_ucp))
            scale_tp = (cu + cn) / 100.0  # preserve all-party sum
            sim_t338[ed] = {
                'ucp_share': scale_tp * new_tp,
                'ndp_share': scale_tp * (100.0 - new_tp),
            }
        rural_u = statistics.mean(sim_t338[n]['ucp_share']
                                   for n in rural_names if n in sim_t338)
        rural_n = statistics.mean(sim_t338[n]['ndp_share']
                                   for n in rural_names if n in sim_t338)
        maj_r = reallocate_snapshot(sim_t338, MAJ, pops, rural_u, rural_n)
        min_r = reallocate_snapshot(sim_t338, MIN, pops, rural_u, rural_n)
        umc = sum(1 for r in maj_r if r['winner'] == 'UCP')
        nmc = sum(1 for r in maj_r if r['winner'] == 'NDP')
        unc = sum(1 for r in min_r if r['winner'] == 'UCP')
        nnc = sum(1 for r in min_r if r['winner'] == 'NDP')
        sweep_rows.append({
            'snapshot_date': d,
            'ucp_share_all_party': round(u, 3),
            'ndp_share_all_party': round(n, 3),
            'ucp_share_two_party': round(snap_ucp_tp, 3),
            'ucp_swing_vs_current_pp': round(delta_ucp, 3),
            'maj_ucp_seats': umc, 'maj_ndp_seats': nmc,
            'min_ucp_seats': unc, 'min_ndp_seats': nnc,
            'min_minus_maj_ucp': unc - umc,
            'min_minus_maj_ndp': nnc - nmc,
        })

    sweep_csv = os.path.join(HIST_DIR, 'uniform_swing_stability.csv')
    with open(sweep_csv, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(sweep_rows[0].keys()))
        w.writeheader()
        w.writerows(sweep_rows)
    print(f"  wrote {sweep_csv}  ({len(sweep_rows)} snapshots simulated)")

    # Summarize sweep asymmetry
    asym_ucp = [r['min_minus_maj_ucp'] for r in sweep_rows]
    asym_counts = {}
    for a in asym_ucp:
        asym_counts[a] = asym_counts.get(a, 0) + 1
    print(f"\n  UCP asymmetry distribution across 77 synthetic snapshots "
          f"(min_UCP − maj_UCP):")
    for a in sorted(asym_counts):
        print(f"    {a:+d} UCP : {asym_counts[a]} snapshots")

    # Record the asymmetry as a function of UCP two-party share
    print(f"\n  UCP asymmetry by UCP two-party share band:")
    bands = [(0, 45), (45, 50), (50, 55), (55, 60), (60, 70), (70, 100)]
    for lo, hi in bands:
        rows = [r for r in sweep_rows
                if lo <= r['ucp_share_two_party'] < hi]
        if not rows:
            continue
        asym_here = [r['min_minus_maj_ucp'] for r in rows]
        print(f"    UCP tp {lo:>3}–{hi:<3}%: n={len(rows)}  "
              f"UCP asym mean={statistics.mean(asym_here):+.2f} "
              f"min={min(asym_here):+d} max={max(asym_here):+d}")

    print("\nDone.")


if __name__ == '__main__':
    main()
