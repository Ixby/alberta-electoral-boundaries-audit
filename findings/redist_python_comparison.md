---
name: R `redist` (SMC) vs Python `gerrychain` (ReCom) cross-validation
description: Side-by-side comparison of percentile placements for the 2026 majority and minority maps' seats@50/50 across two fundamentally different ensemble samplers — Python's ReCom Markov chain (1,010,000 plans, canonical, via `gerrychain`) and R's Sequential Monte Carlo (5,000 plans, canonical, via Harvard's `redist`). On canonical Elections Alberta shapefiles the two samplers agree: the minority map's seats@50/50 (0.5169) lies above the SMC ensemble maximum (0.4943) and at ReCom p99.99.
type: project
---

> **Status banner — read this first.**
> This document was opened in 2026-04-26 against pre-canonical (Derived Provisional Geometry, "DPG") inputs. It carries the pre-canonical comparison through to line ≈ 141 and then the 2026-05-18 canonical re-run from §"2026-05-18 canonical update" onward.
>
> **Authoritative result (canonical, official EA shapefiles, 2026-05-18):** both samplers place the canonical minority map's `seats@50/50` (0.5169) as an extreme outlier. Python ReCom (1,010,000 plans): p99.99. R SMC (5,000 plans, importance-weighted, ESS 1,116): 0 of 5,000 reached the value; ensemble maximum 0.4943, 2.26 pp below the minority's value; bound is therefore above p99.98 on the SMC side.
>
> **What the pre-canonical sections show but no longer support:** the DPG-era v0_9 minority value (0.4831) and the apparent ReCom-vs-SMC disagreement (98.6 vs ~28%) were driven by the now-superseded DPG substrate, not by a sampler discrepancy. The DPG-era municipal-anchoring numbers cited inline (minority 14.5%, majority 71%) were retracted on canonical recomputation (canonical anchoring: majority 80.0%, minority 72.0%, both within the 70–85% Canadian comparator norm; see README and `findings/methods_paper_draft.md`). Pre-canonical inline numbers below are kept for trail-of-work transparency, not as live claims.

> **Backward:**
> - `analysis/scripts/redist_crossvalidation.R` — R SMC sampler run
> - `analysis/scripts/mcmc_ensemble_canonical.py` — Python ReCom canonical ensemble run
> - canonical 2023 VA adjacency graph (4,765 nodes / 13,385 edges)
>
> **Forward:**
> - `reports/academic/report_academic.md` — incorporates the cross-validation finding
> - `findings/README.md` — indexes this finding

# R vs Python cross-validation — 2026-04-26 / 27 (pre-canonical), 2026-05-18 (canonical re-run)

## Why this matters

Gemini's design-review #3: a hostile statistician's strongest attack on the audit's percentile-placement claim is *"this might be a `gerrychain`-specific artefact — a different sampler would give different numbers."* The Harvard `redist` package implements Sequential Monte Carlo (SMC), a fundamentally different sampler from ReCom. If both produce essentially the same percentile placement for the v0_9 minority map's `seats@50/50` value (0.4831), the headline finding is algorithm-independent and library-independent.

## Setup

*Pre-canonical (DPG-era) setup, kept for trail-of-work transparency. See §"2026-05-18 canonical update" for the authoritative re-run.*

| | Python ReCom (`gerrychain`) | R SMC (`redist`) |
|---|---|---|
| Sampler family | Markov chain (ReCom) | Sequential Monte Carlo |
| Ensemble size | 100,000 maps (4 chains × 25,000 steps) | 5,000 maps (`nsims = 5000` in `redist_crossvalidation.R`; a 50k attempt posted a ~6h ETA and was cancelled, a 10k attempt collapsed to 3 unique plans during late-iteration particle resampling) |
| Population tolerance | ±25% | ±25% |
| Substrate | 2023 VA polygons (4,765 nodes / 13,385 edges) | Same |
| Districts | 87 (the 2019 enacted Bill 33 substrate count, used as the seed partition) | 87 (same) |
| Random seed | 42 | 88 (pre-canonical; canonical re-run uses `set.seed(852751799)` immediately before `redist_smc()` — see §"2026-05-18 canonical update") |
| Wall time (this machine) | ~30 minutes | ~25–50 minutes (5k SMC plans; precise wall time not preserved in the surviving run logs) |

Both samplers consume the same input adjacency graph (verified bit-identical: 4,765 nodes / 13,385 edges in both languages).

**District count and the 87 vs 89 question.** Both ensembles generate 87-district plans, seeded from the 2019 enacted Bill 33 boundary set. The canonical minority recommendation has 89 EDs and the canonical majority has 87. The audit's headline metric `seats@50/50` is a *fractional* UCP seat share at province-wide 50/50 vote — normalized by the plan's own district count — so 87-district ensemble values and the 89-district minority's measured value lie on the same fractional axis. The choice to seed neutral plans at 87 (the legally-prior district count) rather than 89 (the proposal-side count) is documented in `analysis/scripts/mcmc_ensemble_canonical.py` and `analysis/scripts/redist_crossvalidation.R`; the audit treats 87 as the appropriate null because it predates the recommendations under review.

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

**2026-04-26 evening update — v0_9 direct measurement converges on the same answer.** After this falsification was published, the PO ran a direct Polsby-Popper measurement on the v0_9 topological substrate (script `analysis/scripts/polsby_popper.py`, verdict at `findings/polsby_popper_verdict.md`). The chair's named lassos themselves score in the *moderate* compactness band: **Calgary-Nolan Hill-Cochrane PP = 0.402, Rocky Mountain House-Banff Park PP = 0.414** (PP > 0.40 is "high compactness"). Two independent methodologies — the SMC-ensemble falsification and direct measurement on the real maps under the cleanest available substrate — point to the same mechanistic interpretation: **the minority commission did not break Area/Perimeter ratio to build their tipping-point firewall.** The corridors are drawn thick enough that PP looks innocent. The mechanism lives in *what the corridors connect* (city blocks extracted across municipal limits into suburban districts), not in the corridor shape itself.

At the time this paragraph was written (2026-04-26), the audit's Lane 2 case was described as resting on two DPG-era substrate-stable measurements: municipal anchoring (then reported as minority 14.5%, majority 71%) and urban hybridization (minority 25 hybrid EDs, majority 9, 12 of the minority's *new*). **The municipal-anchoring half of that claim did not survive canonical recomputation.** On official Elections Alberta shapefiles (received 2026-05-06), majority anchoring = 80.0%, minority = 72.0%; both maps fall inside the 70–85% Canadian comparator norm, and the 4.9× DPG-era gap is retracted (README §"What the audit finds"; methods-paper §7.1, Stage 9). The current Lane 2 case rests on the **sampler-independent and substrate-stable** legs: urban hybridization (unaffected by the geometry upgrade), Airdrie city-splitting (4 vs 2 EDs, a direct count under either substrate), and the chair-flagged cartographic anomalies in the majority report's response text (primary-source evidence, geometry-independent).

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

1. **Sampler bias toward compactness**. ReCom builds plans by recursively merging and splitting along spanning trees, which has a known empirical bias toward more compact maps (Chen 2025, "Balanced Spanning Tree Distributions Have Separation Fairness", [arXiv:2509.15137](https://arxiv.org/abs/2509.15137); see also Cannon, Goldbloom-Helzner et al. 2022, "Spanning Trees and Redistricting", [arXiv:2210.01401](https://arxiv.org/abs/2210.01401), which introduces the spanning-tree distribution as the canonical sampling target). The minority map is non-compact (chair-flagged lasso shapes, anomalies). A sampler that less-strongly penalises non-compactness will explore higher-`seats@50/50` regions of the legal-map space more readily.
2. **Different default constraints between libraries**. The R SMC run uses redist's published defaults; the Python ReCom run uses gerrychain's. The two libraries' constraint handling (how strictly they enforce contiguity, how they handle near-population-tolerance moves) differs in ways that can shift the sampled distribution.
3. **SMC importance-weight handling without resampling**. The R run used `resample = FALSE` to avoid the particle-filter collapse from the prior 10k attempt; the importance-weighted percentiles are sound (ESS = 2,199 of 5,000, no pathological concentration), but the un-resampled population's empirical distribution may differ from the resampled-and-converged target.

## What this means for the audit's headline framing

The Python ReCom finding (top 1.5%) and the R SMC finding (near-median) are *both true* — they are statements about how the minority map looks under two different (but both standard) ways of sampling the legal-map space. The honest public-report framing is therefore:

> *"Under one standard ensemble sampler (gerrychain ReCom), the minority map's `seats@50/50` value sits at the 98.6th percentile of 100,000 simulated maps — a top-1.5% outlier. Under a different standard sampler (R `redist` SMC), it sits near the median. Both samplers are widely used in the academic redistricting literature; they disagree because they sample the legal-map space with different (well-documented) biases. The audit reports both numbers; the surgical-fortification narrative is supported by ReCom but does not survive the SMC cross-check."*

This is a more cautious headline than the public report currently carries. The choice is the PO's: revise the public report to reflect the dual-sampler disagreement, or treat the R SMC result as the methodology-honesty caveat it is and keep the surgical-fortification framing with a footnote pointing here.

## Limitations of this comparison

- **R SMC ensemble size is 5,000, not 100,000+.** The R script runs `nsims = 5000`. A 50,000-plan attempt posted a ~6-hour ETA on this machine and was cancelled; a subsequent 10,000-plan attempt collapsed to 3 unique plans during late-iteration particle resampling. 5,000 plans with `resample = FALSE` and ESS 1,116–2,199 give percentile placements to roughly ±1 pp precision in the right tail — coarser than the Python ReCom ensemble (1,010,000 plans on canonical geometry). On its own the SMC ensemble cannot establish a percentile finer than ~p99.98; the p99.99 figure in the canonical headline is carried by the ReCom ensemble's statistical weight, with the SMC ensemble providing an independent "0 of 5,000 reached the value" sanity floor 2.26 pp above the SMC maximum.
- **`resample = FALSE` is non-standard for tail-percentile work.** Setting `resample = FALSE` was forced by the 10k attempt's particle-collapse failure: with resampling on, late-iteration weight concentration produced only 3 unique surviving plans, which gives no useful tail estimate. Without resampling, the importance-weighted ensemble retains plan diversity (ESS 1,116) but the empirical distribution is no longer the resampled-and-converged target distribution standard SMC theory works with. The qualitative canonical finding (0 of 5,000 reach 0.5169, max 0.4943) is robust to this choice because the minority value sits 2.26 pp above the ensemble maximum — well outside any plausible importance-weighting bias on the upper tail.
- **Different default constraints between libraries.** SMC defaults differ from ReCom in how `pop_temper` and contiguity verification are handled. Both runs use each library's published defaults rather than identical specifications; the comparison is therefore between two *standard library configurations*, not a like-for-like specification match. The canonical agreement — both samplers find 0 plans reach the minority value on official EA geometry — is robust to those default-handling differences in the sense that no plausible reconciliation of the two libraries' constraint enforcement would produce a different qualitative result given how far above the SMC maximum the minority value sits.
- **Population proxy.** R SMC requires strictly-positive integer-like populations. The gpkg's `pop_2021` column has fractional values from areal interpolation, so the R script uses a vote-weighted proxy (`va_ucp + va_ndp + va_other`, integer-rounded). The proxy and the true population are not the same field, and the audit has not quantitatively verified that the proxy preserves the population-balance constraint at every VA. Both substrates are equal-population-balanced as inputs and both samplers' contiguity constraints are enforced on the same adjacency graph, so the legal-map space being sampled is the same in topology even if population is encoded via a proxy column; a future replication that exposes a true integer population field to redist would close this gap.

## 2026-05-18 canonical update — resolution status

Official Elections Alberta canonical shapefiles were released and the full audit re-run completed. Three items close; one remains.

### What closed

**1. Seed placement fixed.** The stability caveat documented three runs of the R SMC script with `set.seed(88)` producing 28%, 5.6%, and 57.9% — caused by `library(redistmetrics)` consuming RNG state before the sampler ran. The current script (`v0.1`) places `set.seed(852751799)` immediately before `redist_smc()` with no intervening R operations that consume RNG state. The fix is in place.

**2. Python ReCom canonical percentile.** The 1,010,000-plan canonical ensemble (official EA shapefiles, 4 chains × 252,500 steps, seed 1432864451) places the minority map's `seats@50/50` at **p99.99** — only 0.006% of plans equal or exceed it.

| Sampler | Geometry | Minority seats@50/50 | Percentile |
|---|---|---|---|
| Python ReCom (`gerrychain`) | Canonical (official EA) | 0.5169 | **99.99** |
| R SMC (`redist`) | v0_9 DPG | (0.4831 — superseded) | ~28–58% (run-stochastic, superseded) |
| R SMC (`redist`) | Canonical (official EA) | 0.5169 | **>p99.98 (0% of 5,000 plans; max 0.4943)** |

The v0_9 DPG minority value (0.4831) is superseded. The canonical minority (0.5169) **exceeds the Python ReCom canonical ensemble median (0.4483) by 6.86 pp** and the ensemble p95 (0.4828) by 3.41 pp — verified against `data/outputs/simulated_ensemble_percentiles_canonical.csv`. Under canonical geometry, the Python ReCom finding (minority at p99.99 of a 1.01M-plan ensemble, ~65 plans of 1,010,000 reaching or exceeding it) is stronger than the v0_9 result, not weaker.

**3. Compactness mechanism REFUTED (finding stands).** Test #2 (high-UCP-advantage SMC plans are *more* compact than other SMC plans, Welch p = 7.7×10⁻²³⁴) is unaffected by the geometry upgrade. The conclusion — that the minority map's UCP advantage does not require non-compact geometry — is correct and holds.

### Resolution confirmed — 2026-05-18

**R SMC canonical re-run complete.** Run date: 2026-05-18. Input: `data/shapefiles/canonical/va_2023_election_day_votes.gpkg`. Seed: `set.seed(852751799)` placed immediately before `redist_smc()` with no intervening R operations that consume RNG state (the fix for the pre-canonical stability caveat). 5,000 plans (`nsims = 5000`), `resample = FALSE`, `pop_temper = 0`, importance-weighted, ESS 1,116. District count: 87 (the 2019 enacted Bill 33 seed partition, matching the Python ReCom canonical ensemble's seed). Population field: vote-totals proxy (`va_ucp + va_ndp + va_other`, integer-rounded) as documented in §"Limitations." Library defaults are `redist`'s published defaults (`pop_temper = 0`, `redist_smc()`-default contiguity verification); the cross-library reconciliation is qualitative — both samplers run in their respective standard configurations — rather than a like-for-like specification match.

| Statistic | R SMC canonical (2026-05-18) |
|---|---|
| Ensemble size | 5,000 plans (ESS 1,116) |
| seats@50/50 — p5 | 0.4368 |
| seats@50/50 — median | 0.4483 |
| seats@50/50 — p95 | 0.4598 |
| seats@50/50 — p99 | 0.4713 |
| seats@50/50 — max | 0.4943 |
| % plans ≥ 0.5169 (canonical minority) | **0%** (0 of 5,000 unweighted; 0.0000% weighted) |
| % plans ≥ 0.4831 (v0_9 legacy) | 0.0116% weighted (3 of 5,000 unweighted = 0.060% unweighted) |

The canonical minority map's seats@50/50 (0.5169) **exceeds the entire R SMC ensemble** — the ensemble maximum of 0.4943 is 2.26 pp below the target. The R SMC cross-validation confirms the Python ReCom finding: the canonical minority map is an extreme outlier under both samplers on canonical geometry.

The prior v0_9 disagreement (SMC near-median vs ReCom p98.6) was driven by the old DPG substrate's lower minority value (0.4831), not by a sampler discrepancy. On canonical geometry both samplers agree: 0% of neutral plans reach the canonical minority's seats@50/50.

### Implication for the audit framing

**Ensemble-size asymmetry, explicit.** The two canonical ensembles are not the same size. Python ReCom is 1,010,000 plans (4 chains × 252,500 steps; ESS 1,429–1,682 on partisan metrics; GR92 R-hat 1.002–1.018). R SMC is 5,000 plans (ESS 1,116, `resample = FALSE`). The p99.99 figure is carried by the ReCom ensemble's statistical weight — 5,000 plans cannot validate a percentile finer than ~p99.98 on their own. What the SMC ensemble adds is **a different operator family reaching the same qualitative conclusion**: 0 of 5,000 importance-weighted plans reach 0.5169 and the SMC maximum (0.4943) sits 2.26 pp below the minority value. Because that gap is so large relative to any plausible importance-weighting bias on the upper tail, the qualitative finding ("the canonical minority's `seats@50/50` is above the entire SMC ensemble") is robust to the `resample = FALSE` posture and to the library-default differences flagged in §"Limitations."

The dual-sampler framing now reads:

> *"Under the canonical Python ReCom ensemble (1,010,000 plans, official Elections Alberta shapefiles), the minority map's `seats@50/50` sits at the 99.99th percentile — only ~65 of 1,010,000 neutral plans equal or exceed it. Under the canonical R SMC ensemble (5,000 plans, official EA shapefiles, Harvard `redist` package), the canonical minority value (0.5169) exceeds the ensemble maximum (0.4943) — 0% of 5,000 SMC plans reached it, placing the minority map above the 99.98th percentile of the R distribution. Both standard ensemble samplers on official geometry agree: the canonical minority map's `seats@50/50` is an extreme outlier. The p99.99 figure is carried by the larger ReCom ensemble; the SMC ensemble independently confirms the qualitative finding from a different operator family with different default constraint handling."*

## Audit-trail anchors

Verified against the actual filesystem on 2026-05-23. Paths that the document previously cited but that do not exist are flagged below; the canonical SMC CSV's numbers are independently verifiable against the on-disk file and match the canonical-resolution table above exactly (weighted p5/p50/p95/p99/max = 0.4368/0.4483/0.4598/0.4713/0.4943; 0 of 5,000 plans reach 0.5169; 0.0116% weighted reach 0.4831; ESS 1,116).

- **R script:** `analysis/scripts/redist_crossvalidation.R` (in repo; `nsims = 5000`, `resample = FALSE`, `pop_temper = 0`, `n_districts = 87`).
- **R output (canonical SMC ensemble, 5,000 plans):** `data/redist_crossvalidation_s50.csv` (in repo; numbers above verified against this file). A second, distinct 5,000-plan CSV with ESS 1,717 exists at `data/outputs/mcmc/redist_crossvalidation_s50.csv` — that file is from a different run (likely the pre-canonical or an intermediate one) and is **not** the source for the canonical numbers cited in this document.
- **R `.rds` artifact:** `data/v0_1_redist_crossvalidation_s50.rds` (in repo; carries the `v0_1_` prefix, i.e. pre-canonical naming). A canonical-era `.rds` is not preserved at a separate path; the canonical CSV is the authoritative artifact.
- **R run log:** `data/logs/redist_crossvalidation_run.log` (in repo) preserves the *pre-canonical* run (DPG substrate `va_polygons_with_2023_votes.gpkg`, `set.seed(88)` era, 57.9% weighted plans ≥ 0.4831 — the 3rd-run stochastic outcome documented in §"Stability caveat"). The canonical 2026-05-18 re-run's stdout log was not separately preserved; the canonical CSV exists and verifies, but a fresh reproducer run is the cleanest way to regenerate a canonical-era log.
- **Python ensemble samples (canonical):** `data/outputs/simulated_ensemble_raw_samples_canonical.csv` (1,010,000 plans, LFS-tracked).
- **Canonical real-map scores:** `data/outputs/simulation_real_map_scores_canonical.json`.
- **Canonical percentile placements:** `data/outputs/simulated_ensemble_percentiles_canonical.csv`.
- **v0_9 real-map scores (superseded):** `data/outputs/final_real_map_scores.json`.
- **v0_9 percentile placements (superseded):** `data/outputs/final_percentile_placement.json`.
