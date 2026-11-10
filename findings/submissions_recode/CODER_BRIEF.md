# Coder brief (stage 2)

You are one of two independent coders. Do not look at the other coder's output, at any earlier classification (`data/submission_search_dataset.csv`, sentiment CSVs), or at the audit's reports. Work only from the submission text and the codebook.

1. Read `findings/submissions_recode/CODEBOOK.md` in full. Apply it exactly.
2. Your unit file `findings/submissions_recode/units/<UNIT>.csv` lists (configuration, id, source) pairs. For each, read the WHOLE submission from `data/submissions/corpus.jsonl` (source = written) or the presenter record from `data/submissions/hansard.jsonl` (source = hearing). Where the text is OCR and unclear, or the codebook says a map page matters, open the source PDF page (the corpus builder's README says where the PDFs are) and read the image.
3. For each pair record one JSON line in `findings/submissions_recode/codes/<UNIT>_<CODER>.jsonl`:
   `{"configuration","id","source","reacts_to","wants","code","quote","page","confidence":"high|medium|low","note"}`
   using the codebook's code values. Every stance code needs a verbatim quote that appears in the text, and its page. If the submission does not actually discuss the configuration, code it as the codebook's "not mentioned".
4. Write incrementally (append every ~20 pairs) so nothing is lost. Do every pair in your unit; do not sample.
5. Do not edit any other file. Do not commit.

Final message, at most 6 lines: pairs coded, counts by code, pairs you found hard and why, and the first line of the file stamped `2026-11-10 HH:MM Alberta time · claude-fable-5-2 · medium` (write that stamp as a JSON line `{"_stamp": "..."}` at the top of your file).
