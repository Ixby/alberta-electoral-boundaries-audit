# v0_1 Topology Cleanup — eliminating inter-ED DPG polygon overlap

**Scope.** The canonical v0_1 Derived Provisional Geometry (DPG) files
`data/v0_1_canonical_{majority,minority}_2026_eds.gpkg` were traced from
600-DPI commission thumbnails; tracing error put some polygons across
shared boundaries. Measured overlap totals:

* **Majority:** 2,753.6 km² of inter-ED overlap across 86 pairs; 1,011
  Voting Areas (VAs) had raw area-weighted total DPG coverage > 1.0
  (maximum 3.00×).
* **Minority:** 16,733.7 km² of inter-ED overlap across 96 pairs; 1,722
  VAs had raw total DPG coverage > 1.0 (maximum 3.95×).

Under MAUP area-weighted attribution (`assignment_va_attribution_maup.py`),
this overlap forced the script to renormalise per-VA weights and pushed
Stony Plain-Drayton Valley to a **24.8 pp UCP→NDP flip** on the minority
map — a Tier-C transcription artefact, not a real commission intent. The
MAUP-v1 measurement also reported minority EG = -2.14 % while the
centroid-in-polygon baseline (§5.2.7 headline) reported minority EG =
+1.82 %. This gap was the immediate driver of the paper's §5.2.7
crosswalk-vs-spatial residual disagreement.

This document reports the topology cleanup procedure, validates it against
three gates (no-overlap, no-erased, area-conservation), re-runs MAUP
against the cleaned DPGs, and gives a suggested paper-ready paragraph
for §5.2.7.

## Method

**Script:** `analysis/scripts/topology_cleanup.py` (521 lines).

For each map independently, the pipeline:

1. **Detect overlaps.** Pairwise intersection of every polygon with every
   other polygon via `GeoDataFrame.sindex.query`; retain only polygonal
   components with area ≥ 1 m² to filter numeric noise.
2. **Precedence resolution.** For each overlap region between polygons A
   and B, assign it to whichever has stronger source evidence:

   | Rank | `canon_source` | Rationale |
   |------|----------------|-----------|
   | 5 | `sweep` | Population-calibrated parametric sweep |
   | 4 | `osm-municipal-buffered` | OSM-anchored (e.g., Edmonton-Beaumont) |
   | 3 | `2019-parent` | Tier-A shapefile inheritance |
   | 1 | `v7` | Visually transcribed (lowest confidence) |

   Tie-breaker (both v7): smaller polygon area wins (concentrated v7 is
   more likely transcription-accurate than sprawling v7).

3. **First subtraction pass.** Each loser's geometry is reduced by the
   union of the overlap regions it lost.

4. **Anti-erasure safeguard.** If subtraction would leave the loser with
   < 10 % of its original area, the loser is instead preserved as-is and
   flagged. This prevents a sprawling sweep or 2019-parent polygon from
   swallowing a correctly-transcribed v7 polygon whole. In the majority
   map, this triggered for 6 EDs (e.g., Calgary-Lougheed, which sweep's
   High River-Vulcan-Siksika polygon covered completely); in the minority
   map, for 1 ED (Calgary-Falconridge).

5. **Second pass (winner-side subtraction).** For each protected loser,
   its preserved geometry is subtracted from every other cleaned polygon
   that still intersects it, unless that would erase the other polygon.

6. **Third pass (centroid-proximity split).** Any residual overlap is
   split between the two remaining contestants by centroid distance of
   each sub-polygon, subject to a 5 % survival floor.

7. **Fourth pass (unconditional resolution).** Any still-residual overlap
   is assigned deterministically to whichever original-polygon centroid
   is closer to the contested region's centroid, without a survival
   floor. This final pass guarantees the no-overlap gate passes.

## Validation

Three gates:

* **No-overlap.** Residual inter-ED intersection ≤ 1000 m² across all
  pairs.
* **No-erased.** No ED's cleaned area < 1 m².
* **Area-conservation.** Cleaned provincial total area matches the
  dissolved-union area of the original polygons within 0.1 %. (Note:
  the naive `geometry.area.sum()` of the original files is inflated by
  overlap double-counting; the union-dissolve total is the true
  provincial footprint, which is what cleaned polygons should sum to.)

**Result:**

| Gate | Majority | Minority |
|------|----------|----------|
| No-overlap (residual km²) | 0.0000 | 0.0000 |
| No-erased | PASS (89/89) | PASS (89/89) |
| Area-conservation (drift vs union) | +0.0000 % | +0.0000 % |

**All gates pass on both maps.**

Overlap resolved:
* Majority: 2,753.6 km² → 0.0 km² (100 % resolved)
* Minority: 16,733.7 km² → 0.0 km² (100 % resolved)

Net per-side ED area delta is negative (49 majority EDs lost territory,
0 gained; 45 minority EDs lost, 0 gained) because the losers only ever
shrink in this algorithm — the overlap they gave up was double-counted
against the winner, so "winner area" doesn't grow beyond the union.

## Outputs

| File | Purpose |
|------|---------|
| `data/v0_2_canonical_majority_2026_eds_topoclean.gpkg` | Cleaned majority DPG |
| `data/v0_2_canonical_minority_2026_eds_topoclean.gpkg` | Cleaned minority DPG |
| `analysis/reports/topology_cleanup_log.csv` | Per-ED before/after areas |
| `analysis/reports/topology_cleanup_summary.json` | Validation gates + stats |
| `data/v0_2_votes_2023_majority_maup.csv` | MAUP-v2 per-ED majority votes |
| `data/v0_2_votes_2023_minority_maup.csv` | MAUP-v2 per-ED minority votes |
| `analysis/reports/assignment_va_to_2026_assignments_maup_v2.csv` | Per-VA attribution |
| `analysis/reports/v0_2_phase4c_maup_summary.json` | MAUP-v2 summary |

## Results — MAUP re-run on cleaned DPGs

`analysis/scripts/assignment_va_attribution_maup_v2.py` re-runs the
area-weighted attribution pipeline against `v0_2_*_topoclean.gpkg`.

### Three-measurement comparison table

| Measurement | Majority EG | Minority EG | Asymmetry (min − maj, pp) | NDP/UCP seats maj | NDP/UCP seats min |
|---|---:|---:|---:|---:|---:|
| Centroid-in-polygon (§5.2.7 headline) | −2.33 % | +1.82 % | +4.15 | — | — |
| MAUP-v1 (raw canonical, overlap present) | −3.25 % | −2.14 % | +1.12 | 38 / 51 | 32 / 57 |
| **MAUP-v2 (topology-cleaned)** | **−2.35 %** | **+1.00 %** | **+3.35** | **40 / 49** | **33 / 56** |
| Δ (v2 vs v1) | +0.91 pp | +3.14 pp | +2.23 pp | +2 NDP | +1 NDP |

### Stony Plain-Drayton Valley flip (minority map)

| Measurement | UCP votes | NDP votes | NDP share | Winner |
|---|---:|---:|---:|---|
| MAUP-v1 (raw) | 82,382 | 112,731 | 57.78 % | NDP |
| **MAUP-v2 (clean)** | **32,579** | **28,490** | **46.65 %** | **UCP** |

The 24.8 pp flip is resolved. Under MAUP-v2 Stony Plain-Drayton Valley
reverts to UCP with a plausible 46.65 % NDP share (consistent with a
semi-rural Alberta riding), and its vote totals drop from an inflated
~195k back to a realistic ~61k two-party — because it no longer scavenges
area-weighted shares from 20+ overlapping metropolitan Edmonton EDs.

### Coverage diagnostics

Provincial area coverage of the VA substrate is essentially unchanged
(majority: 90.91 % → 90.90 %; minority: 89.59 % → 89.55 %). This is
expected: coverage is computed with per-VA sums clipped at 1.0, so
overlap-driven inflation was already clipped away in v1. What the
cleanup changes is *how* the 90 %-ish covered area is distributed —
every km² of VA is now attributed to exactly one (and only one) ED,
which is what the MAUP model assumes and which v0_1 silently violated.

## Interpretation — effect on §5.2.7

The §5.2.7 disagreement the paper currently reports is between:

* the crosswalk (aggregation) asymmetry of roughly **−1.42 pp**; and
* the centroid-spatial asymmetry of roughly **+4.15 pp**.

MAUP-v1 appeared to narrow this gap (reported asymmetry +1.12 pp). After
topology cleanup, MAUP-v2 reports **+3.35 pp** — much closer to the
centroid baseline.

This reverses the tentative interpretation of MAUP-v1. **The MAUP-v1
"narrowing" was itself a Tier-C DPG-topology artefact**: double-counted
VA area inflated minority-map NDP share (driving minority EG from +1.82
toward −2.14) and hid behind the appearance of convergence. Once
overlap is resolved, MAUP-v2 behaves as a lightly smoothed variant of
the centroid-spatial measurement — which is what one expects when
polygons are topologically sound and VAs cross boundaries only at true
edges.

**Verdict on §5.2.7.** Topology cleanup does **not** close the §5.2.7
crosswalk-vs-spatial residual gap below 1 pp. The cleaned spatial
measurement (MAUP-v2 asymmetry = +3.35 pp) remains a full 4.77 pp
distant from the crosswalk (−1.42 pp). Removing the DPG-tracing
artefact moves the spatial measurement *back toward* the centroid
baseline, not toward the crosswalk one. The §5.2.7 disagreement is
therefore **not** a Tier-C geometry artefact — it is a real,
measurement-level divergence between aggregation (crosswalk) and
spatial (centroid/MAUP) attribution, likely reflecting fundamental MAUP
sensitivity to boundary-straddling VAs. The paper's current framing of
§5.2.7 as a "disagreement one should flag, not resolve" is vindicated
by this test.

The Stony Plain-Drayton Valley flip resolving cleanly (24.8 pp UCP→NDP
under v1 → UCP again under v2) is, however, a concrete paper-relevant
win: any future per-ED competitiveness claims sourced from MAUP should
use v0_2 cleaned geometry.

## Suggested paper-ready paragraph (§5.2.7 insertion)

> *Topology cleanup robustness check (fourth measurement layer).* The
> MAUP area-weighted result above depends on the v0_1 canonical
> Derived Provisional Geometry (DPG) polygons being topologically
> sound. In fact they are not: tracing error from the 600-DPI
> commission thumbnails produced 2,754 km² of inter-ED overlap on the
> majority map and 16,734 km² on the minority map (96 overlapping
> pairs), with 1,011 majority VAs and 1,722 minority VAs falling in
> regions claimed by two or more electoral divisions. To isolate the
> contribution of this transcription artefact from any genuine spatial
> signal we ran a precedence-based topology cleanup
> (`topology_cleanup.py`) that awards each overlap region to the
> ED with stronger source evidence
> (`sweep > osm-municipal-buffered > 2019-parent > v7`, with
> smaller-area v7 winning ties) and re-ran MAUP against the cleaned
> geometry. After cleanup the majority efficiency gap changes
> trivially (−3.25 % → −2.35 %), the minority efficiency gap reverts
> to approximately the centroid baseline (−2.14 % → +1.00 %), and the
> headline asymmetry changes sign relative to MAUP-v1's narrowing,
> moving from +1.12 pp back to +3.35 pp — within 0.8 pp of the
> centroid-in-polygon baseline of +4.15 pp. The one per-ED flip driven
> by the MAUP-v1 overlap artefact (Stony Plain-Drayton Valley, which
> scavenged apportioned votes from 20+ metropolitan Edmonton EDs) is
> resolved: the seat returns UCP with a 46.7 % NDP share rather than
> the MAUP-v1 flip to NDP at 57.8 %. We therefore *do not* claim MAUP
> as evidence of convergence between the aggregation and spatial
> measurements in §5.2.7: once polygon topology is corrected MAUP
> behaves as a lightly smoothed variant of the centroid-spatial
> baseline, and the residual ~4.8 pp asymmetry between crosswalk
> (−1.42 pp) and spatial (+3.35 to +4.15 pp) measurements stands as a
> genuine cross-method disagreement deserving flag, not as a Tier-C
> geometry artefact that cleanup resolves.

## References

* Cleanup script: `analysis/scripts/topology_cleanup.py`
* MAUP-v2 script: `analysis/scripts/assignment_va_attribution_maup_v2.py`
* MAUP-v1 script (historical baseline, unchanged): `analysis/scripts/assignment_va_attribution_maup.py`
* MAUP-v1 summary (historical): `analysis/reports/v0_1_phase4c_maup_summary.json`
* MAUP-v2 summary: `analysis/reports/v0_2_phase4c_maup_summary.json`
* Cleanup summary: `analysis/reports/topology_cleanup_summary.json`
* Per-ED cleanup log: `analysis/reports/topology_cleanup_log.csv`
