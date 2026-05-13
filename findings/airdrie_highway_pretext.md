---
name: v0_9_airdrie_highway_pretext
description: Local empirical answer to the Highway Anchoring Defense — at the Airdrie carve, the minority's quadrant boundaries enter via Highway 2 and Highway 567 but exit via free-drawn lines that follow neither the highway grid nor the city limit, slicing through dense residential clusters to reach the next non-Airdrie community.
type: project
---

# v0_9 Airdrie quadrant: highway anchoring as pretext

**Status: companion to `natural_anchoring_secondary_check.md`. The province-wide natural-anchoring run showed that the minority map's CSD-anchoring deficit cannot be recovered as a uniform substitution to highways — all three maps cluster at 38-40 % on highways+rivers. This memo answers the second-order question: at the audit's strongest local case (the Airdrie carve), are the minority's lines actually tracking highways principially, or are highways being used as entry-only pretext while residential mass is sliced by free-drawn lines?**

## 1. The statutory question

Alberta's Electoral Boundaries Commission Act, s.14 (commission report p.15, quoted verbatim in `analysis/methodology/terms_of_reference_verbatim.md`) lists the criteria the Commission "may take into consideration" once the Charter requirement of effective representation is satisfied. Two of those subsections frame this fight:

> **14(b)** communities of interest, including municipalities, regional and rural communities, Indian reserves and Metis settlements,
>
> **14(d)** the availability and means of communication and transportation between various parts of Alberta,

Both are valid criteria. A commission that anchors a boundary on a city limit invokes 14(b); a commission that anchors on a highway invokes 14(d). The empirical question is whether the minority's Airdrie carve uses highways as **principial anchors** (a 14(d) defense) or as **entry pretext** for free-drawn lines that respect neither the road grid nor the city limit (an instrumental use of 14(d) language to defeat 14(b)).

## 2. The empirical answer

For each ED that contains Airdrie territory under v0_9 (population proxy >= 100 voters from 2023 VAs whose centroid is inside Airdrie's CSD), with snap tolerance 500 m matching the audit's headline anchoring runs:

| Map | ED | Perim km | City-limit % | Highway % | Neither % | Airdrie pop | % of CSD |
|---|---|---:|---:|---:|---:|---:|---:|
| Majority | Airdrie-East        | 143.8 |  2.4 | 49.4 | 48.2 | 11,703 | **73.8** |
| Majority | Cochrane-Springbank | 176.0 |  1.1 | 37.9 | 61.0 |  3,658 | 23.1 |
| Majority | Calgary-North East  |  70.9 |  5.0 | 67.9 | 27.1 |    503 |  3.2 |
| Minority | Airdrie East                  | 145.9 |  1.9 | 51.0 | 47.1 | 9,398 | 59.2 |
| Minority | Calgary-Airdrie               | 180.9 |  2.0 | 27.2 | **70.9** | 4,161 | 26.2 |
| Minority | Calgary-Falconridge           |  29.5 | 11.4 | 77.7 | 10.9 | 1,940 | 12.2 |
| Minority | Calgary-Foothills-Airdrie West |  44.1 |  **0.0** | 79.2 | 20.8 |   364 |  2.3 |

(Source: `data/airdrie_quadrant_anchoring.csv`. City-limit % attributed first when a segment matches both substrates, so highway % is the residual highway match.)

The two metrics that isolate the defense are **city-limit %** (does the ED actually trace the gazetted municipal edge it claims to share?) and **neither %** (how much of the ED's perimeter is free-drawn — neither tracking the city limit nor any major highway?).

**City-limit anchoring is symmetrically low across both maps.** The shared Airdrie CSD perimeter is only ~37 km, and every Airdrie-touching ED has a perimeter of 30-180 km, so even an ED that perfectly traced the city limit would only score 20-30 % city-limit. What discriminates is whether, having spent only 1-5 % of perimeter on the city limit, the ED then spends the rest on highways or on free-drawn lines.

**Calgary-Airdrie is the signature case for pretext.** Its perimeter is the longest in the table (180.9 km), only 2.0 % follows the city limit, only 27.2 % follows a major highway, and **70.9 % follows neither** — the highest free-perimeter share of any ED that touches Airdrie. The ED also holds 4,161 Airdrie residents (26.2 % of the CSD), so this free-drawn perimeter is cutting through populated city blocks, not bounding a rural fringe. Calgary-Foothills-Airdrie West shows the inverse pretext: an ED whose name advertises Airdrie but whose perimeter has **0 %** city-limit anchoring — it doesn't even border the gazetted city limit at v0_9 substrate precision.

**The majority's Airdrie-East holds 73.8 % of all Airdrie residents in a single ED.** No minority ED holds a majority of Airdrie's population — the largest, the minority's own Airdrie East, holds 59.2 % and surrenders the rest to three other districts.

## 3. Visual cross-reference

`data/maps/airdrie_4way_teardown.png` (300 DPI, two-panel side-by-side, prepared on the same v0_9 substrate) makes the malice legible at a glance. **Left panel (majority):** Airdrie-East shaded green covers the residential mass; Cochrane-Springbank takes only the western rural fringe; Calgary-North East takes only a small southern sliver. **Right panel (minority):** four colours converge on Airdrie's residential centre. Calgary-Airdrie's boundary enters the city via Highway 2 / QE2 along the eastern flank, then exits not via Highway 567 (which it crosses), not via Highway 2A (which it crosses), but via a free-drawn diagonal that captures dense neighbourhoods on its way to Calgary-Falconridge to the south. Calgary-Foothills-Airdrie West, despite its name, does not touch the city limit at all — it occupies a rural quadrant west of the city and reaches in via highway 2A only. The visual confirms what the metrics describe: highway tracks are used as **entry corridors**, but the **exit lines are free-drawn**.

## 4. Verdict — quote-ready paragraph

The Highway Anchoring Defense is empirically a pretext at the Airdrie carve. Of the four minority EDs that draw Airdrie residents into themselves, one (Calgary-Foothills-Airdrie West) doesn't follow Airdrie's gazetted city limit at all, and the largest by perimeter (Calgary-Airdrie) draws 70.9 % of its boundary along neither the city limit nor any major highway — the highest free-perimeter share of any ED touching the city. The majority concentrates 73.8 % of Airdrie's population inside a single ED that uses the same highway corridors as anchors but does not splinter the residential mass behind them. Section 14(d) of the Act permits a commission to anchor on roads; it does not permit a commission to enter a city via a road and then carve free-handed across populated neighbourhoods to reach a distant rural community. The minority's Airdrie quadrant uses the language of highway anchoring and the geometry of free-drawn diagonals — and the audit's burden of proof on instrumental versus principial use of 14(d) is met locally even where the province-wide natural-anchoring run could not meet it.

## Outputs

- Visual: `data/maps/airdrie_4way_teardown.png` (300 DPI, two-panel)
- Metrics CSV: `data/airdrie_quadrant_anchoring.csv` (7 rows, 11 cols)
- Script: `analysis/scripts/airdrie_quadrant_anchoring.py`

Forward:
  (none yet — Lane 2 prose update consumes this memo)
Backward:
  analysis/reports/natural_anchoring_secondary_check.md
  analysis/scripts/score_anchoring.py
  analysis/scripts/score_natural_anchoring.py
  analysis/methodology/terms_of_reference_verbatim.md
  data/shapefiles/derived/v0_10_topological_{majority,minority}_2026_eds.gpkg
  data/shapefiles/reference/alberta_2021_csds.gpkg
  data/osm/alberta_osm_highways.gpkg
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
