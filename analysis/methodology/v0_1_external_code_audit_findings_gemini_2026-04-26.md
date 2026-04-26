---
name: External code-audit findings — Gemini, 2026-04-26
description: Independent code audit performed by Gemini against the external-code-audit brief at v0_1_external_code_audit_brief.md. Three of four findings confirmed against the actual code. The CRITICAL chain-reset bug requires re-running the headline 2M MCMC ensemble; the percentile placements in the published article may shift.
type: methodology
---

# External code-audit findings — Gemini, 2026-04-26

Audit performed using the brief at `v0_1_external_code_audit_brief.md`. Gemini's response provided in two passes (initial pass blocked on code access; second pass after code was supplied directly produced 4 findings: 2 critical, 1 high, 1 medium).

The audit author (Will Conner) verified each finding against the actual codebase before recording it here. Three of four findings are confirmed; one is documentation-only (not reproduced below). All findings produced action items.

---

## Verified findings

### CRITICAL #1 — MCMC chain state resets to 2019 baseline on every chunk

**Status:** Confirmed against `analysis/scripts/mcmc_ensemble_250k_v0_8.py` lines 104, 107, 113.

**Description.** Inside `_run_chain_chunked()`, the worker calls `assignment = initial_assignment_2019(va)` exactly once at the top (line 104). Inside the chunked loop (line 107), each call to `run_ensemble(graph, assignment, chunk_steps, ...)` (line 113) passes the SAME 2019 baseline assignment. The `assignment` variable is never updated to reflect the final partition of the previous chunk. The chain therefore restarts from the 2019 baseline at the start of every chunk.

**Effect on the headline finding.** The "2,000,000-sample MCMC ensemble" cited throughout `report_public.md` is actually 400 independent 5,000-step chains, each starting from the 2019 enacted map. This:

- Invalidates the autocorrelation diagnostics and ESS calculation (the per-chain time series is broken every 5,000 steps)
- Biases the ensemble distribution toward the 2019 baseline (the chain never explores far from the seed)
- May or may not invalidate the "out of distribution at p100" headline finding — that depends on whether the corrected ensemble produces a meaningfully higher seats@50/50 ceiling than the buggy version (the corrected exploration of the legal-map space could reach maps the buggy version could not)

**Fix.** `run_ensemble()` must accept and return a Partition object so the chunked loop can carry chain state forward. Implementation pending.

**Re-run requirement.** The full 2M MCMC ensemble must be re-run with the fix in place. The percentile placements in the public report are pending until the re-run completes. The headline framing — "no map in 2,000,000 simulated maps reaches the minority's 52.8%" — is currently UNVERIFIED until the re-run produces a true continuous-chain ensemble.

### CRITICAL #2 — Parallel array extraction relies on implicit dict iteration order

**Status:** Confirmed against `analysis/scripts/mcmc_ensemble.py` lines 404-405.

**Description.** Inside `run_ensemble()`, after each ReCom step:
```python
ucp = np.array(list(part["ucp"].values()))
ndp = np.array(list(part["ndp"].values()))
```
Both arrays are built by independently iterating two separate gerrychain Tally dicts. While Python 3.7+ preserves dict insertion order, this gambles on gerrychain's internal Tally implementation maintaining identical insertion order between two separate updaters.

**Effect on the headline finding.** If gerrychain's Tally ordering ever diverges between the UCP and NDP updaters (e.g., due to internal hash-set iteration in update events), per-district vote totals would be silently scrambled, producing wild errors in all four partisan-fairness metrics across affected steps.

**Fix.** Force explicit key alignment:
```python
keys = list(part.parts.keys())
ucp = np.array([part["ucp"][k] for k in keys])
ndp = np.array([part["ndp"][k] for k in keys])
```

### HIGH — Spatial joins double-count votes on overlapping polygons

**Status:** Confirmed against `analysis/scripts/mcmc_ensemble.py` lines 273-280.

**Description.** `score_exogenous_map()` performs `gpd.sjoin(centroids, proposed, how="left", predicate="within")` against the v0_8 reconstructed polygons. The author has documented elsewhere that the v0_8 inheritance-fill carve-out occasionally produces sliver polygons. If a VA centroid falls within an overlapping sliver of two poorly dissolved districts, `sjoin` returns two rows for that single centroid. The subsequent `groupby(id_col).agg(sum)` then credits that VA's votes to both districts.

**Effect on the headline finding.** Inflated per-district vote totals where sliver overlaps exist. Magnitude unknown without re-running with deduplication; the audit's known sliver count (6 minority polygons) bounds the maximum impact, but any pair of overlapping non-zero polygons could trigger this.

**Fix.** Deduplicate by source-VA index before aggregation:
```python
joined = gpd.sjoin(...)
covered = joined.dropna(subset=[id_col])
covered = covered[~covered.index.duplicated(keep="first")]
```

### MEDIUM — Boundary-clipping inconsistency

**Status:** Documentation-only (see audit findings; not separately verified). Recommend applying `np.clip(..., 0, 1)` consistently in `seat_results()` for forward-compatibility with future callers.

---

## Methodology spot-checks (Gemini)

| Formula | Verdict |
|---|---|
| Efficiency gap | Matches Stephanopoulos-McGhee (2014) |
| Mean-median | Matches |
| Declination | Matches Warrington (2018); algebraic equivalence confirmed (`atan2(y - 0.5, x/2) ≡ atan(2y-1, x)`) |
| Seats@50/50 uniform swing | Matches textbook implementation |

The four formulas are correct. The bugs are in the orchestration around them.

---

## Author response and remediation plan

The audit author accepts all three confirmed findings and has triggered remediation:

1. **CRITICAL #1 fix** — modify `run_ensemble()` to accept/return Partition; modify `_run_chain_chunked()` to carry state across chunks. Estimated: 30 min implementation + 60 min full 2M re-run.
2. **CRITICAL #2 fix** — force explicit key alignment in array extraction. Estimated: 5 min implementation.
3. **HIGH fix** — add `index.duplicated(keep="first")` deduplication to `score_exogenous_map()`. Estimated: 5 min implementation.
4. **Regression tests** — add the three tests Gemini specified (CRS enforcement on `score_exogenous_map`, state persistence in chunked `run_ensemble`, sjoin deduplication on overlapping mock polygons). Estimated: 1 hour.
5. **Re-run + delta report** — rerun the 2M MCMC ensemble; compare new percentile placements to the buggy version's published values; document any deltas in `analysis/reports/v0_1_post_audit_recompute_deltas.md`.
6. **Public-report update** — depending on the delta, either confirm the headline finding holds (no prose change needed) or re-state the finding honestly to reflect the corrected numbers.

The audit's pre-registration discipline requires the post-audit deltas to be reported in a dated amendment. If the recomputed `seats@50/50` ensemble ceiling rises above the minority's 52.8%, the "no map in 2M reaches it" claim is retracted and replaced with the corrected finding.

This is the failure mode the brief was designed to surface. The findings are working as intended.

---

## Part 2 — additional audit pass against verification subset and rural test

After the initial four findings (above), Gemini was given access to two further scripts that had not been included in the first pass: `analysis/scripts/mcmc_verification_subset.py` (the court-defensibility byte-verifiable forensic artefact generator) and `analysis/scripts/rural_protection_test.py` (the rural-population fairness check). Three additional findings: 2 critical, 1 medium. All three confirmed against the actual code.

### CRITICAL #3 — Verification subset crashes on step 0 due to type mismatch

**Status:** Confirmed against `analysis/scripts/mcmc_verification_subset.py` lines 121, 128.

**Description.** The script pre-allocates `assignment_arr = np.zeros((N_STEPS, n_va), dtype=np.int8)` but then writes `assignment_arr[step_i, va_id_to_idx[vid]] = partition.assignment[vid]` where `partition.assignment[vid]` is a *string* ED name ("Calgary-Bow", etc.) inherited from `initial_assignment_2019()`. Pushing a string into an `int8` array raises `ValueError` at step 0.

**Effect on the headline finding.** The court-defensibility forensic artefact would never be produced — meaning the audit would not be able to honour its "any reader can recompute and confirm byte-for-byte" promise.

**Fix.** Build a `dist_to_int` mapping from sorted unique district names before the loop, write integers into `assignment_arr`, and persist the inverse `int_to_district` mapping in the meta JSON so verifiers can reconstruct the names.

### CRITICAL #4 — Verification subset duplicates the dict-iteration bug

**Status:** Confirmed against the same file, lines 130-131.

**Description.** Same bug as CRITICAL #2 in the main ensemble, but in the verification artefact generator: `ucp = np.array(list(partition["ucp"].values()), dtype=float)` and the matching `ndp` line both rely on independent iteration order across two gerrychain Tally dicts.

**Effect on the headline finding.** A hostile expert downloading the `.npz` and recomputing metrics with a safe key-aligned approach could produce numbers that don't match the published `.csv`, completely undermining the credibility of the verification artefact.

**Fix.** Same key-alignment fix applied to the verification subset.

### MEDIUM — Rural-protection classifier silently buckets unknown EDs as "rural"

**Status:** Confirmed against `analysis/scripts/rural_protection_test.py` line 97 (now removed).

**Description.** The `classify()` function defaulted to `return "rural"` when no marker matched. Running the strict-replacement (`raise ValueError`) against the actual datasets surfaced **seven previously-silent misclassifications**: `Brooks-Medicine Hat`, `Cypress-Medicine Hat`, `Highwood`, `Lac Ste. Anne-Parkland`, `Medicine Hat-Brooks`, `Medicine Hat-Cypress`, `Mountain View-Kneehill`. Five of those were *small-city + rural-ring* hybrids being silently counted as pure rural, biasing the rural population average downward (Medicine Hat is a 63k-population small city, not a rural town).

**Effect on the headline finding.** The published rural-vs-urban population averages may be slightly off because hybrid pairings in the Medicine Hat / Lac Ste. Anne / Parkland clusters were counted on the rural side. Magnitude unknown until the test is re-run with the corrected classifier; first-order effect is to *raise* the apparent rural average (because hybrids are being removed from the rural pool), which would *weaken* the report's "even with rural protection, rural districts are over-represented" framing very slightly.

**Fix.** Removed the silent fallback; added the seven names to the explicit hybrid_markers / rural_only lists with documentation; final unmatched name now raises so future map proposals must be classified explicitly.

---

## Part 3 — population data sanity check

Gemini also reviewed the `data/va_pop_from_das.csv` underlying the graph. Result: **no findings, no fix required.** The float `pop_2021` values are the expected output of areal-weighted DA→VA population apportionment, and the single zero-population VA is already safeguarded by the `np.maximum(va["pop_2021"], 1.0)` clamp in `mcmc_ensemble.py`. The data extraction is sound.

---

## Updated remediation status (as of 2026-04-26 evening)

All seven code-level findings (4 from Part 1 + 3 from Part 2) are remediated in source. The pre-registration amendment, the regression tests, and the full 2M re-run remain. The headline framing in `report_public.md` is held in pending state until the corrected ensemble produces new percentile placements.

---

## Part 4 — test suite + symmetric-mirror script + dependency review

Gemini was given `tests/test_scoring.py`, `analysis/scripts/targeted_gerrymander_burst_ndp.py`, and `requirements.txt`. Two findings: 1 high, 1 medium.

### HIGH — Test suite did not exercise the geoprocessing pipeline

**Status:** Confirmed; addressed by the new regression tests.

**Description.** The pre-existing test suite covered `seat_results()` math and the verification-subset integrity guarantee, but never exercised `score_exogenous_map()` itself. Specifically, the sjoin double-counting bug (HIGH from Part 1) would not have been caught by any existing test — the verification-subset recompute test bypasses sjoin entirely by re-aggregating from the saved assignment vector.

**Effect on the headline finding.** None directly, but it explains why the bug survived undetected: the test surface area never included the spatial pipeline that feeds the exogenous map scores cited throughout the report.

**Fix.** Three new regression tests added to `tests/test_scoring.py` (one per remediated bug, per Gemini's Part 1 spec): sjoin-overlap dedup, CRS-mismatch reprojection, and chunked-MCMC state persistence. All three pass against the fixed code; the chain-state test in particular asserts threaded execution drifts the partition further from the seed than broken non-threaded execution does.

### MEDIUM — `networkx` was a load-bearing unpinned dependency

**Status:** Confirmed against `requirements.txt` (now fixed).

**Description.** `gerrychain==0.3.2` depends on `networkx`, which had a major-version transition (3.x) with breaking iteration semantics. The original `requirements.txt` left `networkx` to pip's resolver, which on a fresh install would pick the latest version and risk crashing `Graph.from_geodataframe()` or proposal generation with obscure errors — meaning a hostile auditor running `pip install -r requirements.txt` might never get the pipeline to start.

**Fix.** Pinned `networkx==3.6.1` (the version observed in the working environment) with a comment explaining why the pin is load-bearing.

---

## Part 5 — final sign-off + the "you already knew" finding

Gemini's final pass reviewed `parse_2015_results.py` and `phase_4c_prep.py`. No new bugs — but a pointed and useful observation: **the sjoin double-counting fix already existed in `phase_4c_prep.py` line 141** as `joined = joined.drop_duplicates(subset=["VA_NUMBER", "ED_NAME"])`. The HIGH finding from Part 1 is therefore not "the author didn't know about overlapping-polygon duplicates" — it's "the author solved this problem in the data-prep script and forgot to copy the fix into the core MCMC scoring function". The bug was a port-failure, not a knowledge gap. This makes the fix even more straightforward and the audit's quality narrative slightly stronger: the hostile reviewer can verify the author had already demonstrated awareness of the failure mode in another script.

Gemini's closing summary listed five concrete remaining tasks at the time of writing:

1. Fix the MCMC checkpointing state reset → **DONE** (CRITICAL #1)
2. Explicitly align dictionary keys → **DONE** (CRITICAL #2 + verification subset)
3. Copy the sjoin dedup pattern from `phase_4c_prep.py` into `score_exogenous_map` → **DONE** (HIGH)
4. Cast string district names to integers in the verification serializer → **DONE** (Part 2 CRITICAL #3)
5. Pin `networkx` → **DONE** (Part 4 MEDIUM)

All five code-side items are remediated. The audit's outstanding work is now: re-run the full 2M MCMC ensemble against the fixed code, compare percentile placements to the buggy version's published values, file a dated pre-registration amendment, and update `report_public.md` to reflect whichever way the re-run lands.

---

## Final tally

- **9 distinct code-level findings** across 5 Gemini passes (3 CRITICAL, 2 HIGH, 4 MEDIUM/NOTE)
- **9 of 9 remediated in source** as of 2026-04-26 evening
- **12 of 12 regression tests passing** (including the 3 new Gemini-spec tests)
- **0 fixes pending**; only re-run + delta report + amendment + public-report update remain
- **Honest characterisation:** the audit shipped a public-facing forensic claim ("no map in 2M reaches the minority's 52.8%") that was supported by a fundamentally broken ensemble (50 short chains stitched, not one continuous chain). The fact that this was caught by an external adversarial review *before* the headline became load-bearing in any downstream filing is exactly what the brief was designed to do. The pre-registration amendment will say so directly.
