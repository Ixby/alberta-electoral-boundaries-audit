Analytical findings reports, pipeline logs, and regenerable data outputs produced by the scripts in `../scripts/`.

## Findings reports

Core reports that feed the public and academic documents are marked with *.

| File | Description |
|---|---|
| `section_A_population_equality.md` | * Population-equality analysis across 87 EDs |
| `section_C_geographic_coherence.md` | * Geographic coherence and compactness findings |
| `section_D_procedural.md` | * Procedural compliance review |
| `historical_eg_baseline.md` | * Efficiency-gap baseline from 2015–2023 elections |
| `neighbour_drain_analysis.md` | * Neighbour-drain effect findings |
| `da_anchoring_analysis.md` | DA boundary anchor results and discrepancy log |
| `municipal_anchoring_analysis.md` | Municipal boundary anchor results |
| `topology_cleanup_analysis.md` | Topology error counts and fixes per ED |
| `v0_1_dpg_perturbation_analysis.md` | Sensitivity of findings to DPG geometry uncertainty |
| `dpg_perturbation_analysis.md` | DPG perturbation re-run on v0_5 shapefiles |
| `adjacency_analysis.csv` | ED adjacency matrix (CSV) |
| `methods_paper_draft.md` | Methods section draft for academic paper |
| `boundary_propagation_summary.json` | Propagation stats by ED |
| `chen_rodden_decomposition.md` | Chen-Rodden urban-rural decomposition |
| `marginal_seats_findings.md` | Marginal seat analysis |
| `rural_gap_findings.md` | Rural representation gap findings |
| `maup_area_weighted_analysis.md` | MAUP sensitivity for area-weighted attribution |
| `assignment_gerrymander_comparison.md` | Gerrymander comparison across scenarios |
| `tier_c_sweep_analysis.md` | Tier-C boundary sweep summary |
| `vote_anywhere_report.md` | Vote-anywhere spatial integrity |
| `va_spatial_integrity_report.md` | Spatial integrity of vote-anywhere polygons |
| `approximate_shape_analysis.md` | Analysis of approximate (pre-canonical) shapes |
| `terms_of_reference_audit.md` | Audit against Electoral Boundaries Commission ToR |
| `chair_recommendation_5_analysis.md` | Analysis of Commission Chair Recommendation 5 |
| `byelection_assessment.md` | Impact assessment for pending by-elections |
| `plan_b_cross_check.md` | Cross-check of alternative boundary scenario |
| `pre_registration_draft.md` | Pre-registration snapshot |
| `pre_registration_amendment_2026-04-23.md` | Amended pre-registration (2026-04-23) |
| `bias_audit.md` | Internal bias audit of methods and data |
| `claim_significance_analysis.md` | Statistical significance of headline claims |
| `submission_search_findings.md` | Summary of public-submission search |

## Pipeline outputs

The `.csv` and `.json` files (logs, crosswalks, summaries) are **regenerable** by re-running the corresponding script. Do not treat them as source-of-truth for manuscript text; cite the script and methodology instead.

Key regenerable outputs: `population_consistency.csv`, `adjacency_analysis.csv`, `municipal_anchoring_log.csv`, `da_anchoring_log.csv`, `boundary_propagation_log.csv`, `topology_cleanup_log.csv`, `boundary_propagation_summary.json`, `v0_1_phase4c_maup_summary.json`, `phase4f_summary.json`.
