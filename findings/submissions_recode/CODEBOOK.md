# Codebook: what the public asked for, set against each final map

2026-11-09 · stage 1 of 2 (scheme only; no submission has been coded with it yet)

This codebook tells a coder how to record what a written submission or a hearing presenter asked for on eleven questions about nine places (plus two context questions), and how that request compares with what each of the commission's two final maps does there.

## 1. Why the old labels failed, and the rule that fixes it

The old analysis asked one question of each submission: does it support or oppose "the Rocky Mountain House–Banff Park hybrid", "Chestermere merging with Calgary", and so on. An audit of 48 sampled labels found 26 of the 31 support or oppose labels wrong, many of them reversed.

The cause is timing. No member of the public ever saw either final map.

| When | What the public could react to |
|---|---|
| Round 1: written April to June 2025; hearings May 29 to June 2025 | The map in force (drawn 2017, used in 2019 and 2023). No proposal existed. |
| October 2025 | The commission's unanimous **interim** report and map. |
| Round 2: written November to December 2025; hearings January 2026 | The **interim** map. |
| March 23, 2026 | The final report: a **majority** map and a **minority** map, both new. |

So a round 2 letter that says "I oppose this riding" opposes an interim riding. The interim map dissolved Rimbey–Rocky Mountain House–Sundre; the minority map restores a riding of that kind. A letter opposing the interim plan for Rocky Mountain House is therefore, on that point, asking for what the minority later did. The old labels counted it as opposition to the minority.

**The rule.** A coder never records "support" or "oppose" directly. The coder records three things, each with a quote:

1. **What the writer is reacting to**: the map in force, the interim map, or an idea that is on no map.
2. **What the writer wants**: one of the listed arrangements for that place (section 4).
3. **Whether the writer explicitly rejects** any listed arrangement.

The support and oppose codes are then **derived** from a table of what each map does (section 5). The coder does not need to remember which map did what, and cannot reverse a label by misreading whose proposal a letter is about.

## 2. Materials

| File | What it is |
|---|---|
| `data/submissions/corpus.jsonl` | 1,339 written submissions, one record each. Page breaks are marked `[[page N]]`, where N is the page of the source PDF. |
| `data/submissions/hansard.jsonl` | 349 hearing appearances (one presenter at one hearing), from 44 transcripts. Transcript page labels are marked `[EB-N]`. Commissioners' questions are kept, with speaker labels. |
| `findings/submissions_recode/candidates.csv` | The records to read for each configuration (a keyword screen; section 7). |
| The 27 batch PDFs and 2 transcript PDFs on elections.ab.ca | The authority. When the text and the PDF differ, the PDF wins. |

Every webform submission begins with a header the commission's form produced: the writer's municipality, "What is your current electoral division?", "Which proposed electoral division are you making a submission about?", and a ticked list of issues. **The header is part of the record.** It often names the place when the message does not.

## 3. The unit and the coding sheet

The unit is one **(record, element)** pair. Most configurations are one element. Two are split in two (RMH-A and RMH-B; OLDS-A and OLDS-B) because writers routinely ask for one half and say nothing of the other.

One row per pair, in `codes.csv`:

| Column | Content |
|---|---|
| `id` | Record ID, as in the corpus. |
| `element` | Element code from section 4, for example `RMH-A`. |
| `coder` | Coder's initials or model ID. |
| `mentions` | `0` the element's place or subject does not come up; `1` it does. |
| `reacting_to` | `CURRENT` (map in force), `INTERIM`, `IDEA` (an arrangement on no map, including the writer's own), `NONE` (no stance). |
| `want` | The option code the writer asks for (section 4), or blank. |
| `rejects` | Option codes the writer explicitly argues against, separated by spaces, or blank. |
| `match_level` | `exact` the writer describes the option itself; `direction` the writer asks for that kind of arrangement without its particulars (section 6, rule 7). |
| `quote_want` | Verbatim words that show the want or the rejection. Required whenever `want` or `rejects` is filled. |
| `quote_page` | Source-PDF page of the quote (written) or `EB-N` label (hearing). |
| `quote_react` | Verbatim words showing what the writer is reacting to, if `quote_want` does not already show it. The form header counts. |
| `quote_react_page` | Page of that quote. |
| `needs_geometry` | `1` if matching the want to a map needs a boundary lookup the text cannot settle. |
| `note` | Anything a second reader needs: a fallback preference, a campaign letter, doubt about the reading. |
| `code_minority` | Derived, section 5. Leave blank; the script fills it. |
| `code_majority` | Derived, section 5. Leave blank. |

## 4. The elements

Sources for this section: the commission's final report (`evidence/commission_reports/abebc_2026_rpt_final.pdf`; "final p." is the PDF page, which equals the printed page up to p. 68; the minority report is Appendix E, PDF pp. 285 to 359, and carries its own page numbers 1 to 73 from PDF p. 287, so only PDF pages are cited for it); the interim report ("interim p." is the PDF page of the 214-page file posted by Elections Alberta, three more than the printed page number; the repository's copy, `abebc_2025_interim_report.pdf`, is a large-file pointer); and the official boundary files (`data/shapefiles/canonical/ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg`). Population shares are 2021 census dissemination areas laid over those boundaries (`scripts/00_geometry_check.py`; Airdrie figures from `data/outputs/airdrie_split_shares_2026-10-31.json`).

Each option is tagged with the maps that adopt it: **CUR** (in force), **INT** (interim), **MAJ**, **MIN**. An option with no tag is on no map.

### AIRDRIE: how the City of Airdrie is divided (74,100 residents in 2021)

The majority said the minority's Airdrie plan had no public support (final pp. 50, 59, 62). In force: Airdrie-Cochrane (west Airdrie with Cochrane) and Airdrie-East.

| Option | Arrangement | Maps |
|---|---|---|
| `A1` | Two districts centred on Airdrie, each taking in nearby Rocky View County; Crossfield and Irricana with the east one. | INT (Airdrie-East, Airdrie-West; interim p. 62). MAJ, unchanged in kind (final pp. 50, 186, 188): Airdrie-West holds 51% of the city, Airdrie-East 49%. |
| `A2` | Airdrie divided among districts that also take in north Calgary. | MIN (PDF pp. 323, 329, 339): Airdrie-East keeps 55% of the city; Calgary-Airdrie takes 24% and Calgary-Foothills-Airdrie West 21%, and Calgary residents outnumber Airdrie residents in both; Olds-Three Hills-Didsbury takes about 350 residents (0.5%). |
| `A3` | Airdrie-only districts, with no rural area and no part of Calgary. | none |
| `A4` | Keep Airdrie-Cochrane and Airdrie-East as they are. | CUR |
| `A9` | Something else (describe in `note`). | |

### COCHRANE: who Cochrane shares a district with (32,199)

| Option | Arrangement | Maps |
|---|---|---|
| `C1` | Cochrane anchors a district outside Calgary's city limits, with rural or suburban Rocky View County (Springbank, Bearspaw). | INT, MAJ (Cochrane-Springbank; interim p. 66; final p. 192). All of Cochrane. |
| `C2` | Cochrane in a district with northwest Calgary neighbourhoods. | MIN (Calgary-Nolan Hill-Cochrane, with Nolan Hill and Sage Hill; PDF pp. 322, 331). All of Cochrane. |
| `C4` | Keep Airdrie-Cochrane. | CUR |
| `C5` | Cochrane with Canmore, Banff or the mountain parks. | none |
| `C9` | Something else. | |

### CHESTERMERE: whether Chestermere shares a district with Calgary (22,163)

| Option | Arrangement | Maps |
|---|---|---|
| `H1` | All of Chestermere in a district with Strathmore and rural areas; no part of Calgary. | CUR, INT, MAJ (Chestermere-Strathmore; interim p. 65; final p. 190). |
| `H2` | Chestermere, or part of it, in a district with east Calgary. | MIN: the area south of Chestermere Boulevard and west of Rainbow Road (about 1,900 people, 9% of the city) joins Calgary-Peigan-Chestermere; the rest stays in Chestermere-Strathmore (PDF pp. 332, 341). |
| `H3` | A Chestermere-centred district without Strathmore and without Calgary (for example with Langdon or Conrich). | none |
| `H9` | Something else. | |

If a writer wants a Calgary link but objects to dividing Chestermere itself, code `want = H2`, `match_level = direction`, and say so in `note`.

### REDDEER: whether the City of Red Deer is joined to surrounding towns and country (100,844)

| Option | Arrangement | Maps |
|---|---|---|
| `R1` | Two districts wholly inside the city. | CUR, INT, MAJ (Red Deer-North 48%, Red Deer-South 52%; interim p. 75; final pp. 55, 222, 224). |
| `R2` | The city divided among four districts, each joining a slice of the city to towns and country outside it. | MIN (PDF pp. 308, 317, 350, 351): Red Deer-Blackfalds 33% of the city, Red Deer-Innisfail 32%, Red Deer-Sylvan Lake 18%, Red Deer-Lacombe 17%. Sylvan Lake and Blackfalds are each divided between two of them. |
| `R3` | Some joining of part of the city with a neighbouring town or county, but not the four-way plan (say so in `note`). | none. Codes as `R2` at `match_level = direction` only if the writer asks for city and country to share districts as a general design; otherwise leave as `R3`. |
| `R4` | More districts wholly inside the city (three). | none |
| `R9` | Something else. | |

A letter about which rural riding a town belongs in (Sylvan Lake with Innisfail or with Lacombe; Trochu with Innisfail) does not touch this element unless it says whether the town should share a district with part of the city. Code it `mentions = 1`, no want.

### RMH-A: the west-central riding

In force: Rimbey-Rocky Mountain House-Sundre. The interim map dissolved it and divided Clearwater County three ways: the town of Rocky Mountain House and the east to Lacombe-Rocky Mountain House, the area west of Highway 734 to Banff-Jasper, the south to Mountain View-Kneehill (interim pp. 38, 63, 69, 74). The commission reported strong objection (final pp. 39, 53, 54).

| Option | Arrangement | Maps |
|---|---|---|
| `W0` | Keep Clearwater County, with Rocky Mountain House, whole in one district. Nothing said about what else is in it. | MAJ and MIN both do this. |
| `W1` | A west-central, foothills district of its own: Clearwater County, Rocky Mountain House and Sundre together, along Highway 22, not joined to Lacombe or the Highway 2 corridor. Includes "keep Rimbey-Rocky Mountain House-Sundre". | CUR (with Rimbey). MIN (Rocky Mountain House-Banff Park holds all of Clearwater County, Rocky Mountain House, Sundre, Cremona and western Mountain View County; PDF pp. 351, 352). Rimbey itself goes to Wetaskiwin-Ponoka-Maskwacis on both final maps. |
| `W2` | Clearwater County whole, joined eastward with Lacombe County, the City of Lacombe and Blackfalds; Sundre elsewhere. | MAJ (Lacombe-Clearwater; Sundre in Mountain View-Kneehill; final pp. 53, 54, 216, 220). |
| `W3` | The riding dissolved and Clearwater County divided. | INT |
| `W9` | Something else. | |

### RMH-B: Banff National Park joined to the Rocky Mountain House riding

The majority called this "not a good-faith use" of section 15(2) (final p. 63) and submissions asking for it "clearly illogical" (final p. 54).

| Option | Arrangement | Maps |
|---|---|---|
| `B1` | The Rocky Mountain House riding runs through the mountains to the British Columbia border, taking in Banff National Park north of the Banff townsite and Highway 1, the MD of Bighorn and the Stoney Nakoda reserves. The towns of Banff and Canmore are not in it. | MIN, with a section 15(2) exemption (PDF pp. 351, 352). About 1,000 park residents and 1,560 in the MD of Bighorn. |
| `B2` | All of Banff National Park, Banff, Canmore, the MD of Bighorn and the Stoney Nakoda reserves in one Bow Valley district, apart from Rocky Mountain House. | MAJ (Canmore-Banff; final pp. 55, 212). |
| `B3` | Banff and Jasper parks in one district that also takes western Clearwater County. | INT (Banff-Jasper; interim p. 63). |
| `B9` | Something else, including Rocky Mountain House with the Banff townsite (say which). | |

A letter about Banff-Jasper, Canmore or Jasper that never speaks of joining park, Bighorn or Stoney lands with Rocky Mountain House or Clearwater County is **not** an RMH-B mention. It belongs under CANMORE-JASPER. This was the largest single source of wrong labels.

### OLDS-A: the prairie riding and who is in it

| Option | Arrangement | Maps |
|---|---|---|
| `O1` | An Olds-Didsbury-Three Hills riding east of Highway 22 that keeps the rural north-east of Rocky View County (Crossfield, Irricana, Beiseker) and leaves Sundre and western Mountain View County to the foothills riding. | CUR in outline. MIN (PDF pp. 319, 349): Olds, Didsbury, Carstairs, Three Hills, Trochu, Crossfield, Irricana and Beiseker all inside; 65% of Mountain View County. |
| `O2` | Mountain View and Kneehill counties whole, Sundre included; Crossfield, Irricana and Beiseker moved to Airdrie-East. | INT (Mountain View-Kneehill, also with a piece of Clearwater County; interim pp. 73, 74). MAJ (final p. 220; Sundre and Cremona in, Crossfield, Irricana and Beiseker in Airdrie-East). |
| `O9` | Something else. | |

Partial requests map as follows. "Keep Beiseker (or Irricana, or Crossfield) with Olds, not Airdrie-East" is `O1`. "Crossfield belongs with Airdrie" is `O2`. "Keep Mountain View County whole" or "Sundre with Olds" is `O2`. "Sundre belongs with Rocky Mountain House, west of Highway 22" is `O1` here and `W1` under RMH-A.

### OLDS-B: the riding's reach into Airdrie

| Option | Arrangement | Maps |
|---|---|---|
| `E1` | The Olds riding's southern edge takes in part of the City of Airdrie. | MIN: about 350 Airdrie residents on the official boundary. The minority's text does not mention it (PDF p. 349); the majority objects (final p. 62). |
| `E2` | No part of Airdrie in the Olds or Mountain View riding. | INT, MAJ |

Expect almost no mentions. Record any there are.

### STALBERT: St. Albert and Sturgeon County (68,232)

In force, and unchanged in the interim map: a St. Albert district inside the city, and Morinville-St. Albert (renamed St. Albert-Sturgeon), which joins the city north and east of St. Albert Trail and Boudreau Road to Sturgeon County east of Highway 2 (interim pp. 77, 78).

| Option | Arrangement | Maps |
|---|---|---|
| `S0` | The long-standing pattern, with no more said: one district inside the city and one city-county hybrid. | CUR, INT, MAJ, MIN |
| `S1` | As `S0`, with all of Sturgeon County united in the hybrid, the city south of the Sturgeon River moved into the St. Albert district, and Lac Ste. Anne-Parkland abolished. | MAJ (final pp. 204, 206): 83% of the city in St. Albert, 17% in the hybrid. |
| `S2` | As `S0`, with Lac Ste. Anne-Parkland kept and reaching into north-west Sturgeon County and the city's western edge, so three districts hold St. Albert residents. | MIN (PDF pp. 344, 353): 74% of the city in St. Albert, 23% in the hybrid, 4% in Lac Ste. Anne-Parkland. |
| `S3` | All of St. Albert in districts inside the city; no hybrid. | none |
| `S4` | Move a named part of the city from the hybrid into the St. Albert district (or the reverse). Set `needs_geometry = 1`. | depends on the area named |
| `S9` | Something else. | |

### LETHBRIDGE: whether the city is joined to the surrounding country (98,406)

| Option | Arrangement | Maps |
|---|---|---|
| `L1` | Two districts inside the city. | CUR, INT, MAJ (final pp. 56, 57, 254, 256; the majority adds a small piece of Lethbridge County west of the Oldman River to Lethbridge-West). |
| `L2` | The city divided in four, each quarter joined to towns and country outside it. | MIN (PDF pp. 308, 345 to 347): Lethbridge-Little Bow 34% of the city, Lethbridge-Taber-Warner 27%, Lethbridge-Fort Macleod-Crowsnest Pass 23%, Lethbridge-Cardston 17%. |
| `L3` | Some joining of city and country, but not the four-way plan (three seats, one hybrid, and so on). | none. Codes as `L2` at `match_level = direction` only if the writer asks for hybrid ridings for Lethbridge as a design. |
| `L9` | Something else. | |

### LSL: Lesser Slave Lake

| Option | Arrangement | Maps |
|---|---|---|
| `K1` | Keep or restore Lesser Slave Lake as its own northern district. | CUR. MAJ (final pp. 44, 51 to 53, 248; adds Swan Hills, the rest of Big Lakes County and part of Woodlands County; 30,011 people). MIN (PDF pp. 320, 344, 345; adds the rest of Big Lakes County, the MD of Lesser Slave River, Swan Hills and the Fort Assiniboine area). |
| `K2` | Dissolve it: most of it joined to Mackenzie County as "Mackenzie", the MD of Lesser Slave River and the Town of Slave Lake moved to Slave Lake-Westlock-Athabasca. | INT (interim pp. 39, 40, 71, 72). |
| `K9` | Something else. | |

Both final maps adopt `K1`, so on this element a request can support both.

### CANMORE-JASPER (context element)

Not one of the minority configurations the majority attacked. It is coded so that the many letters about the interim Banff-Jasper riding have a home and are not forced onto RMH-B.

| Option | Arrangement | Maps |
|---|---|---|
| `J1` | Jasper stays in West Yellowhead. | CUR, MAJ, MIN (PDF p. 354; final p. 55) |
| `J2` | Banff and Jasper in one national-parks district. | INT (interim p. 63) |
| `J3` | Banff and Canmore together in a compact Bow Valley district (with or without Kananaskis). | CUR, MAJ (Canmore-Banff; final pp. 55, 212) |
| `J4` | Banff and Canmore together in a district that runs south down the foothills to Diamond Valley, Longview and Nanton. | MIN (Canmore-Kananaskis; PDF p. 340) |
| `J5` | Canmore with the Crowsnest Pass, or another arrangement. | none |

A writer may hold `J1` and `J3` at once; write both in `want`, separated by a space.

### HYBRID-GENERAL (context element)

A stance on mixing urban and rural areas in one district **as a principle, with no place named**.

| Option | Meaning |
|---|---|
| `G-PRO` | Hybrids are good in general. |
| `G-CON` | Hybrids should be avoided in general. |
| `G-COND` | Acceptable under stated conditions. |

No support or oppose code is derived from this element for either map. Both final maps use hybrids (the majority map has 27; final p. 44), and the interim map proposed several that drew campaigns of their own. A generic letter says nothing about any one place.

### Interim arrangements that drew the most mail

Keep this list at hand. A round 2 letter that names no place is far more likely to be about one of these than about anything in the minority map.

- Beaumont divided between Leduc and Sherwood Park ridings: about 150 submissions against (final p. 39). Both final maps instead put Beaumont, whole, in an Edmonton hybrid.
- Calgary-Okotoks hybrid: a campaign against (final pp. 39, 40).
- Lesser Slave Lake dissolved into Mackenzie (final pp. 39, 51 to 53).
- Rimbey-Rocky Mountain House-Sundre dissolved, Clearwater County divided (final pp. 39, 53).
- Banff-Jasper (final pp. 39, 55).
- No added seat in south Calgary: a campaign (final pp. 39, 46).

## 5. How the codes are derived

For each row, and for each final map M (minority, then majority):

| Code | Label | Condition |
|---|---|---|
| `0` | Not mentioned | `mentions = 0`. |
| `1` | Mentions, no stance | `mentions = 1`, and both `want` and `rejects` are blank. |
| `2` | Supports what M does there | `want` is an option tagged with M. (For `S4` or any `needs_geometry` row, after the lookup.) |
| `3` | Opposes what M does there | `rejects` includes M's option; or `want` is an option tagged with the other final map and not with M. |
| `4` | Supports a third arrangement | `want` is an option tagged with neither final map (interim-only, current-only, or on no map), and `rejects` does not include M's option. |

Notes on the derivation:

- "Supports" means the request matches. It never means the writer endorsed the map, which the writer never saw.
- Where both final maps adopt the wanted option (`K1`, `W0`, `S0`, `J1`), the row is `2` for both.
- A want at `match_level = direction` still derives `2`, and analysts must report strict counts (exact only) beside broad counts (exact plus direction).
- Code `4` rows usually also cut against the minority's arrangement (someone asking for Airdrie-only seats does not want Airdrie joined to Calgary). They are kept apart from `3` because they cut against the majority's arrangement as well. Report them as their own category.
- HYBRID-GENERAL rows derive no codes.

## 6. Decision rules for hard cases

1. **Name the place or it does not count.** A stance attaches to an element only if the record names the place, names the district, or identifies it beyond doubt (a writer whose form header gives Chestermere as municipality and who writes "our city"). A letter from Edmonton saying "hybrid ridings dilute urban voices" is HYBRID-GENERAL `G-CON` and `mentions = 0` everywhere else.
2. **Use the form header.** "Which proposed electoral division are you making a submission about?" tells you the target. A one-line message, "Splitting a city in two…", under a header naming Beaumont and Leduc-Beaumont is about Beaumont.
3. **Find what they are reacting to before reading for stance.** Round 1 records react to the map in force or to ideas. Round 2 records react to the interim map unless they say otherwise. Words like "the proposed riding", "the commission's plan", "this change" refer to the interim map in round 2.
4. **Opposing an interim arrangement is not opposing the minority.** Translate the objection into a want. "Do not dissolve our riding" is a want for the riding (`W1`, `K1`). "I oppose Banff-Jasper because Jasper belongs with Hinton" is `J1`. Then let section 5 derive the codes.
5. **Supporting an interim arrangement is a want for that option.** "I am satisfied with the new Banff-Jasper division" is `J2`, which is on neither final map: code `4` for both. "The city supports the proposed Airdrie-West and Airdrie-East" is `A1`: `2` for the majority, `3` for the minority.
6. **A place named as an example is a mention, not a stance.** "Lethbridge is larger than Airdrie and St. Albert, which also have two ridings" mentions Airdrie and St. Albert (`mentions = 1`, no want).
7. **Direction and exactness.** If the writer asks for the kind of arrangement (hybrid ridings for Lethbridge; a link between Airdrie and north Calgary) without the particulars a map adopts, use the map's option with `match_level = direction`. If the writer describes the particulars (four ridings radiating from the city), use `exact`. If the writer's particulars contradict the map's (one hybrid plus two city seats), use the "some joining, not this plan" option (`R3`, `L3`) or the `9` option, and explain.
8. **Neighbouring-town letters.** A request about a town outside a city (Coaldale, Sylvan Lake, Crossfield, Beiseker) touches the city's element only if it says the town should, or should not, share a district with part of the city. Beiseker asking to stay with Olds rather than Airdrie-East is `O1` under OLDS-A, and `mentions = 1` with no want under AIRDRIE, because it says nothing about how the city is divided.
9. **One record, several elements.** Code each element on its own row. The same letter can be `W1` under RMH-A and silent under RMH-B.
10. **First preference governs.** If a writer gives a preferred arrangement and a fallback ("ideally X; failing that, Y"), code X and put Y in `note`.
11. **Explicit rejection needs words of rejection.** Fill `rejects` only when the writer argues against that arrangement itself ("Chestermere must not be attached to Calgary"). Preferring something else is not a rejection.
12. **Who is speaking.** Municipal councils, MLAs, party associations and private citizens are coded by the same rules. The submitter's affiliation is in `candidates.csv`; do not weight by it. Analysts may tabulate by it later.
13. **Campaign letters.** Code every copy. If the text matches another record nearly word for word, write `campaign` and the first matching ID in `note`.
14. **Hearing testimony.** Only the presenter's own words carry a stance. A commissioner's question is context. If a presenter answers "yes" to a commissioner's proposition, quote the question and the answer together and say so in `note`. Code a presenter's whole appearance as one record.
15. **Maps and attachments.** Many submissions attach maps that OCR cannot read. If the text refers to an attached map for the substance of the request, open the PDF page. If the map alone carries the request, code from the map, quote its caption or label, and say `from map` in `note`.
16. **When geography is beyond the text.** If the want is clear but matching it to a map needs a boundary you cannot look up (poll numbers, a road you cannot place), fill `want` with the nearest option or the `9` option, set `needs_geometry = 1`, and describe the area in `note`.
17. **Doubt.** If two careful readers could fairly disagree, choose the narrower code (`mentions = 1`, no want) and explain in `note`. A blank want is cheaper than a wrong one.

## 7. Evidence

- Every row with a `want` or a `rejects` needs `quote_want` and `quote_page`. No quote, no stance.
- Quotes are verbatim, 8 to 60 words, from the record's text. Elide only with `[…]`. Do not correct spelling.
- The quote must contain the request or the rejection itself, not the surrounding courtesy.
- For written submissions the page is the source-PDF page from the nearest preceding `[[page N]]` marker. For hearings it is the nearest preceding `[EB-N]` label; if the passage has none before the quote, give the record's PDF page range.
- OCR pages: check the quote against the PDF page when the record's `confidence_note` flags the page, and whenever a word looks wrong. Tesseract reads this typeface's capital "I" as "|"; the corpus corrects the standalone case. If you correct an OCR slip in a quote, write `ocr-corrected` in `note`.
- A script will check that each quote occurs in the record after whitespace is collapsed. Quotes that fail are returned to the coder.

## 8. Reliability

- Two coders code every candidate pair independently, without seeing the old labels or each other's rows.
- Report agreement on `mentions`, on `want`, and on the derived codes (Cohen's kappa for each), before adjudication.
- A third reader settles disagreements and records why.
- The candidate screen is not the denominator. Report counts out of the 1,339 written submissions and, separately, the 349 hearing appearances. Draw a random sample of 100 records the screen did not list for any element and code it in full, to estimate what the screen misses.

## 9. Worked examples

Real records. Page numbers are source-PDF pages. "Old label" is from `data/outputs/submission_sentiment_llm_full_results.csv` as judged in the audit sample.

**1. EBC-2025-2-0693, former mayor of Rocky Mountain House. A reversed label.**
Header: current division "80 - Rimbey-Rocky Mountain House-Sundre"; submission about "Lacombe-Rocky Mountain House; Banff-Jasper; Mountain View-Kneehill" (p. 115). Reacting to INTERIM.
- RMH-A: `want = W1`, exact. Quote (p. 117): "keeping Clearwater County, Rocky Mountain House, and other Eastern Slopes communities together in a single electoral division". Derived: minority `2`, majority `3`.
- RMH-B: `want = B1`, direction. Quote (p. 116): "Rocky has been at the center of a constituency that includes Clearwater County and western Mountain View County, extending all the way to the BC border." Derived: minority `2`, majority `3`. Note: offered as historical precedent for keeping the region whole, not as a request to add park land.
- Old label: Active Opposition to "Rocky Mountain House-Banff Park hybrid".

**2. EBC-2025-2-0409, Clearwater County resident. A reversed label.**
Reacting to INTERIM. RMH-A: `want = W1`, `rejects = W3`. Quote (p. 23): "my concerns with the decision by the commission to eliminate the Rimbey-Rocky Mountain House-Sundre riding and break up Clearwater County into three different constituencies". Derived: minority `2`, majority `3`. RMH-B: `mentions = 0`. Old label: Active Opposition.

**3. EBC-2025-2-0850, Banff-Kananaskis resident. Support for an interim riding pinned on the minority.**
Header: about "53 - Banff-Jasper" (p. 171). Reacting to INTERIM. CANMORE-JASPER: `want = J2`. Quote (p. 172): "I am satisfied with the new Banff-Jasper electoral division." Derived: `4` for both maps, since neither kept Banff-Jasper. RMH-A and RMH-B: `mentions = 0`; Rocky Mountain House is never named. Old label: Active Support for "Rocky Mountain House-Banff Park hybrid".

**4. EBC-2025-2-0896, West Yellowhead business owner.**
Reacting to INTERIM. CANMORE-JASPER: `want = J1`, `rejects = J2`. Quote (p. 105): "my concern regarding the proposal to remove the Municipality of Jasper from West Yellowhead and include it within the proposed Banff–Jasper constituency". Derived: `2` for both maps; both returned Jasper to West Yellowhead. RMH: `mentions = 0`. Old label: Active Opposition to the minority's Rocky Mountain House district.

**5. EBC-2025-1-0139, City of Airdrie, round 1. A reversed label.**
Reacting to CURRENT (Airdrie-Cochrane). COCHRANE: `want = C1`, exact. Quote (p. 165): "We would support the creation of a dedicated Cochrane electoral division that could include the Bearspaw area". Derived: majority `2`, minority `3`. Old label: Active Support for "Calgary-Nolan Hill-Cochrane hybrid". (Code AIRDRIE on its own row from the city's own maps, pp. 163 to 179.)

**6. EBC-2025-2-0671, City of Airdrie, round 2.**
Reacting to INTERIM. AIRDRIE: `want = A1`, exact. Quote (p. 51): "The City of Airdrie strongly supports the Commission's proposed creation of Airdrie-West and Airdrie-East electoral divisions". Derived: majority `2`, minority `3`.

**7. EBC-2025-2-0852, private citizen. A request of the kind the majority said nobody made (final p. 50).**
Reacting to IDEA. AIRDRIE: `want = A2`, direction. Quote (p. 6): "I respectfully urge the Commission to consider electoral boundaries that extend beyond north Calgary to include the City of Airdrie and the Balzac area of Rocky View County." Derived: minority `2`, majority `3`. Note: asks for a north Calgary and Airdrie district in general; does not describe the minority's lines. (The commission's published list gives this number another submitter's name; the stamp on the page governs.)

**8. EBC-2025-2-0811, west Chestermere resident.**
Reacting to CURRENT and INTERIM (both leave Chestermere apart from Calgary). CHESTERMERE: `want = H2`, direction. Quote (p. 66): "An MLA that represents part of Calgary and part of Chestermere would be best positioned to have the right connections in Calgary City Hall". Derived: minority `2`, majority `3`.

**9. EBC-2025-2-0787, Chestermere resident. A reversed label.**
Reacting to INTERIM, approvingly. CHESTERMERE: `want = H1`. Quote (p. 286): "my strong support for the proposed changes outlined in the Commission's interim report that maintain Chestermere's representation as a distinct and vibrant community". Derived: majority `2`, minority `3`. Old label: Active Support for "Chestermere merging with Calgary".

**10. EBC-2025-2-0467, Beaumont. A stance with no place in the message.**
Header (p. 36): municipality "Beaumont"; submission about "68 - Leduc-Beaumont". Message, entire (p. 37): "Splitting a city in two was the idea of someone in government... Did they have any brain cells.??" The header shows the city is Beaumont, which the interim map divided. Every element in this codebook: `mentions = 0`. Old label: Active Opposition to "Chestermere merging with Calgary", a place the letter never names and the interim map never divided.

**11. EBC-2025-2-0209, Beiseker resident. One letter, two elements.**
Header (p. 18): current "76 - Olds-Didsbury-Three Hills"; about "51 - Airdrie-East". Reacting to INTERIM.
- OLDS-A: `want = O1`, exact. Quote (p. 19): "I am writing to strongly oppose the proposal to place Beiseker in the new electoral division of Airdrie-East." Second quote (p. 20): "We share history, economy, schools, hospitals, and daily life with Olds, Didsbury, and Three Hills — not with the City of Airdrie." Derived: minority `2`, majority `3`.
- AIRDRIE: `mentions = 1`, no want (rule 8). Derived: `1`.
- Old label: Active Opposition to "Airdrie 4-way split".

**12. EBC-2025-2-0578, MLA for Morinville-St. Albert. Needs a boundary lookup.**
Reacting to INTERIM. STALBERT: `want = S4`, `needs_geometry = 1`. Quote (p. 75): "I am writing to suggest the relocation of polling sites 43, 44, and 45 from the Morinville-St. Albert riding to the St. Albert riding." Note: moves three polls out of the hybrid into the city district; which final map does so depends on where the polls lie. Derived after lookup. Old label: Active Support for "St. Albert merging with Sturgeon County", although the request moves territory out of the hybrid.

**13. EBC-2025-2-0870, private citizen, Lethbridge.**
Reacting to INTERIM. LETHBRIDGE: `want = L2`, direction. Quote (p. 45): "I urge the Commission to consider hybrid urban-rural ridings for more effective representation." Derived: minority `2`, majority `3`. Strict counts exclude it; broad counts include it. In the same letter Airdrie and St. Albert appear only as comparisons: `mentions = 1`, no want (rule 6).

**14. EBC-2025-2-0058, Joussard resident. Both final maps match.**
Header (p. 16): current "70 - Lesser Slave Lake"; about "72 - Mackenzie". Reacting to INTERIM. LSL: `want = K1`, `rejects = K2`. Quote (p. 16): "my concern about the proposed boundary changes that remove Joussard from the Lesser Slave Lake region and place our community into the proposed Mackenzie electoral division". Derived: `2` for both maps.

**15. HANSARD-R2-T38-005, virtual hearing, January 16, 2026. Hearing testimony, exact match.**
Reacting to INTERIM; proposing an IDEA. LETHBRIDGE: `want = L2`, exact. Quote (EB-632): "it would certainly provide four voices for the city of Lethbridge at the provincial level, it would also ensure that decisions aren’t made exclusively for Lethbridge to the detriment of the surrounding regions". Note: the answer follows a commissioner's question about "having four MLAs tied to" Lethbridge; read the whole appearance (source PDF pp. 197 to 202) for the proposal itself. Derived: minority `2`, majority `3`.

## 10. What this codebook does not do

- It does not judge whether a request was wise, only what it was.
- It does not weigh submissions. A village council and a one-line form entry are one row each.
- It does not cover Calgary's or Edmonton's internal districts, or the minority's other Calgary-edge hybrids (Bearspaw, Springbank, Tsuut'ina, De Winton) and Edmonton-edge hybrids (Spruce Grove, Enoch-Devon). Add elements in the same form if those are wanted; the candidate screen is easy to extend.
- The option tables state what each map does at the level a letter can speak to. A coder who finds a request that the tables cannot place should use the `9` option and describe it, not stretch a listed option to fit.
