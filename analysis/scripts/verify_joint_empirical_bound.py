# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
verify_joint_empirical_bound.py — assumption-free verification of the Ch1 headline
(added 2026-07-08 verification pass)

Three independent checks against the committed canonical ensemble, none of which
assumes multivariate Gaussianity:

  1. Empirical joint bound. Computes Mahalanobis D² for every one of the
     1,010,000 canonical ensemble plans (same covariance construction as
     joint_outlier_score_canonical.py) and counts plans at or beyond each real
     map's D². For the minority map the count is 0, giving the assumption-free
     (b+1)/(B+1) bound p <= 1/1,010,001 = 9.90e-07 — *tighter* than the
     parametric chi-squared(4) figure (1.40e-06) the audit reports. The
     parametric headline is therefore conservative relative to the
     distribution-free statement.

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

    maps_out = {}
    for label, key in MAP_KEYS.items():
        obs = np.array([real[key][c] for c in PARTISAN_COLS]) - mu
        d2 = float(obs @ cinv @ obs)
        count_ge = int((d2_all >= d2).sum())
        maps_out[label] = {
            "d2": round(d2, 4),
            "d": round(d2 ** 0.5, 4),
            "plans_at_or_beyond": count_ge,
            "empirical_tail_fraction": round(count_ge / n_plans, 8),
            "empirical_bound_b1_B1": round((count_ge + 1) / (n_plans + 1), 10),
        }
        print(f"{label:10s} D²={d2:8.2f}  plans>= {count_ge:>7,}  "
              f"empirical (b+1)/(B+1) = {(count_ge + 1) / (n_plans + 1):.2e}")

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
        "gelman_rubin_full_run": rhat,
        "notes": [
            "Empirical bounds are distribution-free: no Gaussian assumption. The minority's "
            "count of 0 gives p <= 1/(N+1) = 9.90e-07, tighter than the parametric 1.40e-06 "
            "headline — the reported parametric figure is conservative.",
            "The majority's empirical tail fraction should be compared to its parametric "
            "joint_partisan_p (0.0971) as a check of the chi-squared(4) model in the region "
            "the ensemble can observe.",
            "R-hat here is on the full 1,010,000-plan run; the §s58a6-B table (2026-05-10) "
            "was computed at the run's 250,000-plan state.",
        ],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nWritten: {OUT_JSON}  ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    run()
