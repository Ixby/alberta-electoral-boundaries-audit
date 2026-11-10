"""Merge the two coders' files into one table and derive the codes by one rule.

Entry: 2026-11-09 23:34 Alberta time · claude-fable-5-2 · medium

The coders wrote their sheets in slightly different layouts, and some filled
the derived codes by hand. This script ignores the hand-filled codes. It reads
only what each coder recorded (mentions, want, rejects, match level) and
derives the minority and majority codes itself, by CODEBOOK.md section 5, so
that both coders are scored by the same rule.

Two points the codebook leaves open are settled here and reported, not hidden:
  * A row that wants an option both maps adopt but explicitly rejects one
    map's own option is coded 3 (opposes) for that map. The explicit rejection
    is the more specific statement.
  * A row with a rejection and no want is coded 3 for a map whose option it
    rejects, and 1 (no stance) for the other map. Such rows are counted
    separately as `rejects_only`.

Outputs (in findings/submissions_recode/):
  merged_codes.csv   one row per (record, element, coder)
  agreement.json     per element: counts by coder, agreement, Cohen's kappa
  disagreements.csv  pairs where the two coders' derived codes differ
"""
import collections
import csv
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Which final maps adopt each option (CODEBOOK.md section 4).
TAGS = {
    "A1": {"MAJ"}, "A2": {"MIN"},
    "C1": {"MAJ"}, "C2": {"MIN"},
    "H1": {"MAJ"}, "H2": {"MIN"},
    "R1": {"MAJ"}, "R2": {"MIN"},
    "W0": {"MAJ", "MIN"}, "W1": {"MIN"}, "W2": {"MAJ"},
    "B1": {"MIN"}, "B2": {"MAJ"},
    "O1": {"MIN"}, "O2": {"MAJ"},
    "E1": {"MIN"}, "E2": {"MAJ"},
    "S0": {"MAJ", "MIN"}, "S1": {"MAJ"}, "S2": {"MIN"},
    "L1": {"MAJ"}, "L2": {"MIN"},
    "K1": {"MAJ", "MIN"},
}
PREFIX_ELEMENT = {"W": "RMH-A", "B": "RMH-B", "O": "OLDS-A", "E": "OLDS-B"}
SPLIT = {"RMH": ["RMH-A", "RMH-B"], "OLDS": ["OLDS-A", "OLDS-B"]}
OPT = re.compile(r"\b([A-Z]\d)\b")


def opts(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        value = " ".join(str(v) for v in value)
    return OPT.findall(str(value))


def first(d, *names, default=""):
    for n in names:
        if n in d and d[n] not in (None, ""):
            return d[n]
    return default


def stated_code(d, which):
    """The coder's own hand-filled code for one map, or None.

    Used only to infer `mentions`, and to keep a bare opposition where the
    coder's sheet has no `rejects` field. A plain `code` is the minority code
    (the coder brief's convention); the majority code is taken only from
    `code_majority`, a two-part `code`, or a "maj=N" in the note.
    """
    v = d.get("code_" + which)
    if v in (None, ""):
        v = d.get("code")
        if isinstance(v, dict):
            v = v.get(which)
        elif isinstance(v, str) and not v.strip().isdigit():
            m = re.search(which[:3] + r"\w*\s*[:=]?\s*(\d)", v, re.I)
            if not m:
                parts = re.findall(r"\d", v)
                m2 = parts[0 if which == "minority" else 1] if len(parts) == 2 else None
                v = int(m2) if m2 else None
            else:
                v = int(m.group(1))
        elif which == "majority":
            m = re.search(r"maj\w*\s*[:=]\s*(\d)", str(d.get("note", "")), re.I)
            v = int(m.group(1)) if m else None
    if isinstance(v, str):
        v = int(v) if v.strip().isdigit() else None
    return v


def element_rows(rec):
    """Yield (element, fields) for one JSON line."""
    conf = rec["configuration"]
    if conf not in SPLIT:
        yield conf, rec
        return
    nested = rec.get("elements")
    for el in SPLIT[conf]:
        if isinstance(nested, dict) and el in nested:
            sub = dict(nested[el])
        elif el == "OLDS-B" and isinstance(rec.get("olds_b"), dict):
            sub = dict(rec["olds_b"])
        elif el == "OLDS-A" and "olds_b" in rec:
            sub = dict(rec)
        else:
            sub = {}
        # Top-level wants and rejects, split by option letter, fill any gap.
        letter = [k for k, v in PREFIX_ELEMENT.items() if v == el][0]
        if not opts(first(sub, "want", "wants")):
            top = [o for o in opts(first(rec, "wants", "want")) if o[0] == letter]
            if top:
                sub["want"] = " ".join(top)
        if not opts(sub.get("rejects")):
            top = [o for o in opts(rec.get("rejects")) if o[0] == letter]
            if top:
                sub["rejects"] = " ".join(top)
        for k in ("confidence", "note", "source"):
            sub.setdefault(k, rec.get(k, ""))
        if "mentions" not in sub and "code_minority" not in sub:
            code = rec.get("code")
            if isinstance(code, dict) and el in code:
                sub["code_minority"] = code[el].get("minority")
            elif isinstance(code, str):
                m = re.search(re.escape(el) + r"\s*min(\d)", code)
                if m:
                    sub["code_minority"] = int(m.group(1))
        yield el, sub


def derive(mentions, want, rejects, which, pending):
    if not mentions:
        return 0
    if pending:
        return None
    tagged_want = [w for w in want if w in TAGS]
    rejects_m = any(which in TAGS.get(r, ()) for r in rejects)
    if rejects_m:
        return 3
    if any(which in TAGS[w] for w in tagged_want):
        return 2
    if tagged_want:
        return 3
    if want:
        return 4
    return 1


def kappa(pairs):
    n = len(pairs)
    if not n:
        return None
    agree = sum(a == b for a, b in pairs) / n
    ca = collections.Counter(a for a, _ in pairs)
    cb = collections.Counter(b for _, b in pairs)
    exp = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return 1.0 if exp == 1 else (agree - exp) / (1 - exp)


def main():
    rows = []
    for path in sorted(glob.glob(os.path.join(HERE, "codes", "*.jsonl"))):
        unit, coder = os.path.basename(path)[:-6].rsplit("_", 1)
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if "_stamp" in rec or "id" not in rec:
                continue
            for el, f in element_rows(rec):
                want = opts(first(f, "want", "wants"))
                rejects = opts(f.get("rejects"))
                mentions = f.get("mentions")
                if mentions in (None, ""):
                    sc = stated_code(f, "minority")
                    mentions = 0 if sc == 0 and not want and not rejects else 1
                mentions = int(mentions) or int(bool(want or rejects))
                pending = "S4" in want or (
                    str(f.get("needs_geometry", "0")) == "1" and not
                    [w for w in want if w in TAGS])
                level = first(f, "match_level")
                cm = derive(mentions, want, rejects, "MIN", pending)
                cj = derive(mentions, want, rejects, "MAJ", pending)
                # A coder who recorded no `rejects` field but hand-coded a
                # bare opposition (3) with no want: keep that opposition.
                inferred = 0
                if not want and not rejects:
                    if stated_code(f, "minority") == 3:
                        cm, inferred = 3, 1
                    if stated_code(f, "majority") == 3:
                        cj, inferred = 3, 1
                rows.append({
                    "unit": unit, "coder": coder, "id": rec["id"],
                    "source": rec.get("source", ""), "element": el,
                    "mentions": mentions, "want": " ".join(want),
                    "rejects": " ".join(rejects), "match_level": level,
                    "pending_geometry": int(bool(pending)),
                    "rejects_only": int((bool(rejects) or inferred) and not want),
                    "code_minority": cm,
                    "code_majority": cj,
                    "confidence": f.get("confidence", ""),
                })
    fields = list(rows[0].keys())
    with open(os.path.join(HERE, "merged_codes.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    by = collections.defaultdict(dict)
    for r in rows:
        by[(r["element"], r["id"])][r["coder"]] = r
    out, dis = {}, []
    for el in sorted({r["element"] for r in rows}):
        both = [v for (e, _), v in by.items() if e == el and len(v) == 2]
        single = sum(1 for (e, _), v in by.items() if e == el and len(v) == 1)
        res = {"pairs_double_coded": len(both), "pairs_single_coded": single}
        for which in ("minority", "majority"):
            key = "code_" + which
            pairs = [(v["A"][key], v["B"][key]) for v in both]
            res[which] = {
                "agreement": round(sum(a == b for a, b in pairs) / len(pairs), 3)
                if pairs else None,
                "kappa": None if kappa(pairs) is None else round(kappa(pairs), 3),
                "counts_A": dict(sorted(collections.Counter(
                    str(a) for a, _ in pairs).items())),
                "counts_B": dict(sorted(collections.Counter(
                    str(b) for _, b in pairs).items())),
                "both_coders_agree": dict(sorted(collections.Counter(
                    str(a) for a, b in pairs if a == b).items())),
            }
        # Stance kappa: "not mentioned" and "mentioned, no stance" merged,
        # since that line is about the keyword screen, not about a request.
        for which in ("minority", "majority"):
            key = "code_" + which
            sp = [(max(v["A"][key] or 0, 1) if v["A"][key] is not None else -1,
                   max(v["B"][key] or 0, 1) if v["B"][key] is not None else -1)
                  for v in both]
            res[which]["stance_agreement"] = round(
                sum(x == y for x, y in sp) / len(sp), 3) if sp else None
            k = kappa(sp)
            res[which]["stance_kappa"] = None if k is None else round(k, 3)
            res[which]["stance_disagreements"] = sum(x != y for x, y in sp)
        # Stance only: did both coders see support (2) or opposition (3)?
        for which in ("minority", "majority"):
            key = "code_" + which
            strict = collections.Counter()
            for v in both:
                a, b = v["A"], v["B"]
                if a[key] == b[key] and a[key] in (2, 3):
                    exact = (a["match_level"] == "exact"
                             and b["match_level"] == "exact")
                    strict[(a[key], "exact" if exact else "broad_only")] += 1
            res[which]["agreed_support_exact"] = strict[(2, "exact")]
            res[which]["agreed_support_broad"] = (strict[(2, "exact")]
                                                  + strict[(2, "broad_only")])
            res[which]["agreed_oppose_exact"] = strict[(3, "exact")]
            res[which]["agreed_oppose_broad"] = (strict[(3, "exact")]
                                                 + strict[(3, "broad_only")])
        out[el] = res
        for v in both:
            a, b = v["A"], v["B"]
            if (a["code_minority"], a["code_majority"]) != (
                    b["code_minority"], b["code_majority"]):
                dis.append({
                    "element": el, "id": a["id"], "source": a["source"],
                    "A_want": a["want"], "A_rejects": a["rejects"],
                    "A_min": a["code_minority"], "A_maj": a["code_majority"],
                    "B_want": b["want"], "B_rejects": b["rejects"],
                    "B_min": b["code_minority"], "B_maj": b["code_majority"],
                })
    json.dump(out, open(os.path.join(HERE, "agreement.json"), "w"), indent=1)
    with open(os.path.join(HERE, "disagreements.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dis[0].keys()))
        w.writeheader()
        w.writerows(dis)
    for el, res in out.items():
        m, j = res["minority"], res["majority"]
        print(f"{el:12s} n={res['pairs_double_coded']:4d} single={res['pairs_single_coded']:3d} "
              f"min k={m['kappa']} sk={m['stance_kappa']} dis={m['stance_disagreements']} sup {m['agreed_support_exact']}/{m['agreed_support_broad']} "
              f"opp {m['agreed_oppose_exact']}/{m['agreed_oppose_broad']} | "
              f"maj sk={j['stance_kappa']} dis={j['stance_disagreements']} sup {j['agreed_support_exact']}/{j['agreed_support_broad']} "
              f"opp {j['agreed_oppose_exact']}/{j['agreed_oppose_broad']}")
    print("disagreements:", len(dis), file=sys.stderr)


if __name__ == "__main__":
    main()
