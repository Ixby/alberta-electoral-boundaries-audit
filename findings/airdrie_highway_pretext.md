---
name: v0_9_airdrie_highway_pretext
description: Tests whether the district lines that divide Airdrie follow highways and the city limit or are free-drawn. On the official boundaries the minority's two Calgary-side districts follow highways and the city limit for about 90 % of their perimeters (Calgary-Airdrie 9.4 % free-drawn; Calgary-Foothills-Airdrie West 8.1 %), so the earlier reading that highway anchoring was a pretext does not hold.
type: project
---

# Airdrie split: do the dividing lines follow highways or the city limit?

> **Superseded figures (2026-10-31, correction C45).** This finding's population shares come from pre-canonical (DPG) geometry. On the official boundaries the majority divides Airdrie roughly in half (Airdrie-East 49.4 %, Airdrie-West 50.6 %), not 73.8 % in one division; the minority's Airdrie-East holds 54.7 % of the city and is 89.6 % Airdrie, so one minority division is Airdrie-majority; and the majority map places no Airdrie residents in Cochrane-Springbank or Calgary-North East (`data/outputs/airdrie_split_shares_2026-10-31.json`).
>
> **Perimeters remeasured (2026-10-31, correction C48).** The same measurement (500 m snap, 50 m vertices, city limit before highway), run on the official boundaries (`analysis/scripts/airdrie_city_limit_anchoring.py`; `data/outputs/airdrie_city_limit_anchoring_2026-10-31.csv`), does not reproduce the table below. Minority: Airdrie-East 170.1 km, city limit 1.6 %, highway 37.3 %, neither 61.1 %; Calgary-Airdrie 39.8 km, 14.9 % / 75.7 % / 9.4 %; Calgary-Foothills-Airdrie West 54.7 km, **10.8 %** / 81.0 % / 8.1 %; Olds-Three Hills-Didsbury 405.2 km, 0.7 % / 12.8 % / 86.6 %. Majority: Airdrie-West 61.6 km, 3.1 % / 59.5 % / 37.4 %; Airdrie-East 195.0 km, 1.0 % / 14.4 % / 84.7 %. Calgary-Foothills-Airdrie West shares about 4 km of border with the city (4.15 km within 20 m of the limit) and holds 20.9 % of its residents; it is not 0 %, and it does not stay outside the city. Calgary-Airdrie is 9.4 % free-drawn, not 70.9 %. Sections 2 and 4 now give the result on the official boundaries; the pre-canonical table is kept in §2.2 as the record of the first run.

**Status: companion to `natural_anchoring_secondary_check.md`. The province-wide natural-anchoring run showed that the minority map's CSD-anchoring deficit cannot be recovered as a uniform substitution to highways — all three maps cluster at 38-40 % on highways+rivers. This memo asks the local question at Airdrie: do the minority's lines track highways and the city limit, or do they enter on a highway and then run free-drawn through the city? On the official boundaries they track highways and the city limit (§2.1).**

## 1. The statutory question

Alberta's Electoral Boundaries Commission Act, s.14 (commission report p.15, quoted verbatim in `analysis/methodology/terms_of_reference_verbatim.md`) lists the criteria the Commission "may take into consideration" once the Charter requirement of effective representation is satisfied. Two of those subsections frame this fight:

> **14(b)** communities of interest, including municipalities, regional and rural communities, Indian reserves and Metis settlements,
>
> **14(d)** the availability and means of communication and transportation between various parts of Alberta,

Both are valid criteria. A commission that anchors a boundary on a city limit invokes 14(b); a commission that anchors on a highway invokes 14(d). The empirical question is whether the minority's Airdrie lines follow highways (a 14(d) reason) or only enter on a highway and then run free-drawn, following neither the road grid nor the city limit, which would make the 14(d) language a cover.

## 2. The empirical answer

### 2.1 Official boundaries

Same measurement (500 m snap, 50 m vertices, city limit attributed before highway), run on Elections Alberta's official boundaries for each district holding Airdrie residents on 2021 census dissemination areas (`analysis/scripts/airdrie_city_limit_anchoring.py`; `data/outputs/airdrie_city_limit_anchoring_2026-10-31.csv`):

| Map | ED | Perim km | City-limit % | Highway % | Neither % | Airdrie residents | % of city |
|---|---|---:|---:|---:|---:|---:|---:|
| Majority | Airdrie-West | 61.6 | 3.1 | 59.5 | 37.4 | 37,514 | 50.6 |
| Majority | Airdrie-East | 195.0 | 1.0 | 14.4 | 84.7 | 36,586 | 49.4 |
| Minority | Airdrie-East | 170.1 | 1.6 | 37.3 | 61.1 | 40,501 | 54.7 |
| Minority | Calgary-Airdrie | 39.8 | 14.9 | 75.7 | 9.4 | 17,752 | 24.0 |
| Minority | Calgary-Foothills-Airdrie West | 54.7 | 10.8 | 81.0 | 8.1 | 15,496 | 20.9 |
| Minority | Olds-Three Hills-Didsbury | 405.2 | 0.7 | 12.8 | 86.6 | 351 | 0.5 |

The two metrics that test the reading are **city-limit %** (does the ED trace the municipal edge?) and **neither %** (how much of its perimeter is free-drawn, following neither the city limit nor a major highway?).

**The minority's Calgary-side districts are the most anchored in the table.** Calgary-Airdrie follows the city limit or a major highway for 90.6 % of its perimeter and is 9.4 % free-drawn; Calgary-Foothills-Airdrie West follows them for 91.9 % and is 8.1 % free-drawn. Both share a few kilometres of border with the city (3.3 km and 4.15 km within 20 m of the limit). These are the districts that take Airdrie residents into Calgary-majority seats, and their lines run along roads and the city edge, not free-hand across the city.

**The highest free-drawn shares belong to the large districts on both maps** that reach out into the surrounding country: Olds-Three Hills-Didsbury (86.6 %) on the minority map and Airdrie-East (84.7 %) on the majority map. A long rural perimeter has few highways or city limits to follow, so this measure does not separate the maps there.

**What this does and does not show.** The perimeter test gives no sign that the minority used highway anchoring as a cover at Airdrie: where its lines divide the city, they follow highways and the city limit. The test does not say whether dividing Airdrie into three pieces (by the audit's 2 % piece rule) was needed in the first place; that is a separate question, taken up in `findings/justification_tests_findings.md` (Test 3).

### 2.2 Pre-canonical run (record)

The first run, on v0_9 derived geometry, for each ED containing Airdrie territory (population proxy >= 100 voters from 2023 VAs whose centroid is inside Airdrie's CSD), with snap tolerance 500 m matching the audit's headline anchoring runs. Its district set and perimeters do not match the official boundaries, and its reading (that Calgary-Airdrie's 70.9 % free-drawn perimeter showed highway anchoring to be a pretext) does not hold on them.

| Map | ED | Perim km | City-limit % | Highway % | Neither % | Airdrie pop | % of CSD |
|---|---|---:|---:|---:|---:|---:|---:|
| Majority | Airdrie-East        | 143.8 |  2.4 | 49.4 | 48.2 | 11,703 | 73.8 |
| Majority | Cochrane-Springbank | 176.0 |  1.1 | 37.9 | 61.0 |  3,658 | 23.1 |
| Majority | Calgary-North East  |  70.9 |  5.0 | 67.9 | 27.1 |    503 |  3.2 |
| Minority | Airdrie East                  | 145.9 |  1.9 | 51.0 | 47.1 | 9,398 | 59.2 |
| Minority | Calgary-Airdrie               | 180.9 |  2.0 | 27.2 | 70.9 | 4,161 | 26.2 |
| Minority | Calgary-Falconridge           |  29.5 | 11.4 | 77.7 | 10.9 | 1,940 | 12.2 |
| Minority | Calgary-Foothills-Airdrie West |  44.1 |  0.0 | 79.2 | 20.8 |   364 |  2.3 |

(Source: `data/airdrie_quadrant_anchoring.csv`. City-limit % attributed first when a segment matches both substrates, so highway % is the residual highway match.)

## 3. Visual cross-reference

`data/maps/airdrie_4way_teardown.png` (300 DPI, two-panel side-by-side) was prepared on the same pre-canonical v0_9 substrate and shows the §2.2 districts, not the official ones. Its reading, that the minority's lines enter Airdrie on highways and leave on free-drawn diagonals, does not hold on the official boundaries (§2.1). For the official split, see the Airdrie figure redrawn to scale (`data/maps/article/figure_airdrie_v3.svg`, correction C46) and `data/outputs/airdrie_split_shares_2026-10-31.json`.

## 4. Verdict — quote-ready paragraph

At Airdrie, the minority's dividing lines follow highways and the city limit. On the official boundaries, the two districts that take Airdrie residents into Calgary-majority seats, Calgary-Airdrie and Calgary-Foothills-Airdrie West, are 9.4 % and 8.1 % free-drawn, the lowest shares of any district touching the city, and each traces part of the city limit (14.9 % and 10.8 % of its perimeter). Section 14(d) of the Act permits a commission to anchor on roads, and here the minority did. The perimeter test gives no evidence that highway anchoring was a cover at Airdrie. Whether the city needed to be split three ways at all is a different question, which this test does not answer.

## Outputs

- Visual: `data/maps/airdrie_4way_teardown.png` (300 DPI, two-panel; pre-canonical)
- Metrics CSV: `data/airdrie_quadrant_anchoring.csv` (7 rows, 11 cols; pre-canonical)
- Script: `analysis/scripts/airdrie_quadrant_anchoring.py` (pre-canonical)
- Official boundaries: `data/outputs/airdrie_city_limit_anchoring_2026-10-31.csv`, from `analysis/scripts/airdrie_city_limit_anchoring.py`

Forward:
  (none yet — Lane 2 prose update consumes this memo)
Backward:
  archive/dpg_era/natural_anchoring_secondary_check.md
  analysis/scripts/score_anchoring.py
  analysis/scripts/score_natural_anchoring.py
  analysis/methodology/terms_of_reference_verbatim.md
  data/shapefiles/derived/v0_10_topological_{majority,minority}_2026_eds.gpkg
  data/shapefiles/reference/alberta_2021_csds.gpkg
  data/osm/alberta_osm_highways.gpkg
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
