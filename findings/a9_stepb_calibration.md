# Amendment 9, Step B: the second calibration result: **fails**

Version 3 of the reconstruction procedure was run once, on 2026-11-03, on the fixed 34-district sample, under Amendment 9 and the rules of `findings/a7_stepb_calibration_protocol.md`.
- Procedure SHA-256 `0b9d07c1…feace62`; scorer `3c470b99…285fda`; frozen Amendment 7 scorer `e3e1340c…59f6`.
- All inputs were re-hashed against the filed values before the run.
- Environment: Python 3.12.13 and PyMuPDF 2.1, as pinned.
- The run started at 11:45 AM MST, wrote its result at 3:22 PM, and was not interrupted.
- Raw output: `findings/a9_stepb_calibration.json`. Run log: `findings/a9_stepb_calibration_run.txt`.

| Gate | Result | Threshold | |
|---|---|---|---|
| T1: VA misassignment | 264 of 1,909 = **13.8%** | at most 10% | **fails** |
| T4: province-wide EG delta | +0.10% → +0.90%, **+0.80 points** | less than 0.5 points | **fails** |
| T2: mean absolute area error (31 placed) | 0.04% | reference < 10% | |
| T3: mean Hausdorff distance (31 placed) | 0.56 km | reference < 5 km | |
| Mean IoU (31 placed) | 0.967 | reference ≥ 0.65 | |

**Under Amendment 9, Part 6, no numeric reading of the panel's map is published before the official shapefiles. Step C does not run, and there is no third attempt.** Amendment 7's failed first calibration also stands.

## Where the 264 misassigned VAs come from

| Cause | Districts | VAs |
|---|---|---|
| Not placed: no local match within the prior's error | Chestermere-Strathmore, Grande Prairie-Wapiti | 47 + 69 |
| Not placed: rejected by the acceptance rule (median 100.7 m, 36% within 60 m) | Peace River | 60 |
| **Placed wrongly, and accepted** | Sherwood Park | 51 |
| Knock-on: VAs of correctly placed districts that fall inside the wrong Sherwood Park reconstruction | Edmonton-City Centre 30, Edmonton-Glenora-Riverview 4, Edmonton-Gold Bar 3 | 37 |
| **Total** | | **264** |

**Sherwood Park is the decisive failure.**
- Its page took version 2's road search as the prior, because it names no matchable municipality. That search chose a placement rotated 90° and 13.5 km off, over north-central Edmonton.
- The fit then passed the acceptance rule: 28,066 matched points, a median of 23.1 m, 85% within 60 m. Edmonton's road grid looks much the same after a quarter turn.
- Its fitted rotation was 89.85°, 0.15° off a right angle. Every correct placement in the run lies within 0.012°. In development, though, accepted pages range up to 0.14° off, so a rotation check set from development would not have caught it cleanly.
- The development pages more than 0.012° off are the three changed city pages whose version 2 prior was ambiguous: Calgary-North West-Bearspaw (0.14°), Edmonton-Meadows (0.10°) and Edmonton-Windermere (0.08°). They have no truth. After this result, they should be presumed possibly misplaced in the same way.
- Version 2's own lock statistics for it were weak (wide_z 2.7, no runner-up recorded). The rule did not use them.

This is a reading of the failure, not a revised result. Without the Sherwood Park misplacement and its knock-on, the misassigned share would have been 176 of 1,909 (9.2%). Every other misassigned VA belongs to a page the procedure correctly declined to place. The registered result is the one above, and it fails.

## What worked

The 30 districts placed correctly match their official geometry at IoU 0.9981 to 0.9998:
- **Urban pages** (Calgary, Edmonton, Red Deer-North): IoU 0.9981 to 0.9996, Hausdorff 1 to 5 m.
- **Rural and large districts: this is the first test of rural pages against official geometry, because no tuning district was rural.**
  - Ten such pages placed at IoU 0.9996 to 0.9998: Camrose, Central Peace-Notley, Cold Lake-Bonnyville-St. Paul, Fort Saskatchewan-Vegreville, Lesser Slave Lake, Lloydminster-Wainwright, Medicine Hat-Brooks, Medicine Hat-Cypress, Strathcona-Sherwood Park and Airdrie-West.
  - Version 1 failed on all ten: it could not place eight and placed the other two wrongly.
  - Airdrie-East, which version 1 also could not place, placed at IoU 0.9992.
  - Hausdorff distances on rural pages run to 376 m (Medicine Hat-Cypress). At those scales one drawn point covers 200 m or more.

The acceptance rule did its job on Peace River, which it declined. It failed on Sherwood Park, which it accepted.

## A recording gap, disclosed

The scorer wrapper records version 3's diagnostics only after `georeference()` returns. So Chestermere-Strathmore and Grande Prairie-Wapiti, which raised inside it ("no local match within the prior's error"), have no recorded prior source or fit statistics. Their error messages are in the result file. Separately, the frozen scorer's progress line prints `inlier30`, which version 3 does not set, so the run log shows 0.000 for every placed page. The real fit statistics are under `v3_diagnostics`. Neither gap changes a gate.

## What follows

- No numeric reading of the panel's map is published before the official shapefiles (Amendment 9, Part 6). R1 and R2 (Amendment 8) are not scored provisionally.
- The headline remains the official shapefiles. They are scored within 72 hours of release, as registered.
- The voting-area cut list (Amendment 9, Part 5) is made only on the official shapefiles.
- The procedure stays in the repository as developed. Its rural placements, checked against truth here for the first time, are recorded above, beside its failures.

## Post-hoc: would a fit-together check have caught it?

Districts fit together like puzzle pieces, so a correct reconstruction should not overlap the official geometry of districts known to be its neighbours. This was checked after the run, when the sample was already spent, so it is a diagnosis and not a result (`findings/a9_stepb_v3_dev/posthoc_fit_together.txt`; code `posthoc_fit_together.py`). For each placed sample district it measures the share of the reconstruction's area that overlaps two things:
1. the official geometry of the 22 non-sample tuning districts, which the procedure is allowed to know;
2. the other placed reconstructions.

- **Every correct placement** overlaps the tuning districts by at most 0.074% of its area.
- **Sherwood Park overlaps them by 82.8%.**
- Among the reconstructions, the only overlaps above 0.3% are Sherwood Park and the three Edmonton districts it lands on: City Centre 64.7%, Glenora-Riverview 3.9% and Gold Bar 2.4%.

A rule rejecting a placement that overlaps known official districts by more than 1% would have caught the wrong acceptance with a wide margin, and rejected nothing else. The registered result does not change.
