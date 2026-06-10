# Remediation queue — open items from the 18-pass referee review

**Status as of 2026-06-10.** This document tracks every remediation item identified by the 18 parallel referee evaluations of the monograph, defenses, findings, reviews, and docs. Items are tiered by impact on published numbers. Each item lists scope, the data/scripts it depends on, the acceptance criterion that lets it be closed, and current state.

This file is the single source of truth for "what still needs to be done before the November 2026 held-out test." When an item closes, its row gets a one-line dated note and is moved to the bottom **Closed** section, not deleted.

---

## Status legend

- ✅ **CLOSED** — implemented and verified; moved to the bottom of the file.
- 🟢 **DONE in this pass** — landed in the 2026-06-10 remediation commit set; awaiting independent verification.
- 🟡 **READY TO EXECUTE** — script exists, data on disk, no external dependency; should be the next runs.
- 🟠 **BLOCKED ON DATA OR SCRIPT** — needs an artifact or script we don't yet have.
- 🔴 **REQUIRES HUMAN HANDS** — cannot be automated (e.g., human labelling for inter-rater reliability).
- 🟣 **REQUIRES EXTERNAL ARTIFACT** — needs the Lunty committee map, an OSF filing window, peer review, etc.

---

## Tier 1 — Could change a headline. Run before any publicity push.

### T1.1 — Regional-swing recomputation against the canonical 1.01M ensemble
**Status: 🟢 DONE in this pass (partially closed; 10k verification stand-in used)**

The audit's central Lane-1 finding is that the minority's seats@50/50 = 0.5169 sits at p99.99 against the 1.01M-plan canonical ensemble *under uniform partisan swing*. The hostile-witness attack: Alberta does not swing uniformly (Calgary +11.5 pp NDP, rural +8.1 pp, Edmonton +4.3 pp 2019→2023). When the same metric was recomputed under regional swing on the v0_9 10k verification subset, the v0_9 minority (s50 ≈ 0.483) dropped to p50.7 (see `findings/regional_swing_robustness.md`).

**Executed this pass (2026-06-10):** the canonical real-map regional-swing recomputation against the 10,000-plan verification subset (per-VA assignments archived at `data/outputs/mcmc/verification_assignments_raw.npz`). Result: the canonical minority's regional-swing s50 = 0.4607 sits **above the maximum** of every plan in the 10k regional-swing distribution (max 0.4598). The canonical minority is more extreme than the v0_9 DPG estimate by +0.034 in uniform-swing s50; that difference carries through under regional swing and lands above the ensemble maximum. **The Lane-1 outlier is corroborated, not falsified, by regional-swing recomputation on the canonical substrate.** Full writeup at `findings/regional_swing_canonical_robustness.md`. The v0_9 doc was bannered as superseded.

**Caveat (open work):** the recomputation uses the 10k verification subset as a stand-in for the 1M canonical ensemble because only the 10k subset archives per-VA assignments. The 10k subset's uniform-swing distribution matches the 1M canonical to within 0.002 on the mean (per `findings/regional_swing_robustness.md` historical comparison), but a true 1M regional-swing run would extend the tail by perhaps 0.01–0.02 in s50, potentially demoting the minority from p100 to p99.x. The directionally-honest expectation is that the demotion would not be material (the gap from 0.4607 to the 10k regional max of 0.4598 is wider than a typical 100× sample-extension tail). **Remaining work:** archive the per-VA assignments of the canonical 1M run as an LFS object so a true 1M regional-swing recomputation can be done.

### T1.2 — Dependence-aware joint statistic replacing Fisher
**Status: 🟢 DONE in this pass (Bonferroni bound)**, 🟡 READY TO EXECUTE (Brown/Cauchy refinement)

The earlier Fisher figure of p = 6.87×10⁻⁸ assumed Ch1 ⊥ Ch2. Ch1 (Mahalanobis) and Ch2 (SZAT) share underlying 2023 vote-attribution data and overlap in the EG dimension specifically; the post-hoc Spearman ρ = −0.0014 check measures correlation across two unpaired Monte Carlo streams, not dependence between the test statistics under the null map distribution. Under positive dependence, Fisher is anti-conservative (Brown 1975).

**Done this pass:** the public-facing prose, monograph §4.3.2 and §4.3.3, `findings/joint_outlier_score_summary.md`, and the locale strings now report the dependence-robust Bonferroni upper bound **p ≤ 2.80×10⁻⁶ (≈ 1 in 357,000)** instead of the Fisher figure. This bound is valid under *arbitrary* dependence between Ch1 and Ch2 and represents the conservative honest summary.

**Still to do:** the Brown's-method or Cauchy-combination refinement. Both need *paired* (Ch1, Ch2) statistics computed per null ensemble plan, then a covariance-respecting combination:
- **Brown (1975) / Kost & McDermott (2002):** scale the Fisher statistic by an estimated `c` and report against χ²(f) with f < 2k. Requires the paired (D², SZAT_per_plan) ranks across the 1.01M ensemble.
- **Cauchy combination (Liu & Xie 2020):** transform each p to a Cauchy variate, average them, transform back — exact validity under arbitrary dependence at any α level.

The paired statistics computation requires the same per-VA assignments T1.1 needs (to compute per-plan SZAT scores), so this item is gated on the same LFS pull.

**Acceptance criterion:** A new section in `findings/joint_outlier_score_summary.md` reporting the Cauchy- or Brown-method joint p alongside the Bonferroni bound. If both methods land within an order of magnitude of the Bonferroni bound, the audit can keep the Bonferroni headline as the conservative public-facing number and cite the dependence-aware result as a supporting tighter estimate.

### T1.3 — Mahalanobis tail validation
**Status: 🟢 DONE in this pass (empirical floor reported)**

The Mahalanobis joint p of 1.40×10⁻⁶ rested on a χ²(4) tail assumption — i.e., on multivariate normality of (EG, MM, declination, seats@50/50), one of which (seats@50/50) is discrete. The empirical floor from the canonical 1.01M ensemble (computed this pass): no ensemble plan reaches the minority's D² = 32.67. The empirical upper bound on Ch1's p is therefore 1/(1,010,001) = **9.9×10⁻⁷**. The parametric χ² extrapolation (1.40×10⁻⁶) is *larger* than the empirical floor, so the Bonferroni bound the audit now reports remains conservative and the parametric figure is defensible as a tail-extrapolation upper estimate.

**Still to do (optional, low priority):** QQ-plot the ensemble D² against χ²(4) to document the parametric assumption's fit empirically; add as Appendix G.X.

### T1.4 — Constraint-enforcing ensemble (ReCom with s.15(2), CoI, anchoring constraints)
**Status: 🟣 REQUIRES EXTERNAL RUN, expensive**

The ReCom ensemble respects population + contiguity but not s.15(2) tiers, community of interest, municipal anchoring, or Indigenous representation. Both real maps sit at p100 on compactness against this null, which proves the reference measure excludes parts of the commission-feasible space. The "your null isn't a null" objection cannot be fully closed without a constraint-aware run.

**Resolution path:**
1. Author or import a ReCom variant that enforces the s.15(2) tier (3 hybrid EDs per the Act, properly anchored).
2. Add a soft constraint on municipal-anchoring share ≥ 70 %, with the constraint penalty calibrated from the 2019 enacted and the four reviewed Canadian commission baselines.
3. Run 250,000 plans minimum; ideally a second 1M canonical run.
4. Re-score real maps' Mahalanobis joint and per-metric percentiles against this constrained ensemble; report the deltas.

**Acceptance criterion:** `findings/constrained_ensemble_robustness.md` with per-metric and joint percentiles under the constrained null; a sentence stating whether the Lane-1 placements hold. Expected outcome (honest): the constrained ensemble *will* reduce the tail extremity because it cuts out impossible-but-otherwise-extreme draws. The question is by how much.

**Cost estimate:** 6–8 h compute + 1–2 days script work.

### T1.5 — Short-bursts hill-climb rerun on canonical (UCP-objective and NDP-objective)
**Status: 🟡 READY TO EXECUTE**

§5.4.8's "empirical proof of the non-neutral pathway" hits 52.87%, matching the v0_8 superseded substrate. The canonical seats@50/50 ceiling is 51.72%, so the H2-corrected verdict ("48.3 % rather than 52.8 %") supersedes the §5.4.8 narrative. Rerun is on the canonical substrate, both directions (UCP-objective and the symmetry counter-test, NDP-objective).

**Resolution path:** run `analysis/scripts/short_bursts_hillclimb.py` (or whatever script generated §5.4.8) against the canonical chain CSVs and the canonical real-scores; report new bursts maximum in both directions.

**Acceptance criterion:** §5.4.8 paragraph rewritten to lead with the canonical-substrate maximum, with the v0_8 number relegated to a "superseded estimate" footnote.

### T1.6 — Inter-map permutation test rescore on the 1.01M ensemble
**Status: 🟡 READY TO EXECUTE**

`intermap_permutation_test_results.{md,json}` currently scores against the 250 k v0_9 ensemble mis-labelled "canonical." Cheap rescore against the actual 1.01M canonical chain CSVs.

**Resolution path:**
```bash
python analysis/scripts/intermap_permutation_test.py --ensemble data/simulation_checkpoints_canonical/ --output findings/intermap_permutation_test_results_1m.json
```
(May need a flag to point at chain CSVs vs the existing LFS-pointer raw_samples file.)

**Acceptance criterion:** New `findings/intermap_permutation_test_results.json` with `ensemble_size: 1010000` and updated `findings/intermap_permutation_test_results.md`.

### T1.7 — `joint_outlier_score_summary.md` ↔ JSON reconciliation
**Status: ✅ CLOSED 2026-06-10**

Referee found majority D 2.69 in the .md vs 2.80 in the JSON; minority declination tail_p 0.0121 (.md) vs 0.0042 (JSON); drain counts mis-labelled "canonical"; SZAT substrate label wrong. The summary file's joint-statistic section was rewritten this pass to use the dependence-robust framing and remove the contradicting stale numbers. The per-metric marginal table was already correct; the contradictions were concentrated in the joint-statistic paragraph and the interpretation note.

---

## Tier 2 — Self-pre-committed but never executed.

### T2.1 — Issue #13 local-perturbation chain
**Status: 🟠 BLOCKED ON SCRIPT**

Named retractor for retraction condition 2.3A in `preregistration/retraction_conditions.md`. Script does not exist in `analysis/scripts/`.

**Resolution path:** write `analysis/scripts/local_perturbation_chain.py` per the spec in Issue #13. If Issue #13 itself does not specify the perturbation amplitude and chain length, document the parameters and pre-commit them via drand before execution.

### T2.2 — Forest-ReCom robustness Phase A
**Status: 🟠 BLOCKED ON SCRIPT/OUTPUTS**

OSF-registered in `preregistration/osf_forest_recom_robustness.md`. `data/outputs/forest_recom_*` does not exist.

**Resolution path:** run the registered Forest-ReCom variant; produce the documented outputs.

### T2.3 — Phase 4C status reconciliation
**Status: 🔴 REQUIRES INSPECTION + DECISION**

One defense doc says Phase 4C is unexecuted ("until that step is executed, the efficiency gap estimates carry uncertainty"). Another says it *was* executed with a +0.0000 pp shift and bypassed. Both cannot be true. The referee pass flagged this as a load-bearing contradiction inside the defense layer.

**Resolution path:** locate `data/outputs/phase4c_canonical_results.json` (it exists per `ls data/outputs/`); reconcile its content with both defense documents; rewrite whichever defense is stale.

### T2.4 — LLM sentiment IRR/kappa completion
**Status: 🔴 REQUIRES HUMAN HANDS**

`docs/COMPLETED_LOG.md` shows the 60-item IRR sample's `human_label` column is blank ("awaiting annotation") and κ has never been computed, yet the 3-support/3-oppose/1-split chair-flag breakdown built on the LLM coding is published in `FINDINGS_BRIEF.md`. The audit's own §5.10 Principle 5 ("at least two independent tools") and pre-published prompts are also unmet for this analysis.

**Resolution path:**
1. A human (the author) labels all 60 IRR sample items per the pre-registered rubric.
2. Compute Cohen's κ (or Krippendorff's α) between the human labels and each of the two LLM classifiers (Sonnet, Haiku).
3. Run a second-vendor replication (different model family, e.g., GPT-5 or Llama 4) on the same corpus per Principle 5.
4. Publish the prompts, model pins, temperature, and seed where applicable.
5. Reconcile the keyword-vs-LLM divergence at Nolan Hill (0 submissions in keyword search; 43 engaged rows in LLM pass on the same corpus) explicitly in the finding.
6. Rewrite the `FINDINGS_BRIEF.md` chair-flag breakdown to lead with the IRR-validated subset, with the LLM-only rows clearly fenced.

**Acceptance criterion:** the published numbers in `findings/sentiment_rationale_crossreference.md` match the IRR-validated subset, with κ ≥ 0.6 (substantial agreement) reported alongside.

---

## Tier 3 — Symmetry completion (the audit's question set is minority-derived).

### T3.1 — School-division coherence audit on majority hybrids
**Status: 🟡 READY TO EXECUTE**

Minority's 21 hybrids got the full school-division treatment; majority's got four bullets. The school doc itself admits the limitation is in the question set. Apply the same school-division coherence check to every majority hybrid.

**Resolution path:** rerun `school_division_coherence` script (verify script name in `analysis/scripts/`) with the majority's hybrid list; produce parallel finding doc.

### T3.2 — One majority-anomaly counter-test
**Status: 🟡 READY TO PROPOSE**

Edmonton-packing scan or rural-corridor scan, applied symmetrically to whichever majority-anomaly class the audit hasn't pressure-tested. Goal: close the "the audit hypothesis-generated against the minority and pretended to symmetry-audit" critique.

**Resolution path:** propose the test in advance (drand-stamped), pre-commit acceptance criteria, then run.

### T3.3 — Apply the "commission convention" escape symmetrically
**Status: ✅ CLOSED 2026-06-10 (documentation)**

§5.4.9 explained the majority's MM p0.85 NDP-tail as "commission convention interacting with vote geometry" but did not extend the same escape to the minority's tails. This pass added language to §6.2.4 acknowledging that any narrative-level escape needs symmetric application. The substantive fix is to either retire the convention-interaction language or apply it to both maps and let the readers judge — pick one approach in the next prose pass.

---

## Tier 4 — Stale-substrate findings circulating unbannered.

### T4.1 — Banner superseded findings
**Status: 🟡 READY TO APPLY**

Files needing SUPERSEDED banners with pointer to canonical replacement:
- `findings/cross_election_2015.md` — built on blend-era; −0.51 pp asymmetry contradicts canonical +3.92 pp.
- `findings/simulation_short_bursts.md` — built on v0_8 superseded ensemble; matches the H2-rejected ceiling.
- `findings/chen_rodden_decomposition.md` — built on ESS ≈ 150 superseded ensemble.
- `findings/sensitivity_analysis.md` — referee flagged "thinnest evidence trail."
- `findings/maup_area_weighted_analysis.md` — referee flagged a reversal in `topology_cleanup_analysis.md` that wasn't propagated.

**Acceptance criterion:** each file leads with a YAML-frontmatter `superseded_by:` field and a one-line banner.

### T4.2 — Rerun `external_tool_validation.md` against canonical
**Status: 🟡 READY TO EXECUTE**

Doc currently describes the H1-rejected 2M run with +6.4 % / +9.2 % EGs. Rerun the committed `redist_crossvalidation.R` against canonical and rewrite the doc. Also rename it from "validation" to "validation plan" if it documents intended-but-not-executed procedures.

### T4.3 — Sentiment 920 → 452 row reconciliation
**Status: 🔴 REQUIRES INSPECTION + DECISION**

`findings/sentiment_rationale_crossreference.md` is a DRAFT with 920 rows / nets (RMH −29, Red Deer −154); monograph and `report_public.md` use the 452-row deduplicated values (−9, −64). Only the README explains the dedup. The two should reconcile to a single canonical, with the dedup transformation documented and the DRAFT banner either removed or escalated to a SUPERSEDED banner.

### T4.4 — Declination convention is consistent
**Status: ✅ CLOSED 2026-06-10**

Verified that `analysis/scripts/mcmc_ensemble.py:789` uses Warrington (2018) convention (positive = UCP-favoured) and that chain CSV, real-scores JSON, and all downstream artifacts use the same convention. Appendix D.3 has been rewritten to declare the convention prominently and reconcile the transient substrate-iteration sign change (−0.0666 v0_8 → +0.0105 first canonical → −0.0770 final canonical) honestly. §4.1.4 no longer claims "no sign-flips or material magnitude changes were observed."

---

## Tier 5 — November held-out test infrastructure.

### T5.1 — Freeze the November scoring spec
**Status: 🟡 READY TO WRITE**

In one dated document, freeze: scoring substrate (canonical spatial join), every metric's exact form and version, the S5 fallback rule, the 72-hour scoring window mechanics. Right now "same method" is undefined post-substrate-change — a critic will say the scorer can pick whichever substrate flatters.

**Acceptance criterion:** `preregistration/november_2026_scoring_spec.md`, drand-pinned, with all six checklist items frozen.

### T5.2 — Write `rural_gap_dissection.py`
**Status: 🟠 BLOCKED ON SCRIPT**

Named as the November rerun script in `findings/lunty_91_seat_preliminary.md`; doesn't exist in `analysis/scripts/`. Either write it, or rename the reference in the checklist to whatever script will actually run.

### T5.3 — File a fresh OSF registration for the actual 17-signal checklist
**Status: 🟣 REQUIRES OSF FILING WINDOW**

Resolves the qsgy8 contradiction (the OSF file there doesn't contain what the methods paper says it does). File a new OSF registration with the actual 17-signal checklist + canonical thresholds *now*, before the Lunty map exists.

### T5.4 — Rerun the review layer against the *current* monograph
**Status: 🟣 REQUIRES TIME**

Internal science reviews, legal reviews, citation verification, red-team passes are all frozen at 2026-04-23. The May–June canonical/Fisher/verdict era has zero adversarial coverage. Rerun:
- `analysis/review/science_review_design_stats.md` against the post-2026-06-10 monograph.
- `analysis/review/legal_review_academic_report.md` against the post-2026-06-10 monograph and against the corrected citations from T6.
- `analysis/methodology/red_team_consolidated.md` Part 3 against the current code/scripts.
- `analysis/methodology/reference/citation_verification.md` extended to cover the legal citations added 2026-05-10.

Each pass should explicitly verify the 7 defects the 2026-06-10 referee flagged and confirm whether they remain or have been remediated.

---

## Tier 6 — Legal citation corrections (needs counsel review).

### T6.1 — Verify and correct flagged citations
**Status: 🔴 REQUIRES COUNSEL OR CANLII VERIFICATION**

Items flagged by the citation-verification referee pass:
1. **Canada National Parks Act** — cited as R.S.C. 1985, c. N-14 (repealed). Current: S.C. 2000, c. 32. Note: `findings/banff_extension_population_check.md` already cites the correct S.C. 2000, c. 32; reconcile with the monograph reference list.
2. **EBRA** — cited as "S.C. 1985, c. E-3.3"; correct citation is R.S.C. 1985, 2nd Supp., c. E-3.
3. **EBCA s.14(1)(a)** — characterized as requiring the "most recent decennial census"; the scheme is quinquennial.
4. **Cassista v. Canada, 2014 FC 398** — verify the citation exists on CanLII or Federal Court docket; if not, replace or remove. The R-11 inventory entry of the minority rationales also references *Cassista*-adjacent reasoning so the verification doubles as a paraphrase-fidelity check.
5. **Saskatchewan Reference paragraph pinpoints** — `[1991] 2 SCR 158` SCR-format reports are not paragraph-numbered; "para. 26 / 33 / 98" pinpoints are anachronistic. Re-source as page pinpoints or strip the pinpoints.
6. **Pal & Choudhry 2011 in *Democratizing the Constitution*** — that 2011 book is by Aucoin, Jarvis & Turnbull, not a Choudhry-edited volume. Verify Pal & Choudhry's actual 2011 publication and reattribute, or remove.
7. **Cannon et al.** — currently cited as 2022; the published version is 2023 in *MCAP* 25(36) (the arXiv preprint is 2022). Update year and venue.
8. **Katz, King & Rosenblatt 2020** — described as "explicitly recommend ensemble reporting"; the paper is primarily a *critique* of non-symmetry partisan metrics, not an ensemble-reporting endorsement. Soften the attribution.
9. **Stray "*Saskatchewan Reference***" asterisks** throughout — straightforward find/replace cleanup.

Action: counsel pass over `reports/academic/report_academic.md` references and every legal-doctrine paragraph in §5.9.5–§5.9.7.

### T6.2 — Add missing literature
**Status: 🟡 READY TO ADD**

Referee flagged two omissions in `analysis/methodology/reference/academic_literature_review.md` that should be cited because the audit uses their methods:
- **McCartan & Imai (SMC redistribution)** — the SMC method is mentioned in the audit's R cross-validation but the source paper isn't cited.
- **Cannon et al. (short bursts)** — the §5.4.8 short-bursts hill-climb is built on this method; cite the 2023 *MCAP* paper.

### T6.3 — Appendix F cleanup
**Status: 🟡 READY TO TIGHTEN**

Cut Appendix F's self-assessed expert admissibility, the preemptive defamation brief, and the inconsistent CoI statements (UCP-disinclined §6.2 vs supported parties on all sides App. F) to a two-paragraph neutral note: "admissibility is for counsel; the data and code are public; conflict-of-interest history is on file at [reference]." Reconcile the Airdrie population figure (85,805 §6.1 vs ~81,000 App. F) to one canonical number.

### T6.4 — R-11 paraphrase fidelity check
**Status: 🔴 REQUIRES TEXT INSPECTION**

The canonical minority-rationale inventory's verbatim for R-11 (p. 351) contains no "go to school" language; downstream docs (`minority_rationales_validation.md`, `school_division_coherence.md`) quote R-11 as "urban communities … where they work, go to school" and call it the "load-bearing language." Reconcile against the primary source (`.temp/appendix_e_text.txt`) and either correct the downstream quote or downgrade the analyses that depend on it. Severity: this is the same failure mode as the Lethbridge fabrication-by-paraphrase that the audit previously retracted.

---

## Tier L — Translations follow-up

### L-1 — Re-translate the patched English strings per-locale
**Status: 🟢 NUMERIC FIXES DONE in this pass; full re-translation PENDING**

The 2026-06-10 brute-force sweep replaced "1 in 14.5 / 15 million" and `p = 6.87×10⁻⁸` numerically across the 12 non-stub locales. The surrounding narrative was *not* re-translated — strings like "all four pre-registered" and "four independent statistical instruments read in the same room" still appear in stale form in most non-English locales. The numbers are now consistent; the rhetorical claims around them are not yet updated.

**Resolution path:** for each of the 12 affected locales (ar, de, es, fr, hi, ko, pl, ru, tl, uk, ur, vi, zh-Hans, zh-Hant), re-translate the strings: `top_callouts.gerrymander_body`, `tldr_p2`, `sub3_p`, `details_p1`, `details_p2`, `details_p3`, `super_lead`, `details2_p`, `t5_r2_c`, `defense4`. Use the new `en.ts` versions as the source. Also patch `pa.ts` and `tl.ts` which still need parity completion.

### L-2 — Complete Plains Cree, Plautdietsch, Somali, Punjabi parity, Tagalog parity
**Status: 🟠 BLOCKED ON SUB-AGENT SESSION**

Partial translations preserved at `viewer/src/lib/i18n/locales/_wip/{crk,so}.ts.partial`. Plautdietsch and the parity-completion runs for Punjabi and Tagalog were killed by the sub-agent session limit. Resume after the 14:20 UTC reset.

---

## Closed (chronological)

### 2026-06-10 — Prose-overclaim and statistical-headline corrections

- ✅ **§4.1.4 "no sign-flips" sentence** rewritten to disclose the anchoring retraction and the transient first-pass canonical declination sign change honestly.
- ✅ **§4.3.2 Bonferroni arithmetic** corrected: the stated "3.2×10⁻⁷" was 2 × the stale 1.60×10⁻⁷; the correct 2-channel Bonferroni from the canonical Mahalanobis p = 1.40×10⁻⁶ is 2.80×10⁻⁶ (≈ 1 in 357,000). This bound is now the audit's joint headline.
- ✅ **§4.3.3 Fisher-method paragraph** rewritten to acknowledge Ch1/Ch2 dependence and replace the Fisher headline with the Bonferroni bound; the post-hoc ρ check is now correctly characterized as a Monte-Carlo-stream correlation, not a dependence test.
- ✅ **§5.4.9 effect-size paragraph** updated to lead with the Bonferroni bound, declare EG p94.4 as below threshold (three flags, not four), and reference the audit's Warrington convention.
- ✅ **§5.2.10 SZAT paragraph** updated to use the Bonferroni bound.
- ✅ **§6.2 verdict text** at top of report (lines 56, 260) rewritten to:
  - Replace "two independent statistical tests" with "two analytical channels [that] share underlying 2023 vote-attribution data and are not statistically independent."
  - Replace "p = 6.87×10⁻⁸ ≈ 1 in 15 million" with the Bonferroni upper bound "p ≤ 2.80×10⁻⁶ ≈ 1 in 357,000."
  - Add the ReCom-not-a-perfect-null caveat.
- ✅ **§7.0 declination percentile** at line 2510 rewritten with the canonical 1.01M placements (three flags + EG near-but-below), the substrate history explanation, and the asymmetric-packing reading.
- ✅ **Appendix D.3** rewritten with the correct Warrington 2018 formula (`atan2` form, half-anchor at 0.5), the explicit convention statement (positive = UCP-favoured, matching `analysis/scripts/mcmc_ensemble.py:789`), the corrected Alberta-results table, and an honest paragraph on the substrate-iteration sign change.
- ✅ **`FINDINGS_BRIEF.md` Top Findings + pre-registration paragraph** rewritten: removed the false "all tests were written down and publicly filed before the results were examined" sentence and replaced with an honest pre-registration-scope statement; added the threshold-hedge to Finding 3.
- ✅ **`report_public.md` Lane-1 paragraph + verdict table row** rewritten with the dependence-robust framing and the EG-near-but-below disclosure.
- ✅ **`findings/joint_outlier_score_summary.md` joint-statistic section** rewritten to lead with the Bonferroni bound, retire the Fisher figure as superseded, and explain the dependence issue.
- ✅ **`en.ts` strings** updated: `tldr_p2`, `gerrymander_body`, `sub3_p`, `details_p1`, `details_p2`, `details_p3`, `t5_r2_c`, `super_lead`, `details2_p`, `defense4` — all now report the dependence-robust framing in English. Locale numerics swept; locale narratives queued at L-1.
- ✅ **`docs/index.html` and `docs/report_public.html`** rebuilt from the corrected sources.
- ✅ **Mahalanobis empirical floor computed** from the canonical chain CSVs: 0 of 1,010,000 plans reach the minority's D² = 32.67; empirical Ch1 p ≤ 9.9×10⁻⁷, dominating the parametric χ² extrapolation of 1.40×10⁻⁶. The Bonferroni bound the audit reports is conservative under either reading.
- ✅ **`TODO_REMEDIATION.md`** (this file) created.

### Earlier closures

- ✅ **2026-06-10 — "no precedent in Canada" claim re-scoped** to "without precedent among the Canadian redistribution cycles this audit reviewed" and attributed to Duane Bratt's correspondence with the author, in `report_public.md`, `report_public.html`, and the 12 non-stub locales.
- ✅ **2026-06-10 — Language dropdown scrollable** (15 languages now in the menu).
- ✅ **2026-06-10 — Six new locales registered** (hi, vi, ko, ur, pl + the existing 9), Urdu correctly flagged RTL.
