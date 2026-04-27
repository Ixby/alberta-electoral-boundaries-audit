---
name: analysis/ Restructure Inventory
description: Per-file category assignments for the three-way split of analysis/ into scripts/, reports/, methodology/. PO-approved 2026-04-23.
type: methodology
---

# analysis/ Restructure Inventory

**Prepared:** 2026-04-23 for PO review of Gemini Proposal 1 (segregate `analysis/` into `scripts/`, `reports/`, `methodology/`).
**PO approval:** Full plan (Phases A + B + C) approved 2026-04-23 per PO response.
**Authoritative source for execution.** This inventory's per-file category assignments must be used verbatim by the restructure pipeline.

---

## Summary

- **Total files in `analysis/` (top-level only, .py + .md, excluding `red_team/` subfolder and `__pycache__/`):** 142
- **Scripts** (executable Python pipelines): 60 → `analysis/scripts/`
- **Reports** (findings / public output): 31 → `analysis/reports/`
- **Methodology** (frameworks / internal audits / red-team docs): 49 → `analysis/methodology/`
- **Ambiguous**: 2 (see Table 4 for resolutions)

Zero-reference files (safe move, Phase A): 12.
3+ incoming-reference files (coordinated move, Phase C): 15.
Largest individual-file rewrite surface: `shape_refinement.py/.md` at 140 incoming refs each.

---

## Table 1 — Scripts (60 files → `analysis/scripts/`)

| Filename | Purpose | Incoming refs |
|---|---|---|
| shape_refinement.py | Core shapefile refinement pipeline | 140 |
| packing_cracking_analysis.py | Gerrymandering detection via packing/cracking metrics | 114 |
| mcmc_ensemble.py | ReCom MCMC ensemble simulation for baseline gerrymandering test | 101 |
| submission_search.py | OCR and full-text search over boundary submission documents | 83 |
| monte_carlo_ci.py | Monte Carlo CI computation for partisan-bias metrics | 68 |
| chen_rodden_alberta.py | Chen-Rodden partisan bias decomposition analysis | 58 |
| assignment_prep.py | Phase 4C preparation pipeline (vote attribution setup) | 48 |
| build_pdf.py | Compiles analysis outputs into final PDF report | 46 |
| check_voice_and_readability.py | Editorial QA: voice consistency + readability scoring | 45 |
| 338canada_reallocate.py | 338Canada polling data reallocation to 2026 ED boundaries | 45 |
| build_cover.py | Generates cover page and front matter for report PDF | 43 |
| mcmc_full_coverage_rescore.py | MCMC ensemble rescoring with 100% geographic coverage | 37 |
| canadian_base_rate_compute.py | Computes baseline partisan bias from Canadian historical cycles | 36 |
| generate_overlay_figures.py | Boundary comparison overlay-map generator (v2) | 33 |
| mcmc_ensemble_100k.py | Extended MCMC ensemble run with 100k samples | 30 |
| 338canada_scraper.py | Scrapes and parses 338Canada polling data | 29 |
| mcmc_full_coverage_rescore_100k.py | Full-coverage MCMC rescore at 100k iterations | 28 |
| csd_community_splits.py | Community separation analysis via school-district boundaries | 26 |
| chen_rodden_decomposition.py | Geography-vs-drawing decomposition of Chen-Rodden metric | 25 |
| build_canonical_shapefiles.py | Authoritative canonical-shapefile compilation pipeline | 24 |
| shape_refinement_v2.py | Shapefile refinement v2 iteration | 24 |
| shape_refinement_v3.py | Shapefile refinement v3 iteration | 22 |
| shape_refinement_v4.py | Shapefile refinement v4 iteration (major revision) | 22 |
| build_full_crosswalks.py | 2019→2026 boundary-change crosswalk builder | 21 |
| 2015_cross_election.py | Cross-election comparison with 2015 Alberta election | 20 |
| shape_refinement_v5.py | Shapefile refinement v5 iteration | 20 |
| simulation_multichain_ensemble.py | Multi-chain variant of MCMC ensemble with Gelman-Rubin | 19 |
| approximate_shape_analysis.py | Geometric analysis of approximate boundary proposals | 19 |
| generate_article_figures.py | Figure generation for article (v3) | 18 |
| canadian_base_rate_recalibrate.py | Recalibration of Canadian base-rate computation | 18 |
| 338canada_historical.py | Historical polling archive from 338Canada | 18 |
| overlap_zone_diagnostic.py | Diagnostic analysis of boundary overlap zones | 18 |
| mcmc_full_coverage_rescore_v2.py | MCMC full-coverage rescore v2 refinement | 17 |
| advance_vote_splat.py | Vote-Anywhere apportionment (ED→VA splat) | 16 |
| justification_tests.py | Statistical tests validating boundary-design claims | 16 |
| majority_symmetry_counter_test.py | Partisan-symmetry test (counter-example case) | 15 |
| cross_election_rural_baseline.py | Rural-area baseline comparison across elections | 15 |
| build_overlay_figures.py | Initial boundary-comparison overlay-map generator | 14 |
| build_composite_shapefiles.py | Composite shapefile assembly from parts | 14 |
| refine_boundaries.py | Shapefile refinement v6 (production version) | 13 |
| shape_refinement_v6_processors.py | v6 refinement modular processor components | 12 |
| airdrie_overlap_diagnostic.py | Airdrie-specific boundary-overlap analysis | 12 |
| electoral_forensics_population.py | Population-equality A1/A2/A3 audit framework | 11 |
| rural_gap_dissection.py | Rural-urban voting-gap component analysis | 11 |
| shape_refinement_v6_writer.py | v6 refinement output writer module | 10 |
| edmonton_beaumont_polygon.py | Edmonton-Beaumont specific boundary polygon work | 10 |
| marginal_seats_analysis.py | Swing-seat vulnerability analysis | 10 |
| track_l_drift.py | Track L: post-implementation boundary drift detector | 9 |
| a1_legal_baseline_2021_census.py | Legal-compliance baseline from 2021 census | 9 |
| phase_4bcdef_execution.py | Phases 4B–4F audit execution pipeline | 8 |
| plan_b_rerun.py | Alternative plan (Plan B) recomputation | 8 |
| edmonton_beaumont_split.py | Edmonton-Beaumont split analysis | 7 |
| poll_attribution_skeleton.py | Phase 4C poll-location vote-attribution framework | 6 |
| parse_2015_results.py | 2015 Alberta election results parsing | 5 |
| assignment_va_attribution.py | Phase 4C voting-area attribution pipeline | 5 |
| submission_ocr.py | OCR processing of scanned submission documents | 5 |
| submission_ocr_analyze.py | Analysis of OCR-extracted submission text | 4 |
| url_archival.py | Wayback Machine archival of submission URLs | 3 |
| build_academic_html.py | HTML compilation for academic output format | 2 |

---

## Table 2 — Reports (31 files → `analysis/reports/`)

| Filename | Purpose | Incoming refs |
|---|---|---|
| pre_registration_draft.md | Formal pre-registration protocol | 33 |
| consistency_audit.md | Consistency audit of applied-vs-stated methods | 29 |
| track_c_checklist_baseline_scoring.md | Track C compliance-checklist baseline scores | 27 |
| chair_recommendation_5_analysis.md | Analysis of Chair Recommendation #5 implications | 18 |
| plan_b_cross_check.md | Cross-check of alternative boundary plan (Plan B) | 16 |
| submission_search_findings.md | Key findings from submission-document search | 7 |
| 2015_cross_election_analysis.md | Cross-election comparison findings (2015 vs 2019) | 6 |
| airdrie_overlap_report.md | Airdrie boundary-overlap incident findings | 6 |
| marginal_seats_findings.md | Swing-seat vulnerability report | 5 |
| rural_gap_findings.md | Rural-urban voting-gap analysis findings | 4 |
| justification_tests_findings.md | Results of statistical validation tests | 4 |
| claim_significance_analysis.md | Statistical significance of key audit claims | 3 |
| 91_seat_preliminary.md | Preliminary analysis of 91-seat proposal | 3 |
| bias_audit.md | Partisan-bias detection findings | 3 |
| assignment_gerrymander_comparison.md | Phase 4C gerrymandering-metric comparison | 2 |
| design_critique.md | Design critique of electoral-division structure | 2 |
| byelection_assessment.md | By-election impact assessment | 2 |
| act_amendment_proposal.md | Proposed amendments to Electoral Divisions Act | 2 |
| ai_use_recommendations_for_committee.md | Recommendations for AI use in committee deliberations | 2 |
| pre_registration_amendment_2026-04-23.md | Amendment to pre-registration protocol (dated) | 1 |
| pre_registration_platform_analysis.md | Analysis of pre-registration implementation platform | 1 |
| va_spatial_integrity_report.md | Voting-area spatial-data integrity assessment | 0 |
| article_figures_v3.md | Figure captions and methodology for article (v3) | 0 |
| approximate_shape_analysis.md | Geometric-analysis narrative for approximate proposals | 0 |
| vote_anywhere_report.md | Mobile/advance-voting impact assessment | 0 |
| section_A_population_equality.md | Report section: population-equality audit | 0 |
| section_C_geographic_coherence.md | Report section: geographic-coherence audit | 0 |
| section_D_procedural.md | Report section: procedural-compliance audit | 0 |
| section_4_geometry_provenance.md | Report section: shapefile-source provenance | 0 |
| terms_of_reference_audit.md | Audit against commission's stated terms of reference | 0 |
| chen_rodden_decomposition.md | Geography-vs-drawing decomposition results writeup | 11 |

---

## Table 3 — Methodology (49 files → `analysis/methodology/`)

| Filename | Purpose | Incoming refs |
|---|---|---|
| red_team_consolidated.md | Consolidated red-team cross-examination document | 123 |
| mcmc_ensemble.md | MCMC ensemble methodology and results narrative | 101 |
| shape_refinement.md | Master shapefile-refinement methodology | 140 |
| mcmc_100k_and_full_coverage.md | MCMC 100k run + full-coverage rescore narrative | 18 |
| s15_2_reaudit.md | Section 15.2 re-audit methodology and findings | 18 |
| science_red_team_design_and_stats.md | Red-team critique of study design and statistics | 15 |
| canadian_base_rate_computed.md | Canadian baseline computation methodology | 15 |
| appendix_c_legal_baseline.md | Legal-baseline appendix (Appendix C) | 12 |
| 338canada_riding_level.md | 338Canada riding-level data documentation | 12 |
| science_red_team_data_priorart_peerreview.md | Red-team critique of data sources and prior art | 11 |
| data_preparation.md | Data-preparation methodology and pipelines | 11 |
| sign_convention_resolution.md | Resolution of sign-convention issues | 10 |
| shape_refinement_v4.md | Shapefile refinement v4 methodology | 10 |
| overlay_figures_v2.md | Boundary-overlay figure-generation v2 narrative | 9 |
| v0_1_majority_symmetry_counter_test.md | Partisan-symmetry test counter-case narrative | 9 |
| science_red_team_reproducibility_and_falsifiability.md | Red-team critique of reproducibility framework | 9 |
| alberta_government_databases_survey.md | Survey of available Alberta government databases | 9 |
| 338canada_historical.md | 338Canada historical-polling archive documentation | 9 |
| csd_community_splits.md | Community-split analysis via school divisions | 9 |
| canonical_shapefile_log.md | Canonical-shapefile build log and QA | 8 |
| canonical_shapefile_methodology.md | Canonical-shapefile construction methodology | 8 |
| chen_rodden_alberta_validation.md | Validation of Chen-Rodden metric for Alberta | 8 |
| commission_source_provenance.md | Commission reference-data source-provenance audit | 8 |
| commission_reference_shapes.md | Commission-provided reference-shapefile documentation | 8 |
| boundary_transcription.md | Manual-boundary digitization methodology | 8 |
| submission_search_log.md | Full-text-search implementation log | 7 |
| v0_1_mcmc_full_coverage_rescore.md | Full-coverage MCMC-rescore narrative | 7 |
| assignment_execution_log.md | Phase 4C execution log and notes | 7 |
| composite_shapefiles_log.md | Composite-shapefile compilation log | 6 |
| build_overlay_figures.md | Overlay-figure generation methodology | 6 |
| academic_literature_review.md | Academic literature review on gerrymandering | 5 |
| shape_refinement_v2.md | Shapefile refinement v2 methodology | 5 |
| shape_refinement_v3.md | Shapefile refinement v3 methodology | 4 |
| shape_refinement_v5.md | Shapefile refinement v5 methodology | 4 |
| shapefile_redteam_report.md | Red-team critique specific to shapefiles | 4 |
| assignment_runbook.md | Phase 4C step-by-step runbook for execution | 3 |
| cochrane_journey_to_work.md | Cochrane geography / journey-to-work analysis | 3 |
| calgary_data_sources_audit.md | Calgary-specific data-source audit | 3 |
| minority_rationales_validation.md | Validation of minority-scenario justifications | 3 |
| minority_rationales_inventory.md | Inventory of minority-scenario design rationales | 3 |
| terms_of_reference_verbatim.md | Commission's terms of reference (verbatim copy) | 2 |
| school_division_coherence.md | School-division geographic-coherence analysis | 2 |
| uncertainty_and_shapefile_impact.md | Uncertainty quantification and sensitivity analysis | 1 |
| threshold_provenance.md | Population-threshold documentation | 1 |
| urban_weight_defense.md | Defense of urban-weighting methodology | 1 |
| reproducibility_verification.md | Reproducibility-verification checklist | 1 |
| editorial_pass_log.md | Editorial-review log | 0 |
| tier_c_pixel_audit.md | Tier C pixel-level boundary audit | 0 |
| 338canada_integration.md | 338Canada data-integration methodology | 0 |
| restructure_inventory.md | This file — permanent record of the restructure decisions | 0 |

---

## Table 4 — Ambiguous cases (already resolved)

| Filename | Target | Alternative | Reasoning |
|---|---|---|---|
| master_plan.md | **methodology/** | reports/ | Functions as audit-framework/timeline; master-plan meta-doc. |
| plan_b_cross_check.md | **reports/** | methodology/ | Presents findings first (cross-check results); method is secondary. |

---

## Table 5 — Highest-risk cross-references (15 files with ≥ 3 incoming refs)

| Filename | Category | Incoming refs | Risk |
|---|---|---|---|
| shape_refinement.py | scripts | 140 | CRITICAL |
| shape_refinement.md | methodology | 140 | CRITICAL |
| packing_cracking_analysis.py | scripts | 114 | CRITICAL |
| mcmc_ensemble.py | scripts | 101 | CRITICAL |
| mcmc_ensemble.md | methodology | 101 | CRITICAL |
| submission_search.py | scripts | 83 | HIGH |
| monte_carlo_ci.py | scripts | 68 | HIGH |
| chen_rodden_alberta.py | scripts | 58 | HIGH |
| assignment_prep.py | scripts | 48 | HIGH |
| build_pdf.py | scripts | 46 | HIGH |
| check_voice_and_readability.py | scripts | 45 | HIGH |
| 338canada_reallocate.py | scripts | 45 | HIGH |
| build_cover.py | scripts | 43 | HIGH |
| mcmc_full_coverage_rescore.py | scripts | 37 | MEDIUM |
| canadian_base_rate_compute.py | scripts | 36 | MEDIUM |

---

## Zero-reference files (Phase A safe-move set, 12 files)

All reports/ or methodology/ with 0 incoming refs — safe to move first:

1. `va_spatial_integrity_report.md` (reports)
2. `article_figures_v3.md` (reports)
3. `approximate_shape_analysis.md` (reports)
4. `vote_anywhere_report.md` (reports)
5. `section_A_population_equality.md` (reports)
6. `section_C_geographic_coherence.md` (reports)
7. `section_D_procedural.md` (reports)
8. `section_4_geometry_provenance.md` (reports)
9. `terms_of_reference_audit.md` (reports)
10. `editorial_pass_log.md` (methodology)
11. `tier_c_pixel_audit.md` (methodology)
12. `338canada_integration.md` (methodology)

---

## Phased execution plan

- **Phase A (low risk):** 12 zero-ref files → validate new directory structure exists and imports work.
- **Phase B (medium risk):** ~45 files with 1–2 incoming refs → batch grep-replace cross-refs after each move.
- **Phase C (high risk):** 15 files with 3+ refs → coordinate moves with external references (report_academic.md, pre-registration docs, FROZEN_MANIFEST.md).
- **Phase D (verification):** ast.parse on every touched .py file; grep for stale `analysis/v0_1_` or `analysis/v0_2_` paths not under the new subdir.
