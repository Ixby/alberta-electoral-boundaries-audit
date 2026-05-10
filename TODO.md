# Alberta Audit — Outstanding Tasks

**Project:** Electoral Boundary Analysis, Phase 1 (minority map)
**Last updated:** 2026-05-10 (new session — ISR relaunched bg02j9iz7 after context expiry; 459 rows remaining)
**Single source of truth for all outstanding work. Planning docs flagged for deletion at bottom.**

---

# M1 — MONDAY 2026-05-12 (Group Chat Review)

Group chat review Monday. These items require no new research — all are prose corrections or short insertions against existing analysis.

## Do before Monday (~4–5 hrs total)

| # | Item | What | Status |
|---|------|------|--------|
| ES-24 | Abstract word-count cut | Trim to 150–250 words; move technical detail to §1 | **DONE 2026-05-10** |
| ES-25 | "US judicial threshold" replace | → "Stephanopoulos-McGhee 7% investigable-bias threshold" at Abstract + §8 + all instances | **DONE 2026-05-10** |
| ES-22 | §5.2.2 deterministic vs MC distinction | Add sentence distinguishing point-estimate table from Monte Carlo sensitivity interval | **DONE 2026-05-10** |
| ES-26 | Declination formula, Appendix D.3 | Added formal definition D.3; PP→D.4, Reock→D.5 | **DONE 2026-05-10** |
| ES-03 | Alberta 2017 seat-count fix | Audited report_academic.md — no "2017 expanded" claim found; stale §2 cross-ref (Quebec 1992/1996/BC 2008) corrected | **DONE 2026-05-10** |
| ES-01 | *Rizzo* case-name fix | Already correct throughout; verified | **DONE (pre-existing)** |
| ES-34 | Abstract dimension labels | Pattern not found in current Abstract — already fixed in prior session | **DONE (pre-existing)** |
| ES-09 | Drop "67th percentile" | Removed from §5.2.1; defensible rank statement kept | **DONE 2026-05-10** |
| ES-31 | Unused references | Added Sancton (2008) body citation at §1.1 municipal anchoring bullet; no Smith (2010) found anywhere | **DONE 2026-05-10** |

## Do if time (~3–4 hrs total, medium difficulty)

| # | Item | What | Status |
|---|------|------|--------|
| ES-05 | Abstract contingency clause | Covered in new Abstract: "EG direction reverses under 2019 votes (see §5.2.3)" | **DONE 2026-05-10** |
| ES-08 | E2 both-readings paragraph | Show RMH-Banff under original + substantive E2; label reformulation explicitly | **DONE 2026-05-10** |
| ES-02 | Comparator trio rewrite §5.9.3 | §5.9.3 already anchored to Quebec 2011 + SCC April 2026; stale §2 pointer fixed | **DONE 2026-05-10** |
| ES-17 | Institutional context paragraph | Added institutional context paragraph at top of §2 | **DONE 2026-05-10** |

## Defer to post-Monday revision (do not attempt this weekend)

- ES-07: Bayesian-screening §4.x subsection (MCMC multi-chain, BH correction)
- ES-14: Canadian literature engagement (Pal, Wesley, Courtney pin-cites — 3–4 h)
- ES-16: Saskatchewan Reference depth (1.5 h)
- ES-10: *Grant v. Torstar* defamation posture (2 h)
- ~~C1: Advance-vote splat computation~~ **DONE 2026-05-10** (C5 Vote Anywhere exclusion applied; substrate 1,544,139 two-party; NDP share 44.66%; see Computational Blockers)
- ~~S2-02: MCMC full-coverage rescore headline update~~ **DONE 2026-05-10** (Gate G2)

---

# M2 — PUBLICATION

Items must complete before either report goes public. Ordered: blockers first, then peer review, then outreach/dissemination.

---

## CRITICAL — Submission Gate

All five conditions must be met before submission. Currently: **5/5 clear** (all gates done 2026-05-10).

| Gate | Condition | Status |
|---|---|---|
| G1 | Fisher independence check: \|ρ\| < 0.30 | **DONE 2026-05-10** (ρ = −0.0014, p = 0.8884; SZAT p updated 0.0044 → 0.0024; Fisher 2ch p = 8.71e-9) |
| G2 | S2-02 MCMC rescore: canonical 250k values from `simulated_ensemble_percentiles_canonical.csv` propagated to §5.4.9, §5.5, §6.2.1, §6.2.2 — key change: minority EG p94.2 (below p95, flag retracted); majority MM p0.85 (new NDP-tail finding) | **DONE 2026-05-10** |
| G3 | BH correction table inserted at §4.3.1: 11 formal tests, 10/11 pass BH at α=0.05; sole failure is Minority EG (p94.2, already retracted) | **DONE 2026-05-10** |
| G4 | Direction disagreement framing in §5.4/§6: EG+MM+seats (minority more UCP) vs declination (minority least UCP) vs 338 April 2026 (minority +1 NDP seat) reconciled explicitly | **DONE 2026-05-10** |
| G5 | Pre-registration timing disclosure fixed in §5.3.1 and `preregistration_salt_audit_trail.md` | **DONE 2026-05-10** |

---

## CRITICAL — Report Accuracy (from red_team_assertions.md)

- **CRIT-A DONE 2026-05-09** Sensitivity table re-run complete. New values (w=0.85 central): majority −0.40%, minority −1.81%, asymmetry −1.41 pp. Range 0.47–1.48 pp (0.70–0.80 bracket). B4 direction reversed: minority now matches 2019 at 46 NDP seats@50/50 vs majority 45. Updated: report_academic.md §§5.2.1/5.2.2/5.2.7/5.2.8/summary table, README.md, report_public.md, assignment_gerrymander_comparison.md, maup_area_weighted_analysis.md, threshold_provenance.md §B.2.1, urban_weight_defense.md, chen_rodden_decomposition.md.
- **CRIT-B DONE 2026-05-09** RMH-Banff "+0.7 seat" and "minority wins RMH-Banff in 50% of samples" text not found in either `report_academic.md` or `report_public.md` — already removed in a prior session. No action required.
- **CRIT-C DONE 2026-05-09** Public report intro corrected.
- **HIGH-A** 2019 cross-election asymmetry values — based on 2015–2019; 2023 data now available. Recompute using 2015–2019–2023; update Appendix A table.
- **HIGH-B** Monte Carlo median drift — median values shift ~0.3 pp between runs; documented internally but not disclosed. Add footnote to Section B/Appendix A explaining variance source; use min/max range instead of point estimates.
- **HIGH-C** Submission count reconciliation — Chair's "no public support" claim vs D-section findings inconsistency. Reconcile counts between `submission_search_findings.md` and Section D narrative; ensure both cite same baseline.
- **HIGH-D DONE 2026-05-09** Wesley commission attribution resolved.
- **HIGH-E DONE 2026-05-09** Nenshi quote fixed.
- **MED-A** Plurality of Albertans claim — needs cross-check. Run `claim_significance_analysis.py`; verify "plurality" (>50%) vs "majority" language threshold.

---

## CRITICAL — Design and Statistical Fixes (from master_plan.md)

- **D1 DONE 2026-05-09** Third-party vote sensitivity run complete. Rule A/B/C results documented.
- **D2 DONE 2026-05-09** Sensitivity interval relabeling complete.
- **D3 DONE 2026-05-09** Cross-election flip mechanical explanation added.
- **D4 DONE 2026-05-09** Neutral-ensemble benchmark caveat added.
- **D5 DONE 2026-05-09** "Six of seven" language downgraded.
- **S1 DONE 2026-05-09** B4 uniform swing footnote added.
- **S2 DONE 2026-05-09** Bonferroni note added below §5.2.1 table.
- **S3 DONE 2026-05-09** §1.2 preamble rewritten.
- **S4 MINOR** Small-N noise floor not disclosed — SE of EG in 89-district system is ~1–2pp; the -1.42pp asymmetry is near the lower bound of reliable detection. Add to MC CI section. Effort: 20 minutes.

### Statistical Corrections — Status

- **S2-01 DONE 2026-05-10** MCMC ESS precision disclosure — canonical 4-chain R-hat table inserted in §5.4 (GR92 + Vehtari 2021 side-by-side); worst-chain ESS 63–94 reported; EG/declination marginal V21 failure disclosed with Ch1 headroom note. OSF s58a6 Section B. Output: `data/outputs/rhat_diagnostic_section_b.json`.
- **S2-02 DONE 2026-05-10 (Gate G2)** — 250k canonical values propagated to §5.4.9, §5.5, §6.2.1, §6.2.2. Minority EG retracted (p94.2); majority MM p0.85 NDP-tail documented with mechanism explanation.
- **S9-01 DONE 2026-05-10** p100 language recalibration — BH footnote (§4.3.1) updated: row 3 retracted, ESS caveat + full-coverage rescore note added. Partisan Bias prose (§5.6): "100th percentile" → "above 99.9% of the ensemble (ESS-adjusted lower bound: at least p95)". Table cells in §5.4 governed by existing ESS-downgrade paragraph — no change.
- **S2-03 DONE 2026-05-10 (Gate G3)** — BH correction table at §4.3.1: 11 tests, 10/11 pass, sole failure Minority EG (already retracted).
- **S2-04 DONE 2026-05-10 (Gate G4)** — Direction disagreement three-layer reconciliation paragraph inserted in §6.
- **FUTURE-01** Two-tier MCMC population constraint — EBCA §15(2) permits up to −50% deviation for qualifying EDs. Deferred to post-review.

---

## CRITICAL — Pre-Registration Timing Disclosure (Gate G5) — **DONE 2026-05-10**

`preregistration_salt_audit_trail.md` corrected: SZAT OSF form (6pt83) filed ~3 hours after szat.py first ran; provenance rests on drand seed committed 2026-04-27, not OSF form. Timeline table added. See `analysis/methodology/preregistration_salt_audit_trail.md` for full record.

---

## CRITICAL — Peer Review (PRE-REVIEW PRIORITY)

Complete before Bratt/Nguyen/Moorman institutional review: ES-02, ES-13, ES-14, ES-17, ES-19 — in that order.

#### CRITICAL (synthesis items 1–6)

- **S1-01 FIXED 2026-05-09** Pre-registration provenance — three edits made.
- **ES-01 DONE (pre-existing)** *Rizzo* case-name — verified correct throughout.
- **ES-02 DONE 2026-05-10** Comparator-trio rewrite §5.9.3 — Quebec 2011 + SCC April 2026 substituted; stale §2 pointer fixed.
- **ES-03 DONE 2026-05-10** Alberta 2017 seat-count — no "2017 expanded" claim found; stale §2 cross-ref corrected.
- **ES-04** (=S2-01/S2-02/S9-01) MCMC percentile demotion — S2-01 DONE 2026-05-10; S2-02 DONE; S9-01 outstanding.
- **ES-05 DONE 2026-05-10** Abstract contingency clause — "EG direction reverses under 2019 votes (see §5.2.3)" added.
- **ES-06 DONE 2026-05-10** Exploratory-vs-confirmatory foregrounding — *Evidentiary status* paragraph added to Abstract; bold "Exploratory vs. confirmatory status" paragraph added to §1 after opening paragraph.

#### HIGH (synthesis items 7–16)

- **ES-07 HIGH** Multiple-comparisons §4.x subsection — add §4.4 paragraph on Bayesian-screening battery and Bonferroni threshold. Effort: 2–3 h. (S2-03 BH table now done; prose subsection still needed.)
- **ES-08 DONE 2026-05-10** E2 both-readings paragraph — RMH-Banff under original + substantive E2 added to §5.3.3.
- **ES-09 DONE 2026-05-10** "67th/71st percentile" demoted — removed from §5.2.1; defensible rank statement kept.
- **ES-10 HIGH** *Grant v. Torstar* + defamation posture — add Appendix F subsection. Effort: 2 h.
- **ES-11 DONE 2026-05-10** Intent-imputation verb softening — "got it wrong" → "do not survive primary-source verification against Alberta Education school-division boundaries" (§5.8 school coherence); "elides this distinction" → "does not carry this distinction" (§5.9.2 R5 provenance). Third instance ("materially misrepresents" → "materially overstates the absence of public support") was already applied in a prior session at §5.9.4.
- **ES-12 HIGH** "Override" vocabulary rewrite §5.9. Effort: 30 min.
- **ES-13 DONE 2026-05-10** VA-polygon vote-coverage §5.4 wiring — paragraph already present at §5.4 line "(ES-13)"; SZAT cross-reference sentence updated to reflect definitive SZAT run uses full-VA substrate (post-C1 2026-05-10).
- **ES-14 HIGH** Canadian literature engagement — Pal, Pal & Choudhry, Courtney pin-cites, Wesley, Seidle into §2 and §5.9.3. Effort: 3–4 h.
- **ES-15 HIGH** *Rucho v. Common Cause* engagement. Effort: 1 h.
- **ES-16 HIGH** Saskatchewan Reference constitutional-standard depth. Effort: 1.5 h.

#### MED (synthesis items 17–27)

- **ES-17 DONE 2026-05-10** Institutional context paragraph — added at top of §2.
- **ES-18 MED** Alberta 2022 federal sub-commission comparator. Effort: 1.5 h.
- **ES-19 MED** Alberta volatility paragraph — Bratt et al. 2019; weight structural findings over partisan-bias findings. Effort: 1 h.
- **ES-20 MED** *Raîche* and *Cassista* to body. Effort: 1 h.
- **ES-21 MED** *Haig v. Canada* ghost reference — cite or remove. Effort: 15 min.
- **ES-22 DONE 2026-05-10** §5.2.2 deterministic vs MC distinction — sentence added distinguishing point-estimate table from MC sensitivity interval.
- **ES-23 MED** Contribution positioning (d). Effort: 1 h.
- **ES-24 DONE 2026-05-10** Abstract word-count cut — trimmed to 150–250 words; technical detail moved to §1.
- **ES-25 DONE 2026-05-10** "US judicial threshold" replaced with "Stephanopoulos-McGhee 7% investigable-bias threshold" throughout.
- **ES-26 DONE 2026-05-10** Declination formula in Appendix D.3 — formal definition added; PP→D.4, Reock→D.5.
- **ES-27 DONE 2026-05-10** Per-metric ESS in §5.4 — worst-chain ESS 63–94 reported in canonical R-hat table (OSF s58a6 Section B); full GR92+Vehtari paragraph in §5.4.

#### LOW (synthesis items 28–36)

- **ES-28 LOW** §E.7 v4-residual-gap collapse. Effort: 30 min.
- **ES-29 LOW** Citation-format cleanup batch. Effort: 1.5 h.
- **ES-30 LOW** Pincite and terminology pass. Effort: 1 h.
- **ES-31 DONE 2026-05-10** Unused references — Sancton (2008) body citation added; no Smith (2010) found.
- **ES-32 LOW** Statistical-presentation clarifications batch. Effort: 1.5 h.
- **ES-33 LOW** Alberta Treasury Board 2024 estimate context. Effort: 20 min.
- **ES-34 DONE (pre-existing)** Abstract dimension labels — pattern not found; already fixed in prior session.
- **ES-35 LOW** Abstract L9 assertiveness. Effort: 15 min.
- **ES-36 LOW** §5.9.5 "implicate" → "be evaluated against". Effort: 10 min.

---

## HIGH — Computational Blockers

### Advance-vote splat (C1 — highest computational priority)

- **C1 DONE 2026-05-10** Advance-vote splat — output at `data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg`; two-party total 1,544,139 (post-C5); NDP share 44.66% (+2.07 pp from ED-only 42.60%); 4,765 VAs; conservation PASS (delta = 0).
- **C5 DONE 2026-05-10** Vote Anywhere exclusion — 87 rows excluded (NDP 87,767 / UCP 74,398 / Other 3,768); filtered inline in `advance_vote_splat.py` before splat weights built.
- **DOC-ACCURACY DONE 2026-05-10** Post-C1 stale-figure sweep — corrected 44.17% → 44.66% and 45.56% → 44.66% (NDP post-splat share) and 1,706,304 → 1,544,139 (substrate two-party total) across: `report_academic.md` §5.2 SZAT disclosure, `shapefile_redteam_report.md` §Known Limitations, `fisher_combination_defense.md` footer, `assignment_gerrymander_comparison.md` §Election-Day bias. Added pre-C5 disclosure note to `advance_vote_sensitivity.md`. `sign_convention_resolution.md` and `section_4_geometry_provenance.md` 45.56% references verified correct (official election total, not substrate).

### OSF s58a6 — Section C: MCMC Rerun for Pending Channels

- **Status: PENDING** — base_seed = 3562959107 (drand round 6099592); registered OSF s58a6 2026-05-10
- **Channels:** population MAD ratio, Reock asymmetry, municipal anchoring departure (all require per-plan outputs not in existing ensemble)
- **Protocol:** 2 chains × 50,000 plans with per-plan MAD, Reock, and anchor-count capture
- **Decision rule:** each channel reported regardless of direction; any p<0.05 added to updated Fisher combination

### Fisher Empirical Independence Check (Gate G1)

- **Script:** `analysis/scripts/szat.py` then `analysis/scripts/validate_fisher_independence.py`
- **Status:** DONE 2026-05-10 — `data/szat_bootstrap_eg_samples.npy` generated; ρ = −0.0014 (PASS); hard stop cleared
- **Gate:** |ρ| < 0.30 ✓ — CI test `test_fisher_channel_independence` now active

### Fisher Combination Defense Document — **DONE**

`analysis/methodology/fisher_combination_defense.md` written with AV1–AV8 (independence, channel selection, minority-only, combination method robustness, directionality, n_eff correction, multiple maps, pre-registration chain). Computed values: Fisher (2ch) p=1.55e-8, Fisher (3ch) p=2.46e-8, Stouffer p~2e-8, Cauchy p~2e-8. `fisher_independence_defense.md` trimmed and pointer added.

### Inter-Map Comparison Permutation Test (Ch1-COMP) — DONE 2026-05-10

**Pre-registered OSF yvc7g (2026-05-10), git ba0e686, drand seed 1823538405 (salt "ch1-comp").**

**Results:** Version A (EG-only) p=0.0303 (observed gap +3.92 pp, null 95th pct +3.43 pp). Version B (Mahalanobis joint) p=0.0001 (D=7.19, null 95th pct 4.38). Both significant. 3/4 metrics minority more UCP-favorable; declination reverses (expected). Verdict: SUPPORTED at classical threshold on both versions.

Output: `analysis/reports/intermap_permutation_test_results.json` + `.md`. Inserted in §5.4 as Ch1-COMP paragraph.

### Phase 4C Vision Assignment (Stages 3–7)

Stage 3 superseded by official shapefiles. Still needed for vote aggregation.

- **Stage 3 SUPERSEDED** — Replace Vision API calls with spatial join of VA centroids against `ea_minority_2026_eds.gpkg` / `ea_majority_2026_eds.gpkg`. Effort: 2 hours.
- **Stage 4:** Aggregate spatial join output to CSV per 2026 ED.
- **Stage 5:** Group VA votes by 2026 ED; aggregate totals. C1 complete — unblocked.
- **Stage 6:** Execute `packing_cracking_analysis.py` on Stage 5 data.
- **Stage 7:** Run `monte_carlo_ci.py` on Stage 5 output.

### External Tool Validation

- **Phase 1 (highest priority):** R `redist` package cross-validation — independently reproduce seats@50/50. Effort: 1 evening + ~90 min runtime.
- **Phase 2:** QGIS visual inspection using official shapefiles (no reconstruction needed). Effort: 1 h setup + 1 afternoon.
- **Phase 2.5:** Maptitude free-trial cross-validation. Effort: 4 h setup + 2 h QA.

---

## HIGH — Sentiment Analysis

- **Corpus:** 1,252 published submissions (1,340 IDs; 88 withdrawn)
- **Full-corpus scan DONE 2026-05-10:** 388 rows, 71 submissions, 49% opp / 21% sup. `data/outputs/submission_sentiment_llm_full_results.csv`
- **Hansard R1 DONE 2026-05-10:** 188/188 community turns classified.
- **Hansard R2 DONE 2026-05-10:** 209/209 community turns classified.
- **§5.9.4.6 written + committed DONE 2026-05-10:** Channel-divergence analysis, per-config tables, intensity-weighted ranking, partisan-sorting caveat. RMH-Banff and Red Deer flip from net-opposed (submissions) to net-supported (Hansard). Airdrie/Chestermere/Nolan-Hill consistently opposed both channels.
- **Intensity scoring pass IN PROGRESS:** `sentiment_intensity_score.py` — 459 active rows, haiku model, ~4h ETA. Relaunched 2026-05-10 (bg02j9iz7) after prior session expired with 0 rows written. Log: `analysis/reports/isr_run1.log`. When complete: update §5.9.4.6 weighted-net table.
- **Remaining forensic pipeline:** `quote_verify_and_clean.py` → `validation_sample.py` → human review → `compute_kappa.py` → `cross_reference_submitters.py`
- **Cross-reference:** Final results against `minority_rationales_validation.md` Proposals A–F
- **Refactor:** Update `submission_sentiment_llm_full.py` to import from `analysis/utils/`

---

## HIGH — Pre-Publication Outreach

### Pre-Brief Academics (do before public release)

Outreach sent to Elections Alberta and Duane Bratt on 2026-04-23; replies received 2026-05-09. Next steps:

1. **Send draft to Bratt** (MRU political science chair, *Orange Chinook* co-editor) — priority flags: ES-14, ES-17, ES-19, ES-02, spatial methodology. Send after ES-02/ES-14/ES-17/ES-19 are complete.
2. **Send spatial methodology sections to Nguyen + Moorman** (MRU GIS/geography) — priority flags: ES-13, spatial methods in §4. Send after ES-13 complete.
3. **One additional academic reviewer** (political science, outside MRU) — identify after Bratt feedback.
4. Response turnaround: allow 2–3 weeks before final revision pass.

### URL Archival

- 13 priority URLs need Wayback Machine + archive.ph submission (authenticated browser session required)
- 6 additional SPN2 POST submissions needed
- After submission: update `FROZEN_MANIFEST.md` and `private_workspace/url_archival_log.md`

### Editorial Factual Ambiguity

- Airdrie population framing (74,100 vs 84,000) — author clarification required. Recommendation: use 84,000 (2024 estimate) throughout.

---

## HIGH — Red-Team Code Corrections

Five HIGH findings still unfixed (from `red_team_code_fixes.md` §5):

- **HIGH-03** Magic-number bounding boxes — deferred
- **HIGH-05** Mixed RNG sources — documentation fix only; deferred
- **HIGH-06** 2015 region classification heuristic — deferred
- **HIGH-08** Chrome `--no-sandbox` hardening — deferred
- **HIGH-11** Suppressed-DA uncertainty accumulation — deferred

Numeric drift 0.05–0.09 pp on sensitivity endpoints from prior rounding corrections — headline numbers unchanged but prose must match.

---

## MEDIUM — Pending Analysis

### Open GitHub Challenges (Issues #13 and #14)

- **MCMC-13 — 2019-seeded ensemble** (GitHub Issue #13): Seed ReCom chain from 2019 enacted geometry; single-boundary moves; population-target-preserving swaps. Effort: 2–3 days + ~90 min compute. Referenced in `retraction_pathway.md` §7.2 and README.md §Known Limitations.

- **COUNTER-14 — Counter-map challenge** (GitHub Issue #14): Retraction condition for §5.8.5 anchoring finding. Produce constraint-legal 89-seat map satisfying minority's stated COI rationales AND achieving majority-comparable municipal-boundary anchoring (CSD/DA edge alignment ≥60%). Status: open; no counter-map submitted as of 2026-05-10.

- **338-RETRO — Historical polling sensitivity** (Track E extension): Use 77 historical 338Canada snapshots to reallocate both 2026 maps across the full polling range. Find crossover pp level where minority-vs-majority seat direction flips. Effort: 2–3 hours adapting `338canada_reallocate.py`.

### Data Source Gaps (minority_rationales_validation.md Proposals A–F)

**StatsCan Journey-to-Work (98-10-0459 series):**
- Already downloaded: Cochrane CSD origin table
- Missing: Airdrie, Chestermere, Sylvan Lake, Innisfail, Red Deer origin-CSD tables
- Impact: R2/R5/R11 verdicts currently INCONCLUSIVE

### Manual Source Verifications

- RMH-Banff attribution — verify against Hansard/X-thread sources before CRIT-B deletion
- Public-support refutation scope — 3 items need manual cross-check

---

## MEDIUM — Dissemination

### SSRN / OSF Preprint (before journal submission)

Post working paper to SSRN and/or OSF Preprints to establish priority. Steps:
1. Finalize report_academic.md (post S2-02, G3, G4 fixes) — version stamp it
2. Post PDF to SSRN (Canadian Social Science category) and OSF Preprints under the existing OSF node
3. Announce to institutional reviewers (Bratt/Nguyen/Moorman) with preprint link
4. Journal submission after preprint is live and at least one reviewer has read draft

**Target journals (in order):** *Canadian Public Policy*, *Electoral Studies*, *Political Science Research and Methods*

### Media Prep Kit

For the window immediately following publication:

1. **1-page non-technical summary** — "What did the Alberta boundary commission do, what did we find, what does it mean for voters" — no p-values, no EG; use the seat-gap and wasted-vote framings
2. **Visual asset package** — 3–5 key figures export-ready (300 dpi PNG); existing SVG outputs in `data/maps/mcmc/` are candidates
3. **FAQ document** — 10 questions a journalist or MLA would ask; pre-drafted answers; include "what this study does NOT claim" section
4. **Contact list** — Bratt + 2 others willing to field media calls; confirmation required before release

### Globe and Mail Data Desk Pitch

- Target: Globe and Mail data-journalism desk (Edmonton-based or national)
- Angle: Alberta's proposed boundary change and what a statistical audit of the process found
- Pitch format: 3-sentence summary + link to preprint + offer of embargoed early access
- Timing: send after preprint is live and BEFORE journal peer-review outcome
- Note: pitch to CBC Alberta as fallback

### Indigenous Dimension — Expanded Section

Current §5.8.4 notes Enoch Cree Nation (Reserve 135) PP=0.065 (lowest in 178-ED joint set) and Tsuut'ina comparison. Needs expansion:

1. **s.35 Constitutional Act, 1982 framing** — boundary decisions that affect reserve lands engage consultation obligations; the EBC's rationale silence for Enoch Cree–Devon pairing has a constitutional dimension beyond electoral design
2. **UNDRIP (Bill C-15, 2021) framing** — Article 18 free, prior, and informed consent in legislative/administrative decisions affecting Indigenous peoples; apply to boundary commission process
3. **Tsuut'ina comparison (partially done)** — Tsuut'ina Nation (Reserve 145) absorbed into Calgary-West in majority proposal; different treatment from Enoch Cree; document the asymmetry in the commission's stated rationale
4. **"Broadest coalition potential" framing** — from six-hats synthesis: this finding has the broadest political-coalition potential of any finding in the audit; it appeals across party lines and to international audiences
5. Effort: 1–2 h for s.35/UNDRIP paragraphs; Tsuut'ina comparison already partially in §5.8.4

---

## MEDIUM — Restructure / Hygiene

### analysis/ Directory Restructure

Three-phase execution (PO-approved 2026-04-23):

- **Phase A (2–3 hours):** 12 zero-reference files — move to correct directories; validate imports
- **Phase B (6–8 hours):** ~45 files with 1–2 references — move in batches; grep-replace cross-references after each
- **Phase C (8–10 hours):** 15 high-risk files with 3+ references
- **Phase D (2–3 hours):** Verification — ast.parse all moved .py; grep for stale paths
- **Awaiting:** execution trigger from PO

### Remediation Hygiene Track (Phases 3–5)

Deferred after Safety Track completion:

- Constants module, ED name resolver, god function decomposition
- `sys.path` removal, `data_loader` abstraction, `mcmc_runner` consolidation
- `ruff` config + `mypy`, `iterrows` migration, TypedDict types

### Paper Methodology Section — Fisher Defense — **DONE**

- `fisher_combination_defense.md` written (AV1–AV8); `fisher_independence_defense.md` trimmed. See Computational Blockers section above.

---

# M3 — LUNTY RELEASE (Nov 2, 2026)

External event: government may table 91-seat map from MLA committee. Trigger: run full pre-registered checklist within 48 hours of tabling.

## November Scorecard Dashboard

Build a public GitHub Pages dashboard for same-day publication alongside the Phase 2 audit:

- **Content:** Phase 2 metrics for the 91-seat Lunty proposal vs the two 89-seat proposals; population equality, EG, MM, declination, seats@50/50, compactness; traffic-light RAG status per metric
- **Stack:** Static site (no server); rendered from audit JSON outputs; GitHub Pages hosting
- **Pre-requisite:** Finalize the Phase 2 pre-registration in OSF before the tabling date; register the exact metric thresholds and direction predictions
- **Effort:** 1 day build (if audit outputs are already in JSON format, which they are)
- **Note:** Dashboard is NOT the paper — it is a companion artifact for immediate public consumption

## Phase 2 — Lunty Committee Map

- **Phase question:** Is the Lunty MLA committee's 91-seat map a gerrymander?
- **Pre-registration:** Must be filed on OSF before the map is tabled (before Nov 2, 2026); use the same drand beacon framework
- **Checklist on tabling:** population equality, packing/cracking analysis, MCMC ensemble against 91-seat neutral baseline, spatial audit, SZAT equivalent
- **Timeline:** 48-hour publication target from tabling date

## 338Canada Refresh (Track E)

Every 60–90 days; next due ~late June 2026. Re-run `338canada_scraper.py` and `338canada_reallocate.py`; update public report if projection moves >0.5pp.

## Phase 2 Methods Paper

After Phase 2 audit is complete, write a methods companion paper covering:
- Extension of the MCMC/SZAT framework to legislative committee maps
- Comparison of commission-drawn vs committee-drawn boundary processes
- November 2026 pre-registered results vs April 2026 exploratory findings

---

# Date-Gated External Events

| Track | Event | Trigger |
|---|---|---|
| A (shapefile integration) | Unblocked 2026-05-06 (commit 873f4d0) | Re-run Phase 5 ensemble after C1 complete |
| B (November 2026) | Lunty committee tables 91-seat map (Nov 2, 2026) | Run full Phase 2 checklist within 48h |
| E (338Canada refresh) | Next due ~late June 2026 | Re-run scraper if projection moves >0.5pp |

---

# External Blockers

- **OSF pre-registration disclosure gap** — Ch1 (Mahalanobis) and Ch2 (SZAT) are not named in any of the four pre-registered files (w2s8k/r3zm7/qsgy8/6pt83). Registrations cover drain test (Ch3) and DPG v11 methodology only. Paper must disclose this gap in §3.7.

  **Corrected timing record (from OS timestamp audit + email evidence, 2026-05-10):** The drand beacon infrastructure was committed 2026-04-27. The official EA shapefiles were received by email from Raymond Mok (Elections Alberta GIS Team Lead) at **09:51 AM on 2026-05-06** — 9 days after the beacon was committed. The drand seed therefore predates the data by 9 days. `szat_summary.json` (SZAT results) was committed in `873f4d0` at 18:11 on 2026-05-06. The OSF SZAT registration (6pt83) script was written at 21:16 — approximately 3 hours later. For Ch1 (Mahalanobis), the canonical ensemble and `joint_outlier_score.json` were committed at 21:51 on 2026-05-06 (commit `299658b`), after `osf_register.py` was created at 20:14 — consistent with the ensemble still running when registration was set up. See Gate G5 for required disclosure fixes.

- **November 2026 committee deadline** — drives Phase 2 publication target

---

# Done

- `eg_utils.py` extraction (szat.py + szat_validate.py unified; DRY fix)
- Generator API migration (reock.py, tier_aware_perturbation; gerrychain-compat files annotated)
- `data_loader.py` lazy config loader (import side effects removed)
- `__main__` guard wrapping (generate_infographic.py × 2, plan_b_rerun.py)
- Integration test suite (`tests/test_pipeline_integration.py` — 6 tests incl. Fisher gate)
- Unit tests: canonical manifest (14), data loader (12)
- `fisher_independence_defense.md` — structural argument + CI gate + empirical check infrastructure
- `fisher_combination_defense.md` — 8 attack vectors (AV1–AV8) with computed values
- Six Hats critique of REMEDIATION_LOG.md + three fixes
- `submission_search.py` keyword pass — 70 flagged submissions, dataset complete
- OSF pre-registrations submitted: w2s8k / r3zm7 / qsgy8 / 6pt83
- OSF file content verified 2026-05-09
- Academic reorganization (voice check PASS, FK 12.9, completed 2026-04-23)
- Editorial three-voice pass (FK 10.0 → 10.6, completed 2026-04-22)
- Outreach to Elections Alberta + Duane Bratt — replies received 2026-05-09
- Sentiment analysis architecture: 4 utils modules; 11 scripts refactored; Hansard parser; forensic pipeline
- OCR recovery: 23 image-only submissions recovered via PyMuPDF + EasyOCR
- Phase 4C VA assignment: 89/89 EDs resolved in both maps
- intermap_permutation_test.py — **DONE 2026-05-10**: V-A p=0.0303, V-B p=0.0001; both significant; inserted in §5.4 as Ch1-COMP (OSF yvc7g)
- Six Hats 4-pass analysis + synthesis
- C1 advance-vote splat — **DONE 2026-05-10**: `va_polygons_with_full_2023_votes.gpkg`; 1,706,304 two-party; NDP 45.56%; 2,110 swing zones
- G1 Fisher independence check — **DONE 2026-05-10**: ρ=−0.0014, p=0.8884; szat.py fixed (swing count 2108→2110, logger NameError); SZAT p updated 0.0044→0.0024; Fisher 2ch p=8.71e-9; all 6 docs updated

---

# Planning Docs — Flagged for Deletion

These documents' outstanding content is now consolidated above. After confirming nothing was missed, delete:

| File | Reason |
| --- | --- |
| `analysis/methodology/master_plan.md` | All open D/S/G/C items now in CRITICAL and HIGH sections above |
| `analysis/methodology/assignment_runbook.md` | Stage 3–7 procedure now in Phase 4C section above |
| `analysis/methodology/assignment_execution_log.md` | Stage status now in Phase 4C section above |
| `analysis/methodology/external_tool_validation_plan.md` | All three phases now in External Validation section above |
| `analysis/red_team/archival_submission_queue.md` | URL archival task now in HIGH section above |
| `analysis/methodology/restructure_inventory.md` | Phase A–D tasks now in Restructure section above |
| `private_workspace/migration.md` | Track C and Track E now in Date-Gated section above |
| `analysis/methodology/editorial_pass_log.md` | Completed log; no outstanding items |
| `REMEDIATION_LOG.md` | Safety Track complete; open items already in Remediation Hygiene section above |

**Do NOT delete (content, not plans):**

- `analysis/red_team/red_team_assertions.md` — assertion inventory; keep until referee response
- `analysis/red_team/red_team_code_fixes.md` — deferred HIGH/MEDIUM rationale; keep until fixes complete
- `analysis/methodology/minority_rationales_validation.md` — scientific findings
- `analysis/meta/FROZEN_MANIFEST.md` — canonical file manifest
- All methodology, findings, and defense documents
