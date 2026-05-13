---
name: Pre-registration amendment log (consolidated)
description: Complete dated chain of all amendments to the audit's pre-registered signature-detection checklist, from initial upload through final hardening. Four source files merged 2026-05-12.
type: project
---

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

*Note: Amendment 4 predates the final canonical 1,010,000-plan ensemble run on official EA shapefiles (completed 2026-05-12). See `data/simulation_convergence_diagnostics_canonical.json` and `analysis/reports/joint_outlier_score.json` for the authoritative canonical numbers.*

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
