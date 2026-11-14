# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
"""
submissions.py
--------------
Entry: 2026-11-10 21:47 Alberta time · claude-opus-5-5 · medium

What the public submissions and hearing records ask about First Nations reserves, Métis
settlements and nations, and whether each final map does it. Descriptive; not registered; no
judgement of intent.

Inputs (submissions_codes/):
  candidates.csv     the 630 records a keyword screen found (written and hearing)
  reads/R*.jsonl     each record read whole by an AI agent (READ_BRIEF.md); one line per record
  map_tests/out_M*.jsonl  each relevant record's request tested on four maps (MAPPING_BRIEF.md)
  review/review_*.jsonl   an independent agent's changes to those tests (REVIEW_BRIEF.md); applied here
  ../placements_all.csv   which district holds each reserve and Métis settlement on each map
Outputs: submissions.csv (one row per relevant record), submissions_counts.json.
"""
import collections
import csv
import glob
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = HERE / "submissions_codes"
STAMP = "2026-11-10 21:47 Alberta time · claude-opus-5-5 · medium"
MAPS = ["map_2019", "majority", "minority", "panel"]
# Group tags from the community each record names. A record can carry several.
GROUPS = [
    ("Enoch Cree Nation", r"enoch"),
    ("Tsuut'ina", r"tsuu|sarcee"),
    ("Stoney Nakoda (Morley, Eden Valley, Big Horn)", r"stoney|nakoda|morley|mini thni|eden valley|big ?horn|bearspaw|chiniki|wesley|goodstoney"),
    ("O'Chiese and Sunchild", r"o.chiese|sunchild|west of rocky"),
    ("Blackfoot (Siksika, Kainai, Piikani)", r"siksika|kainai|blood|piikani|peigan|blackfoot"),
    ("Maskwacis and Pigeon Lake", r"maskwacis|samson|ermineskin|louis bull|montana|pigeon lake"),
    ("Lesser Slave Lake nations and settlements", r"lesser slave|sawridge|driftpile|sucker creek|swan river|kapawe|slave lake|big lakes|east prairie|peavine|gift lake|bigstone|joussard"),
    ("Kee Tas Kee Now nations (Woodland Cree, Lubicon and others)", r"woodland cree|lubicon|kee tas|ktc|loon lake|peerless|atikameg"),
    ("North Peace and the proposed Mackenzie district", r"north peace|mackenzie|dene tha|little red river|tall ?cree|beaver first|high level"),
    ("Saddle Lake, Whitefish Lake, Buffalo Lake, Kikino and the northeast", r"saddle lake|white ?fish lake|buffalo lake|kikino|heart lake|beaver lake|frog lake|onion lake|fishing lake|northeast|cold lake|kehewin"),
    ("Alexander, Alexis, Paul (Wabamun)", r"alexander|alexis|wabamun|paul first"),
    ("Fort McKay and Wood Buffalo", r"fort mckay|fort chipewyan|janvier|anzac|conklin|wood buffalo|fort mcmurray"),
    ("Horse Lake and Sturgeon Lake", r"horse lake|sturgeon lake"),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(pattern):
    out = []
    for p in sorted(glob.glob(str(C / pattern))):
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            if "_stamp" not in r:
                out.append(r)
    return out


def main():
    reads = load("reads/R*.jsonl")
    tests = {t["id"]: t for t in load("map_tests/out_M*.jsonl")}
    review = load("review/review_*.jsonl")
    n_cand = sum(1 for _ in open(C / "candidates.csv", encoding="utf-8")) - 1
    assert len(reads) == n_cand and len({r["id"] for r in reads}) == n_cand
    rel = {r["id"]: dict(r) for r in reads if r["relevant"]}
    assert set(rel) == set(tests)
    applied = []
    for ch in review:
        target = tests[ch["id"]] if ch["field"] in MAPS + ["test", "confidence"] else rel[ch["id"]]
        target[ch["field"]] = ch["new"]
        applied.append(ch)
    rows = []
    for rid, r in sorted(rel.items()):
        t = tests[rid]
        groups = [g for g, pat in GROUPS if re.search(pat, r["community"] + " " + r["request"], re.I)] or ["General or unnamed"]
        rows.append({
            "id": rid, "source": r["source"], "submitter_type": r["submitter"],
            "submitter": r["submitter_note"], "community": r["community"], "groups": "; ".join(groups),
            "request": r["request"], "request_type": r["request_type"], "quote": r["quote"], "page": r["page"],
            "read_confidence": r["confidence"], "test": t["test"],
            "map_2019": t["map_2019"], "commission_majority": t["majority"],
            "commission_minority": t["minority"], "panel_reconstruction": t["panel"],
            "test_confidence": t["confidence"], "test_reason": t["reason"],
        })
    with open(HERE / "submissions.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    cols = ["map_2019", "commission_majority", "commission_minority", "panel_reconstruction"]
    def tally(rs):
        return {m: dict(collections.Counter(x[m] for x in rs)) for m in cols}
    by_group = {}
    for g in [g for g, _ in GROUPS] + ["General or unnamed"]:
        rs = [x for x in rows if g in x["groups"].split("; ")]
        if rs:
            by_group[g] = {"records": len(rs),
                           "by_submitter_type": dict(collections.Counter(x["submitter_type"] for x in rs)),
                           "verdicts": tally(rs),
                           "nation_or_council_ids": [x["id"] for x in rs if x["submitter_type"] == "nation_or_council"]}
    out = {
        "meta": {"entry": STAMP, "script": "findings/reserves_by_map/submissions.py",
                 "inputs": {str(Path(p).relative_to(HERE)): sha(p) for p in
                            sorted(glob.glob(str(C / "**" / "*.jsonl"), recursive=True)) + [str(C / "candidates.csv"), str(HERE / "placements_all.csv")]},
                 "review_changes_applied": len(applied)},
        "records_screened": n_cand, "records_read_whole": sum(1 for r in reads if r["read_whole"]),
        "records_relevant": len(rows),
        "relevant_by_submitter_type": dict(collections.Counter(x["submitter_type"] for x in rows)),
        "relevant_by_source": dict(collections.Counter(x["source"] for x in rows)),
        "verdicts_all": tally(rows),
        "verdicts_nation_or_council": tally([x for x in rows if x["submitter_type"] == "nation_or_council"]),
        "by_group": by_group,
    }
    json.dump(out, open(HERE / "submissions_counts.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ["records_screened", "records_read_whole", "records_relevant",
                                          "relevant_by_submitter_type", "verdicts_all"]}, indent=1))


if __name__ == "__main__":
    main()
