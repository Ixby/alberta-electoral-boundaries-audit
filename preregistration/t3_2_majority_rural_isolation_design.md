---
title: T3.2 — Majority rural-isolation counter-test (pre-commitment)
version: 1.0
date_committed: 2026-06-11
drand_round_target: round at or after the commit hash recording this file
status: PRE-COMMITTED — do not amend after execution except via dated, signed entry in `findings/pre_registration_amendment_log.md`
salt_string: "t3_2_majority_rural_isolation_counter_test"
---

# T3.2 — Majority rural-isolation counter-test (pre-commitment)

This file freezes — *before* execution — the design, metrics, and decision rule for TODO_REMEDIATION T3.2 ("one majority-anomaly counter-test"). It is the symmetric counterpart to the minority-derived `findings/neighbour_drain_analysis.md` and closes the "the audit hypothesis-generated against the minority and pretended to symmetry-audit" critique.

## 1. Motivating anomaly

`findings/joint_outlier_score.json` records:

> "majority drain_score = 0.000179 vs ensemble mean 0.032085, z = −2.915, p < 0.0001 (one-sided, low tail)"

The majority's drain score is **more anomalous against the neutral ensemble than the minority's** (minority p = 0.1342, within the central band). The audit's published headline reads the minority's drain channel as "within null"; the majority's as "anomalously clean, not the partisan direction." The cleanliness has never been pressure-tested for an *engineered* explanation. T3.2 supplies that pressure test.

## 2. Hypothesis pair (frozen before execution)

**H₀ — Geographic.** The majority's anomalously low drain score reflects Alberta's statutory s.15(2) rural carve-outs and natural rural geography. The majority is not structurally more isolated than the minority or the 2019 enacted map on independent rural-isolation metrics.

**H₁ — Engineered.** The majority's low drain score is engineered: rural-anchored EDs were drawn as elongated corridors that minimize contact with urban/suburban populations. The majority will exhibit the most isolated pattern on independent rural-isolation metrics.

## 3. Substrate (frozen)

| Component | Choice |
|---|---|
| Majority map | `data/shapefiles/canonical/ea_majority_2026_eds.gpkg` (89 EDs) |
| Minority map | `data/shapefiles/canonical/ea_minority_2026_eds.gpkg` (89 EDs) |
| 2019 enacted (control) | `data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp` (87 EDs) |
| Rural/urban rule | ED is **rural-anchored** iff its name does not start with one of: `Calgary-`, `Edmonton-`, `Airdrie-`, `Lethbridge-`, `Red Deer-`, `Medicine Hat-`, `St. Albert-`, `Sherwood Park-`, `Fort McMurray-`, `Grande Prairie-`, `Spruce Grove-`. Applied identically to all three maps. |
| Adjacency | `geopandas` polygonal `intersects`-with-positive-shared-boundary; queen contiguity. Same rule across all three maps. |
| CRS for area/perimeter | EPSG:3400 (Alberta 10-TM); 2019 file reprojected from EPSG:3401 to EPSG:3400 before measurement. |

## 4. Metrics (frozen)

For each of the three maps, compute on the set of rural-anchored EDs:

| ID | Metric | Direction interpreting "more isolated" |
|---|---|---|
| R1 | Median Polsby-Popper across rural EDs | **lower** = more elongated corridors |
| R2 | Mean number of urban-anchored neighbors per rural ED | **lower** = less urban contact |
| R3 | Fraction of rural EDs with **zero** urban-anchored neighbors | **higher** = more rural-only stitching |

R1 and R2 are continuous; R3 is a fraction in [0, 1].

## 5. Decision rule (frozen)

Across the three maps, rank each map 1 (most isolated) to 3 (least isolated) on each of R1, R2, R3. Aggregate via mean rank.

- **H₁ supported** (majority is engineered for rural isolation) iff the majority has the lowest mean rank (= most isolated) AND is the most isolated map on ≥ 2 of 3 individual metrics.
- **H₀ supported** (geographic explanation) iff the majority is NOT the most isolated on ≥ 2 of 3 individual metrics.
- **Mixed** iff exactly 1 of 3 metrics finds majority most-isolated.

The 2019 enacted map serves as the geographic control: any "engineered isolation" signal on the majority that the 2019 map also exhibits is downweighted in the narrative report, because that pattern predates the 2025–26 commission process.

## 6. Reading the result

| Outcome | Audit-level meaning |
|---|---|
| H₁ supported on majority | Symmetric finding: the majority has a structural anomaly (rural isolation) the audit never characterized; the minority's drain/anchoring critique applies to the majority in mirrored form. Both maps carry structural anomalies of opposite sign. |
| H₀ supported on majority | The drain anomaly is geographic; no further pressure-test needed. The audit's existing reading ("anomalously clean, not partisan-directional") stands. |
| Mixed | Document as inconclusive; the majority's low drain remains a known anomaly, partially but not robustly characterized. |

The outcome will be published *as-is*, with the same priority and visibility as the minority's structural findings.

## 7. Reproducibility

```bash
python analysis/scripts/t3_2_majority_rural_isolation.py \
  --output-json findings/t3_2_majority_rural_isolation.json \
  --output-md   findings/t3_2_majority_rural_isolation.md
```

The script's git hash at execution time is recorded inside the output JSON (`script_commit` field).

## 8. What this test does *not* answer

- It does not estimate the partisan-bias direction of any isolation pattern (the joint outlier scores already cover that).
- It does not score the candidate Lunty November map. T3.2 closes a referee gap on the May commission analysis only.
- It does not produce a Mahalanobis-style joint p-value against the canonical ensemble (the per-plan rural-isolation metrics are not in the existing ensemble outputs; a true ensemble run is queued under T1.4 / T2.1).

The test answers **one** question: does the majority commission map exhibit a within-map rural-isolation signature stronger than the minority's and the 2019 enacted control's?
