Analytical findings reports, pipeline logs, and regenerable data outputs produced by the scripts in `../scripts/`.

## Findings reports

Core reports that feed the public and academic documents are marked with *.

| File | Description |
|---|---|
| `v0_1_section_A_population_equality.md` | * Population-equality analysis across 87 EDs |
| `v0_1_section_C_geographic_coherence.md` | * Geographic coherence and compactness findings |
| `v0_1_section_D_procedural.md` | * Procedural compliance review |
| `v0_1_historical_eg_baseline.md` | * Efficiency-gap baseline from 2015–2023 elections |
| `v0_1_neighbour_drain_analysis.md` | * Neighbour-drain effect findings |
| `v0_1_da_anchoring_analysis.md` | DA boundary anchor results and discrepancy log |
| `v0_1_municipal_anchoring_analysis.md` | Municipal boundary anchor results |
| `v0_1_topology_cleanup_analysis.md` | Topology error counts and fixes per ED |
| `v0_1_dpg_perturbation_analysis.md` | Sensitivity of findings to DPG geometry uncertainty |
| `v0_5_dpg_perturbation_analysis.md` | DPG perturbation re-run on v0_5 shapefiles |
| `v0_1_adjacency_analysis.csv` | ED adjacency matrix (CSV) |
| `v0_1_methods_paper_draft.md` | Methods section draft for academic paper |
| `v0_1_boundary_propagation_summary.json` | Propagation stats by ED |
| `v0_1_chen_rodden_decomposition.md` | Chen-Rodden urban-rural decomposition |
| `v0_1_marginal_seats_findings.md` | Marginal seat analysis |
| `v0_1_rural_gap_findings.md` | Rural representation gap findings |
| `v0_1_maup_area_weighted_analysis.md` | MAUP sensitivity for area-weighted attribution |
| `phase_4c_gerrymander_comparison.md` | Gerrymander comparison across scenarios |
| `v0_1_tier_c_sweep_analysis.md` | Tier-C boundary sweep summary |
| `v0_1_vote_anywhere_report.md` | Vote-anywhere spatial integrity |
| `va_spatial_integrity_report.md` | Spatial integrity of vote-anywhere polygons |
| `v0_1_approximate_shape_analysis.md` | Analysis of approximate (pre-canonical) shapes |
| `v0_1_terms_of_reference_audit.md` | Audit against Electoral Boundaries Commission ToR |
| `v0_1_chair_recommendation_5_analysis.md` | Analysis of Commission Chair Recommendation 5 |
| `v0_1_byelection_assessment.md` | Impact assessment for pending by-elections |
| `v0_1_plan_b_cross_check.md` | Cross-check of alternative boundary scenario |
| `v0_1_pre_registration_draft.md` | Pre-registration snapshot |
| `v0_1_pre_registration_amendment_2026-04-23.md` | Amended pre-registration (2026-04-23) |
| `v0_1_bias_audit.md` | Internal bias audit of methods and data |
| `v0_1_claim_significance_analysis.md` | Statistical significance of headline claims |
| `submission_search_findings.md` | Summary of public-submission search |

## Pipeline outputs

The `.csv` and `.json` files (logs, crosswalks, summaries) are **regenerable** by re-running the corresponding script. Do not treat them as source-of-truth for manuscript text; cite the script and methodology instead.

Key regenerable outputs: `v0_1_population_consistency.csv`, `v0_1_adjacency_analysis.csv`, `v0_1_municipal_anchoring_log.csv`, `v0_1_da_anchoring_log.csv`, `v0_1_boundary_propagation_log.csv`, `v0_1_topology_cleanup_log.csv`, `v0_1_boundary_propagation_summary.json`, `v0_1_phase4c_maup_summary.json`, `v0_5_phase4f_summary.json`.
