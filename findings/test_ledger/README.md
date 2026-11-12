# Ledger of the unregistered analyses since Step C (2026-11-04 to 2026-11-08)

The analyses made after the provisional Step C reading, with their plans, rules and outcomes, including nulls and failures. Owed and proposed reruns are listed at the end of the table. The registered result is Step C (`../a10_stepc/`); nothing below changes it. Each analysis has a plan in the repository, except the v3 two-lane rerun, which reused the Step C commands. For several, the plan was committed with the results, and that it was written first rests on the author's statement: local targeting (plan 55 seconds before results), referendum electors (2 minutes), packing and cracking parts 1 and 3 (3 minutes), city-boundary weight and population basis (5 minutes each), rural voters (7 minutes), and the Amendment 12 rehearsal, whose run sheet is in the same commit as its results (`97608e51`). Most plans were written after related results were known, and the plans say so. **None of these is a finding on whether any map is a gerrymander.**

## Multiple testing across the whole family

`ledger.py` gathers 132 percentile-ranked comparisons from these analyses, plus 11 tests that report their own p (Chikina-Frieze-Pegden, Fisher, sign). That is not every percentile the analyses report. Among those it leaves out are the Lethbridge lopsided-loss rows in `../packing_cracking/` (including ¶167's p4.7), signal F's election-day rows in `../six_signals/` (including ¶167's NDP seats at p99.95) and set D's competitive-seat count (close4) in `../iap_para167/`, while it keeps election-day rows from other analyses. The counts below are for the rows it holds. It turns each percentile into a two-sided p = 2 × min(pct, 100 − pct), and corrects across all 143. A map beyond every plan gets p = 2 / (n_eff + 1), not 0.

| | Count |
|---|---|
| p-values corrected | 143 |
| Percentile-ranked comparisons | 132 |
| 10% of the percentile-ranked comparisons (the expected number of flags only for measures without ties; see below) | 13.2 |
| Beyond the 5th or 95th percentile (nominal flags) | 12 |
| Significant after Benjamini-Hochberg (false discovery rate 5%) | **0** |
| Significant after Bonferroni | **0** |

**The twelve nominal flags.** Added 2026-11-08: the commission majority's two south-and-central findings, each measured two ways, and the three Lethbridge rows at the ends of the commission city-weight range:

| Comparison | Map | Percentile | Direction |
|---|---|---|---|
| Lethbridge pieces, city-aware regional redraw | panel | 99.5 | more split than neutral |
| Leduc and Beaumont pieces, city-blind regional redraw | panel | 0.2 | less split than neutral, kept whole |
| St. Albert NDP votes in lopsided losses, city-blind | panel | 96.8 | more cracked; inherited from the commission majority |
| Seats under 30% NDP, election-day ballots, set D | ¶167 | 96.1 | more lopsided UCP seats |
| Lethbridge NDP votes in lopsided losses, city-blind | ¶167 | 3.9 | less cracked than neutral; 0%, a tie with the neutral 5th percentile (`../six_signals/`) |
| South and central NDP packing, 13 divisions, city-blind and city-aware | majority | 100.0, 100.0 | above every redraw (p ≥ 0.00093 and 0.0016 at the n_eff floor); the redraws cannot draw its Canmore-Banff (`../changed_districts/`, Limits) |
| South and central NDP votes in lopsided losses, city-blind and city-aware | majority | 4.5, 4.7 | fewer than neutral |
| Lethbridge pieces, city-aware at W = 0.517 and 0.661 | panel | 99.6, 99.9 | more split than neutral (the same finding as the first row, at other weights) |
| Lethbridge NDP votes in lopsided losses, city-aware at W = 0.661 | panel | 96.5 | more cracked; at W = 0.517 it is p93.4, inside |

None survives a correction. The 13.2 overstates how many flags the nonpartisan maps would produce on their own. Many of these measures are counts (seats, pieces) or shares that often sit at exactly 0 or 1, and the percentile splits ties, so a flag is usually rarer than 10%. For the 100 comparisons whose nonpartisan plans are committed (`../changed_districts/chains/`, `../hybrid_regions/chains/`, `../six_signals/regional_south/`, `../city_weight/lethbridge_W*/`), the expected count is 4.6: for each comparison, the share of its own plans that its percentile rule would flag, summed. 11 of the 12 flags are among those 100. The 32 set D comparisons have no committed plans, so the expected count for the whole family cannot be computed here. The closest to surviving are the majority's south-and-central packing rows: they would pass Bonferroni only if the 50,000 plans were independent draws (p about 0.00004), and they are not (`../changed_districts/README.md`). The comparisons overlap (the same maps and chains enter many of them), so they are not independent. Bonferroni is valid under dependence. Benjamini-Hochberg is shown for reference.

## What "p" means here (author's point, 2026-11-07: "districts aren't drawn by chance")

Districts are drawn by deliberate choice, not at random. None of these p-values or percentiles assumes otherwise. Each one, except the three local-targeting tests (two Fisher tests and a sign test, which compare changed and unchanged divisions of the real maps), compares the real map with **nonpartisan alternatives**: maps drawn by a procedure that follows the encoded rules (population, contiguity, and in some sets municipalities and s.15(2)) and never looks at votes. A small p means the map's partisan effect is unusual among maps drawn without reference to party. It does not mean the map was drawn randomly, and a large p does not mean it was. A deliberate choice made for a stated, nonpartisan reason, such as a community of interest or a highway corridor, can land anywhere in that range. The question these numbers help with is narrower: is the partisan pattern of the choices something nonpartisan drawing commonly produces, or rarely produces? Why the choices were made is a separate question, and it is answered by the record of the panel's reasons and how consistently it applied them, not by these numbers.

## The analyses, including the ones without percentiles

| Date | Analysis | Plan | Rule or question | Outcome |
|---|---|---|---|---|
| 11-04 | Seat-count claim (50 UCP / 41 NDP) | `da21f14b` | Does 2023 on the panel's map give 50/41? | 51/40 on the substrate that reproduces 2023; within the reconstruction's range |
| 11-06 | Two-lane scorecard on the v3 reconstruction | none: the Step C commands, rerun unchanged (unregistered sensitivity) | Do the Step C flags change on v3? | No: structural 2 of 5, partisan 1 of 4, as filed (`../iap_v3_two_lane/`) |
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
| 11-07 | City-boundary weight | `5dc4a0dd` | Implied weight from past maps; Lethbridge at the range's ends | Commission range W = 0.517–0.661; panel's Lethbridge lopsided-loss share p93.4 to p96.5, beyond the line only at the top (`../city_weight/`) |
| 11-07 | Local targeting | `399a489a` | Are competitive or NDP-held seats changed more often; which way do close margins move; where do moved NDP votes go | Changed less often, not more (Fisher p 0.27 and 0.007); 5 of 6 close changed divisions moved toward the UCP (sign test p 0.22); 9.0% of moved NDP votes went into lopsided losses, 2.0% the other way (`../local_targeting/`) |
| 11-07 | Stated reasons, checked for consistency | `231efd5d` | Is each stated reason applied the same way to comparable cases? | Lethbridge and Banff rest on reasons applied to Red Deer only in a small way, or not supported by the panel's own numbers; regular shapes consistent; Springbank "urban with urban" not supported by density (`../reasons_consistency/`) |
| 11-07 | Population basis | `c01cbdcd` | A regional shift of 0.5 seats or more between 2021 and 2024 limits that region's comparisons | Calgary +1.31, Edmonton +0.63, everything else −1.40: a limit on every big-city comparison; set D rerun on the growth basis 2026-11-12 (row below) (`../population_basis/`) |
| 11-07 | Rural voters in mixed divisions | `c01cbdcd` | Counts; a regional rerun if an area crosses 5,000 rural residents in urban-majority divisions | Lethbridge County 0 → 8,138 on the panel's map, so the rerun was owed; run 2026-11-12 (row below) (`../rural_voice/`) |
| 11-07 | Amendment 12 rehearsal | run sheet, `97608e51` | Step C on all ballots, on the reconstruction | Same flags as filed: structural 2 of 5, partisan 1 of 4; R1 and R2 not flagged (`../amendment12_rehearsal/`) |
| 11-07 | Amendment 12 replays | filed `6aef29e1` | Every vote-free column equal | 24 of 26 match; early chains 201 and 100 do not and are dropped (Amendment 13); cause not established (`../amendment12_replays/`) |
| 11-08 | Changed districts | `3c501006` | Each map's layout of each changed region, beyond p95 or below p5 | The panel's layouts all inside the band; the commission majority's south-and-central layout packs more NDP votes than every redraw, though the redraws cannot draw its Canmore-Banff (`../changed_districts/`) |
| 11-12 | Lethbridge-region rerun with the rural measures (owed under the 11-07 plan) | `c01cbdcd` | Rank the panel's 8,138 among neutral redraws (the plan sets no threshold) | City-blind p49.9 (median 8,154), municipality-aware p71.2 (median 1,333; 46% of plans at 0, 29% at or above 8,138); same plans as the committed chains, all 396,000 rows replayed; region-wide rural residents in urban-majority divisions p86.2 and p97.5; not in `ledger.py`'s family (`../rural_voice/`) |
| 11-12 | Set D rerun on the 2024 growth basis (proposed in the 11-07 plan; unregistered sensitivity) | `c01cbdcd` | City-versus-rest test and seat counts on the basis the maps were drawn on (no decision rule; registered flag at p95 read as sensitivity) | Panel's city-versus-rest gap +13.6% at p99.8 (p99.7 on published figures; every chain above p99.5), against p59.2 on 2021; provisional (n_eff 462, lag cap binds). City divisions: neutral median 51, panel 49 (p4.3). UCP seats: neutral median 50, panel 51 (p68.8). Indices 252 and 255 did not seed, retired, replaced by 256 (Amendment 11, Part 3). Not in `ledger.py`'s family (`../population_basis/`) |

## Self-corrections, kept on record

- **The family count (found 2026-11-08):** this page, the report and the site said 88 comparisons. That was the count before the local-targeting tests were added (`e159cbe2`); the ledger then held 91 p-values, of which 80 were percentile-ranked. The "expected about 8.8" used the 88. Neither changed a conclusion (0 survived correction either way). The counts above are current.
- **Ties at 0 and 100 (2026-11-08):** `ledger.py` turned a percentile of 100 into p = 0. It now floors p at 2 / (n_eff + 1) and stops on a 0 or 100 with no n_eff.

- **Amendment 12's draft:** it said S5 and R2 use no votes. They do. Corrected before filing (`6887aa41`).
- **The ¶167 undecided rule:** it first counted lines both maps share, and the first committed README (`4216f67a`) reported that version, with three more seats undecided on all ballots (Calgary-Bow-Springbank, Calgary-Bow, Calgary-West-Elbow Valley). The rule was fixed 39 minutes later (`25cf4e0b`).
- **The elector check:** its planned correlation was confounded by the maps' equal-population design. Recorded, and the original numbers were kept.
- **The test threshold:** first presented as a pass/fail line. Re-read against the literature (`../hybrid_regions/threshold_grounding.md`).
