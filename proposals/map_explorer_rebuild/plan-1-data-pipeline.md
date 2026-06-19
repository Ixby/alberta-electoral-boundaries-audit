# Map Explorer Rebuild — Plan 1: Data Pipeline

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Regenerate the three map variants from the canonical GeoPackages into compact, full-fidelity planar GeoJSON (per-feature data embedded), replacing the ~112 MB of hi-res SVG — without touching the viewer yet.

**Architecture:** Refactor `analysis/scripts/build_cover.py` so its per-map data preparation (load canonical → VA→ED vote join → per-VA fill colour) is reusable, then add a GeoJSON exporter that writes EPSG:3401 coordinates shifted to a shared local origin (for deep-zoom GPU float precision) with each feature's tooltip data embedded as properties. The matplotlib PNG (for the PDF cover) stays; the 37 MB SVG export goes.

**Tech Stack:** Python 3.11+, geopandas 1.1, shapely 2.1, pytest. No new runtime dependency unless the size gate (Task 5) forces topology-preserving simplification.

**Spec:** `proposals/map_explorer_rebuild/design.md` (§3.2, §4, §9, §11).

---

## File structure

- **Modify** `analysis/scripts/build_cover.py`:
  - Extract `_prepare_map_data(map_key) -> (eds, name_col, va_render, va_ed_map)` from `build_cover_art` (all load/join/fill logic, current lines ~329–589, including the per-VA `_fill` computation).
  - Add `_export_map_geojson(map_key, eds, name_col, va_render, va_ed_map)` and helpers `_load_or_init_origin`, `_polygon_coords`.
  - `build_cover_art` becomes: prepare data → (minority only) render PNG → export GeoJSON. Remove the SVG `savefig` + `_tag_ed_hover_paths` call.
- **Create** `tests/test_map_explorer_geojson.py` — validates the exported GeoJSON.
- **Output** (written by the script, under the tracked Pages dir): `docs/data/va_<map>.geojson`, `docs/data/ed_<map>.geojson` (map ∈ minority/majority/2019), and `docs/data/map_meta.json` (CRS + shared origin).

Note: `docs/` is the GitHub Pages output and is tracked — committing the new GeoJSON there is correct and intended.

---

## Task 1: Extract reusable per-map data preparation

Pull the data-prep half of `build_cover_art` into a standalone function so GeoJSON export can use it without running matplotlib. No behaviour change — characterized by a test that the prepared frames have the expected shape.

**Files:**
- Modify: `analysis/scripts/build_cover.py` (`build_cover_art`, ~lines 322–671)
- Test: `tests/test_map_explorer_geojson.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_map_explorer_geojson.py
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
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -m pytest tests/test_map_explorer_geojson.py::test_prepare_map_data_shapes -v`
Expected: FAIL with `AttributeError: module 'build_cover' has no attribute '_prepare_map_data'`.

- [ ] **Step 3: Extract `_prepare_map_data`**

In `build_cover.py`, create a new function containing the body of `build_cover_art` from the `cfg = MAP_VARIANTS[map_key]` line through the `va_render["_fill"] = [...]` assignment (current ~lines 329–589). It must end by returning the prepared objects:

```python
def _prepare_map_data(map_key: str):
    """Load canonical geometry, join 2023 votes, compute per-VA fill colours.

    Returns (eds, name_col, va_render, va_ed_map). Pure data prep — no
    matplotlib. Reused by both the PNG render and the GeoJSON export.
    """
    import matplotlib.colors as mcolors
    import numpy as np
    import pandas as pd
    # ... (moved body: load map_path, read eds, VA centroid join, official
    #      scaling, crosswalk + nearest-VA fallbacks, cmap/norm, va_render
    #      construction, density weight, _va_fill, va_render["_fill"] = [...])
    return eds, name_col, va_render, va_ed_map
```

Then change `build_cover_art` to call it:

```python
def build_cover_art(map_key: str = "minority") -> Path:
    eds, name_col, va_render, va_ed_map = _prepare_map_data(map_key)
    # ... existing matplotlib render + exports continue below, unchanged ...
```

Move the imports the body needs (`matplotlib.colors`, `numpy`, `pandas`) into `_prepare_map_data`. The matplotlib `fig, ax = plt.subplots(...)` block and everything after it stays in `build_cover_art`.

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest tests/test_map_explorer_geojson.py::test_prepare_map_data_shapes -v`
Expected: PASS (or SKIP if data absent — then run on a machine with the shapefiles before continuing).

- [ ] **Step 5: Commit**

```bash
git add analysis/scripts/build_cover.py tests/test_map_explorer_geojson.py
git commit -m "refactor(build-cover): extract _prepare_map_data for reuse"
```

---

## Task 2: GeoJSON exporter with origin shift, mm quantization, embedded props

**Files:**
- Modify: `analysis/scripts/build_cover.py`
- Test: `tests/test_map_explorer_geojson.py`

- [ ] **Step 1: Write the failing test**

```python
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
    # raw 3401 magnitudes (~hundreds of km from origin).
    xy = va["features"][0]["geometry"]["coordinates"][0][0]
    assert abs(xy[0]) < 400_000 and abs(xy[1]) < 400_000
    assert meta["crs"] == "EPSG:3401" and "origin_x" in meta and "origin_y" in meta
    # mm quantization → at most 3 decimal places.
    assert round(xy[0], 3) == xy[0]
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -m pytest tests/test_map_explorer_geojson.py::test_export_geojson_minority -v`
Expected: FAIL with `AttributeError: ... has no attribute 'MAP_DATA_DIR'` / `_export_map_geojson`.

- [ ] **Step 3: Implement the exporter**

Add near the top of `build_cover.py` (after `_DOCS`):

```python
MAP_DATA_DIR = REPO_ROOT / "docs" / "data"
COORD_DECIMALS = 3  # millimetre precision; 3401 units are metres
```

Add the helpers + exporter:

```python
def _load_or_init_origin(bounds) -> tuple[float, float]:
    """Shared local origin so on-GPU coordinate magnitudes stay small at deep
    zoom. Persisted once to map_meta.json; every map reuses it so switching
    maps never shifts the view. bounds = (minx, miny, maxx, maxy)."""
    import json
    meta_path = MAP_DATA_DIR / "map_meta.json"
    if meta_path.exists():
        m = json.loads(meta_path.read_text(encoding="utf-8"))
        return float(m["origin_x"]), float(m["origin_y"])
    ox = round((bounds[0] + bounds[2]) / 2.0, COORD_DECIMALS)
    oy = round((bounds[1] + bounds[3]) / 2.0, COORD_DECIMALS)
    MAP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(
        json.dumps({"crs": "EPSG:3401", "origin_x": ox, "origin_y": oy}),
        encoding="utf-8",
    )
    return ox, oy


def _polygon_coords(geom, ox: float, oy: float):
    """(Multi)Polygon → GeoJSON coords, origin-shifted and rounded to mm."""
    def ring(coords):
        return [[round(x - ox, COORD_DECIMALS), round(y - oy, COORD_DECIMALS)] for x, y in coords]

    def one(poly):
        return [ring(poly.exterior.coords)] + [ring(i.coords) for i in poly.interiors]

    if geom.geom_type == "Polygon":
        return "Polygon", one(geom)
    return "MultiPolygon", [one(g) for g in geom.geoms]


def _export_map_geojson(map_key, eds, name_col, va_render, va_ed_map) -> None:
    """Write va_<map>.geojson + ed_<map>.geojson with embedded per-feature
    props, EPSG:3401 coords shifted to the shared origin and quantized to mm."""
    import json

    MAP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    ox, oy = _load_or_init_origin(tuple(eds.total_bounds))

    # ── VA features ────────────────────────────────────────────────────────
    va_feats = []
    for seq_i, (_, row) in enumerate(va_render.iterrows()):
        r, g, b, _a = row["_fill"]
        va_ucp = float(row.get("va_ucp", 0) or 0)
        va_ndp = float(row.get("va_ndp", 0) or 0)
        va_other = float(row.get("va_other", 0) or 0)
        two = max(va_ucp + va_ndp, 1.0)
        ed_name_raw = va_ed_map.get(seq_i)
        gtype, coords = _polygon_coords(row.geometry, ox, oy)
        va_feats.append({
            "type": "Feature",
            "properties": {
                "fill": [round(r * 255), round(g * 255), round(b * 255)],
                "ucp_pct": round(va_ucp / two * 100, 1),
                "ndp_pct": round(va_ndp / two * 100, 1),
                "in_person_votes": int(round(va_ucp + va_ndp + va_other)),
                "poll_name": f"Poll {row.get('VA_NUMBER', '')}",
                "ed_name": "" if (ed_name_raw is None or ed_name_raw != ed_name_raw) else str(ed_name_raw),
            },
            "geometry": {"type": gtype, "coordinates": coords},
        })

    # ── ED features ────────────────────────────────────────────────────────
    has_official = "official_ucp" in eds.columns
    ed_feats = []
    for i, row in eds.iterrows():
        ucp_share = float(row.get("ucp_share", 0.5))
        va_total = int(row.get("total", 0))
        if has_official and (int(round(row.get("official_ucp", 0))) + int(round(row.get("official_ndp", 0)))) > 0:
            uc = int(round(row["official_ucp"])); nd = int(round(row["official_ndp"]))
            votes = uc + nd
            ucp_pct = round(uc / votes * 100, 1); ndp_pct = round(nd / votes * 100, 1)
        else:
            uc = round(ucp_share * va_total); votes = va_total
            ucp_pct = round(ucp_share * 100, 1); ndp_pct = round((1.0 - ucp_share) * 100, 1)
        gtype, coords = _polygon_coords(row.geometry, ox, oy)
        ed_feats.append({
            "type": "Feature",
            "properties": {
                "id": int(i),
                "name": str(row[name_col]),
                "ucp_pct": ucp_pct,
                "ndp_pct": ndp_pct,
                "votes": int(votes),
                "pop": int(row.get("pop", 0)),
                "va_count": int(row.get("va_count", 0)),
            },
            "geometry": {"type": gtype, "coordinates": coords},
        })

    def _fc(feats):
        return {"type": "FeatureCollection", "crs": "EPSG:3401", "features": feats}

    (MAP_DATA_DIR / f"va_{map_key}.geojson").write_text(
        json.dumps(_fc(va_feats), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (MAP_DATA_DIR / f"ed_{map_key}.geojson").write_text(
        json.dumps(_fc(ed_feats), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"[build_cover] [{map_key}] Wrote GeoJSON: {len(va_feats)} VA + {len(ed_feats)} ED")
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest tests/test_map_explorer_geojson.py::test_export_geojson_minority -v`
Expected: PASS. If a column name differs (e.g. `VA_NUMBER`, `va_other`), the assertion or a `KeyError` will pinpoint it — fix the accessor and re-run.

- [ ] **Step 5: Commit**

```bash
git add analysis/scripts/build_cover.py tests/test_map_explorer_geojson.py
git commit -m "feat(build-cover): export per-map GeoJSON (origin-shifted, embedded props)"
```

---

## Task 3: Wire export into the build for all 3 maps; drop the hi-res SVG

**Files:**
- Modify: `analysis/scripts/build_cover.py` (`build_cover_art`, `build_map_variants`)
- Test: `tests/test_map_explorer_geojson.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -m pytest tests/test_map_explorer_geojson.py::test_build_emits_geojson_not_svg -v`
Expected: FAIL (the export call isn't yet wired for all maps / the test exercises the new path before edits land). Confirm it fails, then implement.

- [ ] **Step 3: Rewire the build**

In `build_cover_art`, after the PNG block, **replace** the SVG export + tagging with the GeoJSON export. Concretely:
- Delete the two `plt.savefig(str(svg_out), format="svg", ...)` lines and the surrounding `plt.rcParams['path.simplify']` toggles.
- Delete the `_tag_ed_hover_paths(svg_out, len(eds))` call and the legacy `shutil.copy2(svg_out, COVER_ART_HIRES_SVG)`.
- Keep the PNG block (`if map_key == "minority": plt.savefig(COVER_ART_PNG, ...)`).
- Add: `_export_map_geojson(map_key, eds, name_col, va_render, va_ed_map)`.
- Keep `_export_ed_hover_json` / `_export_va_hover_json` for now (removed at cutover in Plan 3).

Resulting tail of `build_cover_art`:

```python
    # Screen-res PNG (minority only) — still used by the PDF cover + WebGL fallback.
    if map_key == "minority":
        COVER_ART_PNG.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(COVER_ART_PNG, dpi=200, **_save_kwargs)
        print(f"[build_cover] Wrote screen-res art {COVER_ART_PNG.relative_to(REPO_ROOT)}")
    plt.close(fig)

    # Interactive-explorer data (replaces the 37 MB hi-res SVG).
    _export_map_geojson(map_key, eds, name_col, va_render, va_ed_map)

    # Legacy hover JSON kept until the viewer cutover (Plan 3).
    _export_ed_hover_json(eds, name_col, cfg["json"])
    va_json_out = cfg.get("va_json")
    if va_json_out is not None and va_ed_map is not None:
        _export_va_hover_json(va_render, va_ed_map, va_json_out)
    return COVER_ART_PNG
```

`build_map_variants` is unchanged (still builds `majority` and `2019`); each now emits GeoJSON instead of SVG.

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest tests/test_map_explorer_geojson.py -v`
Expected: all PASS.

- [ ] **Step 5: Regenerate the real artifacts and eyeball sizes**

Run: `PYTHONIOENCODING=utf-8 python analysis/scripts/build_cover.py`
Then: `ls -la docs/data/va_*.geojson docs/data/ed_*.geojson docs/images/cover_art.png`
Expected: three `va_*.geojson` + three `ed_*.geojson` exist; `cover_art.png` still present. Note each `va_*.geojson` size for Task 5.

- [ ] **Step 6: Commit**

```bash
git add analysis/scripts/build_cover.py tests/test_map_explorer_geojson.py docs/data/va_*.geojson docs/data/ed_*.geojson docs/data/map_meta.json
git commit -m "feat(build-cover): emit explorer GeoJSON for all 3 maps; drop hi-res SVG export"
```

---

## Task 4: Geometry & reference integrity

Guard the data the viewer will trust: every VA's `ed_name` resolves to a real ED, no NaN/null leaks into props, the shared origin is identical across maps.

**Files:**
- Test: `tests/test_map_explorer_geojson.py`

- [ ] **Step 1: Write the failing test**

```python
@requires_data
def test_geojson_integrity(tmp_path, monkeypatch):
    import json, math
    import build_cover
    monkeypatch.setattr(build_cover, "MAP_DATA_DIR", tmp_path)
    origins = []
    for key in ("minority", "majority", "2019"):
        eds, name_col, va_render, va_ed_map = build_cover._prepare_map_data(key)
        build_cover._export_map_geojson(key, eds, name_col, va_render, va_ed_map)
        va = json.loads((tmp_path / f"va_{key}.geojson").read_text(encoding="utf-8"))
        ed = json.loads((tmp_path / f"ed_{key}.geojson").read_text(encoding="utf-8"))
        ed_names = {f["properties"]["name"] for f in ed["features"]}
        for f in va["features"]:
            p = f["properties"]
            # Non-empty ed_name references must point at a real ED in this map.
            assert p["ed_name"] == "" or p["ed_name"] in ed_names
            # No NaN/None leaked into numeric props.
            for k2 in ("ucp_pct", "ndp_pct", "in_person_votes"):
                assert p[k2] is not None and not (isinstance(p[k2], float) and math.isnan(p[k2]))
        meta = json.loads((tmp_path / "map_meta.json").read_text(encoding="utf-8"))
        origins.append((meta["origin_x"], meta["origin_y"]))
    # All three maps share one origin (so switching maps doesn't jump the view).
    assert len(set(origins)) == 1
```

- [ ] **Step 2: Run it to verify it fails or passes**

Run: `python -m pytest tests/test_map_explorer_geojson.py::test_geojson_integrity -v`
Expected: This may PASS immediately if Task 2/3 are correct. If it FAILS on `ed_name` membership, the VA→ED join produced a name not in `eds[name_col]` — most likely a whitespace/casing mismatch; normalize `ed_name` with `.strip()` in `_export_map_geojson` and in `_export_va_hover_json` to match. If it fails on a shared origin, ensure `_load_or_init_origin` reads the persisted `map_meta.json` (the monkeypatched `MAP_DATA_DIR` persists across the loop within one test).

- [ ] **Step 3: Fix only if failing** (apply the normalization noted above; otherwise no code change).

- [ ] **Step 4: Re-run to confirm green**

Run: `python -m pytest tests/test_map_explorer_geojson.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add analysis/scripts/build_cover.py tests/test_map_explorer_geojson.py
git commit -m "test(map-explorer): guard ED-name references, NaN props, shared origin"
```

---

## Task 5: Size gate + decide on simplification (fidelity-first)

Crispness at ~40,000× is the priority, so simplification is reached for **only** if the full-fidelity files are impractically large. This task records the real sizes and adds a soft regression guard; it adds topology-preserving simplification **only if** a `va_*.geojson` exceeds the soft ceiling.

**Files:**
- Test: `tests/test_map_explorer_geojson.py`
- Modify (conditional): `analysis/scripts/build_cover.py`, `requirements.txt`

- [ ] **Step 1: Add a soft size-regression guard test**

```python
@requires_data
def test_va_geojson_size_guard():
    # Soft guard against accidental bloat — NOT a hard cap. Fidelity wins ties;
    # if a deliberate fidelity change pushes past this, raise the number with a
    # note rather than over-simplifying. Reads the committed docs/data artifacts.
    import os
    SOFT_CEILING_MB = 12.0  # raw; revisit only with a written justification
    for key in ("minority", "majority", "2019"):
        p = REPO_ROOT / "docs" / "data" / f"va_{key}.geojson"
        if not p.exists():
            pytest.skip("run build_cover.py first")
        mb = os.path.getsize(p) / 1e6
        assert mb < SOFT_CEILING_MB, f"va_{key}.geojson is {mb:.1f} MB (> {SOFT_CEILING_MB} soft ceiling)"
```

- [ ] **Step 2: Run it**

Run: `python -m pytest tests/test_map_explorer_geojson.py::test_va_geojson_size_guard -v`
Expected: PASS if the full-fidelity files are under ~12 MB raw (likely; the 37 MB SVG was inflated by path syntax + per-path styling, which GeoJSON drops). If it PASSES, **simplification is not needed — skip Step 3.**

- [ ] **Step 3 (only if Step 2 fails): add gentle topology-preserving simplification**

If and only if a file exceeds the ceiling:
- Add `topojson>=1.9` to `requirements.txt`; `python -m pip install topojson`.
- In `_export_map_geojson`, before building VA features, simplify with shared topology so adjacent VAs keep coincident edges:

```python
    import topojson as tp
    # Conservative tolerance (metres); raise only enough to hit the ceiling.
    topo = tp.Topology(va_render[[ "geometry" ]], prequantize=False, toposimplify=2.0)
    va_render = va_render.assign(geometry=topo.to_gdf().geometry.values)
```

Re-run `build_cover.py`, re-check sizes, and **eyeball the result at maximum zoom on the dev server in Plan 2** before trusting the tolerance. Lower the tolerance if any real boundary detail is lost.

- [ ] **Step 4: Re-run the full suite**

Run: `python -m pytest tests/test_map_explorer_geojson.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_map_explorer_geojson.py analysis/scripts/build_cover.py requirements.txt docs/data/va_*.geojson docs/data/ed_*.geojson
git commit -m "test(map-explorer): size regression guard; simplification only if needed"
```

---

## Done criteria for Plan 1

- `docs/data/{va,ed}_{minority,majority,2019}.geojson` + `map_meta.json` exist, full-fidelity, embedded props, origin-shifted, mm-quantized.
- `python -m pytest tests/test_map_explorer_geojson.py -v` all green.
- `cover_art.png` still produced (PDF cover unaffected); the 37 MB hi-res SVGs are no longer written by the build.
- The viewer is **untouched** — it still reads the old SVGs (which still exist on disk until Plan 3 deletes them). No user-visible change yet.

**Next:** Plan 2 (deck.gl render + bottom-dock UI) is written against these files, starting with a calibration slice that renders `va_minority.geojson` in an `OrthographicView` and validates orientation + float precision at 40,000× (spec §11) before building out interaction.
