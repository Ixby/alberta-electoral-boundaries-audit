# v0.1 School-Division Coherence of the Minority 2026 Hybrid Configurations

## Purpose

Track I (`v0_1_minority_rationales_validation.md`) tested the two minority rationales that *explicitly* invoked "shared schools" (R5 Calgary-Bow-Springbank and R11 Red Deer-Sylvan Lake) and found both contradicted by Alberta school-division geography. This document widens the lens: for *every* minority hybrid, does the district territory fall inside a single Alberta school division (or a coherent pair that shares a catchment), or does it cross division boundaries without saying so?

If the non-explicit hybrids also cross school-division lines, the two contradicted "shared schools" claims are the visible tip of a systematic mismatch between the minority's community-of-interest story and Alberta's on-the-ground school geography. If the non-explicit hybrids mostly stay inside one division (or one public/separate pair in the same municipality), the two explicit failures are isolated rhetorical slips.

## Method

**Source of truth.** Alberta Education publishes the authoritative school-authority boundary map at `https://www.alberta.ca/alberta-school-division-maps` and the school-authority directory at `https://www.alberta.ca/school-authority-directory`. These give the canonical catchment for each public, Catholic, Francophone, and charter division. Where the interactive map was not re-pulled in this session, division coverage was verified against each division's own public description, collated via web search.

**Scope.** Every minority hybrid (any ED with `-hybrid` or `-merged` in the `region_type` column of `data/v0_1_minority_2026_populations.csv`). This yields 21 EDs across Calgary, Edmonton, Red Deer, Lethbridge, and St. Albert regions.

**Classification keys.**
- **School-coherent:** the ED's territory sits entirely inside a single public school division (and, where relevant, a single Catholic division). The "single pair" case — public + Catholic in the same city — counts as coherent because those are parallel jurisdictions covering identical territory.
- **School-incoherent (mild):** the ED spans two adjacent divisions in a geographically plausible way: for example, a city + adjacent rural-county slice where residents on both sides commute across the line. The spanning is not hidden — it's visible on the map — and the commuter/catchment rationale is at least arguable.
- **School-incoherent (severe):** the ED spans two divisions whose catchments do not share students, with no plausible shared-school tie. The spanning either contradicts an explicit minority "shared schools" claim (R5, R11) or silently fragments a division that should not be fragmented.
- **Neutral:** the minority does not invoke shared schools for this ED; whether or not it crosses a division boundary is informational. We still flag the crossing so the pattern can be read across the set.

**What we are not doing.** We are not re-running the population math (closed — see `v0_1_justification_tests_findings.md`). We are not re-running the commute tests (done for Cochrane — see `v0_1_cochrane_journey_to_work.md`). We are testing a narrow claim: does the school-division geography *permit* the minority's community-of-interest framing?

## Alberta school-division coverage (verified)

| Division | Area covered | Catholic counterpart |
|---|---|---|
| Calgary Board of Education (CBE) | City of Calgary only | Calgary Catholic School District (CCSD), same footprint |
| Rocky View Schools | Rocky View County, Airdrie, Chestermere, Cochrane (public) | Christ the Redeemer Catholic (Rocky View + Okotoks + High River rural) |
| Foothills School Division | Foothills County, Okotoks, High River (public) | Christ the Redeemer Catholic |
| Chinook's Edge School Division No. 73 | Central Alberta rural: Sylvan Lake, Innisfail, Didsbury, Carstairs, Olds, Three Hills, south Red Deer County | Red Deer Catholic Regional (Innisfail included) |
| Wolf Creek Public Schools No. 72 | Lacombe County, Ponoka County: Blackfalds, Lacombe, Ponoka, Alix, Bentley, Clive, Eckville, Rimbey | Red Deer Catholic Regional partial; St. Thomas Aquinas RCSSD partial |
| Red Deer Public Schools | City of Red Deer only (public) | Red Deer Catholic Regional (City + partial county) |
| Wild Rose School Division | Rocky Mountain House, Drayton Valley | Red Deer Catholic Regional partial |
| Edmonton Public Schools | City of Edmonton only | Edmonton Catholic Schools (city only) |
| Elk Island Public Schools (EIPS) | Sherwood Park, Strathcona County, Fort Saskatchewan, Lamont County, Vegreville | Elk Island Catholic Schools (same area) |
| Parkland School Division | Parkland County, Stony Plain, Spruce Grove | Evergreen Catholic Separate (same area) |
| Black Gold School Division No. 18 | Leduc County: Leduc, Beaumont, Devon, Calmar, Thorsby, Warburg | St. Thomas Aquinas RCSSD partial |
| Sturgeon Public Schools | Sturgeon County, Morinville, Legal, Gibbons (but NOT City of St. Albert) | Greater St. Albert Roman Catholic |
| St. Albert Public Schools | City of St. Albert only | Greater St. Albert Roman Catholic (City of St. Albert + Morinville + Legal) |
| Palliser School Division No. 26 | Lethbridge County rural (south of city), Coaldale surroundings, Vulcan County north, Picture Butte area | Holy Spirit Catholic (Lethbridge region + Coaldale) |
| Lethbridge School Division | City of Lethbridge only (public) | Holy Spirit Roman Catholic (Lethbridge City + regional rural) |
| Horizon School Division No. 67 | Taber, Vauxhall, Warner, Milk River, Lomond (south-central between Lethbridge and Med Hat) | Holy Spirit RCSSD partial east |
| Westwind School Division No. 74 | Cardston, Magrath, Raymond, Stirling, Glenwood, Hill Spring | Holy Spirit RCSSD partial |
| Livingstone Range School Division | Crowsnest Pass, Pincher Creek, Fort Macleod, Claresholm, Nanton | Holy Spirit RCSSD partial |

Sources: Alberta Education boundary map portal (`alberta.ca/alberta-school-division-maps`); division-by-division web verification conducted this session for Rocky View, Chinook's Edge, Wolf Creek, Palliser, Horizon, Parkland, Black Gold, Sturgeon, Westwind, Elk Island. All coverage claims above reflect publicly documented division self-descriptions.

**Critical structural facts for this audit.**
1. **Calgary Board of Education stops at the City of Calgary boundary.** Any hybrid that extends beyond the city limits crosses from CBE into Rocky View Schools, Foothills School Division, or onto Tsuut'ina land.
2. **Edmonton Public Schools stops at the City of Edmonton boundary.** Any hybrid crossing outside the city moves to Parkland, Black Gold, Sturgeon, St. Albert Public, or EIPS.
3. **Red Deer Public Schools stops at the City of Red Deer boundary.** The surrounding rural is covered by Chinook's Edge (south/west) or Wolf Creek (north/east), with Blackfalds specifically in Wolf Creek and Sylvan Lake/Innisfail in Chinook's Edge.
4. **Lethbridge School Division stops at the City of Lethbridge boundary.** Rural south = Palliser; south-east = Horizon; far south = Westwind; south-west = Livingstone Range.
5. **St. Albert Public Schools stops at the City of St. Albert boundary.** Surrounding Sturgeon County = Sturgeon Public.

These five city-only/regional-rural splits produce a sharp catchment break at every city limit. A hybrid that pairs a city neighbourhood with an adjacent rural community is, definitionally, a cross-division pairing — regardless of whether the minority invokes "shared schools" for that pairing.

## Per-hybrid school-division coherence check

### Calgary-area hybrids (7)

**Calgary-Bow-Springbank** (55,560; R5, explicit shared-schools claim)
- **Divisions covered:** CBE (west Calgary: Bowness, Montgomery, etc.) + Rocky View Schools (Springbank) + CCSD (Catholic parallel for Calgary).
- **Spanning:** yes, CBE ↔ Rocky View Schools.
- **Assessment:** minority explicitly invokes "educational institutions" as a community-of-interest tie (Appendix E, p. 322). CBE and Rocky View Schools run separate trustee elections, separate budgets, separate catchments; Springbank Middle School and Springbank High School draw from Rocky View catchment only.
- **Classification: School-incoherent (severe).**

**Calgary-Foothills-Airdrie West** (58,436)
- **Divisions covered:** CBE (NW Calgary: Foothills neighbourhood area) + Rocky View Schools (west Airdrie).
- **Spanning:** yes, CBE ↔ Rocky View Schools.
- **Assessment:** no explicit shared-schools claim from the minority, but the hybrid pairs a Calgary neighbourhood with Airdrie territory across the municipal boundary. The two student populations do not overlap: CBE schools serve Calgary kids, Rocky View Schools serve Airdrie kids.
- **Classification: School-incoherent (mild)** — the spanning is not hidden (the ED name announces it), and the Calgary–Airdrie commute corridor along Hwy 2 is real. Marked "mild" rather than "severe" because no shared-schools rhetoric is invoked to justify it.

**Calgary-Nolan Hill-Cochrane** (56,282)
- **Divisions covered:** CBE (Nolan Hill, Sage Hill) + Rocky View Schools (Cochrane).
- **Spanning:** yes, CBE ↔ Rocky View Schools.
- **Assessment:** the ED name itself declares the cross-jurisdictional pairing. The minority's rationale (Appendix E, p. 331) invokes "education" among several shared-interest factors but does not go as far as R5's "educational institutions" framing. Cochrane kids attend Rocky View Schools; Nolan Hill kids attend CBE. Cochrane's St. Timothy High School and Bow Valley High School are Rocky View schools, unavailable to Nolan Hill residents. This is the canonical "lasso" configuration flagged in §C3.
- **Classification: School-incoherent (severe).** The minority invokes education-adjacent language in the rationale, and the district geography itself makes the spanning unavoidable.

**Calgary-North West-Bearspaw** (57,246)
- **Divisions covered:** CBE (NW Calgary: Rocky Ridge, Royal Oak area) + Rocky View Schools (Bearspaw).
- **Spanning:** yes, CBE ↔ Rocky View Schools.
- **Assessment:** no explicit shared-schools claim. Rationale (Appendix E, p. 330) cites "commercial corridors and commuter patterns" — narrow economic framing, not educational.
- **Classification: Neutral** — crosses divisions but no school-based rationale is invoked, and Bearspaw is geographically contiguous with NW Calgary. The commercial/commute claim is on solid ground (see Track I: SUPPORTS).

**Calgary-Peigan-Chestermere** (52,639)
- **Divisions covered:** CBE (east Calgary: Forest Lawn, Erin Woods) + Rocky View Schools (south Chestermere).
- **Spanning:** yes, CBE ↔ Rocky View Schools.
- **Assessment:** the rationale (Appendix E, p. 332) does not explicitly claim shared schools, but the minority's "growing social, economic, and transportation connections" framing was flagged in Track I as leaning contradicted on institution-sharing (transit, schools). Chestermere High School serves Rocky View students only; Forest Lawn High School serves CBE students only.
- **Classification: School-incoherent (mild)** — the minority did not name schools as the tie, so it's not a "severe" contradiction; but the hybrid pairs two populations that never share a classroom.

**Calgary-West-Tsuut'ina** (57,827)
- **Divisions covered:** CBE (west Calgary) + Tsuut'ina Nation schools (federally-governed, band-operated; Tsuut'ina operates its own education system under the Tsuut'ina Nation Education Department, separate from Alberta's provincial divisions).
- **Spanning:** yes, CBE ↔ Tsuut'ina Nation education system.
- **Assessment:** Tsuut'ina Nation education is under First Nations jurisdiction, not Alberta Education's division framework. This is a *categorically different* kind of spanning from a CBE/Rocky View split — it reflects federal-provincial jurisdictional reality, not Commission gerrymandering. Track I's verdict on this hybrid was SUPPORTS (economic integration via Taza, Indigenous-consultation coherence).
- **Classification: Neutral** — the spanning is a statutory fact of Indigenous self-governance, not a Commission-drawn contradiction. No rhetorical "shared schools" claim made.

**Calgary-De Winton** (47,732)
- **Divisions covered:** CBE (south Calgary) + Foothills School Division (De Winton, part of Foothills County).
- **Spanning:** yes, CBE ↔ Foothills School Division.
- **Assessment:** hybrid is listed in the populations CSV but not explicitly defended in the R1–R18 inventory (it does not appear in the 18 minority district-specific rationales). De Winton is a hamlet south of Calgary serviced by Foothills School Division.
- **Classification: Neutral** — spans two divisions, no shared-schools claim to contradict.

### Edmonton-area hybrids (4)

**Edmonton-Beaumont** (55,802)
- **Divisions covered:** Edmonton Public Schools (south Edmonton) + Black Gold School Division (Beaumont).
- **Spanning:** yes, EPS ↔ Black Gold.
- **Assessment:** no minority rationale in the R1–R18 inventory names this hybrid (the inventory focuses on Calgary and Red Deer hybrids). The geographic spanning is unavoidable: Beaumont is in Leduc County, EPS covers only City of Edmonton.
- **Classification: School-incoherent (mild)** — no explicit claim to contradict, but the two populations do not share a school system.

**Edmonton-Enoch-Devon** (55,043)
- **Divisions covered:** Edmonton Public Schools (west Edmonton) + Black Gold School Division (Devon) + Enoch Cree Nation schools (band-operated, federally governed).
- **Spanning:** yes, three-way: EPS ↔ Black Gold ↔ Enoch Nation.
- **Assessment:** §C4 already flagged this as combining a reserve with a distant municipality (Devon is south of the North Saskatchewan River, Enoch is north-west of Edmonton). The majority map splits these, pairing Enoch only with adjacent Edmonton territory.
- **Classification: School-incoherent (mild)** — no explicit shared-schools claim; the Indigenous-education spanning (Enoch Nation) is a jurisdictional fact, but the Edmonton–Devon spanning is a Commission choice.

**Edmonton-Glenora-Riverview** (59,708)
- **Divisions covered:** Edmonton Public Schools only (both Glenora and Riverview are Edmonton neighbourhoods).
- **Spanning:** no — both sides inside City of Edmonton, both inside EPS (public) and Edmonton Catholic (Catholic).
- **Assessment:** this is a `Edmonton-merged` rather than a cross-municipality hybrid. Merger of two Edmonton neighbourhoods.
- **Classification: School-coherent.**

**Edmonton-Spruce Grove** (59,524)
- **Divisions covered:** Edmonton Public Schools (west Edmonton) + Parkland School Division (Spruce Grove).
- **Spanning:** yes, EPS ↔ Parkland.
- **Assessment:** Spruce Grove is a City of 38,000+ in Parkland County. Spruce Grove kids attend Parkland School Division schools; west Edmonton kids attend EPS.
- **Classification: School-incoherent (mild)** — no explicit shared-schools claim, but a cross-division pairing of two adjacent populations that never share a classroom.

### Red Deer–area hybrids (4)

**Red Deer-Blackfalds** (52,827)
- **Divisions covered:** Red Deer Public Schools (City portion) + Wolf Creek Public Schools (Blackfalds, plus Alix, Clive if included).
- **Spanning:** yes, RDPS ↔ Wolf Creek.
- **Assessment:** Blackfalds (pop ~11,000) is in Lacombe County, not Red Deer County. Wolf Creek Public serves Blackfalds directly (Iron Ridge Secondary Campus, etc.). Red Deer Public serves only the City of Red Deer. No shared catchment, no shared trustees. The rationale (Appendix E, p. 349) invokes "agricultural services hub" and Joffre plant — not schools specifically, so no contradiction of a stated claim.
- **Classification: School-incoherent (mild)** — cross-division pairing; no shared-schools rhetoric to contradict directly.

**Red Deer-Innisfail** (52,961)
- **Divisions covered:** Red Deer Public Schools (City portion) + Chinook's Edge School Division (Innisfail, Penhold, Delburne, Elnora).
- **Spanning:** yes, RDPS ↔ Chinook's Edge.
- **Assessment:** Chinook's Edge is headquartered *in* Innisfail and serves Innisfail plus surrounding rural Red Deer County south. Red Deer city kids attend Red Deer Public; Innisfail kids attend Chinook's Edge. The rationale (p. 350) invokes "provincial services" hub — AHS Red Deer Zone etc. — not schools.
- **Classification: School-incoherent (mild).**

**Red Deer-Lacombe** (56,180)
- **Divisions covered:** Red Deer Public Schools (City portion) + Wolf Creek Public Schools (Lacombe, Bentley, Eckville) + possibly Chinook's Edge (if the Hwy 11 corridor extends to Sylvan Lake — but Sylvan Lake is in the separate R11 hybrid).
- **Spanning:** yes, RDPS ↔ Wolf Creek.
- **Assessment:** rationale invokes "Highway 11 economic corridor" — a zone/corridor framing, not a school claim. Lacombe is Wolf Creek; Red Deer City is RDPS; different student populations.
- **Classification: School-incoherent (mild).**

**Red Deer-Sylvan Lake** (52,454; R11, explicit shared-schools claim)
- **Divisions covered:** Red Deer Public Schools (City portion) + Chinook's Edge School Division (Sylvan Lake).
- **Spanning:** yes, RDPS ↔ Chinook's Edge.
- **Assessment:** Track I already marked this CONTRADICTED. The rationale (Appendix E, p. 351) invokes "urban communities … where they work, go to school" — the "go to school" claim is the load-bearing language. Sylvan Lake kids attend Chinook's Edge (H.J. Cody Secondary, for example); Red Deer city kids attend Red Deer Public. The two populations share no schools.
- **Classification: School-incoherent (severe).**

### Lethbridge-area hybrids (4)

**Lethbridge-Cardston** (51,831)
- **Divisions covered:** Lethbridge School Division (City portion) + Westwind School Division (Cardston, Magrath) + possibly Holy Spirit Catholic (as Catholic overlap).
- **Spanning:** yes, Lethbridge SD ↔ Westwind.
- **Assessment:** Cardston is ~75 km south of Lethbridge, in its own school division serving Cardston, Magrath, Raymond, Stirling. No shared catchment with Lethbridge city schools. No explicit minority rationale in the R1–R18 inventory names this district (Lethbridge hybrids are not in the Calgary/Red Deer detailed defences).
- **Classification: School-incoherent (mild).**

**Lethbridge-Fort MacLeod-Crowsnest Pass** (54,564)
- **Divisions covered:** Lethbridge School Division (City portion) + Livingstone Range School Division (Fort Macleod, Crowsnest Pass, Pincher Creek area).
- **Spanning:** yes, Lethbridge SD ↔ Livingstone Range.
- **Assessment:** Fort Macleod is ~50 km west of Lethbridge, Crowsnest Pass is ~125 km west. Livingstone Range covers both, plus Claresholm and Nanton. No shared catchment with Lethbridge city.
- **Classification: School-incoherent (mild).**

**Lethbridge-Little Bow** (56,212)
- **Divisions covered:** Lethbridge School Division (City portion) + Palliser School Division (Picture Butte, Vulcan County north, Milo) + possibly Horizon (Lomond area).
- **Spanning:** yes, Lethbridge SD ↔ Palliser (and potentially Horizon).
- **Assessment:** Little Bow is a rural zone to the north of Lethbridge, straddling Palliser and Horizon. Cross-division pairing; no explicit school rationale.
- **Classification: School-incoherent (mild).**

**Lethbridge-Taber-Warner** (60,906)
- **Divisions covered:** Lethbridge School Division (City portion) + Horizon School Division (Taber, Vauxhall, Warner, Milk River).
- **Spanning:** yes, Lethbridge SD ↔ Horizon.
- **Assessment:** Taber is ~50 km east of Lethbridge in Horizon SD. Cross-division pairing.
- **Classification: School-incoherent (mild).**

### St. Albert–area hybrid (1)

**St. Albert-Sturgeon** (52,334)
- **Divisions covered:** St. Albert Public Schools (City of St. Albert) + Sturgeon Public Schools (Morinville, Legal, Gibbons, Sturgeon County).
- **Spanning:** yes, St. Albert Public ↔ Sturgeon Public.
- **Assessment:** St. Albert Public serves the City of St. Albert only; the 2011 Establishment Act explicitly split Morinville/Legal/Gibbons off into Sturgeon Public. Cross-division pairing with no shared catchment. No explicit school rationale in the minority inventory.
- **Classification: School-incoherent (mild).**

## Classification summary

**Hybrid set.** 20 EDs carry a hybrid tag (`-hybrid` or `-merged`) in `data/v0_1_minority_2026_populations.csv`: 8 Calgary-hybrid (including De Winton), 3 Edmonton-hybrid, 1 Edmonton-merged, 4 Red Deer Rest-hybrid, 4 Lethbridge Rest-hybrid, 1 St. Albert Rest-hybrid. One additional ED — **Calgary-Airdrie** — is a cross-municipal hybrid by name and rationale (R3, Appendix E p. 317) but is tagged `Calgary` (not `Calgary-hybrid`) in the CSV. This appears to be a CSV mis-tag. The audit includes Calgary-Airdrie in the inclusive total below. **Flag for parent session's data-hygiene review.**

**Inclusive total: 21 hybrids analysed.**

| Classification | Count | EDs |
|---|---:|---|
| School-coherent | 1 | Edmonton-Glenora-Riverview (intra-Edmonton merger) |
| School-incoherent (severe) | 3 | Calgary-Bow-Springbank (R5 explicit); Red Deer-Sylvan Lake (R11 explicit); Calgary-Nolan Hill-Cochrane (rationale invokes education-adjacent language + lasso geography) |
| School-incoherent (mild) | 14 | Calgary-Airdrie; Calgary-Foothills-Airdrie West; Calgary-Peigan-Chestermere; Edmonton-Beaumont; Edmonton-Enoch-Devon; Edmonton-Spruce Grove; Red Deer-Blackfalds; Red Deer-Innisfail; Red Deer-Lacombe; Lethbridge-Cardston; Lethbridge-Fort MacLeod-Crowsnest Pass; Lethbridge-Little Bow; Lethbridge-Taber-Warner; St. Albert-Sturgeon |
| Neutral | 3 | Calgary-North West-Bearspaw; Calgary-West-Tsuut'ina (Indigenous-jurisdictional spanning); Calgary-De Winton |
| **Total** | **21** | |

### Bottom-line count

**20 of 21 minority hybrids cross at least one Alberta school-division boundary.** Only Edmonton-Glenora-Riverview (a within-Edmonton merger of two city neighbourhoods) is school-coherent.

Of the 20 that span divisions:
- **3 are severe** — the minority makes an explicit or near-explicit shared-schools claim that the division geography contradicts (R5 Bow-Springbank; R11 Sylvan Lake; R1 Nolan Hill-Cochrane).
- **13 are mild** — cross-division pairings without an explicit shared-schools claim; geographically plausible given commute/commercial ties; the spanning is not hidden.
- **3 are neutral** — spanning is either a federal-jurisdictional fact (Tsuut'ina, Enoch via adjacent hybrids) or, for De Winton and Bearspaw, the rationale never invokes institutional sharing at all.

**Is this a systematic pattern?** Yes, in a structural sense: the minority's hybrid doctrine explicitly crosses municipal boundaries, and Alberta's school divisions are built around municipal boundaries, so every cross-municipal hybrid is by construction a cross-division hybrid. **Is the rhetoric damning?** Yes, in a narrower sense: the minority chose to invoke "educational institutions" language in exactly the 2 cases (R5, R11) where the catchment mismatch is most visible, making those two the rhetorical failures Track I already identified.

## Overall verdict

### On the two explicit claims

Both contradicted. Calgary-Bow-Springbank (CBE ↔ Rocky View Schools) and Red Deer-Sylvan Lake (Red Deer Public ↔ Chinook's Edge) are not merely unsupported — they invert the ground truth. Neither pair of populations shares a classroom.

### On the non-explicit hybrids

Of the 19 remaining hybrids (after removing the two explicit-claim cases), **17 cross at least one school-division boundary**. Only 1 is school-coherent (Edmonton-Glenora-Riverview, which is two Edmonton neighbourhoods merged) and 3 are "neutral" (either the spanning is a federal jurisdictional fact — Tsuut'ina Nation, Enoch Nation — or no shared-institution rationale was claimed and the geographic spanning is unavoidable given Alberta's city-only/rural-outer division structure). Of the 17 that do cross, 14 are classified "mild" (cross-division pairing without a shared-schools claim) and 1 is classified "severe" (Calgary-Nolan Hill-Cochrane, where the rationale invokes education-adjacent language and the spanning is the canonical "lasso" flagged in §C3).

**The 2 contradicted explicit claims are not isolated rhetorical slips.** They sit at the extreme end of a systematic pattern: the minority's hybrid design routinely pairs city students with rural-or-other-city students from different school divisions. The explicit "shared schools" rhetoric in R5 and R11 makes the contradiction load-bearing in those two cases; the other 14 "mild" cases do not make the claim, so they cannot be formally contradicted — but they do illustrate that if the minority *had* invoked shared schools across all hybrids, the contradiction would be equally strong.

**Nuance — is this damning?** Part of the pattern is structural, not ideological. Alberta's school-division geography is designed around municipal boundaries: CBE stops at Calgary's limits, Red Deer Public stops at Red Deer's, and so on. Any electoral district that crosses a municipal boundary crosses a school-division boundary by construction. The minority's hybrid doctrine (Appendix E, p. 302) is explicitly about crossing municipal boundaries to pair urban and suburban/rural populations. So the school-division crossings are the mathematical consequence of the doctrine; they are not evidence of gerrymandering on the school dimension.

**What is damning, on a narrower reading:** the minority chose to invoke "educational institutions" and "go to school" language in exactly 2 of its 21 hybrids, and chose them in a way that doesn't withstand five minutes of checking. That is a rhetorical failure, not a structural one — but it is a rhetorical failure on *the most verifiable class of community-of-interest claim* the minority could have made. The 19 cases where they did not invoke schools do not redeem the 2 where they did.

### Implications

- **For §3.6 Chen–Rodden "natural shared geography" discussion.** The Chen–Rodden defence of natural geographic shared-interest is not helped by the school-division data. Rural–urban school divisions in Alberta are designed around municipal boundaries precisely because school catchments are a primary instance of community of interest. The minority's hybrids systematically cross these boundaries. A Chen–Rodden "shared geography" reading would expect electoral districts to align with institutional catchments; the minority map does the opposite.
- **For §5.4 rationales discussion.** The "shared schools" rhetoric in R5 and R11 deserves a sharper treatment than Track I alone provides. Track I showed the two explicit claims fail; this audit shows they fail as the visible surface of a systematic pattern in which the minority's hybrid design does not align with Alberta's school-division geography anywhere it extends beyond city boundaries. The minority chose to deploy school language in exactly the two cases where the geographic miss is visible on the map.

## Proposed insertion for the academic report

**Do not edit. Flagged only.**

**Target — §5.4 Minority Rationales (after the "shared institutions" treatment in Track I):**

**Draft (academic, house voice):**

> A wider school-division coherence check over all 21 of the minority's hybrid configurations confirms the two explicit "shared schools" claims (Calgary-Bow-Springbank; Red Deer-Sylvan Lake) are not isolated. Of the 21 hybrids, 20 span at least two Alberta school divisions; only the within-Edmonton merger (Edmonton-Glenora-Riverview) stays inside a single division. Of the 20 spanning hybrids, 3 make a severe mismatch (the two explicit shared-schools claims plus Calgary-Nolan Hill-Cochrane), 14 are mild (cross-division pairings without a shared-schools claim), and 3 are neutral (Indigenous-jurisdictional spanning for Tsuut'ina and De Winton-style contiguous extensions). The minority's hybrid doctrine (Appendix E, pp. 302–303) explicitly crosses municipal boundaries to pair urban and suburban populations. Because Alberta's provincial school-division geography is built around municipal boundaries (CBE stops at Calgary's limits; Red Deer Public stops at Red Deer's city limits; and so on across Edmonton, Lethbridge, and St. Albert), every cross-municipal hybrid is, by construction, a cross-division hybrid. The school-division crossings are therefore the structural consequence of the doctrine rather than evidence of gerrymandering on the school-catchment dimension. What the school-division check does show is that the minority chose to deploy the rhetorical register of "shared educational institutions" (R5, p. 322) and "go to school" (R11, p. 351) in the specific cases where that language is immediately falsified by Alberta Education's catchment geography. That is a failure of evidentiary discipline on the most verifiable class of community-of-interest claim available to the Commission.

**Proposed headline for the §5.4 insertion:** *"Shared-schools rhetoric in R5 and R11 is the visible surface of a systematic mismatch between the minority's hybrid doctrine and Alberta's school-catchment geography."*

## Data sources and caveats

**Accessed this session.**
- Alberta Education school-authority boundary descriptions (via division-by-division web search): Rocky View Schools, Chinook's Edge School Division No. 73, Wolf Creek Public Schools No. 72, Palliser School Division No. 26, Horizon School Division No. 67, Parkland School Division, Black Gold School Division No. 18, Sturgeon Public Schools, Westwind School Division No. 74, Elk Island Public Schools.
- `data/v0_1_minority_2026_populations.csv` (89 EDs, filtered to 21 hybrids).
- `analysis/methodology/v0_1_minority_rationales_inventory.md` (R1–R25 inventory).
- `analysis/methodology/v0_1_minority_rationales_validation.md` (Track I verdicts).
- `analysis/reports/v0_1_section_C_geographic_coherence.md` (§C4 school-division gap note, now filled).

**Not accessed (and should be, for full precision).**
- The official Alberta.ca interactive boundary map was verified via search result only, not screen-scraped. Individual-school attendance-area maps (for example, for a specific CBE elementary near the Bow-Springbank line) were not fetched — the division-level boundary is what this analysis tests, and that is sufficient for the claim being audited.
- Francophone divisions (Nord-Ouest, Centre-Nord, etc.) overlay these boundaries and operate parallel catchments; they are not material to the urban-rural spanning question addressed here.

**Limitations.**
- Calgary-Airdrie is tagged `Calgary` in the CSV but is structurally a hybrid (crosses municipal boundary). Flagged as a side finding for the parent session — not fixed here.
- Detailed intra-division catchment mismatches (for example, which *specific* CBE high school catchment a Bow-Springbank neighbourhood belongs to) are not audited. The question was division-level coherence, and that is what was tested.
- The minority's exact interior boundary lines are not shapefile-verified in this session; classification is based on the municipal/community unit the ED name and rationale identify.

## What the parent session should do with this

- Read the §5.4 insertion draft; decide whether to apply it alongside Track I's Insertion A (shared-schools specifically) or merge the two.
- Consider whether to add a single-sentence acknowledgement in §3.6 Chen–Rodden that the minority's hybrid doctrine, by design, crosses municipal-aligned institutional catchments — this cuts against the natural-shared-geography defence.
- Decide whether to surface the Calgary-Airdrie CSV tag issue as a separate data-hygiene task.
