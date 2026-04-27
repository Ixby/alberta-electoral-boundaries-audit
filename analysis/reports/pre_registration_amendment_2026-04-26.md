---
name: Pre-registration amendment — 2026-04-26
description: Documents methodology evolution and test-result revisions to the audit's retrospective component (RQ1–7) made between the 2026-04-23 amendment and 2026-04-26. The pre-registered prospective component (RQ8–9) — the 17-test grid that will be applied to the November 2026 Lunty committee map — is unchanged.
type: project
---

# Pre-registration amendment — 2026-04-26

**Registration:** Pre-registered signature-detection checklist for the Alberta MLA Special Select Committee's 91-seat electoral boundary map.
**Author:** Will Conner.
**Original upload:** 2026-04-23, 06:22 PM MT (OSF Registrations).
**Prior amendment:** `pre_registration_amendment_2026-04-23.md` (changes 1–6, weight parameter corrections + AI toolstack disclosure + DPG sunset clause).
**This amendment filed:** 2026-04-26.
**Reason for amendment:** Eleven changes to the retrospective component (RQ1–7) made between the 2026-04-23 amendment and 2026-04-26. Bucket A: five additive enhancements that do not change pre-registered hypotheses or thresholds. Bucket B: five test-result revisions where post-pre-registration evidence changed a published finding. Bucket C: status of the prospective component (RQ8–9) — unchanged.

This amendment is filed in advance of any public republication of the audit, in keeping with the audit's pre-registration discipline. The pre-registration explicitly anticipated retrospective methodology evolution between the registration date and the November 2026 committee map's release (§1, "This registration is mixed: retrospective for RQ1–7, prospective for RQ8–9"); this amendment documents what evolved.

---

## Bucket A — Additive enhancements (no hypothesis change)

These changes strengthen the evidentiary basis of pre-registered tests without altering test definitions, thresholds, or hypotheses. They are documented for transparency.

### Change 1 — MCMC ensemble enlargement: 100,000 → 2,000,000 maps

**Location:** §2 Component 3 (Simulation methodology).

**Before:** *"A Markov Chain Monte Carlo ensemble of 100,000 randomly drawn, legally valid Alberta boundary plans (GerryChain ReCom, ±25% population window, contiguity constraint, seed 42) provides a reference distribution."*

**After:** *"A Markov Chain Monte Carlo ensemble of 2,000,000 randomly drawn, legally valid Alberta boundary plans (GerryChain ReCom, ±25% population window, contiguity constraint, seeded run sequence 42 → 44 → 88) provides a reference distribution. The audit ran the ensemble at progressively larger sizes (100,000 → 250,000 → 1,000,000 → 2,000,000 maps); each enlargement produced the same percentile placements within ±0.5 percentile points, and the 2,000,000-map run is the authoritative reference distribution. Doubling from 1M to 2M did not push the simulation's most extreme `seats@50/50` value any higher (51.72% in both runs), evidencing convergence on the ceiling rather than sampling thinness."*

**Reason:** Larger sample sizes give tighter confidence intervals on the same percentile-rank tests. The pre-registered cutoffs (p95 outlier; rank-among-N positioning) are unchanged. ESS (effective sample size) at the 2M run is 3,138–4,347 across the four metrics, 4× the 1M run, well above publication-grade thresholds in the academic redistricting literature.

**Outputs:** `data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv`, `data/v0_1_mcmc_real_map_scores_250k_v0_8.json`, `data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.json`, `data/mcmc_checkpoints_250k_v0_8/chain{0–3}_samples.csv`, `analysis/reports/v0_1_mcmc_2M_v0_8_full.log`.

---

### Change 2 — Targeted-gerrymander short-bursts test added

**Location:** new §2 Component 4 (Adversarial-procedure test).

**Added:** *"A short-bursts hill-climbing procedure (Cannon, Goldbloom-Helzner, Gupta, Matthews, Suwal 2022, 'Voting Rights, Markov Chains, and Optimization by Short Bursts') was run with the explicit objective of maximising UCP seats at neutral votes, while staying inside the same statutory constraints as the neutral ensemble. Method: 800 bursts × 50 ReCom steps each (40,000 total steps), with each burst's most-UCP-favouring partition selected as the seed for the next burst. Purpose: empirically test whether a non-neutral but legal procedure can reach the minority map's `seats@50/50` territory (which the neutral 2M ensemble cannot)."*

**Reason:** This addresses the methodological caveat that ReCom samples have a known bias toward compact maps; the targeted procedure tests whether the minority's territory is reachable by non-neutral means. *Result:* 52.87% best `seats@50/50` reached in 40,000 steps — within rounding of the minority map's 52.8%. This is supplementary evidence; it does not replace any pre-registered test.

**Outputs:** `analysis/scripts/targeted_gerrymander_burst.py`, `data/targeted_burst_best.json`, `data/targeted_burst_trace.csv`, `analysis/reports/v0_1_targeted_burst.log`.

---

### Change 3 — Rural-representation analysis added

**Location:** new §3 supplementary analysis (Lane 2 context).

**Added:** A comparative analysis of how each of the three real maps (2019 enacted, 2026 majority, 2026 minority) handles rural representation. Computes: per-voter representation weight (rural / urban) under each map; number of section 15(2) special-rural EDs declared; rural ED average population vs ideal; hybrid ED count and population profile.

**Reason:** Pre-empts the strongest rhetorical defence of the minority map's hybrid pattern (the rural-protection-via-hybridization argument articulated in the minority commissioners' Appendix E pp. 302–303). The analysis is supplementary to the pre-registered structural tests; it does not replace any of them.

**Outputs:** `analysis/scripts/rural_protection_test.py` and a new section in `report_public.md` ("The rural-representation question").

---

### Change 4 — 89-of-89 inheritance-fill attribution + fuzzing scenarios

**Location:** §11 B5 (Seats at tied vote, methodology).

**Before:** Spatial-join VA centroids into v0_8-reconstructed polygons; report `seats_at_50_50` over polygons that catch ≥1 centroid (yielding 87 measurable EDs for majority, 83 for minority).

**After:** Same primary attribution; for the 6 minority-map and 2 majority-map polygons that are inheritance-fill slivers and catch no VA centroids, fill votes from each district's *inherited 2019 polygon* (the same geometry the v0_8 reconstruction already uses for those EDs), producing a defensible 89-of-89 attribution. Headline number revises from 54.2% (45 of 83 measurable) to **52.8% (47 of 89)**. A fuzzing-scenario analysis (5 attribution strategies + 10,000 random-attribution trials) brackets the result between 51.7% (worst case) and 57.3% (best case); 89% of trials place the minority above the 2M-ensemble's 51.72% ceiling.

**Reason:** Defensibility improvement on the same metric. The pre-registered hypothesis (the minority map produces an outlier `seats_at_50_50` value relative to the simulation distribution) is unchanged; the attribution is more rigorous. Both the historical 54.2% (83 of 89) reading and the new 52.8% (89 of 89) reading are preserved in the monograph for traceability.

**Outputs:** `analysis/scripts/fuzz_missing_eds.py` and §5.4.7 of `report_academic.md`.

---

### Change 5 — Geometry transition v0_7 → v0_8 (full coverage)

**Location:** §4 Methods, geometry pipeline.

**Before:** Audit used v0_7 canonical polygons (67 of 89 EDs measurable for majority and minority — partial coverage).

**After:** Audit uses v0_8 full-coverage polygons (89 of 89 EDs for both maps via 2019-Tier-A inheritance fill for districts whose 2026 boundaries the commission's published images did not let the audit reconstruct directly). Wherever Phase 4F validation flags an over-extended polygon (e.g., the v0_8 minority's "Peace River" polygon), the disclosure remains in `data/INTEGRITY_STATUS.md`.

**Reason:** v0_8 did not exist at the original pre-registration date. Using v0_8 over v0_7 is methodological improvement, not hypothesis change. The DPG sunset clause from the 2026-04-23 amendment continues to apply (with the duration revision noted in Change 11 below): all geometry-dependent metrics will be recomputed against Elections Alberta's official 2026 shapefiles within two weeks of release.

---

## Bucket B — Test-result revisions (post-evidence changes that need explicit documentation)

These changes affect what specific findings the audit reports. They are properly documented as evidence-driven revisions, not silent edits.

### Change 6 — Lethbridge rationale removed (rationale-validity test: "six of seven" → "five of six")

**Location:** Pre-registered rationale-validity test (S6 in the 17-test grid).

**Before:** The rationale-validity test reported "six of seven contested minority-commissioner rationales fail under independent check," with the seventh (St. Albert-Sturgeon) classified as constraint-forced.

**After:** The rationale-validity test reports "five of six contested minority-commissioner rationales fail under independent check," with the sixth (St. Albert-Sturgeon) classified as the constraint-forced configuration. The previously included Lethbridge–Taber-Warner federal-boundary claim has been removed from the test.

**Reason:** A methodology deep-dive (`analysis/methodology/lethbridge_federal_boundary_check.md`) determined that the minority report does not actually make a federal-boundary claim anywhere — there is no underlying primary source for the rationale the audit had attributed to it. Per the audit's standing inclusion criterion (a rationale is included only if it can be traced to a primary-source minority-report citation), the claim has been removed rather than left as a weak finding. The denominator-and-numerator change ("six of seven" → "five of six") is itself a more defensible reporting standard than retaining a claim with no traceable source.

---

### Change 7 — Banff Park rationale: "zero residents/zero ranches" softened

**Location:** Pre-registered rationale-validity test, Banff sub-claim.

**Before:** *"The extended polygon contains zero year-round residents and zero working ranches."*

**After:** *"The Canada National Parks Act prohibits agricultural tenure on park land, and a polygon-clipped 2021-Census-DA pull on the Banff extension finds no documented year-round-resident population in the strict park-land slice."*

**Reason:** Methodology file `banff_extension_population_check.md` ran a polygon-clipped DA-population pull and found ~491 area-weighted residents in the Banff extension polygon (not zero). The "no working ranches" claim is statutorily entailed by the *Canada National Parks Act* but not separately verified for adjacent Crown-land grazing-lease territory. The framing is updated to reflect what the evidence actually supports. The rationale-validity verdict ("Fail") is unchanged — the substantive finding holds; only the precision of the underlying claim is corrected.

---

### Change 8 — Cross-election direction retracted under v0_8 full coverage

**Location:** §1 Risk-of-influence mitigation point #3, "disclosed contradicting findings" item (b).

**Before:** *"the minority's partisan-direction signal reverses under 2019 vote inputs."*

**After:** *"under v0_8 full-coverage area-proportional attribution, three of four metrics (efficiency gap, declination, seats@50/50) hold direction across 2019 and 2023 votes; only mean-median flips, and the v0_8 ensemble places mean-median sub-threshold for both maps. The earlier 'direction reverses' finding from v0_7 partial coverage is retracted as a partial-coverage artefact (22 unattributed rural EDs whose UCP votes were systematically excluded). The audit retains 'partisan-bias magnitude depends on vote distribution' but retracts the stronger 'direction reverses under 2019 votes' caveat."*

**Reason:** The cross-election finding originally reported under v0_7 partial coverage was the third of three "findings that ran against the prior" disclosed prominently in the pre-registration. Re-running under v0_8 full coverage materially changed the result: the direction-flip was a partial-coverage artefact, not a property of the underlying maps. The retraction is filed openly. The original v0_7 finding is preserved in the historical record (monograph §5.2.3); the v0_8 result is the current authoritative reading.

---

### Change 9 — St. Albert-Sturgeon "stands" verdict: evidentiary basis updated

**Location:** Pre-registered rationale-validity test, St. Albert-Sturgeon sub-claim.

**Before:** *"With the population-deviation rule and the Edmonton-corridor commute geography, no other configuration satisfies both the community-of-interest and the ±25% rule simultaneously."*

**After:** *"The majority map and the minority map independently arrive at the same St. Albert-Sturgeon two-district structure under the Act's constraints. When two independent drafting teams converge on the same configuration, the configuration is constraint-forced rather than engineered."*

**Reason:** The original framing was a counterfactual non-existence claim ("no other configuration satisfies") that was not formally proven by ensemble extraction. Methodology file `st_albert_sturgeon_constraint_search.md` documents that the convergence-test framing ("both maps converge on this") is empirically observable and stronger evidentially than the unproven non-existence claim. The verdict ("Stands") is unchanged; the evidentiary basis is more defensible.

---

### Change 10 — Alberta-calibrated ~5% line added alongside the pre-registered US 7% line

**Location:** §3 Pre-registered tests, S4 (Efficiency gap).

**Before:** S4 reports the efficiency gap relative to the US 7% threshold from *Whitford v. Gill*.

**After:** S4 reports the efficiency gap relative to **two reference lines**: (a) the pre-registered US 7% line from *Whitford v. Gill*, and (b) the ~5% Alberta-calibrated line, derived from the 95th percentile of the audit's MCMC-ensemble efficiency-gap distribution (empirical value 4.37%, rounded up to 5% in public-facing reporting to avoid spurious decimal precision on a partly-subjective cutoff). Both lines are reported for both 2026 maps and the 2019 baseline.

**Reason:** Additional reference line, not a replacement. The pre-registered S4 hypothesis (the minority map crosses the relevant efficiency-gap threshold) is reported against both lines. The minority map exceeds both 5% and 7%; the majority exceeds 5% but not 7%. Reporting against both is more transparent than reporting against either alone.

---

### Change 11 — Sunset-clause window relaxed: 48 hours → two weeks

**Location:** Appendix A (DPG sunset clause), and `report_academic.md` §4.1.4, §5.2.7, abstract block, executive summary.

**Before:** *"The audit commits to: 1. Re-running all DPG-dependent analyses against the official shapefiles within 48 hours of public release."*

**After:** *"The audit commits to: 1. Re-running all DPG-dependent analyses against the official shapefiles within two weeks of public release."*

**Reason:** The original 48-hour window is achievable only with a built-out automation pipeline (continuous monitoring of Elections Alberta release endpoints, automated ingest, re-run, and disclosure). Such a pipeline is on the audit's roadmap but not yet built. A 48-hour commitment from a solo researcher with no automation in place is unrealistic — it would be honoured if the release happens during a clear week and broken if it lands during travel, illness, or any of the ordinary delays that affect any individual researcher. A two-week window covers both the automated and the manual case honestly, and is in line with practice in academic redistricting research. The recompute commitment itself, the requirement to publicly disclose any sign-flip or magnitude change > 0.5pp, and the symmetric application to whichever measurement currently favours the audit's interpretation, are unchanged. The audit will tighten the window if and when the automation pipeline is operational; until then, two weeks is the honest commitment.

---

## Bucket C — Prospective component (RQ8–9): unchanged

The 17-test grid (S1–S6, W1–W3, P1–P5, X1–X3) that will be applied to the November 2026 Lunty committee map is **unchanged from the 2026-04-23 amendment**. All numeric thresholds (10% Calgary zone gap, 4-way Airdrie split, p95 ensemble outlier, US 7% efficiency gap, four R5 conditions) are unchanged. The 72-hour scoring commitment after the November map's release is unchanged.

The only addition affecting the prospective component: the ~5% Alberta-calibrated line (Change 10) will be reported alongside the pre-registered US 7% line for S4 on the November map. This is additive disclosure, not a replacement of the pre-registered test.

---

## Summary

| # | Bucket | Section | Nature | Effect on findings |
|---|---|---|---|---|
| 1 | A | §2 Component 3 | Enhancement — MCMC ensemble enlargement (100k → 2M) | None; tighter precision on same percentile cutoffs |
| 2 | A | §2 new Component 4 | Addition — short-bursts targeted-procedure test | Supplementary evidence; no pre-registered test replaced |
| 3 | A | §3 supplementary | Addition — rural-representation analysis | Supplementary; pre-empts rhetorical counter-argument |
| 4 | A | §11 B5 | Enhancement — 89-of-89 inheritance-fill attribution | Same metric, more defensible attribution; revises 54.2% → 52.8% |
| 5 | A | §4 Methods | Enhancement — v0_7 → v0_8 geometry | Methodological improvement; DPG sunset clause unchanged |
| 6 | B | S6 (rationale validity) | Test-result revision — Lethbridge claim removed | "Six of seven" → "five of six"; defensibility improvement |
| 7 | B | S6 (Banff sub-claim) | Test-result revision — "zero residents/ranches" softened | Verdict ("Fail") unchanged; framing more accurate |
| 8 | B | §1 mitigation #3 | Retraction — cross-election direction-flip | Original v0_7 finding retracted; v0_8 result authoritative |
| 9 | B | S6 (St. Albert sub-claim) | Test-result revision — evidentiary basis updated | Verdict ("Stands") unchanged; convergence framing more defensible |
| 10 | B | §3 S4 | Addition — Alberta-calibrated ~5% line | Additive; pre-registered US 7% line still reported |
| 11 | B | App. A sunset clause | Window relaxation — 48 hours → two weeks | Honesty-of-commitment correction; recompute commitment itself unchanged |
| 12 | C | §3 Prospective (RQ8–9) | No change | The November-map test grid is the contract; intact |

No pre-registered hypotheses, scoring rules, or data inclusion/exclusion criteria for the prospective (RQ8–9) component were changed. The retrospective component (RQ1–7) evolved as documented above; all evolution is traceable to either methodological improvement (Bucket A) or evidence-driven test-result revision (Bucket B), with cited methodology files for each.

The audit's standing commitments hold: (a) the 17-test grid will be applied without modification to the November 2026 Lunty committee map within 72 hours of release; (b) all geometry-dependent metrics will be recomputed against Elections Alberta's official 2026 shapefiles within two weeks of release (revised from 48 hours per Change 11), with any sign-flip or magnitude change >0.5pp publicly disclosed in a dated amendment.
