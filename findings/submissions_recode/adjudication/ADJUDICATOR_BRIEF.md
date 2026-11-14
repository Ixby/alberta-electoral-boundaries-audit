# Adjudicator brief (stage 3)

Two coders read each record independently and disagreed on the stance. You are the third reader. You decide each disputed pair from the record itself.

1. Read `findings/submissions_recode/CODEBOOK.md` in full.
2. Your list is `findings/submissions_recode/adjudication/disputes_part<N>.json`. Each entry gives the element, the record id, and what each coder recorded (want, rejects, note, quote).
3. For each entry, read the WHOLE record: `data/submissions/corpus.jsonl` (written) or `data/submissions/hansard.jsonl` (hearing). Do not decide from the coders' notes alone. Where a coder says the request is on a map, open the PDF page and look.
4. Decide `mentions`, `want`, `rejects` and `match_level` by the codebook. Do not fill derived codes; a script derives them.

Rules for the recurring disputes:
- **A rejection is not a want.** "Do not join us to Calgary" with nothing asked for is `rejects` only, `want` blank. If the writer also asks to stay as they are, or to keep the current riding, `want` is the option that describes the current arrangement.
- **A want needs the writer's own words about this element.** A general objection to an interim riding becomes a want only where codebook section 6 says it does. If the reading needs a step the writer did not take, leave `want` blank and say so.
- **Campaign letters get one code.** Where several records carry the same text, decide once, apply it to all of them, and say which ids you treated as copies.
- **Hearing records** sometimes run into the next presenter. Code only the named presenter's words.
- If the record cannot settle it, say so: set `unresolved` to true and give both readings. Do not force a call.

Write one JSON line per entry to `findings/submissions_recode/adjudication/part<N>.jsonl`:
`{"element","id","source","mentions","want","rejects","match_level","quote","page","sided_with":"A|B|neither","unresolved":false,"read_scope":"whole|...","reason"}`

The quote must be verbatim from the record. First line of the file: `{"_stamp": "<YYYY-MM-DD HH:MM> Alberta time · claude-fable-5-2 · medium"}`, with the time read from `TZ=America/Edmonton date '+%Y-%m-%d %H:%M'`.

Edit no other file. Do not commit. Final message, at most 8 lines: entries decided, how many sided with A, B, neither, how many unresolved, and anything in the codebook that needs a rule it lacks.
