# Alberta Packing/Cracking Analysis — Results v0.1

**Date built:** April 22, 2026  
**Methodology:** Stephanopoulos & McGhee (2014) efficiency gap, McDonald & Best (2015) mean-median, uniform-swing seats-votes curve, vote distribution histogram.  
**Reproducibility:** Run `python3 v0_1_packing_cracking_analysis.py` against the provided 2023 results CSV.

## Headline Finding

The minority 2026 plan moves four canonical academic measures of partisan bias consistently in one direction (toward UCP), by amounts that are non-trivial but below the thresholds US courts have used to flag presumptive gerrymandering.

| Test | 2019 (current) | Minority 2026 (est.) | Shift |
|---|---|---|---|
| Efficiency gap (NDP − UCP) | −2.64% | +0.30% | **+2.94 pp toward UCP** |
| Mean-median gap (NDP) | −2.22 pp | −0.01 pp | **+2.20 pp toward UCP** |
| NDP seats at hypothetical 50/50 vote | 46 | 43 | **−3 seats for NDP** |
| Simulated 2023 outcome | NDP 38, UCP 49 (actual) | NDP 35, UCP 54 | **−3 seats for NDP** |

All four metrics shift the same direction by similar magnitudes. That consistency means the change isn't a quirk of any single test.

## What the Numbers Mean

**Efficiency gap.** Each district's "wasted" votes are: all votes for the loser, plus votes for the winner above the 50%+1 threshold. The gap is `(Wasted_NDP − Wasted_UCP) / Total_votes`. A negative value means UCP wastes more votes (NDP-favorable map). A positive value means NDP wastes more votes (UCP-favorable map). The 2019 boundaries currently sit at −2.64% — slightly NDP-favorable. The minority plan moves this to +0.30%, essentially neutral with a slight UCP lean. The shift of +2.94 pp is the structural change.

**Mean-median.** Across all 87/89 districts, the NDP's mean two-party vote share is compared to the median. Under the 2019 boundaries, NDP mean is 45.21% but the median district is 47.42% — meaning the median district leans slightly NDP-favorable, an indicator of advantageous distribution. Under the minority plan, mean and median converge to essentially the same value (45.01% vs 45.02%). The NDP loses its 2.22-point distributional advantage.

**Seats-votes asymmetry at 50/50.** Under uniform swing, if both parties received 50% of the province-wide vote, how many seats would each win? Under 2019 boundaries: NDP 46, UCP 41 (5-seat NDP advantage). Under the minority plan: NDP 43, UCP 46 (3-seat UCP advantage). An 8-seat swing in the symmetry test.

**Simulated 2023 outcome.** Applying 2023 vote shares directly: 2019 boundaries produce the actual NDP 38 / UCP 49 result. The minority plan produces a simulated NDP 35 / UCP 54 — three seats moving from NDP to UCP.

## Mechanism

The shift comes from four combined moves the minority plan makes:

1. **Hybridizing 11 Calgary urban EDs** with rural extensions (Bearspaw, Springbank, Cochrane town, Chestermere, De Winton, Tsuut'ina, Airdrie portion). Each blend dilutes NDP-strong urban votes with rural UCP votes.

2. **Packing NE Calgary** by inflating populations of McCall-Bhullar, North East, and Falconridge — NDP strongholds — using "electors not population" as the justification. Fewer NDP-voting MLAs per NDP voter.

3. **Merging Edmonton's inner core** from 6 EDs to 5 (Glenora-Riverview merger). Costs NDP one structural seat in its strongest territory.

4. **Adding three s.15(2) protected ridings** (Central Peace-Notley, Lesser Slave Lake, Rocky Mountain House-Banff Park) at populations 30K–38K. These concentrate UCP-friendly representation per voter in sparse rural territory. The Rocky Mountain House-Banff Park boundary is extended into uninhabited Banff National Park to qualify under s.15(2) criteria.

## Context: Neither Map Is an Extreme Gerrymander

- The 7% efficiency gap threshold flagged by US courts in *Whitford v. Gill* and similar cases is not exceeded by either proposal. Both sit well within bounds typical of first-past-the-post systems with strong geographic polarization.
- The current 2019 boundaries (drawn by a 2017 commission with UCP-appointed members) are themselves slightly NDP-favorable, by ~2.6 percentage points on the efficiency gap. This appears to be an artifact of Alberta's natural geography: NDP votes concentrate in Edmonton, but UCP votes spread thinly across many rural districts where they win by even bigger margins (28 districts won by UCP +25%+, vs 11 for NDP). UCP wastes more votes per seat than NDP under the current map.
- The minority plan removes that NDP geographic advantage and replaces it with a roughly neutral-leaning-UCP map. The shift is real but moderate — comparable to a typical post-redistribution adjustment in jurisdictions with similar geographic patterns.

## What This Analysis Does Not Address

- **Majority 2026 plan** is not in the comparison. Need to extract per-ED populations from Appendix B (pp. 87–266) of the report PDF and run the same tests on a third map.
- **Markov Chain Monte Carlo ensemble comparison (Test B5)** — the modern gold standard — requires proposed boundary shapefiles. ABEBC has not released them. Without B5, we can't say whether the minority plan sits in the extreme tail of computer-generated alternatives that meet the same legal criteria.
- **Compactness scores (Test C1, C2)** Polsby-Popper and Reock — also need shapefiles.
- **Spatial precision** of hybrid estimates is limited. Calgary hybrids modeled with a 70/30 urban/rural blend and a 33.5% NDP / 66.5% UCP rural baseline. Actual rural areas absorbed (Bearspaw, Springbank, Cochrane town) are wealthier UCP strongholds, not average rural Alberta — so the true shift is likely larger than +2.94 pp.

## What Would Strengthen the Case

In either direction:

- **The shapefiles, when ABEBC releases them.** Once available, run the MCMC ensemble (GerryChain in Python, or `redist` in R available through MRU lab software). 10,000+ alternative maps generated under the same legal criteria. If the minority plan sits beyond the 95th percentile of efficiency gap, that's strong evidence of intentional partisan optimization. If it sits near the 50th percentile, the +2.94 pp shift is consistent with neutral redistricting given Alberta's geography.

- **Majority 2026 populations from Appendix B.** Same tests applied symmetrically. If majority plan moves the metrics in the opposite direction (more NDP-favorable), that helps localize whether the minority's shift is a deliberate partisan choice or a side effect of necessary urban-rural rebalancing.

- **Poll-by-poll spatial join.** The 2023 Statement of Vote includes per-polling-station results for all 87 EDs. With shapefiles for proposed ridings, every poll could be assigned to its proposed ED, replacing the current approximate hybrid blend with measured vote totals.

- **2019 same-test comparison.** Run the same four tests on 2019 vote shares applied to 2019 boundaries. Compares the partisan asymmetry of the previous election against the same map. Helps separate vote-share-driven effects from boundary-driven effects.

## Bottom Line

The minority plan is not a 1990s North Carolina cartographic atrocity. It is a more subtle structural shift — moving the baseline by roughly 3 percentage points across two independent academic tests, costing NDP roughly 3 seats in a real election outcome. In a province that just elected a UCP majority of 49–38, a 3-seat shift could be the difference between majority and minority in a tighter race. The mechanism is documented, the direction is consistent across multiple tests, and the magnitude is moderate but real.

## Files

- `v0_1_packing_cracking_analysis.py` — the analysis script, fully reproducible
- `v0_1_alberta_2023_results.csv` — input data (87 EDs)
- `v0_1_minority_2026_populations.csv` — for cross-reference

## Versioning

v0.1 — first run. Limits documented above. Treat as a draft pending shapefiles and majority population extraction.
