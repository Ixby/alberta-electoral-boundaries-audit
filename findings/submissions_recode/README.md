# Public submissions: what people asked for, read in full

2026-11-10 01:05 Alberta time · claude-opus-5-5 · medium (results); stage 1 text below: 2026-11-09 23:12 Alberta time · claude-fable-5-2 · medium

This folder replaces the audit's earlier support-and-oppose labels for public submissions. Those labels were unreliable: in a random sample, 26 of 31 were wrong (`findings/audit_2026-11-10/submissions_sample48_judgements.csv`).

## The answer

Every record was read whole: all 1,339 posted written submissions and all 349 hearing presentations, 1,688 in all. For eleven places, each reader wrote down what the person asked for, in their own words, with a quote. A script then compared each request with what each final map does there (`CODEBOOK.md`, section 5).

**Counts are records, not people.** A campaign letter sent 20 times counts 20 times. One person can appear twice, once in a letter and once at a hearing. Nobody saw either final map: people were reacting to the map in force or to the interim map, so "supports" means the request matches what a final map does, not that anyone endorsed that map.

| Place | Records naming it | Ask for what the minority drew | Ask for what the majority drew | Ask for something else | Name it, ask nothing |
|---|---:|---:|---:|---:|---:|
| Lethbridge | 226 | 38 | 93 | 13 | 64 |
| Lesser Slave Lake | 140 | 79 (both maps keep it) | 79 (both maps keep it) | 10 | 51 |
| Red Deer | 101 | 1 | 20 | 0 | 78 |
| Airdrie | 97 | 1 | 10 | 21 | 58 |
| Rocky Mountain House: the west-central riding | 95 | 46 | 10 | 2 | 46 |
| St. Albert | 78 | 20 | 22 | 3 | 46 |
| Cochrane | 68 | 0 | 7 | 1 | 56 |
| Olds: the prairie riding | 67 | 29 | 6 | 8 | 22 |
| Rocky Mountain House: Banff park | 42 | 13 | 2 | 9 | 16 |
| Chestermere | 38 | 3 | 6 | 0 | 23 |
| Olds: reach into Airdrie | 0 | 0 | 0 | 0 | 0 |

Some people argued against an arrangement without asking for anything instead. They are not in the table above. They are counted as opposed in `full_read_results.json`, under `opposes_by_rejection_only`.

The counts above include requests that give the kind of arrangement without its details. Counts for requests that describe it exactly are in `full_read_results.md`.

**Lethbridge.** Yes, there was sentiment both ways.
- 38 records ask for the city to be joined to the country around it, as the minority drew. 18 of them describe the four-way split itself.
- 10 more want some joining of city and country, but not the four-way plan.
- 93 ask for two seats inside the city, as the majority drew.
- 17 more argue against the four-way split without asking for anything else.
- In all, 111 records cut against the minority's Lethbridge arrangement, and 38 match it.

**What this says about the majority's statements.**
- **Cochrane:** no record asks for Cochrane to be joined to northwest Calgary.
- **Airdrie:** one record asks for something like the minority's split (EBC-2025-2-0852, by direction).
- **Red Deer:** one round 1 letter asks for the city to be split into "3-4 separate ridings" with nearby towns (EBC-2025-1-0045). The audit had said that no Red Deer supporter was found. On a full read, one was.
- **Chestermere:** three records ask for a link with Calgary (EBC-2025-2-0384, 0811 and 1091; only 0384 describes it exactly). Twelve cut against it.
- **The two Rocky Mountain House questions and Olds:** more people asked for what the minority drew than for what the majority drew.

**How reliable the reading is.** An earlier pass had two people code the keyword-matched records independently, with a third deciding the 72 disputes (`agreement.json`, `adjudication/`). That pass and this full read give the same stance on 1,621 of the 1,725 record–place pairs both covered (94%). The pairs that differ are listed in `full_read_results.json`. The earlier pass read long records only around keyword hits. This one read every record whole, so it is the count of record.

**What was not done.**
- Six submissions were never posted and could not be read.
- Maps attached to submissions were read from their text where possible; a few need a boundary check (`needs_geometry`).
- Readers worked alone on the full read. Only the earlier keyword pass was double coded.

## Files

| File | What it is |
|---|---|
| `CODEBOOK.md` | The places, the options for each, and how a request becomes a code |
| `FULL_READ_BRIEF.md`, `units_full/`, `codes_full/` | The full read: the brief, the 44 batches, and each reader's codes with quotes |
| `scripts/08_validate_full.py` | Checks every record was read whole and every quote is verbatim |
| `scripts/09_full_read_results.py` | Derives the codes and counts; writes `full_read_codes.csv`, `full_read_results.json`, `full_read_results.md` |
| `CODER_BRIEF.md`, `units/`, `codes/` | The earlier double coding of keyword-matched records |
| `scripts/06_merge_codes.py` | Merges the two coders; writes `merged_codes.csv`, `agreement.json`, `disagreements.csv` |
| `adjudication/` | The third reader's decisions on the 72 disputed pairs |

The rebuilt text (`data/submissions/corpus.jsonl`, `hansard.jsonl`) is not committed. It holds the full text of every submission. Scripts `02_build_corpus.py` and `03_hansard.py` rebuild it from the commission's posted PDFs.

## How the corpus was rebuilt (stage 1)

### The main result of stage 1

The earlier corpus was missing far more than the 93 submissions it was thought to lack. **It was missing the first page of 1,204 of the 1,339 posted submissions.**

The commission posted most submissions as a screenshot of the email or web form (an image, with no text layer), followed by overflow pages that do have a text layer. The earlier extraction read text layers only. For a typical web-form submission it therefore saw the end of the message and the form's footer, and not the header (who wrote, from where, about which riding) or the opening of the message. Submission EBC-2025-2-0001 is the plainest case: the letter is on page 1, an image; the earlier text for it was the closing sentence and sign-off on page 2.

| | Earlier extraction | This rebuild |
|---|---|---|
| Submissions with any text | 1,252 | 1,339 |
| Pages read | 2,244 with a text layer | 3,794 (all) |
| Characters of text | 3.46 million | 5.01 million |
| Submissions with at least twice the text they had before | | 453 |
| Submissions that had under 300 characters before and have more now | | 123 |

Every count the audit has published from keyword searches of the earlier text needs to be rerun on this corpus, not only the support and oppose labels. One example: the earlier text had 56 round 2 submissions that name Slave Lake, the same number the minority report gives ("at least 56"); this corpus has 84. Part of the difference is the form header, where a writer's current riding is recorded and which the earlier text never saw. Across both rounds the same search goes from 61 to 92 for Slave Lake, 44 to 56 for Airdrie, 17 to 22 for Chestermere, 61 to 75 for Red Deer and 48 to 66 for Rocky Mountain House.

## Counts

The commission reports 1,345 written submissions: 198 in round 1 and 1,147 in round 2 (final report p. 14).

| | Round 1 | Round 2 | Total |
|---|---|---|---|
| Counted by the commission | 198 | 1,147 | 1,345 |
| Present in the 27 posted PDFs | 196 | 1,143 | 1,339 |
| **Text recovered** | **196** | **1,143** | **1,339** |
| Not posted, so not readable | 2 | 4 | 6 |

**1,339 of 1,345 have text. Every submission that is in the posted files has been read.** Round 1 is in the four `EBC2025Submissions…ForPosting.pdf` files (numbers 1 to 197); round 2 is in the 23 `EBC-2025-2-…pdf` files (numbers 1 to 1,143).

### The six that cannot be read, and why

| ID | Reason |
|---|---|
| EBC-2025-1-0186 | On the commission's published list of submitters. Not in the posted PDF: the pages go from 185 straight to 187. |
| Round 1, one more | The commission counts 198; the posted batch ends at 197 and the published list at 189. Whatever the 198th is, it is not posted and has no number we can see. |
| EBC-2025-2-1144, 1145, 1146, 1147 | Late submissions, marked "-LS" on the published list. Not in any posted PDF; the last batch ends at 1,143. |

Only Elections Alberta can supply these.

### How the text was obtained

| Method | Pages | Submissions |
|---|---|---|
| Embedded text layer | 1,965 | 100 use nothing else |
| OCR (Tesseract 5.5, English, page rendered at 150 to 300 dpi) | 1,828 | 97 have no text layer at all; 1,142 mix OCR pages and text-layer pages |
| Read by eye from the page image | 1 | 1 (EBC-2025-1-0073, a handwritten letter) |

- **Newly recovered.** 87 submissions the earlier extraction did not have at all: 69 entirely by OCR, 15 by OCR plus text layer, 2 that had a text layer but no readable ID stamp, and 1 read by eye.
- **OCR quality.** Typed pages score 90 to 95 on Tesseract's word-confidence scale and read cleanly; the one systematic slip (capital "I" read as "|") is corrected when it stands alone. Each record carries its character-weighted confidence and a note.
- **Garbled text layers.** 33 pages had a text layer that was symbol soup (fonts embedded without a character map). They were detected and OCR'd instead. Among them are 27 pages of EBC-2025-1-0138 and all of EBC-2025-2-0273.
- **Handwriting.** One page in the whole archive (EBC-2025-1-0073). OCR scored 31 and was unusable; the page was transcribed by eye, with high confidence throughout.
- **What OCR cannot give.** 78 pages in 15 submissions are maps or tables that OCR reads badly (confidence under 75): 1-0064, 1-0101, 1-0114, 1-0142, 1-0147, 1-0155, 2-0020, 2-0067, 2-0159, 2-0236, 2-0538, 2-0746, 2-0778, 2-0809, 2-0939. The written text of each of these submissions is read; the maps themselves must be looked at in the PDF, and the codebook says when (rule 15). EBC-2025-2-0778 alone runs to 198 pages, most of them maps. A further 51 pages are blank or hold only a footer.

### Splitting pages into submissions

Each page carries the commission's ID stamp. The stamp was found by machine on 3,704 pages. 55 pages without a stamp follow a stamped page of the same submission and were assigned to it. 35 pages were assigned by eye (`scripts/manual_page_ids.json`). The split was then checked against the commission's published lists: the listed submitter's name appears in the text of all but 15 of the listed submissions, and each of the 15 was looked at (blacked-out names, organisations writing under a title, two list errors).

Things in the source a later reader should know:

- **Round 1, numbers 190 to 197** carry no stamp and are not on the published list (which stops at 189). They are the eight unstamped items at the end of the last round 1 file, numbered here in page order. The earlier extraction had folded all eight into number 189.
- **Stamps that are wrong on the page.** Number 2-0011 is stamped 012; the first page of 2-0383 is stamped 283; the last two pages of 2-0430 are stamped 429; one page of 1-0128 is stamped 127. Each was settled from the page content.
- **The published list** swaps the names for 2-0851 and 2-0852, prints three round 1 numbers wrongly (5, 21 and 38 appear as 0051, 0212 and 0383), and leaves out 2-0013, 2-0107 and 2-0524, which are in the PDFs. The stamp on the page is treated as the ID throughout.
- EBC-2025-1-0035 holds two messages from the same person, two days apart; the second is unstamped.

## Hearing testimony

The transcripts the earlier analysis classified were found: Elections Alberta posts two compilations of Alberta Hansard transcripts of the commission's public hearings beside the submissions (`2025-2026-EBC-Public-Meeting-Hansard-Round-1.pdf`, 632 pages; `…Round-2.pdf`, 449 pages). Both have a full text layer.

- 44 transcripts: numbers 1 to 28 (May and June 2025) and 32 to 45, 47 and 48 (January 2026). Numbers 29 to 31 and 46 are not in the posted compilations.
- 349 records, one per presenter per hearing (192 in round 1, 157 in round 2), in `data/submissions/hansard.jsonl`. The earlier analysis used single speaking turns as its unit; a presenter's appearance is used here so that a position stated across several answers is read whole. Commissioners' questions are kept in place.

## Files

| File | Content | Personal data |
|---|---|---|
| `data/submissions/corpus.jsonl` | One record per submission: `id`, `round`, `source_pdf`, `pages`, `method`, `text`, plus `n_pages`, `page_methods`, `ocr_mean_conf`, `confidence_note`, `affiliation`, `n_chars`. | Yes: full text. |
| `data/submissions/hansard.jsonl` | One record per presenter per hearing, same core fields plus hearing place, date and speaker. | Yes: names, as published by Hansard. |
| `data/submissions/page_map.csv` | Every page of every batch PDF: which submission it belongs to, how the ID was found, how the text was obtained, OCR confidence. | No. |
| `data/submissions/official_list.csv` | The commission's list reduced to number and affiliation ("Private Citizen", "Mayor of …"). | Offices only, no private names. |
| `findings/submissions_recode/CODEBOOK.md` | The coding scheme. | Short quotes; no private names. |
| `findings/submissions_recode/candidates.csv` | Records to read for each configuration. | No names. |
| `findings/submissions_recode/scripts/` | The pipeline, in run order, and the two small manual-fix files. | No. |

## Storage and privacy: a choice for the author

The submissions are public records. Elections Alberta publishes them with names, and each web-form submitter ticked a box acknowledging that the submission, name and municipality "may be made public". Street addresses, emails and phone numbers are blacked out in the source. Still, the full text holds about 1,170 private citizens' names with their home towns and, in places, more.

What the repository does today: it has never committed the full text (the earlier extraction lived in `.temp/`, which is git-ignored). It commits `data/submission_search_dataset.csv`, which holds IDs, page ranges and 280-character excerpts, and a results file with short quotes.

**Recommendation: keep to that practice. Do not commit `corpus.jsonl` or `hansard.jsonl`.** Commit the page map, the affiliation list, the codebook, the candidate list, the scripts and, later, the coding sheet with its short quotes. Anyone can rebuild the full text from the public PDFs with the scripts, and the page map lets them check that their rebuild splits the pages the same way. This keeps the audit reproducible without making the repository a second, searchable copy of a thousand people's letters.

To make that the default, `data/submissions/.gitignore` already excludes the two full-text files. Delete it to choose the other option. One cost of the private option should be stated: OCR output is not bit-identical across Tesseract versions, so a rebuilt corpus may differ by a character here and there, and a quote check could fail on a rebuilt copy where it passed here. If that matters more than the privacy gain, commit a hash of each record's text beside the page map, or commit the full text.

## Coding scheme and candidate pairs

`CODEBOOK.md` defines eleven elements in nine configurations, plus two context elements. For each it lists the possible arrangements and which map adopts each (in force, interim, majority, minority), with report pages and population shares from the official boundary files. The coder records what the writer is reacting to, which arrangement the writer wants, and any arrangement the writer explicitly rejects, each with a verbatim quote and page. The five codes (not mentioned; mentioned without stance; supports what the map does; opposes it; supports a third arrangement) are then derived by rule, once for the minority map and once for the majority map. Fifteen worked examples from real records are included, nine of them cases the audit found mislabelled; their quotes pass `scripts/05_verify_quotes.py`.

`candidates.csv` comes from a place-name and keyword screen that errs toward inclusion. "Core" means the configuration's own place is named; "context" means only a neighbouring place or district is.

| Configuration | Written, core | Written, context | Hearing, core | Hearing, context | Total pairs |
|---|---|---|---|---|---|
| AIRDRIE | 56 | 19 | 49 | 8 | 132 |
| COCHRANE | 41 | 17 | 40 | 9 | 107 |
| CHESTERMERE | 22 | 18 | 19 | 22 | 81 |
| REDDEER | 75 | 51 | 59 | 19 | 204 |
| RMH | 80 | 82 | 37 | 31 | 230 |
| OLDS | 19 | 59 | 19 | 24 | 121 |
| STALBERT | 78 | 5 | 54 | 6 | 143 |
| LETHBRIDGE | 179 | 24 | 63 | 13 | 279 |
| LSL | 92 | 21 | 41 | 19 | 173 |
| *Nine configurations* | | | | | *1,470* |
| HYBRID-GENERAL (context) | 407 | 159 | 124 | 39 | 729 |
| CANMORE-JASPER (context) | 126 | 72 | 46 | 18 | 262 |

The nine configurations involve 593 different written submissions and 938 written pairs, and 532 hearing pairs. These are reading lists. They are not counts of support, opposition, or even of real mentions: "Lacombe" puts a letter on the Red Deer list, and "Taber" on the Lethbridge list.

## How to rebuild

```
pip install pypdfium2 tesserocr          # tesserocr's wheel bundles Tesseract 5.5
# eng.traineddata (tessdata_fast) into TESSDATA/; the 27 batch PDFs into PDFS/;
# the two Hansard PDFs and the two list PDFs into SRC/
python3 -I scripts/01_ocr_pages.py        PDFS WORK TESSDATA
python3 -I scripts/01b_reocr_garbled.py   PDFS WORK TESSDATA
python3 -I scripts/01c_ocr_mixed_pages.py PDFS WORK TESSDATA
python3 -I scripts/01d_official_list.py   SRC data/submissions/official_list.csv
python3 -I scripts/02_build_corpus.py     WORK/pages data/submissions/corpus.jsonl data/submissions/page_map.csv data/submissions/official_list.csv
python3 -I scripts/03_hansard.py          SRC data/submissions/hansard.jsonl
python3 -I scripts/04_candidates.py       data/submissions/corpus.jsonl data/submissions/hansard.jsonl findings/submissions_recode/candidates.csv
python3 -I scripts/05_verify_quotes.py    data/submissions/corpus.jsonl data/submissions/hansard.jsonl --codebook findings/submissions_recode/CODEBOOK.md
python3 scripts/00_geometry_check.py      data/shapefiles data/census_2021/alberta_da_profile.csv
```

The batch PDFs' names and byte sizes are in `findings/submission_search_log.md`; all are under `https://www.elections.ab.ca/uploads/`. The OCR pass over all 27 files takes a few minutes on four cores.

## Limits

- One reader built the split and the manual fixes. The name check against the commission's list covers first pages; a continuation page stamped with a neighbouring number would not be caught by it unless the number ran backwards (three such pages were caught that way).
- OCR text is good, not perfect. Quotes from OCR pages should be checked against the PDF, as the codebook requires.
- `01_ocr_pages.py` records the share of each page covered by images as 0 (its page-object lookup did not work); the pages it was meant to catch were found another way by `01c_ocr_mixed_pages.py`, which found 26 pages and 2 where OCR added text.
- The option tables in the codebook state what each map does at the level a letter can speak to. They were taken from the report text and checked against the official boundaries by population overlay, not by reading every boundary description.
- The hearing parser relies on Hansard's speaker labels. A presenter whose label is unusual could be merged into the previous presenter's record; the record count equals the transcript's own participant list in 32 of 44 transcripts and differs by one or two in 9; in the other 3 (numbers 23, 42 and 43) the parser did not find the participant page, so there is nothing to compare.

## What is next (stage 2)

1. The author settles the questions below.
2. Two coders, working apart and without the old labels, code every candidate pair to `codes.csv` as the codebook sets out.
3. Run `05_verify_quotes.py --codes`; return failed quotes.
4. Compute agreement, adjudicate, derive the codes for both maps.
5. Code a random sample of 100 records the screen did not list, to measure what the screen misses.
6. Replace academic report sections 5.9.4.1, 5.9.4.6 and 5.9.4.7, public Finding 12 and the site copy that rest on the old counts. Rerun every keyword count quoted anywhere from the earlier text.

## For the author to decide

1. **Full text in the repository or not.** Recommended: not (see above). The `.gitignore` in `data/submissions/` implements that until told otherwise.
2. **Scope.** The codebook covers the nine configurations named in the brief, with CANMORE-JASPER and HYBRID-GENERAL as context elements so that letters about the interim Banff-Jasper riding and generic letters about hybrids have somewhere to go other than the wrong configuration. The minority's other edge-of-city hybrids (Bearspaw, Springbank, Tsuut'ina, De Winton, Spruce Grove, Enoch-Devon) are not covered.
3. **Whether a request in the same direction counts as support.** A letter asking for "hybrid ridings for Lethbridge" asks for the kind of thing the minority did, not for its four-way plan. The codebook records this as a match at `direction` level and requires strict and broad counts to be reported side by side. The author may prefer to report only one.
4. **The hearing unit.** One presenter's whole appearance, not single turns, so the hearing counts will not be comparable with the old 439 rows.
5. **The six unposted submissions.** Ask Elections Alberta for them, or report the base as 1,339 posted of 1,345 received.
6. **What to say now.** Until stage 2 is done, the safest statement is that the earlier submission counts and labels are withdrawn, because the text they were drawn from lacked the first page of nine submissions in ten.
