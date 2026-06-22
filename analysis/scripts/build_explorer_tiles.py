# Map explorer tiler — custom EPSG:3401 quadtree tiling, PACKED into one archive.
# VA heatmap is shared across all 3 maps (fills identical); only ED boundaries
# and each VA's district label differ per map.
#
# Output: viewer/static/mapdata/  (served at /mapdata/). Regenerate with:
#   python analysis/scripts/build_explorer_tiles.py   (full retile ~5-6 min)
#
# Data source: build_cover._prepare_map_data (analysis/scripts/build_cover.py).
# It also reads docs/data/map_meta.json (origin) and four community-name inputs
# under C:\tmp (calgary_comm.json, edmonton_nbhd.json, osm_nbhd.json,
# cgn_ab/cgn_ab_csv_eng.csv); those caches are not yet relocated into the repo.
import json, sys, os, time, shutil, struct, hashlib
from pathlib import Path
import numpy as np

REPO = Path(r"C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit")
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "scripts" / "utils"))
OUT = REPO / "viewer" / "static" / "mapdata"

import build_cover
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import box
from shapely.ops import unary_union
import topojson as tp

MINZ, MAXZ = 0, 10           # z10 tol ~4.8m = source floor (25% of VA segs <5m); past z10 lines/VAs drift
TILE_PX = 256
MAPS = ["minority", "majority", "2019"]


def write_bundle_bin(path, tiles):
    """Binary bundle: uint32 headerLen | header JSON {key:[start,len]} | pad to 4 | body.
       Each tile blob: uint32 nRings | per ring: uint16 vaId, uint16 nPts, nPts*2 float32 XY.
       Layout keeps every coord block 4-byte aligned so the viewer maps Float32Array views
       with zero copy."""
    body = bytearray()
    index = {}
    for k, feats in tiles.items():
        start = len(body)
        body += struct.pack("<I", len(feats))
        for vid, coords in feats:
            npts = len(coords)
            if npts > 65535:
                raise ValueError(f"ring too long: {npts} pts in tile {k}")
            body += struct.pack("<HH", vid, npts)
            body += np.asarray(coords, dtype="<f4").tobytes()
        index[k] = [start, len(body) - start]
    header = json.dumps(index, separators=(",", ":")).encode("utf-8")
    pad = (-(4 + len(header))) % 4
    out = bytearray()
    out += struct.pack("<I", len(header))
    out += header
    out += b"\x00" * pad
    out += body
    data = bytes(out)
    Path(path).write_bytes(data)
    return len(data), hashlib.sha1(data).hexdigest()[:12]   # (bytes, content version)


def rings_of(geom):
    if geom.is_empty:
        return
    if geom.geom_type == "Polygon":
        yield list(geom.exterior.coords)
    elif geom.geom_type == "MultiPolygon":
        for g in geom.geoms:
            if not g.is_empty:
                yield list(g.exterior.coords)


def community_names(va_render):
    """Community per VA, three tiers:
      1. Calgary + Edmonton official neighbourhood polygons (precise point-in-polygon → 'in X')
      2. OSM neighbourhood/suburb points within ~1.5 km (smaller municipalities → 'in X')
      3. nearest CGNDB populated place (rural fallback → 'near X')
    Returns (names, urban_flags)."""
    import json
    cal = gpd.read_file(r'C:\tmp\calgary_comm.json').set_crs(4326, allow_override=True)
    cal = cal[cal['class'] == 'Residential'].copy(); cal['nb'] = cal['name'].str.title()
    edm = gpd.read_file(r'C:\tmp\edmonton_nbhd.json').set_crs(4326, allow_override=True); edm['nb'] = edm['descriptiv']
    urban = gpd.GeoDataFrame(pd.concat([cal[['nb', 'geometry']], edm[['nb', 'geometry']]], ignore_index=True), crs=4326).to_crs(3401)
    urban = urban[urban['nb'].notna()]

    osm = json.load(open(r'C:\tmp\osm_nbhd.json', encoding='utf-8'))
    recs = []
    for e in osm['elements']:
        nm = e.get('tags', {}).get('name')
        if not nm:
            continue
        c = e if e['type'] == 'node' else e.get('center', {})
        if c.get('lon') and c.get('lat'):
            recs.append({'nb': nm, 'lon': c['lon'], 'lat': c['lat']})
    osm_pts = gpd.GeoDataFrame(recs, geometry=gpd.points_from_xy([r['lon'] for r in recs], [r['lat'] for r in recs]), crs=4326).to_crs(3401)

    POP = {'City', 'Town', 'Village', 'Summer Village', 'Hamlet', 'Locality',
           'First Nation Administrative Location', 'Indian Reserve', 'Municipal District', 'County'}
    cgn = pd.read_csv(r'C:\tmp\cgn_ab\cgn_ab_csv_eng.csv')
    cgn = cgn[cgn['Generic Term'].isin(POP)]
    gn = gpd.GeoDataFrame(cgn, geometry=gpd.points_from_xy(cgn['Longitude'], cgn['Latitude']), crs=4326).to_crs(3401)

    cent = gpd.GeoDataFrame(geometry=list(va_render.geometry.centroid), crs=3401)
    uj = gpd.sjoin(cent, urban[['nb', 'geometry']], how='left', predicate='within')
    uj = uj[~uj.index.duplicated(keep='first')].sort_index()
    oj = gpd.sjoin_nearest(cent, osm_pts[['nb', 'geometry']], how='left', distance_col='_d')
    oj = oj[~oj.index.duplicated(keep='first')].sort_index()
    nj = gpd.sjoin_nearest(cent, gn[['Geographical Name', 'geometry']], how='left')
    nj = nj[~nj.index.duplicated(keep='first')].sort_index()
    un = list(uj['nb']); on = list(oj['nb']); od = list(oj['_d']); rn = list(nj['Geographical Name'].fillna(''))
    OSM_R = 1500
    names, urb = [], []
    for i in range(len(va_render)):
        u = un[i] if i < len(un) else None
        if u is not None and u == u and str(u).strip():
            names.append(str(u)); urb.append(True)
        elif i < len(on) and on[i] is not None and on[i] == on[i] and od[i] <= OSM_R:
            names.append(str(on[i])); urb.append(True)
        else:
            names.append(rn[i] if i < len(rn) else ''); urb.append(False)
    return names, urb


def ed_rings(eds, ox, oy):
    feats = []
    for geom in eds.geometry.simplify(60.0, preserve_topology=True):
        for ring in rings_of(geom):
            feats.append([[round(px - ox, 2), round(py - oy, 2)] for px, py in ring])
    return feats


def line_coords(geom, ox, oy):
    """Flatten any geometry to a list of origin-shifted, rounded coord lists (lines only)."""
    out = []
    if geom is None or geom.is_empty:
        return out
    gt = geom.geom_type
    if gt == "LineString":
        out.append([[round(x - ox, 2), round(y - oy, 2)] for x, y in geom.coords])
    elif gt == "MultiLineString":
        for g in geom.geoms:
            out.append([[round(x - ox, 2), round(y - oy, 2)] for x, y in g.coords])
    elif gt == "GeometryCollection":
        for g in geom.geoms:
            out += line_coords(g, ox, oy)
    return out


def ed_label_points(vr, labels, ox, oy):
    """One label anchor (representative interior point) per district in this map."""
    from collections import defaultdict
    groups = defaultdict(list)
    for i, nm in enumerate(labels):
        if nm:
            groups[nm].append(vr.geometry.iloc[i])
    out = []
    for nm, geoms in groups.items():
        try:
            pt = unary_union(geoms).representative_point()
        except Exception:
            pt = max(geoms, key=lambda g: g.area).representative_point()
        out.append([nm, round(pt.x - ox, 2), round(pt.y - oy, 2)])
    return out


def all_arc_lines(topo_dict, ox, oy):
    """Every arc in a topology as a polyline — used for the faint per-VA hairline outline."""
    sx, sy = float(topo_dict["transform"]["scale"][0]), float(topo_dict["transform"]["scale"][1])
    tx, ty = float(topo_dict["transform"]["translate"][0]), float(topo_dict["transform"]["translate"][1])
    out = []
    for arc in topo_dict["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append([round(x * sx + tx - ox, 2), round(y * sy + ty - oy, 2)])
        if len(pts) >= 2:
            out.append(pts)
    return out


def build_ed_edges(topo_dict, label_arrays, ox, oy):
    """ED boundary lines from the SHARED VA topology: an arc between two VAs is a boundary in map k
    iff the two VAs carry different district labels in map k. m=[min,maj,2019].

    Because all three maps share the exact same VA geometry (only the labels differ), there is zero
    inter-map drift — an agreeing boundary is the *identical* arc in every map, so no shimmer and no
    snapping is needed. And every line falls on a VA edge, so it can never cut across a polling
    station the way the district-shapefile lines did. 1-user (perimeter) arcs are dropped, so
    isolated population clusters (Banff townsite, Lake Louise) aren't falsely ringed as their own ED.
    The trade-off — district boundaries through unpopulated land aren't drawn — is what avoids the
    false rings in the first place."""
    sx, sy = float(topo_dict["transform"]["scale"][0]), float(topo_dict["transform"]["scale"][1])
    tx, ty = float(topo_dict["transform"]["translate"][0]), float(topo_dict["transform"]["translate"][1])
    arcs = topo_dict["arcs"]

    def decode(idx):
        x = y = 0
        out = []
        for dx, dy in arcs[idx]:
            x += dx; y += dy
            out.append([round(x * sx + tx - ox, 2), round(y * sy + ty - oy, 2)])
        return out

    # arc index -> set of VA ids that reference it
    users = {}
    for geom in topo_dict["objects"]["data"]["geometries"]:
        vi = int(geom["properties"]["i"])
        polys = geom["arcs"] if geom["type"] == "MultiPolygon" else [geom["arcs"]]
        for poly in polys:
            for ring in poly:
                for ai in ring:
                    users.setdefault(ai if ai >= 0 else ~ai, set()).add(vi)

    LM = [label_arrays[m] for m in MAPS]
    edges = []
    for idx, us in users.items():
        if len(us) != 2:
            continue                              # 1-user perimeter dropped (no false rings); >2 skip
        a, b = sorted(us)
        m = [1 if LM[k][a] != LM[k][b] else 0 for k in range(3)]
        if not any(m):
            continue                              # interior in all maps → never drawn
        coords = decode(idx)
        if len(coords) >= 2:
            edges.append({"g": coords, "m": m})
    print(f"[spike] ed_edges (VA-derived, on VA edges, no drift): {len(edges)} arcs")
    return {"edges": edges, "outline": []}


def build_ed_index():
    """Per-map ED location index for the deck.gl explorer's name search.

    For every district in each map, emit {name, cx, cy, zoom} where (cx, cy) is the
    origin-shifted (EPSG:3401 minus map_meta origin) centroid and `zoom` is a fit-zoom
    that frames the district's bounding box:  zoom = 1 - log2(max(w, h) / 256)  — the
    same formula the viewer uses for the overview floor (DeckExplorer.svelte computes
    the overview as `1 - log2(side / 256)`), applied to the district's own side.

    FAST: loads only the canonical ED polygons per map (the same _prepare_map_data the
    tiler uses) and computes centroids/bounds — NO tiling, no topology. Output:
    viewer/static/mapdata/ed_index_<map>.json. Run via `--ed-index` or build_ed_index().
    """
    meta = json.loads((REPO / "docs" / "data" / "map_meta.json").read_text())
    ox, oy = meta["origin_x"], meta["origin_y"]
    OUT.mkdir(parents=True, exist_ok=True)
    for mk in MAPS:
        eds, name_col, _vr, _vem = build_cover._prepare_map_data(mk)
        eds = eds.to_crs(3401)
        # One entry per distinct district name: union the (possibly multi-row /
        # multipolygon) geometry so centroid + bbox describe the whole district.
        index = []
        for nm, grp in eds.groupby(name_col):
            if nm is None or nm != nm or not str(nm).strip():
                continue
            geom = unary_union(list(grp.geometry))
            if geom.is_empty:
                continue
            c = geom.centroid
            minx, miny, maxx, maxy = geom.bounds
            w = max(maxx - minx, 1.0)
            h = max(maxy - miny, 1.0)
            zoom = 1.0 - float(np.log2(max(w, h) / TILE_PX))
            index.append({
                "name": str(nm),
                "cx": round(c.x - ox, 2),
                "cy": round(c.y - oy, 2),
                "zoom": round(zoom, 4),
            })
        index.sort(key=lambda r: r["name"])
        (OUT / f"ed_index_{mk}.json").write_text(
            json.dumps(index, separators=(",", ":")), encoding="utf-8"
        )
        print(f"  ed_index_{mk}.json: {len(index)} EDs")


def main():
    t0 = time.time()
    shutil.rmtree(OUT / "va", ignore_errors=True)   # drop old loose tiles
    OUT.mkdir(parents=True, exist_ok=True)

    # ── Shared VA layer (from minority; fills + communities identical across maps) ──
    eds, name_col, va_render, va_ed_map = build_cover._prepare_map_data("minority")
    meta = json.loads((REPO / "docs" / "data" / "map_meta.json").read_text())
    ox, oy = meta["origin_x"], meta["origin_y"]
    minx, miny, maxx, maxy = eds.total_bounds
    side = max(maxx - minx, maxy - miny)
    print(f"origin=({ox:.1f},{oy:.1f}) VAs={len(va_render)} side={side:.0f}m")

    communities, urban = community_names(va_render)
    print(f"[spike] communities: {sum(urban)} urban (in), {sum(1 for c in communities if c)-sum(urban)} rural (near)")

    va_props = []
    for seq_i, (_, row) in enumerate(va_render.iterrows()):
        r, g, b, _a = row["_fill"]
        va_ucp = float(row.get("va_ucp", 0) or 0); va_ndp = float(row.get("va_ndp", 0) or 0)
        va_other = float(row.get("va_other", 0) or 0)
        two = max(va_ucp + va_ndp, 1.0)
        va_props.append({
            "id": seq_i,
            "fill": [round(r * 255), round(g * 255), round(b * 255)],
            "name": f"Poll {row.get('VA_NUMBER', '')}",
            "community": communities[seq_i] if seq_i < len(communities) else "",
            "cin": 1 if (seq_i < len(urban) and urban[seq_i]) else 0,
            "ucp": round(va_ucp / two * 100, 1), "ndp": round(va_ndp / two * 100, 1),
            "votes": round(va_ucp + va_ndp + va_other),   # total ballots cast in this VA
        })

    va = gpd.GeoDataFrame({"i": range(len(va_render))}, geometry=list(va_render.geometry), crs=3401)
    print("[spike] building shared-edge topology...")
    t1 = time.time()
    topo = tp.Topology(va, prequantize=1_000_000, shared_coords=True)
    print(f"[spike] topology built in {time.time()-t1:.0f}s")

    packed = {}
    tile_counts = {}
    va_topo_dict = None
    for z in range(MAXZ, MINZ - 1, -1):
        n = 2 ** z
        tsize = side / n
        tol = tsize / TILE_PX
        topo = topo.toposimplify(tol)
        if z == 7:
            va_topo_dict = topo.to_dict()          # ~38m VA arcs → faint per-VA hairline outline
        sva = topo.to_gdf().reset_index(drop=True)
        sva["geometry"] = sva.geometry.buffer(0)   # repair simplification self-intersections
        sidx = sva.sindex
        written = 0
        for x in range(n):
            tx0 = minx + x * tsize
            for y in range(n):
                ty0 = miny + y * tsize
                tb = box(tx0, ty0, tx0 + tsize, ty0 + tsize)
                cand = list(sidx.query(tb))
                if len(cand) == 0:
                    continue
                feats = []
                for ci in cand:
                    g = sva.geometry.iloc[ci]
                    if g is None or g.is_empty or not g.intersects(tb):
                        continue
                    try:
                        clipped = g.intersection(tb)
                    except Exception:
                        continue
                    vid = int(sva["i"].iloc[ci])
                    for ring in rings_of(clipped):
                        feats.append((vid, [(px - ox, py - oy) for px, py in ring]))
                if feats:
                    packed[f"{z}/{x}/{y}"] = feats
                    written += 1
        tile_counts[z] = written
        print(f"  z={z}: tol={tol:.2f}m, {written} tiles")

    # One bin per zoom level — the viewer loads levels 0..current+1 on demand, so a session
    # only downloads the depths it actually views (overview ≈ z0-3; the heavy z7/z8 only when deep).
    BUNDLES = [(z, z) for z in range(MINZ, MAXZ + 1)]
    bundle_info = []
    for lo, hi in BUNDLES:
        bd = {k: v for k, v in packed.items() if lo <= int(k.split("/")[0]) <= hi}
        fn = f"va_{lo}_{hi}.bin"
        nbytes, ver = write_bundle_bin(OUT / fn, bd)
        mb = nbytes / 1e6
        bundle_info.append({"lo": lo, "hi": hi, "file": fn, "mb": round(mb, 2), "tiles": len(bd), "ver": ver})
        print(f"  bundle z{lo}-{hi}: {len(bd)} tiles, {mb:.1f}MB  v{ver}")
    va_mb = sum(b["mb"] for b in bundle_info)

    # Per-VA properties (fill, name, community, votes) — loaded once, indexed by VA id.
    (OUT / "va_props.json").write_text(json.dumps(va_props, separators=(",", ":")), encoding="utf-8")
    print(f"  va_props.json: {len(va_props)} VAs, {(OUT/'va_props.json').stat().st_size/1e6:.2f}MB")

    # ── Per-map: district polygons + VA→district labels (VA order identical across maps) ──
    label_arrays = {}
    map_eds = {}
    for mk in MAPS:
        e, ncol, vr, vem = build_cover._prepare_map_data(mk)
        map_eds[mk] = e
        labels = []
        for i in range(len(vr)):
            v = vem.get(i)
            labels.append("" if (v is None or v != v) else str(v))
        label_arrays[mk] = labels
        (OUT / f"valabels_{mk}.json").write_text(json.dumps(labels, separators=(",", ":")), encoding="utf-8")
        print(f"  {mk}: {len(e)} EDs, {sum(1 for l in labels if l)} labelled VAs")

    # ── ED boundary lines = the ACTUAL canonical district boundary for each map, drawn directly. ──
    # One clean, consistent, accurate line per map — no VA-edge rounding, no rural fill patches. An
    # earlier design rounded boundaries onto polling-area (VA) edges to get zero inter-map drift for
    # the crossfade, but the 2026 maps redrew boundaries across the 2023 polls, so the rounded line
    # staircased and diverged from the truth (and patching the gaps doubled lines all over). The
    # canonical boundary is simpler and correct: where it crosses a coloured poll it just reads as a
    # boundary over the heatmap. Each map's polygons are independent geometry, so an edge belongs to
    # exactly one map (m one-hot); the crossfade still works (each map fades its own boundary, and
    # where two maps differ you see the change directly).
    #
    # Extraction uses topojson: toposimplify only trims arcs' INTERIOR vertices and keeps every arc
    # endpoint (junction) fixed, so simplified arcs always still connect — it cannot open gaps (a
    # per-line simplify drifts shared endpoints apart and DOES open gaps). The raw 2019 shapefile
    # digitises each district separately, so its shared borders don't coincide; topojson can't always
    # pair them, but that's fine — we decode EVERY arc and drop only those on the province silhouette,
    # keeping 2019's doubled-but-contiguous internal lines (offset < ~12m, invisible). The silhouette
    # is taken from the HOLE-FILLED union (2019's non-coincident borders leave sliver-holes that would
    # otherwise be mistaken for exterior and punch gaps in the interior). ──
    from shapely.ops import unary_union as _uu
    from shapely.geometry import LineString as _LS, Polygon as _Poly
    SIMP = 4.0    # m — at the z10 source floor (1px≈4.8m): sub-pixel sharp at every supported zoom
    EXT_TOL = 25.0   # m — arc whose midpoint is within this of the province silhouette = exterior, drop
    ee = {"edges": [], "outline": []}
    for k, mk in enumerate(MAPS):
        meds = map_eds[mk].to_crs(3401)
        prov = _uu(list(meds.geometry))
        prov_ext = _uu([_Poly(p.exterior) for p in (prov.geoms if prov.geom_type == "MultiPolygon" else [prov])]).boundary
        gdf = gpd.GeoDataFrame({"i": range(len(meds))}, geometry=list(meds.geometry), crs=3401)
        topo = tp.Topology(gdf, prequantize=1_000_000, shared_coords=False).toposimplify(SIMP)
        td = topo.to_dict()
        sx, sy = td["transform"]["scale"]; tx, ty = td["transform"]["translate"]
        n0 = len(ee["edges"])
        for arc in td["arcs"]:
            ax = ay = 0; pts = []
            for dx, dy in arc:
                ax += dx; ay += dy; pts.append((ax * sx + tx, ay * sy + ty))
            if len(pts) < 2:
                continue
            ls = _LS(pts)
            if ls.interpolate(0.5, normalized=True).distance(prov_ext) < EXT_TOL:
                continue   # province silhouette — comes from the province fill, not a line
            coords = [[round(px - ox, 2), round(py - oy, 2)] for px, py in pts]
            m = [0, 0, 0]; m[k] = 1
            ee["edges"].append({"g": coords, "m": m})
        print(f"  {mk}: {len(ee['edges'])-n0} canonical boundary arcs")

    # ── Agreement labelling: relabel each segment with which maps SHARE that boundary (multi-hot m),
    # so the viewer can mark where the proposals agree vs where they changed. Two maps "agree" on a
    # boundary where their (independently-digitised) canonical lines coincide within AGREE_TOL. The
    # min/maj/2019 agreement is binary at any tolerance 20–100m (boundaries either coincide tightly or
    # diverge by a district-width), so 30m cleanly separates "same" from "changed". Each physical
    # segment is emitted once, by the lowest-index map that carries it (no offset-doubling); the m flag
    # records every map that shares it. Renderer groups 2+-map segments as agreement, 1-map as unique. ──
    from shapely import segmentize as _seg
    from scipy.spatial import cKDTree as _KD
    AGREE_TOL = 30.0; ASTEP = 8.0; AMIN = 30.0
    arcs_by = {kk: [e for e in ee["edges"] if e["m"][kk]] for kk in range(3)}
    def _dense(es, step):
        a = [np.asarray(_seg(_LS([(x + ox, y + oy) for x, y in e["g"]]), step).coords) for e in es]
        return np.vstack(a) if a else np.empty((0, 2))
    atrees = {kk: _KD(_dense(arcs_by[kk], 4.0)) for kk in range(3)}
    relabel = []
    for kk in range(3):
        oth = [j for j in range(3) if j != kk]
        for e in arcs_by[kk]:
            xy = np.asarray(_seg(_LS([(x + ox, y + oy) for x, y in e["g"]]), ASTEP).coords)
            if len(xy) < 2:
                continue
            inj = {j: atrees[j].query(xy)[0] <= AGREE_TOL for j in oth}
            keys = [tuple(sorted({kk} | {j for j in oth if inj[j][i]}))
                    if min({kk} | {j for j in oth if inj[j][i]}) == kk else None for i in range(len(xy))]
            i = 0
            while i < len(xy):
                if keys[i] is None: i += 1; continue
                j = i
                while j + 1 < len(xy) and keys[j + 1] == keys[i]: j += 1
                if j > i:
                    s = _LS(xy[i:j + 1]).simplify(SIMP)
                    if s.length >= AMIN and len(s.coords) >= 2:
                        mm = [0, 0, 0]
                        for mk2 in keys[i]: mm[mk2] = 1
                        relabel.append({"g": [[round(x - ox, 2), round(y - oy, 2)] for x, y in s.coords], "m": mm})
                i = j + 1
    ee["edges"] = relabel
    print(f"  agreement segments: {len(relabel)}")

    (OUT / "ed_edges.json").write_text(json.dumps(ee, separators=(",", ":")), encoding="utf-8")
    ee_mb = (OUT / "ed_edges.json").stat().st_size / 1e6
    print(f"  ed_edges.json: {len(ee['edges'])} edges, {ee_mb:.2f}MB")

    # Faint per-VA hairline outline (every polling-division boundary).
    va_lines = all_arc_lines(va_topo_dict, ox, oy)
    (OUT / "va_lines.json").write_text(json.dumps(va_lines, separators=(",", ":")), encoding="utf-8")
    print(f"  va_lines.json: {len(va_lines)} VA arcs, {(OUT/'va_lines.json').stat().st_size/1e6:.2f}MB")

    # Per-level geometry bytes (lets the viewer show the marginal cost of each zoom level).
    level_bytes = {}
    for k, feats in packed.items():
        z = int(k.split("/")[0])
        level_bytes[z] = level_bytes.get(z, 0) + 4 + sum(4 + len(coords) * 8 for _vid, coords in feats)

    # Build version = hash over every emitted data file (so any change is detectable).
    data_files = sorted(f for f in OUT.iterdir() if f.is_file() and f.name != "manifest.json")
    build_version = hashlib.sha1(
        "".join(f"{f.name}:{hashlib.sha1(f.read_bytes()).hexdigest()}" for f in data_files).encode()
    ).hexdigest()[:12]
    manifest = {
        "version": build_version,
        "levelBytes": level_bytes,
        "originX": ox, "originY": oy,
        "bbox": [round(minx - ox, 2), round(miny - oy, 2), round(maxx - ox, 2), round(maxy - oy, 2)],
        "side": round(side, 2), "minZoom": MINZ, "maxZoom": MAXZ,
        "maps": MAPS, "bundles": bundle_info, "tileCounts": tile_counts,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    print(f"va_tiles.json={va_mb:.1f}MB  in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    # `--ed-index` rebuilds ONLY the per-map ED search index (fast, no retile).
    if "--ed-index" in sys.argv:
        build_ed_index()
    else:
        main()
        build_ed_index()   # keep the search index in step with a full retile
