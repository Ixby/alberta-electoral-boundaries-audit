"""Build a magazine-style PDF of report_public.md.

Pipeline:
1. Read the markdown.
2. Convert to HTML with the `tables` + `fenced_code` + `extra` extensions.
3. Wrap in a magazine-style HTML template with print-safe CSS.
4. Write the HTML to a temp file.
5. Call Chrome (or Edge) headless with --print-to-pdf to produce the PDF.

Run:  PYTHONIOENCODING=utf-8 python analysis/build_pdf.py
Output: report_public.pdf at the repo root.

Dependencies: markdown (pip install markdown). Chrome or Edge installed at the
standard Windows paths (verified in the script).
"""
from __future__ import annotations

import os
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


# Magazine-style CSS. Serif body, sans-serif display, tinted callout boxes for
# blockquote "sidebars", larger pull-quote style for single-line quotes,
# clean tables with alternating rows, page-break control.
CSS = r"""
@page {
  size: Letter;
  margin: 0.75in 0.75in 0.9in 0.75in;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 9pt;
    color: #666;
  }
  @top-right {
    content: "Two Maps, One Province";
    font-family: Georgia, "Times New Roman", serif;
    font-size: 8.5pt;
    color: #888;
    font-style: italic;
  }
}

html {
  font-family: Georgia, "Times New Roman", "Liberation Serif", serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: #111;
  background: #fff;
}

body {
  max-width: 100%;
  margin: 0;
  padding: 0;
}

/* Title block */
h1 {
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 34pt;
  font-weight: 800;
  letter-spacing: -0.5pt;
  line-height: 1.1;
  margin: 0 0 0.35em 0;
  color: #111;
  page-break-after: avoid;
}

/* Standfirst (italic line right after the title) */
h1 + p em,
h1 + p i {
  font-size: 14pt;
  line-height: 1.45;
  color: #444;
  font-weight: 400;
}

h1 + p {
  font-style: italic;
  font-size: 13.5pt;
  line-height: 1.45;
  color: #444;
  margin-bottom: 1em;
  font-family: Georgia, serif;
}

/* Byline paragraph */
h1 + p + p {
  font-style: normal;
  font-size: 9.5pt;
  color: #666;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.65em;
  margin-bottom: 1em;
  font-family: "Helvetica Neue", Arial, sans-serif;
  letter-spacing: 0.2pt;
  text-transform: uppercase;
  font-weight: 600;
}

/* Part headings */
h2 {
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 18pt;
  font-weight: 700;
  margin-top: 1.8em;
  margin-bottom: 0.7em;
  color: #111;
  border-bottom: 2px solid #111;
  padding-bottom: 0.25em;
  letter-spacing: -0.1pt;
  page-break-after: avoid;
  page-break-before: auto;
}

h2:first-of-type {
  page-break-before: auto;
}

/* Section headings inside parts */
h3 {
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 14pt;
  font-weight: 700;
  margin-top: 1.4em;
  margin-bottom: 0.55em;
  color: #111;
  page-break-after: avoid;
}

h4 {
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 11.5pt;
  font-weight: 700;
  margin-top: 1.1em;
  margin-bottom: 0.4em;
  color: #222;
  page-break-after: avoid;
}

/* Body paragraphs */
p {
  margin: 0 0 0.75em 0;
  text-align: justify;
  hyphens: auto;
  orphans: 3;
  widows: 3;
}

p strong:first-child {
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  font-size: 10.5pt;
  letter-spacing: 0;
}

/* Pull quotes / sidebars / bottom-line blockquotes */
blockquote {
  margin: 1em 0;
  padding: 0.9em 1.1em;
  border-left: 4px solid #111;
  background: #f7f3e9;
  font-size: 11pt;
  line-height: 1.5;
  font-style: normal;
  page-break-inside: avoid;
  border-radius: 2px;
}

blockquote p {
  margin: 0 0 0.5em 0;
  text-align: left;
}

blockquote p:last-child {
  margin-bottom: 0;
}

blockquote strong:first-child {
  color: #7a3f1a;
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 9.5pt;
  text-transform: uppercase;
  letter-spacing: 0.5pt;
  display: block;
  margin-bottom: 0.25em;
}

blockquote em {
  color: #222;
}

/* Lists */
ul, ol {
  margin: 0.6em 0 0.9em 0;
  padding-left: 1.3em;
}

ul li, ol li {
  margin-bottom: 0.3em;
  line-height: 1.5;
}

li strong:first-child {
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
}

/* Tables */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0 0.5em 0;
  font-size: 9.5pt;
  font-family: Georgia, serif;
  page-break-inside: avoid;
}

thead th {
  background: #111;
  color: #fff;
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-weight: 700;
  text-align: left;
  padding: 0.5em 0.6em;
  font-size: 9pt;
  letter-spacing: 0.2pt;
  text-transform: uppercase;
  border-bottom: 1px solid #333;
}

tbody td {
  padding: 0.45em 0.6em;
  border-bottom: 1px solid #ddd;
  vertical-align: top;
  line-height: 1.4;
}

tbody tr:nth-child(even) td {
  background: #fafafa;
}

tbody tr:last-child td {
  border-bottom: 1px solid #111;
}

tbody td strong {
  color: #111;
  font-weight: 700;
}

/* Table caption (italic paragraph after a table) */
table + p em,
table + p i {
  color: #555;
  font-style: italic;
  font-size: 9pt;
}

table + p {
  margin-top: 0;
  margin-bottom: 1.2em;
  font-size: 9pt;
  color: #555;
  text-align: left;
  font-style: italic;
}

/* Code and inline code */
code {
  font-family: "Consolas", "Courier New", monospace;
  font-size: 9pt;
  background: #f1f1f1;
  padding: 0.05em 0.3em;
  border-radius: 2px;
  color: #222;
}

/* Horizontal rule */
hr {
  border: 0;
  border-top: 1px solid #bbb;
  margin: 2em 0;
}

/* Links */
a {
  color: #0e4f7a;
  text-decoration: none;
  border-bottom: 1px dotted #0e4f7a;
}

a:visited { color: #0e4f7a; }

/* Emphasis */
em {
  font-style: italic;
}

strong em, em strong {
  font-weight: 700;
  font-style: italic;
}

/* Disclosure block right after title */
h3:first-of-type {
  font-size: 10.5pt;
  text-transform: uppercase;
  letter-spacing: 0.8pt;
  color: #777;
  margin-top: 0.8em;
  margin-bottom: 0.5em;
  border-bottom: none;
  font-weight: 600;
}

/* Print page breaks - keep Parts starting on new pages */
h2 {
  page-break-before: always;
}

h2:first-of-type {
  page-break-before: auto;
}

/* Don't page-break before first H2 (PART I) since it flows from lede */
h2#part-i-how-the-commission-came-apart {
  page-break-before: always;
}
"""

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Two Maps, One Province - Alberta Electoral Boundaries Audit</title>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def md_to_html(src_path: Path) -> str:
    text = src_path.read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=["tables", "fenced_code", "extra", "sane_lists"])
    body = md.convert(text)
    return HTML_TEMPLATE.format(css=CSS, body=body)


def run_browser_print(browser_path: str, html_path: Path, out_pdf: Path) -> None:
    # Chrome / Edge --headless --print-to-pdf takes a file URL.
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
        "--virtual-time-budget=10000",
        file_url,
    ]
    print(f"[build_pdf] Invoking: {browser_path}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
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
