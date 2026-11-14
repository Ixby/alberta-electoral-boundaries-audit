# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
real_maps.py

Parts 1 and 3 of preregistration/packing_cracking_2026-11-07.md for the real maps: wasted votes split
into surplus (packing-type) and losses (cracking-type, by margin), each map's seats sorted by NDP
two-party share, and where the NDP votes of named areas land. Unregistered. Applies no test of intent.

Reads   data/shapefiles/derived/va_polygons_with_2023_votes.gpkg, va_polygons_all_2023_ballots_primary.gpkg
        data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg, iap_assembled/iap_2026_assembled_v3.gpkg,
        findings/iap_para167/para167_map.gpkg, comparison.json (group membership),
        data/shapefiles/reference/alberta_2021_csds.gpkg
Writes  findings/packing_cracking/real_maps.json

Usage: python -W ignore findings/packing_cracking/real_maps.py
"""
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BALLOTS = {"election_day": ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg",
           "all_ballots": ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"}
MAPS = {"majority": (ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
        "minority": (ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025"),
        "panel": (ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg", "district"),
        "para167": (ROOT / "findings/iap_para167/para167_map.gpkg", "district")}
CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
LETHBRIDGE = "4802012"
NEAR = 0.10


def assign(pts, f, col):
    eds = gpd.read_file(f).to_crs(pts.crs)[[col, "geometry"]]
    j = gpd.sjoin(pts, eds, how="left", predicate="within")
    return j[~j.index.duplicated(keep="first")][col].reindex(pts.index)


def waste(u, n):
    t = u + n
    half = t / 2
    ndp_win = n > u
    out = {}
    for party, v, win in (("ndp", n, ndp_win), ("ucp", u, ~ndp_win)):
        margin = (2 * v - t) / t
        out[party] = {"surplus_pct": round(100 * float((v - half)[win].sum() / t.sum()), 2),
                      "loss_near_pct": round(100 * float(v[~win & (margin > -NEAR)].sum() / t.sum()), 2),
                      "loss_far_pct": round(100 * float(v[~win & (margin <= -NEAR)].sum() / t.sum()), 2),
                      "seats_won": int(win.sum()), "seats_lost_near": int((~win & (margin > -NEAR)).sum()),
                      "won_by_40_plus": int((win & (margin >= 0.40)).sum())}
        out[party]["total_waste_pct"] = round(out[party]["surplus_pct"] + out[party]["loss_near_pct"] + out[party]["loss_far_pct"], 2)
    out["efficiency_gap_two_party_pct"] = round(out["ndp"]["total_waste_pct"] - out["ucp"]["total_waste_pct"], 2)
    return out


def area(lab, u, n, mask, pop=None):
    g = pd.DataFrame({"d": lab, "u": u, "n": n})
    tot = g.groupby("d")[["u", "n"]].sum()
    m = (tot.n - tot.u) / (tot.n + tot.u)
    a = g[mask].groupby("d").n.sum()
    mm = m.reindex(a.index)
    nd = a.sum()
    return {"ndp_votes": round(float(nd)), "in_ndp_won": round(100 * float(a[mm > 0].sum() / nd), 1),
            "in_lost_near": round(100 * float(a[(mm <= 0) & (mm > -NEAR)].sum() / nd), 1),
            "in_lost_far": round(100 * float(a[mm <= -NEAR].sum() / nd), 1),
            "districts": {d: round(float(100 * mm[d]), 1) for d in a.sort_values(ascending=False).index if a[d] >= 0.02 * nd}}


def main():
    base = gpd.read_file(BALLOTS["election_day"]).to_crs(3400)
    pts = base[["geometry"]].copy()
    pts["geometry"] = base.geometry.representative_point()
    labels = {"2019_enacted": base.parent_ed_2019}
    for k, (f, col) in MAPS.items():
        labels[k] = assign(pts, f, col)
        assert labels[k].notna().all(), k
    csd = gpd.read_file(CSD).to_crs(3400)
    ucol = next(c for c in csd.columns if c.upper() == "CSDUID")
    j = gpd.sjoin(pts, csd[[ucol, "geometry"]], how="left", predicate="within")
    leth = (j[~j.index.duplicated(keep="first")][ucol].astype(str).reindex(pts.index) == LETHBRIDGE).to_numpy()

    comp = json.loads((ROOT / "findings/iap_para167/comparison.json").read_text())
    groups = {"west_calgary_cochrane": next(g for g in comp["groups"] if "Cochrane" in g["panel"]),
              "south": next(g for g in comp["groups"] if "Lethbridge" in g["panel"])}
    gmask = {name: labels["panel"].isin(g["panel"]).to_numpy() for name, g in groups.items()}

    out = {"plan": "preregistration/packing_cracking_2026-11-07.md", "lethbridge_vas": int(leth.sum())}
    for b, f in BALLOTS.items():
        v = gpd.read_file(f, ignore_geometry=True)
        assert (v.OBJECTID.values == base.OBJECTID.values).all()
        u, n = v.va_ucp.to_numpy(float), v.va_ndp.to_numpy(float)
        blk = {}
        for k, lab in labels.items():
            t = pd.DataFrame({"d": lab.values, "u": u, "n": n}).groupby("d")[["u", "n"]].sum()
            share = (t.n / (t.u + t.n)).sort_values()
            blk[k] = {"n_seats": int(len(t)), "waste": waste(t.u.to_numpy(), t.n.to_numpy()),
                      "sorted_ndp_share": [round(float(x), 4) for x in share.values],
                      "sorted_names": list(share.index),
                      "seats_40_to_50_ndp": int(((share >= 0.40) & (share < 0.50)).sum()),
                      "seats_under_30_ndp": int((share < 0.30).sum()),
                      "lethbridge": area(lab.values, u, n, leth)}
            if k in ("panel", "para167"):
                blk[k]["areas"] = {name: area(lab.values, u, n, m) for name, m in gmask.items()}
        out[b] = blk
    (HERE / "real_maps.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    for b in BALLOTS:
        print("==", b)
        for k, x in out[b].items():
            w = x["waste"]
            print(f"{k:13s} seats {x['n_seats']}  NDP surplus {w['ndp']['surplus_pct']:5.2f} near-loss {w['ndp']['loss_near_pct']:5.2f} far-loss {w['ndp']['loss_far_pct']:5.2f} | UCP surplus {w['ucp']['surplus_pct']:5.2f} near {w['ucp']['loss_near_pct']:5.2f} far {w['ucp']['loss_far_pct']:5.2f} | EG2p {w['efficiency_gap_two_party_pct']:+.2f} | 40-50% {x['seats_40_to_50_ndp']} <30% {x['seats_under_30_ndp']} | NDP won40+ {w['ndp']['won_by_40_plus']}")
            print("   Lethbridge:", x["lethbridge"])
            for name, a in x.get("areas", {}).items():
                print("   ", name, a)


if __name__ == "__main__":
    main()
