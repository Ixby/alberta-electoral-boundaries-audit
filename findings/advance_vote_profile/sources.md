# Sources

Every outside source behind `README.md`, when it was fetched, and what it says.

Times are Alberta time (UTC−6), converted from the UTC session clock that was read when each request was made. "Read in full" means the file was downloaded and its text was read. "Search summary only" means only a search engine's summary was seen. Nothing here is quoted from memory.

No federal source is used.

## Network notes

- The page-fetch tool could not resolve `www.elections.ab.ca` or `cpsa-acsp.ca`. The same hosts were reachable with `curl` through the session proxy, so files were downloaded that way and converted with `pdftotext`.
- OpenStreetMap Nominatim rate-limited the geocoding run (HTTP 429) several times. Failed lookups were retried, not recorded as "not found".

## Used in the current README

| # | URL | Fetched (Alberta time) | Status | What it is and what was used |
|---|---|---|---|---|
| 1 | `https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Report.pdf` | 2026-11-09 22:40; fetched again 2026-11-10 00:56 (53,177,861 bytes, SHA-256 `51e9771b61bcd05a066b23f733efd563fd36f8ee14f42c309682bf8ebaf31993`) | Read in full (text extracted; figures read as printed numbers) | Elections Alberta, *2023 Provincial General Election Report*. **Used for what "Names on List" counts:** p. 61, "248,688 electors registered to vote at their advance or Election Day voting location, representing 14% of voters" (Table 9: 102,373 during advance voting, 146,315 on election day); p. 61, electors not registered "were required to complete their registration at their voting location prior to being issued their ballot"; p. 62, "Elections Alberta reviews all voting records, declarations, and oaths to update the Register of Electors" and "The Post Election Day List of Electors ... represents a snapshot of voters as of March 26, 2024"; p. 131, turnout "is recalculated using the Post Election Day List of Electors ... electors who are deceased or moved are removed from the list, and new electors are reflected in the correct electoral division and voting area"; p. 131, Table 29, 2023: ballots cast 1,777,315, names on list 2,939,762, turnout 60.5%. Appendix C (registrations at voting places by division) and Appendix D (Post Election Day List of Electors by division) were copied from the extracted text into `inputs/ea_2023_report_appendix_c_d.csv`; Airdrie-East (division 48) was lost in the text extraction from both. **Also from this report (first fetch):** 331 advance voting places, 1,216 election-day voting places, 4,764 voting areas; advance voters are older than the list (29.6% aged 65 or over, against 24.4% of the list). The report gives **no party breakdown by voting method and no early-ballot results below the division**. |
| 2 | `https://nominatim.openstreetmap.org/search` (one query per named 2023 advance poll, limited to the division's bounding box) | 2026-11-09 22:39 onward | Results kept | OpenStreetMap place lookup. Only public polling-place names from the Elections Alberta workbook were sent. Results are in `inputs/advance_poll_geocodes.csv` (tracked; cannot be regenerated bit for bit) with the matched place name beside each. |
| 3 | `https://www.elections.ab.ca/resources/reports/general-elections/` | 2026-11-09 22:40 | Downloaded, used only to confirm where item 1 is published | Elections Alberta list of general-election reports. |

## Read earlier, not relied on in the current README

| # | URL | Fetched (Alberta time) | Status | What it says |
|---|---|---|---|---|
| 4 | `https://openparliament.ca/committees/house-affairs/39-2/6/peter-john-loewen-3/only` | 2026-11-09 22:40 | Read in full | Peter John Loewen, testimony to a House of Commons committee, 22 November 2007, on the 2006 Canadian Election Study: older, more interested and party-identified citizens are more likely to vote in advance. |
| 5 | `https://publications.gc.ca/collections/collection_2014/elections/SE7-3-2007-1-eng.pdf` | 2026-11-09 22:40 | **Not read** (host returned HTML, not the PDF). Search summary only. | Said by the search summary to be the study behind item 4. Unverified. |
| 6 | `https://cpsa-acsp.ca/documents/conference/2016/Garnett.pdf` | 2026-11-09 22:40 | Read in full | Holly Ann Garnett, "Early Voting: Comparing Canada, Finland, Germany and Switzerland", draft conference paper, June 2016 ("DRAFT – Do not cite without permission"). Older voters vote early more in all four countries; evidence on other traits is mixed. |

## The data the tests use (in the repository, not fetched)

- `data/raw/2023_results.xlsx`: the 2023 Statement of Vote workbook, one sheet per division, every poll row with votes by candidate, "Names on List" (election-day stations only), valid, declined, rejected and total ballots.
- `data/raw/2015_results.xlsx`: the 2015 workbook.
- `data/shapefiles/derived/va_polygons_with_2023_votes.gpkg`: voting areas with election-day votes (equal split within a station).
- `data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg`: the registered Amendment 12 all-ballots file (M0).

## What the search did not find

- No published analysis of Alberta 2023 early votes below the division, by anyone.
- No published party breakdown of Alberta early votes by Elections Alberta. The party figures in the README come from our own count of the workbook.
- No Elections Alberta statement, station by station, of how many electors on each station's list registered at the poll.
- The Elections Alberta 2019 general election report was not fetched.
