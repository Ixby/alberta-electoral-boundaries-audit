# Code Review Log — Alberta Audit Scripts
**Date:** 2026-05-08  
**Reviewer:** Claude (Sonnet 4.6)  
**Scope:** All load-bearing analytical scripts, cross-checked against test suite

---

## SEVERITY LEGEND
- **[CRITICAL]** — Silent wrong result, data integrity failure, or reproducibility break
- **[HIGH]** — Stale/wrong documentation that could mislead re-runs; missing guard that breaks on edge case
- **[MEDIUM]** — Code quality or robustness issue; won't silently corrupt results but may cause failure
- **[LOW]** — Cosmetic, duplicate import, harmless redundancy

---

## 1. mcmc_ensemble_canonical.py — Wrong seed salt (CRITICAL)

**File:** `analysis/scripts/mcmc_ensemble_canonical.py`, line 171  
**Code:** `get_canonical_seed("mcmc_ensemble_250k")`  
**Issue:** This is the _canonical_ 100k re-run script, but it uses the salt `"mcmc_ensemble_250k"` — the old DPG ensemble's identifier. The salt is supposed to uniquely identify the run. If anyone ever re-runs with `"mcmc_ensemble_canonical"` as the salt (the natural choice), the ensemble will not be reproducible from the pre-registered seed derivation. Reviewers checking reproducibility will compute a different seed than what was used.  
**Risk:** Reproducibility failure. The actual ensemble was run with this salt, so results are correct *as produced*, but re-production documentation is wrong.  
**Fix:** Either document that the canonical 100k ensemble intentionally uses `"mcmc_ensemble_250k"` salt (for historical continuity), or update the salt and re-note the seed.

---

## 2. szat_validate.py — Stale docstring says wrong thing about szat.py (HIGH)

**File:** `analysis/scripts/szat_validate.py`, lines 15–22  
**Issue:** Docstring says: *"szat.py uses an additive-delta approximation for the bootstrap null."* This is false. `szat.py` was updated to use the **full-recompute** procedure (the pre-registered null). The validate script's "Check 2" still tests additive-approximation vs full-recompute, which is a useful comparison, but the framing in the module docstring now falsely describes the production method.  
**Risk:** Anyone reading the validate script will misunderstand what szat.py does. The description of the pre-registered null procedure is buried in the run comments, not the docstring.  
**Fix:** Update the docstring to say szat.py uses full-recompute (Bernoulli 0.5, pre-registered); Check 2 compares approximation vs full-recompute for fidelity verification.

---

## 3. szat_validate.py — Fallback seed differs from szat.py fallback (HIGH)

**File:** `analysis/scripts/szat_validate.py`, line 143  
**Code:** `seed = 23687475` (fallback)  
**szat.py docstring says:** "Fallback seed 20260506 used if drand_seed is unavailable"  
**szat.py code:** `from drand_seed import get_canonical_seed  # fails loudly if missing — no fallback`  
**Issue:** Three-way inconsistency: (a) szat.py docstring says fallback=20260506, (b) szat.py code has no fallback at all, (c) szat_validate.py has fallback=23687475. If drand_seed is unavailable, szat.py hard-fails (correct behavior), but szat_validate.py silently uses a different seed that was never registered or documented.  
**Risk:** If drand_seed ever fails for szat_validate.py, its bootstrap comparison uses an unregistered seed, making the fidelity comparison meaningless.  
**Fix:** Align szat.py docstring with code (no fallback), and align szat_validate.py to either fail loudly or use the same seed.

---

## 4. mcmc_ensemble.py — score_exogenous_map default id_col is "name_2026" (HIGH)

**File:** `analysis/scripts/mcmc_ensemble.py`, line 292  
**Code:** `def score_exogenous_map(va, proposed_gpkg, id_col: str = "name_2026") -> dict:`  
**Issue:** The canonical shapefiles use `"EDName2025"` as the district ID column. The default is the DPG-derived column name. Any script that calls `score_exogenous_map()` without specifying `id_col` on canonical shapefiles will get a `KeyError` from the sjoin (column not present).  
**Risk:** Silent failure mode for callers — they'd get a KeyError at runtime, not a meaningful error message. Any new script or test that doesn't specify `id_col` will break against canonical files.  
**Fix:** Change default to `"EDName2025"` (canonical convention), or add a check that the column exists with a clear error message.

---

## 5. mcmc_ensemble.py — seat_results() empty-case dict missing ucp_vote_share (MEDIUM)

**File:** `analysis/scripts/mcmc_ensemble.py`, lines 158–165  
**Issue:** When `n == 0` (all-zero vote districts), the returned dict contains `efficiency_gap`, `mean_median`, `declination`, `seats_at_50_50`, `ucp_seats`, `n_districts` — but **not** `ucp_vote_share`. The non-empty return (line 218) includes `ucp_vote_share`.  
**Risk:** Any code that accesses `result["ucp_vote_share"]` on a zero-vote scenario gets `KeyError`. This won't happen in production (real districts have votes) but could cause confusing failures in tests or edge-case diagnostics.  
**Fix:** Add `"ucp_vote_share": float("nan")` to the empty-case return dict.

---

## 6. szat.py — assertion on swing zone count is fragile (MEDIUM)

**File:** `analysis/scripts/szat.py`, lines 250–253  
**Code:** `assert n_swing == 2108, ...`  
**Issue:** This `AssertionError` fires if the canonical shapefiles are updated or VA assignment changes. `AssertionError` is the wrong exception type for a data validation check — it can be silenced by `-O` flag. Also hardcodes an empirical count derived from a specific shapefile version.  
**Risk:** If shapefile is updated (e.g., Elections Alberta issues a correction), the script hard-fails with an opaque assertion. The expected count should be documented as tied to a specific shapefile version/hash.  
**Fix:** Replace `assert` with `if n_swing != 2108: raise ValueError(...)`. Consider also logging the shapefile mod dates or hashes at script start.

---

## 7. historical_eg_baseline.py — 2026 EG comparison values hardcoded (MEDIUM)

**File:** `analysis/scripts/historical_eg_baseline.py`, lines 593–594  
**Code:**
```python
EG_2026_MAJORITY_PCT = -0.40
EG_2026_MINORITY_PCT = -1.81
```
**Issue:** These values are hardcoded module-level constants, not read from `packing_cracking_analysis.py` output. If the packing/cracking script is re-run with different parameters, the historical baseline comparison silently uses stale values. The comment notes an older version used -1.3% and -2.7%.  
**Risk:** Historical baseline report will compare against wrong 2026 reference values without warning.  
**Fix:** Read from `data/packing_cracking_results.json` (or equivalent output) at runtime. If that file doesn't exist, fail with a clear error.

---

## 8. historical_eg_baseline.py — write_report() hardcodes "2019 enacted baseline: -2.64%" (MEDIUM)

**File:** `analysis/scripts/historical_eg_baseline.py`, line 634  
**Code:** `print(f"  2019 enacted baseline:   -2.64%  (reference)")`  
**Issue:** The 2023 EG is re-computed by the script (`results[2]['code_eg_pct']`), but the 2019 enacted baseline comparison is printed as a literal `-2.64%` instead of reading from data. This could be wrong if the source data changes.  
**Risk:** Misleading printed output if 2023 EG recomputation changes.  
**Fix:** This value should come from the `results` list (2023 EG = enacted-map baseline), or be computed separately.

---

## 9. joint_outlier_score_canonical.py — drain_minority_p hardcoded (MEDIUM)

**File:** `analysis/scripts/joint_outlier_score_canonical.py`, line 194  
**Code:** `drain_minority_p = 0.1342`  
**Issue:** Channel 3 (neighbour-drain) p-value is injected as a literal, not read from the neighbour drain output file. If the drain analysis is re-run, this value won't update.  
**Risk:** The Fisher combination correctly excludes this channel, so the primary result (Fisher p) is not affected. But the MD report will show stale drain numbers.  
**Fix:** Read from `analysis/reports/neighbour_drain_analysis.json` (or equivalent), failing with a clear error if missing.

---

## 10. joint_outlier_score_canonical.py — structural metrics hardcoded (MEDIUM)

**File:** `analysis/scripts/joint_outlier_score_canonical.py`, lines 213–240  
**Hardcoded values:** `minority_pct=14.5`, `majority_pct=71.0`, `minority_mad=4707`, `majority_mad=3180`, `minority_pct_below_0_30=34.8`, `majority_pct_below_0_30=13.5`  
**Issue:** These values were derived from earlier analysis runs and are now frozen in the script. They appear in the JSON output as "structural_pending" notes, but any re-run will print stale numbers.  
**Risk:** Low — the MD and JSON outputs correctly flag these as "pending" with no p-values. But a careless reader might take the numbers as current.  
**Fix:** Either read from ensemble output CSV (the values are computed there), or add a comment clearly marking them as frozen from a specific run date.

---

## 11. submission_search.py — pos_counts computed but never written to disk (MEDIUM)

**File:** `analysis/scripts/submission_search.py`, line 457 (`write_outputs`)  
**Issue:** `pos_counts` (the position breakdown by configuration — how many submissions "support" vs "oppose" each keyword configuration) is computed in `search_submissions()` and passed to `write_outputs()`, but `write_outputs()` never uses it. The per-configuration position breakdown (which is the actual research finding — "how many submissions oppose the Airdrie 4-way split?") is only logged to the search log, never persisted in the CSV or as a separate output.  
**Risk:** Analysis gap. The CSV only records per-submission position on first hit; the aggregate "X% oppose, Y% support the RMH-Banff combination" is computed but thrown away.  
**Fix:** Add a `position_counts.csv` output, or add rows to the summary at the bottom of the main CSV.

---

## 12. submission_search.py — olds_three_hills_didsbury pattern tests missing (MEDIUM)

**File:** `analysis/scripts/submission_search.py`, lines 307–309  
**Pattern:**
```python
"olds_three_hills_didsbury": [
    re.compile(r"(olds|didsbury|three\s+hills)[\s\S]{0,300}airdrie", re.I),
    re.compile(r"airdrie[\s\S]{0,300}(olds|didsbury|three\s+hills)", re.I),
],
```
**Issue:** These patterns detect "Olds/Didsbury/Three Hills near Airdrie" — not "Olds-Three Hills-Didsbury as a combined riding". A submission about Airdrie that mentions driving through Olds would trigger this. The patterns don't capture the actual configuration being tested (the minority proposal to combine Olds, Three Hills, and Didsbury as a single rural-ring riding around Airdrie).  
**Related:** No tests exist for this configuration in `test_submission_search.py`. The `TestOldsThreeHillsDidsbury` class is absent.  
**Risk:** False positives in the Olds-Three Hills-Didsbury count; finding could be overstated or misattributed.  
**Fix:** Add patterns that specifically look for Olds AND Three Hills AND Didsbury together (or the riding name), and add fire/no-fire tests.

---

## 13. szat.py and szat_validate.py — duplicate imports (LOW)

**szat.py:** `import sys` appears at lines 49 and 59; `from pathlib import Path` at lines 50 and 62.  
**szat_validate.py:** `import json`, `import sys`, `from pathlib import Path` appear at lines 36–38 (already imported above).  
**Impact:** None functional. Clean up for readability.

---

## 14. canadian_base_rate_compute.py — Alberta 2026 anchor uses literal 0.51 (LOW)

**File:** `analysis/scripts/canadian_base_rate_compute.py`, line 457  
**Code:** `alberta = 0.51`  
**Issue:** The `summarise()` function overrides the formula-computed proxy (1/89*100*0.455 = 0.5112 pp) with the audit's directly-measured EG asymmetry (0.51 pp). This is documented and intentional ("anchor ≡ audit headline"), but it means the anchor in the percentile-rank comparison uses a slightly different value than `Cycle.eg_asymmetry_proxy_pp` would produce for the same row. The discrepancy is 0.001 pp — negligible analytically but worth noting.  
**Risk:** None analytical.

---

## 15. historical_eg_baseline.py — label-based year filtering is fragile (LOW)

**File:** `analysis/scripts/historical_eg_baseline.py`, line 435  
**Code:** `normal = [r for r in results if "2015" not in r["label"]]`  
**Issue:** Filters out the 2015 result by string-matching "2015" in the label. Works with current labels (`"2015 (pre-2017 map, 87 EDs)"`), but would silently include 2015 if the label format changes, or silently exclude a future year like "2015-redux".  
**Fix:** Use an explicit list of "normal" election years, or add a `is_anomalous` field to the result dict.

---

## Cross-script consistency checks

| Check | Result |
|---|---|
| EG sign convention (positive = NDP structural disadvantage) | **CONSISTENT** across szat.py, mcmc_ensemble.py, historical_eg_baseline.py, joint_outlier_score_canonical.py |
| Wasted vote formula (winner surplus vs loser all votes) | **CONSISTENT** — szat.py and szat_validate.py use identical helpers |
| Threshold: szat.py uses total/2 (continuous) | **INTENTIONAL DIFFERENCE** from historical_eg_baseline.py (total//2+1, integer) — documented and tested |
| drand CANONICAL_ROUND = 5500000 | **CONSISTENT** — drand_seed.py, test asserts it |
| N_EFF_CONSERVATIVE = 224 | **CONSISTENT** — joint_outlier_score_canonical.py and test |
| 0.455 deflator in Cycle | **CONSISTENT** — canadian_base_rate_compute.py and test |
| id_col="EDName2025" convention | **CONSISTENT** where called (mcmc_ensemble_canonical.py line 217, test) — BUT default in mcmc_ensemble.py is wrong (see issue 4) |
| Fisher channel independence assumption | **DOCUMENTED** — caveats list in JSON output explicitly flags this |
| Bootstrap null: Bernoulli 0.5 full-recompute | **szat.py uses this; szat_validate.py compares it against additive approximation** |

---

## Tests that don't exist but should

1. `TestOldsThreeHillsDidsbury` — pattern fire/no-fire for the olds_three_hills_didsbury configuration
2. `test_seat_results_empty_case_has_ucp_vote_share` — verifies the zero-case return dict matches the non-empty key set
3. `test_score_exogenous_map_with_wrong_id_col` — ensures a useful error is raised, not a silent wrong result
4. `test_szat_validate_attribution_integrity` — integration test (requires CSV; lower priority)

---

## Summary by script

| Script | Issues | Highest severity |
|---|---|---|
| mcmc_ensemble_canonical.py | Seed salt stale | CRITICAL |
| szat_validate.py | Stale docstring, fallback seed mismatch | HIGH |
| mcmc_ensemble.py | Wrong default id_col, missing ucp_vote_share in empty case | HIGH |
| szat.py | assert vs ValueError, duplicate imports | MEDIUM |
| historical_eg_baseline.py | Hardcoded 2026 EG values, fragile label filter | MEDIUM |
| joint_outlier_score_canonical.py | Hardcoded drain p, hardcoded structural values | MEDIUM |
| submission_search.py | pos_counts not persisted, missing pattern tests | MEDIUM |
| canadian_base_rate_compute.py | Trivial anchor discrepancy | LOW |
| drand_seed.py | Clean | — |
| historical_eg_baseline.py | Clean | — |

---

*Generated by code review session 2026-05-08. Re-run review after addressing HIGH/CRITICAL items.*
