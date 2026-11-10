"""Stage 1d: candidate (record, configuration) pairs for the coders.

A keyword and place-name screen over the full corpus (written submissions and
hearing testimony). It errs toward inclusion: a hit means "a coder must read
this record for this configuration", nothing more. Each configuration has
CORE terms (the places the configuration is about) and CONTEXT terms
(neighbouring places and districts whose mention often carries a relevant
request). A record is listed if any term hits; "tier" says which kind did.

Text is normalised before matching (line-break hyphens joined, whitespace
collapsed, curly quotes straightened) so OCR line wraps do not hide a name.

Output CSV columns:
  configuration, id, source (written|hearing), round, tier (core|context),
  n_hits, matched_terms, hit_pages, source_pdf, pages, affiliation_or_hearing

Usage: python3 -I 04_candidates.py CORPUS_JSONL HANSARD_JSONL OUT_CSV
"""
import csv
import json
import re
import sys

CORPUS, HANSARD, OUT = sys.argv[1:4]

SA = r"s(?:ain)?t\.?\s*albert"
CONFIGS = {
    "AIRDRIE": {
        "core": [r"airdrie"],
        "context": [r"balzac", r"cross\s?iron", r"coventry hills", r"yankee valley",
                    r"veterans b(?:oulevard|lvd)", r"rocky view"],
    },
    "COCHRANE": {
        "core": [r"cochrane", r"nolan hill"],
        "context": [r"sage hill", r"bearspaw", r"springbank", r"glenbow", r"highway 1a", r"hwy 1a"],
    },
    "CHESTERMERE": {
        "core": [r"chestermere"],
        "context": [r"calgary[- ]peigan", r"\bpeigan\b", r"\bjanet\b", r"\bshepard\b", r"langdon",
                    r"prince of peace", r"conrich", r"strathmore", r"forest lawn", r"erin woods"],
    },
    "REDDEER": {
        "core": [r"red deer"],
        "context": [r"blackfalds", r"sylvan lake", r"innisfail", r"penhold", r"\blacombe\b",
                    r"springbrook", r"delburne", r"elnora", r"bowden", r"eckville", r"bentley",
                    r"highway 2a", r"gasoline alley"],
    },
    "RMH": {
        "core": [r"rocky mountain house", r"clearwater", r"\bsundre\b", r"rimbey"],
        "context": [r"nordegg", r"\bcaroline\b", r"big\s?horn", r"eastern slopes", r"\bbanff\b",
                    r"stoney(?! trail)", r"o.?chiese", r"sunchild", r"cremona", r"david thompson",
                    r"(?:highway|hwy\.?) 22\b", r"(?:highway|hwy\.?) 11\b", r"west[- ]central"],
    },
    "OLDS": {
        "core": [r"\bolds\b", r"didsbury", r"three hills"],
        "context": [r"carstairs", r"crossfield", r"beiseker", r"irricana", r"kneehill",
                    r"(?<!calgary-)(?<!calgary )mountain view", r"trochu", r"\bacme\b", r"\blinden\b", r"torrington",
                    r"cremona", r"\bsundre\b"],
    },
    "STALBERT": {
        "core": [SA, r"sturgeon"],
        "context": [r"morinville", r"gibbons", r"bon accord", r"redwater", r"lac ste\.? anne",
                    r"town of legal", r"\blegal,? (?:and )?(?:bon accord|gibbons|morinville|redwater)",
                    r"(?:bon accord|gibbons|morinville|redwater),? (?:and )?legal\b",
                    r"alexander (?:first nation|no\.)"],
    },
    "LETHBRIDGE": {
        "core": [r"lethbridge"],
        "context": [r"coaldale", r"coalhurst", r"picture butte", r"little bow", r"fort macleod",
                    r"blood (?:tribe|reserve)", r"kainai", r"\btaber\b", r"cardston", r"nobleford",
                    r"crowsnest", r"livingstone[- ]macleod"],
    },
    "LSL": {
        "core": [r"slave lake", r"lesser slave"],
        "context": [r"high prairie", r"wabasca", r"big lakes", r"joussard", r"swan hills",
                    r"mackenzie", r"kinuso", r"\bfaust\b", r"driftpile", r"sucker creek",
                    r"northern sunrise", r"red earth", r"m\.?d\.? of opportunity", r"gift lake",
                    r"peavine", r"fort assiniboine"],
    },
    "HYBRID-GENERAL": {
        "core": [r"hybrid", r"urban[- /]+rural", r"rural[- /]+urban", r"rurban",
                 r"blended (?:riding|constituenc|district|division)",
                 r"mixed (?:riding|constituenc|district|division)"],
        "context": [r"split(?:ting|s)? (?:a|the|our|my|this) (?:city|town|community|municipality)",
                    r"divid(?:e|es|ing) (?:a|the|our|my|this) (?:city|town|community|municipality)",
                    r"(?:city|town) (?:in|into) (?:two|half|three|four)",
                    r"urban and rural", r"rural and urban"],
    },
    "CANMORE-JASPER": {
        "core": [r"canmore", r"jasper", r"\bbanff\b"],
        "context": [r"kananaskis", r"bow valley", r"west yellowhead", r"\bhinton\b", r"\bedson\b",
                    r"nanton", r"longview", r"diamond valley", r"icefields", r"national park"],
    },
}


def norm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)       # join words broken across lines
    t = re.sub(r"[ \t]*\n[ \t]*", " ", t)
    return re.sub(r"[ \t]+", " ", t)


def pages_written(text):
    """yield (page_label, page_text) from the [[page n]] markers."""
    parts = re.split(r"\[\[page (\d+)\]\]\n?", text)
    for i in range(1, len(parts), 2):
        yield parts[i], parts[i + 1]


def pages_hearing(text):
    parts = re.split(r"\[(EB-\d+)\]", text)
    yield "start", parts[0]
    for i in range(1, len(parts), 2):
        yield parts[i], parts[i + 1]


COMPILED = {c: {tier: [(p, re.compile(p, re.I)) for p in pats] for tier, pats in d.items()}
            for c, d in CONFIGS.items()}


def screen(rec, pager, source, who):
    rows = []
    pages = [(lab, norm(t)) for lab, t in pager(rec["text"])]
    for cfg, tiers in COMPILED.items():
        hits, terms, hp, tier = 0, [], [], None
        for t in ("core", "context"):
            for pat, rx in tiers[t]:
                n = 0
                for lab, txt in pages:
                    k = len(rx.findall(txt))
                    if k:
                        n += k
                        if lab not in hp:
                            hp.append(lab)
                if n:
                    hits += n
                    terms.append(f"{rx.search(' '.join(p[1] for p in pages)).group(0).lower()}×{n}")
                    tier = tier or t
        if hits:
            rows.append([cfg, rec["id"], source, rec["round"], tier, hits, "; ".join(terms),
                         " ".join(hp), rec["source_pdf"], rec["pages"], who])
    return rows


def main():
    rows = []
    for line in open(CORPUS):
        r = json.loads(line)
        rows += screen(r, pages_written, "written", r.get("affiliation", ""))
    for line in open(HANSARD):
        r = json.loads(line)
        # presenters' names are left out; the record ID leads to them
        rows += screen(r, pages_hearing, "hearing",
                       f"hearing: {r['hearing_place']}, {r['hearing_date']}")
    order = list(CONFIGS)
    rows.sort(key=lambda x: (order.index(x[0]), x[2] != "written", x[1]))
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["configuration", "id", "source", "round", "tier", "n_hits", "matched_terms",
                    "hit_pages", "source_pdf", "pages", "affiliation_or_hearing"])
        w.writerows(rows)
    # summary
    from collections import Counter
    c = Counter((r[0], r[2], r[4]) for r in rows)
    print(f"{'configuration':16} {'written core':>13} {'written ctx':>12} {'hearing core':>13} {'hearing ctx':>12}")
    for cfg in order:
        print(f"{cfg:16} {c[(cfg, 'written', 'core')]:13} {c[(cfg, 'written', 'context')]:12} "
              f"{c[(cfg, 'hearing', 'core')]:13} {c[(cfg, 'hearing', 'context')]:12}")
    print("rows", len(rows))


if __name__ == "__main__":
    main()
