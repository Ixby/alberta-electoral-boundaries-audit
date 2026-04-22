# Phase 4C Runbook

Executable playbook for the Vision-assignment session. Phase 4C prep is
complete; this document scopes the remaining Stage 3 - Stage 7 work.

## Inputs available (produced by `analysis/phase_4c_prep.py`)

| Path | Contents |
|---|---|
| `data/va_polygons_with_2023_votes.gpkg` | 4,765 VA polygons (EPSG:3400) with `va_ndp`, `va_ucp`, `va_other`, `parent_ed_2019`. Main Phase 4C substrate. |
| `data/hybrid_adjacent_vas.csv` | 1,438 VAs flagged for Vision review, with `majority_hybrid_candidate` and `minority_hybrid_candidate` columns. |
| `analysis/va_spatial_integrity_report.md` | Gate S3b (centroid-in-ED, 99.20%) and Gate S3c (vote conservation, 0.0000% diff) results. |

## Gate status at start of Phase 4C execution

- **S3a** (4,765 unique VAs in polls match 4,765 polygons): PASS (prior work)
- **S3b** (>=95% of VA centroids fall within their declared 2019 ED): **PASS** (99.20%)
- **S3c** (VA-aggregated EDay NDP/UCP/Other within 0.1% of poll-level totals): **PASS** (0.0000% for all three)

Substrate integrity is established. Phase 4C can start Stage 3 directly.

## Stage 3 - Vision-assignment scope

For each VA in `hybrid_adjacent_vas.csv`, determine which 2026 ED (majority
map AND minority map) the VA belongs to. Non-flagged VAs inherit the 2026
assignment of their parent 2019 ED trivially.

### Flagged VA breakdown

- Total flagged: **1,438** (30.2% of 4,765)
- Majority-hybrid only: 389
- Minority-hybrid only: 850
- Both majority AND minority: 199
- Parent 2019 EDs covered: 26

### Assignment method

For each flagged VA:
1. Load its polygon from `va_polygons_with_2023_votes.gpkg`.
2. Intersect against the proposed 2026 ED polygon from the relevant
   proposal shapefile (once the 2026 proposal shapefile is available).
3. If a single 2026 ED covers >=90% of the VA area, assign it directly.
4. Otherwise (VA straddles a 2026 boundary), invoke Vision (vision-enabled
   Claude) with the VA map tile + overlaid 2026 boundary to make the call.
5. Record `assigned_2026_majority` and `assigned_2026_minority` back onto
   the GPKG.

### Vision call budget estimate

- Assume ~30% of flagged VAs straddle a 2026 boundary (others clear a 90%
  overlap threshold).
- Expected Vision calls: **~430**.
- At ~500 tokens per call (image + short prompt + short response): **~215K
  tokens** for Stage 3 execution.

If budget tight, prioritize majority-hybrid VAs first (389) before
minority (850) - majority affects the 87-seat map everyone uses.

## Stage 4 - VA-level 2026 aggregation

Input: `data/va_polygons_with_2023_votes.gpkg` with Stage 3's `assigned_2026_*` columns filled.

Output: `analysis/phase_4c_va_to_2026_assignments.csv` -
4,765 rows, one per VA, with `parent_ed_2019`, `assigned_2026_majority`,
`assigned_2026_minority`, `va_ndp`, `va_ucp`, `va_other`.

## Stage 5 - 2026 ED synthetic vote totals

Group VA-level votes by `assigned_2026_majority` and sum NDP/UCP/Other.
Repeat for minority map.

Output: `analysis/phase_4c_2026_synthetic_totals.csv` (one row per 2026 ED
in each map, with synthetic 2023 EDay two-party totals).

## Stage 6 - Packing & cracking re-run

Re-execute `analysis/v0_2_packing_cracking_analysis.py` with the
VA-resolution synthetic totals in place of the prior 2019-ED-proportional
estimates. Diff the efficiency gap / mean-median / partisan-bias metrics
against the v0.2 results.

Output: `analysis/phase_4c_gerrymander_comparison.md` with v0.2 vs 4C
metric deltas and significance.

## Stage 7 - Monte Carlo CIs

Re-run `analysis/v0_3_monte_carlo_ci.py` on the VA-resolution data to get
confidence intervals around the Stage 6 metrics. Budget ~2,000 draws.

Output: `analysis/phase_4c_mc_intervals.md`.

## Notes for the executor

- Attribution method used in Stage 2: **equal-weight split** of each
  Election Day poll's votes across VAs listed in its `voting_areas` field.
  Advance / Mobile / Special Ballot excluded. Poll-level totals conserved
  exactly (0.0000% diff).
- 38 VAs (0.80%) have centroids that fall outside their declared 2019 ED.
  These are almost certainly boundary-adjacent polygons where the centroid
  nudges across a shared ED line; the declared ED is canonical because it
  comes from the poll record, not the geometry. Flag them in Stage 3 but
  do not treat as errors.
- The `hybrid_adjacent_vas.csv` scoping uses token-overlap for (NEW) 2026
  EDs in the minority map (i.e. where no existing 2019 ED name is listed
  as the source). Generic tokens ('Calgary', 'Edmonton', directionals)
  are filtered out so the candidate list stays tight. If Stage 3 discovers
  a VA near a (NEW) boundary that isn't in the flagged list, add it
  manually.
