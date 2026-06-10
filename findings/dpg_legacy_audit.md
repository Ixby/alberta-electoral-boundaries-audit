---
name: dpg_legacy_audit
description: Audit of legacy DPG (Derived Provisional Geometry) data and dependencies in the post-canonical codebase
type: project
date: 2026-06-10
status: scan complete; fixes applied; remaining items queued in TODO_REMEDIATION
---

> **Backward:**
> - `analysis/scripts/canonical_paths.py` — canonical path resolver
> - `analysis/methodology/canonical_shapefile_log.md` — DPG → canonical reconciliation log
> - `archive/dpg_era/` and `archive/provisional_geometries/dpg/` — retired DPG artifacts
> - `findings/post_audit_recompute_deltas.md` — canonical recomputation deltas
>
> **Forward:**
> - `TODO_REMEDIATION.md` — remediation queue items T4.1 (banner stale files), this audit
> - `reports/academic/report_academic.md` §4.1.4 (sunset clause + material-change disclosure)
> - `analysis/scripts/build_cover.py` (hardened this pass to remove silent DPG fallback)

# Legacy DPG-era data and dependencies in the post-canonical codebase

**Status: full repo scan complete 2026-06-10. No DPG-substrate contamination of currently published canonical results was found. Three classes of legacy residue were identified and either fixed in this pass or queued in TODO_REMEDIATION. The most consequential is documented under "Fixed this pass" below. The largest currently-open class is cosmetic (v0_x labels in script docstrings, output filenames, and chart titles) and is queued as a non-blocking cleanup.**

## What I scanned

- All `.py` scripts under `analysis/scripts/` (every script ever invoked in the audit pipeline)
- All `.md` / `.json` artifacts under `findings/`
- All `.json` / `.csv` / `.gpkg` under `data/` (excluding `archive/`)
- The dependency graph (`analysis/methodology/audit_dependency_graph.json`)
- `data/shapefiles/derived/` (the historical DPG home)
- `config.yaml` and `analysis/utils/canonical_manifest.py`

201 active (non-archived) files contained at least one DPG-era reference (`DPG`, `v0_[0-9]+`, `provisional`, `derived_geom`, `approximate_shape`). Of those:
- **0 currently load DPG-substrate data at runtime in any code path that feeds a published canonical number.**
- **2 active scripts and 1 finding artifact had silent-fallback or labelling risks** (fixed this pass).
- **2 finding artifacts were DPG-era results sitting unbannered in the active `findings/` directory** (bannered this pass).
- **~50 scripts** have stale `v0_x` mentions in docstrings, output filenames, or chart titles that compute from canonical data but label outputs as v0_x (cosmetic; queued).

## Fixed this pass

### 1. `analysis/scripts/build_cover.py` — silent DPG fallback chain removed

The cover-art renderer carried a five-element candidate list per map:

```python
APPROX_MAJ_CANDIDATES = [
    CANONICAL / "ea_majority_2026_eds.gpkg",
    DERIVED / "v0_10_topological_majority_2026_eds.gpkg",
    DERIVED / "v0_8_refined_majority_2026_eds.gpkg",
    DERIVED / "v0_8_canonical_majority_2026_eds.gpkg",
    DERIVED / "v0_7_canonical_majority_2026_eds.gpkg",
]
```

The runtime picker selected the first existing path. Canonical comes first, so the script currently renders from canonical. **But the four DPG fallbacks would have silently activated if canonical were ever moved or missing**, with no warning to the user — quietly contaminating the published cover figure. This was the only script with this pattern. **Fix:** the candidate list was reduced to just the canonical path; the script now fails loudly (with a clear FileNotFoundError) if canonical is absent.

### 2. `findings/phase4c_maup_summary.json` — DPG-era v0_5 substrate, now bannered

The file's `inputs` field references `data/v0_5_canonical_majority_2026_eds_da_anchored.gpkg` — a v0_5 DPG approximation, not the official Elections Alberta shapefile. The file name `phase4c_maup_summary.json` is ambiguous and could be (and was) read as a canonical artifact. The current canonical Phase 4C result is `data/outputs/phase4c_canonical_results.json` (regenerated successfully today against the canonical EA shapefiles). **Fix:** added a top-level `_SUPERSEDED` field to the JSON pointing readers at the canonical artifact.

### 3. `findings/phase4f_summary.json` — DPG-era v0_5 hardstop validation, now bannered

Same pattern: inputs are v0_5 DPG approximations of the 2026 EDs being validated against a 2021 census population baseline. The "81 of 86 majority / 87 of 89 minority hardstops" figures cited in monograph §3.3 derive from this file. The hardstops are real signals (population deviation against 2021 census), but the v0_5 ED shapefiles used for the validation were the DPG approximations, not canonical EA shapefiles. The canonical-substrate population validation was performed separately and lives in `findings/cycle_lag_analysis.md` and `data/INTEGRITY_STATUS.md`. **Fix:** same `_SUPERSEDED` banner. The monograph still cites the v0_5-substrate hardstop counts; per the existing §3.2/§3.3 framing this is acknowledged as a "composite signal (real DPG transcription error plus cycle-lag growth heterogeneity, not separable from public data alone)" and the §4.1.4 sunset clause binds the audit to recomputation. Recomputation against canonical shapefiles is queued in TODO_REMEDIATION as T4.1 follow-up; **the v0_5 framing in the monograph is therefore disclosed but not yet fully replaced**.

### 4. Convention confusion between `phase4c_canonical_results.json` and `simulation_real_map_scores_canonical.json`

The two files have been confusing readers (including this referee pass) by reporting opposite-sign-convention values for the same canonical real maps:

| Field | `phase4c_canonical_results.json` | `simulation_real_map_scores_canonical.json` |
|---|---|---|
| Convention | NDP-as-R Warrington | UCP-as-R Warrington |
| Minority seats@50/50 | 0.4831 (NDP seat fraction) | 0.5169 (UCP seat fraction) |
| Minority declination | +0.0463 (positive = NDP advantage) | −0.0770 (positive = UCP advantage) |

The values reconcile exactly: 0.4831 (NDP) + 0.5169 (UCP) = 1.0 ✓; signs of declination are opposite by construction. **Both files are canonical**; they use opposite party references. The published monograph and locale strings consistently use the UCP-as-R chain convention. **Fix:** a `_CONVENTION_NOTE` field was added to `phase4c_canonical_results.json` making the convention swap explicit, so a future analyst reading just one file will know which party reference it uses.

## Not contaminated — false alarms ruled out

### `data/shapefiles/derived/va_polygons_with_*_votes.gpkg`

Despite the path containing the word "derived," these are **not** DPG approximations. They are the canonical Elections Alberta VA shapefile (`va_2023_election_day_votes.gpkg`) with extra columns joined onto it (`parent_ed_2019`, `va_ndp_full`, `va_ucp_full`). Same 4,765 rows, same CRS (EPSG:3400), same geometry. Multiple active scripts read these files for advance-vote analysis; their content is canonical.

### `data/v0_1_redist_crossvalidation_s50.rds`

The R cross-validation `.rds` carries a v0_1 filename. It is acknowledged in `findings/redist_python_comparison.md` as "pre-canonical naming; canonical-era `.rds` not separately preserved — canonical CSV is the authoritative artifact." Honest disclosure already in place.

### `data/maps/hires/v0_1_*.png` and `data/maps/hires_v2/v0_2_*.png`

These are PNG renders of the commission's own published map images from the commission report appendix. The `v0_x` prefix is the audit's own ingestion version of those source images, not a DPG approximation of the maps themselves. They are inputs, not outputs.

### `MAJ_V9` / `MIN_V9` variables in `analysis/scripts/advance_vote_sensitivity.py`

The variables are misleadingly named but point at canonical EA shapefile paths (`data/shapefiles/canonical/ea_majority_2026_eds.gpkg` and the minority equivalent). Cosmetic only; the data is canonical.

## Cosmetic but worth queuing — non-blocking cleanup

The following files have `v0_x` references that survive in docstrings, output filenames, chart titles, or printed labels, despite computing from canonical data. None contaminates a published number, but they confuse readers and tooling:

| File | Issue | Severity |
|---|---|---|
| `analysis/scripts/annotate_ensemble_seats_chart.py` | Chart title reads "v0_9 substrate, 2023 votes" even when run against canonical chain CSVs. SVG output filename `ensemble_distribution_250k_v0_9_seats_at_50_50.svg` is stale (canonical is 1.01M, not 250k). | low-cosmetic |
| `analysis/scripts/advance_vote_sensitivity.py` | Output labels `v0_9_majority` / `v0_9_minority` despite reading from canonical paths. CSV/JSON downstream consumers may attribute "v0_9 era" to canonical results. | medium-cosmetic |
| `analysis/scripts/338canada_*.py` (3 files) | Headline comment `v0_1_338canada_*.py` is stale; data and methods are current. | low-cosmetic |
| `analysis/scripts/article_figures.py` | Header `v0_1_article_figures.py` is stale; outputs are current. | low-cosmetic |
| `analysis/methodology/audit_dependency_graph.json` | `schema_version: "v0_1"`; contains a mix of `L2:mcmc_ensemble_canonical` and `L2:v0_1_assignment_va_attribution_*` nodes. Anyone running the dependency-graph tooling sees a confused topology. | medium-cosmetic |
| `analysis/methodology/szat_methodology.md`, `analysis/methodology/methodological_defenses.md`, `analysis/methodology/plain_language_defense.md`, `analysis/methodology/reference/banff_extension_population_check.md`, `analysis/methodology/reference/airdrie_quadrant_demographic_comparison.md` | Cite `data/shapefiles/derived/` paths in walkthroughs. The paths themselves are valid (those files exist and are canonical content); the framing language sometimes describes them as "DPG-derived" when they are not. | low-cosmetic |

**Resolution path (queued as T4.5 in `TODO_REMEDIATION.md`):** sweep all files above to either (a) drop the v0_x label entirely or (b) replace with a "canonical-era" / explicit-substrate label. None of this changes any number.

## The structural risk that remains

The only structural risk is the **monograph §3.3 hardstop count** ("81 of 86 majority hardstop failures" / "87 of 89 minority hardstop failures"). These numbers derive from the v0_5-substrate `phase4f_summary.json` which has now been bannered as superseded. The honest reading the monograph already carries is:

> "The 81 of 86 majority and 87 of 89 minority hardstop failures documented in `data/INTEGRITY_STATUS.md` are therefore a composite signal: **real DPG transcription error plus cycle-lag growth heterogeneity, not separable from public data alone**. The §4.1.4 sunset clause binds the audit to recomputation if Elections Alberta releases official shapefiles."

Official shapefiles have been released and recomputation has not yet been done for the hardstop-validation specifically. **Queue:** `TODO_REMEDIATION.md` item T4.1 expanded to add a canonical-substrate recomputation of the hardstop validation. The monograph text continues to disclose the composite nature of the v0_5 signal honestly, but a real canonical recomputation will tighten that footnote.

## Confidence level on "no contamination of published canonical numbers"

**High** for the partisan-bias headline numbers (EG, MM, declination, seats@50/50, Mahalanobis joint, Bonferroni bound): these all derive from `data/simulation_checkpoints_canonical/chain[0-3]_samples.csv` (chain output computed against canonical Elections Alberta shapefiles using `mcmc_ensemble_canonical.py` and `phase4c_canonical_attribution.py`). The real-map scoring at `data/outputs/simulation_real_map_scores_canonical.json` is from the same canonical pipeline. Phase 4C re-run today against canonical inputs reproduces all reported values exactly. No DPG substrate enters this pipeline.

**Medium** for the structural-lane numbers (population MAD, compactness, anchoring, neighbour-drain). The metric computations themselves run on canonical shapefiles, but the *thresholds* against which those metrics are scored were calibrated partly during the DPG era. Per §5.7's "stress-test grades" framing, the thresholds are conservative and reaffirmed under canonical recomputation, but the threshold-calibration provenance is documented at `findings/checklist_baseline_scoring.md` and is open to re-verification.

**Medium** for the §3.3 hardstop count (see above).

**Low** for one specific class of cited figures: any number with a "v0_5" / "v0_8" / "v0_9" provenance trail through `phase4f_summary.json` or `phase4c_maup_summary.json`. These now carry SUPERSEDED banners. The monograph still cites them in §3.3 with honest composite-signal language but the numbers themselves are not canonical.

## What would close the audit completely

1. Recompute the population-hardstop validation against canonical EA shapefiles and replace `phase4f_summary.json` with a canonical-substrate equivalent.
2. Sweep all cosmetic v0_x labels per the table above (TODO_REMEDIATION T4.5).
3. Audit-dependency-graph rebuild against the current script set (drop v0_1 node names; add canonical equivalents).
4. Add a canonical-paths-only assertion (similar to the build_cover.py fix) to any other script that loads ED shapefiles, as a defense-in-depth measure against future fallback regressions.

Items 1, 3, 4 are now queued as TODO_REMEDIATION T4.5 (cosmetic sweep) and T4.6 (re-execute hardstop validation; rebuild dep graph). Item 2 is in T4.5 with low priority.

## Reproducibility of this scan

The scan was performed by:

```bash
# Find non-archived files referencing DPG/v0_x
find . -path ./node_modules -prune -o -path ./.git -prune -o \
    -path ./archive -prune -o -path ./viewer/node_modules -prune -o \
    -type f \( -name "*.py" -o -name "*.md" -o -name "*.json" \) -print \
  | xargs grep -l -iE "DPG|v0_[0-9]+|provisional|derived_geom|approximate_shape"

# Find scripts with silent-fallback patterns (the build_cover.py class)
grep -l -E "CANDIDATES|first_existing|for path in.*\.exists" analysis/scripts/*.py

# Find scripts that load v0_x or derived/ at runtime (not just in docstrings)
grep -nE "gpd\.read_file\(.*v0_|gpd\.read_file\(.*derived|read_csv\(.*v0_" analysis/scripts/*.py
```

Anyone re-running this scan against a future commit should hit zero results in classes (b) and (c) once T4.5 closes.
