---
name: Pre-registration amendment — 2026-04-26 evening (post-audit)
description: Records the discovery and remediation of nine pipeline bugs surfaced by an external AI code audit (Gemini) on 2026-04-26, three of them statistically load-bearing. Filed separately from the morning's methodology amendment because the trigger and corrective actions are different in kind. The 2,000,000-step MCMC ensemble is being re-run; this amendment is filed *before* the re-run completes and percentile placements settle.
type: project
---

# Pre-registration amendment — 2026-04-26 evening (post-audit)

**Registration:** Pre-registered signature-detection checklist for the Alberta MLA Special Select Committee's 91-seat electoral boundary map.
**Author:** Will Conner.
**Original upload:** 2026-04-23, 06:22 PM MT (OSF Registrations).
**Prior amendments today:** `v0_1_pre_registration_amendment_2026-04-26.md` (morning amendment — eleven retrospective methodology changes, scope: Bucket A enhancements + Bucket B test-result revisions + Bucket C status of prospective component).
**This amendment filed:** 2026-04-26, evening MT — *before* the corrected MCMC re-run completes.
**Reason for amendment:** External code audit by an independent AI reviewer (Gemini, Anthropic-prompted with the audit's own brief at `analysis/methodology/v0_1_external_code_audit_brief.md`) surfaced nine fixable pipeline bugs across five conversation passes. Three are statistically load-bearing. All nine are now fixed in source ([commit 73544a3](https://github.com/Ixby/alberta-electoral-boundaries-audit/commit/73544a3)) with three new regression tests covering the failure modes. The 2,000,000-step MCMC ensemble is being re-run on the corrected pipeline. **Until that re-run completes and produces new percentile placements, this amendment is the audit's truthful interim record; a follow-up "post-rerun deltas" amendment will be filed when the re-run lands.**

This amendment is filed *before* the new numbers exist on purpose. The audit's pre-registration discipline requires that material methodology changes be recorded as they happen, not retroactively after the consequences are known. If the corrected ensemble produces different percentile placements than the buggy version, the deltas amendment will name them and the public-report headline will be updated accordingly. If the corrected ensemble produces statistically equivalent placements, that will also be named.

---

## What was found

The full audit memo, with each finding's verification status against the actual code and the remediation applied, is at `analysis/methodology/v0_1_external_code_audit_findings_gemini_2026-04-26.md`. Summary tally:

| Severity | Count | Highest-impact example |
|---|---|---|
| CRITICAL | 3 | The 2,000,000-map MCMC ensemble was structurally a stack of 100 independent 20,000-step short-bursts (chain state silently reset to the 2019 baseline at every chunk boundary). |
| HIGH | 2 | `gpd.sjoin` against the v0_8 reconstructed polygons could double-count VAs that fall inside overlapping slivers. The deduplication pattern that fixes this already lived in `phase_4c_prep.py:141`; it had not been ported to `score_exogenous_map`. |
| MEDIUM/NOTE | 4 | `networkx` was an unpinned load-bearing dependency; declination sign-convention comment was wrong (empirical interpretation in the report was always correct, only the doc lied); rural-protection classifier silently bucketed seven previously-unmatched ED names as "rural"; uniform-swing shift was not clipped to [0,1]. |

All nine findings remediated; 12 of 12 regression tests pass against the fixed code (3 new tests added by Gemini's spec covering sjoin dedup, CRS reprojection, and chunked-MCMC state persistence).

---

## What this changes about the audit's headline claims

The published `report_public.md` (v0.23) cited two ensemble-derived numbers prominently:

- **The minority map's `seats@50/50` (52.8%) sat at the 100th percentile of the 2,000,000-map distribution** — i.e., not a single simulated map reached it.
- **The majority map's `seats@50/50` (43.7%) sat at the 12th percentile** — a more neutral but still UCP-adverse position relative to the simulated distribution.

Both claims are **held in revision** until the corrected 2M re-run finishes. Specifically:

**The empirical map scores have already moved** purely from the HIGH-severity sjoin dedup fix (the chain-state fix only affects the ensemble distribution, not the per-map scoring of the proposed maps). Pre-rerun verification with the dedup-fixed `score_exogenous_map` produced these revised real-map scores (post-fix, pre-ensemble):

- 2019 enacted: `seats@50/50 = 0.460` (was previously published as the same approximate value; small or no change expected here because the 2019 map has no sliver-overlap exposure)
- Majority 2026 v8: `seats@50/50 = 0.437` (vs. published 0.437 — confirms direction)
- Minority 2026 v8: `seats@50/50 = **0.542**` (vs. published 0.528 — **a +1.4 percentage-point shift** caused by the sjoin dedup fix alone, before the corrected ensemble distribution is even computed)

The minority's empirical `seats@50/50` therefore moved *upward* by ~1.4 points after the bug fix. The corrected ensemble's max — the simulation ceiling — was 51.72% in the buggy version. Whether the corrected continuous-chain ensemble reaches 54.2% (the new minority value) is what the re-run will determine. There are three possible outcomes:

1. **Corrected ceiling stays below the new minority value (most informative for the headline).** The "no map in 2,000,000 simulated maps reaches the minority's value" framing survives, with the corrected number in place of 52.8% and 51.72%. The audit's qualitative conclusion is reinforced by the bug fix rather than weakened — the dedup that *raised* the minority's empirical score is the same bug class the audit's transparency discipline was designed to surface.
2. **Corrected ceiling rises and meets or exceeds the new minority value.** The "out of distribution at p100" claim is retracted and replaced with the corrected percentile (e.g., "the minority map's `seats@50/50` sits at the Nth percentile of the 2,000,000-map distribution, where N may be < 100"). The headline framing is rewritten to honour the new number; the underlying audit conclusions about Lane 2 (structural-irregularity), the rationale-failure pattern, and the constitutional discussion are *not* affected.
3. **Corrected ensemble fails to converge or produces wildly different per-metric distributions.** The audit publishes the convergence diagnostics and the comparison delta, defers the headline claim, and explicitly invites independent reproduction in R before any percentile-based framing is restored.

In all three cases, this amendment plus the follow-up deltas report and the audit memo will be the public record of how the change was handled.

---

## What is **not** affected by the bug fixes

The retrospective component of the audit (RQ1–7) carries multiple lanes of evidence. The bug fixes affect Lane 1 percentile placements; the following stand independently:

- **Lane 2 (structural-irregularity tests).** Five-of-five firing in the same direction, computed from direct geometric measurement of district shapes, community-of-interest splits, anchoring departures, and chair-flag annotations. No MCMC ensemble involved.
- **The rationale-failure pattern.** Five of six contested redraws fail their own published rationales under independent check, computed from primary sources (the commission's published per-district rationales).
- **The qualitative findings on community splits.** Airdrie, Calgary's NW quadrant, etc. — measured directly from the polygon geometry and the 2021 census small-area frame.
- **The constitutional discussion.** Charter section 3 framework, *Reference re Saskatchewan* [1991], the April 22 SCC ruling on Quebec — these rest on legal sources, not on the audit's pipeline.
- **The April 16 process change.** Documented from primary sources (the legislative motion text, the committee composition).

These five evidentiary planks remain published in their existing form; only the percentile-ensemble claims (Lane 1 statistical-distribution placement) are held in revision pending re-run.

The prospective component (RQ8–9) — the 17-test grid that will be applied to the November 2026 Lunty committee map — is **unchanged**. The same fixed pipeline that will produce post-rerun numbers for the retrospective component is the pipeline that will be applied to the Lunty map; a single fixed codebase is in fact a *strengthening* of the prospective commitment, not a weakening.

---

## Why this amendment is filed before the re-run completes

Because pre-registration discipline asks the author to record the timing and content of methodology changes as they happen. Filing only after the re-run finishes would let the author shape the amendment's framing around whether the new numbers are favourable. Filing now binds the author to whatever the re-run produces, in the same prose, with the same discipline. The deltas report will be appended; the framing in this amendment will not be retroactively rewritten.

The next file in this sequence will be `v0_1_post_audit_recompute_deltas.md` (created when the 2M re-run completes; will record the corrected percentile placements alongside the buggy version's published values, line-by-line). At that point the public report's headline will be updated in the same commit, and a third file in this dated sequence will document any prose changes to `report_public.md`.

---

## Audit-trail anchors

- Code-audit brief (the prompt given to the external reviewer): `analysis/methodology/v0_1_external_code_audit_brief.md`
- Findings memo with verification status and remediation: `analysis/methodology/v0_1_external_code_audit_findings_gemini_2026-04-26.md`
- Remediation commit: `73544a3` ([github](https://github.com/Ixby/alberta-electoral-boundaries-audit/commit/73544a3))
- Buggy-version artefacts preserved at `data/*.buggy_pre_audit_2026-04-26.*` and `data/mcmc_checkpoints_250k_v0_8.buggy_pre_audit_2026-04-26/`
- Post-audit re-run log: `analysis/reports/v0_1_mcmc_2M_post_audit_rerun.log` (in progress at filing time)
- Forthcoming: `analysis/reports/v0_1_post_audit_recompute_deltas.md` (will be created when re-run completes)
