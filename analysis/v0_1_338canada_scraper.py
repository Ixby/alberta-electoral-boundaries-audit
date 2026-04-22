"""
v0_1_338canada_scraper.py
Pulls 338Canada per-riding projections for all 87 Alberta ridings.

Track J, Phase 1. Reads data/v0_1_338canada_ridings_index.csv (code,riding,region),
fetches https://338canada.com/alberta/<code>e.htm for each, parses the embedded
JavaScript data block, and writes data/v0_1_338canada_per_riding_87seat.csv.

Per-page structure (as of scrape):
  Two sibling JS arrays, each with per-party entries:
    - Block 1: {key, label, color, values:[time-series of vote-share %], moe:[MoE %]}
    - Block 2: {key, label, color, values:[time-series of riding win probability %]}
  Last entry of each `values` array is the April 12, 2026 projection.

Output columns:
  district, ucp_share, ucp_moe, ucp_low, ucp_high,
  ndp_share, ndp_moe, ndp_low, ndp_high,
  other_share, leading_party, win_prob_leader,
  ucp_win_prob, ndp_win_prob, snapshot_date, source_url
"""

from __future__ import annotations
import csv
import os
import re
import sys
import time
import urllib.request
from typing import Dict, List, Tuple, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT_ROOT = os.path.dirname(HERE)
INDEX_CSV = os.path.join(AUDIT_ROOT, 'data', 'v0_1_338canada_ridings_index.csv')
OUT_CSV = os.path.join(AUDIT_ROOT, 'data', 'v0_1_338canada_per_riding_87seat.csv')

URL_TMPL = "https://338canada.com/alberta/{code}e.htm"
UA = "Mozilla/5.0 (research; Alberta boundaries audit, v0_1)"
SNAPSHOT_DATE = "2026-04-12"


def fetch(code: str) -> str:
    req = urllib.request.Request(URL_TMPL.format(code=code),
                                 headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', errors='replace')


PARTY_BLOCK_RE = re.compile(
    r"key:\s*'([^']+)',[^}]*?values:\s*\[\s*([\-\d\.\s,]+)\]",
    re.DOTALL,
)
PARTY_WITH_MOE_RE = re.compile(
    r"key:\s*'([^']+)',[^}]*?values:\s*\[\s*([\-\d\.\s,]+)\],\s*moe:\s*\[\s*([\-\d\.\s,]+)\]",
    re.DOTALL,
)


def parse_series(s: str) -> List[float]:
    return [float(x) for x in s.strip().rstrip(',').split(',') if x.strip()]


def parse_page(html: str) -> Dict[str, Dict[str, float]]:
    """Return {party_key: {'share': float, 'moe': float, 'win_prob': float}}.

    Walks the two stacked data blocks:
      - First set of party entries carries values+moe -> vote share + MoE.
      - Second set of party entries carries values only -> win probability.
    """
    # All (key, values, moe) matches -> vote share blocks.
    share_blocks = PARTY_WITH_MOE_RE.findall(html)
    # All (key, values) matches -> union of both blocks; we'll split by order.
    all_value_blocks = PARTY_BLOCK_RE.findall(html)

    parties: Dict[str, Dict[str, float]] = {}
    for key, vals, moes in share_blocks:
        v = parse_series(vals)
        m = parse_series(moes)
        parties[key] = {
            'share': v[-1] if v else float('nan'),
            'moe': m[-1] if m else float('nan'),
            'win_prob': float('nan'),
        }

    # Win-probability blocks = those value blocks that do NOT have a matching moe.
    # Easiest: iterate all_value_blocks, skip any block whose (key,values) matches
    # a share block; the remainder are win-prob blocks.
    share_signature = {(k, v.strip()) for k, v, _ in share_blocks}
    for key, vals in all_value_blocks:
        if (key, vals.strip()) in share_signature:
            continue
        v = parse_series(vals)
        if key in parties:
            parties[key]['win_prob'] = v[-1] if v else float('nan')
        else:
            # Unexpected party appeared only in win-prob block; record it.
            parties[key] = {
                'share': float('nan'),
                'moe': float('nan'),
                'win_prob': v[-1] if v else float('nan'),
            }
    return parties


def leading(parties: Dict[str, Dict[str, float]]) -> Tuple[str, float]:
    best_key, best_share = '', -1.0
    for k, v in parties.items():
        s = v.get('share', float('nan'))
        if s == s and s > best_share:
            best_share, best_key = s, k
    return best_key, best_share


def main():
    rows_out: List[Dict] = []
    with open(INDEX_CSV, encoding='utf-8') as f:
        index = list(csv.DictReader(f))

    failures: List[Tuple[str, str, str]] = []
    for i, row in enumerate(index, 1):
        code = row['code']
        riding = row['riding']
        url = URL_TMPL.format(code=code)
        try:
            html = fetch(code)
            parties = parse_page(html)
        except Exception as e:
            failures.append((code, riding, str(e)))
            continue

        ucp = parties.get('UCP', {})
        ndp = parties.get('NDP', {})
        others_total = sum(p.get('share', 0.0) for k, p in parties.items()
                           if k not in ('UCP', 'NDP'))

        lead_party, _ = leading(parties)
        lead_wp = parties.get(lead_party, {}).get('win_prob', float('nan'))

        ucp_share = ucp.get('share', float('nan'))
        ucp_moe = ucp.get('moe', float('nan'))
        ndp_share = ndp.get('share', float('nan'))
        ndp_moe = ndp.get('moe', float('nan'))

        rows_out.append({
            'district': riding,
            'ucp_share': round(ucp_share, 3),
            'ucp_moe': round(ucp_moe, 3) if ucp_moe == ucp_moe else '',
            'ucp_low': round(ucp_share - ucp_moe, 3) if ucp_moe == ucp_moe else '',
            'ucp_high': round(ucp_share + ucp_moe, 3) if ucp_moe == ucp_moe else '',
            'ndp_share': round(ndp_share, 3),
            'ndp_moe': round(ndp_moe, 3) if ndp_moe == ndp_moe else '',
            'ndp_low': round(ndp_share - ndp_moe, 3) if ndp_moe == ndp_moe else '',
            'ndp_high': round(ndp_share + ndp_moe, 3) if ndp_moe == ndp_moe else '',
            'other_share': round(others_total, 3),
            'leading_party': lead_party,
            'win_prob_leader': round(lead_wp, 2) if lead_wp == lead_wp else '',
            'ucp_win_prob': round(ucp.get('win_prob', float('nan')), 2) if ucp.get('win_prob', float('nan')) == ucp.get('win_prob', float('nan')) else '',
            'ndp_win_prob': round(ndp.get('win_prob', float('nan')), 2) if ndp.get('win_prob', float('nan')) == ndp.get('win_prob', float('nan')) else '',
            'snapshot_date': SNAPSHOT_DATE,
            'source_url': url,
        })
        # Gentle pacing
        time.sleep(0.15)
        if i % 15 == 0:
            print(f"  ... {i}/{len(index)} fetched", file=sys.stderr)

    # Write
    if rows_out:
        cols = list(rows_out[0].keys())
        with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows_out)
        print(f"Wrote {len(rows_out)} rows to {OUT_CSV}")

    if failures:
        print(f"\n{len(failures)} failures:")
        for code, riding, err in failures:
            print(f"  {code} {riding}: {err}")


if __name__ == '__main__':
    main()
