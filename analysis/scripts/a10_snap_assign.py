# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a10_snap_assign.py
------------------

Amendment 10, phase 2: take the assembly (a10_assemble.assemble) and the surviving page polygons,
snap their edges together, measure drift, assign every voting area (VA), and run the sanity check.

  1. Snap       Each surviving reconstruction outline is densified (SEGMENT_MAX) and every vertex within
                SNAP_TOL of a target line moves onto the nearest point of the first tier that has one:
                (a) known-district boundaries, (b) VA boundaries, (c) other reconstructions' outlines
                plus the neighbour-page polylines of piece D when present. Per piece: vertices moved,
                median and max displacement.
  2. Drift      For every adjacent pair of pieces (known and snapped; known-known pairs are official
                and skipped): overlap area + gap area (gap = the part of the two pieces' DRIFT_GAP_BUF
                buffers that lies in neither piece). Total drift = sum / area of the union of pieces.
                Reported before and after snapping; pairs listed worst first.
  3. Assign     A VA goes to the piece containing its representative point (the audit's convention); when
                that point lies in no piece (a gap) it goes to the piece holding the largest share of its
                area, if that is at least MIN_AREA_SHARE, else it is left to the hole fill. VAs the assembly gave to a hole-filled district stay with it.
                Any other piece holding more than CUT_SHARE of a VA marks it CUT; in districts.gpkg a cut
                VA is drawn split along the piece lines, in the VA population report it is apportioned
                by area.
  4. Merged     A component the assembly left unassigned because several unplaced districts claim it
     holes      is split by the better page fit (rejected polygon with the most matched points within 60 m, n_layer_pts * in60, that holds at least one of the VAs) taking the
                VAs it holds >= MIN_AREA_SHARE of, the other claimant (when exactly two) taking the
                rest. Flagged low_confidence (source "split"). With no polygon: left unassigned.
  5. Sanity     91 districts; every VA assigned; each district connected on the VA graph; no district
                overlaps a known district by more than KNOWN_OVERLAP_SANITY (0.1%); area within AREA_TOL_SANITY
                of App. 7; neighbour numbers printed on the page equal the districts adjacent in the
                assembled map (needs piece D's edNN_neighbours.json, else "not run"); coverage complete.

Everything is EPSG:3400. Deterministic.

Usage:
  python analysis/scripts/a10_snap_assign.py --pages OUT_DIR --known tuning|fixed --out RESULT_DIR [--neighbours DIR]
Writes RESULT_DIR/{va_assignment.csv, districts.gpkg, snapped_pieces.gpkg, report.json}.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union
from shapely.strtree import STRtree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a10_assemble as A  # noqa: E402

norm = A.norm

SNAP_TOL = 40.0               # step 1: vertices within this many metres of a target line move onto it
SEGMENT_MAX = 250.0           # step 1: outline segments are densified to at most this length (m) before snapping
CHUNK = 16                    # step 1: target lines are cut into runs of this many segments (keeps nearest-queries fast)
CUT_SHARE = 0.01              # step 3: another piece holding more than this share of a VA marks the VA cut
MIN_AREA_SHARE = A.MIN_AREA_SHARE  # step 3/4: a VA needs at least this share of its area in one piece
DRIFT_GAP_BUF = SNAP_TOL      # step 2: a gap is measured out to this buffer on each piece (slivers up to 2x wide)
DRIFT_TARGET = 0.0005         # step 2: total drift target, 0.05% of the territory covered
N_DISTRICTS = 91              # sanity: districts in the final map
KNOWN_OVERLAP_SANITY = 0.001   # sanity: max overlap with another known district, share of own area (0.1%; the 40 m snap leaves residue of that order)
NB_MIN_EDGE_M = 200.0          # sanity: a shared edge shorter than this is a corner touch, not an adjacency
NB_MIN_SHARE = 0.5             # sanity: more than this share of a district's real neighbours must be printed on its page
CITY_LABELS = {"calgary", "edmonton", "st. albert", "red deer", "lethbridge", "medicine hat",
               "grande prairie", "airdrie", "sherwood park"}  # a bare city label on a page stands for all of the city's districts
FRAME_MIN_W, FRAME_MIN_H = 400.0, 500.0  # sanity: the map frame is the largest dark-stroked rectangle wider/taller than this (pt)
FRAME_DARK = 0.4              # sanity: a stroke counts as dark when every colour channel is below this
OUT_OF_FRAME_MAX = 0.005      # sanity: a district drawn back on its page may have at most this share of its area outside the frame
INSET_NAME = "inset_districts.gpkg"  # sanity: the pages' locator-inset shapes (a10_inset.py fit PAGES_DIR), read from the pages directory; absent = item not run, which fails the sanity check
CONNECT_INSIDE = 0.90            # sanity: a VA-graph component of a district passes if one of its VAs has this share inside the piece
AREA_TOL_FILLED = 0.25        # sanity: filled / split districts (unions of whole VAs) carry cut-VA granularity: figure reported, never gates; this share only marks the row 'info_out_of_25pct'
AREA_TOL_SANITY = 0.05        # sanity: |area - App. 7 area_km2| <= this share of the stated area


# ---- helpers -----------------------------------------------------------------------------------

def _poly_parts(g):
    if g is None or g.is_empty:
        return []
    return [g] if g.geom_type == "Polygon" else [p for p in g.geoms if p.geom_type == "Polygon"]


def _chunks(lines, owners):
    """Cut linestrings into runs of CHUNK segments. Returns (geoms array, owner array)."""
    out, own = [], []
    for ln, o in zip(lines, owners):
        c = shapely.get_coordinates(ln)
        for i in range(0, max(len(c) - 1, 0), CHUNK):
            out.append(LineString(c[i:i + CHUNK + 1]))
            own.append(o)
    return np.array(out, dtype=object), np.array(own)


def _boundary_lines(geoms, owners):
    parts = shapely.get_parts(shapely.boundary(np.asarray(geoms, dtype=object)))
    # owner per part: repeat by number of parts of each boundary
    counts = shapely.get_num_geometries(shapely.boundary(np.asarray(geoms, dtype=object)))
    return list(parts), list(np.repeat(np.asarray(owners, dtype=object), counts))


class Tier:
    def __init__(self, name, geoms, owners):
        self.name, self.geoms, self.owners = name, geoms, owners
        self.tree = STRtree(geoms) if len(geoms) else None

    def without(self, owner):
        keep = self.owners != owner
        return Tier(self.name, self.geoms[keep], self.owners[keep])


def _snap_xy(xy, tiers):
    """Move every row of xy onto the nearest point of the first tier within SNAP_TOL.
    Returns (new xy, moved distance per row, tier index per row or -1)."""
    n = len(xy)
    pts = shapely.points(xy)
    new, tier_of, moved = xy.copy(), np.full(n, -1), np.zeros(n)
    for k, t in enumerate(tiers):
        todo = np.flatnonzero(tier_of < 0)
        if not len(todo) or t.tree is None:
            continue
        ii, _ = t.tree.query_nearest(pts[todo], max_distance=SNAP_TOL, return_distance=True, all_matches=False)
        if not ii.shape[1]:
            continue
        src, lines = todo[ii[0]], t.geoms[ii[1]]
        loc = shapely.line_locate_point(lines, pts[src])
        q = shapely.get_coordinates(shapely.line_interpolate_point(lines, loc))
        moved[src] = np.hypot(*(q - xy[src]).T)
        new[src], tier_of[src] = q, k
    return new, moved, tier_of


def snap_piece(poly, tiers):
    """Snap one polygon; returns (polygon, moved distances of snapped vertices, tier counts, n vertices)."""
    shapely.prepare(poly)
    poly = shapely.segmentize(poly, SEGMENT_MAX)
    parts, all_moved, tier_counts, nv = [], [], np.zeros(len(tiers), int), 0

    def ring(r):
        nonlocal nv
        xy = shapely.get_coordinates(r)[:-1]
        new, moved, tier_of = _snap_xy(xy, tiers)
        nv += len(xy)
        sel = tier_of >= 0
        all_moved.append(moved[sel])
        for k in range(len(tiers)):
            tier_counts[k] += int((tier_of == k).sum())
        return np.vstack([new, new[:1]])

    for p in _poly_parts(poly):
        shell = ring(p.exterior)
        holes = [ring(h) for h in p.interiors]
        parts.append(Polygon(shell, holes))
    g = unary_union([x if x.is_valid else x.buffer(0) for x in parts])
    return A._valid(g), np.concatenate(all_moved) if all_moved else np.array([]), tier_counts, nv


# ---- drift -------------------------------------------------------------------------------------

def _clip(g, b):
    try:
        return g.intersection(b)
    except shapely.errors.GEOSException:
        return g.buffer(0).intersection(b)


def drift(pieces, known_names):
    """Overlap + gap between adjacent pieces. Returns (total fraction, union area, pair rows worst first)."""
    names = list(pieces)
    geoms = np.array([pieces[n] for n in names], dtype=object)
    tree = STRtree(geoms)
    qi, ti = tree.query(geoms, predicate="dwithin", distance=2 * DRIFT_GAP_BUF)
    rows = []
    for a, b in sorted(set((min(x, y), max(x, y)) for x, y in zip(qi, ti) if x != y)):
        if names[a] in known_names and names[b] in known_names:
            continue
        ga, gb = geoms[a], geoms[b]
        t = DRIFT_GAP_BUF
        ba, bb = ga.bounds, gb.bounds
        e = box(max(ba[0], bb[0]) - t, max(ba[1], bb[1]) - t, min(ba[2], bb[2]) + t, min(ba[3], bb[3]) + t)
        if e.is_empty or e.area == 0:
            continue
        clip = box(*e.buffer(3 * t, join_style=2).bounds)
        ca, cb = _clip(ga, clip), _clip(gb, clip)
        ov = _clip(ca, e).intersection(_clip(cb, e)).area if not ca.is_empty and not cb.is_empty else 0.0
        reg = ca.buffer(t, 4).intersection(cb.buffer(t, 4))
        gap = _clip(reg.difference(ca).difference(cb), e).area if not reg.is_empty else 0.0
        if ov > 0 or gap > 0:
            rows.append({"a": names[a], "b": names[b], "overlap_m2": ov, "gap_m2": gap})
    union = unary_union(list(geoms)).area
    rows.sort(key=lambda r: -(r["overlap_m2"] + r["gap_m2"]))
    tot = sum(r["overlap_m2"] + r["gap_m2"] for r in rows)
    return tot / union if union else float("nan"), union, rows


# ---- assignment --------------------------------------------------------------------------------

def _components(n, edges, mask):
    keep = mask[edges[:, 0]] & mask[edges[:, 1]]
    e = edges[keep]
    m = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n))
    return connected_components(m, directed=False)[1]


def split_merged_holes(res, va, edges, polys, pages, name_of):
    """Step 4. Returns ({va row: name}, report list)."""
    unassigned = res.va_district.isna().to_numpy()
    def claimant_eds(d):  # the valid claimants; when every claim was dropped on area, all claimants
        v = sorted(int(e) for e in d.get("claimants", {}))
        return v if v else sorted({int(k["ed"]) for k in d.get("claims", [])})

    detail = [d for d in res.summary.get("unassigned_components_detail", []) if len(claimant_eds(d)) >= 2]
    pair_n = {}
    for d in detail:
        pair_n[tuple(claimant_eds(d))] = pair_n.get(tuple(claimant_eds(d)), 0) + 1
    if not detail or not unassigned.any():
        return {}, []
    lab = _components(len(va), edges, unassigned)
    lab = np.where(unassigned, lab, -1)
    sizes = pd.Series(lab[unassigned]).value_counts()
    geoms = np.asarray(va.geometry.values, dtype=object)
    va_area = shapely.area(geoms)
    out, report = {}, []
    for d in detail:
        cands = [c for c, n in sizes.items() if n == d["n_vas"]]
        comp = [c for c in cands if abs(unary_union(list(geoms[lab == c])).area / 1e6 - d["area_km2"]) < 1e-3]
        if not comp:
            report.append({"claimants": sorted(d["claimants"]), "n_vas": d["n_vas"], "result": "component not re-found"})
            continue
        idx = np.flatnonzero(lab == comp[0])
        eds = claimant_eds(d)
        if pair_n[tuple(eds)] > 1:  # several separate holes, same claimants: left to the assembler's neighbour rule
            report.append({"claimants": eds, "n_vas": len(idx), "result": "left to the assembler (same claimants on several holes)"})
            continue

        def pts60(e):  # matched points within 60 m: the evidence behind a page fit (n_layer_pts * in60)
            dg = (pages.get(e) or {}).get("diagnostics") or {}
            return float(dg.get("n_layer_pts") or 0) * float(dg.get("in60") or 0)

        with_poly = sorted([e for e in eds if e in polys], key=lambda e: (-pts60(e), e))
        if not with_poly or len(eds) != 2:
            report.append({"claimants": eds, "n_vas": len(idx),
                           "result": "left unassigned: " + ("no polygon from either page" if not with_poly
                                                           else f"{len(eds)} claimants (rule handles two)")})
            continue
        # the better fit (lowest med_dist_m) whose polygon actually holds some of the component's VAs
        best, sh, skipped = None, None, []
        for e in with_poly:
            s_ = np.array([_clip(geoms[i], polys[e]).area / va_area[i] for i in idx])
            if (s_ >= MIN_AREA_SHARE).any():
                best, sh = e, s_
                break
            skipped.append(e)
        if best is None:
            report.append({"claimants": eds, "n_vas": len(idx), "result": "left unassigned: no claimant polygon holds a VA"})
            continue
        other = [e for e in eds if e != best][0]
        for i, s_ in zip(idx, sh):
            out[int(i)] = name_of[best] if s_ >= MIN_AREA_SHARE else name_of[other]
        report.append({"claimants": eds, "n_vas": len(idx), "better_fit_ed": best, "matched_pts_within_60m": {e: pts60(e) for e in eds},
                       "to_better": int((sh >= MIN_AREA_SHARE).sum()), "to_other": int((sh < MIN_AREA_SHARE).sum()),
                       "skipped_better_fit_with_no_vas": skipped, "result": "split"})
    return out, report


def assign(va, res, pieces, extra_split, name_of):
    """Step 3. pieces {name: geometry} (known + snapped). Returns per-VA frame:
    district, cut, partners {name: share}, kind in {known, placed, filled, split}."""
    names = list(pieces)
    geoms = np.asarray(va.geometry.values, dtype=object)
    va_area = shapely.area(geoms)
    vi, di, sh = A._area_shares(geoms, va_area, np.array([pieces[n] for n in names], dtype=object))
    shares = [dict() for _ in range(len(va))]
    for v, d, s in zip(vi, di, sh):
        shares[v][names[d]] = float(s)
    # the audit's standing convention: a VA goes to the piece containing its representative point
    ptree = STRtree(np.array([pieces[n] for n in names], dtype=object))
    ri, pi = ptree.query(np.asarray(va.geometry.representative_point().values, dtype=object), predicate="within")
    rep_in = [[] for _ in range(len(va))]
    for r_, p_ in zip(ri, pi):
        rep_in[r_].append(names[p_])
    filled_names = {name_of[e] for e in res.filled}
    known_names = set(res.districts.loc[res.districts.source == "known", "district"])
    dist, kind, partners, allsh = [], [], [], []
    for v in range(len(va)):
        s = shares[v]
        order = sorted(s.items(), key=lambda kv: (-round(kv[1], A.TIE_DECIMALS), kv[0] not in known_names, kv[0]))
        prior = res.va_district.iloc[v]
        if v in extra_split:
            c, k = extra_split[v], "split"
        elif prior is not None and prior in filled_names:
            c, k = prior, "filled"
        elif rep_in[v]:  # representative point inside a piece (overlap of pieces: the larger area share, known first)
            c = sorted(rep_in[v], key=lambda n: (-round(s.get(n, 0.0), A.TIE_DECIMALS), n not in known_names, n))[0]
            k = "known" if c in known_names else "placed"
        elif order and order[0][1] >= MIN_AREA_SHARE:  # a gap: the largest area share
            c = order[0][0]
            k = "known" if c in known_names else "placed"
        else:
            c, k = None, None
        dist.append(c)
        allsh.append(s)
        kind.append(k)
        partners.append({n: x for n, x in order if x > CUT_SHARE and n != c} if c is not None else {})
    return pd.DataFrame({"district": dist, "kind": kind, "partners": partners, "shares": allsh,
                         "cut": [bool(p) for p in partners]}, index=va.index)


def build_geometries(va, table, pieces):
    """District geometry = whole uncut VAs + split parts of cut VAs. Returns (geoms {name: geom},
    weight per VA per district {(row, name): fraction of the VA's area})."""
    geoms = np.asarray(va.geometry.values, dtype=object)
    parts, weight = {}, {}
    for v in np.flatnonzero(table.district.notna().to_numpy()):
        c, pr = table.district.iloc[v], table.partners.iloc[v]
        g = geoms[v]
        if not pr:
            parts.setdefault(c, []).append(g)
            weight[(v, c)] = 1.0
            continue
        allocated = Polygon()
        for n, _ in sorted(pr.items(), key=lambda kv: (-kv[1], kv[0])):
            part = _clip(g, pieces[n]).difference(allocated) if not allocated.is_empty else _clip(g, pieces[n])
            if part.is_empty:
                continue
            allocated = part if allocated.is_empty else unary_union([allocated, part])
            parts.setdefault(n, []).append(part)
            weight[(v, n)] = part.area / g.area
        rest = g.difference(allocated) if not allocated.is_empty else g
        parts.setdefault(c, []).append(rest)
        weight[(v, c)] = rest.area / g.area
    return {n: _polygonal(unary_union(p)) for n, p in parts.items()}, weight


def _polygonal(g):
    """Drop the zero-area lines and points that clipping cut VAs leaves in a union."""
    if g.geom_type in ("Polygon", "MultiPolygon"):
        return g
    polys = [q for q in shapely.get_parts(g) if q.geom_type == "Polygon" and not q.is_empty]
    return unary_union(polys) if polys else Polygon()


# ---- sanity ------------------------------------------------------------------------------------

def sanity(va, table, dgeoms, known, app7, edges, name_of, ed_of, nb_dir, pieces, loose, pooled):
    items = {}
    lab_names = table.district.to_numpy(dtype=object)
    have = sorted(n for n in set(lab_names) if n is not None)

    missing = sorted(ed for ed, n in name_of.items() if n not in have)
    items["districts_91"] = {"pass": len(have) == N_DISTRICTS, "found": len(have), "missing_eds": missing}

    n_un = int(pd.isna(table.district).sum())
    items["every_va_assigned"] = {"pass": n_un == 0, "unassigned_vas": n_un}

    # connectivity on the VA graph
    code = pd.Series(lab_names).astype("category")
    codes = np.where(pd.isna(code.cat.codes) | (code.cat.codes < 0), -1, code.cat.codes).astype(int)
    same = (codes[edges[:, 0]] == codes[edges[:, 1]]) & (codes[edges[:, 0]] >= 0)
    m = coo_matrix((np.ones(int(same.sum())), (edges[same, 0], edges[same, 1])), shape=(len(va), len(va)))
    comp = connected_components(m, directed=False)[1]
    bad, multipart = {}, {}
    for n in have:
        cs = pd.Series(comp[lab_names == n]).value_counts()
        if len(cs) <= 1:
            continue
        has_piece = n in known or any(n in d for d in table.shares)
        comps = []
        for c, cnt in cs.items():
            members = np.flatnonzero((lab_names == n) & (comp == c))
            best = max(table.shares.iloc[v].get(n, 0.0) for v in members)
            # a component passes when one of its VAs has >= CONNECT_INSIDE of its area inside the district's piece;
            # a district with no piece (filled / split) cannot show that, so it must be a single component
            passes = has_piece and best >= CONNECT_INSIDE
            comps.append({"n_vas": int(cnt), "best_inside_share": best, "passes": bool(passes),
                          "vas": [] if passes else [{"objectid": int(va["OBJECTID"].iloc[v]), "va_number": str(va["VA_NUMBER"].iloc[v]),
                                                     "cut": bool(table.cut.iloc[v])} for v in members][:30]})
        if n in pooled:  # a pooled fill claims several hole components by construction
            multipart[ed_of.get(n, n)] = {"va_counts": [c["n_vas"] for c in comps], "why": "pooled hole-fill claim"}
        elif all(c["passes"] for c in comps):
            multipart[ed_of.get(n, n)] = {"va_counts": [c["n_vas"] for c in comps]}
        else:
            bad[ed_of.get(n, n)] = {"components": comps}
    items["each_district_connected"] = {"pass": not bad, "disconnected": bad, "multipart": multipart,
                                       "n_multipart": len(multipart)}

    # overlap with known districts
    ktree = STRtree(list(known.values()))
    kn = list(known)
    off = []
    for n, g in dgeoms.items():
        for j in ktree.query(g, predicate="intersects"):
            if kn[j] == n:
                continue
            f = _clip(g, known[kn[j]]).area / g.area
            if f > KNOWN_OVERLAP_SANITY:
                off.append({"district": n, "ed": ed_of.get(n), "known": kn[j], "share_pct": 100 * f})
    off.sort(key=lambda r: -r["share_pct"])
    items["no_known_overlap_over_0.1pct"] = {"pass": not off, "offenders": off[:15], "n_offenders": len(off)}

    # area vs App. 7
    arows = []
    for n, g in dgeoms.items():
        ed = ed_of[n]
        st = float(app7.loc[ed, "area_km2"])
        # a placed piece is judged on its snapped outline (5%); known districts on their VA union (5%);
        # filled / split districts on their VA union (25%)
        a = (pieces[n].area if n in pieces and n not in known and n not in loose else g.area) / 1e6
        tol = AREA_TOL_FILLED if n in loose else AREA_TOL_SANITY
        arows.append({"ed": ed, "district": n, "area_km2": a, "stated_km2": st, "diff_pct": 100 * (a - st) / st if st else None,
                      "tol_pct": 100 * tol})
    for r in arows:
        r["informational"] = r["district"] in loose
    afail = [r for r in arows if not r["informational"] and (r["diff_pct"] is None or abs(r["diff_pct"]) > r["tol_pct"])]
    ainfo = [r for r in arows if r["informational"] and (r["diff_pct"] is None or abs(r["diff_pct"]) > r["tol_pct"])]
    afail.sort(key=lambda r: -abs(r["diff_pct"] or 0))
    items["area_within_tol_of_stated"] = {"pass": not afail and len(have) == N_DISTRICTS, "n_checked": len(arows),
                                           "n_fail": len(afail), "fails": afail[:20],
                                           "informational_filled_split_over_25pct": ainfo}

    # neighbour numbers
    cl = codes[edges[:, 0]] != codes[edges[:, 1]]
    cl &= (codes[edges[:, 0]] >= 0) & (codes[edges[:, 1]] >= 0)
    adj, pair_vas = {}, {}
    cats = list(code.cat.categories)
    for u, v in edges[cl]:
        a, b = ed_of.get(cats[codes[u]]), ed_of.get(cats[codes[v]])
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
        pair_vas.setdefault(frozenset((a, b)), []).append((int(u), int(v)))
    files = {}
    if nb_dir is not None:
        for f in Path(nb_dir).glob("ed*_neighbours.json"):
            d = json.loads(f.read_text(encoding="utf-8"))
            printed = {int(x) for x in d.get("neighbour_eds", [])}
            for lb in list(d.get("city_labels") or []) + list(d.get("labels") or []):  # a bare city name prints every district of that city
                txt = str(lb.get("text", "") if isinstance(lb, dict) else lb).strip().rstrip("-").strip().lower()
                own = name_of.get(int(d.get("ed", f.stem[2:4])), "").lower()
                if txt in CITY_LABELS and not (own == txt or own.startswith(txt + "-")):  # not on a page inside that city
                    printed |= {e for e, n in name_of.items() if n.lower() == txt or n.lower().startswith(txt + "-")}
            files[int(d.get("ed", f.stem[2:4]))] = printed
    if not files:
        items["page_neighbours_match_adjacency"] = {"pass": None, "status": "not run (no edNN_neighbours.json found)"}
    else:
        mism, page_only_n = [], 0
        for ed, want in sorted(files.items()):
            if name_of.get(ed) not in have:
                continue
            got = adj.get(ed, set())
            page_only_n += len(want - got)  # a page prints everything in its window: informational
            # adjacent districts sharing more than NB_MIN_EDGE_M of edge (corner touches excluded)
            lens = {o: float(dgeoms[name_of[ed]].intersection(dgeoms[name_of[o]]).length)
                    for o in got if o in name_of and name_of[o] in dgeoms}
            real = {o: m for o, m in lens.items() if m > NB_MIN_EDGE_M}
            if not real:
                continue
            printed = [o for o in real if o in want]
            if len(printed) / len(real) <= NB_MIN_SHARE:
                vp = lambda o: sorted({(int(va["OBJECTID"].iloc[u]), int(va["OBJECTID"].iloc[v])) for u, v in pair_vas[frozenset((ed, o))]})[:8]
                mism.append({"ed": ed, "printed_of_adjacent": f"{len(printed)}/{len(real)}",
                             "missing_from_page": [{"other_ed": o, "shared_edge_m": m, "va_pairs_objectid": vp(o)}
                                                   for o, m in sorted(real.items(), key=lambda kv: -kv[1]) if o not in want],
                             "page_only": sorted(want - got)})
        items["page_neighbours_match_adjacency"] = {"pass": not mism, "status": "run (more than half of adjacent districts over 200 m printed)",
                                                    "n_pages": len(files), "n_mismatch": len(mism),
                                                    "page_only_total_informational": page_only_n, "mismatches": mism[:40]}

    # coverage
    va_area = shapely.area(np.asarray(va.geometry.values, dtype=object))
    cov = float(va_area[table.district.notna().to_numpy()].sum() / va_area.sum())
    items["provincial_coverage_complete"] = {"pass": n_un == 0, "va_area_assigned_share": cov}
    return items, adj, arows


def page_frame(n):
    """The page's map frame as a pymupdf-free (x0, y0, x1, y1) in page points."""
    import a9_stepb_reconstruct_v3 as V3
    pg = V3._page(n)
    best, area = None, 0.0
    for d in pg.get_drawings():
        col = d.get("color")
        if col is None or max(col) >= FRAME_DARK:
            continue
        r = d["rect"]
        kinds = {it[0] for it in d["items"]}
        if not (kinds <= {"re", "qu"} or (kinds == {"l"} and len(d["items"]) <= 5)):  # a rectangle, not a long path
            continue
        if r.x0 < pg.rect.x0 - 2 or r.y0 < pg.rect.y0 - 2 or r.x1 > pg.rect.x1 + 2 or r.y1 > pg.rect.y1 + 2:
            continue                                                               # the frame lies on the page
        if r.width > FRAME_MIN_W and r.height > FRAME_MIN_H and r.width * r.height > area:
            best, area = (r.x0, r.y0, r.x1, r.y1), r.width * r.height
    if best is None:
        r = pg.rect
        best = (r.x0, r.y0, r.x1, r.y1)
    return best


def in_frame_item(dgeoms, pages, name_of, used):
    """Each district with an accepted page transform, mapped back to its page (inverse of V1._apply:
    s, theta, t, c from the json diagnostics), must lie inside that page's map frame. The gate covers pages
    whose transform was USED (a placed piece: its snapped outline is mapped back); every other accepted page
    (rejected, filled, split, known) is listed informationally with the final VA-union district."""
    rows = []
    for ed, pg in sorted(pages.items()):
        dg = pg.get("diagnostics") or {}
        n = name_of.get(ed)
        if pg.get("polygon_status") != "accepted" or dg.get("p") is None or dg.get("c") is None or n not in dgeoms:
            continue
        sc, th, tx, ty = dg["p"]
        cx, cy = dg["c"]
        g = used[ed] if ed in used else dgeoms[n]
        cs, sn = np.cos(th), np.sin(th)

        def back(xy):  # ground -> page points
            u, v = (xy[:, 0] - tx) / sc, (xy[:, 1] - ty) / sc
            return np.c_[cs * u + sn * v + cx, cy - (-sn * u + cs * v)]

        polys = []
        for part in _poly_parts(g):
            polys.append(Polygon(back(np.array(part.exterior.coords)), [back(np.array(h.coords)) for h in part.interiors]).buffer(0))
        pg_geom = unary_union(polys)
        x0, y0, x1, y1 = page_frame(ed)
        out = pg_geom.difference(box(x0, y0, x1, y1)).area / pg_geom.area if pg_geom.area else 1.0
        rows.append({"ed": ed, "district": n, "share_outside_frame": float(out), "transform_used": ed in used, "frame_pt": [x0, y0, x1, y1]})
    gated = [r for r in rows if r["transform_used"]]
    bad = [r for r in gated if r["share_outside_frame"] >= OUT_OF_FRAME_MAX]
    info = [r for r in rows if not r["transform_used"] and r["share_outside_frame"] >= OUT_OF_FRAME_MAX]
    return {"pass": not bad and bool(gated), "n_pages": len(gated), "n_fail": len(bad),
            "fails": sorted(bad, key=lambda r: -r["share_outside_frame"]),
            "informational_unused_over_threshold": sorted(info, key=lambda r: -r["share_outside_frame"]),
            "per_page": rows}


def inset_item(inset, out_dir):
    """Compare the assembled districts with the locator-inset shapes on the pages (a10_inset.py check).
    An inset that highlights the wrong district (inset_source_error) is reported, not failed."""
    import subprocess
    if not inset.exists():
        return {"pass": None, "status": f"not run ({inset} absent)"}
    outj = out_dir / "inset_check.json"
    r = subprocess.run([sys.executable, "-W", "ignore", str(Path(__file__).resolve().parent / "a10_inset.py"), "check",
                        "--inset", str(inset), "--districts", str(out_dir / "districts.gpkg"), "--out", str(outj)],
                       capture_output=True, text=True)
    if r.returncode != 0 or not outj.exists():
        return {"pass": False, "status": "error running a10_inset.py", "stderr": r.stderr[-500:]}
    d = json.loads(outj.read_text(encoding="utf-8"))
    rows = d.get("districts", {})
    return {"pass": d.get("n_fail", 1) == 0 and d.get("n_pass", 0) > 0, "status": "run", "n_pass": d.get("n_pass"),
            "n_fail": d.get("n_fail"), "n_source_error": d.get("n_source_error"), "rule": d.get("rule"),
            "failed": d.get("failed"), "source_errors": sorted(int(k) for k, v in rows.items() if v.get("inset_source_error")),
            "per_district": rows}


# ---- main --------------------------------------------------------------------------------------

def _plain(x):
    return A._plain(x)


def run(pages_dir, which, out_dir, nb_dir=None, inset=None):
    inset = Path(pages_dir) / INSET_NAME if inset is None else Path(inset)
    t0 = time.time()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    app7 = A.load_app7()
    name_of = {int(e): norm(str(n)) for e, n in app7["district"].items()}
    ed_of = {n: e for e, n in name_of.items()}
    known = A.known_districts(which, app7)
    va, graph = A.C.me.build_va_graph(verbose=False)
    lp = A.load_pages(pages_dir)
    polys, pages = lp[0], lp[1]
    rej_polys = lp[2] if len(lp) > 2 else {}
    for ed in [e for e in polys if (pages.get(e) or {}).get("polygon_status") == "rejected"]:
        rej_polys[ed] = polys.pop(ed)  # a rejected fit is kept only for the merged-hole split, never as a piece
    res = A.assemble(polys, pages, known, va, app7, graph=graph)
    edges = A._graph_edges(va, graph)
    print(f"[{time.time() - t0:.0f}s] assembly: reconstructed {res.summary['reconstructed']}, "
          f"rejected {sorted(res.rejected)}, filled {res.filled}", flush=True)

    # 1. snap
    recon = {e: polys[e] for e in res.summary["reconstructed"]}
    kn_names = sorted(known)
    kn_lines, kn_own = _boundary_lines([known[n] for n in kn_names], kn_names)
    g1, o1 = _chunks(kn_lines, kn_own)
    va_lines, va_own = _boundary_lines(np.asarray(va.geometry.values, dtype=object), list(range(len(va))))
    g2, o2 = _chunks(va_lines, va_own)
    og, oo = _boundary_lines([recon[e] for e in sorted(recon)], sorted(recon))
    g3, o3 = _chunks(og, oo)
    nb_dir = Path(nb_dir) if nb_dir else Path(pages_dir)
    nbs = sorted(nb_dir.glob("ed*_neighbours.gpkg"))
    n_nb = 0
    for f in nbs:
        g = gpd.read_file(f).to_crs(3400)
        ln = [p for x in g.geometry if x is not None and not x.is_empty for p in shapely.get_parts(x)]
        a, b = _chunks(ln, [-1] * len(ln))
        g3, o3 = np.concatenate([g3, a]), np.concatenate([o3, b])
        n_nb += len(ln)
    tier1, tier2, tier3 = Tier("known boundary", g1, o1), Tier("VA boundary", g2, o2), Tier("other outline / neighbour line", g3, o3)
    print(f"[{time.time() - t0:.0f}s] target lines: known {len(g1)} chunks, VA {len(g2)}, outlines+neighbours {len(g3)} "
          f"({n_nb} neighbour polylines from {len(nbs)} files)", flush=True)
    snapped, snap_stats = {}, {}
    for e in sorted(recon):
        tiers = [tier1, tier2, tier3.without(e)]
        g, mv, tc, nv = snap_piece(recon[e], tiers)
        snapped[e] = g
        snap_stats[e] = {"district": name_of[e], "n_vertices": nv, "n_snapped": int(len(mv)),
                         "by_tier": {t.name: int(c) for t, c in zip(tiers, tc)},
                         "median_move_m": float(np.median(mv)) if len(mv) else None,
                         "max_move_m": float(mv.max()) if len(mv) else None,
                         "area_change_pct": 100 * (g.area - recon[e].area) / recon[e].area}
    allmv = [s for s in snap_stats.values() if s["n_snapped"]]
    snap_total = {"pieces": len(snapped), "vertices": sum(s["n_vertices"] for s in snap_stats.values()),
                  "snapped": sum(s["n_snapped"] for s in snap_stats.values()),
                  "median_of_piece_medians_m": float(np.median([s["median_move_m"] for s in allmv])) if allmv else None,
                  "max_move_m": max([s["max_move_m"] for s in allmv], default=None)}
    print(f"[{time.time() - t0:.0f}s] snapped {snap_total['snapped']}/{snap_total['vertices']} vertices "
          f"in {snap_total['pieces']} pieces", flush=True)

    # 2. drift
    pre_pieces = {**{n: g for n, g in known.items()}, **{name_of[e]: g for e, g in recon.items()}}
    pieces = {**{n: g for n, g in known.items()}, **{name_of[e]: g for e, g in snapped.items()}}
    d0, u0, _ = drift(pre_pieces, set(known))
    d1, u1, rows = drift(pieces, set(known))
    for r in rows:
        r["share_of_total_pct"] = 100 * (r["overlap_m2"] + r["gap_m2"]) / (d1 * u1) if d1 else 0.0
    print(f"[{time.time() - t0:.0f}s] drift {100 * d0:.4f}% -> {100 * d1:.4f}% (target < {100 * DRIFT_TARGET:.2f}%)", flush=True)

    # 4 then 3
    extra, merged_report = split_merged_holes(res, va, edges, {**rej_polys, **polys}, pages, name_of)
    table = assign(va, res, pieces, extra, name_of)
    dgeoms, weight = build_geometries(va, table, pieces)
    print(f"[{time.time() - t0:.0f}s] assigned {int(table.district.notna().sum())}/{len(va)} VAs, "
          f"{int(table.cut.sum())} cut, {len(extra)} from merged-hole splits", flush=True)

    # 5. sanity
    loose = {name_of[e] for e in res.filled} | {n for n in table.district[table.kind == "split"].unique() if n}
    pooled = {name_of[c["assigned_to"]] for c in res.summary["hole_fill_components"] if c.get("assigned_to") is not None
              and any(k["ed"] == c["assigned_to"] and k.get("pooled") for k in c["claims"])}
    items, adj, arows = sanity(va, table, dgeoms, known, app7, edges, name_of, ed_of, nb_dir, pieces, loose, pooled)

    items["districts_inside_page_frame"] = in_frame_item(dgeoms, pages, name_of, {e: g for e, g in snapped.items()})

    # per-district rows
    scale = float(app7["population"].sum()) / float(va["pop_2021"].sum())
    pop = {}
    for (v, n), w in weight.items():
        pop[n] = pop.get(n, 0.0) + w * float(va["pop_2021"].iloc[v]) * scale
    amap = {r["district"]: r for r in arows}
    rec_names = {name_of[e] for e in recon}
    filled_names = {name_of[e] for e in res.filled}
    split_names = {n for n in table.district[table.kind == "split"].unique() if n}
    disc = set(items["each_district_connected"]["disconnected"])
    nbm = {m["ed"]: m for m in items["page_neighbours_match_adjacency"].get("mismatches", [])}
    ov = {o["district"] for o in items["no_known_overlap_over_0.1pct"]["offenders"]}
    drows = []
    for ed in sorted(name_of):
        n = name_of[ed]
        src = ("split" if n in split_names else "known" if n in known else "placed" if n in rec_names
               else "filled" if n in filled_names else "missing")
        sel = table.district == n
        a = amap.get(n, {})
        st_pop = float(app7.loc[ed, "population"])
        pv = pop.get(n)
        fails = []
        if src == "missing":
            fails.append("missing")
        if a and a["diff_pct"] is not None and abs(a["diff_pct"]) > a["tol_pct"] and not a["informational"]:
            fails.append(f"area>{a['tol_pct']:g}%")
        if ed in disc:
            fails.append("disconnected")
        if n in ov:
            fails.append("overlaps known")
        if ed in nbm:
            fails.append("neighbours differ")
        if src == "split":
            fails.append("low_confidence")
        drows.append({"ed": ed, "district": n, "source": src, "low_confidence": src == "split",
                      "n_vas": int(sel.sum()), "n_cut": int((sel & table.cut).sum()),
                      "area_km2": a.get("area_km2"), "stated_area_km2": a.get("stated_km2"), "area_diff_pct": a.get("diff_pct"),
                      "pop_va_scaled": pv, "pop_stated": st_pop,
                      "pop_diff_pct": 100 * (pv - st_pop) / st_pop if pv is not None else None,
                      "fails": fails})

    # outputs
    ids = va[[c for c in ("OBJECTID", "VA_NUMBER") if c in va.columns]].copy()
    ids["district"] = table.district
    ids["ed"] = table.district.map(ed_of).astype("Int64")
    ids["cut"] = table.cut
    ids["cut_partners"] = table.partners.map(lambda p: ";".join(f"{n}:{s:.3f}" for n, s in p.items()))
    ids["confidence"] = np.where(table.district.isna(), "unassigned",
                         np.where(table.cut, "cut", table.kind.map({"known": "known", "placed": "placed",
                                                                    "filled": "filled", "split": "low_confidence"})))
    ids.to_csv(out_dir / "va_assignment.csv", index=False, lineterminator="\n")
    rowd = {r["district"]: r for r in drows}
    gd = gpd.GeoDataFrame([{"ed": ed_of[n], "district": n, "source": rowd[n]["source"], "n_vas": rowd[n]["n_vas"],
                            "n_cut": rowd[n]["n_cut"], "geometry": g} for n, g in sorted(dgeoms.items(), key=lambda kv: ed_of[kv[0]])],
                          crs=3400)
    gd.to_file(out_dir / "districts.gpkg", driver="GPKG")
    gpd.GeoDataFrame([{"ed": e, "district": name_of[e], "geometry": g} for e, g in sorted(snapped.items())],
                     crs=3400).to_file(out_dir / "snapped_pieces.gpkg", driver="GPKG")
    items["districts_match_locator_inset"] = inset_item(Path(inset), out_dir)
    report = {
        "inputs": {"pages": str(pages_dir), "known": which, "neighbours_dir": str(nb_dir)},
        "constants": {"SNAP_TOL_m": SNAP_TOL, "CUT_SHARE": CUT_SHARE, "DRIFT_GAP_BUF_m": DRIFT_GAP_BUF,
                      "DRIFT_TARGET": DRIFT_TARGET, "SEGMENT_MAX_m": SEGMENT_MAX},
        "drift": {"before_snap": d0, "after_snap": d1, "territory_km2": u1 / 1e6, "target": DRIFT_TARGET,
                  "pass": d1 < DRIFT_TARGET, "pairs_worst_first": rows[:30], "n_pairs": len(rows),
                  "note": "pieces = known + snapped reconstructions only; hole-filled districts have no polygon"},
        "snapping": {"total": snap_total, "per_piece": snap_stats},
        "merged_holes": merged_report,
        "assembly": {"rejected": res.rejected, "filled": res.filled, "reconstructed": res.summary["reconstructed"],
                     "failed_pages": res.summary["failed_pages"], "unassigned_components": res.unassigned_components},
        "cut_vas": int(table.cut.sum()),
        "sanity": items,
        "districts": drows,
        "seconds": round(time.time() - t0, 1),
    }
    (out_dir / "report.json").write_text(json.dumps(_plain(report), indent=1), encoding="utf-8")
    return report


def _r(x, nd=4):
    return A._round(x, nd)


def main():
    ap = argparse.ArgumentParser(description="Snap, assign VAs and sanity-check the Amendment 10 map")
    ap.add_argument("--pages", required=True, help="a10_reconstruct_pages.py output directory")
    ap.add_argument("--known", required=True, choices=["tuning", "fixed"])
    ap.add_argument("--out", required=True, help="result directory")
    ap.add_argument("--neighbours", help="directory of edNN_neighbours.json/.gpkg (default: --pages)")
    ap.add_argument("--inset", default=None, help="inset_districts.gpkg for the locator-inset cross-check (default: PAGES_DIR/inset_districts.gpkg)")
    a = ap.parse_args()
    rep = run(a.pages, a.known, a.out, a.neighbours, a.inset)
    d = rep["drift"]
    print(f"\nDRIFT before {100 * d['before_snap']:.4f}%  after {100 * d['after_snap']:.4f}%  "
          f"({'PASS' if d['pass'] else 'FAIL'} vs < {100 * DRIFT_TARGET:.2f}%), territory {d['territory_km2']:.0f} km2, {d['n_pairs']} pairs")
    for r in d["pairs_worst_first"][:8]:
        print(f"  {r['a']} | {r['b']}: overlap {r['overlap_m2'] / 1e6:.4f} km2, gap {r['gap_m2'] / 1e6:.4f} km2 "
              f"({r['share_of_total_pct']:.1f}% of drift)")
    print("SNAP", json.dumps(_r(rep["snapping"]["total"])))
    print("SANITY")
    for k, v in rep["sanity"].items():
        flag = "not run" if v["pass"] is None else ("PASS" if v["pass"] else "FAIL")
        brief = {x: y for x, y in v.items() if not isinstance(y, (list, dict)) and x != "pass"}
        print(f"  {flag:7} {k} {json.dumps(_r(brief))}")
    print("FAILING DISTRICT ROWS")
    for r in rep["districts"]:
        if r["fails"]:
            print(f"  ED {r['ed']:>2} {r['district']:<34} {r['source']:<8} vas {r['n_vas']:>4} cut {r['n_cut']:>3} "
                  f"area {r['area_diff_pct'] if r['area_diff_pct'] is None else round(r['area_diff_pct'], 1)}%  {r['fails']}")
    print(f"done in {rep['seconds']}s")


if __name__ == "__main__":
    main()
