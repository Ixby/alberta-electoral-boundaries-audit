"""Alberta Electoral Boundaries — Compactness Metrics (v0.1)
============================================================
Computes Polsby-Popper compactness scores for every ED in the 2019 enacted
map (87 EDs) and both 2026 proposed maps (89 EDs each).

  Polsby-Popper = 4π × area / perimeter²

Range is 0–1, where 1 = a perfect circle. A score near 0 indicates an
elongated or convoluted boundary. The metric is rotation- and scale-
invariant and is widely used in electoral boundary litigation (Niemi et al.
1990; Polsby & Popper 1991).

Tests computed:
  C1: Per-ED Polsby-Popper score for each of three maps
  C2: Per-map summary statistics (mean, median, std_dev, min, max)
  C3: Count of EDs below 0.30 and 0.40 thresholds per map
  C4: Gate check — warn if any map's mean PP is below 0.15

Inputs:
  data/shapefiles/derived/v0_3_canonical_majority_2026_eds_swept.gpkg
  data/shapefiles/derived/v0_3_canonical_minority_2026_eds_swept.gpkg
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp

Outputs:
  findings/compactness_metrics.csv
      Columns: map, name, area_km2, perimeter_km, polsby_popper,
               pp_percentile_rank
  data/compactness_summary.json
      Per-map: mean, median, std_dev, min, max, count_below_0_3,
               count_below_0_4
  stdout: summary table

Author: v0.1 audit pipeline — geometry analysis per test-selection-rationale
§6.1 / apparatus-defense §2.1. Generated 2026-04-24.

Forward deps:
  - findings/compactness_metrics.csv (consumed by section MD)
  - data/compactness_summary.json (consumed by report_academic.md §5.x)

Backward deps:
  - data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg
  - data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg
  - data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import sys
import logging
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import csv
import json
import math
import sys
from pathlib import Path
from typing import Dict, List

import geopandas as gpd
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent.parent  # .../alberta_audit
logger = logging.getLogger(__name__)


def _pick(plan: str) -> Path:
    """Prefer official canonical shapefiles; fall back to derived (deprecated)."""
    canonical = data_loader._resolve_path(data_loader.CONFIG["data"]["canonical_dir"]) / f"ea_{plan}_2026_eds.gpkg"
    if canonical.exists():
        return canonical
    base = data_loader._resolve_path("data") / "shapefiles" / "derived"
    for fname in (
        f"v0_10_topological_{plan}_2026_eds.gpkg",
        f"v0_8_full_refined_{plan}_2026_eds.gpkg",
        f"v0_8_refined_{plan}_2026_eds.gpkg",
        f"v0_8_canonical_{plan}_2026_eds.gpkg",
        f"v0_7_canonical_{plan}_2026_eds.gpkg",
    ):
        p = base / fname
        if p.exists():
            return p
    return base / f"v0_7_canonical_{plan}_2026_eds.gpkg"


MAPS = {
    "2019_enacted": (
        ROOT
        / "data"
        / "shapefiles"
        / "reference"
        / "alberta_2019_eds"
        / "EDS_ENACTED_BILL33_15DEC2017.shp"
    ),
    "majority_2026": _pick("majority"),
    "minority_2026": _pick("minority"),
}

EXPECTED_COUNTS = {
    "2019_enacted": 87,
    "majority_2026": 89,
    "minority_2026": 89,
}

OUT_CSV = ROOT / "analysis" / "reports" / "compactness_metrics.csv"
OUT_JSON = data_loader._resolve_path("data") / "compactness_summary.json"

# Alberta TM — EPSG:3401 (NAD83 / Alberta 10-TM Forest)
ALBERTA_CRS = "EPSG:3401"

# Gate: warn if mean PP for any map falls below this
GATE_MEAN_PP = 0.15

# Thresholds for count reporting
LOW_THRESHOLD_1 = 0.30
LOW_THRESHOLD_2 = 0.40

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _detect_name_column(gdf: gpd.GeoDataFrame) -> str:
    """Return the column most likely to hold ED names."""
    candidates = [
        "EDName2025",
        "name_2026",
        "ed_name",
        "ED_NAME",
        "name",
        "NAME",
        "EDS_NAME",
        "eds_name",
        "ENAME",
        "ename",
        "DISTRICT_N",
        "district_n",
        "DIV_NAME",
        "div_name",
        "RIDING_NAM",
        "riding_nam",
        "EDName2017",
    ]
    for c in candidates:
        if c in gdf.columns:
            return c
    # Fallback: first non-geometry string column
    for c in gdf.columns:
        if c == gdf.geometry.name:
            continue
        if gdf[c].dtype == object:
            return c
    raise ValueError(f"Cannot identify name column. Columns: {list(gdf.columns)}")


def polsby_popper(area_m2: float, perimeter_m: float) -> float:
    """Return Polsby-Popper score. Returns 0.0 if perimeter is zero."""
    if perimeter_m <= 0:
        return 0.0
    return (4.0 * math.pi * area_m2) / (perimeter_m**2)


def reock_score(geom) -> float:
    """Area / area of minimum bounding circle."""
    # NaN contract: returns float("nan") if geometry is None, empty, or MBC fails.
    if geom is None or geom.is_empty:
        return float("nan")
    try:
        mbc = geom.minimum_bounding_circle()
        # NaN contract: returns float("nan") if MBC is degenerate.
        if mbc is None or mbc.is_empty or mbc.area == 0:
            return float("nan")
        return float(geom.area / mbc.area)
    except Exception as e:
        logger.debug("minimum_bounding_circle unavailable: %s", e)
        return float("nan")


def convex_hull_ratio(geom) -> float:
    """Area / convex hull area."""
    # NaN contract: returns float("nan") if geometry is None or empty.
    if geom is None or geom.is_empty:
        return float("nan")
    hull = geom.convex_hull
    # NaN contract: returns float("nan") if convex hull has zero area.
    if hull is None or hull.area == 0:
        return float("nan")
    return float(geom.area / hull.area)


def schwartzberg_score(area_m2: float, perimeter_m: float) -> float:
    """Ratio of perimeter to circumference of equal-area circle. Inverted: 1 = circle."""
    # NaN contract: returns float("nan") if geometry measurements are non-positive.
    if perimeter_m <= 0 or area_m2 <= 0:
        return float("nan")
    r_equiv = math.sqrt(area_m2 / math.pi)
    return float((2 * math.pi * r_equiv) / perimeter_m)


def percentile_rank(values: List[float], value: float) -> float:
    """Return percentile rank (0–100) of `value` within `values` (midrank)."""
    n = len(values)
    if n == 0:
        return 0.0
    count_below = sum(1 for v in values if v < value)
    count_equal = sum(1 for v in values if v == value)
    return 100.0 * (count_below + 0.5 * count_equal) / n


# ---------------------------------------------------------------------------
# Per-map computation
# ---------------------------------------------------------------------------


def compute_compactness(map_label: str, path: Path) -> List[Dict]:
    """Load a map, reproject to Alberta TM, compute PP for each ED."""
    if not path.exists():
        print(f"  [MISSING] {path}", file=sys.stderr)
        return []

    gdf = gpd.read_file(path)
    name_col = _detect_name_column(gdf)

    # Reproject to metric CRS for accurate area/perimeter
    if gdf.crs is None or gdf.crs.to_epsg() != 3401:
        gdf = gdf.to_crs(ALBERTA_CRS)

    expected = EXPECTED_COUNTS.get(map_label, "?")
    actual = len(gdf)
    if actual != expected and expected != "?":
        raise ValueError(
            f"Map '{map_label}' expected {expected} EDs, got {actual}. Shapefile validation failed."
        )

    rows = []
    for _, row in gdf.iterrows():
        geom = row.geometry
        if geom is None or geom.is_empty:
            raise ValueError(
                f"Map '{map_label}' contains empty geometry for district '{row.get(name_col, 'Unknown')}'. Topology failure."
            )
        area_m2 = geom.area
        perimeter_m = geom.length
        pp = polsby_popper(area_m2, perimeter_m)
        rows.append(
            {
                "map": map_label,
                "name": str(row[name_col]),
                "area_km2": area_m2 / 1e6,
                "perimeter_km": perimeter_m / 1e3,
                "polsby_popper": pp,
                "reock": reock_score(geom),
                "convex_hull": convex_hull_ratio(geom),
                "schwartzberg": schwartzberg_score(area_m2, perimeter_m),
            }
        )

    # Add percentile ranks within this map
    pp_values = [r["polsby_popper"] for r in rows]
    for r in rows:
        r["pp_percentile_rank"] = percentile_rank(pp_values, r["polsby_popper"])

    return rows


def summarise_extended(map_label: str, rows: List[Dict]) -> Dict:
    """Summary including all four compactness metrics."""
    base = summarise(map_label, rows)
    for metric in ["reock", "convex_hull", "schwartzberg"]:
        vals = [
            r[metric] for r in rows if r.get(metric) == r.get(metric)
        ]  # exclude nan
        if vals:
            base[f"{metric}_mean"] = round(sum(vals) / len(vals), 6)
            base[f"{metric}_median"] = round(sorted(vals)[len(vals) // 2], 6)
            base[f"{metric}_min"] = round(min(vals), 6)
    return base


# ---------------------------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------------------------


def summarise(map_label: str, rows: List[Dict]) -> Dict:
    """Compute per-map summary statistics."""
    pp_vals = [r["polsby_popper"] for r in rows]
    if not pp_vals:
        return {"map": map_label, "count": 0}

    pp_vals_sorted = sorted(pp_vals)
    n = len(pp_vals_sorted)
    mean_pp = sum(pp_vals_sorted) / n
    if n % 2 == 1:
        median_pp = pp_vals_sorted[n // 2]
    else:
        median_pp = (pp_vals_sorted[n // 2 - 1] + pp_vals_sorted[n // 2]) / 2.0

    variance = (
        sum((v - mean_pp) ** 2 for v in pp_vals_sorted) / (n - 1) if n > 1 else 0.0
    )
    std_dev = math.sqrt(variance)

    return {
        "map": map_label,
        "count": n,
        "mean": round(mean_pp, 6),
        "median": round(median_pp, 6),
        "std_dev": round(std_dev, 6),
        "min": round(pp_vals_sorted[0], 6),
        "max": round(pp_vals_sorted[-1], 6),
        "count_below_0_3": sum(1 for v in pp_vals if v < LOW_THRESHOLD_1),
        "count_below_0_4": sum(1 for v in pp_vals if v < LOW_THRESHOLD_2),
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def write_csv(all_rows: List[Dict]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "map",
        "name",
        "area_km2",
        "perimeter_km",
        "polsby_popper",
        "pp_percentile_rank",
    ]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(
                {
                    "map": row["map"],
                    "name": row["name"],
                    "area_km2": f"{row['area_km2']:.4f}",
                    "perimeter_km": f"{row['perimeter_km']:.4f}",
                    "polsby_popper": f"{row['polsby_popper']:.6f}",
                    "pp_percentile_rank": f"{row['pp_percentile_rank']:.2f}",
                }
            )
    print(f"CSV written: {OUT_CSV}")


def write_json(summaries: List[Dict]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {"maps": summaries}
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"JSON written: {OUT_JSON}")


def print_summary_table(summaries: List[Dict]) -> None:
    col_w = 18
    hdr = (
        f"{'Map':<{col_w}} {'N':>4}  {'Mean PP':>8}  {'Median':>8}"
        f"  {'Std':>7}  {'Min':>7}  {'Max':>7}  {'<0.30':>6}  {'<0.40':>6}"
    )
    print()
    print("Polsby-Popper Compactness Summary")
    print("=" * len(hdr))
    print(hdr)
    print("-" * len(hdr))
    for s in summaries:
        if s.get("count", 0) == 0:
            print(f"{s['map']:<{col_w}} (no data)")
            continue
        print(
            f"{s['map']:<{col_w}} {s['count']:>4}  {s['mean']:>8.4f}"
            f"  {s['median']:>8.4f}  {s['std_dev']:>7.4f}"
            f"  {s['min']:>7.4f}  {s['max']:>7.4f}"
            f"  {s['count_below_0_3']:>6}  {s['count_below_0_4']:>6}"
        )
    print("=" * len(hdr))


def gate_check(summaries: List[Dict]) -> None:
    print()
    print("Gate check — mean PP < 0.15 (extremely fragmented boundaries)")
    any_fail = False
    for s in summaries:
        mean_pp = s.get("mean")
        if mean_pp is None:
            continue
        if mean_pp < GATE_MEAN_PP:
            print(
                f"  [FAIL] {s['map']}: mean PP = {mean_pp:.4f} — "
                f"below gate threshold {GATE_MEAN_PP}"
            )
            any_fail = True
        else:
            print(f"  [PASS] {s['map']}: mean PP = {mean_pp:.4f}")
    if not any_fail:
        print("  All maps pass the mean PP gate.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    all_rows: List[Dict] = []
    summaries: List[Dict] = []

    for map_label, path in MAPS.items():
        print(f"Processing {map_label}: {path.name} ...", end=" ", flush=True)
        rows = compute_compactness(map_label, path)
        print(f"{len(rows)} EDs")
        all_rows.extend(rows)
        summaries.append(summarise_extended(map_label, rows))

    write_csv(all_rows)
    write_json(summaries)
    print_summary_table(summaries)
    gate_check(summaries)


if __name__ == "__main__":
    main()
