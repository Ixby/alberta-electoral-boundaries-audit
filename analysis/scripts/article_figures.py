# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
article_figures.py

Generate the inline figures the magazine article embeds:

  1. lane1_dotplot.svg    — Lane 1 EG histogram: 1,010,000-plan canonical
     neutral-ensemble maps shown as bars, right tail (p90+) shaded in red.
     Vertical lines for Minority 2026 (+3.96-4.02%, p94.54), Majority 2026
     (+0.04-0.10%, p16.52), and 2019 enacted (+2.41%, p69.5). p95 reference
     line dashed. Values read live from the canonical ensemble CSVs (see
     code below) — this docstring is descriptive only and is not the
     source of truth; if it drifts from the canonical files, trust the code.
  2. lane2_bars.svg       — Lane 2 horizontal bar chart of structural
     irregularities, one row per test, magnitude relative to comparator
     norm; majority + minority side by side; norm band shaded.
  3. stakes_quadrant.svg — 2×2 quadrant: x-axis "Lane 1 (numbers, EG)";
     y-axis "Lane 2 (structural-irregularity count)"; three dots
     (2019 enacted, Majority 2026, Minority 2026) labelled.

All figures saved at 300 DPI to data/maps/article/ for inclusion in
report_public.md via standard ![](data/maps/article/...) markdown.
Style is editorial-print: muted palette, oldstyle numerals via Source
Sans 3 fallback, ~5×3in print sizing for body inclusion.

Run:
    PYTHONIOENCODING=utf-8 python alberta_audit/analysis/scripts/article_figures.py

Forward:  report_public.md (consumes the PNGs)
Backward: stdlib + matplotlib + numpy
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = data_loader._resolve_path("data") / "maps" / "article"
OUT.mkdir(parents=True, exist_ok=True)

# Editorial palette — source of truth is palette.py; do not redeclare here
from palette import (
    MINORITY_PURPLE, MINORITY_PURPLE_LIGHT,
    MAJORITY_TEAL, MAJORITY_TEAL_LIGHT,
    NDP_ORANGE, UCP_BLUE,
    NEUTRAL_2019, RULE_GREY, TEXT_DARK, THRESHOLD_RED, NORM_BAND,
    PAPER_BG, INK_TEXT, INK_MUTED, INK_SUBTLE, save_fig,
)

# matplotlib defaults — match the SITE's typography and surfaces, not print.
# Text is laid out in Arial (metrically close to the site's Segoe UI) and
# saved as live text (svg.fonttype='none'); palette.save_fig() then rewrites
# the family names to the viewer's full font stacks so the browser renders
# figure text in the page's own faces. Backgrounds use the site's warm paper.
plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        "font.size": 9.5,
        "axes.titlesize": 10.5,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "text.color": INK_TEXT,
        "axes.labelcolor": INK_MUTED,
        "xtick.color": INK_SUBTLE,
        "ytick.color": INK_SUBTLE,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.5,
        "axes.edgecolor": INK_MUTED,
        "axes.facecolor": "none",
        "figure.facecolor": PAPER_BG,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
    }
)


def build_lane1_dotplot() -> Path:
    """Lane 1 EG histogram — 250k neutral-ensemble maps with real-map lines overlaid."""
    import pandas as _pd
    import matplotlib.transforms as _mtrans
    from matplotlib.colors import to_rgba

    samples_path = ROOT / "data" / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"
    eg_pct = _pd.read_csv(samples_path, usecols=["efficiency_gap"])["efficiency_gap"].values * 100

    # Read live from simulated_ensemble_percentiles_canonical.csv rather than
    # hardcoding — this block previously hardcoded both the EG values and
    # their percentiles as literals; the percentiles had already drifted
    # (found 2026-07-12) from a prior ensemble run while the raw EG values
    # happened to still be correct, which is exactly how this kind of bug
    # goes unnoticed.
    pct_path = ROOT / "data" / "outputs" / "simulated_ensemble_percentiles_canonical.csv"
    pct_df = _pd.read_csv(pct_path)
    eg_pct_df = pct_df[pct_df["metric"] == "efficiency_gap"].set_index("map")
    minority_row = eg_pct_df.loc["minority 2026 canonical"]
    majority_row = eg_pct_df.loc["majority 2026 canonical"]
    enacted_row = eg_pct_df.loc["2019 enacted"]
    minority_eg = minority_row["value"] * 100
    majority_eg = majority_row["value"] * 100
    enacted_eg = enacted_row["value"] * 100
    minority_pctile = minority_row["percentile"]
    majority_pctile = majority_row["percentile"]
    enacted_pctile = enacted_row["percentile"]
    p95_val = minority_row["ensemble_p95"] * 100

    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=300)

    counts, edges = np.histogram(eg_pct, bins=80)
    centers = (edges[:-1] + edges[1:]) / 2
    widths  = edges[1:]  - edges[:-1]

    # Shade only the region past the p95 outlier line, so the shading and the
    # dashed line tell one story (pre-2026-07-08 the shading began at p90 while
    # the line sat at p95 — two unexplained boundaries).
    bar_colors = [
        to_rgba(THRESHOLD_RED, 0.28) if c >= p95_val else to_rgba(RULE_GREY, 0.55)
        for c in centers
    ]
    ax.bar(centers, counts, width=widths, color=bar_colors, linewidth=0)

    # Blended transform: x in data coords, y in axes fraction (0=bottom, 1=top)
    bx = _mtrans.blended_transform_factory(ax.transData, ax.transAxes)

    # p95 dashed reference line — plain-language label (readability pass 2026-07-08:
    # percentile codes like "p95" replaced with words on all public figures)
    ax.axvline(p95_val, color=THRESHOLD_RED, lw=1.0, linestyle="--", zorder=2)
    ax.text(p95_val + 0.40, 0.66, f"outlier line ~{p95_val:.1f}%\n(gerrymander threshold —\nonly 1 in 20 neutral maps\nlands past this)",
            color=THRESHOLD_RED, fontsize=6.5, fontweight="bold",
            ha="left", va="top", transform=bx)

    # Real-map vertical lines
    ax.axvline(minority_eg, color=MINORITY_PURPLE, lw=2.0, zorder=5)
    ax.axvline(majority_eg, color=MAJORITY_TEAL,   lw=2.0, zorder=5)
    ax.axvline(enacted_eg,  color=NEUTRAL_2019,    lw=1.3, linestyle="--", zorder=4)

    # Label placement (readability pass): majority label over the empty NDP side,
    # 2019 label centred on its own line, minority label in the empty region right
    # of the purple line and ABOVE the outlier-line text (which starts at y=0.66).
    ax.text(majority_eg - 0.18, 0.97, f"Majority 2026: {majority_eg:+.1f}%\nwell inside the\nnormal range",
            color=MAJORITY_TEAL, fontsize=6.5, fontweight="bold",
            ha="right", va="top", transform=bx)
    ax.text(enacted_eg, 0.97, f"2019 map (current):\n{enacted_eg:+.1f}%, inside the\nnormal range",
            color=NEUTRAL_2019, fontsize=6.5, fontweight="bold",
            ha="center", va="top", transform=bx)
    ax.text(minority_eg + 0.40, 0.97,
            f"Minority 2026: {minority_eg:+.1f}%\nmore UCP-tilted than\n{minority_pctile:.0f}% of neutral maps",
            color=MINORITY_PURPLE, fontsize=6.5, fontweight="bold",
            ha="left", va="top", transform=bx)

    # Directional labels at top corners
    # Mathtext arrows: the literal ←/→ glyphs are absent from Georgia (the font
    # matplotlib resolves from the serif stack on Windows) and rendered as tofu
    # boxes in the published SVG/PNG until 2026-07-08. Placed at the BOTTOM
    # corners (2026-07-08 readability pass) so they sit beside the orange/blue
    # direction strips on the x-axis they explain, and clear of the map labels.
    # Live-text SVGs let the browser supply the arrow glyphs (Segoe UI has
    # them); the old mathtext workaround for Georgia's missing arrows is gone.
    ax.text(0.02, 0.05, "← tilts NDP",
            color=NDP_ORANGE, fontsize=7, fontweight="bold",
            ha="left", va="bottom", transform=ax.transAxes)
    ax.text(0.98, 0.05, "tilts UCP →",
            color=UCP_BLUE, fontsize=7, fontweight="bold",
            ha="right", va="bottom", transform=ax.transAxes)

    ax.set_xlim(-7, 7)
    ax.set_xlabel("Partisan tilt of the map (efficiency gap)", fontsize=8, color="#444")
    ax.set_ylabel("Number of neutral maps", fontsize=8, color="#444")
    ax.set_xticks([-6, -4, -2, 0, 2, 4, 6])
    ax.set_xticklabels(["-6%", "-4%", "-2%", "0%", "+2%", "+4%", "+6%"])
    # Thousands-abbreviated y ticks: exact bin counts are irrelevant detail for
    # a lay reader; "40k" carries the same shape information with less ink.
    from matplotlib.ticker import FuncFormatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda t, _: f"{int(t/1000)}k" if t else "0"))
    ax.tick_params(axis="both", direction="out", length=3, pad=2)

    # Two-tone x-axis: orange for negative EG (NDP-favoured), blue for positive (UCP-favoured)
    ax.spines["bottom"].set_visible(False)
    _bx = ax.get_xaxis_transform()
    ax.plot([-7, 0], [0, 0], transform=_bx, color=NDP_ORANGE, lw=1.0, clip_on=False, zorder=10)
    ax.plot([0, 7], [0, 0], transform=_bx, color=UCP_BLUE,   lw=1.0, clip_on=False, zorder=10)

    fig.tight_layout(pad=0.4)
    out = OUT / "lane1_dotplot.svg"
    save_fig(fig, out, pad_inches=0.06)
    plt.close(fig)
    return out


def build_lane2_bars() -> Path:
    """Lane 2 structural tests — small-multiples layout.

    Each test gets its own panel with an independent x-axis so that bars
    for different-unit tests (percentage-points, percent, raw counts) are
    never placed on a shared scale that implies false comparison.
    """
    # (label, majority_value, minority_value, threshold_val_or_None,
    #  x_max, x_unit_label)
    #
    # Corrected 2026-07-08. The previous version of this figure carried:
    #   (a) the RETRACTED municipal-anchoring panel (DPG-era 29.0/55.5 pp below
    #       norm; canonical recomputation puts both maps within the 70-85%
    #       Canadian norm — report §5.8.5) — panel removed;
    #   (b) the Zone A-Zone B gap values (0.4/12.2) paired with the +5%
    #       threshold that belongs to the vs-provincial-mean variant; the
    #       vs-mean values are 2.8/11.5 (report §5.3.1 P1,
    #       findings/population_equality.md §A2), and the zone is NE/central
    #       Calgary, not "NW";
    #   (c) a 5-of-5 structural score; with anchoring neutral the summary is
    #       4 of 5 (public report Part IV table; pre-registered outlier
    #       criterion >= 4 of 5);
    #   (d) a "% widening relative to ensemble" unit label on the MAD panel —
    #       the 48% is relative to the majority map (4,707 vs 3,180,
    #       commission population tables).
    #
    # Readability redesign (2026-07-08, dataviz pass): the MAD panel previously
    # plotted the DERIVED ratio (majority 0, minority 48 "% wider") — a zero-length
    # majority bar misreads as "majority has zero population spread." It now plots
    # the actual mean absolute deviations (3,180 vs 4,707 persons, commission
    # population tables) with the 48%-wider note carried in the panel title.
    # Panel titles rewritten in plain language; jargon moved to sublabels.
    # Tuple: (label, majority_value, minority_value, threshold_or_None,
    #         x_max, x_unit_label, value_format)
    tests = [
        (
            "How unevenly people are spread across districts\n(typical distance from the ideal district size; minority is 48% wider)",
            3180,
            4707,
            None,
            5500,
            "people away from the ideal size (smaller is better)",
            "{:,.0f}",
        ),
        (
            "How overcrowded the NE & central Calgary districts are\n(the audit's line is +5% above the provincial average)",
            2.8,
            11.5,
            5,
            16,
            "% above the provincial average district size",
            "{:g}%",
        ),
        (
            "Boundaries the commission's own chair\nflagged as geographically anomalous",
            0,
            3,
            1,
            5,
            "boundaries flagged",
            "{:g}",
        ),
        (
            "Extra pieces the City of Airdrie is cut into\n(every map must use at least 2)",
            0,
            2,
            None,
            3,
            "extra pieces beyond the required 2",
            "{:g}",
        ),
        (
            "The scorecard: tests fired, out of 5\n(the 5th, municipal anchoring, was neutral for both maps)",
            0,
            4,
            4,
            5.5,
            "tests fired (4 of 5 = structural outlier)",
            "{:g}",
        ),
    ]

    n = len(tests)
    fig, axes = plt.subplots(
        n, 1, figsize=(6.4, 7.6), dpi=300, gridspec_kw={"hspace": 1.20}
    )
    fig.patch.set_facecolor(PAPER_BG)

    bar_h = 0.55

    for ax, (label, maj, mino, threshold, xmax, unit, vfmt) in zip(axes, tests):
        ax.set_facecolor(PAPER_BG)
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color("#aaaaaa")
        ax.spines["bottom"].set_linewidth(0.6)

        # Majority bar (y=1, green)
        ax.barh(
            1,
            maj,
            height=bar_h,
            color=MAJORITY_TEAL,
            alpha=0.9,
            edgecolor="none",
            zorder=2,
        )
        # Minority bar (y=0, red)
        ax.barh(
            0,
            mino,
            height=bar_h,
            color=MINORITY_PURPLE,
            alpha=0.9,
            edgecolor="none",
            zorder=2,
        )

        # Threshold line — skip x=0 (would draw on the axis spine)
        if threshold is not None and threshold > 0:
            ax.axvline(threshold, color=THRESHOLD_RED, lw=1.0, linestyle="--", zorder=3)

        # Value annotations — for zero bars use a right-anchored label at a small
        # positive x so the text doesn't stack on the axis spine or the bar edge.
        offset = xmax * 0.025
        maj_x = max(maj, xmax * 0.04) if maj == 0 else maj + offset
        maj_ha = "left"
        ax.text(
            maj_x,
            1,
            vfmt.format(maj),
            va="center",
            ha=maj_ha,
            fontsize=7.5,
            color=TEXT_DARK,
        )
        mino_x = max(mino, xmax * 0.04) if mino == 0 else mino + offset
        ax.text(
            mino_x,
            0,
            vfmt.format(mino),
            va="center",
            ha="left",
            fontsize=7.5,
            color=TEXT_DARK,
            fontweight="bold",
        )

        ax.set_xlim(0, xmax)
        # Counts get integer ticks — a count axis showing "0.5" reads as nonsense
        # to a lay audience (2026-07-08 readability pass).
        if xmax <= 6:
            from matplotlib.ticker import MaxNLocator
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_ylim(-0.5, 1.7)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["Minority", "Majority"], fontsize=7.5, color=TEXT_DARK)
        ax.tick_params(axis="y", length=0, pad=3)
        ax.tick_params(
            axis="x", direction="out", length=3, labelsize=7, colors="#555555"
        )
        ax.set_xlabel(unit, fontsize=7, color="#666666", labelpad=2)
        ax.set_title(
            label,
            fontsize=8.5,
            fontweight="bold",
            color=TEXT_DARK,
            loc="left",
            pad=3,
            linespacing=1.2,
        )

    # Shared legend at top of figure
    legend_elements = [
        mpatches.Patch(facecolor=MAJORITY_TEAL, alpha=0.9, label="Majority 2026"),
        mpatches.Patch(facecolor=MINORITY_PURPLE, alpha=0.9, label="Minority 2026"),
        plt.Line2D(
            [0],
            [0],
            color=THRESHOLD_RED,
            lw=0.9,
            linestyle="--",
            label="Pass/fail threshold",
        ),
    ]
    fig.legend(
        handles=legend_elements,
        loc="upper right",
        fontsize=7.5,
        frameon=False,
        ncol=3,
        bbox_to_anchor=(0.98, 1.01),
        handletextpad=0.4,
        columnspacing=1.0,
    )

    fig.suptitle(
        "How the two maps score on the structural fairness tests",
        fontsize=10,
        fontweight="bold",
        x=0.04,
        ha="left",
        y=1.02,
        color=TEXT_DARK,
    )

    out = OUT / "lane2_bars.svg"
    save_fig(fig, out, pad_inches=0.08)
    plt.close(fig)
    return out


def build_bias_structure_matrix() -> Path:
    """The Map Scorecard — evidence exhibit, not verdict machine.
    Two-axis plot:
      x = Lane 1 efficiency gap (signed %; canonical official EA shapefiles,
          simulation_real_map_scores_canonical.json; reference line from the
          canonical ensemble p95)
      y = Lane 2 structural red-flag count (of the audit's 5 pre-registered checks)
    Three points: 2019 enacted (grey), Majority 2026 (teal), Minority 2026 (purple).

    Honesty redesign (2026-07-09, author direction): the earlier version shaded
    "WARNING"/"DANGER ZONE" quadrants and labelled the reference lines as if
    crossing them yielded a verdict. Canadian law sets no numeric threshold —
    the effective-representation test is holistic — and both reference lines
    are the audit's own calibrations (the 4.1% line is the p95 of this audit's
    neutral simulation; the 4-of-5 bar is this audit's pre-registered battery
    with no external benchmark; the US 7% figure is an academic proposal never
    adopted by any court). The chart now presents positions and calibrations,
    and says on its face what the lines are and are not."""

    fig, ax = plt.subplots(figsize=(7.2, 5.6), dpi=300)
    fig.subplots_adjust(top=0.82, bottom=0.155, left=0.13, right=0.97)

    # Three real maps — canonical official EA shapefiles (simulation_real_map_scores_canonical.json)
    # Corrected 2026-07-08: minority structural count 5 -> 4 (municipal anchoring
    # retracted on canonical geometry — both maps within the 70-85% Canadian norm;
    # report §5.8.5 — so 4 of the 5 pre-registered structural tests fire).
    # Grounding note (2026-07-08): the 2019 enacted map's structural count of 0
    # rests on the tests runnable against it — MAD 2,010 (tighter than both 2026
    # maps; Appendix C), a 2-way Airdrie configuration, and zero chair flags. The
    # Calgary Zone A-Zone B gap was NOT run on 2019 (2019-era per-ED population
    # data absent from the working bundle; findings/population_equality.md §A1).
    points = [
        ("2019 enacted", 2.41, 0, NEUTRAL_2019),
        ("Majority 2026", 0.10, 0, MAJORITY_TEAL),
        ("Minority 2026", 4.02, 4, MINORITY_PURPLE),
    ]

    threshold_eg_alberta = (
        # Corrected 2026-07-08: previously 4.11 citing "0.041086" — the committed
        # simulated_ensemble_percentiles_canonical.csv ensemble_p95 is 0.041004 -> 4.10%.
        4.10
    )
    threshold_eg_us = 7.0
    threshold_struct = 4

    XMIN, XMAX = -7, 7
    YMIN, YMAX = -0.6, 5.7

    # No verdict shading. The earlier WARNING/DANGER ZONE quadrants implied
    # that crossing a line settles the question; the law it would need to
    # settle has no such line.

    # Reference lines — audit calibrations, in neutral grey, labelled as such
    ax.axvline(threshold_eg_alberta, color="#777777", lw=1.1, linestyle="--", zorder=1)
    ax.axvline(threshold_eg_us, color="#aaaaaa", lw=0.9, linestyle=":", zorder=1)
    ax.axhline(threshold_struct, color="#777777", lw=1.1, linestyle="--", zorder=1)

    ax.text(
        threshold_eg_alberta - 0.12, YMAX - 0.18,
        "~4.1%: only 1 in 20 of the audit's\nneutral simulations tilts further\n(an audit calibration — not a legal line)",
        color="#555555", fontsize=7, fontstyle="italic",
        ha="right", va="top",
    )
    ax.text(
        threshold_eg_us - 0.12, YMAX - 1.05,
        "7%: US academic proposal\n(no court has adopted it)",
        color="#999999", fontsize=7, fontstyle="italic",
        ha="right", va="top",
    )
    # 4-of-5 line: the audit's own pre-registered bar — say so on its face
    ax.text(
        XMIN + 0.12, threshold_struct + 0.08,
        "4 of the audit's 5 pre-registered checks\n(the audit's own pre-set bar — no external benchmark exists)",
        color="#555555", fontsize=7, fontstyle="italic",
        ha="left", va="bottom",
    )

    # Plot dots — larger and slightly brighter, with white halo (zorder 3-4, above threshold lines)
    for label, x, y, color in points:
        ax.scatter(x, y, s=320, c="white", edgecolors="white", linewidths=2.5, zorder=3)
        ax.scatter(x, y, s=240, c=color, edgecolors=TEXT_DARK, linewidths=1.4, zorder=4)

    # Dot labels — close to origin, inside the zone the dot sits in
    # Minority 2026 at (4.02, 4.0) — corrected 2026-07-08: annotation previously said
    # "5 of 5" and anchored at y=5.0, contradicting the corrected point data (4 of 5,
    # anchoring neutral).
    ax.annotate(
        "Minority 2026\n+4.0% / 4 of 5",
        xy=(4.02, 4.0), xytext=(2.2, 4.65),
        fontsize=8.5, fontweight="bold", color=MINORITY_PURPLE,
        ha="right", va="top",
        arrowprops=dict(arrowstyle="-", color=MINORITY_PURPLE, lw=0.9,
                        shrinkA=0, shrinkB=7),
        zorder=5,
    )
    # Majority 2026 at (0.10, 0): label slightly above-right, safe zone
    ax.annotate(
        "Majority 2026\n+0.1% / 0 of 5",
        xy=(0.10, 0.0), xytext=(0.5, 1.1),
        fontsize=8.5, fontweight="bold", color=MAJORITY_TEAL,
        ha="left", va="bottom",
        arrowprops=dict(arrowstyle="-", color=MAJORITY_TEAL, lw=0.9,
                        shrinkA=0, shrinkB=7),
        zorder=5,
    )
    # 2019 enacted at (2.41, 0): label slightly above-left, safe zone
    ax.annotate(
        "2019 enacted\n+2.4% / 0 of 5",
        xy=(2.41, 0.0), xytext=(2.8, 1.1),
        fontsize=8.5, fontweight="bold", color=NEUTRAL_2019,
        ha="left", va="bottom",
        arrowprops=dict(arrowstyle="-", color=NEUTRAL_2019, lw=0.9,
                        shrinkA=0, shrinkB=7),
        zorder=5,
    )

    # Axes
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_xlabel(
        "Partisan tilt — the efficiency gap (Lane 1)\nfurther right = the map favours the UCP more",
        fontsize=9.5, color=TEXT_DARK, labelpad=8, linespacing=1.2,
    )
    ax.set_ylabel(
        "Structural red flags, out of 5 tests (Lane 2)\nhigher = more red flags",
        fontsize=9.5, color=TEXT_DARK, labelpad=8, linespacing=1.2,
    )
    ax.set_xticks([-6, -4, -2, 0, 2, 4, 6])
    ax.set_xticklabels(
        ["-6%", "-4%", "-2%", "0%", "+2%", "+4%", "+6%"],
        fontsize=8.5,
    )
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.tick_params(axis="both", direction="out", length=4, pad=3, colors=TEXT_DARK)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#888888")
    ax.spines["left"].set_linewidth(0.7)
    # Two-tone x-axis: orange for negative EG (NDP-favoured), blue for positive (UCP-favoured)
    ax.spines["bottom"].set_visible(False)
    _bx = ax.get_xaxis_transform()
    ax.plot([XMIN, 0], [0, 0], transform=_bx, color=NDP_ORANGE, lw=1.2, clip_on=False, zorder=10)
    ax.plot([0, XMAX], [0, 0], transform=_bx, color=UCP_BLUE,   lw=1.2, clip_on=False, zorder=10)

    ax.set_title(
        "Where the three maps sit on the audit's two lanes",
        fontsize=12.5, fontweight="bold",
        loc="left", color=TEXT_DARK, pad=40,
    )
    # Subtitle: the epistemic status of every line on this chart, on the chart.
    ax.text(
        0.0, 1.03,
        "Dashed lines are this audit's own calibrations. Canadian law sets no numeric threshold —\n"
        "a court weighs evidence like this holistically under the effective-representation test.",
        transform=ax.transAxes, fontsize=8, color="#555555",
        ha="left", va="bottom",
    )

    out = OUT / "bias_structure_matrix.svg"
    save_fig(fig, out, pad_inches=0.10)
    # stakes_quadrant.svg is the article-facing name for this chart
    save_fig(fig, OUT / "stakes_quadrant.svg", pad_inches=0.10)
    plt.close(fig)
    return out


def main() -> int:
    print("[article figures] generating embedded charts...")
    print(f"  output dir: {OUT}")
    p1 = build_lane1_dotplot()
    print(f"  [ok] {p1.relative_to(ROOT)}")
    p2 = build_lane2_bars()
    print(f"  [ok] {p2.relative_to(ROOT)}")
    p3 = build_bias_structure_matrix()
    print(f"  [ok] {p3.relative_to(ROOT)}")
    print("[article figures] done -- embed via standard markdown image syntax")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
