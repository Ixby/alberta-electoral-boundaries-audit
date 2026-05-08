# DEPRECATED — Derived Provisional Geometries

**Superseded 2026-05-07.** Official Elections Alberta canonical shapefiles are now in `data/shapefiles/canonical/`. All active analysis scripts have been updated to prefer canonical shapefiles over these DPG-derived files.

These files are kept for provenance and reproducibility of earlier pipeline runs. Do not use them for new analysis.

## Files in this directory

| File | Version | Superseded by |
|---|---|---|
| `v11_majority_2026_eds.gpkg` | v11 DPG | `canonical/ea_majority_2026_eds.gpkg` |
| `v11_minority_2026_eds.gpkg` | v11 DPG | `canonical/ea_minority_2026_eds.gpkg` |
| `v0_10_topological_majority_2026_eds.gpkg` | v0_10 | `canonical/ea_majority_2026_eds.gpkg` |
| `v0_10_topological_minority_2026_eds.gpkg` | v0_10 | `canonical/ea_minority_2026_eds.gpkg` |
| `v0_9_topological_majority_2026_eds.gpkg` | v0_9 | `canonical/ea_majority_2026_eds.gpkg` |
| `v0_9_topological_minority_2026_eds.gpkg` | v0_9 | `canonical/ea_minority_2026_eds.gpkg` |
| `va_polygons_with_2023_votes.gpkg` | v1 VA | Superseded by `va_polygons_with_full_2023_votes.gpkg` |
| `va_polygons_with_full_2023_votes.gpkg` | v2 VA | Still in use by SZAT for VA-level attribution |

## DPG methodology

The DPG (Derived Provisional Geometry) framework was built because official shapefiles were not yet released. Full methodology documented at `analysis/methodology/novel_contributions.md` §1 and `analysis/reports/methods_paper_draft.md`. The DPG sunset clause (AsPredicted #289,449) required re-running all analyses against official geometry within 48 hours of release — this has been done; results are in `analysis/reports/`.
