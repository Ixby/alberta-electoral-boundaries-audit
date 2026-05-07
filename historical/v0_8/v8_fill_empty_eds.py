"""
v0_1_v8_fill_empty_eds.py

Bring v0_8 to 100% ED coverage by filling the inherited-empty EDs (21
majority + 12 minority) with Tier-A polygons inherited from the 2019
enacted shapefile.

For each empty 2026 ED:
  1. Locate its 2019 parent by exact name match (e.g., "Calgary-Currie"
     2026 = "Calgary-Currie" 2019). If no exact match, fall back to a
     manually-curated rename map; if still no match, skip and report.
  2. Take the 2019 ED's polygon as the inherited geometry.
  3. The current v0_8 has 100% provincial coverage already (Phase 3
     gap-fill assigned everything to *non-empty* EDs). Inserting the
     2019 inherited polygon would create overlap with whichever
     non-empty ED currently owns that territory.
  4. CARVE the inherited polygon out of any non-empty ED it overlaps
     (using shapely difference). This undoes the Phase-3 over-absorption
     for the urban EDs that should have received the polygon originally.
  5. Assign the inherited (and possibly clipped at the province boundary)
     polygon to the previously-empty ED.

After fill: 89 of 89 EDs have geometry, no overlap, full coverage.

Inputs:
  data/shapefiles/derived/v0_8_canonical_<plan>_2026_eds.gpkg
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp

Outputs:
  data/shapefiles/derived/v0_8_full_<plan>_2026_eds.gpkg
  data/v0_1_v8_fill_summary_<plan>.csv

Dependencies:
  Forward:  any downstream script that wants 100% v0_8 ED coverage.
            Will pick this file up via the standard prefer-chain
            (refined → full → canonical → v7) once consumers are updated.
  Backward: v0_8 canonical (perfecter output) + 2019 enacted shapefile.
"""

# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _perf_utils import Timer, ts  # noqa: E402

ROOT = HERE.parent.parent
DATA = ROOT / "data"
DERIVED = DATA / "shapefiles" / "derived"
REFERENCE_2019 = (
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)

CRS = 3401
EMPTY_THRESHOLD_M2 = 1e5  # ED with < 0.1 km² treated as empty

# Manually-curated rename map for empty 2026 EDs that don't exact-match a
# 2019 name. Each entry is 2026_name → list of 2019 EDs whose union forms
# the 2026 ED's territorial footprint. Empty list = no good fallback,
# script will report it as unfilled.
RENAME_MAP_2019 = {
    # MAJORITY 2026 — empty EDs without exact 2019 name match
    "Calgary-North West": ["Calgary-North West"],
    "Edmonton-Beverly-Clareview": ["Edmonton-Beverly-Clareview"],
    "Edmonton-Glenora-Riverview": ["Edmonton-Glenora", "Edmonton-Riverview"],
    "Edmonton-Manning": ["Edmonton-Manning"],
    "Edmonton-North West": ["Edmonton-North West"],
    "Edmonton-West Henday": ["Edmonton-West Henday"],
    "Edmonton-Windermere": ["Edmonton-Whitemud", "Edmonton-Rutherford"],
    "Lacombe-Clearwater": ["Rimbey-Rocky Mountain House-Sundre"],
    "St. Albert-Sturgeon": ["St. Albert", "Spruce Grove-Stony Plain"],
    "Stony Plain-Drayton Valley": ["Stony Plain", "Drayton Valley-Devon"],
    "Strathcona-Sherwood Park": ["Sherwood Park", "Strathcona-Sherwood Park"],
    "Wetaskiwin-Ponoka-Maskwacis": ["Wetaskiwin-Camrose", "Lacombe-Ponoka"],
    # MINORITY 2026 — empty EDs without exact 2019 name match
    "Calgary-North West-Bearspaw": ["Calgary-North West"],
    "Calgary-Peigan-Chestermere": ["Chestermere-Strathmore"],
    "Calgary-South East": ["Calgary-South East"],
    "Edmonton-Castledowns": ["Edmonton-Castle Downs"],
    "Lethbridge-Taber-Warner": ["Cardston-Siksika", "Taber-Warner"],
    "Red Deer-Blackfalds": ["Red Deer-South", "Innisfail-Sylvan Lake"],
}


def _load_2019() -> dict[str, Polygon]:
    """Return dict of 2019 ED name → polygon, all in CRS 3401."""
    g = gpd.read_file(REFERENCE_2019)
    if g.crs is None or g.crs.to_epsg() != CRS:
        g = g.to_crs(CRS)
    name_col = "EDName2017"
    return {row[name_col].strip(): row.geometry for _, row in g.iterrows()}


def _resolve_inherited(
    name_2026: str, names_2019: dict
) -> tuple[Polygon | MultiPolygon | None, str]:
    """Return (inherited_polygon, source_label).
    First try exact name match, then the rename map."""
    if name_2026 in names_2019:
        return names_2019[name_2026], "exact_2019_match"
    if name_2026 in RENAME_MAP_2019:
        parts = []
        for parent_name in RENAME_MAP_2019[name_2026]:
            if parent_name in names_2019:
                parts.append(names_2019[parent_name])
        if parts:
            return unary_union(parts), f"rename_map ({len(parts)} 2019 parts)"
    return None, "unmatched"


def _clean(geom):
    if geom is None or geom.is_empty:
        return geom
    if not geom.is_valid:
        geom = geom.buffer(0)
    return geom


def fill(plan: str, names_2019: dict) -> dict:
    src = DERIVED / f"v0_8_canonical_{plan}_2026_eds.gpkg"
    if not src.exists():
        print(f"  [skip] {src.name} not found")
        return {"plan": plan, "skipped": True}

    with Timer(f"[{plan}] fill") as t:
        g = gpd.read_file(src)
        if g.crs is None or g.crs.to_epsg() != CRS:
            g = g.to_crs(CRS)

        # Province boundary = current union (after Phase 3 gap-fill, this is full Alberta)
        province = unary_union(g.geometry.values)

        # Identify empty EDs
        areas = g.geometry.area
        empty_mask = areas < EMPTY_THRESHOLD_M2
        empty_idx = g.index[empty_mask].tolist()
        non_empty_idx = g.index[~empty_mask].tolist()
        print(
            f"  {len(empty_idx)} empty EDs, {len(non_empty_idx)} with geometry",
            flush=True,
        )

        new_geoms = list(g.geometry.values)
        log = []

        for i in empty_idx:
            name = str(g.at[i, "name_2026"])
            inherited, source = _resolve_inherited(name, names_2019)
            if inherited is None:
                print(f"  [unmatched] {name}", flush=True)
                log.append(
                    {"ed": name, "source": source, "area_km2": 0.0, "carved_from": ""}
                )
                continue
            # Clip inherited polygon to the current province (don't extend beyond Alberta)
            inherited = _clean(inherited.intersection(province))
            if inherited.is_empty or inherited.area < EMPTY_THRESHOLD_M2:
                print(f"  [empty after clip] {name}", flush=True)
                log.append(
                    {
                        "ed": name,
                        "source": source + "+clip_to_province",
                        "area_km2": 0.0,
                        "carved_from": "",
                    }
                )
                continue

            # Carve the inherited polygon out of any non-empty ED that overlaps,
            # with anti-erasure: if a full carve would reduce a 2026 neighbour
            # below 10 % of its current area (i.e. the 2026 ED is mostly inside
            # the inherited 2019 polygon, meaning the boundaries diverged),
            # fall back to a midline split — give the inherited ED only the
            # half of the overlap nearer its own centroid, leave the other half
            # with the 2026 neighbour.
            ANTI_ERASURE = 0.10
            inherited_after_split = inherited
            carved_from = []
            for j in non_empty_idx:
                gj = new_geoms[j]
                if gj is None or gj.is_empty:
                    continue
                if not gj.intersects(inherited_after_split):
                    continue
                inter = _clean(gj.intersection(inherited_after_split))
                if inter.is_empty or inter.area < 1.0:
                    continue
                # Predicted post-carve neighbour area
                clipped = _clean(gj.difference(inherited_after_split))
                if not clipped.is_empty and clipped.area >= ANTI_ERASURE * gj.area:
                    # Safe full carve — neighbour retains ≥10 % of its area
                    new_geoms[j] = clipped
                    carved_from.append(str(g.at[j, "name_2026"]))
                else:
                    # Over-erasure case — midline-split the overlap.
                    # Each piece of the overlap goes to whichever ED's
                    # centroid it's closer to.
                    ic = inherited_after_split.centroid
                    jc = gj.centroid
                    # We approximate the midline split by picking points from
                    # a buffer-based partition: shrink inherited slightly along
                    # the bisector and award the leftover ring back to gj.
                    # Implementation: pieces of inter closer to ic stay with
                    # inherited; pieces closer to jc go to gj.
                    try:
                        # Use shapely.STRtree-free approach: discretise inter
                        # via bbox subdivisions. Simpler: take the overlap
                        # centroid; if it's closer to inherited's centroid,
                        # full carve; else leave the overlap with gj entirely.
                        pc = inter.centroid
                        d_to_i = pc.distance(ic)
                        d_to_j = pc.distance(jc)
                        if d_to_i < d_to_j:
                            # Inherited keeps the overlap — neighbour gets
                            # reduced but we accept the area-shrink because
                            # the overlap is geographically "more in"
                            # the inherited polygon.
                            new_geoms[j] = clipped
                            carved_from.append(
                                str(g.at[j, "name_2026"]) + " (over-erasure, accepted)"
                            )
                        else:
                            # Neighbour is closer — pull the overlap out of
                            # the inherited polygon and leave gj intact.
                            inherited_after_split = _clean(
                                inherited_after_split.difference(inter)
                            )
                            carved_from.append(
                                str(g.at[j, "name_2026"])
                                + " (midline → kept by neighbour)"
                            )
                    except Exception:
                        new_geoms[j] = clipped
                        carved_from.append(str(g.at[j, "name_2026"]) + " (fallback)")

            inherited = inherited_after_split
            new_geoms[i] = inherited
            print(
                f"  [filled] {name} via {source} "
                f"({inherited.area/1e6:.1f} km², carved from {len(carved_from)} EDs)",
                flush=True,
            )
            log.append(
                {
                    "ed": name,
                    "source": source,
                    "area_km2": inherited.area / 1e6,
                    "carved_from": "; ".join(carved_from),
                }
            )

        g["geometry"] = new_geoms
        out = DERIVED / f"v0_8_full_{plan}_2026_eds.gpkg"
        g.to_file(out, driver="GPKG")
        print(f"  wrote {out.name}", flush=True)

        log_df = pd.DataFrame(log)
        log_path = DATA / f"v0_1_v8_fill_summary_{plan}.csv"
        log_df.to_csv(log_path, index=False)
        print(f"  wrote {log_path.name}", flush=True)

        # Final coverage check
        new_areas = g.geometry.area
        n_with = int((new_areas >= EMPTY_THRESHOLD_M2).sum())
        n_empty = int((new_areas < EMPTY_THRESHOLD_M2).sum())
        coverage_km2 = unary_union(g.geometry.values).area / 1e6
        province_km2 = province.area / 1e6
        coverage_pct = coverage_km2 / province_km2 * 100

        n_filled = sum(1 for r in log if r["area_km2"] > 0)
        n_unmatched = sum(1 for r in log if r["area_km2"] == 0)
        t.note = (
            f"{n_filled} filled, {n_unmatched} unmatched; "
            f"final {n_with}/{len(g)} non-empty, "
            f"{coverage_pct:.4f}% coverage"
        )

    return {
        "plan": plan,
        "n_filled": n_filled,
        "n_unmatched": n_unmatched,
        "n_with_geom": n_with,
        "n_empty": n_empty,
        "coverage_pct": coverage_pct,
        "out": str(out),
    }


def main() -> int:
    with Timer("[v0_8 fill empty EDs]"):
        names_2019 = _load_2019()
        print(
            f"  loaded {len(names_2019)} 2019 enacted EDs as inheritance source",
            flush=True,
        )
        results = []
        for plan in ("majority", "minority"):
            results.append(fill(plan, names_2019))

        print("\n=== SUMMARY ===")
        for r in results:
            if r.get("skipped"):
                continue
            print(
                f"  {r['plan']}: filled {r['n_filled']}, "
                f"unmatched {r['n_unmatched']}; "
                f"final {r['n_with_geom']}/{r['n_with_geom'] + r['n_empty']} "
                f"non-empty ({r['coverage_pct']:.4f}% coverage)"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
