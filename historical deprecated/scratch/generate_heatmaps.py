import sys
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from shapely.geometry import Point

ROOT = Path(
    "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
)
VA_VOTES_PATH = (
    ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
)
SCRATCH_DIR = ROOT / "scratch"


def build_heatmap(map_path, out_file, name_col_guess="name_2026"):
    print(f"Building heatmap for {map_path.name}")
    eds = gpd.read_file(map_path).to_crs(3401)

    # Try to find the name column
    name_col = name_col_guess if name_col_guess in eds.columns else eds.columns[0]
    # Handle the 2019 shapefile which has ED_NAME
    if "ED_NAME" in eds.columns:
        name_col = "ED_NAME"

    eds = eds[eds.geometry.area > 1e6].copy().reset_index(drop=True)

    va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
    va_pts = gpd.GeoDataFrame(
        {"va_ucp": va["va_ucp"].fillna(0), "va_ndp": va["va_ndp"].fillna(0)},
        geometry=va.geometry.centroid,
        crs=3401,
    )

    joined = gpd.sjoin(
        va_pts, eds[[name_col, "geometry"]], how="left", predicate="within"
    )
    agg = (
        joined.groupby(name_col)
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    agg["total"] = (agg["ucp"] + agg["ndp"]).clip(lower=1)
    agg["ucp_share"] = agg["ucp"] / agg["total"]

    eds = eds.merge(agg[[name_col, "ucp_share", "total"]], on=name_col, how="left")
    eds["ucp_share"] = eds["ucp_share"].fillna(0.5)
    eds["total"] = eds["total"].fillna(0)

    # Nearest K fallback for missing EDs
    K = 25
    still_missing = eds["total"] == 0
    if still_missing.any():
        va_centroids = list(
            zip(
                va.geometry.centroid.x.values,
                va.geometry.centroid.y.values,
                va["va_ucp"].fillna(0).values,
                va["va_ndp"].fillna(0).values,
            )
        )
        for idx in eds.index[still_missing]:
            gc = eds.at[idx, "geometry"].centroid
            dists = [
                (((cx - gc.x) ** 2 + (cy - gc.y) ** 2), u, n)
                for cx, cy, u, n in va_centroids
            ]
            dists.sort(key=lambda t: t[0])
            near = dists[:K]
            ucp_sum = float(sum(u for _, u, _ in near))
            ndp_sum = float(sum(n for _, _, n in near))
            if (ucp_sum + ndp_sum) > 0:
                eds.at[idx, "ucp_share"] = ucp_sum / (ucp_sum + ndp_sum)

    # Rendering setup
    ndp_orange = (0.92, 0.45, 0.10)
    ucp_blue = (0.13, 0.36, 0.62)
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "ucp_ndp_direct", [ndp_orange, ucp_blue], N=256
    )
    norm = mcolors.Normalize(vmin=0.30, vmax=0.80, clip=True)

    cover_ivory = "#cccccc"
    fig, ax = plt.subplots(figsize=(6.0, 9), dpi=300)
    fig.patch.set_facecolor(cover_ivory)
    ax.set_facecolor(cover_ivory)
    ax.set_aspect("equal")
    ax.axis("off")

    va_render = va.copy()
    va_ucp_total = va_render["va_ucp"].fillna(0)
    va_ndp_total = va_render["va_ndp"].fillna(0)
    va_two_party = (va_ucp_total + va_ndp_total).clip(lower=1.0)
    va_render["parent_ucp_share"] = va_ucp_total / va_two_party

    if "pop_2021" in va_render.columns:
        pop = va_render["pop_2021"].fillna(0).clip(lower=0)
    else:
        pop = va_two_party + va_render.get(
            "va_other", pd.Series(0, index=va_render.index)
        ).fillna(0)

    area_m2 = va_render.geometry.area.clip(lower=1.0)
    density = pop / area_m2
    log_d = np.log10(density.replace(0, np.nan)).fillna(-12.0)
    d_min, d_max = -8.0, -3.0
    weight = ((log_d - d_min) / (d_max - d_min)).clip(0.10, 1.0)

    ivory_rgb = np.array(mcolors.to_rgb(cover_ivory))

    def _va_fill(ucp_share, w):
        base = np.array(cmap(norm(ucp_share)))[:3]
        if w < 0.5:
            t = w / 0.5
            blended = (1 - t) * ivory_rgb + t * base
        else:
            t = (w - 0.5) / 0.5
            dark = 0.30 * base
            blended = (1 - t) * base + t * dark
        return mcolors.to_hex(blended)

    va_render["_fill"] = [
        _va_fill(s, w) for s, w in zip(va_render["parent_ucp_share"], weight.values)
    ]
    eds["_base_fill"] = [_va_fill(s, 0.20) for s in eds["ucp_share"]]

    eds.plot(ax=ax, color=eds["_base_fill"].tolist(), linewidth=0)
    va_render.plot(ax=ax, color=va_render["_fill"].tolist(), linewidth=0)
    eds.boundary.plot(ax=ax, edgecolor="#1a1a1a", linewidth=0.20)

    # Fix topological slivers by buffering geometries by 1 meter before dissolving
    province = eds.copy()
    province.geometry = province.geometry.buffer(1)
    province = province.dissolve()
    province.boundary.plot(ax=ax, edgecolor="#7a1f1f", linewidth=0.65)

    ax.margins(0.005)
    plt.tight_layout(pad=0)
    plt.savefig(
        out_file,
        format="svg",
        bbox_inches="tight",
        pad_inches=0.02,
        facecolor=cover_ivory,
    )
    plt.close(fig)
    print(f"Saved {out_file.name}")


if __name__ == "__main__":
    maj_path = (
        ROOT
        / "data"
        / "shapefiles"
        / "derived"
        / "v0_10_topological_majority_2026_eds.gpkg"
    )
    build_heatmap(maj_path, SCRATCH_DIR / "majority_heatmap.svg")

    min_path = (
        ROOT
        / "data"
        / "shapefiles"
        / "derived"
        / "v0_10_topological_minority_2026_eds.gpkg"
    )
    build_heatmap(min_path, SCRATCH_DIR / "minority_heatmap.svg")

    # Let's see if we have the 2019 gpkg, or use shp
    eds_2019 = (
        ROOT
        / "data"
        / "shapefiles"
        / "reference"
        / "alberta_2019_eds"
        / "EDS_ENACTED_BILL33_15DEC2017.shp"
    )
    if not eds_2019.exists():
        # Fallback to searching
        files = list((ROOT / "data").rglob("*2019*.shp")) + list(
            (ROOT / "data").rglob("*2019*.gpkg")
        )
        if files:
            eds_2019 = files[0]

    build_heatmap(eds_2019, SCRATCH_DIR / "2019_heatmap.svg")
