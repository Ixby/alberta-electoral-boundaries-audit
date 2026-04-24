# Wayback / archive.ph submission queue — follow-up to frozen manifest

**Context:** `FROZEN_MANIFEST.md` (2026-04-22) notes that a Chrome-based archival retry of six priority unarchived URLs hit the Wayback Machine's "not logged in" daily bandwidth limit. The user has now logged into the Internet Archive, so the previously-blocked submissions can be completed from an authenticated session.

This document is the **submission queue** — each row is a URL to submit via `web.archive.org/save/` (Wayback) and/or `archive.ph/submit/` (archive.ph), with the success-verification step to run afterward.

## Submission order (priority first)

| # | URL | Service | Expected result | Verify by |
|---|-----|---------|-----------------|-----------|
| 1 | https://www.elections.ab.ca/uploads/2015-Provincial-General-Election-Statement-of-Vote.xlsx | Wayback + archive.ph | New snapshot timestamped today | `curl -I <snapshot-url>` returns 200; Statement-of-Vote xlsx is 2015 Alberta general election results |
| 2 | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/tt/STC98-10-0459-2021005-E.zip | Wayback + archive.ph | New snapshot | Zip downloads; contains the journey-to-work crosswalk table used for the Cochrane commuter-tie test |
| 3 | https://data.calgary.ca/resource/tz8z-hyaz.geojson | Wayback + archive.ph | New snapshot | GeoJSON has 14 Calgary ward polygons |
| 4 | https://economicdashboard.alberta.ca/dashboard/population/ | Wayback + archive.ph | New snapshot | Page shows July 2024 TBF population 4,888,723 |
| 5 | https://open.alberta.ca/dataset/alberta-population-estimates | Wayback + archive.ph | New snapshot | Dataset page with quarterly 2021Q2-2025Q2 TBF estimates |
| 6 | https://www12.statcan.gc.ca/rest/census-recensement/2021/ | Wayback + archive.ph | New snapshot | REST root; may return JSON endpoint listing |
| 7 | https://www.elections.ab.ca/uploads/abebc_2017_rpt_final.pdf | archive.ph only (Wayback already has 2025-08-01 snapshot) | archive.ph row populated | Snapshot URL resolves to the 2017 commission final report |
| 8 | https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip | archive.ph only (Wayback has 2025-08-10) | archive.ph row populated | Zip is 2.72 MB; unzips to 87 ED shapefiles |
| 9 | https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip | archive.ph only (Wayback has 2026-04-22) | archive.ph row populated | Zip is 11.8 MB; 4,765 VA polygons |
| 10 | https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000a21a_e.zip | archive.ph only (Wayback has 2026-04-22) | archive.ph row populated | 2021 DA cartographic boundaries, 93.2 MB |
| 11 | https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lcsd000a21a_e.zip | archive.ph only (Wayback has 2026-04-22) | archive.ph row populated | 2021 CSD cartographic boundaries, 38.5 MB |
| 12 | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=005&FILETYPE=CSV | archive.ph only (Wayback has 2026-04-22) | archive.ph row populated | 98-401-X2021005 CSD population table |
| 13 | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/getFile.cfm?LANG=E&GEONO=006&FILETYPE=CSV | archive.ph only (Wayback has 2026-04-22) | archive.ph row populated | 98-401-X2021006 DA population table |

## Bulk-submission procedure (from authenticated browser session)

For Wayback (logged in at https://archive.org/account/login.php):

1. Open `https://web.archive.org/save` in the same browser session that's authenticated.
2. Paste each URL from column 2 where `Service` includes "Wayback."
3. Tick **"Save outlinks"** OFF (we want the single resource, not linked assets).
4. Tick **"Email result"** ON if you want the receipt for the record.
5. Submit and copy the resulting `https://web.archive.org/web/TIMESTAMP/ORIG_URL` from the completion page.
6. Paste the snapshot URL into the `Wayback snapshot` column of `FROZEN_MANIFEST.md`.

For archive.ph:

1. Open `https://archive.ph/` (no login required but rate-limited per IP — use the same user browser rather than an automated tool).
2. Paste each URL from column 2 where `Service` includes "archive.ph."
3. Click **"Save"** and wait for the capture page.
4. The resulting snapshot URL is `https://archive.ph/TIMESTAMP/ORIG_URL` — copy it into the `archive.ph snapshot` column of `FROZEN_MANIFEST.md`.

## After submission

1. Update `FROZEN_MANIFEST.md` with the new snapshot URLs (columns `Wayback snapshot` and `archive.ph snapshot`).
2. Update `analysis/v0_1_url_archival_log.md`'s "Chrome-based pass" appendix to record the bandwidth-block resolution date (today) and the count of URLs successfully archived in this pass.
3. If any URL fails to archive (service error, robots.txt block, etc.), note the reason in the log and mark the cell `submission-failed` rather than `unarchived` — the distinction matters for future reproducibility reviewers.

## Expected net effect

All 13 priority unarchived cells in the manifest should resolve to a real snapshot URL. This closes the evidentiary-chain gap flagged in the Legal Red-Team Framework under D1 ("URL with no archive = HIGH finding until `FROZEN_MANIFEST.md` is updated").

After this pass, the manifest has full dual-archive coverage on every primary source except those where the service declined the capture (robots.txt, JavaScript-rendered content, auth-walled pages). Those are documented in the log with the reason.
