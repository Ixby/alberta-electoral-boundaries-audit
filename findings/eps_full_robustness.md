---
title: Proposal-epsilon robustness check (T1.11 / Amendment 11)
status: COMPLETE 2026-06-13 (100k pilot + 1.01M confirmation both run)
salt: mcmc_ensemble_250k (same base_seed=1432864451 as canonical)
supersedes: nothing — this is a robustness check, not a headline replacement
---

## Headline (1.01M confirmation)

The full 1,010,000-plan full-band (epsilon = ±25%) ensemble confirms the pilot.
Minority partisan-metric percentiles vs the canonical half-band (±12.5%) ensemble:

| Metric (minority) | Canonical (±12.5%) | eps_full 1.01M (±25%) | Shift |
|---|---|---|---|
| efficiency_gap | p94.39 | p94.38 | −0.01 |
| mean_median | p99.98 | p99.96 | −0.02 |
| declination | p98.79 | p98.74 | −0.05 |
| seats_at_50_50 | p99.99 | p99.97 | −0.02 |

All shifts < 0.05 pp at publication-grade resolution (n_eff 1573–2565). The
partisan headline is invariant to the proposal-epsilon. population_mad confirms
the malapportionment mechanism at scale (eps_full band p5/p50/p95 =
5265/6379/7464 vs canonical 2613/3163/3709; both real maps at p0). Detail below.

# Proposal-epsilon robustness check (T1.11 / Amendment 11)

## Question

The canonical 1,010,000-plan ReCom ensemble draws each bipartition with
`recom(..., epsilon = pop_deviation / 2.0)` — i.e. each ReCom split must balance
the two new districts to within ±12.5%, even though the audit's documented legal
space is ±25% (the `alberta_statutory_population_constraint` admits ±25%, with
the s.15(2) carve-out reaching −50%). Referee #2 (D-item A13) asked whether the
half-band proposal under-samples the legal space and whether the headline
percentile placements depend on that choice.

## Method

`mcmc_ensemble.py:563` was changed from `epsilon = pop_deviation / 2.0` to
`epsilon = pop_deviation` (full ±25% proposal balance) and the ensemble was
regenerated under `run_id="eps_full"` — a fully separate output prefix so the
published canonical files are untouched. The base seed is identical to canonical
(`get_canonical_seed("mcmc_ensemble_250k")` = 1432864451), so the **only**
difference between the two ensembles is the proposal epsilon. This is a clean
controlled comparison.

- **Pilot:** 100,000 plans (4 chains × 25,000), completed 2026-06-13, 676 s.
  n_eff per metric 159–227 (modest tail resolution, adequate for a detection run).
- **Confirmation:** 1,010,000 plans (4 chains × 252,500), in progress
  (`run_id="eps_full"`, ~1.7 h). Numbers below are updated from the full run on
  completion.

## Result (100k pilot)

### The partisan-fairness distributions are invariant to epsilon

The neutral-ensemble band (p5/p50/p95) for the partisan metrics is unchanged
between the half-band canonical and the full-band eps_full ensemble:

| Metric | Canonical band (±12.5%) | eps_full band (±25%) |
|---|---|---|
| efficiency_gap | −0.01 / 0.02 / 0.04 | −0.01 / 0.02 / 0.04 |
| seats_at_50_50 | 0.43 / 0.45 / 0.48 | 0.43 / 0.45 / 0.48 |

Consequently the minority commission map's percentile placement on every
partisan metric is robust (shifts < 0.15 pp):

| Metric (minority 2026) | Canonical pctile | eps_full pctile | Shift |
|---|---|---|---|
| efficiency_gap | p94.39 | p94.30 | −0.09 |
| mean_median | p99.98 | p99.91 | −0.07 |
| declination¹ | p98.79 | p98.92 | +0.13 |
| seats_at_50_50 | p99.99 | p99.98 | −0.01 |

¹ The published canonical *percentiles CSV* still carries the pre-Amendment-10
declination convention (−0.077 @ p1.21); the correct post-Amendment-10 value is
+0.077 @ p98.79, which is what the report and the chain CSVs use, and what the
eps_full run reproduces. See the separate stale-derived-output note.

**All four partisan metrics fall in the "Robust" band (< 2 pp shift). The
minority stays in the extreme tail on mean-median, seats@50/50 and declination
(≥ p98.9) and at p94.3 on the efficiency gap (sub-threshold under both ensembles).
The proposal-epsilon choice does not affect the partisan headline.**

### The population-equality distribution is NOT invariant to epsilon

The structural population-MAD metric behaves very differently:

| Metric | Canonical band (±12.5%) | eps_full band (±25%) |
|---|---|---|
| population_mad | 2613 / 3163 / 3709 | 5229 / 6393 / 7461 |

Widening the proposal balance to ±25% lets ensemble plans become roughly twice
as malapportioned (median per-district MAD ~6400 vs ~3160). Both commission maps
(MAD 2827 majority / 3938 minority) then sit *below* the entire full-band
ensemble (p0), where under the canonical band they sit at p15.8 / p99.0.

This is the expected mechanism, not a bug, and it carries a methodological
implication: **the full ±25% proposal produces a neutral comparator that is
wildly malapportioned relative to any real redistricting output, which makes it
an unrealistic baseline for the Lane-2 population-equality battery.** Real
commissions target near-equality; an ensemble whose typical plan is ±25%
imbalanced is not a faithful "neutral" reference for the population metric.

## Conclusion

T1.11 is resolved as a **robustness check, not a headline replacement**:

1. The partisan-fairness headline (minority in the extreme tail on 3 of 4
   metrics, sub-threshold EG) is **fully robust** to the proposal-epsilon choice.
   The partisan ensemble distributions are identical to two decimal places.
2. The canonical ensemble should **remain at epsilon = pop_deviation / 2.0**,
   because the full-band ensemble degrades the population-equality comparator.
   The code change is therefore reverted/parametrised after this run so canonical
   reproduction is faithful; the eps_full artifacts are retained as the
   robustness evidence.

This mirrors how SZAT and the constraint-enforcing ensemble were handled:
a more-permissive alternative null is run symmetrically, the partisan tail is
shown to survive, and the headline is reported under the realistic baseline.

## Artifacts

- `data/outputs/simulated_ensemble_percentiles_eps_full_pilot.csv` (100k pilot)
- `data/outputs/simulated_ensemble_raw_samples_eps_full_pilot.csv` (100k pilot)
- `data/outputs/simulated_ensemble_percentiles_eps_full.csv` (1.01M, on completion)
- `data/simulation_checkpoints_eps_full_pilot/` and `.../eps_full/` chain CSVs
