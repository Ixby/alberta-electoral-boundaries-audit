---
name: R `redist` (SMC) vs Python `gerrychain` (ReCom) cross-validation — pre-canonical history
description: "Pre-canonical (Derived Provisional Geometry) sections of the original 2026-04-26/27 sampler cross-validation, archived 2026-05-23 because the apparent ReCom-vs-SMC disagreement they describe was substrate-driven, not sampler-driven, and did not survive canonical recomputation. The live cross-validation lives at findings/redist_python_comparison.md; this file preserves the trail-of-work record."
type: archive
---

> **Backward:**
> - `findings/redist_python_comparison.md` — live canonical-resolution file (parent / extracted from)
> - `archive/dpg_era/municipal_anchoring_analysis.md` — sibling DPG-era analysis
> - `data/logs/redist_crossvalidation_run.log` — preserves the pre-canonical run output (3rd-run stochastic outcome, 57.9%)
> - `data/v0_1_redist_crossvalidation_s50.rds` — pre-canonical run artifact (v0_1 prefix = pre-canonical naming)
>
> **Forward:**
> - (leaf — trail-of-work archive; not consumed by any live analysis. Git history is the redundant record.)

# Pre-canonical sampler cross-validation history

**Status — ARCHIVED 2026-05-23.** This document captures the pre-canonical sections of the original R `redist` SMC vs Python `gerrychain` ReCom cross-validation (`findings/redist_python_comparison.md`). The pre-canonical work surfaced an apparent sampler disagreement: under DPG geometry the v0_9 minority `seats@50/50` (0.4831) placed at ReCom p98.6 but R-SMC near-median (~p72), failing the ±0.5 pp cross-validation tolerance. The 2026-05-18 canonical re-run on official Elections Alberta shapefiles resolved the disagreement: the gap was driven by the DPG substrate, not by the samplers — on canonical geometry both samplers agree the minority is an extreme outlier. The pre-canonical sections were extracted from the live file on 2026-05-23 and preserved here for trail-of-work transparency. Read the live file at `findings/redist_python_comparison.md` for the current state.

## Why this matters (pre-canonical framing, 2026-04-26)

Gemini's design-review #3: a hostile statistician's strongest attack on the audit's percentile-placement claim is *"this might be a `gerrychain`-specific artefact — a different sampler would give different numbers."* The Harvard `redist` package implements Sequential Monte Carlo (SMC), a fundamentally different sampler from ReCom. If both produce essentially the same percentile placement for the v0_9 minority map's `seats@50/50` value (0.4831), the headline finding is algorithm-independent and library-independent.

## Pre-canonical setup

*Pre-canonical (DPG-era) setup.*

| | Python ReCom (`gerrychain`) | R SMC (`redist`) |
|---|---|---|
| Sampler family | Markov chain (ReCom) | Sequential Monte Carlo |
| Ensemble size | 100,000 maps (4 chains × 25,000 steps) | 5,000 maps (`nsims = 5000` in `redist_crossvalidation.R`; a 50k attempt posted a ~6h ETA and was cancelled, a 10k attempt collapsed to 3 unique plans during late-iteration particle resampling) |
| Population tolerance | ±25% | ±25% |
| Substrate | 2023 VA polygons (4,765 nodes / 13,385 edges) | Same |
| Districts | 87 (the 2019 enacted Bill 33 substrate count, used as the seed partition) | 87 (same) |
| Random seed | 42 | 88 (pre-canonical; canonical re-run uses `set.seed(852751799)`) |
| Wall time (this machine) | ~30 minutes | ~25–50 minutes (precise wall time not preserved) |

## Pre-canonical headline comparison

### Distribution shape (DPG-era)

| Statistic | Python ReCom (100k) | R SMC (5k, importance-weighted) | Δ |
|---|---|---|---|
| seats@50/50 — min | 0.3791 | 0.4368 | +0.057 |
| seats@50/50 — median | 0.4483 | 0.4828 | **+0.035** |
| seats@50/50 — p95 | 0.4828 | 0.4943 | +0.011 |
| seats@50/50 — p99 | 0.4943 | ~0.51 | small |
| seats@50/50 — max | 0.5057 | 0.5287 | +0.023 |
| Effective sample size | ~200 per chain × 4 = ~800 | 2,199 of 5,000 | — |

R SMC's median sits at the Python ReCom p95. Said differently: half of R-SMC plans are at or above the value that 95% of Python-ReCom plans are below.

### v0_9 minority map placement (DPG-era)

| | Python ReCom | R SMC |
|---|---|---|
| Real-map seats@50/50 (v0_9 minority) | 0.4831 | 0.4831 (same input) |
| Empirical percentile in ensemble | **98.57** (1,426 of 100,000) | **~72** (28.06% of plans, 29.03% by importance weight, reach or exceed it) |
| Outlier framing | "top 1.5% — surgical fortification" | "near-median — ordinary" |
| Pass criterion (±0.5pp) | — | **FAIL** — gap is ~26pp |

## Stability caveat — R SMC results are run-stochastic (pre-canonical)

Across three runs of the R SMC script with the same nominal `set.seed(88)`, `nsims=5000`, `resample=FALSE`, `pop_temper=0`, but different library-load orderings, the fraction of plans reaching the minority's 0.4831 was:

| Run | Library load order | % of weighted plans ≥ 0.4831 |
|---|---|---|
| 1st | redist only | 28% |
| 2nd | redist + redistmetrics (no `comp_polsby` call) | 5.6% |
| 3rd | redist + redistmetrics + `comp_polsby` call | 57.9% |

This is an artefact of `library(redistmetrics)` consuming RNG state before the SMC sampler runs, shifting the random-consumption path. The qualitative finding (SMC reaches the value more often than ReCom's 1.4%) is stable across all three runs; the magnitude is not. The fix (`set.seed()` immediately before `redist_smc()` with no intervening RNG-consuming calls) is in place in the current `analysis/scripts/redist_crossvalidation.R` and was used for the 2026-05-18 canonical re-run.

## Pre-canonical disagreement-resolution analysis (DPG-era framing)

The cross-validation did **NOT** pass the ±0.5pp tolerance under DPG. The two samplers produced materially different distributions, and the v0_9 minority's percentile placement depended on which sampler one used:
- Under Python ReCom (gerrychain): the minority value was a **top-1.5% outlier** (the surgical-fortification finding the public report led with at the time).
- Under R SMC (redist): the minority value was **near-median** — about 28% of R-SMC plans reached or exceeded it.

At the time this was framed as a real methodology-sensitive disagreement, not a bug in either pipeline. The most plausible causes considered:

1. **Sampler bias toward compactness**. ReCom builds plans by recursively merging and splitting along spanning trees, which has a known empirical bias toward more compact maps (Chen 2025, "Balanced Spanning Tree Distributions Have Separation Fairness", arXiv:2509.15137; Cannon et al. 2022, "Spanning Trees and Redistricting", arXiv:2210.01401). The minority map is non-compact (chair-flagged lasso shapes, anomalies). A sampler that less-strongly penalises non-compactness would explore higher-`seats@50/50` regions of the legal-map space more readily.
2. **Different default constraints between libraries**. The R SMC run uses redist's published defaults; the Python ReCom run uses gerrychain's. The two libraries' constraint handling (how strictly they enforce contiguity, how they handle near-population-tolerance moves) differs in ways that can shift the sampled distribution.
3. **SMC importance-weight handling without resampling**. The R run used `resample = FALSE` to avoid the particle-filter collapse from the prior 10k attempt; the importance-weighted percentiles are sound (ESS = 2,199 of 5,000, no pathological concentration), but the un-resampled population's empirical distribution may differ from the resampled-and-converged target.

## Pre-canonical headline-framing recommendation (DPG-era)

At the time the prose recommended:

> *"Under one standard ensemble sampler (gerrychain ReCom), the minority map's `seats@50/50` value sits at the 98.6th percentile of 100,000 simulated maps — a top-1.5% outlier. Under a different standard sampler (R `redist` SMC), it sits near the median. Both samplers are widely used in the academic redistricting literature; they disagree because they sample the legal-map space with different (well-documented) biases. The audit reports both numbers; the surgical-fortification narrative is supported by ReCom but does not survive the SMC cross-check."*

## What the canonical recomputation resolved

The 2026-05-18 canonical re-run on official Elections Alberta shapefiles showed that the disagreement was substrate-driven: the canonical minority value (0.5169) is higher than the DPG-era value (0.4831), and on canonical geometry **both samplers agree** the minority is an extreme outlier (ReCom p99.99; R SMC 0 of 5,000 plans reached it, ensemble max 0.4943 — 2.26 pp below). The pre-canonical "sampler disagreement" was an artifact of the DPG substrate, not a property of either sampler. See `findings/redist_python_comparison.md` for the current state.

## Trail-of-work note

The Lane 2 anchoring asymmetry framing carried in the original 2026-04-26 prose (minority 14.5%, majority 71%, a 4.9× DPG-era gap) was likewise retracted on canonical recomputation. The current Lane 2 case rests on the legs that survived: urban hybridization (sampler-independent), Airdrie city-splitting (direct count), and the chair-flagged cartographic anomalies in the majority report's response text (primary-source). See `README.md` §"What the audit finds" and `findings/methods_paper_draft.md` §7.1 Stage 9 for the canonical anchoring numbers (majority 80.0% / minority 72.0%, both within the 70–85% Canadian comparator norm).
