"""canonical_paths.py — Canonical shapefile path resolver.

Official Elections Alberta shapefiles were released after the DPG analysis
phase completed. All active analysis scripts should use these paths.

DPGs (data/shapefiles/derived/) are deprecated — kept for provenance only.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from pathlib import Path
import sys

# Resolve ROOT dynamically relative to this file
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts" / "utils"))
import data_loader

def _resolve_from_config(config_path_str: str) -> Path:
    return ROOT / config_path_str

def canonical_shapefile(plan: str) -> Path:
    """Return path to the canonical shapefile for 'majority' or 'minority'."""
    try:
        config = data_loader.CONFIG
        p_str = config["maps"][plan]["path"]
        p = _resolve_from_config(p_str)
        if not p.exists():
            raise FileNotFoundError(f"Canonical shapefile not found: {p}")
        return p
    except KeyError:
        raise KeyError(f"Map '{plan}' not found in config.yaml maps section.")

def reference_2019_shapefile() -> Path:
    """Return path to the 2019 reference shapefile."""
    config = data_loader.CONFIG
    p_str = config["maps"]["enacted_2019"]["path"]
    p = _resolve_from_config(p_str)
    if not p.exists():
        raise FileNotFoundError(f"2019 reference shapefile not found: {p}")
    return p

# Extract the canonical column dynamically from config if needed, 
# otherwise default to EDName2025 as a safe fallback
try:
    ED_NAME_COL = data_loader.CONFIG["maps"]["majority"]["id_col"]
except KeyError:
    ED_NAME_COL = "EDName2025"

def all_canonical() -> dict:
    """Return {plan: Path} for all available canonical shapefiles."""
    return {
        plan: canonical_shapefile(plan)
        for plan in ("majority", "minority")
    }
