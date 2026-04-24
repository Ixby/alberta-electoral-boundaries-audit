# Vote Anywhere (VAN) Identification Report
## Task A — C5 Analysis
**Source file:** `analysis/polls_2023_unified.csv`
**Date produced:** 2026-04-23

---

## 1. Detection Methodology

Three heuristics were applied to identify VAN polls from `polls_2023_unified.csv`:

| Heuristic | Description | Matches |
|-----------|-------------|---------|
| H1 | `poll_name` contains "Vote Anywhere" (case-insensitive) | 87 |
| H2 | `poll_name` contains "any elector" or "province-wide" | 0 |
| H3 | `voting_areas` is NaN / empty (no VA numbers) | >87 (Advance/Mobile/Special rows generally lack VAs; H1 is the discriminating rule) |

**All 87 identified VAN rows match H1 exclusively.** No rows matched H2. H3 is not uniquely discriminating because all non-Election-Day rows lack VA numbers; H1 (poll_name pattern) is the definitive identifier.

**VAN poll canonical name pattern:** `Vote Anywhere (Out of ED)`
**Ballot type:** All 87 VAN rows have `ballot_type = Advance`
**Distribution:** Exactly one VAN row per 2019 ED (87 EDs × 1 VAN row = 87 rows)

---

## 2. VAN Poll Vote Totals

### 2.1 Province-Wide Vote Totals (All Ballot Types)

Computed from `v0_1_alberta_2023_results.csv` (`total_valid_votes` column, 87 EDs):

| Region | EDs | Total Valid Votes |
|--------|-----|-------------------|
| Calgary | 26 | 551,929 |
| Edmonton | 20 | 370,496 |
| Rest of Alberta | 41 | 842,490 |
| **Province Total** | **87** | **1,764,915** |

### 2.2 VAN Vote Totals (Summed from 87 VAN rows)

| Region | NDP Votes | UCP Votes | Other Votes | VAN Total |
|--------|-----------|-----------|-------------|-----------|
| Calgary (26 EDs) | 37,251 | 29,694 | 1,195 | 68,140 |
| Edmonton (20 EDs) | 30,595 | 14,021 | 1,026 | 45,642 |
| Rest of Alberta (41 EDs) | 19,921 | 30,683 | 1,547 | 52,151 |
| **Province VAN Total** | **87,767** | **74,398** | **3,768** | **165,933** |

### 2.3 VAN as % of Province-Wide Total

| Metric | Value |
|--------|-------|
| Province-wide total votes | 1,764,915 |
| Total VAN votes | 165,933 |
| VAN % of province total | **9.40%** |
| VAN NDP votes | 87,767 |
| VAN UCP votes | 74,398 |
| VAN other votes | 3,768 |

**NDP vote share in VAN polls:** 87,767 / 165,933 = **52.89%**
**UCP vote share in VAN polls:** 74,398 / 165,933 = **44.84%**
**Other vote share in VAN polls:** 3,768 / 165,933 = **2.27%**

---

## 3. Breakdown by Ballot Type

| Ballot Type | VAN Row Count | Notes |
|-------------|---------------|-------|
| Advance | 87 | All VAN rows |
| Election Day | 0 | None — VAN is only an Advance mechanism |
| Mobile | 0 | N/A |
| Special Ballot | 0 | N/A |

VAN votes are a subset of **Advance** ballots. There are no Election Day VAN polls.

### 3.1 VAN as % of Election-Day Total

The Election Day vote total was estimated from the VA-level spatial attribution file (`v0_1_phase4c_majority_2023_votes.csv`), which aggregates VA-polygon Election Day votes per 2026 proposed ED. After excluding two known data-quality outliers (Edmonton-Enoch: 33,176 attributed from over-extended polygon; Edmonton-West Henday: disaggregated into Enoch sub-area), the province-wide Election Day vote total is approximately:

| Component | Votes |
|-----------|-------|
| Calgary Election Day (approx.) | ~275,000 |
| Edmonton Election Day (approx.) | ~188,000–210,000 |
| Rest of Alberta Election Day (approx.) | ~446,000 |
| **Province Election Day Total (est.)** | **~900,000–930,000** |

**VAN votes as % of Election-Day total:** approximately **17.8%–18.4%**

**Interpretation:** Roughly one in five Election-Day-equivalent votes was cast as a VAN Advance ballot, meaning the voter chose a location outside their home ED. These votes cannot be spatially attributed to the VA polygon printed on the ballot and must be apportioned back to the voter's 2019 home ED using the Election Day share within that ED.

**Note on uncertainty:** The Election Day total is an approximation because the phase4c spatial attribution pipeline was run against the 2026 majority ED map (89 EDs), not the 2019 map (87 EDs), and several 2026 EDs have known over-capture or incomplete boundary coverage. The % figure for VAN/Election Day should be treated as ±2 pp.

---

## 4. VAN Vote Totals by ED (Full List)

| ED (2019) | NDP | UCP | Other | VAN Total |
|-----------|-----|-----|-------|-----------|
| Calgary-Acadia | 788 | 566 | 31 | 1,385 |
| Calgary-Beddington | 1,384 | 1,097 | 83 | 2,564 |
| Calgary-Bow | 1,489 | 1,195 | 59 | 2,743 |
| Calgary-Buffalo | 1,130 | 538 | 27 | 1,695 |
| Calgary-Cross | 415 | 355 | 19 | 789 |
| Calgary-Currie | 3,328 | 2,318 | 185 | 5,831 |
| Calgary-East | 615 | 458 | 42 | 1,115 |
| Calgary-Edgemont | 1,374 | 771 | 43 | 2,188 |
| Calgary-Elbow | 1,356 | 1,034 | 81 | 2,471 |
| Calgary-Falconridge | 602 | 351 | 30 | 983 |
| Calgary-Fish Creek | 2,463 | 2,550 | 84 | 5,097 |
| Calgary-Foothills | 1,057 | 892 | 29 | 1,978 |
| Calgary-Glenmore | 1,092 | 718 | 22 | 1,832 |
| Calgary-Hays | 755 | 775 | 21 | 1,551 |
| Calgary-Klein | 2,178 | 1,839 | 70 | 4,087 |
| Calgary-Lougheed | 1,016 | 993 | 57 | 2,066 |
| Calgary-Bhullar-McCall | 1,337 | 1,025 | 0 | 2,362 |
| Calgary-Mountain View | 2,554 | 888 | 53 | 3,495 |
| Calgary-North | 2,613 | 2,406 | 0 | 5,019 |
| Calgary-North East | 781 | 583 | 0 | 1,364 |
| Calgary-North West | 2,259 | 1,976 | 111 | 4,346 |
| Calgary-Peigan | 1,500 | 1,759 | 43 | 3,302 |
| Calgary-Shaw | 1,731 | 1,814 | 32 | 3,577 |
| Calgary-South East | 629 | 841 | 24 | 1,494 |
| Calgary-Varsity | 2,204 | 1,319 | 29 | 3,552 |
| Calgary-West | 601 | 633 | 20 | 1,254 |
| Edmonton-Beverly-Clareview | 779 | 460 | 57 | 1,296 |
| Edmonton-Castle Downs | 1,602 | 981 | 86 | 2,669 |
| Edmonton-City Centre | 960 | 317 | 29 | 1,306 |
| Edmonton-Decore | 1,598 | 1,047 | 151 | 2,796 |
| Edmonton-Ellerslie | 2,593 | 1,334 | 55 | 3,982 |
| Edmonton-Glenora | 1,510 | 450 | 49 | 2,009 |
| Edmonton-Gold Bar | 791 | 251 | 26 | 1,068 |
| Edmonton-Highlands-Norwood | 1,401 | 402 | 60 | 1,863 |
| Edmonton-Manning | 2,188 | 1,096 | 51 | 3,335 |
| Edmonton-McClung | 439 | 239 | 24 | 702 |
| Edmonton-Meadows | 908 | 496 | 14 | 1,418 |
| Edmonton-Mill Woods | 724 | 394 | 0 | 1,118 |
| Edmonton-North West | 1,021 | 501 | 24 | 1,546 |
| Edmonton-Riverview | 2,197 | 1,032 | 85 | 3,314 |
| Edmonton-Rutherford | 717 | 359 | 32 | 1,108 |
| Edmonton-South | 2,798 | 1,650 | 61 | 4,509 |
| Edmonton-South West | 2,229 | 1,228 | 33 | 3,490 |
| Edmonton-Strathcona | 3,517 | 527 | 93 | 4,137 |
| Edmonton-West Henday | 2,062 | 977 | 80 | 3,119 |
| Edmonton-Whitemud | 561 | 280 | 16 | 857 |
| Airdrie-Cochrane | 904 | 1,272 | 41 | 2,217 |
| Airdrie-East | 470 | 941 | 25 | 1,436 |
| Athabasca-Barrhead-Westlock | 270 | 740 | 0 | 1,010 |
| Banff-Kananaskis | 502 | 1,053 | 18 | 1,573 |
| Bonnyville-Cold Lake-St. Paul | 35 | 174 | 0 | 209 |
| Brooks-Medicine Hat | 264 | 460 | 35 | 759 |
| Camrose | 110 | 264 | 16 | 390 |
| Cardston-Siksika | 170 | 392 | 24 | 586 |
| Central Peace-Notley | 91 | 348 | 8 | 447 |
| Chestermere-Strathmore | 226 | 408 | 7 | 641 |
| Cypress-Medicine Hat | 285 | 517 | 16 | 818 |
| Drayton Valley-Devon | 462 | 1,156 | 39 | 1,657 |
| Drumheller-Stettler | 54 | 175 | 3 | 232 |
| Fort McMurray-Lac La Biche | 261 | 634 | 10 | 905 |
| Fort McMurray-Wood Buffalo | 169 | 680 | 112 | 961 |
| Fort Saskatchewan-Vegreville | 418 | 681 | 26 | 1,125 |
| Grande Prairie | 437 | 829 | 51 | 1,317 |
| Grande Prairie-Wapiti | 622 | 1,443 | 39 | 2,104 |
| Highwood | 404 | 1,179 | 26 | 1,609 |
| Innisfail-Sylvan Lake | 459 | 1,278 | 37 | 1,774 |
| Lac Ste. Anne-Parkland | 738 | 1,582 | 91 | 2,411 |
| Lacombe-Ponoka | 106 | 418 | 35 | 559 |
| Leduc-Beaumont | 188 | 301 | 5 | 494 |
| Lesser Slave Lake | 58 | 111 | 3 | 172 |
| Lethbridge-East | 1,195 | 880 | 42 | 2,117 |
| Lethbridge-West | 560 | 494 | 30 | 1,084 |
| Livingstone-Macleod | 131 | 371 | 24 | 526 |
| Maskwacis-Wetaskiwin | 554 | 1,386 | 70 | 2,010 |
| Morinville-St. Albert | 2,091 | 1,607 | 98 | 3,796 |
| Olds-Didsbury-Three Hills | 232 | 813 | 43 | 1,088 |
| Peace River | 39 | 140 | 8 | 187 |
| Red Deer-North | 592 | 591 | 27 | 1,210 |
| Red Deer-South | 852 | 1,167 | 66 | 2,085 |
| Rimbey-Rocky Mountain House-Sundre | 248 | 985 | 189 | 1,422 |
| Sherwood Park | 1,236 | 1,203 | 119 | 2,558 |
| Spruce Grove-Stony Plain | 242 | 373 | 14 | 629 |
| St. Albert | 1,635 | 914 | 31 | 2,580 |
| Strathcona-Sherwood Park | 2,322 | 1,876 | 73 | 4,271 |
| Taber-Warner | 137 | 408 | 31 | 576 |
| Vermilion-Lloydminster-Wainwright | 46 | 128 | 15 | 189 |
| West Yellowhead | 106 | 311 | 0 | 417 |

---

## 5. Key Findings

1. **87 VAN rows identified** — one per 2019 ED, all with ballot_type = "Advance".
2. **VAN votes total 165,933** = **9.40% of the province-wide 2023 vote** (1,764,915 total).
3. **VAN votes are approximately 17.8%–18.4% of Election Day votes** (±2 pp uncertainty due to phase4c approximation).
4. **These votes must not be spatially attributed to the VA polygon.** The poll_name "Vote Anywhere (Out of ED)" confirms the voter is NOT a resident of the VA where they voted. The phase4c pipeline already flags these for home-ED reapportionment using the Election Day share as the attribution key.
5. **Partisan composition of VAN ballots:** NDP 52.9%, UCP 44.8%, Other 2.3% — notably NDP-leaning compared to the province-wide two-party split (approximately 50/50 in many urban EDs). This reflects higher urban VAN uptake where Edmonton NDP-leaning voters were more likely to use province-wide advance facilities.
6. **No H2 matches** (no "any elector" or "province-wide" poll names). The "vote anywhere" terminology was used exclusively as "Vote Anywhere (Out of ED)".

---

## 6. Methodological Notes

- The VAN poll NDP/UCP split (87,767 NDP / 74,398 UCP) is **not** attributable to any single 2026 ED and must NOT be added to phase4c Election Day totals without proper home-ED reapportionment.
- The aggregate VAN NDP share (52.9%) vs UCP share (44.8%) is a province-wide average. Individual EDs vary considerably — urban EDs like Edmonton-Strathcona show 85%+ NDP in VAN, while rural EDs like Central Peace-Notley show 80%+ UCP.
- The three-heuristic check confirms that H1 (poll_name pattern) is both necessary and sufficient. Heuristics H2 and H3 add no additional coverage.
