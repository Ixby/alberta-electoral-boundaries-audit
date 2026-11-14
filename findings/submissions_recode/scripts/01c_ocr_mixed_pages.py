"""Stage 1a, third pass: pages that have BOTH a text layer and a large image.

01_ocr_pages.py OCRs a page only when its text layer is short. A page can
carry a normal-length text layer and still hold more words inside a picture
(a pasted screenshot, a scanned attachment under a typed header). This pass
lists every page that was not OCR'd and holds a raster image of at least
MIN_AREA square inches (pdfimages -list), OCRs it, and stores the OCR text.
02_build_corpus.py then keeps the OCR text when it is clearly longer than the
text layer.

Usage: python3 -I 01c_ocr_mixed_pages.py PDF_DIR OUT_DIR TESSDATA_DIR
"""
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ["OMP_THREAD_LIMIT"] = "2"
DL, OUT, TESS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
MIN_AREA = 12.0  # square inches; a letter page is 93.5


def big_image_pages(pdf):
    out = subprocess.run(["pdfimages", "-list", str(pdf)], capture_output=True, text=True).stdout
    pages = {}
    for line in out.splitlines()[2:]:
        p = line.split()
        try:
            page, w, h, xppi, yppi = int(p[0]), int(p[3]), int(p[4]), float(p[12]), float(p[13])
        except (ValueError, IndexError):
            continue
        if p[2] != "image" or xppi <= 0 or yppi <= 0:
            continue
        pages[page] = max(pages.get(page, 0), (w / xppi) * (h / yppi))
    return {k for k, v in pages.items() if v >= MIN_AREA}


def main():
    import pypdfium2 as pdfium
    import tesserocr
    api = tesserocr.PyTessBaseAPI(path=TESS, lang="eng", psm=tesserocr.PSM.AUTO)
    for f in sorted((OUT / "pages").glob("*.jsonl")):
        name = f.name[:-6]
        rows = [json.loads(l) for l in open(f)]
        big = big_image_pages(DL / name)
        todo = [r for r in rows if r["conf"] == -1 and r["page"] in big and not r.get("mixed_checked")]
        for r in rows:
            r["img"] = 1 if r["page"] in big else 0
        pdf = pdfium.PdfDocument(str(DL / name)) if todo else None
        for r in todo:
            img = pdf[r["page"] - 1].render(scale=200 / 72).to_pil().convert("L")
            api.SetImage(img)
            r["ocr"], r["conf"], r["mixed_checked"] = api.GetUTF8Text() or "", api.MeanTextConf(), True
            print(name, r["page"], "layer", len(r["layer"].strip()), "ocr", len(r["ocr"].strip()),
                  "conf", r["conf"], flush=True)
        with open(str(f) + ".tmp", "w") as out:
            for r in rows:
                out.write(json.dumps(r) + "\n")
        os.replace(str(f) + ".tmp", f)


if __name__ == "__main__":
    main()
