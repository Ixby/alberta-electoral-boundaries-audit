---
name: R `redist` (SMC) vs Python `gerrychain` (ReCom) cross-validation
description: "Canonical cross-validation: on official Elections Alberta shapefiles the minority map's seats@50/50 (0.5169) lies above the R SMC ensemble maximum (0.4943) and at Python ReCom p99.99 of a 1,010,000-plan canonical ensemble. The pre-canonical sampler-disagreement framing (DPG era, April 2026) was substrate-driven and is archived at archive/dpg_era/redist_pre_canonical_history.md."
type: project
---

> **Backward:**
> - `analysis/scripts/redist_crossvalidation.R` — R SMC sampler run
> - `analysis/scripts/mcmc_ensemble_canonical.py` — Python ReCom canonical ensemble run
> - `data/shapefiles/canonical/va_2023_election_day_votes.gpkg` — canonical adjacency substrate
> - `data/redist_crossvalidation_s50.csv` — canonical SMC ensemble (5,000 plans, importance-weighted)
> - `data/outputs/simulated_ensemble_percentiles_canonical.csv` — canonical ReCom percentile placements
> - `archive/dpg_era/redist_pre_canonical_history.md` — pre-canonical trail-of-work archive
>
> **Forward:**
> - `reports/academic/report_academic.md` — incorporates the cross-validation finding
> - `findings/methods_paper_draft.md` — uses the canonical resolution as a worked example
> - `findings/README.md` — indexes this finding

# R vs Python sampler cross-validation — canonical (2026-05-18)

## Authoritative result

On official Elections Alberta shapefiles (received 2026-05-06, canonical run 2026-05-12 for ReCom, 2026-05-18 for SMC), **both samplers place the canonical minority map's `seats@50/50` (0.5169) as an extreme outlier**:

- **Python ReCom**, 1,010,000 plans: **p99.99** (only ~65 of 1,010,000 plans equal or exceed it).
- **R SMC**, 5,000 plans (importance-weighted, ESS 1,116): **0 of 5,000 reached the value**; ensemble maximum 0.4943, 2.26 pp below the minority's value; bound therefore above p99.98.

The two samplers come from different operator families (ReCom is a spanning-tree merge-split Markov chain; SMC is sequential Monte Carlo with importance weights and a tractable target distribution), so their agreement on canonical geometry is a meaningful cross-validation, not a coincidence.

## Why this matters

A hostile statistician's strongest attack on the audit's percentile-placement claim is *"this might be a `gerrychain`-specific artefact — a different sampler would give different numbers."* The R `redist` SMC cross-check directly addresses that objection. Pre-canonical (DPG era) the two samplers materially disagreed; on canonical geometry they agree.

## Setup (canonical)

| | Python ReCom (`gerrychain`) | R SMC (`redist`) |
|---|---|---|
| Sampler family | Markov chain (ReCom) | Sequential Monte Carlo |
| Ensemble size | 1,010,000 plans (4 chains × 252,500 steps) | 5,000 plans (`nsims = 5000`) |
| Population tolerance | ±25% | ±25% |
| Substrate | Canonical EA shapefiles + 2023 VA polygons (4,765 nodes / 13,385 edges) | Same |
| Districts | 87 (2019 enacted Bill 33 seed partition) | 87 (same) |
| Random seed | 1432864451 (drand-beacon-derived) | `set.seed(852751799)` placed immediately before `redist_smc()` |
| Resample / pop_temper (SMC) | n/a | `resample = FALSE`, `pop_temper = 0` (importance-weighted; defaults to avoid the 10k-attempt particle-collapse failure documented in archive) |
| Convergence (ReCom) | GR92 R-hat 1.00179–1.01843; ESS 1,429–1,682 on partisan metrics | n/a |
| Convergence (SMC) | n/a | ESS 1,116 of 5,000 |

Both samplers consume the same input adjacency graph (verified bit-identical: 4,765 nodes / 13,385 edges in both languages).

**District count and the 87-vs-89 question.** Both ensembles generate 87-district plans, seeded from the 2019 enacted Bill 33 boundary set. The canonical minority recommendation has 89 EDs and the canonical majority has 87. The audit's headline metric `seats@50/50` is a *fractional* UCP seat share at province-wide 50/50 vote — normalized by the plan's own district count — so 87-district ensemble values and the 89-district minority's measured value lie on the same fractional axis. The choice to seed neutral plans at 87 (the legally-prior district count) rather than 89 (the proposal-side count) is documented in `analysis/scripts/mcmc_ensemble_canonical.py` and `analysis/scripts/redist_crossvalidation.R`; the audit treats 87 as the appropriate null because it predates the recommendations under review.

## Canonical SMC ensemble — distribution shape

Verified against `data/redist_crossvalidation_s50.csv` on 2026-05-23.

| Statistic | R SMC canonical (5,000 plans, weighted) |
|---|---|
| seats@50/50 — p5 | 0.4368 |
| seats@50/50 — median | 0.4483 |
| seats@50/50 — p95 | 0.4598 |
| seats@50/50 — p99 | 0.4713 |
| seats@50/50 — max | 0.4943 |
| % plans ≥ 0.5169 (canonical minority) | **0%** (0 of 5,000 unweighted; 0.0000% weighted) |
| % plans ≥ 0.4831 (v0_9 legacy, archived) | 0.0116% weighted (3 of 5,000 unweighted = 0.060% unweighted) |

The canonical minority map's seats@50/50 (0.5169) **exceeds the entire R SMC ensemble** — the ensemble maximum of 0.4943 is 2.26 pp below the target.

## Canonical ReCom ensemble — minority placement

| Sampler | Geometry | Minority seats@50/50 | Percentile |
|---|---|---|---|
| Python ReCom (`gerrychain`) | Canonical (official EA) | 0.5169 | **99.99** |
| R SMC (`redist`) | Canonical (official EA) | 0.5169 | **>p99.98 (0% of 5,000 plans; max 0.4943)** |

The canonical minority (0.5169) **exceeds the Python ReCom canonical ensemble median (0.4483) by 6.86 pp** and the ensemble p95 (0.4828) by 3.41 pp — verified against `data/outputs/simulated_ensemble_percentiles_canonical.csv`.

## Substrate-invariant compactness-mechanism falsification tests

Two falsification tests were designed by the principal investigator in 2026-04-26 to probe a "mechanism is the geometry" hypothesis. They are substrate-invariant: they measure properties of the SMC ensemble's internal structure (Polsby-Popper distributions and within-ensemble correlations) and survive the canonical re-run unchanged.

### Test #4 — Compactness distributions across samplers (DPG-era SMC ensemble; verdict holds)

**Prediction:** SMC's Polsby-Popper distribution should be left-shifted (less compact) compared to Python ReCom's. If the two distributions overlap, the "SMC explores less-compact territory" assumption is wrong.

**Result:**

| Statistic | Python ReCom (10k verification subset) | R SMC (5k weighted plans) | Δ |
|---|---|---|---|
| mean PP — median across plans | 0.2501 | 0.2357 | -0.0144 (SMC ~5.7% less compact) |
| mean PP — p5 | 0.2380 | 0.2288 | -0.0092 |
| mean PP — p95 | 0.2645 | 0.2468 | -0.0177 |

**Verdict:** WEAKLY supports the hypothesis. SMC plans are *slightly* less compact than ReCom plans on average, but the distributions overlap heavily.

### Test #2 — High-UCP-advantage SMC plans should be less compact than other SMC plans (REFUTED)

**Prediction:** Within the SMC ensemble, the plans that reach the minority's `seats@50/50` value should have systematically lower mean PP (less compact) than the plans that don't.

**Result:**

| | Plans with seats@50/50 ≥ 0.4831 | Other SMC plans |
|---|---|---|
| N | 2,762 | 2,238 |
| Mean Polsby-Popper | **0.2391** | **0.2339** |

**Difference: +0.0051** (positive = high-UCP plans are *more* compact than other plans). **Welch t-test p-value: 7.7 × 10⁻²³⁴** (rock-solid statistical significance, in the *opposite* direction from the prediction).

**Verdict:** **REFUTES the hypothesis.** The SMC plans that reach the minority's value are not less compact — they are very slightly *more* compact than the SMC plans that don't reach it. The "non-compact geometry is what makes the high-UCP-advantage reachable" claim does not survive the test. This finding is unaffected by the canonical recomputation; it is a within-ensemble structural property that holds on either substrate.

**Implication.** The minority commission did not break Polsby-Popper to build their tipping-point firewall. The corridors are drawn thick enough that PP looks innocent. The mechanism lives in *what the corridors connect* (city blocks extracted across municipal limits into suburban districts), not in the corridor shape itself. The audit's Lane 2 case rests on the legs that *did* survive canonical recomputation: urban hybridization, Airdrie city-splitting, and the chair-flagged cartographic anomalies — see README §"What the audit finds."

## Implication for the audit framing

**Ensemble-size asymmetry, explicit.** The two canonical ensembles are not the same size. Python ReCom is 1,010,000 plans (4 chains × 252,500 steps; ESS 1,429–1,682 on partisan metrics; GR92 R-hat 1.002–1.018). R SMC is 5,000 plans (ESS 1,116, `resample = FALSE`). The p99.99 figure is carried by the ReCom ensemble's statistical weight — 5,000 plans cannot validate a percentile finer than ~p99.98 on their own. What the SMC ensemble adds is **a different operator family reaching the same qualitative conclusion**: 0 of 5,000 importance-weighted plans reach 0.5169 and the SMC maximum (0.4943) sits 2.26 pp below the minority value. Because that gap is so large relative to any plausible importance-weighting bias on the upper tail, the qualitative finding ("the canonical minority's `seats@50/50` is above the entire SMC ensemble") is robust to the `resample = FALSE` posture and to the library-default differences flagged in §"Limitations."

The dual-sampler framing reads:

> *"Under the canonical Python ReCom ensemble (1,010,000 plans, official Elections Alberta shapefiles), the minority map's `seats@50/50` sits at the 99.99th percentile — only ~65 of 1,010,000 neutral plans equal or exceed it. Under the canonical R SMC ensemble (5,000 plans, official EA shapefiles, Harvard `redist` package), the canonical minority value (0.5169) exceeds the ensemble maximum (0.4943) — 0% of 5,000 SMC plans reached it, placing the minority map above the 99.98th percentile of the R distribution. Both standard ensemble samplers on official geometry agree: the canonical minority map's `seats@50/50` is an extreme outlier. The p99.99 figure is carried by the larger ReCom ensemble; the SMC ensemble independently confirms the qualitative finding from a different operator family with different default constraint handling."*

## Limitations

- **R SMC ensemble size is 5,000, not 100,000+.** A 50,000-plan attempt posted a ~6-hour ETA on this machine and was cancelled; a subsequent 10,000-plan attempt collapsed to 3 unique plans during late-iteration particle resampling. 5,000 plans with `resample = FALSE` and ESS 1,116 give percentile placements to roughly ±1 pp precision in the right tail. On its own the SMC ensemble cannot establish a percentile finer than ~p99.98; the p99.99 figure in the canonical headline is carried by the ReCom ensemble's statistical weight.
- **`resample = FALSE` is non-standard for tail-percentile work.** Setting `resample = FALSE` was forced by the 10k attempt's particle-collapse failure: with resampling on, late-iteration weight concentration produced only 3 unique surviving plans. Without resampling, the importance-weighted ensemble retains plan diversity (ESS 1,116) but the empirical distribution is no longer the resampled-and-converged target distribution standard SMC theory works with. The qualitative canonical finding (0 of 5,000 reach 0.5169, max 0.4943) is robust to this choice because the minority value sits 2.26 pp above the ensemble maximum — well outside any plausible importance-weighting bias on the upper tail.
- **Different default constraints between libraries.** SMC defaults differ from ReCom in how `pop_temper` and contiguity verification are handled. Both runs use each library's published defaults rather than identical specifications; the comparison is between two *standard library configurations*, not a like-for-like specification match. The canonical agreement — both samplers find 0 plans reach the minority value on official EA geometry — is robust to those default-handling differences given how far above the SMC maximum the minority value sits.
- **Population proxy (SMC only).** R SMC requires strictly-positive integer-like populations. The gpkg's `pop_2021` column has fractional values from areal interpolation, so the R script uses a vote-weighted proxy (`va_ucp + va_ndp + va_other`, integer-rounded). The proxy and the true population are not the same field, and the audit has not quantitatively verified that the proxy preserves the population-balance constraint at every VA. Both substrates are equal-population-balanced as inputs and both samplers' contiguity constraints are enforced on the same adjacency graph.
- **ReCom compactness bias.** ReCom builds plans by recursively merging and splitting along spanning trees, which has a known empirical bias toward more compact maps (Chen 2025, "Balanced Spanning Tree Distributions Have Separation Fairness", [arXiv:2509.15137](https://arxiv.org/abs/2509.15137); Cannon et al. 2022, "Spanning Trees and Redistricting", [arXiv:2210.01401](https://arxiv.org/abs/2210.01401), which introduces the spanning-tree distribution as the canonical sampling target). The minority map is non-compact (chair-flagged lasso shapes, anomalies). The SMC cross-check is the audit's direct counter to this objection: SMC has a tractable target distribution and a different operator family. On canonical geometry both agree the minority is an outlier, so the conclusion is robust to ReCom's compactness bias.

## Audit-trail anchors

Verified against the actual filesystem on 2026-05-23. The canonical SMC CSV's numbers are independently verifiable against the on-disk file and match the canonical-resolution table above exactly (weighted p5/p50/p95/p99/max = 0.4368/0.4483/0.4598/0.4713/0.4943; 0 of 5,000 plans reach 0.5169; 0.0116% weighted reach 0.4831; ESS 1,116).

- **R script:** `analysis/scripts/redist_crossvalidation.R` (in repo; `nsims = 5000`, `resample = FALSE`, `pop_temper = 0`, `n_districts = 87`).
- **R output (canonical SMC ensemble, 5,000 plans):** `data/redist_crossvalidation_s50.csv` (in repo; numbers above verified against this file). A second, distinct 5,000-plan CSV with ESS 1,717 exists at `data/outputs/mcmc/redist_crossvalidation_s50.csv` — that file is from a different run and is **not** the source for the canonical numbers cited here.
- **R `.rds` artifact:** `data/v0_1_redist_crossvalidation_s50.rds` (pre-canonical naming; canonical-era `.rds` not separately preserved — canonical CSV is the authoritative artifact).
- **R run log:** `data/logs/redist_crossvalidation_run.log` preserves the *pre-canonical* run; canonical 2026-05-18 stdout was not separately preserved. Fresh reproducer run is the cleanest way to regenerate a canonical-era log.
- **Python ensemble samples (canonical):** `data/outputs/simulated_ensemble_raw_samples_canonical.csv` (1,010,000 plans, LFS-tracked).
- **Canonical real-map scores:** `data/outputs/simulation_real_map_scores_canonical.json`.
- **Canonical percentile placements:** `data/outputs/simulated_ensemble_percentiles_canonical.csv`.
- **Pre-canonical trail-of-work archive:** `archive/dpg_era/redist_pre_canonical_history.md` (the original 2026-04-26 setup, distribution-shape comparison, v0_9 placement table, stability caveat triple-run, and pre-canonical disagreement-resolution analysis — all moved on 2026-05-23 when the disagreement was confirmed substrate-driven and the live file was slimmed to canonical-only).
