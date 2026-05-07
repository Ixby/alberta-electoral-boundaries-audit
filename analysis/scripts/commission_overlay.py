"""
v0_1_commission_overlay.py

Visual compliance verification: overlay v0_8 (or v0_7 fallback) ED boundary
lines on top of the commission's high-resolution PNG maps. Produces two output
types per map:

  1. side_by_side — our polygons (left) | commission PNG (right), same region.
     No georeferencing required. Good for "does the overall shape match?"
  2. overlay — our boundary lines drawn on top of the commission PNG using
     estimated geographic extents. Requires calibration (see MAP_SPECS below).

Inputs:
  data/maps/hires/*.svg
  data/shapefiles/derived/v0_1_derived_v8_majority_2026_eds.gpkg  (v0_7 fallback)
  data/shapefiles/derived/v0_1_derived_v8_minority_2026_eds.gpkg  (v0_7 fallback)

Outputs:
  data/maps/verification/v0_8_commission_sidebyside_<slug>.svg
  data/maps/verification/v0_8_commission_overlay_<slug>.svg

Dependencies:
  Forward:  data/maps/hires/*.svg,
            data/shapefiles/derived/v0_1_derived_v8_*_2026_eds.gpkg
  Backward: data/maps/verification/v0_8_commission_*.svg
"""

# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image
from shapely.geometry import box, Point


def _ts():
    return time.strftime("%H:%M:%S")


# ---------------------------------------------------------------------------
# Paths

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
HIRES = DATA / "maps" / "hires"
OUT = DATA / "maps" / "verification"
OUT.mkdir(parents=True, exist_ok=True)

CRS_PLOT = 3401  # NAD83 / Alberta 10-TM Forest (metres, no false easting)


def _gpkg(version_label: str, plan: str) -> Path:
    p = DATA / "shapefiles" / "derived" / f"v0_10_topological_{plan}_2026_eds.gpkg"
    if not p.exists():
        raise FileNotFoundError(f"v0_10 gpkg not found for {plan}: {p}")
    return p


# ---------------------------------------------------------------------------
# Geographic extents in EPSG:3401 metres
# Computed from city centres + provincial boundary bounds.
#
# Alberta total bounds (from v0_7): x=[-329156, 365134], y=[5425575, 6659344]
# City centres (EPSG:3401):
#   Calgary  x=65035  y=5652943
#   Edmonton x=99758  y=5931703
#   Red Deer x=80810  y=5789201
#   Lethbridge x=156169 y=5504836
#   Grande Prairie x=-241666 y=6117928
#   Fort McMurray  x=221351  y=6290297
#
# CALIBRATION: if the overlay looks shifted, adjust the extent tuple.
# The (xmin, xmax, ymin, ymax) defines the geographic area shown in the image
# INCLUDING any margins, title bars, and legend areas.  Shrink xmin/ymin or
# grow xmax/ymax to move our lines left/down; do the opposite to move them
# right/up.


@dataclass
class MapSpec:
    png: str  # filename in data/maps/hires/
    slug: str  # output slug
    plan: str  # "majority" or "minority"
    label: str  # human-readable title
    extent: tuple[float, float, float, float]  # (xmin, xmax, ymin, ymax) EPSG:3401


AB = (-329156, 365134, 5425575, 6659344)  # full Alberta


def _city_box(cx: float, cy: float, r_km: float):
    r = r_km * 1000
    return (cx - r, cx + r, cy - r, cy + r)


MAP_SPECS: list[MapSpec] = [
    # --- Majority ---
    # Report page layout: MAP_r600 file appears BEFORE the text page for the same region.
    # p71: province overview text page (has small inset maps, not a full map page)
    # p72: Calgary full map (600 DPI) — precedes the Calgary ED list on p73
    # p73: Calgary ED list text page
    # p74: Edmonton full map (600 DPI) — precedes the Edmonton ED list on p75
    # p75: Edmonton ED list text page
    # p76: Near Calgary full map (600 DPI) — precedes near-Calgary text on p77
    # p77: Near Calgary text page
    # p79: Near Edmonton text/map page
    # p81, p83, p85: North / Central / South region maps
    MapSpec(
        "v0_1_majority_p71_alberta_overview.svg",
        "majority_overview_p71",
        "majority",
        "Overview text — Majority",
        AB,
    ),
    MapSpec(
        "v0_1_majority_p72_MAP_r600.svg",
        "majority_calgary_map_p72",
        "majority",
        "Calgary MAP — Majority",
        _city_box(65035, 5652943, 65),
    ),
    MapSpec(
        "v0_1_majority_p73_calgary.svg",
        "majority_calgary_text_p73",
        "majority",
        "Calgary text — Majority",
        _city_box(65035, 5652943, 65),
    ),
    MapSpec(
        "v0_1_majority_p74_MAP_r600.svg",
        "majority_edmonton_map_p74",
        "majority",
        "Edmonton MAP — Majority",
        _city_box(99758, 5931703, 65),
    ),
    MapSpec(
        "v0_1_majority_p75_edmonton.svg",
        "majority_edmonton_text_p75",
        "majority",
        "Edmonton text — Majority",
        _city_box(99758, 5931703, 65),
    ),
    MapSpec(
        "v0_1_majority_p76_MAP_r600.svg",
        "majority_near_calgary_map_p76",
        "majority",
        "Near Calgary MAP — Majority",
        _city_box(65035, 5652943, 140),
    ),
    MapSpec(
        "v0_1_majority_p77_near_calgary.svg",
        "majority_near_calgary_text_p77",
        "majority",
        "Near Calgary text — Majority",
        _city_box(65035, 5652943, 140),
    ),
    MapSpec(
        "v0_1_majority_p79_near_edmonton.svg",
        "majority_near_edmonton_p79",
        "majority",
        "Near Edmonton — Majority",
        _city_box(99758, 5931703, 140),
    ),
    MapSpec(
        "v0_1_majority_p81_north.svg",
        "majority_north_p81",
        "majority",
        "North — Majority",
        (AB[0], AB[1], 6150000, AB[3]),
    ),
    MapSpec(
        "v0_1_majority_p83_central.svg",
        "majority_central_p83",
        "majority",
        "Central — Majority",
        (AB[0], AB[1], 5780000, 6200000),
    ),
    MapSpec(
        "v0_1_majority_p85_south.svg",
        "majority_south_p85",
        "majority",
        "South — Majority",
        (AB[0], AB[1], AB[2], 5810000),
    ),
    # --- Minority ---
    # p359 (map73): full Alberta province overview (minority)
    # p360 (map74): Edmonton detail map
    # p361 (map75): Near Calgary region (landscape 6601×5100)
    # p362 (map76): multi-panel summary page (9 smaller maps — overlay not meaningful)
    MapSpec(
        "v0_1_minority_p359_map73.svg",
        "minority_overview_p359",
        "minority",
        "Alberta Overview — Minority",
        AB,
    ),
    MapSpec(
        "v0_1_minority_p360_map74.svg",
        "minority_edmonton_p360",
        "minority",
        "Edmonton — Minority",
        _city_box(99758, 5931703, 65),
    ),
    MapSpec(
        "v0_1_minority_p361_map75.svg",
        "minority_near_calgary_p361",
        "minority",
        "Near Calgary — Minority",
        _city_box(65035, 5652943, 140),
    ),
    MapSpec(
        "v0_1_minority_p362_map76.svg",
        "minority_summary_p362",
        "minority",
        "Summary (multi-panel) — Minority",
        AB,
    ),  # 9-panel page; overlay is approximate
]

# ---------------------------------------------------------------------------
# Helpers

BOUNDARY_COLOR = "#d62728"  # red — high contrast on commission maps
BOUNDARY_LW = 1.5
LABEL_FS = 6.0


def load_png(path: Path) -> np.ndarray:
    """Load PNG, convert palette/RGBA modes to RGB numpy array."""
    img = Image.open(path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    return np.asarray(img)


def load_plan(plan: str) -> gpd.GeoDataFrame:
    path = _gpkg("auto", plan)
    g = gpd.read_file(path)
    if g.crs is None:
        g = g.set_crs(epsg=CRS_PLOT)
    g = g.to_crs(CRS_PLOT)
    # Ensure a name column exists
    for col in ("name_2026", "ED_Name", "ed_name", "name"):
        if col in g.columns:
            g = g.rename(columns={col: "_name"}) if col != "_name" else g
            break
    if "_name" not in g.columns:
        g["_name"] = g.index.astype(str)
    g = g[g.geometry.notna() & ~g.geometry.is_empty].copy()
    return g


def clip_plan(g: gpd.GeoDataFrame, extent: tuple) -> gpd.GeoDataFrame:
    xmin, xmax, ymin, ymax = extent
    mask = box(xmin, ymin, xmax, ymax)
    sub = g[g.geometry.intersects(mask)].copy()
    if sub.empty:
        return sub
    sub = sub.copy()
    sub["geometry"] = sub.geometry.intersection(mask)
    return sub[~sub.geometry.is_empty].reset_index(drop=True)


def render_our_map(ax, gdf: gpd.GeoDataFrame, extent: tuple, title: str):
    xmin, xmax, ymin, ymax = extent
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_facecolor("#f4f1eb")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#aaaaaa")
        s.set_linewidth(0.5)
    ax.set_title(title, fontsize=9, color="#1a1a1a", loc="left", pad=4)
    if not gdf.empty:
        gdf.plot(
            ax=ax, facecolor="#dcd4c4", edgecolor="#2a2a2a", linewidth=0.8, zorder=1
        )
        # Label each ED at representative point
        for _, row in gdf.iterrows():
            try:
                pt = row.geometry.representative_point()
                if xmin < pt.x < xmax and ymin < pt.y < ymax:
                    ax.text(
                        pt.x,
                        pt.y,
                        row["_name"],
                        ha="center",
                        va="center",
                        fontsize=LABEL_FS,
                        color="#111111",
                        clip_on=True,
                        bbox=dict(
                            boxstyle="round,pad=0.1", fc=(1, 1, 1, 0.7), ec="none"
                        ),
                    )
            except Exception:
                pass


def render_overlay(
    ax,
    img: np.ndarray,
    gdf: gpd.GeoDataFrame,
    extent: tuple,
    title: str,
    png_wh: tuple[int, int],
):
    """Draw commission PNG with our boundary lines on top.

    The image pixel origin is top-left; imshow extent is [xmin,xmax,ymin,ymax]
    with ymin at bottom.  PIL/numpy images have row 0 at the TOP, so we flip
    the y-axis via origin='upper' (imshow default) — no manual flip needed.
    """
    xmin, xmax, ymin, ymax = extent

    # imshow expects [left, right, bottom, top]
    ax.imshow(
        img,
        extent=[xmin, xmax, ymin, ymax],
        aspect="auto",
        interpolation="lanczos",
        alpha=0.85,
        zorder=0,
    )
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#aaaaaa")
        s.set_linewidth(0.5)
    ax.set_title(title, fontsize=9, color="#1a1a1a", loc="left", pad=4)

    if not gdf.empty:
        # Only draw boundaries, not fills — let the commission map show through
        gdf.boundary.plot(ax=ax, color=BOUNDARY_COLOR, linewidth=BOUNDARY_LW, zorder=2)


# ---------------------------------------------------------------------------
# Per-spec driver


def process_spec(
    spec: MapSpec, plans: dict[str, gpd.GeoDataFrame], out_dir: Path
) -> dict:
    png_path = HIRES / spec.svg
    if not png_path.exists():
        print(f"  [skip] {spec.svg} not found")
        return {"slug": spec.slug, "skipped": True}

    t_spec = time.time()
    img = load_png(png_path)
    h, w = img.shape[:2]

    gdf_full = plans.get(spec.plan, gpd.GeoDataFrame())
    gdf = clip_plan(gdf_full, spec.extent)

    _src = str(_gpkg("auto", spec.plan))
    version_label = "v0_8" if ("v8" in _src or "canonical" in _src) else "v0_7"

    # --- 1. Side-by-side ---
    fig, (ax_our, ax_com) = plt.subplots(1, 2, figsize=(16, 10), dpi=150)
    render_our_map(
        ax_our, gdf, spec.extent, f"Our {version_label} boundaries\n({spec.label})"
    )
    # Commission PNG on the right — just show it as-is (no georef needed)
    ax_com.imshow(img, aspect="auto", interpolation="lanczos")
    ax_com.set_xticks([])
    ax_com.set_yticks([])
    ax_com.set_title(
        f"Commission map\n({spec.svg})", fontsize=9, color="#1a1a1a", loc="left", pad=4
    )
    for s in ax_com.spines.values():
        s.set_color("#aaaaaa")
        s.set_linewidth(0.5)
    fig.suptitle(spec.label, fontsize=13, fontweight="bold", y=0.97)
    fig.text(
        0.5,
        0.01,
        f"Left: {version_label} derived boundaries  ·  Right: commission source map  "
        f"·  Visual compliance check — boundaries should match in shape and position",
        ha="center",
        va="bottom",
        fontsize=7,
        color="#666666",
    )
    sb_path = out_dir / f"v0_8_commission_sidebyside_{spec.slug}.svg"
    fig.savefig(sb_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # --- 2. Overlay ---
    fig2, ax_ov = plt.subplots(1, 1, figsize=(10, 13), dpi=150)
    render_overlay(
        ax_ov,
        img,
        gdf,
        spec.extent,
        f"{spec.label}\n{version_label} boundaries (red) on commission map",
        (w, h),
    )
    fig2.text(
        0.5,
        0.01,
        "CALIBRATION NOTE: extents are estimated. "
        "If boundary lines appear shifted, adjust the 'extent' in MAP_SPECS for this map.",
        ha="center",
        va="bottom",
        fontsize=7,
        color="#884444",
        style="italic",
    )
    ov_path = out_dir / f"v0_8_commission_overlay_{spec.slug}.svg"
    fig2.savefig(ov_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig2)

    print(
        f"  [{_ts()}] [{spec.slug}] {len(gdf)} EDs visible "
        f"({time.time()-t_spec:.1f}s)  →  {sb_path.name}, {ov_path.name}",
        flush=True,
    )
    return {
        "slug": spec.slug,
        "n_eds": len(gdf),
        "sidebyside": str(sb_path),
        "overlay": str(ov_path),
    }


# ---------------------------------------------------------------------------
# Main


def main() -> int:
    t_start = time.time()
    print(f"[{_ts()}] [commission overlay] START", flush=True)
    print("Loading plans...")
    plans: dict[str, gpd.GeoDataFrame] = {}
    for plan in ("majority", "minority"):
        try:
            plans[plan] = load_plan(plan)
            src = _gpkg("auto", plan).name
            print(f"  {plan}: {len(plans[plan])} EDs from {src}")
        except FileNotFoundError as e:
            print(f"  [warn] {e}")
            plans[plan] = gpd.GeoDataFrame()

    results = []
    print(f"[{_ts()}] processing {len(MAP_SPECS)} commission map specs", flush=True)
    for spec in MAP_SPECS:
        print(f"\n{spec.label}")
        r = process_spec(spec, plans, OUT)
        results.append(r)

    print("\n=== SUMMARY ===")
    produced = [r for r in results if not r.get("skipped")]
    skipped = [r for r in results if r.get("skipped")]
    print(f"  Produced: {len(produced)}  Skipped: {len(skipped)}")
    for r in produced:
        print(f"  {r['slug']:45s}  EDs={r['n_eds']}")
    if skipped:
        print("  Skipped:", [r["slug"] for r in skipped])

    print(f"\nOutputs in: {OUT}")
    print("\nTo calibrate overlays:")
    print(
        "  1. Open v0_8_commission_sidebyside_*.svg — visually confirm boundary shapes match"
    )
    print(
        "  2. Open v0_8_commission_overlay_*.svg — if lines are shifted, adjust the 'extent'"
    )
    print(
        "     in MAP_SPECS. Move xmin left / xmax right to stretch horizontally, etc."
    )
    print(
        f"\n[{_ts()}] [commission overlay] DONE — total {time.time()-t_start:.2f}s",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
