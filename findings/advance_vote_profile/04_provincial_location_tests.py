"""Two partial truths inside provincial divisions (exploratory, not registered).

A. 2023. Each division lists its advance polls by place name with their own
   counts. Where the places could be geocoded (03_geocode_advance_polls.py),
   each voting area is given to its nearest advance poll. That "catchment" is a
   guess: an elector may use any advance poll. A wrong catchment blurs real
   differences, so the slope measured here is a floor, not an estimate.

B. 2015. In rural divisions the advance polls are named for towns
   ("ADVANCE-GRIMSHAW") and so are the election-day polls ("GRIMSHAW NORTH").
   Matching names gives each advance poll a home set of election-day polls.

Both ask the same thing: inside a division, do advance voters near NDP-leaning
election-day polls lean NDP too (beta near 1), or does every advance poll show
the division's one mix (beta = 0, the current rule M0)?

Writes outputs/provincial_location_tests.json, outputs/advance_locations_2023.csv,
       outputs/advance_catchments_2023.csv, outputs/advance_places_2015.csv

Usage: python findings/advance_vote_profile/04_provincial_location_tests.py
"""
import json
import re

import geopandas as gpd
import numpy as np
import pandas as pd

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # works under python -I
import _models as M
from _common import INPUTS, OUT, VA_EDAY, WORKBOOK_2023, build_va_table, load_2023_rows, load_va, logit, region_of, write_csv, write_json

BETAS = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
LAMS = [0, 0.5, 1.0]


def fe_slope(x, y, w, grp):
    x, y, w, grp = np.asarray(x, float), np.asarray(y, float), np.asarray(w, float), np.asarray(grp)
    s = pd.DataFrame({"x": x, "y": y, "w": w, "g": grp})
    s["xd"] = s.x - s.groupby("g").apply(lambda d: np.average(d.x, weights=d.w)).reindex(s.g).values
    s["yd"] = s.y - s.groupby("g").apply(lambda d: np.average(d.y, weights=d.w)).reindex(s.g).values
    den = np.sum(s.w * s.xd ** 2)
    b = float(np.sum(s.w * s.xd * s.yd) / den)
    cl = (s.w * s.xd * (s.yd - b * s.xd)).groupby(s.g).sum()
    return {"beta": round(b, 3), "se_clustered": round(float(np.sqrt((cl ** 2).sum()) / den), 3), "n": int(len(s)),
            "groups": int(s.g.nunique()), "corr_within": round(float(np.corrcoef(s.xd, s.yd)[0, 1]), 3)}


def part_a():
    raw = load_2023_rows()
    g = load_va().to_crs(3400)
    t = build_va_table(g, raw)
    pts = g.geometry.representative_point()
    t["x"], t["y"] = pts.x.values, pts.y.values
    gc = pd.read_csv(INPUTS / "advance_poll_geocodes.csv", dtype={"ed": str})
    adv = raw[raw.kind == "Advance"].merge(gc[["ed", "name", "lat", "lon"]], on=["ed", "name"], how="left")
    ok = adv.lat.notna()
    P = gpd.GeoSeries(gpd.points_from_xy(adv.lon[ok], adv.lat[ok]), crs=4326).to_crs(3400)
    adv["x"], adv["y"] = np.nan, np.nan
    adv.loc[ok[ok].index, "x"] = P.x.values
    adv.loc[ok[ok].index, "y"] = P.y.values
    # keep a geocode only if it falls inside the division (a same-named place elsewhere is a false hit)
    div_poly = g.dissolve("ed").geometry
    inside = [bool(div_poly[e].buffer(500).contains(p)) for e, p in zip(adv.ed[ok], P)]
    adv["located"] = False
    adv.loc[ok[ok].index, "located"] = inside
    out = {"advance_locations": int(len(adv)), "geocoded": int(ok.sum()), "geocoded_inside_division": int(adv.located.sum())}
    rows, per, catch = [], {}, []
    rules = {"M0": M.m0, "M1": M.m1, "M2": M.m2}
    for b_ in BETAS:
        for l_ in LAMS:
            rules[f"G({b_},{l_})"] = (lambda b_, l_: lambda en, eu, gp, An, Au: M.general(en, eu, gp, An, Au, b_, l_, shrink_k=10))(b_, l_)
    for ed, a in adv.groupby("ed"):
        a = a[a.located & ((a.ndp + a.ucp) >= 50)]
        if len(a) < 2:
            continue
        complete = bool(len(a) == (adv.ed == ed).sum())
        v = t[t.ed == ed]
        d = np.hypot(v.x.values[:, None] - a.x.values[None, :], v.y.values[:, None] - a.y.values[None, :])
        near = d.argmin(axis=1)
        for i, j in zip(v.index, near):
            catch.append((i, ed, a.name.values[j], int(a.ndp.values[j]), int(a.ucp.values[j])))
        alloc = {k: r(v.e_n.values, v.e_u.values, v.gap.values, a.ndp.sum(), a.ucp.sum()) for k, r in rules.items()}
        for j, r in enumerate(a.itertuples()):
            c = near == j
            if v.e_n.values[c].sum() + v.e_u.values[c].sum() < 50:
                continue
            row = dict(ed=ed, name=r.name, complete=complete, a_ndp=r.ndp, a_ucp=r.ucp, c_ndp=v.e_n.values[c].sum(), c_ucp=v.e_u.values[c].sum(),
                       c_gap=v.gap.values[c].sum(), c_valid=v.eday_valid.values[c].sum(), n_vas=int(c.sum()))
            for k, (n, u) in alloc.items():
                row[f"{k}_n"], row[f"{k}_u"] = n[c].sum(), u[c].sum()
            rows.append(row)
    write_csv(pd.DataFrame(catch, columns=["va_row_idx", "ed", "location", "loc_ndp", "loc_ucp"]), "advance_catchments_2023.csv")
    L = pd.DataFrame(rows)
    L["adv_share"] = L.a_ndp / (L.a_ndp + L.a_ucp)
    L["catch_share"] = L.c_ndp / (L.c_ndp + L.c_ucp)
    write_csv(L[["ed", "name", "complete", "a_ndp", "a_ucp", "c_ndp", "c_ucp", "c_gap", "c_valid", "n_vas", "adv_share", "catch_share"]], "advance_locations_2023.csv")
    L = L[L.groupby("ed").ed.transform("size") >= 2]
    w = (L.a_ndp + L.a_ucp).values
    out["locations_used"] = int(len(L)); out["divisions_used"] = int(L.ed.nunique())
    out["divisions_with_all_locations_geocoded"] = int(L[L.complete].ed.nunique())
    out["slope_all"] = fe_slope(logit(L.catch_share), logit(L.adv_share), w, L.ed)
    C = L[L.complete]
    out["slope_complete_divisions"] = fe_slope(logit(C.catch_share), logit(C.adv_share), (C.a_ndp + C.a_ucp).values, C.ed)
    # volume: does a location's share of the division's advance ballots follow election-day votes or the turnout gap?
    for c in ("c_valid", "c_gap"):
        L[c + "_sh"] = L[c] / L.groupby("ed")[c].transform("sum")
    L["A_sh"] = (L.a_ndp + L.a_ucp) / (L.a_ndp + L.a_ucp).groupby(L.ed).transform("sum")
    X, Y = (L.c_gap_sh - L.c_valid_sh).values, (L.A_sh - L.c_valid_sh).values
    out["volume"] = {"lambda": round(float(np.sum(X * Y) / np.sum(X * X)), 3),
                     "corr_location_share_with_eday_vote_share": round(float(np.corrcoef(L.A_sh, L.c_valid_sh)[0, 1]), 3),
                     "corr_location_share_with_gap_share": round(float(np.corrcoef(L.A_sh, L.c_gap_sh)[0, 1]), 3),
                     "note": "nearest-poll catchments are a poor guide to how many people use a poll; read with care"}

    def loss(k, D):
        A = (D.a_ndp + D.a_ucp).sum()
        ps, ts, ww = D[f"{k}_n"] / (D[f"{k}_n"] + D[f"{k}_u"]), D.adv_share, D.a_ndp + D.a_ucp
        return {"share_rmse_pts": round(100 * float(np.sqrt((ww * (ps - ts) ** 2).sum() / ww.sum())), 2),
                "ballots_put_at_wrong_location_pct": round(100 * float(0.5 * ((D[f"{k}_n"] - D.a_ndp).abs() + (D[f"{k}_u"] - D.a_ucp).abs()).sum() / A), 2)}
    out["hide_and_predict_all"] = {k.lower(): loss(k, L) for k in ("M0", "M1", "M2")}
    out["grid_share_rmse_pts"] = [{"beta": b_, "lam": l_, "share_rmse_pts": loss(f"G({b_},{l_})", L)["share_rmse_pts"]} for b_ in BETAS for l_ in LAMS]
    out["divisions_where_m1_share_error_below_m0"] = int(sum(
        ((d.a_ndp + d.a_ucp) * (d.M1_n / (d.M1_n + d.M1_u) - d.adv_share) ** 2).sum() < ((d.a_ndp + d.a_ucp) * (d.M0_n / (d.M0_n + d.M0_u) - d.adv_share) ** 2).sum()
        for _, d in L.groupby("ed")))
    # by region
    names = t.drop_duplicates("ed").set_index("ed").name
    L["region"] = L.ed.map(names).map(region_of)
    out["slope_by_region"] = [{"region": r, **fe_slope(logit(d.catch_share), logit(d.adv_share), (d.a_ndp + d.a_ucp).values, d.ed)} for r, d in L.groupby("region") if d.ed.nunique() >= 4]
    return out


def part_b():
    raw = pd.read_csv(OUT / "polls_2015_parsed.csv", dtype={"ed": str})
    rows = []
    stop = {"ADVANCE", "POLL", "THE", "OF", "AND", "NORTH", "SOUTH", "EAST", "WEST", "RURAL", "CENTRAL", "CENTRE", "TOWN", "VILLAGE", "LAKE", "RIVER",
            "FORT", "ST", "PARK", "HALL", "COUNTY", "CITY", "MOUNTAIN", "CREEK", "VALLEY", "HILLS", "HILL", "GROVE", "RED", "DEER", "GRANDE", "PRAIRIE",
            "CALGARY", "EDMONTON", "LETHBRIDGE", "MEDICINE", "HAT", "SPRUCE", "STONY", "PLAIN", "SHERWOOD", "ALBERT", "MCMURRAY", "AIRDRIE", "LEDUC"}
    for ed, d in raw.groupby("ed"):
        adv, ev = d[d.k == "advance"], d[d.k == "eday"]
        toks = {}
        for r in adv.itertuples():
            tk = [x for x in re.split(r"[^A-Z]+", r.poll.upper().replace("ADVANCE", "")) if len(x) >= 4 and x not in stop]
            # also drop tokens that are part of the division's own name (they match everything)
            tk = [x for x in tk if x not in re.split(r"[^A-Z]+", str(r.name).upper())]
            if tk:
                toks.setdefault(" ".join(tk), []).append(r)
        if len(toks) < 2:
            continue
        for key, rs in toks.items():
            pat = key.split()
            m = ev[ev.poll.str.upper().apply(lambda s: all(p in s for p in pat))]
            if len(m) == 0 or (m.ndp + m.ucp).sum() < 50:
                continue
            an, au = sum(r.ndp for r in rs), sum(r.ucp for r in rs)
            if an + au < 50:
                continue
            rows.append(dict(ed=ed, place=key, a_ndp=an, a_ucp=au, c_ndp=m.ndp.sum(), c_ucp=m.ucp.sum(), eday_polls=len(m)))
    L = pd.DataFrame(rows)
    L = L[L.groupby("ed").ed.transform("size") >= 2]
    L["adv_share"], L["catch_share"] = L.a_ndp / (L.a_ndp + L.a_ucp), L.c_ndp / (L.c_ndp + L.c_ucp)
    write_csv(L, "advance_places_2015.csv")
    out = {"places_matched": int(len(L)), "divisions": int(L.ed.nunique()),
           "slope": fe_slope(logit(L.catch_share), logit(L.adv_share), (L.a_ndp + L.a_ucp).values, L.ed)}
    # error of "every advance poll shows the division's advance mix" (M0) against "division shift plus the town's own lean" (beta = 1)
    tot = L.groupby("ed")[["a_ndp", "a_ucp", "c_ndp", "c_ucp"]].transform("sum")
    m0 = tot.a_ndp / (tot.a_ndp + tot.a_ucp)
    shift = logit(m0) - logit(tot.c_ndp / (tot.c_ndp + tot.c_ucp))
    b1 = 1 / (1 + np.exp(-(logit(L.catch_share) + shift)))
    w = L.a_ndp + L.a_ucp
    out["share_rmse_pts"] = {"m0_one_mix_per_division": round(100 * float(np.sqrt((w * (m0 - L.adv_share) ** 2).sum() / w.sum())), 2),
                             "beta1_town_lean_plus_division_shift": round(100 * float(np.sqrt((w * (b1 - L.adv_share) ** 2).sum() / w.sum())), 2)}
    return out


def main():
    res = {"located_polls_2023": part_a(), "town_polls_2015": part_b()}
    write_json("provincial_location_tests.json", res, __file__,
               [WORKBOOK_2023, VA_EDAY, INPUTS / "advance_poll_geocodes.csv", OUT / "polls_2015_parsed.csv"])
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
