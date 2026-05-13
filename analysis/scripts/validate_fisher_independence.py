"""
validate_fisher_independence.py — Empirical Spearman correlation between Ch1 and Ch2.

Measures whether the Mahalanobis distance distribution (Ch1) and the SZAT bootstrap
EG distribution (Ch2) are empirically near-independent. If |ρ| < 0.30, the Fisher
combination claim is defensible for this dataset.

Forward dependencies:
  data/simulated_ensemble_raw_samples_canonical.csv
  data/szat_bootstrap_eg_samples.npy  (produced by szat.py run; see Step 1.1)

Backward dependencies:
  analysis/methodology/fisher_independence_defense.md  (results appended here)

Run after szat.py has been executed with the new np.save code:
  python analysis/scripts/szat.py
  python analysis/scripts/validate_fisher_independence.py

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

REPO = Path(__file__).resolve().parent.parent.parent
DATA = REPO / "data"
DEFENSE_DOC = REPO / "analysis" / "methodology" / "fisher_independence_defense.md"

ENSEMBLE_CSV = DATA / "simulated_ensemble_raw_samples_canonical.csv"
BOOTSTRAP_NPY = DATA / "szat_bootstrap_eg_samples.npy"
PARTISAN_COLS = ["efficiency_gap", "mean_median", "declination"]

RHO_THRESHOLD = 0.30


def _load_ch1_distances(ensemble_path: Path) -> np.ndarray:
    df = pd.read_csv(ensemble_path)
    X = df[PARTISAN_COLS].dropna().values
    mu = X.mean(axis=0)
    cov_inv = np.linalg.pinv(np.cov(X, rowvar=False))
    return np.array([float((x - mu) @ cov_inv @ (x - mu)) for x in X])


def main() -> None:
    if not BOOTSTRAP_NPY.exists():
        print(
            f"ERROR: {BOOTSTRAP_NPY} not found.\n"
            "Run szat.py first to generate bootstrap EG samples:\n"
            "  python analysis/scripts/szat.py\n"
            "Then re-run this script."
        )
        sys.exit(1)

    if not ENSEMBLE_CSV.exists():
        print(f"ERROR: {ENSEMBLE_CSV} not found.")
        sys.exit(1)

    print(f"Loading Ch1 ensemble from {ENSEMBLE_CSV.name}...")
    D_samples = _load_ch1_distances(ENSEMBLE_CSV)
    print(f"  {len(D_samples):,} Ch1 Mahalanobis distances computed")

    print(f"Loading Ch2 bootstrap EG samples from {BOOTSTRAP_NPY.name}...")
    boot_eg = np.load(BOOTSTRAP_NPY)
    print(f"  {len(boot_eg):,} Ch2 bootstrap EG draws loaded")

    n = min(len(D_samples), len(boot_eg))
    if n < 100:
        print(f"WARNING: only {n} samples available for correlation — result unreliable.")

    rho, pval = spearmanr(D_samples[:n], boot_eg[:n])
    print(f"\nSpearman ρ(Ch1-D, Ch2-EG) = {rho:.4f}  p = {pval:.4f}  n = {n:,}")

    if abs(rho) < RHO_THRESHOLD:
        conclusion = (
            f"Channels are empirically near-independent (|ρ| = {abs(rho):.4f} < {RHO_THRESHOLD}). "
            "Fisher combination claim is defensible for this dataset."
        )
    else:
        conclusion = (
            f"WARNING: |ρ| = {abs(rho):.4f} exceeds {RHO_THRESHOLD} threshold. "
            "Review Fisher combination claim — channels may not be approximately independent. "
            "Note: positive correlation makes Fisher conservative (lower-bounds joint significance)."
        )
    print(conclusion)

    result_block = (
        f"\n## Empirical result (2026-05-09)\n\n"
        f"Script: `validate_fisher_independence.py`\n\n"
        f"- Ch1: Mahalanobis distances from {ENSEMBLE_CSV.name} ({len(D_samples):,} draws)\n"
        f"- Ch2: Bootstrap EG samples from {BOOTSTRAP_NPY.name} ({len(boot_eg):,} draws)\n"
        f"- n used for correlation: {n:,}\n\n"
        f"**Spearman ρ = {rho:.4f}   p = {pval:.4f}**\n\n"
        f"{conclusion}\n\n"
        f"*Updated: 2026-05-09*\n"
    )

    existing = DEFENSE_DOC.read_text(encoding="utf-8")
    if "## Empirical result" in existing:
        print("\nNOTE: 'Empirical result' section already exists in fisher_independence_defense.md")
        print("      Update it manually if needed.")
    else:
        DEFENSE_DOC.write_text(existing.rstrip() + "\n" + result_block, encoding="utf-8")
        print(f"\nResults appended to {DEFENSE_DOC.name}")


if __name__ == "__main__":
    main()
