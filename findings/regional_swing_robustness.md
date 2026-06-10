---
name: v0_9_regional_swing_robustness
description: Does the minority map's p98.6 seats@50/50 finding survive a regional-swing recomputation?
type: project
status: SUPERSEDED — DPG-substrate reading; replaced by canonical recomputation
superseded_by: findings/regional_swing_canonical_robustness.md
superseded_date: 2026-06-10
---

> ⚠️ **SUPERSEDED 2026-06-10.** This document records the regional-swing recomputation against the v0_9 DPG-era minority map (uniform-swing s50 ≈ 0.483, regional-swing s50 ≈ 0.42, dropping the minority to p50.7). The **canonical Elections Alberta shapefiles** produced a minority with uniform-swing s50 = 0.5169 and regional-swing s50 = 0.4607 — *above* the maximum of every plan in the 10k verification subset, p100 against both swings. The v0_9 reading underestimated the minority's Lane-1 effect because DPG attribution missed rural-ED VAs that biased seat counts toward NDP. The canonical recomputation supersedes this finding's headline. The methodology, the regional-swing calibration, and the limitations section below are still accurate; only the v0_9-specific s50 values and the "p98.6 collapses to p50.7" headline are superseded. See `findings/regional_swing_canonical_robustness.md` for the canonical reading.

> **Backward:**
> - `analysis/scripts/seats_at_50_50_regional.py` — companion script producing the regional-swing recomputation
> - `verification_assignments_raw.npz` — 10k verification subset with per-VA assignments
> - 2019 → 2023 two-party regional swing inputs
>
> **Forward:**
> - `findings/regional_swing_canonical_robustness.md` — **canonical reading; supersedes this file's headline**
> - `reports/academic/report_academic.md` — incorporates the canonical regional-swing robustness check
> - `findings/joint_outlier_score_summary.md` — cross-references the recomputed percentiles
> - `findings/README.md` — indexes this finding

# v0_9 regional-swing robustness check *(SUPERSEDED — see canonical reading)*

**Original status (v0_9 reading, superseded): the headline p98.6 finding for the minority map COLLAPSES under regional swing — the minority drops to p50.7. But the same recomputation puts the *majority* map at p99.5 in the opposite direction. The uniform-swing assumption was load-bearing; the headline framing has to change, but a defensible (different) outlier story replaces it.**

**Current status (canonical reading, 2026-06-10): the v0_9 reading was an artefact of DPG-substrate underestimation of the minority's seat effect. Under canonical Elections Alberta shapefiles, regional-swing recomputation does *not* falsify Lane 1 — the minority's regional-swing s50 of 0.4607 sits above every plan in the 10k verification subset. See `findings/regional_swing_canonical_robustness.md`.**

## What the hostile-witness attack said

The audit's central Lane-1 number — minority `seats@50/50` = 0.483 at the 98.6th percentile of a 100k ReCom ensemble — is computed under **uniform partisan swing**: every district's UCP share is shifted by the same constant so province-wide UCP = 50%. The attack: Alberta does not swing uniformly. From 2019 to 2023, Calgary swung ~11.5 pts toward the NDP, rural Alberta ~8.1 pts, Edmonton only ~4.3 pts. A uniform shift inflates the seat value of rural/suburban hybrid districts that "should" be safer for the UCP than the provincial average implies.

## Method

Three regions: **Calgary** (26 EDs), **Edmonton** (20 EDs), **Rural** (41 EDs, including the two `Calgary-area` EDs Airdrie-Cochrane and Chestermere-Strathmore — both swing rural-style on inspection). Each VA inherits its region from `parent_ed_2019`, fixed by geography and independent of any candidate map's district lines.

Empirical 2019 → 2023 two-party (UCP / (UCP + NDP)) swing:

| region | 2019 UCP 2p | 2023 UCP 2p | swing | ratio to provincial |
|---|---:|---:|---:|---:|
| provincial | 0.6268 | 0.5412 | -0.0856 | 1.000 |
| Calgary | 0.5981 | 0.4832 | -0.1149 | **1.342** |
| Edmonton | 0.3973 | 0.3543 | -0.0430 | **0.503** |
| Rural | 0.7439 | 0.6627 | -0.0812 | **0.949** |

Regional `seats@50/50`: solve numerically for the shift `s` such that, after applying a per-VA delta of `s · ratio[region(VA)]`, province-wide post-shift UCP 2-party share = 0.5; then aggregate to candidate districts and count UCP wins. Implementation: `analysis/scripts/seats_at_50_50_regional.py`. Pass `--all-three` to score 2019 enacted, v0_9 majority, v0_9 minority. The required shift is `s* = -0.0763` (Calgary VAs shift by -0.1024, rural by -0.0723, Edmonton by -0.0383).

Ensemble re-rank: the 100k production ensemble stores only district-level summaries, not per-VA assignments, so it cannot be re-scored under regional swing. The **10k verification subset** (`verification_assignments_raw.npz`, same seed family / same chain configuration) preserves full per-VA assignments and was used. Sanity check: the 10k subset's uniform-swing s50 distribution matches the 100k production distribution to within 0.002 on the mean and exactly on p5/p95 — it is a valid stand-in for percentile rankings (denominator caveat below).

## Results

| map | s50 (uniform) | percentile (uniform, 100k) | s50 (regional) | percentile (regional, 10k) | denominator |
|---|---:|---:|---:|---:|---:|
| 2019 enacted | 0.460 | p76.9 | 0.414 | **p50.7** | 87 |
| v0_9 majority | 0.461 | p76.9 | 0.449 | **p99.5** | 89 |
| v0_9 minority | 0.483 | **p98.6** | 0.416 | **p50.7** | 89 |

Ensemble distributions:

| metric | mean | p5 | p50 | p95 | max |
|---|---:|---:|---:|---:|---:|
| s50_uniform (10k) | 0.452 | 0.425 | 0.448 | 0.483 | 0.483 |
| s50_regional (10k) | 0.420 | 0.402 | 0.414 | 0.437 | 0.460 |

Note: the 87-district ensemble vs 89-district real maps gives slightly different available seat fractions, but the percentile interpretation is unaffected (s50 is a share, the distribution is dense enough that the granularity step is small relative to the spread).

## Verdict

**The headline p98.6 finding does not survive regional swing.** The minority map's regional s50 is at the median of the comparison ensemble. Under uniform swing the minority looked like a strong UCP gerrymander; under regional swing it looks like a typical map. *Why* it moves: the minority's supposedly-suspicious seats are concentrated in Calgary/Calgary-area, where the actual partisan swing is much larger than the provincial average. A regional swing gives the NDP more votes per Calgary district than uniform does, flipping the marginal Calgary districts in the minority map back to NDP.

**But the same recomputation flags the majority map at p99.5 in the opposite direction.** The majority's regional s50 (0.449) is higher than 99.5% of the ensemble — meaning the majority map gives the UCP *more* seats than nearly any random map does, when swing is regionally-weighted. This is a different finding (the majority "wastes" too few UCP votes given how Calgary actually swings) but it is also an outlier signal.

**Recommendation:** The Lane-1 framing has to be rewritten. Three honest options:

1. Drop seats@50/50 as a Lane-1 metric and lead with the still-robust efficiency-gap and declination findings on the minority (those are not swing-dependent in the same way).
2. Keep seats@50/50 but report **both** numbers, headlined "the minority's apparent UCP-favourability under uniform swing reverses to neutral under empirical regional swing; the majority's apparent neutrality under uniform swing reverses to a pro-UCP outlier under regional swing."
3. Treat regional swing as an **alternative scenario**, not a replacement, and show both in a sensitivity table — leaving the reader to weigh which assumption is more defensible.

Option 2 is the least misleading. Option 3 is the most academically conservative. Option 1 throws away a real signal.

The hostile witness is essentially right that the published number is uniform-swing-dependent — but they are not right that the underlying gerrymandering question goes away. It just relocates.
