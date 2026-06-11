---
name: drain_metric_validation
date: 2026-06-11
verdict: RETAIN_BUT_DROP_LISA_FRAMING_AND_RESTATE_PUBLISHED_NUMBERS
script_commit: 3bfeefa335942064cde342fa49b63b842c1fa277
---

> **Backward:**
> - `analysis/scripts/drain_metric_validation.py` — this analysis
> - `findings/neighbour_drain_analysis.md` — the §5.3.5 result this validates
> - `findings/drain_label_shuffle_null.md` — Phase B null result (Prediction A failure)
> - `analysis/methodology/neighbour_drain_design.md` — pre-registered design
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.3.5 — to be amended per the verdict below

# Drain-metric validation (justify-or-drop)

## Verdict

**RETAIN_BUT_DROP_LISA_FRAMING_AND_RESTATE_PUBLISHED_NUMBERS.** V1 PASS (construct validity holds); V2 FAIL (LISA framing is not numerically anchored — correlation 0.11 majority, ~0 minority, well below 0.30 threshold); V3 PASS (Prediction A confirms on canonical substrate). Three actions required: (a) drop the 'directional bivariate Local Moran's I / LISA' language from §5.3.5 — it is rhetorical, not numerical; (b) re-anchor the §5.3.5 reading on the canonical-substrate numbers (majority = 0.0072, minority = 0.0006) instead of the stale DPG/blended-substrate numbers (majority = 0.000179, minority = 0.006176) currently cited in findings/joint_outlier_score.json and findings/drain_label_shuffle_null.md; (c) retract the joint-outlier 'majority anomalously low (z=-2.915)' framing — it reflects a substrate that has been superseded for every other audit channel.

| Validation | Result |
|---|---|
| V1 — Synthetic ground truth | **PASS** |
| V2 — LISA numerical anchor | **NO** |
| V3 — Pre-registered Prediction A confirmed | **YES** |

## V1 — Synthetic ground truth

Two constructed 9-ED grid maps, identical statewide vote totals (~50/50), 1000 voters per ED, rook contiguity.

- **NEUTRAL**: each ED 50/50 ±2 % jitter. No coupled chain signal expected.
- **PACK-AND-CRACK**: center ED P4 is 90/10 UCP (NDP packed losing by 80 points). Surrounding 8 EDs are 48/52 UCP (NDP narrowly losing). Every (P4, P_outer) directed pair is coupled (same loser) and clears both thresholds.

| Map | drain_score | coupled chain count | construct expectation |
|---|---:|---:|---|
| NEUTRAL | 0.0 | 0 | drain_score ≈ 0 |
| PACK-AND-CRACK | 0.00996 | 4 | drain_score ≫ neutral |

Ratio (pack-crack / neutral): **inf**

**Construct-validity pass criterion (pre-committed):** pack-crack score ≥ 10× neutral score AND pack-crack score ≥ 0.005. Result: PASS.

## V2 — Local Moran's I (bivariate) comparator

For each directed adjacent pair (X, Y) on each canonical Alberta map, compute the bivariate local Moran's I analog

```
I_pair = z_s(X) × (-z_m(Y))
```

where z_s(X) is the standardized winning-surplus rate at X and -z_m(Y) is the negated standardized margin at Y (so that small margins map to large positive values). The audit's §5.3.5 framing as a 'directional bivariate Local Spatial Autocorrelation' analog is anchored only if |I_pair| correlates with the drain-intensity at the same pair.

| Map | Directed pairs | Pearson corr(|I_pair|, drain_intensity) |
|---|---:|---:|
| majority | 502 | 0.1142 |
| minority | 514 | -0.0021 |

**Anchor criterion (pre-committed):** at least one map's |I_pair|↔drain-intensity Pearson r ≥ 0.30.

## V3 — Pre-registered direction replication

- Pre-registered Prediction A: drain(majority) > drain(minority).
- Observed: majority = 0.007213, minority = 0.000591.
- Direction observed: `majority_higher`.
- Prediction A confirmed: **YES**.

Label-shuffle null over 1000 trials gives P(majority > minority | random labels) = 0.912 and P(majority < minority | random labels) = 0.088.

Pre-registered Prediction A (drain(majority) > drain(minority)) CONFIRMS on the canonical EA substrate: majority = 0.007213, minority = 0.000591. The label-shuffle null on the same canonical substrate gives P(majority > minority) = 0.912 — the observed direction is the expected one under random labeling, so confirming Prediction A is not strong evidence on its own; the strength of the finding rests on the observed magnitudes vs the null distribution. IMPORTANT REVERSAL: the previously published Phase B numbers (majority = 0.000179 < minority = 0.006176) and the joint-outlier "majority anomalously low (z=-2.915)" framing were computed on a DPG-era / blended-vote substrate. On the canonical Elections Alberta shapefiles + canonical VA centroid-in-polygon attribution — the substrate every other audit channel uses — the direction is reversed. The audit's published §5.3.5 narrative needs to be re-anchored on the canonical numbers; the prior 'majority anomalously clean' reading does not survive substrate refresh.

## Reproducibility

```bash
python analysis/scripts/drain_metric_validation.py
```

Script commit: `3bfeefa335942064cde342fa49b63b842c1fa277`
