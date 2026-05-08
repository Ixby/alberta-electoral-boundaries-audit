import warnings
import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(
    "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
)
VA_VOTES_PATH = (
    ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
)
EDS_2019_PATH = (
    ROOT
    / "data"
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)
EDS_MIN_PATH = (
    ROOT
    / "data"
    / "shapefiles"
    / "derived"
    / "v0_10_topological_minority_2026_eds.gpkg"
)
EDS_MAJ_PATH = (
    ROOT
    / "data"
    / "shapefiles"
    / "derived"
    / "v0_10_topological_majority_2026_eds.gpkg"
)
PROOFS_DIR = ROOT / "scratch" / "proofs"

os.makedirs(PROOFS_DIR, exist_ok=True)


def load_data():
    eds_2019 = gpd.read_file(EDS_2019_PATH).to_crs(3401)
    name_col = (
        [c for c in eds_2019.columns if "name" in c.lower()][0]
        if [c for c in eds_2019.columns if "name" in c.lower()]
        else eds_2019.columns[0]
    )
    eds_2019 = eds_2019[[name_col, "geometry"]].rename(columns={name_col: "name"})
    eds_2019["name"] = eds_2019["name"].str.upper().str.strip()

    eds_min = gpd.read_file(EDS_MIN_PATH).to_crs(3401)
    name_col = [c for c in eds_min.columns if "name" in c.lower()][0]
    eds_min = eds_min[[name_col, "geometry"]].rename(columns={name_col: "name"})
    eds_min["name"] = eds_min["name"].str.upper().str.strip()

    eds_maj = gpd.read_file(EDS_MAJ_PATH).to_crs(3401)
    name_col = [c for c in eds_maj.columns if "name" in c.lower()][0]
    eds_maj = eds_maj[[name_col, "geometry"]].rename(columns={name_col: "name"})
    eds_maj["name"] = eds_maj["name"].str.upper().str.strip()

    va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
    va_pts = gpd.GeoDataFrame(
        {"va_ucp": va["va_ucp"].fillna(0), "va_ndp": va["va_ndp"].fillna(0)},
        geometry=va.geometry.centroid,
        crs=3401,
    )
    return eds_2019, eds_min, eds_maj, va_pts


def get_events(eds_2019, eds_2026, va_pts, map_label):
    crosswalk = gpd.overlay(
        eds_2019.rename(columns={"name": "name_2019"}),
        eds_2026.rename(columns={"name": "name_2026"}),
        how="intersection",
    )
    crosswalk["area_m2"] = crosswalk.geometry.area
    crosswalk = crosswalk[crosswalk["area_m2"] > 100000].copy()
    crosswalk["slice_id"] = range(len(crosswalk))

    joined = gpd.sjoin(
        va_pts, crosswalk[["slice_id", "geometry"]], how="inner", predicate="within"
    )
    slice_votes = (
        joined.groupby("slice_id")
        .agg(ucp_votes=("va_ucp", "sum"), ndp_votes=("va_ndp", "sum"))
        .reset_index()
    )
    crosswalk = crosswalk.merge(slice_votes, on="slice_id", how="left").fillna(0)
    crosswalk["total_votes"] = crosswalk["ucp_votes"] + crosswalk["ndp_votes"]
    crosswalk = crosswalk[crosswalk["total_votes"] > 2000].copy()

    events = []

    # 1. Cracking
    splits = crosswalk.groupby("name_2019").size()
    cracked = splits[splits >= 3].index
    for district in cracked:
        slices = crosswalk[crosswalk["name_2019"] == district]
        if slices["total_votes"].sum() >= 10000:
            events.append(
                {
                    "type": "Cracking",
                    "map_label": map_label,
                    "target_2019": district,
                    "pieces": slices["name_2026"].tolist(),
                }
            )

    # 2. Packing
    districts_2026 = (
        crosswalk.groupby("name_2026")
        .agg(
            total_votes=("total_votes", "sum"),
            ucp=("ucp_votes", "sum"),
            ndp=("ndp_votes", "sum"),
            sources=("name_2019", "nunique"),
        )
        .reset_index()
    )

    for _, row in districts_2026.iterrows():
        if row["total_votes"] < 15000:
            continue
        margin = max(row["ucp"] / row["total_votes"], row["ndp"] / row["total_votes"])
        if row["sources"] >= 2 and margin > 0.62:
            donor_slices = crosswalk[crosswalk["name_2026"] == row["name_2026"]]
            donors = donor_slices[donor_slices["total_votes"] > 1000][
                "name_2019"
            ].tolist()
            events.append(
                {
                    "type": "Packing",
                    "map_label": map_label,
                    "target_2026": row["name_2026"],
                    "donors": donors,
                }
            )

    # 3. Draining
    eds_2026["area_2026"] = eds_2026.geometry.area
    cw_area = crosswalk.merge(
        eds_2026[["name", "area_2026"]].rename(columns={"name": "name_2026"}),
        on="name_2026",
    )
    cw_area["density"] = cw_area["total_votes"] / cw_area["area_m2"]
    cw_area["score"] = cw_area["density"] * cw_area["area_2026"]
    drains = cw_area.sort_values("score", ascending=False).head(5)
    for _, row in drains.iterrows():
        events.append(
            {
                "type": "Draining",
                "map_label": map_label,
                "target_2019": row["name_2019"],
                "recipient_2026": row["name_2026"],
            }
        )

    return events


def render_event(event, eds_2019, eds_2026):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 10))
    fig.patch.set_facecolor("white")
    for ax in [ax1, ax2, ax3]:
        ax.axis("off")

    etype = event["type"]
    mlabel = event["map_label"]

    # Identify bounding boxes to show surrounding morphology
    if etype == "Cracking" or etype == "Draining":
        target_poly = eds_2019[eds_2019["name"] == event["target_2019"]].geometry.iloc[
            0
        ]
        title_target = event["target_2019"]
    else:  # Packing
        target_poly = eds_2026[eds_2026["name"] == event["target_2026"]].geometry.iloc[
            0
        ]
        title_target = event["target_2026"]

    bbox = target_poly.buffer(20000)  # 20km buffer for morphology context

    # Subplot 1: 2019 Context
    ax1.set_title("1. 2019 Baseline Morphology", fontsize=20, weight="bold")
    context_2019 = eds_2019[eds_2019.intersects(bbox)]
    context_2019.plot(ax=ax1, facecolor="#eeeeee", edgecolor="white", linewidth=1)

    if etype == "Packing":
        # Highlight donors
        donors = eds_2019[eds_2019["name"].isin(event["donors"])]
        donors.plot(ax=ax1, facecolor="#ffcccc", edgecolor="red", linewidth=2)
    else:
        # Highlight target
        target = eds_2019[eds_2019["name"] == title_target]
        target.plot(ax=ax1, facecolor="#cce5ff", edgecolor="blue", linewidth=2)

    ax1.set_xlim(bbox.bounds[0], bbox.bounds[2])
    ax1.set_ylim(bbox.bounds[1], bbox.bounds[3])

    # Subplot 2: The Overlay Effect
    ax2.set_title(
        f"2. Overlay ({etype} Effect)", fontsize=20, weight="bold", color="purple"
    )
    context_2019.plot(ax=ax2, facecolor="#f9f9f9", edgecolor="lightgray", linewidth=1)

    if etype == "Cracking":
        target = eds_2019[eds_2019["name"] == title_target]
        target.plot(ax=ax2, facecolor="#cce5ff", edgecolor="blue", linewidth=2)
        cutters = eds_2026[eds_2026["name"].isin(event["pieces"])]
        gpd.clip(cutters, target).plot(
            ax=ax2, facecolor="none", edgecolor="black", linewidth=4, linestyle="--"
        )
    elif etype == "Draining":
        target = eds_2019[eds_2019["name"] == title_target]
        target.plot(ax=ax2, facecolor="#cce5ff", edgecolor="blue", linewidth=2)
        swallower = eds_2026[eds_2026["name"] == event["recipient_2026"]]
        gpd.clip(swallower, target).plot(
            ax=ax2, facecolor="#ffcc99", edgecolor="orange", linewidth=4, hatch="///"
        )
        swallower.plot(
            ax=ax2, facecolor="none", edgecolor="orange", linewidth=3, linestyle="-."
        )
    elif etype == "Packing":
        donors = eds_2019[eds_2019["name"].isin(event["donors"])]
        donors.plot(ax=ax2, facecolor="#ffcccc", edgecolor="red", linewidth=2)
        sink = eds_2026[eds_2026["name"] == title_target]
        sink.plot(
            ax=ax2, facecolor="none", edgecolor="black", linewidth=4, linestyle="--"
        )

    ax2.set_xlim(bbox.bounds[0], bbox.bounds[2])
    ax2.set_ylim(bbox.bounds[1], bbox.bounds[3])

    # Subplot 3: Resultant 2026
    ax3.set_title(f"3. 2026 {mlabel} Result", fontsize=20, weight="bold")
    context_2026 = eds_2026[eds_2026.intersects(bbox)]
    context_2026.plot(ax=ax3, facecolor="#eeeeee", edgecolor="white", linewidth=1)

    if etype == "Cracking":
        cutters = eds_2026[eds_2026["name"].isin(event["pieces"])]
        cutters.plot(ax=ax3, facecolor="#e5ccff", edgecolor="purple", linewidth=2)
    elif etype == "Draining":
        swallower = eds_2026[eds_2026["name"] == event["recipient_2026"]]
        swallower.plot(ax=ax3, facecolor="#ffcc99", edgecolor="orange", linewidth=2)
    elif etype == "Packing":
        sink = eds_2026[eds_2026["name"] == title_target]
        sink.plot(ax=ax3, facecolor="#a6e3a1", edgecolor="green", linewidth=3)

    ax3.set_xlim(bbox.bounds[0], bbox.bounds[2])
    ax3.set_ylim(bbox.bounds[1], bbox.bounds[3])

    clean_title = f"{mlabel}_{etype}_{title_target.replace(' ', '_').replace('/', '_')}"
    fig.suptitle(
        f"Geometric Proof: {etype} of {title_target} ({mlabel} Map)",
        fontsize=26,
        weight="bold",
        y=1.05,
    )

    plt.tight_layout()
    outpath = PROOFS_DIR / f"{clean_title}.svg"
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Generated proof: {outpath.name}")


if __name__ == "__main__":
    print("Loading data...")
    eds_2019, eds_min, eds_maj, va_pts = load_data()

    print("Analyzing Minority Map events...")
    min_events = get_events(eds_2019, eds_min, va_pts, "Minority")

    print("Analyzing Majority Map events...")
    maj_events = get_events(eds_2019, eds_maj, va_pts, "Majority")

    all_events = min_events + maj_events

    # Deduplicate events (same type, same target, same map)
    seen = set()
    unique_events = []
    for e in all_events:
        target = e.get("target_2019") or e.get("target_2026")
        key = f"{e['map_label']}_{e['type']}_{target}"
        if key not in seen:
            seen.add(key)
            unique_events.append(e)

    print(f"Found {len(unique_events)} distinct geometric events across both maps.")
    for e in unique_events:
        m = eds_min if e["map_label"] == "Minority" else eds_maj
        render_event(e, eds_2019, m)

    print("Done!")
