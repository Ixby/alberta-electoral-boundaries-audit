"""
_fetch_osm_natural.py — fetch Alberta-wide OSM highways and rivers for the
natural-anchoring secondary check. Caches to data/osm/ as GeoJSON-like JSON
so subsequent runs skip the Overpass round-trip.

Highway filter: motorway, trunk, primary, secondary (matches the major-road
classes used by analysis/methodology/shape_refinement.md). Dropped
tertiary to keep the network from being dominated by intra-city street grids
that would inflate every map's anchoring score.

River filter: waterway=river (excludes streams, canals, ditches).

Forward:
    analysis/scripts/score_natural_anchoring.py
Backward:
    Overpass API (overpass-api.de) — public OSM mirror
"""

from __future__ import annotations

import json
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

import geopandas as gpd
from shapely.geometry import LineString

ROOT = Path(__file__).resolve().parent.parent.parent
OSM_DIR = ROOT / "data" / "osm"
OSM_DIR.mkdir(parents=True, exist_ok=True)

# Alberta bbox (S, W, N, E) — WGS84
AB_BBOX = (49.0, -120.05, 60.05, -110.0)

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

UA = "alberta-electoral-audit/0.9 (research; contact wconn161@mtroyal.ca)"


def _overpass_query(ql: str, retries: int = 3) -> dict:
    """POST a query to Overpass; round-robin endpoints on failure."""
    last_err: Exception | None = None
    for endpoint in OVERPASS_URLS:
        for attempt in range(retries):
            try:
                req = urllib.request.Request(
                    endpoint,
                    data=urllib.parse.urlencode({"data": ql}).encode("utf-8"),
                    headers={"User-Agent": UA},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=600) as resp:
                    raw = resp.read()
                    return json.loads(raw)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
                last_err = e
                wait = 30 * (attempt + 1)
                print(
                    f"  [overpass] {endpoint} attempt {attempt+1} failed: {e}; sleeping {wait}s"
                )
                time.sleep(wait)
    raise RuntimeError(f"All Overpass endpoints failed; last error: {last_err}")


def _payload_to_gdf(payload: dict) -> gpd.GeoDataFrame:
    lines: list[LineString] = []
    for el in payload.get("elements", []):
        if el.get("type") != "way":
            continue
        g = el.get("geometry") or []
        if len(g) < 2:
            continue
        try:
            lines.append(LineString([(c["lon"], c["lat"]) for c in g]))
        except Exception:
            continue
    return gpd.GeoDataFrame(geometry=lines, crs="EPSG:4326")


def _fetch_and_persist(label: str, ql: str, gpkg_name: str) -> Path:
    """Fetch from Overpass, write GPKG (committed) and JSON (gitignored).

    The GPKG is the canonical on-disk cache (committed, ~30 MB combined for
    highways+rivers). The JSON is a debug artefact — preserves the raw
    Overpass payload (incl. tag dictionaries) for future filtering work.
    """
    gpkg_out = OSM_DIR / gpkg_name
    json_out = gpkg_out.with_suffix(".json")
    if gpkg_out.exists():
        print(f"  [cache hit] {gpkg_out.name} ({gpkg_out.stat().st_size/1e6:.1f} MB)")
        return gpkg_out
    print(f"  [overpass] fetching Alberta {label}...")
    t0 = time.time()
    data = _overpass_query(ql)
    json_out.write_text(json.dumps(data))
    gdf = _payload_to_gdf(data)
    gdf.to_file(gpkg_out, driver="GPKG")
    print(
        f"  [overpass] {len(gdf)} ways in {time.time()-t0:.0f}s -> "
        f"{gpkg_out.name} ({gpkg_out.stat().st_size/1e6:.1f} MB) "
        f"(+ debug JSON {json_out.stat().st_size/1e6:.1f} MB)"
    )
    return gpkg_out


def fetch_highways() -> Path:
    s, w, n, e = AB_BBOX
    ql = f"""
[out:json][timeout:540];
(
  way["highway"~"^(motorway|trunk|primary|secondary)$"]({s},{w},{n},{e});
);
out geom;
"""
    return _fetch_and_persist(
        "highways (motorway|trunk|primary|secondary)",
        ql,
        "alberta_osm_highways.gpkg",
    )


def fetch_rivers() -> Path:
    s, w, n, e = AB_BBOX
    ql = f"""
[out:json][timeout:540];
(
  way["waterway"="river"]({s},{w},{n},{e});
);
out geom;
"""
    return _fetch_and_persist(
        "rivers (waterway=river)",
        ql,
        "alberta_osm_rivers.gpkg",
    )


if __name__ == "__main__":
    fetch_highways()
    fetch_rivers()
    print("OK")
