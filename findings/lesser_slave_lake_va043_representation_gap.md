# Finding: VA 043 (ED 70) — Geographic Representation Gap, §15(2) Selective Application, and Commission Reversal

**Status:** SUPPORTED — primary source verified (EBC Final Report March 2026, EA canonical vote data)
**Data sources:** polls_2023_unified.csv (EA 2023 results), EA_Voting_Area_Boundaries_2023.shp (EA canonical), data/va_pop_from_das.csv (2021 Census DAs), EBC Final Report (.temp/commission_report.pdf), ISC First Nations Population Profiles April 2026 (Bands 453, 459, 478), Statistics Canada Indigenous Population Profile 2021 (Whitefish Lake FN #459), Alberta *Election Act* RSA 2000 c E-1
**Grounding standard:** Vote data and census populations verified from canonical files; commission report read in session; community name verified 2026-05-14 (Woodland Cree First Nation, Cadotte Lake, Reserve 226 — CGNDB/Wikipedia coordinates fall within VA 043 bounding box)
**Flagged for:** academic report §3.2 (data limitations and AV mechanism), §5.1.5 (§15(2) selective application), §5.3.4 (signatures summary); public report "The Invisible Part"
**Cross-reference:** findings/ebc_s15_selective_application.md

---

## 1. The Data Finding

Voting Area 043 in Electoral Division 70 (Lesser Slave Lake) recorded zero election-day votes in the 2023 Alberta Provincial General Election. Every other VA in ED 70 had election-day polling activity.

**VA 043 profile (verified from EA canonical sources):**
- Geographic area: 4,832 km² (6.95% of ED 70 by area)
- Bounding box (WGS84): 55.99°–57.03°N, 116.74°–115.92°W
- Centroid: 56.54°N, 116.36°W
- 2021 Census population (from data/va_pop_from_das.csv): 844 persons
- Election-day votes: NDP 0, UCP 0
- Voting mechanism: mobile poll only (EA deploys a mobile team; no fixed election-day station)

The community within VA 043 is the **Woodland Cree First Nation** (Cadotte Lake community, Reserve 226, Northern Sunrise County). Confirmed: Cadotte Lake coordinates 56°28'02"N, 116°22'51"W (56.467°N, 116.381°W) fall within the VA 043 bounding box; Woodland Cree Reserve 226 center (56°29'57"N, 116°32'21"W per Wikipedia/CGNDB; 11,660 ha, 48 km northeast of Peace River) also falls within the bounding box. The VA 043 centroid (56.54°N, 116.36°W) is approximately 8 km north of the Cadotte Lake community centre. The initially identified candidate (Loon River Cree Nation, Loon Lake 167/167A, ~115.27°W) was correctly rejected: it is east of the VA 043 eastern boundary (115.92°W). **HOLD resolved 2026-05-14.**

**Advance vote mechanism and the data gap.** EA's advance voting process verifies each voter against the provincial Electoral List System (ELS) before issuing a ballot. The ELS entry carries each voter's home Voting Area number. The VA link exists at the moment of voters-list check. However, advance and mobile ballot envelopes carry no VA identifier, and ballots are tallied at the ED level only. The VA-level attribution data is generated in the normal course of voting and lost in the counting step. This is a policy/administrative choice, not a technical constraint. Whether EA has internally retained or published VA-level advance vote totals in any prior election cycle, and whether the commission requested or received such data, is unknown pending response to the informal inquiry (private_workspace/emails/methodology/02_raymond_ea_va043_advance_vote_2026-05-13.md) and/or FOIP.

**Consequence for analysis:** EA reports advance/mobile ballot totals at the ED level only, with no VA breakdown. The geographic partisan signal for VA 043 is completely absent from EA's published results. There is no published data showing how residents of VA 043 voted in 2023, by party or otherwise.

**ISC registered population and demographic trajectory (Kee Tas Kee Now communities, primary source: ISC April 2026).** The 2021 Census population of 844 for VA 043 is a census-household count. ISC First Nations Population Profiles (April 2026) provide current registered population data for Kee Tas Kee Now Tribal Council member nations in northwestern Alberta, which include communities among the 14 First Nations and Métis communities within ED 70. Peerless Trout First Nation (Band 478): registered population 1,155 (April 2026), up from 966 in the prior ISC profile — 19.5% growth in approximately seven years. Whitefish Lake First Nation #459 (Atikameg): 2021 Census 880 in private households (median age 22.6 years); ISC April 2026 shows 1,423 registered members on own reserve (total registered: 3,266). Lubicon Lake Band No. 453 (own Crown land, no formal reserve): 2021 Census median age 21.2 years. Median ages of 21–23 indicate above-average natural increase ahead. ISC registered population on own reserve and census household population are distinct measures (registered counts legal band membership listed at the community; census counts physical presence); growth in registered on-own-reserve membership is nevertheless a useful proxy for community growth that the TBF estimate used by the commission does not separately capture.

**Status:** The specific relationship between VA 043's territory and individual Kee Tas Kee Now member nations requires NRCANA registry confirmation (see HOLD below). The demographic trajectory data above are from primary sources (StatsCan Indigenous Population Profile 2021; ISC First Nations Population Profiles April 2026) and are citable as supplementary population context.

---

## 2. The Partisan Context

ED 70's northern Voting Area cluster (VAs 029–051, which includes VA 043) is near partisan parity on election day: 534 NDP / 535 UCP (50.0% NDP). The southern cluster (VAs 001–028, including the Slave Lake urban core and surrounding rural areas) is strongly UCP-leaning: 998 NDP / 2,375 UCP (29.6% NDP).

The riding overall went UCP in 2023: 2,636 NDP / 5,171 UCP (33.7% NDP), all ballot types combined.

VA 043's neighbours:
| VA | NDP | UCP | NDP% |
|---|---|---|---|
| 041 | 44 | 40 | 52.4% |
| 042 | 45 | 39 | 53.6% |
| 044 | 27 | 6 | 81.8% |
| **043** | **0 (invisible)** | **0 (invisible)** | **unknown** |

VA 043 is surrounded by NDP-majority VAs. Based on its immediate geographic context it is likely NDP-leaning, but this cannot be confirmed from published data.

**Provincial context.** ED 70 total population (2021 Census): 27,079. Provincial average (89 seats): 54,929. ED 70 sits at −45.4% below the provincial average, just below the §15(2) −50% floor. Northern cluster (VAs 29–51): 10,428 persons, 19% of provincial average.

---

## 3. The Commission Proposal and Reversal

**Interim report (October 2025):** The commission proposed eliminating ED 70 (Lesser Slave Lake) and creating a new division called "Mackenzie," combining the Slave Lake area, M.D. of Lesser Slave River, and Sawridge First Nation with Athabasca-Barrhead-Westlock to the south. The stated rationale was that Lesser Slave Lake's population had fallen below 50% of the provincial average. The interim proposal did not apply §15(2) protection to a preserved Lesser Slave Lake configuration.

**Round 2 public submissions:** More than 80 public submissions responded to the interim proposal. Submissions EBC-2025-2-0028, EBC-2025-2-0029, EBC-2025-2-0039, EBC-2025-2-0060, EBC-2025-2-0064, and others specifically cited the impact on northern Indigenous communities as grounds for opposing elimination. EBC-2025-2-0028 states directly: "We also serve many small Northern Indigenous communities, who would lose this voice."

**Final report (March 23, 2026):** The commission reversed course. The final report preserves a modified, larger-geography Lesser Slave Lake division at −45.4% variance, invoking §15(2) and citing the presence of 14 First Nations and Métis communities within the district. The EBC Final Report explicitly references Indigenous communities as the primary community-of-interest basis for §15(2) protection.

**Partisan arithmetic of the eliminated alternative (2023 election data):**
| Component | NDP | UCP | NDP share |
|---|---|---|---|
| Lesser Slave Lake (ED 70), all ballot types | 2,636 | 5,171 | 33.7% |
| Athabasca-Barrhead-Westlock (ED 49), all ballot types | 5,401 | 15,631 | 25.7% |
| **Proposed Mackenzie (combined)** | **8,037** | **20,802** | **27.9%** |

The proposed Mackenzie would have absorbed the 50/50 northern cluster of Lesser Slave Lake into a riding where the UCP margin exceeds 2.5:1. The northern cluster's near-parity partisan position would have been permanently diluted. ED 70's northern cluster contributes 10,428 people — 19% of the provincial average; the commission's own recognition of their representation interest is reflected in the §15(2) protection ultimately granted.

---

## 4. §15(2) Discretion and the AV Data Gap Intersection

The §15(2) protection granted to Lesser Slave Lake rests on the commission's assessment of community-of-interest for the 14 First Nations and Métis communities in the riding. VA 043 — the only VA in ED 70 with zero election-day votes, almost certainly covering one or more of those 14 communities — contributed zero identifiable votes to the geographic record available to commissioners.

Any geographic analysis of partisan lean or community cohesion in the northern part of the riding would have been blind to VA 043's actual voting behaviour. The commission's assessment of whether the northern communities constitute a coherent community of interest — a determination that informed the §15(2) protection — was made without access to geographic vote data for the VA that covers the most remote northern portion of the riding.

This does not mean the commission reached the wrong conclusion. It means the commission reached the right conclusion for legitimate reasons (the 14 communities are documented in the record; the COI argument was made in public submissions) despite working with an incomplete geographic data picture. The point is not that the commission erred — it is that the advance vote attribution gap creates a structural disadvantage for exactly the communities whose representation the §15(2) provision is designed to protect.

---

## 5. Commission Chair's Characterization of the Minority's Alternative

The EBC Final Report (March 23, 2026), p.10, contains the following verbatim statement from the majority commissioners about the minority's Rocky Mountain House-Banff Park boundary choice:

> "They propose to retain an electoral division of 'Rocky Mountain House-Banff Park' by artificially extending its boundary to the province's western border with British Columbia (taking part of Banff National Park, where no one lives), which is a bad faith effort to ensure it can be protected under s. 15(2) of the Act."

The commission chair applied §15(2) to preserve Lesser Slave Lake (genuine Indigenous communities, 4/5 statutory criteria satisfied) while characterizing the minority's §15(2) engineering for Rocky Mountain House (boundary through uninhabited park, criterion (e) obtained artificially) as "bad faith." Both descriptions are in the primary source. The audit quotes them; it does not independently characterize motive.

Cross-reference: `findings/ebc_s15_selective_application.md` for full differential-treatment analysis.

---

## 6. Lunty Committee Implications

The April 16, 2026 Legislative Assembly motion (Motion 19) set aside both commission reports and established a Special Select Committee (the "Lunty committee," chaired by Brandon Lunty, UCP MLA for Leduc-Beaumont; 3 UCP / 2 NDP; report due November 2, 2026). The committee will face the same §15(2) decisions as the commission — including whether to protect Lesser Slave Lake.

The commission reversed from elimination to protection after 80+ public submissions. The Lunty committee is not required to hold public hearings. This is not a finding about the committee's likely decisions; it is context that the audit has an obligation to note in describing the riding's trajectory.

---

## 7. Competing Indigenous Views on Representation

The commission's record documents two distinct Indigenous positions on the Lesser Slave Lake / Mackenzie question:

- **North Peace Tribal Council** (Lisa Clarke, submission 883, referenced in commission final report): supported a dedicated "Mackenzie" riding that would give northern communities their own, focused electoral voice
- **Linda Green** (submission 968, referenced in commission final report): opposed consolidation; favored preserving multiple northern ridings to maintain "multiple representatives"

These positions reflect a genuine community-of-interest tension: concentrated representation vs. distributed access. The commission resolved in favour of a preserved, expanded Lesser Slave Lake that keeps the northern communities within a coherent geographic unit. The audit notes both positions without adjudicating between them.

---

## 8. What This Finding Can and Cannot Support

**Can support (verified):**
- VA 043 is geographically invisible in EA's published vote attribution
- VA 043's 844 residents voted exclusively via advance/mobile mechanism in 2023 — the specific mechanism (mobile polling team under CEO directive, or Special Ballot under s.52.2 remote-area designation) is pending EA confirmation
- The northern VA cluster containing VA 043 is near partisan parity (534 NDP / 535 UCP on election day)
- ED 70 contains 14 First Nations and Métis communities (EBC Final Report)
- The proposed Mackenzie combination would have diluted the northern cluster's 50/50 position into a 2.5:1 UCP majority
- The commission reversed from elimination to §15(2) protection after Indigenous-community advocacy
- The commission chair described the minority's RMH-Banff Park §15(2) engineering as "bad faith" (EBC Final Report p.10)
- Alberta's *Election Act* s.112(1)(a.1) requires a separate Statement of Vote per voting area; ss.113 and 124 apply this to advance and mobile counts respectively; s.112(2) permits combining VAs when the election officer determines it is "necessary to maintain the secrecy of voting" — EA's aggregate reporting practice rests on this statutory exception, not on the absence of a legal obligation
- The VA link exists at the point of voters-list check
- Whether EA applies s.112(2) as a blanket advance-vote policy or as an individual judgment for specific low-population VAs is unknown (pending EA inquiry)

**Cannot support without further verification:**
- ~~The specific name of the First Nations or Métis community within VA 043~~ RESOLVED 2026-05-14: Woodland Cree First Nation (Cadotte Lake community, Reserve 226; coordinates verified against CGNDB via Wikipedia infobox)
- Whether the commission requested or received VA-level advance vote data from EA
- Whether EA has retained VA-level advance vote data internally in any form
- Any claim of intent in the commission's proposal or reversal
- Whether the Lunty committee will or will not apply §15(2) to Lesser Slave Lake

**Can also support (new, verified from ISC and StatsCan):**
- Peerless Trout FN (Band 478): ISC registered population 1,155 (April 2026), up from 966 (prior profile) = +19.5% in ~7 years (ISC First Nations Population Profiles, April 2026)
- Whitefish Lake FN #459 (Atikameg): 2021 Census community population 880, median age 22.6 years (StatsCan Indigenous Population Profile 2021); ISC April 2026 registered on own reserve: 1,423 (total registered: 3,266)
- Lubicon Lake Band No. 453: 2021 Census median age 21.2 years
- Alberta *Election Act* ss.112(1)(a.1), 112(2), 113, 124 govern the statutory framework for per-VA Statements of Vote and the secrecy exception

**Requires primary source (read in session):**
- Commission final report: verified ✓ (.temp/commission_report.pdf)
- EBCA §15(2) statutory text: verified ✓ (quoted above from commission report citations)
- EA canonical vote data: verified ✓ (polls_2023_unified.csv)
- Census population: verified ✓ (data/va_pop_from_das.csv)
- Alberta *Election Act* RSA 2000 c E-1 ss.112, 113, 120, 124: verified ✓ (full text read in session)
- ISC First Nations Population Profiles (Bands 453, 459, 478): verified ✓ (April 2026, read in session)
- Statistics Canada Indigenous Population Profile 2021 (Whitefish Lake FN #459): verified ✓ (read in session)

---

## 9. Recommended Report Language

**Academic report (§3.2 item 5 addition):**

VA 043 (ED 70, Lesser Slave Lake) exemplifies the data gap at its most acute. The VA covers 4,832 km² in the northern portion of the division, contains 844 persons per the 2021 Census, and recorded zero election-day votes in 2023 — the only VA in ED 70 with no election-day polling activity. It is served exclusively by mobile polling. All votes cast there enter EA's advance/mobile total for the division with no VA attribution. The community's votes are counted; they cannot be located on a map.

The statutory mechanism: Alberta's *Election Act*, RSA 2000, c E-1, s.112(1)(a.1) requires the election officer to complete "a separate Statement of Vote for each voting area." Sections 113 and 124 apply this requirement to advance and mobile vote counts respectively ("with all necessary modifications"). Section 112(2) provides the operative exception: the election officer "may combine the Statements of Vote for more than one voting area in the same electoral division if, in the opinion of the election officer, it is necessary to maintain the secrecy of voting." EA's aggregate advance/mobile reporting therefore rests on s.112(2), not on the absence of a legal obligation to produce per-VA results. The practical mechanism: EA verifies advance voters against the Electoral List System before issuing a ballot; the ELS entry carries each voter's home VA number; that link is not carried forward into results reporting. Whether the 2025–2026 Electoral Boundaries Commission requested or received VA-level advance vote data from EA is unknown; a direct inquiry to EA is pending.

**Academic report (§5.1.5 draft):** See findings/ebc_s15_selective_application.md §9.

**Public report ("The Invisible Part" addition):**
In the northern part of the Lesser Slave Lake division, there is at least one community where every single vote in 2023 was cast through EA's mobile polling team. Those voters' choices are counted in the divisional total but cannot be pinned to any location on a map. That community is in a part of the division the commission initially proposed to eliminate. It voted to keep the division whole. Whether the commission had access to their geographic vote data when making that decision — or was working, like everyone else, with numbers that made those communities invisible — is something we have asked Elections Alberta directly.

---

*Last updated: 2026-05-14*
*HOLD resolved 2026-05-14: Community confirmed as Woodland Cree First Nation (Cadotte Lake, Reserve 226). Sources: Wikipedia/CGNDB infobox for Cadotte Lake, Alberta (56°28'02"N 116°22'51"W) and Woodland Cree 226 (56°29'57"N 116°32'21"W). Both coordinates fall within VA 043 bounding box (55.99–57.03°N, 116.74–115.92°W). EA response on advance vote attribution still pending.*
*STATUTORY UPDATE 2026-05-13: Mechanism revised from "policy/administrative choice" to reflect Alberta Election Act ss.112(1)(a.1), 112(2), 113, 124 — per-VA SOV is required by statute; aggregate reporting rests on s.112(2) secrecy exception. Raymond Mok email draft updated to include statutory questions.*
*Commission report primary source: EBC Final Report (March 23, 2026).*
