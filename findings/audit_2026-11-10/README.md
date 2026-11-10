# Audit recomputations, 2026-11-10

2026-11-09 23:11 Alberta time · claude-fable-5-2 · medium

**Exploratory. Everything here was computed after the fact for the 2026-11-10 audit.** None of it is a registered test, and none of it changes a registered result. The audit found problems whose fixes need new numbers in the reports. The project's rule is that no number goes into a report unless a committed script produces it from committed data. This folder holds those scripts and their outputs.

## How to run

From the repository root, with the packages in `requirements.txt`:

```
git lfs pull          # the .gpkg inputs are Git LFS objects
python findings/audit_2026-11-10/<script>.py
```

Each script reads only committed files, uses no network and no random numbers, and writes its output beside itself. Each was run twice and gave byte-identical output. None of them writes to `data/outputs/script_run_audit.jsonl` or anywhere outside this folder. Run on Python 3.13, numpy 2.5.3, pandas 3.0.5, scipy 1.16.3, geopandas 1.1.3.

| Item | Script | Output |
|---|---|---|
| 1 | `joint_sensitivity.py` | `joint_sensitivity.json` |
| 2 | `ess_uncapped.py` | `ess_uncapped.json` |
| 3 | `calgary_zone_recode.py` | `calgary_zone_recode.json`, `calgary_zone_recode_districts.csv` |
| 4 | `s15_distances.py` | `s15_distances.json` |
| 5 | `pct_rank_ties.py` | `pct_rank_ties.json` |
| 6 | `seat_counts_table.py` | `seat_counts_table.json`, `seat_counts_table.md` |
| 7 | `polls_338.py` | `polls_338.json` |

## 1. How firm is "one in 568,000"? (`joint_sensitivity.py`)

**Asked.** The reports say a neutral process would produce the minority map's combined four-measure profile about once in 568,000 tries. How far does that figure move under other defensible ways of computing it?

**Method.** The published figure measures how far the map's four scores sit from the centre of 1,010,000 neutral plans (a Mahalanobis distance, D²), reads the chance off a chi-square curve, and doubles it. The script recomputes that, then changes one choice at a time. The rank-based version replaces each measure by its normal score (a plan's midrank turned into a standard-normal value) before computing D², which removes skew in single measures. The script also counts sampled plans that are at least as extreme as the map.

**Result, minority map. All on election-day ballots.**

| Version | D² | Chance, exact | Chance, doubled |
|---|---:|---:|---:|
| Published (four measures, chi-square) | 33.64 | 1 in 1,131,382 | 1 in 565,691 |
| Hotelling, 1,413 effective draws | 33.64 | 1 in 898,736 | 1 in 449,368 |
| Hotelling, 894 effective draws (item 2) | 33.64 | 1 in 788,907 | 1 in 394,454 |
| Drop efficiency gap | 29.72 | 1 in 633,877 | 1 in 316,938 |
| Rank-based (normal scores) | 31.80 | 1 in 476,829 | 1 in 238,414 |
| Drop declination | 27.28 | 1 in 194,852 | 1 in 97,426 |
| Forest-ReCom sampler (80,000 plans) | 26.54 | 1 in 40,682 | 1 in 20,341 |

- **Honest range: between roughly 1 in 20,000 and 1 in 570,000** (doubled, as published), or 1 in 97,000 to 1 in 570,000 on the main sampler alone. Every version is rarer than 1 in 10,000. The published 568,000 is 565,691 before rounding.
- Declination and efficiency gap correlate at 0.973, so they are close to one measure counted twice.
- Sampled plans at or beyond the minority map: 0 of 1,010,000 on the published D² (the largest sampled D² is 28.43). On the rank-based D² there are 7. On a one-sided count that adds up how rare each measure is, there are 4. 29 plans match or beat it on mean-median and seats at 50/50 together.
- The model's tail is too thin where it can be checked. Between D² = 13 and 24 the sample holds 1.2 to 3.0 times as many plans as the chi-square curve predicts (1.16 at 13; 1.56 at 16; 2.38 at 20; 2.05 at 24). All four chains agree in direction from 16 up.
- Majority map: D² 7.74, chance 0.10 (about 1 in 10); 102,111 sampled plans are at least as far out. 2019 map: D² 13.16, chance 0.0105 (about 1 in 95); 12,370 plans. Neither is unusual under any version; the full set is in the JSON.

**All ballots: cannot be computed.** The joint figure needs every neutral plan's four scores on all ballots. The all-ballots replay of the 1,010,000 plans is not committed on this branch or on any of the 96 local and remote branch refs in this clone, including `origin/amendment17-local-runs` (searched with `git ls-tree`; the script repeats the search). Only single-measure percentiles are committed, and on all ballots the two measures that carry most of the distance get weaker (mean-median p99.97 to p98.73, seats p99.99 to p99.90). So the election-day figure should not be quoted as if it held on all ballots. The JSON says how to produce the missing chains.

**Limits.** Every model figure lies beyond the largest sampled D², where the curve's shape cannot be checked. The neutral plans have 87 districts and the commission maps 89. The doubling was set for two channels and only one remains, so exact values are given beside it. The forest-ReCom run is small (about 60 to 120 effective draws) and is a rough check, not an equal second estimate. Two counts differ by one from the auditors' scratch figures (7 against 6, 4 against 3): the scratch run read the plans with the parser that breaks ties (item 5).

## 2. How many independent draws? (`ess_uncapped.py`)

**Asked.** The reports say the million plans are "worth about 1,400 independent draws". The pipeline stops adding up the chain's memory at lag 2,000. What does it give with no cap?

**Method.** Effective sample size is the number of plans divided by the autocorrelation time, a sum of autocorrelations. The script computes it three ways: the pipeline's rule with its cap; the same rule run to the first non-positive autocorrelation; and Geyer's initial positive sequence. Each is done on the four chains joined end to end (the pipeline's "pooled" figure), on each chain alone, and with the textbook multi-chain combination.

**Result.**

| Measure | Published (capped) | Uncapped, pooled | Geyer, multi-chain | Uncapped, per-chain sum |
|---|---:|---:|---:|---:|
| Efficiency gap | 1,522 | 1,037 | 1,057 | 1,066 |
| Mean-median | 1,448 | 1,250 | 1,238 | 1,300 |
| Declination | 1,513 | 1,039 | 1,057 | 1,083 |
| Seats at 50/50 | 1,413 | 894 | 899 | 1,229 |

- The capped figures reproduce exactly (1,413 to 1,522). The cap binds everywhere: the autocorrelation is still 0.05 to 0.07 at lag 2,000, so the published figures are upper bounds.
- **Figure to quote: "about 1,000 independent draws" (roughly 900 to 1,300, depending on the measure and the estimator).**
- Against the reports' own floor of 1,000: efficiency gap, mean-median and declination clear it on every uncapped estimate. **Seats at 50/50 does not** on the pooled estimates (894 and 899); it clears only when each chain is measured against its own mean (1,229), which ignores disagreement between chains.
- On the joined chains the uncapped rule and Geyer's rule agree to the first decimal, because the autocorrelation crosses zero smoothly.

**Limits.** These estimates have their own sampling error, very roughly 10 to 20 percent. They describe how well an average is known; far-tail percentiles such as p99.99 rest on a handful of excursions and are known less well than these numbers suggest.

## 3. The Calgary zone gap, recoded by the stated rule (`calgary_zone_recode.py`)

**Asked.** The report states a geographic rule for Calgary's two zones (Zone A is north or east of the Bow River through downtown, then Deerfoot Trail). The committed lists do not follow it everywhere. What is the gap if the rule is applied literally?

**Method.** Each official Calgary district's centroid is tested against a line built from the Bow River (OpenStreetMap) and Deerfoot Trail (Highway 2 in the National Road Network file). Populations are the commission's tables, as in the published figure. The rule is silent on two points, so each is run both ways: where the line passes from river to freeway, and what the line does west of the city.

**Result.** Gap = Zone A's average population over Zone B's.

| Coding | Majority gap | Minority gap |
|---|---:|---:|
| Committed lists (published) | +0.36% | +12.20% |
| Report's partial recode (3 districts, minority only) | +0.36% | +7.70% |
| Literal rule | −2.57% or −3.07% | +5.70% or +5.30% |

- The two districts at issue, **Calgary-Hays and Calgary-South East**, are coded Zone B, but their centroids are east of Deerfoot Trail on both maps (3.6 to 14.3 km), so the rule puts them in Zone A. Calgary-Buffalo and Calgary-Currie move to Zone B on both maps, and Calgary-Peigan-Chestermere to Zone A on the minority map.
- **Calgary-Confluence (majority)** has its centroid in the strip between the river and the freeway, about 240 m west of Deerfoot. If the river governs there it is Zone A (gap −2.57%); if the freeway governs, Zone B (−3.07%).
- **Calgary-Nolan Hill-Cochrane (minority)** has its centroid west of Cochrane, 3 km south of the Bow. Following the river upstream puts it in Zone B (+5.70%); keeping it in Zone A gives +5.30%, which is the auditors' figure.
- **The April 24 "2×" rule** (the test passes if the minority's gap is no more than twice the majority's). On the committed lists it fires easily: 12.20 against 0.73. On the literal rule, comparing sizes, it turns on Calgary-Confluence alone: with Confluence in Zone A it fires narrowly (5.70 or 5.30 against 5.14); with Confluence in Zone B it does not (against 6.14). Read with signs, as written, it fires under every coding, because the majority's gap is negative.
- The public report's measure still holds under every coding: the minority's Zone A is 8.5% to 11.5% above the provincial average (majority 1.3% to 2.8%).
- Every district's zone under every coding is in `calgary_zone_recode_districts.csv`.

**Limits.** A centroid is one point, and Confluence's is within a few hundred metres of both lines. The river file has no names, so the Bow is picked out by position. This item does not address how the lists were first chosen.

## 4. The s.15(2)(b) distance (`s15_distances.py`)

**Asked.** Criterion (b) needs more than 150 km from the Legislature to the district's nearest boundary by the most direct highway route. What does the audit's own road model give for Rocky Mountain House-Banff Park and Lesser Slave Lake?

**Method.** The road model is committed, so this was feasible. The script uses the method of `analysis/scripts/s152_criteria.py`: shortest path over the OpenStreetMap highways extract from the Legislature to the first road point inside each official district.

**Result.**

| District | Road model | Straight line | (b) met? |
|---|---:|---:|---|
| Rocky Mountain House-Banff Park (minority) | 165.2 km | 105.1 km | Yes |
| Lesser Slave Lake (both maps) | 134.1 km | 113.1 km | **No** |
| Central Peace-Notley (both maps) | 220.0 km | 188.7 km | Yes |
| Canmore-Banff (majority) | 314.5 km | 220.6 km | Yes |

- The audit's existing per-voting-area file agrees: 163.2, 134.1, 220.0 and 312.8 km.
- The report hedges (b) for Rocky Mountain House-Banff Park using Rimbey's road distance. **Rimbey is not in that district**: on both official maps the whole town is in Wetaskiwin-Ponoka-Maskwacis.
- The report credits (b) to Lesser Slave Lake. On the same model it falls short by 16 km, on both maps.

**Limits.** This is a model on a highways extract, not a surveyed route. Rocky Mountain House-Banff Park is only 105 km away in a straight line, so its 165 km depends on local roads not counting as a "highway route". Lesser Slave Lake's shortfall does not have that weakness: adding roads cannot lengthen a shortest path. The script does not recompute the other four criteria, so it does not by itself give the new counts out of five.

## 5. The percentile tie bug (`pct_rank_ties.py`)

**Asked.** The percentile code compares decimals for exact equality after reading them from a CSV. Which seats-at-50/50 values does that break, and which published percentiles change?

**Method.** For every k/87, k/89 and k/91 the script writes the value as the chain files hold it, reads it back with the default parser and with the exact one, and lists the values that come back one step off. It then recomputes every published percentile both ways for the main ensemble, the forest-ReCom run and the four 89-district sets (streamed from `origin/amendment17-local-runs` with `git show`; nothing is checked out).

**Result.**

- Values that mis-parse: **33 of 88 for k/87, 32 of 90 for k/89, 36 of 92 for k/91.** The full lists are in the JSON. They include 40/87 and 41/87, 42/89 and 43/89, and 39/91 to 42/91. About half of the main ensemble's seats values (506,567 of 1,010,000) are read one step off.
- **Only one published percentile changes: the 2019 map's seats at 50/50.** It is published as 78.54. With its 266,278 tied plans counted as half, the midrank is **65.36** (52.17% of plans are strictly below, 78.54% at or below).
- Everything else checked reproduces and is unchanged: the other 17 main-ensemble percentiles, the 8 forest-ReCom ones, and the 32 placements in the 89-district sets. The majority's 41/89 and the minority's 46/89 parse exactly, so their ties in the 89-district sets were already counted.

**Limits.** The all-ballots percentiles could not be rechecked because those chains are not committed. The 2019 map's all-ballots value is 41/87, which mis-parses, so its published 74.08 is very likely "at or below", not a midrank. The majority's all-ballots value, 42/89, also mis-parses and would matter in any 89-district all-ballots ranking. The 91-district sets were not recomputed. Which strings mis-parse depends on the pandas parser; the version is recorded.

## 6. One seat table (`seat_counts_table.py`)

**Asked.** One table of UCP-NDP seats on 2023 votes for all five maps, on both sets of ballots, that every surface can cite.

**Method.** Each of the 4,765 voting areas belongs to one district on each map; votes are added up by district and the larger party takes the seat. The commission maps use the official boundary files; the panel's map and the ¶167 map use the audit's reconstructions. "Tied vote" shifts every district by the same amount until the province is 50/50.

**Result.** UCP-NDP.

| Map | Seats | Election-day ballots | All ballots | Tied vote, election-day | Tied vote, all ballots |
|---|---:|---:|---:|---:|---:|
| 2019 map | 87 | 57-30 | 49-38 | 40-47 | 41-46 |
| Commission majority | 89 | 55-34 | 48-41 | 41-48 | 42-47 |
| Commission minority | 89 | 60-29 | 55-34 | 46-43 | 46-43 |
| Panel's map (reconstruction) | 91 | 58-33 | 51-40 | 44-47 | 45-46 |
| ¶167 map (reconstruction) | 91 | 56-35 | 50-41 | 43-48 | 44-47 |

These match every figure already published. Election-day ballots: 932,164, UCP two-party share 57.40%. All ballots: 1,764,915, UCP two-party share 54.44%.

**Limits.** The all-ballots counts use the registered allocation, which spreads ballots not cast on election day evenly by party within each 2019 district. Some seats rest on very few modelled votes: on all ballots, Calgary-Edgemont on the minority map is NDP by 3.6 votes and Calgary-Acadia on the majority map is UCP by 9.7. The audit found other defensible allocations move the minority's all-ballots count to 56 or 57. Two maps are reconstructions, not official files.

## 7. Polls and projection (`polls_338.py`)

**Asked.** The chart labels 338Canada's 48-43 as "latest polls". Give the polls and the projection separately.

**Method.** The script reads the saved text of 338Canada's Alberta page and takes the four listed polls, their plain average and the projection block.

**Result.**

| | UCP | NDP | UCP lead |
|---|---:|---:|---:|
| Pollara, Oct 9 | 46 | 50 | −4 |
| Mainstreet, Oct 16 | 43 | 43 | 0 |
| Abacus, Oct 10 | 47 | 42 | +5 |
| Léger, Oct 3 | 47 | 45 | +2 |
| **Plain average of the four** | **45.75** | **45.0** | **+0.75** |
| **338Canada projection, Oct 19** | **48** (43-53) | **43** (39-48) | **+5** |

The projection is 338Canada's model output. It is 4.25 points more favourable to the UCP on the lead than the plain average of the polls listed beside it.

**Limits.** The saved file prints the poll numbers with no party labels. The script reads the first as UCP and the second as NDP, the order of the projection block in the same file and of the page header as the auditors re-read it; the header itself is not in the repository. The average is unweighted. 338Canada's model weights polls and adds other inputs, so the two are not expected to match.

## The stance-label sample (`submissions_sample48_judgements.csv`)

Entry: 2026-11-09 23:28 Alberta time · claude-fable-5-2 · medium

**What it is.** 48 rows drawn at random from the old submissions search (`findings/submission_search_findings.md`), each read against the submission's own text by an auditor. `llm_label` is the label the old search gave; `audit_judgement` says whether that label is right.

**Result.** 31 of the 48 rows carried a support or oppose label. 26 of those 31 were wrong, many of them reversed. The 17 neutral labels were all right.

**Limits.** One auditor judged the sample; it was not double coded. The full recode in `findings/submissions_recode/` replaces the old labels and is double coded.
