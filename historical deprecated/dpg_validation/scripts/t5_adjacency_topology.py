"""
T5 — Adjacency Topology Equivalence

Builds the adjacency graph (which EDs share a boundary edge) for both the
DPG and official shapefiles, then compares edge sets.

A topology difference means the DPG had a wrong neighbour — which directly
affects the §5.3.5 neighbour-drain adjacency test (the pre-registered PASS
for the minority map). If the adjacency graph changes, that finding needs
a note.

Pass threshold: edge sets identical OR differ by <= 2 edges per map.
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

DPG_MAJ = REPO / "data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg"
DPG_MIN = REPO / "data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg"
OFF_MAJ = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
OUT = ROOT / "outputs/t5_adjacency_diff.csv"
OUT.parent.mkdir(exist_ok=True)

TOUCH_THRESHOLD = 50  # metres — shared boundary must be at least this long


def build_adjacency(gdf, name_col, threshold=TOUCH_THRESHOLD):
    """
    Return a frozenset of frozenset pairs representing adjacent ED pairs.
    Two EDs are adjacent if their shared boundary length >= threshold metres.
    """
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
                    length = sum(
                        g.length
                        for g in shared.geoms
                        if g.geom_type in ("LineString", "MultiLineString")
                    )
                else:
                    length = 0
                if length >= threshold:
                    edges.add(frozenset([gdf.iloc[i]["_name"], gdf.iloc[j]["_name"]]))
            except Exception:
                pass
    return edges


def run_map(label, dpg_path, off_path, dpg_name_col, off_name_col):
    print(f"\n=== {label} ===")
    dpg = gpd.read_file(dpg_path)
    off = gpd.read_file(off_path)

    print(f"  Building DPG adjacency ({len(dpg)} EDs)...")
    dpg_edges = build_adjacency(dpg, dpg_name_col)
    print(f"  Building official adjacency ({len(off)} EDs)...")
    off_edges = build_adjacency(off, off_name_col)

    only_dpg = dpg_edges - off_edges
    only_off = off_edges - dpg_edges
    both = dpg_edges & off_edges

    print(f"  DPG edges:      {len(dpg_edges)}")
    print(f"  Official edges: {len(off_edges)}")
    print(f"  Shared:         {len(both)}")
    print(f"  Only in DPG:    {len(only_dpg)}")
    print(f"  Only in off:    {len(only_off)}")

    t5_pass = len(only_dpg) <= 2 and len(only_off) <= 2
    print(f"  T5 PASS threshold: <= 2 extra edges per side")
    print(f"  T5 RESULT:         {'PASS' if t5_pass else 'FAIL'}")

    if only_dpg:
        print(f"  Extra DPG adjacencies (not in official):")
        for e in sorted(only_dpg, key=lambda x: sorted(x)):
            print(f"    {sorted(e)[0]} -- {sorted(e)[1]}")

    if only_off:
        print(f"  Missing from DPG (in official but not DPG):")
        for e in sorted(only_off, key=lambda x: sorted(x)):
            print(f"    {sorted(e)[0]} -- {sorted(e)[1]}")

    # Flatten to rows for CSV
    rows = []
    for e in only_dpg:
        a, b = sorted(e)
        rows.append({"map": label, "ed_a": a, "ed_b": b, "status": "dpg_only"})
    for e in only_off:
        a, b = sorted(e)
        rows.append({"map": label, "ed_a": a, "ed_b": b, "status": "official_only"})
    for e in both:
        a, b = sorted(e)
        rows.append({"map": label, "ed_a": a, "ed_b": b, "status": "both"})

    return pd.DataFrame(rows), {
        "map": label,
        "dpg_edges": len(dpg_edges),
        "official_edges": len(off_edges),
        "shared_edges": len(both),
        "dpg_only_edges": len(only_dpg),
        "official_only_edges": len(only_off),
        "t5_pass": t5_pass,
    }


def main():
    all_rows = []
    summaries = []

    df_maj, s_maj = run_map("majority", DPG_MAJ, OFF_MAJ, "name_2026", "EDName2025")
    all_rows.append(df_maj)
    summaries.append(s_maj)

    df_min, s_min = run_map("minority", DPG_MIN, OFF_MIN, "name_2026", "EDName2025")
    all_rows.append(df_min)
    summaries.append(s_min)

    combined = pd.concat(all_rows, ignore_index=True)
    combined.to_csv(OUT, index=False)

    print(f"\n--- Summary ---")
    for s in summaries:
        print(
            f"  {s['map']}: shared={s['shared_edges']}  "
            f"dpg_only={s['dpg_only_edges']}  off_only={s['official_only_edges']}  "
            f"{'PASS' if s['t5_pass'] else 'FAIL'}"
        )
    print(f"\nSaved -> {OUT}")


if __name__ == "__main__":
    main()
