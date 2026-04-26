---
name: External code audit brief — for an independent AI reviewer
description: A single self-contained document an audit author can hand to a different AI (Gemini, GPT, Claude in a fresh conversation) to perform an independent code audit of the Alberta Electoral Boundaries Audit pipeline. Designed to be copy-pasted into a single AI conversation as the system/initial-instruction prompt. The reviewing AI does not need any prior project context.
type: methodology
---

# Code-audit brief — please review this codebase as an independent auditor

You are being asked to perform an **independent, hostile code audit** of a public-interest forensic-redistricting research project. The author wants you to find bugs they cannot see. The author has done their own internal QA and has built a small automated test suite. They are explicitly asking you to look beyond what they have already checked and to be sceptical of their work. Treat this as adversarial code review — the goal is to surface real issues, not to flatter the codebase.

This document is everything you need. It contains the project context, what has already been validated, the specific concerns the author wants you to investigate, and the format the author wants your findings returned in. You do not need any other context to perform the review.

---

## 1. The project, in three paragraphs

**What it is.** A non-partisan forensic audit of Alberta's 2025–26 Electoral Boundaries Commission proposals. Three maps under analysis: the 2019 enacted boundaries (currently in force), the commission's 2026 majority recommendation, and the 2026 minority recommendation. The audit produces both a public-facing magazine article and a technical monograph that argue (with statistical and structural evidence) that the minority map shows measurable structural irregularities the majority map does not, including a `seats@50/50` value that no map in 2,000,000 simulated legal Alberta maps reaches. The author is a fourth-year computer-information-systems undergraduate at Mount Royal University.

**Why it matters for the code audit.** The audit's headline claims are quantitative. They will be challenged. If the Python code that produces those quantitative claims has bugs, the entire enterprise's credibility is at stake. The author has explicitly stated in the public report's "honest gaps" section that "standard scientific-software bugs almost certainly exist somewhere at low magnitude and would not be caught by re-running the same Python pipeline." Your job is to find them.

**Where the code lives.** Public GitHub repository: `https://github.com/Ixby/alberta-electoral-boundaries-audit`. Roughly 50 Python scripts under `analysis/scripts/`, written by one author over several months. Open code, open data, deterministic seeds, pinned dependencies. Reproducibility is by design; external replication has not yet been performed.

---

## 2. What has already been done

Do not duplicate this work. Build on it.

- **Pytest test suite** at `tests/test_scoring.py` — 9 tests passing as of writing, including a forensic spot-check that loads 10 randomly-chosen partitions from the verification subset and recomputes their metrics from scratch in a clean reimplementation, confirming match within 1e-6 float tolerance. **The verification subset is byte-trustworthy.** Do not re-prove this; trust it as a baseline.
- **Mypy pass** on the core scoring module surfaced 3 issues: one downstream-caller arithmetic on a returned `object` value (not a bug; a TypedDict refactor would silence it); one `for f in flags:` loop that shadows a file handle from an earlier `with open(...) as f:` block (real code-smell, not a runtime bug). Both are documented; neither is a priority.
- **Pre-registered checklist** at `analysis/reports/v0_1_pre_registration_draft.md` plus two dated amendments documenting all methodology evolution. This documents what the author committed to *before* measuring; deviations are documented.
- **Methodology files** at `analysis/methodology/` — per-claim evidence trails for the audit's substantive findings. Treat as primary-source documentation of what each script is supposed to compute.

---

## 3. What you are being asked to look for

In rough priority order. Be sceptical; the author wrote all of this.

### 3a. Bug categories the author specifically suspects exist

The author has written down their own bug-risk taxonomy. Verify or refute each. If you find a real instance of any of these, please cite the specific file and line.

1. **Off-by-one errors in groupby/aggregation/percentile code.** The audit does substantial pandas `groupby` + `sum` work (per-district vote aggregation, per-step metric scoring, per-percentile ranking). These are classic territory for bugs that don't crash but produce slightly wrong numbers.

2. **Coordinate-reference-system (CRS) silent mismatches.** `geopandas.sjoin` returns zero matches if two layers are in different CRS. The author's various scripts call `to_crs(3401)` somewhat inconsistently. A specific concern: `analysis/scripts/v0_1_mcmc_ensemble.py` builds a graph from voting-area polygons; `analysis/scripts/v0_1_targeted_gerrymander_burst.py` and `analysis/scripts/v0_1_targeted_gerrymander_burst_ndp.py` consume the same graph; `analysis/scripts/v0_1_mcmc_verification_subset.py` does likewise. Confirm the CRS handling is consistent across these.

3. **Floating-point boundary conditions in seats@50/50.** The calculation in `analysis/scripts/v0_1_mcmc_ensemble.py:seat_results()` uses `shifted_share > 0.5` (strict inequality). At exactly 0.5 (which can happen due to uniform-swing arithmetic), the district isn't won. Check whether different rounding conventions in the simulation versus the real-map scoring would produce different seat counts. Also check whether the test cases in `tests/test_scoring.py` exercise this boundary correctly.

4. **Inheritance-fill carve-out edge cases in v0_8 polygon construction.** The audit reconstructs 2026 ED polygons from commission map images and falls back to 2019 polygons for 21–22 districts where the 2026 boundaries can't be extracted. The carve-out logic occasionally produces sliver polygons. The author has handled this in the seats@50/50 metric (see `data/v0_1_mcmc_verification_*` for evidence) but please verify that:
   - The same 6 minority polygons that "catch zero VA centroids" in `analysis/scripts/v0_1_fuzz_missing_eds.py` are identified consistently across other scripts that traverse the polygons.
   - The fuzzing analysis correctly handles edge cases when an "inherited 2019 polygon" overlaps with a different 2026 polygon (potential double-attribution).

5. **Dict-iteration-order assumptions.** Python 3.7+ guarantees stable dict iteration order, but the codebase predates that target on the author's machine being explicit. If any script iterates `assignment.items()` and depends on the order being identical across runs, that's a latent reproducibility bug. The author wants this confirmed or refuted.

6. **Pandas chained-assignment / view-vs-copy patterns.** `df[df.col > x].col2 = y` sometimes modifies a copy. The audit has dozens of such patterns. Most are harmless; some might silently corrupt. Flag the worst offenders.

7. **Random-seed contamination across MCMC chains.** The author runs 4 parallel chains seeded individually. If global numpy state leaks between chain initializations, the chains are correlated when they should be independent — which would inflate ESS and tighten percentile claims artificially. The seed handling is in `analysis/scripts/v0_1_mcmc_ensemble_250k_v0_8.py` and the chunked-checkpoint logic. Confirm chain-independence is preserved.

### 3b. Methodology questions (not just code)

These are the formulas the audit computes. They are textbook formulas; the author has high confidence in them. But please confirm by independent inspection:

- **Efficiency gap.** Implementation in `analysis/scripts/v0_1_mcmc_ensemble.py:seat_results()`. Standard convention used: `(wasted_NDP - wasted_UCP) / total_votes`, with positive values indicating UCP-favoured. Wasted votes for the losing side = all their votes; wasted for the winning side = winning_votes minus the median (formal: minus `total/2` since this is a two-party seat). Confirm this matches Stephanopoulos & McGhee (2014/2015) and that the sign convention is consistent with the audit's prose.

- **Mean-median.** Implementation: `median(ucp_share_per_district) - mean(ucp_share_per_district)`. Confirm sign convention matches the literature (positive = UCP-favoured).

- **Declination.** Implementation: Warrington (2018) formula with `arctan` of the gap-from-50% / win-share-fraction. Confirm sign convention and whether the implementation handles the edge case of one party winning all districts (NaN expected).

- **Seats@50/50 (uniform swing).** Implementation: shift each district's UCP share by `(0.5 - global_UCP_share)`, count wins. Confirm this is the standard uniform-swing implementation and that shift-then-clip (`np.clip(... 0, 1)`) is the correct order.

### 3c. Reproducibility chain

- Is `requirements.txt` complete and pinned? (Author thinks yes, but please verify against actual import statements in the scripts.)
- Are random seeds set deterministically across all stochastic code paths? (Including `random` and `numpy.random`.)
- Does the MCMC ensemble's seed-setting in `v0_1_mcmc_ensemble_250k_v0_8.py` survive multiprocessing without contamination?

### 3d. Test coverage gaps

The pytest suite covers exactly one function (`seat_results`). What other functions in the codebase have *no* test coverage and would benefit most? Suggest 3–5 specific functions where unit tests would catch the highest-impact bugs.

---

## 4. What you are NOT being asked to do

Do not waste effort on:

- Style critiques (variable naming, docstring formatting, PEP-8 conformance) unless they're masking a bug
- Performance optimization — the codebase is already fast enough
- Refactoring suggestions for "cleaner architecture" — the author isn't refactoring
- Validation of the political/historical claims — those are someone else's audit
- Re-running the simulations — the verification subset proves the existing runs are byte-trustworthy

---

## 5. Output format

Return your findings as a markdown document with the following structure. Be specific. Cite file paths and line numbers wherever possible. If you can't reach a conclusion, say so explicitly rather than fabricating one.

```markdown
# Code audit findings — [your name / model name + date]

## Summary

- Total findings: [N critical + N high + N medium + N low]
- Top 3 priority items: [list]
- Overall assessment: [one paragraph — would you trust this codebase?]

## Findings

### CRITICAL — [Title]
- File: `path/to/file.py`
- Lines: [NN-MM]
- Description: [what's wrong]
- Why it matters: [what claim in the audit is affected]
- Suggested fix: [concrete code change]

### HIGH — [Title]
[same structure]

### MEDIUM — [Title]
[same structure]

### LOW / NOTE — [Title]
[same structure]

## What I did not audit

[Be honest. List sections of the codebase you didn't reach, or claims you couldn't evaluate.]

## What the test suite SHOULD cover but doesn't

[Specific function names + the bugs new tests would catch.]

## Methodology spot-checks

For each formula in §3b above:
- Efficiency gap: [matches/diverges from Stephanopoulos-McGhee 2014]
- Mean-median: [matches/diverges]
- Declination: [matches/diverges from Warrington 2018]
- Seats@50/50 uniform swing: [matches/diverges from textbook implementation]
```

---

## 6. Honest meta-context

The author is a solo undergraduate. They cannot afford a paid expert review. They are using AI assistants as a substitute. They are aware this is imperfect — please be especially careful not to be sycophantic or to confirm what they want to hear. If the codebase is fine, say so. If it has serious problems, say so. The author's pre-publication checklist requires explicit external review; your output here is a first pass that will be supplemented (when funding/access allows) by a human expert.

If you find anything that would be embarrassing if a hostile reviewer caught it first, that is exactly the highest-value finding you can produce. Tell the author. They want to know.

---

## 7. How to access the codebase

Public GitHub: `https://github.com/Ixby/alberta-electoral-boundaries-audit`

Key files (in approximate priority order):

1. `analysis/scripts/v0_1_mcmc_ensemble.py` — core scoring functions (`seat_results`, `score_exogenous_map`, `build_va_graph`, `initial_assignment_2019`)
2. `analysis/scripts/v0_1_mcmc_ensemble_250k_v0_8.py` — 2,000,000-sample MCMC pipeline (the headline simulation)
3. `analysis/scripts/v0_1_targeted_gerrymander_burst.py` and `..._burst_ndp.py` — Cannon et al. 2022 short-bursts hill-climb (UCP and NDP directions)
4. `analysis/scripts/v0_1_mcmc_verification_subset.py` — forensic verification subset (10,000 maps with full assignments)
5. `analysis/scripts/v0_1_fuzz_missing_eds.py` — fuzzing analysis on missing-ED attribution
6. `analysis/scripts/v0_1_rural_protection_test.py` — rural-vs-urban representation analysis
7. `tests/test_scoring.py` — the existing pytest suite
8. `requirements.txt` — pinned dependencies
9. `REPRODUCING.md` — step-by-step reproduction guide
10. `report_public.md` — the public-facing article (what the code's outputs feed into)

Read in that order. The first 4 files are where the highest-impact bugs would live.

---

## 8. Time budget guidance

Most of your value is in the first 2–4 hours of careful reading. The audit author needs a good first pass; they don't need a 40-hour exhaustive review. If you find something concerning in a specific file, dig in there. If a file looks clean on inspection, move on; the absence of obvious bugs is itself a finding.

Thank you. Please be honest, specific, and sceptical.
