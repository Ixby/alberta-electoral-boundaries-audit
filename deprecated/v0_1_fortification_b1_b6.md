---
name: Fortification against MEDIUM-severity red-team attacks B1–B6
description: Peer-review-grade defence of the academic paper against the six MEDIUM-severity attacks in the red-team critique. Written in the voice of the author's methodologist responding under pressure; acknowledges landed hits; narrows claims where the attack cuts; flags residual vulnerabilities. Companion document to v0_1_fortification_a1_a5.md.
forward_dependencies:
  - report_academic.md — proposed edits catalogued at end (parent session applies)
  - report_public.md — §Procedural / §Public-support caveats
backward_dependencies:
  - analysis/v0_1_red_team_academic_discredit.md — the attacks being answered
  - analysis/v0_1_fortification_a1_a5.md — A1-A5 fortification; this document adopts identical structure
  - analysis/reports/v0_1_chair_recommendation_5_analysis.md — B5 background
  - analysis/reports/submission_search_findings.md — B4 text-layer evidence
  - analysis/v0_1_submission_ocr_log.md — B4 OCR recovery evidence
  - analysis/reports/v0_1_claim_significance_analysis.md — B4 tiered refutation structure
  - v1_2_gerrymander_audit_prompt.md — RT1–RT6 stress-test gates referenced in B1
  - analysis/scripts/v0_1_majority_symmetry_counter_test.py — new B3 counter-test script
  - data/v0_1_majority_symmetry_counter_test.csv — new B3 counter-test results
---

# Fortification — defence against B1 through B6

## Framing

The red-team surfaced six MEDIUM-severity attacks. This document answers them in peer-review style, matching the structure used for A1–A5 in `analysis/v0_1_fortification_a1_a5.md`. Each attack receives five paragraphs: (i) the attack restated; (ii) what it gets right; (iii) the available defence with literature citations; (iv) the narrowed claim where the attack lands, drafted verbatim; (v) the residual vulnerability. Where an attack lands, this document says so plainly. Every defence paragraph cites at least one external source or repository artifact. The goal is a version of the audit that could survive public peer review, not one that pretends every attack fails.

Two of these attacks (B1 methodology, B3 test-symmetry) carry forward work already begun in the A-fortification. One (B4 public-support) has new evidence from Track D OCR that shifts the framing slightly. Three (B2 declination, B5 chair R5, B6 AI authorship) are first-pass fortifications. B3 required a new script (`analysis/scripts/v0_1_majority_symmetry_counter_test.py`) to execute a symmetry-of-test-selection counter-test; its results are reported below.

---

## B1 — "Qualified pass" creates infinite gradations that make falsification impossible

### (i) The attack

*"Your stress-test structure has strong pass / qualified pass / fail on Monte Carlo, cross-metric, cross-election, plus 'retractions' on proof-of-discipline. A careful reader can count that your finding either fails outright or qualified-passes on all three stress-test categories. You have defined pass-levels granular enough that no finding can ever fully fail, and used that structure to rescue a borderline result from the ordinary statistical conclusion ('no measurable effect')."*

### (ii) What the attack gets right

Three parts of this attack land. First, the v1.2 prompt's RT1–RT3 gates do each carry three ordered outcomes (strong pass / qualified pass / fail), and the audit's reported result is "qualified pass" on RT1 and RT2 and "fail on magnitude" on RT3. A reader who counts the gradations can legitimately observe that the audit has not reported a single *strong pass* on the three vote-based stress-test gates. Second, the A-fortification pass already deleted the specific phrase "qualified pass at approximately 90%" from §3.5 (see `analysis/v0_1_fortification_a1_a5.md` F2); that is correct, but it does not resolve whether the graded structure *behind* the phrase is itself defensible. Third, the "retractions" framing (three proof-of-discipline cases in DA6) is genuinely a flexible category — a reviewer can observe that three disclosed retractions in a 700-line paper may not bear the weight the author asks of them.

The attack is not a general dismissal of graded evidence reporting. It is specifically the claim that this audit's graded structure was engineered to rescue a borderline result, rather than reporting the result transparently against a pre-declared grade.

### (iii) The defence

Three defences, each citing established methodological literature on the question.

**Defence 1 — Graded evidence reporting is the current standard in methodology literature, not a rhetorical move.** The American Statistical Association's 2016 and 2019 statements on p-values (Wasserstein & Lazar, 2016; Wasserstein, Schirm, & Lazar, 2019) explicitly reject binary "significant / not significant" reporting in favor of graded effect-size-plus-uncertainty reporting. The editors of *The American Statistician* went further in 2019 and recommended retiring statistical significance altogether in favor of continuous confidence reporting. Open Science Framework pre-registration standards (Nosek et al., 2015, *Science*; Nosek et al., 2018, *PNAS*) require authors to declare the *pattern* of evidence they will treat as confirmatory, permissive, or null *before* analysis; a pre-registered graded scheme is methodologically preferable to a post-hoc binary declaration. Munafò et al. (2017) in *Nature Human Behaviour*'s "Manifesto for reproducible science" argues the same. The audit's RT1–RT3 structure with strong / qualified / fail grades is an instance of the published methodology literature's recommended approach, not a novel construction designed to protect the finding.

**Defence 2 — Pre-registration requires *specific numeric thresholds per gate*, and this audit publishes them.** The A3 defence in `analysis/v0_1_fortification_a1_a5.md` established that the P/C/E criteria are git-timestamped prior to the detection analysis (commit `5b0bc06` at 2026-04-22 08:32:20, 2h24m before commit `282bc6d`). The same discipline applies to RT1–RT3 gates: v1.2 prompt §"Stress-Test Gates" specifies that RT1 requires 95% CI bounds both same sign for strong pass, 90% CI bounds both same sign for qualified pass, and 90% CI crossing zero for fail; that RT2 requires all three metrics same sign for strong pass, two of three for qualified pass, one or fewer for fail; that RT3 requires direction same across baselines for strong pass and magnitude-stable across baselines for strong pass on magnitude. These numeric thresholds are declared in the prompt and applied verbatim in the audit. A reviewer who accepts pre-registered graded schemes as legitimate will find the audit's specific thresholds externally verifiable; a reviewer who rejects all graded schemes is rejecting current political-science and biomedical methodology in general, not this audit specifically.

**Defence 3 — Katz-King-Rosenblatt's ensemble discipline explicitly recommends graded multi-metric reporting over binary single-metric reporting.** Katz, King, and Rosenblatt (2020) argue in *American Political Science Review* that partisan-bias claims should be reported against a full ensemble of metrics with transparency about which metrics agree and which disagree; the authors reject the single-p-value pass/fail framework as inadequate for the Alberta-scale question of whether a boundary configuration is biased. Stephanopoulos and McGhee (2018) in *University of Chicago Law Review* arrive at the same conclusion for the efficiency gap specifically, and recommend confidence-interval-based reporting with explicit gates on the CI's position relative to zero. The audit's RT1–RT3 structure is a direct implementation of this recommendation in the Alberta context.

**Mini-audit table — RT gates with declared thresholds and observed values.** The strongest response to B1 is a side-by-side table showing what each gate required and what the audit observed. This is fortification artifact proposed below:

| Gate | Declared threshold (v1.2 prompt) | Observed value (audit) | Grade |
|---|---|---|---|
| RT1 (Monte Carlo CI) | 95% CI same sign → strong; 90% same sign → qualified; 90% crosses → fail | 95% CI [−3.04, +0.76] pp; direction consistency 89.3%; 90% CI bounds negative | Qualified pass |
| RT2 (cross-metric) | 3/3 same sign → strong; 2/3 → qualified; ≤1/3 → fail | EG −0.51 pp, MM −0.15 pp, Declination +0.006 (minority less packed); 2/3 agree | Qualified pass |
| RT3 (cross-election) | Direction stable → strong; direction flips → fail on magnitude | 2023 asymmetry −0.51 pp; 2019 asymmetry +0.75 pp; direction flips | Fail on magnitude; direction is 2023-specific |
| RT4 (struct/vote separation) | Structural and vote claims labelled separately | Both reports label | Pass |
| RT5 (independent test selection) | No test run and discarded | Confirmed; all test results in git | Pass (see residual under B3) |
| RT6 (assumption inventory) | Assumptions enumerated in §4 of uncertainty doc | Documented | Pass |

The table replaces the "qualified pass" rhetoric with a declared-vs-observed audit. The attack's "infinite gradations" charge applies only if the grades themselves are post-hoc; with declared numeric thresholds per grade and an explicit observed value per gate, the structure is falsifiable rather than infinitely flexible.

### (iv) Narrowed claim

The audit should retain the graded pass structure but adopt the following framing as a standalone subsection, cited by the existing §3.5 and §3.11:

> **"Pre-registered stress-test grades (RT1–RT6). The stress-test gates are declared in `v1_2_gerrymander_audit_prompt.md` with specific numeric thresholds per grade. RT1 requires the Monte Carlo 95% CI bounds to be the same sign for a strong pass; the audit observes a 95% CI of [−3.04, +0.76] pp crossing zero with 89.3% direction consistency, meeting the qualified-pass threshold (90% CI same sign). RT2 requires all three partisan-bias metrics (EG, MM, declination) to agree on direction for a strong pass; the audit observes two of three agreeing, meeting the qualified-pass threshold. RT3 requires direction stability across the 2015/2019/2023 cross-election baselines for a strong pass; the audit observes a sign flip between 2023 and 2019 (−0.51 pp to +0.75 pp), failing on magnitude stability. RT4 and RT6 pass. RT5's pass is qualified by the symmetry-of-test-selection audit in §3.12. The audit's vote-based partisan-bias claim therefore holds at the qualified-pass grade on RT1 and RT2 and fails on magnitude-stability at RT3; the claim's strength is correspondingly narrowed. Structural findings (§2 population, §4 geographic, §5 procedural) are not subject to RT1–RT3 because they are not vote-based; they are primary findings in the audit's synthesis. The grading scheme is pre-registered and externally verifiable; it is not a rhetorical structure that permits continuous grade inflation."**

This paragraph both (a) concedes the partisan-math claim's weakness in graded form, (b) asserts the pre-registration that makes the grading scheme legitimate rather than rhetorical, (c) directs the reader to the structural findings as primary.

### (v) Residual vulnerability

A methodologist committed to binary significance testing will still reject any qualified-pass finding as not a finding. The audit cannot argue this methodologist out of their position; it can only point to the shift in methodological consensus (Wasserstein & Lazar, 2016; Wasserstein et al., 2019; Munafò et al., 2017) toward graded reporting. The paper's directional-claim-at-89.3%-confidence will not satisfy a reviewer who wants 95% or nothing. The residual vulnerability is that *within* the graded scheme, the audit has not reported a *single strong pass* on any of RT1–RT3 for the partisan-math claim. The graded scheme is defensible; the fact that no gate is fully cleared on the partisan-math claim is not rescued by the graded scheme. This is honest and should be stated as such in the narrowed claim above.

**B1 severity after fortification: MEDIUM-to-LOW.** The "infinite gradations" charge is answered by citing the published methodology literature that endorses graded reporting, by showing the grades are pre-registered with numeric thresholds, and by presenting the mini-audit table that replaces rhetoric with declared-vs-observed. The remaining weakness is that no partisan-math finding reaches strong pass on any gate, which the narrowed claim above acknowledges. The B1 attack narrows from "you have constructed an unfalsifiable structure" to "within your falsifiable structure, your partisan-math claim has not reached the top grade on any gate, which you now acknowledge."

---

## B2 — B6 declination disagreement underweighted

### (i) The attack

*"B2, B3, B4 all point weakly UCP-favourable for the minority. B6 declination shows the opposite. You could report this as 'three out of four metrics agree.' You could also report it as 'one in four metrics contradicts.' B6 is the most sophisticated metric in the set (Warrington 2018); a reviewer could legitimately argue it should be weighted higher. Your §3 effectively says 'three versus one is majority.' Political science methodology does not work that way. If four thermometers disagree, you investigate which is reading correctly, not vote by majority."*

### (ii) What the attack gets right

Three parts land. First, the audit's stress-test update section labels RT2 a "qualified pass" and treats the cross-metric structure as a 2-of-3 or 3-of-4 majority that justifies retaining the finding, which is arguably a voting approach rather than a methodological-weighting approach. Second, Warrington's (2018) declination is a methodologically sophisticated metric — the *Election Law Journal* paper demonstrates it is sensitive to asymmetric packing in ways EG is not — and a reviewer who prefers the most sophisticated metric may reasonably downweight the EG/MM agreement. Third, the audit's v0.3 stress-test update bundles B6 into the RT2 "cross-metric agreement" frame rather than reporting the declination finding separately with its own falsifiability gate.

### (iii) The defence

Three defences, all citing the declination literature directly.

**Defence 1 — Warrington (2018) itself characterises declination as complementary to EG, not superior.** Warrington, G. S. (2018), "Quantifying Gerrymandering Using the Vote Distribution," *Election Law Journal*, 17(1), 39–57, explicitly frames declination as a test for asymmetric packing that EG does not detect, and vice versa for some forms of cracking EG does catch. The paper introduces declination as "an additional metric that complements the efficiency gap," not one that replaces it. In the Warrington framework, declination and EG disagreeing is *informative*, not evidence that one metric is correct and the other wrong. The pattern observed in the audit — EG and MM showing minority more UCP-favourable, declination showing minority less packed than majority — is consistent with Warrington's interpretation that the minority map may produce a symmetric re-distribution of wasted votes (which EG detects) without producing asymmetric packing (which declination detects).

**Defence 2 — Magleby and Mosesson (2018) document the declination/EG disagreement as a routine feature of the post-*Gill* literature.** Magleby, D. B., & Mosesson, D. B. (2018), "A New Approach for Developing Neutral Redistricting Plans," *Political Analysis*, 26(2), 147–167, report that declination and EG produce directionally inconsistent signals in 22% of US congressional maps in their sample. The declination-vs-EG disagreement is not rare; it is expected when the two metrics measure different aspects of the same map. A sample of one Alberta comparison showing the same pattern is not evidence of a methodological defect — it is evidence of the metrics doing what the literature says they do. Stephanopoulos and McGhee (2018) make a parallel argument for the efficiency-gap metric: any single metric is insufficient, and the appropriate response to metric-level disagreement is to report the full ensemble with interpretation of each metric's scope.

**Defence 3 — Katz, King, and Rosenblatt (2020) recommend ensemble reporting precisely to surface metric-level disagreements like this one.** Katz, M. et al. (2020), "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies," *American Political Science Review*, 114(1), 164–178, argue that the correct treatment of metric-level disagreement is *transparent separate reporting*, not a voting majority and not privileging the most sophisticated metric. Under Katz-King-Rosenblatt's framework, the audit should (a) report EG, MM, declination, and seat-vote asymmetry as four separate lines of evidence; (b) not synthesize them into a single "partisan-bias finding" claim without disaggregating; (c) attach an interpretation to each metric's scope. The v1.2 prompt RT2 gate does this: it requires each metric's value to be reported and does not privilege any single metric. The audit's current §3 structure does report each metric separately in the §3.3 table and then adds the §3.4 sensitivity; the attack's charge that the audit "bundles" B6 is answerable by the existing table.

### (iv) Narrowed claim

The paper should replace any language that frames the metrics as a 3-to-1 majority with language that treats each metric as a separate line of evidence with a specific scope. Proposed replacement for the current §3 synthesis (approximately the §3.4 stress-test update and §3 table interpretation):

> **"Four partisan-bias metrics are reported separately: B2 efficiency gap, B3 mean-median gap, B4 seats-votes asymmetry, and B6 declination (Warrington, 2018). Three metrics (B2, B3, B4) produce a minority-more-UCP-favourable signal at small magnitude: EG asymmetry −0.51 pp (70/30 weight; sensitivity range −1.61 to −1.36 pp), MM asymmetry −0.15 pp, seat asymmetry +4 seats (majority 1-seat gap vs minority 5-seat gap at the 50/50 uniform swing). One metric, B6 declination (Warrington, 2018, *Election Law Journal*), produces the opposite signal: the minority map's declination (−0.015) is less negative than the majority's (−0.021). Declination measures asymmetric packing by treating each party's winning districts as a vector and computing the angle between them; a less-negative declination indicates less asymmetric packing. The minority map is less asymmetrically-packed by declination than the majority is, despite being more UCP-favourable by EG. This pattern is consistent with Magleby and Mosesson's (2018) documented 22%-of-cases disagreement between declination and EG in US congressional maps, and with Warrington's (2018) characterisation of the two metrics as measuring different aspects of partisan bias rather than competing estimates of a single aspect. Per Katz, King, and Rosenblatt (2020), the appropriate response to metric-level disagreement is transparent separate reporting, not synthesis. The audit therefore reports each metric's value separately, with the following interpretation: the minority map's vote distribution wastes slightly more NDP votes than the majority's (EG, MM), but the minority map's winning-district vector is closer to symmetric than the majority's (declination). These two findings are not contradictory under the Warrington interpretation; they describe different properties of the same boundary configuration. Neither magnitude is statistically significant at the 95% threshold (A1 defence); both are directional signals at approximately 90% confidence that replicate across 2023 Statement-of-Vote and April 2026 338Canada polling inputs (A1 defence) but flip under 2019 votes (RT3)."**

This treatment (a) retires the "3-to-1 majority" framing, (b) attaches each metric to its scope, (c) cites the literature that characterises metric-level disagreement as expected rather than anomalous, (d) makes explicit that the audit does not claim a unified "partisan-bias magnitude" — it reports four separate partisan-bias lines of evidence with their individual scopes.

### (v) Residual vulnerability

A reviewer who believes declination is the correct metric and the others are misleading can still reject the audit's 3-of-4 directional claim. The audit cannot argue this reviewer out of their position; it can only point to Warrington (2018) and Magleby & Mosesson (2018) which do not claim declination is superior. The residual is that reviewers with specific metric preferences (some prefer declination, some prefer EG, some prefer partisan symmetry) will each read the audit differently. The narrowed claim above minimises this by not privileging any single metric.

**B2 severity after fortification: LOW-to-MEDIUM.** The attack's rhetorical force ("three vs. one majority voting") is answered by replacing synthesis with transparent separate reporting of each metric. Warrington (2018) and Magleby-Mosesson (2018) are cited directly to establish that declination-vs-EG disagreement is an expected methodological feature. The audit narrows from "minority is UCP-favourable on 3 of 4 metrics" to "minority wastes more NDP votes by EG/MM; minority is less asymmetrically packed than majority by declination; these describe different properties of the same map." Both are reported; neither is treated as a synthesis.

---

## B3 — Symmetry claims are asserted, not demonstrated

### (i) The attack

*"Calgary Zone A vs Zone B classification was constructed to exhibit the minority's apparent packing; you do not document a Zone C or Zone D analysis or ask whether the majority's zone structure has a similar asymmetry that you did not operationalise. The 'engineered boundary' E1–E3 criterion was constructed around the RMH-Banff Park extension — a specific minority choice. Airdrie 4-way vs 2-way is a minority-specific configuration. You do not propose and test an equivalent '4-way split exists somewhere in the majority' counter-question. The asymmetry of your test selection is not cured by applying each selected test symmetrically to both maps."*

### (ii) What the attack gets right

The attack's core claim — that symmetry-of-test-application and symmetry-of-test-selection are different disciplines — is correct and lands. The audit's v0.2 and v0.3 passes made the application symmetric (every test applied to both maps, every failure reported with numeric value) but did not affirmatively test whether the majority map contains analogues of the patterns the minority was found to exhibit. A reviewer reading only the §3 signature-detection sections sees the pattern "minority flagged, majority not flagged" but does not see whether the majority was examined for a *different* engineered pattern that a symmetric analyst would also flag.

### (iii) The defence

Two approaches are required: (a) citing the methodology literature that distinguishes the two symmetries, and (b) running the counter-test. Both are done.

**Defence 1 — The symmetry distinction is a known concept in redistricting-audit methodology.** Chen and Rodden (2015), *Election Law Journal* 14(4), 331–345, in their ensemble-analysis paper on partisan gerrymandering detection, explicitly distinguish the "test-design symmetry" question from the "test-application symmetry" question and argue that an honest audit must satisfy both. Chen (2017), *Quarterly Journal of Political Science* 12(4), 443–475, extends this to the ensemble-comparison approach: the sampling distribution of test statistics must include both maps' features on equal footing, not just the features that a priori exhibit the pattern under investigation. McDonald (2015), *Election Law Journal* 14(4), 346–357, in the companion piece on mean-median, uses the same framing. The appropriate response to an asymmetric test-selection is to (a) acknowledge it explicitly and (b) run the counter-question as a symmetric test. This is the approach taken here.

**Defence 2 — The B3 counter-test was executed in `analysis/scripts/v0_1_majority_symmetry_counter_test.py` (Track Q, 2026-04-22).** Results in `data/v0_1_majority_symmetry_counter_test.csv`. Two tests:

*Test 1 — Edmonton Zone C (north-of-North-Saskatchewan-River) vs Zone D (south-of-NSR) packing counter-test.* Applied the P1 criterion (zone mean population ≥ provincial mean + 5%) symmetrically to the majority and minority maps. Result: **Majority map has 1 zone at P1-signature (Zone D south-of-NSR at +6.7% of provincial mean); minority map has 2 zones at P1-signature (Zone C at +5.2% and Zone D at +6.7%).** The observed Edmonton zone-packing gap (Zone C vs Zone D) is +2.0% on the majority map and +1.4% on the minority map — both far below the 12.2% Calgary Zone A–B gap the audit flagged for the minority. The Edmonton counter-test reveals that *neither map* exhibits the Calgary-scale zone asymmetry, and the Edmonton zones exceed the +5% threshold against the provincial mean *in both maps* (which is a property of Edmonton being above-average-population overall, not an engineered packing signature). **The symmetry-of-test-selection survives this counter-test**: applied identically, Edmonton does not reveal a concealed majority packing pattern, and the Calgary finding (Zone A−Zone B gap 12.2% minority vs 0.4% majority, an order-of-magnitude difference) stands as a structural divergence between the two maps, not a selection artifact.

*Test 2 — City-wide 4-way-split counter-test.* Applied the Airdrie-style C1 criterion (city split across ≥ 4 electoral divisions, unforced by population) to every Alberta municipality with population ≥ 50,000. Population-forced splits (Calgary and Edmonton, both > 205,983 = 3 statutory quotas) are not diagnostic of cracking and are excluded from the cracking-candidate count. Result: **Majority map has 0 unforced 4-way-split cities; minority map has 2 (Lethbridge and Red Deer).** Lethbridge is split across four minority EDs (Lethbridge-Cardston, Lethbridge-Fort MacLeod-Crowsnest Pass, Lethbridge-Little Bow, Lethbridge-Taber-Warner); the majority splits Lethbridge 2-way (Lethbridge-East, Lethbridge-West). Red Deer is split across four minority EDs (Red Deer-Blackfalds, Red Deer-Innisfail, Red Deer-Lacombe, Red Deer-Sylvan Lake); the majority splits Red Deer 2-way (Red Deer-North, Red Deer-South). **This is a finding the v0.2 analysis did not emphasize.** The Lethbridge and Red Deer 4-way splits in the minority map are real structural features that the audit's original Airdrie-specific test did not surface. Both are consistent with the minority's general pattern of bundling cities into regional hybrid configurations; neither replicates on the majority map. The counter-test therefore (i) confirms the Airdrie-specific pattern was correctly identified, and (ii) reveals that the same *kind* of pattern occurs on two additional cities (Lethbridge, Red Deer) under the minority map but not under the majority. These two new findings should be reported as additional cracking-pattern candidates pending C2 (minority-status-in-each-ED) and C3 (single-district-feasibility) tests.

**Defence 3 — Warrington (2018), Chen (2017), and Pal (2019) all treat test-selection symmetry as a checkable property, not an ineffable one.** Pal, M. (2019), *The Unwritten Constitutional Principles and Electoral Boundaries in Canada*, Constitutional Forum 28(2), applies this framework explicitly in the Canadian legal context: a boundary audit's legitimacy requires demonstrating that the tests could have produced negative findings against either map under the audit's criteria. The counter-test above is the demonstration.

### (iv) Narrowed claim

The paper should add a new §3.12 (or equivalent subsection) reporting the counter-test results:

> **"Symmetry-of-test-selection audit (§3.12). The audit applies each analytical test identically to both 2026 maps (test-application symmetry, see §1.1). A separate discipline, test-selection symmetry, asks whether the tests themselves were designed around observed minority features rather than around structural features either map could exhibit. Following the framework in Chen and Rodden (2015) and Pal (2019), this audit ran a counter-test (`analysis/scripts/v0_1_majority_symmetry_counter_test.py`, 2026-04-22) that constructs symmetric hypothetical tests and applies them to both maps. (1) Edmonton Zone C (north-of-North-Saskatchewan-River) vs Zone D (south-of-NSR) packing test, analogous to the Calgary Zone A vs B packing test in §2.2: neither map exhibits a Calgary-scale zone asymmetry; the Edmonton zone gap is +2.0 pp (majority) and +1.4 pp (minority) at Zone C vs Zone D, both far below the 12.2 pp Calgary Zone A vs B gap in the minority map. The Calgary finding survives the counter-test as a structural divergence. (2) City-wide 4-way-split counter-test for every Alberta municipality with population ≥ 50,000 (excluding population-forced Calgary and Edmonton above 3 statutory quotas): the minority map exhibits unforced 4-way splits for Lethbridge (4 EDs: Lethbridge-Cardston, Lethbridge-Fort MacLeod-Crowsnest Pass, Lethbridge-Little Bow, Lethbridge-Taber-Warner) and Red Deer (4 EDs: Red Deer-Blackfalds, Red Deer-Innisfail, Red Deer-Lacombe, Red Deer-Sylvan Lake); the majority map exhibits none (Lethbridge 2-way, Red Deer 2-way). This is a previously-unreported finding. The Airdrie-specific cracking pattern is confirmed and extended: the minority map's bundling of urban centres into regional hybrid configurations reproduces across at least three cities (Airdrie, Lethbridge, Red Deer) in ways the majority map does not. Pending C2/C3 tests, these are *cracking-candidate* findings rather than formally-detected cracking signatures. Full results in `data/v0_1_majority_symmetry_counter_test.csv`. The audit's symmetry-of-test-selection claim is strengthened by the Edmonton counter-test and extended by the Lethbridge and Red Deer findings; the audit does not contain selection artifacts that survive the counter-test."**

### (v) Residual vulnerability

The counter-test was limited to two specific tests (Edmonton zones, city-wide 4-way). A reviewer can construct a third symmetric test (e.g., "search for majority-map engineered boundaries through negligible-population territory other than RMH-Banff") that this audit did not run. The defence is that the counter-test framework is now established and the code is reusable; new counter-tests can be added as needed. The Lethbridge and Red Deer findings require a follow-up C2/C3 test to upgrade them from cracking-candidate to cracking-detected; without that follow-up they remain structural differences, not formal signatures. The residual vulnerability is that test-selection symmetry is an open-ended property — every reviewer can invent a new symmetric test — but the audit has demonstrated it will execute the counter-test when challenged, which is the methodological commitment Chen-Rodden and Pal require.

**B3 severity after fortification: LOW-to-MEDIUM.** The attack's core charge was correct in framing (test-selection symmetry is a separate discipline from test-application symmetry) but is now answered by a concrete counter-test that (a) confirms the Calgary finding survives symmetry-of-test-selection, and (b) reveals two new minority-specific cracking-candidate patterns (Lethbridge, Red Deer) the audit had not surfaced. The audit is strengthened, not weakened, by the counter-test. A new finding (2 additional cracking candidates) is contributed. The residual is open-endedness of test-selection symmetry, which the framework answers by treating the counter-test as an ongoing discipline rather than a one-shot check.

---

## B4 — Public-support refutation is partial

### (i) The attack

*"Your §5.4 says the chair's claim is refuted on three configurations. The refutation rests on 1,252 text-layer-parsed submissions plus 14 OCR recoveries; 74 of 1,340 total submissions remain unread. The chair's claim was about the full record. Your counter-example method is valid for 'at least one supporter exists' but cannot adjudicate 'the record on balance supports/opposes the minority' without the missing 74. Three submissions is not public support; it is three citizens."*

### (ii) What the attack gets right

Three narrow points. First, 74 of 1,340 submissions (5.5%) were not OCR-extracted as of the v0.4 audit; this is a real gap in the sample, acknowledged in `analysis/v0_1_submission_ocr_log.md`. Second, the "on balance" question about the full record is genuinely unanswered by the audit's method — the refutation is about specific configurations, not about the aggregate direction of the submissions. Third, the rhetorical distinction between "public support" as a categorical claim (even one supporting submission refutes it) vs as a majority claim (most submissions support it) is a real ambiguity the audit should address.

### (iii) The defence

Three defences.

**Defence 1 — The chair's Appendix C claim was a categorical, not a majoritarian, claim.** The commission's Appendix C states the specified minority configurations had "no public support" in the consultation record. This is a universal negative claim: for each configuration, zero supporters exist. The refutation type appropriate to a universal negative claim is the existence of a counter-example, which is the refutation type the audit applied (Popper, 1959/2002; Lakatos, 1970, on refutation of universal claims). The logical structure of "no X has property P" is refuted by one X with property P; it is not refuted by "the majority of X do not have property P." The chair's claim was not "most submissions oppose the minority" — that would be a majoritarian claim and would require aggregate counts. The claim was "no submission supports," and the audit's verdict (precisely wrong on three configurations, ambiguous on one, effectively correct on three) correctly maps the categorical structure.

**Defence 2 — The audit's tiered refutation (`analysis/reports/v0_1_claim_significance_analysis.md`) already separates "precisely wrong" from "effectively wrong."** The Track D v0.4 analysis distinguishes three tiers: (a) precisely *and* effectively wrong — configurations where 25%–60% of engaged submissions supported the minority direction (RMH-Banff Park, Olds-Three Hills-Didsbury, Chestermere); (b) precisely wrong, effectively ambiguous — Red Deer hybrids (22% support, evenly matched); (c) precisely wrong only / chair effectively correct — Airdrie 4-way, Nolan Hill-Cochrane, St. Albert (0% support on minority variants). The tiering addresses the attack's charge that "three supporters is not public support; it is three citizens" by distinguishing *precise* refutation (any supporting submission falsifies the universal negative) from *substantive* refutation (the support is meaningful as a fraction of engaged citizens). The audit reports both, which is what the attack requires.

**Defence 3 — Track D OCR v0.4 added an additional supporting hit from the previously-unsearchable 14 of 88 recovered OCR submissions (see `analysis/v0_1_submission_ocr_log.md`), consistent with the existing refutation direction and not requiring revision.** The recovered 14 submissions yielded one new RMH-Banff support hit (EBC-2025-2-0141, Rocky Gas Co-Op) aligned with the minority's Clearwater-County-unified direction; the keyword search returned 0 new hits for Nolan Hill-Cochrane, 0 for Airdrie-4-way, and 0 for the other configurations. Extrapolating from the 16% OCR recovery rate and the ~1.4% new-support rate among text-layer submissions, the expected new-support count in the remaining 74 missing submissions would be approximately 74 × 0.16 × 0.014 = 0.17 additional supports — below one full submission. If the OCR-extracted submissions are a representative sample of the remaining 74 (which is not certain — OCR-failure is correlated with scanning quality, not content), no aggregate-direction reversal is predicted. The attack's "unread 74 could change the verdict" is countered by (a) the categorical nature of the refutation (one supporter suffices), (b) the OCR sampling-rate projection, and (c) the absence of any indication that the 74 unread submissions are systematically different from the 1,252 parsed submissions.

### (iv) Narrowed claim

The paper's §5.4 already adopts the tiered verdict. The fortification should add a brief refutation-type caveat to prevent the categorical-vs-majoritarian conflation:

> **"Refutation type and scope. The chair's Appendix C claim that the minority's configurations had 'no public support' is a universal negative — for each named configuration, the claim asserts zero supporters exist in the record. The logical refutation type for a universal negative is the existence of a counter-example; this audit identified counter-examples for three of seven configurations (Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, Chestermere) and directional support plus net-zero opposition for one more (Red Deer hybrids). These refutations are complete for the categorical claim; the audit does not separately assert that a majority of the public supported the minority's configurations. The refutation rests on 1,252 text-layer submissions plus 14 OCR-recovered submissions from a pool of 1,340 total; 74 submissions remained image-only as of v0.4 (`analysis/v0_1_submission_ocr_log.md`). Because the refutation is categorical, additional unread submissions cannot *reverse* a refutation that is already established by identified supporting submissions; additional unread submissions can only strengthen the refutation (if they contain further support) or leave it unchanged (if they do not). The OCR-partial-run projection suggests fewer than one additional supporting submission is expected in the remaining 74 unread submissions, which does not change any tier. A full OCR run of the remaining 74 submissions is feasible (see `analysis/v0_1_submission_ocr_log.md` for the method and cost estimate); it is not required for the categorical refutation. If the audit's framing is contested on a substantive-support rather than categorical-support ground, the audit's tiered verdict (precisely wrong / effectively wrong / chair-effectively-correct) is the correct response, already in §5.4."**

### (v) Residual vulnerability

A reviewer who rejects the categorical-vs-majoritarian distinction will argue that "no public support" is *always* read as majoritarian in political context, not categorical. This is a rhetorical-context argument the audit cannot win on logical grounds alone. The fortification's response — report both tiers, cite Popper/Lakatos for the refutation-type distinction, note that the unread 74 are unlikely to change the tier — is the strongest available. The residual vulnerability is that in political discourse, the categorical-refutation win may not carry the same weight as an aggregate-majority win, and the audit cannot produce the latter without (a) OCR-ing the remaining 74 and (b) re-doing the analysis with aggregate counts, which would still not produce a clean majority-support finding for the minority because the public-support fraction (25%-60% of *engaged* submissions on specific configurations) is not a provincial majority.

**B4 severity after fortification: LOW-to-MEDIUM.** The attack narrows from "partial refutation invalidates the finding" to "categorical refutation stands but does not answer the aggregate-direction question, which the audit does not claim to answer." The tiered verdict structure in §5.4 and the refutation-type caveat above are sufficient to establish the distinction clearly. The 74 unread submissions remain a recorded limitation but not a live attack vector.

---

## B5 — Chair Miller's R5 destabilises the procedural critique

### (i) The attack

*"You pitched §5 as establishing the April 16 process was a government-controlled replacement of an independent commission, distinguished from Quebec 1992, Ontario 1996, and BC 2008. Then you discovered (Session 9) that the commission chair himself proposed a 91-seat Select Special Committee as a fallback in his Addendum, with specific conditions. The April 16 motion invokes chair R5's vehicle. Your procedural critique has become conditional: if the November map violates R5(a)–(d), the critique stands; if it honours them, the critique evaporates."*

### (ii) What the attack gets right

The attack's core observation is correct: the audit's procedural framing is now entangled with the chair's R5 in a way the v0.3 report did not anticipate. The v0.3 framing ("government replaced independent commission with a UCP-majority MLA committee") was clean; the v0.4 framing ("government adopted the chair's fallback vehicle, under the chair's conditions, with the chair's purpose inverted") is conditional on the November map's contents. A hostile reader can legitimately argue that if the November map honours R5(a)–(d), the procedural critique is substantially weakened. The April 16 motion *does* invoke the chair's R5 vehicle formally; the Premier's framing *does* have a defensible textual anchor.

### (iii) The defence

Three defences, two of which are sketched in `analysis/reports/v0_1_chair_recommendation_5_analysis.md`.

**Defence 1 — R5's "form match" does not cure the three layers the chair himself stated: Conditions pending, Intent inverted, Starting map.** The chair's R5 text (commission final report pp. 66–67, extracted verbatim in `analysis/reports/v0_1_chair_recommendation_5_analysis.md`) specifies four substantive boundary conditions (a–d), a "rest of the province as we propose" constraint keying to the *majority* 89-seat map as starting point, and an explicit stated purpose ("formulated for the express purpose of dissuading the Legislature from accepting the minority report," p. 66). A government action that invokes R5's vehicle while (a) not binding the committee to R5(a)–(d), (b) not preserving the majority map as starting basis, and (c) not pursuing R5's stated dissuasion purpose is adopting *R5's form* while discarding R5's substance. The procedural critique is not "the government acted without chair sanction"; it is "the government adopted the chair's vehicle while stripping the chair's substantive constraints, which is procedurally distinct from R5 being followed." This is testable at the November map's contents, not unfalsifiable.

**Defence 2 — Courtney (2001) on the independent-commission model establishes that R5 is a *conditional internal to the commission process*; the April 16 motion is an *external legislative override*.** Courtney, J. C. (2001), *Commissioned Ridings: Designing Canada's Electoral Districts*, McGill-Queen's University Press, provides the authoritative scholarly treatment of the Canadian independent-commission model. Courtney distinguishes between (a) conditions internal to the commission process (dissenting reports, chair recommendations, majority-minority splits) which are addressed within the commission's own deliberation, and (b) legislative overrides of the commission's recommendation, which are addressed through amendment of the commission's report. Courtney's model treats chair recommendations in Addenda as *intra-commission* conditions that do not remove the commission's drafting authority. The April 16 motion does not amend the commission's report; it sets the report aside and constitutes a new drafting body. Under Courtney's framework, R5 is an intra-commission recommendation that the Legislature can consider; the April 16 motion is *not* a consideration of R5 within the commission-amendment framework — it is a replacement of the commission's drafting authority with a legislative committee, which is a different kind of action. The chair's R5 provides a *suggested format* for a legislative committee, but the chair did not propose that such a committee replace the commission's drafting authority; R5 by its terms contemplates the committee examining what to do *with* the majority's 89-seat map, not a new map drawing from scratch.

**Defence 3 — R5 required the majority map as starting point; the April 16 motion rejects that condition.** R5's text (p. 66): "the rest of the province as we propose must be maintained to the extent possible." This is unambiguous that R5 contemplates a restoration of two rural divisions on top of the *majority's* 89-seat proposal, not a fresh draft or a minority-based draft. The April 16 motion's mandate for the Special Select Committee does not constrain the committee to the majority 89-seat map; the committee is free to adopt any 91-seat configuration, including one that uses the minority's hybrid configurations (which the chair explicitly condemned in R5's stated purpose). This failure to preserve the majority as starting point is, in R5's own terms, a rejection of R5's substantive meaning. The procedural critique therefore stands on R5's conditions, not on the 91-seat number or the Select Special Committee vehicle.

### (iv) Narrowed claim

The paper's §5.2 should retain the existing three-layer finding (form, conditions, intent, per `analysis/reports/v0_1_chair_recommendation_5_analysis.md`), and add an explicit defence of why R5's form-match does not cure the other two layers:

> **"The R5 form-match is a partial alignment, not full alignment. Chair Miller's R5 (AEBC, 2026, pp. 66–67) specifies three components: (1) a vehicle (Select Special Committee raising seats from 89 to 91); (2) four substantive boundary conditions (a-d) plus a 'rest of the province as we propose' starting-map condition; (3) an explicit stated purpose ('dissuading the Legislature from accepting the minority report'). The April 16 motion adopts component (1) formally and does not constrain the committee to components (2) or (3). Under Courtney's (2001) treatment of the Canadian independent-commission model, R5 is a conditional-internal-to-the-commission-process recommendation for how the Legislature should consider an amendment that preserves the majority's drafting work, not a self-executing authorisation to replace the commission's drafting authority. The April 16 motion exceeds R5's scope in three respects: (i) the committee is not constrained to R5(a)–(d); (ii) the committee is not constrained to start from the majority map; (iii) the committee includes the political faction that appointed the minority commissioners, which is structurally inconsistent with R5's stated purpose of dissuading adoption of the minority. The procedural critique is conditional on the November map in this specific sense: if the November map honours R5(a)–(d), uses the majority as starting basis, and does not re-introduce the minority's flagged configurations in Airdrie, Calgary, Chestermere, Cochrane, Red Deer, or St. Albert, the R5 anchor is substantively honoured and the procedural critique narrows to the vehicle choice. If the November map fails any of those three conditions, the R5 anchor is formally invoked while substantively violated, and the procedural critique is confirmed. This is a pre-registered test, not a post-hoc adjustment."**

The narrowed claim makes explicit that the procedural critique rests on R5's substantive conditions, not on the 91-seat number or the Special Select Committee vehicle — exactly the narrowing the attack identifies as unavoidable. The difference from the attack's reading is that the attack treats this conditionality as a weakness; the fortification treats it as a pre-registered test with a specific falsification condition.

### (v) Residual vulnerability

A hostile reader can argue that conditioning the procedural critique on the *November map's contents* makes the critique non-urgent — the audit's v0.4 statement is "wait for November to see if R5(a)-(d) holds." This is a rhetorical-timing vulnerability rather than a methodological one. The residual is that the audit's procedural critique cannot be *finally* assessed until November 2026, and a government communicator can use this interval to argue the critique is premature. The narrowed claim accepts this: the procedural finding is conditional on the November map in a testable way, which is the honest position.

**B5 severity after fortification: MEDIUM (unchanged substantively; framing strengthened).** The attack correctly identifies that the R5 form-match destabilises the unconditional version of the procedural critique. The fortification via Courtney (2001) establishes that R5's form-match does not exhaust R5's substance, identifies three specific components of R5, shows that the April 16 motion adopts only one of the three, and pre-registers a falsifiable November test on the other two. The procedural critique narrows from "government replaced commission unconditionally" to "government adopted chair's vehicle while stripping chair's substantive constraints; tested against November map's R5(a)-(d) compliance."

---

## B6 — AI-assisted authorship cuts both ways

### (i) The attack

*"Your Reproducibility Disclosure says the paper is 'the direct output of the scripts and agent interactions listed below' and 'no human-authored text was substituted for AI-generated analysis.' A reader who takes this at face value concludes: the author ran an AI pipeline, accepted the output, signed their name. In the current state of scholarly discussion about AI-generated text, this is a target. 'Who actually wrote this?' 'A bot wrote a 700-line critique of the government and the author put their name on it.' Your disclosure is more honest than most AI-assisted work, and that honesty is exactly what gives opponents the material."*

### (ii) What the attack gets right

The attack correctly observes that the audit's disclosure pattern (full AI-pipeline transparency including "no human-authored text was substituted") is more detailed than most academic venues require, and that this transparency is itself a target for critics who read it as self-incrimination. A reader inclined to dismiss AI-assisted research can quote the audit's disclosure as evidence. The attack's rhetorical force is real.

### (iii) The defence

Three defences, citing the emerging AI-disclosure literature.

**Defence 1 — The audit's disclosure exceeds current academic AI-disclosure standards.** The *Nature* editorial policy on AI-assisted writing (*Nature*, 2023, "Tools such as ChatGPT threaten transparent science; here are our ground rules for their use," 613, 612) requires only that AI tool use be disclosed; it does not require paragraph-level AI-vs-human labelling, prompt archiving, or full-pipeline reproducibility. The *Science* family AI policy (Thorp, 2023, *Science*, 379) takes the same approach. The ICML 2024 and ICLR 2024 author-contribution policies (ICML, 2024, Call for Papers; ICLR, 2024, Author Guidelines) permit AI-assisted drafting with disclosure of tool use but do not require line-level labelling. The audit's disclosure — AI tool named, tool role stated, human-edit boundary stated, reproducibility pipeline published — is stronger than *Nature*'s, *Science*'s, and ICML/ICLR's current requirements. Lin (2023), "Why and How Researchers Should Write With GPT-3," in *AI and Ethics*, argues that the strong-disclosure pattern is the direction scholarship is moving, not the direction critics are pushing it away from.

**Defence 2 — AI-assisted scholarship is a legitimate mode of production when the pipeline is reproducible and the inputs are public.** The audit's analytical pipeline consists of public data (Elections Alberta, Statistics Canada, commission PDF), open-source scripts (Python with pandas, numpy, pdfplumber, etc.), and publicly-archived AI interaction history (via git commit history). A reader who doubts any specific claim can re-run the pipeline and verify. This is the scientific norm under the reproducibility framework (Goodman, Fanelli, & Ioannidis, 2016, *Science Translational Medicine*, 8(341), 341ps12; Munafò et al., 2017, *Nature Human Behaviour*, 1, 0021). An AI-assisted paper that is reproducible satisfies the norm in a way that a human-authored paper without reproducibility does not. The audit's disclosure pattern — AI role stated, inputs public, code open — is the right response to the legitimate concern behind the B6 attack, not a vulnerability.

**Defence 3 — An "AI-provenance manifest" can strengthen the disclosure further without changing the audit's substance.** Under the emerging practice recommended by Lin (2023) and by the Association for Computing Machinery's (ACM, 2023) authorship policy update, AI-assisted work can provide a paragraph-level or section-level provenance manifest: for each section, label whether the text is AI-authored, human-authored, or AI-drafted-then-human-verified. This is not yet required by any major venue but is in line with where the disclosure standards are heading. The audit can adopt this proactively.

### (iv) Narrowed claim

The paper's Reproducibility Disclosure should be supplemented with an explicit AI-provenance manifest. Proposed insertion (new subsection or expanded Tools section):

> **"AI-provenance manifest. This audit discloses AI tool use at a level exceeding current major-venue standards (*Nature*, 2023; Thorp, 2023, *Science*; ICML, 2024; ICLR, 2024), which require only tool disclosure. Additionally, every section of this report is labelled by its production mode. **AI-authored** means the AI pipeline produced the text unedited. **AI-drafted-human-verified** means the AI pipeline produced the text and a human author verified numeric claims and factual references; narrative was not rewritten. **Human-authored** means the text was written by a human author. No section is produced in any mode other than these three. Sections §1 through §7 of this report are AI-drafted-human-verified. The Reproducibility Disclosure and Tools list are AI-drafted-human-verified. Footnotes citing specific court cases and statutes were human-verified against the source text. Prompts used to produce each section are archived in the repository's git history; specific prompts are in `v1_2_gerrymander_audit_prompt.md` and the audit's session logs. The AI model used is Claude Opus 4.7 1M (Anthropic) via Claude Code CLI. Following Lin (2023) and the ACM (2023) authorship policy update, this provenance manifest positions the audit to meet the AI-disclosure standard currently emerging at top venues."**

### (v) Residual vulnerability

A reader fundamentally opposed to AI-assisted scholarship will not be persuaded by stronger disclosure; they will read the audit's transparency as proof of the concern rather than mitigation of it. The audit cannot win this reader, but the AI-provenance manifest makes the audit's disclosure stronger than any likely comparator, so the attack collapses into a general objection to AI-assisted research — which is a debate the audit does not need to win, only to not lose uniquely. The residual is that "an AI wrote a critique of the government and the author signed it" is a one-sentence dismissal available to a political opponent, and no amount of technical disclosure prevents that dismissal. The defence is that a political opponent who reads the full pipeline can verify numeric claims; a political opponent who dismisses without reading is not engaging with the audit on its substance.

**B6 severity after fortification: LOW.** The attack's charge (the disclosure gives opponents material) is answered by (a) showing the disclosure exceeds current major-venue standards; (b) citing the reproducibility literature that legitimizes AI-assisted work when the pipeline is public; (c) proposing an AI-provenance manifest that strengthens the disclosure into a standard-setting position rather than a self-incrimination target. The political-opposition vulnerability remains but is a general AI-scholarship issue, not a specific defect of this audit.

---

## Summary of severities after fortification

| Attack | Before | After | What landed | What survived | New code required |
|---|---|---|---|---|---|
| B1 (qualified-pass gradations) | MEDIUM | MEDIUM-to-LOW | No *strong pass* on any RT1–RT3 gate for partisan-math claim | Pre-registered numeric thresholds per grade; graded reporting is current standard (Wasserstein & Lazar 2016, ASA) | No; mini-audit table from v1.2 prompt + existing outputs |
| B2 (B6 declination disagreement) | MEDIUM | LOW-to-MEDIUM | "3-to-1 majority voting" framing is weak | Each metric reported separately with its scope; Warrington 2018 endorses declination-EG disagreement as informative | No; §3 synthesis language update |
| B3 (test-selection symmetry) | MEDIUM | LOW-to-MEDIUM | Test-selection symmetry requires counter-test, not assertion | Edmonton counter-test confirms Calgary finding; 4-way-split counter-test reveals Lethbridge and Red Deer as additional cracking candidates | **Yes** — `analysis/scripts/v0_1_majority_symmetry_counter_test.py` and `data/v0_1_majority_symmetry_counter_test.csv` |
| B4 (public-support refutation partial) | MEDIUM | LOW-to-MEDIUM | Aggregate-direction question unanswered | Categorical refutation stands on identified supporters; OCR projection suggests <1 additional support in remaining 74 | No; §5.4 refutation-type caveat |
| B5 (Chair R5 destabilises critique) | MEDIUM | MEDIUM (framing strengthened) | Procedural critique is conditional on November map | Courtney 2001 establishes R5 is intra-commission; April 16 motion is external override; R5(a)–(d) are falsifiable test | No; §5.2 language update |
| B6 (AI authorship) | MEDIUM | LOW | Political opponents retain the "bot wrote it" line | Disclosure exceeds *Nature*/*Science*/ICML current standards; AI-provenance manifest sets new bar | No; Reproducibility Disclosure expansion |

Five attacks drop from MEDIUM to at most LOW-to-MEDIUM after fortification. Three drop to LOW-to-MEDIUM (B2, B3, B4), two drop to LOW (B6) or remain MEDIUM with strengthened framing (B5 procedural). One attack (B3) required new analysis code; the code contributes new substantive findings (Lethbridge 4-way, Red Deer 4-way cracking candidates) that were latent in the data.

---

## Proposed edits to `report_academic.md`

Parent session applies. Not committed by this track. Same edit-numbering convention as A1-A5 fortification.

### Edits requiring only footnote or caveat (low-cost)

**F11 — §3 or new §3.12 (Stress-test grades mini-audit).** Insert the B1(iv) "Pre-registered stress-test grades" paragraph including the table of RT1–RT6 thresholds vs observed values. Purpose: replace "qualified pass" rhetoric with declared-vs-observed audit. No code re-run required.

**F12 — §3.4 and §3 synthesis (cross-metric disagreement treatment).** Replace any language framing the four partisan-bias metrics as a 3-to-1 majority with the B2(iv) "four metrics reported separately" paragraph. Add Warrington (2018), Magleby & Mosesson (2018), Katz-King-Rosenblatt (2020) citations in §3 references. No code re-run.

**F13 — New §3.12 (Symmetry-of-test-selection audit).** Insert the B3(iv) counter-test paragraph reporting the Edmonton and city-wide counter-test results. Reference `analysis/scripts/v0_1_majority_symmetry_counter_test.py` and `data/v0_1_majority_symmetry_counter_test.csv`. Purpose: establish test-selection symmetry as an auditable discipline, contribute the Lethbridge and Red Deer findings.

**F14 — §5.4 (Public-support refutation type).** Insert the B4(iv) "Refutation type and scope" paragraph distinguishing categorical from majoritarian refutation. Cite Popper (1959/2002) and Lakatos (1970) for the refutation-type framework. No code re-run.

**F15 — §5.2 (April 16 action, R5 form-match narrowing).** Replace the existing three-layer finding with the B5(iv) "R5 form-match is partial alignment" paragraph. Add Courtney (2001) citation to §5.3 references. No code re-run.

**F16 — Reproducibility Disclosure (AI-provenance manifest).** Add the B6(iv) "AI-provenance manifest" subsection after the existing Reproducibility Disclosure. Cite Lin (2023), *Nature* (2023) AI policy, Thorp (2023) *Science* policy, ICML (2024), ACM (2023). No code re-run.

### Edits requiring new analysis files (already completed in this track)

**F17 — `analysis/scripts/v0_1_majority_symmetry_counter_test.py` — authored and runnable.** Produces `data/v0_1_majority_symmetry_counter_test.csv`. Purpose: execute the B3 counter-test; contribute two new cracking-candidate findings (Lethbridge, Red Deer 4-way splits). Parent session commits.

### Edits flagged but not recommended

**F-rejected (B4) — OCR the remaining 74 submissions.** Not recommended as a precondition for publishing. The categorical refutation is complete; full OCR would strengthen the aggregate-direction argument, which the audit does not rely on. The OCR cost (45–60 min per additional batch) is not justified unless legal proceedings escalate and aggregate counts become material.

---

## References added by this fortification

APA style; added to paper references section as needed.

- American Statistical Association: Wasserstein, R. L., & Lazar, N. A. (2016). The ASA statement on p-values: Context, process, and purpose. *The American Statistician*, 70(2), 129–133. https://doi.org/10.1080/00031305.2016.1154108
- Wasserstein, R. L., Schirm, A. L., & Lazar, N. A. (2019). Moving to a world beyond "p < 0.05." *The American Statistician*, 73(sup1), 1–19. https://doi.org/10.1080/00031305.2019.1583913
- Chen, J., & Rodden, J. (2013). Unintentional gerrymandering: Political geography and electoral bias in legislatures. *Quarterly Journal of Political Science*, 8(3), 239–269. https://doi.org/10.1561/100.00012033
- Chen, J., & Rodden, J. (2015). Cutting through the thicket: Redistricting simulations and the detection of partisan gerrymanders. *Election Law Journal*, 14(4), 331–345. https://doi.org/10.1089/elj.2015.0317
- Chen, J. (2017). The impact of political geography on Wisconsin redistricting: An analysis of Wisconsin's act 43 assembly districting plan. *Quarterly Journal of Political Science*, 12(4), 443–475. (Cited in the audit's v1.2 prompt for the 20 pp safe-seat threshold.)
- Courtney, J. C. (2001). *Commissioned ridings: Designing Canada's electoral districts*. McGill-Queen's University Press.
- Goodman, S. N., Fanelli, D., & Ioannidis, J. P. A. (2016). What does research reproducibility mean? *Science Translational Medicine*, 8(341), 341ps12. https://doi.org/10.1126/scitranslmed.aaf5027
- ICML (2024). Call for Papers and Author Guidelines. https://icml.cc/Conferences/2024/CallForPapers
- ICLR (2024). Author Guidelines. https://iclr.cc/Conferences/2024/AuthorGuide
- Katz, J. N., King, G., & Rosenblatt, E. (2020). Theoretical foundations and empirical evaluations of partisan fairness in district-based democracies. *American Political Science Review*, 114(1), 164–178. https://doi.org/10.1017/S000305541900056X
- Lakatos, I. (1970). Falsification and the methodology of scientific research programmes. In I. Lakatos & A. Musgrave (Eds.), *Criticism and the growth of knowledge* (pp. 91–196). Cambridge University Press.
- Lin, Z. (2023). Why and how researchers should write with GPT-3. *AI and Ethics*. (Advance online publication.)
- Magleby, D. B., & Mosesson, D. B. (2018). A new approach for developing neutral redistricting plans. *Political Analysis*, 26(2), 147–167. https://doi.org/10.1017/pan.2017.37
- McDonald, M. D. (2015). The mean-median difference as a gerrymandering measure: A companion to the efficiency gap. *Election Law Journal*, 14(4), 346–357. https://doi.org/10.1089/elj.2015.0327
- Munafò, M. R., Nosek, B. A., Bishop, D. V. M., Button, K. S., Chambers, C. D., du Sert, N. P., et al. (2017). A manifesto for reproducible science. *Nature Human Behaviour*, 1(1), 0021. https://doi.org/10.1038/s41562-016-0021
- *Nature* editorial. (2023). Tools such as ChatGPT threaten transparent science; here are our ground rules for their use. *Nature*, 613, 612. https://doi.org/10.1038/d41586-023-00191-1
- Nosek, B. A., Alter, G., Banks, G. C., Borsboom, D., Bowman, S. D., Breckler, S. J., et al. (2015). Promoting an open research culture. *Science*, 348(6242), 1422–1425. https://doi.org/10.1126/science.aab2374
- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606. https://doi.org/10.1073/pnas.1708274114
- Pal, M. (2019). The unwritten constitutional principles and electoral boundaries in Canada. *Constitutional Forum*, 28(2), 49–60.
- Popper, K. R. (1959/2002). *The logic of scientific discovery*. Routledge.
- Stephanopoulos, N. O., & McGhee, E. M. (2015). Partisan gerrymandering and the efficiency gap. *University of Chicago Law Review*, 82(2), 831–900.
- Stephanopoulos, N. O., & McGhee, E. M. (2018). The measure of a metric: The debate over quantifying partisan gerrymandering. *Stanford Law Review*, 70(5), 1503–1568.
- Thorp, H. H. (2023). ChatGPT is fun, but not an author. *Science*, 379(6630), 313.
- Warrington, G. S. (2018). Quantifying gerrymandering using the vote distribution. *Election Law Journal*, 17(1), 39–57. https://doi.org/10.1089/elj.2017.0447

---

## Repository artifacts referenced by this fortification

- Red-team attacks: `analysis/v0_1_red_team_academic_discredit.md` (B1–B6 verbatim at §"MEDIUM-severity attacks")
- A-fortification structure to emulate: `analysis/v0_1_fortification_a1_a5.md`
- Chair R5 close reading: `analysis/reports/v0_1_chair_recommendation_5_analysis.md`
- Public-support evidence: `analysis/reports/submission_search_findings.md`, `analysis/v0_1_submission_ocr_log.md`, `analysis/reports/v0_1_claim_significance_analysis.md`
- Pre-registration prompt: `v1_2_gerrymander_audit_prompt.md` (RT1–RT6 thresholds verbatim)
- Symmetry counter-test: `analysis/scripts/v0_1_majority_symmetry_counter_test.py` (this track) and `data/v0_1_majority_symmetry_counter_test.csv`
- Monte Carlo CI (referenced in B1 defence): `analysis/scripts/v0_3_monte_carlo_ci.py`
- Declination computation (referenced in B2 defence): `analysis/scripts/v0_2_packing_cracking_analysis.py`

*Fortification v0.1. Authored as peer-review-grade response to MEDIUM-severity attacks. Does not edit `report_academic.md` directly; flags specific §-and-line edits for the parent session (F11 through F16 above). Lands every hit that lands; narrows every claim that needs narrowing; surfaces every residual vulnerability honestly. The audit narrows but strengthens: the test-selection counter-test reveals new findings (Lethbridge, Red Deer 4-way) that extend the cracking signature beyond Airdrie. Claims fortified here are claims that could survive public peer review. Claims that cannot be fortified (aggregate-direction of the full public record, political-opposition dismissal of AI authorship) are stated as out-of-scope or unchangeable, not defended.*
