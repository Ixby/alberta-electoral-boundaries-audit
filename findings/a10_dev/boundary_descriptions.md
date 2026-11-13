# Written boundary descriptions in the 2026 IAP report

Source: `evidence/legislature/iap_report_2026_hires_text/pNNN.txt` (PDF page NNN; printed page = PDF page - 6). Read-only inventory for use as a third source of each district's shape. Quotes are whole text lines from the text layer, joined with single spaces, nothing reworded. Where a quote ends mid-sentence the text layer itself drops or interleaves the rest (two-column and caption lines are lost in `pdftotext -layout`); check the page image before relying on a truncated edge.

## 0. Findings in brief

- **Metes-and-bounds: exactly one passage** (p085, ED 71 Lethbridge). The word "Commencing" occurs on only two pages; p047 is the unrelated phrase "Prior to the Commission commencing its review". No other division gets a legal description, in the text or in the appendices.
- Everything else is prose: the Section 3 proposals (p013-p096, printed 7-90) describe boundaries in words for about 30 divisions, plus the Minority Opinion (p126-p128, Section IV "How to Restore the Two Rural Electoral Divisions") and one aside on p114.
- **Page offset on the map pages: ED n is on PDF page 215+n, not 214+n** (p216 = ED 1 Calgary-Acadia, population 55,789; p306 = ED 91 Wetaskiwin-Ponoka). Verified by matching the "Estimated Population" line on all 91 pages against `iap_app7_populations.csv` (90 exact; ED 22 reads 543612 because a page number is glued onto 54,361).
- The map pages carry only labels (township/range roads, county and city boundary names, rivers), no prose. Section 3 also has overview maps (p016, p018, p020, p022, p024, p026, p028, ...) with the same kind of labels.
- Prose populations may not match Appendix 7 (e.g. p019 gives Morinville-Sturgeon "47,131 or 12% below average"; the CSV has 53,458). Treat prose figures as pre-adjustment.

## 1. Counts of passages quoted in section 2

| Type | Passages |
|---|---|
| metes-and-bounds | 1 |
| prose boundary | 28 |
| change description | 41 |
| other | 1 |
| total | 71 |

Type codes used below: **MB** metes-and-bounds, **PB** prose boundary (names bounding features), **CH** change description (what moved between which divisions, or what the division consists of), **OT** other. Several PB passages are really composition lists; the ID prefix is B for boundary-describing and C for change/composition; X marks Minority Opinion or other-section passages.

## 2. Passages

### M1 - p085 - metes-and-bounds
Divisions: 71 Lethbridge

> Commencing at a point on the south boundary of Highway 3 west of the Oldman River at Westside Drive, then south to Garry Drive and then, westerly to Metis Trail W., southerly to Whoop Up Drive then easterly to McMaster Blvd and then southerly to Mount Burke Blvd and then westerly at Rocky Mountain Blvd until Sunridge Blvd and then directly south to the left bank of the Oldman River westerly to the southern City Limit of Lethbridge to its easterly boundary, then north to South Parkside Drive westerly to Mayor Magrath Drive then northward to the southerly boundary of Highway 3 and then returning west to the point of commencement.

### B01 - p085 - prose boundary
Divisions: 71 Lethbridge

> It is bounded on the south by the Oldman River in West Lethbridge and the city limits east of the river. It's bounded on the west by Metis Trail West. and on the north by Highway 3. On the eastern side the electoral boundary heads down Mayor Magrath to South Parkside Drive and then east to Highway 4, and then southeast along the railway tracks and then back up north to take in the Research and Development Centre and then south along the Lethbridge's eastern city limits.

### B02 - p013 - prose boundary
Divisions: 67 Lac Ste. Anne

> The Lac Ste. Anne electoral division which the panel is recommending would run from Stony Plain to Onoway to Mayerthorpe along a Highway 43 alignment. Highway 43 is the main highway which runs northwest from Edmonton to Whitecourt, Fox Creek, Valleyview and Grande Prairie and is actually part of the CANAMEX trilateral trade and transportation route connecting Canada, the United States and Mexico. The Lac Ste. Anne electoral division that the panel recommends, like the current Lac Ste. Anne-Parkland, would dip south of the Yellowhead Highway to take in Lake Wabamun and the Paul First Nation Reserve along the east shore of Lake Wabamun, putting it in an electoral division with the First Nations in Lac Ste. Anne, namely the Alexis Nakota Sioux Reserve at Lac Ste. Anne and the Alexander Cree Reserve northwest of Edmonton. This reunites the three Treaty 6 Reserves in the current (2017) Lac Ste. Anne-Parkland, that were

### C01 - p014 - prose boundary
Divisions: 67 Lac Ste. Anne

> Entwistle and Evansburg would continue to be in the same electoral division (Lac Ste. Anne) with the western boundary of the electoral division following Highway 22 north of the Yellowhead and then jogging west to take in Mayerthorpe.

### C02 - p014 - change description
Divisions: 67 Lac Ste. Anne

> In conclusion, the advisory panel proposes an electoral division called "Lac Ste. Anne" roughly consisting of: 1) The Town of Stony Plain; 2) All of Lac Ste. Anne County; 3) Lake Wabamun 4) The most northerly portions of Parkland County as shown on the accompanying map.

### C03 - p014 - change description
Divisions: 53, 79, 90, 60, 87, 62 (the divisions the report lists as modified by the Lac Ste. Anne restoration)

> but they include: 1) To the north: Barrhead-Westlock-Athabasca; 2) To the east: Morinville-St. Albert (formerly St. Albert-Sturgeon); 3) To the west: West Yellowhead; 4) To the south: Spruce Grove-Stony Plain and Drayton Valley-Devon; and 5) As far away as Fort McMurray-Lac La Biche, adjustments had to be made.

### C04 - p017 - change description
Divisions: 87 Spruce Grove

> The impact of all of this is that the Spruce Grove electoral division will be comprised mostly of Spruce Grove. It will not include Stony Plain.

### C05 - p017 - change description
Divisions: 87 Spruce Grove

> Spruce Grove and the areas immediately around it warrant an electoral division of their own. Spruce Grove is a city with a population of roughly 45,000 and is expected to grow. In the meantime, we have recommended extending the electoral division both north and south of Spruce Grove to give it the population it needs. In other words, to give Spruce Grove the population it needs for separate representation, we are including areas outside of Spruce Grove. Here is an example of where an area adjacent to an urban municipality assists it

### B03 - p019 - change description
Divisions: 79 Morinville-Sturgeon

> to push the boundary of the Morinville-Sturgeon electoral division west to parallel Highway 779, except that the Alexander First Nation Reserve would remain in the Lac Ste. Anne electoral division, but Pine Sands on Sandy Lake would become part of Morinville-Sturgeon.

### B04 - p019 - prose boundary
Divisions: 79 Morinville-Sturgeon

> The Morinville-Sturgeon electoral division that the panel recommends has clear and understandable boundaries. Its southern boundary is the City of Edmonton and the southern border of Sturgeon County. Its eastern boundary is the North Saskatchewan River. Its western boundary is the western boundary of Sturgeon County. And the electoral division's northern boundary is roughly the northern boundary of Sturgeon County. The electoral division includes the airbase at Namao, the northeast quadrant of the City of St. Albert and the Town of Morinville, further north along Highway 2. It also includes Legal, Bon Accord, Gibbons, and

### C06 - p019 - change description
Divisions: 79 Morinville-Sturgeon

> The 2025-2026 Electoral Boundaries Commission recommended that the border between the St. Albert electoral division and what we are now calling the Morinville-Sturgeon electoral division be moved within the City of St. Albert such that all areas south of the Sturgeon River in St. Albert would be mapped in the City of St. Albert electoral division. We concur in that recommendation

### C07 - p021 - change description
Divisions: 53 Barrhead-Westlock-Athabasca

> Westlock-Athabasca which are roughly the same as the current Athabasca-Barrhead-Westlock electoral division boundaries. The status quo is maintained and in the absence of a pressing need to make changes, maintaining the status quo is considered good practice in electoral boundary mapping. Studies have

### C08 - p021 - change description
Divisions: 53 Barrhead-Westlock-Athabasca

> The first change is that Swan Hills and Fort Assiniboine are not recommended to be included in the Barrhead-Westlock-Athabasca electoral division. The 2025-2026 Electoral Boundaries Commission recommended putting Swan Hills and Fort Assiniboine in the Lesser Slave Lake electoral division. The reason was because the population of the Lesser Slave Lake electoral division had fallen below 50% of the average population of all electoral divisions in the Province. Recommending such an electoral division is not permitted by the Electoral Boundaries Commission Act. The Commission's reasoning therefore struck us as being reasonable.

### C09 - p021 - change description
Divisions: 53 Barrhead-Westlock-Athabasca

> A second change to the current Athabasca-Barrhead-Westlock electoral division the panel recommends is to add the Saddle Lake Cree Nation's Reserve at the southeastern extremity of the electoral division. The Saddle Lake Cree Nation's Reserve is currently mapped in the Bonnyville-Cold Lake-St. Paul electoral division. The Saddle Lake Cree Nation claims roughly 11,000 members. Portions of the County of St. Paul were recommended by the 2025-2026 Electoral Boundaries Commission to be moved to Bonnyville-Cold Lake-St. Paul because it unites most of the County of St. Paul in the same electoral division. We concur in that recommendation.

### B05 - p023 - prose boundary
Divisions: 62 Fort McMurray-Lac La Biche

> The Fort McMurray-Lac La Biche electoral division, as mapped by the 2016-2017 Electoral Boundaries Commission, currently runs north from the Kikino Metis Settlement south of Lac La Biche to Lac La Biche, and then up Highway 881 paralleling the now defunct Alberta and Great Waterways Railway. The electoral division also parallels the main highway to Fort McMurray (Highway 63). It includes places like Plamondon, Wandering River, Janvier, Anzac, Gregoire Lake and portions of Fort McMurray, principally south of the

### B06 - p023 - prose boundary
Divisions: 62 Fort McMurray-Lac La Biche

> Roughly speaking, Fort McMurray-Lac La Biche's western boundary is the Athabasca River. Its northern boundary is the Athabasca and Clearwater Rivers. Its eastern boundary is the Saskatchewan border and the Cold Lake Air Weapons Range, and its southern boundary is south of Lac La Biche. The 2025-2026 Electoral Boundaries Commission deemed it necessary to push the southern boundary south to Smoky Lake County and then to shed population, recommended moving its two urban communities north of the Athabasca into Fort McMurray-Wood Buffalo.

### C11 - p023 - change description
Divisions: 62 Fort McMurray-Lac La Biche; 63 Fort McMurray-Wood Buffalo

> necessary. It is also no longer necessary to move the Fort McMurray communities of Martin Ridge Estates and Wood Buffalo Estates north of the Athabasca River and south of Thickwood Boulevard into Fort McMurray-Wood Buffalo. The Fort McMurray-Lac La Biche electoral division needs the population these

### C12 - p025 - change description
Divisions: 90 West Yellowhead

> In any event, the advisory panel is able to recommend its restoration. That restoration involved moving Mayerthorpe out of West Yellowhead, as mapped by the 2025-2026 Electoral Boundaries Commission, back into Lac Ste. Anne where it was situated in the last general election.

### B07 - p027 - prose boundary
Divisions: 60 Drayton Valley-Devon

> The current (2017) Drayton Valley-Devon electoral division runs from Devon, through Calmar, Thorsby, Warburg, Alsike, Drayton Valley along Highway 39 and beyond to places like Lodgepole, Brazeau and Cynthia. It also straddles the North Saskatchewan River from Devon to Drayton Valley.

### B08 - p027 - prose boundary
Divisions: 60 Drayton Valley-Devon

> The current Drayton Valley-Devon electoral boundary makes a right turn at the intersection of Highway 22 and Highway 16 and heads east for several kilometres before heading south again on Highway 759 to avoid taking Lake Wabamun out of Lac Ste. Anne. We recommend that electoral boundary to keep Lake Wabamun in Lac Ste. Anne. It also keeps both Entwistle and Evansburg in Lac Ste. Anne. The separation of those two communities on either side of the Pembina River has been an issue before prior boundary commissions.

### B09 - p027 - prose boundary
Divisions: 60 Drayton Valley-Devon; 42 Edmonton-Nisku; 69 Leduc-Beaumont

> One final note, the eastern boundary of Drayton Valley-Devon is right next to the Edmonton International Airport and the Edmonton-Nisku electoral division. Further south the eastern boundary of Drayton Valley-Devon abuts the City of Leduc and the Leduc-Beaumont electoral division. There may need to be adjustments made to the eastern boundary of Drayton Valley-Devon to accommodate Edmonton-Nisku and

### C13 - p030 - change description
Divisions: 42 Edmonton-Nisku; 69 Leduc-Beaumont

> Edmonton-Nisku would consist of Edmonton-South East electoral division, Nisku and areas north of Airport Road east of Highway 2 and west of the Leduc-Beaumont electoral division. The creation of a new electoral

### B10 - p033 - prose boundary
Divisions: 42 Edmonton-Nisku

> Edmonton-Ellerslie, Edmonton-South and Edmonton Meadows. The electoral division which the panel recommends is located roughly where Edmonton-South East was recommended to be located in the 2025- 2026 Electoral Boundaries Commission's Interim Report. It includes Nisku Industrial Park and surrounding areas. It also includes areas north of Beaumont straddling 50th Street, the main road connection between Beaumont and Edmonton. Its northern boundary is roughly the Anthony Henday Drive although its electoral boundary does cross over the Anthony Henday Drive to take in a bit of Edmonton-Ellerslie and Edmonton- Meadows. Its eastern boundary is Edmonton's eastern city limits.

### B11 - p033 - prose boundary
Divisions: 42 Edmonton-Nisku

> Most of the new Edmonton-Nisku electoral division is within the City of Edmonton, although, of course, it also takes in northwestern portions of Leduc County. The Edmonton portions are: 1) Areas in the City of Edmonton, south of 41st Avenue SW, east of Gateway Boulevard, and west of the City of Edmonton's eastern limits (taken from Edmonton-Ellerslie and Edmonton-South); 2) Areas north of 41st Avenue SW, east of 66th Street SW, south of Anthony Henday Drive, and west of the city's eastern limits (taken from Edmonton-Ellerslie); 3) Areas north of Anthony Henday Drive, east of 34th Street NW, south of 16A or 15th Avenue NW and west of 17th Street NW (taken from Edmonton-Ellerslie and Edmonton Meadows); and 4) Areas north of Anthony Henday Drive, east of 50th Street NW, south of 23rd Avenue NW, and west of 34th Street NW (taken from Edmonton-Ellerslie).

### B12 - p035 - prose boundary
Divisions: 45 Edmonton-South

> Edmonton-South is an electoral division west of Highway 2 (Calgary Trail or Gateway Boulevard). It runs from the City of Edmonton's southern limits north to Ellerslie Road. Its western boundary follows Whitemud Creek for most of its length. Edmonton-South is a rapidly growing electoral division. Subject to the changes

### C14 - p035 - change description
Divisions: 45 Edmonton-South; 48 Edmonton-Whitemud; 49 Edmonton-Windermere; 33 Edmonton-Ellerslie

> The elimination of Edmonton-Beaumont and the creation of Edmonton-Nisku enabled the current boundaries of this electoral division to be restored subject to the following changes: 1. It is proposed that this electoral division lose territory along its northern boundary, given its growth in population. All areas north of Ellerslie Road and west of Gateway Boulevard are recommended to be moved to Edmonton-Rutherford. 2. Areas north of Anthony Henday Drive and west of Whitemud Creek are proposed to be moved to Edmonton-Whitemud. This will help balance the populations in the electoral divisions and create clearer boundaries. 3. In addition, it is proposed that the community of Chappelle Gardens be moved to Edmonton-South West (which the 2025-2026 Electoral Boundaries Commission renamed Edmonton-Windermere) to reduce the population of Edmonton-South.

### C15 - p037 - change description
Divisions: 33 Edmonton-Ellerslie

> division to replace the Edmonton-Beaumont electoral division, namely Edmonton-Nisku. In order to create Edmonton-Nisku, all areas of Edmonton-Ellerslie east of 50th Street N.W. and north of the Anthony Henday Drive are recommended to be moved to Edmonton-Nisku. However, the Edmonton-Ellerslie electoral division gains areas south of 25th Avenue S.W. and east of Gateway Boulevard from the Edmonton-South electoral division which previously straddled Gateway Boulevard. That straddling was not considered ideal

### B13 - p037 - prose boundary
Divisions: 33 Edmonton-Ellerslie

> division on the east side of Highway 2 or Gateway Boulevard, running from the City's south city limit (41st Avenue S.W.) north to 23rd Avenue N.W. (i.e. north of the Anthony Henday Drive). Its eastern boundary, south of the Anthony Henday Drive, is 66th Street S. W. Its eastern boundary, north of the Anthony Henday Drive, is 50th Street N.W. while its north boundary is 23rd Avenue N.W. The electoral division consists of the Mill Woods communities of Satoo, Knottwood, Menisa, Ekota, and Sakaw north of the Anthony Henday Drive and the neighborhoods of Ellerslie, Summerside and the Orchards

### B14 - p039 - prose boundary
Divisions: 40 Edmonton-Meadows

> The Edmonton-Meadows electoral division as mapped by the 2025-2026 Electoral Boundaries Commission in its Interim Report (and in its Final Report) has clear and understandable boundaries. Its northern boundary is still Whitemud Drive or Highway 14 (the highway to Viking and Wainwright) and 38th Avenue N.W. Its southern boundary is still Anthony Henday Drive and 16A Avenue N.W. Its western boundary is still 34th

### C16 - p039 - change description
Divisions: 40 Edmonton-Meadows

> bordering Edmonton's eastern city limits. The 2025-2026 Electoral Boundaries Commission recommended that western portions of the current Edmonton-Meadows electoral division west of 34th Street N.W. be moved into Edmonton-Mill Woods and Edmonton-Ellerslie to create Edmonton-Beaumont. The removal of Edmonton-Beaumont has not changed that. Since we are adopting the recommendations of the Commission's Interim Report, it is still recommended that the western portions of the electoral division be moved into Edmonton-Mill Woods and Edmonton-Ellerslie.

### B15 - p041 - prose boundary
Divisions: 49 Edmonton-Windermere

> Edmonton-South West (which the 2025-2026 Electoral Boundaries Commission renamed Edmonton- Windermere in its Final Report) is currently a north-south electoral division between the City's southern boundary (Highway 19 to Devon) and Anthony Henday Drive. It is bounded on the east by Whitemud Creek and the Edmonton-South electoral division. Its current (2017) configuration, which we recommend changing, straddles the North Saskatchewan River on the west. In short, it lies between Devon and the Edmonton International Airport at its south end and the Anthony Henday Drive at its northern end.

### C17 - p041 - change description
Divisions: 49 Edmonton-Windermere

> In its Interim Report, the 2025-2026 Electoral Boundaries Commission recommended moving the western boundary of the electoral division east to the North Saskatchewan River such that the electoral division would no longer have to straddle the river. The advisory panel concurs in that recommendation which, if approved, would put residents west of the river in either Edmonton-West Enoch or Edmonton-McLung.

### C18 - p041 - change description
Divisions: 49 Edmonton-Windermere

> In its Interim Report, the 2025-2026 Electoral Boundaries Commission also adjusted the eastern boundary of the electoral division somewhat, departing from Whitemud Creek between 28th Avenue and 41st. Avenue S.W. along Chappelle Link S.W. The neighbourhood of Chappelle Gardens was recommended to be moved from Edmonton-South into Edmonton-South West (Edmonton-Windermere) to accommodate significant anticipated growth in Edmonton-South. The advisory panel concurs in that recommendation. But for the most part the electoral division's eastern boundary is recommended to be Whitemud Creek which is the current eastern boundary of the electoral division.

### C19 - p043 - change description
Divisions: 48 Edmonton-Whitemud

> Three changes to this electoral division as recommended by the 2025-2026 Electoral Boundaries Commission are also recommended by the advisory panel. The first is to add an area east of Rabbit Hill Road north of the Anthony Henday Drive between Rabbit Hill Road and Whitemud Creek. This was recommended by the 2025-2026 Electoral Boundaries Commission in its Interim Report and Final Report. Secondly, instead of the eastern boundary following Whitemud Drive north to the North Saskatchewan River, the advisory panel recommends it follow Whitemud Creek north to the River. Areas west of Whitemud Creek (between Whitemud Creek and Whitemud Drive) have thereby been added to the electoral division. Reverting back to the Whitemud Creek boundary increases the population of the electoral division. Thirdly, all areas south of Anthony Henday Drive are recommended to be removed. This makes a lot of sense. The Anthony Henday is a major barrier both physically and psychologically. Adding the area between Rabbit Hill Road and Whitemud Creek makes the Edmonton-Whitemud electoral division, arguably, a clearer and more understandable electoral division between the Anthony Henday Drive on the south and the North Saskatchewan River on the north, with Whitemud Creek forming its eastern boundary and the North Saskatchewan River forming not only its northern boundary but also its western boundary. The electoral division now has a configuration similar to Edmonton-South West (Edmonton- Windermere) to the south. The recommended mapping also addressed a criticism of the current mapping by bringing Magrath Heights and Mactaggart, two Terwillegar communities, into the electoral division with the rest of Terwillegar.

### C20 - p045 - change description
Divisions: 46 Edmonton-Strathcona

> Other changes the 2025-2026 Electoral Boundaries Commission recommended to the current (2017) electoral division were to move portions east of 99th Street and north of 63rd Avenue or Argyll Road into Edmonton Gold Bar (neighborhoods like Ritchie, Hazeldean and Argyll). The Commission also expanded the electoral division to the west to take in portions of Edmonton Riverview electoral division, (i.e. McKernan, Parkallen, Belgravia, Windsor Park, Grandview Heights and Lansdowne). The advisory panel concurs with the

### B16 - p045 - prose boundary
Divisions: 46 Edmonton-Strathcona

> centered electoral division, bounded on the south by Whitemud Drive, on the north by the North Saskatchewan River, on the west, by Whitemud Creek and on the east by Gateway Boulevard, 99th Street

### B17 - p048 - prose boundary
Divisions: 85 Rocky Mountain House-Sundre

> The new Rocky Mountain House-Sundre electoral division's southern boundary meanders west along a watershed northwest of Cochrane to the B.C. Border. Its western boundary follows the B.C. Border north to the Brazeau River and then northeast along the Brazeau River to the northern boundary of Clearwater County which is recommended to form the northern boundary of the electoral division as well. The electoral division includes the Saulteaux/Cree First Nations' O'Chiese and Sunchild Reserves in the north. Its eastern boundary is roughly a north-south line just east of the Highway 22 corridor which runs north-south up the spine of the Province's "West Country". The electoral division includes Sundre, Caroline, Rocky Mountain

### C21 - p051 - change description
Divisions: 91 Wetaskiwin-Ponoka

> The significant change here is the inclusion of Ponoka in the electoral division. Ponoka is currently in an electoral division with Lacombe. The 2025-2026 Electoral Boundaries Commission recommended moving Ponoka into this electoral division. The advisory panel concurs. The current Maskwacis-Wetaskiwin electoral division that was mapped by the 2017 Electoral Boundaries Commission, and which was in place for the last general election, is a compact and understandable electoral division comprised of Wetaskiwin, the four First Nations at Maskwacis, as well as Millet, Pigeon Lake, Falun and Westerose. The advisory panel tried to mimic the current electoral division as best we could. However, we had to recommend extending the electoral division west to Alder Flats taking in Battle Lake, Winfield and Buck Lake. To the southwest, the panel recommends extending the electoral division to take in Rimbey. Like the Commission, the advisory panel recommends moving the northeast portion of the electoral division into the Camrose electoral division, including Kavanagh, New Sarepta and Hay Lakes.

### B18 - p053 - prose boundary
Divisions: 68 Lacombe-Sylvan Lake

> The proposed electoral division would include Gull Lake and Bentley to the west and a portion of Buffalo Lake to the east as well as Sylvan Lake to the southwest.

### C22 - p053 - change description
Divisions: 61 Drumheller-Stettler; 68 Lacombe-Sylvan Lake

> Because the Lacombe-Sylvan Lake electoral division extends all the way to Buffalo Lake, there would have to be changes to the west end of the electoral division of Drumheller-Stettler as mapped by the 2025-2026 Electoral Boundaries Commission. The Commission had mapped the western boundary of Drumheller- Stettler extending all the way up to the town limits of Lacombe and Morningside which put a large riding east of the Red Deer River (Drumheller-Stettler) adjacent to Highway 2. That was, perhaps, unavoidable but nevertheless incongruous.

### B19 - p055 - prose boundary
Divisions: 54 Blackfalds-Innisfail

> The advisory panel's proposed Blackfalds-Innisfail electoral division is an electoral division that surrounds Red Deer on all sides. It includes Blackfalds with a population of roughly 12,000 people and Innisfail with a population of about 8,000 people. It takes in a bit of Red Deer at the north end and the Westerner Park, Red Deer's fairgrounds, hockey and rodeo arenas, racetrack and exhibition hall and several other agriculture- related service centres at the south end. South and west of Red Deer the Blackfalds-Innisfail electoral division includes Penhold, Innisfail, Spruce View, the Dickson Dam and Gleniffer Lake. It does not include Sylvan Lake which the advisory panel recommends for the Lacombe-Sylvan Lake electoral division. Nor does it include Bowden which we recommend for Olds-Didsbury-Three Hills. South and east, it includes Delburne, Elnora and Pine Lake.

### C23 - p057 - change description
Divisions: 81 Olds-Didsbury-Three Hills

> The 2025-2026 Electoral Boundaries Commission reluctantly concluded that they had to add portions of Mountain View County that were previously in the deleted Rimbey-Rocky Mountain House-Sundre electoral division to the newly named Mountain View-Kneehill electoral division. Now that Rocky Mountain House- Sundre has been substantially restored, extending Olds-Didsbury-Three Hills out to the west of Sundre is no longer necessary. The Commission also included the Town of Bowden in this electoral division but conceded that it could just as easily have been put in Sylvan Lake-Innisfail. Bowden is between Innisfail and Olds on Highway 2. The Commission's reason for including the Town of Bowden in Mountain View-Kneehill (Olds-Didsbury-Three Hills) was that it balanced the electoral division's population with Sylvan Lake-Innisfail (now Blackfalds-

### C24 - p057 - change description
Divisions: 81 Olds-Didsbury-Three Hills

> The Commission also moved Crossfield and Irricana out of the Olds-Didsbury-Three Hills electoral division to create the new Airdrie East electoral division. We concur in that recommendation as well. The 2025-2026 Electoral Boundaries Commission also recommended moving parts of the extreme southeast of the Olds-Didsbury-Three Hills electoral division into the High River-Vulcan-Siksika electoral division they recommended, including Rockyford, Rosebud, Standard and Hussar. The advisory panel

### C25 - p057 - change description
Divisions: 81 Olds-Didsbury-Three Hills

> 2017 Electoral Boundaries Commission proposed to keep Cardston-Siksika from becoming too large. The panel recommends that the southeast boundary of Olds-Didsbury-Three Hills extend south to the Siksika First Nations Reserve where it will adjoin the recommended Little Bow electoral division in a manner similar to the way the current Olds-Didsbury-Three Hills electoral division adjoins Cardston-Siksika. The recommended Little Bow electoral division is explained later in this report.

### C26 - p059 - change description
Divisions: 61 Drumheller-Stettler

> opportunity to reconfigure the Highway 2 corridor electoral divisions. As a consequence, a portion of the Drumheller-Stettler electoral division west of Buffalo Lake, which the 2025-2026 Electoral Boundaries Commission recommended adding to the electoral division, no longer needs to be added. The portion recommended to be added would have brought Drumheller-Stettler's northwest boundary right up to Highway 2 and the eastern borders of Blackfalds, Lacombe and Morningside. The advisory panel is now in a position to recommend that the northwestern boundary run north-south just east of Stettler through Nevis to Buffalo Lake.

### B20 - p059 - prose boundary
Divisions: 61 Drumheller-Stettler

> Drumheller-Stettler is a huge electoral division, with the Red Deer River as its western boundary and the Saskatchewan border as its eastern boundary. Its northern boundary follows roads to the Saskatchewan border northeast of Provost. It contains Stettler at its northwest end, Provost at its northeast end, Drumheller on its west boundary and Empress (near Medicine Hat) in its extreme southeast. It contains Stettler, Castor,

### B21 - p065 - prose boundary
Divisions: 22 Calgary-North West-Bearspaw

> Calgary-North West is an electoral division bordering Calgary's city limits in northwest Calgary. It was not changed by the 2025-2026 Electoral Boundaries Commission despite submissions requesting that the western boundary of the electoral division be moved westward to include the adjacent Rocky View County communities of Bearspaw Village, Watermark and Church Ranches which the submitters contended were functionally integrated with City of Calgary communities to the east through schools, sports, churches,

### B22 - p065 - prose boundary
Divisions: 22 Calgary-North West-Bearspaw

> Significantly, the electoral division already crosses 12-Mile Coulee Road at its south end to include portions of communities known as Bearspaw Meadows and Rockland Park which is very much an urban subdivision. And the reason is that the City limits themselves cross 12-Mile Coulee Road in a "fish hook" shape to incorporate two Bearspaw communities. And so the electoral division recommended by not only the 2025- 2026 Electoral Boundaries Commission, but also by the 2017 Electoral Boundaries Commission and the 2010 Electoral Boundaries Commission did in fact cross 12-Mile Coulee Road at the south end to take in the two Bearspaw communities, both adjacent to the Bearspaw Reservoir on the Bow River. The reason the boundaries of the City of Calgary cross 12-Mile Coulee Road near the Bow River, we suspect, is to give the City control of its largest fresh water reservoir created by the Bearspaw Dam on the Bow River.

### C27 - p066 - change description
Divisions: 22 Calgary-North West-Bearspaw; 4 Calgary-Bow-Springbank

> Church Ranches is admittedly right across 12-Mile Coulee Road from the Calgary Bow community of Rocky Ridge but there are a handful of other Bearspaw subdivisions north of the highway which are also either adjacent to Rocky Ridge or adjacent to Church Ranches. The issue these communities present is where do you stop? One might go all the way west to Lochend Road (Highway 766) which could serve as a natural electoral boundary, but how far north of Church Ranches do you go to possibly take in Rolling Acres, Biggar Meadows, Biggar Heights and Woodland Estates? The advisory panel would have preferred more input than its process permitted to be comfortable adding Church Ranches to the Calgary Bow electoral division. But it is certainly something for the Legislature, or a future electoral boundaries commission, to consider. As a result, the independent advisory panel is only recommending the inclusion of the Bearspaw subdivisions south of Highway 1A. But there is definitely a case to be made for also including Church Ranches.

### B23 - p069 - prose boundary
Divisions: 4 Calgary-Bow-Springbank; 28 Calgary-West-Springbank; 58 Cochrane

> Second, there is the issue of defining with precision what geographical area should be added. Springbank, as Calgarians generally understand it, consists of a number of suburban and acreage subdivisions west of Calgary on both sides of the TransCanada Highway. For the purposes of the advisory panel's recommendations, Springbank is defined on the west by the north- south Highway 22 connecting Bragg Creek to Cochrane. Its northern boundary is the Bow River. Its southern boundary is Highway 8. And its eastern boundary is the City of Calgary.

### C28 - p069 - change description
Divisions: 4 Calgary-Bow-Springbank; 28 Calgary-West-Springbank

> which made more sense. The advisory panel proposes that Springbank be paired with either Calgary-Bow or Calgary-West depending on what side of the TransCanada Highway its residents live. The connection between Springbank and Cochrane is clearly not as strong as it once was and certainly not as strong as Springbank's connection to Calgary. We were not all agreed, but the majority proposes that the Legislature consider putting North Springbank in the Calgary-Bow electoral division and South Springbank into the Calgary-West electoral division. North Springbank being that portion of Springbank north of the TransCanada Highway and South Springbank being that portion south of the TransCanada Highway.

### C29 - p071 - change description
Divisions: 4 Calgary-Bow-Springbank

> In conclusion, the majority of the advisory panel recommends that the Legislature consider mapping North Springbank into the Calgary-Bow electoral division and naming it Calgary-Bow-Springbank.

### B24 - p073 - prose boundary
Divisions: 28 Calgary-West-Springbank

> In the last general election, Calgary West was a relatively compact and understandable electoral division between Sarcee Trail and the City limits or 101St Street S.W. It was bordered on the north by Bow Trail and on the south by a City of Calgary boundary. It included the Calgary communities of Strathcona, Christie Park, Signature Parke, Signal Hill and Richmond Hill along Sarcee Trail and Aspen Woods, Elbow View, Springbank Hill and Discovery Ridge to the west. The electoral division of Banff-Kananaskis, stretching all the way from

### B25 - p073 - prose boundary
Divisions: 28 Calgary-West-Springbank

> Evidence for that can be found in what the Commission recommended. The Commission recommended putting an elongated east-west stretch of land south of the Elbow River straddling Highway 8 into Calgary- West and called it Calgary-West-Elbow Valley. The Commission's Elbow Valley straddled Highway 8 (the highway to Bragg Creek) all the way to Highway 22 (the highway between Bragg Creek and Cochrane). The electoral division's southern border was the Tsuut'ina Nation's Reserve west of Calgary which the Commission recommended be included in another Calgary electoral division, namely Calgary Glenmore.

### C30 - p073 - change description
Divisions: 28 Calgary-West-Springbank

> those reasons apply equally to the rest of South Springbank. And so, the panel recommends that the entire area loosely referred to as South Springbank be amalgamated with Calgary-West for electoral boundary purposes. The electoral division we propose would have a much more regular polygon shape with straight line boundaries, as opposed to the long, narrow, meandering salamander shape of Calgary-West-Elbow

### C31 - p077 - change description
Divisions: 58 Cochrane

> The 2025-2026 Electoral Boundaries Commission recommended removing West Airdrie and a portion of Rocky View County and putting Cochrane into an electoral division with Springbank south of Cochrane. What the 2025-2026 Electoral Boundaries Commission did made sense, but the advisory panel believes that Springbank's connection to Calgary is even stronger than its connection to Cochrane. This is, the advisory

### C32 - p087 - change description
Divisions: 73 Lethbridge-Little Bow

> Re-establishing a Little Bow electoral division would restore a historically coherent voice for communities tied by Highways 23 and 24, irrigation, intensive agriculture and the Lethbridge-area agricultural services including contiguous portions of eastern Lethbridge along Highway 3 and a contiguous portion of western Lethbridge, again along Highway 3. The proposed electoral division therefore would provide population balance and "connects" the rural electoral division to the urban services, employment and processing capacity in Lethbridge upon which

### B26 - p087 - prose boundary
Divisions: 73 Lethbridge-Little Bow

> The electoral division of Little Bow has been in existence as a provincial constituency since 1913. It has typically extended north from Lethbridge up Highways 23 and 24 capturing places like Nobleford, Barons, Carmangay, Champion, Vulcan and that connect Picture Butte with Enchant, Travers Reservoir, Lomond, Milo, Arrowwood, across the Bow River and the Siksika Reserve to Gleichen and Cluny. Significantly it also

### B27 - p089 - prose boundary
Divisions: 74 Lethbridge-Taber-Warner

> This is an electoral division which is mapped and organized around the Highway 3 and Highway 4 corridors east and south of Lethbridge. Highway 3 east to Coaldale, Taber, with a detour north to Vauxhall, and on to Bow Island. Highway 4 to the south to Warner, Milk River and the U.S. Border at Coutts is a part of the CANAMEX Corridor, a 3,700-mile/6,000 km network of highways and transportation infrastructure linking Alberta, the United States and Mexico. And east of Highway 4 at Stirling the electoral division extends just south of Lethbridge along Highway 61 to Wrentham, Foremost and Manyberries.

### C33 - p091 - change description
Divisions: 72 Lethbridge-Cardston

> Another solution to this population disparity problem is the creation of a Cardston, Magrath, Raymond, and Blood Reserve electoral division that borrows population from the City of Lethbridge (roughly 17,000 people).

### B28 - p093 - prose boundary
Divisions: 76 Macleod-Crowsnest

> Macleod-Crowsnest remains a huge electoral division west of Lethbridge. It runs from Fort Macleod west to the Crowsnest Pass along Highway 3, including Pincher Creek and Waterton Lakes National Park. From Fort Macleod north to High River up Highway 2, including Granum, Claresholm, Stavely, Nanton and Blackie. And north from Lundbreck up Highway 22 to the Chain Lakes Provincial Park and the south boundary of Kananaskis Country. It includes the Piikani First Nation Reserve at Brocket. It is bounded on the south end west by the U.S. and B.C. borders respectively. It is bounded on the east by the Waterton, Belly and Little Bow Rivers. The electoral division's east boundary heads southeast from Monarch along the Belly and Waterton

### C34 - p093 - change description
Divisions: 76 Macleod-Crowsnest

> electoral division. The Commission mapped its northern boundary south of Claresholm along Highway 520 and along the north boundary of Lethbridge County. But in order to draw down the electoral division's north boundary, the Commission had to push its eastern boundary further east to take in Coaldale, Picture Butte, Turin such that the Livingston-Macleod electoral division the Commission recommended would have surrounded the City of Lethbridge on three sides, taking in Coalhurst and Coaldale and territory to the east

### C35 - p095 - change description
Divisions: 52 Banff-Canmore-Diamond Valley

> The change is to the electoral division's southwest boundary to take in not only the Bearspaw First Nation Reserve near Longview, but also the Highway 22 corridor north through Longview, Diamond Valley, Millarville, Priddis and Bragg Creek. Other than this change and the adjustment to the northeast boundary of the

### C36 - p095 - change description
Divisions: 52 Banff-Canmore-Diamond Valley

> Priddis and Bragg Creek. Other than this change and the adjustment to the northeast boundary of the electoral division to accommodate the restoration of the Rocky Mountain House-Sundre electoral division, Banff-Canmore-Diamond Valley is similar to what the 2025-2026 Electoral Boundaries Commission recommended, except that it does not require S.15(2) status.

### C37 - p096 - change description
Divisions: 52 Banff-Canmore-Diamond Valley; 80 Okotoks

> Finally, separating Diamond Valley from Okotoks gives Okotoks its own representative to which it will soon be entitled if it continues to grow the way it has.

### X01 - p114 - other
Divisions: 28 Calgary-West-Springbank (the Commission's Calgary-West-Elbow Valley)

> division of Calgary-West by putting a community outside Calgary into it. That community was Elbow Valley and the area which the Commission incorporated into the electoral division stretched all the way from the city limits to Highway 22 northeast of Bragg Creek.

### X02 - p126 - change description
Divisions: 67 Lac Ste. Anne (Minority Opinion)

> a) the Town of Stony Plain; b) all of Lac Ste. Anne County; c) the three Treaty 6 reserves previously in Lac Ste. Anne-Parkland; and d) the most northern portions of Parkland County as demonstrated on the IAP Majority map.

### X03 - p127 - change description
Divisions: 60 Drayton Valley-Devon (Minority Opinion)

> 26. Because Stony Plain and portions of Parkland County have been removed from Stony Plain-Drayton Valley, Drayton Valley-Devon can be recreated, with its border extending all the way east to Highway 2. Highway 2 is a logical border. This electoral division is also closer to the status quo, with clear transportation

### X04 - p127 - change description
Divisions: 42 Edmonton-Nisku (Minority Opinion)

> 29. To prevent the population of Leduc-Beaumont being too high, the Panel recommends the creation of an "Edmonton-Nisku", consisting of: a) Edmonton-South East as outlined in the Interim Report; and b) Nisku and surrounding rural areas north of Leduc/Airport Road, east of Edmonton International Airport/Highway 2, and west of Beaumont's western border. Everything else south of the North Saskatchewan River in Edmonton can thus revert to the map outlined in the ABEBC Interim Report. This is part of the terms of implementing Recommendation 5. This is a better map of Edmonton, as electoral divisions become smaller. The electoral divisions further follow major roadways and waterways more logically. In particular, it does not become necessary for any electoral division to cross Gateway Boulevard, which is a major divider of communities in South Edmonton. Edmonton-Whitemud can further remain entirely north of Anthony Henday Drive, which is also a major divider in this area of Edmonton.

### X05 - p128 - change description
Divisions: 85 Rocky Mountain House-Sundre and neighbours (Minority Opinion)

> 33. The Panel unanimously proposes the second restored electoral division be "Rocky Mountain House- Sundre", consisting mostly of: a) The vast majority of Clearwater County; b) The most western parts of Mountain View County including all of Sundre and Cremona and surrounding areas; c) Portions of the MD of Bighorn presently in Rimbey-Rocky Mountain House-Sundre; and d) Portions of the MD of Bighorn and Banff National Park north of the Bow River watershed. 34. This has impacts on only six other electoral divisions: a) Mountain View-Kneehill (renamed Olds-Didsbury-Three Hills): loses the most western portions of Mountain View County, including Sundre and Cremona, so as to concentrate on its agricultural core in the Highway 2 corridor; b) Lacombe-Clearwater (renamed Lacombe-Sylvan Lake): becomes all of the areas surrounding Sylvan Lake, most of Lacombe County, the City of Lacombe, the southeastern portions of Ponoka County, a small piece of Clearwater County, and the portions of Ponoka County immediately north of Gull Lake; c) Wetaskiwin-Ponoka-Maskwacis (renamed Wetaskiwin-Ponoka): becomes all of Wetaskiwin County, and almost all of Ponoka County, save for discrete portions included in Lacombe-Sylvan Lake given the need for population balance and the desire to keep all Gull Lake communities together; d) Drumheller-Stettler: loses portions of Lacombe County, which were an odd fit in this sprawling eastern electoral division; e) Sylvan Lake-Innisfail (renamed Blackfalds-Innisfail): becomes most of Red Deer County, except the areas including and immediately around Sylvan Lake, while also including the areas immediately surrounding and including Blackfalds; and f) Canmore-Banff: loses portions presently in Rimbey-Rocky Mountain House-Sundre and north of the Bow River watershed, which share more in common with the Eastern Slopes from transportation,

### X06 - p126 - change description
Divisions: 53, 62, 63, 79 (Minority Opinion)

> 23. As a result of this restoration of Lac Ste. Anne, Barrhead-Westlock-Athabasca can return to borders much closer to the status quo, though exchanging some territory with Cold Lake-Bonnyville-St. Paul for reasons outlined in the Interim Report. It has lost territory to Lesser Slave Lake, in recognition of MLA van Dijken's concern about representing too many counties. The Panel does not propose changing Lesser Slave Lake back to its current borders, consistent with Justice Miller's instructions to preserve the ABEBC Majority Map to the extent possible. Barrhead-Westlock-Athabasca has accordingly become smaller and more compact. This will increase effective representation, and mitigates the MLA's concerns with representing too many municipalities across too vast a geographic distance. 24. Because of these changes, Smoky Lake County can leave Fort McMurray-Lac La Biche. This means that the electoral divisions of Fort McMurray-Lac La Biche and Fort McMurray-Wood Buffalo can return to the same borders as the 2017 redistribution and as outlined in the ABEBC Interim Report. This restoration of the status quo reduces the population in these vast rural areas. This increases effective representation for these areas and minimizes disruptions to the status quo. We are not certain the IAP Majority agrees with restoring the boundaries of Fort McMurray-Wood Buffalo. 25. Another result of the recreation of the Lac Ste. Anne electoral division is the reduction in the size of St. Albert-Sturgeon, by keeping Alexander First Nation in Lac Ste. Anne. This will facilitate effective representation. The electoral division now includes the northeastern corner of St. Albert and the other parts of Sturgeon County outside Alexander First Nation. The Panel unanimously proposes that this electoral division be renamed Morinville-Sturgeon. The low population of Morinville-Sturgeon is justified by the high population growth in this area. This population growth is already significant and the possible development of Meta's artificial intelligence data centre will likely increase that. Despite the gap in population, we do not propose readjusting the border with St. Albert. The imbalance in population with

### Passages not extracted verbatim (context only)

- p029-p030, ED 69 Leduc-Beaumont: narrative of how the Commission's Interim and Final maps put Leduc and Beaumont together or apart; no boundary features beyond C13/B10.
- p061-p063, Northeast Calgary discussion (not a changed division): mentions Deerfoot Trail, 16 Avenue, Trans-Canada Highway, Bow River, 36 Street NE as boundaries of Calgary-Klein / Cross / Confluence.
- p079-p082 (Southern Alberta rationale): Highway 3, 4, 23 corridors, Oldman and Bow Rivers, irrigation districts; no division-level boundary.
- p091 (ED 72): Cardston-Siksika is called an "hourglass shaped electoral division running from the U.S. border to the TransCanada Highway east of Calgary" (the 2017 shape the panel replaces). The new ED 72 is only identified by its communities (see C33).
- p093 (ED 76): beyond B28, "The Commission mapped its northern boundary south of Claresholm along Highway 520 and along the north boundary of Lethbridge County" (C34).
- p120, p130 (Minority): disagreement with the majority's "proposed boundaries of Red Deer-South and Blackfalds-Innisfail"; no feature named. This is the only mention of ED 84 in the report text besides the lists on p161-p162 and Appendix 7.
- p187 (Chair's Addendum, Recommendation 5): restoration "should ... have no impact on any electoral division in Airdrie or containing territory south of Airdrie's southernmost border, with the exception of Drumheller-Stettler", and Edmonton south of the river reverts to the Interim map. A constraint, not a boundary.
- p203-p208 (Appendix 6 composite maps): label-only maps (Lac Ste. Anne cascade, Leduc-Beaumont/Edmonton, Rocky Mountain House-Sundre/Banff, Highway 2 corridor, Calgary); no prose.

## 3. Coverage of the 35 changed divisions

Completeness scale: **full ring** = every side of the division is described in words or metes-and-bounds; **near-full** = most sides, one or more edges unstated or cut off in the text layer; **partial** = some edges or a corridor/composition; **change only** = only what moved between divisions; **none**.

| ED | Name | Passages | Completeness |
|---|---|---|---|
| 1 | Calgary-Acadia | (none; only the name in the Minority's list p161) | none |
| 4 | Calgary-Bow-Springbank | B23, C27, C28, C29, B22 | change only + partial: Springbank defined as W Highway 22, N Bow River, S Highway 8, E Calgary; North Springbank = north of the TransCanada added; Bearspaw subdivisions south of Highway 1A added; no ring for the whole division |
| 22 | Calgary-North West-Bearspaw | B21, B22, C27 | partial: city limits, crosses 12-Mile Coulee Road at south end (Bearspaw Meadows, Rockland Park); said to be unchanged from the Commission map |
| 28 | Calgary-West-Springbank | B24, B25, C28, C30, B23, X01 | partial: old Calgary West = Sarcee Trail to 101 St SW, Bow Trail north, city boundary south; adds all South Springbank (south of the TransCanada, Highway 8 corridor); "regular polygon ... straight line boundaries" |
| 33 | Edmonton-Ellerslie | B13, C14, C15 | near-full prose ring: W Highway 2/Gateway Blvd, S city limit (41 Ave SW), E 66 St SW (south of Henday) / 50 St NW (north of Henday), N 23 Ave NW |
| 40 | Edmonton-Meadows | B14, C16 | full prose ring: N Whitemud Drive/Highway 14 and 38 Ave NW, S Anthony Henday Drive and 16A Ave NW, W 34 St NW, E city limits / Henday |
| 42 | Edmonton-Nisku | B10, B11, C13, B09, X04 | near-full: four numbered Edmonton parcels with street limits (41 Ave SW, Gateway, 66 St SW, Henday, 34 St NW, 16A/15 Ave NW, 17 St NW, 50 St NW, 23 Ave NW), N roughly Henday, E city limits; Leduc County portion only "Nisku ... north of Airport Road east of Highway 2" |
| 45 | Edmonton-South | B12, C14 | near-full: W of Highway 2/Gateway Blvd, S city southern limits, N Ellerslie Rd, W Whitemud Creek; four listed transfers |
| 46 | Edmonton-Strathcona | B16, C20 | full prose ring (east edge cut off in text): S Whitemud Drive, N North Saskatchewan River, W Whitemud Creek, E Gateway Blvd / 99 St ... |
| 48 | Edmonton-Whitemud | C19 | full prose ring: S Anthony Henday Drive, N and W North Saskatchewan River, E Whitemud Creek; Rabbit Hill Road limit |
| 49 | Edmonton-Windermere | B15, C17, C18 | full prose ring: E Whitemud Creek, S city southern boundary (Highway 19 to Devon), N Anthony Henday, W North Saskatchewan River; Chappelle Gardens added |
| 52 | Banff-Canmore-Diamond Valley | C35, C36, C37 | change only: SW boundary extended along Highway 22 corridor (Longview, Diamond Valley, Millarville, Priddis, Bragg Creek) plus Bearspaw First Nation Reserve; NE adjusted for Rocky Mountain House-Sundre |
| 53 | Barrhead-Westlock-Athabasca | C07, C08, C09, X06 | change only: "roughly the same as the current" 2017 boundaries; Swan Hills and Fort Assiniboine out; Saddle Lake Cree Nation Reserve in; Smoky Lake County back in |
| 54 | Blackfalds-Innisfail | B19 | partial: surrounds Red Deer; Blackfalds, Innisfail, Penhold, Dickson Dam, Gleniffer Lake, Delburne, Elnora, Pine Lake; no Sylvan Lake, no Bowden |
| 58 | Cochrane | C31, B23, C28 | change only: Springbank leaves; West Airdrie and Rocky View portion left in the Commission map |
| 60 | Drayton Valley-Devon | B07, B08, B09, X03 | partial: Devon-Calmar-Thorsby-Warburg-Alsike-Drayton Valley along Highway 39; N edge Highway 22/16 east then Highway 759 south; E next to Edmonton airport, abutting City of Leduc; Minority: east to Highway 2 |
| 61 | Drumheller-Stettler | B20, C22, C26 | near-full prose ring (south edge unstated): W Red Deer River, E Saskatchewan border, N roads to the border NE of Provost, NW edge N-S just east of Stettler through Nevis to Buffalo Lake |
| 62 | Fort McMurray-Lac La Biche | B05, B06, C11 | full prose ring (rough): W Athabasca River, N Athabasca and Clearwater Rivers, E Saskatchewan border and Cold Lake Air Weapons Range, S south of Lac La Biche; Smoky Lake County out |
| 63 | Fort McMurray-Wood Buffalo | C11 | change only: Martin Ridge Estates and Wood Buffalo Estates (north of the Athabasca River, south of Thickwood Blvd) stay in Wood Buffalo |
| 67 | Lac Ste. Anne | B02, C01, C02, X02 | partial: Stony Plain - Onoway - Mayerthorpe along Highway 43; west edge Highway 22 north of the Yellowhead then west to take Mayerthorpe; dips south of the Yellowhead to take Lake Wabamun and the Paul reserve; composition list (Stony Plain, all Lac Ste. Anne County, Lake Wabamun, northern Parkland County) |
| 68 | Lacombe-Sylvan Lake | B18, C22, X05 | partial: Gull Lake and Bentley west, part of Buffalo Lake east, Sylvan Lake southwest; Minority gives a composition list |
| 69 | Leduc-Beaumont | C13, B09, X04 | change only: restored 2010-2017 Leduc + Beaumont pairing; Nisku and the airport-side areas go to Edmonton-Nisku |
| 71 | Lethbridge | M1, B01 | FULL RING: metes-and-bounds (M1, from Highway 3 at Westside Drive round to the point of commencement) plus prose summary (B01) |
| 72 | Lethbridge-Cardston | C33 | change only / composition: Cardston, Magrath, Raymond and Blood Reserve borrowing about 17,000 from Lethbridge; no boundary feature |
| 73 | Lethbridge-Little Bow | B26, C32, C25 | partial: N up Highways 23 and 24 (Nobleford ... Vulcan ... Arrowwood, across the Bow River and Siksika Reserve to Gleichen and Cluny); contiguous eastern and western Lethbridge portions; abuts Olds-Didsbury-Three Hills at Siksika |
| 74 | Lethbridge-Taber-Warner | B27 | partial: Highway 3 and 4 corridors east and south of Lethbridge (Coaldale, Taber, Vauxhall, Bow Island, Warner, Milk River, Coutts, Highway 61 to Foremost and Manyberries) |
| 76 | Macleod-Crowsnest | B28, C34 | near-full prose ring (south edge unstated): Highway 3 west to Crowsnest Pass, Highway 2 north to High River, Highway 22 north to Chain Lakes and the south of Kananaskis; E by the Waterton, Belly and Little Bow Rivers |
| 79 | Morinville-Sturgeon | B03, B04, C06, X06 | full prose ring (north edge cut off in text): S City of Edmonton and southern Sturgeon County border, E North Saskatchewan River, W western Sturgeon County boundary (west to parallel Highway 779), N northern Sturgeon boundary; St. Albert border moved so all St. Albert south of the Sturgeon River is in the St. Albert division |
| 80 | Okotoks | C37 | none: only that Diamond Valley is separated from Okotoks |
| 81 | Olds-Didsbury-Three Hills | C23, C24, C25 | change only: gains Bowden; loses Crossfield and Irricana to Airdrie East; SE edge extends to the Siksika Reserve; West Country parts of Mountain View County go to Rocky Mountain House-Sundre |
| 84 | Red Deer-South | (only Minority p120, p130: dispute over the Red Deer-South / Blackfalds-Innisfail border) | none |
| 85 | Rocky Mountain House-Sundre | B17, X05 | full prose ring: S meandering west along a watershed NW of Cochrane to the B.C. border, W the B.C. border north to the Brazeau River, then NE along the Brazeau River to Clearwater County's northern boundary (also the N edge), E roughly N-S just east of the Highway 22 corridor |
| 87 | Spruce Grove | C04, C05, X03 | change only: Stony Plain removed; extended north and south of Spruce Grove for population |
| 90 | West Yellowhead | C12, X03 | change only: Mayerthorpe goes back to Lac Ste. Anne; Minority: loses all of Lac Ste. Anne County |
| 91 | Wetaskiwin-Ponoka | C21 | change only: Ponoka in; NE portion (Kavanagh, New Sarepta, Hay Lakes) to Camrose |

Full ring (written): 40, 46, 48, 49, 62, 71, 79, 85. Only ED 71 has a legal-style (metes-and-bounds) ring; the others are rough compass-point prose (ED 62, 85 are the most usable) and several have one edge cut off in the text layer (46, 79).
None: 1, 80, 84.

## 4. Labels on the map pages themselves

Method: `p(215+n).txt`; labels come out in drawing order and are often split ("BOW RIVER WAT" / "BOW RIVER WATER" are fragments of a BOW RIVER WATERSHED label), so treat each as a name present on the page, not a located line. Numeric highway labels are bare numbers and are not distinguishable from other numbers in the text. Numbers that look like artifacts (e.g. TWP RD 11255, RGE RD 190521, TWP RD 28) are glued neighbours and omitted or marked.

### Five rural changed pages in detail

| ED / page | Township / range roads | Boundary and feature labels |
|---|---|---|
| 85 Rocky Mountain House-Sundre / p300 | RGE RD 43 | CLEARWATER COUNTY BOUNDARY (twice), BOW RIVER (fragments of BOW RIVER WATERSHED), BOUNDARY |
| 61 Drumheller-Stettler / p276 | TWP RD 203 | M.D. OF PROVOST BOUNDARY, RED DEER RIVER |
| 53 Barrhead-Westlock-Athabasca / p268 | TWP RD 580, TWP RD 650, (TWP RD 28 truncated); RGE RD 12 | ATHABASCA COUNTY BOUNDARY (twice), ATHABASCA COUNTY, M.D. OF ... |
| 60 Drayton Valley-Devon / p275 | TWP RD 450 | BRAZEAU COUNTY BOUNDARY, BRAZEAU COUNTY, NORTH SASKATCHEWAN RIVER |
| 91 Wetaskiwin-Ponoka / p306 | TWP RD 414, 420, 450, 480; RGE RD 10, 220, 223 | BRAZEAU COUNTY BOUNDARY, CAMROSE COUNTY BOUNDARY, LEDUC COUNTY BOUNDARY, CLEARWATER COUNTY, PONOKA COUNTY |

### All 35 changed pages (extracted label inventory)

| ED | Page | TWP RD | RGE RD | Boundary / river labels |
|---|---|---|---|---|
| 1 | p216 |  |  | BOW RIVER |
| 4 | p219 | 245 | 40, 41 | BOW RIVER |
| 22 | p237 | 254 |  | CITY OF CALGARY BOUNDARY, BOW RIVER |
| 28 | p243 |  |  | CITY OF CALGARY BOUNDARY, ELBOW RIVER |
| 33 | p248 |  |  |  |
| 40 | p255 |  |  | CITY OF EDMONTON BOUNDARY |
| 42 | p257 | 500, 502, 510 | 244, 254 | CITY OF EDMONTON BOUNDARY |
| 45 | p260 |  | 254 |  |
| 46 | p261 |  |  | (NORTH) SASKATCHEWAN RIVER |
| 48 | p263 |  |  | (NORTH) SASKATCHEWAN RIVER |
| 49 | p264 |  |  | (NORTH) SASKATCHEWAN RIVER |
| 52 | p267 | 282 |  | BOW RIVER |
| 53 | p268 | 580, 650 | 12 | ATHABASCA COUNTY BOUNDARY |
| 54 | p269 | 370, 380 | 43 | RED DEER RIVER |
| 58 | p273 | 262, 272, 280, 282 | 20, 21, 22, 23, 25, 34, 40 | BOW RIVER; a ROCKY RIDGE ... BOUNDARY fragment |
| 60 | p275 | 450 |  | BRAZEAU COUNTY BOUNDARY, NORTH SASKATCHEWAN RIVER |
| 61 | p276 | 203 |  | M.D. OF PROVOST BOUNDARY, RED DEER RIVER |
| 62 | p277 |  |  | ATHABASCA RIVER, BOUNDARY |
| 63 | p278 |  |  | WOOD BUFFALO BOUNDARY |
| 67 | p282 | 540, 560, 594 | 12, 20, 62, 100 |  |
| 68 | p283 | 370, 380, 420 | 43, 54, 55, 220 | RED DEER RIVER |
| 69 | p284 | 500, 502 | 241, 244, 254 | BEAUMONT BOUNDARY, CITY OF LEDUC BOUNDARY |
| 71 | p286 |  | 212 | CITY OF LETHBRIDGE BOUNDARY, OLDMAN RIVER |
| 72 | p287 |  | 204 | BOUNDARY |
| 73 | p288 | 556 | 250, 261 | BOW RIVER |
| 74 | p289 | 150 | 190, 204 | BOW RIVER, OLDMAN RIVER |
| 76 | p291 |  |  | (river label fragment), BOUNDARY |
| 79 | p294 | 540 | 11, 12, 210 | BOUNDARY (fragment) |
| 80 | p295 |  | 261, 271 | TSUUT'INA NATION BOUNDARY, BOW RIVER |
| 81 | p296 | 230, 250, 290, 350 (+72 uncertain) | 40, 250 (+77 uncertain) | COUNTY BOUNDARY (prefix cut), RED DEER RIVER |
| 84 | p299 | 382 | 270, 272, 273 | CITY OF RED DEER BOUNDARY (several), CTY OF RED DEER BOUNDARY |
| 85 | p300 |  | 43 | CLEARWATER COUNTY BOUNDARY, BOW RIVER (WATERSHED fragments) |
| 87 | p302 | 540 | 265, 270, 273, 275 | (SPRUCE/STONY PLAIN) GROVE BOUNDARY fragment |
| 90 | p305 |  | 100 | (WOOD)LANDS COUNTY BOUNDARY, (PEM)BINA RIVER |
| 91 | p306 | 414, 420, 450, 480 | 10, 220, 223 | BRAZEAU, CAMROSE, LEDUC COUNTY BOUNDARY |

Notes: ED 1, 33 and 45 show almost no boundary labels (urban pages; street names only). Urban pages label the city limit (CITY OF CALGARY / EDMONTON / RED DEER / LETHBRIDGE BOUNDARY) rather than roads. Rural pages add county or M.D. boundary names and the township/range road grid, which is the most useful label set for tracing a rural edge.
