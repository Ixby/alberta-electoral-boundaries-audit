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

**Snapshot preservation (2026-04-22):** each live URL below is paired
with the most recent permanent snapshot located on the Internet Archive
Wayback Machine (`web.archive.org`) and/or `archive.ph`. A snapshot URL
is stable even when the live URL drifts, so reproducers can read the
exact bytes retrieved by the audit. Coverage summary and per-URL
archival reasoning are in `analysis/url_archival_log.md`. A URL
flagged "unarchived" has no existing snapshot on either service — that
cell is a manual-capture candidate for any future audit release.

---

## Primary election and commission sources

| Source | URL | Last verified | Status | Bytes | Wayback snapshot | archive.ph snapshot | Notes |
|---|---|---|---|---|---|---|---|
| 2023 Statement of Vote | https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx | 2026-04-22 | 200 OK | 1.7M Elec Day + 1.4M Advance rows | https://web.archive.org/web/20250817223743/https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx | unarchived | Source of `data/2023_results.xlsx` |
| 2026 commission final report | https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf | 2026-04-22 | 200 OK | 80.0 MB | https://web.archive.org/web/20260417002435/https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf | https://archive.ph/20260417001902/https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf | 362 pp. Source of Appendix A (majority), Appendix E (minority), chair Addendum |
| 2017 commission final report | https://www.elections.ab.ca/uploads/abebc_2017_rpt_final.pdf | 2026-04-22 | 200 OK | 36.5 MB | https://web.archive.org/web/20250801111601/https://www.elections.ab.ca/uploads/abebc_2017_rpt_final.pdf | unarchived | Source of 2019-baseline populations |
| 2019 ED shapefiles | https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip | 2026-04-22 | 200 OK | 2.72 MB | https://web.archive.org/web/20250810062836/https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip | unarchived | 87 ED polygons EPSG:3401 |
| 2023 VA shapefiles | https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip | 2026-04-22 | 200 OK | 11.8 MB | https://web.archive.org/web/20260422212613/https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip | unarchived | 4,765 VA polygons EPSG:3400 |
| Elections Alberta — GIS Resources | https://www.elections.ab.ca/resources/maps/ | 2026-04-22 | 200 OK (index) | — | https://web.archive.org/web/20260422212706/https://www.elections.ab.ca/resources/maps/ | https://archive.ph/20181227045415/https://www.elections.ab.ca/resources/maps/ | 2026 shapefiles **NOT YET PUBLISHED**; Phases 4A/4B/5 blocked |
| 2015 Statement of Vote | https://www.elections.ab.ca/uploads/2015-Provincial-General-Election-Statement-of-Vote.xlsx | 2026-04-23 | 200 OK | — | https://web.archive.org/web/20260423112653/https://www.elections.ab.ca/uploads/2015-Provincial-General-Election-Statement-of-Vote.xlsx | unarchived | Source of `data/2015_results.xlsx`; Wayback snapshot added 2026-04-23 via authenticated SPN2 POST |

## Statistics Canada sources

| Source | URL | Last verified | Status | Bytes | Wayback snapshot | archive.ph snapshot | Notes |
|---|---|---|---|---|---|---|---|
| 2021 DA cartographic boundaries | https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000a21a_e.zip | 2026-04-22 | 200 OK (after User-Agent header) | 93.2 MB | https://web.archive.org/web/20260422212905/https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000a21a_e.zip | unarchived | 2021 DA cartographic boundary file |
| 2021 CSD cartographic boundaries | https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcsd000a21a_e.zip | 2026-04-22 | 200 OK | 38.5 MB | https://web.archive.org/web/20260422213031/https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcsd000a21a_e.zip | unarchived | 2021 CSD cartographic boundary file |
| 98-401-X2021006 DA population | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=006&FILETYPE=CSV | 2026-04-22 | 200 OK | 2.1 GB zip → 5.37 GB CSV | https://web.archive.org/web/20260422213237/https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=006&FILETYPE=CSV | unarchived | 98-401-X2021006 — DA population table |
| 98-401-X2021005 CSD population | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=005&FILETYPE=CSV | 2026-04-22 | 200 OK | 197 MB zip → 2.6 GB CSV | https://web.archive.org/web/20260422213502/https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=005&FILETYPE=CSV | unarchived | 98-401-X2021005 — CSD population table |
| Table 17-10-0009 quarterly pop estimates | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901 | 2026-04-22 | 200 OK | — | https://web.archive.org/web/20260422213622/https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901 | https://archive.ph/20230324041258/https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901 | Quarterly population estimates |
| Download-telecharger UI | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E | 2026-04-22 | 200 OK (form UI) | — | https://web.archive.org/web/20260418025639/https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E | unarchived | Interactive download builder; direct getFile URLs above are preferred |
| StatsCan WDS REST root | https://www12.statcan.gc.ca/rest/census-recensement/2021/ | 2026-04-23 | redirects to `/srvmsg/srvmsg404.html` | — | https://web.archive.org/web/20260423112829/https://www12.statcan.gc.ca/rest/census-recensement/2021/ | unarchived | REST API root; the bare URL redirects to StatsCan's generic 404 page rather than an API index — authoritative calls go through the per-table `getFile.cfm` URLs already archived above. Wayback snapshot preserves the redirected state of the root URL |
| Journey-to-work table STC98-10-0459 | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/tt/STC98-10-0459-2021005-E.zip | 2026-04-22 | 200 OK | — | unarchived | unarchived | Cochrane CSD used for commuter-tie test; manual capture needed |

## Alberta Treasury Board / Economic Dashboard sources

| Source | URL | Last verified | Status | Bytes | Wayback snapshot | archive.ph snapshot | Notes |
|---|---|---|---|---|---|---|---|
| Economic Dashboard — Population | https://economicdashboard.alberta.ca/dashboard/population/ | 2026-04-23 | 200 OK | — | https://web.archive.org/web/20260423112817/https://economicdashboard.alberta.ca/dashboard/population/ | unarchived | July 2024 TBF population estimate (4,888,723) used by commission; Wayback snapshot added 2026-04-23 |
| open.alberta.ca — Population estimates | https://open.alberta.ca/dataset/alberta-population-estimates | 2026-04-23 | 200 / 404 on scraper | — | https://web.archive.org/web/20260423112822/https://open.alberta.ca/dataset/alberta-population-estimates | unarchived | Quarterly TBF estimates 2021Q2 through 2025Q2; Wayback SPN2 capture 2026-04-23 recorded the page as seen by its scraper but the scraper received http_status 404, likely because open.alberta.ca bot-blocks or the dataset has been relocated — live URL verified 200 OK via browser UA. Snapshot records the scraper's view at the capture time; a browser-UA re-capture would be preferable for future audits |

## Projection / polling sources

| Source | URL | Last verified | Status | Bytes | Wayback snapshot | archive.ph snapshot | Notes |
|---|---|---|---|---|---|---|---|
| 338Canada — Alberta index | https://338canada.com/alberta/ | 2026-04-22 | 200 OK | — | https://web.archive.org/web/20260302012718/https://338canada.com/alberta/ | https://archive.ph/20241107152411/https://338canada.com/alberta/ | Source of riding codes 1001–1087 |
| 338Canada — per-riding page (pattern) | https://338canada.com/alberta/NNNNe.htm (N=1001–1087) | 2026-04-22 | 200 OK for all 87 | — | https://web.archive.org/web/20260417215902/https://338canada.com/alberta/1001e.htm (probe); https://web.archive.org/web/20260417215936/https://338canada.com/alberta/1044e.htm (probe); https://web.archive.org/web/20260417215940/https://338canada.com/alberta/1087e.htm (probe) | unarchived for pattern | Per-riding pages used by Track J; snapshot date April 12, 2026; three probe pages preserved on Wayback as representative of the 87-URL pattern — the frozen scraped CSV under `data/` is the authoritative artefact |

## City of Calgary open data

| Source | URL | Last verified | Status | Bytes | Wayback snapshot | archive.ph snapshot | Notes |
|---|---|---|---|---|---|---|---|
| Calgary wards GeoJSON | https://data.calgary.ca/resource/tz8z-hyaz.geojson | 2026-04-22 | 200 OK | 638 KB | unarchived | unarchived | 14 Calgary ward polygons; dataset updated 2026-04-08; manual capture needed |

## News sources (cited for procedural facts, §5.2)

| Source | URL pattern | Last verified | Wayback snapshot | archive.ph snapshot | Notes |
|---|---|---|---|---|---|
| CBC Edmonton | https://www.cbc.ca/news/canada/edmonton/ (April 16, 2026 coverage of Motion 19) | 2026-04-22 | https://web.archive.org/web/20260420093704/https://www.cbc.ca/news/canada/edmonton | https://archive.ph/20250819220759/https://www.cbc.ca/news/canada/edmonton/ | Source for April 16 vote count and committee composition |
| Calgary Journal | https://www.calgaryjournal.ca/ (April 21, 2026 follow-up) | 2026-04-22 | unarchived | https://archive.ph/20150410091846/http://www.calgaryjournal.ca/ | Source for advisory panel structure |
| Rimbey Review | https://www.rimbeyreview.com/ (April 16, 2026 premier remarks) | 2026-04-22 | https://web.archive.org/web/20260202063716/https://rimbeyreview.com/ | https://archive.ph/20120913232740/http://www.rimbeyreview.com/ | Source for R5-framing statement |

## Sources that required workarounds

| URL | Issue | Workaround | Wayback snapshot | archive.ph snapshot |
|-----|-------|------------|------------------|---------------------|
| https://www12.statcan.gc.ca/.../lda_000a21a_e.zip | HEAD request hits 30-redirect limit | GET with `User-Agent: Mozilla/5.0` returns 200; see `analysis/data_acquisition_log.md` | https://web.archive.org/web/20260422212905/https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000a21a_e.zip | unarchived |
| https://data.calgary.ca/resource/r9vx-mhnf.geojson | Socrata map view returns 53-byte stub | Use dataset UID `tz8z-hyaz` instead | unarchived | unarchived |
| https://www.elections.ab.ca/uploads/2017-EBC-Final-Report.pdf | 404 on guessed pattern (URL never existed) | Actual URL: `abebc_2017_rpt_final.pdf` (dual-archived above) | n/a (dead URL, never existed) | n/a (dead URL) |

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
  `data/2015_to_2019_crosswalk_partial.csv`).

## Reproducibility expectations

Three classes of reproducibility risk, ordered by likelihood:

1. **URL reorganisation** (high likelihood within 1–3 years). Elections
   Alberta periodically reorganises the `/uploads/` directory. If a
   URL above returns 404, search Elections Alberta's main site for the
   filename (the `.pdf` or `.zip` basename) — the file itself typically
   persists even when the directory structure changes. If the filename
   itself drifts, the Wayback snapshot column is the authoritative
   fallback for every row that has one.
2. **Statistics Canada table retirement** (low likelihood within 5
   years, near-certain on a 10+ year horizon). The specific table
   numbers (17-10-0009, 98-401-X2021005, 98-401-X2021006, 98-10-0459)
   are tied to the 2021 census cycle. The 2026 census cycle will
   introduce a new set of `98-401-X2026...` URLs.
3. **Content drift at stable URLs** (highest-consequence class). 338
   Canada updates per-riding pages continuously. The per-riding pull in
   Track J is against the April 12, 2026 snapshot and is not
   reproducible from the live site today. The scraped CSV
   (`data/338canada_per_riding_87seat.csv`) is the frozen artifact.

Addressed residual risk: this manifest captures the state as of
2026-04-22. A reproducer in 2028 or 2031 should treat the checked-in
CSVs and shapefile extracts under `data/` as the authoritative record;
if a URL drifts, the frozen artefact under `data/` is the source of
truth for that audit. Where a Wayback or archive.ph snapshot exists, it
is a second independent preservation layer — the snapshot URL is
timestamped and cannot be mutated after capture.

## Chrome-based archival retry (2026-04-22)

A browser-driven retry of the six priority unarchived URLs was
attempted via the Wayback public "Save Page Now" UI. All three of the
URLs actually submitted (StatsCan journey-to-work zip, 2015 Statement
of Vote xlsx, Calgary wards geojson) hit an IP-level daily bandwidth
block: Wayback returned a `Sorry — Job failed` page with the message
`You have reached your daily not-logged-in bandwidth limit.` The
remaining three priority URLs (Economic Dashboard, open.alberta.ca
dataset landing, StatsCan REST root) were not submitted because the
block is account-wide and every subsequent call would fail the same
way until the quota resets. No new snapshots were produced; the
"unarchived" cells in the tables above stand. The full attempt trace
and diagnosis is in `analysis/url_archival_log.md` under the
"Chrome-based pass" appendix. Any future archival pass for these six
URLs requires a signed-in Internet Archive session (Bearer token or
authenticated browser).

## How to extend

When new analysis introduces a new URL, append it here with its last
successful access date, a one-line description of what it provided,
and (if possible) submit the URL to both web.archive.org/save/ and
archive.ph/submit/ so the snapshot columns can be populated. A
reproducibility review at each release tag should walk this file and
update `Last verified` plus refresh any snapshots that have aged
beyond the release cycle.
