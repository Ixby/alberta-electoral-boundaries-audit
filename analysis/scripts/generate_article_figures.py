# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
v0_1_generate_article_figures.py

Magazine-legible figures for the article. Replaces the two-panel geographic
overlays (v2) with visual metaphors matched to what each figure is actually
claiming.

Design premise:
  - The claim in the Airdrie, Lethbridge, and Red Deer figures is about
    *partition count* ("how many districts is this city split into?"). That
    is a schematic claim, not a geographic one. v3 renders it as a pair of
    horizontal bars - top bar = majority proposal, bottom bar = minority
    proposal - with each bar divided into labelled segments, one per
    district. Readable at column width, legible at a glance.
  - The claim in the Calgary figure IS partly geographic (rural territory
    pulled from specific compass directions into Calgary-named hybrids).
    v3 renders it as a single minimal map showing only the Calgary
    municipal outline plus the three minority hybrids that best illustrate
    the NW / S / W pulls. Surrounding context is greyed out.

Outputs
  - maps/article/figure_airdrie_v3.svg
  - maps/article/figure_lethbridge_v3.svg
  - maps/article/figure_reddeer_v3.svg
  - maps/article/figure_calgary_v3.svg

Run
  PYTHONIOENCODING=utf-8 python analysis/scripts/generate_article_figures.py

Dependencies (corrected 2026-07-13 — this docstring referenced the deprecated
DPG-era `v0_10_topological_minority_2026_eds.gpkg`; the actual code (PATH_MIN_V7,
below) already loads the canonical shapefile and always has)
  Forward  : data/shapefiles/canonical/ea_minority_2026_eds.gpkg,
             data/shapefiles/reference/alberta_2021_csds.gpkg,
             data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
  Backward : data/maps/article/figure_*_v3.svg,
             findings/article_figures_v3.md,
             report_public.md (four figure references updated to _v3)

Author: sub-agent, article figure redesign, 2026-04-23

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import sys
import logging
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.patches import FancyBboxPatch, Rectangle
from shapely.geometry import Point
from shapely.ops import unary_union

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# ---------------------------------------------------------------------------
# Paths

ROOT = Path(__file__).resolve().parent.parent.parent
logger = logging.getLogger(__name__)
DATA = data_loader._resolve_path("data")
OUT = data_loader._resolve_path("data") / "maps" / "article"
OUT.mkdir(parents=True, exist_ok=True)

PATH_MIN_V7 = DATA / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"
PATH_CSDS = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
PATH_2019 = (
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)

CRS_PLOT = 3401  # NAD83 / Alberta 10-TM Forest, metres

# ---------------------------------------------------------------------------
# Palette & typography

from palette import (
    MAJORITY_SEGMENT_COLORS,
    MINORITY_SEGMENT_COLORS,
)

# Site-integration retint (2026-07-13): surfaces and inks now come from
# palette.py's viewer tokens so the schematic sits on the same paper as the
# page around it. Names kept; values re-pointed.
from palette import PAPER_BG as _PAPER, INK_TEXT as _INK, INK_MUTED as _INK_MUTED, INK_SUBTLE as _INK_SUBTLE, save_fig as _save_fig
COLOR_BG = _PAPER          # viewer --bg: warm paper
COLOR_INK = _INK           # viewer --text
COLOR_INK_SOFT = _INK_MUTED   # viewer --text-muted
COLOR_GREY_MUTED = _INK_SUBTLE  # viewer --text-subtle

# Rural-carve colour for segments whose primary population is outside the
# city - visually distinct from both palette families.
COLOR_RURAL = "#8b5a2b"  # muted umber
COLOR_RURAL_EDGE = "#5a3a1c"

# Fonts. Per spec: Playfair Display bold for titles, Source Sans 3 for
# labels; fall through to Georgia + Arial if the editorial fonts aren't
# installed. On Windows both Georgia and Arial are present, so we don't
# emit the matplotlib font-fallback warning.
from matplotlib import font_manager as _fm

_INSTALLED = {f.name for f in _fm.fontManager.ttflist}
# Site faces (2026-07-13): titles in the site's serif accent (Palatino), labels
# in Arial (metrically close to the site's Segoe UI). SVGs are saved as live
# text and palette.harmonize_svg rewrites these to the full site font stacks.
FONT_TITLE = "Palatino Linotype" if "Palatino Linotype" in _INSTALLED else "Georgia"
FONT_LABEL = "Arial"
plt.rcParams["svg.fonttype"] = "none"

# Canvas geometry - magazine page width. Per spec ~2000x1350 px (7" at 300
# dpi). We use 7.0 x 4.67 for a clean 3:2 aspect.
FIG_DPI = 300
FIG_W_IN = 7.0  # 2100 px at 300 dpi
FIG_H_IN = 4.67  # 1401 px at 300 dpi - ~3:2 aspect


# ---------------------------------------------------------------------------
# Schematic bar helpers


@dataclass
class Segment:
    label: str
    color: str
    sublabel: str = ""
    is_rural_carve: bool = False
    proportion: float = 1.0  # relative weight (bar width share)


def draw_bar(
    ax,
    y_top: float,
    y_bot: float,
    segments: list[Segment],
    x_left: float = 0.05,
    x_right: float = 0.95,
    fig_width_in: float = FIG_W_IN,
) -> None:
    """Render a single horizontal bar as a stack of coloured segments.

    Each segment is labelled inline. Label font size scales to fit the
    segment width; very long names are wrapped onto two lines split at a
    hyphen or space. Sublabels appear beneath the label in smaller italic.
    """
    total = sum(s.proportion for s in segments)
    x = x_left
    width_total = x_right - x_left
    for seg in segments:
        w = width_total * (seg.proportion / total)
        # A segment too narrow to hold its own label (e.g. a few hundred
        # people out of a city) is drawn to scale and labelled below the bar,
        # right-aligned to the bar's end, with a short leader line.
        if w * fig_width_in < 0.30:
            ax.add_patch(Rectangle((x, y_bot), max(w, 0.0015), y_top - y_bot,
                                   facecolor=seg.color, edgecolor=COLOR_INK,
                                   linewidth=0.5, zorder=4))
            cx = x + w / 2
            ax.plot([cx, cx], [y_bot, y_bot - 0.022], color=COLOR_INK,
                    lw=0.6, zorder=4)
            callout = seg.label + (f" · {seg.sublabel}" if seg.sublabel else "")
            ax.text(min(cx + 0.004, x_right), y_bot - 0.028, callout,
                    ha="right", va="top", fontsize=7.5, fontstyle="italic",
                    family=FONT_LABEL, color=COLOR_INK_SOFT, zorder=5)
            x += w
            continue
        rect = FancyBboxPatch(
            (x, y_bot),
            w,
            y_top - y_bot,
            boxstyle="round,pad=0.0,rounding_size=0.006",
            facecolor=seg.color,
            edgecolor=COLOR_INK,
            linewidth=0.77,
            zorder=3,
        )
        ax.add_patch(rect)

        # Convert segment width from axes-fraction to inches to estimate
        # how many characters fit in the bar.
        seg_width_in = w * fig_width_in
        # At fontsize N pt, average character width is ~N * 0.52 pt
        # (72 pt per inch). So approx chars-per-inch = 72 / (N * 0.52).
        # Rearranging: fontsize = 72 * seg_width_in / (chars * 0.52).
        label = seg.label
        # Try to fit on a single line at fontsize 10.5. If not, try two
        # lines, split at the most visually balanced break point.
        best_lines = [label]
        best_fs = 10.5

        def fits(lines, fs):
            max_len = max(len(ln) for ln in lines)
            # Leave 0.08" of padding inside the segment for whitespace
            usable_in = max(seg_width_in - 0.10, 0.02)
            needed_in = max_len * fs * 0.52 / 72.0
            return needed_in <= usable_in

        # Try single line at decreasing sizes
        single_fs = None
        for fs in (11.0, 10.0, 9.0, 8.0, 7.2):
            if fits([label], fs):
                single_fs = fs
                break

        # Try two-line split at a hyphen or space
        two_line_result = None
        if single_fs is None or single_fs <= 7.2:
            split_candidates = []
            # Prefer hyphen splits (the district names are hyphenated
            # compounds, so hyphens are natural break points)
            for i, ch in enumerate(label):
                if ch == "-":
                    split_candidates.append(i + 1)
                elif ch == " ":
                    split_candidates.append(i + 1)
            # Rank candidates by how close the split is to the midpoint
            split_candidates.sort(key=lambda i: abs(i - len(label) / 2))
            for sp in split_candidates:
                left = label[:sp].rstrip("- ")
                right = label[sp:].lstrip("- ")
                if not left or not right:
                    continue
                for fs in (10.5, 9.5, 8.5, 7.5):
                    if fits([left, right], fs):
                        two_line_result = ([left, right], fs)
                        break
                if two_line_result:
                    break

        if two_line_result is not None and (
            single_fs is None or two_line_result[1] > single_fs
        ):
            best_lines, best_fs = two_line_result
        elif single_fs is not None:
            best_lines, best_fs = [label], single_fs
        else:
            # Fall through: rotate 90° for very narrow segments
            best_lines, best_fs = [label], 7.0

        # Rendering position: centered. If there's a sublabel, nudge the
        # label up so the sublabel fits underneath.
        y_mid = (y_top + y_bot) / 2
        label_text = "\n".join(best_lines)
        sub_offset = 0.028 if seg.sublabel else 0.0
        n_label_lines = len(best_lines)
        # Shift label up by half the sublabel space + half the extra line
        # space if multi-line
        if n_label_lines == 1:
            y_label = y_mid + sub_offset * 0.55
        else:
            y_label = y_mid + sub_offset * 0.55 + 0.005

        # Sublabel size, decided before placement. Shrink for narrow
        # segments; two-line labels already consume most of the vertical
        # space, so shrink the sublabel further in that case.
        sub_fs = None
        n_sub_lines = 0
        if seg.sublabel:
            sub_fs = max(best_fs - 2.8, 6.2)
            if n_label_lines >= 2:
                sub_fs = max(sub_fs - 0.8, 5.8)
            # Widest line, not the whole string: a two-line sublabel is as
            # wide as its longer line.
            sub_w_in = max(len(ln) for ln in seg.sublabel.split("\n")) * sub_fs * 0.52 / 72.0
            if sub_w_in > seg_width_in - 0.05:
                sub_fs = max(sub_fs - 1.0, 5.5)
            n_sub_lines = seg.sublabel.count("\n") + 1
        # A multi-line sublabel (2026-11-01, Airdrie shares): centre the
        # label + sublabel stack in the bar so neither runs off its edge.
        # The axes spans the whole figure, so 1 pt = 1 / (FIG_H_IN * 72).
        sub_y_stacked = None
        if n_sub_lines >= 2:
            # Stacking frees vertical room, so keep the sublabel at a
            # readable 6.5 pt where the segment is wide enough for it.
            longest = max(len(ln) for ln in seg.sublabel.split("\n"))
            sub_fs = max(sub_fs, min(6.5, (seg_width_in - 0.10) * 72.0 / (longest * 0.52)))
            pt = 1.0 / (FIG_H_IN * 72.0)
            label_h = n_label_lines * best_fs * 1.15 * pt
            sub_h = n_sub_lines * sub_fs * 1.2 * pt
            gap = 3.0 * pt
            top = y_mid + (label_h + gap + sub_h) / 2
            y_label = top - label_h / 2
            sub_y_stacked = top - label_h - gap - sub_h / 2

        # Flip main label to light on dark segments for contrast
        try:
            import matplotlib.colors as mc

            r, g, b = mc.to_rgb(seg.color)
            luma = 0.299 * r + 0.587 * g + 0.114 * b
        except Exception as e:
            logger.debug("color luma calculation failed, defaulting to light: %s", e)
            luma = 1.0
        label_color = "#ffffff" if luma < 0.45 else COLOR_INK
        ax.text(
            x + w / 2,
            y_label,
            label_text,
            ha="center",
            va="center",
            fontsize=best_fs,
            fontweight="bold",
            family=FONT_LABEL,
            color=label_color,
            zorder=5,
            linespacing=1.0,
        )
        if seg.sublabel:
            # On dark segments, the near-black sublabel becomes illegible.
            # Compute segment brightness (simple luma) and flip to a pale
            # colour when the fill is dark.
            try:
                import matplotlib.colors as mc

                r, g, b = mc.to_rgb(seg.color)
                luma = 0.299 * r + 0.587 * g + 0.114 * b
            except Exception as e:
                logger.debug("color luma calculation failed, defaulting to light: %s", e)
                luma = 1.0
            sublabel_color = "#ece6d4" if luma < 0.45 else COLOR_INK_SOFT
            # Clamp sublabel y so it stays inside the rectangle. The
            # rectangle spans [y_bot, y_top]; keep sublabel baseline at
            # least 0.015 above y_bot.
            sub_y_raw = y_mid - 0.024 * n_label_lines - 0.018
            sub_y = max(sub_y_raw, y_bot + 0.018)
            if sub_y_stacked is not None:
                sub_y = sub_y_stacked
            ax.text(
                x + w / 2,
                sub_y,
                seg.sublabel,
                ha="center",
                va="center",
                fontsize=sub_fs,
                fontstyle="italic",
                family=FONT_LABEL,
                color=sublabel_color,
                zorder=5,
            )
        x += w


def _wrap_to_width(text: str, max_chars: int) -> str:
    """Insert newlines at word boundaries so no line exceeds max_chars."""
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= max_chars:
            cur = cur + " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def draw_schematic(
    fig_path: Path,
    title: str,
    subtitle: str,
    maj_label: str,
    maj_segments: list[Segment],
    min_label: str,
    min_segments: list[Segment],
    inset_callouts: list[tuple[str, str]] | None = None,
    caption: str = "",
    source: str = "Source: commission majority report Appendix A and minority report Appendix E.",
) -> None:
    """Render a two-bar schematic figure.

    Layout (axes fraction):
      0.88-0.98  figure title (serif)
      0.80-0.86  subtitle (one or two wrapped lines)
      0.72       majority bar header
      0.56-0.70  majority bar
      0.44       minority bar header + (optional) inset header
      0.26-0.40  minority bar + inset column
      0.12-0.20  caption (italic, grey)
      0.03-0.07  source credit
    """
    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN), dpi=FIG_DPI, facecolor=COLOR_BG)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    ax.set_facecolor(COLOR_BG)

    # Title - auto-shrink if needed to fit in the 0.88 width band. At
    # fontsize N pt and average glyph width ~N * 0.55 pt, max chars on the
    # line = 0.88 * 7.0 * 72 / (N * 0.55). For N=20, that's ~40 chars.
    title_max_chars_at_20pt = int(0.88 * FIG_W_IN * 72 / (20 * 0.55))
    if len(title) <= title_max_chars_at_20pt:
        title_fs = 20.0
    elif len(title) <= int(0.88 * FIG_W_IN * 72 / (18 * 0.55)):
        title_fs = 18.0
    elif len(title) <= int(0.88 * FIG_W_IN * 72 / (16 * 0.55)):
        title_fs = 16.0
    else:
        title_fs = 15.0
    ax.text(
        0.05,
        0.96,
        title,
        ha="left",
        va="top",
        fontsize=title_fs,
        fontweight="bold",
        family=FONT_TITLE,
        color=COLOR_INK,
    )

    # Subtitle - wrap to ~100 chars so it never exceeds the page width.
    # At fontsize 9.5 pt, ~0.88 * 7.0 * 72 / (9.5 * 0.52) = ~90 chars/line.
    if subtitle:
        sub_wrapped = _wrap_to_width(subtitle, max_chars=95)
        ax.text(
            0.05,
            0.86,
            sub_wrapped,
            ha="left",
            va="top",
            fontsize=9.5,
            family=FONT_LABEL,
            color=COLOR_INK_SOFT,
            linespacing=1.35,
        )

    # Majority bar header
    ax.text(
        0.05,
        0.72,
        maj_label,
        ha="left",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        family=FONT_LABEL,
        color=COLOR_INK,
    )
    draw_bar(
        ax,
        y_top=0.70,
        y_bot=0.55,
        segments=maj_segments,
        x_left=0.05,
        x_right=0.95,
        fig_width_in=FIG_W_IN,
    )

    # Minority bar header
    x_min_right = 0.95 if not inset_callouts else 0.62
    ax.text(
        0.05,
        0.43,
        min_label,
        ha="left",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        family=FONT_LABEL,
        color=COLOR_INK,
    )
    draw_bar(
        ax,
        y_top=0.41,
        y_bot=0.26,
        segments=min_segments,
        x_left=0.05,
        x_right=x_min_right,
        fig_width_in=FIG_W_IN * (x_min_right - 0.05) / 0.9,
    )

    # Inset callouts on the right: three tiny rural-outline markers with
    # arrows pointing to the rural-community name.
    if inset_callouts:
        ax.text(
            0.67,
            0.43,
            "Rural pulls",
            ha="left",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            family=FONT_LABEL,
            color=COLOR_INK,
        )
        step = 0.045
        y0 = 0.39
        for i, (district, pull) in enumerate(inset_callouts):
            cy = y0 - i * step
            mrk = Rectangle(
                (0.67, cy - 0.010),
                0.018,
                0.018,
                facecolor=COLOR_RURAL,
                edgecolor=COLOR_RURAL_EDGE,
                linewidth=0.8,
            )
            ax.add_patch(mrk)
            ax.annotate(
                "",
                xy=(0.72, cy),
                xytext=(0.692, cy),
                arrowprops=dict(arrowstyle="->", color=COLOR_RURAL_EDGE, lw=0.9),
            )
            ax.text(
                0.73,
                cy,
                pull,
                ha="left",
                va="center",
                fontsize=8.5,
                family=FONT_LABEL,
                color=COLOR_INK,
            )

    # Caption at bottom, small italic grey. Wrap to ~110 chars so it
    # doesn't run off the page or into the source line.
    if caption:
        cap_wrapped = _wrap_to_width(caption, max_chars=110)
        ax.text(
            0.05,
            0.18,
            cap_wrapped,
            ha="left",
            va="top",
            fontsize=8.5,
            fontstyle="italic",
            family=FONT_LABEL,
            color=COLOR_GREY_MUTED,
            linespacing=1.35,
        )
    # Source credit at bottom right, smaller
    ax.text(
        0.95,
        0.03,
        source,
        ha="right",
        va="bottom",
        fontsize=7,
        family=FONT_LABEL,
        color=COLOR_GREY_MUTED,
    )

    _save_fig(fig, fig_path, facecolor=COLOR_BG, tight=False)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Calgary minimal geographic map


def load_calgary_outline() -> gpd.GeoSeries:
    g = gpd.read_file(PATH_CSDS)
    calg = g[g["CSDNAME"] == "Calgary"].to_crs(CRS_PLOT)
    return calg.geometry


def load_calgary_hybrids_with_fallback() -> dict[str, object]:
    """Return geometries for the three highlighted minority Calgary hybrids.

    Calgary-West-Tsuut'ina has tier C-null in the v7 gpkg (no polygon was
    transcribed from the thumbnail). We fall back to the 2019 Calgary-West
    polygon as a visually-honest approximation of "territory between west
    Calgary and Tsuut'ina Nation", and flag that honestly in the caption
    and design note.
    """
    gmin = gpd.read_file(PATH_MIN_V7).to_crs(CRS_PLOT)
    g19 = gpd.read_file(PATH_2019).to_crs(CRS_PLOT)

    wanted = [
        "Calgary-Nolan Hill-Cochrane",
        "Calgary-De Winton",
        "Calgary-West-Tsuut'ina",
    ]
    out: dict[str, object] = {}
    for name in wanted:
        sub = gmin[gmin["EDName2025"] == name]
        if sub.empty or sub.iloc[0].geometry is None or sub.iloc[0].geometry.is_empty:
            # Proxy fallback
            if name == "Calgary-West-Tsuut'ina":
                proxy = g19[g19["EDName2017"] == "Calgary-West"]
                if not proxy.empty:
                    out[name] = ("proxy_2019", proxy.iloc[0].geometry)
                    continue
            out[name] = None
            continue
        out[name] = ("primary", sub.iloc[0].geometry)
    return out


def draw_calgary(fig_path: Path) -> dict:
    city_geom = load_calgary_outline()
    hybrids = load_calgary_hybrids_with_fallback()

    # Compute the combined bounds so we see Calgary plus the highlighted
    # hybrids (which extend NW / S / W beyond the municipal boundary).
    geoms_for_extent = list(city_geom)
    for v in hybrids.values():
        if v is not None:
            geoms_for_extent.append(v[1])
    extent_union = unary_union(geoms_for_extent)
    minx, miny, maxx, maxy = extent_union.bounds
    # Padding so labels don't clip at the frame
    pad_x = (maxx - minx) * 0.08
    pad_y = (maxy - miny) * 0.12
    minx, maxx = minx - pad_x, maxx + pad_x
    miny, maxy = miny - pad_y, maxy + pad_y

    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN), dpi=FIG_DPI, facecolor=COLOR_BG)

    # Title - size to fit the 0.88 width band
    title = "Calgary: where rural territory enters the city's name"
    title_max_chars_at_18pt = int(0.88 * FIG_W_IN * 72 / (18 * 0.55))
    if len(title) <= title_max_chars_at_18pt:
        title_fs = 18.0
    else:
        title_fs = 16.0
    fig.text(
        0.05,
        0.95,
        title,
        ha="left",
        va="top",
        fontsize=title_fs,
        fontweight="bold",
        family=FONT_TITLE,
        color=COLOR_INK,
    )
    subtitle_wrapped = _wrap_to_width(
        "Three of the minority's Calgary-named hybrids, each pulling rural or reserve territory into a district whose primary population is Calgary.",
        max_chars=95,
    )
    fig.text(
        0.05,
        0.88,
        subtitle_wrapped,
        ha="left",
        va="top",
        fontsize=9.5,
        family=FONT_LABEL,
        color=COLOR_INK_SOFT,
        linespacing=1.35,
    )

    # Map axes - leave more room below for two-line caption
    ax = fig.add_axes((0.05, 0.18, 0.90, 0.64))
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#c8c8c8")
        s.set_linewidth(0.5)
    ax.set_facecolor(COLOR_BG)

    # 1. Light-grey city outline (municipal boundary, no interior ED lines)
    gpd.GeoSeries(city_geom, crs=CRS_PLOT).plot(
        ax=ax,
        facecolor="#ececec",
        edgecolor="#9a9a9a",
        linewidth=1.0,
        zorder=2,
    )

    # 2. Highlighted minority hybrids - solid fills
    hybrid_colors = {
        "Calgary-Nolan Hill-Cochrane": MINORITY_SEGMENT_COLORS[0],  # teal
        "Calgary-De Winton": MINORITY_SEGMENT_COLORS[1],  # lighter teal
        "Calgary-West-Tsuut'ina": MINORITY_SEGMENT_COLORS[2],  # deep slate
    }
    proxy_notes: list[str] = []
    highlight_geoms: dict[str, object] = {}
    for name, entry in hybrids.items():
        if entry is None:
            continue
        source, geom = entry
        if source == "proxy_2019":
            proxy_notes.append(name)
        color = hybrid_colors[name]
        gpd.GeoSeries([geom], crs=CRS_PLOT).plot(
            ax=ax,
            facecolor=color,
            edgecolor="#111111",
            linewidth=0.84,
            alpha=0.85,
            zorder=4,
        )
        highlight_geoms[name] = geom

    # 3. Label the three highlighted districts with leader lines to white
    # boxes. Positions chosen to avoid overlapping the CALGARY label and
    # each other. We target the centroid of the non-Calgary portion of
    # each hybrid (i.e., the rural tail) so the leader line points at
    # the rural part of the district, not the Calgary part.
    calgary_poly = city_geom.iloc[0]
    label_positions = {
        # name -> (label_x_axes_frac, label_y_axes_frac)
        "Calgary-Nolan Hill-Cochrane": (0.20, 0.93),
        "Calgary-West-Tsuut'ina": (0.05, 0.22),
        "Calgary-De Winton": (0.78, 0.06),
    }
    for name, (ax_fx, ax_fy) in label_positions.items():
        if name not in highlight_geoms:
            continue
        geom = highlight_geoms[name]
        # Point the leader at the rural portion: subtract the Calgary
        # outline from the hybrid to isolate the rural tail, then use
        # its representative point. If the difference is empty (hybrid
        # falls entirely outside Calgary), fall back to the raw rep point.
        try:
            rural_only = geom.difference(calgary_poly)
            if rural_only.is_empty:
                rp = geom.representative_point()
            else:
                rp = rural_only.representative_point()
        except Exception as e:
            logger.debug("geometry difference failed, using raw representative_point: %s", e)
            rp = geom.representative_point()
        lx = minx + ax_fx * (maxx - minx)
        ly = miny + ax_fy * (maxy - miny)
        # Draw leader line
        ax.plot(
            [lx, rp.x], [ly, rp.y], color="#111111", linewidth=0.7, zorder=5, alpha=0.75
        )
        # Label box
        ax.annotate(
            name,
            xy=(lx, ly),
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
            family=FONT_LABEL,
            color=COLOR_INK,
            bbox=dict(
                boxstyle="round,pad=0.35", fc="white", ec="#111111", linewidth=0.8
            ),
            zorder=7,
        )

    # 4. "Calgary" label inside the city outline, subtle. Offset slightly
    # from the rep-point centre to avoid any leader line that passes
    # through the municipal polygon.
    cx_rp = calgary_poly.representative_point()
    ax.annotate(
        "CALGARY",
        xy=(cx_rp.x, cx_rp.y),
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        family=FONT_LABEL,
        color="#555555",
        zorder=3,
        bbox=dict(boxstyle="round,pad=0.3", fc=(1, 1, 1, 0.6), ec="none"),
    )

    # 5. Scale bar - 10 km
    span_x = maxx - minx
    span_y = maxy - miny
    sb_x = minx + span_x * 0.04
    sb_y = miny + span_y * 0.05
    sb_len = 10000  # 10 km in metres
    ax.add_patch(
        Rectangle(
            (sb_x, sb_y),
            sb_len,
            span_y * 0.012,
            facecolor="#111111",
            edgecolor="#111111",
            zorder=7,
        )
    )
    ax.text(
        sb_x + sb_len / 2,
        sb_y + span_y * 0.028,
        "10 km",
        ha="center",
        va="bottom",
        fontsize=7.5,
        family=FONT_LABEL,
        color="#111111",
        zorder=7,
    )

    # 6. Compass rose - top-right corner of the map
    nx = minx + span_x * 0.93
    ny = maxy - span_y * 0.10
    ax.annotate(
        "N",
        xy=(nx, ny + span_y * 0.045),
        xytext=(nx, ny - span_y * 0.045),
        arrowprops=dict(
            facecolor="#111111",
            width=1.4,
            headwidth=6,
            headlength=7,
            edgecolor="#111111",
        ),
        ha="center",
        va="bottom",
        fontsize=8.5,
        fontweight="bold",
        family=FONT_LABEL,
        color="#111111",
        zorder=7,
    )

    # Caption - wrapped, italic, grey. Positioned below the map.
    caption_main = _wrap_to_width(
        "Calgary, with three of the minority's Calgary-named hybrids highlighted. "
        "Each pulls rural or reserve territory into a district whose primary population is Calgary. "
        "The majority map does not draw any of these three.",
        max_chars=110,
    )
    fig.text(
        0.05,
        0.14,
        caption_main,
        ha="left",
        va="top",
        fontsize=8.5,
        fontstyle="italic",
        family=FONT_LABEL,
        color=COLOR_GREY_MUTED,
        linespacing=1.35,
    )
    # Honest caveat if a proxy geometry was used
    if proxy_notes:
        proxied = ", ".join(proxy_notes)
        fig.text(
            0.05,
            0.03,
            f"Caveat: {proxied} has no transcribed 2026 polygon yet; the 2019 Calgary-West shape stands in as a visual approximation.",
            ha="left",
            va="bottom",
            fontsize=7,
            family=FONT_LABEL,
            color=COLOR_GREY_MUTED,
        )

    _save_fig(fig, fig_path, facecolor=COLOR_BG, tight=False)
    plt.close(fig)
    return {"proxy_notes": proxy_notes}


# ---------------------------------------------------------------------------
# Figure specs


def build_airdrie():
    """How each map divides Airdrie's people, drawn to scale.

    Rebuilt 2026-11-01 (DOCUMENTED CORRECTIONS C45). The earlier version drew
    four equal minority segments ("one per compass direction ... each attached
    to a different surrounding district"), which read as four equal quarters
    of the city. Counted by people, the minority's Airdrie East holds 54.7% of
    the city and is 89.6% Airdrie; Calgary-Airdrie (24.0%) and
    Calgary-Foothills-Airdrie West (20.9%) are Calgary-majority; and
    Olds-Three Hills-Didsbury takes about 350 people, by area-sharing of cut
    census areas only. (The four districts by land area are in the 2026-07-08
    note this replaces: Airdrie East 35.5 km^2 of the city, Olds-Three
    Hills-Didsbury 23.2, Calgary-Airdrie 15.8, Calgary-Foothills-Airdrie West
    11.2.) Segment widths and every number drawn are read from
    data/outputs/airdrie_split_shares_2026-10-31.json
    (analysis/scripts/airdrie_split_shares.py), so the picture cannot drift
    from the counts.
    """
    import json

    shares = json.loads(
        (DATA / "outputs" / "airdrie_split_shares_2026-10-31.json").read_text(encoding="utf-8")
    )
    total = shares["airdrie_2021_census_csd"]
    words = {1: "one", 2: "two", 3: "three", 4: "four"}

    def rows(map_key):
        return {d["district"]: d for d in shares["maps"][map_key]["districts"]}

    maj, mino = rows("majority"), rows("minority")

    def pct(x):
        return f"{x * 100:.1f}%"

    def seg(map_rows, district, label, color):
        d = map_rows[district]
        held = d["share_of_airdrie_held"]
        if held < 0.02:
            # Below the audit's 2% piece rule: give people, not a percentage.
            sub = f"about {int(round(d['airdrie_residents'], -1)):,} people"
        else:
            sub = (f"{pct(held)} of the city\n"
                   f"district {d['share_of_district_airdrie'] * 100:.0f}% Airdrie")
        return Segment(label, color, sublabel=sub, proportion=held)

    # West to east within each bar.
    maj_segments = [
        seg(maj, "Airdrie-West", "Airdrie-West", MAJORITY_SEGMENT_COLORS[1]),
        seg(maj, "Airdrie-East", "Airdrie-East", MAJORITY_SEGMENT_COLORS[0]),
    ]
    # The official boundary file spells the minority's division
    # "Airdrie-East"; the minority report's table and the site write
    # "Airdrie East".
    min_segments = [
        seg(mino, "Calgary-Foothills-Airdrie West", "Calgary-Foothills-Airdrie West",
            MINORITY_SEGMENT_COLORS[1]),
        seg(mino, "Calgary-Airdrie", "Calgary-Airdrie", MINORITY_SEGMENT_COLORS[3]),
        seg(mino, "Airdrie-East", "Airdrie East", MINORITY_SEGMENT_COLORS[0]),
        seg(mino, "Olds-Three Hills-Didsbury", "Olds-Three Hills-Didsbury",
            MINORITY_SEGMENT_COLORS[2]),
    ]
    m_maj, m_min = shares["maps"]["majority"], shares["maps"]["minority"]
    n_maj_home = len(m_maj["districts_where_airdrie_is_a_majority"])
    n_min_home = len(m_min["districts_where_airdrie_is_a_majority"])
    ae = mino["Airdrie-East"]
    calgary_held = (mino["Calgary-Airdrie"]["share_of_airdrie_held"]
                    + mino["Calgary-Foothills-Airdrie West"]["share_of_airdrie_held"])

    title = "Airdrie: how each map divides the city"
    subtitle = (
        f"Bar widths are shares of Airdrie's {total:,} residents at the 2021 census "
        "(the city counted 85,805 in its 2024 municipal census). "
        f"The majority gives the city {words[n_maj_home]} divisions where most people "
        f"are from Airdrie; the minority gives it {words[n_min_home]}."
    )
    caption = (
        f"The minority's Airdrie East holds {pct(ae['share_of_airdrie_held'])} of the city and is "
        f"{pct(ae['share_of_district_airdrie'])} Airdrie. Calgary-Airdrie and "
        f"Calgary-Foothills-Airdrie West hold {calgary_held * 100:.0f}% between them; in both, "
        "Calgary residents outnumber Airdrie's. Counting only pieces with at least 2% of the "
        f"city's people, the split is {words[m_min['districts_holding_2pct_or_more']]} pieces "
        f"to {words[m_maj['districts_holding_2pct_or_more']]}."
    )
    draw_schematic(
        OUT / "figure_airdrie_v3.svg",
        title=title,
        subtitle=subtitle,
        maj_label="Majority proposal  \u00b7  2 divisions, both mostly Airdrie",
        maj_segments=maj_segments,
        min_label=(f"Minority proposal  \u00b7  {m_min['districts_with_any_airdrie_residents']} "
                   f"districts, {words[n_min_home]} of them mostly Airdrie"),
        min_segments=min_segments,
        caption=caption,
        source="Source: 2021 census areas over Elections Alberta's official 2026 boundaries "
               "(analysis/scripts/airdrie_split_shares.py).",
    )


def build_lethbridge():
    title = "Lethbridge: two plans, two stories"
    subtitle = (
        "Population ~105,000. The majority draws two compact city ridings. "
        "The minority draws three Lethbridge-prefixed hybrids, each pulling rural territory."
    )
    maj_segments = [
        Segment("Lethbridge-East", MAJORITY_SEGMENT_COLORS[0], proportion=1.0),
        Segment("Lethbridge-West", MAJORITY_SEGMENT_COLORS[1], proportion=1.0),
    ]
    min_segments = [
        Segment(
            "Lethbridge-Cardston",
            MINORITY_SEGMENT_COLORS[0],
            sublabel="core + rural",
            proportion=1.0,
        ),
        # Label abbreviated to fit the segment at magazine column width;
        # the full name "Lethbridge-Fort MacLeod-Crowsnest Pass" is
        # recorded in the design note and in the inset callout.
        Segment(
            "Lethbridge-Fort MacLeod",
            MINORITY_SEGMENT_COLORS[1],
            sublabel="+ Crowsnest Pass",
            proportion=1.3,
        ),
        Segment(
            "Lethbridge-Little Bow",
            MINORITY_SEGMENT_COLORS[2],
            sublabel="core + rural",
            proportion=1.0,
        ),
    ]
    inset = [
        ("Lethbridge-Cardston", "Cardston"),
        ("Fort MacLeod-Crowsnest Pass", "Fort MacLeod"),
        ("Lethbridge-Little Bow", "Lomond"),
    ]
    caption = (
        "Each of the minority's three Lethbridge-prefixed districts attaches a rural community to the city core. "
        "The majority draws two compact Lethbridge ridings and keeps rural territory in separately-named regional districts."
    )
    draw_schematic(
        OUT / "figure_lethbridge_v3.svg",
        title=title,
        subtitle=subtitle,
        maj_label="Majority proposal  \u00b7  2 compact city ridings",
        maj_segments=maj_segments,
        min_label="Minority proposal  \u00b7  3 Lethbridge-prefixed hybrids",
        min_segments=min_segments,
        inset_callouts=inset,
        caption=caption,
    )


def build_reddeer():
    title = "Red Deer: the four-way carve"
    subtitle = (
        "Population ~106,000. The majority draws two compact city ridings plus two rural. "
        "The minority draws four Red Deer-prefixed hybrids."
    )
    maj_segments = [
        Segment(
            "Red Deer-North",
            MAJORITY_SEGMENT_COLORS[0],
            sublabel="compact city",
            proportion=1.0,
        ),
        Segment(
            "Red Deer-South",
            MAJORITY_SEGMENT_COLORS[1],
            sublabel="compact city",
            proportion=1.0,
        ),
        Segment(
            "Lacombe-Clearwater",
            COLOR_RURAL,
            sublabel="rural",
            proportion=1.0,
            is_rural_carve=True,
        ),
        Segment(
            "Sylvan Lake-Innisfail",
            COLOR_RURAL,
            sublabel="rural",
            proportion=1.0,
            is_rural_carve=True,
        ),
    ]
    min_segments = [
        Segment(
            "Red Deer-Blackfalds",
            MINORITY_SEGMENT_COLORS[0],
            sublabel="city + town",
            proportion=1.0,
        ),
        Segment(
            "Red Deer-Innisfail",
            MINORITY_SEGMENT_COLORS[1],
            sublabel="city + town",
            proportion=1.0,
        ),
        Segment(
            "Red Deer-Lacombe",
            MINORITY_SEGMENT_COLORS[2],
            sublabel="city + town",
            proportion=1.0,
        ),
        Segment(
            "Red Deer-Sylvan Lake",
            MINORITY_SEGMENT_COLORS[3],
            sublabel="city + town",
            proportion=1.0,
        ),
    ]
    caption = (
        "The minority attaches a Red Deer prefix to every adjacent rural riding. "
        "Same footprint; four city-named districts where the majority drew two."
    )
    draw_schematic(
        OUT / "figure_reddeer_v3.svg",
        title=title,
        subtitle=subtitle,
        maj_label="Majority proposal  \u00b7  2 compact city ridings plus 2 rural",
        maj_segments=maj_segments,
        min_label="Minority proposal  \u00b7  4 Red Deer-prefixed hybrids",
        min_segments=min_segments,
        caption=caption,
    )


def build_calgary():
    return draw_calgary(OUT / "figure_calgary_v3.svg")


# ---------------------------------------------------------------------------


def main() -> int:
    print("Fonts selected:")
    print(f"  title: {FONT_TITLE}")
    print(f"  label: {FONT_LABEL}")
    print()
    print("Rendering schematics...")
    build_airdrie()
    print("  -> figure_airdrie_v3.svg")
    build_lethbridge()
    print("  -> figure_lethbridge_v3.svg")
    build_reddeer()
    print("  -> figure_reddeer_v3.svg")
    print()
    print("Rendering Calgary minimal map...")
    calg_meta = build_calgary()
    print("  -> figure_calgary_v3.svg")
    if calg_meta.get("proxy_notes"):
        print(f"  proxy notes: {calg_meta['proxy_notes']}")
    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
