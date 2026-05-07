"""Pytest suite for the municipal subdivision split counter.

Tests the logic that aggregates census subdivisions (CSDs) into
electoral districts and properly identifies fragmentation vs cohesion.

Run from the repo root:
    python -m pytest tests/test_municipal_splits.py -v
"""

import sys
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from municipal_splits import count_splits

# ============================================================
# Municipal splits logic tests
# ============================================================


def test_count_splits_single():
    """A CSD fully inside one ED should report 1 district."""
    csd = Polygon([(1, 1), (2, 1), (2, 2), (1, 2)])
    ed1 = Polygon([(0, 0), (3, 0), (3, 3), (0, 3)])

    csds = gpd.GeoDataFrame(
        {"CSDNAME": ["TownA"], "CSDTYPE": ["T"]}, geometry=[csd], crs="EPSG:3401"
    )
    eds = gpd.GeoDataFrame({"name_2026": ["ED1"]}, geometry=[ed1], crs="EPSG:3401")

    result = count_splits(csds, eds, "test", min_overlap_m2=0.0)

    assert len(result) == 1
    assert result.iloc[0]["n_eds"] == 1
    assert result.iloc[0]["eds"] == "ED1"


def test_count_splits_multiple():
    """A CSD crossing the boundary of two EDs should report 2 districts."""
    csd = Polygon([(1, 1), (3, 1), (3, 2), (1, 2)])
    ed1 = Polygon([(0, 0), (2, 0), (2, 3), (0, 3)])
    ed2 = Polygon([(2, 0), (4, 0), (4, 3), (2, 3)])

    csds = gpd.GeoDataFrame(
        {"CSDNAME": ["TownB"], "CSDTYPE": ["T"]}, geometry=[csd], crs="EPSG:3401"
    )
    eds = gpd.GeoDataFrame(
        {"name_2026": ["ED1", "ED2"]}, geometry=[ed1, ed2], crs="EPSG:3401"
    )

    result = count_splits(csds, eds, "test", min_overlap_m2=0.0)

    assert len(result) == 1
    assert result.iloc[0]["n_eds"] == 2
    assert "ED1" in result.iloc[0]["eds"]
    assert "ED2" in result.iloc[0]["eds"]


def test_count_splits_min_overlap_filtering():
    """A CSD spanning two EDs but only grazing one by a tiny sliver
    should filter out the sliver if below the area threshold.
    """
    csd = Polygon([(1, 1), (2.1, 1), (2.1, 2), (1, 2)])
    ed1 = Polygon([(0, 0), (2, 0), (2, 3), (0, 3)])
    ed2 = Polygon([(2, 0), (4, 0), (4, 3), (2, 3)])

    csds = gpd.GeoDataFrame(
        {"CSDNAME": ["TownC"], "CSDTYPE": ["T"]}, geometry=[csd], crs="EPSG:3401"
    )
    eds = gpd.GeoDataFrame(
        {"name_2026": ["ED1", "ED2"]}, geometry=[ed1, ed2], crs="EPSG:3401"
    )

    # Overlap with ED2 is only 0.1, threshold is 0.5
    result = count_splits(csds, eds, "test", min_overlap_m2=0.5)

    assert len(result) == 1
    assert result.iloc[0]["n_eds"] == 1
    assert result.iloc[0]["eds"] == "ED1"
