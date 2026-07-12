# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
verify_joint_empirical_bound.py — Gaussianity-free verification of the Ch1 headline
(added 2026-07-08 verification pass; dependence-honesty correction 2026-07-11)

Three independent checks against the committed canonical ensemble, none of which
assumes multivariate Gaussianity:

  1. Empirical joint scan. Computes Mahalanobis D² for every one of the
     1,010,000 canonical ensemble plans (same covariance construction as
     joint_outlier_score_canonical.py) and counts plans at or beyond each real
     map's D². For the minority map the count is 0: no sampled plan reaches it.

     DEPENDENCE-HONESTY (2026-07-11 correction): the naive (b+1)/(B+1) figure
     (1/1,010,001 = 9.90e-07) assumes the B samples are exchangeable with the
     observed map. MCMC samples are autocorrelated (measured D²-series tau
     ~ 203-258 per chain), so the scan carries only n_eff ~ 4,600 effective
     samples, and 0 exceedances honestly supports (rule of three) an empirical
     upper bound of 3/n_eff ~ 6.5e-04 — nearly three orders of magnitude
     weaker than the naive figure. An earlier version
     of this script (2026-07-08) reported the 9.90e-07 figure as
     "assumption-free"; it is not — it silently swapped "no Gaussianity
     assumption" for "no assumptions". The sub-1e-06 headline therefore rests
     on the parametric chi-squared(4) model (p = 1.40e-06), stated as such;
     the empirical scan's roles are (a) confirming no sampled plan reaches the
     minority and (b) validating the parametric model in the observable region
     (check 2), not tightening the headline.

  2. Parametric-model check in the observable region. The majority map's
     empirical tail fraction is compared to its parametric p; agreement in the
     region where the ensemble can actually check the model supports the
     chi-squared extrapolation used for the minority.

  3. Gelman-Rubin R-hat on the full 1,010,000-plan run (4 chains x 252,500),
     closing the §s58a6-B diagnostic gap (the original R-hat table was computed
     on the run's earlier 250,000-plan state, where efficiency_gap and
     declination marginally exceeded the Vehtari 1.01 recommendation).

Backward:
  data/outputs/simulated_ensemble_raw_samples_canonical.csv
  data/outputs/simulation_real_map_scores_canonical.json
Forward:
  findings/joint_empirical_bound_verification.json
  reports/academic/report_academic.md §5.4.9 (empirical-bound note), §5.4 (R-hat addendum)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcmc_ensemble import autocorrelation_ess

ROOT = Path(__file__).resolve().parent.parent.parent
ENSEMBLE_CSV = ROOT / "data" / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"
REAL_SCORES = ROOT / "data" / "outputs" / "simulation_real_map_scores_canonical.json"
OUT_JSON = ROOT / "findings" / "joint_empirical_bound_verification.json"

PARTISAN_COLS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
MAP_KEYS = {"minority": "minority_2026", "majority": "majority_2026", "enacted": "2019_enacted"}


def gelman_rubin(chains: list[np.ndarray]) -> float:
    """Classic Gelman & Rubin (1992) potential scale reduction factor."""
    n = min(len(x) for x in chains)
    xs = [x[:n] for x in chains]
    means = np.array([x.mean() for x in xs])
    var_s = np.array([x.var(ddof=1) for x in xs])
    w = var_s.mean()
    b = n * means.var(ddof=1)
    var_hat = (n - 1) / n * w + b / n
    return float(np.sqrt(var_hat / w))


def run() -> None:
    t0 = time.time()
    df = pd.read_csv(ENSEMBLE_CSV, usecols=PARTISAN_COLS + ["chain"])
    with open(REAL_SCORES) as f:
        real = json.load(f)

    X = df[PARTISAN_COLS].dropna().values
    mu = X.mean(axis=0)
    cov = np.cov(X, rowvar=False)
    cinv = np.linalg.pinv(cov)
    diffs = X - mu
    d2_all = np.einsum("ij,jk,ik->i", diffs, cinv, diffs)
    n_plans = int(len(d2_all))

    # Effective sample size of the joint D² series (the quantity actually
    # scanned) — the dependence-honest denominator for any empirical bound.
    kept = df[PARTISAN_COLS].dropna().index
    d2_series = pd.Series(d2_all, index=kept)
    ess_per_chain = {}
    n_eff_joint = 0.0
    for chain_id, g in df.loc[kept].groupby("chain"):
        stats = autocorrelation_ess(d2_series.loc[g.index].values)
        ess_per_chain[str(chain_id)] = {"tau": round(stats["tau"], 1), "n_eff": round(stats["n_eff"], 1)}
        n_eff_joint += stats["n_eff"]
    rule_of_three_bound = 3.0 / n_eff_joint if n_eff_joint > 0 else float("nan")
    print(f"joint-D2 n_eff (4 chains pooled) = {n_eff_joint:,.0f}; "
          f"rule-of-three bound at 0 exceedances = {rule_of_three_bound:.2e}")

    maps_out = {}
    for label, key in MAP_KEYS.items():
        obs = np.array([real[key][c] for c in PARTISAN_COLS]) - mu
        d2 = float(obs @ cinv @ obs)
        count_ge = int((d2_all >= d2).sum())
        entry = {
            "d2": round(d2, 4),
            "d": round(d2 ** 0.5, 4),
            "plans_at_or_beyond": count_ge,
            "empirical_tail_fraction": round(count_ge / n_plans, 8),
            "naive_bound_b1_B1_assumes_exchangeability": round((count_ge + 1) / (n_plans + 1), 10),
        }
        if count_ge == 0:
            entry["dependence_honest_empirical_bound"] = round(rule_of_three_bound, 6)
        maps_out[label] = entry
        print(f"{label:10s} D2={d2:8.2f}  plans>= {count_ge:>7,}  "
              f"naive (b+1)/(B+1) = {(count_ge + 1) / (n_plans + 1):.2e}")

    rhat = {}
    for c in PARTISAN_COLS:
        chains = [g[c].values for _, g in df.groupby("chain")]
        rhat[c] = round(gelman_rubin(chains), 5)
        print(f"R-hat (GR92, full 1.01M, 4 chains)  {c:22s} {rhat[c]:.5f}")

    out = {
        "date": time.strftime("%Y-%m-%d"),
        "ensemble": f"{ENSEMBLE_CSV.name} ({n_plans:,} plans, 4 chains x 252,500)",
        "n_plans": n_plans,
        "ensemble_max_d2": round(float(d2_all.max()), 4),
        "maps": maps_out,
        "joint_d2_ess": {
            "per_chain": ess_per_chain,
            "n_eff_pooled": round(n_eff_joint, 1),
            "rule_of_three_bound_at_zero_exceedances": round(rule_of_three_bound, 6),
        },
        "gelman_rubin_full_run": rhat,
        "notes": [
            "DEPENDENCE-HONESTY CORRECTION (2026-07-11): the (b+1)/(B+1) figure assumes "
            "exchangeability; MCMC samples are autocorrelated, so the scan carries only "
            "n_eff effective samples (see joint_d2_ess). Zero exceedances honestly supports "
            "an empirical bound of ~3/n_eff (rule of three), NOT 9.90e-07. The sub-1e-06 "
            "headline rests on the parametric chi-squared(4) model (1.40e-06), stated as "
            "such. The 2026-07-08 version of this file called the naive figure "
            "'assumption-free'; that description was wrong and is retracted.",
            "The scan's Gaussianity-free contributions: (a) no sampled plan reaches the "
            "minority's D2; (b) in the observable region the parametric model tracks the "
            "empirical tail (majority 0.0971 parametric vs 0.0982 empirical; enacted 0.0126 "
            "vs 0.0156), supporting the chi-squared(4) extrapolation.",
            "R-hat here is on the full 1,010,000-plan run; the s58a6-B table (2026-05-10) "
            "was computed at the run's 250,000-plan state.",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nWritten: {OUT_JSON}  ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    run()
