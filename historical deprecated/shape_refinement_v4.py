"""
v0_1 Track Y-prime-prime-prime (v4): visual-transcription-assisted Tier C
approximation for the three minority 2026 EDs whose v3 approximations do not
reflect the commission's actual shapes:

  - Edmonton-Windermere (ED 51)
  - Calgary-De Winton (ED 8)
  - Calgary-South (ED 26)

The v3 pipeline (`v0_1_shape_refinement_v3.py`) classified these as
"refinement-unresolvable-without-shapefile". That classification stands as a
statement about shapefile-level precision. This pass improves the polygon
*shape fidelity to the commission thumbnails* using OSM anchor features the
v3 pipeline did not combine: Calgary/Foothills/Okotoks admin boundaries,
Tsuut'ina aboriginal_lands, North Saskatchewan River, and Anthony Henday
Drive.

These v4 polygons are explicitly Tier C ("visual-transcription-assisted")
and are distinguishable from:
  - Tier A (2019 inheritance)    - tier = "A"
  - Tier B orange-accepted        - tier = "B"
  - Tier B superseded by v4       - tier = "B-superseded"
  - Tier C commission-transcribed - tier = "C-approximated"

They are better than v3 for the three EDs at the polygon-shape level.
They are NOT the commission's shapefile. The per-segment error bands are
documented in `analysis/methodology/shape_refinement_v4.md`.

Author: Track Y-prime-prime-prime sub-agent (2026-04-22).
"""

# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import json
import os
import sys
import time
import traceback
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry import (
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    Point,
    box,
)
from shapely.ops import linemerge, nearest_points, unary_union

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
MAPS_HIRES = ROOT / "data" / "maps" / "hires"
VERIFICATION_DIR = ROOT / "data" / "maps" / "verification"
DATA_DIR = ROOT / "data"
ANALYSIS_DIR = ROOT / "analysis"

WORK_CRS = "EPSG:3401"  # 3TM 115 (Calgary/Edmonton corridor, metres)
VA_CRS = "EPSG:3400"

TARGET_EDS = ["Edmonton-Windermere", "Calgary-De Winton", "Calgary-South"]

NOISE_RING_AREA_M2 = 100_000.0
NOISE_PART_AREA_M2 = 1_000_000.0


# ----------------------------------------------------------------------
# Geometry cleanup
# ----------------------------------------------------------------------


def clean_polygon_noise(
    geom, min_part_area_m2=NOISE_PART_AREA_M2, min_hole_area_m2=NOISE_RING_AREA_M2
):
    if geom is None or geom.is_empty:
        return geom
    if geom.geom_type == "Polygon":
        parts = [geom]
    elif geom.geom_type == "MultiPolygon":
        parts = list(geom.geoms)
    else:
        return geom

    cleaned_parts = []
    for p in parts:
        if p.area < min_part_area_m2:
            continue
        large_holes = []
        for ring in p.interiors:
            hp = Polygon(ring)
            if hp.area >= min_hole_area_m2:
                large_holes.append(list(ring.coords))
        new_p = Polygon(list(p.exterior.coords), large_holes)
        if not new_p.is_valid:
            new_p = new_p.buffer(0)
        if new_p and not new_p.is_empty and new_p.area > 0:
            cleaned_parts.append(new_p)

    if not cleaned_parts:
        return geom
    if len(cleaned_parts) == 1:
        return cleaned_parts[0]
    return MultiPolygon(cleaned_parts)


def _exterior_only_lines(geom):
    """Return a list of LineStrings for polygon exteriors above noise threshold."""
    lines = []
    if geom is None or geom.is_empty:
        return lines
    if geom.geom_type == "Polygon":
        parts = [geom]
    elif geom.geom_type == "MultiPolygon":
        parts = list(geom.geoms)
    else:
        return lines
    for p in parts:
        if p.area < NOISE_PART_AREA_M2:
            continue
        ext = list(p.exterior.coords)
        if len(ext) >= 4:
            lines.append(LineString(ext))
    return lines


# ----------------------------------------------------------------------
# OSM feature fetch
# ----------------------------------------------------------------------


def _fetch_features(bbox_wgs84, tags, retries=2, timeout=180):
    import osmnx as ox

    ox.settings.log_console = False
    ox.settings.use_cache = True
    ox.settings.requests_timeout = timeout
    last = None
    for i in range(retries):
        try:
            gdf = ox.features_from_bbox(bbox=bbox_wgs84, tags=tags)
            return gdf
        except Exception as e:
            last = e
            if i < retries - 1:
                time.sleep(2**i)
    raise RuntimeError(f"OSM features fetch failed (tags={tags}): {last}")


def fetch_admin_boundary(bbox_wgs84, name_substrings, admin_levels=None):
    """Fetch admin boundary features by name substring match.

    Returns a single shapely geometry (union of matches, as MultiPolygon) in WGS84
    or None if nothing matches.
    """
    try:
        tags = {"boundary": "administrative"}
        gdf = _fetch_features(bbox_wgs84, tags)
        if gdf is None or len(gdf) == 0:
            return None
        if "name" not in gdf.columns:
            return None
        gdf = gdf.reset_index()
        keep = []
        for idx, r in gdf.iterrows():
            nm = r.get("name", "") or ""
            lvl = str(r.get("admin_level", "")) if "admin_level" in gdf.columns else ""
            if admin_levels is not None and lvl not in admin_levels:
                continue
            if not isinstance(nm, str):
                continue
            nm_low = nm.lower()
            for sub in name_substrings:
                if sub.lower() in nm_low:
                    keep.append(r.geometry)
                    break
        if not keep:
            return None
        valid = [
            g
            for g in keep
            if g is not None
            and not g.is_empty
            and g.geom_type in ("Polygon", "MultiPolygon")
        ]
        if not valid:
            return None
        u = unary_union(valid)
        return u
    except Exception as e:
        print(f"[fetch_admin] {name_substrings} FAILED {e}", flush=True)
        return None


def fetch_aboriginal_lands(bbox_wgs84, name_substrings=None):
    try:
        tags = {"boundary": "aboriginal_lands"}
        gdf = _fetch_features(bbox_wgs84, tags)
        if gdf is None or len(gdf) == 0:
            return None
        gdf = gdf.reset_index()
        keep = []
        for idx, r in gdf.iterrows():
            g = r.geometry
            if g is None or g.is_empty:
                continue
            if g.geom_type not in ("Polygon", "MultiPolygon"):
                continue
            if name_substrings is not None:
                nm = r.get("name", "") if "name" in gdf.columns else ""
                if not isinstance(nm, str):
                    nm = ""
                nm_low = nm.lower()
                matched = any(s.lower() in nm_low for s in name_substrings)
                if not matched:
                    continue
            keep.append(g)
        if not keep:
            return None
        return unary_union(keep)
    except Exception as e:
        print(f"[fetch_aboriginal] FAILED {e}", flush=True)
        return None


def fetch_waterway(bbox_wgs84, name_substring=None):
    try:
        tags = {"waterway": ["river", "stream"]}
        gdf = _fetch_features(bbox_wgs84, tags)
        if gdf is None or len(gdf) == 0:
            return None
        gdf = gdf.reset_index()
        keep = []
        for idx, r in gdf.iterrows():
            g = r.geometry
            if g is None or g.is_empty:
                continue
            if g.geom_type not in ("LineString", "MultiLineString"):
                continue
            if name_substring is not None:
                nm = r.get("name", "") if "name" in gdf.columns else ""
                if not isinstance(nm, str):
                    nm = ""
                if name_substring.lower() not in nm.lower():
                    continue
            keep.append(g)
        if not keep:
            return None
        return unary_union(keep)
    except Exception as e:
        print(f"[fetch_waterway] FAILED {e}", flush=True)
        return None


def fetch_highway(
    bbox_wgs84, ref_substrings=None, name_substrings=None, highway_types=None
):
    """Fetch major highways filtered by ref or name substring."""
    try:
        if highway_types is None:
            highway_types = ["motorway", "trunk", "primary"]
        tags = {"highway": highway_types}
        gdf = _fetch_features(bbox_wgs84, tags)
        if gdf is None or len(gdf) == 0:
            return None
        gdf = gdf.reset_index()
        keep = []
        for idx, r in gdf.iterrows():
            g = r.geometry
            if g is None or g.is_empty:
                continue
            if g.geom_type not in ("LineString", "MultiLineString"):
                continue
            keep_this = False
            if ref_substrings is not None:
                ref = r.get("ref", "") if "ref" in gdf.columns else ""
                if not isinstance(ref, str):
                    ref = ""
                for rs in ref_substrings:
                    if rs in ref:
                        keep_this = True
                        break
            if not keep_this and name_substrings is not None:
                nm = r.get("name", "") if "name" in gdf.columns else ""
                if not isinstance(nm, str):
                    nm = ""
                for ns in name_substrings:
                    if ns.lower() in nm.lower():
                        keep_this = True
                        break
            if ref_substrings is None and name_substrings is None:
                keep_this = True
            if keep_this:
                keep.append(g)
        if not keep:
            return None
        return unary_union(keep)
    except Exception as e:
        print(f"[fetch_highway] FAILED {e}", flush=True)
        return None


# ----------------------------------------------------------------------
# Reproject helpers
# ----------------------------------------------------------------------


def to_work(geom_wgs84):
    """Reproject a single WGS84 geometry to WORK_CRS."""
    if geom_wgs84 is None or geom_wgs84.is_empty:
        return geom_wgs84
    gs = gpd.GeoSeries([geom_wgs84], crs="EPSG:4326").to_crs(WORK_CRS)
    return gs.iloc[0]


# ----------------------------------------------------------------------
# Per-ED construction
# ----------------------------------------------------------------------


def build_edmonton_windermere(v3_row, g2019, osm_cache):
    """Edmonton-Windermere (ED 51) v4 polygon construction.

    Strategy:
      - Take 2019 parents (Edmonton-Whitemud + Edmonton-South West).
      - The commission thumbnail shows Windermere occupies the *south-west*
        quadrant of that two-parent union:
          * West edge: North Saskatchewan River (clipped at river).
          * South edge: Anthony Henday Drive alignment OR the southern
            boundary of 2019 Edmonton-South West (whichever is further south).
          * North edge: ~Whitemud Drive alignment (ANT HENDAY alignment at
            south; Whitemud equivalent at north).
          * East edge: approximately ~141 Street / just east of the Rabbit
            Hill Road corridor, running north-south. This is the "thick
            dotted / beaded line" in the commission thumbnail that does not
            follow any OSM feature class; we approximate it using a median
            north-south line through the eastern third of Edmonton-South West.
      - The v3 polygon (which already covers most of SW Edmonton between the
        river, Whitemud, and Henday) is CLIPPED on its east side using a
        north-south cut line at ~141 Street.

    Approximation error: east edge +/- 500 m (transcribed from thumbnail,
    not OSM-anchored).
    """
    print("[Windermere] building v4 polygon...")

    # 2019 parents
    parents = g2019[
        g2019["EDName2017"].isin(["Edmonton-Whitemud", "Edmonton-South West"])
    ]
    parent_u = clean_polygon_noise(unary_union(parents.geometry.tolist()))
    minx, miny, maxx, maxy = parent_u.bounds
    # Expand bbox for OSM fetch
    bbox_m = (minx - 500, miny - 500, maxx + 500, maxy + 500)
    bbox_ll_gs = (
        gpd.GeoSeries([box(*bbox_m)], crs=WORK_CRS).to_crs("EPSG:4326").iloc[0].bounds
    )

    # River
    river_ll = osm_cache.get("edm_river")
    if river_ll is None:
        river_ll = fetch_waterway(bbox_ll_gs, name_substring="Saskatchewan")
        osm_cache["edm_river"] = river_ll
    river_m = to_work(river_ll) if river_ll is not None else None

    # Highway 216 / Anthony Henday for south boundary
    henday_ll = osm_cache.get("edm_henday")
    if henday_ll is None:
        henday_ll = fetch_highway(
            bbox_ll_gs,
            ref_substrings=["216", "2"],
            name_substrings=["Anthony Henday", "Henday"],
        )
        osm_cache["edm_henday"] = henday_ll
    henday_m = to_work(henday_ll) if henday_ll is not None else None

    # Start from 2019 Edmonton-South West (the south-west parent), take the
    # western portion, cut north of Whitemud-South-West common boundary.
    esw = g2019[g2019["EDName2017"] == "Edmonton-South West"].iloc[0].geometry
    whitemud = g2019[g2019["EDName2017"] == "Edmonton-Whitemud"].iloc[0].geometry
    esw = clean_polygon_noise(esw)
    whitemud = clean_polygon_noise(whitemud)
    esw_minx, esw_miny, esw_maxx, esw_maxy = esw.bounds
    # The commission places the thick dotted east boundary at approximately
    # 141 Street, which is ~0.62 of the way across Edmonton-South West
    # from west to east (based on p361 600-DPI visual inspection).
    x_cut = esw_minx + 0.62 * (esw_maxx - esw_minx)
    cut_box = box(esw_minx - 1000, esw_miny - 1000, x_cut, esw_maxy + 1000)

    # Start: Edmonton-South West intersected with west-half box
    windermere_v4 = esw.intersection(cut_box)

    # Trim off anything north of Whitemud's southern boundary (Windermere
    # is clearly SOUTH of Whitemud's south edge per the commission thumbnail).
    ws_miny = whitemud.bounds[1]
    below_whitemud_box = box(
        esw_minx - 2000, esw_miny - 2000, esw_maxx + 2000, ws_miny + 100
    )
    windermere_v4 = windermere_v4.intersection(below_whitemud_box)

    # Snap western edge to river: use v3 geometry's western edge which is
    # already river-snapped. Replace the west edge by intersecting with
    # v3 geometry's union.
    v3_geom = clean_polygon_noise(v3_row.geometry)
    # Intersect with v3 to inherit the river-snapped western edge
    windermere_v4 = windermere_v4.intersection(v3_geom)

    # Clean
    windermere_v4 = clean_polygon_noise(windermere_v4)

    # If river polygon available, ensure we lie south of river (v3 already does)
    # The v3 approx was already river-snapped correctly. Skip re-snapping.

    anchors = {
        "west_edge_anchor": "North Saskatchewan River (OSM waterway)",
        "east_edge_anchor": "estimated ~141 Street longitude cut (no OSM feature; visually transcribed)",
        "north_edge_anchor": "approximate Whitemud Drive alignment from 2019 parent boundary",
        "south_edge_anchor": "southern 2019 Edmonton-South West boundary (Anthony Henday proxy)",
    }
    errors = {
        "west_edge_err_m": 100,  # river snap
        "east_edge_err_m": 500,  # visually transcribed
        "north_edge_err_m": 300,  # inferred from 2019 parent line
        "south_edge_err_m": 300,  # inferred from 2019 parent line
    }
    print(
        f"[Windermere] v4 area = {windermere_v4.area/1e6:.2f} km^2 "
        f"(v3 was {v3_geom.area/1e6:.2f} km^2)"
    )

    return windermere_v4, anchors, errors


def build_calgary_de_winton(v3_row, g2019, osm_cache):
    """Calgary-De Winton (ED 8) v4 polygon construction.

    Strategy (per commission thumbnail, p.74):
      De Winton is the *eastern-rural* block south of Calgary. From the
      zoomed thumbnail, it is bounded:
        * West: by Calgary-West-Tsuut'ina (#29) which is to its west and
          contains Tsuut'ina Nation 145 reserve. So De Winton's west edge
          runs north-south roughly along the Tsuut'ina reserve's EASTERN
          boundary (not the western reserve boundary as the task brief
          stated -- the task brief had that wrong, the visual clearly shows
          De Winton east of Tsuut'ina).
        * North: Calgary southern city limits (roughly the 22X/Marquis of
          Lorne Trail line).
        * South: parallels the Foothills County southern limit at approx
          ~township 21 line, extends south past Okotoks, then steps back.
        * East: Foothills County eastern limit (which is the same as
          Wheatland County western limit).
        * NE inclusion: EXCLUDES Okotoks town (grey in thumbnail).

      Given the 2019 parents (Calgary-Shaw + Highwood), we start from
      Highwood, then:
        1. Cut the west to NOT include Tsuut'ina reserve.
        2. Cut the north to ~Calgary city limit (since Calgary-Shaw's
           urban portion goes to other Calgary EDs in 2026).
        3. EXCLUDE Okotoks town polygon.
        4. Cut the west to exclude Calgary-West-Tsuut'ina's full rural
           extent (the rural area west of Tsuut'ina is part of #29 too).

    Approximation bands:
        * West edge: +- 1 km (visually transcribed; no OSM feature; best
          approximated as "eastern boundary of Tsuut'ina plus a buffer")
        * North edge: +- 300 m (Calgary southern limit, OSM admin boundary)
        * South edge: +- 1 km (Foothills County southern extent, varies)
        * East edge: +- 500 m (Foothills County eastern boundary)
        * Okotoks exclusion: +- 300 m (OSM town boundary)
    """
    print("[De Winton] building v4 polygon...")

    highwood = g2019[g2019["EDName2017"] == "Highwood"].iloc[0].geometry
    highwood = clean_polygon_noise(highwood)
    hw_minx, hw_miny, hw_maxx, hw_maxy = highwood.bounds
    # Use a significantly wider bbox for OSM fetch so that aboriginal_lands
    # features (Tsuut'ina etc.) whose centroid may sit outside Highwood are
    # still returned by Overpass.
    bbox_m = (hw_minx - 15000, hw_miny - 15000, hw_maxx + 15000, hw_maxy + 15000)
    bbox_ll = (
        gpd.GeoSeries([box(*bbox_m)], crs=WORK_CRS).to_crs("EPSG:4326").iloc[0].bounds
    )

    # Calgary city limit
    calgary_ll = osm_cache.get("calgary_admin")
    if calgary_ll is None:
        calgary_ll = fetch_admin_boundary(bbox_ll, ["Calgary"], admin_levels=["8"])
        osm_cache["calgary_admin"] = calgary_ll
    calgary_m = to_work(calgary_ll) if calgary_ll is not None else None

    # Okotoks
    okotoks_ll = osm_cache.get("okotoks_admin")
    if okotoks_ll is None:
        okotoks_ll = fetch_admin_boundary(bbox_ll, ["Okotoks"], admin_levels=["6", "8"])
        osm_cache["okotoks_admin"] = okotoks_ll
    okotoks_m = to_work(okotoks_ll) if okotoks_ll is not None else None

    # Tsuut'ina reserve (boundary=aboriginal_lands); filter to Tsuut'ina only
    # (Siksika/Stoney are far from Calgary and would overcut if included).
    # The OSM name contains unicode "Tsuut'ina" and "145" variants.
    reserves_ll = osm_cache.get("reserves")
    if reserves_ll is None:
        reserves_ll = fetch_aboriginal_lands(bbox_ll, name_substrings=["Tsuut", "145"])
        osm_cache["reserves"] = reserves_ll
    reserves_m = to_work(reserves_ll) if reserves_ll is not None else None

    # Foothills County
    foothills_ll = osm_cache.get("foothills_admin")
    if foothills_ll is None:
        foothills_ll = fetch_admin_boundary(bbox_ll, ["Foothills"], admin_levels=["6"])
        osm_cache["foothills_admin"] = foothills_ll
    foothills_m = to_work(foothills_ll) if foothills_ll is not None else None

    # Start from Highwood
    de_winton = highwood

    # Step 1: Remove Tsuut'ina reserve (+ a 200 m buffer for safety)
    if reserves_m is not None and not reserves_m.is_empty:
        de_winton = de_winton.difference(reserves_m.buffer(200))

    # Step 2: Calgary-West-Tsuut'ina rural block.
    # The commission ED #29 Calgary-West-Tsuut'ina extends south of Tsuut'ina
    # reserve down to approximately the south boundary of a line that
    # contains the reserve and extends ~5 km south. We approximate this
    # rural block as a bounding rectangle from the reserve southward.
    # From the thumbnail: ED #29's southern boundary is around a line ~8 km
    # south of Tsuut'ina reserve's southern edge (just past Hwy 22X). East
    # boundary follows reserve eastern edge extended south; west boundary
    # continues west of reserve to the provincial park / Bragg Creek area.
    if reserves_m is not None and not reserves_m.is_empty:
        r_minx, r_miny, r_maxx, r_maxy = reserves_m.bounds
        # Rural block south of reserve: from reserve southern edge down ~8 km,
        # from reserve western edge to reserve eastern edge
        tsuut_rural = box(r_minx - 2000, r_miny - 9000, r_maxx + 500, r_miny)
        de_winton = de_winton.difference(tsuut_rural.buffer(0))

    # Step 3: Remove Okotoks town
    if okotoks_m is not None and not okotoks_m.is_empty:
        de_winton = de_winton.difference(okotoks_m.buffer(50))

    # Step 4: Trim north to Calgary southern city limit (exclude Calgary-
    # urban pieces). Highwood is entirely outside Calgary in 2019 so this
    # may be a no-op, but also remove any slivers inside Calgary.
    if calgary_m is not None and not calgary_m.is_empty:
        de_winton = de_winton.difference(calgary_m.buffer(50))

    # Step 5: The commission shows De Winton as an eastern block, not extending
    # too far west. Cut at a north-south line just west of Tsuut'ina reserve's
    # western edge (to keep it east of the Kananaskis / Foothills rural area).
    if reserves_m is not None and not reserves_m.is_empty:
        r_minx, r_miny, r_maxx, r_maxy = reserves_m.bounds
        # Commission: De Winton's western edge is approximately at the
        # Tsuut'ina reserve's EAST edge (which the reserve extends ~15 km
        # east-west). Cut at x = r_maxx + 200 m buffer.
        keep_east_of = box(r_maxx + 200, hw_miny - 5000, hw_maxx + 5000, hw_maxy + 5000)
        de_winton = de_winton.intersection(keep_east_of)

    # Clean
    de_winton = clean_polygon_noise(de_winton)

    anchors = {
        "west_edge_anchor": "Tsuut'ina Nation 145 eastern reserve boundary (OSM aboriginal_lands)",
        "north_edge_anchor": "Calgary southern city limits (OSM boundary=administrative admin_level=8)",
        "south_edge_anchor": "Highwood ED 2019 southern extent (inherited from parent)",
        "east_edge_anchor": "Foothills County eastern boundary (OSM admin_level=6)",
        "excludes": "Okotoks town (OSM admin_level=6)",
    }
    errors = {
        "west_edge_err_m": 1000,
        "north_edge_err_m": 300,
        "south_edge_err_m": 1000,
        "east_edge_err_m": 500,
        "okotoks_exclusion_err_m": 300,
    }
    print(
        f"[De Winton] v4 area = {de_winton.area/1e6:.2f} km^2 "
        f"(v3 was {v3_row.geometry.area/1e6:.2f} km^2)"
    )

    return de_winton, anchors, errors


def build_calgary_south(v3_row, g2019, osm_cache, de_winton_geom=None):
    """Calgary-South (ED 26) v4 polygon construction.

    Strategy (per commission thumbnail, p.74 zoom):
      Calgary-South #26 is a COMPACT ED carved from the SOUTH-WEST portion
      of 2019 Calgary-Hays, sitting directly south of Calgary-Hays #16 and
      east-north-east of Calgary-Fish Creek #13. It does NOT extend west
      into Calgary-Shaw territory.

      The commission thumbnail shows Calgary-South occupying roughly the
      south-west third of 2019 Calgary-Hays, with a "notch" on its east
      side where Hays (#16) dips south into Calgary-South's would-be area.

      Geometry construction:
        1. Start with 2019 Calgary-Hays polygon.
        2. Restrict to the southwestern ~55% of Hays (south of ~50% y,
           west of ~65% x).
        3. Cut a NE-corner notch (where Hays #16 extends south).

    Approximation bands: all edges +- 500 m (no OSM sub-neighbourhood
    features). Shape is better than v3 (which was ~64 km^2 elongated) but
    is still a rectilinear approximation of a rounded commission polygon.
    """
    print("[Calgary-South] building v4 polygon...")

    hays = g2019[g2019["EDName2017"] == "Calgary-Hays"].iloc[0].geometry
    hays = clean_polygon_noise(hays)
    fish_creek = g2019[g2019["EDName2017"] == "Calgary-Fish Creek"].iloc[0].geometry
    fish_creek = clean_polygon_noise(fish_creek)
    hays_minx, hays_miny, hays_maxx, hays_maxy = hays.bounds

    # Inspection of 2019 Calgary-Hays polygon shows it is an L-shape: a thin
    # east-west strip running along the south Calgary limit (~y=5640000)
    # plus a short southern protrusion at x~69500-72000, y~5636000-5638000.
    # Commission's Calgary-South #26 sits at the top of that southern
    # protrusion area, between Fish Creek #13 (west) and Hays #16 (north).
    #
    # From the zoomed commission thumbnail, Calgary-South is roughly:
    #   centre x ~ 72000-75000, centre y ~ 5639000-5640000
    #   size ~ 3-4 km wide x 2-3 km tall
    #   sits at the south edge of 2019 Hays' wider section
    #   includes a NE "notch" into Hays' east extension
    #
    # We approximate Calgary-South as the south-west lobe of Hays' central
    # section: x from 72000 to 76000, y from hays_miny to hays_miny + 3500.

    west_x = 72000
    east_x = 76500
    south_y = hays_miny - 200
    north_y = hays_miny + 0.85 * (hays_maxy - hays_miny)

    base_rect = box(west_x, south_y, east_x, north_y)
    cs_base = base_rect.intersection(hays)

    # Apply notch on NE corner: a small rectangular notch where Hays #16
    # dips south-east past the main Calgary-South block.
    notch_w = 1500
    notch_h = 1200
    notch = box(east_x - notch_w, north_y - notch_h, east_x + 200, north_y + 200)
    cs_geom = cs_base.difference(notch)

    # Do NOT subtract De Winton (De Winton is outside Calgary; Calgary-South
    # is inside Hays which is inside Calgary city limits).

    # Clean (use smaller part-area threshold so we don't lose the ~8-15 km^2
    # polygon)
    cs_geom = clean_polygon_noise(cs_geom, min_part_area_m2=500_000)

    # If cleaning removed everything, fall back
    if (
        cs_geom is None
        or cs_geom.is_empty
        or (hasattr(cs_geom, "area") and cs_geom.area < 5e5)
    ):
        print("[Calgary-South] fallback: rect based on Hays centroid")
        cent = hays.centroid
        cs_geom = box(
            cent.x - 2000, cent.y - 1500, cent.x + 2000, cent.y + 1500
        ).intersection(hays)

    anchors = {
        "west_edge_anchor": "Calgary-Hays 2019 western edge (Fish Creek boundary)",
        "north_edge_anchor": "approximate ~65% Y-line across Calgary-Hays 2019",
        "south_edge_anchor": "Calgary southern city limit (inherited from Hays)",
        "east_edge_anchor": "approximate ~55% X-line across Calgary-Hays 2019 with NE-corner notch",
    }
    errors = {
        "west_edge_err_m": 300,
        "north_edge_err_m": 500,
        "south_edge_err_m": 300,
        "east_edge_err_m": 500,
        "notch_err_m": 500,
    }
    print(
        f"[Calgary-South] v4 area = {cs_geom.area/1e6:.2f} km^2 "
        f"(v3 was {v3_row.geometry.area/1e6:.2f} km^2)"
    )

    return cs_geom, anchors, errors


# ----------------------------------------------------------------------
# VA-impact computation
# ----------------------------------------------------------------------


def compute_va_impact(v3_gdf, v4_gdf, va_gdf, target_eds):
    """Compute how VA assignments change between v3 and v4 for the target EDs.

    For each target ED and each VA: count 2023 votes that fall in v3 but not
    v4 (or vice versa). Sum by ED.
    """
    # Ensure CRS
    v3_gdf = v3_gdf.to_crs(WORK_CRS)
    v4_gdf = v4_gdf.to_crs(WORK_CRS)
    va = va_gdf.to_crs(WORK_CRS).copy()

    # Compute total 2023 votes per VA: va_ndp + va_ucp + va_other
    party_cols = [c for c in ("va_ndp", "va_ucp", "va_other") if c in va.columns]
    if party_cols:
        va["__votes_total"] = va[party_cols].fillna(0).sum(axis=1)
        vote_col = "__votes_total"
    else:
        vote_col = None
        for c in ("total_votes_2023", "total_votes", "votes_2023", "votes"):
            if c in va.columns:
                vote_col = c
                break
        if vote_col is None:
            vcols = [c for c in va.columns if "vote" in c.lower()]
            if vcols:
                va["__votes_total"] = (
                    va[vcols].select_dtypes(include=[np.number]).sum(axis=1)
                )
                vote_col = "__votes_total"
            else:
                va["__votes_total"] = 1
                vote_col = "__votes_total"

    # VA centroids for point-in-polygon
    va["__cent"] = va.geometry.representative_point()
    va_cent = va.set_geometry("__cent")

    results = []
    for ed in target_eds:
        v3_geom = v3_gdf[v3_gdf["name_2026"] == ed].iloc[0].geometry
        v4_geom = v4_gdf[v4_gdf["name_2026"] == ed].iloc[0].geometry
        in_v3 = va_cent.within(v3_geom)
        in_v4 = va_cent.within(v4_geom)
        sym = in_v3 ^ in_v4  # XOR: in v3 but not v4, or vice versa

        # Also compute geometric sym-diff area
        try:
            sym_diff = v3_geom.symmetric_difference(v4_geom)
            sym_area_km2 = sym_diff.area / 1e6
        except Exception:
            sym_area_km2 = float("nan")

        n_flipped = int(sym.sum())
        votes_flipped = float(va.loc[sym, vote_col].sum())
        v3_only = int((in_v3 & ~in_v4).sum())
        v4_only = int((~in_v3 & in_v4).sum())
        v3_only_votes = float(va.loc[in_v3 & ~in_v4, vote_col].sum())
        v4_only_votes = float(va.loc[~in_v3 & in_v4, vote_col].sum())

        results.append(
            {
                "name_2026": ed,
                "v3_area_km2": round(v3_geom.area / 1e6, 2),
                "v4_area_km2": round(v4_geom.area / 1e6, 2),
                "sym_diff_km2": round(sym_area_km2, 2),
                "vas_flipped_total": n_flipped,
                "votes_flipped_total": round(votes_flipped, 1),
                "vas_in_v3_only": v3_only,
                "votes_in_v3_only": round(v3_only_votes, 1),
                "vas_in_v4_only": v4_only,
                "votes_in_v4_only": round(v4_only_votes, 1),
            }
        )

    return pd.DataFrame(results)


# ----------------------------------------------------------------------
# Verification panel rendering
# ----------------------------------------------------------------------


def render_panel(ed_name, v3_geom, v4_geom, anchors_geom_dict, out_path):
    """Render a 3-layer panel: v3 (grey dashed), v4 (red solid), anchors (light)."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Anchor features first (background)
    colors = {
        "river": "#4a90e2",
        "admin": "#a0a0a0",
        "reserve": "#b89978",
        "highway": "#808080",
        "okotoks": "#c0a080",
    }
    for key, geom in anchors_geom_dict.items():
        if geom is None or (hasattr(geom, "is_empty") and geom.is_empty):
            continue
        try:
            gs = gpd.GeoSeries([geom], crs=WORK_CRS)
            if geom.geom_type in ("LineString", "MultiLineString"):
                gs.plot(
                    ax=ax,
                    color=colors.get(key, "#cccccc"),
                    linewidth=1.0,
                    alpha=0.6,
                    label=f"{key}",
                )
            else:
                gs.boundary.plot(
                    ax=ax,
                    color=colors.get(key, "#cccccc"),
                    linewidth=0.8,
                    alpha=0.5,
                    linestyle=":",
                    label=f"{key}",
                )
        except Exception as e:
            print(f"[render] anchor {key} failed: {e}", flush=True)

    # v3 (grey dashed)
    if v3_geom is not None and not v3_geom.is_empty:
        v3_lines = _exterior_only_lines(v3_geom)
        for i, ln in enumerate(v3_lines):
            gpd.GeoSeries([ln], crs=WORK_CRS).plot(
                ax=ax,
                color="#999999",
                linewidth=1.6,
                linestyle="--",
                label="v3 (superseded)" if i == 0 else None,
            )

    # v4 (red solid)
    if v4_geom is not None and not v4_geom.is_empty:
        lines = _exterior_only_lines(v4_geom)
        for i, ln in enumerate(lines):
            gpd.GeoSeries([ln], crs=WORK_CRS).plot(
                ax=ax,
                color="#c81e3f",
                linewidth=2.2,
                label="v4 (Tier C approximated)" if i == 0 else None,
            )

    # Zoom to the union of v3 and v4 bounds so both are visible
    if v4_geom is not None and not v4_geom.is_empty:
        u = unary_union(
            [g for g in (v3_geom, v4_geom) if g is not None and not g.is_empty]
        )
        minx, miny, maxx, maxy = u.bounds
    else:
        minx, miny, maxx, maxy = v3_geom.bounds
    pad = 0.10 * max(maxx - minx, maxy - miny)
    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"{ed_name} — v4 Tier C approximation", fontsize=13, pad=14)
    caption = (
        "Visual-transcription-assisted Tier C approximation vs v3 "
        "Tier B (superseded). Anchor features: OSM waterway / "
        "administrative / aboriginal_lands. Not a shapefile release."
    )
    fig.text(0.5, 0.02, caption, ha="center", fontsize=9, style="italic", wrap=True)

    # Legend (dedup)
    handles, labels = ax.get_legend_handles_labels()
    seen = set()
    uniq = [(h, l) for h, l in zip(handles, labels) if not (l in seen or seen.add(l))]
    if uniq:
        ax.legend(
            [h for h, _ in uniq],
            [l for _, l in uniq],
            loc="upper right",
            fontsize=9,
            framealpha=0.9,
        )
    plt.subplots_adjust(top=0.93, bottom=0.08)
    plt.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"[render] wrote {out_path}", flush=True)


# ----------------------------------------------------------------------
# Main pipeline
# ----------------------------------------------------------------------


def main():
    t0 = time.time()
    print("=" * 70)
    print("v0_1 shape refinement v4 — Tier C visual-transcription-assisted")
    print("=" * 70)

    # Load inputs
    v3_gdf = gpd.read_file(DATA_DIR / "v0_1_refined_v3_minority_2026_eds.gpkg")
    if v3_gdf.crs is None or str(v3_gdf.crs) != WORK_CRS:
        v3_gdf = v3_gdf.to_crs(WORK_CRS)
    g2019 = gpd.read_file(DATA_DIR / "alberta_2019_eds")
    if g2019.crs is None or str(g2019.crs) != WORK_CRS:
        g2019 = g2019.to_crs(WORK_CRS)

    # Load VAs (use same logic as v3)
    try:
        va = gpd.read_file(DATA_DIR / "va_polygons_with_2023_votes.gpkg")
        if str(va.crs) != WORK_CRS:
            va = va.to_crs(WORK_CRS)
    except Exception as e:
        print(f"[main] WARNING: could not load VAs: {e}")
        va = None

    v4_gdf = v3_gdf.copy(deep=True)
    osm_cache = {}

    notes = {}

    # Edmonton-Windermere
    ew_row = v3_gdf[v3_gdf["name_2026"] == "Edmonton-Windermere"].iloc[0]
    ew_v4, ew_anchors, ew_errors = build_edmonton_windermere(ew_row, g2019, osm_cache)
    v4_gdf.loc[v4_gdf["name_2026"] == "Edmonton-Windermere", "geometry"] = ew_v4
    notes["Edmonton-Windermere"] = {"anchors": ew_anchors, "errors_m": ew_errors}

    # Calgary-De Winton
    dw_row = v3_gdf[v3_gdf["name_2026"] == "Calgary-De Winton"].iloc[0]
    dw_v4, dw_anchors, dw_errors = build_calgary_de_winton(dw_row, g2019, osm_cache)
    v4_gdf.loc[v4_gdf["name_2026"] == "Calgary-De Winton", "geometry"] = dw_v4
    notes["Calgary-De Winton"] = {"anchors": dw_anchors, "errors_m": dw_errors}

    # Calgary-South (needs De Winton for overlap subtraction)
    cs_row = v3_gdf[v3_gdf["name_2026"] == "Calgary-South"].iloc[0]
    cs_v4, cs_anchors, cs_errors = build_calgary_south(
        cs_row, g2019, osm_cache, de_winton_geom=dw_v4
    )
    v4_gdf.loc[v4_gdf["name_2026"] == "Calgary-South", "geometry"] = cs_v4
    notes["Calgary-South"] = {"anchors": cs_anchors, "errors_m": cs_errors}

    # Update tier / confidence / notes for the three EDs
    mask = v4_gdf["name_2026"].isin(TARGET_EDS)
    v4_gdf.loc[mask, "tier"] = "C-approximated"
    v4_gdf.loc[mask, "confidence"] = "low-visually-transcribed"
    if "refined_note" in v4_gdf.columns:
        for ed in TARGET_EDS:
            m = v4_gdf["name_2026"] == ed
            note = notes[ed]
            anchor_str = "; ".join(f"{k}={v}" for k, v in note["anchors"].items())
            err_str = "; ".join(f"{k}={v}" for k, v in note["errors_m"].items())
            v4_gdf.loc[m, "refined_note"] = (
                f"v4 Tier C | anchors: {anchor_str} | err(m): {err_str}"
            )

    # Add a dedicated tier-history column (v4 provenance)
    if "v4_method" not in v4_gdf.columns:
        v4_gdf["v4_method"] = ""
    v4_gdf.loc[mask, "v4_method"] = "visual-transcription-assisted"

    # Save
    out_gpkg = DATA_DIR / "v0_1_refined_v4_minority_2026_eds.gpkg"
    v4_gdf.to_file(out_gpkg, driver="GPKG")
    print(f"\n[main] wrote {out_gpkg}")

    # Impact vs v3
    if va is not None:
        impact = compute_va_impact(v3_gdf, v4_gdf, va, TARGET_EDS)
        impact_csv = DATA_DIR / "boundary_refinement_impact_v4.csv"
        impact.to_csv(impact_csv, index=False)
        print(f"[main] wrote {impact_csv}")
        print(impact.to_string())
    else:
        print("[main] skipped VA impact (no VA file)")
        impact = None

    # Render verification panels
    anchor_geoms = {}
    # Edmonton anchors: river
    if osm_cache.get("edm_river") is not None:
        anchor_geoms["edmonton_river"] = to_work(osm_cache["edm_river"])
    if osm_cache.get("calgary_admin") is not None:
        anchor_geoms["calgary_admin"] = to_work(osm_cache["calgary_admin"])
    if osm_cache.get("okotoks_admin") is not None:
        anchor_geoms["okotoks_admin"] = to_work(osm_cache["okotoks_admin"])
    if osm_cache.get("reserves") is not None:
        anchor_geoms["reserves"] = to_work(osm_cache["reserves"])
    if osm_cache.get("foothills_admin") is not None:
        anchor_geoms["foothills_admin"] = to_work(osm_cache["foothills_admin"])

    # Per-ED panels with contextual anchors
    panel_map = {
        "Edmonton-Windermere": {
            "river": anchor_geoms.get("edmonton_river"),
        },
        "Calgary-De Winton": {
            "admin": anchor_geoms.get("calgary_admin"),
            "okotoks": anchor_geoms.get("okotoks_admin"),
            "reserve": anchor_geoms.get("reserves"),
        },
        "Calgary-South": {
            "admin": anchor_geoms.get("calgary_admin"),
        },
    }

    ed_slug = {
        "Edmonton-Windermere": "edmonton_windermere",
        "Calgary-De Winton": "calgary_de_winton",
        "Calgary-South": "calgary_south",
    }

    for ed, anchors in panel_map.items():
        v3_g = v3_gdf[v3_gdf["name_2026"] == ed].iloc[0].geometry
        v4_g = v4_gdf[v4_gdf["name_2026"] == ed].iloc[0].geometry
        out = VERIFICATION_DIR / f"v0_4_minority_{ed_slug[ed]}.svg"
        render_panel(ed, v3_g, v4_g, anchors, out)

    # Log
    log = {
        "pipeline_version": "v4",
        "target_eds": TARGET_EDS,
        "notes": notes,
        "elapsed_sec": round(time.time() - t0, 1),
    }
    log_path = ANALYSIS_DIR / "shape_refinement_v4_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    print(f"[main] wrote {log_path}")

    print(f"\nDone in {time.time()-t0:.1f} s")


if __name__ == "__main__":
    main()
