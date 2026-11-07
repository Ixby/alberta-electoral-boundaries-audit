# Referendum electors as a check on the population figures (2026-11-07)

**Unregistered and not blind.** Plan committed before any comparison (`preregistration/referendum_electors_check_2026-11-07.md`, commit `36516e5d`). Electors are not population, and the Act's test is population. Nothing here is a finding on whether any map is lawful or a gerrymander. The panel's map is the v3 reconstruction.

## The population source

Both bodies state it: the Alberta Office of Statistics and Information's July 1, 2024 estimates at dissemination-area level, total 4,888,723 (commission final report, PDF pp. 28-29; panel report, PDF pp. 107-108). The panel says it kept them so its map could be compared with the commission's on the same figures, and calls criticism of them "unjustified". These stated tables are the audit's primary population figures for the scorecard. The dissemination-area file itself was not found publicly, so no division outside the stated tables can be scored on it directly.

The commission gives February 2027 as the 2026 census release (PDF p. 28); the panel says 2027.

## Match check

Complete. All 4,904 election-day polls match the 4,904 polygons in Elections Alberta's 2026 voting-area file, on division and voting-area number, with no duplicates. Poll electors sum to each division's stated total and to 3,286,778.

## Result: inside the two cities, electors follow the 2021 overlay more closely than the 2024 estimates

| Correlation with 2026 electors | Stated 2024 estimates | 2021 overlay |
|---|---|---|
| Majority map (official polygons): all 89 | 0.41 | 0.81 |
| Majority: 49 Calgary and Edmonton divisions | **0.18** | **0.81** |
| Majority: the other 40 | 0.83 | 0.85 |
| Panel's map: all 91 | 0.47 | 0.80 |
| Panel's map: Calgary and Edmonton | 0.39 | 0.80 |
| Minority map: Calgary and Edmonton | −0.06 | 0.75 |

Outside the two cities the figures agree. The gap is inside Calgary and Edmonton. By the plan, this is reported as **an open question about the estimates, and it changes no s.15(1) grade.**

**It does not show the estimates are wrong.** Two explanations give the same pattern:
- The estimates are right, and fast-growing city areas hold many children, non-citizens and people not yet on the list. The commission anticipated this (PDF p. 30). The list could also lag new neighbourhoods.
- The estimates place too much growth in those areas.

This check cannot separate them. The 2026 census can, at dissemination-area level.

| Division | Electors 2026 | Stated 2024 | 2021 overlay | Electors per stated person (province 0.672) |
|---|---|---|---|---|
| Calgary-North East | 15,036 | 54,541 | 28,881 | 0.276 |
| Calgary-Bhullar-McCall | 20,256 | 55,887 | 38,535 | 0.362 |
| Edmonton-Meadows (panel's map) | 20,823 | 53,318 | 40,082 | 0.391 |
| Edmonton-Windermere (panel's map) | 25,752 | 54,136 | 34,044 | 0.476 |
| Calgary-South East | 29,472 | 53,551 | 35,677 | 0.55 |
| St. Albert (highest) | 52,246 | 59,935 | 56,504 | 0.872 |

Calgary-North East does not depend on placement: no voting area is cut by its boundary on the majority map. 15,036 electors against 54,541 stated people is the largest unexplained case.

## The maps on electors (a description only, not the Act's test)

| | Majority | Minority | Panel | ¶167 |
|---|---|---|---|---|
| Beyond ±25% on electors | 13 | 10 | 16 | 18 |
| Within ±10% on electors | 37 of 89 | 45 of 89 | 39 of 91 | 39 of 91 |
| Calgary and Edmonton mean against the rest, electors | −7.6% | −0.6% | −3.8% | −4.8% |
| Same, stated population | +9.2% | +15.9% | +13.4% | not stated |

The city gap changes sign. On population, Calgary and Edmonton divisions are larger than the rest; on electors, they are smaller. The commission treated voter parity as no "more than a marginal consideration" under its statute, and said divisions with many non-voters can be harder to represent (PDF p. 30).

## By-elections

Not used. They cover a few divisions, so they cannot update the province, and they cannot be mixed into 2023's vote totals.

Files: `electors_check.py`, `electors_check.json`, `division_table.csv`; `data/referendum/electors_by_va_2026.csv`; source workbooks in `evidence/elections_alberta/referendum_2026/` with `SHA256SUMS`.
