# Multi-chain MCMC convergence summary

**Script:** `analysis/v0_1_mcmc_multichain_ensemble.py`

**Seeds:** [42, 101, 2024]  

**Chains:** 3  

**Steps per chain:** 50,000  

**Burn-in fraction:** 10%  

**Common thinning factor (pooled CSV):** 79  

**Total runtime:** 1487s (24.8 min)


## Per-metric diagnostics

| Metric | R-hat (split) | Per-chain ESS | Combined ESS | Thin | Verdict |
|---|---:|---|---:|---:|---|
| efficiency_gap | 1.0295 | [80, 96, 99] | 275 | 56 | UNDER-SAMPLED (combined ESS 275 < 1000) |
| mean_median | 1.0177 | [78, 115, 105] | 297 | 57 | UNDER-SAMPLED (combined ESS 297 < 1000) |
| declination | 1.0348 | [75, 102, 95] | 272 | 59 | UNDER-SAMPLED (combined ESS 272 < 1000) |
| seats_at_50_50 | 1.0293 | [57, 77, 83] | 217 | 79 | UNDER-SAMPLED (combined ESS 217 < 1000) |

## Overall verdict

**NOT CONVERGED.** Max R-hat = 1.0348 (threshold 1.05), or one or more metrics have combined ESS < 1000. The paper's S5.4 percentile claims cannot rest on this ensemble alone; either extend each chain (more ReCom proposals per chain — ESS scales roughly linearly with chain length) or add additional seeds. A practical escalation is to increase `--steps` by 3-10x and re-run.


## Threshold rationale

- **R-hat < 1.01:** strict Gelman-Rubin criterion (Gelman et al. 2013, *BDA3* ch. 11). Indicates within-chain and between-chain variability are statistically indistinguishable.
- **R-hat < 1.05:** widely-used soft threshold (e.g. PyMC, Stan default warning at 1.05). We treat this as the minimum acceptable criterion for publication-grade claims.
- **R-hat >= 1.1:** chains have not mixed; reported percentiles are not reliable.
- **Combined ESS >= 1000:** gives Monte Carlo standard error on any metric of roughly sigma / sqrt(ESS), so a 5th-percentile estimate has approx ±1-2 percentile-point noise. Below 1000, percentile claims are under-powered.


## Implications for paper S5.4

The paper's S5.4 percentile claims should be held until the ensemble converges. Either rerun with larger `--steps` (recommended: 3x current) or flag the percentile claims explicitly as preliminary pending convergence.


## Reproducibility

```bash
python analysis/v0_1_mcmc_multichain_ensemble.py --seeds 42,101,2024 --steps 50000 --burnin 0.1
```

Independent seeds ensure a peer reviewer can rerun with any permutation of seeds and, if the ensemble has converged, obtain statistically indistinguishable percentile ranks.
