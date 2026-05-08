Python scripts that run every stage of the Alberta electoral boundary audit, from shape construction through statistical analysis to publication output.

## Key analysis scripts

| Script | What it produces |
|---|---|
| `electoral_forensics_population.py` | Main population-equality forensics report |
| `packing_cracking_analysis.py` | Packing/cracking quantification across EDs |
| `compactness_metrics.py` | Polsby-Popper and related compactness scores |
| `contiguity_check.py` | Contiguity violations report |
| `population_consistency.py` | Cross-source population consistency table |
| `adjacency_analysis.py` | ED adjacency matrix and summary stats |
| `neighbour_drain_adjacency.py` | Neighbour-drain effect analysis |
| `mcmc_ensemble_100k.py` | MCMC ensemble (100 k draws) for redistricting bias |
| `historical_eg_baseline.py` | Efficiency-gap baseline from historical elections |
| `dependency_query.py` | Queries audit dependency graph for upstream/downstream links |

## Build scripts

| Script | What it produces |
|---|---|
| `build_pdf.py` | `article.pdf` via LaTeX |
| `build_academic_html.py` | `dist/` HTML publication |

## Shape pipeline (Archived)

> [!NOTE]
> **Deprecated as of May 6, 2026.** Elections Alberta provided the official 2026 shapefiles, triggering the sunset clause. All scripts related to the construction, refinement, and validation of the Derived Provisional Geometries (DPGs) have been moved to the `dpg_archive/` directory.

The DPG pipeline previously ran in this order:
```
build_canonical_shapefiles.py
  → topology_cleanup.py
  → generate_topological_boundaries.py
  → municipal_anchoring.py
  → da_boundary_anchoring.py
  → boundary_propagation.py
```
Each step produced versioned `.gpkg` files (v0_1 through v0_10) in `data/shapefiles/derived/`. This code is retained strictly for provenance to document the blocked-phase methodology.
