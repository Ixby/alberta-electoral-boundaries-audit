> **⚠ SUBSTRATE-STATUS: v0_7 DPG (substrate-stale; canonical recompute queued, 2026-06-11).**
> The four extended partisan metrics below (Partisan Bias, Lopsided-t, Partisan Gini,
> Responsiveness) were computed against v0_7 DPG shapefiles (89 EDs) and a 10,000-sample
> ReCom MCMC ensemble (seed 42, ±25 %). The audit's substrate-provenance audit
> (2026-06-11) flagged this file as the last remaining headline-cited finding not yet
> re-anchored on the canonical Elections Alberta shapefiles + canonical 1,010,000-plan
> ensemble. The §5.2.9 §1.1 BH-table rows 5–6 (Lopsided Margins t = 3.43 / 3.05)
> derive from these numbers and are accurate against v0_7 substrate. Canonical
> recompute is queued in `TODO_REMEDIATION.md` (T4.7). The Lopsided Margins finding
> is independently disclosed in §5.2.9 as a structural property of Alberta's political
> geography present in all three maps including the 2019 baseline, so the audit's
> headline does not depend on the exact v0_7 vs canonical values.
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