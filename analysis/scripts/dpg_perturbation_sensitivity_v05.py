"""
DPG Perturbation Sensitivity (v0_5 / DA-anchored DPG)
=====================================================

Identical Monte Carlo flat-±offset perturbation pipeline to
analysis/scripts/v0_1_dpg_perturbation_sensitivity.py, but points at the
v0_5 DA-anchored canonical gpkg files instead of the v0_2 topology-clean
files. Records how the 90% CI on the majority−minority EG asymmetry moves
when sensitivity is measured against the latest DPG rather than the earlier
baseline.

Inputs (read-only):
  data/va_polygons_with_full_2023_votes.gpkg
  data/v0_5_canonical_majority_2026_eds_da_anchored.gpkg
  data/v0_5_canonical_minority_2026_eds_da_anchored.gpkg
  data/v0_1_majority_full_crosswalk.csv
  data/v0_1_minority_full_crosswalk.csv
  data/v0_1_majority_2026_populations.csv
  data/v0_1_minority_2026_populations.csv

Outputs:
  data/v0_5_dpg_perturbation_samples.csv
  data/v0_5_dpg_perturbation_summary.json

Forward: analysis/reports/v0_1_max_dpi_extraction_and_rerun.md
Backward:
  analysis/scripts/v0_1_dpg_perturbation_sensitivity.py
  analysis/scripts/v0_1_phase_4c_va_attribution_maup.py
  data/v0_5_canonical_{majority,minority}_2026_eds_da_anchored.gpkg
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
SCRIPTS = ANALYSIS / "scripts"

src = SCRIPTS / "v0_1_dpg_perturbation_sensitivity.py"
spec = importlib.util.spec_from_file_location("dpgperturb_v1", src)
mod = importlib.util.module_from_spec(spec)
sys.modules["dpgperturb_v1"] = mod
spec.loader.exec_module(mod)

# Redirect inputs to v0_5
mod.MAJ_CLEAN_GPKG = DATA / "shapefiles" / "derived" / "v0_5_canonical_majority_2026_eds_da_anchored.gpkg"
mod.MIN_CLEAN_GPKG = DATA / "shapefiles" / "derived" / "v0_5_canonical_minority_2026_eds_da_anchored.gpkg"

# Redirect outputs
mod.OUT_SAMPLES_CSV = DATA / "v0_5_dpg_perturbation_samples.csv"
mod.OUT_SUMMARY_JSON = DATA / "v0_5_dpg_perturbation_summary.json"
mod.OUT_WRITEUP = ANALYSIS / "reports" / "v0_5_dpg_perturbation_analysis.md"


if __name__ == "__main__":
    mod.main()
