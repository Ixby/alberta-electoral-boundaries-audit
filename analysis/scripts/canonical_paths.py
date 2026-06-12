# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
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
sys.path.insert(0, str(ROOT / "analysis" / "utils"))
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


# Canonical CRS for the audit. Verified via pyproj 2026-06-12 per T1.7 R2 Ref #10:
#   EPSG:3400 = NAD83 / Alberta 10-TM (Forest),  k₀=0.9992, false easting 500,000 m
#   EPSG:3401 = NAD83 / Alberta 10-TM (Resource), k₀=0.9992, false easting 0 m
# Both projections share scale factor and projection family; they differ only by 500 km
# of false easting. Area/perimeter computations are identical in either system; the only
# hazard is mixing un-reprojected coordinates in an sjoin.
#
# Pipeline default is 3400 (canonical EA shapefiles ship in 3400). Compactness scripts
# (compactness_metrics.py, polsby_popper.py, reock.py) reproject to 3401 for historical
# reasons; the choice is immaterial for area/perimeter but consumers should not mix.
CANONICAL_CRS = "EPSG:3400"
COMPACTNESS_CRS = "EPSG:3401"


def assert_canonical_crs(gdf, label: str = "gdf"):
    """Assert that a GeoDataFrame is in the canonical CRS (3400) before sjoin.

    Raises ValueError if the gdf's CRS doesn't match. Use at every sjoin site
    where coordinates would otherwise be silently misregistered by 500 km.
    """
    from pyproj import CRS
    if gdf.crs is None:
        raise ValueError(f"{label}: CRS is None (cannot assert canonical CRS)")
    expected = CRS.from_user_input(CANONICAL_CRS)
    if not CRS.from_user_input(gdf.crs).equals(expected):
        raise ValueError(
            f"{label}: CRS is {gdf.crs}, not the canonical CANONICAL_CRS={CANONICAL_CRS}. "
            "Reproject with `.to_crs(CANONICAL_CRS)` before sjoin."
        )
