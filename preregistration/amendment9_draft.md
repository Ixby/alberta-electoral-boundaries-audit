## Amendment 9 — A second calibration attempt, with a procedure that reads rural pages

> **Status: in force.** Written 2026-11-03 (Alberta time). At the time of writing:
> - Amendment 7's calibration had been run once and had failed (`findings/a7_stepb_calibration.md`, commit `d1f7a06a`).
> - No reconstruction of a changed district had been scored, and no geometry of the panel's map had been scored on any measure.
> - No official shapefile had been released.
>
> The author directed the second attempt in session ("Prep, file osf, run"; then "A" and "File when ready and continue") on learning that the shapefiles may be months away. Signed 2026-11-03. It is filed as an update to registration 9wp5y. No threshold changes.

**Why.**
- The first procedure placed every city page it could read almost exactly (18 pages: IoU 0.996 to 1.000; 7 of 981 VAs misassigned). It could not read rural pages, and it failed both gates: 49.0% of VAs misassigned against a 10% limit, and an EG delta of −2.16 points against 0.5.
- A second procedure, version 2, was built and tested in development but never run on the sample. It placed the city pages, but only 1 of the 10 changed pages over 10,000 km² (`findings/a9_stepb_v2_development.md`). That draft was not filed.
- Development then found why rural pages fail, and version 3 fixes it.
- The shapefiles are expected only after the bill passes. Amendment 7's calibration is the only route to any numeric reading before then.

**Part 1: The first result stands.** Amendment 7's calibration failed, and that result stays on the record. This amendment registers one further attempt, under the same gates, on the same sample, before it is run. If it fails, there is no third attempt under this amendment.

**Part 2: What is known before the second run.** The second attempt is not blind. These are the limits on what was seen:
- *Seen.* Which sample pages the first procedure could not place, and why. The first run's per-district scores (`findings/a7_stepb_calibration.json`).
- *Not seen.* No sample page was opened while versions 2 and 3 were built. Every development run refused sample districts in code.
- *Development data.* The 22 tuning districts, with their official geometry. The pages of the 35 changed districts, which have no official geometry and so cannot leak it.
- *No rural page has truth.* Every tuning district is urban or small: no tuning page is drawn at more than 29 m per point. Version 3's rural evidence is fit quality only, meaning how closely each page's own lines fall on the reference datasets once placed. The sample run is the first test of rural pages against official geometry.
- *Every unchanged district is already used.* The 56 are the 22 tuning districts and the 34-district sample. No fresh sample exists, so the second attempt reuses the fixed one.

**Part 3: The version 3 procedure.**
- *Code.* `analysis/scripts/a9_stepb_reconstruct_v3.py`, SHA-256 `c49f935e162aecb39c16bb5625d2c9863f48713c6849b2abb834ac333f04c0f0`, commit `08ae272f`.
  - It uses version 2 (`a9_stepb_reconstruct_v2.py`, SHA-256 `c148a5289d843aefb709feae42d75554a4f0e19b6e47d9d87a28467949b4f4f9`) for the outline, the reference layers, the road search and the refinement.
  - Version 2 uses version 1's helpers. Its docstring lists every change.
- *What development found.*
  - Rural pages draw their lines in other styles. The dark-grey 0.92-pt strokes are the full road network, and the light-grey 0.37-pt strokes are the township survey grid. Rules set on city pages matched each against the wrong reference.
  - Prairie roads lie on a one-mile grid, so a road search alone finds near-equal placements a whole number of miles apart.
- *What changed from version 2, and only this:*
  1. *A prior from the page's municipalities.* Village dots, town areas and First Nations reserve areas are matched by name to the 2021 census subdivisions. They are fitted to the subdivisions' centroids: two-point RANSAC with a fixed seed, then least squares. The prior is used when its rotation is within 1° of a right angle and it has either
     - at least 4 inliers, with a scale within 10% of the stated-area scale; or
     - exactly 3 inliers, with a scale within 1.5% and a median residual under max(150 m, 1 point).

     Otherwise version 2's road search, unchanged, supplies the prior.
  2. *Layer identification on each page.* Each grey stroke style is assigned to the reference it matches best within the prior's error: roads (National Road Network plus OpenStreetMap highways) or census-subdivision boundaries. A style matching neither in at least half its points is not used.
  3. *Local refinement.* The search is restricted to the prior's error (municipal prior: max(500 m, 2 × the median residual); version 2 prior: 1,500 m), followed by version 2's robust ICP. If that pass finds no usable layer or no local match, one wide retry runs: an error of max(5,000 m, 3 × the first), a scale within ±1%, and a layer threshold of 40%.
  4. *An acceptance rule, applied before any polygon is returned.* The matched page lines must lie a median of at most 40 m from their references, with at least 60% of them within 60 m. A page that fails the rule counts as a failure. The area check alone cannot do this: the scale is fixed from the stated area, so a wrong placement still passes it.
- *References.*
  - Statistics Canada National Road Network, Alberta, edition 17.0: `data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg`, SHA-256 `bb6d1396a62b9cbb0ce5c3b05c88ad9d432753847f392728dc933b6e8b5988f4`. It is built by `analysis/scripts/build_nrn_extract.py` from `nrn_rrn_ab_GPKG.zip` (SHA-256 `0dfd3afc922f12b870a231bddd359d3430a5b66e04e283131c614f0b38aacf9a`), and contains information licensed under the Open Government Licence – Canada.
  - Statistics Canada 2021 census subdivisions: `data/shapefiles/reference/alberta_2021_csds.gpkg`, SHA-256 `7ee3356b6e5c828db1e016cd96f101bfd0cbc67d8b3f87e429f2316430a4d840`.
  - The OpenStreetMap highways used before: `data/osm/alberta_osm_highways.gpkg`, SHA-256 `d8100044b0f38935bd7ccd539e3f21fb7118bea018d9cfb5827acbad324eacc9`.
  - The panel's report: the high-resolution PDF named in Amendment 7 (SHA-256 `d8ae78ab…a75122`).
- *Environment, pinned.* Python 3.12.13 with PyMuPDF 2.1 (MuPDF 1.28.6). The full package list is in `findings/a9_stepb_v3_dev/environment.txt`. Results depend on the PDF library: PyMuPDF 1.27.2.2 reads the outline stroke without a width on 9 of the 57 development pages. The scorer refuses to run under any other PyMuPDF version.
- *Development results* (`findings/a9_stepb_v3_development.md`):
  - *Tuning districts (official geometry).* All 22 are accepted, at IoU 0.9975 to 0.9996 with boundary error (Hausdorff) of 1 to 6 m.
  - *Changed districts (no geometry, fit quality only).* 34 of 35 are accepted:
    - all 16 under 1,000 km²;
    - all 9 of 1,000 to 10,000 km²;
    - 9 of the 10 over 10,000 km².

    Accepted pages' lines lie a median of 5.4 to 29.6 m from their references, with 72% to 96% within 60 m.
  - *The one failure* is Fort McMurray-Wood Buffalo, whose page names only six First Nations reserves. Its best fit (a median of 182 m, 24% within 60 m) is rejected by the acceptance rule.
  - *VAs near a boundary.* On 24 placed changed pages, 10 of 1,309 VA points (0.8%) lie within 30 m of the reconstructed boundary.
  - *The known risk.* Northern pages with few municipalities are the weak case. The sample's Peace River, Lesser Slave Lake and Central Peace-Notley hold 8.6% of its VAs, and their pages were not opened.

**Part 4: The second run.**
- *Scorer.* `analysis/scripts/a9_stepb_calibrate.py`, SHA-256 `10b37af062bfef993fbb8e00e6aecd9e63cb73261f94201f3106193d33531c07`. It substitutes version 3 into the frozen Amendment 7 scorer `a7_stepb_calibrate.py`, which is unchanged, and records version 3's fit diagnostics for each district.
- *Gates.* T1 (VA misassignment at most 10%) and T4 (province-wide EG delta under 0.5 points), as in Amendment 7. T2, T3 and IoU are reported beside them.
- *Rules.* Those of `findings/a7_stepb_calibration_protocol.md`, unchanged. A page the procedure cannot place, or that fails the acceptance rule, counts against both gates.
- *Running it.* It is run once, after this amendment is filed. The result is committed, pass or fail, before any changed district is scored.

**Part 5: If it passes.** Amendment 7, Part 3, Step C applies unchanged.
- The changed districts are reconstructed with version 3 and combined with the unchanged districts' official geometry.
- Each changed district must pass the 5% population check.
- A page that version 3 cannot place, or that fails the acceptance rule, is not used, and any measure that depends on it is not scored.
- R1 and R2 (Amendment 8) depend on every district. They are scored provisionally only if every changed district is used. Amendment 8, Part 5's rerun rule then applies, with the reconstruction in place of the enacted map.
- The reading is labelled provisional, carries this calibration's measured error, and is kept out of the headline.
- *Voting areas cut.* With the provisional map, and again on the official shapefiles, the audit lists the Elections Alberta voting areas (2023 and 2026 sets) that the map's boundaries cut.
  - The list uses `analysis/scripts/va_bisection.py`. A VA is cut when more than 1% of its area, and more than 0.01 km², lies outside its main district. This rule finds no cuts on the 2019 map.
  - The list is descriptive, not a test. Baselines: the commission majority map cuts 229 of the 4,904 2026 voting areas, and the minority map 364.
  - For the provisional map, a cut within this calibration's measured boundary error is marked as uncertain.

**Part 6: If it fails.** No numeric reading is published before the official shapefiles. The result is published with the reason.

**Part 7: What this does not change.** The headline remains the official shapefiles. No threshold changes.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-03 (Alberta time)
