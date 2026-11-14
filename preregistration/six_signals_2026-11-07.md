# Six further signals (written before any computation)

> Written 2026-11-07, about 6:00 AM Alberta Time (UTC−6), before any figure below has been computed. Unregistered and not blind: the author knows the 2023 results on these maps and the Lethbridge and Banff findings. Requested by the author on 2026-11-07 ("do 1-6"). GitHub only; no OSF filing. Nothing here is a finding on whether any map is a gerrymander.

**Maps:** majority and minority (official), panel (v3) and ¶167. Voting areas are placed by representative point.

## A. Other elections and vote swings (signal 2)

- **Elections:** 2015 and 2019, election-day ballots by voting area (`va_polygons_with_{2015,2019}_votes.gpkg`). 2015's UCP figure is PC plus Wildrose, the parties that merged into the UCP. Only two-party shares are used.
- **What is reported:** seats on each map in each year; the Lethbridge, Banff-area and south-group outcomes; and the efficiency gap.
- **Swing curve:** a uniform two-party swing on 2023 all ballots, from NDP −10 to +10 points in 0.5-point steps. Reported: NDP seats on each map, the panel-minus-¶167 seat difference at each step, and which seats cause it.
- **Reading:** an effect counts as robust if the panel-minus-¶167 difference has the same sign in 2015, 2019 and 2023, and over most of the swing range. Otherwise it is reported as specific to one election.

## B. First Nations reserves and Métis settlements split (signal 6)

- **What is counted:** 2021 census subdivisions of type IRI (Indian reserve) or S-É (Métis settlement) that are divided between two or more divisions. A reserve counts as split if a second division holds at least 1% of its land area.
- **What is reported:** the count, the names, and the population in split reserves, on each map.

## C. How cities are treated (signal 4)

- **Which cities:** every city (CSD type CY) of 20,000 or more.
- **What is reported:**
  - The number of divisions holding at least 2% of its 2021 population.
  - The number its population justifies (ceiling of population / (1.25 × average)).
  - The share of its population in divisions where it is under half the division.
- **Reading:** this shows whether the panel treats cities alike. The panel's stated reasons for the cities that differ are quoted beside the table, with page numbers, and nothing is said about why.

## D. Incumbents, coarse (signal 3)

- **Who:** the member elected in each 2019-boundary division at the 2023 election or a later by-election (`data/reference/alberta_2023_results.csv`, `alberta_byelections_2019_2026.csv`). Party is the party they were elected under; later floor-crossings are not tracked.
- **Where they go:** each member is placed in the new division that holds the largest share of their old division's 2021 population. Home addresses are not used.
- **What is reported:**
  - Pairings: two members placed in the same new division.
  - Members whose new division the other party carried on 2023 all ballots.
  - Counts by party and map.
- **Limit:** this is a proxy only. Where a member lives decides where they can run, and that is not known here.

## E. Growth over the life of the map (signal 5)

- **The method:** each division's stated 2024 population is grown to 2031 at the 2021-2025 annual growth rate of its municipalities. That uses the public municipal estimates (`data/osi/`), weighted by 2021 census population, with dissemination areas placed by representative point.
- **What it is:** a trend extrapolation, not a projection, and it is labelled that way.
- **Status:** the ¶167 map has no stated populations, so it is not scored.
- **What is reported:**
  - Divisions beyond ±25% in 2031.
  - The spread.
  - The correlation, across divisions, between growth and 2023 NDP two-party share.

## F. A neutral redraw of the south only (signal 1)

- **Which region:** the voting areas of the panel's southern group (8 divisions; `findings/iap_para167/comparison.json`). Every other division is held fixed.
- **The chain:** ReCom on that region's voting-area graph.
  - Starting plan and population: the panel's assignment, on 2021 overlay population.
  - Population band: ±25% of the region's mean district population, widened if needed to admit the starting plan, with the width reported.
  - Size: 4 chains × 50,000 steps. Seeds come from drand: SHA-256 of salt + canonical randomness, salt `regional_south_<chain>` (`analysis/scripts/drand_seed.py`).
- **Recorded for every plan:**
  - NDP seats in the region.
  - Where Lethbridge's NDP votes land: won, lost by under 10, lost by more.
  - The number of districts holding at least 2% of Lethbridge.
  - The region's sorted NDP shares.
- **Ballots:** both sets.
- **What is reported:** the panel's and ¶167's group configurations against that distribution, as percentiles.
- **Reading:** a configuration counts as unusual for this region only if it lies beyond the 95th percentile, or below the 5th, of neutral regional plans on the share of Lethbridge's NDP votes in seats lost by 10 or more points.
- **Limit:** this is a local check. It holds the rest of the map fixed, so it cannot speak to effects elsewhere.

**Signed:** Claude (acting as session agent), directed by Will Conner
