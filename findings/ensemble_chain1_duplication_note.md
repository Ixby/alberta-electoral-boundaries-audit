---
title: Canonical ensemble chain 1 — 17,500 duplicated samples (disclosure + sensitivity)
date: 2026-07-09
status: disclosed; no published number changes; resume path hardened
---

> **Backward:**
> - `data/simulation_checkpoints_canonical/chain1_samples.csv` — the affected chain CSV
> - `data/outputs/simulated_ensemble_raw_samples_canonical.csv` — pooled ensemble containing the duplicates
> - `analysis/scripts/mcmc_ensemble_canonical.py` — `_run_chain_chunked` resume path (root cause; hardened same day)
>
> **Forward:**
> - `reports/academic/report_academic.md` DOCUMENTED CORRECTIONS C9
> - `analysis/methodology/test_suite_mutation_audit.md` — the audit that led here

# Chain 1 duplication — what was found, how, and what it does (and does not) change

## Discovery path

A 2026-07-09 mutation audit of the test suite exposed that the chunked-MCMC
state-persistence test could not detect its target regression (degenerate
2-district fixture — see `analysis/methodology/test_suite_mutation_audit.md`).
Reading the production runner (`mcmc_ensemble_canonical.py::_run_chain_chunked`)
during that audit revealed a latent resume-path defect: on crash-resume,
`current_state` is rebuilt from the 2019 seed and the RNG is re-seeded from
position zero, rather than restoring the interrupted chain's state. A replay
probe over the committed chain CSVs was run to check whether any resume had
actually occurred during the canonical run.

## Finding

Chain 1 of the canonical ensemble contains one duplicated block:

- rows **45,000–62,499** are byte-identical to rows **25,000–42,499**
  (17,500 consecutive rows; chunk labels 9–12 vs 5–8);
- the block lies entirely inside the original 250,000-plan-era segment
  (first 62,500 rows per chain), consistent with an interruption and resume
  during the initial run, before the extension to 4 × 252,500;
- chains 0, 2, 3 show no duplicated chunk-start signatures;
- 17,500 / 1,010,000 = **1.73%** of the pooled ensemble is duplicated.

Reproduction (from repo root):

```python
import pandas as pd, numpy as np
eg = pd.read_csv("data/simulation_checkpoints_canonical/chain1_samples.csv",
                 usecols=["efficiency_gap"])['efficiency_gap'].values
assert np.array_equal(eg[45000:62500], eg[25000:42500])
```

## Sensitivity: every headline statistic recomputed without the duplicates

Pooled ensemble with the 17,500 duplicated chain-1 rows removed (n = 992,500):

| Statistic | Published (1,010,000) | Deduplicated (992,500) |
|---|---|---|
| Minority Mahalanobis D² | 32.670 | 32.911 |
| Ch1 parametric p (χ²₄) | 1.40×10⁻⁶ | 1.25×10⁻⁶ |
| Plans at/beyond minority D² | 0 | 0 |
| Plans reaching minority seats@50/50 | 66 | 66 |
| Ensemble EG p95 (the ~4.1% line) | 4.100% | 4.096% |
| Minority EG percentile | p94.39 | p94.46 |
| Minority mean-median percentile | p99.98 | p99.98 |
| Minority seats@50/50 percentile | p99.993 | p99.993 |

**No published flag, threshold, count, or conclusion changes.** Removing the
duplicates makes the headline marginally stronger (the duplicated block lies
in the distribution's interior), and none of the 66 seats@50/50-reaching plans
falls inside the duplicated region. The published figures are retained as-is;
this note and DOCUMENTED CORRECTIONS C9 disclose the duplication rather than
silently regenerating history.

## Remediation

`_run_chain_chunked` now **fails loudly on resume** (raises with instructions)
instead of silently restarting from the 2019 seed with a rewound RNG — silent
resume is exactly how the duplication happened. Full partition checkpointing
(persist each chunk's final assignment; reload on resume) is the correct fix
and is queued before the November 2026 confirmatory run (OSF qsgy8), which
must not inherit this failure mode.
