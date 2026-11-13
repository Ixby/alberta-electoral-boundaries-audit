# The November map, stage by stage

> Times before 2026-11-07 marked MST are UTC−7.

This is the stage record Amendment 7, Part 1 requires.
- Each stage is graded only on what it releases to the public.
- A stage that releases nothing gets no grade, and the record says so, with the date it was checked.
- A change between two stages is reported only when both versions are public.

Times are Alberta time. Sources are archived in `evidence/` with their SHA-256.

| Stage | Status | Released | What is graded | Record |
|---|---|---|---|---|
| 1. The panel's report, tabled | **Released**: the committee's report was created 2026-11-02 07:38 MST, and the 72-hour clock runs from then (Amendment 7, Part 7) | The panel's report, in low- and high-resolution PDFs, and the committee's final report (`evidence/legislature/`) | Part 4 grades: the process lane, the population table, and split counts read from the maps. There are no numeric map scores: no shapefile has been published. | `findings/iap_stage1_part4.md` |
| 2. The Assembly's resolution | Not released (checked 2026-11-02 20:45 MST) | none | none | n/a |
| 3. The bill as introduced | Not released (checked 2026-11-02 20:45 MST; the Assembly's bills list shows no new electoral-divisions bill. Bill 32 is the 91-seat Electoral Boundaries Commission Amendment Act, not a map) | none | none | n/a |
| 4. Amendments to the bill | Not released | none | none | n/a |
| 5. The bill as passed | Not released | none | none | n/a |

**Official shapefiles:** none published as of 2026-11-02 20:45 MST. The Elections Alberta maps page is archived at `evidence/elections_alberta/ea_maps_page_2026-11-02.html`. Elections Alberta's Geomatics Team Lead wrote on 2026-10-28 that the shapefiles follow once the boundaries are "set in bills" (`evidence/correspondence/elections_alberta_gis_2026-10-28.md`).

**Reconstruction (Amendment 7, Part 3):**
- Step A, matching the panel's districts to the commission's, is done (`findings/iap_unchanged_districts.md`).
- Step B, the calibration, was run once on 2026-11-03 and **fails**: 49.0% of the sample's VAs misassigned (gate: at most 10%) and an EG delta of −2.16 points (gate: under 0.5). The procedure places city pages almost exactly but cannot place rural pages (`findings/a7_stepb_calibration.md`).
- A second attempt was registered as Amendment 9 (OSF 9wp5y, update 6aea2abd5e67b5390f474434, 2026-11-03 11:41 AM MST), with version 3 of the procedure, which reads rural pages. It was run once on 2026-11-03 and also **fails**: 13.8% of VAs misassigned and an EG delta of +0.80 points (`findings/a9_stepb_calibration.md`).
  - It placed 30 of the 34 pages correctly, rural pages included (IoU 0.998 to 1.000).
  - It declined three: Chestermere-Strathmore, Grande Prairie-Wapiti and Peace River.
  - It placed Sherwood Park wrongly (rotated 90°, 13.5 km off) and accepted the placement.
  - Amendment 9 allowed no third attempt.
- Amendment 10 (OSF 9wp5y, update `6aeb59edd63871f1daf383ab`, filed 2026-11-04) withdrew that limit (Part 1) and registered a third attempt, which assembles the panel's map from its pages. Its calibration passed on 2026-11-04, as a reproducibility run on pages already seen, not as out-of-sample evidence of accuracy (`findings/a10_stepb_calibration.md`).
- Step C, the provisional map score, ran on 2026-11-04 under Amendment 10, Part 5 (`findings/a10_stepc/`): structural lane 2 of 5 flags, partisan lane 1 of 4. It is labelled provisional and kept out of the headline. Amendments 11 to 13, written after it, are in the amendment log.
