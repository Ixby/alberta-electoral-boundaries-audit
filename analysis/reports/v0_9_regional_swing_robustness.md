---
name: v0_9_regional_swing_robustness
description: Does the minority map's p98.6 seats@50/50 finding survive a regional-swing recomputation?
type: project
---

# v0_9 regional-swing robustness check

**Status: the headline p98.6 finding for the minority map COLLAPSES under regional swing — the minority drops to p50.7. But the same recomputation puts the *majority* map at p99.5 in the opposite direction. The uniform-swing assumption was load-bearing; the headline framing has to change, but a defensible (different) outlier story replaces it.**

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

Ensemble re-rank: the 100k production ensemble stores only district-level summaries, not per-VA assignments, so it cannot be re-scored under regional swing. The **10k verification subset** (`v0_1_mcmc_verification_assignments.npz`, same seed family / same chain configuration) preserves full per-VA assignments and was used. Sanity check: the 10k subset's uniform-swing s50 distribution matches the 100k production distribution to within 0.002 on the mean and exactly on p5/p95 — it is a valid stand-in for percentile rankings (denominator caveat below).

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
