"""Count what the public asked for, from the full read of every record.

Entry: 2026-11-10 01:00 Alberta time (requests split added 01:03) · claude-opus-5-5 · medium

Reads codes_full/F*.jsonl (every submission and hearing record, read whole),
derives each row's code for the minority and the majority map by CODEBOOK.md
section 5 (the same rule as 06_merge_codes.py), and counts records per
element. It then compares the full read with the earlier double coding
(merged_codes.csv, with the adjudicated rows from adjudication/part*.jsonl
replacing the disputed pairs) on the (record, element) pairs both covered.

Outputs (in findings/submissions_recode/):
  full_read_codes.csv      one row per (record, element) the full read coded
  full_read_results.json   counts per element, the comparison, and meta
  full_read_results.md     the same counts as plain tables
"""
import collections
import csv
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module  # noqa: E402

merge = import_module("06_merge_codes")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELEMENTS = ["AIRDRIE", "COCHRANE", "CHESTERMERE", "REDDEER", "RMH-A", "RMH-B",
            "OLDS-A", "OLDS-B", "STALBERT", "LETHBRIDGE", "LSL"]
STAMP = "2026-11-10 01:00 Alberta time · claude-opus-5-5 · medium"
LABEL = {0: "not_mentioned", 1: "no_stance", 2: "supports", 3: "opposes",
         4: "third_arrangement", None: "pending_geometry"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def opts(s):
    return re.findall(r"\b[A-Z]\d\b", s or "")


def derive_row(want, rejects, needs_geometry):
    w, r = opts(want), opts(rejects)
    pending = bool(needs_geometry) and not [x for x in w if x in merge.TAGS]
    return (merge.derive(1, w, r, "MIN", pending),
            merge.derive(1, w, r, "MAJ", pending))


def main():
    inputs = sorted(glob.glob(os.path.join(HERE, "codes_full", "F*.jsonl")))
    read, rows = {}, []
    for path in inputs:
        for line in open(path, encoding="utf-8"):
            r = json.loads(line)
            if "_stamp" in r:
                continue
            if r["kind"] == "read":
                read[r["id"]] = r
            else:
                cm, cj = derive_row(r["want"], r["rejects"], r["needs_geometry"])
                rows.append({
                    "id": r["id"], "source": r["source"], "element": r["element"],
                    "reacts_to": r["reacts_to"], "want": r["want"],
                    "rejects": r["rejects"], "match_level": r["match_level"],
                    "needs_geometry": r["needs_geometry"],
                    "code_minority": cm, "code_majority": cj,
                    "confidence": r["confidence"],
                })
    # One row per (record, element): a reader may have written two lines.
    keyed = {}
    for r in rows:
        keyed.setdefault((r["id"], r["element"]), r)
    rows = list(keyed.values())
    with open(os.path.join(HERE, "full_read_codes.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["element"], r["id"])))

    n_read = len(read)
    n_whole = sum(1 for r in read.values() if r["read_whole"])
    results = {}
    for el in ELEMENTS:
        er = [r for r in rows if r["element"] == el]
        res = {"records_naming_it": len(er)}
        for which in ("minority", "majority"):
            c = collections.Counter(LABEL[r["code_" + which]] for r in er)
            exact = collections.Counter(
                LABEL[r["code_" + which]] for r in er if r["match_level"] == "exact")
            rej_only = sum(1 for r in er if r["rejects"] and not r["want"]
                           and r["code_" + which] == 3)
            res[which] = {
                "supports": c["supports"], "supports_exact": exact["supports"],
                "opposes": c["opposes"], "opposes_exact": exact["opposes"],
                "opposes_by_rejection_only": rej_only,
                "third_arrangement": c["third_arrangement"],
                "no_stance": c["no_stance"],
                "pending_geometry": c["pending_geometry"],
            }
        split = collections.Counter()
        for r in er:
            w = opts(r["want"])
            if not w:
                split["argues_against_only" if opts(r["rejects"]) else "no_request"] += 1
                continue
            t = merge.TAGS.get(w[0], set())
            split["both_maps" if t == {"MAJ", "MIN"} else "minority_only" if t == {"MIN"}
                  else "majority_only" if t == {"MAJ"} else "something_else"] += 1
        res["requests"] = {k: split[k] for k in ("minority_only", "majority_only", "both_maps",
                                                 "something_else", "argues_against_only", "no_request")}
        res["wants"] = dict(sorted(collections.Counter(
            r["want"] for r in er if r["want"]).items()))
        res["rejects"] = dict(sorted(collections.Counter(
            o for r in er for o in opts(r["rejects"])).items()))
        results[el] = res

    # Comparison with the double coding, adjudicated rows replacing disputes.
    dbl = collections.defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(HERE, "merged_codes.csv"), encoding="utf-8")):
        dbl[(r["id"], r["element"])][r["coder"]] = r
    adj = {}
    for p in glob.glob(os.path.join(HERE, "adjudication", "part*.jsonl")):
        for line in open(p, encoding="utf-8"):
            a = json.loads(line)
            if "_stamp" in a:
                continue
            adj[(a["id"], a["element"])] = derive_row(
                a.get("want", ""), a.get("rejects", ""), a.get("needs_geometry", 0))

    def stance(c):
        return "n" if c in (0, 1) else str(c)

    comp = collections.Counter()
    differ = []
    for (rid, el), v in dbl.items():
        if len(v) != 2 or rid not in read:
            continue
        if (rid, el) in adj:
            ref = adj[(rid, el)]
        elif (v["A"]["code_minority"], v["A"]["code_majority"]) == (
                v["B"]["code_minority"], v["B"]["code_majority"]):
            ref = tuple(None if x == "" else int(x) for x in
                        (v["A"]["code_minority"], v["A"]["code_majority"]))
        else:
            continue
        fr = keyed.get((rid, el))
        full = (fr["code_minority"], fr["code_majority"]) if fr else (0, 0)
        same = tuple(map(stance, ref)) == tuple(map(stance, full))
        comp["agree" if same else "differ"] += 1
        if not same:
            differ.append({"id": rid, "element": el,
                           "double_coding": list(ref), "full_read": list(full)})
    out = {
        "meta": {
            "entry": STAMP,
            "script": "findings/submissions_recode/scripts/09_full_read_results.py",
            "inputs": {os.path.relpath(p, HERE): sha(p) for p in inputs},
            "rule": "CODEBOOK.md section 5, as in 06_merge_codes.py",
        },
        "records_read": n_read, "records_read_whole": n_whole,
        "elements": results,
        "comparison_with_double_coding": {
            "pairs_compared": comp["agree"] + comp["differ"],
            "stance_agrees": comp["agree"], "stance_differs": comp["differ"],
            "differences": differ,
        },
    }
    json.dump(out, open(os.path.join(HERE, "full_read_results.json"), "w"), indent=1)

    req = ["| Place | Records naming it | Asks for what only the minority drew | Only the majority | Both maps | Something else | Argues against, asks nothing | No request |",
           "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for el in ELEMENTS:
        q = results[el]["requests"]
        req.append(f"| {el} | {results[el]['records_naming_it']} | {q['minority_only']} | {q['majority_only']} | "
                   f"{q['both_maps']} | {q['something_else']} | {q['argues_against_only']} | {q['no_request']} |")
    lines = [f"# Full read: what the public asked for, by place\n\n{STAMP}\n",
             f"Records read: {n_read} ({n_whole} read whole).\n",
             "## What each record asks for\n"] + req + [
             "\n## Derived codes, each map in turn (support includes requests both maps meet; exact in brackets)\n",
             "| Place | Records naming it | Support minority (exact) | Oppose minority (exact) | "
             "Support majority (exact) | Oppose majority (exact) | Something else | No stance |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for el in ELEMENTS:
        r = results[el]
        m, j = r["minority"], r["majority"]
        lines.append(f"| {el} | {r['records_naming_it']} | {m['supports']} ({m['supports_exact']}) | "
                     f"{m['opposes']} ({m['opposes_exact']}) | {j['supports']} ({j['supports_exact']}) | "
                     f"{j['opposes']} ({j['opposes_exact']}) | {m['third_arrangement']} | {m['no_stance']} |")
    c = out["comparison_with_double_coding"]
    lines.append(f"\nAgainst the double coding (adjudicated): {c['stance_agrees']} of "
                 f"{c['pairs_compared']} pairs give the same stance.\n")
    open(os.path.join(HERE, "full_read_results.md"), "w").write("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
