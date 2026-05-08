# Version: v0.9
from __future__ import annotations
"""
airdrie_quadrant_anchoring.py — Airdrie quadrant teardown
==============================================================
Counter to the "Highway Anchoring Defense" — the hostile-witness counter that
says the minority commission did not abandon anchoring, it merely substituted
Section 14(d) (highways and transportation) for Section 14(b) (municipalities)
when carving Airdrie. The province-wide natural-anchoring secondary check
(commit 6a39960, `natural_anchoring_secondary_check.md`) confirms that
on a province-wide basis the three maps anchor to highways+rivers at
near-identical rates (~38-40 %), so the 14.5 % CSD-anchoring deficit alone
cannot prove the highway substitution was malicious.

This script tests the malice question on the audit's strongest local case:
the Airdrie carve. Airdrie is one CSD (City of Airdrie, CSDUID=4806021,
2021 census population ~73,800; 2024 estimate ~84,000) and qualifies for
~2 EDs at the provincial average (54,929). The minority cuts it 4 ways; the
majority cuts it 3 ways but concentrates ~74 % of Airdrie residents inside a
single ED (Airdrie-East). For each ED that contains Airdrie territory we
compute four perimeter / population metrics:

  1. % of ED perimeter that follows Airdrie's CSD boundary (within snap
     tolerance of 500 m — same tolerance as the headline anchoring runs).
  2. % of ED perimeter that follows a major OSM highway (motorway / trunk /
     primary / secondary — same classes as score_natural_anchoring.py).
  3. % of ED perimeter that follows neither (the "free" perimeter, i.e.
     lines drawn by the commission that don't trace either anchor).
  4. # of Airdrie CSD residents (population proxy = sum of va_ndp + va_ucp +
     va_other for VAs whose centroid falls inside both the ED polygon and
     the Airdrie CSD polygon).

The hypothesis tested by the metrics: minority lines ENTER Airdrie via
highways but DON'T EXIT via the city limit. They cross the city diagonally
rather than tracing it. If true, the minority EDs that touch Airdrie should
show a lower city-limit anchoring share *combined with* a substantial
free-perimeter share that runs through residential mass.

The script also produces a two-panel teardown PNG at 300 DPI.

CLI:
    python analysis/scripts/airdrie_quadrant_anchoring.py

Outputs:
    data/airdrie_quadrant_anchoring.csv
    data/maps/airdrie_4way_teardown.svg

Forward:
    analysis/reports/airdrie_highway_pretext.md
Backward:
    analysis/scripts/score_anchoring.py            (CSD anchoring formula)
    analysis/scripts/score_natural_anchoring.py    (highway anchoring formula)
    data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg
    data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg
    data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
    data/shapefiles/reference/alberta_2021_csds.gpkg
    data/osm/alberta_osm_highways.gpkg
"""

# Version: 0.9 (2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import warnings
from pathlib import Path

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from shapely.geometry import LinearRing, LineString, MultiLineString, Point
from shapely.ops import linemerge, unary_union
from shapely.strtree import STRtree

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
SHP_DERIVED = DATA / "shapefiles" / "derived"
SHP_REF = DATA / "shapefiles" / "reference"
OSM_DIR = DATA / "osm"
MAPS_DIR = DATA / "maps"

V0_9_MIN_GPKG = SHP_DERIVED / "v0_10_topological_minority_2026_eds.gpkg"
V0_9_MAJ_GPKG = SHP_DERIVED / "v0_10_topological_majority_2026_eds.gpkg"
VA_GPKG = SHP_DERIVED / "va_polygons_with_2023_votes.gpkg"
CSD_GPKG = SHP_REF / "alberta_2021_csds.gpkg"
HIGHWAYS_GPKG = OSM_DIR / "alberta_osm_highways.gpkg"

OUT_CSV = DATA / "airdrie_quadrant_anchoring.csv"
OUT_PNG = MAPS_DIR / "airdrie_4way_teardown.svg"

# Match the audit's headline anchoring tolerances (score_anchoring.py)
SNAP_TOL_M: float = 500.0
VERTEX_DENSIFY_M: float = 50.0

WORK_CRS = 3401  # NAD83 / Alberta 10-TM Forest (metres)

# Airdrie CSD population threshold to count an ED as "containing Airdrie"
MIN_AIRDRIE_VA_POP = 100.0

# Hand-picked label positions for the major highways the minority's quadrant
# lines appear to track through Airdrie. Coordinates are EPSG:3401, in metres.
# Derived from OSM "ref" tags + manual placement near segment midpoints inside
# the study window. Format: (label, (x, y), rotation_degrees).
HIGHWAY_LABELS = [
    ("Hwy 2 (QE2)", (69475, 5688189), 90),
    ("Hwy 567", (76738, 5681447), 0),
    ("Hwy 566", (74613, 5671737), 0),
    ("Hwy 791", (81735, 5687644), 90),
    ("Hwy 72", (83857, 5691265), 0),
    ("Hwy 2A", (68765, 5685900), 90),
]


# ---------------------------------------------------------------------------
# Anchoring measurement (lifted from score_anchoring.py / score_natural_anchoring.py)
# ---------------------------------------------------------------------------


def _normalise_edges(edges) -> MultiLineString:
    if edges.geom_type == "MultiLineString":
        edges = linemerge(edges)
    if edges.geom_type == "LineString":
        edges = MultiLineString([edges])
    if edges.geom_type == "GeometryCollection":
        ls = [
            g for g in edges.geoms if g.geom_type in ("LineString", "MultiLineString")
        ]
        edges = unary_union(ls)
    if edges.geom_type == "LineString":
        edges = MultiLineString([edges])
    return edges


def _densify(ring: LinearRing, step: float) -> list[tuple[float, float]]:
    line = LineString(ring.coords)
    L = line.length
    if L <= 0:
        return list(ring.coords)
    n = max(int(np.ceil(L / step)), 8)
    ds = np.linspace(0.0, L, n + 1)[:-1]
    return [(line.interpolate(d).x, line.interpolate(d).y) for d in ds]


def _build_tree(edges: MultiLineString):
    edge_lines = []
    if edges.geom_type == "MultiLineString":
        edge_lines.extend(list(edges.geoms))
    elif edges.geom_type == "LineString":
        edge_lines.append(edges)
    else:
        for g in getattr(edges, "geoms", [edges]):
            if g.geom_type == "LineString":
                edge_lines.append(g)
            elif g.geom_type == "MultiLineString":
                edge_lines.extend(list(g.geoms))
    if not edge_lines:
        return [], None
    tree = STRtree(edge_lines)
    return edge_lines, tree


def _measure_ring_multi(
    ring: LinearRing,
    edge_substrates: list[tuple[str, list, "STRtree"]],
    snap_tol: float,
) -> dict:
    """Walk a ring and tag each segment by which substrate(s) it snaps to.

    Returns total perimeter and per-substrate anchored length, plus the
    "neither" (free) length. A segment counts toward a substrate if BOTH
    endpoints are within snap_tol of that substrate. If a segment matches
    multiple substrates, it's allocated to the first by priority order
    (CSD before highway here, so a stretch that follows both gets attributed
    to CSD anchoring, since CSD is the more specific anchor)."""
    coords = _densify(ring, VERTEX_DENSIFY_M)
    if len(coords) < 4:
        coords = list(ring.coords)

    # Snap-flag each vertex against each substrate
    n_sub = len(edge_substrates)
    flags = [[False] * n_sub for _ in range(len(coords))]
    for i, (x, y) in enumerate(coords):
        p = Point(x, y)
        buf = p.buffer(snap_tol)
        for s_idx, (_, edge_lines, tree) in enumerate(edge_substrates):
            if tree is None or not edge_lines:
                continue
            cand_idxs = tree.query(buf)
            if len(cand_idxs) == 0:
                continue
            best = snap_tol + 1.0
            for idx in cand_idxs:
                edge = edge_lines[int(idx)]
                np_pt = edge.interpolate(edge.project(p))
                d = p.distance(np_pt)
                if d < best:
                    best = d
            if best <= snap_tol:
                flags[i][s_idx] = True

    perim = 0.0
    anchored = [0.0] * n_sub
    free = 0.0
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        seg = float(np.hypot(x2 - x1, y2 - y1))
        perim += seg

        # Segment counts as anchored to substrate s if both endpoints flagged.
        attributed = False
        for s_idx in range(n_sub):
            if flags[i][s_idx] and flags[(i + 1) % len(coords)][s_idx]:
                anchored[s_idx] += seg
                attributed = True
                break  # attribute to first-matching substrate by priority
        if not attributed:
            free += seg
    return {"perim_m": perim, "anchored_m": anchored, "free_m": free}


def measure_ed_anchoring(
    ed_geom,
    edge_substrates: list[tuple[str, list, "STRtree"]],
) -> dict:
    if ed_geom is None or ed_geom.is_empty:
        return {
            "perim_m": 0.0,
            "anchored_m": [0.0] * len(edge_substrates),
            "free_m": 0.0,
        }
    if ed_geom.geom_type == "MultiPolygon":
        parts = list(ed_geom.geoms)
    elif ed_geom.geom_type == "Polygon":
        parts = [ed_geom]
    else:
        parts = [s for s in getattr(ed_geom, "geoms", []) if s.geom_type == "Polygon"]
    perim = 0.0
    anchored = [0.0] * len(edge_substrates)
    free = 0.0
    for poly in parts:
        r = _measure_ring_multi(poly.exterior, edge_substrates, SNAP_TOL_M)
        perim += r["perim_m"]
        free += r["free_m"]
        for s_idx in range(len(edge_substrates)):
            anchored[s_idx] += r["anchored_m"][s_idx]
        for hole in poly.interiors:
            r = _measure_ring_multi(hole, edge_substrates, SNAP_TOL_M)
            perim += r["perim_m"]
            free += r["free_m"]
            for s_idx in range(len(edge_substrates)):
                anchored[s_idx] += r["anchored_m"][s_idx]
    return {"perim_m": perim, "anchored_m": anchored, "free_m": free}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_inputs():
    print("Loading inputs...")
    minority = gpd.read_file(V0_9_MIN_GPKG).to_crs(epsg=WORK_CRS)
    majority = gpd.read_file(V0_9_MAJ_GPKG).to_crs(epsg=WORK_CRS)
    csds = gpd.read_file(CSD_GPKG).to_crs(epsg=WORK_CRS)
    vas = gpd.read_file(VA_GPKG).to_crs(epsg=WORK_CRS)
    highways = gpd.read_file(HIGHWAYS_GPKG).to_crs(epsg=WORK_CRS)
    airdrie_csd = csds[csds["CSDNAME"] == "Airdrie"].iloc[0].geometry
    print(f"  minority EDs:  {len(minority)}")
    print(f"  majority EDs:  {len(majority)}")
    print(f"  highways:      {len(highways):,} ways")
    print(f"  VAs:           {len(vas):,}")
    print(f"  Airdrie CSD:   {airdrie_csd.area / 1e6:.2f} km^2")
    return minority, majority, csds, vas, highways, airdrie_csd


def airdrie_population_per_ed(
    eds: gpd.GeoDataFrame, vas: gpd.GeoDataFrame, airdrie_csd
) -> pd.DataFrame:
    """Sum 2023-vote-proxy population for VAs whose centroid is inside both
    the ED and the Airdrie CSD."""
    vas = vas.copy()
    vas["pop_proxy"] = (
        vas["va_ndp"].fillna(0) + vas["va_ucp"].fillna(0) + vas["va_other"].fillna(0)
    )
    cents = vas.geometry.centroid
    vas_c = gpd.GeoDataFrame(
        vas[["VA_NUMBER", "pop_proxy"]].copy(), geometry=cents, crs=vas.crs
    )
    in_csd = vas_c[vas_c.geometry.within(airdrie_csd)]
    joined = gpd.sjoin(
        in_csd, eds[["name_2026", "geometry"]], predicate="within", how="left"
    )
    grouped = (
        joined.groupby("name_2026")["pop_proxy"].agg(["sum", "count"]).reset_index()
    )
    grouped = grouped.rename(
        columns={"sum": "airdrie_pop_proxy", "count": "airdrie_va_count"}
    )
    return grouped


def build_substrates(airdrie_csd, highways: gpd.GeoDataFrame, study_bbox):
    """Build (label, edge_lines, STRtree) tuples for each substrate.

    Order matters — when a segment matches multiple substrates we attribute
    to the first. We put CSD first because city-limit anchoring is the more
    specific defense (a segment that follows the city limit AND happens to
    lie next to a highway should count toward city-limit anchoring)."""

    # Substrate 1: Airdrie CSD boundary (a single ring)
    csd_edges_geom = _normalise_edges(airdrie_csd.boundary)

    # Substrate 2: major OSM highways near Airdrie. Filter to study bbox + buffer
    # to keep tree small and fast.
    minx, miny, maxx, maxy = study_bbox
    buffer_m = 5_000.0  # 5 km buffer
    hw_clip = highways.cx[
        minx - buffer_m : maxx + buffer_m, miny - buffer_m : maxy + buffer_m
    ]
    print(
        f"  highways in study area: {len(hw_clip):,} ways "
        f"(filtered from {len(highways):,})"
    )
    hw_geom = unary_union(list(hw_clip.geometry))
    hw_geom = _normalise_edges(hw_geom)

    csd_lines, csd_tree = _build_tree(csd_edges_geom)
    hw_lines, hw_tree = _build_tree(hw_geom)
    print(f"  CSD edge LineStrings:     {len(csd_lines):,}")
    print(f"  highway LineStrings:      {len(hw_lines):,}")
    return [
        ("city_limit", csd_lines, csd_tree),
        ("highway", hw_lines, hw_tree),
    ]


# ---------------------------------------------------------------------------
# Main metrics build
# ---------------------------------------------------------------------------


def build_metrics(eds, label, airdrie_csd, substrates, vas):
    """Per-ED city-limit %, highway %, neither %, Airdrie population proxy."""
    pop_df = airdrie_population_per_ed(eds, vas, airdrie_csd)

    # Identify EDs that contain Airdrie territory (population proxy > threshold)
    airdrie_eds = pop_df[pop_df["airdrie_pop_proxy"] >= MIN_AIRDRIE_VA_POP]
    print(
        f"\n  [{label}] EDs containing Airdrie territory (pop_proxy >= {MIN_AIRDRIE_VA_POP}):"
    )
    for _, r in airdrie_eds.sort_values(
        "airdrie_pop_proxy", ascending=False
    ).iterrows():
        print(
            f"    {r['name_2026']:<40s} pop_proxy={r['airdrie_pop_proxy']:8.0f}  "
            f"VAs={r['airdrie_va_count']}"
        )

    # Total Airdrie pop_proxy for share calculations
    total_airdrie_pop = airdrie_eds["airdrie_pop_proxy"].sum()

    rows = []
    for _, r in airdrie_eds.iterrows():
        ed_name = r["name_2026"]
        ed_row = eds[eds["name_2026"] == ed_name].iloc[0]
        m = measure_ed_anchoring(ed_row.geometry, substrates)
        perim = m["perim_m"]
        city_m = m["anchored_m"][0]
        hw_m = m["anchored_m"][1]
        free_m = m["free_m"]
        rows.append(
            {
                "map": label,
                "name_2026": ed_name,
                "perimeter_km": perim / 1000.0,
                "city_limit_km": city_m / 1000.0,
                "highway_km": hw_m / 1000.0,
                "neither_km": free_m / 1000.0,
                "city_limit_pct": 100.0 * city_m / perim if perim else 0.0,
                "highway_pct": 100.0 * hw_m / perim if perim else 0.0,
                "neither_pct": 100.0 * free_m / perim if perim else 0.0,
                "airdrie_pop_proxy": float(r["airdrie_pop_proxy"]),
                "airdrie_va_count": int(r["airdrie_va_count"]),
                "airdrie_pop_share_of_csd": (
                    100.0 * r["airdrie_pop_proxy"] / total_airdrie_pop
                    if total_airdrie_pop
                    else 0.0
                ),
            }
        )
    df = pd.DataFrame(rows).sort_values("airdrie_pop_proxy", ascending=False)
    return df


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------


def render_teardown(
    minority,
    majority,
    airdrie_csd,
    highways,
    vas,
    minority_metrics: pd.DataFrame,
    majority_metrics: pd.DataFrame,
):
    """Two-panel side-by-side: majority cut vs minority cut.

    Layers per panel:
      1. Airdrie CSD polygon (light fill, thick black outline)
      2. ED polygons clipped to a focus window, coloured by ED
      3. Major highways (bold dark line)
      4. VA centroids weighted by population (size = pop_proxy)
      5. ED labels
    """
    print("\nRendering teardown PNG...")

    # Build study bbox: Airdrie CSD + 12 km buffer
    minx, miny, maxx, maxy = airdrie_csd.bounds
    buf_m = 12_000.0
    study_bounds = (minx - buf_m, miny - buf_m, maxx + buf_m, maxy + buf_m)
    sx_min, sy_min, sx_max, sy_max = study_bounds

    # Restrict layers to study window
    hw_clip = highways.cx[sx_min:sx_max, sy_min:sy_max]
    # Filter to major highway classes
    if "highway" in hw_clip.columns:
        hw_clip = hw_clip[
            hw_clip["highway"].isin(["motorway", "trunk", "primary", "secondary"])
        ]
    print(f"  highways in plot: {len(hw_clip):,}")

    # VA centroids inside Airdrie CSD with pop proxy
    vas2 = vas.copy()
    vas2["pop_proxy"] = (
        vas2["va_ndp"].fillna(0) + vas2["va_ucp"].fillna(0) + vas2["va_other"].fillna(0)
    )
    vas2["centroid"] = vas2.geometry.centroid
    vas_c = gpd.GeoDataFrame(
        vas2[["pop_proxy", "centroid"]], geometry="centroid", crs=vas.crs
    )
    vas_in = vas_c[vas_c.geometry.within(airdrie_csd)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 9), dpi=300)

    # Distinct color palettes per panel — pick from tab20 / Set2
    maj_palette = plt.cm.Set2(np.linspace(0, 1, max(len(majority_metrics), 3)))
    min_palette = plt.cm.tab10(np.linspace(0, 1, max(len(minority_metrics), 4)))

    panel_specs = [
        (
            "Majority: 3-way carve\n(74% of Airdrie in 1 ED)",
            axes[0],
            majority,
            majority_metrics,
            maj_palette,
        ),
        (
            "Minority: 4-way carve\n(no ED holds majority of Airdrie)",
            axes[1],
            minority,
            minority_metrics,
            min_palette,
        ),
    ]

    for title, ax, eds_gdf, metrics, palette in panel_specs:
        ax.set_xlim(sx_min, sx_max)
        ax.set_ylim(sy_min, sy_max)
        ax.set_aspect("equal")

        # ED fills (only the EDs that touch Airdrie). Fill across full ED, but
        # the bbox window crops to local view.
        ed_handles = []
        for i, (_, r) in enumerate(metrics.iterrows()):
            ed_name = r["name_2026"]
            ed_geom = eds_gdf[eds_gdf["name_2026"] == ed_name].geometry.iloc[0]
            color = palette[i % len(palette)]
            gpd.GeoSeries([ed_geom], crs=eds_gdf.crs).plot(
                ax=ax,
                facecolor=color,
                edgecolor="black",
                linewidth=1.6,
                alpha=0.45,
                zorder=1,
            )
            # Place label at centroid of ED-clipped-to-view
            ed_clip = ed_geom.intersection(
                gpd.GeoSeries([airdrie_csd.buffer(buf_m * 0.7)], crs=eds_gdf.crs).iloc[
                    0
                ]
            )
            if ed_clip and not ed_clip.is_empty:
                cen = ed_clip.centroid
                short_name = ed_name.replace("Calgary-", "C-").replace("-Airdrie", "-A")
                ax.annotate(
                    short_name,
                    xy=(cen.x, cen.y),
                    fontsize=8.5,
                    fontweight="bold",
                    ha="center",
                    va="center",
                    color="black",
                    bbox=dict(
                        boxstyle="round,pad=0.25", fc=color, ec="black", alpha=0.85
                    ),
                    zorder=5,
                )
            ed_handles.append(mpatches.Patch(color=color, alpha=0.6, label=ed_name))

        # Airdrie CSD — drawn ON TOP of EDs, filled lightly
        gpd.GeoSeries([airdrie_csd], crs=eds_gdf.crs).plot(
            ax=ax,
            facecolor="none",
            edgecolor="black",
            linewidth=2.8,
            zorder=4,
        )

        # Major highways (bold dark line)
        if len(hw_clip) > 0:
            hw_clip.plot(ax=ax, color="#222222", linewidth=1.5, zorder=3)

        # VA centroids weighted by population (residential mass markers)
        if len(vas_in) > 0:
            sizes = (
                vas_in["pop_proxy"] / vas_in["pop_proxy"].max() * 60.0 + 5.0
            ).values
            xs = [g.x for g in vas_in.geometry]
            ys = [g.y for g in vas_in.geometry]
            ax.scatter(
                xs,
                ys,
                s=sizes,
                c="#cc1111",
                alpha=0.55,
                edgecolor="white",
                linewidth=0.4,
                zorder=6,
                label="Voters (size = 2023 pop)",
            )

        # Highway labels — hand-placed at known coordinates around Airdrie.
        # These labels are the major highways the minority's quadrant lines
        # appear to track through the CSD. Coordinates are EPSG:3401.
        for label, (lx, ly), rot in HIGHWAY_LABELS:
            if not (sx_min <= lx <= sx_max and sy_min <= ly <= sy_max):
                continue
            ax.annotate(
                label,
                xy=(lx, ly),
                rotation=rot,
                fontsize=8,
                color="white",
                fontweight="bold",
                ha="center",
                va="center",
                bbox=dict(
                    boxstyle="round,pad=0.22",
                    fc="#222222",
                    ec="white",
                    linewidth=0.6,
                    alpha=0.92,
                ),
                zorder=8,
            )

        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])

        # Legend per panel
        ax.legend(
            handles=ed_handles
            + [
                Line2D(
                    [0], [0], color="black", linewidth=2.6, label="Airdrie city limit"
                ),
                Line2D([0], [0], color="#222222", linewidth=1.5, label="Major highway"),
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor="#cc1111",
                    markersize=8,
                    alpha=0.7,
                    label="Residential VAs",
                ),
            ],
            loc="lower left",
            fontsize=7,
            framealpha=0.9,
        )

    fig.suptitle(
        "How Airdrie was cut: city limits vs. four-way carve",
        fontsize=15,
        fontweight="bold",
        y=0.985,
    )
    fig.text(
        0.5,
        0.948,
        "v0_9 substrate; ED polygons coloured by district. "
        "Airdrie CSD outlined in heavy black. Highways: OSM motorway/trunk/primary/secondary.",
        ha="center",
        fontsize=9,
        color="#333333",
    )
    fig.text(
        0.5,
        0.012,
        "Source: Statistics Canada 2021 CSDs; OSM highways (Apr 2026 Overpass pull); "
        "v0_9 topological ED polygons; 2023 provincial VA results as residential proxy. "
        "Metrics: data/airdrie_quadrant_anchoring.csv.",
        ha="center",
        fontsize=7,
        color="#444444",
    )
    plt.tight_layout(rect=[0, 0.025, 1, 0.92])
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  wrote: {OUT_PNG}")


def main():
    print("=" * 72)
    print("v0_9 Airdrie quadrant anchoring teardown")
    print("=" * 72)

    minority, majority, csds, vas, highways, airdrie_csd = load_inputs()

    # Build study bbox for highway filtering: Airdrie CSD + 15 km buffer
    minx, miny, maxx, maxy = airdrie_csd.bounds
    study_bbox = (minx - 15_000, miny - 15_000, maxx + 15_000, maxy + 15_000)

    print("\nBuilding edge substrates (city-limit + highway, study area only)...")
    substrates = build_substrates(airdrie_csd, highways, study_bbox)

    print("\n=== MINORITY METRICS ===")
    minority_metrics = build_metrics(
        minority, "minority_2026", airdrie_csd, substrates, vas
    )
    print(minority_metrics.drop(columns=["map"]).to_string(index=False))

    print("\n=== MAJORITY METRICS ===")
    majority_metrics = build_metrics(
        majority, "majority_2026", airdrie_csd, substrates, vas
    )
    print(majority_metrics.drop(columns=["map"]).to_string(index=False))

    out = pd.concat([majority_metrics, minority_metrics], ignore_index=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False, float_format="%.3f")
    print(f"\nwrote: {OUT_CSV} ({len(out)} rows)")

    render_teardown(
        minority,
        majority,
        airdrie_csd,
        highways,
        vas,
        minority_metrics,
        majority_metrics,
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
