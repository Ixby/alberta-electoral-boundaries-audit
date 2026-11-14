# data/reference: notes on the reference tables

Known differences between these tables and their sources. Each was checked against the source file named.

## `alberta_2023_results.csv`: three candidates are missing

The table has six candidate slots per division. The official workbook, `data/raw/2023_results.xlsx`, lists a Communist Party candidate in three divisions who is not in the table:

| Division | Candidate | Votes |
|---|---|---:|
| Calgary-East | Jonathan Trautman (CP-A) | 64 |
| Edmonton-Highlands-Norwood | Naomi Rankin (CP-A) | 102 |
| Edmonton-Meadows | Corinne Benson (CP-A) | 213 |

What this does to the numbers:

- The `votes_1` to `votes_6` columns sum to 1,764,536. The `total_valid_votes` column sums to 1,764,915, which is the official figure. The gap is these 379 votes.
- Every division's UCP votes, NDP votes and `total_valid_votes` match the workbook. The province totals are UCP 928,900 and NDP 777,404.
- Third-party votes taken from the candidate columns come to 58,232. The official figure is 58,611 (1,764,915 less 1,706,304).

Which scripts are affected. Eight scripts read the candidate columns. Seven take only the UCP and NDP votes from them (`packing_cracking_analysis.py`, `chen_rodden_alberta.py`, `seats_at_50_50_regional.py`, `marginal_seats_analysis.py`, `vote_anywhere_splat.py`, `findings/seat_claim_test.py`, `findings/p338_projection/simulate_338.py`); where they need "other" votes they compute `total_valid_votes` less UCP less NDP. None of the seven is affected. The eighth, `third_party_sensitivity.py`, summed the remaining candidate columns and so undercounted "other" votes by 379 in those three divisions; it now uses `total_valid_votes` less UCP less NDP. Its committed output, `data/outputs/third_party_sensitivity_results.csv`, was written before that change (rules B and C differ slightly in those three divisions). The other columns (`winner_party`, `winner_pct`, `margin_pct`, `turnout_pct`) do not depend on the missing candidates.

No script that builds this table from the workbook is committed. `tests/test_published_numbers.py` checks the table against the workbook on every run and fails if any difference other than these three appears.

## `minority_2026_populations.csv` and `majority_2026_populations.csv`: printed report against official boundary file

These tables were transcribed from the commission's printed final report. The official boundary files (`data/shapefiles/canonical/ea_{minority,majority}_2026_eds.gpkg`, column `PopCensus`) differ from them in four districts:

| Map | District | Printed report (these tables) | Official boundary file |
|---|---|---:|---:|
| Minority | Calgary-Varsity | 64,982 | 64,932 |
| Majority | Calgary-Acadia | 55,791 | 55,789 |
| Majority | Calgary-Bow | 54,981 | 54,982 |
| Majority | Sylvan Lake-Innisfail | 55,290 | 55,291 |

- The minority table sums to 4,888,773 and the minority boundary file to 4,888,723. The 50-person gap is Calgary-Varsity alone.
- The majority table and the majority boundary file both sum to 4,888,723; the three differences cancel.
- Seven minority districts are spelled differently in the table and the boundary file (for example "Airdrie East" and "Airdrie-East", "St. Albert" and "St Albert"). Their populations are equal.

Results labelled "commission's population tables" use these CSVs (for example the mean absolute deviations 3,180 and 4,707). Results labelled "official shapefiles" use `PopCensus` or the 2021 census overlay.

## `va_pop_from_das.csv` (in `data/`, with a second copy in `data/outputs/`)

The 2021 census population of each voting area, which every ensemble balances on. It is an area-weighted overlay of the 2021 dissemination areas on the voting-area polygons. `analysis/scripts/build_va_pop.py` rebuilds it and compares the result with the committed file; they agree to within 1e-8 persons in every row. The script was written after the file and is not the code that first produced it. The two copies are byte-identical; `mcmc_ensemble.py` reads `data/va_pop_from_das.csv`.
