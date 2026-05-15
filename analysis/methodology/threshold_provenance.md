---
name: Threshold provenance — every numeric threshold traced to its source
description: Per-threshold documentation of the source, justification, and audit application for every decision threshold used in the audit battery. Prevents arbitrary-threshold criticism.
type: methodology
---

# Threshold provenance

Every numeric threshold used to make a pass/fail or flag/no-flag decision in this audit is listed here, with the literature or statutory source that justifies it. The column "Alberta application" describes how the audit uses the threshold, including any adaptation from the original source.

---

## Statistical thresholds

| Threshold | Value | Source | Alberta application |
|---|---|---|---|
| Ensemble outlier flag | p95 (one-tailed) | MGGG GerryChain practice (DeFord, Duchin, Solomon 2021); adopted from lawsuit-grade redistricting litigation standard | Metrics above p95 against the 1M neutral ensemble receive an outlier flag; metrics below are within null. EG flag: minority at p94.4 — **flag retracted** (below p95). Mean-median at p99.98, Seats@50/50 at p99.99 — **flags active**. |
| ESS for publication-grade tail claims | ≥ 1,000 effective samples | MGGG standard; referenced in `test_selection_rationale.md` ("MGGG lawsuit grade") | The 1M canonical run achieves n_eff = 1,495 (Seats@50/50). ESS was the reason the Seats@50/50 flag was temporarily retracted at 250k and reinstated at 1M. |
| Gelman-Rubin R̂ convergence | < 1.05 (publication grade) < 1.02 (preferred) | Gelman & Rubin (1992); refined in Brooks & Gelman (1998) | Canonical 1M run: R̂ ∈ [1.007, 1.017] across all four metrics — within the publication-grade threshold. See §5.4.9 and `data/outputs/simulation_convergence_diagnostics_canonical.json`. |
| Mahalanobis D² significance | p < 0.05 (empirical, against ensemble distribution) | Standard (chi-squared approximation for high-dim feature spaces; Mahalanobis 1936) | D² computed against 1M-plan covariance matrix. Minority p = 1.40×10⁻⁶; majority p = 0.097. Both against the 4-dimensional (EG, MM, Declination, Seats@50/50) feature space. |
| SZAT one-tailed p | p < 0.05 | Standard bootstrap significance threshold; no single literature source mandates this for redistricting but it is the conventional social-science threshold | Applied one-tailed (UCP-direction is the pre-specified alternative); p = 0.0024 (10,000 permutations). |
| Fisher combination significance | p < 0.05 | Fisher (1925) combining k=2 independent tests; T ∼ χ²(4) | T = 39.03, p = 6.87×10⁻⁸. Independence confirmed at ρ = −0.0014 (§G1). |
| Holm-Bonferroni FWER correction | α = 0.10, m = 5 primary structural tests | Holm (1979) step-down procedure; standard FWER control | §7 (line 2248 of academic report): seats@50/50 p = 0.0148 ≤ 0.10/5 = 0.020 (survives at position 2 of sorted p-values). Used as supplementary check; BH is the primary multiple-comparisons method for the November confirmatory protocol. |
| BH false-discovery rate correction | α = 0.05 family-wise (FDR), m = 11 tests | Benjamini & Hochberg (1995) | Primary method for November 2026 confirmatory protocol. 10/11 exploratory-run tests pass BH correction at α = 0.05; sole failure is minority EG (p = 0.056), already retracted on independent grounds. |
| Declination significance | Ensemble percentile < p5 or > p95 | Warrington (2018, 2019) defines the metric; threshold follows the p95 convention above | Minority Declination at p1.21 (NDP-favoured tail — unusual direction; see §5.2.4 for cross-metric reading). |
| Calgary zone asymmetry flag | ≥ 10 percentage points | Internally derived: a 10 pp zone-gap would represent a systematic allocation bias exceeding random within-quota variation. Not from a single external source. | Minority 12.2% vs majority 0.4% — gap = 11.8 pp. Tested under two geographic classification rules; both agree on direction. |

---

## Compactness thresholds

| Threshold | Value | Source | Alberta application |
|---|---|---|---|
| Reock "compact" cutoff | ≥ 0.30 | Reock (1961) original paper; widely used in US redistricting litigation; "conventional Reock < 0.30 threshold" per H10 in academic report §7 | Chair-flagged minority districts: Calgary-Nolan Hill-Cochrane Reock = 0.230 (flagged). Rocky Mountain House-Banff Park Reock = 0.414 (not flagged). |
| Polsby-Popper (no absolute cutoff used) | No universal cutoff applied in this audit | Polsby & Popper (1991); no single accepted threshold in the literature | Per-ED values reported comparatively rather than against a threshold. The H3 finding used plan-mean PP (majority vs minority are similar in mean); H10 used individual PP for the chair-flagged district (PP = 0.402, moderate). |

---

## Anchoring thresholds

| Threshold | Value | Source | Alberta application |
|---|---|---|---|
| Municipal (CSD) boundary anchoring Canadian norm | 70–85% | Established from comparator provinces (federal 2022 Alberta sub-commission, BC 2023, Saskatchewan 2022, Manitoba 2018, Alberta 2017). Computed in `analysis/methodology/canadian_base_rate_computed.md`. | Both 2026 maps within norm on canonical geometry: minority 72.0%, majority 80.0%. Municipal anchoring finding **retracted** per DPG sunset clause. |
| DA-boundary anchoring (secondary) | No Canadian norm established | Insufficient comparator data; the DA anchoring result is presented as a map-comparison finding (majority +7.7 pp, minority +6.6 pp from 2019 baseline) rather than against an absolute threshold. | See `findings/da_anchoring_analysis.md`. |

---

## Statutory thresholds

| Threshold | Value | Source | Alberta application |
|---|---|---|---|
| Population deviation band | ±25% from provincial quota | Alberta Electoral Boundaries Commission Act (EBCA) §15(1) | Audit applies this as the neutral-ensemble constraint in GerryChain ReCom (`analysis/scripts/mcmc_ensemble_canonical.py`). 2026 maps: all 89 EDs within ±25% per commission's published population tables. |
| Special-area population extension | ±50% from provincial quota | EBCA §15(2) — remote, sparsely populated, or special rural areas | The A3 audit (`electoral_forensics_population.py`) checks each commission-invoked §15(2) exception against the statutory criteria: population basis, geographic justification, and cumulative constraint compliance. |

---

## Efficiency gap threshold note

The Stephanopoulos & McGhee (2014, 2015) 7% EG threshold is **not used** in this audit as a pass/fail criterion. `test_selection_rationale.md` §2 explains: "The audit explicitly discards the American 7% threshold in favour of an endogenous, Alberta-specific calibration." The MCMC neutral ensemble provides the Alberta-specific reference distribution; the 7% figure is mentioned only for comparative context and is flagged as "academic-literature authority only; never judicially adopted" (§5.2.1). All 2026 map EG values are below 7% regardless of attribution method.

---

## Source

Academic report §4.3 (test battery), §4.3.2 (Bonferroni), §7 (Holm-Bonferroni reference, H1-H10); `analysis/methodology/test_selection_rationale.md`; literature citations as noted per row.
