#!/usr/bin/env python3
"""joint_sensitivity.py -- how far the joint outlier probability moves under defensible variants.

EXPLORATORY. Computed after the fact for the 2026-11-10 audit. Not a registered test.
ALL FIGURES ARE ON ELECTION-DAY BALLOTS (932,164 of the 1,764,915 ballots cast in 2023).

The published figure ("about one in 568,000") is a model estimate: the squared Mahalanobis
distance D2 of a map's four scores (efficiency gap, mean-median, declination, seats at 50/50)
from the mean of 1,010,000 neutral plans, read off a chi-square(4) tail and doubled. This
script recomputes it and the variants below for the minority, majority and 2019 maps.

  published        chi-square(4) tail of D2; exact, and doubled as published.
  hotelling        F tail allowing for a covariance estimated from n_eff independent draws
                   (pipeline formula F = (n-p)/(p(n+1)) * D2 at n_eff = 1,413), also at the
                   uncapped n_eff of 894 (ess_uncapped.py) and with the exact factor.
  drop_declination three metrics, chi-square(3). Declination correlates 0.97 with efficiency gap.
  drop_eg          three metrics, chi-square(3), dropping efficiency gap instead.
  rank_based       NORMAL-SCORES MAHALANOBIS. Each metric is replaced by its normal score:
                   a plan with midrank r among the N plans gets z = Phi^-1((r - 0.5) / N); the
                   map gets z = Phi^-1((b + 0.5 t + 0.5) / (N + 1)), b = plans strictly below
                   it, t = plans tied with it. D2 is then computed on the z-scores with their
                   own mean and covariance and read off chi-square(4). This removes skew and
                   heavy tails in single metrics; it still assumes a Gaussian dependence.
                   Reported with the count of sampled plans whose own rank-based D2 is at or
                   beyond the map's.
  empirical        No model: the count of sampled plans whose own raw D2 is at or beyond the
                   map's, the largest sampled D2, and two direct counts (plans at or above the
                   map on all four metrics; on mean-median and seats together). Also a
                   one-sided combination: S = sum over metrics of -ln(share of plans at or
                   above that value); count of plans with S at or beyond the map's.
  forest_recom     the published statistic recomputed against the forest-ReCom sampler's
                   80,000 plans (first 5,000 of each chain dropped, as that run's protocol does).
  tail_ratio       (share of sampled plans with D2 >= t) / (chi-square(4) tail at t), for
                   t = 13 .. 24: how well the model fits where it can still be checked.

Inputs : data/simulation_checkpoints_canonical/chain{0..3}_samples.csv
         data/outputs/simulation_real_map_scores_canonical.json
         data/outputs/forest_recom_raw_samples_phaseA.csv
         data/outputs/forest_recom_real_map_scores_phaseA.json
Output : findings/audit_2026-11-10/joint_sensitivity.json
Run    : python findings/audit_2026-11-10/joint_sensitivity.py   (no network, no randomness; ~1 min)
"""
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().with_suffix(".json")
C = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
MAPS = {"minority": "minority_2026", "majority": "majority_2026", "map_2019": "2019_enacted"}
N_EFF_PUBLISHED = 1413   # smallest capped n_eff, used by the pipeline's Hotelling line
N_EFF_UNCAPPED = 894     # smallest uncapped n_eff (seats at 50/50), from ess_uncapped.py
T_GRID = list(range(13, 25))


def sig(x, n=4):
    return float(f"{x:.{n}g}")


def one_in(p):
    return None if p <= 0 else int(round(1.0 / p))


def pblock(d2, df):
    p = float(stats.chi2.sf(d2, df))
    return {"D2": round(float(d2), 4), "D": round(float(np.sqrt(d2)), 4), "df": df,
            "p_exact": sig(p), "one_in_exact": one_in(p),
            "p_doubled": sig(min(1.0, 2 * p)), "one_in_doubled": one_in(min(1.0, 2 * p))}


def maha(X, obs):
    mu = X.mean(0)
    Si = np.linalg.inv(np.atleast_2d(np.cov(X, rowvar=False)))
    d = obs - mu
    ens = np.einsum("ij,jk,ik->i", X - mu, Si, X - mu)
    return float(d @ Si @ d), ens


def hotelling(d2, n, p=4, exact=False):
    factor = (n - p) * n / (p * (n - 1) * (n + 1)) if exact else (n - p) / (p * (n + 1))
    pv = float(stats.f.sf(factor * d2, p, n - p))
    return {"n_eff": n, "p_exact": sig(pv), "one_in_exact": one_in(pv),
            "p_doubled": sig(min(1.0, 2 * pv)), "one_in_doubled": one_in(min(1.0, 2 * pv))}


def all_ballots_search():
    """Is an all-ballots ensemble committed on any branch of this clone? (git ls-tree only.)"""
    pats = ("simulation_checkpoints_allballots", "raw_samples_allballots", "checkpoints_canonical_allballots")
    try:
        refs = subprocess.run(["git", "-C", str(ROOT), "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes"],
                              capture_output=True, text=True, check=True).stdout.split()
    except Exception as e:  # no git: record and carry on
        return {"searched": False, "why": repr(e)}
    hits = []
    for ref in sorted(refs):
        if ref.endswith("/HEAD"):
            continue
        names = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", ref],
                               capture_output=True, text=True).stdout.splitlines()
        hits += [f"{ref}:{n}" for n in names if any(p in n for p in pats)]
    return {"searched": True, "n_refs_searched": len([r for r in refs if not r.endswith('/HEAD')]),
            "includes_origin_amendment17_local_runs": "refs/remotes/origin/amendment17-local-runs" in refs,
            "file_name_patterns": list(pats), "files_found": sorted(hits)}


def main():
    df = pd.concat([pd.read_csv(ROOT / f"data/simulation_checkpoints_canonical/chain{i}_samples.csv",
                                usecols=C + ["chain"], float_precision="round_trip") for i in range(4)],
                   ignore_index=True)
    N = len(df)
    assert N == 1010000
    X = df[C].values
    chain = df["chain"].values
    real = json.loads((ROOT / "data/outputs/simulation_real_map_scores_canonical.json").read_text())
    corr = np.corrcoef(X, rowvar=False)

    # normal scores of the plans, per metric (midranks)
    Z = np.empty_like(X)
    for j in range(4):
        Z[:, j] = stats.norm.ppf((stats.rankdata(X[:, j], method="average") - 0.5) / N)
    # share of plans at or above each plan's own value, per metric (for the one-sided combination)
    U = np.empty_like(X)
    for j in range(4):
        U[:, j] = (N - stats.rankdata(X[:, j], method="min") + 1) / N
    S_ens = -np.log(U).sum(1)

    # forest-ReCom ensemble
    fr = pd.read_csv(ROOT / "data/outputs/forest_recom_raw_samples_phaseA.csv", usecols=C + ["chain", "chunk"],
                     float_precision="round_trip")
    fr = fr[fr["chunk"] >= 1]
    XF = fr[C].values
    freal = json.loads((ROOT / "data/outputs/forest_recom_real_map_scores_phaseA.json").read_text())

    # tail ratio of the ensemble's own D2 (does not depend on which map is scored)
    _, ens_d2 = maha(X, X.mean(0))
    tail = []
    for t in T_GRID:
        model = float(stats.chi2.sf(t, 4))
        n_ge = int((ens_d2 >= t).sum())
        tail.append({"D2": t, "plans_at_or_beyond": n_ge, "empirical_share": sig(n_ge / N),
                     "chi2_4_tail": sig(model), "ratio_empirical_to_model": round(n_ge / N / model, 3),
                     "ratio_by_chain": [round(float((ens_d2[chain == c] >= t).mean() / model), 2) for c in range(4)]})
    ratios = [r["ratio_empirical_to_model"] for r in tail]

    out = {
        "status": "EXPLORATORY - computed after the fact for the 2026-11-10 audit; not a registered test",
        "ballots": "ELECTION-DAY BALLOTS ONLY (932,164 of 1,764,915 ballots cast in 2023). Every figure in this file.",
        "ensemble": {"n_plans": N, "n_chains": 4, "n_districts": 87,
                     "note": "The neutral plans have 87 districts; the two commission maps have 89.",
                     "correlation_matrix": {C[i]: {C[j]: round(float(corr[i, j]), 4) for j in range(4)} for i in range(4)},
                     "correlation_eg_declination": round(float(corr[0, 2]), 4),
                     "largest_sampled_D2": round(float(ens_d2.max()), 4),
                     "largest_sampled_D2_by_chain": [round(float(ens_d2[chain == c].max()), 3) for c in range(4)]},
        "tail_ratio_D2_13_to_24": {
            "what": "share of sampled plans with D2 >= t, divided by the chi-square(4) tail at t; 1.0 = the model fits",
            "rows": tail, "min_ratio": min(ratios), "max_ratio": max(ratios),
            "reading": "The model's tail is too thin where it can be checked: the sample holds %.1f to %.1f times as many plans "
                       "as chi-square(4) predicts between D2 = 13 and 24. Beyond the largest sampled D2 (%.1f) nothing can be checked."
                       % (min(ratios), max(ratios), ens_d2.max()),
            "caveat": "With about 1,000 effective draws these ratios are noisy; see ratio_by_chain.",
        },
        "maps": {},
    }

    for label, key in MAPS.items():
        obs = np.array([real[key][c] for c in C], float)
        d2, _ = maha(X, obs)
        res = {"scores": {c: real[key][c] for c in C}, "n_districts": real[key]["n_districts"]}
        res["published"] = pblock(d2, 4)
        res["hotelling"] = {
            "pipeline_formula_n_eff_1413": hotelling(d2, N_EFF_PUBLISHED),
            "exact_factor_n_eff_1413": hotelling(d2, N_EFF_PUBLISHED, exact=True),
            "pipeline_formula_n_eff_894_uncapped": hotelling(d2, N_EFF_UNCAPPED),
            "note": "Allows only for error in estimating the covariance matrix from n_eff draws.",
        }
        for name, drop in (("drop_declination", 2), ("drop_eg", 0)):
            idx = [j for j in range(4) if j != drop]
            d3, e3 = maha(X[:, idx], obs[idx])
            b = pblock(d3, 3)
            b["metrics"] = [C[j] for j in idx]
            b["plans_at_or_beyond"] = int((e3 >= d3).sum())
            res[name] = b
        # single metrics, for context
        res["single_metric"] = {}
        for j, c in enumerate(C):
            d1, _ = maha(X[:, [j]], obs[[j]])
            res["single_metric"][c] = {
                "D2": round(d1, 3), "plans_at_or_above": int((X[:, j] >= obs[j]).sum()),
                "plans_at_or_below": int((X[:, j] <= obs[j]).sum()),
                "midrank_percentile": round(100.0 * ((X[:, j] < obs[j]).sum() + 0.5 * (X[:, j] == obs[j]).sum()) / N, 4)}
        # rank-based
        zo = np.array([stats.norm.ppf(((X[:, j] < obs[j]).sum() + 0.5 * (X[:, j] == obs[j]).sum() + 0.5) / (N + 1))
                       for j in range(4)])
        dr, er = maha(Z, zo)
        rb = pblock(dr, 4)
        rb.update({"definition": "normal-scores Mahalanobis; see the docstring of joint_sensitivity.py",
                   "map_normal_scores": {C[j]: round(float(zo[j]), 4) for j in range(4)},
                   "plans_at_or_beyond": int((er >= dr).sum()),
                   "empirical_share": sig((er >= dr).sum() / N) if (er >= dr).any() else 0.0,
                   "largest_sampled_rank_D2": round(float(er.max()), 3)})
        res["rank_based"] = rb
        # empirical
        uo = np.array([(X[:, j] >= obs[j]).mean() for j in range(4)])
        s_obs = float(-np.log(np.maximum(uo, 1.0 / N)).sum())
        res["empirical"] = {
            "plans_with_raw_D2_at_or_beyond": int((ens_d2 >= d2).sum()),
            "of": N,
            "largest_sampled_D2": round(float(ens_d2.max()), 4),
            "map_D2_exceeds_every_sampled_plan": bool(d2 > ens_d2.max()),
            "plans_at_or_above_on_all_four_metrics": int(np.all(X >= obs, axis=1).sum()),
            "plans_at_or_above_on_mean_median_and_seats": int(np.all(X[:, [1, 3]] >= obs[[1, 3]], axis=1).sum()),
            "one_sided_sum_of_log_upper_tails": {
                "map_statistic": round(s_obs, 4), "plans_at_or_beyond": int((S_ens >= s_obs).sum()),
                "note": "one-sided, in the UCP-favourable direction; informative for the minority map only"},
            "caveat": "A zero count among 1,010,000 autocorrelated plans worth about 1,000 independent draws supports "
                      "'rarer than roughly 1 in 1,000' on its own; it cannot support a figure in the hundred-thousands.",
        }
        # forest-ReCom
        fobs = np.array([freal[key][c] for c in C], float) if key in freal else obs
        df_, ef = maha(XF, fobs)
        fb = pblock(df_, 4)
        fb.update({"n_plans": int(len(XF)), "plans_at_or_beyond": int((ef >= df_).sum()),
                   "largest_sampled_D2": round(float(ef.max()), 3),
                   "note": "80,000 plans, 4 chains, effective sample size about 60 to 120 per metric: a rough check, "
                           "not a second estimate of equal weight." + ("" if key in freal else
                           " The forest run stored no score for this map; the canonical-run score (same votes, same map) is used.")})
        res["forest_recom"] = fb
        out["maps"][label] = res

    # honest summary range for the minority map
    m = out["maps"]["minority"]
    variants = {
        "published chi-square(4)": m["published"]["one_in_doubled"],
        "Hotelling, n_eff 1,413": m["hotelling"]["pipeline_formula_n_eff_1413"]["one_in_doubled"],
        "Hotelling, n_eff 894 (uncapped)": m["hotelling"]["pipeline_formula_n_eff_894_uncapped"]["one_in_doubled"],
        "drop efficiency gap": m["drop_eg"]["one_in_doubled"],
        "rank-based (normal scores)": m["rank_based"]["one_in_doubled"],
        "drop declination": m["drop_declination"]["one_in_doubled"],
        "forest-ReCom sampler": m["forest_recom"]["one_in_doubled"],
    }
    exact = {
        "published chi-square(4)": m["published"]["one_in_exact"],
        "Hotelling, n_eff 1,413": m["hotelling"]["pipeline_formula_n_eff_1413"]["one_in_exact"],
        "Hotelling, n_eff 894 (uncapped)": m["hotelling"]["pipeline_formula_n_eff_894_uncapped"]["one_in_exact"],
        "drop efficiency gap": m["drop_eg"]["one_in_exact"],
        "rank-based (normal scores)": m["rank_based"]["one_in_exact"],
        "drop declination": m["drop_declination"]["one_in_exact"],
        "forest-ReCom sampler": m["forest_recom"]["one_in_exact"],
    }
    lo, hi = min(variants.values()), max(variants.values())
    main_run = {k: v for k, v in variants.items() if k != "forest-ReCom sampler"}
    out["summary_minority"] = {
        "ballots": "election-day ballots only",
        "one_in_doubled_by_variant": variants,
        "one_in_exact_by_variant": exact,
        "range_one_in_doubled": [lo, hi],
        "range_one_in_doubled_main_sampler_only": [min(main_run.values()), max(main_run.values())],
        "range_one_in_exact": [min(exact.values()), max(exact.values())],
        "honest_range": "On election-day ballots, between roughly 1 in %s and 1 in %s (doubled, as published) depending on the "
                        "modelling choice; the published model gives 1 in %s. Every variant is rarer than 1 in 10,000."
                        % (format(int(float(f"{lo:.2g}")), ","), format(int(float(f"{hi:.2g}")), ","), format(m["published"]["one_in_doubled"], ",")),
        "every_variant_rarer_than_1_in_10000": bool(lo > 10000),
        "sampled_plans_at_or_beyond": {
            "raw_D2": m["empirical"]["plans_with_raw_D2_at_or_beyond"],
            "rank_based_D2": m["rank_based"]["plans_at_or_beyond"],
            "one_sided_sum_of_logs": m["empirical"]["one_sided_sum_of_log_upper_tails"]["plans_at_or_beyond"],
            "forest_recom_raw_D2": m["forest_recom"]["plans_at_or_beyond"],
        },
        "what_the_range_does_not_cover": [
            "All ballots (see all_ballots below).",
            "The 87-versus-89 district mismatch between the neutral plans and the commission maps.",
            "The doubling itself: it was set for two channels and one remains (audit finding joint-stats-4). Exact values are given beside it.",
            "Extrapolation: every model figure lies beyond the largest sampled D2, where the chi-square shape cannot be checked; "
            "between D2 13 and 24 the sample has %.1f to %.1f times the model's tail." % (min(ratios), max(ratios)),
        ],
    }
    out["all_ballots"] = {
        "computed": False,
        "why": "The joint figure needs every plan's four scores on all ballots (to estimate the mean and covariance). "
               "The all-ballots replay of the 1,010,000 plans (data/simulation_checkpoints_allballots/chain{0..3}_samples.csv and "
               "simulated_ensemble_raw_samples_allballots.csv) is not committed on this branch or on any other branch of this "
               "clone; findings/allballots_ranking/README.md records only the SHA-256 of the four chain files.",
        "branch_search": all_ballots_search(),
        "what_is_committed": "Single-metric percentiles only (findings/allballots_ranking/canonical_ranking.json). For the minority map, "
                             "election-day -> all ballots: efficiency gap p94.54 -> p98.82, mean-median p99.97 -> p98.73, "
                             "declination p98.79 -> p99.82, seats at 50/50 p99.99 -> p99.90. The two metrics that carry most of the "
                             "election-day D2 (mean-median and seats) are weaker on all ballots, so the all-ballots joint figure "
                             "cannot be assumed equal to, or stronger than, the election-day one.",
        "how_to_compute": "Re-run mcmc_ensemble_canonical.py with --run-id allballots --va-file "
                          "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg (about 2.5 hours), verify the four "
                          "SHA-256 values in findings/allballots_ranking/README.md, then run this script's calculation on those chains.",
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for label in MAPS:
        r = out["maps"][label]
        print(label, "D2", r["published"]["D2"], "1 in", r["published"]["one_in_exact"], "doubled", r["published"]["one_in_doubled"],
              "| hot", r["hotelling"]["pipeline_formula_n_eff_1413"]["one_in_doubled"],
              "| -decl", r["drop_declination"]["one_in_doubled"], "| -eg", r["drop_eg"]["one_in_doubled"],
              "| rank", r["rank_based"]["one_in_doubled"], r["rank_based"]["plans_at_or_beyond"],
              "| forest", r["forest_recom"]["one_in_doubled"], "| emp", r["empirical"]["plans_with_raw_D2_at_or_beyond"])
    print(out["summary_minority"]["honest_range"])
    print("tail ratios", ratios)
    print("all-ballots files found:", out["all_ballots"]["branch_search"].get("files_found"))


if __name__ == "__main__":
    main()
