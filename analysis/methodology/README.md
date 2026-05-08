Internal working documents covering pre-registration, methodological decisions, red-team review, and audit scaffolding — not public outputs.

| File | Description |
|---|---|
| `pre_registration_draft.md` | Pre-registered hypotheses and analysis plan (original) |
| `retraction_pathway.md` | Conditions under which findings would be retracted or amended |
| `uncertainty_and_shapefile_impact.md` | Quantified uncertainty from DPG geometry and its propagation |
| `bias_audit.md` | Self-audit of analytical choices for directional bias |
| `audit_dependency_graph.dot` / `.json` | Machine-readable dependency graph of all audit outputs |
| `audit_dependency_graph_readme.md` | How to read and query the dependency graph |
| `self_check_protocol.md` | Quality-control trigger phrases and checklists (`check task`, `check project`, `check pre-reg`, `check lit`, `check deps`) |
| `novel_contributions.md` | Four novel methodological contributions: DPG, Neighbour-Drain, SZAT, Two-Lane Scorecard |
| `threshold_provenance.md` | Justification for every numerical threshold used in the audit |
| `null_hypothesis_and_exoneration_criteria.md` | Null hypotheses and criteria for exonerating the Commission |
| `test_selection_rationale.md` | Rationale for which statistical tests were chosen and which were rejected |
| `test_apparatus_defense.md` | Defense of the test apparatus against anticipated challenges |
| `canonical_shapefile_methodology.md` | How DPG-derived shapefiles were constructed and quality-checked |
| `shapefile_redteam_report.md` | Red-team review specific to shapefile construction |
| `sign_convention_resolution.md` | Resolution of sign ambiguity in efficiency-gap calculations |
| `reproducibility_verification.md` | Steps taken to verify end-to-end reproducibility |
| `data_preparation.md` | Data sourcing, cleaning, and crosswalk decisions |
| `master_plan.md` | Phase-by-phase execution plan for the full audit |
| `assignment_runbook.md` | Step-by-step runbook for Phase 4c execution |
| `red_team_consolidated.md` | Consolidated synthesis of all red-team passes (see `analysis/red_team/` for primary red-team pass documents) |

These documents inform the manuscript and are referenced in footnotes but are not themselves public deliverables.

---

## Primary red-team passes

Primary red-team pass documents live in `analysis/red_team/` (not this directory). The synthesis is `red_team_consolidated.md` above.

Key documents in `analysis/red_team/`:

| File | Description |
| --- | --- |
| `science_red_team_design_and_stats.md` | Design and statistics red-team pass |
| `science_red_team_data_priorart_peerreview.md` | Data, prior art, and peer-review red-team pass |
| `science_red_team_reproducibility_and_falsifiability.md` | Reproducibility and falsifiability red-team pass |
| `science_red_team_framework.md` | Framework and scope for science red-team passes |
| `external_code_audit_findings_gemini_2026-04-26.md` | External code audit (Gemini, 2026-04-26) |
| `external_code_audit_findings_meridian.md` | External code audit (Meridian) |
| `legal_red_team_framework.md` | Legal red-team framework |
| `legal_red_team_report_academic.md` | Legal review of academic report |
| `legal_red_team_report_public.md` | Legal review of public report |
| `red_team_conclusions.md` | Consolidated red-team conclusions with open items |
| `red_team_assertions.md` | Assertion-level red-team findings |
| `red_team_code.md` | Code review findings |
| `peer_review_methods.md` | Methods peer-review pass |
| `peer_review_legal.md` | Legal peer-review pass |
| `peer_review_canadian.md` | Canadian context peer-review pass |
