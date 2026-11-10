"""Stage 1a: per-page text for the 27 Elections Alberta batch PDFs.

For every page:
  layer  the embedded text layer (pypdfium2)
  ocr    Tesseract OCR of the page rendered at DPI (tesserocr, eng,
         tessdata_fast), run when the page is image-dominated: the text layer
         is under MIN_LAYER characters, or raster images cover IMG_FRAC or
         more of the page. Otherwise "" (the text layer is the page).
  conf   Tesseract mean word confidence (0-100), -1 when OCR was skipped
  img    share of the page area covered by raster images

Writes one JSON-lines file per PDF, OUT/pages/<pdf>.jsonl, appended page by
page so an interrupted run resumes.

Usage: python3 -I 01_ocr_pages.py PDF_DIR OUT_DIR TESSDATA_DIR [DPI]
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

os.environ["OMP_THREAD_LIMIT"] = "1"
DL, OUT, TESS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
DPI = int(sys.argv[4]) if len(sys.argv) > 4 else 150
MIN_LAYER = 400
IMG_FRAC = 0.25


def image_fraction(page):
    import pypdfium2.raw as raw
    w, h = page.get_size()
    area = 0.0
    for obj in page.get_objects(filter=[raw.FPDF_PAGEOBJ_IMAGE], max_depth=4):
        try:
            l, b, r, t = obj.get_pos()
        except Exception:
            continue
        l, r = max(0, min(l, r)), min(w, max(l, r))
        b, t = max(0, min(b, t)), min(h, max(b, t))
        area += max(0, r - l) * max(0, t - b)
    return min(1.0, area / (w * h)) if w and h else 0.0


def work(name):
    import pypdfium2 as pdfium
    import tesserocr
    dst = OUT / "pages" / (name + ".jsonl")
    done = 0
    if dst.exists():
        done = sum(1 for _ in open(dst))
    api = tesserocr.PyTessBaseAPI(path=TESS, lang="eng", psm=tesserocr.PSM.AUTO)
    pdf = pdfium.PdfDocument(str(DL / name))
    n = len(pdf)
    with open(dst, "a") as out:
        for i in range(done, n):
            page = pdf[i]
            tp = page.get_textpage()
            layer = tp.get_text_bounded() or ""
            tp.close()
            frac = image_fraction(page)
            ocr, conf = "", -1
            if len(layer.strip()) < MIN_LAYER or frac >= IMG_FRAC:
                img = page.render(scale=DPI / 72).to_pil().convert("L")
                api.SetImage(img)
                ocr = api.GetUTF8Text() or ""
                conf = api.MeanTextConf()
            out.write(json.dumps({"page": i + 1, "layer": layer, "ocr": ocr,
                                  "conf": conf, "img": round(frac, 3)}) + "\n")
            out.flush()
            page.close()
    return name, n


if __name__ == "__main__":
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    names = sorted((p.name for p in DL.glob("*.pdf")),
                   key=lambda n: -(DL / n).stat().st_size)
    with ProcessPoolExecutor(4) as ex:
        for r in ex.map(work, names, chunksize=1):
            print(r, flush=True)
