"""
Phase 4B + 4F re-run against the v0_5 DA-anchored DPG.

Re-uses helpers from analysis/scripts/v0_1_phase_4bcdef_execution.py by
loading it as a module and monkey-patching MAJ_CANON_GPKG / MIN_CANON_GPKG
and the output paths. Only Phase 4B (DA -> ED population) and Phase 4F
(commission-population hardstop validation) are executed. Phase 4C is
superseded by v0_1_assignment_va_attribution_maup_v3_v05.py.

Inputs:
  data/v0_5_canonical_majority_2026_eds_da_anchored.gpkg
  data/v0_5_canonical_minority_2026_eds_da_anchored.gpkg
  data/alberta_2021_das.gpkg
  data/alberta_2021_da_populations.csv
  data/majority_full_crosswalk.csv
  data/minority_full_crosswalk.csv
  data/majority_2026_populations.csv
  data/minority_2026_populations.csv

Outputs:
  data/population_2021_majority.csv
  data/population_2021_minority.csv
  data/validation_deltas.csv
  analysis/reports/phase4f_summary.json

Forward: analysis/reports/max_dpi_extraction_and_rerun.md
Backward:
  analysis/scripts/v0_1_phase_4bcdef_execution.py
  data/v0_5_canonical_majority_2026_eds_da_anchored.gpkg
  data/v0_5_canonical_minority_2026_eds_da_anchored.gpkg
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
SCRIPTS = ANALYSIS / "scripts"

# Load the existing pipeline module
src = SCRIPTS / "v0_1_phase_4bcdef_execution.py"
spec = importlib.util.spec_from_file_location("p4bcdef", src)
m = importlib.util.module_from_spec(spec)
sys.modules["p4bcdef"] = m
spec.loader.exec_module(m)

# Redirect inputs to v0_5 DPG
m.MAJ_CANON_GPKG = DATA / "shapefiles" / "derived" / "v0_5_canonical_majority_2026_eds_da_anchored.gpkg"
m.MIN_CANON_GPKG = DATA / "shapefiles" / "derived" / "v0_5_canonical_minority_2026_eds_da_anchored.gpkg"

# Redirect outputs to v0_5 paths
m.OUT_4B_MAJ = DATA / "population_2021_majority.csv"
m.OUT_4B_MIN = DATA / "population_2021_minority.csv"
m.OUT_4F = DATA / "validation_deltas.csv"

OUT_SUMMARY = ANALYSIS / "reports" / "phase4f_summary.json"


def count_hardstops(combined_df) -> dict:
    out = {}
    for label in ("majority", "minority"):
        d = combined_df[combined_df["map"] == label].copy()
        d_nz = d[d["pop_2021_from_das"] > 0]
        out[label] = {
            "n_eds": len(d),
            "n_nonzero": len(d_nz),
            "n_zero_pop": int((d["pop_2021_from_das"] == 0).sum()),
            "n_warn_0p5pct": int(d_nz["delta_scaled_pct"].abs().gt(0.5).sum()),
            "n_hardstop_2pct": int(d_nz["delta_scaled_pct"].abs().gt(2.0).sum()),
            "max_abs_scaled_pct": float(d_nz["delta_scaled_pct"].abs().max()) if len(d_nz) else None,
            "top5_hardstops": (d_nz.reindex(d_nz["delta_scaled_pct"].abs()
                                            .sort_values(ascending=False).index)
                               [["ed_name", "pop_2021_from_das",
                                 "pop_commission", "delta_scaled_pct"]]
                               .head(5).to_dict(orient="records")),
        }
    return out


def main():
    print("=" * 72)
    print("  Phase 4B/4F re-run against v0_5 DA-anchored DPG")
    print("=" * 72)

    maj_4b, min_4b = m.run_phase_4b()
    combined_4f = m.run_phase_4f(maj_4b, min_4b)

    # Summarize
    summary = {
        "inputs": {
            "majority_canonical": str(m.MAJ_CANON_GPKG),
            "minority_canonical": str(m.MIN_CANON_GPKG),
        },
        "outputs": {
            "phase4b_majority_csv": str(m.OUT_4B_MAJ),
            "phase4b_minority_csv": str(m.OUT_4B_MIN),
            "phase4f_combined_csv": str(m.OUT_4F),
            "summary_json": str(OUT_SUMMARY),
        },
        "hardstops": count_hardstops(combined_4f),
    }

    # Also compare with v0_1 baseline from report_academic.md mentions
    v01_4f = DATA / "v0_1_validation_deltas.csv"
    if v01_4f.exists():
        import pandas as pd
        v01 = pd.read_csv(v01_4f)
        summary["v0_1_baseline"] = {
            "hardstops": {
                label: int(v01[(v01["map"] == label) & (v01["pop_2021_from_das"] > 0)]
                           ["delta_scaled_pct"].abs().gt(2.0).sum())
                for label in ("majority", "minority")
            }
        }

    OUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n[WRITE] {OUT_SUMMARY}")

    # Console summary
    print("\n" + "=" * 72)
    print("  HARDSTOPS (|Δ scaled| > 2%)")
    print("=" * 72)
    for lab, s in summary["hardstops"].items():
        print(f"  [{lab}] n_hardstop={s['n_hardstop_2pct']}, "
              f"n_warn={s['n_warn_0p5pct']}, "
              f"zero_pop={s['n_zero_pop']}, "
              f"max_abs_scaled_pct={s['max_abs_scaled_pct']}")
        for r in s["top5_hardstops"]:
            print(f"    {r['ed_name']:<35s} Δ={r['delta_scaled_pct']:+.2f}% "
                  f"mine={r['pop_2021_from_das']:,.0f} comm={r['pop_commission']:,.0f}")


if __name__ == "__main__":
    main()
