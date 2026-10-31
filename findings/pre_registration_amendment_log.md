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
**Amendments filed:** 2026-04-23 · 2026-04-26 (morning) · 2026-04-26 (evening) · 2026-04-27 · 2026-06-10 · 2026-06-11 · 2026-06-12 · 2026-07-10 · 2026-07-11 · 2026-07-12 · 2026-10-29 · 2026-10-30 · 2026-10-31.

---

## Table of amendments

| Date | File | Trigger | Key changes |
|---|---|---|---|
| 2026-04-23 | Amendment 1 | Six corrections after initial upload | Urban-weight parameter corrections (C1–C4); AI toolstack disclosure (C5); DPG sunset clause (C6) |
| 2026-04-26 AM | Amendment 2 | Methodology evolution since 04-23 | MCMC enlargement 100k→2M (C1); short-bursts test (C2); rural analysis (C3); 89-of-89 attribution (C4); v0_7→v0_8 (C5); five test-result revisions (C6–C11) |
| 2026-04-26 PM | Amendment 3 | Gemini code audit — 9 pipeline bugs, 3 critical | Bug-fix remediation record; interim claim revision; 2M ensemble rescinded in postscript |
| 2026-04-27 | Amendment 4 | Final hardening | 250k ensemble locked; v0_9 topology; headline s50=48.31%@p98.5; drand seed pre-committed |
| 2026-06-12 | Amendments 5–7 | Numbering reconciliation | See entry |
| 2026-06-10 | Amendment 8 | November scoring spec | S2 metric clarification |
| 2026-06-11 | Amendment 9 | November structural-lane threshold rule | Midpoint anchoring |
| 2026-06-12 | Amendment 10 | Declination sign convention | Correction |
| 2026-06-12 | Amendment 11 | Spec §1 ↔ §3 | Alignment |
| 2026-06-12 | Amendment 12 | Spec §6 pinning | Self-invalidating pin retired; phantom Amendment 11 entry retired |
| 2026-07-10 | Amendment 13 | Forest-ReCom Phase A | Post-registration code changes |
| 2026-07-11 | Amendment 14 | Publication path | One HTML rendering |
| 2026-07-12 | Amendment 15 | Second ensemble defect | Canonical ensemble scrapped and rerun |
| 2026-10-29 | Amendment 16 | Test X1 (Recommendation 5) | Written scoring rule |
| 2026-10-29 | Amendment 17 | November scoring | Size-matched neutral maps; X1 (a)/(b) rule; three added tests |
| 2026-10-29 | Amendment 18 | Errata | Citations, labels and stale status lines in registered documents |
| 2026-10-29 | Amendment 19 | Errata | A withdrawn timing claim in thresholds.md |
| 2026-10-29 | Amendment 20 | Neutral-map sets | Statute-band, municipality-aware and s.15(2) sets; harness fixes; town-split framing |
| 2026-10-29 | Amendment 21 | s.15(2) spec; Amendment 17 corrections | s.15(2) criteria fixed and checked against the commissions; effective-sample rule; labels; municipality weight W = 0.5 anchored to the 2019 map |
| 2026-10-30 | Amendment 22 | Errata | thresholds.md Option D: the neutral plans have 87 districts, not 89 |
| 2026-10-30 | Amendment 23 | Erratum | s.15(2)(b) distance measured to the district boundary itself; the s.15(2) set is rerun |
| 2026-10-31 | Amendment 24 | Primary size-matched set | Set D (s.15(2), Amendment 23 rule) is the primary size-matched comparison; A–C beside it; headline unchanged |

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

## Amendment 2 — 2026-04-26 (morning)

**Filed:** 2026-04-26.  
**Prior amendment:** Amendment 1 (2026-04-23).  
**Reason:** Eleven changes to the retrospective component (RQ1–7). Bucket A: five additive enhancements. Bucket B: five test-result revisions. Bucket C: prospective component (RQ8–9) unchanged.

---

### Bucket A — Additive enhancements (no hypothesis change)

#### Change 1 — MCMC ensemble enlargement: 100,000 → 2,000,000 maps

*Note: This change was later rescinded in Amendment 3 (evening) postscript; ensemble ultimately locked at 250,000 in Amendment 4.*

**Before:** 100,000-map ensemble, seed 42.  
**After:** 2,000,000-map ensemble, seeded run sequence 42→44→88. Each enlargement (100k→250k→1M→2M) produced the same percentile placements within ±0.5pp.

#### Change 2 — Targeted-gerrymander short-bursts test added

New §2 Component 4: 800 bursts × 50 ReCom steps (40,000 total steps), maximising UCP seats at neutral votes while staying within statutory constraints. Result: 52.87% best `seats@50/50` reached — within rounding of the minority map's then-reported value of 52.8%.

#### Change 3 — Rural-representation analysis added

Comparative analysis of how each of the three real maps handles rural representation: per-voter representation weight, s15(2) special-rural EDs, rural ED average population vs ideal, hybrid ED count.

#### Change 4 — 89-of-89 inheritance-fill attribution + fuzzing scenarios

**Before:** 87 measurable EDs for majority, 83 for minority (spatial-join drops).  
**After:** 89-of-89 via inheritance-fill for sliver polygons that catch no VA centroids. Headline revised from 54.2% (45 of 83) to **52.8% (47 of 89)**. Fuzzing analysis (5 strategies + 10,000 random trials) brackets 51.7%–57.3%; 89% of trials place minority above the 2M-ensemble's 51.72% ceiling.

#### Change 5 — Geometry transition v0_7 → v0_8 (full coverage)

v0_8 full-coverage polygons provide 89-of-89 coverage for both maps via 2019-Tier-A inheritance fill for districts whose 2026 boundaries could not be directly reconstructed. DPG sunset clause (Amendment 1) continues to apply.

---

### Bucket B — Test-result revisions (evidence-driven changes)

#### Change 6 — Lethbridge rationale removed ("six of seven" → "five of six")

Methodology review (`lethbridge_federal_boundary_check.md`) determined the minority report makes no federal-boundary claim traceable to a primary source. Removed from the rationale-validity test.

#### Change 7 — Banff Park rationale: "zero residents" softened

Polygon-clipped DA-population pull found ~491 area-weighted residents in the Banff extension (not zero). Framing updated to reflect what evidence supports. Verdict ("Fail") unchanged.

#### Change 8 — Cross-election direction retracted under v0_8 full coverage

v0_7 partial coverage produced a spurious "direction reverses under 2019 votes" finding (22 unattributed rural EDs systematically excluded). v0_8 full coverage: three of four metrics hold direction across both vote substrates; only mean-median flips. Original v0_7 finding retracted as a partial-coverage artefact. New authoritative reading: direction holds; magnitude is vote-distribution-dependent.

#### Change 9 — St. Albert-Sturgeon "stands" verdict: evidentiary basis updated

**Before:** "No other configuration satisfies both the community-of-interest and the ±25% rule simultaneously" (unproven non-existence claim).  
**After:** "The majority map and the minority map independently arrive at the same two-district structure — convergent-design framing." Verdict ("Stands") unchanged; framing more defensible.

#### Change 10 — Alberta-calibrated ~5% line added alongside pre-registered US 7% line

S4 now reports EG relative to two reference lines: (a) the pre-registered US 7% line (*Whitford v. Gill*); (b) the ~5% Alberta-calibrated line (95th percentile of audit's MCMC-ensemble EG distribution, empirical value 4.37%). Both lines reported for all three maps.

#### Change 11 — Sunset-clause window relaxed: 48 hours → two weeks

Automated pipeline for monitoring Elections Alberta endpoints not yet built. Two-week window is honest for a solo researcher without automation. Recompute commitment, sign-flip disclosure requirement, and symmetric application are unchanged.

---

### Bucket C — Prospective component (RQ8–9): unchanged

The 17-test grid (S1–S6, W1–W3, P1–P5, X1–X3) that will be applied to the November 2026 Lunty committee map is **unchanged**. All numeric thresholds unchanged. The 72-hour scoring commitment after the November map's release is unchanged. The ~5% Alberta-calibrated line (Change 10) will be reported alongside the pre-registered US 7% line for S4, additively.

---

### Summary — Amendment 2

| # | Bucket | Nature | Effect on findings |
|---|---|---|---|
| 1 | A | MCMC 100k → 2M *(later rescinded)* | Tighter precision on same percentile cutoffs |
| 2 | A | Short-bursts targeted-procedure test | Supplementary evidence |
| 3 | A | Rural-representation analysis | Supplementary; pre-empts rhetorical counter |
| 4 | A | 89-of-89 inheritance-fill; 54.2% → 52.8% | More defensible attribution |
| 5 | A | v0_7 → v0_8 geometry | Methodological improvement |
| 6 | B | Lethbridge claim removed; 6/7 → 5/6 | Defensibility improvement |
| 7 | B | Banff "zero residents" softened | Verdict unchanged; framing more accurate |
| 8 | B | Cross-election direction-flip retracted | v0_7 finding retracted; v0_8 authoritative |
| 9 | B | St. Albert convergence framing | Verdict unchanged; evidentiary basis improved |
| 10 | B | Alberta-calibrated ~5% EG line added | Additive; US 7% line still reported |
| 11 | B | Sunset clause 48h → 2 weeks | Honesty-of-commitment correction |
| 12 | C | Prospective RQ8–9 | Unchanged |

---

## Amendment 3 — 2026-04-26 (evening, post-audit)

**Filed:** 2026-04-26 evening MT — *before* the corrected MCMC re-run completes.  
**Trigger:** External code audit by Gemini surfaced nine pipeline bugs (three critical) across five conversation passes, all now remediated.  
**Audit-trail anchors:** `analysis/methodology/external_code_audit_brief.md`, `analysis/red_team/external_code_audit_findings_gemini_2026-04-26.md`, remediation commit `73544a3`.

---

### Bug findings

| Severity | Count | Highest-impact example |
|---|---|---|
| CRITICAL | 3 | 2M MCMC ensemble was structurally a stack of 100 independent 20,000-step short-bursts (chain state silently reset to 2019 baseline at every chunk boundary) |
| HIGH | 2 | `gpd.sjoin` against v0_8 polygons could double-count VAs in overlapping slivers |
| MEDIUM/NOTE | 4 | Unpinned `networkx` dependency; wrong declination sign-convention comment; rural classifier bucketed 7 unmatched EDs; uniform-swing shift not clipped to [0,1] |

All nine remediated. Commit `73544a3`. 3 new regression tests added.

---

### Interim claim status (pending corrected re-run)

Two published ensemble-derived numbers held in revision:
- Minority map `seats@50/50` at **p100 of 2M** — held
- Majority map `seats@50/50` at **p12 of 2M** — held

Post-dedup-fix real-map score (pre-ensemble): minority `seats@50/50` = **0.542** (vs. published 0.528). The sjoin dedup raised, not lowered, the minority value.

Non-ensemble evidence unaffected: Lane 2 structural tests, rationale-failure pattern, community splits, constitutional discussion, April 16 process record.

---

### Postscript — recalibration (2026-04-26 late evening)

Three events after this amendment was filed:

1. Gemini convergence diagnostics at 480k samples (24% of 2M complete) showed gold-standard Rhat 1.0001–1.0018. 2M determined to be statistical overkill.
2. The v0_9 topological VA-dissolve (commit `7cf47a4`) produced a planar partition with zero overlapping coverage, eliminating the 81/95 pixel-traced polygon overlaps. Re-scoring against v0_9 produced material headline-shifting deltas: minority `seats@50/50` 0.5422 → 0.4831.
3. **Recalibration decision**: 2M run cancelled at 1.6M samples. Audit recalibrated back to the pre-registered 100k baseline ensemble on the corrected pipeline + v0_9 substrate. *(Amendment 4 subsequently locks to 250k.)*

**Net effect:** Amendment 2, Bucket-A Change 1 ("100k → 2M") is rescinded. Ensemble size returns to 100k as interim; Amendment 4 locks to 250k.

**Updated AI-use disclosure:** Gemini 3.1 Pro (Google) added alongside Claude (Anthropic) as a load-bearing AI contributor. Five passes of adversarial code review authored by Gemini.

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

### Amendments 5, 6, 7 — Numbering reconciliation (added 2026-06-12)

T1.7 Referee #18 (model fable-5) flagged that this log self-describes as the "complete dated chain" but jumps from Amendment 4 (2026-04-27) directly to Amendment 8 (2026-06-10), with Amendments 5, 6, and 7 missing repo-wide. The honest reconciliation:

- **Amendment 5–7 were not omitted; they were never authored.** During the May 2026 canonical-substrate transition the audit chose to write substrate-supersession records as `findings/canonical_shapefile_log.md` entries, `findings/dpg_legacy_audit.md` bannered files, and inline §1.2 caveats rather than amendment-log entries — partly because those changes were substrate-driven (the documented sunset clause's expected behavior) rather than goalpost-moves in any pre-registered test definition. The numbering jumped 4 → 8 because the spec-edit cluster on 2026-06-10 (Amendment 8 onward) was the next event the audit's own discipline classified as a *pre-registration amendment* in the strict sense (changing a frozen scoring rule).

- **The numbering gap is unsatisfactory anyway.** Skipping 5–7 without documentation undermines the log's "complete dated chain" claim. This entry fills the slots with a single dated cross-reference rather than retro-numbering substrate-supersessions, which would be its own kind of re-writing-after-the-fact. Future amendments will start from 11 (the post-Amendment-10 number).

**Substrate-supersession events 2026-04-28 through 2026-06-09 that would have qualified for amendment numbers under a maximally-conservative reading:**
- 2026-05-06: Official EA shapefiles released; v0_8/v0_9 DPG substrate retired across all numeric findings (would have been Amendment 5)
- 2026-05-12: Canonical 1.01M-plan ensemble completed; superseded the 250k v0_7 DPG ensemble for all percentile-bearing findings (would have been Amendment 6)
- 2026-05-23: Canonical Phase 4C attribution + canonical neighbour-drain coupled-count + multiple sigma1.2 caveats (would have been Amendment 7)

The substantive records of these events exist at `findings/canonical_shapefile_log.md`, `findings/dpg_legacy_audit.md`, `findings/post_audit_recompute_deltas.md`, and the relevant §1.2 caveats; they were just never labelled as amendments. This entry retroactively names them but does not re-write them — the underlying substrate transitions are documented at their original locations.

**Signed:** Claude (acting as session agent, T1.7 #18 follow-up), to be reviewed by Will Conner  
**Date:** 2026-06-12

---

### Amendment 8 — November 2026 scoring spec S2 metric clarification (2026-06-10)

**What changed.** `preregistration/november_2026_scoring_spec.md` §3 structural-lane metric S2 was clarified from "municipalities split into 3+ EDs" to "municipalities split into 2+ EDs (canonical: 8)." The threshold ratio (1.5× majority's count) is unchanged; the effective threshold is now 12 (where it was ambiguous before).

**Why not a goalpost move.** The spec was pre-committed 2026-06-10 against an out-of-existence November Lunty map. The original "3+ EDs" wording was ambiguous about whether "splits" referred to aggregate counts (CSDs touching 3+ EDs) or new-split counts (CSDs gaining +2 EDs relative to 2019). The existing `findings/municipal_splits.md` pipeline (2026-04-24) reports the aggregate "2+ EDs" count with canonical baselines: majority = 8, minority = 11. Switching the spec to match the pipeline (a) removes the ambiguity, (b) anchors to a metric with a published canonical baseline, and (c) is impossible to reverse-engineer for a specific Lunty outcome because the Lunty map does not yet exist.

**Why an unamended reading is not feasible.** Computing a "3+ EDs" count would require re-implementing the municipal_splits intersection logic with a different threshold; the threshold itself was not anchored in any prior canonical artifact. Either choice (2+ or 3+) is defensible methodologically; only the 2+ choice has an existing canonical baseline.

**Effect on the November verdict.** S2 is one of six structural-lane flags. The amendment cannot move the verdict by more than one flag in either direction. The verdict surface (≥3 flags = "replicated") is unchanged.

**Signed:** Claude (acting as session agent), reviewed by Will Conner  
**Date:** 2026-06-10

---

### Amendment 9 — November 2026 structural-lane threshold rule: midpoint anchoring (2026-06-11)

**What changed.** `preregistration/november_2026_scoring_spec.md` §3 structural-lane threshold rule changed from "≥ 1.5× majority's baseline" (applied per metric) to *midpoint anchoring*: for each discriminating metric, the candidate's flag fires iff it lands on the minority's side of the midpoint between the two commission maps' battery-measured canonical values. Two structural changes accompany the rule change:
- **S4 (Polsby-Popper compactness median) is excluded from the flag count.** It is still measured and reported. Median PP is identical on both maps (0.4366) and the tail statistics run the wrong way (majority has more low-PP districts, 16.9 % vs 12.4 % below 0.30, and a lower minimum, 0.149 vs 0.175) — consistent with monograph H3 ("corridors drawn thick enough to make PP look innocent"). Compactness does not discriminate the two commission maps and cannot detect replication.
- **S6 predicate P6 (St. Albert-Sturgeon) is dropped from the discriminating set.** The majority map has the same-named ED, so the predicate is non-discriminating. P6 is still listed in `patterns_reproduced` when matched, for transparency, but does not count toward the S6 score. S6 is now scored against P1–P5 (max 5).

The verdict threshold remains ≥ 3 (now of 5, since S4 is excluded). The 5 discriminating metrics, their measured canonical anchors, and their midpoints are tabulated in the amended §3 of the spec.

**Why not a goalpost move.** The 1.5× rule was identified as miscalibrated when the full battery was first run end-to-end against the canonical commission maps (2026-06-10). With ≥ 1.5× majority's baseline, the **minority itself failed to classify as "replicated"** — it fired only 1 of 6 flags (S6 alone), because the minority/majority ratios on the other metrics sit at 1.30–1.39× (below 1.5×). The 1.5× rule was therefore demanding a Lunty map *more extreme than the minority on multiple dimensions*, which is incoherent for a test whose stated purpose is to detect a Lunty map that replicates the minority signature. Either the multiplier needed to drop or the anchor needed to move. Midpoint anchoring was chosen over a multiplier change because (a) it removes the free parameter entirely (no future amendment cycle can be accused of multiplier-tuning), (b) it is self-validating against the two commission maps that already exist — the minority classifies "replicated" (5/5) and the majority "not replicated" (0/5) by construction (verified algebraically and against the canonical run of `run_structural_battery.py` — majority empirical = 0/5), and (c) the Lunty map does not yet exist, so the amendment cannot be reverse-engineered for a specific outcome.

**Why an unamended reading is not feasible.** The 1.5× rule's failure to classify the minority as "replicated" is a definitional incoherence, not a result one could choose to live with. Holding the multiplier would commit the audit to a November verdict surface in which "Lunty replicates the minority structural signature" is unreachable for any map that wasn't significantly worse than the minority on multiple structural dimensions — a question the test was never designed to answer. The verdict surface needed to mean what its prose said.

**Effect on the November verdict.** The 2 × 2 combined verdict surface (structural × partisan) is unchanged. The four pre-committed headline strings are unchanged. The 72-hour publication commitment is unchanged. The substrate, drand-pinning, and reproduction commands are unchanged. The only change is the threshold rule for which candidate maps classify as "replicated" vs "not replicated" on the structural lane. Under the amended rule, the minority commission map itself meets the definition of "structural-lane signature replicated" (it serves as the reference for the signature); under the 1.5× rule, it did not. Honest framing under both rules: the **majority** classifies "not replicated" on canonical geometry; the amended rule simply makes the **minority** also classify as expected.

**Pre-publication verification (run at amendment time, 2026-06-11):**

| Map | S1 | S2 | S3 | S5 | S6 | Discriminating flags | Verdict |
|---|---|---|---|---|---|---:|---|
| Canonical majority | 2826.89 (False) | 23 (False) | 0.80050 (False) | 0.0072 (False) | 0 (False) | **0/5** | not replicated |
| Canonical minority | 3938.11 (True) | 30 (True) | 0.71970 (True) | 0.0006 (True) | 5 (True) | **5/5** | replicated |

(Empirical majority run: confirmed 0/5 by `run_structural_battery.py` against canonical EA shapefiles, this commit. Minority is mathematically guaranteed to be 5/5 by the midpoint construction.)

**Addendum 2026-06-12 (T1.7 Referee #18 follow-up): per-flag specificity rate against the canonical 1.01M-plan ensemble.** Referee #18 flagged that the midpoint thresholds in this Amendment were fitted to the same two maps they are then "validated" against (training set = test set), and that the false-positive rate of the "structural-lane signature replicated" verdict was undefined. The audit owns the 1.01M-plan canonical ensemble; the S1 (population MAD) flag can be scored against every plan directly because the column is in the ensemble CSV.

**S1 (population MAD) specificity:**
- S1 midpoint = 3382.50; flag fires iff plan MAD > midpoint.
- Ensemble plans firing S1: **259,856 / 1,010,000 = 25.728 %**.
- So under the midpoint rule, Pr(S1 flag | neutral plan) ≈ 25.7%, **far above** the ≤ 5% specificity floor a flag should clear to be discriminating. S1 alone is not a 95% specificity test.

S2 (municipal splits), S3 (anchoring percent on CSD boundaries), and S5 (neighbour-drain) require per-plan ED-partition geometry which is not stored in the ensemble CSVs; computing them requires a side run of the ensemble that saves per-plan VA→ED assignments (T1.4-spec, queued). S4 was already excluded as non-discriminating.

**Implication.** The "≥ 3 of 5 flags = replicated" verdict's true false-positive rate cannot be stated until S2/S3/S5 ensemble specificity rates are computed; the verdict surface is currently a *training-fitted threshold without specificity validation*. The S1 rate above (25.7%) suggests that the joint Pr(≥3/5 flags | neutral) could be material under naive independence (the flags are not independent, so the actual rate could be lower or higher). The Lunty test as currently specified is therefore **screening + report**, not "discovery + significance"; the November protocol should report the verdict alongside the per-flag specificity rates and the joint replication rate against the ensemble, not as a binary "replicated / not replicated" headline.

**Signed:** Claude (acting as session agent), reviewed by Will Conner  
**Date:** 2026-06-11; specificity addendum 2026-06-12

---

### Amendment 10 — Declination sign convention correction (2026-06-12)

**What changed.** `analysis/scripts/mcmc_ensemble.py:215` was returning `(2/π)(θ_R − θ_D)` for declination. Warrington (2018) defines δ = `(2/π)(θ_D − θ_R)`, giving positive δ = R-favoured (= UCP-favoured in this audit's convention). The implementation was therefore sign-flipped relative to its own documented convention and to Warrington 2018. The fix swaps the operand order at line 215; the docstring at lines 149–155 already declared the Warrington convention.

**Verification.** A textbook 10-seat UCP gerrymander (NDP packed at 20% UCP in 2 seats; UCP winning 8 seats at 55% UCP) returns:

| Metric | Implementation (old) | Warrington (corrected) |
|---|---:|---:|
| EG | +0.34 (UCP-favoured) | +0.34 (UCP-favoured) |
| δ | −0.716 | +0.716 (matches Warrington's NC-2014 +0.54 magnitude) |

Two independent metrics on the same gerrymander now agree on direction. Under the old sign, δ disagreed by construction — that disagreement was the artefact of the swapped operand, not a real cross-metric divergence.

**Effect on the published findings.** The sign-flip applies uniformly to every plan in the canonical 1.01M-plan ensemble and to every real-map score. The chain CSVs at `data/simulation_checkpoints_canonical/chain*_samples.csv` have been re-saved with the corrected declination column. Real-map values invert:

| Map | Old δ (implementation) | Old percentile | Corrected δ (Warrington) | New percentile |
|---|---:|---:|---:|---:|
| 2019 enacted | −0.0451 | p8.95 | **+0.0451** | **p91.05** (mild UCP-side) — corrected 2026-06-12 per T1.7 R2 Ref #2; round-1 of this entry spliced the canonical real-map JSON value (−0.0451) with the percentile of a different value (−0.034 sits at old-p18.46 / new-p81.54); the canonical real-map JSON store carries −0.04509, which under Warrington flips to +0.0451 at p91.05. Minority/majority rows below verified exact. |
| Majority 2026 | +0.0267 | p79.62 | **−0.0267** | **p20.36** (mild NDP-side) |
| Minority 2026 | −0.0770 | p1.21 | **+0.0770** | **p98.79** (extreme UCP-tail) |

The minority's declination now **agrees with EG, mean-median, and seats@50/50** on the UCP-favoured tail — four-of-four partisan-bias metrics in the same direction, not three-of-four. The §5.2.4 "declination disagrees by design" extended defense (`reports/academic/report_academic.md` lines 898–932) is restated in §5.2.7-correction: there is no cross-metric disagreement to defend. The "narrow-margin-loss packing" reading was correct as far as it described the mechanism, but the sign-flip means the four metrics never actually pointed in different directions on canonical substrate.

**Why this strengthens the headline.** Under the §1.1 BH-table at α = 0.05, row 9 (declination minority) was already PASS — it remains PASS, but the partisan direction is now UCP-favoured (the tail the audit's verdict surface flagged). The audit's primary claim ("the minority is a statistical outlier on all four pre-registered partisan metrics simultaneously") becomes strictly defensible without the asterisk that declination's direction needed an explanatory note. The Mahalanobis joint p (1.40×10⁻⁶) and the Bonferroni dependence-robust upper bound (p ≤ 2.80×10⁻⁶) are unchanged: D² is computed against the ensemble's own (now correctly-signed) covariance matrix, so flipping the sign of one of the four marginals preserves the joint distance — what changes is the *direction* of the minority's offset along the declination axis, not its magnitude.

**Why not a goalpost move.** The sign-flip was discovered by Referee #5 of the T1.7 adversarial review (model fable-5, 2026-06-12, results at `analysis/review/t1_7_18_referee_results_2026_06_12.md`). The referee verified the discrepancy by running a textbook gerrymander through the implementation and against Warrington's NC-2014 published values. The fix is not a choice between two competing readings; it is a correction of a code error against a fixed external definition. The correction direction was determinate before the percentile recomputation.

**Why an unamended reading is not feasible.** Continuing to cite δ values under the wrong sign convention would either (a) misrepresent Warrington 2018 to future readers, or (b) require restating the convention as "negative = UCP-favoured" everywhere — which contradicts every other partisan-bias metric in the audit and the docstring's own statement. Neither is defensible.

**Effect on the November verdict.** The structural-lane signature definition (Amendment 9) is unchanged. The partisan-lane verdict criterion ("≥ 2 of P1–P4 fire in the UCP direction") is unchanged. The pre-committed 2 × 2 verdict surface is unchanged. What changes is the *interpretation* of the minority commission map: under corrected sign, declination is a fourth UCP-favoured-tail signal rather than an explained disagreement.

**Pre-publication verification:** chain CSV column means after sign-flip — chain0 +0.00084, chain1 +0.00437, chain2 +0.00305, chain3 +0.00156 (all small positive; pre-flip means were the same magnitude with opposite signs). Real-map percentiles recomputed against the corrected ensemble at this commit.

**Signed:** Claude (acting as session agent), reviewed by Will Conner  
**Date:** 2026-06-12

---

### Amendment 11 — Spec §1 ↔ §3 alignment (2026-06-12)

**What changed.** `preregistration/november_2026_scoring_spec.md` §1 outcome 1 said the structural-lane replication outcome requires "at least one partisan-bias metric in the UCP direction." §3 of the same document says the partisan-lane verdict criterion is "≥ 2 of P1–P4 in the UCP direction." T1.7 R1 Ref #18 flagged the contradiction; T1.7 R2 verified the fix landed at commit d9c3520. §1 outcome 1 was rewritten to align with §3 ("at least two of P1–P4 in the UCP direction").

**Why not a goalpost move.** The §3 verdict criterion was the binding one (it appears in the verdict-rule table and in the script that scores the test); §1's "at least one" was a documentation error in the prose summary, not a separately committed threshold. Aligning §1 to §3 removes a contradiction; it does not change the test's actual binding rule.

**Why an unamended reading is not feasible.** The Lunty test cannot be operationalized with two contradictory partisan criteria in the same spec; one had to bind. §3's rule is the one the script consumes, and §3's rule was the earlier-committed one (it predates the §1 prose).

**Effect on the November verdict.** None. The script consumes §3; §1 prose is now consistent.

**Spec hash:** the spec's SHA-256 after this amendment was *not* recorded inside §6 of the spec (self-invalidating); it is recorded externally in `preregistration/seed_commitments.md` per Amendment 12.

**Signed:** Claude (acting as session agent), reviewed by Will Conner  
**Date:** 2026-06-12

---

### Amendment 12 — §6 pinning correction; phantom-Amendment-11 entry retired (2026-06-12)

**What changed.** The §6 "drand pinning" paragraph at commit d9c3520 contained four self-inflicted errors flagged by T1.7 R2 (Refs #4 and #18):

1. The SHA-256 fingerprint `34097af2…` was recorded *inside the file being hashed*, then the same file was edited again later in the session (the §1 fix at Amendment 11). The recorded hash matched a stale tree; the current file hashed differently. A self-referential hash can never verify.
2. §6 claimed a `seed_commitments.md` entry "extended at the same commit" — no such entry was ever written (the file was untouched since 2026-05-08).
3. §6 cited the spec's commit chain as `c12c7c8 → 00b0d6c → d562565`. `git log --follow` shows the actual chain is `2cd4b21 → 4781c70 → c12c7c8 → d9c3520`. Commit `00b0d6c` did not touch the spec (it touched only the structural-battery script and TODO); commit `d562565` did not touch the spec either (it touched the report and findings).
4. §6 cited "Amendment 11" as authority for the §1 fix, but no Amendment 11 log entry existed.

**Why not a goalpost move.** Each item is a factual correction of a documentation error, not a substantive change to any pre-registered test definition. The spec's actual binding rules (§3 partisan criterion, §3 structural-lane midpoint thresholds, the §3 ≥3/5 verdict cutoff) are unchanged.

**Why an unamended reading is not feasible.** A self-invalidating hash pin, a fabricated commit chain, and a phantom amendment number are not credible chain-of-custody. The fix is to retire the self-invalidating hash, restate the true commit chain, author the missing Amendment 11 entry, and record the spec's hash *externally* (in `seed_commitments.md`).

**Effect on the November verdict.** None. The verdict rules are unchanged.

**Pre-publication verification:** the spec's SHA-256 at this commit is recorded in `preregistration/seed_commitments.md` under entry `november_2026_scoring_spec`. Verify externally: `sha256sum preregistration/november_2026_scoring_spec.md` against the value in `seed_commitments.md`.

**Signed:** Claude (acting as session agent), reviewed by Will Conner  
**Date:** 2026-06-12

### Amendment 13 — Forest-ReCom Phase A post-registration code changes (2026-07-10)

**What changed after OSF he53s was filed (and before it, that matters).** The
registration (filed public 2026-07-10, pre-execution) cites the binding prereg
document at commit `264afc5b` and the script scaffold at commit `0d0ab8ef`.
Between filing and execution, the following code changes were made and were
NOT recorded in the declaration at the time — they are recorded here now, per
this log's discipline (flagged by the author the same day):

1. **The execution harness was wired.** At the cited scaffold commit, the
   spanning-forest sampler (`_forest_spanning_method`) was fully implemented
   but `main()` deliberately raised `NotImplementedError` behind the OSF gate.
   Post-filing, the per-chain chunked harness was written (chain salts per
   prereg §6.4, burn-in per §6.4, fail-loud partial-chain guard), and
   `mcmc_ensemble.run_ensemble` gained a `proposal_method` parameter (default
   `None` preserves the canonical spanning-tree path byte-for-byte; suite
   30/30 before and after).
2. **A crash was fixed between execution attempts.** Attempt 1 (immediately
   post-filing) crashed with `NameError: '_random' is not defined` at chain-0
   seeding — before any proposal was drawn. One import line was added;
   attempt 2 ran to completion.
3. **The executed code was working-tree state**, committed as `63e5b692`
   immediately after the run, not a pre-committed hash.
4. **Algorithm naming.** Prereg §6.1 names "Aldous-Broder generalised to
   forests" while citing Wilson (1996) and Marchal (2000) — the loop-erased
   random-walk literature. The implementation is multi-root Wilson (LERW).
   Both algorithms sample the identical distribution (uniform spanning
   forests rooted at the chosen root set); the document's own citations point
   at the implemented method. Resolved in the implementation's favour and
   recorded here rather than silently.
5. **ESS-target semantics.** Prereg §6.4 declared an ESS *target* (≥200 per
   metric per chain) without failure semantics. The run missed it (pooled
   n_eff 61–124). The result was reported with the shortfall disclosed in
   `findings/forest_recom_robustness.md`, the OSF execution-log append, and
   the deltas characterised as "indistinguishable from zero at this run
   size." The interpretive choice (report-with-disclosure rather than
   declare-invalid) is itself recorded here as a post-hoc decision.

**Why the chain of custody survives.** No Forest-ReCom sample existed before
the registration was filed (the script's gate verifiably refuses to run
without a registration ID), and none existed before the harness was
finalised — attempt 1 died before drawing a single proposal. There was
therefore no opportunity for data-dependent tuning of the harness, the
sampler, or the decision rule: the first Forest-ReCom samples ever drawn are
the reported ones. What was compromised was not the epistemics but the
*documentation contemporaneity* — the code changed after the declaration
froze, and the record of that belongs in the declaration's amendment trail,
not in a session transcript.

**Why not a goalpost move.** The hypotheses, the ±5 pp decision rule, the run
size, the chain design, the seeds, and the output paths were all executed
exactly as registered. The changes were: making the registered design run at
all (1–3), resolving a naming ambiguity internal to the document (4), and
choosing disclosure semantics the document failed to specify (5).

**Effect on the Phase A verdict.** None. All four metrics remain Robust under
the pre-registered rule; the ESS caveat already accompanies the result in
every venue.

**Signed:** Claude (acting as session agent), flagged by Will Conner
**Date:** 2026-07-10

### Amendment 14 — Publication-path consolidation: one HTML rendering (2026-07-11)

**What changed.** The repo carried two parallel HTML renderings of the
reports: the viewer site (SvelteKit → `docs/`) and standalone
markdown-to-HTML pages produced by `analysis/scripts/build_html_reports.py`
(`docs/report_public.html`, `docs/report_academic.html`), plus a hand-kept
`docs/FINDINGS_BRIEF.html`. The standalone pages drifted from the canonical
markdown (the deployed `report_public.html` still served the pre-casings
structure; the T1.7 referee had previously caught the same file serving
pre-Amendment-10 values). By author direction ("there only needs to be one
html path"), the script and all three standalone HTML artifacts are removed.
The public and academic reports are published as markdown (canonical, in
`reports/`); the viewer site is the sole HTML rendering.

**Why this touches a registered procedure.** The November scoring spec
(`preregistration/november_2026_scoring_spec.md`, §7 step 5) lists
`python analysis/scripts/build_html_reports.py` in the publication command
sequence. That spec's SHA-256 is committed in
`preregistration/seed_commitments.md`, so the file itself is not edited.
This entry supersedes that one command: the November publication step is now
`cd viewer && npm run build` plus the markdown commit. **No test, threshold,
metric, verdict rule, or deadline changes.** The 72-hour commitment and all
scoring machinery are untouched; this is publication mechanics only.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-07-11

### Amendment 15 — Canonical ensemble scrapped and rerun after a second defect (2026-07-12)

**What changed.** The canonical 1,010,000-plan ReCom ensemble was discarded and
regenerated from scratch. Context: the chain-1 silent-resume duplication
disclosed 2026-07-09 (DOCUMENTED CORRECTIONS C9, `findings/ensemble_chain1_duplication_note.md`)
was retained on the reasoning that its measured sensitivity was negligible.
While hardening the resume path against that defect, a second, independent
defect was found in the same script (`mcmc_ensemble_canonical.py`): the
multi-chain checkpoint writer indexed output files by loop position rather
than by the `--first-chain-idx`-adjusted chain number, risking a silent
clobber of one chain's samples by another's on a partial or resumed run. On
finding a second uninvestigated failure mode in the same generation code, the
judgment was to rerun clean rather than add a second sensitivity footnote.

**What did not change.** The base seed derivation (drand-committed, unchanged),
the ReCom parameters (population deviation ±25%, 4 chains × 252,500 steps),
and the scoring methodology (Mahalanobis joint-tail, Bonferroni dependence-robust
bound) are all identical to the run this replaces. This is a re-execution of
the same pre-registered procedure, not a methodology, threshold, or metric
change. **No test, threshold, metric, or verdict rule changes.**

**Why this touches a registered procedure.** The canonical ensemble is the
substrate for the audit's headline statistical finding (Ch1, OSF-anchored per
the drand-committed seed; see §4.3.3 of the academic report). Rerunning it
changes the reported p-values and D² figures even though the procedure itself
is unchanged — this amendment exists to log that the numeric shift comes from
discarding a defective execution, not from adjusting the test. The resulting
figures are disclosed in DOCUMENTED CORRECTIONS **C10**
(`reports/academic/report_academic.md`), which supersedes C9's retention
disposition; full detail in `findings/ensemble_chain1_duplication_note.md`.
This entry does not touch `preregistration/november_2026_scoring_spec.md` —
the November confirmatory run (OSF qsgy8) is a separate, not-yet-executed
procedure on the final enacted map, unaffected by this rerun of the current
canonical maps' ensemble.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-07-12

### Amendment 16 — Scoring rule for test X1 (Recommendation 5) (2026-10-29)

> **Status: in force.** Drafted 2026-10-29 14:32 MDT and signed 2026-10-29 15:09 MDT, before
> the committee's map is due (November 2, 2026) and before any committee map
> has been published.

**What changes.** Test X1 ("Chair Miller's four conditions", academic report
§5.5; `findings/checklist_baseline_scoring.md` §X1) gets a written scoring rule.
It never had one: X1 does not appear in `preregistration/november_2026_scoring_spec.md`
(v1.2), and its two descriptions overstate Recommendation 5.

1. **Conditions (a), (b) and (c)** are scored met / not met against the majority
   map: (a) no change to any division in Airdrie or with territory south of
   Airdrie's southern boundary, except Drumheller-Stettler (41 majority
   divisions); (b) no change to any Edmonton division north of the North
   Saskatchewan River (11); (c) Edmonton divisions south of the river match the
   commission's October 2025 interim map (10), with the stated Nisku option.
   District sets: `viewer/static/mapdata/lunty_bounds.json`, built by
   `analysis/scripts/build_lunty_bounds.py`.
2. **Condition (d)** ("consider restoring" a Clearwater County and western
   Mountain View County division with s. 15(2) status) is scored in three
   states: **adopted** (the map contains a division mostly of those areas,
   with s. 15(2) status or within ±25%); **considered with a stated reason**
   (the committee or panel report names the option and gives a reason tied to
   the Act's factors); **not shown** (silence, or boilerplate such as "all
   recommendations were considered").
3. **X1 is met** only if (a), (b) and (c) are met and (d) is adopted or
   considered with a stated reason.
4. **Reported beside it, not gating it:** the strict reading of (d) (restored
   or not), and the "rest of the province as we propose … to the extent
   possible" clause as a number — the share of the 27 majority divisions
   outside (a)–(c) that come back unchanged.

**Why this is not a goalpost move.** It is written before the map exists, and
it narrows nothing the audit has scored: X1 has never been executed against any
map. It replaces wording that misstated the source ("restore" for "consider
restoring"; "no impact south of Airdrie", which drops Airdrie itself; "R5 binds
the November committee", when R5 binds no one and Government Motion 37 lets the
panel modify it) with the source's own words. The three-state rule for (d)
follows how Canadian law tests a duty to consider — through the reasons given
(*Baker v. Canada*, 1999, para. 75; *Canada v. Vavilov*, 2019 SCC 65, para. 128;
both confirmed via secondary sources only) — and applies the same way whatever
the map does.

**Why leaving it unamended is not workable.** As written, X1 would either fail a
committee that weighed the Clearwater option and declined it for stated
reasons — scoring a recommendation the chair worded as "consider" as if it
said "restore" — or, read loosely, pass any map whose authors say they
considered it, which no public record could falsify.

**Open dependency.** Condition (c) cannot be scored without the October 2025
interim map, which is not in this repository.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-29 15:09 MDT

---

### Amendment 17 — Size-matched neutral maps and three added November tests (2026-10-29)

> **Status: in force.** Drafted and signed 2026-10-29 18:20 MDT, before the
> committee's map is due (November 2, 2026) and before any committee map has
> been published. Written after public reporting on the advisory panel's draft
> and before that draft was released; the tests below apply the same way to
> whatever the published map contains.

**What changes.** The November scoring (`preregistration/november_2026_scoring_spec.md`
v1.2, Amendment 16) gains a size-matched comparison, a written rule for X1
conditions (a) and (b), and three tests. Nothing registered earlier is
removed or loosened, and the spec's verdict table is unchanged: the three new
tests are reported as separate registered results beside it.

1. **Size-matched neutral maps (co-reported).** The canonical 1,010,000-plan
   ensemble starts every chain from the 2019 map (`initial_assignment_2019`),
   so every plan has 87 districts. The registered comparison against it stands
   as the headline. Beside it, the November map is scored against neutral maps
   with the same number of districts as the map (91 if the map has 91),
   generated by `analysis/scripts/close_seats_ensemble.py` (mode `nk`), which
   runs the canonical harness `analysis/scripts/mcmc_ensemble.py` unchanged
   (same ReCom proposal, ±25% statutory constraint, half-band epsilon, 2023
   election-day VA substrate). Each chain is seeded the way the harness seeds
   its own fallback, by `recursive_tree_part` at epsilon 0.25, with chain seed
   (base_seed × 100,000 + idx × 1,000) mod 2³², base_seed =
   `get_canonical_seed("mcmc_ensemble_250k")`, chain indices 200 and up. Every
   plan completed when scoring begins is used; the plan count and effective
   sample size are reported. If fewer than 20,000 plans are complete, the
   size-matched results are marked provisional and re-run at 100,000.
2. **X1 conditions (a) and (b), scored.** A majority division named in (a) or
   (b) (`viewer/static/mapdata/lunty_bounds.json`) is **unchanged** when one
   district of the new map holds at least 99% of its 2021 population and that
   district's population is at least 99% from the majority division.
   Population is the VA-level 2021 census overlay the ensemble uses
   (`data/va_pop_from_das.csv`), attributed by VA representative point. (a) or
   (b) is met only if every division it names is unchanged. If the October
   2025 interim map is not available when scoring begins, (c) is reported as
   not scored, and X1 is reported as not met if (a) or (b) fails, and as not
   determinable otherwise.
3. **Towns split beyond their minimum.** For every city and town (Statistics
   Canada 2021 CSD types CY and T) of 20,000 to 150,000 people (VA-level 2021
   population), pieces = districts holding at least 2% of its population. A
   town is flagged when pieces > ceil(population ÷ (1.25 × average district
   population)). The statistic is the number of flagged towns, flagged at or
   above the 95th percentile of the size-matched neutral maps; each flagged
   town is listed. Baselines: majority map 0; minority map 6 (Airdrie 3/2,
   Chestermere 2/1, Lethbridge 4/2, Okotoks 2/1, Red Deer 4/2, St. Albert 3/2).
   This extends the registered Drain Pattern (Amendment 4, change 4) from four
   cities to every city and town in the range.
4. **City versus rest, by population.** A district is a Calgary or Edmonton
   district when at least 50% of its population lives in that city. The
   statistic is (mean population of those districts − mean of the rest) ÷ mean
   of the rest, in percent, flagged at or above the 95th percentile of the
   size-matched neutral maps. Baselines (2021 census, VA level): majority
   −0.7%; minority +5.4%.
5. **Competitive seats.** The number of districts whose UCP–NDP two-party gap
   on the 2023 election-day votes is within 4 points, flagged at or below the
   5th percentile of the size-matched neutral maps (fewer close seats than 95%
   of them). Baselines: majority 13 (8 UCP-held, 5 NDP-held); minority 4 (4, 0);
   2019 map 10 (8, 2).

Baselines are from `close_seats_ensemble.py real` at this amendment's commit.
The 89-district runs for the two commission maps are exploratory and are not
part of this amendment.

**Why this is not a goalpost move.** Every rule is fixed before the map is
published, applies to any map, and adds tests without removing or relaxing
one. The size-matched comparison corrects a mismatch the headline comparison
has, without replacing the headline.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-29 18:20 MDT

---

### Amendment 18 — Errata in registered documents (2026-10-29)

> **Status: in force.** Signed 2026-10-29 18:30 MDT. Corrects citations, labels
> and stale status lines. No test, threshold, rule or registered value changes.

Each item was found by the swarm audit (`analysis/review/swarm_audit_2026-10-29.md`)
and checked against its primary source before editing.

- `preregistration/thresholds.md`: the ±25% band is cited as EBCA § 15(1), not
  § 14 (§ 14 is the factors clause; the Act's text is in
  `preregistration/terms_of_reference.md`). Option C (#41) is shown as complete
  (it finished 2026-05-12), so the count is 41 real thresholds, not 40. The
  s.15(2) area note now says the official shapefiles arrived 2026-05-06 and the
  area figures are still taken from the commission's text. The Option D row
  and paragraph give the values after the July 12 rerun (minority p94.54,
  majority p16.52, median +1.63%, n_eff 1,413–1,522). The row and the
  paragraph now mark +4.10% as the registered threshold and give the rerun
  ensemble's 95th percentile, +4.08%, beside it. The threshold does not move.
- `preregistration/retraction_conditions.md`: the commission's rules are in the
  Electoral Boundaries Commission Act, not the Electoral Divisions Act; an
  uncited § 16 is dropped; Government Motion 37 replaces "Motion 19".
- `preregistration/seed_commitments.md`: the canonical ensemble is 1,010,000
  plans, not 100k.
- `preregistration/README.md`: `seed_issue14.md` is the Issue #14 counter-map
  seed (OSF submission pending), not the canonical ensemble's.
- This log: the committee's name and the header's amendment list and table.

**Left as registered:** `preregistration/november_2026_scoring_spec.md` calls the
committee the "Special Select Committee". The file is pinned by SHA-256
(`seed_commitments.md`, current pin `2110548c…`), so the inverted name stays.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-29 18:30 MDT

---

### Amendment 19 — Errata: a withdrawn timing claim in thresholds.md (2026-10-29)

> **Status: in force.** Signed 2026-10-29 18:55 MDT. No test, threshold, rule or
> registered value changes.

`preregistration/thresholds.md` Scenario E1 said the P1 threshold "predates
detection by 2 hours 24 minutes (git timestamps)". The academic report's
pre-registration disclosure withdrew that claim on 2026-04-23: the criteria were
committed in the same commit as the detection run (`282bc6d`). Scenario E1 now
says so. Found by the third check of the swarm audit's fixes.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-29 18:55 MDT

---

### Amendment 20 — Three further neutral-map sets, harness fixes, and the town-split framing (2026-10-29)

> **Status: in force.** Signed 2026-10-29 20:14 MDT, before the committee's map is
> due (November 2, 2026) and before any committee map has been published. The
> author's ruling: the neutral maps should be "as strict as the statute, no more,
> no less". The author confirmed in this session that the registered comparison
> stays the headline and that all three sets below are registered.

**Headline unchanged.** The scoring spec's 87-district canonical comparison stays
the headline, and Amendment 17's size-matched half-band comparison is reported
beside it as before. The three sets below are reported beside those, each
labelled, and none replaces a registered comparison.

**1. Statute-band set.** Same harness as Amendment 17's size-matched chains, but
with the ReCom proposal balance set to the statute's band: epsilon =
pop_deviation = 0.25 (EBCA s.15(1), ±25%). Chain indices 230–239 (91 districts)
and 130–139 (89 districts). The June full-band run (`findings/eps_full_robustness.md`)
moved partisan percentiles by under 0.05 pp but roughly doubled neutral
population spread; population-based measures (MAD, the city-versus-rest gap,
towns split) are therefore read against a wider neutral baseline in this set,
and are labelled so.

**2. Municipality-aware set ("a commission weighing s.14(b)").** Statute band, plus
gerrychain 0.3.2's region-aware ReCom with a soft `region_surcharge` of 1.0 on
the 2021 census subdivision (CSDUID). The weight is fixed here and will not be
tuned after results are seen. No hard rule. Chain indices 240–249 and 140–149.
A sensitivity reading, not a test.

**3. s.15(2) set.** Statute band, plus the s.15(2) exception: up to four divisions
may be as much as 50% below the average where at least three of the five
criteria exist. The Commission's "opinion" is modelled as "the criteria are
met". Criteria: (a) area over 20,000 km² (from VA areas; the surveyed-area limb
is not available); (b) more than 150 km from the Legislature Building to the
nearest boundary by the most direct highway route (approximated from
`data/osm/alberta_osm_highways.gpkg`); (c) no town over 8,000 people (2021 CSD
population); (d) an Indian reserve (CSD types IRI, S-É) or a Metis settlement:
reserves only until the author approves a Metis settlement source, which makes
(d) stricter than the statute; (e) part of the boundary coterminous with the
provincial boundary. Chain indices 250–259 and 150–159. A specification fixing
the split rule and each criterion's computation will be committed before the
committee's map is published; if the set runs after the map, its results remain
pre-registered.

**4. Harness fixes (distribution-preserving).** In `close_seats_ensemble.py` (mode
`nk` only): ReCom pairs whose merged population lies outside 2 × ideal × (1 ±
epsilon) are rejected at once instead of after 100,000 failed spanning-tree
attempts (such pairs have no balanced cut, so the transition distribution is
unchanged; the sample path is not); each chunk is checkpointed (assignment and
both RNG states) and resumes byte-identically; each chunk starts from a
Partition rebuilt from the assignment. In `mcmc_ensemble.py`, the unreachable
s.15(2) branch of the population constraint now matches the statute (below the
average only, at most 50%, area over 20,000 km², at most four districts); output
is unchanged. Chains 201 (91 districts) and 100 (89 districts) ran before these
fixes; chains 220–225 and 120–121 and later run with them. Both sets are valid
draws from the same distribution under different code versions, and are
reported as such. The exact code lands in git before scoring, with its commit
recorded in this log.

**5. Town-split framing.** Amendment 17's town-split test compares a map with
neutral maps that do not try to keep municipalities whole. A flag means "splits
more towns than a population-only neutral map", not "more than the law asks of
a commission". Set 2 gives the comparison against maps that do weigh
municipalities.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-29 20:14 MDT

---

### Amendment 21 — The s.15(2) specification, corrections to Amendment 17, and the municipality-aware weight (2026-10-29)

> **Status: in force.** Drafted 2026-10-29 20:45 MDT and signed 2026-10-29 21:45 MDT,
> before the committee's map is due (November 2, 2026) and before any committee
> map has been published. No s.15(2) chain has run. Two municipality-aware
> chains (241, 243) started at W = 0.5 about 20:50 MDT, on the author's ruling in
> item 3, before this was signed; none of their output has been examined. The author's direction: "we want to make sure we're being faithful
> as possible to the legislation and the norm, we're not chasing goalposts."

Each rule below follows the statute's words where they can be computed. Where
they can't, the rule says which way the approximation errs. The s.15(2) rules
were checked against what Alberta's commissions did, not against any result.

**1. The s.15(2) set (Amendment 20, item 3), specified.** The criteria are
computed by `analysis/scripts/s15_2_criteria.py` from one per-VA table, the same
for neutral maps and real maps. The statute's text is in
`preregistration/terms_of_reference.md` §3d–3e.

- **(a) Area.** The sum of the district's VA areas in an equal-area projection
  (Canada Albers, ESRI:102001), met above 20,000 km². No province-wide source for
  "total surveyed area" is available, so the 15,000 km² limb is treated as not
  met. That errs strict, and only for a district of 15,000–20,000 km² whose
  surveyed area exceeds 15,000 km².
- **(b) Distance.** The shortest route on the OSM highway layer
  (`data/osm/alberta_osm_highways.gpkg`: motorway, trunk, primary and secondary
  roads) from the node nearest the Legislature Building (53.5336° N,
  113.5068° W) to the nearest node within 1 km of the district, met above
  150 km. A district no highway reaches meets (b). Leaving out local roads can
  only lengthen a route, so (b) errs lenient by that much.
- **(c) Town.** The Act does not define "town". Read as a legal status alone, (c)
  would credit a district holding a city with having no town over 8,000, the
  opposite of what the criterion marks. On the real maps that reading makes
  Calgary-Glenmore-Tsuut'ina (majority), Calgary-West-Tsuut'ina (minority) and
  the Medicine Hat districts eligible to sit 50% under quota; no Alberta
  commission has used s.15(2) for a district holding a city. Statutes are read
  for their purpose and to avoid absurd results (*Rizzo & Rizzo Shoes Ltd.
  (Re)*, [1998] 1 SCR 27, paras. 21 and 27; confirmed via secondary sources
  only). So a town here is a city or town
  (2021 CSD types CY and T), or the urban service area of a specialized
  municipality: its 2021 dissemination areas at 400 or more people per km²,
  Statistics Canada's density rule for a population centre. Crowsnest Pass is
  excluded under s.15(3). The author chose this reading in this session
  (2026-10-29, about 21:40 MDT), replacing the status-only reading approved
  earlier that evening for the s.15(2) build
  (`governance/GOVERNANCE-s15-2-chain-model.md`). Two urban
  service areas pass 8,000: Strathcona County's (Sherwood Park, 68,784) and Wood
  Buffalo's (Fort McMurray, 58,964). Populations are 2021 census counts
  (`data/reference/alberta_2021_csd_populations.csv`,
  `alberta_2021_da_populations.csv`). A district contains a town when it holds
  at least 2% of the town's population, Amendment 17's piece rule; (c) is met
  when it contains no town over 8,000.
- **(d) Reserve or settlement.** Indian reserves are the legal reserve
  boundaries in Natural Resources Canada's "Aboriginal Lands of Canada
  Legislative Boundaries" (Canada Lands Survey System; retrieved 2026-10-30
  02:39 UTC; 152 Indian reserves in Alberta; SHA-256 `f87795a1…b8d0`). The 2021
  census layer has only 83 reserve CSDs, because it can leave out uninhabited
  reserves, and the statute does not ask whether anyone lives there. Its three
  "Indian settlement" CSDs are not used: Statistics Canada defines an Indian
  settlement as lacking reserve status. Metis settlements are the Government of
  Alberta's "Metis Settlement" layer (Provincial Geospatial Centre; retrieved
  2026-10-30 02:12 UTC; 10 polygons, all 8 settlements; SHA-256
  `5e7c1270…c1e5`). Both sit under `data/shapefiles/reference/` with a
  SOURCE.md. A district contains one when it holds at least 10% of its area,
  which keeps boundary slivers out.
- **(e) Provincial boundary.** Met when the district's VAs share at least 1 km
  of edge with the provincial outline (VA edge within 100 m of the exterior of
  the 2021 CSD union). Lake shores inside the province do not count.

*Split rule.* ReCom accepts a cut when both new districts hold between 50% and
125% of the average district population. A plan is valid when every district
is within ±25% of the average, except that up to four districts may hold 50% to
75% of it if each meets at least three of (a)–(e). The Commission's "opinion" is
modelled as the criteria being met (Amendment 20). A neutral map takes the
exception only when a random cut lands there; nothing pushes it there. Reported
beside each result: the share of plans with 0 to 4 such districts, and where
they fall. Chain indices 250–259 (91 districts) and 150–159 (89), seeded as in
Amendment 17.

*Checked against the commissions.* The script, run on the 2026 maps, gives
(full output: `data/outputs/s15_2_real_maps.json`; per-VA table:
`data/outputs/s15_2_va_criteria.csv`):

| District | Map | Re-audit count (from the commission's text) | Computed |
|---|---|---|---|
| Central Peace-Notley | majority | 5 | 5 (a b c d e) |
| Lesser Slave Lake | majority | 4 (not e) | 3 (a c d) |
| Canmore-Banff | majority | 3 (b d e) | 3 (b d e) |
| Central Peace-Notley | minority | 5 | 5 |
| Lesser Slave Lake | minority | 4 (not e) | 3 (a c d) |
| Rocky Mountain House-Banff Park | minority | 5 | 5 |

Re-audit counts: `analysis/methodology/population_deviation_reaudit.md`. On the
2019 map, Central Peace-Notley computes 5 and Lesser Slave Lake 4.

Every district a commission placed under s.15(2) qualifies. The one
disagreement is Lesser Slave Lake's (b) in the 2026 maps. Its south-east edge,
a VA from the 2019 Athabasca-Barrhead-Westlock division, lies 134 km from the
Legislature by highway and 113 km in a straight line, so the literal "nearest
boundary" test fails; the commission counted (b) as met (report p. 248). The
literal reading stands. It is the statute's wording, and it changes no
designation: the district still qualifies on (a), (c) and (d). A second
implementation, built separately on the author's machine, found the same
134 km.

**2. Corrections to Amendment 17.**

- **(a) The provisional rule counts effective draws, not plans.** Amendment 17
  marks size-matched results provisional below 20,000 plans. Successive plans
  are strongly correlated, so plans are the wrong unit. On the two completed
  chains (91 districts, chain 201; 89 districts, chain 100), the first 20,000
  plans hold 57 and 99 effective draws for close seats, and 16 and 9 for the
  city-versus-rest gap: too few to place a 95th percentile. The replacement: a
  result is final when its measure's effective sample size, summed over chains
  by the estimator the canonical ensemble reports (Geyer initial positive
  sequence, `simulation_multichain_ensemble.autocorrelation_ess`), is at least
  400 and the estimator's lag cap did not bind. Otherwise it is reported as
  provisional with its n_eff, and re-scored as chains complete. At 400 effective
  draws a map's percentile near the 95th is known to about ±2 points. This is
  stricter than the rule it replaces.
- **(b) X1 (a) and (b) get a strict reading beside them.** The 99%/99% rule
  stays. A median VA holds 862 people, 1.8% of a 91-district average, so a
  moved VA usually fails it. A VA under 1% of a division (about 470 people) can
  move unseen, and a tenth of VAs hold 408 people or fewer. So the strict
  reading (100%/100%) is reported beside each result, with the population moved
  for any division that passes at 99% and not at 100%. It does not gate.
- **(c) Town splits: Sherwood Park and Fort McMurray.** The registered test
  counts CSD types CY and T. That leaves out two urban centres of about 60,000
  to 70,000 people, because each sits inside a specialized municipality. The
  running chains record only CY and T, so the registered statistic stays as
  it is. For the November map, the splits of both urban service areas (as
  defined in item 1(c)) are reported beside it against the 2019, majority and
  minority maps, with no neutral-map percentile.
- **(d) City versus rest gets two labels.** First, it runs on 2021 census
  population for the map and the neutral maps alike, which keeps the comparison
  consistent but departs from the commission's own tables. The majority map
  reads −0.7% here and +9.2% on the commission's populations with districts
  classed by name; the minority reads +5.4% and +15.9%. Population source and
  classification both differ, and the two have not been separated. Second, as
  with town splits (Amendment 20, item 5), a flag means "a larger city–rest
  gap than population-only neutral maps", not "beyond what the law allows".
  s.14(a) lets a commission weigh sparsity, and the 2019 and majority maps'
  values, reported beside it, show what commissions that did so produced.
- **Unchanged:** competitive seats, the town-split rule itself, and X1's (c)
  and (d).

**3. The municipality-aware weight (Amendment 20, item 2).** Amendment 20 fixed
the weight W at 1.0 and promised not to tune it. Calibration runs on the
author's machine, made before any production chain, show what that weight
means. R is the share of 2021 CSDs (169: Calgary and Edmonton excluded, at least
two VAs each) split into more pieces than their population requires, by
Amendment 17's piece and need rules (`Geo.csd_split_ratio`). On the real maps,
R is 0.166 for the 2019 enacted map (28 of 169), 0.112 for the majority (19) and
0.249 for the minority (42). On neutral maps with 91 districts and the statute
band, W = 0 gives 0.388, W = 0.5 gives 0.168 and W = 1.0 gives 0.065 (mean of
the second half of 6,000- or 10,000-step runs).

At W = 1.0 the neutral maps split municipalities at 40% of the enacted map's
rate and well below either commission map. That models a commission stricter
about municipalities than any Alberta commission has been. It is not the norm.

The replacement is W = 0.5, anchored to the 2019 enacted map: the map in force,
and not one under test. Its R of 0.166 falls at W ≈ 0.51 with 91 districts and
W ≈ 0.54 with 89, both within one chain's noise of 0.5. The author first asked
for the mean of all three maps (0.176), which also gives W ≈ 0.5, but the anchor
leaves both 2026 maps out. The minority map is under test and splits the most
municipalities, so it would pull its own benchmark toward itself. And under
Recommendation 5 the November map keeps 52 majority divisions unchanged, so
anchoring to the majority would pull the benchmark toward the map being scored.
The author chose this anchor in this session, 2026-10-29. Production indices:
241, 243, 244 and 245 (91 districts) and 140 and 141 (89); 240 and 242 failed
to seed, and a further failure takes the next free index in the block.

W was tuned against R only. No test statistic from the set had been computed,
per the session that ran the calibration. W is now fixed, and the set stays a
sensitivity reading, not a test.

**4. Code.** The chains run commit `01095181` (branch `amendment17-local-runs`):
the harness patch that Amendment 20, item 4, describes (patch SHA-256
`84f85728…3a35`), plus a Windows power setting that changes speed, not
results. It merges into master with this amendment, together with
`s15_2_criteria.py` and the run log
(`analysis/methodology/amendment17_chain_runs/README.md`).
`tests/test_scoring.py`: 16 passed. A 1,500-step regression of chain 221 gives
identical rows on Linux and on the author's Windows machine (content digest
`66e00fa2…67cf`). The s.15(2) chain code (split rule and constraint) lands
before that set runs, and its commit will be recorded here.

**Why this is not a goalpost move.** Everything here is fixed before the
committee's map exists, before any s.15(2) chain has run, and before any
municipality-aware output has been examined.
Item 1 writes down rules Amendment 20 promised, and tests them against the
commissions' own designations rather than against any result. Item 2 tightens
one rule and adds labels and reported readings; no registered test, threshold
or baseline is loosened. Item 3 is the one place a registered value changes. It
is a sensitivity set's weight, and it moves to match the enacted map on a
structural measure, with the maps under test kept out of the anchor.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-29 21:45 MDT

---

### Amendment 22 — Errata (2026-10-30)

> **Status: in force.** Signed 2026-10-30 03:23 MDT. Corrects the district count
> of the canonical neutral plans in thresholds.md. No test, threshold, rule or
> registered value changes.

`preregistration/thresholds.md` §B.2.1.D (Option D, Threshold #42), under
"Residual vulnerability", said the ensemble imposes a uniform ±25% band "on all
89 EDs". Every one of the 1,010,000 canonical plans has 87 districts, the 2019
map's count (the `n_districts` column of
`data/simulation_checkpoints_canonical/chain{0..3}_samples.csv`), and the band
applies around a quota of 2021 population / 87. The sentence now reads "on all
87 districts of each neutral plan (quota = 2021 population / 87)". The
89-district official shapefiles only score the two commission maps. Found by the
monograph audit (`analysis/review/monograph_audit_2026-10-30.md`, MC-A3) and
applied on the author's approval, given in session on 2026-10-30 ("Go", in reply
to the audit's list of decisions). The academic report records
the same correction as DOCUMENTED CORRECTIONS C18.

The threshold stays at the registered +4.10%. The rest of the sentence, on the
s.15(2) districts the ensemble cannot reach, is unchanged.

**Also noted, not changed:** Amendment 17, item 1, says the canonical ensemble
"starts every chain from the 2019 map (`initial_assignment_2019`)". On 2021
population the 2019 map has 7 of its 87 districts outside ±25%, so the harness
reseeds every chain with an 87-part `recursive_tree_part` partition, and the
2019 map supplies only the district count (academic report C20). Amendment 17's
rules are unaffected: its size-matched chains are seeded that way too, as it
states.

**Left as is:** the same paragraph still describes the ensemble as run "on
official Elections Alberta shapefiles". The plans partition the 4,765 voting
areas, and the shapefiles score the commission maps. Decision A3 covered only
the district count.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-30 03:23 MDT

---

### Amendment 23 — Erratum: s.15(2)(b) measured to the boundary itself (2026-10-30)

> **Status: in force.** Signed 2026-10-30 04:20 MDT, before the committee's map is
> due (November 2, 2026), before any committee map has been published, and before
> any outcome of the s.15(2) set has been examined. The author chose this fix in
> session ("Erratum + rerun").

**What was wrong.** Amendment 21, item 1(b), measured the highway distance from
the Legislature Building to "the nearest node within 1 km of the district". A
highway node within 1 km can sit on a road that runs beside the district without
entering it, so the route could stop short of the boundary. Amendment 21 said
(b) errs lenient; on this point it erred strict. The independent cross-check on
the author's machine found it, in a diff of the two criteria tables (2019
Bonnyville-Cold Lake-St. Paul).

**The rule now.** The shortest route on the same OSM highway layer, from the node
nearest the Legislature Building to the nearest point where a highway reaches
the district's boundary, or to a highway node inside the district; met above
150 km. Each VA records its nearest highway crossing or inside node, and a
district takes the minimum over its VAs, which is the first point a shortest
route reaches inside the district. A district no highway reaches meets (b), as
before. Leaving out local roads still errs lenient.

**Effect.** Per VA, the new distance is longer than the old by 1.1 km at the
median and 3.2 km at the 90th percentile, and up to 62 km. In a few VAs it is
shorter, by up to 3.3 km. 236 VAs move from 150 km or less to over 150 km, and
one moves the other way. On the real maps, no 2026 district and no district a
commission placed under s.15(2) changes; the Amendment 21 check stands,
including Lesser Slave Lake at 134.0 km. Two 2019 districts change on (b):
Bonnyville-Cold Lake-St. Paul goes from 148.0 to 153.1 km (now met), and Fort
McMurray-Lac La Biche from 151.9 to 149.4 km (now not met). Neither was
designated, and each still meets three criteria. Criteria (a), (c), (d) and (e)
are unchanged.

**The s.15(2) set.** The chains already run on the Amendment 21 table are
superseded. Their output stays on file, labelled superseded. Only validation
counts were taken from them (special districts per plan and constraint checks),
and no outcome statistic from them will be reported. The set is rerun on the
corrected table, with the same chain indices and seeds: 251–254 (91 districts)
and 150–151 (89), seeded as in Amendment 17. Index 250 is retired because it
does not seed. Table: `data/outputs/s15_2_va_criteria.csv`, SHA-256
`48c928b8716f6ed218065e01a912ecabd11518917ac9e312376e4d603ee2fafc`, built by
`analysis/scripts/s15_2_criteria.py` at this amendment's commit.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-30 04:20 MDT

---

### Amendment 24 — Set D is the primary size-matched comparison (2026-10-31)

> **Status: in force.** Signed 2026-10-31 00:00 MDT, before the committee's map is
> due (November 2, 2026) and before any committee map has been published. The
> author's direction: "I want the most defensible set"; set D proposed, and the
> author confirmed it in the session on the author's machine ("yes"). The
> disclosure below was corrected 2026-10-31 01:12 MDT, before publication, on the
> author's statement that the results had not been seen.

**What changes.** Amendment 20 put Amendment 17's half-band set (set A) beside the
headline and the three further sets beside those. From this amendment, set D
(s.15(2), the Amendment 23 rule; Amendment 20 set 3) is the primary size-matched
comparison, and sets A, B and C are reported beside it, each labelled; C remains
a sensitivity reading. The scoring spec's 87-district canonical comparison stays
the headline. Every set is reported in one table for every measure, whatever it
shows. No test, threshold or flag rule changes.

**Why set D.** The author's standing rule for the neutral maps is "as strict as
the statute, no more, no less" (Amendment 20). Set A draws its maps with a ±12.5%
proposal band, stricter than the Act's ±25% (s.15(1)). Set B uses the Act's band
but allows no division below −25%, which s.15(2) permits for up to four. Set C
adds a weight chosen by the audit (Amendment 21). Set D is the only set whose
maps may do what the Act allows.

**What set D does not do.** Its criteria are approximations, and they do not all
err the same way (Amendments 21 and 23): (a) errs strict (the surveyed-area limb
is not computed); (b) errs lenient (local roads are left out, which can only
lengthen a route); (c) counts cities as towns, a reading chosen in Amendment 21.

**Disclosure: what existed before this choice.** Amendment 17's flags for the two
commission maps against the 89-district sets had been computed and committed
before this choice (commit `2ecd7931`, 2026-10-30 19:10 MDT;
`findings/size_matched_results_2026-10-30.md`, provisional). The author did not
look at them before choosing. They are:

| Map | Measure | A | B | C | D |
|---|---|---|---|---|---|
| Minority | Competitive seats | p0.2 flag | p0.2 flag | p0.1 flag | p0.3 flag |
| Minority | City versus rest | p99.9 flag | p93.0 | p87.8 | p71.7 |
| Minority | Towns split | p33.3 | p45.0 | p100.0 flag | p47.5 |
| Majority | all three | no flag | no flag | no flag | no flag |

Choosing D over A removes the minority map's city-versus-rest flag from the
primary comparison; it is still reported, under set A. The committee's map has
not been published, so this choice is made without knowledge of its results.
The only prior information about the panel's draft was a meme posted on Facebook
around the committee's October 28 meeting, the item Amendment 17 calls public
reporting. It is archived, with a transcription, at
`preregistration/evidence/2026-10-29_facebook_meme_panel_draft.md` (uploaded
2026-10-29 17:52 MDT, before Amendment 17 was signed). Its claims about Lethbridge,
Okotoks and the Calgary and Edmonton ridings are what Amendment 17's town-split and
city-versus-rest tests address. No panel or committee map, and no result from
either, had been seen.

The four sets are four readings of what a neutral map is, and all four stay in
the report as competing readings, each labelled. D is primary because it alone
follows the Act, the rule the author set in Amendment 20, not because of what it
shows. Against the commission maps the choice cuts against the audit's earlier
findings: it removes one flag on the minority map and adds none.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-10-31 00:00 MDT
