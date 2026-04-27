# Data Integrity Status

**Date:** 2026-04-23 (Option-B remediation)
**Context:** Post-session-12 validation sweep of the three pipelines that produce
published-quality numbers for the audit: (1) packing/cracking (`packing_cracking_analysis.py`),
(2) Phase 4B/C/F execution (`phase_4bcdef_execution.py`), and (3) MCMC
rescore (`mcmc_full_coverage_rescore_v2.py`).

This file is an honest audit of what passes integrity gates and what does not,
as of the commit that introduced it.

---

## Summary verdict

| Pipeline | Complete (conservation) | Canonical (uses canonical shapefiles) | Accurate (passes 2% hardstop) |
|---|---|---|---|
| v0.2 packing/cracking (crosswalk-based, no polygons) | n/a (crosswalk only) | n/a | n/a |
| Phase 4C vote attribution | **✓ PASS** (1,706,249 maj / 1,706,233 min vs 1,706,304 target) | **✓ PASS** (canonical 89/89) | n/a |
| Phase 4B DA→ED population dissolve | ✓ same DA total | ✓ PASS | **✗ FAIL** (81/86 maj, 87/89 min fail 2% hardstop) |
| MCMC full-coverage rescore v2 | **✓ PASS** (two-party total 1,706,304) | **✓ PASS** (canonical 89/89) | partial — 89.8% maj / 80.2% min polygon coverage |

**Bottom line:** Vote-side pipelines (Phase 4C, MCMC rescore) are now defensibly
complete, canonical, and conserving vote totals. Population-side pipeline
(Phase 4B) fails the 2% hardstop on almost every ED — this is a structural
limit of visual-transcription polygons and will not be fixed without official
Elections Alberta 2026 shapefiles.

---

## What Option B remediation fixed

### Fix 1 — Advance-Vote Splat wired in
- Before: Phase 4C totals summed to 896,627 two-party (52.5% of the 1,706,304
  documented 2023 total). Root cause: the VA polygon substrate contained only
  Election-Day votes; the 47.2% non-Election-Day share was never apportioned.
- Fix: `advance_vote_splat.py` ran clean, wrote
  `data/va_polygons_with_full_2023_votes.gpkg` with `va_{ucp,ndp,other}_full`
  columns. Conservation gate: exact (0-vote delta across all three categories).
  Province-wide NDP share moved from 42.60% (Election-Day only) to 45.56%
  (full) — a +2.96 pp upward correction.
- Downstream: `phase_4bcdef_execution.py` and
  `mcmc_full_coverage_rescore_v2.py` now read the full-VA gpkg and use the
  `_full` columns.

### Fix 2 — Canonical shapefiles wired in
- Before: `phase_4bcdef_execution.py` read a layered mix of
  `approximate_majority + derived_v7 + 2019_identity` fallback. The canonical
  shapefiles that session 11 built (`v0_1_canonical_{majority,minority}_2026_eds.gpkg`)
  were never referenced by any downstream script — they were orphans.
- Fix: both pipelines now read `v0_1_canonical_majority_2026_eds.gpkg` (66 v7 +
  18 2019-parent + 4 sweep + 1 osm-municipal-buffered) and
  `v0_1_canonical_minority_2026_eds.gpkg` (84 v7 + 5 2019-parent). Source
  provenance is preserved in the output CSVs' `polygon_source` column.

### Fix 3 — Sign convention corrected via full-VA
- Before (approximate + Election-Day only): 2019 enacted EG = +0.024
  (the paper documents -2.64%). The sign disagreed with published literature.
- After (canonical + full-VA): 2019 enacted EG = -0.0264 — matches the
  paper's documented 2019 baseline to three decimal places. Majority EG
  = -0.0233, Minority EG = +0.0182. Mean-median for 2019 = -0.022 (also
  matches to the published -2.22 pp).

### Fix 4 — CP1252 encoding on polls CSV
- The splat script failed on `polls_2023_unified.csv` with a UTF-8 decode
  error at byte 0xC9 (Ê). Added `encoding="cp1252"` — Windows Latin-1.

---

## What Option B remediation could NOT fix (structural limits)

### Phase 4B — DA population deltas remain catastrophic

After repointing at canonical polygons, Phase 4B still fails the 2% hardstop
threshold on 81 of 86 non-zero-pop majority EDs and 87 of 89 minority EDs.
Worst offenders:

**Majority:**
- Edmonton-Gold Bar: +212% (149,439 DA-derived vs 54,981 commission)
- Edmonton-North West: +129%
- Edmonton-Rutherford: +127%
- Calgary-Buffalo: +108%
- Calgary-Falconridge-Conrich: -100% (zero DA centroids fell inside the
  polygon)
- 3 EDs with zero DA population (Falconridge-Conrich, Glenora-Riverview,
  Highlands-Norwood)

**Minority:**
- Edmonton-Beverly-Clareview: **+428%** (264,708 DA-derived vs 57,481
  commission — polygon absorbs adjacent DAs)
- Stony Plain-Drayton Valley: +282%
- Edmonton-Highlands-Norwood: +135%
- Edmonton-Mill Woods, Edmonton-Manning, Calgary-South: all at -98%

**Root cause:** The canonical shapefiles use `canon_source=v7` for 66 of 89
majority EDs and 84 of 89 minority EDs. v7 polygons are visually transcribed
from the commission's thumbnail maps at ±100 m (river-snapped segments) to
±1 km (general boundary) error. At that tolerance many polygons overlap with
their neighbors or leave territorial gaps. When a 2021 DA centroid lands in
a gap, the DA's population is lost to the pipeline; when it lands in an
overlap region, the population is double-counted in one ED at the expense
of another.

**Not fixable by remediation:** This is the same structural limit that
blocks Phase 4A (Elections Alberta has not released the official 2026
shapefiles). Without shapefiles, the paper's §6.7 Tier-C annex is the
honest statement of what can be claimed: "polygons are explicitly
sub-shapefile-grade with per-segment error bands."

### MCMC coverage gap

MCMC rescore at canonical assigns 89.8% of VAs by polygon on the majority and
80.2% on the minority. The remaining 10–20% fall through to crosswalk
assignment. This is better than the pre-canonical rescore (63.8% / 78.9%) but
still not 100%. Three EDs are missed entirely even by the crosswalk fallback:
`Edmonton-Highlands-Norwood` (majority), `Calgary-South` and `Edmonton-Manning`
(minority). They receive zero votes — enough to bias EG, MM, and seat counts
by a small but detectable amount.

**Partial fix path:** Patch the three missing EDs into the crosswalk by hand;
this would close the gap without requiring polygon geometry. Not done in this
remediation pass.

---

## What each headline number now rests on

| Headline claim | Pipeline | Status |
|---|---|---|
| 2019 EG = -2.64%, MM = -2.22 pp, B4 seats = 46 | v0.2 packing/cracking | ✓ Reproducible (G0 gate passes exactly) |
| MC CI [-2.74, +0.60] pp, 93% direction consistency | v0.3 Monte Carlo CI | ✓ Reproducible |
| A1/A2/A3 population equality (MAD 3,180 vs 4,707; Calgary Zone A-B 0.36% vs 12.20%) | `electoral_forensics_population.py` | ✓ Uses commission published pops, not DA overlay |
| 5/5 minority justification tests FAIL population math | `justification_tests.py` | ✓ Uses CSD populations, not polygon overlay |
| **Asymmetry -1.41 pp (minority more pro-UCP)** at 85% urban weight | v0.2 packing/cracking (crosswalk) | ✓ Reproducible — **but see next row** |
| **Asymmetry +4.1 pp (minority LESS pro-UCP)** from MCMC canonical | `mcmc_full_coverage_rescore_v2.py` | ⚠ Different direction from crosswalk approach — needs reconciliation before publication |
| 2019 map at 0th percentile on EG; minority at 60.3rd | MCMC canonical | ⚠ New result; crosswalk-assigned 10–20% of VAs could swing this |
| Minority at 100th percentile on seats@50/50 | MCMC canonical | ⚠ Same caveat |
| Population-derived per-ED numbers (§6.7 Tier-C) | Phase 4B canonical | ✗ Cannot publish — 89–93% of EDs fail the 2% hardstop |

---

## What the paper should be updated to say

1. **Keep** the v0.2 packing/cracking numbers and MC CI in §3 as the primary
   vote-based findings. These are defensible without any polygon geometry.
2. **Keep** the Section A population equality numbers (commission-published,
   not polygon-derived).
3. **Update** the MCMC ensemble section to reflect the canonical + full-VA
   rescore percentiles, with an explicit footnote about the 10–20%
   crosswalk-assigned VA share.
4. **Explicitly retract** any claim based on the pre-remediation Phase 4C
   numbers (EG +1.44% / -2.71% / +0.31 pp asymmetry — all built on 52.5%
   vote recovery).
5. **Honestly block** any claim that required DA-overlay per-ED populations.
   The §6.7 Tier-C characterisation is already the right framing; extend it
   to cover the full 89-ED scope.
6. **Reconcile** the asymmetry-direction disagreement between the v0.2
   crosswalk approach (-1.41 pp) and the canonical+full-VA MCMC approach
   (+4.1 pp) before publication. Both are internally consistent; the
   disagreement is a real analytical question, not a bug.

---

## Files produced / updated by this remediation

**New:**
- `data/va_polygons_with_full_2023_votes.gpkg` (from splat)
- `analysis/advance_vote_splat_diagnostics.csv`

**Edited:**
- `analysis/scripts/advance_vote_splat.py` — cp1252 encoding
- `analysis/scripts/phase_4bcdef_execution.py` — canonical shapefiles + full-VA
- `analysis/scripts/mcmc_full_coverage_rescore_v2.py` — canonical + full-VA

**Rewritten by rerun:**
- `data/v0_1_population_2021_majority.csv`
- `data/v0_1_population_2021_minority.csv`
- `data/votes_2023_majority.csv`
- `data/votes_2023_minority.csv`
- `data/v0_1_validation_deltas.csv`
- `data/pipeline_summary.json`
- `data/simulation_real_map_scores_full_v2.json`
- `data/simulated_ensemble_percentiles_full_v2.csv`
