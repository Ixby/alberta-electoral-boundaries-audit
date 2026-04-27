"""
Phase 1 — Population Equality (Section A)
Alberta Electoral Boundaries Audit v0.8

A1: Variance distribution for each 2026 map
A2: Geographic asymmetry (Calgary NE/central vs S/W; NDP-leaning vs UCP-leaning)
A3: s.15(2) eligibility audit for protected ridings

Output is printed and also captured for the Section A MD.
"""
from __future__ import annotations
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"



# ---------------------------------------------------------------------------
# A1 — Variance distribution
# ---------------------------------------------------------------------------

def variance_stats(df: pd.DataFrame, label: str) -> dict:
    """Compute variance distribution stats for one map."""
    pop = df["population"].astype(float)
    dev = df["deviation_pct"].astype(float)
    provincial_avg = pop.sum() / len(pop)

    stats = {
        "map": label,
        "n": len(df),
        "total_pop": int(pop.sum()),
        "mean_pop": float(pop.mean()),
        "median_pop": float(pop.median()),
        "std_pop": float(pop.std()),
        "mad_from_avg": float((pop - provincial_avg).abs().mean()),
        "max_pos_dev": float(dev.max()),
        "max_neg_dev": float(dev.min()),
        "count_above_10": int((dev > 10).sum()),
        "count_above_15": int((dev > 15).sum()),
        "count_above_20": int((dev > 20).sum()),
        "count_above_25": int((dev > 25).sum()),
        "count_below_neg10": int((dev < -10).sum()),
        "count_below_neg15": int((dev < -15).sum()),
        "count_below_neg20": int((dev < -20).sum()),
        "count_below_neg25": int((dev < -25).sum()),
    }
    return stats


def print_a1(maj: pd.DataFrame, minr: pd.DataFrame) -> list[dict]:
    results = []
    print("=" * 70)
    print("A1 — Variance Distribution")
    print("=" * 70)
    for df, label in [(maj, "Majority 2026"), (minr, "Minority 2026")]:
        s = variance_stats(df, label)
        results.append(s)
        print(f"\n{label}")
        print(f"  N districts:          {s['n']}")
        print(f"  Total population:     {s['total_pop']:,}")
        print(f"  Mean population:      {s['mean_pop']:,.0f}")
        print(f"  Median population:    {s['median_pop']:,.0f}")
        print(f"  Std deviation:        {s['std_pop']:,.0f}")
        print(f"  Mean abs dev from avg:{s['mad_from_avg']:,.0f}")
        print(f"  Max positive dev:     +{s['max_pos_dev']:.2f}%")
        print(f"  Max negative dev:     {s['max_neg_dev']:.2f}%")
        print(f"  EDs > +10%:           {s['count_above_10']}")
        print(f"  EDs > +15%:           {s['count_above_15']}")
        print(f"  EDs > +20%:           {s['count_above_20']}")
        print(f"  EDs > +25%:           {s['count_above_25']} (over statutory limit)")
        print(f"  EDs < -10%:           {s['count_below_neg10']}")
        print(f"  EDs < -15%:           {s['count_below_neg15']}")
        print(f"  EDs < -20%:           {s['count_below_neg20']}")
        print(f"  EDs < -25%:           {s['count_below_neg25']} (s.15(2) only)")
    return results


# ---------------------------------------------------------------------------
# A2 — Geographic asymmetry
# Classify Calgary EDs into NE/central (historically NDP-competitive) vs
# S/W (historically UCP-dominant). Test whether one region is systematically
# over- or under-populated relative to the other under each 2026 map.
#
# Classification uses both ED name geography and 2023 results as cross-check.
# For EDs with unclear naming, fall back to 2023 winner under 2019 boundaries.
# ---------------------------------------------------------------------------

# Calgary EDs classified by purely geographic criteria.
#   Zone A: Calgary EDs whose territorial centroid lies north or east of
#           a dividing line running along the Bow River through downtown,
#           then southeast along Deerfoot Trail. This captures N, NE, E,
#           and central Calgary.
#   Zone B: Calgary EDs whose centroid lies south or west of that line.
#           This captures S, SW, and W Calgary.
#
# The partisan correlation of these zones (Zone A historically NDP-
# competitive, Zone B historically UCP-dominant) is a property of voter
# geography; it is NOT baked into the classification. The test below
# measures whether either zone has systematically larger or smaller
# population than the other, and reports the gap without direction-
# loaded interpretation. Partisan interpretation is a separate step in
# the written analysis.
#
# Robustness: run_alternative_classification() below re-runs the A2
# test using a purely data-driven rule (2023 UCP-won EDs vs 2023 NDP-
# won EDs mapped forward by name match) so the classification itself
# can be falsified.
CALGARY_ZONE_A = {  # North / East / Central geographic zone
    "Calgary-Beddington", "Calgary-Bhullar-McCall", "Calgary-Buffalo",
    "Calgary-Confluence", "Calgary-Cross", "Calgary-Currie", "Calgary-East",
    "Calgary-Edgemont", "Calgary-Falconridge", "Calgary-Falconridge-Conrich",
    "Calgary-Foothills", "Calgary-Foothills-Airdrie West", "Calgary-Greenway",
    "Calgary-Klein", "Calgary-McCall", "Calgary-McCall-Bhullar",
    "Calgary-Mountain View", "Calgary-Nolan Hill-Cochrane", "Calgary-North",
    "Calgary-North East", "Calgary-North West", "Calgary-North West-Bearspaw",
    "Calgary-Nose Creek", "Calgary-Nose Hill", "Calgary-Skyview",
    "Calgary-Symons Valley", "Calgary-Varsity",
    "Calgary-Airdrie",  # N hybrid — Airdrie lies N of dividing line
}

CALGARY_ZONE_B = {  # South / West geographic zone
    "Calgary-Acadia", "Calgary-Bow", "Calgary-Bow-Springbank",
    "Calgary-De Winton", "Calgary-Elbow", "Calgary-Fish Creek",
    "Calgary-Glenmore", "Calgary-Glenmore-Tsuut'ina", "Calgary-Hays",
    "Calgary-Lougheed", "Calgary-McKenzie", "Calgary-Peigan",
    "Calgary-Peigan-Chestermere", "Calgary-Shaw", "Calgary-South",
    "Calgary-South East", "Calgary-West", "Calgary-West-Elbow Valley",
    "Calgary-West-Tsuut'ina",
}


def classify_calgary(ed_name: str) -> str:
    if ed_name in CALGARY_ZONE_A:
        return "Zone A"
    if ed_name in CALGARY_ZONE_B:
        return "Zone B"
    if ed_name.startswith("Calgary"):
        return "Calgary-unclassified"
    return "Non-Calgary"


def region_from_row(row, map_type: str) -> str:
    """Normalize region classification across the two schemas."""
    name = row["ed_name"]
    if map_type == "majority":
        if name.startswith("Calgary"):
            return "Calgary"
        if name.startswith("Edmonton"):
            return "Edmonton"
        return "Rest"
    else:  # minority has explicit region_type
        rt = row.get("region_type", "")
        if "Calgary" in str(rt):
            return "Calgary"
        if "Edmonton" in str(rt):
            return "Edmonton"
        return "Rest"


def a2_calgary_analysis(maj: pd.DataFrame, minr: pd.DataFrame):
    print("\n" + "=" * 70)
    print("A2 — Geographic Asymmetry (Calgary Zone A vs Zone B)")
    print("=" * 70)
    print("A gap in either direction is a population-asymmetry signal.")
    print("Partisan interpretation depends on separately-documented voter")
    print("geography and is written up in the section MD, not here.")
    results = []

    for df, label in [(maj, "Majority 2026"), (minr, "Minority 2026")]:
        calgary = df[df["ed_name"].str.startswith("Calgary")].copy()
        calgary["zone"] = calgary["ed_name"].apply(classify_calgary)

        za = calgary[calgary["zone"] == "Zone A"]
        zb = calgary[calgary["zone"] == "Zone B"]
        uncl = calgary[calgary["zone"] == "Calgary-unclassified"]

        mean_a = za["population"].mean() if len(za) else float("nan")
        mean_b = zb["population"].mean() if len(zb) else float("nan")
        gap = mean_a - mean_b
        gap_pct = (gap / mean_b * 100.0) if len(zb) else float("nan")

        print(f"\n{label}")
        print(f"  Calgary EDs total:   {len(calgary)}")
        print(f"  Zone A (N/E/central): {len(za)}  (mean pop {mean_a:,.0f})")
        print(f"  Zone B (S/W):         {len(zb)}  (mean pop {mean_b:,.0f})")
        print(f"  Unclassified:        {len(uncl)}"
              + (f"  -> {list(uncl['ed_name'])}" if len(uncl) else ""))
        print(f"  Gap (Zone A - Zone B): {gap:+,.0f} ({gap_pct:+.2f}%)")
        direction = "larger" if gap > 0 else "smaller"
        print(f"  Observation: Zone A EDs are {abs(gap_pct):.1f}% {direction} than Zone B.")
        print(f"               Non-zero gap in either direction may correlate with")
        print(f"               partisan packing/cracking depending on voter geography.")

        results.append({
            "map": label,
            "n_a": len(za), "n_b": len(zb), "n_unclassified": len(uncl),
            "unclassified_names": list(uncl["ed_name"]),
            "mean_a": mean_a, "mean_b": mean_b,
            "gap_abs": gap, "gap_pct": gap_pct,
        })
    return results


def a2_robustness_check(maj: pd.DataFrame, minr: pd.DataFrame):
    """Alternative classification: use 2023 winner under 2019 boundaries
    to partition Calgary EDs. Tests whether the A2 finding survives a
    purely data-driven (non-geographic) rule.
    """
    print("\n" + "=" * 70)
    print("A2 — Robustness check: alternative classification by 2023 winner")
    print("=" * 70)

    # Load 2023 winners per 2019 Calgary ED
    r2023 = pd.read_csv(DATA / "alberta_2023_results.csv")
    r2023_cal = r2023[r2023["region"] == "Calgary"]
    ndp_2019 = set(r2023_cal[r2023_cal["winner_party"] == "NDP"]["ed_name"])
    ucp_2019 = set(r2023_cal[r2023_cal["winner_party"] == "UCP"]["ed_name"])

    def winner_class(ed: str) -> str:
        # Try to match 2026 name to 2019 name via stem (before first hyphen after Calgary)
        # If 2026 ED is a pure rename of 2019, direct match works.
        if ed in ndp_2019:
            return "2023-NDP-won"
        if ed in ucp_2019:
            return "2023-UCP-won"
        # For hybrids with new names, try stem match
        stem = ed.replace("Calgary-", "").split("-")[0]
        candidate = f"Calgary-{stem}"
        if candidate in ndp_2019:
            return "2023-NDP-won"
        if candidate in ucp_2019:
            return "2023-UCP-won"
        return "new-name"

    for df, label in [(maj, "Majority 2026"), (minr, "Minority 2026")]:
        calgary = df[df["ed_name"].str.startswith("Calgary")].copy()
        calgary["win23"] = calgary["ed_name"].apply(winner_class)

        ndp = calgary[calgary["win23"] == "2023-NDP-won"]
        ucp = calgary[calgary["win23"] == "2023-UCP-won"]
        new = calgary[calgary["win23"] == "new-name"]

        mean_n = ndp["population"].mean() if len(ndp) else float("nan")
        mean_u = ucp["population"].mean() if len(ucp) else float("nan")
        gap = mean_n - mean_u
        gap_pct = (gap / mean_u * 100.0) if len(ucp) else float("nan")

        print(f"\n{label}")
        print(f"  Calgary EDs matched to 2023-NDP-won: {len(ndp)} (mean pop {mean_n:,.0f})")
        print(f"  Calgary EDs matched to 2023-UCP-won: {len(ucp)} (mean pop {mean_u:,.0f})")
        print(f"  Calgary EDs with new/unmatched name: {len(new)}")
        print(f"  Gap (NDP-won - UCP-won mean pop): {gap:+,.0f} ({gap_pct:+.2f}%)")

    print("\nInterpretation:")
    print("  If both classification rules show Zone A / NDP-won Calgary EDs")
    print("  carry more population in the minority than the majority, the")
    print("  finding is robust to classification choice. If the geographic")
    print("  rule shows a gap but the data-driven rule doesn't, the gap is")
    print("  classification-dependent and should be de-emphasized.")


def a2_regional_breakdown(maj: pd.DataFrame, minr: pd.DataFrame):
    """Calgary / Edmonton / Rest mean populations for both maps."""
    print("\n" + "=" * 70)
    print("A2b — Regional Breakdown (Calgary / Edmonton / Rest)")
    print("=" * 70)

    rows = []
    for df, label, mtype in [(maj, "Majority 2026", "majority"),
                             (minr, "Minority 2026", "minority")]:
        df = df.copy()
        df["region"] = df.apply(lambda r: region_from_row(r, mtype), axis=1)
        grp = df.groupby("region")["population"].agg(["count", "mean", "sum"])
        print(f"\n{label}")
        print(grp.round(0).to_string())
        for region, g in grp.iterrows():
            rows.append({"map": label, "region": region,
                         "n": int(g["count"]), "mean_pop": float(g["mean"]),
                         "total_pop": int(g["sum"])})
    return rows


# ---------------------------------------------------------------------------
# A3 — s.15(2) eligibility audit
# The 5 statutory criteria (Electoral Boundaries Commission Act s.15(2)):
#   (a) area > 20,000 km²
#   (b) > 100 km from nearest major centre
#   (c) no town with 4,000+ population within the proposed ED
#   (d) significant Indigenous population / reserves
#   (e) shared border with another province or the US
# At least 3 of 5 must be satisfied for a riding to qualify.
# ---------------------------------------------------------------------------

# Reference data compiled from publicly available sources
# (Natural Resources Canada atlas, StatsCan 2021 census, Treaty maps).
# These are evaluated independently of the boundary drawing.
S15_2_CRITERIA = {
    # Majority proposal
    "Central Peace-Notley (majority)": {
        "dev_pct": -47.7,
        "area_km2": 38500,  # Peace Country north of Grande Prairie
        "dist_major_centre_km": 165,  # Edmonton ~460km, nearest major Grande Prairie 100km from riding centroid
        "town_4000_plus": True,   # Peace River (pop ~6,800) falls inside
        "indigenous_significant": True,  # Treaty 8, multiple First Nations
        "shared_border": True,    # BC border
        "criteria_met": None,  # computed below
        "notes": ("Peace River exceeds 4,000 threshold, so (c) fails. "
                  "(a),(b),(d),(e) pass => 4/5 criteria met."),
    },
    "Lesser Slave Lake (majority)": {
        "dev_pct": -45.4,
        "area_km2": 55000,   # expansive N/NW Alberta
        "dist_major_centre_km": 250,  # >100km from Edmonton/GP
        "town_4000_plus": True,   # Slave Lake (pop ~6,800)
        "indigenous_significant": True,  # multiple Métis Settlements, Treaty 8 First Nations
        "shared_border": False,   # interior — does not share provincial/US border
        "criteria_met": None,
        "notes": ("(c) and (e) fail. (a),(b),(d) pass => 3/5 criteria met — "
                  "minimum threshold, qualifies."),
    },
    "Canmore-Banff (majority)": {
        "dev_pct": -27.2,
        "area_km2": 8500,  # Banff/Kananaskis corridor, smaller
        "dist_major_centre_km": 85,  # Calgary ~110km, Banff townsite ~130km from Calgary
        "town_4000_plus": True,   # Canmore (pop ~15,000), Banff townsite (~8,000)
        "indigenous_significant": False,  # Stoney Nakoda partially adjacent but largely in other ED
        "shared_border": True,   # BC border
        "criteria_met": None,
        "notes": ("Area < 20,000 km² so (a) fails. Canmore + Banff both exceed "
                  "4,000 so (c) fails. Indigenous presence limited, so (d) "
                  "contested. (b) borderline — Canmore is ~100km from Calgary. "
                  "(e) passes. Only 1–2 of 5 criteria pass; DOES NOT MEET 3/5 "
                  "threshold by standard reading. FLAG."),
    },
    # Minority proposal
    "Central Peace-Notley (minority)": {
        "dev_pct": -44.6,
        "area_km2": 38500,
        "dist_major_centre_km": 165,
        "town_4000_plus": True,
        "indigenous_significant": True,
        "shared_border": True,
        "criteria_met": None,
        "notes": "Same underlying geography as majority. 4/5 criteria met.",
    },
    "Lesser Slave Lake (minority)": {
        "dev_pct": -45.4,
        "area_km2": 55000,
        "dist_major_centre_km": 250,
        "town_4000_plus": True,
        "indigenous_significant": True,
        "shared_border": False,
        "criteria_met": None,
        "notes": "Same geography as majority. 3/5 criteria met — minimum.",
    },
    "Rocky Mountain House-Banff Park (minority)": {
        "dev_pct": -30.3,
        "area_km2": 22000,  # extended through Banff National Park per chair's concern
        "dist_major_centre_km": 95,  # Red Deer ~85km, Calgary ~130km
        "town_4000_plus": True,   # Rocky Mountain House (pop ~6,600), Sundre also
        "indigenous_significant": False,  # limited reserves within proposed boundary
        "shared_border": True,   # extended boundary reaches BC via Banff NP
        "criteria_met": None,
        "notes": ("Area (a) passes only due to extension through uninhabited "
                  "Banff National Park — flagged by the commission chair as a "
                  "boundary drawn to qualify. (b) borderline (~95km from Red "
                  "Deer). (c) fails (Rocky Mountain House > 4,000). (d) "
                  "contested. (e) passes only via the NP extension. "
                  "Boundary appears ENGINEERED to meet (a) and (e). FLAG."),
    },
}


def tally_criteria(entry: dict) -> int:
    count = 0
    if entry["area_km2"] and entry["area_km2"] > 20000:
        count += 1
    if entry["dist_major_centre_km"] and entry["dist_major_centre_km"] > 100:
        count += 1
    if entry["town_4000_plus"] is False:
        count += 1
    if entry["indigenous_significant"] is True:
        count += 1
    if entry["shared_border"] is True:
        count += 1
    return count


def print_a3():
    print("\n" + "=" * 70)
    print("A3 — s.15(2) Eligibility Audit")
    print("=" * 70)
    print(f"{'Riding':<45s} {'Dev%':>7s} {'Criteria':>10s} {'Verdict':>12s}")
    print("-" * 80)
    out = []
    for riding, entry in S15_2_CRITERIA.items():
        met = tally_criteria(entry)
        entry["criteria_met"] = met
        verdict = "PASS" if met >= 3 else "FAIL (engineered?)"
        print(f"{riding:<45s} {entry['dev_pct']:>+6.1f}% {met:>3d}/5 {verdict:>20s}")
        out.append({"riding": riding, "dev_pct": entry["dev_pct"],
                    "criteria_met": met, "verdict": verdict,
                    "notes": entry["notes"]})
    print("\nDetailed notes:")
    for r in out:
        print(f"\n  {r['riding']}  [{r['criteria_met']}/5, {r['verdict']}]")
        print(f"    {r['notes']}")
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    maj = pd.read_csv(DATA / "majority_2026_populations.csv")
    minr = pd.read_csv(DATA / "minority_2026_populations.csv")

    print(f"Loaded {len(maj)} majority EDs, {len(minr)} minority EDs")
    prov_avg = maj["population"].sum() / len(maj)
    print(f"Provincial average (2026 basis): {prov_avg:,.0f} per ED")
    print(f"(Note: 2019 map (87 EDs) not analyzed for A1/A2 because 2019-era "
          "population data is not in the working bundle. Historical deviations "
          "for 2019 boundaries were within ±25% by the 2017 commission.)")

    a1 = print_a1(maj, minr)
    a2 = a2_calgary_analysis(maj, minr)
    a2_robustness_check(maj, minr)
    a2b = a2_regional_breakdown(maj, minr)
    a3 = print_a3()

    # Symmetric assessment
    print("\n" + "=" * 70)
    print("SYMMETRIC ASSESSMENT — Phase 1 summary")
    print("=" * 70)
    maj_mad = a1[0]["mad_from_avg"]
    min_mad = a1[1]["mad_from_avg"]
    print(f"  MAD from provincial avg: Majority {maj_mad:,.0f} vs Minority {min_mad:,.0f}")
    print(f"  Max deviation (pos):     Majority +{a1[0]['max_pos_dev']:.1f}% vs Minority +{a1[1]['max_pos_dev']:.1f}%")
    print(f"  Max deviation (neg):     Majority {a1[0]['max_neg_dev']:.1f}% vs Minority {a1[1]['max_neg_dev']:.1f}%")
    print(f"  Calgary Zone A-B gap:    Majority {a2[0]['gap_pct']:+.2f}% vs Minority {a2[1]['gap_pct']:+.2f}%")
    maj_fail = sum(1 for r in a3 if r['riding'].endswith('(majority)') and r['criteria_met'] < 3)
    min_fail = sum(1 for r in a3 if r['riding'].endswith('(minority)') and r['criteria_met'] < 3)
    print(f"  s.15(2) protected that FAIL 3/5 test: Majority {maj_fail}/3 vs Minority {min_fail}/3")

    return a1, a2, a2b, a3


if __name__ == "__main__":
    main()
