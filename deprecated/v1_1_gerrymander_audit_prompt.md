# Alberta Electoral Boundaries Audit — Claude Code Continuation Prompt v1.1

**Opus 4.7 1M context. 450,000 token budget. 4-hour wall-clock budget.**

**Changes from v1.0.** Red-team fortifications are now required, not optional. The v0.3 pass found three material weaknesses the original pipeline missed: Monte Carlo CI crosses zero, declination metric disagrees with EG, and 2019 cross-election check reverses the direction. v1.1 makes the tests that caught these mandatory and gates publication readiness on them.

---

## System Directive

Claude Code at xhigh or max effort with Auto mode. Filesystem, autonomous execution, vision, web fetch. Write scripts to disk, run them, read outputs, compile results. The user reads the final report, not the intermediate steps.

**Role.** Lead quantitative political scientist running a non-partisan, evidence-based assessment. Apply identical detection methods symmetrically to all three maps. Every number in the final report has to pass a stage-based falsifiability gate AND a red-team gate.

**Core rule:** no number moves between steps without being provable. Every step also gets red-teamed before its output propagates.

---

## Prior Work — Integrity Status (v0.3)

**Verified and reproducible:**
- `analysis/v0_2_packing_cracking_analysis.py` — symmetric three-map B1–B6 (now including declination); gates G1, G2, G5
- `analysis/v0_3_monte_carlo_ci.py` — Monte Carlo CI over modeling choices; 2019 cross-election check
- `analysis/electoral_forensics_population.py` — A1/A2/A3 with A2 robustness under two classifications; gate G3
- `analysis/v0_1_poll_attribution_skeleton.py` — Phase 4C skeleton, parse-stage gate
- `analysis/v0_1_bias_audit.md` — self-audit finding 3 class-A bias issues, all remediated in v0.2
- `analysis/v0_1_uncertainty_and_shapefile_impact.md` — shapefile-impact scenarios
- `analysis/v0_1_design_critique.md` — red-team pass, 25+ concerns documented

**Structural findings (vote-data-independent, survive red-team):**

| Metric                               | Majority 2026 | Minority 2026 | Asymmetry           |
| ------------------------------------ | ------------- | ------------- | ------------------- |
| A1 MAD from provincial avg           | 3,180         | 4,707         | minority 48% wider  |
| A2 Calgary zone gap (geographic)     | +0.36%        | +12.20%       | minority much larger |
| A2 Calgary gap (2023-winner rule)    | +0.39%        | +7.71%        | same direction       |
| A3 s.15(2) invocations failing 3/5   | 1/3           | 1/3           | equal count, different severity |
| C3 visible anomalies (Calgary)       | 0             | 3             | minority 3 anomalies |
| C4 Airdrie split                     | 2 EDs         | 4 EDs         | minority double split |

**Vote-dependent findings (weakened by red-team):**

| Metric (70/30 weight, 2023 votes)    | 2019     | Majority | Minority | MC 95% CI asymmetry |
| ------------------------------------ | -------- | -------- | -------- | ------------------- |
| B2 Efficiency gap                    | −2.64%   | −0.78%   | −1.36%   | [−3.14, +0.74] pp   |
| B3 Mean-median                       | −2.22 pp | −0.16 pp | −0.33 pp | crosses zero        |
| B4 NDP @ 50/50                       | 46       | 44       | 42       | CI [−3, +1] seats   |
| B6 Declination                       | −0.034   | −0.021   | **−0.015** | reversed direction |

Red-team outcomes:
- **Monte Carlo 95% CI crosses zero.** Direction consistency 89.3%, not 95% significance.
- **Declination disagrees with EG.** Minority is *least* pro-UCP by this metric.
- **2019 vote cross-check reverses.** Minority-majority asymmetry flips sign.

**Reproducibility check first:**
```bash
python3 analysis/v0_2_packing_cracking_analysis.py
python3 analysis/electoral_forensics_population.py
python3 analysis/v0_3_monte_carlo_ci.py
```

All three must reproduce the tables above. Gate G0 blocks downstream work if any number differs.

---

## The Two-Gate Discipline

Every stage now has two gates.

**Integrity gate:** does the output match the inputs correctly? Numbers reproducible, counts correct, no silent data loss. Covered in v1.0.

**Red-team gate:** would a hostile expert accept this finding? Covered in v1.1. Specific tests required below. If any red-team test shows a direction reversal or CI-crosses-zero, the finding's confidence is downgraded accordingly. The report writes what survives both gates as primary, what survives only integrity as secondary with the red-team caveat spelled out.

Publication readiness requires:
1. Every integrity gate passed (G0–G5, S0–S6)
2. Every red-team gate passed OR the weakness disclosed at the top of both reports
3. Structural findings separated from partisan-math findings
4. Confidence levels attached to each claim based on which gates survived

---

## Red-Team Gates (Mandatory in v1.1)

### RT1 — Monte Carlo modeling uncertainty

**Check.** Run `v0_3_monte_carlo_ci.py` with N ≥ 2,000 samples. Vary urban weight ∈ U(0.55, 0.85), rural baseline ∈ U(0.28, 0.38), per-hybrid jitter ±0.10.

**Pass condition.**
- 95% CI for minority-majority EG asymmetry does not cross zero: **strong pass**. Report at classical 95% significance.
- 90% CI does not cross zero but 95% does: **qualified pass**. Report as "directional claim at 90% confidence."
- 90% CI crosses zero: **fail**. Do not claim a measurable partisan shift. Report the direction probability (percentage of samples same-sign) without a magnitude.

**Current status:** 95% CI crosses zero (observed [−3.14, +0.74] pp); direction consistency 89.3%. Qualified pass at ~90%. v0.3 reports updated accordingly.

### RT2 — Cross-metric agreement

**Check.** Compute at least three partisan-bias metrics from the literature: efficiency gap (B2), mean-median (B3), declination (B6). Optional: partisan bias, GEO, lopsided margins.

**Pass condition.**
- All metrics show same direction (all pro-UCP or all pro-NDP for the majority-minority asymmetry): **strong pass**.
- Some metrics same direction, others neutral: **qualified pass**. Report each metric's direction; do not rely on any one.
- Some metrics reverse the direction: **fail for that specific magnitude claim**. Direction becomes unreliable; fall back to reporting each metric's value without synthesis.

**Current status:** EG, MM, B4 agree (minority more UCP-favorable). Declination reverses. Qualified pass; reported directionally.

### RT3 — Cross-election stability

**Check.** Run the same attribution methodology with votes from the previous election. For Alberta, that means 2019 votes as input to the 2026 maps, compared to 2023 votes.

**Pass condition.**
- Direction of the minority-majority asymmetry same in both elections: **strong pass**. Finding reflects map, not electorate.
- Different magnitudes but same direction: **qualified pass**. Magnitude is election-sensitive; direction is not.
- Direction flips between elections: **fail for the specific-election magnitude claim**. The finding partly reflects 2023-specific voter distribution, not a stable map property.

**Current status:** direction flips (2023 asymmetry −0.58 pp, 2019 asymmetry +0.60 pp). Fail. Partisan-math magnitude claim is 2023-specific; cannot be asserted as a stable property.

### RT4 — Structural vs vote-based separation

**Check.** Before publishing, classify each finding as structural (depends only on population and geography) or vote-based (depends on attribution modeling).

**Pass condition.**
- Structural findings are reported as primary with full confidence (pending their own integrity gates).
- Vote-based findings are reported with their RT1–RT3 confidence levels.
- The synthesis treats them separately. No combined "directional consistency across six dimensions" claim that mixes structural and vote-based dimensions unless each is labeled.

**Current status:** v0.3 reports implemented this separation.

### RT5 — Independent test selection

**Check.** Confirm the tests run were not chosen because they produced the expected finding.

**Pass condition.**
- Tests justified by prior literature (cite the paper).
- No test run and discarded without reporting its result.
- At least one test attempted where a null or contrary finding was a plausible outcome.

**Current status:** declination was added specifically to test the EG direction; it reversed. 2019 cross-check was added specifically to test 2023 specificity; it flipped. Both are reported. RT5 passes.

### RT6 — Assumption inventory and falsifiability

**Check.** Document every load-bearing assumption. For each, state what would invalidate it.

**Pass condition.** Every assumption in `analysis/v0_1_uncertainty_and_shapefile_impact.md` §4 is explicitly listed with validation status. Every ambiguity that is a blocker is named.

**Current status:** documented. RT6 passes. Two assumptions flagged as currently unsupported (no majority non-Calgary imagery; rural absorptions assumed = provincial rural average). Two ambiguities flagged as blockers (§A3 Canmore-Banff engineering, §D2 no-public-support claim verification).

---

## Updated Stage Pipeline

Stage 0 through 6 from v1.0 apply unchanged, with RT1–RT6 added at Stage 6 as publication gates.

### Stage 6 — Final Report Update (v1.1 revision)

Before writing the report, confirm all red-team gates have been run. Include their results at the top of both Public/Media and Academic/Legal reports in a "Red-Team Findings" or "Important Honesty Note" section.

**Public/Media edition.** Grade 9 reading level. Wuff voice (plain, grounded, conversational; no "not X — Y" reversals; no templated triads; no emoji; no editorializing reactions). Structural findings primary. Partisan-math findings qualified by RT1–RT3 outcomes. Red-team disclosure at the top, not buried.

**Academic/Legal edition.** Full technical detail. Wuff voice at technical register. Red-team findings in a dedicated section up front. Synthesis separates structural from vote-based dimensions. Falsifiability statement lists what would invalidate the headline.

Required additions if RT1–RT3 produce qualified passes or fails:
- Disclose the qualified-pass confidence level explicitly (e.g., "89% directional consistency, not classical 95% significance").
- Disclose cross-metric disagreement where it exists (e.g., "declination metric reversed the direction of the EG finding").
- Disclose cross-election sensitivity where it exists (e.g., "using 2019 votes as the attribution baseline flips the sign").
- State the most-defensible claim that survives all red-team results.

### Publication Readiness Checklist (v1.1)

- [ ] All Stage S0–S6 integrity gates passed or failure disclosed
- [ ] RT1 Monte Carlo run with N ≥ 2,000, confidence level attached to any magnitude claim
- [ ] RT2 At least three partisan-bias metrics computed; agreement or disagreement reported
- [ ] RT3 Cross-election check performed; direction flip disclosed if present
- [ ] RT4 Structural findings separated from vote-based in both reports
- [ ] RT5 Test selection rationale documented
- [ ] RT6 Assumption inventory and blockers list current
- [ ] Wuff voice applied to both reports
- [ ] Public report at grade 9 reading level (verify with readability score)
- [ ] Red-team disclosure at top of both reports, not buried
- [ ] Migration MD written for the next chat

---

## Symmetry Discipline

Unchanged from v1.0. Every test applied identically to both 2026 proposals. Data gaps disclosed explicitly. No claim whose scope exceeds its data.

---

## Token and Wall-Clock Budget

Unchanged from v1.0. 450K tokens, 4 hours. Per-phase sub-caps (Stage 5 ensemble ≤ 100K).

---

## Trigger

Begin Stage 0. Run through Stage 6 sequentially. Stop at any FAIL gate and report. Stage 6 requires RT1–RT6 all passed or explicitly disclosed in-report.

At completion, report:
- Wall-clock spend
- Token spend
- Every integrity gate status
- Every red-team gate status
- Confidence level attached to each reported claim
- Any files updated or created

---

*Prompt v1.1. Changes from v1.0: Red-team gates RT1–RT6 made mandatory at Stage 6. Structural vs vote-based separation required in synthesis. Qualified-pass/fail framework for partisan-math magnitude claims. Wuff voice and grade 9 reading level specified for Public/Media edition. Prior session (v0.3, Chat 4) executed red-team pass and found three material weaknesses that are now addressed in baseline methodology.*
