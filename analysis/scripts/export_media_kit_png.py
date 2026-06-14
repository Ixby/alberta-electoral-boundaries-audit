# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
"""
export_media_kit_png.py

Export 300 dpi PNG versions of the five key article figures to
data/maps/media_kit/ for media / press distribution.

Wraps article_figures.py and adds a PNG save alongside each SVG.

Run:
    python analysis/scripts/export_media_kit_png.py

Forward:  data/maps/media_kit/  (PNG files, NOT tracked by git — add to .gitignore if needed)
Backward: analysis/scripts/article_figures.py  (source of truth for figure content)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MEDIA_KIT = ROOT / "data" / "maps" / "media_kit"
MEDIA_KIT.mkdir(parents=True, exist_ok=True)

# Figure name → media kit output name
NAME_MAP = {
    "lane1_dotplot":            "fig1_ensemble_dotplot",
    "lane2_bars":               "fig2_structural_scorecard",
    "bias_structure_matrix":    "fig3_bias_structure",
    "stakes_quadrant":          None,  # duplicate of bias_structure_matrix; skip
}

_original_savefig = plt.Figure.savefig


def _patched_savefig(self, fname, *args, **kwargs):
    """Save SVG as normal, and also save PNG to media_kit/."""
    _original_savefig(self, fname, *args, **kwargs)
    stem = Path(str(fname)).stem
    kit_name = NAME_MAP.get(stem)
    if kit_name is None:
        return
    png_path = MEDIA_KIT / f"{kit_name}.png"
    png_kwargs = {k: v for k, v in kwargs.items() if k not in ("format",)}
    _original_savefig(self, png_path, *args, format="png", **png_kwargs)
    sz = png_path.stat().st_size
    print(f"  [media_kit] {png_path.name}  ({sz // 1024} KB)")


plt.Figure.savefig = _patched_savefig  # type: ignore[method-assign]

import article_figures  # noqa: E402 (must come after the patch)


def main() -> int:
    print("[export_media_kit_png] generating media-kit PNGs...")
    print(f"  output dir: {MEDIA_KIT}")
    article_figures.main()

    # Also export the canonical seats@50/50 distribution from mcmc/
    try:
        _export_canonical_seats()
    except Exception as exc:
        print(f"  [warn] canonical seats distribution export failed: {exc}")

    # Airdrie map figure
    try:
        _export_airdrie_figure()
    except Exception as exc:
        print(f"  [warn] Airdrie figure export failed: {exc}")

    print("[export_media_kit_png] done")
    return 0


def _export_canonical_seats() -> None:
    """Re-render the canonical seats_at_50_50 distribution as a 300 dpi PNG."""
    import numpy as np
    import pandas as pd
    import json

    samples_path = ROOT / "data" / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"
    pct_path     = ROOT / "data" / "outputs" / "simulated_ensemble_percentiles_canonical.csv"

    df = pd.read_csv(samples_path, usecols=["seats_at_50_50"])
    vals = df["seats_at_50_50"].dropna().to_numpy()

    pct_df = pd.read_csv(pct_path)
    row = pct_df[(pct_df["metric"] == "seats_at_50_50") & pct_df["map"].str.contains("minority")].iloc[0]
    p5_canon  = float(row["ensemble_p5"])
    p95_canon = float(row["ensemble_p95"])

    # seat fractions; minority_2026 / majority_2026 / 2019_enacted
    REAL_MAPS = {
        "2019 enacted":  0.45977011494252873,
        "Majority 2026": 0.4606741573033708,
        "Minority 2026": 0.516854,
    }
    COLORS = {"2019 enacted": "#888888", "Majority 2026": "#007A6C", "Minority 2026": "#7B2D8B"}

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    fig.patch.set_facecolor("white")
    ax.hist(vals, bins=50, color="#B9C2CF", edgecolor="#4A5060", alpha=0.9, zorder=2)
    ax.axvline(p5_canon,  linestyle="--", color="#888", linewidth=1, zorder=3)
    ax.axvline(p95_canon, linestyle="--", color="#888", linewidth=1, zorder=3)
    ymax = ax.get_ylim()[1]
    ax.text(p5_canon,  ymax * 0.92, "  5th",  color="#444", fontsize=8, ha="left")
    ax.text(p95_canon, ymax * 0.92, "95th  ", color="#444", fontsize=8, ha="right")

    def pct_rank(x):
        return float(np.mean(vals < x) * 100)

    for label, value in REAL_MAPS.items():
        pr = pct_rank(value)
        ax.axvline(value, linestyle="-", linewidth=2.2, color=COLORS[label], zorder=4,
                   label=f"{label}: {value:+.4f}  (p{pr:.1f})")

    ax.set_xlabel("UCP seat share at 50/50 vote split (fraction of 89 seats)")
    ax.set_ylabel(f"Count of neutral maps  (n={len(vals):,})")
    ax.set_title("Seats at 50/50 vote split — canonical ensemble", fontsize=11, loc="left")
    ax.legend(fontsize=8)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)

    out = MEDIA_KIT / "fig4_seats_distribution.png"
    _original_savefig(fig, out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    sz = out.stat().st_size
    print(f"  [media_kit] {out.name}  ({sz // 1024} KB)  [regenerated from data]")


def _export_airdrie_figure() -> None:
    """Export figure_airdrie_v3 as PNG by monkey-patching the article-figures OUT path."""
    import generate_article_figures as gaf

    orig_out = gaf.OUT
    orig_dpi = gaf.FIG_DPI

    # Patch to save PNG to media_kit
    class _PNGOut:
        def __truediv__(self, name):
            stem = Path(name).stem
            return MEDIA_KIT / f"fig5_airdrie_split.png"

    gaf.OUT = _PNGOut()
    gaf.FIG_DPI = 300
    try:
        gaf.build_airdrie()
        out = MEDIA_KIT / "fig5_airdrie_split.png"
        if out.exists():
            sz = out.stat().st_size
            print(f"  [media_kit] {out.name}  ({sz // 1024} KB)")
        else:
            print("  [warn] fig5_airdrie_split.png was not created")
    finally:
        gaf.OUT = orig_out
        gaf.FIG_DPI = orig_dpi


if __name__ == "__main__":
    raise SystemExit(main())
