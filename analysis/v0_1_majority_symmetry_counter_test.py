"""
v0_1 Majority-map symmetry counter-test (Track Q, B3 defence).

Purpose:
  The red-team's attack B3 alleges the audit's tests were constructed around
  observed minority anomalies — Calgary Zone A/B, Airdrie 4-way split, RMH-Banff
  engineered boundary. The defence requires a symmetry-of-test-selection check:
  construct a hypothetical "Zone C vs Zone D" classification in Edmonton and
  apply the same P1-P3 packing criteria to the majority map; run an
  "Airdrie-style 4-way split" test against every city in the majority map to
  see whether the minority-specific pattern has a latent equivalent the audit
  failed to operationalise.

  If the counter-tests reveal nothing above the packing/cracking thresholds
  specified in the v1.2 prompt, the symmetry-of-test-selection claim is
  strengthened. If they reveal something, it is reported and the finding
  is tightened.

Method:
  Test 1 — Edmonton Zone C vs Zone D packing counter-test.
    Classify the majority map's 21 Edmonton EDs into north-of-North
    Saskatchewan River (Zone C) vs south-of-NSR (Zone D) by a simple
    name heuristic (Beverly, Castle Downs, Decore, Manning, Mill Woods
    names pattern north vs. Rutherford, South, Whitemud pattern south).
    Apply P1 (zone mean vs provincial mean, +5% threshold) symmetrically.
    Report any signature.

  Test 2 — City-wide 4-way-split counter-test.
    For every municipality in Alberta with population >= 50,000, count
    the number of 2026 EDs that contain any portion of it under the
    majority map. A count >= 4 is the minority-specific pattern. Apply
    to every city, not only Airdrie. Criterion symmetry: the Airdrie
    test was designed around the minority's 4-way split; this test
    checks whether the majority map also contains a city split across
    >= 4 EDs that the audit did not analyse.

Output:
  data/v0_1_majority_symmetry_counter_test.csv — table of results by test.

Scope:
  This is a counter-test, not a re-analysis. The existing B3 defence
  depends only on whether the majority map contains concealed analogues
  of the patterns the minority was found to exhibit.

Dependencies:
  pandas 2.x, Python 3.14
  data/v0_1_majority_2026_populations.csv
  data/v0_1_minority_2026_populations.csv
  data/v0_1_alberta_2023_results.csv

Author: Sub-agent Track Q for fortification b1_b6.
Date: 2026-04-22
"""

from __future__ import annotations

import csv
import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

PROVINCIAL_MEAN = 54929  # v1.2 prompt and report_academic.md §3 canonical mean
P1_THRESHOLD_PCT = 5.0   # v1.2 prompt P1: zone mean >= provincial mean + 5%
P2_THRESHOLD_PP = 15.0   # v1.2 prompt P2: winning margin >= provincial mean + 15 pp
# C1/C3 joint threshold: a 4-way split is diagnostic only for cities that
# COULD fit within one or two districts at the ±25% statutory band.
# Population 68,661 = provincial mean (54,929) * 1.25 — the statutory maximum
# for a single district. A city above 137,322 (2 quotas) is population-forced
# into >= 3 EDs; a city above 205,983 (3 quotas) is population-forced into
# >= 4 EDs. Calgary, Edmonton are population-forced 4-way splits and so are
# not diagnostic of cracking intent. The Airdrie pattern is diagnostic
# because Airdrie (~84k) fits within 1-2 EDs at the statutory limit.
MAX_POP_FOR_4_ED_CRACKING = 3 * 68661  # 205,983 — cities above this are forced
C1_THRESHOLD_EDS = 4     # minority pattern: community split across >= 4 EDs


# Alberta municipalities with populations >= 50,000 per 2021 census
# (StatsCan 2021 Census profiles). Used to ask whether the majority map
# splits any of them >= 4 ways in the same way the minority splits Airdrie.
CITIES_OVER_50K = {
    "Calgary": 1306784,
    "Edmonton": 1010899,
    "Red Deer": 100844,
    "Lethbridge": 98406,
    "St. Albert": 68232,
    "Medicine Hat": 63271,
    "Grande Prairie": 64141,
    "Airdrie": 74100,  # 2021 census; 2025 est. ~84,000
    "Fort McMurray": 68002,
    "Spruce Grove": 37645,  # below threshold; kept for reference
    "Sherwood Park": 72132,
    "Leduc": 34094,  # below threshold
    "Fort Saskatchewan": 27088,  # below threshold
    "Okotoks": 30214,  # below threshold
}

# For cities with a dedicated 2026 ED name starting with the city name,
# the count of EDs containing that city in each 2026 proposal is readable
# from the ED name list plus hybrid annotations in the rationales and
# crosswalks. For the majority map, we derive the count from ed_name
# prefix matches + known hybrids.


def edmonton_zone_classifier(ed_name: str) -> str:
    """Heuristic classification of Edmonton EDs into north-of-NSR (Zone C)
    vs south-of-NSR (Zone D).

    Reference: Edmonton's North Saskatchewan River bisects the city east-west.
    The classification below is built from published ED-name geography and
    Edmonton Public Library district notes; it is not geopandas-verified.
    A robustness pass with shapefiles is recommended when 2026 polygons
    release; as a counter-test it suffices that the partition is applied
    identically to both 2026 maps.
    """
    # North of the North Saskatchewan River
    zone_c = {
        "Edmonton-Beverly-Clareview",    # NE
        "Edmonton-Castle Downs",          # N
        "Edmonton-Castledowns",           # minority naming variant
        "Edmonton-City Centre",           # straddles, count as north
        "Edmonton-Decore",                # N
        "Edmonton-Glenora-Riverview",     # N (riverside; centroid north)
        "Edmonton-Gold Bar",              # NE
        "Edmonton-Highlands-Norwood",     # NE
        "Edmonton-Manning",               # NE
        "Edmonton-McClung",               # NW
        "Edmonton-Meadows",               # E
        "Edmonton-North West",            # NW
    }
    # South of the North Saskatchewan River
    zone_d = {
        "Edmonton-Beaumont",              # S (hybrid with Beaumont town)
        "Edmonton-Ellerslie",             # S
        "Edmonton-Enoch",                 # SW (majority naming)
        "Edmonton-Enoch-Devon",           # SW (minority naming)
        "Edmonton-Mill Woods",            # SE
        "Edmonton-Rutherford",            # S
        "Edmonton-South",                 # S
        "Edmonton-Spruce Grove",          # W (hybrid; majority has no equivalent)
        "Edmonton-Strathcona",            # S
        "Edmonton-West Henday",           # W / SW
        "Edmonton-Whitemud",              # S
        "Edmonton-Windermere",            # SW
    }
    if ed_name in zone_c:
        return "Zone C"
    if ed_name in zone_d:
        return "Zone D"
    return "Edmonton-unclassified"


def test_1_edmonton_packing(
    maj: pd.DataFrame, minr: pd.DataFrame
) -> list[dict]:
    """Apply P1-style packing test to Edmonton in both 2026 maps.

    Returns list of rows for CSV output. A finding counts as a packing
    signature if zone mean exceeds provincial mean by >= P1_THRESHOLD_PCT.
    """
    results = []
    for df, label in [(maj, "Majority 2026"), (minr, "Minority 2026")]:
        edmonton = df[df["ed_name"].str.startswith("Edmonton")].copy()
        edmonton["zone"] = edmonton["ed_name"].apply(edmonton_zone_classifier)
        zc = edmonton[edmonton["zone"] == "Zone C"]
        zd = edmonton[edmonton["zone"] == "Zone D"]
        uncl = edmonton[edmonton["zone"] == "Edmonton-unclassified"]
        # HIGH-12: fail loudly if any Edmonton ED falls through the
        # hand-curated zone classifier. Silent unclassified rows made
        # the counter-test incomplete — a data refresh that introduced
        # a new Edmonton ED name would previously go unnoticed. The
        # zone dicts above must be updated before this test can run.
        if len(uncl) > 0:
            unclassified_names = uncl["ed_name"].tolist()
            raise ValueError(
                f"HIGH-12: edmonton_zone_classifier missed {len(uncl)} "
                f"ED(s) on {label}: {unclassified_names}. Update zone_c "
                f"or zone_d dicts to cover these names before re-running."
            )

        mean_c = zc["population"].mean() if len(zc) else float("nan")
        mean_d = zd["population"].mean() if len(zd) else float("nan")
        gap_c_vs_prov = (
            (mean_c - PROVINCIAL_MEAN) / PROVINCIAL_MEAN * 100.0
            if len(zc) else float("nan")
        )
        gap_d_vs_prov = (
            (mean_d - PROVINCIAL_MEAN) / PROVINCIAL_MEAN * 100.0
            if len(zd) else float("nan")
        )
        zone_gap = (mean_c - mean_d) if len(zc) and len(zd) else float("nan")
        zone_gap_pct = (
            (zone_gap / mean_d * 100.0)
            if len(zc) and len(zd) else float("nan")
        )
        packing_signature_c = gap_c_vs_prov >= P1_THRESHOLD_PCT
        packing_signature_d = gap_d_vs_prov >= P1_THRESHOLD_PCT

        results.append({
            "test": "Edmonton Zone C/D packing counter-test",
            "map": label,
            "zone": "Zone C (north of NSR)",
            "n_eds": len(zc),
            "mean_population": round(mean_c, 1) if len(zc) else "",
            "deviation_vs_provincial_mean_pct": (
                round(gap_c_vs_prov, 2) if len(zc) else ""
            ),
            "zone_gap_pct": round(zone_gap_pct, 2) if len(zc) and len(zd) else "",
            "unclassified_count": len(uncl),
            "unclassified_names": ";".join(uncl["ed_name"].tolist()),
            "p1_threshold_pct": P1_THRESHOLD_PCT,
            "signature_detected": bool(packing_signature_c),
        })
        results.append({
            "test": "Edmonton Zone C/D packing counter-test",
            "map": label,
            "zone": "Zone D (south of NSR)",
            "n_eds": len(zd),
            "mean_population": round(mean_d, 1) if len(zd) else "",
            "deviation_vs_provincial_mean_pct": (
                round(gap_d_vs_prov, 2) if len(zd) else ""
            ),
            "zone_gap_pct": round(zone_gap_pct, 2) if len(zc) and len(zd) else "",
            "unclassified_count": len(uncl),
            "unclassified_names": ";".join(uncl["ed_name"].tolist()),
            "p1_threshold_pct": P1_THRESHOLD_PCT,
            "signature_detected": bool(packing_signature_d),
        })
    return results


def count_eds_containing_city(df: pd.DataFrame, city: str) -> tuple[int, list[str]]:
    """Count 2026 EDs whose name references the given city, either as
    prefix or as hybrid component. Returns (count, list_of_ed_names).
    """
    matches = []
    for name in df["ed_name"].tolist():
        # Direct prefix
        if name.startswith(city + "-") or name == city:
            matches.append(name)
            continue
        # Hybrid component (city-name present as a hyphen-separated piece)
        pieces = name.split("-")
        if city in pieces:
            matches.append(name)
            continue
        # Compound city name exact match within ED name (e.g., "Calgary-Airdrie")
        if city != "Calgary" and city != "Edmonton":
            # exclude big-city prefixes; they would dominate the match
            if f"-{city}" in name or f"{city}-" in name:
                if name not in matches:
                    matches.append(name)
    return len(matches), matches


def test_2_city_split_counter_test(
    maj: pd.DataFrame, minr: pd.DataFrame
) -> list[dict]:
    """Count ED-containing-city for every municipality >= 50k. Flag where
    count >= 4 AND the city is small enough that its splits are not
    forced by population. Population-forced splits (Calgary, Edmonton)
    are not diagnostic of cracking and are recorded but not flagged.
    """
    results = []
    for city, pop_2021 in sorted(CITIES_OVER_50K.items()):
        if pop_2021 < 50000:
            continue
        maj_count, maj_eds = count_eds_containing_city(maj, city)
        min_count, min_eds = count_eds_containing_city(minr, city)
        # A split is diagnostic of engineered cracking only if the city
        # could fit in fewer EDs at the statutory maximum.
        population_forced = pop_2021 > MAX_POP_FOR_4_ED_CRACKING
        signature_maj_unforced = (
            maj_count >= C1_THRESHOLD_EDS and not population_forced
        )
        signature_min_unforced = (
            min_count >= C1_THRESHOLD_EDS and not population_forced
        )
        results.append({
            "test": "City-wide 4-way-split counter-test",
            "city": city,
            "population_2021_census": pop_2021,
            "population_forced_4plus": population_forced,
            "majority_ed_count": maj_count,
            "majority_ed_names": ";".join(maj_eds),
            "majority_signature_4plus_unforced": bool(signature_maj_unforced),
            "minority_ed_count": min_count,
            "minority_ed_names": ";".join(min_eds),
            "minority_signature_4plus_unforced": bool(signature_min_unforced),
        })
    return results


def main():
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    maj = pd.read_csv(DATA / "v0_1_majority_2026_populations.csv")
    minr = pd.read_csv(DATA / "v0_1_minority_2026_populations.csv")

    print("=" * 70)
    print("Track Q counter-test — symmetry-of-test-selection check")
    print("=" * 70)
    print(f"Provincial mean population (report baseline): {PROVINCIAL_MEAN:,}")
    print(f"P1 packing threshold: zone mean >= prov mean + {P1_THRESHOLD_PCT}%")
    print(f"C1 4-way split threshold: city split across >= {C1_THRESHOLD_EDS} EDs")
    print()

    # Test 1: Edmonton packing counter-test
    test1_rows = test_1_edmonton_packing(maj, minr)
    print("Test 1 — Edmonton Zone C/D packing counter-test")
    print("-" * 70)
    for row in test1_rows:
        sig = "SIGNATURE" if row["signature_detected"] else "no signature"
        print(
            f"  {row['map']}: {row['zone']} n={row['n_eds']} "
            f"mean={row['mean_population']} "
            f"dev_vs_prov_mean={row['deviation_vs_provincial_mean_pct']}% "
            f"[{sig}]"
        )
    print()

    # Test 2: City-split counter-test
    test2_rows = test_2_city_split_counter_test(maj, minr)
    print("Test 2 — City-wide 4-way-split counter-test")
    print("-" * 70)
    print("  (Population-forced splits are recorded but not diagnostic;")
    print(f"   threshold = 3 statutory quotas = {MAX_POP_FOR_4_ED_CRACKING:,}.)")
    for row in test2_rows:
        forced = " [pop-forced]" if row["population_forced_4plus"] else ""
        flag_maj = (
            "** CRACKING-CANDIDATE **"
            if row["majority_signature_4plus_unforced"]
            else "ok"
        )
        flag_min = (
            "** CRACKING-CANDIDATE **"
            if row["minority_signature_4plus_unforced"]
            else "ok"
        )
        print(
            f"  {row['city']:20s} (pop {row['population_2021_census']:>7,}){forced}: "
            f"maj={row['majority_ed_count']} [{flag_maj}]  "
            f"min={row['minority_ed_count']} [{flag_min}]"
        )
    print()

    # Write CSV output (flatten both tests into one file)
    out_path = DATA / "v0_1_majority_symmetry_counter_test.csv"
    all_fields = sorted({k for row in (test1_rows + test2_rows) for k in row.keys()})
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=all_fields)
        writer.writeheader()
        for row in (test1_rows + test2_rows):
            # normalize missing keys so a unified CSV is writable
            for k in all_fields:
                row.setdefault(k, "")
            writer.writerow(row)
    print(f"CSV written: {out_path.relative_to(ROOT)}")

    # Verdict summary
    print()
    print("=" * 70)
    print("Verdict")
    print("=" * 70)
    # Test 1
    maj_sigs_t1 = sum(
        1 for r in test1_rows
        if r["map"] == "Majority 2026" and r["signature_detected"]
    )
    min_sigs_t1 = sum(
        1 for r in test1_rows
        if r["map"] == "Minority 2026" and r["signature_detected"]
    )
    print(
        f"Test 1 Edmonton packing signatures: "
        f"majority={maj_sigs_t1}, minority={min_sigs_t1}"
    )
    # Test 2
    maj_sigs_t2 = sum(
        1 for r in test2_rows if r["majority_signature_4plus_unforced"]
    )
    min_sigs_t2 = sum(
        1 for r in test2_rows if r["minority_signature_4plus_unforced"]
    )
    maj_4way_cities = [
        r["city"] for r in test2_rows if r["majority_signature_4plus_unforced"]
    ]
    min_4way_cities = [
        r["city"] for r in test2_rows if r["minority_signature_4plus_unforced"]
    ]
    print(
        f"Test 2 unforced 4-way-split cities (cracking candidates): "
        f"majority={maj_sigs_t2} ({maj_4way_cities}), "
        f"minority={min_sigs_t2} ({min_4way_cities})"
    )


if __name__ == "__main__":
    main()
