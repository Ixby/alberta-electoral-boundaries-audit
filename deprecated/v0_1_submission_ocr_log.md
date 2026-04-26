# v0_1 submission OCR log

Track D of the Alberta Electoral Boundaries audit: recover the 88 submissions that lacked a text layer in the v0_1 `submission_search.py` extraction.

## Tooling

- **OCR engine:** EasyOCR 1.7.2 (CPU, English, paragraph mode, `detail=0`). Installed fresh via `pip install easyocr` which pulled in torch 2.11.0, torchvision 0.26.0, opencv-python-headless, scikit-image, and EasyOCR's detection + recognition models.
- **Page renderer:** PyMuPDF (fitz) 1.27.2 at 200 DPI.
- **Tesseract CLI check:** not installed on this Windows host. No `tesseract.exe` found in PATH or any of the standard install locations. Would have preferred Tesseract for speed but EasyOCR works without a system dependency.
- **Python:** 3.14.3 with `PYTHONIOENCODING=utf-8`.

## Missing-submission accounting

Prior text-layer extraction left these 88 submissions undetected:

- **R1 (27 missing):** 1, 2, 3, 4, 5, 6, 7, 21, 22, 23, 24, 62, 73, 111, 147, 159, 174, 183, 186, 190, 191, 192, 193, 194, 195, 196, 197.
- **R2 (61 missing):** 2, 6, 7, 10, 11, 41, 44, 54, 76, 85, 98, 102, 103, 104, 106, 129, 141, 160, 163, 227, 253, 254, 270, 358, 377, 378, 379, 430, 444, 454, 469, 477, 483, 492, 499, 524, 531, 573, 596, 602, 610, 612, 615, 616, 639, 644, 654, 673, 704, 707, 766, 810, 828, 829, 841, 966, 973, 1048, 1113, 1122, 1126.

## Approach — targeted OCR

Rather than OCR all 1,590 image-only pages in the archive, the run rendered and OCR'd only pages that fell in the **page-range gaps** between detected submissions for each PDF (i.e. where a missing ID must live). This reduced the OCR workload from ~1,590 pages to **73 targeted pages**.

Plan built by `.temp/submissions/ocr_plan.json` — for each of the 88 missing IDs, find the adjacent detected submissions' page ranges and OCR every image-only page in the gap.

## OCR run

- **Pages targeted:** 73.
- **Pages actually OCR'd before cutoff:** 53 (73%). The run was terminated at ~36 min wall clock because per-page cost on the CPU path varied widely (~10-90 s per page, with some pages stalling on large embedded photographs) and the 60-min wall-clock budget was approaching.
- **Average chars recovered per page:** 1,067.
- **Success rate:** 53/53 pages returned text (no OCR failures); quality is readable but noisy (punctuation and spacing errors are common, e.g. "OUT mission" for "our mission"; "TSG 2YS" for "T5G 2Y5"). The main keyword regex patterns still fire on place-name tokens.

## Recovery

After re-stitching pages through the existing R1/R2 ID regex on the combined text-layer + OCR text:

- **R1 recovered:** 10 of 27 missing — `[1, 2, 3, 4, 5, 6, 7, 111, 159, 183]`.
- **R2 recovered:** 4 of 61 missing — `[2, 76, 141, 469]`.
- **Total recovered:** 14 of 88 (~16%). The remaining 74 missing submissions live in pages that were in the OCR plan but were not processed before the run was cut, or in pages that sit outside the gap-window heuristic used to build the plan.

## Keyword search on recovered OCR text

Applied the same seven regex patterns from `submission_search.py`:

| configuration | OCR new hits |
|---|---|
| airdrie_4way_split | 0 |
| nolan_hill_cochrane | 0 |
| rmh_banff_park | 1 |
| olds_three_hills_didsbury | 0 |
| chestermere_split | 0 |
| red_deer_hybrids | 0 |
| st_albert_sturgeon | 0 |

One new hit-row is appended to `data/submission_search_dataset.csv` with `source = ocr` (and all prior 70 rows are marked `source = text_layer`).

### EBC-2025-2-0141 — Rocky Gas Co-Op

Board submission on behalf of the rural natural-gas co-op serving Clearwater County. Quoted verbatim from OCR (OCR noise preserved):

> "we wish to share OU concerns with the Boundary Commission'$ proposal to eliminate the Rimbey-Rocky Mountain House-Sundre constituency and divide Clearwater County between three different ridings From the local perspective, we recommend that all of Clearwater County remain in the same constituency to ensure effective representation in the Legislature."

> "the Rocky Gas Co-Op board is concerned that dividing the franchise area between three constituencies (Banff-Jasper; Lacombe-Rocky Mountain House, and Mountain View-Kneehill) will make it more challenging to advocate on behalf of our members"

> "We hope that the Boundary Commission will reconsider their draft proposal and ensure that the final electoral boundaries have all of Clearwater County and Rocky Mountain House included in the same constituency."

Position: opposes the majority's three-way split of Clearwater County; asks for Clearwater County + Rocky Mountain House to remain in a single constituency. Directionally supports an RMH-centred hybrid (aligns with the minority's s.15(2) RMH-Banff proposal in keeping RMH as a regional hub rather than dissolving it).

### Additional recovered R1 submissions with relevant content (no regex hit, but notable)

Two R1 submissions explicitly call for an **Airdrie-only urban riding** separated from rural surroundings — directionally related to the Airdrie configuration debate even though they don't trigger the 4-way split regex (which requires the word "four" or "4" near Airdrie):

- **EBC-2025-1-0001 (Rick Anderson, Airdrie):** "The population of Airdrie is projected to pass 88,000 people this year, which means it is large enough to support two electoral districts without the need to include any surrounding rural areas. Please consider creating two dedicated Airdrie ridings (i.e. Airdrie-East & Airdrie-West) and separating the rural communities from the rapidly expanding city of Airdrie." Position: supporting Airdrie as urban-only (2-way internal split, not 4-way).
- **EBC-2025-1-0002 (Aaron Holmes, Airdrie):** "Airdrie is a fast-growing city, with different needs than its surrounding rural areas. You may wish to consider aligning its representation with its municipal boundaries. That would give it a representative who could focus on Airdrie's urban concerns." Position: supporting Airdrie aligned with municipal boundaries.
- **EBC-2025-1-0111:** proposes a "Banff-Jasper-Kananaskis" mountain riding, extending east to Highway 22 only, with the area east of that folded into rural ridings around Calgary. Directionally aligned with the minority's mountain-gateway concept, not with the majority's Banff-Airdrie-East.

## Revised refutation of the chair's "no public support" claim

The prior text-layer pass already refuted the chair's claim for 6 of the 7 configurations. The OCR partial run does not change any tier:

| configuration | tier after text-layer pass | tier after OCR pass |
|---|---|---|
| rmh_banff_park | refuted (20+ text-layer hits incl. EBC-2025-2-0619 explicit s.15(2) proposal) | refuted, further supported by EBC-2025-2-0141 (Rocky Gas Co-Op, Clearwater County unity) |
| chestermere_split | refuted | refuted |
| st_albert_sturgeon | refuted | refuted |
| red_deer_hybrids | refuted | refuted |
| olds_three_hills_didsbury | refuted | refuted |
| airdrie_4way_split | weakly refuted (4 regex hits) | still weakly refuted; OCR recovered two Airdrie-only proposals (0001, 0002) that support splitting Airdrie from rural but not a 4-way split specifically |
| nolan_hill_cochrane | unrefuted (0 hits) | still 0 hits |

## Known limitations

- **53 of 73 planned pages OCR'd.** 20 pages were still queued when the CPU OCR was terminated at the wall-clock budget. The remaining pages would most likely recover more of the 61 missing R2 submissions (R2 has larger gap windows and more missing IDs than R1).
- **Gap-window heuristic may miss some submissions.** If a missing submission's pages lie outside the `(prior_detected.end_page, next_detected.start_page)` window (e.g. at the very start or end of a PDF), the plan won't include them. The recovery rate (16%) is partially bounded by this heuristic; a second pass should OCR every image-only page in each PDF, not just the gap pages.
- **OCR noise.** Character substitutions like "OUI" for "OUR", "5" read as "S", and punctuation mangling mean the existing regex patterns may miss valid hits on OCR'd text. Loosening the patterns with fuzzy matching or spell-correction on OCR output would likely surface additional hits.
- **Attached-file content.** Not addressed here; some submissions reference attached PDFs stored separately.

## What would unblock the remaining 74 submissions

- Install Tesseract (~10-15x faster than EasyOCR CPU on this workload). With Tesseract, the 20 remaining planned pages would finish in under 2 minutes.
- Extend the OCR plan to cover every image-only page in each PDF, not only the gap pages (adds ~1,500 more pages but captures PDFs where the page-range heuristic fails).
- Post-process OCR output with a spell-correction pass before running the regex patterns.

## Files produced

- `.temp/submissions/ocr_plan.json` — the 73-page OCR plan by PDF.
- `.temp/submissions/ocr_pages/*.txt` — 53 per-page OCR text files (gitignored).
- `.temp/submissions/ocr_text/EBC-2025-*.txt` — 14 recovered per-submission stitched OCR texts (gitignored).
- `.temp/submissions/ocr_analysis.json` — summary state.
- `data/submission_search_dataset.csv` — now includes a `source` column; 70 prior rows tagged `text_layer`, 1 new row tagged `ocr` (EBC-2025-2-0141).
- `analysis/scripts/submission_ocr.py` — OCR run script.
- `analysis/scripts/submission_ocr_analyze.py` — standalone analyzer that reads the OCR page files and rebuilds submission text + runs the keyword search (safe to re-run if more OCR pages arrive).

## How to reproduce

```bash
cd alberta_audit
pip install easyocr pymupdf
python analysis/scripts/submission_ocr.py          # OCR the 73 planned pages (~45-60 min CPU)
python analysis/scripts/submission_ocr_analyze.py  # Stitch + keyword search (~10 s)
```
