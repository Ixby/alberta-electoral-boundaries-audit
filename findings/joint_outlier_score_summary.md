> **Backward:**
> - `analysis/scripts/joint_outlier_score_canonical.py` — companion script (Mahalanobis + Fisher combination)
> - canonical 1,010,000-plan ensemble (4 chains × 252,500 steps; OSF s58a6/w2s8k)
> - `findings/extended_partisan_metrics.md` — per-metric inputs to the Mahalanobis channel
> - `findings/drain_label_shuffle_null.md` — neighbour-drain channel inputs
> - SZAT bootstrap null outputs (AsPredicted #289,469)
>
> **Forward:**
> - `reports/academic/report_academic.md` — incorporates the joint outlier score
> - `reports/public/report_public.md` — references the joint probability headline
> - `analysis/methodology/fisher_combination_defense.md` — defends the Fisher combination procedure
> - `findings/README.md` — indexes this finding

# Joint Outlier Score — Alberta 2026 EBC Maps

**Date:** 2026-05-07 (updated 2026-05-12 to canonical 1M ensemble)
**Ensemble:** canonical 1,010,000 plans (official Elections Alberta shapefiles, 4 chains × 252,500 steps, base seed Cloudflare drand beacon, pre-registered OSF s58a6/w2s8k)
**Note:** Values below supersede the prior 100k-run results (2 chains × 50k); prior results: D=6.1059, p=1.60×10⁻⁷, Fisher p=8.71×10⁻⁹. The 1M canonical ensemble is authoritative.
**Question:** How probable is it that a neutral redistricting process produces a map
whose feature vector looks like the minority 2026 map?

**Answer format:** P(feature vector | neutral draw) — the joint probability that
a neutral-draw plan is at least as extreme as the observed map across all active
channels simultaneously. This is *not* a posterior probability of gerrymandering.

---

## Channel 1 — Partisan joint tail (Mahalanobis)

Ensemble: 1,010,000 neutral-draw plans (canonical shapefiles). Metrics: EG, mean-median, declination, seats@50/50.
Mahalanobis distance accounts for the correlation structure between these four metrics.

**Directional note.** The neutral ensemble centre is moderately UCP-favourable (mean EG = +0.0160), reflecting Alberta's natural geographic sorting of voters (rural UCP dispersion; Chen & Rodden 2013). The minority map's extreme MM and s50 scores are driven by structural map choices, not natural geography.

| Map | Mahalanobis distance | Joint p-value (chi-sq, df=4) |
| --- | --- | --- |
| Minority 2026 | 5.72 | 1.40×10⁻⁶ |
| Majority 2026 | 2.69 | 9.7×10⁻² |
| 2019 Enacted  | 3.56 | 1.3×10⁻² |

**Minority marginals (canonical 1M ensemble; marginal tail p derived from ensemble percentiles):**

| Metric | Observed | Ensemble percentile | Marginal tail p (approx) |
| --- | --- | --- | --- |
| efficiency_gap | +0.0402 | p94.4 (below 95th threshold) | ~0.056 — not individually flagged |
| mean_median | +0.0104 | p99.98 | ~0.0002 |
| declination | -0.0770 | p1.21 (NDP tail) | ~0.0121 |
| seats_at_50_50 | +0.5169 | p99.99 | ~0.0001 |

---

## Channel 2 — SZAT bootstrap null

SZAT score: +0.039211 (minority EG − majority EG, swing zones only)
Bootstrap p: 0.0024 (24/10000 permutations exceeded observed, full-recompute)
(AsPredicted #289,469; seed pre-committed at git hash d2aea42; full-recompute procedure)

---

## Channel 3 — Neighbour-Drain label-shuffle null

Pre-registered: AsPredicted #289,451. Executed 2026-05-07 on official canonical shapefiles.

> **⚠ SUBSTRATE-STALE (banner added 2026-06-11).** The drain_score values in this
> section were computed on a DPG-era / blended-vote substrate (the §5.3 blending
> pipeline that predates Phase 4C). The justify-or-drop validation
> (`findings/drain_metric_validation.md`, 2026-06-11) re-computed the continuous
> drain_score on canonical EA shapefiles + canonical VA centroid-in-polygon
> attribution and got `majority = 0.00721`, `minority = 0.00059` — the direction
> REVERSES (majority > minority, matching the §5.3.5 coupled-count table in
> `findings/neighbour_drain_analysis.md`). The "majority z = −2.915 anomalously
> low" reading below is therefore substrate-bound and has been retracted in
> `reports/academic/report_academic.md` §5.3.5 pending a canonical-substrate
> Phase B null re-run. Numbers kept below for trail-of-work only.

| Map | drain_score | Null mean | z-score | p (two-tailed) |
| --- | --- | --- | --- | --- |
| Majority 2026 | 0.000179 | 0.032085 | **−2.915** | **0.0000** |
| Minority 2026 | 0.006176 | 0.016741 | −1.372 | 0.1342 |

**Prediction A** (drain_score(majority) > drain_score(minority)): **NOT CONFIRMED** (0.000179 < 0.006176) *on stale substrate; CONFIRMED on canonical substrate, see drain_metric_validation.md*.

**Prediction B** (both within null p > 0.05): **NOT CONFIRMED for majority** (p < 0.0001, outside null). Minority: CONFIRMED (p = 0.1342, within null).

**Interpretation.** The minority map's drain score (0.0062) is within the neutral-draw null — 13.4% of random label assignments produce equal or higher coupling. This channel does **not** contribute evidence against the minority map.

The majority map's drain_score (0.0002) is significantly *below* the null mean (z = −2.915, p < 0.0001 one-sided) — anomalously clean, not the partisan direction.

**Channel 3 contributes p = 0.1342 (minority within null) — not added to Fisher combination.**

---

## Joint statistic (Channels 1 + 2, minority only) — revised 2026-06-10

| Channel | p-value |
| --- | --- |
| Partisan joint (Mahalanobis) | 1.40×10⁻⁶ |
| SZAT bootstrap | 0.0024 |
| **Dependence-robust upper bound (Bonferroni, 2 × min p)** | **≤ 2.80×10⁻⁶** |
| Earlier Fisher combination (now retired as headline; superseded) | 6.87×10⁻⁸ |

Fisher T = 39.02, chi-sq df = 4. **The Fisher figure assumes Ch1 ⊥ Ch2 and is anti-conservative under positive dependence (Brown 1975).** Ch1's Mahalanobis vector includes the efficiency gap; Ch2 (SZAT) *is* an efficiency-gap decomposition on the same vote substrate. The two channels are not independent — they share underlying 2023 vote-attribution data and overlap in the EG dimension specifically — so the audit's reported joint headline is now the Bonferroni upper bound (p ≤ 2.80×10⁻⁶, ≈ 1 in 357,000), which is valid under arbitrary dependence between the channels. A dependence-aware combination (Brown's scaled χ² or the Cauchy combination per Liu & Xie 2020) is listed as future work in the monograph §10.2.

**Reading:** p ≤ 2.80×10⁻⁶ is the dependence-robust upper bound on the probability that a neutral-draw process produces a map simultaneously this extreme on both the partisan feature vector (Mahalanobis distance) and the swing-zone boundary allocation. Under the neutral ReCom reference distribution (which does not enforce every statutory criterion the commission worked under), this joint event occurs at most about once in every 357,000 draws.

---

## Pending channels (not executable with current ensemble)

| Channel | Reason pending | Marginal finding |
| --- | --- | --- |
| Municipal anchoring departure | Both maps within Canadian norm (majority 80%, minority 72%) on canonical shapefiles — anchoring channel not executable as outlier test | Retracted — not available as a channel |
| Population MAD ratio | Per-plan MAD not in ensemble outputs — requires MCMC rerun with population capture | Minority 1.48× majority |
| Reock asymmetry | Per-plan Reock not in ensemble outputs — requires MCMC rerun | **Retracted (v0_9 substrate).** Canonical EA shapefiles reverse the direction: majority 6.7% (6/89) below 0.30 vs minority 4.5% (4/89). v0_9 had shown minority 2.58× majority (34.8% vs 13.5%). See `findings/reock_verdict.md`. |

---

## Interpretation note

The duck test made precise: the minority map's four-dimensional partisan feature
vector sits at Mahalanobis distance 5.72 from the canonical 1M ensemble centre
(p = 1.40×10⁻⁶). Combined with the SZAT result (p = 0.0024) under the
dependence-robust Bonferroni bound, the joint neutral-null upper bound is
p ≤ 2.80×10⁻⁶ (≈ 1 in 357,000).

Three metrics individually flag above the 95th percentile (MM p99.98, Decl p1.21 NDP-tail, seats@50/50 p99.99). EG at p94.4 does not individually flag but contributes to the joint Mahalanobis distance.

**Channel 3 (Neighbour-Drain) executed 2026-05-07.** Continuous drain-score: minority within null (p = 0.1342); does not contribute to the Fisher combination. Canonical chain-signal count (1M run): minority 2 signals, majority 6 signals, 2019 enacted 5 signals — pre-registered pass criterion (ratio ≤ 1.5×) met at 0.33× (PASS). §5.3.5 establishes that the minority achieves its partisan effect via hybridization rather than the adjacency-drain model this test measures.

Two pending channels (MAD, Reock) point in the same direction marginally; anchoring channel is not executable as an outlier test (both maps within Canadian norm on canonical shapefiles).

The majority map sits at Mahalanobis distance 2.69 from the ensemble centre (p ≈ 0.097) — within the neutral null on all four metrics.

---

*Script: `analysis/scripts/joint_outlier_score_canonical.py`*
*Full output: `findings/joint_outlier_score.json`*
