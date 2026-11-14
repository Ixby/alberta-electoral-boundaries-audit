"""Amendment 7, Step B: fix the calibration sample from the panel's map pages.

Rule (A7 Part 3): "the unchanged districts drawn in the same map pages as changed districts".
Operationalised (fixed before any reconstruction):
  - map pages = Appendix 8 district pages of the high-resolution PDF (district n at PDF page 215+n);
    the Appendix 6 composites are not used;
  - an unchanged district u counts as drawn on changed district c's page when that page carries
    u's district-number label in the neighbour-label style (ArialMT, grey #828282 or #4E4E4E, the same point size as
    the page's own district-number label, which is Arial-Bold in red #93241A) AND a word of u's name in the same grey style within 60 pt.
Inputs: hi-res PDF (SHA-256 d8ae78ab...), findings/iap_unchanged_districts.md (Step A), App. 7 names.
"""
import fitz, csv, re, math, json, sys, hashlib
PDF, STEPA, POPS, OUT = sys.argv[1:5]
ed = {int(r["ed_number"]): r["district"] for r in csv.DictReader(open(POPS, encoding="utf-8"))}
md = open(STEPA, encoding="utf-8").read()
unch = sorted(int(m) for m in re.findall(r"^\| (\d+) \| [^|]+ \| [\d,]+ \| App\. 7, [^|]+ \| \d+ \|", md, re.M))
chg = sorted(set(ed) - set(unch))
doc = fitz.open(PDF)
def spans(pg):
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                yield s["text"].strip(), s["font"], round(s["size"], 1), s["color"], fitz.Rect(s["bbox"])
def words(name): return {re.sub(r"[^a-z]", "", w.lower()) for w in re.split(r"[-\s]+", name) if w}
res, evidence = {}, []
for c in chg:
    S = list(spans(doc[215 + c - 1]))
    own = [s for s in S if s[0] == str(c) and s[1] == "Arial-BoldMT" and s[3] == 0x93241A]
    size = own[0][2] if own else None
    grey = [s for s in S if s[1] == "ArialMT" and s[3] in (0x828282, 0x4E4E4E) and (size is None or s[2] == size)]
    found = []
    for u in unch:
        for n in (s for s in grey if s[0] == str(u)):
            cx, cy = (n[4].x0 + n[4].x1) / 2, (n[4].y0 + n[4].y1) / 2
            near = [s for s in grey if s is not n and math.hypot((s[4].x0 + s[4].x1) / 2 - cx, (s[4].y0 + s[4].y1) / 2 - cy) < 60
                    and (words(s[0]) & words(ed[u]) - {""})]
            if near:
                found.append(u)
                evidence.append({"changed_page_of": c, "pdf_page": 215 + c, "unchanged": u, "name": ed[u],
                                 "number_label_at": [round(v, 1) for v in n[4]], "name_label": near[0][0]})
                break
    res[c] = found
sample = sorted({u for v in res.values() for u in v})
json.dump({"rule": __doc__, "pdf_sha256": hashlib.sha256(open(PDF, "rb").read()).hexdigest(),
           "unchanged": unch, "changed": chg, "by_changed_page": res, "sample": sample,
           "sample_names": {u: ed[u] for u in sample}, "evidence": evidence}, open(OUT, "w", encoding="utf-8"), indent=1)
print(len(sample), [(u, ed[u]) for u in sample])
