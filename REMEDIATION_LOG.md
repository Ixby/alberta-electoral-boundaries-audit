# Remediation Execution Log

**Started:** 2026-05-09  
**Plan:** transient-growing-stearns.md  
**Purpose:** Audit trail for all challenges, validation failures, and plan deviations
encountered during Safety Track and Hygiene Track execution.

Format: log before fixing. Do not resolve a problem without an entry here first.

---

<!-- Append new entries below this line in reverse-chronological order (newest first) -->

## [2026-05-09] Step 1.1 — EG threshold formulas differ across six implementations

**Observed:** Three distinct threshold formulas in use across the six files the plan proposed to unify:

| Implementation | Threshold | Interface | Winner condition |
|---|---|---|---|
| `szat.py` | `total / 2` | `pd.DataFrame` | `ndp >= ucp` |
| `szat_validate.py` | `total / 2` | `pd.DataFrame` | `ndp >= ucp` |
| `mcmc_ensemble.py` (inline) | `total / 2` (vectorised) | `np.ndarray` | `ucp > ndp` (strict) |
| `overlap_zone_diagnostic.py` | `total / 2.0 + 0.5` | `pd.DataFrame` | `ndp >= ucp` |
| `chen_rodden_alberta.py` | `total // 2 + 1` | `List[Dict]` | `ndp > ucp` (strict) |
| `historical_eg_baseline.py` | `total // 2 + 1` | `List[Dict]` + `actual_winner` field | `actual_winner` (not vote comparison) |

The plan's proposed eg_utils sketch used `threshold = total / 2 + 1`, which matches none of the existing implementations.

**Impact:** The plan assumed one extractable formula. In reality:
- `szat.py` + `szat_validate.py` are confirmed near-verbatim copies (same continuous formula, same interface) — this is the real DRY violation.
- `chen_rodden_alberta.py` and `historical_eg_baseline.py` use the integer majority threshold for actual election results with integer votes — a defensible and different choice.
- `mcmc_ensemble.py` uses a vectorised implementation incompatible with a scalar utility function.
- `historical_eg_baseline.py` requires an `actual_winner` field and takes `List[Dict]`, making it architecturally incompatible with a shared DataFrame-based function.

**Action taken:** Narrow extraction scope:
1. `eg_utils._ed_waste` uses `threshold = total / 2` (continuous) matching szat.py/szat_validate.py exactly.
2. `szat.py` and `szat_validate.py` import from eg_utils — the confirmed copy-paste pair.
3. `overlap_zone_diagnostic.py`, `chen_rodden_alberta.py`, `historical_eg_baseline.py`, `mcmc_ensemble.py` retain their local implementations with a header comment: `# Threshold variant differs from eg_utils._ed_waste — see REMEDIATION_LOG.md 2026-05-09`.
4. Plan's "remove from 6 files" becomes "remove from 2 files" (szat.py, szat_validate.py).

**Outcome:** Resolved. The actual DRY risk (the confirmed copy-paste pair) is fixed. The remaining files use legitimately different threshold variants for defensible reasons. Pre-validation snapshot scope reduced to szat.py and szat_validate.py — no cross-implementation comparison needed since they are not running the same formula.
