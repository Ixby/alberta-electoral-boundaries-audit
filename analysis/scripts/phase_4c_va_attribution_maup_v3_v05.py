"""
Phase 4C (MAUP v3) — Re-run MAUP against the v0_5 DA-anchored DPG
=================================================================
Same pipeline as v0_1_phase_4c_va_attribution_maup_v2.py, but points at the
v0_5 canonical gpkg files (DA-anchored on top of v0_4 municipal anchoring
and v0_3 sweep). Records how the MAUP-weighted EG / asymmetry / seats move
from the v0_2 topology-clean baseline to v0_5.

Inputs:
  data/va_polygons_with_full_2023_votes.gpkg
  data/v0_5_canonical_majority_2026_eds_da_anchored.gpkg
  data/v0_5_canonical_minority_2026_eds_da_anchored.gpkg
  data/v0_1_majority_full_crosswalk.csv
  data/v0_1_minority_full_crosswalk.csv
  data/v0_1_majority_2026_populations.csv
  data/v0_1_minority_2026_populations.csv

Outputs:
  data/v0_5_phase4c_majority_2023_votes_maup.csv
  data/v0_5_phase4c_minority_2023_votes_maup.csv
  analysis/reports/v0_5_phase4c_va_to_2026_assignments_maup.csv
  analysis/reports/v0_5_phase4c_maup_summary.json

Forward: analysis/reports/v0_1_max_dpi_extraction_and_rerun.md
Backward:
  analysis/scripts/v0_1_phase_4c_va_attribution_maup.py
  analysis/scripts/v0_1_phase_4c_va_attribution_maup_v2.py
  data/v0_5_canonical_majority_2026_eds_da_anchored.gpkg
  data/v0_5_canonical_minority_2026_eds_da_anchored.gpkg
"""
# Version: 0.1 series  (last updated 2026-04-26)

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

v1_path = SCRIPTS / "v0_1_phase_4c_va_attribution_maup.py"
spec = importlib.util.spec_from_file_location("maup_v1", v1_path)
m1 = importlib.util.module_from_spec(spec)
sys.modules["maup_v1"] = m1
spec.loader.exec_module(m1)

VA_GPKG = DATA / "shapefiles" / "derived" / "va_polygons_with_full_2023_votes.gpkg"
MAJ_GPKG = DATA / "shapefiles" / "derived" / "v0_5_canonical_majority_2026_eds_da_anchored.gpkg"
MIN_GPKG = DATA / "shapefiles" / "derived" / "v0_5_canonical_minority_2026_eds_da_anchored.gpkg"
MAJ_XWALK_CSV = DATA / "v0_1_majority_full_crosswalk.csv"
MIN_XWALK_CSV = DATA / "v0_1_minority_full_crosswalk.csv"
MAJ_POPS_CSV = DATA / "v0_1_majority_2026_populations.csv"
MIN_POPS_CSV = DATA / "v0_1_minority_2026_populations.csv"

OUT_MAJ = DATA / "v0_5_phase4c_majority_2023_votes_maup.csv"
OUT_MIN = DATA / "v0_5_phase4c_minority_2023_votes_maup.csv"
OUT_PER_VA = ANALYSIS / "reports" / "v0_5_phase4c_va_to_2026_assignments_maup.csv"
OUT_SUMMARY = ANALYSIS / "reports" / "v0_5_phase4c_maup_summary.json"

CENTROID_MAJORITY_EG = -0.0233
CENTROID_MINORITY_EG = +0.0182
CENTROID_ASYMMETRY_PP = +4.15

# v0_2 topology-cleaned baseline (read directly from summary if present)
V02_SUMMARY = ANALYSIS / "reports" / "v0_2_phase4c_maup_summary.json"


def load_v02_baseline():
    try:
        with open(V02_SUMMARY) as f:
            d = json.load(f)
        return d.get("maup_v2_topoclean", {}), d.get("asymmetry_pp") or d["maup_v2_topoclean"].get("asymmetry_pp")
    except Exception:
        return {}, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", type=int, default=None)
    args = parser.parse_args()

    print("=" * 72)
    print("  Phase 4C MAUP v3 — DA-anchored (v0_5) DPG")
    print("=" * 72)

    print("\n[load] VA polygons...")
    vas = gpd.read_file(VA_GPKG)
    print(f"  VAs: {len(vas)}")

    print("\n[load] v0_5 DA-anchored DPGs...")
    maj_eds = m1.load_canonical(MAJ_GPKG, vas.crs)
    min_eds = m1.load_canonical(MIN_GPKG, vas.crs)
    print(f"  Majority: {len(maj_eds)}   Minority: {len(min_eds)}")

    maj_xwalk = m1.load_crosswalk(MAJ_XWALK_CSV)
    min_xwalk = m1.load_crosswalk(MIN_XWALK_CSV)
    maj_names = pd.read_csv(MAJ_POPS_CSV)["ed_name"].tolist()
    min_names = pd.read_csv(MIN_POPS_CSV)["ed_name"].tolist()

    print("\n" + "=" * 72)
    print("  MAJORITY (v0_5)")
    print("=" * 72)
    t0 = time.time()
    maj = m1.run_one_map(vas, maj_eds, maj_xwalk, maj_names, "majority",
                         smoke_n=args.smoke)
    print(f"  [majority elapsed: {time.time()-t0:.1f}s]")

    print("\n" + "=" * 72)
    print("  MINORITY (v0_5)")
    print("=" * 72)
    t1 = time.time()
    mino = m1.run_one_map(vas, min_eds, min_xwalk, min_names, "minority",
                          smoke_n=args.smoke)
    print(f"  [minority elapsed: {time.time()-t1:.1f}s]")

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

    # Comparison
    maj_eg = maj["eg"]
    min_eg = mino["eg"]
    asym = (min_eg - maj_eg) * 100

    v02, _ = load_v02_baseline()
    v02_maj_eg = v02.get("majority", {}).get("eg")
    v02_min_eg = v02.get("minority", {}).get("eg")
    v02_asym = v02.get("asymmetry_pp")

    print("\n" + "=" * 72)
    print("  COMPARISON")
    print("=" * 72)
    print(f"  centroid §5.2.7:  maj={CENTROID_MAJORITY_EG*100:+.4f}%  "
          f"min={CENTROID_MINORITY_EG*100:+.4f}%  "
          f"asym={CENTROID_ASYMMETRY_PP:+.4f} pp")
    if v02_maj_eg is not None:
        print(f"  v0_2 MAUP-v2:     maj={v02_maj_eg*100:+.4f}%  "
              f"min={v02_min_eg*100:+.4f}%  "
              f"asym={v02_asym:+.4f} pp")
    print(f"  v0_5 MAUP-v3:     maj={maj_eg*100:+.4f}%  "
          f"min={min_eg*100:+.4f}%  "
          f"asym={asym:+.4f} pp")

    if v02_maj_eg is not None:
        d_maj = (maj_eg - v02_maj_eg) * 100
        d_min = (min_eg - v02_min_eg) * 100
        d_asym = asym - v02_asym
        print(f"  Δ v0_5 vs v0_2:   Δmaj={d_maj:+.4f} pp  "
              f"Δmin={d_min:+.4f} pp  Δasym={d_asym:+.4f} pp")
    else:
        d_maj = d_min = d_asym = None

    # Top-5 per-ED vote shifts vs v0_2
    print("\n[diagnostic] Top per-ED NDP-share shifts (v0_5 minus v0_2):")
    shifts_tables = {}
    for label, v05_path, v02_path in [
        ("majority", OUT_MAJ, DATA / "v0_2_phase4c_majority_2023_votes_maup.csv"),
        ("minority", OUT_MIN, DATA / "v0_2_phase4c_minority_2023_votes_maup.csv"),
    ]:
        try:
            a = pd.read_csv(v05_path)
            b = pd.read_csv(v02_path)
            a["ndp_share"] = a["ndp_2023"] / (a["ndp_2023"] + a["ucp_2023"]).replace(0, pd.NA)
            b["ndp_share"] = b["ndp_2023"] / (b["ndp_2023"] + b["ucp_2023"]).replace(0, pd.NA)
            merged = a[["ed_name", "ndp_share"]].merge(
                b[["ed_name", "ndp_share"]], on="ed_name", suffixes=("_v05", "_v02")
            )
            merged["delta_pp"] = (merged["ndp_share_v05"] - merged["ndp_share_v02"]) * 100
            top = merged.reindex(merged["delta_pp"].abs().sort_values(ascending=False).index).head(10)
            shifts_tables[label] = top.to_dict(orient="records")
            print(f"\n  [{label}]")
            for _, row in top.head(5).iterrows():
                print(f"    {row['ed_name']:<35s}  "
                      f"v0_2={row['ndp_share_v02']*100:6.2f}%  "
                      f"v0_5={row['ndp_share_v05']*100:6.2f}%  "
                      f"Δ={row['delta_pp']:+.2f} pp")
        except Exception as e:
            print(f"  [{label}] shift table failed: {e}")

    verdict = ("v0_5 DA-anchoring moved asymmetry "
               f"{'toward' if abs(asym) < abs(v02_asym or asym) else 'away from'} "
               f"{CENTROID_ASYMMETRY_PP:+.2f} pp centroid"
               if v02_asym is not None else "v0_2 baseline missing")

    summary = {
        "inputs": {
            "va_gpkg": str(VA_GPKG),
            "majority_canonical": str(MAJ_GPKG),
            "minority_canonical": str(MIN_GPKG),
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
        "v0_2_topoclean": {
            "majority_eg": v02_maj_eg,
            "minority_eg": v02_min_eg,
            "asymmetry_pp": v02_asym,
        },
        "v0_5_da_anchored": {
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
        "delta_v05_vs_v02_pp": {
            "majority": d_maj,
            "minority": d_min,
            "asymmetry": d_asym,
        },
        "per_ed_shifts_top10": shifts_tables,
        "verdict": verdict,
    }
    OUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n  wrote: {OUT_SUMMARY}")
    print("\n[DONE]")


if __name__ == "__main__":
    main()
