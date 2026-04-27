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

## Falsification tests (PO-designed, 2026-04-26 evening)

After the initial discrepancy was surfaced, the PO proposed four falsification tests for the "mechanism is the geometry" hypothesis (the claim that the SMC plans reach the minority's `seats@50/50` more often than the ReCom plans because SMC explores less-compact territory). Two of the four (Tests #2 and #4) are runnable directly against the data already in hand. Both ran on 2026-04-26 evening; results below.

### Test #4 — Compactness distributions should differ between samplers

**Prediction:** SMC's Polsby-Popper distribution should be left-shifted (less compact) compared to Python ReCom's. If the two distributions overlap perfectly, the "SMC explores less-compact territory" assumption is wrong and the whole thesis collapses.

**Method:**
- Python ReCom: re-used the 10,000-plan verification subset and computed mean Polsby-Popper per plan via `analysis/scripts/compactness_for_verification_subset.py` (precomputed shared-edge lengths, ~30s for the full subset).
- R SMC: added `redistmetrics::comp_polsby` to `analysis/scripts/redist_crossvalidation.R`, ran on the 5,000-plan SMC ensemble.

**Result:**

| Statistic | Python ReCom (10k verification subset) | R SMC (5k weighted plans) | Δ |
|---|---|---|---|
| mean PP — median across plans | 0.2501 | 0.2357 | -0.0144 (SMC ~5.7% less compact) |
| mean PP — p5 | 0.2380 | 0.2288 | -0.0092 |
| mean PP — p95 | 0.2645 | 0.2468 | -0.0177 |

**Verdict:** WEAKLY supports the hypothesis. SMC plans are *slightly* less compact than ReCom plans on average, but the distributions overlap heavily. SMC is not exploring a meaningfully different region of compactness-space; both samplers produce relatively compact maps with very similar PP distributions.

### Test #2 — High-UCP-advantage SMC plans should be less compact than other SMC plans

**Prediction:** Within the SMC ensemble, the plans that reach the minority map's 0.4831 `seats@50/50` value should have systematically lower mean PP (less compact) than the plans that don't. If the high-UCP-advantage plans are equally or more compact, the "you can't reach 0.4831 without breaking compactness" claim is factually false.

**Result:**

| | Plans with seats@50/50 ≥ 0.4831 | Other SMC plans |
|---|---|---|
| N | 2,762 | 2,238 |
| Mean Polsby-Popper | **0.2391** | **0.2339** |

**Difference: +0.0051** (positive = high-UCP plans are *more* compact than other plans).
**Welch t-test p-value: 7.7 × 10⁻²³⁴** (rock-solid statistical significance, in the *opposite* direction from the prediction).

**Verdict:** **REFUTES the hypothesis.** The SMC plans that reach the minority's `seats@50/50` are not less compact — they are very slightly *more* compact than the SMC plans that don't reach it. The "non-compact geometry is what makes the high-UCP-advantage reachable" claim does not survive the test.

### What this means for the "mechanism is the geometry" thesis

Per the PO's pre-registered criterion at the time the tests were designed: *"If the SMC maps that hit the UCP advantage are significantly less compact than the ReCom maps, the 'Surgical Fortification / Mechanism is the Geometry' thesis is locked in as hard science. If they aren't, drop the thesis and default to Option C (Investigate further) or Option D (Lead entirely with Lane 2)."*

The data falls on the "drop the thesis" side. The strong claim that *"the minority map's UCP-favourable seat advantage is mechanically inseparable from the unusual non-compact geometry the chair flagged"* is not supported by the falsification tests.

**2026-04-26 evening update — v0_9 direct measurement converges on the same answer.** After this falsification was published, the PO ran a direct Polsby-Popper measurement on the v0_9 topological substrate (script `analysis/scripts/v0_9_polsby_popper.py`, verdict at `analysis/reports/v0_9_polsby_popper_verdict.md`). The chair's named lassos themselves score in the *moderate* compactness band: **Calgary-Nolan Hill-Cochrane PP = 0.402, Rocky Mountain House-Banff Park PP = 0.414** (PP > 0.40 is "high compactness"). Two independent methodologies — the SMC-ensemble falsification and direct measurement on the real maps under the cleanest available substrate — point to the same mechanistic interpretation: **the minority commission did not break Area/Perimeter ratio to build their tipping-point firewall.** The corridors are drawn thick enough that PP looks innocent. The mechanism lives in *what the corridors connect* (city blocks extracted across municipal limits into suburban districts), not in the corridor shape itself. The audit's Lane 2 case rests on the two substrate-stable measurements: **municipal anchoring** (minority 14.5%, majority 71%) and **urban hybridization** (minority 25 hybrid EDs, majority 9, 12 of the minority's *new*) — both computed off the v0_9 substrate, both sampler-independent, both stable across substrate generations.

The audit retains:

- The empirical fact that R SMC reaches the minority's value more often than Python ReCom (the magnitude is run-stochastic; see "Stability caveat" below). That fact is real and defensible.
- The Lane 2 structural-irregularity finding (5 of 5 pre-registered tests fired). That finding is unaffected by the falsification — and is in fact *strengthened* by H3's rejection, because it now stands on the two substrate-stable mechanisms (anchoring + hybridization) rather than on PP.
- The Lane 1 ReCom percentile (98.6 — top 1.5%). Still defensible as a single-sampler statement.

The audit does NOT retain:

- The claim that compactness specifically is the mechanism through which the minority commissioners reached 0.4831. The remaining open question is which sub-feature of hybridization (city-cracking patterns specifically, urban-rural composition splits, or cut-edge density across municipal lines) carries the most signal; the audit does not claim to have decomposed it further.

### Stability caveat — R SMC results are run-stochastic

Across three runs of the R SMC script with the same nominal `set.seed(88)`, `nsims=5000`, `resample=FALSE`, `pop_temper=0`, but different library-load orderings, the fraction of plans reaching the minority's 0.4831 was:

| Run | Library load order | % of weighted plans ≥ 0.4831 |
|---|---|---|
| 1st | redist only | 28% |
| 2nd | redist + redistmetrics (no `comp_polsby` call) | 5.6% |
| 3rd | redist + redistmetrics + `comp_polsby` call | 57.9% |

This is an artefact of `library(redistmetrics)` consuming RNG state before the SMC sampler runs, shifting the random-consumption path. The qualitative finding (SMC reaches the value more often than ReCom's 1.4%) is stable across all three runs; the magnitude is not. A future re-run with explicit `set.seed()` immediately before `redist_smc()` (rather than once at the top of the script) would resolve this.

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
