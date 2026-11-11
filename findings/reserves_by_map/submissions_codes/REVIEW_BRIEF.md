# Reserves: independent check of the map verdicts

Two earlier steps exist. Readers coded what each public record asks about reserves, Métis settlements or nations (`mapping/in_M*.jsonl`). Testers then judged, for each record, whether each of four maps does what it asks (`mapping/out_M*.jsonl`, rules in `MAPPING_BRIEF.md`). Both are in `/tmp/claude-0/-home-user-alberta-electoral-boundaries-audit/9af3a5a2-4682-51b8-9140-74f10ed8aad4/scratchpad/reserves/`. Read MAPPING_BRIEF.md first: it lists the inputs (placements CSV, map files, record texts).

Your job is to check, not redo by taste. For each record in your range, ask:
1. Does `test` faithfully state what the record asks (compare `request`, `quote`, `note`; re-read the record text where in doubt)? Is anything stretched: an unnamed place read in, a principle turned into a test?
2. Are the four verdicts right given `placements_all.csv` and the map files? Check every district name in `reason` against the CSV.
3. Is the submitter type (`submitter` in in_M*) consistent? Note: Brooks Arcand-Paul (HANSARD-R1-T07-002 and HANSARD-R2-T48-006) says in T07-002 he is from Alexander First Nation; he should be `member` in both.

Your range: records in input order across in_M1..in_M4 concatenated (138 records), numbered from 1. RANGE A = 1–69, RANGE B = 70–138.

Write `/tmp/claude-0/-home-user-alberta-electoral-boundaries-audit/9af3a5a2-4682-51b8-9140-74f10ed8aad4/scratchpad/reserves/mapping/review_<RANGE>.jsonl`: first line `{"_stamp": "<YYYY-MM-DD HH:MM> Alberta time · claude-opus-5-5 · medium"}` (time from `TZ=America/Edmonton date '+%Y-%m-%d %H:%M'`), then one line per record where you would change something, keys `{"id","field","old","new","why"}` (field is one of test, map_2019, majority, minority, panel, submitter, confidence). A record with nothing to change gets no line. Edit no repository file; do not commit; do not judge intent.

Final message, at most 5 lines: records checked, changes proposed by field, and the biggest issue.
