"""Build a standalone HTML version of the academic technical report for web
deployment at https://willconner.ca/ab_ed/26_04_analysis.

Pipeline:
1. Read report_academic.md.
2. Convert to HTML with tables + fenced_code + extra + toc + attr_list.
3. Wrap in a reading-optimised HTML template with embedded CSS.
4. Write to dist/26_04_analysis/index.html (self-contained, no external assets).

Run:  PYTHONIOENCODING=utf-8 python analysis/scripts/build_academic_html.py
Output: dist/26_04_analysis/index.html at the repo root.

Deployment: the user uploads the `dist/26_04_analysis/` directory contents to
their web host so that `https://willconner.ca/ab_ed/26_04_analysis` (and the
`/index.html` path) serves this file.

Dependencies: markdown (pip install markdown). No browser or other tooling
needed — this produces HTML only.
"""
from __future__ import annotations

import re
from pathlib import Path

import markdown

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_MD = REPO_ROOT / "report_academic.md"
OUT_DIR = REPO_ROOT / "dist" / "26_04_analysis"
OUT_HTML = OUT_DIR / "index.html"

# Reading-optimised CSS. Serif body at comfortable line-height, responsive
# width, anchor links for internal citations, sticky table-of-contents nav
# on wider viewports, readable on mobile, print-safe.
CSS = r"""
:root {
  --serif: Georgia, "Times New Roman", "Liberation Serif", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --mono: "SF Mono", "Consolas", "Courier New", monospace;
  --ink: #1a1a1a;
  --muted: #555;
  --faint: #888;
  --rule: #d6d6d6;
  --rule-strong: #333;
  --link: #7a1f1f;
  --bg: #fdfbf7;
  --sidebar-bg: #f1eadd;
  --max-width: 760px;
}

* { box-sizing: border-box; }

html {
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.6;
  color: var(--ink);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

body {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 2.5rem 1.25rem 4rem;
}

/* --- Masthead --- */
.masthead {
  border-bottom: 2px solid var(--rule-strong);
  padding-bottom: 1.25rem;
  margin-bottom: 2rem;
}

.masthead .kicker {
  font-family: var(--sans);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--muted);
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.masthead h1 {
  font-family: var(--serif);
  font-size: 2.15rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.15;
  margin: 0 0 0.5rem 0;
  color: var(--ink);
}

.masthead .byline {
  font-family: var(--sans);
  font-size: 0.85rem;
  color: var(--muted);
  font-weight: 400;
  margin: 0;
}

.masthead .byline a { color: var(--muted); border-bottom: 1px dotted var(--muted); }

/* --- Headings --- */
h1 {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.2;
  margin: 2em 0 0.5em 0;
  color: var(--ink);
}

h2 {
  font-size: 1.45rem;
  font-weight: 700;
  line-height: 1.25;
  margin: 2.2em 0 0.7em 0;
  color: var(--ink);
  padding-top: 0.4em;
  border-top: 1px solid var(--rule);
}

h3 {
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.3;
  margin: 1.8em 0 0.5em 0;
  color: var(--ink);
}

h4 {
  font-size: 1rem;
  font-weight: 700;
  font-style: italic;
  margin: 1.5em 0 0.4em 0;
  color: var(--ink);
}

/* --- Body text --- */
p {
  margin: 0 0 1em 0;
  text-align: left;
  hyphens: auto;
}

p strong { font-weight: 700; }
em { font-style: italic; }

/* --- Links --- */
a {
  color: var(--link);
  text-decoration: none;
  border-bottom: 1px solid rgba(122, 31, 31, 0.35);
  transition: border-color 0.15s ease;
}

a:hover {
  border-bottom-color: var(--link);
}

/* --- Blockquotes --- */
blockquote {
  margin: 1.5em 0;
  padding: 0.8em 1.2em;
  border-left: 4px solid var(--rule-strong);
  background: var(--sidebar-bg);
  font-family: var(--serif);
  font-style: normal;
  font-size: 0.97rem;
  color: var(--ink);
}

blockquote p { margin: 0 0 0.5em 0; }
blockquote p:last-child { margin-bottom: 0; }
blockquote em { color: var(--ink); }

/* --- Lists --- */
ul, ol {
  margin: 0.5em 0 1.2em 0;
  padding-left: 1.5em;
}

li { margin-bottom: 0.4em; }
li > ul, li > ol { margin-top: 0.3em; margin-bottom: 0.3em; }

/* --- Code --- */
code {
  font-family: var(--mono);
  font-size: 0.88em;
  background: #eeebe4;
  padding: 0.05em 0.35em;
  border-radius: 2px;
  color: #3a2222;
}

pre {
  background: #2a2a2a;
  color: #f1f1f1;
  padding: 1em 1.1em;
  overflow-x: auto;
  border-radius: 4px;
  font-family: var(--mono);
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 1.2em 0;
}

pre code {
  background: transparent;
  color: inherit;
  padding: 0;
}

/* --- Tables --- */
.table-wrap {
  overflow-x: auto;
  margin: 1.2em -0.5em;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 0 0.5em;
  font-size: 0.9rem;
  line-height: 1.45;
}

thead th {
  background: var(--ink);
  color: #fff;
  font-family: var(--sans);
  font-weight: 600;
  text-align: left;
  padding: 0.55em 0.75em;
  font-size: 0.78rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

tbody td {
  padding: 0.55em 0.75em;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}

tbody tr:nth-child(even) td { background: #f8f4eb; }
tbody tr:last-child td { border-bottom: 2px solid var(--ink); }

tbody td strong { font-weight: 700; color: var(--ink); }

/* Table caption (italic paragraph after a table) */
.table-wrap + p em:first-child,
.table-wrap + p > em:only-child {
  display: block;
  font-size: 0.85rem;
  color: var(--muted);
  margin-top: -0.8em;
}

/* --- HR --- */
hr {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 2.5em 0;
}

/* --- TOC (if generated) --- */
.toc {
  font-family: var(--sans);
  font-size: 0.9rem;
  background: var(--sidebar-bg);
  border-left: 4px solid var(--rule-strong);
  padding: 1em 1.2em;
  margin: 2em 0;
}

.toc h3 {
  font-family: var(--sans);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
  margin: 0 0 0.5em 0;
  font-weight: 700;
}

.toc ul { margin: 0; padding-left: 1em; list-style: none; }
.toc li { margin: 0.2em 0; line-height: 1.4; }
.toc a { color: var(--ink); border-bottom: none; }
.toc a:hover { border-bottom: 1px solid var(--link); color: var(--link); }

/* --- Deployment banner + footer --- */
.deploy-banner {
  font-family: var(--sans);
  font-size: 0.8rem;
  color: var(--muted);
  padding: 0.8em 1em;
  background: var(--sidebar-bg);
  border: 1px solid var(--rule);
  border-radius: 4px;
  margin: 0 0 1.5em 0;
}

.deploy-banner strong { color: var(--ink); }

footer {
  margin-top: 4em;
  padding-top: 1.5em;
  border-top: 2px solid var(--rule-strong);
  font-family: var(--sans);
  font-size: 0.85rem;
  color: var(--muted);
  line-height: 1.5;
}

footer p { margin: 0.4em 0; }
footer a { color: var(--muted); border-bottom: 1px dotted var(--muted); }

/* --- Responsive --- */
@media (max-width: 640px) {
  html { font-size: 16px; }
  body { padding: 1.5rem 1rem 3rem; }
  .masthead h1 { font-size: 1.7rem; }
  h1 { font-size: 1.6rem; }
  h2 { font-size: 1.25rem; }
  h3 { font-size: 1.05rem; }
  table { font-size: 0.8rem; }
  thead th, tbody td { padding: 0.4em 0.5em; }
}

/* --- Print --- */
@media print {
  body { max-width: none; padding: 0.5in; }
  .deploy-banner, .toc { display: none; }
  a { color: var(--ink); border-bottom: none; }
  h1, h2, h3 { page-break-after: avoid; }
  table, blockquote, pre { page-break-inside: avoid; }
}
"""

MASTHEAD = """<div class="masthead">
  <p class="kicker">Technical Report · April 2026</p>
  <h1>Alberta Electoral Boundaries Audit</h1>
  <p class="byline">By Will Conner, Mount Royal University · Published April 22, 2026 · <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">Repository and data</a></p>
</div>
<div class="deploy-banner">
  <strong>About this document.</strong> This is the full technical report of the Alberta 2025-26 Electoral Boundaries Commission audit. A shorter magazine-style companion piece, written for a general-public readership, is published separately as <em>Two Maps, One Province</em>. The audit's claims, methodology, and reproducible pipeline are documented in full below. Every number can be re-run from the data and scripts at the linked repository.
</div>
"""

FOOTER = """<footer>
  <p><strong>Cite this document:</strong> Conner, W. (2026). <em>Alberta Electoral Boundaries Audit</em>. Mount Royal University. <a href="https://willconner.ca/ab_ed/26_04_analysis">willconner.ca/ab_ed/26_04_analysis</a></p>
  <p>Repository, data, and commit history: <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a></p>
  <p>Contact and corrections via the repository issue tracker.</p>
</footer>
"""

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Alberta Electoral Boundaries Audit — Technical Report (April 2026)</title>
<meta name="description" content="Full technical report of the Alberta 2025-26 Electoral Boundaries Commission audit. Partisan-bias metrics, signature detection, procedural audit, rationale validation, and pre-registered November checklist.">
<meta name="author" content="Will Conner">
<link rel="canonical" href="https://willconner.ca/ab_ed/26_04_analysis">
<style>
{css}
</style>
</head>
<body>
{masthead}
{body}
{footer}
</body>
</html>
"""


def wrap_tables(html: str) -> str:
    """Wrap <table>...</table> in a scroll container so wide tables don't
    overflow the body on mobile."""
    return re.sub(
        r"(<table[^>]*>.*?</table>)",
        r'<div class="table-wrap">\1</div>',
        html,
        flags=re.DOTALL,
    )


def md_to_html(src_path: Path) -> str:
    text = src_path.read_text(encoding="utf-8")
    # Strip the first H1 from the markdown (masthead supplies the title).
    text = re.sub(r"^# [^\n]*\n", "", text, count=1)
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False, "toc_depth": "2-3"}},
    )
    body = md.convert(text)
    body = wrap_tables(body)
    return HTML_TEMPLATE.format(
        css=CSS, masthead=MASTHEAD, body=body, footer=FOOTER,
    )


def main() -> int:
    if not SRC_MD.exists():
        raise FileNotFoundError(f"Source markdown not found: {SRC_MD}")
    html = md_to_html(SRC_MD)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html, encoding="utf-8")
    size_kb = OUT_HTML.stat().st_size / 1024
    print(
        f"[build_academic_html] Wrote {OUT_HTML.relative_to(REPO_ROOT)} "
        f"({size_kb:.1f} KB)."
    )
    print(
        "[build_academic_html] Deploy: upload the contents of "
        f"{OUT_DIR.relative_to(REPO_ROOT)}/ to "
        "willconner.ca/ab_ed/26_04_analysis/"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
