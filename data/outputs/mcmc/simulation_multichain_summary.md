# Multi-chain MCMC convergence summary

> **Superseded (banner added 2026-07-13).** This is an early diagnostic run (3 chains × 150,000 steps, seeds [42, 101, 2024]) — not the canonical ensemble the current report cites. Its "NOT CONVERGED" verdict was correct for *this* run and is preserved below as historical record, but it does not describe the audit's present evidentiary basis: the canonical ensemble is now 1,010,000 plans (4 chains × 252,500 steps), rerun clean 2026-07-12, with its own convergence diagnostics at `data/outputs/simulation_convergence_diagnostics_canonical.json` (Gelman-Rubin R-hat 1.00011–1.00205, publication-grade ESS 1,413–1,522) — see `reports/academic/report_academic.md` §5.4.9. The "Implications for paper §5.4" section below refers to an old section-numbering scheme and should not be read as a live caveat on the current report.

**Script:** `analysis/scripts/simulation_multichain_ensemble.py`

**Seeds:** [42, 101, 2024]  

**Chains:** 3  

**Steps per chain:** 150,000  

**Burn-in fraction:** 10%  

**Common thinning factor (pooled CSV):** 81  

**Total runtime:** 5474s (91.2 min)


## Per-metric diagnostics

| Metric | R-hat (split) | Per-chain ESS | Combined ESS | Thin | Verdict |
|---|---:|---|---:|---:|---|
| efficiency_gap | 1.0075 | [226, 243, 178] | 648 | 75 | UNDER-SAMPLED (combined ESS 648 < 1000) |
| mean_median | 1.0099 | [228, 264, 291] | 783 | 59 | UNDER-SAMPLED (combined ESS 783 < 1000) |
| declination | 1.0076 | [234, 243, 165] | 643 | 81 | UNDER-SAMPLED (combined ESS 643 < 1000) |
| seats_at_50_50 | 1.0014 | [173, 251, 224] | 647 | 78 | UNDER-SAMPLED (combined ESS 647 < 1000) |

## Overall verdict

**NOT CONVERGED.** Max R-hat = 1.0099 (threshold 1.05), or one or more metrics have combined ESS < 1000. The paper's S5.4 percentile claims cannot rest on this ensemble alone; either extend each chain (more ReCom proposals per chain — ESS scales roughly linearly with chain length) or add additional seeds. A practical escalation is to increase `--steps` by 3-10x and re-run.


## Threshold rationale

- **R-hat < 1.01:** strict Gelman-Rubin criterion (Gelman et al. 2013, *BDA3* ch. 11). Indicates within-chain and between-chain variability are statistically indistinguishable.
- **R-hat < 1.05:** widely-used soft threshold (e.g. PyMC, Stan default warning at 1.05). We treat this as the minimum acceptable criterion for publication-grade claims.
- **R-hat >= 1.1:** chains have not mixed; reported percentiles are not reliable.
- **Combined ESS >= 1000:** gives Monte Carlo standard error on any metric of roughly sigma / sqrt(ESS), so a 5th-percentile estimate has approx ±1-2 percentile-point noise. Below 1000, percentile claims are under-powered.


## Implications for paper S5.4

The paper's S5.4 percentile claims should be held until the ensemble converges. Either rerun with larger `--steps` (recommended: 3x current) or flag the percentile claims explicitly as preliminary pending convergence.


## Reproducibility

```bash
python analysis/scripts/simulation_multichain_ensemble.py --seeds 42,101,2024 --steps 150000 --burnin 0.1
```

Independent seeds ensure a peer reviewer can rerun with any permutation of seeds and, if the ensemble has converged, obtain statistically indistinguishable percentile ranks.
