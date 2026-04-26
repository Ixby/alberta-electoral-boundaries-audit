"""
v0_1_article_figures.py

Generate the inline figures the magazine article embeds:

  1. lane1_dotplot.png    — Lane 1 EG before/after dot plot. Four dots:
     Majority partial (-1.29%), Majority full (+6.43%), Minority partial
     (-2.71%), Minority full (+9.21%), arrows showing the partial→full
     shift, vertical line at the ensemble p95 (4.37%).
  2. lane2_bars.png       — Lane 2 horizontal bar chart of structural
     irregularities, one row per test, magnitude relative to comparator
     norm; majority + minority side by side; norm band shaded.
  3. verdict_quadrant.png — 2×2 quadrant: x-axis "Lane 1 (numbers, EG)";
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

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "data" / "maps" / "article"
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
plt.rcParams.update({
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
})


def build_lane1_dotplot() -> Path:
    """Lane 1 EG dot plot — both 2026 maps placed against two reference
    lines: the audit's Alberta-calibrated 4.37% line and the academic-
    literature US 7% line."""
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=300)

    alberta_line = 5.00
    us_line = 7.00
    # Map colour convention: majority = purple, minority = green
    rows = [
        ("Majority 2026", 6.43, MAJORITY_PURPLE),
        ("Minority 2026", 9.21, MINORITY_GREEN),
    ]

    y_positions = [1, 0]
    for (label, full, color), y in zip(rows, y_positions):
        ax.plot(full, y, "o", markersize=12, color=color,
                markeredgecolor=TEXT_DARK, markeredgewidth=0.6, zorder=4)
        ax.text(-7.5, y, label, ha="left", va="center", fontsize=9,
                color=TEXT_DARK, fontweight="bold")
        ax.text(full, y - 0.32, f"{full:+.2f}%", ha="center", va="top",
                fontsize=8, color=TEXT_DARK, fontweight="bold")

    # Alberta-calibrated threshold line (audit's, more demanding)
    ax.axvline(alberta_line, color=THRESHOLD_RED, lw=1.0, linestyle="--", zorder=1)
    ax.text(alberta_line + 0.15, 1.85, f"Alberta line\n{alberta_line}%",
            color=THRESHOLD_RED, fontsize=7, fontweight="bold",
            ha="left", va="top", linespacing=1.0)

    # US 7% line (Whitford v. Gill literature reference)
    ax.axvline(us_line, color="#888888", lw=0.9, linestyle=":", zorder=1)
    ax.text(us_line + 0.15, 1.85, f"US line\n{us_line}%",
            color="#666666", fontsize=7, fontweight="bold",
            ha="left", va="top", linespacing=1.0)

    # Zero line for reference
    ax.axvline(0, color="#cccccc", lw=0.5, zorder=0)

    # Tail labels (ASCII arrows for cross-platform font safety)
    ax.text(-9.5, 1.85, "<- NDP-favoured", color=NDP_ORANGE,
            fontsize=7, fontweight="bold", ha="left", va="top")
    ax.text(11.0, 1.85, "UCP-favoured ->", color=UCP_BLUE,
            fontsize=7, fontweight="bold", ha="right", va="top")

    # Axes
    ax.set_xlim(-10, 11)
    ax.set_ylim(-0.7, 2.1)
    ax.set_yticks([])
    ax.set_xlabel("Efficiency gap (signed; positive = UCP-favoured)",
                  fontsize=8, color="#444")
    ax.set_xticks([-10, -5, 0, 5, 10])
    ax.set_xticklabels(["-10%", "-5%", "0%", "+5%", "+10%"])
    ax.tick_params(axis="x", direction="out", length=3, pad=2)

    fig.tight_layout(pad=0.3)
    out = OUT / "lane1_dotplot.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.04,
                facecolor="white")
    plt.close(fig)
    return out


def build_lane2_bars() -> Path:
    """Lane 2 horizontal bar chart — magnitude of each structural test
    plotted as majority vs minority side-by-side, normalised so larger
    = more concerning."""
    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=300)

    # Each row: (label, majority_value, minority_value, threshold_val,
    #            normalisation_max_for_visual_scale)
    # We plot bars normalised to [0, 1] where 1 = at-or-beyond
    # the most extreme observed value (visually consistent comparison).
    tests = [
        ("Anchoring departure from norm",   29.0, 55.5, 0,    60),  # pp below 70-85 norm
        ("Population spread (MAD widening %)", 0,  48.0, 0,   60),
        ("NW Calgary excess (% over avg)",   0.4, 12.2, 5,    15),
        ("Chair-flagged anomalies",          0,    3,   1,     5),
        ("Airdrie pieces (over min 2)",      0,    2,   0,     3),
        ("Structural-irregularity count (of 5)", 0, 5,  4,     5),
    ]

    n = len(tests)
    y = np.arange(n)
    bar_h = 0.36

    for i, (label, maj, mino, threshold, vmax) in enumerate(tests):
        # Majority bar (top, purple)
        ax.barh(y[i] + bar_h/2, maj, height=bar_h,
                color=MAJORITY_PURPLE, alpha=0.9, edgecolor="none", zorder=2)
        # Minority bar (bottom, green)
        ax.barh(y[i] - bar_h/2, mino, height=bar_h,
                color=MINORITY_GREEN, alpha=0.9, edgecolor="none", zorder=2)
        # Threshold line for this row
        if threshold > 0:
            ax.plot([threshold, threshold],
                    [y[i] - bar_h - 0.05, y[i] + bar_h + 0.05],
                    color=THRESHOLD_RED, lw=0.8, linestyle="--", zorder=3)
        # Value labels
        ax.text(maj + vmax * 0.015, y[i] + bar_h/2, str(maj) if maj else "—",
                va="center", ha="left", fontsize=7, color=TEXT_DARK)
        ax.text(mino + vmax * 0.015, y[i] - bar_h/2,
                f"{mino}" if isinstance(mino, int) else f"{mino:g}",
                va="center", ha="left", fontsize=7,
                color=TEXT_DARK, fontweight="bold")
        # Test label on the left, with a numeric x-axis for that row
        # (each row has its own scale conceptually but we use a shared
        # 0-to-vmax visual range per row by clipping x-limits per row —
        # a true small-multiples layout)

    # We're using a single shared x scale of 0..60 for visual coherence.
    # Notes: the population MAD widening % and anchoring departure are
    # both plotted against percent-points, which share the 60% scale.
    # Smaller-scale rows (chair flags, Airdrie pieces, structural count)
    # plot at near-zero on this scale and look minimal — we add a
    # secondary annotation column on the right for those.

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in tests], fontsize=8, color=TEXT_DARK)
    ax.invert_yaxis()
    ax.set_xlim(0, 60)
    ax.set_xlabel("Magnitude (units vary per row — see test name)",
                  fontsize=8, color="#666", style="italic")
    ax.set_xticks([0, 15, 30, 45, 60])
    ax.set_xticklabels(["0", "15", "30", "45", "60"], fontsize=7)

    # Title
    ax.set_title("Structural-irregularity tests: majority vs minority",
                 fontsize=10, fontweight="bold", loc="left",
                 color=TEXT_DARK, pad=8)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=MAJORITY_PURPLE, alpha=0.9, label="Majority 2026"),
        mpatches.Patch(facecolor=MINORITY_GREEN, alpha=0.9, label="Minority 2026"),
        plt.Line2D([0], [0], color=THRESHOLD_RED, lw=0.8, linestyle="--",
                   label="Threshold for that test"),
    ]
    ax.legend(handles=legend_elements, loc="lower right",
              fontsize=7.5, frameon=False, handletextpad=0.5)

    fig.tight_layout(pad=0.3)
    out = OUT / "lane2_bars.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.04,
                facecolor="white")
    plt.close(fig)
    return out


def build_verdict_quadrant() -> Path:
    """The verdict in one chart — the article's primary rhetorical
    visual. Two-axis plot:
      x = Lane 1 efficiency gap (signed %; v0_8 full coverage, Run #6 2M MCMC)
      y = Lane 2 structural-irregularity count (of 5 pre-registered tests)
    Three points: 2019 enacted (grey), Majority 2026 (purple), Minority
    2026 (green). Both threshold lines (Alberta ~5%, US 7%) plus the
    structural-irregularity outlier line (4 of 5). The top-right
    quadrant is the danger zone."""

    fig, ax = plt.subplots(figsize=(6.8, 5.2), dpi=300)
    fig.subplots_adjust(top=0.86, bottom=0.16, left=0.13, right=0.97)

    # Three real maps
    points = [
        ("2019 enacted",  2.41, 0,   NEUTRAL_2019),
        ("Majority 2026", 6.43, 0,   MAJORITY_PURPLE),
        ("Minority 2026", 9.21, 5,   MINORITY_GREEN),
    ]

    threshold_eg_alberta = 5.0
    threshold_eg_us = 7.0
    threshold_struct = 4

    XMIN, XMAX = -2, 12
    YMIN, YMAX = -0.6, 5.7

    # Quadrant shading: gradient from clean (no shade) to both-lane outlier (deep)
    # bottom-left clean: no shading
    # top-left structural-only: light pink
    # bottom-right partisan-only: light pink
    # top-right both-lane outlier: deeper pink
    ax.axhspan(threshold_struct, YMAX, xmin=0,
               xmax=(threshold_eg_alberta - XMIN) / (XMAX - XMIN),
               facecolor="#fdf2f4", alpha=0.65, zorder=0)
    ax.axvspan(threshold_eg_alberta, XMAX,
               ymin=0, ymax=(threshold_struct - YMIN) / (YMAX - YMIN),
               facecolor="#fdf2f4", alpha=0.65, zorder=0)
    ax.axvspan(threshold_eg_alberta, XMAX,
               ymin=(threshold_struct - YMIN) / (YMAX - YMIN), ymax=1.0,
               facecolor="#f9d8de", alpha=0.75, zorder=0)

    # Threshold lines
    ax.axvline(threshold_eg_alberta, color=THRESHOLD_RED, lw=1.2,
               linestyle="--", zorder=1)
    ax.axvline(threshold_eg_us, color="#888888", lw=1.0,
               linestyle=":", zorder=1)
    ax.axhline(threshold_struct, color=THRESHOLD_RED, lw=1.2,
               linestyle="--", zorder=1)

    # Threshold labels — placed in the top margin, well clear of dots
    ax.text(threshold_eg_alberta, YMAX - 0.05,
            "Alberta line ~5%",
            color=THRESHOLD_RED, fontsize=8.5, fontweight="bold",
            ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                      edgecolor=THRESHOLD_RED, lw=0.6))
    ax.text(threshold_eg_us, YMAX - 0.05,
            "US line 7%",
            color="#555555", fontsize=8.5, fontweight="bold",
            ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                      edgecolor="#888888", lw=0.6))
    ax.text(XMIN + 0.2, threshold_struct + 0.04,
            "structural-outlier line (4 of 5 tests fail)",
            color=THRESHOLD_RED, fontsize=8, fontweight="bold",
            ha="left", va="bottom", style="italic")

    # Corner annotations — lightweight, low-contrast text in each
    # quadrant so the reader knows what each corner means
    ax.text(XMIN + 0.3, YMIN + 0.15, "clean on both lanes",
            color="#7a7066", fontsize=8, fontstyle="italic",
            ha="left", va="bottom")
    ax.text(XMAX - 0.2, YMAX - 0.6, "DANGER ZONE\nboth lanes flag the map",
            color="#9a3340", fontsize=8.5, fontweight="bold",
            ha="right", va="top", linespacing=1.15)

    # Plot dots — larger and slightly brighter, with white halo
    # for visual pop against the shaded background
    for label, x, y, color in points:
        ax.scatter(x, y, s=320, c="white", edgecolors="white",
                   linewidths=2.5, zorder=3)  # halo
        ax.scatter(x, y, s=240, c=color, edgecolors=TEXT_DARK,
                   linewidths=1.4, zorder=4)

    # Per-dot labels — placed to avoid overlap, with values shown
    label_specs = {
        "2019 enacted":  ((-0.5, -0.42), "right", "top",
                          "+2.4% / 0 of 5"),
        "Majority 2026": ((+0.5, -0.42), "left", "top",
                          "+6.4% / 0 of 5"),
        "Minority 2026": ((-0.5, -0.18), "right", "top",
                          "+9.2% / 5 of 5"),
    }
    for label, x, y, color in points:
        (ox, oy), ha, va, val = label_specs[label]
        ax.text(x + ox, y + oy, label,
                fontsize=10, fontweight="bold", color=TEXT_DARK,
                ha=ha, va=va)
        ax.text(x + ox, y + oy - 0.30, val,
                fontsize=8, color="#555555",
                ha=ha, va="top")

    # Axes
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_xlabel("Lane 1: Efficiency gap (signed %)\nfurther right = more UCP-favoured",
                  fontsize=9.5, color=TEXT_DARK, labelpad=8, linespacing=1.2)
    ax.set_ylabel("Lane 2: Structural-irregularity count (of 5)\nhigher = more structural problems",
                  fontsize=9.5, color=TEXT_DARK, labelpad=8, linespacing=1.2)
    ax.set_xticks([-2, 0, 2, 4, 6, 8, 10, 12])
    ax.set_xticklabels(["-2%", "0%", "+2%", "+4%", "+6%", "+8%", "+10%", "+12%"],
                       fontsize=8.5)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.tick_params(axis="both", direction="out", length=4, pad=3,
                   colors=TEXT_DARK)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#888888")
        ax.spines[spine].set_linewidth(0.7)

    ax.set_title("The verdict in one chart",
                 fontsize=12.5, fontweight="bold", loc="left",
                 color=TEXT_DARK, pad=14)
    ax.text(XMIN, YMAX + 0.55,
            "Each dot is one map. Top-right corner = both lanes flag the map. Bottom-left = clean on both.",
            ha="left", va="bottom", fontsize=8.5, color="#555555",
            style="italic")

    out = OUT / "verdict_quadrant.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.10,
                facecolor="white")
    plt.close(fig)
    return out


def main() -> int:
    print("[article figures] generating embedded charts...")
    print(f"  output dir: {OUT}")
    p1 = build_lane1_dotplot()
    print(f"  [ok] {p1.relative_to(ROOT)}")
    p2 = build_lane2_bars()
    print(f"  [ok] {p2.relative_to(ROOT)}")
    p3 = build_verdict_quadrant()
    print(f"  [ok] {p3.relative_to(ROOT)}")
    print("[article figures] done -- embed via standard markdown image syntax")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
