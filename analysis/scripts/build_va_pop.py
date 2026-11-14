# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
"""
build_va_pop.py — 2021 census population per voting area, by area-weighted overlay.

Builds data/va_pop_from_das.csv, the population weight that build_va_graph()
gives every voting area (VA) and that every ensemble balances on.

Method
------
Each 2021 dissemination area (DA) is intersected with the 4,765 voting-area
polygons, in the VA layer's projection (EPSG:3400). A DA's population is shared
out among the VAs it overlaps in proportion to area:

    pop(VA) = sum over DAs of  population(DA) * area(DA ∩ VA) / area(DA)

Population that falls outside every VA polygon is not assigned (the province
total in the output is 4,262,567 of the DAs' 4,262,635).

The committed file predates this script: it was produced in April 2026 by code
that was never committed. This script was written afterwards and reproduces
the committed file to within 1e-8 persons in every row (largest difference
5e-9). It therefore documents the method and lets anyone check the file; it
is not the code that first wrote it.

Usage
-----
    python analysis/scripts/build_va_pop.py            # rebuild and COMPARE with the committed file
    python analysis/scripts/build_va_pop.py --write    # rebuild and overwrite data/va_pop_from_das.csv

The default only compares, because a rewrite changes the committed file in the
ninth decimal place and would alter its hash for no reason.

Backward:
  data/shapefiles/reference/alberta_2021_das.gpkg   (Git LFS; DA polygons, EPSG:3347)
  data/reference/alberta_2021_da_populations.csv    (2021 census population by DAUID)
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg (Git LFS; row order defines va_row_idx)
Forward:
  data/va_pop_from_das.csv  (read by mcmc_ensemble.build_va_graph)
  data/outputs/va_pop_from_das.csv  (a byte-identical second copy; attribution_sensitivity_check.py reads it)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DA_GPKG = ROOT / "data" / "shapefiles" / "reference" / "alberta_2021_das.gpkg"
DA_POP = ROOT / "data" / "reference" / "alberta_2021_da_populations.csv"
VA_GPKG = ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
OUT = ROOT / "data" / "va_pop_from_das.csv"
TOLERANCE = 1e-6  # persons


def build(da_gpkg: Path = DA_GPKG, da_pop: Path = DA_POP, va_gpkg: Path = VA_GPKG) -> pd.DataFrame:
    """Return a DataFrame with columns va_row_idx, pop_2021 (one row per VA, in file order)."""
    va = gpd.read_file(va_gpkg)[["geometry"]].reset_index(names="va_row_idx")
    da = gpd.read_file(da_gpkg)[["DAUID", "geometry"]]
    pop = pd.read_csv(da_pop, dtype={"DAUID": str})[["DAUID", "population_2021"]]
    da = da.merge(pop, on="DAUID", how="left")
    da["population_2021"] = pd.to_numeric(da["population_2021"], errors="coerce").fillna(0.0)
    da = da.to_crs(va.crs)                      # areas are measured in the VA layer's projection
    da["da_area"] = da.geometry.area
    pieces = gpd.overlay(da, va, how="intersection", keep_geom_type=True)
    share = pieces.geometry.area / pieces["da_area"]
    pop_va = (pieces["population_2021"] * share).groupby(pieces["va_row_idx"]).sum()
    pop_va = pop_va.reindex(range(len(va))).fillna(0.0)
    return pd.DataFrame({"va_row_idx": range(len(va)), "pop_2021": pop_va.to_numpy()})


def compare(built: pd.DataFrame, committed_path: Path = OUT) -> float:
    """Largest absolute difference (persons) between a rebuild and the committed file."""
    committed = pd.read_csv(committed_path)
    if len(committed) != len(built) or not (committed["va_row_idx"].values == built["va_row_idx"].values).all():
        raise ValueError(f"{committed_path} does not have the same rows as the rebuild")
    return float((committed["pop_2021"] - built["pop_2021"]).abs().max())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help=f"overwrite {OUT.relative_to(ROOT)}")
    args = ap.parse_args(argv)
    built = build()
    print(f"rebuilt {len(built):,} voting areas; total population {built['pop_2021'].sum():,.1f}")
    if args.write:
        built.to_csv(OUT, index=False)
        print(f"wrote {OUT.relative_to(ROOT)}")
        return 0
    worst = compare(built)
    print(f"largest difference from committed {OUT.relative_to(ROOT)}: {worst:.3g} persons")
    if worst > TOLERANCE:
        print(f"FAIL: above the {TOLERANCE:g} tolerance")
        return 1
    print("OK: the committed file is reproduced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
