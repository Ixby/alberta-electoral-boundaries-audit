"""
generate_synthetic_91.py — produce a neutral synthetic 91-district plan for dry-runs.

This script generates ONE valid 91-district plan from the canonical VA adjacency
graph for the sole purpose of testing the Phase B Scorecard
(analysis/scripts/phase_b_scorecard.py) on a 91-district input before
the real Lunty Special Select Committee map drops on 2026-11-02.

**This script does not produce a prediction.** The output plan is a random
recursive-tree-partition draw with no committee-style adjustment, no
community-of-interest weighting, no political optimisation, and no narrative
intent. It exists solely so the scorecard can be tested end-to-end on a
91-district shapefile with the canonical pipeline, surfacing any 89/91
column-name or array-size assumptions before the live 72-hour Nov 2 window.

Output is written to:
    proposals/lunty_dry_run/synthetic_neutral_91_test_input.gpkg

with columns:
    EDName2025  (str)  — "Synthetic-01" through "Synthetic-91"
    Shape_Area  (float)
    Shape_Leng  (float)
    geometry    (polygon)

matching the canonical EA shapefile schema so the scorecard reads the file
without modification.

Backward:
    proposals/lunty_dry_run/README.md           — dry-run framing
    analysis/scripts/mcmc_ensemble.py            — build_va_graph()
    data/shapefiles/canonical/va_2023_election_day_votes.gpkg
    data/va_pop_from_das.csv

Forward:
    proposals/lunty_dry_run/synthetic_neutral_91_test_input.gpkg
    proposals/lunty_dry_run/dry_run_report.md   — bugs surfaced
"""
from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = ROOT / "analysis" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(ROOT / "analysis" / "utils"))

from gerrychain import Graph  # noqa: E402
from gerrychain.tree import recursive_tree_part  # noqa: E402

OUT_GPKG = ROOT / "proposals" / "lunty_dry_run" / "synthetic_neutral_91_test_input.gpkg"
VA_PATH = ROOT / "data" / "shapefiles" / "canonical" / "va_2023_election_day_votes.gpkg"
POP_CACHE = ROOT / "data" / "va_pop_from_das.csv"
N_DISTRICTS = 91
POP_TOLERANCE = 0.25  # EBCA standard
LABEL = "DRY_RUN_SYNTHETIC"


def label_seed(label: str) -> int:
    """Derive a deterministic int seed from a verbally-tagged label.

    Avoids any drand-beacon dependency (this is dry-run infrastructure, not a
    pre-registered audit run) while keeping the seed reproducible from the
    label string alone.
    """
    h = hashlib.sha256(label.encode()).hexdigest()
    return int(h[:16], 16) & 0x7FFFFFFF  # 31-bit positive int


def build_canonical_va_graph():
    """Build a rook-adjacency graph over the canonical VA shapefile.

    Self-contained: does not depend on the derived VA gpkg, which is LFS-tracked
    and may not be materialised in dry-run environments. Attaches pop_2021
    from data/va_pop_from_das.csv to each node.
    """
    print(f"[{time.strftime('%H:%M:%S')}] loading canonical VAs from {VA_PATH.name}...")
    va = gpd.read_file(VA_PATH)
    va["va_ndp"] = va["va_ndp"].fillna(0.0).astype(float)
    va["va_ucp"] = va["va_ucp"].fillna(0.0).astype(float)
    va["va_other"] = va["va_other"].fillna(0.0).astype(float)
    va["total_votes"] = va["va_ndp"] + va["va_ucp"] + va["va_other"]

    print(f"  loaded {len(va)} VAs (CRS={va.crs})")

    if not POP_CACHE.exists():
        raise FileNotFoundError(f"Missing {POP_CACHE}")
    pop_df = pd.read_csv(POP_CACHE).set_index("va_row_idx")["pop_2021"]
    mapped = va.index.map(pop_df)
    if mapped.isna().any():
        n_missing = int(mapped.isna().sum())
        raise RuntimeError(
            f"POP_CACHE row indices do not align with VA shapefile: "
            f"{n_missing} of {len(va)} VAs have no matching pop_2021 row. "
            f"Most likely cause: {POP_CACHE.name} was generated against a "
            f"different vintage of {VA_PATH.name} than the one loaded here. "
            f"Regenerate the pop cache against the current VA shapefile "
            f"before re-running. (The previous code silently fillna'd to 0.0 "
            f"and floored to pop=1, producing a 'successful' synthetic plan "
            f"against entirely fabricated populations.)"
        )
    va["pop_2021"] = mapped
    va["pop_2021"] = np.maximum(va["pop_2021"], 1.0)  # floor to avoid zero-pop nodes
    print(f"  total 2021 pop across VAs: {va['pop_2021'].sum():,.0f}")

    print(f"[{time.strftime('%H:%M:%S')}] building adjacency graph...")
    t = time.time()
    graph = Graph.from_geodataframe(va, ignore_errors=True)
    print(f"  built in {time.time()-t:.1f}s: {graph.number_of_nodes()} nodes, "
          f"{graph.number_of_edges()} edges")

    for idx, row in va.iterrows():
        n = graph.nodes[idx]
        n["va_ucp"] = float(row["va_ucp"])
        n["va_ndp"] = float(row["va_ndp"])
        n["va_other"] = float(row["va_other"])
        n["pop_2021"] = float(row["pop_2021"])
        n["total_votes"] = float(row["total_votes"])

    return graph, va


def main() -> int:
    print(f"[{LABEL}] starting synthetic 91-district generator")
    seed = label_seed(LABEL)
    print(f"  seed: {seed} (label '{LABEL}', sha256[:16])")

    graph, va_gdf = build_canonical_va_graph()
    total_pop = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
    ideal_pop = total_pop / N_DISTRICTS
    print(f"  ideal_pop_per_district: {ideal_pop:,.0f}")

    print(f"\nGenerating {N_DISTRICTS}-district partition via recursive_tree_part...")
    import random as _r
    _r.seed(seed)

    assignment = recursive_tree_part(
        graph,
        parts=list(range(1, N_DISTRICTS + 1)),
        pop_target=ideal_pop,
        pop_col="pop_2021",
        epsilon=POP_TOLERANCE,
        node_repeats=4,
    )

    # Verify population balance
    pops = {p: 0.0 for p in range(1, N_DISTRICTS + 1)}
    for node, part_id in assignment.items():
        pops[part_id] += graph.nodes[node]["pop_2021"]
    min_p, max_p = min(pops.values()), max(pops.values())
    dev_envelope = (max_p - min_p) / ideal_pop
    print(f"  partition population range: {min_p:,.0f} to {max_p:,.0f}")
    print(f"  envelope deviation: {dev_envelope*100:.1f}% (target: <= {POP_TOLERANCE*100:.0f}%)")

    if dev_envelope > POP_TOLERANCE:
        print(f"WARNING: deviation envelope {dev_envelope*100:.1f}% exceeds tolerance",
              file=sys.stderr)

    # Materialize the partition as district polygons (we already have va_gdf in hand)
    print("\nMapping partition assignment back to VA polygons...")
    va = va_gdf.copy()
    va["synthetic_district_id"] = va.index.map(assignment)
    if va["synthetic_district_id"].isna().any():
        n_unassigned = int(va["synthetic_district_id"].isna().sum())
        print(f"WARNING: {n_unassigned} VAs unassigned by partition", file=sys.stderr)
        va = va.dropna(subset=["synthetic_district_id"]).copy()

    va["synthetic_district_id"] = va["synthetic_district_id"].astype(int)
    va["EDName2025"] = va["synthetic_district_id"].apply(lambda i: f"Synthetic-{i:02d}")

    print("\nDissolving VAs by synthetic district...")
    eds = va.dissolve(by="EDName2025", aggfunc={"va_ucp": "sum",
                                                "va_ndp": "sum",
                                                "va_other": "sum"}).reset_index()
    eds["Shape_Area"] = eds.geometry.area
    eds["Shape_Leng"] = eds.geometry.length
    eds["synthetic_pop"] = eds["EDName2025"].apply(
        lambda name: pops[int(name.split("-")[1])]
    )
    print(f"  produced {len(eds)} synthetic EDs")
    print(f"  sample: {sorted(eds['EDName2025'].tolist())[:5]} ... "
          f"{sorted(eds['EDName2025'].tolist())[-3:]}")

    # Reorder columns to match canonical EA shapefile schema where possible
    keep_cols = ["EDName2025", "Shape_Area", "Shape_Leng", "synthetic_pop",
                 "va_ucp", "va_ndp", "va_other", "geometry"]
    eds = eds[keep_cols]

    print(f"\nWriting output: {OUT_GPKG}")
    OUT_GPKG.parent.mkdir(parents=True, exist_ok=True)
    eds.to_file(OUT_GPKG, driver="GPKG")
    print(f"  wrote {OUT_GPKG.stat().st_size:,} bytes")

    print("\n" + "=" * 60)
    print("SYNTHETIC 91-DISTRICT TEST INPUT READY")
    print("=" * 60)
    print(f"Path:    {OUT_GPKG}")
    print(f"Schema:  EDName2025 (str), Shape_Area, Shape_Leng, synthetic_pop, "
          "va_ucp, va_ndp, va_other, geometry")
    print(f"Seed:    {seed} (label '{LABEL}')")
    print(f"Districts: {len(eds)}")
    print(f"Pop envelope: {dev_envelope*100:.1f}% (target <= {POP_TOLERANCE*100:.0f}%)")
    print()
    print("This is a SYNTHETIC TEST INPUT for scorecard dry-run only.")
    print("It is NOT a prediction of the Lunty committee's output.")
    print()
    print("Next step: run the scorecard against it:")
    print(f"  python analysis/scripts/phase_b_scorecard.py "
          f"--shapefile {OUT_GPKG} --map-name SyntheticNeutral91 "
          "--name-col EDName2025 --skip-mcmc")
    return 0


if __name__ == "__main__":
    sys.exit(main())
