<stdin>:122: SyntaxWarning: "\|" is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\|"? A raw string is also an option.
# Script Inventory — `alberta_audit/analysis/scripts/`

**Generated:** 2026-05-10  
**Total scripts:** 110 (`__init__.py` excluded from analysis)  
**Archived this session:** 13 (in `historical_deprecated.zip` under `archived_20260510/`)

**Legend for the *Recommendation* column:**
- **KEEP** — actively produces reported results, is imported, or builds the PDF/figures
- **ARCHIVE** — no Python importers, no doc mention, and either DPG-hardcoded or clearly superseded
- **YOUR CALL** — orphan by mechanical checks, but plausibly useful for ongoing work; needs human judgment

---

| # | Script | Purpose | In report? | Importers | DPG? | Recommendation |
|---|---|---|:-:|:-:|:-:|---|
| 1 | `2015_cross_election.py` | Alberta Cross-Election Analysis (v0.1) — 2015 votes on 2019 and 2026 maps. | n | 0 | n | YOUR CALL (doc mention only) |
| 2 | `338canada_historical.py` | v0_1_338canada_historical.py Track AA: historical 338Canada Alberta projections — pipeline. | n | 0 | n | YOUR CALL (doc mention only) |
| 3 | `338canada_reallocate.py` | v0_1_338canada_reallocate.py Track J, Phases 2-3. | Y | 0 | n | **KEEP** (active) |
| 4 | `338canada_scraper.py` | v0_1_338canada_scraper.py Pulls 338Canada per-riding projections for all 87 Alberta ridings. | Y | 0 | n | **KEEP** (active) |
| 5 | `_fetch_osm_natural.py` | _fetch_osm_natural.py — fetch Alberta-wide OSM highways and rivers for the natural-anchoring secondary check. | n | 0 | n | YOUR CALL (private helper) |
| 6 | `a1_legal_baseline_2021_census.py` | v0.1 A1 Legal-Baseline — 2021-census-direct on the 87 existing 2019 EDs. | Y | 0 | n | **KEEP** (active) |
| 7 | `advance_vote_sensitivity.py` |  | n | 0 | n | YOUR CALL (doc mention only) |
| 8 | `advance_vote_splat.py` | v0_1_advance_vote_splat.py ========================== Apportions non-Election-Day votes (Advance, Special Ballot, Mobile) from polls_2023_unified.csv to individual Voting Areas (VAs) using Election-Day vote shares as splat weights. | Y | 0 | n | **KEEP** (active) |
| 9 | `aggregate_sentiment_intensity.py` | aggregate_sentiment_intensity.py Aggregates sentiment intensity scores by configuration to compute the weighted-net intensity metrics for §5.9.4.6. | n | 0 | n | YOUR CALL (doc mention only) |
| 10 | `airdrie_overlap_diagnostic.py` | v0_1_airdrie_overlap_diagnostic.py ==================================== Diagnostic analysis of the Calgary-Airdrie overlap artifact in the canonical minority 2026 ED shapefile. | n | 0 | n | YOUR CALL (doc mention only) |
| 11 | `airdrie_quadrant_anchoring.py` |  | n | 0 | n | YOUR CALL (doc mention only) |
| 12 | `annotate_ensemble_seats_chart.py` | annotate_ensemble_seats_chart.py Regenerates the seats_at_50_50 ensemble distribution chart (v0_9, 250k) with an explanatory callout annotation at the minority 2026 vertical line. | n | 0 | n | **KEEP** (active) |
| 13 | `article_figures.py` | v0_1_article_figures.py Generate the inline figures the magazine article embeds: 1. | n | 0 | n | **KEEP** (active) |
| 14 | `assignment_prep.py` | Phase 4C preparation pipeline. | n | 0 | n | YOUR CALL (doc mention only) |
| 15 | `build_academic_pdf.py` | Build an Alberta Views-style magazine PDF of report_academic.md. | n | 0 | n | **KEEP** (active) |
| 16 | `build_airdrie_visual_teardown.py` | build_airdrie_visual_teardown.py ================================ Visual teardown of the Airdrie 4-way split to counter the "highway anchoring" defense. | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 17 | `build_cover.py` | Build an editorial cover page for the Two Maps, One Province feature. | n | 0 | n | **KEEP** (active) |
| 18 | `build_ei_substrate.py` | Ecological Inference Substrate Builder (Spatial Crosswalk) This script performs Area-Weighted Interpolation to force Statistics Canada Dissemination Area (DA) demographic data onto Elections Alberta Voting Area (VA) polygons by calculating  | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 19 | `build_full_crosswalks.py` | Build full 2019 -> 2026 crosswalks for majority and minority maps. | n | 0 | Y | **ARCHIVE** (DPG-hardcoded) |
| 20 | `build_pdf.py` | Build an Alberta Views-style magazine PDF of report_public.md. | n | 0 | n | **KEEP** (active) |
| 21 | `canadian_base_rate_compute.py` | Canadian inter-map EG asymmetry base rate — Track V proxy computation. | n | 0 | n | YOUR CALL (doc mention only) |
| 22 | `canadian_base_rate_recalibrate.py` | Canadian inter-map EG asymmetry base rate — T3.3 recalibration (2026-04-23). | n | 0 | n | YOUR CALL (doc mention only) |
| 23 | `canonical_paths.py` | canonical_paths.py — Canonical shapefile path resolver. | n | 0 | n | **KEEP** (active) |
| 24 | `check_provenance.py` | Many derived files are not checked into Git due to size, so missing files are only warnings unless running full validation | n | 0 | n | **KEEP** (active) |
| 25 | `check_voice_and_readability.py` | House voice and readability checker. | n | 0 | n | YOUR CALL (doc mention only) |
| 26 | `chen_rodden_alberta.py` | Alberta Electoral Boundaries — Chen & Rodden (2013) Validation Test (v0.1) ========================================================================== Question: does Chen & Rodden's "unintentional gerrymandering" finding (from US context) tr | Y | 0 | n | **KEEP** (active) |
| 27 | `chen_rodden_decomposition.py` | Chen-Rodden geography-vs-drawing decomposition for Alberta's 2019 / 2026 maps against the 100,000-plan MCMC neutral ensemble. | n | 0 | n | YOUR CALL (doc mention only) |
| 28 | `compactness_for_verification_subset.py` | Polsby-Popper compactness for the Python ReCom verification subset. | n | 0 | n | YOUR CALL (doc mention only) |
| 29 | `compactness_metrics.py` | Alberta Electoral Boundaries — Compactness Metrics (v0.1) ============================================================ Computes Polsby-Popper compactness scores for every ED in the 2019 enacted map (87 EDs) and both 2026 proposed maps (89 E | Y | 0 | n | **KEEP** (active) |
| 30 | `compute_kappa.py` | compute_kappa.py Compute Cohen's kappa between LLM and human classifications from the validation sample CSV produced by validation_sample.py. | n | 0 | n | YOUR CALL (doc mention only) |
| 31 | `core_retention.py` | Core Retention Analysis (Incumbent Displacement) Calculates the core retention of electoral districts between two maps. | n | 0 | n | YOUR CALL (doc mention only) |
| 32 | `cross_commissioner_official.py` | Mocking authorship metadata since it's not strictly encoded in GPKG We will simulate that 21 hybrid districts exist, and assign authorship highly disproportionately to a single commissioner to test the flag. | n | 0 | n | **KEEP** (post-canonical) |
| 33 | `cross_election.py` |  | Y | 0 | n | **KEEP** (active) |
| 34 | `cross_election_rural_baseline.py` | Cross-election rural NDP baseline analysis (2015, 2019, 2023). | n | 0 | n | YOUR CALL (doc mention only) |
| 35 | `cross_reference_submitters.py` | Cross-reference EBC written submitters against Hansard public hearing participants. | n | 0 | n | YOUR CALL (doc mention only) |
| 36 | `csd_community_splits.py` | Track H — CSD-level community-splits count, per map. | Y | 0 | n | **KEEP** (active) |
| 37 | `dependency_graph_build.py` | Build the Alberta audit dependency DAG. | n | 0 | n | **KEEP** (active) |
| 38 | `dependency_graph_render.py` | Render the audit dependency graph. | n | 0 | n | **KEEP** (active) |
| 39 | `dependency_query.py` | Dependency-graph invalidation query CLI. | Y | 0 | n | **KEEP** (active) |
| 40 | `drain_label_shuffle_null.py` | drain_label_shuffle_null.py — Continuous drain_score + 10,000 label-shuffle null. | n | 0 | n | **KEEP** (active) |
| 41 | `drand_seed.py` | Cloudflare League of Entropy (Drand) Canonical Seed Generator ------------------------------------------------------------- To ensure cryptographic impartiality of the MCMC simulations, the primary audit seed is derived from a public, verif | n | 8 | n | **KEEP** (active) |
| 42 | `ecological_inference.py` | Ecological Inference (EI) Stub ------------------------------ Estimates voting patterns by demographic group using Bayesian methods or King's Ecological Inference model. | n | 0 | n | YOUR CALL (doc mention only) |
| 43 | `electoral_forensics_population.py` | Phase 1 — Population Equality (Section A) Alberta Electoral Boundaries Audit v0.8 A1: Variance distribution for each 2026 map A2: Geographic asymmetry (Calgary NE/central vs S/W; NDP-leaning vs UCP-leaning) A3: s.15(2) eligibility audit for | Y | 0 | n | **KEEP** (active) |
| 44 | `extended_partisan_metrics.py` | v0_1_extended_partisan_metrics.py =================================== Computes additional partisan bias metrics beyond the four in the MCMC ensemble: - Partisan Bias (seats-votes asymmetry at 50%) - Lopsided Margins (t-test: Wang 2016) - Pa | Y | 0 | n | **KEEP** (active) |
| 45 | `federal_boundary_correlation_official.py` | Real spatial intersection logic would go here | n | 0 | n | **KEEP** (post-canonical) |
| 46 | `generate_article_figures.py` | v0_1_generate_article_figures.py Magazine-legible figures for the article. | n | 0 | Y | **KEEP** (active) |
| 47 | `generate_infographic.py` | One-page PNG infographic of the 2026 Alberta Electoral Boundaries audit results. | n | 0 | n | **KEEP** (active) |
| 48 | `generate_infographic_v2.py` | Infographic v2 — 1920 × 1080, laptop-optimised, 4-colour semantic palette. | n | 0 | n | **KEEP** (active) |
| 49 | `hansard_sentiment_llm.py` | hansard_sentiment_llm.py Runs LLM sentiment classification over the EBC Public Meeting Hansard transcripts (Round 1 and Round 2). | n | 0 | n | YOUR CALL (doc mention only) |
| 50 | `historical_durability_official.py` | Simulate routing these vote shares through the official v11 map | n | 0 | n | **KEEP** (post-canonical) |
| 51 | `historical_eg_baseline.py` | Alberta Historical Efficiency Gap Baseline (v0.1) ================================================= Computes the efficiency gap for the 2015, 2019, and 2023 Alberta provincial elections under the boundary map in effect at each election, pro | n | 0 | n | YOUR CALL (doc mention only) |
| 52 | `intermap_permutation_test.py` | intermap_permutation_test.py ---------------------------- Permutation test for the directional inter-map partisan-bias claim. | n | 0 | n | **KEEP** (active) |
| 53 | `issue14_feasibility_check.py` | issue14_feasibility_check.py — Prep data for manual QGIS feasibility check Prepare a QGIS project file highlighting: 1. | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 54 | `issue14_feasibility_optimization.py` | issue14_feasibility_optimization.py — Automated COI-constrained anchoring optimization For each of the 3 worst-anchoring minority EDs, test whether reassigning perimeter VAs to adjacent EDs can improve anchoring while preserving Tier A COI  | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 55 | `joint_outlier_score.py` | joint_outlier_score.py -- Joint Outlier Score (Duck Score) Addresses the question: how probable is it that a neutral redistricting process would produce a map whose feature vector looks like the minority 2026 map? | n | 0 | n | **KEEP** (active) |
| 56 | `joint_outlier_score_canonical.py` | joint_outlier_score_canonical.py -- Joint Outlier Score (Duck Score), canonical run Same methodology as joint_outlier_score.py but uses the canonical 100k ensemble (simulated_ensemble_raw_samples_canonical.csv) and canonical real-map scores | n | 0 | n | **KEEP** (active) |
| 57 | `justification_tests.py` | v0_1_justification_tests.py Verification pipeline for testable justifications advanced for contested electoral divisions in the 2026 Alberta Electoral Boundaries Commission minority (and in one case majority) reports. | Y | 0 | n | **KEEP** (active) |
| 58 | `majority_symmetry_counter_test.py` | v0_1 Majority-map symmetry counter-test (Track Q, B3 defence). | Y | 0 | n | **KEEP** (active) |
| 59 | `marginal_seats_analysis.py` | Alberta Electoral Boundaries — Marginal Seats / Uniform-Swing Analysis ====================================================================== Task: translate the audit's partisan-shift range (roughly 0.5-1.6 pp efficiency gap, 1-3 seats in  | Y | 0 | n | **KEEP** (active) |
| 60 | `mcmc_ensemble.py` | v0.1 MCMC ensemble gerrymandering test — Alberta 2019 baseline. | Y | 8 | Y | **KEEP** (active) |
| 61 | `mcmc_ensemble_canonical.py` | mcmc_ensemble_canonical.py -------------------------- 100k ReCom MCMC ensemble re-run against official Elections Alberta canonical shapefiles (ea_majority_2026_eds.gpkg / ea_minority_2026_eds.gpkg). | n | 0 | n | **KEEP** (active) |
| 62 | `mcmc_full_coverage_rescore_v2.py` | Validation pass: rescore against the 10k ensemble using the canonical shapefiles and the full-vote VA substrate (Election-Day + splat). | Y | 0 | Y | **KEEP** (active) |
| 63 | `mcmc_verification_subset.py` | Court-defensibility forensic verification subset. | n | 0 | n | YOUR CALL (doc mention only) |
| 64 | `monte_carlo_ci.py` |  | Y | 1 | n | **KEEP** (active) |
| 65 | `municipal_anchoring_2019_baseline.py` |  | n | 0 | n | **KEEP** (active) |
| 66 | `municipal_splits.py` | v0_1_municipal_splits.py ========================= Counts how many times each Alberta municipality is split across multiple electoral districts in the 2019 enacted, majority 2026, and minority 2026 maps. | Y | 0 | Y | **KEEP** (active) |
| 67 | `neighbour_drain_adjacency.py` | Neighbour-drain Adjacency Test (Test 3A) ========================================== Combines §5.3.1 packing and §5.3.2 cracking into a single coupled-signature adjacency count. | Y | 1 | n | **KEEP** (active) |
| 68 | `november_red_alert_scorecard.py` | November Red Alert Scorecard — tripwire for the Lunty committee's 91-seat map. | n | 0 | n | YOUR CALL (doc mention only) |
| 69 | `november_tripwires.py` |  | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 70 | `packing_cracking_analysis.py` |  | Y | 7 | n | **KEEP** (active) |
| 71 | `parse_2015_results.py` | Parse 2015 Alberta provincial election results into CSV. | n | 0 | n | YOUR CALL (doc mention only) |
| 72 | `per_edit_sentiment_analysis.py` | per_edit_sentiment_analysis.py Sentiment analysis focused on minority map edits (areas that differ from majority). | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 73 | `plan_b_rerun.py` | Plan B re-run of the five justification tests. | n | 0 | n | YOUR CALL (doc mention only) |
| 74 | `polsby_popper.py` |  | n | 0 | n | YOUR CALL (doc mention only) |
| 75 | `population_consistency.py` | Population Consistency Cross-Check (Test B2) =============================================== Cross-checks the commission's per-ED population figures (from their published tables) against independent 2021 Census DA totals aggregated by spati | n | 0 | Y | **KEEP** (active) |
| 76 | `post_ocr_cleanup.py` | post_ocr_cleanup.py Run AFTER submission_sentiment_llm_full.py completes AND after OCR recovery. | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 77 | `quote_verify_and_clean.py` | quote_verify_and_clean.py Post-process sentiment results CSV to ensure every exact_quote is a verbatim substring of its source document. | n | 0 | n | YOUR CALL (doc mention only) |
| 78 | `reock.py` |  | Y | 0 | n | **KEEP** (active) |
| 79 | `rural_gap_dissection.py` | v0_1_rural_gap_dissection.py ============================ Forensic drill-down on the 3.9% rural-mean gap between the minority and majority 2026 Alberta electoral-boundary commission maps. | n | 0 | n | YOUR CALL (doc mention only) |
| 80 | `rural_protection_test.py` | Test the UCP-side argument: do the 2026 maps actually protect rural representation, and which one does it better? | n | 0 | n | YOUR CALL (doc mention only) |
| 81 | `s15_ratio_test.py` | s15_ratio_test.py — EBCA §15 population deviation compliance test Computes deviation from the provincial quota for every ED in both maps, then classifies each ED against the §15(1) normal band and §15(2) exception. | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 82 | `score_anchoring.py` | score_anchoring.py — Lane-2 Dangerzone metric #1 (municipal anchoring %) ======================================================================== Wraps the operational definition documented in `analysis/scripts/municipal_anchoring.py` (and  | n | 0 | n | **KEEP** (active) |
| 83 | `score_hybridization.py` | score_hybridization.py - Lane-2 Dangerzone metric #2 (hybrid ED count) ====================================================================== The audit's published prose (e.g. | n | 0 | n | YOUR CALL (doc mention only) |
| 84 | `score_natural_anchoring.py` | score_natural_anchoring.py — Lane-2 secondary check (natural anchoring %) ========================================================================= Companion / counterfactual to `analysis/scripts/score_anchoring.py`. | n | 0 | n | **KEEP** (active) |
| 85 | `sentiment_intensity_score.py` | sentiment_intensity_score.py Second-pass LLM scoring: adds an intensity (1-3) field to each already-classified Active Opposition / Active Support row in submission_sentiment_llm_full_results.csv. | n | 0 | n | YOUR CALL (doc mention only) |
| 86 | `sentiment_monitoring.py` | sentiment_monitoring.py 7 monitoring, error detection, error recovery, and error correction mechanisms for sentiment analysis pipelines. | n | 1 | n | **KEEP** (imported by 1) |
| 87 | `simulation_convergence_diagnostics.py` | Per-chain ESS and Gelman-Rubin R-hat for the corrected 2M MCMC ensemble. | n | 0 | n | **KEEP** (active) |
| 88 | `simulation_multichain_ensemble.py` | series (last updated 2026-04-26) | Y | 0 | n | **KEEP** (active) |
| 89 | `simulation_short_bursts.py` | v0_1_simulation_short_bursts.py ========================== Short-burst analysis: 500 independent 10-step ReCom chains starting from the 2019 enacted assignment. | n | 0 | n | **KEEP** (active) |
| 90 | `sub_ed_clustering_official.py` | Identify "hybrid" fractured districts. | n | 0 | n | **KEEP** (post-canonical) |
| 91 | `submission_ocr.py` | v0_1 OCR pass on image-only pages that likely contain the 88 missing submissions. | n | 0 | n | YOUR CALL (doc mention only) |
| 92 | `submission_ocr_analyze.py` | Standalone analyzer that reads OCR page text files already produced by v0_1_submission_ocr.py and performs the stitching + keyword search step. | n | 0 | n | YOUR CALL (doc mention only) |
| 93 | `submission_ocr_recovery.py` | submission_ocr_recovery.py Recovers text from the 23 image-only submission PDFs that pdfplumber couldn't extract. | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 94 | `submission_search.py` | v0_1 submission keyword search Downloads all 27 EBC submission batch PDFs, extracts text per submission, and runs keyword regexes to verify/refute the chair's claim that the minority's hybrid configurations (Airdrie 4-way, Nolan-Hill-Cochra | Y | 2 | n | **KEEP** (active) |
| 95 | `submission_sentiment_llm.py` | submission_sentiment_llm.py Reads the submission_search_dataset.csv to find which submissions mentioned specific configurations. | n | 0 | n | YOUR CALL (doc mention only) |
| 96 | `submission_sentiment_llm_full.py` | submission_sentiment_llm_full.py Full-corpus scan: runs LLM classification over all 1,252 EBC submissions (not just the keyword-flagged 70). | n | 0 | n | YOUR CALL (doc mention only) |
| 97 | `synthetic_gerrymander_official.py` | Baseline expected median is ~-0.02 | n | 0 | n | **KEEP** (post-canonical) |
| 98 | `szat.py` | szat.py — Swing-Zone Allocation Test Decomposes the efficiency-gap difference between the minority and majority 2026 Alberta Electoral Boundary Commission maps into the specific boundary choices (swing zones) that drive it. | Y | 1 | n | **KEEP** (active) |
| 99 | `szat_validate.py` | szat_validate.py -- Two validation checks for szat.py results. | n | 1 | n | **KEEP** (active) |
| 100 | `targeted_gerrymander_burst.py` | Short-bursts targeted gerrymander: maximise UCP seats@50/50 within ReCom. | Y | 0 | n | **KEEP** (active) |
| 101 | `targeted_gerrymander_burst_ndp.py` | Symmetric short-bursts targeted-gerrymander test: NDP direction. | Y | 0 | n | **KEEP** (active) |
| 102 | `third_party_sensitivity.py` | third_party_sensitivity.py D1 fix: Third-party vote sensitivity analysis. | Y | 0 | n | **KEEP** (active) |
| 103 | `tier_aware_perturbation_official.py` | In a full run, we would intersect these lines with the 2019 enacted map to classify segments as Tier A (0m uncertainty) vs Tier C (300m). | n | 0 | n | **KEEP** (post-canonical) |
| 104 | `track_l_drift.py` | Track L - Province-wide ED drift table (DA-based, accurate aggregation). | n | 0 | n | YOUR CALL (doc mention only) |
| 105 | `update_intensity_section.py` | update_intensity_section.py Updates §5.9.4.6 in report_academic.md with the finalized intensity-weighted net sentiment table. | n | 0 | n | **ARCHIVE?** (no usage signal) |
| 106 | `url_archival.py` | v0_1_url_archival.py Alberta Electoral Boundaries Audit — URL preservation pipeline. | n | 0 | n | YOUR CALL (doc mention only) |
| 107 | `va_attribution_area_weighted.py` |  | n | 0 | n | YOUR CALL (doc mention only) |
| 108 | `validate_fisher_independence.py` | validate_fisher_independence.py — Empirical Spearman correlation between Ch1 and Ch2. | n | 0 | n | **KEEP** (active) |
| 109 | `validation_sample.py` | validation_sample.py Generate a stratified random sample of classified rows for human inter-rater reliability review. | n | 0 | n | YOUR CALL (doc mention only) |

---

## Summary

- KEEP-active: 53
- YOURCALL-docmention: 37
- ARCHIVE-orphan: 10
- KEEP-postcanonical: 6
- YOURCALL-private: 1
- ARCHIVE-DPG: 1
- KEEP-imported: 1
