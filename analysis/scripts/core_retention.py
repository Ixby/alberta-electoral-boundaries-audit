"""Core Retention Analysis (Incumbent Displacement)

Calculates the core retention of electoral districts between two maps.
Core retention is the percentage of a new district's population that comes
from a single old district, or the percentage of an old district's population
that moves to a new district. This is used to detect "hijacking" or
"kidnapping" gerrymanders.
"""

import pandas as pd
import geopandas as gpd


def compute_core_retention_by_area(
    old_eds: gpd.GeoDataFrame,
    new_eds: gpd.GeoDataFrame,
    old_name_col: str,
    new_name_col: str,
) -> pd.DataFrame:
    """
    Computes area-based core retention. For each new ED, calculates what %
    of its area came from which old EDs, and vice versa.

    Returns a DataFrame of intersections with 'retention_of_old' and 'makeup_of_new'.
    """
    old_p = old_eds.to_crs(new_eds.crs).copy()
    old_p["old_area"] = old_p.geometry.area

    new_p = new_eds.copy()
    new_p["new_area"] = new_p.geometry.area

    # Intersect old and new polygons
    intersect = gpd.overlay(
        new_p[[new_name_col, "new_area", "geometry"]],
        old_p[[old_name_col, "old_area", "geometry"]],
        how="intersection",
        keep_geom_type=True,
    )

    intersect["intersect_area"] = intersect.geometry.area

    # Calculate ratios
    intersect["retention_of_old"] = intersect["intersect_area"] / intersect["old_area"]
    intersect["makeup_of_new"] = intersect["intersect_area"] / intersect["new_area"]

    return pd.DataFrame(intersect.drop(columns=["geometry"]))
