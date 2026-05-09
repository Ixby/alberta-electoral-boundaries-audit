"""
pipeline_schemas.py — TypedDict schemas for pipeline stage output validation.

Forward dependencies: none
Backward dependencies: test_pipeline_integration.py
"""
from __future__ import annotations

from typing import TypedDict

__all__ = [
    "EnsembleRowSchema",
    "ConvergenceDiagSchema",
    "PlacementMetricSchema",
    "PlacementEntrySchema",
    "DrainMapSchema",
    "assert_schema",
]


class EnsembleRowSchema(TypedDict):
    efficiency_gap: float
    mean_median: float
    declination: float
    chain: int


class ConvergenceDiagSchema(TypedDict):
    n: int
    tau: float
    n_eff: float
    max_lag_used: int


class PlacementMetricSchema(TypedDict):
    real_value: float
    percentile: float
    ensemble_p50: float


class PlacementEntrySchema(TypedDict):
    efficiency_gap: PlacementMetricSchema
    mean_median: PlacementMetricSchema
    declination: PlacementMetricSchema


class DrainMapSchema(TypedDict):
    n_eds: int
    n_undirected_pairs: int
    chain_signal_rate: float


def assert_schema(data: dict, schema_class: type) -> None:
    """Assert data contains all required keys from schema_class.__annotations__.

    Raises AssertionError with a descriptive message on missing keys.
    Does not enforce exact key equality — extra keys in data are allowed.
    """
    required = set(schema_class.__annotations__)
    missing = required - set(data)
    assert not missing, (
        f"{schema_class.__name__}: missing keys {sorted(missing)}. "
        f"Got: {sorted(data)}"
    )
