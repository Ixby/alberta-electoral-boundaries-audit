# Seat-count claim test: result

> Test plan: `preregistration/seat_claim_test_2026-11-04.md`, committed at `da21f14b` before any computation. Run 2026-11-04 after the registered Amendment 10 run passed (`fd82cdd1`), on its assembled map. Script: `findings/seat_claim_test.py`; full output: `findings/seat_claim_test_result.json`. Provisional, like every reading of the panel's map before its official shapefile.

**The claim** (reported as posted by the Premier, 2026-11-04): on 2023's votes the panel's 91 districts give the NDP 3 more seats and the UCP 1 more than the 2023 result of 49 UCP and 38 NDP, that is **50 UCP, 41 NDP**.

## Result

**Within the reconstruction's uncertainty, one seat from the claim.** On the substrate that reproduces 2023 exactly, the panel's map gives **51 UCP and 40 NDP** (UCP +2, NDP +2). The claim's 50/41 lies inside the range the reconstruction cannot rule out (UCP 49 to 53), and the deciding seat is a near-tie: the unchanged Calgary-Acadia, won by the UCP by 12 votes of about 24,360 (0.05 points) on this substrate.

| Substrate | Check: 2019 map (must be 49 / 38) | Panel's map | Range over undecided districts |
|---|---|---|---|
| A. all ballots, advance ballots spread by election-day share (planned primary) | **52 / 35, fails** | 52 UCP / 39 NDP | UCP 51 to 57 |
| B. election-day ballots only | 57 / 30, fails | 58 UCP / 33 NDP | UCP 55 to 61 |
| C. A rescaled to the official district totals (added; see below) | 49 / 38, passes | **51 UCP / 40 NDP** | UCP 49 to 53 |

## The method check failed on the planned substrate, and what was done

Step 4 of the plan requires the method to reproduce 2023 on the 2019 map. Substrate A does not: it holds 854,502 UCP and 689,637 NDP votes against the official 928,900 and 777,404, about 8% and 11% short, so it under-counts the NDP more and turns three near-tied Calgary seats UCP (Acadia, Edgemont and Glenmore, each decided by about a point or less in 2023). Substrate B, election day only, is further off (57 / 30), because advance ballots, nearly half of 2023's, leaned differently.

Substrate C is not in the plan. It rescales A party by party within each 2019 district so that every district's totals equal the official 2023 results, which makes the 2019 check exact by construction while keeping A's spread of votes within each district. It is reported beside the planned substrates, not instead of them, and the result above is read on C because the plan says a failed check must be reported and the result read with it; A's failure is the reason a fuller substrate was needed.

## What decides it

- **Undecided by the reconstruction** (on C; the margin is smaller than the votes in voting areas cut by a changed line): Banff-Canmore-Diamond Valley (UCP by 0.87 pts), Calgary-Bow-Springbank (UCP by 3.8), Lethbridge (NDP by 4.9), Edmonton-Windermere (NDP by 13.5). Moving any single cut voting area does not change a winner.
- **Closer than 2 points** (on C): Calgary-Acadia (UCP 0.05), Calgary-North (UCP 0.74), Banff-Canmore-Diamond Valley (UCP 0.87), Calgary-Glenmore-Tsuut'ina (NDP 0.96), Calgary-Edgemont (NDP 1.22), Calgary-North West-Bearspaw (UCP 1.58), Calgary-Confluence (NDP 1.67).
- **Beyond the reconstruction:** advance, mobile and special ballots are reported only by district, so within a district they are placed by election-day shares. In a seat decided by 12 votes, that placement, not the boundaries, decides the winner. The claim's own method is not published; a different but reasonable treatment of advance ballots could give 50 / 41.

## What this does and does not show

It checks one arithmetic statement. The claim's count is one seat from ours and inside the reconstruction's uncertainty. A change in seat counts from the old map, with four seats added, is not a measure of partisan fairness, and no conclusion is drawn here about whether the map is a gerrymander. The audit's registered measures of the panel's map are Step C's (Amendments 7 to 10).
