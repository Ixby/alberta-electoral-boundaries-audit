"""
v0_1_build_overlay_figures.py

Build four publication-quality per-municipality translucent overlay maps
comparing the approximate 2026 majority and minority ED proposals.

Visual contract
  Orange (#e87722)  -> majority-only territory
  Blue   (#335c81)  -> minority-only territory
  Brown  (#8b5b3c)  -> overlap (both plans cover the same territory)
  Dashed grey       -> 2019 baseline ED boundaries (reference)
  Light grey fill   -> outside both plans / unclassified in this frame

We EXPLICITLY compute set algebra on the coverage polygons instead of relying
on alpha blending for the overlap colour. This avoids the flat-grey problem
where 0.45-alpha orange + 0.45-alpha blue produces near-muddy-grey everywhere
instead of a readable three-zone Venn.

Data gap handling
  The approximate majority gpkg only carries Tier A/B EDs (57 of 89). For the
  remaining 32 Tier C majority EDs (Lethbridge-East/West, Airdrie-East/West,
  Cochrane-Springbank, etc.), we fall back to the 2019 shapefile as a proxy.
  For Calgary (where no 2019 ED named "Calgary-Bhullar-McCall" etc. exists),
  we exclude the frame-level majority contribution; the caption notes this.
  The honest story: when the majority plan keeps 2019 cores with only minor
  boundary tweaks, using 2019 polygons as a stand-in is a faithful proxy.

Dependencies
  Forward  : data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
             data/v0_1_approximate_majority_2026_eds.gpkg
             data/v0_1_refined_v5_minority_2026_eds.gpkg  (preferred)
             data/v0_1_refined_v4_minority_2026_eds.gpkg  (fallback)
             data/majority_2026_populations.csv  (89-ED list)
             data/majority_hybrid_crosswalk.csv   (rename lineage)
  Backward : maps/article/overlay_calgary.svg
             maps/article/overlay_reddeer.svg
             maps/article/overlay_airdrie.svg
             maps/article/overlay_lethbridge.svg
             analysis/methodology/build_overlay_figures.md

Run
  PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_build_overlay_figures.py

Author : sub-agent, article figures task, 2026-04-22
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


import os
import sys
from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from shapely.geometry import Point, box
from shapely.ops import unary_union

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# ---------------------------------------------------------------------------
# Paths / constants

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
OUT = data_loader._resolve_path("data") / "maps" / "article"
OUT.mkdir(parents=True, exist_ok=True)

PATH_2019 = (
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)
PATH_MAJ = DATA / "shapefiles" / "derived" / "v0_1_approximate_majority_2026_eds.gpkg"
PATH_MIN_V5 = DATA / "shapefiles" / "derived" / "v0_1_refined_v5_minority_2026_eds.gpkg"
PATH_MIN_V4 = DATA / "shapefiles" / "derived" / "v0_1_refined_v4_minority_2026_eds.gpkg"
PATH_MAJ_POPS = DATA / "majority_2026_populations.csv"
PATH_MAJ_XWALK = DATA / "majority_hybrid_crosswalk.csv"

CRS_PLOT = 3401  # NAD83 / Alberta 10-TM Forest, metres

# Map of 2019 ED -> majority 2026 ED used when the majority gpkg omits the Tier C
# entry and we want to attribute the 2019 polygon to the renamed 2026 ED.
# Built lazily from majority_hybrid_crosswalk.csv at load time.

COLOR_MAJ = "#e87722"  # UCP-ish orange
COLOR_MIN = "#335c81"  # dusty blue
COLOR_BOTH = "#8d5a3b"  # mid brown for overlap -- readable, but the
# partition lines drawn on top still stand out.
ALPHA_MAJ = 0.55
ALPHA_MIN = 0.55
ALPHA_BOTH = 0.55

# Strong, contrasting coloured edges so each plan's partition lines are legible
# even over the brown overlap.
EDGE_WIDTH_MAJ = 1.7
EDGE_WIDTH_MIN = 1.7
EDGE_COLOR_MAJ = "#b74000"  # deep bright orange/red
EDGE_COLOR_MIN = "#0b1d3a"  # deep navy
EDGE_WIDTH_2019 = 0.55
BG_OUTSIDE = "#efefef"  # territory inside frame but outside both plans

FONT_TITLE = dict(fontsize=15, fontweight="bold", family="DejaVu Sans")

# ---------------------------------------------------------------------------
# Figure specs


@dataclass(frozen=True)
class FigSpec:
    slug: str
    title: str
    primary_city: str
    city_lonlat: tuple[float, float]
    half_width_km: float
    caption: str


SPECS: list[FigSpec] = [
    FigSpec(
        slug="calgary",
        title="Calgary: majority vs minority 2026",
        primary_city="Calgary",
        city_lonlat=(-114.0719, 51.0447),
        half_width_km=35.0,
        caption=(
            "Calgary and its commuter belt. Orange = majority-only territory; "
            "blue = minority-only territory; brown = both plans cover the same "
            "area. Where the plans diverge most visibly: the northwest corridor "
            "(blue-only, minority Nolan Hill / Cochrane lasso), Chestermere / "
            "Strathmore (blue-only, minority's Chestermere-Strathmore splits "
            "the majority's Chestermere-Strathmore hybrid), and the south "
            "exurbs (blue-only, minority's Calgary-De Winton / Calgary-South). "
            "Approximate 2026 geometry - Elections Alberta has not released "
            "shapefiles. Tier A / B EDs inherit 2019 boundaries; Tier C "
            "minority EDs (heavy dashed black outline, if visible) are "
            "visually transcribed from commission thumbnails. Missing "
            "majority Tier C polygons are proxied from 2019."
        ),
    ),
    FigSpec(
        slug="reddeer",
        title="Red Deer: majority vs minority 2026",
        primary_city="Red Deer",
        city_lonlat=(-113.8117, 52.2681),
        half_width_km=27.0,
        caption=(
            "The Red Deer area. Orange = majority-only; blue = minority-only; "
            "brown = both plans cover the same territory. Both plans cover "
            "the same footprint -- but they name and partition it differently. "
            "The majority draws two compact city EDs (Red Deer-North, Red "
            "Deer-South) plus regional Lacombe-Clearwater and Sylvan "
            "Lake-Innisfail (solid orange lines). The minority renames and "
            "repartitions into four Red Deer-prefixed hybrids: Red "
            "Deer-Sylvan Lake, Red Deer-Innisfail, Red Deer-Blackfalds, Red "
            "Deer-Lacombe (dashed blue lines). Because the approximate "
            "shapes inherit 2019 boundaries where Tier A rules apply, the "
            "inner-city partition here matches the majority's; the "
            "differentiation is in naming and in how rural territory is "
            "attached to a Red Deer-named ED versus a regional ED. "
            "Approximate 2026 geometry - shapefiles not yet released by "
            "Elections Alberta."
        ),
    ),
    FigSpec(
        slug="airdrie",
        title="Airdrie: majority vs minority 2026",
        primary_city="Airdrie",
        city_lonlat=(-114.0167, 51.2917),
        half_width_km=22.0,
        caption=(
            "The Airdrie area. Orange = majority-only; blue = minority-only; "
            "brown = both plans agree. The minority (blue) splits this "
            "commuter shed four ways (Airdrie East, Chestermere-Strathmore, "
            "Olds-Three Hills-Didsbury, Canmore-Kananaskis). The majority "
            "(orange, partly proxied from 2019 for Tier C Airdrie-East / "
            "Airdrie-West / Cochrane-Springbank) keeps an Airdrie-named pair "
            "but folds the rural fringe into regional EDs. Approximate 2026 "
            "geometry - shapefiles not yet released by Elections Alberta. "
            "2019 baseline shown as dashed grey."
        ),
    ),
    FigSpec(
        slug="lethbridge",
        title="Lethbridge: majority vs minority 2026",
        primary_city="Lethbridge",
        city_lonlat=(-112.8333, 49.6956),
        half_width_km=30.0,
        caption=(
            "The Lethbridge area - the symmetric counter-test case. Orange = "
            "majority-only; blue = minority-only; brown = both plans agree. "
            "The minority (blue) draws two Lethbridge hybrids "
            "(Lethbridge-Cardston, Lethbridge-Little Bow), each pulling rural "
            "territory into a Lethbridge-named ED; the majority (orange, "
            "proxied from 2019 for Tier C Lethbridge-East / Lethbridge-West / "
            "Taber-Cardston) keeps two compact Lethbridge city EDs and pushes "
            "rural area into Livingstone-Macleod. Approximate 2026 geometry - "
            "shapefiles not yet released by Elections Alberta. 2019 baseline "
            "shown as dashed grey."
        ),
    ),
]

# Where the approximate majority gpkg omits a Tier C 2026 ED, we map the
# corresponding 2019 polygon(s) onto the 2026 name as a proxy.  Built from
# majority_hybrid_crosswalk.csv + best-guess inheritance for EDs the
# crosswalk doesn't explicitly list (we just pass the 2019 name through if it
# equals the 2026 name).
MAJORITY_TIER_C_2019_PROXIES: dict[str, list[str]] = {
    # From crosswalk.csv (direct renames)
    "Airdrie-West": ["Airdrie-Cochrane"],
    "Airdrie-East": ["Airdrie-East"],
    "Medicine Hat-Brooks": ["Brooks-Medicine Hat"],
    "Leduc-Devon": ["Leduc-Beaumont"],
    "St. Albert-Sturgeon": ["Morinville-St. Albert"],
    "Chestermere-Strathmore": ["Chestermere-Strathmore"],
    "Cold Lake-Bonnyville-St. Paul": ["Bonnyville-Cold Lake-St. Paul"],
    # Not in crosswalk but easily inferred (pass-through / well-known hybrids)
    "Lethbridge-East": ["Lethbridge-East"],
    "Lethbridge-West": ["Lethbridge-West"],
    "Taber-Cardston": ["Taber-Warner", "Cardston-Siksika"],
    "Cochrane-Springbank": ["Banff-Kananaskis"],
    "Canmore-Banff": ["Banff-Kananaskis"],
    "High River-Vulcan-Siksika": ["Highwood", "Cardston-Siksika"],
    "Okotoks-Diamond Valley": ["Highwood"],
    "Mountain View-Kneehill": ["Olds-Didsbury-Three Hills"],
    "Sylvan Lake-Innisfail": ["Innisfail-Sylvan Lake"],
    "Barrhead-Westlock-Athabasca": ["Athabasca-Barrhead-Westlock"],
    "Stony Plain-Drayton Valley": ["Drayton Valley-Devon"],
    "Fort McMurray-Lac La Biche": ["Fort McMurray-Lac La Biche"],
    "Edmonton-Glenora-Riverview": ["Edmonton-Glenora", "Edmonton-Riverview"],
    "Edmonton-Windermere": ["Edmonton-South West"],
    "Edmonton-Beaumont": ["Edmonton-South West"],
    "Edmonton-Enoch": ["Edmonton-South West"],
    # Calgary Tier C -- best guess but Calgary majority hybrids aren't trivially
    # mappable. Use the 2019 urban ED that most overlaps.
    "Calgary-Bhullar-McCall": ["Calgary-McCall"],
    "Calgary-East": ["Calgary-East"],
    "Calgary-Falconridge-Conrich": ["Calgary-Falconridge"],
    "Calgary-Glenmore-Tsuut'ina": ["Calgary-Glenmore"],
    "Calgary-West-Elbow Valley": ["Calgary-West"],
    "Calgary-Confluence": ["Calgary-Peigan"],
    "Calgary-McKenzie": ["Calgary-Foothills"],
    "Calgary-Nose Creek": ["Calgary-Foothills"],
    "Calgary-Symons Valley": ["Calgary-Foothills"],
}


# ---------------------------------------------------------------------------
# Loaders


def load_2019() -> gpd.GeoDataFrame:
    g = gpd.read_file(PATH_2019)
    if g.crs is None:
        g.set_crs(epsg=3401, inplace=True)
    return g.to_crs(CRS_PLOT)


def load_majority_full(g19: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Majority polygons: Tier A/B from gpkg, Tier C proxied from 2019."""
    base = gpd.read_file(PATH_MAJ).to_crs(CRS_PLOT)
    in_gpkg = set(base["name_2026"])

    pops = pd.read_csv(PATH_MAJ_POPS)
    rows_existing = base.copy()

    proxy_rows = []
    g19_by_name = {str(r["EDName2017"]): r.geometry for _, r in g19.iterrows()}
    for name in pops["ed_name"]:
        if name in in_gpkg:
            continue
        parents = MAJORITY_TIER_C_2019_PROXIES.get(name)
        if not parents:
            continue  # no proxy available; skip (will simply be absent in plot)
        geoms = [g19_by_name[p] for p in parents if p in g19_by_name]
        if not geoms:
            continue
        proxy_rows.append(
            {
                "name_2026": name,
                "tier": "C-proxy-2019",
                "confidence": "low",
                "parents_2019": "+".join(parents),
                "note": "proxy: 2019 polygon used for missing Tier C majority shape",
                "geometry": unary_union(geoms),
            }
        )
    if proxy_rows:
        proxy_gdf = gpd.GeoDataFrame(proxy_rows, geometry="geometry", crs=CRS_PLOT)
        combined = pd.concat([rows_existing, proxy_gdf], ignore_index=True)
        return gpd.GeoDataFrame(combined, geometry="geometry", crs=CRS_PLOT)
    return rows_existing


def load_minority(prefer_v5: bool) -> tuple[gpd.GeoDataFrame, str]:
    if prefer_v5 and PATH_MIN_V5.exists():
        return gpd.read_file(PATH_MIN_V5).to_crs(CRS_PLOT), "v5"
    return gpd.read_file(PATH_MIN_V4).to_crs(CRS_PLOT), "v4"


# ---------------------------------------------------------------------------
# Geometry helpers


def lonlat_to_xy(lon: float, lat: float) -> tuple[float, float]:
    p = gpd.GeoSeries([Point(lon, lat)], crs=4326).to_crs(CRS_PLOT).iloc[0]
    return (p.x, p.y)


def bbox_around(lon: float, lat: float, half_km: float):
    cx, cy = lonlat_to_xy(lon, lat)
    h = half_km * 1000.0
    return (cx - h, cy - h, cx + h, cy + h)


def clip_to_bbox(g: gpd.GeoDataFrame, bbox) -> gpd.GeoDataFrame:
    minx, miny, maxx, maxy = bbox
    mask = box(minx, miny, maxx, maxy)
    sub = g[g.geometry.intersects(mask)].copy()
    if sub.empty:
        return sub
    sub["geometry"] = sub.geometry.intersection(mask)
    return sub[~sub.geometry.is_empty]


def compute_zones(maj_clip: gpd.GeoDataFrame, min_clip: gpd.GeoDataFrame, frame_mask):
    """Return (majority_only, minority_only, both) shapely geometries."""
    maj_u = unary_union(maj_clip.geometry.tolist()) if not maj_clip.empty else None
    min_u = unary_union(min_clip.geometry.tolist()) if not min_clip.empty else None

    if maj_u is None and min_u is None:
        return None, None, None
    if maj_u is None:
        return None, min_u.intersection(frame_mask), None
    if min_u is None:
        return maj_u.intersection(frame_mask), None, None

    both = maj_u.intersection(min_u)
    only_maj = maj_u.difference(min_u)
    only_min = min_u.difference(maj_u)
    return (
        only_maj.intersection(frame_mask),
        only_min.intersection(frame_mask),
        both.intersection(frame_mask),
    )


# ---------------------------------------------------------------------------
# Drawing helpers


def add_scale_bar(ax, x0, y0, length_km=10, height_m=400):
    length_m = length_km * 1000.0
    # white bg halo
    halo = mpatches.Rectangle(
        (x0 - length_m * 0.08, y0 - height_m * 1.2),
        length_m * 1.16,
        height_m * 4.5,
        linewidth=0,
        facecolor="white",
        alpha=0.85,
        zorder=4,
    )
    ax.add_patch(halo)
    bar = mpatches.Rectangle(
        (x0, y0),
        length_m,
        height_m,
        linewidth=0.8,
        edgecolor="black",
        facecolor="black",
        zorder=5,
    )
    ax.add_patch(bar)
    ax.text(
        x0 + length_m / 2,
        y0 + height_m * 2.0,
        f"{length_km} km",
        ha="center",
        va="bottom",
        fontsize=7.5,
        family="DejaVu Sans",
        zorder=6,
    )


def add_north_arrow(ax, x, y, size=1500):
    halo = mpatches.Circle(
        (x, y),
        radius=size * 1.2,
        linewidth=0,
        facecolor="white",
        alpha=0.85,
        zorder=4,
    )
    ax.add_patch(halo)
    ax.annotate(
        "N",
        xy=(x, y + size),
        xytext=(x, y - size),
        arrowprops=dict(facecolor="black", width=2, headwidth=8, headlength=8),
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        family="DejaVu Sans",
        zorder=6,
    )


def label_ed(ax, geom, text, fontsize=7.5, weight="normal", color="#1a1a1a"):
    try:
        pt = geom.representative_point()
    except Exception:
        return
    ax.annotate(
        text,
        xy=(pt.x, pt.y),
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
        family="DejaVu Sans",
        color=color,
        bbox=dict(boxstyle="round,pad=0.18", fc=(1, 1, 1, 0.85), ec="none"),
        zorder=7,
    )


# ---------------------------------------------------------------------------
# Per-figure render


def draw_figure(spec: FigSpec, g2019, maj, mino, mino_version: str) -> dict:
    bbox = bbox_around(*spec.city_lonlat, spec.half_width_km)
    minx, miny, maxx, maxy = bbox
    frame_mask = box(minx, miny, maxx, maxy)

    maj_c = clip_to_bbox(maj, bbox)
    min_c = clip_to_bbox(mino, bbox)
    g19_c = clip_to_bbox(g2019, bbox)

    # --- Figure geometry
    fig_w = 8.0
    ratio = (maxy - miny) / max(1.0, (maxx - minx))
    fig_h = max(7.0, min(10.5, fig_w * ratio + 1.8))  # +caption margin

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)

    # --- Background: light grey for territory outside either plan
    bg = mpatches.Rectangle(
        (minx, miny),
        maxx - minx,
        maxy - miny,
        facecolor=BG_OUTSIDE,
        edgecolor="none",
        zorder=0,
    )
    ax.add_patch(bg)

    # --- Set-algebra zones
    only_maj, only_min, both = compute_zones(maj_c, min_c, frame_mask)

    def _draw_geom(geom, facecolor, edgecolor, alpha, zorder):
        if geom is None or geom.is_empty:
            return
        g = gpd.GeoSeries([geom], crs=CRS_PLOT)
        g.plot(
            ax=ax,
            facecolor=facecolor,
            edgecolor="none",
            linewidth=0,
            alpha=alpha,
            zorder=zorder,
        )

    # Draw overlap (both plans cover) in back so orange and blue surface on top.
    # The three zones are geometrically disjoint; z-ordering matters only for
    # the millimetre-scale rendering overlap at shared-boundary segments.
    _draw_geom(both, COLOR_BOTH, "#5d3d29", ALPHA_BOTH, zorder=1)
    _draw_geom(only_maj, COLOR_MAJ, "#a6551a", ALPHA_MAJ, zorder=2)
    _draw_geom(only_min, COLOR_MIN, "#223f59", ALPHA_MIN, zorder=2)

    # --- 2019 baseline (dashed, drawn ABOVE fills so it stays visible)
    if not g19_c.empty:
        g19_c.boundary.plot(
            ax=ax,
            linewidth=EDGE_WIDTH_2019,
            color="#555555",
            linestyle=(0, (3, 2)),
            zorder=3,
        )

    # --- ED boundaries from each plan. Solid for majority, dashed for
    # minority -- instant visual separation when both plans partition the
    # same territory differently.
    if not maj_c.empty:
        maj_c.boundary.plot(
            ax=ax,
            linewidth=EDGE_WIDTH_MAJ,
            color=EDGE_COLOR_MAJ,
            linestyle="-",
            alpha=0.95,
            zorder=4,
        )
    if not min_c.empty:
        min_c.boundary.plot(
            ax=ax,
            linewidth=EDGE_WIDTH_MIN,
            color=EDGE_COLOR_MIN,
            linestyle=(0, (4, 2.5)),
            alpha=0.95,
            zorder=5,
        )

    # --- Emphasise Tier-C approximated EDs in minority (heavy black dashed)
    tierc_flag = min_c[min_c["tier"].astype(str).str.contains("C", na=False)].copy()
    if not tierc_flag.empty:
        tierc_flag.boundary.plot(
            ax=ax,
            linewidth=1.6,
            color="#0a0a0a",
            linestyle=(0, (2, 2)),
            zorder=5,
        )

    # --- Labels. Use a two-pass minimum-distance scheme:
    #   1. Collect candidate labels with their centroid-like anchor.
    #   2. Greedy placement: skip any label whose anchor is too close to an
    #      already placed label (prevents the stacking issue).
    # Majority names labelled in dark orange; minority names in dark blue.
    # If the same name is in both plans, label it once in black.
    frame_area = (maxx - minx) * (maxy - miny)
    min_label_area = frame_area * 0.012

    maj_names = set(maj_c["name_2026"]) if not maj_c.empty else set()
    min_names = set(min_c["name_2026"]) if not min_c.empty else set()
    shared = maj_names & min_names

    def _candidates(gdf, text_color, weight):
        out = []
        if gdf.empty:
            return out
        for _, row in gdf.iterrows():
            name = str(row["name_2026"])
            if row.geometry.is_empty or row.geometry.area < min_label_area:
                continue
            try:
                pt = row.geometry.representative_point()
            except Exception:
                continue
            tc = "#111111" if name in shared else text_color
            w = "bold" if name in shared else weight
            out.append((name, pt.x, pt.y, row.geometry.area, tc, w))
        return out

    cands = []
    cands += _candidates(maj_c, "#5c2e0d", "bold")
    cands += _candidates(min_c, "#17283d", "normal")
    # Sort biggest polygons first so large EDs get labelled even if crowded.
    cands.sort(key=lambda t: -t[3])

    placed: list[tuple[float, float]] = []
    labelled = set()
    min_sep = min(maxx - minx, maxy - miny) * 0.07  # no two labels within 7%
    for name, x, y, _area, tc, w in cands:
        if name in labelled:
            continue
        too_close = any(
            ((x - px) ** 2 + (y - py) ** 2) ** 0.5 < min_sep for px, py in placed
        )
        if too_close:
            continue
        # Build a tiny synthetic point geometry for label placement
        from shapely.geometry import Point as _P

        label_ed(ax, _P(x, y), name, fontsize=7.5, weight=w, color=tc)
        placed.append((x, y))
        labelled.add(name)

    # --- Primary city marker + label
    cx, cy = lonlat_to_xy(*spec.city_lonlat)
    if minx <= cx <= maxx and miny <= cy <= maxy:
        ax.scatter(
            [cx],
            [cy],
            s=45,
            color="black",
            zorder=8,
            marker="o",
            edgecolor="white",
            linewidth=1.2,
        )
        ax.annotate(
            spec.primary_city.upper(),
            xy=(cx, cy),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=12,
            fontweight="bold",
            family="DejaVu Sans",
            color="#111111",
            zorder=9,
            bbox=dict(
                boxstyle="round,pad=0.25", fc=(1, 1, 1, 0.9), ec="#111", linewidth=0.6
            ),
        )

    # --- Scale bar + north arrow
    scale_km = 10 if spec.half_width_km >= 20 else 5
    sx = minx + (maxx - minx) * 0.05
    sy = miny + (maxy - miny) * 0.05
    add_scale_bar(ax, sx, sy, length_km=scale_km, height_m=max(300, scale_km * 35))

    nx = minx + (maxx - minx) * 0.93
    ny = miny + (maxy - miny) * 0.11
    add_north_arrow(ax, nx, ny, size=scale_km * 110)

    # --- Legend
    handles = [
        mpatches.Patch(
            facecolor=COLOR_MAJ,
            alpha=ALPHA_MAJ,
            edgecolor=EDGE_COLOR_MAJ,
            label="Majority only (orange fill)",
        ),
        mpatches.Patch(
            facecolor=COLOR_MIN,
            alpha=ALPHA_MIN,
            edgecolor=EDGE_COLOR_MIN,
            label="Minority only (blue fill)",
        ),
        mpatches.Patch(
            facecolor=COLOR_BOTH,
            alpha=ALPHA_BOTH,
            edgecolor="#5d3d29",
            label="Both plans cover (brown fill)",
        ),
        Line2D(
            [0],
            [0],
            color=EDGE_COLOR_MAJ,
            linewidth=EDGE_WIDTH_MAJ,
            linestyle="-",
            label="Majority partition line (solid)",
        ),
        Line2D(
            [0],
            [0],
            color=EDGE_COLOR_MIN,
            linewidth=EDGE_WIDTH_MIN,
            linestyle=(0, (4, 2.5)),
            label="Minority partition line (dashed)",
        ),
        Line2D(
            [0],
            [0],
            color="#555555",
            linewidth=1.0,
            linestyle=(0, (3, 2)),
            label="2019 baseline",
        ),
    ]
    if not tierc_flag.empty:
        handles.append(
            Line2D(
                [0],
                [0],
                color="#0a0a0a",
                linewidth=1.6,
                linestyle=(0, (2, 2)),
                label="Tier C minority (visually transcribed)",
            )
        )
    ax.legend(handles=handles, loc="upper left", fontsize=7.5, framealpha=0.94)

    # --- Axis cleanup
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#bfbfbf")
        s.set_linewidth(0.6)

    ax.set_title(spec.title, **FONT_TITLE, loc="left", pad=8)

    # --- Caption
    caption = spec.caption
    if mino_version == "v5":
        caption += (
            " Minority shapes use v5 refinement (improved Tier C "
            "shapes for De Winton, Calgary-South, Windermere)."
        )
    else:
        caption += " Minority shapes use v4 refinement."
    fig.text(
        0.03,
        0.015,
        caption,
        ha="left",
        va="bottom",
        fontsize=7.5,
        family="DejaVu Sans",
        color="#333333",
        wrap=True,
    )

    # Leave generous bottom margin for caption
    fig.subplots_adjust(left=0.03, right=0.97, top=0.94, bottom=0.18)

    out_path = OUT / f"overlay_{spec.slug}.svg"
    fig.savefig(
        out_path, dpi=300, bbox_inches="tight", facecolor="white", pad_inches=0.15
    )
    plt.close(fig)

    # Compute visible ED counts
    return {
        "slug": spec.slug,
        "path": str(out_path),
        "maj_count": len(maj_c),
        "min_count": len(min_c),
        "tierC_count": int(len(tierc_flag)),
        "min_version": mino_version,
        "caption": caption,
    }


def main() -> int:
    print("Loading geometry...")
    g19 = load_2019()
    maj = load_majority_full(g19)
    min_gdf, ver = load_minority(prefer_v5=True)
    print(
        f"  2019 n={len(g19)}  majority(full w/ proxies) n={len(maj)}  "
        f"minority n={len(min_gdf)} (ver {ver})"
    )

    results = []
    for spec in SPECS:
        print(f"\nDrawing {spec.slug}...")
        r = draw_figure(spec, g19, maj, min_gdf, ver)
        print(
            f"  -> {r['path']}  (maj={r['maj_count']} min={r['min_count']} "
            f"tierC={r['tierC_count']})"
        )
        results.append(r)

    print("\n=== SUMMARY ===")
    for r in results:
        print(f"{r['slug']:12s}  {r['path']}")
        print(
            f"  maj_eds={r['maj_count']} min_eds={r['min_count']} "
            f"tierC_visible={r['tierC_count']} min_version={r['min_version']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
