"""Build VA shapefiles with 2019 and 2015 election vote attribution.

Uses the canonical EA VA polygons (parent_ed_2019 crosswalk) and ED-level
results from data/reference/ to produce:
  data/shapefiles/derived/va_polygons_with_2019_votes.gpkg
  data/shapefiles/derived/va_polygons_with_2015_votes.gpkg

Vote distribution: area-proportional within each 2019 ED. Each VA's share
equals its area divided by the summed area of all VAs in that 2019 ED.
The va_ndp/va_ucp column names are preserved so the MCMC ensemble reads
them identically to the canonical 2023 file.

Purpose: Alberta-specific EG threshold durability analysis across election
cycles. The p95 EG from the neutral ensemble under each year's votes reveals
whether the jurisdiction-specific investigable threshold is election-stable.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""

import sys
from pathlib import Path
import re
import numpy as np
import pandas as pd
import geopandas as gpd

ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / "data"
DERIVED = DATA / "shapefiles" / "derived"
REF = DATA / "reference"
OUTPUTS = DATA / "outputs"

VA_CANONICAL = DERIVED / "va_polygons_with_full_2023_votes.gpkg"
RESULTS_2019 = REF / "alberta_2019_results.csv"
RESULTS_2015 = REF / "alberta_2015_results.csv"
CROSSWALK_2015_2019 = OUTPUTS / "2015_to_2019_crosswalk.csv"

OUT_2019 = DERIVED / "va_polygons_with_2019_votes.gpkg"
OUT_2015 = DERIVED / "va_polygons_with_2015_votes.gpkg"


def _parse_2019_results() -> pd.DataFrame:
    """Extract NDP and UCP vote totals by 2019 ED name."""
    df = pd.read_csv(RESULTS_2019)
    rows = []
    for _, row in df.iterrows():
        ndp_votes = 0.0
        ucp_votes = 0.0
        for i in range(1, 9):
            cand = row.get(f"cand_{i}", "")
            votes = row.get(f"votes_{i}", 0)
            if not isinstance(cand, str) or pd.isna(votes):
                continue
            votes = float(votes)
            m = re.search(r"\((\w+)\)", cand)
            if not m:
                continue
            party = m.group(1).upper()
            if party == "NDP":
                ndp_votes += votes
            elif party == "UCP":
                ucp_votes += votes
        rows.append({"ed_name": row["ed_name"], "ndp": ndp_votes, "ucp": ucp_votes})
    result = pd.DataFrame(rows)
    total_ndp = result["ndp"].sum()
    total_ucp = result["ucp"].sum()
    print(f"  2019 parsed: {len(result)} EDs, NDP total={total_ndp:,.0f}, UCP total={total_ucp:,.0f}")
    two_party_share = total_ndp / (total_ndp + total_ucp)
    print(f"  NDP two-party share: {two_party_share:.3f} ({two_party_share*100:.1f}%)")
    return result.set_index("ed_name")


def _parse_2015_results() -> pd.DataFrame:
    """Extract NDP and UCP-equivalent vote totals by 2015 ED name.

    2015 uses ucp_equiv = PC + WRP (conservative coalition before UCP merger).
    """
    df = pd.read_csv(RESULTS_2015)
    result = df[["ed_2015", "ndp", "ucp_equiv"]].copy()
    # Strip source-document section header accidentally captured in ed_2015 field
    result["ed_2015"] = result["ed_2015"].str.replace(
        r"^Statement Of Results By Poll - ", "", regex=True
    )
    result = result.rename(columns={"ed_2015": "ed_name", "ucp_equiv": "ucp"})
    total_ndp = result["ndp"].sum()
    total_ucp = result["ucp"].sum()
    print(f"  2015 parsed: {len(result)} EDs, NDP total={total_ndp:,.0f}, UCP-equiv total={total_ucp:,.0f}")
    two_party_share = total_ndp / (total_ndp + total_ucp)
    print(f"  NDP two-party share: {two_party_share:.3f} ({two_party_share*100:.1f}%)")
    return result.set_index("ed_name")


def _project_2015_to_2019(results_2015: pd.DataFrame) -> pd.DataFrame:
    """Distribute 2015 ED votes to 2019 EDs using population-weighted crosswalk."""
    xwalk = pd.read_csv(CROSSWALK_2015_2019)
    rows = []
    for _, xrow in xwalk.iterrows():
        ed15 = xrow["ed_2015_2010boundaries"]
        ed19 = xrow["ed_2019_2017boundaries"]
        weight = float(xrow["population_weight"])
        if ed15 not in results_2015.index:
            print(f"  WARNING: {ed15} not in 2015 results — skipping")
            continue
        r = results_2015.loc[ed15]
        rows.append({"ed_2019": ed19, "ndp": r["ndp"] * weight, "ucp": r["ucp"] * weight})
    df = pd.DataFrame(rows).groupby("ed_2019")[["ndp", "ucp"]].sum().reset_index()
    df = df.rename(columns={"ed_2019": "ed_name"})
    total_ndp = df["ndp"].sum()
    total_ucp = df["ucp"].sum()
    print(f"  2015->2019 projected: {len(df)} EDs, NDP={total_ndp:,.0f}, UCP-equiv={total_ucp:,.0f}")
    return df.set_index("ed_name")


def _distribute_to_vas(va: gpd.GeoDataFrame, ed_votes: pd.DataFrame, label: str) -> gpd.GeoDataFrame:
    """Area-proportional distribution of ED-level votes to VA polygons."""
    va = va.copy()
    va["_area"] = va.geometry.area

    # Compute area fraction of each VA within its parent 2019 ED
    ed_area = va.groupby("parent_ed_2019")["_area"].sum().rename("_ed_area")
    va = va.join(ed_area, on="parent_ed_2019")
    va["_frac"] = va["_area"] / va["_ed_area"]

    # Assign ED-level votes scaled by area fraction
    va_ndp = []
    va_ucp = []
    unmatched = []
    for _, row in va.iterrows():
        ed = row["parent_ed_2019"]
        frac = row["_frac"]
        if ed in ed_votes.index:
            va_ndp.append(ed_votes.loc[ed, "ndp"] * frac)
            va_ucp.append(ed_votes.loc[ed, "ucp"] * frac)
        else:
            unmatched.append(ed)
            va_ndp.append(0.0)
            va_ucp.append(0.0)

    if unmatched:
        print(f"  WARNING ({label}): {len(set(unmatched))} EDs unmatched: {set(unmatched)}")

    va["va_ndp"] = va_ndp
    va["va_ucp"] = va_ucp
    va["va_other"] = 0.0  # not available for threshold analysis; set to 0

    total_ndp = va["va_ndp"].sum()
    total_ucp = va["va_ucp"].sum()
    two_party = total_ndp / (total_ndp + total_ucp)
    print(f"  VA distribution ({label}): NDP={total_ndp:,.0f}, UCP={total_ucp:,.0f}, "
          f"NDP two-party={two_party:.3f} ({two_party*100:.1f}%)")

    return va.drop(columns=["_area", "_ed_area", "_frac"])


def build_2019_va():
    print("[2019] Loading canonical VA polygons...")
    va = gpd.read_file(VA_CANONICAL)
    print(f"  {len(va)} VAs loaded")

    print("[2019] Parsing election results...")
    ed_votes = _parse_2019_results()

    print("[2019] Distributing votes to VAs...")
    va_out = _distribute_to_vas(va, ed_votes, "2019")

    keep_cols = ["OBJECTID", "ED_NUM", "ED_NAME", "VA_NUMBER",
                 "va_ndp", "va_ucp", "va_other", "parent_ed_2019", "geometry"]
    va_out = va_out[[c for c in keep_cols if c in va_out.columns]]
    va_out.to_file(OUT_2019, driver="GPKG")
    print(f"[2019] Written: {OUT_2019}")


def build_2015_va():
    print("[2015] Loading canonical VA polygons...")
    va = gpd.read_file(VA_CANONICAL)
    print(f"  {len(va)} VAs loaded")

    print("[2015] Parsing election results...")
    results_2015 = _parse_2015_results()

    print("[2015] Projecting 2015 EDs to 2019 EDs via crosswalk...")
    ed_votes_2019 = _project_2015_to_2019(results_2015)

    # Check coverage
    va_eds = set(va["parent_ed_2019"].unique())
    missing = va_eds - set(ed_votes_2019.index)
    if missing:
        print(f"  WARNING: {len(missing)} 2019 EDs missing from crosswalk-projected 2015 votes: {missing}")

    print("[2015] Distributing votes to VAs...")
    va_out = _distribute_to_vas(va, ed_votes_2019, "2015")

    keep_cols = ["OBJECTID", "ED_NUM", "ED_NAME", "VA_NUMBER",
                 "va_ndp", "va_ucp", "va_other", "parent_ed_2019", "geometry"]
    va_out = va_out[[c for c in keep_cols if c in va_out.columns]]
    va_out.to_file(OUT_2015, driver="GPKG")
    print(f"[2015] Written: {OUT_2015}")


if __name__ == "__main__":
    build_2019_va()
    print()
    build_2015_va()
    print()
    print("Done. Use --va-file with mcmc_ensemble_canonical.py to run threshold ensembles:")
    print(f"  python analysis/scripts/mcmc_ensemble_canonical.py \\")
    print(f"    --va-file {OUT_2019} --run-id threshold_2019 --n-steps 50000 --n-chains 2 --seed 3562959107")
    print(f"  python analysis/scripts/mcmc_ensemble_canonical.py \\")
    print(f"    --va-file {OUT_2015} --run-id threshold_2015 --n-steps 50000 --n-chains 2 --seed 3562959107")
