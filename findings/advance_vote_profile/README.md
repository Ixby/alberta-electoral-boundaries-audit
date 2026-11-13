# Where did the early voters live? Placing 2023's early ballots with rule P

2026-11-10 01:33 Alberta time · claude-opus-5-5 · medium

**Status: registered (Amendment 14).** Rule P is the registered way to place 2023's early ballots when scoring the November map. Amendment 14 was signed on 2026-11-10 at 13:22 Alberta time and filed on OSF (project 9wp5y, update 6af36f7fe50e8122e3826eba). Amendment 12's rule (called M0 below) is reported beside it as a sensitivity (Amendment 14, Part 4). The scorecard under P, scored after signing, is in `scorecard_p.md`. This folder gives the evidence for the rule and its results. It says nothing about whether any map is a gerrymander.

**Not blind.** This rule was chosen after the audit had already seen that placing early ballots by each party's local strength moves the all-ballots results against the commission minority's map (from 55 to 57 UCP seats, and an efficiency gap from +2.55% to +5.64%). The choice was made knowing which way it cuts. The evidence below uses no map, and it would read the same whichever way the seats moved. A reader should still weigh the timing. Amendment 14 says this in its status line.

## The answer first

- **The rule.** Rule P places each division's early ballots only among the people on the list who did not vote on election day. Each area keeps its own election-day lean.
- **The lean.** Provincial evidence puts the strength of that lean at about 1, that is, early voters lean the same way as their election-day neighbours. The honest range is **0.87 to 1.22**. The value used is **1.0**.
- **The 100% limit.** Under P no voting station passes 100% turnout, except two tiny stations that already pass it on election day alone. Under M0, 26 stations pass 100%.
- **Seats, as ranges over that lean.** At all eight lean values run from 0.87 to 1.22, no seat moves on any map. Under P: 2019 map **49–38**, majority **48–41**, minority **57–32**, panel reconstruction v3 **50–41**, paragraph 167 reconstruction **50–41**. Under M0 the minority is 55–34 and the panel reconstruction 51–40. The others are the same.
- **What changes.** Three seats, all close. On the minority map, Calgary-Edgemont (NDP by 4 modelled votes under M0, UCP by 401 under P) and Calgary-Glenmore (NDP by 24, UCP by 68). On the panel reconstruction, Banff-Canmore-Diamond Valley (UCP by 229, NDP by 1,276).
- **The range is too narrow to trust alone.** It covers only the strength of the lean. The provincial data cannot soundly measure how far P misses in a single station. A seat won by 68 modelled votes should not be read as settled.
- **The comparison maps.** The redraw-test null was rescored here under P. The canonical ensemble and sets A to D were replayed on the machine that holds their chains (32 of 36 chains pass; the four Forest-ReCom chains fail and are dropped). Under P the minority's efficiency gap of +5.64% is at the 99.98th percentile of the canonical ensemble and above P1's line of +2.15%; 192 of 1,010,000 plans reach it. See "The other comparison sets" below.

## The problem

In 2023, 809,660 of 1,706,304 two-party ballots (47.45%) were not cast on election day. They were cast at advance polls, through "Vote Anywhere" (an advance ballot cast outside your own division), by special ballot (mail and the returning office), or at mobile polls in care homes. "Two-party" means NDP plus UCP.

Elections Alberta reports these early ballots only as a total for each 2019 division. To score a new map, the audit has to place them among the division's voting areas. A voting area is the smallest unit Elections Alberta draws. Where a new boundary cuts an old division, the placement decides which new district the ballots land in.

The early ballots leaned NDP: 48.84% NDP against 42.60% on election day, a gap of 6.25 points. The NDP did better off election day in 83 of 87 divisions. Every rule here keeps each division's official totals exactly, so this lean is never lost. Only the placement inside a division is a model.

## Rule P

Rule P has two parts.

**Who gets the ballots (the count side).** An early ballot can only belong to someone on the list who did not vote on election day. Anything else would be illegal. So P gives each station a share of the division's early ballots equal to its share of the division's election-day non-voters. Election-day non-voters are the names on the list minus the election-day ballots. There is no blend with election-day votes. The "count dial" λ is 1 exactly, by rule, not by estimate.

**Which party (the lean side).** Each area keeps its own election-day lean, after the division-wide shift toward the NDP. A lean strength of 0 would give every area the division's one mix (that is M0's choice). A strength of 1 means early voters share the whole of their neighbours' lean. The strength is measured on a log-odds scale, a standard way to compare party shares that keeps them between 0% and 100%.

P uses no number from any federal election.

The one tuning number left is a small pull toward the division's share for very small areas (10 ballots' worth). It keeps a station with a handful of votes from getting an extreme share.

## How strong is the lean?

Two provincial tests have a partly known answer. Both ask the same thing: inside a division, do early voters near NDP-leaning stations lean NDP too?

**The 2023 advance polls, placed on the map** (`04_provincial_location_tests.py`, `06_robustness.py`). The 2023 results name 254 advance polls with their own counts. 151 were found in OpenStreetMap inside their own division. That leaves 123 polls in 54 divisions with at least two located polls. Each voting area was given to its nearest located poll.

- The lean strength is **1.00 (± 0.07)**. Under M0 it would be 0. When results are reshuffled as if M0 were true, the test returns 0.00 ± 0.02, so the test can tell the two apart.
- Resampling whole divisions gives a 95% range of **0.87 to 1.22**. This is the range used below.
- Other reasonable ways of fitting give 0.88 (every poll counted equally) and 1.13 (without West Yellowhead and Banff-Kananaskis, which carry 66% of the weight).
- The polls cover 261,493 of 575,496 in-division advance ballots (45.4%). Vote Anywhere and special ballots (212,562) are not tested by anything provincial.
- "Nearest poll" is a rough guess at who uses a poll. Rough guesses blur real differences.

**2015 town-named polls.** In 2015 rural advance polls and election-day polls were both named for towns. Matching names gives 36 advance polls in 12 divisions. The lean strength is **0.99 (± 0.20)**. That is a small sample, from eight years earlier, with three parties.

So the estimate is about 1, the honest range is 0.87 to 1.22, and the value used is 1.0. The provincial evidence gives no reason to move off 1.0.

## The 100% limit

### What "Names on List" counts

The 2023 results workbook gives "Names on List" for each of the 1,216 election-day stations, 2,939,762 in total (`07_turnout_and_count.py`).

- That total equals the "Names on List" in Table 29 of Elections Alberta's 2023 report (p. 131). Division by division, it equals the report's Appendix D, the Post Election Day List of Electors, in all 86 divisions the text extraction could read. The 87th, Airdrie-East, was dropped by the extraction; it equals what is left of the total.
- So "Names on List" is the **Post Election Day List of Electors**, a snapshot as of March 26, 2024 (p. 62).
- The report says that list was updated from "all voting records, declarations, and oaths" (p. 62), and that "new electors are reflected in the correct electoral division and voting area" (p. 131). 248,688 electors registered at a voting place, in advance or on election day (p. 61).
- **What follows.** Electors who registered at the poll on election day are most likely on the list, in the voting area where they live. That rests on the report's general description. The report does not say it station by station, so it is **not established** for any one station. People who died or moved before March 2024 were removed, so a few voters may be missing from the list.

### Stations already over 100% on election day

Two stations are over 100% on election day alone. No station is at exactly 100%.

| Station | Names on list | Election-day ballots | Turnout | Most plausible reason |
|---|---:|---:|---:|---|
| Remote Area - Fort Fitzgerald (division 61, area 036) | 2 | 15 | 750% | People who live or work nearby but are listed elsewhere, or who registered at the poll and were placed in another voting area. Cannot tell from the data. |
| Calgary Drop In Centre (division 04, area 064) | 9 | 21 | 233% | A homeless shelter. Most plausibly voters with no fixed address registered there, and the March 2024 list counts only those still listed there. Not established. |

### The hard check

Under P, no station passes 100% unless it already did on election day. This holds for every lean strength, because the count side does not depend on it. The reason is simple. In every division, early ballots are fewer than election-day non-voters (at most 59% of them, in Calgary-North West). So each station gets fewer early ballots than it has non-voters. The two stations above get no early ballots under P and stay where election day put them. The check passes in `05_models_headlines.py` and `07_turnout_and_count.py`. It is not forced; it follows from take-up being below 1 in every division, and the scripts stop if that ever fails.

### The turnout distribution

Station turnout here means election-day ballots plus placed early ballots, divided by names on the list. Each bin includes its upper edge.

| Turnout | Election day alone | M0 | P |
|---|---:|---:|---:|
| 0 to 5% | 3 | 2 | 0 |
| 5 to 10% | 1 | 1 | 0 |
| 10 to 15% | 16 | 1 | 0 |
| 15 to 20% | 17 | 5 | 0 |
| 20 to 25% | 107 | 8 | 0 |
| 25 to 30% | 266 | 8 | 0 |
| 30 to 35% | 294 | 11 | 4 |
| 35 to 40% | 202 | 23 | 12 |
| 40 to 45% | 117 | 55 | 31 |
| 45 to 50% | 99 | 87 | 73 |
| 50 to 55% | 55 | 153 | 128 |
| 55 to 60% | 27 | 150 | 226 |
| 60 to 65% | 6 | 164 | 310 |
| 65 to 70% | 2 | 168 | 278 |
| 70 to 75% | 2 | 113 | 135 |
| 75 to 80% | 0 | 85 | 13 |
| 80 to 85% | 0 | 65 | 4 |
| 85 to 90% | 0 | 39 | 0 |
| 90 to 95% | 0 | 32 | 0 |
| 95 to 100% | 0 | 20 | 0 |
| over 100% | 2 | 26 | 2 |

| Percentile | Election day alone | M0 | P |
|---|---:|---:|---:|
| 1 | 12.7% | 21.5% | 39.4% |
| 5 | 21.5% | 40.2% | 46.3% |
| 25 | 28.1% | 53.3% | 56.6% |
| 50 (middle station) | 33.3% | 62.7% | 62.2% |
| 75 | 40.5% | 73.2% | 67.0% |
| 95 | 52.8% | 92.7% | 72.6% |
| 99 | 59.7% | 108.4% | 77.1% |
| Highest | 750.0% | 1294.9% | 750.0% |

- **M0 is impossible in places.** It gives early ballots to the stations that were busiest on election day. That pushes 26 stations past 100% and 46 past 95%: 26 of 1,216 stations get more early ballots than they have election-day non-voters. This is evidence against M0's count side.
- **P is possible everywhere it can be.** Its only stations over 100% are the two above.
- **P makes turnout more even.** Inside a division, station turnouts typically differ by 2.9 points under P (one standard deviation, middle division), against 5.1 on election day alone and 10.0 under M0. Whether real turnout was that even cannot be checked: no source counts early voters by station.

## Does P's count side hold?

P assumes that, inside a division, the same share of election-day non-voters voted early at every station. Call that share the early take-up. Two provincial looks bear on it (`07_turnout_and_count.py`).

- **Across the 87 divisions.** Take-up runs from 24% (Calgary-East) to 59% (Calgary-North West), middle 42%. Divisions with higher election-day turnout had somewhat higher take-up (correlation 0.21; a link this strong would arise by chance about 1 time in 20 (p = 0.05), so it is borderline). The link shows in Calgary, Edmonton and the smaller cities (rank correlations 0.36 to 0.40, none clear on its own), not in rural divisions (−0.06).
- **Inside divisions, at the located advance polls.** The same link is weak and not distinguishable from zero (correlation 0.12 within divisions; slope 2.6 ± 2.0 on the log scale).
- **What it means.** If the cross-division link also holds inside divisions, P puts slightly too few early ballots in high-turnout areas and slightly too many in low-turnout areas. The data do not show that it holds inside divisions. They do not show that it does not.
- **What the data cannot say.** Who voted early at any station. Divisions differ in poll sites, hours, distances and campaigns, so a link between divisions is not a link inside one. The located polls are nearest-poll guesses, and a poll's count depends on its size and hours. Vote Anywhere, special and mobile ballots, about 29% of early two-party ballots, are not covered.

## How far could P be wrong?

The only provincial place to measure P's own miss is the 123 located polls (`06_robustness.py`). There, a poll's early party share scatters around P's line by 0.17 on the log-odds scale beyond counting noise. Its ballot count scatters around P's count side by 0.78 on the log scale.

**That is not a sound error model for stations, so it is not used.** The scatter mixes P's own error with the error of guessing who uses each poll. A poll's count depends on its hours and size. Polls are larger than stations, and nothing provincial shows how the error shrinks or grows at a station, or whether neighbouring stations err together.

So the ranges below vary only the lean strength, over 0.87 to 1.22, computed at eight values of the lean (0.87, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.22), not as a continuous sweep. They are narrower than the true uncertainty.

## Results on every map

Scripts: `05_models_headlines.py`. Formulas: the audit's own (`analysis/scripts/mcmc_ensemble.py`, `seat_results`). Voting areas go to districts by a point inside each area, the audit's rule. M0 is read straight from Amendment 12's filed vote file; the M0 rebuilt here matches it to a millionth of a vote.

Plain meanings:
- **Efficiency gap.** The difference between the two parties' "wasted" votes (votes for a loser, and a winner's votes beyond what it needed), as a share of all votes. Positive favours the UCP.
- **Mean-median.** The middle district's UCP share minus the average district's. Positive favours the UCP.
- **UCP seats at a tied vote.** UCP seats if every district shifted by the same amount until the province was 50–50.
- **Close seats.** Two-party margin of 4 points or less.

| Map | Rule | UCP–NDP seats | Efficiency gap | Mean-median | UCP seats at a tied vote | Close seats |
|---|---|---:|---:|---:|---:|---:|
| 2019 map (87) | M0 | 49–38 | −2.64% | −2.22% | 41 | 12 |
| | P | 49–38 | −2.64% | −2.22% | 41 | 12 |
| Commission majority (89) | M0 | 48–41 | −2.70% | −3.51% | 42 | 11 |
| | P | 48–41 | −2.83% | −3.81 to −3.74% (−3.77 at lean 1.0) | 42 | 11 |
| Commission minority (89) | M0 | 55–34 | +2.55% | +0.08% | 46 | 7 |
| | P | 57–32 | +5.64% | +0.44 to +0.54% (+0.51 at lean 1.0) | 46 | 8 to 9 (9 at lean 1.0) |
| Panel reconstruction v3 (91) | M0 | 51–40 | −1.66% | −1.09% | 45 | 10 |
| | P | 50–41 | −2.84% | −0.55 to −0.35% (−0.47 at lean 1.0) | 45 | 9 |
| Paragraph 167 reconstruction (91) | M0 | 50–41 | −2.19% | −2.90% | 44 | 10 |
| | P | 50–41 | −2.33% | −2.28 to −2.03% (−2.18 at lean 1.0) | 44 | 10 |

Where P differs across the lean, its range over the eight lean values from 0.87 to 1.22 comes first, with the lean-1.0 value in brackets; a single P figure is the same at every lean value. Seats, efficiency gaps and tied-vote seats do not move across those values on any map. (Under P a district's total ballots do not depend on the lean, and the efficiency gap then depends only on who wins each seat.) The 2019 map gives the same figures under both rules because its districts are the 2019 divisions, whose official totals both rules keep.

**Checks, all passed** (printed by `05_models_headlines.py`, stored in `outputs/headline.json`):
1. Every division's official NDP, UCP and other totals are returned exactly, under M0 and every P (largest difference about one billionth of a vote).
2. The 2019 map gives 49–38 under M0 and every P.
3. No station passes 100% under P beyond the two already over on election day.
4. The rebuilt M0 equals Amendment 12's filed vote file.

### The seats that change

| Map | District | M0 margin | P margin over 0.87 to 1.22 (eight lean values) | P margin at lean 1.0 |
|---|---|---|---|---|
| Minority | Calgary-Edgemont | NDP by 4 | UCP by 349 to 488 | UCP by 401 |
| Minority | Calgary-Glenmore | NDP by 24 | UCP by 59 to 83 | UCP by 68 |
| Panel v3 | Banff-Canmore-Diamond Valley | UCP by 229 | NDP by 1,105 to 1,547 | NDP by 1,276 |

Margins are modelled votes (UCP minus NDP). Under M0 the two minority seats hung on 4 and 24 modelled votes. Under P, Calgary-Glenmore hangs on 59 to 83 (68 at lean 1.0). On the majority, panel and paragraph 167 maps, Calgary-Acadia is UCP by 34 to 43 under P (38 at lean 1.0). Every district's margins are in `outputs/district_margins.csv`.

On the minority map the efficiency gap moves in two steps, one per seat. Nothing moved smoothly.

## The comparison maps (ensembles)

The audit ranks each map against computer-drawn maps. Each set is listed below, with where its maps are.

| Set | Its maps | Rescored under P here? |
|---|---|---|
| Redraw-test null for R1 and R2 (Amendments 8 and 13), built for the provisional panel reconstruction | Stored in this repository (`findings/a10_stepc/territory/`, 2,000 maps) | **Yes** |
| Canonical, 87 districts, 1,010,000 maps | Not stored. Rebuilt only by rerunning the chains. Election-day scores are here. | No: far too slow here; see `REPLAY.md` |
| Set D, 91 districts, s.15(2), 1,010,000 maps | Chains on the machine with the `alberta_audit` clone | No: see `REPLAY.md` |
| Sets A, B and C, 89 and 91 districts | Chains on that machine (set A's chains 201 and 100 are here but fail to replay, Amendment 13) | No: see `REPLAY.md` |
| Forest-ReCom Phase A (robustness check) | Not stored; election-day scores are here | No: see `REPLAY.md` |

**The redraw-test null under P** (`09_rescore_territory_null.py`). The map it was built for is the provisional panel reconstruction (`iap_2026_assembled.gpkg`). Each test flags at p < 0.05.

| Test | M0: value, p | P: value, p |
|---|---|---|
| R1, efficiency gap | −1.66%, p = 0.914 | −2.84%, p = 0.619 |
| R2, neighbour-drain | 0.01043, p = 0.419 | 0.00053, p = 0.576 |
| Mean-median (reported) | −1.09%, p = 0.912 | −0.47%, p = 0.981 |
| Declination (reported) | −0.060, p = 0.794 | −0.080, p = 0.639 |
| UCP seats (reported) | 51, p = 1.000 | 50, p = 0.853 |

Neither R1 nor R2 flags under either rule. The M0 rescore here matches the filed all-ballots result exactly, which checks the scoring code.

### The other comparison sets, replayed on the machine that holds them (2026-11-10 13:15 Alberta time · claude-opus-5-5 · medium)

The canonical ensemble and sets A to D were rerun on the P vote file on the PC that holds their chains (`outputs/replay_p_run.md`). Each rerun drew the same plans as the original: every column that does not depend on votes matches, row for row, in all 32 chains. The four Forest-ReCom chains did not match on one column (`population_mad`, in 391 to 451 of 25,000 rows, by at most 9.1×10⁻¹³) and were dropped, as Amendment 13 requires.

Efficiency gap under P, as a midrank percentile of the plans that passed (higher means more UCP-favouring; `outputs/ensemble_ranks_p.json`):

| Set | 2019 map | Majority | Minority | Panel (v3) | ¶167 map |
|---|---|---|---|---|---|
| Canonical (87) | 21.05 | 18.41 | 99.98 | 18.31 | 25.78 |
| A (89 / 91) | | 18.86 | 99.99 | 19.10 | 27.22 |
| B (89 / 91) | | 18.84 | 99.98 | 18.82 | 26.68 |
| C (89 / 91) | | 35.47 | 100.00 | 35.76 | 46.46 |
| D (91, s.15(2)) | | | | 18.85 | 26.70 |

The threshold lines under P are in `outputs/thresholds_p.json` (`11_thresholds_p.py`, run on that machine): P1's line, the 95th percentile of the canonical efficiency gap, is +2.15%, and 192 of 1,010,000 plans reach the minority's +5.64%. On M0's file the same rule gives +1.39%. S5's midpoint is 0.00588, but under P the two commission maps' drain scores swap order (majority 0.00403, minority 0.00773). Amendment 14, Part 3 sets S5 aside on the P file: it gives no flag to any map and counts as not flagged. The author chose this after the replay, knowing its effect: read as written, S5 would flag the majority, the panel reconstruction (drain 0.00053) and the ¶167 map, and not the minority, which would put the panel reconstruction at 3 of 5 (`scorecard_p.md`). The drain scores and the midpoint are reported beside the result.

## The vote file

`08_build_vote_file_p.py` writes `data/shapefiles/derived/va_polygons_all_2023_ballots_p.gpkg`.

- It is built the same way as Amendment 12's file (`va_polygons_all_2023_ballots_primary.gpkg`, from `analysis/scripts/vote_anywhere_splat.py --primary`): the election-day file, same rows and shapes, with the NDP, UCP and other columns replaced by all ballots.
- Size 22,040,576 bytes. SHA-256 `bf9b27226e457ddb4b8c2feaa77f7402d1c3d1284657c821d208f6597b8f73bd`. A rebuild gives the same bytes.
- Every division's official totals hold. Compared with M0, P puts 84,506 two-party votes in different voting areas.
- Git: the registered sibling file is tracked by Git LFS. This file matches the repository's LFS pattern (`*.gpkg`) but is not committed.

## What cannot be known

- **Where any early voter lives.** Every rule here is a model. The tests show which model is closer on average, not what happened in a given area.
- **Whether take-up was even inside a division.** P assumes it. The data neither confirm nor rule it out.
- **How far P misses at a single station.** No sound provincial measure exists. The ranges here cover the lean strength only.
- **Vote Anywhere and special ballots** (212,562 two-party ballots, 12.5% of the total). They have no location at all. They are placed like the other early ballots.
- **Mobile polls.** Cast in named care homes; placed with the rest. They are 1.3% of the vote.
- **Below the station.** Election-day votes are split equally among a station's voting areas (the audit's existing rule). P inherits that.
- **Exactly who is on each station's list.** The list is the March 2024 list, not the list on election day.
- **The 96 advance polls not found** on the map, and two lookups lost to rate limits. 55% of in-division advance ballots are outside the location test.
- **Competitive-seat flags under P.** Not computed. `ensemble_ranks_p.json` gives each map's percentile but not each set's 5th percentile, which the flag needs (`scorecard_p.md`).

## What was adopted

Amendment 14 (`findings/pre_registration_amendment_log.md`) adopts P for the scoring of the November map.

1. It names P, its lean of 1.0 and its count dial of 1, and it says that P was chosen after its effect on the maps was known (see "Not blind").
2. The vote file above is fixed by its hash (Part 2).
3. The replays in `REPLAY.md` pass their row-for-row check in 32 of 36 chains; Forest-ReCom is dropped (Part 3). The threshold lines come from them (`outputs/thresholds_p.json`). S5 is set aside on the P file and counts as not flagged (Part 3).
4. Every vote-based result is reported three ways: under P (registered), under M0 (sensitivity) and on election-day ballots (sensitivity) (Part 4). P's seats are reported with their range across the lean, 0.87 to 1.22, and a seat decided by fewer modelled votes than the change across that range is named as too close to call (Part 5).
5. It does not reopen the registered Phase 1 results.

The scorecard under P, with M0 beside it, is in `scorecard_p.md`; the panel and ¶167 maps are the audit's reconstructions, so their counts are provisional. Structural and partisan counts under P: panel reconstruction 2 of 5 and 1 of 4; majority 0 of 5 and 0 of 4; minority 4 of 5 (replicated) and 4 of 4 (present); ¶167 map 2 of 5 and 0 of 4. Under M0 the minority's structural count is 5 of 5.

## Files

| File | What it does |
|---|---|
| `01_measure_skew.py` | How early ballots differ from election-day ballots, 2023 and 2015 |
| `03_geocode_advance_polls.py` | Looked up the named 2023 advance polls; the results are kept in `inputs/advance_poll_geocodes.csv`. Do not rerun unless you mean to rebuild them. |
| `04_provincial_location_tests.py` | The located-poll test (2023) and the town-name test (2015) |
| `06_robustness.py` | Other fits, placebos, leverage, coverage, and P's scatter at the located polls (seed 20261110) |
| `07_turnout_and_count.py` | What "Names on List" counts, station turnout, the hard check, P's count assumption |
| `05_models_headlines.py` | M0 and P on all five maps, the checks, the seats that change |
| `08_build_vote_file_p.py` | The P vote file |
| `09_rescore_territory_null.py` | The redraw-test null rescored under P |
| `10_replay_p.py` | Commands, check and ranking for the replays on another machine |
| `11_thresholds_p.py` | P1's and S5's lines from the replayed canonical ensemble |
| `12_scorecard_p.py`, `scorecard_p.md` | The scorecard under P, with M0 beside it |
| `REPLAY.md` | What to run there, the checks, what to bring back |
| `_models.py`, `_common.py` | The rules, the loaders, the output helpers |
| `inputs/advance_poll_geocodes.csv` | Geocodes for the advance polls (252 rows, 156 located; cannot be regenerated bit for bit, as OpenStreetMap changes daily) |
| `inputs/ea_2023_report_appendix_c_d.csv` | Appendices C and D of the Elections Alberta 2023 report, copied from the PDF text (86 divisions; Airdrie-East was lost in extraction) |
| `outputs/SCHEMA.md` | Every output file and its columns |
| `sources.md` | Every outside source, when it was fetched, and what it says |

Run order, from the repository root: 01, 04, 06, 07, 05, 08, 09, then `10_replay_p.py check`. For example `python findings/advance_vote_profile/01_measure_skew.py`. In a worktree where large files are LFS pointers, set `AVP_DATA_ROOT` to a checkout that holds the real files.
