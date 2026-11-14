# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain), Statistics Canada 2021 (Open Government Licence) | https://ixby.github.io
"""
packing_cracking.py
-------------------
Are the reserve voters packed or cracked on any map? Descriptive, exploratory, not registered.

For each map, every 2023 voting area (election-day votes, the located substrate) is assigned to the
district holding its representative point. A voting area is "on reserve" when at least half its land
lies in one of the reserves in measures.py. For each district that holds reserve voting areas, the
script reports: the reserve two-party votes and the NDP share of them, the district's two-party
votes and margin, the reserve share of the district's two-party vote, and whether moving every
reserve vote to the other side would change the district's winner (a "decisive" bloc).

Cracking would show as a group spread across more districts, each with a smaller share and none
decisive. Packing would show as a group concentrated where its party already wins big. Election-day
votes only: advance and special ballots cannot be located on or off a reserve. The panel's map is
the reconstruction.

Backward: data/shapefiles/derived/va_polygons_with_2023_votes.gpkg, measures.py (RESERVES, MAPS)
Forward: findings/reserves_by_map/README.md
"""
import json
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

from measures import MAPS, REPO, RESERVES

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
NATION_GROUP = {k: ("Blackfoot" if "Blackfoot" in v[0] else v[0]) for k, v in RESERVES.items()}


def main():
    va = gpd.read_file(REPO / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg").to_crs(3401)
    va["vid"] = range(len(va))
    csd = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(3401)
    res = csd[csd["CSDUID"].astype(str).isin(RESERVES)][["CSDUID", "geometry"]]
    o = gpd.overlay(va[["vid", "geometry"]], res, how="intersection")
    o["share"] = o.area / o["vid"].map(va.set_index("vid").area)
    o = o[o["share"] >= 0.5]
    va["group"] = va["vid"].map(dict(zip(o["vid"], o["CSDUID"].astype(str).map(NATION_GROUP))))
    pts = va.copy()
    pts["geometry"] = va.geometry.representative_point()
    out = {"reserve_voting_areas": {g: int((va["group"] == g).sum()) for g in sorted(va["group"].dropna().unique())},
           "reserve_votes_2023_election_day": {}, "maps": {}}
    for g, d in va[va["group"].notna()].groupby("group"):
        n, u = d["va_ndp"].sum(), d["va_ucp"].sum()
        out["reserve_votes_2023_election_day"][g] = {"ndp": round(n), "ucp": round(u), "ndp_share_two_party": round(100 * n / (n + u), 1)}
    for m, (f, col) in MAPS.items():
        e = gpd.read_file(REPO / f).to_crs(3401)[[col, "geometry"]]
        j = gpd.sjoin(pts[["vid", "geometry"]], e, how="left", predicate="within")
        va["district"] = va["vid"].map(dict(zip(j["vid"], j[col])))
        rows = []
        for dist, d in va.groupby("district"):
            r = d[d["group"].notna()]
            if r.empty:
                continue
            dn, du = d["va_ndp"].sum(), d["va_ucp"].sum()
            rn, ru = r["va_ndp"].sum(), r["va_ucp"].sum()
            margin = dn - du  # NDP minus UCP, election day
            flip = (dn - rn + ru) - (du - ru + rn)  # margin if every reserve vote went the other way
            rows.append({"district": dist, "groups": sorted(r["group"].unique()),
                         "reserve_two_party": round(rn + ru), "reserve_ndp_share": round(100 * rn / (rn + ru), 1),
                         "district_two_party": round(dn + du), "district_ndp_minus_ucp": round(margin),
                         "district_winner": "NDP" if margin > 0 else "UCP",
                         "reserve_share_of_district": round(100 * (rn + ru) / (dn + du), 1),
                         "decisive": bool((margin > 0) != (flip > 0)),
                         "winner_without_reserves": "NDP" if (dn - rn) > (du - ru) else "UCP"})
        out["maps"][m] = sorted(rows, key=lambda x: x["district"])
    (HERE / "packing_cracking.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out["reserve_votes_2023_election_day"], indent=1))
    for m, rows in out["maps"].items():
        print("==", m)
        for r in rows:
            print(f"  {r['district']:40s} {','.join(r['groups']):22s} reserve {r['reserve_two_party']:5d} ({r['reserve_ndp_share']}% NDP) = {r['reserve_share_of_district']}% of {r['district_two_party']}; margin {r['district_ndp_minus_ucp']:+d} {r['district_winner']}; without reserves {r['winner_without_reserves']}; decisive {r['decisive']}")


if __name__ == "__main__":
    main()
