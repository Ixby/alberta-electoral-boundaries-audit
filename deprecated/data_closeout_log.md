# Data Closeout — Technical Log

Session: 2026-04-22, agent: data-closeout.
Follows `analysis/data_acquisition_log.md`.

## Summary table

| Gap | Status | New file(s) |
|-----|--------|-------------|
| 1. StatsCan 2021 DA populations | **ACQUIRED** | `data/alberta_2021_da_populations.csv` (6,203 DAs, Σ = 4,262,635 ✓) |
| 2. 2026 ABEBC shapefiles | **not-yet-released** | — |
| 3. Appendix E minority crosswalk (retry) | **partially acquired** | `data/v0_1_minority_hybrid_crosswalk_appendixE.csv` (22 hybrid rows) |
| 4. 2015→2019 boundary crosswalk | **partial best-effort** | `data/v0_1_2015_to_2019_crosswalk_partial.csv` (21 low-to-high-conf. rows) |
| 5. Municipal / CSD data | **ACQUIRED** | `data/alberta_2021_csds.gpkg` (423 AB CSDs) + `data/alberta_2021_csd_populations.csv` |

## Gap 1 — StatsCan 2021 DA populations

**Acquired.** Full DA-level population data for all 6,203 Alberta dissemination areas.

URLs tried:
- `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E` — form-based, no direct link.
- `https://www150.statcan.gc.ca/n1/en/catalogue/98-401-X2021006` — catalog page, links back to form.
- `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=006&FILETYPE=CSV` **← this is the direct comprehensive download URL for table 98-401-X2021006 (2.1 GB zip, 5.37 GB CSV when extracted)**.

Workflow:
1. Downloaded 2.25 GB zip to `.temp/statscan_da_profile_006.zip` via curl with browser UA.
2. Extracted via `zipfile.ZipFile.open(...)` streaming to avoid 5.37 GB unzipped file.
3. Filtered Alberta DAs (ALT_GEO_CODE starts with `48`) with `CHARACTERISTIC_ID=1` (Population, 2021).
4. Wrote columns `DAUID, DGUID, GEO_NAME, population_2021` to `data/alberta_2021_da_populations.csv`.

**Validation**: parsed 6,182 numeric values from 6,203 rows; 21 suppressed for confidentiality. Sum = **4,262,635**, which is the official StatsCan Alberta 2021 Census population count. DAUID field keys directly into `data/alberta_2021_das.gpkg`.

## Gap 2 — 2026 ABEBC shapefiles

**Not-yet-released** (as expected).

URL tried: `https://www.elections.ab.ca/resources/maps/` (2026-04-22).

Page still lists only:
- `2019Boundaries_ED-Shapefiles.zip`
- `2023Boundaries_VAs.zip`

No `2026*` filename present. The 2026 PDF maps may follow post-assent. Recommend re-check after royal assent of the final report (expected summer 2026).

## Gap 3 — Appendix E minority crosswalk re-parse

**Partially acquired.** Previous agent missed a 3-block hybrid crosswalk on pages 307-308 (PDF section VIII, "Process in Drawing the Boundaries"). These three tables explicitly map current (2019) EDs to minority-proposed (2026) hybrid EDs:

- Calgary block: 11 rows (9 existing + 2 new)
- Edmonton Capital Region block: 3 rows (1 existing + 2 new)
- Red Deer/Lethbridge block: 8 rows (all existing → renamed)

Total: **22 hybrid-riding mappings** extracted with 100% confidence. These complement the earlier `v0_1_minority_hybrid_crosswalk.csv` (token-overlap heuristic) and should be preferred where they overlap.

Written to `data/v0_1_minority_hybrid_crosswalk_appendixE.csv`.

**No full 89-row crosswalk table exists in Appendix E.** Appendix E describes each proposed ED in prose only (pages 309-362). Second-pass regex for "formerly / previously / renamed / corresponds to" language returned only 3 usable prose hits outside the 22 structured rows (all already captured by the hybrid tables). Full current→proposed mapping for the 67 non-hybrid minority EDs cannot be mechanically extracted without manual ED-by-ED reading.

## Gap 4 — 2015→2019 boundary crosswalk

**Partial best-effort.** Source: `.temp/ebc_2017_final.pdf` (197 pages, already in `.temp/`).

The 2017 EBC final report does NOT contain a structured current→new crosswalk table. However, prose on pages 20-58 identifies ~15 explicit rename/split/consolidation events and flags two area-wide consolidations:

- Central-west Alberta: 5 existing (2010-era) EDs consolidated into 4 new + 1 renamed (p52, p57).
- Southeast Alberta: 7 existing EDs consolidated into 6 (p57, p58).

Captured 21 rows into `data/v0_1_2015_to_2019_crosswalk_partial.csv` with `change_type` and `confidence` columns. Confidence ranges from `high` (explicit textual rename, e.g. Airdrie→Airdrie-East+Airdrie-Cochrane) to `low` (inferred from consolidation-list membership).

**Known limitations**:
- 2015 elections used 87 EDs from the 2010 commission, not 83 as casually stated elsewhere. The 2010 final report (`.temp/ebc_2010_final.pdf`, 61.9 MB) contains prose + raster maps but no tabular crosswalk.
- Roughly 65-70 of the 87 2015→2019 ED mappings are identity (same name, possibly minor boundary tweaks). These identity mappings are NOT listed in the CSV — analysts should treat unlisted 2015 names as presumed-identity.
- Full boundary-accurate 2015→2019 crosswalk would require either (a) manual transcription from the 2010 report's 87 ED descriptions, or (b) spatial overlay of 2010-era and 2017-era shapefiles. The 2010-era shapefile is **not publicly posted** by Elections Alberta — only the 2019 and 2023 versions are at `elections.ab.ca/resources/maps/`.

## Gap 5 — Municipal / CSD data

**Acquired.** Two deliverables:

1. `data/alberta_2021_csds.gpkg` — 423 Alberta Census Subdivision polygons, EPSG:3347, 5.5 MB.
   Fields: `CSDUID, DGUID, CSDNAME, CSDTYPE, LANDAREA, PRUID, geometry`.
   Source: `https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcsd000a21a_e.zip` (38.5 MB national cartographic boundary file, filtered `PRUID='48'`).

2. `data/alberta_2021_csd_populations.csv` — 423 rows, columns `DGUID, ALT_GEO_CODE, GEO_LEVEL, GEO_NAME, population_2021`.
   Source: filtered from `98-401-X2021005_English_CSV_data.csv` inside `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=005&FILETYPE=CSV` (197 MB zip → 2.6 GB CSV).

Together these enable programmatic §C4 community-of-interest analysis: join CSD polygons to the ED shapefile to compute, for each ED, what fraction of each CSD falls within it (split detection).

## Retries / failures

| Task | Retries | Outcome |
|------|---------|---------|
| StatsCan GEONO probe | 1 (probed 002-008 to confirm GEONO=006 is DA-level) | success |
| DA download | 1 (5.5 min for 2.25 GB) | success |
| CSD shapefile URL | 2 (searched for `lcsd000a21a_e.zip` pattern) | success |
| 2026 ABEBC shapefile watch | 1 fetch | confirmed not-yet-released |
| Appendix E deep re-parse | 1 | found 3 tables the prior agent missed (pp 307-308) |

## Remaining gaps (require human intervention)

1. **Full 2015→2019 crosswalk** — requires either manual PDF transcription (~2-3 hours for a human) or a 2010-era AB ED shapefile which is not public. Alternative: contact Elections Alberta data services directly.
2. **2026 shapefiles** — release schedule controlled by EBC/Elections Alberta; not under analyst control.
3. **Full 67-row non-hybrid minority crosswalk** — requires ED-by-ED prose reading of Appendix E (pp 309-362). Automatable with a long-context LLM pass but not with regex.

## Software environment

Unchanged from acquisition session: Python 3.14, geopandas 1.1.3, pdfplumber 0.11.9, pyogrio, requests/curl.

New direct URLs catalogued for future use:
```
https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO={001..008}&FILETYPE={CSV,TAB,IVT}
```
GEONO=001 is Canada/prov/terr; 005 is +CD+CSD; 006 is +DA; etc. Bypasses form.
