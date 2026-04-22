# v0.1 Calgary Data Sources Audit — post-2021, sub-city

**Question:** Track L's A2 zone-gap finding (Calgary minority: +12.20% NE/central-vs-S/W; majority: +0.36%) uses 2021 Census dissemination-area populations. Does any publicly-available Calgary dataset newer than the 2021 Census exist at ward, community, or other sub-CMA geography that could be used to re-run A2 at a fresher vintage? Track L's verdict was "blocked: Calgary cancelled its civic census in 2020." This audit verifies that claim.

**Bottom line:** Track L's "blocked" verdict is **substantively correct for the specific A2 re-run** but **overstated as a blanket statement**. No publicly-available dataset publishes a 2024 or 2025 population count per Calgary ward or per Calgary community. Every Calgary sub-city population figure currently in public circulation ultimately traces back to the 2021 Federal Census. The newer data that does exist (SRG sector forecasts, dwelling counts, building permits, school enrolment by school) either stops at planning-sector resolution (7 sectors, not 14 wards), measures a growth increment rather than a population level, or requires a crosswalk that has not been publicly published post-2021.

The gap is narrower than Track L framed. A 2026 federal census is scheduled; detailed release begins late 2027. Between now and then, the only sub-city population signal is **growth direction** (via SRG sectors and per-sector permit counts), not **population level**. An A2 re-run at ward level today would be a crosswalk exercise built on 2021 Census ward totals uplifted by sector growth — which is a model, not a measurement.

## Verdict summary

| Rank | Source | Geography | Vintage | Verdict | A2 re-run utility |
|---:|---|---|---|---|---|
| 1 | Calgary SRG Forecast (Socrata dataset `e7ib-v9n4`) | 7 planning sectors | 2018–2028, updated Aug 2024 | **USABLE** as growth proxy | Can uplift 2021 Census ward totals via sector→ward crosswalk; produces a modelled 2024/2025 ward population, not a measurement |
| 2 | Communities by Ward crosswalk (Socrata `jd78-wxjp`) | Community → ward, 206 communities | Updated 2024-04-15 | **USABLE** as a crosswalk | Essential infrastructure for any sub-city re-run; does not itself contain population |
| 3 | StatsCan 17-10-0142 / CSD 2021-boundary successor | CSD (Calgary = single CSD) | 2024 estimate (1,569,133 on 2024-07-01) | **PARTIAL** | Citywide total, not sub-city. Use as control total for a modelled ward distribution |
| 4 | Calgary & Region Population Outlook, Corporate Economics | City of Calgary, CER, CMA | 2024 and 2025-2030 editions | **USABLE** for citywide control | No ward/community detail |
| 5 | Alberta Regional Dashboard — Calgary | City of Calgary | 2025 | **USABLE** for citywide control | No sub-city resolution |
| 6 | CMHC Rental Market by Zone (Calgary) | 10 CMHC zones inside Calgary CMA | Oct 2025 | **PARTIAL** | Publishes vacancy, rent, unit counts — **not** population. Zones are CMHC-specific, not ward-aligned |
| 7 | Calgary 2021 Federal Census by Ward (Socrata `k4pr-cznc`) | 14 wards | 2021 Census, static | Baseline | Already in the audit |
| 8 | Calgary Community Profiles (206 communities) | Community | 2021 Census, published 2023 | Baseline | Already the level the audit could but does not drill to |
| 9 | Civic Census by Community & Dwelling Structure (Socrata `set9-futw`) | Community | Frozen at 2019 | **UNUSABLE for refresh** | Last civic census 2019; program cancelled 2020; resumes 2027 |
| 10 | CBE 2024-25 Enrolment Report | School (mappable to community) | Sept 2024 | **PARTIAL** | Proxy for child-population change; total K-12 = 142,402; would need school→community→ward rollup |
| 11 | Calgary Building Permits (Socrata `c2es-76ed`) | Permit address | Live | **PARTIAL** | 2024 permits issued = 18,168 residential. Usable as growth-direction signal at community level with geocoding |
| 12 | Calgary Transit Ridership (Socrata `iema-jbc4`) | System-level | Live monthly | **UNUSABLE for A2**; useful for Track G (Cochrane) | No station-level or O-D detail in the public release |
| 13 | CMRB Regional Housing Needs Assessment 2024 | CMRB region / member municipalities | 2024 | **PARTIAL** | Member-municipality rollup, not Calgary sub-city |
| 14 | AHS population by AHS Zone | Calgary AHS Zone (whole southern AB) | Annual | **UNUSABLE** | Calgary Zone > City of Calgary; too coarse |
| 15 | Airdrie 2025 Municipal Census | City of Airdrie | 2025 | **USABLE** for Track L | Calibrates `AIRDRIE_GROWTH = 1.168` used in `v0_1_track_l_drift.py` |
| 16 | Cochrane / Chestermere / Okotoks 2024/2025 estimates | Individual CSD | 2025 | **USABLE** for Track L | Calibrates ring-town growth factors in Track L Plan B |

## Sources checked, in detail

### 1. City of Calgary Open Data Portal (data.calgary.ca)

**2021 Federal Census Population and Dwellings by Ward** — `k4pr-cznc`
- URL: https://data.calgary.ca/Demographics/2021-Federal-Census-Population-and-Dwellings-by-Wa/k4pr-cznc
- Metadata confirms: "one-time load of Statistics Canada federal census data from 2021," update frequency every 5 years. Last rowsUpdatedAt October 2024, but that is the dataset-description edit, not new population data. Ward boundaries frozen at 2022 (the ward-boundary redraw for 2025 was applied separately to `r9vx-mhnf`).
- Vintage: **2021 only.** Next refresh cycle: 2026 Census release (starts late 2027).

**Civic Census by Ward and Dwelling Structure** — `yr3w-mcsu`
**Civic Census by Community and Dwelling Structure** — `set9-futw`
- Last data year: **2019**. Row count confirmed via Socrata `$select=max(census_year)`: 2019.
- Civic Census program cancelled in 2020 budget cuts, officially reinstated by Council in 2024, first new census **2027** (biennial thereafter). Exactly as Track L stated.
- Verdict: **UNUSABLE for a 2024/2025 A2 refresh.** These are the tables that would be ideal if the program had run. They stopped in 2019.

**Communities by Ward** — `jd78-wxjp`
- URL: https://data.calgary.ca/Government/Communities-by-Ward/jd78-wxjp
- **Last updated: 2024-04-15.** Schema: `comm_code`, `name`, `sector`, `srg` status, `comm_structure`, `ward_num`. 206 communities mapped to 14 wards and 7 SRG sectors.
- Verdict: **USABLE as infrastructure.** This is the missing-piece crosswalk for any sector-to-ward or community-to-ward re-aggregation. Mapping 2021 Census community totals to 2025 wards using this crosswalk is straightforward; mapping SRG sector-level growth increments back down to ward is the harder direction and relies on the assumption that within-sector growth is uniform.

**Community Boundaries** — `ab7m-fwn6`
- URL: https://data.calgary.ca/Base-Maps/Community-Boundaries/ab7m-fwn6
- Last updated: 2026-04-01. Spatial layer only; no population field.
- Verdict: **USABLE as geometry** for any spatial re-aggregation of census DAs to current community boundaries.

**Ward Boundaries** — `r9vx-mhnf`
- Updated 2025-11-01 (post-2025-election boundary adjustment).
- Verdict: **USABLE as geometry.** Note: the A2 analysis should re-check ward boundary vintage against its own DA-to-ward join if this update has moved lines.

**Annual Dwelling Count by Dwelling Type** — `j687-p59z`
- Metadata suggests 1997-present annual, but rowsUpdatedAt = 2019-09-04. Last genuine load is ambiguous; Socrata API returned empty rows on `$select=max(census_year)`.
- Verdict: **PARTIAL** at best. Needs direct data-owner confirmation.

**Single Family Home Ownership by Community** — `smdf-sxph`
- Static artefact from Civic Census era (no 2020-2023 refresh).
- Verdict: **UNUSABLE** for post-2021.

**Building Permits** — `c2es-76ed`
- Live, permit-by-permit with address geocoding. 2024 total = 18,168 residential permits (5,341 single-detached, 1,842 semi-detached, 3,343 townhouses, 7,312 apartments). Plus 3,787 new secondary suites.
- Verdict: **PARTIAL.** A permit is not a completed dwelling, and a dwelling is not an occupied household. Usable as a **growth-direction signal** by community if geocoded to community boundaries, but a permit-to-population conversion requires occupancy assumptions (1.5–2.6 persons per unit in Calgary, varying by unit type and community) that introduce modelling uncertainty.

### 2. City of Calgary Planning Services & Data Analytics

**Suburban Residential Growth (SRG) Forecast** — Socrata `e7ib-v9n4` + storymap
- URL (data): https://data.calgary.ca/Services-and-Amenities/Suburban-Residential-Growth-SRG-Forecast/e7ib-v9n4
- URL (2024–2028 storymap): https://storymaps.arcgis.com/stories/6d7a9bcb73814daab1ff73bf7e1001d9
- URL (2025–2029 storymap): https://storymaps.arcgis.com/stories/8f63497a4e9343b6af311defa8ae0eb1
- Last updated (data): **2024-08-06.** Semiannual cadence.
- Schema: `sector_key`, `year`, `sector` (one of NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, WEST, NORTHWEST), `lowd_units`, `multi_units`, `ttl_units`, `low_pop`, `multi_pop`, `ttl_pop`. 77 rows covering years 2018–2028.
- Critical caveat: **`ttl_pop` is the population expected to be absorbed by newly-constructed dwellings in new suburban communities per sector per year**, not total sector population. A 2024 West sector `ttl_pop` near 7,000 does not mean West sector has 7,000 residents; it means ~7,000 net new residents absorbed into new dwellings that year. This is a growth increment, not a population level.
- Verdict: **USABLE as a growth proxy**, not as a population snapshot. To get a 2024 or 2025 ward-level population one would have to: (a) take 2021 Census community totals, (b) use Communities-by-Ward to aggregate to ward, (c) apportion annual SRG sector-level new-dwelling population down to the new-community level using SRG's per-community housing-starts data, (d) apportion established-community growth from StatsCan citywide control totals proportionally, (e) sum back up to ward. Each step introduces modelling uncertainty.

**Calgary and Region Population Outlook 2024–2029 (Spring 2024)**
- URL: https://www.calgary.ca/content/dam/www/cfod/finance/documents/corporate-economics/calgary-and-region-economic-outlook/spring-2024-calgary-and-region-population-outlook-2024-2029.pdf
- Published by City of Calgary Corporate Economics. Key numbers: April 2023 estimate 1,422,800 (+5.6% on year); 4.9% growth forecast for 2024; 1.5% average 2025–2029; 1,608,700 by 2029.
- Geography: **City of Calgary total, Calgary Economic Region, Calgary CMA.** No ward, no community, no sector.
- Verdict: **USABLE as citywide control total** for Track L's Plan B scaling; **not usable directly for A2 zone breakdown.**

**Calgary and Region Economic Outlook 2025–2030** (Spring 2025, Fall 2025 editions)
- URL: https://www.calgary.ca/research/economic-outlook.html
- Same geography profile; later vintage.
- Verdict: **USABLE** same as above. Fall 2025 edition should be preferred over Spring 2024 for Track L's provincial control target.

**Community Profiles (206) and Ward Profiles (14)**
- URLs: https://www.calgary.ca/communities/profiles.html and https://www.calgary.ca/communities/profiles/wards.html
- Confirmed by direct PDF extraction (Ward 7 profile, 32 pages, 2023 publication): every population figure is **"Population in private households in 2021"** from the 2021 Census of Canada, accessed via the Community Data Program. No post-2021 update.
- Verdict: **Baseline already used.** Ward-level profiles **exist** and are publicly downloadable; the A2 audit could in principle use 14 ward totals directly from these instead of aggregating from DAs, but the vintage is identical to what the audit currently uses (2021). The gain would be computational cleanness, not freshness.

### 3. Calgary Economic Development

- URL: https://www.calgaryeconomicdevelopment.com/insights/demographics/
- Redistributes Corporate Economics citywide figures plus CMA-level StatsCan. No sub-city breakdowns.
- Verdict: **UNUSABLE** for A2 refresh.

### 4. Calgary Board of Education / Calgary Catholic

**CBE 2024–25 School Enrolment Report**
- URL: https://cbe.ab.ca/FormsManuals/School-Enrolment-Report-2024-2025.pdf
- Total CBE enrolment 2024-25: 142,402 (per news release). Report includes per-community growth Sept 2023 → Sept 2024.
- Verdict: **PARTIAL proxy.** A CBE school catchment does not equal a community does not equal a ward. Building a school-to-ward rollup is feasible but brittle: ~240 CBE schools, private-school and Calgary Catholic kids not counted, catchment overlaps, and students who enrol outside catchment introduce noise. Proxies only the 5–18 age band, not total population. Would be useful to corroborate sector-level growth direction but not to produce a ward-level population level.

### 5. Calgary Transit — orthogonal to A2, relevant to Track G

**Calgary Transit Ridership** — Socrata `iema-jbc4`
- System-level monthly ridership, fare categories, no station-level O-D.
- Verdict: **UNUSABLE for sub-city population.** Also **UNUSABLE for Track G's Nolan Hill question** — publishes no boarding-by-station data, no O-D disaggregation within Calgary.

**Calgary Transit Routes** — Socrata `hpnd-riq4`
- Route geometry. No rider data.
- Verdict: Not relevant.

No public Calgary Transit dataset provides origin-destination pairs within Calgary or station-level LRT/BRT boarding counts at the level of geography Track G needs (Cochrane-bound commuter destination within Calgary). This dataset family **does not resolve** the within-Calgary destination gap that Track G called out.

### 6. CMHC

**Rental Market Survey by Calgary zone** (October 2025)
- URL: https://www03.cmhc-schl.gc.ca/hmip-pimh/en/TableMapChart/Table?TableId=2.1.31.3&GeographyId=0140&GeographyTypeId=3
- 10 CMHC-defined zones inside Calgary CMA (Downtown, Beltline, North Hill, Southwest, Southeast, Northwest, Northeast, Chinook, Fish Creek, Other Centres).
- Publishes unit counts, vacancy, rent — **not population.** Zones are purpose-built for housing-market reporting, not aligned to wards.
- Verdict: **PARTIAL.** Unit-count growth by CMHC zone is a signal; converting to population needs occupancy assumptions and a CMHC-zone→ward crosswalk that does not exist publicly.

**CMHC Housing Supply Report Fall 2024**
- URL: https://assets.cmhc-schl.gc.ca/sites/cmhc/professional/housing-markets-data-and-research/market-reports/housing-supply-report/2024/housing-supply-report-2024-fall-en.pdf
- CMA-level analytic summary; no sub-CMA population.
- Verdict: **UNUSABLE.**

### 7. Alberta Health Services

**Distribution of Population Covered by AHS Geographic Zone** (Open Alberta)
- AHS Calgary Zone encompasses Calgary plus surrounding MD/CSD ring (Airdrie, Cochrane, High River, etc.). Population ≈ 1.8 million. Larger than the City of Calgary CSD.
- AHS does not publicly release intra-Zone population breakdowns at ward or community level.
- Verdict: **UNUSABLE.**

### 8. CFIB / Calgary Chamber / BILD Calgary

**BILD Calgary** — builder-industry association, publishes housing-starts and buyer-demand at sector level, largely re-publication of Corporate Economics/CMHC figures with industry commentary.
**Calgary Chamber** — macro economic commentary, no sub-city population.
**CFIB** — business-employment at provincial level.
- Verdict: **UNUSABLE** for ward-level population.

### 9. Statistics Canada Administrative Data

**Table 17-10-0142 (archived) / 2021-boundary successor** — CSD-level population estimates
- Calgary appears as a single CSD (DGUID 2021A00054806016). **No sub-city decomposition.**
- Most recent: 2024 postcensal estimate (July 1, 2024) = **1,569,133.** 2025 edition released January 2026.
- URL (2024 Daily release): https://www150.statcan.gc.ca/n1/daily-quotidien/250116/dq250116b-eng.htm
- Verdict: **PARTIAL.** Usable as a citywide control total for any A2 ward-distribution model, not as a direct sub-city input.

**Table 98-10-0459 (2021 Census commuting)** — already used by Track G, confirmed no within-Calgary disaggregation.

**Table 17-10-0135** (estimates, CSD, prior boundaries) — superseded, same geography limits.

### 10. Ring-municipality cross-reference (Track L calibration, not A2)

- **Airdrie 2025 Municipal Census:** 90,044 (vs Track L's assumed 1.310 ≈ 101,000 — TRACK L FIGURE APPEARS OPTIMISTIC IF APPLIED TO 2024 DATA; 90,044 is from April 2025 municipal count, not July 2025 StatsCan estimate which is closer to 92,544.) Flag for Track L review.
- **Cochrane:** 2024 municipal estimate ≈ 39,397 (vs Track L's 1.205 × 32,199 ≈ 38,800). Consistent within 2%.
- **Chestermere:** 2025 municipal = 31,671 (vs Track L's 1.352 × ~20,000 = ~27,000 plus July estimate 33,360). Roughly consistent.
- **Okotoks:** 2025 = 32,992 (vs Track L's 1.155 × 28,881 ≈ 33,358). Consistent within 1%.
- Verdict: Track L's ring-municipality growth factors are **largely vindicated by published 2024/2025 municipal censuses.** The Airdrie figure warrants a second look (the municipal April 2025 number is 90,044 vs Track L's implied ~101,000 for mid-2025) but the discrepancy is within the stated uncertainty band of Track L.

## Top-3 highest-value Calgary datasets newer than 2021 the audit should use but currently isn't

1. **Communities by Ward crosswalk (`jd78-wxjp`, updated 2024-04-15).** This is essential plumbing for any sub-city re-aggregation. The A2 audit currently works at DA level; adding a community→ward layer would allow the zone-gap finding to be re-stated in the same unit of analysis (ward) that both the city and the Commission use. **Zero freshness gain**, but substantial clarity and robustness gain. The 14-ward total from the 2021 Census is already in `k4pr-cznc` at Socrata.

2. **SRG Forecast (`e7ib-v9n4`, updated 2024-08-06).** The only publicly-available Calgary dataset that publishes a per-sector, per-year post-2021 population **increment** at sub-city resolution. Not a population level; not directly a ward. But when combined with the Communities-by-Ward crosswalk and the 2021 Census ward baseline, it can produce a modelled 2024 and 2025 ward-level population that would be defensible as a sensitivity check on A2. **Not a replacement for the census, a stress-test on the A2 finding's robustness to intercensal drift.**

3. **StatsCan 2024 CSD postcensal estimate (1,569,133 as of July 2024).** Citywide control total. Already cited in Track L indirectly via the provincial reconciliation target. Making it explicit in A2 (as the total against which any ward-distribution model must sum) would tighten the audit's documentation.

## Ward-level or community-level 2024/2025 populations published directly?

**No.** Confirmed by direct metadata pull and PDF extraction:
- The only public per-ward population number is 2021 Census (Socrata `k4pr-cznc`; Ward 7 profile PDF; community profile PDFs).
- The only public per-community population number is 2021 Census (206 community profiles) or 2019 Civic Census (Socrata `set9-futw`).
- The SRG Forecast publishes sector-level population **increments** (7 sectors, 2018–2028) but not absolute sector populations, and not at ward granularity.
- The Civic Census program will not produce new sub-city population data before 2027.

## Can the A2 Calgary zone-gap finding be re-run at fresher granularity with publicly-available data TODAY?

**Not as a measurement.** As a model: yes, with caveats.

A defensible 2024 or 2025 ward-level population model could be built from:
1. 2021 Census ward totals (Socrata `k4pr-cznc`, 14 rows).
2. StatsCan 2024 citywide postcensal estimate (1,569,133) as the control total.
3. SRG per-sector population increments 2022–2024 (Socrata `e7ib-v9n4`).
4. Communities-by-Ward crosswalk (Socrata `jd78-wxjp`) to map sectors to wards.
5. Building permits geocoded to ward (Socrata `c2es-76ed`) to refine established-ward uplift.

The residual uncertainty is the within-sector allocation of growth (the SRG publishes sector-level, not community-level, population absorption in its public dataset; the community-level data lives inside the storymap and may require a different endpoint). A Monte Carlo run with plausible within-sector allocation ranges would produce a confidence band on each ward's modelled 2024 population.

An A2 re-run on this basis would answer **"does the NE/central vs S/W gap persist if we use our best 2024 model rather than the 2021 Census?"** It would not answer **"what do 2024 NE/central and S/W populations actually measure?"** — that question is unanswerable with current public data.

## Track L's "blocked" verdict — stands or revised?

**Revise to: "blocked for direct measurement, open for modelled sensitivity."**

Track L's literal claim — that Calgary publishes no 2024/2025 ward or community-level population — is correct. The Civic Census cancellation and the 2027 restart are both real. No public dataset today provides a measured ward-level population for any year after 2021.

But Track L framed this as total closure, and that is overstated. The public data ecosystem is richer than the verdict suggested. There is enough material — SRG sector forecasts, a maintained Communities-by-Ward crosswalk, live building-permit data, StatsCan CSD postcensal totals — to build a transparent, reproducible 2024/2025 ward-level **model**. Whether the A2 finding survives that model (the +12.20% minority gap and +0.36% majority gap persist, shrink, or flip) is the question the audit could answer but has not tried to.

Recommendation: downgrade the verdict from "blocked" to "blocked for measurement, unaddressed for modelling." Flag the three datasets above (Communities-by-Ward crosswalk, SRG Forecast, StatsCan CSD 2024 estimate) as the minimum input bundle for a sensitivity re-run. The A2 zone-gap finding as stated is still the best available direct evidence; the modelling question is whether it holds under intercensal drift, and that question is answerable with the inputs catalogued here.

## Commute data for Track G (orthogonal to A2)

No publicly-available Calgary Transit or CMRB dataset disaggregates commute flows **within** Calgary. Station-level LRT boarding data is not in the public Socrata feed. The CMRB does not publish a post-2021 origin-destination survey. Track G's "Nolan Hill vs downtown vs SE" question remains unanswerable from open data; custom tabulation from StatsCan (2021 Census, Census Tract place-of-work) is the only public path and requires a custodian request.

This is consistent with what `v0_1_cochrane_journey_to_work.md` already flagged as follow-up. No change required to that verdict.

## Files and URLs — quick reference

| Artefact | URL | Vintage | Machine-readable |
|---|---|---|---|
| Communities by Ward crosswalk | https://data.calgary.ca/Government/Communities-by-Ward/jd78-wxjp | 2024-04-15 | Yes (Socrata JSON/CSV) |
| SRG Forecast | https://data.calgary.ca/Services-and-Amenities/Suburban-Residential-Growth-SRG-Forecast/e7ib-v9n4 | 2024-08-06 | Yes |
| 2021 Census by Ward | https://data.calgary.ca/Demographics/2021-Federal-Census-Population-and-Dwellings-by-Wa/k4pr-cznc | 2021 | Yes |
| Civic Census by Community | https://data.calgary.ca/Demographics/Civic-Census-by-Community-and-Dwelling-Structure/set9-futw | 2019 (frozen) | Yes |
| Community Boundaries | https://data.calgary.ca/Base-Maps/Community-Boundaries/ab7m-fwn6 | 2026-04-01 | Yes |
| Ward Boundaries | https://data.calgary.ca/Government/Ward-Boundaries/r9vx-mhnf | 2025-11-01 | Yes |
| Building Permits | https://data.calgary.ca/Business-and-Economic-Activity/Building-Permits/c2es-76ed | Live | Yes |
| Population Outlook 2024-29 | https://www.calgary.ca/content/dam/www/cfod/finance/documents/corporate-economics/calgary-and-region-economic-outlook/spring-2024-calgary-and-region-population-outlook-2024-2029.pdf | Spring 2024 | PDF |
| Economic Outlook 2025-30 | https://www.calgary.ca/research/economic-outlook.html | Spring / Fall 2025 | PDF |
| StatsCan CSD estimate 2024 | https://www150.statcan.gc.ca/n1/daily-quotidien/250116/dq250116b-eng.htm | 2024-07-01 | Table |
| Ward Profile PDF example (Ward 7) | https://www.calgary.ca/content/dam/www/programs-services/property-housing-and-neighbourhoods/neighbourhood-and-community-relationships/profiles/ward-profiles/ward-7-profile.pdf | 2021 Census, 2023 publication | PDF |
| CMHC Calgary zones (rental) | https://www03.cmhc-schl.gc.ca/hmip-pimh/en/TableMapChart/Table?TableId=2.1.31.3&GeographyId=0140&GeographyTypeId=3 | Oct 2025 | HTML/CSV |
| Airdrie 2025 Municipal Census | https://www.airdrie.ca/index.cfm?serviceID=1965 | Apr 2025 | HTML |
| CBE 2024-25 Enrolment | https://cbe.ab.ca/FormsManuals/School-Enrolment-Report-2024-2025.pdf | Sept 2024 | PDF |

## Notes on confidence

This audit was performed via public URL enumeration, Socrata API metadata pulls, and PDF extraction. Coverage is not exhaustive — in particular, the Suburban Residential Growth storymap contains community-level tables that are accessible via the ArcGIS Story Maps UI but not through the Socrata API, and which could not be inspected in this session because the UI requires browser rendering. A follow-up pass with a browser-rendering tool could extract community-level SRG data if the sector-level data is judged insufficient for an A2 model.

The Community Data Program (communitydata.ca) was noted in CBE and ward-profile metadata but not directly queried; it is a member-login service and requires institutional credentials. Calgary's ward profiles cite it as the source through which StatsCan 2021 Census data was accessed. It is unlikely to contain post-2021 data that StatsCan itself has not released.

A2-relevant TODO for the audit (flag only, no edits made per task scope):
- Consider commissioning a sensitivity re-run using the Communities-by-Ward crosswalk, SRG Forecast, and StatsCan 2024 CSD total. If the +12.20% minority gap persists within a ±3% band across plausible within-sector allocation rules, the A2 finding is robust to intercensal drift. If it narrows below the legal-window threshold, the finding's policy weight needs restating.
- Consider the 2026 Census release schedule (detailed sub-city tables out late 2027) as the natural sunset date for the current A2 finding's freshness caveat.
