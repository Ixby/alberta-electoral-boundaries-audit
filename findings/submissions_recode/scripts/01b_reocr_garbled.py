"""Stage 1a, second pass: OCR pages whose embedded text layer is unusable.

Some PDFs embed fonts without a usable character map, so the text layer comes
out as symbol soup ("!\"#$%&'(") although the page looks fine. A page is
treated as garbled when under 60% of its non-space characters are letters or
when under half of its "words" contain a vowel. Those pages are rendered and
OCR'd, and the page file is rewritten in place with the OCR text and a
"garbled_layer": true flag (the junk layer is kept for the record).

Also re-OCRs, at 300 dpi, any OCR page under LOW_CONF confidence that holds
more than 200 characters, keeping whichever pass scored higher.

Usage: python3 -I 01b_reocr_garbled.py PDF_DIR OUT_DIR TESSDATA_DIR
"""
import json
import os
import re
import sys
from pathlib import Path

os.environ["OMP_THREAD_LIMIT"] = "2"
DL, OUT, TESS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
LOW_CONF = 80


def garbled(layer):
    s = layer.strip()
    if len(s) < 200:
        return False
    body = re.sub(r"\s", "", s)
    letters = sum(c.isalpha() for c in body) / len(body)
    words = s.split()
    vow = sum(bool(re.search(r"[aeiouyAEIOUY]", w)) for w in words) / max(1, len(words))
    return letters < 0.6 or vow < 0.5


def main():
    import pypdfium2 as pdfium
    import tesserocr
    api = tesserocr.PyTessBaseAPI(path=TESS, lang="eng", psm=tesserocr.PSM.AUTO)
    for f in sorted((OUT / "pages").glob("*.jsonl")):
        rows = [json.loads(l) for l in open(f)]
        todo_g = [r for r in rows if r["conf"] == -1 and garbled(r["layer"])]
        todo_l = [r for r in rows if 0 <= r["conf"] < LOW_CONF and len(r["ocr"].strip()) > 200
                  and not r.get("reocr")]
        if not todo_g and not todo_l:
            continue
        pdf = pdfium.PdfDocument(str(DL / f.name[:-6]))
        for r in todo_g:
            img = pdf[r["page"] - 1].render(scale=200 / 72).to_pil().convert("L")
            api.SetImage(img)
            r["ocr"], r["conf"], r["garbled_layer"] = api.GetUTF8Text() or "", api.MeanTextConf(), True
            print("garbled", f.name[:-6], r["page"], r["conf"], len(r["ocr"]), flush=True)
        for r in todo_l:
            img = pdf[r["page"] - 1].render(scale=300 / 72).to_pil().convert("L")
            api.SetImage(img)
            t, c = api.GetUTF8Text() or "", api.MeanTextConf()
            r["reocr"] = True
            if c > r["conf"]:
                print("improved", f.name[:-6], r["page"], r["conf"], "->", c, flush=True)
                r["ocr"], r["conf"] = t, c
        with open(str(f) + ".tmp", "w") as out:
            for r in rows:
                out.write(json.dumps(r) + "\n")
        os.replace(str(f) + ".tmp", f)


if __name__ == "__main__":
    main()
