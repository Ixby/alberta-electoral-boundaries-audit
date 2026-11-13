# Full-read brief (stage 4)

The author's instruction: read entire statements, not keyword hits. Every submission and every hearing record is read whole in this pass.

You are one reader. Your batch is `findings/submissions_recode/units_full/<BATCH>.csv` (columns: id, source, n_chars).

## What to do

1. Read `findings/submissions_recode/CODEBOOK.md` in full. Apply it exactly.
2. For each record in your batch, read the WHOLE text, first character to last:
   - source `written`: the record in `data/submissions/corpus.jsonl`;
   - source `hearing`: the record in `data/submissions/hansard.jsonl`.
   Print each record to yourself in pieces of at most 12,000 characters and read every piece. **Do not search for keywords. Do not skim. Do not skip a record because it looks off-topic.** A request can sit anywhere in a letter.
3. Do not look at any earlier coding (`codes/`, `merged_codes.csv`, `adjudication/`, `data/submission_search_dataset.csv`) or at the audit's reports.
4. For each record, decide for each of these eleven elements whether the writer speaks to it: `AIRDRIE`, `COCHRANE`, `CHESTERMERE`, `REDDEER`, `RMH-A`, `RMH-B`, `OLDS-A`, `OLDS-B`, `STALBERT`, `LETHBRIDGE`, `LSL`.
5. Hearing records sometimes run into the next presenter, and include commissioners' questions. Code only the named presenter's own words. An answer of "yes" to a commissioner's description counts; say so in `note`.

## What to write

Append to `findings/submissions_recode/codes_full/<BATCH>.jsonl`, one JSON object per line. Write after every 10 records so nothing is lost.

**Resuming a batch.** If the output file already exists, keep every line in it. Do not re-read records that already have a `read` line. Append your own stamp line, then continue with the records that have none.

First line of the file: `{"_stamp": "<YYYY-MM-DD HH:MM> Alberta time · <model id> · <effort>"}` (your prompt gives the model id and effort). Read the time with `TZ=America/Edmonton date '+%Y-%m-%d %H:%M'`. Do not estimate it.

**One `read` line for every record**, with exactly these keys:

`{"kind":"read","id":"…","source":"written|hearing","chars_read":12345,"read_whole":true,"asks":"one plain sentence: what this writer asks the commission for, or 'no request'"}`

`chars_read` must equal the record's length. If you could not read all of it, set `read_whole` to false and say why in `asks`.

**One `code` line for each element the record speaks to** (none for elements it does not mention), with exactly these keys, in this order:

`{"kind":"code","id":"…","source":"…","element":"LETHBRIDGE","reacts_to":"CURRENT|INTERIM|IDEA|NONE","want":"L1","rejects":"L2","match_level":"exact|direction|","needs_geometry":0,"quote":"verbatim words from the record","page":"PDF page or EB-N label","confidence":"high|medium|low","note":"…"}`

- `want`: one option code from the codebook, or `""`. `rejects`: option codes separated by spaces, or `""`.
- A place named with no request about it: `want` and `rejects` both `""`, `reacts_to` `NONE`, `quote` may be `""`.
- Every line with a `want` or a `rejects` needs a verbatim `quote` of at least 8 words where the record has that many, and its page.
- A rejection is not a want. "Do not join us to Calgary" with nothing asked for is `rejects` only.
- Do not write derived support or oppose codes. A script derives them.

When you finish, run `python3 findings/submissions_recode/scripts/08_validate_full.py <BATCH>` and fix every problem it prints.

Edit no other file. Do not commit.

Final message, at most 6 lines: records read (must equal the batch size), any not read whole and why, code lines written by element, and the records you found hardest.
