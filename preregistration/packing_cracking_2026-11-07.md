# Measuring packing and cracking (written before any computation)

> Written 2026-11-07, about 5:20 AM Alberta Time (UTC−6), before any figure below has been computed. Unregistered and not blind: the author knows each map's efficiency gap, its ranks and the ¶167 comparison. Requested by the author on 2026-11-07. GitHub only; no OSF filing. Nothing here is a finding on whether any map is a gerrymander. Packing and cracking describe where voters end up; they do not show why lines were drawn.

## Maps and votes

- **Maps:** 2019 enacted, commission majority and minority (official), panel (v3) and ¶167. Voting areas are placed by representative point.
- **Votes:** two-party UCP and NDP only. Two ballot sets: election day (registered substrate) and all ballots (`va_polygons_all_2023_ballots_primary.gpkg`, which matches the official results).

## 1. Wasted votes, split in two

In each seat, the winner needs half the two-party vote:
- **Surplus (packing-type):** the winner's votes beyond that half.
- **Loss (cracking-type):** all of the loser's votes.

Losses are further split by margin: under 10 points, and 10 points or more. Reported for each party and map, as shares of the two-party vote. The efficiency gap is the difference in total waste, so the split shows which kind of waste drives it.

## 2. Seat by seat against neutral maps

- **The replay:** set D's four 91-seat chains (idx 251-254, 252,500 steps each) are replayed with their original seeds, on both ballot sets.
- **What is recorded:** every 10th step, each plan's seats sorted by NDP two-party share. The wrapper `analysis/scripts/sorted_shares_replay.py`, a new file in the `alberta_audit` clone, adds the recording and changes nothing else.
- **Replay check:** every vote-independent column must equal the original run's. If any differs, the replay is not used.
- **The comparison:** for each position from weakest to strongest NDP seat, the 5th to 95th percentile range of neutral plans, with the panel's and the ¶167 map's seat at that position marked.
- **The labels:**
  - **Packing:** NDP seats at the top that are more lopsided than 95% of neutral plans at that position.
  - **Cracking:** more seats between 40% and 50% NDP than 95% of neutral plans have.
  - The same is reported for the UCP side (seats under 30% NDP).
- **Status:** the 89-seat commission maps have no matching neutral set here, so they get part 1 and part 3 only.

## 3. Communities the critics name

For each area, the NDP's two-party votes are split three ways: in seats the NDP wins, in seats it loses by under 10 points, and in seats it loses by more. The number of seats holding at least 2% of the area's people is also reported.

- **Lethbridge (city):** on all five maps, and in the neutral replay (recorded with the sorted shares).
- **Northwest Calgary and Cochrane:** the voting areas in the four districts of the panel's west Calgary group (`findings/iap_para167/`), on the panel's and ¶167 maps.
- **Banff, Okotoks and the south:** the voting areas of the panel's southern group, on the same two maps.

Groups 2 and 3 come from the ¶167 comparison, so for those only the panel and ¶167 maps share an area definition.

## How the result is read

- A map is named as packing or cracking at a position only by the 95% rule above.
- Being outside the neutral range is a description of the map, not evidence of intent.
- Undecided seats from the reconstruction are listed beside any position where the panel's map is outside the range.
- No conclusion is drawn on whether any map is a gerrymander.

**Signed:** Claude (acting as session agent), directed by Will Conner
