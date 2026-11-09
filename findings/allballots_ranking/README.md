# All-ballots ranking: every map against plans scored on the same ballots (2026-11-05)

**Sensitivity analysis, not registered.** Every registered test, the canonical ensemble and the headline use election-day votes, and none of them change. This note gives no conclusion on whether any map is a gerrymander.

## Why

C51 (2026-11-05) added the Vote Anywhere ballots back and scored the real maps on all ballots. It ranked those scores against plans scored on election-day votes only, or against levels calibrated on election-day votes. That comparison mixes vote data: adding the missing ballots moves the simulated plans about as much as the real maps (canonical median efficiency gap +1.63% → −1.57%; set D +1.53% → −1.58%). This note ranks each map against the same plans rescored on all ballots.

## How

ReCom proposals depend only on population, so the same seeds give the same plans whatever votes are attached. Both ensembles were replayed with their original seeds on `data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg` (from `vote_anywhere_splat.py --primary`, commit `4f7de6bb`; SHA-256 `c9e21ac90fb97b9ee4a7e4da7c80d44922e5849842fc283344f724bb2711be72`). That file is the election-day file with `va_ucp/va_ndp/va_other` replaced by all-ballots values; it equals the official result in all 87 districts.

| Ensemble | Command | Ran (MST) | Plans |
|---|---|---|---|
| Canonical (87 districts, base seed 1432864451) | `mcmc_ensemble_canonical.py --n-steps 1010000 --n-chains 4 --chunk-size 5000 --run-id allballots --va-file <primary gpkg> --max-workers 4` | 01:55–04:18 | 4 × 252,500 |
| Set D (91 districts, s.15(2), idx 251–254) | `close_seats_ensemble.py nk --k 91 --idx N --steps 252500 --chunk 500 --s152 data/outputs/s15_2_va_criteria.csv --va-file <primary gpkg> --out data/simulation_checkpoints_k91_s152a23_allballots/chainN_samples.csv` (run in the `alberta_audit` clone) | 02:07–03:12 | 4 × 252,500 |

The first set D launch (01:56) failed at startup on an unquoted path and wrote no rows; it was relaunched unchanged at 02:07.

**Replay check.** In every chain, every row's vote-independent columns equal the original run's: `step, population_mad, reock_proxy_median, reock_proxy_pct_below_030, n_districts` for the canonical; also `n_parts, n_city_districts, towns_flagged, s152_districts` for set D. So these are the same 2,020,000 plans, with only the votes changed. The election-day column below reproduces the report's existing percentiles (for example minority efficiency gap p94.54, majority mean-median p0.99). No script or output for this check is committed, and neither is the script that wrote `canonical_ranking.json`, so this paragraph is the check's only record in the repository.

The all-ballots chain CSVs are not committed (the election-day canonical chains are, in `data/simulation_checkpoints_canonical/`). SHA-256:

```
ba0f12106c65d306ad8e2e43ef9be0aadebf7147f6bb8041ace159c9165ff5ad  data/simulation_checkpoints_allballots/chain0_samples.csv
57ab214c41aea18e506a57f6a2d7ae3a23b2aa5c5d5fe4f93d6bc8f9f8db252d  data/simulation_checkpoints_allballots/chain1_samples.csv
e156dc1255e84f38681b845758d0bd7f880edcffd8526248c753b2913da6ffe7  data/simulation_checkpoints_allballots/chain2_samples.csv
9c0602db0ea8fff8b61d7b0c7c4fb27bcbf5ca61ef32fc9112ce24d29b5a189e  data/simulation_checkpoints_allballots/chain3_samples.csv
67d8baf28ecbada2b0ebdda8b8d47a8f0e9aba30e35ddf81973437e74e1345be  (alberta_audit) data/simulation_checkpoints_k91_s152a23_allballots/chain251_samples.csv
d1150b3c8f975fced8d93c6c95318d63b83b366304ae947a802699ee3e50a9ca  (alberta_audit) data/simulation_checkpoints_k91_s152a23_allballots/chain252_samples.csv
dd925ec6df2f7580d30eb33bd817f95dd7f21889d6d1ae593960566af1c5bef9  (alberta_audit) data/simulation_checkpoints_k91_s152a23_allballots/chain253_samples.csv
85a9f0978846bd155ea9ac4ff19bc33dfc024bf1c9ce86e90cdf4274dddd881b  (alberta_audit) data/simulation_checkpoints_k91_s152a23_allballots/chain254_samples.csv
```

## Results: the 2019 map and the commission maps against the canonical ensemble

Midrank percentiles, 1,010,000 plans each, with one exception noted below the table. Source: `canonical_ranking.json`.

| Map | Measure | Election-day value | Percentile | All-ballots value | Percentile |
|---|---|---:|---:|---:|---:|
| 2019 | Efficiency gap | +2.41% | 69.46 | −2.64% | 27.59 |
| 2019 | Mean-median | −0.77% | 91.81 | −2.22% | 28.00 |
| 2019 | Declination | +0.045 | 91.33 | −0.057 | 49.84 |
| 2019 | Seats at 50/50 | 0.460 | 78.54 | 0.471 | 74.08 |
| Majority | Efficiency gap | +0.10% | 16.52 | −2.70% | 26.48 |
| Majority | Mean-median | −3.62% | 0.99 | −3.51% | 1.24 |
| Majority | Declination | −0.027 | 21.85 | −0.093 | 17.26 |
| Majority | Seats at 50/50 | 0.461 | 78.54 | 0.472 | 74.08 |
| Minority | Efficiency gap | +4.02% | 94.54 | +2.55% | **98.82** |
| Minority | Mean-median | +1.04% | 99.97 | +0.08% | 98.73 |
| Minority | Declination | +0.077 | 98.79 | +0.046 | 99.82 |
| Minority | Seats at 50/50 | 0.517 | 99.99 | 0.517 | 99.90 |

Plans at or above the minority's efficiency gap: 55,169 of 1,010,000 on election-day votes; 11,903 on all ballots.

**The 2019 map's seats at 50/50 is not a midrank.** Its election-day value, 40/87, is shared by 266,278 plans (26.4%), but the ranking compares floats exactly and the CSV's 40/87 does not equal the map's in the last digit, so every tied plan counts as below. The 78.54 is therefore the share of plans at or below 40/87; counting the ties as half gives 65.36 (recomputed from the committed canonical chains; the academic report gives both). The majority's 41/89 cannot tie with any k/87, so its 78.54 is right. The 2019 map's all-ballots 74.08, at 41/87, equals the majority's and may carry the same error; it cannot be checked here, because the all-ballots chains are not committed.

**Not shown as a headline: UCP seat percentiles for the 89-district maps.** The canonical ensemble has 87 districts, so a seat count from an 89-district map is partly a district-count effect. For the record (`canonical_ranking.json`): 2019 map 57 → 49 seats (p85.71 → p59.98, a like-for-like count); majority 55 → 48; minority 60 → 55. Ensemble median 55 → 49 of 87.

## Results: the panel's map against set D

Source: `setD_panel_all_ballots.json` (all ballots) and `../a10_stepc/size_matched.json` (election-day, Step C). Only set D is used: `size_matched_results.py` also reads the repo's set A chains, which are election-day, so those entries were removed from the saved file.

| Measure | Election-day value | Percentile | All-ballots value | Percentile |
|---|---:|---:|---:|---:|
| Efficiency gap | +1.45% | 47.87 | −1.66% | 48.02 |
| Mean-median | −2.53% | 17.00 | −1.09% | 77.41 |
| Declination | +0.004 | 52.41 | −0.060 | 47.57 |
| Seats at 50/50 | 0.484 | 91.63 | 0.495 | 89.90 |
| UCP seats (of 91) | 58 | 42.68 | 51 | 42.85 |
| Competitive seats, close4 (registered, flags at ≤ p5) | 11 | 75.19 | 10 | 34.38 |
| Towns split (registered, flags at ≥ p95) | 1 | 0.00 | 1 | 0.00 |
| City vs rest gap (registered, flags at ≥ p95) | +4.27% | 59.17 | +4.27% | 59.17 |

No registered size-matched flag fires on either set of votes. Every set D measure except population MAD remains *provisional* under Amendment 5, Part 16 (the lag cap binds), as in Step C. 51 UCP seats matches the seat-claim test's substrate D.

## Reading

- **Matched ranking changes the C51 reading for the minority.** C51 withdrew the claim that the minority's efficiency gap "would be flagged" on a fuller substrate, because +2.55% sits below the 4.10% and 5% lines. Those lines were calibrated on election-day votes, so that comparison crossed substrates as well. Against plans scored on the same ballots, the minority's efficiency gap is p98.82 (election-day p94.54) and its declination p99.82 (p98.79). Mean-median and seats at 50/50 stay above p98.
- **The withdrawal stands as written** for the level threshold. Its "levels fall" framing should not be read alone: the minority's efficiency gap and declination rankings get stronger on matched data, not weaker.
- **The majority and the 2019 map move toward the middle** on efficiency gap and declination. The majority's mean-median stays near p1.
- **The panel's map stays near set D's median** on efficiency gap, declination and seats. Its mean-median moves most (p17 → p77) and its competitive-seat count moves from above to below the median.
- **These matched percentiles replace the `ptile_full` columns** in `data/outputs/attribution_sensitivity_check_all_ballots.json`, which rank all-ballots values against the election-day ensemble (for example, minority efficiency gap 72.76).
