# Alberta Audit — Completed Work Log

**Project:** Electoral Boundary Analysis, Phase 1 (minority map)
**Migrated from TODO.md:** 2026-05-11
**Purpose:** Archive of completed items. All open/pending work remains in `TODO.md`.

---

## M1 — Monday 2026-05-12 Group Chat Review

All 15 items completed 2026-05-10: ES-24, ES-25, ES-22, ES-26, ES-03, ES-01, ES-34, ES-09, ES-31, ES-05, ES-08, ES-02, ES-17, ES-07, C1, S2-02. Detail per item in commit history and `analysis/methodology/editorial_pass_log.md`.

---

## CRITICAL — Submission Gates

All 5/5 clear as of 2026-05-10.

- **G1 DONE 2026-05-10** Fisher independence check: ρ = −0.0014, p = 0.8884 (PASS |ρ| < 0.30); SZAT p updated 0.0044 → 0.0024; Fisher 2ch p = 8.71e-9.
- **G2 DONE 2026-05-10** S2-02 MCMC rescore: canonical 250k values from `simulated_ensemble_percentiles_canonical.csv` propagated to §5.4.9, §5.5, §6.2.1, §6.2.2 — key change: minority EG p94.2 (below p95, flag retracted); majority MM p0.85 (new NDP-tail finding).
- **G3 DONE 2026-05-10** BH correction table inserted at §4.3.1: 11 formal tests, 10/11 pass BH at α=0.05; sole failure is Minority EG (p94.2, already retracted).
- **G4 DONE 2026-05-10** Direction disagreement framing in §5.4/§6: EG+MM+seats (minority more UCP) vs declination (minority least UCP) vs 338 April 2026 (minority +1 NDP seat) reconciled explicitly.
- **G5 DONE 2026-05-10** Pre-registration timing disclosure fixed in §5.3.1 and `preregistration_salt_audit_trail.md`.

---

## CRITICAL — Report Accuracy (from red_team_assertions.md)

- **CRIT-A DONE 2026-05-09** Sensitivity table re-run complete. New values (w=0.85 central): majority −0.40%, minority −1.81%, asymmetry −1.41 pp. Range 0.47–1.48 pp (0.70–0.80 bracket). B4 direction reversed: minority now matches 2019 at 46 NDP seats@50/50 vs majority 45. Updated: report_academic.md §§5.2.1/5.2.2/5.2.7/5.2.8/summary table, README.md, report_public.md, assignment_gerrymander_comparison.md, maup_area_weighted_analysis.md, threshold_provenance.md §B.2.1, urban_weight_defense.md, chen_rodden_decomposition.md.
- **CRIT-B DONE 2026-05-09** RMH-Banff "+0.7 seat" and "minority wins RMH-Banff in 50% of samples" text not found in either report — already removed in a prior session. No action required.
- **CRIT-C DONE 2026-05-09** Public report intro corrected.
- **HIGH-A DONE 2026-05-10** Cross-election asymmetry table (2015–2019–2023) added to Appendix A.1 with three-election data (2015 +0.03 pp, 2019 +0.75 pp, 2023 −0.51 pp) and cycle-contingency caveat.
- **HIGH-B DONE 2026-05-10** Monte Carlo median drift (~0.3 pp variance between runs) disclosed in footnote [^1] to §5.2.3. Canonical Run #4 median (−1.40 pp) differs from preliminary run (−1.44 pp) consistent with Monte Carlo sampling; direction and sensitivity bounds unaffected.
- **HIGH-C DONE 2026-05-10** Submission count reconciliation — Section D aligned with `submission_search_findings.md`: 1,252 of ~1,340 submissions extracted; remainder (~88, 6.6%) are image-only PDFs.
- **HIGH-D DONE 2026-05-09** Wesley commission attribution resolved.
- **HIGH-E DONE 2026-05-09** Nenshi quote fixed.

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
- **S4 DONE 2026-05-10** Small-N noise floor — SE ~1–2pp paragraph added to §5.2.3; 1.41pp central asymmetry characterised as near lower bound of reliable detection at 89 seats.
- **S2-01 DONE 2026-05-10** MCMC ESS precision disclosure — canonical 4-chain R-hat table inserted in §5.4 (GR92 + Vehtari 2021 side-by-side); worst-chain ESS 63–94 reported; EG/declination marginal V21 failure disclosed with Ch1 headroom note. OSF s58a6 Section B. Output: `data/outputs/rhat_diagnostic_section_b.json`.
- **S2-02 DONE 2026-05-10 (Gate G2)** 250k canonical values propagated to §5.4.9, §5.5, §6.2.1, §6.2.2. Minority EG retracted (p94.2); majority MM p0.85 NDP-tail documented with mechanism explanation.
- **S9-01 DONE 2026-05-10** p100 language recalibration — BH footnote (§4.3.1) updated: row 3 retracted, ESS caveat + full-coverage rescore note added. Partisan Bias prose (§5.6): "100th percentile" → "above 99.9% of the ensemble (ESS-adjusted lower bound: at least p95)".
- **S2-03 DONE 2026-05-10 (Gate G3)** BH correction table at §4.3.1: 11 tests, 10/11 pass, sole failure Minority EG (already retracted).
- **S2-04 DONE 2026-05-10 (Gate G4)** Direction disagreement three-layer reconciliation paragraph inserted in §6.
- **DECISION-CH3 2026-05-10** Neighbour-Drain novelty claim dropped from `novel_contributions.md`. Pre-registered test (AsPredicted #289,451, OSF r3zm7) returned inverted finding — minority map zero coupled chain signals vs three on both comparators. Post-hoc reframing as "topology classifier" rejected (HARKing). Decision: report result honestly as Channel 3 per pre-registration obligation; no novelty claim; internalization interpretation noted as hypothesis in discussion only.

---

## CRITICAL — Pre-Registration Timing Disclosure (Gate G5) — DONE 2026-05-10

`preregistration_salt_audit_trail.md` corrected: SZAT OSF form (6pt83) filed ~3 hours after szat.py first ran; provenance rests on drand seed committed 2026-04-27, not OSF form. Timeline table added.

---

## CRITICAL — Peer Review (ES-01 through ES-36)

- **S1-01 FIXED 2026-05-09** Pre-registration provenance — three edits made.
- **ES-01 DONE (pre-existing)** *Rizzo* case-name — verified correct throughout.
- **ES-02 DONE 2026-05-10** Comparator-trio rewrite §5.9.3 — Quebec 2011 + SCC April 2026 substituted; stale §2 pointer fixed.
- **ES-03 DONE 2026-05-10** Alberta 2017 seat-count — no "2017 expanded" claim found; stale §2 cross-ref corrected.
- **ES-04 DONE** (=S2-01/S2-02/S9-01) MCMC percentile demotion — all sub-items complete.
- **ES-05 DONE 2026-05-10** Abstract contingency clause — "EG direction reverses under 2019 votes (see §5.2.3)" added.
- **ES-06 DONE 2026-05-10** Exploratory-vs-confirmatory foregrounding — *Evidentiary status* paragraph added to Abstract; bold paragraph added to §1.
- **ES-07 DONE 2026-05-10** Multiple-comparisons §4.x subsection — §4.3.2 added with Bonferroni vs BH comparison; Fisher combination section and rationale included.
- **ES-08 DONE 2026-05-10** E2 both-readings paragraph — RMH-Banff under original + substantive E2 added to §5.3.3.
- **ES-09 DONE 2026-05-10** "67th/71st percentile" demoted — removed from §5.2.1; defensible rank statement kept.
- **ES-10 DONE 2026-05-10** *Grant v. Torstar* + defamation posture — Appendix F expanded (~750 words); responsible-communication defence, fair-comment test, and outreach rationale documented.
- **ES-11 DONE 2026-05-10** Intent-imputation verb softening — "got it wrong" → "do not survive primary-source verification"; "elides this distinction" → "does not carry this distinction"; "materially misrepresents" → "materially overstates" (prior session).
- **ES-12 DONE 2026-05-10** "Override" vocabulary rewrite §5.9 — "government is pushing boundary choices" replaced with "committee's eventual map will include"; "government-controlled drafting" → "MLA-committee-directed"; "displacing commission-recommended boundaries" → "reassigning".
- **ES-13 DONE 2026-05-10** VA-polygon vote-coverage §5.4 wiring — paragraph already present; SZAT cross-reference updated to reflect definitive SZAT run uses full-VA substrate.
- **ES-14 DONE 2026-05-10** Canadian literature engagement — §2 redistribution paragraph expanded: Courtney chs. 6–7/10–11 pin-cites; Pal (2015) discretion/design-choice framework; Pal & Choudhry (2011, 2014); Wesley (2011, 2015); Seidle (1991) *(note: Seidle reference subsequently removed 2026-05-11 — see VERIFY in TODO.md)*. §5.9.3 expanded. 5 references added.
- **ES-15 DONE 2026-05-10** *Rucho v. Common Cause* engagement.
- **ES-16 DONE 2026-05-10** Saskatchewan Reference constitutional-standard depth.
- **ES-17 DONE 2026-05-10** Institutional context paragraph — added at top of §2.
- **ES-18 DONE 2026-05-10** Alberta 2022 federal sub-commission comparator — comprehensive subsection in §5.9.3 (~350 words).
- **ES-19 DONE 2026-05-10** Alberta volatility paragraph — inserted at end of §5.2.3; cites Bratt, Brownsey, Sutherland & Taras (2019) *Orange Chinook* and CPSR 2020 special issue; weights structural findings over partisan-bias findings.
- **ES-20 DONE 2026-05-10** *Raîche* and *Cassista* to body — integrated into main body at §158 with holdings and application to Saskatchewan Reference standard.
- **ES-21 DONE (pre-existing)** *Haig v. Canada* ghost reference — already removed.
- **ES-22 DONE 2026-05-10** §5.2.2 deterministic vs MC distinction — sentence added.
- **ES-23 DONE 2026-05-10** Contribution positioning (d) — strengthened as headline; (a)–(c) as supporting; grounded in EBCA §12(3), 2022 federal precedent, Courtney-Pal lineage.
- **ES-24 DONE 2026-05-10** Abstract word-count cut — trimmed to 150–250 words.
- **ES-25 DONE 2026-05-10** "US judicial threshold" → "Stephanopoulos-McGhee 7% investigable-bias threshold" throughout.
- **ES-26 DONE 2026-05-10** Declination formula in Appendix D.3 — formal definition added; PP→D.4, Reock→D.5.
- **ES-27 DONE 2026-05-10** Per-metric ESS in §5.4 — worst-chain ESS 63–94 reported in canonical R-hat table.
- **ES-28 DONE (verified pre-existing 2026-05-11)** §E.7 v4-residual-gap collapse — already collapsed to 2-paragraph summary in report; verified.
- **ES-29 DONE 2026-05-11** Citation-format cleanup: (1) Added missing ASA 2016 p-value statement to References; (2) standardized Data Sources section from APA-style parenthetical years to APSA-consistent non-parenthetical; (3) Chen/Rodden already (2013) throughout — no (2015) remaining; (4) court-cases format confirmed correct. Seidle (1991) *Rethinking Government* removed — cited book does not match intended Lortie Commission work; see VERIFY in TODO.md.
- **ES-30 DONE 2026-05-11** Pincite and terminology: (1) Courtney chapter pincites (chs. 6–7 / 10–11 / 3–4) already present in §2 and §5.9.3 — verified; (2) EBCA section pincites (§12(3), §15(2), §14) already in body text — verified; (3) "independent" (relationship to government) vs "non-partisan" (drawing mandate) applied consistently — verified by sampling.
- **ES-31 DONE 2026-05-10** Unused references — Sancton (2008) body citation added; no Smith (2010) found.
- **ES-32 DONE 2026-05-11** Statistical-presentation clarifications: (1) §4.1.2 G1 "confirmed against SoV" removed; replaced with "arithmetic verified: 777,404 + 928,900 = 1,706,304; source: data/raw/2023_results.xlsx"; (2) §5.1.1 MAD footnote — verified by hand: MAD=4,707 against both 54,929 and 54,930; (3) §5.2.5 Chen-Rodden/ReCom disambiguation added; (4) §5.3.1 source CSV confirmed (votes_2023_minority.csv has ndp_2023/ucp_2023 columns); (5) §5.6 Edmonton units clarification added.
- **ES-33 DONE (verified pre-existing 2026-05-11)** Alberta Treasury Board 2024 estimate context — two sentences at §3.3 already present.
- **ES-34 DONE (pre-existing)** Abstract dimension labels — already fixed in prior session.
- **ES-35 DONE (verified pre-existing 2026-05-11)** Abstract L9 assertiveness — already handled.
- **ES-36 DONE (pre-existing)** §5.9.5 "implicate" → "be evaluated against" — already corrected.

---

## Computational Blockers — Completed

- **1M canonical ensemble DONE 2026-05-12** — 4 chains × 252,500 steps = 1,010,000 total plans assembled. Chain1 experienced a sampler hang at chunk 12/50 of the extension (documented commit 70e2695, 2026-05-11); hang resolved and all 4 chains completed. ESS: 1,429–1,682 (partisan metrics), exceeds publication-grade threshold. Key result changes vs 250k run: seats@50/50 individual flag reinstated (n_eff=1,495 gives ESS-adjusted lower bound ≈p98, above p95 threshold); all other flags and conclusions unchanged. §5.4.9 and §5.4.10 direction-of-travel table updated to 1M values.

- **C1 DONE 2026-05-10** Advance-vote splat — `va_polygons_with_full_2023_votes.gpkg`; two-party total 1,544,139 (post-C5); NDP share 44.66%; 4,765 VAs; conservation PASS (delta = 0).
- **C5 DONE 2026-05-10** Vote Anywhere exclusion — 87 rows excluded (NDP 87,767 / UCP 74,398 / Other 3,768); filtered inline in `advance_vote_splat.py`.
- **DOC-ACCURACY DONE 2026-05-10** Post-C1 stale-figure sweep — corrected NDP post-splat share and substrate two-party total across 6 documents.
- **Fisher Independence Check (Gate G1) DONE 2026-05-10** `data/szat_bootstrap_eg_samples.npy` generated; ρ = −0.0014 (PASS); hard stop cleared; CI test `test_fisher_channel_independence` now active.
- **Fisher Combination Defense DONE** `analysis/methodology/fisher_combination_defense.md` written with AV1–AV8. Computed values: Fisher (2ch) p=8.71e-9, Fisher (3ch) p=1.57e-8, Stouffer p=2.29e-8, Cauchy p=3.20e-7. `fisher_independence_defense.md` trimmed.
- **Ch1-COMP DONE 2026-05-10** Inter-map comparison permutation test. Pre-registered OSF yvc7g (2026-05-10), git ba0e686, drand seed 1823538405 (salt "ch1-comp"). Results: Version A (EG-only) p=0.0303; Version B (Mahalanobis joint) p=0.0001. Both significant. Inserted in §5.4 as Ch1-COMP paragraph.
- **mcmc_anchoring_ensemble.py + full run DONE 2026-05-12** CSD edge-crossing anchoring metric implemented and full 10,000-plan run completed (OSF s58a6 pending channel). Seed: 80780579 (drand round 6099592, salt "alberta-audit-anchoring-ensemble"). Metric: fraction of cut edges crossing a CSD boundary. Smoke test (2 chains × 50 steps) and full run (2 chains × 5,000 steps = 10,000 plans) both exit code 0. Full-run results: ensemble median 17.82%, p5 16.73%, p95 18.97%; majority 37.63% → p100; minority 29.75% → p100. Pre-registered direction not confirmed (minority predicted < ensemble median; actual: p100). Null finding on "anomalous unanchoring." Outputs: `data/outputs/csd_anchoring_ensemble.csv`, `data/outputs/csd_anchoring_results.json`. §5.4.9 updated.

---

## Sentiment Analysis — Completed Phases

- **Full-corpus scan DONE 2026-05-10** 388 rows, 71 submissions, 49% opp / 21% sup. `data/outputs/submission_sentiment_llm_full_results.csv`.
- **Hansard R1 DONE 2026-05-10** 188/188 community turns classified.
- **Hansard R2 DONE 2026-05-10** 209/209 community turns classified.
- **§5.9.4.6 written + committed DONE 2026-05-10** Channel-divergence analysis, per-config tables, intensity-weighted ranking, partisan-sorting caveat. RMH-Banff and Red Deer flip from net-opposed (submissions) to net-supported (Hansard). Airdrie/Chestermere/Nolan-Hill consistently opposed both channels.
- **quote_verify_and_clean.py DONE 2026-05-12** 100% verification rate: 482 VERIFIED, 26 NEAR_MATCH, 0 UNVERIFIED (508 quoted rows). Logic: NFKD → ASCII normalize, literal substring check, fallback SequenceMatcher ratio ≥ 0.85. Outputs: `data/outputs/quotes_verified.csv`, `data/outputs/quote_verification_summary.json`.
- **validation_sample.py DONE 2026-05-12** 60-item stratified IRR sample across configuration × classification cells. Seed: 670497761 (drand round 6099592, salt "alberta-audit-irr-sample"). Output: `data/outputs/irr_validation_sample.csv` (human_label column blank — awaiting annotation).
- **compute_kappa.py DONE 2026-05-12** Script complete. Implements Cohen's kappa with confusion matrix and per-class P/R/F1. Acceptable-for-publication threshold: kappa ≥ 0.60. Run after human fills `human_label` column.
- **cross_reference_submitters.py DONE 2026-05-12** Majority-submission sentiment contradicts commission's claimed public support on 3 of 6 matched rationales: R1 Calgary-Nolan Hill-Cochrane (38 oppose / 12 support → CONTRA_COMMISSION), R3 Airdrie (38/12 → CONTRA_COMMISSION), R10 Red Deer (58/24 → CONTRA_COMMISSION). R2 Chestermere: ALIGNS_WITH_AUDIT. Outputs: `data/outputs/cross_reference_results.csv`, `data/outputs/cross_reference_summary.json`.
- **attribution_sensitivity_check.py DONE 2026-05-12** Partial vs full vote coverage (va_ndp ~50% vs va_ndp_full ~89%). Minority map outlier status preserved 4/4 metrics under both variants. Majority mean-median shifts p0.92 → p5.78 (within null; direction unchanged). Full results: `analysis/methodology/attribution_sensitivity_robustness.md`. Academic report updated: corrections table line 1226, direction-of-travel footnote line 1296.
- **monte_carlo_ci.py path fix DONE 2026-05-12** 2019 results CSV path corrected: `data/reference/alberta_2019_results.csv` (was missing two path levels and `reference/` subdir).

---

## Methodology and Defense Documents — Completed

- `fisher_independence_defense.md` — structural argument + CI gate + empirical check infrastructure
- `fisher_combination_defense.md` — 8 attack vectors (AV1–AV8) with computed values
- Six Hats critique of REMEDIATION_LOG.md + three fixes
- `submission_search.py` keyword pass — 70 flagged submissions, dataset complete
- OSF pre-registrations submitted: w2s8k / r3zm7 / qsgy8 / 6pt83
- OSF file content verified 2026-05-09

---

## Earlier Completed Items (pre-2026-05-09)

- `eg_utils.py` extraction (szat.py + szat_validate.py unified; DRY fix)
- Generator API migration (reock.py, tier_aware_perturbation; gerrychain-compat files annotated)
- `data_loader.py` lazy config loader (import side effects removed)
- `__main__` guard wrapping (generate_infographic.py × 2, plan_b_rerun.py)
- Integration test suite (`tests/test_pipeline_integration.py` — 6 tests incl. Fisher gate)
- Unit tests: canonical manifest (14), data loader (12)
- Six Hats 4-pass analysis + synthesis
- Academic reorganization (voice check PASS, FK 12.9, completed 2026-04-23)
- Editorial three-voice pass (FK 10.0 → 10.6, completed 2026-04-22)
- Outreach to Elections Alberta + Duane Bratt — replies received 2026-05-09
- Sentiment analysis architecture: 4 utils modules; 11 scripts refactored; Hansard parser; forensic pipeline
- OCR recovery: 23 image-only submissions recovered via PyMuPDF + EasyOCR
- Phase 4C VA assignment: 89/89 EDs resolved in both maps
- intermap_permutation_test.py — V-A p=0.0303, V-B p=0.0001; both significant; OSF yvc7g
- C1 advance-vote splat — `va_polygons_with_full_2023_votes.gpkg`; 1,706,304 two-party; NDP 45.56%; 2,110 swing zones
- G1 Fisher independence check — ρ=−0.0014, p=0.8884; szat.py fixed (swing count 2108→2110, logger NameError); SZAT p updated 0.0044→0.0024; Fisher 2ch p=8.71e-9; all 6 docs updated
