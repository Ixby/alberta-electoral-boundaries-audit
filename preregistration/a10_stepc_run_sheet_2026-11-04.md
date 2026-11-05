# Step C run sheet: provisional scoring of the panel's assembled map (2026-11-04)

> Committed before any measure of the panel's map in this sheet is computed. It fixes the inputs, commands, flags and output paths of the registered Step C (Amendment 7, Part 3; Amendment 9, Part 5; Amendment 10, Part 5) and changes no rule or threshold. Where a registered rule needed a reading, the reading is stated here, before the run. Environment: `C:/Users/email/.venvs/audit-k91/Scripts/python.exe` (Python 3.12.13, PyMuPDF 2.1). Outputs go to `findings/a10_stepc/` unless stated.

Every output is **provisional**, kept out of the headline, and carries this label: the calibration was a reproducibility run on seen data (Amendment 10, Part 2), T1 0 of 1,909, efficiency-gap delta 0.00 points, final mean Hausdorff 0.031 km, mean IoU 0.9993 (`findings/a10_stepb_calibration.md`). No step gives or implies a conclusion on whether the map is a gerrymander; the specification's verdict label is reported as that test's outcome only.

## Inputs

| Input | Path | SHA-256 |
|---|---|---|
| The panel's assembled map (frozen pipeline output, registered run `fd82cdd1`) | `findings/a10_stepb_run/districts_real_map.gpkg` | recorded in the ingest record |
| Its registered voting-area assignment | `findings/a10_stepb_run/va_assignment_real_map.csv` (= `C:/tmp/a10reg/fixed/va_assignment.csv`) | `5380406772ccb91b9187b360668086816e2dd30f4f72987a744ddd920aaae6dc` |
| Scoring copy (ingest output; names copied to `EDName2025`) | `data/shapefiles/iap_assembled/iap_2026_assembled.gpkg` and `.ingest.json` | in `.ingest.json` |
| s.15(2) criteria table | `data/outputs/s15_2_va_criteria.csv` | `48c928b8716f6ed218065e01a912ecabd11518917ac9e312376e4d603ee2fafc` (the Amendment 5, Part 15 table) |
| Stated populations (App. 7) | `data/iap/iap_app7_populations.csv` | — |
| Territory-null code (Amendment 8) | worktree `wt-a8` at `42b5fda8`: `territory_null.py` `46fc7a16…ee02`, `territory_score.py` `0485e788…2b55` (verified) | |
| Cut-VA sensitivity | `findings/a10_dev/cut_va_sensitivity.py` `c264a49e3a408e6710b8d4bb36fe8196b6ffc60ac30ce0c3155bcf5a652fa0dc` (verified) | |

The published gap-free copy (`districts_real_map_published.gpkg`) feeds no score.

**Polygon path against the registered assignment (checked before this sheet, no measure computed).** Assigning the 4,765 voting areas by representative point to the frozen districts file reproduces the registered assignment for 4,764 of them. The one difference: VA 875 (Rimbey-Rocky Mountain House-Sundre poll 042; 498 people on the 2021 overlay, 218 election-day votes), a cut VA with 45% of its area in Lacombe-Sylvan Lake, is assigned to Rocky Mountain House-Sundre by the registered run and to Lacombe-Sylvan Lake by representative point. Steps that read polygons (1–7) use the polygon path; steps that take an assignment (9, 10) use the registered assignment. The difference is reported beside every result it can touch.

**Ingest (step 0, run before this sheet; a check, not a measure).** `ingest_committee_map.py --src findings/a10_stepb_run/districts_real_map.gpkg --name-col district --out data/shapefiles/iap_assembled/iap_2026_assembled.gpkg`: every blocking check passes; 91 districts. It is written to its own path, not the enacted map's (`data/shapefiles/lunty/`).

## Registered steps

1. **Partisan lane** (spec §7 step 2):
   `analysis/scripts/phase4c_canonical_attribution.py --majority data/shapefiles/iap_assembled/iap_2026_assembled.gpkg --output data/outputs/iap_assembled_phase4c.json --map-key iap_2026_assembled`, then
   `analysis/scripts/joint_outlier_score_canonical.py --map-key iap_2026_assembled --real-scores data/outputs/iap_assembled_phase4c.json --output findings/a10_stepc/joint_outlier.json`.
   Substrate: the registered 2023 election-day voting-area votes. Substrate C of the seat-claim test is not used anywhere in Step C.
2. **Structural lane** (spec §7 step 3): `run_structural_battery.py --shapefile data/shapefiles/iap_assembled/iap_2026_assembled.gpkg --output findings/a10_stepc/structural.json --label iap_2026_assembled`.
3. **Specification outcome** (spec §7 step 4): `verdict_synthesis.py --structural findings/a10_stepc/structural.json --joint findings/a10_stepc/joint_outlier.json --output findings/a10_stepc/verdict.json`.
4. **X1** (Amendment 5, Part 13): `score_x1.py --map data/shapefiles/iap_assembled/iap_2026_assembled.gpkg --out findings/a10_stepc/x1.json`. The October 2025 interim map is not in the repository, so (c) is "not scored", as Part 13 provides. No `--d-record`: if (d) is not adopted on the geometry, the panel's report is read for a stated reason and the X1 result is reported under both hand entries, with the page.
5. **Size-matched comparison** (Amendment 5, Parts 14–18; set D primary):
   `close_seats_ensemble.py real --out data/outputs/iap_assembled_real_maps.json --extra data/shapefiles/iap_assembled/iap_2026_assembled.gpkg`, then
   `size_matched_results.py --root ../alberta_audit --real data/outputs/iap_assembled_real_maps.json --candidate iap_2026_assembled --out-json findings/a10_stepc/size_matched.json --out-md findings/a10_stepc/size_matched.md`.
   `../alberta_audit` (branch `amendment17-local-runs`, holding the chain outputs) is read only; its branch is not switched. Cells are reported as the script labels them (final or provisional, Part 16).
6. **qsgy8 tripwires** (Amendment 5, Part 6; beside the verdict): `november_tripwires.py --shapefile data/shapefiles/iap_assembled/iap_2026_assembled.gpkg`, stdout saved to `findings/a10_stepc/tripwires.txt`.
7. **R1 and R2** (Amendment 8, via Amendment 10, Part 5).
   - *Eligibility (checked before this sheet, from geometry only).* Every changed district is placed or filled; Fort McMurray-Wood Buffalo is filled from the hole its neighbours leave (Amendment 10, Part 3), so it is used. Under Amendment 8, Part 5's rerun rule, applied to the scoring copy by `territory()` at `42b5fda8`: 58 commission-majority districts are fixed, the 56 of Step A, Calgary-Acadia, and **Edmonton-Meadows**, which the panel changed but which the assembled map fills with exactly the majority's voting areas (by representative point), so the rule fixes it. The remaining territory is one component of 1,753 voting areas holding 33 districts (against 1,782 and 34 in the calibration). App. 7 puts two fixed districts more than 25% below its average (Central Peace-Notley −46.5%, Lesser Slave Lake −44.1%), so the territory's s.15(2) cap is 2. R1 and R2 are therefore scored.
   - *Null rerun.* From `wt-a8`, chains 1–5, the registered seeds (drand round 6606642, salts `a8-territory-null-chain1`–`5`), 100,000 steps, thin 250:
     `analysis/scripts/territory_null.py --idx N --enacted <wt-osf>/data/shapefiles/iap_assembled/iap_2026_assembled.gpkg --stated-low 2 --out C:/tmp/a10stepc/territory`, run detached (WMI + pythonw runner).
   - *Scoring.* `territory_score.py plans C:/tmp/a10stepc/territory`; `territory_score.py rank <scoring copy> C:/tmp/a10stepc/territory --stated-low 2` (reference chains 1–4, burn 10,000); `territory_score.py real <scoring copy> --shuffle 10000` for the reported-only label-shuffle p. Outputs copied to `findings/a10_stepc/territory/` (scores, rank, logs; plans by SHA-256 only if too large).
   - Every territory district outside ±25% on the overlay is listed beside the result.
8. **Cut voting-area range** (Amendment 10, Part 5; sensitivity, not a gate): `A10_STEPC=1 findings/a10_dev/cut_va_sensitivity.py --map fixed --snap-dir C:/tmp/a10reg/fixed --out-prefix findings/a10_stepc/cut_va_sensitivity`.
9. **Voting areas cut** (Amendment 9, Part 5; descriptive): `va_bisection.py --map data/shapefiles/iap_assembled/iap_2026_assembled.gpkg --label iap_2026_assembled --vas 2023 2026 --out-csv findings/a10_stepc/va_cuts.csv`, marked "on the assembled map".
   - *Reading of "within the calibration's measured boundary error".* A cut is marked **uncertain** when at least one side of it is a changed district's line and the part outside the main district lies wholly within 31 m (the final mean Hausdorff distance, 0.031 km) of the main district. Cuts between two known districts are the commission's geometry and are not marked. The 31 m is a mean, not a worst case; this is stated beside the list.

## Supplementary (not registered tests)

10. EBCA population rules: `rules_check.py --assignment findings/a10_stepc/assignment_nodes.csv` (the registered assignment as `node,district`, node = OBJECTID − 1, the graph's row order) ` --table data/outputs/s15_2_va_criteria.csv --stated data/iap/iap_app7_populations.csv --label iap_2026_assembled --out findings/a10_stepc/rules_check.json`.

## Record

`findings/a10_stepc/README.md` gives every result with its label, any step that fails to run and why, and every deviation from this sheet.

## Changes to this sheet

- **Step 6 named the wrong script.** `november_tripwires.py` is an unregistered v0.2 city-split check (it also requires EPSG:3401 and fails on the CSD file's column names). qsgy8's four tripwires (MO #1–#4) are scored by `analysis/scripts/phase_b_scorecard.py`, the script its dry run used: `--shapefile data/shapefiles/iap_assembled/iap_2026_assembled.gpkg --map-name iap_2026_assembled --name-col EDName2025 --skip-mcmc --map-s50 <step 1's seats at 50/50> --out-dir findings/a10_stepc`. MO #4 uses the cached ReCom and SMC outputs (`--skip-mcmc`). The failed `november_tripwires.py` attempts produced no result and are recorded in the README. This change was written after the scorecard had run (it was run as soon as the wrong script failed); no other script or flag set was tried.
- **Step 7: chain 3 does not seed.** On the assembled map's territory (33 districts on 1,753 voting areas) the registered seed for chain 3 fails in `recursive_tree_part` ("Could not find a possible cut after 50000 attempts"); the code at `42b5fda8` has no fallback, and Amendment 8 states none. Following the audit's precedent for a chain that does not seed (Amendment 5, Part 14: set D's index 250 "is retired because it does not seed", and the next free index is used), chain 3 is retired and **chain 6** (salt `a8-territory-null-chain6`, same code and run length) takes its place. The reference chains are 1, 2, 4 and 6 (`rank --ref 1 2 4 6`); chain 5 stays the holdout. This was decided when chain 3's failure was seen, before any territory plan or R1/R2 statistic was scored.
