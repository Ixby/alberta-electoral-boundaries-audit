---
name: Live-tasks registry
description: Running record of background sub-agents spawned by any session. Maintained so a session terminated by usage limits can be resumed from a clean state — the next session can re-spawn unfinished tasks without losing context. Each entry records the task prompt, expected outputs, and the state of partial outputs on disk at last check.
forward_dependencies:
  - migration.md (carries forward the current state summary)
  - next session's kickoff procedure
backward_dependencies:
  - each sub-agent's prompt (preserved verbatim here for re-spawn)
---

# Live-tasks registry

**Purpose.** When a Claude session spawns background sub-agents with the `Agent` tool, and then the main session is terminated by usage limits or user action before those agents return, the sub-agents still complete but their outputs land on disk with no one watching. The next session should check this file to learn what was dispatched, verify the outputs on disk, and either integrate finished outputs or re-spawn unfinished ones.

**Discipline.** When the main session spawns a sub-agent, it should add an entry below. When the sub-agent returns, the entry moves to the "Completed this session" section. If the session ends with live entries remaining, those entries are a handoff to the next session.

**Template for each entry:**

```
## <ISO timestamp> — <short track name>

**Agent ID:** <id from spawn>
**Status:** RUNNING / COMPLETED / TIMED-OUT / FAILED / RESUMABLE
**Task summary:** <one paragraph>
**Expected output contract:**
- <file 1>
- <file 2>
**Observed on-disk outputs at last check:** <paths, partial or complete>
**Re-spawn prompt:** <full sub-agent prompt verbatim, so next session can re-dispatch>
**Notes:** <any special context, e.g., "Wayback SPN2 quota blocked"; "needs Chrome MCP"; "pre-requisite sub-agent X must finish first">
```

**Entry lifecycle.** An entry moves through: RUNNING (live) → COMPLETED (outputs integrated) / TIMED-OUT (wall-clock exceeded) / FAILED (returned with error). RESUMABLE is for partial work: the sub-agent produced some output before termination, and the next session can resume from disk state instead of re-running from zero.

---

## Currently live tasks

*(none — session 10 closed with all spawned tasks integrated)*

---

## Completed this session (session 10)

### 2026-04-22 — Track Y-prime-prime-prime — Tier C visual-transcription approximation for 3 misclassified EDs

**Agent ID:** a-visual-transcription (background agent a9029db98c0e3d389)
**Status:** COMPLETED.
**Expected outputs (delivered):**
- `analysis/v0_1_shape_refinement_v4.md`
- `analysis/v0_1_shape_refinement_v4.py`
- `analysis/v0_1_shape_refinement_v4_log.json`
- `data/v0_1_refined_v4_minority_2026_eds.gpkg`
- `data/v0_1_boundary_refinement_impact_v4.csv`
- `maps/verification/v0_4_minority_edmonton_windermere.png`
- `maps/verification/v0_4_minority_calgary_de_winton.png`
- `maps/verification/v0_4_minority_calgary_south.png`

**Integration:** §6.7 of `report_academic.md` extended with a Tier C visual-transcription annex paragraph. v4 runs parallel to v3; does not replace it. Territorial gap closed ~90 %; per-segment error bands documented. `analysis/v0_1_commission_reference_shapes.md` superseded by v4 for the three EDs (original mismatch observations retained for the record). No further action without commission shapefile release.

### 2026-04-22 — Track T — Threshold provenance compendium

**Status:** COMPLETED.
**Expected outputs (delivered):**
- `analysis/v0_1_threshold_provenance.md`

**Integration:** linked from Appendix B of `report_academic.md`. No further action.

### 2026-04-22 — Track U — Chen-Rodden Alberta validation

**Status:** COMPLETED.
**Expected outputs (delivered):**
- `analysis/v0_1_chen_rodden_alberta_validation.md`
- `analysis/v0_1_chen_rodden_alberta.py`
- `data/v0_1_chen_rodden_simulation.csv`
- `data/v0_1_chen_rodden_summary.json`

**Integration:** §3.6 rewritten to reflect mechanism correction (UCP more-packed; NDP dispersed-losses). No further action.

### 2026-04-22 — Track V — Canadian comparator base rate

**Status:** COMPLETED, partial (proxy computation; full per-cycle EG quantification flagged as future work).
**Expected outputs (delivered):**
- `analysis/v0_1_canadian_base_rate_computed.md`
- `analysis/v0_1_canadian_base_rate_compute.py`
- `data/v0_1_canadian_redistribution_base_rate.csv` (updated with 6 cycle proxies)

**Resumable work:** direct per-ED EG computation across BC 2023, Saskatchewan 2022, Manitoba 2018, etc. would strengthen the benchmark from proxy to measured. Each cycle requires 4–8 hours of spatial-crosswalk reconstruction. Flagged but not blocking.

### 2026-04-22 — Track W — OSF pre-registration draft

**Status:** COMPLETED, submission-ready.
**Expected outputs (delivered):**
- `analysis/v0_1_pre_registration_draft.md`
- `analysis/v0_1_pre_registration_platform_analysis.md`

**Pending user action:** OSF account signup + upload + embargo to 2026-11-02. Submission instructions in the platform-analysis file. ~30–45 min of PO time.

### 2026-04-22 — Track X — Approximate 2026 shapefiles + compactness

**Status:** COMPLETED, Tier C declined as methodologically out of scope.
**Expected outputs (delivered):**
- `analysis/v0_1_approximate_shape_analysis.md`
- `analysis/v0_1_approximate_shape_analysis.py`
- `data/v0_1_approximate_majority_2026_eds.gpkg`
- `data/v0_1_approximate_minority_2026_eds.gpkg`
- `data/v0_1_compactness_scores.csv`
- `data/v0_1_tierC_parent_union_reference.csv`

**Integration:** §6.7 populated with Tier A/B measurable-subset findings. No further action without commission shapefile release.

### 2026-04-22 — Track Y / Y-prime / Y-prime-prime — Shape refinement

**Status:** COMPLETED across three passes.
**Expected outputs (delivered):**
- `analysis/v0_1_shape_refinement.md` + `.py` (v1 road snap)
- `analysis/v0_1_shape_refinement_v2.md` + `.py` (v2 feature-class including waterway/admin/rail)
- `analysis/v0_1_shape_refinement_v3.md` + `.py` + `.log.json` (v3 additional red-ED passes + noise-cleanup rendering fix)
- `data/v0_1_refined_*.gpkg` (three vintages)
- `data/v0_1_boundary_refinement_impact*.csv`
- `maps/hires/` (12 × 600-DPI PNG extractions)
- `maps/verification/v0_1_*.png`, `v0_2_*.png`, `v0_3_*.png`

**Integration:** §6.7 of academic report cites the three-pass history, the three-tier boundary-confidence classification, and the 1,012 residual voter-impact figure. No further action without commission shapefile release.

### 2026-04-22 — Track Z — 2015 cross-election extension

**Status:** COMPLETED.
**Expected outputs (delivered):**
- `analysis/v0_1_2015_cross_election.py`
- `analysis/v0_1_2015_cross_election_analysis.md`
- `data/v0_1_2015_to_2019_crosswalk.csv` (87 of 87 mapped, 127 links)
- `data/v0_1_2015_cross_election_summary.csv`
- `data/v0_1_cross_election_asymmetry_3way.csv`

**Integration:** §3.5 of academic report extended with the three-election distribution. No further action.

### 2026-04-22 — Track AA — 338Canada historical stability

**Status:** COMPLETED, with material paper correction.
**Expected outputs (delivered):**
- `analysis/v0_1_338canada_historical.md`
- `analysis/v0_1_338canada_historical.py`
- `data/v0_1_338canada_historical_snapshots.csv` (77 aggregate snapshots)
- `data/v0_1_338_historical/per_riding_pre2023.csv`
- `data/v0_1_338_historical/pre2023_reallocated_*.csv`
- `data/v0_1_338_historical/stability_table.csv`
- `data/v0_1_338_historical/uniform_swing_stability.csv`
- 87 per-riding Wayback HTML snapshots

**Integration:** §3.5 rewritten, `analysis/v0_1_338canada_riding_level.md` §3 table corrected (UCP/NDP columns), structural-invariance claim retracted. No further action.

### 2026-04-22 — Consistency audit

**Status:** COMPLETED.
**Expected outputs (delivered):**
- `analysis/v0_1_sign_convention_resolution.md`
- `analysis/v0_1_consistency_audit.md`

**Integration:** 5 priority fixes applied (sign-convention footnote at §3.2 and §8.1; 89.3% → 90.5% across 7 locations; source_maps → maps in 5 files; Airdrie / Red Deer vintage tags; Calgary-Airdrie tag correction). No further action.

### 2026-04-22 — URL archival (CDX pass)

**Status:** COMPLETED, partial.
**Expected outputs (delivered):**
- `analysis/v0_1_url_archival.py`
- `analysis/v0_1_url_archival_log.md`
- `FROZEN_MANIFEST.md` updated with Wayback + archive.ph snapshot columns

**Coverage:** 19 of 27 URLs (70.4%). 8 remain unarchived pending authenticated IA session.

### 2026-04-22 — URL archival (Chrome-based retry)

**Status:** COMPLETED, 0 new captures.
**Expected outputs (delivered):**
- `analysis/v0_1_url_archival_log.md` extended with Chrome-pass appendix
- `FROZEN_MANIFEST.md` extended with retry-pass section

**Block:** Wayback IP-wide daily quota on unauthenticated Save-Page-Now. Path forward: authenticated IA account with SPN2 Bearer token. 6 priority URLs remain unarchived.

### 2026-04-22 — School-division coherence check

**Status:** COMPLETED.
**Expected outputs (delivered):**
- `analysis/v0_1_school_division_coherence.md`

**Integration:** §5.4 extended with systematic finding (20 of 21 minority hybrids cross a school-division boundary). Calgary-Airdrie tag correction applied as side-finding. No further action.

---

## Session-10 sub-agent prompts (preserved verbatim for re-run / audit)

The full prompts used to spawn each sub-agent above are preserved in the commit history (git log each sub-agent's result) and in the prior migration document entries. If a future session needs the prompt for a specific track, re-derive from the committed analysis file's methodology section — prompts were designed as self-contained briefs and the analysis file faithfully reflects the task scope.

For the record, each sub-agent was spawned with:
- A specified working directory (always `C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit`)
- A token budget (ranging 15K–50K)
- A wall-clock budget (45–150 minutes)
- An explicit no-commit / no-report-edit instruction
- A structured output contract (named files, specific formats)
- House-voice, no-emoji, version-prefix, and encoding constraints

---

## Handoff rules for the next session

**At session start:**

1. Read this file.
2. Check the "Currently live tasks" section. If empty (as expected after a clean shutdown), proceed to normal session kickoff.
3. If non-empty, for each live entry:
   - Check the "Observed on-disk outputs at last check" against the actual filesystem. If any files are present, the sub-agent had at least partially completed.
   - Decide: integrate the partial output, re-spawn the sub-agent fresh with the preserved prompt, or mark as abandoned.
4. Move resolved live entries to the appropriate Completed section with a status update.

**At session end (or when spawning sub-agents that may not finish in-session):**

1. For every sub-agent spawned this session that is still live, add an entry under "Currently live tasks".
2. Update the entry's status and observed outputs each time a TaskOutput notification arrives.
3. If the main session is about to hit a usage limit, do a final save pass: move completed entries to Completed, ensure live entries have their prompts preserved, commit this file.

This file should always be committed; it is tracked intentionally.
