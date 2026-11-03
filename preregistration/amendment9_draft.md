## Amendment 9 — A second calibration attempt, with a procedure that can read rural pages

> **Status: NOT FILED, and on hold.** Development showed that version 2 does not place most rural pages (`findings/a9_stepb_v2_development.md`), so filing it would spend the only sample on a known failure. The draft is kept as the record of what was prepared. Part 3 needs a fit-quality rejection rule, and Part 2 needs a statement that no rural page has truth, before any later version could be filed.
>
> Written 2026-11-03 (Alberta time). At the time of writing:
> - Amendment 7's calibration had been run once and had failed (`findings/a7_stepb_calibration.md`, commit `d1f7a06a`).
> - No reconstruction of a changed district had been made.
> - No geometry of the panel's map had been scored.
> - No official shapefile had been released.
> - The author directed the second attempt in session ("Prep, file osf, run"), on learning that the shapefiles may be months away.

**Why.**
- The first procedure placed every city page it could read almost exactly (18 pages: IoU 0.996 to 1.000, 7 of 981 VAs misassigned). It could not read rural pages, and it failed the gates: 49.0% of VAs misassigned against a 10% limit, and an EG delta of −2.16 points against 0.5.
- The failures had two causes:
  - The procedure matched only the city pages' arterial-road style. 12 rural and small-city pages had none.
  - It accepted the district outline only at 2.76 pt. One page draws it at another width, and three pages fell back to the small locator map's outline.
- The shapefiles are expected only after the bill passes, which may be months away. Amendment 7's calibration is the only route to any numeric reading before then.

**Part 1: The first result stands.** Amendment 7's calibration failed, and that result stays on the record. This amendment registers one further attempt, under the same gates, on the same sample, before it is run. If the second attempt also fails, there is no third under this amendment.

**Part 2: What is known before the second run.** The second attempt is not blind, and these are the limits on what was seen:
- *Seen:* which sample pages the first procedure could not place, and why (no strokes of the expected style, or no outline in the expected style); and the first run's per-district scores (`findings/a7_stepb_calibration.json`).
- *Not seen:* no sample page was opened while version 2 was built.
- *Development data:*
  - the 22 tuning districts, with their official geometry, as before;
  - the pages of the 35 changed districts, which have no official geometry and so cannot leak it.

  Layer semantics were established on tuning pages only. For example, the medium-grey 0.92-pt strokes are census-subdivision boundaries: 71–87% of their points lie within 60 m of a 2021 CSD boundary.
- *Every unchanged district is already used.* The 56 are the 22 tuning districts and the 34-district sample. No fresh sample exists, so the second attempt reuses the fixed one.

**Part 3: The version 2 procedure.**
- *Code.* `analysis/scripts/a9_stepb_reconstruct_v2.py`, SHA-256 {V2_SHA}, commit {V2_COMMIT}. It reuses version 1's helpers unchanged, and its docstring lists every change.
- *What changed from version 1, and only this:*
  1. *Outline.* The page's own outline is the reddish stroke at least 2.0 pt wide with the largest extent.
  2. *Two matched layers, each against its own reference:*
     - roads (grey 0.70 strokes, 0.30–1.60 pt) against the Statistics Canada National Road Network, Alberta, edition 17.0, together with the OpenStreetMap highways used before;
     - municipal and county lines against the 2021 census-subdivision boundaries.
     The NRN extract is `data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg`, SHA-256 {NRN_SHA}, made from `nrn_rrn_ab_GPKG.zip`, SHA-256 `0dfd3afc…acf9a`. It contains information licensed under the Open Government Licence – Canada.
  3. *Scale from the panel's stated area (App. 7).* The search runs over ±15% of the scale at which the outline's area equals the stated area, and the chosen fit must give an area within 10% of it. A page with no such fit counts as a failure.
- *Development results* (`findings/a9_stepb_v2_development.md`):
  - {DEV_SUMMARY}

**Part 4: The second run.**
- *Scorer.* `analysis/scripts/a9_stepb_calibrate.py` (SHA-256 {CAL_SHA}). It substitutes version 2 into the frozen Amendment 7 scorer `a7_stepb_calibrate.py`, which is unchanged.
- *Gates.* T1 (VA misassignment at most 10%) and T4 (province-wide EG delta under 0.5 points), as in Amendment 7. T2, T3 and IoU are reported beside them.
- *Rules.* Those of `findings/a7_stepb_calibration_protocol.md`, unchanged. An unplaceable page counts against both gates.
- *Running it.* It is run once, after this amendment is filed. The result is committed, pass or fail, before any changed district is reconstructed.

**Part 5: If it passes.** Amendment 7, Part 3, Step C applies unchanged.
- The changed districts are reconstructed with version 2 and combined with the unchanged districts' official geometry.
- Each changed district must pass the 5% population check.
- Pages version 2 cannot place are not used, and any measure that depends on them is not scored. R1 and R2 (Amendment 8) depend on every district.
- The reading is labelled provisional, carries this calibration's measured error, and is kept out of the headline.
- *Voting areas cut.* With the provisional map, and again on the official shapefiles, the audit lists the Elections Alberta voting areas (2023 and 2026 sets) that the map's boundaries cut.
  - It uses `analysis/scripts/va_bisection.py`: a VA is cut when more than 1% of its area, and more than 0.01 km², lies outside its main district. The rule finds no cuts on the 2019 map.
  - The list is descriptive, not a test. Baselines: the commission majority map cuts 229 of the 4,904 2026 voting areas, and the minority map 364.
  - For the provisional map, a cut within this calibration's measured boundary error is marked as uncertain.

**Part 6: What this does not change.** The headline remains the official shapefiles. No threshold changes.
