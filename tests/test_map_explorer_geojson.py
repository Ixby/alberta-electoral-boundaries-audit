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
