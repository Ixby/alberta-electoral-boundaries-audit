"""Split every record (written and hearing) into batches for the full-read pass.

Entry: 2026-11-09 23:37 Alberta time · claude-fable-5-2 · medium

Every record is in exactly one batch. Batches hold about 230,000 characters so
one reader can read each record whole. Order is fixed (by id), so a rerun gives
the same batches.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))
LIMIT = 230_000

recs = []
for name, source in (("corpus", "written"), ("hansard", "hearing")):
    for line in open(os.path.join(ROOT, "data", "submissions", name + ".jsonl"),
                     encoding="utf-8"):
        r = json.loads(line)
        recs.append((source, r["id"], len(r.get("text") or "")))
recs.sort(key=lambda t: (t[0] != "written", t[1]))

batches, cur, size = [], [], 0
for source, rid, n in recs:
    if cur and (size + n > LIMIT or cur[0][0] != source):
        batches.append(cur)
        cur, size = [], 0
    cur.append((source, rid, n))
    size += n
if cur:
    batches.append(cur)

out = os.path.join(HERE, "units_full")
for i, b in enumerate(batches, 1):
    with open(os.path.join(out, f"F{i:02d}.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "source", "n_chars"])
        for source, rid, n in b:
            w.writerow([rid, source, n])
print(len(recs), "records in", len(batches), "batches")
for i, b in enumerate(batches, 1):
    print(f"F{i:02d}", b[0][0], len(b), sum(x[2] for x in b))
