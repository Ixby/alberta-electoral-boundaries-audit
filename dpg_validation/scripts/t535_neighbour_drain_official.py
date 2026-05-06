"""
§5.3.5 — Neighbour-Drain Adjacency Test on Official Geometry

Re-runs the pre-registered neighbour-drain test from the original audit
using official Elections Alberta shapefiles instead of DPG geometry.

Test logic (unchanged from audit):
  A "chain signal" exists when:
    ED X has losing-party surplus >= 0.15 (packed)
    AND adjacent ED Y has winning margin <= 0.05 (cracked)
  A "coupled chain signal" requires the losing party in X = losing party in Y.

Pre-registered pass criterion: minority coupled count <= 1.5x majority coupled count.

Audit v0_8 result: minority 4, majority 3 (ratio 1.33x) -> PASS

This script asks: does that PASS hold when adjacency is derived from official
geometry rather than the DPG?
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

VA_PATH  = REPO / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
OFF_MAJ  = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN  = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
OUT      = ROOT / "outputs/t535_neighbour_drain_official.csv"
OUT.parent.mkdir(exist_ok=True)

TOUCH_THRESHOLD  = 50    # metres — shared boundary >= this to count as adjacent
SURPLUS_THRESH   = 0.15  # losing-party surplus threshold for "packed"
MARGIN_THRESH    = 0.05  # winning margin threshold for "cracked"
PASS_RATIO       = 1.5   # pre-registered: minority/majority coupled count <= this

# Original audit result (v0_8 substrate) for comparison
AUDIT_COUPLED = {"majority": 3, "minority": 4}


def build_adjacency(gdf, name_col, threshold=TOUCH_THRESHOLD):
    """Return frozenset of frozenset pairs for EDs sharing >= threshold m boundary."""
    gdf = gdf.to_crs("EPSG:3400").copy()
    gdf["_name"] = gdf[name_col].str.strip()
    edges = set()
    n = len(gdf)
    for i in range(n):
        for j in range(i + 1, n):
            try:
                shared = gdf.iloc[i].geometry.intersection(gdf.iloc[j].geometry)
                if shared.is_empty:
                    continue
                if shared.geom_type in ("LineString", "MultiLineString"):
                    length = shared.length
                elif shared.geom_type == "GeometryCollection":
                    length = sum(g.length for g in shared.geoms
                                 if g.geom_type in ("LineString", "MultiLineString"))
                else:
                    length = 0
                if length >= threshold:
                    edges.add(frozenset([gdf.iloc[i]["_name"], gdf.iloc[j]["_name"]]))
            except Exception:
                pass
    return edges


def agg_votes_to_eds(va_gdf, ed_gdf, ed_name_col):
    """Assign VA centroids to EDs, aggregate NDP and UCP votes per ED."""
    centroids = va_gdf.copy()
    centroids.geometry = va_gdf.geometry.centroid

    joined = gpd.sjoin(
        centroids[["geometry", "va_ndp", "va_ucp"]],
        ed_gdf[["geometry", ed_name_col]],
        how="left", predicate="within"
    )
    missed = joined[joined[ed_name_col].isna()].index
    if len(missed):
        nearest = gpd.sjoin_nearest(
            centroids.loc[missed, ["geometry", "va_ndp", "va_ucp"]],
            ed_gdf[["geometry", ed_name_col]],
            how="left"
        )
        joined.loc[missed, ed_name_col] = nearest[ed_name_col].values
        joined.loc[missed, "va_ndp"]    = nearest["va_ndp"].values
        joined.loc[missed, "va_ucp"]    = nearest["va_ucp"].values

    agg = joined.groupby(ed_name_col)[["va_ndp", "va_ucp"]].sum().reset_index()
    agg.columns = ["ed_name", "ndp", "ucp"]
    agg["total"] = agg["ndp"] + agg["ucp"]
    agg["ndp_share"] = agg["ndp"] / agg["total"].replace(0, np.nan)
    agg["ucp_share"] = agg["ucp"] / agg["total"].replace(0, np.nan)
    # Winning margin = |ndp_share - ucp_share|
    agg["margin"] = (agg["ndp_share"] - agg["ucp_share"]).abs()
    # Winner and loser
    agg["winner"] = np.where(agg["ndp"] > agg["ucp"], "NDP", "UCP")
    agg["loser"]  = np.where(agg["ndp"] > agg["ucp"], "UCP", "NDP")
    # Losing-party surplus = losing party's share (not wasted, just their total share)
    agg["losing_surplus"] = np.where(
        agg["ndp"] > agg["ucp"], agg["ucp_share"], agg["ndp_share"]
    )
    return agg.set_index("ed_name")


def chain_signals(vote_df, adj_edges):
    """
    Find all chain signals and coupled chain signals from the adjacency graph.

    Returns list of dicts describing each signal found.
    """
    signals = []
    for edge in adj_edges:
        a, b = sorted(edge)
        if a not in vote_df.index or b not in vote_df.index:
            continue

        for packed_ed, cracked_ed in [(a, b), (b, a)]:
            packed  = vote_df.loc[packed_ed]
            cracked = vote_df.loc[cracked_ed]

            if (packed["losing_surplus"] >= SURPLUS_THRESH and
                    cracked["margin"] <= MARGIN_THRESH):

                coupled = packed["loser"] == cracked["loser"]
                signals.append({
                    "packed_ed":      packed_ed,
                    "cracked_ed":     cracked_ed,
                    "packed_surplus": round(packed["losing_surplus"], 4),
                    "cracked_margin": round(cracked["margin"], 4),
                    "packed_loser":   packed["loser"],
                    "cracked_loser":  cracked["loser"],
                    "coupled":        coupled,
                })

    return signals


def run_map(label, off_path, va_gdf):
    print(f"\n=== {label} ===")
    off = gpd.read_file(off_path).to_crs("EPSG:3400")

    print(f"  Building official adjacency ({len(off)} EDs)...")
    adj = build_adjacency(off, "EDName2025")
    print(f"  Official edges: {len(adj)}")

    print(f"  Aggregating votes to official EDs...")
    votes = agg_votes_to_eds(va_gdf, off, "EDName2025")

    signals = chain_signals(votes, adj)
    total_signals   = len(signals)
    coupled_signals = sum(1 for s in signals if s["coupled"])

    print(f"  Chain signals (total):   {total_signals}")
    print(f"  Coupled chain signals:   {coupled_signals}")
    print(f"  Audit v0_8 coupled:      {AUDIT_COUPLED[label]}")
    print(f"  Delta vs audit:          {coupled_signals - AUDIT_COUPLED[label]:+d}")

    if signals:
        df_sig = pd.DataFrame(signals)
        print(f"\n  All chain signals:")
        print(df_sig[["packed_ed","cracked_ed","packed_surplus","cracked_margin","coupled"]].to_string(index=False))

    return coupled_signals, signals


def main():
    print("Loading VA polygons...")
    va = gpd.read_file(VA_PATH).to_crs("EPSG:3400")

    maj_coupled, maj_signals = run_map("majority", OFF_MAJ, va)
    min_coupled, min_signals = run_map("minority", OFF_MIN, va)

    ratio = min_coupled / maj_coupled if maj_coupled > 0 else float("inf")
    t535_pass = ratio <= PASS_RATIO

    print(f"\n--- §5.3.5 Summary ---")
    print(f"  Majority coupled signals (official):  {maj_coupled}")
    print(f"  Minority coupled signals (official):  {min_coupled}")
    print(f"  Ratio (minority/majority):            {ratio:.2f}x")
    print(f"  Pre-registered pass threshold:        <= {PASS_RATIO}x")
    print(f"  §5.3.5 RESULT (official geometry):    {'PASS' if t535_pass else 'FAIL'}")
    print(f"\n  Audit v0_8 result: minority={AUDIT_COUPLED['minority']} majority={AUDIT_COUPLED['majority']} ratio={AUDIT_COUPLED['minority']/AUDIT_COUPLED['majority']:.2f}x PASS")
    print(f"  Delta: majority {maj_coupled - AUDIT_COUPLED['majority']:+d}  minority {min_coupled - AUDIT_COUPLED['minority']:+d}")

    rows = maj_signals + min_signals
    for r in rows:
        r["map"] = "majority" if r in maj_signals else "minority"
    # Re-tag properly
    for r in maj_signals:
        r["map"] = "majority"
    for r in min_signals:
        r["map"] = "minority"

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nSaved -> {OUT}")


if __name__ == "__main__":
    main()
