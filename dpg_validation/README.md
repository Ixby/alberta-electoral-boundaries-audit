# DPG Validation Experiment

**Purpose:** Validate the v0_10 Derived Provisional Geometries (DPGs) against the official Elections Alberta shapefiles received May 2026. This experiment does not replace any published finding — it tests whether the DPG methodology was accurate enough to support those findings.

**Not for publication.** Results feed into the §4.1.4 sunset clause rerun. If a headline metric shifts by more than its stated precision, the paper is updated.

## Inputs

| File | Description |
|---|---|
| `data/official/majority/EBC2025_Boundaries_Apr092026.shp` | Official majority (Final Report) — 89 EDs, EPSG:3400 |
| `data/official/minority/Minority_Report_Boundaries.shp` | Official minority — 89 EDs, EPSG:3400 |
| `../data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg` | Canonical DPG majority |
| `../data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg` | Canonical DPG minority |
| `../data/shapefiles/derived/va_polygons_with_2023_votes.gpkg` | VA polygons with 2023 vote data |

## Tests

| Script | Test | Key output |
|---|---|---|
| `t1_vote_attribution.py` | VA assignment match rate + partisan swing from mismatch | `outputs/t1_misassignment_report.csv` |
| `t2_area_fidelity.py` | Per-ED area error DPG vs official | `outputs/t2_area_fidelity.csv` |
| `t3_boundary_displacement.py` | Per-ED Hausdorff + mean boundary displacement (metres) | `outputs/t3_displacement_per_ed.csv` |
| `t4_metric_rerun.py` | Headline metrics recomputed on official geometry | `outputs/t4_metric_delta.csv` |
| `t5_adjacency_topology.py` | Adjacency graph diff (affects §5.3.5 neighbour-drain) | `outputs/t5_adjacency_diff.csv` |

Run all five in order: `python scripts/t1_vote_attribution.py` etc.
Results are summarised by `python scripts/summarise.py` → `outputs/results_summary.md`.

## Join strategy

DPG names were derived from raster reconstruction and do not reliably match official `EDName2025`. All matching uses **maximum-area spatial overlap**: for each DPG polygon, the official polygon with the largest intersection area is its official counterpart. The name mapping is written to `outputs/name_mapping.csv` for review.

## Pass thresholds

These were set before running any test.

| Test | Pass condition |
|---|---|
| T1 | ≤ 2% of VAs misassigned; net partisan swing < 0.1 pp efficiency gap |
| T2 | Mean per-ED area error < 1%; no ED > 3% |
| T3 | Mean displacement < 500 m; no ED > 2 km Hausdorff |
| T4 | Each headline metric within stated precision (see script comments) |
| T5 | Adjacency graph edge sets identical or differ by ≤ 2 edges per map |
