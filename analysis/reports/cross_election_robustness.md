---
name: cross_election_robustness
description: Does the v0_9 minority's outlier status hold across 2015, 2019, and 2023 votes, or is it 2023-specific?
type: project
---

# v0_9 cross-election robustness

**Status: directionally holds 3-of-3, with caveats. The minority is more pro-UCP than the majority on `seats_at_50_50` under all three election-year vote distributions.** The 2023 ensemble-percentile defence is partially contaminated by vote-level mismatch and should be reported with that caveat.

## Three-election table

Lane-1 metrics computed on the v0_9 topological substrate (same script shape as `cross_election_v8_full.py`, extended to 2015 and v0_9 polygons; same `seat_results()` definition as `mcmc_ensemble.py`). Vote attribution: 2023 = VA-centroid; 2019 = area-overlap from 2019 enacted polygons; 2015 = re-attribute via `2015_to_2019_crosswalk.csv` then area-overlap.

| Year | Maj s50 | Min s50 | Min − Maj | Min %ile vs 2023 ensemble | Maj %ile | Maj EG | Min EG | Maj decl | Min decl |
|---|---|---|---|---|---|---|---|---|---|
| 2015 | 0.6517 | 0.6517 | 0.000 | 100.00 % | 100.00 % | +0.072 | +0.102 | −0.245 | −0.294 |
| 2019 | 0.5169 | 0.5618 | +0.045 | 100.00 % | 100.00 % | −0.009 | +0.012 | −0.060 | −0.122 |
| 2023 | 0.4607 | 0.4719 | +0.011 | **92.99 %** | 76.88 % | +0.015 | +0.018 | −0.028 | +0.010 |

(Ensemble = the 100k-step ReCom run trained on 2023 votes, `data/v0_1_mcmc_ensemble_samples_250k_v0_8.csv`, n=100,000. Percentile = fraction of ensemble samples with `seats_at_50_50` strictly less than the real map's value. Sign conventions per `mcmc_ensemble.py:seat_results`: positive EG = UCP-favoured; negative declination = UCP-favoured.)

## Headline question — does the minority's outlier status hold?

**Direction: yes, 3-of-3.** Minority s50 ≥ majority s50 in every year. Minority EG ≥ majority EG in every year. Minority declination is more UCP-favoured (more negative) than majority in 2015 and 2019; in 2023 the minority's declination is +0.010 vs majority −0.028 — that's the only direction inversion across all three years × four metrics × two cross-cuts.

**Magnitude: weakens dramatically when the electorate is more UCP-favouring.** In 2023 (UCP 57.4 % two-party share) the minority sits +1.1 pp above the majority on s50 and at the 93rd percentile of the 2023 ensemble — flagged but not an extreme outlier. In 2019 (UCP 62.8 %) the minority is +4.5 pp above the majority and *both* maps sit beyond the maximum of the 2023 ensemble. In 2015 (UCP-equiv 56.0 %, in the same range as 2023) the minority and majority *tie* at 0.6517 — the pro-UCP geometry of the minority and majority cannot be distinguished by this metric at 2015 vote distributions.

The 2015 tie is the single most important nuance: at a UCP vote share comparable to 2023, on 2015 vote *geography*, the minority is **not** more pro-UCP than the majority on s50. The asymmetry that the audit reports for 2023 is partially a function of *which* UCP-leaning polygons are gerrymandered together — and the polygon-level partisan geography in 2015 (Wildrose+PC two-party) was not yet the same as in 2023.

## Ensemble-percentile caveat

The 100k ensemble was trained on 2023 votes only. Comparing 2015/2019 minority s50 against it conflates two things:

  1. **Map-level partisan bias** — what the test is supposed to isolate.
  2. **Election-year vote-distribution skew** — UCP at 56 % vs 63 % vs 57 % shifts the entire s50 distribution, not just the real map's position in it.

The 100 % percentile placements for 2015 and 2019 are dominated by (2): both maps land beyond the ensemble maximum because the ensemble was only run under 2023 vote conditions. A clean test would re-run the ensemble three times (one per election-year vote vector) and place each year's real map within its matched ensemble; we have not done that here. The 2023 row (93 % minority, 77 % majority) is the only one where the percentile reading is not contaminated.

## Verdict

**Holds in 2 of 3 cleanly + qualified pass on the 3rd.**

  - **2023** (clean comparison): minority is a 93rd-percentile outlier; majority is at the 77th. Defensible.
  - **2019** (vote-mismatch caveat applies): direction holds clearly (+4.5 pp s50 gap, all four metrics agree).
  - **2015** (vote-mismatch caveat applies, plus the s50 gap is **zero**): direction holds on EG, mean-median, and declination; but s50 — the headline metric — ties. The 2015 tie is honest evidence that the s50 asymmetry is partly a 2023-vote-distribution artefact, not purely a structural property of the maps.

This is closer to "Holds in 2 of 3" than "Holds in 3 of 3." It does **not** support the strong framing "the minority is a structural pro-UCP outlier under any vote distribution." It supports the weaker framing "the minority is a 2023-vote pro-UCP outlier; in earlier vote geographies the structural advantage shrinks (2019) or vanishes (2015 s50)."

For Lane 1 the recommended report-text change is to add this 2015/2019/2023 table and an honest paragraph noting the s50 tie in 2015. The headline "1-seat asymmetry on the 100k ensemble" remains valid for 2023 votes but should not be implicitly extended to other election years.

## 338Canada cross-check (separate)

`analysis/scripts/338canada_historical.py` was re-run; the live fetch timed out at 10 min (Wayback CDX rate limits + 87 per-riding pulls), so its existing cached outputs (last refreshed 2026-04-23) remain authoritative. Per `data/reference/polling_338_historical/stability_table.csv`:

  - **2026-04-12 current snapshot** (full 87-riding scrape): majority UCP/NDP = 67/22, minority = 66/23 → minority is **−1 UCP, +1 NDP** vs majority.
  - **Pre-2023-election snapshot** (Wayback last capture per riding, March-May 2023): majority 48/39, minority 49/39 → minority is **+1 UCP** vs majority.

The 338 cross-check therefore shows the *minority-versus-majority asymmetry direction itself flips between 2023-pre-election projection (minority more pro-UCP) and the current 2026-04-12 projection (minority less pro-UCP)*, which is independently consistent with the 2015 s50 tie reported above: the asymmetry is sensitive to the underlying vote distribution and is not a fixed structural property of the maps. The 338 aggregate uniform-swing sweep over 77 snapshots (`uniform_swing_stability.csv`) shows the same dependence on provincial UCP share.

## Data and reproduction

  - Per-map per-year metrics: `data/cross_election_per_map.csv` (6 rows: 2 maps × 3 elections) and `.json`.
  - Script: `analysis/scripts/cross_election.py`.
  - Total runtime: ~11 minutes (dominated by 2015/2019 area-overlap into 89 v0_9 polygons × 87 2019 polygons; 2023 VA-centroid join is ~0.1 s).
