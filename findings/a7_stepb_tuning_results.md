# Step B tuning results (Amendment 7)

*Copied into the repository on 2026-11-03 from the working folder it was written in; the paths below are that folder. The frozen procedure is `analysis/scripts/a7_stepb_reconstruct.py` (identical apart from its two file paths and its docstring); the run's rules are in `findings/a7_stepb_calibration_protocol.md`.*

Procedure: `C:/Users/email/AppData/Local/Temp/ceb/stepb/reconstruct.py` (`reconstruct(ed_number, window=None)`; CLI `python reconstruct.py 3 5 ...`).
Evaluation: `evaluate.py` (official geometry loaded only via `truth.py`, filtered to the 22 tuning EDs at read time). Raw per-ED output: `results.json`; log `eval_final.log`.
Final code = prior-free version (no stated-area prior). All 22 rows come from this code. (Afterwards only the no-CSD-hit branch changed, to raise an error / accept `window=`; ED 5 and 65 were re-run and are identical.) The earlier area-prior version, with equally good results, is kept as `reconstruct_v1_area_prior.py` / `results_v1_area_prior.json`.

## Per-district results (tuning set, n = 22)

| ED | District | IoU | Area err % | Hausdorff km | VA mis (n/N) | VA mis % | rot deg | scale m/pt | road-pt inliers<30m |
|---|---|---|---|---|---|---|---|---|---|
| 3 | Calgary-Bhullar-McCall | 0.9992 | +0.023 | 0.0023 | 0/27 | 0.0 | 270.00 | 15.723 | 0.975 |
| 5 | Calgary-Buffalo | 0.9984 | -0.024 | 0.0015 | 0/45 | 0.0 | 269.99 | 4.505 | 0.932 |
| 7 | Calgary-Cross | 0.9988 | -0.091 | 0.0033 | 0/50 | 0.0 | 270.00 | 9.199 | 0.952 |
| 9 | Calgary-East | 0.9992 | +0.019 | 0.0034 | 0/63 | 0.0 | 0.00 | 19.174 | 0.895 |
| 12 | Calgary-Falconridge-Conrich | 0.9988 | -0.091 | 0.0034 | 0/37 | 0.0 | 270.00 | 16.099 | 0.911 |
| 15 | Calgary-Hays | 0.9990 | +0.004 | 0.0038 | 0/40 | 0.0 | 359.99 | 18.023 | 0.933 |
| 16 | Calgary-Klein | 0.9992 | +0.020 | 0.0027 | 0/50 | 0.0 | 270.00 | 15.626 | 0.923 |
| 17 | Calgary-Lougheed | 0.9987 | -0.093 | 0.0062 | 0/51 | 0.0 | 270.00 | 18.029 | 0.897 |
| 19 | Calgary-Mountain View | 0.9988 | +0.021 | 0.0021 | 0/66 | 0.0 | 270.00 | 12.272 | 0.883 |
| 20 | Calgary-North | 0.9985 | -0.012 | 0.0030 | 0/39 | 0.0 | 0.00 | 13.804 | 0.922 |
| 21 | Calgary-North East | 0.9989 | -0.012 | 0.0029 | 0/23 | 0.0 | 270.03 | 12.270 | 0.950 |
| 23 | Calgary-Nose Creek | 0.9992 | -0.020 | 0.0027 | 0/38 | 0.0 | 0.01 | 16.104 | 0.924 |
| 24 | Calgary-Shaw | 0.9996 | +0.018 | 0.0018 | 0/47 | 0.0 | 269.99 | 14.189 | 0.906 |
| 25 | Calgary-South East | 0.9983 | +0.094 | 0.0062 | 0/36 | 0.0 | 270.00 | 15.346 | 0.907 |
| 29 | Edmonton-Beverly-Clareview | 0.9993 | +0.001 | 0.0027 | 0/53 | 0.0 | 270.00 | 19.173 | 0.928 |
| 30 | Edmonton-Castle Downs | 0.9988 | -0.013 | 0.0026 | 0/50 | 0.0 | 269.99 | 11.503 | 0.975 |
| 32 | Edmonton-Decore | 0.9990 | +0.041 | 0.0023 | 0/53 | 0.0 | 0.00 | 9.588 | 0.979 |
| 37 | Edmonton-Highlands-Norwood | 0.9990 | -0.006 | 0.0018 | 0/47 | 0.0 | 270.00 | 10.353 | 0.943 |
| 38 | Edmonton-Manning | 0.9996 | +0.001 | 0.0025 | 0/47 | 0.0 | 0.00 | 22.760 | 0.942 |
| 43 | Edmonton-North West | 0.9992 | +0.005 | 0.0020 | 0/49 | 0.0 | 270.00 | 16.602 | 0.980 |
| 65 | Grande Prairie | 0.9992 | +0.060 | 0.0043 | 0/45 | 0.0 | 0.01 | 28.767 | 0.970 |
| 88 | St. Albert | 0.9996 | +0.018 | 0.0032 | 0/63 | 0.0 | 0.00 | 20.990 | 0.989 |

N districts = 22; mean IoU = 0.9990; mean |area err| = 0.031%; mean Hausdorff = 0.0030 km; min IoU = 0.9983; max Hausdorff = 0.0062 km; overall VA misassignment = 0/1019 = 0.00% (mean per-district 0.00%)


## Gates (registration reference)

| Gate | Threshold | Result | Pass |
|---|---|---|---|
| VA misassignment | <= 10% | 0.00% (0 of 1019 VAs) | yes |
| Mean area error | < 10% | 0.031% (mean absolute) | yes |
| Mean Hausdorff | < 5 km | 0.0030 km (max 0.0062 km) | yes |
| Mean IoU | >= 65% | 99.90% (min 99.83%) | yes |

VA misassignment: VAs from va_2023_election_day_votes.gpkg, read with a bbox around union(reconstruction, official)+2 km, assigned by `representative_point()`; misassigned = in exactly one of {reconstruction, official}; % = misassigned / VAs in the official district. The overall % pools the 22 districts. (Official geometry is 2026, VAs are 2023, so a VA straddling a boundary is possible; none was misassigned.)

## Why the result is this tight, and what the procedure does

The panel's page outline is a vector copy of the boundary, so shape error is nil once the page is placed; the whole problem is the page -> EPSG:3400 transform. Measured on tuning pages (diagnostic outline->official fits on tuning EDs only; never used as control inside the procedure):
* The page map is 10-TM-compatible, north-up, uniform scale: **no shear and no projective term needed**; free-rotation fits gave 0 or exactly 270 deg (+/-0.03), median residual 2-9 m.
* **Pages are rotated by exact multiples of 90 deg** (most Calgary/Edmonton pages 270, others 0). A theta=0-only search fails on those.

Pipeline (control = labelled arterial roads vs OSM highways, plus CSD names only to pick the search window; no ED geometry; no stated area):
1. `extract_page`: pymupdf `get_drawings()` on page index 214+n. Outline = stroke (type `s` or `fs`) of width 2.76 +/-0.05 with reddish colour (r > g+0.2 and r > b+0.2; (0.61,0.25,0.17) on all 22 pages). Main-map linework = drawings painted BEFORE the outline in z-order (the inset locator map and labels are painted after, so they never pollute matching). Arterial strokes = type `s`, colour (0.70,0.70,0.70) +/-0.02, width 0.88-1.45 pt. Title = the page's own Arial-Bold red #93241A label.
2. Outline polygon: union of drawn paths -> polygonize -> keep faces with odd even-odd parity against the path (handles self-touching outlines, which made a plain shapely `Polygon` invalid on EDs 29/88).
3. Search window: CSDs (alberta_2021_csds.gpkg) whose name is a whole-token match in the page text. Anchor = CSD(s) named in the red title (e.g. "Calgary" for Calgary-Buffalo); keep only hits within 25 km of the anchor (drops spurious far matches such as Lacombe/Lakeview/Vegreville that the first version let in); window = envelope + 6 km. No anchor -> densest cluster of hits. No hits at all -> raise a clear error unless the caller passes `window=` (whole-province scanning is deliberately not attempted).
4. Wide stage, prior-free: OSM-highway proximity field exp(-d/150 m) on a 100 m grid (resolution coarsened so the grid is <= 25 M cells); log-spaced scale 3-40 m/pt in 8% steps x theta {0,90,180,270}; FFT cross-correlation of the rasterised page arterials with the field; score = z-score of the correlation peak ((peak - mean)/std over translations). Raw mean proximity prefers tiny scales dropped into dense road networks; the z-score removes that (verified on EDs 3, 5, 7, 65).
5. Top 6 distinct wide candidates each get a local fine search (scale +/-7% in 15 steps, 25 m grid, sigma 60 m) and a robust two-way ICP over (s, theta, tx, ty): soft-L1 (f_scale 10 m), page->OSM and OSM->page nearest-neighbour residuals, radii annealed 120/60/30/15 m x 3 iterations, soft priors (scale 4% about the fine-search scale; rotation 0.5 deg). Winner = highest fraction of page arterial points within 30 m of OSM (`inlier30`; tuning winners 0.88-0.99; runner-ups 0.45-0.89 or converge to the same solution).
6. Apply the transform to the outline polygon (holes kept).

The stated area_km2 (stated_populations.csv) is computed only as an agreement diagnostic (`s_area`); the recovered scale differs from it by <= 2.5% (largest on ED 5, 4 km2). It is not used by the algorithm.

## Parameters (all)
road colour (0.7,0.7,0.7) +/-0.02, width 0.88-1.45 pt; outline width 2.76 +/-0.05 reddish; page sampling 3 pt; OSM sampling 15 m; CSD anchor cluster 25 km; window buffer 6 km; wide scales 3-40 m/pt step 8% (log); angles 0/90/180/270; wide grid 100 m, sigma 150 m, max 25e6 cells; fine grid 25 m, sigma 60 m, scale +/-7% x 15; candidates 6; ICP radii (120,60,30,15), 3 iterations each, f_scale 10 m, scale prior 4%, rotation prior 0.5 deg. Determinism: no RNG anywhere; `reconstruct(5)` called twice returned byte-identical WKB (checked).

## What failed / what I had to fix
* theta fixed at 0 (first design): Calgary p3 and Edmonton p29 gave coarse score ~0.40 and IoU 0.0 (page rotated 270 deg). Fixed by the 4-angle search.
* First version used the stated area as the scale prior (worked, same IoUs) but that is not map-derived control; replaced by the prior-free wide search. The raw (non-z-scored) wide search picked tiny scales on ED 3 (IoU 0.0); z-scoring fixed it. On ED 5 the z margin is thin (4.9 vs 4.6), hence top-6 candidates + ICP-inlier selection.
* Window = envelope of all CSD-name hits let distant spurious hits through (ED 88 matched Lacombe, ED 38 Vegreville). Fixed with title anchor + 25 km cluster. The whole-province fallback was impractical (OSM densification for the province ran for minutes with growing memory), so it now raises an explicit error instead.
* ED 20: outline painted as stroke+fill (`fs`), not `s`; fixed. ED 38: page widths are 0.93/1.39 rather than 0.92/1.38, so an exact-match road filter found nothing; fixed with a tolerance band.
* The documented outline colour (0.43,0.38,0.29) is NOT the outline on these pages ((0.61,0.25,0.17) is); (0.43,0.38,0.29) 2.76-pt strokes appear on ED 88 as other linework. A held-out page whose outline lacks a reddish 2.76-pt stroke makes the code raise "no outline stroke found" rather than guess.
* Diagnostics (tuning only): centroid-aligned overlays and an unconstrained outline->official fit hit degenerate minima until rotation was started from a grid of angles and scale pinned.
* Grey (0.8) fill pieces are clipped to the frame and split into many drawings, so they were not used to build the polygon. Not needed or used: road-name text, rivers, CSD boundaries, projective fit.

## Caveats for the held-out application (untested)
* 20/22 tuning pages are Calgary/Edmonton; the rest are Grande Prairie and St. Albert. Rural pages (few arterials in the OSM highway layer, county-line-only content) are untested: there is no river/CSD-boundary stage. Check `last_info['inlier30']` (tuning 0.88-0.99) and `wide_z` (tuning 4.4+) and review pages that fall below.
* Page style drift (stroke colours/widths/paint type) already happened inside the tuning set (ED 20, ED 38); expect more on held-out pages.
* Rotations that are not multiples of 90 deg would need a wider angle list (ICP only absorbs ~0.5 deg).
* Leakage guard: `reconstruct()` refuses non-tuning EDs unless env `STEPB_ALLOW_ANY=1` (intended only for the post-calibration run).
* The `window=` override test on ED 65 (IoU 0.9992) used a window built from the official polygon; it only exercises the code path.

## Leakage confirmation
Only pages of the 22 tuning EDs were opened/extracted/rendered (ED 3, 5, 7, 9, 12, 15, 16, 17, 19, 20, 21, 23, 24, 25, 29, 30, 32, 37, 38, 43, 65, 88). Official geometry was read only via `truth.py`, filtered to the 22 tuning names right after reading. VAs were read only through per-district bbox windows for the metric, never as control. No held-out/sample/changed-district page or geometry was touched (`sample.json` / `select_sample.py`, already in the folder, were not opened).
