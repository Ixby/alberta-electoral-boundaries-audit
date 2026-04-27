---
name: Pre-registration — Alberta Electoral Boundaries Audit signature-detection checklist for the November 2026 MLA-committee 91-seat map
description: Submission-ready pre-registration document for OSF Registrations (recommended platform; see analysis/reports/pre_registration_platform_analysis.md). Commits the audit to a fixed 17-signal checklist, with numeric thresholds and pass/fail criteria, to be scored on the Alberta MLA-committee 91-seat map within 72 hours of its release (target date 2026-11-02). Closes D17 (self-held pre-registration vulnerability) by placing the checklist under third-party custody with a verifiable timestamp.
forward_dependencies:
  - OSF Registration submission (PO-held; see Phase 3 instructions in analysis/reports/pre_registration_platform_analysis.md)
  - Track C re-audit of November committee map (executed against this pre-registered checklist)
  - report_academic.md §3.11 (baseline scorecard; the November column is the outcome of this pre-registration)
backward_dependencies:
  - analysis/reports/track_c_checklist_baseline_scoring.md (test list, numeric thresholds, baseline scoring for majority and minority 2026 maps)
  - report_public.md §"What a gerrymander in the 91-seat map would actually look like" (plain-language checklist)
  - report_academic.md §3.7–3.10 (signature-detection methodology)
  - analysis/v0_1_red_team_round_2.md §D17 (vulnerability this closes)
  - analysis/reports/chair_recommendation_5_analysis.md (R5 conditions included as X1)
---

# Pre-registration — Alberta Electoral Boundaries Audit signature-detection checklist (November 2026 MLA-committee 91-seat map)

## 1. Foreknowledge of data or evidence

**Selected category.** *Analyses in this plan have been conducted already.* At least some of the analyses described in this plan have been conducted by the authors, making this a retrospective registration.

**Explanation.**

This registration is mixed: retrospective for RQ1–7, prospective for RQ8–9.

*RQ1–7 (retrospective).* The commission maps under analysis — the majority 2026 proposal, the minority 2026 proposal, and the 2019 enacted boundaries — exist and have been fully analysed by the author prior to this submission. Population tables, four partisan-bias metrics, the submission-archive keyword search across 1,252 of approximately 1,340 submissions, and the close reading of the chair's Addendum Recommendation 5 were all conducted before registration. These questions are registered retrospectively to document the criteria and thresholds used, create a public record of the findings, and establish the baseline scorecard against which the November committee map will be scored.

Three specific actions were taken to reduce the risk of unintended influences on analysis decisions:

1. **Symmetric application.** Every test applied to the minority map was applied identically to the majority map and the 2019 baseline. Results that contradicted the author's stated prior — that the minority map warranted scrutiny — are retained in full and disclosed prominently. Three findings ran against the prior: (a) the majority's Canmore-Banff district qualifies cleanly under corrected statutory thresholds; (b) the minority's partisan-direction signal reverses under 2019 vote inputs; (c) the commission chair's "no public support" claim is upheld on three of the five configurations he named, not all five. All three are reported without qualification in the academic report and the public article.

2. **Pre-specified numeric thresholds.** The detection criteria for packing (≥10% Calgary zone gap), cracking (≥4 Airdrie divisions), and the ensemble outlier test (top-5% percentile) were specified in the same analytical-pass commit as the detection run. An earlier claim of intra-session separation between specification and detection was investigated, found to be inaccurate, and retracted in the academic report (§5.3.1 pre-registration disclosure). The honest framing — criteria were set at the head of the session that produced the results, not from a prior independent pass — is stated explicitly.

3. **Sensitivity and cross-election testing.** The partisan-bias direction was tested against three elections (2015, 2019, 2023) and one polling snapshot (338Canada April 2026). The direction reversal under 2019 vote inputs is reported as a property of the finding rather than suppressed. Monte Carlo confidence intervals (N=2,000, 95% CI crossing zero) are reported alongside the directional claim.

*RQ8–9 (prospective).* The Alberta MLA Special Select Committee's 91-seat map does not yet exist. No boundary proposals have been published; the advisory panel's membership and terms of reference were not public as of the registration date. The thresholds in RQ8 and RQ9 — the 10% Calgary zone gap, the four-division Airdrie threshold, the four R5 conditions — were derived from the retrospective analysis of the commission maps before the committee map exists, and are held by this registration as the criteria the audit commits to applying when the November map is released without modification.

---

## 2. Title and metadata

**Title.** Pre-registered signature-detection checklist for the Alberta MLA Special Select Committee's 91-seat electoral boundary map.

**Author.** Will Conner.

**Affiliation.** Independent civic audit. Not affiliated with the Government of Alberta, the Alberta Electoral Boundaries Commission, the MLA Special Select Committee, or any political party.

**Corresponding audit.** *Alberta Redistricting Audit* (2026). Academic report (`report_academic.md`) and public report (`report_public.md`). Repository time-stamped via public git history.

**Pre-registration date.** 2026-04-22 (document draft); submission date to OSF held by the author (see submission instructions).

**Target map.** The 91-seat electoral division map to be tabled by the Alberta MLA Special Select Committee chaired by Brandon Lunty (MLA, Leduc-Beaumont). The committee was established by Alberta Legislative Assembly Motion 19, passed 44-36 on 2026-04-16, with a reporting deadline of 2026-11-02.

**Scope.** This pre-registration binds the audit to a fixed set of 17 tests (S1–S6 strong signals, W1–W3 weak signals, P1–P5 process signals, X1–X3 supplementary gates) with numeric thresholds where applicable and pass/fail criteria for each. It commits the audit to score the committee's map on these tests within 72 hours of map release, without post-hoc revision of criteria.

**Not scoped.** This pre-registration does not commit the audit to a specific rhetorical framing, a specific headline claim, or a specific conclusion about whether the November map is or is not a gerrymander. It commits the audit to the test grid and the scoring rule; the narrative is determined by the scored results.

---

## 2. Study type, causal interpretation, and design

**Study type.** Other. The design spans three methods that do not fit a single OSF category: a forensic audit of existing administrative documents and data (observational/comparative), a simulation study (MCMC neutral ensemble of 100,000 alternative maps), and a pre-registered prospective test of a not-yet-existing map. The closest single category is "Non-randomized study" (observational, comparative), but that label omits the simulation component and the prospective pre-registration purpose.

**Causal interpretation.** Indirect inference on causal relationship(s). The study examines whether the minority map's structural features are consistent with deliberate partisan design, but is not designed to isolate intent as a measured causal variable. The inference is indirect: converging structural, statistical, and procedural signals are taken as evidence consistent with partisan motivation, but the study cannot rule out alternatives — geography, coincidence, individual commissioner preference — for any single finding. The MCMC ensemble narrows the geography-as-explanation alternative for the partisan-bias component; it does not eliminate it. The structural findings (population distribution, zone asymmetry, engineered boundary, community fragmentation) do not depend on vote data and are not subject to the natural-packing alternative; they constitute the primary evidence.

**Blinding.** Not applicable (no experiment). The analogue procedures are symmetric test application and pre-specified thresholds; these are documented under risk-of-influence mitigations below and in §1.

**Study design.**

This is a comparative forensic audit of three electoral boundary maps: the 2019 enacted Alberta boundaries (87 seats), the 2026 majority commission proposal (89 seats), and the 2026 minority commission proposal (89 seats). The design has three components applied to all three maps using identical methodology.

*Component 1 — Structural audit (observational, within-subject repeated measures).* Seven tests are applied symmetrically to all three maps: population distribution variance (A1), Calgary geographic-zone asymmetry (A2), s.15(2) remote-district eligibility (A3), and four gerrymander-signature tests (packing, cracking, engineered boundary, rationale validity). Each test is applied to all three maps; each map is a condition, not a subject. The comparison of interest is the minority-vs-majority difference on each test, with the 2019 enacted baseline as a reference for pre-existing structure.

*Component 2 — Partisan-bias metrics (observational, within-subject repeated measures).* Four partisan-bias metrics — efficiency gap, mean-median gap, seats-at-tied-vote under uniform swing, and declination — are computed on all three maps using 2023 provincial election vote totals reallocated to each map's district configuration via explicit crosswalk dictionaries. The same blending weights and reallocation methodology are applied to both 2026 maps. Sensitivity is tested across five urban-weight parameters (0.60, 0.70, 0.80, 0.85, 0.90) and three election cycles (2015, 2019, 2023) plus an April 2026 polling snapshot, yielding a 4-metric × 4-input matrix for each map.

*Component 3 — Simulation (MCMC neutral ensemble).* A Markov Chain Monte Carlo ensemble of 100,000 randomly drawn, legally valid Alberta boundary plans (GerryChain ReCom, ±25% population window, contiguity constraint, seed 42) provides a reference distribution. Each real map's partisan-bias metrics are expressed as percentile ranks within this distribution. This component tests whether each map's values are unusual relative to what neutral redistricting would produce given Alberta's actual geography, addressing the natural-packing alternative explanation.

*Prospective component (RQ8–9).* The November 2026 MLA Special Select Committee map, when released, will be scored against the same 17-test grid (§4 of this registration) using the same scripts and thresholds. No new tests or threshold adjustments will be introduced at that time.

*Risk-of-influence mitigations.* (1) Symmetric application: all tests are applied to all three maps; results that favour either map are retained. (2) Pre-specified thresholds: numeric criteria (10% zone gap, 4-way split, 7% EG, p95 ensemble rank) were set before the November map exists. (3) Cross-election and sensitivity testing: direction claims are qualified by the election cycle under which they hold and the parameter range over which they are stable. (4) Disclosed contradicting findings: three findings that ran against the author's prior are reported prominently in both the retrospective results and this pre-registration.

---

## 5. Sampling and data collection

This study uses no human subjects and no primary data collection in the conventional sense. All data are existing public administrative records or derived from them. The sampling strategy and data sources are described by dataset below.

**Electoral division population tables.** Source: the Alberta Electoral Boundaries Commission Final Report (March 23, 2026), variance tables for both proposals; the 2017 EBC Final Report, population tables for the 2019 enacted boundaries. Full census of all electoral divisions in each map — 87 EDs (2019), 89 EDs (majority 2026), 89 EDs (minority 2026). No sampling; all proposed districts are included. Files: `data/alberta_2019_populations.csv`, `data/majority_2026_populations.csv`, `data/minority_2026_populations.csv`, `data/minority_2026_populations_appendixE.csv`.

**Provincial election vote totals.** Source: Elections Alberta Statements of Vote for 2015, 2019, and 2023 general elections. Full census of all polling stations in each election — 1,973 poll records for 2023 (87 ridings). No sampling; all polls included. Files: `data/2023_results.xlsx`, `data/2019_results.xlsx`, `data/alberta_2015_results.csv` (parsed from 2015 Statement of Vote). Reallocated to 2026 proposed ED configurations via explicit crosswalk dictionaries (`data/majority_hybrid_crosswalk.csv`, `data/minority_hybrid_crosswalk.csv`).

**Boundary shapefiles.** Source: Elections Alberta GIS page. 2019 enacted ED polygons (87 polygons, EPSG:3401, `data/alberta_2019_eds/`); 2023 Voting Area polygons (4,765 polygons, EPSG:3400, `data/alberta_2023_vas/`). 2026 ED polygons have not been released by Elections Alberta as of the registration date; a formal written request for those files has been filed and is awaiting response. Synthetic 2026 boundaries were constructed from the commission's Appendix E boundary descriptions and refined over three passes to ±1 km positional accuracy for Tier A/B districts; Tier C hybrid boundaries remain unresolvable at shapefile-grade precision. Files: `analysis/reports/approximate_shape_analysis.md`, `analysis/methodology/shape_refinement_v2.md`, `data/boundary_refinement_impact_v3.csv`.

**2021 Census dissemination area populations and geometry.** Source: Statistics Canada, `lda_000a21a_e.zip` (national DA shapefile, filtered to Alberta, PRUID=48). 6,203 Alberta DAs, EPSG:3347. Used for population weighting in hybrid-district vote attribution and urban/rural classification robustness checks. File: `data/alberta_2021_das.gpkg`.

**Public submission archive.** Source: Alberta Electoral Boundaries Commission submission archive, accessed via the commission's public portal. Approximately 1,340 written submissions received across two rounds of public consultation. Of these, 1,252 were machine-parseable (had extractable text layers in their PDFs); 88 were image-only scans. The parseable submissions were keyword-searched using regex patterns against district names and configuration keywords. No sampling; all 1,252 parseable submissions were searched. The 88 image-only submissions represent a 6.6% coverage gap. File: `data/submission_search_dataset.csv`; methodology: `analysis/scripts/submission_search.py`; findings: `analysis/reports/submission_search_findings.md`.

**Commission report primary text.** Source: AEBC Final Report (March 23, 2026), 362 pages, including Appendix C (chair's majority rationale), Appendix E (minority rationale and boundary descriptions), and the chair's Addendum Recommendation 5 (pp. 66–67). Acquired as `commission_report.pdf` (80 MB, gitignored in `.temp/`); tables and text extracted via pdfplumber. Full document; no sampling.

**338Canada riding-level projections.** Source: 338Canada Alberta landing page, April 2026 snapshot. Per-riding projections scraped via `analysis/scripts/338canada_scraper.py` and reallocated to 2026 proposed ED configurations via `analysis/scripts/338canada_reallocate.py`. 87 current ridings; April 2026 snapshot. A 77-snapshot historical stability probe covers 2020-02-23 through 2026-04-12.

**Prospective data (RQ8–9).** The November 2026 MLA Special Select Committee 91-seat map does not yet exist. When the committee releases its map (target date 2026-11-02), the audit will acquire the map's boundary descriptions from the committee's official published materials and, if available, Elections Alberta's official shapefile release. No data will be collected or analysed before the map is publicly released. The 72-hour scoring window begins at first public release.

**Inclusion and exclusion criteria.** All electoral divisions in each of the three maps are included in the population-equality and structural analyses — no exclusions. For partisan-bias metrics, electoral divisions with no contested UCP/NDP race in 2023 (one riding: Fort McMurray-Lac La Biche, where the NDP did not field a candidate) are excluded from the two-party efficiency gap and mean-median computations; this exclusion is documented in `analysis/scripts/packing_cracking_analysis.py`. The MCMC ensemble uses all 4,765 Voting Area polygons in the 2023 VA shapefile as the substrate; no VAs are excluded.

---

## 7. Sample size, rationale, and stopping rules

**Sample size by unit of analysis.**

| Unit of analysis | N | Notes |
|---|---|---|
| Electoral divisions — 2019 enacted | 87 | Full census; fixed by law |
| Electoral divisions — majority 2026 | 89 | Full census; fixed by commission report |
| Electoral divisions — minority 2026 | 89 | Full census; fixed by commission report |
| Electoral divisions — November 2026 committee map | 91 | Full census; fixed by Motion 19 |
| Voting Areas (MCMC substrate) | 4,765 | Full census; fixed by Elections Alberta 2023 VA release |
| Polling records — 2023 election | 1,973 | Full census across 87 ridings |
| Polling records — 2019 election | ~1,940 | Full census (approximate; exact count in raw file) |
| Polling records — 2015 election | ~1,800 | Full census (approximate; pre-2017 boundaries) |
| Public submissions — machine-parseable | 1,252 | 93.4% of total; 88 image-only excluded |
| MCMC ensemble plans | 100,000 | See rationale below |
| 338Canada historical snapshots | 77 | 2020-02-23 through 2026-04-12 |

Sample sizes are not a design choice for the observational components — they are the complete populations defined by law (seat counts), by Elections Alberta releases (VA polygons, poll records), and by the commission's submission archive. There are no conditions, treatments, or clusters in the conventional sense; each "condition" is one of the three (or four) maps, and all units within each map are included.

**Sample size rationale.**

For the observational components, the sample is the full population — no power calculation is relevant. Every electoral division, every poll record, and every parseable submission is included.

For the MCMC ensemble, 100,000 plans were drawn because: (a) preliminary convergence diagnostics on a 10,000-plan run showed running-mean traces stabilising within the first 30–40% of samples; (b) the 100,000-plan run yields effective sample sizes of approximately 148–160 per metric (integrated autocorrelation time τ ≈ 625–675), which is sufficient for policy-comparison percentile claims at the p95 threshold used in this registration but below the ~5,000 ESS considered lawsuit-grade by MGGG practice; (c) the 100,000-plan run was achievable in approximately 12 minutes on a laptop and was the largest run feasible within the session budget. The pre-registered threshold (top-5% UCP-favourability) is conservative relative to the chain's ESS: the p95 boundary can be estimated reliably at n_eff ≈ 150. A 1,000,000-plan run with thinning to ~5,000 effective draws is identified as future work to achieve peer-review-grade precision.

**Starting and stopping rules.**

This study generates no new primary data. All existing data were acquired prior to registration (see §5). There is no pilot-testing phase and no ongoing collection to terminate for the retrospective components.

For the prospective component (RQ8–9), data collection begins when the November 2026 committee map is publicly released (target date 2026-11-02) and ends when the audit has acquired sufficient boundary information to score all non-blocked tests in §9 (the 17-test pre-registered grid). The 72-hour scoring window beginning at first public release is the de facto stopping rule: all tests that can be scored within 72 hours of map release will be scored; tests requiring shapefiles not released within that window are recorded as BLOCKED and revisited when shapefiles become available. No additional data collection will occur after the 72-hour scorecard is published, except to update BLOCKED tests when blocking conditions resolve.

---

## 9. Manipulated variables

None. This is an observational study. No variables are manipulated by the researchers. The three maps (2019 enacted, majority 2026, minority 2026) and the prospective November 2026 committee map are existing or anticipated administrative outputs, not experimental treatments assigned by the researchers.

The urban-weight parameter used in hybrid-district vote attribution (tested at 0.60, 0.70, 0.80, 0.85, and 0.90) is a modelling sensitivity parameter, not a manipulation — it represents uncertainty about the composition of hybrid districts and is varied to characterise how the efficiency-gap finding changes across plausible assumptions, not to test a causal effect of the parameter itself.

---

## 10. Measured variables

**Primary structural variables (computed per electoral division, per map):**

- *Population* — resident population assigned to each electoral division, sourced from the commission's per-ED variance tables (2024 OSI estimate base). Unit: persons. Range: approximately 35,000–90,000 for Alberta EDs.
- *Variance from provincial quota* — per-ED deviation from the provincial population quota expressed as a percentage: (ED population − quota) / quota × 100. Quota derived as total provincial population ÷ number of EDs.
- *Zone classification (Calgary)* — binary indicator: Zone A (NDP-leaning, northern/eastern/central Calgary) or Zone B (UCP-leaning, southern/western Calgary), assigned by two classification rules (geographic partition and 2023 election result). Used to compute the Calgary zone gap.
- *Hybrid flag* — binary indicator: whether an electoral division joins a city neighbourhood with a rural or exurban community across the municipal boundary. Sourced from the commission's crosswalk tables and the minority's Appendix E boundary descriptions.
- *s.15(2) invocation* — binary indicator: whether an ED is designated as a remote/sparse district under Electoral Divisions Act s.15(2), exempt from the standard ±25% population window.

**Partisan-bias input variables (computed per electoral division, per map × election cycle):**

- *NDP votes* — total votes cast for the NDP candidate in the electoral division. Sourced from Elections Alberta Statements of Vote (2015, 2019, 2023) reallocated to 2026 proposed ED configurations via crosswalk dictionaries.
- *UCP votes* — total votes cast for the UCP candidate (or PC + WRP combined for 2015).
- *Total valid votes* — NDP + UCP + all other candidates' votes.
- *NDP two-party vote share* — NDP votes ÷ (NDP votes + UCP votes), expressed as a proportion. Range: 0–1.
- *Winner* — binary indicator: NDP or UCP won the ED under the given vote-to-ED reallocation.
- *Winning margin* — winning party's two-party share minus 0.5, expressed in percentage points. Positive = NDP-favourable; negative = UCP-favourable under the audit's sign convention.
- *Wasted votes (NDP)* — votes cast for the NDP that did not contribute to electing the NDP candidate: all NDP votes in EDs the NDP lost, plus NDP votes above the 50%+1 threshold in EDs the NDP won.
- *Wasted votes (UCP)* — analogous for UCP.

**Process and documentary variables (binary or categorical, per configuration or per map):**

- *Public support classification* — for each of seven minority-proposed configurations: the count of submissions supporting, opposing, or neutral toward the configuration; the net support score; and the support rate (supporting ÷ total engaged submissions). Sourced from the submission keyword-search dataset (`data/submission_search_dataset.csv`).
- *Rationale validity* — for each of the minority's 25 inventoried justifications: pass / fail / partial against the verification dataset (census populations, journey-to-work tables, school-division boundaries). Binary per rationale; summarised as a count of contradictions per configuration.
- *R5 condition satisfaction* — for the November committee map: binary pass/fail for each of four conditions specified in the chair's Addendum Recommendation 5.
- *Process signal indicators (P1–P5)* — binary pass/fail for each of five procedural signals (public hearings held, advisory panel named, draft released, adoption vote character, AI disclosure), scored for the November committee map.

**MCMC ensemble variables (computed per simulated plan):**

- *Efficiency gap* — per plan; used to construct the reference distribution for percentile ranking.
- *Mean-median gap* — per plan.
- *Seats at 50/50 vote share* — per plan.
- *Declination* — per plan.

---

## 11. Indices and derived variables

All index formulas are implemented in `analysis/scripts/packing_cracking_analysis.py` and `analysis/scripts/electoral_forensics_population.py`. Definitions follow the cited sources exactly; deviations are noted.

**A1 — Mean absolute deviation (MAD).**
MAD = (1/n) × Σ |population_i − quota|, where quota = Σ population_i / n, summed over all n EDs in the map. Reported in persons and as a percentage of quota.

**A2 — Calgary geographic-zone gap.**
Zone gap = (mean population of Zone A EDs − mean population of Zone B EDs) / mean population of Zone B EDs × 100, expressed as a percentage. Zone A = NDP-leaning Calgary EDs; Zone B = UCP-leaning Calgary EDs. Two classification rules tested: (i) geographic partition (north/east/central vs south/west); (ii) 2023 election winner. Both rules are reported; the conservative (lower) estimate is used as the headline. The gap is directional: positive values indicate Zone A is larger, which under the packing mechanism means NDP-leaning districts are over-populated relative to UCP-leaning ones.

**B2 — Efficiency gap (EG).**
EG = (wasted_votes_NDP − wasted_votes_UCP) / total_valid_votes. Sign convention: negative EG = UCP-favoured (more NDP votes wasted than UCP votes). Wasted votes for the losing party = all votes cast for that party in EDs it lost. Wasted votes for the winning party = votes cast above the 50%+1 threshold. Following Stephanopoulos & McGhee (2015). For hybrid EDs, vote totals are estimated by blending the urban-core and rural-absorption portions at the specified urban weight (central estimate 0.85; sensitivity range 0.60–0.90).

**B3 — Mean-median gap (MM).**
MM = mean(NDP two-party share across all EDs) − median(NDP two-party share across all EDs), expressed in percentage points. Negative MM = NDP vote share is more skewed toward the right tail than the median district (UCP-favoured). Following McDonald & Best (2015).

**B4 — Seats at 50/50 uniform swing.**
A uniform swing S is applied to every ED's NDP two-party share: adjusted_share_i = NDP_share_i + S, where S is chosen so that Σ adjusted_share_i / n = 0.50. Each ED is counted as NDP-won if adjusted_share_i > 0.50. The resulting NDP seat count is the B4 output. Following Gelman & King (1994).

**B6 — Declination.**
Declination δ is the angle between the best-fit line through UCP-winning EDs (x = UCP two-party share, y = ED rank normalised 0–1) and the best-fit line through NDP-winning EDs, expressed in radians. δ = 0 indicates symmetric distribution of winning margins; negative δ (under the audit's sign convention) indicates UCP-winning margins are more spread / NDP-winning margins are more compressed. Following Warrington (2018). The sign convention used here is documented in `analysis/methodology/sign_convention_resolution.md`.

**MCMC ensemble percentile.**
For each of the four metrics (B2, B3, B4, B6), each real map's value is ranked against the 100,000-plan distribution: percentile = (number of ensemble plans with a more UCP-favourable value than the real map) / 100,000 × 100. A percentile of 95 means the real map is more UCP-favourable than 95% of neutral alternatives on that metric.

**Packing test composite (P1–P3).**
Three sub-criteria are evaluated for each Calgary zone-gap flagging: P1 (Zone A mean population exceeds provincial mean by ≥5%), P2 (Zone A NDP win rate exceeds 60%), P3 (counterfactual seat loss: NDP would gain ≥1 additional seat under equal-population zoning). All three must pass for a formal packing signature to be recorded. Individual P-criterion outcomes are reported alongside the composite.

**Scorecard signal tally.**
The pre-registered scorecard (§9 of this registration) aggregates the 17 individual test outcomes (PASS, FAIL, BLOCKED, PENDING, UNDETERMINED) into: count of strong signals triggered (S1–S6), count of weak signals triggered (W1–W3), count of process signals triggered (P1–P5), and supplementary gate outcomes (X1–X3). No arithmetic weighting is applied — each test's outcome is binary and reported individually. The narrative follows the scorecard; no index score is computed that would collapse the 17 tests into a single "gerrymander score."

---

## 13. Analysis plan

### 13.1 Statistical models

This study does not use inferential statistical models in the traditional sense (regression, ANOVA, SEM). The analyses are forensic comparisons — each map's computed metric is compared against the other maps' values and, where applicable, against a reference distribution. The analytical methods are described below by component.

**Component 1 — Structural comparisons (descriptive, non-parametric).**
No statistical model. Each structural variable (MAD, zone gap, Airdrie split count, s.15(2) boundary configuration) is computed for each map and compared directly. The comparison is a deterministic pass/fail against pre-specified thresholds (§9). No p-values or confidence intervals are computed for structural variables; the thresholds are population-level criteria derived from the Electoral Divisions Act and the commission's own variance tables, not sample statistics.

**Component 2 — Partisan-bias metrics (descriptive with sensitivity analysis).**
No regression model. Each of the four metrics (EG, MM, B4, B6) is computed as a point estimate for each map × election cycle combination. Sensitivity analysis: the EG is re-computed at urban weights 0.60, 0.70, 0.80, 0.85 (central estimate), and 0.90 to produce a range rather than a single point estimate. Cross-election stability: the EG and MM are recomputed substituting 2019 and 2015 vote totals for 2023 to test directional stability. Monte Carlo confidence interval: 2,000 samples varying urban weight (uniform 0.55–0.85), rural baseline vote share (uniform 0.26–0.36), and per-hybrid jitter (±0.10 uniform) are drawn to produce an empirical 95% CI on the minority-majority EG asymmetry. Direction consistency across Monte Carlo samples is reported as a proportion (the percentage of samples in which the minority map is more UCP-favourable than the majority).

**Component 3 — MCMC ensemble percentile (simulation-based reference distribution).**
No parametric model. Each real map's metric values are ranked against the 100,000-plan ReCom ensemble. The test statistic is the percentile rank; the threshold is p95 (top 5% of UCP-favourable plans). Convergence diagnostics: running-mean traces and integrated autocorrelation time are computed per metric to confirm the chain has stabilised. The effective sample size (n_eff ≈ 148–160) is reported as a precision caveat alongside all percentile claims.

**Component 4 — Submission-archive verification (frequency counts, qualitative classification).**
No statistical model. For each of the seven configurations, the count of supporting, opposing, and neutral submissions is reported. The support rate (supporting / total engaged) is a descriptive proportion. No significance test is applied to submission counts; the test is whether the count of supporting submissions is greater than zero (a binary factual question about the chair's "no public support" claim), not whether the support rate differs significantly from any null.

**Component 5 — Prospective scoring of November map (pre-registered threshold tests).**
Each of the 17 tests in §9 is applied to the November map and recorded as PASS, FAIL, BLOCKED, PENDING, or UNDETERMINED. No statistical model. The outcome of each test follows deterministically from the map's values and the pre-registered thresholds.

**Positive and negative controls.** The 2019 enacted map serves as the negative control for the structural and partisan-bias analyses: it is the known pre-existing baseline, expected to sit near the centre of the neutral ensemble and to show no minority-specific signatures. The majority map serves as a positive control for the packing test: it should show near-zero Calgary zone gap (observed: 0.36%), confirming the test distinguishes the two 2026 maps rather than flagging a province-wide artefact.

### 13.2 Transformations

No transformations, centering, or recoding are applied to the population or vote-count data. Variables are used in their natural units (persons, vote counts, proportions).

The NDP two-party vote share is a ratio variable computed from raw vote counts; it is not log-transformed or otherwise rescaled. The efficiency gap is computed as a signed proportion (range −1 to +1 in theory; in practice within ±0.10 for Alberta). The mean-median gap is computed in percentage-point units. Declination is computed in radians and reported as-is.

Categorical variable coding: zone classification (Zone A / Zone B) is a binary indicator coded 0/1 for arithmetic purposes (mean population by zone). Winner (NDP / UCP) is a binary indicator coded NDP=1, UCP=0 for seat-count summation. The hybrid flag is binary (1 = hybrid). The s.15(2) flag is binary (1 = remote-district invocation). Process signal outcomes are coded as five-level categorical: PASS / FAIL / BLOCKED / PENDING / UNDETERMINED.

### 13.3 Inference criteria

**Structural tests (RQ1–3, S1–S3).** Binary pass/fail against pre-specified thresholds: 10% Calgary zone gap (strong signal), 4 or more Airdrie divisions (cracking), presence of an uninhabited-area boundary extension with no additional represented community (engineered boundary). No p-values. The thresholds are operationalisations of legal and geometric criteria, not statistical significance cutoffs.

**Partisan-bias direction (RQ4).** A directional claim is supported if: (a) three or more of the four metrics show the minority map as more UCP-favourable than the majority map under 2023 vote input; and (b) the Monte Carlo direction consistency proportion exceeds 85% (observed: 90.5%). Classical 95% significance is not asserted — the Monte Carlo 95% CI crosses zero — and this is disclosed explicitly. The finding is characterised as a directional observation at approximately 90% confidence, not a statistically significant result.

**Ensemble percentile (RQ5, S5).** The threshold is p95 (top 5% UCP-favourable tail of the 100,000-plan neutral ensemble). One-tailed test (UCP-favourable direction only, given the directional hypothesis). The effective sample size caveat (n_eff ≈ 150) is reported alongside any percentile claim.

**Submission-archive factual test (RQ6).** The criterion is binary: does at least one parseable submission explicitly support the configuration? No significance threshold. A single identified supporting submission is sufficient to refute a "no public support" characterisation for that configuration.

**Addendum documentary test (RQ7).** Textual: the criterion is whether the addendum's own language contradicts the government's stated reading. The test is pass/fail against three specific textual facts: the presence of the sentence "My majority colleagues do not agree with me on this point"; the four conditional clauses; the stated purpose of dissuading adoption of the minority map.

**Multiple comparisons.** Seventeen tests are applied to each map. No multiple-comparisons correction (e.g., Bonferroni) is applied, for two reasons documented in the academic report (§5.2): (a) the tests are not independent — they measure related aspects of the same maps, so a Bonferroni correction would be overly conservative; (b) the study's inference goal is not to control family-wise error rate across a null-hypothesis significance testing framework but to characterise a pattern across six independent analytical dimensions, following the consistency-across-N methodology of Katz, King, and Rosenblatt (2020). All 17 test outcomes are reported, including PASSes, so readers can assess the overall pattern without selective reporting.

### 13.4 Data inclusion and exclusion

All electoral divisions in each map are included. No outlier exclusion is applied to population or vote data.

The one exclusion: Fort McMurray-Lac La Biche (2023) is excluded from two-party vote share computations because the NDP did not field a candidate in that riding, making a two-party NDP/UCP share undefined. This riding is included in population-equality computations and retained in the MCMC ensemble substrate with its actual vote totals.

For the submission archive: the 88 image-only submissions (6.6% of total) are excluded from keyword search because they lack machine-readable text. They are not excluded from the denominator when reporting coverage (the audit reports "1,252 of approximately 1,340" rather than treating the parseable set as the full population). No submissions within the parseable set are excluded on content grounds.

For the MCMC ensemble: all 4,765 Voting Area polygons are included as substrate. No VAs are excluded. The 38 boundary-adjacent VAs (0.80%) whose centroids fall outside their declared 2019 parent ED are assigned to their declared ED (from the poll record) rather than their geometric centroid ED; this is documented as a canonical assignment rule, not an exclusion.

### 13.5 Missing data

This study has no missing data in the conventional sense — the datasets are administrative records with complete population-level coverage for all EDs and polls that existed in each election.

Three structured gaps exist and are handled as follows:

1. **2026 official shapefiles (not released).** Analyses that require precise 2026 polygon geometry — Polsby-Popper and Reock compactness for Tier C EDs, the MCMC ensemble seeded from 2026 geometry — are recorded as BLOCKED rather than imputed. Synthetic Tier A/B geometries are used where positional accuracy is within ±1 km; Tier C hybrid EDs are not imputed. When official shapefiles are released, BLOCKED tests will be re-run and results updated.

2. **88 image-only submissions.** Not imputed. The submission-archive finding rests on identified positive counter-examples in the parseable set; the 88 excluded submissions could only affect counts, not the binary refutation verdict. Their exclusion is disclosed and the coverage rate is reported.

3. **November 2026 committee map (does not yet exist).** RQ8–9 outcomes are recorded as PENDING until the map is released. No imputation or forecasting of the November map's content is performed prior to its release.

### 13.6 Other planned analyses

**Cross-election stability probe.** The EG and MM are computed substituting 2019 and 2015 vote totals for 2023 (with appropriate crosswalk reallocation). This is a planned analysis documented in `analysis/scripts/monte_carlo_ci.py` and `analysis/reports/2015_cross_election_analysis.md`. Results are reported alongside the 2023-baseline findings; the directional reversal under 2019 is a registered finding, not a post-hoc anomaly.

**338Canada per-riding cross-validation.** The minority-majority seat gap is recomputed using 338Canada April 2026 per-riding projections reallocated through the audit's crosswalk dictionaries. This is test X3 in §9 and is a planned analysis documented in `analysis/scripts/338canada_reallocate.py`.

**Symmetry-of-test-selection audit.** Every test applied to detect a minority-specific pattern is applied to the majority map asking the same question. Results are reported in §5.6 of the academic report. This is a planned analysis, not a post-hoc robustness check.

**Natural-packing (Chen-Rodden) validation.** A test of whether the Chen-Rodden (2013) urban-packing mechanism operates in Alberta, using wasted-vote decomposition and Moran's I on NDP two-party share. Documented in `analysis/scripts/chen_rodden_alberta.py`. Results are used to frame the partisan-bias findings (whether the EG difference between the two 2026 maps reflects geography or design) and are a planned analysis registered here.

---

## 15. Context and additional information

**Author standing and institutional context.** This audit was conducted by Will Conner, a fourth-year undergraduate in Computer Information Systems at Mount Royal University, without institutional sponsorship, faculty co-authorship, or research funding. It is not a commissioned report for any government body, political party, or advocacy organization. The author has previously supported the Alberta New Democratic Party, which is disclosed in both the academic report and the public article. The methodology is designed to produce the same results regardless of that prior; three findings that contradicted the author's expectations are retained and prominently disclosed.

**Why this pre-registration is being submitted after analysis of RQ1–7.** The April 16, 2026 Alberta Legislative Assembly vote to set aside the commission's maps and establish a five-MLA drafting committee was announced publicly on that date. The audit's retrospective analysis of the two commission maps was substantially complete before that vote. The November 2026 committee map — the confirmatory test — could not have been pre-registered before the April 16 vote because the committee did not exist until that date. The practical window for pre-registration of the prospective component (RQ8–9) opened on April 16 and closes when the November map is released. This registration is filed within that window. The retrospective component (RQ1–7) cannot be made prospective retroactively; it is registered here to create a public record of the criteria and to establish that the thresholds used to evaluate the commission maps were fixed before the committee map was drawn, not derived from the committee map after the fact.

**Public interest framing.** Alberta's 2025–26 redistricting is a live policy dispute with direct consequences for three provincial election cycles (2027, 2031, 2035). The audit is published as a public-interest document, not as a partisan intervention. Its intended readership includes journalists, legal counsel assessing potential constitutional challenges under *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158, citizens filing submissions to the Lunty committee, and academic researchers working on Canadian redistricting and partisan-bias measurement. The public report targets a grade-9 reading level; the academic report targets a technical audience. Both are available at the project's public GitHub repository.

**Relationship to legal proceedings.** The audit is not prepared for use in any specific litigation and is not commissioned by any legal party. Its methods are designed to meet the evidentiary standards discussed in *Gill v. Whitford*, 585 U.S. ___ (2018) and in the Canadian constitutional framework, but the audit makes no claim to be litigation-ready without peer review and the improvements identified in the academic report (publication-grade MCMC, measured vote attribution via official shapefiles, multiple-comparisons correction).

**Known limitations not addressed elsewhere in this registration.** (1) The MCMC ensemble is seeded from 2019 boundaries rather than 2026 geometry, because the 2026 shapefiles have not been released. This makes the ensemble conservative — a 2026-seeded ensemble would likely place the minority map at a more extreme percentile, not a less extreme one. (2) The partisan-bias direction reverses under 2019 vote inputs. This is fully disclosed and is a registered finding (§13.3), not a post-hoc qualification. (3) The study does not attempt to infer intent. The convergence of structural signals across six independent dimensions is taken as evidence consistent with deliberate partisan design; the study does not rule out alternative explanations for any single dimension. The academic report's §7.2 lists explicit falsifiers for each primary claim.

**Timeline.** Retrospective analysis completed: 2026-04-22. This registration submitted: 2026-04-23. November committee map expected: 2026-11-02. Prospective scoring window: within 72 hours of map release. Updated results incorporating official shapefiles: when Elections Alberta responds to the formal shapefile request.

**Declared toolstack.** This audit was produced using the following tools: Python 3.11 (pandas, numpy, geopandas/pyogrio, shapely, pyproj, GerryChain 0.3.2, textstat, pdfplumber, rapidfuzz, osmnx); Elections Alberta GIS data; Statistics Canada DA shapefiles; pdfplumber for commission report extraction; and Claude (Anthropic), a large language model used as an analytical and writing assistant throughout the project. Claude's role included: drafting and revising report text, proposing analysis structure and section outlines, identifying consistency gaps between documents, and surfacing edge cases in the methodology (e.g., the Vote Anywhere apportionment issue and the pre-registration disclosure requirement). All substantive analytical claims — metric values, thresholds, data provenance, and code outputs — were verified against primary sources and script outputs by the author. Claude did not execute code or access external data independently; all script runs were performed by the author in a local Python environment. The use of an AI assistant is disclosed here and in both the public and academic reports in accordance with emerging norms for AI-assisted research.

---

## 16. Randomization

Not applicable to the observational and documentary components of this study (Components 1, 2, and the prospective RQ8–9 scoring).

The simulation component (Component 3, MCMC neutral ensemble) uses pseudo-random number generation to draw 100,000 alternative boundary plans. This is not randomization of subjects to treatments; it is stochastic sampling of the legal map space to construct a reference distribution. Parameters: GerryChain 0.3.2 ReCom proposal; random seed 42 (fixed and published); 4,765 Voting Area polygons as the substrate; ±25% population deviation constraint; queen-contiguity constraint. The seed is fixed so that the ensemble is exactly reproducible by any third party running the same script against the same input data. The ensemble run is documented at `analysis/methodology/mcmc_100k_and_full_coverage.md`; per-sample data at `data/simulated_ensemble_raw_samples_100k.csv`.

---

## 5. Research questions and hypotheses

Nine research questions are evaluated in this study. RQ1–3 are structural: they test map geometry and population tables and do not require vote data. RQ4–5 are partisan-bias questions: they use reallocated vote totals and are direction-stable under 2020s-era vote inputs but reverse under 2019. RQ6–7 are documentary: they test the commission's submission-archive characterization and the chair's addendum against the primary record. RQ8–9 are prospective and constitute the confirmatory pre-registered hypotheses; RQ1–7 are the retrospective baseline that establishes the detection criteria before the November map exists.

**RQ1.** Does the minority commission map's Calgary electoral division population distribution contain a systematic asymmetry between NDP-leaning and UCP-leaning districts — specifically, does the mean population of NDP-leaning districts exceed the mean population of UCP-leaning districts by a margin larger than observed under the majority commission map or the 2019 enacted boundaries?

*Implication: if the asymmetry exceeds 10% under the minority map and is below 1% under the majority and 2019 maps, a packing signature is detected in the minority map only.*

**RQ2.** Does the minority commission map fragment the City of Airdrie across a greater number of electoral divisions than population arithmetic requires, given the Act's ±25% population window — specifically, more than two divisions, which is the maximum the majority map uses?

*Implication: if Airdrie is split across four or more divisions under the minority map and two under the majority, a cracking signature is detected in the minority map only.*

**RQ3.** Does the minority commission map contain at least one electoral division boundary that formally satisfies the Electoral Divisions Act's s.15(2) remote-district provision but whose specific geographic configuration adds no additional represented community — that is, where an alternative boundary drawing, using the same population bands, would represent real communities the adopted boundary does not?

*Implication: if such a boundary is identified under the minority map and no equivalent boundary is found under the majority map, an engineered-boundary signature is detected in the minority map only.*

**RQ4.** Do four standard partisan-bias metrics — efficiency gap, mean-median gap, seats at a tied provincial vote under uniform swing, and declination — show directionally consistent UCP-favouring asymmetry for the minority map relative to the majority map, using 2023 provincial election vote totals reallocated to each proposed district configuration?

*Implication: if three or more of the four metrics show the minority map as more UCP-favouring than the majority map, and the direction holds across modelling-parameter sensitivity analysis, a directional partisan-bias finding is supported. If the direction is unstable across election cycles or parameter choices, the finding is qualified as cycle-contingent rather than structural.*

**RQ5.** Does the minority commission map's partisan-bias profile fall outside the distribution produced by a neutral Markov Chain Monte Carlo ensemble of 100,000 randomly drawn, legally valid Alberta electoral boundary plans — specifically, does it rank in the top 5% of UCP-favouring plans on any of the four metrics in RQ4?

*Implication: if the minority map falls in the top 5% on at least one metric and the majority map does not, the minority map is a distributional outlier relative to what neutral redistricting would produce.*

**RQ6.** Did the commission chair's Appendix C accurately characterize the public submission record when it stated that the five disputed minority configurations — Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert — had "no public support" in the consultation record?

*Implication: if keyword search of the parseable submission archive recovers at least one submission explicitly supporting any of the five configurations, the "no public support" characterization is factually incorrect for that configuration. The finding is graded by configuration: configurations with zero supporting submissions retain the chair's characterization; configurations with identified supporting submissions do not.*

**RQ7.** Does the commission chair's Addendum Recommendation 5 support the April 16, 2026 Alberta Legislative Assembly motion — specifically, does the addendum recommend that the Legislature adopt the minority map, or does it commit the use of its 91-seat number to conditions and purposes inconsistent with the motion as passed?

*Implication: if the addendum explicitly states that the majority commissioners did not agree with the recommendation, that the recommendation was conditional on the Legislature rejecting the majority map, and that its purpose was to dissuade adoption of the minority map, then the government's stated warrant for the motion is materially incomplete as a characterization of the addendum.*

**RQ8 (prospective — November 2026 committee map).** Will the Alberta MLA Special Select Committee's 91-seat electoral boundary map, tabled by November 2, 2026, preserve any of the three gerrymander signatures detected in the minority commission map — Calgary zone population asymmetry ≥10%, Airdrie fragmentation across ≥4 divisions, or an engineered s.15(2) boundary — and will it introduce additional signatures beyond the minority's set?

*Implication: if zero of the three signatures are preserved and no new signatures are introduced, the committee's map does not replicate the structural patterns flagged in the minority map. If one or more signatures are preserved or new ones introduced, the committee's map continues the structural pattern the audit identified in the rejected minority proposal.*

**RQ9 (prospective — November 2026 committee map).** Will the Alberta MLA Special Select Committee's 91-seat map satisfy all four conditions the commission chair specified in Addendum Recommendation 5 as prerequisites for the Legislature to act on that addendum — no impact on Airdrie or south of it except Drumheller-Stettler; no impact north of Edmonton's North Saskatchewan River; south-of-NSR Edmonton districts reverting to the interim-report configuration; and a Clearwater County / western Mountain View County s.15(2) seat restored?

*Implication: if all four conditions are met, the committee's map is consistent with the stated terms of the addendum the government cited as its warrant. If one or more conditions are not met, the committee used the addendum's seat number without adopting its operative constraints.*

---

## 3. Background

On 2026-04-16 the Alberta Legislative Assembly passed Motion 19 (44-36), setting aside the Alberta Electoral Boundaries Commission's 2026 majority report and establishing a Special Select Committee of five MLAs (three UCP, two NDP) chaired by Brandon Lunty to produce a 91-seat electoral boundary map by 2026-11-02. The motion was framed as partially aligned with the commission chair's Addendum Recommendation 5, which proposed, in the event the Legislature could not accept the majority's 89-seat boundaries, raising the seat count to 91 through an all-party Select Special Committee to restore two rural s.15(2) districts while maintaining the rest of the province as the majority proposed. The committee's mandate does not include public hearings on the draft map. Its advisory panel membership and terms of reference were unpublished as of 2026-04-22 (CBC Edmonton, 2026-04-16; Calgary Journal, 2026-04-21).

The *Alberta Redistricting Audit* (2026) has analysed the two 89-seat commission maps (majority and minority) using the same signature-detection methodology pre-registered below. It detected three formal gerrymander signatures under the minority map (Calgary Zone A packing, Airdrie four-way cracking, Rocky Mountain House-Banff Park engineered s.15(2) boundary) and zero under the majority. The full baseline scorecard is in `analysis/reports/track_c_checklist_baseline_scoring.md` (repository state as of this pre-registration's submission date). The November 91-seat map is a held-out test: the audit pre-registers here the criteria under which the committee's map will be scored on the same grid, before the map exists.

This pre-registration closes a vulnerability identified in round 2 of the audit's red-team analysis (D17, `analysis/v0_1_red_team_round_2.md`): "pre-registration as typically practised (OSF, AsPredicted) requires a third party to hold the pre-registered criteria; the audit's November checklist is self-held." Posting this document to OSF before the map lands places the checklist under third-party custody with a verifiable timestamp.

---

## 3. Pre-registered tests

All 17 tests below carry over from the calibrated checklist in `analysis/reports/track_c_checklist_baseline_scoring.md`. Each has a numeric threshold (where applicable) and a binary pass/fail criterion. Each test has a stated blocker condition: if the blocker applies, the test is recorded as BLOCKED (not "failed"), with the blocker reason logged. BLOCKED tests do not count toward the "triggered" tally.

### Strong signals (S1–S6)

**S1. The three minority signatures are preserved in the November map.**
- *Threshold.* A map preserves all three formal signatures detected under the minority if: (a) a Calgary zone partition exists where one zone's mean ED population exceeds the other's by ≥10% (minority baseline: 12.20%, Zone A vs Zone B); (b) the City of Airdrie is split across ≥4 EDs; (c) a s.15(2) district exists whose geographic area includes ≥20% uninhabited protected land (national park, wilderness area, or equivalent) with population-weighted centroid outside the protected area.
- *Pass.* 0 of 3 criteria met. *Fail (signature triggered).* ≥1 of 3 criteria met. Reporting also states the count (0, 1, 2, or 3).
- *Blocker.* None. All three criteria are computable from the map plus 2021 census CSD data, irrespective of 2026 shapefile release.

**S2. New signatures appear beyond the minority's set.**
- *Threshold.* Any of: (a) Edmonton zone packing ≥10% gap between any two defensible Edmonton zones (using river, ward, or municipal partition); (b) cracking (≥4 EDs) in a third Alberta city not already flagged (i.e., beyond Airdrie in S1; Lethbridge and Red Deer are already flagged as cracking candidates in the baseline and are in-scope for this test); (c) an additional engineered s.15(2) boundary beyond the one flagged in S1.
- *Pass.* 0 of 3 criteria met. *Fail.* ≥1 of 3 criteria met.
- *Blocker.* None.

**S3. Both extra rural seats have engineered boundaries.**
- *Threshold.* The committee's 91-seat map contains 2 more seats than the existing 87-seat map (2019) or 2 more than the 89-seat proposals. Identify the incremental seats by comparison. If both (or at least 2) added seats relative to the majority 89-seat baseline are rural and both invoke s.15(2) with boundaries that include ≥20% uninhabited protected land, the signal fires.
- *Pass.* 0 or 1 engineered rural additions. *Fail.* 2 engineered rural additions.
- *Blocker.* If the November map's relationship to the 89-seat majority baseline is not reconstructible (e.g., the committee publishes only the final 91-seat map with no differential trace), the audit will compare to the 2019 87-seat baseline instead. Record which baseline was used.

**S4. Efficiency gap crosses the US 7% threshold.**
- *Threshold.* Efficiency gap (Stephanopoulos and McGhee 2015) computed on 2023 provincial election votes reallocated to the November map, using the audit's pre-existing 85/15 urban/rural weighting (w=0.85, the central blending convention applied identically to both 2026 commission maps; sensitivity range 0.60–0.90 also reported), exceeds 7% in absolute magnitude.
- *Pass.* |EG| ≤ 7.00%. *Fail.* |EG| > 7.00%.
- *Blocker.* Requires a vote-to-ED reallocation. If 2026 shapefiles are not released, the audit will use poll-to-ED crosswalks where available, as in the baseline. If even poll-level reallocation is infeasible, the test is BLOCKED.

**S5. Ensemble outlier test.**
- *Threshold.* The November map's UCP-favourability percentile, computed against a Markov-Chain Monte Carlo ensemble of ≥10,000 rule-following alternative 91-seat maps (GerryChain, seed published), falls in the top 5% (percentile ≥ 95) of UCP-favourable plans.
- *Pass.* Percentile < 95. *Fail.* Percentile ≥ 95.
- *Blocker.* Requires 2026 shapefiles. If Elections Alberta or the committee does not release shapefiles with the map, the test is BLOCKED. The audit will not infer shapefiles from the report text; inferred ensembles are not valid substitutes.

**S6. Publicly-supported configurations dropped; unsupported ones kept.**
- *Threshold.* Using the submission-archive public-support tiers in `analysis/reports/submission_search_findings.md`: the map drops configurations in tier "documented public support" (e.g., Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, Chestermere) while keeping configurations in tier "no documented public support" (Airdrie 4-way, Nolan Hill-Cochrane). The test fires if ≥1 supported config is dropped AND ≥1 unsupported config is kept, in the same map.
- *Pass.* No inversion. *Fail.* Both conditions met.
- *Blocker.* None (submission archive is complete as of this pre-registration).

### Weak signals (W1–W3)

**W1. Two extra rural seats on their own.**
- *Threshold.* The committee adds 2 rural seats relative to the 89-seat majority baseline, regardless of whether their boundaries are engineered (if both are engineered, S3 fires instead and this test is subsumed).
- *Pass / Fail.* Fires when 2 rural seats added without engineering. On its own, this is the stated UCP position and is not a strong signal.
- *Blocker.* Requires baseline identification per S3.

**W2. Calgary zone gap similar to the minority's.**
- *Threshold.* Calgary Zone A vs Zone B mean-ED-population gap ≥ 5% (below S1's 10% strong-signal threshold but above a null baseline). Majority baseline: 0.36%; minority baseline: 12.20%.
- *Pass.* Gap < 5%. *Weak signal.* 5% ≤ gap < 10%. *Strong signal (folds into S1).* Gap ≥ 10%.
- *Blocker.* None.

**W3. Nolan Hill-Cochrane hybrid retained without stronger justification.**
- *Threshold.* The map contains an ED that pairs Cochrane with a Calgary residential neighbourhood across the city limit (the minority's Calgary-Nolan Hill-Cochrane pattern), and the committee's stated rationale does not add substantive evidence beyond commuter-tie claims already shown unsupported at CSD resolution (`analysis/methodology/cochrane_journey_to_work.md`).
- *Pass.* No such pairing, or pairing with additional evidence. *Fail.* Pairing present with commuter-tie-only defence.
- *Blocker.* If the committee does not publish per-ED rationale text, the audit scores "ED boundaries present: yes/no" only and notes the rationale-evaluation gap.

### Process signals (P1–P5)

**P1. Committee proceedings closed to the public.**
- *Threshold.* The committee did not hold public hearings on the draft map before it was tabled.
- *Pass.* Public hearings held and transcripts published. *Fail.* No public hearings on draft map.
- *Blocker.* None.

**P2. Advisory panel members not named / terms of reference withheld.**
- *Threshold.* As of 2026-04-22, advisory panel membership and terms were unpublished. The test fires if membership and/or terms are never published prior to or with the November map release.
- *Pass.* Both published. *Fail.* Either remains unpublished at map release.
- *Blocker.* None.

**P3. Draft map not released for public comment.**
- *Threshold.* A draft of the committee's map was not released for public comment prior to the final 91-seat map.
- *Pass.* Draft released with ≥14-day public comment window. *Fail.* No draft public-comment window.
- *Blocker.* None.

**P4. Legislative adoption without amendment or published dissent.**
- *Threshold.* If the Legislature votes to adopt the committee's map, and the vote passes without amendment AND without a published dissenting opinion from any committee member.
- *Pass.* Either: the map is not yet adopted at scoring time (then record as "pending"); the map is adopted with published dissent; the map is amended during adoption. *Fail.* Adopted unanimously without amendment and without dissent.
- *Blocker.* If adoption timing falls after the 72-hour scoring window, record as "pending" and revisit once a legislative record exists.

**P5. AI tools used without disclosure.**
- *Threshold.* The committee uses AI-assisted tools in map drafting (a possibility raised by the Premier's 2026-04-16 remarks) and does not publish with the map: the prompts used, model versions, random seeds, candidate ensembles considered, and selection criteria. The audit's own AI-use framework (`analysis/reports/ai_use_recommendations_for_committee.md`) is the published standard against which disclosure is measured.
- *Pass.* Either: no AI tools used (with a clear committee statement); or AI tools used with full disclosure per the audit's framework. *Fail.* AI tools used with partial or no disclosure.
- *Blocker.* If the committee neither affirms nor denies AI use, record as "undetermined" and note the transparency gap separately.

### Supplementary gates (X1–X3)

**X1. Chair Miller's Recommendation 5 conditions (a)–(d) are satisfied.**
- *Threshold.* From the Chair's Addendum to the Majority Report (AEBC, 2026, pp. 66–67):
  - (a) No impact on any electoral division in Airdrie or south of it except Drumheller-Stettler.
  - (b) No impact north of Edmonton's North Saskatchewan River.
  - (c) South-of-NSR Edmonton districts revert to the interim-report map.
  - (d) A Clearwater County plus western Mountain View County s.15(2) district is restored.
- *Pass.* All four conditions met. *Fail (partial).* 1–3 conditions met (record count). *Fail (inverted).* 0 conditions met.
- *Blocker.* Condition (c) requires comparing to the interim-report Edmonton south-of-NSR districts; the interim report is public.

**X2. Rationale-against-data checks.**
- *Threshold.* For each rationale the committee states for a specific ED configuration, the audit cross-checks against the verification dataset used in the baseline scoring (Alberta Education school-division boundaries; StatsCan 2021 journey-to-work table 98-10-0459; Alberta Treasury Board 2024 population estimate; 2021 census CSD populations). A contradiction fires when a stated rationale is directly falsified by a public dataset.
- *Pass.* 0 rationale-contradictions. *Weak signal.* 1–2 contradictions. *Strong signal.* ≥3 contradictions.
- *Blocker.* If the committee does not publish per-ED rationale text, X2 is BLOCKED and noted as a transparency gap.

**X3. 338Canada (or equivalent) partisan cross-validation.**
- *Threshold.* The November map's reallocated seat count (using 338Canada poll-level projection or equivalent independent projection) shifts the UCP seat total by ≥2 relative to the majority baseline (which 338 reallocation gives as 67 UCP / 22 NDP). The test fires on UCP-favourable shifts of ≥2 seats.
- *Pass.* UCP reallocation ≤ 68. *Weak signal.* 69 ≤ UCP reallocation ≤ 70. *Strong signal.* UCP reallocation ≥ 71.
- *Blocker.* Requires 338Canada to publish a 91-seat reallocation, or the audit to compute its own via poll-to-ED crosswalks. If infeasible within the 72-hour scoring window, X3 is flagged as PENDING rather than BLOCKED, and updated when the reallocation is available.

### Scoring timing

All 17 tests will be scored within 72 hours of the November 2026 91-seat map's public release. The 72-hour window starts when the map is first publicly posted by the committee, the Legislative Assembly, or Elections Alberta — whichever is earliest. If the map is released piecemeal (e.g., overview map followed by per-ED boundaries), the 72-hour window starts at the first release that contains sufficient information for test scoring (ED names and rough boundaries are sufficient for S1-a, S1-b, S6, W2, W3, P1-P5, X1; detailed shapefiles are required for S4, S5, and X3).

---

## 4. Scoring authority

The audit's methodology is independently runnable. The scripts and data supporting each test are public in the audit's repository (see §3 test-by-test citations to files in `analysis/`). A third party can replicate the scoring by executing the same scripts against the committee's released map.

**Commitment.** The audit author will publish the per-test scorecard within 72 hours of map release, in the same structure as the baseline scorecard (`analysis/reports/track_c_checklist_baseline_scoring.md`), with each test's outcome recorded as PASS, FAIL (triggered), BLOCKED, PENDING, or UNDETERMINED, per the criteria in §3.

**No criteria revision.** The audit will not revise the numeric thresholds or pass/fail criteria in §3 between this pre-registration's submission and the scoring of the November map. Any discovered error in a threshold will be disclosed as an erratum but the original threshold remains in force for the November scoring. If a post-hoc methodological improvement is worth applying, it is recorded and scheduled for the next map cycle, not retrofitted into this scoring.

**Author disclosure.** The audit author is the scorer. This pre-registration does not create external scorer custody (which only a Registered Report at a peer-reviewed journal would achieve). The pre-registration creates *criteria custody*: the tests, thresholds, and pass/fail rules cannot be altered between now and the scoring, because the authoritative copy is held by OSF with a verifiable timestamp. Readers verify the author's scoring against the OSF-held criteria. This is the standard D17 fix (OSF-held pre-registration) and is the minimum methodological guarantee the audit commits to before the map lands.

---

## 5. What would falsify the audit's critique

If the November 91-seat map meets **all** of the following conditions, the audit will publish a concession statement in the November re-audit noting that its structural critique of the minority's signatures does not extend to the committee's output:

1. **S1 = 0 triggered.** Zero of three minority signatures are preserved in the November map (no Calgary zone packing ≥10%, no ≥4-way Airdrie split, no engineered s.15(2) boundary).
2. **S2 = 0 triggered.** No new signatures introduced beyond the minority's set.
3. **S6 = PASS.** No documented-public-support inversion.
4. **P1, P2, P3 all = PASS.** Committee held public hearings on the draft, named its advisory panel and published its terms, and released a draft for public comment before tabling.
5. **X2 ≤ 1 contradicted rationale.** The committee's per-ED rationales are substantially consistent with public datasets.

Additional conditions that, if met, strengthen the concession:
- S4 = PASS (efficiency gap ≤ 7%), indicating the map is not in US-court-flagged territory.
- S5 = PASS (ensemble percentile < 95) if shapefiles are released and the ensemble can run.
- X1 = all four R5 conditions met.

If all five core conditions hold and shapefiles are released allowing S5 to run and S5 passes, the audit will publicly note that **the committee's map, by the audit's own pre-registered criteria, is not a gerrymander under the methodology the audit applied to the minority map.** This is the strongest concession the pre-registered framework can produce; it is available.

Conversely, if any **four or more** of the strong-signal tests (S1 triggered, S2 triggered, S3 triggered, S4 failed, S5 failed, S6 failed) fire together with P1–P3 all failed, the audit's existing critique extends to the November map and the "sure-sign" threshold stated in the public checklist is met. Intermediate configurations (e.g., one signature triggered plus two process signals) are reported literally — not collapsed into a single "gerrymander / not gerrymander" verdict — per the audit's existing graded-evidence reporting discipline (Nosek et al. 2018; Munafò et al. 2017; ASA 2016, 2019).

---

## 6. Anticipated analyses

On the November map, the audit will compute and publish:

1. **Population equality (A-series).** MAD (mean absolute deviation), maximum deviation, distribution of per-ED population across the 91 seats, count of EDs outside the ±25% statutory window under 2021 census and 2024 TBF population estimates. Comparison against majority and minority baselines.
2. **Partisan metrics (B-series).** Efficiency gap, mean-median difference, declination, partisan bias at 50/50 vote share, using 2023 provincial vote reallocations. Comparison against baselines.
3. **Signature count (S-series).** Scored per §3.
4. **Geographic coherence (C-series).** Visual inspection of named EDs for lasso/corridor shapes, engineered statutory boundaries, and community-of-interest splits; symmetric-test-selection application of the same anomaly-scan question set used for the 89-seat maps.
5. **Process audit (D/P-series).** Inspection of the committee's public record for hearings, panel disclosure, draft-comment window, adoption vote, and AI-use disclosure.
6. **338Canada / independent reallocation (X3).** Seat-count reallocation using the same 338Canada riding-level methodology applied to the 89-seat maps (`analysis/methodology/338canada_riding_level.md`).
7. **Ensemble percentile (S5).** GerryChain MCMC ensemble, if shapefiles are released. Seed published with results.

All seven analyses produce numeric outputs. None of the thresholds or calculation methods will be changed between this pre-registration and the November scoring.

---

## 7. Commitments not to do

The audit commits **not to** do any of the following between this pre-registration and the November scoring:

1. **No post-hoc threshold adjustment.** The numeric thresholds in §3 (10% zone gap, 4-way Airdrie split, 7% efficiency gap, top-5% ensemble percentile, 5% weak-signal zone gap, 2-seat UCP shift) are fixed. No test's threshold will be tightened or loosened between now and November scoring.
2. **No new supplementary tests invented after map release.** The test set is fixed at the 17 tests in §3. If after the map lands the audit notices a feature that would warrant a new test, that observation will be reported as a "post-hoc observation not pre-registered" and will not affect the pre-registered scorecard's totals.
3. **No cherry-picking of reportable tests.** All 17 tests will be scored and reported, including tests that PASS (no signal triggered) or that return BLOCKED for lack of shapefiles. The scorecard will report the full grid, not a subset.
4. **No headline upgrade.** The audit will not elevate a triggered weak signal to a strong-signal claim in the narrative, nor downgrade a strong-signal trigger to a weak-signal footnote. The narrative tracks the scorecard.
5. **No re-ordering of the falsification criteria.** The five conditions in §5 that would produce a concession are fixed. The audit will not add a sixth condition after the map lands to preserve a gerrymander framing.
6. **No silent revision of pre-registration.** If a correction to this document is needed post-submission, it will be posted as a new OSF version with the diff visible and a stated reason. The original OSF-held version remains the authoritative criteria set; post-dated corrections do not retroactively change what was pre-registered.
7. **No selective release timing.** The November scorecard will be published in full within 72 hours of map release, regardless of whether the map appears favourable or unfavourable to the committee.

---

## 8. Reproducibility

The scripts that compute each test's output are in the audit's public repository at `analysis/` (paths cited per-test in §3). Python dependencies are pinned in `requirements.txt`. The 2021 census CSD data, 2023 election poll data, and commission report extracts are in `data/`. A third party can clone the repository, install dependencies, and replicate the baseline scoring against the known 89-seat maps. The November scoring uses the same scripts with the November map as input; no new scripts will be introduced that are not pre-registered here.

**Repository time-stamp.** The audit's git history is public and independent of OSF; readers can verify that the scripts and thresholds referenced here existed at the OSF submission date.

---

## 9. Declarations

- **Funding.** Self-funded. No institutional, governmental, or political-party funding.
- **Conflicts of interest.** None known. The author is not a candidate, party member, or commissioner.
- **AI use disclosure.** The audit uses large-language-model tools (Anthropic Claude; OpenAI GPT-family models at various points) for analysis assistance. The reproducibility commitment in §8 is what makes the AI-assisted analyses verifiable: scripts, data, and thresholds are published; a reader can run them without an LLM in the loop. The audit's broader AI-use framework is in `analysis/reports/ai_use_recommendations_for_committee.md`.
- **Version.** v0.1 of the pre-registration document. Later versions, if posted to OSF, will be visible alongside v0.1 with the original v0.1 timestamp preserved.

---

## 10. References

- Alberta Electoral Boundaries Commission. (2026). *Final Report*. Edmonton: Legislative Assembly of Alberta.
- American Statistical Association. (2016). Statement on statistical significance and p-values. *The American Statistician*, 70(2), 129–133.
- American Statistical Association. (2019). Moving to a world beyond "p < 0.05." *The American Statistician*, 73(sup1), 1–19.
- CBC Edmonton. (2026, April 16). Alberta Legislature approves motion to replace boundary commission process.
- Calgary Journal. (2026, April 21). Special Select Committee on electoral boundaries — what we know and do not know.
- Munafò, M. R., et al. (2017). A manifesto for reproducible science. *Nature Human Behaviour*, 1(1), 0021.
- Nosek, B. A., et al. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.
- Statistics Canada. (2021). *Journey to Work, Table 98-10-0459*. 2021 Census of Population.
- Stephanopoulos, N. O., & McGhee, E. M. (2015). Partisan gerrymandering and the efficiency gap. *University of Chicago Law Review*, 82, 831–900.
- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

---

*End of pre-registration document.*
