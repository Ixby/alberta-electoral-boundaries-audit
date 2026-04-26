---
name: External code-audit findings — Meridian (Claude Opus 4.7), 2026-04-26
description: Second-pass independent code audit of the Alberta Electoral Boundaries Audit pipeline, run after the first-pass Gemini audit (commit 73544a3) had already remediated 9 findings. Output is what Gemini missed — three HIGH findings that affect headline-claim credibility, plus medium/low items.
type: methodology
---

# Code audit findings — Meridian (Claude Opus 4.7) + 2026-04-26

## Summary

- **Total findings: 0 critical + 3 high + 3 medium + 5 low/note**
- **Top 3 priority items:**
  1. Burst scripts retain the dict-iteration-order vulnerability that Gemini's CRITICAL #2 fix removed elsewhere ([targeted_gerrymander_burst.py:51-52](analysis/scripts/targeted_gerrymander_burst.py#L51-L52), [targeted_gerrymander_burst_ndp.py:52-53](analysis/scripts/targeted_gerrymander_burst_ndp.py#L52-L53))
  2. `efficiency_gap` is reimplemented in [fuzz_missing_eds.py:54-59](analysis/scripts/fuzz_missing_eds.py#L54-L59) with a different formula from canonical `seat_results` — `total/2 + 1` vs `total/2`. The two are not algebraically equivalent.
  3. ESS / autocorrelation diagnostics are computed on the *concatenated* 4-chain DataFrame at [mcmc_ensemble_250k_v0_8.py:267](analysis/scripts/mcmc_ensemble_250k_v0_8.py#L267). The cross-chain boundaries depress apparent autocorrelation, so the Geyer initial-positive truncation fires earlier than it should, **inflating reported n_eff**. Direction of bias is wrong for a "publication-grade ESS" claim.

- **Overall assessment:** I would trust this codebase as a research artefact, with caveats. The four headline metric formulas inside [seat_results](analysis/scripts/mcmc_ensemble.py#L110-L211) are textbook-correct, the verification-subset integrity guarantee is real, and the post-Gemini fixes (commit 73544a3) closed the worst structural bugs. The findings below are not pipeline-killers — they are the kind of "low-magnitude scientific-software bugs" the brief's §6 explicitly anticipated. Two are sign-symbol mismatches that would embarrass the author if a hostile expert spotted them first; one is a credibility-affecting overestimate of n_eff that should be recomputed before the public report cites convergence numbers; the rest are reproducibility-and-comment hygiene. **The "no map in 2,000,000 reaches the minority's value" headline is not threatened by anything I found, but the convergence-quality framing around it should be re-checked under per-chain ESS.**

---

## Audit context — what was already done

- The brief at [v0_1_external_code_audit_brief.md](analysis/methodology/v0_1_external_code_audit_brief.md) was previously handed to Gemini, which produced 9 findings remediated in commit `73544a3`. The full Gemini memo is at [v0_1_external_code_audit_findings_gemini_2026-04-26.md](analysis/methodology/v0_1_external_code_audit_findings_gemini_2026-04-26.md).
- The 9 Gemini fixes (chunked-chain state threading, dict-iteration alignment in `run_ensemble` and `verification_subset`, sjoin dedup in `score_exogenous_map`, int8 type-cast crash in verification subset, rural classifier strict mode, networkx pin, seats@50/50 clipping, declination sign-convention comment, three regression tests) were **verified present** in the current code; none of my findings re-flag them.
- This is a second pass *on top of* Gemini's. My value is what Gemini missed.

---

## Findings

### HIGH — Burst scripts still rely on dict-iteration order (Gemini's CRITICAL #2 fix not propagated)

- **Files:**
  - [targeted_gerrymander_burst.py:51-52](analysis/scripts/targeted_gerrymander_burst.py#L51-L52)
  - [targeted_gerrymander_burst_ndp.py:52-53](analysis/scripts/targeted_gerrymander_burst_ndp.py#L52-L53)

- **Description.** Both burst scripts contain a `score(partition)` helper that builds parallel UCP/NDP arrays by independently iterating two separate gerrychain Tally dicts:
  ```python
  ucp = np.array(list(partition["ucp"].values()), dtype=float)
  ndp = np.array(list(partition["ndp"].values()), dtype=float)
  ```
  This is the **exact pattern** Gemini's CRITICAL #2 flagged in `run_ensemble`. The fix Gemini put in place there — explicit key alignment via `keys = list(partition.parts.keys())` then index by `[k]` — was applied to [mcmc_ensemble.py:451-453](analysis/scripts/mcmc_ensemble.py#L451-L453) and [mcmc_verification_subset.py:148-150](analysis/scripts/mcmc_verification_subset.py#L148-L150) but **not** propagated to either burst script. Grep across the repo finds these as the only two remaining instances.

- **Why it matters.** The burst scripts produce the symmetric short-bursts result that the public report cites: "the targeted procedure CAN reach the minority map's UCP-favouring territory (52.87%)" — and the mirror NDP-direction equivalent. If gerrychain's two Tally updaters ever iterate parts in different order (a contract gerrychain does not promise — the whole reason Gemini insisted on explicit alignment elsewhere), per-district UCP/NDP totals are scrambled. The hill-climb then selects a "best" partition based on a corrupted seat count, and the headline 52.87% number is wrong. The bug is dormant in the current gerrychain version (0.3.2) but the entire reason it was fixed in `run_ensemble` is that the order-equality is fragile against future gerrychain releases or unrelated updater additions.

- **Suggested fix.** Replace lines 50-54 in both files with:
  ```python
  def score(partition):
      keys = list(partition.parts.keys())
      ucp = np.array([partition["ucp"][k] for k in keys], dtype=float)
      ndp = np.array([partition["ndp"][k] for k in keys], dtype=float)
      s = seat_results(ucp, ndp)
      return s["seats_at_50_50"], s
  ```
  Same fix Gemini already applied twice. Five-minute change.

---

### HIGH — Inconsistent efficiency-gap formula in `fuzz_missing_eds.py`

- **File:** [fuzz_missing_eds.py:54-59](analysis/scripts/fuzz_missing_eds.py#L54-L59)

- **Description.** This script reimplements `efficiency_gap` instead of importing it from `seat_results`:
  ```python
  def efficiency_gap(ucp_arr, ndp_arr):
      total = ucp_arr + ndp_arr
      won = ucp_arr > ndp_arr
      wasted_ucp = np.where(won, ucp_arr - (total / 2 + 1), ucp_arr)
      wasted_ndp = np.where(won, ndp_arr, ndp_arr - (total / 2 + 1))
      return float((wasted_ndp.sum() - wasted_ucp.sum()) / total.sum())
  ```
  The canonical implementation in [mcmc_ensemble.py:154-157](analysis/scripts/mcmc_ensemble.py#L154-L157) is:
  ```python
  ucp_wasted = np.where(ucp_win, ucp - total / 2, ucp)
  ndp_wasted = np.where(~ucp_win, ndp - total / 2, ndp)
  eg = (ndp_wasted.sum() - ucp_wasted.sum()) / total.sum()
  ```
  The fuzz script subtracts `total/2 + 1` from the winner; the canonical subtracts `total/2`. The `+1` is a discrete-vote "minimum margin to win" adjustment (treating votes as integers, the smallest winning total is `total/2 + 1`), which is one defensible convention — but it is **not** the Stephanopoulos-McGhee (2014) formula the audit cites, and not what the canonical `seat_results` uses.

- **Why it matters.** The fuzz scenarios feed an "EG" column in the published table at the bottom of `fuzz_missing_eds.py` (lines 165-168, then 170-175 for the 10k-resample distribution). If the report's prose anywhere compares those EG values to the canonical-pipeline EG values published elsewhere, the comparison is invalid — the numbers come from two different formulas. The discrepancy magnitude is roughly `n_districts / total_votes` per side, which for 89 districts and ~1.7M votes is ~5×10⁻⁵ — small in absolute terms but non-zero, asymmetric (always slightly UCP-favouring vs canonical), and exactly the kind of thing a hostile reviewer would catch if they re-ran the fuzz scenarios with the canonical `seat_results.efficiency_gap` and got different numbers.

- **Suggested fix.** Delete the local `efficiency_gap` function and import from canonical:
  ```python
  from v0_1_mcmc_ensemble import seat_results
  ...
  m = seat_results(ucp_arr, ndp_arr)
  eg = m["efficiency_gap"]
  ```
  Then re-run the script and update any downstream tables. If the `+1` discrete-vote convention is intentional, document why and make the canonical match — but two parallel conventions in the same audit is the wrong answer.

---

### HIGH — Autocorrelation/ESS computed on concatenated 4-chain DataFrame inflates n_eff

- **File:** [mcmc_ensemble_250k_v0_8.py:248, 266-271](analysis/scripts/mcmc_ensemble_250k_v0_8.py#L248-L271)

- **Description.** After 4 parallel chains finish, the script concatenates them via `df = pd.concat(parts, ignore_index=True)` and then computes autocorrelation diagnostics on the concatenated series:
  ```python
  for key, label in metrics_config:
      diag = autocorrelation_ess(df[key].values)
  ```
  But the concatenated series contains 3 chain-boundary discontinuities. At each boundary, sample `i` and sample `i+1` come from different chains seeded from independent RNG streams — they are *not* autocorrelated. As lag `k` grows, more and more pairs in the autocovariance sum span boundaries, depressing the apparent ACF toward zero faster than the within-chain ACF actually decays.

  [autocorrelation_ess](analysis/scripts/mcmc_ensemble_100k.py#L79-L129) uses Geyer's initial-positive-sequence truncation (stop summing when `acf[k] ≤ 0`). With the cross-chain depression, that condition triggers *earlier* than it would on a single continuous chain, producing a smaller estimated `tau`, and therefore a **larger** estimated `n_eff = n / tau`. The bias is the wrong direction for an honesty-of-convergence claim: reported ESS is optimistic.

- **Why it matters.** The 250k script writes [v0_1_mcmc_convergence_diagnostics_250k_v0_8.json](data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.json) which the audit cites as evidence the chain is well-mixed. If the same code runs the 2M ensemble (it's the same script with `--n-steps=2000000`), the headline "publication-grade ESS" is inflated by the same mechanism. A sceptical reader recomputing per-chain (treating each chain separately, then aggregating) will get a smaller `n_eff` than what's published.

  Caveat: the magnitude of the inflation depends on the within-chain `tau`. If `tau` is small (say, < 5) the bias is negligible; if `tau` is large (say, > 100, which the published `tau` figures imply for some metrics), the bias can be material.

- **Suggested fix.** Compute per-chain ESS and aggregate:
  ```python
  per_chain_diags = []
  for chain_csv in chain_paths:
      chain_df = pd.read_csv(chain_csv)
      per_chain_diags.append(autocorrelation_ess(chain_df[key].values))
  # Aggregate: total n_eff = sum of per-chain n_eff (independent chains)
  agg_n_eff = sum(d["n_eff"] for d in per_chain_diags if not np.isnan(d["n_eff"]))
  agg_tau_avg = np.mean([d["tau"] for d in per_chain_diags if not np.isnan(d["tau"])])
  ```
  Persist both the per-chain and aggregate diagnostics. If the post-fix aggregate `n_eff` is materially smaller than what the old concatenated code published, file a dated pre-registration amendment and update the report's convergence prose.

---

### MEDIUM — RNG reseeded every chunk inside a single threaded chain

- **File:** [mcmc_ensemble_250k_v0_8.py:120-130](analysis/scripts/mcmc_ensemble_250k_v0_8.py#L120-L130)

- **Description.** Inside `_run_chain_chunked`, after the Gemini state-threading fix, partition state is correctly threaded across chunks via `current_state`. But at every chunk boundary, the worker also reseeds:
  ```python
  chunk_seed = base_seed * 100_000 + chain_idx * 1_000 + chunk_idx
  _np.random.seed(chunk_seed)
  _random.seed(chunk_seed)
  ```
  For a 250k-step chain with `chunk_size=5000`, this reseeds 50 times per chain. For 2M with `chunk_size=5000` and `n_chains=4` (500k per chain), it reseeds 100 times per chain. Each reseed restarts the proposal-RNG sequence from a fresh Mersenne-Twister state.

- **Why it matters.** Within a single threaded chain, the RNG-driven proposal sequence is no longer a continuous Markov walk — it's 50–100 short walks, each with the partition state continuing forward but the proposal randomness restarting. This subtly changes the chain's mixing behaviour vs a chain run with a single seed. In particular, the within-chain autocorrelation structure has artefacts at chunk boundaries (similar in spirit to the cross-chain finding above, but at finer granularity). The convergence diagnostics may look better-behaved than a true single-RNG chain because the periodic reseeds inject "fresh" randomness.

  This is a less severe version of finding §3 above; the chunk-boundary effect on ACF within a chain is smaller than the cross-chain boundary because chunk boundaries are 5000-apart and only the proposal RNG resets, not the partition.

- **Suggested fix.** Drop the per-chunk reseed. Set the chain seed once at the top of `_run_chain_chunked` and let the RNG advance with the chain:
  ```python
  chain_seed = base_seed * 100_000 + chain_idx * 1_000
  _np.random.seed(chain_seed)
  _random.seed(chain_seed)
  for chunk_idx in range(chunks_done, n_chunks):
      # no reseed here; let RNG advance
      ...
  ```
  Trade-off: this loses the deterministic-resume property the per-chunk seed gave. But the existing code already documents (lines 73-75) that resume-after-crash invalidates chain continuity anyway, and the headline runs are documented to be from-scratch. So the determinism the per-chunk seed bought wasn't actually useful for the publication-grade run.

---

### MEDIUM — `keep="first"` in score_exogenous_map sjoin dedup is non-deterministic across GEOS versions

- **File:** [mcmc_ensemble.py:300](analysis/scripts/mcmc_ensemble.py#L300)

- **Description.** Gemini's HIGH fix added `covered = covered[~covered.index.duplicated(keep="first")]` to dedup overlapping-polygon double-attribution. The dedup is correct in *count* (each VA contributes once) but not deterministic in *which polygon wins*. `gpd.sjoin` row order depends on the spatial-index iteration order in the underlying GEOS / pyogrio stack. Different GEOS minor versions, different shapely builds, and different pyogrio builds can produce different orderings. With `keep="first"`, the same VA can be attributed to a different district on a different machine.

- **Why it matters.** The audit's reproducibility promise — "any reader can recompute and confirm byte-for-byte" — is undercut whenever a v0_8 carve-out produces sliver overlaps. The fuzzing brief at [fuzz_missing_eds.py](analysis/scripts/fuzz_missing_eds.py) bounds the affected polygon count at 6 in the minority, so the magnitude is small, but the *kind* of non-determinism (different reviewer, different number) is exactly what reviewers complain about loudly when they catch it.

- **Suggested fix.** Make the tie-break explicit and deterministic. After sjoin and before the duplicate-drop, sort by the polygon-id column:
  ```python
  joined = gpd.sjoin(...)
  covered = joined.dropna(subset=[id_col])
  covered = covered.sort_values(by=id_col, kind="mergesort")  # stable
  covered = covered[~covered.index.duplicated(keep="first")]
  ```
  Now the same VA always gets credited to the alphabetically-first overlapping district, regardless of GEOS version. Document the convention in the docstring. Then add a regression test that builds a synthetic VA inside two named overlapping polygons and asserts the deterministic tie-break.

---

### MEDIUM — Both burst scripts share `SEED=137`; first-burst trajectories are bit-identical

- **Files:**
  - [targeted_gerrymander_burst.py:43](analysis/scripts/targeted_gerrymander_burst.py#L43)
  - [targeted_gerrymander_burst_ndp.py:41](analysis/scripts/targeted_gerrymander_burst_ndp.py#L41)

- **Description.** Both scripts seed `np.random` and `random` with `SEED=137`. The NDP-direction script's comment at line 41 says "same seed as the UCP-maximization run for symmetry." Because both scripts then build the same VA graph, run `recursive_tree_part` only if needed (same condition), and start the first 50-step ReCom burst from the same 2019 seed partition with the same proposal RNG, **the first burst's proposal sequence is bit-identical between the two runs**. They diverge starting at burst 2 because each picks a different "best" partition (the highest UCP-share state for the UCP run, the lowest for the NDP run) and that partition feeds into the next burst's MarkovChain construction.

- **Why it matters.** The audit frames the two burst runs as "symmetric independent tests": the UCP-maximisation can reach the minority territory; the NDP-maximisation can reach the majority territory. If a reviewer reads "independent" as "uncorrelated", they will be wrong about burst 1 and approximately wrong about burst 2 (still partially correlated through the shared RNG state at burst boundaries). For an existence claim ("a non-neutral procedure can reach X"), this is harmless — the procedure is hill-climbing, not statistical inference. For the framing of the symmetry test, "shared seed" should be disclosed.

- **Suggested fix.** Either change one script's seed (e.g. `SEED_NDP = 138`) and document why the seeds differ, OR keep the shared seed and document explicitly in the burst write-up that "the symmetric runs share an RNG seed; this is intentional so the two procedures evaluate the SAME proposal trajectory under opposite selection rules". The latter is actually a cleaner experimental design — but only if it's named.

---

### LOW / NOTE — `pct_rank` docstring claims "strict less than" but implementation is midrank

- **File:** [mcmc_ensemble.py:472-480](analysis/scripts/mcmc_ensemble.py#L472-L480)

- **Description.** Docstring says `Uses strict 'less than' like scipy.percentileofscore(kind='mean')`. The code is `100.0 * (below + 0.5 * equal) / len(values)` — that is the *midrank* convention (`scipy.percentileofscore(kind='mean')`), which is **not** strict less-than. The implementation matches scipy correctly; only the descriptor is wrong.

- **Why it matters.** Affects how the audit's "pNN" labels in the histograms ([analysis/methodology](analysis/methodology/)) are read. A reader expecting "strict less" sees `pr = 100.0` and concludes "no map in N samples reaches this value", but midrank `pr = 100.0` is also reached when **a small fraction of samples tie the value** (because each tie contributes 0.5/N rather than 0). For the headline "no map reaches the minority's seats@50/50" claim, the prose should be tested against `np.sum(ensemble_values >= real_value)` rather than `pct_rank == 100`, or the docstring should be corrected.

- **Suggested fix.** Replace docstring sentence with `Uses midrank convention (scipy.percentileofscore kind='mean'): below + half of ties, divided by n.` Then audit the prose claims that depend on `pct_rank` to confirm they distinguish "no ties" from "no strictly-greater". The verification subset's `data/v0_1_mcmc_real_map_scores_250k_v0_8.json` should be checked for `seats_at_50_50` ties between the minority's value and any ensemble samples.

---

### LOW / NOTE — Stale "reload graph" comment in 250k_v0_8.py

- **File:** [mcmc_ensemble_250k_v0_8.py:253-255](analysis/scripts/mcmc_ensemble_250k_v0_8.py#L253-L255)

- **Description.** Comment says `# Reload the parent's graph for the post-run analysis (real-map scores etc. don't need it ...)`. No reload happens. The post-run code only consumes `df` (concatenated samples) and the `m_maj`/`m_min` real-map scores already computed before the pool. The comment is misleading.

- **Suggested fix.** Delete lines 253-255 — the comment isn't load-bearing.

---

### LOW / NOTE — `os.environ.setdefault("PYTHONIOENCODING", "utf-8")` in `main()` is a no-op

- **Files:**
  - [mcmc_ensemble.py:650](analysis/scripts/mcmc_ensemble.py#L650)
  - [mcmc_ensemble_100k.py:327](analysis/scripts/mcmc_ensemble_100k.py#L327)
  - [mcmc_ensemble_250k_v0_8.py:357](analysis/scripts/mcmc_ensemble_250k_v0_8.py#L357)

- **Description.** Setting `PYTHONIOENCODING` *inside* a Python process has no effect on stdout encoding — Python reads that env var at interpreter startup. Setting it in `main()` only affects subprocesses spawned after the assignment.

- **Why it matters.** On Windows with default cp1252 stdout, any non-ASCII output (e.g., the `±` character in `pop_deviation=±25%`) raises `UnicodeEncodeError`. The `setdefault` line gives a false sense of safety.

- **Suggested fix.** Either invoke with the env var set externally (the [REPRODUCING.md](REPRODUCING.md) docstring already documents this), or use `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` at the top of `main()`. Drop the no-op `os.environ.setdefault`.

---

### LOW / NOTE — `fuzz_missing_eds.py` runs at module import (no `if __name__ == "__main__"`)

- **File:** [fuzz_missing_eds.py](analysis/scripts/fuzz_missing_eds.py) — entire file

- **Description.** No `main()` function and no `if __name__ == "__main__":` guard. The 10,000-trial Monte Carlo at lines 146-159 runs at module-import time. Anyone importing this module for any reason — e.g. a test that wants to share its `seats_at_50_50` helper — pays the full simulation cost.

- **Suggested fix.** Wrap the procedural body in `def main(): ...` and add `if __name__ == "__main__": main()`. Keep the helpers (`seats_at_50_50`, `efficiency_gap`, `add_rows`) at module level for reuse. Better still, after fixing the §HIGH-#2 finding, delete `efficiency_gap` and `seats_at_50_50` from this file entirely and import from canonical.

---

### LOW / NOTE — Divide-by-zero in fuzz `seats_at_50_50` is masked but warns

- **File:** [fuzz_missing_eds.py:47](analysis/scripts/fuzz_missing_eds.py#L47)

- **Description.** `np.where(total > 0, ucp_arr / total, 0.5)` — numpy evaluates both branches of `where`, so `ucp_arr / total` is computed even where `total == 0`, raising a divide-by-zero RuntimeWarning. The result is correct (the 0.5 replaces the inf/nan) but the warning floods the log.

- **Suggested fix.** Either guard with `np.errstate(divide="ignore", invalid="ignore")`, or precompute a safe denominator: `safe_total = np.where(total > 0, total, 1)`; `ucp_share = np.where(total > 0, ucp_arr / safe_total, 0.5)`.

---

## What I did not audit

Honest list of coverage gaps in this pass:

- **Headline 2M MCMC dataset.** I did not load the actual `data/v0_1_mcmc_ensemble_*250k_v0_8.csv` or the convergence-diagnostics JSON. My finding §HIGH-#3 (ESS inflation) is structural — derived from reading the code, not from re-running the diagnostic. Confirming the *magnitude* of the bias requires recomputing per-chain ESS on the actual checkpoint files. The current `data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.buggy_pre_audit_2026-04-26.json` (preserved as the pre-fix copy) and the post-fix rerun would let an investigator quantify the inflation.
- **Verification-subset npz contents.** I trusted the brief's §2 statement that the verification subset is byte-trustworthy and did not re-run the recompute spot-check. The pytest test for this passes per the brief.
- **All ~50 non-priority scripts.** The brief listed 7 priority files; I read 8 (the seven plus `mcmc_ensemble_100k.py` which exports `autocorrelation_ess`). Scripts I did NOT read include but are not limited to: `v0_1_chen_rodden_*.py`, `compactness_metrics.py`, `dpg_perfecter.py`, `v0_1_phase_4c_*.py`, `extended_partisan_metrics.py`, `marginal_seats_analysis.py`, `parse_2015_results.py`, `electoral_forensics_population.py`, the OCR / scraper utilities, and the article-figure builders. Bugs in those scripts would feed in to derived datasets but would not affect the four core formulas in `seat_results`.
- **Geometry / shapefile-builder pipeline.** The v0_8 inheritance-fill logic that produces the 2026 reconstructed polygons lives in `v0_1_build_canonical_shapefiles*.py` and `v0_1_shape_refinement_v*.py`. I did not audit polygon construction. The §3a #4 brief concern about "double-attribution edge cases" is partially addressed by Gemini's sjoin dedup fix; the deterministic-tie-break finding (§MEDIUM-#5 above) closes another corner.
- **R / QGIS validation.** The brief mentions a planned R cross-validation; no R code in scope.
- **Pre-registration amendment compliance.** I read the audit brief and the Gemini findings but did not check whether the pre-registration document at `analysis/reports/v0_1_pre_registration_draft.md` is consistent with the current code's behaviour after the Gemini fixes.
- **Multiprocessing pickling.** `_run_chain_chunked` is dispatched via `ProcessPoolExecutor`. I did not test that the args tuple pickles cleanly under spawn-mode (Windows default) — but the script has presumably been running successfully for the 2M dataset, so this is not a latent bug.

---

## What the test suite SHOULD cover but doesn't

Five untested behaviours, ranked by likely bug-magnitude:

1. **`score()` in the burst scripts.** The pattern Gemini flagged in `run_ensemble` lives untested in two more places (this finding's §HIGH-#1). A test that builds a synthetic 4-district partition and asserts that `score(part)` returns the same metrics as `seat_results` called directly with the explicit-key-aligned arrays would catch the propagation gap and any regression. Test should construct a partition where the two Tally updaters' `.values()` order differs (mock-patchable in a unit test) — that's the only way to make the latent bug manifest in CI.

2. **`autocorrelation_ess` per-chain vs concatenated.** A test that generates a synthetic 4-chain dataset (each chain a known AR(1) process, chains independently seeded), computes ESS per-chain and concatenated, and asserts the concatenated estimate is *not* used as the headline ESS. Would have caught §HIGH-#3.

3. **`fuzz_missing_eds.efficiency_gap` vs canonical.** A test that calls both `efficiency_gap` (local) and `seat_results(...)["efficiency_gap"]` on the same arrays and asserts equality (or asserts the documented difference). Would have caught §HIGH-#2 — and would prevent the local copy from drifting away from canonical again.

4. **`seat_results` declination NaN edge case.** Brief §3b explicitly asks for the one-party-wins-everything edge case. The current test suite does not exercise it. A 3-line test (`np.array([60, 60, 60])` UCP, `np.array([40, 40, 40])` NDP → `assert math.isnan(m["declination"])`) would close it.

5. **`score_exogenous_map` deterministic tie-break under overlap.** Existing test [test_score_exogenous_map_sjoin_deduplicates_overlap](tests/test_scoring.py#L263-L302) confirms count-once but not which-polygon-wins. Add an assertion that the chosen district name matches the alphabetically-first of the overlapping polygons (assuming the §MEDIUM-#5 fix above is applied).

---

## Methodology spot-checks

For the four formulas in brief §3b:

- **Efficiency gap (canonical `seat_results`):** Matches Stephanopoulos & McGhee (2014). `wasted_winner = winner_votes - total/2`; `wasted_loser = loser_votes`; `EG = (wasted_NDP - wasted_UCP) / total`. Sign convention positive = UCP-favoured is consistent with the report's prose. **Verdict: matches.**
  - Caveat: the local reimplementation in `fuzz_missing_eds.py` uses `total/2 + 1` (discrete-vote convention) and is **not** equivalent — see §HIGH-#2.

- **Mean-median:** `np.median(ucp_share) - np.mean(ucp_share)`. McDonald & Best (2015) convention. When NDP voters are packed into a few low-UCP-share districts, the mean is dragged down below the median → positive value → UCP-favoured. **Verdict: matches.** Internal sign convention consistent with EG.

- **Declination:** Warrington (2018). `theta_R = atan2(mean_ucp_in_ucp_won - 0.5, R/(2n))`; `theta_D = atan2(0.5 - mean_ucp_in_ndp_won, D/(2n))`; `δ = (2/π)(theta_R - theta_D)`. NaN when one party wins all districts. The local sign convention (negative = UCP-favoured) is **inverted** relative to the most common literature convention (positive = focus-party-disadvantaged), which the in-code comment now correctly documents (Gemini doc-only fix). **Verdict: matches Warrington algebraically; sign convention is internally consistent and the report's empirical interpretation always tracked the local convention.** A reader new to the code who pattern-matches to the literature will be momentarily confused — that's a documentation cost, not a correctness cost.

- **Seats@50/50 (uniform swing):** Compute provincial UCP share, shift each district's UCP share by `0.5 - province`, clip to [0,1] (Gemini fix), count districts where shifted share `> 0.5` strict. **Verdict: matches textbook implementation.** Strict `>` correctly handled per documented "ties → NDP wins" convention; the `np.clip` is forward-compatibility, not a correctness change.

---

## Closing note

If the author re-runs the headline 2M ensemble with: (a) the burst-script Tally fix, (b) `fuzz_missing_eds` using canonical `efficiency_gap`, (c) per-chain ESS computation, and (d) the deterministic tie-break in `score_exogenous_map` — the resulting numbers will not move materially for any current published claim, but the **defensibility** of those claims under hostile review goes up by a noticeable margin. None of these are pipeline-killers, none threaten the "no map in 2M reaches the minority's value" headline. They are precisely the "low-magnitude scientific-software bugs" the brief's §6 asked me to surface, exactly so they can be cleaned up before someone hostile finds them.

The remediation footprint is small: roughly 30 lines of code changes plus 5 new unit tests.
