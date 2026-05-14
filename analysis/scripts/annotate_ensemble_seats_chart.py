"""
annotate_ensemble_seats_chart.py

Regenerates the seats_at_50_50 ensemble distribution chart (v0_9, 250k)
with an explanatory callout annotation at the minority 2026 vertical line.

This script reads the existing raw samples CSV rather than re-running the
full ensemble. It replicates the plot_metric() style from mcmc_ensemble.py
but adds the callout so the chart is self-contained for a lay reader.

Output
------
  data/maps/mcmc/ensemble_distribution_250k_v0_9_seats_at_50_50.svg  (overwrite)

Run
---
  python analysis/scripts/annotate_ensemble_seats_chart.py

Dependencies
------------
  Backward: data/outputs/mcmc/simulated_ensemble_raw_samples.csv,
            data/outputs/mcmc/simulated_ensemble_percentiles_250k.csv
  Forward : report_public.md (seats_at_50_50 ensemble figure reference)
"""
from __future__ import annotations

# Version: 0.1 series  (added 2026-04-28 — annotation overlay only)


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
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
SAMPLES_CSV = DATA / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"
PERCENTILES_CSV = DATA / "outputs" / "simulated_ensemble_percentiles_canonical.csv"
OUT = DATA / "maps" / "mcmc" / "ensemble_distribution_canonical_seats_at_50_50.svg"

# Canonical real-map seats_at_50_50 scores (from findings/joint_outlier_score.json)
REAL_MAPS = {
    "2019 enacted": 0.45977011494252873,
    "Majority 2026": 0.4606741573033708,
    "Minority 2026": 0.516854,
}

COLORS = {
    "2019 enacted": "#1f2937",
    "Majority 2026": "#7a4d8a",  # majority purple
    "Minority 2026": "#4a8a5c",  # minority green
}

TEXT_DARK = "#1a1a1a"


def pct_rank(values: np.ndarray, x: float) -> float:
    return float(np.mean(values < x) * 100)


def main() -> None:
    df = pd.read_csv(SAMPLES_CSV)
    vals = df["seats_at_50_50"].dropna().to_numpy()
    n_sample = len(vals)
    # The canonical ensemble is 250,000 steps; the raw samples CSV may be
    # a subset. Use the pre-computed percentiles for the callout so the
    # annotation always reflects the full 250k run.
    pct_df = pd.read_csv(PERCENTILES_CSV)
    row = pct_df[
        (pct_df["metric"] == "seats_at_50_50")
        & (pct_df["map"].str.contains("minority"))
    ].iloc[0]
    minority_pct_canonical = float(row["percentile"])
    n_ensemble_canonical = 250_000
    n_above_canonical = int(
        round((1.0 - minority_pct_canonical / 100) * n_ensemble_canonical)
    )
    p5_canon = float(row["ensemble_p5"])
    p95_canon = float(row["ensemble_p95"])
    print(
        f"  loaded {n_sample:,} sample rows; canonical percentile = {minority_pct_canonical:.1f}"
    )

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=130)
    fig.patch.set_facecolor("white")

    ax.hist(vals, bins=50, color="#B9C2CF", edgecolor="#4A5060", alpha=0.9, zorder=2)

    ax.axvline(p5_canon, linestyle="--", color="#888", linewidth=1, zorder=3)
    ax.axvline(p95_canon, linestyle="--", color="#888", linewidth=1, zorder=3)
    ymax = ax.get_ylim()[1]
    ax.text(p5_canon, ymax * 0.92, "  5th", color="#444", fontsize=8, ha="left")
    ax.text(p95_canon, ymax * 0.92, "95th  ", color="#444", fontsize=8, ha="right")

    for label, value in REAL_MAPS.items():
        pr = pct_rank(vals, value)
        ax.axvline(
            value,
            linestyle="-",
            linewidth=2.2,
            color=COLORS[label],
            zorder=4,
            label=f"{label}: {value:+.4f}  (p{pr:.1f})",
        )

    # Callout annotation for the minority 2026 line — uses canonical 250k percentile
    minority_val = REAL_MAPS["Minority 2026"]
    callout_text = (
        f"Minority 2026 — {minority_pct_canonical:.1f}th percentile\n"
        f"Only ~{n_above_canonical:,} of {n_ensemble_canonical:,} maps\n"
        f"go this far UCP-favoured"
    )
    ymax_data = ax.get_ylim()[1]
    ax.annotate(
        callout_text,
        xy=(minority_val, ymax_data * 0.35),
        xytext=(minority_val - 0.048, ymax_data * 0.72),
        fontsize=9,
        color=COLORS["Minority 2026"],
        fontweight="bold",
        ha="center",
        va="bottom",
        linespacing=1.4,
        arrowprops=dict(
            arrowstyle="-|>",
            color=COLORS["Minority 2026"],
            lw=1.4,
            connectionstyle="arc3,rad=-0.25",
        ),
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="white",
            edgecolor=COLORS["Minority 2026"],
            linewidth=1.0,
            alpha=0.92,
        ),
        zorder=6,
    )

    ax.set_xlabel(
        "UCP seat share at province-wide 50/50 vote (uniform swing)",
        fontsize=10,
    )
    ax.set_ylabel(f"Count (out of {n_sample:,} samples)", fontsize=10)
    ax.set_title(
        "Ensemble distribution — UCP seat share at 50/50 vote\n"
        "(ReCom on 2019 enacted map, VA-level atomic units, v0_9 substrate, 2023 votes)",
        fontsize=10,
    )
    ax.legend(loc="upper left", framealpha=0.95, fontsize=9)
    ax.grid(axis="y", linestyle=":", linewidth=0.5, alpha=0.6, zorder=1)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUT, dpi=130, facecolor="white")
    plt.close(fig)
    print(f"  -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
