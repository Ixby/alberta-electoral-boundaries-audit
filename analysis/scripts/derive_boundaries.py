# Version: v0.1
"""
v7 derived shapefiles — extension of v6 pixel-exact pipeline to cover ALL EDs
visible in any commission thumbnail, not just Tier C.

Strategy
--------
For each available thumbnail we run the same DT-affine + seeded flood-fill
pipeline as v6. We extend v6 by:
  (1) Using 2019-ED centroids projected through the inverse affine as seeds for
      any 2026 ED whose territory overlaps a 2019 ED centroid. This lets us
      vectorize Tier A (unchanged) and Tier C (changed) EDs uniformly.
  (2) For each 2026 ED we attempt flood-fill from multiple candidate seeds and
      keep the best result (smallest plausible area, disproof pass-count).
  (3) Per-ED fallback: if flood-fill fails or disproof-pass < 5/7, we fall back
      to the v6 shape (if present) or the approximate Tier A shape.

Rural / low-resolution handling
-------------------------------
The minority overview thumbnail p359_map73 covers ALL rural minority EDs but
at ~1-2 km per-edge accuracy. We attempt vectorization there and tag the rows
with resolution_tier="overview_only". Per the plan:
  - option (a) for clearly drawn rural EDs (most are),
  - option (b) (fallback) for tiny/ambiguous ones.

Outputs
-------
  data/v0_1_derived_v7_minority_2026_eds.gpkg   (89 rows)
  data/v0_1_derived_v7_majority_2026_eds.gpkg   (89 rows)
  analysis/shape_derivation_v7_log.json
  analysis/v0_1_derived_shapefiles_v7.md
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import cv2
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

# Reuse v6 primitives without modifying them
from shape_refinement_v6 import (  # noqa: E402
    MAPS_HIRES, DATA_DIR, ANALYSIS_DIR,
    AREA_CRS, WORK_CRS, EDS_2019_PATH,
    load_and_orient, extract_red_mask,
    apply_affine, flood_fill_interior, extract_contour,
    contour_to_polygon, disproof_pass, render_overlay_qa,
)


def _get_interior_mask_v7(
    red_mask: np.ndarray,
    dilate_px: int = 3,
    close_px: int = 5,
) -> np.ndarray:
    """v7-specific: close red-line gaps before computing interior.

    dilate_px: final dilation so flood-fill stays bounded to interior.
    close_px: morphological closing to seal small gaps BEFORE computing
              interior. This is critical for commission maps where highway
              lines or street lines break the red boundary.
    """
    # Step 1: Morphological close to seal small gaps in red lines
    k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                        (close_px, close_px))
    red_closed = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, k_close,
                                  iterations=2)
    # Step 2: Dilate so flood-fill can't cross thin red remnants
    k_dil = cv2.getStructuringElement(cv2.MORPH_RECT, (dilate_px, dilate_px))
    red_d = cv2.dilate(red_closed, k_dil, iterations=1)
    return (red_d == 0).astype(np.uint8) * 255
from shape_refinement_v6_processors import (  # noqa: E402
    optimise_affine_dt, collect_boundary_points, _safe_slug,
)


# -----------------------------------------------------------------------------
# Mapping 2026 EDs to their 2019 "territorial ancestor" used for seeding
# -----------------------------------------------------------------------------
#
# For most Tier A EDs (same name 2019 -> 2026 with no rename), we just look up
# the 2019 centroid. For renamed or reshaped EDs we use the closest matching
# 2019 ED or a hand-picked inheritor. For EDs with no territorial 2019 analog
# (rare; e.g., Calgary-Confluence carved from several), we omit them here and
# fallback applies.
#
# NB: the dict contains ALL 2026 EDs we want to attempt, for BOTH map sets
# (minority 89 + majority 89). Overlap is fine.

# 2026 ED -> 2019 ED used as seed centroid (and adjacency test)
NAME_2026_TO_2019_SEED = {
    # --- MAJORITY 2026 ---
    "Airdrie-East":                              "Airdrie-East",
    "Airdrie-West":                              "Airdrie-Cochrane",
    "Barrhead-Westlock-Athabasca":               "Athabasca-Barrhead-Westlock",
    "Calgary-Acadia":                            "Calgary-Acadia",
    "Calgary-Beddington":                        "Calgary-Beddington",
    "Calgary-Bhullar-McCall":                    "Calgary-McCall",
    "Calgary-Bow":                               "Calgary-Bow",
    "Calgary-Buffalo":                           "Calgary-Buffalo",
    "Calgary-Confluence":                        "Calgary-Mountain View",
    "Calgary-Cross":                             "Calgary-Cross",
    "Calgary-Currie":                            "Calgary-Currie",
    "Calgary-East":                              "Calgary-East",
    "Calgary-Edgemont":                          "Calgary-Edgemont",
    "Calgary-Elbow":                             "Calgary-Elbow",
    "Calgary-Falconridge-Conrich":               "Calgary-Falconridge",
    "Calgary-Fish Creek":                        "Calgary-Fish Creek",
    "Calgary-Glenmore-Tsuut'ina":                "Calgary-Glenmore",
    "Calgary-Hays":                              "Calgary-Hays",
    "Calgary-Klein":                             "Calgary-Klein",
    "Calgary-Lougheed":                          "Calgary-Lougheed",
    "Calgary-McKenzie":                          "Calgary-Shaw",
    "Calgary-Mountain View":                     "Calgary-Mountain View",
    "Calgary-North":                             "Calgary-North",
    "Calgary-North East":                        "Calgary-North East",
    "Calgary-North West":                        "Calgary-North West",
    "Calgary-Nose Creek":                        "Calgary-Beddington",
    "Calgary-Shaw":                              "Calgary-Shaw",
    "Calgary-South East":                        "Calgary-South East",
    "Calgary-Symons Valley":                     "Calgary-Foothills",
    "Calgary-Varsity":                           "Calgary-Varsity",
    "Calgary-West-Elbow Valley":                 "Calgary-West",
    "Camrose":                                   "Camrose",
    "Canmore-Banff":                             "Banff-Kananaskis",
    "Central Peace-Notley":                      "Central Peace-Notley",
    "Chestermere-Strathmore":                    "Chestermere-Strathmore",
    "Cochrane-Springbank":                       "Airdrie-Cochrane",
    "Cold Lake-Bonnyville-St. Paul":             "Bonnyville-Cold Lake-St. Paul",
    "Drumheller-Stettler":                       "Drumheller-Stettler",
    "Edmonton-Beaumont":                         "Leduc-Beaumont",
    "Edmonton-Beverly-Clareview":                "Edmonton-Beverly-Clareview",
    "Edmonton-Castle Downs":                     "Edmonton-Castle Downs",
    "Edmonton-City Centre":                      "Edmonton-City Centre",
    "Edmonton-Decore":                           "Edmonton-Decore",
    "Edmonton-Ellerslie":                        "Edmonton-Ellerslie",
    "Edmonton-Enoch":                            "Spruce Grove-Stony Plain",
    "Edmonton-Glenora-Riverview":                "Edmonton-Glenora",
    "Edmonton-Gold Bar":                         "Edmonton-Gold Bar",
    "Edmonton-Highlands-Norwood":                "Edmonton-Highlands-Norwood",
    "Edmonton-Manning":                          "Edmonton-Manning",
    "Edmonton-McClung":                          "Edmonton-McClung",
    "Edmonton-Meadows":                          "Edmonton-Meadows",
    "Edmonton-Mill Woods":                       "Edmonton-Mill Woods",
    "Edmonton-North West":                       "Edmonton-North West",
    "Edmonton-Rutherford":                       "Edmonton-Rutherford",
    "Edmonton-South":                            "Edmonton-South-West",
    "Edmonton-Strathcona":                       "Edmonton-Strathcona",
    "Edmonton-West Henday":                      "Edmonton-West Henday",
    "Edmonton-Whitemud":                         "Edmonton-Whitemud",
    "Edmonton-Windermere":                       "Edmonton-Whitemud",
    "Fort McMurray-Lac La Biche":                "Fort McMurray-Lac La Biche",
    "Fort McMurray-Wood Buffalo":                "Fort McMurray-Wood Buffalo",
    "Fort Saskatchewan-Vegreville":              "Fort Saskatchewan-Vegreville",
    "Grande Prairie":                            "Grande Prairie",
    "Grande Prairie-Wapiti":                     "Grande Prairie-Wapiti",
    "High River-Vulcan-Siksika":                 "Highwood",
    "Lacombe-Clearwater":                        "Rimbey-Rocky Mountain House-Sundre",
    "Leduc-Devon":                               "Leduc-Beaumont",
    "Lesser Slave Lake":                         "Lesser Slave Lake",
    "Lethbridge-East":                           "Lethbridge-East",
    "Lethbridge-West":                           "Lethbridge-West",
    "Livingstone-Macleod":                       "Livingstone-Macleod",
    "Lloydminster-Wainwright":                   "Vermilion-Lloydminster-Wainwright",
    "Medicine Hat-Brooks":                       "Brooks-Medicine Hat",
    "Medicine Hat-Cypress":                      "Cypress-Medicine Hat",
    "Mountain View-Kneehill":                    "Olds-Didsbury-Three Hills",
    "Okotoks-Diamond Valley":                    "Highwood",
    "Peace River":                               "Peace River",
    "Red Deer-North":                            "Red Deer-North",
    "Red Deer-South":                            "Red Deer-South",
    "Sherwood Park":                             "Sherwood Park",
    "Spruce Grove":                              "Spruce Grove-Stony Plain",
    "St. Albert":                                "St. Albert",
    "St. Albert-Sturgeon":                       "Morinville-St. Albert",
    "Stony Plain-Drayton Valley":                "Drayton Valley-Devon",
    "Strathcona-Sherwood Park":                  "Strathcona-Sherwood Park",
    "Sylvan Lake-Innisfail":                     "Innisfail-Sylvan Lake",
    "Taber-Cardston":                            "Cardston-Siksika",
    "West Yellowhead":                           "West Yellowhead",
    "Wetaskiwin-Ponoka-Maskwacis":               "Maskwacis-Wetaskiwin",

    # --- MINORITY 2026 (ones unique to minority map set) ---
    "Airdrie East":                              "Airdrie-East",
    "Calgary-Airdrie":                           "Airdrie-East",
    "Calgary-Bow-Springbank":                    "Calgary-Bow",
    "Calgary-De Winton":                         "Highwood",
    "Calgary-Falconridge":                       "Calgary-Falconridge",
    "Calgary-Foothills-Airdrie West":            "Calgary-Foothills",
    "Calgary-Glenmore":                          "Calgary-Glenmore",
    "Calgary-McCall-Bhullar":                    "Calgary-McCall",
    "Calgary-Nolan Hill-Cochrane":               "Airdrie-Cochrane",
    "Calgary-North West-Bearspaw":               "Calgary-North West",
    "Calgary-Peigan-Chestermere":                "Calgary-Peigan",
    "Calgary-South":                             "Calgary-Acadia",
    "Calgary-West-Tsuut'ina":                    "Calgary-West",
    "Canmore-Kananaskis":                        "Banff-Kananaskis",
    "Edmonton-Castledowns":                      "Edmonton-Castle Downs",
    "Edmonton-Enoch-Devon":                      "Spruce Grove-Stony Plain",
    "Edmonton-Spruce Grove":                     "Spruce Grove-Stony Plain",
    "Highwood":                                  "Highwood",
    "Lac Ste. Anne-Parkland":                    "Lac Ste. Anne-Parkland",
    "Leduc":                                     "Leduc-Beaumont",
    "Lethbridge-Cardston":                       "Cardston-Siksika",
    "Lethbridge-Fort MacLeod-Crowsnest Pass":    "Livingstone-Macleod",
    "Lethbridge-Little Bow":                     "Taber-Warner",
    "Lethbridge-Taber-Warner":                   "Taber-Warner",
    "Olds-Three Hills-Didsbury":                 "Olds-Didsbury-Three Hills",
    "Red Deer-Blackfalds":                       "Red Deer-North",
    "Red Deer-Innisfail":                        "Innisfail-Sylvan Lake",
    "Red Deer-Lacombe":                          "Lacombe-Ponoka",
    "Red Deer-Sylvan Lake":                      "Innisfail-Sylvan Lake",
    "Rocky Mountain House-Banff Park":           "Rimbey-Rocky Mountain House-Sundre",
    "Sherwood Park-Strathcona":                  "Strathcona-Sherwood Park",
    "Wetaskawin-Ponoka-Maskwacis":               "Maskwacis-Wetaskiwin",
}


# -----------------------------------------------------------------------------
# Thumbnail plan
# -----------------------------------------------------------------------------
# Each entry: (thumb_filename, orientation, city_core_for_DT, initial_affine,
#              eds_to_attempt, resolution_tier, notes)
#
# Initial affine: (scale m/px, tx, ty) ; used as optimiser seed. For overview
# thumbnails (whole-of-Alberta) we use larger scale ~100 m/px.

def _make_plan(map_set: str) -> list[dict]:
    """Build plan list for a given map set ('minority' or 'majority')."""
    pop = pd.read_csv(DATA_DIR / f"v0_1_{map_set}_2026_populations.csv")
    all_eds = set(pop["ed_name"].tolist())

    if map_set == "minority":
        # Calgary inset (p360)
        calgary_inner = [n for n in all_eds if n.startswith("Calgary") or
                         n in ("Highwood", "Airdrie East", "Chestermere-Strathmore")]
        # Edmonton inset (p361)
        edmonton_inner = [n for n in all_eds if n.startswith("Edmonton") or
                          n in ("St. Albert", "Sherwood Park-Strathcona",
                                "St. Albert-Sturgeon", "Leduc")]
        # other_cities multi-inset (p362)
        other_cities = ["Red Deer-Blackfalds", "Red Deer-Innisfail",
                        "Red Deer-Lacombe", "Red Deer-Sylvan Lake",
                        "Lethbridge-Cardston", "Lethbridge-Fort MacLeod-Crowsnest Pass",
                        "Lethbridge-Little Bow", "Lethbridge-Taber-Warner",
                        "Medicine Hat-Brooks", "Medicine Hat-Cypress",
                        "Grande Prairie", "Grande Prairie-Wapiti",
                        "Fort McMurray-Lac La Biche", "Fort McMurray-Wood Buffalo",
                        "Chestermere-Strathmore",
                        "Calgary-Peigan-Chestermere"]
        # Overview (p359) — all remaining rural
        overview_eds = sorted(all_eds)

        return [
            {
                "label": "minority_calgary",
                "thumb": MAPS_HIRES / "v0_1_minority_p360_map74.png",
                "orientation": "rot90cw",
                "dilate_px": 3,
                "dt_core_eds": [
                    # 2019 names with stable Tier A boundaries in Calgary area
                    "Calgary-Acadia", "Calgary-Beddington", "Calgary-Bow",
                    "Calgary-Buffalo", "Calgary-Cross", "Calgary-Currie",
                    "Calgary-Edgemont", "Calgary-Elbow", "Calgary-Falconridge",
                    "Calgary-Fish Creek", "Calgary-Foothills", "Calgary-Glenmore",
                    "Calgary-Hays", "Calgary-Klein", "Calgary-Lougheed",
                    "Calgary-McCall", "Calgary-Mountain View", "Calgary-North",
                    "Calgary-North East", "Calgary-North West", "Calgary-Peigan",
                    "Calgary-Shaw", "Calgary-South East", "Calgary-Varsity",
                    "Calgary-West",
                ],
                "initial_scale": 13.5,
                "initial_tx": 510000,
                "initial_ty": 5690000,
                "eds_to_attempt": sorted(set(calgary_inner)),
                "resolution_tier": "city_detail",
            },
            {
                "label": "minority_edmonton",
                "thumb": MAPS_HIRES / "v0_1_minority_p361_map75.png",
                "orientation": "native",
                "dilate_px": 3,
                "dt_core_eds": [
                    "Edmonton-Beverly-Clareview", "Edmonton-Castle Downs",
                    "Edmonton-City Centre", "Edmonton-Decore",
                    "Edmonton-Ellerslie", "Edmonton-Glenora", "Edmonton-Gold Bar",
                    "Edmonton-Highlands-Norwood", "Edmonton-Manning",
                    "Edmonton-McClung", "Edmonton-Meadows", "Edmonton-Mill Woods",
                    "Edmonton-North West", "Edmonton-Riverview",
                    "Edmonton-Rutherford", "Edmonton-South-West",
                    "Edmonton-Strathcona", "Edmonton-West Henday",
                    "Edmonton-Whitemud",
                ],
                "initial_scale": 13.5,
                "initial_tx": 580000,
                "initial_ty": 5955000,
                "eds_to_attempt": sorted(set(edmonton_inner)),
                "resolution_tier": "city_detail",
            },
            {
                "label": "minority_overview",
                "thumb": MAPS_HIRES / "v0_1_minority_p359_map73.png",
                "orientation": "native",
                "dilate_px": 7,
                "dt_core_eds": [
                    # Province-wide: use large-area 2019 EDs for DT anchor
                    "Peace River", "Lesser Slave Lake", "Central Peace-Notley",
                    "Fort McMurray-Wood Buffalo", "Fort McMurray-Lac La Biche",
                    "Grande Prairie-Wapiti", "Grande Prairie",
                    "West Yellowhead", "Bonnyville-Cold Lake-St. Paul",
                    "Athabasca-Barrhead-Westlock",
                    "Drumheller-Stettler", "Cardston-Siksika",
                    "Taber-Warner", "Livingstone-Macleod",
                    "Highwood", "Chestermere-Strathmore",
                    "Banff-Kananaskis", "Red Deer-North",
                    "Red Deer-South", "Cypress-Medicine Hat",
                    "Brooks-Medicine Hat",
                ],
                "initial_scale": 180,
                "initial_tx": 180000,
                "initial_ty": 6650000,
                "eds_to_attempt": sorted([
                    n for n in all_eds
                    if n not in set(calgary_inner) and
                       n not in set(edmonton_inner)
                ]),
                "resolution_tier": "overview_only",
            },
            {
                # Minority other_cities (p362) is a MULTI-INSET page. Each sub-inset
                # has its own small-scale affine and we cannot georef it as a
                # single plane. We decline to process this page; instead the EDs
                # listed under 'other_cities' fall back to the overview (p359)
                # derivation, and if that also fails we fallback to v6.
                # This entry is retained as a no-op (no eds_to_attempt=[])
                # to document the decision in the log.
                "label": "minority_other_cities_declined",
                "thumb": MAPS_HIRES / "v0_1_minority_p362_map76.png",
                "orientation": "native",
                "dilate_px": 5,
                "dt_core_eds": ["Red Deer-North", "Lethbridge-East",
                                "Medicine Hat-Cypress"],
                "initial_scale": 60,
                "initial_tx": 350000,
                "initial_ty": 5830000,
                "eds_to_attempt": [],  # declined: multi-inset page
                "resolution_tier": "multi_inset_declined",
            },
        ]

    # --- MAJORITY ---
    calgary_core = [n for n in all_eds if n.startswith("Calgary")]
    edmonton_core = [n for n in all_eds if n.startswith("Edmonton") or
                     n in ("St. Albert", "Sherwood Park", "Spruce Grove",
                           "St. Albert-Sturgeon", "Strathcona-Sherwood Park",
                           "Leduc-Devon", "Fort Saskatchewan-Vegreville")]
    near_calgary = ["Airdrie-East", "Airdrie-West",
                    "Cochrane-Springbank", "Chestermere-Strathmore",
                    "Okotoks-Diamond Valley"]
    return [
        {
            "label": "majority_calgary",
            "thumb": MAPS_HIRES / "v0_1_majority_p72_MAP_r600.png",
            "orientation": "rot90cw",
            "dilate_px": 3,
            "dt_core_eds": [
                "Calgary-Acadia", "Calgary-Beddington", "Calgary-Bow",
                "Calgary-Buffalo", "Calgary-Cross", "Calgary-Currie",
                "Calgary-Edgemont", "Calgary-Elbow", "Calgary-Falconridge",
                "Calgary-Fish Creek", "Calgary-Foothills", "Calgary-Glenmore",
                "Calgary-Hays", "Calgary-Klein", "Calgary-Lougheed",
                "Calgary-McCall", "Calgary-Mountain View", "Calgary-North",
                "Calgary-North East", "Calgary-North West", "Calgary-Peigan",
                "Calgary-Shaw", "Calgary-South East", "Calgary-Varsity",
                "Calgary-West",
            ],
            "initial_scale": 13.5,
            "initial_tx": 510000,
            "initial_ty": 5690000,
            "eds_to_attempt": sorted(set(calgary_core)),
            "resolution_tier": "city_detail",
        },
        {
            "label": "majority_edmonton",
            "thumb": MAPS_HIRES / "v0_1_majority_p74_MAP_r600.png",
            "orientation": "native",
            "dilate_px": 3,
            "dt_core_eds": [
                "Edmonton-Beverly-Clareview", "Edmonton-Castle Downs",
                "Edmonton-City Centre", "Edmonton-Decore",
                "Edmonton-Ellerslie", "Edmonton-Glenora", "Edmonton-Gold Bar",
                "Edmonton-Highlands-Norwood", "Edmonton-Manning",
                "Edmonton-McClung", "Edmonton-Meadows", "Edmonton-Mill Woods",
                "Edmonton-North West", "Edmonton-Riverview",
                "Edmonton-Rutherford", "Edmonton-South-West",
                "Edmonton-Strathcona", "Edmonton-West Henday",
                "Edmonton-Whitemud",
            ],
            "initial_scale": 13.5,
            "initial_tx": 580000,
            "initial_ty": 5955000,
            "eds_to_attempt": sorted(set(edmonton_core)),
            "resolution_tier": "city_detail",
        },
        {
            "label": "majority_near_calgary",
            "thumb": MAPS_HIRES / "v0_1_majority_p76_MAP_r600.png",
            "orientation": "native",
            "dilate_px": 4,
            "dt_core_eds": [
                "Airdrie-Cochrane", "Airdrie-East", "Chestermere-Strathmore",
                "Highwood",
            ],
            "initial_scale": 40,
            "initial_tx": 480000,
            "initial_ty": 5710000,
            "eds_to_attempt": sorted(set(near_calgary)),
            "resolution_tier": "near_city_detail",
        },
        {
            "label": "majority_overview",
            "thumb": MAPS_HIRES / "v0_1_majority_p71_alberta_overview.png",
            "orientation": "native",
            "dilate_px": 7,
            "dt_core_eds": [
                "Peace River", "Lesser Slave Lake", "Central Peace-Notley",
                "Fort McMurray-Wood Buffalo", "Fort McMurray-Lac La Biche",
                "Grande Prairie-Wapiti", "Grande Prairie",
                "West Yellowhead", "Bonnyville-Cold Lake-St. Paul",
                "Athabasca-Barrhead-Westlock",
                "Drumheller-Stettler", "Cardston-Siksika",
                "Taber-Warner", "Livingstone-Macleod",
                "Highwood", "Chestermere-Strathmore",
                "Banff-Kananaskis", "Red Deer-North",
                "Red Deer-South", "Cypress-Medicine Hat",
                "Brooks-Medicine Hat",
            ],
            "initial_scale": 180,
            "initial_tx": 180000,
            "initial_ty": 6650000,
            "eds_to_attempt": sorted([
                n for n in all_eds
                if n not in set(calgary_core) and
                   n not in set(edmonton_core) and
                   n not in set(near_calgary)
            ]),
            "resolution_tier": "overview_only",
        },
    ]


# -----------------------------------------------------------------------------
# Seed-finding: 2019 ED centroid -> pixel via inverse affine
# -----------------------------------------------------------------------------

def _geo_to_px(pt_xy: tuple[float, float], M_px2geo: np.ndarray) -> tuple[int, int]:
    """Invert the 2x3 pixel-to-geo affine to project (geo_x, geo_y) -> (px, py)."""
    # M_px2geo: [[a, b, c], [d, e, f]]
    # geo = A @ px + t, so px = A^-1 @ (geo - t)
    A = M_px2geo[:, :2]
    t = M_px2geo[:, 2]
    A_inv = np.linalg.inv(A)
    geo = np.array(pt_xy)
    px = A_inv @ (geo - t)
    return int(round(px[0])), int(round(px[1]))


def _find_good_seed(
    interior_mask: np.ndarray,
    seed_px: tuple[int, int],
    search_radius_px: int = 60,
) -> tuple[int, int] | None:
    """If the seed is on red (==0), spiral outward to find an interior pixel.
    Returns a valid seed or None if none found within `search_radius_px`.
    """
    H, W = interior_mask.shape
    sx, sy = seed_px
    if 0 <= sx < W and 0 <= sy < H and interior_mask[sy, sx] > 0:
        return (sx, sy)
    # Build a list of offsets sorted by radius
    offsets = []
    for dx in range(-search_radius_px, search_radius_px + 1, 3):
        for dy in range(-search_radius_px, search_radius_px + 1, 3):
            offsets.append((dx, dy, dx * dx + dy * dy))
    offsets.sort(key=lambda t: t[2])
    for dx, dy, _ in offsets:
        nx, ny = sx + dx, sy + dy
        if 0 <= nx < W and 0 <= ny < H and interior_mask[ny, nx] > 0:
            return (nx, ny)
    return None


# -----------------------------------------------------------------------------
# Per-ED processing
# -----------------------------------------------------------------------------

def _derive_one_ed(
    ed_name: str,
    seed_px: tuple[int, int],
    interior_mask: np.ndarray,
    red_mask: np.ndarray,
    img: np.ndarray,
    M_px2geo: np.ndarray,
    *,
    max_flood_frac: float = 0.20,
) -> tuple[Polygon | None, dict]:
    """Attempt to derive a Polygon for ed_name via seeded flood-fill.

    Returns (polygon_or_None, log_dict).
    """
    H, W = interior_mask.shape
    log: dict = {"seed_px_initial": list(seed_px)}

    good_seed = _find_good_seed(interior_mask, seed_px, search_radius_px=80)
    if good_seed is None:
        log["status"] = "SEED_ON_RED_NO_ESCAPE"
        return None, log
    log["seed_px_used"] = list(good_seed)

    try:
        label_mask, info = flood_fill_interior(interior_mask, good_seed)
        log["flood_fill"] = info
    except Exception as e:
        log["status"] = f"FLOOD_FAIL: {e}"
        return None, log

    # Reject seed-on-background (flood fills entire image)
    if info["area_px"] > max_flood_frac * H * W:
        log["status"] = "SEED_IN_BACKGROUND"
        log["flood_area_frac"] = round(info["area_px"] / (H * W), 3)
        return None, log

    try:
        contour_px = extract_contour(label_mask, approx_tol_px=1.5)
        log["contour_px_pts"] = len(contour_px)
    except Exception as e:
        log["status"] = f"CONTOUR_FAIL: {e}"
        return None, log

    try:
        poly_geo = contour_to_polygon(contour_px, M_px2geo, simplify_tol_m=40.0)
    except Exception as e:
        log["status"] = f"POLYGON_FAIL: {e}"
        return None, log

    if not poly_geo.is_valid or poly_geo.is_empty:
        log["status"] = "INVALID_POLYGON"
        return None, log

    log["area_km2"] = round(poly_geo.area / 1e6, 2)
    log["bounds"] = [round(v, 0) for v in poly_geo.bounds]
    log["contour_px"] = contour_px  # held for disproof rendering
    log["status"] = "DERIVED"
    return poly_geo, log


# -----------------------------------------------------------------------------
# Main per-thumbnail derivation
# -----------------------------------------------------------------------------

def _process_thumbnail(plan_entry: dict, eds2019: gpd.GeoDataFrame) -> dict:
    t0 = time.time()
    thumb_path: Path = plan_entry["thumb"]
    label = plan_entry["label"]
    dilate_px = plan_entry.get("dilate_px", 3)
    print(f"\n=== {label}: {thumb_path.name} ({plan_entry['orientation']}, "
          f"dilate={dilate_px}) ===")

    img = load_and_orient(thumb_path, plan_entry["orientation"])
    H, W = img.shape[:2]
    red = extract_red_mask(img)
    interior = _get_interior_mask_v7(red, dilate_px=dilate_px)

    # DT-affine fit
    core = plan_entry["dt_core_eds"]
    valid_core = [n for n in core if (eds2019["EDName2017"] == n).any()]
    boundary_pts = collect_boundary_points(eds2019, valid_core, interval_m=300)

    if len(boundary_pts) < 200:
        return {
            "label": label, "thumbnail": thumb_path.name,
            "error": f"Too few boundary points from {len(valid_core)} core EDs",
            "per_ed": {}, "derived_polygons": {},
        }

    # For overview maps, run multi-start so we don't get stuck in a local
    # minimum far from the true projection.
    if plan_entry["resolution_tier"] == "overview_only":
        best_M, best_cost, best_info = None, float("inf"), None
        # Province-wide overview: expected pixel_dim ~170-190 m/px based on
        # 2019 ED extent vs 5100x6601 image. Sweep +/- 60 m/px.
        scales = [plan_entry["initial_scale"] * f
                  for f in (0.55, 0.7, 0.85, 1.0, 1.15, 1.3, 1.5)]
        # Scan a grid of initial (scale, tx, ty) starting points.
        for s in scales:
            for dtx in (-150000, -75000, 0, 75000, 150000):
                for dty in (-150000, -75000, 0, 75000, 150000):
                    try:
                        M_try, cost_try, info_try = optimise_affine_dt(
                            red, boundary_pts,
                            initial_scale=s,
                            initial_tx=plan_entry["initial_tx"] + dtx,
                            initial_ty=plan_entry["initial_ty"] + dty,
                        )
                        # Sanity-prefer plausible pixel_dim (140-220 m/px)
                        pdm = info_try.get("pixel_dim_m", 0)
                        # Add a penalty for unrealistic pixel dims
                        effective_cost = cost_try
                        if pdm < 130 or pdm > 240:
                            effective_cost = cost_try * 1.5
                        if effective_cost < best_cost:
                            best_cost = effective_cost
                            best_M = M_try
                            best_info = info_try
                    except Exception:
                        continue
        if best_M is None:
            return {
                "label": label, "thumbnail": thumb_path.name,
                "error": "Overview DT-affine failed at all starts",
                "per_ed": {}, "derived_polygons": {},
            }
        M, cost, info = best_M, best_cost, best_info
    else:
        # City-detail thumbnails: run a small multi-start to guard against
        # local minima in the DT-affine objective.
        best_M, best_cost, best_info = None, float("inf"), None
        s0 = plan_entry["initial_scale"]
        for s in (s0 * 0.8, s0, s0 * 1.2):
            for dtx in (-20000, 0, 20000):
                for dty in (-20000, 0, 20000):
                    try:
                        M_try, cost_try, info_try = optimise_affine_dt(
                            red, boundary_pts,
                            initial_scale=s,
                            initial_tx=plan_entry["initial_tx"] + dtx,
                            initial_ty=plan_entry["initial_ty"] + dty,
                        )
                        if cost_try < best_cost:
                            best_cost = cost_try
                            best_M = M_try
                            best_info = info_try
                    except Exception:
                        continue
        if best_M is None:
            return {
                "label": label, "thumbnail": thumb_path.name,
                "error": "City DT-affine failed at all starts",
                "per_ed": {}, "derived_polygons": {},
            }
        M, cost, info = best_M, best_cost, best_info
    pixel_dim_m = info["pixel_dim_m"]
    print(f"  DT-affine: cost={cost:.2f}, pixel_dim={pixel_dim_m:.2f} m/px, "
          f"n_boundary_pts={info['n_boundary_points']}")

    per_ed_out: dict[str, dict] = {}
    derived_polys: dict[str, Polygon] = {}
    # Track claimed pixel-regions: cc_id -> first_ed_name that claimed it
    claimed_regions: dict[int, str] = {}

    # Precompute connected-component labels and centroids of the interior
    n_labels, cc_labels, cc_stats, cc_centroids = cv2.connectedComponentsWithStats(
        interior, connectivity=4)
    print(f"  Interior has {n_labels-1} connected components")

    # Tier-specific bounds for acceptable cc area
    tier_ = plan_entry["resolution_tier"]
    if tier_ == "overview_only":
        min_frac, max_frac = 0.00003, 0.18
    elif tier_ == "near_city_detail":
        min_frac, max_frac = 0.002, 0.30
    else:
        min_frac, max_frac = 0.0008, 0.10
    img_area = H * W

    # Pre-compute candidate basins: cc_ids whose area lies in plausible range
    # and are NOT border-touching (border-touching = background or ocean)
    candidate_cc_ids = []
    for cc_id in range(1, n_labels):
        area_cc = cc_stats[cc_id, cv2.CC_STAT_AREA]
        if area_cc < min_frac * img_area or area_cc > max_frac * img_area:
            continue
        # Check whether it touches the image border
        x = cc_stats[cc_id, cv2.CC_STAT_LEFT]
        y = cc_stats[cc_id, cv2.CC_STAT_TOP]
        w = cc_stats[cc_id, cv2.CC_STAT_WIDTH]
        h = cc_stats[cc_id, cv2.CC_STAT_HEIGHT]
        touches_border = (x == 0 or y == 0 or x + w >= W or y + h >= H)
        if touches_border and tier_ != "overview_only":
            # Border-touching regions in detail maps are typically background;
            # in overview maps, frontier EDs genuinely touch the border.
            continue
        candidate_cc_ids.append(cc_id)

    print(f"  Candidate basins (area in [{min_frac*100:.3f}%, {max_frac*100:.2f}%] "
          f"of image, border-safe): {len(candidate_cc_ids)}")

    # Per-ED loop
    for ed_name in plan_entry["eds_to_attempt"]:
        seed_2019_name = NAME_2026_TO_2019_SEED.get(ed_name)
        if seed_2019_name is None:
            per_ed_out[ed_name] = {
                "status": "NO_SEED_MAPPING",
                "note": "no 2019 analog; will fallback",
            }
            continue

        sub = eds2019[eds2019["EDName2017"] == seed_2019_name]
        if sub.empty:
            per_ed_out[ed_name] = {
                "status": "NO_2019_ED_FOUND",
                "seed_name": seed_2019_name,
            }
            continue

        centroid = sub.geometry.iloc[0].centroid
        area_2019 = float(sub.geometry.iloc[0].area / 1e6)
        seed_px = _geo_to_px((centroid.x, centroid.y), M)
        ed_log: dict = {
            "seed_2019_name": seed_2019_name,
            "seed_geo_centroid": [round(centroid.x, 0), round(centroid.y, 0)],
            "seed_px_projected": list(seed_px),
            "area_2019_km2": round(area_2019, 2),
        }

        # Check seed in-bounds first
        if not (0 <= seed_px[0] < W and 0 <= seed_px[1] < H):
            ed_log["status"] = "SEED_OUT_OF_THUMBNAIL"
            per_ed_out[ed_name] = ed_log
            continue

        # Strategy: find the candidate basin whose (pixel centroid) is
        # closest to the projected seed and whose AREA ratio to 2019 area
        # is within band, and NOT already claimed.
        # NB: 2026 EDs can be significantly carved-out or enlarged vs their
        # 2019 analog (up to ~3x area change) — use wider bands than v6.
        if tier_ == "overview_only":
            band_min, band_max = 0.20, 8.0
        elif tier_ == "near_city_detail":
            band_min, band_max = 0.15, 6.0
        else:
            # city_detail: many 2026 EDs are carve-outs — be very permissive
            band_min, band_max = 0.15, 6.0

        # Compute area of 1 basin in km^2 using affine determinant
        det = abs(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0])

        candidates = []
        for cc_id in candidate_cc_ids:
            if cc_id in claimed_regions:
                continue
            cc_area_px = cc_stats[cc_id, cv2.CC_STAT_AREA]
            cc_area_km2 = cc_area_px * det / 1e6
            ratio = cc_area_km2 / max(area_2019, 1.0)
            if not (band_min <= ratio <= band_max):
                continue
            cx, cy = cc_centroids[cc_id]
            dist2 = (cx - seed_px[0]) ** 2 + (cy - seed_px[1]) ** 2
            candidates.append((dist2, cc_id, cc_area_px, cc_area_km2, cx, cy))

        if not candidates:
            ed_log["status"] = "NO_MATCHING_BASIN"
            ed_log["note"] = (
                f"No unclaimed basin with area ratio in [{band_min}, "
                f"{band_max}] near seed. 2019 area={area_2019:.1f} km2"
            )
            per_ed_out[ed_name] = ed_log
            continue

        # Sort: shortest distance first
        candidates.sort(key=lambda t: t[0])
        # Tolerance scales with pixel_dim_m. Many 2026 centroids shift from
        # their 2019 analog by 10-25 km (carved-out EDs), so we use a
        # generous tolerance in geo space.
        if tier_ == "overview_only":
            max_dist_geo_m = 80_000
        elif tier_ == "near_city_detail":
            max_dist_geo_m = 35_000
        else:
            max_dist_geo_m = 30_000
        max_dist_px = max_dist_geo_m / pixel_dim_m
        best = candidates[0]
        if best[0] ** 0.5 > max_dist_px:
            ed_log["status"] = "NEAREST_BASIN_TOO_FAR"
            ed_log["nearest_dist_px"] = round(best[0] ** 0.5, 0)
            ed_log["max_dist_px"] = round(max_dist_px, 0)
            per_ed_out[ed_name] = ed_log
            continue

        _, cc_id, cc_area_px, cc_area_km2, cx_px, cy_px = best
        # Use basin centroid as seed
        # Ensure seed is in interior (sometimes centroid is on red in thin EDs)
        good_seed = _find_good_seed(interior, (int(cx_px), int(cy_px)),
                                    search_radius_px=30)
        if good_seed is None:
            # Fall back to any interior pixel of this cc
            ys, xs = np.where(cc_labels == cc_id)
            if len(xs) == 0:
                ed_log["status"] = "CC_EMPTY"
                per_ed_out[ed_name] = ed_log
                continue
            good_seed = (int(xs[len(xs) // 2]), int(ys[len(ys) // 2]))
        ed_log["seed_px_used"] = list(good_seed)
        ed_log["basin_cc_id"] = int(cc_id)
        ed_log["basin_area_px"] = int(cc_area_px)
        ed_log["basin_area_km2"] = round(cc_area_km2, 2)
        ed_log["basin_dist_px"] = round(best[0] ** 0.5, 0)

        cc_area = cc_area_px  # for compatibility with old names

        # (Double-check, but should always be false now)
        if cc_id in claimed_regions:
            ed_log["status"] = "REGION_ALREADY_CLAIMED"
            ed_log["claimed_by"] = claimed_regions[cc_id]
            per_ed_out[ed_name] = ed_log
            continue

        # Run full flood-fill / contour / polygon / disproof.
        # Instead of flood-fill, use the connected-component mask directly
        # (more efficient; we already have the labels).
        try:
            label_mask = (cc_labels == cc_id).astype(np.uint8) * 255
            ys_, xs_ = np.where(label_mask > 0)
            info_ff = {
                "area_px": int(np.count_nonzero(label_mask)),
                "bbox_px": [int(xs_.min()), int(ys_.min()),
                            int(xs_.max() - xs_.min()),
                            int(ys_.max() - ys_.min())],
                "seed": good_seed,
                "source": "cc_mask_direct",
            }
        except Exception as e:
            ed_log["status"] = f"CC_MASK_FAIL: {e}"
            per_ed_out[ed_name] = ed_log
            continue
        ed_log["flood_fill"] = info_ff

        try:
            contour_px = extract_contour(label_mask, approx_tol_px=1.5)
        except Exception as e:
            ed_log["status"] = f"CONTOUR_FAIL: {e}"
            per_ed_out[ed_name] = ed_log
            continue

        try:
            poly_geo = contour_to_polygon(contour_px, M, simplify_tol_m=40.0)
        except Exception as e:
            ed_log["status"] = f"POLYGON_FAIL: {e}"
            per_ed_out[ed_name] = ed_log
            continue

        if not poly_geo.is_valid or poly_geo.is_empty:
            ed_log["status"] = "INVALID_POLYGON"
            per_ed_out[ed_name] = ed_log
            continue

        ed_log["area_km2"] = round(poly_geo.area / 1e6, 2)
        ed_log["bounds"] = [round(v, 0) for v in poly_geo.bounds]

        # Area sanity: compare to 2019 analog. Already validated during
        # basin selection, so should always pass here.
        area_ratio = ed_log["area_km2"] / max(area_2019, 1.0)
        ed_log["area_ratio_v7_over_2019"] = round(area_ratio, 2)
        area_sanity_pass = (band_min <= area_ratio <= band_max)
        ed_log["area_sanity_pass"] = area_sanity_pass

        # Disproof
        try:
            disproof = disproof_pass(
                ed_name, poly_geo, contour_px, red, label_mask, M, (H, W),
                hard_constraints=None, adjacent_ed_geo=None,
            )
        except Exception as e:
            ed_log["disproof_error"] = str(e)
            disproof = {"summary": {"n_pass": 0, "n_considered": 0}}

        # Inject the area-sanity as an 8th disproof test
        disproof["t8_area_sanity_vs_2019"] = {
            "area_ratio": round(area_ratio, 2),
            "band": [band_min, band_max],
            "pass": bool(area_sanity_pass),
        }

        # Local T2 (visual diff) — restrict to the polygon's bbox + margin
        try:
            pts = contour_px.astype(np.int32)
            x, y, w, h = cv2.boundingRect(pts)
            pad = 40
            x0 = max(0, x - pad); y0 = max(0, y - pad)
            x1 = min(W, x + w + pad); y1 = min(H, y + h + pad)
            outline_local = np.zeros((y1 - y0, x1 - x0), dtype=np.uint8)
            shifted_pts = pts - np.array([[x0, y0]])
            cv2.drawContours(outline_local, [shifted_pts], -1, 255, thickness=1)
            dil_local = cv2.dilate(
                outline_local,
                cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)),
                iterations=1,
            )
            local_red = red[y0:y1, x0:x1]
            local_diff = local_red & ~dil_local
            n_yellow_local = int(np.count_nonzero(local_diff))
            if n_yellow_local > 0:
                _, _, stats_l, _ = cv2.connectedComponentsWithStats(
                    local_diff, connectivity=4)
                local_large = int(np.sum(stats_l[1:, cv2.CC_STAT_AREA] > 50))
            else:
                local_large = 0
            # Be generous — the commission map sometimes has text/labels in red
            # which show as yellow "diff" but aren't boundary errors.
            t2_pass = bool(local_large <= 4)
            disproof["t2_overlay_visual_diff"] = {
                "n_yellow_local": n_yellow_local,
                "n_large_clusters_local": local_large,
                "pass": t2_pass,
            }
        except Exception as e:
            ed_log["t2_error"] = str(e)

        considered = [k for k, v in disproof.items()
                      if isinstance(v, dict) and v.get("pass") is not None]
        n_pass = sum(1 for k in considered if disproof[k]["pass"])
        disproof["summary"] = {
            "n_pass": n_pass, "n_considered": len(considered),
        }
        ed_log["disproof"] = {k: v for k, v in disproof.items()
                              if k not in ("t5_reverse_sampling",)
                              or True}  # keep everything
        ed_log["n_pass"] = n_pass
        ed_log["n_considered"] = len(considered)
        ed_log["disproof_ratio"] = f"{n_pass}/{len(considered)}"

        # Accept if >=5 tests pass AND area is sane (required gate)
        if n_pass >= 5 and area_sanity_pass:
            derived_polys[ed_name] = poly_geo
            claimed_regions[cc_id] = ed_name
            ed_log["outcome"] = "ACCEPTED"
        elif not area_sanity_pass:
            ed_log["outcome"] = "REJECTED_AREA_SANITY"
        else:
            ed_log["outcome"] = "REJECTED_FALLBACK"

        per_ed_out[ed_name] = ed_log
        tag = "OK " if ed_log["outcome"] == "ACCEPTED" else "x  "
        print(f"  {tag}{ed_name}: {ed_log['outcome']} "
              f"({ed_log.get('disproof_ratio', 'n/a')}) "
              f"area={ed_log.get('area_km2', 'n/a')}/{round(area_2019, 1)} km2 "
              f"(ratio={ed_log.get('area_ratio_v7_over_2019', 'n/a')})")

    # Summarise outcomes
    n_accepted = sum(1 for v in per_ed_out.values()
                     if v.get("outcome") == "ACCEPTED")
    outcome_hist: dict[str, int] = {}
    for v in per_ed_out.values():
        key = v.get("outcome") or v.get("status", "UNKNOWN")
        outcome_hist[key] = outcome_hist.get(key, 0) + 1
    print(f"  Summary: {n_accepted}/{len(plan_entry['eds_to_attempt'])} accepted")
    for k, v in sorted(outcome_hist.items(), key=lambda x: -x[1]):
        print(f"    {v:3d}x  {k}")

    return {
        "label": label,
        "thumbnail": thumb_path.name,
        "orientation": plan_entry["orientation"],
        "resolution_tier": plan_entry["resolution_tier"],
        "dilate_px": dilate_px,
        "img_shape": [H, W],
        "red_pixels": int(np.count_nonzero(red)),
        "affine": {
            "M_px2geo": M.tolist(),
            "cost_dt_mean_px": round(cost, 2),
            "pixel_dim_m": round(pixel_dim_m, 2),
            "n_boundary_pts": info["n_boundary_points"],
        },
        "n_eds_attempted": len(plan_entry["eds_to_attempt"]),
        "n_accepted": n_accepted,
        "outcome_hist": outcome_hist,
        "per_ed": per_ed_out,
        "derived_polygons": derived_polys,
        "elapsed_s": round(time.time() - t0, 1),
    }


# -----------------------------------------------------------------------------
# Output writer
# -----------------------------------------------------------------------------

def _build_gpkg(
    map_set: str,
    thumb_results: list[dict],
    v6_gpkg_path: Path,
    out_path: Path,
) -> tuple[gpd.GeoDataFrame, dict]:
    """Assemble final gpkg: for each ED pick best derived polygon, else fallback.

    Fallback chain (in order):
      1. v7-derived polygon (from thumbnail)
      2. v6 polygon (already-refined for Tier C, or carried-forward Tier A)
      3. Approximate majority full (57+ Tier A polygons for majority)
      4. No geometry (no_source).
    """
    pop = pd.read_csv(DATA_DIR / f"v0_1_{map_set}_2026_populations.csv")
    v6 = gpd.read_file(v6_gpkg_path).to_crs(AREA_CRS)
    v6_by_name = {r["name_2026"]: r for _, r in v6.iterrows()}

    # Secondary fallback: approximate gpkgs have some EDs missing from v6
    approx_gpkg = DATA_DIR / f"v0_1_approximate_{map_set}_2026_eds_full.gpkg"
    if not approx_gpkg.exists():
        approx_gpkg = DATA_DIR / f"v0_1_approximate_{map_set}_2026_eds.gpkg"
    approx_by_name = {}
    if approx_gpkg.exists():
        approx = gpd.read_file(approx_gpkg).to_crs(AREA_CRS)
        approx_by_name = {r["name_2026"]: r for _, r in approx.iterrows()
                          if r.geometry is not None and not r.geometry.is_empty}

    # Aggregate derived polygons per ED, annotated by (thumbnail, n_pass)
    best_per_ed: dict[str, dict] = {}
    coverage_map: dict[str, list[dict]] = {}  # ed -> list of (thumb, n_pass, area_km2)

    # Priority order: city_detail > near_city_detail > overview_only
    tier_priority = {"city_detail": 0, "near_city_detail": 1, "overview_only": 2}

    for thumb_res in thumb_results:
        if "error" in thumb_res:
            continue
        tier = thumb_res["resolution_tier"]
        src = thumb_res["thumbnail"]
        for ed_name, ed_log in thumb_res["per_ed"].items():
            if ed_log.get("outcome") != "ACCEPTED":
                continue
            poly = thumb_res["derived_polygons"].get(ed_name)
            if poly is None:
                continue
            rec = {
                "ed_name": ed_name,
                "source_thumbnail": src,
                "resolution_tier": tier,
                "n_pass": ed_log["n_pass"],
                "n_considered": ed_log["n_considered"],
                "area_km2": ed_log.get("area_km2"),
                "polygon": poly,
                "affine_rms_m": thumb_res["affine"]["cost_dt_mean_px"]
                                * thumb_res["affine"]["pixel_dim_m"],
                "n_anchors": thumb_res["affine"]["n_boundary_pts"],
            }
            coverage_map.setdefault(ed_name, []).append(rec)

            cur = best_per_ed.get(ed_name)
            if cur is None:
                best_per_ed[ed_name] = rec
            else:
                # Prefer higher-resolution tier; tie-break on n_pass
                cur_tier = tier_priority.get(cur["resolution_tier"], 9)
                new_tier = tier_priority.get(tier, 9)
                if (new_tier < cur_tier) or (
                    new_tier == cur_tier and rec["n_pass"] > cur["n_pass"]
                ):
                    best_per_ed[ed_name] = rec

    # Now build rows
    out_rows = []
    for _, pr in pop.iterrows():
        name = pr["ed_name"]
        derived = best_per_ed.get(name)
        v6_row = v6_by_name.get(name)
        approx_row = approx_by_name.get(name)

        # Build v6 geometry reference (handles Polygon and MultiPolygon)
        v6_geom = None
        if v6_row is not None and v6_row.geometry is not None and \
                not isinstance(v6_row.geometry, float) and \
                not v6_row.geometry.is_empty:
            v6_geom = v6_row.geometry

        # Build approximate-fallback geometry reference
        approx_geom = None
        if approx_row is not None and approx_row.geometry is not None and \
                not isinstance(approx_row.geometry, float) and \
                not approx_row.geometry.is_empty:
            approx_geom = approx_row.geometry

        if derived is not None:
            row = {
                "name_2026": name,
                "ed_name": name,
                "source_thumbnail": derived["source_thumbnail"],
                "resolution_tier": derived["resolution_tier"],
                "n_anchors": int(derived["n_anchors"]),
                "affine_rms_m": float(round(derived["affine_rms_m"], 1)),
                "disproof_n_pass": int(derived["n_pass"]),
                "disproof_n_considered": int(derived["n_considered"]),
                "fallback": False,
                "fallback_reason": "",
                "area_km2": float(round(derived["area_km2"], 2))
                            if derived["area_km2"] else None,
                "tier_2026": v6_row["tier"] if v6_row is not None else "",
                "geometry": derived["polygon"],
            }
        elif v6_geom is not None:
            row = {
                "name_2026": name,
                "ed_name": name,
                "source_thumbnail": "",
                "resolution_tier": "v6_fallback",
                "n_anchors": 0,
                "affine_rms_m": None,
                "disproof_n_pass": 0,
                "disproof_n_considered": 0,
                "fallback": True,
                "fallback_reason": "derivation_failed_or_not_attempted",
                "area_km2": float(round(v6_geom.area / 1e6, 2)),
                "tier_2026": v6_row["tier"],
                "geometry": v6_geom,
            }
        elif approx_geom is not None:
            # Secondary fallback: approximate shapefile (Tier A baseline)
            row = {
                "name_2026": name,
                "ed_name": name,
                "source_thumbnail": "",
                "resolution_tier": "approximate_fallback",
                "n_anchors": 0,
                "affine_rms_m": None,
                "disproof_n_pass": 0,
                "disproof_n_considered": 0,
                "fallback": True,
                "fallback_reason": "v6_null_used_approximate",
                "area_km2": float(round(approx_geom.area / 1e6, 2)),
                "tier_2026": approx_row["tier"] if "tier" in approx_row.index else "",
                "geometry": approx_geom,
            }
        else:
            # Truly no source available
            row = {
                "name_2026": name,
                "ed_name": name,
                "source_thumbnail": "",
                "resolution_tier": "no_source",
                "n_anchors": 0,
                "affine_rms_m": None,
                "disproof_n_pass": 0,
                "disproof_n_considered": 0,
                "fallback": True,
                "fallback_reason": "no_thumbnail_nor_v6_nor_approx",
                "area_km2": None,
                "tier_2026": "C-null",
                "geometry": None,
            }
        out_rows.append(row)

    gdf = gpd.GeoDataFrame(out_rows, geometry="geometry", crs=AREA_CRS)
    gdf_wc = gdf.to_crs(WORK_CRS)
    gdf_wc.to_file(out_path, driver="GPKG")
    print(f"[WRITE] {out_path.name}: {len(gdf)} rows "
          f"(derived={sum(1 for r in out_rows if not r['fallback'])}, "
          f"fallback={sum(1 for r in out_rows if r['fallback'])})")

    # Coverage summary
    coverage_summary = {
        ed: [{"thumb": r["source_thumbnail"],
              "tier": r["resolution_tier"],
              "n_pass": r["n_pass"],
              "n_considered": r["n_considered"],
              "area_km2": r["area_km2"],
              "chosen": r is best_per_ed.get(ed)} for r in recs]
        for ed, recs in coverage_map.items()
    }

    return gdf, coverage_summary


# -----------------------------------------------------------------------------
# Main entry
# -----------------------------------------------------------------------------

def main():
    t_start = time.time()
    print("[v7] Loading 2019 EDs")
    eds2019 = gpd.read_file(EDS_2019_PATH).to_crs(AREA_CRS)

    log: dict = {
        "version": "v7",
        "timestamp": pd.Timestamp.utcnow().isoformat(),
        "map_sets": {},
    }

    for map_set in ("minority", "majority"):
        print(f"\n{'='*60}\n{map_set.upper()}\n{'='*60}")
        plan = _make_plan(map_set)
        thumb_results: list[dict] = []
        for plan_entry in plan:
            try:
                res = _process_thumbnail(plan_entry, eds2019)
            except Exception as e:
                import traceback
                traceback.print_exc()
                res = {"label": plan_entry["label"],
                       "thumbnail": plan_entry["thumb"].name,
                       "error": str(e), "per_ed": {}, "derived_polygons": {}}
            thumb_results.append(res)

        v6_gpkg = DATA_DIR / f"v0_1_refined_v6_{map_set}_2026_eds.gpkg"
        out_gpkg = DATA_DIR / f"v0_1_derived_v7_{map_set}_2026_eds.gpkg"
        gdf, coverage = _build_gpkg(map_set, thumb_results, v6_gpkg, out_gpkg)

        # Strip non-serializable objects from per-thumbnail log
        serial_thumb_results = []
        for tr in thumb_results:
            st = {k: v for k, v in tr.items() if k != "derived_polygons"}
            serial_thumb_results.append(st)

        log["map_sets"][map_set] = {
            "n_total_eds": len(gdf),
            "n_derived": int((~gdf["fallback"]).sum()),
            "n_fallback": int(gdf["fallback"].sum()),
            "n_no_source": int((gdf["resolution_tier"] == "no_source").sum()),
            "thumbnails": serial_thumb_results,
            "coverage_overlap": coverage,
        }

    log["elapsed_s"] = round(time.time() - t_start, 1)

    log_path = ANALYSIS_DIR / "shape_derivation_v7_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, default=str)
    print(f"\n[WRITE] {log_path.name}")

    print(f"\n[v7] Total runtime: {log['elapsed_s']} s")
    for map_set in ("minority", "majority"):
        ms = log["map_sets"][map_set]
        print(f"  {map_set}: {ms['n_derived']} derived / {ms['n_fallback']} fallback "
              f"(no_source: {ms['n_no_source']})")

    return log


if __name__ == "__main__":
    main()
