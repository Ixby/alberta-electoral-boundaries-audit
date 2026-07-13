> **Backward:**
> - `analysis/scripts/mcmc_ensemble_canonical.py` — the canonical ReCom ensemble whose robustness this pre-registration covers
> - `analysis/scripts/drand_seed.py` — beacon-derived seeding infrastructure
> - `preregistration/seed_commitments.md` — chain-of-custody for prior pre-registrations (qsgy8, 6pt83, w2s8k, r3zm7)
> - `data/outputs/simulation_convergence_diagnostics_canonical.json` — n_eff and R-hat values being checked
>
> **Forward:**
> - `analysis/scripts/forest_recom_ensemble.py` — the script this pre-registration commits to running
> - `findings/forest_recom_robustness.md` — results document (to be created after execution)

# OSF Pre-Registration — Forest-ReCom Sampler Robustness Check

> **Pre-registration target:** OSF (form to be filed at the same time as the
> first beacon-anchored execution of `forest_recom_ensemble.py`)
>
> **Status when this document is committed to git:** Pre-execution. No
> Forest-ReCom samples have been drawn from any beacon-anchored seed. The
> drand seed for the run is fixed in `analysis/scripts/drand_seed.py`'s
> `get_canonical_seed("forest_recom_robustness")` and is computable
> from the public beacon at round 5,500,000 before the script has ever run.

---

## 1. Title

**Forest-ReCom sampler robustness check for the Alberta Electoral Boundaries Audit canonical 1.01 M ensemble.**

## 2. Authors

Will Conner (Mount Royal University). Independent personal research.

## 3. Question

Is the directional finding of the audit's canonical 1,010,000-plan ReCom ensemble — that the 2026 minority commission proposal sits in the extreme tail of every pre-registered partisan-fairness metric — robust to the choice of spanning-structure weighting used by the proposal mechanism?

## 4. Why this is a real question

Standard ReCom samples a uniform spanning tree of the joint subgraph of two merged districts at each proposal step and finds a balance cut. Spanning-tree weighting is known to put more probability mass on compact partitions than the uniform-over-valid-plans distribution that "neutral" implies (see DeFord, Duchin & Solomon, *Recombination: A Family of Markov Chains for Redistricting*, 2021, §4 on stationary-distribution bias). On a substrate as constrained as Alberta — three statutorily-protected s.15(2) districts that legally reach −50% population deviation, large rural districts that compactness penalises, dense urban-edge growth — this bias is plausible enough to test.

The direction of the bias is not predictable in advance. A more-compact-than-feasible ensemble could make the minority's compactness flags look *more* extreme (the comparison set is too compact, so any non-compact map sits further in the tail) or *less* extreme (the comparison set is biased toward exactly the geometric properties the minority's flagged regions also have).

This pre-registration commits to running Forest-ReCom — which replaces spanning-tree weighting with spanning-forest weighting and is known to shift the stationary distribution toward less-compact partitions — and reporting the result regardless of direction.

## 5. Hypothesis (directional, pre-committed)

**H₀ (null, to be rejected):** The minority proposal's percentile rank on the four canonical partisan-fairness metrics (efficiency gap, mean-median, declination, seats@50/50) shifts by less than 5 percentile points under Forest-ReCom relative to canonical ReCom. (Operationally: the canonical conclusion is robust to spanning-structure choice.)

**H₁ (alternative):** The minority proposal's percentile rank shifts by 5 or more percentile points on at least one of the four metrics. (Operationally: spanning-structure choice matters and the canonical claim needs to be qualified.)

The 5-point threshold is chosen because:
- It is smaller than the gap between the minority's current percentile (p99.99 on seats@50/50) and the next-most-extreme percentile worth flagging (p95, the audit's outlier threshold).
- It is large enough to be detectable above sampling noise at the planned Forest-ReCom run size (see §7 below).
- It is committed in writing before the run; no post-hoc adjustment.

## 6. Methodology

### 6.1 Sampler

**Base proposal:** gerrychain `recom` (same library, same version as the canonical run — `gerrychain==0.3.2` per the repo's lock).

**Spanning-structure method:** Replace the canonical `_bpt_global` (boundary-permutation-tree global, the spanning-tree method used in `mcmc_ensemble.py:548`) with a spanning-forest sampler. Specifically: for each proposal step, draw a uniform spanning forest with two trees from the joint two-district subgraph using Aldous-Broder generalised to forests (see Wilson 1996; Marchal 2000 for the loop-erased-random-walk derivation). The first connected component becomes district A; the second becomes district B; the implicit cut between them is checked for population balance.

### 6.2 Substrate

Identical to the canonical run:
- `data/shapefiles/canonical/ea_majority_2026_eds.gpkg`
- `data/shapefiles/canonical/ea_minority_2026_eds.gpkg`
- `data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg`
- Initial partition: 2019 enacted 87-district map (`initial_assignment_2019()`)
- Population column: `pop_2021`, target = 2021 census population / 89
- Deviation: ±25% with the same s.15(2) special-district exceptions as the canonical run (`alberta_statutory_population_constraint` in `mcmc_ensemble.py:558`)

### 6.3 Seed

Derived from the public Cloudflare drand beacon round **5,500,000** (same round as the canonical run; randomness hex committed in `analysis/scripts/drand_seed.py`).

**Clarification on round 5,500,000 reuse:** This round is a historical beacon output (October 2025); it was publicly available and unmodifiable before this pre-registration document was written. The audit's pre-registration discipline requires that the salt string (`"forest_recom_robustness"`) be fixed *before* any Forest-ReCom result is observed. Because the round is public and fixed, and the salt string is committed before the analysis runs, the round is legitimately reusable for this robustness check (which is being pre-registered before execution). For comparison, `preregistration/seed_commitments.md` Amendment A §1 explicitly rejects using round 5,500,000 for the Lunty-map future test, because that test requires a drand round *after* the Lunty committee's map publishes — a future, unknown beacon output that serves as a time-lock for the pre-registered scoring procedure. The two uses are in different contexts with different security requirements; round reuse is acceptable here but not there.

Salt: `"forest_recom_robustness"`. This salt string is fixed in this document and in `analysis/scripts/forest_recom_ensemble.py` and is committed to git at the same time as this pre-registration. The salt could not have been chosen by inspecting Forest-ReCom results, because no Forest-ReCom result exists at the time of commit.

A reviewer can compute the seed independently:
```
python analysis/scripts/drand_seed.py --salt forest_recom_robustness
```
and verify it matches the seed printed when the ensemble run begins.

### 6.4 Run size

**Phase A — detection run (committed now, this pre-registration):**
- 100,000 total samples
- 4 chains × 25,000 steps each, started from the same initial partition with chain-specific salt suffixes (`forest_recom_robustness_chain_{0,1,2,3}`)
- Burn-in: first 5,000 steps per chain dropped before metric reporting
- Effective sample size target: ≥ 200 per partisan metric per chain (a quarter of the canonical run's per-chain n_eff, reflecting the smaller wall-clock budget for a detection run)

**Phase B — scale-up run (conditional, NOT pre-committed here):**
- If Phase A indicates H₁ (any metric shifts by ≥ 5 percentile points), a Phase B at 1,000,000 samples will be filed as a separate pre-registration before being executed. The current document does not commit to Phase B.
- If Phase A is clean (all metrics within 5 points), no scale-up is required and the result stands as filed.

### 6.5 Outputs (pre-committed locations)

```
data/outputs/forest_recom_raw_samples_phaseA.csv
data/outputs/forest_recom_real_map_scores_phaseA.json
data/outputs/forest_recom_percentiles_phaseA.csv
data/outputs/forest_recom_convergence_diagnostics_phaseA.json
```

These paths are committed before the run. If the run fails or is aborted, the absence of these files (with a non-empty `findings/forest_recom_robustness.md` reporting the failure) is itself the publishable result.

### 6.6 Convergence diagnostics

Computed and reported identically to the canonical run:
- Gelman-Rubin R-hat per partisan metric, 4-chain split
- Geyer's initial-positive-sequence τ and n_eff per metric (`autocorrelation_ess` in `mcmc_ensemble.py`)
- Lag-1, lag-10, lag-100 autocorrelations per metric
- Trace plots per metric per chain

## 7. Pre-committed decision rule

Let `p_canonical(m)` = percentile rank of the minority proposal's value on metric `m` in the canonical 1.01 M ReCom ensemble.

Let `p_forest(m)` = percentile rank of the minority proposal's value on metric `m` in the Phase A 100 k Forest-ReCom ensemble.

For each m in {efficiency_gap, mean_median, declination, seats_at_50_50}:

| `|p_canonical(m) − p_forest(m)|` | Verdict on metric m |
|---|---|
| < 2 pp | Robust |
| 2–5 pp | Borderline (reported, not flagged) |
| ≥ 5 pp | Shifts materially; canonical claim qualified |

**Joint verdict:**
- If all four metrics are Robust or Borderline: the canonical claim survives. The audit's public copy is updated to add the sentence "*Forest-ReCom Phase A (100 k) yields percentile ranks within ±5 pp of canonical ReCom on every partisan metric.*"
- If any metric crosses the 5-pp threshold: the canonical claim is qualified. The audit's public copy is updated to add "*Forest-ReCom Phase A (100 k) shifts the minority's [metric] percentile from p[canonical] to p[forest]. The directional finding survives this shift on [N − 1] of 4 metrics, but the specific percentile claim on [metric] is sampler-dependent and should be read with this uncertainty.*" Phase B may then be filed as a separate pre-registration.

The pre-registration also commits to publishing the Phase A result regardless of direction. If the run is started, the result is reported, with no option to retract on the grounds that the result is unflattering.

## 8. Reporting commitments

1. **Results document at `findings/forest_recom_robustness.md`** — created within 7 days of Phase A run completion. Reports R-hat, n_eff, all four percentile comparisons, and the joint verdict per §7.

2. **Public-copy update to en.ts §5** — within 14 days of the findings doc. Adds the sentence from §7 (one version or the other) to `commission_split.finding3` or a dedicated `finding4`.

3. **Academic-report update to `reports/academic/report_academic.md` §5.2.7** — within 30 days. Adds a subsection citing this OSF prereg by registration number and the findings doc.

4. **OSF registration update.** This pre-registration is filed as a single OSF form before the script is executed. The form references this markdown document by commit hash. The execution log (printed seed, R-hat, n_eff) is appended to the OSF form within 24 hours of run completion.

## 9. What this pre-registration does *not* commit to

- Any additional sampler beyond Forest-ReCom Phase A. Multi-scale merge-split, constraint-set rejection sampling, and other variants are not in scope of this document.
- Any change to the substrate (shapefiles, VA-to-ED attribution, population basis).
- Any change to the four partisan-fairness metrics or their definitions.
- Any post-hoc adjustment of the 5-percentile-point threshold based on Phase A results.

## 10. Disclosure

The author has no funding, advisory, or political-staff relationship to any party, candidate, or commission member. The audit is independent personal research. This Forest-ReCom robustness check is being undertaken specifically to address a methodological concern raised in an internal review (the spanning-tree bias of ReCom samplers on highly-constrained substrates) and is pre-registered to prevent any post-hoc framing of the result.

---

*Document commit:* This file is committed to the public git repository at the time of OSF filing. The drand seed for `"forest_recom_robustness"` can be verified against the public beacon round 5,500,000 from any clone of the repository. The Forest-ReCom script (`analysis/scripts/forest_recom_ensemble.py`) is committed in the same commit as this document; if the document and the script ever drift, the document binds.

---

## Post-filing addendum (2026-07-10 — nothing above this line has been altered)

- Filed as OSF registration **he53s** (public) on 2026-07-10; executed the
  same day; results at `findings/forest_recom_robustness.md` (commit
  `63e5b692`); execution log appended to the OSF record per §8.4.
- Post-registration code changes (harness wiring, one crash fix between
  execution attempts, Wilson-vs-Aldous-Broder naming resolution, ESS-target
  disclosure semantics) are documented in
  `findings/pre_registration_amendment_log.md` **Amendment 13**. No sample
  existed before the registration or before the harness was finalised; the
  hypotheses, decision rule, run size, seeds, and output paths executed
  exactly as written above.
