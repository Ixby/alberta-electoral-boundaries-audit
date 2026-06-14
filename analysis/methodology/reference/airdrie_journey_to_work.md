> **Backward:**
> - Statistics Canada Table 98-10-0459-01 — primary source (2021 Census CSD-level commuting flows)
> - `analysis/scripts/fetch_journey_to_work_csds.py` — extraction script
>
> **Forward:**
> - `data/outputs/airdrie_journey_to_work.csv` — output consumed downstream
> - `analysis/methodology/reference/minority_rationales_validation.md` R3/R4 — Airdrie→Calgary commute evidence
> - `reports/academic/report_academic.md` §5.9 — incorporates the commute-tie verdict

# v0.1 Airdrie Journey-to-Work — Tracks R3, R4

**Verdict: SUPPORTS the commuter-tie rationale at city level. Does not determine whether a 4-way split is necessary (CLOSED-FAIL on population math).**

## Data source

- **Table:** Statistics Canada 98-10-0459-01, "Commuting flow from geography of residence to geography of work by gender: Census subdivisions." (2021 Census of Population.)
- **Retrieval:** Full-table ZIP bulk download, retrieved 2026-06-13.
- **DGUID:** `2021A00054806021` (Airdrie CY, Alberta; verified from table scan).
- **Script:** `analysis/scripts/fetch_journey_to_work_csds.py`
- **Output:** `data/outputs/airdrie_journey_to_work.csv`.

## Results

Airdrie had 22,340 resident workers with a usual place of work in the 2021 Census.

### Top ten destinations, 2021 Census

| Rank | Place of work | Workers | Share of all workers | Share of out-commuters |
|---:|---|---:|---:|---:|
| 1 | Calgary (CY), Alta. | 10,260 | 45.9% | 76.2% |
| 2 | Airdrie (CY), Alta. (self) | 8,875 | 39.7% | (self) |
| 3 | Rocky View County (MD), Alta. | 1,650 | 7.4% | 11.0% (est.) |
| 4 | Edmonton (CY), Alta. | 235 | 1.1% | — |
| 5 | Crossfield (T), Alta. | 165 | 0.7% | — |
| 6 | Cochrane (T), Alta. | 105 | 0.5% | — |
| 7 | Red Deer (CY), Alta. | 90 | 0.4% | — |
| 8 | Fort McMurray / Wood Buffalo, Alta. | 90 | 0.4% | — |

Out-commuters (workers whose place of work is not Airdrie): 22,340 − 8,875 = 13,465. Calgary = 10,260 / 13,465 = **76.2% of out-commuters.**

## Interpretation

Airdrie is simultaneously a commuter suburb of Calgary *and* a city with a substantial internal labour market. The 39.7% within-Airdrie work share is higher than Chestermere (17.0%) and Cochrane (49.2%), suggesting Airdrie sits between a pure bedroom community and a self-contained city.

The 76.2% of out-commuters going to Calgary is the strongest measurable evidence supporting Minority Rationales R3 ("strong economic, community, and transportation ties") and R4 ("functional integration of Airdrie and northern Calgary") at the city-to-city level.

**What this data settles:** Airdrie has a real Calgary commuter tie above the CMA membership threshold. The tie exists and is quantifiable.

**What this data does not settle:** Whether the commuter tie *requires* a Calgary-Airdrie hybrid district (rather than two Airdrie-named districts each partially overlapping a Calgary edge) is a policy question about how to respond to the tie. The majority draws two Airdrie districts (Airdrie North and Airdrie South) without a Calgary piece. The minority draws one purely Airdrie district (Airdrie East) and three Calgary-Airdrie hybrids. The population math for the minority's 4-way split is CLOSED-FAIL (Test 3 in `justification_tests_findings.md`): the 4-way split forces each Airdrie quarter into a host district dominated by non-Airdrie voters.

## Files

- `data/outputs/airdrie_journey_to_work.csv` — 39 non-zero destinations, origin Airdrie (CY), Alberta.
- `.temp/statscan_98-10-0459.zip` — full table source (gitignored).
