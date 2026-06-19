"""Tests for the interactive-explorer GeoJSON export (Plan 1)."""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "analysis" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "utils"))

CANONICAL = REPO_ROOT / "data" / "shapefiles" / "canonical"
DERIVED_VA = REPO_ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"

requires_data = pytest.mark.skipif(
    not (CANONICAL / "ea_minority_2026_eds.gpkg").exists() or not DERIVED_VA.exists(),
    reason="canonical/derived shapefiles not present",
)

EXPECTED_ED_COUNT = {"minority": 89, "majority": 89, "2019": 87}
EXPECTED_VA_COUNT = 4765


@requires_data
def test_prepare_map_data_shapes():
    import build_cover
    eds, name_col, va_render, va_ed_map = build_cover._prepare_map_data("minority")
    assert len(eds) == EXPECTED_ED_COUNT["minority"]
    assert len(va_render) == EXPECTED_VA_COUNT
    assert name_col in eds.columns
    # Per-VA fill must be available without matplotlib having drawn anything.
    assert "_fill" in va_render.columns
    r, g, b, a = va_render.iloc[0]["_fill"]
    assert 0.0 <= r <= 1.0 and a == 1.0


@requires_data
def test_export_geojson_minority(tmp_path, monkeypatch):
    import json
    import build_cover
    # Redirect output to a temp dir so the test never touches docs/.
    monkeypatch.setattr(build_cover, "MAP_DATA_DIR", tmp_path)
    eds, name_col, va_render, va_ed_map = build_cover._prepare_map_data("minority")
    build_cover._export_map_geojson("minority", eds, name_col, va_render, va_ed_map)

    va = json.loads((tmp_path / "va_minority.geojson").read_text(encoding="utf-8"))
    ed = json.loads((tmp_path / "ed_minority.geojson").read_text(encoding="utf-8"))
    meta = json.loads((tmp_path / "map_meta.json").read_text(encoding="utf-8"))

    assert va["type"] == "FeatureCollection"
    assert len(va["features"]) == EXPECTED_VA_COUNT
    assert len(ed["features"]) == EXPECTED_ED_COUNT["minority"]

    # Embedded VA props.
    p = va["features"][0]["properties"]
    assert set(["fill", "ucp_pct", "ndp_pct", "in_person_votes", "poll_name", "ed_name"]) <= set(p)
    assert isinstance(p["fill"], list) and len(p["fill"]) == 3
    assert all(0 <= c <= 255 for c in p["fill"])

    # Embedded ED props.
    ep = ed["features"][0]["properties"]
    assert set(["name", "ucp_pct", "ndp_pct", "votes", "pop", "va_count"]) <= set(ep)

    # Origin shift: coordinates are centred near zero (|x|,|y| < ~400 km), not
    # raw 3401 magnitudes (~hundreds of km from origin). Feature 0 is a
    # MultiPolygon (4762/4765 VAs are), so drill to the first point regardless
    # of Polygon vs MultiPolygon nesting depth.
    xy = va["features"][0]["geometry"]["coordinates"]
    while isinstance(xy[0], list):
        xy = xy[0]
    assert abs(xy[0]) < 400_000 and abs(xy[1]) < 400_000
    assert meta["crs"] == "EPSG:3401" and "origin_x" in meta and "origin_y" in meta
    # mm quantization → at most 3 decimal places.
    assert round(xy[0], 3) == xy[0]
