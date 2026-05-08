#!/usr/bin/env python
from __future__ import annotations
"""
v0_1_simulation_multichain_ensemble.py
=================================
Multi-chain ReCom MCMC for Alberta 4,765-VA substrate with Gelman-Rubin
convergence diagnostic. Addresses Gemini red-team Phase D.2 and the
ESS~150 vulnerability from red-team finding S2-01/S3-02.

Runs N independently-seeded chains (default 3) of M ReCom proposals each
(default 30000 per chain; user-adjustable). Computes split-chain R-hat
per metric per Gelman et al. (2013, *Bayesian Data Analysis*, 3rd ed.,
chap. 11) and produces a pooled ensemble with combined ESS target > 1000
per metric.

Chain independence is enforced by:
  1. Per-chain `numpy.random.default_rng(seed)` for any local stochastic
     draws performed by this script.
  2. Per-chain `np.random.seed(seed)` and `random.seed(seed)` applied
     immediately before each chain start so the gerrychain internal RNGs
     (which use the module-level generators) draw from disjoint streams
     by construction.

Why split-chain R-hat?
----------------------
The 2013 Gelman et al. split-chain diagnostic halves each chain and
treats the 2N halves as independent sequences. This catches
within-chain non-stationarity (e.g. slow drift from the 2019 seed) that
naive between-chain R-hat misses.

Outputs:
    data/simulation_multichain_samples.csv        # per-chain per-step samples (post-burnin)
    data/simulation_multichain_pooled.csv         # thinned + pooled
    data/simulation_multichain_rhat.json          # per-metric R-hat + ESS
    data/simulation_multichain_summary.md         # human-readable summary

CLI:
    python v0_1_simulation_multichain_ensemble.py --seeds 42,101,2024 --steps 30000
    python v0_1_simulation_multichain_ensemble.py --seeds 42,101,2024 --steps 100000  # publication grade

Forward: analysis/v0_1_mcmc_multichain_writeup.md (to be authored once run)
Backward:
  data/va_polygons_with_2023_votes.gpkg
  data/va_pop_from_das.csv
  analysis/scripts/v0_1_mcmc_ensemble.py (build_va_graph, run_ensemble, seat_results)
  analysis/scripts/v0_1_mcmc_full_coverage_rescore_100k.py (efficiency_gap, mean_median,
                                                    declination, seats_at_50_50)
  gerrychain, numpy, pandas
"""

# Version: 0.1 series  (last updated 2026-04-26)


import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import argparse
import json
import os
import random as _random
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse the graph-building + chain-running infrastructure from the single-chain
# script (which already handles seed-partition fallback via recursive_tree_part,
# updaters, pop_deviation=0.25, etc.).
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mcmc_ensemble import (  # noqa: E402
    build_va_graph,
    initial_assignment_2019,
    run_ensemble,
    seat_results,
)
from gerrychain.tree import recursive_tree_part  # noqa: E402

# The rescore script exposes DataFrame-shaped metric fns. We don't strictly need
# them for per-step scoring (run_ensemble/seat_results already yield all four
# metrics per step), but we import them so the one-to-one equivalence between
# streaming metrics and post-hoc pooled metrics is documented in imports — and
# so future maintainers see the canonical source of the metric definitions.
from mcmc_full_coverage_rescore_100k import (  # noqa: E402, F401
    efficiency_gap,
    mean_median,
    declination,
    seats_at_50_50,
)

ROOT = HERE.parent.parent  # scripts/ -> analysis/ -> repo root
DATA = data_loader._resolve_path("data")
DATA.mkdir(parents=True, exist_ok=True)

SAMPLES_CSV = DATA / "simulation_multichain_samples.csv"
POOLED_CSV = DATA / "simulation_multichain_pooled.csv"
RHAT_JSON = DATA / "simulation_multichain_rhat.json"
SUMMARY_MD = DATA / "simulation_multichain_summary.md"

METRIC_KEYS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
METRIC_LABELS = {
    "efficiency_gap": "Efficiency gap (UCP-favoured if positive)",
    "mean_median": "Mean-median (UCP share; UCP-favoured if positive)",
    "declination": "Declination (UCP-favoured if positive)",
    "seats_at_50_50": "UCP seat share at 50/50 vote (uniform swing)",
}

# Thresholds
R_HAT_CONVERGED = 1.01  # strict target from Gelman et al. 2013
R_HAT_ACCEPTABLE = 1.05  # soft threshold still acceptable
R_HAT_FAIL = 1.10  # above this => non-converged
COMBINED_ESS_TARGET = 1000


# ---------------------------------------------------------------------------
# Autocorrelation / ESS (Geyer initial-positive-sequence) per chain
# ---------------------------------------------------------------------------


def autocorrelation_ess(x: np.ndarray, max_lag: int | None = None) -> dict:
    """Integrated autocorrelation time and effective sample size for a single
    1-D chain segment.

    Uses Geyer (1992) initial-positive-sequence truncation: sum autocorrelations
    from lag 1 upward until the first non-positive autocorrelation (the Markov
    chain has "lost" reversible contribution after that lag).

    Returns dict with n, tau, n_eff, max_lag_used, rho_lag_{1,10,100}.
    """
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 4:
        return {
            "n": int(n),
            "tau": float("nan"),
            "n_eff": float("nan"),
            "max_lag_used": 0,
            "rho_lag_1": float("nan"),
            "rho_lag_10": float("nan"),
            "rho_lag_100": float("nan"),
        }

    x_centered = x - x.mean()
    var0 = float(np.dot(x_centered, x_centered) / n)
    if var0 == 0 or not np.isfinite(var0):
        return {
            "n": int(n),
            "tau": float("nan"),
            "n_eff": float("nan"),
            "max_lag_used": 0,
            "rho_lag_1": float("nan"),
            "rho_lag_10": float("nan"),
            "rho_lag_100": float("nan"),
        }

    if max_lag is None:
        max_lag = min(n // 4, 2000)

    acf = np.empty(max_lag + 1, dtype=float)
    acf[0] = 1.0
    for k in range(1, max_lag + 1):
        cov = float(np.dot(x_centered[:-k], x_centered[k:]) / n)
        acf[k] = cov / var0

    tau = 1.0
    used_lag = max_lag
    for k in range(1, max_lag + 1):
        if acf[k] <= 0:
            used_lag = k - 1
            break
        tau += 2.0 * acf[k]

    n_eff = n / tau if tau > 0 else float("nan")
    return {
        "n": int(n),
        "tau": float(tau),
        "n_eff": float(n_eff),
        "max_lag_used": int(used_lag),
        "rho_lag_1": float(acf[1]) if max_lag >= 1 else float("nan"),
        "rho_lag_10": float(acf[10]) if max_lag >= 10 else float("nan"),
        "rho_lag_100": float(acf[100]) if max_lag >= 100 else float("nan"),
    }


# ---------------------------------------------------------------------------
# Gelman-Rubin split-chain R-hat
# ---------------------------------------------------------------------------


def split_chain_rhat(chains: list[np.ndarray]) -> dict:
    """Compute split-chain R-hat per Gelman et al. (2013) BDA3 §11.4.

    Splits each of the N input chains in half -> 2N half-chains of length
    n = floor(len/2). Treats these as m=2N independent sequences.

        W     = mean of per-half-chain variances (within-chain variance)
        B     = (n / (m - 1)) * sum_j (mean_j - grand_mean)^2  (between-chain)
        V_hat = ((n-1)/n) * W + (1/n) * B
        R_hat = sqrt(V_hat / W)

    Target: R_hat < 1.01 (strict converged); < 1.05 acceptable; > 1.10 failed.

    Returns a dict with r_hat, W, B, V_hat, m (= 2N half-chains), n
    (half-chain length), and the per-half-chain means/vars for inspection.
    """
    # Drop NaNs per chain, then take the shortest length so half-chains align.
    cleaned = []
    for c in chains:
        c = np.asarray(c, dtype=float)
        c = c[~np.isnan(c)]
        cleaned.append(c)

    if any(len(c) < 4 for c in cleaned):
        return {
            "r_hat": float("nan"),
            "W": float("nan"),
            "B": float("nan"),
            "V_hat": float("nan"),
            "m_half_chains": 0,
            "n_per_half": 0,
            "half_chain_means": [],
            "half_chain_vars": [],
            "note": "chain too short for split R-hat (need >= 4 samples per chain)",
        }

    shortest = min(len(c) for c in cleaned)
    # Use even length so the split is exact. Drop trailing odd sample if needed.
    if shortest % 2 == 1:
        shortest -= 1
    if shortest < 4:
        return {
            "r_hat": float("nan"),
            "W": float("nan"),
            "B": float("nan"),
            "V_hat": float("nan"),
            "m_half_chains": 0,
            "n_per_half": 0,
            "half_chain_means": [],
            "half_chain_vars": [],
            "note": "chain too short after even-trimming",
        }

    n = shortest // 2  # per-half-chain length

    half_chains = []
    for c in cleaned:
        c_trimmed = c[:shortest]
        half_chains.append(c_trimmed[:n])
        half_chains.append(c_trimmed[n:])

    m = len(half_chains)  # = 2 * N_chains

    # Per half-chain mean and (sample) variance with ddof=1 per BDA3.
    means = np.array([np.mean(hc) for hc in half_chains], dtype=float)
    vars_ = np.array([np.var(hc, ddof=1) for hc in half_chains], dtype=float)

    grand_mean = float(np.mean(means))

    W = float(np.mean(vars_))  # within-chain variance (avg of sample vars)
    # Between-chain variance scaled by n (number of draws per half-chain):
    # B = n * sample variance of half-chain means (ddof=1).
    if m > 1:
        B = float(n * np.var(means, ddof=1))
    else:
        B = float("nan")

    if W == 0 or not np.isfinite(W):
        return {
            "r_hat": float("nan"),
            "W": float(W),
            "B": float(B),
            "V_hat": float("nan"),
            "m_half_chains": int(m),
            "n_per_half": int(n),
            "half_chain_means": [float(x) for x in means],
            "half_chain_vars": [float(x) for x in vars_],
            "note": "within-chain variance is zero or non-finite",
        }

    V_hat = ((n - 1) / n) * W + (B / n) if np.isfinite(B) else float("nan")
    r_hat = float(np.sqrt(V_hat / W)) if np.isfinite(V_hat) else float("nan")

    return {
        "r_hat": float(r_hat),
        "W": float(W),
        "B": float(B),
        "V_hat": float(V_hat),
        "m_half_chains": int(m),
        "n_per_half": int(n),
        "grand_mean": grand_mean,
        "half_chain_means": [float(x) for x in means],
        "half_chain_vars": [float(x) for x in vars_],
    }


# ---------------------------------------------------------------------------
# Per-chain execution
# ---------------------------------------------------------------------------


def run_one_chain(
    graph,
    assignment,
    seed: int,
    n_steps: int,
    chain_idx: int,
    effective_seed: int | None = None,
) -> pd.DataFrame:
    """Run a single ReCom chain, seeding RNGs immediately before the chain loop.

    We seed BOTH numpy's global RNG and python's `random` module before calling
    run_ensemble, because gerrychain's internal proposal code uses those module-
    level generators. Independent seeds across chains therefore yield
    independent streams.

    `seed` is the user-facing seed recorded in the output DataFrame (for
    reporting/reviewer reproducibility).  `effective_seed` is the seed actually
    used to initialise numpy/random — defaults to `seed` but can be overridden
    on retry so the regen-RNG path explores a different neighbourhood.

    Returns a per-step DataFrame with schema:
      chain_idx, seed, step, efficiency_gap, mean_median, declination, seats_at_50_50
    """
    eff = effective_seed if effective_seed is not None else seed
    print(
        f"\n[{time.strftime('%H:%M:%S')}] === chain {chain_idx + 1} "
        f"(seed={seed}, effective_seed={eff}, steps={n_steps}) ==="
    )
    t0 = time.time()

    # Seed before the chain starts so gerrychain's internal RNG usage is
    # deterministic per (effective_seed, initial-state, graph).
    np.random.seed(eff)
    _random.seed(eff)

    rows = run_ensemble(graph, assignment, n_steps)

    df = pd.DataFrame(rows)
    # run_ensemble returns full seat_results dicts; keep only metric + step cols
    # and annotate with chain identity.
    keep = ["step"] + METRIC_KEYS
    df = df[keep].copy()
    df.insert(0, "chain_idx", int(chain_idx))
    df.insert(1, "seed", int(seed))

    elapsed = time.time() - t0
    print(
        f"[{time.strftime('%H:%M:%S')}] chain {chain_idx + 1} done: "
        f"{len(df)} samples in {elapsed:.0f}s "
        f"({elapsed / max(1, len(df)) * 1000:.1f} ms/step)"
    )
    return df


# ---------------------------------------------------------------------------
# Per-metric diagnostics assembly
# ---------------------------------------------------------------------------


def diagnose_metric(metric: str, per_chain_arrays: list[np.ndarray]) -> dict:
    """Run the full diagnostic battery for a single metric:

    - Per-chain ESS (autocorrelation_ess)
    - Split-chain R-hat across chains
    - Combined ESS = sum of per-chain n_eff (chains are independent)
    - Thinning factor = floor(max per-chain tau / 10) if max tau > 100
    - Convergence flag (R_hat < R_HAT_ACCEPTABLE AND combined ESS >= 1000)
    """
    per_chain_diag = [autocorrelation_ess(arr) for arr in per_chain_arrays]
    per_chain_ess = [
        float(d["n_eff"]) if np.isfinite(d["n_eff"]) else float("nan")
        for d in per_chain_diag
    ]
    per_chain_tau = [
        float(d["tau"]) if np.isfinite(d["tau"]) else float("nan")
        for d in per_chain_diag
    ]

    # Combined ESS: chains are independent after per-chain burn-in.
    combined_ess = float(np.nansum(per_chain_ess))

    rhat = split_chain_rhat(per_chain_arrays)

    # Thinning factor for pooled CSV construction.
    finite_taus = [t for t in per_chain_tau if np.isfinite(t)]
    max_tau = max(finite_taus) if finite_taus else float("nan")
    if np.isfinite(max_tau) and max_tau > 100:
        thinning_factor = int(max(1, np.floor(max_tau / 10)))
    else:
        thinning_factor = 1

    r_hat_val = rhat["r_hat"]
    converged = (
        np.isfinite(r_hat_val)
        and r_hat_val < R_HAT_ACCEPTABLE
        and np.isfinite(combined_ess)
        and combined_ess >= COMBINED_ESS_TARGET
    )

    return {
        "r_hat": r_hat_val,
        "r_hat_W": rhat["W"],
        "r_hat_B": rhat["B"],
        "r_hat_V_hat": rhat["V_hat"],
        "r_hat_m_half_chains": rhat["m_half_chains"],
        "r_hat_n_per_half": rhat["n_per_half"],
        "r_hat_half_chain_means": rhat.get("half_chain_means", []),
        "r_hat_note": rhat.get("note", ""),
        "per_chain_n": [int(d["n"]) for d in per_chain_diag],
        "per_chain_tau": per_chain_tau,
        "per_chain_ess": per_chain_ess,
        "per_chain_rho_lag_1": [float(d["rho_lag_1"]) for d in per_chain_diag],
        "per_chain_rho_lag_10": [float(d["rho_lag_10"]) for d in per_chain_diag],
        "per_chain_rho_lag_100": [float(d["rho_lag_100"]) for d in per_chain_diag],
        "combined_ess": combined_ess,
        "thinning_factor": int(thinning_factor),
        "converged": bool(converged),
    }


# ---------------------------------------------------------------------------
# Pooling + thinning
# ---------------------------------------------------------------------------


def build_pooled(
    samples_df: pd.DataFrame, per_metric: dict[str, dict]
) -> tuple[pd.DataFrame, int]:
    """Thin each chain by the MAX of the per-metric thinning factors (so the
    pooled series is valid for every metric) and concatenate.

    We use one common thinning factor across metrics to keep the pooled CSV's
    row-wise interpretation clean — each pooled row is a single plan sampled
    after burn-in + thinning from some chain.

    Returns (pooled_df[METRIC_KEYS], common_thin_factor).
    """
    thin_factors = [per_metric[m]["thinning_factor"] for m in METRIC_KEYS]
    common_thin = int(max(thin_factors)) if thin_factors else 1
    if common_thin < 1:
        common_thin = 1

    pooled_parts = []
    for chain_idx, g in samples_df.groupby("chain_idx", sort=True):
        g = g.sort_values("step").reset_index(drop=True)
        thinned = g.iloc[::common_thin]
        pooled_parts.append(thinned[METRIC_KEYS])
    pooled = pd.concat(pooled_parts, ignore_index=True)
    return pooled, common_thin


# ---------------------------------------------------------------------------
# Markdown summary
# ---------------------------------------------------------------------------


def write_summary_md(
    out_path: Path,
    seeds: list[int],
    steps_per_chain: int,
    burnin_fraction: float,
    per_metric: dict[str, dict],
    overall_converged: bool,
    max_r_hat: float,
    common_thin_factor: int,
    total_runtime_sec: float,
) -> None:
    def verdict_str(d: dict) -> str:
        r = d["r_hat"]
        ess = d["combined_ess"]
        if not np.isfinite(r):
            return "INDETERMINATE (R-hat not finite)"
        if r < R_HAT_CONVERGED and ess >= COMBINED_ESS_TARGET:
            return (
                f"CONVERGED (R-hat<{R_HAT_CONVERGED:.2f}, ESS>={COMBINED_ESS_TARGET})"
            )
        if r < R_HAT_ACCEPTABLE and ess >= COMBINED_ESS_TARGET:
            return (
                f"ACCEPTABLE (R-hat<{R_HAT_ACCEPTABLE:.2f}, ESS>={COMBINED_ESS_TARGET})"
            )
        if r >= R_HAT_FAIL:
            return f"NOT CONVERGED (R-hat>={R_HAT_FAIL:.2f})"
        if ess < COMBINED_ESS_TARGET:
            return f"UNDER-SAMPLED (combined ESS {ess:.0f} < {COMBINED_ESS_TARGET})"
        return "MARGINAL"

    lines: list[str] = []
    lines.append("# Multi-chain MCMC convergence summary\n")
    lines.append(
        f"**Script:** `analysis/scripts/v0_1_simulation_multichain_ensemble.py`\n"
    )
    lines.append(f"**Seeds:** {seeds}  \n")
    lines.append(f"**Chains:** {len(seeds)}  \n")
    lines.append(f"**Steps per chain:** {steps_per_chain:,}  \n")
    lines.append(f"**Burn-in fraction:** {burnin_fraction:.0%}  \n")
    lines.append(f"**Common thinning factor (pooled CSV):** {common_thin_factor}  \n")
    lines.append(
        f"**Total runtime:** {total_runtime_sec:.0f}s "
        f"({total_runtime_sec/60:.1f} min)\n"
    )
    lines.append("")
    lines.append("## Per-metric diagnostics\n")
    lines.append(
        "| Metric | R-hat (split) | Per-chain ESS | Combined ESS " "| Thin | Verdict |"
    )
    lines.append("|---|---:|---|---:|---:|---|")
    for m in METRIC_KEYS:
        d = per_metric[m]
        ess_list = ", ".join(
            f"{e:.0f}" if np.isfinite(e) else "NaN" for e in d["per_chain_ess"]
        )
        r = d["r_hat"]
        r_str = f"{r:.4f}" if np.isfinite(r) else "NaN"
        lines.append(
            f"| {m} | {r_str} | [{ess_list}] | {d['combined_ess']:.0f} "
            f"| {d['thinning_factor']} | {verdict_str(d)} |"
        )
    lines.append("")

    # Overall verdict
    lines.append("## Overall verdict\n")
    if overall_converged:
        lines.append(
            f"**CONVERGED.** All four metrics satisfy R-hat < {R_HAT_ACCEPTABLE} "
            f"(max R-hat = {max_r_hat:.4f}) and combined ESS >= "
            f"{COMBINED_ESS_TARGET}. The pooled ensemble can be used as the "
            f"reference distribution for the paper's S5.4 percentile claims, "
            f"and the chain's stationary distribution is plausibly a fair "
            f"representation of the neighbourhood of legal plans reachable "
            f"from the 2019 seed under ReCom with pop deviation <= 0.25.\n"
        )
    else:
        lines.append(
            f"**NOT CONVERGED.** Max R-hat = {max_r_hat:.4f} "
            f"(threshold {R_HAT_ACCEPTABLE}), or one or more metrics have "
            f"combined ESS < {COMBINED_ESS_TARGET}. The paper's S5.4 "
            f"percentile claims cannot rest on this ensemble alone; either "
            f"extend each chain (more ReCom proposals per chain — ESS scales "
            f"roughly linearly with chain length) or add additional seeds. A "
            f"practical escalation is to increase `--steps` by 3-10x and "
            f"re-run.\n"
        )
    lines.append("")

    # Threshold rationale
    lines.append("## Threshold rationale\n")
    lines.append(
        f"- **R-hat < {R_HAT_CONVERGED}:** strict Gelman-Rubin criterion "
        f"(Gelman et al. 2013, *BDA3* ch. 11). Indicates within-chain and "
        f"between-chain variability are statistically indistinguishable.\n"
        f"- **R-hat < {R_HAT_ACCEPTABLE}:** widely-used soft threshold "
        f"(e.g. PyMC, Stan default warning at 1.05). We treat this as the "
        f"minimum acceptable criterion for publication-grade claims.\n"
        f"- **R-hat >= {R_HAT_FAIL}:** chains have not mixed; reported "
        f"percentiles are not reliable.\n"
        f"- **Combined ESS >= {COMBINED_ESS_TARGET}:** gives Monte Carlo "
        f"standard error on any metric of roughly sigma / sqrt(ESS), so a "
        f"5th-percentile estimate has approx ±1-2 percentile-point noise. "
        f"Below 1000, percentile claims are under-powered.\n"
    )
    lines.append("")

    # Implications for §5.4 if converged
    lines.append("## Implications for paper S5.4\n")
    if overall_converged:
        lines.append(
            "The pooled ensemble in `data/simulation_multichain_pooled.csv` "
            "(thinned to approximately-independent draws) is the correct "
            "reference distribution for reporting percentile ranks of the "
            "2019 enacted map and the two 2026 proposals. Standard "
            "bootstrap CIs on the reported 5th/95th percentiles are now "
            "valid because the effective sample size exceeds 1000 per "
            "metric.\n"
        )
    else:
        lines.append(
            "The paper's S5.4 percentile claims should be held until the "
            "ensemble converges. Either rerun with larger `--steps` "
            "(recommended: 3x current) or flag the percentile claims "
            "explicitly as preliminary pending convergence.\n"
        )
    lines.append("")

    # Audit trail
    lines.append("## Reproducibility\n")
    lines.append("```bash")
    seeds_str = ",".join(str(s) for s in seeds)
    lines.append(
        f"python analysis/scripts/v0_1_simulation_multichain_ensemble.py "
        f"--seeds {seeds_str} --steps {steps_per_chain} "
        f"--burnin {burnin_fraction}"
    )
    lines.append("```\n")
    lines.append(
        "Independent seeds ensure a peer reviewer can rerun with any "
        "permutation of seeds and, if the ensemble has converged, obtain "
        "statistically indistinguishable percentile ranks.\n"
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------


def parse_seeds(s: str) -> list[int]:
    parts = [p.strip() for p in s.split(",") if p.strip()]
    if not parts:
        raise argparse.ArgumentTypeError("--seeds must have at least one integer")
    try:
        return [int(p) for p in parts]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"--seeds must be comma-separated integers; got {s!r}"
        ) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Multi-chain ReCom MCMC with Gelman-Rubin split-chain R-hat "
            "for Alberta VA substrate."
        )
    )
    parser.add_argument(
        "--seeds",
        type=parse_seeds,
        default=[42, 101, 2024],
        help="Comma-separated integers, one per chain. Default: 42,101,2024.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=30000,
        help="ReCom proposals per chain. Default: 30000.",
    )
    parser.add_argument(
        "--burnin",
        type=float,
        default=0.10,
        help=(
            "Fraction of each chain discarded as burn-in before diagnostics. "
            "Default: 0.10 (i.e. first 10%% of each chain)."
        ),
    )
    args = parser.parse_args(argv)

    seeds: list[int] = args.seeds
    n_steps: int = args.steps
    burnin_fraction: float = args.burnin

    if burnin_fraction < 0.0 or burnin_fraction >= 1.0:
        parser.error("--burnin must be in [0.0, 1.0)")

    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

    t_start = time.time()
    print("=" * 72)
    print("Multi-chain ReCom MCMC — Alberta 4,765-VA substrate")
    print("=" * 72)
    print(f"  seeds:              {seeds}")
    print(f"  steps per chain:    {n_steps:,}")
    print(f"  burn-in fraction:   {burnin_fraction:.0%}")
    print(f"  n_chains:           {len(seeds)}")
    print(f"  total proposals:    {len(seeds) * n_steps:,}")
    print("=" * 72)

    # Build graph ONCE (shared read-only across chains).
    print(
        f"\n[{time.strftime('%H:%M:%S')}] building VA graph (shared across chains)..."
    )
    va, graph = build_va_graph()
    assignment = initial_assignment_2019(va)
    print(f"  2019 baseline districts: {len(set(assignment.values()))}")

    # Pre-generate a tight-seed partition ONCE using a known-good regen seed.
    # The 2019 enacted map violates +/-25% (max indiv dev 44.77%) so each chain
    # would otherwise trigger its own non-deterministic recursive_tree_part
    # regen — which failed on chain 2 / seed=101 in practice. Generating the
    # tight seed here with regen_seed=42 (known to succeed) and reusing it
    # means every chain starts from an identical valid partition; chain-to-
    # chain divergence is driven entirely by the per-chain ReCom proposal RNG.
    tight_regen_seed = 42
    total_pop = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
    num_dist = len(set(assignment.values()))
    ideal_pop = total_pop / num_dist
    pop_deviation = 0.25  # matches run_ensemble default
    print(
        f"\n[{time.strftime('%H:%M:%S')}] pre-generating shared tight-seed "
        f"partition (regen_seed={tight_regen_seed}, n_dist={num_dist}, "
        f"ideal_pop={ideal_pop:,.0f}, pop_deviation={pop_deviation:.0%})..."
    )
    np.random.seed(tight_regen_seed)
    _random.seed(tight_regen_seed)
    tight_assignment = recursive_tree_part(
        graph,
        parts=list(range(num_dist)),
        pop_target=ideal_pop,
        pop_col="pop_2021",
        epsilon=pop_deviation / 2.0,
        node_repeats=3,
    )
    # Quick sanity check: verify the pre-generated seed is within +/-pop_deviation
    tight_pops = {}
    for node, dist in tight_assignment.items():
        tight_pops[dist] = tight_pops.get(dist, 0.0) + graph.nodes[node]["pop_2021"]
    min_p, max_p = min(tight_pops.values()), max(tight_pops.values())
    tight_max_dev = max(abs(max_p - ideal_pop), abs(min_p - ideal_pop)) / ideal_pop
    print(
        f"  tight seed generated: pop {min_p:,.0f} - {max_p:,.0f}, "
        f"max-indiv-dev={tight_max_dev:.2%} "
        f"({'within' if tight_max_dev <= pop_deviation else 'OUTSIDE'} "
        f"+/-{pop_deviation:.0%})"
    )
    if tight_max_dev > pop_deviation:
        print(
            f"  WARNING: tight seed exceeds +/-{pop_deviation:.0%}; "
            f"run_ensemble will attempt its own regen per-chain."
        )
    else:
        # Override the assignment variable so each chain starts from the tight seed.
        assignment = tight_assignment

    # Run each chain. The 2019 enacted map violates the +/-25% ReCom constraint
    # (max indiv dev 44.77%), so run_ensemble internally regenerates a tight
    # seed via recursive_tree_part. That regen is non-deterministic and can
    # fail (it failed on chain 2 / seed=101 during the first multichain run
    # at this graph). We wrap each chain in a retry loop that swaps the
    # effective_seed (feeding a different RNG stream into recursive_tree_part)
    # up to 4 times before giving up on that chain. The reviewer-facing `seed`
    # column in the output DataFrame stays at the user-supplied seed for
    # reproducibility documentation.
    per_chain_dfs: list[pd.DataFrame] = []
    for i, seed in enumerate(seeds):
        last_err = None
        for retry_idx in range(4):
            effective_seed = seed if retry_idx == 0 else seed * 1000 + retry_idx
            try:
                df = run_one_chain(
                    graph,
                    assignment,
                    seed=seed,
                    n_steps=n_steps,
                    chain_idx=i,
                    effective_seed=effective_seed,
                )
                last_err = None
                break
            except RuntimeError as e:
                last_err = e
                print(
                    f"  chain {i + 1} (seed={seed}) regen failed on attempt "
                    f"{retry_idx + 1}/4 (effective_seed={effective_seed}): {e}. "
                    f"Retrying with a perturbed effective_seed..."
                )
        if last_err is not None:
            raise last_err
        per_chain_dfs.append(df)

    # Combine raw samples (pre-burnin) for writeout.
    full_samples_df = pd.concat(per_chain_dfs, ignore_index=True)

    # Apply burn-in: drop the first burnin_fraction of steps from each chain.
    burnin_n = int(np.floor(burnin_fraction * n_steps))
    print(
        f"\n[{time.strftime('%H:%M:%S')}] discarding first {burnin_n} steps "
        f"per chain as burn-in ({burnin_fraction:.0%} x {n_steps})"
    )

    post_burnin_dfs = []
    for df in per_chain_dfs:
        df_sorted = df.sort_values("step").reset_index(drop=True)
        post = df_sorted.iloc[burnin_n:].copy()
        post_burnin_dfs.append(post)

    post_burnin_df = pd.concat(post_burnin_dfs, ignore_index=True)
    post_burnin_df.to_csv(SAMPLES_CSV, index=False)
    print(
        f"  wrote {SAMPLES_CSV} ({len(post_burnin_df)} post-burnin samples "
        f"across {len(seeds)} chains)"
    )

    # Per-metric diagnostics on post-burnin chains.
    print(f"\n[{time.strftime('%H:%M:%S')}] computing per-metric diagnostics...")
    per_metric: dict[str, dict] = {}
    for metric in METRIC_KEYS:
        per_chain_arrays = [df[metric].to_numpy(dtype=float) for df in post_burnin_dfs]
        diag = diagnose_metric(metric, per_chain_arrays)
        per_metric[metric] = diag

        ess_list = ", ".join(
            f"{e:.0f}" if np.isfinite(e) else "NaN" for e in diag["per_chain_ess"]
        )
        r = diag["r_hat"]
        r_str = f"{r:.4f}" if np.isfinite(r) else "NaN"
        print(
            f"  {metric:<18s} R-hat={r_str}  "
            f"per-chain ESS=[{ess_list}]  combined_ESS={diag['combined_ess']:.0f}  "
            f"thin={diag['thinning_factor']}  converged={diag['converged']}"
        )

    max_r_hat = float(
        max(
            (
                per_metric[m]["r_hat"]
                for m in METRIC_KEYS
                if np.isfinite(per_metric[m]["r_hat"])
            ),
            default=float("nan"),
        )
    )
    overall_converged = all(per_metric[m]["converged"] for m in METRIC_KEYS)

    # Build pooled CSV (one common thinning factor).
    pooled_df, common_thin = build_pooled(post_burnin_df, per_metric)
    pooled_df.to_csv(POOLED_CSV, index=False)
    print(f"\n[{time.strftime('%H:%M:%S')}] wrote pooled CSV: {POOLED_CSV}")
    print(f"  common thinning factor: {common_thin}")
    print(f"  pooled rows: {len(pooled_df):,}")

    # Write R-hat JSON.
    total_runtime = time.time() - t_start
    rhat_payload = {
        "seeds": [int(s) for s in seeds],
        "n_chains": len(seeds),
        "steps_per_chain": int(n_steps),
        "burnin_fraction": float(burnin_fraction),
        "burnin_steps_per_chain": int(burnin_n),
        "post_burnin_steps_per_chain": int(n_steps - burnin_n),
        "total_proposals": int(len(seeds) * n_steps),
        "total_post_burnin_samples": int(len(post_burnin_df)),
        "pooled_samples": int(len(pooled_df)),
        "common_thin_factor": int(common_thin),
        "per_metric": per_metric,
        "overall_converged": bool(overall_converged),
        "max_r_hat": max_r_hat,
        "r_hat_converged_threshold": R_HAT_CONVERGED,
        "r_hat_acceptable_threshold": R_HAT_ACCEPTABLE,
        "r_hat_fail_threshold": R_HAT_FAIL,
        "combined_ess_target": COMBINED_ESS_TARGET,
        "total_runtime_sec": float(total_runtime),
        "script_version": "v0_1_simulation_multichain_ensemble.py",
    }
    with open(RHAT_JSON, "w", encoding="utf-8") as f:
        json.dump(rhat_payload, f, indent=2, default=float)
    print(f"[{time.strftime('%H:%M:%S')}] wrote R-hat JSON: {RHAT_JSON}")

    # Write markdown summary.
    write_summary_md(
        SUMMARY_MD,
        seeds=seeds,
        steps_per_chain=n_steps,
        burnin_fraction=burnin_fraction,
        per_metric=per_metric,
        overall_converged=overall_converged,
        max_r_hat=max_r_hat,
        common_thin_factor=common_thin,
        total_runtime_sec=total_runtime,
    )
    print(f"[{time.strftime('%H:%M:%S')}] wrote summary: {SUMMARY_MD}")

    # Final verdict line.
    print()
    print("=" * 72)
    if overall_converged:
        print(
            f"VERDICT: CONVERGED (max R-hat = {max_r_hat:.4f}, "
            f"all metrics have combined ESS >= {COMBINED_ESS_TARGET})"
        )
    else:
        print(
            f"VERDICT: NOT CONVERGED (max R-hat = {max_r_hat:.4f}; "
            f"at least one metric has combined ESS < {COMBINED_ESS_TARGET})"
        )
    print(f"Total runtime: {total_runtime:.0f}s ({total_runtime/60:.1f} min)")
    print("=" * 72)

    return 0 if overall_converged else 2


if __name__ == "__main__":
    raise SystemExit(main())
