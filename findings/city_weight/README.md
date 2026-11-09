# How much weight have Alberta's drawers given city boundaries?

> **Unregistered and not blind.** Plan: `preregistration/city_weight_calibration_2026-11-07.md` (`5dc4a0dd`), written before anything here was computed. The split ratios of the 2019, majority and minority maps and the Lethbridge results were already known. GitHub only. Nothing here says whether any map is a gerrymander or why any line was drawn.

## Split ratios

**R** is the share of 169 municipalities split into more pieces than their population needs (`real_ratios.py`, `real_ratios.json`). Older maps are measured on 2021 municipalities and population, so their R is approximate.

The Calgary and Edmonton line crossings are in `big_city_lines.json`.

## Implied weight

`implied_w.py` reads each map's R on the calibration curve for its number of districts, by linear interpolation (`implied_w.json`). The curves come from:
- `calibration_{a,b,c}.jsonl`: indices 280–296, 10,000 steps each;
- the Amendment 17 runs (`alberta_audit/analysis/methodology/amendment17_chain_runs/`).

| Map | Districts | R | Implied W | Sets the range |
|---|---|---|---|---|
| 2003 commission | 83 | 0.178 | 0.553 | yes |
| 2010 commission | 87 | 0.160 | 0.537 | yes |
| 2017 commission | 87 | 0.166 | 0.517 | yes |
| 2026 commission majority | 89 | 0.112 | 0.661 | yes |
| 2026 commission minority | 89 | 0.249 | 0.312 | no |
| 2026 panel (v3) | 91 | 0.148 | 0.566 | no |
| ¶167 | 91 | 0.136 | 0.593 | no |

**Commission range: W = 0.517 to 0.661.** The 0.5 used in every city-aware run so far sits just below it.

**Limits:**
- Each curve point is one 10,000-step chain. Some 91-district points are 6,000 steps (`implied_w.py` names the source of each).
- The 89-district curve is nearly flat between W = 0.65 (R 0.113) and 0.75 (0.108). So the majority's 0.661 is imprecise: any W from about 0.65 to 0.75 fits it within the noise.
- **One run failed:** the 87-district point at W = 0.25 (idx 295) could not seed ("Could not find a possible cut after 50000 attempts", `calib_295.err`). It is not needed, because every 87-district map's R lies between the W = 0.5 and W = 0.75 points.

## Lethbridge at the two ends of the range

The plan reruns the Lethbridge city-aware regional redraw, unchanged except for W, at the lowest and highest commission W (`lethbridge_at_w.py`, `lethbridge_at_w.json`):
- 4 chains of 50,000 steps;
- the original seed salts (`regional_Lethbridge_muni_{1..4}`), so each chain differs from its W = 0.5 counterpart only in W;
- the reading rule of `preregistration/hybrid_regions_2026-11-07.md`.

Run 2026-11-08, 6:06 to 6:27 PM Alberta Time.

| W | Lethbridge in 2 / 3 / 4 pieces | Panel: 4 pieces | Panel: city NDP votes in lopsided losses (44.7%) |
|---|---|---|---|
| 0.517 | 51.0% / 48.2% / 0.8% | p99.6 | p93.4, inside |
| 0.5 (as run, `../hybrid_regions/`) | 51.5% / 47.6% / 0.9% | p99.5 | p93.3, inside |
| 0.661 | 67.9% / 31.9% / 0.3% | p99.9 | **p96.5, beyond the line** |

**Reading.** The plan's rule reads the lopsided-loss share. At the low end of the range the commissions have applied, the panel's map is inside the line, as at 0.5. At the high end it is beyond it. So whether the Lethbridge result counts as unusual depends on which commission's treatment of city boundaries the comparison uses. The weight that matches the 2026 commission majority's own map is the one that puts it beyond the line.

The four-way split itself is rare at every W in the range: 0.3% to 0.8% of plans.

**Multiple testing.** The four new comparisons are in the family ledger (`../test_ledger/`). None survives correction, and the smallest p is 0.0026 for the four-way split at W = 0.661.

As always, `../hybrid_regions/threshold_grounding.md` gives the literature context for the 95th-percentile line.
