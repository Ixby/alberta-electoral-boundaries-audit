"""Pytest suite for Core Retention / Incumbent Displacement metrics.

Tests the intersection overlay logic that determines how much of an old
district is retained in a new map.

Run from the repo root:
    python -m pytest tests/test_core_retention.py -v
"""

import sys
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import pytest
import math

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from core_retention import compute_core_retention_by_area

# ============================================================
# Core Retention overlay tests
# ============================================================


def test_core_retention_perfect_match():
    """If the old and new boundaries are identical, retention is 100%."""
    poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    old_eds = gpd.GeoDataFrame({"old_name": ["ED1"]}, geometry=[poly], crs="EPSG:3401")
    new_eds = gpd.GeoDataFrame(
        {"new_name": ["ED1_NEW"]}, geometry=[poly], crs="EPSG:3401"
    )

    res = compute_core_retention_by_area(old_eds, new_eds, "old_name", "new_name")
    assert len(res) == 1
    assert math.isclose(res.iloc[0]["retention_of_old"], 1.0)
    assert math.isclose(res.iloc[0]["makeup_of_new"], 1.0)


def test_core_retention_split():
    """If an old ED is split perfectly in half, retention drops to 50%."""
    poly_old = Polygon([(0, 0), (4, 0), (4, 2), (0, 2)])
    poly_new1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    poly_new2 = Polygon([(2, 0), (4, 0), (4, 2), (2, 2)])

    old_eds = gpd.GeoDataFrame(
        {"old_name": ["ED_OLD"]}, geometry=[poly_old], crs="EPSG:3401"
    )
    new_eds = gpd.GeoDataFrame(
        {"new_name": ["NEW1", "NEW2"]}, geometry=[poly_new1, poly_new2], crs="EPSG:3401"
    )

    res = compute_core_retention_by_area(old_eds, new_eds, "old_name", "new_name")
    assert len(res) == 2

    res_sorted = res.sort_values("new_name").reset_index(drop=True)
    # The old ED was split equally, so each new piece has 50% of the old ED
    assert math.isclose(res_sorted.iloc[0]["retention_of_old"], 0.5)
    assert math.isclose(res_sorted.iloc[1]["retention_of_old"], 0.5)

    # However, each new ED is entirely made up of the old ED (100% makeup)
    assert math.isclose(res_sorted.iloc[0]["makeup_of_new"], 1.0)
    assert math.isclose(res_sorted.iloc[1]["makeup_of_new"], 1.0)
