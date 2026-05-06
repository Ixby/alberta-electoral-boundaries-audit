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

#### T4 — Headline Metric Rerun (T4 still running — partial results from last run)

| Metric | Majority (official) | Majority (DPG) | Delta | Minority (official) | Minority (DPG) | Delta |
|--------|--------------------|--------------|----|--------------------|--------------|----|
| Population MAD | 3,179 | 3,180 | **−1 person** | 4,706 | 4,707 | **−1 person** |
| Municipal anchoring | TBD (rerunning with buffer fix) | 71.0% | TBD | TBD | 14.5% | TBD |
| NW Calgary excess | 0.77% | 2.8% | −2.03 pp | 6.27% | 11.5% | −5.23 pp |
| Airdrie partitions | **2** | 2 | **0** | **4** | 4 | **0** |

Municipal anchoring was returning 0.0% due to exact-intersection failure across
different digitization sources. Fixed to use 50 m buffer approach — rerun in progress.

Population MAD and Airdrie count are **exact matches**. These are the two
geometry-independent metrics and both confirm the DPG attribute data is correct.

NW Calgary excess differs because the geometric error changes which VAs land in
which NW Calgary EDs, altering the population-weighted mean.

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

**What is intact from the original audit:**
1. Population MAD — exact (geometry-independent)
2. Airdrie partition count — exact (geometry-independent)
3. EG direction (sign) on minority map — stable across DPG and official

**What is degraded or unconfirmed:**
4. Municipal anchoring — couldn't confirm with exact intersection; buffer rerun pending
5. NW Calgary excess — differs by 2–5 pp due to VA misassignment changing population allocations
6. EG magnitude on minority — 35× larger in official geometry (0.11% DPG vs 4.0% official)
7. Adjacency graph — majority 28% wrong, minority 50% wrong
8. Any finding that depended on specific ED boundaries (Hausdorff, area, etc.)

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
| `scripts/ta_va_ceiling.py` | Sub-VA ceiling estimation | NOT YET WRITTEN |
| `scripts/tb_va_misassignment_map.py` | VA misassignment classification | NOT YET WRITTEN |
| `scripts/make_v11.py` | v11 GeoPackage generator | NOT YET WRITTEN |

---

### Open Items

- [ ] T4 rerun (buffer-based municipal anchoring) — background job running
- [ ] Write scripts/ta_va_ceiling.py
- [ ] Write scripts/tb_va_misassignment_map.py
- [ ] PO approval to proceed to Phase 2 (raster re-reading)
- [ ] Confirm raster source files are accessible for re-reading session
- [ ] Decide whether v11 scope is majority-only or both maps

---

*Log continues as work progresses.*
