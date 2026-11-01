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
**Amendment 5** (2026-11-01) consolidates every later change and is to be filed there.

---

## Table of amendments

| Date | File | Trigger | Key changes |
|---|---|---|---|
| 2026-04-23 | Amendment 1 | Five corrections after initial upload | Urban-weight parameter corrections (C1–C4); AI toolstack disclosure (C5) |
| 2026-04-27 | Amendment 4 | Final hardening | 250k ensemble locked; v0_9 topology; headline s50=48.31%@p98.5; drand seed pre-committed |
| 2026-11-01 | Amendment 5 | Consolidation of every unfiled change (earlier entries 2, 3, 8–25, 27, 28) | 40 parts, grouped by registered document; mapping table at its end |

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
