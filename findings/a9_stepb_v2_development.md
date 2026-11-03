# Step B, version 2: development results, and why Amendment 9 was not filed

> Written 2026-11-03 (Alberta time). **Amendment 9 has not been filed, and the second calibration has not been run.** No sample page was opened. The 34-district sample is still unspent.

## What was tried

Version 2 of the reconstruction procedure (`analysis/scripts/a9_stepb_reconstruct_v2.py`) changed three things from version 1:
- it reads the page's own outline;
- it matches two layers, roads against the Statistics Canada National Road Network (Alberta, edition 17.0) plus OpenStreetMap highways, and municipal lines against the 2021 census-subdivision boundaries;
- it sets the scale from the panel's stated area.

It was evaluated on two groups:
- the tuning districts, against their official geometry;
- the 35 changed districts, which have no official geometry, so only the quality of the fit can be read.

Raw results are in `findings/a9_stepb_v2_dev/`. The page lists used are recorded there too. None of the 57 districts is in the sample (`findings/a7_stepb_sample.json`).

## Results

**Tuning districts (official geometry).** 20 of the 22 placed, at IoU 0.998 to 1.000 and boundary error (Hausdorff) of 1 to 5 m. The other two, Calgary-Bhullar-McCall (3) and Grande Prairie (65), found no fit consistent with the stated area under an earlier build of version 2. Their rerun on the final build is recorded in `findings/a9_stepb_v2_dev/`. Every tuning page has a scale below 23 m per point. **No tuning page is rural, so there is no truth-based evidence on rural pages at all.**

**Changed districts (no geometry).** Fit quality depends on the district's size:

| Stated area | Pages | What the fit shows |
|---|---|---|
| under 600 km² | 16 | 13 lock clearly. 3 are ambiguous: Edmonton-Meadows (40) and Edmonton-Windermere (49), where the runner-up scores the same, and Calgary-North West-Bearspaw (22), whose agreement score is low at 0.64. |
| 1,000 to 10,000 km² | 9 | 8 lock: a strong peak, with the runner-up far behind. Lethbridge-Cardston (72) does not. |
| over 10,000 km² | 10 | 1 locks (Olds-Didsbury-Three Hills, 81). 9 do not: the best and second-best fits are both poor and almost equal. |

The pages that do not lock are Banff-Canmore-Diamond Valley, Macleod-Crowsnest, Barrhead-Westlock-Athabasca, Lethbridge-Taber-Warner, Rocky Mountain House-Sundre, Fort McMurray-Lac La Biche, Drumheller-Stettler, West Yellowhead and Fort McMurray-Wood Buffalo.

"Locks" is a judgment from fit statistics, not a measured accuracy. The 30 m agreement score cannot be compared across scales: on a page at 400 m per point, 30 m is less than a tenth of a point.

## Why the second calibration would fail

T1 allows at most 10% of the sample's VAs to be misassigned, which is 190 of 1,909.
- The sample's eight districts over 10,000 km² hold 490 VAs (25.7%): Camrose, Lloydminster-Wainwright, Medicine Hat-Brooks, Grande Prairie-Wapiti, Cold Lake-Bonnyville-St. Paul, Central Peace-Notley, Lesser Slave Lake and Peace River.
- On changed pages of that size, version 2 locked once in ten.
- If it does as well on the sample, T1 fails on those districts alone, even if every other page places perfectly.

Amendment 9 allows no third attempt, so running it now would spend the only sample on a known failure.

## A flaw any version 3 must fix

The area check cannot catch a wrong placement. Every page that did not lock still passed it, at 0.93 to 1.00 of the stated area, because the scale is fixed from that area before the fit is made. Those pages would count as placed and feed into Step C.

A future procedure needs a rejection rule based on fit quality, registered before the run. Candidate measures are the margin over the runner-up and the strength of the correlation peak. Any registration must also say plainly that no rural page has truth.

## What has not changed

- Amendment 7's calibration failed, and that result stands (`findings/a7_stepb_calibration.md`).
- Step C does not run.
- The headline remains the official shapefiles.
