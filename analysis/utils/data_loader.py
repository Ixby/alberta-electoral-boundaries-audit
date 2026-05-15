"""
Centralized Data Loader Utility

Handles loading configuration from config.yaml, reading shapefiles via GeoPandas,
standardizing Coordinate Reference Systems (CRS), and providing a unified interface
for all analytical scripts to access data.
"""

import yaml
from pathlib import Path
import geopandas as gpd

# Resolve the repository root relative to this file's location
# (analysis/utils/data_loader.py → analysis/ → repo root)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"

def load_config() -> dict:
    """Loads and parses the central config.yaml file."""
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

_CONFIG: dict | None = None


def get_config() -> dict:
    """Return the cached config, loading from disk on first call."""
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = load_config()
    return _CONFIG


# Module-level alias kept for backward compatibility with callers that
# do `from data_loader import CONFIG`. New code should call get_config().
CONFIG = get_config()

# Findings directory — where all analysis scripts write their outputs.
# Config key: paths.findings_dir (default: "findings" if key absent).
FINDINGS = ROOT_DIR / CONFIG.get("paths", {}).get("findings_dir", "findings")


def _resolve_path(rel_path: str) -> Path:
    """Resolves a config relative path to an absolute Path object."""
    return ROOT_DIR / rel_path

def load_shapefile(path_key: str, crs: int = None) -> gpd.GeoDataFrame:
    """
    Loads a shapefile from a path, standardizing the CRS.
    
    Args:
        path_key: The string path (relative to repo root) or a Path object.
        crs: The EPSG code to project to. If None, uses audit.crs_epsg from config.
        
    Returns:
        GeoDataFrame projected to the target CRS.
    """
    target_crs = crs if crs is not None else get_config().get("audit", {}).get("crs_epsg", 3400)
    
    file_path = _resolve_path(path_key) if isinstance(path_key, str) else path_key
    
    if not file_path.exists():
        raise FileNotFoundError(f"Shapefile not found: {file_path}")
        
    gdf = gpd.read_file(file_path)
    
    # Standardize CRS
    if gdf.crs is None or gdf.crs.to_epsg() != target_crs:
        gdf = gdf.to_crs(epsg=target_crs)
        
    return gdf

def get_map(map_name: str) -> gpd.GeoDataFrame:
    """Load a predefined map from the config.

    Accepts either role-based keys ('map_a', 'map_b', 'reference') or
    backward-compatible keys ('majority', 'minority', 'enacted_2019').
    """
    maps_config = get_config().get("maps", {})
    if map_name not in maps_config:
        raise KeyError(f"Map '{map_name}' not defined in config.yaml under 'maps'.")

    path = maps_config[map_name].get("path")
    if not path:
        raise ValueError(f"No path defined for map '{map_name}' in config.yaml.")

    return load_shapefile(path)


def get_map_config(map_name: str) -> dict:
    """Return the full config block for a named map (path, id_col, label, role).

    Accepts either role-based ('map_a', 'map_b', 'reference') or
    backward-compatible ('majority', 'minority', 'enacted_2019') keys.
    """
    maps_config = get_config().get("maps", {})
    if map_name not in maps_config:
        raise KeyError(f"Map '{map_name}' not defined in config.yaml under 'maps'.")
    return maps_config[map_name]

def get_substrate() -> gpd.GeoDataFrame:
    """
    Loads the demographic/voting substrate defined in the config.
    Falls back to fallback_path if primary path doesn't exist.
    """
    sub_config = get_config().get("substrate", {})
    primary_path = _resolve_path(sub_config.get("path", ""))
    fallback_path = _resolve_path(sub_config.get("fallback_path", ""))
    
    if primary_path.exists():
        return load_shapefile(primary_path)
    elif fallback_path.exists():
        return load_shapefile(fallback_path)
    else:
        raise FileNotFoundError(f"Substrate not found at {primary_path} or {fallback_path}")

def get_columns() -> dict:
    """Returns the column mappings defined in the config."""
    return get_config().get("substrate", {}).get("columns", {})


def get_party_labels() -> dict:
    """Return the parties block from config: incumbent, opposition, incumbent_historical.

    Falls back to Alberta-specific defaults so scripts are not broken if the
    parties block is absent (e.g., when running against a pre-Track-F config).
    """
    defaults = {
        "incumbent": "UCP",
        "opposition": "NDP",
        "incumbent_historical": "RBC",
    }
    cfg = get_config().get("parties", {})
    return {**defaults, **cfg}


def get_election_config() -> dict:
    """Return the elections block from config: current_year, boundary_year, baseline_years."""
    defaults = {
        "current_year": 2023,
        "boundary_year": 2026,
        "baseline_years": [2019, 2015],
    }
    cfg = get_config().get("elections", {})
    return {**defaults, **cfg}
