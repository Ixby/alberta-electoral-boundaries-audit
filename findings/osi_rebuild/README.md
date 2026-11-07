# Rebuilding the panel's small-area population figures: failed its own test twice (2026-11-07)

**Unregistered.** The plan, with its pass/fail rule, was committed before any fit (`preregistration/osi_da_rebuild_2026-11-07.md`, commit `d3d069da`). **The rebuild did not pass, so it is not used to total any new boundary.** This failure is kept on record.

## Result

Each map was held out in turn: fit on the other two, then predict the held-out map's published division totals. Divisions whose polygon also appears on a map in the fit are excluded from the test.

| Held out | Divisions tested | Mean error | Largest error | Prior alone (mean) | Plan's rule (mean ≤ 2.0%, largest ≤ 6.0%) |
|---|---|---|---|---|---|
| Majority | 24 | 1.36% | 6.02% (Lethbridge-East) | 2.76% | **Fail** |
| Minority | 65 | 1.58% | 7.71% (Calgary-Airdrie) | 5.20% | **Fail** |
| Panel (v3) | 33 | 1.46% | 5.45% (Edmonton-South) | 4.66% | Pass |

The fit roughly halves the prior's error, and every mean is under 2%, but on two maps a single division misses by more than the 6% limit. **The limit was fixed in advance and is not moved after the fact,** even where the miss is 6.02%.

**Where it misses.** The biggest misses fall where a line runs through the middle of a city and cuts census areas whose people are not spread evenly:
- Lethbridge-East and Lethbridge-West miss in opposite directions (−6.0% and +5.7%).
- Calgary-Airdrie and Calgary-Beddington miss in opposite directions (−7.7% and +6.1%).
- On the panel's map, Edmonton-South, Windermere and Ellerslie miss by up to 5.5%.

Splitting a census area by its land area (the plan's rule) cannot place people correctly inside a city area that straddles a line. Elections Alberta's own method is not published.

**What it means.** The published totals cannot be turned into reliable small-area figures this way, so the ¶167 map's three amended divisions still have no population figure from the source. The request to the Office of Statistics and Information is the way to get the real file.

## Changes from the plan, all made before any hold-out result was seen

- **Split areas:** an area counts as split only if a second division holds at least 1% of it. Smaller pieces are slivers where lines do not quite meet. Split areas hold 13-14% of 2021 population. This affects the reported share only, not the fit.
- **Zero municipalities:** the nine municipalities estimated at zero (dissolved or merged) give no growth rate and are dropped as constraints. That leaves 412 of 421 municipalities.
- **Prior weight:** "In proportion to each prior" was implemented as a chi-square scale, so a new neighbourhood with a small prior can still grow.
- **Guards and caching:** guards for non-finite values were added, and area weights are cached in `.weights_cache/`, which is not committed. The two failed runs before this one crashed on those values and produced no hold-out result.

The solver stopped on its tolerance (status 2), not on its iteration limit.

## Second and last attempt: splitting by electors (failed)

Plan committed before running (`preregistration/osi_da_rebuild_v2_2026-11-07.md`, commit `2f9aa3c9`). It is not blind: the design was chosen after the first attempt's misses were known. One thing changed: a census area crossing a line was split by 2026 referendum electors (through Elections Alberta's 2026 voting areas) instead of land area. City blocks would be better, but Statistics Canada's block files refused an automated download (HTTP 403).

| Held out | Divisions tested | Mean error | Largest error | Prior alone (mean) | Rule | Solver |
|---|---|---|---|---|---|---|
| Majority | 24 | 0.78% | 1.88% (Canmore-Banff) | 2.49% | Pass | converged (status 2) |
| Minority | 65 | 1.60% | **6.96% (Calgary-Airdrie)** | 5.35% | **Fail** | hit the 400-iteration limit (status 1) |
| Panel (v3) | 33 | 1.40% | 5.47% (Edmonton-South) | 4.57% | Pass | hit the 400-iteration limit (status 1) |

**The rebuild fails, and per its plan, this series stops here.** Splitting by electors fixed Lethbridge: the majority hold-out drops from a 6.02% largest miss to 1.88%. It did not fix Calgary-Airdrie and Calgary-Beddington on the minority map (−7.0% and +6.3%). These are fast-growing north Calgary areas, where electors lag population, so electors are a weak guide to where the people are.

**One caveat on the failure itself:** two of the three fits stopped at the solver's iteration limit, which was carried over unchanged from the plan. A longer run might do better. Changing that after seeing the result would be fitting the test, so it is not done here. If it is ever tried, it is a new attempt with its own plan.

The ¶167 map's amended divisions still have no figure from the source. The way forward is the data request, or Statistics Canada's 2021 block files downloaded by hand.

## Not run

No third attempt is made under these plans.

Files: `rebuild_da_2024.py` (`--split area` for the first attempt, `--split electors` for the second), `holdout.json`, `holdout_v2.json`.
