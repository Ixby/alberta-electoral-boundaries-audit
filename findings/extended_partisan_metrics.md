# Extended Partisan Metrics — Alberta 2026 Electoral Maps

Computed against v0_7 shapefiles (89 EDs, full province coverage).
Ensemble percentile ranks from 10k ReCom MCMC samples (seed 42, ±25%).

## Results

| Map | N EDs | Partisan Bias | PB pct | Lopsided-t | Lopsided-p | Partisan Gini | Responsiveness |
|-----|-------|--------------|--------|-----------|-----------|--------------|----------------|
| 2019_enacted | 87 | -0.0057 | +99.4 | +3.070 | 0.003 | +0.0252 | 2.87 |
| majority_2026 | 87 | -0.0402 | +76.8 | +3.158 | 0.002 | +0.0227 | 1.15 |
| minority_2026 | 83 | -0.0422 | +49.7 | +3.491 | 0.001 | +0.0326 | 2.41 |

## Interpretation

**Partisan Bias**: Positive = UCP gets >50% of seats at 50/50 vote.
**Lopsided Margins t**: Positive = UCP wins by larger margins than NDP (packing signal).
**Partisan Gini**: Positive = asymmetry favours UCP across the full seats-votes curve.
**Responsiveness**: How many extra seats per 1% vote swing. Lower = more entrenched.

_Generated 2026-04-25 08:50 — elapsed 3s_