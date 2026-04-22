# Frozen Manifest — external URLs and data-source last-access log

**Audit:** Alberta Electoral Boundaries Audit, report_academic.md v0.2
**Frozen:** 2026-04-22
**Purpose:** Reproducibility against URL drift. Every external source used
anywhere in the audit is listed here with the date and status of the most
recent successful access. If a URL has drifted by the time someone
attempts reproduction, this file names the exact content that was
retrieved so the reproducer can search for a mirror.

Addresses red-team attack C9 (*"Reproducibility claims over-promise;
URLs will drift"*). Pinned library versions live in `requirements.txt`;
the pinned interpreter in `setup.md`.

---

## Primary election and commission sources

| URL | Last verified | Status | Bytes | Notes |
|-----|---------------|--------|-------|-------|
| https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx | 2026-04-22 | 200 OK | 1.7M Elec Day + 1.4M Advance rows | Source of `data/2023_results.xlsx` |
| https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf | 2026-04-22 | 200 OK | 80.0 MB | 362 pp. Source of Appendix A (majority), Appendix E (minority), chair Addendum |
| https://www.elections.ab.ca/uploads/abebc_2017_rpt_final.pdf | 2026-04-22 | 200 OK | 36.5 MB | Source of 2019-baseline populations |
| https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip | 2026-04-22 | 200 OK | 2.72 MB | 87 ED polygons EPSG:3401 |
| https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip | 2026-04-22 | 200 OK | 11.8 MB | 4,765 VA polygons EPSG:3400 |
| https://www.elections.ab.ca/resources/maps/ | 2026-04-22 | 200 OK (index) | — | 2026 shapefiles **NOT YET PUBLISHED**; Phases 4A/4B/5 blocked |
| https://www.elections.ab.ca/uploads/2015-Provincial-General-Election-Statement-of-Vote.xlsx | 2026-04-22 | 200 OK | — | Source of `data/2015_results.xlsx` |

## Statistics Canada sources

| URL | Last verified | Status | Bytes | Notes |
|-----|---------------|--------|-------|-------|
| https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000a21a_e.zip | 2026-04-22 | 200 OK (after User-Agent header) | 93.2 MB | 2021 DA cartographic boundary file |
| https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcsd000a21a_e.zip | 2026-04-22 | 200 OK | 38.5 MB | 2021 CSD cartographic boundary file |
| https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=006&FILETYPE=CSV | 2026-04-22 | 200 OK | 2.1 GB zip → 5.37 GB CSV | 98-401-X2021006 — DA population table |
| https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=005&FILETYPE=CSV | 2026-04-22 | 200 OK | 197 MB zip → 2.6 GB CSV | 98-401-X2021005 — CSD population table |
| https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901 | 2026-04-22 | 200 OK | — | Table 17-10-0009 — quarterly population estimates |
| https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E | 2026-04-22 | 200 OK (form UI) | — | Interactive download builder; direct getFile URLs above are preferred |
| https://www12.statcan.gc.ca/rest/census-recensement/2021/ | 2026-04-22 | 200 OK | — | StatsCan WDS REST API root |
| https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/tt/STC98-10-0459-2021005-E.zip | 2026-04-22 | 200 OK | — | Journey-to-work table (Cochrane CSD used for commuter-tie test) |

## Alberta Treasury Board / Economic Dashboard sources

| URL | Last verified | Status | Bytes | Notes |
|-----|---------------|--------|-------|-------|
| https://economicdashboard.alberta.ca/dashboard/population/ | 2026-04-22 | 200 OK | — | July 2024 TBF population estimate (4,888,723) used by commission |
| https://open.alberta.ca/dataset/alberta-population-estimates | 2026-04-22 | 200 OK | — | Quarterly TBF estimates 2021Q2 through 2025Q2 |

## Projection / polling sources

| URL | Last verified | Status | Bytes | Notes |
|-----|---------------|--------|-------|-------|
| https://338canada.com/alberta/ | 2026-04-22 | 200 OK | — | 338 Canada Alberta index page; source of riding codes 1001–1087 |
| https://338canada.com/alberta/NNNNe.htm (N=1001–1087) | 2026-04-22 | 200 OK for all 87 | — | Per-riding pages used by Track J; snapshot date April 12, 2026 |

## City of Calgary open data

| URL | Last verified | Status | Bytes | Notes |
|-----|---------------|--------|-------|-------|
| https://data.calgary.ca/resource/tz8z-hyaz.geojson | 2026-04-22 | 200 OK | 638 KB | 14 Calgary ward polygons; dataset updated 2026-04-08 |

## News sources (cited for procedural facts, §5.2)

| URL pattern | Last verified | Notes |
|-------------|---------------|-------|
| https://www.cbc.ca/news/canada/edmonton/ (April 16, 2026 coverage of Motion 19) | 2026-04-22 | Source for April 16 vote count and committee composition |
| https://www.calgaryjournal.ca/ (April 21, 2026 follow-up) | 2026-04-22 | Source for advisory panel structure |
| https://www.rimbeyreview.com/ (April 16, 2026 premier remarks) | 2026-04-22 | Source for R5-framing statement |

## Sources that required workarounds

| URL | Issue | Workaround |
|-----|-------|------------|
| https://www12.statcan.gc.ca/.../lda_000a21a_e.zip | HEAD request hits 30-redirect limit | GET with `User-Agent: Mozilla/5.0` returns 200; see `analysis/data_acquisition_log.md` |
| https://data.calgary.ca/resource/r9vx-mhnf.geojson | Socrata map view returns 53-byte stub | Use dataset UID `tz8z-hyaz` instead |
| https://www.elections.ab.ca/uploads/2017-EBC-Final-Report.pdf | 404 on guessed pattern | Actual URL: `abebc_2017_rpt_final.pdf` |

## Sources that were NOT retrieved but are referenced

- **2026 shapefiles for the 89-seat proposed maps** — Elections Alberta
  had not published these as of 2026-04-22. Phases 4A/4B/5 of the audit
  are blocked pending release. Expected release window is commonly
  within 90 days of the final report (commission final report dated
  March 23, 2026). Until release, the audit's §2 population numbers
  derive from the commission's own per-ED tables, not from direct
  shapefile aggregation against 2021 census DAs.
- **2010 EBC Final Report** — downloaded for reference but contains no
  machine-readable 2010-era → 2019-era ED crosswalk. The 2015 → 2019
  boundary crosswalk is incomplete (see
  `data/v0_1_2015_to_2019_crosswalk_partial.csv`).

## Reproducibility expectations

Three classes of reproducibility risk, ordered by likelihood:

1. **URL reorganisation** (high likelihood within 1–3 years). Elections
   Alberta periodically reorganises the `/uploads/` directory. If a
   URL above returns 404, search Elections Alberta's main site for the
   filename (the `.pdf` or `.zip` basename) — the file itself typically
   persists even when the directory structure changes.
2. **Statistics Canada table retirement** (low likelihood within 5
   years, near-certain on a 10+ year horizon). The specific table
   numbers (17-10-0009, 98-401-X2021005, 98-401-X2021006, 98-10-0459)
   are tied to the 2021 census cycle. The 2026 census cycle will
   introduce a new set of `98-401-X2026...` URLs.
3. **Content drift at stable URLs** (highest-consequence class). 338
   Canada updates per-riding pages continuously. The per-riding pull in
   Track J is against the April 12, 2026 snapshot and is not
   reproducible from the live site today. The scraped CSV
   (`data/v0_1_338canada_per_riding_87seat.csv`) is the frozen artifact.

Addressed residual risk: this manifest captures the state as of
2026-04-22. A reproducer in 2028 or 2031 should treat the checked-in
CSVs and shapefile extracts under `data/` as the authoritative record;
if a URL drifts, the frozen artefact under `data/` is the source of
truth for that audit.

## How to extend

When new analysis introduces a new URL, append it here with its last
successful access date and a one-line description of what it provided.
A reproducibility review at each release tag should walk this file and
update `Last verified`.
