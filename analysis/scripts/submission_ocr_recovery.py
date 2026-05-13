"""
submission_ocr_recovery.py

Recovers text from the 23 image-only submission PDFs that pdfplumber couldn't extract.

Strategy:
  1. Re-parse the batch PDFs to find page boundaries for each failed submission ID.
  2. Render those pages to images via PyMuPDF at 200 DPI.
  3. Run EasyOCR over each page image.
  4. Write recovered text back to .temp/submissions/text/<id>.txt.

After running, re-run submission_sentiment_llm_full.py — it will classify the recovered
submissions on the next pass (they won't be in the progress CSV yet).

Requirements: pymupdf (fitz), easyocr, Pillow
Usage:
    python analysis/scripts/submission_ocr_recovery.py [--dry-run]

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

import re
import sys
import logging
from pathlib import Path

import csv
import fitz  # PyMuPDF

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent
TEMP = ROOT / ".temp" / "submissions"
TEXT_DIR = TEMP / "text"
DPI = 200

# ── The 23 known OCR-failure IDs (no extractable submission content) ──────────
FAILED_IDS: set[tuple[int, int]] = {
    # (round, id_int)
    (1, 11), (1, 13), (1, 15), (1, 16), (1, 18), (1, 20),
    (1, 65), (1, 82), (1, 86), (1, 97),
    (1, 114), (1, 132), (1, 146), (1, 151), (1, 153),
    (1, 187), (1, 188),
    (2, 507), (2, 535), (2, 618), (2, 992), (2, 1042), (2, 1043),
}

# Batch PDF definitions  (filename, round, start_id, end_id)
R1_FILES = [
    ("EBC2025Submissions1-50ForPosting.pdf",   1,   1,  50),
    ("EBC2025Submissions51-100ForPosting.pdf",  1,  51, 100),
    ("EBC2025Submissions101-150ForPosting.pdf", 1, 101, 150),
    ("EBC2025Submissions151-197ForPosting.pdf", 1, 151, 197),
]
R2_FILES = []
for _s in range(1, 1144, 50):
    _e = min(_s + 49, 1143)
    R2_FILES.append((f"EBC-2025-2-{_s:03d}-to-{_e:03d}.pdf", 2, _s, _e))

ALL_BATCHES = R1_FILES + R2_FILES

R1_ID_RE = re.compile(r"\bEBC[-\s]?2025[-\s]?1[-\s]?0*(\d{1,3})\b", re.I)
R2_ID_RE = re.compile(r"\bEBC[-\s]?2025[-\s]?2[-\s]?0*(\d{1,4})\b", re.I)


def _id_re(rnd: int):
    return R1_ID_RE if rnd == 1 else R2_ID_RE


def canonical_id(rnd: int, num: int) -> str:
    if rnd == 1:
        return f"EBC-2025-1-{num:04d}"
    return f"EBC-2025-2-{num:04d}"


# ── Find page ranges for each failed ID in its batch PDF ─────────────────────

def find_page_ranges(batch_path: Path, rnd: int, start: int, end: int,
                     wanted: set[int]) -> dict[int, tuple[int, int]]:
    """
    Returns {id_int: (first_page_0indexed, last_page_0indexed)} for each wanted ID
    found in this batch. Pages are 0-indexed (PyMuPDF convention).
    """
    if not batch_path.exists():
        logger.warning("Batch not found: %s", batch_path.name)
        return {}

    id_re = _id_re(rnd)
    doc = fitz.open(str(batch_path))
    n_pages = len(doc)

    # Pass 1: find which page each ID first appears on
    id_first_page: dict[int, int] = {}
    for pi in range(n_pages):
        text = doc[pi].get_text("text")
        m = id_re.search(text)
        if m:
            sid = int(m.group(1))
            if start <= sid <= end and sid not in id_first_page:
                id_first_page[sid] = pi

    doc.close()

    # Pass 2: build page ranges (first_page .. next_id_page - 1)
    sorted_ids = sorted(id_first_page)
    ranges: dict[int, tuple[int, int]] = {}
    for i, sid in enumerate(sorted_ids):
        if sid not in wanted:
            continue
        fp = id_first_page[sid]
        # last page is one before the next known ID starts (or the final page)
        if i + 1 < len(sorted_ids):
            lp = id_first_page[sorted_ids[i + 1]] - 1
        else:
            lp = n_pages - 1
        ranges[sid] = (fp, lp)

    return ranges


# ── Render pages to PIL images ────────────────────────────────────────────────

def render_pages(batch_path: Path, first: int, last: int) -> list:
    """Return list of PIL Images for pages first..last (0-indexed, inclusive)."""
    import PIL.Image
    doc = fitz.open(str(batch_path))
    images = []
    mat = fitz.Matrix(DPI / 72, DPI / 72)
    for pi in range(first, last + 1):
        pix = doc[pi].get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
        img = PIL.Image.frombytes("L", (pix.width, pix.height), pix.samples)
        images.append(img)
    doc.close()
    return images


# ── EasyOCR pass ─────────────────────────────────────────────────────────────

def ocr_images(images: list) -> str:
    import easyocr
    import numpy as np

    logger.info("  Initialising EasyOCR reader (first call downloads models if absent)...")
    reader = easyocr.Reader(["en"], gpu=False, verbose=False)

    lines = []
    for i, img in enumerate(images):
        arr = np.array(img)
        results = reader.readtext(arr, detail=0, paragraph=True)
        lines.extend(results)
        if len(images) > 1:
            lines.append("")  # page break separator

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main(dry_run: bool = False) -> None:
    # Group failed IDs by batch
    batch_work: dict[str, tuple[Path, int, int, int, set[int]]] = {}
    for fname, rnd, bstart, bend in ALL_BATCHES:
        wanted = {num for (r, num) in FAILED_IDS if r == rnd and bstart <= num <= bend}
        if wanted:
            batch_work[fname] = (TEMP / fname, rnd, bstart, bend, wanted)

    logger.info("Batches to process: %d", len(batch_work))

    recovered = 0
    failed = []

    for fname, (batch_path, rnd, bstart, bend, wanted) in batch_work.items():
        logger.info("\n--- %s (round %d, ids %d-%d) ---", fname, rnd, bstart, bend)
        logger.info("  Wanted IDs: %s", sorted(wanted))

        page_ranges = find_page_ranges(batch_path, rnd, bstart, bend, wanted)

        for sid in sorted(wanted):
            cid = canonical_id(rnd, sid)
            out_path = TEXT_DIR / f"{cid}.txt"

            if sid not in page_ranges:
                logger.warning("  %s — page range not found in PDF (may be redacted)", cid)
                failed.append(cid)
                continue

            fp, lp = page_ranges[sid]
            logger.info("  %s — pages %d-%d", cid, fp + 1, lp + 1)

            if dry_run:
                logger.info("    [dry-run] would render pages %d-%d and OCR", fp, lp)
                continue

            try:
                images = render_pages(batch_path, fp, lp)
                logger.info("  Rendered %d page(s), running EasyOCR...", len(images))
                text = ocr_images(images)

                if len(text.strip()) < 30:
                    logger.warning("  %s — OCR returned very little text (%d chars); may be truly blank", cid, len(text))
                    failed.append(cid)
                else:
                    out_path.write_text(text, encoding="utf-8")
                    logger.info("  %s — recovered %d chars -> %s", cid, len(text), out_path.name)
                    recovered += 1

            except Exception as e:
                logger.error("  %s — error: %s", cid, e)
                failed.append(cid)

    print(f"\nResults:")
    print(f"  Recovered: {recovered}")
    print(f"  Unrecoverable (redacted or truly blank): {len(failed)}")
    if failed:
        print(f"  Unrecoverable IDs: {failed}")

    if not dry_run and recovered > 0:
        _purge_from_progress(recovered_ids=[
            cid for (rnd, num) in FAILED_IDS
            for cid in [canonical_id(rnd, num)]
            if (TEXT_DIR / f"{cid}.txt").stat().st_size > 100
        ])


def _purge_from_progress(recovered_ids: list[str]) -> None:
    """Remove recovered submission IDs from the full-scan progress CSV so the
    next run of submission_sentiment_llm_full.py re-classifies them."""
    progress_csv = ROOT / "data" / "outputs" / "submission_sentiment_llm_full_progress.csv"
    if not progress_csv.exists():
        logger.info("Progress CSV not found yet — nothing to purge.")
        return

    purge_set = set(recovered_ids)
    kept = []
    removed = 0
    with progress_csv.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        for row in reader:
            if row.get("submission_id") in purge_set:
                removed += 1
            else:
                kept.append(row)

    with progress_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(kept)

    print(f"  Progress CSV: removed {removed} recovered IDs -> {progress_csv.name}")
    print(f"  Re-run submission_sentiment_llm_full.py to classify them.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        logger.info("DRY RUN — no files will be written")
    main(dry_run=dry_run)
