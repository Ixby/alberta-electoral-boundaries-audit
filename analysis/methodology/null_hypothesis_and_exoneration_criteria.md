---
name: Null hypotheses and exoneration criteria — pre-committed test definitions
description: Per-test null hypotheses, pass/fail thresholds, pre-registration IDs, and exoneration criteria for every test in the audit battery. Distinguishes exploratory from pre-registered confirmatory tests.
type: methodology
---

# Null hypotheses and exoneration criteria

This document is the authoritative lookup for what each test in the audit battery was testing, what would constitute a pass or fail, and what pre-registration anchors the test definition. It covers both the current exploratory run (2026 commission maps) and the forthcoming confirmatory run (November 2026 Lunty-committee map).

**Exploratory vs. confirmatory distinction.** The primary Ch1/Ch2/Fisher tests are exploratory: seeds were committed to the public drand beacon before the official shapefile release, but the specific test names and combination method were not pre-registered on OSF before execution. Ch3 (neighbour drain), the Lunty-committee scorecard (qsgy8), and the intermap permutation test (yvc7g) are pre-registered confirmatory tests. See §1 Introduction for the full distinction and its inferential implications.

---

## Test battery: null hypotheses and thresholds

### A-family — Population equality (§5.1)

| Test | Null hypothesis | Pass/fail threshold | Pre-registration | Status |
|---|---|---|---|---|
| A1 — Population MAD | Minority MAD ≤ majority MAD (no systematic population-dispersion asymmetry) | Minority MAD > majority MAD constitutes a directional finding; magnitude ≥ 10% gap considered non-trivial | Not pre-registered (structural, no OSF) | **Active finding**: minority 3,938 vs majority 2,827 (48% wider) |
| A2 — Calgary zone asymmetry | Minority and majority Calgary zone asymmetries fall within 1 pp of each other | ≥ 10 pp difference constitutes a packing signal | Not pre-registered (structural) | **Active finding**: 12.2% minority vs 0.4% majority |
| A3 — s.15(2) eligibility audit | Each commission-invoked s.15(2) exception satisfies all criteria in the Alberta EBCA | Any invoked exception that fails a statutory criterion constitutes a procedural finding | Not pre-registered (statutory, not statistical) | See `findings/population_equality.md` |

### B-family — Partisan bias (§5.2)

| Test | Null hypothesis | Pass/fail threshold | Pre-registration | Status |
|---|---|---|---|---|
| B2 — Efficiency gap (EG) | Minority-majority EG asymmetry = 0 (no wasted-vote differential between maps) | 90%+ of 2,000 Monte Carlo parameter draws in the same direction constitutes a directional finding; 7% absolute threshold explicitly discarded in favour of Alberta-specific calibration | Exploratory; not pre-registered | Direction-active: negative in 90.5% of draws; magnitude not precise at 89 seats |
| B3 — Mean-median | Minority-majority MM gap = 0 | Directional consistency across cross-election inputs | Exploratory | Active: minority −1.20 pp vs majority −0.66 pp (minority more UCP-favourable) |
| B4 — Seats@50/50 uniform swing | Minority seats@50/50 ≤ majority seats@50/50 | Minority > majority under 2023 vote input | Exploratory | Active: 46 vs 45 (blended attribution) |
| B5 — MCMC ensemble (Mahalanobis, Ch1) | Minority feature vector drawn from neutral redistricting distribution (p ≥ 0.05) | p < 0.05 one-tailed constitutes an outlier finding | Exploratory; seeds committed to drand before shapefile receipt | **Active finding**: p = 1.40×10⁻⁶ (D² = 32.67 against 1M-plan ensemble) |
| B6 — Declination | No winning-district-margin angle asymmetry between minority and majority | Directional consistency with B2/B3/B4 | Exploratory | Minority at ensemble p1.21 (NDP-favoured tail — direction disagrees with EG; see §5.2.4) |
| B7 — Intermap permutation | Minority-majority partisan-metric distance ≤ distance between random neutral plan pairs | p < 0.05 | Pre-registered: OSF:yvc7g | See `findings/intermap_permutation_test_results.md` |

### Ch2 — SZAT boundary-choice test (§5.2.10)

| Test | Null hypothesis | Pass/fail threshold | Pre-registration | Status |
|---|---|---|---|---|
| SZAT (Ch2) | EG of the 2,110 swing VAs (those assigned differently between minority and majority) = 0 under a null distribution of 10,000 random label-shuffles | p < 0.05 one-tailed | Exploratory (seeds committed to drand) | **Active finding**: SZAT score = +0.0209, p = 0.0024 (bootstrap, 10k permutations) |

### Fisher combination (§5.5)

| Test | Null hypothesis | Pass/fail threshold | Pre-registration | Status |
|---|---|---|---|---|
| Fisher Ch1+Ch2 | Joint null: both Ch1 and Ch2 p-values drawn from Uniform(0,1) | T = −2(ln p₁ + ln p₂) ∼ χ²(4); p < 0.05 constitutes joint rejection | Exploratory (combination method not pre-registered) | **Active finding**: T = 39.03, p = 6.87×10⁻⁸; independence confirmed (§G1, ρ = −0.0014) |

### Ch3 — Neighbour drain (pre-registered)

| Test | Null hypothesis | Pass/fail threshold | Pre-registration | Status |
|---|---|---|---|---|
| Neighbour drain (Ch3) | Drain score (surplus NDP votes in packed EDs flowing to adjacent cracked EDs) = 0 | p < 0.05 against label-shuffle null | **Pre-registered: OSF:r3zm7** | See `findings/neighbour_drain_analysis.md` |

### November 2026 Lunty-committee confirmatory scorecard

| Test | Null hypothesis | Pass/fail threshold | Pre-registration | Status |
|---|---|---|---|---|
| Forensic signature scorecard | November committee map scores ≤ majority commission map on structural-irregularity count | ≥ 4 of 5 structural signals triggered constitutes a gerrymander-consistent finding | **Pre-registered: OSF:qsgy8 (AsPredicted #289,455)** | Pending — map due November 2, 2026 |

### C-family — Geographic coherence (§5.8)

| Test | Null hypothesis | Pass/fail threshold | Pre-registration | Status |
|---|---|---|---|---|
| C1 Polsby-Popper | No per-ED compactness differences between minority and majority beyond geometry-forced variation | Per-ED PP < threshold for chair-flagged districts | Not pre-registered (structural) | H10: Calgary-Nolan Hill-Cochrane PP = 0.402 (moderate); Reock = 0.230 (flagged) |
| C2 Reock | No elongation-compactness differences between minority and majority | Per-ED Reock < 0.30 conventional threshold | Not pre-registered | H10: Calgary-Nolan Hill-Cochrane Reock = 0.230 (flagged) |
| Municipal anchoring | Minority anchoring ≥ 70% CSD edge alignment (Canadian comparator norm) | Both maps within 70–85% norm = pass; outside = finding | Pre-registered (s58a6) | **Retracted** on canonical geometry: minority 72.0%, majority 80.0%; both within norm |

---

## Exoneration criteria

The minority map is exonerated of the specific directional claim (structure favours UCP relative to majority map) if ANY of the following is met:

1. Phase 4C measured vote attribution produces minority-majority EG asymmetry < 0.005 pp or opposite sign at the central parameter setting.
2. An independent analyst replicates the MCMC ensemble (same GerryChain ReCom, same shapefiles, independent seed) and the minority's Mahalanobis D² falls below p90 (D² < 18.3 against the 1M ensemble covariance matrix).
3. The SZAT bootstrap, rerun with an independently derived swing-zone definition, returns p > 0.10.
4. The November Lunty-committee 91-seat map scores ≥ 4 of 5 structural irregularity signals under the pre-registered scorecard (OSF:qsgy8), indicating that Alberta drawing difficulty rather than minority-specific choices explains the pattern.

---

## Source

§4.3 test battery; §4.3.1 multiple-comparisons handling; §5 results sections; H1-H10 hypothesis tests (§7); pre-registration amendment log (`findings/pre_registration_amendment_log.md`); `analysis/methodology/test_selection_rationale.md`.
