# Neutral regional redraws where the panel's map has hybrid ridings (2026-11-07)

**Unregistered, provisional, not blind.** Plan committed before any chain (`preregistration/hybrid_regions_2026-11-07.md`, commit `d2c1353e`). All ballots are the primary figures. The panel's map is the v3 reconstruction. These measures describe where a city's NDP voters land. They do not show why a line was drawn, and nothing here says whether any map is a gerrymander.

Each region was redrawn many times, holding every other division fixed, in two ways:
- **City-blind:** population and contiguity only.
- **City-aware:** ReCom's municipal surcharge at weight 0.5 (the audit's set C setting), so lines prefer municipal boundaries.

For each region the panel's actual configuration is placed against those neutral redraws as percentiles. The plan's rule: a configuration is unusual if the share of the city's NDP votes in seats the NDP loses by 10 points or more lies beyond the neutral 95th percentile, or below the 5th.

## Result

| Region | City-blind: NDP votes in lopsided losses (percentile) | City-aware: same | City-aware: number of pieces (percentile) | Unusual by the plan's rule |
|---|---|---|---|---|
| **Lethbridge** | 45% (p71) | 45% (**p93**) | 4 (**p99.5**) | no, on either variant |
| **St. Albert** | 15% (**p97**) | 15% (p92) | 2 (p47) | city-blind only |
| Calgary (Springbank) | 13% (p45) | 13% (p59) | 6 (p37) | no |
| Edmonton (Enoch, Nisku) | 0% (p12) | 0% (p37) | 9 (p50) | no |
| Leduc and Beaumont | 100% (p87) | 100% (p58) | 1 (p14) | no |
| Airdrie, Chestermere, Fort Saskatchewan, Grande Prairie, Medicine Hat, Spruce Grove | 100% (p50-72) | 100% (p50-60) | ordinary | no |

In the last row, all six cities' NDP voters are in seats the NDP loses badly on every neutral plan too, because the NDP does not win any seat in those regions. The test has nothing to detect there.

**Lethbridge, the case the critics name.**
- **Pieces:** the city-aware redraws split Lethbridge two ways in 51% of plans and three ways in 48%. Four ways happens in 0.9%, and the panel's map does it.
- **Seats:** city-aware plans give the NDP a median of 2 seats in the region; the panel's map gives 1 (p21).
- **Votes in lopsided losses:** neutral city-aware plans put a median of 1.5% of the city's NDP votes in seats lost by 10 or more points, against 45% on the panel's map. That is p93, just inside the plan's 95% line. **By the rule fixed in advance, the configuration is not unusual.**
- **Why the rule gives a different answer from the piece count:** the rule measures where the votes land, not how many pieces there are. Its city-aware distribution has a long tail (95th percentile 49%). The four chains agree (medians 1.2% to 2.1%).
- **Against the city-blind redraws** (signal F) the same configuration is at p71. Neutral maps that ignore city boundaries split Lethbridge routinely, so the result depends on whether the benchmark respects municipalities. The Act's s.14(b) asks the drawer to consider municipalities, which is the case for treating the city-aware benchmark as the closer one.

**St. Albert.**
- **The rule:** it fires on the city-blind redraws (p97) but not the city-aware ones (p92).
- **Inherited, not added:** the panel's St. Albert arrangement matches the commission majority's. Both put about 23% of the city in a mostly rural division (Morinville-Sturgeon on the panel's map, St. Albert-Sturgeon on the majority's; `../six_signals/README.md`, signal C).
- **Who owns the pattern:** it belongs to both maps, not to the panel's changes.

**The commission majority's configuration** could not be compared in any region, because its divisions never cover exactly a region's voting areas.

## Limits
- Regions are local: holding the rest of the map fixed means effects elsewhere are not seen.
- The weight 0.5 is one setting. A stronger preference for municipal lines would make Lethbridge's four-way split rarer still.
- The reconstruction's lines are traced. Rerun on the official shapefile.

Files: `regions.json`, `summary.json`, `chains/` (per chain CSV and JSON with drand salts), `regional_redraw.py`.

## Chikina-Frieze-Pegden local test for Lethbridge (2026-11-07)

Plan committed before any walk (`preregistration/cfp_lethbridge_2026-11-07.md`, commit `f9bb45da`). The chain:
- **Moves:** a reversible single-area flip chain, uniform over (area, touching district) pairs with Metropolis-Hastings acceptance min(1, B/B'). It is written out in full, not taken from gerrychain, because gerrychain's flip proposal is not exactly reversible when an area touches a district along several edges.
- **Walks:** four walks of 1,000,000 steps from the panel's southern configuration, with drand salts `cfp_lethbridge_1` to `_4`.
- **Adjacency:** queen, so corner-touching areas count as neighbours.
- **Population:** within ±25% of the region mean, on 2021 population.
- **Pinned:** six voting areas that cannot reach the region are held in their district.

**Deviation from the plan, made after a 20,000-step smoke test and before any of the four walks:** even under queen adjacency, two of the panel's districts are not contiguous on the reconstruction. Lethbridge-Little Bow is in 3 pieces and Banff-Canmore-Diamond Valley in 2, because their lines cut voting areas that are placed by representative point. So the state space allows each district no more pieces than it has in the panel's plan. That is a property of the state, so the chain stays reversible.

| Walk | Moves accepted | Areas reassigned by the end | V1: Lethbridge NDP votes in lopsided losses (start 44.7%), walk 5th / median / 95th | ε | p = √(2ε) | V2: pieces (start 4), walk 5th / median / 95th | ε | p |
|---|---|---|---|---|---|---|---|---|
| 1 | 449,162 | 60% | 28% / 62% / 74% | 0.908 | 1.0 | 4 / 4 / 4 | 1.00 | 1.0 |
| 2 | 451,973 | 58% | 28% / 63% / 100% | 0.880 | 1.0 | 4 / 4 / 4 | 0.99 | 1.0 |
| 3 | 430,263 | 55% | 20% / 32% / 65% | 0.397 | 0.89 | 3 / 4 / 4 | 0.93 | 1.0 |
| 4 | 440,916 | 73% | 21% / 52% / 100% | 0.505 | 1.0 | 4 / 4 / 5 | 0.99 | 1.0 |

**Result: the panel's southern configuration is not a local outlier**, on either value, on any walk (every p at least 0.89, against the plan's 0.025). Small changes to the plan crack Lethbridge as much or more as often as they crack it less: on three of the four walks the median is above the panel's 44.7%.

**Limits:**
- **Weak test of the split:** single-area flips rarely change how many districts hold 2% of a city, so V2 has little power here.
- **Local only:** by Cho and Rubinstein-Salzedo (2019), this is a local test. It says nothing about how the configuration compares with all neutral maps; that is what the ensemble percentiles above measure.

Files: `cfp_lethbridge.py`, `cfp_lethbridge.json`, `cfp/walkN.json`. The per-step values, `cfp/walkN.npy` at 8 MB each, are not committed.

## Which comparison set: why more than one is reported (2026-11-07)

There is no single right comparison set for a map. Each neutral ensemble is a sample from one chosen distribution, not "all neutral maps": the algorithm, the population band, contiguity, the s.15(2) rules and whether municipal lines are preferred all shape it. Herschlag et al. (2020) compare a plan with ensembles "satisfying all legal criteria", so an ensemble is only as valid a comparison as the criteria built into it.

"Neutral" means drawn without partisan data. It does not mean lawful, or what a commission is supposed to do. The Act tells drawers to weigh communities of interest, municipalities, geography, transportation and clear boundaries (s.14), and *Carter* allows departures from parity for such reasons. The ensembles here encode population and contiguity, and in the city-aware runs, municipalities and s.15(2), but not the rest. So:
- **What a difference can mean:** a difference from a neutral ensemble can come from legitimate factors the ensemble leaves out, not from partisanship. A partisan choice can also hide behind such a factor.
- **What the ensemble answers:** what maps look like when only the encoded rules matter. That is useful for separating the effects of geography (where voters live) from line-drawing choices.
- **The local test** answers a narrower question again: is this map extreme compared with small changes to itself? By Cho and Rubinstein-Salzedo (2019), a map can pass one test and fail the other.

For that reason this audit reports several comparison sets and reads across them:
1. **Neutral ensembles with different encoded rules:** city-blind and city-aware here; sets A to D province-wide. A result that holds across all of them is robust. One that flips between them depends on the rule that differs, and is reported that way.
2. **Human-drawn reference maps:** the 2026 commission majority and minority, ¶167, and earlier commission maps. They are not neutral, but they show what drawers working under the same law actually produced.
3. **The local test**, from the map itself.
4. **The panel's stated reasons**, checked for consistent application. This is the closest to the legal question, and it is not statistical.

**Lethbridge on this reading.** Splitting the city four ways is ordinary if municipal boundaries carry no weight. It is rare if they carry the weight Alberta's commissions have given them, and it is not a local outlier. How much weight the Act requires is a legal judgment. `../city_weight/` estimates how much weight past commissions have actually applied.
