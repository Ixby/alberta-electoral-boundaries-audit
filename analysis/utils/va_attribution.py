"""
va_attribution.py — Canonical VA→ED attribution helper.

T1.14 closed 2026-06-12 per T1.7 R1 Ref #3 D7. Three "identical" attribution
implementations existed across the codebase with subtle but real differences
in how they handled boundary VAs and unresolved centroids:

  - phase4c_canonical_attribution.py:84-95 — uses sjoin_nearest as fallback
    for VAs whose representative_point() fell outside every ED polygon.
    No tie-break for multi-ED containment; relies on join order.

  - mcmc_ensemble.py:334-339 — drops unresolved (NaN ED_NAME) rows entirely
    and de-duplicates with `keep="first"` (which resolves multi-ED
    containment by join order — nondeterministic when sjoin returns
    multiple matches for a single centroid).

  - packing_cracking_analysis.py:297-298 — same as mcmc_ensemble.py;
    no nearest fallback; nondeterministic tie-break.

This unified helper:
  1. Uses `representative_point()` centroid-in-polygon as the primary attribution.
  2. Applies `sjoin_nearest` fallback for unresolved centroids (matches phase4c).
  3. Resolves multi-ED containment deterministically by the *largest intersection
     area* between the VA polygon and each candidate ED (replaces the
     nondeterministic `keep="first"`).
  4. Asserts CRS-equality between VA layer and ED layer at the sjoin site
     (catches the 500 km easting hazard from T4.10-CRS).
  5. Logs vote conservation: prints n_va_votes_total and n_attributed_total,
     warns on > 0.01% loss.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path
from typing import Optional

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent


def _assert_crs_match(va_gdf: gpd.GeoDataFrame, ed_gdf: gpd.GeoDataFrame) -> None:
    """Catch the 500 km easting hazard before sjoin silently misregisters."""
    from pyproj import CRS
    if va_gdf.crs is None or ed_gdf.crs is None:
        raise ValueError("va_attribution: CRS must not be None on either input")
    if not CRS.from_user_input(va_gdf.crs).equals(CRS.from_user_input(ed_gdf.crs)):
        raise ValueError(
            f"va_attribution: VA CRS={va_gdf.crs} does not match ED CRS={ed_gdf.crs}. "
            "Reproject one side before calling. EPSG:3400 and 3401 differ by 500,000 m "
            "of false easting and will produce nonsense overlay results when mixed."
        )


def attribute(
    va_gdf: gpd.GeoDataFrame,
    ed_gdf: gpd.GeoDataFrame,
    ed_name_col: str,
    *,
    ucp_col: str = "va_ucp",
    ndp_col: str = "va_ndp",
    nearest_fallback: bool = True,
    verbose: bool = False,
) -> pd.DataFrame:
    """Return a DataFrame with columns [ed_name_col, 'ndp', 'ucp', 'total'].

    Parameters
    ----------
    va_gdf : GeoDataFrame with VA polygons + `ucp_col` / `ndp_col` vote columns
    ed_gdf : GeoDataFrame with ED polygons + `ed_name_col`
    ed_name_col : str
        Name of the ED-name column in `ed_gdf` (e.g. 'EDName2025', 'EDName2017')
    nearest_fallback : bool
        If True, unresolved VA centroids (outside every ED polygon) are attached
        to the nearest ED via sjoin_nearest. If False, unresolved rows are
        dropped (matches `mcmc_ensemble.py` / `packing_cracking_analysis.py`
        legacy behavior).
    """
    _assert_crs_match(va_gdf, ed_gdf)

    centroids = va_gdf.copy()
    centroids["geometry"] = va_gdf.geometry.representative_point()
    eds = ed_gdf[[ed_name_col, "geometry"]].copy()

    # Primary attribution: centroid within ED polygon
    joined = gpd.sjoin(
        centroids[[ucp_col, ndp_col, "geometry"]],
        eds,
        how="left",
        predicate="within",
    )

    n_va = len(centroids)
    n_unresolved = int(joined[ed_name_col].isna().sum())

    if n_unresolved > 0 and nearest_fallback:
        unresolved = joined[ed_name_col].isna()
        nearest = gpd.sjoin_nearest(
            centroids.loc[unresolved.values][[ucp_col, ndp_col, "geometry"]],
            eds,
            how="left",
            distance_col="_nearest_dist_m",
        )
        # In case sjoin_nearest produces ties (equidistant), keep the first
        # deterministically — but log it.
        nearest = nearest[~nearest.index.duplicated(keep="first")]
        joined.loc[unresolved.values, ed_name_col] = nearest[ed_name_col].values

    # Deterministic multi-ED tie-break: if sjoin returns multiple matches for
    # one centroid (rare, only when polygons overlap or share boundaries), keep
    # the row whose ED has the larger intersection area with the original VA
    # polygon. Replaces the nondeterministic `keep="first"` of legacy scripts.
    dup_mask = joined.index.duplicated(keep=False)
    if dup_mask.any():
        n_dup = int(dup_mask.sum())
        # Compute intersection area for each duplicate row
        dup_idx = joined.index[dup_mask].unique()
        keepers = []
        va_geoms = va_gdf.geometry
        for i in dup_idx:
            candidates = joined.loc[[i]]
            best_idx = None
            best_area = -1.0
            for row_pos, row in candidates.iterrows():
                ed_name = row[ed_name_col]
                if pd.isna(ed_name):
                    continue
                ed_poly = eds.loc[eds[ed_name_col] == ed_name, "geometry"].iloc[0]
                try:
                    area = float(va_geoms.iloc[i].intersection(ed_poly).area)
                except Exception:
                    area = 0.0
                if area > best_area:
                    best_area = area
                    best_idx = row_pos
            if best_idx is not None:
                keepers.append(best_idx)
        # Drop other duplicates
        joined = joined.drop(joined.index[dup_mask].difference(keepers))
        if verbose:
            print(f"    Multi-ED tie-break: {n_dup} duplicate rows resolved by largest intersection area")

    # Final: aggregate
    n_attributed = int(joined[ed_name_col].notna().sum())
    if verbose:
        print(f"  va_attribution: {n_attributed}/{n_va} VAs attributed "
              f"({n_unresolved} required nearest fallback)")

    joined = joined.dropna(subset=[ed_name_col])
    agg = (
        joined.groupby(ed_name_col)
        .agg(ndp=(ndp_col, "sum"), ucp=(ucp_col, "sum"))
        .reset_index()
    )
    agg["total"] = agg["ndp"] + agg["ucp"]

    # Vote conservation
    total_va = float(va_gdf[ucp_col].sum() + va_gdf[ndp_col].sum())
    total_attr = float(agg["total"].sum())
    loss_pct = 100.0 * (total_va - total_attr) / total_va if total_va > 0 else 0.0
    if abs(loss_pct) > 0.01:
        warnings.warn(
            f"va_attribution: vote conservation lost {loss_pct:.4f}% "
            f"(VA total {total_va:.0f}, attributed {total_attr:.0f}). "
            "Check nearest_fallback / multi-ED tie-break behaviour."
        )

    return agg


__all__ = ["attribute"]
