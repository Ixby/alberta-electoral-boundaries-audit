# Derived shapefiles

> **Superseded 2026-07-13.** This README described the pre-official-shapefile (DPG) pipeline
> as "canonical." It is not. Since the official Elections Alberta shapefiles arrived
> 2026-05-06, the canonical majority and minority 2026 maps are
> `data/shapefiles/canonical/ea_majority_2026_eds.gpkg` and
> `data/shapefiles/canonical/ea_minority_2026_eds.gpkg` — see
> `analysis/methodology/canonical_shapefile_log.md` and CLAUDE.md's DPG sunset clause.
> The `v0_10_topological_majority_2026_eds.gpkg` / `v0_10_topological_minority_2026_eds.gpkg`
> files this README used to describe as canonical **do not exist on disk** and have not
> since before this directory was last touched (2026-04-28). Only the four
> `va_polygons_with_*.gpkg` files below are actually present, and they are still live inputs
> (vote-attribution substrate for the MCMC ensemble and cross-election checks), which is why
> this file is corrected rather than deleted.

## Files (what is actually here)

| File | Description |
| --- | --- |
| `va_polygons_with_2023_votes.gpkg` | Vote-anywhere (VA) polling station polygons joined to 2023 provincial election results. Contains `parent_ed_2019` column used to score the 2019 enacted map without a separate shapefile. Primary input for all MCMC ensemble runs. |
| `va_polygons_with_full_2023_votes.gpkg` | Same as above, retaining all raw attribute columns. Used for detailed vote-attribution diagnostics and the full-vote sensitivity check (ES-13). |
| `va_polygons_with_2019_votes.gpkg` | VA polygons joined to 2019 provincial election results. Input to the Option C cross-election EG-threshold ensemble ([§5.2.8](../../../reports/academic/report_academic.md)). |
| `va_polygons_with_2015_votes.gpkg` | VA polygons joined to 2015 provincial election results. Same purpose as above, for the 2015 electoral context. |

## What is not here

The 2026 majority and minority maps are **not** in this directory. They are the official
Elections Alberta shapefiles at `data/shapefiles/canonical/ea_majority_2026_eds.gpkg` and
`data/shapefiles/canonical/ea_minority_2026_eds.gpkg`.

The 2019 enacted map is not a derived file either. It is the official statutory shapefile at
`reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`. It is scored in the ensemble by
aggregating VA polygons via the `parent_ed_2019` column, not by loading a separate derived file.

The v0_1 through v0_10 DPG (digitized proposal geometry) pipeline stages — approximate,
refined, canonical, topology-cleaned, swept, municipal-anchored, DA-anchored,
boundary-propagated, perfecter, sliver-fixed — predate the 2026-05-06 official shapefile
release and are archived, not active. They are documented in git history and in
`archive/dpg_era/` and `archive/provisional_geometries/`. Do not reference them in any active
script.

## Provenance (historical — DPG era, superseded by canonical EA shapefiles 2026-05-06)

The v0_9 topological geometries were produced by `generate_topological_boundaries.py` from the
v0_8 perfecter output, with geometry errors corrected by `shape_refinement_v6_writer.py`. An
independent code audit (Gemini, 2026-04-26) identified and remediated 9 bugs across the
pipeline before the DPG-era 250,000-step MCMC ensemble was run on that substrate. v0_10 was
produced by `fix_slivers_v0_10.py`, which resolved 5 sub-pixel boundary slivers in the majority
map and 2 in the minority map, achieving zero-overlap topology in both. This DPG-era output was
the basis for Lane 1 metrics only until it was superseded by the canonical 1,010,000-step
(4 chains × 252,500 steps) ensemble run on the official Elections Alberta shapefiles.
