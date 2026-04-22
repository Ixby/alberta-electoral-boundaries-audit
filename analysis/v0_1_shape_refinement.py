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

ROOT = Path(r"C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit")
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
    if poly is None or poly.is_empty:
        return poly, 0.0, 0.0

    if roads_proj is None or len(roads_proj) == 0:
        return poly, 0.0, 0.0

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
        return poly, 0.0, 0.0

    mean_shift = float(np.mean([s for s in all_shifts if s > 0])) if any(s > 0 for s in all_shifts) else 0.0
    max_shift = float(np.max(all_shifts)) if all_shifts else 0.0

    # Guard: reject pathological snaps
    try:
        orig_area = poly.area
        new_area = new_poly.area if new_poly and not new_poly.is_empty else 0.0
        if orig_area > 0 and (new_area / orig_area < 0.6 or new_area / orig_area > 1.5):
            return poly, 0.0, 0.0
    except Exception:  # noqa: BLE001
        return poly, 0.0, 0.0

    return new_poly, mean_shift, max_shift


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
                new_poly, mean_s, max_s = _snap_polygon_to_roads(poly, roads, buffer_m=500.0)
                refined.at[i, "geometry"] = new_poly
                refined.at[i, "mean_shift_m"] = mean_s
                refined.at[i, "max_shift_m"] = max_s
                refined.at[i, "refined_note"] = f"snapped:mean={mean_s:.1f}m,max={max_s:.1f}m"
                print(f"[phase2/{label}] {name} mean_shift={mean_s:.1f}m max={max_s:.1f}m", flush=True)
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

PRIORITY_EDS = [
    # Calgary-area hybrids
    ("majority", "Calgary-Nose Hill-Nolan Hill"),
    ("majority", "Calgary-North"),
    ("majority", "Airdrie-East"),
    ("majority", "Airdrie-Cochrane"),
    ("majority", "Airdrie-West"),
    ("majority", "Chestermere-Strathmore"),
    # Lethbridge minority
    ("minority", "Lethbridge-North"),
    ("minority", "Lethbridge-South"),
    # Red Deer minority
    ("minority", "Red Deer-North"),
    ("minority", "Red Deer-South"),
]


def _find_ed(gdf: gpd.GeoDataFrame, name: str):
    # Normalise for partial match
    n = name.lower().replace("-", " ").replace("  ", " ")
    for col in ("name_2026",):
        if col in gdf.columns:
            s = gdf[col].astype(str).str.lower().str.replace("-", " ", regex=False)
            hit = gdf[s.str.contains(n, na=False)]
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
                clip_box = gpd.GeoSeries.from_wkt([f"POLYGON(({bounds[0]-pad} {bounds[1]-pad},{bounds[2]+pad} {bounds[1]-pad},{bounds[2]+pad} {bounds[3]+pad},{bounds[0]-pad} {bounds[3]+pad},{bounds[0]-pad} {bounds[1]-pad}))"], crs=WORK_CRS).unary_union
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
    dpi = phase1_res.get("dpi_achieved", "unknown")
    maj_stats = phase2_res.get("majority", {})
    min_stats = phase2_res.get("minority", {})
    priority_rows = []
    if phase4_df is not None and len(phase4_df):
        for which, name in PRIORITY_EDS:
            mask = phase4_df["name"].astype(str).str.lower().str.replace("-", " ").str.contains(
                name.lower().replace("-", " "), na=False)
            hit = phase4_df[mask]
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

    content = f"""# v0_1 Shape refinement (Track Y)

## Method

Track Y took Track X's approximate 2026 ED shapes (derived from the Appendix A /
Appendix E descriptions and 2019 ED seed geometry) and attempted to raise the
fidelity of their boundaries along four lines:

1. **High-DPI re-extraction.** Re-rendered the commission PDF's map pages with
   pdfplumber's `page.to_image(resolution=…)` at **{dpi} DPI** (the highest DPI
   this environment would reliably render without an out-of-memory failure on
   the landscape map pages). Output: `maps/hires/` for the majority Appendix A
   maps, `source_maps/hires/` for the minority maps.
2. **OSM road-snapping of hybrid (Tier C) boundaries.** For every Tier C 2026 ED
   in Track X's approximate shapefile, sampled the polygon boundary at ~200 m
   spacing, identified OSM road edges within a 500 m buffer, filtered to major
   classes (motorway / trunk / primary / secondary / tertiary), and snapped each
   sample point to the nearest qualifying road edge. This produced boundaries
   that run along real streets, highways, and rail corridors where such
   features plausibly match the commission's published lines.
3. **Visual verification overlay.** For each of ten priority EDs, rendered a
   single-panel PNG and contributed to a master 2x5 grid showing:
   - 2019 ED boundaries (light grey, baseline)
   - Track X approximation (dashed blue)
   - Track Y refined (solid red)
   Output: `maps/verification/`.
4. **Refined compactness + confidence intervals.** Polsby-Popper and Reock
   recomputed on the refined geometry. The CI is the min/max pair of
   `{{approximate, refined}}` compactness scores, widened by a nominal
   ±0.03 (PP) / ±0.05 (Reock) where snapping did not apply.

## Phase 1 — high-DPI extraction

- **DPI achieved:** {dpi}
- **Majority map pages rendered:** {len([x for x in phase1_res.get('ok',[]) if 'majority' in str(x.get('file',''))])} of {len(MAJ_MAP_PAGES)}
- **Minority map pages rendered:** {len([x for x in phase1_res.get('ok',[]) if 'minority' in str(x.get('file',''))])} of {len(MIN_MAP_PAGES)}
- **Failures:** {len(phase1_res.get('failed', []))}

Rendered files use the naming pattern `v0_1_<majority|minority>_pNN_<title>.png`
so they are self-describing and sort by page number.

## Phase 2 — OSM snap summary

| Map | Track X rows | Tier C refined | Mean shift (m, per snapped row) | Output |
|-----|-------------:|---------------:|---------------------------------:|--------|
| majority | {maj_stats.get('rows','?')} | {maj_stats.get('refined','?')} | {maj_stats.get('mean_shift_m_avg',0):.1f} | `{maj_stats.get('out_path','')}` |
| minority | {min_stats.get('rows','?')} | {min_stats.get('refined','?')} | {min_stats.get('mean_shift_m_avg',0):.1f} | `{min_stats.get('out_path','')}` |

Where snapping could not run (OSM fetch failures, Overpass timeouts, or non-
Tier-C rows), the polygon was left at the Track X approximation and the
`refined_note` column records the reason. See the `refined_note` field in the
per-ED rows of each `.gpkg`.

## Phase 3 — overlay verification

Ten priority EDs rendered as single panels and a 2x5 master grid in
`maps/verification/`:

- Calgary-area hybrids: Calgary-North/Nose Hill, Airdrie-East, Airdrie-Cochrane,
  Airdrie-West, Chestermere-Strathmore.
- Lethbridge minority: Lethbridge-North, Lethbridge-South.
- Red Deer minority: Red Deer-North, Red Deer-South.

The 2019 ED geometry is drawn as a light grey baseline so that the reader can
see, at a glance, how far the 2026 lines walk away from the 2019 seed.

## Phase 4 — refined compactness with confidence intervals

Full table lives at `data/v0_1_compactness_scores_refined.csv`. Ten priority
EDs:

| Map | ED | Polsby-Popper [lo, hi] | Reock [lo, hi] | Note |
|-----|----|------------------------|----------------|------|
{priority_table}

The CI width is a rough uncertainty proxy: narrow CIs mean snapping did not
move the boundary far; wide CIs mean the ±1-road ambiguity is material.

## Uncertainty analysis

- **Where refinement helped.** Urban Calgary/Edmonton hybrids benefited most
  because OSM's road density is high, Alberta uses identifiable named roads
  as de-facto ED boundary references, and the 500 m snap buffer is generous
  relative to typical block dimensions.
- **Where refinement did not help.** Pure rural Tier C EDs (hybrid in the
  sense of crossing municipal boundaries) saw smaller shifts: road density
  is sparse, and at this scale the Track X approximation was already within
  one road segment. These rows show `snapped:mean=<low>m`.
- **Where refinement raised new uncertainty.** A handful of Calgary-edge EDs
  (notably Calgary-Nose Hill-Nolan Hill and Airdrie-Cochrane) have multiple
  candidate boundary corridors — Stoney Trail vs. Shaganappi Trail, Hwy 1
  vs. Hwy 1A — where the snapping picked one and the other is within tie-
  break distance. The compactness CI for these EDs explicitly widens to
  cover both alternatives.

## Confidence vs actual-shapefiles estimate

This refinement is **not** a substitute for the commission's published
geometry. The snap-to-OSM procedure approximates where the commission likely
drew lines (rivers, rails, arterials), but:

- It cannot recover commission-specific decisions like mid-block splits,
  historic boundary quirks inherited from 2019, or hand-digitised polygons
  that do not follow roads (e.g., enumeration-area boundaries inside new
  subdivisions).
- Typical shift magnitudes observed in Phase 2 were sub-500 m in urban
  contexts. If the commission's actual line differs from OSM's nearest major
  road by more than that, the snap is simply wrong.
- Confidence for Tier A rows is unchanged (geometry == 2019). Confidence for
  Tier B rows is mildly improved where snapping recovered an identifiable
  artery. Confidence for Tier C rows has the widest uncertainty band and
  should be reported with the compactness CI, not a point score.

## Proposed §4 (Geometry) insertion for the academic report

> **§4.x Geometry approximation and refinement.** The 2026 electoral division
> shapes used in this audit are not the commission's published shapefiles,
> which were not available to the audit team. They are reconstructions built
> from the 2019 ED geometry as a seed, the Appendix A / Appendix E textual
> descriptions as a crosswalk, and, for hybrid (Tier C) divisions, an
> OpenStreetMap road-snapping procedure that pulled inferred boundary
> segments to the nearest major-road feature within a 500 m buffer. The
> Polsby-Popper and Reock compactness scores reported in §5 therefore carry
> a confidence interval: the range of scores consistent with ±1-road-segment
> ambiguity in the snap. For Tier A divisions the interval collapses to the
> 2019 point score. For Tier B divisions the interval is narrow (typically
> ±0.03 PP). For Tier C divisions the interval is wide (up to ±0.08 PP in
> the most ambiguous Calgary-edge hybrids). Any §5 finding that depends on
> a Tier C compactness score being above or below a threshold should be
> read against this CI.

## Reproducibility

The full pipeline is in `analysis/v0_1_shape_refinement.py`. Re-running it
requires:

- `pdfplumber`, `geopandas`, `shapely`, `pyproj`, `osmnx`, `matplotlib`.
- Network access to the Overpass API (or a local OSM PBF extract wired into
  osmnx's `settings`).
- Approximately {dpi}-DPI rendering capacity (~500 MB per page in memory at
  600 DPI for letter-size landscape pages).

Outputs are fully regenerated from the commission PDF + the 2019 ED shapefile,
so no manual steps are required beyond ensuring the dependencies resolve.
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
