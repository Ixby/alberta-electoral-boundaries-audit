# Data Acquisition — Technical Log

Session: 2026-04-22, agent: data-acquisition.

## URL verification (HEAD requests)

| URL | Result |
|-----|--------|
| `https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip` | 200, 2.72 MB, application/x-zip-compressed ✓ |
| `https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip` | 200, 11.8 MB, application/zip ✓ |
| `https://www12.statcan.gc.ca/.../lda_000a21a_e.zip` | HEAD failed ("Exceeded 30 redirects"). GET with browser User-Agent works: 200, 93.2 MB, application/x-zip-compressed |
| `https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf` | 200, 80.0 MB, application/pdf ✓ |
| `https://www.elections.ab.ca/uploads/2017-EBC-Final-Report.pdf` | **404** — wrong pattern. Actual URL found via web search: `https://www.elections.ab.ca/uploads/abebc_2017_rpt_final.pdf` (36.5 MB, 200). |

## What worked

### 1. Elections Alberta shapefiles
Both downloaded and extracted cleanly on first attempt.

- 2019 EDs: 87 polygons, EPSG:3401, loads in geopandas, total area 662,581 km².
- 2023 VAs: 4,765 polygons, EPSG:3400, loads in geopandas, same total area. Exactly matches the 4,765 unique (ed_2019, voting_area) pairs in `analysis/polls_2023_unified.csv`.

### 2. StatsCan 2021 DAs
National shapefile (168 MB .shp) downloaded to `.temp/`, then filtered using pyogrio's `where="PRUID='48'"` clause (1.6 s for 6,203 AB rows). Saved to `data/alberta_2021_das.gpkg` at 15.5 MB. CRS EPSG:3347. Attribute fields: `DAUID, DGUID, LANDAREA, PRUID, geometry`.

**Note**: This file has **no population attribute** attached. StatsCan distributes geographies and the census data separately. The 2021 population table (98-401-X2021006) is a separate download. That file was **not** included in this session because:
- It's served via a JavaScript-based download builder at `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/`, not a direct URL.
- The DA-level population can be retrieved from StatsCan's WDS API in a single call: `https://www12.statcan.gc.ca/rest/census-recensement/2021/GeographyFile?... ` but it requires a product-specific parameter.
- For minimum viable Phase 4B, the population can be dissolved from the 2023 VA populations (which are in `v0_1_alberta_2023_results.csv` implicitly via ballot counts) or derived from per-ED 2019 populations in `v0_1_alberta_2019_populations.csv`.

**Recommended next step**: if DA-level population is needed, use StatsCan's 2021 Census Profile CSV at `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E` with geography = Dissemination Area. I did not attempt this in-session because the download endpoint requires form POST / session cookies.

### 3. Commission PDF — Appendix E parse
- PDF downloaded to `.temp/commission_report.pdf` (80 MB, 362 pages).
- Appendix E starts at **page 285** (confirmed by pdfplumber search).
- Extracted pages 285-362 to `.temp/appendix_e_text.txt` (200 KB).
- **Machine-readable table found**: on page 357 the minority lists all 89 proposed EDs with populations. Parsed 89 rows into `data/v0_1_minority_2026_populations_appendixE.csv`.
- **No tabular current→proposed crosswalk** in Appendix E. Built a synthetic crosswalk using token-overlap heuristics (see `appendix_e_recon_log.md`).

### 4. 2017 EBC Final Report (for 2019-baseline populations)
- Initial URL guess 404'd. Web search located `abebc_2017_rpt_final.pdf`.
- Two-column population table on pages 60-61 parsed into 87 (name, population, variance%) rows.
- Saved as `data/v0_1_alberta_2019_populations.csv`.

### 5. Calgary wards
- First attempted Socrata resource endpoint `https://data.calgary.ca/resource/r9vx-mhnf.geojson` — returned 53-byte stub (geometry-less features).
- Catalog search revealed `r9vx-mhnf` is a *map* view; the actual *dataset* is `tz8z-hyaz`. Retrieved 14 wards (638 KB GeoJSON, EPSG:4326, updated 2026-04-08).

## What did NOT work / gaps

### 2015-election boundary crosswalk
- **2010 EBC Final Report** (61.9 MB) downloaded for reference, but contains only prose + PDF-rasterised maps of the pre-2019 boundaries. No machine-readable crosswalk table from the 2010-era 87 EDs to the 2017-era 87 EDs.
- **No file `data/v0_1_2015_to_2019_crosswalk.csv` was produced**. Constructing this would require manually transcribing from the 2010 report's ED-by-ED narrative.
- **Impact on audit**: RT3 cross-election checks using 2015 vote data cannot be done boundary-to-boundary without this crosswalk. The 2015 results file `data/2015_results.xlsx` exists and is indexed by 2010-era ED names — future analysts must treat 2015→2019 boundary shifts as a known confound.

### StatsCan DA population attribute
- Shapefile only contains geography. Population (2021 Census) is a separate download requiring interactive form submission. See "StatsCan 2021 DAs" above for the workaround path.

### Minority machine-readable hybrid crosswalk
- No such table in Appendix E. Heuristic crosswalk produced with known caveats; see `analysis/appendix_e_recon_log.md`.

## Retries / failures summary

| Task | Retries | Outcome |
|------|---------|---------|
| StatsCan DA HEAD | 1 (switched to GET with browser UA) | success |
| 2017 EBC Final Report URL | 2 (guess → web search) | success |
| Calgary wards Socrata GeoJSON | 3 (resource → geospatial export → catalog search) | success via `tz8z-hyaz` |
| 2015 boundary crosswalk | 0 (no plausible URL found) | skipped, documented as gap |

## Software environment

- Python 3.14, geopandas 1.1.3, pdfplumber 0.11.9, requests 2.33.1
- Platform: Windows 11, bash shell
- No MCP tools used for data acquisition — all direct HTTP + pdfplumber
