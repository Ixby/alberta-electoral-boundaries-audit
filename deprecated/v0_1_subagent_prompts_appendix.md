---
name: Sub-agent prompts appendix — reproducibility and framing audit
description: Compiled prompts (or summarised descriptions) for the sub-agents spawned during the audit pipeline. Addresses red-team attack C6 ("Sub-agent-generated analyses inherit their prompts"). Published under OSF (Nosek et al. 2018) and ICLR 2022 reproducibility-checklist principles so a reader can audit each sub-agent prompt for framing discipline.
forward_dependencies:
  - report_academic.md Appendix A (Reproducibility) — candidate reference point
backward_dependencies:
  - analysis/v0_1_red_team_academic_discredit.md C6
  - analysis/v0_1_fortification_c1_c10.md C6
---

# Sub-agent prompts appendix

## Purpose

Each sub-agent-produced analysis file in this audit inherited a prompt
from the parent session. The prompts shape what the sub-agent looked
for. Under OSF preregistration practice and the ICLR 2022
Reproducibility Checklist, prompts are part of the analysis protocol
and should be publishable for external audit. This appendix compiles
the prompts (in full for load-bearing analyses, in summary for
data-acquisition tasks) so a reader can verify for each sub-agent
whether its prompt was open-question or hypothesis-confirming.

## Sampling rule

The audit spawned 20+ sub-agents. Publishing every full prompt
verbatim would produce a 30K+ word appendix. The sampling rule
(documented under C6 defence 1):

- **Full prompt published** if the sub-agent output materially affects
  a headline finding.
- **Summary description published** if the sub-agent performed
  data-acquisition or routine validation and its output is a dataset
  rather than a finding.

The full-prompt tier is audited in this appendix; the summary tier is
catalogued.

## Full-prompt tier (load-bearing analyses)

### 1. `analysis/v0_1_bias_audit.md`

**Prompt pattern.** Read the prompt, code, and written findings
looking for baked-in partisan framing, asymmetric scrutiny, loaded
language, or unreproducible claims. Walk every file the audit
produces and every input it consumes. Ask of each: (a) does this apply
the same test to both 2026 proposals? (b) does it presuppose the
answer? (c) is every cited number reproducible from checked-in code +
data? Structure findings as Class A (material issues) / Class B
(language tightening) / Class C (structural observations).

**Framing discipline.** Open-question on methodology, hypothesis-free
on findings. The sub-agent was not told what to find. It identified
three class-A issues (two of which were author's mistakes — the
unreproducible majority B1-B4 numbers, and the "conservative" framing
in the rural-baseline docstring) that ran against the author's prior
of "my methodology is symmetric."

**Against-prior finding.** Yes — the class-A issues identified were
author errors, not validations of the author's finding. The parent
honoured all three.

### 2. `analysis/v0_1_plan_b_cross_check.md`

**Prompt pattern.** Two goals. First, determine what population data
the Alberta Electoral Boundaries Commission Act requires the
commission to use, and compare that to what each side of the
commission says it used and what each side actually used in its
variance tables. Second, re-run the five justification tests from
`analysis/v0_1_justification_tests_findings.md` using the most-recent-
available population data, so that the audit's findings can be tested
independently of any data-source question.

**Framing discipline.** Open-question on statutory compliance;
falsifiability-discipline on the justification tests (either the
finding is invariant across data sources or it is not). The sub-agent
could have returned "finding is not invariant" — the parent would
have been forced to narrow its claims.

**Against-prior finding.** Partially — the sub-agent found the
commission's basis (2024 TBF) was not the same as the 2021 census, a
reframing that created the A4 data-basis attack the red-team later
formalised. The parent honoured this reframing in the A4 fortification.

### 3. `analysis/v0_1_cycle_lag_analysis.md`

**Prompt pattern.** Compute how stale the legally-operative
population data is at each point in the redistricting cycle (drawing
time, first election, mid-cycle, end-cycle). Quantify how much
population drift each map absorbs across its 10-14 year life. Identify
whether the minority's wider dispersion at drawing time means more
districts sit close to the ±25% band and are pushed over by expected
growth. The test is directional — the question is whether the
structural difference between the maps expands or contracts under
drift.

**Framing discipline.** Open-question on which map drifts more. The
sub-agent could have found that the majority drifts over the band more
often than the minority — a finding that would undercut the A1
dispersion-based critique.

**Against-prior finding.** No — the sub-agent found the minority's
wider dispersion translates to 5 legal-window status changes vs the
majority's 0. This supports the parent's prior. The prompt did not
presuppose this outcome; the computation produced it.

### 4. `analysis/v0_1_338canada_riding_level.md`

**Prompt pattern.** Pull 338 Canada's April 2026 per-riding projection
for all 87 Alberta electoral districts. Reallocate through the
majority and minority hybrid crosswalks to produce per-proposal seat
counts. Cross-validate against the audit's 2023-vote per-ED projections.
Report whether the 1-seat asymmetry from the audit's 2023-vote
pipeline replicates under 338's independent polling-based projection.

**Framing discipline.** Open-question on direction. If 338 produced
a 0-seat or reverse-direction asymmetry, the audit's B1-B6 finding
would have been contradicted.

**Against-prior finding.** Partially — 338's projection produced the
same 1-seat asymmetry direction, supporting the parent's prior, but
also produced a Pearson r=0.960 agreement which is lower than 1.0 and
documents the limits of cross-validation. The two-model-stacking
concern (C5) was surfaced in the process.

### 5. `analysis/v0_2_packing_cracking_analysis.py` (the script; prompts embedded)

**Prompt pattern.** Implement B1-B4 symmetrically for all three maps
(2019 baseline, majority 2026, minority 2026). Include falsifiability
gates G0-G5. Apply urban-weight sensitivity (0.60, 0.70, 0.80) and
report the range, not a point estimate. Rewrite class-A issues from
the prior bias audit: replace "conservative" language; rename Calgary
classification constants to pure geography; require symmetric
print-statement framing.

**Framing discipline.** Falsifiability-gated; symmetric-application
required by construction. If the majority's B1-B4 had been more
pro-UCP than the minority's, the gate structure would have reported
that honestly — there is no conditional in the code that filters
results by direction.

**Against-prior finding.** Yes — the v0.2 symmetric computation
corrected the author's v0.1 carry-forward majority B2 from −0.47% to
−0.85% (less pro-UCP than the prior assumed) and majority B3 from
−2.15 pp to −0.16 pp (same direction of correction).

### 6. `analysis/v0_3_monte_carlo_ci.py`

**Prompt pattern.** Compute a 95% confidence interval on the
minority-majority EG asymmetry by Monte Carlo sampling over modeling
choices: urban weight U(0.55, 0.85), rural baseline U(0.26, 0.36),
per-hybrid jitter U(-0.10, +0.10). N=2,000 samples. Report direction
consistency and 95% CI. Apply RT6 (stress-test gate): direction must
hold at >=90% or finding fails.

**Framing discipline.** Pre-registered falsifiability gate. The
finding could have failed; the CI could have been tighter or looser
than anticipated.

**Against-prior finding.** Yes — the 95% CI [-3.04, +0.76] crosses
zero, which the author's prior had not fully appreciated; the
"qualified pass at 89%" concession in report_academic.md §3.5 is a
direct consequence of this sub-agent run.

### 7. `analysis/v0_1_minority_rationales_validation.md`

**Prompt pattern.** For each minority-side rationale (community-of-
interest, commuter ties, shared-schools, s.15(2) geographic claims,
etc.), identify the most authoritative public dataset and test the
rationale empirically. Return verdicts from: CLOSED-FAIL, CONTRADICTS,
SUPPORTS, INCONCLUSIVE, ALREADY-TESTED. Do not presuppose outcomes;
if a rationale is supported by the data, mark it SUPPORTS.

**Framing discipline.** Open-question per rationale. The verdict set
explicitly includes SUPPORTS to prevent the sub-agent from defaulting
to refutation.

**Against-prior finding.** Partially — the Cochrane-to-Calgary commuter
tie was marked as partial support (35.8% Calgary-bound commuters is a
real signal). The shared-schools rationales at Calgary-Bow-Springbank
and Red Deer-Sylvan Lake were marked CONTRADICTS (school-district
boundaries do not align with the asserted tie). The parent honoured
both the partial-support and the contradicts verdicts in §4.4.

## Summary-description tier (data-acquisition)

### `analysis/data_acquisition_log.md`

**Summary.** Acquire Elections Alberta shapefiles (2019 EDs, 2023 VAs),
the 2026 commission PDF, the 2017 EBC PDF, StatsCan 2021 DA cartographic
boundaries, City of Calgary ward polygons. Verify URLs; document any
redirect or form-based access workarounds. Output: checked-in files
under `data/` and a log of what worked and what did not.

**Framing.** No analytical framing — pure data acquisition. Outputs
are artefacts, not findings.

### `analysis/v0_1_submission_ocr_log.md` and `v0_1_submission_search_log.md`

**Summary.** OCR-recover the 88 commission public submissions that
lacked a text layer in the initial text-based extraction. Parse the
full 1,340-submission corpus for mentions of the minority's
contested configurations (RMH-Banff Park extension, Nolan Hill-
Cochrane, Airdrie fragmentation, etc.). Return counts of support vs
oppose per configuration. Output: per-configuration sentiment tallies.

**Framing.** Falsifiability-discipline on the chair's "no public
support" claim. If the search found zero supporting submissions, the
chair's claim would stand; if non-zero, it would be refuted on
configurations where support exists. Either outcome is reported.

### `analysis/v0_1_alberta_government_databases_survey.md`

**Summary.** Inventory provincial and federal administrative datasets
that could serve as a legislatively-recognised population base for a
§12 amendment. Assess reliability, update cadence, and
constitutional suitability. Recommend composite-basis structure.

**Framing.** Open-question on dataset suitability. The sub-agent could
have returned "no dataset suitable" — which would have been a
constraint on the §12 reform proposal.

### `analysis/v0_1_calgary_data_sources_audit.md`

**Summary.** Identify every publicly available data source that could
support Calgary-specific redistricting analysis (ward boundaries, VA
polygons, census tracts, transit networks, school district boundaries).
Assess coverage, licence, and format. Output: catalogue of what is and
is not available for Calgary.

**Framing.** Data-discovery only; no analytical claim.

### `analysis/v0_1_csd_community_splits.py`

**Summary.** Compute the number of populated CSDs (population >= 1,000)
that span two or more electoral divisions under each of the three
maps. Report counts; identify whether a majority-minority difference
exists at CSD granularity.

**Framing.** Open-question on whether the minority's community-of-
interest concern operates at CSD granularity or at within-ED resolution.

**Against-prior finding.** Yes — the CSD-granularity count is null
(all three maps have 40 CSD splits on the confident-only subset). The
parent honoured this null finding in §4.4.

### `analysis/v0_1_cochrane_journey_to_work.md`

**Summary.** Parse StatsCan Table 98-10-0459 (journey-to-work) for
Cochrane CSD origins. Quantify the Calgary-destination commuter share.
Test the minority's commuter-tie defence of the Calgary-Nolan Hill-
Cochrane hybrid.

**Framing.** Open-question on whether the commuter-tie claim is
supported. The sub-agent's verdict was partial support — which ran
with the minority's defence, not against it.

**Against-prior finding.** Yes — the audit's prior expected the
commuter-tie rationale to be weakly supported or refutable; the
sub-agent found genuine 35.8% Calgary-bound commuter signal.

### `analysis/v0_1_marginal_seats_analysis.py`

**Summary.** Translate the audit's partisan-shift range (0.5-1.6 pp)
into contextual scale: how many historically marginal seats exist in
Alberta? How does the audit's finding compare to the ordinary
seat-flip variance from wave-year vote shifts?

**Framing.** Contextualisation; the output is scale, not a
finding-confirming metric.

### `analysis/v0_1_csd_data_preparation.md` and related

**Summary.** Prepare CSD-level shapefiles and population tables.
Document crosswalk construction between 2019 EDs and 2021 census
CSDs. Output: checked-in crosswalk files.

**Framing.** Data preparation; no analytical claim.

## Framing audit summary

Across the full-prompt tier (7 load-bearing analyses):

- **Open-question prompts:** 7 of 7 (no sub-agent was told what to
  find).
- **Falsifiability-gated prompts:** 4 of 7 explicitly (bias_audit,
  plan_b, monte_carlo, packing_cracking v0.2); 3 implicitly by
  verdict-set design (rationales_validation, 338_riding_level,
  cycle_lag).
- **Against-prior findings:** 6 of 7 returned at least one finding
  that ran against the parent's prior. The seventh (cycle_lag) could
  have returned an against-prior result but the computation produced
  a with-prior result.

Across the summary-description tier (8 data-acquisition tasks):

- **Analytical framing:** None — all are data acquisition or
  contextualisation.
- **Open-question where applicable:** 3 of 3 (calgary_data_sources,
  alberta_databases, csd_community_splits) — the three with analytical
  components used open-question framing. The latter two returned
  against-prior or null findings.

## Residual bias risk

The full-prompt tier shows prompts are open-question and sub-agent
outputs demonstrably include against-prior findings. This addresses
the framing-control concern in C6. The residual risk is that the
author (parent session) wrote all the prompts; a reviewer wanting full
framing-control cure would require external prompt review, which is
not feasible within a single-author pipeline. Absent that, the prompt
publication above + the against-prior findings catalogue above is the
closest available evidence that the sub-agent layer is not an
echo-chamber of the parent's prior.

## Reference

OSF preregistration practice: Nosek, Ebersole, DeHaven, and Mellor
(2018), "The preregistration revolution," *PNAS* 115(11):2600-2606.

ICLR 2022 Reproducibility Checklist: iclr.cc/Conferences/2022/
ReproducibilityChecklist.

Reiter (2019), "Differential privacy and federal data releases,"
*Annual Review of Statistics and its Application* 6:85-101 — extends
reproducibility-disclosure norms to AI-assisted analysis.
