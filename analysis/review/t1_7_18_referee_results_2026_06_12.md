---
title: T1.7 — 18-Referee Adversarial Review (results)
date: 2026-06-12
status: COMPLETE — triage published; remediation queued
commit_reviewed: e6d57c7
review_model: claude-fable-5 (18 parallel adversarial agents)
---

# T1.7 — 18-Referee Adversarial Review (results)

Eighteen adversarial-referee agents (fable-5) were dispatched against the monograph at commit `e6d57c7` (2026-06-11). Each agent had a single specialty and was instructed to surface up to 5 weaknesses with concrete citations to peer-reviewed methodology / case law. **Ninety distinct findings were returned.**

This file consolidates the findings into action tiers and queues remediation. Specialty assignments at the bottom.

## Severity Tier A — Material correction; addressable now

These are findings that change the audit's headline reading or constitute factual errors that should be corrected before any external publicity push. Mostly verifiable in-repo.

| # | Source | Where | Finding | Effect |
|---|---|---|---|---|
| A1 | Ref 5 | `mcmc_ensemble.py:215` + `report_academic.md:447, 2892–2894, 532, 905–932` + `reports/public/report_public.md:271` | Declination implementation sign-flipped vs Warrington 2018. Verified with textbook UCP gerrymander (EG correctly +0.34; δ returns −0.716; Warrington analog +0.54). | Minority δ = −0.0770 / p1.21 is *UCP-favoured tail* (p98.8 properly oriented). B6 *agrees* with B2-B4 → 4-of-4 partisan-bias signals in UCP-favoured tail. "Declination disagrees by design" defense and the public report's "NDP-tail" framing inverted. **Strengthens** the headline, doesn't weaken it. |
| A2 | Ref 8 | `report_academic.md:318, 2140, 2725, 3015` | `Cassista v Canada (AG)`, 2014 FC 398 appears to be a **fabricated citation** — not on CanLII, not in Elections Canada's court-cases index, not anywhere. Used to structure the entire discretion-space architecture in §2 / §5.9.5 / Appendix F. | Either verify the citation (and add the verification to `citation_verification.md`) or excise it everywhere and substitute real authority (Dixon v BC (AG) 1989, Reference re Electoral Divisions Statutes Amendment Act (Alta CA 1994)). |
| A3 | Ref 8 | `report_academic.md:318, 3015` | **Raîche's holding inverted.** Text claims Raîche found a "s.3 violation" and ordered boundaries revisited. Actual Federal Court holding: NO Charter s.3 violation under Carter deference; violations were *statutory only* (EBRA s.15, OLA Part VII). "Heneghan J." attribution unsupported. | Audit loses its only s.3 strike-down anchor. Restate as statutory-reasonableness review; note this *strengthens* commission deference. |
| A4 | Ref 7 | `report_academic.md:766` | **§5.1.5 misquotes s.15(2)** — fabricates a clause ("The Commission may have an electoral division… if the Commission is of the opinion the electoral division should be established") that doesn't exist in the actual statute. Audit's own `terms_of_reference_audit.md:52` carries the correct text ("may have a population that is as much as 50% below…"). | Differential-treatment analysis rests on the fabricated clause. Restate per real statutory text. |
| A5 | Ref 14 | `docs/FINDINGS_BRIEF.md:161-167` | **Inverts the chair-anomaly verdict.** FINDINGS_BRIEF says "the chair's overall concern about the minority map is supported by the record"; the source finding (`reports/public/report_public.md:152`) explicitly says **"This finding cuts against the chair, not against the minority"** (chair right on 3 of 7, wrong on 3, partially wrong on 1). | Public summary directly contradicts its own source. Rewrite. |
| A6 | Ref 12 | `report_academic.md:2051,2056,2094` vs `findings/sentiment_analysis_completion_report.md:40-43,47,212,226-229` | Sentiment coverage claim "all 1,252 parseable submissions classified" contradicted by provenance file: **only 182/1,252 (14.5%) processed**. Published aggregates contradict source: Red Deer −154 vs published −64; Nolan Hill −122 vs −55. | Re-run scan or retract "all 1,252" claim; publish row-level 962/920/452 reconciliation. |
| A7 | Ref 12 | `report_academic.md` R17 quote area | **Fabricated quote appendage** — R17 minority-rationale text quoted with "in the face of sustained urban growth" appended; words absent from archived excerpt `data/outputs/minority_rationales.csv`. Quote verification was explicitly deferred. | Verify or excise. |
| A8 | Ref 7 | `report_academic.md:1294` | Claims "2010 EBC drew the 2019 enacted map." It was the **2017 Bielby commission**, not 2010 Walter. "Dunvegan-Central Peace" is 2010-era naming. The "2/4 used vs 3/4 now" framing anchored to wrong report. | Re-attribute; re-verify "explicitly declining a third" against the 2017 Bielby report. |
| A9 | Ref 8 | `report_academic.md:2333` | **"Rural overrepresentation" labelled gerrymander direction contradicts Carter.** Carter [1991] 2 SCR 158 **upheld** Saskatchewan's deliberate rural weighting; rural over-weighting within ±25% EBCA tolerance is presumptively constitutional, not an irregularity. | Relabel "population-weighting shift (Carter-permissible unless unjustified)." |
| A10 | Ref 8 | `report_academic.md:2390` | §6.2 "fails effective representation" definition smuggles in a *necessity* test: "beyond what geographic constraints *require*." Carter permits deviations *justified* by Carter factors, not only those geography *requires*. | Replace "require" with "be justified by any Carter factor." |
| A11 | Ref 1 / Ref 6 / Ref 16 | `report_academic.md:522-536, 538` | **BH table is mis-sorted + arithmetically wrong + claims "m=11 independent" falsely.** Rank 9 (p=1.2×10⁻²) precedes rank 10 (p=9.8×10⁻³); adjusted-p values violate monotone step-up; Mahalanobis (row 2) is a deterministic function of rows 3, 4, 9, 11 (composite double-counts marginals); rows 5–6 share one substrate. | Re-sort and recompute (conclusions unchanged but the table as printed is not BH); apply BY (Benjamini-Yekutieli 2001) or drop the composite row; strike "independent." |
| A12 | Ref 1 / Ref 16 | `reports/public/report_public.md:240` | **Transposed conditional.** "Joint probability of accidentally drawing a map that hits the extreme statistical tail across four *independent* partisan metrics … is at most 1 in 357,000. You cannot blunder your way into the 99.99th percentile." Converts P(data \| neutral) into P(accident \| data). "Independent" is false (Mahalanobis covariance exists because they're correlated). I patched the Fisher→Bonferroni number today but missed this. | Delete "accidentally" / "independent" / "blunder your way"; state P(data \| neutral) explicitly. |
| A13 | Ref 2 | `mcmc_ensemble.py:553` | **Effective ε is ±12.5%, not the documented ±25%.** `epsilon=pop_deviation / 2.0` in ReCom proposal. Statutory s.15(2)-style branch at lines 558–573 is unreachable dead code; sampler never proposes such states. §5.4.1's acknowledged "±25% vs §15(2)" gap **understates the real gap by 2×**. | Set `epsilon=pop_deviation`; publish empirical max-deviation histogram of sampled plans. Material to the headline-percentile interpretation. |
| A14 | Ref 13 | `report_academic.md:376, 368`; `cycle_lag_analysis.md:88-93` | **14.69% provincial-growth figure mixes incompatible population universes** — 2021 census *count* (4,262,635) vs Q2-2024 *postcensal estimate* (4,888,723). Estimates rebase on counts adjusted for net undercoverage (Alberta has highest provincial net undercoverage). July 2021 *adjusted* estimate is 4,442,879 (+4.2% level shift). Like-for-like 2021→mid-2024 growth is ~10%, not 14.69%. 17.8% 2021→mid-2025 repeats the error. | Rebase all drift/growth figures on July 1, 2021 *adjusted* estimate. |
| A15 | Ref 13 | `findings/phase4f_hardstop_canonical.md` (today's work) | **My T4.6 canonical hardstop has zero diagnostic power.** All 178 deltas are negative; derived totals sum to 4,262,567 — test compares 2021-count universe to 2024-estimate universe → guaranteed −12.8% mean shift against 2% threshold. "Pure cycle-lag growth heterogeneity" overclaims. | Reframe as ED-share-of-provincial-total (removes level shifts); restores real transcription check. |
| A16 | Ref 6 | `extended_partisan_metrics_canonical.py:214-217` (today's work) | **My canonical PB percentile uses mismatched null.** Map PB swings via *unweighted mean* of district shares; ensemble column `seats_at_50_50 − 0.5` swings via *turnout-weighted provincial share*. Result: published majority PB −0.0281 at "p93.31" — like-for-like canonical value is 0.4607 (41/89 seats) at p77.8 (already in report at line 863). Plus 2019 (87 EDs) ranked against 89-seat null. | Recompute using provincial-vote-weighted swing; reconcile §5.2.9 with §5.2.1 B4. |
| A17 | Ref 11 | `report_academic.md:1187-1189` | **C3 arithmetic fails.** Airdrie 85,805 > 1.25×54,929 = 68,661, so "single-district feasible within ±25% band" is mathematically false; criterion was bent ("plus a rural-boundary adjustment"). | Fix arithmetic; cracking lacks wasted-vote component; either add per-community wasted-vote check or relabel as community-of-interest splitting. |
| A18 | Ref 14 | `report_academic.md:2344` | "Six independent dimensions" contradicted six lines later in same paragraph ("correlated dimensions, not independent"). | Replace with "six correlated measurement dimensions (five of six under §1.2 precision; declination dissents)." Note: declination dissent reverses if A1 lands. |

## Severity Tier B — Process / pre-registration discipline gaps

These compromise the audit's pre-registration discipline but don't directly invalidate any single finding.

| # | Source | Where | Finding |
|---|---|---|---|
| B1 | Ref 4 | `drand_seed.py:12,27`; `seed_commitments.md:100-108` | **drand round 5500000 is from October 2025**, months *before* salts were committed (April 2026). The randomness was already public when salts were chosen — "computationally infeasible to predict future beacon" defense is void. Three docs cite three different rounds (5500000, 6062459, 5,800,000). |
| B2 | Ref 18 | `preregistration/november_2026_scoring_spec.md:98` | Spec's drand-round commitment is still literally `[committed]` placeholder. `seed_commitments.md` has no `november_2026_scoring_spec` entry. §7 still claims scripts "do NOT exist" (both exist since 2026-06-10). |
| B3 | Ref 18 | `preregistration/november_2026_scoring_spec.md:20 vs :69` | Spec contradicts itself on partisan criterion — §1 says "at least *one* partisan-bias metric"; §3 says "≥ *two* of P1-P4 fire." Internal contradiction in pre-reg document. |
| B4 | Ref 4 | `preregistration/t3_2_majority_rural_isolation_design.md` (today's work) | **T3.2 "pre-registration" was 85 seconds before execution.** Commits 5fbd1ca (design) → 3bfeefa (result) = 17:12:56 → 17:14:21. The 347-line analysis script co-committed with design; could trivially encode known results. Declared `salt_string` never used (test is deterministic). Audit's own §5.3.1 standard would label this exploratory. |
| B5 | Ref 11 | `preregistration/t3_2_majority_rural_isolation_design.md` (today's work) | T3.2 design doc cites z=−2.915 as motivation, mislabeled "against the canonical 1.01M-plan ensemble" — it's actually the Phase B label-shuffle null. The z-value itself is substrate-stale (canonical z=−3.17). Rural/urban classifier is name-prefix-based: minority's "Airdrie East" (space) doesn't match "Airdrie-" prefix → classifies rural; majority's "Airdrie-Cochrane" matches → classifies urban. "Minority least isolated" is partly a producer-naming artifact. |
| B6 | Ref 18 | `findings/pre_registration_amendment_log.md` | Log self-describes as "complete dated chain" but jumps Amendment 4 → Amendment 8; Amendments 5-7 absent repo-wide. Spec header still v1.0 (2026-06-10) despite Amendment 9 rewriting §3 on 06-11. |
| B7 | Ref 4 | `report_academic.md:1143` vs `citation_verification.md:63,99` | AsPredicted records: same test cited as #289,455 (`null_hypothesis_and_exoneration_criteria.md:66`) AND #289452 (`phase_b_scorecard.py:90`). Public-vs-not-public contradicted across docs. |
| B8 | Ref 18 | `findings/pre_registration_amendment_log.md:336–349` | **Amendment 9 self-validation is circular.** Midpoint thresholds fitted to the only two existing maps, then "validated" on those same maps — training set = test set. Audit owns 1.01M ensemble; never computed Pr(≥3/5 flags \| neutral plan). False-positive rate undefined. |

## Severity Tier C — Substrate-staleness in framing / text

| # | Source | Where | Finding |
|---|---|---|---|
| C1 | Ref 17 | `report_academic.md:1768` (RT7) | Stress-test gate RT7 graded on Run #3 (250k v0_7 centroid); never regraded against canonical 1.01M. |
| C2 | Ref 17 | `report_academic.md:271, 638, 1764` (RT3) | RT3 cross-election stability graded on blend-era asymmetries (−0.51 / +0.75 pp); canonical recompute gives +3.92 pp (opposite sign, 4× magnitude). |
| C3 | Ref 10 | `report_academic.md:1850` (§5.8.4) | Edmonton-Enoch-Devon "L-shaped corridor" qualitative claim rests on v0_9 PP = 0.065 while canonical PP = 0.534. Retracted substrate supports a live claim. |
| C4 | Ref 11 | `report_academic.md:1743` (§5.6 T3.2 motivation) | Cites z = −2.915 as motivation for T3.2; that number is now bannered SUBSTRATE-STALE. (Today's work.) |
| C5 | Ref 9 | `report_academic.md:919, 1317, 1325, 1462` | "MGGG lawsuit-grade" ESS benchmark misattributed — only succeeded in state constitutional courts (LWV v PA); Canadian admissibility goes through R v Mohan / White Burgess (Daubert never applies). |

## Severity Tier D — Methodological / technical depth issues

These don't invalidate any finding directly but raise the bar a careful reviewer applies.

| # | Source | Where | Finding |
|---|---|---|---|
| D1 | Ref 1 | `report_academic.md:1598-1599, 1637` | Headline p = 1.40×10⁻⁶ is parametric χ²₄ tail, not ensemble-empirical. ESS-bounded empirical tail is ~6.7×10⁻⁴; propagates to Bonferroni headline. |
| D2 | Ref 1 | §4.3.2 / §5.4.9 Bonferroni m=2 | Post-hoc selection: Ch3 ("only pre-registered confirmatory") returned null and is excluded; honest bound ≥ 3×min-p. Line 547's "clears α/11=0.0045 by multiple orders of magnitude" is false (factor 1.9). |
| D3 | Ref 1 | `analysis/scripts/szat.py:409-420` | SZAT permutation violates exchangeability — Bernoulli flips on spatially autocorrelated VAs (Moran's I z=12.15 contra independence); needs block permutation (Legendre 1993). Plus missing (b+1)/(B+1) correction. |
| D4 | Ref 2 | `mcmc_ensemble_canonical.py:146-161` | Resume path silently corrupts chains — RNG reseeded with identical chain_seed on resume → replays from step 0. Latent (1.01M run uninterrupted) but breaks reproducibility. |
| D5 | Ref 2 | `mcmc_ensemble_canonical.py:289, 297-305, 316-327` | Canonical ESS computed across chain joins; no burn-in before headline percentiles. n_eff=1,495 underwriting §5.4.9 "ESS-adjusted p98" includes ε=0.25 initialization-bias samples. |
| D6 | Ref 3 | `mcmc_ensemble_canonical.py:243-256` vs `findings/maup_attribution_canonical.md:79` | **Differential measurement error.** Ensemble plans are unions of whole VAs (zero attribution error); real maps are scored via centroid sjoin which carries attribution error. §5.4.9 percentiles compare error-bearing real-map statistics against error-free null. Audit's own pop-weighted check shows centroid EG error ≈ 0.05-0.1 pp — same magnitude as the p94.4↔p95 gap. |
| D7 | Ref 3 | three "identical" attribution implementations | `phase4c_canonical_attribution.py:84-95` (nearest-fallback, no dedupe), `mcmc_ensemble.py:334-339`, `packing_cracking_analysis.py:297-298` (dropna + dedupe keep="first") handle boundary VAs differently despite docstrings claiming they "mirror exactly." `keep="first"` resolves multi-ED containment by join order — nondeterministic. |
| D8 | Ref 10 | `score_anchoring.py:143-179` | Anchoring metric implementation lacks the "contiguous ≥1 km" filter the report text and footnote require. Published 72.0/80.0/75.2% measure a more permissive quantity than defined. |
| D9 | Ref 10 | `score_anchoring.py:52-55` | SNAP_TOL_M = 500 m carried from DPG ±500 m positional error onto exact canonical geometry; no sensitivity analysis at 100 / 250 / 500 m. §5.8.5 "anchoring within Canadian norm" verdict may be tolerance-dependent. |
| D10 | Ref 15 | `drain_phase_b_canonical.py:209` (today) | Default seed `460508741` is hardcoded; salt_string declared `drain-label-shuffle-canonical-2026-06-11` would derive 2769319138; docstring claims `drain-label-shuffle` → 3594712923. Three inconsistent claims; seed matches none. Same orphan seed at `drain_metric_validation.py:301`. |
| D11 | Ref 15 | `drain_metric_validation.py:109` (today) | Mixed RNG families: stdlib `random.Random(20260611)` (date-picked seed) alongside `np.random.default_rng` at :308. Repeats deferred red-team finding HIGH-05. |
| D12 | Ref 15 | `requirements.txt:2-10` vs `red_team_consolidated.md:1599` | Pinned env: Python 3.11 / numpy 1.26.4. Verified env: Python 3.14.3 / numpy 2.4.2. numpy 1.26.4 has no Python 3.14 wheels — `pip install -r requirements.txt` fails on the documented interpreter. CI uses Python 3.12, unpinned. |
| D13 | Ref 15 | `.gitattributes:17` | 170 MB canonical ensemble is plain git, not LFS — pattern `data/mcmc_checkpoints_*/chain*` doesn't match `data/simulation_checkpoints_canonical/`. `git check-attr` confirms `filter: unspecified`. |
| D14 | Ref 6 | `report_academic.md:822` vs `findings/advance_vote_sensitivity.md:56` | False EG turnout-invariance claim contradicted by audit's own finding (majority EG flips sign +0.0144 → −0.0149 when advance votes restored). §5.2.1 table mixes substrates (2019 = full CSV; 2026 = election-day-only). |
| D15 | Ref 6 | `report_academic.md:1061-1063` | EG threshold verdict 4.10% rests on 0.14 pp margin (Phase 4C +3.96% vs threshold), like-for-like 0.08 pp; order-statistic SE at ESS exceeds 0.08 pp. Sub/over-threshold call indeterminate. |
| D16 | Ref 6 | `report_academic.md:528-529, 1099` | Lopsided Margins misused directionally: positive t = UCP (seat-majority party) packed = NDP-favourable signal, counted as PASS alongside UCP-favourable findings. Welch-t scales with win-set sizes (29/34/38), not packing severity. |
| D17 | Ref 17 | `findings/regional_swing_canonical_robustness.md:78` | Arithmetic contradiction: claims 0.0009 gap is "wider than" the same doc's 0.01-0.02 estimated tail extension. Off by an order of magnitude. |
| D18 | Ref 10 | `canonical_shapefile_log.md:24-26` | EPSG:3400 mislabeled "Alberta 3TM"; actually 10-TM Resource. Pipeline mixes 3400 (k₀=0.9992) and 3401 (k₀=0.9999) without explicit conversion at all sjoin sites. |
| D19 | Ref 10 | `compactness_metrics.py:181-194` | Reock computed against Shapely polygonal MBC approximation in a *conformal* projection (point scale varies 0.9992 → 1.0007 across Alberta); biases large-area northern EDs vs Calgary. |
| D20 | Ref 12 | `report_academic.md:1931` | Pre-Vavilov standard-of-review vocabulary ("manifest unreasonableness") — defunct under Vavilov 2019 SCC 65. |
| D21 | Ref 12 | `report_academic.md:2100` | Commission mischaracterized as "quasi-judicial"; it's polycentric/advisory. Inflates the fairness baseline. All 7 sentiment configurations are chair-flagged; no symmetric majority-side scan. |
| D22 | Ref 9 | `report_academic.md:1053` | §5.2.8 false provenance: 7% EG threshold claimed "calibrated to US Congressional delegation sizes 1972-2010"; actually entered via Whitford expert testimony on state legislative plans. |
| D23 | Ref 9 | `report_academic.md:1721, 955` | §5.6 Chen-Rodden 2013 miscited — their QJPS paper is about geography-driven bias, not test-selection symmetry. "Chen-Rodden identity" attribution unsupported. |
| D24 | Ref 9 | `report_academic.md:304` | Rucho misread as "metrics need corroboration"; Rucho is institutional non-justiciability. NC plaintiffs presented the full structural+procedural package and still lost. |
| D25 | Ref 16 | `report_academic.md:1578, 1586, 1592-1594` | "Neutral commission drawing" null isn't actually tested — both real maps p100 on Reock+CSD anchoring; majority MM p0.85 excused as "commission convention" while minority outliers aren't discounted. Severity failure (Mayo 2018). |
| D26 | Ref 16 | `report_academic.md:508-516` vs §6.2.1 | "Bayesian-screening" label deployed to decline multiplicity correction; no prior/likelihood/posterior anywhere; full Bayesian explicitly ruled out at line 611; then exploratory p ≤ 2.80×10⁻⁶ re-deployed as verdict-bearing. |
| D27 | Ref 17 | `findings/sensitivity_analysis.md:28-41` | Population-deviation OAT sweep is scriptless, header-flagged SUPERSEDED; canonical 1.01M ran at ±25% only; no factorial sensitivity. |
| D28 | Ref 2 | §5.2.10 + ES-13 | "Symmetric exclusion" defense for 47.2% advance-ballot drop is invalid for tail claims — changes vote geography, not invariant. Audit's own full-vote SZAT sensitivity shows material shifts with a Calgary sign reversal. |
| D29 | Ref 5 | `report_academic.md:1569` | δ scored on 87-district 2019 map against 89-district ensemble; Warrington's δ̃ exists for cross-size comparison. Numerically negligible but unacknowledged. |
| D30 | Ref 12 | `report_academic.md:2146-2148` | Three "doctrinal holdings" extracted from CBC/CP reporting of an unreasoned bench dismissal pending SCC reasons; equates Quebec *legislative* freeze with Alberta *commissioner* design rationale. |

## Severity Tier E — Lower-priority cleanups

(About 25 additional findings — referee #7 W4 (Banff-Park s.15(2)(b) "functional centre of gravity" gloss), referee #11 W5 (Lethbridge/Red Deer reverse-engineered thresholds), referee #13 W4/W5 (Plan B non-reproducible; LSL contradicts §3.3), referee #14 W1/W5 (intent-asserting language in public report), referee #16 W5 ("constraint-bound expectation" smuggles a loss function), referee #18 W5 (72-hour window underspecified), etc.) Not enumerated here; remediate after Tier A-D close.

## Recommended remediation sequence

### Phase 1 — Tier A factual corrections (this session if possible)
- A1 declination sign-flip (verify, fix `mcmc_ensemble.py:215`, recompute, update §5.2.4 / §6.2.1 / RT2 / public report; **strengthens** headline)
- A2 Cassista verification (verify in CanLII; if fabricated, excise and substitute)
- A3 Raîche restatement
- A4 s.15(2) statutory misquote
- A5 FINDINGS_BRIEF chair-anomaly inversion
- A8 2010 vs 2017 commission mis-attribution
- A11 BH table re-sort + recompute + drop "independent"
- A12 transposed-conditional language in public report
- A13 ReCom ε=0.125 vs documented 0.25 (verify, fix, rerun)
- A15/A16 today's-work canonical recompute reframing
- A18 "six independent dimensions" rewording

### Phase 2 — Tier B pre-registration discipline (after Tier A)
- B1 drand-round timing acknowledgment / formal pre-reg of November salt with future round
- B2 fill in `[committed]` placeholders
- B3 spec internal contradiction (one vs two partisan flags)
- B4 mark T3.2 as exploratory/same-session
- B5 fix T3.2 design-doc mislabeling + classifier
- B6 fill Amendments 5-7 gap
- B8 specificity-rate calculation for Amendment 9

### Phase 3 — Tier C substrate-text-staleness (mechanical)
- C1 regrade RT7 against canonical 1.01M
- C2 regrade RT3 against canonical +3.92 pp
- C3 rewrite §5.8.4 Edmonton-Enoch-Devon on canonical PP
- C4 refresh §5.6 T3.2 motivation paragraph
- C5 MGGG Daubert citation correction

### Phase 4 — Tier D methodological deepening (queue for sustained work)
- D1-D5 statistical / MCMC depth fixes
- D6-D7 attribution unification
- D8-D9 anchoring metric reconciliation
- D10-D13 reproducibility cleanups (drand seeds, env pinning, LFS, single-command battery)
- D14-D30 various

## Agent specialty assignments (for trail-of-work)

| # | Specialty | Internal id |
|---|---|---|
| 1 | Statistical methodology + multiple-comparisons | a10968f13ab93833f |
| 2 | MCMC ensemble + ReCom | adc41d727df9849e5 |
| 3 | Vote attribution + MAUP | ab315a3100c1a4707 |
| 4 | Pre-registration + drand seeds | a29cb3fd392f15e7b |
| 5 | Declination + Warrington 2018 | ad7480de7ffa1f46d |
| 6 | Efficiency gap + Stephanopoulos-McGhee | a0ed657f03fdbd84c |
| 7 | Alberta statutory + EBCA | a121ede8b01d78af9 |
| 8 | Charter + Carter | a8ad637112f4198b5 |
| 9 | Comparative US gerrymander | aa823c77673752a9b |
| 10 | Geographic + GIS | a8cc7656d09583c3f |
| 11 | Engineering signatures + RMH-Banff | af2cc89f6c9ee55f3 |
| 12 | Process + procedural anomaly | aefb2e1520aa68711 |
| 13 | Population data + 2021/2026 | a5b03fe076f603086 |
| 14 | Language + framing | a8903aa70e108336f |
| 15 | Codebase + reproducibility | a546e13bbfbc81211 |
| 16 | Bayesian + decision theory | a16cf83ecd952021c |
| 17 | Robustness + sensitivity | ae2bddc954c470f33 |
| 18 | Replication + November 2026 | a750cb5f6f5639b57 |
