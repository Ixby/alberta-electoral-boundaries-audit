# Packing and cracking, measured (2026-11-07)

**Unregistered, provisional, not blind.** Plan committed before computing (`preregistration/packing_cracking_2026-11-07.md`, commit `c2f1a710`). Two-party votes (UCP and NDP) on two ballot sets. The panel's map is the v3 reconstruction. These measures describe where voters end up. They do not show why a line was drawn, and nothing here says whether any map is a gerrymander.

## Part 1: wasted votes, split in two (share of all two-party votes)

Surplus is the winner's votes beyond half (packing-type). Losses are the loser's votes, split by margin (cracking-type). All ballots:

| Map | NDP surplus | NDP losses within 10 pts | NDP losses by 10+ | UCP surplus | UCP losses within 10 | UCP losses by 10+ | Gap (NDP waste minus UCP) |
|---|---|---|---|---|---|---|---|
| 2019 (87) | 4.24 | 5.31 | 14.13 | 8.68 | 5.82 | 11.82 | −2.64 |
| Majority (89) | 4.20 | 4.32 | 15.13 | 8.64 | 6.22 | 11.49 | −2.70 |
| Minority (89) | 4.05 | 5.48 | **16.74** | 8.49 | **3.32** | 11.91 | +2.55 |
| Panel (91) | 4.15 | 4.23 | 15.78 | 8.59 | 6.46 | 10.77 | −1.66 |
| ¶167 (91) | 4.23 | 4.32 | 15.36 | 8.67 | 5.81 | 11.62 | −2.19 |

Election-day figures are in `real_maps.json`. Every gap shifts toward the UCP, and the order of the gaps changes: ¶167 −0.24, majority +0.10, panel +1.45, 2019 +2.41, minority +4.03. The minority map still has the most NDP votes in lopsided losses and the fewest UCP near-losses, and the panel's map still sits between the commission maps. But the panel-versus-¶167 difference in NDP lopsided losses reverses: the panel's map has 0.16 points fewer (15.81 against 15.97).

**Reading.** On every map the NDP's largest waste is votes in seats it loses badly. Its surplus is small, so the familiar "NDP packed into Edmonton" pattern is modest by this measure. The minority commission map has the most NDP votes in lopsided losses and the fewest UCP near-losses. The panel's map sits between the commission maps. Compared with ¶167 it has 0.4 points more NDP votes in lopsided losses and 0.8 fewer UCP votes in lopsided losses. Those differences are small on a provincial scale. Part 2 will show whether they are unusual against neutral maps.

## Part 3: where the named areas' NDP votes land

Share of the area's NDP two-party votes, all ballots. Margins are NDP minus UCP.

**Lethbridge (city)**

| Map | In seats the NDP wins | In seats it loses by under 10 | In seats it loses by 10+ | Seats holding the city (margin) |
|---|---|---|---|---|
| 2019 | 53.8% | 46.2% | 0% | West +11.8, East −3.0 |
| Majority | 50.2% | 49.8% | 0% | West +11.2, East −1.6 |
| ¶167 | 50.2% | 49.8% | 0% | same as majority |
| **Panel** | **55.3%** | **0%** | **44.7%** | Lethbridge +5.1, Little Bow −26.3, Cardston −22.8, Taber-Warner −51.5 |
| Minority (commission) | 0% | 0% | **100%** | four hybrids, −20.1 to −28.6 |

On the majority map, the city's NDP voters are split between a seat the NDP holds and one it lost narrowly. On the panel's map:
- About 55% are combined into one seat the NDP wins by less (+5.1 against +11.2).
- About 45% are placed in three seats the UCP wins by 23 to 52 points.
- The narrowly lost seat is gone.

The NDP's seat count in the city is the same on these votes (one), but it loses a competitive second seat. This is the pattern usually called cracking. The commission minority's map does it to the whole city.

On election-day ballots, the panel's Lethbridge seat is narrowly UCP (−4.5). Under the majority map, the same voters sit 49.9% in a seat the NDP wins.

**Banff, Okotoks and the south (the panel's southern group, all ballots).**
- **Panel:** 22.9% of the area's NDP votes are in seats the NDP wins, 15.7% in near-losses and 61.4% in seats lost by 10 or more.
- **¶167:** 33.4%, 20.6% and 46.0%.
- **The difference is mostly Banff.** Canmore-Banff is NDP by 11.5 on the ¶167 map. The panel's Banff-Canmore-Diamond Valley is UCP by 1.3, which is undecided within the reconstruction.

**Northwest Calgary and Cochrane (the west Calgary group).** The two maps are about the same: 56.5% and 53.9% in near-losses, with nothing in seats the NDP wins on either. The Springbank and Bearspaw changes do not move this measure much.

## Part 2: seat by seat against neutral maps

Set D's four 91-seat chains were replayed from their seeds on both ballot sets, keeping every 10th plan's sorted seat shares (101,000 plans per ballot set). **Replay check passed:** in all eight chains every vote-independent column equals the original run row for row, and on all ballots the efficiency gap also equals the earlier all-ballots run. All ballots are the primary figures (Amendment 12); election-day figures are in `sorted_vs_neutral_election_day.json`.

| All ballots | Panel | ¶167 | Neutral 5th / median / 95th |
|---|---|---|---|
| NDP seats | 40 (p57) | 41 (p78) | 37 / 40 / 42 |
| Seats at 40-50% NDP (cracking count) | 18 (p36) | 18 (p36) | 15 / 19 / 22 |
| Seats under 30% NDP | 21 (p77) | 22 (p92) | 17 / 20 / 22 |
| Sorted positions above the neutral 95th | 2 (Calgary-Nose Creek, Edmonton-Strathcona) | 10 | |
| Sorted positions below the neutral 5th | 2 (Drumheller-Stettler, Morinville-Sturgeon) | 11 | |
| Lethbridge NDP votes in seats lost by 10+ | 44.7% (p72) | 0% (**p4.7**; a tie with the neutral 5th percentile, see below) | 0% / 21% / 62% |

**By the plan's rules:**
- **Cracking:** neither map. Neither has more seats at 40-50% NDP than 95% of neutral plans.
- **Packing:** one NDP seat on each map is more lopsided than 95% of neutral plans at its position, Edmonton-Strathcona (80.9% against 80.6%). Both maps share Edmonton's lines.
- **Shape of the curve:** the panel's sorted seats lie inside the neutral band at 87 of 91 positions. The ¶167 map leaves the band at 21 positions. It has more NDP-competitive Calgary and Lethbridge seats than neutral maps (above the band from rank 47 to 62) and more lopsided UCP rural seats (below the band at ranks 1 to 27).
- **¶167's Lethbridge p4.7:** 0% is the lowest value possible and equals the neutral 5th percentile. The percentile counts the plans tied at 0 as half, so the p4.7 comes from ties, not from a value below the band.

**Reading.** Against province-wide neutral maps, the panel's seat curve is ordinary. The ¶167 map is the outlier, in the NDP's favour on seats and with rural UCP voters packed. This agrees with the regional redraw (`../six_signals/`): what the neutral maps call unusual is keeping Lethbridge whole, not splitting it. These neutral maps also ignore municipal boundaries, and the municipality-aware regional runs (`../hybrid_regions/`) test that.

Code: `real_maps.py` (parts 1 and 3); `alberta_audit/analysis/scripts/sorted_shares_replay.py` (part 2).
