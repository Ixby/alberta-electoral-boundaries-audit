## Amendment 10 — A third attempt: the panel's map assembled like a puzzle and checked against every page, registered as a reproducibility run

> **Status: in force.** Written 2026-11-03 and 2026-11-04 (Alberta time). At the time of writing:
> - Amendment 7's calibration had failed (`findings/a7_stepb_calibration.md`), and so had Amendment 9's (`findings/a9_stepb_calibration.md`, commit `2da38dc0`).
> - No partisan or structural measure of the panel's map had been computed.
> - No enacted geometry existed. The only published district geometry is the commission's proposed map, which Elections Alberta released as a shapefile. The author reported that Elections Alberta could not release the panel's boundaries before the bill.
>
> The limit of one further attempt in Amendment 9, Part 1, was set by the session agent when drafting that amendment. It was not set by the author and is not required by the method. The author directed this attempt in session: "the limit of two is artificial and something you created arbitrarily. There's no reason this can't be done." {FILED_LINE}

**Why.**
- The second calibration placed 30 of the 34 sample pages at IoU 0.998 to 1.000. Ten of them were rural districts, the first rural pages ever checked against published geometry. It failed on one wrong acceptance: Sherwood Park, placed rotated 90° and 13.5 km off, over three Edmonton districts. That one placement cost 88 of the 264 misassigned voting areas.
- Districts fit together like puzzle pieces, and every page carries more than its own outline: its neighbours' boundaries, their numbers, and a locator map of the whole province. A correct piece must fit its neighbours, lie inside its own page and match its place on the locator map. The wrong Sherwood Park placement fails all three.
- For the panel's map, most pieces are known under one stated assumption: the 56 districts the panel reports unchanged from the commission's map, by name and stated population (Amendment 7, Step A), are taken at the commission's published geometry. Every voting area in the remaining territory then belongs to one of the 35 changed districts.

**Part 1: Amendment 9, Part 1, is superseded.** The sentence "If it fails, there is no third attempt under this amendment" is withdrawn. Both failed calibrations stay on the record. Any attempt after this one also needs its own amendment, filed before its run, stating what has been seen.

**Part 2: What has been seen, and what this run can and cannot show.** This attempt is not blind.
- *The sample is development data.* Every sample page has been reconstructed and compared with the commission's geometry. The rules in Part 3 were built on those results, and several were changed because of what they did to the sample's score:
  1. the conflict-count tie-break in rule 2, after a misplaced Edmonton-Meadows knocked out three correct sample districts (Edmonton-Glenora-Riverview, McClung and West Henday);
  2. the 25% area tolerance for hole claims, chosen over 15% partly because the sample scored 6.65% against 8.43%;
  3. scoping city labels to pages outside that city, and matching mutual claims by area, after Sherwood Park's and Windermere's holes were exchanged;
  4. pooling a district's title claims, after Chestermere-Strathmore's hole came in two parts;
  5. assigning voting areas by representative point, the audit's standing convention, which removed the last three wrongly assigned voting areas.

  The record of every iteration, with the sample score at each, is `findings/a10_stepb_development.md`.
- *The expected result is stated in advance.* The pipeline is deterministic. On the development fixture, which rebuilds every page from the second run's saved transforms, it assigns all 1,909 sample voting areas correctly (T1 0.0%) with an efficiency-gap delta of 0.00 points (T4), and passes every sanity item. The registered run reproduces that from the PDF with the frozen code. It is a reproducibility check of the frozen pipeline, not out-of-sample evidence about its accuracy.
- *Evidence that could not be tuned.* The changed districts have no published geometry, so nothing in development could fit them to truth. Their evidence is internal consistency between independent sources on the PDF:
  - each page draws its neighbours' boundaries, and those lines sit a median 3 m (90th percentile 6 m) from the neighbours' own placed outlines and the known boundaries, with 98% of their length within 30 m;
  - on the real map's known set, every assembled district sits within 0.94 km (median 0.3 km) of its shape on the page's locator map, which is fitted to the commission's outline, not to any reconstruction;
  - drawn back onto its own page, no placed district extends outside the page's map frame;
  - drift between adjacent pieces after snapping is 0.003% of the territory on the real map's known set, and 0.005% on the calibration set.
- *What else was used.* The locator-map fit (`a10_inset.py`) aligns each inset to the outline of the whole province, or of the Calgary or Edmonton districts, in the commission's map. Those outlines include the outer edges of some sample districts. They are used only for the locator-map sanity item, never for placing a page or assigning a voting area.
- *The real map already exists in development.* The panel's map has been assembled from development data with the 56 unchanged districts known (`snap_fixed`), and it passes the sanity check. No partisan or structural measure has been computed on it.
- *A tested change not adopted.* A version 4 that seeds pages from the locator map before the road search was tested on the four misplaced pages. It placed Sherwood Park correctly (IoU 0.999), placed Edmonton-Meadows and Edmonton-Windermere within 0.9 km of their locator shapes, and still could not place Calgary-North West-Bearspaw. It is not used here, because adopting it would invalidate the development run; it is recorded in the development record.

**Part 3: The assembly.** Version 3 (`analysis/scripts/a9_stepb_reconstruct_v3.py`, SHA-256 `0b9d07c1…feace62`) is unchanged. `analysis/scripts/a10_assemble.py` (SHA-256 `3a75ee3d943dd34ae0fa5f6cc36963ed9dc2599d4cf492bec99664cadbd3d9da`) is applied to every page result before any district is scored:
1. *Known-overlap rule.* A reconstruction overlapping the known districts by more than 5% of its own area is rejected. In the second run, correct placements reached 0.074% and the wrong one 82.8%.
2. *Mutual-overlap rule.* Where two reconstructions overlap by more than 10% of the smaller one's area, one is rejected: the one in conflict with more other reconstructions; if equal, the one overlapping the known districts more; if equal, the one with fewer of its matched points within 60 m. Conflicts are recounted after each rejection.
3. *Provisional assignment.* Each voting area goes to the district, known or reconstructed, holding the largest share of its area. One less than half covered is left for the hole fill.
4. *Hole fill.* Unassigned voting areas are grouped into connected components on the voting-area graph. A district that was not placed, or was rejected, claims a component when all of these hold:
   - the component's area is within 25% of the district's stated area (App. 7);
   - either its page's red title names a census subdivision whose centroid lies in the component (hyphens read as spaces, so "Grande Prairie-Wapiti" names Grande Prairie), or, when no title town lies in any component, the component's representative point lies inside the envelope of every census subdivision named on its page or in its title, buffered by the larger of 6 km and half the square root of its stated area;
   - more than half of the districts touching the component are among the neighbour numbers printed on its page. A city's name on a page counts for all that city's districts, but only on a page whose own district is not in that city. A page with no neighbour record cannot claim.

   A component is filled when it has one claimant that claims nothing else. A district whose title names towns in several components claims them together, with the area test on their union. Where several districts and components claim each other, the unique one-to-one pairing that best matches their areas is taken. A fragment whose every neighbouring voting area belongs to one district goes to that district. Anything else stays unassigned, with its claimants recorded.
5. *Population: reported, not gated.* Amendment 7, Step C, set aside a district whose 2021 voting-area population, scaled to the provincial total, differed from its stated population by more than 5%. That gate is withdrawn. On the 57 districts whose geometry is known, the difference runs from −39.3% to +12.7%, and 34 of 57 exceed 5% (`findings/a10_dev/population_check_noise.csv`). The panel's figures are current estimates and the 2021 census predates recent growth (Calgary-North East −39%). The difference is reported for every reconstructed or filled district.

**Part 3b: Snapping, final assignment and the sanity check.** `analysis/scripts/a10_snap_assign.py` (SHA-256 `49f8a928b60358d34339b5b17eaad0c5bc266eba373961694c549b37653e87b9`):
1. *Sources.* Each district appears on its own page and, as a neighbour, on each adjacent page. `analysis/scripts/a10_neighbours.py` (SHA-256 `be38125f4929c585c6838539102f425bc99306ddd04411fabde1da8a6f015ff0`) extracts the neighbour boundaries (grey 1.84-pt strokes) and the printed neighbour numbers and city names. `analysis/scripts/a10_inset.py` (SHA-256 `0b87758adeb1bdf8fe471e30381a8e5f81b5a94aa50675429ee50bebeef446ed`) carries each page's locator map to ground. The report's written boundary descriptions (`findings/a10_dev/boundary_descriptions.md`) were inventoried and used to check lines by hand, as with Drumheller-Stettler's west side, which the panel moved east of Stettler. The code does not read them.
2. *Edges snap together.* A reconstruction vertex within 40 m of a known boundary, a voting-area boundary, or another outline or neighbour line moves onto it, in that order of preference.
3. *Drift* is the area of overlaps plus gaps between adjacent pieces, as a share of the territory. The target is under 0.05%.
4. *Final assignment, as Elections Alberta would assign.* Each voting area goes to the piece containing its representative point. One whose point lies in no piece goes to the piece holding the larger share of its area. A voting area cut by a line is flagged, and its population is apportioned by area in the population report. A hole two unplaced districts share is split by the better of their pages' rejected fits, the one with more matched points within 60 m, and both districts are flagged lower confidence. A rejected fit is used for this split only.
5. *Sanity check.* Every item must pass, and an item that cannot be run fails:
   - 91 districts, every voting area assigned once, and the province covered;
   - each district connected, allowing parts its own page draws;
   - no district overlapping a known district by more than 0.1% of its area;
   - each placed district's snapped area within 5% of its stated area (filled or split districts are reported, not gated: a hole of whole voting areas runs smaller than the drawn district);
   - for each district, more than half of its neighbours sharing more than 200 m of edge are printed on its page;
   - every placed district, drawn back onto its own page, inside the page's map frame;
   - every district within 3 km of its shape on the page's locator map (or half the shape's width for districts under 5 km across), with overlap at least 0.45 for larger ones. Barrhead-Westlock-Athabasca's locator map highlights Drayton Valley-Devon, a source error that is reported and not counted.

**Part 4: The third run.**
- *Command.* `analysis/scripts/a10_run.py` (SHA-256 `eaed0fa6849c53717287d9a88fe9b6e00c412277902affa431795eeebbc7f0a4`) runs, in order:
  1. the pages (`a10_reconstruct_pages.py`, SHA-256 `e55997ad6b96742444f04277f5e5530d6de61962f9d310ebad3e4a74577e9caa`) for the 69 pages that are not known districts;
  2. the neighbour extraction;
  3. the locator-map fit;
  4. the scorer (`analysis/scripts/a10_stepb_calibrate.py`, SHA-256 `05461b50947a142db3b7bca549f7db0b3c7a8023f55ffc8e504108eb15d362c5`).

  The pages may be run in two detached processes over halves of the list first. `a10_run.py --skip-pages` then runs steps 2 to 4 over them. Every page is deterministic, and a stopped page run resumes from the pages already saved; the stop is disclosed.
- *Gates.* As in Amendment 7, on the final assignment with the 22 tuning districts as the known set:
  - T1: at most 10% of the sample's voting areas in the wrong district, with unassigned counted as wrong;
  - T4: province-wide efficiency-gap delta under 0.5 points.

  Every sanity item must also pass. The assembly-only figures, T2, T3 and IoU are reported beside them.
- *Changed pages.* They are reconstructed in the same run because the hole fill needs every other piece in place. No measure of any changed district is computed until the result is committed, pass or fail.
- *Environment.* Python 3.12.13 with PyMuPDF 2.1. The scorer refuses any other.
- *Development check* (`findings/a10_stepb_development.md`): a dry run of the full sequence (`a10_run.py --skip-pages`) from a clean directory, seeded with the development page outputs, gave T1 0 of 1,909, T4 0.00 points, drift 0.005%, and every sanity item passing, with a voting-area assignment identical to the development run (`findings/a10_dev/dryrun_calibration.json`). All scripts are at commit `22a5ee41`.

**Part 5: If it passes.** Amendment 7, Part 3, Step C applies, with the assembly in place of raw polygons:
- The known set becomes the 56 unchanged districts plus Calgary-Acadia, at the commission's published geometry. The 35 changed pages from the same run are assembled under Parts 3 and 3b, and the sanity check must pass on that map too.
- A district that is not placed or filled is not used, and any measure that depends on it is not scored.
- R1 and R2 (Amendment 8) are scored provisionally only if every changed district is used. Amendment 8, Part 5's rerun rule applies, with the assembled map in place of the enacted map.
- The reading is labelled provisional, states that its calibration was a reproducibility run on seen data (Part 2), and is kept out of the headline. The voting-area cut list (Amendment 9, Part 5) is made on the assembled map and marked as such.

**Part 6: If it fails.** No numeric reading of the panel's map is published before the enacted map's shapefiles. The result is published with the reason.

**Part 7: What this changes and what it does not.**
- Amendment 7's 5% population gate is withdrawn (Part 3, rule 5).
- Amendment 9's one-attempt limit is withdrawn (Part 1).
- The T1 and T4 thresholds are unchanged.
- The headline remains the shapefiles of the map as enacted, which Elections Alberta publishes once the boundaries are set in a bill.

**Signed:** Claude (acting as session agent), directed by Will Conner
**Date:** 2026-11-04 (Alberta time)
