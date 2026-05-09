"""
Integration tests for pipeline stage output schemas.

These tests load actual data files produced by the analysis pipeline and validate
that they match the expected schemas. All tests are skipped if the required file is
absent — CI does not have the data files in the repo.

Forward dependencies: pipeline_schemas.py
Backward dependencies: none (end-to-end validation only)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd
import pytest

# Resolve repo root: this file is in tests/, repo root is one level up
REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "tests"))
from pipeline_schemas import (
    ConvergenceDiagSchema,
    DrainMapSchema,
    EnsembleRowSchema,
    PlacementEntrySchema,
    PlacementMetricSchema,
    assert_schema,
)


# ── File paths ────────────────────────────────────────────────────────────────

ENSEMBLE_RAW = REPO_ROOT / "data" / "simulated_ensemble_raw_samples_canonical.csv"
ENSEMBLE_PCT = REPO_ROOT / "data" / "simulated_ensemble_percentiles_canonical.csv"
CONVERGENCE  = REPO_ROOT / "data" / "simulation_convergence_diagnostics_canonical.json"
PLACEMENT    = REPO_ROOT / "data" / "outputs" / "final_percentile_placement.json"
DRAIN        = REPO_ROOT / "data" / "neighbour_drain_summary.json"


# ── test_ensemble_csv_schema ─────────────────────────────────────────────────

@pytest.mark.skipif(not ENSEMBLE_RAW.exists(), reason="ensemble CSV not in repo")
def test_ensemble_raw_csv_schema():
    """Ensemble CSV must have required columns with correct dtypes and no NaN."""
    df = pd.read_csv(ENSEMBLE_RAW)

    required_cols = list(EnsembleRowSchema.__annotations__)
    missing = [c for c in required_cols if c not in df.columns]
    assert not missing, f"Missing columns: {missing}"

    assert len(df) > 0, "Ensemble CSV is empty"

    for col in ("efficiency_gap", "mean_median", "declination"):
        nan_count = df[col].isna().sum()
        assert nan_count == 0, f"{col} has {nan_count} NaN values in ensemble CSV"

    assert df["chain"].dtype in (int, "int64", "int32"), "chain column is not integer"


@pytest.mark.skipif(not ENSEMBLE_PCT.exists(), reason="ensemble percentiles CSV not in repo")
def test_ensemble_percentiles_csv_schema():
    """Ensemble percentiles CSV must have metric, map, value, percentile columns."""
    df = pd.read_csv(ENSEMBLE_PCT)
    for col in ("metric", "map", "value", "percentile"):
        assert col in df.columns, f"Missing column: {col}"
    assert len(df) > 0


# ── test_convergence_diagnostics_schema ──────────────────────────────────────

@pytest.mark.skipif(not CONVERGENCE.exists(), reason="convergence diagnostics not in repo")
def test_convergence_diagnostics_schema():
    """Convergence diagnostics JSON must have n_eff for each tracked metric."""
    with open(CONVERGENCE, encoding="utf-8") as fh:
        data = json.load(fh)

    assert isinstance(data, dict), "Convergence diagnostics must be a dict"
    assert len(data) > 0, "Convergence diagnostics is empty"

    for metric, diag in data.items():
        assert_schema(diag, ConvergenceDiagSchema)
        assert diag["n_eff"] > 0, f"{metric}: n_eff must be positive, got {diag['n_eff']}"
        assert not math.isnan(diag["n_eff"]), f"{metric}: n_eff is NaN"


# ── test_joint_outlier_score_schema ──────────────────────────────────────────

@pytest.mark.skipif(not PLACEMENT.exists(), reason="placement output not in repo")
def test_joint_outlier_placement_schema():
    """Final percentile placement JSON must have EG/MM/Dec for each map variant."""
    with open(PLACEMENT, encoding="utf-8") as fh:
        data = json.load(fh)

    assert isinstance(data, dict), "Placement output must be a dict"
    assert len(data) >= 2, "Expected at least 2 map variants in placement output"

    for map_key, entry in data.items():
        assert isinstance(entry, dict), f"{map_key}: entry must be a dict"
        assert_schema(entry, PlacementEntrySchema)

        for metric in ("efficiency_gap", "mean_median", "declination"):
            assert_schema(entry[metric], PlacementMetricSchema)
            rv = entry[metric]["real_value"]
            pct = entry[metric]["percentile"]
            assert not math.isnan(rv), f"{map_key}/{metric}: real_value is NaN"
            assert 0.0 <= pct <= 100.0, f"{map_key}/{metric}: percentile {pct} out of [0, 100]"


# ── test_drain_summary_schema ─────────────────────────────────────────────────

@pytest.mark.skipif(not DRAIN.exists(), reason="drain summary not in repo")
def test_drain_summary_schema():
    """Neighbour drain summary must have majority/minority entries with required fields."""
    with open(DRAIN, encoding="utf-8") as fh:
        data = json.load(fh)

    for map_key in ("majority", "minority"):
        assert map_key in data, f"Missing top-level key: {map_key}"
        assert_schema(data[map_key], DrainMapSchema)
        rate = data[map_key]["chain_signal_rate"]
        assert 0.0 <= rate <= 1.0, f"{map_key}: chain_signal_rate {rate} out of [0, 1]"
