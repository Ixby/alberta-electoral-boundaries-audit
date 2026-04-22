# v1.2 Prompt Red-Team — Clean-Room Execution Readiness

**Author:** final red-team agent
**Date:** 2026-04-22
**Target:** `v1_2_gerrymander_audit_prompt.md`
**Purpose:** Identify anything that would prevent a cold-start Claude Code session from executing the v1.2 pipeline to clean completion.

---

## Summary

**Ready to execute with two blockers fixed.** Both blockers are documentation mismatches (script name, missing-file claim), not methodological gaps. After those, v1.2 can run.

---

## Blockers

### B1. Script name mismatch (Gate G0 will fail immediately)

Prompt references `analysis/check_wuff_voice.py` in three places:
- Line 40 (prior-work inventory)
- Line 74 (Gate G0 reproducibility check command list)
- Line 156 (PR1 publication gate)

Actual file: `analysis/check_voice_and_readability.py`. Content-wise the script matches the prompt's description. The script's own docstring line 15 still says "Usage: python3 analysis/check_wuff_voice.py..." so the rename happened on disk but was not propagated to the prompt or the docstring.

**Fix:** rename file OR update 4 locations (3 prompt + 1 docstring).

### B2. Known-constraint claim contradicts the data directory

Prompt line 23: *"No analogous minority crosswalk found in the bundle."*

`data/v0_1_minority_hybrid_crosswalk.csv` exists. Listed in `data/data_acquisition_manifest.md`. A cold-start agent that reads the prompt first will not discover it; an agent that reads the data dir first will be confused.

**Fix:** either delete the file if it is stale / incorrect / unused, or update the prompt line to state how the minority crosswalk is to be used (and for what RT gate).

---

## Material issues

### M1. Gate G0 cannot pass given current report inconsistency

Gate G0 (line 78): "Gate G0 blocks downstream work if any number differs by more than 0.05 pp or one seat." The carry-forward table in the prompt has majority B2 = −0.85%. The academic report (`report_academic.md:235`) has majority B2 = −0.78%. Difference is 0.07 pp, over the 0.05 gate.

This means Gate G0, strictly enforced, will FAIL on v1.2 cold-start — not because the scripts drifted, but because the prompt and the academic report disagree on the baseline number. Agent will halt with a gate failure that is really a documentation inconsistency.

**Fix:** resolve which EG value is canonical (see v0_2_final_redteam.md §1.1) and update the stale side before execution.

### M2. RT1 numeric thresholds vs reported current status

RT1 (lines 95–101) says the gate test is about the 95% CI and 90% CI crossing zero. "Current status" says "95% CI [−2.99, +0.76] pp crosses zero; 89.3% direction consistency. Qualified pass at ~90%."

But 89.3% direction consistency and 90% CI same-sign are DIFFERENT statistics. A directional-consistency count of 89.3% does not directly imply whether the 90% CI crosses zero. The prompt conflates these two tests in the "current status" line. Under a strict RT1 reading, the gate requires actually computing the 90% CI — nowhere does the prompt show that computation's result.

**Fix:** either (a) add an explicit "90% CI: [lo, hi]" row to Monte Carlo output and gate on it, or (b) change RT1's pass criterion to "direction consistency ≥ 90%" (simpler, matches what's actually reported).

### M3. Vision budget leaves ~130K headroom for all non-vision work

800 × 400 = 320K tokens. Total budget 450K. Remaining 130K must cover: PDF recon, 5+ script executions in Stage 3, Stage 4 refined metrics, Stage 6 report rewrites, RT1–RT6 and PR1–PR4 gate reports, CHANGELOG block, reproducibility manifest.

For a single Stage 6 report regeneration of the academic report alone (~10K tokens output × input context ~30K) the agent will burn 40K on that task. PR gates need to re-read both reports (two files at ~8K each). PDF recon alone needs ~20K. Budget is realistically ~100K short.

**Fix:** raise nominal budget to 600K (Opus 4.7 1M supports this easily), OR explicitly scope Stage 3 Vision down to ≤500 VAs, OR mark Phase 4C as a separate session.

### M4. Pre-Stage-3 PDF recon has mixed known/unknown state

Prompt line 190 under Pre-Stage-3: "3. Extract Appendix E (minority report text) for any minority-hybrid-specific language. Known result: TBD on next execution."

So the recon pre-step has two majority tasks with known results and one minority task with an unknown result. A cold-start agent running this will produce new information about Appendix E that was not available during v1.2 drafting — and no branch in the pipeline handles contingencies from that recon. What if Appendix E reveals a cheap minority crosswalk? What if it reveals mismatches with the existing minority hybrid crosswalk file (B2 above)?

**Fix:** either execute Appendix E recon before running v1.2 (close the unknown) or add an explicit decision tree: "if Appendix E reveals X, do Y; if Z, do W."

### M5. MAJORITY_2026_MAPPING correctness state unclear

Line 23: "Airdrie-East and Medicine Hat-Brooks were `blend` but should be `direct`." Prompt does not state whether the mapping has been corrected in the checked-in script or still contains the errors. If errors are uncorrected, Gate G0 numbers (current carry-forward) may themselves be wrong; if corrected, the carry-forward reflects corrected values. A cold-start agent has no way to know which without inspecting the script.

**Fix:** state explicitly: "As of v1.2 baseline, `MAJORITY_2026_MAPPING` has been corrected to mark Airdrie-East and Medicine Hat-Brooks as `direct`; carry-forward numbers in the table above reflect the corrected mapping."

---

## Symmetry violations in the prompt

### S1. Majority-side recon done; minority-side recon deferred

See M4. Pre-Stage-3 task set is not symmetric between majority and minority.

### S2. RT gates apply to vote-based findings; no analogous gate set for structural findings

RT1 (Monte Carlo), RT2 (cross-metric), RT3 (cross-election) all target the vote-based Section B. RT4 (structural vs vote-based separation) is a reporting gate, not a finding-validity gate. There is no "structural robustness" gate for Section A (A1 population, A2 Calgary zones, A3 s.15(2)), Section C (C3 anomalies, C4 community splits), or Section D (procedural + submission archive).

This asymmetry is defensible *because* the structural findings are from published documents and visual inspection with less modeling uncertainty, but the prompt does not explicitly justify the asymmetry. A hostile reviewer could ask: why does the minority's 12.2% Calgary zone gap not get a Monte-Carlo-style robustness test? (Answer: it's tested via A2 alternative classification rule G4.) That answer could be made explicit in the prompt.

**Fix (optional):** add a short statement in the two-gate-discipline section: "Structural findings are robustness-tested via integrity gates G3/G4 (alternative-classification checks); red-team gates RT1–RT3 target the vote-based findings only. This asymmetry is by design: structural findings derive from published documents with lower modeling-uncertainty than vote-attribution findings."

---

## Load-bearing assumptions that are unstated

### U1. That Stage 3 Vision assignment can be done by an agent with the same rigor as by a human analyst with QGIS

Vision-based VA attribution at ≤800 inspections is the entire Phase 4C refinement plan. The prompt does not state the accuracy floor required. If Vision gets 85% right, are the remaining 15% errors randomly distributed or biased? The prompt says Zero-Sum Verification catches errors at the ED level but not at the VA level.

**Fix:** add a "Vision assignment accuracy assumption" to the assumption inventory with a falsifiability condition: if random spot-check of 20 Vision-assigned VAs shows error rate > 10%, fall back to a non-Vision method.

### U2. That the 2026 shapefile release is not imminent

Whole-pipeline scoping (Phase 4C Vision path, MCMC blocked) is conditioned on "shapefiles will not be available before execution." If they become available mid-execution, the Vision path is pointless and MCMC becomes available. Prompt does not say what to do if shapefiles appear mid-run.

**Fix:** add a Stage 1 decision branch: "If shapefiles are released during execution, abort the Vision path, switch to Stage 2 centroid-in-polygon, and run MCMC in Stage 5."

### U3. That 2015 vote data is usable without a pre-2017-to-2019 boundary crosswalk

Public report §What is Missing item 5 notes: "The 2015 map used different district boundaries than the 2019 map. The audit could not use 2015 vote data directly in the cross-election check." Prompt line 25 says 2015 data IS in the bundle and cites it for RT3. How is RT3 using 2015 data if the crosswalk is missing?

**Fix:** clarify in the prompt whether RT3 uses 2015 at the provincial-aggregate level (which doesn't need a crosswalk) or at the ED level (which does). The text currently ambiguates.

---

## Budget math overflow check

| Item                                      | Tokens (est.) |
| ----------------------------------------- | ------------- |
| Gate G0 (5 script runs, read outputs)     | ~15K          |
| Pre-Stage-3 PDF recon                     | ~25K          |
| Stage 3 Vision (800 VAs × 400)            | 320K          |
| Stage 4 refined B1–B4 computation         | ~15K          |
| Stage 5 MCMC (blocked, skip)              | 0             |
| Stage 6 report regeneration (both)        | ~50K          |
| RT1–RT6 + PR1–PR4 gate reports            | ~20K          |
| Inter-stage reasoning / tool calls        | ~20K          |
| Reproducibility manifest + changelog      | ~10K          |
| **Total estimated**                       | **~475K**     |

Against a 450K budget, this is already over. Any mid-run troubleshooting or re-run will push significantly over. A realistic session needs ≥600K.

**Fix:** raise stated budget to 600K, or cut Vision scope in half (which harms Phase 4C precision).

---

## Publication Gate (PR1–PR4) readiness

- **PR1 house voice:** script exists under a different name (see B1). After rename, should pass.
- **PR2 readability:** current Public 7.1, Academic 11.7 — well under thresholds. Passes unless regenerated reports drift.
- **PR3 reproducibility manifest:** not currently written. Must be generated during Stage 6. Not a blocker but a required new artefact.
- **PR4 changelog:** trivial after Stage 6.

---

## Final Execution-Readiness Verdict

After the two blockers (B1 script rename, B2 minority-crosswalk claim) and the documentation inconsistency (M1 EG number) are fixed, v1.2 is executable in a clean-room session. The six material issues (M2–M6) should be addressed pre-execution but are not strictly blocking.

Without those fixes, a cold-start agent will either:
1. Halt at Gate G0 (file not found or number mismatch), or
2. Improvise around the inconsistencies, violating the prompt's own "no mid-run improvisation" rule.

Budget may also be insufficient for a complete Stage-3-through-Stage-6 run at 450K; recommend 600K.

---

*End of v1.2 prompt red-team.*
