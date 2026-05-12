# Alberta Audit — Outstanding Tasks

**Project:** Electoral Boundary Analysis, Phase 1 (minority map)
**Last updated:** 2026-05-12
**Completed work:** see `COMPLETED_LOG.md`

---

# M2 — PUBLICATION

Items must complete before either report goes public.

---

## CRITICAL — Citation Verification

- **VERIFY — Seidle resolved, Small pending** The original Seidle (1991) *Rethinking Government* citation was wrong (finance volume, not commission structure) and was removed in ES-29. Search confirmed Seidle has no RCERF volume on boundary commissions — his volumes are 4 (*Comparative Issues in Party and Election Finance*) and 5 (*Issues in Party and Election Finance in Canada*), both on finance. The correct RCERF boundary-reform volume is: **Small, D. (ed.) (1991). *Drawing the Map: Equality and Efficacy of the Vote in Canadian Electoral Boundary Reform*. Research Studies, Vol. 11, Royal Commission on Electoral Reform and Party Financing. Dundurn Press.** §5.9.3 already has Courtney (2001) covering the commission model; Small adds a primary RCERF-layer citation. **Action required:** read Small (1991) Vol. 11 and add citation to §5.9.3 body and References when content is verified. Low-risk to publish without it — does not block publication.

---

## CRITICAL — Deferred Statistical Extensions

- **FUTURE-01** Two-tier MCMC population constraint — EBCA §15(2) permits up to −50% deviation for qualifying EDs. Deferred to post-review. **Decision 2026-05-11:** leave the registered ensemble (OSF qsgy8) untouched for the audit; the idea may appear as a thought-exercise or Section 14 discussion item. A proper implementation would require a separate pre-registered robustness ensemble with new drand seed and would need to solve the seeder-feasibility issue documented at `mcmc_ensemble.py` lines 463–481.
- **FUTURE-02** Neighbour-Drain extension — graph diffusion operator. Current test measures directed pairs; intended mechanism is multi-target cascading (graph diffusion problem). Standalone methods paper contribution if pursued. See audit discussion section (Ch3 internalization hypothesis).

---

## HIGH — Computational Blockers

### OSF s58a6 — Section C: MCMC Rerun for Pending Channels

- **Status: PARTIALLY DONE** — base_seed = 3562959107 (drand round 6099592); registered OSF s58a6 2026-05-10
- **Channels:** population MAD ratio, Reock asymmetry, municipal anchoring departure
- **Protocol:** 2 chains × 50,000 plans with per-plan MAD, Reock, and anchor-count capture
- **Decision rule:** each channel reported regardless of direction; any p<0.05 added to updated Fisher combination
- **MAD — DONE and independently confirmed:** Canonical 1M: minority p99.0, majority p15.8. Section C independent seed (3562959107, 100k): minority p99.26, majority p16.58. ✓ Values match within sampling variation. §5.4.9 updated with independent-verification note.
- **Reock — DONE and independently confirmed (null finding):** Both maps at p100 median compactness under both canonical and Section C seeds. No out-of-distribution signal in either run. Reported as null in §5.4.9. ✓
- **Municipal anchoring — STILL PENDING:** Per-plan anchor-count not implemented in `mcmc_ensemble_canonical.py`. Section C executed without this channel. Requires separate implementation before this channel can be reported.

### Option C threshold ensembles — write-up on completion

- **Runs:** `run_id threshold_2019` / `threshold_2015` (seed 3562959107, 2 chains × 50k plans each, VA files `va_polygons_with_2019_votes.gpkg` / `va_polygons_with_2015_votes.gpkg`)
- **When complete:** extract p95 EG from each run's percentiles CSV; update §5.2.8 Option C table row and reading paragraph; update threshold_provenance.md B.2.1.C with computed values
- **Write-up rule (pre-committed 2026-05-12, commit 257cfc2):**
  - Report all three p95 values (2015, 2019, 2023 = 4.10%) in a table
  - Option D (4.10%, 2023 context) remains the primary Alberta-calibrated threshold regardless of what the 2015/2019 runs return
  - If either run's p95 < 4.02% (minority map canonical EG), report that as-is — do not use it to change the primary verdict or select a lower threshold
  - Frame as jurisdiction-normed range (floor, ceiling, centre), not as a stability test

---

### Phase 4C Vision Assignment (Stages 3–7)

Stage 3 superseded by official shapefiles. Still needed for vote aggregation.

- **Stage 3 SUPERSEDED** — Replace Vision API calls with spatial join of VA centroids against `ea_minority_2026_eds.gpkg` / `ea_majority_2026_eds.gpkg`. Effort: 2 hours.
- **Stage 4:** Aggregate spatial join output to CSV per 2026 ED.
- **Stage 5:** Group VA votes by 2026 ED; aggregate totals. C1 complete — unblocked.
- **Stage 6:** Execute `packing_cracking_analysis.py` on Stage 5 data.
- **Stage 7:** Run `monte_carlo_ci.py` on Stage 5 output.

### External Tool Validation

- **Phase 1 (highest priority):** R `redist` package cross-validation — independently reproduce seats@50/50. Effort: 1 evening + ~90 min runtime.
- **Phase 2:** QGIS visual inspection using official shapefiles. Effort: 1 h setup + 1 afternoon.
- **Phase 2.5:** Maptitude free-trial cross-validation. Effort: 4 h setup + 2 h QA.

---

## HIGH — Sentiment Analysis

- **Intensity scoring COMPLETE** (452 deduped rows, haiku model, 2026-05-10): §5.9.4.6 weighted-net table updated.
- **Remaining forensic pipeline:** `quote_verify_and_clean.py` → `validation_sample.py` → human review → `compute_kappa.py` → `cross_reference_submitters.py`
- **Cross-reference:** Final results against `minority_rationales_validation.md` Proposals A–F
- **Refactor:** Update `submission_sentiment_llm_full.py` to import from `analysis/utils/`

---

## HIGH — Pre-Publication Outreach

### Pre-Brief Academics (do before public release)

Outreach sent to Elections Alberta and Duane Bratt on 2026-04-23; replies received 2026-05-09.

1. **Send draft to Bratt** — DONE 2026-05-11.
2. **Send spatial methodology sections to Lan Nguyen + Lynn Moorman** (MRU GIS/geography). — **DRAFT READY 2026-05-13** at `private_workspace/emails/06_nguyen_moorman_spatial_review_2026-05-13.md`. Four specific questions: (a) Alberta 3TM vs east–west distortion; (b) VA centroid boundary attribution; (c) Reock via shapely.minimum_bounding_circle(); (d) 500m CSD-edge buffer tolerance. Pre-send checklist in draft.
3. **One additional academic reviewer** (political science, outside MRU) — **TWO DRAFTED 2026-05-13:**
   - **Peter Loewen (U of T, Munk School)** — Canadian institutional framing (§5.9, §1 commission discretion framing, Saskatchewan Reference). Draft: `private_workspace/emails/07_peter_loewen_uoft_2026-05-13.md`
   - **Jowei Chen (U Michigan)** — MCMC methodology (ReCom §15(2) constraint, R-hat thresholds, Mahalanobis novelty, Fisher independence). Draft: `private_workspace/emails/08_jowei_chen_umich_2026-05-13.md`
   - Recommended send order: Loewen and Nguyen/Moorman simultaneously; Chen after Loewen replies (strengthens credibility signal).
4. Response turnaround: allow 2–3 weeks before final revision pass.

### URL Archival

- 13 priority URLs need Wayback Machine + archive.ph submission (authenticated browser session required)
- 6 additional SPN2 POST submissions needed
- After submission: update `FROZEN_MANIFEST.md` and `private_workspace/url_archival_log.md`

### Editorial Factual Ambiguity

- Airdrie population framing (74,100 vs 84,000) — author clarification required. Recommendation: use 84,000 (2024 estimate) throughout. See also CLR-04.

---

## HIGH — Red-Team Code Corrections

Five HIGH findings deferred (from `red_team_code_fixes.md` §5):

- **HIGH-03** Magic-number bounding boxes — deferred
- **HIGH-05** Mixed RNG sources — documentation fix only; deferred
- **HIGH-06** 2015 region classification heuristic — deferred
- **HIGH-08** Chrome `--no-sandbox` hardening — deferred
- **HIGH-11** Suppressed-DA uncertainty accumulation — deferred

Numeric drift 0.05–0.09 pp on sensitivity endpoints from prior rounding corrections — headline numbers unchanged but prose must match.

---

## MEDIUM — Pending Analysis

### Open GitHub Challenges (Issues #13 and #14)

- **MCMC-13 — 2019-seeded ensemble** (GitHub Issue #13): Seed ReCom chain from 2019 enacted geometry; single-boundary moves; population-target-preserving swaps. Effort: 2–3 days + ~90 min compute.
- **COUNTER-14 — Counter-map challenge** (GitHub Issue #14): Retraction condition for §5.8.5 anchoring finding. Produce constraint-legal 89-seat map satisfying minority's stated COI rationales AND achieving majority-comparable municipal-boundary anchoring (CSD/DA edge alignment ≥60%). Status: no counter-map submitted as of 2026-05-10.
- **338-RETRO — Historical polling sensitivity** (Track E extension): Use 77 historical 338Canada snapshots to reallocate both 2026 maps across the full polling range. Find crossover pp level where minority-vs-majority seat direction flips. Effort: 2–3 hours adapting `338canada_reallocate.py`.

### Data Source Gaps (minority_rationales_validation.md Proposals A–F)

**StatsCan Journey-to-Work (98-10-0459 series):**
- Already downloaded: Cochrane CSD origin table
- Missing: Airdrie, Chestermere, Sylvan Lake, Innisfail, Red Deer origin-CSD tables
- Impact: R2/R5/R11 verdicts currently INCONCLUSIVE

### Manual Source Verifications

- ~~RMH-Banff attribution — verify against Hansard/X-thread sources before CRIT-B deletion~~ **DONE 2026-05-09** (see COMPLETED_LOG.md)
- Public-support refutation scope — 3 items need manual cross-check

---

## MEDIUM — Dissemination

### SSRN / OSF Preprint (before journal submission)

1. Finalize report_academic.md — version stamp it
2. Post PDF to SSRN (Canadian Social Science category) and OSF Preprints under the existing OSF node
3. Announce to institutional reviewers (Bratt/Nguyen/Moorman) with preprint link
4. Journal submission after preprint is live and at least one reviewer has read draft

**Target journals (in order):** *Canadian Public Policy*, *Electoral Studies*, *Political Science Research and Methods*

### Media Prep Kit

1. **1-page non-technical summary** — no p-values, no EG; use seat-gap and wasted-vote framings
2. **Visual asset package** — 3–5 key figures export-ready (300 dpi PNG); existing SVGs in `data/maps/mcmc/` are candidates
3. **FAQ document** — 10 questions a journalist or MLA would ask; pre-drafted answers; include "what this study does NOT claim"
4. **Contact list** — Bratt + 2 others willing to field media calls; confirmation required before release

### Globe and Mail Data Desk Pitch

- Target: Globe and Mail data-journalism desk
- Angle: Alberta's proposed boundary change and what a statistical audit found
- Pitch format: 3-sentence summary + link to preprint + offer of embargoed early access
- Timing: send after preprint is live and BEFORE journal peer-review outcome
- Note: pitch to CBC Alberta as fallback

### Indigenous Dimension — Expanded Section

Current §5.8.4 notes Enoch Cree Nation (Reserve 135) PP=0.065 and Tsuut'ina comparison. Needs expansion:

1. **s.35 Constitutional Act, 1982 framing** — boundary decisions affecting reserve lands engage consultation obligations
2. **UNDRIP (Bill C-15, 2021) framing** — Article 18 free, prior, and informed consent
3. **Tsuut'ina comparison** — Tsuut'ina Nation (Reserve 145) absorbed into Calgary-West in majority proposal; different treatment from Enoch Cree; document the asymmetry in commission's stated rationale
4. Effort: 1–2 h for s.35/UNDRIP paragraphs; Tsuut'ina comparison partially in §5.8.4

---

## MEDIUM — Restructure / Hygiene

### analysis/ Directory Restructure

Three-phase execution (PO-approved 2026-04-23). Awaiting execution trigger from PO.

- **Phase A (2–3 h):** 12 zero-reference files — move to correct directories; validate imports
- **Phase B (6–8 h):** ~45 files with 1–2 references — move in batches; grep-replace cross-references after each
- **Phase C (8–10 h):** 15 high-risk files with 3+ references
- **Phase D (2–3 h):** Verification — ast.parse all moved .py; grep for stale paths

### Remediation Hygiene Track (Phases 3–5)

Deferred after Safety Track completion:

- Constants module, ED name resolver, god function decomposition
- `sys.path` removal, `data_loader` abstraction, `mcmc_runner` consolidation
- `ruff` config + `mypy`, `iterrows` migration, TypedDict types

### Post-Publication Refactor — "one function, one paragraph"

**Trigger:** after both reports ship. Do NOT attempt mid-audit.

Collapse `analysis/scripts/` from ~87 files into ~15–20 topic modules. Inputs to start: `analysis/methodology/scripts_inventory.md`. The 27 scripts named directly in `report_academic.md` form the irreducible citation surface — new module functions must preserve those names via thin shims.

---

# M3 — LUNTY RELEASE (Nov 2, 2026)

**Moved to `private_workspace/M3_LUNTY_RELEASE.md`.** Re-merge into this file only after the Lunty committee tables its 91-seat map.

---

# Date-Gated External Events

| Track | Event | Trigger |
|---|---|---|
| A (shapefile integration) | Unblocked 2026-05-06 (commit 873f4d0); C1 complete | Phase 4C Stages 3–7 still pending |
| B (November 2026) | Lunty committee tables 91-seat map (Nov 2, 2026) | Run full Phase 2 checklist within 48h |
| E (338Canada refresh) | Next due ~late June 2026 | Re-run scraper if projection moves >0.5pp |

---

# External Blockers

- **OSF pre-registration disclosure gap** — Ch1 (Mahalanobis) and Ch2 (SZAT) are not named in any of the four pre-registered files (w2s8k/r3zm7/qsgy8/6pt83). Registrations cover drain test (Ch3) and DPG v11 methodology only. Paper must disclose this gap in §3.7. Timing record: drand beacon committed 2026-04-27; official EA shapefiles received 09:51 AM 2026-05-06 (9 days after beacon); SZAT results committed 18:11 2026-05-06; OSF SZAT registration (6pt83) written 21:16 (~3 h later); Ch1 ensemble committed 21:51 after `osf_register.py` created at 20:14.
- **November 2026 committee deadline** — drives Phase 2 publication target.

---

# Planning Docs — Flagged for Deletion

After confirming nothing was missed, delete:

| File | Reason |
| --- | --- |
| `analysis/methodology/master_plan.md` | All open D/S/G/C items now in COMPLETED_LOG.md |
| `analysis/methodology/assignment_runbook.md` | Stage 3–7 procedure in Phase 4C section above |
| `analysis/methodology/assignment_execution_log.md` | Stage status in Phase 4C section above |
| `analysis/methodology/external_tool_validation_plan.md` | All three phases in External Validation section above |
| `analysis/red_team/archival_submission_queue.md` | URL archival task in HIGH section above |
| `analysis/methodology/restructure_inventory.md` | Phase A–D tasks in Restructure section above |
| `analysis/methodology/editorial_pass_log.md` | Completed log; no outstanding items |

**Do NOT delete (content, not plans):**

- `analysis/red_team/red_team_assertions.md` — assertion inventory; keep until referee response
- `analysis/red_team/red_team_code_fixes.md` — deferred HIGH/MEDIUM rationale; keep until fixes complete
- `analysis/methodology/minority_rationales_validation.md` — scientific findings
- `analysis/meta/FROZEN_MANIFEST.md` — canonical file manifest
- All methodology, findings, and defense documents

---

# PO Clarification Required

Items surfaced during the 2026-05-12 grounding sweep. Do not publish until resolved.

| ID | File | Claim | Issue | Status |
|---|---|---|---|---|
| **CLR-01** | `README.md` §Direction-of-travel | "2019 enacted: D²=12.12, p=0.020" | Old DPG-era value. | **RESOLVED 2026-05-12** — updated to D²=12.75, p=0.013 (1M covariance) in README.md, academic report §5.4.10, and joint_outlier_score.json. |
| **CLR-02** | `README.md` §Dependency graph | "48 of 74 findings … leaves 26" | Could not verify without running query. | **RESOLVED 2026-05-12** — verified by running `dependency_query.py --invalidate L0:data.2023_statement_of_vote`; confirmed 48/74 orphaned, 26 robust. |
| **CLR-03** | `README.md` §A2, structural cost table | "11.5% above provincial mean" (minority NE/central Calgary zone), "2.8% above average" (majority) | Zone label incorrect ("northwest" vs "northeast/central"). | **RESOLVED 2026-05-12** — verified against `section_A_population_equality.md`; label corrected to NE/central; values confirmed (minority 61,225 = 11.5%, majority 56,460 = 2.8%). |
| **CLR-04** | `README.md`, academic report | Airdrie ~84,000 residents | 74,100 (2021 Census) vs 84,000 (2024 municipal census). | **RESOLVED 2026-05-13** — corrected to 85,805 (City of Airdrie 2024 municipal census, released July 2, 2024; https://www.airdrie.ca/index.cfm?serviceID=2242&ID=1248) across 8 locations in README.md, academic report, and public report. Citation added to References §Data sources. |
| **CLR-05** | `analysis/reports/joint_outlier_score.json` | Anchoring values 14.5% / 71.0% in `structural_pending` | DPG-era values, retracted finding. | **RESOLVED 2026-05-12** — updated to 72% / 80% with RETRACTED status label. |
| **CLR-06** | `analysis/reports/joint_outlier_score.json` | `caveats: "Ensemble is 100k plans"` | D² and Fisher p from 100k covariance. | **RESOLVED 2026-05-12** — recomputed from 1M covariance: minority D²=32.67 (p=1.40e-06), majority D²=7.85 (p=0.097), enacted D²=12.75 (p=0.013); Fisher p=6.87e-08 (T=39.03). |
| **CLR-07** | `REPRODUCING.md` | Gemini commit hashes `73544a3` and `972b04a` | Commit attribution may be inaccurate. | **RESOLVED 2026-05-12** — hash references removed; Gemini description updated to reflect SZAT/scorecard collaboration. |
