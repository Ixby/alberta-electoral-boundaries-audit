# Joint Outlier Score — Alberta 2026 EBC Maps

**Date:** 2026-07-12 (regenerated; first canonical run 2026-05-07)
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

**Directional note.** The neutral ensemble centre is moderately UCP-favourable (mean EG = +0.0160), reflecting Alberta's natural geographic sorting of voters (rural UCP dispersion; Chen & Rodden 2013). The minority map's extreme MM and s50 scores are driven by structural map choices, not natural geography.

| Map | Mahalanobis distance | p (chi-sq, df=4) | p (n_eff-adjusted, F(4,1409)) |
| --- | --- | --- | --- |
| Minority 2026 | 5.7999 | 8.80e-07 | 1.11e-06 |
| Majority 2026 | 2.7814 | 1.02e-01 | 1.03e-01 |
| 2019 Enacted  | 3.6283 | 1.05e-02 | 1.10e-02 |

*n_eff-adjusted p uses Hotelling T² correction (F-distribution) with n_eff = 1413 — the conservative lower bound from convergence diagnostics. Both columns reject the null for the minority map.*

**Minority marginals:**

| Metric | Observed | Ensemble mean | Marginal tail p |
| --- | --- | --- | --- |
| efficiency_gap | +0.0402 | +0.0160 | 0.0546 |
| mean_median | +0.0104 | -0.0187 | 0.0003 |
| declination | +0.0770 | +0.0014 | 0.0121 |
| seats_at_50_50 | +0.5169 | +0.4529 | 0.0001 |

---

## Channel 2 — SZAT bootstrap null

SZAT score: +0.039211 (minority EG − majority EG, swing zones only)
Bootstrap p: 0.0025 ((b+1)/(B+1); 24/10000 permutations exceeded observed, full-recompute)
(AsPredicted #289,469; seed pre-committed at git hash d2aea42; full-recompute procedure)

**Status (2026-06-13): retired as a confirmatory channel.** Under a contiguity-respecting
block-permutation null the SZAT p-value is 0.1947 (variance inflation 5.79× vs the i.i.d.
flip; `findings/szat_block_permutation.md`). The bootstrap p above is the i.i.d.-flip value,
retained as exploratory context only. The joint headline rests on Channel 1 alone.

---

## Channel 3 — Neighbour-Drain label-shuffle null (canonical substrate)

Pre-registered: OSF r3zm7 / AsPredicted #289,451. Canonical-substrate Phase B re-run 2026-06-11
(`findings/drain_label_shuffle_null_canonical.json`, 10,000 permutations, seed 460508741).

| Map | drain_score | Null mean | z-score | p (two-tailed) |
| --- | --- | --- | --- | --- |
| Majority 2026 | 0.007213 | 0.049257 | **-3.173** | **0.0002** |
| Minority 2026 | 0.000591 | 0.028057 | -2.750 | 0.0002 |
| 2019 Enacted | 0.001530 | 0.052987 | -3.520 | 0.0000 |

**Prediction A** (drain_score(majority) > drain_score(minority)): **CONFIRMED** on the canonical substrate (0.007213 vs 0.000591).

**Interpretation.** All three maps — including the pre-commission 2019 enacted baseline — are
anomalously *low* against their own label-shuffle nulls; the 2019 enacted map is the most
anomalous (z = -3.52). No map is singularly anomalous on this metric.
(The superseded DPG/blended-substrate run reported minority p = 0.1342 within null and majority
z = −2.915; those values did not survive the canonical re-run and are retained only as
stale_* provenance fields in the JSON.)

**Channel 3 is reported per pre-registration and is not part of the joint headline.**

---

## Joint statistic — Bonferroni upper bound (Fisher retired)

**Operative headline: p ≤ 1.76e-06 (= 2 × Ch1), valid under arbitrary dependence
between the two examined channels.** The Fisher combination below assumed Ch1/Ch2
independence and was retired 2026-06-10 (the channels share the 2023 vote substrate;
Fisher is anti-conservative under positive dependence — Brown 1975). It is preserved
as historical record only.

| Channel | p (unadjusted) | p (n_eff-adjusted) |
| --- | --- | --- |
| Partisan joint (Mahalanobis) | 8.80e-07 | 1.11e-06 |
| SZAT bootstrap (retired, i.i.d.-flip) | 0.0025 | 0.0025 |
| **Fisher combined (historical)** | **4.61e-08** | **5.74e-08** |

Unadjusted: Fisher T = 39.870, chi-sq df = 4.
n_eff-adjusted: Fisher T = 39.405, using Hotelling T² p for Ch1 (n_eff = 1413, conservative lower bound).

**Reading:** the operative claim is the dependence-robust bound p ≤ 1.76e-06
(≈ 1 in 568,182) — under the neutral null, a map with
Channel 1's joint partisan profile arises at most about once in every
568,182 draws, allowing for the two channels examined.
The historical Fisher figure (4.61e-08) overstated joint significance by
assuming channel independence.

---

## Supplementary structural channels (all resolved — none pending)

| Channel | Status | Finding |
| --- | --- | --- |
| Municipal anchoring departure | RETRACTED on canonical geometry (§5.8.5) — DPG-era 4.9× ratio did not survive; canonical: maj 80.0% / min 71.8%, both within 70–85% Canadian norm | No longer a channel |
| Population MAD ratio | Captured in canonical ensemble outputs (per-plan `population_mad`) | Minority 1.39× majority (3,938 vs 2,827); minority at p99.1 of the neutral ensemble |
| Reock asymmetry | Captured in canonical ensemble outputs (per-plan proxy Reock) | Null finding: both real maps sit at ~p100 on median compactness (anomalously compact — expected for commission maps); minority/majority pct<0.30 ratio 0.5× (the DPG-era 2.58× value was retracted — see DOCUMENTED CORRECTIONS) |

*(Corrected 2026-07-08: this table previously described MAD and Reock as "pending — not in
ensemble outputs" and carried the retracted 2.58× Reock ratio and a stale 1.48× MAD ratio.
The canonical ensemble outputs contain per-plan values for both metrics.)*

---

## Interpretation note

The duck test made precise: the minority map's four-dimensional partisan feature
vector sits at Mahalanobis distance 5.80 from the ensemble center
(p = 8.80e-07). The operative joint statistic is the dependence-robust Bonferroni
upper bound p ≤ 1.76e-06. SZAT (Ch2) is exploratory context only
(block-permutation p = 0.1947); the retired Fisher combination is preserved above as
historical record.

**Channel 3 (Neighbour-Drain, canonical substrate 2026-06-11).** All three maps are
anomalously low against their label-shuffle nulls (2019 enacted most anomalous,
z = -3.52); Prediction A is directionally confirmed.
The channel is reported per pre-registration and is not part of the joint headline.

The majority map sits at Mahalanobis distance 2.78 from the ensemble
center (p = 1.02e-01) — outlier on MM in the NDP-favourable direction.

---

*Script: `analysis/scripts/joint_outlier_score_canonical.py`*
*Full output: `findings/joint_outlier_score.json`*
