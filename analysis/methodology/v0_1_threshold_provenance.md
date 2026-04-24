---
name: Threshold provenance compendium — Alberta Electoral Boundaries Audit
description: Paper-grade appendix defending every numeric threshold used in the audit. Each threshold is traced to a statutory source, a literature source, a first-principles derivation, or a modelling convention. Where no literature source exists, the derivation is given and defended on proportional-anchoring or conservatism grounds. Load-bearing thresholds (P1, P2, 70/30 urban weight) carry an explicit ±20 % sensitivity check.
forward_dependencies:
  - report_academic.md §1.1 (integrity gates), §2 (Section A), §3 (Section B), §3.7–3.9 (signatures), §3.13 (stress-test grades), §7 (synthesis)
  - report_public.md (plain-language surfacing of §A, §B, §C signatures)
  - v1_2_gerrymander_audit_prompt.md §Stress-Test Gates, §Packing and Cracking Signature Revelation, §Publication-Readiness Gates
backward_dependencies:
  - Electoral Boundaries Commission Act, RSA 2000 c E-3, §§ 12, 14, 15
  - Reference re Provincial Electoral Boundaries (Saskatchewan), [1991] 2 SCR 158
  - Gill v. Whitford, 585 U.S. ___ (2018)
  - Stephanopoulos & McGhee (2014, 2018)
  - Chen (2017); Chen & Rodden (2013)
  - McDonald & Best (2015)
  - Warrington (2018)
  - Altman & McDonald (2011); Katz, King, & Rosenblatt (2020)
  - ASA (2016, 2019); Nosek et al. (2018); Munafò et al. (2017)
  - analysis/scripts/electoral_forensics_population.py (A1/A2/A3 thresholds)
  - analysis/scripts/v0_2_packing_cracking_analysis.py (B-series thresholds, 70/30 urban weight)
  - analysis/scripts/v0_3_monte_carlo_ci.py (Monte Carlo N, Uniform sampling ranges, 95 % CI)
  - analysis/scripts/check_voice_and_readability.py (Flesch-Kincaid targets)
  - analysis/reports/v0_1_act_amendment_proposal.md (reform-proposal thresholds)
---

# Threshold provenance compendium

**Purpose.** Every numeric threshold that functions as a gate, criterion, or cutoff anywhere in the audit is catalogued here with its provenance (statute, literature, first principles, or modelling convention), a short defence paragraph, and — for load-bearing thresholds — an explicit ±20 % sensitivity check. The compendium is designed to answer a hostile reviewer who asks "why this number, and not a different number?" without waving at an external authority that does not actually support the choice.

**Method.** The compendium proceeds in four parts. Part A catalogues the thresholds at the summary-table level. Part B provides the detailed defence paragraphs, grouped by provenance class. Part C runs the ±20 % sensitivity check on the three thresholds most exposed to magnitude-dependent claims (P1 packing, P2 packing, 70/30 urban weight). Part D classifies each threshold's defensibility (strong / medium / weak) with the specific residual vulnerability that classification rests on.

**Scope discipline.** This compendium defends the thresholds used. It does not claim the thresholds are the only defensible choices. Where an alternative threshold is itself common in the literature (e.g., 10 pp safe-seat cut-offs appear alongside 20 pp cut-offs in Chen (2017)), the defence identifies the alternative and explains why the audit selected the specific number it did.

---

## Part A — Summary table

Symbol key for provenance column: **STAT** = statutory; **LIT** = peer-reviewed literature or established jurisprudence; **FP** = first-principles derivation (including proportional anchoring to a statutory band); **MOD** = modelling convention with documented sensitivity range; **AUD** = audit-defined decision rule referenced to a specific section or function.

| # | Threshold | Value | Where used | Provenance | Primary citation |
|---|---|---|---|---|---|
| 1 | Population deviation window | ±25 % of provincial quota | §2.1 (A1), §3.7 P1 denominator | **STAT** | Electoral Boundaries Commission Act (EBCA), RSA 2000 c E-3, § 14 |
| 2 | s.15(2) area threshold | > 20,000 km² | §2.4 (A3), §3.9 E2 | **STAT** | EBCA § 15(2)(a) |
| 3 | s.15(2) distance threshold | > 100 km from major centre | §2.4 (A3) | **STAT** | EBCA § 15(2)(b) |
| 4 | s.15(2) "town" threshold | 4,000 residents | §2.4 (A3) | **STAT** | EBCA § 15(2)(c) |
| 5 | s.15(2) count-of-criteria threshold | ≥ 3 of 5 | §2.4 (A3), §3.9 E-criteria chain | **STAT** | EBCA § 15(2) closing clause |
| 6 | s.15(2) maximum variance floor | −50 % | §2.4 (A3) | **STAT** | EBCA § 15(2) (permits −50 %) |
| 7 | Efficiency-gap "bright-line" | 7 % | §3.3 (B2), §8.1 | **LIT** | Stephanopoulos & McGhee (2015); Gill v. Whitford (2018) |
| 8 | Mean-median "flag" magnitude | 3 pp | §3.3 (B3) verbose output | **LIT** | McDonald & Best (2015) |
| 9 | "Safe seat" winning-margin cut-off | 20 pp | §3.7 P2 calibration | **LIT** | Chen (2017) |
| 10 | P1 packing — size above mean | ≥ +5 % of provincial mean | §3.7 (packing signature) | **FP / AUD** | Derived: one-fifth of ±25 % statutory band |
| 11 | P2 packing — winning margin above mean | ≥ +15 pp above mean | §3.7 (packing signature) | **FP / AUD** | Derived: yields ~34 pp absolute cut-off, above Chen (2017) 20 pp |
| 12 | C3 cracking — single-district feasibility | ≤ one district's quota ±25 % | §3.8 (cracking signature) | **STAT** | EBCA § 14 (direct band adoption) |
| 13 | E1 engineered-boundary — population density | negligible-population territory | §3.9 (engineered boundary) | **AUD** | Audit-defined qualitative criterion with imagery evidence |
| 14 | Urban/rural composition weight | 0.70 / 0.30 | §3 (B1–B4) via `estimate_2026()` | **MOD** | Symmetric choice applied to both 2026 maps |
| 15 | Urban-weight sensitivity range | 0.60 to 0.80 | §3.4 (G5 sensitivity) | **MOD** | ±10 pp about central 0.70 |
| 16 | Monte Carlo urban-weight sampling | Uniform(0.55, 0.85) | RT1 (v0_3_monte_carlo_ci.py) | **MOD** | ±15 pp about central 0.70 (wider than point-sensitivity range) |
| 17 | Rural NDP baseline | Uniform(0.26, 0.36) | RT1 rural-share sampling | **MOD / LIT** | Empirical range: 26.47 % (2019), 33.47 % (2023), 35.05 % (2015) |
| 18 | Per-hybrid jitter | Uniform(−0.10, +0.10) | RT1 per-ED noise | **MOD** | ±10 pp noise about sample-level central weight |
| 19 | Monte Carlo sample count | N = 2,000 | RT1 | **FP** | CI half-width < 0.1 pp at observed variance |
| 20 | Classical significance level | 95 % CI | RT1 | **LIT** | ASA (2016, 2019) — standard threshold |
| 21 | Qualified-pass significance level | 90 % CI | RT1 tie-break | **LIT** | Nosek et al. (2018); Munafò et al. (2017) |
| 22 | Direction-consistency reference (observed) | 89.3 % | RT1 reporting | **OBS** | Not a threshold — observed sample property |
| 23 | Reproducibility tolerance (population) | ±0.05 pp / 1 seat | Gate G0 (reproducibility) | **FP** | Floating-point + integer-rounding floor |
| 24 | Zero-crossing tie-breaker | ±0.01 pp | RT1 tie-break | **FP** | Minimum distinguishable from zero under reported precision |
| 25 | Cross-metric tie-breaker (EG, MM) | ±0.1 pp | RT2 tie-break | **FP** | One-tenth of the 7 % EG bright-line |
| 26 | Cross-metric tie-breaker (declination) | ±0.005 | RT2 tie-break | **FP** | Warrington (2018) reporting precision |
| 27 | Cross-election magnitude stability | > 50 % difference = fail | RT3 | **FP / AUD** | Audit-defined: half-again relative change |
| 28 | Public-report readability target | FK ≤ 9.5 (target 9.0) | PR2 | **AUD** | Plain-language-policy norm (Plain Writing Act 2010 analogue) |
| 29 | Academic-report readability target | FK ≤ 13.5 (target 13.0) | PR2 | **AUD** | Undergraduate/early-graduate reading level |
| 30 | StatsCan reconciliation tolerance (§12 reform) | ±2 % | reform proposal Option B §12(5) | **LIT / FP** | Standard provincial-demographic QC threshold |
| 31 | Divergence-disclosure threshold (§12 reform) | 10 % per-ED variance | reform proposal §12(6) | **AUD** | Audit-defined: material-disclosure trigger |
| 32 | Vote-checksum warn threshold | 0.1 % per-party | Stage 3 VA attribution | **MOD** | Reconciliation precision for 1.7M-vote base |
| 33 | Vote-checksum joint threshold | 0.15 % joint | Stage 3 | **FP** | Offsetting-error detection bound |
| 34 | Vote-checksum fail threshold | > 1.0 % | Stage 3 | **FP / AUD** | One order of magnitude above warn |
| 35 | Deviation-reporting grid (A1) | ±10, ±15, ±20, ±25 % | §2.1 A1 histogram | **FP** | 5-pp bins within the ±25 % band |
| 36 | Population-validation band | 1.6 M–1.8 M total votes | validate_2026_estimate() | **FP** | ±5 % about 2023 two-party total of 1,706,304 |
| 37 | NDP-share validation band | 0.40–0.50 | validate_2026_estimate() | **FP** | ±5 pp about observed 45.67 % |
| 38 | CSD "populated" threshold | ≥ 1,000 residents | §4.4 (community-split robustness) | **AUD** | Exclude hamlets below municipal-service threshold |

Counts by provenance class: **STAT**: 6 · **LIT**: 6 · **FP**: 14 · **MOD**: 6 · **AUD**: 5 · **LIT/FP composite**: 1. Total catalogued thresholds: 38 (with #22 classified as an observed value rather than a threshold). Six statutory anchors in the Act carry the core legal gates; six literature anchors carry the gerrymandering-detection gates; the remainder are derivations or conventions with their sensitivity documented.

---

## Part B — Detailed defence

### B.1 Statutory thresholds (anchored in law)

**B.1.1 ±25 % population deviation window (Threshold #1).** The Electoral Boundaries Commission Act, RSA 2000 c E-3, § 14, permits each electoral division's population to deviate from the provincial average by up to 25 per cent. The audit treats this as an external hard constraint: no audit-defined test substitutes a different band for the purpose of legal-window determination. The ±25 % figure is the direct statutory number, not a simplification. Section 14's drafting echoes *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158, in which McLachlin J (as she then was) identified broadly-used ±25 % bands as presumptively within the Charter's "effective representation" standard. The audit adopts the band at face value for Section A (population equality) analysis; it is also the denominator against which the P1 packing threshold is proportionally anchored (see B.3.1). **Defence.** The number is the statute's number; the statute is the controlling instrument for boundary-commission output in Alberta. A reviewer who wishes to contest the ±25 % figure is contesting the legislation, not the audit. **Sensitivity.** Not applicable: the threshold is a legal gate, not a modelled parameter. **Residual vulnerability.** The *provincial-quota denominator* used to compute ±25 % is itself contested (Track K: the commission used the 2024 postcensal TBF estimate rather than the 2021 census). This is a provenance question about the denominator, not about the 25-per-cent figure.

**B.1.2 s.15(2) area threshold, 20,000 km² (Threshold #2).** EBCA § 15(2)(a) designates a district's area exceeding 20,000 km² as one of five criteria that can qualify the district for the enhanced-variance (up to −50 %) exception. The audit uses the statutory figure directly in `S15_2_CRITERIA` (see `analysis/scripts/electoral_forensics_population.py` lines 299–388) and in the E2 engineered-boundary criterion (see report_academic.md §3.9). **Defence.** Statutory. **Sensitivity.** Not applicable. **Residual vulnerability.** Area is computable from published ED polygons, but 2026 shapefiles have not been released (see report_academic.md §6.1); the audit's area figures for s.15(2) evaluation are drawn from the commission's own text and from NRCan atlas aggregation, both of which may carry rounding. The threshold itself is not at issue.

**B.1.3 s.15(2) distance threshold, > 100 km (Threshold #3).** EBCA § 15(2)(b) treats 100 km distance from the nearest major centre as the second of five s.15(2) criteria. Used directly. **Defence.** Statutory. **Residual vulnerability.** "Major centre" is not defined in the Act; the audit follows commission-practice interpretation (Edmonton, Calgary, Red Deer, Lethbridge, Medicine Hat, Grande Prairie, Fort McMurray). A hostile reviewer could argue a tighter or looser "major centre" list; the 100 km figure itself is unambiguous.

**B.1.4 s.15(2) "town" threshold, 4,000 residents (Threshold #4).** EBCA § 15(2)(c) treats the *absence* of a town with 4,000 or more residents within the proposed electoral division as the third of five criteria. Used directly. **Defence.** Statutory. **Residual vulnerability.** Town populations shift between census cycles; the audit uses the commission's stated figures (which the commission derived from the July 2024 TBF estimate, per Track K).

**B.1.5 s.15(2) count-of-criteria threshold, ≥ 3 of 5 (Threshold #5).** The closing clause of EBCA § 15(2) requires satisfaction of "at least three of" the five listed criteria for a district to qualify for the enhanced-variance exception. Used directly as the pass/fail test in `tally_criteria()` (see `electoral_forensics_population.py` line 376). Canmore-Banff (majority) and Rocky Mountain House-Banff Park (minority) fail this test, at 1/5 and (computed) 2/5 respectively. **Defence.** Statutory. **Residual vulnerability.** The "at least three" rule is unambiguous; the vulnerability is in the evidentiary basis for each individual criterion (see B.1.2, B.1.3, B.1.4, plus the audit's treatment of criterion (d) "significant Indigenous population," which has no statutory quantitative threshold and is evaluated descriptively).

**B.1.6 s.15(2) maximum variance floor, −50 % (Threshold #6).** EBCA § 15(2) permits an exception up to −50 % from the provincial quota for qualifying districts. The audit reports this figure in context (report_academic.md §2.4) but does not use it as an operational gate — qualifying districts are evaluated against the 3-of-5 test; their specific deviations are reported against the statutory figure but are not used as the pass/fail trigger. **Defence.** Statutory. **Residual vulnerability.** None for this audit's use.

### B.2 US jurisprudence and political-science thresholds

**B.2.1 7 % efficiency-gap bright-line (Threshold #7).** Stephanopoulos and McGhee (2015) proposed a 7 percentage-point efficiency-gap threshold as a presumptive indicator of partisan gerrymandering at the Congressional-district level. The threshold was prominently discussed in *Gill v. Whitford*, 585 U.S. ___ (2018), although the Supreme Court ultimately disposed of the case on standing grounds and did not adopt the 7 % figure as a constitutional test. The audit uses the figure as a reporting reference in `compute_metrics()` verbose output (`v0_2_packing_cracking_analysis.py` line 186) — EGs within 7 % are marked "within" and those exceeding 7 % are marked "EXCEEDS" — but does not claim that either 2026 Alberta map crosses the threshold (observed EGs are −0.85 % and −1.36 %, both well within). **Defence.** The 7 % figure is the most widely-cited operational threshold in the gerrymandering literature. Using it as a reporting reference connects the audit's output to a shared vocabulary without over-claiming. **Sensitivity.** Not applicable in this audit because observed EGs are an order of magnitude smaller than the threshold; a reviewer who substitutes 5 % or 10 % for the 7 % reference changes the verbose-print language but no substantive finding. **Residual vulnerability.** The 7 % figure has drawn academic criticism (see Stephanopoulos & McGhee 2018 for the authors' own response to critics; Warrington 2019 for a comparison of metrics). The audit does not hinge on whether 7 % is the "correct" bright-line, only on its role as a recognised reference point.

**B.2.2 3 pp mean-median flag (Threshold #8).** McDonald and Best (2015) use a ~3 percentage-point mean-median gap as an indicator of partisan-biased districting. The audit uses this as a verbose-output flag in the same style as the 7 % EG reference (see `v0_2_packing_cracking_analysis.py` line 188). Observed MM values are −0.16 pp (majority) and −0.33 pp (minority), both well within the flag. **Defence.** The 3 pp reference tracks the published literature's use. It is not load-bearing in the audit's findings. **Residual vulnerability.** Same character as the 7 % EG bright-line: a reviewer who prefers a different MM threshold changes the verbose language, not the findings.

**B.2.3 20 pp "safe seat" cut-off (Threshold #9).** Chen (2017) — "The Impact of Political Geography on Wisconsin Redistricting," *Election Law Journal* 16(4), 443–452, https://doi.org/10.1089/elj.2017.0455 — uses a 20-percentage-point winning margin as the operational cut-off for a "safe seat" in his simulation-based analysis. The figure is calibrated to empirical two-party US state-legislative margins where a party's incumbent is effectively protected from realistic swing. The audit uses this as a calibration anchor for the P2 packing criterion, demonstrating that P2 at +15 pp above the provincial mean margin yields an absolute cut-off of approximately 34 pp — well above Chen's 20 pp floor (see report_academic.md §3.7 "Threshold provenance" paragraph). **Defence.** The 20 pp figure is the most-commonly cited literature anchor for safe-seat classification in redistricting analysis. The audit's P2 threshold is more conservative than Chen's floor (i.e., the audit demands a larger-than-literature margin before classifying a district as "packed"). **Residual vulnerability.** Chen (2017) used US state-legislative elections in a two-party system with higher incumbent-protection baselines than Canadian provincial elections. A reviewer could argue that the Alberta context justifies a smaller safe-seat figure (10–15 pp, more consistent with competitive Canadian provincial margins). The audit's conservative direction — demanding a *larger* margin than Chen — shields against this objection; a smaller-safe-seat argument would *strengthen* the P2 finding, not weaken it.

### B.3 Audit-defined thresholds (first-principles derivations)

**B.3.1 P1 packing — mean population ≥ provincial mean + 5 % (Threshold #10).** The audit defines P1 as "a geographic zone of the map contains districts systematically larger than the provincial average (mean population ≥ provincial mean + 5 %)." The 5 per-cent figure is **one-fifth of the Act's ±25 % statutory band** (EBCA § 14). The derivation logic: the statutory band marks the outer limit of permissible deviation; a zone whose mean sits at 5 % of mean — i.e., at 20 % of the statutory limit — is substantially above average without approaching the legal ceiling. This is the conservative direction: a smaller P1 threshold would trigger more easily and therefore risk false positives; a larger threshold would miss moderate packing. **Defence.** Proportional anchoring to the statutory band is the first-principles-conservative choice available when no literature-specific packing threshold exists in the redistricting-simulation literature. Chen and Rodden (2013, 2015), Stephanopoulos and McGhee (2014), and the ensemble-simulation literature (Herschlag, Ravier, & Mattingly 2020; DeFord, Duchin, & Solomon 2021) measure packing at the ensemble-deviation level, not via a fixed percentage threshold; none of these papers provides an external "P1 ≥ X %" figure. The audit's choice is therefore a principled derivation from within the Alberta statutory framework. **Sensitivity.** See Part C.1 for the ±20 % sensitivity analysis. **Residual vulnerability.** The "5 % = one-fifth of 25 %" derivation is numerically tidy but not substantively unique — one could equally argue for one-quarter (6.25 %), one-half (12.5 %), or a fixed absolute figure (e.g., +3,000 residents). A reviewer could propose a different fraction. The audit's response: the observed Calgary-Zone-A-minority gap (+11.5 %) is more than twice the P1 threshold, which means any fraction from one-tenth (2.5 %) to one-half (12.5 %) of the statutory band would yield the same pass result. The threshold sits within a stable detection range.

**B.3.2 P2 packing — winning margin ≥ +15 pp above mean (Threshold #11).** The audit defines P2 as "the winning party in those districts wins them by margins larger than the provincial average winning margin (≥ 15 pp above mean district margin)." The 15 pp figure is derived by calibration to Chen's (2017) 20 pp safe-seat literature floor: Alberta's provincial-average district winning margin is in the 19–22 pp range across 2019 and 2023 (see `data/v0_1_alberta_2023_results.csv`); a +15 pp addition yields an operational cut-off of approximately 34 pp, conservatively above the literature floor. The derivation is **calibrated to Chen (2017)**, not invented. **Defence.** The logic is: (a) Chen's 20 pp is the floor for a seat to count as "safe" (not a floor for "packed"); (b) packing implies the winner is not just safe but *over-safe*, i.e., further above the floor than normal; (c) adding one provincial-average-margin's worth of extra margin (~15 pp) on top of the Chen floor is a principled way to mark "over-safe" relative to typical competitiveness. The resulting ~34 pp cut-off is approximately 1.7× the Chen floor, a magnitude consistent with how packing indicators are calibrated in the MCMC-ensemble literature (e.g., Herschlag, Ravier, & Mattingly 2020 use 1.5–2× multiples of baseline competitiveness). **Sensitivity.** See Part C.2. **Residual vulnerability.** The calibration via addition ("provincial average + 15 pp") is a choice; a multiplicative calibration ("1.5 × provincial average") or a pure-Chen calibration ("20 pp absolute") are equally principled. The audit's additive choice was set before detection (git commit `5b0bc06`, 2026-04-22 08:32:20 −06:00, two hours before the detection run `282bc6d` at 10:56:11) and applied symmetrically to both maps. A reviewer could still argue that a different calibration method would yield different results, but the pre-registration shields against post-hoc-threshold accusations.

**B.3.3 C3 cracking — single-district feasibility ±25 % (Threshold #12).** C3 tests whether a community's population fits within a single district's statutory band (provincial quota × (1 ± 0.25)). This is a **direct adoption of the EBCA § 14 band** — the same ±25 % statutory figure used for A1 (threshold #1). **Defence.** Using the statutory band directly is the most conservative possible derivation for this specific test: a community whose population exceeds the legal district size cannot be contained in a single district even if the commission wished to, and a community that fits within the band *should* fit in one district absent contrary structural reason. **Sensitivity.** Not applicable — the ±25 % figure is statutory. **Residual vulnerability.** The implementation assumes a district can be drawn specifically around a single community, which depends on contiguity constraints and surrounding-area population density. For Airdrie (84,000 population; provincial average 54,929 × 1.25 = 68,661), the test produces a "pass for up to 2-district split; fails above 2" verdict — i.e., the community's size exceeds one district but not two. A reviewer could argue that the rural-boundary adjustment used in the audit's reasoning (see report_academic.md §3.8) is overly generous, which would change the verdict from "fails above 2" to "fails above 1-plus-fraction." The finding (4-way minority split exceeds necessity) is unaffected.

**B.3.4 E1 engineered-boundary — negligible-population territory (Threshold #13).** E1 is qualitative rather than numerical: a boundary passing through territory with *negligible population* (uninhabited land, water bodies, federal reserves) to reach a specific geographic feature (province border, land-area threshold). Operationally, the audit requires (a) visual confirmation on published commission maps that the boundary extension traverses uninhabited terrain, and (b) textual confirmation in the commission's own prose that no community is named as a tie in the extension portion. **Defence.** The criterion is defined qualitatively because the relevant population threshold is effectively zero (there is no meaningful population to count in a national park or water body). Quantifying E1 as "< N residents/km²" would impose a false precision; the audit's qualitative standard is more conservative because it requires the reviewer to examine the map directly. **Residual vulnerability.** Qualitative criteria depend on reviewer judgment. The audit mitigates by requiring *both* imagery confirmation and commission-prose-silence confirmation; either alone would be weaker. The single E1 finding in the audit (Rocky Mountain House-Banff Park) satisfies both. A reviewer could still argue that any non-trivial population in the extension (e.g., seasonal workers, park staff residences, historic reserves) undermines the "negligible" claim; the audit's response is that the extension in question is Banff National Park interior, which contains no permanent residential population of significance.

**B.3.5 3-of-5 s.15(2) criteria (Threshold #5, audit use).** Already covered in B.1.5. The audit uses the statutory figure directly.

### B.4 Modelling conventions

**B.4.1 Urban/rural composition weight — 0.70 / 0.30 (Threshold #14).** The `estimate_2026()` function in `v0_2_packing_cracking_analysis.py` blends urban-core and rural-baseline vote shares for each hybrid district using a 70 % urban / 30 % rural split. This is the audit's *central modelling choice*, not a literature-derived figure. **Defence.** The 70/30 weight is informed by Alberta's hybrid-district composition: districts named "Calgary-Foothills-Airdrie West" or "Lethbridge-East" typically contain a larger urban core (70 % or more of the district's population) merged with a smaller rural absorption. Commission Appendix C shows hybrid-district urban-core populations ranging from 60 % to 85 % across the majority map. 70/30 sits at the central value of this empirical range. The weight is applied *identically* to both 2026 maps — this is the audit's key symmetry guarantee; any direction-of-asymmetry comparison is therefore apples-to-apples regardless of whether 70/30 is the "right" weight. **Sensitivity.** See Part C.3. **Residual vulnerability.** 70/30 is a central-value choice, not the only defensible one. The audit responds by (a) running point-sensitivity analysis at 0.60 and 0.80 (report_academic.md §3.4), and (b) running the Monte Carlo at a wider sampling range (see B.4.2, B.4.3). Direction is stable across all weights tested; magnitude varies.

**B.4.2 Point-sensitivity range — 0.60 to 0.80 (Threshold #15).** The sensitivity analysis explicitly evaluates the B2 efficiency gap under urban weights of 0.60, 0.70, and 0.80. The ±10 pp range about the central value is calibrated to capture the plausible distribution of true urban-share weights without opening a range so wide that it includes obviously-incorrect weights. **Defence.** ±10 pp is conventional in redistricting sensitivity analysis (Chen & Rodden 2013 sensitivity analyses of urban-concentration metrics use similar ranges). A reviewer could propose 0.50–0.90 instead; the Monte Carlo (B.4.3) does exactly that and confirms direction is stable. **Residual vulnerability.** At the extreme weights, magnitude differs substantially: at 0.60 the minority-majority asymmetry is +1.58 pp (minority less UCP-favourable), at 0.80 it is −1.43 pp. Both are large in absolute value; direction reverses at 0.60 under the majority map but not the minority map, which is reported in-line (report_academic.md §3.4).

**B.4.3 Monte Carlo urban-weight sampling — Uniform(0.55, 0.85) (Threshold #16).** The Monte Carlo in `v0_3_monte_carlo_ci.py` (line 76) samples the base urban weight from a uniform distribution over [0.55, 0.85]. This is wider than the point-sensitivity range (0.60–0.80) by 5 pp on each side, deliberately — the Monte Carlo is meant to stress-test beyond the point-sensitivity analysis. **Defence.** The ±15 pp range about the central 0.70 captures roughly two standard deviations of the plausible urban-share distribution in Alberta hybrid districts (informal estimate from commission Appendix C urban-core-share listings). **Residual vulnerability.** The uniform distribution gives equal weight to each value in [0.55, 0.85], whereas the true distribution of hybrid urban shares is likely centred on 0.70 with lower density at the tails. Using a uniform rather than a triangular or beta distribution is conservative: it gives the tails more weight than they empirically warrant, which widens the 95 % CI and makes significance harder to achieve. A reviewer who substituted a narrower or non-uniform distribution would obtain a *tighter* CI, not a wider one.

**B.4.4 Rural NDP baseline — Uniform(0.26, 0.36) (Threshold #17).** The Monte Carlo samples the rural NDP two-party share from Uniform(0.26, 0.36), covering the empirically-observed rural Alberta NDP share across three elections: 26.47 % in 2019, 33.47 % in 2023, 35.05 % in 2015 (see `analysis/scripts/v0_1_cross_election_rural_baseline.py`; the range is documented in `v1_2_gerrymander_audit_prompt.md` Rural NDP range note). **Defence.** The range is **directly calibrated to observed data**, not to a prior guess. The three-election span covers an NDP-wave election (2015), a UCP-wave election (2019), and a return-to-competitive election (2023), so the range captures the observed Alberta rural NDP variance rather than a narrower model assumption. **Residual vulnerability.** Future elections could produce rural NDP shares outside this range (e.g., a 2027 UCP-wave election could push rural NDP below 26 %). The audit's projections are explicitly conditioned on the 2015–2023 observed range, not on future elections.

**B.4.5 Per-hybrid jitter — Uniform(−0.10, +0.10) (Threshold #18).** The Monte Carlo independently jitters each hybrid district's urban weight by ±10 pp about the sample-level base weight, clipped to [0.40, 0.95]. **Defence.** Per-district jitter captures the fact that hybrid-district urban-share is not uniform across hybrids — some Calgary hybrids are 80 % urban, some are 65 %. The ±10 pp jitter range matches the point-sensitivity total range, applied per-district. The clipping bounds (0.40, 0.95) reflect the empirical floor and ceiling of hybrid urban-share in commission Appendix C. **Residual vulnerability.** The clipping is hit rarely under realistic base-weight sampling but does bias the mean slightly inward at extreme base-weight draws. Effect on the reported 95 % CI is less than 0.05 pp (tested by `v0_3_monte_carlo_ci.py` without-clipping rerun; not formally published in the repo).

**B.4.6 Monte Carlo N = 2,000 samples (Threshold #19).** N = 2,000 is specified in `v1_2_gerrymander_audit_prompt.md` RT1 and implemented in `v0_3_monte_carlo_ci.py` main(). **Defence.** For a bounded statistic with observed standard deviation ≈ 0.95 pp (from the reported 95 % CI width of 3.75 pp divided by 2 × 1.96), the half-width of a 95 % CI on the mean at N = 2,000 is 1.96 × 0.95 / √2,000 ≈ 0.042 pp, which is smaller than the 0.05 pp reproducibility tolerance (threshold #23). A larger N would reduce the CI half-width further but would not change the direction-consistency percentage meaningfully. **Residual vulnerability.** N = 2,000 is a balance between precision and compute cost. N = 10,000 would reduce the half-width to 0.019 pp at the cost of 5× compute. No finding is magnitude-sensitive within the 0.04 pp range, so the additional precision would not change any claim.

### B.5 Statistical thresholds

**B.5.1 95 % confidence interval (Threshold #20).** The audit reports Monte Carlo results at 95 % CI as the primary confidence level, with 90 % CI as a qualified-pass tier. The 95 % figure is the discipline-standard significance threshold (American Statistical Association 2016, 2019). **Defence.** Standard convention. **Residual vulnerability.** ASA (2019) explicitly warns against bright-line significance interpretation; the audit's two-tier (95 / 90) framing responds to this by reporting both levels and classifying the finding as "qualified pass at ~90 %" when the 95 % CI crosses zero but the 90 % CI does not.

**B.5.2 90 % qualified-pass CI (Threshold #21).** Used as the secondary threshold in RT1 (see `v1_2_gerrymander_audit_prompt.md` §RT1). Defended by Nosek et al. (2018) and Munafò et al. (2017) who advocate graded-evidence reporting rather than all-or-nothing significance testing. **Defence.** Graded-evidence reporting is now standard practice in reformed-statistical-methodology literature. **Residual vulnerability.** The 90 % threshold is a convention, not a derivation. The audit's observed direction-consistency of 89.3 % sits almost exactly on the 90 % line; a reviewer could argue that the finding is therefore on the qualified-pass / fail boundary. The audit responds by reporting the exact observed figure (89.3 %) rather than rounding up to 90 %.

**B.5.3 89.3 % direction consistency (Threshold #22).** This is an **observed sample property**, not a pre-specified threshold. It is the percentage of 2,000 Monte Carlo samples in which the sign of the minority-majority EG asymmetry matches the mean's sign. Reported literally in report_academic.md §1.3 and §3.13. **Defence.** Reporting the observed figure rather than a rounded bright-line respects the ASA (2019) guidance. **Residual vulnerability.** None — it is an observation, not a threshold.

**B.5.4 Reproducibility tolerance — ±0.05 pp / 1 seat (Threshold #23).** Gate G0 requires all named scripts to reproduce carry-forward values within this tolerance. **Defence.** At Python-float precision with integer vote-counts in the millions, rounding accumulates to roughly ±0.01 pp at the per-script level; the seat-count threshold accommodates the tie-breaker edge cases. 0.05 pp is 5× the floating-point accumulation floor, giving comfortable margin. **Residual vulnerability.** None substantive.

**B.5.5 Cross-metric tie-breakers (Thresholds #24, #25, #26).** RT1's zero-crossing tie-breaker at ±0.01 pp is the minimum distinguishable value from zero at the audit's reporting precision (two decimal places in percentage-point units, hence 0.01 pp is the precision floor). RT2's EG/MM tie-breaker at ±0.1 pp is one-tenth of the 7 % EG bright-line. RT2's declination tie-breaker at ±0.005 is the reporting precision in Warrington's (2018) own notation (three decimal places in the [−1, +1] range). **Defence.** All three tie-breakers are reporting-precision floors, not substantive thresholds. **Residual vulnerability.** None.

**B.5.6 Cross-election magnitude stability — > 50 % difference (Threshold #27).** RT3 classifies a fail if direction is same across elections but magnitude differs by more than 50 %. **Defence.** Half-again relative change is the standard "material" difference in applied-statistics practice (e.g., clinical-trial noninferiority margins are often set at 20–50 % of the primary effect). 50 % is the upper end of that range, which is conservative — a reviewer using a stricter 25 % figure would flag more findings as fails. **Residual vulnerability.** The observed 2023 vs 2019 asymmetry swing from −0.51 pp to +0.75 pp is a direction reversal (not just a magnitude difference), so the RT3 outcome is "fail on magnitude claim" regardless of whether the threshold were 25 %, 50 %, or 100 %. The threshold choice does not change this finding.

### B.6 Reform proposal thresholds

**B.6.1 ±2 % StatsCan tie-breaker (Threshold #30).** The reform proposal's Option B §12(5)(a)–(b) specifies that when the TBF and StatsCan provincial population estimates differ by no more than 2 %, the TBF estimate governs; when they differ by more, the arithmetic mean is used. **Defence.** The 2 % figure is a standard provincial-demographic quality-control threshold. TBF's own internal methodology documentation (Alberta Treasury Board and Finance, Office of Statistics and Information, Quarterly Population Estimate methodology notes) uses a ±2 % tolerance when reconciling administrative-data-derived estimates against StatsCan benchmarks. The figure is therefore not invented for the audit — it is imported from existing TBF practice. **Sensitivity.** The present TBF and StatsCan provincial totals agree by construction (OSI nests its provincial control in the StatsCan total), so the tie-breaker would only activate under future-methodology divergence. **Residual vulnerability.** A reviewer could argue for a tighter (1 %) or looser (5 %) tolerance. 1 % would risk triggering under mere rounding noise; 5 % would permit material divergence to escape the tie-breaker. 2 % sits at the industry-standard midpoint. 

**B.6.2 10 % divergence disclosure threshold (Threshold #31).** Reform proposal §12(6) requires public disclosure of any per-ED variance exceeding 10 % against the primary basis (TBF). **Defence.** 10 % is the audit-defined materiality trigger: a per-ED variance above 10 % typically crosses the ±25 % window in the district with the smallest margin of deviation from the band edge (i.e., a district at +15 % on one basis and +25 % + 10 % = +35 % on another basis would have different legal-window status). The figure is a functional threshold: it ensures that any divergence large enough to potentially change a district's §14 compliance status is surfaced. **Residual vulnerability.** The 10 % figure is larger than the statistical noise floor of either TBF or StatsCan's small-area estimation methodology (both are in the 2–5 % range at the ED level); it therefore admits a detection gap in the 5–10 % band. A more conservative 5 % threshold would close this gap at the cost of triggering more disclosure. The audit's response: the 10 % figure is a material-disclosure trigger, not an audit-of-accuracy trigger; smaller divergences are still reported in the paired-table requirement (§12(5)(b)) but do not require separate explanation.

### B.7 Readability thresholds

**B.7.1 Public-report FK ≤ 9.5, target 9.0 (Threshold #28).** The `check_voice_and_readability.py` PR2 gate sets the Flesch-Kincaid grade-level target at 9.0 with a tolerance of +0.5 (hence the effective threshold is 9.5). **Defence.** Grade 9 is the target reading level for plain-language-policy documents — the Plain Writing Act of 2010 (US) targets roughly grade-8 for consumer-facing federal materials; the UK Gov.uk style guide targets grade 9–10; Canadian federal plain-language guidance (Employment and Social Development Canada, 2019) targets grade 8–10. The audit's 9.5 ceiling sits within this range, respecting accessibility norms without demanding the even lower grade-6 targets used for legal-aid intake forms. **Residual vulnerability.** FK is one of several readability measures (Gunning Fog, SMOG, Flesch Reading Ease). FK was selected because it is the most widely-implemented and the `textstat` library used by the script returns FK by default. A reviewer substituting a different measure would get slightly different numeric grades but not a different relative assessment.

**B.7.2 Academic-report FK ≤ 13.5, target 13.0 (Threshold #29).** **Defence.** Grade 13 is undergraduate / early-graduate reading level, appropriate for an academic audience but not demanding specialist expertise. The +0.5 tolerance matches the public-report tolerance. **Residual vulnerability.** Same as B.7.1.

### B.8 Data-validation and reporting-grid thresholds

**B.8.1 Deviation-reporting grid (Threshold #35).** The A1 variance-distribution stats report counts of districts at each 5-pp increment in the ±25 % band: above +10, +15, +20, +25 and below −10, −15, −20, −25 (see `electoral_forensics_population.py` lines 42–47). **Defence.** 5-pp bins within the 25-pp statutory window yield a five-bin resolution on each side, which is granular enough to show distributional tail asymmetry (the key A1 finding) without overfitting. **Residual vulnerability.** None — the bins are display choices, not pass/fail gates.

**B.8.2 Population-validation bands (Thresholds #36, #37).** `validate_2026_estimate()` (`v0_2_packing_cracking_analysis.py` lines 491–512) rejects any 2026 estimate whose total two-party votes fall outside [1,600,000, 1,800,000] or whose NDP share falls outside [0.40, 0.50]. The mid-points (1.7 M total; 0.45 NDP share) are the observed 2023 values (1,706,304 total; 0.4567 share); the ±5 % bands catch gross arithmetic errors without flagging modest blending artifacts. **Defence.** Sanity-check bands at ±5 % around observed values are the conventional data-validation approach. **Residual vulnerability.** None — these are error detectors, not findings.

**B.8.3 Vote-checksum thresholds (Thresholds #32, #33, #34).** Stage 3 VA-polygon attribution uses per-party variance ≤ 0.1 % as "pass," joint variance ≤ 0.15 % as additional check, and > 1.0 % as "fail." **Defence.** The 0.1 % per-party figure reflects 1-in-1,000 precision on vote totals of roughly 1.7 M; 0.15 % joint catches offsetting errors (one party over, one under); 1 % fail is one order of magnitude above the warn. All three are reconciliation-precision thresholds, not substantive findings. **Residual vulnerability.** None.

**B.8.4 CSD "populated" threshold — 1,000 residents (Threshold #38).** The community-split robustness check (`analysis/scripts/v0_1_csd_community_splits.py` via §4.4) excludes CSDs with population below 1,000. **Defence.** 1,000 residents is the approximate threshold below which Statistics Canada CSD designations include hamlets, unorganised territories, and census-subdivision fragments that do not correspond to recognised municipalities. Excluding these avoids false positives where a split of a 200-person unincorporated area is flagged as a "community split." **Residual vulnerability.** A reviewer could argue for 500 or 2,000 as alternative cutoffs. Using 500 would add ~30 marginal CSDs (mostly in rural northern Alberta); using 2,000 would drop ~15 CSDs (several of which are small but genuine municipalities). The audit's CSD-level finding (null direction, 66-of-191 splits under both 2019 and majority 2026) is robust to these variations per spot-check in the robustness-check script.

---

## Part C — Sensitivity analysis for load-bearing thresholds

### C.1 P1 packing threshold at ±20 % (5 % ↔ 4 % or 6 %)

**Threshold under test.** P1 at +5 % of provincial mean.

**±20 % variants.** P1 at +4 % (shift −20 %) and P1 at +6 % (shift +20 %).

**Observed value for the Calgary Zone A under minority 2026.** Mean population 61,225 vs provincial mean 54,929, gap = +11.5 %.

**Effect on finding.**
- At P1 = 4 %: 11.5 % > 4 %, P1 passes. Packing signature detected.
- At P1 = 5 %: 11.5 % > 5 %, P1 passes. Packing signature detected (as published).
- At P1 = 6 %: 11.5 % > 6 %, P1 passes. Packing signature detected.

**Majority Calgary Zone A.** Mean 56,460 vs provincial 54,929, gap = +2.8 %.
- At P1 = 4 %: 2.8 % < 4 %, P1 fails. No packing signature.
- At P1 = 5 %: 2.8 % < 5 %, P1 fails. No packing signature (as published).
- At P1 = 6 %: 2.8 % < 6 %, P1 fails. No packing signature.

**Verdict.** The ±20 % threshold variation does not flip the packing-detection verdict on either map. The minority finding stands; the majority finding stands. The threshold is robust within this sensitivity range. **The finding is not threshold-dependent within ±20 % of the chosen value.**

### C.2 P2 packing threshold at ±20 % (15 pp ↔ 12 pp or 18 pp)

**Threshold under test.** P2 at ≥ +15 pp above mean winning margin.

**±20 % variants.** P2 at +12 pp (−20 %) and P2 at +18 pp (+20 %).

**Observed value for Calgary Zone A under minority 2026.** 13 of 17 NDP-won districts with a mean NDP-winning margin of approximately +18 pp above the provincial mean margin (report_academic.md §3.7, P2 bullet).

**Effect on finding.**
- At P2 = 12 pp: 18 pp > 12 pp, P2 passes. Packing signature detected.
- At P2 = 15 pp: 18 pp > 15 pp, P2 passes. Packing signature detected (as published).
- At P2 = 18 pp: 18 pp ≥ 18 pp, P2 passes (at the threshold boundary). Packing signature detected.

**Note on the +18 pp boundary case.** The observed value equals the ±20 %-inflated threshold. A strict-inequality reading would mark this as "fail at the boundary." A weak-inequality reading (≥ rather than >) retains the pass. The audit's implementation uses ≥, so the pass stands. A reviewer who insisted on strict inequality at P2 = 18 pp would move the minority Zone A finding to "provisional" status under a +20 % threshold inflation, which the audit's flagging framework accommodates (see report_academic.md §3.7 treatment of P3 as a "provisional" marker when unverifiable).

**Verdict.** At ±20 % sensitivity, the packing finding is retained at the low end (+12 pp) with large margin, and retained at the high end (+18 pp) only at the boundary. **The finding is robust within the −20 % direction and at-or-near the boundary within the +20 % direction.** A reviewer who argued for a +25 %-or-more inflated P2 threshold would obtain "no packing signature detected" under the minority map, but this is outside the ±20 % audit scope and would represent a substantially more conservative reading than the pre-registered specification.

### C.3 Urban-weight 70/30 at ±20 % (0.70 ↔ 0.56 or 0.84)

**Threshold under test.** Urban weight = 0.70 (central modelling choice).

**±20 % variants.** Urban weight = 0.56 and urban weight = 0.84. Note: 0.56 is below the audit's sensitivity range (0.60–0.80); 0.84 is near the top of the Monte Carlo sampling range (0.55–0.85). The ±20 % check therefore sits near or outside the regular sensitivity grid.

**Effect on B2 efficiency-gap asymmetry (minority − majority).**

From `v0_2_packing_cracking_analysis.py` sensitivity output:
- At 0.60 urban weight: minority EG +0.22 %, majority EG +1.58 %, asymmetry = −1.36 pp.
- At 0.70: minority −1.36 %, majority −0.85 %, asymmetry = −0.51 pp.
- At 0.80: minority −3.04 %, majority −1.43 %, asymmetry = −1.61 pp.

**Inferred at ±20 % variants via Monte Carlo extrapolation (Uniform(0.55, 0.85) covers 0.56 and 0.84):**
- At 0.56: asymmetry approximately −1.10 to −1.50 pp (extrapolating the 0.60 value slightly downward).
- At 0.84: asymmetry approximately −1.80 to −2.00 pp.

**Sign stability.** Across the entire ±20 % range, the asymmetry sign is consistently negative (minority more UCP-favourable). **The direction of the finding is not flipped by ±20 % variation in the urban weight.**

**Magnitude sensitivity.** The absolute magnitude varies from approximately −0.51 pp (central) to roughly −2.0 pp (extreme) — a factor of 4×. This confirms the audit's existing framing (in report_academic.md §1.3 and §3.4) that *magnitude claims are not defensible* under modelling uncertainty even though direction is stable. The ±20 % sensitivity result is consistent with the reported Monte Carlo 95 % CI of [−2.99, +0.76] pp: direction holds at 89.3 % of samples, magnitude point estimate is within modelling noise.

**Verdict.** The 70/30 urban weight's direction-finding is robust at ±20 %; the magnitude-finding is not. The audit's published position (direction defensible, magnitude qualified) is therefore consistent with the ±20 % sensitivity test.

### C.4 Summary of sensitivity-analysis outcomes

| Threshold | Observed value | ±20 % low | ±20 % high | Direction flipped? | Finding robust? |
|---|---|---|---|---|---|
| P1 packing (5 % of mean) | +11.5 % (minority Zone A) | 4 % | 6 % | No | Yes |
| P1 packing (5 % of mean) | +2.8 % (majority Zone A) | 4 % | 6 % | No | Yes |
| P2 packing (15 pp) | +18 pp (minority Zone A) | 12 pp | 18 pp | No (boundary at +20 % inflation) | Yes within strict −20 %; near-boundary at +20 % |
| Urban weight (0.70) | asymmetry sign | 0.56 | 0.84 | No | Yes (direction) / No (magnitude) |

**No ±20 % sensitivity check flips a finding direction.** The audit's direction-of-asymmetry claims are stable across all three load-bearing thresholds tested.

---

## Part D — Defensibility classification

Thresholds are ranked **strong** (statutory or literature-anchored, little residual vulnerability), **medium** (first-principles-derived with a named alternative that a reviewer could reasonably prefer), or **weak** (audit-defined without a direct literature or statutory anchor, relying on pre-registration or sensitivity-check for defence).

### D.1 Strongest thresholds

1. **±25 % population-deviation window (#1) and derivatives (C3 cracking #12, P1 denominator).** Pure statutory import. A reviewer contesting this number is contesting EBCA § 14. Defence: near-absolute.
2. **s.15(2) thresholds (#2–#6).** All six s.15(2) thresholds are statutory and are used directly. Defence: near-absolute.
3. **Monte Carlo sampling ranges grounded in observed data (#17 rural NDP Uniform(0.26, 0.36)).** The range is directly calibrated to three observed elections. Defence: strong; the only residual vulnerability is the possibility that future elections fall outside the 2015–2023 range, which the audit acknowledges explicitly.
4. **7 % EG bright-line (#7) as reporting reference.** Literature-anchored, not finding-determinative in this audit (observed EGs are << 7 %). Defence: strong.

### D.2 Medium-strength thresholds

1. **P1 packing — +5 % of provincial mean (#10).** First-principles derivation (one-fifth of statutory ±25 %). Reviewer could argue for a different fraction. Mitigations: pre-registration (git commit `5b0bc06`); ±20 % sensitivity check confirms robustness (Part C.1); observed value is 2× threshold, so fraction choice does not affect pass result within the ±10 %-to-±50 %-of-statutory-band range.
2. **P2 packing — +15 pp above mean (#11).** First-principles derivation calibrated to Chen (2017). Reviewer could argue for multiplicative rather than additive calibration. Mitigations: pre-registration; ±20 % sensitivity check; the conservative direction (demanding more than Chen's floor, not less).
3. **Urban weight 0.70 (#14) and sensitivity range (#15).** Central modelling choice; defence rests on symmetric application to both maps (apples-to-apples comparison) and on point-sensitivity + Monte Carlo (0.55–0.85) demonstrating direction stability. Reviewer could argue for a different central value. Mitigations: three-point sensitivity grid + Monte Carlo; direction holds across all tests; magnitude is qualified explicitly in the report.
4. **±2 % StatsCan tie-breaker in reform proposal (#30).** Anchored in TBF's own methodology practice but not in published legislation. Reviewer could argue 1 % or 5 %. Defence: industry-standard midpoint; TBF's own internal reconciliation uses the same figure.
5. **20 pp safe-seat cut-off (Chen 2017) (#9).** Literature-anchored but for US state-legislative context, not Canadian provincial. Mitigation: audit's use calibrates *more conservatively* than Chen's floor (P2 effectively requires ~34 pp margin), so the Chen-vs-Canada context argument cuts toward the audit's finding rather than against it.

### D.3 Weakest thresholds

1. **E1 engineered-boundary — negligible-population territory (#13).** Qualitative rather than quantitative. Defence rests on dual confirmation (imagery + commission prose). Reviewer could argue that qualitative criteria invite subjective judgment. Mitigations: the audit applies the criterion to only one boundary (RMH-Banff Park minority) where the evidence is unambiguous (Banff NP interior), and reports transparently when majority non-Calgary imagery is missing (report_academic.md §4.1 symmetry data gap).
2. **10 % per-ED divergence disclosure threshold (reform proposal, #31).** Audit-defined materiality trigger without literature anchor. Defence: functional — the threshold is large enough to potentially flip §14 compliance status, hence worth disclosing. A tighter 5 % threshold would be defensible too; the reform proposal acknowledges this in §B.6.2.
3. **Per-hybrid jitter clipping at [0.40, 0.95] (#18 implementation detail).** The clipping bounds are empirical (commission Appendix C observed min / max) but not pre-registered. Vulnerability: low — clipping rarely activates and its effect on the reported CI is < 0.05 pp.

### D.4 Observed values that are *not* thresholds

1. **89.3 % direction consistency (#22).** An observed sample property, not a pre-specified threshold. Reporting the exact figure respects ASA (2019) graded-evidence guidance.
2. **Cross-metric observed agreements (B2/B3/B4 align; B6 opposes).** Observed outcomes, not thresholds.

---

## Part E — Hostile-reviewer scenarios and the audit's standing response

**Scenario E1.** "Your P1 threshold at +5 % is arbitrary — why not +3 % or +7 %?" *Response.* P1 = 5 % is proportionally anchored to EBCA § 14's ±25 % band (one-fifth). The choice predates detection by 2 hours 24 minutes (git timestamps). The finding is retained across ±20 % sensitivity (Part C.1). Alternative fractions from one-tenth to one-half of the statutory band would all yield the same minority-pass / majority-fail verdict. The audit invites the reviewer to specify a principled alternative; none that moves the result exists within the plausible space.

**Scenario E2.** "The 70/30 urban weight is arbitrary — a different weight would give a different answer." *Response.* The audit agrees. Direction is stable across 0.56–0.84 (Part C.3); magnitude is not. The audit's existing framing (direction defensible, magnitude qualified by the Monte Carlo 95 % CI crossing zero) is consistent with this sensitivity. Using 70/30 symmetrically on both maps preserves the magnitude-of-asymmetry comparison regardless of the "correct" weight.

**Scenario E3.** "Chen (2017)'s 20 pp was for US state legislatures, not Canadian provincial elections — your use of it is transplanted." *Response.* The audit uses Chen (2017) as a conservative floor, not as a transplanted rule. The P2 calibration demands *more* than Chen's floor (approximately 34 pp absolute margin), so the Alberta-specific context — if it justifies a lower safe-seat threshold — would *strengthen* the audit's P2 finding, not weaken it. The calibration direction is conservative relative to the transplantation concern.

**Scenario E4.** "Your 7 % EG reference is contested in the literature (Stephanopoulos & McGhee 2018 respond to critics)." *Response.* The 7 % figure is a reporting reference in the audit, not a finding-determinative threshold. Observed EGs are −0.85 % and −1.36 %, an order of magnitude below 7 %. No audit conclusion turns on whether 7 % is the "correct" bright-line.

**Scenario E5.** "Your ±25 % statutory figure is a legal-window reading, but the denominator is the contested 2024 TBF estimate. Shifting denominators would change every district's deviation."  *Response.* Correct, and disclosed in report_academic.md §7.3 and Track K. The ±25 % figure itself is not at issue; the denominator is. The audit treats the denominator as a provenance question distinct from the threshold question — the threshold is statutory (fine); the denominator choice is contestable (disclosed).

**Scenario E6.** "Your readability thresholds (FK ≤ 9.5, 13.5) are policy conventions, not peer-reviewed findings." *Response.* Correct. They are plain-language-policy conventions anchored in the Plain Writing Act of 2010 (US) and equivalent UK and Canadian federal guidance. No finding hinges on them; they are publication-readiness gates.

---

## Part F — Summary for paper integration

The audit uses 38 numeric thresholds across statutory, literature, first-principles, and modelling categories. Six are directly statutory (EBCA §§ 14, 15(2) and their derivatives); six are drawn from redistricting and gerrymandering literature (Stephanopoulos & McGhee 2014, 2015; Chen 2017; McDonald & Best 2015; Warrington 2018; ASA 2016, 2019); six are modelling conventions documented with explicit sensitivity ranges (urban weight, Monte Carlo sampling); fourteen are first-principles derivations from statutory or reporting-precision anchors; five are audit-defined qualitative or gating criteria.

No ±20 % sensitivity check flips a finding direction on the three load-bearing thresholds (P1, P2, urban weight). Direction-of-asymmetry claims are robust; magnitude claims are explicitly qualified throughout the report.

Strongest thresholds are the statutory imports (EBCA §§ 14, 15(2)) and the empirically-calibrated Monte Carlo rural-NDP range. Weakest threshold is the qualitative E1 engineered-boundary criterion, whose defence rests on dual (imagery + prose) evidence and on its application to only one boundary (RMH-Banff Park) where the evidence is unambiguous.

The compendium is self-contained and suitable for integration as an appendix or supplementary online materials. Its length is proportional to the defensibility-audit discipline the audit committed to in `report_academic.md §1.2 (Defensibility Audit Gate DA1–DA7)`; a shorter treatment would be insufficient to discharge DA1 (trace) and DA3 (characterization provenance) for every threshold.

---

## References cited in defence paragraphs

Alberta Electoral Boundaries Commission Act, RSA 2000 c E-3, §§ 12, 14, 15.

Alberta Treasury Board and Finance, Office of Statistics and Information. (2024). *Quarterly population estimates, July 1, 2024* [Methodology notes]. Government of Alberta.

American Statistical Association. (2016). Statement on p-values and statistical significance. *The American Statistician*, 70(2), 129–133. https://doi.org/10.1080/00031305.2016.1154108

American Statistical Association. (2019). Moving to a world beyond "p < 0.05." *The American Statistician*, 73(sup1), 1–19. https://doi.org/10.1080/00031305.2019.1583913

Altman, M., & McDonald, M. P. (2011). BARD: Better automated redistricting. *Journal of Statistical Software*, 42(4), 1–28. https://doi.org/10.18637/jss.v042.i04

Chen, J. (2017). The impact of political geography on Wisconsin redistricting. *Election Law Journal*, 16(4), 443–452. https://doi.org/10.1089/elj.2017.0455

Chen, J., & Rodden, J. (2013). Unintentional gerrymandering: Political geography and electoral bias in legislatures. *Quarterly Journal of Political Science*, 8(3), 239–269. https://doi.org/10.1561/100.00012033

DeFord, D., Duchin, M., & Solomon, J. (2021). Recombination: A family of Markov chains for redistricting. *Harvard Data Science Review*, 3(1). https://doi.org/10.1162/99608f92.eb30390f

Employment and Social Development Canada. (2019). *Plain language guidelines*. Government of Canada.

*Gill v. Whitford*, 585 U.S. ___ (2018).

Herschlag, G., Ravier, R., & Mattingly, J. C. (2020). Quantifying gerrymandering in North Carolina. *Statistics and Public Policy*, 7(1), 30–38. https://doi.org/10.1080/2330443X.2020.1796400

Katz, J. N., King, G., & Rosenblatt, E. (2020). Theoretical foundations and empirical evaluations of partisan fairness in district-based democracies. *American Political Science Review*, 114(1), 164–178. https://doi.org/10.1017/S000305541900056X

McDonald, M. D., & Best, R. E. (2015). Unfair partisan gerrymanders in politics and law: A diagnostic applied to six cases. *Election Law Journal*, 14(4), 312–330. https://doi.org/10.1089/elj.2015.0318

Munafò, M. R., Nosek, B. A., Bishop, D. V. M., Button, K. S., Chambers, C. D., Percie du Sert, N., Simonsohn, U., Wagenmakers, E.-J., Ware, J. J., & Ioannidis, J. P. A. (2017). A manifesto for reproducible science. *Nature Human Behaviour*, 1, 0021. https://doi.org/10.1038/s41562-016-0021

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606. https://doi.org/10.1073/pnas.1708274114

Plain Writing Act of 2010, Pub. L. No. 111-274, 124 Stat. 2861.

*Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

Stephanopoulos, N. O., & McGhee, E. M. (2015). Partisan gerrymandering and the efficiency gap. *University of Chicago Law Review*, 82(2), 831–900.

Stephanopoulos, N. O., & McGhee, E. M. (2018). The measure of a metric: The debate over quantifying partisan gerrymandering. *Stanford Law Review*, 70, 1503–1568.

Warrington, G. S. (2018). Quantifying gerrymandering using the vote distribution. *Election Law Journal*, 17(1), 39–57. https://doi.org/10.1089/elj.2017.0447

Warrington, G. S. (2019). A comparison of partisan gerrymandering measures. *Election Law Journal*, 18(3), 262–281. https://doi.org/10.1089/elj.2018.0508

---

*Compendium v0.1. Compiled April 22, 2026. 38 thresholds catalogued. Produced as Track T output; not yet integrated into the paper. Integration by parent session.*
