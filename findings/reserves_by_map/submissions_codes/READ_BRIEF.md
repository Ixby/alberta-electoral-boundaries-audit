# Reserves read: what the public asked about First Nations reserves and Métis settlements

The author asked: "take a look at the public submissions and see if they support the redistricting of any of Alberta's reserves." You read records in full and record what each says about which electoral district a First Nations reserve, a Métis settlement, or a nation's lands should be in.

## Your batch

`/tmp/claude-0/-home-user-alberta-electoral-boundaries-audit/9af3a5a2-4682-51b8-9140-74f10ed8aad4/scratchpad/reserves/batches/<BATCH>.csv` (id, source, n_chars, terms that matched a keyword screen). Text: source `written` → `/home/user/alberta-electoral-boundaries-audit/.claude/worktrees/agent-ab4f3c8cd527d412f/data/submissions/corpus.jsonl`; `hearing` → `.../hansard.jsonl` in the same folder (field `text`).

## Read every record whole

Print each record to yourself in pieces of at most 12,000 characters and read every piece. Do not search for keywords inside it and skip the rest. The keyword screen only found candidates; many hits are land acknowledgements ("Treaty 6 territory"), the word "reserve" in another sense, or a passing mention. A hearing record may run into the next presenter, and includes commissioners' questions: code only the named presenter's own words; an answer of "yes" to a commissioner's description counts (say so).

## What to record

Write `/tmp/claude-0/-home-user-alberta-electoral-boundaries-audit/9af3a5a2-4682-51b8-9140-74f10ed8aad4/scratchpad/reserves/codes/<BATCH>.jsonl`. First line: `{"_stamp": "<YYYY-MM-DD HH:MM> Alberta time · claude-opus-5-5 · medium"}` with the time from `TZ=America/Edmonton date '+%Y-%m-%d %H:%M'`. Write after every 10 records.

One line per record, exactly these keys in this order:
`{"id","source","chars_read","read_whole","submitter","submitter_note","relevant","community","request","request_type","quote","page","confidence","note"}`

- `chars_read`: must equal the record's length; `read_whole`: true, or false with the reason in `note`.
- `submitter`: `nation_or_council` (a First Nation, tribal council, Métis settlement council, Métis Nation of Alberta or similar body, or someone speaking on its behalf: chief, councillor, staff), `member` (an individual who says they are a member of a nation or a Métis settlement), `non_member` (anyone else), `unknown`.
- `submitter_note`: who, in a few words (e.g. "Chief, Siksika Nation"; "resident of Cochrane").
- `relevant`: true only if the record says something about which district a reserve, Métis settlement, or nation's lands should be in, or about keeping communities of one nation (or several nations) together or apart. False for land acknowledgements, passing mentions, other senses of "reserve", and general statements about Indigenous representation that name no district arrangement. General statements about Indigenous representation (e.g. "northern ridings must stay because of First Nations") can be relevant if they ask for a district arrangement; then say so.
- `community`: the reserve(s), nation(s) or settlement(s) the request is about, as named in the record (e.g. "Siksika Nation", "Stoney Nakoda (Eden Valley, Big Horn)", "Tsuut'ina", "Woodland Cree, Lubicon"); "" if not relevant.
- `request`: one plain sentence: what they ask, e.g. "keep Siksika with Strathmore-Brooks", "put Eden Valley and Big Horn with Morley in Banff-Kananaskis", "keep the Blackfoot nations in one district", "do not move O'Chiese and Sunchild out of the Rocky Mountain House riding", "no request".
- `request_type`: `keep_with` | `join_to` | `keep_nations_together` | `separate` | `other` | `none`.
- `quote`: verbatim words from the record (at least 8 words where the record has them) that show the request; `page`: PDF page (written) or EB-N label (hearing). Empty only if `request_type` is none.
- `confidence`: high | medium | low. `note`: anything a second reader needs.

Do not judge which final map does what they ask; the lead does that. Do not judge intent. Edit no repository file. Do not commit.

## Before you finish

Check with a script that every record in your batch has one line, `chars_read` equals the record's length, and every non-empty quote appears in the record text (whitespace-collapsed, case-insensitive).

Final message, at most 5 lines: records read (must equal the batch size), how many relevant, how many relevant by `nation_or_council`, and the records you found hardest.
