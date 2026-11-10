# Sources

Every outside source used in `README.md`, with when it was fetched and what it says.
Times are UTC, read from the session clock when the request was made (2026-11-10 UTC is the evening of 2026-11-09 in Alberta).
"Read in full" means the file was downloaded and its text was read. "Search summary only" means only a search engine's summary was seen. Nothing here is quoted from memory.

## Network notes

- The page-fetch tool could not resolve `www.elections.ab.ca`, `publications.gc.ca` or `cpsa-acsp.ca`. The same hosts were reachable with `curl` through the session proxy, so the files below were downloaded that way and converted with `pdftotext`.
- `publications.gc.ca` returned a web page in place of the PDF asked for (18 KB of HTML). That document was **not read**; see item 9.
- OpenStreetMap Nominatim rate-limited the geocoding run (HTTP 429) several times. Failed lookups were retried, not recorded as "not found".

## Data downloaded and used in the tests

| # | URL | Fetched (UTC) | What it is and what was used |
|---|---|---|---|
| 1 | `https://www.elections.ca/res/rep/off/ovr2021app/53/data_donnees/pollresults_resultatsbureau48001.csv` to `...48034.csv` (34 files) | 2026-11-10 04:38 | Elections Canada, official poll-by-poll results, 44th general election (2021), the 34 Alberta ridings. Votes by candidate for every ordinary poll, advance poll (numbers 600 and up), mobile poll and special-voting group, with electors per poll. Used in `02_federal_gradient.py`. |
| 2 | `https://www.elections.ca/res/rep/off/ovr2019app/51/data_donnees/pollresults_resultatsbureau48001.csv` to `...48034.csv` (34 files) | 2026-11-10 04:38 | Same, 43rd general election (2019). |
| 3 | `https://ftp.maps.canada.ca/pub/elections_elections/Electoral-districts_Circonscription-electorale/Elections_Canada_2021/PD_CA_2021_EN.zip` | 2026-11-10 04:38–04:41 | Elections Canada polling-division boundaries, 2021. Only the attribute table was used: fields `FED_NUM`, `PD_NUM`, `ADV_POLL_N` say which advance poll serves each polling division. 99.5% of Alberta polling divisions matched. |
| 4 | `https://ftp.maps.canada.ca/pub/elections_elections/Electoral-districts_Circonscription-electorale/Elections_Canada_2019/polling_divisions_boundaries_2019.shp.zip` | 2026-11-10 04:44 | Same for 2019 (fields `FEDNUM`, `PDNUM`, `ADVPOLLNUM`). 100% matched. |
| 5 | `https://nominatim.openstreetmap.org/search` (one query per named 2023 advance poll, limited to the division's bounding box) | 2026-11-10 04:39 onward | OpenStreetMap place lookup. Only public polling-place names from the Elections Alberta workbook were sent. Results are in `inputs/advance_poll_geocodes.csv` (tracked; cannot be regenerated bit for bit, see README) with the matched place name beside each. |

Directory listings read to find items 3 and 4: `https://ftp.maps.canada.ca/pub/elections_elections/Electoral-districts_Circonscription-electorale/`, `.../Elections_Canada_2021/`, `.../Elections_Canada_2019/` (2026-11-10 04:38–04:41).

## Reports and papers

| # | URL | Fetched (UTC) | Status | What it says |
|---|---|---|---|---|
| 6 | `https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Report.pdf` | 2026-11-10 04:40 | Read in full (text extracted; figures read as printed numbers) | Elections Alberta, *2023 Provincial General Election Report*. Of 1,764,915 valid ballots: advance 757,453 (42.92%), election day 931,829 (52.80%), special ballot 51,351 (2.91%), mobile 24,282 (1.38%) (summary page). "A total of 758,637 electors voted at an advance voting location, representing 42.7% of the vote ... an 8.3% increase over ... 2019." "166,732 were cast by electors using the vote anywhere service, representing 22% of the volume at advance voting locations. This is a decrease from ... 2019 ... when 31.9%" (p. 99). "Of the voters who voted at advance voting locations, 29.6% were 65 years or older in 2023, compared to 20.5% in the 2019 Provincial General Election"; Figure 37 gives advance voters by age: 18–24 5.8%, 25–34 11.7%, 35–44 16.5%, 45–54 16.6%, 55–64 19.8%, 65+ 29.6% (p. 101–102). Table 10: 65+ are 24.4% of the post-election list of electors, 18–24 are 8.9%. 331 advance voting places, 1,216 election-day voting places, 691 mobile locations, 4,764 voting areas. "on average two to three advance voting locations in electoral divisions in Edmonton and Calgary, compared to an average of five ... in all other electoral divisions"; advance places "generally situated so that no elector should have to travel more than 100 km". History table (Figure 39/40): advance ballots were 15.8% of valid votes in 2015, 36.7% in 2019, 42.7% in 2023. The report gives **no party breakdown by voting method and no advance results below the division**. |
| 7 | `https://www.elections.ca/res/rec/eval/pes2025/evt/evt_e.pdf` | 2026-11-10 04:40 | Read in full | Elections Canada, *Turnout by Age Group and Gender in the 45th General Election* (February 2026). Table 4: advance polls were 34.3% of ballots in 2021 and 37.9% in 2025. Table 5, share of voters in each age group who used advance polls or special ballots: in 2021, 28.3% of voters aged 18–24, 30.6% of 25–34, 32.3% of 35–44, 35.2% of 45–54, 43.8% of 55–64, 53.5% of 65–74, 52.9% of 75+; in 2025, 37.4% up to 53.0%. Older voters use early voting much more. National figures, not Alberta. |
| 8 | `https://openparliament.ca/committees/house-affairs/39-2/6/peter-john-loewen-3/only` | 2026-11-10 04:40 | Read in full | Peter John Loewen, testimony to the House of Commons Procedure and House Affairs Committee, 22 November 2007, reporting a study of the 2006 Canadian Election Study: "older citizens were more likely to vote in advance than younger citizens. Those interested in politics were more likely to vote in advance ... Those who identified with a political party and/or were contacted by political parties were more likely to vote in advance." Also: "for every ten additional voters who decided to vote in advance in 2006, nearly six of those individuals would not have voted otherwise." |
| 9 | `https://publications.gc.ca/collections/collection_2014/elections/SE7-3-2007-1-eng.pdf` | 2026-11-10 04:40 | **Not read** (host returned HTML, not the PDF). Search summary only. | Described by the search summary as a 2007 Elections Canada study using the 2006 Canadian Election Study that finds advance voters are older and more engaged. It appears to be the study behind item 8. Authorship unverified. Not relied on beyond item 8. |
| 10 | `https://cpsa-acsp.ca/documents/conference/2016/Garnett.pdf` | 2026-11-10 04:40 | Read in full | Holly Ann Garnett, "Early Voting: Comparing Canada, Finland, Germany and Switzerland", paper for the Canadian Political Science Association meeting, June 2016. Marked "DRAFT – Do not cite without permission", so it is used only as a pointer to the literature. Finds that in all four countries the oldest age group is more likely to vote early; in Canada the gap between middle and oldest age groups is small ("about a 2 percentage point difference"). Interest in politics is positively related to early voting. Its literature review: "Most researchers find that early voters tend to be older (Barreto et al., 2006; Blais et al., 2007; Gronke and Toffey, 2008); but evidence about the impact of other socio-demographic characteristics is more mixed." |
| 11 | `https://www.elections.ab.ca/resources/reports/general-elections/` | 2026-11-10 04:40 | Downloaded, used only to confirm where item 6 is published | Elections Alberta list of general-election reports. |
| 12 | `https://laws-lois.justice.gc.ca/eng/acts/E-2.01/page-14.html` | 2026-11-10 05:14 | Read (advance-polling sections only) | Canada Elections Act, s. 168: the returning officer shall "establish in his or her electoral district advance polling districts that consist of one or more polling divisions"; "(3) An advance polling station shall be established in each advance polling district." This sources the structure of the federal test. The text read does not say in so many words that an elector may vote in advance only at that station. The only read-in-full support for that premise is item 7, whose Table 4 labels the ballots "Electors voting at their assigned advance polling station". |
| 13 | `https://newswire.ca/news-releases/advance-voting-begins-friday-877912348.html` | 2026-11-10 05:14 | **Not read** (HTTP 403). Search summary only. | Described by the search summary as an Elections Canada release saying that at advance polls "electors can only vote at their assigned polling station". Unverified; not relied on. |

## Unsourced statements in the README (marked there)

- "Older voters lean conservative": general knowledge, no source fetched.
- That a federal elector voting in advance must use the assigned advance poll: supported by items 7 and 12; stated outright only in item 13, which could not be read.

## Independent verification

An independent verifier re-downloaded items 1 to 4, rebuilt the federal join, and spot-checked items 6, 7, 8 and 10 against the text (`audit2/verify-advance.json` in the session scratchpad, 2026-11-10 UTC). It found no source cited from memory among those checked. Its corrections are applied in the README. Its extra checks are rebuilt in `06_robustness.py` and `07_residual_error.py`.

## Search results seen but not opened (leads only, nothing in the README rests on them)

Searches run 2026-11-10 04:39–04:48 UTC.

- `https://www.cambridge.org/core/journals/canadian-journal-of-political-science-revue-canadienne-de-science-politique/article/i-came-i-saw-i-voted-distance-to-polling-locations-and-voter-turnout-in-ontario-canada/84EB73738B9DE67B869A013432566C02` — Garnett and Grogan (2021), distance to polling places and turnout in Ontario. Search summary: a negative, non-linear relation between distance and turnout; it studies assigned election-day polls, not advance polls. Not read.
- `https://www.elections.ab.ca/resources/media/news-releases/chief-electoral-officer-releases-2023-provincial-general-election-report/` — news release for item 6. Not read.
- `https://livewirecalgary.com/2023/05/23/advance-vote-day-1-albertas-2019-vote-record-smashed-on-first-day-of-voting/` — news story on advance turnout. Not read.
- `https://election.lab.ufl.edu/precinct-data/` — VEST precinct data page. The search did not confirm how US precinct data sets spread early votes reported only at county level, so the earlier audit note that party-specific spreading is "the usual practice" stays **unverified**.

## What the search did not find

- No published analysis of Alberta 2023 advance votes below the division level, by anyone.
- No published party breakdown of Alberta advance votes by Elections Alberta. The party figures in the README come from our own count of the Statement of Vote workbook (`data/raw/2023_results.xlsx`).
- No Canadian study of how distance to an *advance* poll affects who votes early.
- The Elections Alberta 2019 general election report was not fetched. The 2019 figures quoted come from the 2023 report's own comparisons (item 6).
