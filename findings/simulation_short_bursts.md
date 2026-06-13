# MCMC Short-Burst Analysis — Alberta 2026 Electoral Maps

**Config:** 500 bursts × 10 steps each; pop deviation ±25%; seed 42.
Starting point: 2019 enacted assignment. Each burst is an independent ReCom chain with a unique seed.

## Burst-endpoint distribution

| Metric | Mean | p5 | p50 | p95 | Min | Max |
|---|---|---|---|---|---|---|
| efficiency_gap | +0.0074 | -0.0049 | +0.0048 | +0.0227 | -0.0261 | +0.0385 |
| mean_median | -0.0134 | -0.0215 | -0.0125 | -0.0089 | -0.0371 | -0.0035 |
| declination | -0.0254 | -0.0534 | -0.0313 | -0.0025 | -0.0791 | +0.0381 |
| seats_at_50_50 | +0.4566 | +0.4483 | +0.4598 | +0.4713 | +0.4253 | +0.4713 |

## Real map percentile ranks within burst distribution

A high rank means the real map score is more extreme than most 10-step neighbourhood walks can reach from the 2019 starting point.

| Map | Metric | Value | Burst pct rank |
|---|---|---|---|
| 2019_enacted | efficiency_gap | +0.0241 | 95.6 |
| 2019_enacted | mean_median | -0.0077 | 98.6 |
| 2019_enacted | declination | +0.0451 | 100.0 |
| 2019_enacted | seats_at_50_50 | +0.4598 | 33.8 |
| majority_2026 | efficiency_gap | +0.0010 | 9.6 |
| majority_2026 | mean_median | -0.0362 | 0.2 |
| majority_2026 | declination | -0.0267 | 69.4 |
| majority_2026 | seats_at_50_50 | +0.4607 | 88.4 |
| minority_2026 | efficiency_gap | +0.0402 | 100.0 |
| minority_2026 | mean_median | +0.0104 | 100.0 |
| minority_2026 | declination | +0.0770 | 100.0 |
| minority_2026 | seats_at_50_50 | +0.5169 | 100.0 |

_Generated 2026-06-13 03:36 — elapsed 186s_