---
name: Science red-team — S1 (pre-registration), S2 (statistical validity), S9 (claim calibration)
description: Peer-review-standard red-team of the Alberta Electoral Boundaries Audit on the three science-framework dimensions most exposed to methods-paper criticism. Uses git history, raw CSV arithmetic, and the ESS/autocorrelation JSON produced by the 100k MCMC run to grade the audit's design, statistical validity, and claim calibration. Companion to the legal red-team pass; does not duplicate quotes / provenance / script reproduction work done there.
forward_dependencies:
  - analysis/v0_1_science_red_team_reproducibility_and_falsifiability.md (S3, S4, S5, S8)
  - analysis/v0_1_science_red_team_data_priorart_peerreview.md (S6, S7, S10)
  - report_academic.md (findings in this file will be consumed before release sign-off)
backward_dependencies:
  - analysis/v0_1_science_red_team_framework.md (dimension definitions, severity scale)
  - analysis/v0_1_legal_red_team_framework.md (shared severity language, overlap points)
  - report_academic.md, analysis/v0_1_mcmc_ensemble.md, analysis/v0_1_track_c_checklist_baseline_scoring.md, analysis/v0_1_pre_registration_draft.md, analysis/v0_1_canadian_base_rate_computed.md, analysis/v0_1_majority_symmetry_counter_test.py
  - data/v0_1_mcmc_*.csv, data/v0_1_mcmc_convergence_diagnostics_100k.json, data/v0_1_canadian_redistribution_base_rate.csv
---

# Science red-team — design, statistics, and claim calibration

**Date:** 2026-04-23
**Reviewer posture:** methods-paper peer review (candidate venues: *Election Law Journal*, *Statistics and Public Policy*, *PNAS Nexus*). Findings are graded at the severity a careful reviewer would assign in a first-round review.
**Scope:** S1 (experimental design / pre-registration), S2 (statistical validity), S9 (claim calibration). All three dimensions overlap and the cross-cutting issues (MCMC ESS, multiple-comparison burden, p100 language) are discussed under whichever dimension they bite hardest.

---

## Status update — 2026-04-23 (post-T0/T1/T2 remediation)

Authoritative current-state view of the findings in this file against the remediation commits that landed 2026-04-23 (d25e659 T0, a62eb53 T1, de7c48e T2, afb3a4a + 3b7dbfb session-12 data pipeline).

| Finding | Status | Fix location |
|---|---|---|
| S1-01 (CRITICAL) "2h24m separation" provenance claim is false | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual release-blocker — the §3.7 provenance paragraph still needs correction. |
| S1-02 (HIGH) Submission-keyword list pre-dates checklist | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S1-03 (HIGH) E2 reformulation / optional-stopping pattern | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual (disclosure already present in-paper; formal OSF custody pending). |
| S1-04 (HIGH) Counter-test caveat propagation | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S1-05 (MED) Track-C baseline chronology disclosure | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S2-01 (CRITICAL) MCMC ESS ≈150, not 10,000 — p100 over-claims precision | ADDRESSED | a62eb53 §5.4 explicit ESS-150 tail downgrade paragraph: raw p100/p1.6 bounded to p95.35/p2.5 at chain effective precision; minority seats-at-50/50 retracted to p89.72. Directly implements the S2-01 recommendation. |
| S2-02 (CRITICAL) 100k full-coverage rescore contradicts §3.11 headline | ADDRESSED | afb3a4a + 3b7dbfb rewire Phase 4C + MCMC rescore to canonical shapefiles (`data/v0_1_canonical_{majority,minority}_2026_eds.gpkg`); Advance-Vote Splat wired in with two-party total 1,706,249/1,706,233 against target 1,706,304; 2019 EG sign now matches paper's documented −2.64%. a62eb53 ESS downgrade further aligns reported percentiles with effective precision. |
| S2-03 (HIGH) No family-wise error-rate control across 21 tests | ADDRESSED | de7c48e §6 Discussion adds explicit paragraph naming FWER concern, explaining why Bonferroni/BH is the wrong response for a consistency-of-correlated-dimensions frame; documents Katz-King-Rosenblatt (2020) + Altman-McDonald (2011) authority for the choice. Implements S2-03 remediation #1 verbatim. |
| S2-04 (HIGH) B4 uniform-swing violation not quantified | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S2-05 (HIGH) Canadian base-rate "71st percentile" circular | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S2-06 (MED) MC direction-consistency CI not reported | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S2-07 (MED) Declination implementation verified correct (docstring nit only) | NOT ADDRESSED | Not in T0/T1/T2 scope; LOW-effort residual. |
| S2-08 (LOW) Base-rate CSV column ambiguity | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S9-01 (CRITICAL) "p100" / "every one of 10,000" over-claims | ADDRESSED | a62eb53 ESS-150 tail downgrade directly rewrites p100/p1.6 → p95.35/p2.5; d25e659 Abstract + §5.2.7 two-measurement reframing (−1.42pp vs +4.15pp as systematic spatial-resolution sensitivity). Together these implement S9-01's "ESS-adjusted language" fix. |
| S9-02 (HIGH) "Three formal signatures" tighter than evidence | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual release-blocker per the file's own classification. |
| S9-03 (HIGH) "Six dimensions" collapses to four families | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S9-04 (MED) "One to three seats" range structural disclosure | PARTIAL | d25e659 §5.2.7 two-measurement framing (blended crosswalk −1.42pp vs high-res spatial +4.15pp) provides structural range explanation at the measurement-sensitivity level; explicit public-report rewrite per S9-04 recommendation still pending. |
| S9-05 (MED) "71st percentile" framing — tied to S2-05 | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| Implicit finding — Gill v. Whitford mischaracterization | ADDRESSED | d25e659 corrects Gill v. Whitford language in 4 places (SCOTUS vacated/remanded on standing; did not adopt 7% threshold). |
| Implicit finding — Rizzo citation form | ADDRESSED | d25e659 corrects Rizzo universally to *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 S.C.R. 27. |
| Implicit finding — sign-convention ambiguity (EG/MM/declination) | ADDRESSED | a62eb53 §4.3 universal sign-convention glossary (negative = UCP advantage, positive = NDP advantage). |
| Implicit finding — Core-vs-Margin VA sensitivity for MCMC | ADDRESSED | a62eb53 §5.2.7 Core-vs-Margin VA partition: ~8–12% of two-party votes in Margin VAs (±500m of DPG boundary or crosswalk fallback); max swing at risk ±1.5pp. |
| Implicit finding — Chair-claim public-support overclaim | ADDRESSED | d25e659 §5.9.4 softens to "materially overstates the absence of public support." |

Historical finding records in the rest of this file remain unchanged for audit-trail continuity; this section is the authoritative current-state view.

---

## Summary table

| ID | Severity | Dimension | File / section | One-line finding |
|---|---|---|---|---|
| S1-01 | **CRITICAL** | S1 | `report_academic.md` §3.7 pre-registration provenance paragraph | The v1.2 prompt's commit `5b0bc06` does NOT contain P/C/E criteria; those criteria first appear in commit `282bc6d` (the same commit as the detection run). The paper's "2 hours 24 minutes of separation" is incorrect; the specification and the detection are co-temporal. |
| S1-02 | **HIGH** | S1 | §5.4 submission-search; `analysis/submission_search.py` build_patterns | Submission-archive keyword list (seven regex patterns) was created in commit `42d2925` **before** the `"what a gerrymander would look like"` checklist was written (`2838028`). S6 of the checklist depends on a keyword classification whose rules were fixed pre-checklist; pattern-shaping during the 88-comment manual-review stage is a researcher degree of freedom that was not disclosed. |
| S1-03 | **HIGH** | S1 / S9 | §3.9 E2 reformulation | E2 was reformulated from "narrow eligibility" to "substantive choice-over-alternatives" after the §15(2) re-audit showed the narrow test would fail. Disclosed in-paper, but the reformulation fits the Hauke–Kerridge optional-stopping pattern (rule changed after observing data crossed the threshold). Keeping the signature in the formal count without an external committed criteria set risks Type-I inflation in the three-signature headline. |
| S1-04 | **HIGH** | S1 / S9 | §3.13 counter-tests (Lethbridge, Red Deer 4-way splits) | Paper acknowledges "specified and executed in the same analytical pass" and excludes them from the formal signature count. Caveat is present but the adjacent §3.10 "signatures summary" table and the §7 synthesis still list "three formal signatures"; if these counter-tests were added, the count would be five, and the §3.12 checklist's S2 "new signatures appear beyond the minority's set" result would change from "0 new" to "2 candidate new." Keep current caveat, but flag that the paper's `S2 = 0` claim is partly an artefact of the separation rule. |
| S1-05 | **MED** | S1 | `analysis/v0_1_track_c_checklist_baseline_scoring.md` | The Track-C baseline scoring was committed `59d5984 2026-04-22 13:13:48` — after the packing/cracking detection (`282bc6d 10:56:11`) and after the submission-search tier analysis (`339b72e 10:11:27`). The checklist was written with knowledge of how the 89-seat maps would score; "pre-registered for the November map" is correct but "calibrated before looking at the data" is not. |
| S2-01 | **CRITICAL** | S2 | §3.11 MCMC headline percentiles | `data/v0_1_mcmc_convergence_diagnostics_100k.json`: autocorrelation time τ = 624–674, **effective sample size per metric = 148–160**. The paper reports p100 on mean-median and seats-at-50/50 against "10,000 alternatives" but the effective independent sample is ≈150. The p100 claim is statistically ≈ one-effective-sample resolution; the defensible language is p ≥ 95 or "no observed sample was more extreme." |
| S2-02 | **CRITICAL** | S2 / S9 | §3.11 MCMC headline percentiles | The untracked `data/v0_1_mcmc_ensemble_percentiles_full_100k.csv` (100k samples, full-coverage rescore) **already exists** and produces materially different numbers: minority mean-median p98.76 (not p100), minority seats@50/50 **p94.27** (below the 95 threshold; no longer an outlier), majority mean-median **p92.66** (paper says p6.6 — opposite tail), majority seats@50/50 **p57.86** (paper says p1.7 — no longer NDP-favoured outlier), minority declination **p1.56** (strongly NDP-favoured by declination). The paper's §3.11 headline is stale. |
| S2-03 | **HIGH** | S2 | §3.3, §3.4, §3.5, §3.11, §3.12 — family of tests | The audit runs at least 13 distinct statistical tests on overlapping 2023 vote data (listed in §"Explicit test inventory" below). No family-wise error-rate control is reported. Under Bonferroni at α=0.05, per-test threshold is 0.0038; under Benjamini-Hochberg, at least one claimed finding (the MCMC p100 claim) does not survive when corrected. |
| S2-04 | **HIGH** | S2 | §3.3 B4 seats-at-50/50 uniform-swing assumption | The paper notes the 2019→2023 swing was not uniform (NDP gained more in Edmonton than Calgary) but does not quantify the consequence for the seat-count headline. A non-uniform swing analysis against observed 2019→2023 regional deltas would shift the B4 central estimate by an untested amount; the audit should compute it. |
| S2-05 | **HIGH** | S2 | `analysis/v0_1_canadian_base_rate_computed.md` | Compression factor 0.455 is calibrated from **n=1 data point** (Alberta 2025–26 itself). The claim "Alberta sits at the 71st percentile of the Canadian distribution" is then computed against a sample that *includes the anchor cycle*, creating a circularity. Recomputed percentile excluding the anchor (n=6): Alberta's 0.51 pp sits above three of six (Alberta 2017 0.52, Manitoba 2018 0.80 at or above; BC 2023, SK 2022, Federal-AB 2022, Alberta 2010 all at 0.00). That is ≈ 50th percentile among non-Alberta cycles, not 71st. |
| S2-06 | **MED** | S2 | §3.5 Monte Carlo CI | The "90.5% direction consistency in 2,000 MC samples" is reported but the 2,000 samples share the same underlying vote data and crosswalk — it is a modelling-uncertainty estimate, not a sampling-uncertainty estimate. The 90.5% figure's CI is `binomial(n=2000, p=0.905)`, so ±1.3 pp at 95% confidence: i.e., 89.2–91.8% direction consistency. The paper reports the point estimate only. |
| S2-07 | **MED** | S2 | `analysis/v0_1_mcmc_ensemble.py` declination | Verified against Warrington (2018) Eq. 2 and the author's reference Python (arXiv 1803.04799). The audit uses `atan2(mean_ucp_in_ucp_won − 0.5, R/(2n))` which algebraically equals Warrington's `arctan((1 − 2·mean_Rwin) · n/R)` up to a global sign flip that also propagates through theta_D and cancels in `(theta_R − theta_D)`. Implementation is mathematically equivalent. No finding other than: add a unit test against a published Warrington benchmark to lock in reproducibility. |
| S2-08 | **LOW** | S2 | `data/v0_1_canadian_redistribution_base_rate.csv` | Column `seats_changed_between_a_and_b` is `3` for the Alberta 2025–26 anchor while the paper uses `Δs=1`. Different concepts (boundary-changed EDs vs. partisan-winner-flip seats) but same column name; a peer reviewer will ask. Add a second column or rename. |
| S9-01 | **CRITICAL** | S9 | §3.11, §7 synthesis, public-report headlines | "p100" and "more UCP-favoured than every one of 10,000 alternatives" both over-claim precision. The defensible version is "p ≥ 95 within an MCMC ensemble of effective sample size ~150 per metric" or "no observed sample among the 10,000 was more UCP-favoured; a one-effective-sample tail statement." The current magnitude language does not survive the ESS diagnostic. |
| S9-02 | **HIGH** | S9 | §3.10 "three formal signatures detected" | With E2 reformulated mid-audit (S1-03), calling the RMH-Banff Park finding a "formal" signature where "formal" implies "passed pre-registered thresholds" is tighter than the evidence. Replace "formal" with "three signatures on the reformulated test set" or "two formal (Airdrie cracking, Calgary Zone-A packing) plus one reformulation-dependent (RMH-Banff Park)." |
| S9-03 | **HIGH** | S9 | Abstract / §7 "directional consistency across six dimensions" | The six dimensions are not independent: §A1 (MAD), §A2 (Calgary zone), §A2b (rest-of-province population), and the §A3 counterfactual are all population-math tests that collapse into a single "wider population dispersion in minority" finding. The honest count is four independent families: population-math (collapses A1/A2/A2b/A3), partisan-bias (B2/B3/B4/B6 — themselves entangled, see §3.5.1), spatial (C3/C4), procedural (D). The paper's own §3.5.1 admits B2/B3/B4 are closely related; the same collapsing should be applied symmetrically to the A-family. |
| S9-04 | **MED** | S9 | Public report "one to three seats" | The paper (§3.5, §7) and public report frame the seat-count range; the public report's headline of "one to three" needs explicit disclosure that "three" is a Monte-Carlo 95% upper bound, not a central estimate. At the central (0.70 urban weight) case the gap is 1 seat; the 3-seat end comes from the 2,000-sample jitter. Currently presented as a range without that structural explanation. |
| S9-05 | **MED** | S9 | §3.5 Canadian base rate framing | The paper phrases the result as "Alberta 2025-26 is in the minority of Canadian redistribution cycles that produce any inter-map partisan-winner asymmetry." That is defensible. What is NOT defensible is the "71st percentile" number (see S2-05); it should be dropped in favour of "three of seven cycles show non-zero asymmetry; Alberta is among them at the middle of the three." |

**Severity counts:**

| Dim | CRITICAL | HIGH | MED | LOW |
|---|---:|---:|---:|---:|
| S1 | 1 | 3 | 1 | 0 |
| S2 | 2 | 3 | 2 | 1 |
| S9 | 1 | 2 | 2 | 0 |
| **Total** | **4** | **8** | **5** | **1** |

---

## S1 — Pre-registration findings (detail)

### S1-01 CRITICAL — P/C/E criteria were NOT pre-registered in commit 5b0bc06

The paper's §3.7 "Pre-registration provenance" paragraph claims:

> *"The P/C/E criteria and their numeric thresholds are specified in `v1_2_gerrymander_audit_prompt.md`, committed as `5b0bc06` at 2026-04-22 08:32:20 −06:00. The signature-detection analysis reported in §3.7–3.9 was committed as `282bc6d` at 2026-04-22 10:56:11 −06:00. The criteria exist in the repository 2 hours 24 minutes before the detection runs."*

Verified via `git show 5b0bc06:v1_2_gerrymander_audit_prompt.md`: commit `5b0bc06` contains no P1/P2/P3, C1/C2/C3, or E1/E2/E3 specifications. The `## Packing and Cracking Signature Revelation` section containing the numeric criteria was added in commit `282bc6d` (`git show 282bc6d -- v1_2_gerrymander_audit_prompt.md` shows the criteria being introduced as `+` lines in the same commit that produced the detection run).

The actual separation between criteria specification and detection run is therefore **zero minutes**, not 2 hours 24 minutes. The paper's provenance claim is false in its precise form. A peer reviewer who checks `git show` will flag this immediately, and the finding does damage to the entire §3.7–3.10 pre-registration framing.

**Recommendation.** Three concurrent fixes:
1. Retract the "2 hours 24 minutes" claim in §3.7 verbatim and replace with "The P/C/E criteria and the signature-detection analysis were committed in the same commit (`282bc6d`). The only temporal separation between criteria-specification and detection-run is intra-session (order of operations within one commit). The November-map pre-registration (`analysis/v0_1_pre_registration_draft.md`) is the remediation that closes this gap for future scoring; the 89-seat-map signatures should be characterised as 'retrospectively defined' not 'pre-registered.'"
2. In §3.10 summary, replace "three formal signatures" with "three retrospectively-defined signatures" until OSF submission is complete.
3. Add explicit statement that S1-derived findings become pre-registered from the OSF submission date forward, not backward.

### S1-02 HIGH — Submission-archive keyword list was created before the checklist

`git log --all --follow analysis/submission_search.py` shows creation in commit `42d2925 2026-04-22 08:58:29`. The "What a gerrymander in the 91-seat map would actually look like" checklist — which contains S6 (publicly-supported configurations dropped / unsupported ones kept) — was written in commit `2838028 2026-04-22 11:02:06`. That is **two hours after** the keyword list shipped and the submission-archive search ran.

S6 is scored using the public-support tiers produced by `submission_search.py`. If the checklist had been written first, a reviewer could check whether the keyword patterns were shaped to the checklist's needs. As-is, the keyword patterns were shaped to the exercise "refute the chair's Appendix C claim" and the checklist was retrofitted to use the tier outputs. The 13 manual-review corrections (documented in `deprecated/submission_search_log.md`) are a researcher-degree-of-freedom vector: the classification heuristic's support/oppose regex was the output, but the 13 hand-corrections were inputs to the final tier table without a committed rule for how ambiguous classifications got reassigned.

**Recommendation.**
1. Treat S6 in the baseline scoring as "retrospectively defined on the keyword-search output" and explicitly state that the November map's S6 scoring will use the frozen keyword set plus a pre-declared re-classification rule (e.g., "any ambiguous-leaning-support classification re-scored as supporting only if the snippet names the configuration explicitly").
2. Commit the 13 manual-review corrections as a separate CSV with an explicit rule for each.
3. For the OSF pre-registration, add the full keyword regex list and the classification heuristic to the pre-registration document so that "criteria custody" is held for the November scoring.

### S1-03 HIGH — E2 reformulation fits the optional-stopping pattern (disclosed, but requires handling)

§3.9 discloses: *"The E2 criterion was initially framed as a statutory-eligibility test ('without extension, ED would not qualify') and the §15(2) re-audit against corrected thresholds failed that narrow test. On review the test is reformulated to match the signature the audit was actually trying to measure."*

Disclosure is to the audit's credit. The structural question, however, is whether the reformulation — rule changed after observing that the narrow test would fail — is *distinguishable* from optional stopping. Under Hauke & Kerridge, optional stopping is present when: (a) a pre-specified rule's result would have been unfavourable; (b) the rule is changed so the result is favourable; (c) both rules are defensible a priori; (d) the change is disclosed but treated as a methodological improvement rather than an erosion of the inferential guarantee.

The audit meets all four conditions. The §3.9 justification ("the substantive test is the correct one," grounded in *Rizzo v. Rizzo Shoes*'s purposive principle) is a defensible a-priori substantive reformulation — but it is also exactly what an optional-stopping pattern looks like when the investigator has a good argument for the switch. The protection against this class of inference inflation is *pre-registered external custody* of the test definition, which the audit does not have for its own 89-seat-map scoring (it is in preparation for the November map via OSF).

**Recommendation.**
1. Keep the E2 reformulation and its disclosure. The disclosure is strong practice.
2. In §3.10 and §7, qualify the "three signatures" count explicitly: "Airdrie cracking and Calgary Zone-A packing are signatures under the pre-commit criteria; the Rocky Mountain House-Banff Park engineered-boundary signature is scored on a mid-audit reformulated E2 and should be read as 'signature under the reformulated substantive test.'"
3. Add the reformulated E2 criteria to the OSF pre-registration's S1 definition so the November scoring runs against the committed version.

### S1-04 HIGH — §3.13 Lethbridge / Red Deer counter-tests: caveat is present but not fully propagated

§3.13 says: *"The counter-test framework was specified and executed in the same analytical pass ... these two cracking candidates are therefore held separately from the Airdrie cracking signature in §3.8."*

The caveat is correct and strong. Two propagation gaps:

1. In §3.10 "Signatures summary" table, Lethbridge and Red Deer do not appear at all. If they were included, they would be "detected (cracking-candidate)" rather than "not applicable." A reviewer looking at the table alone would not know the counter-tests exist.
2. In §3.12 Track-C scoring, the S2 signal ("New signatures appear beyond the minority's set") is scored **0** for both maps. But Lethbridge 4-way and Red Deer 4-way are precisely "new signatures beyond the minority's Airdrie/Calgary/RMH set." Scoring them as 0 because they were found in the same pass as the counter-test is consistent with the caveat, but the aggregate scorecard inherits the "3 signatures, no new ones" pattern from a boundary condition the reader has to reconstruct.

**Recommendation.**
1. Add a row to the §3.10 table: "Cracking-candidate (Lethbridge 4-way, Red Deer 4-way)" with "Detected (held separately, pending C-threshold run)" in the minority column and "Not detected" in the majority column.
2. In §3.12, add a footnote to the S2 row noting that if the counter-test patterns were treated as pre-registered signatures the count would be 2 new, and cite §3.13 for the reason they are held separately.

### S1-05 MED — Track-C baseline scorecard was written after both detection and refutation runs

Chronology (verified via `git log --follow --format='%h %ci'`):
- `5b0bc06 2026-04-22 08:32:20` — v1.2 prompt (no P/C/E yet)
- `42d2925 2026-04-22 08:58:29` — submission-search refutation run complete
- `282bc6d 2026-04-22 10:56:11` — P/C/E criteria introduced, detection run complete
- `339b72e 2026-04-22 10:11:27` — tiered refutation paper text
- `2838028 2026-04-22 11:02:06` — checklist written into `report_public.md`
- `59d5984 2026-04-22 13:13:48` — Track-C baseline scoring executed

Every element of the checklist's scoring was known before the checklist was written. The self-calibration paragraph in `v0_1_track_c_checklist_baseline_scoring.md` ("Running the checklist against the two maps whose content is already known confirms the checklist distinguishes them in the expected direction") is candid about this. The residual concern is that a reader who does not trace the commits will assume the checklist was drafted before the scoring exercise.

**Recommendation.** Add a one-paragraph "chronology" note at the top of `v0_1_track_c_checklist_baseline_scoring.md` listing the commit timestamps in order, with the framing "The checklist was drafted with full knowledge of the 89-seat scoring outputs; its methodological guarantee applies to future maps (November) and not to the baseline scoring on the two maps whose content was already known."

---

## S2 — Statistical validity findings (detail)

### Explicit test inventory (for multiple-comparison count)

Listed here per the framework requirement. Each row is a distinct statistical test run on the 2023 Statement-of-Vote or a derivative of it. Tests that re-use the same hypothesis with different parameters are counted once but noted.

| # | Test | Sample | Report section | Status vs null |
|---|---|---|---|---|
| 1 | A1 MAD difference (majority vs minority) | 89 EDs × 2 maps | §2.1 | Descriptive, no null framing |
| 2 | A2 Calgary zone-gap (geographic rule) | ≤29 Calgary EDs × 2 maps | §2.2 | Descriptive |
| 3 | A2 robustness (2023-winner-based) | same EDs × 2 maps | §2.2 | Replication of #2 |
| 4 | A2b rest-of-province mean | 38–40 rural EDs × 2 maps | §2.3 | Descriptive |
| 5 | B2 Efficiency gap at urban weight 0.70 | 89 EDs × 2 maps | §3.3 | No explicit null |
| 6 | B2 sensitivity at w=0.60, 0.80 | 89 × 2 × 2 | §3.4 | Replication of #5 |
| 7 | B3 Mean-median | 89 × 2 | §3.3 | No explicit null |
| 8 | B4 Seats-at-50/50 | 89 × 2 | §3.3 | No explicit null |
| 9 | B6 Declination | 89 × 2 | §3.4 | No explicit null |
| 10 | MC 2000-sample directional-consistency | 2,000 samples | §3.5 | 90.5% direction; no binomial null |
| 11 | 2019 cross-election check (3-way: 2015, 2019, 2023) | 87 EDs × 3 elections × 2 maps | §3.5 | Direction-invariance null |
| 12 | 338Canada historical stability (77 snapshots) | 77 snapshots × 2 maps | §3.5 | Direction-invariance null |
| 13 | MCMC ensemble (10k + 100k) × 4 metrics × 3 maps | 10k or 100k samples × 4 × 3 | §3.11 | Tail-percentile null |
| 14 | Counter-test Edmonton zone gap | 21 EDs × 2 maps | §3.13 | Signature null |
| 15 | Counter-test city-wide 4-way splits | 8 cities × 2 maps | §3.13 | Signature null |
| 16 | Chen-Rodden neutral ensemble (150 plans) | 150 plans | §3.6 | Mechanism null |
| 17 | Submission-archive keyword-match rates | 1,252 submissions × 7 configs | §5.4 | Per-config proportion null |
| 18 | CSD community-split count | 191 CSDs × 3 maps | §4.4 | Count null |
| 19 | Compactness (Polsby-Popper, Reock) | 57–70 EDs × 2 maps | §6.7 | Count null |
| 20 | Canadian base-rate percentile | 7 cycles | §3.3 | Percentile null |
| 21 | Cycle-lag ±25% drift (5 of 87 / 0 of 89 / 5 of 89) | 87 or 89 EDs × 3 maps | Preamble §2.1 | Count null |

**Total: 21 distinct statistical tests on overlapping 2023-derived data** (some tests use 2019 or 2015 substrate, but the headline findings are 2023-based). No family-wise error-rate correction is reported. Under Bonferroni, per-test α = 0.05/21 = 0.0024. Under Benjamini–Hochberg with 21 tests, the 5th smallest p-value would need to be below 0.012 to pass the q=0.05 threshold. The paper's single Monte Carlo confidence statement (90.5% direction consistency) is not a p-value but a direction-proportion; re-expressed as a one-sided binomial against a null of 50-50 direction, p ≈ 10^{-350} (trivially passes) but the other tests each carry their own family-wise burden.

The practical bite: the paper's single "90.5% direction consistency" framing gives a reader the impression of one controlled statistical test. In reality the paper rests on at least 21 tests, most of which are not formally null-hypothesis-framed, and the MCMC p100 claim that a careful reviewer will zero in on is itself one of those 21. The audit's §7 discipline paragraph ("when single dimensions are underpowered, cross-dimensional agreement is the inferential artefact") is the right framing — but it must be accompanied by an explicit test inventory and a family-wise statement.

### S2-01 CRITICAL — MCMC effective sample size is ~150, not 10,000

`data/v0_1_mcmc_convergence_diagnostics_100k.json` reports, per metric:

| Metric | n (raw) | τ (autocorr. time) | n_eff (ESS) | ρ lag-100 |
|---|---:|---:|---:|---:|
| Efficiency gap | 100,000 | 673.6 | **148.4** | 0.485 |
| Mean-median | 100,000 | 624.0 | **160.3** | 0.502 |
| Declination | 100,000 | 662.4 | **151.0** | 0.501 |
| Seats @ 50/50 | 100,000 | 645.9 | **154.8** | 0.519 |

ESS is the number of statistically independent samples the chain delivers per metric. The raw 10,000 is ≈ 15 independent samples; the 100,000 is ≈ 150 independent samples. For a tail-percentile claim "p ≥ 95," the standard statistical requirement is ESS ≥ 100 per metric with explicit CI on the tail estimate; for "p100" (strict outlier claim) the requirement is higher, with the MGGG group's publication-grade guidance typically ≥ 1,000 ESS per metric.

A Monte Carlo standard error on a proportion p at ESS = 150 is approximately `sqrt(p(1-p)/150)`. At p = 0.95, SE ≈ 0.018; 95% CI for the percentile is [0.915, 0.986]. At p = 1.00 (i.e. no observed sample more extreme), the Clopper-Pearson one-sided 95% upper CI is 1 − 0.05^{1/150} ≈ 0.020, i.e. the true percentile could be as low as p = 0.980 — the p100 is a 150-sample ceiling, not a 10,000-sample ceiling.

**Recommendation.**
1. Replace every p100 in the paper with "percentile ≥ 98 (95% CI, ESS ≈ 150)."
2. Report ESS and τ in §3.11 explicitly. The diagnostic file already exists; just integrate it.
3. The falsifiability hook ("if the 100k run moves either 2026 map off its tail") is substantively the right remediation and should be elevated from "held preliminary" to the actual reportable finding.

### S2-02 CRITICAL — 100k full-coverage rescore data exists and changes headline numbers materially

`data/v0_1_mcmc_ensemble_percentiles_full_100k.csv` contains a 100,000-sample MCMC run with the full-coverage hybrid-crosswalk rescore (the same remediation §3.11 describes as "in progress"). Key differences between that CSV and the paper's §3.11 table:

| Metric | Map | Paper §3.11 (10k, partial) | data/...full_100k.csv (100k, full) | Change |
|---|---|---|---|---|
| Mean-median | Majority 2026 | p6.6 (NDP-favoured tail) | **p92.66** (UCP-favoured tail) | Flipped tail |
| Mean-median | Minority 2026 | p100 | p98.76 | Still ≥95 |
| Declination | Majority 2026 | p52.2 (central) | p6.31 (NDP-favoured) | Shifts |
| Declination | Minority 2026 | p18.0 | **p1.56** (extreme NDP-favoured) | Material shift |
| Seats @ 50/50 | Majority 2026 | p1.69 (NDP-favoured tail) | **p57.86** (central) | Flipped tail |
| Seats @ 50/50 | Minority 2026 | p100 | **p94.27** | **Below p95 threshold** |

Two findings the paper currently carries that do not survive the full-coverage 100k rescore:

1. **"Majority 2026 at p1.7 on seats-at-50/50"** — the NDP-favoured outlier finding. In the paper, this is part of the "three p ≥ 95 or p ≤ 5 flags" in §3.11 and is called out as a "counter-intuitive result worth surfacing honestly." Under the 100k full-coverage run it is p57.86, inside the central band.
2. **"Minority 2026 at p100 on seats-at-50/50"** — headline UCP-favoured outlier. Under 100k full-coverage, minority is p94.27, which does not cross the pre-registered p ≥ 95 threshold.

The minority mean-median p98.76 and minority declination p1.56 do survive. The declination direction (strongly NDP-favoured) is consistent with the paper's §3.5.1 discussion of declination disagreeing with EG/MM/B4.

The **structural floor** finding in §3.11 (ensemble median seats-at-50/50 at ~0.448, i.e. UCP-favoured by default) is independent of the per-map percentiles and survives.

**Recommendation.** Block release until §3.11 is updated to reflect the 100k full-coverage numbers. The changes strengthen one finding (minority MM p98.76) and weaken two (majority seats p1.7, minority seats p100). Publishing the current §3.11 when the CSV shows a different result creates a serious credibility hazard: a reviewer or adversarial analyst who runs `diff` against the public data will find the paper contradicts the committed data.

### S2-03 HIGH — No family-wise error-rate control across 21 tests

Already detailed in the test inventory above. Two concrete remediations:

1. Publish a family-wise statement in §3.11 or a new §3.15: "The audit applies 21 distinct statistical tests to overlapping 2023-derived substrate. Family-wise error-rate control is not applied because several tests are not framed against a formal null (A1 MAD, counter-tests, compactness counts). The analytical framework is 'consistency across multiple weakly-powered tests' (Altman & McDonald 2011) rather than 'single test passes single threshold.' The MCMC tail-percentile claim in §3.11 is the one test that would benefit from explicit FWE control; we report its ESS-adjusted CI per S2-01 rather than apply Bonferroni."
2. Mark the 21-test inventory in the paper's Data Availability statement.

### S2-04 HIGH — B4 uniform-swing violation not quantified

§3.5.1 notes: *"B4 assumes uniform swing. Alberta elections have historically swung uniformly enough that this is defensible, but the 2019→2023 swing was not uniform (NDP gained more in Edmonton than in Calgary); the counterfactual should be read with that caveat."*

Disclosure is to the audit's credit. The peer-review objection: "how much does the headline seat-count change under a regionally-weighted swing?" is unanswered. A regional-swing-adjusted B4 can be computed from the same script (`v0_2_packing_cracking_analysis.py`) in under an hour: compute Edmonton-specific vs Calgary-specific vs rural-specific swing coefficients from the 2019→2023 regional shifts, apply them separately, re-count seats. Until done, the "42 NDP seats at 50/50 under minority" number in Table §3.3 is a point estimate with unmeasured sensitivity.

**Recommendation.** Run the regional-swing counterfactual. Report the range. If the range shifts the minority's seat count by more than 1, the "2-seat reduction for NDP" line in the §7 table narrows.

### S2-05 HIGH — Canadian base-rate "71st percentile" claim is circular

`data/v0_1_canadian_redistribution_base_rate.csv` has n=7 cycles of which 1 is the Alberta 2025–26 anchor (the cycle being assessed). The `v0_1_canadian_base_rate_computed.md` file computes the compression factor 0.455 from the anchor itself (1 data point) and then reports Alberta 2025–26 at the "71st percentile" of the 7-cycle distribution that includes the anchor.

Two independent circularities:

1. **Compression-factor calibration.** 0.455 is derived from Alberta 2025–26's own EG asymmetry (0.51 pp) divided by its own seat-share asymmetry (1.12 pp). Applying 0.455 to other cycles assumes Alberta 2025–26's seat-to-EG compression is the population compression. With n=1 calibration, the factor is an assumption, not an estimate. The file acknowledges a [0.4, 0.6] plausibility band; a reviewer will ask why the reported percentile uses a single point.
2. **Including the anchor in the percentile.** Percentiles of a statistic against a distribution should be computed against an *independent* distribution. Alberta 2025–26 contributes 1 of 7 observations; "71st percentile of 7 cycles" = "5 of 7 at or below" = "including Alberta itself." The honest framing is "5 of the 6 non-Alberta cycles are at or below 0.51 pp" = **83rd percentile among the non-anchor sample of 6**. Or, reported ordinally: "Alberta 2025–26 is the middle of three cycles with non-zero asymmetry (Alberta 2017 0.52; Alberta 2025–26 0.51; Manitoba 2018 0.80)."

**Recommendation.**
1. Drop the "71st percentile" framing; use the "middle of three non-zero cycles" framing.
2. Report the compression-factor sensitivity: under the [0.4, 0.6] band, minimum EG asymmetry estimate for Manitoba 2018 is 0.70 pp (compression 0.4 × seat-share 1.75) — still above Alberta's low end — and Alberta 2017's estimate is 0.46–0.69. The ordinal ranking survives the compression-band sensitivity; the percentile-framing does not.

### S2-06 MED — Monte Carlo direction-consistency CI not reported

The "90.5% of 2,000 samples show minority more UCP-favourable" framing is a proportion estimate, not a hypothesis test. Its binomial 95% CI at n=2,000 is [89.2%, 91.8%] (Clopper-Pearson). The point estimate is reported without the CI in §3.5, §7, and the preamble. A reviewer will ask for the CI.

**Recommendation.** In each place the 90.5% number appears, add "(95% CI 89.2–91.8%)."

### S2-07 MED — Declination implementation verified correct

Cross-checked `analysis/v0_1_mcmc_ensemble.py` lines 140–157 against Warrington's reference Python in arXiv 1803.04799:

- Warrington: `theta = arctan((1 − 2·mean_Rwin) · n/R)`, `gamma = arctan((2·mean_Dwin − 1) · n/D)`, `declination = 2·(gamma − theta)/π`.
- Audit: `theta_R = atan2(mean_ucp_win − 0.5, R/(2n))`, `theta_D = atan2(0.5 − mean_ucp_in_ndp_won, D/(2n))`, `declination = (2/π)·(theta_R − theta_D)`.

Algebraically: audit `y/x` for theta_R is `(mean − 0.5) · 2n / R = −(1 − 2·mean) · n/R = −` Warrington y/x. The audit's theta_R = −theta_Warrington. Likewise theta_D = −gamma_Warrington. So `theta_R − theta_D = −theta_W + gamma_W = gamma_W − theta_W` — the final declination is identical.

No finding. Small improvement: the audit's docstring says "theta_R = atan2(mean UCP share in UCP-won − 0.5, R/n)" (line 142). The actual code uses `R/(2n)`, not `R/n`. Docstring should be corrected.

### S2-08 LOW — base-rate CSV column name ambiguity

`data/v0_1_canadian_redistribution_base_rate.csv` column `seats_changed_between_a_and_b` is `3` for Alberta 2025–26 but `1` is the partisan-flip count used in the analysis. The difference is benign (the "3" refers to EDs with boundary changes), but the column name invites misreading. Rename to `ed_boundary_changes_between_a_and_b` and add a separate `partisan_flip_count` column.

---

## S9 — Claim calibration findings (detail)

### S9-01 CRITICAL — "p100" language is tighter than the evidence

The paper's §3.11 reports minority 2026 at p100 on mean-median and seats-at-50/50. The public report's headline language calls this "more UCP-favoured than every one of 10,000 alternatives."

Three calibration failures stack:
1. The raw 10,000 and the raw 100,000 each have ESS ≈ 15 and ≈ 150 respectively (S2-01); "every one of 10,000" implies 10,000 independent draws.
2. Under 100k full-coverage rescore, minority mean-median is p98.76, not p100; minority seats@50/50 is p94.27, not p100 (S2-02).
3. The strict meaning of p100 (no observed sample more extreme) is a 150-sample tail-ceiling, not a 10,000-sample floor.

The defensible version: *"In a 100,000-sample ReCom ensemble (effective sample size ≈150 per metric), the minority 2026 map sits in the top 2% on mean-median and in the top 6% on seats-at-50/50. No observed sample was more extreme on mean-median."*

**Recommendation.** Replace every "p100" and "every one of 10,000 alternatives" in the paper and public report with ESS-adjusted language. Block release on this change.

### S9-02 HIGH — "Three formal signatures" is tighter than the evidence under the reformulated E2

The public report and §3.10 summary headline "three formal signatures detected in the minority." Under the reformulated-E2 reading, one of those three (RMH-Banff Park engineered boundary) is signature-under-substantive-test, not signature-under-originally-committed-test. The adjective "formal" implies pre-committed, which S1-01 and S1-03 show the E2 was not.

**Recommendation.** Replace "three formal signatures" with one of:
- "three signatures on the reformulated test set" (shortest, most accurate);
- "two formal signatures (Airdrie cracking, Calgary Zone-A packing) plus one signature under the substantive-E2 reformulation (RMH-Banff Park)"; or
- "three signatures, one of which (RMH-Banff Park) was scored on a test reformulated mid-audit; see §3.9."

The third is the most defensible in a peer-review context.

### S9-03 HIGH — "Six dimensions" count collapses under independence check

The abstract and §7 synthesis lean on "directional consistency across six dimensions." The six are: §A1 (MAD), §A2 (Calgary zone), §A2b (rest-of-province), §A3 (s.15(2)), §B (partisan bias), §C (spatial / community-of-interest), §D (procedural). Of these, A1, A2, A2b, and A3 are all computed on the same per-ED population vector; they share one underlying source. §3.5.1 acknowledges B2/B3/B4 are closely related to wasted-vote-and-seat-counterfactual. The honest independent-family count is four: population-math, partisan-bias, spatial, procedural. "Six dimensions" reads as six independent tests; the actual inferential evidence is four families of weakly-related tests.

**Recommendation.** Reframe §7 and the abstract: "directional consistency across four independent evidence families (population-math, partisan-bias, spatial, procedural), covering six measurement frameworks overall." The public report should adopt the "four families" language in its synthesis.

### S9-04 MED — "One to three seats" range needs structural disclosure

The public report uses "one to three seats at a tied vote, with a 95-percent confidence interval that crosses zero." The academic paper §3.5 is clear that the 1-seat gap is the central estimate at the 70/30 weighting; the "three" end is the 2,000-sample Monte Carlo upper bound under weight/jitter sensitivity. A reader of the public report gets the impression of a range between central-case-1 and central-case-3; the actual structure is central-case-1 and tail-case-3.

**Recommendation.** Public-report language: "one seat at the central modelling weight, with a 95-percent confidence interval that extends to three seats under modelling jitter and crosses zero in the other direction." Academic report §3.5 already has the structure; propagate to the public report.

### S9-05 MED — "71st percentile" Canadian framing should be reworded (see S2-05)

Already specified in S2-05. Under S9 lens: the "71st percentile" framing is tighter than the evidence in two ways (compression-factor calibration from n=1; percentile includes the anchor). The "middle of three non-zero cycles" framing is both defensible and rhetorically cleaner.

---

## Proposed pre-registration improvements for OSF submission

The current `analysis/v0_1_pre_registration_draft.md` for the November 91-seat map is solid but would close additional S1 findings if the following were added:

1. **Add an "S0 — scorable set" definition.** Commit that if the committee publishes only the final map with no per-ED rationale, the S6, X2, W3 tests are scored as BLOCKED (not FAIL). Currently stated per-test; consolidating into a scorable-set definition reduces the ambiguity a reviewer will find.
2. **Add the 21-test inventory and a family-wise statement.** Currently the pre-registration commits to 17 tests for the November scoring; the repository's headline also cites partisan-bias tests, counter-tests, and MCMC runs that are run on the baseline. Adding the full inventory and committing to no new post-hoc tests closes S2-03 for the November cycle.
3. **Add the keyword regex list and classification heuristic.** For S6 (publicly-supported configs dropped / unsupported kept), the November scoring will re-run `submission_search.py` against whatever submissions the committee receives. Commit the keyword regex list and the support/oppose heuristic verbatim in the pre-registration, so the keyword shape is held under external custody. Closes S1-02 for November.
4. **Add ESS-adjusted MCMC language to S5.** Replace "top 5% (percentile ≥ 95)" with "top 5% (percentile ≥ 95) at ESS ≥ 100 per metric, 95% Clopper-Pearson CI reported with the point estimate." Closes S2-01 for November.
5. **Commit the declination implementation.** `analysis/v0_1_mcmc_ensemble.py`'s `seat_results()` function is the reference implementation; freeze the SHA of the script at OSF submission time.
6. **Commit the family-wise correction rule.** Add an explicit rule for how the November scoring will handle multiple-comparison adjustment if >5 strong-signal tests fire simultaneously.

---

## Release blockers vs. acknowledgement-as-limitation

**Block release until fixed:**

- **S1-01** CRITICAL — the pre-registration provenance claim is false as stated. Must be retracted or corrected before release.
- **S2-01** CRITICAL — p100 language without ESS adjustment. Must be corrected before release.
- **S2-02** CRITICAL — the paper's §3.11 headline numbers contradict committed data. Must be updated to match the 100k full-coverage rescore (or §3.11 must be retracted until the rescore is complete and committed).
- **S9-01** CRITICAL — public report headlines over-claim MCMC precision. Must be recalibrated before release.
- **S1-02** HIGH — if S6 scoring depends on the submission keyword list, the keyword list's retrospective origin needs explicit disclosure. Acknowledge-as-limitation acceptable if the disclosure is in the paper; release-block if the paper continues to describe S6 as "pre-registered."
- **S9-02** HIGH — "three formal signatures" must be replaced with one of the reformulation-disclosed alternatives before release. Release-block.

**Acknowledge as limitation (release-permitting):**

- **S1-03** HIGH — E2 reformulation is disclosed; strengthen with an explicit OSF-time-stamp comparison.
- **S1-04** HIGH — counter-test caveat is present; propagate to §3.10 and §3.12.
- **S1-05** MED — add commit-timeline chronology note to baseline scoring doc.
- **S2-03** HIGH — family-wise error-rate statement added to §3.11 or new §3.15.
- **S2-04** HIGH — regional-swing B4 counterfactual added as an appendix or a future-work note with a committed deadline.
- **S2-05** HIGH — rewrite the Canadian base-rate percentile framing; fix compression-sensitivity reporting.
- **S2-06** MED — add the 90.5% Monte Carlo CI parenthetically.
- **S2-07** MED — fix declination docstring (`R/n` → `R/(2n)`).
- **S2-08** LOW — rename CSV column.
- **S9-03** HIGH — rewrite "six dimensions" as "four independent evidence families."
- **S9-04** MED — public-report "one to three" needs the structural-disclosure rewrite.
- **S9-05** MED — tied to S2-05.

---

## Notes for the parent session

- Legal-framework D4 (reproducibility) overlaps with S2-02 (MCMC full-coverage data exists but is not in the paper). Same fix closes both.
- Legal-framework D10 (time-stamping) overlaps with S1-01, S1-02, S1-05. The OSF submission is the single remediation that closes the time-stamping and pre-registration concerns for future scoring.
- The audit's own `v0_1_design_critique.md` and `v0_1_bias_audit.md` already anticipate several of these findings; the red-team value is in pinning severity and block-vs-limit classification.

---

*End of findings file.*
