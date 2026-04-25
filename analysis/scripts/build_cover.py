"""Build an editorial cover page for the Two Maps, One Province feature.

Pipeline:
1. Generate the hero image: Alberta outline (silhouette, dark) with overlaid
   boundary-line art showing where majority and minority 2026 proposals
   diverge. Orange for majority, blue for minority, grey dashed for the 2019
   baseline.
2. Compose a standalone cover HTML using Playfair Display / Lora / Source
   Sans 3 typography, warm ivory background, editorial hierarchy.
3. Render cover HTML to cover.pdf via Chrome headless.
4. Merge cover.pdf + report_public.pdf into a single final PDF.

Run:  PYTHONIOENCODING=utf-8 python analysis/scripts/build_cover.py
Output: report_public.pdf at the repo root (cover + article merged).
        maps/cover_art.png as the hero image (also referenced in cover).

Dependencies: geopandas, shapely, matplotlib, markdown, pypdf, pypdfium2.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pypdf
from shapely.ops import unary_union

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ALBERTA_EDS = REPO_ROOT / "data" / "alberta_2019_eds"
APPROX_MAJ = REPO_ROOT / "data" / "v0_1_approximate_majority_2026_eds.gpkg"
# Prefer v5 (then v6 when available) for the minority polygons
APPROX_MIN_V6 = REPO_ROOT / "data" / "v0_1_refined_v6_minority_2026_eds.gpkg"
APPROX_MIN_V5 = REPO_ROOT / "data" / "v0_1_refined_v5_minority_2026_eds.gpkg"

COVER_ART_PNG = REPO_ROOT / "data" / "maps" / "cover_art.png"
OUT_PDF = REPO_ROOT / "report_public.pdf"
ARTICLE_PDF = REPO_ROOT / "report_public_article.pdf"  # temp intermediate

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
    raise FileNotFoundError("No Chrome or Edge found on this machine.")


# ==========================================================
# Cover art: Alberta silhouette with boundary-line overlay
# ==========================================================


def build_cover_art() -> Path:
    """Render the Alberta silhouette hero image.

    - Province outline only (no fill) in dark ink
    - Majority 2026 and minority 2026 boundaries rendered as confident
      coloured strokes clipped to the province interior
    - 2019 hairlines omitted (they cluttered without adding signal)
    """
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path as MplPath

    alberta = gpd.read_file(ALBERTA_EDS).to_crs(3400)

    # Province boundary: dissolve all 87 EDs into one polygon
    alberta_union = unary_union(alberta.geometry.values)
    alberta_shape = gpd.GeoDataFrame(geometry=[alberta_union], crs=3400)

    # Load the 2026 approximations (clipped to province boundary to stop
    # any sliver lines spilling outside the silhouette)
    def _clip(gdf):
        if gdf is None:
            return None
        clipped = gpd.clip(gdf, alberta_shape, keep_geom_type=False)
        return clipped

    maj = _clip(gpd.read_file(APPROX_MAJ).to_crs(3400)) if APPROX_MAJ.exists() else None
    if APPROX_MIN_V6.exists():
        minor = _clip(gpd.read_file(APPROX_MIN_V6).to_crs(3400))
    elif APPROX_MIN_V5.exists():
        minor = _clip(gpd.read_file(APPROX_MIN_V5).to_crs(3400))
    else:
        minor = None

    # Figure: generous aspect ratio that matches Alberta's own (~0.6 wide).
    # Transparent background so the cream page colour shows through.
    fig, ax = plt.subplots(figsize=(6, 9), dpi=300)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.set_aspect("equal")
    ax.axis("off")

    # Majority 2026 boundaries — warm orange, readable weight
    if maj is not None and not maj.empty:
        maj.boundary.plot(
            ax=ax,
            linewidth=0.5,
            color="#e87722",
            alpha=0.95,
            zorder=2,
        )

    # Minority 2026 boundaries — dusty blue, dashed
    if minor is not None and not minor.empty:
        minor.boundary.plot(
            ax=ax,
            linewidth=0.6,
            color="#335c81",
            alpha=0.95,
            linestyle=(0, (3.5, 2)),
            zorder=3,
        )

    # Province outline on top — clean dark stroke, no fill
    alberta_shape.boundary.plot(
        ax=ax,
        linewidth=2.2,
        color="#0e0e0e",
        zorder=5,
    )

    # Trim whitespace
    ax.margins(0.005)
    plt.tight_layout(pad=0)

    COVER_ART_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        COVER_ART_PNG,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.02,
        transparent=True,
    )
    plt.close(fig)
    print(f"[build_cover] Wrote hero art {COVER_ART_PNG.relative_to(REPO_ROOT)}")
    return COVER_ART_PNG


# ==========================================================
# Cover HTML
# ==========================================================

COVER_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The Quiet Part — cover</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Source+Sans+3:wght@400;600;700&display=swap');

@page {
  size: Letter;
  margin: 0;
}

html, body {
  margin: 0;
  padding: 0;
  width: 8.5in;
  height: 11in;
  font-family: "Lora", Georgia, serif;
  color: #1a1a1a;
}

.cover {
  position: relative;
  width: 8.5in;
  height: 11in;
  background: #f5ede0;
  overflow: hidden;
  padding: 0.75in 0.85in;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Vertical accent bar on the left */
.cover::before {
  content: "";
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 0.28in;
  background: linear-gradient(to bottom, #7a1f1f 0%, #7a1f1f 32%, #e87722 32%, #e87722 66%, #335c81 66%, #335c81 100%);
}

/* ----- Kicker ----- */
.kicker {
  font-family: "Source Sans 3", sans-serif;
  font-size: 9pt;
  font-weight: 700;
  letter-spacing: 4pt;
  text-transform: uppercase;
  color: #7a1f1f;
  margin: 0 0 0.3in 0;
  padding-top: 0.1in;
}

.kicker .issue {
  color: #1a1a1a;
  font-weight: 400;
  letter-spacing: 3pt;
}

/* ----- Hero image ----- */
.hero {
  flex: 0 1 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0.1in 0 0.25in 0;
  min-height: 0;
}

.hero img {
  max-width: 78%;
  max-height: 4.2in;
  height: auto;
  object-fit: contain;
  display: block;
}

/* ----- Title block ----- */
.title-block {
  margin: 0 0 0.15in 0;
}

.title {
  font-family: "Playfair Display", Georgia, serif;
  font-weight: 900;
  font-size: 68pt;
  letter-spacing: -1.5pt;
  line-height: 1.0;
  color: #0e0e0e;
  margin: 0 0 0.2in 0;
  padding: 0;
  white-space: nowrap;
}

.title .accent {
  color: #7a1f1f;
}

.title .tick {
  font-style: italic;
  font-weight: 700;
}

.deck {
  font-family: "Playfair Display", Georgia, serif;
  font-style: italic;
  font-weight: 400;
  font-size: 15pt;
  line-height: 1.35;
  color: #3a3a3a;
  max-width: 5.8in;
  margin: 0 0 0.25in 0;
}

/* ----- Footer: byline + locator ----- */
.footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-top: 1px solid #1a1a1a;
  padding-top: 0.18in;
  margin-top: 0.1in;
}

.byline {
  font-family: "Source Sans 3", sans-serif;
  font-size: 9pt;
  font-weight: 700;
  letter-spacing: 2pt;
  text-transform: uppercase;
  color: #1a1a1a;
}

.byline .contact {
  display: block;
  font-weight: 400;
  letter-spacing: 1pt;
  text-transform: none;
  color: #555;
  font-size: 8.5pt;
  margin-top: 0.04in;
  font-family: "Lora", Georgia, serif;
  font-style: italic;
}

.locator {
  font-family: "Source Sans 3", sans-serif;
  font-size: 8pt;
  font-weight: 600;
  letter-spacing: 1.5pt;
  text-transform: uppercase;
  color: #555;
  text-align: right;
  line-height: 1.5;
}

.locator .url {
  display: block;
  color: #7a1f1f;
  font-weight: 700;
  letter-spacing: 0.5pt;
  text-transform: none;
  font-size: 9pt;
  margin-top: 0.04in;
  font-family: "Lora", Georgia, serif;
}

/* Subtle lines at top-right = issue identifier */
.issue-marker {
  position: absolute;
  top: 0.45in;
  right: 0.85in;
  font-family: "Source Sans 3", sans-serif;
  font-size: 7.5pt;
  letter-spacing: 3pt;
  color: #888;
  text-transform: uppercase;
  text-align: right;
  font-weight: 600;
}

/* Legend strip below hero, referencing the cover-art colour language */
.legend {
  display: flex;
  gap: 0.4in;
  font-family: "Source Sans 3", sans-serif;
  font-size: 8pt;
  letter-spacing: 1.2pt;
  text-transform: uppercase;
  font-weight: 600;
  color: #555;
  margin: -0.1in 0 0.15in 0;
}

.legend .swatch {
  display: inline-block;
  width: 0.22in;
  height: 2pt;
  margin-right: 0.09in;
  vertical-align: middle;
}

.legend .swatch-maj { background: #e87722; }
.legend .swatch-min { background: #335c81; border-top: 1px dashed #335c81; }
.legend .swatch-2019 { background: #bbb; }
</style>
</head>
<body>
<div class="cover">

  <div class="issue-marker">No. 01 · April 2026</div>

  <div class="kicker">
    An Electoral Boundaries Audit<br>
    <span class="issue">Alberta · 2026</span>
  </div>

  <div class="hero">
    <img src="{hero_src}" alt="Alberta with overlaid 2026 electoral boundary proposals: 2019 baseline, majority map in orange, minority map in dashed blue.">
  </div>

  <div class="legend">
    <span><span class="swatch swatch-2019"></span>2019 baseline</span>
    <span><span class="swatch swatch-maj"></span>Majority 2026</span>
    <span><span class="swatch swatch-min"></span>Minority 2026</span>
  </div>

  <div class="title-block">
    <h1 class="title">The <span class="tick">Quiet</span> Part<span class="accent">.</span></h1>
    <p class="deck">Alberta's electoral-boundary commission split three to two. The government threw out both maps and handed the drafting pencil to five MLAs instead. An audit of what was rejected, what the government is promising, and what to watch for in November.</p>
  </div>

  <div class="footer">
    <div class="byline">
      By Will Conner
      <span class="contact">wconn161@mtroyal.ca</span>
    </div>
    <div class="locator">
      Full technical report
      <span class="url">github.com/Ixby/alberta-electoral-boundaries-audit</span>
    </div>
  </div>

</div>
</body>
</html>
"""


def build_cover_html(hero_png: Path) -> str:
    # Embed the hero via file:// URL so Chrome finds it at render time.
    # Use plain string replace to avoid str.format colliding with CSS braces.
    hero_src = hero_png.resolve().as_uri()
    return COVER_HTML.replace("{hero_src}", hero_src)


# ==========================================================
# Render cover HTML -> cover PDF (single page) via Chrome
# ==========================================================


def render_cover_pdf(cover_html_path: Path, out_pdf: Path) -> None:
    browser = find_browser()
    file_url = cover_html_path.resolve().as_uri()
    cmd = [
        browser,
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
    print(f"[build_cover] Rendering cover via {browser}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout or "")
        raise RuntimeError(f"Cover render failed ({result.returncode}).")
    print(f"[build_cover] Wrote cover PDF {out_pdf.name}")


# ==========================================================
# Merge cover.pdf + article.pdf -> final PDF
# ==========================================================


def merge_pdfs(cover_pdf: Path, article_pdf: Path, out_pdf: Path) -> None:
    writer = pypdf.PdfWriter()
    writer.append(str(cover_pdf))
    writer.append(str(article_pdf))
    with open(out_pdf, "wb") as f:
        writer.write(f)
    print(
        f"[build_cover] Merged final PDF {out_pdf.relative_to(REPO_ROOT)} "
        f"({out_pdf.stat().st_size/1024:.1f} KB)"
    )


# ==========================================================
# Orchestrator
# ==========================================================


def main() -> int:
    # 1. Hero art
    hero_png = build_cover_art()

    # 2. Cover HTML
    cover_html = build_cover_html(hero_png)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".html", delete=False
    ) as tmp:
        tmp.write(cover_html)
        cover_html_path = Path(tmp.name)

    # 3. Cover PDF
    with tempfile.NamedTemporaryFile(
        mode="wb", suffix="_cover.pdf", delete=False
    ) as tmp:
        cover_pdf_path = Path(tmp.name)
    try:
        render_cover_pdf(cover_html_path, cover_pdf_path)
    finally:
        try:
            cover_html_path.unlink()
        except OSError:
            pass

    # 4. Article PDF (regenerate via the existing article pipeline)
    print("[build_cover] Regenerating article body...")
    build_pdf_py = REPO_ROOT / "analysis" / "build_pdf.py"
    # The existing build_pdf.py writes to report_public.pdf; we temporarily
    # rename after the run so we can keep article and final distinct.
    subprocess.run(
        [sys.executable, str(build_pdf_py)],
        check=True,
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )
    # build_pdf.py wrote to OUT_PDF (report_public.pdf). Move it aside.
    if OUT_PDF.exists():
        OUT_PDF.replace(ARTICLE_PDF)

    # HIGH-07: verify the rename succeeded. On Windows, .replace() can
    # silently fail if OUT_PDF is held open by a PDF viewer. Without
    # this assert the merge step would fall through to a stale
    # ARTICLE_PDF from the previous run.
    if not ARTICLE_PDF.exists():
        raise RuntimeError(
            f"HIGH-07: build_pdf.py did not produce {ARTICLE_PDF}. "
            "Possible cause: report_public.pdf held open by another "
            "process (close any open viewers and re-run)."
        )

    # 5. Merge cover + article into final report_public.pdf
    merge_pdfs(cover_pdf_path, ARTICLE_PDF, OUT_PDF)

    # Cleanup
    try:
        cover_pdf_path.unlink()
    except OSError:
        pass
    try:
        ARTICLE_PDF.unlink()
    except OSError:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
