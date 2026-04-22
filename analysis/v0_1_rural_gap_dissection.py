"""
v0_1_rural_gap_dissection.py
============================
Forensic drill-down on the 3.9% rural-mean gap between the minority and majority
2026 Alberta electoral-boundary commission maps.

Headline the audit reported:
    Minority rest-of-province mean = 50,336
    Majority rest-of-province mean = 52,281
    Gap = -3.9% (minority rural ridings are smaller on average)

This script answers:
  1. Which specific rural EDs drive the gap (the 10 smallest rural EDs per map)?
  2. What is the UCP vote share in the 2019 predecessors of those EDs?
  3. Is the minority's smaller rural mean concentrated in UCP-leaning ridings
     (a packing-for-rural-overrep signal) or spread across the partisan spectrum?
  4. Direct ED-by-ED rural population comparison (majority vs minority).

Inputs (all stdlib csv, relative to ../data/):
  - v0_1_majority_2026_populations.csv
  - v0_1_minority_2026_populations.csv
  - v0_1_majority_hybrid_crosswalk.csv
  - v0_1_minority_hybrid_crosswalk.csv
  - v0_1_minority_hybrid_crosswalk_appendixE.csv
  - v0_1_alberta_2019_results.csv
  - v0_1_alberta_2023_results.csv

Outputs (written to this directory):
  - v0_1_rural_gap_smallest10_majority.csv
  - v0_1_rural_gap_smallest10_minority.csv
  - v0_1_rural_gap_ed_comparison.csv
  - v0_1_rural_gap_summary.json
"""

from __future__ import annotations

import csv
import json
import os
import re
from typing import Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = HERE

MAJ_POP = os.path.join(DATA, "v0_1_majority_2026_populations.csv")
MIN_POP = os.path.join(DATA, "v0_1_minority_2026_populations.csv")
MAJ_XWALK = os.path.join(DATA, "v0_1_majority_hybrid_crosswalk.csv")
MIN_XWALK = os.path.join(DATA, "v0_1_minority_hybrid_crosswalk.csv")
MIN_XWALK_E = os.path.join(DATA, "v0_1_minority_hybrid_crosswalk_appendixE.csv")
R2019 = os.path.join(DATA, "v0_1_alberta_2019_results.csv")
R2023 = os.path.join(DATA, "v0_1_alberta_2023_results.csv")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def norm_name(s: str) -> str:
    """Normalise an ED name so 'Airdrie-East' == 'Airdrie East' == 'airdrie east'."""
    if s is None:
        return ""
    s = s.strip().strip('"').lower()
    s = s.replace(".", "")
    s = re.sub(r"[\s\-_]+", " ", s)
    return s


def read_csv(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def is_rural_majority(name: str) -> bool:
    """Majority CSV has no region_type; classify by prefix."""
    return not (name.startswith("Calgary") or name.startswith("Edmonton"))


def is_rural_minority(region_type: str) -> bool:
    """Minority CSV region_type classification: 'Rest' / 'Rest-hybrid' / 'Rest-s15(2)' are rural."""
    return region_type.startswith("Rest")


# --------------------------------------------------------------------------- #
# Vote-share computation from results CSV
# --------------------------------------------------------------------------- #

PARTY_RE = re.compile(r"\(([^)]+)\)\s*$")


def party_share(row: Dict[str, str], target_party: str) -> Optional[float]:
    """
    Return the target_party (e.g. 'UCP' or 'NDP') vote share (0-100) for a
    results row. The results CSV lists candidates as 'Name (PARTY)' in cand_N
    and votes in votes_N, with total_valid_votes.
    """
    try:
        total = float(row.get("total_valid_votes") or 0)
    except ValueError:
        total = 0.0
    if total <= 0:
        return None

    for i in range(1, 9):
        cand = row.get(f"cand_{i}") or ""
        vote_str = row.get(f"votes_{i}") or ""
        if not cand or not vote_str:
            continue
        m = PARTY_RE.search(cand)
        if not m:
            continue
        party = m.group(1).strip().upper()
        if party == target_party.upper():
            try:
                return 100.0 * float(vote_str) / total
            except ValueError:
                return None
    return 0.0  # party didn't run a candidate here


# --------------------------------------------------------------------------- #
# Predecessor mapping: 2026 proposed ED -> list of 2019 predecessors
# --------------------------------------------------------------------------- #

def build_predecessor_map(xwalk_rows: List[Dict[str, str]], key2026: str, key2019: str) -> Dict[str, List[str]]:
    """
    For each 2026 proposed ED (normalised), collect list of 2019 predecessor
    ED names. For non-hybrid proposals the crosswalk often has the same
    name on both sides (identity); for hybrids it has multiple 2019 rows.
    """
    out: Dict[str, List[str]] = {}
    for r in xwalk_rows:
        p2026 = (r.get(key2026) or "").strip().strip('"')
        p2019 = (r.get(key2019) or "").strip().strip('"')
        if not p2026 or not p2019:
            continue
        key = norm_name(p2026)
        out.setdefault(key, []).append(p2019)
    return out


def combined_minority_predecessors() -> Dict[str, List[str]]:
    """
    Merge the two minority crosswalks: the main one (current_2019 ->
    proposed_2026) and the Appendix-E one (current_ed_2019 -> recommended_minority_2026).
    """
    m: Dict[str, List[str]] = {}

    # main
    for r in read_csv(MIN_XWALK):
        p2026 = (r.get("proposed_2026") or "").strip().strip('"')
        p2019 = (r.get("current_2019") or "").strip().strip('"')
        if p2026 and p2019:
            m.setdefault(norm_name(p2026), []).append(p2019)

    # appendix-E (this one is the authoritative minority-specific crosswalk)
    for r in read_csv(MIN_XWALK_E):
        p2026 = (r.get("recommended_minority_2026") or "").strip().strip('"')
        p2019 = (r.get("current_ed_2019") or "").strip().strip('"')
        if p2026 and p2019:
            m.setdefault(norm_name(p2026), []).append(p2019)

    # dedupe lists
    for k, v in m.items():
        seen = []
        for x in v:
            if x not in seen:
                seen.append(x)
        m[k] = seen
    return m


# --------------------------------------------------------------------------- #
# Vote-share lookup with identity fallback
# --------------------------------------------------------------------------- #

def results_by_normname(rows: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    return {norm_name(r["ed_name"]): r for r in rows if r.get("ed_name")}


# Alias: crosswalks use short forms; 2019 results CSV uses the official long form.
# Only add aliases verified by direct inspection of the 2019 results ED list.
PRED_ALIAS = {
    "canmore banff": "banff kananaskis",
    "rocky mountain house sundre": "rimbey rocky mountain house sundre",
    "athabasca barrhead": "athabasca barrhead westlock",
}


def avg_share_for_predecessors(
    predecessors: List[str],
    results_idx: Dict[str, Dict[str, str]],
    party: str,
) -> Tuple[Optional[float], List[str]]:
    """Average party share across predecessor EDs; also return the list used/missed."""
    shares = []
    missed = []
    used = []
    for p in predecessors:
        nk = norm_name(p)
        row = results_idx.get(nk)
        if row is None and nk in PRED_ALIAS:
            row = results_idx.get(PRED_ALIAS[nk])
        if row is None:
            missed.append(p)
            continue
        s = party_share(row, party)
        if s is None:
            missed.append(p)
            continue
        shares.append(s)
        used.append(p)
    if not shares:
        return None, missed
    return sum(shares) / len(shares), used


# --------------------------------------------------------------------------- #
# Main analysis
# --------------------------------------------------------------------------- #

def main() -> None:
    maj_rows = read_csv(MAJ_POP)
    min_rows = read_csv(MIN_POP)

    maj_rural = [
        {"ed_name": r["ed_name"], "population": int(r["population"]), "deviation_pct": r.get("deviation_pct", "")}
        for r in maj_rows if is_rural_majority(r["ed_name"])
    ]
    min_rural = [
        {
            "ed_name": r["ed_name"],
            "population": int(r["population"]),
            "deviation_pct": r.get("deviation_pct", ""),
            "region_type": r.get("region_type", ""),
        }
        for r in min_rows if is_rural_minority(r.get("region_type", ""))
    ]

    maj_mean = sum(e["population"] for e in maj_rural) / len(maj_rural)
    min_mean = sum(e["population"] for e in min_rural) / len(min_rural)
    gap_pct = (min_mean - maj_mean) / maj_mean * 100.0

    print(f"Majority rural N={len(maj_rural)}, mean={maj_mean:,.0f}")
    print(f"Minority rural N={len(min_rural)}, mean={min_mean:,.0f}")
    print(f"Gap = {gap_pct:+.2f}% (minority vs majority)")

    # Sort ascending by population; take 10 smallest
    maj_small10 = sorted(maj_rural, key=lambda x: x["population"])[:10]
    min_small10 = sorted(min_rural, key=lambda x: x["population"])[:10]

    # Predecessors
    maj_predmap = build_predecessor_map(read_csv(MAJ_XWALK), "proposed_2026", "current_2019")
    min_predmap = combined_minority_predecessors()

    # Results indices
    r2019 = read_csv(R2019)
    r2023 = read_csv(R2023)
    idx2019 = results_by_normname(r2019)
    idx2023 = results_by_normname(r2023)

    def enrich(row: Dict, predmap: Dict[str, List[str]]) -> Dict:
        key = norm_name(row["ed_name"])
        preds = predmap.get(key)
        if not preds:
            # identity fallback: the 2026 name itself as 2019 predecessor
            preds = [row["ed_name"]]
        ucp19, used19 = avg_share_for_predecessors(preds, idx2019, "UCP")
        ndp19, _ = avg_share_for_predecessors(preds, idx2019, "NDP")
        ucp23, used23 = avg_share_for_predecessors(preds, idx2023, "UCP")
        ndp23, _ = avg_share_for_predecessors(preds, idx2023, "NDP")
        return {
            **row,
            "predecessors_2019": "; ".join(preds),
            "preds_matched_2019": "; ".join(used19),
            "preds_matched_2023": "; ".join(used23),
            "ucp_share_2019": round(ucp19, 2) if ucp19 is not None else "",
            "ndp_share_2019": round(ndp19, 2) if ndp19 is not None else "",
            "ucp_share_2023": round(ucp23, 2) if ucp23 is not None else "",
            "ndp_share_2023": round(ndp23, 2) if ndp23 is not None else "",
        }

    maj_enriched = [enrich(r, maj_predmap) for r in maj_small10]
    min_enriched = [enrich(r, min_predmap) for r in min_small10]

    # Write smallest-10 tables
    def write_csv(path: str, rows: List[Dict], fieldnames: List[str]) -> None:
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in fieldnames})

    maj_fields = ["ed_name", "population", "deviation_pct",
                  "predecessors_2019", "ucp_share_2019", "ndp_share_2019",
                  "ucp_share_2023", "ndp_share_2023", "preds_matched_2019", "preds_matched_2023"]
    min_fields = ["ed_name", "population", "deviation_pct", "region_type",
                  "predecessors_2019", "ucp_share_2019", "ndp_share_2019",
                  "ucp_share_2023", "ndp_share_2023", "preds_matched_2019", "preds_matched_2023"]

    write_csv(os.path.join(OUT, "v0_1_rural_gap_smallest10_majority.csv"), maj_enriched, maj_fields)
    write_csv(os.path.join(OUT, "v0_1_rural_gap_smallest10_minority.csv"), min_enriched, min_fields)

    # Average UCP / NDP share across the 10 smallest rural EDs per map
    def avg_field(rows, key):
        vals = [float(r[key]) for r in rows if r.get(key) not in ("", None)]
        return sum(vals) / len(vals) if vals else None

    summary = {
        "maj_rural_n": len(maj_rural),
        "min_rural_n": len(min_rural),
        "maj_rural_mean_pop": round(maj_mean, 1),
        "min_rural_mean_pop": round(min_mean, 1),
        "gap_pct_minority_vs_majority": round(gap_pct, 2),
        "smallest10": {
            "majority": {
                "avg_pop": round(sum(r["population"] for r in maj_small10) / 10.0, 1),
                "avg_ucp_2019": round(avg_field(maj_enriched, "ucp_share_2019"), 2) if avg_field(maj_enriched, "ucp_share_2019") else None,
                "avg_ndp_2019": round(avg_field(maj_enriched, "ndp_share_2019"), 2) if avg_field(maj_enriched, "ndp_share_2019") else None,
                "avg_ucp_2023": round(avg_field(maj_enriched, "ucp_share_2023"), 2) if avg_field(maj_enriched, "ucp_share_2023") else None,
                "avg_ndp_2023": round(avg_field(maj_enriched, "ndp_share_2023"), 2) if avg_field(maj_enriched, "ndp_share_2023") else None,
            },
            "minority": {
                "avg_pop": round(sum(r["population"] for r in min_small10) / 10.0, 1),
                "avg_ucp_2019": round(avg_field(min_enriched, "ucp_share_2019"), 2) if avg_field(min_enriched, "ucp_share_2019") else None,
                "avg_ndp_2019": round(avg_field(min_enriched, "ndp_share_2019"), 2) if avg_field(min_enriched, "ndp_share_2019") else None,
                "avg_ucp_2023": round(avg_field(min_enriched, "ucp_share_2023"), 2) if avg_field(min_enriched, "ucp_share_2023") else None,
                "avg_ndp_2023": round(avg_field(min_enriched, "ndp_share_2023"), 2) if avg_field(min_enriched, "ndp_share_2023") else None,
            },
        },
    }

    # --------------------------------------------------------------- #
    # ED-by-ED rural comparison: match majority ED to nearest minority ED by name
    # Some names differ slightly; we use normalised name fuzzy bucket (exact normalised
    # match first, then a loose contains-based match).
    # --------------------------------------------------------------- #
    min_by_nkey = {norm_name(r["ed_name"]): r for r in min_rural}
    min_keys = list(min_by_nkey.keys())

    def find_min_match(maj_name: str) -> Optional[str]:
        k = norm_name(maj_name)
        if k in min_by_nkey:
            return k
        # token-overlap fallback
        toks = set(k.split())
        best = None
        best_overlap = 0
        for mk in min_keys:
            ov = len(toks & set(mk.split()))
            if ov > best_overlap:
                best = mk
                best_overlap = ov
        return best if best_overlap >= max(1, len(toks) // 2) else None

    comp_rows = []
    for mr in maj_rural:
        mk = find_min_match(mr["ed_name"])
        if mk is None:
            comp_rows.append({
                "majority_name": mr["ed_name"],
                "majority_pop": mr["population"],
                "minority_name": "",
                "minority_pop": "",
                "delta_pop": "",
                "direction": "NO_MIN_MATCH",
            })
            continue
        minr = min_by_nkey[mk]
        delta = minr["population"] - mr["population"]
        direction = "minority_larger" if delta > 0 else ("minority_smaller" if delta < 0 else "equal")
        comp_rows.append({
            "majority_name": mr["ed_name"],
            "majority_pop": mr["population"],
            "minority_name": minr["ed_name"],
            "minority_pop": minr["population"],
            "delta_pop": delta,
            "direction": direction,
        })

    comp_rows.sort(key=lambda r: r["delta_pop"] if isinstance(r["delta_pop"], int) else 0)
    write_csv(os.path.join(OUT, "v0_1_rural_gap_ed_comparison.csv"),
              comp_rows,
              ["majority_name", "majority_pop", "minority_name", "minority_pop", "delta_pop", "direction"])

    # Direction tally
    dir_counts = {}
    for r in comp_rows:
        dir_counts[r["direction"]] = dir_counts.get(r["direction"], 0) + 1
    summary["direction_tally"] = dir_counts

    with open(os.path.join(OUT, "v0_1_rural_gap_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Summary ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
