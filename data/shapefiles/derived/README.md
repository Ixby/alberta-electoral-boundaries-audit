GeoPackage files produced by the shape-construction pipeline, from initial approximation through to the final analysis-ready shapefiles.

## Pipeline stages

All files cover the 87 proposed 2026 Alberta electoral districts (EDs) in majority and minority scenarios unless otherwise noted. Files without a "v0_N_" prefix are auxiliary.

| Stage | Files | What it adds |
|---|---|---|
| **Approximate** (v0_1) | `v0_1_approximate_majority_2026_eds.gpkg` / `_full.gpkg` / `v0_1_approximate_minority_2026_eds.gpkg` | Initial ED polygons digitized from Commission proposal documents (DPG-derived). `_full` retains all attribute columns; the plain version is trimmed. |
| **Refined v1–v6** | `v0_1_refined_*.gpkg` | Iterative geometry corrections via `v0_1_shape_refinement_v*.py`. v1–v5 are intermediate; **v6 is the final refined version** and the only one carried forward. |
| **Canonical** (v0_1) | `v0_1_canonical_majority_2026_eds.gpkg` / `v0_1_canonical_minority_2026_eds.gpkg` | Standardized attribute schema, CRS set to EPSG:3400, built from v6 refined geometry by `v0_1_build_canonical_shapefiles_v2.py`. |
| **Topology-cleaned** (v0_2) | `v0_2_canonical_majority_2026_eds_topoclean.gpkg` / `v0_2_canonical_minority_2026_eds_topoclean.gpkg` | Topology errors (slivers, gaps, self-intersections) fixed by `v0_1_topology_cleanup.py`. |
| **Swept** (v0_3) | `v0_3_canonical_majority_2026_eds_swept.gpkg` / `v0_3_canonical_minority_2026_eds_swept.gpkg` | Tier-C boundary sweep applied; minor urban fringe adjustments. |
| **Municipal-anchored** (v0_4) | `v0_4_canonical_majority_2026_eds_anchored.gpkg` / `v0_4_canonical_minority_2026_eds_anchored.gpkg` | ED boundaries snapped to Statistics Canada Census Subdivision (municipal) boundaries by `v0_1_municipal_anchoring.py`. |
| **DA-anchored** (v0_5) | `v0_5_canonical_majority_2026_eds_da_anchored.gpkg` / `v0_5_canonical_minority_2026_eds_da_anchored.gpkg` | Further snapped to Dissemination Area boundaries by `v0_1_da_boundary_anchoring.py`, enabling precise population attribution. |
| **Boundary-propagated** (v0_6) | `v0_6_canonical_majority_2026_eds_propagated.gpkg` / `v0_6_canonical_minority_2026_eds_propagated.gpkg` | Population-weighted boundary propagation applied by `v0_1_boundary_propagation.py`. **These are the final canonical shapefiles used in all analysis.** |

## Auxiliary files

| File | Description |
|---|---|
| `v0_1_composite_majority_2026_eds.gpkg` / `v0_1_composite_minority_2026_eds.gpkg` | Composite shapefiles merging multiple source passes; used for QA comparison only. |
| `v0_1_derived_v7_majority_2026_eds.gpkg` / `v0_1_derived_v7_minority_2026_eds.gpkg` | Experimental v7 derivation; superseded by the canonical pipeline. |
| `va_polygons_with_2023_votes.gpkg` / `va_polygons_with_full_2023_votes.gpkg` | Vote-anywhere (VA) polling station polygons joined to 2023 results for spatial integrity analysis. |

## Provenance note

All files whose lineage includes a DPG (digitized proposal geometry) step are **provisional**. They will be replaced once Elections Alberta releases official shapefiles for the 2026 boundary proposal. The `v0_1_dpg_perturbation_analysis.md` report quantifies how sensitive audit findings are to DPG geometry uncertainty.
