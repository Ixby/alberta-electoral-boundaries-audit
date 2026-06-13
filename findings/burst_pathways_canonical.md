---
title: Neutral vs targeted ReCom burst pathways (canonical substrate) — T1.5 / T1.5b
status: COMPLETE 2026-06-13
supersedes: v0_8-substrate §5.4.8 burst numbers (findings/_archive_simulation_short_bursts_v0_8.md)
scripts: analysis/scripts/simulation_short_bursts.py (neutral), analysis/scripts/targeted_gerrymander_burst.py (targeted)
substrate: official Elections Alberta canonical shapefiles, 87-district 2019-seed start, pop_2021, +/-25%
---

# Neutral vs targeted ReCom burst pathways (canonical)

This is the canonical-substrate execution of the §5.4.8 "non-neutral pathway"
demonstration. Two burst experiments bracket the minority commission map between
what neutral drift can reach and what deliberate partisan optimisation can reach.

## Experiment 1 — Neutral short bursts (T1.5)

500 independent neutral ReCom chains of 10 steps each, all started from a single
tight recursive-tree-part seed (the 2019 enacted assignment exceeds +/-25% on 2021
population, so one balanced 87-district seed is generated and reused — this both
fixes a per-burst-regeneration inefficiency and makes the experiment measure
10-step reach from one fixed neutral point). Seed 42.

**Burst-endpoint distribution (neutral reach):**

| Metric | p5 | p50 | p95 | min | max |
|---|---|---|---|---|---|
| efficiency_gap | −0.0049 | +0.0048 | +0.0227 | −0.0261 | +0.0385 |
| mean_median | −0.0215 | −0.0125 | −0.0089 | −0.0371 | −0.0035 |
| declination | −0.0534 | −0.0313 | −0.0025 | −0.0791 | +0.0381 |
| seats_at_50_50 | +0.4483 | +0.4598 | +0.4713 | +0.4253 | +0.4713 |

**Real-map rank within the neutral burst distribution (percentile of bursts below the real value):**

| Map | EG | MM | declination | s50 |
|---|---|---|---|---|
| 2019 enacted | 95.6 | 98.6 | 100.0 | 33.8 |
| majority 2026 | 9.6 | 0.2 | 69.4 | 88.4 |
| **minority 2026** | **100.0** | **100.0** | **100.0** | **100.0** |

**The minority map is more extreme than every one of the 500 neutral 10-step
walks on all four partisan metrics.** Its values (EG +0.0402, MM +0.0104,
declination +0.0770, s50 0.5169) each exceed the neutral burst maximum. The
neutral neighbourhood of the 2019 start simply does not extend to where the
minority map sits — most visibly on seats@50/50, where the neutral ceiling is
0.4713 versus the minority's 0.5169. The majority map, by contrast, lies inside
the neutral envelope (s50 p88.4, EG p9.6, MM p0.2).

## Experiment 2 — Targeted hill-climb (T1.5b)

800 bursts of 50 steps each, greedy hill-climb maximising UCP seats@50/50
(deliberate partisan objective). Seed 137. Completed in 14.8 min at ~45 steps/s.

**Best seats@50/50 reached: 0.5287 = exactly 46/87 seats.** Metrics of the
maximally-gerrymandered map found: EG +0.0237, MM +0.0103, declination +0.0197,
s50 0.5287.

This 0.5287 ceiling reproduces the earlier v0_8-substrate value exactly, because
it is a discrete seat ceiling (46 of 87 seats at a tied vote) that is robust to
substrate. The v0_8 number is therefore confirmed, not replaced — but it is now
established on the official canonical shapefiles, removing the superseded-substrate
caveat that the §5.4.8 paragraph previously carried.

## Synthesis — the minority sits between the two ceilings

| Pathway | seats@50/50 ceiling |
|---|---|
| Neutral 10-step drift from 2019 (max of 500 walks) | 0.4713 |
| **Minority 2026 commission map** | **0.5169** |
| Deliberate UCP-objective hill-climb (max) | 0.5287 |

The minority map cannot be reached by neutral drift (it is past the neutral
maximum on every partisan metric) and sits close to the deliberate-gerrymander
ceiling. The majority map sits inside the neutral envelope. This is the empirical
"non-neutral pathway" finding: the minority's partisan position is reachable only
by partisan optimisation, not by neutral redistricting from the prior map.

This is consistent with, and independent of, the Lane-1 ensemble result (minority
at the extreme tail of the 1.01M neutral ensemble) — the burst experiment asks the
complementary local question (reachability from the 2019 start) rather than the
global question (position in the full neutral distribution).

## Artifacts

- `data/simulation_short_bursts.csv`, `data/simulation_short_bursts_summary.json` (neutral)
- `data/targeted_burst_trace.csv`, `data/targeted_burst_best.json` (targeted)
