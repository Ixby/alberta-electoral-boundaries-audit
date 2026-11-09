# The panel's report, checked: claim inventory

Source: Independent Advisory Panel report (2026), high-resolution PDF, SHA-256 `d8ae78abcec3660f8158a327a25df7508b649ce5595788e8b265b362b2a75122`; text layer at `evidence/legislature/iap_report_2026_hires_text/`. Page numbers are the report's printed pages; PDF page = printed + 6. The full reading, with quotes, is `analysis/review/iap_report_reading_2026-11.md`.

Each row is a factual claim that can be checked against a primary source. Opinions and legal arguments (for example "proposals are a form of free speech" or how "necessary" should be read) are not in this list. They are weighed point by point in the review itself, with the evidence each side gives.

**Checkers.** R = checked in this repository (commission reports, official commission shapefiles, 2023 results, the panel's App. 7). W = checked on the web or against the commission's original submission files, by the CLI session.

**Verdicts** (filled in by the checks): holds · partly holds · does not hold · cannot be checked from public sources.

## Majority claims

| ID | Claim | Page | Checker | Source to check against |
|---|---|---|---|---|
| M1 | The Commission's Interim Report "recognized the desirability of preserving as much as possible the current (2017) electoral division of Drayton Valley-Devon" | p.21 | R | Commission Interim Report (Oct 2025), as quoted or summarized in the final report |
| M2 | "Residents of Leduc and Beaumont, as well as their mayors, asked for this electoral division"; "negative reaction by people in Beaumont to being paired with Sherwood Park" | p.23 | W | Commission submission archive; commission final report |
| M3 | Little Bow "has been in existence as a provincial constituency since 1913" | p.81 | W | Elections Alberta historical constituency records |
| M4 | Macleod-Crowsnest "avoids the incongruous encirclement of the City of Lethbridge that the Commission's recommendation entailed" | p.87 | R | Commission majority official shapefile |
| M5 | Red Deer and Lethbridge do not share population with a division outside their boundaries on the Commission's map (pp.75–76); "all but Lethbridge have been a part of a hybrid" (p.107) | pp.75–76, 107 | R | Commission majority official shapefile; 2019 map |
| M6 | "There are currently (since 2017) 19 hybrid electoral divisions", plus the Commission's eight, 27 in all | pp.107–108 | R | 2019 enacted map; commission final report |
| M7 | The Commission's variances ran "0.2% to … 14%", average 4.63% (5.72% with special divisions); its special-consideration divisions were Central Peace-Notley, Lesser Slave Lake and Canmore-Banff | pp.103–104 | R | Commission majority populations (final report) |
| M8 | Lesser Slave Lake's current boundaries "make it eligible for Section 15(2) status without additional territory being added" | p.15 | R | 2019 map; `data/outputs/s15_2_real_maps.json` |
| M9 | "Lethbridge already has population to spare" | p.74 | R | App. 7; Lethbridge's 2024 population against two divisions at 53,722 |
| M10 | 2023 seat shares and the Loosemore-Hanby, Gallagher and Rae indices (no source given) | pp.103–104 | R | `data/reference/alberta_2023_results.csv` |
| M11 | A Meta "$13-billion artificial intelligence data centre" near Morinville-Sturgeon | p.13 | W | Public announcements |
| M12 | Springbank dry reservoir "$850-million" | p.68 | W | Government of Alberta project page |
| M13 | Agriculture is "nearly 20% of GDP in the Lethbridge region"; "roughly 4,000 people in Lethbridge alone work directly for local food processing plants" (no source given) | p.74 | W | Statistics Canada; City of Lethbridge / Economic Development Lethbridge |
| M14 | Saddle Lake has about 11,000 members | p.15 | W | Indigenous Services Canada registered population |
| M15 | The mid-2025 provincial population estimates "were not scheduled to be released until July 2026" | p.101 | W | Treasury Board and Finance release calendar |
| M16 | The panel's own band: 25% of 53,722 is 13,430; 40,292 to 67,152 | p.102 | R | Arithmetic |
| M17 | Case citations: Carter [1991] 2 SCR 158; Lalande 2026 SCC 13; 1991 ABCA 317; 1994 ABCA 342 (existence, and whether each says what it is cited for) | ss.4–12 | W | CanLII |

## Minority claims

| ID | Claim | Para. / page | Checker | Source to check against |
|---|---|---|---|---|
| N1 | Miller "was the only one of the five commissioners to agree to the contents of the Addendum" | ¶3, p.116 | R | Commission final report (Addendum, Rec. 5) |
| N2 | Lethbridge residents sought to preserve the city's boundaries "by an over 5:1 margin" in their submissions; "approximately 75 to 14" | ¶117, ¶127 | W | Commission submission archive |
| N3 | "Rebecca Brown was the only resident of Bearspaw who wrote about this issue" | ¶104 | W | Commission submission archive |
| N4 | "Dividing Springbank was never proposed to the ABEBC" | ¶106 | W | Commission submission archive |
| N5 | "Not a single submission, to our knowledge, asked for Diamond Valley to be paired with Banff" | ¶138 | W | Commission submission archive |
| N6 | "Most of our colleagues' proposed boundaries were also clearly opposed by the vast majority of submissions that the ABEBC received" | p.115 | W | Commission submission archive; the audit's §5.9.4 labels |
| N7 | City populations (Alberta Municipal Affairs 2024; Fort McMurray 83,467 from the 2025 municipal census; Sherwood Park 75,575) and gaps of 20,000 or more against Lethbridge | ¶95–97, Table 2 | W | Municipal Affairs 2024 population list; municipal censuses |
| N8 | Including Bearspaw and Springbank in Calgary adds "about an additional 350 persons per Calgary electoral division" | ¶110–112 | R | App. 7; commission majority populations |
| N9 | Table 5: the majority's changes to Calgary and Lethbridge "increase population disparities. In small ways" | ¶147–151 | R | App. 7; commission majority populations |
| N10 | Calgary and Lethbridge are "where Alberta's most competitive electoral divisions are disproportionately found at present" | ¶56 | R | 2023 results |
| N11 | Agriculture employs 11,500 of 155,100 in the Lethbridge-Medicine Hat region, June 2026 (no source given) | ¶131 | W | Statistics Canada Labour Force Survey, economic region |
| N12 | "There is no precedent for the redrawing of the entirety of a province after an independent commission has completed that task in at least the past three decades of Canadian history" | ¶18 | R + W | The audit's own record (Bratt; the 1992 Alberta case) and other provinces |
| N13 | The panel had "4.5 months from the appointment of the panelists", against about 12 months for a commission | ¶72 | W | Committee transcripts; Motion 37 |
| N14 | Government statements at the passage of Motion 37 (Canadian Press, 18 April 2026; the Premier's Chief of Staff on X; the MLA for Leduc-Beaumont) | ¶79–81 | W | The articles and posts cited |
| N15 | Sigalet, Inside Policy (Macdonald-Laurier Institute), 4 May 2026, and Lisa Young's newsletter, 19 April 2026, say what they are quoted for | ¶55–56 | W | The articles |
| N16 | Case citations: Sinclair-Desgagne 2026 SCC 31; Henriksen Estate 2026 BCSC 1058; Hunt 2026 FCA 88; Piekut 2025 SCC 13; Nova Scotia Reference 2017 NSCA 10; Federation acadienne 2024 NSSC 339; SC 2022 c 6 (existence, and whether each says what it is cited for) | throughout | W | CanLII; federal statutes |
| N17 | Ian Gray's figure: a vote in Edmonton-Glenora-Riverview "worth roughly 32% less" than in Drumheller-Stettler | ¶153 | R | Interim Report populations (the geography Gray addressed) |

## Internal consistency

The 30 discrepancies in section 8 of the reading are checked in the text layer and reported as found. Items 1, 3, 4, 5, 6, 7, 11, 12 and 13 are confirmed in the text; the others are naming, layout or different-map comparisons, labelled as such.
