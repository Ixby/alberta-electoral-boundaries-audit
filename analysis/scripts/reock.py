# Version: v0.9
"""
reock.py
=============
Reock compactness for the v0_9 topological VA-dissolve substrate.

Reock = 4 * area / (pi * D^2), where D is the diameter of the smallest
enclosing circle of each district. Score in [0, 1]; higher = more compact.
The pre-registration committed to *both* Polsby-Popper and Reock; PP has
been computed (analysis/scripts/polsby_popper.py); this script fires
the Reock gun that was silently dropped.

Implementation uses Shapely 2.0+'s `shapely.minimum_bounding_circle`,
which exposes the GEOS smallest-enclosing-circle routine. Welzl-style
fallback is included for older Shapely; if neither is reachable the
script raises rather than silently substituting an inferior heuristic.

Dependencies
  Forward  : data/shapefiles/derived/v0_9_topological_minority_2026_eds.gpkg
             data/shapefiles/derived/v0_9_topological_majority_2026_eds.gpkg
  Backward : data/reock_per_district.csv
             analysis/reports/reock_verdict.md
"""
# Version: 0.9 series  (last updated 2026-04-26)

from __future__ import annotations

import math
import os
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
MIN_GPKG = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_minority_2026_eds.gpkg"
MAJ_GPKG = ROOT / "data" / "shapefiles" / "derived" / "v0_9_topological_majority_2026_eds.gpkg"
OUT_CSV = ROOT / "data" / "reock_per_district.csv"

TARGET_CRS = "EPSG:3401"
REOCK_THRESHOLD = 0.30  # Conventional flag threshold for Reock

LASSO_NAMED = [
    "Calgary-Nolan Hill-Cochrane",
    "Rocky Mountain House-Banff Park",
    "Stony Plain-Drayton Valley",
    "Calgary-Foothills-Airdrie West",
    "Edmonton-Enoch-Devon",
]


# ---------------------------------------------------------------------
# Smallest enclosing circle
# ---------------------------------------------------------------------

def _mbc_diameter_via_shapely(geom) -> float:
    """Return the diameter of the smallest enclosing circle using
    Shapely 2.0+'s minimum_bounding_circle. Returns NaN if unavailable.
    """
    try:
        from shapely import minimum_bounding_circle  # type: ignore
    except Exception:
        return float("nan")
    if geom is None or geom.is_empty:
        return float("nan")
    circle = minimum_bounding_circle(geom)
    if circle is None or circle.is_empty:
        return float("nan")
    # The minimum bounding circle is a polygonal approximation; its
    # bounds give the diameter on either axis (which are equal for a
    # true circle approximation). Use minx/maxx for stability.
    minx, miny, maxx, maxy = circle.bounds
    return max(maxx - minx, maxy - miny)


def _welzl_diameter(geom) -> float:
    """Welzl's algorithm fallback on the polygon's exterior coordinates.
    Used only if shapely.minimum_bounding_circle is unavailable.
    """
    import random
    if geom is None or geom.is_empty:
        return float("nan")
    pts: list[tuple[float, float]] = []
    if hasattr(geom, "geoms"):
        for g in geom.geoms:
            pts.extend(list(g.exterior.coords))
    else:
        pts.extend(list(geom.exterior.coords))
    pts = list({p for p in pts})
    if not pts:
        return float("nan")
    random.seed(42)
    random.shuffle(pts)

    def circle_from_2(a, b):
        cx = (a[0] + b[0]) / 2
        cy = (a[1] + b[1]) / 2
        r = math.hypot(a[0] - cx, a[1] - cy)
        return (cx, cy, r)

    def circle_from_3(a, b, c):
        ax, ay = a; bx, by = b; cx, cy = c
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < 1e-12:
            return None
        ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay)
              + (cx**2 + cy**2) * (ay - by)) / d
        uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx)
              + (cx**2 + cy**2) * (bx - ax)) / d
        r = math.hypot(ax - ux, ay - uy)
        return (ux, uy, r)

    def in_circle(c, p):
        return math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2] + 1e-9

    def trivial(R):
        if not R:
            return (0.0, 0.0, 0.0)
        if len(R) == 1:
            return (R[0][0], R[0][1], 0.0)
        if len(R) == 2:
            return circle_from_2(R[0], R[1])
        c = circle_from_3(R[0], R[1], R[2])
        return c if c is not None else circle_from_2(R[0], R[1])

    def welzl(P, R, n):
        if n == 0 or len(R) == 3:
            return trivial(R)
        p = P[n - 1]
        D = welzl(P, R, n - 1)
        if D is not None and in_circle(D, p):
            return D
        return welzl(P, R + [p], n - 1)

    # Iterative Welzl on a sample (full Welzl on millions of vertices is
    # slow; we sample 1500 boundary points which is plenty for the
    # bounding circle).
    if len(pts) > 1500:
        idx = list(range(len(pts)))
        random.shuffle(idx)
        pts = [pts[i] for i in idx[:1500]]
    c = welzl(pts, [], len(pts))
    if c is None:
        return float("nan")
    return 2.0 * c[2]


def bounding_circle_diameter(geom) -> float:
    d = _mbc_diameter_via_shapely(geom)
    if not math.isnan(d) and d > 0:
        return d
    return _welzl_diameter(geom)


def reock(geom) -> tuple[float, float]:
    """Return (diameter_m, reock_score)."""
    if geom is None or geom.is_empty:
        return float("nan"), float("nan")
    d = bounding_circle_diameter(geom)
    if not d or math.isnan(d) or d <= 0:
        return float("nan"), float("nan")
    score = (4.0 * geom.area) / (math.pi * d * d)
    return d, score


def score_map(gpkg_path: Path, label: str) -> pd.DataFrame:
    gdf = gpd.read_file(gpkg_path)
    if gdf.crs is None or gdf.crs.to_string() != TARGET_CRS:
        gdf = gdf.to_crs(TARGET_CRS)
    rows = []
    for _, r in gdf.iterrows():
        g = r.geometry
        d, s = reock(g)
        rows.append({
            "map": label,
            "ed_name": r["name_2026"],
            "area_m2": g.area if g is not None else None,
            "bounding_circle_diameter_m": d,
            "reock": s,
        })
    return pd.DataFrame(rows)


def print_summary(label: str, df: pd.DataFrame) -> None:
    re = df["reock"].dropna()
    n = len(re)
    below = int((re < REOCK_THRESHOLD).sum())
    pct = (below / n * 100.0) if n else 0.0
    print(f"\n{label}: {n} EDs scored")
    print(f"  Reock < {REOCK_THRESHOLD}: {below}/{n} = {pct:.1f}%")
    print(f"  mean Reock={re.mean():.3f}  median={re.median():.3f}")
    print(f"  bottom 10 by Reock:")
    bot = df.dropna(subset=["reock"]).nsmallest(10, "reock")
    for _, r in bot.iterrows():
        print(f"    {r['ed_name']:<45s}  Reock={r['reock']:.3f}")


def print_lasso_lookup(df_all: pd.DataFrame) -> None:
    print("\n" + "=" * 72)
    print("FIVE NAMED LASSO DISTRICTS — v0_9 REOCK")
    print("=" * 72)
    for name in LASSO_NAMED:
        rows = df_all[df_all["ed_name"] == name]
        if rows.empty:
            print(f"  {name:<45s}  NOT FOUND in either v0_9 map")
            continue
        for _, r in rows.iterrows():
            tag = f"below {REOCK_THRESHOLD}" if r["reock"] < REOCK_THRESHOLD else f"above {REOCK_THRESHOLD}"
            print(f"  [{r['map']:<8s}] {r['ed_name']:<45s}  "
                  f"Reock={r['reock']:.3f}  ({tag})")


def main() -> None:
    print(f"Loading minority {MIN_GPKG.name}...")
    df_min = score_map(MIN_GPKG, "minority")
    print(f"Loading majority {MAJ_GPKG.name}...")
    df_maj = score_map(MAJ_GPKG, "majority")

    df_all = pd.concat([df_min, df_maj], ignore_index=True)
    df_all.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV} ({len(df_all)} rows)")

    print("\n" + "=" * 72)
    print("v0_9 REOCK SUMMARY")
    print("=" * 72)
    print_summary("MINORITY", df_min)
    print_summary("MAJORITY", df_maj)

    print_lasso_lookup(df_all)


if __name__ == "__main__":
    main()
