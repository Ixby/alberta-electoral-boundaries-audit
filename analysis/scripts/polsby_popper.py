# Version: v0.9
"""
polsby_popper.py
=====================
Polsby-Popper compactness for the v0_9 topological VA-dissolve substrate.

The v0_1 numbers (7.1 % minority vs 3.5 % majority below PP 0.25) were
computed before the topological cleanup. v0_1 had three of the five named
"lasso" districts in Tier C (uncomputed), and pixel-tracing in the v0_1
substrate documented inflation of non-compactness (Stony Plain-Drayton
Valley flipped UCP->NDP under v0_1 overlaps, reverted under v0_2 cleanup).
This re-runs PP on the gapless / overlap-free v0_9 substrate so the lasso
claim can be evaluated against numbers that survive the v0_9 substrate.

Dependencies
  Forward  : data/shapefiles/derived/v0_9_topological_minority_2026_eds.gpkg
             data/shapefiles/derived/v0_9_topological_majority_2026_eds.gpkg
  Backward : data/polsby_popper_per_district.csv
             analysis/reports/polsby_popper_verdict.md
"""
# Version: 0.9 series  (last updated 2026-04-26)

from __future__ import annotations

import math
import os
from pathlib import Path

import geopandas as gpd
import pandas as pd

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
MIN_GPKG = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_minority_2026_eds.gpkg"
MAJ_GPKG = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_majority_2026_eds.gpkg"
OUT_CSV = ROOT / "data" / "polsby_popper_per_district.csv"

TARGET_CRS = "EPSG:3401"
PP_THRESHOLD = 0.25

LASSO_NAMED = [
    "Calgary-Nolan Hill-Cochrane",
    "Calgary-Foothills-Airdrie West",
    "Edmonton-Enoch-Devon",
    "Stony Plain-Drayton Valley",
    "Calgary-Airdrie",
]


def polsby_popper(geom) -> float:
    if geom is None or geom.is_empty:
        return float("nan")
    perim = geom.length
    if perim == 0:
        return float("nan")
    return (4.0 * math.pi * geom.area) / (perim * perim)


def score_map(gpkg_path: Path, label: str) -> pd.DataFrame:
    gdf = gpd.read_file(gpkg_path)
    if gdf.crs is None or gdf.crs.to_string() != TARGET_CRS:
        gdf = gdf.to_crs(TARGET_CRS)
    rows = []
    for _, r in gdf.iterrows():
        g = r.geometry
        rows.append({
            "map": label,
            "ed_name": r["name_2026"],
            "area_m2": g.area if g is not None else None,
            "perimeter_m": g.length if g is not None else None,
            "polsby_popper": polsby_popper(g),
        })
    return pd.DataFrame(rows)


def print_summary(label: str, df: pd.DataFrame) -> None:
    pp = df["polsby_popper"].dropna()
    n = len(pp)
    below = int((pp < PP_THRESHOLD).sum())
    pct = (below / n * 100.0) if n else 0.0
    print(f"\n{label}: {n} EDs scored")
    print(f"  PP < {PP_THRESHOLD}: {below}/{n} = {pct:.1f}%")
    print(f"  mean PP={pp.mean():.3f}  median={pp.median():.3f}")
    print(f"  bottom 10 by PP:")
    bot = df.dropna(subset=["polsby_popper"]).nsmallest(10, "polsby_popper")
    for _, r in bot.iterrows():
        print(f"    {r['ed_name']:<45s}  PP={r['polsby_popper']:.3f}")


def print_lasso_lookup(df_all: pd.DataFrame) -> None:
    print("\n" + "=" * 72)
    print("FIVE NAMED LASSO DISTRICTS — v0_9 PP")
    print("=" * 72)
    for name in LASSO_NAMED:
        rows = df_all[df_all["ed_name"] == name]
        if rows.empty:
            print(f"  {name:<45s}  NOT FOUND in either v0_9 map")
            continue
        for _, r in rows.iterrows():
            tag = "below 0.25" if r["polsby_popper"] < PP_THRESHOLD else "above 0.25"
            print(f"  [{r['map']:<8s}] {r['ed_name']:<45s}  PP={r['polsby_popper']:.3f}  ({tag})")


def main() -> None:
    print(f"Loading minority {MIN_GPKG.name}...")
    df_min = score_map(MIN_GPKG, "minority")
    print(f"Loading majority {MAJ_GPKG.name}...")
    df_maj = score_map(MAJ_GPKG, "majority")

    df_all = pd.concat([df_min, df_maj], ignore_index=True)
    df_all.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV} ({len(df_all)} rows)")

    print("\n" + "=" * 72)
    print("v0_9 POLSBY-POPPER SUMMARY")
    print("=" * 72)
    print_summary("MINORITY", df_min)
    print_summary("MAJORITY", df_maj)

    print_lasso_lookup(df_all)


if __name__ == "__main__":
    main()
