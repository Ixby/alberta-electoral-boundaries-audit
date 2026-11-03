# Amendment 7, Step B: the calibration protocol (fixed before the run)

This file fixes how the single Step B run is scored. It is committed, with the procedure, before the procedure touches any sample page.

**Inputs, by SHA-256:**
- The procedure: `analysis/scripts/a7_stepb_reconstruct.py`. It is the tuning-set procedure (`findings/a7_stepb_tuning_results.md`) with two changes: its two file paths are now repository paths, and its docstring names it. No parameter changed.
- The scorer: `analysis/scripts/a7_stepb_calibrate.py`.
- The sample: `findings/a7_stepb_sample.json`, 34 districts, fixed on 2026-11-02 at about 21:30 MST.
- The panel's high-resolution PDF: `evidence/legislature/iap_report_2026_hires.pdf` (`d8ae78ab…75122`).
- The panel's App. 7 table, as transcribed at stage 1: `data/iap/iap_app7_populations.csv`. It is used only for the district names and, as a diagnostic, the stated areas.
- Official geometry: `data/shapefiles/canonical/ea_majority_2026_eds.gpkg`. Roads: `data/osm/alberta_osm_highways.gpkg`. Place names: `data/shapefiles/reference/alberta_2021_csds.gpkg`.

The SHA-256 values are in the commit message that adds this file.

**How the tuning went.** The procedure was built on the 22 unchanged districts outside the sample. On them:
- mean IoU was 0.9990;
- voting-area misassignment was 0 of 1,019;
- mean Hausdorff distance was 3 m.

20 of the 22 are Calgary or Edmonton pages, so rural pages are untested.

**What is scored** (Amendment 7, Part 3):

| | Rule | Pass |
|---|---|---|
| Voting areas | The canonical VA polygons (`mcmc_ensemble.build_va_graph`), each placed by its representative point | |
| T1: VA misassignment | A sample VA is one whose point lies in a sample district's official geometry. It is right when the point lies in that district's reconstruction and in no other sample district's reconstruction. If the procedure cannot place a page (it raises an error), every VA of that district counts as wrong. | at most 10% wrong |
| T4: efficiency-gap delta | Start from the commission majority map and put each sample reconstruction in place of its official district. Other districts lose any area a reconstruction covers. Where two reconstructions overlap, the lower ED number keeps the overlap. A district that could not be placed is left out, so its VAs fall in no district. The efficiency gap of that map (`score_exogenous_map`, 2023 election-day votes) is compared with the official map's. | less than 0.5 points |
| Reported beside the gates | T2 mean absolute area error, T3 mean Hausdorff distance, mean IoU, and the procedure's own fit diagnostics (`inlier30`, `wide_z`) for every district | not gates |

**A dry run of the scorer.** It used no reconstruction and no sample page. The official geometry stood in for every reconstruction, and one district (ED 2) was forced to fail.
- T1 counted only ED 2's 54 VAs as wrong, out of 1,909.
- T4 moved by −0.56 points, because ED 2's VAs fell out of the map.

So one unplaceable district is enough to fail T4 under these rules. That strictness is intended.

**After the run:**
- Nothing is tuned or corrected by hand. A page the procedure flags is reported, not fixed.
- Any later change to the procedure is disclosed with its rerun, and the first run stays the result.
- The result is committed and recorded in `findings/map_stages.md`, pass or fail, before any changed district is reconstructed.
