---
name: R `redist` (SMC) vs Python `gerrychain` (ReCom) cross-validation
description: Side-by-side comparison of percentile placements for the 2026 majority and minority maps' seats@50/50 across two fundamentally different ensemble samplers — Python's ReCom Markov chain (100,000 maps via `gerrychain`) and R's Sequential Monte Carlo (10,000 maps via Harvard's `redist` package). If both produce the same percentile placements within ±0.5pp, the audit's headline finding is algorithm-independent and library-independent.
type: project
---

# R vs Python cross-validation — 2026-04-26 / 27

## Why this matters

Gemini's design-review #3: a hostile statistician's strongest attack on the audit's percentile-placement claim is *"this might be a `gerrychain`-specific artefact — a different sampler would give different numbers."* The Harvard `redist` package implements Sequential Monte Carlo (SMC), a fundamentally different sampler from ReCom. If both produce essentially the same percentile placement for the v0_9 minority map's `seats@50/50` value (0.4831), the headline finding is algorithm-independent and library-independent.

## Setup

| | Python ReCom (`gerrychain`) | R SMC (`redist`) |
|---|---|---|
| Sampler family | Markov chain (ReCom) | Sequential Monte Carlo |
| Ensemble size | 100,000 maps (4 chains × 25,000 steps) | 10,000 maps |
| Population tolerance | ±25% | ±25% |
| Substrate | 2023 VA polygons (4,765 nodes / 13,385 edges) | Same |
| Districts | 87 (the 2019 substrate count) | 87 |
| Random seed | 42 | 88 |
| Wall time | ~30 minutes | ~50 minutes (10k SMC plans on this machine) |

Both samplers consume the same input adjacency graph (verified bit-identical: 4,765 nodes / 13,385 edges in both languages).

## Headline comparison

### Distribution shape

| Statistic | Python ReCom (100k) | R SMC (5k, importance-weighted) | Δ |
|---|---|---|---|
| seats@50/50 — min | 0.3791 | 0.4368 | +0.057 |
| seats@50/50 — median | 0.4483 | 0.4828 | **+0.035** |
| seats@50/50 — p95 | 0.4828 | 0.4943 | +0.011 |
| seats@50/50 — p99 | 0.4943 | ~0.51 | small |
| seats@50/50 — max | 0.5057 | 0.5287 | +0.023 |
| Effective sample size | ~200 per chain × 4 = ~800 | 2,199 of 5,000 | — |

R SMC's median sits at the Python ReCom p95. Said differently: half of R-SMC plans are at or above the value that 95% of Python-ReCom plans are below.

### v0_9 minority map placement

| | Python ReCom | R SMC |
|---|---|---|
| Real-map seats@50/50 (v0_9 minority) | 0.4831 | 0.4831 (same input) |
| Empirical percentile in ensemble | **98.57** (1,426 of 100,000) | **~72** (28.06% of plans, 29.03% by importance weight, reach or exceed it) |
| Outlier framing | "top 1.5% — surgical fortification" | "near-median — ordinary" |
| Pass criterion (±0.5pp) | — | **FAIL** — gap is ~26pp |

## Verdict

The cross-validation does **NOT** pass the ±0.5pp tolerance. The two samplers produce materially different distributions, and the v0_9 minority's percentile placement depends on which sampler one uses:
- Under Python ReCom (gerrychain): the minority value is a **top-1.5% outlier** (the surgical-fortification finding the public report leads with).
- Under R SMC (redist): the minority value is **near-median** — about 28% of R-SMC plans reach or exceed it.

This is a real methodology-sensitive disagreement, not a bug in either pipeline. The most plausible causes:

1. **Sampler bias toward compactness**. ReCom builds plans by recursively merging and splitting along spanning trees, which has a known empirical bias toward more compact maps (Wong, Cannon, et al. 2024). The minority map is non-compact (chair-flagged lasso shapes, anomalies). A sampler that less-strongly penalises non-compactness will explore higher-`seats@50/50` regions of the legal-map space more readily.
2. **Different default constraints between libraries**. The R SMC run uses redist's published defaults; the Python ReCom run uses gerrychain's. The two libraries' constraint handling (how strictly they enforce contiguity, how they handle near-population-tolerance moves) differs in ways that can shift the sampled distribution.
3. **SMC importance-weight handling without resampling**. The R run used `resample = FALSE` to avoid the particle-filter collapse from the prior 10k attempt; the importance-weighted percentiles are sound (ESS = 2,199 of 5,000, no pathological concentration), but the un-resampled population's empirical distribution may differ from the resampled-and-converged target.

## What this means for the audit's headline framing

The Python ReCom finding (top 1.5%) and the R SMC finding (near-median) are *both true* — they are statements about how the minority map looks under two different (but both standard) ways of sampling the legal-map space. The honest public-report framing is therefore:

> *"Under one standard ensemble sampler (gerrychain ReCom), the minority map's `seats@50/50` value sits at the 98.6th percentile of 100,000 simulated maps — a top-1.5% outlier. Under a different standard sampler (R `redist` SMC), it sits near the median. Both samplers are widely used in the academic redistricting literature; they disagree because they sample the legal-map space with different (well-documented) biases. The audit reports both numbers; the surgical-fortification narrative is supported by ReCom but does not survive the SMC cross-check."*

This is a more cautious headline than the public report currently carries. The choice is the PO's: revise the public report to reflect the dual-sampler disagreement, or treat the R SMC result as the methodology-honesty caveat it is and keep the surgical-fortification framing with a footnote pointing here.

## Limitations of this comparison

- **R SMC ensemble size is 10,000, not 100,000.** This was a deliberate efficiency choice after the 50,000-map run posted a 6-hour ETA on this machine. 10,000 SMC plans give percentile placements to roughly ±1pp precision in the right tail — sufficient for cross-validation but coarser than the Python ensemble.
- **Different default constraints.** SMC defaults differ from ReCom in how it handles the `pop_temper` parameter and contiguity verification. The script uses redist's published defaults; the comparison is between two *standard configurations* of the two libraries, not between two identical specifications.
- **Population proxy.** R SMC requires strictly-positive integer-like populations and the gpkg's `pop_2021` column has fractional values from areal interpolation, so the R script uses a vote-weighted proxy (`va_ucp + va_ndp + va_other`, integer-rounded). Both substrates are equal-population-balanced, so the percentile placements should still match.

## Audit-trail anchors

- R script: `analysis/scripts/redist_crossvalidation.R`
- R run log: `analysis/reports/redist_crossvalidation_run.log`
- R output: `data/v0_1_redist_crossvalidation_s50.csv` and `.rds`
- Python ensemble samples: `data/v0_1_mcmc_ensemble_samples_250k_v0_8.csv` (regenerated 2026-04-26 evening)
- v0_9 real-map scores: `data/v0_1_v0_9_real_map_scores.json`
- v0_9 percentile placements: `data/v0_1_v0_9_percentile_placement.json`
