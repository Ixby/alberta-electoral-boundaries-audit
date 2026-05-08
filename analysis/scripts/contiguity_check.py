"""Alberta Electoral Boundaries — Contiguity Check (v0.1)
=========================================================
Verifies that each ED in each map is a contiguous polygon with no
disconnected island sub-polygons that would prevent effective representation.

Definition of contiguous (this script):
  - A Polygon geometry is always contiguous.
  - A MultiPolygon geometry is contiguous if its largest part accounts for
    ≥ 95 % of the total ED area. The 95 % threshold tolerates small islands
    (lakes, minor enclaves) that exist for legitimate cadastral reasons while
    flagging structurally split EDs where a meaningful population island is
    detached from the main body.

Inputs:
  data/shapefiles/derived/v0_3_canonical_majority_2026_eds_swept.gpkg
  data/shapefiles/derived/v0_3_canonical_minority_2026_eds_swept.gpkg
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp

Outputs:
  analysis/reports/contiguity_check.csv
      Columns: map, name, geom_type, num_parts, largest_part_area_pct,
               contiguous
  data/contiguity_summary.json
      Per-map: total_eds, contiguous_eds, fragmented_eds,
               fragmented_ed_names
  stdout: pass/fail gate per map; explicit list of non-contiguous EDs

Author: v0.1 audit pipeline — geometry analysis per test-selection-rationale
§6.1 / apparatus-defense §2.1. Generated 2026-04-24.

Forward deps:
  - analysis/reports/contiguity_check.csv (consumed by section MD)
  - data/contiguity_summary.json (consumed by report_academic.md §5.x)

Backward deps:
  - data/shapefiles/derived/v0_3_canonical_majority_2026_eds_swept.gpkg
  - data/shapefiles/derived/v0_3_canonical_minority_2026_eds_swept.gpkg
  - data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent.parent  # .../alberta_audit


def _pick(plan: str) -> Path:
    base = data_loader._resolve_path("data") / "shapefiles" / "derived"
    for fname in (
        f"v0_8_full_refined_{plan}_2026_eds.gpkg",
        f"v0_8_refined_{plan}_2026_eds.gpkg",
        f"v0_8_canonical_{plan}_2026_eds.gpkg",
        f"v0_7_canonical_{plan}_2026_eds.gpkg",
        f"v0_3_canonical_{plan}_2026_eds_swept.gpkg",
    ):
        p = base / fname
        if p.exists():
            return p
    return base / f"v0_3_canonical_{plan}_2026_eds_swept.gpkg"


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

OUT_CSV = ROOT / "analysis" / "reports" / "contiguity_check.csv"
OUT_JSON = data_loader._resolve_path("data") / "contiguity_summary.json"

# An ED is contiguous if its largest part is >= this fraction of total area
CONTIGUITY_THRESHOLD = 0.95

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _detect_name_column(gdf: gpd.GeoDataFrame) -> str:
    """Return the column most likely to hold ED names."""
    candidates = [
        "name_2026",
        "ed_name",
        "ED_NAME",
        "EDName2017",
        "EDName2010",
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
    ]
    for c in candidates:
        if c in gdf.columns:
            return c
    for c in gdf.columns:
        if c == gdf.geometry.name:
            continue
        if gdf[c].dtype == object:
            return c
    raise ValueError(f"Cannot identify name column. Columns: {list(gdf.columns)}")


def _contiguity_stats(geom) -> Tuple[str, int, float, bool]:
    """
    Return (geom_type, num_parts, largest_part_area_pct, is_contiguous).

    For a Polygon: num_parts=1, largest_part_area_pct=100.0, contiguous=True.
    For a MultiPolygon: measure the largest sub-polygon area as a fraction
    of total area and apply the threshold.
    For null / empty geometry: return sentinel values.
    """
    if geom is None or geom.is_empty:
        return ("Empty", 0, 0.0, False)

    geom_type = geom.geom_type

    if geom_type == "Polygon":
        return ("Polygon", 1, 100.0, True)

    if geom_type == "MultiPolygon":
        parts: List[Polygon] = list(geom.geoms)
        num_parts = len(parts)
        total_area = geom.area
        if total_area <= 0:
            return ("MultiPolygon", num_parts, 0.0, False)
        largest_area = max(p.area for p in parts)
        largest_pct = (largest_area / total_area) * 100.0
        is_contiguous = (largest_pct / 100.0) >= CONTIGUITY_THRESHOLD
        return ("MultiPolygon", num_parts, largest_pct, is_contiguous)

    # GeometryCollection or other unexpected type — treat as non-contiguous
    return (geom_type, 1, 0.0, False)


# ---------------------------------------------------------------------------
# Per-map computation
# ---------------------------------------------------------------------------


def check_contiguity(map_label: str, path: Path) -> List[Dict]:
    """Load a map and compute contiguity stats for each ED."""
    if not path.exists():
        print(f"  [MISSING] {path}", file=sys.stderr)
        return []

    gdf = gpd.read_file(path)
    name_col = _detect_name_column(gdf)

    expected = EXPECTED_COUNTS.get(map_label, "?")
    actual = len(gdf)
    if actual != expected:
        print(
            f"  [WARN] {map_label}: expected {expected} EDs, got {actual}",
            file=sys.stderr,
        )

    rows = []
    for _, row in gdf.iterrows():
        geom = row.geometry
        geom_type, num_parts, largest_pct, is_contiguous = _contiguity_stats(geom)
        rows.append(
            {
                "map": map_label,
                "name": str(row[name_col]),
                "geom_type": geom_type,
                "num_parts": num_parts,
                "largest_part_area_pct": round(largest_pct, 4),
                "contiguous": is_contiguous,
            }
        )

    return rows


# ---------------------------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------------------------


def summarise(map_label: str, rows: List[Dict]) -> Dict:
    """Compute per-map contiguity summary."""
    total = len(rows)
    contiguous = [r for r in rows if r["contiguous"]]
    fragmented = [r for r in rows if not r["contiguous"]]
    return {
        "map": map_label,
        "total_eds": total,
        "contiguous_eds": len(contiguous),
        "fragmented_eds": len(fragmented),
        "fragmented_ed_names": [r["name"] for r in fragmented],
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def write_csv(all_rows: List[Dict]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "map",
        "name",
        "geom_type",
        "num_parts",
        "largest_part_area_pct",
        "contiguous",
    ]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"CSV written: {OUT_CSV}")


def write_json(summaries: List[Dict]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {"maps": summaries}
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"JSON written: {OUT_JSON}")


def print_findings(summaries: List[Dict]) -> None:
    print()
    print("Contiguity Check Results")
    print("=" * 60)
    all_pass = True
    for s in summaries:
        n_frag = s["fragmented_eds"]
        status = "PASS" if n_frag == 0 else "FAIL"
        if n_frag > 0:
            all_pass = False
        print(
            f"  [{status}] {s['map']}: "
            f"{s['contiguous_eds']}/{s['total_eds']} contiguous, "
            f"{n_frag} fragmented"
        )
        if n_frag > 0:
            for name in s["fragmented_ed_names"]:
                print(f"           >> NON-CONTIGUOUS: {name}")
    print("=" * 60)
    if all_pass:
        print("Gate: PASS — all EDs in all maps are contiguous.")
    else:
        print(
            "Gate: FAIL — non-contiguous EDs detected. "
            "Review fragmented_ed_names in the JSON summary."
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    all_rows: List[Dict] = []
    summaries: List[Dict] = []

    for map_label, path in MAPS.items():
        print(f"Processing {map_label}: {path.name} ...", end=" ", flush=True)
        rows = check_contiguity(map_label, path)
        print(f"{len(rows)} EDs")
        all_rows.extend(rows)
        summaries.append(summarise(map_label, rows))

    write_csv(all_rows)
    write_json(summaries)
    print_findings(summaries)


if __name__ == "__main__":
    main()
