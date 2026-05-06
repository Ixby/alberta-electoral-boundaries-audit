# Deprecated Files

Files in this folder were used during earlier versions of the audit and are preserved for historical reference, provenance, and reproducibility of prior commits. They should not be cited in current outputs.

Do not add new active work here. New deprecations: move the file, add an entry below, commit.

---

## Scripts (superseded by later versions)

| File | Superseded by | Notes |
| --- | --- | --- |
| `shape_refinement.py` (v0_1) through `shape_refinement_v5.py` | `analysis/scripts/shape_refinement_v6_processors.py` + `shape_refinement_v6_writer.py` | Sequential boundary-refinement pipeline; v6 is the current version imported by `derive_boundaries.py` |
| `dpg_perturbation_sensitivity.py` (v1) | `analysis/scripts/dpg_perturbation_sensitivity_v05.py` | Flat ±500 m perturbation against v0_2 topology-clean files; v05 uses DA-anchored DPGs |
| `dpg_perturbation_sensitivity_v2.py` | `analysis/scripts/dpg_perturbation_sensitivity_v05.py` | Tiered-sigma variant; superseded by v05 |
| `assignment_va_attribution.py` | `analysis/scripts/assignment_va_attribution_maup_v3_v05.py` | Initial VA→ED centroid assignment; MAUP-corrected version is current |
| `assignment_va_attribution_maup.py` | `analysis/scripts/assignment_va_attribution_maup_v3_v05.py` | First MAUP correction pass |
| `assignment_va_attribution_maup_v2.py` | `analysis/scripts/assignment_va_attribution_maup_v3_v05.py` | Second MAUP correction pass |
| `mcmc_full_coverage_rescore.py` | `analysis/scripts/mcmc_full_coverage_rescore_v2.py` | 19-row crosswalk version with partial-coverage bug (flagged in red_team_consolidated.md); v2 fixes this |
| `mcmc_ensemble_100k.py` | `analysis/scripts/mcmc_ensemble_250k.py` | 100k-sample run; superseded by 250k |
| `mcmc_full_coverage_rescore_100k.py` | `analysis/scripts/mcmc_full_coverage_rescore_v2.py` | 100k rescore pass; superseded |
| `v0_8/cross_election_v8_full.py` | `analysis/scripts/cross_election.py` | v0_8 cross-election script with known ED-alignment bug |
| `v0_8/mcmc_ensemble_250k_v0_8.py` | `analysis/scripts/mcmc_ensemble_250k.py` | v0_8 buggy ensemble run |
| `v0_8/v8_*.py` (6 files) | `analysis/scripts/` current pipeline | v0_8 diagnostic and refinement scripts from the alignment-fix pass |

---

## Methodology documents (superseded or version-tagged)

| File | Notes |
| --- | --- |
| `shape_refinement_v3.md` | Documents v3 refinement pass; v6 is current |
| `shape_refinement_v4.md` | Documents v4 refinement pass |
| `v0_1_shape_refinement_v2.md` | Documents v2 refinement pass |
| `v0_1_science_red_team_reproducibility_and_falsifiability.md` | v0_1 red-team pass; superseded by `analysis/red_team/science_red_team_framework.md` and `red_team_consolidated.md` |
| `v0_1_cycle_lag_commentary.md` | v0_1 cycle-lag analysis commentary; current analysis is `analysis/reports/cycle_lag_analysis.md` |
| `v0_1_max_dpi_extraction_and_rerun.md` | v0_1 DPI extraction log; current: `analysis/reports/` |

---

## Process and provenance logs (preserved for audit trail)

| File | Notes |
| --- | --- |
| `appendix_e_recon_log.md` | Appendix E PDF reconnaissance log |
| `data_acquisition_log.md` | Data-acquisition pass log |
| `data_closeout_log.md` | Data-closeout pass log |
| `submission_search_log.md` | Submission-search technical log |
| `v0_1_submission_ocr_log.md` | OCR log for non-text-layer submissions |
| `v0_1_alberta_audit_chat2_migration.md` | Session handoff log from chat 2 |

---

## Archived data outputs

`data_outputs/` contains superseded CSV/JSON files from earlier pipeline runs:

| File | Superseded by |
| --- | --- |
| `boundary_refinement_impact.csv` through `_v5.csv` | `data/outputs/boundary_refinement_impact_v6.csv` |
| `dpg_perturbation_samples.csv`, `_v2_tiered.csv` | `data/outputs/dpg_perturbation_samples_v3_tight.csv` |
| `dpg_perturbation_summary_v2_tiered.json` | `data/outputs/dpg_perturbation_summary_v3_tight.json` |
| `2015_to_2019_crosswalk_partial.csv` | `data/outputs/2015_to_2019_crosswalk.csv` (full version) |

Earlier versioned phase outputs are in `v0_1/` and `v0_2/` subdirectories. The `simulation_checkpoints_*` directories contain partially-executed MCMC runs (v0_8 buggy run and a 2M-step killed run) preserved for reproducibility audits.

---

## Report backups (redundant; git is version control)

| File | Notes |
| --- | --- |
| `report_academic_backup.md` | Manual backup of `report_academic.md`; deprecated 2026-05-06 — git history is authoritative |
| `report_public_backup.md` | Manual backup of `report_public.md`; deprecated 2026-05-06 — git history is authoritative |

---

## Note on draft-process artefacts (fortification passes, red-team rounds)

The v0_1 and v0_2 red-team, fortification, and prompt-readiness documents were moved to `private_notes/` (gitignored) during the 2026-04-23 consolidation pass. They are documented in `analysis/meta/PRIVATE_FILES.md`. The consolidated synthesis is `analysis/methodology/red_team_consolidated.md`.

Primary red-team passes are in `analysis/red_team/`.
