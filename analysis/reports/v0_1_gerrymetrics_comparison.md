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
| EG | majority_2026 | -0.00734 | -0.00734 | +5.38e-17 |
| Mean-median | majority_2026 | +0.00829 | +0.00829 | +1.67e-16 |
| Declination (adj) | majority_2026 | -0.02080 | -0.02080 | +2.84e-16 |
| Partisan bias | majority_2026 | +0.01515 | +0.01515 | +0.00e+00 |
| EG | minority_2026 | +0.02652 | +0.02652 | +0.00e+00 |
| Mean-median | minority_2026 | -0.01107 | -0.01107 | +1.11e-16 |
| Declination (adj) | minority_2026 | -0.13514 | -0.13514 | +5.83e-16 |
| Partisan bias | minority_2026 | -0.02113 | -0.02113 | -5.55e-17 |

## EG variant family

| Metric | 2019 enacted | Majority 2026 | Minority 2026 |
|---|---|---|---|
| EG (ours) | +0.0149 | -0.0073 | +0.0265 |
| EG (gm cross-check) | +0.0149 | -0.0073 | +0.0265 |
| Difference gap | -0.0552 | -0.0868 | -0.0764 |
| Loss gap | +0.0850 | +0.0721 | +0.1295 |
| Surplus gap | -0.0701 | -0.0794 | -0.1029 |
| Vote-centric gap | +0.1735 | +0.1479 | +0.2704 |
| Vote-centric gap 2 | +0.0701 | +0.0340 | +0.1239 |
| Tau gap (τ=0, ≈2×EG) | +0.0298 | -0.0147 | +0.0530 |
| Tau gap (τ=1) | +0.1508 | +0.1261 | +0.2405 |

## Lopsided margins: t-test (Wang 2016) vs Mann-Whitney U

| Map | t-test diff (adj) | t-test p | Mann-Whitney stat (adj) | MW p |
|---|---|---|---|---|
| 2019_enacted | +0.0599 | 0.9952 | -606 | 0.0265 |
| majority_2026 | +0.0745 | 0.9983 | -294 | 0.0071 |
| minority_2026 | +0.0737 | 0.9945 | -320 | 0.0242 |

_Note: positive t-diff and MW-stat = UCP wins by larger margins than NDP (packing/cracking signal if combined with seat asymmetry)._

_Generated 2026-04-24 23:12 — elapsed 4s_