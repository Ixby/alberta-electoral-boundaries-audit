"""Stage 1c: public-hearing testimony (Alberta Hansard transcripts of the
commission's public hearings) as one record per presenter per hearing.

Source: the two transcript compilations Elections Alberta posts beside the
written submissions (round 1: May-June 2025; round 2: January 2026).
Text comes from the PDFs' text layer (pdftotext, reading order).

A record is everything one presenter said at one hearing. It is built from
"passages": a passage opens when the presenter speaks and runs until another
member of the public speaks, so the commissioners' questions stay in place
(speaker labels kept) and the answers can be read in context. Commission
members and staff never open a passage. Hansard page labels are kept in the
text as "[EB-123]" so quotes can be cited by transcript page.

Usage: python3 -I 03_hansard.py SRC_DIR OUT_JSONL
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
FILES = [(1, "2025-2026-EBC-Public-Meeting-Hansard-Round-1.pdf"),
         (2, "2025-2026-EBC-Public-Meeting-Hansard-Round-2.pdf")]
COMMISSION = {"The Chair", "The Acting Chair", "Justice Miller", "Mr. Clark",
              "Mr. Evans", "Dr. Martin", "Mrs. Samson", "Ms Samson",
              "Mr. Roth", "Mr. Massolin", "Ms Dean", "Mr. Chair"}
TITLED = re.compile(
    r"^((?:The (?:Acting )?Chair)|(?:(?:Mr\.|Ms|Mrs\.?|Miss|Dr\.|Member|Chief|"
    r"Grand Chief|Mayor|Reeve|Councillor|Hon\.|Elder|Justice|Rev\.|Father|"
    r"Pastor|Sgt\.|Col\.|Prof\.) [A-Z][\w’'\-]*(?: [A-Z][\w’'\-\.]*){0,3})"
    r"|(?:An? (?:Hon\. )?(?:Member|Speaker|Participant))|(?:Unidentified Speaker)"
    r"|(?:Participant)): ", re.M)
DATE = re.compile(r"^(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day, ")


def pages_of(pdf):
    txt = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True,
                         text=True, check=True).stdout
    return txt.split("\f")


def clean(chunk):
    keep = []
    for line in chunk.split("\n"):
        s = line.strip()
        if re.fullmatch(r"EB-\d+", s):
            keep.append(f"[{s}]")
        elif s.startswith("Electoral Boundaries Commission –") or \
                re.fullmatch(r"(January|February|May|June) \d{1,2}, 20\d\d", s):
            continue
        else:
            keep.append(line)
    return "\n".join(keep)


def main():
    recs = {}
    order = []
    for rnd, name in FILES:
        pages = pages_of(SRC / name)
        meta = None
        cur = None
        for pno, page in enumerate(pages, 1):
            m = re.search(r"Transcript No\. (\d+)", page)
            if m and "Public Hearings" in page and len(page) < 600:
                lines = [l.strip() for l in page.splitlines() if l.strip()]
                i = lines.index("Public Hearings")
                j = next(k for k in range(i + 1, len(lines)) if DATE.match(lines[k]))
                meta = {"no": int(m.group(1)), "place": " ".join(lines[i + 1:j]),
                        "date": lines[j], "participants": []}
                cur = None
                continue
            if meta is None:
                continue
            head = page[:300]
            if "Participants\n" in head and "Electoral Boundaries Commission Public Hearings" in head:
                body = page.split("Participants\n", 1)[1]
                meta["participants"] = [l.strip() for l in body.splitlines() if l.strip()]
                continue
            if "Transcript produced by Alberta Hansard" in page:
                continue
            names = [re.escape(p.split(",")[0].strip()) for p in meta["participants"]]
            marks = [(mm.start(), mm.group(1)) for mm in TITLED.finditer(page)]
            if names:
                full = re.compile(r"^(" + "|".join(names) + r"): ", re.M)
                marks += [(mm.start(), mm.group(1)) for mm in full.finditer(page)]
            marks = sorted(set(marks))
            pos = 0
            for start, who in marks + [(len(page), None)]:
                chunk = page[pos:start]
                if cur is not None and chunk:
                    r = recs[cur]
                    r["text"] += clean(chunk)
                    if pno not in r["_pages"]:
                        r["_pages"].append(pno)
                pos = start
                if who is None or who in COMMISSION:
                    continue
                key = (rnd, meta["no"], who)
                if key != cur:
                    if key not in recs:
                        order.append(key)
                        recs[key] = {"id": None, "round": rnd, "source_pdf": name,
                                     "pages": None, "_pages": [],
                                     "method": "text-layer (pdftotext, reading order)",
                                     "transcript_no": meta["no"],
                                     "hearing_place": meta["place"],
                                     "hearing_date": meta["date"],
                                     "speaker": who,
                                     "participants_listed": meta["participants"],
                                     "text": ""}
                    else:
                        recs[key]["text"] += "\n[...]\n"
                    cur = key
    seq = {}
    with open(OUT, "w") as out:
        for key in order:
            r = recs[key]
            t = (key[0], key[1])
            seq[t] = seq.get(t, 0) + 1
            r["id"] = f"HANSARD-R{key[0]}-T{key[1]:02d}-{seq[t]:03d}"
            pp = r.pop("_pages")
            runs, a = [], None
            for p in pp:
                if a is None:
                    a = b = p
                elif p == b + 1:
                    b = p
                else:
                    runs.append((a, b)); a = b = p
            runs.append((a, b))
            r["pages"] = ",".join(str(x) if x == y else f"{x}-{y}" for x, y in runs)
            r["text"] = r["text"].strip()
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("records", len(order))


if __name__ == "__main__":
    main()
