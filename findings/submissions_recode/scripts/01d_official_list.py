"""Stage 1a, side input: the commission's own lists of written submissions.

Elections Alberta posts two index PDFs (round one, round two) giving, for each
submission number, the submitter's name and affiliation. This script keeps
the number and the affiliation only (for example "Private Citizen",
"Mayor of Coaldale", "MLA for Peace River"); names are not written out.

Output CSV: id, round, number, affiliation, late (the list's "-LS" suffix),
list_note (typos in the list resolved here).

Usage: python3 -I 01d_official_list.py SRC_DIR OUT_CSV
"""
import csv
import re
import subprocess
import sys
from pathlib import Path

SRC, OUT = Path(sys.argv[1]), sys.argv[2]
FILES = [(1, "EBC-2025-List-of-Written-Submissions-Round-One.pdf", 198),
         (2, "EBC-2025-List-of-Written-Submissions-Round-Two.pdf", 1147)]
# Numbers the list prints wrongly; resolved from their position in the list.
TYPOS = {(1, 51, 0): 5, (1, 212, 0): 21, (1, 383, 0): 38}

rows = []
for rnd, name, top in FILES:
    txt = subprocess.run(["pdftotext", "-layout", str(SRC / name), "-"],
                         capture_output=True, text=True, check=True).stdout
    seen = {}
    for line in txt.splitlines():
        m = re.match(r"\s*EBC-2025-%d-(\d+)(-LS)?\s+(.*?)(?:\s{2,}(.*))?$" % rnd, line)
        if not m:
            continue
        n = int(m.group(1))
        k = seen.get(n, 0)
        seen[n] = k + 1
        note = ""
        raw = m.group(1)
        if (rnd, n, 0) in TYPOS and (n > top or (n == 51 and raw == "0051")):
            note = f"list prints EBC-2025-{rnd}-{raw}; position in the list shows it is number {TYPOS[(rnd, n, 0)]}"
            n = TYPOS[(rnd, n, 0)]
        aff = (m.group(4) or "").strip()
        if not aff and m.group(3).strip().lower().startswith("private citizen"):
            aff = "Private Citizen"
        rows.append([f"EBC-2025-{rnd}-{n:04d}", rnd, n, aff, "yes" if m.group(2) else "", note])
rows.sort(key=lambda r: (r[1], r[2]))
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "round", "number", "affiliation", "late", "list_note"])
    w.writerows(rows)
print(len(rows), "rows")
