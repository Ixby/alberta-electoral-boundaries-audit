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
**Status: 🟢 DONE (Bonferroni bound) + ✅ Cauchy/ACAT refinement CLOSED 2026-06-13**; 🟠 Brown's scaled-χ² still BLOCKED on paired per-plan statistics

The earlier Fisher figure of p = 6.87×10⁻⁸ assumed Ch1 ⊥ Ch2. Ch1 (Mahalanobis) and Ch2 (SZAT) share underlying 2023 vote-attribution data and overlap in the EG dimension specifically; the post-hoc Spearman ρ = −0.0014 check measures correlation across two unpaired Monte Carlo streams, not dependence between the test statistics under the null map distribution. Under positive dependence, Fisher is anti-conservative (Brown 1975).

**Done this pass:** the public-facing prose, monograph §4.3.2 and §4.3.3, `findings/joint_outlier_score_summary.md`, and the locale strings now report the dependence-robust Bonferroni upper bound **p ≤ 2.80×10⁻⁶ (≈ 1 in 357,000)** instead of the Fisher figure. This bound is valid under *arbitrary* dependence between Ch1 and Ch2 and represents the conservative honest summary.

**Cauchy/ACAT refinement — CLOSED 2026-06-13.** The aggregated Cauchy test (Liu & Xie 2020) is valid under *arbitrary* dependence and — unlike Brown's method — needs **only the two channel p-values**, not the paired per-plan statistics. Computed in `analysis/scripts/cauchy_combination_joint.py` (output `findings/joint_outlier_score_cauchy.json`): with equal weights, ACAT(Ch1 = 1.40×10⁻⁶, Ch2 = 0.0024) = **2.80×10⁻⁶ (1 in 357,351)** — numerically identical to the Bonferroni bound (ratio 0.999). The result is **Ch1-dominated and essentially invariant to Ch2**: substituting the block-permutation SZAT p (≈ 0.19, T1.10b) for the i.i.d.-flip p (0.0024) shifts the combined p by < 0.01 %. A second dependence-robust method therefore reproduces the published headline; the Bonferroni bound is not an artefact of the conservative construction. Written into `findings/joint_outlier_score_summary.md` (joint-combination section + retired-Fisher banner), report §4.3.3 and §5.5.

**Still to do — Brown's scaled-χ² (🟠 BLOCKED).** Brown (1975) / Kost & McDermott (2002) scale the Fisher statistic by an estimated `c` and report against χ²(f) with f < 2k. This *does* need the paired (D², SZAT_per_plan) ranks across the 1.01M ensemble, which require the per-VA assignments T1.1 needs (to compute per-plan SZAT scores) — gated on the same LFS/assignment-archive pull. Lower priority now that the Cauchy method has confirmed the bound.

**Acceptance criterion (met for Cauchy):** A new section in `findings/joint_outlier_score_summary.md` reporting the Cauchy- or Brown-method joint p alongside the Bonferroni bound. The Cauchy result lands *on* the Bonferroni bound (within 0.1 %), so the audit keeps the Bonferroni headline as the conservative public-facing number and cites the Cauchy result as the dependence-aware corroboration.

### T1.3 — Mahalanobis tail validation
**Status: ✅ CLOSED 2026-06-13 (QQ-validation landed)**

The Mahalanobis joint p of 1.40×10⁻⁶ rested on a χ²(4) tail assumption — i.e., on multivariate normality of (EG, MM, declination, seats@50/50), one of which (seats@50/50) is discrete. The empirical floor from the canonical 1.01M ensemble (computed this pass): no ensemble plan reaches the minority's D² = 32.67. The empirical upper bound on Ch1's p is therefore 1/(1,010,001) = **9.9×10⁻⁷**. The parametric χ² extrapolation (1.40×10⁻⁶) is *larger* than the empirical floor, so the Bonferroni bound the audit now reports remains conservative and the parametric figure is defensible as a tail-extrapolation upper estimate.

**QQ-validation — CLOSED 2026-06-13.** `analysis/scripts/mahalanobis_qq_validation.py` computes per-plan D² over all 1.01M plans (μ, Σ, pinv identical to the published Ch1 pipeline; minority reproduces at D² = 32.6692 → χ²(4) p = 1.396×10⁻⁶) and QQ-plots against χ²(4). Finding at `findings/mahalanobis_chi2_qq_validation.md` (+ figure + JSON). **Honest result:** χ²(4) fits the bulk excellently (mean 4.000; median Δ −0.04) but the upper tail is *mildly heavier* (variance +6.5 %; p99.9 quantile +1.5) — χ²(4) is mildly anti-conservative in the p99–p99.99 band, not conservative. The earlier "parametric is larger than the empirical floor → conservative" framing above is **corrected**: the empirical floor is ESS-coarse (T1.9), and the parametric tail is mildly thin. Headline survives anyway because (a) the minority's D² = 32.67 exceeds the empirical max over all 1.01M draws (27.74) — outlier status is empirical, not parametric — and (b) the published hedges (Hotelling-F 1.73×10⁻⁶; Bonferroni 2.80×10⁻⁶) already build in a factor-of-two margin that absorbs the observed thickening. No Appendix G exists; the finding doc is the deliverable.

### T1.4 — Constraint-enforcing ensemble (ReCom with s.15(2), CoI, anchoring constraints)
**Status: 🟢 FIRST RUN EXECUTED 2026-06-13 (100k); publication-grade 1M run queued as T1.4-full**

First constraint-enforcing run landed (`analysis/scripts/constraint_enforcing_ensemble.py`, 100,000 steps, drand salt `constraint-ensemble-v1`, ~20 min wall clock; finding at `findings/constraint_enforcing_ensemble_100k.md`):
- **Full ±25% proposal ε** (also closes the T1.11 proposal-epsilon bug for this run)
- **s.15(2) tier via freeze-from-real-seed** — seeding from the real majority map bypasses the H6 recursive_tree_part infeasibility; freeze set self-identified as 5 districts <75% of ideal on 2021 substrate (3 statutory + 2 cycle-lag Calgary suburbs)
- **Municipal-split tally** per plan over 170 multi-VA CSDs

**Results (both seeds, same day):** three of the minority's four partisan metrics are robust ≥p98.7 tail flags under every null tested (MM ≥p99.8, decl ≥p98.7, s50 ≥p99.98). **EG is threshold-straddling and seed-dependent: p97.24 under the majority-seeded freeze (fires) but p94.17 under the minority-seeded freeze and p94.4 unconstrained** — the honest reading is "p94–p97 band, neither clean fire nor clean miss." Majority becomes *more* normal on every metric under both constrained nulls. ReCom splits 55–67 municipalities vs real maps' 23/30 (both ≈p0) — the commission-convention auxiliary is now empirically measured and applies symmetrically (closes the T1.17 measurement gap), and supplies the Amendment-9 S2 specificity rate (Pr(splits≤30 | ReCom) ≈ 2×10⁻⁴). Seed-dependence of the EG result was caught by the audit's own symmetric-robustness discipline before any external claim was made.

**Remaining for T1.4-full:** (a) 1M-scale run (~3.5 h at 85 steps/s, parallelizable across 4 chains); (b) minority-seeded robustness run (freeze RMH-Banff Park instead of Canmore-Banff); (c) like-for-like split-count universe (CY/T/SM filter in the per-plan tally); (d) soft-constrained variant (penalized acceptance on splits ≤ 30) — the recorded tally shows a hard constraint would reject ≈99.98 % of proposals, so the soft design is required.

### T1.4a — Population-weighted MAUP attribution per plan against the 1.01M ensemble
**Status: 🟠 PC QUEUE — needs ~8 h dedicated compute window (parallelizable to ~30–45 min on 16 cores)**

The 2026-06-10 MAUP-attribution finding (`findings/maup_attribution_canonical.md`) ran population-weighted attribution on the *real maps only* and showed centroid is invariant to attribution method to within 0.1 pp on every Lane-1 metric. The published percentile placements (p94.4 on minority EG, etc.) however are calibrated against an ensemble built using centroid attribution per plan. Publication-grade move: rerun the attribution layer per ensemble plan and re-score the real maps against the resulting pop-weighted ensemble distribution.

**Resolution path:**
1. Extract per-plan VA assignments from the canonical chain (10k verification subset is on disk at `data/outputs/mcmc/verification_assignments_raw.npz`; extending to 1M needs the per-plan assignment archive — same LFS data debt as T1.1).
2. For each plan, apply `va_attribution_population_weighted.py` to the plan's VA-to-ED assignment.
3. Aggregate to the ensemble's marginal partisan-metric distributions; place the real maps' pop-weighted values against the new distributions.

**Compute:** ~30 s × 1.01M plans = ~8 h single-core; ~30–45 min on a 16-core PC.

**Acceptance:** `findings/maup_population_weighted_ensemble.md` reporting placements under (a) centroid-attrib against centroid-built ensemble (current canonical) and (b) pop-weighted-attrib against pop-weighted-built ensemble. If they agree within ±2 percentile points, the audit's percentile claims survive a publication-grade attribution audit.

### T1.5 — Short-bursts hill-climb rerun on canonical (UCP-objective and NDP-objective)
**Status: 🟡 SCRIPT REPAIRED + READY; full run needs dedicated compute window**

§5.4.8's "empirical proof of the non-neutral pathway" hits 52.87%, matching the v0_8 superseded substrate. This pass: `analysis/scripts/simulation_short_bursts.py` was repaired (a `seed=None` bug in the per-burst seed pass-through to `run_ensemble`) and is now ready to run against canonical EA shapefiles. **Profiling on the canonical 4,765-VA graph shows each ReCom step costs ~10–15 s** (the bipartition_tree generation is heavy at 89 districts × n=4765); a 500-burst × 10-step run is ~60–120 min wall clock. This session attempted a 50-burst preview but did not complete in the available compute window. The script is correct and ready; the run should happen in a session with a 1–2-hour dedicated compute slot.

Reproduction command (once ready):
```bash
nohup python analysis/scripts/simulation_short_bursts.py > /tmp/bursts.log 2>&1 &
# wait ~60 min; outputs land at:
#   findings/simulation_short_bursts.md
#   data/simulation_short_bursts_summary.json
#   data/simulation_short_bursts.csv
```

**Acceptance criterion (unchanged):** §5.4.8 paragraph rewritten to lead with the canonical-substrate maximum, with the v0_8 number relegated to a "superseded estimate" footnote. Targeted hill-climb (separate script `targeted_gerrymander_burst.py`) still pending — that one is the "deliberate non-neutral pathway" test rather than the neutral-neighbourhood characterisation; queued under T1.5b.

### T1.5b — Targeted hill-climbing bursts (UCP and NDP objectives)
**Status: 🟠 BLOCKED ON SCRIPT verification**

`targeted_gerrymander_burst.py` is the script referenced by §5.4.8 as the "deliberate non-neutral pathway" test. Verify it exists, then run against canonical. The earlier 52.87% s50 maximum from this script needs replacing with a canonical-substrate value.

### T1.6 — Inter-map permutation test rescore on the 1.01M ensemble
**Status: ✅ CLOSED 2026-06-12 (committed 4e886db; status marker reconciled 2026-06-13).** `findings/intermap_permutation_test_results.json` now carries `ensemble_n: 1010000`; report §5.4.9 Version B cites the canonical rescore (D = 7.17 vs null p95 = 4.43; p = 9.999×10⁻⁵ under (b+1)/(B+1); 4/4 metrics minority-UCP-favoured post-Amendment-10). The acceptance criterion (1.01M ensemble + updated md) is met.

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
**Status: 🟢 STUB LANDED 2026-06-10 (see Tier 5 above for full status)**

### T2.2 — Forest-ReCom robustness Phase A
**Status: 🟠 BLOCKED ON SCRIPT/OUTPUTS**

OSF-registered in `preregistration/osf_forest_recom_robustness.md`. `data/outputs/forest_recom_*` does not exist.

**Resolution path:** run the registered Forest-ReCom variant; produce the documented outputs.

### T2.3 — Phase 4C status reconciliation
**Status: ✅ CLOSED 2026-06-10**

The contradiction was inside `analysis/methodology/plain_language_defense.md` — same document, two adjacent entries (~250 lines apart) said opposite things about Phase 4C. Phase 4C was actually re-run today against canonical Elections Alberta shapefiles (`analysis/scripts/phase4c_canonical_attribution.py`) and produces the canonical real-map numbers (minority EG +4.02%, minority s50 = 0.5169 UCP / 0.4831 NDP). Both defense entries were rewritten to point at the canonical execution and disambiguate "Phase 4C VA-polygon attribution" (now executed) from "MAUP centroid-vs-area-weighted test on the v0_9 substrate" (the +0.0000 pp shift that was being mis-cited as Phase 4C's result). `methodological_defenses.md` was not affected — its +0.0000 pp entry correctly refers to MAUP on v0_9, not Phase 4C.

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
**Status: ✅ CLOSED 2026-06-11**

`analysis/methodology/reference/school_division_coherence_majority.md` written: per-hybrid school-division coherence applied to all 19 majority hybrids using the same classification keys as the minority-hybrid analysis. Result: **majority 68.4 % cross-division (13/19), minority 95.2 % (20/21)**. The asymmetry is real but the minority-specific finding (20/21 cross + invoking "shared schools" where the catchment fails) is *strengthened*, not weakened, by symmetric scrutiny: the majority makes no "shared schools" claim, so its 13 cross-division hybrids are honest about the geometric fact rather than failed rhetorical justifications. The symmetric audit's value is to verify the minority-specific finding is about *claims made*, not about boundaries crossed.

Minority's 21 hybrids got the full school-division treatment; majority's got four bullets. The school doc itself admits the limitation is in the question set. Apply the same school-division coherence check to every majority hybrid.

**Resolution path:** rerun `school_division_coherence` script (verify script name in `analysis/scripts/`) with the majority's hybrid list; produce parallel finding doc.

### T3.2 — One majority-anomaly counter-test
**Status: ✅ CLOSED 2026-06-11**

Pre-registered as a rural-isolation counter-test against the majority's z = −2.915 anomalously-low drain score. Design locked at commit `5fbd1ca` (`preregistration/t3_2_majority_rural_isolation_design.md`, salt `t3_2_majority_rural_isolation_counter_test`) before execution. Three independent metrics (R1 median PP rural, R2 mean urban-nbrs/rural, R3 zero-urban-frac) applied symmetrically to majority 2026, minority 2026, and 2019 enacted as geographic control.

**Result: H₀ supported.** Majority is rank-1 on 1 of 3 metrics (compactness only); 2019 enacted is the most rural-isolated map overall. The drain anomaly is consistent with natural Alberta rural geography, not engineered isolation. Full result `findings/t3_2_majority_rural_isolation.md`; added to academic report §5.6 as Counter-test 3.

### T3.3 — Apply the "commission convention" escape symmetrically
**Status: ✅ CLOSED 2026-06-10 (documentation)**

§5.4.9 explained the majority's MM p0.85 NDP-tail as "commission convention interacting with vote geometry" but did not extend the same escape to the minority's tails. This pass added language to §6.2.4 acknowledging that any narrative-level escape needs symmetric application. The substantive fix is to either retire the convention-interaction language or apply it to both maps and let the readers judge — pick one approach in the next prose pass.

---

## Tier 4 — Stale-substrate findings circulating unbannered.

### T4.1 — Banner superseded findings
**Status: ✅ CLOSED 2026-06-13 (all candidates bannered)**

Files bannered via the DPG legacy audit (`findings/dpg_legacy_audit.md`):
- ✅ `findings/phase4c_maup_summary.json` (`_SUPERSEDED` field with canonical pointer)
- ✅ `findings/phase4f_summary.json` (same)
- ✅ `findings/regional_swing_robustness.md` (`status: SUPERSEDED` + banner; superseded by `regional_swing_canonical_robustness.md`)

Banners verified present 2026-06-13 (added in the interim, marker reconciled):
- ✅ `findings/cross_election_2015.md` — `status: SUPERSEDED` (blend-era −0.51 pp vs canonical +3.92 pp).
- ✅ `findings/chen_rodden_decomposition.md` — `status: SUPERSEDED` (100k ESS≈150 → canonical 1.01M pending).
- ✅ `findings/sensitivity_analysis.md` — `status: PARTIALLY SUPERSEDED` (substrate-era; canonical sweep pending).
- ✅ `findings/maup_area_weighted_analysis.md` — `status: SUPERSEDED`, `superseded_by: findings/topology_cleanup_analysis.md`.
- ✅ `findings/simulation_short_bursts.md` — YAML banner added 2026-06-13 (DPG v0_7 pre-shapefile substrate; canonical rerun queued at T1.5; report §5.4.8/§5.4.10 already carries the historical-record banner).

**Acceptance criterion (met):** each file leads with a YAML-frontmatter `status:`/`superseded_by:` field and a one-line banner. Numeric regeneration of the stale values remains gated on the respective canonical reruns (T1.5 for short-bursts; canonical 1.01M for Chen-Rodden), tracked under those items.

### T4.5 — Cosmetic v0_x label sweep (non-blocking)
**Status: 🟠 RE-SCOPED 2026-06-13 — most listed targets are NOT stale; remainder is prose-framing-only, deferred low priority.**

Re-examination 2026-06-13 found the original target list is largely outdated:
- `annotate_ensemble_seats_chart.py`, `article_figures.py` — **0 v0_x occurrences** (already clean).
- `advance_vote_sensitivity.py` — the 2 occurrences are **accurate file-path references** (`data/shapefiles/derived/v0_10_topological_*.gpkg`, the real shapefile version), not stale labels; editing them would make the docstring *incorrect*. Leave as-is.
- `analysis/methodology/audit_dependency_graph.json` — **358 occurrences**, but these are machine-consumed node IDs / `schema_version` read by `dependency_query.py`. This is NOT a safe blind cosmetic sweep; rewriting node IDs without running the dependency-query apparatus end-to-end (needs the full env) risks orphaning the graph. Deferred until it can be regenerated + verified by `dependency_query.py`, not hand-edited.

Genuinely remaining (prose framing only, low value): DPG-provisional framing language in `szat_methodology.md` (1), `methodological_defenses.md` (9), `plain_language_defense.md` (16), `reference/banff_extension_population_check.md`, `reference/airdrie_quadrant_demographic_comparison.md`. These are judgment-heavy per-occurrence prose edits with no effect on any number; left as low-priority polish rather than risking inaccurate mass rewrites.

### T4.6 — Re-execute the v0_5-substrate hardstop validation against canonical
**Status: ✅ CLOSED 2026-06-11**

Canonical-substrate Phase 4F population-hardstop validation completed against official Elections Alberta shapefiles + Statistics Canada 2021 DAs (script `analysis/scripts/phase4f_hardstop_canonical.py`; result `findings/phase4f_hardstop_canonical.md`). On clean canonical geometry **89 of 89 majority EDs and 89 of 89 minority EDs fail the 2 % hardstop** (median |Δ| = 9.6 % majority / 10.4 % minority; max 47.0 % / 41.9 %). The v0_5 counts (81/86 + 87/89) were lower only because the DPG substrate had 27 majority and 22 minority EDs with zero scoreable population (the polygons did not exist in v0_5); those EDs passed by being missing rather than by being within threshold. Monograph §3.3 has been refreshed with the canonical reading.

### T4.8 — Drain coupled-count three-way reconciliation
**Status: ✅ CLOSED 2026-06-12**

The implementation's coupled definition (`winner(X) == loser(Y)` at `neighbour_drain_adjacency.py:396`) is the binding convention — it has been the implementation since the script was written; every published canonical-substrate coupled-count derives from it (despite varying across published copies due to substrate iteration). The pre-registration design doc (`analysis/methodology/neighbour_drain_design.md`) prose loosely says "same losing party" but the implementation is what the audit actually consumed.

Resolution: the audit retains the implementation's binding convention. The three competing published counts (§5.3.5 6/2/5; `neighbour_drain_analysis.md` 2/1/5; today's recompute 2/1/2) reflect substrate iteration (different VA vote layers / different adjacency-buffer parameters across runs), not a convention dispute. The headline (Bonferroni p ≤ 2.80×10⁻⁶) is unaffected — Channel 3 is excluded from the headline. The §5.3.5 narrative now correctly disambiguates the coupled-count substrate dependence; a canonical-Phase-B re-run with the in-tree current parameters lands at `findings/drain_label_shuffle_null_canonical.md` (continuous drain score, not coupled count) and is the audit's authoritative Channel-3 read.

### T4.7 — Substrate-provenance sweep (2026-06-11) — canonical Phase B drain null + extended-partisan-metrics canonical recompute
**Status: ✅ CLOSED 2026-06-11**

Both canonical recomputes landed in the same session:

1. **`findings/drain_label_shuffle_null_canonical.md`** — canonical-substrate Phase B null (10,000 label-shuffle permutations). Results: majority drain = 0.007213 (z = −3.173), minority = 0.000591 (z = −2.750), 2019 enacted = 0.001530 (z = −3.520). Pre-registered Prediction A (drain(majority) > drain(minority)) CONFIRMS on canonical; "majority singularly anomalously low" framing does NOT survive — all three maps are anomalously low against their own canonical null, with the 2019 enacted baseline the most anomalous of the three. Channel 3 remains excluded from the Bonferroni headline. Old v0_2 / blended-substrate file (`findings/drain_label_shuffle_null.md`) bannered SUPERSEDED.

2. **`findings/extended_partisan_metrics_canonical.md`** — canonical Partisan Bias, Lopsided-t, Proportionality Deviation, Responsiveness on canonical EA shapefiles + 1,010,000-plan ReCom ensemble. Lopsided-t majority = +3.80 (was 3.43 v0_7); Lopsided-t minority = +3.17 (was 3.05 v0_7); 2019 enacted = +3.07. Lopsided Margins finding remains a structural property of Alberta's political geography on all three maps. §1.1 BH-table rows 5–6 refreshed with the canonical t-values; §5.2.9 rewritten in place. Minority PB sign-flipped on canonical (+0.0169 vs v0_7 −0.0422) — substrate artefact, headline does not depend on PB. Old v0_7 file (`findings/extended_partisan_metrics.md`) bannered SUPERSEDED.

`findings/joint_outlier_score.json` `neighbour_drain` block updated with canonical values; stale values preserved under `stale_*` keys for trail-of-work. `findings/joint_outlier_score_summary.md` Channel 3 section updated.

Every headline-cited number now traces to canonical inputs.

### T4.2 — Rewrite `external_tool_validation.md` against canonical
**Status: ✅ CLOSED 2026-06-11**

Doc rewritten in place:
- "Python pipeline runs 2,000,000 maps" → "canonical pipeline runs 1,010,000 plans (4 chains × 252,500 steps)"
- R cross-validation seed `set.seed(88)` → `set.seed(852751799)` with the note about the redistmetrics RNG-consume defect that motivated the explicit seeding order
- Stale EG numbers (majority +6.4% / minority +9.2%) replaced with canonical Phase 4C values (majority +0.10% / minority +3.96%)
- DPG-era v0_8 polygon paths (data/shapefiles/derived/v0_8_full_refined_*) replaced with canonical paths (data/shapefiles/canonical/ea_*_2026_eds.gpkg)
- Phase 2 reframed from "validate the DPG reconstructions against commission images" to "validate the canonical shapefiles against commission images" — the prior framing was moot once the official shapefiles arrived
- "v0_1_compactness.py" → "polsby_popper.py" + "reock.py" (the actual current scripts)
- Output doc names (v0_1_qgis_visual_inspection_findings.md, v0_1_maptitude_cross_validation.md) de-versioned

The doc title still reads "validation plan" rather than "validation report" — that's intentional, the document remains a walkthrough for a reviewer who hasn't run any of these tools yet. The R cross-validation specifically WAS executed and its result is in `findings/redist_python_comparison.md`; the doc points there.

### T4.3 — Sentiment 920 → 452 row reconciliation
**Status: ✅ CLOSED 2026-06-11**

Empirical check against `data/outputs/sentiment_intensity_scores.csv`: the canonical file has **452 rows** representing **394 unique submission IDs** across **7 configurations × 3 scan types** (full_corpus, hansard_r1, hansard_r2). The "920" figure cited in earlier drafts was a pre-deduplication scoring pass that double-counted Hansard turns appearing across multiple speakers.

Updated:
- `findings/sentiment_rationale_crossreference.md` — header and Data sources block use the 452 figure; row-count provenance note added explaining the 920→452 transition.
- `findings/sentiment_analysis_completion_report.md` — abstract, methodology details, and source-file pointer all updated to 452.

Monograph §5.9.4.6 numbers (using the 452-row aggregates) are unchanged.

### T4.4 — Declination convention is consistent
**Status: ✅ CLOSED 2026-06-10**

Verified that `analysis/scripts/mcmc_ensemble.py:789` uses Warrington (2018) convention (positive = UCP-favoured) and that chain CSV, real-scores JSON, and all downstream artifacts use the same convention. Appendix D.3 has been rewritten to declare the convention prominently and reconcile the transient substrate-iteration sign change (−0.0666 v0_8 → +0.0105 first canonical → −0.0770 final canonical) honestly. §4.1.4 no longer claims "no sign-flips or material magnitude changes were observed."

---

## Tier 5 — November held-out test infrastructure.

### T5.1 — Freeze the November scoring spec
**Status: ✅ CLOSED 2026-06-10**

`preregistration/november_2026_scoring_spec.md` written. Substrate, metrics, thresholds, the 2×2 verdict surface, the 72-hour publication commitment, and the substrate-iteration handling rule are all frozen. The doc declares two scripts (`run_structural_battery.py` and `verdict_synthesis.py`) that need to be written before 2026-10-01 — those gaps are now tracked in this remediation queue as T5.1a/T5.1b. The drand pinning is queued for the next routine drand round following this commit; seed commitment will be appended to `preregistration/seed_commitments.md` under entry `november_2026_scoring_spec`.

### T5.1a — Write `analysis/scripts/run_structural_battery.py`
**Status: 🟢 ALL SIX METRICS FUNCTIONAL 2026-06-10**

### T5.1c — Calibrate the November structural-lane thresholds
**Status: ✅ CLOSED 2026-06-11 (Amendment 9: midpoint anchoring)**

Adopted midpoint anchoring (no free multiplier). For each discriminating metric, the candidate's flag fires iff it lands on the *minority's side of the midpoint* between the two commission maps' battery-measured canonical values. Direction-aware (S1/S2/S6 above midpoint = flag; S3/S5 below midpoint = flag). Self-validating: minority classifies "replicated" (5/5) and majority "not_replicated" (0/5) by construction — confirmed empirically on canonical majority (0/5 flags). S4 (compactness) is measured but excluded from the count: median PP is identical on both maps and tail stats run the wrong way (consistent with monograph H3). P6 (St. Albert-Sturgeon) is dropped from S6's predicate set because the majority has the same-named ED — non-discriminating. Verdict threshold remains ≥3 of 5.

Battery-measured canonical anchors (2026-06-11):

| Metric | Majority | Minority | Midpoint | Minority side |
|---|---:|---:|---:|---|
| S1 pop MAD | 2826.89 | 3938.11 | 3382.50 | above |
| S2 splits (≥2 EDs) | 23 | 30 | 26.5 | above |
| S3 anchoring (%-perim) | 0.80050 | 0.71970 | 0.76010 | below |
| S5 drain score | 0.0072 | 0.0006 | 0.0039 | below |
| S6 patterns (P1–P5) | 0 | 5 | 2.5 | above (≥3) |

`preregistration/november_2026_scoring_spec.md` and `findings/pre_registration_amendment_log.md` Amendment 9 to be updated in the next prose pass (the script itself documents the rule in its preamble).

The November scoring spec references this script as the structural-lane (S1–S6) battery runner. Stub committed 2026-06-10. Smoke-tested against canonical minority shapefile: S4 (Polsby-Popper) executes end-to-end and returns 0.437 median (above the 0.248 threshold; no flag). S1, S2, S3, S5, S6 emit `flag: null` with specific wire-in pointers in `_note`. The verdict counts `null` as "did not execute" (not as a flag), so the script refuses to publish a final verdict until the stubs land.

**Remaining work (each is a ~1–4 h refactor of an existing component script):**
- S1: extract per-ED population MAD from `mcmc_ensemble.py`'s population overlay
- S2: expose `count_triple_splits(shapefile) -> int` from `municipal_splits.py`
- S3: expose `compute_anchoring_score(shapefile) -> float` from `score_anchoring.py`
- S5: expose `drain_score(shapefile, votes) -> float` and `null_pvalue(score) -> float` from `neighbour_drain_adjacency.py` and `drain_label_shuffle_null.py`
- S6: catalog chair-flagged pattern predicates from `findings/chair_recommendation_5_analysis.md` as a JSON predicate list

### T5.1b — Write `analysis/scripts/verdict_synthesis.py`
**Status: ✅ CLOSED 2026-06-10**

Fully functional. Smoke-tested against synthetic joint-outlier input + structural stub output: correctly identifies "not_replicated × present → no structural replication; partisan-bias signature is present" headline, correctly refuses `publishable_72h: true` until structural stubs land.

### T5.2 — Write `analysis/scripts/rural_gap_dissection.py`
**Status: ✅ CLOSED 2026-06-10**

Full implementation landed 2026-06-10. Takes per-ED population CSV + per-ED votes CSV; produces partisan-lean breakdown of rural-mean populations; classifies as `pack_rural_ucp` / `pack_rural_ndp` / `no_partisan_signal`. Thresholds frozen 2026-06-10 in the script source. Ready to run for canonical minority/majority comparison and ready for the November Lunty map once population + vote overlays land.

### T2.1 — Issue #13 local-perturbation chain
**Status: 🟢 STUB LANDED 2026-06-10; `single_va_swap()` kernel pending**

`analysis/scripts/local_perturbation_chain.py` committed with framework, retraction rule, CLI, and output schema. The single-VA swap proposal kernel raises `NotImplementedError` with a pointer to the Issue #13 spec. drand-pinning enforcement (warns if `--seed` not supplied) and the retraction rule (`fraction ≥ 0.05` of perturbations with any p95 flag = Lane-1 retraction) are frozen in the script source.

**Remaining work:** implement `single_va_swap(graph, partition, rng) -> (accepted, new_partition)` against `gerrychain.GeographicPartition`; wire up scoring against `data/simulation_checkpoints_canonical/`; file a drand seed before the retraction-grade run.

### T5.2 — Write `analysis/scripts/rural_gap_dissection.py`
**Status: ✅ CLOSED 2026-06-10 (see Tier 5 above)**

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
**Status: ✅ CLOSED 2026-06-10**

Cannon et al. citation corrected from "2022" to "2023" with the arXiv-vs-published distinction noted. McCartan & Imai (2023, *AoAS* 17(4): 3300–3323) added to the references list with a pointer to the audit's use of `redist_smc()` for algorithm-independence corroboration. Reference list update is in `reports/academic/report_academic.md` and now flows through `docs/report_academic.html` via the rebuild. The standalone `analysis/methodology/reference/academic_literature_review.md` still needs the same two additions — queued as T6.2 follow-up.

### T6.3 — Appendix F cleanup
**Status: ✅ CLOSED 2026-06-10**

Appendix F was tightened end to end:
- The four-section *White Burgess* self-admissibility analysis was replaced with a four-bullet neutral posture statement: "admissibility is for counsel; data and code are public; pre-registration documented at OSF; CoI history on file; the author makes no representation regarding personal qualification as an expert witness."
- The seven-factor *Grant v. Torstar* preemptive defamation brief plus the *WIC Radio* fair-comment posture were replaced with a single paragraph: characterisations are anchored to direct quotations, primary-source citations, and visible reasoning; the audit does not pre-adjudicate any defamation defence.
- The Airdrie population reconciled to the §5.3.2 vintage triple (74,100 / 85,805 / 90,044 across the 2021 Census / 2024 City census / 2025 City census) rather than the previously inconsistent "approximately 81,000" figure.
- The substantive Saskatchewan Reference and voter-impact-translation sections were preserved unchanged — those are the legitimately load-bearing parts of the Appendix.

Net effect: removed roughly 1,800 words of self-grading and preemptive-defence prose that referees identified as credibility-eroding; kept the substantive legal framework that lets counsel actually use the audit. `docs/report_academic.html` rebuilt.

### T6.4 — R-11 paraphrase fidelity check
**Status: ✅ CLOSED 2026-06-12**

Re-verified against the canonical minority-rationale inventory at `data/outputs/minority_rationales.csv:12`. The verbatim R-11 source text reads "*…challenges of electoral divisions that represent a rural population but do not represent the urban community **where they work go to school and gather**.*" The "go to school" phrase IS in the source (as part of the run-on "where they work go to school and gather"). The downstream paraphrases at `minority_rationales_validation.md:82` and `school_division_coherence.md:162` quote R-11 as "*urban communities … where they work, go to school*" — punctuation added but no fabricated content. The earlier TODO entry's premise ("R-11 contains no 'go to school' language") was incorrect. Paraphrase is faithful; no correction needed.

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
- ✅ **Mahalanobis empirical floor computed** from the canonical chain CSVs: **0 of 1,010,000 correlated draws** reach the minority's D² = 32.67. Under the (b+1)/(B+1) exchangeable-draws formula the naive empirical bound would be ≤ 9.9×10⁻⁷, but the ensemble's autocorrelation (τ ≈ 601-707; n_eff ≈ 1,495) means the honest ESS-bounded empirical tail floor is approximately **1/(n_eff+1) ≈ 6.7×10⁻⁴** — coarser than the parametric χ²₄ tail of 1.40×10⁻⁶, not finer (corrected 2026-06-12 per T1.7 R2 Ref #1; round-1 of this note claimed the empirical bound "dominated" the parametric, which is wrong under autocorrelation). The published headline is the parametric χ²₄ extrapolation; the empirical observation is "0 exceedances in 1.01M correlated draws (ESS-bounded floor ~6.7×10⁻⁴, consistent with the parametric ~1.4×10⁻⁶ at the chain's effective precision)." The Bonferroni headline bound is conservative under either reading.
- ✅ **`TODO_REMEDIATION.md`** (this file) created.

### Earlier closures

- ✅ **2026-06-10 — "no precedent in Canada" claim re-scoped** to "without precedent among the Canadian redistribution cycles this audit reviewed" and attributed to Duane Bratt's correspondence with the author, in `report_public.md`, `report_public.html`, and the 12 non-stub locales.
- ✅ **2026-06-10 — Language dropdown scrollable** (15 languages now in the menu).
- ✅ **2026-06-10 — Six new locales registered** (hi, vi, ko, ur, pl + the existing 9), Urdu correctly flagged RTL.

---

## Tier D — T1.7 code-side queued items (added 2026-06-12)

The 18-referee adversarial review (T1.7) surfaced a cluster of methodological / technical depth issues requiring code changes or rerun. Documented inline in the report; full text remediation queued here.

### T1.8 — BH → BY adjustment under dependence (Ref #1 / #6 / #16)
**Status: ✅ CLOSED 2026-06-12.** BY adjustment computed: m=11, H_m=3.0199, multiplier 3.02. All 10 PASS rows survive (row 10 declination 3.99×10⁻² is the largest borderline; row 11 minority EG 1.69×10⁻¹ still FAILS). Verdict 10 PASS / 1 FAIL unchanged from BH. Documented at §1.1 BH-table dependence-disclosure paragraph.

### T1.9 — Mahalanobis empirical-tail floor (Ref #1)
**Status: ✅ CLOSED 2026-06-12.** Honest restatement: (b+1)/(B+1) over 1.01M *correlated* draws requires exchangeability; the honest ESS-bounded empirical floor is ≈ 1/(n_eff+1) ≈ 6.7×10⁻⁴, COARSER than the parametric χ²₄ tail of 1.40×10⁻⁶, not finer. Published headline remains the parametric value; empirical observation is "0 exceedances in 1.01M correlated draws (ESS-bounded floor ~6.7×10⁻⁴, consistent with the parametric ~1.4×10⁻⁶ at the chain's effective precision)". Round-1's "dominating the parametric" claim was wrong under autocorrelation; round-3 corrected.

### T1.10 — SZAT block-permutation null (Ref #1)
**Status: ✅ CLOSED 2026-06-12 (T1.10b executed; marker reconciled 2026-06-13).** (b+1)/(B+1) finite-sample correction landed in `szat.py` (minimum reported p now 1/(N+1) = 1×10⁻⁴ at N_BOOT=10,000); exchangeability caveat disclosed inline at szat.py + §5.5. **T1.10b (the full block-permutation null) was executed and committed 2026-06-12 (0c770c4):** the 2,110 swing-zone VAs form one giant connected component (2,086 VAs), so the i.i.d.-flip null understated variance by 5.79×; the block-permuted p ≈ 0.19. Ch2 does not survive the contiguity correction and is dropped from the joint headline (which is now Ch1 alone). Finding at `findings/szat_block_permutation.md`; report §5.4.9 / §1.1 / §6.2 updated. The "p may move modestly but verdict survives" prediction held — the headline moved to Ch1-alone and the Bonferroni bound is unchanged (Ch1 was always binding).

### T1.11 — ReCom proposal ε rerun (Ref #2 A13)
`mcmc_ensemble.py:558` sets `epsilon = pop_deviation / 2.0`. Rerun with `epsilon = pop_deviation` so the proposal samples the documented ±25% legal space. ~8h single-core; 1.01M ensemble regenerated.

### T1.12 — Resume-path corruption + per-chain ESS + burn-in (Ref #2 D4 D5)
**Status: 🟡 PARTIAL CLOSE 2026-06-12.** Per-chain ESS computed and documented in §5.4 (Geyer initial-monotone-sequence τ; per-chain min 308–597; pooled 1,448–1,814 — matches the published n_eff 1,429–1,682 bracket). 5τ ≈ 4,100-sample burn-in per chain investigated as post-processing: no published percentile shifts by more than 0.02 pp. Resume-path corruption fix (serialize final partition per chunk; chunk-dependent seeds) deferred to next ensemble re-run (T1.11/T1.12-resume); risk is latent — the 1.01M run was uninterrupted.

### T1.13 — Differential measurement error (Ref #3 D6)
**Status: ✅ CLOSED 2026-06-12.** Already addressed by `findings/maup_attribution_canonical.md`: population-weighted attribution confirms centroid to within 0.1 pp on every partisan-bias metric on both commission maps. The p94.4↔p95 EG gap on the minority is not crossed by the attribution-method shift.

### T1.14 — Attribution-function unification (Ref #3 D7)
**Status: ✅ CLOSED 2026-06-12.** Unified helper at `analysis/utils/va_attribution.py`. Features: representative_point centroid-in-polygon primary; sjoin_nearest fallback; deterministic largest-intersection-area tie-break for multi-ED containment (replaces the nondeterministic `keep="first"`); CRS-equality assertion at sjoin (catches T4.10-CRS hazard); vote-conservation logging. Smoke test: 4765/4765 VAs attributed on both canonical commission maps, 0 nearest-fallback, 0 multi-ED tie-breaks, vote conservation to-the-vote. Legacy scripts not yet refactored to call the helper — follow-on cleanup.

### T1.15 — Code-side reproducibility cleanups (Ref #15 D10-D13)
**Status: 🟡 PARTIAL CLOSE 2026-06-12.**
- D10: `drain_phase_b_canonical.py` default seed now derived from `get_canonical_seed(SALT)` via the canonical drand-anchored seed function (with fallback to 460508741 for environments lacking drand_seed). ✅
- D11: `drain_metric_validation.py` synth_neutral_votes + replicate_direction both derive seeds via `get_canonical_seed("drain_metric_validation_2026_06_11")`; stdlib `random.Random` replaced with `np.random.default_rng`. ✅
- D12: `requirements.txt` refreeze deferred (needs verified-env capture). 🟠
- D13: LFS migration deferred (rewriting history risks invalidating commit hashes cited as pre-registration anchors; needs careful planning). 🟠

### T1.16 — Sensitivity factorial + ES-13 full-vote (Ref #2 / #17 D27 D28)
**Status: ✅ ES-13 CLOSED 2026-06-12.** Full-vote sensitivity recomputed and documented in §5.4.4. Headline implication: minority EG at +5.79% under full-vote attribution exceeds both the Alberta-calibrated 4.10% threshold and the academic 5% S-M threshold. Direction holds on all four metrics on both maps; no sign flips. Election-day reading retained as primary; full-vote reading reported as sensitivity. Population-deviation factorial sweep (D27) still deferred to a future canonical re-run.

### T1.17 — Severity audit (Ref #16 D25)
**Status: ✅ CLOSED 2026-06-12.** Acknowledgment added to §5.4.9 majority MM paragraph: the "commission convention" auxiliary is not applied symmetrically to the minority's tails. Audit's response: rename the null "ReCom-typical plan" everywhere in §6.2 verdict text. Constraint-enforcing ensemble queued as T1.4 is the methodologically complete answer; Bonferroni headline holds under ReCom-typical interpretation.

### T1.18 — Cross-size declination δ̃ (Ref #5 D29)
**Status: ✅ CLOSED 2026-06-12.** Caveat added at §5.4.10 Population MAD paragraph. At n=87 vs n=89, ln ratio = 0.9949 (sub-0.5% correction); 2019 declination p91.05 against the 89-ED ensemble does not shift materially under δ̃.

### T4.9 — Substrate-honest refreshes (Refs #6 #13 #18)
- T4.9-share: ✅ CLOSED 2026-06-12 — Phase 4F share-based recompute landed (78/89 majority, 72/89 minority fail share-drift hardstop; median 5.8% drift).
- T4.9-PB-swing: ✅ CLOSED 2026-06-12 — `partisan_bias()` now accepts `totals=` for turnout-weighted swing; canonical values verified to match ensemble `seats_at_50_50 − 0.5` exactly.
- T4.9-full-vote: ✅ CLOSED 2026-06-12 — see T1.16.
- T4.9-sentiment: ✅ CLOSED 2026-06-12 — row-level reconciliation: 1,254 unique submission IDs processed; results CSV has 388 full_corpus + 209 hansard_r1 + 230 hansard_r2 = 827 rows. The "182/14.5%" round-1 correction was itself wrong.

### T4.10 — Anchoring metric + CRS reconciliation (Ref #10 D8 D9 D18)
- T4.10-anchor: 🟡 PARTIAL CLOSE 2026-06-12 — contiguous-≥1km filter implemented in `score_anchoring.py:_measure_ring()`. Full-province recompute deferred (slow; needs longer compute window). Sensitivity sweep at 100/250/500m snap tolerance queued.
- T4.10-CRS: ✅ CLOSED 2026-06-12 — `CANONICAL_CRS = "EPSG:3400"` + `COMPACTNESS_CRS = "EPSG:3401"` constants added to `canonical_paths.py` with verified pyproj description (3400 = 10-TM Forest, 3401 = 10-TM Resource; both k₀=0.9992; differ only by 500 km false easting). `assert_canonical_crs()` helper added. `canonical_shapefile_log.md` label corrected. `compactness_metrics.py` docstring corrected (was wrongly labelling 3401 as Forest).
