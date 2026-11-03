# The November map, stage by stage

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
- Step B, the calibration, follows the November drand pin (`preregistration/seed_commitments.md`, round 6606642).
- Step C, the provisional map score, runs only if the calibration passes.
