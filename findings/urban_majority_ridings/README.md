# How many ridings have an urban majority?

2026-11-13 05:00 Alberta time · claude-fable-5-2 · low

**Status: descriptive, exploratory, not registered.** It checks one public claim. It says nothing about why any line was drawn. The panel's map is the audit's reconstruction, so its row is provisional. Numbers: `count.json`, from `count.py`.

## The claim

A post shared on Threads and Facebook, seen 2026-11-12 and credited to Philip Cape, says of the 91-riding map: 82% of Albertans live in urban centres and 18% in rural areas; the 69 urban ridings on the previous map are now 43, and rural and hybrid ridings went from 18 to 48; so 82% of the population is represented by 42% of the seats and the rural 18% "command 58% of the legislature".

## What the count shows

Each 2021 census dissemination area is placed in its municipality and its riding. A riding is urban-majority when over half its residents live in an urban municipality. Two definitions of urban are used, because the post gives none. Neither is Statistics Canada's "population centre" measure, the usual source of an 82% figure; the two sit on either side of it.

| Map | Ridings | Urban-majority, cities only | Urban-majority, cities and towns |
|---|---:|---:|---:|
| 2019 | 87 | 58 (67%) | 77 (89%) |
| Commission majority | 89 | 62 (70%) | 77 (87%) |
| Commission minority | 89 | 61 (69%) | 80 (90%) |
| Panel (reconstruction) | 91 | 62 (68%) | 80 (88%) |

Urban share of the 2021 population: 70.9% (cities only), 86.0% (cities, towns, Strathcona County and Wood Buffalo).

- **The share of urban-majority ridings tracks the urban share of the population on every map**, under both definitions. On the panel's map it is 68% against 70.9%, or 88% against 86.0%. Neither is near 42%.
- **The claim counts every mixed riding as a rural seat.** Urban residents of a mixed riding vote in it, and in most mixed ridings they are the majority.
- **The "69 to 43" figure does not reproduce.** Ridings that are at least 90% city residents number 54 on the 2019 map and 55 on the panel's. Ridings between 10% and 90% city residents go from 13 to 17 (28 to 33 on the wider definition). The post does not say how it classed ridings.
- **What does change is how cities are divided.** The panel's map has more mixed ridings than the 2019 map and splits some cities into more pieces (`findings/city_weight/README.md`). That is a question about communities, not about how many seats urban voters hold.

## Limits

- 2021 census populations, not the 2024 estimates the maps were drawn on.
- A dissemination area counts wholly in the riding and municipality that hold its representative point.
- The wider definition counts the rural parts of Strathcona County and Wood Buffalo as urban, so it overstates a little. Villages, summer villages and hamlets are not counted as urban in either.
- Urban-majority says who is the majority of residents, not how a riding votes.
