# What the public asked about reserves, and which maps do it

2026-11-10 21:40 Alberta time · claude-opus-5-5 · medium

**Status: descriptive, not registered.** This file says what the submissions asked and whether each map does it. It says nothing about why any map placed a reserve where it did. The panel's map is the reconstruction (`findings/a10_stepb_run/districts_real_map.gpkg`), so its column is provisional until the official file is posted. Numbers: `submissions_counts.json` and `submissions.csv`, from `submissions.py`.

## The question

Do the public submissions support moving any of Alberta's First Nations reserves or Métis settlements into a different district?

## How it was done

1. **Screen.** A keyword screen of all 1,688 written submissions and hearing records found 630 that mention a First Nation, a reserve, a treaty, a Métis settlement, or a nation by name (`submissions_codes/candidates.csv`).
2. **Read.** AI agents read each of the 630 whole, not by keyword hit (`submissions_codes/READ_BRIEF.md`). A script checked, for each record, that the characters read equal its length and that each quote appears word for word in its text. 138 records say something about which district a reserve, settlement or nation should be in.
3. **Test.** For each of the 138, agents tested the request against the four maps, using where every reserve and settlement falls (`placements_all.csv`; `submissions_codes/MAPPING_BRIEF.md`).
4. **Check.** Two other agents checked every test (`submissions_codes/REVIEW_BRIEF.md`) and proposed 20 changes, all applied by the script (`submissions_codes/review/`).

Every step was done by AI agents (claude-opus-5-5) and checked by script and by a second agent, not by a person.

**Map verdicts.** *Meets*: the map does what was asked. *Partly*: some of the places are placed as asked, some not. *Does not meet*: it does something else. *Not testable*: the request names no arrangement a map can be checked against.

## Who asked

| Submitter | Records |
|---|---:|
| A First Nation, tribal council or similar body | 5 |
| Someone who says they belong to a nation or Métis settlement | 6 |
| Unclear | 2 |
| Anyone else (residents, MLAs, mayors, councils, groups) | 125 |
| **Total** | **138** |

**No record comes from the government of Siksika, Kainai, Piikani, the Stoney Nakoda nations, Tsuut'ina, Enoch or Saddle Lake.** The corpus's affiliation field, and a search of every record's text for a chief or council of the southern nations, find none. Some MLAs passed on what they had heard from nations (for example, Jason Nixon relaying Chief Poucette of Big Horn, EB-780). Those count as the MLA's record, not the nation's.

The five records from nations or councils:

| Record | Body | Asks | 2019 | Majority | Minority | Panel |
|---|---|---|---|---|---|---|
| EBC-2025-1-0128 (p. 75) | Fort McKay First Nation | Stay in Fort McMurray-Wood Buffalo; do not split the nation | meets | meets | meets | meets |
| EBC-2025-2-0883 (p. 75) | North Peace Tribal Council | Keep the interim Mackenzie district; do not split northern nations across ridings | partly | partly | partly | partly |
| EBC-2025-2-1100 (p. 132) | Alberta North Central Alliance | Keep Lesser Slave Lake whole; do not split Sawridge from the lakeshore nations | meets | meets | meets | meets |
| HANSARD-R2-T36-006 (EB-594) | Alberta North Central Alliance | The same, at the hearing | meets | meets | meets | meets |
| HANSARD-R2-T36-008 (EB-595) | Lesser Slave Lake Indian Regional Council | Do not split the Lesser Slave Lake constituency | meets | meets | meets | meets |

The Alliance's members are five First Nations and five municipalities. No final map has a Mackenzie district, so the North Peace request is met only in part: its four nations stay together in Peace River on every map.

## What was asked, by nation

A record counts under every group it names, so the rows add up to more than 138. The four numbers in each map's column are meets / partly / does not meet / not testable.

| Group | Records | 2019 | Majority | Minority | Panel |
|---|---:|---|---|---|---|
| Lesser Slave Lake nations and settlements | 37 | 26/6/4/1 | 29/3/4/1 | 33/0/3/1 | 29/4/3/1 |
| Enoch Cree Nation | 24 | 5/1/14/4 | 10/4/6/4 | 11/4/5/4 | 10/4/6/4 |
| Stoney Nakoda (Morley, Eden Valley, Big Horn) | 22 | 5/7/9/1 | 4/15/2/1 | 5/13/3/1 | 4/15/2/1 |
| Tsuut'ina | 16 | 2/2/10/2 | 1/6/7/2 | 6/7/1/2 | 1/6/7/2 |
| North Peace and the proposed Mackenzie district | 16 | 8/2/5/1 | 9/3/3/1 | 9/3/3/1 | 9/3/3/1 |
| O'Chiese and Sunchild | 15 | 7/3/5/0 | 7/6/2/0 | 9/6/0/0 | 7/6/2/0 |
| Saddle Lake, Whitefish Lake, Buffalo Lake, Kikino and the northeast | 15 | 4/4/7/0 | 4/5/6/0 | 11/1/3/0 | 6/6/3/0 |
| Blackfoot (Siksika, Kainai, Piikani) | 14 | 1/3/9/1 | 4/3/6/1 | 6/5/2/1 | 5/5/3/1 |
| Kee Tas Kee Now nations (Woodland Cree, Lubicon and others) | 11 | 9/0/2/0 | 9/0/2/0 | 9/0/2/0 | 9/0/2/0 |
| Fort McKay and Wood Buffalo | 9 | 3/5/1/0 | 3/5/1/0 | 8/1/0/0 | 3/6/0/0 |
| Maskwacis and Pigeon Lake | 3 | 2/1/0/0 | 3/0/0/0 | 3/0/0/0 | 3/0/0/0 |
| Alexander, Alexis, Paul (Wabamun) | 2 | 1/0/1/0 | 2/0/0/0 | 1/0/1/0 | 1/0/1/0 |
| Horse Lake and Sturgeon Lake | 1 | 0/0/1/0 | 0/1/0/0 | 0/1/0/0 | 0/1/0/0 |
| General or unnamed | 14 | 3/2/1/8 | 3/2/1/8 | 2/3/1/8 | 3/2/1/8 |

Groups are set by matching names in each record's coded community and request (`GROUPS` in `submissions.py`), so a record that names a nation in passing can land in its group. Each row lists its records in `submissions.csv`.

## The moves the 2026 maps make, and what was asked about each

**Enoch into an Edmonton district.** Every 2026 map does this; the 2019 map had Enoch in Drayton Valley-Devon. 12 records ask for it or back the interim Edmonton-West-Enoch district: "Please add the Enoch Cree Nation to the urban Edmonton ridings nearby" (EBC-2025-1-0027, p. 55). 5 oppose the mixed city-and-reserve district, among them Edmonton's Mayor Andrew Knack: it "risks a fundamental misalignment of representative concerns" (EBC-2025-2-0817, p. 82). The rest ask Enoch's own view, or make no testable request.

**Tsuut'ina into a Calgary district.** Every 2026 map does this; in 2019 Tsuut'ina shared Banff-Kananaskis with Morley. 6 records ask for Tsuut'ina in a Calgary district, 4 of them in Calgary-West (EBC-2025-2-0768, -0866, -0956, -1050). Only the minority map joins it to Calgary-West. The majority and panel maps join it to a Glenmore district. 0768 is from a member of Tsuut'ina Nation. Several others back the interim Banff-Jasper district, which kept Tsuut'ina with the Stoney reserves.

**Stoney Nakoda.** 13 records ask that the Stoney reserves be in one district. Most back the interim Banff-Jasper district, or MLA Sarah Elmeligi's ask to put "Eden Valley and Bighorn in the riding of Banff-Kananaskis, just to make sure that all of the Stoney Nation communities are in one riding" (HANSARD-R1-T13-005, EB-205). No map puts all three reserve areas in one district: 2019 used three districts, and every 2026 map uses two. The majority and panel maps join Morley and Eden Valley and leave Big Horn with Rocky Mountain House. The minority map joins Morley and Big Horn and leaves Eden Valley with Canmore. In the other direction, 7 records ask to keep O'Chiese, Sunchild or Big Horn with Rocky Mountain House, not in Banff-Jasper (e.g. HANSARD-R2-T45-004, EB-780). Every 2026 map does that: the minority map by putting Rocky Mountain House in the same district as Morley.

**The Blackfoot nations.** 2 records ask that Siksika, Kainai and Piikani be together: "should not be divided" (EBC-2025-1-0043, p. 91), and MLA Brooks Arcand-Paul, who says he is from Alexander First Nation (HANSARD-R1-T07-002, EB-113). No 2026 map does it; each puts the three in three districts. 4 records ask to undo the 2019 Cardston-Siksika district that joined Kainai and Siksika (e.g. EBC-2025-1-0183, p. 98). The 2026 maps do, wholly or in part. 3 records ask to join Kainai to a Lethbridge district (e.g. HANSARD-R2-T37-003, EB-608). The minority and panel maps do; the majority does not. 1 record asks the opposite, that the Blackfoot reserves not be joined to urban Lethbridge (EBC-2025-2-0791).

**Saddle Lake and the northeast.** 7 records ask to move Saddle Lake, or Whitefish Lake and the Buffalo Lake and Kikino settlements, into Athabasca-Barrhead-Westlock. Most come from MLA Scott Cyr and the northern MLAs' joint paper, which appears in five records (0669, 0809, 0978, 0989, 1015). The minority map moves all of them. The panel map moves Saddle Lake only. The majority map moves Saddle Lake to Fort McMurray-Lac La Biche, not to Athabasca. No nation in this group made a submission.

**Lesser Slave Lake.** 37 records, the largest group, among them the three council records above. Nearly all ask to keep the Lesser Slave Lake nations and settlements together, against the interim map's Mackenzie split. Every final map keeps them together.

## What this shows

The submissions back some of the 2026 maps' reserve moves: Enoch into Edmonton, Tsuut'ina into Calgary, and Saddle Lake into the Athabasca district. Each of these was asked for by more records than opposed it, mostly by MLAs and residents. Other moves were not asked for. No record asks to split the Blackfoot nations three ways, and the most common Stoney Nakoda request, all reserves in one district, is met by no map. The nations' own governments said almost nothing about district lines in this record. The only ones that did are northern: Fort McKay, the North Peace Tribal Council and the Lesser Slave Lake Indian Regional Council. Every map does what Fort McKay and Lesser Slave Lake asked, and does the North Peace request in part.

## Limits

- **Records, not people.** The northern MLAs' joint paper appears in five records, and some people both wrote and spoke at a hearing. Counts are of records.
- **Unreadable maps.** Some submissions attach maps whose content does not survive as text (e.g. EBC-2025-1-0101, -0114, -0142, -0146, which back a four-district Lethbridge plan). Where the text does not say where a reserve goes, the record is not counted as relevant.
- **Judgement calls.** 67 of the 138 tests are rated medium or low confidence (`test_confidence`). Records that back the interim Banff-Jasper district get *partly* or *does not meet* depending on how many of the named reserves stay apart; the reviewers flagged this as not fully consistent.
- **Places not in the files.** Lubicon Lake and the Mountain Cree Camp are not in the 2021 census reserve list; requests naming them are partly or not testable.
- **Names.** The CSV keeps the names of people who spoke at public hearings and of officeholders. Private citizens who wrote in are described, not named.

## Files

- `submissions.csv`: one row per relevant record: submitter, request, verbatim quote and page, the four map verdicts, and the test's reasoning.
- `submissions_counts.json`: the counts above, with input hashes.
- `submissions.py`: builds both from `submissions_codes/`.
- `placements_all.py`, `placements_all.csv`, `placements_all.json`: which district holds each reserve and Métis settlement on each map.
- `submissions_codes/`: the briefs, the screen, every read (all 630 records), every map test and the reviews. The full texts of the submissions are not in the repository.
