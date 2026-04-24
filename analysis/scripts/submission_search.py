"""
v0_1 submission keyword search
Downloads all 27 EBC submission batch PDFs, extracts text per submission,
and runs keyword regexes to verify/refute the chair's claim that the minority's
hybrid configurations (Airdrie 4-way, Nolan-Hill-Cochrane, RMH-Banff,
Olds-Three-Hills-Didsbury, Chestermere, Red Deer hybrids, St. Albert-Sturgeon)
had NO public support in the submissions.

Dependencies:
- Forward: None
- Backward: pdfplumber, re, urllib, csv, pathlib
Produces:
  data/submission_search_dataset.csv
  analysis/reports/submission_search_findings.md
  analysis/methodology/submission_search_log.md

Usage:
  python analysis/scripts/submission_search.py [--phase={download|parse|search|all}]
"""
from __future__ import annotations
import os
import re
import csv
import sys
import json
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
TEMP = ROOT / ".temp" / "submissions"
TEXT = TEMP / "text"
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
TEMP.mkdir(parents=True, exist_ok=True)
TEXT.mkdir(parents=True, exist_ok=True)

BASE = "https://www.elections.ab.ca/uploads/"
UA = {"User-Agent": "Mozilla/5.0 (audit-research; public-interest)"}

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


def download_one(name: str) -> Path:
    out = TEMP / name
    if out.exists() and out.stat().st_size > 1000:
        return out
    url = BASE + urllib.parse.quote(name)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r, open(out, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    return out


def download_all(log):
    for name, _, _ in R1_FILES + R2_FILES:
        try:
            p = download_one(name)
            log.append(f"[download] OK {p.stat().st_size:>10,} {name}")
        except Exception as e:
            log.append(f"[download] FAIL {name}: {e!r}")


R1_ID_PATTERNS = [
    # actual format in PDFs: "EBC 2025-1-008" or "EBC-2025-1-010"
    re.compile(r"\bEBC[-\s]?2025[-\s]?1[-\s]?0*(\d{1,3})\b", re.I),
    # fallbacks
    re.compile(r"^\s*Submission\s*#?\s*(\d{1,3})\b", re.I | re.M),
]
R2_ID_PATTERN = re.compile(r"\bEBC[-\s]?2025[-\s]?2[-\s]?0*(\d{1,4})\b", re.I)


def extract_r2_pdf(pdf_path: Path, start: int, end: int, log):
    import pdfplumber
    # Build a flat list of (page_num, page_text)
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for pi, p in enumerate(pdf.pages):
                t = p.extract_text() or ""
                pages.append((pi + 1, t))
    except Exception as e:
        log.append(f"[parse-R2] FAIL {pdf_path.name}: {e!r}")
        return {}

    # Identify submission boundaries by EBC-2025-2-XXX markers
    current = None
    current_start_page = None
    accum = []
    subs = {}  # id_int -> (start_page, end_page, text, source)
    last_match_id = None
    for pnum, text in pages:
        m = R2_ID_PATTERN.search(text)
        if m:
            sid = int(m.group(1))
            if start <= sid <= end and sid != current:
                # close prior
                if current is not None:
                    subs[current] = (current_start_page, pnum - 1, "\n".join(accum), pdf_path.name)
                current = sid
                current_start_page = pnum
                accum = [text]
                last_match_id = sid
                continue
        if current is not None:
            accum.append(text)
    if current is not None:
        subs[current] = (current_start_page, pages[-1][0], "\n".join(accum), pdf_path.name)
    log.append(f"[parse-R2] {pdf_path.name}: {len(subs)} submissions detected (expected up to {end-start+1})")
    return subs


def extract_r1_pdf(pdf_path: Path, start: int, end: int, log):
    import pdfplumber
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for pi, p in enumerate(pdf.pages):
                t = p.extract_text() or ""
                pages.append((pi + 1, t))
    except Exception as e:
        log.append(f"[parse-R1] FAIL {pdf_path.name}: {e!r}")
        return {}

    # R1 has fewer explicit IDs; try to split by "Submission #N" or similar headers.
    # Fall back: concatenate all text under a single synthetic ID per file.
    subs = {}
    current = None
    current_start_page = None
    accum = []
    for pnum, text in pages:
        matched_id = None
        for pat in R1_ID_PATTERNS:
            m = pat.search(text)
            if m:
                n = int(m.group(1))
                if start <= n <= end:
                    matched_id = n
                    break
        if matched_id is not None and matched_id != current:
            if current is not None:
                subs[current] = (current_start_page, pnum - 1, "\n".join(accum), pdf_path.name)
            current = matched_id
            current_start_page = pnum
            accum = [text]
        else:
            if current is not None:
                accum.append(text)
            else:
                # text before first header — skip or bucket to synthetic "pre"
                pass
    if current is not None:
        subs[current] = (current_start_page, pages[-1][0], "\n".join(accum), pdf_path.name)

    if not subs:
        # Fallback: dump all text as single pseudo-submission with range
        total = "\n".join(t for _, t in pages)
        if total.strip():
            synthetic = start  # tag with the file's start id as a sentinel
            subs[synthetic] = (1, pages[-1][0] if pages else 0, total, pdf_path.name + " [unsplit]")

    log.append(f"[parse-R1] {pdf_path.name}: {len(subs)} submissions detected (expected up to {end-start+1})")
    return subs


def parse_all(log):
    """Extract text and write per-submission text files."""
    r1_subs = {}  # id -> (start_page, end_page, text, source)
    for name, start, end in R1_FILES:
        p = TEMP / name
        if not p.exists():
            log.append(f"[parse-R1] SKIP missing {name}")
            continue
        subs = extract_r1_pdf(p, start, end, log)
        r1_subs.update(subs)

    r2_subs = {}
    for name, start, end in R2_FILES:
        p = TEMP / name
        if not p.exists():
            log.append(f"[parse-R2] SKIP missing {name}")
            continue
        subs = extract_r2_pdf(p, start, end, log)
        r2_subs.update(subs)

    # Write text files
    for sid, (sp, ep, txt, src) in r1_subs.items():
        fn = TEXT / f"EBC-2025-1-{sid:04d}.txt"
        fn.write_text(txt, encoding="utf-8", errors="replace")
    for sid, (sp, ep, txt, src) in r2_subs.items():
        fn = TEXT / f"EBC-2025-2-{sid:04d}.txt"
        fn.write_text(txt, encoding="utf-8", errors="replace")

    log.append(f"[parse] R1 submissions: {len(r1_subs)}, R2 submissions: {len(r2_subs)}")
    # persist metadata
    meta = {
        "r1": {f"{k}": {"start_page": v[0], "end_page": v[1], "source": v[3]} for k, v in r1_subs.items()},
        "r2": {f"{k}": {"start_page": v[0], "end_page": v[1], "source": v[3]} for k, v in r2_subs.items()},
    }
    (TEMP / "submission_meta.json").write_text(json.dumps(meta, indent=2))
    return r1_subs, r2_subs


# Keyword patterns — checked against lowercased text
def build_patterns():
    return {
        "airdrie_4way_split": [
            # explicit 4-way
            re.compile(r"airdrie[\s\S]{0,120}(four[-\s]?way|4[-\s]?way|split\s+into\s+four|split\s+into\s+4|four\s+districts|4\s+districts|four\s+ridings|4\s+ridings)", re.I),
            re.compile(r"(split(ting)?|divid(e|ing|ed)|carv(e|ing|ed))[\s\S]{0,80}airdrie[\s\S]{0,120}(four|4)\b", re.I),
            # any discussion of splitting/dividing Airdrie (broader — catches 2-way or 4-way critiques)
            re.compile(r"(split(ting)?|divid(e|ing|ed)|carv(e|ing|ed)|break(ing)?\s+up|fragment)[\s\S]{0,60}(the\s+city\s+of\s+)?airdrie", re.I),
            re.compile(r"airdrie[\s\S]{0,80}(should|must|can)\s*(not|n'?t)?\s*be\s*(split|divid|broken|fragment)", re.I),
        ],
        "nolan_hill_cochrane": [
            # Nolan Hill + Cochrane in same sentence / short window
            re.compile(r"nolan\s+hill[\s\S]{0,200}cochrane", re.I),
            re.compile(r"cochrane[\s\S]{0,200}nolan\s+hill", re.I),
        ],
        "rmh_banff_park": [
            re.compile(r"rocky\s+mountain\s+house[\s\S]{0,200}(banff|national\s+park|park)", re.I),
            re.compile(r"(banff|national\s+park)[\s\S]{0,200}rocky\s+mountain\s+house", re.I),
        ],
        "olds_three_hills_didsbury": [
            re.compile(r"(olds|didsbury|three\s+hills)[\s\S]{0,300}airdrie", re.I),
            re.compile(r"airdrie[\s\S]{0,300}(olds|didsbury|three\s+hills)", re.I),
        ],
        "chestermere_split": [
            re.compile(r"chestermere[\s\S]{0,200}(split|divid|calgary|peigan|forest\s+lawn)", re.I),
            re.compile(r"(split|divid|calgary)[\s\S]{0,80}chestermere", re.I),
        ],
        "red_deer_hybrids": [
            re.compile(r"red\s+deer[\s\S]{0,200}(blackfalds|innisfail|sylvan\s+lake|lacombe)", re.I),
            re.compile(r"(blackfalds|innisfail|sylvan\s+lake|lacombe)[\s\S]{0,200}red\s+deer", re.I),
        ],
        "st_albert_sturgeon": [
            re.compile(r"st\.?\s+albert[\s\S]{0,200}sturgeon", re.I),
            re.compile(r"sturgeon[\s\S]{0,200}st\.?\s+albert", re.I),
        ],
    }


SUPPORT_WORDS = re.compile(
    r"\b(support|in\s+favou?r|endorse|agree\s+with|should\s+be|makes\s+sense|good\s+idea|prefer|recommend(ed|ing)?|accept)\b",
    re.I,
)
OPPOSE_WORDS = re.compile(
    r"\b(oppose|against|disagree|reject|do\s+not\s+support|don'?t\s+support|object|wrong|bad\s+idea|unacceptable|harm(s|ful)?|should\s+not|must\s+not|problem(atic)?|concern(ed|s)?|against\s+the\s+proposal)\b",
    re.I,
)


def classify_position(snippet: str) -> str:
    s = snippet
    sup = len(SUPPORT_WORDS.findall(s))
    opp = len(OPPOSE_WORDS.findall(s))
    if sup == 0 and opp == 0:
        return "neutral"
    if sup > 0 and opp == 0:
        return "supporting"
    if opp > 0 and sup == 0:
        return "opposing"
    # both present
    if sup > opp:
        return "ambiguous-leaning-support"
    if opp > sup:
        return "ambiguous-leaning-oppose"
    return "ambiguous"


def search_submissions(log):
    pats = build_patterns()
    rows = []
    totals = defaultdict(int)
    pos_counts = defaultdict(lambda: defaultdict(int))
    files_searched = 0

    for txt_file in sorted(TEXT.glob("*.txt")):
        files_searched += 1
        text = txt_file.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            continue
        stem = txt_file.stem  # e.g. EBC-2025-2-0042
        parts = stem.split("-")
        try:
            rnd = int(parts[2])  # "1" or "2"
            sid = int(parts[3])
        except Exception:
            rnd, sid = 0, 0

        row = {
            "submission_id": stem,
            "round": rnd,
            "source_file": "",  # filled below
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
        }
        any_hit = False
        snippets = []

        keymap = {
            "airdrie_4way_split": "mentions_airdrie_4way_split",
            "nolan_hill_cochrane": "mentions_nolan_hill_cochrane",
            "rmh_banff_park": "mentions_rmh_banff_park",
            "olds_three_hills_didsbury": "mentions_olds_three_hills_didsbury",
            "chestermere_split": "mentions_chestermere_split",
            "red_deer_hybrids": "mentions_red_deer_hybrids",
            "st_albert_sturgeon": "mentions_st_albert_sturgeon",
        }

        for pat_key, regs in pats.items():
            for rg in regs:
                m = rg.search(text)
                if m:
                    row[keymap[pat_key]] = True
                    any_hit = True
                    totals[pat_key] += 1
                    # 300-char window around match
                    s0 = max(0, m.start() - 150)
                    s1 = min(len(text), m.end() + 150)
                    snip = text[s0:s1].replace("\n", " ")
                    pos = classify_position(snip)
                    pos_counts[pat_key][pos] += 1
                    snippets.append((pat_key, pos, snip))
                    break  # one hit per configuration per submission

        if any_hit:
            # pick first snippet as "relevant_quote"; use the pos from first hit as primary
            first_pat, first_pos, first_snip = snippets[0]
            row["position_on_mentioned"] = first_pos
            quote = first_snip.strip()
            # trim to 280 chars for CSV readability
            row["relevant_quote"] = quote[:280]
            rows.append(row)

    # load page-range / source metadata
    meta_path = TEMP / "submission_meta.json"
    meta = {}
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
    for r in rows:
        sid = r["submission_id"]
        # key is the int id
        key = str(int(sid.split("-")[-1]))
        rnd_k = "r1" if r["round"] == 1 else "r2"
        m = meta.get(rnd_k, {}).get(key)
        if m:
            r["source_file"] = m.get("source", "")
            r["page_range"] = f"{m.get('start_page','')}-{m.get('end_page','')}"

    log.append(f"[search] files_searched={files_searched} rows_with_hits={len(rows)}")
    for k, v in totals.items():
        log.append(f"[search] {k}: {v} mentions")

    return rows, totals, pos_counts, files_searched


def write_outputs(rows, totals, pos_counts, files_searched, log):
    DATA.mkdir(exist_ok=True)
    csv_path = DATA / "submission_search_dataset.csv"
    fields = [
        "submission_id", "round", "source_file", "page_range",
        "mentions_airdrie_4way_split", "mentions_nolan_hill_cochrane",
        "mentions_rmh_banff_park", "mentions_olds_three_hills_didsbury",
        "mentions_chestermere_split", "mentions_red_deer_hybrids",
        "mentions_st_albert_sturgeon",
        "position_on_mentioned", "relevant_quote",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
        # summary row
        summary = {k: "" for k in fields}
        summary["submission_id"] = "__SUMMARY__"
        summary["round"] = 0
        summary["source_file"] = f"files_with_hits={len(rows)} files_searched={files_searched}"
        summary["page_range"] = ""
        summary["mentions_airdrie_4way_split"] = totals.get("airdrie_4way_split", 0)
        summary["mentions_nolan_hill_cochrane"] = totals.get("nolan_hill_cochrane", 0)
        summary["mentions_rmh_banff_park"] = totals.get("rmh_banff_park", 0)
        summary["mentions_olds_three_hills_didsbury"] = totals.get("olds_three_hills_didsbury", 0)
        summary["mentions_chestermere_split"] = totals.get("chestermere_split", 0)
        summary["mentions_red_deer_hybrids"] = totals.get("red_deer_hybrids", 0)
        summary["mentions_st_albert_sturgeon"] = totals.get("st_albert_sturgeon", 0)
        summary["position_on_mentioned"] = ""
        summary["relevant_quote"] = "counts per configuration"
        w.writerow(summary)
    log.append(f"[out] wrote {csv_path}")
    return csv_path


def main():
    log = []
    phase = "all"
    for a in sys.argv[1:]:
        if a.startswith("--phase="):
            phase = a.split("=", 1)[1]

    if phase in ("download", "all"):
        download_all(log)
    if phase in ("parse", "all"):
        parse_all(log)
    if phase in ("search", "all"):
        rows, totals, pos_counts, n = search_submissions(log)
        csv_path = write_outputs(rows, totals, pos_counts, n, log)
        # persist intermediate JSON for findings writer
        (TEMP / "search_result.json").write_text(json.dumps({
            "totals": dict(totals),
            "pos_counts": {k: dict(v) for k, v in pos_counts.items()},
            "files_searched": n,
            "rows_count": len(rows),
            "rows": rows,
        }, indent=2))
    # write log
    (ANALYSIS / "submission_search_log.md").write_text(
        "# submission_search log\n\n" + "\n".join(log) + "\n", encoding="utf-8"
    )
    print("\n".join(log[-30:]))


if __name__ == "__main__":
    main()
