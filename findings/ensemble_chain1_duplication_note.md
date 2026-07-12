---
title: Canonical ensemble chain 1 — 17,500 duplicated samples (disclosure, and the clean rerun that superseded it)
date: 2026-07-09; resolved 2026-07-12
status: disclosed 2026-07-09; ensemble scrapped and rerun clean 2026-07-12; canonical headline figures superseded
---

> **Backward:**
> - `data/simulation_checkpoints_canonical/chain1_samples.csv` — the affected chain CSV (since overwritten by the 2026-07-12 rerun)
> - `data/outputs/simulated_ensemble_raw_samples_canonical.csv` — pooled ensemble containing the duplicates (since regenerated)
> - `analysis/scripts/mcmc_ensemble_canonical.py` — `_run_chain_chunked` resume path (root cause; hardened same day) and the chain-indexing clobber defect found 2026-07-12 (see Resolution below)
>
> **Forward:**
> - `reports/academic/report_academic.md` DOCUMENTED CORRECTIONS C9 (original disclosure) and C10 (supersedes C9 — the rerun)
> - `analysis/methodology/test_suite_mutation_audit.md` — the audit that led here

# Chain 1 duplication — what was found, how, and what happened next

**This note originally disclosed a duplication defect while retaining the affected run's published figures (see "Sensitivity analysis at the time," below) — that disposition no longer holds.** On 2026-07-12 the canonical ensemble was scrapped and rerun clean after a second, independent defect was found in the same code path. See "Resolution: the ensemble was scrapped and rerun," below, for what changed and why. The discovery narrative that follows is retained verbatim as the historical record.

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

## Sensitivity analysis at the time (superseded — see Resolution, below)

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

At the time, no published flag, threshold, count, or conclusion changed.
Removing the duplicates made the headline marginally stronger (the duplicated
block lay in the distribution's interior), and none of the 66
seats@50/50-reaching plans fell inside the duplicated region. On that basis
the published figures were retained as-is, and this note plus DOCUMENTED
CORRECTIONS C9 disclosed the duplication rather than silently regenerating
history. **That disposition held only until a second, independent defect
turned up in the same code path — see below.**

## Resolution: the ensemble was scrapped and rerun (2026-07-12)

While hardening `_run_chain_chunked` against the resume defect (see
Remediation, below), a second, unrelated defect was found in the same script:
the multi-chain checkpoint writer indexed output files by loop position
(`chain{i}_samples.csv`) rather than by the `--first-chain-idx`-adjusted chain
number, so a partial or resumed multi-chain run could silently clobber one
chain's samples with another's. Retaining a run known to carry two
independent, uninvestigated failure modes in its own generation code — even
one with a demonstrated-negligible sensitivity — was judged the wrong call
once the second defect surfaced. Rather than write a second sensitivity
footnote, the canonical ensemble was discarded and regenerated from scratch.

**The rerun:** 4 fresh chains, 1,010,000 plans total, unchanged base seed,
identical OSF-committed methodology (no scoring or methodology change — this
is a clean re-execution of the same pre-registered procedure). Ran
2026-07-12, 05:02–10:01 (4h59m), via a detached wrapper outside the
interactive session (`.temp/ensemble_rerun_wrapper.py`, not committed —
session infrastructure).

**Verification:** the same duplicated-block replay probe that found the
original defect was rerun against all four new chain CSVs. No duplicated
blocks were found in any chain:

```python
import pandas as pd, numpy as np
for i in range(4):
    eg = pd.read_csv(f"data/simulation_checkpoints_canonical/chain{i}_samples.csv",
                      usecols=["efficiency_gap"])['efficiency_gap'].values
    chunk = 2500
    seen = {}
    for s in range(0, len(eg) - chunk, chunk):
        block = eg[s:s+chunk].tobytes()
        assert block not in seen, f"chain{i}: duplicate at {s}"
        seen[block] = s
```

Convergence improved over the C9-era run: Gelman-Rubin R-hat (full 1.01M run,
4 chains) 1.00113–1.00388 → **1.00011–1.00205**.

**Outcome — the headline figures changed, and moved stronger, not weaker:**

| Statistic | C9-era (duplicated) run | Clean rerun (2026-07-12) |
|---|---|---|
| Minority Mahalanobis D² | 32.6692 | 33.6385 |
| Ch1 parametric p (χ²₄) | 1.40×10⁻⁶ | 8.80×10⁻⁷ |
| Bonferroni dependence-robust bound | p ≤ 2.80×10⁻⁶ | p ≤ 1.76×10⁻⁶ |
| Verbal form | about one in 357,000 | about one in 568,000 |
| n_eff-adjusted (Hotelling T²) p | 1.73×10⁻⁶ | 1.11×10⁻⁶ |
| Dependence-honest rule-of-three bound | 6.52×10⁻⁴ (n_eff 4,599) | 6.86×10⁻⁴ (n_eff 4,372) |

Every canonical-ensemble-derived number cited in either report or the viewer
site was updated to the clean rerun's values on 2026-07-12. See DOCUMENTED
CORRECTIONS **C10** in `reports/academic/report_academic.md` (supersedes C9).

## Remediation

`_run_chain_chunked` now **fails loudly on resume** (raises with instructions)
instead of silently restarting from the 2019 seed with a rewound RNG — silent
resume is exactly how the duplication happened. The chain-indexing clobber
defect found 2026-07-12 was fixed the same day (checkpoint paths now index by
the adjusted chain number, not loop position). Full partition checkpointing
(persist each chunk's final assignment; reload on resume) remains queued
before the November 2026 confirmatory run (OSF qsgy8), which must not inherit
either failure mode.
