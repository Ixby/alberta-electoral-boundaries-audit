Analytical findings reports, pipeline logs, and regenerable data outputs produced by the scripts in `../analysis/scripts/`.

> **CRS note:** GeoJSON files in `data/outputs/district_patterns/` are CRS84/WGS84 (EPSG:4326). The canonical audit shapefiles are EPSG:3400 (Alberta 10-TM). Do not reproject the GeoJSONs for analysis — they are display copies only.

---

## Core Findings

Files marked * are directly cited in both the public report and the academic monograph.

| File | Description |
|---|---|
| `population_equality.md` | * Population-equality analysis across 87 EDs (A1/A2/A3 tests) |
| `geographic_coherence.md` | * Geographic coherence and compactness (Lane 2 structural) |
| `procedural_analysis.md` | * Procedural compliance review |
| `partisan_bias_summary.md` | * Partisan bias B1–B6: packing, cracking, efficiency gap across all three maps |
| `historical_eg_baseline.md` | * Efficiency-gap baseline from 2015–2023 Alberta elections |
| `neighbour_drain_analysis.md` | * Neighbour-drain effect findings |
| `da_anchoring_analysis.md` | * Dissemination-area boundary anchor results and discrepancy log |
| `municipal_anchoring_analysis.md` | * Municipal boundary anchor results |
| `terms_of_reference_audit.md` | * Audit against Electoral Boundaries Commission Terms of Reference |
| `chair_recommendation_5_analysis.md` | * Analysis of Commission Chair Recommendation 5 |
| `joint_outlier_score_summary.md` | * Joint Mahalanobis D² outlier score summary (Fisher-combined p-value) |

---

## Lane 1 — Statistical

Vote-attribution and MCMC-based findings. Depend on `data/shapefiles/derived/` VA polygons.

| File | Description |
|---|---|
| `boundary_sweep_analysis.md` | Tier-C boundary sweep: SZAT channel analysis |
| `extended_partisan_metrics.md` | Extended partisan metrics (mean-median split, Declination, wasted-vote ratio) |
| `gerrymetrics_comparison.md` | GerryMetrics cross-validation against external Python library |
| `chen_rodden_decomposition.md` | Chen-Rodden urban-rural efficiency-gap decomposition |
| `marginal_seats_findings.md` | Marginal seat distribution across maps |
| `intermap_permutation_test_results.md` | Intermap permutation test: minority vs majority vs Lunty map |

---

## Lane 2 — Structural

Geometry-only findings. Depend only on canonical shapefiles and topology.

| File | Description |
|---|---|
| `polsby_popper_verdict.md` | Polsby-Popper compactness verdict per ED |
| `reock_verdict.md` | Reock compactness verdict per ED |
| `topology_cleanup_analysis.md` | Topology error counts and corrections per ED |
| `airdrie_highway_pretext.md` | Airdrie boundary and Highway 2 corridor alignment analysis |
| `airdrie_overlap_report.md` | Airdrie four-way split: overlap area calculation |
| `municipal_splits.md` | Municipal boundary splits by commission map |
| `natural_anchoring_secondary_check.md` | Secondary natural-feature anchoring check (rivers, escarpments) |
| `va_spatial_integrity_report.md` | Spatial integrity of vote-anywhere polygons |
| `vote_anywhere_report.md` | Vote-anywhere coverage findings |
| `lesser_slave_lake_va043_representation_gap.md` | Lesser Slave Lake VA 043 representation gap: Woodland Cree community boundary analysis |
| `geometry_provenance.md` | Geometry provenance chain and canonical shapefile transition log |

---

## Procedural & Political

| File | Description |
|---|---|
| `ebc_s15_selective_application.md` | * Section 15 selective application: unequal deviation justification across EDs |
| `byelection_assessment.md` | Impact assessment for pending by-elections under each map |
| `justification_tests_findings.md` | Commission justification-text statistical tests |
| `pre_registration_amendment_log.md` | Pre-registration amendment log (OSF entries and change justifications) |
| `pre_registration_platform_analysis.md` | Platform-level analysis underlying the pre-registration |
| `claim_significance_analysis.md` | Statistical significance of headline claims |
| `post_audit_recompute_deltas.md` | Finding deltas after official-shapefile recompute (M2 check) |
| `checklist_baseline_scoring.md` | Section-by-section baseline scoring checklist |
| `lunty_91_seat_preliminary.md` | Lunty 91-seat map preliminary assessment |
| `edmonton_beaumont_log.md` | Edmonton-Beaumont boundary discrepancy log |
| `dangerzone_metric_definitions.md` | Danger-zone metric formal definitions |

---

## Robustness & Sensitivity

| File | Description |
|---|---|
| `sensitivity_analysis.md` | Sensitivity analysis: key parameter choices across all tests |
| `regional_swing_robustness.md` | Regional swing assumption robustness check |
| `cross_election_robustness.md` | Cross-election consistency check (2015–2023) |
| `cross_election_2015.md` | 2015 election cross-check results |
| `cycle_lag_analysis.md` | Cycle-lag analysis: redistribution effect over time |
| `advance_vote_sensitivity.md` | Advance-vote inclusion/exclusion sensitivity |
| `rural_gap_findings.md` | Rural representation gap findings |
| `assignment_gerrymander_comparison.md` | Gerrymander metric comparison across VA-assignment scenarios |
| `maup_area_weighted_analysis.md` | MAUP sensitivity: area-weighted vote attribution |
| `maup_centroid_sensitivity.md` | MAUP sensitivity: centroid-based vote attribution |
| `redist_python_comparison.md` | redist (R) vs Python ensemble comparison |
| `simulation_short_bursts.md` | Short-burst simulation robustness check (10k vs 250k runs) |
| `burst_symmetry_analysis.md` | Burst-symmetry analysis for MCMC convergence |
| `drain_label_shuffle_null.md` | Neighbour-drain null distribution: label-shuffle test |

---

## Public Submissions

| File | Description |
|---|---|
| `submission_search_findings.md` | Summary of public-submission search and categorisation |
| `submission_search_log.md` | Full public-submission search event log |
| `sentiment_analysis_completion_report.md` | Submission sentiment and intensity analysis (452 deduplicated rows) |
| `sentiment_rationale_crossreference.md` | Sentiment-rationale cross-reference to commission published findings |

---

## Methods

| File | Description |
|---|---|
| `methods_paper_draft.md` | Methods section draft for the academic paper |

---

## Pipeline Outputs

The files below are **regenerable** by re-running the corresponding script. Do not cite them directly in the manuscripts; cite the script and methodology instead.

| File | Description |
|---|---|
| `adjacency_analysis.csv` | ED adjacency matrix |
| `advance_vote_splat_diagnostics.csv` | Advance-vote splat diagnostics |
| `airdrie_four_way_split_teardown.png` | Airdrie four-way split diagram (figure) |
| `assignment_va_to_2026_assignments_maup.csv` | VA → 2026 ED MAUP assignment crosswalk |
| `assignment_va_to_2026_assignments_maup_v2.csv` | VA → 2026 ED MAUP assignment crosswalk (v2) |
| `boundary_propagation_log.csv` | Boundary propagation event log |
| `boundary_propagation_summary.json` | Boundary propagation summary statistics |
| `compactness_metrics.csv` | Per-ED compactness metrics (Polsby-Popper, Reock) |
| `contiguity_check.csv` | ED contiguity verification results |
| `da_anchoring_log.csv` | DA boundary anchor discrepancy log |
| `intermap_permutation_test_results.json` | Intermap permutation test raw results |
| `joint_outlier_score.json` | Joint Mahalanobis outlier score per map |
| `municipal_anchoring_log.csv` | Municipal boundary anchor event log |
| `neighbour_drain_log.csv` | Per-ED neighbour-drain drain log |
| `phase4c_maup_summary.json` | Phase 4c MAUP summary statistics |
| `phase4c_va_to_2026_assignments_maup.csv` | Phase 4c MAUP assignment crosswalk |
| `phase4f_summary.json` | Phase 4f ensemble summary statistics |
| `population_consistency.csv` | ED population consistency check (deviation table) |
| `s15_deviation_compliance.csv` | s.15 Electoral Boundaries Commission Act deviation compliance table |
| `szat_2019_baseline.json` | SZAT 2019 election baseline results |
| `szat_results.csv` | SZAT per-ED results (canonical vote attribution) |
| `szat_results_full_votes.csv` | SZAT per-ED results (full vote tally) |
| `szat_summary.json` | SZAT summary statistics (canonical vote attribution) |
| `szat_summary_full_votes.json` | SZAT summary statistics (full vote tally) |
| `tier_c_crop_manifest.json` | Tier-C boundary crop manifest |
| `tier_c_sweep_log.csv` | Tier-C boundary sweep event log |
| `topology_cleanup_log.csv` | Topology cleanup event log |
| `topology_cleanup_summary.json` | Topology cleanup summary statistics |
