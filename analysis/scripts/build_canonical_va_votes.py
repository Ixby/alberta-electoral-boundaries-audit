"""Build canonical VA-level election-day vote attribution for 2023 Alberta general election.

Only election-day ballot rows carry a VA assignment in Elections Alberta's published
results. Advance, mobile, and special ballots are reported at the ED level only —
EA does not record which VA an advance voter came from. This script uses only the
election-day rows, which represent 381,932 NDP votes and are the only votes that
can be honestly attributed to a specific geographic voting area.

Where a polling station serves multiple VAs (e.g., voting_areas = "001,002,003"),
votes are split equally across those VAs. This is the only defensible split given
EA publishes no within-station geographic breakdown.

Backward:
  data/shapefiles/reference/alberta_2023_vas/EA_Voting_Area_Boundaries_2023.shp
  data/outputs/polls_2023_unified.csv
Forward:
  data/shapefiles/canonical/va_2023_election_day_votes.gpkg
"""
from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
VA_SHP = ROOT / "data/shapefiles/reference/alberta_2023_vas/EA_Voting_Area_Boundaries_2023.shp"
POLLS_CSV = ROOT / "data/outputs/polls_2023_unified.csv"
OUT_GPKG = ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg"

EXPECTED_NDP_TOTAL = 381_932


def build() -> gpd.GeoDataFrame:
    va = gpd.read_file(VA_SHP)
    # Normalise join keys: ED_NUM is zero-padded 2-digit str, VA_NUMBER is 3-digit str
    va["_ed"] = va["ED_NUM"].str.zfill(2)
    va["_va"] = va["VA_NUMBER"].str.zfill(3)

    polls = pd.read_csv(POLLS_CSV, encoding="latin1")
    ed_polls = polls[polls["ballot_type"] == "Election Day"].copy()

    # Explode: one row per (station, VA), equal-split votes
    rows: list[dict] = []
    for _, row in ed_polls.iterrows():
        raw = str(row.get("voting_areas", ""))
        if not raw or raw == "nan":
            continue
        vas = [v.strip().zfill(3) for v in raw.split(",") if v.strip()]
        if not vas:
            continue
        n = len(vas)
        ed_str = str(int(row["sheet_num"])).zfill(2)
        for va_num in vas:
            rows.append({
                "_ed": ed_str,
                "_va": va_num,
                "va_ndp": row["ndp_votes"] / n,
                "va_ucp": row["ucp_votes"] / n,
                "va_other": row["other_votes"] / n,
            })

    exploded = pd.DataFrame(rows)

    # Aggregate in case a VA_NUMBER appears more than once within an ED
    agg = (
        exploded.groupby(["_ed", "_va"], as_index=False)
        [["va_ndp", "va_ucp", "va_other"]]
        .sum()
    )

    result = va.merge(agg, on=["_ed", "_va"], how="left")
    result[["va_ndp", "va_ucp", "va_other"]] = (
        result[["va_ndp", "va_ucp", "va_other"]].fillna(0.0)
    )
    result = result.drop(columns=["_ed", "_va"])

    ndp_total = result["va_ndp"].sum()
    if abs(ndp_total - EXPECTED_NDP_TOTAL) > 1:
        raise ValueError(
            f"NDP vote total mismatch: got {ndp_total:.1f}, expected {EXPECTED_NDP_TOTAL}. "
            "Check ED_NUM / VA_NUMBER join keys."
        )

    unmatched = (result["va_ndp"] == 0) & (result["va_ucp"] == 0)
    n_unmatched = unmatched.sum()
    if n_unmatched > 0:
        print(f"WARNING: {n_unmatched} VAs received zero votes (unmatched in polls CSV).")
        print(result[unmatched][["ED_NUM", "VA_NUMBER"]].to_string())

    return result


if __name__ == "__main__":
    print("Building canonical VA election-day vote attribution...")
    gdf = build()
    print(f"Rows: {len(gdf)}")
    print(f"NDP total: {gdf['va_ndp'].sum():.1f}  (expected {EXPECTED_NDP_TOTAL})")
    print(f"UCP total: {gdf['va_ucp'].sum():.1f}")
    print(f"UCP share: {gdf['va_ucp'].sum() / (gdf['va_ucp'].sum() + gdf['va_ndp'].sum()) * 100:.2f}%")
    gdf.to_file(OUT_GPKG, driver="GPKG")
    print(f"Written: {OUT_GPKG}")
