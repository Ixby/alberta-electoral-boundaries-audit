---
name: Pre-registration amendment log (consolidated)
description: The amendments to the audit's pre-registered signature-detection checklist. Amendments 1 and 4 as filed on OSF (registration 9wp5y), and Amendment 5, which consolidates every later change.
type: project
---

> **Backward:**
> - `v0_1_pre_registration_draft.md`, OSF registration 9wp5y — the document being amended (not in this repository)
> - `v0_1_pre_registration_amendment_2026-04-23.md` and `pre_registration_amendment_2026-04-27_final_hardening.md`, OSF registration 9wp5y — Amendments 1 and 4 as filed
> - the dated amendment files merged into this log on 2026-05-12, and the unfiled entries Amendment 5 replaces — in the repository's history
>
> **Forward:**
> - `findings/README.md` — indexes this finding
> - (leaf — consolidated amendment record; reviewer-facing)

# Pre-registration amendment log

**Registration:** Pre-registered signature-detection checklist for the Select Special Committee on Electoral Boundaries' map.  
**Author:** Will Conner.  
**First upload:** 2026-04-23, 6:22 PM MDT, to OSF project 2gue9, which is private. It was not a registration. The first registrations (w2s8k, r3zm7, qsgy8) were filed on 2026-05-06 at 3:50 PM MDT.  
**Times:** Alberta time (MDT or MST) throughout, except inside the filed text of Amendments 1 and 4 and where marked UTC.  
**On OSF:** the checklist with Amendments 1 (2026-04-23) and 4 (2026-04-27), as files in registration 9wp5y (registered 2026-05-06, 22:27 MDT).  
**Amendment 5** (2026-11-01) consolidates every later change. It was filed there on 2026-11-01 at 3:13 PM MST, as registration update 6ae7b85d4c54dce4aebde274, with a pointer to it added to qsgy8, u47bq and he53s. **Amendment 6** (2026-11-02) corrects Amendment 5, Part 5; it was filed there on 2026-11-02 at 5:34 AM MST, as registration update 6ae88339b3b6e88d2bbde26b. **Amendment 7** (2026-11-02) sets out stage-by-stage scoring and the calibrated-reconstruction rules; it was filed there on 2026-11-02 at 8:20 PM MST, as registration update 6ae95303438cd6c135f38454. **Amendment 8** (2026-11-03) adds two redraw tests, the swing-zone test and neighbour-drain, calibrated before the map is scored; it was filed there on 2026-11-02 at 11:26 PM MST, as registration update 6ae97e98a6de1679355f6114. **Amendment 9** (2026-11-03) registers one further Step B calibration attempt, with version 3 of the reconstruction procedure; it was filed there on 2026-11-03 at 11:41 AM MST, as registration update 6aea2abd5e67b5390f474434. **Amendment 10** (2026-11-04) registers a third Step B calibration attempt as a reproducibility run of the assembly pipeline, which fits the pages together like a puzzle and checks the map against every page; it was filed there on 2026-11-04 at 2:51 PM MST, as registration update 6aeb59edd63871f1daf383ab. **Amendment 11** (2026-11-05) makes three workarounds from the provisional Step C run the registered procedure for the official map: the cut-voting-area sensitivity scores the map given, the redraw-test scorer takes the scored map, and a chain that does not seed is replaced by the next index; it was filed there on 2026-11-05 at 7:41 AM MST, as registration update 6aec9576dea08eafc55f6106.

---

## Table of amendments

| Date | File | Trigger | Key changes |
|---|---|---|---|
| 2026-04-23 | Amendment 1 | Five corrections after initial upload | Urban-weight parameter corrections (C1–C4); AI toolstack disclosure (C5) |
| 2026-04-27 | Amendment 4 | Final hardening | 250k ensemble locked; v0_9 topology; headline s50=48.31%@p98.5; drand seed pre-committed |
| 2026-11-01 | Amendment 5 | Consolidation of every unfiled change (earlier entries 2, 3, 8–25, 27, 28) | 40 parts, grouped by registered document; mapping table at its end |
| 2026-11-02 | Amendment 6 | The author asked who did the hostile review | Corrects Amendment 5, Part 5: the AI tools used and what each did |
| 2026-11-02 | Amendment 7 | The panel's map was published as images only, and the map can still change before it becomes law | The November map is scored in stages, on what each stage releases; numeric scores on official shapefiles, or on a reconstruction only if it passes a registered calibration; P5, P6, P7 readings; P8 erratum |
| 2026-11-03 | Amendment 8 | The author asked to carry the swing-zone test and neighbour-drain to the November map | Two redraw tests (R1 efficiency gap, R2 neighbour-drain) ranked against neutral redraws of the panel's changed territory; calibrated before filing; T4/T1 label erratum |
| 2026-11-03 | Amendment 9 | Amendment 7's calibration failed, and the shapefiles may be months away | One further calibration attempt on the same sample, with version 3 of the reconstruction, which reads rural pages; acceptance rule; pinned environment; one run, published pass or fail |
| 2026-11-04 | Amendment 10 | Amendment 9's calibration failed on one wrong placement; the author ruled its one-attempt limit artificial | A third calibration attempt with the assembly pipeline (puzzle assembly, edge snapping, representative-point assignment, sanity check against every page), as a reproducibility run on seen data; 5% population gate withdrawn |

**Note on publication status (author's ruling, 2026-10-31; not an amendment).** The audit is unpublished until November 3, 2026. Entries in this log dated before then record draft revisions made while the audit was being prepared, not retractions of published claims. Where an entry says a claim was "retracted" or "withdrawn", it means the claim was removed from the draft before publication.

---

## Amendment 1 — 2026-04-23

*As filed on OSF: `v0_1_pre_registration_amendment_2026-04-23.md` in registration 9wp5y, SHA-256 `2ba09d1bcab2a513802101a34ef160991e7fe40e808d6647ae9f7b79b762acbf` (<https://osf.io/download/69fc2ccfee9a223c53f1ff9e>). The text below is the filed text; the file's front matter and title are replaced by this heading, and its headings sit one level lower.*

**Registration:** Pre-registered signature-detection checklist for the Alberta MLA Special Select Committee's 91-seat electoral boundary map.  
**Author:** Will Conner.  
**Original upload:** 2026-04-23, 06:22 PM MT.  
**This amendment filed:** 2026-04-23.  
**Reason for amendment:** Five corrections and additions identified after initial upload. No thresholds or hypotheses were altered. Changes 1–4 correct stale weight parameters that were not updated when the central urban-weight estimate was revised from 0.70 to 0.85 earlier in the analysis session. Change 5 adds a toolstack disclosure that should have been present at initial submission.

---

### Change 1 — §11 Indices, B2 formula: central weight and sensitivity range

**Location:** §11 Indices and derived variables, B2 — Efficiency gap (EG), final sentence.

**Before:**
> For hybrid EDs, vote totals are estimated by blending the urban-core and rural-absorption portions at the specified urban weight (central estimate 0.70; sensitivity range 0.60–0.80).

**After:**
> For hybrid EDs, vote totals are estimated by blending the urban-core and rural-absorption portions at the specified urban weight (central estimate 0.85; sensitivity range 0.60–0.90).

**Reason:** The central urban-weight estimate was updated from 0.70 to 0.85 based on Calgary DA-level population density analysis conducted prior to registration. The sensitivity range was extended from 0.60–0.80 to 0.60–0.90 to cover the full parameter space tested in the analysis scripts. The initial upload retained the old values. This correction brings the pre-registration into alignment with the actual parameters used in `analysis/v0_2_packing_cracking_analysis.py` and reported in both audit reports.

---

### Change 2 — §9 Manipulated variables: sensitivity sweep values

**Location:** §9 Manipulated variables, second paragraph.

**Before:**
> The urban-weight parameter used in hybrid-district vote attribution (tested at 0.60, 0.70, and 0.80) is a modelling sensitivity parameter...

**After:**
> The urban-weight parameter used in hybrid-district vote attribution (tested at 0.60, 0.70, 0.80, 0.85, and 0.90) is a modelling sensitivity parameter...

**Reason:** Same as Change 1. The three-value list was carried forward from an earlier draft; the actual analysis tests five values. Corrected to match the scripts.

---

### Change 3 — §2 Study design, Component 2: parameter count and values

**Location:** §2 Study type, causal interpretation, and design — Component 2 paragraph.

**Before:**
> Sensitivity is tested across three urban-weight parameters (0.60, 0.70, 0.80) and three election cycles...

**After:**
> Sensitivity is tested across five urban-weight parameters (0.60, 0.70, 0.80, 0.85, 0.90) and three election cycles...

**Reason:** Same as Changes 1–2. Corrected to match actual analysis.

---

### Change 4 — §3 Pre-registered tests, S4: sensitivity range

**Location:** §3 Pre-registered tests, S4 — Efficiency gap crosses the US 7% threshold, threshold description.

**Before:**
> ...using the audit's pre-existing 85/15 urban/rural weighting (w=0.85, the central blending convention applied identically to both 2026 commission maps; sensitivity range 0.60–0.80 also reported)...

**After:**
> ...using the audit's pre-existing 85/15 urban/rural weighting (w=0.85, the central blending convention applied identically to both 2026 commission maps; sensitivity range 0.60–0.90 also reported)...

**Reason:** The sensitivity range stated here must match the range stated in the Indices section (Change 1). Corrected from 0.60–0.80 to 0.60–0.90 for consistency.

---

### Change 5 — §15 Context: declared toolstack added

**Location:** §15 Context and additional information — new paragraph appended after the Timeline entry.

**Added:**
> **Declared toolstack.** This audit was produced using the following tools: Python 3.11 (pandas, numpy, geopandas/pyogrio, shapely, pyproj, GerryChain 0.3.2, textstat, pdfplumber, rapidfuzz, osmnx); Elections Alberta GIS data; Statistics Canada DA shapefiles; pdfplumber for commission report extraction; and Claude (Anthropic), a large language model used as an analytical and writing assistant throughout the project. Claude's role included: drafting and revising report text, proposing analysis structure and section outlines, identifying consistency gaps between documents, and surfacing edge cases in the methodology (e.g., the Vote Anywhere apportionment issue and the pre-registration disclosure requirement). All substantive analytical claims — metric values, thresholds, data provenance, and code outputs — were verified against primary sources and script outputs by the author. Claude did not execute code or access external data independently; all script runs were performed by the author in a local Python environment. The use of an AI assistant is disclosed here and in both the public and academic reports in accordance with emerging norms for AI-assisted research.

**Reason:** AI use disclosure was omitted from the initial upload. Emerging norms for research involving large language model assistance (see e.g. Nature portfolio policies, 2023; ICMJE recommendations update, 2023) require disclosure of AI tools used in analysis and writing. The disclosure is additive — it documents what tools were used; it does not change any finding, threshold, or hypothesis.

---

### Summary

| # | Section | Nature | Effect on findings |
|---|---|---|---|
| 1 | §11 B2 formula | Correction — weight values | None; aligns text with scripts |
| 2 | §9 Manipulated variables | Correction — parameter list | None; aligns text with scripts |
| 3 | §2 Study design | Correction — parameter count and list | None; aligns text with scripts |
| 4 | §3 S4 threshold | Correction — sensitivity range | None; aligns text with §11 |
| 5 | §15 Toolstack | Addition — AI use disclosure | None; additive disclosure only |

No hypotheses, thresholds, research questions, scoring rules, or data inclusion/exclusion criteria were changed. The pre-registered 7% EG threshold (S4), the 10% zone-gap threshold (S1/RQ1), the four-division Airdrie threshold (S1/RQ2), and the p95 ensemble threshold (RQ5) are unchanged.

---

## Amendment 4 — 2026-04-27 (final hardening)

*As filed on OSF: `pre_registration_amendment_2026-04-27_final_hardening.md` in registration 9wp5y, SHA-256 `b023a0d43cf4fd056405f0fe7aa6d6dbb68b5a51c921b3101106b33f4e63c509` (uploaded 2026-04-27). The text below is the filed text; the file's title is replaced by this heading, and its headings sit one level lower.*

This document formally amends the audit's pre-registration. It records the final parameter locking and methodological hardening executed prior to the publication of the final academic and public reports.

### Summary of Final Procedural Updates
Following the initial post-audit review (April 26), three major structural refinements were applied to the audit pipeline to ensure maximum legal defensibility and mathematical rigour. These changes supersede all prior parameters for the published headline findings.

#### Change 1 — Finalization of MCMC Ensemble Sample Size: 250,000 Maps
**Before:** The audit explored ensemble sizes of 100k, 250k, 1M, and 2M. An earlier amendment reverted the authoritative baseline to the 100,000-map ReCom standard following convergence diagnostics.
**After:** The final, authoritative legal standard is permanently locked to **250,000 maps** (run as four parallel chains of 62,500 maps each). 
**Rationale:** To proactively stave off accusations of "p-hacking" (adjusting parameters until a desired result is found), the exact scale progression must be formally logged. The ensemble size was initially scaled from 250,000 to 1,000,000 to 2,000,000 to investigate contradictory diagnostic signals in the tail probabilities. This extreme scale-up revealed that the contradictions were not a product of insufficient chain mixing, but rather a structural imprecision in the underlying map geometry (the `v0_8` topological gaps). While the initial methodology was theoretically sound, the boundary implementation was flawed and required a complete re-write. Once the `v0_9` topological substrate successfully snapped the data to precise boundaries, the inputs became clean and the statistical contradictions resolved instantly. At that point, the audit executed standard procedure: 10,000 maps to check the logic, 100,000 to validate the distributions, and 250,000 to hit the required legal and constitutional standard. Seeing perfect consistency across all metrics at 250k, the scaling stopped, establishing the final, rigorously defensible baseline without arbitrary parameter hunting.

#### Change 2 — Hardening to `v0_9` Topological Substrate
**Before:** Spatial attribution and ensemble scoring relied on a `v0_7` and `v0_8` geographic substrate that had known topological imperfections (leaving trace gaps where municipal boundaries aligned imperfectly with Statistics Canada dissemination blocks). The resulting inheritance-fill approach achieved only partial (83-of-89) pure geometric coverage.
**After:** All quantitative metrics and ensemble scoring have been fully migrated to the **`v0_9` canonical topological substrate**. 
**Rationale:** The `v0_9` substrate forces absolute topological validity and applies a robust area-proportional logic to edge-cases. This achieves **100% geometric coverage (89-of-89 districts)**, eliminating all attribution artifacts.

#### Change 3 — Final Headline `seats@50/50` Outlier Percentile
**Before:** Prior un-hardened metrics estimated the 2026 minority map's `seats@50/50` UCP advantage at 52.8% (p98.6).
**After:** Using the fully-hardened `v0_9` topological substrate against the official 250,000-map legal ensemble, the minority map's true value is **48.31%**. This places it at exactly the **98.5th percentile** of the neutral simulation (the top 1.5%).
**Rationale:** The 52.8% figure was an attribution artefact caused by the 83-of-89 geometric dropouts. The 48.31% metric is structurally and mathematically absolute. The core qualitative finding remains completely unchanged: the minority map remains an extreme statistical outlier (only 3,750 of 250,000 neutral procedures reach this advantage) and crosses all 5 pre-registered structural irregularity tests.

#### Change 4 — Pre-Registration of November 91-Seat Map Tripwire
**Context:** To preemptively evaluate the forthcoming November 91-seat committee map without retroactively fitting tests to its outcomes, the audit hereby pre-registers the exact structural red flag ("tripwire") that will trigger a formal fail condition in automated scoring scripts.
**Registered Tripwire:** The Drain Pattern (Mid-Sized City Integrity). The audit flags an extreme structural anomaly if mid-sized cities (Airdrie, Red Deer, Lethbridge, St. Albert) are split into more than their population-dictated expected seats with >2% area overlap each. This is structurally unjustified by their populations and mirrors the engineered fractionation detected in the 2026 minority recommendation. 
**Discarded Tripwire:** The Lasso Pattern (Polsby-Popper Compactness). This test was removed from the automated tripwires. As documented in prior retractions, Polsby-Popper discrepancies evaporated under the mathematically-strict `v0_9` substrate. Using a known-brittle metric as a tripwire is scientifically dishonest and has been struck from the evaluation pipeline.

#### Change 5 — Clarification on Qualitative Outliers (The "Absolute Magnitude Fallacy")
**Context:** Critics may falsely claim that updating the minority map's `seats@50/50` metric from 52.8% to 48.31% represents a "shift toward neutrality" or a reversal of the packing finding since it drops below 50%.
**Defense:** This is the Absolute Magnitude Fallacy. Under the strict statutory constraints of Alberta's mapping rules and the 2023 vote distributions, a perfectly neutral (median) map yields only **46.1%**. Therefore, 48.31% is not "neutral"—it remains an extreme top-1.5% structural outlier (p98.5). The qualitative finding of severe geometric fortification remains absolutely unchanged.

#### Change 6 — Effective Sample Size (ESS) vs Autocorrelation
**Context:** The audit officially reports an Effective Sample Size (ESS) of roughly 375 independent draws extracted from the 250,000 total maps.
**Defense:** ReCom Markov chains operating on highly-constrained 89-node graphs inherently possess massive autocorrelation (integrated autocorrelation time τ > 300). The audit explicitly recognizes this mathematical reality. This high autocorrelation is precisely *why* the chain was scaled to 250,000 steps instead of the academic standard of 10,000. Extracting 375 perfectly independent draws from 250,000 highly-correlated steps provides statistically robust resolution for the 95th percentile.

#### Change 7 — Cryptographic Seeding for Future November Testing
**Context:** The script `drand_seed.py` was locked to round 6062459 (April 27, 2026).
**Defense:** This drand seed is exclusively bound to the *future* randomized testing of the forthcoming November 91-seat map. It is explicitly locked on April 27 to pre-commit randomness six months *before* the November data exists. The historical 250k simulation uses deterministic, hardcoded seeds (e.g., Seed 42) to ensure anyone can download the repository and achieve bit-identical mathematical reproduction of the published distributions.

### Archival and Namespace Clean-Up
To ensure procedural transparency, all historical code and data artifacts (v0.1 through v0.8) have been preserved in `historical/` subdirectories. The active project namespace has been completely de-versioned. All references to scripts (e.g. `v0_9_cross_election.py` → `cross_election.py`) have been streamlined to maintain a pristine, current-state working directory for independent auditors.

**Signed:** Will Conner, Project Author
**Date:** April 27, 2026

---

## Amendment 5 — Consolidated record of the changes made after Amendment 4

> **Status: in force.** Signed 2026-11-01 (Alberta time) on the author's direction in session ("Squash all unfiled amendments into one, even if already signed, check for accuracy, reset amendment number to reflect the next slot on osf"), with the author's decisions on how registration qsgy8 relates to the specification (Part 6) and on S6's pattern P4 (Part 24). No committee map, and no result from one, had been seen in session at signing. The committee's October 28 transcript had been read (archived 2026-11-01, 03:02 MDT, at `evidence/legislature/ceb_transcript_2026-10-28.pdf`). In it, members describe the advisory panel's proposals in words: Lethbridge divided among four ridings, three rural seats reinserted, Lethbridge lending population to Cardston. It holds no map or district list, and nothing in it was scored.

Parts 29–39 added 2026-11-01 after the corpus check, on the author's direction ('Apply all as proposed'). Part 40, and corrections to the header and to Parts 1, 2, 5, 14, 17, 18, 20, 22, 26, 27, 29 and 30, added the same day after this amendment was checked against OSF and the repository's history, on the author's direction to make sure OSF is up to date and the amendments are accurate.

**What this amendment is.** Amendments 1 and 4 are the only amendments filed on OSF; they are files in registration 9wp5y, registered 2026-05-06 at 22:27 MDT. This log now reproduces them as filed (Part 40). The audit's in-repository log (`findings/pre_registration_amendment_log.md`) also holds entries numbered 2, 3, 8–25, 27 and 28, dated 2026-04-26 to 2026-11-01. None of them was filed. This amendment replaces all of them and states only the changes still in force, grouped by the document each one changes. Numbers 5 to 7 were never used, and this amendment takes number 5. The entries it replaces are removed from this log; their full text, as signed, is in the repository's history (commit `ca539bc4` holds the last version). Numbers 6 and 7 stay unused. Amendment 26 (size-matched sets for a map of any seat count, signed on branch `size-matched-candidate`) is not part of this amendment and is not on OSF.

**Publication status.** The audit is unpublished until November 3, 2026. Where earlier entries say a claim was "published", "retracted" or "withdrawn", they mean a draft was revised. The same applies to the registered documents in `preregistration/`: where they speak of findings already published (for example "an author who has already published findings" in `lane3_process_scorecard_draft.md`, and "the audit's published headline" in `t3_2_majority_rural_isolation_design.md`), they mean the draft.

#### A. The pre-registered checklist (OSF 9wp5y; Amendments 1 and 4)

**Part 1 — Official boundaries and the canonical ensemble replace the provisional geometry and the 250,000-plan ensemble.**
- *Boundaries.* Elections Alberta's official 2026 shapefiles were received on 2026-05-06. Under the sunset clause, an in-repository commitment that was never filed on OSF (`preregistration/retraction_conditions.md` §6.1; Part 40), every metric that depended on the derived provisional geometries (v0_7 to v0_9) was recomputed on them.
- *Blend model.* The urban–rural blend model that Amendment 1, Changes 1–4 adjust was retired on 2026-05-18. Exact voting-area attribution on the official boundaries (Phase 4C) replaced it. Its urban weight no longer enters any result.
- *Ensemble.* The 250,000-plan ensemble locked in Amendment 4, Change 1 is replaced by the canonical ensemble:
  - 1,010,000 plans: 4 chains of 252,500 steps;
  - base seed 1432864451 (salt `mcmc_ensemble_250k`, drand round 5500000);
  - ReCom proposals within ±12.5%, and every plan within ±25% of a quota of 2021 population ÷ 87;
  - every plan has 87 districts, the 2019 map's count;
  - each chain starts from an 87-part `recursive_tree_part` partition, and the 2019 map supplies only the district count.
- *History of the ensemble.* It was first completed on 2026-05-12. On 2026-07-12 it was discarded and rerun from scratch, with the same seed and parameters, after a second defect was found in the checkpoint writer of `analysis/scripts/mcmc_ensemble_canonical.py` (ledger C9, C10). The rerun is the reference for every percentile.
- *What no longer applies.* Amendment 4, Changes 3, 5 and 6 describe the retired ensemble.
- *Current figures.* On the canonical ensemble:
  - the minority map's seats at 50/50 is 0.5169 (46 of 89), at p99.99;
  - its joint Mahalanobis p is 8.80 × 10⁻⁷, with a Bonferroni upper bound of p ≤ 1.76 × 10⁻⁶ (`data/outputs/simulated_ensemble_percentiles_canonical.csv`; `findings/joint_outlier_score.json`).
  These figures place 89-district maps against 87-district plans.

**Part 2 — The sunset-clause window is two weeks, not 48 hours.**
On 2026-04-26, before the shapefiles were released, the sunset clause's window was relaxed from 48 hours to two weeks. Neither window was filed on OSF (Part 40). The duty to recompute, to disclose any change of sign, and to apply the clause to both maps did not change. The shapefiles arrived on 2026-05-06. The headline recompute closed on 2026-05-18 (day 12). Full integration, including the re-run of the drain test, closed on 2026-05-23 (day 17, three days past the window) (`preregistration/retraction_conditions.md` §6.1). The same two-week window applies to the November map if it is first released only as PDF or image files (scoring specification, §2).

**Part 3 — The Alberta-calibrated efficiency-gap line.**
The efficiency gap is reported against the US 7% line and an Alberta-calibrated line. The Alberta line is Threshold #42 in `preregistration/thresholds.md` (Option D): +4.10%, the canonical ensemble's 95th percentile when it was registered. The 2026-07-12 rerun gives +4.08% (0.04084); the threshold stays at +4.10%. This replaces the "about 5%" line (4.37%) of 2026-04-26. The same +4.10% is the November test's P1 threshold.

**Part 4 — The November drand round (Amendment 4, Change 7).**
`analysis/scripts/drand_seed.py` uses drand round 5500000 (October 2025), not round 6062459. Round 5500000 was public before the salts were fixed, so it cannot anchor the November test. The November round is to be a round at or after the first publication of the committee's final map. At the time of this amendment no round has been pinned (`preregistration/seed_commitments.md`, entry `november_2026_scoring_spec`).

**Part 5 — Declared toolstack (Amendment 1, Change 5).**
Two more tools were used. Gemini (Google) reviewed the code adversarially, in five passes (unfiled entry 3, 2026-04-26). Codex (OpenAI) helped with scripting and data processing, and checked the literature review's citations (`analysis/methodology/reference/citation_verification.md`, 2026-05-06). `CONTRIBUTING.md` calls Gemini's commentary "collaborative" and Codex's "adversarial"; this part follows the records cited. Claude also worked as a coding agent (Claude Code): on the author's direction, its sessions ran scripts and committed changes, including ensemble runs, scoring and site builds. Each such change is in the repository's history.

#### B. The November 2026 scoring specification (`preregistration/november_2026_scoring_spec.md`, version 1.2)

**Part 6 — The specification and its pin.**
- *The document.* The November map is scored under this specification. It was first committed on 2026-06-10 and edited from 2026-06-10 to 2026-06-12, in commits `2cd4b21` → `4781c70` → `c12c7c8` → `d9c3520`, and then one more commit that rewrote §6. The chain that §6 gave earlier (`c12c7c8` → `00b0d6c` → `d562565`) was wrong. The specification is not on OSF.
- *Registration qsgy8.* Registered on OSF on 2026-05-06, it holds an earlier plan for the committee's 91-seat map (its Part B): four tripwires, MO #1–#4 (a city with more than 1.5 times its population-justified districts; lasso-shaped urban–rural districts; total municipal anchoring under 70%; the two samplers' seats-at-50/50 ranks more than 25 points apart), and a bootstrap seed. **The specification decides the November verdict.** qsgy8's four tripwires are scored on the same map, the same day, and reported beside the verdict; they do not decide it. Amendment 4 (filed) dropped a lasso tripwire, and no source has been found for the 70% "Canadian norm" behind MO #3 (ledger C49); both tripwires are scored as registered.
- *qsgy8's Part A premise.* Part A's H2 says the "Minority commissioners were NDP-aligned" and predicts their map would be better for the NDP (lower efficiency gap, mean-median and drain score); H3 predicts a smaller population spread on the minority map. The premise is wrong. The Legislative Assembly's notice "Electoral Boundaries Commission to soon begin consultations" (March 28, 2025; archived at `evidence/legislature/assembly_news_ebc_appointed_2025-03-28.html`, SHA-256 64b9986d5b7ec9c99df1c227773005128e37acd5fedc229e2937acf54fa9db4f) lists Dr. Julian Martin and John D. Evans, KC, the minority report's authors, as "Nominated by the President of Executive Council", and Greg Clark and Susan Samson as "Nominated by the Leader of His Majesty's Loyal Opposition". The minority commissioners were the government's nominees. Neither prediction was borne out on the official files. On H2, the minority's efficiency gap (+4.02% against +0.10%) and mean-median are the more UCP-favourable; only its drain score is lower. On H3, the minority's spread is wider on every population base, if only slightly on the 2021 census mean absolute deviation (10.2% against 10.1% of quota).
- *qsgy8's baselines.* qsgy8 says "Minority map metrics NOT computed at registration time", yet it gives minority baselines (MO #1: Airdrie in 4 districts; MO #3: "minority 89-seat map: 41%"), and its archived `drain_v2_plan.md` already reports an official-geometry drain result for the minority (21 coupled pairs). MO #3's 41% is a traced-boundary figure. On the official boundaries the minority's anchoring is 71.8% (S3's measure), so MO #3 does not fire on it. qsgy8 also calls the committee a "commission".
- *The pin.* The specification's SHA-256 is recorded outside the file, in `seed_commitments.md`, because a hash written inside the file it describes can never verify.
- *The one later edit.* The specification has been edited once since the 2026-06-12 pin. On 2026-07-12 (commit `893e6d3a`), after the ensemble rerun, §5's Bonferroni bound was updated from p ≤ 2.80 × 10⁻⁶ to p ≤ 1.76 × 10⁻⁶. The edit is recorded in `seed_commitments.md` as "Amendment A". The file's SHA-256 is now `2110548c9e82170425ba760eee1574afd83ebae96d8ce094f5f8ad278f0cdbe3`.

**Part 7 — Structural lane: midpoint anchoring.**
This replaces the rule "at least 1.5 times the majority map's value". A flag fires when the November map falls on the minority's side of the midpoint between the two commission maps' measured values:

| ID | Measure | Majority | Minority | Midpoint | Flag if |
|---|---|---:|---:|---:|---|
| S1 | Median absolute deviation of district population from the median | 2826.89 | 3938.11 | 3382.50 | above 3382.50 |
| S2 | Cities, towns and specialized municipalities (CSD types CY, T, SM) split into 2 or more districts | 23 | 30 | 26.5 | above 26.5 |
| S3 | Share of district perimeter on CSD boundaries | 0.80050 | 0.71970 | 0.76010 | below 0.76010 |
| S5 | Neighbour-drain adjacency score | 0.0072 | 0.0006 | 0.0039 | below 0.0039 |
| S6 | Hybrid patterns P1–P5 reproduced | 0 | 5 | 2.5 | 3 or more |

- *Values.* The table gives the values frozen in the specification. The runs cited below measure S3 at 0.7996 (majority) and 0.7178 (minority). The flags are the same either way.
- *Excluded.* S4 (median Polsby–Popper, 0.4366 on both maps) is measured and reported but not counted. P6 (St. Albert–Sturgeon) is listed when it matches but does not count toward S6, because the majority map has the same district.
- *Verdict.* The lane reads "replicated" when 3 or more of the 5 flags fire. On the official boundaries the minority map scores 5 of 5 and the majority map 0 of 5 (`findings/structural_battery_result.json`; `findings/structural_battery_majority.json`).
- *Disclosed: S3 and S5.* Both fire on the minority's side of the midpoint, but the audit does not treat either measure as evidence against the minority. Anchoring no longer separates the two maps as a finding (minority 71.8%, majority 80.0%, either side of the 2019 map's 75.1%; Part 31). On the drain test the minority is the less adjacency-coupled map, a registered pass (`preregistration/retraction_conditions.md` §3.4). A November map with 72% anchoring would still fire S3 and count toward "replicated".
- *The script.* `analysis/scripts/run_structural_battery.py` flags S1 at 3382.50 or above, and S5 below 0.0039018, the unrounded midpoint of 0.0072127 and 0.0005909.
- *Specificity.* The lane is a screen, not a significance test. How often each flag fires on neutral maps is reported beside the verdict:
  - S1 fires on 255,934 of the 1,010,000 canonical plans (25.34%; 87-district plans).
  - A calibration on 200 neutral 91-district maps from set D (`findings/structural_lane_calibration_2026-10-31.md`; not a registered test) found the lane reading "replicated" on 93.5% of them.

**Part 8 — §1 agrees with §3.** The first outcome in §1 requires at least two of P1–P4 in the UCP direction, as the §3 verdict rule does. The earlier "at least one" was a drafting error, not a separate threshold.

**Part 9 — Declination sign (P3).** Declination is (2/π)(θ_D − θ_R), as Warrington (2018) defines it: positive favours the UCP (`analysis/scripts/mcmc_ensemble.py:227`). The canonical chain files carry this sign. On the canonical ensemble:
- minority map: +0.0770 (p98.79);
- majority map: −0.0267 (p21.85);
- 2019 map: +0.0451 (p91.33).

The same sign applies in the registered documents. With it, the minority's declination is +0.077 (p98.79) and agrees with the efficiency gap, mean-median and seats at 50/50: four of four. These statements are withdrawn:
- B6 "disagrees with B2" (`null_hypotheses.md` §1.2, the §7.1 table and the §7.2 list);
- "declination reverses" and "3/4" direction consistency (`null_hypotheses.md` §2.6; `retraction_conditions.md` §2.2 and §2.6 C);
- the old-sign row in `seed_robustness_rerun.md` Section C (−0.0770, at p1.89 and p1.21).

**Part 10 — Reference ensemble.** §2 calls the canonical ensemble fixed. It was regenerated on 2026-07-12 (Part 1), before any committee map existed, under the same paths, seed and parameters. P2–P4 are placed against the rerun. P1's threshold stays at +4.10%.

**Part 11 — Publication step.** In §7, step 5, `python analysis/scripts/build_html_reports.py` is withdrawn; the script no longer exists. The step is `cd viewer && npm run build`, plus the commit of the markdown reports. The 72-hour commitment is unchanged. §7 also says `run_structural_battery.py` and `verdict_synthesis.py` do not exist yet; both now exist in `analysis/scripts/`.

**Part 12 — The committee's name.** The specification calls it the "Special Select Committee". It is the Select Special Committee on Electoral Boundaries, created by Government Motion 37, passed on 2026-04-21. This amendment does not edit the file.

#### C. Test X1 (Recommendation 5), scored beside the specification

**Part 13 — How X1 is scored.** X1 is not in the specification.
- *Conditions (a)–(c),* against the majority map (district lists in `viewer/static/mapdata/lunty_bounds.json`):
  - (a) no change to any division in Airdrie, or with territory south of Airdrie's southern boundary, except Drumheller-Stettler (41 divisions);
  - (b) no change to any Edmonton division north of the North Saskatchewan River (11 divisions);
  - (c) Edmonton divisions south of the river match the commission's October 2025 interim map (10 divisions), with its stated Nisku option.
- *When a division is unchanged.* One district of the new map holds at least 99% of the division's 2021 population, and that district's population is at least 99% from the division. Population is the voting-area 2021 census overlay (`data/va_pop_from_das.csv`), assigned by each voting area's representative point. A strict reading (100% and 100%), with the population moved, is reported beside it; it does not decide the result.
- *Condition (d)* ("consider restoring" a Clearwater County and western Mountain View County division with s.15(2) status) has three states:
  - adopted: a division made mostly of those areas, with s.15(2) status or within ±25%;
  - considered with a stated reason tied to the Act's factors;
  - not shown.
- *The result.* X1 is met only if (a), (b) and (c) are met and (d) is adopted or considered with a stated reason.
- *If the interim map is missing.* The interim map is not in the repository. If it is not available when scoring begins, (c) is reported as not scored. X1 is then not met if (a) or (b) fails, and is otherwise not determinable.
- *Reported beside X1, not deciding it:* (d) read strictly (restored or not), and the share of the other 27 majority divisions that come back unchanged.

#### D. Size-matched neutral maps and three added tests (beside the specification)

**Part 14 — The size-matched sets.**
- *The headline is unchanged.* The specification's comparison with the 87-district canonical ensemble stays the headline. Beside it, the November map is scored against neutral maps with its own number of districts. Sets exist for 89 and 91 districts.
- *How the chains are run.* All sets use `analysis/scripts/close_seats_ensemble.py` (mode `nk`) on the canonical ReCom harness:
  - ±25% statutory constraint;
  - 2023 election-day voting-area substrate;
  - 2021 voting-area population.
- *How the chains are seeded.* The seed is (base_seed × 100,000 + idx × 1,000) mod 2³², with base_seed = `get_canonical_seed("mcmc_ensemble_250k")`. Each chain starts from `recursive_tree_part` at epsilon 0.25.
- *The four sets:*
  - **A.** ReCom proposals within ±12.5%. Indices from 200 (91 districts) and from 100 (89 districts).
  - **B.** The statute's band: proposal epsilon 0.25 (EBCA s.15(1)). Indices 230–239 and 130–139.
  - **C.** Set B plus GerryChain's region-aware ReCom, with a soft surcharge W = 0.5 on 2021 census subdivisions. W is anchored to the 2019 enacted map: the share of 169 CSDs split beyond need, R = 0.166 (28 of 169), falls at W ≈ 0.51 (91 districts) and W ≈ 0.54 (89). W = 1.0 is not used. C is a sensitivity reading, not a test. Indices 241, 243, 244 and 245, and 140 and 141; a further failure takes the next free index in the block.
  - **D.** The statute's band plus the s.15(2) exception, using the split rule in Part 15. Indices 251–254 and 150–151; index 250 is retired because it does not seed. Chains run on the superseded s.15(2) table are not reported.
- *Which set is primary.* **Set D is the primary size-matched comparison.** Sets A, B and C are reported beside it, each labelled, and every set appears in one table for every measure.
- *Harness fixes.* The fast-fail for infeasible pairs, the checkpoint and resume, the rebuilt partitions, and the correction of the unreachable s.15(2) branch in `mcmc_ensemble.py` all preserve the distribution. They are at commit `01095181`. Chains 201 and 100 ran before these fixes and later chains after; both are valid draws from the same distribution.

**Part 15 — The s.15(2) criteria (set D and real maps).**
- *Source.* `analysis/scripts/s15_2_criteria.py` computes the criteria from one per-voting-area table, the same for neutral and real maps: `data/outputs/s15_2_va_criteria.csv`, SHA-256 `48c928b8716f6ed218065e01a912ecabd11518917ac9e312376e4d603ee2fafc`. The statute's text is in `preregistration/terms_of_reference.md` §3d–3e.
- *The criteria:*
  - **(a)** The district's area, measured in Canada Albers (ESRI:102001), is over 20,000 km². The 15,000 km² surveyed-area limb is treated as not met; this errs strict.
  - **(b)** The shortest route on the OSM highway layer (motorway, trunk, primary and secondary roads) is over 150 km. It runs from the node nearest the Legislature Building (53.5336° N, 113.5068° W) to the nearest point where a highway reaches the district's boundary, or to a highway node inside it. A district no highway reaches meets (b). Leaving out local roads errs lenient.
  - **(c)** No "town" over 8,000 people (2021 census) holds 2% or more of its population in the district. A town is a city or town (CSD types CY and T), or the urban service area of a specialized municipality: its dissemination areas at 400 or more people per km². Crowsnest Pass is excluded under s.15(3). Two urban service areas pass 8,000: Sherwood Park (68,784) and Fort McMurray (58,964). The reading that counts legal town status alone was examined and not adopted.
  - **(d)** The district holds at least 10% of the area of an Indian reserve or a Metis settlement:
    - reserves: Natural Resources Canada's legal boundaries, 152 reserves, SHA-256 `f87795a1…b8d0`;
    - settlements: the Government of Alberta layer, 10 polygons covering 8 settlements, SHA-256 `5e7c1270…c1e5`.
  - **(e)** The district's voting areas share at least 1 km of edge with the provincial boundary.
- *Split rule.* ReCom accepts a cut when both new districts hold 50% to 125% of the average population. A plan is valid when every district is within ±25%, except that up to four districts may hold 50% to 75% of the average if each meets at least three of (a)–(e). The Commission's "opinion" is modelled as the criteria being met. The share of plans with 0 to 4 such districts, and where they fall, is reported.
- *Checked against the commissions.* Every district that a commission placed under s.15(2) qualifies (`data/outputs/s15_2_real_maps.json`). The one disagreement is Lesser Slave Lake's (b): 134.0 km by highway, where the commission counted (b) as met (final report, p. 248). The literal reading stands; the district still qualifies on (a), (c) and (d).

**Part 16 — When a size-matched result is final.**
A result is final when its measure's effective sample size, summed over chains by the canonical estimator (Geyer's initial positive sequence), is at least 400 and the estimator's lag cap did not bind. Otherwise it is reported as provisional, with its effective sample size, and re-scored as chains complete. This replaces the earlier rule of 20,000 plans.

**Part 17 — Three added tests,** each flagged against the size-matched sets and reported beside the specification's verdict table:
- **Towns split beyond their minimum.**
  - *Rule.* Covers cities and towns (CSD types CY and T) of 20,000 to 150,000 people. Pieces are districts holding at least 2% of a town's population. A town is flagged when its pieces exceed ceil(population ÷ (1.25 × average district population)).
  - *Statistic.* The count of flagged towns, flagged at or above the 95th percentile. Each flagged town is listed.
  - *Baselines.* Majority 0; minority 6.
  - *Label.* A flag means "splits more towns than a population-only neutral map", not "more than the law asks". Set C gives the comparison with maps that weigh municipalities.
  - *Reported beside it, with no percentile.* The splits of the Sherwood Park and Fort McMurray urban service areas, compared with the 2019, majority and minority maps.
  - *Relation to Amendment 4.* The test extends the Drain Pattern (Amendment 4, Change 4) to every city and town in the range.
- **City versus rest.**
  - *Rule.* A Calgary or Edmonton district has at least 50% of its population in that city. The statistic is (mean population of those districts − mean of the rest) ÷ mean of the rest, flagged at or above the 95th percentile.
  - *Baselines.* Majority −0.7% and minority +5.4%, on 2021 census population.
  - *Commission's tables.* On the commission's populations, with districts classed by name, the values are +9.2% and +15.9%. The difference in source and classification has not been separated.
  - *Label.* A flag means "a larger gap than population-only neutral maps", not "beyond what the law allows".
- **Competitive seats.**
  - *Rule.* Districts whose UCP–NDP two-party gap on 2023 election-day votes is within 4 points, flagged at or below the 5th percentile.
  - *Baselines.* Majority 13; minority 4; 2019 map 10.
- *What was known when they were set.* The three tests were signed on 2026-10-29 at 18:20 MDT. At 17:52 MDT that day the author had uploaded to the session a Facebook meme about the advisory panel's draft (`preregistration/evidence/2026-10-29_facebook_meme_panel_draft.md`; who posted it is unknown, and its claims are unverified). Two of the tests address its claims: the town-split test (Lethbridge split into four ridings; Okotoks split) and the city-versus-rest test (Calgary and Edmonton ridings averaging 7,000 more residents per MLA). No panel or committee map had been published or seen.

**Part 18 — What was known before set D was made primary.**
Before set D was made primary (2026-10-31, 00:00 MDT), the flags for the two commission maps against the 89-district sets had been computed and committed (commit `2ecd7931`, 2026-10-30 19:07 MDT; `findings/size_matched_results_2026-10-30.md`, provisional). By the author's account, those flags had not been looked at.

| Map | Measure | A | B | C | D |
|---|---|---|---|---|---|
| Minority | Competitive seats | p0.2 flag | p0.2 flag | p0.1 flag | p0.3 flag |
| Minority | City versus rest | p99.9 flag | p93.0 | p87.8 | p71.7 |
| Minority | Towns split | p33.3 | p45.0 | p100.0 flag | p47.5 |
| Majority | All three | no flag | no flag | no flag | no flag |

Choosing set D removes the minority map's city-versus-rest flag from the primary comparison. It is still reported under set A.

The only information the audit then had about the advisory panel's draft was the Facebook meme described in Part 17.

#### E. `preregistration/thresholds.md`

**Part 19 — Errata (no threshold moves).**
- The ±25% band is EBCA s.15(1), not s.14.
- Option C (#41) is complete (2026-05-12). 42 items are catalogued, 41 of them thresholds.
- The official shapefiles arrived on 2026-05-06. The s.15(2) area figures are still taken from the commission's text.
- Option D's registered threshold is +4.10%. The rerun ensemble's 95th percentile is +4.08%. Against that ensemble the minority map is at p94.54 and the majority map at p16.52; the ensemble's median is +1.63% and n_eff is 1,413–1,522.
- §B.2.1.D: every canonical neutral plan has 87 districts, and the band applies around a quota of 2021 population ÷ 87. The 89-district shapefiles only score the commission maps.
- Part A, row #42 gives the ensemble's 95th percentile as +0.0410 and cites `data/simulated_ensemble_percentiles_canonical.csv`. The file is at `data/outputs/`, and the rerun gives 0.04084. The registered threshold stays +4.10%.
- Rows #3 and #4 give s.15(2)(b) as "> 100 km from major centre" and (c) as "4,000 residents". The Act reads more than 150 km by highway from the Legislature Building, and no town of more than 8,000 people (`preregistration/terms_of_reference.md` §3d). The audit computes the Act's values (Part 15). B.1.3–B.1.5 and D.1 item 2 repeat the same errors: "100 km … major centre", "4,000 or more residents … Used directly", criterion (d) as a "significant Indigenous population", and "All six … used directly". The Act's (d) is that the division contains an Indian reserve or a Metis settlement (s.15(2)(d)).
- B.1.5 gives Canmore-Banff 1 of the 5 criteria and Rocky Mountain House–Banff Park 2. Computed on the official boundaries, they meet 3 and 5 (`data/outputs/s15_2_real_maps.json`).
- Rows #14 and #15 still hold the urban weight before Amendment 1 (0.70; range 0.60–0.80). Amendment 1 set 0.85 and 0.60–0.90, and Part 1 retired the model.

**Part 20 — When the packing thresholds were set.** The P1 and P2 thresholds first appear in commit `282bc6d` (2026-04-22, 10:56 MDT), the commit that records the detection run, so the packing test is exploratory. The earlier commit `5b0bc06` (08:32 MDT the same day) adds the v1.2 prompt and the analysis script without either threshold. These statements in `thresholds.md` are withdrawn:
- B.3.2: the additive choice "was set before detection (git commit `5b0bc06`, 2026-04-22 08:32:20 −06:00, two hours before the detection run `282bc6d` at 10:56:11)";
- D.2 item 1: "pre-registration (git commit `5b0bc06`)" for P1;
- D.2 item 2: "pre-registration" for P2.

Scenario E1's response already says the choice was made in the detection commit. The claim that P1 "predates detection by 2 hours 24 minutes" was removed from the draft earlier.

#### F. `preregistration/retraction_conditions.md`

**Part 21 — Errata.**
- The commission's rules are in the Electoral Boundaries Commission Act, not the Electoral Divisions Act.
- An uncited "§ 16" is dropped.
- The committee was created by Government Motion 37, not "Motion 19".

**Part 22 — Condition 4.3 B (Trade-off Frontier; Issue #14): direction of the inference.**
- *What is unchanged.* The test: the Issue #14 counter-map challenge, judged by the same community-of-interest and anchoring criteria.
- *What a successful counter-map does.* A "Symmetric-Airdrie" counter-map strengthens the finding, because it shows the minority's low anchoring was not required by its stated reasons.
- *What weakens or retracts the finding.* A demonstration that no constraint-legal map achieves the minority's claimed community-of-interest preservation with anchoring comparable to the majority's. Decisive evidence of that retracts the finding.
- No counter-map has been filed. The §8 table row "4 Statutory Silence" is read the same way.
- `seed_issue14.md`'s success row ("Best plan anchoring ≥60% … §5.8.5 retracted under condition B") is read the same way. Its 60% bar is met by both official maps (minority 71.8%, majority 80.0%), so the test no longer separates them.
- Part 31 withdraws the §5.8.5 anchoring finding under condition 4.3 A, so condition 4.3 B has no finding left to act on. This part records how 4.3 B reads, for the record and for any later use of the challenge.

**Part 23 — Condition 4.1, "Visible anomalies (3 chair-flagged)".**
- *The reading.* The final report puts these objections in the majority's own section, written as "we":
  - the geometric objections, pp. 62–63;
  - "bad faith effort", p. 10;
  - "no public support", pp. 59 and 62.
  The chair is one of the three commissioners who signed it. The condition is read as "flagged by the commission's majority, the chair among them", and its registered name is kept.
- *Edmonton-Windermere.* The condition's list includes an "Edmonton-Windermere stepped boundary", which the report's objections do not mention. The audit's confirmed three are:
  - Rocky Mountain House–Banff Park;
  - Calgary-Nolan Hill–Cochrane;
  - the Olds–Three Hills–Didsbury reach into Airdrie.
  The wording stays as registered.
- *Also read this way.* §5.1's heading, "Chair's 'no public support' claim".

#### G. `preregistration/null_hypotheses.md`

**Part 24 — "Chair-flagged" and the "no public support" claim.**
- *Where it applies.* The §5.8.2 rows ("chair-flagged visible anomalies") and §7.2 item 5 (the "chair's 'no public support' claim") are read as the commission's majority's, as in Part 23. Names, tests and thresholds are unchanged. The file's other mentions of the chair's flags are read the same way.
- *Not covered: S6.* S6 in the scoring specification ("Chair-flagged hybrid patterns") is not covered by this reading. Its predicates were set from the chair's addendum to the majority report (final report, p. 67), and it is unchanged.
- *Disclosed: pattern P4.* One of S6's patterns is not one the chair objected to. P4 is a Calgary district joined with Bearspaw or Rocky View. In the addendum the chair wrote that he did not consider the Bearspaw and Springbank hybrids "necessarily unreasonable", and "may well have agreed with them" (p. 67). P4 stays in S6 as registered; the label is disclosed here, not changed in the test.

#### H. `preregistration/lane3_process_scorecard_draft.md` (OSF u47bq; the OSF copy stays frozen)

**Part 25 — Facts, and how the cells are read.**
- **P1 and P7.** The committee has six members: four UCP, including the chair, and two NDP. P1 is read as "six members, four of them government MLAs", not as a vote count. The Standing Orders (effective 2026-03-16) do not settle whether the chair votes on every question. P1 stays Partial and P7 stays Yes.
- **P4.** The commission received 1,345 written submissions: 198 before the interim report and 1,147 after (final report, p. 14). The cell stays Yes.
- **P6.**
  - The Lieutenant Governor in Council appoints the commission's chair (EBCA s.2(1)(a)), not the Chief Justice.
  - The committee was created by Government Motion 37, not "Motion 19".
  - The commission's cell stays Yes.
  - P6 scores the body whose vote settles the map. For the committee process that is the committee, chaired by a government MLA: No.
- **Count.** Counted by the cells as defined, the committee process scores 1 Yes, 1 Partial, 5 No and 2 Pending.
- **P9** stays as registered: "without precedent among the reviewed cycles". Bratt's description of the 2026 process as without precedent in Canada stands. Alberta's 1992 committee was a different case: it followed a deadlocked commission whose five members filed five separate reports. It is not a precedent for 2026.

#### I. `preregistration/seed_commitments.md` and `preregistration/README.md`

**Part 26 — Errata.** The canonical ensemble has 1,010,000 plans, not 100,000. `seed_issue14.md` is the seed commitment for the Issue #14 counter-map challenge, not the canonical ensemble's; it was never filed on OSF (its "OSF submission pending" is read that way, Part 29). `seed_commitments.md` also calls qsgy8 the "MCMC seed" registration and lists it as the specification's "OSF mirror". Neither holds: qsgy8 (2026-05-06) holds a Phase 2 comparison and the prospective plan in Part 6, with a bootstrap seed (drand round 5500000, salt `lunty-bootstrap`), and it predates the specification. Registrations w2s8k, r3zm7, qsgy8, 6pt83, yvc7g, s58a6 and he53s each carry the same two plan files beside their own form (he53s's own plan is in its form); the checklist and Amendments 1 and 4 are in registration 9wp5y.

`README.md` says every document not marked DRAFT "was committed before the corresponding data was examined". Several were written after some of their data had been examined, and each says so: `t3_2_majority_rural_isolation_design.md`; the SZAT registration 6pt83 (`seed_commitments.md`); Section A of `seed_robustness_rerun.md`; `null_hypotheses.md` §2.5; the retrospective column of `lane3_process_scorecard_draft.md`; and `thresholds.md`'s P1 and P2 (Part 20). The README's table calls `retraction_conditions.md` "Named conditions (G0–G5)"; it is read as "Named retraction conditions by finding (§§1–7)". The table also leaves out `osf_forest_recom_robustness.md` (OSF he53s), `t3_2_majority_rural_isolation_design.md` and the `evidence/` folder.

#### J. `preregistration/osf_forest_recom_robustness.md` (OSF he53s)

**Part 27 — Changes made after filing.** Registration he53s was filed publicly on 2026-07-09 at 23:42 MDT, before any Forest-ReCom sample existed. Afterwards:
1. The execution harness was wired (chain salts and burn-in per §6.4), and `run_ensemble` gained a `proposal_method` parameter, which leaves the default path unchanged.
2. A crash at chain-0 seeding (a missing import) was fixed. It happened before any proposal was drawn.
3. The executed code was committed after the run, not before it.
4. The sampler is multi-root Wilson (loop-erased random walk). §6.1's "Aldous-Broder" names a different algorithm that samples the same distribution, and §6.1's own citations point to Wilson's method.
5. The ESS target (at least 200 per metric per chain) was missed: pooled n_eff was 61–124. The result was reported with the shortfall disclosed. That choice was made after the run.

The hypotheses, the ±5-percentile-point decision rule, the run size, the seeds and the output paths were executed as registered. All four metrics are Robust.

Errata in the filed text, read as follows:
- §6.2's quota is 2021 population ÷ 87, not ÷ 89.
- No s.15(2) exception applies. The canonical run applies none (Part 1), so §4's "three statutorily-protected s.15(2) districts" and §6.2's "same s.15(2) special-district exceptions as the canonical run" do not describe it.
- The start map is redrawn by `recursive_tree_part` when the 2019 map breaks the band, as it does on 2021 population (Part 1); §6.2's "2019 enacted 87-district map" is the start only when it fits.
- §6.3's rejection of round 5500000 for the November test is in the specification's pin row in `seed_commitments.md`, not in "Amendment A §1".
- §6.4's target of 200 per chain is not "a quarter of the canonical run's per-chain n_eff"; that n_eff is about 355–380.

#### K. `reports/academic/report_academic.md` §6.2.6 (pre-committed falsifiers)

**Part 28 — The premise of item 2 is struck.** The item no longer opens with "The 2019 cross-election direction reversal extends to 338Canada April 2026 polling". On the official 2019 files there is no reversal: the minority remains the more UCP-favourable map (ledger C44). The test stands as written: if more recent polling shows the direction flipping under several 2020s-era voter distributions, the structural pattern becomes harder to read as engineering. (Item 1 follows Part 22.)

The registered documents are read the same way. On the official files the minority's efficiency gap is the more UCP-favourable on 2015, 2019 and 2023 votes (`thresholds.md` B.2.1.C table: +10.54% against +7.58%, −0.49% against −1.32%, +4.02% against +0.10%). "Direction reverses (2019 = +0.75 pp, 2023 = −0.51 pp)" (`null_hypotheses.md` §1.2 B3), "2019 flips" (§7.1 rows B2 and B3; §7.4) and "a direction reversal" (`thresholds.md` B.5.6) refer to the retired blend model.

#### L. Errata found in the corpus check of November 1, 2026 (registered documents)

Each erratum below states what the registered text says and how it is now read; the errata are not written into the files. No test or threshold changes. The files in `preregistration/` have been edited in place before, and the repository's history records each edit: for example, the errata of the unfiled entry 18 (commit `2c06ba32`, 2026-10-29) and the repointing of their amendment references to this amendment (commits `189a4ea5` and `578f4f49`, 2026-11-01). The copies on OSF stay as filed.

**Part 29 — OSF identifiers in the registered documents.**
- `thresholds.md` (header `osf_id: r3zm7`), `retraction_conditions.md` (`w2s8k`) and `terms_of_reference.md` ("OSF w2s8k (primary audit registration)") are not on OSF. The registrations their headers name hold the two plan files (Part 26) and their own forms: w2s8k registers the DPG v11 geometry validation, r3zm7 the neighbour-drain label-shuffle null.
- `null_hypotheses.md` names OSF 2gue9 as its "public pre-registration" and says its criteria are "verifiable at" that link. 2gue9 is a private project; readers cannot open it. An earlier version of the file (`null_hypothesis_and_exoneration_criteria.md`, uploaded 2026-04-27) is in 9wp5y, registered 2026-05-06 at 22:27 MDT.
- Its "OSF Track W, filed 2026-04-23" is the checklist's first upload. The checklist was registered on 2026-05-06 at 22:27 MDT (9wp5y).
- Its §5 says an amendment "will be filed citing this document as Change 7". It never was.
- `retraction_conditions.md` §0 and §6.1 speak of "the four OSF registrations" carrying the two plan files. Seven carry them (Part 26). OSF holds nine registrations in all: w2s8k, r3zm7, qsgy8, 6pt83, 9wp5y, yvc7g, s58a6, he53s and u47bq.
- Status lines that say a filing is still to come are read as follows. `lane3_process_scorecard_draft.md` ("OSF registration — pending") is registration u47bq, registered 2026-07-14 at 2:09 AM MDT. `osf_forest_recom_robustness.md` ("form to be filed") is registration he53s, registered 2026-07-09 at 11:42 PM MDT. `seed_issue14.md` ("OSF submission pending") describes a filing that was never made; no OSF record matches it.

**Part 30 — `seed_commitments.md`: what qsgy8 and 6pt83 hold.** Part 26 corrected the labels; this part corrects the substance.
- qsgy8 was filed about six hours after the official shapefiles arrived: they came at 09:51 MDT on 2026-05-06, and qsgy8 was registered at 15:50. It names only the salt `lunty-bootstrap`. It does not hold `mcmc_ensemble_250k`. So the salt table's "OSF qsgy8 … Predates EA shapefiles", and the statement that the salt "was registered in … qsgy8 before any ensemble results were observed", do not hold.
- 250,000-plan results existed by 2026-04-27 (Amendment 4), and Amendment 4, Change 7 records that the 250,000-plan run used fixed seeds (for example, seed 42).
- 6pt83 is the SZAT registration, so the statement that none of the OSF registrations specifies the SZAT method is withdrawn.
- The OSF records disagree on when the seed commit `d2aea42` was made: 6pt83, w2s8k and r3zm7 give 2026-05-06, and s58a6 gives 2026-04-27. The commit itself (`d2aea425f379f4d60cb37883b13fcf33d9cd9d55`, on GitHub) is dated 2026-05-06 at 15:44 MDT, about six hours after the shapefiles arrived. s58a6's date is wrong. The copy of `drand_seed.py` uploaded to OSF on 2026-04-27 (in 9wp5y) holds no salts. So the statement that `"szat-bootstrap"` was committed on 2026-04-27, nine days before the shapefiles, does not hold.
- The timeline table names an Elections Alberta staff member. It is read as "received from Elections Alberta (data request)".

**Part 31 — Municipal anchoring: condition 4.3 A has been met.** On the official boundaries the minority's municipal anchoring is 71.8% and the majority's 80.0%, a ratio of 1.11× (`findings/structural_battery_result.json`; `findings/structural_battery_majority.json`). That is what `retraction_conditions.md` condition 4.3 A describes: the ratio "collapses toward 1×". Under its §0 the §5.8.5 anchoring finding is withdrawn. Part 22 changed only condition 4.3 B. In `null_hypotheses.md`, C5 (pass if the ratio is 2 or less) now passes. The §7.1 rows that call the anchoring figures and ratio "Structural-Robust-Durable", §7.2 item 4, §7.3 ("the audit's cleanest finding … this one survives") and the §7.8 row no longer hold. The traced figures they cite (71.0% and 14.5%; 4.9× to 5.1×) are superseded.

**Part 32 — The §5.3 signatures on the official maps.** No formal signature is detected on the official maps (packing fails its margin test; cracking and the engineered-boundary signature are not detected).
- *Packing (§5.3.1).* Not detected: P2 fails on the official attribution. The minority's Calgary Zone A has 8 of 17 districts won by the NDP. Their mean winning margin is 15.0 points against a provincial mean of 27.6, so 12.6 points below, where P2 needs 15 above (`data/outputs/packing_signature_rescore_2026-11-01.json`; `analysis/scripts/packing_signature_rescore.py`). The file §5.3.1 cites (`votes_2023_minority.csv`) gives 9 of 17, 12.3 points below. P1 still holds: Zone A districts average 11.5% above the provincial mean, against 2.8% on the majority map. That is a population-equality finding. The test was always exploratory (Part 20).
- *Cracking (§5.3.2).* Not detected on the official boundaries (ledger C46).
- *Engineered boundary (§5.3.3).* Rocky Mountain House–Banff Park is not detected under the registered reading (Reading A). It is detected only under a reading adopted after the fact.
- *How the registered text is read.* `thresholds.md` C.2 gives the minority's Zone A as "13 of 17 NDP-won districts" with a margin of about +18 points above the mean. 13 of 17 is the majority map's count in the cited file, and P2 fails at each of C.2's settings (12, 15 and 18 points). C.1's "Packing signature detected" lines and C.4's P2 row are read the same way. In `null_hypotheses.md`, the §7.1 rows for the three signatures, §7.2 item 2 ("All three §5.3 signatures") and the §7.8 row no longer hold, and A3's "Current: 1 (RMH-Banff Park) vs 0" is read as not detected under the registered reading. `retraction_conditions.md` §3.1–§3.3 have no detected signature left to retract. The checklist's §2 (9wp5y) says the audit "detected three formal gerrymander signatures" under the minority map; on the official maps it detects none. The checklist's November criteria are unchanged.

**Part 33 — Population spread (A1) is not Durable.** `null_hypotheses.md` §7.1 calls A1 "Plan-B invariant" and "Structural-Durable", §7.2 item 1 says the minority is "materially looser on every metric", and the §7.8 row tags A1 [SRD]. None of this holds across population bases. On the 2021 census the mean absolute deviation is 10.2% of quota for the minority and 10.1% for the majority (report Appendix C). The 48% gap (4,707 against 3,180) is on the commission's 2024 tables only. On median absolute deviation the minority is wider (3,938 against 2,827, p99.1 against the canonical ensemble), but against an ensemble drawn with the statute's ±25% proposal band it sits at p0.013, in the more-equal tail (report §5.4.9).

**Part 34 — Where the minority falls in the ensemble's 5–95 band.** On the canonical ensemble the minority is outside the band on three measures, all on the UCP side: mean-median p99.97, declination p98.79 and seats at 50/50 p99.99. Only the efficiency gap, at p94.54, is inside.
- `null_hypotheses.md` §2.5 (its table, "Three of four metrics fall inside", "isolated to seats-at-50/50"), §4 item 1, the §7.1 Chen-Rodden rows and the §7.2 list, and `retraction_conditions.md` §2.4 A and §7.2 ("3-of-4-in-band"), describe the traced v0_2 run. They are withdrawn. Seats at 50/50 counts UCP seats, so its upper tail favours the UCP, not the NDP. The minority's value is 0.5169, not 0.5057 (§2.4 B).
- `null_hypotheses.md` §1.2 B5 ("all four are in the extreme tails") and `osf_forest_recom_robustness.md` §3 ("the extreme tail of every pre-registered partisan-fairness metric") are read as: three of four; the efficiency gap, at p94.54, is inside. B5 therefore does not pass. None of the four metrics was registered before the commission maps were scored.

**Part 35 — Which ensemble the older references mean.** "The final 250,000-map ensemble" (`null_hypotheses.md`, note on timestamping) and "the canonical 250k ensemble" (`retraction_conditions.md` §2.6 B) mean the retired 250,000-plan ensemble of Amendment 4. The canonical ensemble has 1,010,000 plans (Part 1). `seed_robustness_rerun.md` Section B was computed on 2026-05-10, at the first canonical run's 250,000-plan state. Section C was checked against that run's 1,010,000 plans (completed 2026-05-12). That run was discarded on 2026-07-12 (Part 1), so Section C's "independently confirmed" refers to it, not to the rerun.

**Part 36 — The "no public support" tally.** The majority's "no public support" claim names five places: Airdrie, Cochrane, Chestermere, Red Deer and St. Albert (final report pp. 59, 62). It holds for three (Airdrie, Cochrane and St. Albert) and is partly wrong for two (Chestermere and Red Deer). `null_hypotheses.md` §1.4 ("4 of 7 have documented support (Canmore-Banff, Chestermere, RMH-Rocky Gas Co-Op plus one)") and `retraction_conditions.md` §5.1 ("four or more of the contested configurations") are read on that basis. Support for Rocky Mountain House–Banff Park and Olds–Three Hills–Didsbury answers a claim the majority did not make, and Canmore-Banff is a majority district.

**Part 37 — Blend-model figures in `thresholds.md`.** B.2.1, B.2.1.A, B.2.1.B, B.2.2, B.4.2, C.3 and Scenario E4 quote the retired blend model (Part 1): efficiency gaps of −0.40% and −1.81% (or −0.85% and −1.36%), mean-medians of −0.16 and −0.33 points, and its urban-weight grid. Part 19 flagged only rows #14 and #15. On the canonical figures the efficiency gap is +4.02% for the minority and +0.10% for the majority, and the mean-median +1.04 and −3.62 points. On those figures:
- Option A's "Observed minority EG (−1.81 %) is now below the 2-seat floor" fails: +4.02% is above the 2.25% floor.
- Option B's claim that "any fraction from one-tenth (2.5 %) to one-half" of the band gives the same result fails: +4.02% is above 2.5%. The minority is still under the 5% line.
- B.2.2's "both well within the flag" fails for the majority: −3.62 points is beyond the 3-point mean-median flag, on the NDP side.
- E4's "an order of magnitude below 7 %" fails: on 2015 votes both maps are over 7% (B.2.1.C's own table).

**Part 38 — Threshold counts and dates in `thresholds.md`.** Part A's provenance column gives STAT 7, LIT 5, FP 10, FP/AUD 4, MOD 6, MOD/LIT 1 and AUD 5, plus one each of FP/STAT, FP/OBS, LIT/FP and OBS. The counts line under Part A ("STAT: 6 · LIT: 6 · FP: 16 · MOD: 7") and Part F's "Six are directly statutory" are read that way. Rows #39–#42 were added in May 2026, not in August as the closing note says.

**Part 39 — Seats under s.13.** `terms_of_reference.md` §8 says "89 is a statutory input to the Commission (Act s.13, as amended by 2024 c17 s3)". 89 governed the 2025–26 commission; s.13 now reads 91 (2026 c7 s2).

#### M. This log

**Part 40 — This log's copies of Amendments 1 and 4.** Earlier versions of this log did not reproduce the filed text of either amendment. Both now appear above as filed.
- *Amendment 1.* The filed amendment (9wp5y, SHA-256 `2ba09d1b…`) has five changes. The log's copy listed six. Its Change 6, a "Derived Provisional Geometries" disclosure and a 48-hour sunset clause, is not in the filed file. The copy also shortened the filed text and renamed the committee.
- *Amendment 4.* The log's copy paraphrased the filed text (9wp5y, SHA-256 `b023a0d4…`). It gave the scale progression as "10k→100k→250k"; the filed text says the ensemble was first scaled from 250,000 to 1,000,000 and 2,000,000, then run at 10,000, 100,000 and 250,000. It wrote "~3,750" for "3,750", cut "crosses all 5 pre-registered structural irregularity tests" to "all", and added a note on the 1,010,000-plan ensemble that the filed text does not have.
- *The sunset clause.* The DPG disclosure and the sunset clause are in-repository commitments. `preregistration/retraction_conditions.md` §6.1 states the clause and calls its window "in-repo discipline, not externally pre-registered". No OSF document registers the clause or either window. Parts 1 and 2 cite it on that basis.
- The earlier copies are in the repository's history (commit `ca539bc4` and before).

#### What this amendment does not change

This amendment does not edit the November scoring specification. The file's SHA-256 is `2110548c…`, the value `seed_commitments.md` records after the specification's one later edit (Part 6); the 2026-06-12 pin, `e3546346…`, no longer matches it. The specification's references to Amendments 8, 9, 11 and 12 are translated by the table below. Unchanged: the 2 × 2 verdict surface, the partisan-lane rule (at least 2 of P1–P4), the thresholds for P1–P4 (P1 at +4.10%), and the 72-hour commitment.

Rules that changed, against what was filed or first committed:
- the sunset-clause window: 48 hours to two weeks (Part 2);
- the Alberta efficiency-gap line: about 5% (4.37%) to +4.10% (Part 3);
- the November drand round: round 6062459 withdrawn; a round at or after the map's publication, not yet pinned (Part 4);
- the structural lane: the 1.5-times rule replaced by the midpoint rule (Part 7);
- how X1 is scored (Part 13);
- the size-matched sets: W = 0.5 in place of 1.0, and set D primary (Part 14);
- the s.15(2) criteria: (b) by highway route from the Legislature, urban service areas counted as towns under (c), and Metis settlements counted with reserves under (d) (Part 15);
- when a result is final: an effective sample size of 400 in place of 20,000 plans (Part 16);
- three added tests (Part 17);
- the direction of condition 4.3 B (Part 22);
- how the scorecard's P1 and P6 cells are read, and the committee process's count (Part 25).

Registered findings withdrawn or read differently: the declination statements (Part 9), the packing thresholds' timing (Part 20), municipal anchoring (Part 31), the §5.3 signatures (Part 32), population spread A1 (Part 33) and the 5–95 band (Part 34).

The entries that made these changes all record that they were signed before the committee's map was due on November 2, 2026, and before any committee map had been published.

#### Where the earlier entries went

| Old | New part(s) | Not carried (reason) |
|---|---|---|
| 1 | Updated by Parts 1 and 5 | Filed; reproduced as filed. The unfiled Change 6 of earlier copies is not carried (Part 40) |
| 2 | C10 → 3; C11 → 2 | C1 (2M; reversed by 3 and 4), C2–C3 (supplementary analyses), C4–C5 (superseded by Amendment 4, then Part 1), C6–C9 (result revisions, not rules; superseded by the official-boundary recompute), Bucket C (superseded by Parts 6–13) |
| 3 | 5 | Bug record, interim claims and 2M postscript (superseded by Amendment 4, which is filed, and by Part 1) |
| 4 | Updated by Parts 1 and 4; C4 extended by Part 17 | Filed; reproduced as filed (Part 40) |
| 5–7 | 1 | Placeholder; number 5 is reused |
| 8 | 7 ("≥ 2 EDs") | The 1.5× rule and "canonical: 8" (superseded by Amendment 9) |
| 9 | 7 | — |
| 10 | 9 | — |
| 11 | 8 | — |
| 12 | 6 | The e3546346 pin (superseded by 2110548c; Part 6) |
| 13 | 27 | — |
| 14 | 11 | — |
| 15 | 1, 10 | "OSF qsgy8" / "OSF-anchored" labels (wrong) |
| 16 | 13 | — |
| 17 | 13, 14, 17 | The 20,000-plan rule (replaced by Part 16); the 2019-start statement (wrong; Part 1) |
| 18 | 12, 19, 21, 26 | — |
| 19 | 20 | — |
| 20 | 14, 15, 17 | W = 1.0 (replaced by 0.5); the reserves-only (d) (replaced) |
| 21 | 13, 14, 15, 16, 17 | Item 1(b)'s nearby-node rule (replaced by Amendment 23; Part 15) |
| 22 | 19 (and 1, seeding) | — |
| 23 | 15 | — |
| 24 | 14, 18 | — |
| 25 | — | Withdrawn unsigned; Amendment 21's reading stands (Part 15) |
| 27 | 22, 25, 28 | Item 2's 1992 "precedent" sentence (contrary to the ruling; Part 25 restates it) |
| 28 | 23, 24 | "p. 66" (it is p. 67) and the claim that "'Chair' is accurate" for all of S6 |

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-01 (Alberta time)

---

## Amendment 6 — Correction to Amendment 5, Part 5 (the AI tools)

> **Status: in force.** Written 2026-11-02 (Alberta time), after the author asked who did the hostile review, and signed the same day on the author's approval of its text, given in the CLI session ("Go"). It is filed as an update to registration 9wp5y. No test, threshold or finding changes.

**What was checked.** On 2026-11-02, read-only:
- the author's computer: the Codex extension's session logs (`~/.codex`), the Gemini CLI's chat logs and the Antigravity IDE's conversation index (`~/.gemini`), and the Downloads and Documents folders;
- the repository's full commit history.

Web use of ChatGPT, Codex cloud, Gemini and Kimi leaves no record on the computer and was not checked.

**Part 5's list of the other tools is replaced by the following.**
- **Gemini (Google)**, through the Gemini CLI and the Antigravity IDE, from 2026-04-23 to 2026-05-08:
  - an evaluation of the academic paper (Gemini CLI, 2026-04-23);
  - a red-team review of the audit, opened with "make sure the science is sound" (Antigravity, 2026-04-23);
  - a code audit (2026-04-26; `analysis/review/external_audit_gemini.md`);
  - code fixes written in response to a red-team review (commit `94700697`, 2026-04-26 23:40 MDT, which credits it as co-author).

  Antigravity can run other models, and the model used in each of its sessions is not recorded on the computer. Part 5's "in five passes" is withdrawn: no record supports the count.
- **Kimi AI (Moonshot AI)** audited the code on 2026-04-27. Its findings were fixed that morning, in commits `8933e648` ("fix adversarial AI audit findings", 09:41 MDT), `aa81bd20` ("resolve remaining Kimi AI audit findings", 09:58) and `d936a47a` ("resolve Kimi AI moderate findings", 10:30). No earlier disclosure named it.
- **Codex (OpenAI)** checked the literature review's citations on 2026-05-06 (`analysis/methodology/reference/citation_verification.md`). An attempt at 09:18 MDT on 2026-04-27 to have it audit the repository failed before it produced anything; the model was not available on the author's plan. No other Codex use is recorded on the computer, so Part 5's "helped with scripting and data processing" is withdrawn.
- **Who did the hostile review.** The author recalls Codex doing it. The computer holds no record of that. The records show adversarial reviews by Gemini (2026-04-23 to 04-26) and Kimi (2026-04-27). The author's web history, which was not checked, could settle it.

What Part 5 says about Claude is unchanged.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-02 (Alberta time)

---

## Amendment 7 — Scoring the November map in stages, on what is released

> **Status: in force.** Written 2026-11-02 and 2026-11-03 (Alberta time), after the committee reported, from the committee's report, the panel's report and the October 28 transcript, and before any reconstruction of the panel's map was made or any of its geometry was scored. Signed 2026-11-03 on the author's approval in session ("Do. It"). It is filed as an update to registration 9wp5y. No threshold changes.

**What happened.** The Select Special Committee reported on 2026-11-02. It adopted no map of its own: it acknowledged the Independent Advisory Panel's report and concluded its review, saying "the appropriate forum to offer any comments or observations on the Report is the Legislative Assembly" (committee report, p. 11). The map before the Assembly is the panel's 91-district map. The panel's report is published in two versions: a low-resolution PDF of 150-dpi page images, and a high-resolution PDF (`high443404_8-5x11_iapreport_digital-oct29.pdf`, 847,622,582 bytes, 308 pages, SHA-256 `d8ae78abcec3660f8158a327a25df7508b649ce5595788e8b265b362b2a75122`, served from the Assembly library at https://librarysearch.assembly.ab.ca/client/en_CA/search/asset/236105/1 and downloaded 2026-11-02 18:03 MST). The high-resolution version has a full text layer, and its district maps are vector drawings, not images. Elections Alberta has published no shapefile. Its Geomatics Team Lead wrote to the author on 2026-10-28: "The proposed ED boundaries are not set in bills yet. Once they are ready, the shp will be ready from our election website" (`evidence/correspondence/elections_alberta_gis_2026-10-28.md`).

**Part 1 — The map is scored in stages, and only on what is released.** The panel's report sets out what follows it (pp. 109–110). The Assembly may accept, reject or alter the proposals by resolution; the Government then introduces a bill, which goes through the normal legislative process and may be amended. The stages are:
1. the panel's report, tabled 2026-11-02;
2. the Assembly's resolution;
3. the bill as introduced;
4. each amendment to the bill;
5. the bill as passed (Royal Assent).

The audit grades only what is released to the public at each stage. A stage that releases nothing gets no grade, and the record says so, with the date checked. A stage is graded only on what it releases. A change between two stages is reported only when both versions are public. The stage record is `findings/map_stages.md`, with each source archived in `evidence/` with its SHA-256.

**Part 2 — Which map is scored.** The scoring specification scores "the committee's final map". The committee adopted none. Each stage's map is scored as that stage releases it. The headline is the map in the bill as passed.

**Part 3 — Numeric scores: official shapefiles, or a reconstruction only if it passes a calibration.** The partisan lane, the structural lane, X1 and the size-matched comparison are scored on official shapefiles, each within 72 hours of its release, and that scoring is the headline. Elections Alberta expects to publish them once the boundaries are set in a bill. Before then, the specification's §2 fallback (a reconstruction scored as provisional) is used only under the rules below, which replace §2's.
- *Why the rules.* Those tests need each voting area's district exactly. The registered validation of the April reconstructions (OSF w2s8k) measured, for the image-based reconstruction against the official shapefiles: mean overlap with the true district (IoU) 38% and 36%; 29% and 33% of voting areas in the wrong district; mean area error about 41% and 43%; mean boundary displacement about 19 and 23 km; and efficiency-gap error 0.55 and 3.89 points (majority and minority). The partisan thresholds sit within that error; P1's is +4.10%.
- *Source.* Any reconstruction uses only the high-resolution PDF named above, identified by its SHA-256: its vector boundary strokes, placed on the ground against features the maps label (roads, county lines, rivers). The 150-dpi version is not used. A vector source may do far better than the April images did; the calibration below decides whether it does.
- *Step A: districts the panel left unchanged.* A panel district whose name and stated population (Appendix 7) match a district of the commission majority's final map exactly is taken as unchanged, and the commission's official shapefile is used for it. The matches are listed before any reconstruction is done.
- *Step B: calibration.* Before any changed district is reconstructed, at least 10 unchanged districts are reconstructed from the panel's map images, by the same procedure that will be used for the changed ones, and compared with their official geometry. The sample is fixed before reconstruction begins: the unchanged districts drawn in the same map pages as changed districts, and, if fewer than 10, the rest drawn by a seeded random choice among the remaining unchanged districts, half urban and half rural. The calibration passes only if both registered w2s8k thresholds hold:
  - T1: at most 10% of the sample's voting areas are assigned to the wrong district;
  - T4: the province-wide efficiency gap computed with the sample's reconstructions in place of their official geometry differs from the all-official figure by less than 0.5 points.

  The w2s8k measures T2 (mean area error) and T3 (mean boundary displacement) are reported beside these.
- *Step C: if it passes.* The changed districts are reconstructed and combined with the unchanged districts' official geometry, and the map is scored. Each changed district's 2021 voting-area population is compared with its stated population, after scaling to the provincial total. A district more than 5% off is not used, and any measure that depends on it is not scored. The reading is labelled provisional, carries the calibration's measured error, and is excluded from the headline.
- *If it fails.* No numeric reading is published before official shapefiles. The calibration's result is published with the reason.
- *A limit, disclosed in advance.* Unchanged districts reconstructing well does not prove the changed ones do. Boundaries that run block by block through a city, as in Lethbridge's four-way split, are the hardest to place, even from vector drawings. The population check in Step C is the guard for them.

**Part 4 — What each stage gets without geometry.** Within 72 hours of a stage's release:
- the process lane (Lane 3 scorecard, OSF u47bq), graded from the published documents, with the page cited for each cell;
- the population table the stage itself publishes (district populations and deviations from the average), with any arithmetic check;
- counts read from the published maps and district names: which cities and towns are split, and into how many districts. These are labelled as counts read from the published maps, not geometric scores.

**Part 5 — Readings of the process-lane cells.**
- *P5.* Graded under its registered rule: "structurally foreclosed if P2–P4 remain No". Any boundary change the record credits to input outside a public process is reported beside the grade, not as part of it.
- *P6 and P7.* Amendment 5, Part 25 reads them against the committee, as the body whose vote settles the map. The committee adopted no map; the map becomes law only through the Assembly's resolution and bill. P6 and P7 are read against the Legislative Assembly, which the Speaker chairs. The cells' definitions are unchanged.

**Part 6 — Erratum in the scorecard (P8, commission column).** The registered text says the audit "found five of six failed independent check". The current count (academic report §5.9.6) is: two of six fail on population arithmetic, two hold in part, one was not tested on the minority's stated grounds, and one is withdrawn. The cell stays Yes; it scores publication, not accuracy.

**Part 7 — When the first stage's clock starts.** The panel's report was confidential until tabled (committee report, p. 11), and archived copies of the committee's page first link it on 2026-11-02. The 72-hour clock for stage 1 starts at 07:38 MST on 2026-11-02, when the committee's report was created, the earliest plausible tabling time, unless the Assembly's record gives an earlier one. The November drand round (Amendment 5, Part 4) is a round at or after that time, committed before any scoring run.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-03 (Alberta time)

## Amendment 8 — Two redraw tests on the November map (the swing-zone test and neighbour-drain), calibrated before the map is scored

> **Status: in force.** Written 2026-11-03 (Alberta time).
> - At the time of writing, the panel's map had been published as images only, no geometry of it had been scored on any partisan measure, and no official shapefile had been released.
> - The calibration below uses only neutral plans and the commission maps. It reads no November geometry.
> - Signed 2026-11-03 on the author's approval in session ("File"). It is filed as an update to registration 9wp5y.
> - No existing threshold changes.

**Why.** Wuff asked that the two adjacency-and-boundary tests be carried to the November map: the swing-zone allocation test (SZAT, OSF 6pt83) and neighbour-drain (OSF r3zm7; AsPredicted #289451). Both need changes before they can be used.
- **SZAT's registered null does not work on these maps.**
  - It flips each swing-zone voting area independently.
  - On the commission maps, 2,086 of the 2,110 swing-zone areas form one connected block. The block-permutation correction moved p from 0.0024 to about 0.19, and SZAT was retired as a confirmatory test (academic report §5.2.10).
  - The panel's changed districts are contiguous, so the same collapse is expected.
  - The November map also has 91 districts against the majority map's 89, so a difference in efficiency gap between them mixes the two added seats with the boundary choices.
- **Neighbour-drain is already scored on the November map, as S5 of the structural lane (Amendment 5, Part 7).** On 200 neutral 91-district maps, S5 fires 43.5% of the time (`findings/structural_lane_calibration_2026-10-31.md`). That makes S5 a weak screen on its own.

This amendment adds one null that fits both tests: neutral redraws of the territory the panel changed, with the districts it left alone held fixed.

**Part 1: The territory null.**
- *Fixed districts.* These are the 56 districts the panel left unchanged (Amendment 7, Step A; `findings/iap_unchanged_districts.md`), at the commission majority's official geometry.
  - Calgary-Acadia is also fixed. On the voting-area graph it is cut off from the rest of the changed territory, so it can only ever hold one district. The panel changed it by 2 people.
- *Redrawn territory.* Everything else: one connected region of 1,782 voting areas, which the panel divides into 34 districts. Voting areas are placed in districts by representative point.
- *Sampler.* This is the set D sampler (`close_seats_ensemble.py`, Amendment 17), unchanged: ReCom on the canonical voting-area graph, 2021 census population overlay. The statute is applied as written:
  - s.15(1): every district within ±25% of the provincial average (overlay total ÷ 91), not the territory's own average;
  - s.15(2): up to 50% below the average for a district meeting at least 3 of the 5 criteria, on the Amendment 23 criteria table (SHA-256 `48c928b8…2fafc`). At most 4 such districts province-wide. Two unchanged districts already use s.15(2) (Central Peace-Notley, Lesser Slave Lake), so at most 2 in the territory.
- *Code.* `analysis/scripts/territory_null.py` (SHA-256 `46fc7a16…ee02`) and `territory_score.py` (`0485e788…2b55`), branch `a8-territory-null`, commit `42b5fda8`.
  - The calibration plans were drawn at `401e15b5`. The generalised code at `42b5fda8` reproduces them byte for byte.
  - Outputs are in `data/outputs/a8_territory_null/`: `plans.npz` (`204d89a5…c3c7`), `scores.csv` (`3aac2c68…f2cd`) and `calibration.json` (`6eb1ab82…8ad2`).
- *Seeds.* drand round 6606642 (`preregistration/seed_commitments.md`). Chains 1–5 use salts `a8-territory-null-chain1` to `a8-territory-null-chain5`; the label-shuffle draws use salt `a8-drain-label-shuffle-` followed by the map's file name.
- *Runs.*
  - Reference chains 1–4 and holdout chain 5, 100,000 steps each.
  - One plan is kept every 250 steps, and the first 10,000 steps are discarded.
  - That leaves 1,440 reference plans and 360 holdout plans.

**Part 2: Test R1, the swing-zone test as a redraw test.**
- *Statistic.* The efficiency gap of the full 91-district November map: 2023 election-day two-party votes, voting areas by representative point (`territory_score.py`, the same substrate as the null).
- *Null.* The efficiency gaps of the reference plans: the 57 fixed districts plus 34 neutral districts in the territory.
- *p.* Two-sided rank, 2 × min(share of null ≤ observed, share ≥ observed).
- *Flag.* The test flags at p < 0.05, and the direction is reported.
- *Reported beside it, not gating.* Mean-median, declination and UCP seats, each ranked the same way.

This asks the swing-zone test's question directly: given the districts the panel kept, are its lines in the territory it redrew unusual among neutral lines drawn under the same statute?

**Part 3: Test R2, neighbour-drain as a redraw test.**
- *Statistic.* The registered neighbour-drain score: the sum, over coupled directed adjacent pairs, of max(0, s_X − 0.15) × max(0, 0.05 − m_Y).
  - It is computed on the same substrate, with adjacency taken from shared voting-area edges.
  - On the majority map this gives 0.0072418, and the original `drain_score` function gives the same number (S5's registered value is 0.0072127, from polygon adjacency).
- *Null, p and flag.* As in R1, against the reference plans' drain scores.
- *Reported beside it.* The registered label-shuffle p (10,000 permutations), with its false-positive rate on neutral plans from Part 4. S5 itself is unchanged.

**Part 4: Calibration, run before filing.**

| Check | Result |
|---|---|
| Split-R̂ across chains 1–4, efficiency gap | 1.009 |
| Split-R̂, drain | 1.004 |
| Null 95% interval, efficiency gap | −0.02% to +2.24% (mean +1.21%, UCP-favoured positive) |
| Null 95% interval, drain | 0.0022 to 0.0258 (mean 0.0083) |
| Holdout false-positive rate at p < 0.05, R1 | 4.4% (mean-median 5.3%, declination 4.7%) |
| Holdout false-positive rate at p < 0.05, R2 | 1.4% (conservative) |
| Label-shuffle null on neutral holdout plans, share with p < 0.05 | **97.5%** of 200 (2,000 permutations each) |
| Majority map on this substrate: EG, drain | majority (89 districts) EG +0.10%, drain 0.00724; minority EG +4.02%, drain 0.00059. These match the audit's canonical values. Neither map is in the null's population (89 districts, and nothing held fixed), so they are not ranked. |

On reading it:
- The rank tests are calibrated: false-positive rates are near or below 5%, and the chains agree (R̂ ≤ 1.011).
- The registered label-shuffle null flags nearly every neutral plan. It ignores geography, and real districting arranges similar neighbours next to each other. Its p is therefore reported only and never used as a gate.
  - This agrees with the audit's registered canonical run (`findings/drain_label_shuffle_null_canonical.md`, polygon adjacency): the majority, minority and 2019 maps all sit far below that null (p ≤ 0.0002).
  - This substrate (voting-area edges) reproduces that null on the majority map: mean 0.047 against the canonical 0.049. The vectorised null matches the original function within Monte Carlo error.
- **Sensitivity.** R1 flags a November map whose efficiency gap falls outside −0.02% to +2.24%, given the 57 fixed districts. R2 flags a drain score outside 0.0022 to 0.0258.

**Part 5: Which map, and when.**
- *Headline.* R1 and R2 are scored on the official shapefiles within 72 hours of their release, beside the structural and partisan lanes.
- *Before the shapefiles.* There is no provisional score. Amendment 7's Step B calibration was run on 2026-11-03 and failed (`findings/a7_stepb_calibration.md`), so no reconstruction of the panel's map is scored.
- *The null is always rerun on the enacted map's own fixed set before scoring*, with the code at `42b5fda8`, the same seeds and the same run lengths. This holds even if nothing changed, and the rerun is disclosed.
  - A commission-majority district is fixed when an enacted district holds exactly the same voting areas (by representative point), whatever its name.
  - A component of the remaining territory that the enacted map fills with one district is fixed too.
  - The territory's district count is the number of enacted districts in it.
  - The s.15(2) cap in the territory is 4 minus the fixed districts the enacted map's own population table puts more than 25% below its average.
  - If the remaining territory has more than one multi-district component, R1 and R2 are not scored. The code redraws exactly one, and adding more would be a new procedure.
- *Population base.*
  - The null applies the statute to the 2021 census overlay. The panel balanced its map on 2024 estimates.
  - An enacted district can therefore lie outside ±25% on the overlay. For example, the majority map's Canmore-Banff is −32% on the overlay, and its fixed Calgary-North East −38%.
  - Such a map is still scored, and every territory district outside the null's band on the overlay is listed beside the result.

**Part 6: What this changes and what it does not.**
- SZAT as registered (6pt83, swing-zone permutation null) stays retired. R1 is a new test, scored beside the specification and not part of its verdict.
- S5 and the structural lane are unchanged. R2 is reported beside them.
- Neither test gives a verdict on whether the map is a gerrymander. Each locates the panel's choices within neutral choices under the same statute and the same fixed districts.
- The two tests are reported separately, each at its own 0.05. Where both flag, that is stated; they are not combined.

**Part 7: Erratum (Amendment 7, Part 3).** Amendment 7 calls the efficiency-gap gate "T4". In the w2s8k plan (`dpg2_experiment_plan.md`, §T-C) that gate is "T1 EG delta" (< 0.5 points), and w2s8k's T4 is population MAD. The quantities and thresholds Amendment 7 states are what Step B computes. Only the label is wrong.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-03 (Alberta time)

## Amendment 9 — A second calibration attempt, with a procedure that reads rural pages

> **Status: in force.** Written 2026-11-03 (Alberta time). At the time of writing:
> - Amendment 7's calibration had been run once and had failed (`findings/a7_stepb_calibration.md`, commit `d1f7a06a`).
> - No reconstruction of a changed district had been scored, and no geometry of the panel's map had been scored on any measure.
> - No official shapefile had been released.
>
> The author directed the second attempt in session ("Prep, file osf, run"; then "A" and "File when ready and continue") on learning that the shapefiles may be months away. Signed 2026-11-03. It is filed as an update to registration 9wp5y. No threshold changes.

**Why.**
- The first procedure placed every city page it could read almost exactly (18 pages: IoU 0.996 to 1.000; 7 of 981 VAs misassigned). It could not read rural pages, and it failed both gates: 49.0% of VAs misassigned against a 10% limit, and an EG delta of −2.16 points against 0.5.
- A second procedure, version 2, was built and tested in development but never run on the sample. It placed the city pages, but only 1 of the 10 changed pages over 10,000 km² (`findings/a9_stepb_v2_development.md`). That draft was not filed.
- Development then found why rural pages fail, and version 3 fixes it.
- The shapefiles are expected only after the bill passes. Amendment 7's calibration is the only route to any numeric reading before then.

**Part 1: The first result stands.** Amendment 7's calibration failed, and that result stays on the record. This amendment registers one further attempt, under the same gates, on the same sample, before it is run. If it fails, there is no third attempt under this amendment.

**Part 2: What is known before the second run.** The second attempt is not blind. These are the limits on what was seen:
- *Seen.* Which sample pages the first procedure could not place, and why. The first run's per-district scores (`findings/a7_stepb_calibration.json`).
- *Not seen.* No sample page was opened while versions 2 and 3 were built. Every development run refused sample districts in code.
- *Development data.* The 22 tuning districts, with their official geometry. The pages of the 35 changed districts, which have no official geometry and so cannot leak it.
  - The changed pages also draw neighbouring districts' lines, and some of those neighbours are sample districts.
  - Those lines were matched only against roads and census-subdivision boundaries, never against official district geometry.
  - No sample district was reconstructed.
- *No rural page has truth.* Every tuning district is urban or small: no tuning page is drawn at more than 29 m per point. Version 3's rural evidence is fit quality only, meaning how closely each page's own lines fall on the reference datasets once placed. The sample run is the first test of rural pages against official geometry.
- *Every unchanged district is already used.* The 56 are the 22 tuning districts and the 34-district sample. No fresh sample exists, so the second attempt reuses the fixed one.

**Part 3: The version 3 procedure.**
- *Code.* `analysis/scripts/a9_stepb_reconstruct_v3.py`, SHA-256 `0b9d07c14ec85fc59669a1b5bb81a24c65379f17bbfcc3b1aa5258be9feace62`, commit `6305cb0a`.
  - It uses version 2 (`a9_stepb_reconstruct_v2.py`, SHA-256 `c148a5289d843aefb709feae42d75554a4f0e19b6e47d9d87a28467949b4f4f9`) for the outline, the reference layers, the road search and the refinement.
  - Version 2 uses version 1's helpers. Its docstring lists every change.
- *What development found.*
  - Rural pages draw their lines in other styles. The dark-grey 0.92-pt strokes are the full road network, and the light-grey 0.37-pt strokes are the township survey grid. Rules set on city pages matched each against the wrong reference.
  - Prairie roads lie on a one-mile grid, so a road search alone finds near-equal placements a whole number of miles apart.
- *What changed from version 2, and only this:*
  1. *A prior from the page's municipalities.* Village dots, town areas and First Nations reserve areas are matched by name to the 2021 census subdivisions. They are fitted to the subdivisions' centroids: two-point RANSAC, then least squares. The RANSAC's generator seed (0) is a fixed algorithm constant, not a sampling seed. On every development page, another seed gives the same inliers and fit (`findings/a9_stepb_v3_dev/ransac_seed_check.txt`). The prior is used when its rotation is within 1° of a right angle and it has either
     - at least 4 inliers, with a scale within 10% of the stated-area scale; or
     - exactly 3 inliers, with a scale within 1.5% and a median residual under max(150 m, 1 point). Three points fix rotation poorly, so a 3-inlier prior's rotation is snapped to the right angle, and its scale and translation are refitted.

     Otherwise version 2's road search, unchanged, supplies the prior.
  2. *Layer identification on each page.* Each grey stroke style is assigned to the reference it matches best within the prior's error: roads (National Road Network plus OpenStreetMap highways) or census-subdivision boundaries. A style matching neither in at least half its points is not used.
  3. *Local refinement.* The search is restricted to the prior's error (municipal prior: max(500 m, 2 × the median residual); version 2 prior: 1,500 m), followed by version 2's robust ICP.
  4. *An acceptance rule, applied before any polygon is returned.* A page counts as a failure unless it has:
     - at least 2,000 matched page points;
     - a median distance of at most 40 m from their references;
     - at least 60% of them within 60 m.

     The area check alone cannot do this: the scale is fixed from the stated area, so a wrong placement still passes it. The point floor was added in development after Fort McMurray-Wood Buffalo matched only its 363 provincial-border points (99% within 60 m) in a wrong place, where its roads agreed at 4%.
- *References.*
  - Statistics Canada National Road Network, Alberta, edition 17.0: `data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg`, SHA-256 `bb6d1396a62b9cbb0ce5c3b05c88ad9d432753847f392728dc933b6e8b5988f4`. It is built by `analysis/scripts/build_nrn_extract.py` from `nrn_rrn_ab_GPKG.zip` (SHA-256 `0dfd3afc922f12b870a231bddd359d3430a5b66e04e283131c614f0b38aacf9a`), and contains information licensed under the Open Government Licence – Canada.
  - Statistics Canada 2021 census subdivisions: `data/shapefiles/reference/alberta_2021_csds.gpkg`, SHA-256 `7ee3356b6e5c828db1e016cd96f101bfd0cbc67d8b3f87e429f2316430a4d840`.
  - The OpenStreetMap highways used before: `data/osm/alberta_osm_highways.gpkg`, SHA-256 `d8100044b0f38935bd7ccd539e3f21fb7118bea018d9cfb5827acbad324eacc9`.
  - The panel's report: the high-resolution PDF named in Amendment 7 (SHA-256 `d8ae78ab…a75122`).
- *Environment, pinned.* Python 3.12.13 with PyMuPDF 2.1 (MuPDF 1.28.6). The full package list is in `findings/a9_stepb_v3_dev/environment.txt`. Results depend on the PDF library: PyMuPDF 1.27.2.2 reads the outline stroke without a width on 9 of the 57 development pages. The scorer refuses to run under any other Python or PyMuPDF version.
- *Development results* (`findings/a9_stepb_v3_development.md`):
  - *Tuning districts (official geometry).* All 22 are accepted, at IoU 0.9975 to 0.9996 with boundary error (Hausdorff) of 1 to 6 m.
  - *Changed districts (no geometry, fit quality only).* 34 of 35 are accepted:
    - all 16 under 1,000 km²;
    - all 9 of 1,000 to 10,000 km²;
    - 9 of the 10 over 10,000 km².

    Accepted pages have 9,363 to 53,806 matched points, lying a median of 5.4 to 29.6 m from their references, with 72% to 96% within 60 m.
  - *The one failure* is Fort McMurray-Wood Buffalo, whose page names only six First Nations reserves. Its fit matches only the provincial border, and the acceptance rule rejects it.
  - *VAs near a boundary.* On 24 placed changed pages, 10 of 1,309 VA points (0.8%) lie within 30 m of the reconstructed boundary.
  - *The known risk.* Northern pages with few municipalities are the weak case. The sample's Peace River, Lesser Slave Lake and Central Peace-Notley hold 8.6% of its VAs, and their pages were not opened.

**Part 4: The second run.**
- *Scorer.* `analysis/scripts/a9_stepb_calibrate.py`, SHA-256 `3c470b99a51d162eba44a45d4d5db357ca77fa798289681a268dbc43da285fda`. It substitutes version 3 into the frozen Amendment 7 scorer `a7_stepb_calibrate.py`, which is unchanged, and records version 3's fit diagnostics for each district.
- *Gates.* T1 (VA misassignment at most 10%) and T4 (province-wide EG delta under 0.5 points), as in Amendment 7. T2, T3 and IoU are reported beside them.
- *Rules.* Those of `findings/a7_stepb_calibration_protocol.md`, unchanged. A page the procedure cannot place, or that fails the acceptance rule, counts against both gates.
- *Running it.*
  - It is run once, after this amendment is filed, in the pinned environment, as a detached process that logs each district as it finishes.
  - The result is committed, pass or fail, before any changed district is scored.
  - A run stopped by the computer before it writes its result file is not a result. It is restarted from the beginning, unchanged, and the stop is disclosed with the result.

**Part 5: If it passes.** Amendment 7, Part 3, Step C applies unchanged.
- The changed districts are reconstructed with version 3 and combined with the unchanged districts' official geometry.
- Each changed district must pass the 5% population check.
- A page that version 3 cannot place, or that fails the acceptance rule, is not used, and any measure that depends on it is not scored.
- R1 and R2 (Amendment 8) depend on every district. They are scored provisionally only if every changed district is used. Amendment 8, Part 5's rerun rule then applies, with the reconstruction in place of the enacted map. Fort McMurray-Wood Buffalo fails in development, so R1 and R2 are expected not to be scored provisionally.
- The reading is labelled provisional, carries this calibration's measured error, and is kept out of the headline.
- *Voting areas cut.* With the provisional map, and again on the official shapefiles, the audit lists the Elections Alberta voting areas (2023 and 2026 sets) that the map's boundaries cut.
  - The list uses `analysis/scripts/va_bisection.py`. A VA is cut when more than 1% of its area, and more than 0.01 km², lies outside its main district. This rule finds no cuts on the 2019 map.
  - The list is descriptive, not a test. Baselines: the commission majority map cuts 229 of the 4,904 2026 voting areas, and the minority map 364.
  - For the provisional map, a cut within this calibration's measured boundary error is marked as uncertain.

**Part 6: If it fails.** No numeric reading is published before the official shapefiles. The result is published with the reason.

**Part 7: What this does not change.** The headline remains the official shapefiles. No threshold changes.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-03 (Alberta time)

## Amendment 10 — A third attempt: the panel's map assembled like a puzzle and checked against every page, registered as a reproducibility run

> **Status: in force.** Written 2026-11-03 and 2026-11-04 (Alberta time). At the time of writing:
> - Amendment 7's calibration had failed (`findings/a7_stepb_calibration.md`), and so had Amendment 9's (`findings/a9_stepb_calibration.md`, commit `2da38dc0`).
> - No partisan or structural measure of the panel's map had been computed.
> - No enacted geometry existed. The only published district geometry is the commission's proposed map, which Elections Alberta released as a shapefile. The author reported that Elections Alberta could not release the panel's boundaries before the bill.
>
> The limit of one further attempt in Amendment 9, Part 1, was set by the session agent when drafting that amendment. It was not set by the author and is not required by the method. The author directed this attempt in session: "the limit of two is artificial and something you created arbitrarily. There's no reason this can't be done." The author approved filing in session ("Strip then file"; then "Do your recommendations ... Go"). Signed 2026-11-04. It is filed as an update to registration 9wp5y.

**Why.**
- The second calibration placed 30 of the 34 sample pages at IoU 0.998 to 1.000. Ten of them were rural districts, the first rural pages ever checked against published geometry. It failed on one wrong acceptance: Sherwood Park, placed rotated 90° and 13.5 km off, over three Edmonton districts. That one placement cost 88 of the 264 misassigned voting areas.
- Districts fit together like puzzle pieces, and every page carries more than its own outline: its neighbours' boundaries, their numbers, and a locator map of the whole province. A correct piece must fit its neighbours, lie inside its own page and match its place on the locator map. The wrong Sherwood Park placement fails all three.
- For the panel's map, most pieces are known under one stated assumption: the 56 districts the panel reports unchanged from the commission's map, by name and stated population (Amendment 7, Step A), are taken at the commission's published geometry. Every voting area in the remaining territory then belongs to one of the 35 changed districts.

**Part 1: Amendment 9, Part 1, is superseded.** The sentence "If it fails, there is no third attempt under this amendment" is withdrawn. Both failed calibrations stay on the record. Any attempt after this one also needs its own amendment, filed before its run, stating what has been seen.

**Part 2: What has been seen, and what this run can and cannot show.** This attempt is not blind.
- *The sample is development data.* Every sample page has been reconstructed and compared with the commission's geometry. The rules in Part 3 were built on those results, and several were changed because of what they did to the sample's score:
  1. the conflict-count tie-break in rule 2, after a misplaced Edmonton-Meadows knocked out three correct sample districts (Edmonton-Glenora-Riverview, McClung and West Henday);
  2. the 25% area tolerance for hole claims, chosen over 15% partly because the sample scored 6.65% against 8.43%;
  3. scoping city labels to pages outside that city, and matching mutual claims by area, after Sherwood Park's and Windermere's holes were exchanged;
  4. pooling a district's title claims, after Chestermere-Strathmore's hole came in two parts;
  5. assigning voting areas by representative point, the audit's standing convention, which removed the last three wrongly assigned voting areas.

  The record of every iteration, with the sample score at each, is `findings/a10_stepb_development.md`.
- *The expected result is stated in advance.* The pipeline is deterministic. On the development fixture, which rebuilds every page from the second run's saved transforms, it assigns all 1,909 sample voting areas correctly (T1 0.0%) with an efficiency-gap delta of 0.00 points (T4), and passes every sanity item. The registered run reproduces that from the PDF with the frozen code. It is a reproducibility check of the frozen pipeline, not out-of-sample evidence about its accuracy.
- *Evidence that could not be tuned.* The changed districts have no published geometry, so nothing in development could fit them to truth. Their evidence is internal consistency between independent sources on the PDF:
  - each page draws its neighbours' boundaries, and those lines sit a median 3 m (90th percentile 6 m) from the neighbours' own placed outlines and the known boundaries, with 98% of their length within 30 m;
  - on the real map's known set, every assembled district sits within 0.94 km (median 0.3 km) of its shape on the page's locator map, which is fitted to the commission's outline, not to any reconstruction;
  - drawn back onto its own page, no placed district extends outside the page's map frame;
  - drift between adjacent pieces after snapping is 0.003% of the territory on the real map's known set, and 0.005% on the calibration set;
  - each changed line is drawn on both districts' pages. On the real map, across 131 changed district pairs (103 drawn on both pages), the drawings sit a median 5.4 m from the final line (95th percentile 24 m), and 3.7% of the length is more than 30 m off. Where two drawings differ by more than 30 m, three voting areas have more than 1% of their area between them, holding 1,952 people, and none would change district if the line followed the other drawing (`findings/a10_dev/line_consensus.py`, SHA-256 `0f7e5447bc247fc23e79b2b9229038ea9988a5f23ed5a395a2203c51665fb7b5`). On the calibration set, accepted pages' drawings sit a median 7 m from the true line; rejected pages' grey lines sit 162 m off, and lose to the accepted page in 98% of disagreements;
  - the report's written boundary descriptions were measured against the assembled lines for eight changed districts (`findings/a10_dev/description_check.py`, SHA-256 `9710569cbcd76323cf9dcc515ee0cd57f5fabdf5e6a262c45aea374391d5f935`). Lethbridge and Morinville-Sturgeon match to a median 10 m and 8.5 m. Each larger miss was drawn back onto its page (`findings/a10_dev/description_overlay.py`, SHA-256 `8cb9a526235cd83b073b0e61dbe1d7fab1d20ecfdf4ac42be1ef36ce9ce1f6e1`): on Edmonton-Strathcona, Edmonton-Whitemud, Fort McMurray-Lac La Biche and Rocky Mountain House-Sundre the final boundary follows the page's own red outline to a median 1 to 8 m, and the miss is the check matching an unnamed river or a highway the page does not follow, or the text being loose ("roughly", "just east of the Highway 22 corridor", where the page draws the boundary about 11 km east). Edmonton-Windermere and Edmonton-Meadows are hole fills on the real map: their page fits were rejected for overlapping known districts, and sit 21 km and 17 km from the fills, so the fitted outlines cannot test them. Three other checks can. Each page's own drawn shape, fitted onto the fill by a quarter-turn, a scale and a shift, overlaps it at IoU 0.971 and 0.983, with boundaries a median 19 m and 10 m apart (`findings/a10_dev/fill_shape_check.py`, SHA-256 `2835b67f3ec77940ba5d7ab174c59cf221c1db583055bd445d4cb79e553b3063`); Version 4's independent placements agree (IoU 0.967 and 0.991); and both fills sit within 0.94 km of their locator shapes. The same shape check gives Fort McMurray-Wood Buffalo 1.000, and Calgary-North West-Bearspaw 0.996: it gave 0.776 before the districts-file fix below, which this check prompted. These checks led to changes in how the districts file is drawn, not in any voting area's assignment. Twelve passages name streets, creeks, rail or watersheds that the map data does not carry and were not checked;
  - 153 voting areas on the real map are cut by a changed line, holding 3.8% of the province's population; 26 are split closer than 60/40 (`findings/a10_dev/cut_va_sensitivity.py`, SHA-256 `c264a49e3a408e6710b8d4bb36fe8196b6ffc60ac30ce0c3155bcf5a652fa0dc`). On the calibration set, flipping every cut voting area with at least a tenth of its area on the other side, in whichever direction moves the efficiency gap, gives a range of −0.10 to +0.06 points, with T1 at most 0.52%. These bounds are built greedily from single flips and do not model interactions. No such range has been computed on the real map;
  - fifteen voting areas on the real map have their representative point within 100 m of a changed line (`findings/a10_dev/near_line_vas.py`, SHA-256 `049a3505d828783e1e77ce34c795bc59b9335c278cf62f82c5cc1f8214200965`). For ten, every page drawing of the line agrees with the assignment, with the point at least three drawing-grid steps from the finest-scale drawing (the map's coordinates are stored on a 0.092-point grid, 0.8 m to 75 m on the ground by page). Three agree but sit closer than that. Two, holding 1,312 people, have their points in the gap between the two pages' drawings, 3 m and 10 m outside the assigned district's own page outline; the PDF cannot decide them, and they are assigned by the area-share rule.
- *What else was used.* The locator-map fit (`a10_inset.py`) aligns each inset to the outline of the whole province, or of the Calgary or Edmonton districts, in the commission's map. Those outlines include the outer edges of some sample districts. They are used only for the locator-map sanity item, never for placing a page or assigning a voting area.
- *The real map already exists in development.* The panel's map has been assembled from development data with the 56 unchanged districts known (`snap_fixed`), and it passes the sanity check. No partisan or structural measure has been computed on it.
- *A tested change not adopted.* A version 4 that seeds pages from the locator map before the road search was tested on the four misplaced pages. It placed Sherwood Park correctly (IoU 0.999), placed Edmonton-Meadows and Edmonton-Windermere within 0.9 km of their locator shapes, and still could not place Calgary-North West-Bearspaw. It is not used here, because adopting it would invalidate the development run; it is recorded in the development record.
- *Fixes after the checks.* Drawing the final districts back onto their pages found faults in how the districts file draws cut voting areas, not in which district gets any voting area. The file carried zero-area lines and points left by the split, in 15 real-map districts. And the part of a voting area outside its district's snapped piece stayed with that district: 1,299 detached fragments (0.14 km², among them a chain along the B.C. border south of Rocky Mountain House-Sundre's page), a 5.8 km² strip that Cochrane's own page places in Calgary-North West-Bearspaw, and 17 placed districts departing from their page outlines by more than 0.1 km² somewhere. `a10_snap_assign.py` now writes polygons only; draws the part of a voting area that lies inside another district's piece with that district; and gives each part that lies in no piece to the other district it shares the longest edge with, among the voting area's own parts and the districts with no piece, keeping it only if it touches no other district. Calgary-North West-Bearspaw's drawn area went from 31.4 to 37.4 km² (stated 37), and Cochrane's from 569.6 to 563.5 km² (stated 564). Four voting areas between Edmonton-South and Edmonton-Windermere are now flagged cut. No voting area changed district, and drift is unchanged on both maps. The fix drew the commission's own Calgary-Buffalo, a tuning district, at its true 4.20 km², which failed the 5% area item against App. 7's stated 4 km²: App. 7 rounds to whole km². The area item now also allows that rounding (0.5 km²); no other district is affected. 270 detached fragments remain (0.04 km², the longest 0.8 km). Two placed districts still depart from their page outlines by more than 0.1 km²: Banff-Canmore-Diamond Valley and Macleod-Crowsnest, by 8.9 and 9.0 km², where whole voting areas run past the drawn line.
- *Final assignment against each page.* For every district placed from its own page, the voting areas whose representative point lies inside the page's outline were compared with the final assignment (`findings/a10_dev/final_vs_page.py`, SHA-256 `4b5393e3d7a3ff7e0f29c8632ff2cad7743abc5854766cc291d70abb724523ff`). On the real map, none of the 30 placed districts loses a voting area its page contains. Two gain one each: cut voting areas whose representative points lie 3 m and 10 m outside the page outline, holding 1,312 people.
- *An open item.* The grey neighbour lines drawn on the known districts' pages of the real map run more than 100 m from the final line for 6.8% of their length, against 1.2% for those on the placed pages. The likely cause is neighbour lines missing on some of those pages, so the check measures against the wrong line, but this is not confirmed. It does not touch any changed line.

**Part 3: The assembly.** Version 3 (`analysis/scripts/a9_stepb_reconstruct_v3.py`, SHA-256 `0b9d07c1…feace62`) is unchanged. `analysis/scripts/a10_assemble.py` (SHA-256 `3a75ee3d943dd34ae0fa5f6cc36963ed9dc2599d4cf492bec99664cadbd3d9da`) is applied to every page result before any district is scored:
1. *Known-overlap rule.* A reconstruction overlapping the known districts by more than 5% of its own area is rejected. In the second run, correct placements reached 0.074% and the wrong one 82.8%.
2. *Mutual-overlap rule.* Where two reconstructions overlap by more than 10% of the smaller one's area, one is rejected: the one in conflict with more other reconstructions; if equal, the one overlapping the known districts more; if equal, the one with fewer of its matched points within 60 m. Conflicts are recounted after each rejection.
3. *Provisional assignment.* Each voting area goes to the district, known or reconstructed, holding the largest share of its area. One less than half covered is left for the hole fill.
4. *Hole fill.* Unassigned voting areas are grouped into connected components on the voting-area graph. A district that was not placed, or was rejected, claims a component when all of these hold:
   - the component's area is within 25% of the district's stated area (App. 7);
   - either its page's red title names a census subdivision whose centroid lies in the component (hyphens read as spaces, so "Grande Prairie-Wapiti" names Grande Prairie), or, when no title town lies in any component, the component's representative point lies inside the envelope of every census subdivision named on its page or in its title, buffered by the larger of 6 km and half the square root of its stated area;
   - more than half of the districts touching the component are among the neighbour numbers printed on its page. A city's name on a page counts for all that city's districts, but only on a page whose own district is not in that city. A page with no neighbour record cannot claim.

   A component is filled when it has one claimant that claims nothing else. A district whose title names towns in several components claims them together, with the area test on their union. Where several districts and components claim each other, the unique one-to-one pairing that best matches their areas is taken. A fragment whose every neighbouring voting area belongs to one district goes to that district. Anything else stays unassigned, with its claimants recorded.
5. *Population: reported, not gated.* Amendment 7, Step C, set aside a district whose 2021 voting-area population, scaled to the provincial total, differed from its stated population by more than 5%. That gate is withdrawn. On the 57 districts whose geometry is known, the difference runs from −39.3% to +12.7%, and 34 of 57 exceed 5% (`findings/a10_dev/population_check_noise.csv`). The panel's figures are current estimates and the 2021 census predates recent growth (Calgary-North East −39%). The difference is reported for every reconstructed or filled district. On the real map the largest gaps are in south Edmonton's growth areas: Edmonton-Windermere −29.7% and Edmonton-Meadows −20.8%, both filled, and Edmonton-South −19.0%, placed from its own page.

**Part 3b: Snapping, final assignment and the sanity check.** `analysis/scripts/a10_snap_assign.py` (SHA-256 `ab11d3dc292c875d434f44a8e7352422e6019ab51eb21d19a64094daed4b84a9`):
1. *Sources.* Each district appears on its own page and, as a neighbour, on each adjacent page. `analysis/scripts/a10_neighbours.py` (SHA-256 `be38125f4929c585c6838539102f425bc99306ddd04411fabde1da8a6f015ff0`) extracts the neighbour boundaries (grey 1.84-pt strokes) and the printed neighbour numbers and city names. `analysis/scripts/a10_inset.py` (SHA-256 `0b87758adeb1bdf8fe471e30381a8e5f81b5a94aa50675429ee50bebeef446ed`) carries each page's locator map to ground. The report's written boundary descriptions (`findings/a10_dev/boundary_descriptions.md`) were inventoried and used to check lines by hand, as with Drumheller-Stettler's west side, which the panel moved east of Stettler. The code does not read them.
2. *Edges snap together.* A reconstruction vertex within 40 m of a known boundary, a voting-area boundary, or another outline or neighbour line moves onto it, in that order of preference.
3. *Drift* is the area of overlaps plus gaps between adjacent pieces, as a share of the territory. The target is under 0.05%.
4. *Final assignment, as Elections Alberta would assign.* Each voting area goes to the piece containing its representative point. One whose point lies in no piece goes to the piece holding the larger share of its area. A voting area cut by a line is flagged, and its population is apportioned by area in the population report. In the districts file it is drawn split along the snapped pieces; a part of it inside another district's piece is drawn with that district, and a part in no piece with the other district it shares the longest edge with (a district with no piece counts), or with its own district if it touches no other. A hole two unplaced districts share is split by the better of their pages' rejected fits, the one with more matched points within 60 m, and both districts are flagged lower confidence. A rejected fit is used for this split only.
5. *Sanity check.* Every item must pass, and an item that cannot be run fails:
   - 91 districts, every voting area assigned once, and the province covered;
   - each district connected, allowing parts its own page draws;
   - no district overlapping a known district by more than 0.1% of its area;
   - each placed district's snapped area within 5% of its stated area, or within App. 7's rounding to whole km² if that is larger (filled or split districts are reported, not gated: a hole of whole voting areas runs smaller than the drawn district);
   - for each district, more than half of its neighbours sharing more than 200 m of edge are printed on its page;
   - every placed district, drawn back onto its own page, inside the page's map frame;
   - every district within 3 km of its shape on the page's locator map (or half the shape's width for districts under 5 km across), with overlap at least 0.45 for larger ones. Barrhead-Westlock-Athabasca's locator map highlights Drayton Valley-Devon, a source error that is reported and not counted.

**Part 4: The third run.**
- *Command.* `analysis/scripts/a10_run.py` (SHA-256 `eaed0fa6849c53717287d9a88fe9b6e00c412277902affa431795eeebbc7f0a4`) runs, in order:
  1. the pages (`a10_reconstruct_pages.py`, SHA-256 `e55997ad6b96742444f04277f5e5530d6de61962f9d310ebad3e4a74577e9caa`) for the 69 pages that are not known districts;
  2. the neighbour extraction;
  3. the locator-map fit;
  4. the scorer (`analysis/scripts/a10_stepb_calibrate.py`, SHA-256 `05461b50947a142db3b7bca549f7db0b3c7a8023f55ffc8e504108eb15d362c5`).

  The pages may be run in two detached processes over halves of the list first. `a10_run.py --skip-pages` then runs steps 2 to 4 over them. Every page is deterministic, and a stopped page run resumes from the pages already saved; the stop is disclosed.
- *Gates.* As in Amendment 7, on the final assignment with the 22 tuning districts as the known set:
  - T1: at most 10% of the sample's voting areas in the wrong district, with unassigned counted as wrong;
  - T4: province-wide efficiency-gap delta under 0.5 points.

  Every sanity item must also pass. The assembly-only figures, T2, T3 and IoU are reported beside them.
- *Changed pages.* They are reconstructed in the same run because the hole fill needs every other piece in place. No measure of any changed district is computed until the result is committed, pass or fail.
- *Environment.* Python 3.12.13 with PyMuPDF 2.1. The scorer refuses any other.
- *Development check* (`findings/a10_stepb_development.md`): a dry run of the full sequence (`a10_run.py --skip-pages`) from a clean directory, seeded with the development page outputs, gave T1 0 of 1,909, T4 0.00 points, drift 0.005%, and every sanity item passing, with a voting-area assignment identical to the development run (`findings/a10_dev/dryrun_calibration.json`). After the fixes to the districts file, the full sequence was run again from a clean directory seeded with the same page outputs: the same figures, with both maps' voting-area assignments identical to the development run. All scripts are at commit `84383097`.

**Part 5: If it passes.** Amendment 7, Part 3, Step C applies, with the assembly in place of raw polygons:
- The known set becomes the 56 unchanged districts plus Calgary-Acadia, at the commission's published geometry. The 35 changed pages from the same run are assembled under Parts 3 and 3b, and the sanity check must pass on that map too.
- A district that is not placed or filled is not used, and any measure that depends on it is not scored.
- R1 and R2 (Amendment 8) are scored provisionally only if every changed district is used. Amendment 8, Part 5's rerun rule applies, with the assembled map in place of the enacted map.
- The cut voting-area range is reported beside the reading: `findings/a10_dev/cut_va_sensitivity.py` (SHA-256 above), step 2 run on the assembled map with `A10_STEPC=1`, giving the efficiency gap with every cut voting area of at least 10% minority share flipped each way. It is a sensitivity figure, not a gate, and its bounds are greedy.
- The reading is labelled provisional, states that its calibration was a reproducibility run on seen data (Part 2), and is kept out of the headline. The voting-area cut list (Amendment 9, Part 5) is made on the assembled map and marked as such.

**Part 6: If it fails.** No numeric reading of the panel's map is published before the enacted map's shapefiles. The result is published with the reason.

**Part 7: What this changes and what it does not.**
- Amendment 7's 5% population gate is withdrawn (Part 3, rule 5).
- Amendment 9's one-attempt limit is withdrawn (Part 1).
- The T1 and T4 thresholds are unchanged.
- The headline remains the shapefiles of the map as enacted, which Elections Alberta publishes once the boundaries are set in a bill.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-04 (Alberta time)

## Amendment 11 — Fixes found by the provisional Step C run, before the official map is scored

> **Status: in force.** Written 2026-11-04 (Alberta time), after the provisional Step C run on the panel's assembled map (`findings/a10_stepc/README.md`, commits `8fcf4318` and `083c0d1f`). Every Step C result has been seen. Nothing here changes a test, a threshold, a statistic or a reading of a result. It changes two pieces of code that failed when the panel's map was scored, and it writes down one procedure that was applied by precedent during the run. All three would recur on the official map.

**Why.** Step C ran each registered step by hand. Three registered pieces did not do what the amendments say they do on a scored map:

- the cut-voting-area sensitivity (Amendment 10, Part 5) scored the commission majority's map, not the map given;
- the redraw-test scorer (Amendment 8) cannot score a rerun's plans from its command line;
- one redraw-test chain did not seed, and no amendment says what to do.

Step C worked around each and disclosed it (`preregistration/a10_stepc_run_sheet_2026-11-04.md`, "Changes to this sheet"). This amendment makes the workarounds the registered procedure, so the official map's run needs no decision at run time.

**Part 1: the cut-voting-area sensitivity on a scored map.** `findings/a10_dev/cut_va_sensitivity.py` (SHA-256 `c264a49e…a0dc`) builds, in its step 2, the calibration composite (the majority map with only the sample districts replaced) for every map. On `--map fixed` it therefore never scored the changed districts; its Step C output gave the majority's efficiency gap (+0.098%) instead of the panel's (+1.45%). That output is kept as `findings/a10_stepc/cut_va_sensitivity_fixed_REGISTERED_CODE_DEFECT.json`. For any scored map, the registered script is `findings/a10_stepc/cut_va_sensitivity_stepc.py` (SHA-256 `5f45ec65e7266b29146567190fa906084da958f9dca2bf490b394ec0f4defe8b`). It differs from the original in that step only: on `--map fixed` each district is the union of the voting areas the assignment gives it. On `--map tuning` it is unchanged. Its baseline efficiency gap equals the partisan lane's and R1's on the same map (+1.45%).

**Part 2: the redraw-test scorer takes the scored map.** At `42b5fda8`, `territory_score.py` (SHA-256 `0485e788…2b55`) builds its territory from the scored map only in `rank`. `plans` and `calibrate` build it from Step A's list, so on a rerun (Amendment 8, Part 5) they fail with a shape mismatch. The registered scorer becomes `territory_score.py` at the commit that adds `--enacted` and `--stated-low` to `plans` and `calibrate`, passed to the same `Substrate` that `rank` uses (SHA-256 `47ead0966445b4f2a3aefbc33102b155666b7bf7fd7f1b0c263c17367fd9a142`). Without `--enacted` both subcommands behave exactly as before. Check: on Step C's plans, `plans --enacted` reproduces Step C's `scores.csv` byte for byte (made with the wrapper `score_plans_enacted.py`, SHA-256 `9ed54016…c79a`), and `calibrate --ref 1 2 4 6 --holdout 5 --enacted` reproduces its `calibration.json` byte for byte (made with `calibrate_enacted.py`, SHA-256 `db227364…5da`). The fix is commit `569250cd` on branch `a8-territory-null`. The two wrappers are then no longer needed; they stay in `findings/a10_stepc/territory/` as the record of what Step C ran.

**Part 3: a redraw-test chain that does not seed.** Amendment 8 runs chains 1 to 5 from the registered drand round (salts `a8-territory-null-chainN`, N the chain's index). Chains 1 to 4 are the reference and chain 5 is the holdout. A chain *does not seed* when `territory_null.py` exits before its first step because `recursive_tree_part` finds no starting plan. Then:

1. That chain is retired and recorded as retired with its log. It is not rerun with another seed or setting.
2. Its place is taken by the next index not yet used: 6, then 7, and so on, with the same code, salt pattern, run length and thinning. A replacement for a reference chain joins the reference set. A replacement for chain 5 becomes the holdout.
3. Whether every chain seeds is settled when the chains are launched, before any plan is scored. The reference and holdout chains are written into the run record at that point.

This is the rule Step C applied, citing Amendment 5, Part 14 (set D's index 250, retired because it does not seed; the next free index is used). Step C retired chain 3 and used chain 6.

**What this amendment does not change.** No test, threshold, null, ensemble, statistic, flag rule or outcome rule. The 2×2 outcome, X1, the size-matched sets, the qsgy8 tripwires, R1 and R2 are scored exactly as Amendments 5 to 10 say. The Step C results stand as recorded, labelled provisional. This amendment gives no conclusion on whether any map is a gerrymander.

**Outside this amendment (on GitHub, not registered).** These changes were also made after Step C. They are tooling and data checks, not registered rules.
- `analysis/scripts/run_stepc.py` runs Step C as one command and stops at the first failure.
- `analysis/scripts/check_changed_reproduced.py` checks before scoring that the map's geometry agrees with Step A's list of changed districts. On the provisional map it flags Edmonton-Meadows.
- `analysis/scripts/vote_anywhere_splat.py` builds the all-ballots substrate with the Vote Anywhere ballots included; it is used by the seat-claim test, not by Step C.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-05 (Alberta time)

## Amendment 12 — All 2023 ballots replace election-day ballots in every registered step that uses votes

> **Status: in force.** Written 2026-11-07, about 7:20 AM Alberta Time (UTC−6), at the author's direction ("do the amendment"), before the official map has been posted or scored. **Not blind:** results on all ballots for the reconstructed panel map and the commission maps had already been seen (`findings/allballots_ranking/`, `findings/iap_para167/`). Their effect on outcomes is disclosed in Part 5.

**Why.** The registered steps use 2023 election-day votes. Those leave out about half of 2023's ballots (advance, mobile, special and Vote Anywhere), which Elections Alberta reports only by division. On the 2019 map, election-day votes elect 57 UCP and 30 NDP; the 2023 result was 49 and 38. The all-ballots substrate puts those ballots back by voting area, matches the official result in every 2019 division, and returns 49 and 38 (`findings/seat_claim_test_result.md`, substrate D).

**Part 1: the substrate.** Every registered step that uses 2023 votes uses `data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg` (SHA-256 `c9e21ac90fb97b9ee4a7e4da7c80d44922e5849842fc283344f724bb2711be72`, built by `analysis/scripts/vote_anywhere_splat.py --primary` at commit `4f7de6bb`). These steps are:
- the specification's partisan lane, P1 to P5;
- the structural lane's S5 (neighbour drain), which classes districts by their 2023 vote margins;
- the size-matched sets' competitive-seat test and their reported partisan measures (Amendment 5, Part 14);
- the redraw tests R1 (swing zone) and R2 (drain) (Amendment 8).

Steps that use no votes are unchanged: S1 to S4 and S6, X1, towns over-divided and the city-versus-rest test.

**Part 2: the ensembles.** Each ensemble is the same set of plans, rescored on all ballots. The chains are replayed from their registered seeds with `--va-file` pointing to the file above. A replay counts only if every vote-independent column matches the original run row for row.
- **Already replayed and checked:** the canonical ensemble (4 × 252,500) and set D (91 districts). Hashes are in `findings/allballots_ranking/README.md`.
- **Replayed before the official map is scored, under the same check:** sets A, B and C, and Amendment 8's territory null for R1 and R2.

**Part 3: thresholds.** Every registered threshold defined as a percentile of an ensemble is taken from the replayed ensemble, by the same rule.
- **P1:** its fixed line (+4.10%) was the canonical ensemble's 95th percentile on election-day votes (thresholds.md #42; Amendment 5, Part 19). On all ballots that percentile is **+1.39%** (0.01394), and that is P1's threshold under this amendment.
- **S5:** its line is the midpoint between the commission maps' drain scores (Amendment 5, Part 7). On election-day votes that is 0.0039018 (majority 0.0072127, minority 0.0005909). On all ballots, by the same rule, it is **0.0019398** (majority 0.0037118, minority 0.0001678; `findings/amendment12_checks/`). The flag still fires below the line.
- **P2 to P4, the Part 14 tests, R1 and R2:** these are ranked within their ensembles, so their rules do not change.
- **No other threshold moves.**

**Part 4: election-day results are still computed.** Every registered step is also run on election-day votes and reported beside the all-ballots result, as a sensitivity. The provisional Step C reading (`findings/a10_stepc/`), on election-day votes, stands as filed.

When the official map is posted it is processed at once, under the owner's standing order of 2026-11-05. If any replay in Part 2 has not finished by then:
- the election-day run goes first, labelled a sensitivity;
- the registered result is the all-ballots run, made as soon as the replays pass;
- the run record states the order.

**Part 5: what this changes on results already seen.** Disclosed so that no reader has to work it out.
- **The reconstructed panel map, structural lane:** 2 of 5 on both ballot sets. Its drain score is 0.00442 on election-day votes and 0.01043 on all ballots, above the line on both, so S5 does not fire.
- **The reconstructed panel map, partisan lane:** 1 of 4 on both ballot sets. P4 is at p98.8 on election-day votes and p98.82 on all ballots. P1 does not fire on either (+1.45% against +4.10%; −1.66% against +1.39%). P2 is at p19.7 and p79.45. P3 is at p52.4 and p48.22.
- **The commission minority map:** this amendment governs the scoring of the November map. It does not reopen the registered Phase 1 results. But the same rule applied to the minority map would move its partisan lane from 3 of 4 to **4 of 4**: its efficiency gap on all ballots (+2.55%) is above +1.39%, where its election-day gap (+4.02%) was just below +4.10%.
- **The commission majority map:** 0 of 4 on both ballot sets.

**What this amendment does not change.** Every test, null, statistic, flag rule and outcome rule other than the vote substrate, P1's line and S5's line. That includes the 2×2 outcome, X1, the structural lane apart from S5's line, the qsgy8 tripwires and the 3-of-5 and 2-of-4 counts.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-07 (Alberta time)

## Amendment 13 — How Amendment 12's replays are met: the redraw-test null, and set A without chain 201

> **Status: in force.** Written 2026-11-07, about 11:50 AM Alberta Time (UTC−6), at the author's direction ("yes to both"), before the official map has been posted or scored. **Not blind:** the all-ballots rehearsal on the reconstructed panel map (`findings/amendment12_rehearsal/`) had already been run, and its results are disclosed in Part 3.

**Why.** Amendment 12, Part 2 requires the ensembles to be replayed from their registered seeds on the all-ballots file, and a replay counts only if every vote-independent column matches the original row for row. The rehearsal found two places where that rule cannot be applied as written.

**Part 1: the redraw-test null (R1 and R2, Amendment 8).** The territory null's sampler (`analysis/scripts/territory_null.py`) reads no votes. Its plans depend only on population, the voting-area graph and the seed. Votes enter only when plans are scored (`territory_score.py`, `Substrate`). A replay "with `--va-file`" would therefore draw the same plans, and the script has no such option.
- **Rule:** Part 2 is met for R1 and R2 by scoring the null's plans on the all-ballots file. Before scoring, each plan file's SHA-256 is checked equal to the file the null wrote.
- **For the official map:** its own null is run once from the registered seeds (Amendment 8, Part 5). Its plans are scored on all ballots (the registered result) and on election-day ballots (the sensitivity, Amendment 12, Part 4).

Nothing else about R1 or R2 changes.

**Part 2: set A without chain 201.** Set A's chain 201 (91 districts, 47,500 steps, an early chain kept in `data/simulation_checkpoints_k91`) does not replay. On all ballots, its `step` and `n_parts` columns match, but `population_mad` differs in 47,497 of its 47,500 rows. So the replay is not the same set of plans, and under Part 2 it does not count. The cause has not been established.
- **Rule:** on all ballots, set A is chains 221–224.
- **On election-day ballots:** set A keeps chain 201, as filed, and the election-day sensitivity is reported on both chain lists.

No other chain is excluded by this amendment. Any other chain that fails its replay check is reported and dropped by the same rule.

**Part 3: what this changes on results already seen.** On the reconstructed panel map (provisional), the rehearsal reads the same as the filed Step C:
- 2 of 5 structural flags, and 1 of 4 partisan flags (seats at 50/50, p98.8);
- X1 not met;
- R1 p = 0.914 and R2 p = 0.419 on all ballots (0.665 and 0.597 on election-day ballots), neither flagged.

On set A (chains 221–224), the city-versus-rest test is at p99.6 on all ballots (p99.5 as filed). Set A is the ±12.5% set; as filed, the statute's own bands (sets B and D) do not flag it.

**What this amendment does not change.** Every test, threshold, null and outcome rule, and every other part of Amendment 12.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-07 (Alberta time)
