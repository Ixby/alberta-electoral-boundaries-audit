# Amendment 14 (draft, unsigned): early ballots go only to people who did not vote on election day

Entry: 2026-11-10 01:31 Alberta time · claude-opus-5-5 · medium (redraft). First draft: 2026-11-09 23:19 Alberta time · claude-fable-5-2 · medium.

> **Status: draft. Not in force, not signed, not filed.** Redrafted at the author's direction: early ballots belong only to electors who did not vote on election day, and federal elections are kept out of the rule. It takes effect only when the author signs it and it is filed as an update to registration 9wp5y. No item is open; the draft awaits the author's signature.
>
> **Not blind.** Before this was written, the audit had seen that placing early ballots by each area's own lean moves the all-ballots results against the commission minority's map: 55 to 57 UCP seats, and an efficiency gap of +2.55% to +5.64%. The rule's evidence uses no map. A reader should still weigh the timing. Part 6 sets out the effects.

## Why

Amendment 12 moved every vote-based step to all 2023 ballots. About 47.5% of two-party ballots were not cast on election day: advance, Vote Anywhere, special and mobile. Elections Alberta reports those only by 2019 division. So the audit has to place them among each division's polling stations.

Amendment 12's file does that with one party mix per division, in proportion to each station's election-day votes. That rule fails two plain tests (`findings/advance_vote_profile/`):

- **It counts people twice.** An early voter cannot also have voted on election day. Amendment 12 gives busy election-day stations the most early ballots. It puts more early ballots in 26 stations than those stations have people who did not vote on election day, which pushes each of them past 100% turnout.
- **It ignores where early voters lean.** In 2023, early ballots were 48.8% NDP against 42.6% on election day, a gap of 6.2 points across the province. The NDP did better off election day in 83 of 87 divisions. Inside a division, the 123 advance polls that could be located lean like the election-day stations around them, almost one for one (1.00 ± 0.07). Amendment 12 assumes they do not lean at all.

## Part 1: the rule (rule P)

Within each 2019 division, ballots not cast on election day are placed as follows.

- **Who can receive them.** Only electors who did not vote on election day: each station's names on the list (Elections Alberta's post-election list of electors) minus its election-day ballots. Each station gets early ballots in proportion to that number. A station with no such electors gets none.
- **Their lean.** Each station's early ballots lean the way its election-day ballots leaned, one for one, after a division-wide shift that returns the division's official early-ballot totals for each party exactly.
- **Stations that serve several voting areas** are split among their voting areas as in Amendment 12.
- **No federal data** enters the rule, its checks or its ranges.

The lean is set from provincial evidence only: the 2023 located advance polls (1.00 ± 0.07) and the 2015 town-named advance polls (0.99 ± 0.20). The range carried in Part 5 is 0.87 to 1.22.

**Checks that must pass** (all pass on the draft file):
1. Every division's NDP, UCP and other totals equal the official results.
2. The 2019 map returns 49 UCP and 38 NDP.
3. No station receives more early ballots than its electors who did not vote on election day.
4. No station passes 100% turnout except the two that already exceed it on election day alone: Fort Fitzgerald (2 on the list, 15 voted) and the Calgary Drop In Centre (9 on the list, 21 voted). Why those two exceed their lists cannot be confirmed from the data.

## Part 2: the vote file

Every registered step that uses 2023 votes uses the file built under Part 1:

- `data/shapefiles/derived/va_polygons_all_2023_ballots_p.gpkg`, built by `findings/advance_vote_profile/08_build_vote_file_p.py`, 22,040,576 bytes, SHA-256 `bf9b27226e457ddb4b8c2feaa77f7402d1c3d1284657c821d208f6597b8f73bd`. A rebuild gives the same bytes. Added in commit 6a735426.
- The steps are those listed in Amendment 12, Part 1. Steps that use no votes are unchanged.

## Part 3: the ensembles and thresholds

As in Amendment 12, Parts 2 and 3, with the Part 2 file here.

- Each ensemble is the same set of plans, rescored on that file. A replay counts only if every vote-independent column matches the original run row for row. A chain that fails is reported and dropped (Amendment 13). The commands and checks are in `findings/advance_vote_profile/REPLAY.md`.
- Thresholds defined as an ensemble percentile are taken from the replayed ensemble by the same rule: P1's line (the 95th percentile of the canonical ensemble's efficiency gap) and S5's line (the midpoint of the two commission maps' drain scores).
- No registered result is stated on the new file until its ensemble has been replayed. Until then, the Amendment 12 results stand as filed, each with a note that the placement rule is under amendment.
- The one ensemble whose plans are stored in the repository, the redraw-test null for R1 and R2, has been rescored on the new file: neither test flags (R1 p = 0.619, R2 p = 0.576).
- The canonical ensemble and sets A to D were replayed on the draft file on 2026-11-10; all 32 chains passed the row-for-row check. The four Forest-ReCom chains failed it and are dropped. The lines under rule P (`findings/advance_vote_profile/outputs/thresholds_p.json`, `11_thresholds_p.py`):
  - **P1:** the 95th percentile of the canonical ensemble's efficiency gap is **+2.15%** (0.0215028; the same rule on the Amendment 12 replay reproduces its +1.39%). The minority map's +5.64% is above it; 192 of 1,010,000 plans reach it.
  - **S5:** the midpoint of the two commission maps' drain scores is **0.00588** (majority 0.00403, minority 0.00773; the same call on the Amendment 12 file reproduces its 0.00194).
  - **S5 is set aside on this file** (the author's decision, 2026-11-10). Under Amendment 12 the minority's drain sat far below the majority's, and S5 flags a map below the midpoint (Amendment 5, Part 7). Under rule P the order reverses: the minority's drain (0.00773) is above the majority's (0.00403). Any direction chosen now would be chosen knowing which map it flags. So on the rule P file S5 gives no flag: both drain scores and the midpoint are reported as a sensitivity. S5's registered reading on the file in force stands as filed.

## Part 4: what is reported beside it

Every vote-based result is reported three ways:
1. on the Part 1 rule (the registered result);
2. on Amendment 12's rule, as a sensitivity;
3. on election-day ballots, as a sensitivity (Amendment 12, Part 4).

## Part 5: seats are reported with the range the rule supports

No source shows where any one early voter lives. 12.5% of all ballots (Vote Anywhere and special) have no location at all. So seat counts on all ballots are given with the range across the provincial lean range (0.87 to 1.22). That range covers the lean only. It does not cover other unknowns, so it understates the real uncertainty. A seat decided by fewer modelled votes than the change across that range is named as too close to call.

## Part 6: what this changes on results already seen

Disclosed so that no reader has to work it out. Seats are UCP–NDP on all 2023 ballots. The ensembles were replayed on the draft file on 2026-11-10 (32 of 36 chains pass; Forest-ReCom dropped; `findings/advance_vote_profile/outputs/replay_p_run.md`). Efficiency-gap percentiles against the canonical ensemble under rule P: minority 99.98, majority 18.41, panel 18.31, ¶167 25.78, 2019 map 21.05.

| Map | Amendment 12 rule | Rule P (lean 0.87 to 1.22) | Efficiency gap, Amendment 12 → rule P |
|---|---|---|---|
| 2019 (87) | 49–38 | 49–38 | −2.64% → −2.64% |
| Commission majority (89) | 48–41 | 48–41 | −2.70% → −2.83% |
| Commission minority (89) | 55–34 | 57–32 | +2.55% → +5.64% |
| Panel, reconstructed (91) | 51–40 | 50–41 | −1.66% → −2.84% |
| ¶167 map, reconstructed (91) | 50–41 | 50–41 | −2.19% → −2.33% |

- **No seat moves across the lean range** on any map.
- **Seats at a tied vote do not change:** minority 46, majority 42, panel 45, ¶167 44.
- **The minority map's change is two seats:** Calgary-Edgemont (NDP by 4 → UCP by 401, range 349 to 488) and Calgary-Glenmore (NDP by 24 → UCP by 68, range 59 to 83). Its efficiency gap moves in steps with them.
- **The panel map's change is one seat:** Banff-Canmore-Diamond Valley (UCP by 229 → NDP by 1,276, range 1,105 to 1,547). It loses the one seat that separated it from the ¶167 map on all ballots.
- **This amendment governs the scoring of the November map.** It does not reopen the registered Phase 1 results. On the commission minority's map it points the same way as Amendment 12 did, and further.
- **The scorecard counts on the reconstructed panel map** (2 of 5, 1 of 4) are not restated here. They wait for the replay in Part 3.

## What this amendment does not change

Amendment 12's use of all ballots. Every test, null, statistic, flag rule and outcome rule. The election-day results. Any result that uses no votes.

**Signed:** *(unsigned draft)*
**Date:**
