# Amendment 7, Step B: the calibration sample (fixed before any reconstruction)

> Times before 2026-11-07 marked MST are UTC−7.

Amendment 7, Part 3 (OSF 9wp5y, update 6ae95303…) defines the sample as "the unchanged districts drawn in the same map pages as changed districts", topped up to 10 by a seeded draw if needed. The sample below was fixed on 2026-11-02 at about 20:30 MST (commit `9eaaea54`, 20:31 MST). No district had been reconstructed at that time, and no georeferencing had been built or tuned.

**How the rule is applied** (`analysis/scripts/a7_stepb_select_sample.py`; output `findings/a7_stepb_sample.json`):

- Only the Appendix 8 district pages of the high-resolution PDF are used (district n at PDF page 215+n). The Appendix 6 composites are not used.
- An unchanged district u counts as drawn on a changed district c's page when that page carries u's district-number label in the neighbour-label style and a word of u's name in the same style within 60 pt.
  - The neighbour-label style is ArialMT in grey #828282 or #4E4E4E, at the same point size as the page's own district-number label (Arial-Bold, red #93241A).
  - This separates district labels from township, range and highway numbers, which use other fonts and colours.
- The unchanged set is Step A's 56 districts (`findings/iap_unchanged_districts.md`); the changed set is the other 35.

**Result: 34 districts.** That is at least 10, so the drand top-up draw is not used. The November round (6606642) is pinned but unused by Step B.

| ED | District | Drawn on the pages of changed EDs |
|---|---|---|
| 2 | Calgary-Beddington | 4 |
| 6 | Calgary-Confluence | 1 |
| 8 | Calgary-Currie | 4 |
| 10 | Calgary-Edgemont | 4, 28 |
| 11 | Calgary-Elbow | 1 |
| 13 | Calgary-Fish Creek | 1 |
| 14 | Calgary-Glenmore-Tsuut'ina | 1, 28 |
| 18 | Calgary-McKenzie | 1 |
| 26 | Calgary-Symons Valley | 4 |
| 27 | Calgary-Varsity | 4, 28 |
| 31 | Edmonton-City Centre | 46 |
| 34 | Edmonton-Enoch | 48, 49, 87 |
| 35 | Edmonton-Glenora-Riverview | 46 |
| 36 | Edmonton-Gold Bar | 40, 46 |
| 39 | Edmonton-McClung | 46, 48 |
| 41 | Edmonton-Mill Woods | 33, 40, 42, 46 |
| 44 | Edmonton-Rutherford | 33, 42, 45, 46, 48, 49 |
| 47 | Edmonton-West Henday | 87 |
| 50 | Airdrie-East | 81 |
| 51 | Airdrie-West | 52, 58, 81 |
| 55 | Camrose | 42, 60, 61, 68, 69, 91 |
| 56 | Central Peace-Notley | 90 |
| 57 | Chestermere-Strathmore | 80, 81 |
| 59 | Cold Lake-Bonnyville-St. Paul | 62 |
| 64 | Fort Saskatchewan-Vegreville | 53, 79 |
| 66 | Grande Prairie-Wapiti | 90 |
| 70 | Lesser Slave Lake | 53, 62, 63, 90 |
| 75 | Lloydminster-Wainwright | 61 |
| 77 | Medicine Hat-Brooks | 61, 73, 74, 81 |
| 78 | Medicine Hat-Cypress | 74 |
| 82 | Peace River | 63 |
| 83 | Red Deer-North | 84 |
| 86 | Sherwood Park | 79 |
| 89 | Strathcona-Sherwood Park | 40, 42, 79 |

**Excluded after checking:** a looser name-only scan also matched these, and both were checked by hand:
- Calgary-North (20): no district-number label 20 appears on any changed page. The match came from the words of "Calgary-North West-Bearspaw".
- St. Albert (88): no label 88 appears on Morinville-Sturgeon's page (PDF 294). "St. Albert" there is the municipality's name.

**Changed pages showing no unchanged district:** EDs 22, 54, 67, 71, 72, 76 and 85. Their drawn neighbours are all changed districts.

**Separation (no leakage):**
- The georeferencing procedure is developed and tuned only on the 22 unchanged districts outside this sample, and on labelled roads, rivers and municipal boundaries.
- The procedure is committed, with its SHA, before it is run once on the sample.
- Any change made after seeing sample results is disclosed in the calibration record, with the rerun.

**Test labels (erratum queued for the next amendment):**
- Amendment 7 calls the efficiency-gap gate "T4". OSF w2s8k's v11 table (dpg2_experiment_plan.md, §T-C) names that gate "T1 EG delta" (<0.5 pp). w2s8k's T4 is population MAD, and its T3 is mean Hausdorff distance.
- The thresholds and quantities match Amendment 7's text: VA misassignment at most 10%, and an EG delta under 0.5 points. Step B computes exactly what Amendment 7 describes.
- Beside them, Step B reports T2 (mean area error, w2s8k v11 reference <10%), T3 (mean Hausdorff, <5 km) and mean IoU (w2s8k v11 reference ≥65%), as references only, not gates.
