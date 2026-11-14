"""Extract 338Canada's Alberta riding projections from saved riding pages.

Usage: python extract_338.py <dir with riding_urls.tsv and pages/<id>.html> <out.csv>
riding_urls.tsv lines: url<TAB>riding id<TAB>riding name (taken from the autocomplete list on
https://338canada.com/alberta/districts.htm). Each riding page is https://338canada.com/alberta/<id>e.htm.
The projection block on each page reads: lower %, upper %, point %, "± n%", optional arrow, party.

The pages are not in the repository (they are 338Canada's work), so this cannot be rerun from a
clone as it stands. To rerun it, fetch each page in riding_urls.tsv into pages/<id>.html and check
its SHA-256 against page_sha256.tsv first. 338Canada updates its pages in place, so only a copy
archived on 2026-10-19 will match.
"""
import csv, html, re, sys

src, out = sys.argv[1], sys.argv[2]
rows = []
for line in open(f"{src}/riding_urls.tsv"):
    if not line.strip():
        continue
    url, rid, name = line.rstrip("\n").split("\t")
    raw = open(f"{src}/pages/{rid}.html", encoding="utf-8", errors="replace").read()
    text = html.unescape(re.sub(r"<[^>]+>", "|", re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)))
    text = re.sub(r"(\|\s*)+", "|", text)
    end = text.find("338Canada Popular vote projection")
    seg = text[text.rfind("Latest update", 0, end):end]
    rec = {"id": rid, "name": name}
    m = re.search(r"Latest update: ([A-Z][a-z]+ \d{1,2}, \d{4})", seg)
    rec["updated"] = m.group(1) if m else ""
    for lo, hi, mid, _pm, party in re.findall(r"\|(\d+)%\|(\d+)%\|(\d+)%\|± (\d+)%\|(?:[▲▼]\|)?([A-Za-z]+)(?=\|)", seg):
        rec[party], rec[party + "_lo"], rec[party + "_hi"] = int(mid), int(lo), int(hi)
    m = re.search(r"\|([A-Z]+) 2023\|([\d.]+)%", seg)
    if m:
        rec["winner2023"], rec["winner2023_pct"] = m.group(1), float(m.group(2))
    rows.append(rec)
keys = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("id", "name", "updated"), k))
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader()
    w.writerows(rows)
