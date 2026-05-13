"""
Alberta Electoral Boundaries — Marginal Seats / Uniform-Swing Analysis
======================================================================
Task: translate the audit's partisan-shift range (roughly 0.5-1.6 pp
efficiency gap, 1-3 seats in a tied election) into concrete historical
context. Which real seats in 2023, 2019, and 2015 would have flipped
under small uniform swings?

Two-party convention:
    2023, 2019:  UCP vs NDP. Two-party NDP share = NDP / (NDP + UCP).
    2015:        No UCP yet. PC + WRP = UCP-equivalent. Two-party NDP
                 share = NDP / (NDP + PC + WRP).

A "uniform swing of X pp toward UCP" means: subtract X pp from each ED's
two-party NDP share, recompute who holds the seat. Candidates outside
the two-party universe (Liberal, AP, Green, IND) are ignored; see
caveats in the findings MD.

Inputs:
    data/alberta_2023_results.csv
    data/alberta_2019_results.csv
    data/alberta_2015_results.csv

Outputs:
    Stdout summary tables + a short findings block that is also written
    into findings/marginal_seats_findings.md by a sibling task.

No pandas/numpy dependency — stdlib only.
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)



import csv
import os
import re
from collections import Counter
from statistics import mean

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "..", "data"))

F_2023 = os.path.join(DATA, "alberta_2023_results.csv")
F_2019 = os.path.join(DATA, "alberta_2019_results.csv")
F_2015 = os.path.join(DATA, "alberta_2015_results.csv")

PARTY_RE = re.compile(r"\(([^)]+)\)\s*$")


def _extract_party(name: str) -> str:
    """'Tyler Shandro (UCP)' -> 'UCP'. Empty / malformed -> ''."""
    if not name:
        return ""
    m = PARTY_RE.search(name.strip())
    return m.group(1).upper() if m else ""


def load_candidate_file(path: str) -> list[dict]:
    """Parse 2019/2023 candidate-level CSVs into per-ED NDP/UCP vote pairs."""
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ed = row["ed_name"].strip()
            region = row.get("region", "").strip()
            ndp_votes = ucp_votes = 0
            for i in range(1, 9):
                cand = row.get(f"cand_{i}") or ""
                votes = row.get(f"votes_{i}") or ""
                if not cand or not votes:
                    continue
                try:
                    v = int(votes)
                except ValueError:
                    continue
                party = _extract_party(cand)
                if party == "NDP":
                    ndp_votes += v
                elif party == "UCP":
                    ucp_votes += v
            out.append(
                {
                    "ed": ed,
                    "region": region,
                    "ndp": ndp_votes,
                    "ucp": ucp_votes,
                }
            )
    return out


def load_2015_file(path: str) -> list[dict]:
    """2015: NDP vs (PC + WRP) as UCP-equivalent."""
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ed = row["ed_2015"].strip()
            ndp = int(row.get("ndp") or 0)
            # ucp_equiv column is already pc+wrp per the parse script, but
            # be defensive: prefer ucp_equiv if present, else pc+wrp.
            ucp_equiv = row.get("ucp_equiv")
            if ucp_equiv not in (None, ""):
                ucp = int(ucp_equiv)
            else:
                ucp = int(row.get("pc") or 0) + int(row.get("wrp") or 0)
            out.append(
                {
                    "ed": ed,
                    "region": "",
                    "ndp": ndp,
                    "ucp": ucp,
                }
            )
    return out


def compute_margins(rows: list[dict]) -> list[dict]:
    """Attach two-party NDP share and signed margin (NDP - UCP)."""
    enriched = []
    for r in rows:
        ndp, ucp = r["ndp"], r["ucp"]
        two_party = ndp + ucp
        if two_party <= 0:
            continue
        ndp_share = ndp / two_party  # 0..1
        margin = ndp_share - 0.5  # signed; positive = NDP won two-party
        enriched.append(
            {
                **r,
                "two_party": two_party,
                "ndp_share": ndp_share,
                "margin": margin,
                "abs_margin_pp": abs(margin) * 100,
                "winner": "NDP" if margin > 0 else "UCP",
            }
        )
    return enriched


def bucket_marginals(enriched: list[dict], threshold_pp: float) -> list[dict]:
    """Return rows where |two-party margin| < threshold_pp (e.g. 5.0)."""
    t = threshold_pp / 100.0
    return [r for r in enriched if abs(r["margin"]) < t]


def apply_uniform_swing(enriched: list[dict], swing_pp_to_ucp: float) -> dict:
    """
    swing_pp_to_ucp > 0 => subtract from NDP share, positive swing to UCP.
    Returns dict with:
        before_counts: (ndp, ucp)
        after_counts: (ndp, ucp)
        flips: list of (ed, old_winner, new_winner, old_margin_pp, new_margin_pp)
    """
    shift = swing_pp_to_ucp / 100.0
    before_n = sum(1 for r in enriched if r["winner"] == "NDP")
    before_u = sum(1 for r in enriched if r["winner"] == "UCP")
    after_n = after_u = 0
    flips = []
    for r in enriched:
        new_share = r["ndp_share"] - shift
        new_winner = "NDP" if new_share > 0.5 else "UCP"
        if new_winner == "NDP":
            after_n += 1
        else:
            after_u += 1
        if new_winner != r["winner"]:
            flips.append(
                {
                    "ed": r["ed"],
                    "region": r["region"],
                    "old_winner": r["winner"],
                    "new_winner": new_winner,
                    "old_margin_pp": (r["ndp_share"] - 0.5) * 100,
                    "new_margin_pp": (new_share - 0.5) * 100,
                }
            )
    return {
        "swing_pp_to_ucp": swing_pp_to_ucp,
        "before": (before_n, before_u),
        "after": (after_n, after_u),
        "flips": flips,
    }


def summarize_election(label: str, enriched: list[dict]) -> dict:
    """Print a block describing this election's marginal structure."""
    n = len(enriched)
    ndp_wins = sum(1 for r in enriched if r["winner"] == "NDP")
    ucp_wins = n - ndp_wins
    bands = {}
    for t in (1.0, 3.0, 5.0):
        m = bucket_marginals(enriched, t)
        bands[t] = m
    print(f"\n=== {label} ===")
    print(f"EDs with valid two-party totals: {n}")
    print(f"Two-party seat count: NDP {ndp_wins} / UCP-equivalent {ucp_wins}")
    for t, rows in bands.items():
        print(f"  |margin| < {t:.1f} pp : {len(rows)} seats")

    # Uniform swings
    swings = {}
    for sw in (-3.0, -1.5, 1.5, 3.0):
        res = apply_uniform_swing(enriched, sw)
        swings[sw] = res
        direction = "toward UCP" if sw > 0 else "toward NDP"
        n_before, u_before = res["before"]
        n_after, u_after = res["after"]
        print(
            f"  Swing {abs(sw):.1f} pp {direction}: "
            f"NDP {n_before}->{n_after}, UCP {u_before}->{u_after}, "
            f"flips={len(res['flips'])}"
        )
    return {
        "label": label,
        "n": n,
        "ndp_wins": ndp_wins,
        "ucp_wins": ucp_wins,
        "bands": bands,
        "swings": swings,
        "enriched": enriched,
    }


def format_margin_table(rows: list[dict], top_n: int = 20) -> str:
    """Sorted ascending by absolute margin — the most vulnerable seats."""
    ordered = sorted(rows, key=lambda r: r["abs_margin_pp"])
    out_lines = []
    for r in ordered[:top_n]:
        out_lines.append(
            f"  {r['ed']:<35} {r['winner']:<4} "
            f"{r['abs_margin_pp']:5.2f} pp  ({r['region']})"
        )
    return "\n".join(out_lines)


def format_flip_list(flips: list[dict]) -> str:
    if not flips:
        return "  (none)"
    out = []
    for f in flips:
        out.append(
            f"  {f['ed']:<35} {f['old_winner']} -> {f['new_winner']}  "
            f"(was {f['old_margin_pp']:+.2f} pp, now {f['new_margin_pp']:+.2f} pp)"
        )
    return "\n".join(out)


# --- Calgary A2 watch list --------------------------------------------------
# The A2 minority-map packing analysis flagged Calgary NDP-leaning districts
# as packed in the minority 2026 proposal. For the purposes of this script
# we treat any Calgary ED where the 2023 two-party NDP share > 0.5 as a
# Zone-A-relevant seat. This is a heuristic not a spatial join; see MD.
def zone_a_candidates(enriched_2023: list[dict]) -> list[dict]:
    return [
        r
        for r in enriched_2023
        if r["region"].lower() == "calgary" and r["ndp_share"] > 0.5
    ]


def main() -> None:
    print("Alberta marginal-seats / uniform-swing analysis")
    print("=" * 60)

    raw23 = load_candidate_file(F_2023)
    raw19 = load_candidate_file(F_2019)
    raw15 = load_2015_file(F_2015)

    enr23 = compute_margins(raw23)
    enr19 = compute_margins(raw19)
    enr15 = compute_margins(raw15)

    s23 = summarize_election("2023 (current boundaries)", enr23)
    s19 = summarize_election("2019 (current boundaries)", enr19)
    s15 = summarize_election(
        "2015 (pre-2017 boundaries — NOT directly comparable)", enr15
    )

    print("\n--- Top 20 closest 2023 seats (two-party margin) ---")
    print(format_margin_table(enr23, 20))

    print("\n--- Seats that flip under a 1.5 pp uniform swing TOWARD UCP (2023) ---")
    print(format_flip_list(s23["swings"][1.5]["flips"]))

    print("\n--- Seats that flip under a 1.5 pp uniform swing TOWARD NDP (2023) ---")
    print(format_flip_list(s23["swings"][-1.5]["flips"]))

    print("\n--- Seats that flip under a 3.0 pp uniform swing TOWARD UCP (2023) ---")
    print(format_flip_list(s23["swings"][3.0]["flips"]))

    print("\n--- Seats that flip under a 3.0 pp uniform swing TOWARD NDP (2023) ---")
    print(format_flip_list(s23["swings"][-3.0]["flips"]))

    # Zone A
    zone_a = zone_a_candidates(enr23)
    zone_a_marginal = [r for r in zone_a if r["abs_margin_pp"] < 3.0]
    print("\n--- Calgary NDP-held 2023 EDs (Zone-A-relevant heuristic) ---")
    print(f"Total: {len(zone_a)}  |  within 3 pp: {len(zone_a_marginal)}")
    for r in sorted(zone_a, key=lambda r: r["abs_margin_pp"])[:15]:
        print(
            f"  {r['ed']:<35} NDP share {r['ndp_share']*100:5.2f}%  "
            f"margin {r['abs_margin_pp']:5.2f} pp"
        )

    # --- Summary block (also written into the findings MD) -----------------
    m3_23 = len(s23["bands"][3.0])
    m3_19 = len(s19["bands"][3.0])
    m3_15 = len(s15["bands"][3.0])
    flips_15_23 = len(s23["swings"][1.5]["flips"])
    flips_15_19 = len(s19["swings"][1.5]["flips"])
    flips_15_15 = len(s15["swings"][1.5]["flips"])
    flips_30_23 = len(s23["swings"][3.0]["flips"])

    summary = f"""
SUMMARY (<200 words)
--------------------
In 2023, {m3_23} of 87 Alberta ridings were decided by a two-party margin
under 3 percentage points; in 2019, {m3_19}; in 2015, {m3_15} (2015 on
older boundaries — not directly comparable). A uniform 1.5 pp shift —
the midpoint of the audit's estimated map-driven swing range — would
have flipped {flips_15_23} seat(s) in 2023, {flips_15_19} in 2019, and
{flips_15_15} in 2015. A 3.0 pp shift in 2023 would flip {flips_30_23}.

The 2023 result (UCP 49 / NDP 38, 11-seat gap) was too lopsided for a
1-3 seat map effect to change which party formed government. But in a
tied or near-tied election — the scenario the audit's efficiency-gap
language addresses — those marginal Calgary seats are exactly where a
1-3 pp map-driven shift decides the outcome. The concrete reading: a
3.9 percent population deviation is not numerically huge, but on the
2023 marginal landscape it is the same order of magnitude as the gap
separating several individual Calgary ridings from flipping.
""".rstrip()

    print(summary)


if __name__ == "__main__":
    main()
