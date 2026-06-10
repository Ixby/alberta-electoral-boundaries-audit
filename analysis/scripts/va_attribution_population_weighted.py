# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta + StatsCan (public domain) | https://ixby.github.io
"""
va_attribution_population_weighted.py — Population-weighted VA→ED attribution
===============================================================================

The most rigorous attribution method available without polling-station-level
geocoding. For each VA polygon and each ED polygon it intersects:

  1. Overlay VA × ED → intersection slivers
  2. Overlay each sliver with 2021 DA polygons → DA-slivers
  3. weight_i = (population of DA-sliver) / (population of full VA)
  4. Apportion the VA's UCP / NDP / other votes proportionally to weight_i

This matters where VAs straddle ED boundaries with uneven population
distribution — a VA half-empty pasture and half-small-town should not split
votes 50/50; almost all votes are in the town. Area-weighted MAUP misses
this; centroid-in-polygon misses it; population-weighted MAUP catches it.

Inputs
------
--shapefile PATH      Candidate ED shapefile (.gpkg). Default canonical
                      majority.
--va-shapefile PATH   VA polygons with 2023 votes. Default canonical.
--da-shapefile PATH   2021 census DA polygons. Default
                      data/shapefiles/reference/alberta_2021_das.gpkg.
--da-pop-col STRING   Column name for DA population (default: pop_2021).
--ed-id-col STRING    ED name column (default: EDName2025).
--out PATH            Per-ED CSV.

Output: per-ED CSV with (ed_2026, ndp, ucp, other, total,
n_va_intersections, pop_attributed_frac).

Backward:
  data/shapefiles/canonical/va_2023_election_day_votes.gpkg
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/reference/alberta_2021_das.gpkg
Forward:
  data/outputs/pop_weighted_canonical_<map>.csv
  findings/maup_attribution_canonical.md
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent


def population_weighted_attribution(
    va: gpd.GeoDataFrame,
    eds: gpd.GeoDataFrame,
    das: gpd.GeoDataFrame,
    ed_id_col: str = "EDName2025",
    da_pop_col: str = "pop_2021",
    verbose: bool = True,
) -> tuple[pd.DataFrame, dict]:
    """Population-weighted VA→ED attribution. Three-way overlay (VA × ED × DA)."""
    t0 = time.time()
    va = va.copy()
    eds = eds.copy()
    das = das.copy()
    # Reproject DAs and EDs into VA CRS
    if eds.crs != va.crs:
        eds = eds.to_crs(va.crs)
    if das.crs != va.crs:
        das = das.to_crs(va.crs)
    va["va_idx"] = range(len(va))
    eds["ed_idx"] = range(len(eds))
    das["da_idx"] = range(len(das))

    # Step 1: VA × ED overlay (intersection slivers)
    if verbose:
        print(f"  overlay 1/2: {len(va)} VAs x {len(eds)} EDs ...")
    sliver = gpd.overlay(va[["va_idx", "geometry"]], eds[["ed_idx", "geometry"]],
                        how="intersection", keep_geom_type=False)
    sliver = sliver[sliver.geometry.area > 0]
    if verbose:
        print(f"    VA×ED slivers: {len(sliver):,}  ({time.time()-t0:.1f}s)")

    # Step 2: VA×ED slivers × DA overlay → DA-slivers
    if verbose:
        print(f"  overlay 2/2: {len(sliver):,} VA×ED slivers x {len(das)} DAs ...")
    t1 = time.time()
    da_slivers = gpd.overlay(
        sliver, das[["da_idx", da_pop_col, "geometry"]],
        how="intersection", keep_geom_type=False,
    )
    da_slivers = da_slivers[da_slivers.geometry.area > 0]
    if verbose:
        print(f"    DA slivers: {len(da_slivers):,}  ({time.time()-t1:.1f}s)")

    # Step 3: per (VA, ED, DA) sliver, compute pop = DA_pop × (sliver_area / DA_area)
    # We have DA_idx so look up DA total area
    da_area = das.set_index("da_idx").geometry.area
    da_slivers["sliver_area"] = da_slivers.geometry.area
    da_slivers["da_total_area"] = da_slivers["da_idx"].map(da_area)
    da_slivers["sliver_pop"] = da_slivers[da_pop_col] * (
        da_slivers["sliver_area"] / da_slivers["da_total_area"].clip(lower=1.0)
    )

    # Step 4: per (VA, ED) sliver — sum sliver populations to get sliver_pop_total
    va_ed_pop = da_slivers.groupby(["va_idx", "ed_idx"], as_index=False)["sliver_pop"].sum()

    # Step 5: per VA — total pop across all its (VA, ED) slivers
    va_pop_total = va_ed_pop.groupby("va_idx")["sliver_pop"].sum().rename("va_pop_total")
    va_ed_pop = va_ed_pop.merge(va_pop_total, on="va_idx", how="left")
    va_ed_pop["weight"] = va_ed_pop["sliver_pop"] / va_ed_pop["va_pop_total"].clip(lower=1.0)

    # Step 6: attribute votes per (VA, ED) by weight × VA votes
    va_votes = va.set_index("va_idx")[["va_ucp", "va_ndp", "va_other"]] if "va_other" in va.columns else \
               va.set_index("va_idx")[["va_ucp", "va_ndp"]].assign(va_other=0)
    for col in ("va_ucp", "va_ndp", "va_other"):
        va_ed_pop[col] = va_ed_pop["va_idx"].map(va_votes[col].fillna(0))
        va_ed_pop[f"attr_{col[3:]}"] = va_ed_pop[col] * va_ed_pop["weight"]

    # Step 7: aggregate per ED
    per_ed = va_ed_pop.groupby("ed_idx")[["attr_ucp", "attr_ndp", "attr_other"]].sum().reset_index()
    per_ed = per_ed.merge(eds[["ed_idx", ed_id_col]], on="ed_idx", how="left")
    per_ed["total"] = per_ed["attr_ucp"] + per_ed["attr_ndp"] + per_ed["attr_other"]
    per_ed = per_ed.rename(columns={
        ed_id_col: "ed_2026",
        "attr_ucp": "ucp",
        "attr_ndp": "ndp",
        "attr_other": "other",
    })

    # Diagnostics
    in_ucp = float(va["va_ucp"].sum())
    in_ndp = float(va["va_ndp"].sum())
    out_ucp = float(per_ed["ucp"].sum())
    out_ndp = float(per_ed["ndp"].sum())
    pop_attr_frac = float(va_ed_pop.groupby("va_idx")["weight"].sum().mean())

    stats = {
        "in_ucp": in_ucp,
        "in_ndp": in_ndp,
        "out_ucp": out_ucp,
        "out_ndp": out_ndp,
        "drift_ucp": out_ucp - in_ucp,
        "drift_ndp": out_ndp - in_ndp,
        "mean_va_weight_sum": pop_attr_frac,
        "n_va_ed_slivers": len(va_ed_pop),
        "n_da_slivers": len(da_slivers),
        "total_seconds": time.time() - t0,
    }
    return per_ed.drop(columns=["ed_idx"]), stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--shapefile", type=Path,
                    default=ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg")
    ap.add_argument("--va-shapefile", type=Path,
                    default=ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg")
    ap.add_argument("--da-shapefile", type=Path,
                    default=ROOT / "data/shapefiles/reference/alberta_2021_das.gpkg")
    ap.add_argument("--ed-id-col", default="EDName2025")
    ap.add_argument("--da-pop-col", default="pop_2021")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    verbose = not args.quiet
    if verbose:
        print(f"[population-weighted attribution]")
        print(f"  VA shapefile : {args.va_shapefile.name}")
        print(f"  ED shapefile : {args.shapefile.name}")
        print(f"  DA shapefile : {args.da_shapefile.name}")
        print(f"  Output CSV   : {args.out}")

    va = gpd.read_file(args.va_shapefile)
    eds = gpd.read_file(args.shapefile)
    das = gpd.read_file(args.da_shapefile)
    # Heuristic DA-pop detection
    if args.da_pop_col not in das.columns:
        candidates = [c for c in das.columns if "pop" in c.lower()]
        if candidates:
            args.da_pop_col = candidates[0]
            if verbose:
                print(f"  auto-detected DA pop column: {args.da_pop_col}")
        else:
            # No pop on the shapefile — try the reference CSV join (DAUID-keyed)
            ref_csv = ROOT / "data/reference/alberta_2021_da_populations.csv"
            if "DAUID" in das.columns and ref_csv.exists():
                pop_df = pd.read_csv(ref_csv, dtype={"DAUID": str})
                pop_col_name = [c for c in pop_df.columns if "pop" in c.lower()][0]
                pop_df = pop_df.rename(columns={pop_col_name: "pop_2021"})
                das["DAUID"] = das["DAUID"].astype(str)
                das = das.merge(pop_df[["DAUID", "pop_2021"]], on="DAUID", how="left")
                das["pop_2021"] = das["pop_2021"].fillna(0.0)
                args.da_pop_col = "pop_2021"
                if verbose:
                    print(f"  joined DA pop from {ref_csv.name}")
            else:
                print(f"ERROR: no pop column in DA shapefile; got {list(das.columns)}", file=sys.stderr)
                return 2

    per_ed, stats = population_weighted_attribution(
        va, eds, das, ed_id_col=args.ed_id_col, da_pop_col=args.da_pop_col, verbose=verbose
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    per_ed.to_csv(args.out, index=False)
    if verbose:
        print(f"  wrote per-ED CSV: {args.out}  ({len(per_ed)} rows)")
        print(f"  in totals:  UCP={stats['in_ucp']:,.1f}  NDP={stats['in_ndp']:,.1f}")
        print(f"  out totals: UCP={stats['out_ucp']:,.1f}  NDP={stats['out_ndp']:,.1f}")
        print(f"  drift: ΔUCP={stats['drift_ucp']:+.1f}  ΔNDP={stats['drift_ndp']:+.1f}  "
              f"(mean VA weight sum = {stats['mean_va_weight_sum']:.4f}; ideal = 1.0)")
        print(f"  total time: {stats['total_seconds']:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
