"""
generate_realistic_91.py — Phase B synthetic 91-district input.

Starts from the canonical Elections Alberta majority recommendation (89 EDs)
and adds 2 plausible committee-style splits to produce a 91-district plan
that looks more like a real Lunty Special Select Committee output than a
random recursive-tree partition does.

**This script does NOT produce a prediction.** It produces a synthetic
test input that exercises the scorecard against a committee-like 91-district
shapefile. The two EDs split here (Calgary-McKenzie, Edmonton-McClung) are
chosen on a defensible-but-arbitrary rationale ("split the two largest urban
EDs to preempt population overflow in the 2031 census cycle"), not on any
information about what the Lunty committee will actually do.

Output is written to:
    proposals/lunty_dry_run/synthetic_realistic_91_test_input.gpkg

Method (per ED to split):
    1. Spatial-join VAs → ED via centroid-in-polygon (same convention as
       analysis/scripts/packing_cracking_analysis.py score_map_by_spatial_join).
    2. Compute the ED's bounding-box extent. Split perpendicular to the
       longer dimension (east-west if the ED is wider, north-south if taller).
    3. Bisect the contained VAs by the median centroid coordinate along the
       split axis; assign half to "<ED>-North"/"-East" and half to "<ED>-South"/"-West".
    4. Dissolve the VAs by new sub-ED name to produce two polygons that
       replace the original ED. The other 87 EDs' polygons are preserved
       byte-for-byte from the canonical gpkg.

The result is a 91-ED gpkg with the same column schema as
ea_majority_2026_eds.gpkg, so the scorecard reads it without modification.

Backward:
    proposals/lunty_dry_run/README.md
    data/shapefiles/canonical/ea_majority_2026_eds.gpkg  (89-ED base)
    data/shapefiles/canonical/va_2023_election_day_votes.gpkg  (VA centroids)

Forward:
    proposals/lunty_dry_run/synthetic_realistic_91_test_input.gpkg
    proposals/lunty_dry_run/dry_run_report.md  (Phase B section)
"""
from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
MAJ_GPKG = ROOT / "data" / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg"
VA_GPKG = ROOT / "data" / "shapefiles" / "canonical" / "va_2023_election_day_votes.gpkg"
POP_CACHE = ROOT / "data" / "va_pop_from_das.csv"
OUT_GPKG = ROOT / "proposals" / "lunty_dry_run" / "synthetic_realistic_91_test_input.gpkg"

# Two largest-population EDs in the canonical majority map. Splitting them is a
# defensible-but-arbitrary "preempt 2031-cycle overflow" committee rationale.
# Not a prediction of what Lunty will do.
SPLIT_EDS = ["Calgary-McKenzie", "Edmonton-McClung"]


def split_ed(va_subset: gpd.GeoDataFrame, ed_name: str, original_geom) -> list[dict]:
    """Bisect VAs in an ED into two halves perpendicular to the longer axis."""
    minx, miny, maxx, maxy = original_geom.bounds
    width = maxx - minx
    height = maxy - miny

    centroids = va_subset.geometry.representative_point()
    if width >= height:
        # ED is wider than tall — split east/west
        coord = centroids.x
        median_val = float(coord.median())
        labels = ["West", "East"]
        masks = [coord < median_val, coord >= median_val]
    else:
        # ED is taller than wide — split north/south
        coord = centroids.y
        median_val = float(coord.median())
        labels = ["South", "North"]
        masks = [coord < median_val, coord >= median_val]

    out_rows = []
    for label, mask in zip(labels, masks):
        chunk = va_subset[mask.values]
        if len(chunk) == 0:
            print(f"WARNING: {ed_name}-{label} got 0 VAs", file=sys.stderr)
            continue
        sub_geom = chunk.geometry.unary_union
        # Per-chunk actual population from the per-VA pop attribution.
        # Previously this slot was hardcoded to original_pop/2 at the call
        # site, which masked any real population imbalance when the
        # bisection split VAs evenly but populations unevenly (e.g.
        # Calgary-McKenzie's residential vs industrial halves).
        sub_pop = float(chunk["pop_2021"].sum())
        out_rows.append({
            "EDName2025": f"{ed_name}-{label}",
            "EDNum2025": None,  # synthetic; original EDNum doesn't apply
            "PopCensus": sub_pop,
            "geometry": sub_geom,
            "_va_ucp": float(chunk["va_ucp"].sum()),
            "_va_ndp": float(chunk["va_ndp"].sum()),
            "_va_other": float(chunk["va_other"].sum()),
            "_n_vas": len(chunk),
        })
    return out_rows


def main() -> int:
    print(f"[Phase B] starting realistic-plausible 91-district generator")
    print(f"  starting base: canonical majority (89 EDs)")
    print(f"  committee-style splits: {SPLIT_EDS}")

    maj = gpd.read_file(MAJ_GPKG)
    print(f"  loaded {len(maj)} majority EDs, CRS={maj.crs}")

    va = gpd.read_file(VA_GPKG)
    print(f"  loaded {len(va)} VAs, CRS={va.crs}")
    if va.crs != maj.crs:
        va = va.to_crs(maj.crs)

    # Attach per-VA 2021 population so split halves can report their
    # actual populations instead of a hardcoded original_pop/2 (which
    # would mask the residential-vs-industrial population imbalance the
    # bisection is supposed to surface for the scorecard to flag).
    if not POP_CACHE.exists():
        raise FileNotFoundError(f"Missing {POP_CACHE} (needed for per-half PopCensus)")
    pop_df = pd.read_csv(POP_CACHE).set_index("va_row_idx")["pop_2021"]
    mapped = va.index.map(pop_df)
    if mapped.isna().any():
        n_missing = int(mapped.isna().sum())
        raise RuntimeError(
            f"POP_CACHE row indices do not align with VA shapefile: "
            f"{n_missing} of {len(va)} VAs have no matching pop_2021 row. "
            f"Regenerate {POP_CACHE.name} against the current {VA_GPKG.name}."
        )
    va["pop_2021"] = mapped.astype(float)

    # Spatial-join VAs → majority EDs (centroid-in-polygon)
    va_pts = va.copy()
    va_pts["geometry"] = va_pts.geometry.representative_point()
    joined = gpd.sjoin(
        va_pts[["va_ucp", "va_ndp", "va_other", "pop_2021", "geometry"]],
        maj[["EDName2025", "geometry"]],
        how="left",
        predicate="within",
    )
    joined = joined.dropna(subset=["EDName2025"])
    joined = joined[~joined.index.duplicated(keep="first")]
    # Bring back VA polygon geometry (we joined on centroids; switch back for dissolve)
    joined["geometry"] = va.loc[joined.index, "geometry"].values
    print(f"  joined {len(joined)} VAs to majority EDs via centroid-in-polygon")

    new_rows = []
    for _, ed_row in maj.iterrows():
        ed_name = ed_row["EDName2025"]
        if ed_name in SPLIT_EDS:
            sub_vas = joined[joined["EDName2025"] == ed_name]
            print(f"\n  splitting {ed_name} (had {len(sub_vas)} VAs)...")
            splits = split_ed(sub_vas, ed_name, ed_row.geometry)
            for s in splits:
                print(f"    -> {s['EDName2025']}: {s['_n_vas']} VAs, "
                      f"ucp={s['_va_ucp']:,.0f}, ndp={s['_va_ndp']:,.0f}")
                new_rows.append({
                    "EDName2025": s["EDName2025"],
                    "EDNum2025": s["EDNum2025"],
                    "PopCensus": s["PopCensus"],  # actual sum of per-VA pop_2021
                    "Km2": None,
                    "Hectares": None,
                    "Acres": None,
                    "Shape_Area": s["geometry"].area,
                    "Shape_Leng": s["geometry"].length,
                    "va_ucp": s["_va_ucp"],
                    "va_ndp": s["_va_ndp"],
                    "va_other": s["_va_other"],
                    "geometry": s["geometry"],
                })
        else:
            # Preserve original ED geometry byte-for-byte; attach VA-level vote totals
            sub_vas = joined[joined["EDName2025"] == ed_name]
            new_rows.append({
                "EDName2025": ed_name,
                "EDNum2025": ed_row.get("EDNum2025"),
                "PopCensus": ed_row.get("PopCensus"),
                "Km2": ed_row.get("Km2"),
                "Hectares": ed_row.get("Hectares"),
                "Acres": ed_row.get("Acres"),
                "Shape_Area": ed_row.get("Shape_Area"),
                "Shape_Leng": ed_row.get("Shape_Leng"),
                "va_ucp": float(sub_vas["va_ucp"].sum()),
                "va_ndp": float(sub_vas["va_ndp"].sum()),
                "va_other": float(sub_vas["va_other"].sum()),
                "geometry": ed_row.geometry,
            })

    out = gpd.GeoDataFrame(new_rows, crs=maj.crs, geometry="geometry")
    print(f"\nFinal ED count: {len(out)} "
          f"(expected: {len(maj) + len(SPLIT_EDS)} = "
          f"{len(maj)} base + {len(SPLIT_EDS)} new sub-EDs)")
    assert len(out) == len(maj) + len(SPLIT_EDS), "wrong final ED count"

    OUT_GPKG.parent.mkdir(parents=True, exist_ok=True)
    out.to_file(OUT_GPKG, driver="GPKG")
    print(f"\nWrote {OUT_GPKG} ({OUT_GPKG.stat().st_size:,} bytes)")

    print()
    print("=" * 60)
    print("REALISTIC-PLAUSIBLE 91-DISTRICT TEST INPUT READY")
    print("=" * 60)
    print(f"Base map:    canonical majority (89 EDs)")
    print(f"Committee splits: {len(SPLIT_EDS)} EDs split E/W or N/S "
          "perpendicular to their longer axis")
    print(f"  - {SPLIT_EDS[0]} -> ...-West, ...-East (or North/South)")
    print(f"  - {SPLIT_EDS[1]} -> ...-West, ...-East (or North/South)")
    print(f"Districts: {len(out)}")
    print()
    print("This is a SYNTHETIC TEST INPUT for scorecard dry-run only.")
    print("It is NOT a prediction of the Lunty committee's output.")
    print("The 2 splits are an arbitrary 'preempt 2031-cycle overflow' choice.")
    print()
    print("Next step:")
    print(f"  python analysis/scripts/phase_b_scorecard.py "
          f"--shapefile {OUT_GPKG} --map-name SyntheticRealistic91 "
          "--name-col EDName2025 --out-dir proposals/lunty_dry_run --skip-mcmc")
    return 0


if __name__ == "__main__":
    sys.exit(main())
