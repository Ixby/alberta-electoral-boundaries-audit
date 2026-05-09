# Software Development Patterns Audit
**Date:** 2026-05-08 | **Reassessed:** 2026-05-08  
**Scope:** 108 Python files in `analysis/scripts/` and `analysis/utils/`  
**Method:** 5 parallel adversarial agents + mechanical grep passes; re-verified after session changes  

Findings are verified against actual file contents. Agent hallucinations have been dropped.

## Reassessment Summary

All structural pattern findings (A1–A5, M1–M7) remain open — session work addressed bugs and methodology documentation but did not remediate any pattern violations. One count correction: hardcoded seeds is **5** (not 8); the original pass matched comment lines and string literals it shouldn't have. Actual instances: `chen_rodden_alberta.py:205`, `generate_infographic.py:155`, `monte_carlo_ci.py:160,163`, `simulation_multichain_ensemble.py:695`.

The `historical deprecated/` folder (271 files, 589 MB) was archived to `historical_deprecated.zip` via Git LFS and deleted. It was not in `analysis/scripts/` or `analysis/utils/` so no audit counts are affected.

---

## ABSENT PATTERNS

### A1 — Single source of truth for EG/wasted-vote logic [HIGH]
The wasted-vote computation (`_ed_waste`, `compute_eg`) is **independently reimplemented** in at least 6 files instead of living once in a utility:

| File | Functions |
|------|-----------|
| `szat.py` | `_ed_waste`, `compute_eg`, `_eg_from_agg` |
| `szat_validate.py` | `_ed_waste`, `compute_eg` (copy-paste) |
| `historical_eg_baseline.py` | `compute_eg` |
| `overlap_zone_diagnostic.py` | `compute_eg`, `compute_eg_for_eds`, `compute_eg_swing` |
| `chen_rodden_alberta.py` | `efficiency_gap` |
| `mcmc_ensemble.py` | inline in `seat_results` |

`szat_validate.py` is a near-verbatim copy of the `szat.py` versions. If the wasted-vote formula needs a fix, it must be applied in 6 places. One has already drifted (the docstring in `historical_eg_baseline.py` was wrong — caught in ADVERSARIAL_AUDIT.md).

**Pattern needed:** Extract `_ed_waste` + `compute_eg` into `analysis/utils/eg_utils.py`. All callers import from there.

---

### A2 — Single source of truth for provincial population constant [MEDIUM]
`4_262_635` (Alberta 2021 Census total) appears scattered in 3 files:
- `a1_legal_baseline_2021_census.py:429,526,527`
- `szat_validate.py:235`
- `track_l_drift.py:49`

**Pattern needed:** One named constant `AB_2021_CENSUS_TOTAL = 4_262_635` in `analysis/utils/constants.py`, imported everywhere.

---

### A3 — Dependency annotations absent in 97 of 108 files [HIGH]
Project rule (CLAUDE.md/pattern 6.9): every file must declare forward and backward dependencies in its header. **97 files are non-compliant.** Only `szat.py`, `mcmc_ensemble_canonical.py`, `joint_outlier_score_canonical.py`, `data_loader.py`, `canonical_manifest.py`, `drand_seed.py`, `mcmc_ensemble.py`, `mcmc_ensemble_250k.py`, `simulation_multichain_ensemble.py`, and a handful of others have them.

Non-compliant files include major pipeline stages:
`a1_legal_baseline_2021_census.py`, `packing_cracking_analysis.py`, `chen_rodden_alberta.py`, `build_overlay_figures.py`, `submission_search.py`, `338canada_*.py`, etc.

**Pattern needed:** Add `Forward dependencies:` / `Backward dependencies:` sections to all 97 files.

---

### A4 — Integration tests absent [HIGH]
The pipeline has 8+ stages that feed into each other:
```
Census data → a1_legal_baseline → va_polygons → mcmc_ensemble → joint_outlier_score
                                              → szat → szat_validate
```
There are zero tests that verify:
- Output of stage N is valid input for stage N+1
- Schema is preserved across file boundaries
- Population totals are conserved

All 148 tests operate on synthetic in-memory data. If a stage outputs a column with a wrong name, it propagates silently until a downstream script crashes at runtime.

---

### A5 — Test coverage: 87 of 108 modules have no tests at all [HIGH]
Completely untested critical modules include:
- `canonical_manifest.py` — SHA-256 integrity checker with no test for mismatch, missing file, or corrupt file
- `data_loader.py` — used by every script, no tests for missing config, invalid CRS, missing columns
- `a1_legal_baseline_2021_census.py` — 14 public functions, foundational to all population analysis
- `chen_rodden_alberta.py`, `neighbour_drain_adjacency.py`, `submission_search.py`, `szat_validate.py`
- All 338canada files (scraper, reallocate, historical)

---

## MISUSED PATTERNS

### M1 — `except Exception:` with no logging: 24 instances [HIGH]
Bare exception catches that swallow errors silently. Full list:

| File | Lines | Risk |
|------|-------|------|
| `chen_rodden_alberta.py` | 131, 280, 333 | Spatial autocorrelation / chi2 fails silently, returns 0.0 or NaN |
| `neighbour_drain_adjacency.py` | 223, 237, 260 | Adjacency computation fails silently; results may be topologically wrong |
| `compactness_metrics.py` | 181 | Reock calculation fails, returns NaN — indistinguishable from legitimate NaN |
| `reock.py` | 95 | Same problem, different file |
| `a1_legal_baseline_2021_census.py` | 72 | UTF-8 encoding config silently fails |
| `build_overlay_figures.py` | 431, 567 | Figure generation fails silently |
| `generate_article_figures.py` | 269, 303, 704 | Figures silently fail |
| `generate_overlay_figures.py` | 459 | Figure silently fails |
| `commission_overlay.py` | 317 | Overlay computation silently fails |
| `cross_election.py` | 317 | Cross-election alignment silently fails |
| `joint_outlier_score_canonical.py` | 80 | Joint score calc silently fails |
| `municipal_splits.py` | 93 | Municipal boundary processing silently fails |
| `score_hybridization.py` | 151 | Hybridization scores silently fail |
| `submission_search.py` | 391 | Text extraction silently fails |
| `submission_sentiment_llm.py` | 35 | data_loader import silently falls back |
| `_fetch_osm_natural.py` | 90 | OSM fetch silently fails |
| `compactness_for_verification_subset.py` | 87 | Geometry error silently caught |

**Pattern needed:** Every `except Exception:` must either re-raise, or log with `print(f"WARNING: {e}", file=sys.stderr)` and document what the fallback means analytically.

---

### M2 — Silent `float("nan")` returns without caller contract: 26 instances [HIGH]
Functions return `float("nan")` on failure with no logging and no documented contract for callers. Callers in the pipeline often don't check for NaN before aggregating, which means NaN propagates into summary statistics silently.

Most affected: `compactness_metrics.py` (6 sites), `chen_rodden_alberta.py` (3 sites), `polsby_popper.py` (2 sites), `reock.py` (2 sites), `extended_partisan_metrics.py` (2 sites), `mcmc_ensemble.py` (1 site).

**Pattern needed:** Either log a warning before returning NaN, or raise a specific exception type (`GeometryError`, `InsufficientDataError`) so callers can distinguish expected empty from computation failure.

---

### M3 — God functions (>100 lines): 67 instances [MEDIUM]
The worst offenders violate single-responsibility — they compute, validate, format, and write output in one block:

| File | Function | Lines |
|------|----------|-------|
| `dependency_graph_build.py` | `build_nodes_and_edges()` | 1155 |
| `338canada_historical.py` | `main()` | 409 |
| `submission_ocr.py` | `run()` | 361 |
| `joint_outlier_score_canonical.py` | `run()` | 356 |
| `build_overlay_figures.py` | `draw_figure()` | 294 |
| `neighbour_drain_adjacency.py` | `write_analysis_md()` | 288 |
| `szat.py` | `run()` | 242 |
| `joint_outlier_score.py` | `run()` | 249 |

`joint_outlier_score_canonical.py:run()` at 356 lines does: file loading, EG computation, Mahalanobis computation, Fisher combination, markdown report generation, JSON output, and console printing. This should be 6+ functions.

---

### M4 — Column name fragmentation across 108 files [MEDIUM]
The ED name column is referenced under 5 different names with no central mapping:

| Column name | Files using it |
|-------------|---------------|
| `EDName2025` | 11 files |
| `EDName2017` | 18 files |
| `EDName` | 25 files |
| `ed_name` | 43 files |
| `parent_ed` | 14 files |

Scripts that join shapefiles often assume which name they'll find without asserting. When canonical shapefiles used `EDName2025` instead of `EDName`, the fix required touching `score_exogenous_map()` in `mcmc_ensemble.py` plus the `id_col` parameter in `mcmc_ensemble_canonical.py`. If another shapefile comes in with `EDName2026`, the breakage would be discovered at runtime.

**Pattern needed:** A column alias resolver in `canonical_paths.py` or `data_loader.py`: `def get_ed_name_col(gdf) -> str` that detects which variant is present.

---

### M5 — Hardcoded magic seeds: 5 instances [MEDIUM] *(corrected from 8; prior count matched comment lines)*

`seed=42` appears in `chen_rodden_alberta.py:205`, `monte_carlo_ci.py:163`, and `simulation_multichain_ensemble.py:695`. These are outside the pre-registered drand seed system. `monte_carlo_ci.py` runs N=2,000 samples with seed=42 which is documented in a print statement but not in any pre-registration.

---

### M6 — Test antipatterns: 2 tests with no assertions [LOW]
- `test_cross_election_baseline.py:94` — function body exists, no assert statements
- `test_tripwires.py:17` — setup code with no assertions (test always passes regardless of outcome)

---

### M7 — `szat_validate.py:235` — `PROV_POP` used only in Check 4 (added this session) [LOW]
`PROV_POP = 4_262_635` was just added to `szat_validate.py` as part of the O2 sensitivity fix. This is a local constant that should be imported from a shared `constants.py` once A2 is resolved.

---

## PRIORITISED REMEDIATION ORDER

| Priority | Finding | Effort | Risk of not fixing |
|----------|---------|--------|-------------------|
| 1 | **A1** — Extract EG utils | 2h | Formula drift across files → silent numerical divergence |
| 2 | **M1** — Add logging to all 24 bare excepts | 1h | Silent failures in spatial analysis; results wrong, appear valid |
| 3 | **M2** — NaN return contracts (26 sites) | 2h | NaN propagates into published statistics |
| 4 | **A5** — Tests for canonical_manifest + data_loader | 3h | Hash integrity guard has no self-tests |
| 5 | **A4** — One integration test per pipeline stage | 4h | Schema drift goes undetected between stages |
| 6 | **A2** — Single population constant | 30m | Divergence if Census figures are revised |
| 7 | **M4** — Column name resolver | 1h | Shapefile format change → runtime crash |
| 8 | **A3** — Dependency annotations (97 files) | 4h | Required by project rule; traceability gap |
| 9 | **M3** — Decompose god functions | 8h+ | Untestable, unmaintainable analysis core |
| 10 | **M5** — Replace magic seeds with named constants | 30m | Reproducibility documentation incomplete |

---

## NOT FIXING (with rationale)

- `_fetch_osm_natural.py` — one-off data fetch utility; never run in analysis pipeline; silent fail on OSM timeout is acceptable
- `build_pdf.py`, `build_cover.py`, `build_academic_pdf.py` — report assembly scripts; god function length is acceptable for layout code
- `dependency_graph_build.py` `build_nodes_and_edges()` at 1155 lines — graph construction; the complexity is inherent to the domain model, not poor design
- 338canada scraper files — external dependency; fragility is inherent to web scraping; adding assertions inside the scraper doesn't help if the site changes
