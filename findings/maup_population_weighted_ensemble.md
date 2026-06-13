---
title: Population-weighted attribution placement vs canonical ensemble (T1.4a)
status: COMPLETE
---

# T1.4a — Population-weighted attribution placement

**Why no per-plan assignment archive is needed.** The canonical ReCom ensemble assigns *atomic VAs* to districts; a VA is never split across its own assigned district, so the ensemble's partisan-metric distribution is invariant to the VA→ED attribution method. Attribution can only move a *real-map* value. T1.4a therefore reduces to scoring both commission maps under centroid and under population-weighted (VA × ED × 2021-DA three-way overlay) attribution from the same VA basis, and re-placing each against the invariant 1,010,000-plan ensemble.

**Verdict: the published percentile claims SURVIVES** (max |percentile shift| = 0.95 pp across all metrics and both maps; acceptance threshold ±2 pp).

## minority_2026

| Metric | Centroid value @ pctile | Pop-weighted value @ pctile | Δ pctile |
|---|---|---|---|
| efficiency_gap | +0.0402 @ p94.39 | +0.0395 @ p93.83 | -0.57 |
| mean_median | +0.0104 @ p99.98 | +0.0096 @ p99.95 | -0.02 |
| declination | +0.0770 @ p98.79 | +0.0775 @ p98.81 | +0.02 |
| seats_at_50_50 | +0.5169 @ p99.99 | +0.5169 @ p99.99 | +0.00 |

## majority_2026

| Metric | Centroid value @ pctile | Pop-weighted value @ pctile | Δ pctile |
|---|---|---|---|
| efficiency_gap | +0.0010 @ p15.47 | +0.0004 @ p14.52 | -0.95 |
| mean_median | -0.0362 @ p0.92 | -0.0360 @ p0.97 | +0.05 |
| declination | -0.0267 @ p20.38 | -0.0268 @ p20.29 | -0.09 |
| seats_at_50_50 | +0.4607 @ p77.81 | +0.4607 @ p77.81 | +0.00 |
