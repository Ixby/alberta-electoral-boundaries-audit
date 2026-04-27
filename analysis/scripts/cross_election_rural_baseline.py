"""
Cross-election rural NDP baseline analysis (2015, 2019, 2023).

Answers: how stable is the rural NDP share across elections? The audit's
70/30 blend uses the 2023 observed rural share (33.5%) as the rural
baseline for hybrid districts. Monte Carlo sensitivity (v0_3) sampled
rural_ndp_share ~ Uniform(0.28, 0.38). This script tests whether that
range is realistic by reporting the observed rural share across three
elections with different political conditions.

Boundary caveat: 2015 EDs used pre-2017-commission boundaries; 2019 and
2023 used the current 87 EDs. The 2015 'Rest of Alberta' classification
here is made by ED-name heuristic (Calgary-*, Edmonton-*, else rural),
which closely matches the actual 2015 regional split but is not
boundary-accurate.

Output: prints rural NDP share for each of the three elections, plus
the implied Monte Carlo sampling range to cover realistic variation.
"""
# Version: 0.1 series  (last updated 2026-04-26)

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"


def region_from_name(ed_name: str) -> str:
    n = ed_name.strip()
    if n.lower().startswith("calgary"):
        return "Calgary"
    if n.lower().startswith("edmonton"):
        return "Edmonton"
    return "Rest of Alberta"


def load_2023() -> list:
    out = []
    with open(DATA / "alberta_2023_results.csv") as f:
        for r in csv.DictReader(f):
            ndp = ucp = 0
            for i in range(1, 7):
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
            out.append({"region": r.get("region", "Rest of Alberta"),
                        "ndp": ndp, "ucp_equiv": ucp})
    return out


def load_2019() -> list:
    out = []
    with open(DATA / "alberta_2019_results.csv") as f:
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
            out.append({"region": r.get("region", "Rest of Alberta"),
                        "ndp": ndp, "ucp_equiv": ucp})
    return out


def load_2015() -> list:
    out = []
    with open(DATA / "alberta_2015_results.csv") as f:
        for r in csv.DictReader(f):
            ndp = int(r["ndp"])
            ucp_equiv = int(r["ucp_equiv"])
            if ndp + ucp_equiv == 0:
                continue
            out.append({"region": region_from_name(r["ed_2015"]),
                        "ndp": ndp, "ucp_equiv": ucp_equiv})
    return out


def rural_two_party_share(records: list) -> dict:
    rural = [r for r in records if r["region"] == "Rest of Alberta"]
    total_ndp = sum(r["ndp"] for r in rural)
    total_ucp = sum(r["ucp_equiv"] for r in rural)
    two_party = total_ndp + total_ucp
    return {
        "n_eds": len(rural),
        "total_ndp": total_ndp,
        "total_ucp_equiv": total_ucp,
        "two_party_total": two_party,
        "ndp_share": total_ndp / two_party if two_party else 0.0,
    }


def main():
    print("=" * 70)
    print("  Rural NDP two-party share across three elections")
    print("=" * 70)

    elections = [
        ("2015", load_2015, "NDP wave (Notley majority); UCP = PC+WRP"),
        ("2019", load_2019, "UCP first post-merger; Kenney majority"),
        ("2023", load_2023, "UCP re-election; Smith majority"),
    ]

    results = {}
    for year, loader, desc in elections:
        recs = loader()
        stats = rural_two_party_share(recs)
        results[year] = stats
        print(f"\n  {year}: {desc}")
        print(f"    Rural EDs: {stats['n_eds']}")
        print(f"    Rural NDP two-party: {stats['ndp_share']*100:.2f}%")
        print(f"    Rural NDP total votes: {stats['total_ndp']:,}")
        print(f"    Rural UCP-equiv votes: {stats['total_ucp_equiv']:,}")

    # Range across elections
    shares = [results[y]["ndp_share"] for y in ["2015", "2019", "2023"]]
    print("\n" + "=" * 70)
    print("  Cross-election range")
    print("=" * 70)
    print(f"  Min rural NDP share: {min(shares)*100:.2f}% ({['2015','2019','2023'][shares.index(min(shares))]})")
    print(f"  Max rural NDP share: {max(shares)*100:.2f}% ({['2015','2019','2023'][shares.index(max(shares))]})")
    print(f"  Range: {(max(shares)-min(shares))*100:.2f} pp")
    print()
    print("  Monte Carlo implication:")
    print(f"    v0.3 sampled rural_ndp_share ~ Uniform(0.28, 0.38) — 10 pp range")
    print(f"    Observed 2015-2023 range: {min(shares)*100:.1f}% to {max(shares)*100:.1f}%")
    if max(shares) > 0.40 or min(shares) < 0.25:
        print(f"    FLAG: observed range exceeds Monte Carlo sampling range.")
        print(f"    Sensitivity analysis should widen to Uniform(0.20, 0.55) to")
        print(f"    cover realistic rural political variation. Expected effect:")
        print(f"    wider CI on minority-majority EG asymmetry.")
    else:
        print(f"    Monte Carlo range roughly matches observed variation.")


if __name__ == "__main__":
    main()
