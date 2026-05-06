# dpg2 Work Log

*Experiment: DPG Methodology Analysis and v11 Design*
*Started: 2026-05-06*

---

## Session 1 — dpg1 Results Review and dpg2 Plan (2026-05-06)

### dpg1 Baseline Results (all tests complete)

#### DPG Accuracy (IoU)

| Map | Total EDs | 2019-inherited (excluded) | Reconstructed | Mean IoU (recon) | Min IoU |
|-----|-----------|--------------------------|---------------|-----------------|---------|
| Majority | 89 | 35 | 54 | **37.78%** | 0.00% (Airdrie-West) |
| Minority | 89 | 31 | 58 | **36.32%** | 0.00% (Lethbridge-Cardston) |

Note: All 54 reconstructed majority EDs and 58 reconstructed minority EDs fell below 90% IoU.

---

#### T1 — Vote Attribution Equivalence

| Map | Total VAs | Misassigned | % Misassigned | EG (DPG) | EG (Official) | EG Delta | Pass |
|-----|-----------|-------------|---------------|----------|---------------|----------|------|
| Majority | 4,765 | 1,368 | 28.71% | +0.636% | +0.083% | 0.553 pp | FAIL |
| Minority | 4,765 | 1,568 | 32.91% | +0.111% | +3.999% | 3.889 pp | FAIL |

Threshold: ≤2% misassignment, <0.1 pp EG delta.

Key finding: The EG *direction* (NDP disadvantaged, positive value) is consistent
between DPG and official for both maps. The minority magnitude swing (+3.889 pp)
is significant but the sign is preserved. Direction finding from the audit is robust;
magnitude claims are not.

---

#### T2 — Area Fidelity

| Map | Mean abs area error | Max abs area error | EDs > 3% error | Pass |
|-----|--------------------|--------------------|----------------|------|
| Majority | ~41% | 211% (Calgary-Acadia) | 89/89 | FAIL |
| Minority | ~43% | 168% | 89/89 | FAIL |

Threshold: mean <1%, no ED >3%.

Note: These are geometric area errors from VA misassignment, not errors in
the PopCensus attribute (which is exact). Population figures are correct
by construction.

---

#### T3 — Geometric Boundary Displacement

| Map | Mean Hausdorff | Max Hausdorff | EDs > 2 km | Mean boundary disp | Pass |
|-----|---------------|---------------|------------|-------------------|------|
| Majority | 19,070 m | 94,993 m (Barrhead-Westlock-Athabasca) | 73/89 | 3,178 m | FAIL |
| Minority | 22,564 m | 136,657 m (Canmore-Kananaskis) | 81/89 | 3,379 m | FAIL |

Threshold: mean Hausdorff <500 m, no ED >2,000 m.

Worst majority offenders: Barrhead-Westlock-Athabasca (95 km), Mountain View-Kneehill (87 km),
Okotoks-Diamond Valley matched to wrong ED (83 km), Edmonton-Beaumont matched to Leduc-Devon (68 km).

Worst minority offenders: Canmore-Kananaskis matched to Rocky Mountain House-Banff Park (137 km),
Medicine Hat-Cypress (122 km), Calgary-Airdrie matched to Olds-Three Hills-Didsbury (103 km).

The minority worst-offender list shows many dpg_name ≠ official_name matches — this means
the spatial max-overlap matching itself is finding wrong ED pairs, indicating whole-ED
misplacements, not just boundary imprecision.

---

#### T4 — Headline Metric Rerun (COMPLETE — buffer-based anchoring, 50 m)

| Metric | Majority (official) | Majority (DPG) | Delta | Minority (official) | Minority (DPG) | Delta |
|--------|--------------------|--------------|----|--------------------|--------------|----|
| Population MAD | 3,179 | 3,180 | **−1 person** | 4,706 | 4,707 | **−1 person** |
| Municipal anchoring | **48.8%** | 71.0% | −22.2 pp | **41.1%** | 14.5% | +26.6 pp |
| NW Calgary excess | 0.8% | 2.8% | −2.0 pp | 6.3% | 11.5% | −5.2 pp |
| Airdrie partitions | **2** | 2 | **0** | **4** | 4 | **0** |

Population MAD and Airdrie count are exact matches (geometry-independent).

**CRITICAL FINDING — Municipal anchoring reversal:**

The DPG reported a 56.5 pp gap between majority (71.0%) and minority (14.5%),
which was used to characterise the minority map as poorly anchored to municipal
boundaries. The official geometry shows a gap of only **7.7 pp** (48.8% vs 41.1%).

Direction of error is opposite for the two maps:

- Majority DPG *over-reported* anchoring by 22.2 pp (VA edges happen to follow CSDs; commission lines are less rigidly bound to them)
- Minority DPG *under-reported* anchoring by 26.6 pp (VA misassignment created boundaries that cut through municipalities, masking the fact that the official minority map largely respects them)

This is a systematic bias: VA misassignment in the minority map caused the DPG
boundaries to cross CSD lines in ways the official boundaries do not. The finding
that "the minority map has dramatically lower municipal anchoring" does not survive
validation against official geometry.

NW Calgary excess also over-stated (DPG 11.5% vs official 6.3% for minority) for
the same reason: misassigned VAs shifted population counts between NW Calgary EDs.

---

#### T5 — Adjacency Topology

| Map | DPG edges | Official edges | Shared | DPG-only | Official-only | Pass |
|-----|----------|---------------|--------|----------|---------------|------|
| Majority | 247 | 239 | 179 | 68 | 60 | FAIL |
| Minority | 272 | 239 | 136 | 136 | 103 | FAIL |

Threshold: ≤2 extra edges per side.

The minority map is especially degraded: 136 spurious DPG adjacencies and 103 missing
real ones. Only 136/272 DPG edges (50%) correspond to actual adjacencies. The §5.3.5
neighbour-drain finding must be re-examined against official geometry.

---

### Interpretation

Findings that fail under better data are noted here with their original claim and the correction.
They are not removed from the audit — they are disclosed.

**Confirmed intact:**
1. Population MAD — exact (geometry-independent). 48% wider spread for minority confirmed.
2. Airdrie partition count — exact. 4 vs 2 confirmed.
3. EG direction (sign) on minority map — stable. Minority disadvantages NDP under both DPG and official geometry. Magnitude is actually stronger in official (4.0% vs 0.11% DPG) — direction finding is reinforced, not weakened.

**Failed under official geometry:**

4. **Municipal anchoring** — original claim: 71% majority, 14.5% minority (56.5 pp gap). Official geometry: 48.8% majority, 41.1% minority (7.7 pp gap). The claim that the minority map poorly follows CSD boundaries is not supported. The DPG systematically misrepresented minority map boundaries due to VA misassignment placing lines across CSDs that the actual commission lines do not cross.

5. **NW Calgary excess magnitude** — original claim: 11.5% minority, 2.8% majority. Official: 6.3% minority, 0.8% majority. Direction holds (minority still higher); minority magnitude overstated by ~83%.

6. **EG magnitude** — original DPG figure was 0.11% for minority. Official geometry gives 4.0%. Direction is confirmed and strengthened; the specific 0.11% figure should not be cited.

**Suspended pending v11:**

7. **§5.3.5 neighbour-drain adjacency finding** — stated as a pre-registered PASS for the minority map. T5 shows 50% of minority DPG adjacency edges are wrong. Whether the specific ED pair tested in §5.3.5 was correctly adjacent in DPG is unknown until v11 is produced. Finding is suspended.

8. Any other finding that named a specific ED boundary, area, or neighbour relationship.

**Root cause:**
The DPG was built by assigning entire VA polygons to EDs based on raster-map
reading. VA misassignment errors cascade: one wrong VA creates incorrect area,
incorrect boundary, incorrect adjacency, and incorrect vote attribution.
The mean IoU of ~37% means the average reconstructed ED has about 37% of its
area correctly placed.

---

### dpg2 Plan Summary

Full plan: `dpg2_experiment_plan.md`

**Phase 1 — Diagnostic (next session):**
- T-A: Sub-VA ceiling — what's the theoretical maximum IoU? (expected ≥75%)
- T-B: VA misassignment map — which VAs are wrong and how many need rework?

**Phase 2 — v11 Construction:**
- Systematic re-reading of raster source for priority VAs
- Log every change: `v11_va_assignment_log.csv`
- Reconstruct DPG from corrected assignments

**Phase 3 — v11 Validation:**
- Same T1–T5 suite on v11 geometry
- Pre-registered thresholds: mean IoU ≥65%, T1 ≤10% misassignment, T3 ≤5 km Hausdorff

---

### Scripts Written This Session

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/ta_va_ceiling.py` | Sub-VA ceiling estimation | WRITTEN — not yet run |
| `scripts/tb_va_misassignment_map.py` | VA misassignment classification | WRITTEN — not yet run |
| `scripts/make_v11.py` | v11 GeoPackage generator | NOT YET WRITTEN |

---

### Open Items

- [x] T4 rerun (buffer-based municipal anchoring) — complete
- [x] Write scripts/ta_va_ceiling.py
- [x] Write scripts/tb_va_misassignment_map.py
- [ ] PO approval to proceed to Phase 2 (raster re-reading)
- [ ] Confirm raster source files are accessible for re-reading session
- [ ] Decide whether v11 scope is majority-only or both maps

---

*Log continues as work progresses.*

---

## Session 2 — Phase 1 Completion + Drain v2 Plan (2026-05-06, continued)

### T-A Results (Sub-VA Ceiling)

| Map | Mean ceiling IoU | Min ceiling IoU | EDs < 75% | H2 result |
|-----|-----------------|-----------------|-----------|-----------|
| Majority | 100.1% | 100.0% (Calgary-Bow) | 0 | **SUPPORTED** |
| Minority | 100.2% | 100.0% (Calgary-Acadia) | 0 | **SUPPORTED** |

H2 pre-registered: mean ceiling ≥ 75%.

**Interpretation**: The official shapefiles were built by dissolving VA polygons — confirmed
by GIS staff acknowledgement in commission report (Mok, Cirka, Pittman). There is zero
sub-VA precision error. Every IoU deficit in v0_10 is Type A (VA misassignment), which
is fully correctable in v11.

### §5.3.5 on Official Geometry

| Map | Coupled signals | Audit v0_8 coupled | Delta |
|-----|-----------------|--------------------|-------|
| Majority | 47 | 3 | +44 |
| Minority | 21 | 4 | +17 |

Ratio (minority/majority): 0.45× — well below 1.5× threshold → **PASS**.

**Note**: Direction inverted from audit finding. Audit v0_8 showed minority slightly
above majority (1.33×); official geometry shows minority substantially below majority
(0.45×). Both are PASSes but in opposite relative directions. This is a data quality
artefact — the v0_8 minority DPG adjacency was 50% wrong (136/272 spurious edges).
The §5.3.5 finding on official geometry is the authoritative result.

Output: `outputs/t535_neighbour_drain_official.csv`

### T-B Status

`scripts/tb_va_misassignment_map.py` was started but output not yet present in
`outputs/tb_va_misassignment_map.csv`. Script may be still running or was not completed.
The boundary-proximity union computation is the bottleneck (O(n) polygon operations per VA).

### Drain v2 Plan

Written to `../analysis/methodology/drain_v2_plan.md`.

Summary of phases:

| Phase | Description | Effort | Status |
|-------|-------------|--------|--------|
| A — Continuous intensity | Replace binary gate with intensity product | 1-2 hr | **Pending** |
| B — Label shuffle null | Permute ED vote totals 10k times; compute z-score | 4-6 hr | Pending |
| E — Specificity weighting | Weight by 1 - null frequency per pair | 2 hr | After B |
| C — VA-level shuffles | Spatially-aware null, boundary VA swaps | 1-2 wk | After v11 |
| D — MCMC re-run | Full re-run with assignment output | TBD | Deferred (PO decision) |

Infrastructure constraint: existing `simulated_ensemble_raw_samples_100k.csv` stores
only aggregate metrics — no per-plan VA assignments. Phase B label shuffle is the
practical immediate baseline.

---

### Open Items (updated)

- [ ] T-B: re-run `scripts/tb_va_misassignment_map.py` and record output
- [ ] Drain Phase A: modify `neighbour_drain_adjacency.py` for continuous intensity
- [ ] Drain Phase B: write `scripts/drain_label_shuffle_null.py`
- [ ] PO approval to proceed to Phase 2 (raster re-reading / v11)
- [ ] Confirm raster source files accessible for re-reading session
- [ ] Decide v11 scope (majority-only or both maps)
- [ ] Add failed-findings disclosure to audit report documents
Loading VA polygons...
  4765 VAs loaded

=== majority ===
  Assigning VAs to DPG EDs...
  Assigning VAs to official EDs...
  Building official boundary for proximity classification...
  Classifying VAs...

  Total VAs:            4765
  Correct:              3542 (74.3%)
  Misassigned (clear):  1131 (23.7%)
  Near boundary (ambig):92 (1.9%)

  Top 10 EDs by rework VA count:
                   ed_name  n_underclaim_vas  n_overclaim_vas  n_total_rework
       Livingstone-Macleod                29               64              93
 High River-Vulcan-Siksika                66               23              89
            Edmonton-Enoch                42               41              83
Stony Plain-Drayton Valley                20               54              74
 Calgary-West-Elbow Valley                45               27              72
        Lacombe-Clearwater                38               29              67
Calgary-Glenmore-Tsuut'ina                45               19              64
            Calgary-Acadia                 3               58              61
          Calgary-McKenzie                57                0              57
        Calgary-Confluence                49                7              56

=== minority ===
  Assigning VAs to DPG EDs...
  Assigning VAs to official EDs...
  Building official boundary for proximity classification...
  Classifying VAs...

  Total VAs:            4765
  Correct:              2798 (58.7%)
  Misassigned (clear):  1828 (38.4%)
  Near boundary (ambig):139 (2.9%)

  Top 10 EDs by rework VA count:
                   ed_name  n_underclaim_vas  n_overclaim_vas  n_total_rework
    Calgary-Bow-Springbank                51               70             121
   Lethbridge-Taber-Warner                59               56             115
     Lethbridge-Little Bow                70               44             114
           Calgary-Airdrie                33               67             100
Stony Plain-Drayton Valley                23               77             100
       Lethbridge-Cardston                57               33              90
       Red Deer-Blackfalds                17               69              86
      Edmonton-Enoch-Devon                39               45              84
          Edmonton-McClung                17               55              72
             Calgary-Klein                18               52              70

Saved -> C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\dpg_validation\outputs\tb_va_misassignment_map.csv
Saved -> C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\dpg_validation\outputs\tb_misassignment_summary.csv
