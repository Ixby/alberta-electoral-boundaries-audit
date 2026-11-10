# Amendment 14 (draft, unsigned) — Early ballots are placed by where the evidence says early voters live

Entry: 2026-11-10 00:05 Alberta time · claude-fable-5-2 · medium

> **Status: draft. Not in force, not signed, not filed.** Written 2026-11-10 at the author's direction ("Draft the amendment"). It takes effect only when the author signs it and it is filed as an update to registration 9wp5y. Two items marked **[to fill before signing]** do not exist yet.
>
> **Not blind.** Before this was written, the audit had seen that the new rule moves the all-ballots results against the commission minority's map: 55 to 56–57 UCP seats, and an efficiency gap of +2.55% to about +4.6% to +5.6%. The rule was studied on 2026-11-09, after an audit of the vote file showed that sensitivity. The evidence for the rule uses no map. A reader should still weigh the timing. Part 6 sets out the effects.

**Why.** Amendment 12 moved every vote-based step to all 2023 ballots. About 47.5% of two-party ballots were not cast on election day (advance, Vote Anywhere, special and mobile). Elections Alberta reports them only by 2019 division, so the audit has to place them among each division's voting areas. Amendment 12's file does that with one party mix per division: every voting area gets the division's early-ballot mix, in proportion to its election-day votes.

That rule was an assumption, and it was not tested. It has now been tested (`findings/advance_vote_profile/`, commit `dbd1257f`; independently verified, with corrections applied):
- **The skew is real.** In 2023, ballots not cast on election day were 48.8% NDP against 42.6% on election day: 6.2 points, in the NDP's direction in 83 of 87 divisions.
- **Early voters lean like their neighbours.** Where the answer can be checked, early voters share their election-day neighbours' lean almost one for one.
  - Federal advance polls in Alberta, which are counted for small fixed areas: 0.98 ± 0.03 in 2021 and 0.94 ± 0.03 in 2019. Other reasonable fits give 0.83 to 0.93.
  - 123 located 2023 provincial advance polls: 1.00 ± 0.07. Two divisions carry most of that result.
  - A placebo in which Amendment 12's rule is true returns 0.00.
- **Amendment 12's rule gives impossible turnouts.** It pushes about 20 polling stations past 100% turnout. Rules that use the list of electors push none.

So Amendment 12's placement rule is rejected by the evidence. This amendment replaces it. It does not change Amendment 12's decision to use all ballots.

**Part 1: the rule.** Within each 2019 division, ballots not cast on election day are placed as follows. This is rule R, `general(β = 0.96, λ = 0.89)` in `findings/advance_vote_profile/_models.py`.
- **Lean.** Each polling station's area keeps its own election-day lean, at strength 0.96, after a division-wide shift that returns the division's official early-ballot totals for each party exactly.
- **Count.** Each area's share of the division's early ballots is 89% in proportion to its electors who did not vote on election day (names on the list minus election-day ballots), and 11% in proportion to its election-day votes.
- **Stations serving several voting areas** are split among their voting areas as in Amendment 12.
- **The check that must pass:** every division's NDP, UCP and other totals equal the official results, and the 2019 map returns 49 UCP and 38 NDP.

The two numbers come from federal elections in Alberta (the mean of the 2019 and 2021 estimates). The provincial data confirm the lean. Nothing provincial pins the 89%.

**Part 2: the vote file.** Every registered step that uses 2023 votes uses the file built under Part 1.
- File: `data/shapefiles/derived/va_polygons_all_2023_ballots_r.gpkg` **[to fill before signing: build script, commit, SHA-256]**.
- The steps are those listed in Amendment 12, Part 1. Steps that use no votes are unchanged.

**Part 3: the ensembles and thresholds.** As in Amendment 12, Parts 2 and 3, with the Part 2 file here.
- Each ensemble is the same set of plans, rescored on that file. A replay counts only if every vote-independent column matches the original run row for row. A chain that fails is reported and dropped (Amendment 13).
- Thresholds defined as an ensemble percentile are taken from the replayed ensemble by the same rule: P1's line (the 95th percentile of the canonical ensemble's efficiency gap) and S5's line (the midpoint of the two commission maps' drain scores). **[to fill before signing or at first scoring: both values]**
- No registered result is stated on the new file until its ensemble has been replayed. Until then, the Amendment 12 results stand as filed, and each carries a note that the placement rule is under amendment.

**Part 4: what is reported beside it.** Every vote-based result is reported three ways:
1. on the Part 1 rule (the registered result);
2. on Amendment 12's rule (one mix per division), as a sensitivity;
3. on election-day ballots, as a sensitivity (Amendment 12, Part 4).

**Part 5: seats are reported as ranges.** No source shows where any one early voter lives, and 12.5% of all ballots (Vote Anywhere and special) have no location at all. So seat counts on all ballots are given as the Part 1 value with the range the rule's own error supports, computed by `findings/advance_vote_profile/07_residual_error.py` (fixed seed) on the map being scored. A seat decided by fewer modelled votes than that error is named as too close to call.

**Part 6: what this changes on results already seen.** Disclosed so that no reader has to work it out. Seats are UCP–NDP on all 2023 ballots. Percentiles are not given: the ensembles have not been replayed on the new file.

| Map | Amendment 12 rule | Part 1 rule | Range | Efficiency gap, Amendment 12 → Part 1 |
|---|---|---|---|---|
| 2019 (87) | 49–38 | 49–38 | official result | −2.64% → −2.64% |
| Commission majority (89) | 48–41 | 48–41 | 47 to 49 | −2.70% → −2.81% |
| Commission minority (89) | 55–34 | 57–32 | 56 to 57 | +2.55% → +5.64% |
| Panel, reconstructed (91) | 51–40 | 50–41 | 49 to 51 | −1.66% → −2.82% |
| ¶167 map, reconstructed (91) | 50–41 | 50–41 | 49 to 51 | −2.19% → −2.32% |

- **Seats at a tied vote do not change** on any map: minority 46, majority 42, panel 45, ¶167 44.
- **The minority map's change is two seats:** Calgary-Glenmore (66 modelled votes) and Calgary-Edgemont (384). Its efficiency gap moves in steps with them: +2.6% with neither, about +4.0% to +4.6% with one, +5.6% with both.
- **The panel map** loses the one seat that separated it from the ¶167 map on all ballots.
- **This amendment governs the scoring of the November map.** It does not reopen the registered Phase 1 results. On the commission minority's map it points the same way as Amendment 12 did, and further.
- **The scorecard counts on the reconstructed panel map** (2 of 5, 1 of 4) are not restated here. They wait for the replay in Part 3.

**What this amendment does not change.** Amendment 12's use of all ballots. Every test, null, statistic, flag rule and outcome rule. The election-day results. Any result that uses no votes.

**Signed:** *(unsigned draft)*
**Date:**
