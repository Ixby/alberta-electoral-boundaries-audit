"""Build an Alberta Views-style magazine PDF of report_public.md.

Pipeline:
1. Read the markdown.
2. Convert to HTML with tables + fenced_code + extra + attr_list + sane_lists.
3. Post-process HTML to add .deck, .sidebar, .lede classes for targeted styling.
4. Wrap in a magazine-style HTML template with Playfair Display / Lora /
   Source Sans 3 typography (Google Fonts).
5. Write to a temp HTML file and print it via Chrome headless.

Run:  PYTHONIOENCODING=utf-8 python analysis/scripts/build_pdf.py
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

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_MD = REPO_ROOT / "report_public.md"
import tempfile as _tempfile

# Write the intermediate article PDF + HTML to .temp/ rather than the
# repo root; only the merged report_public.pdf is the published artefact.
_TMP_DIR = REPO_ROOT / ".temp"
_TMP_DIR.mkdir(exist_ok=True)
OUT_PDF = _TMP_DIR / "article.pdf"
OUT_HTML = _TMP_DIR / "article.html"

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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,opsz,wght@0,5..1200,400..900;1,5..1200,400..900&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,400..700&display=swap');

@page {
  size: Letter;
  margin: 0.65in 0.85in 0.75in 0.85in;
  @bottom-center {
    content: counter(page);
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 9pt;
    color: #666;
    font-weight: 400;
  }
  @top-left {
    content: "THE QUIET PART";
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 7.5pt;
    color: #7a7a7a;
    letter-spacing: 2pt;
    font-weight: 600;
  }
  @top-right {
    content: string(chapter);
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 7.5pt;
    color: #7a7a7a;
    letter-spacing: 2pt;
    font-weight: 600;
    text-transform: uppercase;
  }
}

@page :first {
  @top-left { content: ""; }
  @top-right { content: ""; }
  @bottom-center { content: ""; }
}

html {
  font-family: "Lora", "Georgia", "Liberation Serif", serif;
  font-size: 10pt;
  line-height: 1.5;
  letter-spacing: 0.01em;
  color: #1a1a1a;
  background: #fff;
  font-feature-settings: "kern" 1, "liga" 1, "onum" 1, "pnum" 1;
  font-variant-numeric: oldstyle-nums proportional-nums;
  font-optical-sizing: auto;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
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
  font-size: 20pt;
  font-weight: 900;
  letter-spacing: -0.3pt;
  line-height: 1.15;
  color: #111;
  margin: 1.4em 0 0.55em 0;
  padding-top: 0.6em;
  border: none;
  border-top: 0.5pt solid #111;
  clear: both !important;       /* force float context to close above the rule */
  page-break-after: avoid;
  page-break-inside: avoid;
  text-align: left;
  text-wrap: balance;
  string-set: chapter content();
}

/* Float-killer: anything above the h2's top rule must close above it.
   Without this, the previous section's right-floated sidebar can extend
   below the rule and visually collide with the new section's title. */
h2::before {
  content: "";
  display: block;
  clear: both;
  height: 0;
}

h2:first-of-type {
  margin-top: 0.6em;
  border-top: none;
  padding-top: 0;
}

h2:first-of-type::before {
  content: none;
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
  margin: 0.85em 0 0.3em 0;
  page-break-after: avoid;
}

/* ----- Body paragraphs ----- */
p {
  margin: 0 0 0.55em 0;
  text-align: justify;
  hyphens: auto;
  -webkit-hyphens: auto;
  hyphenate-limit-chars: 6 3 2;
  hyphenate-limit-lines: 2;
  orphans: 2;
  widows: 2;
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
  line-height: 0.78;
  padding: 0 0.14em 0 0;
  color: #8a2a2a;
  margin-top: -0.08em;
  padding-top: 0.02em;
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
  border-top: 0.5pt solid #888;
  border-bottom: 0.5pt solid #888;
  background: transparent;
  font-family: "Playfair Display", Georgia, serif;
  font-style: italic;
  font-size: 13pt;
  line-height: 1.4;
  color: #333;
  text-align: center;
  /* page-break-inside intentionally not set — let pull quotes break if they need to */
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
  font-size: 10pt;
  line-height: 1.5;
  text-align: left;
  border: none;
  background: #f5e8cf;
  padding: 0.9em 1.1em;
  margin: 0.8em 0 1em 0;
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
  width: 30%;
  /* No max-height + overflow:hidden — we will not silently amputate copy.
     If a sidebar is too tall to flow inside its section, the layout below
     handles it via page-break-inside:avoid. */
  background: #f0f7f7;
  border: none;
  border-left: 3px solid #2a8a8a;
  padding: 0.55em 0.7em 0.55em 0.65em;
  font-family: "Lora", Georgia, serif;
  font-style: normal;
  font-size: 8pt;
  line-height: 1.4;
  text-align: left;
  margin: 0.1in 0 0.15in 0.2in;
  color: #1a1a1a;
  box-sizing: border-box;
  page-break-inside: avoid;
  contain: layout;
}

/* Sidebar after an h2: keep the float so following body text wraps
   around it instead of leaving a column of whitespace beside it.
   The h2's own clear:both already prevents it from collapsing into a
   previous section's float. */

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

/* ----- Scorecard (compact tinted callout) ----- */
blockquote.scorecard {
  background: #fdf6f7;
  border: none;
  border-left: 3pt solid #7b2d3e;
  padding: 0.4em 0.7em 0.4em 0.85em;
  font-family: "Lora", Georgia, serif;
  font-style: normal;
  font-size: 8.5pt;
  line-height: 1.35;
  text-align: left;
  margin: 0.1in 0;
  color: #1a1a1a;
  page-break-inside: avoid;
  box-sizing: border-box;
}

/* No "fold here" ornament — it was reading as ugly on the printed page */
blockquote.scorecard::before {
  content: none;
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
  margin: 0.7em 0 0.3em 0;
  font-family: "Lora", Georgia, serif;
  font-size: 9.5pt;
  font-variant-numeric: tabular-nums lining-nums;
  clear: both;                /* never overlap a floated sidebar */
}

/* Tables can break across pages but rows should not split, and the
   header should repeat on the new page. */
thead { display: table-header-group; }
tbody tr { page-break-inside: avoid; break-inside: avoid; }

thead th {
  background: transparent;
  color: #111;
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 600;
  text-align: left;
  padding: 0.6em 0.7em 0.4em;
  font-size: 8pt;
  letter-spacing: 0.8pt;
  text-transform: uppercase;
  border-bottom: 0.5pt solid #111;
}

tbody td {
  padding: 0.4em 0.7em;
  border-bottom: 1px solid #d8d8d8;
  vertical-align: top;
  line-height: 1.4;
}

tbody tr:last-child td { border-bottom: 0.5pt solid #111; }

tbody td strong { color: #7b2d3e; font-weight: 600; }

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

/* ----- Horizontal rule (markdown ---) ----- */
hr {
  border: 0;
  border-top: 0.5pt solid #ccc;
  margin: 1.4em 0 0 0;
  height: 0;
  clear: both;
  page-break-after: avoid;
}

/* When an hr precedes an h2, the h2's own top rule is redundant.
   Suppress the h2 rule so we don't get two stacked lines. */
hr + h2 {
  border-top: none;
  padding-top: 0;
  margin-top: 0.5em;
}

/* When an hr is the very first thing after an h1 deck (the title block
   ends with hr / lede), give the deck more breathing room. */
hr + p.lede {
  margin-top: 1.0em;
}

/* ----- Links -----
   Underline: 0.8pt solid #1a1a1a (the body-text colour) so the link
   marker survives a grayscale render on e-ink readers (Kindle, Kobo,
   reMarkable). Pre-2026-04-27 the underline was 0.5pt #b56a6a (a faint
   pink) which collapses to a near-invisible gray on monochrome devices;
   the link colour #7a1f1f also collapses to mid-gray on grayscale, so
   underline carries the link signal on e-ink while colour carries it on
   print/screen. */
a {
  color: #7a1f1f;
  text-decoration: none;
  border-bottom: 0.8pt solid #1a1a1a;
  text-underline-offset: 2pt;
}

/* ----- Verdict callout (h3 wrapped via post-processor) ----- */
h3.verdict {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-size: 8.5pt;
  font-weight: 700;
  letter-spacing: 3pt;
  text-transform: uppercase;
  color: #5c1f2d;
  border-top: 3px double #5c1f2d;
  padding-top: 0.7em;
  margin-top: 1.6em;
  margin-bottom: 0.3em;
  page-break-after: avoid;
  break-after: avoid;
}

h3.verdict + p {
  font-family: "Playfair Display", Georgia, serif;
  font-size: 16pt;
  font-style: italic;
  font-weight: 400;
  line-height: 1.28;
  color: #1a1a1a;
  margin: 0.3em 0 0.9em 0;
  text-align: left;
  page-break-before: avoid;
  break-before: avoid;
}

h3.verdict + p strong {
  font-style: italic;
  font-weight: 700;
  color: #5c1f2d;
}

/* ----- Author opinion blockquote (post-processor tags) ----- */
blockquote.opinion {
  border-top: none;
  border-bottom: none;
  border-left: 3pt solid #8a2a2a;
  background: #faf6f0;
  padding: 1em 1.3em;
  font-style: normal;
  font-family: "Lora", Georgia, serif;
  font-size: 10pt;
  line-height: 1.55;
  text-align: left;
  margin: 1em 0 1.4em 0;
  page-break-inside: avoid;
  break-inside: avoid;
}

blockquote.opinion p {
  text-align: left;
  font-style: normal;
  font-family: "Lora", Georgia, serif;
  font-size: 10pt;
  line-height: 1.55;
}

blockquote.opinion strong:first-child {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 2.2pt;
  color: #8a2a2a;
  display: block;
  margin-bottom: 0.55em;
  font-style: normal;
}

/* ============================================================
   COLLISION-PREVENTION RULES (layout-artist review, 2026-04-25)
   ============================================================ */

/* Section integrity: keep headings with at least 2 lines of following
   body. Page breaks should land between paragraphs, not orphan a
   subsection title at the bottom of a page. */
h2, h3, h3.verdict {
  page-break-after: avoid;
  break-after: avoid;
}
h2 + p, h3 + p, h3.verdict + p {
  page-break-before: avoid;
  break-before: avoid;
  orphans: 3;
  widows: 3;
}
h2 + blockquote, h3 + blockquote {
  page-break-before: avoid;
  break-before: avoid;
}

/* Opinion blocks always start fresh — never wrap around a float */
blockquote.opinion {
  clear: both;
}

/* Drop-cap clearance below deck box — was colliding when deck wraps tall */
blockquote.deck + p.lede {
  margin-top: 1.0em;
  clear: both;
}
p.lede::first-letter {
  shape-outside: margin-box;
}

/* Heading collision: h2 + h3 / h2 + verdict-h3 — collapse the second
   heading's top decoration when it follows another heading directly */
h2 + h3 {
  margin-top: 0.5em;
}
h2 + h3.verdict {
  margin-top: 0.6em;
  padding-top: 0;
  border-top: none;
}

/* Verdict-callout breathing room from the previous paragraph's last line */
p + h3.verdict {
  margin-top: 2em;
}
h3.verdict + p + h3.verdict {
  margin-top: 1.8em;
  padding-top: 0.7em;
  border-top: 1px solid #ddd;   /* lighter rule when verdicts stack */
}

/* Scorecards must not stack — visually crowds the tear-out metaphor */
blockquote.scorecard + blockquote.scorecard {
  margin-top: 1.4em;
  page-break-before: always;
  break-before: page;
}

/* Section openers that should always start fresh on a new page */
h2.new-page, h3.new-page {
  page-break-before: always;
  break-before: page;
}

/* Inline-floating figure: behaves like a sidebar (right-floated, content
   wraps around it) instead of taking the full text column. Used for
   secondary inline figures. */
img.inline-float {
  float: right;
  clear: right;
  width: 50%;
  max-width: 4in;
  max-height: 4in;
  margin: 0.05in 0 0.15in 0.25in;
  page-break-inside: avoid;
  break-inside: avoid;
}

/* Hero figure for the verdict quadrant — the article's primary
   rhetorical visual. Full-width, takes roughly 1/3 to 1/2 of the
   page so it commands attention. */
img.verdict-hero {
  display: block;
  width: 95%;
  max-width: 6.5in;
  max-height: 5.4in;            /* ~1/2 page on a Letter sheet */
  margin: 0.25in auto 0.2in auto;
  page-break-inside: avoid;
  break-inside: avoid;
  clear: both;
}
/* Defeat the global figure max-height cap for the verdict-hero figure */
img.verdict-hero { max-height: 5.4in !important; }

/* Override the global tbody:last-child border on tables INSIDE scorecards
   (the heavy black bar fights the dashed maroon border) */
blockquote.scorecard tbody tr:last-child td {
  border-bottom: none;
}


/* ----- Emphasis ----- */
em { font-style: italic; }
strong { font-weight: 700; }

/* ----- Lists ----- */
ul, ol {
  margin: 0.4em 0 0.8em 0;
  padding-left: 1.4em;
}

ul li, ol li {
  margin-bottom: 0.25em;
  line-height: 1.5;
}

li strong:first-child {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
}

/* ----- Figures (images with captions) ----- */
img {
  max-width: 100%;
  max-height: 3.4in;          /* keep figures from forcing big orphan-whitespace pushes */
  height: auto;
  display: block;
  margin: 1.0em auto 0.4em;
  page-break-inside: avoid;
  break-inside: avoid;
  clear: both;
}

/* Captions: markdown image alt text doesn't render; use a following <em>
   for caption text. Style follows Lora italic, smaller, grey. */
img + em, p > img + em, p:has(img) + p > em {
  display: block;
  font-family: "Lora", Georgia, serif;
  font-style: italic;
  font-size: 8pt;
  line-height: 1.35;
  color: #666;
  text-align: left;
  margin: 0.3em 0 1.2em 0;
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
<base href="{base_href}">
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

    # 2. Tag callouts by the all-caps title in the first <strong> tag.
    # Editorial convention: a blockquote whose first <strong> is an
    # all-caps title is a callout. Whether it renders as a floated sidebar
    # or as a full-width scorecard is determined by title membership.
    SCORECARD_TITLES = {
        "ONE WAY TO READ THE TWO MAPS",
        "RETRACTION CONDITIONS",
    }
    callout_title_re = re.compile(
        r"<blockquote(?:\s+class=\"[^\"]*\")?>\s*<p>\s*<strong>"
        r"([A-Z][A-Z0-9 \-—'&/]{2,})"
        r"</strong>"
    )

    def _tag_callout(m: re.Match) -> str:
        body = m.group(0)
        if 'class="' in body[:30]:
            return body
        title_match = callout_title_re.match(body)
        if not title_match:
            return body
        title = title_match.group(1).strip().rstrip("—").strip()
        cls = "scorecard" if title in SCORECARD_TITLES else "sidebar"
        return body.replace("<blockquote>", f'<blockquote class="{cls}">', 1)

    html = re.sub(
        r"<blockquote(?:\s+class=\"[^\"]*\")?>[\s\S]*?</blockquote>",
        _tag_callout,
        html,
    )

    # 2c. Blockquotes containing <strong>OPINION or "THE PLAIN READING" anywhere → opinion.
    def _tag_opinion(m: re.Match) -> str:
        body = m.group(0)
        if 'class="' in body[:30]:
            return body
        if re.search(r"<strong>(OPINION|THE PLAIN READING)", body, flags=re.IGNORECASE):
            return body.replace("<blockquote>", '<blockquote class="opinion">', 1)
        return body

    html = re.sub(
        r"<blockquote(?:\s+class=\"[^\"]*\")?>[\s\S]*?</blockquote>",
        _tag_opinion,
        html,
    )

    # 2d. <h3>Verdict on …</h3> → verdict callout.
    html = re.sub(
        r"<h3>(Verdict on [^<]+)</h3>",
        r'<h3 class="verdict">\1</h3>',
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
    base_href = src_path.resolve().parent.as_uri() + "/"
    return HTML_TEMPLATE.format(css=CSS, body=body, base_href=base_href)


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
        raise RuntimeError(f"Browser print failed with exit code {result.returncode}.")


def main() -> int:
    if not SRC_MD.exists():
        raise FileNotFoundError(f"Source markdown not found: {SRC_MD}")
    browser = find_browser()
    html = md_to_html(SRC_MD)
    OUT_HTML.write_text(html, encoding="utf-8")
    html_kb = OUT_HTML.stat().st_size / 1024
    print(
        f"[build_pdf] Wrote {OUT_HTML.name} "
        f"({html_kb:.1f} KB) at {OUT_HTML.resolve()}"
    )
    run_browser_print(browser, OUT_HTML, OUT_PDF)
    pdf_kb = OUT_PDF.stat().st_size / 1024
    print(
        f"[build_pdf] Wrote {OUT_PDF.name} " f"({pdf_kb:.1f} KB) at {OUT_PDF.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
