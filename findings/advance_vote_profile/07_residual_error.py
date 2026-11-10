"""How stable are the seat counts under rule R once the rule's own error is included? (exploratory, not registered)

05_models_headlines.py varies only the two dials. Even with the right dials, R misses the true
advance vote of a small area by some amount. This script measures that miss on the federal
advance districts (the only place the truth is known) and adds it to R at each of the 1,216
provincial election-day stations.

  share noise   extra scatter of a district's advance log-odds around R's line, beyond what
                counting error alone gives (federal, mean of 2019 and 2021)
  volume noise  scatter of log(true advance ballots / ballots R's count dial predicts)

Caution: the noise is measured on federal advance districts (about 4,700 electors each) and
applied independently to provincial stations (about 2,400 electors each). Smaller areas may
be noisier; neighbouring stations may share errors. A half-size run is given for scale.

Method follows the independent verifier's check (audit2/verify-advance.json), rebuilt here.
Seed 20261110, 1,000 draws per scenario.

Writes outputs/residual_error.json
Usage: python findings/advance_vote_profile/07_residual_error.py
"""
import contextlib
import importlib.util
import io
import json

import numpy as np
import pandas as pd
from scipy.optimize import brentq

import _models as M
from _common import HERE, OUT, build_va_table, division_totals, load_2023_rows, load_va, logit

SEED = 20261110
N = 1000

spec = importlib.util.spec_from_file_location("h05", HERE / "05_models_headlines.py")
with contextlib.redirect_stdout(io.StringIO()):
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)


def calibrate(year):
    t = pd.read_csv(OUT / f"federal_alberta_advance_districts_{year}.csv").reset_index(drop=True)
    w = (t.a_lib_ndp + t.a_con).values.astype(float)
    x, y = logit(t.eday_share), logit(t.adv_share)
    sw = pd.Series(w).groupby(t.fed.values).transform("sum").values
    xd = x - pd.Series(w * x).groupby(t.fed.values).transform("sum").values / sw
    yd = y - pd.Series(w * y).groupby(t.fed.values).transform("sum").values / sw
    b = np.sum(w * xd * yd) / np.sum(w * xd * xd)
    r = yd - b * xd
    p = t.adv_share.values
    tot, samp = np.average(r ** 2, weights=w), np.average(1 / (w * p * (1 - p)), weights=w)
    t["A"], t["V"] = t.a_con + t.a_lib_ndp + t.a_other, t.con + t.lib_ndp + t.other
    t["G"] = (t.electors - t.V).clip(lower=0)
    for c in "AVG":
        t[c + "s"] = t[c] / t.groupby("fed")[c].transform("sum")
    X, Y = (t.Gs - t.Vs).values, (t.As - t.Vs).values
    lam = np.sum(X * Y) / np.sum(X * X)
    lr = np.log(t.As / ((1 - lam) * t.Vs + lam * t.Gs))
    return {"residual_log_odds_sd": round(float(np.sqrt(tot)), 4), "counting_error_sd": round(float(np.sqrt(samp)), 4),
            "excess_sd": round(float(np.sqrt(max(tot - samp, 0))), 4), "volume_log_sd": round(float(lr.std()), 4),
            "median_electors_per_district": float(t.electors.median())}


def main():
    cal = {str(y): calibrate(y) for y in (2021, 2019)}
    sig_e = float(np.mean([c["excess_sd"] for c in cal.values()]))
    sig_v = float(np.mean([c["volume_log_sd"] for c in cal.values()]))
    raw, g = load_2023_rows(), load_va()
    t = build_va_table(g, raw)
    t["gap"] = t.gap.fillna(0).clip(lower=0)
    tot = division_totals(raw)
    official = raw.groupby("ed")[["ndp", "ucp"]].sum()
    lab = h.assignments(g.to_crs(3400))
    hd = json.loads((OUT / "headline.json").read_text())["recommended"]
    BETA, LAM = hd["beta"], hd["lam"]
    idx = {ed: np.where(t.ed.values == ed)[0] for ed in sorted(t.ed.unique())}
    en_, eu_, gp_ = t.e_n.values, t.e_u.values, t.gap.values

    def alloc(eps=None, eta=None, bd=None, ld=None):
        n, u = en_.copy(), eu_.copy()
        for ed, ix in idx.items():
            en, eu, gp = en_[ix], eu_[ix], gp_[ix]
            An, Au = float(tot.ndp[ed]), float(tot.ucp[ed])
            T, e = An + Au, en + eu
            lam = LAM if ld is None else ld[ed]
            beta = BETA if bd is None else bd[ed]
            w = e / e.sum()
            if gp.sum() > 0:
                w = (1 - lam) * w + lam * gp / gp.sum()
            if eta is not None:
                w = w * np.exp(eta[ix])
                w = w / w.sum()
            P = en.sum() / e.sum()
            p = (en + 10 * P) / (e + 10)
            x = beta * (M._logit(p) - M._logit(P))
            if eps is not None:
                x = x + eps[ix]
            a = brentq(lambda a: float(np.sum(w / (1 + np.exp(-(a + x)))) - An / T), -30, 30)
            q = 1 / (1 + np.exp(-(a + x)))
            n[ix] += T * w * q
            u[ix] += T * w * (1 - q)
        return n, u

    dist = lambda n, u, l: pd.DataFrame({"d": l, "u": u, "n": n}).groupby("d")[["u", "n"]].sum()
    n0, u0 = alloc()
    chk = pd.DataFrame({"ed": t.ed, "n": n0, "u": u0}).groupby("ed").sum()
    div_err = float(max((chk.n - official.ndp).abs().max(), (chk.u - official.ucp).abs().max()))
    assert div_err < 1e-6 and len(chk) == 87
    base = {mp: dist(n0, u0, l) for mp, l in lab.items()}
    st = t.station.fillna("none").values
    ust, inv = np.unique(st, return_inverse=True)
    rng = np.random.default_rng(SEED)
    scen = {"share noise": (sig_e, 0, False), "share + volume noise": (sig_e, sig_v, False),
            "share + volume noise, dials vary by division": (sig_e, sig_v, True), "half-size share noise": (sig_e / 2, 0, False)}
    mc5 = json.loads((OUT / "headline.json").read_text())["monte_carlo"]
    res = {}
    for name, (se_, sv_, dials) in scen.items():
        seats, marg, egs = {mp: [] for mp in lab}, {mp: [] for mp in lab}, {mp: [] for mp in lab}
        for _ in range(N):
            eps = rng.normal(0, se_, len(ust))[inv]
            eta = rng.normal(0, sv_, len(ust))[inv] if sv_ > 0 else None
            bd = {ed: max(0.0, rng.normal(BETA, mc5["beta_sd_between_divisions"])) for ed in idx} if dials else None
            ld = {ed: float(np.clip(rng.normal(LAM, mc5["lam_sd_between_divisions"]), 0, 1)) for ed in idx} if dials else None
            n, u = alloc(eps, eta, bd, ld)
            for mp, l in lab.items():
                d = dist(n, u, l)
                seats[mp].append(int((d.u > d.n).sum()))
                marg[mp].append((d.u - d.n).values)
                egs[mp].append(h.metrics(n, u, l)[0]["efficiency_gap_pct"])
        out = {}
        for mp in lab:
            s = pd.Series(seats[mp]).value_counts(normalize=True).sort_index()
            m = np.array(marg[mp])
            bm = base[mp].u - base[mp].n
            sd = pd.Series(m.std(0), index=base[mp].index)
            z = bm.abs() / sd.replace(0, np.nan)
            flip = pd.Series(((m > 0) != (bm.values > 0)).mean(0), index=base[mp].index)
            out[mp] = {"ucp_seats_distribution": {int(k): round(float(v), 3) for k, v in s.items()},
                       "seats_p5_p95": [int(np.percentile(seats[mp], 5)), int(np.percentile(seats[mp], 95))],
                       "efficiency_gap_pct_p5_p50_p95": [round(float(q), 2) for q in np.percentile(egs[mp], [5, 50, 95])],
                       "seats_within_2sd_of_zero": int((z < 2).sum()),
                       "chance_of_flip": {k: round(float(v), 3) for k, v in flip.sort_values(ascending=False).head(5).items() if v > 0.01},
                       "margin_votes_and_sd": {k: [round(float(bm[k])), round(float(sd[k]))] for k in z.sort_values().index[:4]}}
        res[name] = out
        print(name, json.dumps({k: (v["ucp_seats_distribution"], v["efficiency_gap_pct_p5_p50_p95"]) for k, v in out.items()}), flush=True)
    final = {"status": "exploratory, not registered", "seed": SEED, "draws": N, "rule": {"beta": BETA, "lam": LAM},
             "calibration": cal, "share_noise_sd_log_odds": round(sig_e, 4), "volume_noise_sd_log": round(sig_v, 4),
             "check_R_returns_official_totals": {"divisions": 87, "max_abs_error_votes": div_err}, "results": res}
    (OUT / "residual_error.json").write_text(json.dumps(final, indent=1))
    print(json.dumps(final["results"], indent=1))


if __name__ == "__main__":
    main()
