# Derived shapefiles

GeoPackage files used in all analysis. Only v0_10 files are canonical; all prior pipeline stages (v0_1 through v0_9) have been superseded and are not present on disk.

## Files

| File | Description |
| --- | --- |
| `v0_10_topological_majority_2026_eds.gpkg` | **Canonical majority 2026 map.** 89 electoral districts. Zero polygon overlaps. Produced by fixing 5 sub-pixel dissolve slivers present in v0_9. Used for all Lane 1 and Lane 2 scoring. |
| `v0_10_topological_minority_2026_eds.gpkg` | **Canonical minority 2026 map.** 89 electoral districts. Zero polygon overlaps. Produced by fixing 2 sub-pixel dissolve slivers present in v0_9. Used for all Lane 1 and Lane 2 scoring. |
| `va_polygons_with_2023_votes.gpkg` | Vote-anywhere (VA) polling station polygons joined to 2023 provincial election results. Contains `parent_ed_2019` column used to score the 2019 enacted map without a separate shapefile. Primary input for all MCMC ensemble runs. |
| `va_polygons_with_full_2023_votes.gpkg` | Same as above, retaining all raw attribute columns. Used for detailed vote-attribution diagnostics. |

## What is not here

The 2019 enacted map is not a derived file. It is the official statutory shapefile at `reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`. It is scored in the ensemble by aggregating VA polygons via the `parent_ed_2019` column, not by loading a separate derived file.

The v0_1 through v0_8 pipeline stages (approximate, refined, canonical, topology-cleaned, swept, municipal-anchored, DA-anchored, boundary-propagated, perfecter) are documented in git history. They are not present on disk. Do not reference them in any active script.

## Provenance

The v0_9 topological geometries were produced by `generate_topological_boundaries.py` from the v0_8 perfecter output, with geometry errors corrected by `shape_refinement_v6_writer.py`. An independent code audit (Gemini, 2026-04-26) identified and remediated 9 bugs across the pipeline before the canonical 250,000-step MCMC ensemble was run. v0_10 was produced by `fix_slivers_v0_10.py`, which resolved 5 sub-pixel boundary slivers in the majority map and 2 in the minority map, achieving zero-overlap topology in both. The corrected ensemble output is the basis for all Lane 1 metrics in the public report.

All geometry that traces back to a DPG (digitized proposal geometry) step is provisional pending release of official Elections Alberta shapefiles.
