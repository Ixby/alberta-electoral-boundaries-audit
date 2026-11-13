"""Check that quotes occur verbatim in the records they are attributed to.

Two uses:
  1. python3 -I 05_verify_quotes.py CORPUS_JSONL HANSARD_JSONL --codebook CODEBOOK.md
     checks the worked examples: every double-quoted passage of 6+ words that
     follows a record ID heading in section 9.
  2. python3 -I 05_verify_quotes.py CORPUS_JSONL HANSARD_JSONL --codes codes.csv
     checks quote_want / quote_react in a coding sheet, including the page.

Matching collapses whitespace, joins words hyphenated across a line break,
and treats curly and straight quotation marks and dash variants as equal.
"[…]" in a quote matches any run of text.
"""
import csv
import json
import re
import sys


def norm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = t.replace("–", "-").replace("—", "-")
    t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)
    return re.sub(r"\s+", " ", t).strip()


def found(quote, text):
    parts = [re.escape(norm(p)) for p in re.split(r"\[…\]|\[\.\.\.\]", quote) if p.strip()]
    return bool(parts) and re.search(".*?".join(parts), norm(text), re.S) is not None


def page_text(rec, page):
    t = rec["text"]
    if str(page).startswith("EB-"):
        m = re.search(r"\[%s\](.*?)(?=\[EB-\d+\]|\Z)" % re.escape(page), t, re.S)
    else:
        m = re.search(r"\[\[page %s\]\](.*?)(?=\[\[page \d+\]\]|\Z)" % page, t, re.S)
    return m.group(1) if m else None


def main():
    recs = {}
    for fn in sys.argv[1:3]:
        for line in open(fn):
            r = json.loads(line)
            recs[r["id"]] = r
    mode, path = sys.argv[3], sys.argv[4]
    bad = n = 0
    if mode == "--codebook":
        body = open(path).read().split("## 9. Worked examples", 1)[1]
        for block in re.split(r"\n\*\*\d+\. ", body)[1:]:
            rid = re.match(r"((?:EBC-2025-\d-\d{4})|(?:HANSARD-R\d-T\d\d-\d{3}))", block).group(1)
            block = block.split("Old label:")[0]      # old labels are not quotes
            for q in re.findall(r"\"([^\"]*)\"", block):
                if len(q.split()) < 6:
                    continue
                n += 1
                if not found(q, recs[rid]["text"]):
                    bad += 1
                    print("NOT FOUND", rid, "|", q[:90])
    else:
        for row in csv.DictReader(open(path)):
            for qc, pc in (("quote_want", "quote_page"), ("quote_react", "quote_react_page")):
                q = (row.get(qc) or "").strip()
                if not q:
                    continue
                n += 1
                rec = recs.get(row["id"])
                if rec is None or not found(q, rec["text"]):
                    bad += 1
                    print("NOT FOUND", row["id"], row["element"], qc, "|", q[:90])
                    continue
                pt = page_text(rec, row.get(pc, ""))
                if pt is not None and not found(q, pt):
                    print("WRONG PAGE", row["id"], row["element"], qc, row.get(pc))
    print(f"{n} quotes checked, {bad} not found")


if __name__ == "__main__":
    main()
