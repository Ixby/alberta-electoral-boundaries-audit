# Where did the advance voters live? Testing how to spread 2023's non-election-day ballots

2026-11-09 23:15 Alberta time · claude-fable-5-2 · medium

**Status: exploratory, not registered.** Nothing here changes the audit's registered method. The registered rule for spreading these ballots is Amendment 12. Changing it needs a new amendment that the author signs, and a replay of the comparison maps (the "ensembles") on the new vote file. This folder gives the evidence for that decision. It gives no conclusion on whether any map is a gerrymander.

**Not blind.** This rule was studied and recommended on 2026-11-09, after the audit had already seen that a party-specific spread moves the all-ballots results against the commission minority's map (55 to 57 UCP seats, efficiency gap +2.55% to about +5.6%). The choice of R was made knowing which way it cuts. The evidence for the rule (the federal test and the provincial advance polls) uses no map and would read the same whichever way the seats moved, but a reader should weigh the timing. Amendment 12 carried a statement of this kind; any amendment adopting R must carry one too.

An independent verifier re-derived the four main claims and confirmed them with corrections (`audit2/verify-advance.json` in the session scratchpad). Those corrections are applied in this version. Scripts 06 and 07 rebuild the verifier's extra checks.

## The short version

- In 2023, 809,660 of 1,706,304 two-party ballots (47.5%) were not cast on election day. Elections Alberta reports them only per 2019 division.
- Those ballots leaned NDP: 48.8% NDP against 42.6% on election day, a gap of 6.2 points province-wide (42.60% against 48.84%) and 4.8 points inside the average division.
- The audit's current rule (M0) gives every voting area in a division the same party mix for these ballots. **The evidence rejects that.** In every test with a known answer, advance voters lean the same way as their election-day neighbours, almost one for one.
- The rule the evidence supports (R) keeps each area's own lean and spreads the ballots by where people did *not* vote on election day. Its two numbers are borrowed from federal elections. Nothing provincial pins the second one.
- Seats under R, as ranges: **minority 56 to 57** UCP seats (55 under M0), **majority 47 to 49** (48 under M0), panel reconstruction 49 to 51 (51 under M0). The point values are 57, 48 and 50. Seats at a tied vote do not move.
- **The whole change on the minority map is two seats**: Calgary-Glenmore (UCP by 66 modelled votes under R) and Calgary-Edgemont (UCP by 384). The efficiency gap moves in steps with those two flips: +2.6% with neither, about +4.0% to +4.6% with one, +5.6% with both. Nothing shifted smoothly by 3 points.
- The rule is well supported. The point seat counts under it are not. With the rule's own error included, the minority map shows 57 in roughly 60% to 76% of draws, and the majority map shows 48 in about 51% to 57%.
- What stays unknown: the home voting area of any single advance voter. The provincial results cannot show it.

## What was asked

The author's direction: mimic the election-day pattern, but advance votes skew, so find what that skew looks like in Alberta and apply it. Test every assumption against the data we hold and against public and academic knowledge. Aim for the most faithful picture possible.

Two things have to be settled. They are separate.

1. **The skew** (how the party mix of early ballots differs from election day). This is observed for every division. No rule can get it wrong, because every rule here returns each division's official totals.
2. **The spread** (which voting areas inside a division those ballots belong to). This is not observed. It matters only where a new district line cuts an old division, which is most of them.

## What the evidence says about the profile

### From the data we hold

Source: `data/raw/2023_results.xlsx`, all 1,973 poll rows in 87 divisions. Script: `01_measure_skew.py`. "NDP share" means NDP ÷ (NDP + UCP).

| 2023 ballot type | Two-party ballots | NDP share | Against election day |
|---|---:|---:|---:|
| Election day | 896,644 | 42.6% | — |
| Advance, voted inside own division | 575,496 | 47.1% | +4.5 |
| Advance, "Vote Anywhere" (voted outside own division) | 162,165 | 54.1% | +11.5 |
| Special ballot (mail and returning office) | 50,397 | 54.9% | +12.3 |
| Mobile polls (care homes and similar) | 21,602 | 42.7% | +0.1 |
| All non-election-day | 809,660 | 48.8% | +6.2 |

- **Nearly every division shows it.** The NDP did better off election day in 83 of 87 divisions. The average division gap is +4.8 points (middle value +4.7, spread ±3.0). The largest is Banff-Kananaskis at +12.0. The largest the other way is Peace River at −7.1.
- **By place.** Calgary +3.6 points, Edmonton +6.3, smaller cities and suburbs +6.9, rural +6.0. Calgary's skew is the smallest. Calgary also votes early the most: 51% of its two-party ballots, against 45% in rural divisions.
- **By how close the division was.** Close divisions (election-day margin under 10 points) +4.0; middling +5.4; safe +6.5. The link is weak and not statistically clear (rank correlation with margin 0.03).
- **The skew is a shift, not a reshuffle.** Across the 87 divisions, the early vote follows the election-day vote one for one, with a constant push toward the NDP. On the log-odds scale (the usual scale for comparing shares near 0 or 1) the slope is 1.00 ± 0.02 and the correlation is 0.98. A division that is 10 points more NDP on election day is about 10 points more NDP among early voters too.
- **Advance polls inside one division do not agree with each other.** The workbook names 254 advance polls with their own counts, two or more in 80 divisions. Under M0 they should all show the same mix, give or take chance. They do not: the middle gap between a division's most and least NDP advance poll is 9.3 points, and a standard test of "same mix" fails overwhelmingly (chi-square 8,771 on 162 degrees of freedom). Divisions whose election-day stations vary more also have advance polls that vary more (rank correlation 0.55).
- **2015** (`data/raw/2015_results.xlsx`, NDP against PC + Wildrose). Advance ballots were only 16% of the vote. They leaned NDP by +2.6 points province-wide, but the average division showed no lean (−0.3 ± 4.5). Calgary leaned the other way (−3.3). Mobile polls were strongly anti-NDP (−11.2). The one-for-one pattern across divisions held (slope 1.08 ± 0.03).
- **2019.** The repository holds no 2019 poll-level results, only division totals. 2019 could not be measured.

So the *size and even the sign* of the skew change from election to election. The *shape* does not: early voters track their election-day neighbours.

### From public and academic sources

Full list with URLs, access times and what each says: `sources.md`. Anything not read in full is marked there.

- **Elections Alberta, 2023 general election report** (read in full). Advance ballots were 42.9% of valid votes, up from 36.7% in 2019 and 15.8% in 2015. 22% of advance ballots used Vote Anywhere (31.9% in 2019). **Advance voters are older**: 29.6% were 65 or over, against 24.4% of the list of electors; 5.8% were 18 to 24, against 8.9%. Edmonton and Calgary divisions had two to three advance polls each, other divisions about five, placed so that no one should travel more than 100 km. The report gives no party figures by voting method and nothing below the division.
- **Elections Canada, turnout by age, 2025 report** (read in full). Nationally, over half of voters aged 65 and up used advance polls or special ballots in 2021 and 2025, against about 30% to 37% of voters under 45.
- **Loewen, House of Commons committee testimony, 2007**, on the 2006 Canadian Election Study (read in full): older, more interested, party-identified and party-contacted citizens are more likely to vote in advance.
- **Garnett, 2016 conference paper** (read in full; a draft, used only as a guide to the literature): older voters vote early more in all four countries studied, but the age gap in Canada is small; most studies find early voters are older and more engaged, and the evidence on income and education is mixed.
- **Not found:** any published analysis of Alberta 2023 advance votes below the division; any Canadian study of distance to advance polls. The earlier audit note that party-specific spreading is "the usual practice" in US precinct data could not be confirmed and stays unverified.

One thing the age profile alone would not predict: Alberta's 2023 early vote leaned NDP, although early voters are older. (That older voters lean conservative is assumed here from general knowledge. It is not sourced.) Our own federal count (below) shows the opposite sign in the same province: federal advance voters in Alberta leaned Conservative by 7 to 8 points in 2019 and 2021. The skew depends on the campaign. That is why the rule should take the skew from each division's own official totals, which all rules here do, and should not import a skew from anywhere else.

## What the data can and cannot pin down

| In the data | What it identifies |
|---|---|
| 254 named advance polls with counts (2023) | The party mix of early voters differs from place to place inside a division. With a location for each poll, roughly which side of the division leans which way. |
| "Names on List" for all 1,216 election-day stations (2,939,762 electors) | How many electors in each station's area did **not** vote on election day. Early voters must come from that group. |
| 242 mobile-poll rows named by facility | Where those 21,602 ballots were cast. Not used to place them; they are 1.3% of the vote. |
| One Vote Anywhere row and two special-ballot rows per division | Only the division total. Nothing about location. |
| `data/va_pop_from_das.csv` | 2021 population per voting area. Not used in the recommended rule; the electors list is the more direct count. |

**Cannot be identified from any provincial source:** the home voting area of an early voter. An elector may use any advance poll, so a poll's count is not a count of its neighbourhood. And 95% of election-day votes are themselves reported for groups of voting areas, not single areas, so no rule can be finer than the station.

## The candidate rules

Each rule spreads a division's early ballots over its voting areas. Each returns the division's official totals exactly.

| Name | Party mix in each area | How many ballots each area gets |
|---|---|---|
| **M0** current rule (Amendment 12) | Same in every area: the division's early mix | In proportion to election-day two-party votes |
| **M1** party-specific | Follows the area's own lean (each party's early ballots follow that party's election-day votes) | Follows from the above |
| **M2** turnout gap | Half way between M0 and the area's own lean | In proportion to electors who did not vote on election day |
| **M3** location-informed | As R, but each geocoded advance poll's ballots go only to the areas nearest that poll | As R inside each poll's area |
| **R** recommended | The area's own lean, at strength 0.96 | 89% by electors who did not vote on election day, 11% by election-day votes |

R belongs to a two-dial family, written G(β, λ) in the scripts (`_models.py`).

- **β (lean dial).** 0 means every area gets the division's mix (M0). 1 means early voters share the whole of their area's election-day lean, after the division-wide shift.
- **λ (count dial).** 0 means ballots are spread like election-day votes. 1 means they are spread like the electors who stayed home on election day.

R's two numbers are not chosen by taste, but they are **imported from federal elections**. 0.96 and 0.89 are the averages of the 2019 and 2021 federal Alberta estimates below. In those elections the early vote leaned the other way (7 to 8 points more Conservative). The provincial data confirm the lean dial (Tests 2 and 3). **Nothing provincial pins the 89%**, and between federal ridings the count dial varies widely (spread ±0.40 to ±0.44). "0.96" also carries more decimals than the evidence: other reasonable ways of fitting give 0.86 to 0.93 (see Test 1). Seats do not change anywhere in the lean range 0.5 to 1.0.

Under R, as under every rule here, **all 87 divisions return their official NDP and UCP totals** (largest difference one billionth of a vote; checked in `05_models_headlines.py` and again in `07_residual_error.py`). Each division's observed skew is kept exactly. Only the spread inside the division changes.

## The tests

### Test 1. Federal advance polls in Alberta: a test with a known answer

Script: `02_federal_gradient.py`. Elections Canada, unlike Elections Alberta, counts advance ballots for small fixed areas. Each "advance polling district" is a known group of ordinary polls, with one advance polling station (Canada Elections Act s. 168, `sources.md` item 12). The test assumes that a federal elector who votes in advance does so at the poll assigned to their home district. Support: Elections Canada's own table labels these ballots "Electors voting at their assigned advance polling station" (`sources.md` item 7). No source read in full states the rule in so many words, so treat the premise as supported, not proven. So for all 34 Alberta federal ridings we know the true early vote of about 660 small areas.

The test hides those small-area counts, keeps only the riding's early total (which is all Alberta's provincial results give), spreads it with each rule, and compares with the truth. Party pair: Conservative against Liberal plus NDP.

| | 2021 | 2019 |
|---|---:|---:|
| Advance districts tested | 663 | 649 |
| Early two-bloc ballots | 582,592 | 573,652 |
| **Lean dial β** measured inside ridings | **0.98 ± 0.03** | **0.94 ± 0.03** |
| **Count dial λ** measured inside ridings | **0.90 ± 0.08** | **0.88 ± 0.09** |
| Error in each district's early party share: M0 | 8.1 points | 6.9 points |
| … M1 | 3.3 | 2.8 |
| … M2 | 5.1 | 4.6 |
| … best in family, G(1, 0) | 3.4 | 3.1 |
| Early ballots put in the wrong district: M0 | 13.4% | 12.9% |
| … M1 | 11.8% | 11.2% |
| … M2 | 9.5% | 9.3% |
| … best in family, G(1, 1) | 9.1% | 9.0% |
| Ridings where M1 beats M0 | 31 of 34 | 32 of 34 |

- The lean dial sits at 1, not 0. M0's error on party share is more than double that of any rule that keeps the local lean.
- When the dials are picked on 33 ridings and scored on the 34th, β = 1 and λ = 1 are picked every time, in both years.
- The two years agree, although the federal skew ran the opposite way to the 2023 provincial one. The shape holds whatever the sign.
- The count dial matters less. Moving λ from 0 to 1 cuts misplaced ballots by about a quarter. An honest caution: the turnout-gap rule makes total turnout look smoother across a riding than it really is (2.7 points of spread against a true 5.6 in 2021), while M0 makes it look rougher (6.7). The truth is between them.
- β differs between ridings (spread ±0.24; no riding of 34 below 0.5 in 2021, one in 2019).
- **Other reasonable specifications give a lower slope** (`06_robustness.py`). The 0.98 and 0.94 above weight each district by its ballots and work on the log-odds scale. Unweighted, or on the plain share scale, the slope is 0.93 (2021) and 0.86 to 0.87 (2019). With both changes it is 0.88 and 0.83. Counting noise on the election-day side pulls slopes down; the upper bound from fitting the other way round is about 1.2. So "about one for one" holds across specifications as roughly **0.85 to 1.0**, and ±0.03 understates the uncertainty.
- **Placebo: the test can tell the rules apart.** Shuffling the advance results among the districts of each riding, which is what M0 would look like, gives a slope of 0.00 ± 0.06 (largest of 200 shuffles: 0.18 in 2021, 0.17 in 2019). The test does not produce a slope near 1 by itself.

Limit: this is a federal election. It is the same electorate and the same kind of polling place, but not the same contest. Tests 2 and 3 check the provincial side directly.

### Test 2. The 2023 provincial advance polls, placed on the map

Scripts: `03_geocode_advance_polls.py`, `04_provincial_location_tests.py`. Of the 254 named advance polls, 156 were found in OpenStreetMap and 151 fell inside their division. That leaves 123 polls in 54 divisions with two or more located polls. Each voting area is given to its nearest located poll.

- **Lean dial, provincial 2023: β = 1.00 ± 0.07.** Advance polls set among NDP-leaning election-day stations lean NDP by the same amount. M0 predicts 0.
- By place: rural 0.93 ± 0.05, Edmonton 1.01 ± 0.12, Calgary 1.33 ± 0.15, smaller cities 1.31 ± 0.18.
- Error in each poll's party share: M0 6.5 points, M1 4.7, M2 4.8.
- **This estimate is less firm than ±0.07 suggests** (`06_robustness.py`). Two divisions supply 66% of what the estimate rests on: West Yellowhead (the Jasper polls, 36%) and Banff-Kananaskis (the Canmore and Banff polls, 30%). Without both, the slope is 1.13 ± 0.13. Resampling whole divisions gives a 95% range of 0.87 to 1.21. Unweighted, the slope is 0.88 ± 0.08. Only 37 of the 54 divisions show a positive relation taken alone. It still rejects 0.
- **Placebo.** If M0 were true, every poll would draw its ballots from the division's one mix. Simulating that 500 times gives a slope of 0.00 ± 0.02.
- **Coverage.** The 123 polls hold 261,493 of the 575,496 in-division advance ballots (45%), in 54 of 87 divisions. Vote Anywhere and special ballots (212,562) are not tested by any provincial check.
- "Nearest poll" is a rough guess at who uses a poll. Rough guesses blur real differences. Of the 96 polls not found, only 8 are "Returning Office" entries. Most are ordinary halls, hotels and churches missing from OpenStreetMap. 39 rows that list several sites, or a site after a dash, were placed by one name only (for example "Exshaw, Spring Bank, Edge School, Banff Centre" by its first).
- This test says little about the count dial. A poll's volume depends on its size and hours, not only on who lives nearby.

### Test 3. 2015 town-named advance polls

In 2015 rural advance polls were named for towns, and so were election-day polls. Matching names gives 36 advance polls in 12 divisions. **β = 0.99 ± 0.20.** Error in party share: M0 8.7 points, local lean 5.4. A small sample, eight years earlier, with three parties. Same answer.

### Test 4. Does the implied turnout make sense?

`05_models_headlines.py` adds each rule's early ballots to the election-day ballots at each of the 1,216 stations and divides by the names on the list.

| Rule | Stations over 100% turnout | Over 90% | Under 30% |
|---|---:|---:|---:|
| Election day alone | 2 | — | — |
| M0 | 23 | 74 | 26 |
| M1 | 22 | 72 | 24 |
| M2 | 2 | 2 | 0 |
| R | 2 | 3 | 2 |

M0 and M1 hand busy election-day stations still more early ballots, and push 20 or so past 100%, which cannot happen. Rules that use the electors list do not. (The two stations over 100% under every rule already exceed it on election day alone; their lists are tiny.) This favours the count dial being well above 0 in the provincial data too. It is a plausibility check, not a measurement.

### What the tests add up to

- **M0 against the rest: decisive.** Placebos show the tests return 0 when M0 is true. Five independent checks (federal 2019, federal 2021, provincial 2023 polls, provincial 2015 polls, and the chi-square on 2023 advance polls) all reject a single party mix per division. None supports it.
- **The lean dial: about one for one, roughly 0.85 to 1.0 across specifications** (federal 0.83 to 0.98; provincial 2023 0.88 to 1.13; provincial 2015 0.99 ± 0.20). Far from 0. The provincial evidence leans heavily on two mountain-park divisions and covers 45% of in-division advance ballots.
- **The count dial: federal only.** Federal data put it near 0.9, with wide variation between ridings. Provincial data can only say "above 0" (Test 4). This is the weaker half of R.
- **M1 against R: the data favour R mildly, and it makes almost no difference to the results.**

## Results on all 2023 ballots

Script: `05_models_headlines.py`. Formulas: `analysis/scripts/mcmc_ensemble.py` (`seat_results`), and the audit's close-seat rule (two-party margin of 4 points or less). Voting areas are assigned to districts by the audit's own rule (representative point). Checks that pass under every rule: each division's official totals are returned exactly, and the 2019 map gives the official 49–38.

Efficiency gap: the difference between the two parties' "wasted" votes as a share of all votes; positive favours the UCP. Mean-median: the middle district's UCP share minus the average district's; positive favours the UCP. Tied vote: UCP seats if every district shifted by the same amount until the province was 50–50.

| Map | Rule | UCP–NDP seats | Efficiency gap | Mean-median | UCP seats at a tied vote | Close seats |
|---|---|---:|---:|---:|---:|---:|
| 2019 map (87) | every rule | 49–38 | −2.64% | −2.22% | 41 | 12 |
| Majority (89) | M0 | 48–41 | −2.70% | −3.51% | 42 | 11 |
| | M1 | 48–41 | −2.73% | −3.73% | 42 | 11 |
| | M2 | 48–41 | −2.83% | −3.67% | 42 | 11 |
| | M3 | 48–41 | −2.78% | −3.76% | 42 | 10 |
| | **R** | **48–41** | **−2.81%** | **−3.75%** | **42** | **11** |
| Minority (89) | M0 | 55–34 | +2.55% | +0.08% | 46 | 7 |
| | M1 | 57–32 | +5.58% | +0.53% | 46 | 8 |
| | M2 | 57–32 | +5.65% | +0.26% | 46 | 8 |
| | M3 | 57–32 | +5.89% | +0.49% | 46 | 8 |
| | **R** | **57–32** | **+5.64%** | **+0.51%** | **46** | **9** |
| Panel reconstruction v3 (91) | M0 | 51–40 | −1.66% | −1.09% | 45 | 10 |
| | M1 | 50–41 | −2.70% | −0.39% | 45 | 9 |
| | M2 | 50–41 | −2.84% | −0.76% | 45 | 10 |
| | M3 | 50–41 | −2.92% | −0.27% | 45 | 9 |
| | **R** | **50–41** | **−2.82%** | **−0.49%** | **45** | **9** |
| ¶167 map (91) | M0 | 50–41 | −2.19% | −2.90% | 44 | 10 |
| | M1 | 50–41 | −2.22% | −2.31% | 44 | 10 |
| | M2 | 50–41 | −2.33% | −2.52% | 44 | 10 |
| | M3 | 50–41 | −2.39% | −2.05% | 44 | 10 |
| | **R** | **50–41** | **−2.32%** | **−2.23%** | **44** | **10** |

M3 places 261,493 ballots by poll in 54 divisions and uses R for the rest. Full table with the whole G(β, λ) grid: `outputs/headline_table.csv`.

What changes between M0 and R:

- **Minority map.** Calgary-Edgemont goes from NDP by 4 modelled votes to UCP by 384. Calgary-Glenmore goes from NDP by 24 to UCP by 66. Under M0 both seats hung on a handful of modelled votes. Those two seats are the whole change. The efficiency gap is a step function of them: +2.55% with neither, about +4.0% to +4.6% with one, +5.6% with both, so each flip is worth about 1.5 points. No smooth 3-point shift happened.
- **Panel reconstruction.** Banff-Canmore-Diamond Valley goes from UCP by 229 to NDP by 1,212.
- **Majority and ¶167 maps.** No seat changes. Calgary-Acadia stays UCP by a thin margin (10 votes under M0, 37 under R).

### The honest range

**Lead with ranges, not points: minority 56 to 57 UCP seats, majority 47 to 49, panel reconstruction 49 to 51, ¶167 map 49 to 51.** Three ways of asking how far the unknown can move the answer follow. The third is the fullest and is the source of those ranges.

1. **Every rule the evidence supports** (lean dial 0.75 to 1.25, count dial 0 to 1, plus M1). This varies the rule only:

| Map | UCP seats | Efficiency gap | Mean-median | Tied-vote seats | Close seats |
|---|---|---|---|---|---|
| Majority | 48 | −2.83% to −2.70% | −3.82% to −3.65% | 42 | 11 |
| Minority | 56 to 57 | +4.57% to +5.65% | +0.38% to +0.57% | 46 | 8 to 9 |
| Panel v3 | 50 | −2.84% to −2.68% | −0.62% to −0.25% | 45 | 9 |
| ¶167 | 50 | −2.33% to −2.19% | −2.48% to −2.01% | 44 | 10 |

2. **Letting the dials differ from division to division** as much as they differ between federal ridings (`05_models_headlines.py`, 1,000 draws, seed 20261109). Minority 57 in 92.8% of draws, majority 48 in 97.8%. **This understates the uncertainty.** It assumes R is exactly right once the dials are right. Do not quote these percentages alone.

3. **Adding the rule's own error** (`07_residual_error.py`, 1,000 draws per row, seed 20261110). Even with the right dials, R misses a small area's true advance vote. On the federal advance districts that miss is 0.17 on the log-odds scale beyond counting error, and 0.26 (log scale) on the number of ballots. Errors of that size are added at each of the 1,216 provincial stations.

| Scenario | Minority: draws at 57 / 56 / 55 or fewer | Majority: draws at 48 / 47 / 49 | Panel v3: draws at 50 |
|---|---|---|---|
| Error in party share | 76% / 23% / 2% | 57% / 24% / 17% | 57% |
| Error in share and in ballot count | 66% / 29% / 5% | 56% / 22% / 19% | 56% |
| Both, and dials vary by division | 60% / 32% / 7% | 51% / 22% / 23% | 52% |
| Half-size share error (for scale) | 98% / 2% / 0% | 76% / 22% / 2% | 76% |

Middle 90% of draws in the fullest scenario: minority 55 to 57 seats, efficiency gap +3.1% to +5.7%; majority 47 to 49 seats, −4.2% to −1.5%; panel and ¶167 49 to 51 seats.

- Under R, 3 to 4 minority-map seats sit within two standard deviations of a tie: Calgary-Glenmore (UCP by 66, ±54 to ±66), Edmonton-Enoch-Devon (UCP by 193, ±156 to ±273), Calgary-Edgemont (UCP by 384, ±211 to ±234). The majority map has 6. Its Calgary-Acadia (UCP by 37, ±100) changes hands in about a third of draws.
- **The same fragility applies to M0.** Its 55 was 4 and 24 modelled votes away from 56 and 57.
- Caution on scenario 3: the error is measured on federal advance districts (about 4,700 electors each) and applied independently to provincial stations (about 2,400 each). Smaller areas may be noisier, and neighbouring stations may err together. The half-size row shows how much the answer depends on that size.
- The independent verifier ran this design first (minority 57 in 62% to 74%, majority 48 in 53% to 57%). The figures here are our own rerun with a different seed. They agree within sampling noise.

## What cannot be known

- **Where any early voter lives.** Every rule here is a model. The tests show which model is closest on average, not what happened in a given voting area.
- **Whether the federal pattern carries over exactly.** The lean dial is confirmed provincially (Tests 2 and 3). The count dial is confirmed only loosely (Test 4).
- **Vote Anywhere and special ballots** (212,562 two-party ballots, 12.5% of the total). They have no location at all. They are spread like the other early ballots. Applying R to each ballot type on its own gives the same seats and efficiency gaps to two decimals.
- **Mobile polls.** Cast in named care homes; spread division-wide here. They are 1.3% of the vote.
- **Below the station.** Election-day votes are split equally among a station's voting areas (the audit's existing rule). R inherits that.
- **Ensemble percentiles.** The audit ranks each map against about a million computer-drawn maps scored on M0 votes. Those have not been rescored under R. **No percentile, threshold or pass/fail reading is given here, and none should be inferred.** The reference lines would move too.
- **The 96 advance polls not found** and the two lookups lost to rate limits. In all, 55% of in-division advance ballots are outside Test 2.

## Recommendation

1. **Primary allocation: R**, i.e. each area keeps its own election-day lean at strength 0.96, and ballots are spread 89% by electors who did not vote on election day and 11% by election-day votes. It is the rule the tests pick and it produces no impossible turnouts. Its two numbers are measured on federal elections in Alberta, not provincial ones. The 89% has no provincial confirmation.
2. **If the author prefers a rule with no fitted numbers, use M1.** It gives the same seats on all five maps, and efficiency gaps within 0.12 points of R. Its weakness is Test 4.
3. **Report ranges, not points:** minority 56 to 57 UCP seats, majority 47 to 49, panel and ¶167 49 to 51, with the note that the minority change is two seats decided by 66 and 384 modelled votes. Do not publish 57 or +5.64% as point findings. Keep M0's figures as the registered result until an amendment replaces it.
4. **Do not keep M0 as primary.** It is the one rule every test rejects, and it produces the audit's thinnest margins (4 and 24 modelled votes).
5. **Before any published number changes:** a signed amendment naming the rule and stating that it was chosen after its effect on the maps was known (see "Not blind"), a rebuilt all-ballots vote file with its hash, and a replay of the ensembles on that file so that percentiles can be restated.

## Files

| File | What it is |
|---|---|
| `01_measure_skew.py` | Skew by ballot type, division, region and closeness, 2023 and 2015 |
| `02_federal_gradient.py` | Test 1. Downloads federal files on first run (set `AVP_FED_DIR` to choose where; about 250 MB) |
| `03_geocode_advance_polls.py` | Looks up the named 2023 advance polls; results kept in `inputs/advance_poll_geocodes.csv` |
| `inputs/advance_poll_geocodes.csv` | The geocodes the results depend on. See "The geocode file" below |
| `04_provincial_location_tests.py` | Tests 2 and 3 |
| `05_models_headlines.py` | All rules on all five maps, the range, the Monte Carlo (seed 20261109), Test 4 |
| `06_robustness.py` | Other specifications, placebos, leverage and coverage for Tests 1 and 2 (seed 20261110); writes `outputs/robustness.json` |
| `07_residual_error.py` | Seat stability with the rule's own error included (seed 20261110); writes `outputs/residual_error.json` |
| `_models.py`, `_common.py` | The rules and the loaders |
| `outputs/skew_summary.json`, `skew_2023_by_division.csv`, `skew_2015_by_division.csv`, `polls_2015_parsed.csv` | Skew measurements |
| `outputs/federal_gradient.json`, `federal_alberta_advance_districts_2019.csv`, `…_2021.csv` | Test 1 |
| `outputs/provincial_location_tests.json`, `advance_locations_2023.csv`, `advance_catchments_2023.csv`, `advance_places_2015.csv` | Tests 2 and 3 |
| `outputs/headline_table.csv`, `headline.json`, `turnout_plausibility.json`, `va_allocations.csv` | Results; per-voting-area ballots under M0, M1, M2 and R |
| `sources.md` | Every URL fetched, when, and what it says |

Run order: 01, 02, 04, 05, 06, 07, from the repository root, e.g. `python findings/advance_vote_profile/01_measure_skew.py`. In a worktree where large files are LFS pointers, set `AVP_DATA_ROOT` to a checkout that holds the real files. Do not rerun script 03 unless you mean to rebuild the geocodes.

### The geocode file

`inputs/advance_poll_geocodes.csv` has 252 rows, 156 with a location. SHA-256: `54d3f9af576a487ab5df590ddf6e8aea4ec7d2d6e6eb946f5e1c17c2e2fb68df`.

- **How it was made.** On 2026-11-09 (Alberta time) `03_geocode_advance_polls.py` sent one OpenStreetMap Nominatim lookup per named advance poll, limited to the division's bounding box, and took the first match. Each row keeps the matched place name and the text searched, so any match can be checked by eye.
- **What went wrong.** The service rate-limited the run several times. Failed lookups were retried. Two rows were never completed and are absent: division 07 "Returning Office - Clayburn Center" and division 72 "Ethnic Association".
- **It cannot be regenerated bit for bit.** OpenStreetMap changes daily and the service's ranking is not fixed.
- **Where it lives.** It first sat in a git-ignored `cache/` folder. It now sits in `inputs/`, which is tracked. After the move, scripts 01, 02, 04 and 05 were rerun and all 15 output files that existed then were byte-identical to the earlier run.
