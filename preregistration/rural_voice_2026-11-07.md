# Plan: rural voters in mixed city-and-rural divisions (2026-11-07)

**Unregistered. Written before computing.** Not blind: the panel's Lethbridge split, and the votes in those divisions, are already known.

**Question.** Every test so far asks whether city voters are cracked. This plan asks the reverse: when a city is spread into rural divisions, do rural communities end up as a minority inside a division whose result the city part decides? The panel's minority raised this ("residents ... have consciously chosen not to live in Calgary", p.146).

**Definitions, fixed now:**
- **Rural:** a voting area whose representative point is outside every 2021 CSD of type city (CY) or town (T). That includes villages, summer villages, municipal districts and counties, improvement districts, special areas, reserves and Métis settlements.
- **Urban:** in a city or town CSD.
- **Mixed division:** a division with between 5% and 95% of its 2021 population rural.
- **Votes:** all 2023 ballots (the primary substrate, `va_polygons_all_2023_ballots_primary.gpkg`), UCP and NDP only. Election-day figures are computed and reported beside.
- **Rural preference overridden:** a mixed division where the rural part's two-party leader differs from the whole division's leader.

**Measures, for the majority, minority and panel (reconstruction v3) maps:**
1. **Rural share:** for each division, the rural share of 2021 population. Also the number of rural residents living in divisions where they are under 50% of the population (rural residents in urban-majority divisions).
2. **Rural preference overridden:** the rural residents and rural voters in divisions where the rural part's leader differs from the division's leader.
3. **Municipal splits of rural municipalities:** for each municipal district or county, the number of divisions holding at least 5% of its population.
4. **Focus areas:**
   - the Lethbridge area: the divisions holding any of Lethbridge city or Lethbridge County;
   - the Springbank area: the divisions holding Rocky View County west of Calgary.

   Each is reported division by division, majority map against panel map.

**Neutral comparison.** It can be done only if the region chains can be rerun with these measures added. `findings/hybrid_regions/regional_redraw.py` stores no plan assignments, so its committed chains cannot be rescored. If the measures show a change of 5,000 or more rural residents moving into urban-majority divisions in a focus area, rerun that region's redraws (city-blind and municipality-aware, the same seeds and settings) with measures 1–2 recorded. Report the panel's rank among them. The rerun waits until memory is free after the Amendment 12 replays.

**Reading rules:**
- A rural minority inside a mixed division is a design choice the Act permits. The question is how many people it affects, how that compares with the commission majority's map, and how it compares with the neutral redraws if they are run.
- "Overridden" describes a 2023 vote count. It is not a statement about representation quality.
- Nothing here says whether any map is a gerrymander.

**Outputs:** `findings/rural_voice/` (script, JSON, README).
