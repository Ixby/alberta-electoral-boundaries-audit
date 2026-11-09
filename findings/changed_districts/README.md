# Packing and cracking in every changed district

> **Unregistered and not blind.** The plan, `preregistration/changed_districts_2026-11-07.md` (`3c501006`), was written before any chain ran, but the Lethbridge, Banff and west Calgary results were already known. All ballots are primary (Amendment 12). Nothing here says whether any map is a gerrymander or why any line was drawn. Each comparison places a map's layout of a region among nonpartisan alternative redraws of the same region.

## What ran

Each division that differs between the commission majority's map and the panel's map is in one of three regions (`groups.json`). Each region covers the same voting areas on both maps. Every other division is held fixed.
- Each region was redrawn at each map's own district count.
- Each was redrawn two ways: city-blind, and city-aware (weight 0.5).
- Each redraw is 2 chains of 25,000 steps after 1,000 burn-in, with seeds from drand.
- That makes 20 chains (`chains/`) and 50,000 plans per comparison.

Runs: 2026-11-07, 9:41 to 10:22 AM Alberta Time (UTC−6). Three detached workers; the `worker*.log` files are kept. Summary: `summary.json` (`changed_redraw.py summarize`, rerun 2026-11-08).

## Results

Percentile of each map's layout among the redraws with its own district count. All ballots. A flag is at or beyond the 95th or the 5th percentile.

| Region | Map (divisions) | Variant | NDP seats | Packing | Near-miss | Lopsided losses |
|---|---|---|---|---|---|---|
| South and central | majority (13) | blind | 2, p94.3 | 2.16%, **p100.0** | 13.2%, p66.4 | 64.8%, **p4.5** |
| | | city-aware | 2, p73.2 | 2.16%, **p100.0** | p77.2 | **p4.7** |
| | panel (14) | blind | 1, p48.4 | 0.71%, p65.4 | 10.1%, p47.9 | 75.2%, p33.3 |
| | | city-aware | 1, p19.2 | p18.4 | p72.4 | p51.4 |
| North and south Edmonton | majority (14) | blind | 6, p73.4 | 11.2%, p58.5 | 0.0%, p34.5 | 44.9%, p53.5 |
| | | city-aware | p87.3 | p32.3 | p44.6 | p34.7 |
| | panel (15) | blind | 6, p58.1 | 11.7%, p94.4 | 0.0%, p34.4 | 47.9%, p90.5 |
| | | city-aware | p64.1 | p34.5 | p44.0 | p37.0 |
| West Calgary | majority (4) | blind / city-aware | 0, p49.5 / p49.3 | 0 | 53.9%, p35.8 / p33.8 | 46.1%, p64.5 / p67.1 |
| | panel (4) | blind / city-aware | 0, p49.5 / p49.3 | 0 | 56.5%, p58.5 / p62.3 | 43.5%, p41.7 / p38.3 |

The measures are shares of the region's NDP two-party votes:
- **packing:** the surplus beyond half in seats the NDP wins;
- **near-miss:** votes in seats it loses by under 10 points;
- **lopsided losses:** votes in seats it loses by 10 points or more.

**The panel's layouts.** Every one of them sits inside the band in every region and on every measure. The closest to the edge is north Edmonton city-blind: packing at p94.4 and lopsided losses at p90.5.

**The commission majority's layout of the south and central region is the outlier.**
- Its NDP packing (2.16%) is above all 100,000 redraws in both variants; the largest redraw value is 1.53%.
- Its share of NDP votes in lopsided losses is low: p4.5 city-blind and p4.7 city-aware.

The blind and city-aware rows test the same real-map value against two sets of redraws. They are one finding measured two ways, not two findings.

**A lead, not a cause.** On all ballots, the majority's layout gives the NDP two seats in the region, each won by a wide margin:
- Lethbridge-West, 55.6% NDP;
- Canmore-Banff, 55.2% NDP.

Lethbridge-East is then a near miss at 49.2%. The panel's layout has one NDP seat (Lethbridge, 52.5%), and Banff-Canmore-Diamond Valley becomes a near miss at 49.3%. So the panel's changes lower NDP packing in this region; they do not raise it. Two wide NDP wins in one region is a configuration the neutral redraws almost never produce. Keeping the Bow Valley towns and the west side of Lethbridge as their own divisions would produce it. That reading has not been tested here.

## Multiple testing

The 48 new comparisons (4 measures × 12 map-variant cells) are in the family ledger (`../test_ledger/`). The family is now 139 comparisons.
- **The floor on p.** A percentile of 100 is not p = 0. The ledger floors p at 2 / (n_eff + 1), using the registered n_eff estimator (`size_matched_results.ess`, summed over the two chains). For the majority's south-and-central packing, n_eff is 2,153 (city-blind) and 1,211 (city-aware), so p ≥ 0.00093 and 0.0016.
- **With that floor, nothing survives correction.** Bonferroni needs p ≤ 0.00036, and Benjamini-Hochberg needs the same for the smallest p.
- **Treated as independent:** if the 50,000 plans were independent draws, p would be about 0.00004, and both rows would pass Bonferroni. They are not independent, so the registered floor is the one used.

**UCP packing is reported, not ranked.**
- **Why:** within a fixed region, the sum over all seats of (NDP votes − half the votes) is a constant. So the UCP surplus in UCP-won seats equals the NDP surplus in NDP-won seats minus that constant, and the two measures rank identically.
- **What that changes:** the plan's reason for the measure ("a map that packs one party's voters may also be spreading the other party's more evenly") cannot hold for packing measured this way.
- **The earlier summary:** it showed different UCP percentiles in west Calgary (p9.4 against p49.5). That came from float rounding in exact ties. The percentile now treats values within 1e-9 as ties.

## Limits

- **Poor mixing:** the north Edmonton city-aware chains mix poorly, with n_eff 24 to 73 on seats and packing. On packing their median equals their 95th percentile (11.7%), so those rows are weak evidence either way.
- **The reconstruction:** the panel's map is the audit's reconstruction, not the official file.
- **Shared runs:** these regions overlap the Lethbridge and hybrid-region runs (`../hybrid_regions/`, `../six_signals/`). The same votes enter several comparisons.
