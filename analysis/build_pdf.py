"""Build an Alberta Views-style magazine PDF of report_public.md.

Pipeline:
1. Read the markdown.
2. Convert to HTML with tables + fenced_code + extra + attr_list + sane_lists.
3. Post-process HTML to add .deck, .sidebar, .lede classes for targeted styling.
4. Wrap in a magazine-style HTML template with Playfair Display / Lora /
   Source Sans 3 typography (Google Fonts).
5. Write to a temp HTML file and print it via Chrome headless.

Run:  PYTHONIOENCODING=utf-8 python analysis/build_pdf.py
Output: report_public.pdf at the repo root.

Dependencies: markdown (pip install markdown). Chrome or Edge at the
standard Windows install paths. Network access on first run for the
Google Fonts @import (cached afterward).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_MD = REPO_ROOT / "report_public.md"
OUT_PDF = REPO_ROOT / "report_public.pdf"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_browser() -> str:
    for path in CHROME_CANDIDATES:
        if Path(path).exists():
            return path
    raise FileNotFoundError(
        "No Chrome or Edge found in the expected Windows install paths."
    )


# Alberta Views-style CSS. Playfair Display for display, Lora for body,
# Source Sans 3 for UI elements. Warm editorial palette. Drop cap on the
# lede. Tinted deck standfirst and teal-accented sidebars. Thin-ruled
# pull quotes. Ornamental section dividers. Letter page with folio and
# running head.
CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Source+Sans+3:wght@400;600;700&display=swap');

@page {
  size: Letter;
  margin: 0.9in 0.85in 1in 0.85in;
  @bottom-center {
    content: counter(page);
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 9pt;
    color: #999;
    font-weight: 400;
  }
  @top-left {
    content: "THE QUIET PART";
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 7.5pt;
    color: #b0b0b0;
    letter-spacing: 2.5pt;
    font-weight: 600;
  }
  @top-right {
    content: "AN ELECTORAL BOUNDARIES AUDIT";
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 7.5pt;
    color: #b0b0b0;
    letter-spacing: 2.5pt;
    font-weight: 600;
  }
}

@page :first {
  @top-left { content: ""; }
  @top-right { content: ""; }
  @bottom-center { content: ""; }
}

html {
  font-family: "Lora", "Georgia", "Liberation Serif", serif;
  font-size: 10.5pt;
  line-height: 1.6;
  color: #1a1a1a;
  background: #fff;
}

body { margin: 0; padding: 0; }

/* ----- Masthead (title + deck + byline) ----- */
h1 {
  font-family: "Playfair Display", Georgia, serif;
  font-size: 48pt;
  font-weight: 900;
  letter-spacing: -1.2pt;
  line-height: 0.95;
  margin: 0.2em 0 0.35em 0;
  color: #111;
  page-break-after: avoid;
}

/* Deck — italic subtitle right after h1 */
h1 + p {
  font-family: "Playfair Display", Georgia, serif;
  font-style: italic;
  font-weight: 400;
  font-size: 16pt;
  line-height: 1.35;
  color: #444;
  margin: 0.4em 0 1.1em 0;
  text-align: left;
}

/* Byline */
h1 + p + p {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 600;
  font-size: 8.5pt;
  letter-spacing: 2pt;
  text-transform: uppercase;
  color: #555;
  margin: 0 0 0 0;
  padding: 0.7em 0 0.5em 0;
  border-top: 1px solid #333;
  border-bottom: 1px solid #ccc;
  text-align: center;
}

/* Link row after byline */
h1 + p + p + p {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 400;
  font-size: 8.5pt;
  letter-spacing: 0.3pt;
  color: #666;
  text-align: center;
  margin: 0.5em 0 1.8em 0;
}

/* ----- Disclosure heading ----- */
h3 {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-size: 8pt;
  font-weight: 700;
  letter-spacing: 2.8pt;
  text-transform: uppercase;
  color: #8a2a2a;
  margin: 1.3em 0 0.5em 0;
  page-break-after: avoid;
}

/* ----- Part headings (h2) ----- */
h2 {
  font-family: "Playfair Display", Georgia, serif;
  font-size: 22pt;
  font-weight: 900;
  letter-spacing: -0.3pt;
  line-height: 1.15;
  color: #111;
  margin: 1.2em 0 0.55em 0;
  padding-top: 0.25em;
  border: none;
  border-top: 2px solid #111;
  clear: both;
  page-break-after: avoid;
  page-break-inside: avoid;
  text-align: left;
}

h2:first-of-type {
  margin-top: 1em;
  border-top: none;
  padding-top: 0;
}

/* ----- Section subheads (h3 after the disclosure) ----- */
h3:not(:first-of-type) {
  font-family: "Playfair Display", Georgia, serif;
  font-size: 15pt;
  font-weight: 700;
  font-style: italic;
  letter-spacing: 0;
  color: #222;
  text-transform: none;
  margin: 1.2em 0 0.4em 0;
  page-break-after: avoid;
}

/* ----- Body paragraphs ----- */
p {
  margin: 0 0 0.7em 0;
  text-align: justify;
  hyphens: auto;
  orphans: 3;
  widows: 3;
}

/* Drop cap on the lede paragraph */
p.lede {
  text-indent: 0;
  clear: both;
}

p.lede::first-letter {
  float: left;
  font-family: "Playfair Display", Georgia, serif;
  font-weight: 900;
  font-size: 5.8em;
  line-height: 0.85;
  padding: 0.05em 0.14em 0 0;
  color: #8a2a2a;
  margin-top: 0.02em;
}

/* ----- Bold standfirst at paragraph start ----- */
p > strong:first-child {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  font-size: 10pt;
  color: #111;
}

/* ----- Pull quote (blockquote without deck or sidebar class) ----- */
blockquote {
  margin: 1.6em 1em;
  padding: 1.1em 1.2em;
  border-left: none;
  border-top: 1px solid #333;
  border-bottom: 1px solid #333;
  background: transparent;
  font-family: "Playfair Display", Georgia, serif;
  font-style: italic;
  font-size: 14pt;
  line-height: 1.4;
  color: #333;
  text-align: center;
  page-break-inside: avoid;
}

blockquote p {
  margin: 0 0 0.4em 0;
  text-align: center;
  font-family: "Playfair Display", Georgia, serif;
  font-style: italic;
  font-size: 14pt;
}

blockquote p:last-child { margin-bottom: 0; }

blockquote p > strong:first-child {
  font-family: inherit;
  font-size: inherit;
  font-weight: 700;
  font-style: italic;
}

/* ----- Deck (bottom-line standfirst) ----- */
blockquote.deck {
  font-family: "Lora", Georgia, serif;
  font-style: normal;
  font-size: 10.5pt;
  line-height: 1.55;
  text-align: left;
  border: none;
  background: #f5e8cf;
  padding: 1.25em 1.4em;
  margin: 1.2em 0 1.5em 0;
  color: #222;
  page-break-inside: avoid;
}

blockquote.deck p {
  margin: 0;
  text-align: left;
  font-style: normal;
  font-family: "Lora", Georgia, serif;
  font-size: 10.5pt;
  line-height: 1.55;
}

blockquote.deck strong:first-child {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  font-size: 8.5pt;
  text-transform: uppercase;
  letter-spacing: 2.2pt;
  color: #8a2a2a;
  display: block;
  margin-bottom: 0.55em;
}

/* ----- Sidebar (tinted teal callout, floated right) ----- */
blockquote.sidebar {
  float: right;
  clear: right;
  width: 38%;
  background: #f0f7f7;
  border: none;
  border-left: 3px solid #2a8a8a;
  padding: 0.55em 0.7em 0.55em 0.65em;
  font-family: "Lora", Georgia, serif;
  font-style: normal;
  font-size: 8.5pt;
  line-height: 1.45;
  text-align: left;
  margin: 0.15in 0 0.2in 0.22in;
  color: #1a1a1a;
  box-sizing: border-box;
  page-break-inside: avoid;
}

blockquote.sidebar p {
  text-align: left;
  font-style: normal;
  font-family: "Lora", Georgia, serif;
  font-size: 8.5pt;
  line-height: 1.45;
  margin: 0 0 0.45em 0;
}

blockquote.sidebar p:last-child { margin-bottom: 0; }

blockquote.sidebar strong:first-child {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  font-size: 7.5pt;
  text-transform: uppercase;
  letter-spacing: 1.8pt;
  color: #1d6b6b;
  display: block;
  margin-bottom: 0.2em;
}

/* ----- Scorecard (clip-and-save tear-out card) ----- */
blockquote.scorecard {
  background: #fdf6f7;
  border-left: none;
  border-right: none;
  border-top: 2px dashed #7b2d3e;
  border-bottom: 2px dashed #7b2d3e;
  padding: 0.45em 0.6em;
  font-family: "Lora", Georgia, serif;
  font-style: normal;
  font-size: 8.5pt;
  line-height: 1.38;
  text-align: left;
  margin: 0.15in 0;
  color: #1a1a1a;
  page-break-inside: avoid;
  page-break-before: avoid;
  box-sizing: border-box;
}

blockquote.scorecard::before {
  content: "\2702  fold here";
  display: block;
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-size: 6.5pt;
  color: #7b2d3e;
  letter-spacing: 1.5pt;
  text-transform: uppercase;
  margin-bottom: 0.25em;
  opacity: 0.6;
}

blockquote.scorecard p {
  text-align: left;
  font-style: normal;
  font-family: "Lora", Georgia, serif;
  font-size: 8.5pt;
  line-height: 1.38;
  margin: 0 0 0.3em 0;
}

blockquote.scorecard p:last-child { margin-bottom: 0; }

blockquote.scorecard strong:first-child {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 2pt;
  color: #5c1f2d;
  display: block;
  margin-bottom: 0.3em;
}

blockquote.scorecard em {
  font-size: 8pt;
  color: #444;
}

blockquote.scorecard table {
  width: 100%;
  border-collapse: collapse;
  font-size: 8pt;
  margin: 0.3em 0;
}

blockquote.scorecard table thead th {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  font-size: 6.5pt;
  text-transform: uppercase;
  letter-spacing: 1pt;
  color: #5c1f2d;
  padding: 0.18em 0.4em 0.18em 0;
  text-align: left;
  line-height: 1.2;
  border-bottom: 1px solid #c9a0a8;
}

blockquote.scorecard table thead th:last-child,
blockquote.scorecard table tbody td:last-child {
  text-align: center;
  width: 5em;
}

blockquote.scorecard table tbody td {
  padding: 0.14em 0.4em 0.14em 0;
  border-bottom: 1px solid #e8d5d8;
  vertical-align: top;
  line-height: 1.35;
}

blockquote.scorecard table tbody tr:last-child td {
  border-bottom: none;
}

blockquote.scorecard table tbody td:last-child {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  font-size: 7.5pt;
  color: #7b2d3e;
}

/* ----- Tables ----- */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.2em 0 0.4em 0;
  font-family: "Lora", Georgia, serif;
  font-size: 9.5pt;
  page-break-inside: avoid;
}

thead th {
  background: transparent;
  color: #111;
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  text-align: left;
  padding: 0.6em 0.7em 0.4em;
  font-size: 8pt;
  letter-spacing: 1.5pt;
  text-transform: uppercase;
  border-bottom: 2px solid #111;
}

tbody td {
  padding: 0.55em 0.7em;
  border-bottom: 1px solid #d8d8d8;
  vertical-align: top;
  line-height: 1.45;
}

tbody tr:last-child td { border-bottom: 2px solid #111; }

tbody td strong { color: #111; font-weight: 700; }

/* Table caption (italic paragraph right after a table) */
table + p {
  color: #666;
  font-style: italic;
  font-size: 8.5pt;
  font-family: "Lora", Georgia, serif;
  text-align: left;
  margin: 0.2em 0 1.4em 0;
  letter-spacing: 0.2pt;
}

/* ----- Horizontal rule as ornamental three-dot divider ----- */
hr {
  border: 0;
  border-top: 1px solid #ddd;
  margin: 1em 0;
  height: 0;
  clear: both;
  page-break-after: avoid;
}

/* ----- Links ----- */
a {
  color: #7a1f1f;
  text-decoration: none;
  border-bottom: 1px solid rgba(122, 31, 31, 0.35);
}

/* ----- Emphasis ----- */
em { font-style: italic; }
strong { font-weight: 700; }

/* ----- Lists ----- */
ul, ol {
  margin: 0.6em 0 1.1em 0;
  padding-left: 1.4em;
}

ul li, ol li {
  margin-bottom: 0.4em;
  line-height: 1.55;
}

li strong:first-child {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
}

/* ----- Figures (images with captions) ----- */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1.2em auto 0.3em;
  page-break-inside: avoid;
}

/* ----- Author bio at end ----- */
.author-bio, p.author-bio {
  margin-top: 3em;
  padding: 1.5em 0 1em 0;
  border-top: 2px solid #333;
  border-bottom: 1px solid #ccc;
  font-family: "Lora", Georgia, serif;
  font-size: 9.5pt;
  font-style: italic;
  line-height: 1.5;
  color: #555;
  text-align: left;
}

.author-bio em, p.author-bio em { font-style: italic; }
"""

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The Quiet Part — An Alberta Electoral Boundaries Audit</title>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def post_process_html(html: str) -> str:
    """Tag the HTML with classes the CSS targets.

    1. First <blockquote> becomes the deck (bottom-line standfirst).
    2. Blockquotes whose first <strong> starts with "SIDEBAR" become
       sidebars (teal callout boxes).
    3. First <p> after the first <h2> becomes the lede (drop cap target).
    """
    # 1. First blockquote → deck
    html = re.sub(r"<blockquote>", '<blockquote class="deck">', html, count=1)

    # 2. Any remaining <blockquote> whose first strong text begins with SIDEBAR → sidebar.
    #    Pattern: <blockquote>\s*<p><strong>SIDEBAR  (case-insensitive)
    html = re.sub(
        r"<blockquote>(\s*<p><strong>SIDEBAR)",
        r'<blockquote class="sidebar">\1',
        html,
        flags=re.IGNORECASE,
    )

    # 2b. Blockquotes whose first strong begins with SCORECARD → scorecard.
    html = re.sub(
        r"<blockquote>(\s*<p><strong>SCORECARD)",
        r'<blockquote class="scorecard">\1',
        html,
        flags=re.IGNORECASE,
    )

    # 3. First <p> after the first <hr> → lede (drop cap). This is the
    #    first intro paragraph below the masthead block (title + deck +
    #    byline + links + hr).
    html = re.sub(
        r"(<hr\s*/?>\s*)<p>",
        r'\1<p class="lede">',
        html,
        count=1,
    )

    return html


def md_to_html(src_path: Path) -> str:
    text = src_path.read_text(encoding="utf-8")
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "extra", "sane_lists", "attr_list"]
    )
    body = md.convert(text)
    body = post_process_html(body)
    return HTML_TEMPLATE.format(css=CSS, body=body)


def run_browser_print(browser_path: str, html_path: Path, out_pdf: Path) -> None:
    file_url = html_path.resolve().as_uri()
    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf.resolve()}",
        "--print-to-pdf-no-header",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=15000",
        file_url,
    ]
    print(f"[build_pdf] Invoking: {browser_path}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout or "")
        raise RuntimeError(
            f"Browser print failed with exit code {result.returncode}."
        )


def main() -> int:
    if not SRC_MD.exists():
        raise FileNotFoundError(f"Source markdown not found: {SRC_MD}")
    browser = find_browser()
    html = md_to_html(SRC_MD)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".html", delete=False
    ) as tmp:
        tmp.write(html)
        tmp_path = Path(tmp.name)
    try:
        run_browser_print(browser, tmp_path, OUT_PDF)
        size_kb = OUT_PDF.stat().st_size / 1024
        print(
            f"[build_pdf] Wrote {OUT_PDF.name} "
            f"({size_kb:.1f} KB) at {OUT_PDF.resolve()}"
        )
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
