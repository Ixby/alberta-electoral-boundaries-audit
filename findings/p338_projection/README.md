> **Exploratory, unregistered, for learning.** Computed 2026-11-09 in the cloud session, after the projection was known; no plan was written in advance and nothing here is a registered test. It applies a third party's projection (338Canada, October 19, 2026) to the maps; it is not a forecast and says nothing about why any line was drawn. The panel's map and the ¶167 map are the audit's reconstructions.
>
> **Inputs.** The 338 snapshot is `evidence/projections/338canada_2026-10-19/ridings_2026-10-19.csv`. The script reads copies of these repo files (at `557d11fe`) from an `inputs/` folder beside it, with the SHA-256 of each copy in `input_sha256.txt`. To rerun it, copy them into `inputs/` under the names on the left, and put the 338 CSV one level up as `p338_ridings_2026-10-19.csv`:
>
> | Name in `inputs/` | Repo path |
> |---|---|
> | `polls_2023_unified.csv` | `data/outputs/polls_2023_unified.csv` |
> | `alberta_2023_results.csv` | `data/reference/alberta_2023_results.csv` |
> | `assignment_va_to_2026_canonical.csv` | `data/outputs/assignment_va_to_2026_canonical.csv` |
> | `panel_assignment_nodes_a10_stepc_replay.csv` | `findings/a10_stepc_replay/assignment_nodes.csv` |
> | `panel_assignment_nodes_a10_stepc.csv` | `findings/a10_stepc/assignment_nodes.csv` |
> | `panel_va_assignment_real_map_a10_stepb.csv` | `findings/a10_stepb_run/va_assignment_real_map.csv` |
> | `para167_va_assignment.csv` | `findings/iap_para167/va_assignment.csv` |
> | `real_maps_all_ballots.json` | `findings/allballots_ranking/real_maps_all_ballots.json` |
> | `para167_real_maps_all_ballots.json` | `findings/iap_para167/real_maps_all_ballots.json` |
> | `ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg` | `data/shapefiles/canonical/` |
> | `va_polygons_with_2023_votes.gpkg`, `va_polygons_with_full_2023_votes.gpkg` | `data/shapefiles/derived/` |
>
> The all-ballots voting-area votes were rebuilt in memory by the audit's own Amendment 12 rule, because the committed all-ballots file is a Git LFS pointer in the cloud checkout; the rebuild matches the official count in all 87 districts. Sanity checks: 2023 all-ballots seats reproduce the audit's figures on all five maps exactly (49, 48, 55, 51, 50), and re-aggregation to the 2019 map reproduces 338's 43–43–1.

# 338Canada's Alberta projection, run on five electoral maps

338Canada projection of October 19, 2026, run on November 9, 2026. The 2023 votes and the map assignments come from the audit repository at commit `557d11fe`, which was only read; nothing in it was changed. This is a learning exercise, not a forecast.

## The short answer

- **Yes, the map changes the advantage, and one map stands out.** On the commission minority's map the UCP wins a majority even when it trails the NDP slightly province-wide. It needs a lead of −0.2 points. On the commission majority's map, the panel's map and the ¶167 map it needs a lead of about 5.3 to 5.4 points; on the 2019 map, 4.3. In the same 5,000 simulated elections, the minority's map gives a different government from the majority's map in about 1 in 4. Each time, the minority's map gives a UCP majority where the majority's map gives an NDP one.
- **The panel's map and the commission majority's map are close.** The panel's map has 2 more seats in total, and the UCP wins both of them (median). The lead the UCP needs is almost the same (5.3 against 5.4 points). The two maps give different governments in about 4% of the simulated elections, always with the panel's map giving the UCP the majority.
- **Panel's map against the 2019 map:** the UCP needs about 1 point more of a lead on the panel's map. They give different governments in about 6% of simulated elections, mostly when the 2019 map gives the UCP a majority and the panel's map does not.
- **At 338's central numbers the race is a dead heat on every map but the minority's.** The 2019 map gives 43 to 43, with Red Deer-North exactly tied. The majority, panel and ¶167 maps give the NDP a bare majority. The minority's map gives the UCP 53 of 89.
- **Once local randomness is added, the UCP is a slight favourite on every map.** Its majority chance is 54 to 62% on four maps and 78% on the minority's. The reason is that more of the NDP's projected wins are narrow. On the 2019 map we get 62%, close to 338's own 60%. Whether the UCP or the NDP is the favourite on the majority, panel and ¶167 maps depends on how much local randomness you assume; the order of the maps does not.

## What was done

1. **2023 votes, all ballots.** We rebuilt the audit's all-ballots votes for each of 4,765 voting areas: election day plus advance, mobile, special and Vote Anywhere ballots, using the audit's own rule (Amendment 12). They match the official 2023 count in all 87 districts.
2. **Which voting area is in which district on each map.** These come from the audit's tables. The 2019 map uses Elections Alberta's own coding and the commission maps use the official shapefiles. The panel's map and the ¶167 map use the audit's reconstructions from the panel's report.
3. **Moving 2023 toward 338's projection, district by district (2019 map).**
   - *Proportional (main method).* In each voting area, the UCP share is multiplied by (338's UCP ÷ the 2023 UCP share) for its district, and the same is done for the NDP and "other". The shares are then rescaled to add to 100%. One pass leaves district totals up to 0.6 points off 338's numbers, so the step is repeated until every district lands exactly on 338's numbers.
   - *Additive (check).* Each voting area gets its district's change in points (for example UCP −5, NDP +3), clipped at zero and rescaled.
   - Each voting area keeps its 2023 number of voters.
4. **Parties.** The parties are UCP, NDP and "other", where other = 100 − UCP − NDP. "Other" covers every other party, including those 338 lists (PTPA, REP, WIP, Greens) and the small ones it does not. In 7 districts nobody outside the UCP and NDP ran in 2023. There the projected "other" vote is spread evenly over the district's voting areas.
5. **Counting.** Voting areas are added up into each map's districts. Ties count as ties. "Within 4 points" uses the audit's definition: the UCP-NDP gap as a share of their combined vote.
6. **Monte Carlo, 5,000 draws, fixed seed.** Each draw combines two random shifts in the UCP-minus-NDP lead, with half the shift going to the UCP and half coming from the NDP:
   - *One province-wide shift.* Its standard deviation is 6.1 points of lead, so that 338's ±5 band for each party is a 90% interval.
   - *An independent shift in each 2019 district.* 338's riding ranges (typically ±7) are read as 90% intervals that already include the provincial ±5. The riding-only part is what remains: a standard deviation of 5.5 points of lead in a typical riding (3.5 to 9.1).

   The voting areas are then re-swung to each draw's numbers, and **every map is scored on the same draws**.
7. **Seats at 50/50.** We used the audit's method (shift every district's two-party share by the same amount until the province is tied) on the projected district totals. Doing it inside the model gives the same counts.

## Checks

- **2023 (all ballots): passed exactly on all five maps.** UCP seats, seats within 2 and 4 points, and seats at 50/50 all equal the audit's published numbers. UCP seats are 49 on the 2019 map, 48 on the majority's map, 55 on the minority's, 51 on the panel's and 50 on the ¶167 map. The table is in `out/tables.md`.
- **338 (2019 map): passed.** Adding the voting areas back into the 2019 districts gives 338's own riding leaders, 43 UCP, 43 NDP and 1 tie. Both methods reproduce every riding's numbers exactly. The only riding that "flips" is Red Deer-North, and only before the repeat passes: a single proportional pass breaks 338's exact 45–45 tie by 0.05 points (UCP 45.04, NDP 44.99). That is an approximation in the single pass, not a real change, and the repeated passes remove it. All 87 riding names match the official list, checked against 338's own 2023 winners.

## Results by map

**At 338's point projection** (both methods give the same seats):

| Map | Seats | Majority needs | UCP | NDP | Tied | UCP / NDP seat share | Within 4 pts | Within 2 pts | Within 1 pt | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2019 enacted | 87 | 44 | 43 | 43 | 1 | 49% / 49% | 12 | 3 | 1 | no majority (tie) |
| Commission majority | 89 | 45 | 42 | 46 | 1 | 47% / 52% | 11 | 4 | 1 | NDP majority |
| Commission minority | 89 | 45 | 53 | 36 | 0 | 60% / 40% | 10 | 4 | 3 | UCP majority |
| Advisory panel (reconstructed) | 91 | 46 | 44 | 46 | 1 | 48% / 51% | 12 | 4 | 1 | NDP majority |
| Panel minority ¶167 (reconstructed) | 91 | 46 | 43 | 47 | 1 | 47% / 52% | 12 | 4 | 1 | NDP majority |

The tie on four maps is the same riding. Red Deer-North is unchanged on the majority, panel and ¶167 maps, so 338's 45–45 carries over.

**Across 5,000 simulated elections:**

| Map | UCP seats, median (5th–95th) | NDP seats, median (5th–95th) | P(UCP majority) | P(NDP majority) | P(hung) |
|---|---:|---:|---:|---:|---:|
| 2019 enacted | 46 (35–62) | 41 (25–52) | 62% | 38% | 0% |
| Commission majority | 45 (34–64) | 44 (25–55) | 54% | 46% | 0% |
| Commission minority | 53 (34–67) | 36 (22–55) | 78% | 22% | 0% |
| Advisory panel (reconstructed) | 47 (35–66) | 44 (25–56) | 58% | 42% | 0% |
| Panel minority ¶167 (reconstructed) | 46 (36–65) | 45 (26–55) | 54% | 46% | 0% |

A hung legislature never happens. Every map has an odd number of seats, and only the UCP and NDP win seats (no "other" candidate came close in any draw), so whoever wins more seats has a majority. A hung result would need a tied riding, and ties only appear through 338's rounding at the point projection.

**What it takes.** The first column below is the province-wide UCP lead over the NDP (in points of the total vote) at which the UCP reaches a majority, with no local randomness. Below that lead, the NDP has the majority. On these maps there is no gap in between.

| Map | UCP lead needed for a UCP majority | UCP seats at a 50/50 vote, this projection | Same, audit (2023 votes) |
|---|---:|---:|---:|
| 2019 enacted | +4.3 | 39 of 87 (45%) | 41 of 87 (47%) |
| Commission majority | +5.4 | 40 of 89 (45%) | 42 of 89 (47%) |
| Commission minority | −0.2 | 46 of 89 (52%) | 46 of 89 (52%) |
| Advisory panel (reconstructed) | +5.3 | 42 of 91 (46%) | 45 of 91 (49%) |
| Panel minority ¶167 (reconstructed) | +5.4 | 41 of 91 (45%) | 44 of 91 (48%) |

Weighted by 2023 turnout, 338's riding numbers add up to UCP 47.6%, NDP 43.4%, a lead of **+4.2**. That is a little less than 338's headline of 48 to 43 (+5). At +5, the 2019 map would give the UCP a majority and the other three maps would still fall just short. Under this projection, every map except the minority's gives the UCP 2 to 3 fewer seats at a tied vote than 2023's votes did. The minority's map is the only one where a tied vote gives the UCP a majority.

## Map against map

These comparisons use the same draws on every map. The seat difference is the first map's count minus the second's in each draw. The maps have different numbers of seats, so the **UCP seat lead over the NDP** is the fairer comparison.

| Comparison | UCP seats: median (5th–95th) | UCP seat lead over NDP: median (5th–95th) | Draws with a different government | UCP majority only on first / only on second |
|---|---:|---:|---:|---:|
| panel − majority | +2 (+1 to +3) | +2 (0 to +4) | 4.4% | 4.4% / 0.0% |
| panel − 2019 | +1 (−1 to +5) | −2 (−6 to +6) | 5.8% | 1.0% / 4.9% |
| minority − majority | +6 (0 to +10) | +12 (0 to +20) | 24.1% | 24.1% / 0.0% |
| ¶167 − panel | −1 (−2 to +1) | −2 (−4 to +2) | 3.9% | 0.0% / 3.9% |
| majority − 2019 | −1 (−3 to +2) | −4 (−8 to +2) | 8.6% | 0.2% / 8.4% |
| minority − 2019 | +6 (−2 to +9) | +10 (−6 to +16) | 16.0% | 15.9% / 0.1% |
| minority − panel | +4 (−2 to +8) | +10 (−2 to +18) | 19.7% | 19.7% / 0.0% |
| ¶167 − majority | +1 (+1 to +2) | 0 (0 to +2) | 0.5% | 0.5% / 0.0% |

**Where the minority map's edge comes from.** In this projection Lethbridge and Red Deer lean NDP. The minority's map splits each city four ways and joins the pieces to rural areas, and all eight pieces go UCP. On the majority's map the same two cities give the NDP three seats and one tie. Several districts on Calgary's edge are also joined to Airdrie, Cochrane or Chestermere. The UCP wins 14 of the 29 districts with "Calgary" in their names on the minority's map, against 7 of 28 on the majority's. This describes what the lines do with these votes. It says nothing about why they were drawn.

**Panel against majority.** The panel's two extra seats are outside Calgary and Edmonton. The UCP gains three seats there and loses one in Edmonton.

## Does it hold up under other assumptions?

| Variant (same draws) | P(UCP maj.): 2019 | majority | minority | panel | ¶167 | Different govt: panel vs majority | panel vs 2019 | minority vs majority |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Main (proportional swing) | 62% | 54% | 78% | 58% | 54% | 4.4% | 5.8% | 24.1% |
| Additive swing | 62% | 54% | 78% | 58% | 54% | 4.3% | 6.0% | 24.4% |
| No riding-level noise | 50% | 42% | 76% | 43% | 42% | 0.5% | 7.4% | 33.8% |
| Riding noise × 1.5 | 68% | 59% | 77% | 63% | 60% | 4.6% | 7.1% | 18.6% |
| 338's ranges read as 95% intervals | 61% | 52% | 82% | 58% | 53% | 5.4% | 5.2% | 29.7% |

The swing method makes no difference. The amount of local randomness changes the headline chances: without it, the NDP is the slight favourite on the majority, panel and ¶167 maps. It does not change the order of the maps, which stays minority first for the UCP, then 2019, then panel, then majority and ¶167 about level. The median seat differences between maps barely move either (`out/results.json`).

## What this can and can't tell you

- **338 is a projection, not a poll.** It is built from polls and a model. If the polls miss, or 338's regional adjustments are off, every map moves with it. Our simulation only spreads outcomes as widely as 338's own ranges. 338 does not say what confidence level those ranges are, so we assumed 90%.
- **338's riding model already makes assumptions.** Its riding numbers come from "a mostly-proportional swing model adjusted with provincial and regional polls". We put a second swing step on top of theirs. On the 2019 map we reproduce their numbers exactly, but any regional pattern they got wrong carries straight through to every other map.
- **Whole-percent rounding.** 338 publishes whole percents, so each riding's numbers can be off by up to half a point per party. Red Deer-North's exact tie comes from this rounding. Seats within 1 or 2 points at the point projection are really undecided.
- **Inside each district, we assume the change looks like 2023.** Proportional swing assumes a party gains or loses everywhere in a district in proportion to its 2023 vote; additive swing assumes it moves by the same points everywhere. The two agree here, but both are assumptions. Real swings are uneven (newer suburbs can move differently from older neighbourhoods), and uneven swings decide exactly the seats that new maps create by cutting old districts in new places. This does not matter on the 2019 map, where the totals are 338's by construction. It does matter on the other four.
- **Voting areas and turnout are from 2023.** Each voting area keeps its 2023 number of voters, so growth since then (fast-growing suburbs and commuter towns) is not counted. The 2023 ballots not cast on election day are placed by the audit's rule, not observed. Separately, 338's own 2023 baseline differs from the official count in a few ridings (largest: Cardston-Siksika, 70.3% against 74.1%). That does not change the targets, which are 338's projections.
- **The panel's map and the ¶167 map are reconstructions** from the panel's report, not official shapefiles. About 245 voting areas are cut by reconstructed lines. The audit found that the seats that differ between those two maps depend on such areas. Treat a difference of a seat or two involving these maps as within the reconstruction's error.
- **The riding-level noise is tied to the 2019 districts,** so that every map faces the same draws. A new district built from pieces of several old ones therefore averages their noise, which gives slightly less local randomness to maps that cut old districts more.
- **"Other" parties are lumped together.** None wins a seat in any draw, so a strong local independent or third-party candidate is not modelled.
- **What it cannot tell you:** why any line was drawn, whether a map is lawful or fair, or what will happen on election day. It uses one snapshot of polling, from October 19, 2026.

## Files

All files are in this folder, `p338/sim/`.

- `simulate_338.py` runs the whole simulation; `make_tables.py` builds the tables. Run them in that order with `python3 -I -W ignore`. They take about 3 minutes.
- `out/results.json` holds every number above, plus the checks and diagnostics.
- `out/districts_<map>.csv` has one file per map (`map2019`, `majority`, `minority`, `panel`, `para167`) and one row per district. Each row has 2023 shares, projected shares under both methods, the projected winner, the margin, close-seat flags, and the share of simulated elections each party wins. The 2019 file also has 338's own numbers and ranges and the single-pass check.
- `out/seats_vs_lead.csv` gives UCP and NDP seats on every map at each province-wide lead from about −16 to +24 points, without local randomness.
- `out/tables.md` contains the generated tables.
- `inputs/` holds copies of the audit files used, with `SHA256SUMS.txt`.

## The chart: "The new map: 91 seats."

`data/maps/article/same_votes_five_maps.png` (1080×1350, rendered at 2×) is for a general reader. It centres on the panel's 91-seat map now before MLAs and reads it two ways, as Wuff framed it: one view speaks to today's politics on the map, the other to the map itself.

1. **Today's polls** (today's politics on this map): UCP 44, NDP 46, 1 exact tie. Source: `out/results.json` `point.panel.proportional`. With NDP exactly on the 46-seat majority line and one tie, the chart calls it "Too close to call".
2. **Typical of 5,000 simulated elections** (what this map tends to do around today's numbers): UCP 47, NDP 44; the UCP wins a majority 58% of the time. Source: `mc.main.maps.panel` `ucp_median`, `ndp_median` and `p_ucp_majority`.
3. **Why they differ:** at today's numbers, 11 of the NDP's 46 projected wins on this map are by less than 4 points, against 2 of the UCP's 44 (`out/districts_panel.csv`). Polling error tips more of the NDP's narrow leads.

**Reference table, same two readings:**

| Map | Today's polls | Typical simulation | UCP majority |
|---|---|---|---|
| Panel members' alternative (91) | 43–47 | 46–45 | 54% |
| Current map, since 2019 (87) | 43–43 | 46–41 | 62% |
| Commission's map (89) | 42–46 | 45–44 | 54% |
| Dissenting commissioners' map (89) | 53–36 | 53–36 | 78% |

**Punchline:** "The new map isn't the outlier. The dissenting commissioners' map was." It holds on both readings.

The chart counts seats only, and the footer points to the audit's local checks, such as the Lethbridge split. Source: `meme/same_votes_five_maps.html`; render with `node meme/render.cjs` (Playwright, Chromium).
