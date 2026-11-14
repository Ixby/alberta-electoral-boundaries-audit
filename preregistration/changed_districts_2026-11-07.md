# Packing and cracking in every changed or new district (written before any chain)

> Written 2026-11-07, about 9:35 AM Alberta Time (UTC−6), before any chain below has run. Unregistered and not blind: the Lethbridge, Banff and west Calgary results are known. Requested by the author on 2026-11-07. GitHub only; no OSF filing. All ballots are primary (Amendment 12). Nothing here says whether any map is a gerrymander or why any line was drawn.

## Regions

Every division that differs between the commission majority's map and the panel's map falls into one of three groups. These are the connected components of voting areas that change district, found before this plan:

| Group | Panel divisions | Majority divisions | Voting areas |
|---|---|---|---|
| South and central | 14 | 13 | 792 |
| North and south Edmonton | 15 | 14 | 740 |
| West Calgary | 4 | 4 | 221 |

The south and central group includes the restored Rocky Mountain House-Sundre. The north group includes the restored Lac Ste. Anne and the interim-report lines in south Edmonton. Each group covers exactly the same voting areas on both maps, so each map's configuration of the group can be compared with neutral redraws of it. Every other division is held fixed.

## Chains

- **Districts per redraw:** each group is redrawn twice, once with the panel's number of districts and once with the majority's. Each map is compared with redraws of its own number, because a group with an extra seat can only be compared with neutral plans that also have it. West Calgary has 4 districts on both maps, so it gets one set.
- **Variants:** city-blind and city-aware (weight 0.5).
- **Size:** 2 chains of 25,000 steps for each variant and district count.
- **Everything else:** as in `preregistration/hybrid_regions_2026-11-07.md`, with seeds from drand under the salt `changed_<group>_<k>_<variant>_<chain>`.

## Measures, for the NDP two-party votes cast in the group

- **Packing:** the share of the group's NDP votes that are surplus, beyond half the votes, in seats the NDP wins.
- **Near-miss cracking:** the share in seats the NDP loses by under 10 points.
- **Submerging:** the share in seats it loses by 10 points or more.
- **Seats:** the NDP seats in the group.
- **For comparison:** the same packing share for UCP votes. A map that packs one party's voters may also be spreading the other party's more evenly.

## Reading

Each map's configuration is placed as a percentile among neutral redraws with its own district count. A measure is flagged at or beyond the 95th or the 5th percentile. All new comparisons are then added to the ledger (`findings/test_ledger/`) and corrected for multiple testing (Benjamini-Hochberg, and Bonferroni) across the whole family. A flag that does not survive correction is reported as nominal.

**Signed:** Claude (acting as session agent), directed by Will Conner
