# The panel minority's ¶167 map against the panel's map (written before any computation)

> Written 2026-11-07, before the map below has been built or scored. **Unregistered, and written after Step C was seen:** the author of this plan already knows the panel's map's scores and the commission maps' scores, so this is not blind. It is committed first so the construction and the reading cannot be fitted to the result. Registered artifacts, the registered Step C and registered X1 stand unchanged. Requested by the author on 2026-11-07. GitHub only; no OSF filing.

## The question

Did the panel's changes beyond the two-seat restoration move seats or fairness measures, and in whose favour? The panel's minority lists at ¶167 (IAP report, PDF pp. 161-163) a complete 91-division map that restores the two divisions and otherwise keeps closer to Recommendation 5. Scoring that list beside the panel's map answers the question for that comparison.

The list is the proposal of two panel members in a dispute, so it is a comparison point and not a neutral baseline. Neutral baselines are the ensembles, used below.

## Building the map

From ¶167, item by item, in EPSG:3400:

| Items | Source | Geometry |
|---|---|---|
| 1-68 | "As Mapped by the ABEBC Majority Final Report" | The official majority shapefile, `ea_majority_2026_eds.gpkg` |
| 69-76 | "As Mapped by the ABEBC Interim Report" | The v3 polygons of the same name. No interim shapefile exists here. The panel says it adopted the interim report for these areas. Checked by comparing Appendix 7 with the interim report's populations, and any mismatch is reported |
| 77-88 | "As Mapped in the IAP Majority Report, for a Unanimous IAP" | The v3 polygons of the same name |
| 89 Canmore-Banff | Majority, "excluding areas that the unanimous IAP has moved to Rocky Mountain House-Sundre" | Majority polygon minus v3 Rocky Mountain House-Sundre |
| 90 Blackfalds-Innisfail | IAP majority, "excluding areas in the City of Red Deer" | v3 polygon minus the majority's Red Deer-North and Red Deer-South |
| 91 Olds-Didsbury-Three Hills | IAP majority, "excluding areas in Wheatland County" | v3 polygon minus Wheatland County, taken from the CSD layer the audit already uses |

v3 is `iap_2026_assembled_v3.gpkg`, SHA-256 `8ea5caf68ac95bffe3d7e8a58635b8888f742b3bf115cf3787da3cc92caca1b7`.

**Fit check, reported whatever it shows.** The list claims to cover Alberta with 91 divisions. Pieces from three sources may overlap or leave gaps. The build reports every overlap and gap over 0.1 km², with its area and its voting areas, and compares each rebuilt division's population with its stated figure.

**Resolving overlaps and gaps.** Voting areas go to divisions by representative point, as in the audit's other runs:
- A point in one division goes to it.
- A point in two goes to the ¶167 majority-list division, because the list says those divisions are as the commission mapped them. If both or neither are on that list, it goes to the division holding more of the voting area's area.
- A point in none goes to the division holding the most of the voting area's area; these are listed.

If gaps or overlaps hold more than 1% of Alberta's population, the list could not be built as read: that is reported as the first finding and the comparison is marked unreliable.

## What is scored

Both maps, by the same code, on the same two ballot sets:
- **Election-day ballots** (the audit's registered substrate).
- **All ballots** (`va_polygons_with_all_2023_ballots.gpkg`, substrate D of the seat-claim test, which reproduces the official results). Method check: the 2019 map must return 49 UCP and 38 NDP.

Measures: seats, efficiency gap, mean-median, declination, seats at 50/50, close seats, population MAD and the structural battery (S1-S6). Every district whose winner differs is named with its margin.

Rank against the 91-district set D chains, on matching ballots. That is the same treatment the panel's map received in `findings/allballots_ranking/`.

**By group of changes.** Where a group of divisions covers the same ground on both maps, that group alone is switched, to show its share of any difference:
- West Calgary and Cochrane
- Banff and Okotoks
- Lethbridge and the south
- The minority's two other amendments (Red Deer in Blackfalds-Innisfail; Wheatland County in Olds-Didsbury-Three Hills)

A group that is not closed is reported as not separable, not forced.

**Undecided seats.** A seat is undecided if its margin is smaller than the votes in voting areas cut by a line that differs between the two maps. Seat differences are reported with the undecided seats named.

## How the result is read

- **Reported whichever way it comes out.** A difference favouring either party, or none, is reported at the same prominence.
- **What it can show:** the net effect of these changes on these measures, on 2023's votes, against this comparison map.
- **What it cannot show:** purpose. An effect does not show intent, and no effect does not show the changes were justified. A net-zero total can hide offsetting local effects, which is why the groups and the named seats are reported.
- **Provisional:** both maps rest on the page reconstruction. Rerun on the official shapefile when it is posted.
- By the audit's standing rule, no conclusion is drawn on whether any map is a gerrymander, and no ruling on whether a change was necessary under Motion 37.

**Signed:** Claude (acting as session agent), directed by Will Conner
