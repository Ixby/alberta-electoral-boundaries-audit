# Ledger of the unregistered analyses since Step C (2026-11-04 to 2026-11-07)

Every analysis made after the provisional Step C reading, with its plan, its rule and its outcome, including nulls and failures. The registered result is Step C (`../a10_stepc/`); nothing below changes it. Each analysis had a plan committed before it was computed, but most were written after related results were known, and the plans say so. **None of these is a finding on whether any map is a gerrymander.**

## Multiple testing across the whole family

`ledger.py` gathers every percentile-ranked comparison these analyses made (88 in all), turns each into a two-sided p = 2 × min(pct, 100 − pct), and corrects across the family. Chikina-Frieze-Pegden p-values enter as reported.

| | Count |
|---|---|
| Comparisons | 88 |
| Expected beyond the 5th or 95th percentile if the maps behaved like the nonpartisan comparison maps | about 8.8 |
| Beyond the 5th or 95th percentile (nominal flags) | 5 |
| Significant after Benjamini-Hochberg (false discovery rate 5%) | **0** |
| Significant after Bonferroni | **0** |

**The five nominal flags:**

| Comparison | Map | Percentile | Direction |
|---|---|---|---|
| Lethbridge pieces, city-aware regional redraw | panel | 99.5 | more split than neutral |
| Leduc and Beaumont pieces, city-blind regional redraw | panel | 0.2 | less split than neutral, kept whole |
| St. Albert NDP votes in lopsided losses, city-blind | panel | 96.8 | more cracked; inherited from the commission majority |
| Seats under 30% NDP, election-day ballots, set D | ¶167 | 96.1 | more lopsided UCP seats |
| Lethbridge NDP votes in lopsided losses, city-blind | ¶167 | 3.9 | less cracked than neutral |

Fewer nominal flags turned up than the nonpartisan comparison maps would produce on their own, and none survives a correction. The 88 comparisons overlap (the same maps and chains enter many of them), so they are not independent. Bonferroni is valid under dependence. Benjamini-Hochberg is shown for reference.

## What "p" means here (author's point, 2026-11-07: "districts aren't drawn by chance")

Districts are drawn by deliberate choice, not at random. None of these p-values or percentiles assumes otherwise. Each one compares the real map with **nonpartisan alternatives**: maps drawn by a procedure that follows the encoded rules (population, contiguity, and in some sets municipalities and s.15(2)) and never looks at votes. A small p means the map's partisan effect is unusual among maps drawn without reference to party. It does not mean the map was drawn randomly, and a large p does not mean it was. A deliberate choice made for a stated, nonpartisan reason, such as a community of interest or a highway corridor, can land anywhere in that range. The question these numbers help with is narrower: is the partisan pattern of the choices something nonpartisan drawing commonly produces, or rarely produces? Why the choices were made is a separate question, and it is answered by the record of the panel's reasons and how consistently it applied them, not by these numbers.

## Every analysis, including the ones without percentiles

| Date | Analysis | Plan | Rule or question | Outcome |
|---|---|---|---|---|
| 11-04 | Seat-count claim (50 UCP / 41 NDP) | `da21f14b` | Does 2023 on the panel's map give 50/41? | 51/40 on the substrate that reproduces 2023; within the reconstruction's range |
| 11-07 | ¶167 map beside the panel's | `5eb63b34` | Net effect of the panel's southern changes | 1 seat (all ballots), 2 (election day), all undecided; ¶167 is the outlier against set D |
| 11-07 | Referendum electors | `36516e5d` | Electors against estimates and the 2021 census | Planned correlation test confounded (recorded in `2a9a4e00`); regional shares point slightly to the census; no grade changed |
| 11-07 | Census eligibility | `e2f5ae2e` | How much of the low elector count does citizenship and age explain | About half overall; Calgary-North East still 39% short |
| 11-07 | Small-area population rebuild v1 | `d3d069da` | Hold-out mean ≤ 2%, max ≤ 6% | **Failed** (6.02%, 7.71%) |
| 11-07 | Rebuild v2 (elector split) | `2f9aa3c9` | Same | **Failed** (minority 6.96%); series stopped |
| 11-07 | Packing and cracking, parts 1 and 3 | `c2f1a710` | Wasted-vote split; named areas | Lethbridge: 45% of the city's NDP votes in lopsided losses on the panel's map; small province-wide differences |
| 11-07 | Packing and cracking, part 2 | `c2f1a710` | Cracking count above p95; packing at top positions | Neither map cracks; one shared Edmonton seat packs; panel inside the band at 87 of 91 positions |
| 11-07 | Six signals A (elections and swing) | `0610a3a9` | Same sign across elections and swing | Robust and small: the panel is 1-2 NDP seats below ¶167 |
| 11-07 | Six signals B-E | `0610a3a9` | Descriptive | Reserves: 3 split, 2 possibly tracing artefacts; Lethbridge alone 4-way among mid-size cities; Lethbridge members paired; growth leans NDP on every map |
| 11-07 | Six signals F (south, city-blind) | `0610a3a9` | Lethbridge lopsided-loss share beyond p95 or below p5 | Panel p71 (not unusual); ¶167 p3.9 |
| 11-07 | Hybrid regions | `d2c1353e` | Same rule, 11 regions, two variants | Only St. Albert, city-blind; Lethbridge city-aware p93 |
| 11-07 | Chikina-Frieze-Pegden | `f9bb45da` | p < 0.025 | Not a local outlier (p ≥ 0.89) |
| 11-07 | City-boundary weight | `5dc4a0dd` | Implied weight from past maps | Running |
| 11-07 | Amendment 12 replays | filed `6aef29e1` | Every vote-free column equal | 221, 222 match; 201 cannot replay (early code) and is excluded; rest running |

## Self-corrections made today, kept on record

- **Amendment 12's draft:** it said S5 and R2 use no votes. They do. Corrected before filing (`6887aa41`).
- **The ¶167 undecided rule:** it first counted lines both maps share. Corrected before reporting.
- **The elector check:** its planned correlation was confounded by the maps' equal-population design. Recorded, and the original numbers were kept.
- **The test threshold:** first presented as a pass/fail line. Re-read against the literature (`../hybrid_regions/threshold_grounding.md`).
