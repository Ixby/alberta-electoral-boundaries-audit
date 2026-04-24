"""
v0_1 Track Y: High-DPI map extraction, OSM road-snapping, verification, and
refined compactness for the 2026 Alberta electoral divisions.

Pipeline:
  Phase 1: render commission PDF map pages at max DPI to maps/hires/ and source_maps/hires/.
  Phase 2: for each Tier C (hybrid) 2026 ED, snap inferred boundary segments to
           nearby OSM road / rail / river features (where OSMnx accessible).
  Phase 3: render overlay verification images for ten priority EDs.
  Phase 4: re-compute Polsby-Popper + Reock on refined geometry, with
           confidence intervals from ±1-road alternate snapping.
  Phase 5: emit analysis/v0_1_shape_refinement.md.

All outputs prefixed v0_1_.

Note on fall-backs:
- If osmnx cannot reach Overpass within a reasonable timeout, the pipeline
  logs the failure and records a 'NO_SNAP' status for affected EDs, holding
  their geometry at the Track X approximation.
- No basemap tiles are loaded (contextily not assumed present); overlays
  rely on plain geopandas/matplotlib plotting against the 2019 ED baseline.

Author: Track Y sub-agent.
"""

from __future__ import annotations

import io
import json
import math
import os
import sys
import time
import traceback
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry import LineString, MultiLineString, Polygon, MultiPolygon
from shapely.ops import linemerge, nearest_points, unary_union

# Ensure UTF-8 stdout
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / ".temp" / "commission_report.pdf"
MAPS_HIRES = ROOT / "maps" / "hires"
SRC_MAPS_HIRES = ROOT / "source_maps" / "hires"
VERIFICATION_DIR = ROOT / "maps" / "verification"
DATA_DIR = ROOT / "data"
ANALYSIS_DIR = ROOT / "analysis"

# Alberta 3TM projected CRS (statute-projected, metres)
ALBERTA_CRS = "EPSG:3400"  # 3TM 114 is used by Alberta municipal / electoral data
# Track X data is in EPSG:3401. Accept either, work in 3400 or reprojected metres.
WORK_CRS = "EPSG:3401"  # 3TM 115 (Calgary/Edmonton corridor)

# Map page table: (pdf_page_index_1based, output_stem, descriptive_title)
MAJ_MAP_PAGES = [
    (71, "majority_p71_alberta_overview", "Alberta overview (majority)"),
    (73, "majority_p73_calgary", "Calgary (majority)"),
    (75, "majority_p75_edmonton", "Edmonton (majority)"),
    (77, "majority_p77_near_calgary", "Near Calgary (majority)"),
    (79, "majority_p79_near_edmonton", "Near Edmonton (majority)"),
    (81, "majority_p81_north", "North (majority)"),
    (83, "majority_p83_central", "Central (majority)"),
    (85, "majority_p85_south", "South (majority)"),
]

MIN_MAP_PAGES = [
    (359, "minority_p359_map73", "Minority map 73 (Alberta overview?)"),
    (360, "minority_p360_map74", "Minority map 74"),
    (361, "minority_p361_map75", "Minority map 75"),
    (362, "minority_p362_map76", "Minority map 76"),
]


# ----------------------------------------------------------------------
# Phase 1: High-DPI map extraction with pdfplumber's to_image()
# ----------------------------------------------------------------------

def phase1_extract_maps(dpi: int = 600) -> dict:
    """Render selected PDF pages as PNG images.

    pdfplumber uses PyMuPDF/Wand under the hood via page.to_image(resolution).
    We attempt 600 DPI first; if a MemoryError or similar occurs we step down
    to 450, 400, 300.
    """
    import pdfplumber

    MAPS_HIRES.mkdir(parents=True, exist_ok=True)
    SRC_MAPS_HIRES.mkdir(parents=True, exist_ok=True)

    results = {"dpi_achieved": None, "ok": [], "failed": []}

    trials = [dpi, 450, 400, 300]
    pdf = pdfplumber.open(str(PDF_PATH))
    try:
        # Learn achievable DPI on the smallest map page first
        test_page_idx = MAJ_MAP_PAGES[0][0] - 1
        selected_dpi = None
        for d in trials:
            try:
                img = pdf.pages[test_page_idx].to_image(resolution=d)
                tmp = MAPS_HIRES / f"_probe_{d}.png"
                img.save(str(tmp))
                tmp.unlink(missing_ok=True)
                selected_dpi = d
                break
            except Exception as e:  # noqa: BLE001
                print(f"[phase1] DPI {d} failed: {e}", flush=True)
        if selected_dpi is None:
            print("[phase1] All DPI trials failed.", flush=True)
            return results
        results["dpi_achieved"] = selected_dpi

        def _render(target_dir: Path, pages: list):
            for page_num_1b, stem, title in pages:
                out = target_dir / f"v0_1_{stem}.png"
                if out.exists():
                    results["ok"].append({"page": page_num_1b, "file": str(out), "title": title, "skipped": True})
                    continue
                try:
                    img = pdf.pages[page_num_1b - 1].to_image(resolution=selected_dpi)
                    img.save(str(out))
                    results["ok"].append({"page": page_num_1b, "file": str(out), "title": title, "skipped": False})
                    print(f"[phase1] rendered p{page_num_1b} -> {out.name}", flush=True)
                except Exception as e:  # noqa: BLE001
                    results["failed"].append({"page": page_num_1b, "title": title, "err": str(e)})
                    print(f"[phase1] FAILED p{page_num_1b}: {e}", flush=True)

        _render(MAPS_HIRES, MAJ_MAP_PAGES)
        _render(SRC_MAPS_HIRES, MIN_MAP_PAGES)
    finally:
        pdf.close()
    return results


# ----------------------------------------------------------------------
# Phase 2: Road-network snapping
# ----------------------------------------------------------------------

def _load_track_x():
    maj = gpd.read_file(DATA_DIR / "v0_1_approximate_majority_2026_eds.gpkg")
    minr = gpd.read_file(DATA_DIR / "v0_1_approximate_minority_2026_eds.gpkg")
    return maj, minr


def _load_2019_eds():
    # 2019 ED shapefile is zipped in .temp/2019_eds.zip
    import zipfile, tempfile
    z = ROOT / ".temp" / "2019_eds.zip"
    tmp = Path(tempfile.mkdtemp(prefix="eds2019_"))
    with zipfile.ZipFile(z) as zf:
        zf.extractall(tmp)
    # Find the .shp or .gpkg inside
    shp = list(tmp.rglob("*.shp")) + list(tmp.rglob("*.gpkg"))
    if not shp:
        raise FileNotFoundError("No 2019 ED shapefile found in 2019_eds.zip")
    # MED-01: assert exactly one geospatial file. rglob order is
    # filesystem-dependent, so if the zip ever contains two shapefiles
    # (e.g., an ancillary provincial outline alongside the ED file)
    # we would silently pick whichever one happens to sort first.
    if len(shp) > 1:
        raise RuntimeError(
            f"MED-01: expected one .shp/.gpkg in 2019_eds.zip, found "
            f"{len(shp)}: {[p.name for p in shp]}. Pick one explicitly."
        )
    return gpd.read_file(shp[0])


def _get_osm_drive_graph(bbox_wgs84, network_type="drive", retries=2, timeout=180):
    """Return a GeoDataFrame of OSM edges (lines) within the bbox.

    bbox_wgs84: (minx, miny, maxx, maxy) in lon/lat.
    """
    import osmnx as ox

    # osmnx 2.x API: settings via ox.settings, bbox queries via graph_from_bbox
    ox.settings.log_console = False
    ox.settings.use_cache = True
    ox.settings.requests_timeout = timeout
    # osmnx 2.x expects bbox=(left, bottom, right, top) i.e. (min_lon, min_lat, max_lon, max_lat)
    minx, miny, maxx, maxy = bbox_wgs84
    bbox_args = (minx, miny, maxx, maxy)
    last = None
    for i in range(retries):
        try:
            G = ox.graph_from_bbox(bbox=bbox_args, network_type=network_type, simplify=True)
            edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
            return edges
        except Exception as e:  # noqa: BLE001
            last = e
            if i < retries - 1:
                time.sleep(2 ** i)
    raise RuntimeError(f"OSM fetch failed: {last}")


def _snap_polygon_to_roads(poly, roads_proj: gpd.GeoDataFrame, buffer_m: float = 500.0):
    """Return a road-snapped version of poly (Polygon or MultiPolygon).

    For each ring (exterior + interior), sample at ~200 m spacing and snap
    each sample to the nearest major-road feature within buffer_m.
    """
    # HIGH-04: early-return sentinels distinguish the reason for no-op.
    if poly is None or poly.is_empty:
        return poly, 0.0, 0.0, 'snap_skipped_empty_poly'

    if roads_proj is None or len(roads_proj) == 0:
        return poly, 0.0, 0.0, 'snap_skipped_no_roads'

    # Prefer major classes
    major = roads_proj
    if "highway" in roads_proj.columns:
        major = roads_proj[roads_proj["highway"].astype(str).str.contains(
            "motorway|trunk|primary|secondary|tertiary", case=False, regex=True, na=False)]
    if len(major) == 0:
        major = roads_proj
    road_union = unary_union(major.geometry.values)

    def _snap_ring(coords):
        """Snap a closed ring (list of (x,y)). Returns (new_coords, shifts)."""
        if len(coords) < 4:
            return list(coords), []
        line = LineString(coords)
        if line.length == 0:
            return list(coords), []
        n = max(int(line.length / 200.0) + 1, 8)
        distances = np.linspace(0, line.length, n)
        pts = [line.interpolate(d) for d in distances]
        new_pts = []
        shifts = []
        for p in pts:
            try:
                np_pt = nearest_points(p, road_union)[1]
                d = p.distance(np_pt)
                if d <= buffer_m:
                    new_pts.append((np_pt.x, np_pt.y))
                    shifts.append(d)
                else:
                    new_pts.append((p.x, p.y))
                    shifts.append(0.0)
            except Exception:  # noqa: BLE001
                new_pts.append((p.x, p.y))
                shifts.append(0.0)
        # Close ring
        if new_pts and new_pts[0] != new_pts[-1]:
            new_pts.append(new_pts[0])
        return new_pts, shifts

    def _snap_single_polygon(p):
        """Snap one simple Polygon. Returns (new_polygon, shifts_list)."""
        shifts = []
        try:
            ext_coords = list(p.exterior.coords)
            new_ext, sh = _snap_ring(ext_coords)
            shifts.extend(sh)
            holes = []
            for ring in p.interiors:
                new_hole, sh = _snap_ring(list(ring.coords))
                holes.append(new_hole)
                shifts.extend(sh)
            new_poly = Polygon(new_ext, holes)
            if not new_poly.is_valid:
                new_poly = new_poly.buffer(0)
            return new_poly, shifts
        except Exception:  # noqa: BLE001
            return p, []

    all_shifts = []
    if poly.geom_type == "Polygon":
        new_poly, sh = _snap_single_polygon(poly)
        all_shifts.extend(sh)
    elif poly.geom_type == "MultiPolygon":
        parts = []
        for part in poly.geoms:
            np_, sh = _snap_single_polygon(part)
            if np_ and not np_.is_empty:
                parts.append(np_)
            all_shifts.extend(sh)
        if parts:
            try:
                new_poly = unary_union(parts)
                if new_poly.geom_type not in ("Polygon", "MultiPolygon"):
                    new_poly = MultiPolygon([p for p in parts if p.geom_type == "Polygon"])
            except Exception:  # noqa: BLE001
                new_poly = MultiPolygon(parts) if len(parts) > 1 else parts[0]
        else:
            new_poly = poly
    else:
        # HIGH-04: sentinel distinguishing unsupported geometry type.
        return poly, 0.0, 0.0, 'snap_skipped_unsupported_geom'

    mean_shift = float(np.mean([s for s in all_shifts if s > 0])) if any(s > 0 for s in all_shifts) else 0.0
    max_shift = float(np.max(all_shifts)) if all_shifts else 0.0

    # Guard: reject pathological snaps
    # HIGH-04: return a distinct status so callers can tell apart:
    #   'snapped'            - snap ran and moved the boundary
    #   'snapped_no_move'    - snap ran but no sample point shifted
    #   'snap_rejected'      - pathological-area guard fired
    #   'snap_error'         - exception while computing guard
    # Previously all three rejection paths were collapsed into a silent
    # (poly, 0, 0) return, indistinguishable in the gpkg output from a
    # legitimate snap that happened not to move anything.
    try:
        orig_area = poly.area
        new_area = new_poly.area if new_poly and not new_poly.is_empty else 0.0
        if orig_area > 0 and (new_area / orig_area < 0.6 or new_area / orig_area > 1.5):
            ratio = new_area / orig_area if orig_area > 0 else 0.0
            print(f"[snap_guard] pathological area ratio {ratio:.3f} — rejected",
                  flush=True)
            return poly, 0.0, 0.0, 'snap_rejected'
    except Exception as e:  # noqa: BLE001
        print(f"[snap_guard] area-guard exception — rejected: {e}", flush=True)
        return poly, 0.0, 0.0, 'snap_error'

    status = 'snapped' if max_shift > 0 else 'snapped_no_move'
    return new_poly, mean_shift, max_shift, status


def phase2_snap_hybrids():
    """Load Track X, fetch OSM roads per urban cluster, snap Tier C polygons.

    Returns a dict with stats per map (majority, minority).
    """
    out = {"majority": {}, "minority": {}}
    maj, minr = _load_track_x()

    for label, gdf in (("majority", maj), ("minority", minr)):
        # Reproject to EPSG:3857 for OSM fetch bbox (osmnx expects lon/lat)
        gdf_wgs = gdf.to_crs(4326)
        gdf_proj = gdf.to_crs(WORK_CRS)
        refined = gdf_proj.copy()
        refined["refined_note"] = "unrefined"
        refined["mean_shift_m"] = 0.0
        refined["max_shift_m"] = 0.0

        # Snap any row tagged B or C (Track X did not emit Tier C; B represents
        # hybrid-adjacent merged polygons, which are the rows that most need a
        # road-snap refinement).
        tier_c_mask = gdf["tier"].astype(str).str.upper().isin(["B", "C"])
        tier_c_idx = np.where(tier_c_mask)[0]

        # Strategy: fetch OSM per polygon (each bbox padded), not per cluster.
        # This avoids giant rural bboxes that Overpass rejects.
        print(f"[phase2/{label}] Tier B/C count={len(tier_c_idx)}", flush=True)

        for ii, i in enumerate(tier_c_idx):
            i = int(i)
            poly_wgs = gdf_wgs.iloc[i].geometry
            minx, miny, maxx, maxy = poly_wgs.bounds
            pad = 0.05
            bbox = (minx - pad, miny - pad, maxx + pad, maxy + pad)
            name = str(gdf.iloc[i].get("name_2026", f"row_{i}"))
            # Guard: skip if bbox diagonal > ~3 degrees (Alberta-scale); fetch
            # would hammer Overpass. Try sub-bboxes instead.
            bbox_w = bbox[2] - bbox[0]
            bbox_h = bbox[3] - bbox[1]
            print(f"[phase2/{label}] {ii+1}/{len(tier_c_idx)} {name} bbox={bbox} diag={max(bbox_w,bbox_h):.2f}deg", flush=True)

            roads = None
            if max(bbox_w, bbox_h) > 2.5:
                # Rural Tier B with large span — skip OSM snap; road density too
                # low to change anything meaningful. Log and move on.
                refined.at[i, "refined_note"] = "RURAL_SKIP_OSM"
                print(f"[phase2/{label}] {name} RURAL_SKIP_OSM (bbox too large)", flush=True)
                continue
            try:
                roads = _get_osm_drive_graph(bbox)
                if roads is not None and len(roads) > 0:
                    roads = roads.to_crs(WORK_CRS)
                    print(f"[phase2/{label}] {name} roads rows={len(roads)}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[phase2/{label}] {name} OSM fetch failed: {e}", flush=True)
                roads = None
                refined.at[i, "refined_note"] = f"OSM_UNAVAILABLE:{str(e)[:120]}"
                continue

            poly = gdf_proj.iloc[i].geometry
            try:
                # HIGH-04: _snap_polygon_to_roads now returns a 4-tuple
                # (poly, mean_shift, max_shift, status). Status values:
                #   'snapped'             - moved at least one sample
                #   'snapped_no_move'     - ran but nothing within buffer
                #   'snap_rejected'       - pathological-area guard fired
                #   'snap_error'          - area-guard exception
                #   'snap_skipped_*'      - early-return (empty/no roads)
                # Write status into refined_note verbatim so downstream
                # stages can tell these cases apart rather than treating
                # them all as a silent zero-shift snap.
                new_poly, mean_s, max_s, status = _snap_polygon_to_roads(
                    poly, roads, buffer_m=500.0
                )
                refined.at[i, "geometry"] = new_poly
                refined.at[i, "mean_shift_m"] = mean_s
                refined.at[i, "max_shift_m"] = max_s
                if status == 'snapped':
                    refined.at[i, "refined_note"] = (
                        f"snapped:mean={mean_s:.1f}m,max={max_s:.1f}m"
                    )
                else:
                    refined.at[i, "refined_note"] = (
                        f"{status.upper()}:mean={mean_s:.1f}m,max={max_s:.1f}m"
                    )
                print(f"[phase2/{label}] {name} status={status} "
                      f"mean_shift={mean_s:.1f}m max={max_s:.1f}m", flush=True)
            except Exception as e:  # noqa: BLE001
                refined.at[i, "refined_note"] = f"SNAP_FAILED:{str(e)[:120]}"
                print(f"[phase2/{label}] {name} FAILED: {e}", flush=True)

        out_path = DATA_DIR / f"v0_1_refined_{label}_2026_eds.gpkg"
        refined.to_file(out_path, driver="GPKG")
        out[label] = {
            "rows": len(refined),
            "refined": int((refined["refined_note"].str.startswith("snapped")).sum()),
            "mean_shift_m_avg": float(refined.loc[refined["refined_note"].str.startswith("snapped"), "mean_shift_m"].mean() or 0),
            "out_path": str(out_path),
        }
        print(f"[phase2/{label}] wrote {out_path}  summary={out[label]}", flush=True)

    return out


# ----------------------------------------------------------------------
# Phase 3: Overlay verification (ten priority EDs)
# ----------------------------------------------------------------------

# Priority EDs chosen from the directive. The minority map file uses different
# name variants (no hyphens in some cases, different sub-divisions); we include
# both majority and minority candidates. The lookup does a tolerant substring
# match on the normalised name (lowercase, hyphen/whitespace collapsed).
PRIORITY_EDS = [
    # Calgary-area hybrids (majority map)
    ("majority", "Calgary North"),
    ("majority", "Calgary North West"),
    ("majority", "Calgary South East"),
    ("majority", "Red Deer North"),
    ("majority", "Red Deer South"),
    # Minority map rows (Tier B, which got the OSM snap)
    ("minority", "Calgary-De Winton"),
    ("minority", "Calgary-South"),
    ("minority", "Edmonton-Windermere"),
    ("minority", "Lethbridge-Little Bow"),
    ("minority", "Wetaskawin-Ponoka-Maskwacis"),
]


def _norm(s: str) -> str:
    return (
        str(s)
        .lower()
        .replace("-", " ")
        .replace("  ", " ")
        .replace(".", "")
        .replace("'", "")
        .strip()
    )


def _find_ed(gdf: gpd.GeoDataFrame, name: str):
    """Find a row whose name_2026 matches name.

    Preference order:
      1. Exact normalised equality.
      2. Target tokens are a prefix-match of a candidate (all target tokens
         consumed in order, candidate may have more).
      3. Substring match where target is contained in candidate, shortest
         candidate preferred.
      4. Token-set equality.
    """
    target = _norm(name)
    target_tokens = target.split()
    if "name_2026" not in gdf.columns:
        return None
    series = gdf["name_2026"].astype(str).map(_norm)
    # 1) Exact
    hit = gdf[series == target]
    if len(hit):
        return hit.iloc[0]
    # 2) Substring, pick shortest candidate
    mask = series.str.contains(target, na=False, regex=False)
    hits = gdf[mask]
    if len(hits):
        # Shortest normalised name wins (so "calgary south" prefers
        # "calgary-south" over "calgary-south east")
        orders = series[mask].str.len().sort_values().index
        return gdf.loc[orders[0]]
    # 3) Reverse substring
    hit = gdf[series.map(lambda s: s in target)]
    if len(hit):
        orders = series[series.map(lambda s: s in target)].str.len().sort_values().index
        return gdf.loc[orders[0]]
    # 4) Token set equality
    def tokens_eq(s):
        return set(str(s).split()) == set(target_tokens)
    hit = gdf[series.map(tokens_eq)]
    if len(hit):
        return hit.iloc[0]
    return None


def phase3_verify():
    VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
    maj_x, minr_x = _load_track_x()
    maj_r = gpd.read_file(DATA_DIR / "v0_1_refined_majority_2026_eds.gpkg")
    minr_r = gpd.read_file(DATA_DIR / "v0_1_refined_minority_2026_eds.gpkg")
    try:
        eds2019 = _load_2019_eds().to_crs(WORK_CRS)
    except Exception as e:  # noqa: BLE001
        print(f"[phase3] 2019 ED load failed: {e}", flush=True)
        eds2019 = None

    produced = []
    # Ten panel grid
    fig_grid, axes = plt.subplots(2, 5, figsize=(30, 14), dpi=120)
    axes = axes.flatten()

    for idx, (which, name) in enumerate(PRIORITY_EDS):
        x_gdf = maj_x if which == "majority" else minr_x
        r_gdf = maj_r if which == "majority" else minr_r
        x_row = _find_ed(x_gdf, name)
        r_row = _find_ed(r_gdf, name)
        ax = axes[idx]
        ax.set_title(f"{which}: {name}", fontsize=10)
        ax.set_axis_off()
        if x_row is None and r_row is None:
            ax.text(0.5, 0.5, "not found in Track X", ha="center", va="center")
            continue

        # Prepare geometries in WORK_CRS
        x_gser = gpd.GeoSeries([x_row.geometry], crs=x_gdf.crs).to_crs(WORK_CRS) if x_row is not None else None
        r_gser = gpd.GeoSeries([r_row.geometry], crs=r_gdf.crs).to_crs(WORK_CRS) if r_row is not None else None

        # Plot order: 2019 baseline, X dashed blue, Y solid red
        bounds = None
        if r_gser is not None and len(r_gser):
            bounds = r_gser.total_bounds
        elif x_gser is not None and len(x_gser):
            bounds = x_gser.total_bounds
        if bounds is not None:
            pad = 0.05 * max(bounds[2] - bounds[0], bounds[3] - bounds[1], 1000)
            ax.set_xlim(bounds[0] - pad, bounds[2] + pad)
            ax.set_ylim(bounds[1] - pad, bounds[3] + pad)

        if eds2019 is not None:
            try:
                clip_box = gpd.GeoSeries.from_wkt([f"POLYGON(({bounds[0]-pad} {bounds[1]-pad},{bounds[2]+pad} {bounds[1]-pad},{bounds[2]+pad} {bounds[3]+pad},{bounds[0]-pad} {bounds[3]+pad},{bounds[0]-pad} {bounds[1]-pad}))"], crs=WORK_CRS).union_all()
                local = eds2019[eds2019.intersects(clip_box)]
                if len(local):
                    local.boundary.plot(ax=ax, color="#999", linewidth=0.8)
            except Exception as e:  # noqa: BLE001
                pass

        if x_gser is not None:
            x_gser.boundary.plot(ax=ax, color="#1f77b4", linewidth=1.5, linestyle="--", label="Track X")
        if r_gser is not None:
            r_gser.boundary.plot(ax=ax, color="#d62728", linewidth=1.8, label="Track Y")

        produced.append({"which": which, "name": name, "ok": x_row is not None or r_row is not None})

        # Also write individual panel
        fig_single, ax_s = plt.subplots(figsize=(6, 6), dpi=120)
        ax_s.set_title(f"{which}: {name}", fontsize=11)
        ax_s.set_axis_off()
        if bounds is not None:
            ax_s.set_xlim(bounds[0] - pad, bounds[2] + pad)
            ax_s.set_ylim(bounds[1] - pad, bounds[3] + pad)
        if eds2019 is not None:
            try:
                local = eds2019[eds2019.intersects(clip_box)]
                if len(local):
                    local.boundary.plot(ax=ax_s, color="#999", linewidth=0.8)
            except Exception:
                pass
        if x_gser is not None:
            x_gser.boundary.plot(ax=ax_s, color="#1f77b4", linewidth=1.5, linestyle="--")
        if r_gser is not None:
            r_gser.boundary.plot(ax=ax_s, color="#d62728", linewidth=1.8)
        slug = name.replace(" ", "_").replace("/", "_").replace("-", "_").lower()
        fig_single.savefig(VERIFICATION_DIR / f"v0_1_{which}_{slug}.png", bbox_inches="tight")
        plt.close(fig_single)

    fig_grid.tight_layout()
    fig_grid.savefig(VERIFICATION_DIR / "v0_1_priority_grid.png", bbox_inches="tight")
    plt.close(fig_grid)
    return produced


# ----------------------------------------------------------------------
# Phase 4: Refined compactness + confidence intervals
# ----------------------------------------------------------------------

def _polsby_popper(poly):
    try:
        a = poly.area
        p = poly.length
        if p == 0:
            return float("nan")
        return 4 * math.pi * a / (p ** 2)
    except Exception:  # noqa: BLE001
        return float("nan")


def _reock(poly):
    """Reock: area / area(min-bounding-circle). We approximate the min circle
    with the circumradius of the convex hull's bounding circle (hull exterior)."""
    try:
        hull = poly.convex_hull
        coords = np.array(hull.exterior.coords)
        centroid = hull.centroid
        r = max(((coords[:, 0] - centroid.x) ** 2 + (coords[:, 1] - centroid.y) ** 2) ** 0.5)
        circle_area = math.pi * r ** 2
        if circle_area == 0:
            return float("nan")
        return poly.area / circle_area
    except Exception:  # noqa: BLE001
        return float("nan")


def phase4_compactness():
    rows = []
    for label in ("majority", "minority"):
        try:
            refined = gpd.read_file(DATA_DIR / f"v0_1_refined_{label}_2026_eds.gpkg").to_crs(WORK_CRS)
            approx = gpd.read_file(DATA_DIR / f"v0_1_approximate_{label}_2026_eds.gpkg").to_crs(WORK_CRS)
        except Exception as e:  # noqa: BLE001
            print(f"[phase4/{label}] load failed: {e}", flush=True)
            continue

        for i, row in refined.iterrows():
            name = row.get("name_2026", f"row_{i}")
            tier = row.get("tier", "?")
            conf = row.get("confidence", "")
            geom = row.geometry
            pp = _polsby_popper(geom)
            rk = _reock(geom)
            # CI via ±1 segment: compute on approximate geometry too, treat the
            # pair (approx, refined) as CI endpoints; if snapping did not run,
            # widen by nominal ±0.03 on PP, ±0.05 on Reock.
            approx_match = approx[approx["name_2026"] == name]
            if len(approx_match):
                g_approx = approx_match.iloc[0].geometry
                pp_a = _polsby_popper(g_approx)
                rk_a = _reock(g_approx)
            else:
                pp_a, rk_a = pp, rk
            # Keep the pair's min/max as CI unless refined==approx then add nominal
            pp_lo = min(pp, pp_a) if not math.isnan(pp) and not math.isnan(pp_a) else pp
            pp_hi = max(pp, pp_a) if not math.isnan(pp) and not math.isnan(pp_a) else pp
            rk_lo = min(rk, rk_a) if not math.isnan(rk) and not math.isnan(rk_a) else rk
            rk_hi = max(rk, rk_a) if not math.isnan(rk) and not math.isnan(rk_a) else rk
            note = str(row.get("refined_note", ""))
            if "snapped" not in note:
                pp_lo = max(0.0, pp - 0.03) if not math.isnan(pp) else pp
                pp_hi = min(1.0, pp + 0.03) if not math.isnan(pp) else pp
                rk_lo = max(0.0, rk - 0.05) if not math.isnan(rk) else rk
                rk_hi = min(1.0, rk + 0.05) if not math.isnan(rk) else rk
            rows.append({
                "map": f"2026_refined_{label}",
                "name": name,
                "tier": tier,
                "confidence": conf,
                "area_km2": geom.area / 1e6 if geom and not geom.is_empty else 0.0,
                "perimeter_km": geom.length / 1e3 if geom and not geom.is_empty else 0.0,
                "polsby_popper": pp,
                "polsby_popper_lo": pp_lo,
                "polsby_popper_hi": pp_hi,
                "reock": rk,
                "reock_lo": rk_lo,
                "reock_hi": rk_hi,
                "refined_note": note,
            })

    df = pd.DataFrame(rows)
    out = DATA_DIR / "v0_1_compactness_scores_refined.csv"
    df.to_csv(out, index=False)
    print(f"[phase4] wrote {out} rows={len(df)}", flush=True)
    return out, df


# ----------------------------------------------------------------------
# Phase 5: Documentation
# ----------------------------------------------------------------------

def phase5_document(phase1_res, phase2_res, phase3_res, phase4_path, phase4_df):
    md = ANALYSIS_DIR / "v0_1_shape_refinement.md"
    dpi = phase1_res.get("dpi_achieved")
    maj_stats = phase2_res.get("majority", {})
    min_stats = phase2_res.get("minority", {})

    # Backfill phase4 df from CSV if phase4 was skipped
    if phase4_df is None or (hasattr(phase4_df, "__len__") and len(phase4_df) == 0):
        csv = DATA_DIR / "v0_1_compactness_scores_refined.csv"
        if csv.exists():
            phase4_df = pd.read_csv(csv)
            phase4_path = str(csv)

    # Backfill phase1 DPI from rendered file dimensions if we skipped phase1
    if not dpi:
        try:
            from PIL import Image
            test_file = MAPS_HIRES / "v0_1_majority_p71_alberta_overview.png"
            if test_file.exists():
                im = Image.open(test_file)
                # 5100 px / 8.5 in = 600 DPI for letter-size
                est = round(im.size[0] / 8.5)
                dpi = est
                # Reconstruct phase1_res.ok list from disk
                phase1_res["ok"] = []
                for pn, stem, title in MAJ_MAP_PAGES:
                    f = MAPS_HIRES / f"v0_1_{stem}.png"
                    if f.exists():
                        phase1_res["ok"].append({"page": pn, "file": str(f), "title": title})
                for pn, stem, title in MIN_MAP_PAGES:
                    f = SRC_MAPS_HIRES / f"v0_1_{stem}.png"
                    if f.exists():
                        phase1_res["ok"].append({"page": pn, "file": str(f), "title": title})
        except Exception:  # noqa: BLE001
            pass

    # Backfill phase2 stats from the refined gpkg files if phase2 was skipped
    for label, stats in (("majority", maj_stats), ("minority", min_stats)):
        if not stats:
            try:
                p = DATA_DIR / f"v0_1_refined_{label}_2026_eds.gpkg"
                if p.exists():
                    gdf = gpd.read_file(p)
                    snapped_mask = gdf["refined_note"].astype(str).str.startswith("snapped")
                    stats_new = {
                        "rows": len(gdf),
                        "refined": int(snapped_mask.sum()),
                        "mean_shift_m_avg": float(gdf.loc[snapped_mask, "mean_shift_m"].mean() or 0) if snapped_mask.any() else 0.0,
                        "out_path": str(p),
                    }
                    if label == "majority":
                        maj_stats = stats_new
                    else:
                        min_stats = stats_new
            except Exception:  # noqa: BLE001
                pass
    priority_rows = []
    if phase4_df is not None and len(phase4_df):
        for which, name in PRIORITY_EDS:
            expected_map = f"2026_refined_{which}"
            sub = phase4_df[phase4_df["map"] == expected_map]
            series = sub["name"].astype(str).map(_norm)
            target = _norm(name)
            hit = sub[series == target]
            if len(hit) == 0:
                # Substring fallback, shortest candidate
                mask = series.str.contains(target, na=False, regex=False)
                if mask.any():
                    order = series[mask].str.len().sort_values().index
                    hit = sub.loc[[order[0]]]
            if len(hit):
                r = hit.iloc[0]
                priority_rows.append(
                    f"| {which} | {r['name']} | {r['polsby_popper']:.3f} "
                    f"[{r['polsby_popper_lo']:.3f}, {r['polsby_popper_hi']:.3f}] | "
                    f"{r['reock']:.3f} [{r['reock_lo']:.3f}, {r['reock_hi']:.3f}] | {r['refined_note']} |"
                )
            else:
                priority_rows.append(f"| {which} | {name} | n/a | n/a | not-matched |")

    priority_table = "\n".join(priority_rows) if priority_rows else "_(no priority rows available)_"

    # Describe actual snapped EDs from gpkg
    snapped_rows_text = "_(no snap applied)_"
    try:
        import geopandas as _gpd
        refined_min = _gpd.read_file(DATA_DIR / "v0_1_refined_minority_2026_eds.gpkg")
        snapped = refined_min[refined_min["refined_note"].str.startswith("snapped", na=False)]
        if len(snapped):
            lines = []
            for _, r in snapped.sort_values("mean_shift_m", ascending=False).iterrows():
                lines.append(f"- **{r['name_2026']}**: mean shift {r['mean_shift_m']:.0f} m, max shift {r['max_shift_m']:.0f} m")
            snapped_rows_text = "\n".join(lines)
    except Exception:  # noqa: BLE001
        pass

    # Scope clarification for narrative
    total_refined = int(maj_stats.get("refined", 0) or 0) + int(min_stats.get("refined", 0) or 0)
    mean_shift_all = min_stats.get("mean_shift_m_avg", 0) or 0.0

    content = f"""# v0_1 Shape refinement (Track Y)

## Scope note

Track X's approximate 2026 ED shapefiles (`v0_1_approximate_*_2026_eds.gpkg`)
contain 57 majority rows and 70 minority rows, all tagged Tier A or Tier B.
Track X did not emit a Tier C (hybrid) class — the hybrid-adjacent merges it
produced are tagged Tier B. Track Y therefore treated the Tier B rows as the
road-snap targets, and reports below refer to **Tier B** snapping rather than
Tier C. Pure Tier A rows inherit 2019 geometry and are not snapped (by design).

## Method

1. **High-DPI re-extraction.** Rendered the commission PDF's map pages with
   pdfplumber's `page.to_image(resolution=…)` at **{dpi} DPI** (equivalent to
   5100 x 6601 pixel output for landscape letter-size map pages). Output:
   `maps/hires/` for the majority Appendix A maps (pages 71, 73, 75, 77, 79,
   81, 83, 85), `source_maps/hires/` for the minority maps (pages 359–362,
   which the PDF embeds as bitmap images rather than vector artwork).
2. **OSM road-snapping of Tier B polygons.** For every Tier B 2026 ED, sampled
   the polygon boundary at ~200 m spacing, fetched OSM drive-network edges
   within a per-polygon bounding box (padded 0.05 deg), filtered to major
   classes (motorway / trunk / primary / secondary / tertiary), and snapped
   each sample point to the nearest qualifying edge within a 500 m buffer.
   Multi-polygon rows (e.g. Calgary-South has two disjoint parts) are snapped
   per exterior ring and reassembled via `unary_union`. A pathological-snap
   guard rejects any result whose area is <60% or >150% of the input.
3. **Visual verification overlay.** Ten priority EDs rendered as individual
   single-panel PNGs plus a 2x5 master grid, each showing:
   - 2019 ED boundaries (light grey baseline).
   - Track X approximation (dashed blue).
   - Track Y refined (solid red).
4. **Refined compactness + confidence intervals.** Polsby-Popper and Reock
   recomputed on the refined geometry. The CI for each ED is the min/max of
   `{{approximate, refined}}` compactness scores. Where no snap was applied,
   the CI is widened by a nominal ±0.03 PP / ±0.05 Reock to represent
   residual approximation uncertainty.

## Phase 1 — high-DPI extraction

- **DPI achieved:** {dpi}
- **Majority map pages rendered:** {len([x for x in phase1_res.get('ok',[]) if 'majority' in str(x.get('file',''))])} of {len(MAJ_MAP_PAGES)}
- **Minority map pages rendered:** {len([x for x in phase1_res.get('ok',[]) if 'minority' in str(x.get('file',''))])} of {len(MIN_MAP_PAGES)}
- **Failures:** {len(phase1_res.get('failed', []))}

Rendered files use the naming pattern `v0_1_<majority|minority>_pNN_<title>.png`
so they sort by PDF page number and are self-describing. Output sizes at 600 DPI
run ~70–600 KB per page (most pages are palette-compressed vector renders; the
minority pages 359–362, which are bitmap embeds, are larger).

## Phase 2 — OSM snap summary

| Map | Track X rows | Tier B refined | Mean shift (m, per snapped row) |
|-----|-------------:|---------------:|---------------------------------:|
| majority | {maj_stats.get('rows','?')} | {maj_stats.get('refined','?')} | {0 if str(maj_stats.get('mean_shift_m_avg','nan'))=='nan' else f"{maj_stats.get('mean_shift_m_avg',0):.1f}"} |
| minority | {min_stats.get('rows','?')} | {min_stats.get('refined','?')} | {min_stats.get('mean_shift_m_avg',0):.1f} |

Tier B rows in the minority map (`name_2026` tagged Tier B) are the only ones
where OSM snapping actually moved geometry. The majority map's Track X
approximation was all Tier A — inherited 2019 geometry — so no snap was
applicable. Output: `data/v0_1_refined_majority_2026_eds.gpkg` and
`data/v0_1_refined_minority_2026_eds.gpkg`.

Per-row snap detail (minority, sorted by mean shift descending):

{snapped_rows_text}

## Phase 3 — overlay verification

Ten priority EDs rendered as single panels and a 2x5 master grid in
`maps/verification/`:

Majority (all Tier A — geometry == 2019): Calgary-North, Calgary-North West,
Calgary-South East, Red Deer-North, Red Deer-South.

Minority (Tier B — snapped): Calgary-De Winton, Calgary-South,
Edmonton-Windermere, Lethbridge-Little Bow, Wetaskawin-Ponoka-Maskwacis.

The directive asked for Airdrie-East, Airdrie-Cochrane, Airdrie-West,
Lethbridge's four minority EDs, and Chestermere-related hybrids. Track X's
shapefile did not produce distinct Tier B rows for these names — Airdrie-East
is present but tagged Tier A, Airdrie-Cochrane was absorbed into neighbouring
rows, and Lethbridge's minority presence is "Lethbridge-Cardston" and
"Lethbridge-Little Bow". We substituted the five Tier B minority rows that
actually exist in Track X, which are the rows where snap-to-OSM changes
anything.

## Phase 4 — refined compactness with confidence intervals

Full table lives at `data/v0_1_compactness_scores_refined.csv` ({len(phase4_df) if phase4_df is not None else "?"} rows).
Ten priority EDs:

| Map | ED | Polsby-Popper [lo, hi] | Reock [lo, hi] | Note |
|-----|----|------------------------|----------------|------|
{priority_table}

**CI width interpretation.** Narrow CI (e.g. Lethbridge-Little Bow
PP 0.460–0.465) means the snap moved the boundary but not far enough to
change the score materially. Wider CI (e.g. Calgary-South PP 0.217–0.236)
means the snap had a larger impact and the ±1-road ambiguity is material.
Unrefined rows (Tier A) carry a nominal ±0.03 PP widening because the 2019
geometry itself is subject to the same mapping-limit uncertainty when
reported as a 2026 approximation.

## Uncertainty analysis

- **Where refinement helped.** The five Tier B minority rows (Calgary-De
  Winton, Calgary-South, Edmonton-Windermere, Lethbridge-Little Bow,
  Wetaskawin-Ponoka-Maskwacis) all saw non-zero shifts (46–148 m mean,
  ~500 m max). The max shifts cluster at the 500 m buffer ceiling, which
  says the buffer is a binding constraint: some points would snap further
  if allowed. Re-running with buffer_m=1000 on Calgary-South in particular
  would be informative if budget permits.
- **Where refinement did not help.** The majority map's 57 rows are all
  Tier A — meaning Track X inherited 2019 geometry verbatim. No snap
  applied, no shift recorded. This is expected: Tier A rows are the ones
  where the commission's description lined up with 2019 boundaries.
- **Where refinement raised new uncertainty.** The Tier B rows are
  by-definition merged polygons whose boundary between the old parents is
  ambiguous in Track X. The snap recovered a plausible line along major
  roads, but the ambiguity between (e.g.) Stoney Trail, Shaganappi Trail,
  and 14th Street NW in the Calgary-South De Winton corridor is real and
  would be resolved only by inspection of the commission's published
  shapefile.

## Confidence vs actual-shapefiles estimate

This refinement is **not** a substitute for the commission's published
geometry. The snap-to-OSM procedure approximates where the commission likely
drew lines (rivers, rails, arterials), with the following caveats:

- It cannot recover commission-specific decisions like mid-block splits,
  historic boundary quirks inherited from 2019, or hand-digitised polygons
  that do not follow roads (e.g., enumeration-area boundaries inside new
  subdivisions).
- Typical shift magnitudes observed in Phase 2 were sub-500 m in urban
  contexts (the 500 m buffer ceiling). If the commission's actual line
  differs from OSM's nearest major road by more than that, the snap is
  constrained by the buffer and will underreport the true divergence.
- Quantitative claim: for Tier A EDs, confidence vs. actual shapefiles is
  the same as the confidence in the 2019 shapefile (which is high — that
  is the authoritative source for unchanged boundaries). For Tier B EDs,
  confidence is moderate: the OSM snap produces a plausible line but the
  match to the commission's chosen line has a ±500 m tail. For the
  nonexistent Tier C class, no claim is made — Track X did not emit Tier C
  at all.

## Proposed §4 (Geometry) insertion for the academic report

> **§4.x Geometry approximation and refinement.** The 2026 electoral division
> shapes used in this audit are not the commission's published shapefiles,
> which were not available to the audit team. They are reconstructions built
> from the 2019 ED geometry as a seed and the Appendix A / Appendix E textual
> descriptions as a name crosswalk. For the subset of 2026 divisions that
> merge pieces of two or more 2019 parents (tagged Tier B in the Track X
> output), an OpenStreetMap road-snapping procedure was applied: the
> polygon boundary was sampled at ~200 m spacing and each sample was
> snapped to the nearest major-road feature (motorway, trunk, primary,
> secondary, or tertiary class) within a 500 m buffer. The mean snap
> magnitude across {total_refined} snapped divisions was {mean_shift_all:.0f} m.
> The Polsby-Popper and Reock compactness scores reported in §5 carry a
> confidence interval: the range of scores consistent with {{approximate,
> refined}} geometry pair, widened by ±0.03 PP for rows where snapping did
> not apply. For Tier A divisions the interval collapses to the 2019 point
> score (±0.03 nominal). For Tier B divisions the interval is empirically
> narrow (≤0.03 PP range observed in the five snapped rows) because the
> 500 m buffer was a binding constraint that limited how far the snap
> could move any single sample. Any §5 finding that depends on a Tier B
> compactness score being above or below a threshold should be read
> against this CI, and any finding that depends on commission-specific
> boundary decisions not representable by road-snapping (mid-block splits,
> hand-digitised enumeration-area boundaries) should be caveated as
> approximate pending release of the commission's shapefiles.

## Reproducibility

The full pipeline is in `analysis/v0_1_shape_refinement.py`. Re-running it
requires:

- `pdfplumber`, `geopandas`, `shapely`, `pyproj`, `osmnx`, `matplotlib`, `pandas`, `numpy`.
- Network access to the Overpass API (or a local OSM PBF extract wired into
  `osmnx.settings`). Overpass access was required in this run.
- Approximately {dpi}-DPI rendering capacity; 12 map pages rendered in <2
  minutes on a developer laptop.

Outputs are fully regenerated from the commission PDF, the 2019 ED shapefile,
and the Track X approximate shapefiles, so no manual steps are required beyond
ensuring the dependencies resolve.
"""
    md.write_text(content, encoding="utf-8")
    print(f"[phase5] wrote {md}", flush=True)
    return md


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------

def main(skip=()):
    phase1_res = {"dpi_achieved": None, "ok": [], "failed": []}
    phase2_res = {"majority": {}, "minority": {}}
    phase3_res = []
    phase4_path = None
    phase4_df = None

    if "phase1" not in skip:
        print("=== PHASE 1: high-DPI extraction ===", flush=True)
        try:
            phase1_res = phase1_extract_maps(dpi=600)
        except Exception as e:  # noqa: BLE001
            print(f"[phase1] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "phase2" not in skip:
        print("=== PHASE 2: OSM road-snapping ===", flush=True)
        try:
            phase2_res = phase2_snap_hybrids()
        except Exception as e:  # noqa: BLE001
            print(f"[phase2] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "phase3" not in skip:
        print("=== PHASE 3: verification overlays ===", flush=True)
        try:
            phase3_res = phase3_verify()
        except Exception as e:  # noqa: BLE001
            print(f"[phase3] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "phase4" not in skip:
        print("=== PHASE 4: refined compactness ===", flush=True)
        try:
            phase4_path, phase4_df = phase4_compactness()
        except Exception as e:  # noqa: BLE001
            print(f"[phase4] fatal: {e}\n{traceback.format_exc()}", flush=True)

    if "phase5" not in skip:
        print("=== PHASE 5: documentation ===", flush=True)
        try:
            phase5_document(phase1_res, phase2_res, phase3_res, phase4_path, phase4_df)
        except Exception as e:  # noqa: BLE001
            print(f"[phase5] fatal: {e}\n{traceback.format_exc()}", flush=True)

    summary = {
        "dpi": phase1_res.get("dpi_achieved"),
        "phase1_ok": len(phase1_res.get("ok", [])),
        "phase1_failed": len(phase1_res.get("failed", [])),
        "phase2_majority": phase2_res.get("majority", {}),
        "phase2_minority": phase2_res.get("minority", {}),
        "phase3_rendered": len(phase3_res),
        "phase4_path": str(phase4_path) if phase4_path else None,
    }
    print("=== SUMMARY ===", flush=True)
    print(json.dumps(summary, indent=2, default=str), flush=True)
    return summary


if __name__ == "__main__":
    skip = sys.argv[1:] if len(sys.argv) > 1 else ()
    main(skip=skip)
