# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""Build the cover/hero art and the map-explorer data exports.

Pipeline:
1. Generate the hero image: Alberta outline (silhouette, dark) with overlaid
   boundary-line art showing where majority and minority 2026 proposals
   diverge. Orange for majority, blue for minority, grey dashed for the 2019
   baseline.
2. Build the majority / minority / 2019 map variants and export the
   map-explorer GeoJSON + hover JSON consumed by the viewer
   (tests/test_map_explorer_geojson.py exercises these exports).

Run:  PYTHONIOENCODING=utf-8 python analysis/scripts/build_cover.py
Output: maps/cover_art.png + cover_art_hires.svg, and the viewer mapdata
        exports. (The merged report_public.pdf this script once assembled
        was removed 2026-07-11 along with build_pdf.py — the public report
        is published as markdown only.)

Dependencies: geopandas, shapely, matplotlib.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import subprocess
import sys
import tempfile
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ALBERTA_EDS = data_loader._resolve_path("data") / "shapefiles" / "reference" / "alberta_2019_eds"
DERIVED = data_loader._resolve_path("data") / "shapefiles" / "derived"
# Canonical Elections Alberta shapefiles only. The earlier DPG fallback
# chain (v0_10_topological → v0_8_refined → v0_8_canonical → v0_7_canonical)
# was removed 2026-06-10: it would silently fall through to DPG geometry if
# canonical were ever moved or missing, contaminating the cover render. Now
# the script fails loudly if canonical is absent.
CANONICAL = data_loader._resolve_path("data") / "shapefiles" / "canonical"
APPROX_MAJ_CANDIDATES = [
    CANONICAL / "ea_majority_2026_eds.gpkg",
]
APPROX_MIN_CANDIDATES = [
    CANONICAL / "ea_minority_2026_eds.gpkg",
]
# Phase 4C VA→2026-ED assignments (conservation-exact crosswalk authored by
# the topological resolver). Used by the heatmap fill to assign each VA
# its parent 2026 ED.
VA_TO_2026_ASSIGNMENTS = (
    REPO_ROOT / "analysis" / "assignment_va_to_2026_assignments.csv"
)

COVER_ART_PNG = data_loader._resolve_path("data") / "maps" / "cover_art.png"
COVER_ART_HIRES_SVG = data_loader._resolve_path("data") / "maps" / "cover_art_hires.svg"
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_browser() -> str:
    for path in CHROME_CANDIDATES:
        if Path(path).exists():
            return path
    raise FileNotFoundError("No Chrome or Edge found on this machine.")


# ==========================================================
# Cover art: Alberta silhouette with boundary-line overlay
# ==========================================================


VA_VOTES_PATH = (
    data_loader._resolve_path("data") / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
)

_DOCS = REPO_ROOT / "docs"

MAP_DATA_DIR = REPO_ROOT / "docs" / "data"
COORD_DECIMALS = 3  # millimetre precision; 3401 units are metres

# Per-map output paths and source configs for the interactive viewer.
MAP_VARIANTS = {
    "minority": {
        "candidates": APPROX_MIN_CANDIDATES,
        "shp": None,
        "name_candidates": ["name_2026", "EDName2025", "ED_NAME", "NAME"],
        "svg": _DOCS / "images" / "cover_art_minority_hires.svg",
        "json": _DOCS / "data" / "ed_hover_minority.json",
        "va_json": _DOCS / "data" / "va_hover_minority.json",
    },
    "majority": {
        "candidates": APPROX_MAJ_CANDIDATES,
        "shp": None,
        "name_candidates": ["name_2026", "EDName2025", "ED_NAME", "NAME"],
        "svg": _DOCS / "images" / "cover_art_majority_hires.svg",
        "json": _DOCS / "data" / "ed_hover_majority.json",
        "va_json": _DOCS / "data" / "va_hover_majority.json",
    },
    "2019": {
        "candidates": None,
        "shp": ALBERTA_EDS / "EDS_ENACTED_BILL33_15DEC2017.shp",
        "name_candidates": ["EDName2017", "EDName2025", "ED_NAME", "NAME"],
        "svg": _DOCS / "images" / "cover_art_2019_hires.svg",
        "json": _DOCS / "data" / "ed_hover_2019.json",
        "va_json": _DOCS / "data" / "va_hover_2019.json",
    },
}


def _load_official_2023_results() -> dict:
    """Parse data/raw/2023_results.xlsx for official 2023 EA results.

    Returns {ed_name_2019: {"ucp": int, "ndp": int}} keyed by 2019 ED name.
    Returns {} if the source files are missing.
    """
    import pandas as pd
    import geopandas as gpd

    xlsx_path = REPO_ROOT / "data" / "raw" / "2023_results.xlsx"
    shp_path = (
        REPO_ROOT / "data" / "shapefiles" / "reference"
        / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
    )
    if not xlsx_path.exists() or not shp_path.exists():
        return {}

    eds2019 = gpd.read_file(str(shp_path))
    num_to_name = {int(r.EDNumber20): r.EDName2017 for _, r in eds2019.iterrows()}

    xl = pd.ExcelFile(str(xlsx_path))
    results = {}
    for sheet in xl.sheet_names:
        ed_name = num_to_name.get(int(sheet))
        if ed_name is None:
            continue
        df = xl.parse(sheet, header=None)
        headers = df.iloc[0].tolist()
        ndp_cols = [i for i, h in enumerate(headers) if isinstance(h, str) and "\nNDP" in h]
        ucp_cols = [i for i, h in enumerate(headers) if isinstance(h, str) and "\nUCP" in h]
        total_row = next(
            (row for _, row in df.iterrows()
             if "Total (All Voting Options)" in str(row.iloc[1] if len(row) > 1 else "")),
            None,
        )
        if total_row is None or not ndp_cols or not ucp_cols:
            continue
        ndp = sum(float(total_row.iloc[c]) for c in ndp_cols if pd.notna(total_row.iloc[c]))
        ucp = sum(float(total_row.iloc[c]) for c in ucp_cols if pd.notna(total_row.iloc[c]))
        results[ed_name] = {"ucp": int(ucp), "ndp": int(ndp)}

    print(f"[build_cover] Loaded official 2023 results for {len(results)} 2019 EDs")
    return results


def _tag_ed_hover_paths(svg_path: Path, n_eds: int) -> None:
    """Post-process the hi-res SVG:
    1. Stamp data-ed-id and pointer-events on the hit-detection layer.
    2. Remove pacman nodes — VA paths with d-attr < 80 chars that are too tiny
       to render meaningfully and appear as artifacts at high zoom.
    3. Add a micro-stroke matching each VA's fill colour (stroke-width 0.002,
       paint-order: stroke fill) so coordinate-rounding gaps between adjacent
       polygons are invisible even at maximum zoom.
    """
    import re
    import xml.etree.ElementTree as ET
    from io import StringIO

    ns = "http://www.w3.org/2000/svg"
    ET.register_namespace("", ns)
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

    tree = ET.parse(str(svg_path))
    root = tree.getroot()

    # ── 1. Hit-detection layer ────────────────────────────────────────────────
    hit_g = root.find(f".//{{{ns}}}g[@id='ed_hover_layer']")
    if hit_g is None:
        print("[build_cover] WARN: ed_hover_layer not found in SVG — hover disabled")
    else:
        paths = hit_g.findall(f"{{{ns}}}path")
        for i, p in enumerate(paths[:n_eds]):
            p.set("data-ed-id", str(i))
            p.set("pointer-events", "all")
        print(f"[build_cover] Tagged {min(len(paths), n_eds)} hit-detection paths in SVG")

    # ── 2 & 3. VA layer: pacman removal + gap-filling micro-stroke ────────────
    pc2 = root.find(f".//{{{ns}}}g[@id='PatchCollection_2']")
    if pc2 is not None:
        removed = 0
        updated = 0
        _fill_re = re.compile(r"fill:([^;]+)")
        for i, path in enumerate(list(pc2.findall(f"{{{ns}}}path"))):
            d = path.get("d", "")
            if len(d) < 80:
                # Pacman node: tiny VA fragment, remove it entirely.
                pc2.remove(path)
                removed += 1
                continue
            path.set("data-va-id", str(i))
            # Micro-stroke matching fill; painted under fill so it only
            # bleeds outward into any coordinate-rounding gap (≤ 0.001 SVG units).
            style = path.get("style", "")
            m = _fill_re.search(style)
            fill = m.group(1).strip() if m else "none"
            path.set("style", f"{style};stroke:{fill};stroke-width:0.002;paint-order:stroke fill")
            updated += 1
        print(f"[build_cover] VA layer: removed {removed} pacman nodes, "
              f"added gap-fill stroke to {updated} paths")

    buf = StringIO()
    tree.write(buf, encoding="unicode")
    svg_path.write_text(buf.getvalue(), encoding="utf-8")


def _export_ed_hover_json(eds, name_col: str, out_path: Path) -> None:
    """Export per-ED tooltip data: name, vote split, official vote counts, population."""
    import json

    out_path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    has_official = "official_ucp" in eds.columns
    for i, row in eds.iterrows():
        ucp_share = float(row.get("ucp_share", 0.5))
        va_total = int(row.get("total", 0))

        if has_official:
            off_ucp = int(round(row.get("official_ucp", 0)))
            off_ndp = int(round(row.get("official_ndp", 0)))
            off_total = off_ucp + off_ndp
        else:
            off_total = 0

        if off_total > 0:
            ucp_votes = off_ucp
            ndp_votes = off_ndp
            votes = off_total
            ucp_pct = round(off_ucp / off_total * 100, 1)
            ndp_pct = round(off_ndp / off_total * 100, 1)
        else:
            ucp_votes = round(ucp_share * va_total)
            ndp_votes = va_total - ucp_votes
            votes = va_total
            ucp_pct = round(ucp_share * 100, 1)
            ndp_pct = round((1.0 - ucp_share) * 100, 1)

        records.append({
            "id": i,
            "name": str(row[name_col]),
            "ucp_pct": ucp_pct,
            "ndp_pct": ndp_pct,
            "ucp_votes": ucp_votes,
            "ndp_votes": ndp_votes,
            "votes": votes,
            "pop": int(row.get("pop", 0)),
            "va_count": int(row.get("va_count", 0)),
        })
    out_path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    print(f"[build_cover] Exported hover data for {len(records)} EDs -> {out_path.name}")


def _export_va_hover_json(va_render, va_ed_map, out_path: Path) -> None:
    """Export per-VA tooltip data: poll name, 2026 ED assignment, vote split."""
    import json

    out_path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for seq_i, (_, row) in enumerate(va_render.iterrows()):
        va_ucp   = float(row.get("va_ucp",   0) or 0)
        va_ndp   = float(row.get("va_ndp",   0) or 0)
        va_other = float(row.get("va_other", 0) or 0)
        two_party  = max(va_ucp + va_ndp, 1.0)
        in_person_votes = int(round(va_ucp + va_ndp + va_other))
        ucp_pct = round(va_ucp / two_party * 100, 1)
        ndp_pct = round(va_ndp / two_party * 100, 1)
        va_number = row.get("VA_NUMBER", "")
        ed_name_raw = va_ed_map.get(seq_i)
        records.append({
            "va_id":        seq_i,
            "ed_name":      "" if (ed_name_raw is None or ed_name_raw != ed_name_raw) else str(ed_name_raw),
            "poll_name":    f"Poll {va_number}",
            "ucp_votes":    int(round(va_ucp)),
            "ndp_votes":    int(round(va_ndp)),
            "other_votes":  int(round(va_other)),
            "in_person_votes": in_person_votes,
            "ucp_pct":    ucp_pct,
            "ndp_pct":    ndp_pct,
        })
    out_path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    print(f"[build_cover] Exported VA hover data for {len(records)} VAs -> {out_path.name}")


def _pick(candidates):
    for p in candidates:
        if p.exists():
            return p
    return None


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
            votes = va_total
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


def _prepare_map_data(map_key: str):
    """Load canonical geometry, join 2023 votes, compute per-VA fill colours.

    Returns (eds, name_col, va_render, va_ed_map). Pure data prep — no
    matplotlib rendering. Reused by both the PNG render and the GeoJSON export.
    """
    import matplotlib.colors as mcolors
    import numpy as np
    import pandas as pd

    cfg = MAP_VARIANTS[map_key]
    if cfg["shp"]:
        map_path = Path(cfg["shp"])
        if not map_path.exists():
            raise FileNotFoundError(f"2019 reference shapefile not found: {map_path}")
    else:
        map_path = _pick(cfg["candidates"])
        if map_path is None:
            raise FileNotFoundError(f"No {map_key} GPKG candidate available")
    print(f"[build_cover] [{map_key}] ED source: {map_path.name}")

    eds = gpd.read_file(map_path).to_crs(3401)
    name_col = next((c for c in cfg["name_candidates"] if c in eds.columns), eds.columns[0])
    eds = eds[eds.geometry.area > 1e6].copy().reset_index(drop=True)
    print(f"[build_cover] {len(eds)} non-empty EDs to render")

    # 2. Per-ED 2023 vote share via VA-centroid spatial join
    official_2023 = _load_official_2023_results()
    _va_ed_map = None
    if VA_VOTES_PATH.exists():
        va = gpd.read_file(VA_VOTES_PATH).to_crs(3401)
        _va_cols = {
            "va_ucp": va["va_ucp"].fillna(0),
            "va_ndp": va["va_ndp"].fillna(0),
            "parent_ed_2019": va["parent_ed_2019"].fillna(""),
        }
        if "pop_2021" in va.columns:
            _va_cols["pop_2021"] = va["pop_2021"].fillna(0)
        va_pts = gpd.GeoDataFrame(_va_cols, geometry=va.geometry.centroid, crs=3401)
        joined = gpd.sjoin(
            va_pts,
            eds[[name_col, "geometry"]],
            how="left",
            predicate="within",
        )
        _va_ed_map = joined.groupby(joined.index)[name_col].first()
        _agg_kw = {"ucp": ("va_ucp", "sum"), "ndp": ("va_ndp", "sum"), "va_count": ("va_ucp", "count")}
        if "pop_2021" in joined.columns:
            _agg_kw["pop"] = ("pop_2021", "sum")
        agg = joined.groupby(name_col).agg(**_agg_kw).reset_index()
        agg["total"] = (agg["ucp"] + agg["ndp"]).clip(lower=1)
        agg["ucp_share"] = agg["ucp"] / agg["total"]
        _merge_cols = [name_col, "ucp_share", "total", "va_count"] + (["pop"] if "pop" in agg.columns else [])
        eds = eds.merge(agg[_merge_cols], on=name_col, how="left")

        # Scale to official totals: distribute each 2019 ED's full results
        # (election-day + advance + vote-anywhere) to 2026 EDs proportionally
        # by how many VA election-day voters are in each 2026 ED slice.
        if official_2023:
            va_ed19_totals = (
                va.groupby("parent_ed_2019")[["va_ucp", "va_ndp"]]
                .sum()
                .assign(va_total=lambda d: (d["va_ucp"] + d["va_ndp"]).clip(lower=1))
                .reset_index()
            )
            joined_notnull = joined[joined[name_col].notna()].copy()
            pair = (
                joined_notnull.groupby([name_col, "parent_ed_2019"])[["va_ucp", "va_ndp"]]
                .sum()
                .reset_index()
            )
            pair = pair.merge(va_ed19_totals[["parent_ed_2019", "va_total"]], on="parent_ed_2019", how="left")
            pair["va_total"] = pair["va_total"].fillna(1)
            pair["frac"] = (pair["va_ucp"] + pair["va_ndp"]) / pair["va_total"]
            pair["off_ucp"] = pair.apply(
                lambda r: r["frac"] * official_2023.get(r["parent_ed_2019"], {}).get("ucp", 0), axis=1
            )
            pair["off_ndp"] = pair.apply(
                lambda r: r["frac"] * official_2023.get(r["parent_ed_2019"], {}).get("ndp", 0), axis=1
            )
            official_agg = pair.groupby(name_col)[["off_ucp", "off_ndp"]].sum().reset_index()
            official_agg.columns = [name_col, "official_ucp", "official_ndp"]
            eds = eds.merge(official_agg, on=name_col, how="left")
            eds["official_ucp"] = eds["official_ucp"].fillna(0)
            eds["official_ndp"] = eds["official_ndp"].fillna(0)
    else:
        print(
            f"[build_cover] WARN: {VA_VOTES_PATH.name} not found; "
            f"all EDs will render as neutral 50/50"
        )
        eds["ucp_share"] = 0.5
        eds["total"] = 0
        eds["pop"] = 0
    eds["ucp_share"] = eds["ucp_share"].fillna(0.5)
    eds["total"] = eds["total"].fillna(0)
    if "pop" not in eds.columns:
        eds["pop"] = 0
    eds["pop"] = eds["pop"].fillna(0).astype(int)
    eds["inferred"] = False
    print(
        f"[build_cover] {int((eds['total'] > 0).sum())}/{len(eds)} EDs received VA votes"
    )

    # 2b. Crosswalk-inheritance fallback for EDs the centroid-join missed.
    # The v0_8 reconstruction inherits some 2026 minority polygons from v0_7
    # (which itself inherits from 2019), and a handful end up in physical
    # positions where no 2023 VA centroid falls inside them. For those we
    # look up the 2019 parent ED(s) via minority_hybrid_crosswalk.csv
    # and aggregate the VAs that belonged to those parents — yielding the
    # 2019-vote-distribution-projected-onto-this-2026-name share. This
    # CANNOT model the partisan effect of the boundary shift; it's an
    # illustrative fill, not a quantitative claim, and the cover caption
    # discloses it.
    crosswalk_path = data_loader._resolve_path("data") / "minority_hybrid_crosswalk.csv"
    if VA_VOTES_PATH.exists() and crosswalk_path.exists():
        cw = pd.read_csv(crosswalk_path)
        # 2026-name -> list of 2019 parents (drop "(NEW)" sentinel rows)
        cw_real = cw[cw["current_2019"].astype(str) != "(NEW)"]
        parents_by_2026 = (
            cw_real.groupby("proposed_2026")["current_2019"]
            .apply(lambda s: [p for p in s.dropna().unique()])
            .to_dict()
        )
        miss_mask = eds["total"] == 0
        n_inferred = 0
        for idx in eds.index[miss_mask]:
            ed_name = eds.at[idx, name_col]
            parents = parents_by_2026.get(ed_name, [])
            if not parents:
                continue
            inh = va[va["parent_ed_2019"].isin(parents)]
            ucp_sum = float(inh["va_ucp"].fillna(0).sum())
            ndp_sum = float(inh["va_ndp"].fillna(0).sum())
            if (ucp_sum + ndp_sum) <= 0:
                continue
            eds.at[idx, "ucp_share"] = ucp_sum / (ucp_sum + ndp_sum)
            eds.at[idx, "total"] = ucp_sum + ndp_sum
            eds.at[idx, "inferred"] = True
            n_inferred += 1
        print(
            f"[build_cover] inferred 2019-parent vote share for "
            f"{n_inferred} EDs missed by centroid-join"
        )

    # 2c. Final fallback for any ED still grey (genuinely new 2026
    # creations with no 2019 parent in the crosswalk, or parent rows
    # whose VAs all aggregated to zero votes). Use the K nearest VA
    # centroids to the ED's own centroid. Crude, but guarantees the
    # cover renders no grey districts.
    if VA_VOTES_PATH.exists():
        from shapely.geometry import Point

        K = 25
        still_missing = eds["total"] == 0
        n_nearest = 0
        if still_missing.any():
            va_centroids = list(
                zip(
                    va.geometry.centroid.x.values,
                    va.geometry.centroid.y.values,
                    va["va_ucp"].fillna(0).values,
                    va["va_ndp"].fillna(0).values,
                )
            )
            for idx in eds.index[still_missing]:
                gc = eds.at[idx, "geometry"].centroid
                dists = [
                    (((cx - gc.x) ** 2 + (cy - gc.y) ** 2), u, n)
                    for cx, cy, u, n in va_centroids
                ]
                dists.sort(key=lambda t: t[0])
                near = dists[:K]
                ucp_sum = float(sum(u for _, u, _ in near))
                ndp_sum = float(sum(n for _, _, n in near))
                if (ucp_sum + ndp_sum) <= 0:
                    continue
                eds.at[idx, "ucp_share"] = ucp_sum / (ucp_sum + ndp_sum)
                eds.at[idx, "total"] = ucp_sum + ndp_sum
                eds.at[idx, "inferred"] = True
                n_nearest += 1
            print(
                f"[build_cover] nearest-{K}-VA fallback used for "
                f"{n_nearest} EDs with no crosswalk parent"
            )

    # 3. Direct UCP-blue → NDP-orange interpolation. Tighter norm window
    #    (35–75%) pushes more EDs toward full saturation for a bolder look.
    #    Endpoints are the parties' official brand colours:
    #    NDP orange #F58220 (Pantone 1505 C) / UCP blue #1C4583 (2026 logo).
    ndp_orange = (0.960784, 0.509804, 0.125490)   # #F58220
    ucp_blue   = (0.109804, 0.270588, 0.513725)   # #1C4583
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "ucp_ndp_direct", [ndp_orange, ucp_blue], N=256
    )
    norm = mcolors.Normalize(vmin=0.35, vmax=0.75, clip=True)

    # Build the per-VA dataframe. Hue is determined by EACH VA's OWN 2023
    # partisan share (not the parent ED's average), so a UCP stronghold
    # inside an NDP-leaning ED renders as a blue cluster on an orange
    # field, and an NDP stronghold inside a UCP ED renders as orange
    # inside the surrounding blue. ED-level partisan lean still emerges
    # naturally because most VAs in an ED tend to lean the same way.
    va_render = va.copy().reset_index(drop=True)
    # to_crs(3401) splits 3 VAs into 2–5 parts, producing more SVG paths than rows.
    # data-va-id is assigned by enumerate over SVG paths, so any split breaks the
    # path-index → JSON-va_id correspondence for all subsequent rows.
    # Fix: replace multi-part geometries with their largest polygon part (one path per row).
    va_render["geometry"] = [
        max(g.geoms, key=lambda p: p.area) if g.geom_type == "MultiPolygon" and len(g.geoms) > 1 else g
        for g in va_render.geometry
    ]
    va_ucp_total = va_render["va_ucp"].fillna(0)
    va_ndp_total = va_render["va_ndp"].fillna(0)
    va_two_party = (va_ucp_total + va_ndp_total).clip(lower=1.0)
    va_render["parent_ucp_share"] = va_ucp_total / va_two_party

    # Per-VA population density and lightness modulation.
    # pop_2021 is on the va frame from the centroid build above; if missing,
    # fall back to vote-weighted proxy.
    if "pop_2021" in va_render.columns:
        pop = va_render["pop_2021"].fillna(0).clip(lower=0)
    else:
        pop = (
            va_render["va_ucp"].fillna(0)
            + va_render["va_ndp"].fillna(0)
            + va_render["va_other"].fillna(0)
        )
    area_m2 = va_render.geometry.area.clip(lower=1.0)
    density = pop / area_m2  # people per m^2
    # Heatmap-style: log-scale density; blend each VA's partisan colour
    # with cover-ivory by a lightness weight in [0, 1].
    # weight=0 -> pure ivory (very low density), weight=1 -> full saturated
    # partisan colour (very high density).
    log_d = np.log10(density.replace(0, np.nan)).fillna(-12.0)
    d_min, d_max = -8.5, -3.5
    weight = ((log_d - d_min) / (d_max - d_min)).clip(0.0, 1.0)

    _white = np.array([1.0, 1.0, 1.0])

    def _va_fill(ucp_share, w):
        # Density encoded as lightness, not alpha — fully opaque throughout.
        # Sparse rural → pale tint of the partisan colour.
        # Dense urban  → full saturation.
        # No semi-transparent patches; the map reads cleanly at any zoom.
        base = np.array(cmap(norm(ucp_share)))[:3]
        t = float(np.clip(w ** 0.6, 0.18, 1.0))   # gamma curve keeps rural readable
        colored = (1.0 - t) * _white + t * base
        return (*colored, 1.0)   # always fully opaque

    va_render["_fill"] = [
        _va_fill(s, w) for s, w in zip(va_render["parent_ucp_share"], weight.values)
    ]

    return eds, name_col, va_render, _va_ed_map


def build_cover_art(map_key: str = "minority") -> Path:
    """Render one of three map variants coloured by 2023 two-party vote share.

    map_key: "minority" | "majority" | "2019"
    """
    cfg = MAP_VARIANTS[map_key]
    eds, name_col, va_render, _va_ed_map = _prepare_map_data(map_key)

    # 4. Render — VA-level fill with population-density lightness modulation.
    #    Each VA gets the partisan colour of its assigned 2026 ED (hue), and
    #    a lightness scaled by VA-local population density (paler = sparse,
    #    darker = dense). This gives the reader two signals in a single
    #    image: the partisan-leaning hue (blue/orange) and the population-
    #    centre heatmap (where within an ED the people actually are). The
    #    v0_9 substrate's polygon boundaries are overlaid as thin lines so
    #    the 89-district structure remains visible.
    fig, ax = plt.subplots(figsize=(6.0, 9), dpi=300)
    fig.patch.set_facecolor('none')   # transparent background
    ax.set_facecolor('none')          # transparent axes
    ax.set_aspect("equal")
    ax.axis("off")

    # 4a. Province interior fill: white so sparse rural areas (low alpha VAs)
    #     show white rather than the transparent page background. Outside the
    #     province boundary remains transparent (shows the dark page through).
    province = eds.dissolve()
    province.plot(ax=ax, color="white", linewidth=0, rasterized=False)

    # 4b. VA layer on top — heatmap-modulated fills carry the population-
    #     density signal where VAs exist (i.e. where people actually live).
    # VA edges at 0.2 so the tessellation is subtly visible; ED edges are
    # exactly 2× that (0.4) so the district structure reads over the VA grid.
    va_render.plot(
        ax=ax,
        color=va_render["_fill"].tolist(),
        edgecolor="none",
        linewidth=0,
        rasterized=False,
    )

    # 4c. ED boundaries — tagged with GID so the viewer can recolour them
    #     dynamically per active map (purple / teal / grey).
    _nb = len(ax.collections)
    eds.boundary.plot(
        ax=ax,
        edgecolor="#718096",  # neutral grey; viewer overrides per map key
        linewidth=0.1,
        rasterized=False,
    )
    for _c in ax.collections[_nb:]:
        _c.set_gid("ed_boundary_layer")

    # 4d. Provincial outline: use unary_union to merge all ED polygons into a
    #     single geometry before drawing the boundary — this removes interior
    #     topology gaps that would otherwise render as spurious red line caps.
    from shapely.ops import unary_union
    _outer = gpd.GeoDataFrame(geometry=[unary_union(eds.geometry)], crs=eds.crs)
    _outer.boundary.plot(
        ax=ax,
        edgecolor="#7a1f1f",  # title-accent red (outer edge only)
        linewidth=0.2,
        rasterized=False,
    )

    # 4e. Transparent hit-detection polygon layer — one polygon per ED, invisible
    #     but tagged with data-ed-id in SVG post-processing so the browser can
    #     identify which ED the cursor is over for the hover tooltip.
    _n = len(ax.collections)
    eds.plot(ax=ax, facecolor=(0, 0, 0, 0), edgecolor=(0, 0, 0, 0), linewidth=0, rasterized=False)
    for _c in ax.collections[_n:]:
        _c.set_gid("ed_hover_layer")

    ax.margins(0.005)
    plt.tight_layout(pad=0)

    svg_out = cfg["svg"]
    json_out = cfg["json"]
    svg_out.parent.mkdir(parents=True, exist_ok=True)

    _save_kwargs = dict(bbox_inches="tight", pad_inches=0.02, facecolor="none", transparent=True)
    # Screen-res PNG (minority only) — still used by the PDF cover + WebGL fallback.
    if map_key == "minority":
        COVER_ART_PNG.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(COVER_ART_PNG, dpi=200, **_save_kwargs)
        print(f"[build_cover] Wrote screen-res art {COVER_ART_PNG.relative_to(REPO_ROOT)}")
    plt.close(fig)

    # Interactive-explorer data (replaces the 37 MB hi-res SVG).
    _export_map_geojson(map_key, eds, name_col, va_render, _va_ed_map)

    # Legacy hover JSON kept until the viewer cutover (Plan 3).
    _export_ed_hover_json(eds, name_col, json_out)
    va_json_out = cfg.get("va_json")
    if va_json_out is not None and _va_ed_map is not None:
        _export_va_hover_json(va_render, _va_ed_map, va_json_out)

    # Keep legacy ed_hover.json in sync so the pre-cutover embed still works (removed in Plan 3).
    if map_key == "minority":
        import shutil
        shutil.copy2(str(json_out), str(REPO_ROOT / "docs" / "data" / "ed_hover.json"))

    return COVER_ART_PNG


def build_map_variants() -> None:
    """Build majority and 2019 map variants for the interactive viewer selector."""
    for key in ("majority", "2019"):
        print(f"[build_cover] Building {key} map variant...")
        build_cover_art(map_key=key)


# ==========================================================
# Orchestrator
# ==========================================================


def main() -> int:
    # 1. Hero art (minority = default / cover map)
    build_cover_art()
    # 2. Majority and 2019 variants + map-explorer GeoJSON/hover exports
    build_map_variants()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
