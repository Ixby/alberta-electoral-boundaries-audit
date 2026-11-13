# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a10_publish_districts.py
------------------------

The published copy of an Amendment 10 districts file: the same 91 districts with no gaps, no overlaps and no
shards.

a10_snap_assign.py (frozen by Amendment 10) draws each district from its voting areas (VAs), splitting cut
VAs along the snapped pieces. The VA layer itself has small overlaps, and clipping leaves slivers, so the
drawn file carries a few hundred square metres of gaps and overlaps and a few hundred detached shards over
the province. This step removes them for publication and display only. It never writes va_assignment.csv,
so no test, score or VA assignment depends on it.

  1. Find the problems. shapely.coverage_invalid_edges marks every district edge that does not match its
     neighbour's exactly (a gap, an overlap or unmatched vertices). Every TILE_M grid tile within WINDOW_M
     of a marked edge is mended.
  2. Mend each tile locally. Inside the tile, every district edge and the VA layer's outline are noded and
     polygonized into faces that partition it, and each face goes to exactly one district:
       - a face inside one district stays with it;
       - a face inside several (an overlap) goes to the one holding the VA under its representative point
         (va_assignment.csv), else to the larger district;
       - a face inside the VA layer but no district (a gap) goes to the district it shares the longest
         edge with.
  3. Shards. A detached part of a district smaller than SHARD_KM2 and SHARD_SHARE of the district, touching
     another district, goes to the district it shares the longest edge with. A part touching no other
     district (an island) stays. Parts at least that large (exclaves a page draws) stay.
  4. Check: the districts' union equals the VA layer's union and the sum of their
     areas equals the union (both within TOL_M2), and no district has a shard left; edges still marked invalid
     are reported (exact lines can keep unmatched vertices at tile seams). A failed check exits 1.

Memory: tiles are clipped with clip_by_rect, so nothing is noded province-wide, and each district takes one
difference against all the tiles at the end; the run stops if free memory falls below MIN_FREE_GB.

Usage: python -W ignore analysis/scripts/a10_publish_districts.py SNAP_DIR [OUT_GPKG]
  OUT_GPKG defaults to SNAP_DIR/districts_published.gpkg; a report goes beside it as .json.
"""
import ctypes
import json
import sys
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import box
from shapely.ops import unary_union
from shapely.strtree import STRtree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a10_assemble as A  # noqa: E402

WINDOW_M = 50.0      # step 1: buffer around each invalid edge stretch
SHARD_KM2 = 0.5      # step 3: a detached part smaller than this ...
SHARD_SHARE = 0.01   # ... and than this share of its district is a shard
TILE_M = 1000.0      # step 1: windows are grouped into tiles of this size, mended once each
GAP_M = 1.0          # step 1: gaps narrower than this between districts are marked too
SNAP_JOIN_M = 0.05   # step 3: a moved piece is snapped to its new district within this distance
TOL_M2 = 1.0         # step 4: gaps and overlaps left over the whole province, m2
MIN_FREE_GB = 1.5    # stop if free physical memory falls below this


class MEMSTAT(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong), ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


def free_gb():
    m = MEMSTAT()
    m.dwLength = ctypes.sizeof(MEMSTAT)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2**30


def guard():
    if free_gb() < MIN_FREE_GB:
        sys.exit(f"stopped: free memory {free_gb():.2f} GB below {MIN_FREE_GB} GB")


def polygonal(g):
    if g.is_empty:
        return shapely.Polygon()
    if g.geom_type in ("Polygon", "MultiPolygon"):
        return g
    ps = [p for p in shapely.get_parts(g) if p.geom_type == "Polygon" and not p.is_empty]
    return unary_union(ps) if ps else shapely.Polygon()


def clip(g, x0, y0, x1, y1):
    try:
        return shapely.clip_by_rect(g, x0, y0, x1, y1)
    except shapely.errors.GEOSException:
        return shapely.make_valid(g).intersection(box(x0, y0, x1, y1))


def shared(q, g):
    """Length of q's edge that lies along g (g clipped to q's box first, so g may be large)."""
    x0, y0, x1, y1 = q.bounds
    gl = clip(g, x0 - 1, y0 - 1, x1 + 1, y1 + 1)
    if gl.is_empty:
        return 0.0
    return float(q.boundary.intersection(gl.buffer(0.01)).length)


def main():
    t0 = time.time()
    snap = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else snap / "districts_published.gpkg"
    d = gpd.read_file(snap / "districts.gpkg").to_crs(3400)
    asg = pd.read_csv(snap / "va_assignment.csv")
    va, _ = A.C.me.build_va_graph(verbose=False)
    va = va[["geometry"]].to_crs(3400)
    assert len(va) == len(asg)
    va_tree = STRtree(list(va.geometry))
    va_ed = asg.ed.to_numpy()
    eds = [int(e) for e in d.ed]
    geom = {int(e): polygonal(shapely.make_valid(g)) for e, g in zip(d.ed, d.geometry)}
    before = {e: g.area for e, g in geom.items()}
    U = unary_union(list(va.geometry))
    print(f"[{time.time() - t0:.0f}s] loaded; free {free_gb():.1f} GB", flush=True)
    guard()

    # 1. problem tiles
    bad = shapely.coverage_invalid_edges([geom[e] for e in eds], gap_width=GAP_M)
    bad = [x for x in bad if x is not None and not x.is_empty]
    tiles = set()
    for x in bad:
        for cx, cy in shapely.get_coordinates(shapely.segmentize(x, TILE_M / 4)):
            for dx in (-WINDOW_M, WINDOW_M):
                for dy in (-WINDOW_M, WINDOW_M):
                    tiles.add((int((cx + dx) // TILE_M), int((cy + dy) // TILE_M)))
    tiles = sorted(tiles)
    print(f"[{time.time() - t0:.0f}s] {len(bad)} districts with invalid edges, {len(tiles)} tiles", flush=True)

    # 2. mend each tile; the mended faces replace the tiles in one difference per district at the end
    gtree = STRtree([geom[e] for e in eds])
    mended = {}
    n_over = n_gap = 0
    a_over = a_gap = 0.0
    for ti, (i, j) in enumerate(tiles):
        if ti % 100 == 0:
            guard()
        x0, y0, x1, y1 = i * TILE_M, j * TILE_M, (i + 1) * TILE_M, (j + 1) * TILE_M
        wbox = box(x0, y0, x1, y1)
        local = {eds[k]: polygonal(clip(geom[eds[k]], x0, y0, x1, y1)) for k in gtree.query(wbox)}
        local = {e: g for e, g in local.items() if not g.is_empty}
        if not local:
            continue
        Ub = clip(U, x0, y0, x1, y1)
        lines = unary_union([g.boundary for g in local.values()] + [Ub.boundary, wbox.boundary])
        faces = [f for f in shapely.get_parts(shapely.polygonize(shapely.get_parts(lines))) if f.area > 0]
        le = list(local)
        ltree = STRtree([local[e] for e in le])
        gaps = []
        for f in faces:
            p = f.representative_point()
            hit = [le[k] for k in ltree.query(p, predicate="within")]
            if len(hit) == 1:
                mended.setdefault(hit[0], []).append(f)
            elif len(hit) > 1:
                n_over += 1
                a_over += f.area
                v = list(va_tree.query(p, predicate="within"))
                ve = int(va_ed[v[0]]) if v else None
                mended.setdefault(ve if ve in hit else max(hit, key=lambda e: geom[e].area), []).append(f)
            elif Ub.contains(p):
                gaps.append(f)
        for q in gaps:
            lens = {e: shared(q, local[e]) for e in local}
            best = max(lens, key=lens.get)
            if lens[best] > 0:
                mended.setdefault(best, []).append(q)
                n_gap += 1
                a_gap += q.area
        if ti % 500 == 0:
            print(f"[{time.time() - t0:.0f}s] tile {ti}/{len(tiles)}", flush=True)
    T = unary_union([box(i * TILE_M, j * TILE_M, (i + 1) * TILE_M, (j + 1) * TILE_M) for i, j in tiles])
    for e in eds:
        geom[e] = polygonal(unary_union([geom[e].difference(T), *mended.get(e, [])]))
    print(f"[{time.time() - t0:.0f}s] tiles mended: {n_over} overlaps ({a_over:.1f} m2), {n_gap} gaps ({a_gap:.1f} m2)", flush=True)
    guard()

    # 3. shards and leftover gaps, repeated until nothing moves (a moved piece is snapped to its new district
    #    within SNAP_JOIN_M first, so it joins it instead of staying a separate part)
    n_shard, a_shard = 0, 0.0
    for rnd in range(4):
        tree = STRtree([geom[e] for e in eds])
        moves = []
        for e in eds:
            ps = list(shapely.get_parts(geom[e]))
            if len(ps) < 2:
                continue
            big = max(p.area for p in ps)
            for p in ps:
                if p.area == big or p.area >= SHARD_KM2 * 1e6 or p.area >= SHARD_SHARE * geom[e].area:
                    continue
                lens = {eds[j]: shared(p, geom[eds[j]]) for j in tree.query(p.buffer(0.01)) if eds[j] != e}
                lens = {c: x for c, x in lens.items() if x > 0}
                if lens:
                    moves.append((e, max(lens, key=lens.get), p))
        gap = polygonal(U.difference(unary_union(list(geom.values()))))
        for q in shapely.get_parts(gap):
            if q.area <= 0:
                continue
            lens = {eds[j]: shared(q, geom[eds[j]]) for j in tree.query(q.buffer(0.01))}
            lens = {c: x for c, x in lens.items() if x > 0}
            if lens:
                moves.append((None, max(lens, key=lens.get), q))
                n_gap += 1
                a_gap += q.area
        if not moves:
            break
        for e, c, p in moves:
            if e is not None:
                geom[e] = polygonal(geom[e].difference(p))
                n_shard += 1
                a_shard += p.area
            geom[c] = polygonal(unary_union([geom[c], shapely.snap(p, geom[c], SNAP_JOIN_M)]))
        print(f"[{time.time() - t0:.0f}s] round {rnd + 1}: {len(moves)} pieces moved", flush=True)
    print(f"[{time.time() - t0:.0f}s] {n_shard} shards moved ({a_shard:.1f} m2)", flush=True)
    guard()

    # 4. check
    left_bad = [x for x in shapely.coverage_invalid_edges([geom[e] for e in eds], gap_width=GAP_M)
                if x is not None and not x.is_empty]
    D = unary_union(list(geom.values()))
    left_gap = U.difference(D).area
    left_over = sum(g.area for g in geom.values()) - D.area
    shards_left = []
    for e in eds:
        ps = list(shapely.get_parts(geom[e]))
        big = max(p.area for p in ps)
        for p in ps:
            if p.area != big and p.area < SHARD_KM2 * 1e6 and p.area < SHARD_SHARE * geom[e].area:
                if any(shared(p, geom[eds[j]]) > 0 for j in tree.query(p.buffer(0.01)) if eds[j] != e):
                    shards_left.append(e)
    ok = left_gap <= TOL_M2 and left_over <= TOL_M2 and not shards_left  # left_bad: reported (tile seams can leave unmatched vertices on exact lines)
    rows = [{"ed": e, "area_change_m2": round(geom[e].area - before[e], 2)} for e in eds if abs(geom[e].area - before[e]) > 0.01]
    rep = {"snap": str(snap), "tiles": len(tiles), "overlaps_resolved": n_over, "overlap_m2": round(a_over, 2),
           "gaps_filled": n_gap, "gap_m2": round(a_gap, 2), "shards_moved": n_shard, "shard_m2": round(a_shard, 2),
           "left_invalid_edges": len(left_bad), "left_gap_m2": round(left_gap, 3), "left_overlap_m2": round(left_over, 3),
           "shards_left": shards_left, "multipart_districts": [e for e in eds if len(shapely.get_parts(geom[e])) > 1],
           "tol_m2": TOL_M2, "pass": ok, "seconds": round(time.time() - t0),
           "max_district_change_m2": max((abs(r["area_change_m2"]) for r in rows), default=0.0), "districts_changed": rows}
    out_d = d.copy()
    out_d["geometry"] = [geom[int(e)] for e in d.ed]
    out_d.to_file(out, driver="GPKG")
    with open(out.with_suffix(".json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rep, fh, indent=1)
    print({k: v for k, v in rep.items() if k != "districts_changed"}, flush=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
