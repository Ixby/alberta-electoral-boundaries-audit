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

## Why keep these

The audit's reproducibility discipline requires that every historical claim be traceable to the script and data that produced it. If a v0.1 finding needs to be re-examined, the script must still exist. Deleting it would break the audit trail documented in `analysis/v0_1_bias_audit.md`.

Do not add new work to this folder. New deprecations should be added in the same style (script + corresponding writeup moved together, with a note in this README).
