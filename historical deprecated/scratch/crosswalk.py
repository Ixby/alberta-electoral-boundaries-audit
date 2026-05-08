import warnings
import geopandas as gpd
import pandas as pd
from pathlib import Path

# Suppress warnings for clean output
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


def run_crosswalk():
    print("Loading geographic data...")
    eds_2019 = gpd.read_file(EDS_2019_PATH).to_crs(3401)
    name_col_2019 = [c for c in eds_2019.columns if "name" in c.lower()]
    name_col_2019 = name_col_2019[0] if name_col_2019 else eds_2019.columns[0]
    eds_2019 = eds_2019[[name_col_2019, "geometry"]].rename(
        columns={name_col_2019: "name_2019"}
    )

    eds_min = gpd.read_file(EDS_MIN_PATH).to_crs(3401)
    name_col_2026 = [c for c in eds_min.columns if "name" in c.lower()][0]
    eds_min = eds_min[[name_col_2026, "geometry"]].rename(
        columns={name_col_2026: "name_2026"}
    )

    va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
    va_pts = gpd.GeoDataFrame(
        {"va_ucp": va["va_ucp"].fillna(0), "va_ndp": va["va_ndp"].fillna(0)},
        geometry=va.geometry.centroid,
        crs=3401,
    )

    print("Computing geometric intersections (The Pairwise Table)...")
    # Spatial Crosswalk
    crosswalk = gpd.overlay(eds_2019, eds_min, how="intersection")

    # Drop microscopic slivers caused by border digitization differences
    crosswalk["area_m2"] = crosswalk.geometry.area
    crosswalk = crosswalk[crosswalk["area_m2"] > 100000].copy()  # > 0.1 sq km
    crosswalk["slice_id"] = range(len(crosswalk))

    print("Attributing 2023 voting blocks to the intersection slices...")
    joined = gpd.sjoin(
        va_pts, crosswalk[["slice_id", "geometry"]], how="inner", predicate="within"
    )

    # Aggregate votes by slice
    slice_votes = (
        joined.groupby("slice_id")
        .agg(ucp_votes=("va_ucp", "sum"), ndp_votes=("va_ndp", "sum"))
        .reset_index()
    )

    crosswalk = crosswalk.merge(slice_votes, on="slice_id", how="left").fillna(0)
    crosswalk["total_votes"] = crosswalk["ucp_votes"] + crosswalk["ndp_votes"]

    # Filter slices that actually contain a meaningful number of people
    crosswalk = crosswalk[crosswalk["total_votes"] > 2000].copy()

    # 1. DETECT CRACKING (A single 2019 district shattered into many pieces)
    print("\n=======================================================")
    print("DETECTING CRACKING (Major 2019 Districts Shattered)")
    print("=======================================================")

    # Find 2019 districts that were split into the most meaningful chunks
    splits = crosswalk.groupby("name_2019").size()
    cracked_candidates = splits[splits >= 3].index

    for district in cracked_candidates:
        slices = crosswalk[crosswalk["name_2019"] == district].sort_values(
            "total_votes", ascending=False
        )
        total_d_votes = slices["total_votes"].sum()
        if total_d_votes < 10000:  # Lowered threshold to ensure we catch districts
            continue

        print(
            f"\n[CRACKING] {district.upper()} was shattered into {len(slices)} pieces:"
        )
        for _, row in slices.iterrows():
            winner = "NDP" if row["ndp_votes"] > row["ucp_votes"] else "UCP"
            print(
                f"  -> {row['total_votes']:,.0f} votes sent to [2026] {row['name_2026']} (Leans {winner})"
            )

    # 2. DETECT DRAINING / HYBRIDIZATION (Urban chunks swallowed by rural districts)
    print("\n=======================================================")
    print("DETECTING DRAINING (Urban Slices Attached to Rural)")
    print("=======================================================")
    # Look for slices that came from high-density 2019 districts but got assigned to massive 2026 districts
    # We can approximate this by looking at the area of the 2026 parent district
    eds_min["area_2026"] = eds_min.geometry.area
    cw_with_area = crosswalk.merge(eds_min[["name_2026", "area_2026"]], on="name_2026")

    # Find slices with high vote density (lots of votes, small slice area) that ended up in massive 2026 districts
    cw_with_area["slice_density"] = (
        cw_with_area["total_votes"] / cw_with_area["area_m2"]
    )

    # Sort by extreme hybrid mismatch: very dense slice, very large parent district
    cw_with_area["hybrid_score"] = (
        cw_with_area["slice_density"] * cw_with_area["area_2026"]
    )
    drains = cw_with_area.sort_values("hybrid_score", ascending=False).head(5)

    for _, row in drains.iterrows():
        print(f"\n[URBAN DRAIN DETECTED]:")
        print(
            f"  -> A dense chunk of [2019] {row['name_2019']} ({row['total_votes']:,.0f} votes)"
        )
        print(f"  -> Was swallowed by the massive [2026] {row['name_2026']}")
        margin = row["ndp_votes"] - row["ucp_votes"]
        lean = "NDP" if margin > 0 else "UCP"
        print(
            f"  -> This effectively drained a +{abs(margin):,.0f} {lean} advantage into a rural periphery."
        )

    # 3. DETECT PACKING (Combining multiple chunks to form a vote sink)
    print("\n=======================================================")
    print("DETECTING PACKING (Vote Sinks Formed from Multiple 2019 Chunks)")
    print("=======================================================")

    # Calculate 2026 district vote totals and margins
    districts_2026 = (
        crosswalk.groupby("name_2026")
        .agg(
            total_votes=("total_votes", "sum"),
            ucp_votes=("ucp_votes", "sum"),
            ndp_votes=("ndp_votes", "sum"),
            num_2019_sources=("name_2019", "nunique"),
        )
        .reset_index()
    )

    # Find extreme vote sinks (e.g., >68% vote share for one party)
    districts_2026["ucp_share"] = (
        districts_2026["ucp_votes"] / districts_2026["total_votes"]
    )
    districts_2026["ndp_share"] = (
        districts_2026["ndp_votes"] / districts_2026["total_votes"]
    )

    # Filter for packed districts assembled from multiple (>=2) meaningful sources
    packed = (
        districts_2026[
            (districts_2026["num_2019_sources"] >= 2)
            & (
                (districts_2026["ucp_share"] > 0.62)
                | (districts_2026["ndp_share"] > 0.62)
            )
            & (districts_2026["total_votes"] > 15000)
        ]
        .sort_values("num_2019_sources", ascending=False)
        .head(5)
    )

    for _, row in packed.iterrows():
        winner = "NDP" if row["ndp_share"] > 0.5 else "UCP"
        share = max(row["ndp_share"], row["ucp_share"]) * 100
        print(
            f"\n[PACKING] [2026] {row['name_2026'].upper()} is a {winner} Vote Sink ({share:.1f}%)."
        )
        print(
            f"  -> It was assembled by harvesting {row['num_2019_sources']} different 2019 districts:"
        )

        pieces = crosswalk[crosswalk["name_2026"] == row["name_2026"]].sort_values(
            "total_votes", ascending=False
        )
        for _, piece in pieces.iterrows():
            if piece["total_votes"] > 1000:  # Only show meaningful chunks
                print(
                    f"     - Pulled {piece['total_votes']:,.0f} votes from [2019] {piece['name_2019']}"
                )


if __name__ == "__main__":
    run_crosswalk()
