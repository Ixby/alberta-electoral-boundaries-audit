"""
v0_1_article_figures.py

Generate the inline figures the magazine article embeds:

  1. lane1_dotplot.svg    — Lane 1 EG before/after dot plot. Four dots:
     Majority partial (-1.29%), Majority full (+6.43%), Minority partial
     (-2.71%), Minority full (+9.21%), arrows showing the partial→full
     shift, vertical line at the ensemble p95 (4.37%).
  2. lane2_bars.svg       — Lane 2 horizontal bar chart of structural
     irregularities, one row per test, magnitude relative to comparator
     norm; majority + minority side by side; norm band shaded.
  3. verdict_quadrant.svg — 2×2 quadrant: x-axis "Lane 1 (numbers, EG)";
     y-axis "Lane 2 (structural-irregularity count)"; three dots
     (2019 enacted, Majority 2026, Minority 2026) labelled.

All figures saved at 300 DPI to data/maps/article/ for inclusion in
report_public.md via standard ![](data/maps/article/...) markdown.
Style is editorial-print: muted palette, oldstyle numerals via Source
Sans 3 fallback, ~5×3in print sizing for body inclusion.

Run:
    PYTHONIOENCODING=utf-8 python alberta_audit/analysis/scripts/v0_1_article_figures.py

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

# Editorial palette
NDP_ORANGE = "#ea7414"
UCP_BLUE = "#225d9e"
MAJORITY_PURPLE = "#7a4d8a"
MINORITY_GREEN = "#4a8a5c"
NEUTRAL_2019 = "#666666"
RULE_GREY = "#888888"
TEXT_DARK = "#1a1a1a"
THRESHOLD_RED = "#7b2d3e"
NORM_BAND_GREEN = "#cfe5d0"

# matplotlib defaults — try to match the article's print typography
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Lora", "Source Serif 4", "Georgia", "DejaVu Serif"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.5,
        "axes.edgecolor": "#444",
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
    }
)


def build_lane1_dotplot() -> Path:
    """Lane 1 EG dot plot — v0_9 substrate values against two reference
    lines: the audit's Alberta-calibrated p95 (~4%) and the US 7% line."""
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=300)

    # v0_9 topological substrate canonical values (final_real_map_scores.json)
    alberta_line = 4.03  # ensemble p95 from simulated_ensemble_percentiles_250k.csv
    us_line = 7.00
    rows = [
        ("Majority 2026", 1.44, MAJORITY_PURPLE),
        ("Minority 2026", 1.75, MINORITY_GREEN),
    ]

    y_positions = [1, 0]
    for (label, full, color), y in zip(rows, y_positions):
        ax.plot(
            full,
            y,
            "o",
            markersize=12,
            color=color,
            markeredgecolor=TEXT_DARK,
            markeredgewidth=0.6,
            zorder=4,
        )
        ax.text(
            -4.5,
            y,
            label,
            ha="left",
            va="center",
            fontsize=9,
            color=TEXT_DARK,
            fontweight="bold",
        )
        ax.text(
            full,
            y - 0.32,
            f"{full:+.2f}%",
            ha="center",
            va="top",
            fontsize=8,
            color=TEXT_DARK,
            fontweight="bold",
        )

    # Alberta-calibrated threshold line (ensemble p95)
    ax.axvline(alberta_line, color=THRESHOLD_RED, lw=1.0, linestyle="--", zorder=1)
    ax.text(
        alberta_line + 0.15,
        1.85,
        "Alberta line\n~4%",
        color=THRESHOLD_RED,
        fontsize=7,
        fontweight="bold",
        ha="left",
        va="top",
        linespacing=1.0,
    )

    # US 7% line (Whitford v. Gill literature reference)
    ax.axvline(us_line, color="#888888", lw=0.9, linestyle=":", zorder=1)
    ax.text(
        us_line + 0.15,
        1.85,
        "US line\n7%",
        color="#666666",
        fontsize=7,
        fontweight="bold",
        ha="left",
        va="top",
        linespacing=1.0,
    )

    # Zero line for reference
    ax.axvline(0, color="#cccccc", lw=0.5, zorder=0)

    # Tail labels
    ax.text(
        -4.8,
        1.85,
        "<- NDP-favoured",
        color=NDP_ORANGE,
        fontsize=7,
        fontweight="bold",
        ha="left",
        va="top",
    )
    ax.text(
        9.5,
        1.85,
        "UCP-favoured ->",
        color=UCP_BLUE,
        fontsize=7,
        fontweight="bold",
        ha="right",
        va="top",
    )

    # Axes — tighter x-range: both dots are under 2%; reference lines at 4% and 7%
    ax.set_xlim(-5, 10)
    ax.set_ylim(-0.7, 2.1)
    ax.set_yticks([])
    ax.set_xlabel(
        "Efficiency gap (signed; positive = UCP-favoured)", fontsize=8, color="#444"
    )
    ax.set_xticks([-4, -2, 0, 2, 4, 6, 8])
    ax.set_xticklabels(["-4%", "-2%", "0%", "+2%", "+4%", "+6%", "+8%"])
    ax.tick_params(axis="x", direction="out", length=3, pad=2)

    fig.tight_layout(pad=0.3)
    out = OUT / "lane1_dotplot.svg"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.04, facecolor="white")
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
    tests = [
        (
            "Municipal anchoring\ndeparture from norm",
            29.0,
            55.5,
            None,
            65,
            "pp below the 70–85 pp norm",
        ),
        (
            "Population spread\n(MAD widening)",
            0,
            48.0,
            None,
            55,
            "% widening relative to ensemble",
        ),
        (
            "NW Calgary district size\nexcess over average",
            0.4,
            12.2,
            5,
            16,
            "% above provincial average",
        ),
        ("Chair-flagged\nanomalies", 0, 3, 1, 5, "count"),
        ("Airdrie city splits\n(above minimum of 2)", 0, 2, 0, 3, "additional splits"),
        ("Structural-irregularity\nscore (of 5 tests)", 0, 5, 4, 5.5, "tests failing"),
    ]

    n = len(tests)
    fig, axes = plt.subplots(
        n, 1, figsize=(6.4, 6.8), dpi=300, gridspec_kw={"hspace": 0.55}
    )
    fig.patch.set_facecolor("white")

    bar_h = 0.55

    for ax, (label, maj, mino, threshold, xmax, unit) in zip(axes, tests):
        ax.set_facecolor("white")
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color("#aaaaaa")
        ax.spines["bottom"].set_linewidth(0.6)

        # Majority bar (y=1, purple)
        ax.barh(
            1,
            maj,
            height=bar_h,
            color=MAJORITY_PURPLE,
            alpha=0.9,
            edgecolor="none",
            zorder=2,
        )
        # Minority bar (y=0, green)
        ax.barh(
            0,
            mino,
            height=bar_h,
            color=MINORITY_GREEN,
            alpha=0.9,
            edgecolor="none",
            zorder=2,
        )

        # Threshold line
        if threshold is not None:
            ax.axvline(threshold, color=THRESHOLD_RED, lw=1.0, linestyle="--", zorder=3)

        # Value annotations on bar end
        offset = xmax * 0.02
        ax.text(
            max(maj, 0) + offset,
            1,
            f"{maj:g}",
            va="center",
            ha="left",
            fontsize=7.5,
            color=TEXT_DARK,
        )
        label_mino = f"{mino:g}" if isinstance(mino, float) else str(mino)
        ax.text(
            max(mino, 0) + offset,
            0,
            label_mino,
            va="center",
            ha="left",
            fontsize=7.5,
            color=TEXT_DARK,
            fontweight="bold",
        )

        ax.set_xlim(0, xmax)
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
        mpatches.Patch(facecolor=MAJORITY_PURPLE, alpha=0.9, label="Majority 2026"),
        mpatches.Patch(facecolor=MINORITY_GREEN, alpha=0.9, label="Minority 2026"),
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
        "Structural-irregularity tests: majority vs minority",
        fontsize=10,
        fontweight="bold",
        x=0.04,
        ha="left",
        y=1.02,
        color=TEXT_DARK,
    )

    out = OUT / "lane2_bars.svg"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.08, facecolor="white")
    plt.close(fig)
    return out


def build_bias_structure_matrix() -> Path:
    """The Bias-Structure Matrix — the article's primary rhetorical
    visual. Two-axis plot:
      x = Lane 1 efficiency gap (signed %; canonical official EA shapefiles, 50k 2-chain ensemble)
      y = Lane 2 structural-irregularity count (of 5 pre-registered tests)
    Three points: 2019 enacted (grey), Majority 2026 (purple), Minority
    2026 (green). Both threshold lines (Alberta ~4%, US 7%) plus the
    structural-irregularity outlier line (4 of 5). The top-right
    quadrant is the danger zone."""

    fig, ax = plt.subplots(figsize=(6.8, 5.2), dpi=300)
    fig.subplots_adjust(top=0.86, bottom=0.16, left=0.13, right=0.97)

    # Three real maps — canonical official EA shapefiles (simulation_real_map_scores_canonical.json)
    points = [
        ("2019 enacted", 2.41, 0, NEUTRAL_2019),
        ("Majority 2026", 0.10, 0, MAJORITY_PURPLE),
        ("Minority 2026", 4.02, 5, MINORITY_GREEN),
    ]

    threshold_eg_alberta = (
        3.90  # canonical ensemble p95 (simulated_ensemble_raw_samples_canonical.csv)
    )
    threshold_eg_us = 7.0
    threshold_struct = 4

    XMIN, XMAX = -1, 9
    YMIN, YMAX = -0.6, 5.7

    # Quadrant shading: gradient from clean (no shade) to both-lane outlier (deep)
    # bottom-left clean: no shading
    # top-left structural-only: light pink
    # bottom-right partisan-only: light pink
    # top-right both-lane outlier: deeper pink
    ax.axhspan(
        threshold_struct,
        YMAX,
        xmin=0,
        xmax=(threshold_eg_alberta - XMIN) / (XMAX - XMIN),
        facecolor="#fdf2f4",
        alpha=0.65,
        zorder=0,
    )
    ax.axvspan(
        threshold_eg_alberta,
        XMAX,
        ymin=0,
        ymax=(threshold_struct - YMIN) / (YMAX - YMIN),
        facecolor="#fdf2f4",
        alpha=0.65,
        zorder=0,
    )
    ax.axvspan(
        threshold_eg_alberta,
        XMAX,
        ymin=(threshold_struct - YMIN) / (YMAX - YMIN),
        ymax=1.0,
        facecolor="#f9d8de",
        alpha=0.75,
        zorder=0,
    )

    # Threshold lines
    ax.axvline(
        threshold_eg_alberta, color=THRESHOLD_RED, lw=1.2, linestyle="--", zorder=1
    )
    ax.axvline(threshold_eg_us, color="#888888", lw=1.0, linestyle=":", zorder=1)
    ax.axhline(threshold_struct, color=THRESHOLD_RED, lw=1.2, linestyle="--", zorder=1)

    # Threshold labels — placed in the top margin, well clear of dots
    ax.text(
        threshold_eg_alberta,
        YMAX - 0.05,
        "Alberta line ~4%",
        color=THRESHOLD_RED,
        fontsize=8.5,
        fontweight="bold",
        ha="center",
        va="bottom",
        bbox=dict(
            boxstyle="round,pad=0.18",
            facecolor="white",
            edgecolor=THRESHOLD_RED,
            lw=0.6,
        ),
    )
    ax.text(
        threshold_eg_us,
        YMAX - 0.05,
        "US line 7%",
        color="#555555",
        fontsize=8.5,
        fontweight="bold",
        ha="center",
        va="bottom",
        bbox=dict(
            boxstyle="round,pad=0.18", facecolor="white", edgecolor="#888888", lw=0.6
        ),
    )
    ax.text(
        XMIN + 0.2,
        threshold_struct + 0.04,
        "structural-outlier line (4 of 5 tests fail)",
        color=THRESHOLD_RED,
        fontsize=8,
        fontweight="bold",
        ha="left",
        va="bottom",
        style="italic",
    )

    # Corner annotations — lightweight, low-contrast text in each
    # quadrant so the reader knows what each corner means
    ax.text(
        XMIN + 0.15,
        YMIN + 0.15,
        "clean on both lanes",
        color="#7a7066",
        fontsize=8,
        fontstyle="italic",
        ha="left",
        va="bottom",
    )
    ax.text(
        XMIN + 0.15,
        YMAX - 0.2,
        "structural outlier\n(Lane 2 only)",
        color="#9a3340",
        fontsize=8,
        fontstyle="italic",
        ha="left",
        va="top",
        linespacing=1.15,
    )
    ax.text(
        XMAX - 0.15,
        YMAX - 0.2,
        "DANGER ZONE\nboth lanes flag",
        color="#9a3340",
        fontsize=8.5,
        fontweight="bold",
        ha="right",
        va="top",
        linespacing=1.15,
    )

    # Plot dots — larger and slightly brighter, with white halo
    # for visual pop against the shaded background
    for label, x, y, color in points:
        ax.scatter(
            x, y, s=320, c="white", edgecolors="white", linewidths=2.5, zorder=3
        )  # halo
        ax.scatter(x, y, s=240, c=color, edgecolors=TEXT_DARK, linewidths=1.4, zorder=4)

    # Per-dot labels — placed to avoid overlap, with v0_9 values shown
    label_specs = {
        "2019 enacted": ((+0.3, -0.42), "left", "top", "+2.4% / 0 of 5"),
        "Majority 2026": ((+0.3, +0.25), "left", "bottom", "+0.1% / 0 of 5"),
        "Minority 2026": ((-0.3, -0.18), "right", "top", "+4.0% / 5 of 5"),
    }
    for label, x, y, color in points:
        (ox, oy), ha, va, val = label_specs[label]
        ax.text(
            x + ox,
            y + oy,
            label,
            fontsize=10,
            fontweight="bold",
            color=TEXT_DARK,
            ha=ha,
            va=va,
        )
        ax.text(
            x + ox, y + oy - 0.30, val, fontsize=8, color="#555555", ha=ha, va="top"
        )

    # Axes
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_xlabel(
        "Lane 1: Efficiency gap (signed %)\nfurther right = more UCP-favoured",
        fontsize=9.5,
        color=TEXT_DARK,
        labelpad=8,
        linespacing=1.2,
    )
    ax.set_ylabel(
        "Lane 2: Structural-irregularity count (of 5)\nhigher = more structural problems",
        fontsize=9.5,
        color=TEXT_DARK,
        labelpad=8,
        linespacing=1.2,
    )
    ax.set_xticks([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    ax.set_xticklabels(
        ["-1%", "0%", "+1%", "+2%", "+3%", "+4%", "+5%", "+6%", "+7%", "+8%", "+9%"],
        fontsize=8.5,
    )
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.tick_params(axis="both", direction="out", length=4, pad=3, colors=TEXT_DARK)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#888888")
        ax.spines[spine].set_linewidth(0.7)

    ax.set_title(
        "The Bias-Structure Matrix",
        fontsize=12.5,
        fontweight="bold",
        loc="left",
        color=TEXT_DARK,
        pad=14,
    )
    ax.text(
        XMIN,
        YMAX + 0.55,
        "Each dot is one map. Top-right corner = both lanes flag the map. Bottom-left = clean on both.",
        ha="left",
        va="bottom",
        fontsize=8.5,
        color="#555555",
        style="italic",
    )

    out = OUT / "bias_structure_matrix.svg"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.10, facecolor="white")
    # verdict_quadrant.svg is the article-facing name for this chart
    fig.savefig(
        OUT / "verdict_quadrant.svg",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.10,
        facecolor="white",
    )
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
