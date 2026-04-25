Python scripts that run every stage of the Alberta electoral boundary audit, from shape construction through statistical analysis to publication output.

## Key analysis scripts

| Script | What it produces | DPG-dependent? |
|---|---|---|
| `electoral_forensics_population.py` | Main population-equality forensics report | Yes |
| `v0_2_packing_cracking_analysis.py` | Packing/cracking quantification across EDs | Yes |
| `v0_1_compactness_metrics.py` | Polsby-Popper and related compactness scores | Yes |
| `v0_1_contiguity_check.py` | Contiguity violations report | Yes |
| `v0_1_population_consistency.py` | Cross-source population consistency table | Yes |
| `v0_1_adjacency_analysis.py` | ED adjacency matrix and summary stats | Yes |
| `v0_1_neighbour_drain_adjacency.py` | Neighbour-drain effect analysis | Yes |
| `v0_1_municipal_anchoring.py` | Municipal boundary anchor pass (v0_4 shapefiles) | Yes |
| `v0_1_da_boundary_anchoring.py` | Dissemination-area anchor pass (v0_5 shapefiles) | Yes |
| `v0_1_boundary_propagation.py` | Population-weighted boundary propagation (v0_6 shapefiles) | Yes |
| `v0_1_mcmc_ensemble_100k.py` | MCMC ensemble (100 k draws) for redistricting bias | Yes |
| `v0_1_historical_eg_baseline.py` | Efficiency-gap baseline from historical elections | No |
| `v0_1_dependency_query.py` | Queries audit dependency graph for upstream/downstream links | No |

## Build scripts

| Script | What it produces |
|---|---|
| `build_pdf.py` | `article.pdf` via LaTeX |
| `build_academic_html.py` | `dist/` HTML publication |

## Shape pipeline (run in order)

```
v0_1_build_canonical_shapefiles.py
  → v0_1_topology_cleanup.py
  → v0_1_build_canonical_shapefiles_v2.py
  → v0_1_municipal_anchoring.py
  → v0_1_da_boundary_anchoring.py
  → v0_1_boundary_propagation.py
```

Each step produces the correspondingly versioned `.gpkg` files in `data/shapefiles/derived/`. See that directory's README for what each version adds.

`v0_1_shape_refinement_v*.py` (v1–v5) are intermediate iterations; **v6 is the final version** used as input to the canonical pipeline. The helper modules `v0_1_shape_refinement_v6_processors.py` and `v0_1_shape_refinement_v6_writer.py` are called by v6, not run directly.
