# Alberta Audit — Outstanding Tasks

**Project:** Electoral Boundary Analysis, Phase 1 (minority map)
**Last updated:** 2026-05-10
**Single source of truth for all outstanding work. Planning docs flagged for deletion at bottom.**

---

## MONDAY REVIEW PREP — Weekend Fast Fixes

Group chat review Monday. These items require no new research — all are prose corrections or short insertions against existing analysis.

### Do before Monday (~4–5 hrs total)

| # | Item | What | Effort |
|---|------|------|--------|
| ES-24 | Abstract word-count cut | Trim to 150–250 words; move technical detail to §1 | 30 min |
| ES-25 | "US judicial threshold" replace | → "Stephanopoulos-McGhee 7% investigable-bias threshold" at Abstract L11 + all instances | 20 min |
| ES-22 | §6 synthesis table numeric drift | Reconcile +1.53/+1.58 and −1.52/−1.43 mismatches from §5.2.2 source cells | 45 min |
| ES-26 | Declination formula, Appendix D.3 | Add formal definition alongside EG and MM | 20 min |
| ES-03 | Alberta 2017 seat-count fix | 2017 Bielby kept 87 seats (not expanded); audit all references implying 2017 expansion | 30 min |
| ES-01 | *Rizzo* case-name fix | → "*Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 SCR 27 at para 21" at L406, L419, References | 20 min |
| ES-34 | Abstract dimension labels | Fix (A, B, C, D, 4, 5) → (1)–(6) | 10 min |
| ES-09 | Drop "71st percentile" | Remove from Abstract and §6 headline; replace with "second-largest of seven sampled cycles" | 45 min |
| ES-31 | Unused references | Sancton (2021) and Smith (2010): cite or remove; check "The Argument" cross-reference | 45 min |

### Do if time (~3–4 hrs total, medium difficulty)

| # | Item | What | Effort |
|---|------|------|--------|
| ES-05 | Abstract contingency clause | Append "under 2023 vote attribution; direction reverses under 2019 votes" to Abstract L9 and §6 | 30 min |
| ES-08 | E2 both-readings paragraph | Show RMH-Banff under original + substantive E2; label reformulation explicitly | 1.5–2 h |
| ES-02 | Comparator trio rewrite §5.9.3 | Drop Quebec 1992/Ontario 1996/BC 2008 (all misdescribed); anchor to Quebec 2024–SCC April 22 | 45 min |
| ES-17 | Institutional context paragraph | §2 paragraph on non-partisan mandate vs US state legislatures; why EG carries different weight | 1 h |

### Defer to post-Monday revision (do not attempt this weekend)

- ES-07: Bayesian-screening §4.x subsection (MCMC multi-chain, BH correction)
- ES-14: Canadian literature engagement (Pal, Wesley, Courtney pin-cites — 3–4 h)
- ES-16: Saskatchewan Reference depth (1.5 h)
- ES-10: *Grant v. Torstar* defamation posture (2 h)
- C1: Advance-vote splat computation (1–2 days)
- S2-02: MCMC full-coverage rescore headline update

---

## CRITICAL — Publication Blockers

### Report Accuracy Fixes (from red_team_assertions.md)

Required before either report goes public:

- **CRIT-A DONE 2026-05-09** Sensitivity table re-run complete. New values (w=0.85 central): majority −0.40%, minority −1.81%, asymmetry −1.41 pp. Range 0.47–1.48 pp (0.70–0.80 bracket). B4 direction reversed: minority now matches 2019 at 46 NDP seats@50/50 vs majority 45. Updated: report_academic.md §§5.2.1/5.2.2/5.2.7/5.2.8/summary table, README.md, report_public.md, assignment_gerrymander_comparison.md, maup_area_weighted_analysis.md, threshold_provenance.md §B.2.1, urban_weight_defense.md, chen_rodden_decomposition.md.
- **CRIT-B DONE 2026-05-09** RMH-Banff "+0.7 seat" and "minority wins RMH-Banff in 50% of samples" text not found in either `report_academic.md` or `report_public.md` — already removed in a prior session. No action required.
- **CRIT-C DONE 2026-05-09** Public report intro "materially wrong on three of them" corrected to "wrong on two of the five — Red Deer's record was evenly divided rather than absent, and Chestermere had three submissions in favour — and his broader 'no support' framing missed the record on two additional configurations the minority adopted from the submissions." Academic report's "upheld on three of seven" is accurate as written.
- **HIGH-A** 2019 cross-election asymmetry values — based on 2015–2019; 2023 data now available. Recompute using 2015–2019–2023; update Appendix A table.
- **HIGH-B** Monte Carlo median drift — median values shift ~0.3 pp between runs; documented internally but not disclosed. Add footnote to Section B/Appendix A explaining variance source; use min/max range instead of point estimates.
- **HIGH-C** Submission count reconciliation — Chair's "no public support" claim vs D-section findings inconsistency. Reconcile counts between `submission_search_findings.md` and Section D narrative; ensure both cite same baseline.
- **HIGH-D DONE 2026-05-09** Wesley commission attribution — no "Chair Ed Wesley" or incorrect 2017 citation found in either `report_academic.md` or `report_public.md`. Academic report uses "EBC 2017 Final Report" at Appendix C table (line 2104) — correct. Already resolved in a prior session.
- **HIGH-E DONE 2026-05-09** Nenshi quote fixed: dropped stitched "Let's be clear," prefix (from different paragraph in source); corrected comma insertion "and, in fact," → "and in fact" (matching DiscoverAirdrie verbatim). The substantive cheating/gerrymandering/assault clause is confirmed verbatim in source.
- **MED-A** Plurality of Albertans claim — needs cross-check. Run `claim_significance_analysis.py`; verify "plurality" (>50%) vs "majority" language threshold.

### Design and Statistical Fixes (from master_plan.md)

- **D1 DONE 2026-05-09** Third-party vote sensitivity run complete. Rule A/B/C results documented in §3.2 Coverage caveats (new bullet 4): EG reverses under Rule C (both maps flip to NDP-favourable; minority +7.41%, majority +4.16%); B3 holds direction under all three rules; disclosure notes Ch1/Ch2 are unaffected. Source: `analysis/scripts/third_party_sensitivity.py`, output `data/outputs/third_party_sensitivity_results.csv`.
- **D2 DONE 2026-05-09** Sensitivity interval relabeling complete. All "confidence interval" labels in `report_academic.md` (§5.2.3 key block + lines 1680/1682/1684 + line 128) and `monte_carlo_ci.py` (docstring title + line 153 print statement) relabeled to "sensitivity interval." Footnote added to §5.2.3 explaining: parameter uncertainty (not frequentist CI); under spatial autocorrelation effective N ~20–30 widens bounds 1.5–2×.
- **D3 DONE 2026-05-09** Cross-election flip mechanical explanation added to `report_academic.md` §3.3 ("Cross-election asymmetry reversal: mechanical explanation" paragraph). Explains Springbank/Bearspaw/Cochrane hybrid blend-zone sensitivity; 2023 suburban NDP share near urban mean vs 2019 shallower penetration; reversal is a model-estimation property, not a different boundary configuration. Also fixed §1.2 item 3 retraction language: clarified v0_8 refutes individual-map sign-flip (v0_7 artifact) but does NOT retract asymmetry direction reversal (+0.75 pp under 2019 documented in §5.2.3); added forward reference to §3.3.
- **D4 DONE 2026-05-09** Neutral-ensemble benchmark caveat added to §5.2.2 (before "Boundary-straddle" paragraph): notes inter-map difference has no theoretical null alone; §5.4.9 provides benchmark (50k canonical run, official shapefiles); minority p95.9/p99.99 outlier, majority within null. Shapefile blocker resolved per commit 873f4d0.
- **D5 DONE 2026-05-09** "Six of seven" language already downgraded to "five of six" in prior sessions (Lethbridge withdrawal). OSF non-coverage disclosure added: (1) §5.9.6 preamble — "Registration status" paragraph noting rationale-failure is qualitative post-hoc, none of OSF {w2s8k, r3zm7, qsgy8, 6pt83} names it as a pre-specified metric; (2) §6.2.2 Lane 2 table — "(qualitative, not pre-registered)" qualifier added to the Rationale-failure row, distinguishing it from the Pre-registered structural-irregularity count in the next row.
- **S1 DONE 2026-05-09** B4 uniform swing footnote added below §5.2.1 table: "Uniform swing model (Gelman & King, 1994). Alberta's non-linear seat-vote curve means true NDP seat count at 50/50 is likely lower; presented for comparability, not prediction."
- **S2 DONE 2026-05-09** Bonferroni note added below §5.2.1 table: 12 comparisons (4 metrics × 3 maps); Bonferroni threshold α=0.0125; no single metric reaches it; finding rests on directional consistency.
- **S3 DONE 2026-05-09** §1.2 preamble item 1 rewritten: "Monte Carlo 95% CI" → "Monte Carlo sensitivity interval"; "[−3.04, +0.76] pp" label updated; "approximately 90% confidence" → "90.5% of draws … a sensitivity result, not a frequentist confidence level." Remaining instances of "approximately 90%" checked in §5.2.3 — already updated under D2.
- **S4 MINOR** Small-N noise floor not disclosed — SE of EG in 89-district system is ~1–2pp; the -1.42pp asymmetry is near the lower bound of reliable detection. Add to MC CI section. Effort: 20 minutes.

### Peer Review Remediation (40–55 hrs estimated)

Source: `editor_synthesis.md`, `science_red_team_design_and_stats.md`

Item numbers (ES-01 through ES-36) match the synthesis priority list in `editor_synthesis.md §2`.

#### PRE-REVIEW PRIORITY (complete before Bratt/Nguyen/Moorman institutional review)

ES-02, ES-13, ES-14, ES-17, ES-19 — in that order. Bratt will hit ES-14/ES-17/ES-19 immediately; Nguyen+Moorman will hit ES-13. ES-02 is fastest. All others deferred to post-review revision.

---

#### CRITICAL (synthesis items 1–6)

- **S1-01 FIXED 2026-05-09** Pre-registration provenance — three edits made:
  1. `README.md` line 109: removed "2 hours and 24 minutes" claim; replaced with accurate description (P/C/E criteria co-temporal in same commit; drand-anchored channels predating shapefile release)
  2. `README.md` line 125: updated "Issue #1 — Official geometry" from stale "no shapefiles released" to resolved state (shapefiles received 2026-05-06, commit `873f4d0`)
  3. `outputs/academic_report/report_academic.md` §5.3.1: added "OSF file content disclosure (verified 2026-05-09)" paragraph — discloses that neither `dpg2_experiment_plan.md` nor `drain_v2_plan.md` names Ch1 (Mahalanobis) or Ch2 (SZAT); Ch1/Ch2 have no named OSF pre-registration document; 6pt83 timestamp note; Fisher combination disclosure requirement
- **ES-01 CRITICAL** *Rizzo* case-name error — change "*Rizzo v. Rizzo Shoes*" to "*Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 SCR 27 at para 21" at L406, L419, and References court-cases block; add Driedger pin-cite. Effort: 20 min.
- **ES-02 CRITICAL** Comparator-trio rewrite §5.9.3 — Quebec 1992, Ontario 1996, BC 2008 are all materially misdescribed; drop all three. Replace with: (a) Quebec 2011 Bill 132 (National Assembly refused to proclaim CRE's delimitation — the Canadian reviewer's own suggested real-override comparator); (b) forward reference to §5.9.5 for the April 22, 2026 SCC ruling (7–2, upheld QCA striking down Quebec's CRE freeze as Charter s.3 violation, six days after the Alberta motion). Framing: "The April 16 Alberta motion has no precedent in any Canadian provincial boundary cycle reviewed in Courtney (2001); the closest constitutional analogue is the Quebec government's 2024 statutory freeze on CRE redistricting, which the SCC struck down on April 22, 2026 — see §5.9.5." Remove "most government-controlled among the three most commonly cited comparators." Effort: 45 min (not 2–3 h — the SCC anchor is already documented in §5.9.5; this is cut-and-forward-reference, not a historical research task).
- **ES-03 CRITICAL** Alberta 2017 seat-count correction — the 2017 Bielby commission kept Alberta at 87 seats (the 2010 Walter commission expanded from 83). Audit all references implying 2017 increased the count. Flag in §5.9.2 that 2026 is the first expansion beyond 87. Effort: 30 min.
- **ES-04** (=S2-01/S2-02/S9-01 below) MCMC percentile demotion — covered under S2-01, S2-02, S9-01.
- **ES-05 CRITICAL** Abstract contingency clause — append "under 2023 vote attribution; direction reverses under 2019 votes" to Abstract L9 and §6 synthesis. Reword §6: "under 2023 vote input, five of six tested dimensions point in the same direction; under 2019 vote input, the partisan-bias dimension reverses." Effort: 30 min. (D3 added the §3.3 explanation; this is the Abstract/§6 propagation.)
- **ES-06 CRITICAL** Exploratory-vs-confirmatory foregrounding — lift exploratory-status language from §5.3.1 to Abstract and §1. Distinguish: current detection is exploratory; November 2026 OSF re-run is confirmatory. (S1-01 fixed pre-registration provenance but did not update Abstract/§1 language.) Effort: 30 min.
- **S2-01** MCMC ESS precision disclosure — language recalibration on ESS-adjusted confidence bounds; report per-metric ESS (which metric carries p98.8 — near 148 or 160?). Effort: 30 min.
- **S2-02** MCMC full-coverage rescore — `data/simulated_ensemble_percentiles_full_100k.csv` contradicts paper headlines: minority mean-median p98.76 (not p100), seats@50/50 p94.27 (below 95 threshold), majority mean-median p92.66 (not p6.6), majority seats@50/50 p57.86 (not p1.7). §3.11 headline numbers must be updated before release.
- **S9-01** p100 language recalibration — "above the entire ensemble" requires calibrated wording throughout §5.4, §5.5, §6, §8.
- **FUTURE-01** Two-tier MCMC population constraint — EBCA §15(2) permits up to −50% deviation for qualifying EDs; current ensemble uses ±25% uniformly, excluding s.15(2) configurations from the sample space. Implement a two-tier constraint: ±25% for the 86 non-s.15(2) EDs, down-to-−50% for the 3 s.15(2) EDs in each map. Note: the 2010 EBC used only 2 s.15(2) slots (Dunvegan-Central Peace-Notley + Lesser Slave Lake); both 2026 maps add a third invocation not in the 2019 baseline. Re-score real maps against this ensemble to quantify the effect on partisan-metric percentiles. Both maps use comparable s.15(2) EDs so asymmetry finding is expected to be robust; absolute percentile positions may shift. Disclosed in §5.4. No blocking dependency; deferred to post-review computation.

#### HIGH (synthesis items 7–16)

- **ES-07 HIGH** Multiple-comparisons §4.x subsection — S2 added a table footnote to §5.2.1 but Methods M2 requires an explicit §4.x treatment or Bayesian-screening reframe. Add a §4.4 paragraph: "These four metrics are reported as a Bayesian screening battery for the November 2026 confirmatory test. Family-wise α under Bonferroni for four tests at α=0.05 is 0.0125; no single metric reaches this threshold individually." Effort: 2–3 h.
- **ES-08 HIGH** E2 reformulation (RMH-Banff Park) — add "both readings" paragraph to §5.3.3 showing RMH-Banff signature under both the original and substantive E2. Label substantive-E2 finding as post-test reformulation. Distinguish purposive interpretation of §15(2) EBCA (legitimate) from reformulation of the audit's own test (which Driedger does not authorise). Pre-register substantive E2 for November in OSF. Effort: 1.5–2 h.
- **ES-09 HIGH** "71st percentile" demote — drop "71st percentile" from Abstract and §6 headline. Replace with rank language: "second-largest of seven sampled cycles." If percentile stays anywhere, move to appendix with standard-error estimate. Effort: 45 min.
- **ES-10 HIGH** *Grant v. Torstar* + defamation posture — add *Grant v. Torstar*, 2009 SCC 61 and *WIC Radio Ltd. v. Simpson*, 2008 SCC 40 to References; add Appendix F subsection "Author's legal posture regarding named-individual characterisations" naming responsible-communication and fair-comment defences, *Grant v. Torstar* diligence factors, outreach attempts (or justification for none) re Chair Miller, Premier Smith, named commissioners. Effort: 2 h.
- **ES-11 HIGH** Intent-imputation verb softening — three specific instances: (a) "materially misrepresents" → "materially overstates the absence of public support"; (b) "elides this distinction" → "does not carry this distinction"; (c) "got it wrong" → "do not survive primary-source verification." Effort: 15 min.
- **ES-12 HIGH** "Override" vocabulary rewrite §5.9 — Discussion table: "Standard override path" → "Ordinary legislative non-adoption"; "Government-controlled drafting" → "Government-chaired committee replacing commission drafting." Abstract must match §5.9.3's honest comparator caveat. Effort: 30 min.
- **ES-13 HIGH** VA-polygon vote-coverage §5.4 wiring — D1 added the §3.2 coverage caveat; still need one paragraph in §5.4 disclosing Election-Day-only bias (52.5% coverage) and how it affects the MCMC percentile flags. Effort: 45 min.
- **ES-14 HIGH** Canadian literature engagement — Pal (2016) *Fractured Right to Vote* McGill LJ 61:2; Pal & Choudhry (2011, 2014); Courtney (2001) chs. 6–7 and 10–11 with actual pin-cites (not ornamental); Wesley (2011) *Code Politics* UBC Press cited as scholar; Seidle (1991) for institutional genealogy. Must go into §2 and §5.9.3 body, not just References. Effort: 3–4 h.
- **ES-15 HIGH** *Rucho v. Common Cause* engagement — either (a) state explicitly that *Rucho* governs US federal justiciability only with no Canadian carry-over, or (b) strip US-judicial-legitimacy borrowing from §5.2.1 and attribute the 7% threshold to Stephanopoulos-McGhee alone. Editor recommends both. Effort: 1 h.
- **ES-16 HIGH** Saskatchewan Reference constitutional-standard depth — add paragraph to §2 acknowledging "effective representation" is not a variance test; quantitative findings are evidentiary inputs to a constitutional weighing that includes non-quantitative factors. Distinguish Charter s.3 (right to vote; Saskatchewan Reference) from s.15 equality. Effort: 1.5 h.

#### MED (synthesis items 17–27)

- **ES-17 MED** Institutional Context paragraph — §2 paragraph naming the non-partisan-mandate distinction between Canadian provincial commissions and US state legislatures; why the same EG metric carries different inferential weight in the two regimes. Effort: 1 h.
- **ES-18 MED** Alberta 2022 federal sub-commission comparator — in §5.3.2 and §5.6, engage the 2022 federal Boundaries Commission's Airdrie–Chestermere and Banff–Airdrie treatment choices as a direct benchmark for the provincial majority's 2-district approach. Effort: 1.5 h.
- **ES-19 MED** Alberta volatility paragraph — add to §5.2.3 or §6 acknowledging Alberta's electoral churn (Bratt et al. 2019 *Orange Chinook*; CPSR 2020 special issue) and weighting structural findings more heavily than partisan-bias findings in the synthesis. Effort: 1 h.
- **ES-20 MED** *Raîche* and *Cassista* to body — move *Raîche v. Canada (AG)*, 2004 FC 679 and *Cassista v. Canada (AG)*, 2014 FC 398 from Appendix F to body at §5.9.5; both apply Saskatchewan Reference to specific boundary disputes. Effort: 1 h.
- **ES-21 MED** *Haig v. Canada* ghost reference — in References but never cited in body; either cite at §2 (s.3 effective-participation chain) or remove. Effort: 15 min.
- **ES-22 MED** §5.2.2/§6 synthesis table numeric drift — reconcile §6 synthesis table directly from §5.2.2 cells; fix the +1.53/+1.58 and −1.52/−1.43 mismatches. Also add a sentence at top of §5.2.2 distinguishing deterministic sensitivity (point estimates by weight) from full Monte Carlo envelope. Effort: 45 min.
- **ES-23 MED** Contribution positioning (d) — reframe §1 headline as "first systematic computational audit of an Alberta provincial boundary commission placed within Canadian commission norms." Routing-dependent (matters most if targeting *Canadian Public Policy*). Effort: 1 h.
- **ES-24 MED** Abstract word-count cut — trim to 150–250 words; move technical detail to §1. Effort: 30 min.
- **ES-25 MED** "US judicial threshold" shorthand replacement — change to "Stephanopoulos-McGhee 7% investigable-bias threshold" at Abstract L11 and all other "US judicial" instances. Effort: 20 min.
- **ES-26 MED** Declination formula in Appendix D.3 — implementation is verified against Warrington (2018) but formal definition missing from Appendix D alongside EG and MM. Effort: 20 min.
- **ES-27 MED** Per-metric ESS in §5.4 — report ESS per metric (not a range 148–160); identify which metric carries p98.8. Effort: 30 min. (Overlaps S2-01.)

#### LOW (synthesis items 28–36)

- **ES-28 LOW** §E.7 v4-residual-gap collapse — collapse to 2-paragraph summary plus pointer to `analysis/methodology/commission_reference_shapes.md`. Effort: 30 min.
- **ES-29 LOW** Citation-format cleanup batch — Chen and Rodden 2013/2015 year resolution; neutral-form-first with SCR parallel consistently; Saskatchewan Reference form consistency; Warrington (2019) as primary at §5.2.4; *Rizzo* paragraph pin-cite. Effort: 1.5 h.
- **ES-30 LOW** Pincite and terminology pass — Courtney chs. 6–7 and 10–11 pincites; "independent" vs "non-partisan" terminology; EBCA section-level pincites for §12 and §15 invocations. Effort: 1 h.
- **ES-31 LOW** Unused/misaligned References — Sancton (2021) and Smith (2010) engage-or-remove; "The Argument" stale cross-reference check. Effort: 45 min.
- **ES-32 LOW** Statistical-presentation clarifications batch — §5.1.1 MAD-against-majority-mean footnote; §5.2.5 Chen-Rodden-vs-§5.4-ReCom disambiguation; §5.3.1 Calgary Zone A source-CSV cite; §5.6 Edmonton counter-test units; §4.1.2 Gate G1 SoV rounding verification. Effort: 1.5 h.
- **ES-33 LOW** Alberta Treasury Board 2024 estimate context — two sentences at §3.3 placing Alberta alongside Quebec/BC/Manitoba statutory-basis choices. Effort: 20 min.
- **ES-34 LOW** Abstract dimension numbering — fix (A, B, C, D, 4, 5) → (1)–(6) for consistency. Effort: 10 min.
- **ES-35 LOW** Abstract L9 assertiveness — footnote assertions to §5.3.2 evidence or switch to summary-phrase form. Effort: 15 min.
- **ES-36 LOW** §5.9.5 "implicate" → "be evaluated against". Effort: 10 min.

### Red-Team Code Corrections

Five HIGH findings still unfixed (from `red_team_code_fixes.md` §5):

- **HIGH-03** Magic-number bounding boxes in v4/v5 shape refinement — 40+ sites need conversion to fractional/centroid-relative coordinates with `Polygon.contains(Point)` asserts. Scope creep; deferred.
- **HIGH-05** Mixed RNG sources across Moran's I and Chen-Rodden tests — documentation fix only (state numpy version in docstrings). Not gate-blocking; deferred.
- **HIGH-06** 2015 region classification heuristic error-bounds — requires poll-level re-aggregation; out of code-fix scope. Deferred.
- **HIGH-08** Chrome `--no-sandbox` and `--virtual-time-budget` hardening — build-pipeline refactor; deferred.
- **HIGH-11** Suppressed-DA uncertainty accumulation — requires new per-ED "suppressed-DA pop share" column; moderate scope. Deferred.

Also deferred: MED-02, -04, -05, -06, -08 through -13 (policy/documentation). Rationale for all deferral decisions in `red_team_code_fixes.md`.

Numeric drift 0.05–0.09 pp on sensitivity endpoints from prior rounding corrections — headline numbers unchanged but prose must match.

### Manual Source Verifications

- RMH-Banff attribution — verify against Hansard/X-thread sources before CRIT-B deletion
- Public-support refutation scope — 3 items need manual cross-check

---

## HIGH — Pre-Submission

### Computational Pipeline (from master_plan.md)

These must run before Phase 4C results are used in reports:

- **C1 HIGHEST** Advance-vote splat — closes the 47.5% missing-vote gap. Input: `polls_2023_unified.csv` (ballot_type, voting_areas, ndp_votes, ucp_votes). Method: distribute each non-Election-Day poll's votes to its VAs proportionally by Election-Day share. Output: updated VA substrate with full 2023 vote totals (target: 1,706,304 two-party). Consequence: makes Phase 4C comparable to v0.2; likely resolves EG sign flip; raises NDP province-wide share from 42.60% to ~44.17%. Effort: 1–2 days.
- **C4 DONE** Third-party vote sensitivity — run via `third_party_sensitivity.py` 2026-05-09; see D1 entry above for results.
- **C5** Vote Anywhere exclusion — filter `polls_2023_unified.csv` for Vote Anywhere polls; exclude from VA substrate; quantify excluded vote total. Effort: 1 hour.
- **C6 DONE 2026-05-09** Sensitivity table re-run — same as CRIT-A; see that entry for results and files updated.
- **C2 SUPERSEDED** Overlap-zone fuzzing — superseded by official shapefiles (commit `873f4d0`). Spatial join against official polygons replaces v0_8 reconstruction uncertainty. No longer needed.
- **C3 SUPERSEDED** Edmonton-Beaumont parametric split — superseded by official shapefiles. The shapefile defines the boundary exactly; no parametric sweep needed.
- **C7 SUPERSEDED** Calgary-Airdrie overlap clip — superseded by official shapefiles. The official minority shapefile is the authoritative boundary; v0_8 Tier A clipping is no longer the canonical source. If overlap exists in the official shapefile it is the commission's intended boundary, not a reconstruction error.

### Spatial/GIS Outstanding (from master_plan.md)

- **G2 SUPERSEDED** Overlap-zone impact — superseded by official shapefiles; see C2.
- **G3** Advance-vote splat validation — after C1 build: compare pre/post-splat EG; if EG shifts >0.5pp, investigate which polls drove it. Effort: within C1.
- **G4 SUPERSEDED** Calgary-Airdrie overlap clip — superseded by official shapefiles; see C7.
- **G5 SUPERSEDED** Direct-rename area validation — with official shapefiles, area comparison should be done against official polygons via geopandas, not the v0_8 Tier A reconstructions. Superseded; replace with: run `geopandas` area check of official shapefile EDs against 2019 boundary areas for Method 0 EDs.

### Sentiment Analysis — LLM Classification

- **Corpus:** 1,252 published submissions (commission assigned 1,340 IDs across R1+R2; 88 withdrawn/not posted — confirmed absent from batch PDFs)
- **Keyword pass (complete):** `analysis/scripts/submission_sentiment_llm.py` — 76 tasks across 70 flagged submissions → `data/submission_sentiment_llm_results.csv`
- **Full-corpus scan (in progress):** `analysis/scripts/submission_sentiment_llm_full.py` — all 1,252 submissions; scan is running (~218/1,252 as of last log check 2026-05-09 ~19:51); output → `data/outputs/submission_sentiment_llm_full_results.csv`
- **OCR recovery (complete):** 23 image-only submissions recovered; stale progress rows pending cleanup
- **Cleanup needed:** Run `post_ocr_cleanup.py` after scan finishes — purges 10 stale OCR IDs from progress CSV, drops 5 false-positive result rows (EBC-2025-1-0082 classified on boilerplate)
- **Re-classify:** Re-run `submission_sentiment_llm_full.py` for the 10 purged IDs only (~3 min)
- **Hansard analysis (ready to run):** `analysis/scripts/hansard_sentiment_llm.py` — 188 R1 + 209 R2 = 397 community turns to classify; source files at `.temp/submissions/text/hansard_r1.txt` / `hansard_r2.txt`
- **Refactor:** Update `submission_sentiment_llm_full.py` to import from `analysis/utils/` (last script not using shared utils; can't modify while running)
- **Forensic pipeline:** After scan + Hansard complete: run `quote_verify_and_clean.py` → `validation_sample.py` → human review → `compute_kappa.py` → `cross_reference_submitters.py`
- **Cross-reference:** Final results against `minority_rationales_validation.md` Proposals A–F

### Fisher Empirical Independence Check

- **Script:** `analysis/scripts/szat.py` then `analysis/scripts/validate_fisher_independence.py`
- **Status:** Deferred — shapefile blocker now resolved (official shapefiles committed 2026-05-06); remaining blocker is full vote data (C1 advance-vote splat needed for complete VA substrate)
- **Blocker:** `data/szat_bootstrap_eg_samples.npy` does not exist; unblocked once C1 complete
- **Gate:** |ρ| < 0.30; activates CI test `test_fisher_channel_independence` automatically once .npy exists
- **Hard stop:** Do not submit paper while `fisher_independence_defense.md` shows "pending"

### URL Archival

- 13 priority URLs need Wayback Machine + archive.ph submission (authenticated browser session required)
- 6 additional SPN2 POST submissions needed (authenticated Internet Archive account)
- After submission: update `FROZEN_MANIFEST.md` and `private_workspace/url_archival_log.md` with snapshot URLs

### Editorial Factual Ambiguity

- Airdrie population framing (74,100 vs 84,000) — author clarification required before final draft. Recommendation: use 84,000 (2024 estimate) throughout to match commission's own 2024-vintage framing.

---

## MEDIUM — Pending Analysis

### Phase 4C Vision Assignment (Stages 3–7)

**Status: Superseded for spatial assignment; still needed for vote aggregation.**

Official shapefiles available (commit `873f4d0`, 2026-05-06). Vision API calls for polygon reconstruction (Stage 3) are no longer needed — VA-to-ED assignment can be done via direct spatial join against official shapefile polygons.

- **Stage 3 SUPERSEDED** — Replace 430 Vision API calls with: spatial join of `polls_2023_unified.csv` VA centroids against official `ea_minority_2026_eds.gpkg` / `ea_majority_2026_eds.gpkg`. Output: `assignment_va_to_2026_spatial_join.csv`. Effort: 2 hours (geopandas point-in-polygon).
- **Stage 4:** Aggregate spatial join output to CSV per 2026 ED. Output: `assignment_va_to_2026_aggregation.csv`.
- **Stage 5:** Group VA votes by 2026 ED; aggregate NDP/UCP/other totals. Output: `assignment_2026_synthetic_ed_totals.csv`. Note: requires C1 (advance-vote splat) first to fill 47.5% vote gap.
- **Stage 6:** Execute `packing_cracking_analysis.py` on Stage 5 data; generate updated B1–B6 metrics for all three maps.
- **Stage 7:** Run `monte_carlo_ci.py` on Stage 5 output; compute confidence intervals.
- **Blocker:** C1 (advance-vote splat) must run before Stage 5 — 47.5% of 2023 votes are non-Election-Day and currently excluded from `polls_2023_unified.csv`.
- **Note:** 2026-04-16 motion set aside commission proposals; reassess whether Stage 6–7 outputs are still needed for the publication target.

### Full 89/89 ED Resolution + Phase 5 Ensemble

- **89/89 EDs resolved** in both maps (session 12) — 13 via `crosswalk_split_default` fallback. The "86/89" figure in older docs is stale.
- **Shapefile blocker RESOLVED 2026-05-06** — `ea_majority_2026_eds.gpkg` and `ea_minority_2026_eds.gpkg` added to `data/shapefiles/canonical/` in commit `873f4d0`; Elections Alberta official shapefiles are now the canonical files
- Phase 5 ensemble, Stage 7 full-vote attribution, topology checksum, and population checks now unblocked
- Next: re-run ensemble with official shapefiles. Blocked on C1 (advance-vote splat) for full vote coverage.

### External Tool Validation (from external_tool_validation_plan.md)

- **Phase 1 (highest priority):** R `redist` package cross-validation — independently reproduce seats@50/50 finding. Effort: 1 evening setup + ~90 min runtime. Output: `external_validation_phase1_redist_results.md` + comparison table.
- **Phase 2:** QGIS visual inspection — ~~georegister v0_8 polygon reconstructions against commission maps~~ **SUPERSEDED:** official shapefiles now available (commit `873f4d0`). Use official `ea_minority_2026_eds.gpkg` / `ea_majority_2026_eds.gpkg` directly; compare against 2019 boundaries; inspect 6 contested EDs. No reconstruction georeferencing needed. Effort: 1 hour setup + 1 afternoon. Output: `external_validation_phase2_qgis_report.md` + overlays for Section C.
- **Phase 2.5 (14-day window):** Maptitude free-trial — cross-validate area/perimeter measurements. Effort: 4 hours setup + 2 hours QA. Output: Maptitude-to-Polsby-Popper comparison table.
- **Phase 3 (defer to journal submission):** ArcGIS publication-grade figures.

### Inter-Map Comparison Permutation Test (Ch1-COMP)

**Question:** Does the directional partisan-bias claim — minority map more UCP-biased than majority — reach classical significance on a comparison test, not just an absolute-position test?

**Honest prediction before running:** EG-only version likely fails (ensemble pair distances exceed 1.42 pp routinely). Mahalanobis joint version (all 4 metrics) has a realistic chance. Pre-commit to report regardless of direction.

#### Falsifiable hypothesis

**H₀ (null):** The minority and majority commission proposals differ in their joint partisan-metric position by no more than randomly drawn pairs of constraint-legal neutral maps. Formally: the Mahalanobis distance D(minority, majority) falls at or below the 95th percentile of {D(map_i, map_j)} for random pairs (i, j) drawn from the neutral ensemble.

**H₁ (alternative, one-tailed, direction pre-specified):** D(minority, majority) > 95th percentile of ensemble random-pair distances. Direction is pre-specified: minority is asserted to be more UCP-biased (higher EG in UCP-favourable direction, higher seats-at-50-50 for UCP).

**Falsification:** If D(minority, majority) ≤ 95th percentile, H₀ is not rejected. Paper then states: "The inter-map comparison does not reach classical significance on the paired-draw permutation test; the partisan-difference claim rests on directional sensitivity consistency (lower bound 0.47 pp above zero) and on each map's individual ensemble position rather than on a formally significant inter-map gap."

#### Test structure

**Test statistic — two versions:**

*Version A (EG-only, exploratory)*: T_EG = EG(minority) − EG(majority) = 1.42 pp observed. Null distribution: 10,000 random pairs from `simulated_ensemble_raw_samples_canonical.csv`; compute absolute EG difference for each pair. Critical value = 95th percentile of that distribution. Report p-value as fraction of pairs exceeding 1.42 pp.

*Version B (Mahalanobis joint, primary)*: T_M = (d^T Σ^{−1} d)^{0.5} where d = v(minority) − v(majority) is the 4-metric difference vector and Σ is the ensemble covariance matrix from `simulated_ensemble_raw_samples_canonical.csv`. Null distribution: compute T_M for 10,000 random pairs. Critical value = 95th percentile.

**Data inputs (all existing):**

- `data/simulated_ensemble_raw_samples_canonical.csv` — 100k neutral draws, columns: `efficiency_gap`, `mean_median`, `declination`, `seats_at_50_50`
- `data/simulation_real_map_scores_canonical.json` — real minority and majority metric vectors

**Implementation:** `analysis/scripts/intermap_permutation_test.py` — **written and ready**. Runtime: ~60 seconds (10k pairs from 100k-row CSV). Output: `analysis/reports/intermap_permutation_test_results.json` + `.md`.

**Pre-registration requirement:** Pre-register H₀, H₁, Version A/B, and the pre-commitment to report regardless of direction in OSF before running. Alternatively, label result explicitly as exploratory and cite this TODO entry as the pre-analysis plan. Do not run without this on record.

**Paper impact:**

- Positive result → add to §5.4 as "Ch1-COMP: inter-map comparison test, p < 0.05" — directly addresses the directional claim at classical threshold
- Null result → add paragraph to §5.4 noting the limit: "classical significance applies to each map's absolute ensemble position, not to the inter-map comparison; direction is established by sensitivity consistency"

---

### Open GitHub Challenges (Issues #13 and #14)

- **MCMC-13 — 2019-seeded ensemble** (GitHub Issue #13): Seed the ReCom chain from the 2019 enacted geometry instead of a random start, restricted to single-boundary moves, population-target-preserving swaps, and COI-preserving proposals. A chain anchored at the enacted baseline more directly models incremental commission drawing and may place both 2026 maps differently within the ensemble distribution. Effort: 2–3 days implementation + ~90 min compute. Referenced in `retraction_pathway.md` §7.2 and README.md §Known Limitations.

- **COUNTER-14 — Counter-map challenge** (GitHub Issue #14): Retraction condition for §5.8.5 anchoring finding. Produce a constraint-legal 89-seat Alberta map satisfying the minority's stated COI rationales (Airdrie ≤2-way split, Cochrane–NW connection, RMH without Banff Park extension, Nolan Hill–Cochrane preserved) AND achieving majority-comparable municipal-boundary anchoring (CSD/DA edge alignment ≥60%). Requirements: official shapefiles, EBCA statutory population band (±25%; −50% for §15(2) EDs), no Enoch Cree–Devon pairing without documented rationale. Status: open; no counter-map submitted as of 2026-05-10. If a qualifying counter-map is produced, §5.8.5 retracts. Filed in `retraction_pathway.md` §4 Statutory Silence.

- **338-RETRO — Historical polling sensitivity** (Track E extension): Use the 77 historical 338Canada snapshots in `data/reference/338canada_historical_snapshots.csv` to reallocate both 2026 maps across the full polling range via the audit's crosswalk. Find the crossover pp level where the minority-vs-majority seat direction flips and characterize the width of the direction-stable zone. Output: updated `analysis/methodology/338canada_historical.md` with crossover estimate. Effort: 2–3 hours adapting `338canada_reallocate.py`.

---

### Data Source Gaps (minority_rationales_validation.md Proposals A–F)

**StatsCan Journey-to-Work (98-10-0459 series):**

- Already downloaded: Cochrane CSD origin table (`cochrane_journey_to_work.csv`, 27 destination rows aggregated from StatsCan 98-10-0459) — supports R1: 49.2% work within Cochrane, 35.8% to Calgary, 4.0% to Rocky View
- Missing: Airdrie, Chestermere, Sylvan Lake, Innisfail, Red Deer origin-CSD tables
- Impact: R2 (Chestermere), R5 (Springbank), R11 (Sylvan Lake) verdicts are currently INCONCLUSIVE; specific flow data would resolve them
- Action: Download from StatsCan ODESI or custom order via 98-10-0459-01-eng.zip filter by origin CSD

**Alberta Legislative Assembly Hansard:**

- This is the legislature/committee Hansard (debates about the bill), not the EBC public hearing transcripts (already in `.temp/submissions/text/hansard_r1.txt` / `hansard_r2.txt`)
- Needed to verify RMH-Banff attribution (CRIT-B) and source Nenshi/Wesley quotes (HIGH-D, HIGH-E)
- Status: Access restrictions on Hansard search. Workaround: manually search `assembly.ab.ca/adr/hansard` for specific session dates.

**CBC articles:**

- No data files exist; paywalled
- Impact: context for D-section public figures' statements; non-critical if Hansard quotes are sourced
- Workaround: search CBC accessible via Google cache / web.archive.org for specific article URLs

---

## MEDIUM — Restructure / Hygiene

### analysis/ Directory Restructure

Three-phase execution (PO-approved 2026-04-23):

- **Phase A (2–3 hours):** 12 zero-reference files — move to correct directories; validate imports
- **Phase B (6–8 hours):** ~45 files with 1–2 references — move in batches; grep-replace cross-references after each
- **Phase C (8–10 hours):** 15 high-risk files with 3+ references (shape_refinement.py: 140 refs; packing_cracking_analysis.py: 114; mcmc_ensemble.py: 101)
- **Phase D (2–3 hours):** Verification — ast.parse all moved .py; grep for stale paths
- **Awaiting:** execution trigger from PO

### Remediation Hygiene Track (Phases 3–5)

Deferred after Safety Track completion:

- Constants module, ED name resolver, god function decomposition
- `sys.path` removal, `data_loader` abstraction, `mcmc_runner` consolidation
- `ruff` config + `mypy`, `iterrows` migration, TypedDict types

### Paper Methodology Section — Fisher Defense Language

- `analysis/methodology/fisher_combination_defense.md` — AV2–AV8 responses ready to copy into supplementary materials or referee response letter

---

## Date-Gated (External Events)

- **Track A (shapefile integration):** Unblocked 2026-05-06 (commit `873f4d0`; not 2026-05-09 as earlier drafts stated). Integrate official Elections Alberta shapefiles; re-run Phase 5 ensemble, spatial metrics, topology checksum. Blocked on C1 (advance-vote splat) for full vote coverage before ensemble re-run.
- **Track C (Nov 2, 2026 committee):** Government may table 91-seat map. Trigger: run full pre-registered checklist on new proposal within 48 hours of tabling (population equality, packing/cracking, spatial audit).
- **Track E (338Canada refresh):** Every 60–90 days; next due ~late June 2026. Re-run `338canada_scraper.py` and `338canada_reallocate.py`; update public report if projection moves >0.5pp.

---

## External Blockers

- **OSF pre-registration disclosure gap** — Ch1 (Mahalanobis) and Ch2 (SZAT) are not named in any of the four pre-registered files (w2s8k/r3zm7/qsgy8/6pt83). Registrations cover drain test (Ch3) and DPG v11 methodology only. Paper must disclose this gap in §3.7. Note: registration 6pt83 (timestamped ~3h after shapefile commit 873f4d0 on 2026-05-07) cannot be treated as pre-dating the data; w2s8k/r3zm7/qsgy8 predate by ~2.5h.
- **November 2026 committee deadline** — drives publication target

---

## Done

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
- OSF file content verified 2026-05-09 — `dpg2_experiment_plan.md` (DPG v11, H1–H5, T-A–T-D) and `drain_v2_plan.md` (§5.3.5 drain test) confirmed; neither contains Mahalanobis/SZAT/P/C/E criteria (confirms S1-01; see External Blockers for disclosure requirement)
- Academic reorganization (voice check PASS, FK 12.9, completed 2026-04-23)
- Editorial three-voice pass (FK 10.0 → 10.6, completed 2026-04-22)
- Outreach to Elections Alberta + Duane Bratt — replies received 2026-05-09
- Sentiment analysis architecture: 4 utils modules (sentiment_config, source_loader, quote_verifier, claude_client); 11 scripts refactored; Hansard parser with participant allow-list; forensic quote verification pipeline
- OCR recovery: 23 image-only submissions recovered via PyMuPDF + EasyOCR; `post_ocr_cleanup.py` created
- Phase 4C VA assignment: 89/89 EDs resolved in both maps (session 12); 13 EDs via `crosswalk_split_default` fallback; Edmonton-Beaumont/Highlands-Norwood direct-override fix

---

## Planning Docs — Flagged for Deletion

These documents' outstanding content is now consolidated above. After confirming nothing was missed, delete:

| File | Reason |
| --- | --- |
| `analysis/methodology/master_plan.md` | All open D/S/G/C items now in CRITICAL and HIGH sections above |
| `analysis/methodology/assignment_runbook.md` | Stage 3–7 procedure now in Phase 4C section above |
| `analysis/methodology/assignment_execution_log.md` | Stage status now in Phase 4C section above |
| `analysis/methodology/external_tool_validation_plan.md` | All three phases now in External Validation section above |
| `analysis/red_team/archival_submission_queue.md` | URL archival task now in HIGH section above; specific URLs should be retained in `FROZEN_MANIFEST.md` or `private_workspace/url_archival_log.md` before deletion |
| `analysis/methodology/restructure_inventory.md` | Phase A–D tasks now in Restructure section above |
| `private_workspace/migration.md` | Track C and Track E now in Date-Gated section above |
| `analysis/methodology/editorial_pass_log.md` | Completed log; no outstanding items; factual ambiguity flag already in TODO |
| `REMEDIATION_LOG.md` | Safety Track complete; open items already in Remediation Hygiene section above |

**Do NOT delete (content, not plans):**

- `analysis/red_team/red_team_assertions.md` — assertion inventory is a reference document; fixes are summarized above but original assertions may be needed for referee response
- `analysis/red_team/red_team_code_fixes.md` — deferred HIGH/MEDIUM rationale belongs here; keep until fixes are complete
- `analysis/methodology/minority_rationales_validation.md` — scientific findings
- `analysis/meta/FROZEN_MANIFEST.md` — canonical file manifest
- All methodology, findings, and defense documents
