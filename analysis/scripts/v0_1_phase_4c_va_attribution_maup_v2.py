"""
Phase 4C (MAUP v2) — Re-run MAUP against topology-cleaned DPG
==============================================================
Identical to v0_1_phase_4c_va_attribution_maup.py except it points at the
v0_2 topology-cleaned canonical gpkg files produced by
`v0_1_topology_cleanup.py`. The v1 canonical files exhibited inter-ED
polygon overlap (~2,700 km² majority / ~16,500 km² minority) that inflated
MAUP coverage for 1,011 / 1,722 VAs and drove the Stony Plain-Drayton
Valley 24.8 pp flip. This script measures what the MAUP EG / asymmetry
becomes once that overlap is resolved by canon_source-based precedence
(sweep > osm-municipal-buffered > 2019-parent > v7; tie: smaller area wins).

Inputs (read-only):
  data/va_polygons_with_full_2023_votes.gpkg
  data/v0_2_canonical_majority_2026_eds_topoclean.gpkg
  data/v0_2_canonical_minority_2026_eds_topoclean.gpkg
  data/v0_1_majority_full_crosswalk.csv
  data/v0_1_minority_full_crosswalk.csv
  data/v0_1_majority_2026_populations.csv
  data/v0_1_minority_2026_populations.csv

Outputs:
  data/v0_2_phase4c_majority_2023_votes_maup.csv
  data/v0_2_phase4c_minority_2023_votes_maup.csv
  analysis/reports/phase_4c_va_to_2026_assignments_maup_v2.csv
  analysis/reports/v0_2_phase4c_maup_summary.json

Forward: analysis/reports/v0_1_topology_cleanup_analysis.md
Backward:
  analysis/scripts/v0_1_phase_4c_va_attribution_maup.py
  analysis/scripts/v0_1_topology_cleanup.py
  data/v0_2_canonical_majority_2026_eds_topoclean.gpkg
  data/v0_2_canonical_minority_2026_eds_topoclean.gpkg
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
SCRIPTS = ANALYSIS / "scripts"

# Reuse helpers from the v1 MAUP script so the two pipelines stay in sync.
v1_path = SCRIPTS / "v0_1_phase_4c_va_attribution_maup.py"
spec = importlib.util.spec_from_file_location("maup_v1", v1_path)
m1 = importlib.util.module_from_spec(spec)
sys.modules["maup_v1"] = m1
spec.loader.exec_module(m1)

VA_GPKG = DATA / "va_polygons_with_full_2023_votes.gpkg"
MAJ_CLEAN_GPKG = DATA / "v0_2_canonical_majority_2026_eds_topoclean.gpkg"
MIN_CLEAN_GPKG = DATA / "v0_2_canonical_minority_2026_eds_topoclean.gpkg"
MAJ_XWALK_CSV = DATA / "v0_1_majority_full_crosswalk.csv"
MIN_XWALK_CSV = DATA / "v0_1_minority_full_crosswalk.csv"
MAJ_POPS_CSV = DATA / "v0_1_majority_2026_populations.csv"
MIN_POPS_CSV = DATA / "v0_1_minority_2026_populations.csv"

OUT_MAJ = DATA / "v0_2_phase4c_majority_2023_votes_maup.csv"
OUT_MIN = DATA / "v0_2_phase4c_minority_2023_votes_maup.csv"
OUT_PER_VA = ANALYSIS / "reports" / "phase_4c_va_to_2026_assignments_maup_v2.csv"
OUT_SUMMARY = ANALYSIS / "reports" / "v0_2_phase4c_maup_summary.json"

CENTROID_MAJORITY_EG = -0.0233
CENTROID_MINORITY_EG = +0.0182
CENTROID_ASYMMETRY_PP = +4.15

# MAUP-v1 (before topology cleanup) — from v0_1_phase4c_maup_summary.json
MAUP_V1_MAJORITY_EG = -0.03251765
MAUP_V1_MINORITY_EG = -0.02135434
MAUP_V1_ASYMMETRY_PP = (MAUP_V1_MINORITY_EG - MAUP_V1_MAJORITY_EG) * 100


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", type=int, default=None)
    args = parser.parse_args()

    print("=" * 72)
    print("  Phase 4C MAUP v2 — re-run after topology cleanup")
    print("=" * 72)

    print("\n[load] VA polygons...")
    vas = gpd.read_file(VA_GPKG)
    print(f"  VAs: {len(vas)}")

    print("\n[load] v0_2 topology-cleaned DPGs...")
    maj_eds = m1.load_canonical(MAJ_CLEAN_GPKG, vas.crs)
    min_eds = m1.load_canonical(MIN_CLEAN_GPKG, vas.crs)
    print(f"  Majority: {len(maj_eds)}   Minority: {len(min_eds)}")

    maj_xwalk = m1.load_crosswalk(MAJ_XWALK_CSV)
    min_xwalk = m1.load_crosswalk(MIN_XWALK_CSV)
    maj_names = pd.read_csv(MAJ_POPS_CSV)["ed_name"].tolist()
    min_names = pd.read_csv(MIN_POPS_CSV)["ed_name"].tolist()

    # === MAJORITY ===
    print("\n" + "=" * 72)
    print("  MAJORITY (topology-cleaned)")
    print("=" * 72)
    t0 = time.time()
    maj = m1.run_one_map(vas, maj_eds, maj_xwalk, maj_names, "majority",
                         smoke_n=args.smoke)
    print(f"  [majority elapsed: {time.time()-t0:.1f}s]")

    # === MINORITY ===
    print("\n" + "=" * 72)
    print("  MINORITY (topology-cleaned)")
    print("=" * 72)
    t1 = time.time()
    mino = m1.run_one_map(vas, min_eds, min_xwalk, min_names, "minority",
                          smoke_n=args.smoke)
    print(f"  [minority elapsed: {time.time()-t1:.1f}s]")

    # Outputs
    print("\n[write] outputs...")
    maj["ed_totals"].to_csv(OUT_MAJ, index=False)
    mino["ed_totals"].to_csv(OUT_MIN, index=False)
    per_va = pd.concat([
        maj["apportioned"].assign(map="majority"),
        mino["apportioned"].assign(map="minority"),
    ], ignore_index=True)[[
        "map", "OBJECTID", "parent_ed_2019", "VA_NUMBER", "name_2026",
        "area_weight", "va_ndp_full_share", "va_ucp_full_share",
        "va_other_full_share", "fallback",
    ]].rename(columns={"name_2026": "ed_2026"})
    per_va.to_csv(OUT_PER_VA, index=False)
    print(f"  wrote: {OUT_MAJ}")
    print(f"  wrote: {OUT_MIN}")
    print(f"  wrote: {OUT_PER_VA} ({len(per_va):,} rows)")

    # === COMPARISON ===
    print("\n" + "=" * 72)
    print("  COMPARISON: centroid | MAUP-v1 | MAUP-v2 (topology-cleaned)")
    print("=" * 72)
    maj_eg = maj["eg"]
    min_eg = mino["eg"]
    asym = (min_eg - maj_eg) * 100

    print(f"  centroid §5.2.7:  maj={CENTROID_MAJORITY_EG*100:+.4f}%  "
          f"min={CENTROID_MINORITY_EG*100:+.4f}%  "
          f"asym={CENTROID_ASYMMETRY_PP:+.4f} pp")
    print(f"  MAUP-v1 (raw):    maj={MAUP_V1_MAJORITY_EG*100:+.4f}%  "
          f"min={MAUP_V1_MINORITY_EG*100:+.4f}%  "
          f"asym={MAUP_V1_ASYMMETRY_PP:+.4f} pp")
    print(f"  MAUP-v2 (clean):  maj={maj_eg*100:+.4f}%  "
          f"min={min_eg*100:+.4f}%  "
          f"asym={asym:+.4f} pp")

    d_maj_v1 = (maj_eg - MAUP_V1_MAJORITY_EG) * 100
    d_min_v1 = (min_eg - MAUP_V1_MINORITY_EG) * 100
    d_asym_v1 = asym - MAUP_V1_ASYMMETRY_PP
    print(f"  Δ v2 vs v1:       Δmaj={d_maj_v1:+.4f} pp  "
          f"Δmin={d_min_v1:+.4f} pp  Δasym={d_asym_v1:+.4f} pp")

    # Stony-Plain flip check
    print("\n[diagnostic] Stony Plain-Drayton Valley under v2:")
    for lab, t in [("majority", maj), ("minority", mino)]:
        row = t["ed_totals"][t["ed_totals"]["ed_name"].str.contains("Stony Plain", case=False, na=False)]
        if not row.empty:
            u = float(row["ucp_2023"].iloc[0])
            d = float(row["ndp_2023"].iloc[0])
            share = d / (u + d) if (u + d) > 0 else float("nan")
            winner = "NDP" if d > u else "UCP"
            print(f"  [{lab}] UCP={u:.0f}  NDP={d:.0f}  NDP share={share*100:.2f}%  winner={winner}")

    # Verdict
    abs_asym_v1 = abs(MAUP_V1_ASYMMETRY_PP)
    abs_asym_v2 = abs(asym)
    if abs_asym_v2 < 1.0:
        verdict = "MAUP-v2 closes §5.2.7 gap below 1 pp"
    elif abs_asym_v2 < abs_asym_v1 - 0.25:
        verdict = "MAUP-v2 narrows §5.2.7 gap"
    elif abs_asym_v2 > abs_asym_v1 + 0.25:
        verdict = "MAUP-v2 widens §5.2.7 gap"
    else:
        verdict = "MAUP-v2 preserves §5.2.7 gap"
    print(f"\n  VERDICT: {verdict}")

    summary = {
        "inputs": {
            "va_gpkg": str(VA_GPKG),
            "majority_canonical_clean": str(MAJ_CLEAN_GPKG),
            "minority_canonical_clean": str(MIN_CLEAN_GPKG),
        },
        "outputs": {
            "majority_votes_csv": str(OUT_MAJ),
            "minority_votes_csv": str(OUT_MIN),
            "per_va_attribution_csv": str(OUT_PER_VA),
            "summary_json": str(OUT_SUMMARY),
        },
        "centroid_baseline_527": {
            "majority_eg": CENTROID_MAJORITY_EG,
            "minority_eg": CENTROID_MINORITY_EG,
            "asymmetry_pp": CENTROID_ASYMMETRY_PP,
        },
        "maup_v1_raw_canonical": {
            "majority_eg": MAUP_V1_MAJORITY_EG,
            "minority_eg": MAUP_V1_MINORITY_EG,
            "asymmetry_pp": MAUP_V1_ASYMMETRY_PP,
        },
        "maup_v2_topoclean": {
            "majority": {
                "eg": maj["eg"],
                "mm_gap": maj["mm_gap"],
                "ndp_seats": maj["ndp_seats"],
                "ucp_seats": maj["ucp_seats"],
                "two_party_total": maj["two_party_total"],
                "coverage": maj["coverage"],
                "conservation": maj["conservation"],
            },
            "minority": {
                "eg": mino["eg"],
                "mm_gap": mino["mm_gap"],
                "ndp_seats": mino["ndp_seats"],
                "ucp_seats": mino["ucp_seats"],
                "two_party_total": mino["two_party_total"],
                "coverage": mino["coverage"],
                "conservation": mino["conservation"],
            },
            "asymmetry_pp": asym,
        },
        "delta_v2_vs_v1_pp": {
            "majority": d_maj_v1,
            "minority": d_min_v1,
            "asymmetry": d_asym_v1,
        },
        "verdict": verdict,
    }
    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"  wrote: {OUT_SUMMARY}")

    print("\n[DONE]")


if __name__ == "__main__":
    main()
