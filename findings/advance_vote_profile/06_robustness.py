"""How firm is the provincial lean estimate? Other specifications, placebos, leverage, coverage, and the
size of P's own error on the located polls (exploratory, not registered). Provincial data only.

Reads this folder's outputs/advance_locations_2023.csv, inputs/advance_poll_geocodes.csv and the 2023 workbook.
Writes outputs/robustness.json. Seed 20261110 (bootstrap and placebos).

Usage: python findings/advance_vote_profile/06_robustness.py
"""
import numpy as np
import pandas as pd

from _common import INPUTS, OUT, WORKBOOK_2023, load_2023_rows, logit, write_json

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


def provincial(rng):
    L = pd.read_csv(OUT / "advance_locations_2023.csv", dtype={"ed": str})
    L = L[L.groupby("ed").ed.transform("size") >= 2].reset_index(drop=True)
    x, y, w = logit(L.catch_share), logit(L.adv_share), (L.a_ndp + L.a_ucp).values.astype(float)
    b, se, xd, yd = fe(L.ed, x, y, w)
    out = {"polls": int(len(L)), "divisions": int(L.ed.nunique()), "log_odds_weighted": [round(b, 3), round(se, 3)]}
    bu, seu, _, _ = fe(L.ed, x, y, np.ones(len(L)))
    bs, ses, _, _ = fe(L.ed, L.catch_share.values, L.adv_share.values, w)
    out["log_odds_unweighted"], out["share_scale_weighted"] = [round(bu, 3), round(seu, 3)], [round(bs, 3), round(ses, 3)]
    out["reverse_regression_upper_bound"] = round(float(np.sum(w * yd * yd) / np.sum(w * xd * yd)), 3)
    lev = pd.Series(w * xd * xd).groupby(L.ed.values).sum().sort_values(ascending=False)
    lev = lev / lev.sum()
    out["leverage_top5"] = [{"division": k, "share": round(float(v), 3), "polls": L[L.ed == k].name.tolist()} for k, v in lev.head(5).items()]
    out["leverage_top2_share"] = round(float(lev.head(2).sum()), 3)
    top2 = list(lev.head(2).index)
    for tag, drop in (("drop_top1", [top2[0]]), ("drop_second", [top2[1]]), ("drop_top2", top2)):
        d = L[~L.ed.isin(drop)]
        bb, ss, _, _ = fe(d.ed, logit(d.catch_share), logit(d.adv_share), (d.a_ndp + d.a_ucp).values)
        out[tag] = [round(bb, 3), round(ss, 3)]
    out["dropped_divisions"] = top2
    eds = L.ed.unique()
    jk = [fe(L.ed[(L.ed != e).values], x[(L.ed != e).values], y[(L.ed != e).values], w[(L.ed != e).values])[0] for e in eds]
    out["leave_one_division_out_range"] = [round(min(jk), 3), round(max(jk), 3)]
    boot = []
    for _ in range(2000):
        pick = rng.choice(eds, len(eds))
        d = pd.concat([L[L.ed == e].assign(g=i) for i, e in enumerate(pick)])
        boot.append(fe(d.g, logit(d.catch_share), logit(d.adv_share), (d.a_ndp + d.a_ucp).values)[0])
    out["cluster_bootstrap_draws"] = 2000
    out["cluster_bootstrap_95pct"] = [round(float(q), 2) for q in np.percentile(boot, [2.5, 97.5])]
    pos = sum(np.corrcoef(logit(d.catch_share), logit(d.adv_share))[0, 1] > 0 for _, d in L.groupby("ed"))
    out["divisions_with_positive_within_relation"] = [int(pos), int(L.ed.nunique())]
    pl = [fe(L.ed, x, permute_within(L.ed.values, y, rng), w)[0] for _ in range(500)]
    out["placebo_permute_within_division"] = {"draws": 500, "mean": round(float(np.mean(pl)), 3), "sd": round(float(np.std(pl)), 3)}
    tot = L.groupby("ed")[["a_ndp", "a_ucp"]].transform("sum")
    p0 = (tot.a_ndp / (tot.a_ndp + tot.a_ucp)).values
    sim = [fe(L.ed, x, logit(rng.binomial(w.astype(int), p0) / w), w)[0] for _ in range(500)]
    out["placebo_m0_true_simulation"] = {"draws": 500, "mean": round(float(np.mean(sim)), 3), "sd": round(float(np.std(sim)), 3)}

    # P's own error at the located polls: scatter of a poll's early log-odds around the line with beta = 1,
    # beyond what counting alone gives; and scatter of its ballot count around P's count side.
    r = yd - 1.0 * xd
    p = L.adv_share.values
    tot_var, samp_var = np.average(r ** 2, weights=w), np.average(1 / (w * p * (1 - p)), weights=w)
    A_sh = (L.a_ndp + L.a_ucp) / (L.a_ndp + L.a_ucp).groupby(L.ed).transform("sum")
    G_sh = L.c_gap / L.c_gap.groupby(L.ed).transform("sum")
    out["residual_at_located_polls"] = {
        "share_residual_sd_log_odds": round(float(np.sqrt(tot_var)), 4), "counting_error_sd_log_odds": round(float(np.sqrt(samp_var)), 4),
        "excess_sd_log_odds": round(float(np.sqrt(max(tot_var - samp_var, 0))), 4),
        "count_residual_sd_log": round(float(np.log(A_sh / G_sh).std()), 4),
        "median_two_party_ballots_per_poll": float(np.median(w)),
        "sound_as_station_level_error_model": False,
        "why_not": ["a poll's catchment is a guess (nearest poll); an elector may use any advance poll, so the scatter mixes "
                    "catchment error with the rule's own error", "a poll's count depends on its hours and size, not only on who lives near it",
                    "polls are larger than stations and cover 45% of in-division advance ballots in 54 divisions; no provincial data "
                    "show how the error scales down to a station or whether neighbouring stations err together"]}
    raw = load_2023_rows()
    adv = raw[raw.kind == "Advance"]
    out["coverage"] = {"in_division_advance_two_party_ballots": int((adv.ndp + adv.ucp).sum()), "in_tested_polls": int(w.sum()),
                       "pct": round(100 * float(w.sum() / (adv.ndp + adv.ucp).sum()), 1), "divisions_tested": int(L.ed.nunique()), "divisions_total": 87,
                       "untested_vote_anywhere_and_special_two_party_ballots": int(raw[raw.kind.isin(["Vote Anywhere", "Special Ballot"])][["ndp", "ucp"]].sum().sum())}
    gc = pd.read_csv(INPUTS / "advance_poll_geocodes.csv", dtype={"ed": str})
    miss = gc[gc.lat.isna()]
    out["unlocated_polls"] = {"in_file": int(len(gc)), "not_found": int(len(miss)), "name_contains_returning": int(miss.name.str.contains("Returning").sum()),
                              "multi_site_rows_placed_at_first_name": int(gc[gc.lat.notna() & (gc["query"] != gc.name)].shape[0])}
    return out


def main():
    rng = np.random.default_rng(SEED)
    res = {"located_polls_2023": provincial(rng)}
    write_json("robustness.json", res, __file__, [OUT / "advance_locations_2023.csv", INPUTS / "advance_poll_geocodes.csv", WORKBOOK_2023], seed=SEED)
    import json
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
