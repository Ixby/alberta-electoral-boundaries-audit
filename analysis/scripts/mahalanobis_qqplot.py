# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
mahalanobis_qqplot.py -- QQ-plot: ensemble D² vs chi²(4), Appendix G diagnostic

Diagnostic only — documents how well the chi²(4) parametric assumption fits the
empirical Mahalanobis D² distribution from the canonical 1,010,000-plan ensemble.

Uses *exactly* the same covariance math as joint_outlier_score_canonical.py:
  X = ensemble[cols].dropna().values
  mu = X.mean(axis=0)
  cov = np.cov(X, rowvar=False)   # ddof=1
  cov_inv = np.linalg.pinv(cov)   # pseudoinverse, same as canonical script

Output:
  data/maps/mcmc/qqplot_mahalanobis_vs_chi2_4.svg
  KS D-statistic printed to stdout
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent.parent
ENSEMBLE_CSV = ROOT / "data" / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"
OUT_SVG = ROOT / "data" / "maps" / "mcmc" / "qqplot_mahalanobis_vs_chi2_4.svg"

PARTISAN_COLS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]


def compute_ensemble_d2(ensemble: pd.DataFrame, cols: list[str]) -> np.ndarray:
    """
    Compute Mahalanobis D² for every row in `ensemble`.

    Exactly replicates the covariance setup in joint_outlier_score_canonical.py
    (lines 117-123): mean-centre, np.cov(rowvar=False), np.linalg.pinv.
    """
    X = ensemble[cols].dropna().values          # shape (n, 4)
    mu = X.mean(axis=0)                         # (4,)
    cov = np.cov(X, rowvar=False)               # (4, 4), ddof=1
    cov_inv = np.linalg.pinv(cov)              # pseudoinverse
    diff = X - mu                               # (n, 4)
    d2 = np.einsum("ij,jk,ik->i", diff, cov_inv, diff)  # vectorised D²
    return d2


def make_qqplot(d2: np.ndarray, out_path: Path, df: int = 4) -> None:
    """
    QQ-plot: empirical D² quantiles on x-axis, chi²(df) quantiles on y-axis,
    with a 45° reference line.

    Uses a quantile grid (5000 evenly spaced probabilities) rather than raw
    scatter of 1M points so the SVG stays small.
    """
    # Exclude p=0 and p=1 to avoid ±inf quantiles
    probs = np.linspace(0.0001, 0.9999, 5000)

    emp_q = np.quantile(d2, probs)             # empirical D² quantiles
    theo_q = stats.chi2.ppf(probs, df=df)      # chi²(4) theoretical quantiles

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.scatter(emp_q, theo_q, s=3, alpha=0.4, color="#2c7bb6", linewidths=0,
               label="Quantile pairs")

    # 45° reference line over the range [0, max(both)]
    ref_max = max(emp_q.max(), theo_q.max()) * 1.05
    ax.plot([0, ref_max], [0, ref_max], color="#d7191c", linewidth=1.5,
            linestyle="--", label="45° reference (perfect fit)")

    ax.set_xlabel("Empirical D² quantile (ensemble)", fontsize=11)
    ax.set_ylabel("Theoretical χ²(4) quantile", fontsize=11)
    ax.set_title(
        "QQ-plot: ensemble Mahalanobis D² vs χ²(4)\n"
        "Canonical 1,010,000-plan ReCom ensemble, 4 metrics",
        fontsize=11,
    )
    ax.set_xlim(0, ref_max)
    ax.set_ylim(0, ref_max)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=False, nbins=6))
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=False, nbins=6))
    ax.legend(fontsize=9, loc="upper left")

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"Plot saved: {out_path}")


def compute_ks(d2: np.ndarray, df: int = 4) -> float:
    """
    KS D-statistic between empirical D² and chi²(df).

    Note: with n ≈ 1M, the KS p-value is nearly always << 0.05 due to the
    massive sample size and mild discreteness in seats_at_50_50. The
    *D-statistic* (maximum CDF deviation) is the interpretable quantity.
    A D below ~0.01-0.02 indicates practically excellent fit.
    """
    result = stats.kstest(d2, "chi2", args=(df,))
    return float(result.statistic)


def main() -> None:
    print(f"Loading ensemble: {ENSEMBLE_CSV}")
    ensemble = pd.read_csv(ENSEMBLE_CSV)
    print(f"  Rows: {len(ensemble):,}  Columns: {ensemble.columns.tolist()}")

    missing = [c for c in PARTISAN_COLS if c not in ensemble.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    print(f"\nComputing D² for {len(ensemble):,} ensemble plans...")
    d2 = compute_ensemble_d2(ensemble, PARTISAN_COLS)
    print(f"  D² range: [{d2.min():.4f}, {d2.max():.4f}]")
    print(f"  D² mean:  {d2.mean():.4f}  (chi²(4) mean = 4.000)")
    print(f"  D² median:{np.median(d2):.4f}  (chi²(4) median = {stats.chi2.median(4):.4f})")

    # KS statistic
    ks_d = compute_ks(d2)
    print(f"\nKolmogorov-Smirnov D-statistic vs chi²(4): {ks_d:.6f}")
    print(f"  (KS p-value is not reported: with n={len(d2):,} it is always near 0")
    print(f"   regardless of practical fit quality; interpret D-stat magnitude)")

    # QQ-plot
    print(f"\nGenerating QQ-plot...")
    make_qqplot(d2, OUT_SVG, df=4)

    # Extra: tail comparison at selected high percentiles
    print(f"\nTail comparison (empirical D² vs chi²(4) at extreme percentiles):")
    for pct in [0.990, 0.999, 0.9999]:
        emp_val = float(np.quantile(d2, pct))
        theo_val = float(stats.chi2.ppf(pct, df=4))
        direction = "heavier" if emp_val > theo_val else "lighter"
        print(f"  p={pct:.4f}: empirical={emp_val:.3f}  chi²(4)={theo_val:.3f}  ({direction} empirical tail)")

    # Minority map observed D²
    d2_obs = 5.7157 ** 2  # from findings/joint_outlier_score.json
    emp_tail = float(np.mean(d2 >= d2_obs))
    theo_tail = float(stats.chi2.sf(d2_obs, df=4))
    print(f"\nMinority map observed D² = {d2_obs:.4f}")
    print(f"  Empirical tail prob (fraction of ensemble >= D²_obs): {emp_tail:.4e}")
    print(f"  Parametric chi²(4) tail prob:                         {theo_tail:.4e}")
    if emp_tail > 0:
        ratio = emp_tail / theo_tail
        print(f"  Ratio empirical/parametric: {ratio:.2f}x")
        if ratio > 1:
            print(f"  => Empirical tail is HEAVIER => parametric p is anti-conservative")
            print(f"     (1.40e-06 understates the true tail probability)")
        else:
            print(f"  => Empirical tail is LIGHTER => parametric p is conservative")
            print(f"     (1.40e-06 overstates the true tail probability)")
    else:
        print(f"  Empirical tail = 0 (no ensemble plans reach D²_obs = {d2_obs:.2f})")
        print(f"  => Cannot estimate ratio; parametric approximation is the only option")


if __name__ == "__main__":
    main()
