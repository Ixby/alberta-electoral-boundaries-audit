# Test of a published seat-count claim about the panel's map (written before any computation)

> Written 2026-11-04, about 4:50 PM MST, before any seat count or vote total of the panel's map has been computed. The registered Amendment 10 run is in progress; this test runs only after its result is committed, and only on its assembled map. It is not part of the registered November scoring and changes nothing in it.

## The claim

Reported to the author as posted by the Premier on Facebook on 2026-11-04, after remarks in the Legislature:

> "Using the last election's popular vote results, the new boundaries would give the NDP +3 more seats and the UCP +1."

The 2023 general election on the 87-district map elected 49 UCP and 38 NDP members. Read as changes from that result, the claim is that 2023's votes on the panel's 91 districts elect **50 UCP and 41 NDP**. The claim's own method (vote source, how advance votes were placed) is not published.

## What is computed

1. **Map.** The panel's map as assembled by the registered Amendment 10 run (`findings/a10_*`), with the 56 unchanged districts and Calgary-Acadia at the commission's published geometry and every voting area (VA) assigned to one district. If the registered run fails, this test is not run, and that is reported.
2. **Votes.** 2023 general election results per VA, on two substrates:
   - **A (primary): all ballots.** Election-day VA results plus the advance, mobile and special ballots Elections Alberta reports only by district, spread to that district's VAs by their election-day shares (`analysis/scripts/advance_vote_splat.py`, `va_polygons_with_full_2023_votes.gpkg`). This is the closest the data allow to "the last election's popular vote results".
   - **B: election-day ballots only** (`va_polygons_with_2023_votes.gpkg`), the audit's standing substrate.
3. **Seats.** Each district goes to the party with the most votes in it, all parties counted. Reported: seats by party on each substrate, every district's winner and margin, and the districts won by under 2 points.
4. **Check of the method.** The same code on the 2019 map (the 87 districts the 2023 election used) must return 49 UCP and 38 NDP on substrate A; if it does not, the gap is reported first and the test result is read with it.
5. **What the reconstruction cannot decide.** For each district, the votes in VAs cut by one of its changed lines (Amendment 10's cut list) are compared with its margin. A district whose margin is smaller than the votes in its cut VAs, or whose winner changes when any one of its cut VAs with at least 10% of its area on the other side is moved across, is marked **undecided by the reconstruction**. The seat count is reported as a range over those districts.

## How the result is read

- **Consistent with the claim:** both substrates give 50 UCP and 41 NDP, and the range from step 5 contains no other count; or substrate A does and the only differences are districts marked undecided.
- **Not consistent with the claim:** both substrates give another count, outside the range from step 5.
- **Otherwise:** reported as within the reconstruction's uncertainty, with the districts that decide it named.

The test checks one arithmetic statement. A change in seat counts from the old map, with four seats added, is not a measure of partisan fairness, and by the audit's standing rule no conclusion is drawn here about whether any map is a gerrymander. The audit's registered measures of the map are the ones in Amendments 7 to 10.

**Signed:** Claude (acting as session agent), directed by Will Conner
