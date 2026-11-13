#!/usr/bin/env python3
"""seat_counts_table.py -- one table of UCP-NDP seats on 2023 votes for five maps.

EXPLORATORY. Computed after the fact for the 2026-11-10 audit. Not a registered test.

Maps   : 2019 (87 seats), commission majority (89), commission minority (89),
         the panel's map (91, the audit's reconstruction), the para-167 map (91, reconstruction).
Ballots: election-day ballots only, and all ballots (the registered Amendment 12 allocation).
Output : findings/audit_2026-11-10/seat_counts_table.json and .md
Run    : python findings/audit_2026-11-10/seat_counts_table.py   (no network, no randomness)

Inputs (all committed; the two .gpkg vote files are Git LFS objects, so `git lfs pull` first):
  votes, election day : data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
  votes, all ballots  : data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg
  2019 map            : column parent_ed_2019 of the vote files (Elections Alberta's own coding)
  majority, minority  : data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg, the official
                        files; a voting area goes to the district that holds its representative
                        point (the rule of the audit's headline scorer, mcmc_ensemble.py
                        score_exogenous_map). Cross-check: data/outputs/assignment_va_to_2026_canonical.csv,
                        a committed table built by centroid, which differs in 12 and 20 voting areas
                        and gives the same seat counts.
  panel               : findings/a10_stepb_run/va_assignment_real_map.csv (district)
  para 167            : findings/iap_para167/va_assignment.csv (district)

Method: each of the 4,765 voting areas belongs to one district on each map. District totals of
UCP and NDP votes are summed; the party with more votes takes the seat (other parties are
ignored, as in analysis/scripts/mcmc_ensemble.py seat_results). "Seats at a tied vote" shifts
every district's two-party UCP share by the same amount until the province is exactly 50/50
(uniform swing), the audit's own definition; an exact tie would count half.
"""
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
VOTES = {
    "election_day": "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg",
    "all_ballots": "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg",
}
CANON = "data/outputs/assignment_va_to_2026_canonical.csv"
PANEL = "findings/a10_stepb_run/va_assignment_real_map.csv"
PARA167 = "findings/iap_para167/va_assignment.csv"
MAPS = [
    ("map_2019", "2019 map", "parent_ed_2019 (Elections Alberta coding)"),
    ("majority_2026", "Commission majority", "data/shapefiles/canonical/ea_majority_2026_eds.gpkg : EDName2025, by representative point"),
    ("minority_2026", "Commission minority", "data/shapefiles/canonical/ea_minority_2026_eds.gpkg : EDName2025, by representative point"),
    ("panel", "Panel's map (reconstruction)", PANEL + " : district"),
    ("para167", "Para. 167 map (reconstruction)", PARA167 + " : district"),
]


def score(ucp, ndp):
    """Seats, tied-vote seats and closest margins from per-district UCP and NDP totals."""
    ucp, ndp = np.asarray(ucp, float), np.asarray(ndp, float)
    two = ucp + ndp
    assert (two > 0).all()
    n = len(two)
    share = ucp / two
    prov = ucp.sum() / two.sum()
    shifted = np.clip(share + (0.5 - prov), 0.0, 1.0)
    wins50 = float((shifted > 0.5 + 1e-9).sum() + 0.5 * (np.abs(shifted - 0.5) <= 1e-9).sum())
    return {
        "n_districts": int(n),
        "ucp_seats": int((ucp > ndp).sum()),
        "ndp_seats": int((ndp > ucp).sum()),
        "exact_ties": int((ucp == ndp).sum()),
        "ucp_two_party_share_pct": round(100 * prov, 4),
        "ucp_seats_at_tied_vote": wins50,
        "ndp_seats_at_tied_vote": n - wins50,
        "ucp_seat_share_at_tied_vote_pct": round(100 * wins50 / n, 2),
        "majority_line": n // 2 + 1,
        "two_thirds_line": int(np.ceil(2 * n / 3)),
    }


def closest(df_d, k=3):
    d = df_d.assign(margin_votes=df_d.ucp - df_d.ndp)
    d = d.reindex(d.margin_votes.abs().sort_values(kind="stable").index).head(k)
    return [
        {"district": i, "winner": "UCP" if r.margin_votes > 0 else "NDP",
         "margin_votes": round(abs(float(r.margin_votes)), 1),
         "margin_two_party_pts": round(100 * abs(float(r.margin_votes)) / float(r.ucp + r.ndp), 2)}
        for i, r in d.iterrows()
    ]


def by_representative_point(va_geom, crs, gpkg):
    ed = gpd.read_file(ROOT / gpkg)[["EDName2025", "geometry"]].to_crs(crs)
    pts = gpd.GeoDataFrame(geometry=va_geom.representative_point(), crs=crs)
    j = gpd.sjoin(pts, ed, predicate="within", how="left")
    assert not j.index.duplicated().any() and j.EDName2025.notna().all(), gpkg
    return j.EDName2025.reindex(pts.index).values


def main():
    canon = pd.read_csv(ROOT / CANON, dtype={"VA_NUMBER": str})
    panel = pd.read_csv(ROOT / PANEL, dtype={"VA_NUMBER": str})
    p167 = pd.read_csv(ROOT / PARA167)
    out = {
        "status": "EXPLORATORY - computed after the fact for the 2026-11-10 audit; not a registered test",
        "what": "UCP-NDP seats on 2023 votes, five maps, two sets of ballots, plus seats at a tied province-wide vote",
        "caveats": [
            "The panel's map and the para-167 map are the audit's reconstructions from the panel's report, not official boundary files.",
            "All-ballots votes use the registered Amendment 12 allocation: ballots not cast on election day are spread over a 2019 division's voting areas with one weight for every party. Other defensible spreads move some all-ballots counts by one or two seats (audit finding vote-substrate-1).",
            "Election-day votes use the audit's equal split of a polling station's votes across the voting areas it serves.",
            "Seats are two-party (UCP against NDP); no third party or independent leads in any district on these files.",
        ],
        "inputs": {"votes": VOTES, "assignments": {k: src for k, _, src in MAPS}},
        "checks": {},
        "table": {},
    }
    rows_md = []
    for vkey, vpath in VOTES.items():
        va = gpd.read_file(ROOT / vpath)
        va["VA_NUMBER"] = va["VA_NUMBER"].astype(str)
        # Row order is the join key for the two reconstructions (node / va_index = row number).
        assert len(va) == 4765 == len(canon) == len(panel) == len(p167)
        assert (va.OBJECTID.values == canon.OBJECTID.values).all()
        assert (va.VA_NUMBER.values == canon.VA_NUMBER.values).all()
        assert (va.parent_ed_2019.values == canon.parent_ed_2019.values).all()
        assert (va.OBJECTID.values == panel.OBJECTID.values).all()
        assert (va.VA_NUMBER.values == panel.VA_NUMBER.values).all()
        assert (p167.va_index.values == np.arange(4765)).all()
        if vkey == "election_day":
            # the canonical assignment file carries its own copy of the election-day votes
            assert np.allclose(va[["va_ndp", "va_ucp", "va_other"]].values,
                               canon[["va_ndp", "va_ucp", "va_other"]].values, atol=1e-9)
        assign = {
            "map_2019": va.parent_ed_2019.values,
            "majority_2026": by_representative_point(va.geometry, va.crs, "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"),
            "minority_2026": by_representative_point(va.geometry, va.crs, "data/shapefiles/canonical/ea_minority_2026_eds.gpkg"),
            "panel": panel.district.values,
            "para167": p167.district.values,
        }
        tot = {c: float(va["va_" + c].sum()) for c in ("ucp", "ndp", "other")}
        out["checks"][vkey] = {
            "voting_areas": int(len(va)),
            "province_ucp": round(tot["ucp"], 3), "province_ndp": round(tot["ndp"], 3),
            "province_other": round(tot["other"], 3),
            "province_all_parties": round(sum(tot.values()), 3),
        }
        out["table"][vkey] = {}
        xc = {}
        for mkey, col in (("majority_2026", "ed_2026_maj"), ("minority_2026", "ed_2026_min")):
            d = pd.DataFrame({"d": canon[col].values, "ucp": va.va_ucp.values, "ndp": va.va_ndp.values}).groupby("d").sum()
            r = score(d.ucp.values, d.ndp.values)
            xc[mkey] = {"voting_areas_assigned_differently": int((canon[col].values != assign[mkey]).sum()),
                        "ucp_seats": r["ucp_seats"], "ndp_seats": r["ndp_seats"],
                        "ucp_seats_at_tied_vote": r["ucp_seats_at_tied_vote"]}
        out["checks"][vkey]["centroid_table_cross_check"] = xc
        for mkey, label, _ in MAPS:
            a = pd.Series(assign[mkey])
            assert a.notna().all(), mkey
            d = pd.DataFrame({"d": a.values, "ucp": va.va_ucp.values, "ndp": va.va_ndp.values}).groupby("d").sum()
            r = score(d.ucp.values, d.ndp.values)
            r["label"] = label
            r["closest_three_districts"] = closest(d)
            out["table"][vkey][mkey] = r
    # markdown table
    md = [
        "# UCP-NDP seats on 2023 votes, five maps",
        "",
        "Exploratory. Computed after the fact for the 2026-11-10 audit by `seat_counts_table.py`. "
        "The panel's map and the para. 167 map are the audit's reconstructions.",
        "",
        "| Map | Seats | Election-day ballots: UCP-NDP | All ballots: UCP-NDP | Tied vote, election-day: UCP-NDP | Tied vote, all ballots: UCP-NDP |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    f = lambda x: str(int(x)) if float(x).is_integer() else str(x)
    for mkey, label, _ in MAPS:
        e, a = out["table"]["election_day"][mkey], out["table"]["all_ballots"][mkey]
        md.append(
            f"| {label} | {e['n_districts']} | {e['ucp_seats']}-{e['ndp_seats']} | {a['ucp_seats']}-{a['ndp_seats']} | "
            f"{f(e['ucp_seats_at_tied_vote'])}-{f(e['ndp_seats_at_tied_vote'])} | "
            f"{f(a['ucp_seats_at_tied_vote'])}-{f(a['ndp_seats_at_tied_vote'])} |"
        )
    e, a = out["checks"]["election_day"], out["checks"]["all_ballots"]
    md += [
        "",
        f"Election-day ballots: {e['province_all_parties']:,.0f} (UCP {e['province_ucp']:,.0f}, NDP {e['province_ndp']:,.0f}); "
        f"UCP two-party share {out['table']['election_day']['map_2019']['ucp_two_party_share_pct']:.2f}%.",
        f"All ballots: {a['province_all_parties']:,.0f} (UCP {a['province_ucp']:,.0f}, NDP {a['province_ndp']:,.0f}); "
        f"UCP two-party share {out['table']['all_ballots']['map_2019']['ucp_two_party_share_pct']:.2f}%.",
        "",
        "\"Tied vote\" moves every district's two-party UCP share by the same amount until the province is 50/50.",
        "All-ballots counts use the registered Amendment 12 allocation; see the README for its limits.",
        "",
    ]
    (HERE / "seat_counts_table.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (HERE / "seat_counts_table.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[4:12]))


if __name__ == "__main__":
    main()
