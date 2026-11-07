# The panel minority's ¶167 map beside the panel's map (2026-11-07)

**Unregistered, provisional, and not blind.** The plan was committed before computing (`preregistration/r5_comparator_2026-11-07.md`, commit `5eb63b34`), but its author already knew the panel's scores. Registered Step C and X1 stand. Both maps rest on the page reconstruction, so rerun on the official shapefile when it is posted. Nothing here is a finding on whether any map is a gerrymander, or on whether a change was necessary under Motion 37.

¶167 is the proposal of two panel members in a dispute. It is a comparison point, not a neutral baseline.

## Result

Undoing the panel's changes south of Airdrie moves every partisan measure a little toward the NDP, apart from a near-tie on election-day mean-median. The seat difference is 1 on all ballots and 2 on election-day ballots, and every seat that differs is undecided by the reconstruction. So the direction is consistent and the size is not established.

The changes also do not make the panel's map stand out from the neutral plans. On most measures it sits nearer their median than the ¶167 map does, and neither map reaches p95 on any partisan measure against set D. On the structural lane the ¶167 map fires more flags than the panel's (3 of 5 against 2 of 5).

| Measure (rank against 91-district set D) | Panel, election day | ¶167, election day | Panel, all ballots | ¶167, all ballots |
|---|---|---|---|---|
| Seats, UCP / NDP | 58 / 33 (p42.7) | 56 / 35 (p7.5) | 51 / 40 (p42.9) | 50 / 41 (p21.9) |
| Efficiency gap | +1.45% (p47.9) | −0.24% (p13.3) | −1.66% (p48.0) | −2.19% (p36.8) |
| Mean-median | −2.53 (p17.0) | −2.46 (p19.7) | −1.09 (p77.4) | −2.90 (p6.5) |
| Declination | +0.004 (p52.4) | −0.039 (p11.7) | −0.060 (p47.6) | −0.080 (p25.3) |
| Seats at 50/50 | 48.35% (p91.6) | 47.25% (p77.7) | 49.45% (p89.9) | 48.35% (p72.6) |
| Close seats (within 4 points) | 11 | 12 | 10 | 10 |

Method check: the 2019 map returns 49 UCP / 38 NDP on all ballots, as it should, and 57 / 30 on election-day ballots, as before. Set D ranks reproduce the panel's published all-ballots figures (for example efficiency gap p48.02). Set D's n_eff status is provisional, as in `../allballots_ranking/`.

| Structural check (flag rule, spec §3) | Panel | ¶167 |
|---|---|---|
| S1 population MAD (above 3,382.5) | **3,557** | **3,413** |
| S2 municipal splits (above 26.5) | 24 | 23 |
| S3 anchoring (below 76.01%) | **74.29%** | **75.84%** |
| S5 drain (below 0.0039) | 0.00442 | **0.00369** |
| S6 chair-flag patterns (3 or more) | 1 | 0 |
| S4 Polsby-Popper median (not counted) | 0.4549 | 0.4335 |
| **Flags** | **2 of 5** | **3 of 5** |
| Towns over-divided (`towns_flagged`) | 1 (Lethbridge, 4 districts for 2) | 0 |
| City gap | +4.27% | +3.46% |

Bold = flag. On the rule's own terms 3 of 5 reads "replicated" for ¶167, but S1, S3 and S5 all fire close to midpoints set between the commission maps. Those midpoints were written for a third map, not for a variant of one. This is reported, not explained away.

## Which changes do the work

Groups were found from the voting areas that move, not assumed. There are three, and each can be switched alone.

| Group (panel's names) | Seats on panel's map → ¶167 map, all ballots | Efficiency gap if only this group is undone |
|---|---|---|
| South: Banff-Canmore-Diamond Valley, Okotoks, Lethbridge, Lethbridge-Cardston, Lethbridge-Little Bow, Lethbridge-Taber-Warner, Macleod-Crowsnest, Olds-Didsbury-Three Hills | 7 UCP, 1 NDP → 6 UCP, 2 NDP | −2.19% (all of the difference) |
| West Calgary and Cochrane: Calgary-Bow-Springbank, Calgary-North West-Bearspaw, Calgary-West-Springbank, Cochrane | 4 UCP → 4 UCP | No change |
| Red Deer in Blackfalds-Innisfail: Blackfalds-Innisfail, Red Deer-South | 2 UCP → 2 UCP | No change |

**Deviation from the plan's four groups:** Banff and Okotoks, Lethbridge and the south, and the Wheatland amendment are connected, so they form one group and are not forced apart.

**The seat that differs on all ballots.** Canmore-Banff is NDP by 11.25 points on the ¶167 map. The panel's Banff-Canmore-Diamond Valley, which adds the Highway 22 corridor, is UCP by 1.29 points (229 votes), with about 3,700 votes in voting areas cut by its lines. The panel's stated reason is population: to meet the 25% limit without s.15(2) status (PDF p.95). The minority disputes that it had to be done this way (¶¶140-141). Both the effect and the reason are on the record, and this does not show why the line was drawn.

**On election-day ballots** Lethbridge-West (NDP by 1.29) is the second seat. On all ballots Lethbridge-East is UCP by 1.54 on the ¶167 map, so Lethbridge gives each map one NDP seat there.

**Undecided seats** (margin smaller than the votes in voting areas cut by a differing line) are listed in `comparison.json`. On all ballots: Banff-Canmore-Diamond Valley, Lethbridge, Lethbridge-Cardston, Calgary-Bow-Springbank (panel); Canmore-Banff, Lethbridge-East, Calgary-Bow, Calgary-West-Elbow Valley (¶167).

## Fit check

The list closes. Three sources assembled into 91 divisions with 814 people (0.02%) in overlaps and no voting area in a gap, against the plan's 1% limit. The overlaps are 7.3 km² between High River-Vulcan-Siksika and Olds-Didsbury-Three Hills (one voting area, assigned by the plan's rule) and 4.2 km² between West Yellowhead and Canmore-Banff (no voting area). Interim-mapped divisions use v3 polygons, since no interim shapefile exists here. Their populations match the interim report, including Fort McMurray-Lac La Biche 47,304 and Fort McMurray-Wood Buffalo 46,721. `fit_check.json` has the detail.

## What this cannot show

It cannot show purpose. It covers one election's votes. It compares against one proposal, and a net figure can hide local effects, which is why the seats are named. It also does not test whether the panel applied its stated reasons consistently.

Files: `build_para167.py`, `compare_para167.py`, `para167_map.gpkg`, `va_assignment.csv`, `comparison.json`, `real_maps_*.json`, `structural.json`.
