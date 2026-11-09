# Rural voters in mixed city-and-rural divisions (2026-11-07)

**Unregistered and not blind.** The plan was committed before computing (`preregistration/rural_voice_2026-11-07.md`, commit `c01cbdcd`). The panel's map is the v3 reconstruction (provisional until the official shapefile is posted). Population is the 2021 census on voting areas. Votes are all 2023 ballots, UCP and NDP only; election-day votes give the same divisions on every map. Nothing here says whether any map is a gerrymander, and "overridden" describes a 2023 vote count, not the quality of anyone's representation.

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

The Lethbridge area crosses the plan's 5,000-resident trigger (8,138). So the south region's redraws are to be rerun, city-blind and municipality-aware, with the same seeds and settings as `findings/hybrid_regions/`, recording these rural measures. Then the panel's 8,138 is ranked among neutral redraws. **Not yet run.** It was held back while the Amendment 12 replays ran; they finished on 2026-11-08 (`../amendment12_replays/`), and this rerun is still owed.

Files: `rural_voice.py`, `rural_voice.json`.
