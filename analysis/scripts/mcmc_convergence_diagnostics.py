"""Per-chain ESS and Gelman-Rubin R-hat for the corrected 2M MCMC ensemble.

Addresses Gemini's design-review #1 (statistical defensibility): the
audit's prior pooled-ensemble ESS computation inflated n_eff by treating
the concatenated 4-chain DataFrame as a single time series. Per-chain
ESS is the honest unit of information; Gelman-Rubin R-hat across chains
is the standard convergence diagnostic the academic redistricting
literature expects.

Inputs:  data/mcmc_checkpoints_250k_v0_8/chain{0..3}_samples.csv
Outputs: data/v0_1_mcmc_convergence_diagnostics_per_chain.json

Usage:
    python analysis/scripts/v0_1_mcmc_convergence_diagnostics.py

Re-runnable: works against a partial run (any sample count >= 4 per chain).
The script reports the sample count used per chain so a later check can
distinguish in-progress diagnostics from final-run diagnostics.
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mcmc_ensemble_100k import autocorrelation_ess

REPO_ROOT = HERE.parent.parent
CHECKPOINT_DIR = REPO_ROOT / "data" / "mcmc_checkpoints_250k_v0_8"
OUT_JSON = REPO_ROOT / "data" / "v0_1_mcmc_convergence_diagnostics_per_chain.json"

METRICS = ("efficiency_gap", "mean_median", "declination", "seats_at_50_50")


def gelman_rubin_rhat(chains: list[np.ndarray]) -> dict:
    """Standard Gelman-Rubin (1992) potential-scale-reduction factor.

    chains: list of 1D arrays, each one a per-chain time series of one
    metric. Chains must be the same length (truncated to the shortest
    if not). Returns Rhat plus the building blocks (B, W, V_hat) so a
    reviewer can audit the math.

    Convergence convention: Rhat < 1.1 is the typical publish-grade
    threshold; Rhat < 1.05 is the gold standard.
    """
    cleaned = [np.asarray(c, dtype=float) for c in chains]
    cleaned = [c[~np.isnan(c)] for c in cleaned]
    m = len(cleaned)
    if m < 2:
        return {"m": m, "n": 0, "rhat": float("nan"),
                "B": float("nan"), "W": float("nan"), "V_hat": float("nan"),
                "note": "Rhat needs at least 2 chains"}
    n = min(len(c) for c in cleaned)
    if n < 4:
        return {"m": m, "n": int(n), "rhat": float("nan"),
                "B": float("nan"), "W": float("nan"), "V_hat": float("nan"),
                "note": "Rhat needs at least 4 samples per chain"}
    # Truncate all chains to the shortest length so within-chain variance
    # is computed over identical sample counts (standard practice).
    arr = np.array([c[:n] for c in cleaned])  # shape (m, n)

    # Per-chain mean and variance (s_j^2 uses n-1 denominator)
    chain_means = arr.mean(axis=1)
    chain_vars = arr.var(axis=1, ddof=1)
    overall_mean = chain_means.mean()

    # B/n is the variance of chain means; B is that times n
    between = (n / (m - 1)) * np.sum((chain_means - overall_mean) ** 2)
    # W is the average within-chain variance
    within = chain_vars.mean()

    if within <= 0 or not np.isfinite(within):
        return {"m": m, "n": int(n), "rhat": float("nan"),
                "B": float(between), "W": float(within), "V_hat": float("nan"),
                "note": "W is zero or non-finite (chain may be degenerate)"}

    # V-hat: pooled estimate of the marginal posterior variance
    v_hat = ((n - 1) / n) * within + (1.0 / n) * between
    rhat = float(np.sqrt(v_hat / within))

    return {
        "m": int(m),
        "n": int(n),
        "rhat": rhat,
        "B": float(between),
        "W": float(within),
        "V_hat": float(v_hat),
        "chain_means": [float(x) for x in chain_means],
        "chain_vars": [float(x) for x in chain_vars],
    }


def main() -> int:
    print(f"[diagnostics] reading per-chain CSVs from {CHECKPOINT_DIR}")
    chain_paths = sorted(CHECKPOINT_DIR.glob("chain*_samples.csv"))
    if len(chain_paths) < 2:
        raise RuntimeError(
            f"Need at least 2 per-chain CSVs in {CHECKPOINT_DIR}, "
            f"found {len(chain_paths)}"
        )
    chain_dfs = [pd.read_csv(p) for p in chain_paths]
    chain_lengths = [len(df) for df in chain_dfs]
    print(f"[diagnostics] loaded {len(chain_dfs)} chains: lengths={chain_lengths}")

    out: dict = {
        "n_chains": len(chain_dfs),
        "chain_lengths": chain_lengths,
        "min_chain_length": min(chain_lengths),
        "metrics": {},
    }

    for metric in METRICS:
        per_chain_ess = []
        for i, df in enumerate(chain_dfs):
            if metric not in df.columns:
                raise KeyError(f"{metric} missing from chain{i}_samples.csv columns: {list(df.columns)}")
            d = autocorrelation_ess(df[metric].to_numpy())
            d["chain_idx"] = i
            per_chain_ess.append(d)

        # Gelman-Rubin Rhat across chains
        rhat = gelman_rubin_rhat([df[metric].to_numpy() for df in chain_dfs])

        # Pooled ESS for comparison with the audit's earlier (concatenated) figure
        pooled = autocorrelation_ess(
            pd.concat([df[metric] for df in chain_dfs], ignore_index=True).to_numpy()
        )

        per_chain_neff_total = sum(
            (d["n_eff"] for d in per_chain_ess if np.isfinite(d.get("n_eff", float("nan"))))
        )
        worst_per_chain_ess = min(
            (d["n_eff"] for d in per_chain_ess if np.isfinite(d.get("n_eff", float("nan")))),
            default=float("nan"),
        )
        out["metrics"][metric] = {
            "per_chain": per_chain_ess,
            "per_chain_neff_total": float(per_chain_neff_total),
            "worst_per_chain_ess": float(worst_per_chain_ess),
            "pooled_ess_inflated_estimate": pooled,
            "gelman_rubin": rhat,
        }

        rhat_val = rhat.get("rhat", float("nan"))
        verdict = (
            "GOLD < 1.05" if rhat_val < 1.05
            else "PUBLISH < 1.10" if rhat_val < 1.10
            else "REVISE >= 1.10"
        ) if np.isfinite(rhat_val) else "N/A"
        print(f"  {metric:18s}  worst-chain ESS={worst_per_chain_ess:>9.1f}  "
              f"sum-per-chain ESS={per_chain_neff_total:>10.1f}  "
              f"pooled (inflated) ESS={pooled.get('n_eff', float('nan')):>10.1f}  "
              f"Rhat={rhat_val:.4f}  [{verdict}]")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2))
    print(f"[diagnostics] wrote {OUT_JSON.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
