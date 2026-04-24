"""
v0_1_build_overlay_figures_v2.py

Rebuild the four magazine-article overlay maps as two-panel side-by-side
comparisons ("Majority proposal 2026" vs "Minority proposal 2026") rather
than set-arithmetic overlays. The v1 overlay dissolved into mostly-brown
"both plans cover" rectangles because the plans agree on the exterior
footprint but disagree on the internal partition - exactly what the
article's argument is about. A side-by-side layout lets each partition
read clearly.

For each region:
  - Left panel  : majority 2026 polygons clipped to the shared bbox
  - Right panel : minority 2026 polygons clipped to the shared bbox
  - Both panels share extent, projection (EPSG:3401), scale bar, north
    arrow; the highlighted 2-3 EDs the caption flags are colour-filled
    against a neutral ivory/grey base, labelled inline.

Data sources (same as v1)
  - data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp   (Tier A identity)
  - data/v0_1_approximate_majority_2026_eds.gpkg             (Tier A+B majority)
  - data/v0_1_refined_v6_minority_2026_eds.gpkg              (full minority)
  - data/v0_1_majority_full_crosswalk.csv                    (88-row name map)
  - data/v0_1_minority_full_crosswalk.csv                    (88-row name map)

Tier C handling
  The majority gpkg only carries 57 of 87 2026 EDs. For Tier C majority EDs
  that don't appear in the gpkg we proxy from the 2019 polygon that the
  majority crosswalk maps onto the new name. This is explicit and honest -
  where a 2026 majority ED is a straight rename from one 2019 ED, the 2019
  shape stands in for the 2026 shape; where it's a boundary tweak or split,
  we flag it visually with a lighter fill and the caveat line in the credit.

  The minority v6 gpkg carries all 87 EDs so no proxying is needed.

Outputs
  - maps/article/overlay_calgary_v2.png
  - maps/article/overlay_airdrie_v2.png
  - maps/article/overlay_lethbridge_v2.png
  - maps/article/overlay_reddeer_v2.png   (Red Deer option 1 - see md note)

Run
  PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_build_overlay_figures_v2.py

Dependencies
  Forward  : data/alberta_2019_eds/*.shp, data/v0_1_approximate_majority_2026_eds.gpkg,
             data/v0_1_refined_v6_minority_2026_eds.gpkg,
             data/v0_1_majority_full_crosswalk.csv,
             data/v0_1_minority_full_crosswalk.csv
  Backward : maps/article/overlay_*_v2.png,
             analysis/methodology/v0_1_overlay_figures_v2.md,
             report_public.md (four figure references updated to _v2)

Author: sub-agent, overlay rebuild task, 2026-04-23
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, box
from shapely.ops import unary_union

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# ---------------------------------------------------------------------------
# Paths / constants

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
OUT = ROOT / "data" / "maps" / "article"
OUT.mkdir(parents=True, exist_ok=True)

PATH_2019 = DATA / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
PATH_MAJ = DATA / "shapefiles" / "derived" / "v0_1_approximate_majority_2026_eds.gpkg"
PATH_MIN_V6 = DATA / "shapefiles" / "derived" / "v0_1_refined_v6_minority_2026_eds.gpkg"
# v7-derived gpkgs carry the FULL 89-ED partitioning with proper hybrid names
# (e.g. "Calgary-Peigan-Chestermere", "Lethbridge-Fort MacLeod-Crowsnest Pass",
# "Red Deer-Blackfalds"). They include some null-geometry rows for Tier-C EDs
# we couldn't transcribe from thumbnails; for those we fall back to the
# approximate_majority gpkg, then to 2019 crosswalk proxies.
PATH_MAJ_V7 = DATA / "shapefiles" / "derived" / "v0_1_derived_v7_majority_2026_eds.gpkg"
PATH_MIN_V7 = DATA / "shapefiles" / "derived" / "v0_1_derived_v7_minority_2026_eds.gpkg"
PATH_MAJ_XWALK = DATA / "v0_1_majority_full_crosswalk.csv"
PATH_MIN_XWALK = DATA / "v0_1_minority_full_crosswalk.csv"

CRS_PLOT = 3401  # NAD83 / Alberta 10-TM Forest, metres

# ---------------------------------------------------------------------------
# Palette - editorial, not political. Neutral base, warm highlight.

COLOR_BASE_URBAN = "#f0e4d0"        # warm ivory (slightly more saturated than ivory)
COLOR_BASE_RURAL = "#dcd4c4"        # cool ecru (darker than before for contrast)
COLOR_HIGHLIGHT = "#e87722"         # majority accent orange (for highlights)
COLOR_HIGHLIGHT_MIN = "#335c81"     # minority accent blue
COLOR_HIGHLIGHT_ALPHA = 0.78
COLOR_BASE_EDGE = "#2a2a2a"
COLOR_PROXY_HATCH = "///"            # hatch on Tier-C-proxied majority polys

EDGE_WIDTH = 1.1
EDGE_WIDTH_HIGHLIGHT = 1.8

# Fonts (use what's installed on Windows; Georgia is a workable Playfair-alike,
# DejaVu Sans is a workable Source Sans 3-alike).
FONT_TITLE_FAMILY = "Georgia"       # editorial serif
FONT_LABEL_FAMILY = "DejaVu Sans"   # ED names, credit line

# Decide whether an ED's polygon is rural-looking (>= 2000 km2) to pick a base
# shade. The intent is a soft visual difference between urban tiles and their
# rural surroundings, not a data encoding.
RURAL_AREA_THRESHOLD_M2 = 2e9  # 2000 km2

# Figure geometry - 1600 px wide at 300 dpi, taller than 900 so the map
# panels can be near-square.  The task spec suggested 1600x900 but that
# produces panels too squat for the Calgary/Lethbridge frames; a 4:3 figure
# (1600x1200) keeps each panel close to square and leaves headroom for the
# figure title on top and a 2-line credit at the bottom.
FIG_DPI = 300
FIG_W = 16.0 / 3.0          # 5.333 in = 1600 px at 300 dpi
FIG_H = 4.0                 # 1200 px at 300 dpi -> 4:3 aspect

# ---------------------------------------------------------------------------
# Figure specs
#
# Each spec lists the 2-3 EDs to highlight in each panel. Names must match
# the `name_2026` column of the respective gpkg (majority and minority v6).

@dataclass(frozen=True)
class FigSpec:
    slug: str
    region_title: str
    city_lonlat: tuple[float, float]
    half_width_km: float
    majority_highlights: tuple[str, ...]
    minority_highlights: tuple[str, ...]
    notes: str = ""


SPECS: list[FigSpec] = [
    FigSpec(
        slug="calgary",
        region_title="Calgary",
        city_lonlat=(-114.0719, 51.0447),
        half_width_km=42.0,
        # Majority: the four EDs that the article says "in the minority these
        # become..." - under the majority they stay as familiar regional names.
        majority_highlights=(
            "Airdrie-West",           # 2019: Airdrie-Cochrane
            "Chestermere-Strathmore", # identity
            "Calgary-West-Elbow Valley",
            "Calgary-Glenmore-Tsuut'ina",
        ),
        # Minority: the contested Calgary hybrids - these reach rural
        # territory into Calgary-named districts.
        minority_highlights=(
            "Calgary-Airdrie",              # from 2019 Airdrie-Cochrane
            "Calgary-Peigan-Chestermere",
            "Calgary-De Winton",
            "Calgary-West-Tsuut'ina",
        ),
        notes="commuter belt; 4 highlights each side",
    ),
    FigSpec(
        slug="airdrie",
        region_title="Airdrie",
        city_lonlat=(-114.0167, 51.2917),
        half_width_km=26.0,
        # Majority: the 2-way Airdrie split (Airdrie-East, Airdrie-West)
        majority_highlights=(
            "Airdrie-East",
            "Airdrie-West",
        ),
        # Minority: the (up to) 4-way Airdrie shred. Calgary-Peigan-Chestermere,
        # which the article body names, does not actually extend north of
        # Calgary in the v7 geometry - the Airdrie-adjacent districts are
        # Airdrie East, Calgary-Foothills-Airdrie West, Olds-Three Hills-
        # Didsbury, plus Chestermere-Strathmore on the east side.
        minority_highlights=(
            "Airdrie East",                      # note: no hyphen in v6/v7
            "Calgary-Foothills-Airdrie West",
            "Olds-Three Hills-Didsbury",
            "Chestermere-Strathmore",
        ),
        notes="2 vs 4 partition of the same commuter shed",
    ),
    FigSpec(
        slug="lethbridge",
        region_title="Lethbridge",
        city_lonlat=(-113.5, 49.75),       # shifted NW to include Crowsnest
        half_width_km=75.0,                 # wide: Crowsnest Pass to Cardston
        majority_highlights=(
            "Lethbridge-East",
            "Lethbridge-West",
        ),
        minority_highlights=(
            "Lethbridge-Cardston",
            "Lethbridge-Fort MacLeod-Crowsnest Pass",
            "Lethbridge-Little Bow",
            # The article body also mentions "Lethbridge-Taber-Warner" but the
            # v7 minority gpkg folds Taber-Warner into Lethbridge-Little Bow,
            # so only 3 Lethbridge-named hybrids appear here. Documented in
            # analysis/methodology/v0_1_overlay_figures_v2.md.
        ),
        notes="2 vs 3 partition; Taber-Warner folded into Little Bow in v7",
    ),
    FigSpec(
        slug="reddeer",
        region_title="Red Deer",
        city_lonlat=(-113.8117, 52.2681),
        half_width_km=32.0,
        majority_highlights=(
            "Red Deer-North",
            "Red Deer-South",
            "Lacombe-Clearwater",
            "Sylvan Lake-Innisfail",
        ),
        minority_highlights=(
            "Red Deer-Sylvan Lake",
            "Red Deer-Innisfail",
            "Red Deer-Blackfalds",
            "Red Deer-Lacombe",
        ),
        notes="2 compact seats + 2 regional seats VS 4 RD-named hybrids",
    ),
]


# Build a lookup from 2026 name -> 2019 parent ED name(s) for proxy use.
# Uses the full 88-row crosswalk. Any name_2026 we can't find a polygon for via
# the gpkgs falls back here.
def build_proxy_map(xwalk_path: Path) -> dict[str, list[str]]:
    xw = pd.read_csv(xwalk_path)
    out: dict[str, list[str]] = {}
    for _, row in xw.iterrows():
        p26 = str(row["proposed_2026"]).strip()
        c19 = str(row["current_2019"]).strip()
        if p26 == "nan" or c19 == "nan" or not p26 or not c19:
            continue
        out.setdefault(p26, []).append(c19)
    return out


# ---------------------------------------------------------------------------
# Loaders

def load_2019() -> gpd.GeoDataFrame:
    g = gpd.read_file(PATH_2019)
    if g.crs is None:
        g.set_crs(epsg=3401, inplace=True)
    return g.to_crs(CRS_PLOT)


def _has_valid_geom(geom) -> bool:
    return geom is not None and not geom.is_empty


def load_plan(primary_paths: list[Path],
              plan_label: str,
              xwalk_path: Path,
              g19: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Build a per-plan GeoDataFrame of 2026 EDs with `is_proxy` flag.

    Strategy (per ED name, in order):
      1. First primary gpkg that has a valid geometry for that name.
      2. Later primary gpkg that has a valid geometry for that name.
      3. 2019 proxy via the full crosswalk.

    `primary_paths` is ordered most-preferred to least-preferred. For majority
    we pass [v7_derived, approximate_majority]. For minority we pass
    [v7_derived, v6_refined].
    """
    # Start with the union of all names seen across primary files
    all_names: set[str] = set()
    loaded: list[gpd.GeoDataFrame] = []
    for path in primary_paths:
        if not path.exists():
            continue
        g = gpd.read_file(path).to_crs(CRS_PLOT)
        loaded.append(g)
        all_names |= set(g["name_2026"].tolist())

    # Also include any 2026 names from the crosswalk (full 87-ED partition)
    proxy_map = build_proxy_map(xwalk_path)
    all_names |= set(proxy_map.keys())

    g19_by_name = {str(r["EDName2017"]): r.geometry for _, r in g19.iterrows()}

    rows: list[dict] = []
    source_counts = {"primary": 0, "proxy": 0, "missing": 0}
    for name in sorted(all_names):
        geom = None
        source = None
        for g in loaded:
            sub = g[g["name_2026"] == name]
            if sub.empty:
                continue
            row_geom = sub.iloc[0].geometry
            if _has_valid_geom(row_geom):
                geom = row_geom
                source = "primary"
                break
        if geom is None:
            parents = proxy_map.get(name, [])
            polys = [g19_by_name[p] for p in parents if p in g19_by_name]
            if polys:
                geom = unary_union(polys)
                source = "proxy"
        if geom is None:
            source_counts["missing"] += 1
            continue

        source_counts[source] += 1
        rows.append({
            "name_2026": name,
            "is_proxy": (source == "proxy"),
            "source": source,
            "geometry": geom,
        })

    gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs=CRS_PLOT)
    print(f"  [{plan_label}] primary={source_counts['primary']} "
          f"proxy={source_counts['proxy']} missing={source_counts['missing']}")
    return gdf


def load_majority(g19: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return load_plan([PATH_MAJ_V7, PATH_MAJ], "majority", PATH_MAJ_XWALK, g19)


def load_minority(g19: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return load_plan([PATH_MIN_V7, PATH_MIN_V6], "minority", PATH_MIN_XWALK, g19)


# ---------------------------------------------------------------------------
# Geometry helpers

def lonlat_to_xy(lon: float, lat: float) -> tuple[float, float]:
    p = gpd.GeoSeries([Point(lon, lat)], crs=4326).to_crs(CRS_PLOT).iloc[0]
    return (p.x, p.y)


def bbox_around(lon: float, lat: float, half_km: float) -> tuple[float, float, float, float]:
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
    return sub[~sub.geometry.is_empty].reset_index(drop=True)


def base_fill_color(area_m2: float) -> str:
    return COLOR_BASE_RURAL if area_m2 >= RURAL_AREA_THRESHOLD_M2 else COLOR_BASE_URBAN


# ---------------------------------------------------------------------------
# Drawing helpers

def add_scale_bar(ax, x0, y0, length_km=10, height_m=400):
    length_m = length_km * 1000.0
    halo = mpatches.Rectangle(
        (x0 - length_m * 0.05, y0 - height_m * 1.0),
        length_m * 1.10, height_m * 3.8,
        linewidth=0, facecolor="white", alpha=0.85, zorder=4,
    )
    ax.add_patch(halo)
    bar = mpatches.Rectangle(
        (x0, y0), length_m, height_m,
        linewidth=0.7, edgecolor="black", facecolor="black", zorder=5,
    )
    ax.add_patch(bar)
    ax.text(
        x0 + length_m / 2, y0 + height_m * 1.8, f"{length_km} km",
        ha="center", va="bottom", fontsize=6.5, family=FONT_LABEL_FAMILY,
        zorder=6,
    )


def add_north_arrow(ax, x, y, size=1500):
    halo = mpatches.Circle(
        (x, y), radius=size * 1.3,
        linewidth=0, facecolor="white", alpha=0.85, zorder=4,
    )
    ax.add_patch(halo)
    ax.annotate(
        "N",
        xy=(x, y + size), xytext=(x, y - size),
        arrowprops=dict(facecolor="black", width=1.5, headwidth=6, headlength=7),
        ha="center", va="bottom",
        fontsize=8, fontweight="bold", family=FONT_LABEL_FAMILY,
        zorder=6,
    )


def label_ed(ax, geom, text, fontsize=7.5, weight="normal", color="#1a1a1a",
             bbox=None):
    try:
        pt = geom.representative_point()
    except Exception:
        return
    # Clamp label inside current axis limits so long names at frame edges
    # don't get clipped off the panel. We compute the expected label width in
    # map units by reading the *figure* dpi + axis position and combining
    # with fontsize.
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    fig = ax.get_figure()
    dpi = fig.get_dpi()
    fig_w_in, fig_h_in = fig.get_size_inches()
    ax_pos = ax.get_position()
    ax_w_in = ax_pos.width * fig_w_in
    ax_h_in = ax_pos.height * fig_h_in
    x_data_per_inch = (xmax - xmin) / max(ax_w_in, 0.01)
    y_data_per_inch = (ymax - ymin) / max(ax_h_in, 0.01)
    # Rough label width in inches: each char ~ 0.55 * fontsize pt, 72 pt/in.
    approx_label_w_in = len(text) * fontsize * 0.55 / 72.0
    approx_label_h_in = fontsize * 1.4 / 72.0
    mx_text = (approx_label_w_in / 2.0) * x_data_per_inch
    my_text = (approx_label_h_in / 2.0) * y_data_per_inch
    mx_base = (xmax - xmin) * 0.015
    my_base = (ymax - ymin) * 0.015
    mx = mx_base + mx_text
    my = my_base + my_text
    x = min(max(pt.x, xmin + mx), xmax - mx)
    y = min(max(pt.y, ymin + my), ymax - my)
    ax.annotate(
        text,
        xy=(x, y),
        ha="center", va="center",
        fontsize=fontsize, fontweight=weight, family=FONT_LABEL_FAMILY,
        color=color,
        bbox=bbox if bbox is not None else dict(
            boxstyle="round,pad=0.18",
            fc=(1, 1, 1, 0.88), ec="none"),
        zorder=9,
        clip_on=False,
    )


# ---------------------------------------------------------------------------
# Panel render

def render_panel(ax, gdf: gpd.GeoDataFrame, bbox, highlight_names: tuple[str, ...],
                 highlight_color: str, panel_title: str,
                 city_lonlat: tuple[float, float], primary_city_label: str,
                 scale_km: int, show_scale: bool, show_north: bool):
    minx, miny, maxx, maxy = bbox

    # Set limits early so label clamping works
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#bfbfbf")
        s.set_linewidth(0.5)

    # Background rectangle (very light frame color so any gap outside the
    # plan polygons reads as outside-the-partition)
    bg = mpatches.Rectangle(
        (minx, miny), maxx - minx, maxy - miny,
        facecolor="#fbf9f3", edgecolor="none", zorder=0,
    )
    ax.add_patch(bg)

    # Draw non-highlighted EDs first as neutral base
    highlight_set = set(highlight_names)
    highlighted_rows: list[tuple[str, object, bool]] = []
    if not gdf.empty:
        for _, row in gdf.iterrows():
            name = str(row.get("name_2026", ""))
            is_proxy = bool(row.get("is_proxy", False))
            if name in highlight_set:
                highlighted_rows.append((name, row.geometry, is_proxy))
                continue
            fill = base_fill_color(row.geometry.area)
            fill_patch = gpd.GeoSeries([row.geometry], crs=CRS_PLOT)
            fill_patch.plot(
                ax=ax, facecolor=fill, edgecolor="none",
                alpha=1.0, zorder=1,
            )
            if is_proxy:
                # light hatch to signal "approximate shape"
                fill_patch.plot(
                    ax=ax, facecolor="none", edgecolor="#c2a87a",
                    hatch="///", linewidth=0.0, alpha=0.55, zorder=2,
                )
            fill_patch.plot(
                ax=ax, facecolor="none", edgecolor=COLOR_BASE_EDGE,
                linewidth=EDGE_WIDTH, zorder=3,
            )

        # Then the highlighted EDs on top
        for name, geom, is_proxy in highlighted_rows:
            g_one = gpd.GeoSeries([geom], crs=CRS_PLOT)
            g_one.plot(
                ax=ax, facecolor=highlight_color, edgecolor="none",
                alpha=COLOR_HIGHLIGHT_ALPHA, zorder=4,
            )
            if is_proxy:
                g_one.plot(
                    ax=ax, facecolor="none", edgecolor="#2a2a2a",
                    hatch="///", linewidth=0.0, alpha=0.45, zorder=5,
                )
            g_one.plot(
                ax=ax, facecolor="none",
                edgecolor="#111111", linewidth=EDGE_WIDTH_HIGHLIGHT,
                zorder=6,
            )

    # City marker + label
    cx, cy = lonlat_to_xy(*city_lonlat)
    if minx <= cx <= maxx and miny <= cy <= maxy:
        ax.scatter([cx], [cy], s=32, color="black", zorder=7,
                   marker="o", edgecolor="white", linewidth=1.0)
        ax.annotate(
            primary_city_label.upper(),
            xy=(cx, cy),
            xytext=(7, 7), textcoords="offset points",
            fontsize=9, fontweight="bold", family=FONT_LABEL_FAMILY,
            color="#111111", zorder=10,
            bbox=dict(boxstyle="round,pad=0.22",
                      fc=(1, 1, 1, 0.9), ec="#111", linewidth=0.5),
        )

    # Scale bar (bottom-left) - only on left panel to save space
    if show_scale:
        sx = minx + (maxx - minx) * 0.04
        sy = miny + (maxy - miny) * 0.045
        add_scale_bar(ax, sx, sy, length_km=scale_km,
                      height_m=max(250, scale_km * 30))

    # North arrow (top-right) - only on right panel to save space
    if show_north:
        nx = minx + (maxx - minx) * 0.93
        ny = maxy - (maxy - miny) * 0.10
        add_north_arrow(ax, nx, ny, size=max(scale_km * 90, 800))

    # Panel title
    ax.set_title(panel_title, fontsize=11, fontweight="bold",
                 family=FONT_TITLE_FAMILY, color="#1a1a1a",
                 loc="left", pad=6)

    # Now label highlighted EDs (after the city marker, so labels can dodge
    # the city label by stepping off the representative point via clamp)
    for name, geom, _is_proxy in highlighted_rows:
        # Label font size scales with name length so long hybrid names fit
        fs = 7.0 if len(name) <= 22 else (6.3 if len(name) <= 32 else 5.7)
        label_ed(ax, geom, name, fontsize=fs, weight="bold",
                 color="#111111")


# ---------------------------------------------------------------------------
# Per-figure driver

def draw_figure(spec: FigSpec, maj: gpd.GeoDataFrame,
                mino: gpd.GeoDataFrame) -> dict:
    bbox = bbox_around(*spec.city_lonlat, spec.half_width_km)

    maj_c = clip_to_bbox(maj, bbox)
    min_c = clip_to_bbox(mino, bbox)

    # Check highlight name availability - warn if something's missing
    maj_have = set(maj_c["name_2026"]) if not maj_c.empty else set()
    min_have = set(min_c["name_2026"]) if not min_c.empty else set()
    missing_maj = [h for h in spec.majority_highlights if h not in maj_have]
    missing_min = [h for h in spec.minority_highlights if h not in min_have]
    if missing_maj:
        print(f"  [warn] {spec.slug}: majority highlights missing from frame: {missing_maj}")
    if missing_min:
        print(f"  [warn] {spec.slug}: minority highlights missing from frame: {missing_min}")

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=FIG_DPI)
    # Explicit axes placement: left band from (0.03 -> 0.49) wide, right band
    # from (0.51 -> 0.97). Vertical band from 0.09 (credit) to 0.84 (below
    # figure title).
    ax_l = fig.add_axes((0.03, 0.09, 0.46, 0.75))
    ax_r = fig.add_axes((0.51, 0.09, 0.46, 0.75))

    # Choose scale bar distance based on the half-width
    if spec.half_width_km >= 60:
        scale_km = 25
    elif spec.half_width_km >= 35:
        scale_km = 20
    elif spec.half_width_km >= 20:
        scale_km = 10
    else:
        scale_km = 5

    render_panel(
        ax=ax_l, gdf=maj_c, bbox=bbox,
        highlight_names=spec.majority_highlights,
        highlight_color=COLOR_HIGHLIGHT,
        panel_title="Majority proposal 2026",
        city_lonlat=spec.city_lonlat,
        primary_city_label=spec.region_title,
        scale_km=scale_km,
        show_scale=True,
        show_north=False,
    )
    render_panel(
        ax=ax_r, gdf=min_c, bbox=bbox,
        highlight_names=spec.minority_highlights,
        highlight_color=COLOR_HIGHLIGHT_MIN,
        panel_title="Minority proposal 2026",
        city_lonlat=spec.city_lonlat,
        primary_city_label=spec.region_title,
        scale_km=scale_km,
        show_scale=False,
        show_north=True,
    )

    # Figure-level title (above both panels) - large serif, left-aligned
    fig.text(
        0.035, 0.92,
        f"{spec.region_title} \u00b7 majority vs minority 2026",
        fontsize=15, fontweight="bold",
        family=FONT_TITLE_FAMILY, color="#0e0e0e",
        ha="left", va="baseline",
    )

    # 8pt muted-grey two-line credit at bottom-right
    fig.text(
        0.97, 0.015,
        "Approximate 2026 geometry pending shapefile release.\n"
        "Dimmed polygons in majority panel = 2019 shape used as Tier-C proxy.",
        ha="right", va="bottom",
        fontsize=7.0, family=FONT_LABEL_FAMILY, color="#6a6a6a",
        linespacing=1.3,
    )

    out_path = OUT / f"overlay_{spec.slug}_v2.png"
    fig.savefig(out_path, dpi=FIG_DPI,
                facecolor="white")
    plt.close(fig)

    n_maj_proxy = int(maj_c.get("is_proxy", pd.Series([], dtype=bool)).sum()) if not maj_c.empty else 0
    return {
        "slug": spec.slug,
        "path": str(out_path),
        "maj_visible": len(maj_c),
        "min_visible": len(min_c),
        "maj_proxy_visible": n_maj_proxy,
        "missing_maj_highlights": missing_maj,
        "missing_min_highlights": missing_min,
    }


def main() -> int:
    print("Loading geometry...")
    g19 = load_2019()
    maj = load_majority(g19)
    mino = load_minority(g19)
    print(f"  2019 n={len(g19)}  majority n={len(maj)}  minority n={len(mino)}")
    maj_proxy_names = sorted(maj[maj["is_proxy"] == True]["name_2026"].tolist())
    min_proxy_names = sorted(mino[mino["is_proxy"] == True]["name_2026"].tolist())
    print(f"  Majority proxied from 2019 ({len(maj_proxy_names)} EDs):")
    for n in maj_proxy_names:
        print(f"    - {n}")
    print(f"  Minority proxied from 2019 ({len(min_proxy_names)} EDs):")
    for n in min_proxy_names:
        print(f"    - {n}")

    results = []
    for spec in SPECS:
        print(f"\nDrawing {spec.slug}...")
        r = draw_figure(spec, maj, mino)
        print(f"  -> {r['path']}  (maj_visible={r['maj_visible']} "
              f"min_visible={r['min_visible']} maj_proxy_visible={r['maj_proxy_visible']})")
        results.append(r)

    print("\n=== SUMMARY ===")
    for r in results:
        print(f"{r['slug']:12s}  {r['path']}")
        print(f"  maj_visible={r['maj_visible']} min_visible={r['min_visible']} "
              f"maj_proxy_visible={r['maj_proxy_visible']}")
        if r["missing_maj_highlights"]:
            print(f"  missing_maj_highlights={r['missing_maj_highlights']}")
        if r["missing_min_highlights"]:
            print(f"  missing_min_highlights={r['missing_min_highlights']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
