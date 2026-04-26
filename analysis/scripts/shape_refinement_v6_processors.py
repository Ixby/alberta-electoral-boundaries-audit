"""
Per-thumbnail processors for v6 pipeline.

Georef strategy: distance-transform optimisation of a 6-parameter affine
matching 2019 Tier A boundary points to the red-mask pixels of the
thumbnail. This produces sub-100m georef residuals when the minority map
leaves Tier A boundaries unchanged (true for ~80% of Calgary inner EDs).
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import time
from pathlib import Path

import cv2
import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

from shape_refinement_v6 import (
    ROOT, MAPS_HIRES, VERIFY_DIR, DATA_DIR, ANALYSIS_DIR, TEMP_DIR,
    AREA_CRS, V5_MIN_GPKG,
    load_and_orient, extract_red_mask, get_interior_mask,
    fit_affine, apply_affine,
    flood_fill_interior, extract_contour, contour_to_polygon,
    disproof_pass, render_overlay_qa, render_verification_panel,
)


# ---------------------------------------------------------------------------
# Distance-transform optimisation for affine geo->pixel
# ---------------------------------------------------------------------------

def optimise_affine_dt(
    red_mask: np.ndarray,
    boundary_pts_geo: np.ndarray,  # (N, 2) in AREA_CRS
    initial_scale: float = 13.5,
    initial_tx: float = 510000.0,
    initial_ty: float = 5690000.0,
) -> tuple[np.ndarray, float, dict]:
    """Optimise 6-param affine (geo -> pixel) by minimising distance
    transform from projected boundary points to red mask.

    Returns (M_px2geo 2x3, cost_final, info).
    """
    H, W = red_mask.shape
    not_red = (red_mask == 0).astype(np.uint8) * 255
    dt = cv2.distanceTransform(not_red, cv2.DIST_L2, maskSize=3)

    def cost(params):
        a, b, c, d, e, f = params
        px = a * boundary_pts_geo[:, 0] + b * boundary_pts_geo[:, 1] + c
        py = d * boundary_pts_geo[:, 0] + e * boundary_pts_geo[:, 1] + f
        valid = (px >= 0) & (px < W - 1) & (py >= 0) & (py < H - 1)
        if valid.sum() < 500:
            return 1e10
        px_v = px[valid].astype(np.int32)
        py_v = py[valid].astype(np.int32)
        pen = (len(boundary_pts_geo) - valid.sum()) * 50.0
        return float(dt[py_v, px_v].mean() + pen / len(boundary_pts_geo))

    # Initial: forward geo->pixel with y-flip.
    # geo_x = s*px + tx  =>  px = (geo_x - tx) / s
    # geo_y = -s*py + ty =>  py = (ty - geo_y) / s
    # So a = 1/s, b = 0, c = -tx/s; d = 0, e = -1/s, f = ty/s
    s = initial_scale; tx = initial_tx; ty = initial_ty
    x0 = [1 / s, 0.0, -tx / s, 0.0, -1 / s, ty / s]
    c0 = cost(x0)

    # Brute-force pre-search for good initial tx/ty
    # HIGH-02: replaced np.arange on floats with np.linspace and
    # explicit point counts. np.arange accumulates floating-point
    # error and on the s dimension could return 12 or 13 points
    # depending on rounding, silently missing the upper boundary cell.
    # linspace with inclusive endpoint gives a deterministic grid:
    #   tx, ty: 11 points spanning +/-50000 at 10000 spacing
    #   s:      13 points spanning +/-3 at 0.5 spacing
    # This expands the search by one boundary cell per axis versus
    # the arange version but never drops a cell under any platform.
    best = (c0, x0)
    tx_grid = np.linspace(initial_tx - 50000, initial_tx + 50000, 11)
    ty_grid = np.linspace(initial_ty - 50000, initial_ty + 50000, 11)
    s_grid = np.linspace(initial_scale - 3, initial_scale + 3, 13)
    for tx_try in tx_grid:
        for ty_try in ty_grid:
            for s_try in s_grid:
                x_try = [1 / s_try, 0, -tx_try / s_try, 0, -1 / s_try, ty_try / s_try]
                c_try = cost(x_try)
                if c_try < best[0]:
                    best = (c_try, x_try)

    res = minimize(
        cost, best[1], method="Nelder-Mead",
        options={"xatol": 1e-9, "fatol": 0.01, "maxiter": 5000, "maxfev": 10000, "adaptive": True},
    )
    a, b, c, d, e, f = res.x
    FM = np.array([[a, b], [d, e]])
    FM_inv = np.linalg.inv(FM)
    # px -> geo: geo = FM_inv @ (p - t)
    t = np.array([c, f])
    t_inv = -FM_inv @ t
    M_px2geo = np.hstack([FM_inv, t_inv.reshape(2, 1)])
    det = abs(a * e - b * d)
    return M_px2geo, float(res.fun), {
        "pixel_dim_m": float(np.sqrt(1 / det)),
        "initial_cost": float(c0),
        "brute_cost": float(best[0]),
        "final_cost": float(res.fun),
        "n_boundary_points": len(boundary_pts_geo),
        "M_geo2px_params": [float(v) for v in res.x],
    }


def collect_boundary_points(
    eds2019: gpd.GeoDataFrame,
    ed_names: list,
    interval_m: float = 200.0,
) -> np.ndarray:
    sub = eds2019[eds2019["EDName2017"].isin(ed_names)].copy()
    pts = []
    for g in sub.geometry:
        geoms = [g] if g.geom_type == "Polygon" else list(g.geoms)
        for p in geoms:
            line = LineString(list(p.exterior.coords))
            for d in np.arange(0, line.length, interval_m):
                pt = line.interpolate(d)
                pts.append((pt.x, pt.y))
    return np.array(pts)


# ---------------------------------------------------------------------------
# Common per-ED processing
# ---------------------------------------------------------------------------

def _hard_contains(lat: float, lon: float):
    pt = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326").to_crs(AREA_CRS).iloc[0]
    def fn(poly):
        return poly.contains(pt)
    fn.__name__ = f"contains_point({lat},{lon})"
    return fn


def _lat_to_y(lat: float) -> float:
    pt = gpd.GeoSeries([Point(-113.5, lat)], crs="EPSG:4326").to_crs(AREA_CRS).iloc[0]
    return pt.y


def _lon_to_x(lon: float) -> float:
    pt = gpd.GeoSeries([Point(lon, 51.0)], crs="EPSG:4326").to_crs(AREA_CRS).iloc[0]
    return pt.x


def _safe_slug(s: str) -> str:
    return s.lower().replace(" ", "_").replace("-", "_").replace("'", "")


def _process_one_target(
    ed_name, seed_px, interior_mask, red_mask, img, M,
    hard_constraints, adjacent_ed_geo,
    verify_out, overlay_out, v5_geo,
):
    H, W = img.shape[:2]
    log_ed = {"seed_px": list(seed_px)}
    try:
        label_mask, info = flood_fill_interior(interior_mask, seed_px)
        log_ed["flood_fill"] = info
    except Exception as e:
        log_ed["status"] = "FLOOD_FAIL"
        log_ed["error"] = str(e)
        return None, log_ed

    if info["area_px"] > 0.30 * H * W:
        log_ed["status"] = "SEED_OUTSIDE_ED"
        log_ed["error"] = f"flood area {info['area_px']} > 30% of image"
        return None, log_ed

    try:
        contour_px = extract_contour(label_mask, approx_tol_px=1.5)
        log_ed["contour_px_pts"] = len(contour_px)
    except Exception as e:
        log_ed["status"] = "CONTOUR_FAIL"
        log_ed["error"] = str(e)
        return None, log_ed

    try:
        poly_geo = contour_to_polygon(contour_px, M, simplify_tol_m=40.0)
    except Exception as e:
        log_ed["status"] = "POLYGON_FAIL"
        log_ed["error"] = str(e)
        return None, log_ed

    log_ed["area_km2"] = round(poly_geo.area / 1e6, 2)
    log_ed["bounds"] = [round(v, 0) for v in poly_geo.bounds]

    disproof = disproof_pass(
        ed_name, poly_geo, contour_px, red_mask, label_mask, M, (H, W),
        hard_constraints, adjacent_ed_geo,
    )
    log_ed["disproof_attempts"] = disproof

    qa = render_overlay_qa(ed_name, contour_px, red_mask, img, overlay_out)
    disproof["t2_overlay_visual_diff"] = {
        "n_yellow_px": qa["n_yellow_px"],
        "n_large_clusters": qa["n_large_clusters"],
        "pass": qa["t2_pass"],
    }
    considered = [k for k, v in disproof.items()
                  if isinstance(v, dict) and v.get("pass") is not None]
    n_pass = sum(1 for k in considered if disproof[k]["pass"])
    disproof["summary"] = {"n_pass": n_pass, "n_considered": len(considered)}

    try:
        render_verification_panel(ed_name, poly_geo, v5_geo, verify_out)
    except Exception as e:
        log_ed["verify_render_err"] = str(e)

    log_ed["status"] = "OK"
    log_ed["overlay"] = str(overlay_out.name)
    log_ed["verification_panel"] = str(verify_out.name)
    return poly_geo, log_ed


# ===========================================================================
# CALGARY MINORITY
# ===========================================================================

def process_calgary_minority(eds2019):
    t0 = time.time()
    thumb = MAPS_HIRES / "v0_1_minority_p360_map74.png"
    img = load_and_orient(thumb, "rot90cw")
    H, W = img.shape[:2]
    red = extract_red_mask(img)
    interior = get_interior_mask(red)

    # Use inner-Calgary 2019 EDs for DT optimisation
    inner_names = [
        "Calgary-Acadia", "Calgary-Beddington", "Calgary-Bow", "Calgary-Buffalo",
        "Calgary-Cross", "Calgary-Currie", "Calgary-Edgemont", "Calgary-Elbow",
        "Calgary-Falconridge", "Calgary-Fish Creek", "Calgary-Foothills",
        "Calgary-Glenmore", "Calgary-Hays", "Calgary-Klein", "Calgary-Lougheed",
        "Calgary-McCall", "Calgary-Mountain View", "Calgary-North", "Calgary-North East",
        "Calgary-North West", "Calgary-Peigan", "Calgary-Shaw", "Calgary-South East",
        "Calgary-Varsity", "Calgary-West",
    ]
    boundary_pts = collect_boundary_points(eds2019, inner_names, interval_m=200)
    M, cost, info = optimise_affine_dt(red, boundary_pts,
                                       initial_scale=13.5, initial_tx=510000, initial_ty=5690000)
    print(f"  DT-affine: cost={cost:.2f}, pixel_dim={info['pixel_dim_m']:.2f} m/px")

    targets = {
        "Calgary-De Winton": (3500, 4100),
        "Calgary-South": (4337, 3289),
    }
    hc = {
        "Calgary-De Winton": {
            "contains_okotoks": _hard_contains(50.7258, -113.975),
        },
        "Calgary-South": {
            "near_calgary_centre": lambda p: (
                abs(p.centroid.x - 563000) < 30_000 and
                abs(p.centroid.y - 5655000) < 30_000
            ),
            "east_of_fish_creek": lambda p: p.bounds[0] > 563000,  # east of rough Fish Creek line
        },
    }
    adj_map = {"Calgary-De Winton": "Highwood", "Calgary-South": "Calgary-Hays"}
    adj_geo = {}
    for ed, adj_name in adj_map.items():
        sub = eds2019[eds2019["EDName2017"] == adj_name]
        adj_geo[ed] = sub.geometry.iloc[0] if not sub.empty else None

    v5 = gpd.read_file(V5_MIN_GPKG).to_crs(AREA_CRS)
    v5_map = {r["name_2026"]: r.geometry for _, r in v5.iterrows()}

    VERIFY_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    per_ed_log = {}
    for ed_name, seed in targets.items():
        slug = _safe_slug(ed_name)
        verify_out = VERIFY_DIR / f"v0_6_minority_{slug}.png"
        overlay_out = VERIFY_DIR / f"v0_6_overlay_minority_{slug}.png"
        poly, log = _process_one_target(
            ed_name, seed, interior, red, img, M,
            hc.get(ed_name), adj_geo.get(ed_name),
            verify_out, overlay_out, v5_map.get(ed_name),
        )
        if poly is not None:
            results[ed_name] = poly
        per_ed_log[ed_name] = log
        print(f"  {ed_name}: {log.get('status')} area={log.get('area_km2')} km2 "
              f"disproof={log.get('disproof_attempts', {}).get('summary', {})}")

    return results, {
        "thumbnail": thumb.name, "orientation": "rot90cw",
        "img_shape": [H, W],
        "red_pixels": int(np.count_nonzero(red)),
        "affine": {
            "M_px2geo": M.tolist(),
            "cost_dt_mean_px": round(cost, 2),
            "pixel_dim_m": round(info["pixel_dim_m"], 2),
            "n_boundary_pts": info["n_boundary_points"],
        },
        "per_ed": per_ed_log,
        "elapsed_s": round(time.time() - t0, 1),
    }


# ===========================================================================
# EDMONTON MINORITY
# ===========================================================================

def process_edmonton_minority(eds2019):
    t0 = time.time()
    thumb = MAPS_HIRES / "v0_1_minority_p361_map75.png"
    img = load_and_orient(thumb, "native")
    H, W = img.shape[:2]
    red = extract_red_mask(img)
    interior = get_interior_mask(red)

    # Edmonton inner-city EDs (Tier A in both 2019 and 2026 minority)
    inner_names = [
        "Edmonton-Beverly-Clareview", "Edmonton-Castle Downs", "Edmonton-City Centre",
        "Edmonton-Decore", "Edmonton-Ellerslie", "Edmonton-Glenora", "Edmonton-Gold Bar",
        "Edmonton-Highlands-Norwood", "Edmonton-Manning", "Edmonton-McClung",
        "Edmonton-Meadows", "Edmonton-Mill Woods", "Edmonton-North West",
        "Edmonton-Riverview", "Edmonton-Rutherford", "Edmonton-South-West",
        "Edmonton-Strathcona", "Edmonton-West Henday", "Edmonton-Whitemud",
    ]
    # Filter to those that exist in 2019
    valid_inner = [n for n in inner_names if (eds2019["EDName2017"] == n).any()]
    boundary_pts = collect_boundary_points(eds2019, valid_inner, interval_m=200)
    # Edmonton's initial params: approx. EPSG:3400 centre (600000, 5930000), pixel_dim ~ 13
    M, cost, info = optimise_affine_dt(red, boundary_pts,
                                       initial_scale=13.5, initial_tx=580000, initial_ty=5955000)
    print(f"  DT-affine: cost={cost:.2f}, pixel_dim={info['pixel_dim_m']:.2f} m/px")

    targets = {
        "Edmonton-Windermere": (3350, 3700),
    }
    hc = {
        "Edmonton-Windermere": {
            "south_of_river": lambda p: p.bounds[3] <= _lat_to_y(53.55) + 500,
        },
    }
    adj_geo = {}
    sub = eds2019[eds2019["EDName2017"] == "Edmonton-Whitemud"]
    if not sub.empty:
        adj_geo["Edmonton-Windermere"] = sub.geometry.iloc[0]

    v5 = gpd.read_file(V5_MIN_GPKG).to_crs(AREA_CRS)
    v5_map = {r["name_2026"]: r.geometry for _, r in v5.iterrows()}

    results = {}
    per_ed_log = {}
    for ed_name, seed in targets.items():
        slug = _safe_slug(ed_name)
        verify_out = VERIFY_DIR / f"v0_6_minority_{slug}.png"
        overlay_out = VERIFY_DIR / f"v0_6_overlay_minority_{slug}.png"
        poly, log = _process_one_target(
            ed_name, seed, interior, red, img, M,
            hc.get(ed_name), adj_geo.get(ed_name),
            verify_out, overlay_out, v5_map.get(ed_name),
        )
        if poly is not None:
            results[ed_name] = poly
        per_ed_log[ed_name] = log
        print(f"  {ed_name}: {log.get('status')} area={log.get('area_km2')} km2")

    return results, {
        "thumbnail": thumb.name, "orientation": "native",
        "img_shape": [H, W],
        "red_pixels": int(np.count_nonzero(red)),
        "affine": {
            "M_px2geo": M.tolist(),
            "cost_dt_mean_px": round(cost, 2),
            "pixel_dim_m": round(info["pixel_dim_m"], 2),
            "n_boundary_pts": info["n_boundary_points"],
        },
        "per_ed": per_ed_log,
        "elapsed_s": round(time.time() - t0, 1),
    }


# ===========================================================================
# CALGARY MAJORITY
# ===========================================================================

def process_calgary_majority(eds2019):
    t0 = time.time()
    thumb = MAPS_HIRES / "v0_1_majority_p72_MAP_r600.png"
    img = load_and_orient(thumb, "rot90cw")
    H, W = img.shape[:2]
    red = extract_red_mask(img)
    interior = get_interior_mask(red)

    # Same inner-Calgary list; many of these remain Tier A in majority
    inner_names = [
        "Calgary-Acadia", "Calgary-Beddington", "Calgary-Bow", "Calgary-Buffalo",
        "Calgary-Cross", "Calgary-Currie", "Calgary-Edgemont", "Calgary-Elbow",
        "Calgary-Falconridge", "Calgary-Fish Creek", "Calgary-Foothills",
        "Calgary-Glenmore", "Calgary-Hays", "Calgary-Klein", "Calgary-Lougheed",
        "Calgary-McCall", "Calgary-Mountain View", "Calgary-North", "Calgary-North East",
        "Calgary-North West", "Calgary-Peigan", "Calgary-Shaw", "Calgary-South East",
        "Calgary-Varsity", "Calgary-West",
    ]
    boundary_pts = collect_boundary_points(eds2019, inner_names, interval_m=200)
    M, cost, info = optimise_affine_dt(red, boundary_pts,
                                       initial_scale=13.5, initial_tx=510000, initial_ty=5690000)
    print(f"  DT-affine: cost={cost:.2f}, pixel_dim={info['pixel_dim_m']:.2f} m/px")

    targets = {
        "Calgary-East": (4500, 2400),
        "Calgary-Falconridge-Conrich": (4700, 1600),
        "Calgary-Glenmore-Tsuut'ina": (2800, 2500),
        "Calgary-West-Elbow Valley": (2500, 3200),
    }
    hc = {}
    adj_geo = {}

    results = {}
    per_ed_log = {}
    for ed_name, seed in targets.items():
        slug = _safe_slug(ed_name)
        verify_out = VERIFY_DIR / f"v0_6_majority_{slug}.png"
        overlay_out = VERIFY_DIR / f"v0_6_overlay_majority_{slug}.png"
        poly, log = _process_one_target(
            ed_name, seed, interior, red, img, M,
            None, None, verify_out, overlay_out, None,
        )
        if poly is not None:
            results[ed_name] = poly
        per_ed_log[ed_name] = log
        print(f"  {ed_name}: {log.get('status')} area={log.get('area_km2')} km2")

    return results, {
        "thumbnail": thumb.name, "orientation": "rot90cw",
        "img_shape": [H, W],
        "red_pixels": int(np.count_nonzero(red)),
        "affine": {
            "M_px2geo": M.tolist(),
            "cost_dt_mean_px": round(cost, 2),
            "pixel_dim_m": round(info["pixel_dim_m"], 2),
            "n_boundary_pts": info["n_boundary_points"],
        },
        "per_ed": per_ed_log,
        "elapsed_s": round(time.time() - t0, 1),
    }


# ===========================================================================
# EDMONTON MAJORITY
# ===========================================================================

def process_edmonton_majority(eds2019):
    t0 = time.time()
    thumb = MAPS_HIRES / "v0_1_majority_p74_MAP_r600.png"
    img = load_and_orient(thumb, "native")
    H, W = img.shape[:2]
    red = extract_red_mask(img)
    interior = get_interior_mask(red)

    inner_names = [
        "Edmonton-Beverly-Clareview", "Edmonton-Castle Downs", "Edmonton-City Centre",
        "Edmonton-Decore", "Edmonton-Ellerslie", "Edmonton-Glenora", "Edmonton-Gold Bar",
        "Edmonton-Highlands-Norwood", "Edmonton-Manning", "Edmonton-McClung",
        "Edmonton-Meadows", "Edmonton-Mill Woods", "Edmonton-North West",
        "Edmonton-Riverview", "Edmonton-Rutherford", "Edmonton-South-West",
        "Edmonton-Strathcona", "Edmonton-West Henday", "Edmonton-Whitemud",
    ]
    valid_inner = [n for n in inner_names if (eds2019["EDName2017"] == n).any()]
    boundary_pts = collect_boundary_points(eds2019, valid_inner, interval_m=200)
    M, cost, info = optimise_affine_dt(red, boundary_pts,
                                       initial_scale=13.5, initial_tx=580000, initial_ty=5955000)
    print(f"  DT-affine: cost={cost:.2f}, pixel_dim={info['pixel_dim_m']:.2f} m/px")

    targets = {
        "Edmonton-Beaumont": (3796, 4193),
        "Edmonton-Enoch": (2400, 2800),
    }
    results = {}
    per_ed_log = {}
    for ed_name, seed in targets.items():
        slug = _safe_slug(ed_name)
        verify_out = VERIFY_DIR / f"v0_6_majority_{slug}.png"
        overlay_out = VERIFY_DIR / f"v0_6_overlay_majority_{slug}.png"
        poly, log = _process_one_target(
            ed_name, seed, interior, red, img, M,
            None, None, verify_out, overlay_out, None,
        )
        if poly is not None:
            results[ed_name] = poly
        per_ed_log[ed_name] = log
        print(f"  {ed_name}: {log.get('status')} area={log.get('area_km2')} km2")

    return results, {
        "thumbnail": thumb.name, "orientation": "native",
        "img_shape": [H, W],
        "red_pixels": int(np.count_nonzero(red)),
        "affine": {
            "M_px2geo": M.tolist(),
            "cost_dt_mean_px": round(cost, 2),
            "pixel_dim_m": round(info["pixel_dim_m"], 2),
            "n_boundary_pts": info["n_boundary_points"],
        },
        "per_ed": per_ed_log,
        "elapsed_s": round(time.time() - t0, 1),
    }
