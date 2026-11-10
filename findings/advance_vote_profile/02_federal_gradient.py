"""A test with a known answer: federal advance polls in Alberta (exploratory, not registered).

Elections Canada reports advance polls for small "advance polling districts".
Each one is a fixed group of ordinary polling divisions, and the published
polling-division file says which. So inside every Alberta federal riding we
know the true advance vote of each group of polls. The provincial results give
no such thing.

The test: hide the advance-district counts, keep only the riding's advance
total (what Elections Alberta gives us provincially), spread it over polling
divisions with each candidate rule, add up to advance districts, and compare
with the truth.

Party pair: Conservative against Liberal + NDP (the closest federal analogue of
UCP against NDP in Alberta).

Inputs are downloaded on first run into AVP_FED_DIR (default cache/federal):
  elections.ca  poll-by-poll results, 34 Alberta ridings, 2021 (and 2019)
  ftp.maps.canada.ca  polling-division attribute table (PD -> advance poll)
Writes outputs/federal_alberta_advance_districts_<year>.csv, outputs/federal_gradient.json

Usage: python findings/advance_vote_profile/02_federal_gradient.py
"""
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

import _models as M
from _common import CACHE, OUT, logit

FED = Path(os.environ.get("AVP_FED_DIR", CACHE / "federal"))
FED.mkdir(parents=True, exist_ok=True)
RES = {2021: "https://www.elections.ca/res/rep/off/ovr2021app/53/data_donnees/pollresults_resultatsbureau{}.csv",
       2019: "https://www.elections.ca/res/rep/off/ovr2019app/51/data_donnees/pollresults_resultatsbureau{}.csv"}
PD = {2021: "https://ftp.maps.canada.ca/pub/elections_elections/Electoral-districts_Circonscription-electorale/Elections_Canada_2021/PD_CA_2021_EN.zip",
      2019: "https://ftp.maps.canada.ca/pub/elections_elections/Electoral-districts_Circonscription-electorale/Elections_Canada_2019/polling_divisions_boundaries_2019.shp.zip"}
COLS = ["fed", "name", "namef", "ps", "psname", "void", "nopoll", "mergewith", "rej", "electors", "fam", "mid", "first",
        "party", "partyf", "inc", "elected", "votes"]
BETAS = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
LAMS = [0, 0.25, 0.5, 0.75, 1.0]


def get(url, dest):
    if not dest.exists() or dest.stat().st_size < 1000:
        subprocess.run(["curl", "-sL", "-m", "1200", "-A", "research-client/1.0", "-o", str(dest), url], check=False)
    return dest.exists() and dest.stat().st_size > 1000


def pd_map(year):
    f = FED / f"pd_map_{year}_alberta.csv"
    if f.exists():
        return pd.read_csv(f)
    z = FED / f"PD_{year}.zip"
    if not get(PD[year], z) or not zipfile.is_zipfile(z):
        return None
    import geopandas as gpd
    with zipfile.ZipFile(z) as zz:
        dbf = [n for n in zz.namelist() if n.lower().endswith(".dbf")][0]
        zz.extract(dbf, FED)
    d = gpd.read_file(FED / dbf, ignore_geometry=True)
    d.columns = [c.upper() for c in d.columns]
    fedc = [c for c in d.columns if c.startswith("FED") and "NUM" in c][0]
    advc = [c for c in d.columns if c.startswith("ADV")][0]
    pdc = "PD_NUM" if "PD_NUM" in d.columns else "PDNUM"
    d[pdc] = pd.to_numeric(d[pdc], errors="coerce")
    d = d[(d[fedc] // 1000) == 48][[fedc, pdc, advc]].drop_duplicates()
    d.columns = ["fed", "pd", "adv"]
    d["adv"] = pd.to_numeric(d.adv, errors="coerce")
    d = d.dropna().astype(int).drop_duplicates(["fed", "pd"])
    d.to_csv(f, index=False)
    return d


def polls(year):
    frames = []
    for i in range(48001, 48035):
        f = FED / f"f{year}_{i}.csv"
        if not get(RES[year].format(i), f):
            return None
        d = pd.read_csv(f)
        d.columns = COLS
        frames.append(d)
    d = pd.concat(frames)
    d["ps"] = d.ps.astype(str).str.strip()
    d["bloc"] = np.where(d.party == "Conservative", "con", np.where(d.party.isin(["Liberal", "NDP-New Democratic Party"]), "lib_ndp", "other"))
    p = d.pivot_table(index=["fed", "ps"], columns="bloc", values="votes", aggfunc="sum").fillna(0).reset_index()
    meta = d.drop_duplicates(["fed", "ps"])[["fed", "ps", "electors", "mergewith", "void"]]
    p = p.merge(meta, on=["fed", "ps"])
    p["num"] = pd.to_numeric(p.ps.str.extract(r"^(\d+)")[0], errors="coerce")
    return p


def build(year):
    """One row per ordinary polling division (PD) and one per advance district, Alberta."""
    m, p = pd_map(year), polls(year)
    if m is None or p is None:
        return None, None
    ordn = p[p.num.notna() & (p.num < 400)].copy()
    ordn["pd"] = ordn.num.astype(int)
    # a poll merged with another reports no votes of its own: move its electors to the poll that holds the votes
    tgt = pd.to_numeric(ordn.mergewith.astype(str).str.extract(r"^(\d+)")[0], errors="coerce")
    ordn["pd_eff"] = np.where(tgt.notna(), tgt, ordn.pd).astype(int)
    pdv = ordn.groupby(["fed", "pd_eff"])[["con", "lib_ndp", "other", "electors"]].sum().reset_index().rename(columns={"pd_eff": "pd"})
    pdv = pdv.merge(m, on=["fed", "pd"], how="left")
    adv = p[p.num.notna() & (p.num >= 600) & (p.num < 700)].copy()
    adv["adv"] = adv.num.astype(int)
    advv = adv.groupby(["fed", "adv"])[["con", "lib_ndp", "other"]].sum().reset_index()
    advv.columns = ["fed", "adv", "a_con", "a_lib_ndp", "a_other"]
    return pdv, advv


def score_riding(pdv, advv, rule):
    """rule(e_n, e_u, gap, A_n, A_u) -> per-PD allocation. 'n' = Liberal+NDP, 'u' = Conservative."""
    g = pdv.dropna(subset=["adv"])
    n, u = rule(g.lib_ndp.values, g.con.values, (g.electors - g.con - g.lib_ndp - g.other).values, advv.a_lib_ndp.sum(), advv.a_con.sum())
    pred = pd.DataFrame({"adv": g.adv.values.astype(int), "pn": n, "pu": u}).groupby("adv").sum()
    t = advv.set_index("adv").join(pred, how="left").fillna(0)
    return t


def losses(t):
    A = (t.a_con + t.a_lib_ndp).sum()
    misplaced = 0.5 * ((t.pn - t.a_lib_ndp).abs() + (t.pu - t.a_con).abs()).sum()
    ps = t.pn / (t.pn + t.pu).replace(0, np.nan)
    ts = t.a_lib_ndp / (t.a_lib_ndp + t.a_con).replace(0, np.nan)
    w = t.a_con + t.a_lib_ndp
    ok = ps.notna() & ts.notna()
    se_share = float((w[ok] * (ps[ok] - ts[ok]) ** 2).sum())
    vol = 0.5 * ((t.pn + t.pu) - w).abs().sum()
    return dict(A=float(A), misplaced=float(misplaced), se_share=se_share, w=float(w[ok].sum()), vol=float(vol))


def run_year(year):
    pdv, advv = build(year)
    if pdv is None:
        return {"available": False}
    matched = pdv.adv.notna()
    out = {"available": True, "ridings": int(pdv.fed.nunique()), "polling_divisions": int(len(pdv)), "pd_matched_to_advance_district_pct": round(100 * matched.mean(), 2),
           "advance_districts": int(len(advv))}
    # descriptive table per advance district
    g = pdv.dropna(subset=["adv"]).assign(adv=lambda d: d.adv.astype(int)).groupby(["fed", "adv"])[["con", "lib_ndp", "other", "electors"]].sum().reset_index()
    t = advv.merge(g, on=["fed", "adv"], how="inner")
    t = t[(t.con + t.lib_ndp > 50) & (t.a_con + t.a_lib_ndp > 50)]
    t["eday_share"] = t.lib_ndp / (t.lib_ndp + t.con)
    t["adv_share"] = t.a_lib_ndp / (t.a_lib_ndp + t.a_con)
    t.to_csv(OUT / f"federal_alberta_advance_districts_{year}.csv", index=False)
    e, a = t.lib_ndp.sum() / (t.lib_ndp + t.con).sum(), t.a_lib_ndp.sum() / (t.a_lib_ndp + t.a_con).sum()
    out["alberta_lib_ndp_share_of_three_party_pct"] = {"election_day": round(100 * e, 2), "advance": round(100 * a, 2), "skew_pts": round(100 * (a - e), 2)}
    out["advance_two_bloc_votes"] = int((t.a_lib_ndp + t.a_con).sum())
    out["advance_share_of_eday_plus_advance_pct"] = round(100 * (t.a_lib_ndp + t.a_con).sum() / (t.a_lib_ndp + t.a_con + t.lib_ndp + t.con).sum(), 1)
    # 1. slope inside ridings: advance log-odds on election-day log-odds, riding fixed effects
    x, y, w = logit(t.eday_share), logit(t.adv_share), (t.a_lib_ndp + t.a_con).values
    xd = x - pd.Series(x).groupby(t.fed.values).transform(lambda s: np.average(s, weights=w[s.index])).values
    yd = y - pd.Series(y).groupby(t.fed.values).transform(lambda s: np.average(s, weights=w[s.index])).values
    b = float(np.sum(w * xd * yd) / np.sum(w * xd * xd))
    # cluster-robust SE by riding
    res = yd - b * xd
    cl = pd.Series(w * xd * res).groupby(t.fed.values).sum()
    se = float(np.sqrt((cl ** 2).sum()) / np.sum(w * xd * xd))
    out["within_riding_slope_beta"] = {"beta": round(b, 3), "se_clustered_by_riding": round(se, 3), "n_districts": int(len(t)),
                                       "corr_within": round(float(np.corrcoef(xd, yd)[0, 1]), 3)}
    perr = {}
    for fed, s in t.groupby("fed"):
        if len(s) >= 4:
            ww = (s.a_lib_ndp + s.a_con).values
            xx, yy = logit(s.eday_share), logit(s.adv_share)
            xx, yy = xx - np.average(xx, weights=ww), yy - np.average(yy, weights=ww)
            if np.sum(ww * xx * xx) > 0:
                perr[fed] = float(np.sum(ww * xx * yy) / np.sum(ww * xx * xx))
    pv = pd.Series(perr)
    out["within_riding_slope_beta"]["per_riding_quantiles_10_25_50_75_90"] = [round(float(q), 2) for q in pv.quantile([0.1, 0.25, 0.5, 0.75, 0.9])]
    out["within_riding_slope_beta"]["per_riding_mean"] = round(float(pv.mean()), 3)
    out["within_riding_slope_beta"]["per_riding_sd"] = round(float(pv.std()), 3)
    out["within_riding_slope_beta"]["ridings_with_beta_below_0.5"] = int((pv < 0.5).sum())
    # by urban / rural riding (riding number ranges are not geographic, so use the riding name)
    # 2. where the advance ballots are: share of the riding's advance ballots against shares of election-day votes and of the gap
    t["A"] = t.a_con + t.a_lib_ndp + t.a_other
    t["V"] = t.con + t.lib_ndp + t.other
    t["G"] = (t.electors - t.V).clip(lower=0)
    for c in ("A", "V", "G", "electors"):
        t[c + "_sh"] = t[c] / t.groupby("fed")[c].transform("sum")
    X = (t.G_sh - t.V_sh).values
    Y = (t.A_sh - t.V_sh).values
    lam = float(np.sum(X * Y) / np.sum(X * X))
    r = Y - lam * X
    cl = pd.Series(X * r).groupby(t.fed.values).sum()
    out["volume_lambda"] = {"lambda": round(lam, 3), "se_clustered_by_riding": round(float(np.sqrt((cl ** 2).sum()) / np.sum(X * X)), 3),
                            "reading": "advance share = (1-lambda) x election-day-vote share + lambda x turnout-gap share",
                            "mean_abs_error_pts_of_riding_advance": {"lam0_eday_votes": round(100 * float(np.abs(t.A_sh - t.V_sh).mean()), 3),
                                                                      "lam1_turnout_gap": round(100 * float(np.abs(t.A_sh - t.G_sh).mean()), 3),
                                                                      "electors": round(100 * float(np.abs(t.A_sh - t.electors_sh).mean()), 3),
                                                                      "fitted": round(100 * float(np.abs(Y - lam * X).mean()), 3)}}
    # how much total turnout (election day + advance) varies between districts of one riding: truth against each rule
    At = t.groupby("fed").A.transform("sum")
    sd = lambda adv_: float(((t.V + adv_) / t.electors).groupby(t.fed).std().median())
    out["within_riding_sd_of_total_turnout_pts"] = {"truth": round(100 * sd(t.A), 2), "implied_by_M0_weights": round(100 * sd(t.V_sh * At), 2),
                                                    "implied_by_turnout_gap_weights": round(100 * sd(t.G_sh * At), 2),
                                                    "election_day_only": round(100 * sd(0 * t.A), 2)}
    lr = {}
    for fed, s in t.groupby("fed"):
        xx, yy = (s.G_sh - s.V_sh).values, (s.A_sh - s.V_sh).values
        if len(s) >= 4 and np.sum(xx * xx) > 0:
            lr[fed] = float(np.sum(xx * yy) / np.sum(xx * xx))
    lr = pd.Series(lr)
    out["volume_lambda"]["per_riding_quantiles_10_25_50_75_90"] = [round(float(q), 2) for q in lr.quantile([0.1, 0.25, 0.5, 0.75, 0.9])]
    out["volume_lambda"]["per_riding_sd"] = round(float(lr.std()), 3)
    # 3. full hide-and-predict test of each rule, and a grid over the general family
    feds = sorted(set(pdv.fed) & set(advv.fed))
    rules = {"M0": M.m0, "M1": M.m1, "M2": M.m2}
    for b_ in BETAS:
        for l_ in LAMS:
            rules[f"G({b_},{l_})"] = (lambda b_, l_: lambda en, eu, gp, An, Au: M.general(en, eu, gp, An, Au, b_, l_, shrink_k=10))(b_, l_)
    per = {k: {} for k in rules}
    for fed in feds:
        pv_, av_ = pdv[pdv.fed == fed], advv[advv.fed == fed]
        av_ = av_[av_.adv.isin(pv_.adv.dropna().astype(int))]
        for k, rule in rules.items():
            per[k][fed] = losses(score_riding(pv_, av_, rule))

    def agg(k, sub=None):
        L = [v for f, v in per[k].items() if sub is None or f in sub]
        A = sum(x["A"] for x in L)
        return {"ballots_put_in_wrong_district_pct": round(100 * sum(x["misplaced"] for x in L) / A, 2),
                "share_rmse_pts": round(100 * float(np.sqrt(sum(x["se_share"] for x in L) / sum(x["w"] for x in L))), 2),
                "volume_error_pct": round(100 * sum(x["vol"] for x in L) / A, 2)}
    out["hide_and_predict"] = {k: agg(k) for k in ("M0", "M1", "M2")}
    grid = {k: agg(k) for k in rules if k.startswith("G(")}
    out["grid"] = grid
    best = min(grid, key=lambda k: grid[k]["ballots_put_in_wrong_district_pct"])
    best_s = min(grid, key=lambda k: grid[k]["share_rmse_pts"])
    out["best_in_grid"] = {"by_ballots_misplaced": best, **{"misplaced_" + kk: vv for kk, vv in grid[best].items()}, "by_share_rmse": best_s}
    # leave-one-riding-out: choose (beta, lam) on the other ridings, score on the held-out riding
    gk = [k for k in rules if k.startswith("G(")]
    tot = {"A": 0.0, "misplaced": 0.0, "se": 0.0, "w": 0.0}
    picks = {}
    for fed in feds:
        others = [f for f in feds if f != fed]
        pick = min(gk, key=lambda k: sum(per[k][f]["misplaced"] for f in others))
        picks[pick] = picks.get(pick, 0) + 1
        x = per[pick][fed]
        tot["A"] += x["A"]; tot["misplaced"] += x["misplaced"]; tot["se"] += x["se_share"]; tot["w"] += x["w"]
    out["leave_one_riding_out"] = {"picks": picks, "ballots_put_in_wrong_district_pct": round(100 * tot["misplaced"] / tot["A"], 2),
                                   "share_rmse_pts": round(100 * float(np.sqrt(tot["se"] / tot["w"])), 2)}
    # ridings where each rule beats M0
    out["ridings_where_rule_beats_M0"] = {k: int(sum(per[k][f]["misplaced"] < per["M0"][f]["misplaced"] for f in feds)) for k in ("M1", "M2", best)}
    out["ridings_scored"] = len(feds)
    return out


def main():
    res = {str(y): run_year(y) for y in (2021, 2019)}
    (OUT / "federal_gradient.json").write_text(json.dumps(res, indent=1))
    for y, r in res.items():
        print("==", y, {k: v for k, v in r.items() if k not in ("grid",)})
        if r.get("available"):
            g = r["grid"]
            print("   ballots put in the wrong advance district, % (rows beta, cols lam)", LAMS)
            for b_ in BETAS:
                print("   ", b_, [g[f"G({b_},{l_})"]["ballots_put_in_wrong_district_pct"] for l_ in LAMS])
            print("   share RMSE, points")
            for b_ in BETAS:
                print("   ", b_, [g[f"G({b_},{l_})"]["share_rmse_pts"] for l_ in LAMS])


if __name__ == "__main__":
    main()
