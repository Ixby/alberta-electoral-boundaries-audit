"""
v0_1_article_figures.py

Generate the inline figures the magazine article embeds:

  1. lane1_dotplot.svg    — Lane 1 EG histogram: 250,000 neutral-ensemble
     maps shown as bars, right tail (p90+) shaded in red. Vertical lines
     for Minority 2026 (+4.02%, p94), Majority 2026 (+0.10%, p15), and
     2019 enacted (+2.41%, p69). p95 reference line dashed.
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

# Editorial palette — source of truth is palette.py; do not redeclare here
from palette import (
    MINORITY_PURPLE, MINORITY_PURPLE_LIGHT,
    MAJORITY_TEAL, MAJORITY_TEAL_LIGHT,
    NDP_ORANGE, UCP_BLUE,
    NEUTRAL_2019, RULE_GREY, TEXT_DARK, THRESHOLD_RED, NORM_BAND,
)

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
    """Lane 1 EG histogram — 250k neutral-ensemble maps with real-map lines overlaid."""
    import pandas as _pd
    import matplotlib.transforms as _mtrans
    from matplotlib.colors import to_rgba

    samples_path = ROOT / "data" / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"
    eg_pct = _pd.read_csv(samples_path, usecols=["efficiency_gap"])["efficiency_gap"].values * 100

    # Verified from simulation_real_map_scores_canonical.json and
    # simulated_ensemble_percentiles_canonical.csv
    minority_eg = 4.02   # p94.4 of neutral ensemble
    majority_eg = 0.10   # p15.5
    enacted_eg  = 2.41   # p69.0, 2019 enacted baseline
    p95_val     = 4.10   # ensemble p95

    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=300)

    counts, edges = np.histogram(eg_pct, bins=80)
    centers = (edges[:-1] + edges[1:]) / 2
    widths  = edges[1:]  - edges[:-1]

    p90_val = float(np.percentile(eg_pct, 90))
    bar_colors = [
        to_rgba(THRESHOLD_RED, 0.28) if c >= p90_val else to_rgba(RULE_GREY, 0.55)
        for c in centers
    ]
    ax.bar(centers, counts, width=widths, color=bar_colors, linewidth=0)

    # Blended transform: x in data coords, y in axes fraction (0=bottom, 1=top)
    bx = _mtrans.blended_transform_factory(ax.transData, ax.transAxes)

    # p95 dashed reference line
    ax.axvline(p95_val, color=THRESHOLD_RED, lw=1.0, linestyle="--", zorder=2)
    ax.text(p95_val + 0.12, 0.97, "p95\n4.1%",
            color=THRESHOLD_RED, fontsize=6.5, fontweight="bold",
            ha="left", va="top", transform=bx)

    # Real-map vertical lines
    ax.axvline(minority_eg, color=MINORITY_PURPLE, lw=2.0, zorder=5)
    ax.axvline(majority_eg, color=MAJORITY_TEAL,   lw=2.0, zorder=5)
    ax.axvline(enacted_eg,  color=NEUTRAL_2019,    lw=1.3, linestyle="--", zorder=4)

    # Labels — minority goes left of its line to clear the p95 label at 4.22
    ax.text(minority_eg - 0.15, 0.97, "Minority 2026\n+4.02%, p94",
            color=MINORITY_PURPLE, fontsize=6.5, fontweight="bold",
            ha="right", va="top", transform=bx)
    ax.text(majority_eg, 0.97, "Majority 2026\n+0.10%, p15",
            color=MAJORITY_TEAL, fontsize=6.5, fontweight="bold",
            ha="center", va="top", transform=bx)
    ax.text(enacted_eg + 0.12, 0.97, "2019 enacted\n+2.41%, p69",
            color=NEUTRAL_2019, fontsize=6.5, fontweight="bold",
            ha="left", va="top", transform=bx)

    # Directional labels at top corners
    ax.text(0.02, 0.99, "← NDP-favoured",
            color=NDP_ORANGE, fontsize=7, fontweight="bold",
            ha="left", va="top", transform=ax.transAxes)
    ax.text(0.98, 0.99, "UCP-favoured →",
            color=UCP_BLUE, fontsize=7, fontweight="bold",
            ha="right", va="top", transform=ax.transAxes)

    ax.set_xlim(-5, 10)
    ax.set_xlabel("Efficiency gap (positive = UCP-favoured)", fontsize=8, color="#444")
    ax.set_ylabel("Neutral maps", fontsize=8, color="#444")
    ax.set_xticks([-4, -2, 0, 2, 4, 6, 8])
    ax.set_xticklabels(["-4%", "-2%", "0%", "+2%", "+4%", "+6%", "+8%"])
    ax.tick_params(axis="both", direction="out", length=3, pad=2)

    fig.tight_layout(pad=0.4)
    out = OUT / "lane1_dotplot.svg"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.06, facecolor="white")
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
        n, 1, figsize=(6.4, 7.8), dpi=300, gridspec_kw={"hspace": 0.80}
    )
    fig.patch.set_facecolor("white")

    bar_h = 0.55

    for ax, (label, maj, mino, threshold, xmax, unit) in zip(axes, tests):
        ax.set_facecolor("white")
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
            f"{maj:g}",
            va="center",
            ha=maj_ha,
            fontsize=7.5,
            color=TEXT_DARK,
        )
        label_mino = f"{mino:g}" if isinstance(mino, float) else str(mino)
        mino_x = max(mino, xmax * 0.04) if mino == 0 else mino + offset
        ax.text(
            mino_x,
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
    Three points: 2019 enacted (grey), Majority 2026 (green), Minority
    2026 (red). Both threshold lines (Alberta ~4%, US 7%) plus the
    structural-irregularity outlier line (4 of 5). The top-right
    quadrant is the danger zone."""

    fig, ax = plt.subplots(figsize=(6.8, 5.2), dpi=300)
    fig.subplots_adjust(top=0.86, bottom=0.16, left=0.13, right=0.97)

    # Three real maps — canonical official EA shapefiles (simulation_real_map_scores_canonical.json)
    points = [
        ("2019 enacted", 2.41, 0, NEUTRAL_2019),
        ("Majority 2026", 0.10, 0, MAJORITY_TEAL),
        ("Minority 2026", 4.02, 5, MINORITY_PURPLE),
    ]

    threshold_eg_alberta = (
        4.11  # canonical ensemble p95 (simulated_ensemble_percentiles_canonical.csv: 0.041086)
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
        "Alberta line ~4.1%",
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
        "US gerrymander signal line 7%",
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
    # Label offsets chosen to prevent three specific collisions:
    # - "2019 enacted" previously placed below y=0 dot, val text fell below ylim=-0.6 → moved above
    # - "Minority 2026" dot at (4.02, 5) is near Alberta bbox at top → offset further down
    # - "Majority 2026" and "2019 enacted" both at y=0; offset in opposite directions to separate
    label_specs = {
        "2019 enacted":  ((+0.30, +0.32), "left", "bottom", "+2.4% / 0 of 5"),
        "Majority 2026": ((-0.30, +0.28), "right", "bottom", "+0.1% / 0 of 5"),
        "Minority 2026": ((-0.30, -0.55), "right", "top",    "+4.0% / 5 of 5"),
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
            x + ox,
            y + oy + (0.22 if va == "bottom" else -0.28),
            val,
            fontsize=8,
            color="#555555",
            ha=ha,
            va=va,
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
