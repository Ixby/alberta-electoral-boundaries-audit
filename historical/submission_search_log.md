# submission_search technical log

## Phase 1 — Recon

- Verified 27 batch PDF URLs with GET (HEAD returns 403 on `elections.ab.ca/uploads/`).
- Round 1 filename pattern: `EBC2025Submissions{start}-{end}ForPosting.pdf`.
- Round 2 filename pattern: `EBC-2025-2-{start:03d}-to-{end:03d}.pdf` (hyphens, not spaces as the prompt suggested).
- Total archive size: **347.8 MB** across 27 PDFs.
- `pdfplumber 0.11.9` installed and working against Python 3.14.3.
- First R1 file: 107 pages, of which 62 (58%) have <50 chars of extractable text — a substantial portion of R1 submissions are scanned images.
- First R2 file: 118 pages, 89,896 chars extractable, 52 zero-char pages — mostly attached images; primary webform text is machine-readable with explicit "EBC-2025-2-NNN" IDs.

## Phase 2 — Download

- Downloaded all 27 PDFs to `.temp/submissions/`. All 200 responses, no failures.
- Largest single file: `EBC-2025-2-751-to-800.pdf` at 94 MB.
- Total on-disk footprint: ~348 MB. Correctly gitignored under `.temp/`.

## Phase 3 — Parse

Per-batch detected-submission counts (from `pdfplumber` text extraction + ID-regex splitting):

| Batch | Detected | Expected |
|---|---|---|
| R1 1-50 | 39 | 50 |
| R1 51-100 | 48 | 50 |
| R1 101-150 | 48 | 50 |
| R1 151-197 | 35 | 47 |
| R1 total | **170** | 197 |
| R2 all 23 batches | **1082** | 1143 |
| **Total** | **1252** | **1340** |

Coverage: **93.4%** of submissions extracted with parseable text. Missing submissions are primarily those with image-only scans lacking an EBC-2025-X-NNN text-layer marker.

Notable pdfplumber warnings during parse: "Could not get FontBBox from font descriptor because None cannot be parsed as 4 floats" (benign; does not affect text extraction).

R1 id-pattern initially used "Submission #N" which didn't match the actual "EBC 2025-1-NNN" / "EBC-2025-1-NNN" format in the PDFs. Fixed the R1 regex to match both variants (with/without hyphen, with/without spaces), which increased R1 detected submissions from near-zero to 170.

## Phase 4 — Keyword search

Regex patterns built for seven configurations:

- `airdrie_4way_split` — variants of "airdrie near four/4/split/divide"
- `nolan_hill_cochrane` — "nolan hill" within 200 chars of "cochrane"
- `rmh_banff_park` — "rocky mountain house" near "banff/national park/park"
- `olds_three_hills_didsbury` — olds/didsbury/three hills near airdrie
- `chestermere_split` — chestermere near split/divid/calgary/peigan/forest lawn
- `red_deer_hybrids` — red deer near blackfalds/innisfail/sylvan lake/lacombe
- `st_albert_sturgeon` — st. albert near sturgeon

Second pass result:
```
[search] files_searched=1252 rows_with_hits=70
chestermere_split:        13
st_albert_sturgeon:       11
airdrie_4way_split:        4
red_deer_hybrids:         23
olds_three_hills_didsbury: 5
rmh_banff_park:           20
nolan_hill_cochrane:       0
```

Sanity check confirmed zero hits are correct:
- "airdrie" appears in 44 submissions; "nolan" in 5; "nolan hill AND cochrane" co-occurrence: 0.
- "airdrie" near "four/4" within 300 chars: 10 submissions, but none explicitly propose a 4-way split. The matches are incidental (list numbering, population percentages, etc.).
- Manual review confirmed **EBC-2025-2-1017** explicitly OPPOSES dividing Airdrie at all.

## Phase 5 — Manual review & findings

Manually reviewed all 70 row-hits against their full text in `.temp/submissions/text/`. Key discoveries:

1. **EBC-2025-2-0619** ("Appropriate Political Representation for Alpine Alberta") contains a detailed section titled **"3.2 Proposed Electoral Division Amendment 2: Rocky Mountain House-Banff"** — a direct explicit proposal matching the minority's s.15(2) configuration. This is the single strongest counter-example to the chair's claim.
2. Multiple Clearwater-County-area submissions (0091, 0095, 0555, 1029) align directionally with an RMH-Banff-gateway hybrid.
3. Beiseker submissions (0209 Balson, 0161 Ledoyen) explicitly support preserving an Olds-Didsbury-Three Hills-style rural riding rather than the majority's dissolution into Airdrie-East.
4. Red Deer City Councillor submission (0252 Krahn) proposes a Sylvan-Lake-Lacombe-Blackfalds northern hybrid aligned with minority's approach. Sylvan Lake business owner (0266 Mackenzie) proposes Sylvan Lake + Lacombe pairing.
5. Chestermere opposition to Calgary merger (0687, 0785, 0787) aligns with minority's preservation of Chestermere as separate.

## Output files

- `data/submission_search_dataset.csv` — 70 hit rows + 1 summary row. Columns as specified in the task prompt. Summary row stores per-configuration counts in the `mentions_*` integer fields.
- `analysis/reports/submission_search_findings.md` — written verdict.
- `analysis/scripts/submission_search.py` — reproducible pipeline.
- `.temp/submissions/submission_meta.json` — start_page / end_page / source_file per submission id.
- `.temp/submissions/search_result.json` — intermediate dump of all hits with snippets.
- `.temp/submissions/text/EBC-2025-*.txt` — 1,252 per-submission text files (gitignored).

## Known limitations

- **OCR not performed.** ~88 submissions (6.6%) have image-only content. A sampled OCR pass was deemed out-of-scope for this task; the chair's claim is already refuted by text-layer evidence alone.
- **Position classifier is heuristic** and was manually reviewed/overridden in the findings write-up for key submissions. CSV rows may show auto-classified `neutral` for submissions that on reading are supporting or opposing (e.g., EBC-2025-2-0619 is auto-classified neutral but is in fact an explicit supporting proposal).
- **Keyword patterns may miss paraphrases** that don't use the specific place-name co-occurrences the regexes test for.
- **Attached files not searched.** Some submissions reference attached PDFs (e.g., EBC-2025-1-0139 references "Airdrie-Feedback-Submission-AEBC-May-2025.pdf"). Only the enclosing batch-PDF text layer was searched.

## How to reproduce

```bash
cd alberta_audit
python analysis/scripts/submission_search.py --phase=download   # ~5 min
python analysis/scripts/submission_search.py --phase=parse      # ~2 min
python analysis/scripts/submission_search.py --phase=search     # <30 sec
```

All outputs land in `data/`, `analysis/`, and `.temp/submissions/`.
