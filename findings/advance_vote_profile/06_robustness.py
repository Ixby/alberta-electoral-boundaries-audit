"""How firm is "about one for one"? Other specifications, placebos, leverage, coverage (exploratory, not registered).

Reads only this folder's own outputs and inputs:
  outputs/federal_alberta_advance_districts_<year>.csv, outputs/advance_locations_2023.csv,
  inputs/advance_poll_geocodes.csv, and the 2023 workbook.
Writes outputs/robustness.json. Seed 20261110.

Follows checks first run by the independent verifier (audit2/verify-advance.json), rebuilt here.

Usage: python findings/advance_vote_profile/06_robustness.py
"""
import json

import numpy as np
import pandas as pd

from _common import INPUTS, OUT, load_2023_rows, logit

SEED = 20261110


def fe(g, x, y, w):
    """Slope of y on x with group fixed effects, weights w, SE clustered by group. Returns b, se, xd, yd."""
    g, x, y, w = np.asarray(g), np.asarray(x, float), np.asarray(y, float), np.asarray(w, float)
    sw = pd.Series(w).groupby(g).transform("sum").values
    xd = x - pd.Series(w * x).groupby(g).transform("sum").values / sw
    yd = y - pd.Series(w * y).groupby(g).transform("sum").values / sw
    b = np.sum(w * xd * yd) / np.sum(w * xd * xd)
    cl = pd.Series(w * xd * (yd - b * xd)).groupby(g).sum()
    return float(b), float(np.sqrt((cl ** 2).sum()) / np.sum(w * xd * xd)), xd, yd


def permute_within(g, y, rng):
    yp = y.copy()
    for _, ix in pd.Series(np.arange(len(g))).groupby(np.asarray(g)).indices.items():
        yp[ix] = y[rng.permutation(ix)]
    return yp


def federal(year, rng):
    t = pd.read_csv(OUT / f"federal_alberta_advance_districts_{year}.csv").reset_index(drop=True)
    w = (t.a_lib_ndp + t.a_con).values.astype(float)
    xs, ys = t.eday_share.values, t.adv_share.values
    x, y = logit(xs), logit(ys)
    b, se, xd, yd = fe(t.fed, x, y, w)
    bu, seu, _, _ = fe(t.fed, x, y, np.ones(len(t)))
    bs, ses, _, _ = fe(t.fed, xs, ys, w)
    bsu, sesu, _, _ = fe(t.fed, xs, ys, np.ones(len(t)))
    rev = float(np.sum(w * yd * yd) / np.sum(w * xd * yd))
    pl = [fe(t.fed, x, permute_within(t.fed.values, y, rng), w)[0] for _ in range(200)]
    return {"log_odds_weighted": [round(b, 3), round(se, 3)], "log_odds_unweighted": [round(bu, 3), round(seu, 3)],
            "share_scale_weighted": [round(bs, 3), round(ses, 3)], "share_scale_unweighted": [round(bsu, 3), round(sesu, 3)],
            "reverse_regression_upper_bound": round(rev, 3),
            "placebo_permute_advance_results_within_riding": {"draws": 200, "mean": round(float(np.mean(pl)), 3), "sd": round(float(np.std(pl)), 3),
                                                               "max": round(float(np.max(pl)), 3)}}


def provincial(rng):
    L = pd.read_csv(OUT / "advance_locations_2023.csv", dtype={"ed": str})
    L = L[L.groupby("ed").ed.transform("size") >= 2].reset_index(drop=True)
    x, y, w = logit(L.catch_share), logit(L.adv_share), (L.a_ndp + L.a_ucp).values.astype(float)
    b, se, xd, yd = fe(L.ed, x, y, w)
    out = {"polls": int(len(L)), "divisions": int(L.ed.nunique()), "log_odds_weighted": [round(b, 3), round(se, 3)]}
    bu, seu, _, _ = fe(L.ed, x, y, np.ones(len(L)))
    bs, ses, _, _ = fe(L.ed, L.catch_share.values, L.adv_share.values, w)
    out["log_odds_unweighted"], out["share_scale_weighted"] = [round(bu, 3), round(seu, 3)], [round(bs, 3), round(ses, 3)]
    lev = pd.Series(w * xd * xd).groupby(L.ed.values).sum().sort_values(ascending=False)
    lev = lev / lev.sum()
    names = {r.ed: r.name for r in L.itertuples()}
    out["leverage_share_top5"] = {k: round(float(v), 3) for k, v in lev.head(5).items()}
    out["leverage_top2_share"] = round(float(lev.head(2).sum()), 3)
    out["top2_divisions_example_polls"] = {k: L[L.ed == k].name.tolist() for k in lev.head(2).index}
    top2 = list(lev.head(2).index)
    for drop in ([top2[0]], [top2[1]], top2):
        d = L[~L.ed.isin(drop)]
        bb, ss, _, _ = fe(d.ed, logit(d.catch_share), logit(d.adv_share), (d.a_ndp + d.a_ucp).values)
        out["drop_" + "_".join(drop)] = [round(bb, 3), round(ss, 3)]
    eds = L.ed.unique()
    jk = []
    for e in eds:
        m = (L.ed != e).values
        jk.append(fe(L.ed[m], x[m], y[m], w[m])[0])
    out["leave_one_division_out_range"] = [round(min(jk), 3), round(max(jk), 3)]
    boot = []
    for _ in range(2000):
        pick = rng.choice(eds, len(eds))
        d = pd.concat([L[L.ed == e].assign(g=i) for i, e in enumerate(pick)])
        boot.append(fe(d.g, logit(d.catch_share), logit(d.adv_share), (d.a_ndp + d.a_ucp).values)[0])
    out["cluster_bootstrap_95pct"] = [round(float(q), 2) for q in np.percentile(boot, [2.5, 97.5])]
    pos = sum(np.corrcoef(logit(d.catch_share), logit(d.adv_share))[0, 1] > 0 for _, d in L.groupby("ed"))
    out["divisions_with_positive_within_relation"] = [int(pos), int(L.ed.nunique())]
    # placebo 1: shuffle advance results among a division's polls
    pl = [fe(L.ed, x, permute_within(L.ed.values, y, rng), w)[0] for _ in range(500)]
    out["placebo_permute_within_division"] = {"draws": 500, "mean": round(float(np.mean(pl)), 3), "sd": round(float(np.std(pl)), 3)}
    # placebo 2: make M0 true. Every poll draws its ballots from the division's one advance mix.
    tot = L.groupby("ed")[["a_ndp", "a_ucp"]].transform("sum")
    p0 = (tot.a_ndp / (tot.a_ndp + tot.a_ucp)).values
    sim = [fe(L.ed, x, logit(rng.binomial(w.astype(int), p0) / w), w)[0] for _ in range(500)]
    out["placebo_M0_true_simulation"] = {"draws": 500, "mean": round(float(np.mean(sim)), 3), "sd": round(float(np.std(sim)), 3)}
    # coverage
    raw = load_2023_rows()
    adv = raw[raw.kind == "Advance"]
    out["coverage"] = {"in_division_advance_two_party_ballots": int((adv.ndp + adv.ucp).sum()), "in_tested_polls": int(w.sum()),
                       "pct": round(100 * float(w.sum() / (adv.ndp + adv.ucp).sum()), 1), "divisions_tested": int(L.ed.nunique()), "divisions_total": 87,
                       "untested_vote_anywhere_and_special_two_party_ballots": int(raw[raw.kind.isin(["Vote Anywhere", "Special Ballot"])][["ndp", "ucp"]].sum().sum())}
    gc = pd.read_csv(INPUTS / "advance_poll_geocodes.csv", dtype={"ed": str})
    miss = gc[gc.lat.isna()]
    out["unlocated_polls"] = {"in_file": int(len(gc)), "not_found": int(len(miss)), "name_contains_Returning": int(miss.name.str.contains("Returning").sum()),
                              "multi_site_rows_placed_at_first_name": int(gc[gc.lat.notna() & (gc["query"] != gc.name)].shape[0])}
    return out


def main():
    rng = np.random.default_rng(SEED)
    res = {"seed": SEED, "federal_2021": federal(2021, rng), "federal_2019": federal(2019, rng), "provincial_2023": provincial(rng)}
    (OUT / "robustness.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
