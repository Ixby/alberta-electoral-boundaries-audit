---
name: t3_2_majority_rural_isolation
date: 2026-06-11
preregistration: preregistration/t3_2_majority_rural_isolation_design.md
type: counter-test
verdict: H0_supported
script_commit: 5fbd1ca113fca2a83f9fdf057e892db000c5eed5
---

> **Backward:**
> - `preregistration/t3_2_majority_rural_isolation_design.md` — pre-committed design
> - `analysis/scripts/t3_2_majority_rural_isolation.py` — this analysis
> - `findings/joint_outlier_score.json` — source of the majority drain anomaly motivating the test
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.6 — symmetry-of-test-selection audit (extend with this entry)
> - `findings/README.md` — index

# T3.2 — Majority rural-isolation counter-test (result)

## Summary

Majority is most-isolated on only 1 of 3 metrics and is not the most isolated map overall (enacted_2019 is). The drain anomaly is consistent with natural Alberta rural geography, not engineered isolation.

## Per-map metric values

| Map | n EDs | n rural | R1 median PP (rural) | R2 mean urban-nbrs/rural ED | R3 frac rural with 0 urban nbrs |
|---|---:|---:|---:|---:|---:|
| majority_2026 | 89 | 28 | 0.3465 | 2.143 | 0.107 |
| minority_2026 | 89 | 23 | 0.3971 | 2.478 | 0.043 |
| enacted_2019 | 87 | 31 | 0.3866 | 1.774 | 0.258 |

## Rank table (1 = most rural-isolated on the axis)

| Map | R1 (median PP↓) | R2 (urban-nbrs↓) | R3 (zero-urban frac↑) | Mean rank |
|---|---:|---:|---:|---:|
| majority_2026 | 1 | 2 | 2 | 1.667 |
| minority_2026 | 3 | 3 | 3 | 3.000 |
| enacted_2019 | 2 | 1 | 1 | 1.333 |

## Decision (per §5 of the pre-registered design)

- **Verdict:** `H0_supported`
- **Majority is rank-1 on:** 1 of 3 metrics
- **Overall most-isolated map:** enacted_2019

Majority is most-isolated on only 1 of 3 metrics and is not the most isolated map overall (enacted_2019 is). The drain anomaly is consistent with natural Alberta rural geography, not engineered isolation.

## Reproducibility

```bash
python analysis/scripts/t3_2_majority_rural_isolation.py \
  --output-json findings/t3_2_majority_rural_isolation.json \
  --output-md   findings/t3_2_majority_rural_isolation.md
```

Script commit: `5fbd1ca113fca2a83f9fdf057e892db000c5eed5`
