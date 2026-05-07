"""Pytest suite for the population consistency cross-checker.

Tests the spatial join logic that aggregates Census Dissemination Area
(DA) populations to Electoral Districts to verify boundary alignments.

Run from the repo root:
    python -m pytest tests/test_population_consistency.py -v
"""

import sys
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from population_consistency import da_pop_by_ed

# ============================================================
# Population spatial-aggregation tests
# ============================================================


def test_da_pop_by_ed():
    """DA populations should sum correctly to their enclosing EDs."""
    ed1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    ed2 = Polygon([(2, 0), (4, 0), (4, 2), (2, 2)])
    eds = gpd.GeoDataFrame(
        {"name": ["ED1", "ED2"]}, geometry=[ed1, ed2], crs="EPSG:3401"
    )

    da1 = Point(1, 1).buffer(0.1)
    da2 = Point(1.5, 1).buffer(0.1)
    da3 = Point(3, 1).buffer(0.1)

    das = gpd.GeoDataFrame(
        {"DAUID": ["1", "2", "3"], "population_2021": [100.0, 50.0, 200.0]},
        geometry=[da1, da2, da3],
        crs="EPSG:3401",
    )

    res = da_pop_by_ed(eds, "name", das, target_crs=None)

    assert res["ED1"] == 150.0
    assert res["ED2"] == 200.0


def test_da_pop_by_ed_unassigned_da():
    """DAs strictly outside any ED should not contribute to any district."""
    ed1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    eds = gpd.GeoDataFrame({"name": ["ED1"]}, geometry=[ed1], crs="EPSG:3401")

    da1 = Point(1, 1).buffer(0.1)
    da2 = Point(10, 10).buffer(0.1)

    das = gpd.GeoDataFrame(
        {"DAUID": ["1", "2"], "population_2021": [100.0, 50.0]},
        geometry=[da1, da2],
        crs="EPSG:3401",
    )

    res = da_pop_by_ed(eds, "name", das, target_crs=None)

    assert res["ED1"] == 100.0


def test_da_pop_by_ed_empty_ed():
    """EDs containing no DAs should gracefully report 0.0 population."""
    ed1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    eds = gpd.GeoDataFrame({"name": ["ED1"]}, geometry=[ed1], crs="EPSG:3401")

    da1 = Point(10, 10).buffer(0.1)

    das = gpd.GeoDataFrame(
        {"DAUID": ["1"], "population_2021": [100.0]}, geometry=[da1], crs="EPSG:3401"
    )

    res = da_pop_by_ed(eds, "name", das, target_crs=None)

    assert res["ED1"] == 0.0
