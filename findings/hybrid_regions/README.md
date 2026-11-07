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
