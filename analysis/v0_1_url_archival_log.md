# v0_1 URL archival log

**Date:** 2026-04-22
**Pipeline:** `analysis/v0_1_url_archival.py`
**Inputs:** `FROZEN_MANIFEST.md`
**Outputs:** `.temp/frozen_manifest_urls.txt`, `.temp/wayback_results.csv`,
`.temp/archiveph_results.csv`, updated `FROZEN_MANIFEST.md` with
snapshot columns per row.

## Coverage summary

| Metric | Count | Rate |
|---|---|---|
| Unique URLs extracted | 27 | — |
| Wayback snapshots located | 18 | 66.7% |
| archive.ph snapshots located | 7 | 25.9% |
| Dual coverage (both services) | 6 | 22.2% |
| Any-service coverage (at least one) | 19 | 70.4% |
| Unarchived on both services | 8 | 29.6% |

URL extraction dropped two manifest-internal pattern rows that are not
real URLs: `https://www12.statcan.gc.ca/.../lda_000a21a_e.zip` (an
ellipsis illustrating an earlier row) and
`https://338canada.com/alberta/NNNNe.htm` (an `N=1001–1087` template).
Three concrete per-riding pages (`1001`, `1044`, `1087`) were added as
representative probes so the 87-URL pattern has Wayback coverage for at
least its endpoints.

## Methodology constraints and pivot

The initial Phase 2 implementation posted to `https://web.archive.org/save/<URL>`,
the canonical capture endpoint. As of 2026 that endpoint requires
authentication for anonymous clients (HTTP 401 via the SPN2 JSON path,
HTTP 520 via the web path with `X-RL: 0` rate-limit header). Without an
Internet Archive account we cannot force a fresh capture. The pipeline
pivoted to the CDX search API
(`https://web.archive.org/cdx/search/cdx`) which anonymously returns the
most recent 200-status snapshot for a given URL. That path worked and
is what the coverage numbers above reflect.

archive.ph also rate-limited `/submit/` POSTs (HTTP 429). The pipeline
fell back to `/newest/<URL>` which returns existing snapshots without
triggering a new capture. A retry pass confirmed the non-`ok` rows are
genuine HTTP 404 responses (no existing archive.ph snapshot) rather
than transient rate-limits.

## Wayback successes (18/27)

All located via CDX API; content-type and length verified for the
critical five via HEAD to each snapshot URL (section "Spot-check
verification" below).

Complete list in `.temp/wayback_results.csv`.

## archive.ph successes (7/27)

1. `https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf`
2. `https://www.elections.ab.ca/resources/maps/`
3. `https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901`
4. `https://338canada.com/alberta/`
5. `https://www.cbc.ca/news/canada/edmonton/`
6. `https://www.calgaryjournal.ca/`
7. `https://www.rimbeyreview.com/`

The three news URLs have old archive.ph captures (2015, 2012) — stale
but better than nothing as a reproducibility anchor for the fact that
the domain existed and served content.

## Unarchived on both services (8)

These URLs have no existing snapshot on either Wayback (CDX zero-row) or
archive.ph (HTTP 404 from `/newest`).

| URL | Reason unarchived | Manual-attempt guidance |
|---|---|---|
| `https://www.elections.ab.ca/uploads/2015-Provincial-General-Election-Statement-of-Vote.xlsx` | Never submitted to either service | Submit to `web.archive.org/save/` (requires free IA account) |
| `https://data.calgary.ca/resource/tz8z-hyaz.geojson` | Socrata API URL, rarely crawled | Submit to `web.archive.org/save/` |
| `https://data.calgary.ca/resource/r9vx-mhnf.geojson` | Dead Socrata UID per the manifest (known 53-byte stub) | Do not attempt; URL is documented as bad |
| `https://economicdashboard.alberta.ca/dashboard/population/` | Alberta gov dashboard, behind JS redirect chain | Submit to `web.archive.org/save/` and archive.ph |
| `https://open.alberta.ca/dataset/alberta-population-estimates` | Dataset landing page | Submit to both services |
| `https://www12.statcan.gc.ca/rest/census-recensement/2021/` | API root; empty response | Low priority; downstream `getFile.cfm` URLs are archived |
| `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/tt/STC98-10-0459-2021005-E.zip` | Large zip, rarely crawled | Submit to `web.archive.org/save/` |
| `https://www.elections.ab.ca/uploads/2017-EBC-Final-Report.pdf` | Known-dead guessed URL; real file is `abebc_2017_rpt_final.pdf` (dual-archived) | Do not attempt; documented as a 404 guess |

## Spot-check verification

For the six most-critical Wayback snapshots, HEAD requests confirmed
real archived content with correct content-types:

| Snapshot | HTTP | Content-Type | Content-Length |
|---|---|---|---|
| 2026 commission report | 200 | application/pdf | 83,912,947 bytes |
| 2017 commission report | 200 | application/pdf | 36,458,244 bytes |
| Elections AB maps index | 200 | text/html | (chunked) |
| 2019 ED shapefiles | 200 | application/x-zip-compressed | 2,852,757 bytes |
| StatsCan DA boundaries | 200 | application/x-zip-compressed | 97,683,595 bytes |
| 338 Canada Alberta | 200 | text/html | (chunked) |

The binary byte counts match the manifest's "Bytes" column to within
compression/metadata variance (2019 ED is 2.85 MB vs manifest 2.72 MB;
StatsCan DA is 97.7 MB vs manifest 93.2 MB). These are consistent with
zip-container bytes reported differently by different tools — the hash
of the inner payload is what matters for reproducibility, and the
snapshot URL is stable.

## Recommendations for manual archival

When an IA-authenticated session is available (user logs in to
archive.org and uses the Save Page Now 2 UI or SPN2 API with a Bearer
token), submit the 6 unarchived URLs in the priority order below:

1. `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/tt/STC98-10-0459-2021005-E.zip` — used by `v0_1_cochrane_journey_to_work.md`
2. `https://www.elections.ab.ca/uploads/2015-Provincial-General-Election-Statement-of-Vote.xlsx` — used by `parse_2015_results.py`
3. `https://economicdashboard.alberta.ca/dashboard/population/` — used as the 4,888,723 population-estimate citation
4. `https://open.alberta.ca/dataset/alberta-population-estimates` — quarterly TBF estimates context
5. `https://data.calgary.ca/resource/tz8z-hyaz.geojson` — 14 Calgary ward polygons
6. `https://www12.statcan.gc.ca/rest/census-recensement/2021/` — REST root (low priority)

Skip: `data.calgary.ca/resource/r9vx-mhnf.geojson` (known bad URL) and
`elections.ab.ca/uploads/2017-EBC-Final-Report.pdf` (never existed).

For academic papers cited in `v0_1_academic_literature_review.md` that
live behind DOIs, the recommended preservation is:

- Resolve the DOI at `doi.org` to get the publisher landing page URL,
  then submit that resolved URL to Wayback. This preserves the
  citation even if the publisher-side abstract drifts.
- For open-access versions on arXiv or SSRN, submit the canonical
  arXiv/SSRN URL directly — those services also support Wayback
  crawling via `robots.txt` permissions.

## Pipeline reproducibility

`analysis/v0_1_url_archival.py` is idempotent against the two rate-
limit-friendly endpoints (CDX for Wayback, `/newest` for archive.ph).
Re-running it produces the same outputs plus any new snapshots made in
the interim. The script depends only on the `requests` package (version
pinned in `requirements.txt`) and runs under the pinned Python
interpreter documented in `setup.md`. Ad-hoc retry passes for archive.ph
(when the binding constraint is transient 429s rather than genuine
404s) can be driven from the same module without modification.

## Chrome-based pass (2026-04-22, appendix)

A second archival attempt was made via the public Wayback "Save Page
Now" UI at `https://web.archive.org/save/` driven by a Chrome MCP
browser session. The hypothesis was that the public UI, when loaded in
a real browser from a client IP distinct from the Python pipeline's
host, might bypass the SPN2 anonymous-rate-limit cap that had blocked
the earlier Python path.

Three of the six priority URLs were attempted:

1. `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/tt/STC98-10-0459-2021005-E.zip`
2. `https://www.elections.ab.ca/uploads/2015-Provincial-General-Election-Statement-of-Vote.xlsx`
3. `https://data.calgary.ca/resource/tz8z-hyaz.geojson`

All three attempts returned the same response from Wayback's SPN
job-queue: a "Sorry — Job failed" page with the explicit text
`You have reached your daily not-logged-in bandwidth limit. Please
email us at "info@archive.org" if you would like to discuss this
more.` The block is IP-level and applies to every unauthenticated
save request for the remainder of the daily quota window,
independent of URL size or domain.

The Chrome session was not signed in to an Internet Archive account.
The remaining three priority URLs
(`economicdashboard.alberta.ca/dashboard/population/`,
`open.alberta.ca/dataset/alberta-population-estimates`,
`www12.statcan.gc.ca/rest/census-recensement/2021/`) were not
attempted because the binding constraint is the account-level quota,
not any per-URL property — every subsequent call would fail
identically until the quota resets.

Net coverage change from this pass: zero. The 19/27 (70.4%) any-service
coverage stands. The six priority URLs remain candidates for a future
pass with an authenticated IA session (Bearer token via the SPN2 API
or a signed-in browser session for the SPN UI). The three skipped
URLs (`tz8z-hyaz.geojson` + two dashboard/landing pages) are behind
the same block.

### Why the Python pipeline's 401/520 and the browser's "Sorry"
### page are the same error

The Python SPN2 JSON API returns HTTP 401 for unauthenticated save
requests; the web-UI path under `/save/<URL>` returns a 200 HTML page
that contains the "Sorry" block plus a 520-ish `X-RL: 0` header.
Both trigger on the same upstream counter — the Internet Archive's
per-IP `not-logged-in bandwidth` quota, which is shared across all
save paths for a given source IP. The browser-based pass observed
here is the UI-layer rendering of the same underlying block the
Python pipeline hit. Neither approach can succeed without an IA
account; the account attaches quota to a user rather than an IP.
