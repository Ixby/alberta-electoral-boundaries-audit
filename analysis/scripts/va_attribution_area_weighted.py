# Version: v0.9
from __future__ import annotations
"""
v0.9 — Area-weighted VA-to-2026-ED attribution (MAUP sensitivity)
=================================================================

Purpose
-------
Provide an MAUP-defensible alternative to the centroid-in-polygon assignment
used by `assignment_va_attribution.py` and `mcmc_ensemble.score_exogenous_map`.

For each VA polygon:
  1. Intersect with every 2026 ED polygon.
  2. weight_i = intersection_area_i / VA_total_area
  3. Apportion the VA's UCP / NDP / other votes proportionally.

Per-VA weights are normalised to sum to ≤ 1.0; any uncovered remainder
(numerical edge or VA polygon extending past the union of EDs) is ignored —
that fraction of votes is not credited to any ED. The script reports the
per-VA-area coverage so this is auditable.

Output
------
A per-ED CSV with (ed_2026, ndp, ucp, other, total, n_va_intersections)
under area-weighted attribution.

Forward
-------
findings/maup_centroid_sensitivity.md  (verdict memo)

Backward
--------
data/shapefiles/derived/va_polygons_with_2023_votes.gpkg  (canonical VA substrate)
data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg
data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg
analysis/scripts/assignment_va_attribution_maup.py  (prior MAUP work — full-vote variant)
analysis/scripts/mcmc_ensemble.py:score_exogenous_map  (centroid baseline being tested)

Type: project
Version: v0.9 (2026-04-26)

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import argparse
import sys
import time
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = data_loader._resolve_path("data")

DEFAULT_VA = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"


def area_weighted_attribution(
    va_gdf: gpd.GeoDataFrame,
    ed_gdf: gpd.GeoDataFrame,
    ed_id_col: str = "name_2026",
    verbose: bool = True,
) -> tuple[pd.DataFrame, dict]:
    """Apportion each VA's votes to 2026 EDs by intersection-area weight.

    Returns (per_ed_df, stats).
    """
    if ed_gdf.crs != va_gdf.crs:
        ed_gdf = ed_gdf.to_crs(va_gdf.crs)

    # Pre-clean geometries.
    va = va_gdf.copy()
    va["geometry"] = va.geometry.buffer(0)
    eds = ed_gdf.copy()
    eds["geometry"] = eds.geometry.buffer(0)

    # Stable per-VA id (some upstream files repeat OBJECTID across map variants).
    va["_va_idx"] = range(len(va))
    va["_va_area"] = va.geometry.area

    if verbose:
        print(f"  overlay: {len(va)} VAs x {len(eds)} EDs ...")
    t0 = time.time()
    inter = gpd.overlay(
        va[["_va_idx", "va_ucp", "va_ndp", "va_other", "_va_area", "geometry"]],
        eds[[ed_id_col, "geometry"]],
        how="intersection",
        keep_geom_type=False,
    )
    inter = inter[inter.geometry.geom_type.isin(["Polygon", "MultiPolygon"])].copy()
    inter["_inter_area"] = inter.geometry.area
    inter = inter[inter["_inter_area"] > 0].copy()
    inter["weight"] = inter["_inter_area"] / inter["_va_area"]
    if verbose:
        print(
            f"    overlay produced {len(inter):,} (VA, ED) rows in {time.time()-t0:.1f}s"
        )

    # Normalise per-VA weights so they sum to 1.0 (eliminates numerical edge
    # leakage where a tiny polygon strip lies just outside the ED union).
    w_sum = inter.groupby("_va_idx")["weight"].transform("sum")
    inter["weight_n"] = inter["weight"] / w_sum.where(w_sum > 0, 1.0)

    # Coverage diagnostics: how much of each VA's area landed inside an ED.
    per_va_cov = inter.groupby("_va_idx")["weight"].sum().rename("cov")
    cov_df = (
        va[["_va_idx", "_va_area"]]
        .merge(per_va_cov, on="_va_idx", how="left")
        .fillna({"cov": 0.0})
    )
    cov_df["cov"] = cov_df["cov"].clip(upper=1.0)
    n_full = int((cov_df["cov"] >= 0.9999).sum())
    n_zero = int((cov_df["cov"] < 1e-6).sum())
    n_part = len(cov_df) - n_full - n_zero
    area_cov = float(
        (cov_df["_va_area"] * cov_df["cov"]).sum() / cov_df["_va_area"].sum()
    )
    if verbose:
        print(
            f"    VA coverage: {n_full} full, {n_part} partial, {n_zero} zero  "
            f"(area-weighted coverage = {area_cov*100:.3f}%)"
        )

    # Nearest-ED fallback for VAs with zero polygon-coverage (matches the
    # centroid pipeline's nearest_ed fallback in assignment_va_attribution.py).
    # Without this, these VAs' votes would be silently dropped, biasing the
    # MAUP comparison vs centroid attribution which DOES place them somewhere.
    n_fallback = 0
    fallback_rows = []
    if n_zero > 0:
        zero_idx = cov_df.loc[cov_df["cov"] < 1e-6, "_va_idx"].tolist()
        zero_va = va[va["_va_idx"].isin(zero_idx)]
        for _, vrow in zero_va.iterrows():
            cent = vrow.geometry.representative_point()
            dists = eds.geometry.distance(cent)
            nearest_ed = eds.iloc[dists.idxmin()][ed_id_col]
            fallback_rows.append(
                {
                    "_va_idx": vrow["_va_idx"],
                    ed_id_col: nearest_ed,
                    "weight_n": 1.0,
                    "ucp": vrow["va_ucp"],
                    "ndp": vrow["va_ndp"],
                    "other": vrow["va_other"],
                    "_inter_area": 0.0,
                    "_va_area": vrow["_va_area"],
                    "weight": 0.0,
                    "va_ucp": vrow["va_ucp"],
                    "va_ndp": vrow["va_ndp"],
                    "va_other": vrow["va_other"],
                }
            )
            n_fallback += 1
        if verbose:
            print(
                f"    nearest-ED fallback applied to {n_fallback} zero-coverage VAs "
                f"(matches centroid pipeline behaviour)"
            )

    # Apportion votes by normalised weight.
    inter["ucp"] = inter["weight_n"] * inter["va_ucp"]
    inter["ndp"] = inter["weight_n"] * inter["va_ndp"]
    inter["other"] = inter["weight_n"] * inter["va_other"]

    # Append fallback rows (already in apportioned form: weight_n=1.0).
    if fallback_rows:
        fb_df = pd.DataFrame(fallback_rows)
        inter = pd.concat([inter, fb_df], ignore_index=True, sort=False)

    # Per-ED aggregation.
    per_ed = inter.groupby(ed_id_col, as_index=False).agg(
        ucp=("ucp", "sum"),
        ndp=("ndp", "sum"),
        other=("other", "sum"),
        n_va_intersections=(ed_id_col, "size"),
    )
    per_ed["total"] = per_ed["ucp"] + per_ed["ndp"] + per_ed["other"]
    per_ed = (
        per_ed.rename(columns={ed_id_col: "ed_2026"})
        .sort_values("ed_2026")
        .reset_index(drop=True)
    )

    # Conservation check: per-VA apportioned totals should equal originals (within numeric floor).
    va_check = va.set_index("_va_idx")[["va_ucp", "va_ndp", "va_other"]]
    ap_check = inter.groupby("_va_idx")[["ucp", "ndp", "other"]].sum()
    joined = va_check.join(ap_check, how="left").fillna(0.0)
    # Rows with zero coverage drop out of attribution → dvotes equals -original on those VAs.
    # Only meaningful for fully-covered VAs.
    full_va = cov_df[cov_df["cov"] >= 0.9999]["_va_idx"].tolist()
    delta_ucp = (
        float((joined.loc[full_va, "ucp"] - joined.loc[full_va, "va_ucp"]).abs().max())
        if full_va
        else 0.0
    )
    delta_ndp = (
        float((joined.loc[full_va, "ndp"] - joined.loc[full_va, "va_ndp"]).abs().max())
        if full_va
        else 0.0
    )

    stats = {
        "n_vas": len(va),
        "n_eds": len(eds),
        "n_overlay_rows": int(len(inter)),
        "n_vas_full_coverage": n_full,
        "n_vas_partial_coverage": n_part,
        "n_vas_zero_coverage": n_zero,
        "n_vas_nearest_ed_fallback": n_fallback,
        "va_area_weighted_coverage": area_cov,
        "max_per_va_ucp_residual_full": delta_ucp,
        "max_per_va_ndp_residual_full": delta_ndp,
        "vote_total_ucp_in": float(va["va_ucp"].sum()),
        "vote_total_ndp_in": float(va["va_ndp"].sum()),
        "vote_total_other_in": float(va["va_other"].sum()),
        "vote_total_ucp_out": float(per_ed["ucp"].sum()),
        "vote_total_ndp_out": float(per_ed["ndp"].sum()),
        "vote_total_other_out": float(per_ed["other"].sum()),
    }
    return per_ed, stats


def main():
    p = argparse.ArgumentParser(description="Area-weighted VA-to-ED vote attribution.")
    p.add_argument(
        "--shapefile",
        required=True,
        type=Path,
        help="Path to the 2026 ED gpkg (e.g. v0_10_topological_majority_2026_eds.gpkg).",
    )
    p.add_argument(
        "--va-shapefile",
        default=DEFAULT_VA,
        type=Path,
        help=f"Path to the VA gpkg (default: {DEFAULT_VA}).",
    )
    p.add_argument(
        "--ed-id-col",
        default="name_2026",
        help="Column on the ED shapefile holding the ED name (default: name_2026).",
    )
    p.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Output CSV path (per-ED area-weighted vote totals).",
    )
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    verbose = not args.quiet
    if verbose:
        print(f"[area-weighted attribution]")
        print(f"  VA shapefile : {args.va_shapefile}")
        print(f"  ED shapefile : {args.shapefile}")
        print(f"  Output CSV   : {args.out}")

    va = gpd.read_file(args.va_shapefile)
    eds = gpd.read_file(args.shapefile)

    per_ed, stats = area_weighted_attribution(
        va, eds, ed_id_col=args.ed_id_col, verbose=verbose
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    per_ed.to_csv(args.out, index=False)
    if verbose:
        print(f"  wrote per-ED CSV: {args.out}  ({len(per_ed)} rows)")
        print(
            f"  in  totals: UCP={stats['vote_total_ucp_in']:,.1f}  NDP={stats['vote_total_ndp_in']:,.1f}  other={stats['vote_total_other_in']:,.1f}"
        )
        print(
            f"  out totals: UCP={stats['vote_total_ucp_out']:,.1f}  NDP={stats['vote_total_ndp_out']:,.1f}  other={stats['vote_total_other_out']:,.1f}"
        )
        ucp_drift = stats["vote_total_ucp_in"] - stats["vote_total_ucp_out"]
        ndp_drift = stats["vote_total_ndp_in"] - stats["vote_total_ndp_out"]
        print(
            f"  drift: ΔUCP={ucp_drift:+.2f}  ΔNDP={ndp_drift:+.2f}  "
            f"(coverage = {stats['va_area_weighted_coverage']*100:.4f}% of VA area)"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
