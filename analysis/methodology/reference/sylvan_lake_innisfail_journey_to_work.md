> **Backward:**
> - Statistics Canada Table 98-10-0459-01 — primary source
> - `analysis/scripts/fetch_journey_to_work_csds.py` — extraction script
>
> **Forward:**
> - `data/outputs/sylvan_lake_journey_to_work.csv`
> - `data/outputs/innisfail_journey_to_work.csv`
> - `analysis/methodology/reference/minority_rationales_validation.md` R11 — Red Deer–Sylvan Lake commuter verdict
> - `reports/academic/report_academic.md` §5.9

# v0.1 Sylvan Lake + Innisfail Journey-to-Work — Track R11

**Verdict (R11): PARTIALLY SUPPORTS. Commuter tie to Red Deer is confirmed for both communities. School-division claim ("go to school" in Red Deer) is contradicted by school-division geography.**

## Data sources

Extracted 2026-06-13 via `analysis/scripts/fetch_journey_to_work_csds.py` from `data/outputs/statscan_98-10-0459.zip`.

- Sylvan Lake DGUID: `2021A00054808012`
- Innisfail DGUID: `2021A00054808008`

## Sylvan Lake results

4,625 resident workers with a usual place of work.

| Rank | Place of work | Workers | Share of all workers | Share of out-commuters |
|---:|---|---:|---:|---:|
| 1 | Sylvan Lake (T), Alta. (self) | 1,830 | 39.6% | (self) |
| 2 | Red Deer (CY), Alta. | 1,520 | 32.9% | 54.4% |
| 3 | Red Deer County (MD), Alta. | 330 | 7.1% | — |
| 4 | Lacombe (T), Alta. | 185 | 4.0% | — |
| 5 | Calgary (CY), Alta. | 125 | 2.7% | — |
| 6 | Lacombe County (MD), Alta. | 120 | 2.6% | — |
| 7 | Ponoka County (MD), Alta. | 100 | 2.2% | — |

Out-commuters (work outside Sylvan Lake): 4,625 − 1,830 = 2,795. Red Deer = 1,520 / 2,795 = **54.4% of out-commuters.**

## Innisfail results

2,420 resident workers with a usual place of work.

| Rank | Place of work | Workers | Share of all workers | Share of out-commuters |
|---:|---|---:|---:|---:|
| 1 | Innisfail (T), Alta. (self) | 1,585 | 65.5% | (self) |
| 2 | Red Deer (CY), Alta. | 385 | 15.9% | 46.4% |
| 3 | Red Deer County (MD), Alta. | 165 | 6.8% | — |
| 4 | Olds (T), Alta. | 80 | 3.3% | — |
| 5 | Calgary (CY), Alta. | 60 | 2.5% | — |
| 6 | Lacombe (T), Alta. | 40 | 1.7% | — |

Out-commuters: 2,420 − 1,585 = 835. Red Deer = 385 / 835 = **46.1% of out-commuters.**

## Interpretation

### Commuter claim (R11 "where they work")

The commuter-tie component of R11 is **confirmed** at CSD level. A majority of Sylvan Lake out-commuters (54.4%) and nearly half of Innisfail out-commuters (46.1%) commute to Red Deer. Red Deer is the dominant non-local destination for both communities.

This confirms the minority's rationale that these communities have a functional labour-market link to Red Deer. The question (as with Cochrane-Nolan Hill and Airdrie) is whether the *specific* electoral district configuration responds to this tie appropriately — in this case, whether combining part of the City of Red Deer with Sylvan Lake or Innisfail represents the community better than a purely rural Sylvan Lake–Innisfail combination paired with a purely urban Red Deer set of districts.

### School claim (R11 "where they go to school")

Sylvan Lake K–12 schools are operated by **Chinook's Edge School Division** (headquarters in Innisfail). Red Deer city schools are **Red Deer Public Schools** and **Red Deer Catholic Regional Division** — separate jurisdictions. Students from Sylvan Lake do not normally attend Red Deer city schools and vice versa. The "go to school" rationale in R11 is not supported by school-division geography for K–12 education.

University/college: Red Deer Polytechnic (formerly RDC) serves both communities, but this applies to all of central Alberta (not specific to Sylvan Lake/Innisfail). The post-secondary institution claim is plausible but generic and does not specifically tie Sylvan Lake or Innisfail to Red Deer in a way that distinguishes them from other surrounding communities.

## Files

- `data/outputs/sylvan_lake_journey_to_work.csv` — 28 non-zero destinations.
- `data/outputs/innisfail_journey_to_work.csv` — 13 non-zero destinations.
