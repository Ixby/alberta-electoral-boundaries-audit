# Deprecated Files

Files in this folder were used during earlier versions of the audit and are preserved for historical reference, provenance, and reproducibility of prior commits. They should not be cited in current outputs.

## Contents

- **`v0_1_packing_cracking_analysis.py`** — Original B1–B4 script that computed metrics only for the 2019 baseline and minority 2026, not the majority. Superseded by `analysis/v0_2_packing_cracking_analysis.py`, which covers all three maps symmetrically with falsifiability gates. The v0.1 script is retained because its 2019 and minority numbers match v0.2 and it served as the reproducibility reference during the v0.2 bias-remediation pass.
- **`v0_1_packing_cracking_results.md`** — First-session written findings from v0.1. Superseded by `report_academic.md` §3 which uses the symmetric v0.2 numbers.
- **`_phase1_output.txt`** — Raw console output from the first Phase 1 execution. Retained only as a timestamp artifact.
- **`v0_8_gerrymander_audit_prompt.md`** — Original continuation prompt authored before this repository existed.
- **`v0_9_gerrymander_audit_prompt.md`** — First revision; 150K→500K token ceiling, 4-hour wall-clock cap, VA-polygon Phase 4C substrate.
- **`v1_0_gerrymander_audit_prompt.md`** — Stage-based falsifiability gates S0–S6 introduced.
- **`v1_1_gerrymander_audit_prompt.md`** — Red-team gates RT1–RT6 added.

The current prompt is `v1_2_gerrymander_audit_prompt.md` at the repository root.

## Draft-process artefacts

The following files documented the audit's internal stress-testing and methodology-hardening passes during drafting. They are preserved for provenance but are not required to replicate the audit's findings. A replicator who wants only the results should ignore this folder.

- **`v0_1_red_team_academic_discredit.md`** — First adversarial pass on the academic paper; 21 attacks ranked by severity.
- **`v0_1_red_team_round_2.md`** — Second adversarial pass identifying 17 new / residual / missed attacks after the first fortification.
- **`v0_1_fortification_a1_a5.md`** — Peer-review-grade defence of the five HIGH-severity attacks from the first red-team, with narrowed claims.
- **`v0_1_fortification_b1_b6.md`** — Defence of the six MEDIUM-severity attacks; produced the symmetry counter-test that revealed the Lethbridge and Red Deer 4-way findings.
- **`v0_1_fortification_c1_c10.md`** — Defence of the ten LOW-severity attacks; literature-backed responses plus the initial Canadian comparator catalogue.
- **`v0_1_subagent_prompts_appendix.md`** — Archive of the sub-agent prompts used during analysis passes.
- **`v0_1_prompt_readiness.md`** — v1.1 → v1.2 prompt execution-readiness assessment.
- **`v0_2_final_redteam.md`** — Early stress-test pass on methodology and prompt design.
- **`v1_2_prompt_redteam.md`** — Red-team pass on the v1.2 prompt itself.
- **`appendix_e_recon_log.md`** — Appendix E PDF reconnaissance log.
- **`data_acquisition_log.md`** — Data-acquisition pass log.
- **`data_closeout_log.md`** — Data-closeout pass log.
- **`submission_search_log.md`** — Submission-search technical log.
- **`v0_1_submission_ocr_log.md`** — OCR log for the non-text-layer submissions.

These files include methodology critiques and are useful for understanding how the audit was stress-tested. They are not primary outputs. If the audit's conclusions change because of new data, the fortification files may need updating; consult `report_academic.md` and the active `analysis/` files first.

## Why keep these

The audit's reproducibility discipline requires that every historical claim be traceable to the script and data that produced it. If a v0.1 finding needs to be re-examined, the script must still exist. Deleting it would break the audit trail documented in `analysis/v0_1_bias_audit.md`.

Do not add new work to this folder. New deprecations should be added in the same style (script + corresponding writeup moved together, with a note in this README).
