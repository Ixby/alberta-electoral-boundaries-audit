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
    """Lane 1 EG before/after — the article's most consequential
    visual. Shows the partial→full coverage shift crossing the
    ensemble-p95 line."""
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=300)

    threshold = 4.37
    # x-axis: signed EG. Negative = NDP-favoured tail; positive = UCP.
    rows = [
        ("Majority 2026", -1.29, 6.43, UCP_BLUE),
        ("Minority 2026", -2.71, 9.21, NDP_ORANGE),
    ]

    y_positions = [1, 0]
    for (label, partial, full, _), y in zip(rows, y_positions):
        # Faded "partial" dot
        ax.plot(partial, y, "o", markersize=10, color="#bbbbbb",
                markeredgecolor=TEXT_DARK, markeredgewidth=0.5, zorder=3)
        # Bold "full" dot
        ax.plot(full, y, "o", markersize=11, color=TEXT_DARK,
                markeredgecolor=TEXT_DARK, markeredgewidth=0.5, zorder=4)
        # Arrow connecting them
        ax.annotate(
            "", xy=(full, y), xytext=(partial, y),
            arrowprops=dict(arrowstyle="->", lw=1.0, color=TEXT_DARK,
                            shrinkA=8, shrinkB=8),
            zorder=2,
        )
        # Map label on the y-axis
        ax.text(-7.5, y, label, ha="left", va="center", fontsize=9,
                color=TEXT_DARK, fontweight="bold")
        # Value labels
        ax.text(partial, y - 0.3, f"{partial:+.2f}%", ha="center", va="top",
                fontsize=7, color="#777777", style="italic")
        ax.text(full, y - 0.3, f"{full:+.2f}%", ha="center", va="top",
                fontsize=7.5, color=TEXT_DARK, fontweight="bold")

    # Threshold line
    ax.axvline(threshold, color=THRESHOLD_RED, lw=1.0, linestyle="--", zorder=1)
    ax.text(threshold + 0.15, 1.7, f"ensemble p95 = {threshold}%",
            color=THRESHOLD_RED, fontsize=7.5, fontweight="bold",
            ha="left", va="top")

    # Zero line for reference
    ax.axvline(0, color="#cccccc", lw=0.5, zorder=0)

    # Tail labels (ASCII arrows for cross-platform font safety)
    ax.text(-9.5, 1.7, "<- NDP-favoured", color=NDP_ORANGE,
            fontsize=7, fontweight="bold", ha="left", va="top")
    ax.text(11.0, 1.7, "UCP-favoured ->", color=UCP_BLUE,
            fontsize=7, fontweight="bold", ha="right", va="top")

    # Axes
    ax.set_xlim(-10, 11)
    ax.set_ylim(-0.7, 2.0)
    ax.set_yticks([])
    ax.set_xlabel("Efficiency gap (signed; positive = UCP-favoured)",
                  fontsize=8, color="#444")
    ax.set_xticks([-10, -5, 0, 5, 10])
    ax.set_xticklabels(["-10%", "-5%", "0%", "+5%", "+10%"])
    ax.tick_params(axis="x", direction="out", length=3, pad=2)

    # Legend at bottom
    legend_elements = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#bbbbbb",
                   markeredgecolor=TEXT_DARK, markersize=8,
                   label="Partial coverage (67/89 EDs)"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=TEXT_DARK,
                   markeredgecolor=TEXT_DARK, markersize=8,
                   label="Full coverage (89/89 EDs)"),
    ]
    ax.legend(handles=legend_elements, loc="lower center",
              bbox_to_anchor=(0.5, -0.35), ncol=2, frameon=False,
              fontsize=7.5, handletextpad=0.5)

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
        # Majority bar (top, blue)
        ax.barh(y[i] + bar_h/2, maj, height=bar_h,
                color=UCP_BLUE, alpha=0.65, edgecolor="none", zorder=2)
        # Minority bar (bottom, orange)
        ax.barh(y[i] - bar_h/2, mino, height=bar_h,
                color=NDP_ORANGE, alpha=0.85, edgecolor="none", zorder=2)
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
        mpatches.Patch(facecolor=UCP_BLUE, alpha=0.65, label="Majority 2026"),
        mpatches.Patch(facecolor=NDP_ORANGE, alpha=0.85, label="Minority 2026"),
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
    """2×2 verdict quadrant: x = Lane 1 EG (full coverage); y =
    structural-irregularity count. Three dots: 2019 baseline, Majority
    2026, Minority 2026. Labels in plain English so it reads at a
    glance."""
    fig, ax = plt.subplots(figsize=(5.2, 4.6), dpi=300)

    # x = Lane 1 EG (signed); y = Lane 2 structural count (0-5)
    points = [
        ("2019 enacted",  2.41, 0,   NEUTRAL_2019),
        ("Majority 2026", 6.43, 0,   UCP_BLUE),
        ("Minority 2026", 9.21, 5,   NDP_ORANGE),
    ]

    threshold_eg = 4.37
    threshold_struct = 4   # 4 of 5 = outlier

    # Quadrant shading
    ax.axvspan(threshold_eg, 12, ymin=0, ymax=(threshold_struct + 0.3) / 5.5,
               color="#fdf6f7", alpha=0.6, zorder=0)
    ax.axvspan(threshold_eg, 12, ymin=(threshold_struct + 0.3) / 5.5, ymax=1.0,
               color="#fde8ec", alpha=0.7, zorder=0)
    ax.axhspan(threshold_struct, 5.5, xmin=0,
               xmax=(threshold_eg + 1) / 13, color="#fdf6f7", alpha=0.5, zorder=0)

    # Threshold lines
    ax.axvline(threshold_eg, color=THRESHOLD_RED, lw=0.8, linestyle="--", zorder=1)
    ax.axhline(threshold_struct, color=THRESHOLD_RED, lw=0.8, linestyle="--", zorder=1)

    # Axis labels
    ax.text(threshold_eg + 0.15, 5.3, "EG p95",
            color=THRESHOLD_RED, fontsize=7.5, fontweight="bold",
            ha="left", va="top")
    ax.text(0.3, threshold_struct + 0.05,
            "structural-irregularity outlier line (4 of 5)",
            color=THRESHOLD_RED, fontsize=7.5, fontweight="bold",
            ha="left", va="bottom")

    # Quadrant labels (corners)
    ax.text(0.5, 5.4, "BOTH-LANE OUTLIER\n(structural + magnitude)",
            color="#7b2d3e", fontsize=7, fontweight="bold", alpha=0,
            ha="left", va="top")  # placeholder for layout

    # Plot dots
    for label, x, y, color in points:
        ax.scatter(x, y, s=180, c=color, edgecolors=TEXT_DARK,
                   linewidths=1.0, zorder=4)
        # Label position offset
        if label == "Minority 2026":
            offset_x, offset_y = 0.4, 0.0
            ha = "left"
        elif label == "Majority 2026":
            offset_x, offset_y = 0.4, 0.25
            ha = "left"
        else:
            offset_x, offset_y = -0.4, -0.25
            ha = "right"
        ax.text(x + offset_x, y + offset_y, label,
                fontsize=8.5, fontweight="bold", color=TEXT_DARK,
                ha=ha, va="center")

    # Axes
    ax.set_xlim(-1, 12)
    ax.set_ylim(-0.5, 5.5)
    ax.set_xlabel("Lane 1: Efficiency gap (full-coverage, signed %)",
                  fontsize=9, color=TEXT_DARK, labelpad=6)
    ax.set_ylabel("Lane 2: Structural-irregularity count (of 5)",
                  fontsize=9, color=TEXT_DARK, labelpad=6)
    ax.set_xticks([0, 3, 6, 9])
    ax.set_xticklabels(["0%", "+3%", "+6%", "+9%"])
    ax.set_yticks([0, 1, 2, 3, 4, 5])

    ax.set_title("The verdict in one chart",
                 fontsize=10.5, fontweight="bold", loc="left",
                 color=TEXT_DARK, pad=10)

    # Subtitle / caption
    fig.text(0.5, -0.03,
             "Top-right quadrant = both lanes flag the map. "
             "Bottom-left = clean on both.",
             ha="center", fontsize=7.5, color="#666", style="italic")

    fig.tight_layout(pad=0.5)
    out = OUT / "verdict_quadrant.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.06,
                facecolor="white")
    plt.close(fig)
    return out


def main() -> int:
    print("[article figures] generating embedded charts…")
    print(f"  output dir: {OUT}")
    p1 = build_lane1_dotplot()
    print(f"  ✓ {p1.relative_to(ROOT)}")
    p2 = build_lane2_bars()
    print(f"  ✓ {p2.relative_to(ROOT)}")
    p3 = build_verdict_quadrant()
    print(f"  ✓ {p3.relative_to(ROOT)}")
    print("[article figures] done — embed via standard markdown image syntax")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
