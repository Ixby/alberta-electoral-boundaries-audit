# Voting areas cut by district boundaries

`analysis/scripts/va_bisection.py` lists the voting areas (polls) a district map cuts. This is descriptive, not a test.

**The rule.** A voting area counts as cut when more than 1% of its area, and more than 0.01 km², lies outside the district that holds most of it.

**The voting areas checked.**
- Elections Alberta's 2023 voting areas (4,765).
- Its 2026 voting areas (4,904), from `EA_Voting_Area_Boundaries_2026.zip`. It was downloaded 2026-11-03 01:49 MST from https://www.elections.ab.ca/uploads/EA_Voting_Area_Boundaries_2026.zip, linked from the maps page archived at `evidence/elections_alberta/ea_maps_page_2026-11-02.html`. Its SHA-256 is `3bf299108aade69139f84e48e990708e924270f178022141d470d85808f6dd5a`, and the archived copy is in `evidence/elections_alberta/`.

Both sets nest in the 2019 divisions.

| Map | 2023 VAs cut | 2026 VAs cut | File |
|---|---|---|---|
| 2019 enacted (noise floor) | 0 | 0 | `2019_enacted.csv` |
| Commission majority, 2026 | 222 | 229 | `majority_2026.csv` |
| Commission minority, 2026 | 363 | 364 | `minority_2026.csv` |

The 2019 map cuts none of either set. So the rule's floors leave out digitising slivers, and every listed cut is a real one.

**The panel's map.** Its geometry has not been published.
- Its 56 unchanged districts are the majority's, so any cut whose pieces all lie in unchanged districts carries into the panel's map unchanged.
- On the 2026 voting areas, 63 of the majority's 229 cuts are of that kind. They are listed in `panel_known_cuts_2026vas.csv`, and on the 2023 voting areas the count is 61 of 222.
- The other 166 touch at least one district the panel changed. Whether the panel's map keeps them, removes them or adds new cuts can be read only from its geometry: the official shapefiles, or a reconstruction that passes the Step B calibration.
