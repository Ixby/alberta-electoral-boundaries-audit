# Reserves: does each final map do what the submission asked?

Readers have already read every candidate record whole and coded what each asks about reserves, Métis settlements or nations (BRIEF.md, same folder). Your job: for each relevant record in your batch, test its request against four maps. Do not judge intent. Edit no repository file. Do not commit.

## Inputs

- Your batch: `/tmp/claude-0/-home-user-alberta-electoral-boundaries-audit/9af3a5a2-4682-51b8-9140-74f10ed8aad4/scratchpad/reserves/mapping/in_<BATCH>.jsonl` (the readers' codes: community, request, request_type, quote, page, note).
- Where every reserve (2021 census, type IRI) and Métis settlement falls on each map: `/home/user/alberta-electoral-boundaries-audit/findings/reserves_by_map/placements_all.csv` (main district per map, and any split ≥1%). Splits under 5% are edge error of the panel reconstruction or slivers; treat the place as in its main district, and say so if it matters.
- The four maps, if you need to place a town or area that is not a reserve (point in polygon with geopandas; reproject both to EPSG:3401):
  - 2019 (87 districts): `data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`, name column `EDName2017`
  - commission majority (89): `data/shapefiles/canonical/ea_majority_2026_eds.gpkg`, `EDName2025`
  - commission minority (89): `data/shapefiles/canonical/ea_minority_2026_eds.gpkg`, `EDName2025`
  - panel (91, reconstruction, provisional): `findings/a10_stepb_run/districts_real_map.gpkg`, `district`
  - towns and municipalities: `data/shapefiles/reference/alberta_2021_csds.gpkg` (`CSDNAME`, `CSDTYPE`). Paths are relative to `/home/user/alberta-electoral-boundaries-audit`.
- If you must re-read a record's text: written → `/home/user/alberta-electoral-boundaries-audit/.claude/worktrees/agent-ab4f3c8cd527d412f/data/submissions/corpus.jsonl`, hearing → `hansard.jsonl` there (`id`, `text`). Re-read when the coded request is unclear about which places are meant.

## Nations with several reserves (from the census list; check the CSV)

- Stoney Nakoda: Stoney 142, 143, 144 (Morley) and 142B; Eden Valley 216 (Bearspaw); Big Horn 144A (Wesley).
- Blackfoot Confederacy in Alberta: Siksika 146; Kainai = Blood 148, 148A; Piikani 147, Peigan Timber Limit "B".
- Maskwacis: Samson 137, 137A; Ermineskin 138; Louis Bull 138B; Montana 139; Pigeon Lake 138A is shared.
- Woodland Cree 226–228; Loon Lake 235; Peerless Trout 238; Utikoomak Lake 155, 155A (Whitefish Lake / Atikameg); Lubicon has no reserve in the 2021 census file. Lesser Slave Lake nations: Driftpile, Sucker Creek, Swan River, Sawridge, Kapawe'no. Others as named in the CSV.
- A reserve named in a record but not in the CSV: say `not_testable` with "not in the census file".
- Unpopulated parcels (population 0) matter less than populated reserves; say so where one alone decides the verdict.

## What to judge

For each map, does the map's arrangement do what the record asks?

- `meets`: the map does what is asked (for the 2019 map this just means its arrangement already matches the request).
- `does_not_meet`: it does the opposite or something else.
- `partly`: some of the places asked for are placed as asked and some are not; say which.
- `not_testable`: the request names no district arrangement that can be checked (a general principle such as "keep reserves whole", a request about the interim report's names that has no counterpart, a request with no place named), or the place is not in the file.

Rules:
- "Keep X with town Y" or "join X to Y": X's main district equals the district holding Y (town Y by its CSD; a riding name by the district on that map that holds the riding's core town). If the request names a riding from the interim report (e.g. Banff-Jasper, Mackenzie), test the arrangement it describes, not the name.
- "Keep nations together": all the named nations' populated reserves are in one district.
- "Keep in riding Z" where Z is a 2019 riding name: test whether the 2026 map keeps the reserve with the same core town as in 2019.
- "Separate": the named places are in different districts.
- A record that only opposes one district (e.g. Edmonton-West-Enoch) without saying where the place should go: test "the place is not in a district with that arrangement" and say so in `test`.
- Do not stretch. If you have to guess what is asked, use `not_testable` and say why.

## Output

Write `/tmp/claude-0/-home-user-alberta-electoral-boundaries-audit/9af3a5a2-4682-51b8-9140-74f10ed8aad4/scratchpad/reserves/mapping/out_<BATCH>.jsonl`. First line: `{"_stamp": "<YYYY-MM-DD HH:MM> Alberta time · claude-opus-5-5 · medium"}`, time from `TZ=America/Edmonton date '+%Y-%m-%d %H:%M'`. Then one line per input record, in input order, exactly these keys:

`{"id","places","test","map_2019","majority","minority","panel","reason","confidence"}`

- `places`: list of the place names as spelled in the CSV (or town names) the test used.
- `test`: one plain sentence, what you checked ("Big Horn 144A, O'Chiese 203 and Sunchild 202 in the same district as Rocky Mountain House town").
- `map_2019` … `panel`: one of `meets`, `does_not_meet`, `partly`, `not_testable`.
- `reason`: the districts each place falls in on each map, briefly, e.g. "2019: all Rimbey-RMH-Sundre; maj: Lacombe-Clearwater, RMH town in Rocky Mountain House-Sundre…". Name any district you placed by point in polygon.
- `confidence`: high | medium | low.

Write after every 10 records. Before finishing, check with a script that you have one line per input id, in order, with valid values.

Final message, at most 5 lines: records done (must equal the batch size), how many `not_testable` on every map, and the hardest records.
