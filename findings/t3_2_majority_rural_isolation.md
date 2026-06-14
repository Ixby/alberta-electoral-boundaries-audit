---
name: t3_2_majority_rural_isolation
date: 2026-06-11
preregistration: preregistration/t3_2_majority_rural_isolation_design.md
type: counter-test
verdict: H0_supported
script_commit: 5fbd1ca113fca2a83f9fdf057e892db000c5eed5
---

> **⚠ INTRA-SESSION EXPLORATORY — NOT PRE-REGISTERED.** Design and script were co-committed 85 seconds before this result (see design doc §"Status reclassification" for verification). Read as exploratory evidence, not as a confirmatory pre-registered test. Design doc reclassified 2026-06-12 per T1.7 R2 Ref #4. Also note: the design doc's Airdrie classifier amendment (`"Airdrie"` without hyphen) was NOT reflected in the script at time of original execution — `"Airdrie-"` was used, meaning `Airdrie East` (minority, space-separated) was misclassified as rural. This verdict reflects the hyphen-sensitive run. The corrected classifier is in the script as of 2026-06-13. A re-run with the corrected classifier is queued for the November-window genuinely-pre-registered T3.2.

> **Backward:**
> - `preregistration/t3_2_majority_rural_isolation_design.md` — intra-session exploratory design (reclassified 2026-06-12)
> - `analysis/scripts/t3_2_majority_rural_isolation.py` — this analysis (Airdrie classifier corrected 2026-06-13)
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
