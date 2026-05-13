# Data Acquisition Manifest

Acquired 2026-04-22 by data-acquisition session. All files are ready for offline analysis; the next Phase 4 / RT analysis session can run without network access.

## Files committed to `data/` (small, versioned)

| File | Size | Source | Integrity | Use |
|------|------|--------|-----------|-----|
| `alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.*` | 3.9 MB | https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip | 87 polygons, EPSG:3401, loads clean | 2019 baseline boundaries for A1/A2, Phase 4B dissolves, maps |
| `alberta_2023_vas/EA_Voting_Area_Boundaries_2023.*` | 17 MB | https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip | 4,765 polygons, EPSG:3400, matches polls CSV exactly | RT3 vote-to-geometry attribution, Phase 4B dissolves into proposed 2026 EDs |
| `alberta_2021_das.gpkg` | 15.5 MB | StatsCan `lda_000a21a_e.zip` (national DA, filtered to PRUID=48) | 6,203 Alberta DAs, EPSG:3347, loads clean | Phase 4B population dissolves onto 2026 proposed boundaries; urban/rural weighting for A2 |
| `calgary_wards.geojson` | 638 KB | `data.calgary.ca` Socrata dataset `tz8z-hyaz` (GeoJSON export) | 14 wards, EPSG:4326, current (updated 2026-04-08) | A2 third robustness check — Calgary ward-based ED classification |
| `alberta_2019_populations.csv` | 5.5 KB | Parsed from 2017 EBC Final Report pp. 60-61 (see `.temp/ebc_2017_final.pdf`) | 87 rows: ed_name, population, variance_pct | A1/A2 on 2019 baseline (commission's own 2017 population snapshot) |
| `minority_2026_populations_appendixE.csv` | 2.7 KB | Parsed from commission final report Appendix E, p. 357 | 89 rows: num, proposed_2026, population | Cross-check of existing `minority_2026_populations.csv` |
| `minority_hybrid_crosswalk.csv` | 5.5 KB | Heuristic mapping of 89 minority-proposed EDs to 87 2019 EDs + hybrid flag | See caveats in `analysis/appendix_e_recon_log.md` | Analogous to `majority_hybrid_crosswalk.csv` for minority audit arm |

Existing files in `data/` (pre-session, untouched): `2015_results.xlsx`, `2023_results.xlsx`, `alberta_2015_results.csv`, `alberta_2019_results.csv`, `alberta_2023_results.csv`, `majority_2026_populations.csv`, `majority_hybrid_crosswalk.csv`, `minority_2026_populations.csv`, `submission_search_dataset.csv`.

## Files retained in `.temp/` (gitignored — large binaries)

| File | Size | Source | Use |
|------|------|--------|-----|
| `commission_report.pdf` | 80.0 MB | https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf | Raw 2025-2026 EBC Final Report (362 pages) — re-parse as needed |
| `ebc_2017_final.pdf` | 34.8 MB | https://www.elections.ab.ca/uploads/abebc_2017_rpt_final.pdf | 2016-17 EBC Final Report (197 pages) — source for 2019 populations |
| `ebc_2010_final.pdf` | 59.1 MB | https://www.elections.ab.ca/uploads/abebc_2010_rpt_final.pdf | 2009-10 EBC Final Report — source for 2015-election boundaries (see gap note in log) |
| `lda_2021_national.zip` | 93.2 MB | https://www12.statcan.gc.ca/.../lda_000a21a_e.zip | National DA shapefile, AB-filtered subset saved to `data/alberta_2021_das.gpkg` |
| `lda_extract/` | 162 MB | extracted from above | Delete if space is tight; Alberta subset in GeoPackage is sufficient |
| `2019_eds.zip`, `2023_vas.zip` | 15 MB total | Elections Alberta originals | Source archives of the already-extracted shapefiles |
| `appendix_e_text.txt` | 200 KB | pdfplumber extraction of pp. 285-362 | Appendix E raw text for future re-parsing |
| `ebc_2017_text.txt` | 306 KB | pdfplumber extraction of 2017 report | Full-text cache |

## Gaps (see `analysis/data_acquisition_log.md` for details)

- **2015-era boundary crosswalk (2010 commission → 2017 commission)**: not found as a machine-readable file. The 2010 final report contains the pre-2019 87-ED boundaries in prose, but no crosswalk table. Would require manual construction from the 2010 report maps if RT3 cross-election checks against 2015 data are desired.
- **Minority prose hybrid crosswalk**: Appendix E does not contain a tabular current→proposed mapping. The `minority_hybrid_crosswalk.csv` was built by name-matching the minority's 89 proposed EDs against the 87 current EDs using Jaccard token overlap (threshold 0.4) plus exact-name match. 73 rows were mapped confidently; 16 proposed EDs had no current-2019 name match (likely new hybrids or renamings); 14 current-2019 EDs had no minority-proposed match (likely merged/absorbed). The hybrid flag is a heuristic based on multi-part names combining a city and a rural-marker token — **review manually before using for statistical claims**.
