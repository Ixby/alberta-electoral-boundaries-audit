# 338Canada Alberta projection, October 19, 2026 (snapshot)

**Source.** [338Canada](https://338canada.com/alberta/), Philippe J. Fournier. Latest Alberta update shown on every page: **October 19, 2026**. 338Canada describes its riding numbers as "a mostly-proportional swing model adjusted with provincial and regional polls conducted by professional pollsters. This is not a poll, but a projection based on polls."

**Fetched** 2026-11-09 between 11:18 and 11:22 UTC (05:18–05:22 Alberta time, UTC−6), from this cloud session, one request every 1.2 seconds. The district list came from https://338canada.com/alberta/districts.htm; each riding from https://338canada.com/alberta/<id>e.htm (ids 1001–1087).

**Provincial projection on the Alberta page:** UCP 48% (43–53), NDP 43% (39–48), each "± 5%". The page's "Latest Alberta Polls" box listed Pollara (2026-10-09), Mainstreet (2026-10-16), Abacus (2026-10-10) and Léger (2026-10-03); the raw numbers are in `provincial_summary.txt` as the page printed them.

**On the current 87-district map**, the riding point projections give UCP 43 leads, NDP 43, and one exact tie (Red Deer-North, 45–45).

## Files

| File | What it is |
|---|---|
| `ridings_2026-10-19.csv` | One row per riding: point projection and low/high range for each party listed (UCP, NDP, GPA, PTPA, REP, WIP), whole percent, and the 2023 winner with share as 338 prints it. |
| `projection_blocks.txt` | The projection block of each riding page as text, exactly as extracted, so every number in the CSV can be checked against what the page said. |
| `provincial_summary.txt` | The provincial projection and polls box from the Alberta page. |
| `page_sha256.tsv` | Size, fetch time and SHA-256 of every riding page as fetched. |
| `riding_urls.tsv` | The 87 riding URLs and names. |
| `extract_338.py` | The parser that turned the pages into the CSV. |

Hashes of the two index pages as fetched: Alberta page (`/alberta/`, 177,672 bytes) `53fcbc4cdd8225c90d10c4d11d1333b63f9c28bec4e768e6a52d9285aa7416c0`; district list (`/alberta/districts.htm`, 158,877 bytes) `eae4a896baad9fd03dbf528deb56e13fde851627dc95ac0a844bc0d2dc8d7b85`.

The pages themselves are not redistributed here: they are 338Canada's work. The numbers, the extracted text blocks and the hashes are kept so the snapshot can be checked against an archived copy. 338Canada updates in place, so the live pages will not match after its next update.

Used by `findings/p338_projection/`.
