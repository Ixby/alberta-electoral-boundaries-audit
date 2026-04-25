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
ALBERTA_EDS = REPO_ROOT / "data" / "shapefiles" / "reference" / "alberta_2019_eds"
DERIVED = REPO_ROOT / "data" / "shapefiles" / "derived"
# Prefer v0_8 refined → v0_8 canonical → v0_7 canonical for the boundary art
APPROX_MAJ_CANDIDATES = [
    DERIVED / "v0_8_refined_majority_2026_eds.gpkg",
    DERIVED / "v0_8_canonical_majority_2026_eds.gpkg",
    DERIVED / "v0_7_canonical_majority_2026_eds.gpkg",
]
APPROX_MIN_CANDIDATES = [
    DERIVED / "v0_8_refined_minority_2026_eds.gpkg",
    DERIVED / "v0_8_canonical_minority_2026_eds.gpkg",
    DERIVED / "v0_7_canonical_minority_2026_eds.gpkg",
]

COVER_ART_PNG = REPO_ROOT / "data" / "maps" / "cover_art.png"
OUT_PDF = REPO_ROOT / "report_public.pdf"   # final = cover + article
ARTICLE_PDF = REPO_ROOT / "article.pdf"     # already produced by build_pdf.py

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


VA_VOTES_PATH = REPO_ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"


def _pick(candidates):
    for p in candidates:
        if p.exists():
            return p
    return None


def build_cover_art() -> Path:
    """Cover hero: v0_8 EDs erupting outward from Edmonton, colour-coded
    by 2023 two-party vote share.

    Motion:
    - Edmonton is the eruption epicentre. Each ED is displaced radially
      outward from Edmonton by a NON-LINEAR factor — far EDs blow much
      further than near ones, producing the "eruption" feel rather than
      a uniform exploded-diagram pull-apart.
    - Each ED leaves three motion-trail ghost copies trailing back
      toward Edmonton at decreasing opacity, conveying the sense the
      pieces are mid-flight.
    - Edmonton's own ED stays in place (or moves only minimally) to
      visually anchor the epicentre.

    Colour:
    - Divergent NDP-orange ↔ white ↔ UCP-blue, centred on 50/50.
      Canadian convention: UCP/Conservative blue, NDP orange.
    - VA centroids spatially joined into v0_8 EDs for per-ED 2023
      totals. EDs catching zero VAs (inherited-empty from v0_7) get
      neutral grey fill.
    """
    import math
    import shapely.affinity
    import matplotlib.colors as mcolors

    # Edmonton city-centre coordinates in EPSG:3401 (NAD83 / AB 10-TM Forest).
    # These match the landmark anchors used in the alignment proof.
    EDMONTON = (97000.0, 5933000.0)

    # Eruption strength parameters — tuned so Alberta remains visually
    # recognisable. The faint dotted backdrop outline of the original
    # (un-exploded) province carries the shape; the displaced pieces
    # carry the motion.
    BASE_PUSH_FRAC = 0.025       # tiny baseline push (every ED nudges)
    POWER_PUSH_COEF = 0.09       # max displacement ≈ 9% of radius for the farthest ED
    POWER = 1.3                  # exponent: <1 = uniform, 1 = linear, >1 = explosive
    GHOST_STEPS = 3              # number of motion-trail ghost copies per ED
    GHOST_ALPHA_BASE = 0.16      # opacity of the brightest motion ghost

    # 1. Pick map (prefer v0_8 refined → canonical → v0_7)
    maj_path = _pick(APPROX_MAJ_CANDIDATES)
    if maj_path is None:
        raise FileNotFoundError("No majority GPKG candidate available")
    print(f"[build_cover] Hero ED source: {maj_path.name}")

    eds = gpd.read_file(maj_path).to_crs(3401)
    name_col = "name_2026" if "name_2026" in eds.columns else eds.columns[0]
    eds = eds[eds.geometry.area > 1e6].copy().reset_index(drop=True)
    print(f"[build_cover] {len(eds)} non-empty EDs to render")

    # 2. Per-ED 2023 vote share via VA-centroid spatial join
    if VA_VOTES_PATH.exists():
        va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
        va_pts = gpd.GeoDataFrame(
            {"va_ucp": va["va_ucp"].fillna(0),
             "va_ndp": va["va_ndp"].fillna(0)},
            geometry=va.geometry.centroid,
            crs=3401,
        )
        joined = gpd.sjoin(
            va_pts, eds[[name_col, "geometry"]],
            how="left", predicate="within",
        )
        agg = joined.groupby(name_col).agg(
            ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum")
        ).reset_index()
        agg["total"] = (agg["ucp"] + agg["ndp"]).clip(lower=1)
        agg["ucp_share"] = agg["ucp"] / agg["total"]
        eds = eds.merge(agg[[name_col, "ucp_share", "total"]],
                        on=name_col, how="left")
    else:
        print(f"[build_cover] WARN: {VA_VOTES_PATH.name} not found; "
              f"all EDs will render as neutral 50/50")
        eds["ucp_share"] = 0.5
        eds["total"] = 0
    eds["ucp_share"] = eds["ucp_share"].fillna(0.5)
    eds["total"] = eds["total"].fillna(0)
    print(f"[build_cover] {int((eds['total'] > 0).sum())}/{len(eds)} EDs received VA votes")

    # 3. Province silhouette (faint backdrop) — dissolve all renderable EDs in
    #    their ORIGINAL positions before exploding
    province_orig = unary_union(eds.geometry.values)

    # 4. Compute per-ED radial displacement vector from Edmonton.
    #    Distance is measured ED-centroid to Edmonton; final translation
    #    distance scales as: radius * (BASE + POWER_COEF * (radius/R_max)^POWER)
    centroids = [(g.centroid.x, g.centroid.y) for g in eds.geometry]
    radii = [math.hypot(cx - EDMONTON[0], cy - EDMONTON[1]) for cx, cy in centroids]
    R_max = max(radii) if radii else 1.0

    def _displacement(cx, cy, r):
        if r < 1.0:  # avoid div-by-zero for an ED whose centroid IS Edmonton
            return (0.0, 0.0)
        ux, uy = (cx - EDMONTON[0]) / r, (cy - EDMONTON[1]) / r  # unit vector
        push_distance = r * (BASE_PUSH_FRAC + POWER_PUSH_COEF * (r / R_max) ** POWER)
        return (ux * push_distance, uy * push_distance)

    eds["disp"] = [_displacement(cx, cy, r) for (cx, cy), r in zip(centroids, radii)]
    eds["exploded"] = [
        shapely.affinity.translate(g, dx, dy)
        for g, (dx, dy) in zip(eds.geometry, eds["disp"])
    ]

    # 5. Divergent colormap NDP-orange ↔ white ↔ UCP-blue
    ndp_orange = (0.92, 0.45, 0.10)
    ucp_blue   = (0.13, 0.36, 0.62)
    white      = (0.97, 0.96, 0.94)
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "ucp_ndp_div", [ndp_orange, white, ucp_blue], N=256
    )
    norm = mcolors.Normalize(vmin=0.30, vmax=0.70)

    # 6. Render
    fig, ax = plt.subplots(figsize=(6, 9), dpi=300)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.set_aspect("equal")
    ax.axis("off")

    # Province silhouette in the original (pre-eruption) position — kept
    # confident enough to read as Alberta at a glance. The eruption
    # happens INSIDE this anchor outline so the shape stays recognisable.
    gpd.GeoSeries([province_orig], crs=3401).plot(
        ax=ax, facecolor="none", edgecolor="#0e0e0e",
        linewidth=1.4, linestyle="-", alpha=0.55, zorder=1,
    )
    # Plus a fainter dashed echo just outside it to add depth
    gpd.GeoSeries([province_orig.buffer(8000)], crs=3401).plot(
        ax=ax, facecolor="none", edgecolor="#0e0e0e",
        linewidth=0.4, linestyle=(0, (1, 3)), alpha=0.25, zorder=1,
    )

    no_vote_color = "#cfcbc4"

    # 7a. Motion ghosts — for each ED, draw GHOST_STEPS faint copies trailing
    #     from near-Edmonton out to the just-before-final position. Innermost
    #     ghost is faintest, outermost ghost (frame just before final) is the
    #     boldest of the ghosts.
    for _, row in eds.iterrows():
        g = row.geometry  # original (pre-explode)
        dx, dy = row["disp"]
        if abs(dx) < 1.0 and abs(dy) < 1.0:
            continue  # essentially static — no ghosts needed
        if row["total"] > 0:
            color = cmap(norm(row["ucp_share"]))
        else:
            color = no_vote_color
        for k in range(1, GHOST_STEPS + 1):
            frac = k / (GHOST_STEPS + 1)  # 0.25, 0.5, 0.75 for GHOST_STEPS=3
            ghost = shapely.affinity.translate(g, dx * frac, dy * frac)
            ghost_alpha = GHOST_ALPHA_BASE * frac  # later ghosts brighter
            gpd.GeoSeries([ghost], crs=3401).plot(
                ax=ax, facecolor=color, edgecolor="none",
                alpha=ghost_alpha, zorder=2,
            )

    # 7b. Final exploded EDs on top of their motion ghosts
    for _, row in eds.iterrows():
        g = row["exploded"]
        if g is None or g.is_empty:
            continue
        if row["total"] > 0:
            color = cmap(norm(row["ucp_share"]))
        else:
            color = no_vote_color
        gpd.GeoSeries([g], crs=3401).plot(
            ax=ax, facecolor=color, edgecolor="#1a1a1a",
            linewidth=0.35, alpha=0.95, zorder=3,
        )

    # 7c. Tiny epicentre marker at Edmonton — subtle dark dot to anchor the eruption
    ax.scatter(
        [EDMONTON[0]], [EDMONTON[1]],
        s=18, c="#0e0e0e", marker="o", zorder=4,
        edgecolors="none", alpha=0.7,
    )

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
  height: 10.95in;        /* 0.05in shy of letter to defeat Chrome's blank-page heuristic */
  background: #f5ede0;
  overflow: hidden;
  padding: 0.7in 0.8in;
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

.legend .swatch-ucp { background: #225d9e; }
.legend .swatch-tied { background: #f4efe6; border: 0.5pt solid #888; }
.legend .swatch-ndp { background: #ea7414; }
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
    <span><span class="swatch swatch-ucp"></span>UCP-leaning</span>
    <span><span class="swatch swatch-tied"></span>50/50</span>
    <span><span class="swatch swatch-ndp"></span>NDP-leaning</span>
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
    # Take only the first page of the cover — Chrome's PDF renderer
    # sometimes appends a blank trailing page when content fits exactly to
    # the @page boundary.
    cover_reader = pypdf.PdfReader(str(cover_pdf))
    writer.add_page(cover_reader.pages[0])
    writer.append(str(article_pdf))
    with open(out_pdf, "wb") as f:
        writer.write(f)
    print(
        f"[build_cover] Merged final PDF {out_pdf.relative_to(REPO_ROOT)} "
        f"({out_pdf.stat().st_size/1024:.1f} KB, "
        f"{len(cover_reader.pages)} cover page(s) → first page only)"
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

    # 4. Article PDF — regenerate via the existing pipeline (writes article.pdf)
    print("[build_cover] Regenerating article body...")
    build_pdf_py = REPO_ROOT / "analysis" / "scripts" / "build_pdf.py"
    subprocess.run(
        [sys.executable, str(build_pdf_py)],
        check=True,
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )
    if not ARTICLE_PDF.exists():
        raise RuntimeError(
            f"build_pdf.py did not produce {ARTICLE_PDF}. "
            "Possible cause: article.pdf held open by another process."
        )

    # 5. Merge cover + article into final report_public.pdf
    merge_pdfs(cover_pdf_path, ARTICLE_PDF, OUT_PDF)

    # Cleanup the cover-only intermediate (keep article.pdf — it's the
    # standalone artefact that build_pdf.py advertises as its output).
    try:
        cover_pdf_path.unlink()
    except OSError:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
