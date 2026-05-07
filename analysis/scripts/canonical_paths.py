"""canonical_paths.py — Canonical shapefile path resolver.

Official Elections Alberta shapefiles were released after the DPG analysis
phase completed. All active analysis scripts should use these paths.

DPGs (data/shapefiles/derived/) are deprecated — kept for provenance only.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # .../alberta_audit
_CANONICAL = ROOT / "data" / "shapefiles" / "canonical"

# Column name for ED name in canonical shapefiles
ED_NAME_COL = "EDName2025"

# Reference 2019 shapefile (authoritative; not a DPG)
_REFERENCE_2019 = ROOT / "data" / "shapefiles" / "reference" / "alberta_2019_eds"


def canonical_shapefile(plan: str) -> Path:
    """Return path to the canonical shapefile for 'majority' or 'minority'."""
    p = _CANONICAL / f"ea_{plan}_2026_eds.gpkg"
    if not p.exists():
        raise FileNotFoundError(
            f"Canonical shapefile not found: {p}\n"
            "Ensure data/shapefiles/canonical/ contains the official EA files."
        )
    return p


def reference_2019_shapefile() -> Path:
    """Return path to the 2019 reference shapefile."""
    p = _REFERENCE_2019 / "EDS_ENACTED_BILL33_15DEC2017.shp"
    if not p.exists():
        raise FileNotFoundError(f"2019 reference shapefile not found: {p}")
    return p


def all_canonical() -> dict:
    """Return {plan: Path} for all available canonical shapefiles."""
    return {
        plan: canonical_shapefile(plan)
        for plan in ("majority", "minority")
    }
