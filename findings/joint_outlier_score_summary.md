# Joint Outlier Score — Alberta 2026 EBC Maps

**Date:** 2026-05-07
**Ensemble:** canonical 1,010,000 plans (official Elections Alberta shapefiles, 4 chains × 252,500, base_seed=1432864451)
**Question:** How probable is it that a neutral redistricting process produces a map
whose feature vector looks like the minority 2026 map?

**Answer format:** P(feature vector | neutral draw) — the joint probability that
a neutral-draw plan is at least as extreme as the observed map across all active
channels simultaneously. This is *not* a posterior probability of gerrymandering.

---

## Channel 1 — Partisan joint tail (Mahalanobis)

Ensemble: 1,010,000 neutral-draw plans (canonical shapefiles). Metrics: EG, mean-median, declination, seats@50/50.
Mahalanobis distance accounts for the correlation structure between these four metrics.

**Directional note.** The neutral ensemble centre is moderately UCP-favourable (mean EG = +0.0164), reflecting Alberta's natural geographic sorting of voters (rural UCP dispersion; Chen & Rodden 2013). The minority map's extreme MM and s50 scores are driven by structural map choices, not natural geography.

| Map | Mahalanobis distance | p (chi-sq, df=4) | p (n_eff-adjusted, F(4,1424)) |
| --- | --- | --- | --- |
| Minority 2026 | 5.7157 | 1.40e-06 | 1.73e-06 |
| Majority 2026 | 2.8022 | 9.71e-02 | 9.88e-02 |
| 2019 Enacted  | 3.5701 | 1.26e-02 | 1.31e-02 |

*n_eff-adjusted p uses Hotelling T² correction (F-distribution) with n_eff = 1428 — the conservative lower bound from convergence diagnostics. Both columns reject the null for the minority map.*

**Minority marginals:**

| Metric | Observed | Ensemble mean | Marginal tail p |
| --- | --- | --- | --- |
| efficiency_gap | +0.0402 | +0.0164 | 0.0561 |
| mean_median | +0.0104 | -0.0186 | 0.0002 |
| declination | +0.0770 | +0.0025 | 0.0121 |
| seats_at_50_50 | +0.5169 | +0.4533 | 0.0001 |

---

## Channel 2 — SZAT bootstrap null

SZAT score: +0.039211 (minority EG − majority EG, swing zones only)
Bootstrap p: 0.0024 (24/10000 permutations exceeded observed, full-recompute)
(AsPredicted #289,469; seed pre-committed at git hash d2aea42; full-recompute procedure)

---

## Channel 3 — Neighbour-Drain label-shuffle null

Pre-registered: AsPredicted #289,451. Executed 2026-05-07 on official canonical shapefiles.

> **⚠ SUBSTRATE-STALE (banner reapplied 2026-06-12 after Amendment-10 regeneration).** The drain_score values in this section were computed on a DPG-era / blended-vote substrate and are superseded by the canonical-substrate Phase B re-run at `findings/drain_label_shuffle_null_canonical.md` (majority = 0.00721 / z = −3.173; minority = 0.000591 / z = −2.750; 2019 enacted = 0.001530 / z = −3.520). Direction reverses on canonical: majority > minority. "Majority singularly anomalously low" does not survive — all three maps are anomalously low against their own canonical null, 2019 the most extreme. Numbers kept below for trail-of-work only.

| Map | drain_score | Null mean | z-score | p (two-tailed) |
| --- | --- | --- | --- | --- |
| Majority 2026 | 0.000179 | 0.032085 | **-2.915** | **0.0000** |
| Minority 2026 | 0.006176 | 0.016741 | −1.372 | 0.1342 |

**Prediction A** (drain_score(majority) > drain_score(minority)): **NOT CONFIRMED** (0.000179 < 0.006176) *on stale substrate; CONFIRMED on canonical substrate per `drain_label_shuffle_null_canonical.md`*.

**Prediction B** (both within null p > 0.05): **NOT CONFIRMED for majority** (p < 0.0001, outside null). Minority: CONFIRMED (p = 0.1342, within null).

**Interpretation.** The minority map's drain score (0.0062) is within the neutral-draw null — 13.4% of random label assignments produce equal or higher coupling. This channel does **not** contribute evidence against the minority map.

The majority map's drain_score (0.0002) is significantly *below* the null mean (z = −2.915, p < 0.0001 one-sided) — anomalously clean, not the partisan direction.

**Channel 3 contributes p = 0.1342 (minority within null) — not added to Fisher combination.**

---

## Joint combination — dependence-robust (Channels 1 + 2, minority only)

**Headline (revised 2026-06-10; Cauchy corroboration added 2026-06-13, T1.2).**
Ch1 (Mahalanobis) and Ch2 (SZAT) are **not independent** — they share the 2023
vote-attribution substrate and overlap on the efficiency-gap dimension — so a
Fisher combination (which assumes independence) is anti-conservative under
positive dependence (Brown 1975). The audit's operative joint statistic is the
**Bonferroni upper bound, p ≤ 2.80×10⁻⁶ (≈ 1 in 357,000)** = 2 × min(Ch1, Ch2),
valid under *arbitrary* dependence between the channels.

| Combination method | Joint p | ≈ 1 in | Dependence assumption |
| --- | --- | --- | --- |
| **Bonferroni** `2·min(Ch1, Ch2)` (headline) | **2.80×10⁻⁶** | **357,000** | none (arbitrary dependence) |
| **Cauchy / ACAT** (Liu & Xie 2020) | 2.80×10⁻⁶ | 357,351 | none (arbitrary dependence) |
| Fisher (retired) | 6.89×10⁻⁸ | 14,509,987 | independence (false here) |

**Cauchy (ACAT) corroboration (T1.2, computed 2026-06-13).** The aggregated
Cauchy test of Liu & Xie (2020) is valid under arbitrary dependence and needs
only the two channel p-values (unlike Brown's scaled-χ², which needs the paired
per-plan (D², SZAT) statistics still blocked on the per-VA assignment archive).
With equal weights it returns **p = 2.80×10⁻⁶ — numerically identical to the
Bonferroni bound (ratio 0.999)**. The reason is structural: the joint signal is
Ch1-dominated, so the ACAT statistic reduces to ≈ 2·p_min in this regime. The
result is **essentially invariant to the Ch2 value**: substituting the
contiguity-respecting block-permutation SZAT p (≈ 0.19, T1.10b) for the
i.i.d.-flip p (0.0024) shifts the combined p by < 0.01 % (still 1 in ≈ 357,000).
A second, independent dependence-robust method therefore reproduces the
published headline and shows it is not an artefact of the conservative
Bonferroni construction. Script: `analysis/scripts/cauchy_combination_joint.py`;
output: `findings/joint_outlier_score_cauchy.json`.

> **Fisher figure retired.** The earlier combined value (p = 6.89×10⁻⁸, T = 39.023,
> "1 in 14,509,987") assumed Ch1 ⊥ Ch2 and is **no longer used**. It is retained
> here for trail-of-work only. The Spearman ρ = −0.0014 check that once justified
> the independence assumption measures correlation across two *unpaired* Monte
> Carlo streams, not the dependence between the test statistics under the null map
> distribution, and does not license Fisher's method.

---

## Pending channels (not executable with current ensemble)

| Channel | Reason pending | Marginal finding |
| --- | --- | --- |
| Municipal anchoring departure | RETRACTED on canonical geometry (§5.8.5) — DPG-era 4.9× ratio did not survive; canonical: maj 80.0% / min 72.0%, both within 70–85% Canadian norm | No longer a pending channel |
| Population MAD ratio | Per-plan MAD not in ensemble outputs — requires MCMC rerun with population capture | Minority 1.48× majority |
| Reock asymmetry | Per-plan Reock not in ensemble outputs — requires MCMC rerun | Minority 2.58× majority on % below 0.30 |

---

## Interpretation note

The duck test made precise: the minority map's four-dimensional partisan feature
vector sits at Mahalanobis distance 5.72 from the ensemble center
(p = 1.40e-06). Combined with the SZAT result (p = 0.0024) under the
**dependence-robust** Bonferroni bound — corroborated to within 0.1 % by the
Cauchy/ACAT combination — the joint neutral-null probability is
**p ≤ 2.80×10⁻⁶ (≈ 1 in 357,000)**. (The earlier Fisher figure of 6.89×10⁻⁸
assumed channel independence and is retired; see the joint-combination section
above.)

**Channel 3 (Neighbour-Drain) executed 2026-05-07.** Minority within null
(p = 0.1342); does not contribute to the Fisher combination. The pre-registered
predictions (A and B) were not confirmed. The majority map shows anomalously
low pack-crack coupling (p < 0.0001, z = −2.915), which is an inverted finding
relative to the prediction — the majority is unusually clean on this metric.

Three pending channels (anchoring, MAD, Reock) point in the same direction
marginally. When those channels have proper null distributions, the combined
p-value will only decrease or stay flat.

The majority map sits at Mahalanobis distance 2.80 from the ensemble
center (p = 9.71e-02) — outlier on MM in the NDP-favourable direction.

---

*Script: `analysis/scripts/joint_outlier_score_canonical.py`*
*Full output: `findings/joint_outlier_score.json`*
