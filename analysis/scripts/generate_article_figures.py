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
  - maps/article/figure_airdrie_v3.png
  - maps/article/figure_lethbridge_v3.png
  - maps/article/figure_reddeer_v3.png
  - maps/article/figure_calgary_v3.png

Run
  PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_generate_article_figures.py

Dependencies
  Forward  : data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg,
             data/shapefiles/reference/alberta_2021_csds.gpkg,
             data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
  Backward : maps/article/figure_*_v3.png,
             analysis/reports/article_figures_v3.md,
             report_public.md (four figure references updated to _v3)

Author: sub-agent, article figure redesign, 2026-04-23
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

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
DATA = ROOT / "data"
OUT = ROOT / "data" / "maps" / "article"
OUT.mkdir(parents=True, exist_ok=True)

PATH_MIN_V7 = DATA / "shapefiles" / "derived" / "v0_10_topological_minority_2026_eds.gpkg"
PATH_CSDS = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
PATH_2019 = DATA / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"

CRS_PLOT = 3401  # NAD83 / Alberta 10-TM Forest, metres

# ---------------------------------------------------------------------------
# Palette & typography
#
# Warm (orange/ochre) for the majority proposal, cool (teal/slate) for the
# minority, neutral ivory for background. Rural carve segments get a
# distinct earthy tone so the reader sees "this slice belongs to something
# that is not the city."

COLOR_BG = "#faf6ee"            # ivory page
COLOR_INK = "#141414"           # near-black
COLOR_INK_SOFT = "#3a3a3a"      # body
COLOR_GREY_MUTED = "#8a8a8a"    # credit line

# Majority = warm orange family (segments distinct but related)
MAJORITY_SEGMENT_COLORS = (
    "#e07a1c",  # saturated orange
    "#f2a14e",  # softer tangerine
    "#c95a0c",  # deeper burnt orange
    "#f5c38a",  # pale ochre
)
# Minority = cool teal/slate family (segments distinct but related)
MINORITY_SEGMENT_COLORS = (
    "#2f6b7a",  # teal
    "#4d92a3",  # lighter teal
    "#254a5a",  # deep slate
    "#79b1bc",  # pale teal
)
# Rural-carve colour for segments whose primary population is outside the
# city - visually distinct from both palette families.
COLOR_RURAL = "#8b5a2b"         # muted umber
COLOR_RURAL_EDGE = "#5a3a1c"

# Fonts. Per spec: Playfair Display bold for titles, Source Sans 3 for
# labels; fall through to Georgia + Arial if the editorial fonts aren't
# installed. On Windows both Georgia and Arial are present, so we don't
# emit the matplotlib font-fallback warning.
from matplotlib import font_manager as _fm
_INSTALLED = {f.name for f in _fm.fontManager.ttflist}
FONT_TITLE = "Playfair Display" if "Playfair Display" in _INSTALLED else "Georgia"
FONT_LABEL = (
    "Source Sans 3" if "Source Sans 3" in _INSTALLED
    else ("Source Sans Pro" if "Source Sans Pro" in _INSTALLED else "Arial")
)

# Canvas geometry - magazine page width. Per spec ~2000x1350 px (7" at 300
# dpi). We use 7.0 x 4.67 for a clean 3:2 aspect.
FIG_DPI = 300
FIG_W_IN = 7.0             # 2100 px at 300 dpi
FIG_H_IN = 4.67            # 1401 px at 300 dpi - ~3:2 aspect


# ---------------------------------------------------------------------------
# Schematic bar helpers

@dataclass
class Segment:
    label: str
    color: str
    sublabel: str = ""
    is_rural_carve: bool = False
    proportion: float = 1.0  # relative weight (bar width share)


def draw_bar(ax, y_top: float, y_bot: float, segments: list[Segment],
             x_left: float = 0.05, x_right: float = 0.95,
             fig_width_in: float = FIG_W_IN) -> None:
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
        rect = FancyBboxPatch(
            (x, y_bot),
            w, y_top - y_bot,
            boxstyle="round,pad=0.0,rounding_size=0.006",
            facecolor=seg.color,
            edgecolor=COLOR_INK,
            linewidth=1.1,
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

        if two_line_result is not None and (single_fs is None or two_line_result[1] > single_fs):
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

        # Flip main label to light on dark segments for contrast
        try:
            import matplotlib.colors as mc
            r, g, b = mc.to_rgb(seg.color)
            luma = 0.299 * r + 0.587 * g + 0.114 * b
        except Exception:
            luma = 1.0
        label_color = "#ffffff" if luma < 0.45 else COLOR_INK
        ax.text(
            x + w / 2, y_label, label_text,
            ha="center", va="center",
            fontsize=best_fs, fontweight="bold",
            family=FONT_LABEL,
            color=label_color,
            zorder=5,
            linespacing=1.0,
        )
        if seg.sublabel:
            # Shrink sublabel for narrow segments. Two-line labels
            # already consume most of the vertical space, so shrink the
            # sublabel further in that case.
            sub_fs = max(best_fs - 2.8, 6.2)
            if n_label_lines >= 2:
                sub_fs = max(sub_fs - 0.8, 5.8)
            sub_w_in = len(seg.sublabel) * sub_fs * 0.52 / 72.0
            if sub_w_in > seg_width_in - 0.05:
                sub_fs = max(sub_fs - 1.0, 5.5)
            # On dark segments, the near-black sublabel becomes illegible.
            # Compute segment brightness (simple luma) and flip to a pale
            # colour when the fill is dark.
            try:
                import matplotlib.colors as mc
                r, g, b = mc.to_rgb(seg.color)
                luma = 0.299 * r + 0.587 * g + 0.114 * b
            except Exception:
                luma = 1.0
            sublabel_color = "#ece6d4" if luma < 0.45 else COLOR_INK_SOFT
            # Clamp sublabel y so it stays inside the rectangle. The
            # rectangle spans [y_bot, y_top]; keep sublabel baseline at
            # least 0.015 above y_bot.
            sub_y_raw = y_mid - 0.024 * n_label_lines - 0.018
            sub_y = max(sub_y_raw, y_bot + 0.018)
            ax.text(
                x + w / 2, sub_y,
                seg.sublabel,
                ha="center", va="center",
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


def draw_schematic(fig_path: Path, title: str, subtitle: str,
                    maj_label: str, maj_segments: list[Segment],
                    min_label: str, min_segments: list[Segment],
                    inset_callouts: list[tuple[str, str]] | None = None,
                    caption: str = "") -> None:
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
    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN), dpi=FIG_DPI,
                     facecolor=COLOR_BG)
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
        0.05, 0.96, title,
        ha="left", va="top",
        fontsize=title_fs, fontweight="bold",
        family=FONT_TITLE,
        color=COLOR_INK,
    )

    # Subtitle - wrap to ~100 chars so it never exceeds the page width.
    # At fontsize 9.5 pt, ~0.88 * 7.0 * 72 / (9.5 * 0.52) = ~90 chars/line.
    if subtitle:
        sub_wrapped = _wrap_to_width(subtitle, max_chars=95)
        ax.text(
            0.05, 0.86, sub_wrapped,
            ha="left", va="top",
            fontsize=9.5,
            family=FONT_LABEL,
            color=COLOR_INK_SOFT,
            linespacing=1.35,
        )

    # Majority bar header
    ax.text(
        0.05, 0.72, maj_label,
        ha="left", va="bottom",
        fontsize=10.5, fontweight="bold",
        family=FONT_LABEL, color=COLOR_INK,
    )
    draw_bar(ax, y_top=0.70, y_bot=0.55, segments=maj_segments,
             x_left=0.05, x_right=0.95, fig_width_in=FIG_W_IN)

    # Minority bar header
    x_min_right = 0.95 if not inset_callouts else 0.62
    ax.text(
        0.05, 0.43, min_label,
        ha="left", va="bottom",
        fontsize=10.5, fontweight="bold",
        family=FONT_LABEL, color=COLOR_INK,
    )
    draw_bar(ax, y_top=0.41, y_bot=0.26, segments=min_segments,
             x_left=0.05, x_right=x_min_right,
             fig_width_in=FIG_W_IN * (x_min_right - 0.05) / 0.9)

    # Inset callouts on the right: three tiny rural-outline markers with
    # arrows pointing to the rural-community name.
    if inset_callouts:
        ax.text(
            0.67, 0.43, "Rural pulls",
            ha="left", va="bottom",
            fontsize=9.5, fontweight="bold",
            family=FONT_LABEL, color=COLOR_INK,
        )
        step = 0.045
        y0 = 0.39
        for i, (district, pull) in enumerate(inset_callouts):
            cy = y0 - i * step
            mrk = Rectangle((0.67, cy - 0.010), 0.018, 0.018,
                            facecolor=COLOR_RURAL, edgecolor=COLOR_RURAL_EDGE,
                            linewidth=0.8)
            ax.add_patch(mrk)
            ax.annotate(
                "",
                xy=(0.72, cy), xytext=(0.692, cy),
                arrowprops=dict(arrowstyle="->", color=COLOR_RURAL_EDGE,
                                lw=0.9),
            )
            ax.text(
                0.73, cy, pull,
                ha="left", va="center",
                fontsize=8.5,
                family=FONT_LABEL, color=COLOR_INK,
            )

    # Caption at bottom, small italic grey. Wrap to ~110 chars so it
    # doesn't run off the page or into the source line.
    if caption:
        cap_wrapped = _wrap_to_width(caption, max_chars=110)
        ax.text(
            0.05, 0.18, cap_wrapped,
            ha="left", va="top",
            fontsize=8.5, fontstyle="italic",
            family=FONT_LABEL, color=COLOR_GREY_MUTED,
            linespacing=1.35,
        )
    # Source credit at bottom right, smaller
    ax.text(
        0.95, 0.03,
        "Source: commission majority report Appendix A and minority report Appendix E.",
        ha="right", va="bottom",
        fontsize=7, family=FONT_LABEL, color=COLOR_GREY_MUTED,
    )

    fig.savefig(fig_path, dpi=FIG_DPI, facecolor=COLOR_BG)
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
        sub = gmin[gmin["name_2026"] == name]
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

    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN), dpi=FIG_DPI,
                     facecolor=COLOR_BG)

    # Title - size to fit the 0.88 width band
    title = "Calgary: where rural territory enters the city's name"
    title_max_chars_at_18pt = int(0.88 * FIG_W_IN * 72 / (18 * 0.55))
    if len(title) <= title_max_chars_at_18pt:
        title_fs = 18.0
    else:
        title_fs = 16.0
    fig.text(
        0.05, 0.95,
        title,
        ha="left", va="top",
        fontsize=title_fs, fontweight="bold",
        family=FONT_TITLE, color=COLOR_INK,
    )
    subtitle_wrapped = _wrap_to_width(
        "Three of the minority's Calgary-named hybrids, each pulling rural or reserve territory into a district whose primary population is Calgary.",
        max_chars=95,
    )
    fig.text(
        0.05, 0.88,
        subtitle_wrapped,
        ha="left", va="top",
        fontsize=9.5,
        family=FONT_LABEL, color=COLOR_INK_SOFT,
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
        ax=ax, facecolor="#ececec", edgecolor="#9a9a9a",
        linewidth=1.4, zorder=2,
    )

    # 2. Highlighted minority hybrids - solid fills
    hybrid_colors = {
        "Calgary-Nolan Hill-Cochrane": MINORITY_SEGMENT_COLORS[0],   # teal
        "Calgary-De Winton": MINORITY_SEGMENT_COLORS[1],             # lighter teal
        "Calgary-West-Tsuut'ina": MINORITY_SEGMENT_COLORS[2],        # deep slate
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
            ax=ax, facecolor=color, edgecolor="#111111",
            linewidth=1.2, alpha=0.85, zorder=4,
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
        "Calgary-West-Tsuut'ina":       (0.05, 0.22),
        "Calgary-De Winton":            (0.78, 0.06),
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
        except Exception:
            rp = geom.representative_point()
        lx = minx + ax_fx * (maxx - minx)
        ly = miny + ax_fy * (maxy - miny)
        # Draw leader line
        ax.plot([lx, rp.x], [ly, rp.y],
                color="#111111", linewidth=0.7, zorder=5, alpha=0.75)
        # Label box
        ax.annotate(
            name,
            xy=(lx, ly),
            ha="center", va="center",
            fontsize=9, fontweight="bold",
            family=FONT_LABEL, color=COLOR_INK,
            bbox=dict(boxstyle="round,pad=0.35",
                      fc="white", ec="#111111", linewidth=0.8),
            zorder=7,
        )

    # 4. "Calgary" label inside the city outline, subtle. Offset slightly
    # from the rep-point centre to avoid any leader line that passes
    # through the municipal polygon.
    cx_rp = calgary_poly.representative_point()
    ax.annotate(
        "CALGARY",
        xy=(cx_rp.x, cx_rp.y),
        ha="center", va="center",
        fontsize=10, fontweight="bold",
        family=FONT_LABEL, color="#555555",
        zorder=3,
        bbox=dict(boxstyle="round,pad=0.3",
                  fc=(1, 1, 1, 0.6), ec="none"),
    )

    # 5. Scale bar - 10 km
    span_x = maxx - minx
    span_y = maxy - miny
    sb_x = minx + span_x * 0.04
    sb_y = miny + span_y * 0.05
    sb_len = 10000  # 10 km in metres
    ax.add_patch(Rectangle(
        (sb_x, sb_y), sb_len, span_y * 0.012,
        facecolor="#111111", edgecolor="#111111", zorder=7,
    ))
    ax.text(
        sb_x + sb_len / 2, sb_y + span_y * 0.028,
        "10 km",
        ha="center", va="bottom",
        fontsize=7.5, family=FONT_LABEL, color="#111111",
        zorder=7,
    )

    # 6. Compass rose - top-right corner of the map
    nx = minx + span_x * 0.93
    ny = maxy - span_y * 0.10
    ax.annotate(
        "N",
        xy=(nx, ny + span_y * 0.045),
        xytext=(nx, ny - span_y * 0.045),
        arrowprops=dict(facecolor="#111111", width=1.4, headwidth=6,
                         headlength=7, edgecolor="#111111"),
        ha="center", va="bottom",
        fontsize=8.5, fontweight="bold",
        family=FONT_LABEL, color="#111111",
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
        0.05, 0.14, caption_main,
        ha="left", va="top",
        fontsize=8.5, fontstyle="italic",
        family=FONT_LABEL, color=COLOR_GREY_MUTED,
        linespacing=1.35,
    )
    # Honest caveat if a proxy geometry was used
    if proxy_notes:
        proxied = ", ".join(proxy_notes)
        fig.text(
            0.05, 0.03,
            f"Caveat: {proxied} has no transcribed 2026 polygon yet; the 2019 Calgary-West shape stands in as a visual approximation.",
            ha="left", va="bottom",
            fontsize=7, family=FONT_LABEL, color=COLOR_GREY_MUTED,
        )

    fig.savefig(fig_path, dpi=FIG_DPI, facecolor=COLOR_BG)
    plt.close(fig)
    return {"proxy_notes": proxy_notes}


# ---------------------------------------------------------------------------
# Figure specs

def build_airdrie():
    title = "Airdrie: one city, four partitions"
    subtitle = ("Population ~90,000. The majority draws two ridings both named Airdrie. "
                "The minority cuts the city into four pieces \u2014 one per compass direction \u2014 "
                "each attached to a different surrounding district.")
    maj_segments = [
        Segment("Airdrie-East", MAJORITY_SEGMENT_COLORS[0], proportion=1.0),
        Segment("Airdrie-West", MAJORITY_SEGMENT_COLORS[1], proportion=1.0),
    ]
    # Four minority segments, one per quadrant of the city:
    #   south -> Calgary-Airdrie, west -> Calgary-Foothills-Airdrie West,
    #   north -> Calgary-Nolan Hill-Cochrane, east -> Airdrie East
    min_segments = [
        Segment("Calgary-Airdrie", MINORITY_SEGMENT_COLORS[3],
                sublabel="south", proportion=1.0),
        Segment("Airdrie East", MINORITY_SEGMENT_COLORS[0],
                sublabel="east", proportion=1.0),
        Segment("Calgary-Nolan Hill-Cochrane", MINORITY_SEGMENT_COLORS[2],
                sublabel="north", proportion=1.0),
        Segment("Calgary-Foothills-Airdrie West", MINORITY_SEGMENT_COLORS[1],
                sublabel="west", proportion=1.0),
    ]
    caption = ("The minority cuts Airdrie into four pieces, each attached to a different surrounding district. "
               "Only one of the four is named Airdrie alone; the other three carry Calgary or regional names. "
               "The majority draws two compact ridings, both named Airdrie.")
    draw_schematic(
        OUT / "figure_airdrie_v3.png",
        title=title, subtitle=subtitle,
        maj_label="Majority proposal  \u00b7  2 ridings, both named Airdrie",
        maj_segments=maj_segments,
        min_label="Minority proposal  \u00b7  4 segments, only one named Airdrie",
        min_segments=min_segments,
        caption=caption,
    )


def build_lethbridge():
    title = "Lethbridge: two plans, two stories"
    subtitle = ("Population ~105,000. The majority draws two compact city ridings. "
                "The minority draws three Lethbridge-prefixed hybrids, each pulling rural territory.")
    maj_segments = [
        Segment("Lethbridge-East", MAJORITY_SEGMENT_COLORS[0], proportion=1.0),
        Segment("Lethbridge-West", MAJORITY_SEGMENT_COLORS[1], proportion=1.0),
    ]
    min_segments = [
        Segment("Lethbridge-Cardston", MINORITY_SEGMENT_COLORS[0],
                sublabel="core + rural", proportion=1.0),
        # Label abbreviated to fit the segment at magazine column width;
        # the full name "Lethbridge-Fort MacLeod-Crowsnest Pass" is
        # recorded in the design note and in the inset callout.
        Segment("Lethbridge-Fort MacLeod",
                MINORITY_SEGMENT_COLORS[1],
                sublabel="+ Crowsnest Pass", proportion=1.3),
        Segment("Lethbridge-Little Bow", MINORITY_SEGMENT_COLORS[2],
                sublabel="core + rural", proportion=1.0),
    ]
    inset = [
        ("Lethbridge-Cardston", "Cardston"),
        ("Fort MacLeod-Crowsnest Pass", "Fort MacLeod"),
        ("Lethbridge-Little Bow", "Lomond"),
    ]
    caption = ("Each of the minority's three Lethbridge-prefixed districts attaches a rural community to the city core. "
               "The majority draws two compact Lethbridge ridings and keeps rural territory in separately-named regional districts.")
    draw_schematic(
        OUT / "figure_lethbridge_v3.png",
        title=title, subtitle=subtitle,
        maj_label="Majority proposal  \u00b7  2 compact city ridings",
        maj_segments=maj_segments,
        min_label="Minority proposal  \u00b7  3 Lethbridge-prefixed hybrids",
        min_segments=min_segments,
        inset_callouts=inset,
        caption=caption,
    )


def build_reddeer():
    title = "Red Deer: the four-way carve"
    subtitle = ("Population ~106,000. The majority draws two compact city ridings plus two rural. "
                "The minority draws four Red Deer-prefixed hybrids.")
    maj_segments = [
        Segment("Red Deer-North", MAJORITY_SEGMENT_COLORS[0],
                sublabel="compact city", proportion=1.0),
        Segment("Red Deer-South", MAJORITY_SEGMENT_COLORS[1],
                sublabel="compact city", proportion=1.0),
        Segment("Lacombe-Clearwater", COLOR_RURAL,
                sublabel="rural", proportion=1.0, is_rural_carve=True),
        Segment("Sylvan Lake-Innisfail", COLOR_RURAL,
                sublabel="rural", proportion=1.0, is_rural_carve=True),
    ]
    min_segments = [
        Segment("Red Deer-Blackfalds", MINORITY_SEGMENT_COLORS[0],
                sublabel="city + town", proportion=1.0),
        Segment("Red Deer-Innisfail", MINORITY_SEGMENT_COLORS[1],
                sublabel="city + town", proportion=1.0),
        Segment("Red Deer-Lacombe", MINORITY_SEGMENT_COLORS[2],
                sublabel="city + town", proportion=1.0),
        Segment("Red Deer-Sylvan Lake", MINORITY_SEGMENT_COLORS[3],
                sublabel="city + town", proportion=1.0),
    ]
    caption = ("The minority attaches a Red Deer prefix to every adjacent rural riding. "
               "Same footprint; four city-named districts where the majority drew two.")
    draw_schematic(
        OUT / "figure_reddeer_v3.png",
        title=title, subtitle=subtitle,
        maj_label="Majority proposal  \u00b7  2 compact city ridings plus 2 rural",
        maj_segments=maj_segments,
        min_label="Minority proposal  \u00b7  4 Red Deer-prefixed hybrids",
        min_segments=min_segments,
        caption=caption,
    )


def build_calgary():
    return draw_calgary(OUT / "figure_calgary_v3.png")


# ---------------------------------------------------------------------------

def main() -> int:
    print("Fonts selected:")
    print(f"  title: {FONT_TITLE}")
    print(f"  label: {FONT_LABEL}")
    print()
    print("Rendering schematics...")
    build_airdrie()
    print("  -> figure_airdrie_v3.png")
    build_lethbridge()
    print("  -> figure_lethbridge_v3.png")
    build_reddeer()
    print("  -> figure_reddeer_v3.png")
    print()
    print("Rendering Calgary minimal map...")
    calg_meta = build_calgary()
    print("  -> figure_calgary_v3.png")
    if calg_meta.get("proxy_notes"):
        print(f"  proxy notes: {calg_meta['proxy_notes']}")
    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
