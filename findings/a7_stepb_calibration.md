# Amendment 7, Step B: the calibration result: **fails**

The procedure was run once, on 2026-11-03, on the fixed 34-district sample, under the rules fixed in `findings/a7_stepb_calibration_protocol.md` (procedure, scorer and inputs committed with their SHA-256 at `2a1aa42b`; corrected App. 7 hash at `273e3c88`). Raw output: `findings/a7_stepb_calibration.json`.

| Gate | Result | Threshold | |
|---|---|---|---|
| T1: VA misassignment | 935 of 1,909 = **49.0%** | at most 10% | **fails** |
| T4: province-wide EG delta | +0.10% → −2.06%, **−2.16 points** | less than 0.5 points | **fails** |
| T2: mean absolute area error (21 placed) | 14.2% | reference < 10% | |
| T3: mean Hausdorff distance (21 placed) | 6.09 km | reference < 5 km | |
| Mean IoU (21 placed) | 0.856 | reference ≥ 0.65 | |

**Under Amendment 7, Part 3, no numeric reading of the panel's map is published before the official shapefiles. Step C does not run.**

## Why it fails

The procedure placed 18 of the sample's 34 pages almost exactly, and failed on the other 16. It failed in three ways:

1. **12 rural and small-city pages could not be placed at all.** They are Airdrie-East, Camrose, Central Peace-Notley, Chestermere-Strathmore, Cold Lake-Bonnyville-St. Paul, Fort Saskatchewan-Vegreville, Grande Prairie-Wapiti, Lesser Slave Lake, Lloydminster-Wainwright, Medicine Hat-Brooks, Medicine Hat-Cypress and Peace River.
   - The error on each was `need at least one array to concatenate`. The page has none of the road strokes the procedure matches against OpenStreetMap: grey, 0.88 to 1.45 pt wide, the style of the city pages it was tuned on.
   - The tuning set held only 2 such pages (Grande Prairie and St. Albert), both cities. The tuning record warned that rural pages were untested.
2. **One page has no outline in the style the procedure looks for:** Edmonton-Glenora-Riverview. Its error was `no outline stroke found`.
3. **Three pages were placed wrongly:** Calgary-Glenmore-Tsuut'ina, Airdrie-West and Strathcona-Sherwood Park. Each had IoU 0.000, an area about 99.5% too small, and was 38 to 46 km off.
   - The procedure's own fit diagnostic flagged all three. Their `inlier30` values were 0.571, 0.523 and 0.346, against 0.875 to 1.000 on every page placed correctly and 0.88 to 0.99 on the tuning set.
   - The tiny areas suggest it took a small reddish stroke for the outline.

On the 18 pages it placed correctly (9 Calgary and 7 Edmonton districts, Red Deer-North and Sherwood Park), the result matches tuning: IoU 0.996 to 1.000 and Hausdorff distance under 10 m, with 7 of 981 VAs misassigned (1 in Calgary-Elbow, 6 in Edmonton-City Centre).

## What follows

- The result stands. Under the protocol, a later fix (rural road styles, a stricter outline test, a gate on `inlier30`) would be disclosed with its rerun, and this first run would remain the result.
- No partisan or structural number is computed on a reconstruction of the panel's map.
- The November map is scored on the official shapefiles, within 72 hours of their release (Amendment 7, Part 3).
- Stage 1 keeps its geometry-free grades (`findings/iap_stage1_part4.md`).
