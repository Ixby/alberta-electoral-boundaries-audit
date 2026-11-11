# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain), Statistics Canada 2021 (Open Government Licence) | https://ixby.github.io
"""
turnout_scenario.py
-------------------
What if the reserves had voted in 2023 at the turnout they showed in the 2026 referendum?
Descriptive, exploratory, not registered.

For each nation, the scale factor is its 2026 referendum Question 10 election-day valid ballots at
on-reserve voting places (measures.json, referendum_q10_by_nation) over its 2023 election-day
two-party votes in on-reserve voting areas (same rule as packing_cracking.py: at least half the
voting area's land on the reserve). Each reserve voting area's NDP and UCP votes are multiplied by
its nation's factor, keeping the 2023 party split. Every other voting area keeps its 2023 votes.
Districts are then re-decided on election-day two-party votes, and seats are counted province-wide.

Tsuut'ina has no on-reserve community voting place in the referendum file (Redwood House is a
leasehold townsite), so it has no factor of its own: the main scenario leaves it at 2023 turnout,
and a sensitivity gives it the factor of all the other nations pooled.

Also reported, for each district holding reserve areas: the break-even factor, the multiple of
2023 reserve turnout at which the reserve vote would flip the district (none when the reserve vote
leans the same way as the winner).

Backward: data/shapefiles/derived/va_polygons_with_2023_votes.gpkg, measures.py, measures.json
Forward: findings/reserves_by_map/README.md
"""
import json
import sys
import warnings
from pathlib import Path

import geopandas as gpd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from measures import MAPS, REPO, RESERVES  # noqa: E402

warnings.filterwarnings("ignore")


def main():
    ref = json.loads((HERE / "measures.json").read_text(encoding="utf-8"))["referendum_q10_by_nation"]
    va = gpd.read_file(REPO / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg").to_crs(3401)
    va["vid"] = range(len(va))
    csd = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(3401)
    res = csd[csd["CSDUID"].astype(str).isin(RESERVES)][["CSDUID", "geometry"]]
    o = gpd.overlay(va[["vid", "geometry"]], res, how="intersection")
    o["share"] = o.area / o["vid"].map(va.set_index("vid").area)
    o = o[o["share"] >= 0.5]
    va["nation"] = va["vid"].map(dict(zip(o["vid"], o["CSDUID"].astype(str).map(lambda c: RESERVES[c][0]))))

    nations = {}
    for n, d in va[va["nation"].notna()].groupby("nation"):
        tp = float(d["va_ndp"].sum() + d["va_ucp"].sum())
        b = ref.get(n)
        ballots = b["remain"] + b["begin_separation_process"] if b else None
        nations[n] = {"voting_areas_2023": int(len(d)), "two_party_2023": round(tp),
                      "ndp_share_2023": round(100 * d["va_ndp"].sum() / tp, 1),
                      "referendum_ballots_2026": ballots,
                      "factor": round(ballots / tp, 2) if ballots else None}
    pooled_b = sum(v["referendum_ballots_2026"] for v in nations.values() if v["factor"])
    pooled_t = sum(v["two_party_2023"] for v in nations.values() if v["factor"])
    pooled = pooled_b / pooled_t

    def factors(sens):
        return {n: (v["factor"] if v["factor"] else (pooled if sens else 1.0)) for n, v in nations.items()}

    pts = va.copy()
    pts["geometry"] = va.geometry.representative_point()
    out = {"meta": {"status": "exploratory, descriptive, not registered",
                    "votes": "2023 election day, two-party (va_ndp, va_ucp)",
                    "pooled_factor_for_tsuutina_sensitivity": round(pooled, 2)},
           "nations": nations, "maps": {}}
    for m, (f, col) in MAPS.items():
        e = gpd.read_file(REPO / f).to_crs(3401)[[col, "geometry"]]
        j = gpd.sjoin(pts[["vid", "geometry"]], e, how="left", predicate="within")
        va["district"] = va["vid"].map(dict(zip(j["vid"], j[col])))
        res_m = {"unplaced_voting_areas": int(va["district"].isna().sum())}
        for label, sens in (("2023_turnout", None), ("2026_turnout", False), ("2026_turnout_tsuutina_pooled", True)):
            fac = factors(sens) if sens is not None else {n: 1.0 for n in nations}
            k = va["nation"].map(fac).fillna(1.0)
            g = va.assign(n=va["va_ndp"] * k, u=va["va_ucp"] * k).groupby("district")[["n", "u"]].sum()
            win = (g["n"] > g["u"]).map({True: "NDP", False: "UCP"})
            res_m[label] = {"seats": {"NDP": int((win == "NDP").sum()), "UCP": int((win == "UCP").sum())},
                            "winners": win.to_dict()}
        base, new, sens = (res_m[x]["winners"] for x in ("2023_turnout", "2026_turnout", "2026_turnout_tsuutina_pooled"))
        rows = []
        for dist, d in va.groupby("district"):
            r = d[d["nation"].notna()]
            if r.empty:
                continue
            rn, ru = r["va_ndp"].sum(), r["va_ucp"].sum()
            rest = (d["va_ndp"].sum() - rn) - (d["va_ucp"].sum() - ru)  # NDP minus UCP outside reserve areas
            lean = rn - ru
            be = -rest / lean if lean and (-rest / lean) > 0 else None
            fk = factors(False)
            sn = (r["va_ndp"] * r["nation"].map(fk)).sum()
            su = (r["va_ucp"] * r["nation"].map(fk)).sum()
            rows.append({"district": dist, "nations": sorted(r["nation"].unique()),
                         "reserve_two_party_2023": round(rn + ru), "reserve_two_party_2026_turnout": round(sn + su),
                         "district_ndp_minus_ucp_2023": round(rest + lean),
                         "district_ndp_minus_ucp_2026_turnout": round(rest + sn - su),
                         "reserve_share_2026_turnout": round(100 * (sn + su) / (d["va_ndp"].sum() + d["va_ucp"].sum() - rn - ru + sn + su), 1),
                         "winner_2023_turnout": base[dist], "winner_2026_turnout": new[dist],
                         "winner_2026_tsuutina_pooled": sens[dist],
                         "break_even_factor": round(be, 1) if be else None})
        res_m["reserve_districts"] = rows
        res_m["flips"] = [d for d in base if base[d] != new[d]]
        res_m["flips_tsuutina_pooled"] = [d for d in base if base[d] != sens[d]]
        for x in ("2023_turnout", "2026_turnout", "2026_turnout_tsuutina_pooled"):
            del res_m[x]["winners"]
        out["maps"][m] = res_m
    (HERE / "turnout_scenario.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(nations, indent=1, ensure_ascii=False), "pooled", round(pooled, 2))
    for m, r in out["maps"].items():
        print("==", m, "unplaced", r["unplaced_voting_areas"], {x: r[x]["seats"] for x in ("2023_turnout", "2026_turnout", "2026_turnout_tsuutina_pooled")},
              "flips", r["flips"], r["flips_tsuutina_pooled"])
        for d in r["reserve_districts"]:
            print(f"  {d['district']:38s} {d['reserve_two_party_2023']:5d}->{d['reserve_two_party_2026_turnout']:5d} "
                  f"margin {d['district_ndp_minus_ucp_2023']:+6d}->{d['district_ndp_minus_ucp_2026_turnout']:+6d} "
                  f"share {d['reserve_share_2026_turnout']}% {d['winner_2023_turnout']}->{d['winner_2026_turnout']} BE {d['break_even_factor']}")


if __name__ == "__main__":
    main()
