# Drain Metric v2 — Improvement Plan

*Document status: pre-registered design*  
*Date: 2026-05-06*  
*Scope: `analysis/scripts/neighbour_drain_adjacency.py` and successors*

---

## Background

The §5.3.5 neighbour-drain test was designed to detect pack-and-crack adjacency:
a "packed" ED (losing party over-represented) directly adjacent to a "cracked" ED
(win margin narrow enough to suggest votes were redistributed there).

### What the original v0_8 test did

- Binary threshold gate: losing-party surplus ≥ 0.15 AND adjacent winning margin ≤ 0.05
- Coupled = same losing party in both EDs
- Pre-registered pass criterion: minority coupled count ≤ 1.5× majority coupled count
- Substrate: DPG v0_2 (majority) and v0_8 (minority), adjacency buffer 600 m
- Surplus formula: `s = max(max_votes - floor(N/2) - 1, 0) / N`
- Margin formula: `m = |ndp - ucp| / N`

### What v0_10 validation revealed

1. **Geometry dependency**: DPG v0_2/v0_8 had ~37% mean IoU vs official shapefiles.
   The v0_8 flip (minority 1.33× PASS) was caused by broken adjacency, not real signal.

2. **Official geometry result** (t535_neighbour_drain_official.py):
   - Majority: 47 coupled, Minority: 21 coupled, Ratio: 0.45× → PASS
   - Direction *inverted* from audit finding (minority now lower, not higher)
   - This does not invalidate the test; it confirms the v0_8 substrate was the problem

3. **Binary threshold creates resolution cliff**: A coupled pair at surplus=0.151 scores
   the same as surplus=0.499. This loses intensity information.

4. **No baseline calibration**: There is no null distribution — we don't know whether
   47 coupled signals in the majority map is remarkable or expected by chance.

5. **Adjacency forcing**: Some ED pairs are geographically constrained to be adjacent
   regardless of commission intent. A drain signal on forced adjacencies carries less
   weight than one on pairs where non-adjacency was a plausible commission choice.

---

## Infrastructure Constraint

The existing MCMC ensemble (`data/outputs/mcmc/simulated_ensemble_raw_samples_100k.csv`,
100k rows) stores **only aggregate metrics**: efficiency_gap, mean_median, declination,
seats_at_50_50, ucp_seats, n_districts, ucp_vote_share, step.

**No per-plan VA assignments are stored.** This means ensemble-based drain calibration
cannot use the existing MCMC output directly — it would require re-running MCMC with
assignment output enabled (expensive) or using a label-shuffling null (practical).

All phases below are designed with this constraint in mind.

---

## Improvements

### Phase A — Continuous Intensity Score (immediate, no ensemble needed)

Replace the binary gate with a continuous intensity product per coupled pair:

```
intensity(X, Y) = max(0, s_X - s₀) × max(0, m₀ - m_Y)
```

Where:
- `s_X` = losing-party surplus in packed ED X
- `s₀` = surplus threshold (currently 0.15)
- `m_Y` = winning margin in cracked ED Y
- `m₀` = margin threshold (currently 0.05)

Aggregate: `drain_score(map) = Σ intensity(X, Y)` over all coupled adjacent pairs.

This preserves the existing threshold logic as a gate (intensity = 0 if either condition
fails) but weights signals by how extreme they are. A surplus of 0.49 in a map with
margin 0.01 scores ~10× a surplus of 0.16 with margin 0.04.

**Implementation**: Modify `chain_signals()` in `neighbour_drain_adjacency.py` to
return intensity alongside the binary coupled flag. Add `drain_score` to the summary
output.

**Output**: Side-by-side binary count vs continuous drain score for all four map
substrates (2019, majority, minority, and any future v11).

**Effort**: 1-2 hours, single-file edit.

---

### Phase B — Label-Shuffling Null Distribution (moderate effort)

Build a null distribution by permuting which ED gets which vote vector while keeping
adjacency structure fixed.

**Rationale**: The MCMC ensemble doesn't store VA assignments. Label shuffling is the
practical alternative — it asks: "if vote totals were the same but randomly distributed
across the ED geography, how many coupled drain signals would we expect?"

**Procedure**:
1. Take official adjacency graph (239 edges per map, from t535 output)
2. Take official vote totals per ED (va-aggregated, from t535 output)
3. For each of N=10,000 permutations:
   a. Randomly shuffle which ED name gets which (ndp, ucp) vote vector
   b. Recompute surplus, margin, and winning party for each ED
   c. Count coupled chain signals (binary, same threshold as original)
   d. Also compute continuous drain score
4. Record count and drain score per permutation
5. Compute z-score and percentile for the real maps against this null

**Output**: Per-map z-score and percentile rank; histogram of null distribution;
significance threshold at p < 0.05 (2.5th / 97.5th percentile of null).

**Limitation**: Label shuffling preserves the marginal vote distribution but not
spatial autocorrelation. Two geographically adjacent EDs that happen to be politically
similar in the real map would be decoupled. This makes the null slightly conservative
(easier to look significant than a full spatial null would be). Acceptable for a first
baseline.

**Effort**: 4-6 hours. New script `scripts/drain_label_shuffle_null.py`.

---

### Phase C — VA-Level Contiguity-Respecting Shuffles (high effort, if warranted)

Build a spatially-aware null by shuffling VAs between adjacent EDs rather than swapping
entire ED vote vectors.

**Procedure**:
1. For each shuffle iteration:
   a. Pick a random boundary ED pair from the official adjacency graph
   b. Identify VAs within 200m of the shared border
   c. For each boundary VA, with probability 0.5, swap its ED assignment
   d. Recompute ED vote totals from VA assignments
   e. Count drain signals
2. Run 10,000 iterations with random walk on VA assignments

**Why this is better**: Respects the spatial structure of VA polygons. Produces
maps with the same number of EDs and the same geographic footprint, with small
local perturbations that resemble commission-level edits. The null is closer to
"what would we see if the commission had drawn slightly different borders?"

**Why this is harder**: Requires the full VA-to-ED assignment table (available
after v11 construction). Also requires that each shuffled map remain valid
(EDs must stay contiguous — VA swaps can create disconnected EDs if not careful).

**Effort**: 1-2 weeks. Depends on v11 completion.

**Recommended**: Defer until v11 is available. Use Phase B null as interim.

---

### Phase D — Full MCMC Re-Run with Assignment Output (expensive)

Re-run the gerrychain ensemble but modify it to save per-plan VA-to-ED assignments
alongside aggregate metrics.

**What this enables**: True ensemble drain calibration — each of 100k simulated maps
has its own adjacency structure derived from its actual VA assignments. This eliminates
the label-shuffling approximation entirely.

**Why deferred**: The existing ensemble run took significant compute time. Re-running
it is a separate project decision. Storage cost: each plan's VA-to-ED mapping is
4,765 integers × 100k plans ≈ 2 GB at minimum.

**Effort**: Depends on gerrychain infrastructure availability. Likely requires PO
decision on compute budget before starting.

---

## Phase E — Boundary Specificity Weighting

Weight each chain signal by how often the same pair fires in the null ensemble.

For each coupled pair (X, Y):
```
specificity_weight(X, Y) = 1 - P(coupled signal on (X,Y) | null)
```

Where P is the frequency in the label-shuffling null (Phase B).

Pairs that fire frequently in random permutations — because they are geographically
forced or because both EDs happen to have similar vote distributions — receive low
weight. Pairs that are rare in the null receive high weight.

**Aggregated weighted drain score**:
```
weighted_drain(map) = Σ intensity(X,Y) × specificity_weight(X,Y)
```

**Requires Phase B as a prerequisite.** Write as extension to `drain_label_shuffle_null.py`.

---

## Execution Sequence

| Phase | Depends On | Effort | Priority |
|-------|-----------|--------|----------|
| A — Continuous intensity | Nothing | 1-2 hr | **Now** |
| B — Label shuffle null | Phase A | 4-6 hr | **Next session** |
| E — Specificity weighting | Phase B | 2 hr | After B |
| C — VA-level shuffles | v11 + Phase B | 1-2 wk | After v11 |
| D — MCMC re-run | PO decision | TBD | Deferred |

---

## Pre-Registered Outcomes

Run Phase A and B on the four existing substrates (2019-inherited, majority DPG,
minority DPG, majority official, minority official) before looking at any results.
Record predictions here before unblinding:

**Prediction A**: Continuous drain score will rank official majority > official minority
(consistent with the binary result 47 vs 21).

**Prediction B**: Label-shuffling null will show that both official map scores are
within the null distribution (since the binary ratio is 0.45×, well below 1.5×).
If the majority score is a high-percentile outlier in the null, that is a new positive
finding worth reporting.

**Prediction C**: After specificity weighting, the Cochrane-Springbank → Calgary-Symons
Valley / Calgary-North cluster will be downweighted (these are geographically constrained
pairs) and the Strathcona-Sherwood Park cluster will be upweighted (less topologically
forced).

---

## Metric Validity Assessment

### Is draining a valid metric?

**Yes, with caveats.**

Draining is a real gerrymandering archetype. The spatial coupling between packed and
cracked EDs is a genuine forensic signal — it is what distinguishes pack-and-crack from
pack-and-dilute, which operates at a map-wide level rather than locally.

The pre-registered §5.3.5 test is appropriately conservative (ratio ≤ 1.5× rather than
a strict equality test). The finding on official geometry (0.45×, both maps well within
expected range) is a clean PASS and is interpretable.

**Caveats:**

1. **Resolution**: Binary thresholds lose intensity information. Phase A addresses this.

2. **No baseline**: Without a null, we cannot say whether 47 coupled signals is
   "a lot." Phase B addresses this.

3. **Geographic forcing**: Some adjacencies exist regardless of commission intent.
   Phase E addresses this.

4. **Vote estimation vs actual**: The v0_8 drain test used vote totals estimated from
   VA centroids via `packing_cracking_analysis.py`. The t535 re-run uses actual
   2023 VA vote totals aggregated to official EDs, which is the correct approach.

5. **Two-party simplification**: The metric uses NDP and UCP votes only, dropping
   minor-party and spoiled ballots. This is defensible for Alberta provincial context
   but should be disclosed.

**Summary**: The methodology is sound. The v0_8 result was noise from broken geometry,
not metric instability. On clean data, the metric gives a stable, interpretable result.

---

## Files

| File | Purpose |
|------|---------|
| `analysis/scripts/neighbour_drain_adjacency.py` | Current v1 implementation (modify for Phase A) |
| `analysis/scripts/drain_label_shuffle_null.py` | NEW — Phase B + E |
| `analysis/methodology/drain_v2_plan.md` | This document |
| `dpg_validation/scripts/t535_neighbour_drain_official.py` | Official-geometry re-run (complete) |
| `dpg_validation/outputs/t535_neighbour_drain_official.csv` | Official-geometry results (complete) |
