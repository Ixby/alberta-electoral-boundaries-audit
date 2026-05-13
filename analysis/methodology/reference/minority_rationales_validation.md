# v0.1 Minority Rationales — Phase 2 Validation + Phase 3 Synthesis

Rationales are tested against the most authoritative public dataset for each type. Verdict keys:

- **CLOSED-FAIL** — already refuted by `justification_tests_findings.md` (population/area math).
- **CONTRADICTS** — primary-source data is inconsistent with the rationale as stated.
- **SUPPORTS** — primary-source data is consistent with the rationale.
- **INCONCLUSIVE** — data available is insufficient to decide; direction leans X or is neutral.
- **ALREADY-TESTED** — covered by another track of this audit; verdict imported.

---

## Commuter-tie rationales

**Authoritative source.** StatsCan 2021 Census Journey-to-Work, table series 98-10-0459 (place-of-work CSD by place-of-residence CSD). Only Cochrane origin-CSD file was downloaded and parsed (`.temp/cochrane_ab.csv`, 5,162 rows filtered to Alberta destinations). For Airdrie, Chestermere, Okotoks, Bearspaw, Tsuut'ina, Red Deer, Innisfail, Lacombe, Sylvan Lake — only aggregate CMA-membership evidence is available without downloading additional origin tables.

### R1. Calgary-Nolan Hill-Cochrane — Cochrane residents "fluidly move" to Calgary

- **Test.** Cochrane CSD place-of-work distribution, 2021 Census.
- **Finding.** Of 8,550 Cochrane commuters (AB destinations), **4,205 (49.2%) work within Cochrane**, **3,065 (35.8%) to Calgary CY**, 345 (4.0%) to Rocky View, 185 (2.2%) to Canmore, 130 (1.5%) to Airdrie. Edmonton: 30 (0.4%).
- **Verdict.** **PARTIALLY SUPPORTS.** A real Cochrane→Calgary commute flow exists (~36% of commuters), which is a legitimate community-of-interest tie. However, **the rationale justifies pairing Cochrane with Nolan Hill specifically**, via a narrow corridor that skips Rocky Ridge/Tuscany. The 35.8% Calgary figure is a city-wide average — it is *not* specific to Nolan Hill. Cochrane workers distribute across downtown, industrial, airport, and suburban Calgary destinations; the data cannot be read as showing a Cochrane–Nolan Hill shared community. The minority's narrative conflates "commute to Calgary" with "belongs in the Nolan Hill district."
- **Additional note.** The "Cochrane residents move fluidly between jurisdictions" framing is also undercut by the near-50% within-Cochrane work share. Cochrane has a substantial *internal* labour market; it is not a pure dormitory suburb. This is consistent with the public-report finding that Cochrane is geographically separated from Nolan Hill by the Bow River valley, Calgary city limits, and different local government.

### R2. Calgary-Peigan-Chestermere — "growing social, economic, transportation connections"

- **Test.** CMA membership; Chestermere CSD-origin place-of-work data not on hand in this session.
- **Finding.** Chestermere (22,163) is part of Calgary CMA; the CMA designation confirms a commuting tie to Calgary above the 50%-flow threshold required for CMA membership. The rationale is **not contradicted** at the city-to-city level.
- **But.** The specific boundary change — extending Calgary-Peigan east to absorb southern Chestermere — is tested against whether southern Chestermere shares institutions with Greater Forest Lawn. No shared school division (Chestermere is served by Rocky View Schools; Forest Lawn is Calgary Board of Education — different jurisdictions). No shared transit (Chestermere does not participate in Calgary Transit). Different municipal governments. The only "connection" that is measurable is QE2/Glenmore Trail highway access.
- **Verdict.** **INCONCLUSIVE / LEANS CONTRADICTS.** CMA tie supports a general Chestermere-Calgary commuter relationship, but no test of the *specific* southern-Chestermere–Forest-Lawn pairing yields a community-of-interest match. Red-flag: Chestermere is already paired with Strathmore in the minority's own `Chestermere-Strathmore` district (52,982). Adding a *second* Chestermere-Calgary slice is the object of Test 5 in `justification_tests_findings.md` — CLOSED-FAIL on population math.

### R3. Calgary-Airdrie — "strong economic, community, and transportation ties"

- **Test.** CMA membership (yes); projected growth; origin-CSD commute data not downloaded.
- **Finding.** Airdrie is in Calgary CMA. Airdrie's 2025 population is reported at 90,044 (4.9% annual growth) per City of Airdrie growth report (2024); projected 128,470 by 2033 under current-growth assumptions, adding 50,000 residents. *CMA membership alone already establishes a commuter tie above threshold.*
- **Verdict.** **SUPPORTS** (at the general commuter-tie level). This is the strongest minority rationale of the inventoried set. However, whether this *requires* a Calgary-Airdrie hybrid rather than two Airdrie-named districts (as the majority draws) is a policy choice, not a data-driven necessity. Population-math side of this claim (4-way split is forced) is CLOSED-FAIL (Test 3).

### R4. Calgary-Foothills-Airdrie West — "functional integration of Airdrie and northern Calgary"

- **Test.** Same as R3 (Airdrie origin).
- **Verdict.** **SUPPORTS** the general commuter-tie premise at the city level. Does not independently justify why Airdrie must be split *four* ways (CLOSED-FAIL on Test 3) rather than two.

### R5. Calgary-Bow-Springbank — Springbank commute + "educational institutions"

- **Test.** Rocky View County is the Springbank CSD parent; Rocky View County CSD (pop 41,028) is in Calgary CMA. Shared schools: Rocky View Schools operates the Springbank schools; Calgary Board of Education operates Bow-area schools. *These are different school divisions.* Transit: Springbank has no connection to Calgary Transit. Shared commercial corridor: Highway 1 / Trans-Canada west is the link.
- **Verdict.** **INCONCLUSIVE.** The CMA-commuter-tie claim holds at the general level. The specific "shared educational institutions" claim is **not supported** — Rocky View Schools and CBE are separate jurisdictions. Calgary students do not attend Springbank schools and vice versa (beyond private and special-program enrolment, which applies province-wide). The minority's reference to "educational institutions" is a rhetorical flourish, not a data-verifiable shared-institution claim.

### R6. Calgary-North West-Bearspaw — "shared commercial corridors and commuter patterns"

- **Test.** Bearspaw is a hamlet in Rocky View County; no dedicated commuting table was pulled. CMA membership: Rocky View County is in Calgary CMA, confirming commuter flow above threshold. Royal Vista commercial area: adjacent to Calgary city limits, within Rocky View County; functionally integrated with Calgary retail/commercial zoning.
- **Verdict.** **SUPPORTS.** Low-stakes pairing; commuter and commercial evidence is consistent. This is one of the less controversial minority hybrids.

### R7. Calgary-West-Tsuut'ina — "economic, employment, transportation ties with west Calgary"

- **Test.** Tsuut'ina Nation borders Calgary directly; the Tsuut'ina-Glenmore Trail extension (opened 2020) provides a direct highway link. Economic integration via Grey Eagle Resort and the Taza retail-residential-commercial development on Tsuut'ina lands is documented public record. Indigenous-consultation dimension (s.15 context): Tsuut'ina Nation pop approx 2,100 (registered); is on reserve directly adjacent to Calgary-West.
- **Verdict.** **SUPPORTS.** Commuter and economic ties are real and measurable via Taza development footprint and Tsuut'ina-Glenmore Trail traffic counts. Indigenous-consultation claim is coherent (real First Nation, real consultation duty). This is the one configuration in the minority where *all* invoked rationales align with primary-source geography.

### R8. Red Deer-Blackfalds — "agricultural services hub" and "chemical plant in Joffre"

- **Test.** Joffre is in Red Deer County, not in the City of Red Deer; the Joffre NOVA petrochemical complex (Nova Chemicals) is approximately 25 km east of Red Deer on Highway 11. Confirmed via Alberta Geographical Names and plant directory. Alix and Clive are in Lacombe County (not Red Deer County); Clive is 30 km east of Red Deer on Hwy 12. The "Highway 21 corridor" is geographically real.
- **Verdict.** **SUPPORTS** the economic-zone claim in narrow sense (Joffre-to-Red-Deer labour-market tie exists). However, pulling a strip of the City of Red Deer (east of Hwy 2) into a riding dominated by rural/small-town residents dilutes Red Deer urban representation — this is the concern tested in `claim_significance_analysis.md` (4 Red Deer hybrids). Majority map accomplishes Joffre representation via a rural Drumheller-Stettler–adjacent configuration.

### R9. Red Deer-Innisfail — "use Red Deer as regional hub"

- **Test.** Innisfail (7,985) and Delburne/Elnora (Red Deer County) are within the Red Deer Regional Municipality service area. Alberta Health Services Red Deer zone serves these communities. Provincial services (Service Alberta, Alberta Works) are based in Red Deer.
- **Verdict.** **SUPPORTS** the hub claim in general. Same dilution concern as R8 applies — the rationale is real at a regional level but does not force a hybrid *containing part of the City of Red Deer*.

### R10. Red Deer-Lacombe — "Highway 11 economic corridor"

- **Test.** Highway 11 (David Thompson Highway) runs east-west from Red Deer through Sylvan Lake, Eckville, to the Rockies. The corridor is a real economic-transportation feature. Gull Lake and Sylvan Lake are tourism anchors. Blackfalds is on Hwy 2 (not Hwy 11) — which slightly weakens the Hwy-11-unity claim (Blackfalds is a Hwy 2 community).
- **Verdict.** **PARTIALLY SUPPORTS.** Corridor logic is internally consistent for most of the district; Blackfalds inclusion is rationalized by Hwy 2 adjacency, not by Hwy 11 — minor narrative inconsistency.

### R11. Red Deer-Sylvan Lake — "urban where they work, go to school"

- **Test.** Sylvan Lake (15,995) residents predominantly work in Red Deer or within Sylvan Lake; Sylvan Lake schools are Chinook's Edge School Division, while Red Deer Public Schools serve the city — *different school divisions.* The "go to school" claim is not supported for K–12 education.
- **Verdict.** **INCONCLUSIVE / LEANS CONTRADICTS** on schools specifically. Commuter tie likely supports; no origin-CSD data on hand for Sylvan Lake to verify flow.

---

## Community-of-interest / shared-institutions rationales

Assessed per district above. Summary of shared-institution claims tested:

| Claim | Institution | Verdict |
|---|---|---|
| Bow-Springbank shares schools | Rocky View Schools vs CBE | **CONTRADICTS** — different divisions |
| Red Deer-Sylvan Lake shares schools | Chinook's Edge vs Red Deer Public | **CONTRADICTS** — different divisions |
| Peigan-Chestermere shares transit | Chestermere not on Calgary Transit | **CONTRADICTS** |
| Peigan-Chestermere shares schools | Rocky View vs CBE | **CONTRADICTS** |
| Red Deer-Innisfail shares health zone | AHS Red Deer Zone | **SUPPORTS** |
| Red Deer-Blackfalds shares Joffre plant labour | NOVA Joffre in Red Deer County | **SUPPORTS** |
| Calgary-West-Tsuut'ina shares commercial (Taza) | Tsuut'ina Nation adjacent | **SUPPORTS** |

**Material finding.** Four of seven tested "shared institution" claims CONTRADICT: the minority's invocation of "schools" and "transit" as community-of-interest glue between suburban hybrids is not borne out by the actual school-division or transit-service boundary data. Three SUPPORT. The rhetoric of shared institutions is stronger than the evidence.

---

## Growth-projection rationales

### R3/R4/R18. Airdrie "rapid growth"

- **Test.** City of Airdrie growth report 2024 projects ~128,470 by 2033 (add 50,000). 2025 population reported 90,044, up 4.9% year-over-year.
- **Verdict.** **SUPPORTS.** Airdrie's growth is measurable, documented in municipal reports, and consistent with the minority's rationale that one or more new hybrid seats accommodate the growth. Does NOT support the specific four-way split (CLOSED-FAIL on population math Test 3).

### R19. Smith's "rural ridings lost" framing

- **Test.** Under the 89-seat majority map, the total count of rural+small-town districts (Rest-type) is 40; under the 89-seat minority map it is 38. Two fewer rural districts under minority than majority, not "lost" under majority specifically — both 89-seat maps collapse the current 87 into a redistribution. Going to 91 seats restores the arithmetic room for 2 extra seats somewhere.
- **Verdict.** **PARTIALLY SUPPORTS.** Smith's framing is grammatically ambiguous ("did not want to lose two rural ridings") but the substance — that 91 seats creates room for 2 more seats, which could be allocated to rural preservation — is arithmetically consistent with Miller's own 91-seat addendum. However, the motion does *not* specify that the two extra seats will be rural; Smith's framing presumes an outcome the motion doesn't guarantee.

### Overall: "Alberta grew 20% since 2017" as rationale for 91 seats

- **Test.** StatsCan T17-10-0009 (quarterly population). 2017 pop ~4,280,000. 2024 estimate ~4,960,000. Growth ≈ 16% (not 20%) but approaches 20% when extending to 2025 and comparing to the 2017 *boundaries-commission baseline*.
- **Verdict.** **SUPPORTS** directionally. The exact "20%" figure is a rounding-up; the underlying growth is real.

---

## Indigenous-consultation rationales

### R7. Calgary-West-Tsuut'ina

- **Test.** Tsuut'ina Nation is a real First Nation adjacent to west Calgary with established economic integration (Taza, Grey Eagle, Costco Tsuut'ina Gateway).
- **Verdict.** **SUPPORTS.**

### R12. Rocky Mountain House-Banff Park — "dividing regional Indian reserves from the nearest economic hub"

- **Test.** Indian reserves in the RMH-Banff-Sundre region: Stoney Nakoda Nations (Chiniki, Bearspaw, Wesley) — reserves at Morley (Bighorn, Kananaskis), which are in the Bow Valley, not in Clearwater County. Sunchild First Nation and O'Chiese First Nation are in Clearwater County northwest of Rocky Mountain House — these are the reserves the minority text appears to reference. Rocky Mountain House is indeed the nearest service hub for Sunchild and O'Chiese.
- **Verdict.** **SUPPORTS** for Sunchild/O'Chiese → RMH hub linkage. But the Banff National Park extension (the contested part) does *not* serve Indigenous community hubs — Morley-area Stoney Nakoda are in the Bow Valley and the majority map pairs them with Canmore-Banff, which is a defensible alternative. The Indigenous-consultation rationale supports keeping RMH paired with Sunchild/O'Chiese; it does NOT force the Banff NP extension.

### R15/R16. Central Peace-Notley, Lesser Slave Lake

- **Test.** Both are shared with majority; Indigenous population in Lesser Slave Lake CSDs includes Kapawe'no, Sucker Creek, Swan River, Driftpile First Nations.
- **Verdict.** **SUPPORTS** (both maps).

---

## Historical-continuity rationales

### R12. Banff National Park — "historical precedent"

- **Test.** Checked 2019 enacted map (Bill 33 `EDS_ENACTED_BILL33_15DEC2017.shp`) and predecessor maps. The 2017 Rimbey-Rocky Mountain House-Sundre district does contain a portion of Banff National Park in its southwestern corner; the 2012 electoral division also did. So **historical precedent exists** at the surface level.
- **Verdict.** **SUPPORTS** the bare claim of precedent. But the minority's extension is *more extensive* than the historical one — the 2026 minority proposal extends to the BC border through a long uninhabited NP corridor, whereas the 2017 precedent is a smaller NP adjunct. The precedent exists; the degree of extension is novel.

### R13. Olds-Three Hills-Didsbury — "keep established communities along Hwy 2 corridor"

- **Test.** The existing 2019 Olds-Didsbury-Three Hills district (2017 Bill 33) already contains Olds, Didsbury, Carstairs, Three Hills, Crossfield. The minority "extends" the boundary south into Rocky View County.
- **Verdict.** **PARTIALLY SUPPORTS** the continuity claim (the core Hwy 2 towns stay together). But the southern extension into Rocky View that pulls in North Airdrie territory is a new element; that element is CLOSED-FAIL on population math (Test 1).

---

## Economic-zone rationales

### R10. Highway 11 corridor (Red Deer-Lacombe)

- **Test.** Highway 11 connects Red Deer, Sylvan Lake, Eckville, Rocky Mountain House, Nordegg, and Saskatchewan Crossing. It is a real designated economic corridor.
- **Verdict.** **SUPPORTS.** Blackfalds inclusion is on Hwy 2 not Hwy 11 — noted inconsistency but overall corridor logic holds.

### R12. RMH "north-south economic corridors along Highway 22"

- **Test.** Highway 22 (Cowboy Trail) runs north-south from Crowsnest Pass through Turner Valley, Black Diamond, Cochrane, Sundre, Rocky Mountain House. It is a real Alberta tourism-designated corridor.
- **Verdict.** **SUPPORTS** at corridor level.

### R8/R10/hybrid doctrine — "regional economies" framing

- **Test.** Alberta Regional Economic Development Alliances (REDAs) divide Alberta into 7 zones. The Central Alberta REDA covers Red Deer, Innisfail, Blackfalds, Lacombe, Sylvan Lake — all four minority Red Deer hybrid districts fall within one REDA. The Calgary Regional Partnership covers Calgary, Airdrie, Cochrane, Chestermere, Okotoks, Rocky View, High River — all the minority Calgary-area hybrids fall within one regional partnership.
- **Verdict.** **SUPPORTS** at the zone level. Districts within a shared REDA/regional-partnership zone do have a legitimate economic-zone rationale for grouping. This does not, however, force *any specific configuration* within the zone — the minority could draw cleaner lines and still respect REDA boundaries.

---

## Political-framing rationales

### R19/R20/R21/R22/R23

- **Test.** `findings/submission_search_findings.md` + `findings/claim_significance_analysis.md` already assess public backing. Summary: three of seven contested minority configurations (RMH-Banff, ODH, Chestermere) materially have public support; one (Red Deer hybrids) is split; three (Airdrie 4-way, Nolan Hill-Cochrane, St. Albert minority alt) do not.
- **Verdict.** **ALREADY-TESTED.** Smith's/Lunty's "effective representation for growing Alberta" frames are not per-district claims; they are generic. The specific minority configurations they implicitly defend have uneven public backing.

---

## Procedural rationales (April 16 motion)

Motion terms (no public hearings; 91-seat ceiling; UCP-majority committee; November 2 deadline; advisory panel escape clauses).

- **Test.** Elections Alberta's public comment, reported in news, describes the timeline as "very challenging" because boundary changes typically require 18 months' lead time before a general election (next: fall 2027). The 91-seat addendum from Chair Miller exists in the majority report as a conditional suggestion, not as a recommendation. The motion takes Miller's conditional up as an affirmative government position.
- **Verdict.** **INCONCLUSIVE at the legal level** (courts, not audits, adjudicate). **PARTIALLY CONTRADICTS** the "following Miller's own suggestion" framing — Miller's 91-seat suggestion was conditional on the legislature *rejecting* the 89-seat majority map, not on also dismissing the commission and installing an MLA committee.

---

## Verdict summary table

| Rationale ID | Type | Verdict | Already-tested? |
|---|---|---|---|
| R1 Nolan Hill-Cochrane commute | Commuter-tie | PARTIALLY SUPPORTS | New |
| R2 Peigan-Chestermere | Commuter + shared-institution | INCONCLUSIVE / LEANS CONTRADICTS | Pop math CLOSED-FAIL |
| R3 Calgary-Airdrie | Growth + commuter | SUPPORTS | Pop math CLOSED-FAIL |
| R4 Foothills-Airdrie W | Commuter | SUPPORTS general | Pop math CLOSED-FAIL |
| R5 Bow-Springbank | Commuter + schools | INCONCLUSIVE | New |
| R6 NW-Bearspaw | Commuter + economic | SUPPORTS | New |
| R7 West-Tsuut'ina | Indigenous + commuter | SUPPORTS | New |
| R8 Red Deer-Blackfalds | Economic + Joffre | SUPPORTS (narrow) | Pop math CLOSED-FAIL |
| R9 Red Deer-Innisfail | Commuter + hub | SUPPORTS general | Pop math CLOSED-FAIL |
| R10 Red Deer-Lacombe Hwy 11 | Economic-zone | PARTIALLY SUPPORTS | Pop math CLOSED-FAIL |
| R11 Red Deer-Sylvan Lake schools | Commuter + schools | INCONCLUSIVE / LEANS CONTRADICTS | Pop math CLOSED-FAIL |
| R12 RMH-Banff | Area + Indigenous + historical + economic | Area = CLOSED-FAIL; Indigenous = SUPPORTS (Sunchild/O'Chiese); Banff ext = PARTIALLY SUPPORTS historical | Area CLOSED-FAIL |
| R13 ODH Hwy-2 continuity | Community + historical | PARTIALLY SUPPORTS; Airdrie slice CLOSED-FAIL | Pop math CLOSED-FAIL (Test 1) |
| R14 Airdrie East | Procedural | n/a — no positive claim |  |
| R15 Central Peace-Notley | Indigenous + area | SUPPORTS | Shared with majority |
| R16 Lesser Slave Lake | Indigenous + area | SUPPORTS | Shared with majority |
| R17 Hybrid doctrine | Rural-preservation | INCONCLUSIVE (philosophical) | New |
| R18 Growth uncertainty | Growth | Self-hedged (minority concedes uncertainty) | New |
| R19 Smith "lose rural" | Procedural + rural | PARTIALLY SUPPORTS (ambiguous) | New |
| R20 Smith AI quote | Political-framing | n/a |  |
| R21 Nixon population growth | Growth | SUPPORTS at 16–20% level | New |
| R22 Lunty effective representation | Political-framing | n/a |  |
| R23 Lunty NDP framing | Political-framing | n/a |  |
| R24 Motion terms | Procedural | INCONCLUSIVE (legal question) | New |
| R25 91 seats = 20% growth | Growth | SUPPORTS directionally (16–20% actual) | New |

**Verdict breakdown (substantive rationales, excluding pure political-framing and procedural):**

- SUPPORTS: 7 (R3, R6, R7, R15, R16; R8 narrow; R21 growth)
- PARTIALLY SUPPORTS: 5 (R1, R4, R10, R12 historical/Indigenous, R13, R19)
- INCONCLUSIVE: 3 (R5, R11, R24)
- CONTRADICTS / LEANS CONTRADICTS: 2 (R2 specific Chestermere-Forest-Lawn; R5 Bow-Springbank schools; R11 Sylvan Lake schools)
- CLOSED-FAIL (population/area math, already refuted): 5 (Tests 1–5)

---

## Phase 3 — Proposed insertions into reports

Do NOT apply here — flagged for parent session. Each insertion lists target section and both grade-9 and academic draft.

### Insertion A — Shared-schools rationale fails for two hybrid claims

**Target — public report:** section "Were the minority's configurations forced by population math?" (after the five-test table)

**Draft (grade 9):** "Two more minority rationales were checked against simple public data. The minority defends Calgary-Bow-Springbank partly on the idea that Springbank and west Calgary share schools. They do not — Springbank is in Rocky View Schools, west Calgary is in the Calgary Board of Education. The same problem shows up for Red Deer-Sylvan Lake. Sylvan Lake is in Chinook's Edge School Division; Red Deer city is in Red Deer Public. The 'shared schools' argument does not hold."

**Target — academic report:** §D2 Community-of-Interest Audit (new sub-subsection)

**Draft (academic):** "Two minority shared-institution claims fail cross-reference against Alberta Education school-division boundaries. The Calgary-Bow-Springbank rationale (Appendix E, p. 322) invokes 'educational institutions' as a community-of-interest tie between Springbank and west Calgary; Springbank falls within Rocky View School Division No. 41, while the relevant west-Calgary catchment falls within the Calgary Board of Education. Similarly, the Red Deer-Sylvan Lake rationale (Appendix E, p. 351) cites schooling as an urban-rural tie; Sylvan Lake falls within Chinook's Edge School Division No. 73, while the City of Red Deer is served by Red Deer Public Schools and Red Deer Catholic Regional Schools (Alberta Education boundary map, 2024). The 'shared schools' rationale is unsupported in both cases."

### Insertion B — Cochrane commute specifically measured

**Target — public report:** existing Calgary-Nolan Hill-Cochrane bullet

**Draft:** "The minority defends Calgary-Nolan Hill-Cochrane partly on the idea that Cochrane residents 'move fluidly' between Cochrane and Calgary. StatsCan's 2021 journey-to-work data for Cochrane shows 49 percent of Cochrane commuters work inside Cochrane, 36 percent work somewhere in Calgary, and the rest scatter to Canmore, Rocky View, and Airdrie. There is a real Cochrane-Calgary commute — but it is a minority of workers, and the data does not single out Nolan Hill as the destination. The minority's own narrative flattens 'Cochrane commutes somewhere in Calgary' into 'Cochrane belongs in the Nolan Hill district.'"

**Target — academic report:** §C3 spatial-anomaly discussion of Calgary-Nolan Hill-Cochrane

**Draft:** "StatsCan table 98-10-0459 (2021 Census journey-to-work) disaggregates Cochrane CSD commute destinations. Of 8,550 Cochrane workers with an Alberta place of work, 4,205 (49.2%) work within Cochrane, 3,065 (35.8%) commute to Calgary CY, 345 (4.0%) to Rocky View County, 185 (2.2%) to Canmore, 135 (1.6%) to Wood Buffalo, and 130 (1.5%) to Airdrie. The Calgary flow is a genuine commuter-tie signal at the city-to-city level but is silent on the Nolan Hill sub-destination; the minority's pairing of Cochrane specifically with the Nolan Hill/Sage Hill ward is not further supported by the place-of-work data."

### Insertion C — Airdrie growth projection is real but does not force four-way split

**Target — public report:** Airdrie split four ways row in the contested-configurations table

**Draft (addendum, parenthesized):** "(Airdrie's growth is real — City projections put the 2033 population at about 128,000, adding 50,000 from 2024. That supports the minority's general case for more Airdrie-adjacent seats, but not the specific four-way split, which the population arithmetic also does not force.)"

**Target — academic report:** §A footnote on Airdrie population

**Draft:** "The City of Airdrie 2024 Growth Report projects 128,470 residents by 2033 (base 2024, +50,000), consistent with recent 4.9% annual growth (Discover Airdrie, 2024, citing Airdrie Community Services). This projection supports the minority's growth-projection rationale for new Airdrie-adjacent seats in a general sense but is orthogonal to the specific four-way split, which is tested and fails in `justification_tests_findings.md` Test 3."

### Insertion D — Piikani geographic mismatch (Peigan name)

**Target — academic report:** §D2 name-convention note

**Draft:** "The 'Peigan' in Calgary-Peigan-Chestermere is inherited from the existing Calgary-Peigan electoral division, which was named for Peigan Trail SE, a road forming part of the district's northern boundary (Wikipedia, 'Calgary-Peigan'). The Piikani Nation itself is located approximately 200 km south of Calgary near Pincher Creek and Fort Macleod (Piikani 147 Reserve). The district name does not denote an Indigenous community-of-interest tie to Calgary; the minority's retention of the name in the hybrid extension preserves a road-based etymology. This is a naming note, not a finding of fault."

### Insertion E — Miller's 91-seat addendum vs the motion

**Target — public report:** section "The 91-seat proposal, so far" — adjust phrasing

**Draft (replacement suggestion for existing sentence on Miller's addendum):** "Miller's 91-seat addendum was a conditional: if the legislature rejected the 89-seat majority map, he suggested going to 91 seats using the majority as a starting point, adding two rural seats. The April 16 motion takes the 91-seat number but does not take the majority map as starting point. Instead, it creates an MLA committee and sends the drafting work back from scratch. That is a different decision than Miller proposed."

**Target — academic report:** §5.2 April 16 government action

**Draft:** "The April 16 motion's 91-seat framing echoes Chair Miller's conditional 91-seat addendum. However, Miller's conditional presupposed the majority-recommended map as a starting point with two additional rural seats added. The motion declines the majority map entirely and commits the redraw to a Special Select Committee with UCP majority (three UCP, two NDP) chaired by MLA Brandon Lunty, advised by a panel whose composition has not yet been disclosed (CBC Edmonton, April 16, 2026). The motion also eliminates public hearings on any new map (Daveberta Substack, April 17, 2026; Calgary Journal, April 21, 2026), a procedural departure from prior commissions. The 91-seat number and the committee structure are separable choices; the motion adopts both."

### Insertion F — Shared REDA zone supports regional-economy framing

**Target — academic report:** §3 hybrid discussion (new supporting note)

**Draft:** "Alberta's Regional Economic Development Alliance geography provides partial support for the minority's general hybrid doctrine. The Central Alberta REDA covers Red Deer, Innisfail, Blackfalds, Lacombe, and Sylvan Lake — encompassing all four of the minority's Red Deer hybrid districts. The Calgary Regional Partnership covers Calgary, Airdrie, Cochrane, Chestermere, Okotoks, Rocky View, and High River — encompassing the minority's Calgary hybrids. This is a real, documented regional-economy organisation. It does not, however, dictate specific intra-zone boundary configurations; any map that groups districts within these zones satisfies the zone-coherence criterion."

---

## Data sources accessed vs attempted-but-blocked

**Accessed:**

- Appendix E text extraction (`.temp/appendix_e_text.txt`, 2,752 lines)
- Cochrane journey-to-work (StatsCan 98-10-0459, `.temp/cochrane_ab.csv`, 5,162 rows)
- 2021 CSD population table (`data/alberta_2021_csd_populations.csv`)
- 2019 enacted shapefile for historical-continuity check (`data/alberta_2019_eds/`)
- Web: City of Airdrie 2024 growth report (via DiscoverAirdrie.com reporting), Alberta Open Data population projection 2025–2051, CBC Edmonton April 16 coverage, Calgary Journal April 21 coverage, Daveberta Substack analysis, parliamentum.org blog
- Web: Wikipedia entries for Piikani Nation, Calgary-Peigan district, Alberta school divisions

**Attempted-but-blocked:**

- Alberta Hansard April 16 daily transcript direct fetch (HTTP 403 from WebFetch client)
- CBC full-article WebFetch on several URLs (403)
- StatsCan 98-10-0438 full download for Airdrie and Chestermere origin-CSDs (portal returns profile pages; direct table not obtained in this session)
- Alberta Education interactive boundary map (validated via search result only, not downloaded)

**Pending (flagged for future):**

- Track G Cochrane-specific deeper analysis — no output file present as of this session; treated as pending per instructions.
- Hansard primary transcript pull for verbatim Smith/Nixon/Lunty quotes (news reports used as secondary).
- Origin-CSD commute for Airdrie, Chestermere, Sylvan Lake, Bearspaw, Tsuut'ina — would strengthen the R3/R4/R6/R7/R11 tests from CMA-level to micro-level.
