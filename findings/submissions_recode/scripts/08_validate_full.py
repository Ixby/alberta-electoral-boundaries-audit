"""Check one full-read batch file: every record read whole, fixed keys, quotes verbatim.

Entry: 2026-11-09 23:37 Alberta time · claude-fable-5-2 · medium

Usage: python3 08_validate_full.py F01        (or no argument: every batch)
"""
import csv
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))
ELEMENTS = {"AIRDRIE", "COCHRANE", "CHESTERMERE", "REDDEER", "RMH-A", "RMH-B",
            "OLDS-A", "OLDS-B", "STALBERT", "LETHBRIDGE", "LSL"}
PREFIX = {"AIRDRIE": "A", "COCHRANE": "C", "CHESTERMERE": "H", "REDDEER": "R",
          "RMH-A": "W", "RMH-B": "B", "OLDS-A": "O", "OLDS-B": "E",
          "STALBERT": "S", "LETHBRIDGE": "L", "LSL": "K"}
READ_KEYS = ["kind", "id", "source", "chars_read", "read_whole", "asks"]
CODE_KEYS = ["kind", "id", "source", "element", "reacts_to", "want", "rejects",
             "match_level", "needs_geometry", "quote", "page", "confidence", "note"]


def squash(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def load_texts():
    texts = {}
    for name in ("corpus", "hansard"):
        for line in open(os.path.join(ROOT, "data", "submissions", name + ".jsonl"),
                         encoding="utf-8"):
            r = json.loads(line)
            texts[r["id"]] = r.get("text") or ""
    return texts


def check(batch, texts):
    problems = []
    unit = list(csv.DictReader(open(os.path.join(HERE, "units_full", batch + ".csv"))))
    want_ids = {r["id"]: r for r in unit}
    path = os.path.join(HERE, "codes_full", batch + ".jsonl")
    if not os.path.exists(path):
        return [f"{batch}: no output file"], 0, 0
    seen_read, n_code = set(), 0
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except ValueError:
            problems.append(f"{batch}:{i}: not JSON")
            continue
        if i == 1:
            if "_stamp" not in r or not re.match(
                    r"\d{4}-\d\d-\d\d \d\d:\d\d Alberta time · \S+ · \S+", r["_stamp"]):
                problems.append(f"{batch}:1: first line must be the stamp")
            continue
        if "_stamp" in r:
            # A reader who resumes a batch adds its own stamp line.
            if not re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d Alberta time · \S+ · \S+", r["_stamp"]):
                problems.append(f"{batch}:{i}: bad stamp line")
            continue
        kind = r.get("kind")
        if r.get("id") not in want_ids:
            problems.append(f"{batch}:{i}: id {r.get('id')} is not in this batch")
            continue
        text = texts[r["id"]]
        if kind == "read":
            if list(r.keys()) != READ_KEYS:
                problems.append(f"{batch}:{i}: read keys must be {READ_KEYS}")
            if r.get("read_whole") and r.get("chars_read") != len(text):
                problems.append(f"{batch}:{i}: chars_read {r.get('chars_read')} != {len(text)}")
            seen_read.add(r["id"])
        elif kind == "code":
            n_code += 1
            if list(r.keys()) != CODE_KEYS:
                problems.append(f"{batch}:{i}: code keys must be {CODE_KEYS}")
                continue
            el = r["element"]
            if el not in ELEMENTS:
                problems.append(f"{batch}:{i}: unknown element {el}")
                continue
            opts = (r["want"] + " " + r["rejects"]).split()
            if r["want"] and len(r["want"].split()) != 1:
                problems.append(f"{batch}:{i}: want must be one option")
            for o in opts:
                if not re.fullmatch(PREFIX[el] + r"\d", o):
                    problems.append(f"{batch}:{i}: option {o} does not belong to {el}")
            if r["reacts_to"] not in ("CURRENT", "INTERIM", "IDEA", "NONE"):
                problems.append(f"{batch}:{i}: bad reacts_to")
            if r["match_level"] not in ("exact", "direction", ""):
                problems.append(f"{batch}:{i}: bad match_level")
            if r["confidence"] not in ("high", "medium", "low"):
                problems.append(f"{batch}:{i}: bad confidence")
            if opts and not r["quote"]:
                problems.append(f"{batch}:{i}: a want or rejects needs a quote")
            if r["quote"] and squash(r["quote"]) not in squash(text):
                problems.append(f"{batch}:{i}: quote not found verbatim in {r['id']}")
        else:
            problems.append(f"{batch}:{i}: kind must be read or code")
    for rid in want_ids:
        if rid not in seen_read:
            problems.append(f"{batch}: no read line for {rid}")
    return problems, len(seen_read), n_code


def main():
    texts = load_texts()
    batches = sys.argv[1:] or sorted(
        os.path.basename(p)[:-4] for p in glob.glob(os.path.join(HERE, "units_full", "F*.csv")))
    bad = 0
    for b in batches:
        problems, n_read, n_code = check(b, texts)
        for p in problems:
            print(p)
        bad += len(problems)
        print(f"{b}: {n_read} read lines, {n_code} code lines, {len(problems)} problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
