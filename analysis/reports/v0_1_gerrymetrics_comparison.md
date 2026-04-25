# gerrymetrics Cross-Validation & EG Variant Family

All metrics computed with equal-turnout assumption. Sign convention: **positive = UCP-favoured** throughout.
gerrymetrics input: `ndp_share = 1 − ucp_share` (NDP plays 'Dem' role). Declination and lopsided-margins test statistics negated to match sign convention.

## Cross-validation: our implementation vs gerrymetrics

| Metric | Map | Ours | gerrymetrics | Difference |
|---|---|---|---|---|
| EG | 2019_enacted | +0.01491 | +0.01491 | +0.00e+00 |
| Mean-median | 2019_enacted | -0.00767 | -0.00767 | -5.55e-17 |
| Declination (adj) | 2019_enacted | -0.04509 | -0.04509 | +1.73e-16 |
| Partisan bias | 2019_enacted | -0.00575 | -0.00575 | +5.55e-17 |
| EG | majority_2026 | +0.00595 | +0.00595 | +0.00e+00 |
| Mean-median | majority_2026 | -0.01791 | -0.01791 | +0.00e+00 |
| Declination (adj) | majority_2026 | -0.01313 | -0.01313 | +3.47e-17 |
| Partisan bias | majority_2026 | -0.04023 | -0.04023 | +0.00e+00 |
| EG | minority_2026 | +0.02617 | +0.02617 | +0.00e+00 |
| Mean-median | minority_2026 | -0.01074 | -0.01074 | +5.55e-17 |
| Declination (adj) | minority_2026 | -0.09895 | -0.09895 | +3.89e-16 |
| Partisan bias | minority_2026 | -0.04217 | -0.04217 | -5.55e-17 |

## EG variant family

| Metric | 2019 enacted | Majority 2026 | Minority 2026 |
|---|---|---|---|
| EG (ours) | +0.0149 | +0.0060 | +0.0262 |
| EG (gm cross-check) | +0.0149 | +0.0060 | +0.0262 |
| Difference gap | -0.0552 | -0.0572 | -0.0662 |
| Loss gap | +0.0850 | +0.0691 | +0.1185 |
| Surplus gap | -0.0701 | -0.0631 | -0.0923 |
| Vote-centric gap | +0.1735 | +0.1404 | +0.2454 |
| Vote-centric gap 2 | +0.0701 | +0.0462 | +0.1115 |
| Tau gap (τ=0, ≈2×EG) | +0.0298 | +0.0119 | +0.0523 |
| Tau gap (τ=1) | +0.1508 | +0.1212 | +0.2133 |

## Lopsided margins: t-test (Wang 2016) vs Mann-Whitney U

| Map | t-test diff (adj) | t-test p | Mann-Whitney stat (adj) | MW p |
|---|---|---|---|---|
| 2019_enacted | +0.0599 | 0.9952 | -606 | 0.0265 |
| majority_2026 | +0.0601 | 0.9967 | -627 | 0.0262 |
| minority_2026 | +0.0709 | 0.9968 | -479 | 0.0217 |

_Note: positive t-diff and MW-stat = UCP wins by larger margins than NDP (packing/cracking signal if combined with seat asymmetry)._

_Generated 2026-04-25 08:50 — elapsed 3s_