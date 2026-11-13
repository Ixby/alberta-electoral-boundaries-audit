"""Stage 1b: one record per written submission.

Reads the per-page files from 01_ocr_pages.py, picks the better text for each
page (text layer or OCR), finds the commission's ID stamp on each page, and
groups pages into submissions. Manual fixes (pages whose stamp could not be
read by machine, pages transcribed by eye) come from two small JSON files
kept beside this script:

  manual_page_ids.json   {"<pdf>": {"<page>": <submission number or 0>}}
                         0 = page is a batch cover / not part of a submission
  manual_page_text.json  {"<pdf>": {"<page>": {"text": "...", "note": "..."}}}

Output (JSON lines), fields:
  id, round, source_pdf, pages, n_pages, method, confidence_note,
  page_methods, ocr_mean_conf, n_chars, text
and a page map CSV (pdf, page, id, how the id was found, method, conf, chars).

Usage: python3 -I 02_build_corpus.py PAGES_DIR OUT_JSONL OUT_PAGEMAP_CSV [OFFICIAL_LIST_CSV]
  OFFICIAL_LIST_CSV (from 01d_official_list.py) adds an "affiliation" field.
"""
import csv
import json
import re
import sys
from pathlib import Path

PAGES, OUT, PMAP = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
HERE = Path(__file__).resolve().parent


def load_json(name):
    p = HERE / name
    return json.load(open(p)) if p.exists() else {}


AFFIL = {}
if len(sys.argv) > 4:
    for row in csv.DictReader(open(sys.argv[4])):
        AFFIL[row["id"]] = row["affiliation"] + (" (late submission)" if row["late"] else "")

MAN_ID = load_json("manual_page_ids.json")
MAN_TXT = load_json("manual_page_text.json")

R1 = [("EBC2025Submissions1-50ForPosting.pdf", 1, 50),
      ("EBC2025Submissions51-100ForPosting.pdf", 51, 100),
      ("EBC2025Submissions101-150ForPosting.pdf", 101, 150),
      ("EBC2025Submissions151-197ForPosting.pdf", 151, 197)]
R2 = []
for s in range(1, 1144, 50):
    e = min(s + 49, 1143)
    R2.append((f"EBC-2025-2-{s:03d}-to-{e:03d}.pdf", s, e))
FILES = [(1, *x) for x in R1] + [(2, *x) for x in R2]

# The stamp reads EBC-2025-<round>-<number>; OCR sometimes swaps look-alike
# characters or drops hyphens, so the pattern is loose and the number is
# range-checked against the batch.
STAMP = r"E\s?B\s?C\s?[-–—_.~ ]{0,3}20\s?25\s?[-–—_.~ ]{0,3}%d\s?[-–—_.~ ]{0,3}([0-9OoIlSsBZ]{1,5})\b"
FIX = str.maketrans("OoIlSsBZ", "00115582")


# A few round-1 stamps leave the round digit out ("EBC 2025-174").
STAMP_R1_SHORT = re.compile(r"EBC[ -]2025-(\d{2,3})(?![-\d])")


def find_id(text, rnd, lo, hi):
    for m in re.finditer(STAMP % rnd, text):
        try:
            n = int(m.group(1).translate(FIX))
        except ValueError:
            continue
        if lo <= n <= hi:
            return n
    if rnd == 1:
        for m in STAMP_R1_SHORT.finditer(text):
            if lo <= int(m.group(1)) <= hi:
                return int(m.group(1))
    return None


def choose(rec):
    # pdfium writes U+0002 where a line ends in a hyphen; in these files that
    # is almost always the hyphen of a compound name (Airdrie-East)
    layer, ocr = rec["layer"].replace("\r\n", "\n").replace("\x02", "-"), rec["ocr"]
    ls, os_ = layer.strip(), ocr.strip()
    if not os_:
        return layer, "text-layer"
    # Tesseract reads the capital I of this typeface as a vertical bar
    ocr = re.sub(r"(?<![\w|])\|(?=[ ’'\n])", "I", ocr)
    if rec.get("garbled_layer"):
        return ocr, "ocr"
    if len(ls) >= 0.8 * len(os_) and len(ls) >= 200:
        return layer, "text-layer"
    return ocr, "ocr"


def main():
    subs = {}
    order = []
    rows = []
    for rnd, name, lo, hi in FILES:
        pages = [json.loads(l) for l in open(PAGES / (name + ".jsonl"))]
        cur = None
        for rec in pages:
            pno = rec["page"]
            text, method = choose(rec)
            conf = rec["conf"] if method == "ocr" else -1
            man = MAN_TXT.get(name, {}).get(str(pno)) if isinstance(MAN_TXT.get(name), dict) else None
            note = ""
            if man:
                text, method, note = man["text"], man.get("method", "read-by-eye"), man.get("note", "")
                conf = -1
            how = "stamp"
            mid = MAN_ID.get(name, {}).get(str(pno)) if isinstance(MAN_ID.get(name), dict) else None
            if mid is not None:
                how = "manual"
            else:
                # the stamp sits at the top of the page: look there first, in
                # both versions of the page text, then anywhere on the page
                mid = (find_id(rec["layer"][:400], rnd, lo, hi)
                       or find_id(rec["ocr"][:400], rnd, lo, hi)
                       or find_id(rec["layer"], rnd, lo, hi)
                       or find_id(rec["ocr"], rnd, lo, hi))
                if mid is None:
                    how = "inherited"
                    mid = cur
            if mid == 0:
                rows.append([name, pno, "", "cover/none", method, conf, len(text.strip())])
                continue
            cur = mid
            if mid is None:
                rows.append([name, pno, "", "unassigned", method, conf, len(text.strip())])
                continue
            sid = f"EBC-2025-{rnd}-{mid:04d}"
            if sid not in subs:
                subs[sid] = {"id": sid, "round": rnd, "source_pdf": name, "_p": []}
                order.append(sid)
            subs[sid]["_p"].append((pno, text, method, conf, note, how))
            rows.append([name, pno, sid, how, method, conf, len(text.strip())])
    with open(OUT, "w") as out:
        for sid in order:
            s = subs[sid]
            pp = s.pop("_p")
            nums = [p[0] for p in pp]
            runs, a = [], None
            for p in nums:
                if a is None:
                    a = b = p
                elif p == b + 1:
                    b = p
                else:
                    runs.append((a, b)); a = b = p
            runs.append((a, b))
            s["pages"] = ",".join(str(x) if x == y else f"{x}-{y}" for x, y in runs)
            s["n_pages"] = len(nums)
            methods = [p[2] for p in pp]
            kinds = sorted(set(methods))
            s["method"] = kinds[0] if len(kinds) == 1 else "mixed: " + " + ".join(
                f"{k} ({methods.count(k)} p.)" for k in kinds)
            # confidence is weighted by characters, so a footer-only page or a
            # map does not drag down a clean letter
            ocrp = [(p[3], len(p[1].strip())) for p in pp if p[3] >= 0]
            wsum = sum(n for _, n in ocrp)
            s["ocr_mean_conf"] = round(sum(c * n for c, n in ocrp) / wsum, 1) if wsum else None
            notes = [f"p.{p[0]}: {p[4]}" for p in pp if p[4]]
            if ocrp:
                lowp = [str(p[0]) for p in pp if 0 <= p[3] < 75 and len(p[1].strip()) > 200]
                c = (f"Tesseract word confidence {s['ocr_mean_conf']} (character-weighted mean) "
                     f"over {len(ocrp)} OCR page(s)")
                if lowp:
                    c += ("; page(s) under 75 with more than 200 characters, usually maps or "
                          "tables, check against the PDF before quoting: " + ", ".join(lowp))
                notes.insert(0, c)
            if "inherited" in {p[5] for p in pp}:
                notes.append("page(s) without a readable ID stamp, assigned to this submission "
                             "because they follow it: " + ", ".join(str(p[0]) for p in pp if p[5] == "inherited"))
            if "manual" in {p[5] for p in pp}:
                notes.append("ID set by eye for page(s) " + ", ".join(str(p[0]) for p in pp if p[5] == "manual")
                             + " (see scripts/manual_page_ids.json)")
            s["confidence_note"] = "; ".join(notes) if notes else "embedded text layer; no OCR needed"
            s["affiliation"] = AFFIL.get(sid, "not on the commission's published list")
            s["page_methods"] = {str(p[0]): p[2] for p in pp}
            s["text"] = "\n".join(f"[[page {p[0]}]]\n{p[1].strip()}" for p in pp)
            s["n_chars"] = sum(len(p[1].strip()) for p in pp)
            out.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(PMAP, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_pdf", "page", "id", "id_found_by", "text_method", "ocr_conf", "chars"])
        w.writerows(rows)
    print("submissions", len(order))


if __name__ == "__main__":
    main()
