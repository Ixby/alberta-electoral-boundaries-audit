"""
Alberta Cross-Election Analysis (v0.1) — 2015 votes on 2019 and 2026 maps.
==========================================================================

Extends the 2019/2023 two-election direction-stability test (see
analysis/scripts/v0_3_monte_carlo_ci.py) by adding a 2015 third data point.

Construction:

1. Load the 2015 election results per pre-2017 ED (from parse_2015_results.py
   output: data/v0_1_alberta_2015_results.csv).

2. Load the 2015-to-2019 crosswalk
   (data/v0_1_2015_to_2019_crosswalk.csv) and re-attribute pre-2017 ED
   votes to post-2017 (2019) ED boundaries using population_weight as the
   vote-attribution weight.

3. Combine PC + Wildrose into UCP-equivalent (the 2017 merger) at the ED
   level. Match parse_2015_results.py's approach. Liberal and other
   small-party votes are retained for turnout denominators but do not
   contribute to EG wasted-vote computation (consistent with the audit's
   two-party framing in v0_2_packing_cracking_analysis).

4. Run compute_metrics() (the existing B1-B6 suite) on:
   a. 2019 map with 2015-attributed votes
   b. Majority 2026 (via hybrid crosswalk)
   c. Minority 2026 (via hybrid crosswalk)

5. Compute cross-election direction-stability: is the
   minority-majority EG asymmetry direction consistent with the
   2019-vote and 2023-vote results?

Caveats:
- Weighted vote re-attribution is population-proportional, not
  polling-division-accurate. It assumes the partisan geography within
  each 2015 ED is uniform. For splits this is a first-order
  approximation.
- "Rural" baseline under 2015 is ambiguous because 2015 EDs were
  boundary-different. We use an ED-name heuristic (Calgary-*/Edmonton-*
  else rural). See v0_1_cross_election_rural_baseline.py.

Usage:
  PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_2015_cross_election.py
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from v0_2_packing_cracking_analysis import (
    compute_metrics,
    estimate_2026,
    MAJORITY_2026_MAPPING,
    MINORITY_2026_MAPPING,
)

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"


# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------

def clean_2015_ed_name(name: str) -> str:
    if name.startswith("Statement Of Results By Poll - "):
        return name[len("Statement Of Results By Poll - "):]
    return name


def load_2015_results() -> list:
    """Load per-ED 2015 totals: NDP, PC, WRP, Liberal, other."""
    rows = []
    with open(DATA / "v0_1_alberta_2015_results.csv") as f:
        for r in csv.DictReader(f):
            name = clean_2015_ed_name(r["ed_2015"])
            rows.append({
                "ed_2015": name,
                "ndp": int(r["ndp"]),
                "ucp_equiv": int(r["ucp_equiv"]),  # PC + WRP
                "lib": int(r["lib"]),
                "other": int(r["other"]),
                "total": int(r["total"]),
            })
    return rows


def load_crosswalk() -> list:
    rows = []
    with open(DATA / "v0_1_2015_to_2019_crosswalk.csv") as f:
        for r in csv.DictReader(f):
            rows.append({
                "ed_2015": r["ed_2015_2010boundaries"],
                "ed_2019": r["ed_2019_2017boundaries"],
                "change_type": r["change_type"],
                "weight": float(r["population_weight"]),
                "confidence": r["confidence"],
            })
    return rows


def region_from_2019_name(ed_name: str) -> str:
    n = ed_name.strip()
    if n.lower().startswith("calgary"):
        return "Calgary"
    if n.lower().startswith("edmonton"):
        return "Edmonton"
    return "Rest of Alberta"


# ---------------------------------------------------------------------
# 2015 -> 2019 re-attribution
# ---------------------------------------------------------------------

def attribute_2015_to_2019(
    votes_2015: list, crosswalk: list
) -> list:
    """Return a list of 2019-boundary EDs with NDP + UCP-equiv vote totals.

    Apply population_weight as the re-attribution weight. This treats
    partisan geography within each 2015 ED as uniform — a first-order
    approximation.
    """
    by_2015 = {r["ed_2015"]: r for r in votes_2015}
    accum = defaultdict(lambda: {"ndp": 0.0, "ucp": 0.0, "lib": 0.0, "other": 0.0})

    for link in crosswalk:
        src = by_2015.get(link["ed_2015"])
        if not src:
            print(f"  WARN: crosswalk 2015 ED not in results: {link['ed_2015']}")
            continue
        w = link["weight"]
        dst = link["ed_2019"]
        accum[dst]["ndp"] += src["ndp"] * w
        accum[dst]["ucp"] += src["ucp_equiv"] * w
        accum[dst]["lib"] += src["lib"] * w
        accum[dst]["other"] += src["other"] * w

    out = []
    for ed, vals in accum.items():
        ndp = int(round(vals["ndp"]))
        ucp = int(round(vals["ucp"]))
        lib = int(round(vals["lib"]))
        other = int(round(vals["other"]))
        out.append({
            "ed": ed,
            "region": region_from_2019_name(ed),
            "ndp": ndp,
            "ucp": ucp,
            "lib": lib,
            "other": other,
        })
    return out


# ---------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------

def rural_two_party_share(districts: list) -> float:
    rural = [d for d in districts if d["region"] == "Rest of Alberta"]
    tn = sum(d["ndp"] for d in rural)
    tu = sum(d["ucp"] for d in rural)
    return tn / (tn + tu) if (tn + tu) else 0.0


def main():
    print("=" * 70)
    print("  2015-Votes Cross-Election Analysis (v0.1)")
    print("  Third data point in direction-stability test (2015 / 2019 / 2023)")
    print("=" * 70)

    votes_2015 = load_2015_results()
    crosswalk = load_crosswalk()
    print(f"\n  Loaded {len(votes_2015)} pre-2017 EDs with 2015 results")
    print(f"  Loaded {len(crosswalk)} crosswalk links")

    # Confidence summary
    conf_counts = defaultdict(int)
    for c in crosswalk:
        conf_counts[c["confidence"]] += 1
    print(f"  Confidence: high={conf_counts['high']}, medium={conf_counts['medium']}, low={conf_counts['low']}")

    # Attribute to 2019 boundaries
    dists_2015_on_2019 = attribute_2015_to_2019(votes_2015, crosswalk)
    print(f"\n  Attributed to {len(dists_2015_on_2019)} 2019-boundary EDs")

    # Sanity: total votes conservation
    tot_2015 = sum(r["ndp"] + r["ucp_equiv"] + r["lib"] + r["other"] for r in votes_2015)
    tot_attributed = sum(d["ndp"] + d["ucp"] + d["lib"] + d["other"] for d in dists_2015_on_2019)
    print(f"  Conservation check: 2015 total={tot_2015:,}  attributed total={tot_attributed:,}  "
          f"delta={tot_attributed-tot_2015:+d}")

    # NDP two-party vs UCP-equiv
    tn = sum(d["ndp"] for d in dists_2015_on_2019)
    tu = sum(d["ndp"] + d["ucp"] for d in dists_2015_on_2019)
    print(f"  2015 NDP two-party (on 2019 boundaries): {tn/tu*100:.2f}%")

    # Rural baseline
    rural_ndp_2015 = rural_two_party_share(dists_2015_on_2019)
    print(f"  2015 rural NDP two-party: {rural_ndp_2015*100:.2f}%")

    # ------- 2019 map, 2015 votes -------
    m_2019 = compute_metrics(
        dists_2015_on_2019,
        "2019 MAP under 2015 VOTE ATTRIBUTION",
    )

    # ------- Majority 2026, 2015 votes -------
    maj_2015 = estimate_2026(dists_2015_on_2019, MAJORITY_2026_MAPPING, rural_ndp_2015)
    # Validate
    if len(maj_2015) != 89:
        print(f"  WARN: Majority 2026 estimate has {len(maj_2015)} EDs, expected 89")
    m_maj = compute_metrics(maj_2015, "MAJORITY 2026 under 2015 VOTE ATTRIBUTION")

    # ------- Minority 2026, 2015 votes -------
    min_2015 = estimate_2026(dists_2015_on_2019, MINORITY_2026_MAPPING, rural_ndp_2015)
    if len(min_2015) != 89:
        print(f"  WARN: Minority 2026 estimate has {len(min_2015)} EDs, expected 89")
    m_min = compute_metrics(min_2015, "MINORITY 2026 under 2015 VOTE ATTRIBUTION")

    # ------- 3-map comparison -------
    print("\n" + "=" * 70)
    print("  2015-VOTE three-map comparison")
    print("=" * 70)
    print(f"  Metric              | 2019    | Majority | Minority")
    print(f"  Districts            | {m_2019['n']:>7d} | {m_maj['n']:>8d} | {m_min['n']:>8d}")
    print(f"  Actual seats NDP/UCP | {m_2019['ndp_seats']}/{m_2019['ucp_seats']:<2d} | "
          f"{m_maj['ndp_seats']}/{m_maj['ucp_seats']:<2d}   | {m_min['ndp_seats']}/{m_min['ucp_seats']:<2d}")
    print(f"  B2 Efficiency gap    | {m_2019['eg']*100:+6.2f}% | {m_maj['eg']*100:+7.2f}% | {m_min['eg']*100:+7.2f}%")
    print(f"  B3 Mean-median       | {m_2019['mm_gap']*100:+6.2f}pp| {m_maj['mm_gap']*100:+7.2f}pp| {m_min['mm_gap']*100:+7.2f}pp")
    print(f"  B4 NDP @ 50/50       | {m_2019['ndp_at_50']:>7d} | {m_maj['ndp_at_50']:>8d} | {m_min['ndp_at_50']:>8d}")
    print(f"  B6 Declination       | {m_2019['declination']:+7.4f} | {m_maj['declination']:+8.4f} | {m_min['declination']:+8.4f}")

    # Asymmetry
    asym_eg = (m_min["eg"] - m_maj["eg"]) * 100
    asym_mm = (m_min["mm_gap"] - m_maj["mm_gap"]) * 100
    asym_b4 = m_min["ndp_at_50"] - m_maj["ndp_at_50"]
    asym_dec = m_min["declination"] - m_maj["declination"]
    print()
    print("  Minority-Majority asymmetry under 2015 votes:")
    print(f"    EG:          {asym_eg:+.2f} pp")
    print(f"    Mean-median: {asym_mm:+.2f} pp")
    print(f"    B4 seats:    {asym_b4:+d} seats at 50/50")
    print(f"    Declination: {asym_dec:+.4f}")

    # Save result summary to CSV for downstream comparison
    out_path = DATA / "v0_1_2015_cross_election_summary.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["map", "n", "ndp_seats", "ucp_seats", "eg_pct",
                    "mm_gap_pp", "ndp_at_50", "ucp_at_50", "declination",
                    "prov_ndp_pct"])
        for label, m in [("2019", m_2019), ("Majority 2026", m_maj),
                         ("Minority 2026", m_min)]:
            w.writerow([label, m["n"], m["ndp_seats"], m["ucp_seats"],
                        m["eg"] * 100, m["mm_gap"] * 100,
                        m["ndp_at_50"], m["ucp_at_50"],
                        m["declination"], m["prov_ndp"] * 100])
    print(f"\n  Wrote summary to {out_path}")

    # ------- Three-election direction-stability table -------
    # 2015 asym_eg just computed. Pull 2019 and 2023 asymmetries from the
    # existing analyses (we re-compute them here to produce a clean table).
    print("\n" + "=" * 70)
    print("  Cross-election direction-stability (minority - majority EG asymmetry)")
    print("=" * 70)

    # 2019 votes
    from v0_3_monte_carlo_ci import cross_check_2019_votes  # noqa: F401
    # Inline the 2019-vote computation to avoid re-printing.
    dists_2019_votes = _load_2019_votes()
    rural_2019 = rural_two_party_share(dists_2019_votes)
    maj_2019 = estimate_2026(dists_2019_votes, MAJORITY_2026_MAPPING, rural_2019)
    min_2019 = estimate_2026(dists_2019_votes, MINORITY_2026_MAPPING, rural_2019)
    m_2019v_maj = compute_metrics(maj_2019, "maj 2019", verbose=False)
    m_2019v_min = compute_metrics(min_2019, "min 2019", verbose=False)
    asym_2019 = (m_2019v_min["eg"] - m_2019v_maj["eg"]) * 100

    # 2023 votes (load from the existing 2023 results)
    from v0_2_packing_cracking_analysis import load_2023_results
    dists_2023 = load_2023_results()
    rural_2023 = rural_two_party_share(dists_2023)
    maj_2023 = estimate_2026(dists_2023, MAJORITY_2026_MAPPING, rural_2023)
    min_2023 = estimate_2026(dists_2023, MINORITY_2026_MAPPING, rural_2023)
    m_2023_maj = compute_metrics(maj_2023, "maj 2023", verbose=False)
    m_2023_min = compute_metrics(min_2023, "min 2023", verbose=False)
    asym_2023 = (m_2023_min["eg"] - m_2023_maj["eg"]) * 100

    print(f"  Election  | Maj EG   | Min EG   | Asymmetry (Min-Maj)")
    print(f"  2015      | {m_maj['eg']*100:+6.2f}% | {m_min['eg']*100:+6.2f}% | {asym_eg:+6.2f} pp")
    print(f"  2019      | {m_2019v_maj['eg']*100:+6.2f}% | {m_2019v_min['eg']*100:+6.2f}% | {asym_2019:+6.2f} pp")
    print(f"  2023      | {m_2023_maj['eg']*100:+6.2f}% | {m_2023_min['eg']*100:+6.2f}% | {asym_2023:+6.2f} pp")

    # Direction verdict
    # Sign convention, per compute_metrics formula in v0_2:
    #   EG = (ndp_wasted - ucp_wasted) / total
    #   POSITIVE EG means NDP wastes more votes -> pro-UCP bias
    #   NEGATIVE EG means UCP wastes more votes -> pro-NDP bias
    # Therefore (min_EG - maj_EG):
    #   POSITIVE asymmetry = minority MORE pro-UCP than majority
    #   NEGATIVE asymmetry = minority LESS pro-UCP (more pro-NDP) than majority
    # N.B.: analysis/scripts/v0_3_monte_carlo_ci.py lines 158-159 print inverted
    # labels and should be re-worded in a follow-up.
    signs = [asym_eg, asym_2019, asym_2023]
    same_sign_neg = all(s < 0 for s in signs)
    same_sign_pos = all(s > 0 for s in signs)
    print()
    if same_sign_pos:
        print("  DIRECTION: All three elections produce POSITIVE asymmetry")
        print("             (minority MORE pro-UCP than majority).")
        print("             Direction claim passes RT3 strongly (3/3).")
    elif same_sign_neg:
        print("  DIRECTION: All three elections produce NEGATIVE asymmetry")
        print("             (minority LESS pro-UCP / more pro-NDP than majority).")
        print("             Direction claim reversed (3/3 in opposite direction).")
    else:
        pos_count = sum(1 for s in signs if s > 0)
        neg_count = sum(1 for s in signs if s < 0)
        print(f"  DIRECTION: Mixed. {pos_count} positive (minority MORE pro-UCP),")
        print(f"             {neg_count} negative (minority LESS pro-UCP).")
        if pos_count == 2 or neg_count == 2:
            print("             Qualified pass on RT3 (2/3 agree).")
        else:
            print("             No dominant direction. RT3 fails; direction is")
            print("             contingent on electorate conditions.")

    # Save cross-election summary
    xe_path = DATA / "v0_1_cross_election_asymmetry_3way.csv"
    with open(xe_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["election", "maj_eg_pct", "min_eg_pct",
                    "asymmetry_pp", "maj_mm_pp", "min_mm_pp",
                    "maj_ndp50", "min_ndp50",
                    "maj_declination", "min_declination"])
        w.writerow(["2015",
                    m_maj["eg"] * 100, m_min["eg"] * 100, asym_eg,
                    m_maj["mm_gap"] * 100, m_min["mm_gap"] * 100,
                    m_maj["ndp_at_50"], m_min["ndp_at_50"],
                    m_maj["declination"], m_min["declination"]])
        w.writerow(["2019",
                    m_2019v_maj["eg"] * 100, m_2019v_min["eg"] * 100, asym_2019,
                    m_2019v_maj["mm_gap"] * 100, m_2019v_min["mm_gap"] * 100,
                    m_2019v_maj["ndp_at_50"], m_2019v_min["ndp_at_50"],
                    m_2019v_maj["declination"], m_2019v_min["declination"]])
        w.writerow(["2023",
                    m_2023_maj["eg"] * 100, m_2023_min["eg"] * 100, asym_2023,
                    m_2023_maj["mm_gap"] * 100, m_2023_min["mm_gap"] * 100,
                    m_2023_maj["ndp_at_50"], m_2023_min["ndp_at_50"],
                    m_2023_maj["declination"], m_2023_min["declination"]])
    print(f"  Wrote three-election asymmetry table to {xe_path}")


def _load_2019_votes() -> list:
    """Load 2019 per-ED NDP/UCP totals. Lifted from v0_3_monte_carlo_ci."""
    path = DATA / "v0_1_alberta_2019_results.csv"
    out = []
    with open(path) as f:
        for r in csv.DictReader(f):
            ndp = ucp = 0
            for i in range(1, 9):
                cand = r.get(f"cand_{i}", "") or ""
                votes_s = r.get(f"votes_{i}", "") or ""
                if not cand or not votes_s:
                    continue
                try:
                    v = int(votes_s)
                except ValueError:
                    continue
                if cand.endswith("(NDP)"):
                    ndp = v
                elif cand.endswith("(UCP)"):
                    ucp = v
            if ndp + ucp == 0:
                continue
            out.append({
                "ed": r["ed_name"],
                "region": r.get("region", "Rest of Alberta"),
                "ndp": ndp,
                "ucp": ucp,
            })
    return out


if __name__ == "__main__":
    main()
