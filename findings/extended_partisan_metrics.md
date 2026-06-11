> **⚠ SUPERSEDED 2026-06-11 by `findings/extended_partisan_metrics_canonical.md`.**
> The four metrics below were computed against v0_7 DPG shapefiles + 10k ReCom.
> Canonical-substrate recompute (canonical EA shapefiles + canonical VA centroid-in-
> polygon attribution + 1,010,000-plan canonical ensemble) has landed:
>
> | Metric | v0_7 maj | canonical maj | v0_7 min | canonical min | 2019 (canonical) |
> |---|---:|---:|---:|---:|---:|
> | Partisan Bias | −0.0402 | **−0.0281** | −0.0422 | **+0.0169** | −0.0057 |
> | Lopsided-t | +3.158 | **+3.800** | +3.491 | **+3.169** | +3.070 |
> | Responsiveness | 1.15 | **1.12** | 2.41 | **1.69** | 2.87 |
>
> The minority's PB sign-flipped on canonical (+0.0169 vs −0.0422). The Lopsided-t
> signal remains a structural property of Alberta's political geography present on
> all three maps. Academic-report §5.2.9 and §1.1 BH-table rows 5-6 have been
> refreshed with the canonical numbers. This file kept for trail-of-work only.
>
> **Backward:**
> - extended-metrics computation script (companion in `analysis/scripts/`)
> - v0_7 shapefiles (89 EDs)
> - 10k ReCom MCMC samples (seed 42, ±25%) for percentile placement
>
> **Forward:**
> - `reports/academic/report_academic.md` — incorporates the extended partisan metrics
> - `findings/joint_outlier_score_summary.md` — uses these metrics as channel inputs
> - `findings/README.md` — indexes this finding

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