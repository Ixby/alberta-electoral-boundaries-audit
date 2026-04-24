# Legal red-team findings — `data/` artifact provenance

**Framework:** `analysis/red_team/v0_1_legal_red_team_framework.md` Dimension **D5** (Data provenance).
**Scope:** every file directly under `data/` plus sub-directories `data/alberta_2019_eds/`, `data/alberta_2023_vas/`, `data/v0_1_338_historical/` (as specified by the directive). Generated 2026-04-23.
**Total artifacts reviewed:** 88 (56 CSVs, 15 GPKGs, 1 GeoJSON, 6 JSONs, 2 XLSXs, 1 shapefile set (8 files), 1 VA shapefile set (5 files), 89 cached HTMLs and auxiliary files in `data/v0_1_338_historical/`, 2 internal README / manifest docs).
**Reference manifests consulted:** `FROZEN_MANIFEST.md`, `data/data_acquisition_manifest.md`, `data/alberta_shapefiles_README.md`, `analysis/v0_1_data_preparation.md`.

**Severity counts:** CRITICAL = 0, HIGH = 7, MEDIUM = 11, LOW = 5.

> CRITICAL findings (per D5 rules) would require (a) an artifact with no documented source anywhere in the repo, or (b) a documented source that does not match the actual contents. No artifact reviewed meets either bar — every artifact has at least a partial chain traceable through `v0_1_data_preparation.md` and the schema contents match the source claims. HIGH findings below identify the broken links in the chain to `FROZEN_MANIFEST.md`.

---

## Summary table

| # | File | Sev | One-line finding | Proposed fix |
|---|------|-----|------------------|--------------|
| 1 | `data/2015_results.xlsx` | HIGH | FROZEN_MANIFEST lists filename `2015-Provincial-General-Election-Statement-of-Vote.xlsx`; `v0_1_data_preparation.md` and `parse_2015_results.py` reference `2015PGE-Official-Results.xlsx`. One of the two is the wrong URL for the bytes actually in `data/2015_results.xlsx`. | Verify which URL actually served the xlsx on 2026-04-22, then correct the other document. Both should reference identical URL. |
| 2 | `data/v0_1_alberta_2019_results.csv` | HIGH | Source URL `https://www.elections.ab.ca/uploads/2019PGEOfficialResultsAllEDs.xlsx` is cited only in `v0_1_data_preparation.md`; NOT in `FROZEN_MANIFEST.md`. No archive. Manual per-sheet extraction, no parser script committed. | Add row to `FROZEN_MANIFEST.md`; archive the URL to Wayback; commit a parser analogous to `parse_2015_results.py`. |
| 3 | `data/submission_search_dataset.csv` | HIGH | Upstream source is 27 EBC submission batch PDFs at `https://www.elections.ab.ca/uploads/EBC2025Submissions{start}-{end}ForPosting.pdf`. None of these 27 URLs appear in `FROZEN_MANIFEST.md`. This file directly underpins `report_public.md:162` submission-count claims. | Add a table row to `FROZEN_MANIFEST.md` that either enumerates the 27 URLs or captures the pattern with a dated archival probe. |
| 4 | `data/v0_1_majority_2026_populations.csv`, `data/v0_1_minority_2026_populations.csv` | HIGH | "Manually extracted" from commission PDF pp. 44-45 and Appendix E. No parser script committed; extraction is not mechanically reproducible. `FROZEN_MANIFEST.md` references the 80 MB PDF but no script binds PDF→CSV. | Commit `analysis/parse_commission_populations.py` (pdfplumber-based) and note the page-range in each CSV header. |
| 5 | `data/v0_1_minority_hybrid_crosswalk.csv` | HIGH | File is a heuristic output (Jaccard token overlap ≥0.4 plus exact match) per `data/data_acquisition_manifest.md`. 16 proposed EDs unmapped, 14 current EDs unmapped. `data_acquisition_manifest.md` warns "review manually before using for statistical claims" — but the file is an input to downstream scripts (MCMC rescore, build_full_crosswalks). | Either (a) freeze a manually-verified version alongside the heuristic, or (b) document in the CSV header exactly which rows are heuristic-only vs. manually verified. |
| 6 | `data/v0_1_338canada_per_riding_87seat.csv` | HIGH | Scraped from `338canada.com/alberta/NNNNe.htm` on 2026-04-12. FROZEN_MANIFEST row records three probe URLs archived on Wayback (1001, 1044, 1087) — the remaining 84 URLs are unarchived at the per-page level. Track J relies on the frozen CSV, but per-row cross-check against a Wayback snapshot is available for only 3/87 ridings. | Submit the remaining 84 per-riding URLs to `web.archive.org/save/` (this was attempted in `v0_1_url_archival_log.md` but IP-blocked). |
| 7 | `data/v0_1_338_historical/*.html` (87 per-riding Wayback HTML dumps) + `per_riding_pre2023.csv`, `uniform_swing_stability.csv`, `stability_table.csv`, `alberta_landing_raw.html`, `alberta_landing_xaxis.json`, `per_riding_wayback.json`, `pre2023_per_riding_validation.json` | HIGH | Entire sub-directory (pre-2023 338Canada historical snapshots) has no row in `FROZEN_MANIFEST.md`. The HTMLs carry Wayback timestamps in their filenames (w20230529) but the chain "which per-riding Wayback URLs were scraped? on what date?" is only in `analysis/v0_1_338canada_historical.py` — not cross-indexed in the manifest. | Add a table to FROZEN_MANIFEST listing the 87 pre-2023 Wayback URLs, or at minimum reference the generating script's output manifest. |
| 8 | `data/v0_1_approximate_majority_2026_eds.gpkg`, `_approximate_minority_2026_eds.gpkg`, `_approximate_majority_2026_eds_full.gpkg` | MED | Derived from 2019 shapefile + commission Appendix A/C mappings via `v0_1_approximate_shape_analysis.py`. Source chain documented. But: file suffix `_full` is the 63-row partial, while the 57-row is labelled default — naming is inverted from what a reviewer would expect. | Add a header-line CSV alongside each GPKG documenting the row-count rationale; or rename. |
| 9 | `data/v0_1_refined_{majority,minority,v2,v3,v4,v5,v6}_2026_eds.gpkg` (12 files) | MED | Refinement chain v1→v2→v3→v4→v5→v6 exists across `v0_1_shape_refinement.py`, `_v2.py`, `_v3.py`, `_v4.py`, `_v5.py`, `_v6.*`. All scripts committed. But the minority has refinements v1→v6 while the majority stops at v3 (except v6). Reader cannot tell from filename alone which is "current". | See "Supersession / deprecation candidates" below. |
| 10 | `data/v0_1_derived_v7_majority_2026_eds.gpkg`, `_minority_v7.gpkg` | MED | New 89-row schema (vs. 57/70 in v6) via `v0_1_shape_derivation_v7.py`. Columns `source_thumbnail`, `affine_rms_m`, `disproof_n_pass` suggest this is a photo-derivation pass over commission maps — a different provenance chain than v1-v6. | Document the v7 derivation input source (which commission map thumbnails?) in a header comment in the script. |
| 11 | `data/va_polygons_with_2023_votes.gpkg` | MED | 4,765-VA substrate derived from `alberta_2023_vas/` shapefile + `analysis/polls_2023_unified.csv`. Chain documented in `v0_1_data_preparation.md` §4 and `phase_4c_prep.py`. But the file is the MCMC ensemble substrate, `polls_2023_unified.csv` is in `analysis/` not `data/`, and the integrity gates are reported in `va_spatial_integrity_report.md`. Three-hop chain for a critical artifact. | Add the integrity-gate numbers as attributes on the GPKG (or a sidecar `.json`). |
| 12 | `data/v0_1_mcmc_ensemble_samples.csv`, `_samples_100k.csv`, `_percentiles.csv`, `_percentiles_100k.csv`, `_percentiles_full.csv`, `_percentiles_full_v2.csv`, `v0_1_mcmc_real_map_scores*.json` (4 versions) | MED | Stochastic outputs. `v0_1_mcmc_real_map_scores.json` records `seed: 42` and `n_steps: 10000`; the 100k variants are at `seed: 42` (per script). But the chain between "samples → percentiles → real_map_scores" runs through multiple scripts (`v0_1_mcmc_ensemble.py`, `_100k.py`, `_full_coverage_rescore.py`, `_full_coverage_rescore_v2.py`, `_full_coverage_rescore_100k.py`) producing five percentile variants. Reviewer cannot tell which is canonical. | Document in a README which percentile file is the canonical report input. Deprecate the rest. |
| 13 | `data/v0_1_338canada_historical_snapshots.csv` | MED | 77 snapshot rows from `338canada.com/alberta/` landing page via `v0_1_338canada_historical.py`. FROZEN_MANIFEST row for the `/alberta/` landing page has both Wayback and archive.ph snapshots, so the provenance chain is complete. But the CSV has no header-line provenance annotation. | Add a `source` column or header comment with the snapshot URL. |
| 14 | `data/v0_1_338canada_reallocated_majority.csv`, `_minority.csv` | MED | Reallocated 2026 projections from 338 data. Script `v0_1_338canada_reallocate.py` is committed. Inputs (87-seat per-riding CSV, audit 2023 baseline, 2019 populations) are all traceable. Chain complete. But the note column is empty on nearly all rows, so a reviewer cannot distinguish direct-mapping from reallocation at a glance. | Populate `note` column for non-direct mappings. |
| 15 | `data/v0_1_2015_to_2019_crosswalk.csv`, `_partial.csv` | MED | Partial crosswalk built from commission report prose (2017 report pp. 37 etc.). Referenced in `v0_1_data_preparation.md` §7 as "Elections Alberta does not publish pre-2017 shapefiles" gap. Chain is prose-only. | Header comment in CSV naming page-range and prose source per row; already partially present in the `note` column. Upgrade to full-row coverage. |
| 16 | `data/v0_1_boundary_refinement_impact.csv`, `_v3.csv`, `_v4.csv`, `_v5.csv`, `_v6.csv` (missing `_v2`) | MED | Version chain v1→v3→v4→v5→v6 with v2 skipped in filenames (v2 is described as a pass-through in `v0_1_shape_refinement_v2.py:350`). Reviewer sees a discontinuous versioning. | Rename v1 → v1, clarify in a README that v2 is intentionally absent. |
| 17 | `data/v0_1_mcmc_convergence_diagnostics_100k.json` | MED | Per-metric autocorrelation diagnostics. No `seed` or `n_steps` recorded (inferred from `v0_1_mcmc_ensemble_100k.py`). Reviewer would have to open the script. | Write `seed` and `run_timestamp` into the JSON. |
| 18 | `data/v0_1_a1_legal_baseline_2019eds_2021census.csv` | MED | Produced by `v0_1_a1_legal_baseline_2021_census.py`; inputs are `data/v0_1_alberta_2019_populations.csv` (commission's 2017 report pp. 60-61) + `alberta_2021_csds.gpkg` + DA pops. Chain complete. CSV has no header annotation. | One-line header comment. |
| 19 | `data/va_pop_from_das.csv` | LOW | Cache file generated once by `v0_1_mcmc_ensemble.py` (area-weighted DA→VA overlay). Totals to StatCan 4.26M. Chain documented in `v0_1_mcmc_ensemble.md:131`. | Add a one-line source annotation in a sidecar. |
| 20 | `data/v0_1_chen_rodden_simulation.csv`, `_summary.json` | LOW | Chen-Rodden 500-plan simulation by `v0_1_chen_rodden_alberta.py`. `summary.json` records 150-plan rerun; the CSV is 500-plan. Version mismatch suggests a re-run where one file was regenerated but not the other. | Verify 500 vs 150 plan counts; regenerate both from a single seed. |
| 21 | `data/v0_1_province_wide_drift_*.csv` (3 files) | LOW | Per `v0_1_track_l_drift.py`. CSV is well-annotated with aggregation method in the `aggregation_method` column. Chain complete. | No action. |
| 22 | `data/v0_1_canadian_redistribution_base_rate.csv` | LOW | Per `v0_1_canadian_base_rate_compute.py`. Row-level `primary_source` column is populated. Chain complete. | No action. |
| 23 | `data/v0_1_cochrane_journey_to_work.csv` | LOW | StatsCan Table 98-10-0459 Cochrane filter. URL is in FROZEN_MANIFEST marked "unarchived". | Submit to Wayback. |
| 24 | Remaining well-documented artifacts (housekeeping) | LOW | See closing list. | — |

---

## Detailed findings: CRITICAL and HIGH

### HIGH-1. `data/2015_results.xlsx` URL mismatch between reproducibility documents

**Files:** `data/2015_results.xlsx`
**Dimension:** D5 + D1 (evidentiary chain)
**Observation.**
- `FROZEN_MANIFEST.md` row 36 names the source as `https://www.elections.ab.ca/uploads/2015-Provincial-General-Election-Statement-of-Vote.xlsx`.
- `analysis/v0_1_data_preparation.md` L50 names the source as `https://www.elections.ab.ca/uploads/2015PGE-Official-Results.xlsx`.
- `analysis/parse_2015_results.py` header L4 names the source as `2015PGE-Official-Results.xlsx`.

The two filename forms refer to potentially different files (the second looks like the 2017 commission's redistribute-era filename; the first is the official post-election Statement of Vote style). A third party reproducing the audit cannot tell which URL actually produced the 1,104,073-byte file in `data/`. The xlsx loaded cleanly with 87 sheets matching ED01-ED87 naming, so contents are internally consistent. But the URL is the one evidentiary claim a cross-examiner tests first.

**Cross-exam question.** "Your FROZEN_MANIFEST says one URL, your parser script says another. Which URL actually served the bytes in `data/2015_results.xlsx` on 2026-04-22?"

**Recommendation.** Resolve the discrepancy: either (a) re-curl both URLs and keep whichever returns 200 + matches the SHA-256 of the committed file, then update the losing document, or (b) if both URLs serve the same bytes (Elections Alberta may alias them), document the aliasing explicitly in FROZEN_MANIFEST.

---

### HIGH-2. `data/v0_1_alberta_2019_results.csv` upstream URL not in FROZEN_MANIFEST

**Files:** `data/v0_1_alberta_2019_results.csv`
**Dimension:** D5
**Observation.**
- `v0_1_data_preparation.md` L40 names source as `https://www.elections.ab.ca/uploads/2019PGEOfficialResultsAllEDs.xlsx`.
- `FROZEN_MANIFEST.md` contains rows for 2015 and 2023 Statements of Vote but **no row for the 2019 xlsx**.
- No raw `data/2019_results.xlsx` is committed (only the parsed CSV).
- Extraction method: "manual per-sheet CSV extraction" per `v0_1_data_preparation.md` — no parser script.

The 2019 CSV underpins every cross-election statement in the audit. Without a URL archived in FROZEN_MANIFEST and a parser script committed, a third party cannot re-derive the 87-row CSV from the upstream.

**Cross-exam question.** "Where in this repository is the URL for your 2019 election data archived against Wayback, and what script parsed the xlsx to CSV?"

**Recommendation.**
1. Add a row to `FROZEN_MANIFEST.md` for the 2019 xlsx with a live URL + Wayback snapshot.
2. Commit `analysis/parse_2019_results.py` analogous to `parse_2015_results.py`.
3. Optionally: commit the raw `data/2019_results.xlsx` for belt-and-suspenders preservation.

---

### HIGH-3. `data/submission_search_dataset.csv` upstream 27 PDFs not in FROZEN_MANIFEST

**Files:** `data/submission_search_dataset.csv` (72 rows = 70 hits + 1 OCR-added hit + 1 summary)
**Dimension:** D5 (upstream source traceability)
**Observation.**
- Source: 27 EBC submission batch PDFs at `https://www.elections.ab.ca/uploads/EBC2025Submissions{start}-{end}ForPosting.pdf` pattern, enumerated in `submission_search.py:44-50`.
- `FROZEN_MANIFEST.md` contains **no rows for any of the 27 URLs**. Only the submission landing page is referenced indirectly through `data_preparation.md` L139.
- The CSV directly supports `report_public.md:162` public-support count claims ("three in support, four opposed, fifteen neutral" etc.).
- The 27 PDFs themselves are gitignored under `.temp/submissions/` (not committed).

A third party reproducing the `report_public.md:162` counts must re-download the 27 PDFs. If any URL drifts, the count cannot be reproduced. FROZEN_MANIFEST is specifically the anti-drift document, yet the 27 most consequence-bearing URLs are not in it.

**Cross-exam question.** "Your report says 'three submissions in favour and only one opposed.' What is the source URL that, if drifted tomorrow, would invalidate this count? Where is that URL archived?"

**Recommendation.** Add a table block to `FROZEN_MANIFEST.md`:
```
## EBC 2025 submission archive
| Batch | URL | Last verified | Wayback | archive.ph |
|-------|-----|---------------|---------|------------|
| R1 1-50 | ...EBC2025Submissions1-50ForPosting.pdf | 2026-04-22 | ... | ... |
| R1 51-100 | ... | ... |
| ... (27 rows) | ... |
```

Submit all 27 URLs to `web.archive.org/save/` once IP quota resets.

---

### HIGH-4. `v0_1_majority_2026_populations.csv` and `_minority_2026_populations.csv` — no parser script for the commission-PDF extraction

**Files:** `data/v0_1_majority_2026_populations.csv`, `data/v0_1_minority_2026_populations.csv`
**Dimension:** D4 (methodology reproducibility) + D5
**Observation.**
- Both files are per `v0_1_data_preparation.md` "manually extracted from pp. 44-45" (majority) and "manually extracted from Appendix E variance table" (minority).
- No parser script committed. A reproducer must open the 80 MB PDF, find the correct tables, and retype 89 rows × 4 columns.
- `data/v0_1_minority_2026_populations_appendixE.csv` is a second extraction that "corroborates the first with minor rounding differences" — but that second file exists only because someone else re-extracted; it's a one-off corroboration, not a mechanical replay.
- These two files are inputs to A1 legal baseline, packing/cracking, marginal seats, MCMC, Chen-Rodden — the entire Section A/B apparatus.

**Cross-exam question.** "You base your Section A population-equality findings on two CSVs that were typed by hand from a 80-megabyte PDF. Where is the parser that a reproducer would run?"

**Recommendation.** Commit `analysis/parse_commission_populations.py` using `pdfplumber.extract_tables()` on pp. 44-45 for majority and on Appendix E for minority. Include a diff-check against the existing CSVs. This is ≤ 50 lines of code and closes a D4+D5 gap in one pass.

---

### HIGH-5. `v0_1_minority_hybrid_crosswalk.csv` — heuristic output labelled as data

**Files:** `data/v0_1_minority_hybrid_crosswalk.csv` (also the `_appendixE.csv` variant)
**Dimension:** D5 + D4
**Observation.**
- Generated by Jaccard token overlap (threshold 0.4) + exact match per `data/data_acquisition_manifest.md` L35.
- Of 89 minority-proposed EDs: 73 mapped confidently, 16 new names, 14 current EDs unmapped. The manifest explicitly warns: "review manually before using for statistical claims."
- But the file IS an input to `v0_1_build_full_crosswalks.py`, `v0_1_mcmc_full_coverage_rescore*.py`, `v0_1_approximate_shape_analysis.py`, and `phase_4c_prep.py`. All of these produce statistical claims.
- No manually-verified override file exists.

**Cross-exam question.** "Your own data-acquisition manifest tells readers not to use this file for statistical claims, yet five downstream scripts that produce statistical claims read it as input. Explain the discrepancy."

**Recommendation.**
1. Freeze a manually-verified version (`v0_1_minority_hybrid_crosswalk_verified.csv`) with all 89 rows checked against commission Appendix E text and maps.
2. In the heuristic file, add a `manual_verified` boolean column populated TRUE only where a human has signed off on the row.
3. Downstream scripts should refuse to run unless the verified file exists.

---

### HIGH-6. `v0_1_338canada_per_riding_87seat.csv` — per-riding archive coverage is 3/87

**Files:** `data/v0_1_338canada_per_riding_87seat.csv`
**Dimension:** D1 + D5
**Observation.**
- FROZEN_MANIFEST row 63 records three probe URLs (1001, 1044, 1087) archived on Wayback on April 12, 2026.
- The remaining 84 per-riding URLs were NOT archived. The manifest states: "The per-riding pages used by Track J; snapshot date April 12, 2026; three probe pages preserved on Wayback as representative of the 87-URL pattern — the frozen scraped CSV under `data/` is the authoritative artefact."
- This is an explicit acknowledgment that 84 of 87 URLs have no independent Wayback preservation. The audit's position is that the CSV itself is authoritative. A hostile cross-examiner would argue the CSV could have been tampered with post-scrape; the Wayback snapshots are the independent preservation layer and they cover only 3/87.

**Cross-exam question.** "For 84 of your 87 ridings, there is no independent archive of the 338Canada page. How does a fact-checker verify that your scraped CSV matches what was actually on the website on April 12, 2026?"

**Recommendation.** When IA daily bandwidth block resets (see FROZEN_MANIFEST "Chrome-based archival retry" section), submit the 84 remaining per-riding URLs via a signed-in Internet Archive session. Update the FROZEN_MANIFEST snapshot column for each.

---

### HIGH-7. `data/v0_1_338_historical/` — 87 per-riding Wayback HTMLs, entire directory absent from FROZEN_MANIFEST

**Files:** `data/v0_1_338_historical/riding_1001_w20230529.html` through `riding_1087_w20230529.html` (87 files) + `per_riding_pre2023.csv`, `uniform_swing_stability.csv`, `stability_table.csv`, `alberta_landing_raw.html`, `alberta_landing_xaxis.json`, `per_riding_wayback.json`, `pre2023_per_riding_validation.json`
**Dimension:** D5
**Observation.**
- This sub-directory contains Wayback-cached 338Canada HTML dumps, timestamped 2023-05-29 in filename. Source URLs are presumably `https://web.archive.org/web/20230529.../338canada.com/alberta/NNNNe.htm`.
- `FROZEN_MANIFEST.md` has no row for this directory. The Wayback URLs are recorded only in `data/v0_1_338_historical/per_riding_wayback.json` (22 KB) as script-internal state.
- Generating script: `v0_1_338canada_historical.py`.
- Pre-2023 seat stability is a published finding (stability_table.csv is the one-liner).

**Cross-exam question.** "Your pre-2023 seat-stability table (67 maj / 66 min) rests on 87 Wayback-archived HTMLs. Where in FROZEN_MANIFEST is each of those 87 Wayback URLs recorded?"

**Recommendation.** Add a "338Canada historical snapshots" block to FROZEN_MANIFEST. Alternatively, since the HTMLs themselves are committed to the repo (~140 KB each × 87 = 12 MB), declare them the authoritative record and point FROZEN_MANIFEST at `per_riding_wayback.json` for the URL list.

---

## MEDIUM findings (table-only)

All MEDIUM items are captured in rows 8-18 of the summary table above. None block release; each is a gap that a careful reviewer would note.

---

## LOW / housekeeping

- `va_pop_from_das.csv`, `v0_1_chen_rodden_simulation.csv`, `v0_1_chen_rodden_summary.json`, `v0_1_province_wide_drift_*.csv` (3), `v0_1_canadian_redistribution_base_rate.csv`, `v0_1_cochrane_journey_to_work.csv` — provenance chain is complete; add one-line source annotations in file headers where absent.
- Root-level `data/alberta_shapefiles_README.md` and `data/data_acquisition_manifest.md` are the two internal docs that already do most of the provenance heavy lifting. Keeping them both is fine — but they disagree on file scope (the manifest says 7 files were acquired in the 2026-04-22 session, the shapefile README describes 2019 EDs and 2023 VAs only). Consider merging.
- `data/v0_1_338_historical/pre2023_per_riding_validation.json` — small JSON with a pearson_r coefficient; no header comment naming what is being validated.
- CPG files (`.cpg`) in both shapefile directories are 5-byte UTF-8 declarations — correct and standard, noted for completeness only.
- Naming inconsistency: some files are `v0_1_*` (project prefix) while others are plain (e.g. `hybrid_adjacent_vas.csv`, `va_pop_from_das.csv`). This is cosmetic.

---

## Supersession / deprecation candidates

The following files are superseded by later versions of the same analysis and are candidates for `deprecated/`:

| File | Superseded by | Rationale |
|------|---------------|-----------|
| `data/v0_1_refined_majority_2026_eds.gpkg` (v1) | `v0_1_refined_v6_majority_2026_eds.gpkg` (v6) and `v0_1_derived_v7_majority_2026_eds.gpkg` (v7) | v1 of the majority refinement is a pass-through (see `v0_1_shape_refinement_v2.py:350`); v6 and v7 are the current analytic substrates. |
| `data/v0_1_refined_minority_2026_eds.gpkg` (v1) | `v0_1_refined_v6_minority_2026_eds.gpkg` + `_v6_minority_2026_eds_full.gpkg` + `v0_1_derived_v7_minority_2026_eds.gpkg` | 3 subsequent versions. |
| `data/v0_1_refined_v2_majority_2026_eds.gpkg` | `v6`, `v7` | Intermediate step. |
| `data/v0_1_refined_v2_minority_2026_eds.gpkg` | `v6`, `v7` | Intermediate step. |
| `data/v0_1_refined_v3_majority_2026_eds.gpkg` | `v6`, `v7` | Intermediate step. |
| `data/v0_1_refined_v3_minority_2026_eds.gpkg` | `v6`, `v7` | Intermediate step. |
| `data/v0_1_refined_v4_minority_2026_eds.gpkg` | `v6`, `v7` | Intermediate step. |
| `data/v0_1_refined_v5_minority_2026_eds.gpkg` | `v6`, `v7` | Intermediate step. |
| `data/v0_1_approximate_majority_2026_eds_full.gpkg` (63 rows) | `v0_1_refined_v6_majority_2026_eds.gpkg` (89 rows) or `v0_1_derived_v7_majority_2026_eds.gpkg` (89 rows) | "_full" suffix is misleading; 63-row version is superseded by 89-row derived. |
| `data/v0_1_approximate_minority_2026_eds.gpkg` (70 rows) | `v0_1_refined_v6_minority_2026_eds.gpkg` | Earlier refinement step. |
| `data/v0_1_boundary_refinement_impact.csv`, `_v3.csv`, `_v4.csv`, `_v5.csv` | `_v6.csv` | v6 is the current. |
| `data/v0_1_compactness_scores.csv` | `v0_1_compactness_scores_refined.csv` | `_refined` supersedes. |
| `data/v0_1_mcmc_ensemble_percentiles.csv`, `_full.csv`, `_full_v2.csv` | `_100k.csv` (100k-step canonical) and `_full_v2.csv` (full coverage v2) | Keep `_100k.csv` and `_full_v2.csv`; deprecate the other two. Or: pick one canonical and document in a README. |
| `data/v0_1_mcmc_real_map_scores.json`, `_full.json`, `_full_v2.json` | `_100k.json` (canonical) + `_full_v2.json` (full coverage) | Same rationale. |
| `data/v0_1_2015_to_2019_crosswalk_partial.csv` | `v0_1_2015_to_2019_crosswalk.csv` | Partial was upgraded to full; partial can be moved to `deprecated/` or left as a diff reference. |
| `data/v0_1_minority_hybrid_crosswalk_appendixE.csv` | `v0_1_minority_hybrid_crosswalk.csv` (heuristic) or a new verified variant | Two minority crosswalks in `data/` without a canonical-selector. |

**Before moving to `deprecated/`:** verify each file is not still read as input by an active script. The check is one `Grep` sweep per filename. Several of these intermediate GPKGs ARE read by intermediate shape refinement scripts (`v0_1_shape_refinement_v3.py` reads v2's output, etc.). That's expected for a refinement chain. Moving means breaking the chain; keep the intermediates in place and mark them "pipeline stage N of 7" in a manifest, not in `deprecated/`.

---

## Notes for the consolidated legal red-team pass

- No CRITICAL D5 findings means the `data/` layer does not block release on data-provenance grounds.
- The seven HIGH findings cluster on two themes: (a) FROZEN_MANIFEST.md is incomplete for the submission PDFs, 2019 xlsx, and 338 historical Wayback URLs — that's a straightforward manifest-update pass; and (b) two committed CSVs (majority/minority populations, minority hybrid crosswalk) were human-extracted with no mechanical parser, leaving a D4+D5 gap that a parser commit would close.
- Release readiness: D5 is GREEN-with-remediation. Tighten the seven HIGHs before public release.
