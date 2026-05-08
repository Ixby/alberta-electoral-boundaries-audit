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
# (analysis/scripts/utils/data_loader.py)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"

def load_config() -> dict:
    """Loads and parses the central config.yaml file."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Global cached config
CONFIG = load_config()

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
    target_crs = crs if crs is not None else CONFIG.get("audit", {}).get("crs_epsg", 3400)
    
    file_path = _resolve_path(path_key) if isinstance(path_key, str) else path_key
    
    if not file_path.exists():
        raise FileNotFoundError(f"Shapefile not found: {file_path}")
        
    gdf = gpd.read_file(file_path)
    
    # Standardize CRS
    if gdf.crs is None or gdf.crs.to_epsg() != target_crs:
        gdf = gdf.to_crs(epsg=target_crs)
        
    return gdf

def get_map(map_name: str) -> gpd.GeoDataFrame:
    """
    Loads a predefined map from the config (e.g., 'majority', 'minority', 'enacted_2019').
    """
    maps_config = CONFIG.get("maps", {})
    if map_name not in maps_config:
        raise KeyError(f"Map '{map_name}' not defined in config.yaml under 'maps'.")
        
    path = maps_config[map_name].get("path")
    if not path:
        raise ValueError(f"No path defined for map '{map_name}' in config.yaml.")
        
    return load_shapefile(path)

def get_substrate() -> gpd.GeoDataFrame:
    """
    Loads the demographic/voting substrate defined in the config.
    Falls back to fallback_path if primary path doesn't exist.
    """
    sub_config = CONFIG.get("substrate", {})
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
    return CONFIG.get("substrate", {}).get("columns", {})
