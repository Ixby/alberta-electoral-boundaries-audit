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
# Pre-2023 has full 87-riding coverage in Mar-May 2023; other windows
# have sparse coverage and are handled via the landing-page aggregate sweep.
WAYBACK_TARGETS = [
    ("2023-05-29", "pre-2023-election (final capture before election day)"),
]
# Window for the CDX search (used to find the last pre-election capture
# for each riding). UTC dates, inclusive.
PRE23_WINDOW = ("20230301", "20230529")  # March 1 to election day


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
    """Compute provincial UCP / NDP two-party vote share via the audit's
    load_2023_results loader (handles cand_N/votes_N pair parsing).
    """
    sys.path.insert(0, os.path.join(AUDIT_ROOT, 'analysis'))
    from v0_2_packing_cracking_analysis import load_2023_results  # type: ignore
    dists = load_2023_results()
    ucp = sum(d['ucp'] for d in dists)
    ndp = sum(d['ndp'] for d in dists)
    return {
        'ucp_actual_tp': 100.0 * ucp / (ucp + ndp),
        'ndp_actual_tp': 100.0 * ndp / (ucp + ndp),
        'ucp_votes': ucp, 'ndp_votes': ndp,
    }


def alberta_2023_actual_seats() -> Dict[str, int]:
    """Compute actual 2023 UCP/NDP seat counts using the audit's loader."""
    sys.path.insert(0, os.path.join(AUDIT_ROOT, 'analysis'))
    from v0_2_packing_cracking_analysis import load_2023_results  # type: ignore
    dists = load_2023_results()
    ucp = sum(1 for d in dists if d['ucp'] > d['ndp'])
    ndp = sum(1 for d in dists if d['ndp'] > d['ucp'])
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


def wayback_cdx_last_before(url: str, yyyymmdd_from: str,
                             yyyymmdd_to: str) -> Optional[str]:
    """Use the CDX search API to find the LAST capture of `url` in the
    window [yyyymmdd_from, yyyymmdd_to] with status 200. Returns the
    full Wayback URL to the capture, or None.
    """
    api = (f"http://web.archive.org/cdx/search/cdx?"
           f"url={urllib.request.quote(url)}"
           f"&output=json&from={yyyymmdd_from}&to={yyyymmdd_to}"
           f"&filter=statuscode:200&fl=timestamp,original"
           f"&limit=200")
    req = urllib.request.Request(api, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            arr = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"  cdx query failed for {url}: {e}", file=sys.stderr)
        return None
    if len(arr) <= 1:
        return None
    # Last row = latest timestamp in window
    ts, orig = arr[-1][0], arr[-1][1]
    return f"https://web.archive.org/web/{ts}/{orig}"


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


def wayback_pull_per_riding_window(ridings_index: List[Dict],
                                     window_from: str, window_to: str,
                                     max_ridings: int = 87) -> List[Dict]:
    """Pull per-riding pages from Wayback, choosing the LAST capture in the
    given window for each riding. Returns a list of per-riding dicts.

    If the HTML cache for a riding already exists (keyed by `w{window_to}`),
    skip the CDX query and parse the cached file directly.
    """
    rows: List[Dict] = []
    hit = miss = 0
    for i, r in enumerate(ridings_index[:max_ridings]):
        code = r['code']
        riding = r['riding']
        url = f"https://338canada.com/alberta/{code}e.htm"
        cache = os.path.join(HIST_DIR, f'riding_{code}_w{window_to}.html')
        if os.path.exists(cache) and os.path.getsize(cache) > 1000:
            # Cache hit — skip CDX, parse directly.
            with open(cache, encoding='utf-8') as f:
                html = f.read()
            snap_date = _extract_projection_date(html)
            try:
                parties = _parse_riding_html(html)
                ucp_share = parties.get('UCP', {}).get('share')
                ndp_share = parties.get('NDP', {}).get('share')
                if ucp_share is None or ndp_share is None:
                    rows.append({'district': riding, 'code': code,
                                 'ucp_share': None, 'ndp_share': None,
                                 'snap_date': snap_date,
                                 'wayback_url': '(cached)', 'wayback_ts': '',
                                 'note': 'parse missing UCP/NDP (cache)'})
                    miss += 1
                else:
                    rows.append({'district': riding, 'code': code,
                                 'ucp_share': round(ucp_share, 3),
                                 'ndp_share': round(ndp_share, 3),
                                 'snap_date': snap_date,
                                 'wayback_url': '(cached)', 'wayback_ts': '',
                                 'note': '(from cache)'})
                    hit += 1
            except Exception as e:
                rows.append({'district': riding, 'code': code,
                             'ucp_share': None, 'ndp_share': None,
                             'snap_date': snap_date,
                             'wayback_url': '(cached)', 'wayback_ts': '',
                             'note': f'parse error (cache): {e}'})
                miss += 1
            if (i + 1) % 15 == 0:
                print(f"  wayback (cache) {i+1}/{len(ridings_index[:max_ridings])} "
                      f"(hit={hit}, miss={miss})", file=sys.stderr)
            continue
        wb = wayback_cdx_last_before(url, window_from, window_to)
        if not wb:
            rows.append({'district': riding, 'code': code,
                         'ucp_share': None, 'ndp_share': None,
                         'snap_date': '',
                         'wayback_url': '', 'wayback_ts': '',
                         'note': 'no capture in window'})
            miss += 1
            continue
        # Parse the wayback timestamp out of the URL
        ts_m = re.search(r'/web/(\d{14})/', wb)
        ts = ts_m.group(1) if ts_m else ''
        html = fetch_cached(wb, cache)
        if html.startswith('__FETCH_ERROR__'):
            rows.append({'district': riding, 'code': code,
                         'ucp_share': None, 'ndp_share': None,
                         'snap_date': '',
                         'wayback_url': wb, 'wayback_ts': ts,
                         'note': html[:80]})
            miss += 1
            continue
        snap_date = _extract_projection_date(html)
        try:
            parties = _parse_riding_html(html)
            ucp_share = parties.get('UCP', {}).get('share')
            ndp_share = parties.get('NDP', {}).get('share')
            if ucp_share is None or ndp_share is None:
                rows.append({'district': riding, 'code': code,
                             'ucp_share': None, 'ndp_share': None,
                             'snap_date': snap_date,
                             'wayback_url': wb, 'wayback_ts': ts,
                             'note': 'parse missing UCP/NDP'})
                miss += 1
            else:
                rows.append({'district': riding, 'code': code,
                             'ucp_share': round(ucp_share, 3),
                             'ndp_share': round(ndp_share, 3),
                             'snap_date': snap_date,
                             'wayback_url': wb, 'wayback_ts': ts,
                             'note': ''})
                hit += 1
        except Exception as e:
            rows.append({'district': riding, 'code': code,
                         'ucp_share': None, 'ndp_share': None,
                         'snap_date': snap_date,
                         'wayback_url': wb, 'wayback_ts': ts,
                         'note': f'parse error: {e}'})
            miss += 1
        time.sleep(0.1)
        if (i + 1) % 15 == 0:
            print(f"  wayback window {window_from}-{window_to}: "
                  f"{i+1}/{len(ridings_index[:max_ridings])} "
                  f"(hit={hit}, miss={miss})", file=sys.stderr)
    return rows


MONTHS = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
          'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
          'November': 11, 'December': 12}


def _extract_projection_date(html: str) -> str:
    """Return ISO date of the projection printed on the archived page
    (e.g. 'Latest projection: March 11, 2023'), or empty string.
    """
    m = re.search(r'Latest projection:\s+([A-Za-z]+)\s+(\d+),?\s+(\d{4})', html)
    if not m:
        m = re.search(r'338Canada Popular vote projection\s*\|\s*([A-Za-z]+)\s+(\d+),?\s+(\d{4})',
                      html)
    if m:
        mon, day, year = m.group(1), int(m.group(2)), int(m.group(3))
        mm = MONTHS.get(mon)
        if mm:
            return f"{year:04d}-{mm:02d}-{day:02d}"
    return ''


def _parse_riding_html(html: str) -> Dict[str, Dict[str, float]]:
    """Extract UCP and NDP projected vote shares from a 338Canada riding
    page.

    Supports two page formats:

      (A) Current (2025+) pages: JavaScript data blocks of the form
          `key: 'UCP', ..., values: [...time series], moe: [...]`.
          The last array entry is the current projection.

      (B) Legacy (pre-2025) pages and Wayback archives thereof: the
          projection is rendered as an inline SVG with text elements
          like `<text ... fill="#366092">44% ± 8%</text>` for UCP and
          `<text ... fill="#E17C0D">47% ± 8%</text>` for NDP.
          (#366092 = UCP blue, #E17C0D = NDP orange per 338's palette.)
    """
    out: Dict[str, Dict[str, float]] = {}

    # Format A
    PARTY_WITH_MOE_RE = re.compile(
        r"key:\s*'([^']+)',[^}]*?values:\s*\[\s*([\-\d\.\s,]+)\],\s*moe:\s*\[\s*([\-\d\.\s,]+)\]",
        re.DOTALL,
    )
    for key, vals, _moes in PARTY_WITH_MOE_RE.findall(html):
        v = [float(x) for x in vals.split(',') if x.strip()]
        if v and key not in out:
            out[key] = {'share': v[-1]}
    if out:
        return out

    # Format B — parse the ridingvote SVG. The `ridingvote-N` suffix varies
    # (N=0 for some pages, 1 for others, depending on page template).
    m = re.search(r'<svg id="ridingvote-\d+"[^>]*>(.*?)</svg>', html, re.DOTALL)
    if not m:
        return out
    svg = m.group(1)
    # Extract text entries: fill + text
    entries = re.findall(r'<text[^>]*fill="(#[0-9A-Fa-f]{6})"[^>]*>([^<]+)</text>',
                         svg)
    # Party color map (338's canonical palette)
    COLOR_TO_PARTY = {
        '#366092': 'UCP',
        '#E17C0D': 'NDP',
        '#12bbff': 'ABP',   # Alberta Party
        '#84BD00': 'WIP',   # WildIndependence
        '#3D9B35': 'GPA',   # Green
        '#D71920': 'LIB',
        '#A9A9A9': 'OTH',
    }
    # Find "N% ± M%" entries and associate with preceding-or-same-color label
    # We walk entries: the pattern per party is [percent-text, label-text]
    # in order. E.g. (#E17C0D, '47% ± 8%'), (#E17C0D, 'NDP').
    pct_re = re.compile(r'(\d+(?:\.\d+)?)\s*%\s*(?:±|\+/-)?\s*(\d+(?:\.\d+)?)?')
    for color, text in entries:
        color_l = color.lower()
        # Match against the map with case-insensitive comparison
        party = None
        for k, v in COLOR_TO_PARTY.items():
            if k.lower() == color_l:
                party = v
                break
        if not party:
            continue
        if '%' not in text:
            continue
        pm = pct_re.search(text)
        if not pm:
            continue
        try:
            share = float(pm.group(1))
        except ValueError:
            continue
        # Only record the first share per party (the N% entry, not e.g. 'UCP 2019')
        # '2019' or year-like labels should be skipped — check if nearby
        # label text contains a year.
        if party in out:
            continue
        # Skip 'UCP 2019' type entries — these come with labels starting with party name
        # (already labels, no %). We're filtering via '%' check above.
        out[party] = {'share': share}
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
    sys.path.insert(0, os.path.join(AUDIT_ROOT, 'analysis'))
    from v0_2_packing_cracking_analysis import load_2023_results  # type: ignore
    out = {}
    for d in load_2023_results():
        u = d['ucp']; n = d['ndp']
        if u + n == 0:
            continue
        out[d['ed']] = {
            'ucp': u, 'ndp': n,
            'ucp_pct_tp': 100.0 * u / (u + n),
            'ndp_pct_tp': 100.0 * n / (u + n),
            'region': d.get('region', ''),
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

    # Note: Phase 2b wayback aggregate pulls are not required — the current
    # landing page already embeds the full 77-snapshot time-series from
    # 2020-02-23 onward, so we already have aggregate UCP/NDP/seat values
    # at every historical date without needing a separate wayback query.
    # Wayback is only used below for per-riding reconstruction, where the
    # time-series is not embedded in the current site.

    # ---- Phase 3: per-riding pulls for pre-2023 window (full 87) ----
    print("\nPhase 3: pre-2023 per-riding Wayback pulls (window = last capture "
          f"per riding in {PRE23_WINDOW[0]}-{PRE23_WINDOW[1]}).")
    ridings_index_path = os.path.join(DATA, 'v0_1_338canada_ridings_index.csv')
    if not os.path.exists(ridings_index_path):
        print(f"  no ridings index at {ridings_index_path}; skipping per-riding phase.")
        return
    with open(ridings_index_path, encoding='utf-8') as f:
        ridings_index = list(csv.DictReader(f))
    print(f"  riding count: {len(ridings_index)}")

    per_riding_results: Dict[str, List[Dict]] = {}
    pre23_rows = wayback_pull_per_riding_window(
        ridings_index, PRE23_WINDOW[0], PRE23_WINDOW[1], max_ridings=87)
    per_riding_results['2023-05-29_pre_election'] = pre23_rows
    pre_hit = sum(1 for r in pre23_rows if r.get('ucp_share') is not None)
    pre_miss = sum(1 for r in pre23_rows if r.get('ucp_share') is None)
    print(f"  pre-2023 per-riding: hit={pre_hit} miss={pre_miss} of {len(pre23_rows)}")

    # Save the raw per-riding table
    with open(os.path.join(HIST_DIR, 'per_riding_wayback.json'), 'w',
              encoding='utf-8') as f:
        json.dump(per_riding_results, f, indent=2)
    # Also CSV for easier inspection
    csv_path = os.path.join(HIST_DIR, 'per_riding_pre2023.csv')
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(pre23_rows[0].keys()))
        w.writeheader()
        w.writerows(pre23_rows)
    print(f"  wrote {csv_path}")

    # ---- Phase 2b (per-riding accuracy) for pre-2023 ----
    pre_hits_local = [r for r in pre23_rows if r.get('ucp_share') is not None]
    pre_hits = pre_hits_local
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

    # Pre-2023 full-87 reallocation
    pre23_rows = per_riding_results.get('2023-05-29_pre_election', [])
    pre23_hits = [r for r in pre23_rows if r.get('ucp_share') is not None]
    n_obs = len(pre23_hits)
    if n_obs >= 80:
        pre23_t338 = {h['district']: {'ucp_share': h['ucp_share'],
                                       'ndp_share': h['ndp_share']}
                       for h in pre23_hits}
        # Any ridings missing from pre23? Fall back to current to avoid
        # dropping an ED in the crosswalk (flagged in MD).
        missing_in_pre23 = [d for d in current_t338 if d not in pre23_t338]
        for d in missing_in_pre23:
            pre23_t338[d] = current_t338[d]
        rural_ucp_pre = statistics.mean(pre23_t338[n]['ucp_share']
                                         for n in rural_names if n in pre23_t338)
        rural_ndp_pre = statistics.mean(pre23_t338[n]['ndp_share']
                                         for n in rural_names if n in pre23_t338)
        maj_pre = reallocate_snapshot(pre23_t338, MAJ, pops,
                                       rural_ucp_pre, rural_ndp_pre)
        min_pre = reallocate_snapshot(pre23_t338, MIN, pops,
                                       rural_ucp_pre, rural_ndp_pre)
        ucp_maj_pre = sum(1 for r in maj_pre if r['winner'] == 'UCP')
        ndp_maj_pre = sum(1 for r in maj_pre if r['winner'] == 'NDP')
        ucp_min_pre = sum(1 for r in min_pre if r['winner'] == 'UCP')
        ndp_min_pre = sum(1 for r in min_pre if r['winner'] == 'NDP')
        stability_table.append({
            'snapshot_date': f'pre-2023-election (338 last capture per riding '
                             f'in {PRE23_WINDOW[0]}-{PRE23_WINDOW[1]})',
            'maj_ucp': ucp_maj_pre, 'maj_ndp': ndp_maj_pre,
            'min_ucp': ucp_min_pre, 'min_ndp': ndp_min_pre,
            'min_minus_maj_ucp': ucp_min_pre - ucp_maj_pre,
            'min_minus_maj_ndp': ndp_min_pre - ndp_maj_pre,
            'n_ridings_observed': n_obs,
            'source': f'wayback full 87 pre-2023 (missing filled '
                      f'{len(missing_in_pre23)} from current)'})
        print(f"\n  pre-2023 full 87: maj {ucp_maj_pre}/{ndp_maj_pre}, "
              f"min {ucp_min_pre}/{ndp_min_pre}, "
              f"asymmetry UCP {ucp_min_pre - ucp_maj_pre:+d} "
              f"NDP {ndp_min_pre - ndp_maj_pre:+d}")
        # Also record the per-ED pre-2023 reallocation for reporting
        pre_maj_csv = os.path.join(HIST_DIR, 'pre2023_reallocated_majority.csv')
        pre_min_csv = os.path.join(HIST_DIR, 'pre2023_reallocated_minority.csv')
        for path, rows in [(pre_maj_csv, maj_pre), (pre_min_csv, min_pre)]:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
        print(f"  wrote {pre_maj_csv}")
        print(f"  wrote {pre_min_csv}")
    else:
        print(f"\n  pre-2023 per-riding coverage insufficient ({n_obs}/87); "
              f"skipping defensible pre-2023 full reallocation.")
        stability_table.append({
            'snapshot_date': 'pre-2023-election',
            'maj_ucp': '', 'maj_ndp': '', 'min_ucp': '', 'min_ndp': '',
            'min_minus_maj_ucp': '', 'min_minus_maj_ndp': '',
            'n_ridings_observed': n_obs,
            'source': 'wayback coverage insufficient'})

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
