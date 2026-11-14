# Rural voters in mixed city-and-rural divisions (2026-11-07)

**Unregistered and not blind.** The plan (`preregistration/rural_voice_2026-11-07.md`, commit `c01cbdcd`) was committed about seven minutes before the results; that it was written first rests on the author's statement. The panel's map is the v3 reconstruction (provisional until the official shapefile is posted). Population is the 2021 census on voting areas. Votes are all 2023 ballots, UCP and NDP only; election-day votes give the same divisions on every map. Nothing here says whether any map is a gerrymander, and "overridden" describes a 2023 vote count, not the quality of anyone's representation.

**Rural** means outside every city or town. That covers counties and municipal districts, villages, summer villages, reserves, Métis settlements, improvement districts and special areas. It is 19.7% of Alberta's 2021 population.

## Province-wide

| Map | Mixed divisions (5–95% rural) | Rural residents in urban-majority divisions | Mixed divisions where the rural part's 2023 leader lost | Rural residents there | Counties split 3+ ways |
|---|---:|---:|---|---:|---:|
| Commission majority (89) | 30 | 273,409 | Canmore-Banff, Edmonton-Enoch | 12,778 | 4 |
| Commission minority (89) | 38 | 410,324 | none | 0 | 8 |
| Panel, reconstruction v3 (91) | 35 | 287,160 | Edmonton-Enoch, Edmonton-Nisku | 10,689 | 8 |
| ¶167 (91) | 32 | 245,846 | Canmore-Banff, Edmonton-Enoch, Edmonton-Nisku | 17,705 | 5 |

Counties split three or more ways (each piece holding at least 5% of the county's people):
- **Majority:** Greenview, Lacombe, Parkland, Rocky View (4 pieces).
- **Panel:** Foothills, Greenview, Leduc, Lethbridge County, Parkland (4), Red Deer County, Rocky View (6), Wheatland.

## Lethbridge County

Lethbridge County has 14,576 rural residents in 2021.

| Map | Divisions holding Lethbridge city or county | Rural residents of the area in urban-majority divisions |
|---|---|---:|
| Majority | Lethbridge-East (0% rural), Lethbridge-West (0%), Livingstone-Macleod (67% rural) | **0** |
| Panel | Lethbridge (0%), Lethbridge-Cardston (44%), Lethbridge-Little Bow (34%), Lethbridge-Taber-Warner (61%) | **8,138** |
| Minority | four Lethbridge hybrids, 28–42% rural each | 14,576 |

In the panel's two urban-majority hybrids, the rural parts vote heavily UCP: 78% in Lethbridge-Cardston and 80% in Lethbridge-Little Bow, against 55–56% in their Lethbridge parts. Both parts lean the same way, so in 2023 no rural preference was overridden. But in those two divisions rural residents are now the minority of a division whose population is mostly city.

## Springbank (Rocky View County west of Calgary)

The area has 17,677 rural residents in 2021. On every map they sit in urban-majority or mixed divisions. The panel moves more of them into Calgary divisions: about 10,500 rural residents are in Calgary-Bow-Springbank (2,601; the division is 5% rural), Calgary-West-Springbank (7,629; 14% rural) and Calgary-North West-Bearspaw (293). On the majority's map the only Calgary division with rural residents here is Calgary-West-Elbow Valley (2,267); its Cochrane-Springbank is not a Calgary division. The Springbank parts of the panel's two Springbank divisions vote within about 2 points of the Calgary parts they join. Rocky View County as a whole goes from 4 pieces to 6.

## Reading

- **What the panel adds against the commission majority:** about 14,000 more rural residents province-wide in urban-majority divisions. In Lethbridge County the count goes from 0 to 8,138. Four more counties are split three or more ways.
- **How the minority compares:** its map goes further on every count (410,324 residents; all of Lethbridge County).
- **2023 votes:** one of the panel's changes overrides a rural preference by the plan's definition. Of its two "overridden" cases, Edmonton-Enoch is unchanged from the majority's map. Edmonton-Nisku is the panel's own change: it replaces the majority's Edmonton-Beaumont, which is not overridden, and holds about 7,000 of the 10,689 rural residents (Edmonton-Enoch's 3,656 is the majority's 12,778 less Canmore-Banff's 9,122).
- **The question the counts cannot answer:** whether a rural minority inside a city-majority division loses its voice. That is the minority report's concern and the panel's community-of-interest argument, and it is not testable with vote counts.

## Owed under the plan

The Lethbridge area crosses the plan's 5,000-resident trigger (8,138). So the south region's redraws are to be rerun, city-blind and municipality-aware, with the same seeds and settings as `findings/hybrid_regions/`, recording these rural measures. Then the panel's 8,138 is ranked among neutral redraws. **Run on 2026-11-12; see the next section.**

Files: `rural_voice.py`, `rural_voice.json`.

## The owed rerun: Lethbridge County's 8,138 among neutral redraws of the south (2026-11-12)

**Unregistered, not blind.** This runs the plan's "Neutral comparison" step (`preregistration/rural_voice_2026-11-07.md`, commit `c01cbdcd`). The panel's figure was known before the run. Votes are all 2023 ballots, with election-day beside, UCP and NDP only. Nothing here says whether any map is a gerrymander. A rural minority in a mixed division is a design choice the Act permits.

**What ran.** `lethbridge_rerun.py` replays the south region's neutral redraws (8 divisions, 462 voting areas, every other division held fixed). Each variant runs through its own generator's loop, copied line for line. The only addition is the plan's measures 1–2, recorded for every plan. Neither original script is edited.

| Variant | Generator | Seeds (drand salts) | Steps per chain | Plans kept |
|---|---|---|---|---:|
| City-blind | `../six_signals/regional_south.py` `run()` (the set `../hybrid_regions/` uses for Lethbridge city-blind) | `regional_south_1` to `_4` | 50,000, first 1,000 discarded | 4 × 49,000 |
| Municipality-aware (W = 0.5) | `../hybrid_regions/regional_redraw.py` `run("Lethbridge", "muni", c, 50000)` | `regional_Lethbridge_muni_1` to `_4` | 51,000, first 1,000 discarded | 4 × 50,000 |

- **Replay check.** Every chain also writes the original measure columns. All 396,000 rows equal the committed CSVs (`../six_signals/regional_south/chainN.csv`, `../hybrid_regions/chains/Lethbridge_muni_N.csv`). So these are the same plans, scored on more measures. Each seed was asserted against the committed chain JSON before stepping.
- **Panel self-check.** Scored through the same function on each setup, the panel gives 8,138, as `rural_voice.py` does. The region holds all 14,576 of Lethbridge County's rural residents.
- **Runtime.** The four municipality-aware chains ran in parallel, about 17 to 19 minutes each (05:35 to 05:54 Alberta time). The four city-blind chains ran in parallel, about 8 to 13 minutes each (05:53 to 06:08). Interpreter: `C:\Users\email\.venvs\audit-k91`, the one the original chains used.

**Measure: Lethbridge County rural residents in urban-majority divisions** (the panel's 8,138). Percentiles are midrank, as in `../hybrid_regions/`.

| Variant | Plans | 5th | Median | 95th | Plans with 0 | Plans at or above 8,138 | Panel's percentile | Per-chain percentiles |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| City-blind | 196,000 | 2,583 | 8,154 | 14,576 | 0.2% | 50.1% | **p49.9** | 49.3–50.5 |
| Municipality-aware | 200,000 | 0 | 1,333 | 14,576 | 46.4% | 28.8% | **p71.2** | 70.1–72.4 |

- **City-blind redraws:** the panel's 8,138 is the median. Redraws that ignore municipal lines put about as many county residents into city-majority divisions as the panel does.
- **Municipality-aware redraws:** nearly half of them (46%) put no county rural resident in an urban-majority division, and the median is 1,333. Still, 29% put 8,138 or more there. The distribution has two clumps: 65% of plans below 5,000, and 26% between 10,000 and 14,576 (all of the county).
- **The plan sets no threshold for this rank.** It asks only for the panel's rank.

**The plan's other measures, region-wide** (all 8 divisions; the panel's value, then its percentile):

| Measure | Panel | City-blind percentile (median) | Municipality-aware percentile (median) |
|---|---:|---|---|
| Rural residents in urban-majority divisions | 82,387 | p86.2 (59,021) | p97.5 (49,249) |
| Mixed divisions (5–95% rural) | 7 | p41.0 (7) | p84.1 (6) |
| Urban-majority mixed divisions | 5 | p66.3 (5) | p93.8 (3) |
| Rural preference overridden, all ballots: divisions / rural residents | 0 / 0 | p33.0 (66% of plans have none) | p43.1 (86% have none) |
| Same, election-day | 0 / 0 | p48.1 (96% have none) | p48.2 (96% have none) |

- **Region-wide rural residents in urban-majority divisions:** the panel's 82,387 is beyond 97.5% of the municipality-aware redraws (2.5% reach it) and beyond 86% of the city-blind ones. This count covers the whole south region, not only Lethbridge County. On the panel's map it is the rural residents of five divisions under 50% rural: Macleod-Crowsnest (24,684; 49.9% rural), Okotoks (16,668; 36%), Lethbridge-Cardston (15,688; 44%), Lethbridge-Little Bow (14,930; 34%) and Banff-Canmore-Diamond Valley (10,417; 28%). Macleod-Crowsnest sits on the 50% line, so a few hundred people either way would move about 25,000 residents in or out of this count. The measure is a hard threshold and should be read with that in mind.
- **No rural preference overridden:** in 2023 no mixed division in the panel's south had a rural part that voted differently from the whole division. That is also the most common outcome in the redraws.
- **The plan sets no flag rule for these measures.** They are reported as positions.

**Deviations from the plan.**
1. **"Same seeds and settings as `findings/hybrid_regions/`".** For Lethbridge, that set's city-blind variant was never run by `regional_redraw.py`. Its `summarize()` reads the six-signals F chains (`regional_south.py`). So the city-blind rerun replays those chains, with their seeds and their burn-in convention (1,000 discarded within 50,000 steps, so 49,000 kept rather than 50,000). Read literally, a city-blind run of `regional_redraw.py` would be a new chain set. It would not be the set the hybrid-regions table reports.
2. **Measure 1 per division.** The plan defines measure 1 per division for the real maps. For the redraws, the per-plan record holds region totals (rural residents in urban-majority divisions, mixed and urban-majority mixed counts), not eight per-division shares.
3. **Region-wide measures.** These are reported beside the focus count. The plan's ranking target is the focus count (8,138).

**Limits.**
- The region is local, as in `../hybrid_regions/`.
- The municipality-aware weight 0.5 is one setting.
- The panel's lines are the v3 reconstruction.

Files: `lethbridge_rerun.py`, `lethbridge_rerun.json` (summary, replay check), `lethbridge_rerun_selfcheck.json` (panel), `lethbridge_chains/` (per-chain CSV and JSON, original columns plus the rural columns).
