"""
Tests for analysis/utils/data_loader.py.

Forward dependencies: none
Backward dependencies: data_loader.load_config, load_shapefile, get_map, get_columns
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import box

# Ensure utils is importable
_utils = Path(__file__).resolve().parent.parent / "analysis" / "utils"
if str(_utils) not in sys.path:
    sys.path.insert(0, str(_utils))

import data_loader


# ── Helpers ───────────────────────────────────────────────────────────────────

def _minimal_gdf(epsg: int = 4326) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"id": [1]},
        geometry=[box(0, 0, 1, 1)],
        crs=f"EPSG:{epsg}",
    )


def _yaml_config(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "config.yaml"
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


# ── _resolve_path ─────────────────────────────────────────────────────────────

def test_resolve_path_is_absolute():
    result = data_loader._resolve_path("data/something.gpkg")
    assert result.is_absolute()


def test_resolve_path_relative_to_root():
    result = data_loader._resolve_path("data/something.gpkg")
    assert result.name == "something.gpkg"
    assert "data" in result.parts


# ── load_config ───────────────────────────────────────────────────────────────

def test_load_config_missing_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(data_loader, "CONFIG_PATH", tmp_path / "no_config.yaml")
    result = data_loader.load_config()
    assert result == {}


def test_load_config_reads_yaml(tmp_path, monkeypatch):
    cfg_path = _yaml_config(tmp_path, """\
        audit:
          crs_epsg: 3401
    """)
    monkeypatch.setattr(data_loader, "CONFIG_PATH", cfg_path)
    result = data_loader.load_config()
    assert result["audit"]["crs_epsg"] == 3401


def test_load_config_empty_file_returns_empty(tmp_path, monkeypatch):
    p = tmp_path / "empty.yaml"
    p.write_text("", encoding="utf-8")
    monkeypatch.setattr(data_loader, "CONFIG_PATH", p)
    result = data_loader.load_config()
    assert result == {}


# ── load_shapefile ────────────────────────────────────────────────────────────

def test_load_shapefile_not_found_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(data_loader, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(data_loader, "_CONFIG", {})
    with pytest.raises(FileNotFoundError, match="not found"):
        data_loader.load_shapefile("missing/file.gpkg")


def test_load_shapefile_reprojects(tmp_path, monkeypatch):
    """load_shapefile reprojects to target CRS when gdf.crs differs."""
    monkeypatch.setattr(data_loader, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(data_loader, "_CONFIG", {})

    fake_file = tmp_path / "shapes.gpkg"
    fake_file.write_bytes(b"dummy")

    expected_gdf = _minimal_gdf(epsg=3401)

    # Build mock before entering patch context so attributes are set cleanly
    src_gdf_mock = MagicMock()
    src_gdf_mock.crs.to_epsg.return_value = 4326  # source is 4326, target is 3401
    src_gdf_mock.to_crs.return_value = expected_gdf

    with patch("data_loader.gpd") as mock_gpd:
        mock_gpd.read_file.return_value = src_gdf_mock
        data_loader.load_shapefile(str(fake_file), crs=3401)
        src_gdf_mock.to_crs.assert_called_once_with(epsg=3401)


def test_load_shapefile_uses_config_crs_fallback(tmp_path, monkeypatch):
    """load_shapefile uses audit.crs_epsg from CONFIG when crs arg is None."""
    monkeypatch.setattr(data_loader, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(data_loader, "_CONFIG", {"audit": {"crs_epsg": 3347}})

    fake_file = tmp_path / "shapes.gpkg"
    fake_file.write_bytes(b"dummy")

    with patch("data_loader.gpd") as mock_gpd:
        src = MagicMock(spec=gpd.GeoDataFrame)
        src.crs = MagicMock()
        src.crs.to_epsg.return_value = 4326
        src.to_crs.return_value = src
        mock_gpd.read_file.return_value = src

        data_loader.load_shapefile(str(fake_file), crs=None)
        src.to_crs.assert_called_once_with(epsg=3347)


# ── get_map ───────────────────────────────────────────────────────────────────

def test_get_map_missing_map_name_raises_key_error(monkeypatch):
    monkeypatch.setattr(data_loader, "_CONFIG", {"maps": {}})
    with pytest.raises(KeyError, match="not defined"):
        data_loader.get_map("nonexistent_map")


def test_get_map_no_path_raises_value_error(monkeypatch):
    monkeypatch.setattr(data_loader, "_CONFIG", {"maps": {"majority": {}}})
    with pytest.raises(ValueError, match="No path defined"):
        data_loader.get_map("majority")


# ── get_columns ───────────────────────────────────────────────────────────────

def test_get_columns_returns_dict(monkeypatch):
    cols = {"ndp": "ndp_2023", "ucp": "ucp_2023"}
    monkeypatch.setattr(data_loader, "_CONFIG", {"substrate": {"columns": cols}})
    assert data_loader.get_columns() == cols


def test_get_columns_missing_config_returns_empty(monkeypatch):
    monkeypatch.setattr(data_loader, "_CONFIG", {})
    assert data_loader.get_columns() == {}
