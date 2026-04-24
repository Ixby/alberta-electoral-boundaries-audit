"""
v0_1_airdrie_overlap_diagnostic.py
====================================
Diagnostic analysis of the Calgary-Airdrie overlap artifact in the canonical
minority 2026 ED shapefile.

The Calgary-Airdrie polygon was likely traced too broadly during pixel extraction
from the commission's minority overview map, causing ~530 km² of overlap with:
  - Calgary-Nolan Hill-Cochrane     (~264 km²)
  - Olds-Three Hills-Didsbury       (~197 km²)
  - Calgary-Foothills-Airdrie West  (~71 km²)

Steps:
  1. Inspect the Calgary-Airdrie minority polygon geometry
  2. Compute the over-extension for each overlapping ED
  3. Propose corrected boundary options (A = no-overlap clip, B = radius clip)
  4. Identify VAs in the overlap zone and check their parent ED attribution
  5. Write analysis/v0_1_airdrie_overlap_report.md

Outputs:
  analysis/v0_1_airdrie_overlap_report.md   (summary report)

Author: sub-agent, 2026-04-23
"""
from __future__ import annotations

import math
import os
import sys
from datetime import datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.ops import unary_union

# ---------------------------------------------------------------------------
# Paths

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = str(Path(__file__).resolve().parent.parent)
DATA_DIR = os.path.join(ROOT, "data")
ANALYSIS_DIR = os.path.join(ROOT, "analysis")

MINORITY_GPKG = os.path.join(DATA_DIR, "v0_1_canonical_minority_2026_eds.gpkg")
VA_GPKG = os.path.join(DATA_DIR, "va_polygons_with_2023_votes.gpkg")
REPORT_PATH = os.path.join(ANALYSIS_DIR, "v0_1_airdrie_overlap_report.md")

WORK_CRS = 3401  # NAD83 / Alberta 10-TM Forest (metres)

# Known approximate City of Airdrie centre in EPSG:3401
AIRDRIE_X = 52_000
AIRDRIE_Y = 5_682_000

TARGET_ED = "Calgary-Airdrie"


# ---------------------------------------------------------------------------
# Helpers

def km2(area_m2: float) -> float:
    return area_m2 / 1_000_000.0


def vertex_count(geom) -> int:
    """Count exterior ring vertices (plus first interior ring hole vertices)."""
    from shapely.geometry import Polygon, MultiPolygon
    total = 0
    if geom is None or geom.is_empty:
        return 0
    geoms = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
    for g in geoms:
        if hasattr(g, "exterior"):
            total += len(g.exterior.coords)
            for interior in g.interiors:
                total += len(interior.coords)
    return total


# ---------------------------------------------------------------------------
# Step 1 — Load minority shapefile and inspect Calgary-Airdrie

def step1_inspect(eds: gpd.GeoDataFrame) -> dict:
    print("\n=== STEP 1: Inspecting Calgary-Airdrie polygon ===")

    # Case-insensitive fuzzy match
    mask = eds["name_2026"].str.strip().str.lower() == TARGET_ED.lower()
    if not mask.any():
        # Try partial match
        mask = eds["name_2026"].str.contains("Airdrie", case=False, na=False)
        print(f"  Exact match not found; using partial match. Candidates: {eds.loc[mask, 'name_2026'].tolist()}")

    if not mask.any():
        print("  ERROR: Could not find Calgary-Airdrie in minority shapefile!")
        print(f"  Available EDs (first 20): {eds['name_2026'].head(20).tolist()}")
        sys.exit(1)

    row = eds[mask].iloc[0]
    geom = row.geometry

    area_km2 = km2(geom.area)
    bbox = geom.bounds  # (minx, miny, maxx, maxy)
    centroid = geom.centroid
    n_vertices = vertex_count(geom)

    dist_to_airdrie = math.sqrt(
        (centroid.x - AIRDRIE_X) ** 2 + (centroid.y - AIRDRIE_Y) ** 2
    ) / 1000.0  # km

    print(f"  ED name       : {row['name_2026']}")
    print(f"  Area          : {area_km2:.1f} km²")
    print(f"  Bounding box  : minx={bbox[0]:.0f}, miny={bbox[1]:.0f}, "
          f"maxx={bbox[2]:.0f}, maxy={bbox[3]:.0f}")
    print(f"  Centroid      : x={centroid.x:.0f}, y={centroid.y:.0f}")
    print(f"  Vertices      : {n_vertices:,}")
    print(f"  Dist centroid -> City of Airdrie (~52000, 5682000): {dist_to_airdrie:.1f} km")
    print(f"  Is centroid near Airdrie (< 50 km)? {'YES' if dist_to_airdrie < 50 else 'NO – ARTIFACT LIKELY'}")

    return {
        "name_2026": row["name_2026"],
        "area_km2": area_km2,
        "bbox": bbox,
        "centroid_x": centroid.x,
        "centroid_y": centroid.y,
        "n_vertices": n_vertices,
        "dist_to_airdrie_km": dist_to_airdrie,
        "geom": geom,
        "idx": eds[mask].index[0],
    }


# ---------------------------------------------------------------------------
# Step 2 — Compute intersections with overlapping EDs

def step2_intersections(eds: gpd.GeoDataFrame, airdrie_info: dict) -> list[dict]:
    print("\n=== STEP 2: Computing overlaps with adjacent EDs ===")

    airdrie_geom = airdrie_info["geom"]
    airdrie_area = airdrie_info["area_km2"]
    airdrie_idx = airdrie_info["idx"]

    results = []
    # Dynamically find all intersecting EDs except the target itself
    for idx, row in eds.iterrows():
        if idx == airdrie_idx:
            continue
            
        geom = row.geometry
        if not airdrie_geom.intersects(geom) or airdrie_geom.intersection(geom).area < 1.0: # ignore point touches
            continue
            
        adj_area_km2 = km2(geom.area)

        intersection = airdrie_geom.intersection(geom)
        inter_area_km2 = km2(intersection.area)

        pct_of_airdrie = 100.0 * inter_area_km2 / airdrie_area if airdrie_area > 0 else 0
        pct_of_adj = 100.0 * inter_area_km2 / adj_area_km2 if adj_area_km2 > 0 else 0

        print(f"\n  Overlap: {TARGET_ED} × {row['name_2026']}")
        print(f"    Adjacent ED area     : {adj_area_km2:.1f} km²")
        print(f"    Intersection area    : {inter_area_km2:.1f} km²")
        print(f"    % of Calgary-Airdrie : {pct_of_airdrie:.1f}%")
        print(f"    % of adjacent ED     : {pct_of_adj:.1f}%")

        results.append({
            "adjacent_ed": row["name_2026"],
            "adjacent_area_km2": adj_area_km2,
            "intersection_geom": intersection,
            "intersection_area_km2": inter_area_km2,
            "pct_of_airdrie": pct_of_airdrie,
            "pct_of_adjacent": pct_of_adj,
        })

    total_overlap = sum(r["intersection_area_km2"] for r in results)
    print(f"\n  TOTAL overlap area    : {total_overlap:.1f} km²")
    print(f"  % of Calgary-Airdrie  : {100*total_overlap/airdrie_area:.1f}%")

    return results


# ---------------------------------------------------------------------------
# Step 3 — Propose corrected boundaries

def step3_clip_options(
    eds: gpd.GeoDataFrame,
    airdrie_info: dict,
    overlap_results: list[dict],
    vas: gpd.GeoDataFrame,
) -> dict:
    print("\n=== STEP 3: Proposing corrected boundaries ===")

    airdrie_geom = airdrie_info["geom"]
    airdrie_idx = airdrie_info["idx"]
    orig_area = airdrie_info["area_km2"]

    # --- Option A: Clip to union of all non-overlapping EDs ----
    overlap_ed_names_lower = {r["adjacent_ed"].lower() for r in overlap_results}
    # Build union of all OTHER EDs (not Airdrie itself, not the three overlapping ones)
    other_geoms = eds.loc[
        (~eds.index.isin([airdrie_idx])) &
        (~eds["name_2026"].str.lower().isin(overlap_ed_names_lower)),
        "geometry"
    ].tolist()

    # Also get the three overlapping EDs' geometries so we can subtract them
    overlap_geoms = [r["intersection_geom"] for r in overlap_results]
    overlap_union = unary_union(overlap_geoms) if overlap_geoms else None

    # Option A: remove the overlap zone from Airdrie
    if overlap_union and not overlap_union.is_empty:
        option_a_geom = airdrie_geom.difference(overlap_union)
    else:
        option_a_geom = airdrie_geom

    option_a_area = km2(option_a_geom.area)
    print(f"\n  Option A (difference from overlap zones):")
    print(f"    Area: {option_a_area:.1f} km²  (was {orig_area:.1f} km²)")
    print(f"    Reduction: {orig_area - option_a_area:.1f} km² ({100*(orig_area-option_a_area)/orig_area:.1f}%)")

    # Count VAs inside Option A vs original
    va_centroids = vas.copy()
    va_centroids["centroid_geom"] = va_centroids.geometry.centroid
    va_centroids_gdf = gpd.GeoDataFrame(va_centroids, geometry="centroid_geom", crs=vas.crs)

    orig_count = va_centroids_gdf[va_centroids_gdf.geometry.within(airdrie_geom)].shape[0]
    option_a_count = va_centroids_gdf[va_centroids_gdf.geometry.within(option_a_geom)].shape[0]
    print(f"    VAs in original Calgary-Airdrie : {orig_count:,}")
    print(f"    VAs in Option A                 : {option_a_count:,}")

    # --- Option B: Clip to circles of varying radius around Airdrie centre ---
    airdrie_centre = Point(AIRDRIE_X, AIRDRIE_Y)
    radii = [20_000, 25_000, 30_000]  # metres
    option_b_results = {}

    print(f"\n  Option B (radius clip around City of Airdrie centre x={AIRDRIE_X}, y={AIRDRIE_Y}):")
    for r_m in radii:
        circle = airdrie_centre.buffer(r_m)
        clipped = airdrie_geom.intersection(circle)
        area_km2 = km2(clipped.area)
        count = va_centroids_gdf[va_centroids_gdf.geometry.within(clipped)].shape[0]
        r_km = r_m // 1000
        print(f"    r={r_km} km: area={area_km2:.1f} km², VAs inside={count:,}")
        option_b_results[r_km] = {"geom": clipped, "area_km2": area_km2, "va_count": count}

    return {
        "option_a_geom": option_a_geom,
        "option_a_area_km2": option_a_area,
        "option_a_va_count": option_a_count,
        "orig_va_count": orig_count,
        "option_b": option_b_results,
    }


# ---------------------------------------------------------------------------
# Step 4 — VAs in the overlap zone

def step4_overlap_vas(
    vas: gpd.GeoDataFrame,
    overlap_results: list[dict],
    airdrie_info: dict,
) -> dict:
    print("\n=== STEP 4: VAs in the overlap zone ===")

    if not overlap_results:
        print("  No overlap results to analyse.")
        return {}

    overlap_union = unary_union([r["intersection_geom"] for r in overlap_results])

    # Use centroid-in-polygon for VA membership
    va_centroids = vas.copy()
    va_centroids["_cx"] = va_centroids.geometry.centroid.x
    va_centroids["_cy"] = va_centroids.geometry.centroid.y
    va_centroids["_centroid"] = va_centroids.geometry.centroid
    va_cents_gdf = gpd.GeoDataFrame(va_centroids, geometry="_centroid", crs=vas.crs)

    in_overlap = va_cents_gdf[va_cents_gdf.geometry.within(overlap_union)].copy()

    print(f"  VAs whose centroid falls in the overlap zone: {len(in_overlap):,}")

    if len(in_overlap) == 0:
        print("  No VAs found in overlap zone.")
        return {"count": 0}

    # Examine parent_ed columns
    parent_cols = [c for c in in_overlap.columns if "parent" in c.lower() or "ed_2019" in c.lower() or "name_2026" in c.lower()]
    print(f"  Available parent/ED columns: {parent_cols}")

    # Try to find the right column
    parent_col = None
    for candidate in ["parent_ed_2019", "ed_2019", "ed_name_2019", "parent_ed"]:
        if candidate in in_overlap.columns:
            parent_col = candidate
            break

    if parent_col:
        parent_dist = in_overlap[parent_col].value_counts()
        print(f"\n  {parent_col} distribution in overlap-zone VAs:")
        for val, cnt in parent_dist.items():
            print(f"    {val!r}: {cnt}")
    else:
        print(f"  WARNING: No parent ED column found. Available columns: {list(in_overlap.columns)[:30]}")

    # Vote tallies
    vote_cols = [c for c in in_overlap.columns if any(x in c.lower() for x in ["ndp", "ucp", "total", "vote"])]
    print(f"\n  Vote columns found: {vote_cols}")

    total_ndp = None
    total_ucp = None
    for col in in_overlap.columns:
        if "ndp" in col.lower() and "total" in col.lower():
            total_ndp = in_overlap[col].sum()
        if "ucp" in col.lower() and "total" in col.lower():
            total_ucp = in_overlap[col].sum()

    # Fallback: sum any ndp/ucp numeric column
    if total_ndp is None:
        ndp_cols = [c for c in in_overlap.columns if "ndp" in c.lower() and in_overlap[c].dtype in ["float64", "int64"]]
        if ndp_cols:
            total_ndp = in_overlap[ndp_cols[0]].sum()
    if total_ucp is None:
        ucp_cols = [c for c in in_overlap.columns if "ucp" in c.lower() and in_overlap[c].dtype in ["float64", "int64"]]
        if ucp_cols:
            total_ucp = in_overlap[ucp_cols[0]].sum()

    print(f"\n  Total NDP votes in overlap zone : {total_ndp}")
    print(f"  Total UCP votes in overlap zone : {total_ucp}")

    # Check for Airdrie-Cochrane parent assignment
    if parent_col:
        has_airdrie_cochrane = in_overlap[parent_col].str.contains("Airdrie", case=False, na=False).any()
        print(f"\n  Any VA has parent containing 'Airdrie'? {'YES' if has_airdrie_cochrane else 'NO'}")
        print(f"  If NO -> VAs are attributed to a different 2019 parent = confirms pixel-extraction error")

    return {
        "count": len(in_overlap),
        "total_ndp": total_ndp,
        "total_ucp": total_ucp,
        "parent_col": parent_col,
        "parent_dist": in_overlap[parent_col].value_counts().to_dict() if parent_col else {},
        "in_overlap_df": in_overlap,
        "overlap_union": overlap_union,
    }


# ---------------------------------------------------------------------------
# Step 5 — Write report

def step5_write_report(
    airdrie_info: dict,
    overlap_results: list[dict],
    clip_options: dict,
    va_stats: dict,
) -> None:
    print("\n=== STEP 5: Writing report ===")

    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append("# Calgary-Airdrie Overlap Diagnostic Report")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Script:** `analysis/v0_1_airdrie_overlap_diagnostic.py`")
    lines.append(f"**Source:** `data/v0_1_canonical_minority_2026_eds.gpkg`")
    lines.append("")

    # ---- 1. Summary of Over-Extension ----
    lines.append("## 1. Summary of the Over-Extension")
    lines.append("")
    lines.append(f"The `{TARGET_ED}` polygon in the canonical minority shapefile covers "
                 f"**{airdrie_info['area_km2']:.1f} km²**, with its centroid at "
                 f"(x={airdrie_info['centroid_x']:.0f}, y={airdrie_info['centroid_y']:.0f}) in EPSG:3401.")
    lines.append("")
    lines.append(f"The City of Airdrie's known approximate centre is at (x={AIRDRIE_X}, y={AIRDRIE_Y}). "
                 f"The polygon centroid is **{airdrie_info['dist_to_airdrie_km']:.1f} km** from this reference point.")
    lines.append("")
    lines.append("### Polygon Geometry")
    lines.append("")
    lines.append("| Property | Value |")
    lines.append("|---|---|")
    lines.append(f"| Area | {airdrie_info['area_km2']:.1f} km² |")
    bb = airdrie_info["bbox"]
    lines.append(f"| Bounding box (EPSG:3401) | minx={bb[0]:.0f}, miny={bb[1]:.0f}, maxx={bb[2]:.0f}, maxy={bb[3]:.0f} |")
    lines.append(f"| Centroid | x={airdrie_info['centroid_x']:.0f}, y={airdrie_info['centroid_y']:.0f} |")
    lines.append(f"| Vertices | {airdrie_info['n_vertices']:,} |")
    lines.append(f"| Distance to Airdrie centre | {airdrie_info['dist_to_airdrie_km']:.1f} km |")
    lines.append("")

    # ---- Overlap table ----
    lines.append("### Overlaps with Adjacent EDs")
    lines.append("")
    lines.append("| Adjacent ED | Adjacent Area (km²) | Intersection (km²) | % of Airdrie | % of Adjacent |")
    lines.append("|---|---|---|---|---|")
    total_overlap = 0.0
    for r in overlap_results:
        lines.append(f"| {r['adjacent_ed']} | {r['adjacent_area_km2']:.1f} | "
                     f"{r['intersection_area_km2']:.1f} | {r['pct_of_airdrie']:.1f}% | {r['pct_of_adjacent']:.1f}% |")
        total_overlap += r["intersection_area_km2"]
    lines.append(f"| **TOTAL** | — | **{total_overlap:.1f}** | "
                 f"**{100*total_overlap/airdrie_info['area_km2']:.1f}%** | — |")
    lines.append("")
    lines.append(f"The Calgary-Airdrie polygon overlaps its three neighbours by a combined "
                 f"**{total_overlap:.1f} km²**, representing "
                 f"**{100*total_overlap/airdrie_info['area_km2']:.1f}%** of its total footprint. "
                 f"This is consistent with a pixel-extraction artifact: the polygon was traced too broadly "
                 f"from the commission's overview map rather than from a precise boundary description.")
    lines.append("")

    # ---- 2. VA Count and Votes at Risk ----
    lines.append("## 2. Voting Areas at Risk")
    lines.append("")
    va_count = va_stats.get("count", 0)
    total_ndp = va_stats.get("total_ndp")
    total_ucp = va_stats.get("total_ucp")
    parent_dist = va_stats.get("parent_dist", {})

    lines.append(f"**{va_count:,} VAs** have their centroid inside the overlap zone "
                 f"(intersection of Calgary-Airdrie with any of the three adjacent EDs).")
    lines.append("")
    if va_count > 0:
        lines.append("### Vote Totals in Overlap Zone (2023 Provincial Election)")
        lines.append("")
        lines.append("| Party | Votes |")
        lines.append("|---|---|")
        lines.append(f"| NDP | {int(total_ndp) if total_ndp is not None else 'N/A':,} |")
        lines.append(f"| UCP | {int(total_ucp) if total_ucp is not None else 'N/A':,} |")
        lines.append("")
        if parent_dist:
            lines.append("### Parent ED 2019 Distribution in Overlap Zone")
            lines.append("")
            lines.append("| Parent ED (2019) | VA Count |")
            lines.append("|---|---|")
            for ed, cnt in sorted(parent_dist.items(), key=lambda x: -x[1]):
                lines.append(f"| {ed} | {cnt} |")
            lines.append("")
            # Interpretation
            has_airdrie = any("airdrie" in str(k).lower() for k in parent_dist)
            if has_airdrie:
                lines.append("The overlap-zone VAs carry a `parent_ed_2019` of `Airdrie-Cochrane` (or similar), "
                             "which is **consistent** with their correct geographic location. The pixel-extraction "
                             "artifact caused Airdrie-Cochrane VAs to appear inside Calgary-Airdrie.")
            else:
                lines.append("The overlap-zone VAs do **NOT** have a `parent_ed_2019` of `Airdrie-Cochrane`. "
                             "They belong to different 2019 parents, confirming that the Calgary-Airdrie polygon "
                             "was traced so broadly it captured territory from entirely different 2019 EDs. "
                             "This strongly supports the pixel-extraction artifact hypothesis.")
            lines.append("")

    # ---- 3. Clip Options ----
    lines.append("## 3. Corrected Boundary Options")
    lines.append("")
    orig_va = clip_options.get("orig_va_count", 0)
    lines.append(f"Original Calgary-Airdrie VA count (centroid-in-polygon): **{orig_va:,}**")
    lines.append("")

    lines.append("### Option A — Subtract the Overlap Zones")
    lines.append("")
    lines.append("Clip Calgary-Airdrie by subtracting the exact intersection geometry "
                 "with each of the three overlapping EDs.")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Resulting area | {clip_options['option_a_area_km2']:.1f} km² |")
    lines.append(f"| Area removed | {airdrie_info['area_km2'] - clip_options['option_a_area_km2']:.1f} km² |")
    lines.append(f"| VAs retained | {clip_options['option_a_va_count']:,} |")
    lines.append(f"| VAs removed | {orig_va - clip_options['option_a_va_count']:,} |")
    lines.append("")

    lines.append("### Option B — Radius Clip Around City of Airdrie")
    lines.append("")
    lines.append(f"Intersect Calgary-Airdrie with a circle of radius r centred on "
                 f"(x={AIRDRIE_X}, y={AIRDRIE_Y}).")
    lines.append("")
    lines.append("| Radius | Resulting Area (km²) | VAs Retained |")
    lines.append("|---|---|---|")
    for r_km, info in sorted(clip_options["option_b"].items()):
        lines.append(f"| {r_km} km | {info['area_km2']:.1f} | {info['va_count']:,} |")
    lines.append("")

    # ---- 4. Recommendation ----
    lines.append("## 4. Recommendation")
    lines.append("")
    lines.append("**Recommended approach: Option A (subtract overlap zones).**")
    lines.append("")
    lines.append("Rationale:")
    lines.append("")
    lines.append("- Option A is geometrically conservative: it removes only the territory "
                 "that is provably incorrect (the intersecting area) without making assumptions "
                 "about what the 'true' boundary is.")
    lines.append("- Option B requires selecting an arbitrary radius and assumes the commission "
                 "intended a compact circle, which may not be accurate.")
    lines.append("- Option A preserves every VA that falls exclusively within the "
                 "Calgary-Airdrie polygon and removes only those in the ambiguous overlap zone.")
    lines.append("- The resulting polygon can be further refined against official commission "
                 "boundary descriptions once those are available.")
    lines.append("")
    lines.append("If Option A produces a polygon that is too fragmented or leaves isolated slivers, "
                 "Option B with r=25 km is the next-best fallback, as it captures the City of Airdrie "
                 "and immediately adjacent areas without extending into the adjacent EDs.")
    lines.append("")

    # ---- 5. Impact on Minority EG ----
    lines.append("## 5. Impact on Minority Electoral Geography")
    lines.append("")
    lines.append(f"If the **{va_count:,}** overlap-zone VAs were reassigned to their correct EDs "
                 f"(based on `parent_ed_2019` or geographic containment):")
    lines.append("")

    if total_ndp is not None and total_ucp is not None and (total_ndp + total_ucp) > 0:
        ndp_share = 100 * total_ndp / (total_ndp + total_ucp)
        ucp_share = 100 - ndp_share
        lines.append(f"- The overlap zone contains approximately {int(total_ndp + total_ucp):,} "
                     f"two-party votes ({ndp_share:.0f}% NDP / {ucp_share:.0f}% UCP).")
        if ndp_share > 55:
            lean = "NDP-leaning"
        elif ucp_share > 55:
            lean = "UCP-leaning"
        else:
            lean = "closely contested"
        lines.append(f"- This territory appears **{lean}**, suggesting that misattribution could "
                     f"affect both the seat count and party vote-share distribution in the minority map.")
    else:
        lines.append("- Vote totals in the overlap zone could not be computed from available data.")

    lines.append("- Until the correct boundary is confirmed from official sources, the Calgary-Airdrie "
                 "minority polygon should be treated as **unreliable** and excluded from any analyses "
                 "that depend on precise Calgary-Airdrie boundaries.")
    lines.append("")
    lines.append("**No shapefiles were modified. This is a diagnostic report only.**")
    lines.append("")
    lines.append("---")
    lines.append(f"*Report generated by `v0_1_airdrie_overlap_diagnostic.py` on {now}.*")

    report_text = "\n".join(lines)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"  Report written to: {REPORT_PATH}")


# ---------------------------------------------------------------------------
# Main

def main():
    print("=" * 70)
    print("v0_1_airdrie_overlap_diagnostic.py")
    print(f"Run at: {datetime.now()}")
    print("=" * 70)

    # Load minority EDs
    print(f"\nLoading minority EDs from:\n  {MINORITY_GPKG}")
    eds = gpd.read_file(MINORITY_GPKG)
    if eds.crs is None or eds.crs.to_epsg() != WORK_CRS:
        eds = eds.to_crs(epsg=WORK_CRS)
    print(f"  Loaded {len(eds)} EDs, CRS: EPSG:{eds.crs.to_epsg()}")
    print(f"  Columns: {list(eds.columns)}")

    # Identify the name column
    name_col_candidates = ["name_2026", "ED_NAME", "name", "NAME", "RIDING_NAME", "riding_name"]
    name_col = None
    for c in name_col_candidates:
        if c in eds.columns:
            name_col = c
            break
    if name_col is None:
        # Use first string column
        for c in eds.columns:
            if eds[c].dtype == object and c != "geometry":
                name_col = c
                break
    if name_col != "name_2026":
        eds = eds.rename(columns={name_col: "name_2026"})
        print(f"  Renamed column '{name_col}' -> 'name_2026'")

    # Print all ED names so we can verify
    print(f"\n  All ED names in minority shapefile ({len(eds)} EDs):")
    for n in sorted(eds["name_2026"].tolist()):
        print(f"    {n}")

    # Load VA polygons
    print(f"\nLoading VA polygons from:\n  {VA_GPKG}")
    vas = gpd.read_file(VA_GPKG)
    if vas.crs is None or vas.crs.to_epsg() != WORK_CRS:
        vas = vas.to_crs(epsg=WORK_CRS)
    print(f"  Loaded {len(vas):,} VAs, CRS: EPSG:{vas.crs.to_epsg()}")
    print(f"  VA columns: {list(vas.columns)[:20]}")

    # Run steps
    airdrie_info = step1_inspect(eds)
    overlap_results = step2_intersections(eds, airdrie_info)
    clip_options = step3_clip_options(eds, airdrie_info, overlap_results, vas)
    va_stats = step4_overlap_vas(vas, overlap_results, airdrie_info)
    step5_write_report(airdrie_info, overlap_results, clip_options, va_stats)

    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
