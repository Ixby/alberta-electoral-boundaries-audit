# Recommendation 5, graded by degree (2026-11-06)

**Unregistered, written after Step C was seen.** The registered result is X1 (Amendment 5, Part 13): **not met**, and it stands (`../a10_stepc/x1.json`; rerun on v3 with the same result, `x1_v3.json`). X1 is pass or fail by design. This file reports the same recommendation by degree, beside it. Nothing here is a finding on whether any map is a gerrymander, and nothing rules on whether a departure was necessary.

Reproduce: `score_x1.py --map <v3> --name-col district --out findings/iap_r5_degree/x1_v3.json`, then `findings/iap_r5_degree/r5_degree.py`.

## What is being graded

The text is Justice Dallas Miller's Recommendation 5 (Addendum to the Majority Report, final report pp. 66-67; IAP report App. 3). It is not Mr. Lunty's: he chairs the Select Special Committee. Government Motion 37 told the panel to "incorporate the recommendations provided in Recommendation 5 ... subject to any modifications the independent advisory panel considers necessary".

R5 has four lettered conditions and a main clause. The five items below are those. The grade is the degree itself: the count and the share. The words are a label for it, chosen after the results were known.

| Item | What R5 says | Degree | Label |
|---|---|---|---|
| Main clause | "restore the two electoral divisions"; "The rest of the province as we propose must be maintained to the extent possible." | Both restored (Lac Ste. Anne; Rocky Mountain House-Sundre), unanimously. Of the 27 divisions no lettered condition covers, 13 come back identical; 14 changed | Restoration followed; the rest partly |
| (a) | "no impact on any electoral division in Airdrie or containing territory south of Airdrie's southernmost border, with the exception of Drumheller-Stettler" | **29 of 41 divisions identical, holding 71.8% of the zone's population.** 12 changed, 11 of them with people moving. About 142,000 of 2.27 million people (6.3%) no longer sit with the largest part of their division | **Partly: the largest departure** |
| (b) | "no impact on any electoral division north of the North Saskatchewan River in Edmonton" | 11 of 11 identical | Followed |
| (c) | South-of-river Edmonton divisions revert "to the map outlined in the interim report, with the possible exception of including Nisku in Edmonton-South East" | 9 of 10 match the interim population to the person. The tenth is the Nisku option, as a new division | Followed, using the option R5 allowed |
| (d) | "consider restoring an electoral division mostly consisting of Clearwater County and western Mountain View County ... with s. 15(2) status" | Rocky Mountain House-Sundre: 61% of its population and 79% of its area are in that zone; 99.3% of the zone is in it | Followed |

**How "identical" is read.** Two independent ways, and a division counts only if both agree:
- *Stated:* Appendix 7 against the majority's official table: same name, same population, area within 0.5 km². This needs no reconstruction.
- *Overlay:* the registered 99%/99% rule on the v3 map.

That is why (a) is 29 here and 31 on registered X1. The two extra departures are Calgary-North West and Chestermere-Strathmore (below). The registered 31 is unchanged.

**On (c).** X1 still reports (c) as "not scored", as its rule requires, because the rule needs the interim *map* and no shapefile of it exists here. The check above uses the interim report's Appendix E table (`data/iap/abebc_interim_edmonton_south.csv`, from `evidence/commission_reports/abebc_2025_interim_report.pdf`). Matching populations are strong evidence, not proof, of matching lines. The panel's text agrees ("we are adopting the recommendations of the Commission's Interim Report", p.33, PDF 39).

## Every departure in zone (a)

Population is the majority's stated figure. "Kept" is the share staying with the largest successor; "gain" is the share of the successor from elsewhere (2021 overlay by VA representative point, v3). People moved are estimates. "Support" is the panel's own division of opinion.

| Majority division | Became (largest part) | Stated pop. | Kept | Gain | People moved | Support | Panel's stated reason (page) |
|---|---|---|---|---|---|---|---|
| Calgary-North West | Calgary-North West-Bearspaw | 52,488 → 54,361 | 100% | 0.6% | gains Bearspaw (+1,873 stated) | Majority only | Bearspaw "functionally integrated" with Calgary; "this is not gerrymandering by the panel" (p.59, PDF 65) |
| Calgary-Bow | Calgary-Bow-Springbank | 54,982 → 58,673 | 100% | 5.1% | gains North Springbank | Majority only | "It mixes urban with urban residents." (p.65, PDF 71) |
| Calgary-West-Elbow Valley | Calgary-West-Springbank | 54,167 → 58,305 | 100% | 10.1% | gains South Springbank | Majority only | "much more regular polygon shape with straight line boundaries" (p.67, PDF 73) |
| Cochrane-Springbank | Cochrane | 56,487 → 46,785 | 83.4% | 0% | ~9,400 | Majority only | Springbank's tie to Calgary "even stronger than its connection to Cochrane" (p.71, PDF 77) |
| Canmore-Banff | Banff-Canmore-Diamond Valley | 39,961 → 48,862 | 93.4% | 19.8% | ~2,600 | Under 1,000 people unanimous (minority ¶6); the rest majority only | "a minor change ... to capture the necessary population" (PDF 95); avoids s.15(2) (p.89) |
| Okotoks-Diamond Valley | Okotoks | 55,284 → 49,853 | 86.9% | 6.1% | ~7,300 | Majority only | Follows from Banff-Canmore-Diamond Valley (p.89-90) |
| Lethbridge-East | Lethbridge | 57,463 → 58,897 | 52.3% | 54.0% | ~27,400 | Majority only | "Lethbridge already has population to spare." (p.74, PDF 80) |
| Lethbridge-West | Lethbridge | 54,235 → 58,897 | 59.2% | 46.0% | ~22,100 | Majority only | Same |
| Taber-Cardston | Lethbridge-Taber-Warner | 54,933 → 52,955 | 63.7% | 38.3% | ~19,900 | Majority only | Lethbridge residents supply "necessary population" (PDF 79) |
| High River-Vulcan-Siksika | Macleod-Crowsnest | 53,351 → 52,185 | 51.2% | 43.8% | ~26,000 | Majority only | Southern community of interest (pp.73-76) |
| Livingstone-Macleod | Macleod-Crowsnest | 50,144 → 52,185 | 46.0% | 56.2% | ~27,100 | Majority only | "avoids the incongruous encirclement of the City of Lethbridge" (p.87, PDF 93) |
| Chestermere-Strathmore | Chestermere-Strathmore | 56,679, same | 100% | 0% | none | No stated reason found | Stated area 1,025 km² against 1,019.72. It is a 3.25 km² riverbank strip with no voting area (`../iap_reconstruction_check/`), probably a drafting line, not a choice |

Full table of all 41: `zone_a_divisions.csv`. Numbers: `r5_degree.json`.

Two things the registered rule cannot show:
- **Calgary-North West passes the 99% rule and still changed.** Only 0.6% of its overlay population is new, so X1 counts it unchanged, yet the panel moved its boundary on purpose and renamed it.
- **Chestermere-Strathmore** has identical people and a different area.

Calgary's other 25 divisions, both Airdrie divisions and both Medicine Hat divisions are identical. The panel's north-east Calgary paper (Cross, Klein, East, Confluence) was not adopted as a map ("no improvements to recommend", p.4, PDF 10), so it is not a departure on the map.

## The 14 changed outside the lettered zones

Barrhead-Westlock-Athabasca, Drumheller-Stettler (R5(a)'s named exception), Fort McMurray-Lac La Biche, Fort McMurray-Wood Buffalo, Lacombe-Clearwater, Leduc-Devon, Mountain View-Kneehill, Red Deer-South, Spruce Grove, St. Albert-Sturgeon, Stony Plain-Drayton Valley, Sylvan Lake-Innisfail, West Yellowhead, Wetaskiwin-Ponoka-Maskwacis.

R5's "to the extent possible" expects some of this, so the count does not settle it. The minority treats these as the restoration's cascade (¶6, ¶32, ¶34, list at ¶167), with two objections: about 1,300 Red Deer residents in Blackfalds-Innisfail ("unnecessary and ill-advised", ¶37), and Wheatland County in Olds-Didsbury-Three Hills (¶167, item 91).

## Were the departures allowed? Each side, no ruling

Motion 37's test is what "the independent advisory panel considers necessary". So a departure from R5 is not by itself a breach of the panel's terms. What the record shows:

- **The panel's position.** R5's mandatory wording "may not have been deliberate. Clearly, it was inappropriate." (p.92, PDF 98). The conditions were "not binding on the panel" (p.93, PDF 99), and the direction to review the whole province "made it 'necessary' to adjust that so-called condition" (same page). The panel makes that argument about R5 as a whole. For the individual zone (a) changes its reasons are better representation or merit, as tabled above; "necessary population" appears only for the Lethbridge and Canmore population balance.
- **The minority's position.** "all additional changes that our colleagues recommend to areas south of Airdrie fall outside this Panel's mandate" (p.114, PDF 120); the majority reads "necessary" as "preferable" (¶84, p.134). Its list at ¶167 is its claim that the two restorations can be done while touching only Drumheller-Stettler and fewer than 1,000 people in Canmore-Banff in zone (a). **That is the comparison point for degree: 40 of 41 on the minority's list against 29 of 41 on the map proposed.** The audit has not built or tested that list as a map.
- **The committee.** It changed nothing: it resolved to "acknowledge" the report and "conclude its review" (final report, section 5.0). The opposition members' appendix says motions to bind the panel to R5, including no changes south of Airdrie, "were voted down by the UCP majority". That is their account, in their minority report.
