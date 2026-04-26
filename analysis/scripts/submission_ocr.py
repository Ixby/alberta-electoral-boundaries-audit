"""
v0_1 OCR pass on image-only pages that likely contain the 88 missing submissions.

Dependencies:
- Forward: None
- Backward: easyocr, pymupdf (fitz), Pillow, json, csv, pathlib
Produces:
  .temp/submissions/ocr_pages/<pdf_stem>_p<NNN>.txt
  .temp/submissions/ocr_results.json
  (Updates) data/submission_search_dataset.csv with OCR source rows
  analysis/v0_1_submission_ocr_log.md

Approach:
1. Use the ocr_plan.json (already built) to target 73 pages in 23 PDFs.
2. Render each page at 200 DPI with PyMuPDF, OCR via EasyOCR CPU.
3. Try to re-detect missing EBC-2025-X-NNN IDs from OCR text.
4. For each recovered submission, run the 7 keyword regex patterns from submission_search.py.
5. Append new hit rows to data/submission_search_dataset.csv with source='ocr'.
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations
import sys, io, json, re, csv, time
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
TEMP = ROOT / ".temp" / "submissions"
TEXT = TEMP / "text"
OCR_DIR = TEMP / "ocr_pages"
OCR_DIR.mkdir(parents=True, exist_ok=True)
DATA = ROOT / "data"

sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
from submission_search import build_patterns, classify_position, R1_ID_PATTERNS, R2_ID_PATTERN

def run():
    import fitz
    import easyocr
    plan = json.loads((TEMP / "ocr_plan.json").read_text())

    log = []
    t0 = time.time()
    log.append(f"[init] loading EasyOCR...")
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    log.append(f"[init] ready in {time.time()-t0:.1f}s")

    total_pages = sum(len(v) for v in plan.values())
    log.append(f"[plan] {total_pages} pages across {len(plan)} PDFs")

    page_texts = {}  # (pdf_name, page_idx) -> text
    char_counts = []
    t1 = time.time()
    count = 0
    for pdf_name, pages in plan.items():
        pdf_path = TEMP / pdf_name
        doc = fitz.open(pdf_path)
        for pidx in pages:
            count += 1
            page = doc[pidx]
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            try:
                result = reader.readtext(img_bytes, detail=0, paragraph=True)
                text = "\n".join(result)
            except Exception as e:
                text = ""
                log.append(f"[ocr-fail] {pdf_name} p{pidx+1}: {e!r}")
            page_texts[f"{pdf_name}|{pidx}"] = text
            char_counts.append(len(text))
            out_file = OCR_DIR / f"{Path(pdf_name).stem}_p{pidx+1:04d}.txt"
            out_file.write_text(text, encoding="utf-8", errors="replace")
            if count % 5 == 0:
                elapsed = time.time() - t1
                rate = count / elapsed
                eta = (total_pages - count) / rate if rate > 0 else 0
                log.append(f"[ocr] {count}/{total_pages} pages, {elapsed:.0f}s elapsed, ETA {eta:.0f}s")
                print(log[-1], flush=True)
        doc.close()
    log.append(f"[ocr] done in {time.time()-t1:.0f}s, avg chars/page={sum(char_counts)/max(len(char_counts),1):.0f}")

    # Persist raw results
    (TEMP / "ocr_results.json").write_text(json.dumps({
        "page_texts": page_texts,
        "char_counts": char_counts,
    }))

    # Now reconstruct per-submission text from OCR pages.
    # We re-read each PDF, concatenate consecutive OCR'd pages + any text-layer neighbors,
    # and try to detect EBC-2025-X-NNN.
    # Simpler approach: for each OCR'd page, look for any EBC-2025 id; assign page text
    # to that submission id (stitching happens when the text-layer extractor ran).
    R1_FILES = [
        ("EBC2025Submissions1-50ForPosting.pdf", 1, 50),
        ("EBC2025Submissions51-100ForPosting.pdf", 51, 100),
        ("EBC2025Submissions101-150ForPosting.pdf", 101, 150),
        ("EBC2025Submissions151-197ForPosting.pdf", 151, 197),
    ]
    R2_FILES = []
    for start in range(1, 1144, 50):
        end = min(start+49, 1143)
        R2_FILES.append((f"EBC-2025-2-{start:03d}-to-{end:03d}.pdf", start, end))

    r1_missing = {1,2,3,4,5,6,7,21,22,23,24,62,73,111,147,159,174,183,186,190,191,192,193,194,195,196,197}
    r2_missing = {2,6,7,10,11,41,44,54,76,85,98,102,103,104,106,129,141,160,163,227,253,254,270,358,377,378,379,430,444,454,469,477,483,492,499,524,531,573,596,602,610,612,615,616,639,644,654,673,704,707,766,810,828,829,841,966,973,1048,1113,1122,1126}

    # Build per-submission OCR texts by reconstructing whole PDFs with OCR stitched in.
    ocr_subs = {}  # (round, id) -> text

    all_files = [(n, s, e, 1) for (n,s,e) in R1_FILES] + [(n, s, e, 2) for (n,s,e) in R2_FILES]
    for pdf_name, start, end, rnd in all_files:
        pdf_path = TEMP / pdf_name
        if not pdf_path.exists():
            continue
        doc = fitz.open(pdf_path)
        pages = []
        for i, pg in enumerate(doc):
            tl = pg.get_text() or ""
            key = f"{pdf_name}|{i}"
            if key in page_texts:
                combined = (tl + "\n" + page_texts[key]).strip()
            else:
                combined = tl
            pages.append((i+1, combined))
        doc.close()

        # Detect IDs & accumulate
        if rnd == 2:
            id_pat = R2_ID_PATTERN
            current = None
            current_sp = None
            accum = []
            for pnum, text in pages:
                m = id_pat.search(text)
                if m:
                    sid = int(m.group(1))
                    if start <= sid <= end and sid != current:
                        if current is not None:
                            ocr_subs[(2, current)] = "\n".join(accum)
                        current = sid
                        current_sp = pnum
                        accum = [text]
                        continue
                if current is not None:
                    accum.append(text)
            if current is not None:
                ocr_subs[(2, current)] = "\n".join(accum)
        else:  # R1
            current = None
            accum = []
            for pnum, text in pages:
                matched = None
                for pat in R1_ID_PATTERNS:
                    m = pat.search(text)
                    if m:
                        n = int(m.group(1))
                        if start <= n <= end:
                            matched = n
                            break
                if matched is not None and matched != current:
                    if current is not None:
                        ocr_subs[(1, current)] = "\n".join(accum)
                    current = matched
                    accum = [text]
                else:
                    if current is not None:
                        accum.append(text)
            if current is not None:
                ocr_subs[(1, current)] = "\n".join(accum)

    # Count which of the previously-missing ids were recovered
    recovered_r1 = sorted([sid for (r,sid) in ocr_subs if r==1 and sid in r1_missing])
    recovered_r2 = sorted([sid for (r,sid) in ocr_subs if r==2 and sid in r2_missing])
    log.append(f"[recover] R1 recovered ids: {recovered_r1}")
    log.append(f"[recover] R2 recovered ids: {recovered_r2}")
    log.append(f"[recover] total: R1 {len(recovered_r1)}/27, R2 {len(recovered_r2)}/61")

    # Run keyword search on recovered submissions
    pats = build_patterns()
    keymap = {
        "airdrie_4way_split": "mentions_airdrie_4way_split",
        "nolan_hill_cochrane": "mentions_nolan_hill_cochrane",
        "rmh_banff_park": "mentions_rmh_banff_park",
        "olds_three_hills_didsbury": "mentions_olds_three_hills_didsbury",
        "chestermere_split": "mentions_chestermere_split",
        "red_deer_hybrids": "mentions_red_deer_hybrids",
        "st_albert_sturgeon": "mentions_st_albert_sturgeon",
    }
    new_rows = []
    totals = defaultdict(int)
    for (rnd, sid), text in ocr_subs.items():
        if rnd == 1 and sid not in r1_missing:
            continue
        if rnd == 2 and sid not in r2_missing:
            continue
        if not text.strip():
            continue
        sid_str = f"EBC-2025-{rnd}-{sid:04d}"
        row = {
            "submission_id": sid_str,
            "round": rnd,
            "source_file": "",
            "page_range": "",
            "mentions_airdrie_4way_split": False,
            "mentions_nolan_hill_cochrane": False,
            "mentions_rmh_banff_park": False,
            "mentions_olds_three_hills_didsbury": False,
            "mentions_chestermere_split": False,
            "mentions_red_deer_hybrids": False,
            "mentions_st_albert_sturgeon": False,
            "position_on_mentioned": "N/A",
            "relevant_quote": "",
            "source": "ocr",
        }
        any_hit = False
        snippets = []
        for pk, regs in pats.items():
            for rg in regs:
                m = rg.search(text)
                if m:
                    row[keymap[pk]] = True
                    any_hit = True
                    totals[pk] += 1
                    s0 = max(0, m.start()-150)
                    s1 = min(len(text), m.end()+150)
                    snip = text[s0:s1].replace("\n", " ")
                    snippets.append((pk, classify_position(snip), snip))
                    break
        if any_hit:
            row["position_on_mentioned"] = snippets[0][1]
            row["relevant_quote"] = snippets[0][2].strip()[:280]
            new_rows.append(row)

    log.append(f"[hits] {len(new_rows)} OCR-sourced submissions had keyword hits")
    for k, v in totals.items():
        log.append(f"[hits] {k}: {v}")

    # Persist OCR submissions (full text, for later inspection)
    ocr_text_dir = TEMP / "ocr_text"
    ocr_text_dir.mkdir(exist_ok=True)
    for (rnd, sid), text in ocr_subs.items():
        fn = ocr_text_dir / f"EBC-2025-{rnd}-{sid:04d}.txt"
        fn.write_text(text, encoding="utf-8", errors="replace")

    # Append to CSV — first read existing, then rewrite with added source column and new rows
    csv_path = DATA / "submission_search_dataset.csv"
    existing = []
    existing_fields = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        rdr = csv.DictReader(f)
        existing_fields = list(rdr.fieldnames)
        existing = list(rdr)

    fields = existing_fields[:]
    if "source" not in fields:
        fields.append("source")

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in existing:
            if "source" not in r:
                r["source"] = "text_layer"
            w.writerow(r)
        for r in new_rows:
            # fill any fields
            for k in fields:
                r.setdefault(k, "")
            w.writerow(r)

    log.append(f"[out] appended {len(new_rows)} rows (source=ocr) to {csv_path}")

    (TEMP / "ocr_run.log").write_text("\n".join(log))
    # Return state for markdown writer
    return {
        "total_pages_planned": total_pages,
        "pages_ocrd": count,
        "avg_chars": sum(char_counts)/max(len(char_counts),1),
        "min_chars": min(char_counts) if char_counts else 0,
        "max_chars": max(char_counts) if char_counts else 0,
        "recovered_r1": recovered_r1,
        "recovered_r2": recovered_r2,
        "new_hit_rows": new_rows,
        "totals": dict(totals),
        "log": log,
        "ocr_subs_keys": sorted([f"EBC-2025-{r}-{s:04d}" for (r,s) in ocr_subs.keys()
                                 if (r==1 and s in r1_missing) or (r==2 and s in r2_missing)]),
    }


if __name__ == "__main__":
    result = run()
    (TEMP / "ocr_summary.json").write_text(json.dumps(result, indent=2, default=str))
    print("\nDONE")
    print(f"recovered: R1 {len(result['recovered_r1'])}/27, R2 {len(result['recovered_r2'])}/61")
    print(f"new hit rows: {len(result['new_hit_rows'])}")
    for k, v in result["totals"].items():
        print(f"  {k}: {v}")
