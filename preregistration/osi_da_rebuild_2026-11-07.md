# Rebuilding the panel's small-area population figures from what was published (written before any fitting)

> Written 2026-11-07, about 3:05 AM MST, before any fit has been run. Unregistered and not blind: the author knows the published totals and the 2021 counts. Requested by the author on 2026-11-07. GitHub only; no OSF filing. Nothing here is a finding on whether any map is lawful or a gerrymander.

## Why

The commission and the panel used the Office of Statistics and Information's July 1, 2024 estimates for each dissemination area (DA), which Elections Alberta totalled for each proposed division. That file is not public. A data request is being drafted separately. Meanwhile, the published division totals are many views of the same file, and they can be used to rebuild figures close to it.

## Inputs

- **Published division totals, fit targets:**
  - Majority, 89 divisions: `PopCensus` on `ea_majority_2026_eds.gpkg`
  - Minority, 89 divisions: `ea_minority_2026_eds.gpkg`
  - Panel, 91 divisions: Appendix 7, on the v3 reconstruction
- **Prior:** each DA's 2021 census count, scaled by its municipality's growth from 2021 to 2024 in the public municipal estimates (open.alberta.ca, file updated January 14, 2026, SHA-256 `3d7655dc4e95bcc459aa542f3d8447d22d3a2abd69654610d5d478b5c110833f`).
  - That file is a later vintage than the one the commission used, so it is a prior and a soft constraint, never a hard one.
  - DAs with a 2021 count under 50 get a prior of 50, so new neighbourhoods can grow.
- **Province total:** 4,888,723, hard.

## Method

- **Splitting a DA across divisions:** a DA crossing a division line is split by area share. This is a guess: how Elections Alberta split such DAs is not published. The share of province population in split DAs is reported.
- **The fit:** non-negative figures for the 6,203 DAs, solving a weighted least-squares problem:
  - Division totals: weight 1, relative to each total.
  - Municipal 2024 estimates: weight 0.1.
  - Staying close to the prior: weight 0.01, in proportion to each prior.
- **The code:** `findings/osi_rebuild/rebuild_da_2024.py`. The weights are fixed here and not tuned after seeing results.

## Pass/fail check, fixed now

Hold one map out, fit on the other two, and predict the held-out map's published totals. Each map is held out in turn.

- **Only divisions that differ count.** A division whose polygon is the same on a map used in the fit is excluded from the test, because predicting it is trivial. Its count is reported.
- **Pass:** on each held-out map, the mean absolute error on those divisions is 2.0% or less, and no division is off by more than 6.0%.
- **The panel's map is held to the same thresholds,** but any miss there is reported beside its reconstruction error, because its polygons are v3, not official.
- **Fail:** if any held-out map fails, the rebuilt figures are reported as not reproducing the source, and they are not used to total new boundaries.

## If it passes

Using the fit on all three maps:
- **The ¶167 map:** totals for its 91 divisions, including the three amended ones, with deviations, the ±25% band and s.15(2).
- **The census and elector checks:** rerun inside divisions with the rebuilt 2024 figures in place of 2021, for northeast Calgary in particular. This is reported as a sensitivity.

Every rebuilt figure is labelled as a reconstruction, not the source data.

**Signed:** Claude (acting as session agent), directed by Will Conner
