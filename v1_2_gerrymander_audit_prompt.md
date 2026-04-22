# Alberta Electoral Boundaries Audit — Claude Code Continuation Prompt v1.2

**Opus 4.7 1M context. 450,000 token budget (raise to 600K if Phase 4C Vision-on-VA-polygons is executed). 4-hour wall-clock budget.**

**Changes from v1.1.** Six execution-readiness gaps closed based on the readiness assessment (`analysis/v0_1_prompt_readiness.md`). PDF recon converted a Stage 3 unknown into a known constraint. RT gates now have numeric thresholds. Publication gate adds readability and house voice checks.

---

## System Directive

Claude Code at xhigh or max effort with Auto mode. Filesystem, autonomous execution, vision, web fetch. Write scripts to disk, run them, read outputs, compile results. The user reads the final report, not the intermediate steps.

**Role.** Lead quantitative political scientist running a non-partisan, evidence-based assessment. Apply identical detection methods symmetrically to all three maps. Every number in the final report has to pass a stage-based falsifiability gate and a stress-test gate.

**Core rule:** no number moves between steps without being provable. Every step also gets stress-tested before its output propagates.

---

## Known Constraints from Prior Recon

**The commission report PDF (pp 87–266, Appendix B) is prose, not tables.** Confirmed by direct inspection. It contains street-name-based boundary descriptions but no machine-readable VA→ED crosswalk. Stage 3a PDF crosswalk path is therefore not viable as a cheap extraction. Vision-on-maps (3c) is the primary path for 2026 attribution without shapefiles.

**Appendix C (pg 269) has the majority's hybrid-level crosswalk.** Extracted to `data/v0_1_majority_hybrid_crosswalk.csv`. Use this to verify hand-coded `MAJORITY_2026_MAPPING` entries; mismatches found in the v0.3→v1.2 pass (Airdrie-East and Medicine Hat-Brooks were `blend` but should be `direct`) have been corrected in `v0_2_packing_cracking_analysis.py`.

**Minority crosswalk is heuristic.** `data/v0_1_minority_hybrid_crosswalk.csv` was built by a data-acquisition sub-agent using name-matching (73 confident mappings, 16 new names, 14 unmapped out of 89 proposed EDs). Appendix E contains no tabular crosswalk equivalent to Appendix C; the minority file is approximate and should be flagged as such when used.

**2015 data is in the bundle.** `data/v0_1_alberta_2015_results.csv` with 87 pre-2017-commission EDs and NDP/PC/WRP/LIB totals. PC+WRP sums represent UCP-equivalent. RT3 (cross-election) now covers 2015/2019/2023 where boundary-mapping permits.

**Rural NDP range observed across three elections: 26.47% to 35.05%.** Monte Carlo rural_ndp_share range updated to Uniform(0.26, 0.36) in `v0_3_monte_carlo_ci.py`.

---

## Prior Work — Integrity Status (v1.2 baseline)

**Verified and reproducible:**
- `analysis/v0_2_packing_cracking_analysis.py` — symmetric three-map B1–B6. Hybrid mappings verified against Appendix C.
- `analysis/v0_3_monte_carlo_ci.py` — Monte Carlo CI, 2019 cross-check, 2015 range used for rural baseline.
- `analysis/electoral_forensics_population.py` — A1/A2/A3 + robustness check.
- `analysis/parse_2015_results.py` — 2015 election parser (parsed shares match official within 0.13 pp).
- `analysis/v0_1_cross_election_rural_baseline.py` — cross-election rural trend.
- `analysis/check_voice_and_readability.py` — voice + readability gate.
- `analysis/v0_1_poll_attribution_skeleton.py` — Phase 4C skeleton.
- `analysis/v0_1_bias_audit.md`, `v0_1_design_critique.md`, `v0_1_uncertainty_and_shapefile_impact.md`, `v0_1_prompt_readiness.md` — self-audits.

**Structural findings (vote-data-independent, survive stress-test):**

| Metric                               | Majority 2026 | Minority 2026 | Asymmetry           |
| ------------------------------------ | ------------- | ------------- | ------------------- |
| A1 MAD from provincial avg           | 3,180         | 4,707         | minority 48% wider  |
| A2 Calgary zone gap (geographic)     | +0.36%        | +12.20%       | minority much larger |
| A2 Calgary gap (2023-winner rule)    | +0.39%        | +7.71%        | same direction       |
| A3 s.15(2) invocations failing 3/5   | 1/3           | 1/3           | equal count, different severity |
| C3 visible anomalies (Calgary)       | 0             | 3             | minority 3 anomalies |
| C4 Airdrie split                     | 2 EDs         | 4 EDs         | minority double split |

**Vote-dependent findings (bracket from stress-test):**

| Metric (2023 votes, 70/30 central)   | 2019     | Majority | Minority | MC 95% CI asymmetry |
| ------------------------------------ | -------- | -------- | -------- | ------------------- |
| B2 Efficiency gap                    | −2.64%   | −0.85%   | −1.36%   | [−2.99, +0.76] pp   |
| B3 Mean-median                       | −2.22 pp | −0.18 pp | −0.33 pp | crosses zero        |
| B4 NDP @ 50/50                       | 46       | 44       | 42       | CI [−3, +1] seats   |
| B6 Declination                       | −0.034   | −0.021   | **−0.015** | disagreement       |

Red-team outcomes:
- **RT1 Monte Carlo 95% CI crosses zero.** Direction consistency 89.3%, qualified pass.
- **RT2 Declination disagrees with EG.** Qualified pass; magnitude claims require cross-metric disclosure.
- **RT3 2019 cross-check reverses direction** (+0.60 to +0.75 pp). Fail on magnitude stability.

**Reproducibility check first (Gate G0):**
```bash
python3 analysis/v0_2_packing_cracking_analysis.py
python3 analysis/electoral_forensics_population.py
python3 analysis/v0_3_monte_carlo_ci.py
python3 analysis/v0_1_cross_election_rural_baseline.py
python3 analysis/check_voice_and_readability.py
```

All five must run to completion with outputs matching the tables above. Gate G0 blocks downstream work if any number differs by more than 0.05 pp or one seat.

---

## Two-Gate Discipline (Integrity + Stress-Test)

Every stage has two gates. Integrity gate checks output matches inputs. Red-team gate checks a hostile expert would accept the finding. Publication requires both gates pass OR the weakness disclosed at the top of both reports.

Structural findings are reported as primary. Partisan-math findings are qualified by RT1–RT3 outcomes. Confidence levels attach to each claim based on which gates survived.

---

## Stress-Test Gates (v1.2, tightened thresholds)

### RT1 — Monte Carlo modeling uncertainty

**Check.** Run `v0_3_monte_carlo_ci.py` with N ≥ 2,000 samples.

**Numeric thresholds (new in v1.2):**
- 95% CI bounds both same sign: **strong pass**. Report as "measured asymmetry [lo, hi] pp, classical 95% significance."
- 90% CI bounds same sign, 95% crosses zero: **qualified pass**. Report as "directional claim at 90% confidence, 95% CI [lo, hi] pp crosses zero."
- 90% CI crosses zero: **fail**. Do not claim measurable magnitude. Report direction probability (percentage of same-sign samples) with no point estimate.
- Tie-breaker: if the zero-crossing CI touches zero within ±0.01 pp, count as crossing.

**Current status:** 95% CI [−2.99, +0.76] pp crosses zero; 89.3% direction consistency. **Qualified pass at ~90%.**

### RT2 — Cross-metric agreement

**Check.** Compute at least three partisan-bias metrics: B2 (EG), B3 (MM), B6 (declination).

**Numeric thresholds:**
- All three metrics produce same sign on majority-minority asymmetry: **strong pass**.
- Two of three same sign: **qualified pass**. Report each metric separately; no single synthesized magnitude.
- One or fewer same sign: **fail**. Do not claim a partisan-magnitude shift. Report each metric's value without synthesis.
- Tie-breaker: within ±0.005 (for declination) or ±0.1 pp (for EG/MM) of zero counts as neutral, not agreeing.

**Current status:** EG and MM both show minority more UCP-favorable (−0.51, −0.15 pp asymmetry). Declination shows opposite. **Qualified pass.**

### RT3 — Cross-election stability

**Check.** Run attribution methodology with 2019 votes as input. If boundary-mapping permits (2015 uses pre-2017 ED boundaries), also run 2015.

**Numeric thresholds:**
- Direction same across all election baselines: **strong pass**.
- Same direction but magnitude differs by >50%: **qualified pass** on direction, fail on magnitude.
- Direction flips across baselines: **fail on magnitude claim**. The finding partly reflects election-specific voter distribution.

**Current status:** 2023 asymmetry −0.51 pp; 2019 asymmetry +0.75 pp. **Direction flips. Fail on magnitude claim.** Direction is 2023-specific, not a stable map property.

### RT4 — Structural vs vote-based separation

**Check.** Before publication, classify each finding as structural or vote-based. No "consistency across N dimensions" claim that mixes them without labels.

**Pass condition.** Both reports contain clear separation. Current v0.3 reports do.

### RT5 — Independent test selection

**Check.** No test run and discarded. Every test's result reported. Logged in `analysis/test_log.md` if ambiguous.

**Pass condition.** Confirmed by agent self-report with audit trail in git history.

### RT6 — Assumption inventory and falsifiability

**Check.** Every load-bearing assumption in `analysis/v0_1_uncertainty_and_shapefile_impact.md` §4 listed. Blockers named.

**Pass condition.** Documented; review required on each new run to check new assumptions were added if new code was written.

---

## Defensibility Audit Gate (DA)

Before any number or characterization reaches a published report, it must pass a defensibility check. "Defensible" means: a hostile expert presented with the claim, the source data, and the derivation code should be unable to find a genuine factual fault. Interpretation can be argued; calculation and citation must be unassailable.

**DA1 — Trace.** Every numeric claim in either report traces to a specific script + data file combination. The combination is explicitly cited in the reproducibility manifest of the academic report (Appendix A). If a number appears in the reports but not in the manifest, add it or remove it — no orphans.

**DA2 — Recomputability.** Running the cited script on the cited data must reproduce the claimed number within ±0.05 percentage point or ±1 seat, whichever is applicable. Gate G0 in the pipeline enforces this. A failed DA2 check halts publication until the claim is reconciled or retracted.

**DA3 — Characterization provenance.** Every prose characterization (e.g., "engineered boundary," "materially wrong," "small but consistent") must either cite a specific observable feature of the data (with verbose description) or be labelled as an interpretation, conclusion, or inference. Interpretations can stand without hard provenance if they are labelled as such. Flat assertions cannot.

**DA4 — Speculative claim labelling.** Any claim whose evidentiary basis does not yet exist (e.g., 91-seat map analysis, future election outcomes, commissioner intent) must be labelled as speculation, preliminary, or inference, with a confidence level (HIGH / MEDIUM / LOW / SPECULATION) attached. Fail if a speculative claim is presented as a finding.

**DA5 — Legal-citation correctness.** Any court case, statute, or academic paper cited in the reports must be cited for its actual holding, not a related or superficially-similar proposition. Cross-check against authoritative summaries (for cases) or the paper's abstract (for academic work). A Pal (2015) citation used to support a gerrymandering claim where Pal (2015) is actually about party politics fails DA5.

**DA6 — Author bias disclosure.** If the author holds a known prior on the politics of the subject matter, the disclosure appears in both reports. Methodology must be designed to produce the same numbers regardless of author opinion, and at least one case where the numbers overruled the author's prior must be cited (a proof-of-discipline).

**DA7 — Alternative-framing acknowledgment.** For any claim whose interpretation depends on modeling choice or voter-geography assumption (Chen & Rodden natural packing, cross-election reversal, Monte Carlo CI), an alternative framing must be stated or explicitly considered in the relevant section. Suppressing a known alternative framing fails DA7.

**Gate behaviour.** Run the defensibility audit as the last step before Stage 6 report publication. If DA1–DA7 all pass, publish. If any fails, the claim is either revised to the defensible form or removed. No claim enters a published report in a state that fails DA1–DA7.

## Packing and Cracking Signature Revelation (required in Stage 6)

The audit must formally detect and reveal packing and cracking signatures wherever the analytical tests produce them. "Formally detect" means: state the criterion, state whether the criterion is met, name the specific zone that meets it, and name the specific zone that does not. No hedging the signature away in prose.

### Packing signature detection

A packing signature exists when a party's voters are concentrated into fewer, larger-than-average districts such that their excess votes are wasted. The detection criteria:

**P1.** A geographic zone of the map contains districts systematically larger than the provincial average (mean population ≥ provincial mean + 5%).

**P2.** The winning party in those districts wins them by margins larger than the provincial average winning margin (≥ 15 pp above mean district margin).

**P3.** The party losing those zoned districts has geographic concentration elsewhere such that its overall vote share would translate to more seats in an equally-populated zone configuration.

If all three are met, a packing signature is detected. If P1 and P2 are met but P3 cannot be verified, the signature is flagged as "provisional" — packing is suggested but not confirmed without a counterfactual.

**Required output in the academic report §B:** a subsection titled "Packing signatures detected" that lists every zone meeting the criteria, per map, with the specific numeric values each criterion produced. Zones that fail criteria are also named ("No packing signature detected in [zone] under [map]: P1 fails with [value]").

### Cracking signature detection

A cracking signature exists when a community's voters are split across more districts than geographic necessity requires, such that the community is a numerical minority in each district. The detection criteria:

**C1.** A contiguous municipality, First Nations territory, or recognized community of interest is divided across N districts, where N exceeds the number that would result from a single-centre-of-gravity assignment.

**C2.** In each of those N districts, the community's voters are a minority (below the winning margin for the district's political majority).

**C3.** The community's population is large enough that a single district could contain it with population within ±25% of provincial average.

If all three are met, a cracking signature is detected. C3 is the "was it necessary to split?" test. If C1 and C2 are met but the community is too large for a single district (C3 fails), the signature is "forced by population" rather than "engineered by cracking."

**Required output:** a subsection titled "Cracking signatures detected" with the same structure as the packing section.

### Engineered-boundary signature detection

A third signature type: boundaries drawn specifically to qualify for a rule or exception rather than to represent a community.

**E1.** The boundary passes through territory with negligible population (uninhabited land, water bodies, federal reserves) to reach a specific feature (province border, land-area threshold, etc.).

**E2.** Without that extension, the district would not qualify for the rule or exception it invokes.

**E3.** The extension does not serve a stated community-of-interest rationale in the commission's own justification.

If all three are met, an engineered-boundary signature is detected.

**Required output:** a subsection titled "Engineered-boundary signatures detected," listing each flagged district with the specific feature, the rule it qualifies for, and evidence from the commission's published rationale.

### Signature revelation reporting requirement

In every report (public, academic, HTML) the signatures detected for a map must be listed in a clearly-labelled "Signatures detected" section. The public report may use plain-language phrasings ("NDP-leaning Calgary districts are packed — minority map shows the signature, majority map does not") but the signature terminology must appear explicitly. Readers should not have to infer from prose that a signature was detected; they should see it named.

Where no signature is detected, the report says "no signature detected" plainly. The distinction between "not detected" and "not tested" is preserved.

## Publication-Readiness Gates (v1.2)

Additions beyond RT1-RT6:

### PR1 — house voice

**Check.** Run `python3 analysis/check_voice_and_readability.py`.

**Pass condition.** Exit 0 for both reports. No "not X — Y" mirror reversals, no emoji, no editorializing reactions, no templated triads.

**Current status:** Both reports PASS.

### PR2 — Readability

**Check.** Flesch-Kincaid approximation via `check_voice_and_readability.py`.

**Thresholds:**
- Public report: FKG ≤ 9.5 (target 9.0, tolerance +0.5)
- Academic report: FKG ≤ 13.5 (target 13.0, tolerance +0.5)

**Current status:** Public 7.1, Academic 11.7. **Both PASS with margin.**

### PR3 — Reproducibility manifest

**Check.** Every number in either report is traceable to a specific script + data file. Add a manifest at the bottom of the academic report listing each key number with its script/data origin.

**Pass condition.** Manifest written. Scripts named. Data files named. Line numbers where helpful.

### PR4 — Changelog from prior version

**Check.** If v1.2 execution produces numbers different from v1.1's carry-forward, changelog section at the top of both reports lists them.

**Pass condition.** Changelog written or explicit "no changes from v1.1 baseline" statement.

---

## Updated Stage Pipeline

Stage 0 through 6 from v1.1 with these refinements:

### Pre-Stage 3 (PDF Recon)
Download commission PDF to `.temp/` (gitignored). Recon:
1. Check Appendix B for machine-readable tables. **Known result: none.** Skip detailed reparse.
2. Extract Appendix C hybrid crosswalk to `data/v0_1_majority_hybrid_crosswalk.csv`. Verify `MAJORITY_2026_MAPPING` entries. Flag discrepancies.
3. Extract Appendix E (minority report text) for any minority-hybrid-specific language. Known result: TBD on next execution.
4. Report findings to `analysis/pdf_recon_log.md`.

### Stage 3 (VA-Polygon Attribution)

**Vision budget cap:** ≤ 800 VA centroid inspections total across both maps, concentrated on hybrid-adjacent VAs (interior VAs are trivially assigned by 2019-ED membership alone). At ~400 tokens per inspection, 320K tokens.

**Total Vote Checksum (tightened):**
- Per-party variance ≤ 0.1%: pass
- Joint variance ≤ 0.15%: additional check; catches offsetting errors
- Any variance > 1.0%: fail

### Stage 6 (Final Report)

Now runs PR1–PR4 as publication gates. Regeneration of both reports. house voice applied. Grade 9 for public report. Reproducibility manifest. Changelog section.

---

## Execution-Ready Validation Matrix

Before triggering, verify:

- [ ] Gate G0 passes: all 5 reproducibility scripts match carry-forward
- [ ] house voice checker exists and runs clean on current reports
- [ ] PDF recon pre-step runs successfully (needs internet)
- [ ] `data/v0_1_majority_hybrid_crosswalk.csv` exists and was verified
- [ ] `.gitignore` contains `.temp/` so PDF download doesn't get committed
- [ ] Sensitivity range for rural_ndp_share in `v0_3_monte_carlo_ci.py` is Uniform(0.26, 0.36) based on 2015/2019/2023 observed

If all above check: v1.2 can execute cold with no mid-run improvisation required on the items closed this session.

---

## Symmetry Discipline

Unchanged from v1.1. Every test applied identically to both 2026 proposals. Data gaps disclosed explicitly. No claim whose scope exceeds its data.

---

## Trigger

Begin Stage 0. Run through Stage 6 sequentially. Stop at any FAIL gate and report. Stage 6 requires RT1–RT6 and PR1–PR4 all passed or explicitly disclosed in-report.

At completion, report:
- Wall-clock spend
- Token spend
- Every integrity gate status (G0–G5, S0–S6)
- Every stress-test gate status (RT1–RT6)
- Every publication gate status (PR1–PR4)
- Confidence level attached to each reported claim
- Any files updated or created

---

*Prompt v1.2. Changes from v1.1:*

- *Pre-Stage-3 PDF recon task now embedded; Appendix B confirmed prose-only; Appendix C crosswalk saved as data asset*
- *RT1–RT6 numeric thresholds tightened with tie-breakers*
- *PR1 house voice check and PR2 readability check added as publication gates, with `check_voice_and_readability.py` implementation*
- *Vision budget explicit: ≤ 800 VA inspections at ~320K tokens*
- *Total Vote Checksum now also checks joint variance*
- *Rural baseline Uniform(0.26, 0.36) grounded in 2015/2019/2023 observed range*
- *Execution-Ready Validation Matrix at the bottom confirms readiness before triggering*

*Optimized for Opus 4.7 1M context with a 450K token budget and 4-hour wall-clock budget. Prior session executed v1.1 readiness assessment and closed four of six execution gaps; two remain (shapefiles release, submission-archive search), both external.*
