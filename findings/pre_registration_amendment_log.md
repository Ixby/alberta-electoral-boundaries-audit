---
name: Pre-registration amendment log (consolidated)
description: Complete dated chain of all amendments to the audit's pre-registered signature-detection checklist, from initial upload through final hardening. Four source files merged 2026-05-12.
type: project
---

> **Backward:**
> - `analysis/reports/pre_registration_draft.md` — the document being amended
> - `analysis/reports/pre_registration_amendment_2026-04-26_evening_post_audit.md` and the other dated amendment files merged here
>
> **Forward:**
> - `findings/README.md` — indexes this finding
> - (leaf — consolidated amendment record; reviewer-facing)

# Pre-registration amendment log

**Registration:** Pre-registered signature-detection checklist for the Select Special Committee on Electoral Boundaries' map.  
**Author:** Will Conner.  
**Original upload:** 2026-04-23, 06:22 PM MT (OSF Registrations).  
**On OSF:** the checklist with Amendments 1 (2026-04-23) and 4 (2026-04-27), as files in registration 9wp5y (registered 2026-05-07).  
**Amendment 5** (2026-11-01) consolidates every later change and is to be filed there.

---

## Table of amendments

| Date | File | Trigger | Key changes |
|---|---|---|---|
| 2026-04-23 | Amendment 1 | Six corrections after initial upload | Urban-weight parameter corrections (C1–C4); AI toolstack disclosure (C5); DPG sunset clause (C6) |
| 2026-04-27 | Amendment 4 | Final hardening | 250k ensemble locked; v0_9 topology; headline s50=48.31%@p98.5; drand seed pre-committed |
| 2026-11-01 | Amendment 5 | Consolidation of every unfiled change (earlier entries 2, 3, 8–25, 27, 28) | 28 parts, grouped by registered document; mapping table at its end |

**Note on publication status (author's ruling, 2026-10-31; not an amendment).** The audit is unpublished until November 3, 2026. Entries in this log dated before then record draft revisions made while the audit was being prepared, not retractions of published claims. Where an entry says a claim was "retracted" or "withdrawn", it means the claim was removed from the draft before publication.

---

## Amendment 1 — 2026-04-23

**Filed:** 2026-04-23.  
**Reason:** Six corrections and additions identified after initial upload. No thresholds or hypotheses altered. Changes 1–4 correct stale weight parameters not updated when the central urban-weight estimate was revised from 0.70 to 0.85 earlier in the analysis session. Change 5 adds a toolstack disclosure. Change 6 adds a DPG disclosure and 48-hour sunset-clause commitment.

---

### Change 1 — §11 Indices, B2 formula: central weight and sensitivity range

**Location:** §11 Indices and derived variables, B2 — Efficiency gap (EG), final sentence.

**Before:**
> For hybrid EDs, vote totals are estimated by blending the urban-core and rural-absorption portions at the specified urban weight (central estimate 0.70; sensitivity range 0.60–0.80).

**After:**
> For hybrid EDs, vote totals are estimated by blending the urban-core and rural-absorption portions at the specified urban weight (central estimate 0.85; sensitivity range 0.60–0.90).

**Reason:** Central estimate updated from 0.70 to 0.85 based on Calgary DA-level population density analysis conducted prior to registration. Sensitivity range extended from 0.60–0.80 to 0.60–0.90 to cover the full parameter space tested in the analysis scripts.

---

### Change 2 — §9 Manipulated variables: sensitivity sweep values

**Before:** Tested at 0.60, 0.70, and 0.80.  
**After:** Tested at 0.60, 0.70, 0.80, 0.85, and 0.90.  
**Reason:** Same as Change 1. Three-value list was from an earlier draft; actual analysis tests five values.

---

### Change 3 — §2 Study design, Component 2: parameter count and values

**Before:** "Sensitivity is tested across three urban-weight parameters (0.60, 0.70, 0.80)..."  
**After:** "Sensitivity is tested across five urban-weight parameters (0.60, 0.70, 0.80, 0.85, 0.90)..."  
**Reason:** Same as Changes 1–2.

---

### Change 4 — §3 Pre-registered tests, S4: sensitivity range

**Before:** "...sensitivity range 0.60–0.80 also reported..."  
**After:** "...sensitivity range 0.60–0.90 also reported..."  
**Reason:** Must match the range in the Indices section (Change 1).

---

### Change 5 — §15 Context: declared toolstack added

**Added:**
> **Declared toolstack.** This audit was produced using the following tools: Python 3.11 (pandas, numpy, geopandas/pyogrio, shapely, pyproj, GerryChain 0.3.2, textstat, pdfplumber, rapidfuzz, osmnx); Elections Alberta GIS data; Statistics Canada DA shapefiles; pdfplumber for commission report extraction; and Claude (Anthropic), a large language model used as an analytical and writing assistant throughout the project. Claude's role included: drafting and revising report text, proposing analysis structure and section outlines, identifying consistency gaps between documents, and surfacing edge cases in the methodology (e.g., the Vote Anywhere apportionment issue and the pre-registration disclosure requirement). All substantive analytical claims — metric values, thresholds, data provenance, and code outputs — were verified against primary sources and script outputs by the author. Claude did not execute code or access external data independently; all script runs were performed by the author in a local Python environment. The use of an AI assistant is disclosed here and in both the public and academic reports in accordance with emerging norms for AI-assisted research.

**Reason:** AI use disclosure omitted from initial upload.

---

### Change 6 — Derived Provisional Geometries (DPG) disclosure and sunset clause

**Location:** New Appendix A to the pre-registered protocol, and a corresponding disclosure in `report_academic.md` §4.1.4.

**Added:**
> **Derived Provisional Geometries (DPG).** All 2026 ED boundary geometries referenced in this pre-registration are DPG, reconstructed from the commission's 600-DPI PNG extractions via affine transformation, OpenStreetMap feature-class snapping, and population-calibrated parametric sweep. Two error modes are distinguished: (1) perimeter-mode uncertainty (±500 m typical) affects Polsby-Popper and Reock compactness scores; (2) area-mode uncertainty (Tier-dependent) can exceed 100% on individual Tier-C hybrid EDs. Full error-mode breakdown at `data/INTEGRITY_STATUS.md`.
>
> **Sunset clause.** All DPG-dependent metrics — Polsby-Popper band thresholds (C1), Reock band thresholds (C2), Phase 4C per-ED measured vote totals, MCMC real-map percentile placements, and any claim depending on spatial attribution of 2023 Voting Areas to 2026 ED polygons — are **provisional** until Elections Alberta publishes official 2026 topological shapefiles. The audit commits to: (1) re-running all DPG-dependent analyses against the official shapefiles within 48 hours of public release *(subsequently relaxed to two weeks — see Amendment 2, Change 11)*; (2) publicly disclosing any sign-flip or material magnitude change; (3) treating the official-shapefile recomputation as the **authoritative** result for every DPG-dependent metric.

---

### Summary — Amendment 1

| # | Section | Nature | Effect on findings |
|---|---|---|---|
| 1 | §11 B2 formula | Correction — weight values | None; aligns text with scripts |
| 2 | §9 Manipulated variables | Correction — parameter list | None; aligns text with scripts |
| 3 | §2 Study design | Correction — parameter count and list | None; aligns text with scripts |
| 4 | §3 S4 threshold | Correction — sensitivity range | None; aligns text with §11 |
| 5 | §15 Toolstack | Addition — AI use disclosure | None; additive disclosure only |
| 6 | App. A | Addition — DPG disclosure + sunset clause | None immediate; binds future recomputation |

---

## Amendment 4 — 2026-04-27 (final hardening)

**Filed:** 2026-04-27.  
**Trigger:** Final parameter locking and methodological hardening prior to publication of final academic and public reports. All prior parameters superseded by this amendment for published headline findings.

---

### Change 1 — MCMC ensemble locked at 250,000 maps

**Final state:** Four parallel chains × 62,500 maps = **250,000 total maps**.  
**Rationale:** The exact scale progression (10k→100k→250k) is logged to pre-empt p-hacking accusations. After v0_9 resolved topological contradictions, statistical diagnostics confirmed convergence at 250k. No further scaling required.

---

### Change 2 — Hardening to v0_9 topological substrate

**Final state:** All quantitative metrics and ensemble scoring use **v0_9 canonical topological substrate**, achieving **100% geometric coverage (89-of-89 districts)** with zero attribution artefacts.

---

### Change 3 — Final headline `seats@50/50`

**Before (v0_8 DPG):** 52.8% at p98.6 (published pre-hardening).  
**After (v0_9 canonical):** **48.31% at p98.5** (top 1.5%).  
**Rationale:** 52.8% was an attribution artefact from the 83-of-89 geometric dropouts. 48.31% is the structurally and mathematically absolute value under the fully-hardened substrate. The core finding is unchanged: the minority map remains an extreme statistical outlier (only ~3,750 of 250,000 neutral procedures reach this value), crossing all pre-registered structural irregularity tests.

*Note: Amendment 4 predates the final canonical 1,010,000-plan ensemble run on official EA shapefiles (completed 2026-05-12). See `data/simulation_convergence_diagnostics_canonical.json` and `findings/joint_outlier_score.json` for the authoritative canonical numbers.*

---

### Change 4 — Pre-registration of November 91-seat map tripwire

**Registered tripwire:** The Drain Pattern (mid-sized city integrity) — flags an extreme structural anomaly if Airdrie, Red Deer, Lethbridge, or St. Albert are split into more than their population-dictated seats with >2% area overlap each.  
**Discarded tripwire:** The Lasso Pattern (Polsby-Popper compactness) — removed. Polsby-Popper discrepancies evaporated under the v0_9 substrate. Using a known-brittle metric as a tripwire was struck from the evaluation pipeline.

---

### Change 5 — Absolute magnitude fallacy disclosure

Critics claiming that updating minority `seats@50/50` from 52.8% to 48.31% represents "a shift toward neutrality" commit the Absolute Magnitude Fallacy. Under Alberta's statutory constraints and 2023 vote distributions, a perfectly neutral (median) map yields only **46.1%**. Therefore 48.31% remains a top-1.5% structural outlier. Qualitative finding unchanged.

---

### Change 6 — ESS and autocorrelation disclosure

Official reported ESS: ~375 independent draws from 250,000 total maps. ReCom chains on highly-constrained 89-node graphs have high autocorrelation (integrated autocorrelation time τ > 300), which is why the chain was scaled to 250k instead of the academic standard of 10k.

---

### Change 7 — Cryptographic seeding for November testing

`drand_seed.py` locked to round 6062459 (2026-04-27). This seed is exclusively bound to future randomised testing of the November 91-seat map, pre-committed six months before the November data exists. The historical 250k simulation uses deterministic hardcoded seeds (e.g., seed 42) for bit-identical reproduction.

---

### Archival and namespace clean-up

Historical v0.1–v0.8 code and data artefacts preserved in `historical/` subdirectories. Active project namespace de-versioned. All script references streamlined for independent auditors.

**Signed:** Will Conner, Project Author  
**Date:** 2026-04-27

---

## Amendment 5 — Consolidated record of the changes made after Amendment 4

> **Status: in force.** Signed 2026-11-01 (Alberta time) on the author's direction in session ("Squash all unfiled amendments into one, even if already signed, check for accuracy, reset amendment number to reflect the next slot on osf"), with the author's decisions on how registration qsgy8 relates to the specification (Part 6) and on S6's pattern P4 (Part 24). No committee map, and no result from one, had been seen in session at signing.

Parts 29–39 added 2026-11-01 after the corpus check, on the author's direction ('Apply all as proposed').

**What this amendment is.** Amendments 1 and 4 are the only amendments filed on OSF; they are files in registration 9wp5y, registered 2026-05-07. The audit's in-repository log (`findings/pre_registration_amendment_log.md`) also holds entries numbered 2, 3, 8–25, 27 and 28, dated 2026-04-26 to 2026-11-01. None of them was filed. This amendment replaces all of them and states only the changes still in force, grouped by the document each one changes. Numbers 5 to 7 were never used, and this amendment takes number 5. The entries it replaces are removed from this log; their full text, as signed, is in the repository's history (commit `ca539bc4` holds the last version). Numbers 6 and 7 stay unused. Amendment 26 (size-matched sets for a map of any seat count, signed on branch `size-matched-candidate`) is not part of this amendment and is not on OSF.

**Publication status.** The audit is unpublished until November 3, 2026. Where earlier entries say a claim was "published", "retracted" or "withdrawn", they mean a draft was revised. The same applies to the registered documents in `preregistration/`: where they speak of findings already published (for example "an author who has already published findings" in `lane3_process_scorecard_draft.md`, and "the audit's published headline" in `t3_2_majority_rural_isolation_design.md`), they mean the draft.

#### A. The pre-registered checklist (OSF 9wp5y; Amendments 1 and 4)

**Part 1 — Official boundaries and the canonical ensemble replace the provisional geometry and the 250,000-plan ensemble.**
- *Boundaries.* Elections Alberta's official 2026 shapefiles were received on 2026-05-06. Under the sunset clause (Amendment 1, Change 6), every metric that depended on the derived provisional geometries (v0_7 to v0_9) was recomputed on them.
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
On 2026-04-26, before the shapefiles were released, the window in Amendment 1, Change 6 was relaxed from 48 hours to two weeks. The duty to recompute, to disclose any change of sign, and to apply the clause to both maps did not change. The shapefiles arrived on 2026-05-06. The headline recompute closed on 2026-05-18 (day 12). Full integration, including the re-run of the drain test, closed on 2026-05-23 (day 17, three days past the window) (`preregistration/retraction_conditions.md` §6.1). The same two-week window applies to the November map if it is first released only as PDF or image files (scoring specification, §2).

**Part 3 — The Alberta-calibrated efficiency-gap line.**
The efficiency gap is reported against the US 7% line and an Alberta-calibrated line. The Alberta line is Threshold #42 in `preregistration/thresholds.md` (Option D): +4.10%, the canonical ensemble's 95th percentile when it was registered. The 2026-07-12 rerun gives +4.08% (0.04084); the threshold stays at +4.10%. This replaces the "about 5%" line (4.37%) of 2026-04-26. The same +4.10% is the November test's P1 threshold.

**Part 4 — The November drand round (Amendment 4, Change 7).**
`analysis/scripts/drand_seed.py` uses drand round 5500000 (October 2025), not round 6062459. Round 5500000 was public before the salts were fixed, so it cannot anchor the November test. The November round is to be a round at or after the first publication of the committee's final map. At the time of this amendment no round has been pinned (`preregistration/seed_commitments.md`, entry `november_2026_scoring_spec`).

**Part 5 — Declared toolstack (Amendment 1, Change 5).**
Two more tools were used: Gemini (Google), for adversarial review of the code, and Codex (OpenAI), for scripting and data processing. Claude also worked as a coding agent (Claude Code): on the author's direction, its sessions ran scripts and committed changes, including ensemble runs, scoring and site builds. Each such change is in the repository's history.

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

- *Excluded.* S4 (median Polsby–Popper, 0.4366 on both maps) is measured and reported but not counted. P6 (St. Albert–Sturgeon) is listed when it matches but does not count toward S6, because the majority map has the same district.
- *Verdict.* The lane reads "replicated" when 3 or more of the 5 flags fire. On the official boundaries the minority map scores 5 of 5 and the majority map 0 of 5 (`findings/structural_battery_result.json`; `findings/structural_battery_majority.json`).
- *The script.* `analysis/scripts/run_structural_battery.py` flags S1 at 3382.50 or above, and S5 below 0.0039018, the unrounded midpoint of 0.0072127 and 0.0005909.
- *Specificity.* The lane is a screen, not a significance test. How often each flag fires on neutral maps is reported beside the verdict:
  - S1 fires on 255,934 of the 1,010,000 canonical plans (25.34%; 87-district plans).
  - A calibration on 200 neutral 91-district maps from set D (`findings/structural_lane_calibration_2026-10-31.md`; not a registered test) found the lane reading "replicated" on 93.5% of them.

**Part 8 — §1 agrees with §3.** The first outcome in §1 requires at least two of P1–P4 in the UCP direction, as the §3 verdict rule does. The earlier "at least one" was a drafting error, not a separate threshold.

**Part 9 — Declination sign (P3).** Declination is (2/π)(θ_D − θ_R), as Warrington (2018) defines it: positive favours the UCP (`analysis/scripts/mcmc_ensemble.py:227`). The canonical chain files carry this sign. On the canonical ensemble:
- minority map: +0.0770 (p98.79);
- majority map: −0.0267 (p21.85);
- 2019 map: +0.0451 (p91.33).

**Part 10 — Reference ensemble.** §2 calls the canonical ensemble fixed. It was regenerated on 2026-07-12 (Part 1), before any committee map existed, under the same paths, seed and parameters. P2–P4 are placed against the rerun. P1's threshold stays at +4.10%.

**Part 11 — Publication step.** In §7, step 5, `python analysis/scripts/build_html_reports.py` is withdrawn; the script no longer exists. The step is `cd viewer && npm run build`, plus the commit of the markdown reports. The 72-hour commitment is unchanged. §7 also says `run_structural_battery.py` and `verdict_synthesis.py` do not exist yet; both now exist in `analysis/scripts/`.

**Part 12 — The committee's name.** The specification calls it the "Special Select Committee". It is the Select Special Committee on Electoral Boundaries, created by Government Motion 37, passed on 2026-04-21. The pinned file is not edited.

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
- *Harness fixes.* The fast-fail for infeasible pairs, the checkpoint and resume, the rebuilt partitions, and the correction of the unreachable s.15(2) branch in `mcmc_ensemble.py` all preserve the distribution. They are at commit `01095181` (patch SHA-256 `84f85728…3a35`). Chains 201 and 100 ran before these fixes and later chains after; both are valid draws from the same distribution.

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

**Part 18 — What was known before set D was made primary.**
Before set D was made primary (2026-10-31, 00:00 MDT), the flags for the two commission maps against the 89-district sets had been computed and committed (commit `2ecd7931`, 2026-10-30 19:07 MDT; `findings/size_matched_results_2026-10-30.md`, provisional). By the author's account, those flags had not been looked at.

| Map | Measure | A | B | C | D |
|---|---|---|---|---|---|
| Minority | Competitive seats | p0.2 flag | p0.2 flag | p0.1 flag | p0.3 flag |
| Minority | City versus rest | p99.9 flag | p93.0 | p87.8 | p71.7 |
| Minority | Towns split | p33.3 | p45.0 | p100.0 flag | p47.5 |
| Majority | All three | no flag | no flag | no flag | no flag |

Choosing set D removes the minority map's city-versus-rest flag from the primary comparison. It is still reported under set A.

The only prior information about the advisory panel's draft was a meme posted on Facebook, archived at `preregistration/evidence/2026-10-29_facebook_meme_panel_draft.md`.

#### E. `preregistration/thresholds.md`

**Part 19 — Errata (no threshold moves).**
- The ±25% band is EBCA s.15(1), not s.14.
- Option C (#41) is complete (2026-05-12). 42 items are catalogued, 41 of them thresholds.
- The official shapefiles arrived on 2026-05-06. The s.15(2) area figures are still taken from the commission's text.
- Option D's registered threshold is +4.10%. The rerun ensemble's 95th percentile is +4.08%. Against that ensemble the minority map is at p94.54 and the majority map at p16.52; the ensemble's median is +1.63% and n_eff is 1,413–1,522.
- §B.2.1.D: every canonical neutral plan has 87 districts, and the band applies around a quota of 2021 population ÷ 87. The 89-district shapefiles only score the commission maps.
- Part A, row #42 gives the ensemble's 95th percentile as +0.0410 and cites `data/simulated_ensemble_percentiles_canonical.csv`. The file is at `data/outputs/`, and the rerun gives 0.04084. The registered threshold stays +4.10%.
- Rows #3 and #4 give s.15(2)(b) as "> 100 km from major centre" and (c) as "4,000 residents". The Act reads more than 150 km by highway from the Legislature Building, and no town of more than 8,000 people (`preregistration/terms_of_reference.md` §3d). The audit computes the Act's values (Part 15).
- B.1.5 gives Canmore-Banff 1 of the 5 criteria and Rocky Mountain House–Banff Park 2. Computed on the official boundaries, they meet 3 and 5 (`data/outputs/s15_2_real_maps.json`).
- Rows #14 and #15 still hold the urban weight before Amendment 1 (0.70; range 0.60–0.80). Amendment 1 set 0.85 and 0.60–0.90, and Part 1 retired the model.

**Part 20 — Scenario E1.** The P1 threshold was committed in the same commit as the detection run (`282bc6d`). The claim that it "predates detection by 2 hours 24 minutes" was removed from the draft. B.3.2 and D.2 item 1 repeat the claim; it is withdrawn there too.

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
- *Disclosed: pattern P4.* One of S6's patterns is not one the chair objected to. P4 is a Calgary district joined with Bearspaw or Rocky View. In the addendum the chair wrote that he did not consider the Bearspaw and Springbank hybrids unreasonable, and "may well have agreed with them" (p. 67). P4 stays in S6 as registered; the label is disclosed here, not changed in the test.

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

**Part 26 — Errata.** The canonical ensemble has 1,010,000 plans, not 100,000. `seed_issue14.md` is the seed commitment for the Issue #14 counter-map challenge (OSF submission pending), not the canonical ensemble's. `seed_commitments.md` also calls qsgy8 the "MCMC seed" registration and says the specification is "mirrored" in it. Neither holds: qsgy8 (2026-05-06) holds a Phase 2 comparison and the prospective plan in Part 6, with a bootstrap seed (drand round 5500000, salt `lunty-bootstrap`), and it predates the specification. Registrations w2s8k, r3zm7, qsgy8, 6pt83, yvc7g and s58a6 each carry the same two plan files; the checklist and Amendments 1 and 4 are in registration 9wp5y.

#### J. `preregistration/osf_forest_recom_robustness.md` (OSF he53s)

**Part 27 — Changes made after filing.** Registration he53s was filed publicly on 2026-07-10, before any Forest-ReCom sample existed. Afterwards:
1. The execution harness was wired (chain salts and burn-in per §6.4), and `run_ensemble` gained a `proposal_method` parameter, which leaves the default path unchanged.
2. A crash at chain-0 seeding (a missing import) was fixed. It happened before any proposal was drawn.
3. The executed code was committed after the run, not before it.
4. The sampler is multi-root Wilson (loop-erased random walk). §6.1's "Aldous-Broder" names a different algorithm that samples the same distribution, and §6.1's own citations point to Wilson's method.
5. The ESS target (at least 200 per metric per chain) was missed: pooled n_eff was 61–124. The result was reported with the shortfall disclosed. That choice was made after the run.

The hypotheses, the ±5-percentile-point decision rule, the run size, the seeds and the output paths were executed as registered. All four metrics are Robust.

#### K. `reports/academic/report_academic.md` §6.2.6 (pre-committed falsifiers)

**Part 28 — The premise of item 2 is struck.** The item no longer opens with "The 2019 cross-election direction reversal extends to 338Canada April 2026 polling". On the official 2019 files there is no reversal: the minority remains the more UCP-favourable map (ledger C44). The test stands as written: if more recent polling shows the direction flipping under several 2020s-era voter distributions, the structural pattern becomes harder to read as engineering. (Item 1 follows Part 22.)

#### What this amendment does not change

The November scoring specification itself is not edited, so its SHA-256 pin still holds; its references to Amendments 8, 9, 11 and 12 are translated by the table below. The 2 × 2 verdict surface, the partisan-lane rule (at least 2 of P1–P4), every threshold value above, and the 72-hour commitment are unchanged.

The registered rules that did change are:
- the structural-lane rule (Part 7, June 2026);
- the municipality weight W (Part 14);
- the s.15(2)(b) measurement (Part 15);
- the choice of set D as primary (Part 14);
- the stricter rule on when a result is final (Part 16).

The amendment entries that made these changes all record that they were signed before the committee's map was due on November 2, 2026, and before any committee map had been published.

#### Where the earlier entries went

| Old | New part(s) | Not carried (reason) |
|---|---|---|
| 1 | Updated by Parts 1, 2 and 5 | Filed; stays as filed |
| 2 | C10 → 3; C11 → 2 | C1 (2M; reversed by 3 and 4), C2–C3 (supplementary analyses), C4–C5 (superseded by Amendment 4, then Part 1), C6–C9 (result revisions, not rules; superseded by the official-boundary recompute), Bucket C (superseded by Parts 6–13) |
| 3 | 5 | Bug record, interim claims and 2M postscript (superseded by Amendment 4, which is filed, and by Part 1) |
| 4 | Updated by Parts 1 and 4; C4 extended by Part 17 | Filed; stays as filed |
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
