# Population basis: 2021 census against the 2024 estimates the maps were drawn on (2026-11-07)

**Unregistered.** The plan, with its decision rule (`preregistration/population_basis_2026-11-07.md`, commit `c01cbdcd`), was committed with the results, five minutes before them; that it was written first rests on the author's statement. Nothing here says whether any map is a gerrymander.

## Result: the basis matters, and it matters most for the city-versus-rest test

**Seat entitlement moved between 2021 and 2024.** Each voting area's 2021 population is scaled by its municipality's growth in the province's 2021-to-2024 estimates; 99.8% of people get their own municipality's factor. The total is set to the panel's 4,888,723.

| Region | Seats on 2021 census | Seats on 2024 estimates | Shift |
|---|---:|---:|---:|
| Calgary | 27.89 | 29.20 | **+1.31** |
| Edmonton | 21.59 | 22.21 | **+0.63** |
| Calgary ring (Airdrie, Chestermere, Cochrane, Okotoks, Rocky View, Foothills) | 4.88 | 4.97 | +0.09 |
| Edmonton ring | 8.10 | 7.69 | −0.41 |
| Other cities of 20,000+ | 6.95 | 6.73 | −0.23 |
| Everything else | 21.60 | 20.20 | **−1.40** |

Calgary and Edmonton together go from 49.5 seats' worth of people to 51.4. **Under the plan's rule (a shift of 0.5 seats or more), the 2021 basis is a limit on every comparison involving Calgary, Edmonton or the rural remainder.**

**What the real maps did.** All three maps (majority, minority, panel), and the ¶167 map, have 49 divisions that are at least half Calgary or Edmonton. Set D's neutral maps, balanced on 2021, have a median of 49 (5th to 95th percentile 47 to 51). So on the 2021 basis the real maps look ordinary on city seat count. On the 2024 figures the maps were actually drawn on, the two cities hold about 51.4 seats' worth of people in 49 city divisions.

**Measure 4** (each region's entitlement shift against the gap between the panel's seat count there and set D's median) cannot be computed from committed outputs. Set D's chains record only the combined count of divisions at least half Calgary or Edmonton (`n_city_districts`), not seat counts by region. The combined count above is the nearest measure they hold.

**The city-versus-rest gap on each basis** (mean population of city divisions against the rest; the definition the size-matched test uses):

| Map | On 2021 census (what the test scores) | On the map's own published 2024 figures |
|---|---:|---:|
| Commission majority | −0.7% | +9.2% |
| Commission minority | +5.4% | +15.1% |
| Panel (reconstruction v3) | +4.3% | +13.4% |

The registered size-matched test scores each map on 2021 population against neutral maps balanced on 2021. Because the cities grew faster, a map balanced on 2024 figures shows a smaller city gap on 2021 figures than it really has. Every map's gap is about 9 to 10 points larger on its own figures. The neutral maps were never drawn on 2024 figures, so how they would score on that basis is not known from the existing chains. **The size-matched city-versus-rest percentiles (for example the panel's p59.2 in set D) should be read as measured on a basis the maps were not drawn on.**

## Validation, and what it limits

Against each map's published division totals, the growth basis misses by 6.6% to 6.7% on average (largest 36%, Calgary-North East). The 2021 census, scaled to the same total, misses by 7.8% to 8.1%. A single growth rate per municipality cannot say where in a city people were added, which is why the small-area rebuild failed (`findings/osi_rebuild/`). So:
- The regional figures above are reliable. They depend on whole-municipality totals, which come straight from the estimates.
- Division-level figures on the growth basis are not reliable. For the real maps' own figures, use their published totals, as the second table does.

On the growth basis the real maps' population spread is wider than on either other basis (panel MAD 6,350, against 5,125 on 2021 and 4,214 published). That comes from this within-city error, not from the maps.

## What follows (per the plan's decision rule)

**Proposed here, run on 2026-11-12 (next section):** a rerun of set D (91 districts, s.15(2), same seeds) on the growth basis, with the city-versus-rest test and seat counts recomputed. The registered chain script reads `pop_2021` from the graph, so this needs a copy of it with a population override. The registered script itself is not edited.

Before that rerun, these limits applied:
- Comparisons involving the big cities carry this limit.
- Seat measures in the neutral maps give Calgary and Edmonton about two seats fewer than 2024 figures would.
- The cities lean NDP in 2023, so the 2021 basis likely moves the neutral maps' NDP seat counts down. Then any real map's NDP seat count looks better against them than it would against neutral maps drawn on 2024 figures.

That direction is an inference from the entitlement shift, not a measured result. The rerun below measures it.

Files: `population_basis.py`, `population_basis.json`, `city_counts.py`, `city_counts.json`.

## Set D rerun on the 2024 growth basis (2026-11-12)

**Unregistered sensitivity analysis, provisional.** This runs the rerun the plan proposed (`preregistration/population_basis_2026-11-07.md`, commit `c01cbdcd`). The registered size-matched result is unchanged: on the 2021 basis the panel's city-versus-rest gap is at p59.2 in set D, and this summary reproduces it (p59.17). Nothing here says whether any map is a gerrymander. The city-versus-rest gap measures how population is split between city divisions and the rest. It is not a partisan measure, and it does not say why a line was drawn.

**What ran.**
- **Script.** `close_seats_ensemble_growth.py` is a copy of `alberta_audit` `analysis/scripts/close_seats_ensemble.py` (commit `2994113c`; the file is unchanged since `ee7eb5ce`, before the all-ballots set D run). The registered script is not edited. The copy makes three changes, listed in its header:
  1. Its repository root is pinned to the `alberta_audit` clone, so it runs on that clone's harness.
  2. `--pop-file growth_nodes.csv` replaces `pop_2021` on every graph node, and on the voting-area table, right after each `build_va_graph` call. First it checks that the file's `pop_2021` equals the graph's. So the seed plan, ReCom, the s.15(2) ideal and town totals, the city gap, town splits and `population_mad` all run on the growth basis.
  3. A read-only record of districts per region is added. It makes no random draw.
- **Override file.** `growth_nodes.csv` (SHA-256 `205b653c0ca66f8cdf7a8467c348d3d5e6cb849600cc1626a525f825431c7908`, written by `growth_nodes.py`) uses `population_basis.py`'s formula exactly. It reproduces `population_basis.json`'s regional entitlements to within 0.001 seats. That hash is in every checkpoint.
- **Faithfulness check.** With no `--pop-file`, the copy's first 500 rows of chain 251 equal the original all-ballots chain 251, on every column.
- **Command.** For each chain: `nk --k 91 --idx N --steps 252500 --chunk 500 --s152 data/outputs/s15_2_va_criteria.csv --va-file <all-ballots primary gpkg> --pop-file growth_nodes.csv`. The criteria table's SHA-256 is `48c928b8…`, as in the original checkpoints. Seeds are `chain_seed(idx)`, the same function and indices as the original.
- **Same seeds, different plans.** The population differs, so these are not the same plans as the 2021 set. A plan-for-plan replay is not possible.
- **Votes.** All 2023 ballots, as in the set D directory `population_basis.py` reads. The plan names no vote basis. The city gap and city-division counts do not depend on votes. Election-day seat counts were not recorded.
- **Runtime.** About 40 to 45 minutes per chain (2,381 to 2,699 s), with 4 to 6 processes running at once. The chains ran from 05:40 to 06:51 Alberta time.

**Two chains did not seed, and were retired (Amendment 11, Part 3, following Amendment 5, Part 14's index 250).**
- **Index 252.** `recursive_tree_part` found no cut after 50,000 attempts while building the starting plan (05:42). The log is in `setd_growth_logs/chain252_seed_failure.log`.
- **Index 255,** the next unused index, failed the same way (06:10). Its log is `setd_growth_logs/chain255_seed_failure.log`.
- **Index 256** seeded and took the place. Neither failed chain was rerun with another seed or setting.
- So the growth set is 251, 253, 254 and 256, against the 2021 set's 251–254. On the growth basis 2 of 6 indices tried did not seed.
- **When the set was fixed.** It was fixed when 256 was launched (06:11), before any plan was compared with the panel (about 06:28). Before that, one row of chain 251 was read, at about 05:41, only to confirm the override was on.
- **Both ways are reported.** Results are given for the four chains pooled, and for the three indices the two sets share (251, 253, 254). They agree.

| Chain | Seed | Rows | SHA-256 (not committed; in `alberta_audit/data/simulation_checkpoints_k91_s152a23_allballots_growth/`) |
|---|---:|---:|---|
| 251 | 2041389144 | 252,500 | `65051f1f1cb89840b35bfbdf156b674fcda7adeb8bd888832c1e418d29cbba32` |
| 253 | 2041391144 | 252,500 | `717a5df9dd14fcfb09ec4f6298fcd1a33f6b648d555da8514aa17826935e045d` |
| 254 | 2041392144 | 252,500 | `9afc89d443737ef8bb712579d4f86f57f683ba06e4129db9d9079ebefe055793` |
| 256 | 2041394144 | 252,500 | `c87a3be805c3b9b872dd947286838e3c41335eb2aefc9bd4a4948b990076247a` |

### City-versus-rest gap (the size-matched test's measure)

The registered size-matched flag is at or above the set's 95th percentile. Percentiles are midrank. The real maps are scored on the same basis as the neutral maps. On the growth basis the panel's value uses the same voting-area growth population. Its published App. 7 figures are shown beside, and the two agree.

| Basis of the neutral maps and the score | Plans | Neutral 5th / median / 95th | Panel | ¶167 |
|---|---:|---|---|---|
| 2021 census (registered; chains 251–254) | 1,010,000 | −1.7% / +3.5% / +8.6% | +4.27% (p59.2) | +3.46% (p49.3) |
| Growth basis (chains 251, 253, 254, 256) | 1,010,000 | −2.6% / +3.1% / +9.0% | +13.61% (**p99.76**); published figures +13.40% (p99.71) | +12.72% (p99.53) |
| Growth basis, shared indices 251, 253, 254 only | 757,500 | −2.8% / +3.0% / +9.0% | +13.61% (p99.71) | +12.72% (p99.44) |

- **On the basis the map was drawn on,** the panel's city-versus-rest gap is beyond the size-matched 95th-percentile line. Its city divisions average about 13.6% more people than the rest. Neutral maps balanced on the same figures give a median of about 3%.
- **Every chain agrees.** The panel's percentile is p99.54, p99.95, p99.65 and p99.89 in chains 251, 253, 254 and 256. Each chain's own 95th percentile is between 7.6% and 10.0%.
- **¶167** is beyond the line too (p99.53).
- **The 89-district maps** (commission majority and minority) are not placed against this 91-district set, as in existing practice. On the growth basis their gaps are +8.3% and +15.0%.
- **Status: provisional.** On the growth chains, n_eff for this measure is 462, but the registered estimator's lag cap binds (on at least one chain), so 462 is an upper bound. The uncapped diagnostic gives 213. On the 2021 set the figures are 523 with the cap binding, and 281 uncapped. Under Amendment 5, Part 16 the result is provisional. The repository already notes that this measure's n_eff is too low to place a 95th percentile firmly (`../size_matched_results_2026-10-30.md`). The chains also differ: chain 253's growth median is +1.4%, the others +3.5% to +3.6%. The panel's percentile is above p99.5 in each chain, so its position does not hinge on any one chain.
- **This plan sets no decision rule for the rerun.** The flag rule above is the registered size-matched rule, applied here as a sensitivity reading. It does not replace the registered result.

### Seat counts

| Measure | Neutral on 2021: 5th / median / 95th | Panel on 2021 | Neutral on growth: 5th / median / 95th | Panel on growth |
|---|---|---|---|---|
| Districts at least half Calgary or Edmonton | 47 / 49 / 51 | 49 (p42.5) | 49 / 51 / 53 | 49 (**p4.3**) |
| Of those, Calgary | not recorded | 28 | 28 / 29 / 31 | 28 (p13.2) |
| Of those, Edmonton | not recorded | 21 | 21 / 22 / 24 | 21 (p14.9) |
| UCP seats, all 2023 ballots | 49 / 51 / 54 | 51 (p42.9) | 47 / 50 / 53 | 51 (p68.8) |

- **City divisions.** Neutral maps balanced on the growth figures give Calgary and Edmonton a median of 51 divisions. The panel's 49 is at p4.3. On the 2021 basis the median was 49 and the panel's 49 was ordinary (p42.5). The shift of two is the size the entitlement figures above predicted (49.5 → 51.4 seats' worth of people). These are counts with many ties, so the percentile moves in steps.
- **UCP seats.** The neutral median falls from 51 to 50. The inference above is borne out in direction: on the 2021 basis the neutral maps had about one more UCP seat at the median. The panel's 51 moves from p42.9 to p68.8. That is inside the band on both bases.
- **Calgary and Edmonton separately** were not recorded in the 2021 set D chains, so only the growth side has them.

**Plan measure 4, now computable on the growth side.** Districts are counted by plurality region (the region holding most of a district's population). These counts exist only for the growth chains; the 2021 chains recorded only the combined city count.

| Region | Entitlement shift, 2021 → 2024 (seats) | Panel | Neutral median on growth | Panel minus median | Panel's percentile |
|---|---:|---:|---:|---:|---|
| Calgary | +1.31 | 28 | 29 | −1 | p10.9 |
| Edmonton | +0.63 | 21 | 22 | −1 | p12.7 |
| Calgary ring | +0.09 | 5 | 5 | 0 | p65.8 |
| Edmonton ring | −0.41 | 8 | 7 | +1 | p69.6 |
| Other cities 20,000+ | −0.23 | 6 | 7 | −1 | p18.4 |
| Everything else | −1.40 | 23 | 21 | +2 | p96.3 |

- **Direction.** Calgary and Edmonton, which grew the most, each have one division fewer on the panel's map than the growth-basis median. The rural remainder ("everything else"), which grew the least, has two more.
- **How far to read this.** Six regions are too few for a correlation, so none is reported. The plan's measure 4 also compared against the 2021 set D median, which cannot be done because those chains have no per-region counts.

**Deviations from the plan, and choices it left open.**
1. **Retired indices.** 252 and 255 did not seed. They were retired and replaced by 256 under Amendment 11, Part 3.
2. **Vote basis.** The plan names none. All ballots was used, matching the set D directory `population_basis.py` reads.
3. **Real-map scoring.** On the growth basis the real maps were scored on the same voting-area growth population as the neutral maps, with the published figures beside. The two give the same reading (p99.76 and p99.71).
4. **Read-only region counts** were added to the copy, for measure 4.
5. **Town splits.** The growth basis is scaled to the panel's 4,888,723. The copy's town-split measure uses absolute size limits (20,000 to 150,000), so on this basis it tracks 13 towns instead of 12. That measure is not part of this rerun's reading.

**Limits.**
- **Within-city growth.** The growth basis gives every part of a municipality the same growth factor. Its division-level error is 6.6% on average (validation above). The city-versus-rest gap and the city-division counts are aggregates over about 50 divisions, and the panel's growth-basis and published gaps agree to 0.2 points.
- **Provisional n_eff,** as above.
- **Outside the ledger's correction.** These percentiles are not in `../test_ledger/ledger.py`'s multiple-testing family, so its "none survives correction" reading does not cover them.

Files: `close_seats_ensemble_growth.py` (the copy), `growth_nodes.py`, `growth_nodes.csv`, `growth_nodes.json` (override and real maps on both bases), `setd_growth_summary.py`, `setd_growth.json`, `setd_growth_logs/` (the two seed failures).
