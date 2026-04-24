---
name: Phase 4C execution log
description: Step-by-step record of the Phase 4C VA-level vote attribution execution, including what worked, what didn't, and what remains blocked.
---

# Phase 4C execution log

**Date:** 2026-04-23
**Session:** 11
**Executor:** parent session (direct execution after two sub-agent failures)

## Prior attempts

1. **Session 10, D5 sub-agent (first attempt):** BLOCKED by sandbox
   restrictions. Sub-agent could not run Python. Zero files created.
   Substrate integrity verified (S3a/b/c pass) before hitting the wall.

2. **Session 11, D5 sub-agent (second attempt):** BLOCKED by Bash
   permission denial. Same environment restriction. Zero files created.

3. **Session 11, parent session (this attempt):** Succeeded. All stages
   completed. Two iterative passes to fix assignment logic.

## Execution steps

### Pass 1: Crosswalk-first approach (abandoned)

Built manual `MAJORITY_2019_TO_2026` and `MINORITY_2019_TO_2026`
crosswalk dictionaries. Results: majority 85 EDs, minority 84 EDs.
Multiple 2019 ED names leaked through (Calgary-Foothills, Calgary-Peigan,
etc.) because the manual crosswalk missed splits and unmapped EDs.

### Pass 2: Spatial-first approach (final)

Restructured to use centroid-in-polygon spatial join as the primary
assignment method, with fallback to flagged-VA candidate column and
then to an inverted v0.2 crosswalk.

**Assignment method breakdown:**

| Method | Majority | Minority |
|---|---|---|
| Spatial (centroid-in-polygon) | 3,041 | 3,707 |
| Candidate (flagged VA column) | 327 | 538 |
| Crosswalk (inverted v0.2 map) | 1,027 | 444 |
| Unresolved (parent name leaked) | 370 | 76 |
| **Total** | **4,765** | **4,765** |

**Result:** 86 unique 2026 EDs for each map (expected: 89). Perfect
vote conservation (zero drift).

### Why 3 EDs are missing per map

The approximate 2026 shapefiles contain only Tier A (inherited 2019
geometry) polygons. When a 2019 ED splits into two 2026 EDs (e.g.,
Calgary-Beddington → Calgary-Beddington + Calgary-Nose Creek), both
new EDs share the same parent polygon. The spatial join assigns all
VAs to the parent's 2026 name; the sibling ED gets zero VAs because
its polygon is not distinct from the parent's.

Without 2026 shapefiles, the split boundary is unknown.

## Output files

| File | Rows/size | Contents |
|---|---|---|
| `analysis/phase_4c_va_to_2026_assignments.csv` | 4,765 rows | Per-VA assignment with method and confidence |
| `analysis/phase_4c_2026_synthetic_totals.csv` | 172 rows | Per-ED vote totals (86 majority + 86 minority) |
| `analysis/reports/phase_4c_gerrymander_comparison.md` | — | v0.2 vs 4C comparison with methodological notes |
| `analysis/scripts/v0_1_phase_4c_va_attribution.py` | ~340 lines | Execution script |

## Gates

| Gate | Status | Detail |
|---|---|---|
| S3a (VA count match) | PASS (prior) | 4,765 VAs |
| S3b (centroid containment) | PASS (prior) | 99.20% |
| S3c (vote conservation) | PASS (prior) | 0.0000% |
| Vote conservation (Phase 4C) | PASS | 0.0 drift |
| ED count (89 expected) | PARTIAL | 86 resolved per map |

## Remaining work (shapefile-gated)

1. Full 89-ED resolution requires 2026 shapefiles (Track A)
2. Full-vote attribution (advance/mobile/special apportionment) requires
   Stage 7 per the runbook, which needs the spatial assignments to be
   complete (currently partial)
3. Phase 5 (B5 GerryChain ensemble, C1 Polsby-Popper, C2 Reock) also
   requires shapefiles
