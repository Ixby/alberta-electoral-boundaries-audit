# Population basis: 2021 census against the 2024 estimates the maps were drawn on (2026-11-07)

**Unregistered.** The plan, with its decision rule, was committed before computing (`preregistration/population_basis_2026-11-07.md`, commit `c01cbdcd`). Nothing here says whether any map is a gerrymander.

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

**The city-versus-rest gap on each basis** (mean population of city divisions against the rest; the definition the size-matched test uses):

| Map | On 2021 census (what the test scores) | On the map's own published 2024 figures |
|---|---:|---:|
| Commission majority | −0.7% | +9.2% |
| Commission minority | +5.4% | +15.1% |
| Panel (reconstruction v3) | +4.3% | +13.4% |

The registered size-matched test scores each map on 2021 population against neutral maps balanced on 2021. Because the cities grew faster, a map balanced on 2024 figures shows a smaller city gap on 2021 figures than it really has. Every map's gap is about 9 to 10 points larger on its own figures. The neutral maps were never drawn on 2024 figures, so how they would score on that basis is not known from the existing chains. **The size-matched city-versus-rest percentiles (for example the panel's p59.2 in set D) should be read as measured on a basis the maps were not drawn on.**

## Validation, and what it limits

Against each map's published division totals, the growth basis misses by 6.6% to 6.7% on average (largest 36%, Calgary-North East). The 2021 census, scaled to the same total, misses by 7.8%. A single growth rate per municipality cannot say where in a city people were added, which is why the small-area rebuild failed (`findings/osi_rebuild/`). So:
- The regional figures above are reliable. They depend on whole-municipality totals, which come straight from the estimates.
- Division-level figures on the growth basis are not reliable. For the real maps' own figures, use their published totals, as the second table does.

On the growth basis the real maps' population spread is wider than on either other basis (panel MAD 6,350, against 5,125 on 2021 and 4,214 published). That comes from this within-city error, not from the maps.

## What follows (per the plan's decision rule)

**Proposed, not launched:** a rerun of set D (91 districts, s.15(2), same seeds) on the growth basis, with the city-versus-rest test and seat counts recomputed. The registered chain script reads `pop_2021` from the graph, so this needs a copy of it with a population override. The registered script itself is not edited. Memory is committed to the Amendment 12 replays until they finish.

Until then:
- Comparisons involving the big cities carry this limit.
- Seat measures in the neutral maps give Calgary and Edmonton about two seats fewer than 2024 figures would.
- The cities lean NDP in 2023, so the 2021 basis likely moves the neutral maps' NDP seat counts down. Then any real map's NDP seat count looks better against them than it would against neutral maps drawn on 2024 figures.

That direction is an inference from the entitlement shift, not a measured result.

Files: `population_basis.py`, `population_basis.json`, `city_counts.py`, `city_counts.json`.
