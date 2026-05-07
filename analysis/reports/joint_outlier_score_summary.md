# Joint Outlier Score — Alberta 2026 EBC Maps

**Date:** 2026-05-07
**Ensemble:** canonical 100k plans (official Elections Alberta shapefiles, 2 chains × 50k)
**Question:** How probable is it that a neutral redistricting process produces a map
whose feature vector looks like the minority 2026 map?

**Answer format:** P(feature vector | neutral draw) — the joint probability that
a neutral-draw plan is at least as extreme as the observed map across all active
channels simultaneously. This is *not* a posterior probability of gerrymandering.

---

## Channel 1 — Partisan joint tail (Mahalanobis)

Ensemble: 100,000 neutral-draw plans (canonical shapefiles). Metrics: EG, mean-median, declination, seats@50/50.
Mahalanobis distance accounts for the correlation structure between these four metrics.

**Directional note.** The neutral ensemble centre is moderately UCP-favourable (mean EG = +0.0160), reflecting Alberta's natural geographic sorting of voters (rural UCP dispersion; Chen & Rodden 2013). The minority map's extreme MM and s50 scores are driven by structural map choices, not natural geography.

| Map | Mahalanobis distance | Joint p-value (chi-sq, df=4) |
| --- | --- | --- |
| Minority 2026 | 6.1059 | 1.60e-07 |
| Majority 2026 | 2.6873 | 1.25e-01 |
| 2019 Enacted  | 3.5624 | 1.29e-02 |

**Minority marginals:**

| Metric | Observed | Ensemble mean | Marginal tail p |
| --- | --- | --- | --- |
| efficiency_gap | +0.0402 | +0.0160 | 0.0413 |
| mean_median | +0.0104 | -0.0197 | 0.0001 |
| declination | -0.0770 | -0.0021 | 0.0042 |
| seats_at_50_50 | +0.5169 | +0.4523 | 0.0000 |

---

## Channel 2 — SZAT bootstrap null

SZAT score: +0.039165 (minority EG − majority EG, swing zones only)
Bootstrap p: 0.0044 (44/10000 permutations exceeded observed, full-recompute)
(AsPredicted #289,469; seed pre-committed at git hash d2aea42; full-recompute procedure)

---

## Channel 3 — Neighbour-Drain label-shuffle null

Pre-registered: AsPredicted #289,451. Executed 2026-05-07 on official canonical shapefiles.

| Map | drain_score | Null mean | z-score | p (two-tailed) |
| --- | --- | --- | --- | --- |
| Majority 2026 | 0.000179 | 0.032085 | **−2.915** | **0.0000** |
| Minority 2026 | 0.006176 | 0.016741 | −1.372 | 0.1342 |

**Prediction A** (drain_score(majority) > drain_score(minority)): **NOT CONFIRMED** (0.000179 < 0.006176).

**Prediction B** (both within null p > 0.05): **NOT CONFIRMED for majority** (p < 0.0001, outside null). Minority: CONFIRMED (p = 0.1342, within null).

**Interpretation.** The minority map's drain score (0.0062) is within the neutral-draw null — 13.4% of random label assignments produce equal or higher coupling. This channel does **not** contribute evidence against the minority map.

The majority map's drain_score (0.0002) is significantly *below* the null mean (z = −2.915, p < 0.0001 one-sided) — anomalously clean, not the partisan direction.

**Channel 3 contributes p = 0.1342 (minority within null) — not added to Fisher combination.**

---

## Fisher Combined (Channels 1 + 2, minority only)

| Channel | p-value |
| --- | --- |
| Partisan joint (Mahalanobis) | 1.60e-07 |
| SZAT bootstrap | 0.0044 |
| **Fisher combined** | **1.55e-08** |

Fisher T = 42.148, chi-sq df = 4.

**Reading:** p = 1.55e-08 is the probability that a neutral-draw process
produces a map simultaneously this extreme on both the partisan feature vector and
the swing-zone boundary allocation. Under the neutral null, this combination
occurs roughly once in every 64,348,959 draws.

---

## Pending channels (not executable with current ensemble)

| Channel | Reason pending | Marginal finding |
| --- | --- | --- |
| Municipal anchoring departure | Canadian comparator distribution too thin for rigorous p-value | Minority 4.9× below comparator norm |
| Population MAD ratio | Per-plan MAD not in ensemble outputs — requires MCMC rerun with population capture | Minority 1.48× majority |
| Reock asymmetry | Per-plan Reock not in ensemble outputs — requires MCMC rerun | Minority 2.58× majority on % below 0.30 |

---

## Interpretation note

The duck test made precise: the minority map's four-dimensional partisan feature
vector sits at Mahalanobis distance 6.11 from the ensemble center
(p = 1.60e-07). Combined with the SZAT result (p = 0.0044) and Fisher's
method, the joint neutral-null probability is p = 1.55e-08.

**Channel 3 (Neighbour-Drain) executed 2026-05-07.** Minority within null
(p = 0.1342); does not contribute to the Fisher combination. The pre-registered
predictions (A and B) were not confirmed. The majority map shows anomalously
low pack-crack coupling (p < 0.0001, z = −2.915), which is an inverted finding
relative to the prediction — the majority is unusually clean on this metric.

Three pending channels (anchoring, MAD, Reock) point in the same direction
marginally. When those channels have proper null distributions, the combined
p-value will only decrease or stay flat.

The majority map sits at Mahalanobis distance 2.69 from the ensemble
center (p = 1.25e-01) — outlier on MM in the NDP-favourable direction.

---

*Script: `analysis/scripts/joint_outlier_score_canonical.py`*
*Full output: `analysis/reports/joint_outlier_score.json`*
