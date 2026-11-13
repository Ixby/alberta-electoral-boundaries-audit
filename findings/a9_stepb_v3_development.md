# Step B, version 3: development results

> Written 2026-11-03 (Alberta time), before Amendment 9 was filed and before the second calibration was run. No sample page was opened: every development run refused the 34 sample districts in code, and none of the 57 districts below is in `findings/a7_stepb_sample.json`.

## What was found

Version 2 (`findings/a9_stepb_v2_development.md`) placed the city pages but locked onto only 1 of the 10 changed pages over 10,000 km². Looking at a failing rural page, Drumheller-Stettler, showed why:

- **Its line styles mean other things on rural pages.** Once the page was placed from its village dots, the dark-grey 0.92-pt strokes lay a median 16 m from the National Road Network: they are the full road network. The light-grey 0.37-pt strokes were the township survey grid. Version 2's fixed rules, set on city pages, matched the first against census-subdivision boundaries and the second against roads.
- **Prairie roads lie on a one-mile grid.** A road search with no other information finds many near-equal placements a whole number of miles apart, which is the "no lock" version 2 showed.
- **The page's municipalities break the grid.** The map draws village dots at Statistics Canada's own subdivision centroids. Matching 24 dots by name placed Drumheller-Stettler with a median residual of 40 m, before any road matching. Town areas and First Nations reserve areas are drawn from the subdivision polygons too. Their centroids add matches on pages with few villages, such as Rocky Mountain House-Sundre (the author pointed out that it has more than one municipality). Some names wrap across lines, such as "Rocky / Mountain / House".

The survey-grid numbers in the margins were also tried as a prior (township and range labels against Township Road and Range Road names in the road network). They place a page to within 0.2 to 1.5 km, too loose against a 1.6-km road spacing, so version 3 does not use them.

## The procedure

`analysis/scripts/a9_stepb_reconstruct_v3.py`; its docstring lists every change. In short:
1. a prior from the page's municipalities (dots, town areas and reserve areas matched to 2021 census subdivisions), or else version 2's road search;
2. each grey line style assigned to the reference it matches (roads, or census-subdivision boundaries);
3. a local search and ICP within the prior's error;
4. an acceptance rule: at least 2,000 matched page points, lying a median of at most 40 m from their references, with at least 60% of them within 60 m.

The thresholds were set from the results below. Every accepted page has 9,363 to 53,806 matched points, a median of 5.4 to 29.6 m and 72% to 96% within 60 m.

## Results

| | Pages | Accepted | Notes |
|---|---|---|---|
| Tuning districts (official geometry) | 22 | 22 | IoU 0.9975 to 0.9996; boundary error (Hausdorff) 1 to 6 m |
| Changed districts under 1,000 km² | 16 | 16 | |
| Changed districts of 1,000 to 10,000 km² | 9 | 9 | version 2 locked 8 |
| Changed districts over 10,000 km² | 10 | 9 | version 2 locked 1; the failure is Wood Buffalo |

The one failure is **Fort McMurray-Wood Buffalo** (86,353 km²). Its page names only six First Nations reserves and no other subdivision: Fort McMurray is part of the Regional Municipality of Wood Buffalo, not a subdivision of its own. Three of the six matched, 571 m apart on median. It went through three stages in development, recorded here because the last one changed the rule:
1. *First build.* No line style matched a reference within the prior's error, so the page failed.
2. *A wide retry, since removed.* After a failed first pass the search widened to 5 km and ±1% scale. That placed the page with a median of 182 m and 24% within 60 m, which the rule rejects.
3. *Final build.* A 3-match prior's rotation is now snapped to the right angle, because three points fix rotation poorly (this prior carried 0.36°). With that change the first pass matched only the dark-grey 2.76-pt provincial-border style: 363 points, a median of 15.8 m and 99% within 60 m. At that placement the page's roads agree with the road network at only 4% within 60 m, so the placement is wrong. The median-and-share rule would have accepted it.

So the acceptance rule gained a floor of 2,000 matched points (accepted pages have at least 9,363), and the wide retry was removed: it never produced an accepted page, and a wide search risks a one-mile alias on prairie pages. Under the final rule the page fails, and in a calibration run a page like this counts as a failure.

Every placed page, by stated area ("Rule" is the acceptance rule):

| ED | Set | District | Stated km² | Prior | Matched points | Median distance (m) | Within 60 m | Rule | IoU | Hausdorff (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | tuning | Calgary-Buffalo | 4 | v2 | 13,528 | 7.1 | 0.89 | pass | 0.9985 | 1 |
| 40 | changed | Edmonton-Meadows | 13 | v2 | 15,318 | 17.6 | 0.93 | pass | — | — |
| 7 | tuning | Calgary-Cross | 16 | v2 | 34,757 | 7.8 | 0.93 | pass | 0.9975 | 6 |
| 19 | tuning | Calgary-Mountain View | 16 | v2 | 30,409 | 6.8 | 0.92 | pass | 0.9995 | 1 |
| 32 | tuning | Edmonton-Decore | 18 | v2 | 22,676 | 5.9 | 0.96 | pass | 0.9981 | 3 |
| 37 | tuning | Edmonton-Highlands-Norwood | 19 | v2 | 26,787 | 6.6 | 0.91 | pass | 0.9985 | 2 |
| 30 | tuning | Edmonton-Castle Downs | 21 | v2 | 27,394 | 6.8 | 0.95 | pass | 0.9988 | 4 |
| 20 | tuning | Calgary-North | 23 | v2 | 32,085 | 6.5 | 0.92 | pass | 0.9982 | 3 |
| 46 | changed | Edmonton-Strathcona | 24 | v2 | 32,291 | 6.3 | 0.89 | pass | — | — |
| 21 | tuning | Calgary-North East | 25 | v2 | 26,179 | 8.0 | 0.91 | pass | 0.9976 | 5 |
| 33 | changed | Edmonton-Ellerslie | 26 | v2 | 29,555 | 7.4 | 0.90 | pass | — | — |
| 48 | changed | Edmonton-Whitemud | 26 | v2 | 22,968 | 5.9 | 0.87 | pass | — | — |
| 1 | changed | Calgary-Acadia | 27 | v2 | 25,250 | 6.5 | 0.94 | pass | — | — |
| 84 | changed | Red Deer-South | 31 | v2 | 30,726 | 6.8 | 0.94 | pass | — | — |
| 43 | tuning | Edmonton-North West | 32 | v2 | 35,324 | 6.3 | 0.92 | pass | 0.9986 | 3 |
| 17 | tuning | Calgary-Lougheed | 34 | v2 | 34,761 | 8.0 | 0.91 | pass | 0.9994 | 3 |
| 24 | tuning | Calgary-Shaw | 34 | v2 | 25,615 | 6.9 | 0.91 | pass | 0.9994 | 3 |
| 16 | tuning | Calgary-Klein | 37 | v2 | 31,148 | 6.5 | 0.94 | pass | 0.9996 | 2 |
| 22 | changed | Calgary-North West-Bearspaw | 37 | v2 | 19,513 | 22.4 | 0.90 | pass | — | — |
| 3 | tuning | Calgary-Bhullar-McCall | 41 | v2 | 33,407 | 7.3 | 0.93 | pass | 0.9989 | 4 |
| 25 | tuning | Calgary-South East | 44 | v2 | 29,971 | 8.1 | 0.90 | pass | 0.9984 | 5 |
| 23 | tuning | Calgary-Nose Creek | 45 | v2 | 31,361 | 7.0 | 0.93 | pass | 0.9990 | 3 |
| 12 | tuning | Calgary-Falconridge-Conrich | 46 | v2 | 29,685 | 7.0 | 0.94 | pass | 0.9985 | 5 |
| 45 | changed | Edmonton-South | 50 | v2 | 23,474 | 8.1 | 0.88 | pass | — | — |
| 29 | tuning | Edmonton-Beverly-Clareview | 56 | v2 | 32,215 | 6.4 | 0.86 | pass | 0.9992 | 3 |
| 49 | changed | Edmonton-Windermere | 56 | v2 | 16,352 | 23.9 | 0.85 | pass | — | — |
| 71 | changed | Lethbridge | 57 | v2 | 38,593 | 8.4 | 0.84 | pass | — | — |
| 88 | tuning | St. Albert | 57 | v2 | 21,615 | 6.4 | 0.85 | pass | 0.9992 | 4 |
| 15 | tuning | Calgary-Hays | 63 | v2 | 30,473 | 6.5 | 0.93 | pass | 0.9991 | 4 |
| 9 | tuning | Calgary-East | 68 | v2 | 30,230 | 7.2 | 0.93 | pass | 0.9987 | 5 |
| 38 | tuning | Edmonton-Manning | 97 | v2 | 23,951 | 7.7 | 0.85 | pass | 0.9991 | 5 |
| 65 | tuning | Grande Prairie | 112 | v2 | 21,230 | 7.7 | 0.86 | pass | 0.9993 | 4 |
| 69 | changed | Leduc-Beaumont | 114 | v2 | 23,597 | 5.9 | 0.92 | pass | — | — |
| 4 | changed | Calgary-Bow-Springbank | 119 | v2 | 45,266 | 5.7 | 0.94 | pass | — | — |
| 42 | changed | Edmonton-Nisku | 128 | v2 | 41,205 | 5.8 | 0.92 | pass | — | — |
| 28 | changed | Calgary-West-Springbank | 165 | v2 | 34,401 | 6.4 | 0.90 | pass | — | — |
| 87 | changed | Spruce Grove | 283 | v2 | 28,023 | 5.4 | 0.94 | pass | — | — |
| 58 | changed | Cochrane | 564 | v2 | 29,031 | 6.3 | 0.92 | pass | — | — |
| 80 | changed | Okotoks | 1,213 | v2 | 15,600 | 8.9 | 0.78 | pass | — | — |
| 79 | changed | Morinville-Sturgeon | 2,182 | municipalities | 17,175 | 8.2 | 0.88 | pass | — | — |
| 54 | changed | Blackfalds-Innisfail | 3,557 | municipalities | 18,989 | 8.4 | 0.88 | pass | — | — |
| 68 | changed | Lacombe-Sylvan Lake | 3,882 | municipalities | 27,078 | 9.0 | 0.87 | pass | — | — |
| 67 | changed | Lac Ste. Anne | 4,319 | municipalities | 15,077 | 8.7 | 0.81 | pass | — | — |
| 72 | changed | Lethbridge-Cardston | 5,432 | municipalities | 11,915 | 8.0 | 0.92 | pass | — | — |
| 91 | changed | Wetaskiwin-Ponoka | 6,138 | municipalities | 35,340 | 9.8 | 0.84 | pass | — | — |
| 60 | changed | Drayton Valley-Devon | 6,256 | municipalities | 25,687 | 9.5 | 0.78 | pass | — | — |
| 73 | changed | Lethbridge-Little Bow | 8,428 | municipalities | 30,791 | 10.0 | 0.82 | pass | — | — |
| 81 | changed | Olds-Didsbury-Three Hills | 10,339 | municipalities | 34,719 | 9.2 | 0.85 | pass | — | — |
| 52 | changed | Banff-Canmore-Diamond Valley | 11,483 | municipalities | 15,027 | 9.9 | 0.89 | pass | — | — |
| 76 | changed | Macleod-Crowsnest | 13,380 | municipalities | 9,363 | 29.6 | 0.72 | pass | — | — |
| 53 | changed | Barrhead-Westlock-Athabasca | 15,750 | municipalities | 31,229 | 10.8 | 0.87 | pass | — | — |
| 74 | changed | Lethbridge-Taber-Warner | 16,957 | municipalities | 32,581 | 12.4 | 0.73 | pass | — | — |
| 85 | changed | Rocky Mountain House-Sundre | 25,122 | municipalities | 17,409 | 10.8 | 0.93 | pass | — | — |
| 62 | changed | Fort McMurray-Lac La Biche | 32,317 | municipalities | 10,383 | 11.8 | 0.89 | pass | — | — |
| 61 | changed | Drumheller-Stettler | 38,398 | municipalities | 53,806 | 12.9 | 0.81 | pass | — | — |
| 90 | changed | West Yellowhead | 49,405 | municipalities | 13,109 | 12.6 | 0.93 | pass | — | — |
| 63 | changed | Fort McMurray-Wood Buffalo | 86,353 | municipalities | 363 | 15.8 | 0.99 | **fails** | — | — |

Sources: `findings/a9_stepb_v3_dev/results.json`.

## Checks

- **The repository module reproduces the development runs.** Most development runs used a working copy of the procedure. Before the rotation snap, the repository module gave the same transform to the last digit on Lethbridge-Cardston (72) and Lac Ste. Anne (67), both with a municipal prior, and on Cochrane (58), with a version 2 prior.
  - The snap changes only 3-match priors, which in development are Lac Ste. Anne and Wood Buffalo. Both were rerun with the final module, and their rows above are from that run. Lac Ste. Anne moved 0.03 m.
  - The exact registered code path was then run on non-sample pages: the scorer wrapper's patch, `reconstruct()` with its acceptance rule, and the diagnostics record (`smoke_test.txt`). It returned Calgary-Buffalo (5) and Lac Ste. Anne with the development transforms, and rejected Wood Buffalo under the rule.
- **How close to exact.** On the 24 placed changed pages checked (`va_risk.txt`), 10 of 1,309 voting-area points (0.8%) lie within 30 m of the reconstructed boundary. With the fits' median error of 5 to 30 m, misassignment of placed pages should stay near 1%. Unplaceable pages are the main risk to T1.
- **What the outlines follow.** On 18 placed pages, 53% to 100% of the outline lies within 40 m of a road, a census-subdivision boundary or a 2026 voting-area boundary (`outline_sources.txt`); 15 of the 18 are at 87% or more. The mountain pages score lowest, because they follow watersheds and rivers: Macleod-Crowsnest 53%, Banff-Canmore-Diamond Valley 68% and Rocky Mountain House-Sundre 71%. Outlines were not snapped to these lines; version 3 uses the page's own outline.
- **Environment.** Python 3.12.13 with PyMuPDF 2.1 (`environment.txt`). See `findings/a9_stepb_v2_development.md` for why it must be pinned.

## Limits, stated before the run

- **No rural page has truth.** Every tuning district is urban or small (at most 29 m per point). Rural evidence is fit quality only, and the sample run is the first test of rural pages against official geometry.
- **Northern pages with few municipalities are the weak case.** The sample includes Peace River, Lesser Slave Lake and Central Peace-Notley, which together hold 164 of its 1,909 VAs (8.6%). Their pages were not opened. They are expected to name more towns than Wood Buffalo's page does, but if two or more fail like it, T1 is unlikely to pass.
