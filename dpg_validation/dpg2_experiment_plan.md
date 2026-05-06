# DPG2 — Methodology Analysis and v11 Design Plan

*Created: 2026-05-06*
*Status: Pre-registered hypotheses and test suite — do not modify thresholds after v11 production begins.*

---

## 1. What the Results Tell Us

### 1.1 Summary of dpg1 Findings

| Test | Majority | Minority | Threshold | Result |
|------|----------|----------|-----------|--------|
| dpg_accuracy (mean IoU, reconstructed) | 37.78% | 36.32% | — | BASELINE |
| T1 VA misassignment | 28.71% VAs | 32.91% VAs | ≤2% | FAIL |
| T1 EG delta | 0.55 pp | 3.89 pp | <0.1 pp | FAIL |
| T2 mean area error | ~41% | ~43% | <1% | FAIL |
| T3 mean Hausdorff | ~19 km | TBD | <500 m mean | FAIL |
| T4 Population MAD delta | −1 person | −1 person | — | EXACT |
| T4 Airdrie partitions | 2 = 2 | 4 = 4 | — | EXACT |
| T5 adjacency extra edges | 68/60 | 136/103 | ≤2 per side | FAIL |

### 1.2 Error Decomposition

The v0_10 DPG was built by assigning VA (Voting Area) polygons to 2026 EDs by
reading 300 DPI raster maps, then dissolving. There are three distinct sources
of error:

**Type A — VA misassignment (correctable):**
A VA was read as belonging to the wrong ED. The resulting DPG polygon
for each affected ED is geometrically wrong — it includes polygons it shouldn't
and/or excludes polygons it should have. This is the dominant error type based
on the magnitude of T1/T2/T3 failures.

Evidence: Airdrie-West has 0% IoU against the official Airdrie-West shapefile.
The official Cochrane-Springbank ED occupies most of that geographic area. This
means the DPG Airdrie-West VAs were assigned somewhere else, and Cochrane-
Springbank VAs were mis-claimed. Similarly, Calgary-Acadia has 211% area error —
the DPG Acadia spans ~153 km² but the official version is ~49 km²; ~100 km² of
VA polygons were incorrectly attached.

**Type B — Sub-VA precision ceiling (irreducible with current method):**
Even with perfect VA assignments, the official commission boundary lines cut
through VAs in some places. The commission draws arbitrary geographic lines
(along roads, rivers, etc.) that bisect VA polygons. A VA-resolution DPG cannot
replicate that precision; it can only assign whole VAs.

This creates a theoretical ceiling on achievable IoU that is strictly < 100%
for any ED where the official boundary crosses through a VA rather than
following a VA edge.

**Type C — Topological artifacts (minor):**
The dissolve process creates slivers or gaps at VA corners. Magnitude is small.

### 1.3 Critical Implication for the Audit

**Population MAD and Airdrie count are exact** — these metrics were computed
from the PopCensus attribute column in the official report, not from derived
geometry. They are correct by construction and survive regardless of geometric
accuracy.

**EG direction on the minority map is geometry-dependent.** The DPG produced
EG = +0.111% (NDP disadvantaged) and the official geometry produces EG = +3.999%
(same direction but 35× larger). The direction is stable; the magnitude is not.
Any audit finding that cited a specific EG magnitude computed from v0_10 needs
a caveat.

**Municipal anchoring (71% majority, 14.5% minority) is unvalidated.** The DPG
boundaries follow VA polygon edges, which were built to respect CSD boundaries.
Official commission boundaries may not follow VAs and may not align exactly with
the CSD shapefile — making this metric hard to confirm via exact intersection.

**Adjacency graph (§5.3.5 neighbour-drain finding) is geometry-dependent.**
The majority map has 68 spurious DPG adjacencies and 60 missing ones. The
minority map is worse. Any finding that depended on specific adjacency pairs
(e.g., which EDs are neighbours) must be re-verified against official geometry.

---

## 2. Theoretical Maximum IoU (Sub-VA Ceiling)

Before attempting v11, we must estimate how much of the 37% mean IoU is
recoverable by better VA assignment vs how much is the irreducible precision
ceiling. This is **Test T-A** (see §4).

Estimation approach:
- For each official ED polygon, compute what fraction of its area consists of
  VAs that are fully contained (IoU with VA polygon ≥ 99%) vs VAs that are only
  partially inside the official boundary.
- `ceiling_IoU = sum(area of fully-contained VAs) / official_ED_area`
- If the ceiling is typically 75-85%, most of the 37% deficit is recoverable.
- If the ceiling is typically 45-55%, the method has a fundamental limitation.

Hypothesis: The ceiling is ≥75% for most EDs (H2 below). This is based on the
observation that Elections Alberta generally uses natural/administrative features
as ED boundaries — rivers, roads, CSD boundaries — which tend to coincide with
VA polygon edges.

---

## 3. Hypotheses (Pre-Registered)

All thresholds below are set before any v11 geometry is produced.

**H1 — Error decomposition:**
At least 60% of the observed IoU deficit is attributable to Type A
(VA misassignment), not Type B (sub-VA precision). Operationalised: the
mean sub-VA ceiling IoU (T-A) is ≥65% for majority reconstructed EDs.

**H2 — Theoretical ceiling:**
The mean sub-VA ceiling IoU across all 89 majority EDs is ≥75%, indicating
that the VA polygon layer has sufficient spatial resolution to represent the
commission's drawn boundaries in most cases.

**H3 — v11 target:**
After correcting VA assignments using the raster re-reading procedure (§5),
v11 achieves mean IoU ≥65% for reconstructed EDs (majority map).
Secondary target: minority map mean IoU ≥60% (harder due to more new EDs).

**H4 — EG direction stability:**
The EG sign for the minority map is consistent across v0_10, v11, and official
geometry (all show NDP disadvantaged, i.e., positive EG value). If v11 agrees
in direction, the direction finding from the audit is robust to geometry error.

**H5 — Historical feasibility trigger:**
If v11 achieves mean IoU ≥65% for majority reconstructed EDs, the same
VA-assignment procedure applied to historical Alberta raster maps (2012, 2017)
would yield similarly reliable reconstructions (within ±5 pp uncertainty), and
those reconstructions would be appropriate for comparative historical analysis.

---

## 4. Test Suite

### T-A: Sub-VA Ceiling Estimation (NEW — diagnostic, runs before v11)

**Purpose:** Quantify the maximum achievable IoU for a VA-resolution DPG.

**Method:**
For each official ED polygon, intersect against the full VA polygon layer.
For each VA:
  - `contained_pct = intersection_area / va_area`
  - If `contained_pct ≥ 0.95`: VA is "fully inside" — count full VA area
  - Else: VA straddles the boundary — count only the intersection area

Ceiling IoU = `sum(fully_inside_va_areas) / official_ed_area`

**Output:** `outputs/ta_va_ceiling.csv`
  Columns: map, ed_name, official_area_km2, ceiling_iou_pct, n_full_vas, n_partial_vas, partial_va_area_km2

**Pass criterion (pre-registered):**
  - Mean ceiling IoU ≥ 75% (tests H1 and H2)

---

### T-B: Misassignment Classification (NEW — diagnostic, runs before v11)

**Purpose:** Identify which VAs are likely misassigned in v0_10, and classify
the error type.

**Method:**
For each VA polygon, determine which ED it currently belongs to in v0_10 (DPG)
and which ED contains the VA's centroid in the official shapefile. If they differ,
the VA is a candidate misassignment.

Classify each discrepant VA:
  - Type A1 (over-claim): VA centroid is in official ED X, but v0_10 assigns it to ED Y
  - Type A2 (under-claim): VA centroid is in official ED X, but v0_10 doesn't assign it to X
  - Type B (boundary): VA straddles official boundary — no single correct assignment

**Output:** `outputs/tb_va_misassignment_map.csv`
  Columns: va_id, va_area_km2, dpg_ed, official_ed, error_type, confidence

**Derived statistics:**
  - n_type_a_vas: count of VAs that are clearly misassigned
  - pct_va_area_misassigned: % of total VA area that is misassigned
  - top_affected_eds: EDs with most misassigned VAs (rework priority list)

---

### T-C: v11 Full Accuracy Suite (runs after v11 is produced)

Re-run dpg_accuracy.py and T1–T5 on v11 geometry.

**Pre-registered pass thresholds for v11:**

| Metric | v0_10 result | v11 threshold |
|--------|-------------|---------------|
| Mean IoU (reconstructed) | 37.78% maj / 36.32% min | ≥65% maj / ≥60% min |
| T1 VA misassignment | 28.71% / 32.91% | ≤10% |
| T1 EG delta | 0.55 / 3.89 pp | <0.5 pp |
| T2 mean area error | ~41% / ~43% | <10% mean |
| T3 mean Hausdorff | ~19 km / TBD | <5 km mean |
| T5 extra adjacency edges | 68/60 per side | ≤10 per side |

Note: Thresholds are set deliberately below the official pass thresholds (T1–T5
were designed to evaluate DPG against official, not as absolute quality gates)
and above v0_10 results.

---

### T-D: EG Stability Check (runs after v11)

Compute EG at v0_10, v11, and official (from dpg1 data).

Pre-registered criteria:
  - EG direction (sign) consistent across all three → direction finding is robust
  - If v11 EG disagrees in sign with official → geometric error was masking true partisan structure; flag as unreliable
  - If v11 EG magnitude is within 1 pp of official → v11 is sufficient for quantitative claims

---

## 5. v11 Reconstruction Procedure

### 5.1 Source Material Protocol

**Read-only (never modified):**
- `data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg` — original DPG
- `data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg` — original DPG
- `data/shapefiles/derived/va_polygons_with_2023_votes.gpkg` — VA source polygons
- Raster source images (300 DPI maps used for original reading)
- Official shapefiles (dpg_validation/data/official/) — read-only oracle only

**New outputs (created, not copied from any source):**
- `data/shapefiles/derived/v0_11_topological_majority_2026_eds.gpkg`
- `data/shapefiles/derived/v0_11_topological_minority_2026_eds.gpkg`
- `data/shapefiles/derived/v11_va_assignment_log.csv` — full audit trail

**Critical rule — oracle contamination:**
The official shapefiles may be used to IDENTIFY which VA assignments are
suspicious (via T-B diagnostic). But every individual correction must be
independently traceable back to visual evidence in the raster source image.
Do not move a VA boundary simply because the official map places it elsewhere —
reopen the raster, look at the colour/shading, and confirm the correct ED.
If the raster is ambiguous, record the VA as UNCERTAIN and do not change it.

This is essential for scientific credibility. A v11 that simply reproduced
the official geometry would be circular and useless for validation.

### 5.2 Prioritization (derived from T-B output)

The T-B misassignment map produces a ranked list of VAs to re-examine.
Work in this order:
1. VAs where dpg_ed ≠ official_ed AND confidence = HIGH (unambiguous centroid-in-polygon mismatch)
2. VAs in EDs with IoU < 20% (worst cases first — Airdrie-West, Calgary-Nose Creek, Calgary-Symons Valley, etc.)
3. VAs in EDs with IoU 20–50% (middle tier)
4. VAs in EDs with IoU > 50% (fine-tuning, may not be worth the rework)

### 5.3 Assignment Log Schema

Every VA whose assignment is changed must be logged:

```
va_id, old_ed, new_ed, reason_code, raster_evidence_note, confidence, reviewer
```

Reason codes:
- `RASTER_REREAD`: Returned to raster and confirmed new assignment is correct
- `RASTER_AMBIGUOUS`: Raster is ambiguous; new assignment is best interpretation
- `TOPOLOGY_FIX`: Required for geometric consistency (no isolated VAs)
- `UNCHANGED`: VA examined but assignment confirmed correct; no change made

### 5.4 Procedure Steps

1. **Run T-A and T-B diagnostics** → get ceiling estimate and priority VA list
2. **Sort priority list by impact** (large VAs in badly-wrong EDs first)
3. **For each priority VA:**
   - Open the raster at that VA's location
   - Determine which ED colour/shading the VA belongs to
   - If unambiguous: log RASTER_REREAD with description of visual evidence
   - If ambiguous: log RASTER_AMBIGUOUS with note, assign to most likely ED
   - If truly unclear: log as UNCERTAIN and keep original assignment
4. **After all high/medium priority VAs reviewed:**
   - Re-dissolve VA assignments → generate v0_11 GeoPackages
   - Run T-C and T-D

---

## 6. Implications for Historical Maps

The dpg2 goal is to establish whether the VA-assignment methodology is
reliable enough for scientific use.

**Validation chain:**
```
Official shapefile ← v11 (IoU ≥65%) ← improved VA assignment procedure
                                               ↓
                               Apply same procedure to 2012/2017 rasters
                                               ↓
                            Historical DPG (no official oracle available)
                            Uncertainty = same as v11's residual error
```

If H3 is confirmed (v11 ≥65% mean IoU), then:
- The method has been validated against ground truth for 2026
- Applying it to historical maps gives geometries with ~35% expected IoU deficit
- Historical comparative analysis is valid if the conclusions are robust to ±35% geometric uncertainty
- Conclusions that depend on fine geometric precision (Hausdorff, adjacency) should be reported as geometry-dependent and uncertain

If H3 fails (v11 < 65%):
- The method cannot be recommended for historical maps without a fundamentally different approach
- A hybrid approach (VA assignment + boundary line tracing from raster) would be needed

---

## 7. What the Code Needs (Functional Changes for v11)

### 7.1 New scripts required

- `scripts/ta_va_ceiling.py` — sub-VA ceiling estimation
- `scripts/tb_va_misassignment_map.py` — VA-level misassignment classification
- `scripts/make_v11.py` — ingest corrected assignment log, re-dissolve, output GeoPackages

### 7.2 Changes to existing scripts

- `dpg_accuracy.py`: Accept a GeoPackage path as argument (`--dpg-path`) so same script runs on v0_10 and v0_11
- `t4_metric_rerun.py`: Already updated to buffer-based municipal anchoring (50 m)
- No other changes to T1–T5 — they should be parameter-driven, not hard-coded to v0_10 paths

### 7.3 No changes to source DPG files

`v0_10_topological_majority_2026_eds.gpkg` and `v0_10_topological_minority_2026_eds.gpkg`
are historical artifacts. They must remain byte-identical to the files used in
the original audit. Git hash is the integrity check.

---

## 8. Execution Sequence

```
Phase 1 (diagnostic — read-only):
  1. Verify T3/T4 complete correctly (pending background jobs)
  2. Write and run scripts/ta_va_ceiling.py
  3. Write and run scripts/tb_va_misassignment_map.py
  4. Produce priority rework list

Phase 2 (v11 construction):
  5. Systematic VA re-reading session (human + raster source material)
  6. Populate v11_va_assignment_log.csv
  7. Run make_v11.py to dissolve and output GeoPackages

Phase 3 (v11 validation):
  8. Run dpg_accuracy.py on v11
  9. Run T1-T5 on v11
  10. Run T-D EG stability check
  11. Write dpg2 results summary

Phase 4 (reporting):
  12. Update audit methodology notes (§4.1.4) with v11 provenance
  13. Revise any geometry-dependent findings from original audit
```

---

*End of dpg2 experiment plan.*
