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
        maps/cover_art.svg as the hero image (also referenced in cover).

Dependencies: geopandas, shapely, matplotlib, markdown, pypdf, pypdfium2.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import subprocess
import sys
import tempfile
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pypdf

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ALBERTA_EDS = data_loader._resolve_path("data") / "shapefiles" / "reference" / "alberta_2019_eds"
DERIVED = data_loader._resolve_path("data") / "shapefiles" / "derived"
# Prefer v0_9 (topological VA-dissolve, gapless by construction) →
# v0_8 refined → v0_8 canonical → v0_7 canonical
CANONICAL = data_loader._resolve_path("data") / "shapefiles" / "canonical"
APPROX_MAJ_CANDIDATES = [
    CANONICAL / "ea_majority_2026_eds.gpkg",
    DERIVED / "v0_10_topological_majority_2026_eds.gpkg",
    DERIVED / "v0_8_refined_majority_2026_eds.gpkg",
    DERIVED / "v0_8_canonical_majority_2026_eds.gpkg",
    DERIVED / "v0_7_canonical_majority_2026_eds.gpkg",
]
APPROX_MIN_CANDIDATES = [
    CANONICAL / "ea_minority_2026_eds.gpkg",
    DERIVED / "v0_10_topological_minority_2026_eds.gpkg",
    DERIVED / "v0_8_refined_minority_2026_eds.gpkg",
    DERIVED / "v0_8_canonical_minority_2026_eds.gpkg",
    DERIVED / "v0_7_canonical_minority_2026_eds.gpkg",
]
# Phase 4C VA→2026-ED assignments (conservation-exact crosswalk authored by
# the topological resolver). Used by the heatmap fill to assign each VA
# its parent 2026 ED.
VA_TO_2026_ASSIGNMENTS = (
    REPO_ROOT / "analysis" / "assignment_va_to_2026_assignments.csv"
)

COVER_ART_PNG = data_loader._resolve_path("data") / "maps" / "cover_art.png"
OUT_PDF = (
    REPO_ROOT / "report_public.pdf"
)  # final = cover + article (the only PDF in the repo root)
ARTICLE_PDF = (
    REPO_ROOT / ".temp" / "article.pdf"
)  # intermediate, written by build_pdf.py to .temp/

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


VA_VOTES_PATH = (
    data_loader._resolve_path("data") / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
)


def _pick(candidates):
    for p in candidates:
        if p.exists():
            return p
    return None


def build_cover_art() -> Path:
    """Cover hero: the 2026 minority commission map, rendered in its actual
    geographic positions, with each ED coloured by 2023 two-party vote share.

    No radial displacement, no exploded-diagram pull-apart, no perspective
    scaling — just the map as the minority commissioners proposed it.

    Colour:
    - Direct UCP-blue ↔ NDP-orange interpolation, centred on 50/50.
      Canadian convention: UCP/Conservative blue, NDP orange.
    - VA centroids spatially joined into v0_8 EDs for per-ED 2023 totals.
      EDs catching zero VAs (inherited-empty from v0_7) get neutral grey.
    """
    import matplotlib.colors as mcolors

    # 1. Pick map (prefer v0_8 refined → canonical → v0_7).
    # Use the MINORITY map: this is the map the audit ends up critiquing,
    # so it's the one the cover should put in front of the reader.
    map_path = _pick(APPROX_MIN_CANDIDATES)
    if map_path is None:
        raise FileNotFoundError("No minority GPKG candidate available")
    print(f"[build_cover] Hero ED source: {map_path.name}")

    eds = gpd.read_file(map_path).to_crs(3401)
    name_col = "name_2026" if "name_2026" in eds.columns else eds.columns[0]
    eds = eds[eds.geometry.area > 1e6].copy().reset_index(drop=True)
    print(f"[build_cover] {len(eds)} non-empty EDs to render")

    # 2. Per-ED 2023 vote share via VA-centroid spatial join
    if VA_VOTES_PATH.exists():
        va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
        va_pts = gpd.GeoDataFrame(
            {"va_ucp": va["va_ucp"].fillna(0), "va_ndp": va["va_ndp"].fillna(0)},
            geometry=va.geometry.centroid,
            crs=3401,
        )
        joined = gpd.sjoin(
            va_pts,
            eds[[name_col, "geometry"]],
            how="left",
            predicate="within",
        )
        agg = (
            joined.groupby(name_col)
            .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
            .reset_index()
        )
        agg["total"] = (agg["ucp"] + agg["ndp"]).clip(lower=1)
        agg["ucp_share"] = agg["ucp"] / agg["total"]
        eds = eds.merge(agg[[name_col, "ucp_share", "total"]], on=name_col, how="left")
    else:
        print(
            f"[build_cover] WARN: {VA_VOTES_PATH.name} not found; "
            f"all EDs will render as neutral 50/50"
        )
        eds["ucp_share"] = 0.5
        eds["total"] = 0
    eds["ucp_share"] = eds["ucp_share"].fillna(0.5)
    eds["total"] = eds["total"].fillna(0)
    eds["inferred"] = False
    print(
        f"[build_cover] {int((eds['total'] > 0).sum())}/{len(eds)} EDs received VA votes"
    )

    # 2b. Crosswalk-inheritance fallback for EDs the centroid-join missed.
    # The v0_8 reconstruction inherits some 2026 minority polygons from v0_7
    # (which itself inherits from 2019), and a handful end up in physical
    # positions where no 2023 VA centroid falls inside them. For those we
    # look up the 2019 parent ED(s) via minority_hybrid_crosswalk.csv
    # and aggregate the VAs that belonged to those parents — yielding the
    # 2019-vote-distribution-projected-onto-this-2026-name share. This
    # CANNOT model the partisan effect of the boundary shift; it's an
    # illustrative fill, not a quantitative claim, and the cover caption
    # discloses it.
    crosswalk_path = data_loader._resolve_path("data") / "minority_hybrid_crosswalk.csv"
    if VA_VOTES_PATH.exists() and crosswalk_path.exists():
        import pandas as pd

        cw = pd.read_csv(crosswalk_path)
        # 2026-name -> list of 2019 parents (drop "(NEW)" sentinel rows)
        cw_real = cw[cw["current_2019"].astype(str) != "(NEW)"]
        parents_by_2026 = (
            cw_real.groupby("proposed_2026")["current_2019"]
            .apply(lambda s: [p for p in s.dropna().unique()])
            .to_dict()
        )
        miss_mask = eds["total"] == 0
        n_inferred = 0
        for idx in eds.index[miss_mask]:
            ed_name = eds.at[idx, name_col]
            parents = parents_by_2026.get(ed_name, [])
            if not parents:
                continue
            inh = va[va["parent_ed_2019"].isin(parents)]
            ucp_sum = float(inh["va_ucp"].fillna(0).sum())
            ndp_sum = float(inh["va_ndp"].fillna(0).sum())
            if (ucp_sum + ndp_sum) <= 0:
                continue
            eds.at[idx, "ucp_share"] = ucp_sum / (ucp_sum + ndp_sum)
            eds.at[idx, "total"] = ucp_sum + ndp_sum
            eds.at[idx, "inferred"] = True
            n_inferred += 1
        print(
            f"[build_cover] inferred 2019-parent vote share for "
            f"{n_inferred} EDs missed by centroid-join"
        )

    # 2c. Final fallback for any ED still grey (genuinely new 2026
    # creations with no 2019 parent in the crosswalk, or parent rows
    # whose VAs all aggregated to zero votes). Use the K nearest VA
    # centroids to the ED's own centroid. Crude, but guarantees the
    # cover renders no grey districts.
    if VA_VOTES_PATH.exists():
        from shapely.geometry import Point

        K = 25
        still_missing = eds["total"] == 0
        n_nearest = 0
        if still_missing.any():
            va_centroids = list(
                zip(
                    va.geometry.centroid.x.values,
                    va.geometry.centroid.y.values,
                    va["va_ucp"].fillna(0).values,
                    va["va_ndp"].fillna(0).values,
                )
            )
            for idx in eds.index[still_missing]:
                gc = eds.at[idx, "geometry"].centroid
                dists = [
                    (((cx - gc.x) ** 2 + (cy - gc.y) ** 2), u, n)
                    for cx, cy, u, n in va_centroids
                ]
                dists.sort(key=lambda t: t[0])
                near = dists[:K]
                ucp_sum = float(sum(u for _, u, _ in near))
                ndp_sum = float(sum(n for _, _, n in near))
                if (ucp_sum + ndp_sum) <= 0:
                    continue
                eds.at[idx, "ucp_share"] = ucp_sum / (ucp_sum + ndp_sum)
                eds.at[idx, "total"] = ucp_sum + ndp_sum
                eds.at[idx, "inferred"] = True
                n_nearest += 1
            print(
                f"[build_cover] nearest-{K}-VA fallback used for "
                f"{n_nearest} EDs with no crosswalk parent"
            )

    # 3. Direct UCP-blue → NDP-orange interpolation. Tighter norm window
    #    (35–75%) pushes more EDs toward full saturation for a bolder look.
    ndp_orange = (0.92, 0.40, 0.05)   # richer orange
    ucp_blue   = (0.08, 0.28, 0.58)   # deeper blue
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "ucp_ndp_direct", [ndp_orange, ucp_blue], N=256
    )
    norm = mcolors.Normalize(vmin=0.35, vmax=0.75, clip=True)

    # 4. Render — VA-level fill with population-density lightness modulation.
    #    Each VA gets the partisan colour of its assigned 2026 ED (hue), and
    #    a lightness scaled by VA-local population density (paler = sparse,
    #    darker = dense). This gives the reader two signals in a single
    #    image: the partisan-leaning hue (blue/orange) and the population-
    #    centre heatmap (where within an ED the people actually are). The
    #    v0_9 substrate's polygon boundaries are overlaid as thin lines so
    #    the 89-district structure remains visible.
    fig, ax = plt.subplots(figsize=(6.0, 9), dpi=300)
    fig.patch.set_facecolor('none')   # transparent background
    ax.set_facecolor('none')          # transparent axes
    ax.set_aspect("equal")
    ax.axis("off")

    # Build the per-VA dataframe. Hue is determined by EACH VA's OWN 2023
    # partisan share (not the parent ED's average), so a UCP stronghold
    # inside an NDP-leaning ED renders as a blue cluster on an orange
    # field, and an NDP stronghold inside a UCP ED renders as orange
    # inside the surrounding blue. ED-level partisan lean still emerges
    # naturally because most VAs in an ED tend to lean the same way.
    import pandas as pd

    va_render = va.copy()
    va_ucp_total = va_render["va_ucp"].fillna(0)
    va_ndp_total = va_render["va_ndp"].fillna(0)
    va_two_party = (va_ucp_total + va_ndp_total).clip(lower=1.0)
    va_render["parent_ucp_share"] = va_ucp_total / va_two_party

    # Per-VA population density and lightness modulation.
    # pop_2021 is on the va frame from the centroid build above; if missing,
    # fall back to vote-weighted proxy.
    if "pop_2021" in va_render.columns:
        pop = va_render["pop_2021"].fillna(0).clip(lower=0)
    else:
        pop = (
            va_render["va_ucp"].fillna(0)
            + va_render["va_ndp"].fillna(0)
            + va_render["va_other"].fillna(0)
        )
    area_m2 = va_render.geometry.area.clip(lower=1.0)
    density = pop / area_m2  # people per m^2
    # Heatmap-style: log-scale density; blend each VA's partisan colour
    # with cover-ivory by a lightness weight in [0, 1].
    # weight=0 -> pure ivory (very low density), weight=1 -> full saturated
    # partisan colour (very high density).
    import numpy as np

    log_d = np.log10(density.replace(0, np.nan)).fillna(-12.0)
    d_min, d_max = -8.5, -3.5
    weight = ((log_d - d_min) / (d_max - d_min)).clip(0.0, 1.0)

    _white = np.array([1.0, 1.0, 1.0])

    def _va_fill(ucp_share, w):
        # Density encoded as lightness, not alpha — fully opaque throughout.
        # Sparse rural → pale tint of the partisan colour.
        # Dense urban  → full saturation.
        # No semi-transparent patches; the map reads cleanly at any zoom.
        base = np.array(cmap(norm(ucp_share)))[:3]
        t = float(np.clip(w ** 0.6, 0.18, 1.0))   # gamma curve keeps rural readable
        colored = (1.0 - t) * _white + t * base
        return (*colored, 1.0)   # always fully opaque

    va_render["_fill"] = [
        _va_fill(s, w) for s, w in zip(va_render["parent_ucp_share"], weight.values)
    ]

    # 4a. Province interior fill: white so sparse rural areas (low alpha VAs)
    #     show white rather than the transparent page background. Outside the
    #     province boundary remains transparent (shows the dark page through).
    province = eds.dissolve()
    province.plot(ax=ax, color="white", linewidth=0)

    # 4b. VA layer on top — heatmap-modulated fills carry the population-
    #     density signal where VAs exist (i.e. where people actually live).
    va_render.plot(
        ax=ax,
        color=va_render["_fill"].tolist(),
        linewidth=0,
    )

    # 4c. ED boundaries overlaid last so the 89-district structure
    #     remains readable through the heatmap.
    eds.boundary.plot(
        ax=ax,
        edgecolor="#1a1a1a",
        linewidth=0.55,
    )

    # 4d. Provincial outline: trace the outer edge in the same accent red
    #     as the title's period so the silhouette pops off the dark backdrop.
    province.boundary.plot(
        ax=ax,
        edgecolor="#7a1f1f",  # title-accent red
        linewidth=3.5,
    )

    ax.margins(0.005)
    plt.tight_layout(pad=0)

    COVER_ART_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        COVER_ART_PNG,
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.02,
        facecolor='none',
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
  background: #cccccc;        /* 20% grey full-bleed */
  font-family: "Lora", Georgia, serif;
  color: #1a1a1a;
}

.cover {
  position: relative;
  width: 8.5in;
  height: 10.95in;        /* 0.05in shy of letter to defeat Chrome's blank-page heuristic */
  background: #cccccc;
  overflow: hidden;
  padding: 0.4in 0.5in;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* Vertical accent bar on the left — anchored at the BODY level so it
   extends the full 11in page height (full bleed). The .cover element
   is intentionally 0.05in shy of letter height to avoid Chrome's
   blank-page heuristic; if the bar were anchored to .cover, it would
   stop short of the bottom edge by that 0.05in. Anchoring to body
   guarantees full edge-to-edge bleed. */
body::before {
  content: "";
  position: absolute;
  left: 0; top: 0;
  width: 0.28in;
  height: 11in;
  background: linear-gradient(to bottom, #7a1f1f 0%, #7a1f1f 32%, #e87722 32%, #e87722 66%, #335c81 66%, #335c81 100%);
  z-index: 1;
}

/* ----- Kicker ----- */
.kicker {
  font-family: "Source Sans 3", sans-serif;
  font-size: 9pt;
  font-weight: 700;
  letter-spacing: 4pt;
  text-transform: uppercase;
  color: #7a1f1f;
  margin: 0 0 0.1in 0;
  padding-top: 0.05in;
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
  /* Negative horizontal margin lets the hero bleed past the .cover's
     0.8in side padding all the way to the page edges. */
  margin: 0.05in -0.8in 0.1in -0.52in;   /* leave 0.28in for the left accent bar */
  min-height: 0;
}

.hero img {
  max-width: 100%;           /* fills the bleed area */
  max-height: 8.25in;        /* 75% of 11in page height — map is the dominant visual */
  height: auto;
  object-fit: contain;
  display: block;
}

.hero-caption {
  font-family: "Lora", Georgia, serif;
  font-style: italic;
  font-size: 6.5pt;
  line-height: 1.3;
  color: #8a8074;
  text-align: right;
  margin: 0.06in 0 0 0;
  padding: 0.04in 0 0 0;
  border-top: 0.4pt solid #d3cabd;
  letter-spacing: 0.1pt;
}

.hero-caption::before {
  content: "Cover map · ";
  font-family: "Source Sans 3", sans-serif;
  font-style: normal;
  font-weight: 700;
  font-size: 6.5pt;
  letter-spacing: 1.5pt;
  text-transform: uppercase;
  color: #7a1f1f;
  margin-right: 0.3em;
}

/* ----- Title block ----- */
.title-block {
  margin: 0 0 0.08in 0;
}

.title {
  font-family: "Playfair Display", Georgia, serif;
  font-weight: 900;
  font-size: 36pt;
  letter-spacing: -0.8pt;
  line-height: 1.0;
  color: #0e0e0e;
  margin: 0 0 0.08in 0;
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
  font-size: 9.5pt;
  line-height: 1.3;
  color: #3a3a3a;
  max-width: 6.5in;
  margin: 0 0 0.08in 0;
}

/* ----- Footer: byline + locator ----- */
.footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-top: 1px solid #1a1a1a;
  padding-top: 0.06in;
  margin-top: 0.04in;
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
  text-decoration: none;
  /* Border-bottom (not text-decoration) survives both colour and
     grayscale renders on e-ink readers; the colour itself collapses
     to mid-gray on monochrome. */
  border-bottom: 0.6pt solid #1a1a1a;
  padding-bottom: 0.5pt;
}
.locator .url:hover { text-decoration: underline; }

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
  font-size: 7.5pt;
  letter-spacing: 1.2pt;
  text-transform: uppercase;
  font-weight: 600;
  color: #555;
  margin: 0 0 0.06in 0;
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
    <img src="{hero_src}" alt="Alberta with the 2026 minority commission map overlaid, each electoral district coloured by 2023 vote share.">
  </div>

  <div class="legend">
    <span><span class="swatch swatch-ucp"></span>UCP-leaning</span>
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
      Audit executive summary
      <a class="url" href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a>
    </div>
  </div>

  <p class="hero-caption">The 2026 minority commission proposal — the map this audit ends up critiquing. Each district is coloured by its 2023 UCP–NDP vote share.</p>

</div>
</body>
</html>
"""


def build_cover_html(hero_path: Path) -> str:
    # Embed the hero via file:// URL so Chrome finds it at render time.
    # Use plain string replace to avoid str.format colliding with CSS braces.
    hero_src = hero_path.resolve().as_uri()
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
        f"{len(cover_reader.pages)} cover page(s) -> first page only)"
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
