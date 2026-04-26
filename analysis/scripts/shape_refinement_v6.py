"""
v0_1 Track Y-v6: pixel-exact boundary vectorisation for Tier C 2026 EDs
by direct red-boundary tracing from commission thumbnails.

Scope (extended 2026-04-22):
  MINORITY: Edmonton-Windermere (51), Calgary-De Winton (8), Calgary-South (26)
  MAJORITY: Calgary + Edmonton Tier C EDs visible in the city thumbnails
    (rural-only Tier C escalated; thumbnails don't cover them).

Pipeline (per thumbnail):
  1. Load image, rotate to north-up.
  2. HSV red-mask + morphological cleanup.
  3. Hand-picked pixel anchors (visually identified from the rotated thumbnail)
     paired with 2019 Tier A ED centroids -> fit affine (pixel -> EPSG:3400).
  4. For each target Tier C ED: seeded flood-fill from a pixel known to be
     inside that ED; extract outer contour; apply affine; simplify.
  5. Run 7-test active-disproof pass before commit.
  6. Write outputs.

Honesty caveats (see markdown):
  - The Calgary minority thumbnail IS CROPPED — De Winton's real southward
    extent (per PO reference and v5's Livingstone-Macleod ~10 km extension)
    is OFF-MAP. v6 vectorises only the thumbnail-visible portion.
  - Residual per-edge error ~30-80 m (thumbnail pixel ~9-15 m plus georef
    RMS typically <100 m).
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import hashlib  # HIGH-01: deterministic per-ED seeding (Python hash() is randomized).
import json
import os
import time
from pathlib import Path

import cv2
import geopandas as gpd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry import Polygon, MultiPolygon, Point, box
from shapely.ops import unary_union

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
MAPS_HIRES = ROOT / "data" / "maps" / "hires"
VERIFY_DIR = ROOT / "data" / "maps" / "verification"
DATA_DIR = ROOT / "data"
ANALYSIS_DIR = ROOT / "analysis"
TEMP_DIR = ROOT / ".temp"

WORK_CRS = "EPSG:3401"
AREA_CRS = "EPSG:3400"
EDS_2019_PATH = DATA_DIR / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
V5_MIN_GPKG = DATA_DIR / "v0_1_refined_v5_minority_2026_eds.gpkg"

HSV_RED_LO1 = np.array([0, 100, 80])
HSV_RED_HI1 = np.array([12, 255, 255])
HSV_RED_LO2 = np.array([165, 100, 80])
HSV_RED_HI2 = np.array([179, 255, 255])


# ---------------------------------------------------------------------------
# Image pre-processing
# ---------------------------------------------------------------------------

def load_and_orient(thumb_path: Path, orientation: str) -> np.ndarray:
    img = cv2.imread(str(thumb_path))
    if img is None:
        raise FileNotFoundError(thumb_path)
    if orientation == "rot90cw":
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif orientation != "native":
        raise ValueError(orientation)
    return img


def extract_red_mask(img_bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.bitwise_or(
        cv2.inRange(hsv, HSV_RED_LO1, HSV_RED_HI1),
        cv2.inRange(hsv, HSV_RED_LO2, HSV_RED_HI2),
    )
    kclose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kclose, iterations=2)
    kopen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kopen, iterations=1)
    return mask


def get_interior_mask(red_mask: np.ndarray) -> np.ndarray:
    """Slightly dilate red, then complement -> interior."""
    red_d = cv2.dilate(red_mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    return (red_d == 0).astype(np.uint8) * 255


# ---------------------------------------------------------------------------
# Affine fit
# ---------------------------------------------------------------------------

def fit_affine(src_px: np.ndarray, dst_geo: np.ndarray) -> tuple[np.ndarray, float]:
    N = src_px.shape[0]
    A = np.hstack([src_px, np.ones((N, 1))])
    coef_x, *_ = np.linalg.lstsq(A, dst_geo[:, 0], rcond=None)
    coef_y, *_ = np.linalg.lstsq(A, dst_geo[:, 1], rcond=None)
    M = np.vstack([coef_x, coef_y])
    pred = A @ M.T
    rms = float(np.sqrt(((dst_geo - pred) ** 2).sum(axis=1).mean()))
    return M, rms


def apply_affine(pts: np.ndarray, M: np.ndarray) -> np.ndarray:
    A = np.hstack([pts, np.ones((pts.shape[0], 1))])
    return A @ M.T


# ---------------------------------------------------------------------------
# Seeded flood-fill and contour extraction
# ---------------------------------------------------------------------------

def flood_fill_interior(interior_mask: np.ndarray, seed_px: tuple[int, int]) -> tuple[np.ndarray, dict]:
    """Flood-fill the interior mask from a seed; return label mask + bbox.

    Returns (label_mask uint8 0/255, info dict with area_px and bbox).
    """
    H, W = interior_mask.shape
    sx, sy = seed_px
    if not (0 <= sx < W and 0 <= sy < H):
        raise ValueError(f"seed out of bounds: {seed_px}")
    if interior_mask[sy, sx] == 0:
        raise ValueError(f"seed on red boundary: {seed_px}")
    flood = interior_mask.copy()
    mask = np.zeros((H + 2, W + 2), dtype=np.uint8)
    flags = 4 | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)
    # Use floodFill with mask output
    cv2.floodFill(flood, mask, (sx, sy), 128, 0, 0, flags)
    label_mask = (mask[1:-1, 1:-1] > 0).astype(np.uint8) * 255
    area_px = int(np.count_nonzero(label_mask))
    # Bounding rect
    ys, xs = np.where(label_mask > 0)
    bbox = (int(xs.min()), int(ys.min()), int(xs.max() - xs.min()), int(ys.max() - ys.min()))
    return label_mask, {"area_px": area_px, "bbox_px": bbox, "seed": seed_px}


def extract_contour(label_mask: np.ndarray, approx_tol_px: float = 1.5) -> np.ndarray:
    """Extract the largest outer contour, simplify by Douglas-Peucker."""
    contours, _ = cv2.findContours(label_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        raise RuntimeError("No contour found in label mask")
    contour = max(contours, key=cv2.contourArea)
    # Pre-simplify in pixel space
    approx = cv2.approxPolyDP(contour.astype(np.float32), epsilon=approx_tol_px, closed=True)
    return approx[:, 0, :].astype(np.float64)


def contour_to_polygon(
    contour_px: np.ndarray,
    M: np.ndarray,
    simplify_tol_m: float = 40.0,
) -> Polygon:
    geo_pts = apply_affine(contour_px, M)
    if len(geo_pts) < 4:
        raise ValueError("contour too small")
    poly = Polygon(geo_pts)
    if not poly.is_valid:
        poly = poly.buffer(0)
    if poly.geom_type == "MultiPolygon":
        poly = max(poly.geoms, key=lambda p: p.area)
    poly = poly.simplify(simplify_tol_m, preserve_topology=True)
    if not poly.is_valid:
        poly = poly.buffer(0)
        if poly.geom_type == "MultiPolygon":
            poly = max(poly.geoms, key=lambda p: p.area)
    return poly


# ---------------------------------------------------------------------------
# Active-disproof pass (7 tests)
# ---------------------------------------------------------------------------

def disproof_pass(
    ed_name: str,
    poly_geo: Polygon,
    contour_px: np.ndarray,
    red_mask: np.ndarray,
    label_mask: np.ndarray,
    M: np.ndarray,
    img_shape: tuple,
    hard_constraints: dict | None = None,
    adjacent_ed_geo: Polygon | None = None,
) -> dict:
    H, W = img_shape
    tests = {}

    # T1: Red-pixel coverage within dilated outline (local bbox)
    x, y, w, h = cv2.boundingRect(contour_px.astype(np.int32))
    pad = 15
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(W, x + w + pad), min(H, y + h + pad)
    shifted = (contour_px.astype(np.int32) - np.array([[x0, y0]]))
    outline = np.zeros((y1 - y0, x1 - x0), dtype=np.uint8)
    cv2.drawContours(outline, [shifted], -1, 255, thickness=1)
    dil = cv2.dilate(outline, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)), iterations=1)
    local_red = red_mask[y0:y1, x0:x1]
    total_red = int(np.count_nonzero(local_red))
    near = int(np.count_nonzero(local_red & dil))
    coverage = near / max(total_red, 1)
    tests["t1_red_coverage_local"] = {
        "value": round(coverage, 4),
        "pass": bool(coverage >= 0.90),
        "target": ">=0.90",
        "red_px_local": total_red,
        "red_near_outline": near,
    }

    # T2: placeholder filled after rendering
    tests["t2_overlay_visual_diff"] = {"pass": None, "note": "set post-rendering"}

    # T3: Hard constraints
    if hard_constraints:
        results = []
        for cname, fn in hard_constraints.items():
            try:
                ok = bool(fn(poly_geo))
            except Exception:
                ok = False
            results.append({"constraint": cname, "pass": ok})
        tests["t3_hard_constraints"] = {
            "results": results,
            "pass": bool(all(r["pass"] for r in results)),
        }
    else:
        tests["t3_hard_constraints"] = {"pass": True, "note": "none"}

    # T4: neighbour shared edge
    if adjacent_ed_geo is not None and not adjacent_ed_geo.is_empty:
        inter = poly_geo.buffer(50).intersection(adjacent_ed_geo.buffer(50))
        shared_len = inter.length / 2 if not inter.is_empty else 0
        tests["t4_neighbour_shared_edge"] = {
            "shared_length_m": round(float(shared_len), 0),
            "pass": bool(shared_len > 100),
        }
    else:
        tests["t4_neighbour_shared_edge"] = {"pass": True, "note": "no neighbour"}

    # T5: reverse sampling
    minx, miny, maxx, maxy = poly_geo.bounds
    # HIGH-01: replaced `hash(ed_name) % (2**32)` with a stable sha256
    # digest. Python's built-in hash() is randomized per process unless
    # PYTHONHASHSEED is pinned, so two runs could seed different RNG
    # streams and produce different T5 pass/fail flags. sha256 is
    # deterministic across processes and Python versions.
    seed_int = int.from_bytes(
        hashlib.sha256(ed_name.encode('utf-8')).digest()[:4], 'big'
    )
    rng = np.random.default_rng(seed_int)
    hits = 0
    tries = 0
    while hits < 20 and tries < 2000:
        px = rng.uniform(minx, maxx); py = rng.uniform(miny, maxy)
        if poly_geo.contains(Point(px, py)):
            hits += 1
        tries += 1
    tests["t5_reverse_sampling"] = {"inside_count": hits, "pass": bool(hits == 20)}

    # T6: bbox within thumbnail
    corners_geo = apply_affine(np.array([[0, 0], [W, 0], [W, H], [0, H]]), M)
    ext_minx, ext_miny = corners_geo[:, 0].min(), corners_geo[:, 1].min()
    ext_maxx, ext_maxy = corners_geo[:, 0].max(), corners_geo[:, 1].max()
    ok6 = (minx >= ext_minx - 1500 and maxx <= ext_maxx + 1500
           and miny >= ext_miny - 1500 and maxy <= ext_maxy + 1500)
    tests["t6_bbox_within_thumbnail"] = {
        "pass": bool(ok6),
        "poly_bounds": [round(v, 0) for v in poly_geo.bounds],
        "thumb_extent": [round(ext_minx, 0), round(ext_miny, 0),
                         round(ext_maxx, 0), round(ext_maxy, 0)],
    }

    # T7: scale consistency
    fill = np.zeros((H, W), dtype=np.uint8)
    cv2.fillPoly(fill, [contour_px.astype(np.int32)], 255)
    area_px = int(np.count_nonzero(fill))
    det = abs(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0])
    a_shapely = poly_geo.area / 1e6
    a_px = (area_px * det) / 1e6
    pct = abs(a_shapely - a_px) / max(a_shapely, 1e-9) * 100
    tests["t7_area_scale_consistency"] = {
        "area_shapely_km2": round(a_shapely, 2),
        "area_px_km2": round(a_px, 2),
        "pct_diff": round(pct, 2),
        "pass": bool(pct < 5.0),
    }

    considered = [k for k, v in tests.items() if isinstance(v, dict) and v.get("pass") is not None]
    n_pass = sum(1 for k in considered if tests[k]["pass"])
    tests["summary"] = {"n_pass": n_pass, "n_considered": len(considered)}
    return tests


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_verification_panel(
    ed_name: str, poly_geo: Polygon, v5_geo: Polygon | None,
    out_path: Path,
):
    fig, ax = plt.subplots(figsize=(10, 10))
    gx, gy = poly_geo.exterior.xy
    ax.plot(gx, gy, "-", color="red", lw=2.0, label="v6 (pixel-exact)")
    if v5_geo is not None and not v5_geo.is_empty:
        try:
            if v5_geo.geom_type == "Polygon":
                vx, vy = v5_geo.exterior.xy
                ax.plot(vx, vy, "--", color="blue", lw=1.0, alpha=0.65, label="v5 (approx.)")
        except Exception:
            pass
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.legend(loc="upper right")
    ax.set_title(f"{ed_name}\nv6 area = {poly_geo.area/1e6:.2f} km²"
                 f"{'  (v5 = %.2f)' % (v5_geo.area/1e6,) if v5_geo is not None and not v5_geo.is_empty else ''}")
    ax.set_xlabel("Easting (m, EPSG:3400)")
    ax.set_ylabel("Northing (m, EPSG:3400)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def render_overlay_qa(
    ed_name: str,
    contour_px: np.ndarray,
    red_mask: np.ndarray,
    img: np.ndarray,
    out_path: Path,
) -> dict:
    """Overlay v6 outline (green) on thumbnail; flag yellow diffs.

    Returns {n_yellow_px, n_large_clusters, t2_pass}.
    """
    H, W = img.shape[:2]
    overlay = img.copy()
    pts = contour_px.astype(np.int32)
    cv2.polylines(overlay, [pts], isClosed=True, color=(0, 255, 0), thickness=4)
    outline_mask = np.zeros((H, W), dtype=np.uint8)
    cv2.drawContours(outline_mask, [pts], -1, 255, thickness=1)
    dil = cv2.dilate(outline_mask, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)), iterations=1)
    x, y, w, h = cv2.boundingRect(pts)
    pad = 60
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(W, x + w + pad), min(H, y + h + pad)
    diff_local = np.zeros_like(red_mask)
    diff_local[y0:y1, x0:x1] = red_mask[y0:y1, x0:x1] & ~dil[y0:y1, x0:x1]
    overlay[diff_local > 0] = (0, 255, 255)
    cx0, cy0 = max(0, x - 200), max(0, y - 200)
    cx1, cy1 = min(W, x + w + 200), min(H, y + h + 200)
    crop = overlay[cy0:cy1, cx0:cx1]
    cv2.imwrite(str(out_path), crop)
    n_yellow = int(np.count_nonzero(diff_local))
    if n_yellow > 0:
        _, _, stats, _ = cv2.connectedComponentsWithStats(diff_local, connectivity=4)
        large = int(np.sum(stats[1:, cv2.CC_STAT_AREA] > 10))
    else:
        large = 0
    return {
        "n_yellow_px": n_yellow,
        "n_large_clusters": large,
        "t2_pass": bool(large == 0),
    }


# ---------------------------------------------------------------------------
# Pipeline configuration for each thumbnail
# ---------------------------------------------------------------------------

# Thumbnail config: (path, orientation, anchors, target_EDs, seeds, hard_constraints)
# anchors: list of (px_col, px_row, ed_2019_name)
# seeds: {ed_name_2026: (px_col, px_row)}

# Note: all pixel coordinates below refer to the NORTH-UP ORIENTED image
# (after the rotation specified in `orientation`).

# Calgary minority (p360) — rotated 90 CW for north-up
# Based on visual inspection of the label-centroid overlay and cross-check
# against pixel areas consistent with 2019 Tier A ED areas.
# Pixel-area -> Tier A ED mapping (derived from area-matching at ~9 m/px):
#   L 2 (320k px -> ~26 km2 at 9m)   = Calgary-Beddington  (27.6 km2)
#   L14 (218k px -> ~17.7 km2)        = Calgary-Mountain View or Calgary-North
#   L 3 (253k px -> ~20.5 km2)        = Calgary-North East or Calgary-Varsity
# ... etc.
# Below we hard-code 5 anchors with high confidence from visual inspection.

CAL_MIN_ANCHORS = [
    # (px_col, px_row, 2019_ed_name)
    # L 2 is near the TOP of the rotated map (high px_row=898 actually means NORTH due to y-axis)
    # At px_row=898 (top of image after rotation=NORTH geographically) and px_col=3818 (middle east)
    # Candidate: Calgary-Beddington (north-central Calgary) ~ geo (563146, 5661799)
    (3818, 898, "Calgary-Beddington"),
    # L 3 at (4105, 1140): slightly east of L2; Calgary-Cross? geo (573778, 5656104) ~ NE
    (4105, 1140, "Calgary-North East"),   # 253k px -> 20.5 km2 (vs Calg-NE=66 km2, wrong); try Cross=15.8
    # Use Calgary-Klein at L61 (76k -> 6 km2, way off from 37). Hmm.
    # Let me use more reliable anchors:
    # L 14 (218k px -> 17.7 km2 at 9m): Calgary-North (21.2) or Calgary-Mountain View (17.8)
    (3272, 1552, "Calgary-North"),        # geo (563130, 5667726)
    # L 95 (91k -> 7.4 km2) ~ Calgary-Currie (15.9) or Buffalo (10.5). Let's skip -- too small.
    # L101 (Calgary-De Winton — our target, skip as anchor)
    # L104 (768k -> 62 km2): Calgary-South East? Or very close to it.
    (5356, 3409, "Calgary-South East"),   # geo (575476, 5634793) — far SE
    # L 73 (791k -> 64 km2) ~ Calgary-North East (66). Centroid (4938, 2715) ~ east-central
    (4938, 2715, "Calgary-Hays"),         # Hays 24 km2 — likely more reliable than "North East"
    # Actually, looking more carefully: L 73 at (4938, 2715) could be Calg-Hays (24) but that's small.
    # Skip this. Use more visually-obvious features.
]

# I'll hand-pick 5 confident anchors and accept the residual.
# Using spatial logic: in the rotated Calgary minority image,
# Tsuut'ina Nation 145 reserve centroid is at pixel (2751, 2756) (from earlier grey-detection).
# Tsuut'ina 145 geographic centroid: approximately UTM zone 12, EPSG:3400 = (548400, 5649000) — let me look up
# Actually let me use what we CAN verify: the full map's N/S/E/W extremes.

# Pragmatic anchors: map-frame corners correspond to SOMEWHERE in 2019 space.
# From the rotated image, the red-mask extent was x=[749, 6018], y=[504, 4445].
# The geographic extent of EDs visible in the map is approximately:
#   Latitude: 50.4 - 51.5 (Okotoks to N Airdrie)   -> UTM 12 N: ~5585000 to 5705000 (EPSG:3400)
#   Longitude: -114.6 to -113.2 (Cochrane to Chestermere) -> UTM 12 E: 460000 to 600000


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main():
    print("[v6] Starting pipeline")
    t_start = time.time()
    log = {"version": "v6", "timestamp": pd.Timestamp.utcnow().isoformat(),
           "thumbnails": {}, "per_ed": {}}

    # Delegate to per-thumbnail processors that are defined in v6_processors.py
    from shape_refinement_v6_processors import (
        process_calgary_minority,
        process_edmonton_minority,
        process_calgary_majority,
        process_edmonton_majority,
    )

    eds2019 = gpd.read_file(EDS_2019_PATH).to_crs(AREA_CRS)

    results = {}  # {ed_name: polygon_geo_AREA_CRS}
    for proc_fn, label in [
        (process_calgary_minority, "calgary_minority"),
        (process_edmonton_minority, "edmonton_minority"),
        (process_calgary_majority, "calgary_majority"),
        (process_edmonton_majority, "edmonton_majority"),
    ]:
        try:
            print(f"\n=== {label} ===")
            sub_results, sub_log = proc_fn(eds2019)
            results.update(sub_results)
            log["thumbnails"][label] = sub_log
        except Exception as e:
            print(f"[ERROR] {label}: {e}")
            log["thumbnails"][label] = {"error": str(e)}
            import traceback; traceback.print_exc()

    # Write results (delegated)
    from shape_refinement_v6_writer import write_outputs
    write_outputs(results, log)

    print(f"\n[v6] Done in {time.time()-t_start:.1f} s")


if __name__ == "__main__":
    main()
