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

     DEPENDENCE: the naive (b+1)/(B+1) figure (1/1,010,001 = 9.90e-07)
     assumes the B samples are exchangeable with the observed map. MCMC samples
     are autocorrelated, so the scan carries only the D² series' effective
     sample size (computed below and written to joint_d2_ess; 4,372 pooled on
     the committed ensemble, per-chain tau 214 to 251), and 0 exceedances
     supports (rule of three) an empirical upper bound of 3/n_eff, about
     6.9e-04: nearly three orders of magnitude weaker than the naive figure.
     The naive figure is not "assumption-free". The sub-1e-06 headline rests on
     the parametric chi-squared(4) model (p = 8.8e-07 in
     findings/joint_outlier_score.json), stated as such. The empirical scan
     confirms that no sampled plan reaches the minority; it does not tighten
     the headline.

  2. Parametric-model check in the observable region. Each map's empirical
     tail fraction is written beside its chi-squared(4) p. They are close at
     the majority's D² (7.7) and the 2019 map's (13.2). That is two points; further
     out (D² 16 to 24) the sample holds 1.6 to 3.0 times as many plans as the
     model predicts (findings/audit_2026-11-10/joint_sensitivity.json), so these two
     points do not validate the model at the minority's D².

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


def chi2_sf_df4(d2: float) -> float:
    """Upper tail of the chi-squared distribution with 4 degrees of freedom
    (closed form: exp(-x/2) * (1 + x/2)); the parametric model's p for a D²."""
    return float(np.exp(-d2 / 2.0) * (1.0 + d2 / 2.0))


def build_notes(maps_out: dict, n_eff_joint: float, rule_of_three_bound: float,
                n_plans: int, any_cap_bound: bool) -> list[str]:
    """Notes for the output JSON, built from the values computed in this run."""
    naive = 1.0 / (n_plans + 1)
    mn, mj, en = maps_out["minority"], maps_out["majority"], maps_out["enacted"]
    notes = [
        f"The (b+1)/(B+1) figure ({naive:.2e}) assumes exchangeability; MCMC samples are "
        f"autocorrelated, so the scan carries only n_eff = {n_eff_joint:,.0f} effective samples "
        f"(see joint_d2_ess). Zero exceedances supports an empirical bound of about 3/n_eff = "
        f"{rule_of_three_bound:.2e} (rule of three), not {naive:.2e}. The sub-1e-06 headline "
        f"rests on the parametric chi-squared(4) model ({mn['parametric_chi2_4_p']:.2e}), "
        "stated as such.",
        f"What the scan shows without assuming Gaussianity: (a) {mn['plans_at_or_beyond']:,} "
        f"sampled plans reach the minority's D2; (b) at the two other maps' D2 the parametric "
        f"model and the empirical tail are close (majority {mj['parametric_chi2_4_p']:.4f} parametric "
        f"vs {mj['empirical_tail_fraction']:.4f} empirical; enacted {en['parametric_chi2_4_p']:.4f} "
        f"vs {en['empirical_tail_fraction']:.4f}). Two points do not validate the model at the "
        "minority's D2: between D2 16 and 24 the sample holds 1.6 to 3.0 times as many plans as "
        "the model predicts (findings/audit_2026-11-10/joint_sensitivity.json).",
        "R-hat here is on the full 1,010,000-plan run; the s58a6-B table (2026-05-10) "
        "was computed at the run's 250,000-plan state.",
    ]
    if any_cap_bound:
        notes.append(
            "The lag cap bound on at least one chain's D2 series: its tau is understated, so "
            "n_eff is an upper bound and the rule-of-three bound is a lower bound on the honest "
            "empirical bound."
        )
    return notes

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
        ess_per_chain[str(chain_id)] = {"tau": round(stats["tau"], 1), "n_eff": round(stats["n_eff"], 1),
                                        "lag_cap_bound": bool(stats["cap_bound"])}
        n_eff_joint += stats["n_eff"]
    any_cap_bound = any(v["lag_cap_bound"] for v in ess_per_chain.values())
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
            "parametric_chi2_4_p": chi2_sf_df4(d2),
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
        "notes": build_notes(maps_out, n_eff_joint, rule_of_three_bound, n_plans, any_cap_bound),
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nWritten: {OUT_JSON}  ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    run()
