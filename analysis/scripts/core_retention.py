"""Compute core-retention and constituency-makeup fractions via polygon overlay.

Backward:
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
Forward:
  # Returns retention/makeup DataFrame to caller — no file output.
"""
from __future__ import annotations

import geopandas as gpd
import pandas as pd


def compute_core_retention_by_area(
    old_eds: gpd.GeoDataFrame,
    new_eds: gpd.GeoDataFrame,
    old_col: str,
    new_col: str,
) -> pd.DataFrame:
    """Return retention and makeup fractions for every (old, new) ED pair.

    Parameters
    ----------
    old_eds : GeoDataFrame — old district map with column ``old_col`` + geometry.
    new_eds : GeoDataFrame — new district map with column ``new_col`` + geometry.
    old_col : Column name holding the district identifier in ``old_eds``.
    new_col : Column name holding the district identifier in ``new_eds``.

    Returns
    -------
    DataFrame with one row per (old, new) pair that has non-zero intersection:
      - ``retention_of_old`` : intersection_area / old_area  (0–1)
      - ``makeup_of_new``    : intersection_area / new_area  (0–1)
    """
    old_with_area = old_eds[[old_col, "geometry"]].copy()
    old_with_area["_old_area"] = old_with_area.geometry.area

    new_with_area = new_eds[[new_col, "geometry"]].copy()
    new_with_area["_new_area"] = new_with_area.geometry.area

    intersection = gpd.overlay(
        old_with_area,
        new_with_area,
        how="intersection",
        keep_geom_type=False,
    )
    intersection["_int_area"] = intersection.geometry.area
    intersection = intersection[intersection["_int_area"] > 0].copy()

    intersection["retention_of_old"] = (
        intersection["_int_area"] / intersection["_old_area"]
    )
    intersection["makeup_of_new"] = (
        intersection["_int_area"] / intersection["_new_area"]
    )

    return intersection[
        [old_col, new_col, "retention_of_old", "makeup_of_new"]
    ].reset_index(drop=True)
