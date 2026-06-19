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

    # Origin shift + mm quantization: walk every coordinate pair of feature 0.
    def _points(coords):
        if coords and isinstance(coords[0][0], (int, float)):
            yield from coords          # a ring: list of [x, y]
        else:
            for sub in coords:
                yield from _points(sub)
    pts = list(_points(va["features"][0]["geometry"]["coordinates"]))
    assert pts, "feature 0 has no coordinates"
    for px, py in pts:
        assert abs(px) < 400_000 and abs(py) < 400_000      # origin-shifted
        assert round(px, 3) == px and round(py, 3) == py     # mm-quantized
    assert meta["crs"] == "EPSG:3401" and "origin_x" in meta and "origin_y" in meta


@requires_data
def test_build_emits_geojson_not_svg(tmp_path, monkeypatch):
    import build_cover
    monkeypatch.setattr(build_cover, "MAP_DATA_DIR", tmp_path)
    # Point the SVG/json outputs at tmp so the test is hermetic.
    for k, cfg in build_cover.MAP_VARIANTS.items():
        cfg["svg"] = tmp_path / f"cover_art_{k}_hires.svg"
    for key in ("minority", "majority", "2019"):
        eds, name_col, va_render, va_ed_map = build_cover._prepare_map_data(key)
        build_cover._export_map_geojson(key, eds, name_col, va_render, va_ed_map)
        assert (tmp_path / f"va_{key}.geojson").exists()
        assert (tmp_path / f"ed_{key}.geojson").exists()
        # The 37 MB hi-res SVG must no longer be produced by the export path.
        assert not (tmp_path / f"cover_art_{key}_hires.svg").exists()
