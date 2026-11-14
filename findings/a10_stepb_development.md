# Amendment 10: development of the assembly, snapping and verification pipeline

> Written 2026-11-03 and 2026-11-04 (Alberta time), before Amendment 10 was filed. Every number here comes from the development fixture: the 34 sample pages' placements from the second calibration run (`findings/a9_stepb_calibration.json`) and the 35 changed pages' placements from version 3 development (`findings/a9_stepb_v3_dev/results.json`), rebuilt by `findings/a10_dev/make_fixture.py`. The sample is fully seen; this record exists so that what was seen, and what was changed because of it, is on the record before the registered run.

## The target set by the author

Iterate until drift is under 0.05%, every voting area is assigned as Elections Alberta would assign it, edges snap together, a sanity check passes on the final map, and every district is recovered from the PDF, from its own page, its neighbours' pages and the report's text.

## What the pipeline does

1. **Pages** (`analysis/scripts/a10_reconstruct_pages.py`). Version 3 runs on each page and saves the polygon and diagnostics, including rejected fits, marked as such.
2. **Assembly** (`analysis/scripts/a10_assemble.py`). Known-overlap and mutual-overlap rejection, assignment of voting areas by largest area share, hole fill by claim, enclosed fragments, population reported.
3. **Snap, assign, verify** (`analysis/scripts/a10_snap_assign.py`). Edges snapped within 40 m, drift measured, every voting area assigned, merged holes split by the better rejected fit, the sanity check.
4. **Scorer** (`analysis/scripts/a10_stepb_calibrate.py`). The Amendment 7 gates on the final assignment, with the assembly-only figures beside them.
5. **Neighbours** (`analysis/scripts/a10_neighbours.py`). The neighbour numbers and neighbour boundaries drawn on each page.

## The iterations, in order, and what each one found

| # | Change | Found by | Fixture result (calibration set) |
|---|---|---|---|
| 1 | First assembly: overlap rules with a fit-quality tie-break, hole fill by page anchor, 5% population gate | design | T1 14.46%, T4 +1.93. A misplaced Edmonton-Meadows (a changed page) rejected three correct sample districts on the fit-quality tie-break; the 5% population gate would have set aside most correct districts |
| 2 | Tie-break by conflict count first; population reported, not gated | #1 | Glenora-Riverview, McClung and West Henday kept; Meadows rejected |
| 3 | Hole claims: title-named town in the hole, else the page's place-name envelope; area within 25% of stated | #1, #2 | Sherwood Park's page claimed Windermere's hole (similar size); Grande Prairie-Wapiti's title names a known city, so its claim never fell through to the envelope |
| 4 | Envelope from every place named on the page and in the title, buffered by half the district's extent; claim (b) when no title town lies in any hole | #3 | T1-like 6.65%; every filled district correct |
| 5 | Printed-neighbour check on claims, majority form; a city's name counts for its districts | #3, snap sanity | Sherwood Park's claim on Windermere's hole rejected |
| 6 | Pooled title claims (Chestermere and Strathmore in separate fragments) | fragment diagnosis | Chestermere-Strathmore filled with all 48 of its voting areas |
| 7 | Snap stage: edges within 40 m; drift; merged hole split by the rejected fit with more matched points | snap runs | Drift 0.005% on the calibration set, 0.003% on the real map's known set; Peace River 60 of 60 |
| 8 | Sanity items refined: multipart allowed where the page draws it; adjacency ⊆ printed, majority, edges over 200 m, city labels; filled-district area informational | snap runs | every item passes on both sets |
| 9 | In-frame item (a placed district drawn back on its page must lie inside the map frame) | author | the four misplaced transforms 100% outside; every used transform 0.0% |
| 10 | Locator-inset item | author | 90 of 91 pass on both sets; largest offset 0.94 km on the real map's known set and 2.95 km on the calibration set; page 268's inset highlights the wrong district (source error) |
| 11 | Final assignment by representative point | author's standard ("as Elections Alberta would") | 11 voting areas moved; T1 0.0% |
| 12 | Version 4 (locator-inset prior) tested on the four misplaced pages, not adopted | inset finding | Sherwood Park IoU 0.999; Meadows and Windermere within 0.9 km of their inset shapes; Calgary-North West-Bearspaw still unplaced (`analysis/scripts/a10_stepb_reconstruct_v4.py`) |
| 13 | Reporting-only checks: cut voting-area range, two drawings of each changed line, written descriptions with page overlays (`findings/a10_dev/`) | author ("how do we drive it down") | calibration flip range −0.10 to +0.06 points, T1 at most 0.52%; on the real map no disputed voting area changes district; every description miss traced to the check or the text, or to a hole fill that Version 4 confirms (IoU 0.967, 0.991) |
| 14 | Districts file written as polygons only | row 13 overlays (zero-area lines in 15 districts) | assignments, drift and sanity unchanged on both maps |
| 15 | Districts file: a cut voting area's part inside another piece drawn with that district; a part in no piece given to the neighbour it shares the longest edge with, filled districts included | author ("strip then file"); final-vs-page audit (1,299 fragments; Cochrane holding a 5.8 km² strip of Calgary-North West-Bearspaw) | North West-Bearspaw 31.4 to 37.4 km² (stated 37), its page shape now IoU 0.996 on the fill; placed districts departing from their pages by over 0.1 km² 17 to 4; no assignment changed |
| 16 | Near-line voting areas checked against every drawing; filled districts' own page shapes fitted onto the fills | author ("triple check") | of 15 voting areas within 100 m of a changed line, 10 settled, 3 agreeing within the drawing grid, 2 (1,312 people) undecidable from the PDF; Windermere 0.970, Meadows 0.983 |

**Final fixture result:** on the calibration set (22 tuning districts known), all 1,909 sample voting areas assigned correctly (T1 0.0%), efficiency-gap delta 0.00 points (T4), 91 districts, every voting area assigned, drift 0.005%, every sanity item passing, Peace River and Fort McMurray-Wood Buffalo flagged lower confidence (split). Before snapping, the assembly alone gave T1 3.3% and T4 −0.03 points. On the real map's known set (56 unchanged and Calgary-Acadia), every sanity item passes with drift 0.003%. Rules added after the fixture first scored, and the sample outcomes that prompted them, are listed in Amendment 10, Part 2. The fixture is development data: these figures are expected, not out-of-sample (`C:/tmp` working copies are not part of the record; the registered run writes its own).

## Findings worth keeping

- **Three development pages were misplaced**, all with ambiguous road-search priors: Calgary-North West-Bearspaw (overlapping known districts by 16%), Edmonton-Windermere (51%) and Edmonton-Meadows (15 km off). The known-overlap rule catches all three on the real map.
- **The population check cannot gate.** On the 57 known districts, the panel's stated populations differ from the scaled 2021 voting-area populations by −39% to +13% (`findings/a10_dev/population_check_noise.csv`).
- **Hole fills are made of whole voting areas**, so their area runs under the drawn area by the parts of cut voting areas that lie in them. Chestermere-Strathmore's hole is 28% under its stated area for that reason alone.
- **Pages do not print every neighbour**, and show a city's districts under the city's name.
- **A shape that bleeds off its page is wrong.** Drawing each final district back onto its own page with that page's transform marks the four misplaced transforms (Calgary-North West-Bearspaw, Edmonton-Meadows, Edmonton-Windermere, Sherwood Park) at 100% outside the map frame and no other page above 0.3%.
- **The locator inset is a provincial map in the map's own coordinates.** On pages 50 to 91 the inset is drawn at 7.49 km per point with no rotation beyond the page's, and fits the known districts to a median 0.5 km; Calgary and Edmonton pages carry a city inset instead. Assembled districts sit a median 0.3 km (at most 0.9 km) from their inset shapes; the four misplaced page fits sat 12 to 21 km off. Page 268's inset highlights Drayton Valley-Devon instead of Barrhead-Westlock-Athabasca, a source error in the report.
- **The report's written descriptions** (`findings/a10_dev/boundary_descriptions.md`) give a full metes-and-bounds ring for one changed district (Lethbridge) and rough prose rings for seven more. They are a check on particular lines, not a source for whole districts.

## Environment

Python 3.12.13 with PyMuPDF 2.1 (`findings/a9_stepb_v3_dev/environment.txt`), as pinned in Amendment 9; the scorer refuses any other.
