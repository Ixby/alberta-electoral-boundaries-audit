# First Nations reserves on each map, and how they voted in the 2026 referendum

2026-11-10 21:05 Alberta time · claude-opus-5-5 · high (from settings, not per-entry)

**Status: descriptive, exploratory, not registered.** This file states no conclusion about any map's intent or lawfulness. The panel's map is the reconstruction (`findings/a10_stepb_run/districts_real_map.gpkg`), so its placements are provisional until the official file is posted. Numbers: `measures.json`, from `measures.py`.

## The question

Does the panel's map split reserves out of their districts, put the Stoney Nakoda reserves in separate districts, or split the Blackfoot Confederacy?

## What the maps do

**No reserve is cut.** On all four maps, each reserve's land sits in one district. One small exception shows on the panel reconstruction: Stoney 142B, 96% in one district and 4%, unpopulated, in another. That is within the reconstruction's edge error.

**Districts holding each nation's populated reserves** (a reserve counts in the district holding most of its land):

| Nation | 2019 map | Commission majority | Commission minority | Panel (reconstruction) |
|---|---|---|---|---|
| Blackfoot Confederacy in Alberta (Siksika, Kainai, Piikani) | 2 | 3 | 3 | 3 |
| Stoney Nakoda (Morley, Eden Valley, Big Horn) | 3 | 2 | 2 | 2 |
| Tsuut'ina | 1, shared with Morley | 1, a Calgary district | 1, a Calgary district | 1, a Calgary district |

- **Blackfoot.** On the 2019 map, Siksika and Kainai shared Cardston-Siksika and Piikani was in Livingstone-Macleod. All three 2026 maps put the three nations in three different districts. The panel map does the same as both commission maps.
- **Stoney Nakoda.** The reserves go from three districts in 2019 to two on every 2026 map. The panel map puts Morley and Eden Valley together in Banff-Canmore-Diamond Valley. Big Horn, about 200 km north near Nordegg, is in Rocky Mountain House-Sundre.
- **Tsuut'ina** is a separate Dene nation. It shared Banff-Kananaskis with Morley in 2019. On all three 2026 maps it is joined to a Calgary district.

The per-reserve table, with every district share, is in `measures.json` (`placement`).

## The law

Section 14(b) of the *Electoral Boundaries Commission Act* says the commission *may* take into consideration "communities of interest, including municipalities, regional and rural communities, Indian reserves and Metis settlements" (`preregistration/terms_of_reference.md`). The wording names reserves, not nations or confederacies, and it is permissive. Section 15(2)(d) also counts a reserve inside a division as one of the criteria for a low-population division.

## How the reserves voted on Question 10

Question 10 asked whether Alberta should remain a province of Canada (option 1), or whether the government should begin the constitutional process for a binding referendum on separation (option 2). The table compares the election-day votes cast at voting places on the reserves with the election-day votes in the rest of the same 2019 division.

| Nation (voting places) | Remain | Begin process | Remain share | Rest of division, election day |
|---|---|---|---|---|
| Siksika (2 places, Cardston-Siksika) | 1,241 | 19 | 98.5% | 42.5% |
| Kainai (Kainai Multi Purpose Building, Levern, Moses Lake) | 1,286 | 17 | 98.7% | 42.5% |
| Piikani (community hall, Livingstone-Macleod) | 486 | 10 | 98.0% | 51.6% |
| Stoney Nakoda (Morley, Eden Valley, Big Horn) | 1,444 | 52 | 96.5% | 40.2% to 67.3% by division |

The rest-of-division shares are Banff-Kananaskis 67.3%, Cardston-Siksika 42.5%, Livingstone-Macleod 51.6% and Rimbey-Rocky Mountain House-Sundre 40.2%.

**What this shows.** On this one question, the reserve communities of all three Blackfoot nations and of Stoney Nakoda voted almost identically (96 to 99% remain). The neighbouring communities in their divisions split close to even, or leaned the other way. That is one measurable sign that each group of reserves shares interests that differ from those of the districts around it. It is a single referendum question, not a party vote. It says nothing about why the maps placed the reserves as they did.

## Limits

- **Locating the voting places.** The referendum's voting-area numbers do not match the 2023 voting-area polygons, so on-reserve places were picked by name. `RESERVE_PLACES` in `measures.py` gives the basis for each one. Levern and Moses Lake are communities on the Blood reserve; the Eden Valley place is Bearspaw First Nation's Sprung building, opened in May 2025.
- **Redwood House** (Banff-Kananaskis, voting areas 037 and 038) is at Redwood Meadows, a leasehold townsite on Tsuut'ina land whose residents are mostly not members. It is reported separately, not counted for Tsuut'ina: area 037 voted 97.6% remain and area 038 67.7%. No Tsuut'ina community voting place was found in this file.
- **Election day only.** Advance, mobile and special ballots are reported by voting place or for the whole division, so they cannot be placed on or off a reserve. They are left out of both sides of the comparison.
- **Electors on the list.** On-reserve turnout sometimes exceeds 100% (Kainai Multi Purpose Building: 531 ballots against 405 electors on the list). That fits a list of electors that undercounts reserve residents, who then registered at the poll. The 2021 census also gives no population for Stoney Nakoda or Tsuut'ina, which suggests those reserves were not fully enumerated.
- **The "rest of division" side** includes other First Nations' voting places: Sunchild and O'Chiese are in Rimbey-Rocky Mountain House-Sundre.

## Open next step

Whether these nations asked to be kept together can be checked against the public submissions, which were read in full (`findings/submissions_recode/`). That step has not been taken.

## Sources

- Elections Alberta, 2026 referendum official results, Question 10, poll results for divisions 50, 54, 73 and 80 (`inputs/`, SHA-256 in `measures.json`): <https://officialresults.elections.ab.ca/>
- Bearspaw First Nation, "Multipurpose building represents new chapter in Eden Valley" (2025-05-28): <https://bearspawfirstnation.ca/2025/05/28/multipurpose-building-represents-new-chapter-in-eden-valley/>
- Kainai Nation communities (Standoff, Levern, Moses Lake, Old Agency): <https://en.wikipedia.org/wiki/Kainai_Nation>
