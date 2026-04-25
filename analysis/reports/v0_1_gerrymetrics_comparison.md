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
| EG | majority_2026 | +0.01320 | +0.01320 | +0.00e+00 |
| Mean-median | majority_2026 | -0.02060 | -0.02060 | +0.00e+00 |
| Declination (adj) | majority_2026 | -0.04551 | -0.04551 | +3.19e-16 |
| Partisan bias | majority_2026 | -0.01515 | -0.01515 | +0.00e+00 |
| EG | minority_2026 | +0.02893 | +0.02893 | +0.00e+00 |
| Mean-median | minority_2026 | -0.01035 | -0.01035 | -1.11e-16 |
| Declination (adj) | minority_2026 | -0.12840 | -0.12840 | +2.78e-16 |
| Partisan bias | minority_2026 | -0.03521 | -0.03521 | -5.55e-17 |

## EG variant family

| Metric | 2019 enacted | Majority 2026 | Minority 2026 |
|---|---|---|---|
| EG (ours) | +0.0149 | +0.0132 | +0.0289 |
| EG (gm cross-check) | +0.0149 | +0.0132 | +0.0289 |
| Difference gap | -0.0552 | -0.0560 | -0.0728 |
| Loss gap | +0.0850 | +0.0824 | +0.1307 |
| Surplus gap | -0.0701 | -0.0692 | -0.1017 |
| Vote-centric gap | +0.1735 | +0.1679 | +0.2726 |
| Vote-centric gap 2 | +0.0701 | +0.0665 | +0.1266 |
| Tau gap (τ=0, ≈2×EG) | +0.0298 | +0.0264 | +0.0579 |
| Tau gap (τ=1) | +0.1508 | +0.1551 | +0.2417 |

## Lopsided margins: t-test (Wang 2016) vs Mann-Whitney U

| Map | t-test diff (adj) | t-test p | Mann-Whitney stat (adj) | MW p |
|---|---|---|---|---|
| 2019_enacted | +0.0599 | 0.9952 | -606 | 0.0265 |
| majority_2026 | +0.0587 | 0.9908 | -343 | 0.0421 |
| minority_2026 | +0.0744 | 0.9951 | -321 | 0.0251 |

_Note: positive t-diff and MW-stat = UCP wins by larger margins than NDP (packing/cracking signal if combined with seat asymmetry)._

_Generated 2026-04-25 07:25 — elapsed 4s_