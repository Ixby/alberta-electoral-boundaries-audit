# Second attempt at the small-area rebuild: splitting by electors (written before any fitting)

> Written 2026-11-07, about 5:00 AM Alberta Time (UTC−6), before this version has been run. Unregistered and **not blind**: the first attempt (`osi_da_rebuild_2026-11-07.md`, result in `findings/osi_rebuild/README.md`, commit `a523d787`) failed. Its largest misses are known (Lethbridge, Calgary-Airdrie and Beddington, south Edmonton), and this design was chosen after seeing them. Approved by the author on 2026-11-07 ("ok"). GitHub only; no OSF filing.

## What changes

One thing changes: how a dissemination area (DA) that crosses a division line is split.

- **Version 1** split it by land area.
- **Version 2** splits it by 2026 referendum electors. The DA is overlaid on Elections Alberta's 2026 voting areas. Each piece of the DA gets the electors of its voting area in proportion to the area of that voting area it covers. The DA's share in each division is its electors there over its electors in total.
- A DA with no electors on this route falls back to land area.

City blocks would be better, but Statistics Canada's block files refused an automated download (HTTP 403), and that is not worked around.

Everything else is unchanged from version 1: targets, prior, weights (1, 0.1, 0.01, 100), the 1% split rule for reporting, dropping municipalities estimated at zero, and the solver.

## Pass/fail rule, unchanged

Hold out each map in turn and predict its published totals. Only divisions whose polygon does not appear on a map in the fit are tested.

- **Pass:** the mean absolute error is 2.0% or less and no division is off by more than 6.0%, on every held-out map.
- **This is the last attempt in this series.** If it fails, the rebuild is reported as failed twice and stops. The data request, or city blocks obtained by hand, would be the next step, under a new plan.

## If it passes

The same uses as version 1:
- Totals for the ¶167 map, including its three amended divisions.
- A rerun of the eligibility check inside divisions, labelled a reconstruction and a sensitivity.

**Signed:** Claude (acting as session agent), directed by Will Conner
