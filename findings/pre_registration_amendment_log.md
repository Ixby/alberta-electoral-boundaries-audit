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

**Registration:** Pre-registered signature-detection checklist for the Alberta MLA Special Select Committee's electoral boundary map.  
**Author:** Will Conner.  
**Original upload:** 2026-04-23, 06:22 PM MT (OSF Registrations).  
**Amendments filed:** 2026-04-23 · 2026-04-26 (morning) · 2026-04-26 (evening) · 2026-04-27.

---

## Table of amendments

| Date | File | Trigger | Key changes |
|---|---|---|---|
| 2026-04-23 | Amendment 1 | Six corrections after initial upload | Urban-weight parameter corrections (C1–C4); AI toolstack disclosure (C5); DPG sunset clause (C6) |
| 2026-04-26 AM | Amendment 2 | Methodology evolution since 04-23 | MCMC enlargement 100k→2M (C1); short-bursts test (C2); rural analysis (C3); 89-of-89 attribution (C4); v0_7→v0_8 (C5); five test-result revisions (C6–C11) |
| 2026-04-26 PM | Amendment 3 | Gemini code audit — 9 pipeline bugs, 3 critical | Bug-fix remediation record; interim claim revision; 2M ensemble rescinded in postscript |
| 2026-04-27 | Amendment 4 | Final hardening | 250k ensemble locked; v0_9 topology; headline s50=48.31%@p98.5; drand seed pre-committed |

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
| 2019 enacted | −0.034 | p8.95 | **+0.034** | **p81.54** (mild UCP-side) |
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
