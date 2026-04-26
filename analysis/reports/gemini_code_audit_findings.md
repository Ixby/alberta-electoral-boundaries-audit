# Code audit findings — Gemini 3.1 Pro (High) - 2026-04-26

## Summary

- Total findings: 1 critical + 1 high + 1 medium + 1 low
- Top 3 priority items:
  1. Dict-iteration order bug in targeted gerrymander scoring (`v0_1_targeted_gerrymander_burst.py`).
  2. Missing spatial-join deduplication in fuzzing script (`v0_1_fuzz_missing_eds.py`).
  3. PRNG sequence continuity breakage via per-chunk reseeding in the 250k ensemble (`v0_1_mcmc_ensemble_250k_v0_8.py`).
- Overall assessment: I would trust the core findings of this codebase for the 2M ensemble runs, as the critical bugs were already mitigated in those primary scripts (the author already included fixes referencing prior audit findings). However, the supplementary analytical scripts (fuzzing and targeted bursts) contain real flaws that could distort those specific supplementary claims.

## Findings

### CRITICAL — Unstable dict iteration order in targeted burst scoring
- File: `analysis/scripts/v0_1_targeted_gerrymander_burst.py`
- Lines: 50-54
- Description: `score(partition)` constructs the vote arrays by calling `list(partition["ucp"].values())` and `list(partition["ndp"].values())`. While Python 3.7+ preserves dict insertion order, GerryChain's `Tally` updaters do not guarantee that two separate tallies will populate keys in the exact same order. If they diverge, District A's UCP vote is paired with District B's NDP vote, resulting in garbage inputs to `seat_results()`. The author already applied the explicit-key-alignment fix to `v0_1_mcmc_ensemble.py` and `v0_1_mcmc_verification_subset.py` (citing a prior Gemini audit) but missed this script.
- Why it matters: The targeted gerrymander's entire claim ("can a non-neutral procedure reach the minority's seats@50/50?") relies on this scoring function accurately guiding the hill-climb. If the score is noisy/garbage, the bursts won't reliably maximize the true metric.
- Suggested fix: I have already committed a fix to align the keys:
```python
keys = list(partition.parts.keys())
ucp = np.array([partition["ucp"][k] for k in keys], dtype=float)
ndp = np.array([partition["ndp"][k] for k in keys], dtype=float)
```

### HIGH — Overlapping slivers double-counted in fuzzing script
- File: `analysis/scripts/v0_1_fuzz_missing_eds.py`
- Lines: 17-20
- Description: The script joins VA centroids to minority map polygons using `gpd.sjoin()`. The author notes elsewhere that the v0_8 polygon construction occasionally produces overlapping slivers. If a centroid falls inside such an overlap, `sjoin` returns multiple rows. Unlike `score_exogenous_map()` in `v0_1_mcmc_ensemble.py`—which explicitly deduplicates these matches via `covered = covered[~covered.index.duplicated(keep="first")]`—this script omits the deduplication.
- Why it matters: The fuzzing script brackets the missing EDs' impact on the minority map's `seats@50/50`. If overlap slivers double-count VA votes, the baseline vote totals and partisan balance of the non-missing EDs are slightly distorted.
- Suggested fix: I have committed the fix to add `covered = covered[~covered.index.duplicated(keep="first")]` before the groupby aggregation.

### MEDIUM — PRNG sequence continuity broken by per-chunk reseeding
- File: `analysis/scripts/v0_1_mcmc_ensemble_250k_v0_8.py`
- Lines: 121-123
- Description: In `_run_chain_chunked`, the script calls `_np.random.seed(chunk_seed)` and `_random.seed(chunk_seed)` inside the `for chunk_idx` loop. This re-seeds the random number generator every 5,000 steps to allow for deterministic resume. However, it breaks the PRNG's internal state. An MCMC chain of 250,000 steps should consume a single continuous stream of random numbers; stitching 50 different 5k streams together alters the statistical properties of the generator.
- Why it matters: Technically, it violates the assumptions of the Markov chain's transition probabilities by creating an artificial periodicity in the RNG's phase space. Practically, with a 5k chunk size and the Mersenne Twister, the impact is likely negligible, but it's an MCMC anti-pattern.
- Suggested fix: Only re-seed at the start of the chain (if `n_done == 0`), or serialize the PRNG state into the checkpoint files and restore it on resume.

### LOW / NOTE — Float boundary drift at exact 0.5 ties in uniform swing
- File: `analysis/scripts/v0_1_mcmc_ensemble.py`
- Lines: 198-200
- Description: `seats_at_50_50` computes `shifted = np.clip(ucp_share + swing, 0.0, 1.0)` and then evaluates `shifted > 0.5`. The comment correctly states "at 0.5 tied: treat as NDP win for symmetry (rounding)". However, floating point representation of `0.5 - province_ucp` can yield `shifted` values like `0.5000000000000001` or `0.4999999999999999` for an exact tie.
- Why it matters: A true exact tie could randomly be credited to UCP if the float rounding error leans positive. Given the scale of vote totals, exact ties are practically non-existent, but the logic relies on perfect float arithmetic which isn't guaranteed.
- Suggested fix: Add a small epsilon (`1e-9`) tolerance check or use integer arithmetic. 

## What I did not audit

- I did not validate the logic inside Gerrychain itself (`recom`, `recursive_tree_part`).
- I did not verify the creation of the underlying data files (`va_polygons_with_2023_votes.gpkg`, DA populations), trusting them as stated.
- I did not review the Python 3.7+ backward compatibility of the entire codebase, only the dict iteration order specific bug.

## What the test suite SHOULD cover but doesn't

1. `score()` in `v0_1_targeted_gerrymander_burst.py`: The dict iteration bug would have been caught if this function had a unit test injecting unaligned mock dictionaries.
2. `v0_1_fuzz_missing_eds.py`'s manual aggregation logic: Needs a test to verify it handles polygon overlap slivers identically to the main pipeline.
3. `v0_1_rural_protection_test.py`'s `classify()` function: A simple parameterized test checking that all 87 specific ED names map to the expected urban/rural/hybrid category would prevent silent classification failures if name spellings drift.

## Methodology spot-checks

For each formula in §3b above:
- **Efficiency gap**: Matches Stephanopoulos-McGhee 2014. Formula computes `(wasted_NDP - wasted_UCP) / total`. Sign convention correctly results in positive values when UCP is favoured.
- **Mean-median**: Matches standard implementation. Positive values correctly indicate UCP-favoured maps.
- **Declination**: Matches Warrington 2018 geometry. Gracefully handles the NaN edge case if a party wins zero seats. Sign convention (negative = UCP-favoured) is consistent with the code comments.
- **Seats@50/50 uniform swing**: Matches textbook implementation. The shift-then-clip sequence is correct and ensures vote shares cannot exceed [0, 1] bounds.
