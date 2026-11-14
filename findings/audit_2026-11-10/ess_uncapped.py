#!/usr/bin/env python3
"""ess_uncapped.py -- effective sample size of the canonical ensemble without the lag cap.

EXPLORATORY. Computed after the fact for the 2026-11-10 audit. Not a registered test.

Neighbouring plans in a ReCom chain are near-copies, so 1,010,000 plans carry far fewer
independent draws. The effective sample size is n / tau, where tau = 1 + 2 * (sum of the
autocorrelations rho_k). The three estimators differ only in where that sum stops:

  capped   : the pipeline's rule (analysis/scripts/mcmc_ensemble.py autocorr_ess): add rho_k
             until the first rho_k <= 0, but never beyond lag 2,000. In this run rho is still
             positive at lag 2,000 everywhere, so the cap always binds and tau is too small.
  uncapped : the same rule with no cap: add rho_k up to the first rho_k <= 0.
  geyer    : Geyer's (1992) initial positive sequence: add the pairs rho_2m + rho_2m+1 while a
             pair is positive. (The initial MONOTONE sequence is also given, for reference.)

Each is computed (a) on the four chains joined end to end, which is how the pipeline computes
its published "pooled" figures, and (b) on each chain alone, then added up across chains.
(a) measures every chain against the pooled mean, so disagreement between chains lowers it,
and it borrows a little across the three joins; (b) measures each chain against its own mean,
so it ignores disagreement between chains and is the most generous.
Geyer's rule is also applied (c) to the standard multi-chain combination of the per-chain
autocovariances (Gelman et al., BDA3 s.11.5; Vehtari et al. 2021, without rank-normalising),
which is the textbook pooled estimate and also counts disagreement between chains.

In this run "uncapped" and "geyer initial positive" agree to the first decimal on (a) and (b):
the autocorrelation crosses zero smoothly, so the two rules stop within one lag of each other.

Input : data/simulation_checkpoints_canonical/chain{0,1,2,3}_samples.csv (4 x 252,500 plans)
Output: findings/audit_2026-11-10/ess_uncapped.json
Run   : python findings/audit_2026-11-10/ess_uncapped.py   (no network, no randomness; ~20 s)
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().with_suffix(".json")
PARTISAN = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
OTHER = ["population_mad", "reock_proxy_median", "reock_proxy_pct_below_030"]
CAP = 2000
FLOOR = 1000  # the reports' own "publication-grade" floor (about 1,000 to 2,000 draws)


def acf(x):
    """Autocorrelation at every lag, 1/n normalisation (identical to the pipeline's lag loop)."""
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    m = 1 << (2 * n - 1).bit_length()
    f = np.fft.rfft(x, m)
    a = np.fft.irfft(f * np.conj(f), m)[:n] / n
    return a / a[0]


def tau_first_nonpositive(rho, cap=None):
    K = len(rho) - 1 if cap is None else min(cap, len(rho) - 1)
    nonpos = np.nonzero(rho[1:K + 1] <= 0)[0]
    last = int(nonpos[0]) if len(nonpos) else K  # number of lags summed
    return 1.0 + 2.0 * float(rho[1:last + 1].sum()), last, bool(len(nonpos) == 0)


def tau_geyer(rho, monotone=False):
    m = (len(rho)) // 2
    pairs = rho[0:2 * m:2] + rho[1:2 * m:2]
    nonpos = np.nonzero(pairs <= 0)[0]
    stop = int(nonpos[0]) if len(nonpos) else m
    g = pairs[:stop]
    if monotone:
        g = np.minimum.accumulate(g)
    return -1.0 + 2.0 * float(g.sum()), 2 * stop - 1


def multichain_geyer(chains):
    """BDA3 / Vehtari et al. (2021) multi-chain autocorrelation, then Geyer truncation."""
    M, N = len(chains), len(chains[0])
    acov = []
    for c in chains:
        x = np.asarray(c, float)
        r = acf(x)
        acov.append(r * x.var())  # autocovariance, 1/n normalisation
    acov = np.mean(acov, axis=0)
    means = np.array([np.mean(c) for c in chains])
    W = float(np.mean([np.var(c, ddof=1) for c in chains]))
    B_over_n = float(means.var(ddof=1))
    var_plus = (N - 1) / N * W + B_over_n
    rho = 1.0 - (W - acov * N / (N - 1)) / var_plus
    t_pos, lag = tau_geyer(rho)
    t_mon, _ = tau_geyer(rho, monotone=True)
    return {"geyer_initial_positive": {"tau": round(t_pos, 2), "ess": round(M * N / t_pos, 1), "last_lag": lag},
            "geyer_initial_monotone": {"tau": round(t_mon, 2), "ess": round(M * N / t_mon, 1)},
            "rhat_classic": round(float(np.sqrt(var_plus / W)), 5)}


def all_estimators(x):
    rho = acf(x)
    n = len(x)
    t_cap, l_cap, cap_bound = tau_first_nonpositive(rho, CAP)
    t_unc, l_unc, _ = tau_first_nonpositive(rho)
    t_gey, l_gey = tau_geyer(rho)
    t_mon, _ = tau_geyer(rho, monotone=True)
    return {
        "n": int(n),
        "capped": {"tau": round(t_cap, 2), "ess": round(n / t_cap, 1), "last_lag": l_cap,
                   "cap_binds": cap_bound, "rho_at_cap": round(float(rho[CAP]), 4)},
        "uncapped": {"tau": round(t_unc, 2), "ess": round(n / t_unc, 1), "last_lag": l_unc},
        "geyer_initial_positive": {"tau": round(t_gey, 2), "ess": round(n / t_gey, 1), "last_lag": l_gey},
        "geyer_initial_monotone": {"tau": round(t_mon, 2), "ess": round(n / t_mon, 1)},
    }


def main():
    chains = [pd.read_csv(ROOT / f"data/simulation_checkpoints_canonical/chain{i}_samples.csv",
                          usecols=PARTISAN + OTHER, float_precision="round_trip") for i in range(4)]
    assert all(len(c) == 252500 for c in chains)
    pub = json.loads((ROOT / "data/outputs/simulation_convergence_diagnostics_canonical.json").read_text())
    EST = ["capped", "uncapped", "geyer_initial_positive", "geyer_initial_monotone"]
    metrics = {}
    for m in PARTISAN + OTHER:
        pooled = all_estimators(np.concatenate([c[m].values for c in chains]))
        per = [all_estimators(c[m].values) for c in chains]
        summed = {e: round(sum(p[e]["ess"] for p in per), 1) for e in EST}
        metrics[m] = {
            "published_pooled_ess": round(pub[m]["n_eff"], 1),
            "capped_reproduces_published": bool(abs(pooled["capped"]["ess"] - pub[m]["n_eff"]) < 0.06),
            "pooled_chains_joined": pooled,
            "per_chain": per,
            "per_chain_sum": summed,
            "multichain_combination": multichain_geyer([c[m].values for c in chains]),
            "largest_per_chain_tau_uncapped": max(p["uncapped"]["tau"] for p in per),
        }
    # Which figure to quote: the two cap-free estimators, on both pooling conventions.
    quote = {}
    for m in PARTISAN:
        vals = [metrics[m]["pooled_chains_joined"]["uncapped"]["ess"], metrics[m]["pooled_chains_joined"]["geyer_initial_positive"]["ess"],
                metrics[m]["per_chain_sum"]["uncapped"], metrics[m]["per_chain_sum"]["geyer_initial_positive"],
                metrics[m]["multichain_combination"]["geyer_initial_positive"]["ess"]]
        quote[m] = {
            "capped_published": metrics[m]["pooled_chains_joined"]["capped"]["ess"],
            "uncapped_pooled": vals[0], "geyer_pooled": vals[1],
            "uncapped_per_chain_sum": vals[2], "geyer_per_chain_sum": vals[3],
            "geyer_multichain_combination": vals[4],
            "cap_free_low": min(vals), "cap_free_high": max(vals),
            "clears_1000_floor": {
                "capped_published": bool(metrics[m]["pooled_chains_joined"]["capped"]["ess"] >= FLOOR),
                "uncapped_pooled": bool(vals[0] >= FLOOR), "geyer_pooled": bool(vals[1] >= FLOOR),
                "uncapped_per_chain_sum": bool(vals[2] >= FLOOR), "geyer_per_chain_sum": bool(vals[3] >= FLOOR),
                "geyer_multichain_combination": bool(vals[4] >= FLOOR),
                "under_every_cap_free_estimate": bool(min(vals) >= FLOOR),
            },
        }
    lo = min(q["cap_free_low"] for q in quote.values())
    hi = max(q["cap_free_high"] for q in quote.values())
    pooled_unc = [quote[m]["uncapped_pooled"] for m in PARTISAN]
    out = {
        "status": "EXPLORATORY - computed after the fact for the 2026-11-10 audit; not a registered test",
        "ballots": "election-day ballots (the canonical ensemble)",
        "n_plans": 1010000, "n_chains": 4, "lag_cap_in_pipeline": CAP, "floor_used_by_reports": FLOOR,
        "metrics": metrics,
        "partisan_summary": quote,
        "figure_to_quote": {
            "published_capped_range": [min(quote[m]["capped_published"] for m in PARTISAN), max(quote[m]["capped_published"] for m in PARTISAN)],
            "uncapped_pooled_range_same_estimator_no_cap": [min(pooled_unc), max(pooled_unc)],
            "cap_free_range_all_variants": [lo, hi],
            "suggested_wording": (
                "about 1,000 independent draws (roughly %s to %s depending on the measure and the estimator; "
                "seats at 50/50 is the lowest)" % (format(int(round(lo, -2)), ","), format(int(round(hi, -2)), ","))),
            "why": "The published 1,413-1,522 stop the autocorrelation sum at lag 2,000 while the autocorrelation is still "
                   "positive (0.05 to 0.07), so they are upper bounds. Removing the cap lowers every partisan figure by "
                   "about a quarter to a third.",
            "metrics_clearing_1000_under_every_cap_free_estimate": [m for m in PARTISAN if quote[m]["clears_1000_floor"]["under_every_cap_free_estimate"]],
            "metrics_not_clearing_1000_under_at_least_one": [m for m in PARTISAN if not quote[m]["clears_1000_floor"]["under_every_cap_free_estimate"]],
        },
        "limits": [
            "An autocorrelation time of about 1,000 steps is estimated from chains of 252,500 steps, about 200 to 300 "
            "autocorrelation times each; the estimates themselves carry sampling error of very roughly 10 to 20 percent.",
            "ESS here is for estimating a mean. Far-tail percentiles (such as p99.99) depend on a handful of excursions "
            "and are less well determined than these numbers suggest.",
            "The first row of each chain is the starting plan and no burn-in is dropped, as in the pipeline.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for m in PARTISAN + OTHER:
        q = metrics[m]
        print(f"{m:26s} published {q['published_pooled_ess']:7.1f} capped {q['pooled_chains_joined']['capped']['ess']:7.1f} "
              f"uncapped {q['pooled_chains_joined']['uncapped']['ess']:7.1f} (lag {q['pooled_chains_joined']['uncapped']['last_lag']}) "
              f"geyer {q['pooled_chains_joined']['geyer_initial_positive']['ess']:7.1f} mono {q['pooled_chains_joined']['geyer_initial_monotone']['ess']:7.1f} | "
              f"multichain geyer {q['multichain_combination']['geyer_initial_positive']['ess']:7.1f} | per-chain sums {q['per_chain_sum']}")
    print(out["figure_to_quote"]["suggested_wording"])


if __name__ == "__main__":
    main()
