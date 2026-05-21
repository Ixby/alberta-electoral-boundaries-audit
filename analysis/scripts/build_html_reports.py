"""Convert markdown reports to standalone HTML pages in docs/.

Produces:
  docs/report_public.html   ← reports/public/report_public.md
  docs/report_academic.html ← reports/academic/report_academic.md

Run:
  python analysis/scripts/build_html_reports.py          # both
  python analysis/scripts/build_html_reports.py public   # public only
  python analysis/scripts/build_html_reports.py academic # academic only

Dependencies: pip install markdown
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = REPO_ROOT / "docs"

REPORTS = {
    "public": {
        "src": REPO_ROOT / "reports" / "public" / "report_public.md",
        "out": DOCS / "report_public.html",
        "subtitle": "Plain-language analysis of Alberta's 2026 electoral boundary commission",
    },
    "academic": {
        "src": REPO_ROOT / "reports" / "academic" / "report_academic.md",
        "out": DOCS / "report_academic.html",
        "subtitle": "Full technical monograph with statistical methodology and citations",
    },
}

MD_EXTENSIONS = [
    "tables",
    "fenced_code",
    "extra",
    "attr_list",
    "sane_lists",
    "md_in_html",
    TocExtension(permalink=True, toc_depth="2-3"),
]

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: Georgia, "Times New Roman", Times, serif;
  font-size: 11.5pt;
  line-height: 1.65;
  color: #111;
  background: #e8e4dc;
  padding: 1.5rem 1rem;
}

.page {
  background: #fff;
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem 3.5rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.18);
}

/* ── Header ──────────────────────────────────────────────── */
.doc-header {
  border-bottom: 2.5px solid #1a2e45;
  padding-bottom: 1rem;
  margin-bottom: 1.8rem;
}

.doc-header h1 {
  font-size: 20pt;
  font-weight: bold;
  color: #1a2e45;
  line-height: 1.25;
  margin-bottom: 0.3rem;
}

.doc-header .subtitle {
  font-size: 11pt;
  color: #444;
  font-style: italic;
  margin-bottom: 0.4rem;
}

.doc-header .meta {
  font-size: 9pt;
  color: #666;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
}

.doc-header .meta a { color: #1a5276; }

/* ── Nav TOC ─────────────────────────────────────────────── */
.toc-block {
  background: #f5f5f0;
  border: 1px solid #d8d4cc;
  border-radius: 3px;
  padding: 1rem 1.2rem 1rem 1.4rem;
  margin-bottom: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  font-size: 9.5pt;
}

.toc-block summary {
  font-weight: 600;
  font-size: 10pt;
  cursor: pointer;
  color: #1a2e45;
  margin-bottom: 0.5rem;
}

.toc-block ul { padding-left: 1.2em; }
.toc-block li { margin: 0.15rem 0; }
.toc-block a { color: #1a5276; text-decoration: none; }
.toc-block a:hover { text-decoration: underline; }

/* ── Body content ────────────────────────────────────────── */
.content h1 {
  font-size: 18pt;
  color: #1a2e45;
  margin: 2rem 0 0.6rem;
  line-height: 1.3;
}

.content h2 {
  font-size: 14pt;
  color: #1a2e45;
  border-left: 3px solid #1a2e45;
  padding-left: 0.6rem;
  margin: 2rem 0 0.6rem;
}

.content h3 {
  font-size: 12pt;
  color: #222;
  margin: 1.4rem 0 0.4rem;
}

.content h4 {
  font-size: 11pt;
  color: #333;
  margin: 1.1rem 0 0.3rem;
  font-style: italic;
}

.content p {
  margin-bottom: 0.75rem;
}

.content ul, .content ol {
  padding-left: 1.6em;
  margin-bottom: 0.8rem;
}

.content li { margin-bottom: 0.2rem; }

.content blockquote {
  border-left: 3px solid #bbb;
  padding: 0.4rem 0.8rem;
  color: #444;
  margin: 0.8rem 0;
  font-size: 10.5pt;
}

.content code {
  font-family: "Consolas", "Courier New", monospace;
  font-size: 9.5pt;
  background: #f4f2ef;
  padding: 0.1em 0.3em;
  border-radius: 2px;
}

.content pre {
  background: #f4f2ef;
  border: 1px solid #ddd;
  border-radius: 3px;
  padding: 0.7rem 0.9rem;
  overflow-x: auto;
  margin: 0.8rem 0;
}

.content pre code {
  background: none;
  padding: 0;
  font-size: 9pt;
}

.content table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9.5pt;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  margin: 0.8rem 0 1.2rem;
}

.content th {
  background: #1a2e45;
  color: #fff;
  font-weight: 600;
  padding: 0.35rem 0.5rem;
  text-align: left;
}

.content td {
  padding: 0.3rem 0.5rem;
  border: 1px solid #ddd;
  vertical-align: top;
}

.content tr:nth-child(even) td { background: #f8f7f5; }

.content img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0.6rem auto;
}

.content hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 1.5rem 0;
}

.content details {
  border: 1px solid #ddd;
  border-radius: 3px;
  padding: 0.6rem 0.9rem;
  margin: 0.8rem 0;
  background: #fafaf8;
}

.content details summary {
  cursor: pointer;
  font-weight: 600;
  color: #1a2e45;
}

/* ── Permalink anchors (from TOC extension) ─────────────── */
.headerlink {
  font-size: 0.8em;
  color: #bbb;
  text-decoration: none;
  margin-left: 0.3em;
  vertical-align: middle;
}

.headerlink:hover { color: #1a5276; }

/* ── Footer ─────────────────────────────────────────────── */
.doc-footer {
  border-top: 1px solid #ccc;
  margin-top: 2rem;
  padding-top: 0.8rem;
  font-size: 8.5pt;
  color: #666;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
}

.doc-footer a { color: #1a5276; }

/* ── Back to top ─────────────────────────────────────────── */
#back-top {
  position: fixed;
  bottom: 1.5rem;
  right: 1.2rem;
  width: 2.4rem;
  height: 2.4rem;
  background: #1a2e45;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  text-decoration: none;
  opacity: 0.65;
  transition: opacity 0.2s;
  z-index: 100;
  box-shadow: 0 2px 6px rgba(0,0,0,0.25);
}

#back-top:hover { opacity: 1; }

@media (max-width: 640px) {
  .page { padding: 1.5rem 1.2rem; }
  .content h2 { font-size: 13pt; }
  #back-top { bottom: 0.8rem; right: 0.6rem; }
}

@media print {
  body { background: #fff; padding: 0; }
  .page { box-shadow: none; max-width: 100%; padding: 1.5cm 1.8cm; }
  #back-top { display: none; }
  .content h2 { page-break-after: avoid; }
  .content table { page-break-inside: avoid; }
}
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
{css}
  </style>
</head>
<body>
<div class="page">

  <div class="doc-header">
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="meta">
      Alberta Electoral Boundary Audit &nbsp;&middot;&nbsp; May 2026 &nbsp;&middot;&nbsp;
      Official Elections Alberta shapefiles &nbsp;&middot;&nbsp;
      <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a>
    </div>
  </div>

  <details class="toc-block" open>
    <summary>Table of Contents</summary>
{toc}
  </details>

  <div class="content">
{body}
  </div>

  <div class="doc-footer">
    Alberta Electoral Boundary Audit &nbsp;&middot;&nbsp; May 2026 &nbsp;&middot;&nbsp;
    Pre-registered at OSF &nbsp;&middot;&nbsp;
    <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a>
  </div>

</div>
<a href="#" id="back-top" aria-label="Back to top">&#x2191;</a>
</body>
</html>
"""


def extract_title(md_text: str) -> str:
    for line in md_text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return "Alberta Electoral Boundary Audit"


def strip_image_directives(md_text: str) -> str:
    """Re-anchor image paths: data/maps/... → images/... (docs/ layout)."""
    return re.sub(r'!\[([^\]]*)\]\(data/maps/([^)]+)\)', r'![\1](images/\2)', md_text)


def build_report(key: str) -> None:
    cfg = REPORTS[key]
    src: Path = cfg["src"]
    out: Path = cfg["out"]
    subtitle: str = cfg["subtitle"]

    if not src.exists():
        print(f"SKIP {key}: {src} not found")
        return

    md_text = src.read_text(encoding="utf-8")
    md_text = strip_image_directives(md_text)

    title = extract_title(md_text)

    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    body_html = md.convert(md_text)
    toc_html = getattr(md, "toc", "")

    html = HTML_TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        css=CSS,
        toc=toc_html,
        body=body_html,
    )

    out.write_text(html, encoding="utf-8")
    print(f"Written: {out.relative_to(REPO_ROOT)}")


def main() -> None:
    targets = sys.argv[1:] or list(REPORTS.keys())
    unknown = [t for t in targets if t not in REPORTS]
    if unknown:
        print(f"Unknown targets: {unknown}. Choose from: {list(REPORTS.keys())}")
        sys.exit(1)
    for key in targets:
        build_report(key)


if __name__ == "__main__":
    main()
