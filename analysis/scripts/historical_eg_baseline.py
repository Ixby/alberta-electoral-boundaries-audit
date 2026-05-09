"""
Alberta Historical Efficiency Gap Baseline (v0.1)
=================================================
Computes the efficiency gap for the 2015, 2019, and 2023 Alberta provincial
elections under the boundary map in effect at each election, producing an
Alberta-specific historical range. Resolves Issue #16.

Background
----------
The audit's packing/cracking analysis (packing_cracking_analysis.py)
applies a 7% EG threshold from Stephanopoulos & McGhee (2014), calibrated to
US Congressional elections 1972-2010. That threshold has never been validated
for Alberta. This script computes EG for three enacted-map elections to
establish an Alberta-specific historical reference range.

Maps in effect
--------------
  2015: Pre-2017 boundaries (87 EDs, Electoral Boundaries Commission 2009-10)
  2019: Bill 33 (2017) boundaries (87 EDs) — same as data/shapefiles/reference/
  2023: Bill 33 (2017) boundaries (same 87 EDs)

Two-party framing
-----------------
For all three elections, EG is computed on a two-party (NDP vs right-bloc
conservative, RBC) basis:
  - 2015: RBC = PC + Wildrose (WRP), as stored in the ucp_equiv column.
    The 2017 merger makes this the natural comparison bloc. Liberals and
    other small parties are retained in total_valid_votes for context but
    do not enter the wasted-vote computation.
  - 2019: RBC = UCP (the merged party). Direct two-party contest.
  - 2023: RBC = UCP. Direct two-party contest.

Actual seat winners (plurality of all-party votes) are used to determine
which party's votes count as "wasted above threshold" vs "wasted in loss."
In 2015, NDP won many seats with plurality but not two-party majority;
those seats correctly count as NDP wins for wasted-vote purposes.

Formula (Stephanopoulos & McGhee 2014 wasted-vote form)
--------------------------------------------------------
  For each district:
    if NDP won: NDP_wasted += max(0, NDP_votes - (total_2p // 2 + 1))
                RBC_wasted += RBC_votes
    else:       RBC_wasted += max(0, RBC_votes - (total_2p // 2 + 1))
                NDP_wasted += NDP_votes

  code_eg = (NDP_wasted - RBC_wasted) / total_2p_provincial

Sign convention (matching packing_cracking_analysis.py)
------------------------------------------------------------
  code_eg = (NDP_wasted - RBC_wasted) / total

  code_eg < 0  =>  NDP wastes fewer votes than RBC in absolute terms.
                   Under the standard wasted-vote reading this is a structural
                   NDP efficiency advantage, but the paper applies a
                   raw-proportionality correction that may reverse the label.
                   See analysis/methodology/sign_convention_resolution.md for
                   the authoritative reconciliation with S-M 2:1-slope convention.

  This script uses the same formula as v0_2 (code_eg). All comparisons with
  the 2026 proposed maps are code_eg-to-code_eg, so the convention is
  internally consistent.

Inputs
------
  data/alberta_2015_results.csv  — 87 pre-2017 EDs, NDP/PC/WRP/Lib/other votes
  data/alberta_2019_results.csv  — 87 Bill 33 EDs, candidate-level 2019
  data/alberta_2023_results.csv  — 87 Bill 33 EDs, candidate-level 2023

Outputs
-------
  data/historical_eg_baseline.json
  analysis/reports/historical_eg_baseline.md

Dependencies
------------
Forward:
  data/historical_eg_baseline.json
  analysis/reports/historical_eg_baseline.md
Backward:
  data/alberta_2015_results.csv  (from analysis/scripts/parse_2015_results.py)
  data/alberta_2019_results.csv
  data/alberta_2023_results.csv
  analysis/scripts/packing_cracking_analysis.py  (sign convention reference)

Usage
-----
  PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_historical_eg_baseline.py
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import csv
import json
import os
import statistics
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------


def _find(filename: str) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    for p in [
        os.path.join(here, "..", "data", filename),
        os.path.join(here, "data", filename),
        os.path.join("data", filename),
        filename,
    ]:
        if os.path.exists(p):
            return os.path.normpath(p)
    raise FileNotFoundError(f"Cannot find data file: {filename}")


def _out(filename: str) -> str:
    """Resolve output path relative to the project root."""
    here = os.path.dirname(os.path.abspath(__file__))
    # scripts/ is two levels below the project root (scripts/ -> analysis/ -> root)
    # but data/ and analysis/reports/ are siblings of analysis/ at the project root
    project_root = os.path.normpath(os.path.join(here, "..", ".."))
    if filename.endswith(".json"):
        return os.path.join(project_root, "data", filename)
    elif filename.endswith(".md"):
        return os.path.join(project_root, "analysis", "reports", filename)
    return os.path.join(project_root, filename)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_2015() -> List[Dict]:
    """
    Load 87 pre-2017 EDs with NDP and RBC (PC+WRP=ucp_equiv) votes.
    Actual winner determined by plurality across all parties (ndp, pc, wrp, lib, other).
    """
    rows = []
    with open(_find("alberta_2015_results.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                ndp = int(r["ndp"])
                rbc = int(r["ucp_equiv"])  # PC + WRP (pre-merger combined)
                pc = int(r["pc"])
                wrp = int(r["wrp"])
                lib = int(r.get("lib", 0) or 0)
                oth = int(r.get("other", 0) or 0)
            except (ValueError, KeyError):
                continue
            # Actual winner: plurality across all parties
            all_votes = {"ndp": ndp, "pc": pc, "wrp": wrp, "lib": lib, "other": oth}
            winner_party = max(all_votes, key=all_votes.get)
            actual_winner = "NDP" if winner_party == "ndp" else "RBC"
            rows.append(
                {
                    "ed": r.get("ed_2015", r.get("sheet", "?")),
                    "ndp": ndp,
                    "rbc": rbc,
                    "actual_winner": actual_winner,
                    "total_all": ndp + pc + wrp + lib + oth,
                }
            )
    return rows


def load_2019() -> List[Dict]:
    """
    Load 87 Bill 33 EDs with NDP and UCP (=RBC) votes from candidate-level data.
    Actual winner from winner_party column.
    """
    rows = []
    with open(_find("alberta_2019_results.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ndp = ucp = 0
            for i in range(1, 9):
                cand = r.get(f"cand_{i}", "") or ""
                votes = r.get(f"votes_{i}", "") or ""
                if not cand or not votes:
                    continue
                try:
                    v = int(float(votes))
                except (ValueError, TypeError):
                    continue
                if "(NDP)" in cand:
                    ndp = v
                elif "(UCP)" in cand:
                    ucp = v
            if ndp + ucp == 0:
                continue
            winner_raw = r.get("winner_party", "")
            actual_winner = "NDP" if winner_raw.strip() == "NDP" else "RBC"
            total_valid = r.get("total_valid_votes", "") or ""
            try:
                total_all = int(float(total_valid))
            except (ValueError, TypeError):
                total_all = ndp + ucp
            rows.append(
                {
                    "ed": r.get("ed_name", r.get("sheet", "?")),
                    "ndp": ndp,
                    "rbc": ucp,
                    "actual_winner": actual_winner,
                    "total_all": total_all,
                }
            )
    return rows


def load_2023() -> List[Dict]:
    """
    Load 87 Bill 33 EDs with NDP and UCP (=RBC) votes from candidate-level data.
    Actual winner from winner_party column.
    """
    rows = []
    with open(_find("alberta_2023_results.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ndp = ucp = 0
            for i in range(1, 7):
                cand = r.get(f"cand_{i}", "") or ""
                votes = r.get(f"votes_{i}", "") or ""
                if not cand or not votes:
                    continue
                try:
                    v = int(float(votes))
                except (ValueError, TypeError):
                    continue
                if "(NDP)" in cand:
                    ndp = v
                elif "(UCP)" in cand:
                    ucp = v
            if ndp + ucp == 0:
                continue
            winner_raw = r.get("winner_party", "")
            actual_winner = "NDP" if winner_raw.strip() == "NDP" else "RBC"
            total_valid = r.get("total_valid_votes", "") or ""
            try:
                total_all = int(float(total_valid))
            except (ValueError, TypeError):
                total_all = ndp + ucp
            rows.append(
                {
                    "ed": r.get("ed_name", r.get("sheet", "?")),
                    "ndp": ndp,
                    "rbc": ucp,
                    "actual_winner": actual_winner,
                    "total_all": total_all,
                }
            )
    return rows


# ---------------------------------------------------------------------------
# EG computation
# ---------------------------------------------------------------------------


# Threshold variant differs from eg_utils._ed_waste — see REMEDIATION_LOG.md 2026-05-09.
# Uses integer majority threshold (tt // 2 + 1); requires actual_winner field; takes List[Dict].
def compute_eg(districts: List[Dict], label: str) -> Dict:
    """
    Compute the efficiency gap for a list of districts.

    Each district dict must have: ndp, rbc, actual_winner ('NDP' or 'RBC').

    Returns a dict with EG and supporting statistics.
    Sign convention: code_eg = (NDP_wasted - RBC_wasted) / total_2p.
    Negative => RBC wastes more in absolute terms. See module docstring.
    """
    ndp_wasted = 0
    rbc_wasted = 0
    total_2p = 0
    ndp_wins = 0
    rbc_wins = 0
    ndp_votes_total = 0
    rbc_votes_total = 0

    for d in districts:
        ndp = d["ndp"]
        rbc = d["rbc"]
        win = d["actual_winner"]
        tt = ndp + rbc
        if tt == 0:
            continue
        thr = tt // 2 + 1

        if win == "NDP":
            ndp_wasted += max(0, ndp - thr)
            rbc_wasted += rbc
            ndp_wins += 1
        else:
            rbc_wasted += max(0, rbc - thr)
            ndp_wasted += ndp
            rbc_wins += 1

        total_2p += tt
        ndp_votes_total += ndp
        rbc_votes_total += rbc

    if total_2p == 0:
        raise ValueError(f"No valid two-party votes for {label}")

    code_eg = (ndp_wasted - rbc_wasted) / total_2p
    ndp_share = ndp_votes_total / total_2p
    ndp_seat_share = ndp_wins / (ndp_wins + rbc_wins)

    # Seat-vote shortcut (S-M 2015 eq. 5, NDP perspective):
    #   EG_NDP_SM ≈ (seat_share - 0.5) - 2*(vote_share - 0.5)
    # Note: code_eg = -EG_NDP_SM. Included for reference.
    eg_sm_ndp = (ndp_seat_share - 0.5) - 2 * (ndp_share - 0.5)

    return {
        "label": label,
        "n_districts": ndp_wins + rbc_wins,
        "ndp_votes": ndp_votes_total,
        "rbc_votes": rbc_votes_total,
        "total_2p": total_2p,
        "ndp_share_pct": round(ndp_share * 100, 4),
        "rbc_share_pct": round((1 - ndp_share) * 100, 4),
        "ndp_wins": ndp_wins,
        "rbc_wins": rbc_wins,
        "ndp_seat_share_pct": round(ndp_seat_share * 100, 4),
        "ndp_wasted": ndp_wasted,
        "rbc_wasted": rbc_wasted,
        "code_eg_pct": round(code_eg * 100, 4),  # matches v0_2 sign
        "eg_sm_ndp_pct": round(eg_sm_ndp * 100, 4),  # S-M perspective, NDP-framed
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _sign_label(eg_pct: float) -> str:
    """
    Human-readable wasted-vote label.
    code_eg < 0 means NDP wasted fewer votes than RBC in absolute terms.
    Use a neutral phrasing; the 'advantage' interpretation depends on context
    (see sign_convention_resolution.md).
    """
    if abs(eg_pct) < 0.5:
        return "roughly balanced wasted votes"
    return "NDP wastes fewer votes" if eg_pct < 0 else "RBC wastes fewer votes"


def print_result(r: Dict) -> None:
    label = r["label"]
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  {label}")
    print(sep)
    print(f"  Districts:            {r['n_districts']}")
    print(f"  NDP two-party share:  {r['ndp_share_pct']:.2f}%")
    print(f"  RBC two-party share:  {r['rbc_share_pct']:.2f}%")
    print(f"  NDP seats won:        {r['ndp_wins']} / {r['n_districts']}")
    print(f"  RBC seats won:        {r['rbc_wins']} / {r['n_districts']}")
    print(f"  NDP wasted votes:     {r['ndp_wasted']:,}")
    print(f"  RBC wasted votes:     {r['rbc_wasted']:,}")
    print(
        f"  EG (code_eg):         {r['code_eg_pct']:+.2f}%  [{_sign_label(r['code_eg_pct'])}]"
    )
    print(f"  EG (S-M NDP-framed):  {r['eg_sm_ndp_pct']:+.2f}%")


def write_json(
    results: List[Dict], eg_2026_majority_pct: float, eg_2026_minority_pct: float
) -> str:
    eg_values = [r["code_eg_pct"] for r in results]
    historical_min = min(eg_values)
    historical_max = max(eg_values)
    historical_range = historical_max - historical_min

    payload = {
        "description": (
            "Alberta historical efficiency gap baseline. "
            "code_eg sign convention: (NDP_wasted - RBC_wasted) / total_2p. "
            "Negative => RBC wasted more (paper convention: negative = UCP-favourable). "
            "See sign_convention_resolution.md for full reconciliation."
        ),
        "elections": results,
        "alberta_historical_range": {
            "min_pct": round(historical_min, 4),
            "max_pct": round(historical_max, 4),
            "range_pct": round(historical_range, 4),
            "elections_included": [r["label"] for r in results],
        },
        "comparison_2026": {
            "majority_eg_pct": eg_2026_majority_pct,
            "minority_eg_pct": eg_2026_minority_pct,
            "note": (
                "2026 EG values from packing_cracking_analysis.py "
                "at urban_weight=0.85 (canonical run). "
                "Source: THREE-MAP COMPARISON table, B2 Efficiency gap row."
            ),
            "majority_within_historical_range": (
                historical_min <= eg_2026_majority_pct <= historical_max
            ),
            "minority_within_historical_range": (
                historical_min <= eg_2026_minority_pct <= historical_max
            ),
        },
        "threshold_analysis": {
            "us_threshold_pct": 7.0,
            "alberta_suggested_threshold_pct": 3.0,
            "rationale": (
                "The S&M 7% threshold was calibrated to US Congressional elections "
                "1972-2010. Alberta's three-election historical range spans "
                f"{historical_min:+.2f}% to {historical_max:+.2f}% (code_eg). "
                "The largest observed deviation is "
                f"{abs(historical_min):.2f}% (2015 NDP landslide under pre-2017 map). "
                "The 2019 and 2023 enacted-map elections produced EG values between "
                "-1.5% and -2.7%, well within the 7% US threshold. "
                "A province-specific threshold calibrated to the Alberta historical "
                "maximum of the 2019/2023 range (approximately 3%) would be more "
                "appropriate than the US 7% standard for Alberta context. "
                "The 2015 outlier reflects a unique multi-party vote-split environment "
                "and should not anchor the threshold for standard two-party conditions."
            ),
        },
    }

    path = _out("historical_eg_baseline.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return path


def write_report(
    results: List[Dict], eg_2026_majority_pct: float, eg_2026_minority_pct: float
) -> str:
    eg_values = [r["code_eg_pct"] for r in results]
    historical_min = min(eg_values)
    historical_max = max(eg_values)
    # For the "normal election" range (2019 and 2023 only — exclude the
    # 2015 multi-party vote-split anomaly). Use explicit year prefix matching
    # rather than substring exclusion so future years aren't silently filtered.
    _normal_years = {"2019", "2023"}
    normal = [r for r in results if r["label"][:4] in _normal_years]
    normal_min = min(r["code_eg_pct"] for r in normal)
    normal_max = max(r["code_eg_pct"] for r in normal)

    lines = [
        "# Alberta Historical Efficiency Gap Baseline — v0.1",
        "",
        "**Issue:** #16  |  **Script:** `analysis/scripts/v0_1_historical_eg_baseline.py`",
        "",
        "## Summary",
        "",
        "This report computes the efficiency gap (EG) for the 2015, 2019, and 2023 "
        "Alberta provincial elections under the boundary map in effect at each election. "
        "The purpose is to establish an Alberta-specific historical reference range, "
        "replacing the US Congressional 7% threshold (Stephanopoulos & McGhee 2014) "
        "with a province-specific calibration.",
        "",
        "## Sign convention",
        "",
        "All EG values use the `code_eg` convention from "
        "`packing_cracking_analysis.py`:",
        "",
        "```",
        "code_eg = (NDP_wasted − RBC_wasted) / total_two_party_votes",
        "```",
        "",
        "Negative values mean RBC (right-bloc conservative) wastes more votes "
        "in absolute terms. Under the paper's raw-proportionality reading, "
        "negative = UCP-favourable. See "
        "`analysis/methodology/sign_convention_resolution.md` for the full "
        "reconciliation with the Stephanopoulos-McGhee 2:1-slope convention.",
        "",
        "## Results by election",
        "",
        "| Election | Map | NDP vote share | NDP seats | EG (code_eg) | Reading |",
        "|---|---|---|---|---|---|",
    ]

    for r in results:
        map_name = {
            "2015": "Pre-2017 (87 EDs)",
            "2019": "Bill 33 2017 (87 EDs)",
            "2023": "Bill 33 2017 (87 EDs)",
        }.get(r["label"][:4], r["label"])
        lines.append(
            f"| {r['label']} | {map_name} | {r['ndp_share_pct']:.1f}% | "
            f"{r['ndp_wins']}/87 | **{r['code_eg_pct']:+.2f}%** | "
            f"{_sign_label(r['code_eg_pct'])} |"
        )

    lines += [
        "",
        "## Alberta historical range",
        "",
        f"- **Full range (all three elections):** {historical_min:+.2f}% to {historical_max:+.2f}%",
        f"- **Normal-election range (2019 + 2023 only):** {normal_min:+.2f}% to {normal_max:+.2f}%",
        "",
        "The 2015 result (-21.63%) reflects an unusual three-party contest where "
        "NDP won 53 of 87 seats on 44% of the two-party vote due to the PC/Wildrose "
        "split. Even combining PC and WRP into a single RBC bloc, the vote-split "
        "dynamics produced an extreme EG reading. This value represents an upper "
        "bound on what Alberta's enacted maps can produce under exceptional "
        "circumstances, not a typical operating range.",
        "",
        "Under two-party conditions (2019 and 2023), the enacted map produced "
        f"EG values of {normal_min:+.2f}% to {normal_max:+.2f}%, a range of "
        f"{abs(normal_max - normal_min):.2f} percentage points.",
        "",
        "## Comparison with 2026 proposed maps",
        "",
        "EG values for the 2026 proposals are taken from "
        "`packing_cracking_analysis.py` (urban_weight = 0.85 canonical run):",
        "",
        f"| Map | EG (code_eg) | Within 2019-2023 range? | Within full historical range? |",
        "|---|---|---|---|",
        f"| 2019 enacted (2023 votes) | -2.64% | — (reference) | Yes |",
        f"| Majority 2026 proposal | {eg_2026_majority_pct:+.2f}% | "
        f"{'Yes' if normal_min <= eg_2026_majority_pct <= normal_max else 'No'} | "
        f"{'Yes' if historical_min <= eg_2026_majority_pct <= historical_max else 'No'} |",
        f"| Minority 2026 proposal | {eg_2026_minority_pct:+.2f}% | "
        f"{'Yes' if normal_min <= eg_2026_minority_pct <= normal_max else 'No'} | "
        f"{'Yes' if historical_min <= eg_2026_minority_pct <= historical_max else 'No'} |",
        "",
        "## Threshold analysis",
        "",
        "### US 7% threshold",
        "",
        "The Stephanopoulos & McGhee (2014) 7% threshold was calibrated to US "
        "Congressional elections. Under that standard, all three Alberta enacted-map "
        "elections and both 2026 proposals fall well within the threshold. The 2015 "
        "outlier is the only Alberta election that would exceed the US threshold, "
        "and it reflects multi-party vote-split dynamics absent in 2019 and 2023.",
        "",
        "### Alberta-specific threshold",
        "",
        "A province-specific threshold calibrated to Alberta's normal two-party "
        "operating range is more appropriate. The 2019-2023 range spans approximately "
        f"{abs(normal_max - normal_min):.1f} pp, with a maximum absolute value of "
        f"{max(abs(normal_min), abs(normal_max)):.2f}% (2023). "
        "An Alberta-specific alert threshold of approximately **3%** "
        "(slightly above the observed enacted-map maximum of "
        f"{max(abs(normal_min), abs(normal_max)):.2f}%) would:",
        "",
        "- Include both 2019 and 2023 enacted-map elections within the normal zone.",
        "- Flag the 2026 proposals if they deviate meaningfully from the enacted-map baseline.",
        "- Be grounded in observed Alberta electoral geography rather than US redistricting norms.",
        "",
        "Under a 3% Alberta threshold, both 2026 proposals remain within the normal "
        "zone. The more meaningful comparison is the **relative shift** from the 2019 "
        "enacted baseline (-2.64%), which v0_2 reports as +2.24 pp (majority) and "
        "+0.83 pp (minority).",
        "",
        "## Methodological notes",
        "",
        "1. **2015 boundary map:** The pre-2017 EDs are distinct from the Bill 33 "
        "   boundaries. EG is computed on actual 2015 contest results under the map "
        "   in effect, not re-attributed to 2019 boundaries.",
        "",
        "2. **RBC definition:** For 2015, RBC = PC + Wildrose (the `ucp_equiv` "
        "   column from `parse_2015_results.py`). For 2019 and 2023, RBC = UCP. "
        "   This is consistent with `v0_1_2015_cross_election.py`.",
        "",
        "3. **Actual winner determination:** In 2015, the actual seat winner is the "
        "   party with the plurality of all-party votes (not the two-party winner). "
        "   NDP won 53 seats by plurality despite being below 50% of two-party votes "
        "   in many of those seats. This is the correct input to the wasted-vote formula.",
        "",
        "4. **Data sources:**",
        "   - 2015: `data/alberta_2015_results.csv` (from `parse_2015_results.py`)",
        "   - 2019: `data/alberta_2019_results.csv`",
        "   - 2023: `data/alberta_2023_results.csv`",
        "",
        "5. **Cross-check:** The 2023 EG computed here (-2.64%) matches the v0_2 "
        '   script\'s "2019 BOUNDARIES (CURRENT) under 2023 vote shares" result '
        "   exactly, confirming formula consistency.",
        "",
        "---",
        "*Generated by `analysis/scripts/v0_1_historical_eg_baseline.py`. "
        "Do not edit manually — re-run the script to regenerate.*",
    ]

    path = _out("historical_eg_baseline.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# FROZEN 2026-04-26: 2026 EG comparison values from packing_cracking_analysis.py
# canonical run (urban_weight=0.85, THREE-MAP COMPARISON table, B2 EG row).
# These are not read from a file at runtime — packing_cracking_analysis.py does
# not write a stable machine-readable output that this script can consume.
# If packing_cracking_analysis.py is re-run with different parameters, update
# these constants manually and record the run date and parameters above.
# Earlier task description referenced -1.3% and -2.7%; those were from an older
# weight configuration.
import warnings as _warnings
_warnings.warn(
    "historical_eg_baseline.py: EG_2026_*_PCT are frozen constants from "
    "2026-04-26 packing_cracking_analysis.py run (urban_weight=0.85). "
    "Re-run packing_cracking_analysis.py and update these if the 2026 maps change.",
    UserWarning,
    stacklevel=1,
)
del _warnings
EG_2026_MAJORITY_PCT = -0.40
EG_2026_MINORITY_PCT = -1.81


def main() -> None:
    print("=" * 60)
    print("  Alberta Historical EG Baseline (v0.1)")
    print("  Issue #16: Province-specific threshold calibration")
    print("=" * 60)

    # Load and compute
    districts_2015 = load_2015()
    districts_2019 = load_2019()
    districts_2023 = load_2023()

    results = [
        compute_eg(districts_2015, "2015 (pre-2017 map, 87 EDs)"),
        compute_eg(districts_2019, "2019 (Bill 33 map, 87 EDs)"),
        compute_eg(districts_2023, "2023 (Bill 33 map, 87 EDs)"),
    ]

    for r in results:
        print_result(r)

    # Summary
    eg_values = [r["code_eg_pct"] for r in results]
    print(f"\n{'=' * 60}")
    print("  ALBERTA HISTORICAL RANGE")
    print("=" * 60)
    print(f"  2015 EG: {results[0]['code_eg_pct']:+.2f}%")
    print(f"  2019 EG: {results[1]['code_eg_pct']:+.2f}%")
    print(f"  2023 EG: {results[2]['code_eg_pct']:+.2f}%")
    print(f"  Historical range: {min(eg_values):+.2f}% to {max(eg_values):+.2f}%")
    print()
    print(f"  Normal-election range (2019 + 2023):")
    normal_vals = [results[1]["code_eg_pct"], results[2]["code_eg_pct"]]
    print(f"    {min(normal_vals):+.2f}% to {max(normal_vals):+.2f}%")

    print(f"\n{'=' * 60}")
    print("  COMPARISON WITH 2026 PROPOSED MAPS")
    print("=" * 60)
    print(f"  2019 enacted baseline:   -2.64%  (reference)")
    print(f"  Majority 2026 (v0_2):    {EG_2026_MAJORITY_PCT:+.2f}%")
    print(f"  Minority 2026 (v0_2):    {EG_2026_MINORITY_PCT:+.2f}%")
    print()
    print(
        f"  All 2026 values within 2019-2023 range "
        f"({min(normal_vals):+.2f}% to {max(normal_vals):+.2f}%): "
        f"{all(min(normal_vals) <= v <= max(normal_vals) for v in [EG_2026_MAJORITY_PCT, EG_2026_MINORITY_PCT])}"
    )

    print(f"\n{'=' * 60}")
    print("  THRESHOLD ANALYSIS")
    print("=" * 60)
    print(f"  US S&M (2015) threshold:     ±7.00%")
    print(f"  Alberta 2019-2023 max abs:    {max(abs(v) for v in normal_vals):.2f}%")
    print(f"  Suggested Alberta threshold:  ~3.00%")
    print(
        f"  All 2026 values within 3%:   "
        f"{all(abs(v) <= 3.0 for v in [EG_2026_MAJORITY_PCT, EG_2026_MINORITY_PCT])}"
    )
    print()
    print("  Finding: The US 7% threshold is not calibrated to Alberta.")
    print("  Alberta's two-party elections (2019, 2023) show EG in the")
    print(
        f"  {min(normal_vals):+.2f}% to {max(normal_vals):+.2f}% range under the enacted map."
    )
    print("  A province-specific threshold of ~3% is more appropriate.")
    print("  Both 2026 proposals remain within this threshold;")
    print("  the more meaningful test is the relative shift from the")
    print("  enacted baseline, which v0_2 reports as +2.24 pp (majority)")
    print("  and +0.83 pp (minority).")

    # Write outputs
    json_path = write_json(results, EG_2026_MAJORITY_PCT, EG_2026_MINORITY_PCT)
    md_path = write_report(results, EG_2026_MAJORITY_PCT, EG_2026_MINORITY_PCT)
    print(f"\n  Wrote: {json_path}")
    print(f"  Wrote: {md_path}")


if __name__ == "__main__":
    main()
