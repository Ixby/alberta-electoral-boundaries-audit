"""Generate the new main page from the accepted rewrite (rewrite_tab.md):
   - home_en.ts.txt : a `home: {...}` object to paste into en.ts
   - home_body.svelte.txt : the <main> body markup that renders it
One walk over the markdown produces both, so keys and markup cannot drift."""
import json, re, sys

SRC, OUT_TS, OUT_SV = sys.argv[1:4]
md = open(SRC).read()

# Open-check markers never ship as written.
PUBLIC = {
    " [verify: passage and assent not found]": " Its passage has not been confirmed.",
    " [cite: reporting on the committee's October 28, 2026 meeting, Rocky Mountain Room, supplied by the author; video and transcript pending]":
        " (per reporting on the committee's October 28, 2026 meeting; transcript citation pending)",
}
for k, v in PUBLIC.items():
    assert k in md, k
    md = md.replace(k, v)
assert not re.search(r"\[(verify|cite|confirm)", md.split("## Alberta's Electoral Map, Audited", 1)[1])

SECTIONS = {  # ### heading -> (key prefix, element id)
    "What happened": ("happened", "what-happened"),
    "What the minority map does": ("does", "what-the-map-does"),
    "What the law requires, and what it doesn't": ("law", "what-the-law-requires"),
    "How the committee got the job": ("system", "how-it-got-here"),
    "How we know": ("know", "how-we-know"),
    "The November test": ("test", "november-test"),
    "What would change my mind": ("mind", "change-our-mind"),
    "The author's view": ("authors", "authors-view"),
    "Fixes for next time": ("fixes", "fixes-teaser"),
}
# Headings renamed in the 2026-10-29 voice pass keep their original anchor ids,
# so links shared before the rename still land.
SUB_IDS = {
    "Recommendation 5: what the government cited": "recommendation-5",
    "What I can say, and what I can't": "what-we-can-say-and-what-we-can-t",
    "Unequal district sizes": "the-cost-equal-votes",
    "The seat advantage": "what-it-buys",
    "How the neutral maps were drawn": "the-what-if-machine",
    "Checking with a second method": "did-the-result-survive-attack",
    "Limits of the simulation": "what-the-machine-can-t-see",
    "What didn't hold up": "where-the-audit-lost",
}


def inline(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", s)

    def link(m):
        text, url = m.group(1), m.group(2)
        if url.startswith("/"):
            return f'<a href="__BASE__{url}">{text}</a>'
        if url.startswith("#"):
            return f'<a href="{url}">{text}</a>'
        return f'<a href="{url}" rel="noopener">{text}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, s)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ── blocks ──────────────────────────────────────────────────────────────────
lines = md.split("\n")
blocks, i = [], 0
while i < len(lines):
    ln = lines[i]
    if not ln.strip():
        i += 1
        continue
    m = re.match(r"^(#{1,4}) (.*)$", ln)
    if m:
        blocks.append(("h", len(m.group(1)), m.group(2).strip()))
        i += 1
        continue
    if ln.startswith("- "):
        items = []
        while i < len(lines) and lines[i].startswith("- "):
            items.append(lines[i][2:].strip())
            i += 1
        blocks.append(("ul", items))
        continue
    if ln.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            if not re.match(r"^\|[\s:|-]+\|$", lines[i]):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
            i += 1
        blocks.append(("table", rows))
        continue
    para = []
    while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4} |- |\|)", lines[i]):
        para.append(lines[i].strip())
        i += 1
    blocks.append(("p", " ".join(para)))

# drop the tab title + its lead; stop before "About me" (rendered by #contact)
start = next(n for n, b in enumerate(blocks) if b[0] == "h" and b[2] == "Alberta's Electoral Map, Audited")
end = next(n for n, b in enumerate(blocks) if b[0] == "h" and b[2] == "About me")
about = blocks[end + 1:]
blocks = blocks[start:end]

strings = {}  # dotted key -> value
markup = []
counters = {}


def key(prefix, kind):
    counters[(prefix, kind)] = counters.get((prefix, kind), 0) + 1
    return f"{prefix}.{kind}{counters[(prefix, kind)]}"


def put(k, v):
    """Store a string; return the expression that renders it (internal links
    carry __BASE__, so their expression adds the base path)."""
    assert k not in strings, k
    strings[k] = v
    expr = f"t(lang.current, 'home.{k}')"
    return expr + ".replaceAll('__BASE__', base)" if "__BASE__" in v else expr


# ── hero: h1, subtitle, status, this-week strip ─────────────────────────────
hero = blocks[1:5]
assert blocks[0][2] == "Alberta's Electoral Map, Audited" and all(b[0] == "p" for b in hero[:3])
put("hero.h1", blocks[0][2])
put("hero.subtitle", inline(hero[0][1]))
put("hero.status", inline(hero[1][1]))
put("hero.week", inline(hero[2][1]))
rest = blocks[4:]

prefix, in_sub = None, False
n = 0
while n < len(rest):
    b = rest[n]
    if b[0] == "h" and b[1] == 3:  # page h2
        if prefix:
            markup.append("  </section>\n")
        prefix, sid = SECTIONS[b[2]]
        hk = put(f"{prefix}.h", b[2])
        markup.append(f'  <section id="{sid}">\n    <h2>{{{hk}}} <a href="#{sid}" class="section-link" aria-label={{{hk}}}>#</a></h2>')
        n += 1
        continue
    if b[0] == "h" and b[1] == 4:  # page h3
        if b[2] == "The results":  # hidden slot until the November scoring
            markup.append("    <!-- \"The results\" slot: filled after the November scoring (see proposals/site_rewrite_2026-10-29). -->")
            n += 1
            continue
        hid = SUB_IDS.get(b[2], slug(b[2]))
        if b[2] == "What I can say, and what I can't":
            # p "I can say:" + ul, p "I can't say:" + ul -> the existing ✓/✗ box
            (_, can_lbl), (_, can), (_, cant_lbl), (_, cant) = rest[n + 1:n + 5]
            hk = put(f"{prefix}.box_h", b[2])
            rows = []
            for it in can:
                rows.append(f'        <li class="row can"><span class="mark" aria-hidden="true">✓</span><span class="text">{{@html {put(key(prefix, "can"), inline(it))}}}</span></li>')
            for it in cant:
                rows.append(f'        <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{{@html {put(key(prefix, "cant"), inline(it))}}}</span></li>')
            markup.append(f'    <div class="boundary-block">\n      <h3 id="{hid}">{{{hk}}}</h3>\n      <ul class="boundary-list">\n' + "\n".join(rows) + "\n      </ul>\n    </div>")
            n += 5
            continue
        hk = put(key(prefix, "h3_"), b[2])
        markup.append(f'    <h3 id="{hid}">{{{hk}}}</h3>')
        n += 1
        continue
    if b[0] == "p":
        text = b[1]
        if text.startswith("*[Figure: stakes_quadrant"):
            cap = text.split("]*", 1)[1].strip()
            ck = put(f"{prefix}.fig_caption", inline(cap))
            markup.append(f'''    <figure style="margin:1.2rem 0;text-align:center;">
      <picture>
        <source type="image/webp" srcset="images/stakes_quadrant.webp">
        <img src="images/stakes_quadrant.jpg" data-full="images/stakes_quadrant.svg" alt={{t(lang.current, 'stakes.scorecard_fig_alt')}} class="chart-img" style="max-width: 100%;" width="474" height="377" loading="lazy" decoding="async">
      </picture>
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{{@html {ck}}}</figcaption>
    </figure>''')
        elif text.startswith("— Will Conner"):
            markup.append(f'    <p style="margin: 1rem 0 1.4rem;">{{{put(f"{prefix}.signed", text)}}}</p>')
        else:
            markup.append(f"    <p>{{@html {put(key(prefix, 'p'), inline(text))}}}</p>")
        n += 1
        continue
    if b[0] == "ul":
        lis = [f"      <li>{{@html {put(key(prefix, 'li'), inline(it))}}}</li>" for it in b[1]]
        cls = ' class="r5-conditions"' if any(it.startswith("**(a)") for it in b[1]) else ""
        markup.append(f"    <ul{cls}>\n" + "\n".join(lis) + "\n    </ul>")
        n += 1
        continue
    if b[0] == "table":
        tk = key(prefix, "table")
        head, body = b[1][0], b[1][1:]
        ths = "".join(f"<th scope=\"col\">{{@html {put(f'{tk}_h{j}', inline(c))}}}</th>" for j, c in enumerate(head, 1))
        trs = []
        for r, row in enumerate(body, 1):
            tds = "".join(f"<td>{{@html {put(f'{tk}_r{r}c{j}', inline(c))}}}</td>" for j, c in enumerate(row, 1))
            trs.append(f"          <tr>{tds}</tr>")
        markup.append(f'    <div class="table-wrap">\n      <table>\n        <thead><tr>{ths}</tr></thead>\n        <tbody>\n' + "\n".join(trs) + "\n        </tbody>\n      </table>\n    </div>")
        n += 1
        continue
    raise SystemExit(f"unhandled block {b}")
markup.append("  </section>\n")

# about me p1/p2 -> body.about_me values (reported, not written into `home`)
about_ps = [inline(b[1]) for b in about if b[0] == "p"]


# ── emit en.ts object ───────────────────────────────────────────────────────
def nest(d):
    root = {}
    for k, v in d.items():
        cur = root
        parts = k.split(".")
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    return root


def emit(obj, ind):
    out = []
    for k, v in obj.items():
        kk = k if re.match(r"^[A-Za-z_]\w*$", k) else json.dumps(k)
        if isinstance(v, dict):
            out.append(f"{ind}{kk}: {{\n{emit(v, ind + chr(9))}\n{ind}}},")
        else:
            out.append(f"{ind}{kk}: {json.dumps(v, ensure_ascii=False)},")
    return "\n".join(out)


open(OUT_TS, "w").write("\t// Main page, rewrite of 2026-10-29 (proposals/site_rewrite_2026-10-29).\n\t// Generated from the accepted draft together with its markup in +page.svelte.\n\thome: {\n" + emit(nest(strings), "\t\t") + "\n\t},\n")
open(OUT_SV, "w").write("\n".join(markup) + "\n")
json.dump({"about_p1": about_ps[0], "about_p2": about_ps[1], "n_strings": len(strings)}, open(OUT_TS + ".about.json", "w"), ensure_ascii=False, indent=1)
words = sum(len(re.sub(r"<[^>]+>", "", v).split()) for v in strings.values())
print(f"{len(strings)} strings, {words} words; about_me p1/p2 captured")
