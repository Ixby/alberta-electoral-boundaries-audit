"""
Standalone analyzer that reads OCR page text files already produced by
v0_1_submission_ocr.py and performs the stitching + keyword search step.

Works even if the OCR run was interrupted — uses whatever pages are present.

Dependencies:
- Forward: None
- Backward: pymupdf (fitz), csv, json, pathlib
Produces:
  data/submission_search_dataset.csv (updated with source=ocr rows)
  analysis/v0_1_submission_ocr_log.md
"""

# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations
import sys, json, re, csv, time
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
TEMP = ROOT / ".temp" / "submissions"
OCR_DIR = TEMP / "ocr_pages"
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"

sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
from submission_search import (
    build_patterns,
    classify_position,
    R1_ID_PATTERNS,
    R2_ID_PATTERN,
)


def main():
    import fitz

    log = []
    # Load OCR page texts from disk
    ocr_pages = {}  # pdf_name -> {page_idx: text}
    total_chars = 0
    n_pages = 0
    for f in sorted(OCR_DIR.glob("*.txt")):
        stem = f.stem  # e.g. "EBC2025Submissions1-50ForPosting_p0001"
        m = re.match(r"(.+)_p(\d+)$", stem)
        if not m:
            continue
        pdf_stem = m.group(1)
        pidx_1based = int(m.group(2))
        pdf_name = f"{pdf_stem}.pdf"
        text = f.read_text(encoding="utf-8", errors="replace")
        ocr_pages.setdefault(pdf_name, {})[pidx_1based - 1] = text
        total_chars += len(text)
        n_pages += 1
    log.append(
        f"[load] {n_pages} OCR page files loaded, avg {total_chars/max(n_pages,1):.0f} chars/page"
    )

    R1_FILES = [
        ("EBC2025Submissions1-50ForPosting.pdf", 1, 50),
        ("EBC2025Submissions51-100ForPosting.pdf", 51, 100),
        ("EBC2025Submissions101-150ForPosting.pdf", 101, 150),
        ("EBC2025Submissions151-197ForPosting.pdf", 151, 197),
    ]
    R2_FILES = []
    for start in range(1, 1144, 50):
        end = min(start + 49, 1143)
        R2_FILES.append((f"EBC-2025-2-{start:03d}-to-{end:03d}.pdf", start, end))

    r1_missing = {
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        21,
        22,
        23,
        24,
        62,
        73,
        111,
        147,
        159,
        174,
        183,
        186,
        190,
        191,
        192,
        193,
        194,
        195,
        196,
        197,
    }
    r2_missing = {
        2,
        6,
        7,
        10,
        11,
        41,
        44,
        54,
        76,
        85,
        98,
        102,
        103,
        104,
        106,
        129,
        141,
        160,
        163,
        227,
        253,
        254,
        270,
        358,
        377,
        378,
        379,
        430,
        444,
        454,
        469,
        477,
        483,
        492,
        499,
        524,
        531,
        573,
        596,
        602,
        610,
        612,
        615,
        616,
        639,
        644,
        654,
        673,
        704,
        707,
        766,
        810,
        828,
        829,
        841,
        966,
        973,
        1048,
        1113,
        1122,
        1126,
    }

    ocr_subs = {}
    all_files = [(n, s, e, 1) for (n, s, e) in R1_FILES] + [
        (n, s, e, 2) for (n, s, e) in R2_FILES
    ]

    for pdf_name, start, end, rnd in all_files:
        pdf_path = TEMP / pdf_name
        if not pdf_path.exists():
            continue
        doc = fitz.open(pdf_path)
        pages = []
        for i, pg in enumerate(doc):
            tl = pg.get_text() or ""
            combined = tl
            if pdf_name in ocr_pages and i in ocr_pages[pdf_name]:
                combined = (tl + "\n" + ocr_pages[pdf_name][i]).strip()
            pages.append((i + 1, combined))
        doc.close()

        if rnd == 2:
            id_pat = R2_ID_PATTERN
            current = None
            accum = []
            for pnum, text in pages:
                m = id_pat.search(text)
                if m:
                    sid = int(m.group(1))
                    if start <= sid <= end and sid != current:
                        if current is not None:
                            ocr_subs[(2, current)] = "\n".join(accum)
                        current = sid
                        accum = [text]
                        continue
                if current is not None:
                    accum.append(text)
            if current is not None:
                ocr_subs[(2, current)] = "\n".join(accum)
        else:
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

    recovered_r1 = sorted(
        [sid for (r, sid) in ocr_subs if r == 1 and sid in r1_missing]
    )
    recovered_r2 = sorted(
        [sid for (r, sid) in ocr_subs if r == 2 and sid in r2_missing]
    )
    log.append(f"[recover] R1 recovered: {recovered_r1}")
    log.append(f"[recover] R2 recovered: {recovered_r2}")
    log.append(
        f"[recover] counts: R1 {len(recovered_r1)}/{len(r1_missing)}, R2 {len(recovered_r2)}/{len(r2_missing)}"
    )

    # Keyword search
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
                    s0 = max(0, m.start() - 150)
                    s1 = min(len(text), m.end() + 150)
                    snip = text[s0:s1].replace("\n", " ")
                    snippets.append((pk, classify_position(snip), snip))
                    break
        if any_hit:
            row["position_on_mentioned"] = snippets[0][1]
            row["relevant_quote"] = snippets[0][2].strip()[:280]
            new_rows.append(row)

    log.append(f"[hits] {len(new_rows)} OCR-sourced submissions with keyword hits")
    for k, v in totals.items():
        log.append(f"[hits] {k}: {v}")

    # Save per-submission OCR stitched text
    ocr_text_dir = TEMP / "ocr_text"
    ocr_text_dir.mkdir(exist_ok=True)
    for (rnd, sid), text in ocr_subs.items():
        if (rnd == 1 and sid in r1_missing) or (rnd == 2 and sid in r2_missing):
            (ocr_text_dir / f"EBC-2025-{rnd}-{sid:04d}.txt").write_text(
                text, encoding="utf-8", errors="replace"
            )

    # Update CSV — add source column to existing + append OCR rows
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
            if "source" not in r or not r.get("source"):
                r["source"] = "text_layer"
            w.writerow(r)
        for r in new_rows:
            for k in fields:
                r.setdefault(k, "")
            w.writerow(r)
    log.append(f"[out] wrote {len(new_rows)} OCR rows to {csv_path}")

    # Return summary
    return {
        "n_pages": n_pages,
        "total_chars": total_chars,
        "avg_chars": total_chars / max(n_pages, 1),
        "recovered_r1": recovered_r1,
        "recovered_r2": recovered_r2,
        "new_rows": new_rows,
        "totals": dict(totals),
        "log": log,
        "recovered_ids_all": sorted(
            [
                f"EBC-2025-{r}-{s:04d}"
                for (r, s) in ocr_subs.keys()
                if (r == 1 and s in r1_missing) or (r == 2 and s in r2_missing)
            ]
        ),
    }


if __name__ == "__main__":
    result = main()
    (TEMP / "ocr_analysis.json").write_text(json.dumps(result, indent=2, default=str))
    print(f"pages={result['n_pages']} avg_chars={result['avg_chars']:.0f}")
    print(
        f"recovered: R1 {len(result['recovered_r1'])}/27, R2 {len(result['recovered_r2'])}/61"
    )
    print(f"new hit rows: {len(result['new_rows'])}")
    for k, v in result["totals"].items():
        print(f"  {k}: {v}")
    print("\nHit submissions:")
    for r in result["new_rows"]:
        hits = [
            k.replace("mentions_", "")
            for k, v in r.items()
            if k.startswith("mentions_") and v is True or v == "True"
        ]
        print(
            f"  {r['submission_id']} [{r['position_on_mentioned']}]: {','.join(hits)}"
        )
