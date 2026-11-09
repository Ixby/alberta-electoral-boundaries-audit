# Signs of local targeting in the panel's changes (2026-11-07)

**Unregistered, provisional, not blind.** Plan committed before computing (`preregistration/local_targeting_2026-11-07.md`, commit `399a489a`). Compared with the commission majority's map; all ballots; the panel's map is the v3 reconstruction. Nothing here shows why a line was drawn or says whether any map is a gerrymander.

## A. Were competitive seats more likely to be changed? No.

| Majority divisions | Changed by the panel | Rate | Fisher p (two-sided) |
|---|---|---|---|
| Competitive (within 10 points) | 4 of 18 | 22% | 0.27 against safe seats (27 of 71, 38%) |
| NDP-won | 8 of 41 | 20% | 0.007 against UCP-won (23 of 48, 48%) |

The panel changed competitive seats and NDP-held seats *less* often than the rest. That is mostly the confound named in the plan: the two restorations cascade through rural central Alberta, which is safe UCP. The NDP-held result is one of the lower p-values in the ledger (5th of 143, `../test_ledger/`), but it does not survive the multiple-testing correction, and it points away from blanket targeting of NDP seats.

## B. Which way did the changes move close margins? Mostly toward the UCP, in a few seats.

Of the 6 changed divisions within 10 points on either map, 5 moved toward the UCP and 1 toward the NDP (sign test p = 0.22, not significant):

| Panel division (majority source) | Margin NDP − UCP: majority → panel |
|---|---|
| Lethbridge-Little Bow (Lethbridge-East) | −1.6 → −26.3 |
| Banff-Canmore-Diamond Valley (Canmore-Banff) | +10.4 → −1.3 |
| Lethbridge (Lethbridge-West) | +11.2 → +5.1 |
| Calgary-North West-Bearspaw (Calgary-North West) | −0.6 → −1.6 |
| Calgary-Bow-Springbank (Calgary-Bow) | −3.4 → −3.7 |
| Edmonton-Nisku (Edmonton-Beaumont) | +1.5 → +21.1 (toward the NDP; interim-report lines that ¶167 shares) |

## C. Where did the moved voters' NDP votes go?

157,699 NDP votes are in voting areas that changed division.

| NDP votes moved, from (majority) → to (panel) | Seats the NDP loses by 10+ | Loses by under 10 | NDP wins |
|---|---|---|---|
| From seats lost by 10+ | 87,684 | 2,808 | 344 |
| From seats lost by under 10 | 5,400 | 23,387 | 5,767 |
| From seats the NDP won | 8,799 | 6,854 | 16,657 |

**Of the moved NDP votes, 9.0% (14,199) went from a seat the NDP won or nearly won into one it loses by 10 or more. Only 2.0% (3,152) went the other way.** Split by division pair (same votes and rule as `local_targeting.py`), most of the 9.0% is the Lethbridge change in section B: 10,033 votes from Lethbridge-East and Lethbridge-West into the three Lethbridge hybrids. Most of the rest, 3,706, is Edmonton-Beaumont voters moved into Leduc-Beaumont. The Banff change moves its NDP votes into a near loss, not a lopsided one; only 460 go from Canmore-Banff into Rocky Mountain House-Sundre.

## Reading

The panel's changes do not fall on competitive or NDP-held seats more often than on other seats, and province-wide the map is ordinary (see `../packing_cracking/`, `../changed_districts/`). The effect is local:
- **Where it is:** a small number of changes, centred on Lethbridge and Banff.
- **Which way it runs:** consistently against the NDP, moving NDP voters from competitive seats into lopsided ones about four times as often as the reverse.
- **How big it is:** about one seat on 2023's votes.

No test here reaches significance after correction, and none can show intent. The changed-district redraws (`../changed_districts/`) test this local pattern against neutral redraws of the same areas. The panel's layouts sit inside the band in every region and on every measure. The commission majority's south-and-central layout is the outlier there, though the redraws cannot draw its Canmore-Banff.

Files: `local_targeting.py`, `local_targeting.json`.
