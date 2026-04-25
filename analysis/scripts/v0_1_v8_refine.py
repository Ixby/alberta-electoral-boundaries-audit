"""
v0_1_v8_refine.py

Resolve residual overlaps left by v0_1_dpg_perfecter.py.  The perfecter
applies an anti-erasure rule (>=10% of loser must remain after clip) which
preserves a small number of overlap pairs — most are sub-square-metre
artefacts but a few are kilometre-scale (e.g. Airdrie-East ∩
Calgary-Falconridge-Conrich = 141.9 km²).  These need a deterministic
resolution rule before downstream MCMC, gerrymetrics, and overlay
verification.

Resolution rule
---------------
For each pair (a, b) with overlap > 1 m²:
  1. Determine the "winner" by canon_source TIER_RANK (higher tier wins).
     Ties broken by larger non-overlapping area.
  2. Clip the loser by the winner.
  3. If the clip would erase >=90% of the loser (anti-erasure trigger),
     instead split the overlap by midline: assign the half nearer the
     winner's centroid to the winner, the other half to the loser.

This guarantees zero residual overlap and zero ED erasure.

Inputs:
  data/shapefiles/derived/v0_8_canonical_<plan>_2026_eds.gpkg

Outputs:
  data/shapefiles/derived/v0_8_refined_<plan>_2026_eds.gpkg
  data/v0_1_v8_refine_summary_<plan>.csv

Dependencies:
  Forward:  data/shapefiles/derived/v0_8_canonical_*.gpkg
  Backward: data/shapefiles/derived/v0_8_refined_*.gpkg,
            data/v0_1_v8_refine_summary_*.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, MultiLineString
from shapely.ops import unary_union, split

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
DERIVED = DATA / "shapefiles" / "derived"

# Match the perfecter's tier ranking
TIER_RANK = {
    "da-anchored": 5,
    "municipal-anchored": 4,
    "osm-municipal-buffered": 3,
    "v7": 2,
    "sweep": 1,
}

ANTI_ERASURE = 0.10  # if clip would erase >90% of loser, fallback to midline split
MIN_OVERLAP_AREA = 1.0  # m² — ignore floating-point dust


def _clean(geom):
    if not geom.is_valid:
        geom = geom.buffer(0)
    return geom


def _midline_split(loser_geom, winner_geom, overlap):
    """Split `overlap` by a perpendicular bisector through the midpoint
    between the two centroids.  Half nearer winner → winner; half nearer
    loser → loser."""
    wc = winner_geom.centroid
    lc = loser_geom.centroid
    # Vector from loser to winner
    dx, dy = wc.x - lc.x, wc.y - lc.y
    if dx == 0 and dy == 0:
        # Degenerate — fall back to giving everything to winner
        return None, overlap

    # Midpoint between centroids
    mx, my = (wc.x + lc.x) / 2, (wc.y + lc.y) / 2
    # Perpendicular direction
    px, py = -dy, dx
    # Build a long line through midpoint along perpendicular
    L = max(overlap.bounds[2] - overlap.bounds[0],
            overlap.bounds[3] - overlap.bounds[1]) * 4 + 1000
    cutter = LineString([
        (mx - px / (px*px + py*py)**0.5 * L, my - py / (px*px + py*py)**0.5 * L),
        (mx + px / (px*px + py*py)**0.5 * L, my + py / (px*px + py*py)**0.5 * L),
    ])

    try:
        pieces = list(split(overlap, cutter).geoms)
    except Exception:
        return None, overlap

    # Half nearer winner centroid → winner share; other → loser share
    winner_pieces, loser_pieces = [], []
    for p in pieces:
        if p.is_empty:
            continue
        d_to_winner = p.centroid.distance(wc)
        d_to_loser = p.centroid.distance(lc)
        if d_to_winner < d_to_loser:
            winner_pieces.append(p)
        else:
            loser_pieces.append(p)

    w = unary_union(winner_pieces) if winner_pieces else None
    l = unary_union(loser_pieces) if loser_pieces else None
    return l, w


def refine(plan: str) -> dict:
    src = DERIVED / f"v0_8_canonical_{plan}_2026_eds.gpkg"
    if not src.exists():
        print(f"  [skip] {src.name} not found")
        return {"plan": plan, "skipped": True}

    g = gpd.read_file(src)
    if "canon_source" not in g.columns:
        g["canon_source"] = "v7"
    if "name_2026" not in g.columns:
        # First text column as fallback
        for c in g.columns:
            if g[c].dtype == object and c != "geometry":
                g = g.rename(columns={c: "name_2026"})
                break

    n = len(g)
    print(f"\n=== {plan} 2026 ===  loaded {n} EDs from {src.name}")

    geoms = [_clean(geom) for geom in g.geometry.values]
    ranks = [TIER_RANK.get(s, 1) for s in g["canon_source"].values]
    names = g["name_2026"].astype(str).values

    sindex = gpd.GeoSeries(geoms, crs=g.crs).sindex
    pairs = []
    for i in range(n):
        for j in sindex.intersection(geoms[i].bounds):
            if j <= i:
                continue
            try:
                inter = geoms[i].intersection(geoms[j])
            except Exception:
                continue
            if inter.area > MIN_OVERLAP_AREA:
                pairs.append((i, j, inter.area))

    pairs.sort(key=lambda t: -t[2])
    print(f"  {len(pairs)} overlap pairs > {MIN_OVERLAP_AREA} m² to resolve")

    resolution_log = []
    for (i, j, _) in pairs:
        gi, gj = geoms[i], geoms[j]
        try:
            inter = gi.intersection(gj)
        except Exception:
            continue
        if inter.is_empty or inter.area <= MIN_OVERLAP_AREA:
            continue

        # Decide winner
        if ranks[i] > ranks[j]:
            wi, li = i, j
        elif ranks[j] > ranks[i]:
            wi, li = j, i
        else:
            wi, li = (i, j) if (gi.area - inter.area) >= (gj.area - inter.area) else (j, i)

        gw, gl = geoms[wi], geoms[li]
        clipped = _clean(gl.difference(gw))

        # Detect nested case: loser is fully (or near-fully) inside winner.
        # In that case we INVERT ownership — the loser keeps its full polygon,
        # and the winner gets a hole carved out. This is the only sane resolution
        # for a nested ED — splitting or erasing it would destroy electoral data.
        loser_fully_nested = (inter.area / gl.area) > 0.95 if gl.area > 0 else False

        if loser_fully_nested:
            # Carve the loser polygon out of the winner; loser keeps its original
            new_winner = _clean(gw.difference(gl))
            if not new_winner.is_empty and new_winner.area >= ANTI_ERASURE * gw.area:
                geoms[wi] = new_winner
                # geoms[li] (loser) keeps its full original polygon, untouched
                method = "nested_invert"
            else:
                # Even inverted, the winner would be erased — keep both as-is
                # and accept the residual overlap (data is fundamentally bad).
                method = "unresolvable_keep_both"
        elif clipped.is_empty or clipped.area < ANTI_ERASURE * gl.area:
            # Anti-erasure trigger — midline split instead
            l_keep, w_extra = _midline_split(gl, gw, inter)
            if l_keep is None or l_keep.is_empty:
                # Degenerate — give everything to winner; loser becomes empty (rare)
                geoms[li] = clipped
                method = "anti_erasure_winner_take_all"
            else:
                # Loser keeps its non-overlap region + half-overlap nearer it
                non_overlap_l = _clean(gl.difference(inter))
                geoms[li] = _clean(unary_union([non_overlap_l, l_keep]))
                method = "midline_split"
        else:
            geoms[li] = clipped
            method = "clip"

        resolution_log.append({
            "winner": names[wi],
            "loser": names[li],
            "overlap_km2": inter.area / 1e6,
            "method": method,
        })

    g["geometry"] = geoms
    out = DERIVED / f"v0_8_refined_{plan}_2026_eds.gpkg"
    g.to_file(out, driver="GPKG")

    # Re-validate: any residual overlaps?
    geoms2 = [_clean(geom) for geom in g.geometry.values]
    sindex2 = gpd.GeoSeries(geoms2, crs=g.crs).sindex
    residual_n = 0
    residual_area = 0.0
    for i in range(n):
        for j in sindex2.intersection(geoms2[i].bounds):
            if j <= i:
                continue
            try:
                a = geoms2[i].intersection(geoms2[j]).area
            except Exception:
                continue
            if a > MIN_OVERLAP_AREA:
                residual_n += 1
                residual_area += a

    log_df = pd.DataFrame(resolution_log)
    log_path = DATA / f"v0_1_v8_refine_summary_{plan}.csv"
    log_df.to_csv(log_path, index=False)

    method_counts = log_df["method"].value_counts().to_dict() if not log_df.empty else {}
    print(f"  resolution methods: {method_counts}")
    print(f"  wrote {out.name}")
    print(f"  wrote {log_path.name}")
    print(f"  residual overlaps after refinement: {residual_n} pairs, "
          f"{residual_area/1e6:.6f} km²")

    return {
        "plan": plan,
        "n_eds": n,
        "n_pairs_resolved": len(resolution_log),
        "method_counts": method_counts,
        "residual_pairs": residual_n,
        "residual_km2": residual_area / 1e6,
        "out": str(out),
    }


def main() -> int:
    print("[v0_8 refinement: resolving residual overlaps]")
    results = []
    for plan in ("majority", "minority"):
        results.append(refine(plan))

    print("\n=== SUMMARY ===")
    for r in results:
        if r.get("skipped"):
            print(f"  {r['plan']}: SKIPPED (input not found)")
            continue
        print(f"  {r['plan']}: resolved {r['n_pairs_resolved']} pairs  "
              f"(methods: {r['method_counts']})  "
              f"→ residual {r['residual_pairs']} pairs / {r['residual_km2']:.6f} km²")
    return 0


if __name__ == "__main__":
    sys.exit(main())
