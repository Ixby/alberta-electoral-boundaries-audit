> **Backward:**
> - `analysis/scripts/structural_lane_calibration.py` — produces every number here
> - `data/outputs/structural_lane_calibration_2026-10-31.json` — per-plan results
> - `analysis/scripts/run_structural_battery.py`, `preregistration/november_2026_scoring_spec.md` §3 — the registered lanes
> - `findings/pre_registration_amendment_log.md` — Amendments 9, 23 and 24
>
> **Forward:**
> - the November verdict write-up reports these rates beside the 2×2

# How often the November verdict's lanes fire on neutral maps

**Date:** 2026-10-31 06:00 MDT (Alberta time). **Status:** calibration. No registered rule, threshold or verdict changes; the author chose to measure, not move (option 1).

## Summary

On 200 neutral 91-district maps drawn under the statute's rules (set D, the primary size-matched set under Amendment 24):

- **The structural lane says "replicated" on nearly all of them.** That's 93.5% with the registered battery, where S6 cannot fire on unnamed maps, and 100% with a geometric stand-in for S6.
- **The partisan lane says "present" on 8.5%.**
- **Both lanes fire on 7.5%.**

The structural lane's thresholds sit midway between the majority and minority commission maps (Amendment 9). Both commission maps follow municipal lines and balance populations more tightly than neutral maps do, so neutral maps land on the minority side of the midpoint. Three flags fire on almost every neutral plan:

- **S1, population spread:** 100%.
- **S3, municipal anchoring:** 100%.
- **S2, municipal splits:** 91%.

So a "structural signature replicated" result tells you whether a map resembles the minority more than the majority. It does not tell you whether a map departs from neutral. Read on its own, it is no evidence of engineering. The partisan lane does carry that evidence, and its false-positive rate is close to its nominal 5%.

For the November verdict this means:

- **Both lanes** ("replicates on both lanes"): about 1 in 13 neutral maps would show this. The partisan lane carries the result.
- **Structural only:** 86% of neutral maps would show this (93.5% structural minus 7.5% both). It should be read as "unlike the majority map in structure", not as a signature of intent.
- **Partisan only:** about 1% of neutral maps would show this.
- **Neither:** 5.5% of neutral maps would show this.

These rates are reported beside the registered verdict. They don't replace it.

## What was run

- **Plans.** Four calibration chains (290, 291, 293, 295; 292 and 294 failed to seed) were run with the production set-D sampler (`close_seats_ensemble.py` at `amendment17-local-runs@2994113c`) and the Amendment 23 criteria table. After a 10,000-step burn-in, one plan was kept every 2,500 steps, 50 per chain, 200 in all.
- **Structural lane.** `run_structural_battery.py` was run exactly as registered, on each plan's districts dissolved from the VA polygons. S6 is name-based: it reads district names such as "Airdrie" or "Cochrane" with "Calgary", so it cannot fire on unnamed plans. The registered count is therefore a lower bound. A geometric stand-in replaces names with where each place's people fall:
  - P1 and P5: Airdrie or Red Deer split into 3 or more districts, counting a district when it holds at least 2% of the city's people.
  - P2 to P4: a district with at least 10% of its people in each of Calgary and Cochrane, Chestermere or Rocky View County.
  
  On the commission maps the stand-in agrees with the registered S6: the majority map has no flag (0 hits), and the minority map is flagged (4 hits, against the registered S6's 5).
- **Partisan lane.** P1 to P4 were scored against the 87-district canonical ensemble, from each plan's chain row, in the UCP direction, as spec §3 sets them.

## Results

| Measure | Neutral plans that fire |
|---|---|
| S1_population_mad | 100.0% (200 of 200; 95% interval 98.1–100.0%) |
| S2_municipal_split_count | 91.0% (182 of 200; 95% interval 86.2–94.2%) |
| S3_anchoring_score | 100.0% (200 of 200; 95% interval 98.1–100.0%) |
| S4_polsby_popper_median | 0.0% (0 of 200; 95% interval 0.0–1.9%) |
| S5_drain_score | 43.5% (87 of 200; 95% interval 36.8–50.4%) |
| S6_chair_flag_replication | 0.0% (0 of 200; 95% interval 0.0–1.9%) |
| S6_geometric_stand_in | 89.0% (178 of 200; 95% interval 83.9–92.6%) |

| Lane | Neutral plans |
|---|---|
| Structural lane replicated (registered battery; S6 cannot fire) | 93.5% (187 of 200; 95% interval 89.2–96.2%) |
| Structural lane replicated (geometric S6 stand-in) | 100.0% (200 of 200; 95% interval 98.1–100.0%) |
| Partisan lane present | 8.5% (17 of 200; 95% interval 5.4–13.2%) |
| Both lanes (registered) | 7.5% (15 of 200; 95% interval 4.6–12.0%) |
| Both lanes (geometric S6 stand-in) | 8.5% (17 of 200; 95% interval 5.4–13.2%) |

## Limits

- **The intervals are too narrow.** Plans 2,500 steps apart in one chain are not independent, and the intervals assume they are.
- **Only set D is measured.** Sets A (±12.5%) and C (municipality-aware) would lower S1 and S2–S3 respectively. Set D is used because Amendment 24 makes it primary.
- **The S6 stand-in is this audit's construction,** including its 10% cut. The registered S6 cannot be computed on unnamed maps.
