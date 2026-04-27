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

> **TODO — fill once R run completes (currently in progress; see `analysis/reports/redist_crossvalidation_run.log`).**

### Distribution shape

| Statistic | Python ReCom (100k) | R SMC (10k) | Δ | Within ±0.5pp tolerance? |
|---|---|---|---|---|
| seats@50/50 — median | 0.4483 | TBD | TBD | TBD |
| seats@50/50 — p5 | 0.4253 | TBD | TBD | TBD |
| seats@50/50 — p95 | 0.4828 | TBD | TBD | TBD |
| seats@50/50 — p99 | 0.4943 | TBD | TBD | TBD |
| seats@50/50 — max | 0.5057 | TBD | TBD | TBD |

### v0_9 minority map placement

| | Python ReCom | R SMC |
|---|---|---|
| Real-map seats@50/50 (v0_9 minority) | 0.4831 | 0.4831 (same input) |
| Percentile in ensemble | 98.57 (1,426 of 100,000) | TBD |
| Pass criterion (±0.5pp) | — | TBD |

## Verdict

> **TODO — fill after percentile is computed.**

If R SMC produces a percentile placement within ±0.5pp of the Python ReCom 98.57:
- The audit's headline `seats@50/50` outlier framing is **algorithm-independent**
- Hostile reviewers cannot dismiss the finding as a `gerrychain`-library artefact
- The v0_9 substrate's measurement is reproducible across two different research stacks

If R SMC produces a materially different percentile (>2pp away):
- The discrepancy is investigated before any headline framing is finalized
- The audit publishes both numbers and reports the disagreement honestly
- Possible causes: SMC's pop_temper parameter, different default constraint handling, or — least likely but most important — a real bug in one of the two pipelines

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
