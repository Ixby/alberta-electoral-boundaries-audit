# Adversarial Audit Report — Alberta Boundary Analysis

**Date:** 2026-05-08  
**Method:** 5 parallel adversarial subagents + author verification of claimed findings  
**Scope:** All scripts in `analysis/scripts/`, all tests in `tests/`

Findings are graded CONFIRMED (verified by reading code), PLAUSIBLE (reasonable concern, not disproved), or REJECTED (agent hallucination or misreading).

---

## Fixed in This Session

### F1 — CONFIRMED — Negation blindness in position classifier (HIGH)
**File:** `submission_search.py:344`

`OPPOSE_WORDS` covered `do not support` and `don't support` but NOT `cannot support`, `can't support`, `will not support`, `won't support`, `would not support`, `wouldn't support`. Any of these phrases would match `support` in `SUPPORT_WORDS` and zero times in `OPPOSE_WORDS`, classifying as `"supporting"`.

**Fix applied:** Added six missing negation patterns to `OPPOSE_WORDS`.  
**Tests added:** `test_classify_cannot_support_is_opposing`, `test_classify_wont_support_is_opposing`, `test_classify_will_not_support_is_opposing`

---

### F2 — CONFIRMED — `problem(atic)?` in OPPOSE_WORDS causes false positives (MEDIUM)
**File:** `submission_search.py:344`

`problem(atic)?` matched any mention of "problem" or "problematic" regardless of context. Neutral geographic descriptions ("the problematic terrain", "the problem of road access") would fire OPPOSE_WORDS and shift classification toward "opposing". Removes legitimate neutral submissions from the neutral bucket.

**Fix applied:** Removed `problem(atic)?` from `OPPOSE_WORDS`.  
**Test added:** `test_classify_problematic_terrain_is_neutral`

---

### F3 — CONFIRMED — Centroid method inconsistency between szat.py and mcmc_ensemble.py (HIGH)
**File:** `szat.py:183` vs `mcmc_ensemble.py:306`

`szat.py` used `va_gdf.geometry.centroid` (true geometric centroid, can fall outside concave polygons). `mcmc_ensemble.py` used `centroids.geometry.representative_point()` (guaranteed interior point). For irregular VA polygons that straddle a boundary, the two methods can assign the VA to different EDs, producing different swing-zone counts and vote attribution between the two scripts.

**Fix applied:** `szat.py` now uses `representative_point()` to match `mcmc_ensemble.py`. The 2108 assertion comment updated to note the method change.

**Important:** The 2108 swing-VA count was pre-registered against canonical shapefiles. If `representative_point()` produces a different count than `centroid` did for these specific files, the `ValueError` will fire on the first run. The assertion value must then be updated to the new count and the change documented in the pre-registration amendment.

---

## Open Issues — Not Fixed (require methodological decisions or data runs)

### O1 — PLAUSIBLE — Fisher combination independence assumption (HIGH)
**File:** `joint_outlier_score_canonical.py:214–223`

Both Channel 1 (Mahalanobis multivariate outlier on MCMC ensemble) and Channel 2 (SZAT bootstrap) condition on the same 2023 Alberta vote vector. They are not measuring truly independent quantities. The comment in the code acknowledges this: `"# Fisher combination assumes Channel 1 and Channel 2 are independent — approximately true."` A hostile reviewer will challenge "approximately."

**What the code does right:** Ch1 asks "is the minority map an outlier in the space of geographically valid plans?" Ch2 asks "do the swing-zone boundary choices specifically drive EG?". These are different questions using the same underlying votes.

**Recommendation:** Add a short methodology note (in `analysis/methodology/`) computing the empirical Spearman correlation between Ch1 and Ch2 test statistics across the ensemble; if ρ < 0.3, the "approximately independent" claim is defensible. The note should appear in any publication.

---

### O2 — PLAUSIBLE — SZAT bootstrap null is unconstrained (MEDIUM-HIGH)
**File:** `szat.py:376–391`

The Bernoulli(0.5) null shuffles each swing VA independently with no regard for population balance, contiguity, or other Electoral Divisions Act constraints. Under a constrained null (only permutations satisfying Act requirements), the variance of the EG distribution would be narrower, and the observed SZAT score might be less extreme. This is the strongest methodological objection a hostile reviewer can raise against Ch2.

**Counterargument in the audit's favour:** The swing zone is small (2108 of ~16,000 VAs). Most permutations preserve near-balance because the swing VAs were selected precisely because they straddle the boundary — swapping them back and forth changes boundary shape but rarely violates population constraints badly. This argument should be made explicitly in the methodology.

**Recommendation:** Add a sensitivity check in `szat_validate.py`: for a random sample of 500 bootstrap permutations, compute the population MAD of the resulting maps. If population MAD stays within ±2× the real-map MAD in >95% of permutations, the unconstrained null is empirically defensible for these specific shapefiles.

---

### O3 — PLAUSIBLE — N_EFF choice direction (corrected from agent error) (LOW)
**File:** `joint_outlier_score_canonical.py:65`

Agent claimed using N_EFF=224 (minimum of 224–326 range) was the *least* conservative choice. **This is wrong.** For the Hotelling T² formula used here, smaller n_eff → smaller F-statistic → larger p-value → harder to reach significance. N_EFF=224 IS the most conservative choice for this formula.

**Actual concern:** The convergence diagnostics that produced the 224–326 range are not visible in the code. The value 224 is hardcoded with a comment but no direct link to the diagnostic output file. If the diagnostics are re-run, the code must be manually updated. Recommendation: add `N_EFF_SOURCE = DATA / "simulation_convergence_diagnostics_canonical.json"` and a startup check that reads n_eff from that file rather than hardcoding.

---

### O4 — PLAUSIBLE — Salt strings not directly verifiable from code (MEDIUM)
**Files:** `mcmc_ensemble_canonical.py:175`, `szat.py:348`

Salt `"mcmc_ensemble_250k"` (for 100k ensemble) and `"szat-bootstrap"` (for SZAT) are hardcoded strings. A hostile reviewer can ask: "prove these strings were chosen before the results were known." The code comments explain historical continuity but code comments are not an audit trail.

**What exists:** OSF pre-registrations qsgy8 and r3zm7 should contain these strings. The validation depends on whether those documents are public and link to specific salt values. If they do, the concern is resolved. If they don't explicitly name the salt strings, it's a gap.

**Recommendation:** Add to the methodology documentation a direct quote from each pre-registration document specifying the salt string. If the pre-registration predates the salt choice, file a dated amendment.

---

### O5 — PLAUSIBLE — drain_label_shuffle_null.json has no generating script in repo (MEDIUM)
**File:** `joint_outlier_score_canonical.py:193–211`

The DRAIN metric p-values are read from `data/drain_label_shuffle_null.json`. There is no visible script in `analysis/scripts/` that generates this file. If a reviewer does a fresh clone and the file is absent, the code falls back to hardcoded values (`p=0.1342`, `z=-2.915`, `z=-3.141`) with a warning. These fallback values are not independently verifiable.

**Recommendation:** Either (a) add the generating script to the repo with documentation, or (b) add `drain_label_shuffle_null.json` to the repository so the fallback is never needed in practice.

---

### O6 — PLAUSIBLE — Warrington declination formula not validated for Alberta (LOW)
**File:** `mcmc_ensemble.py:187–200`

The declination metric uses the Warrington (2018) formula designed for U.S. two-party races. Alberta's 2015 election had a three-party split (NDP/PC/Wildrose). The formula uses only two-party vote shares, but the 2015 analysis requires collapsing PC+Wildrose to a single "right bloc" vote. This aggregation assumption should be stated and defended.

---

### O7 — PLAUSIBLE — Sign convention comment in historical_eg_baseline.py is misleading (LOW)
**File:** `historical_eg_baseline.py:50–55`

The docstring says `"code_eg < 0 => negative = UCP (RBC) advantage"` but the formula `(NDP_wasted - RBC_wasted)` with a negative value means NDP wastes *fewer* votes. Under standard wasted-vote convention that means NDP is more efficient = NDP structural advantage. The comment appears backward.

The inline note references `analysis/methodology/sign_convention_resolution.md` for the "paper's raw-proportionality reading" explanation. That document should be the authoritative source; the docstring comment alone is unclear and should be updated to point readers directly to the methodology doc rather than attempting a one-line summary.

---

## Rejected Agent Claims (hallucinations or misreadings)

| Agent claim | Why rejected |
|-------------|-------------|
| `parent_ed_2019` wrong because built from `ED_NAME` | `ED_NAME` in the 2023 VA file correctly refers to the pre-2026 riding boundaries under which 2023 votes were cast. Naming it `parent_ed_2019` is correct. |
| N_EFF=224 is least conservative | Wrong direction of effect. Smaller n_eff → larger p-value → more conservative for Hotelling T². |
| Position counts misattributed across configurations | `pos_counts[pat_key][pos]` is updated per-configuration in the inner loop (line 427), not globally. Each config's counts are independent. |
| Multi-configuration position_on_mentioned bug | `position_on_mentioned` in the CSV row is the first-hit position (a documented known limitation, not a bug in the per-config counts). |
| test_synthetic_gerrymander.py is in the core test suite | That file has no pytest collection; it's a standalone script, not part of the 144-test suite. |
| CRS never validated in joint_outlier_score_canonical.py | That file reads a pre-scored CSV (not shapefiles), so CRS is not relevant to it. CRS validation belongs in the scripts that do spatial joins (szat.py and mcmc_ensemble.py — both have it). |

---

## Test Coverage Gaps Identified (not bugs, not fixed here)

1. No integration test that loads real ensemble CSV and verifies Ch1 p-value is in the right ballpark. Current tests only verify formula correctness on synthetic data.
2. No integration test for the SZAT bootstrap that runs against fixture shapefiles and checks the output p-value is < 0.05.
3. `historical_eg_baseline.py` has no test file. The main() function logic is untested.
4. The `write_outputs()` function in `submission_search.py` is untested (no fixture for the CSV output format).

These gaps do not invalidate the current test suite but represent areas where a malicious code change could go undetected.

---

## Summary by Severity

| Severity | Count | Action |
|----------|-------|--------|
| Fixed this session | 3 | Applied — see F1, F2, F3 |
| Open / methodological | 5 | See O1–O5 — require methodology notes or re-runs |
| Docstring/documentation | 2 | See O6, O7 — low risk, clarification needed |
| Rejected (agent error) | 6 | See rejection table above |
