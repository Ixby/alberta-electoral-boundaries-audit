"""
replot_mcmc_figures.py
----------------------
Regenerate all MCMC ensemble SVGs (ensemble_distribution_* and running_mean_*)
from saved checkpoint CSV files and scores JSON files, without re-running the
MCMC chains. Run after changing plot colours or layout in mcmc_ensemble.py.

Usage
-----
  python analysis/scripts/replot_mcmc_figures.py

Outputs
-------
  data/maps/mcmc/ensemble_distribution_{run_id}_{metric}.svg
  data/maps/mcmc/running_mean_{run_id}_{metric}.svg
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from mcmc_ensemble import plot_metric, plot_running_mean  # noqa: E402

MAPS = ROOT / "data" / "maps" / "mcmc"
MAPS.mkdir(parents=True, exist_ok=True)

DATA = ROOT / "data"


def _load_checkpoints(checkpoint_dir: Path, metric_keys: list[str]) -> pd.DataFrame:
    parts = []
    for csv_path in sorted(checkpoint_dir.glob("chain*_samples.csv")):
        df = pd.read_csv(csv_path)
        parts.append(df)
    if not parts:
        raise FileNotFoundError(f"No chain CSVs in {checkpoint_dir}")
    combined = pd.concat(parts, ignore_index=True)
    # keep only columns that exist
    return combined[[k for k in metric_keys if k in combined.columns]]


def _scores_to_realmap(scores: dict, metric_key: str) -> dict:
    """Build real_maps dict from a scores JSON for one metric."""
    result = {}
    for map_key, display in [
        ("2019_enacted",   "2019 enacted"),
        ("majority_2026",  "Majority 2026"),
        ("minority_2026",  "Minority 2026"),
    ]:
        entry = scores.get(map_key)
        if entry is None:
            continue
        if isinstance(entry, dict):
            val = entry.get(metric_key, float("nan"))
        else:
            val = float("nan")
        result[display] = val if val is not None else float("nan")
    return result


VARIANTS = [
    {
        "run_id": "canonical",
        "checkpoint_dir": DATA / "simulation_checkpoints_canonical",
        "scores_json": DATA / "outputs" / "simulation_real_map_scores_canonical.json",
        "metrics": [
            "efficiency_gap", "mean_median", "declination", "seats_at_50_50",
            "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030",
        ],
    },
    {
        "run_id": "section_c",
        "checkpoint_dir": DATA / "simulation_checkpoints_section_c",
        "scores_json": DATA / "outputs" / "mcmc" / "simulation_real_map_scores.json",
        "metrics": [
            "efficiency_gap", "mean_median", "declination", "seats_at_50_50",
            "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030",
        ],
    },
    {
        "run_id": "threshold_2019",
        "checkpoint_dir": DATA / "simulation_checkpoints_threshold_2019",
        "scores_json": DATA / "outputs" / "mcmc" / "simulation_real_map_scores_full.json",
        "metrics": [
            "efficiency_gap", "mean_median", "declination", "seats_at_50_50",
            "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030",
        ],
    },
    {
        "run_id": "threshold_2015",
        "checkpoint_dir": DATA / "simulation_checkpoints_threshold_2015",
        "scores_json": DATA / "outputs" / "mcmc" / "simulation_real_map_scores_full_v2.json",
        "metrics": [
            "efficiency_gap", "mean_median", "declination", "seats_at_50_50",
            "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030",
        ],
    },
    {
        "run_id": "250k_v0_10",
        "samples_csv": DATA / "outputs" / "mcmc" / "simulated_ensemble_raw_samples_250k.csv",
        "scores_json": DATA / "outputs" / "mcmc" / "simulation_real_map_scores_250k.json",
        "metrics": ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"],
    },
]


def process_variant(v: dict) -> None:
    run_id = v["run_id"]
    metrics = v["metrics"]
    print(f"\n--- {run_id} ---")

    # Load samples
    if "checkpoint_dir" in v:
        cdir = v["checkpoint_dir"]
        if not cdir.exists():
            print(f"  skip: checkpoint dir not found: {cdir}")
            return
        df = _load_checkpoints(cdir, metrics)
    else:
        csv = v["samples_csv"]
        if not csv.exists():
            print(f"  skip: samples CSV not found: {csv}")
            return
        df = pd.read_csv(csv)

    # Load scores
    scores_path = v["scores_json"]
    if not scores_path.exists():
        print(f"  skip: scores JSON not found: {scores_path}")
        return
    with open(scores_path) as f:
        scores = json.load(f)

    for metric in metrics:
        if metric not in df.columns:
            print(f"  skip metric {metric}: not in samples")
            continue
        vals = df[metric].dropna().to_numpy()
        if len(vals) == 0:
            print(f"  skip metric {metric}: no data")
            continue

        real_maps = _scores_to_realmap(scores, metric)

        dist_out = MAPS / f"ensemble_distribution_{run_id}_{metric}.svg"
        plot_metric(metric, metric, vals, real_maps, dist_out)
        print(f"  [ok] {dist_out.name}")

        rm_out = MAPS / f"running_mean_{run_id}_{metric}.svg"
        plot_running_mean(metric, vals, rm_out, metric)
        print(f"  [ok] {rm_out.name}")

    # Also regenerate the annotate_ensemble_seats_chart for canonical
    if run_id == "canonical":
        try:
            import annotate_ensemble_seats_chart as aesc
            aesc.main()
            print("  [ok] annotate_ensemble_seats_chart")
        except Exception as e:
            print(f"  [warn] annotate_ensemble_seats_chart failed: {e}")


def main() -> None:
    for v in VARIANTS:
        process_variant(v)
    print("\nDone.")


if __name__ == "__main__":
    main()
