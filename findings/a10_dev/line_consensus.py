# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
line_consensus.py
-----------------

Amendment 10, extra check 2: two drawings of each changed line. Reporting only; it never changes a placement
or an assignment, and it computes no partisan measure (population and total ballots cast only; the party
columns are summed into one ballots-cast number on load and dropped before any real-map data is touched).

Every boundary between two districts A and B is drawn on page A (A's outline) and on page B (B's outline), and
both pages also carry it as a grey stroke in edNN_neighbours.gpkg. For every adjacent pair (A, B) in the final
districts.gpkg where at least one of A, B is not 'known', the DRAWINGS of the shared boundary are

  poly:A, poly:B   the page polygon outline (edNN.gpkg), only when that district is source 'placed' and its page
                   was accepted (the page was used);
  nb:A,   nb:B     the grey strokes of page A / page B (edNN_neighbours.gpkg), whatever the district's source.

poly:X and nb:X are two strokes of one page, so they agree by construction; a DISAGREEMENT between drawings is
only counted between different pages (page A against page B).

Method
  1. Shared boundary = A.boundary within 1.5 m of B, merged; pairs with a shared edge under 200 m are corner
     touches and skipped (as in a10_snap_assign NB_MIN_EDGE_M).
  2. Sample every 25 m. For each drawing, the nearest point within 500 m (the 'clip'): distance and location.
     A drawing is present on a pair when it lies within 500 m of at least half the samples.
  3. Per pair: length, drawings present, median and 95th percentile of the distance pooled over (sample, drawing),
     length share beyond 30 m and beyond 100 m (same pooling).
  4. Disputed strips: for two drawings from different pages, consecutive samples whose nearest points are more than
     30 m apart (mean over the 25 m step) are joined into a quadrilateral between the two drawings (a 'ladder';
     jumps of the nearest point over 150 m between neighbouring samples are dropped); the strip is the union.
     A VA with more than 1% of its area in a strip and assigned to A or B is a disputed VA. Would it change?
     The region between the final line and drawing d is laddered the same way; a VA's representative point inside
     that region lies on the other side of d, so its assignment would change if the line followed d.
  5. Calibration (known=tuning): the truth line is the commission majority-map outline of the pair: both
     districts in the truth set (unchanged_56 + Calgary-Acadia) -> the shared outline of both ('both');
     one district in the truth set -> that district's outline within 600 m of the final line ('one').
     Distance from each drawing's nearest point (and from the final line) to the truth, and, where two drawings
     from different pages disagree by more than 30 m, which one is closer to truth.

Usage:
  python findings/a10_dev/line_consensus.py --snap C:/tmp/a10test/snap_tuning --tag tuning
  python findings/a10_dev/line_consensus.py --snap C:/tmp/a10test/snap_fixed  --tag fixed
Writes findings/a10_dev/line_consensus_<tag>.json and disputed_vas_<tag>.csv. Deterministic, EPSG:3400.
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
from shapely.geometry import LineString
from shapely.strtree import STRtree

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))
import a10_assemble as A  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
STEP = 25.0              # sampling step along the shared boundary (m)
CLIP = 500.0             # a drawing counts only within this distance of the shared boundary (m)
SHARE_TOL = 1.5          # shared boundary = A.boundary within this distance of B (m)
MIN_EDGE = 200.0         # shared edges shorter than this are corner touches (m)
NEAR, FAR = 30.0, 100.0  # reported thresholds (m)
PRESENT_MIN = 0.5        # a drawing is present when within CLIP of at least this share of the samples
JUMP = 150.0             # ladder: nearest points that move more than this between neighbouring samples are dropped (m)
VA_SHARE = 0.01          # a VA is disputed when more than this share of its area is in a strip
VA_SENS = 0.001          # sensitivity only: VAs with more than this share are also counted (summary.disputed_vas_sensitivity_0p1pct)
TRUTH_CLIP = 600.0       # calibration, 'one' truth: the known outline within this distance of the final line (m)
WIN_MARGIN = 10.0        # calibration: a drawing wins a disagreement when closer to truth by more than this (m)
CHUNK = 24               # segments per line chunk in the nearest-point trees


def chunks(lines):
    out = []
    for ln in lines:
        c = shapely.get_coordinates(ln)
        for i in range(0, max(len(c) - 1, 0), CHUNK):
            out.append(LineString(c[i:i + CHUNK + 1]))
    return np.array(out, dtype=object)


def line_parts(g):
    return [p for p in shapely.get_parts(g) if p.geom_type in ("LineString", "LinearRing") and not p.is_empty]


class Draw:
    def __init__(self, label, page, kind, cls, lines):
        self.label, self.page, self.kind, self.cls = label, page, kind, cls
        self.geoms = chunks(lines)
        self.tree = STRtree(self.geoms) if len(self.geoms) else None

    def nearest(self, pts, maxd=CLIP):
        n = len(pts)
        dist, xy = np.full(n, np.nan), np.full((n, 2), np.nan)
        if self.tree is None or n == 0:
            return dist, xy
        ii, dd = self.tree.query_nearest(pts, max_distance=maxd, return_distance=True, all_matches=False)
        if ii.shape[1]:
            sl = shapely.shortest_line(pts[ii[0]], self.geoms[ii[1]])
            dist[ii[0]] = dd
            xy[ii[0]] = shapely.get_coordinates(shapely.get_point(sl, -1))
        return dist, xy


def load_va():
    """VA polygons with population and ballots cast. The party columns are summed into one ballots-cast number
    and dropped on the spot: no partisan figure exists past this function."""
    me = A.C.me
    va = gpd.read_file(me.VA_PATH, columns=["OBJECTID", "VA_NUMBER", "va_ndp", "va_ucp", "va_other"])
    va["ballots_cast"] = va[["va_ndp", "va_ucp", "va_other"]].fillna(0.0).astype(float).sum(axis=1)
    va = va.drop(columns=["va_ndp", "va_ucp", "va_other"])
    pop = pd.read_csv(me.DATA / "va_pop_from_das.csv").set_index("va_row_idx")["pop_2021"]
    va["pop_2021"] = va.index.map(pop).fillna(0.0)
    if va.crs is None or va.crs.to_epsg() != 3400:
        va = va.to_crs(3400)
    return va


def sample_parts(line):
    """Midpoint samples every ~STEP m along each merged part. Returns (points array, part id, seg length)."""
    pts, pid, seg = [], [], []
    for k, ln in enumerate(line_parts(shapely.line_merge(line))):
        L = ln.length
        n = max(1, int(round(L / STEP)))
        p = shapely.line_interpolate_point(ln, (np.arange(n) + 0.5) / n * L)
        pts.append(p), pid.append(np.full(n, k)), seg.append(np.full(n, L / n))
    if not pts:
        return np.array([], dtype=object), np.array([], int), np.array([])
    return np.concatenate(pts), np.concatenate(pid), np.concatenate(seg)


def ladder(p, q, pid, ok_extra=None, min_mean=None):
    """Quadrilaterals between two point sequences p, q (N,2) joining consecutive samples of one part.
    Segment k is kept when all four corners are finite, neither side jumps more than JUMP and, if min_mean is
    given, the mean separation over the segment exceeds it. Returns (polygons array, kept mask over segments)."""
    n = len(p)
    if n < 2:
        return np.array([], dtype=object), np.zeros(0, bool)
    a0, a1, b0, b1 = p[:-1], p[1:], q[:-1], q[1:]
    fin = np.isfinite(a0).all(1) & np.isfinite(a1).all(1) & np.isfinite(b0).all(1) & np.isfinite(b1).all(1)
    ok = fin & (pid[:-1] == pid[1:])
    with np.errstate(invalid="ignore"):
        ok &= (np.hypot(*(a1 - a0).T) <= JUMP) & (np.hypot(*(b1 - b0).T) <= JUMP)
        if min_mean is not None:
            ok &= (np.hypot(*(a0 - b0).T) + np.hypot(*(a1 - b1).T)) / 2 > min_mean
    if not ok.any():
        return np.array([], dtype=object), ok
    c = np.stack([a0[ok], a1[ok], b1[ok], b0[ok], a0[ok]], axis=1)
    return shapely.make_valid(shapely.polygons(c)), ok


def stats(d):
    d = d[np.isfinite(d)]
    if not len(d):
        return {"n": 0, "median_m": None, "p95_m": None, "share_gt30": None, "share_gt100": None}
    return {"n": int(len(d)), "median_m": round(float(np.median(d)), 2), "p95_m": round(float(np.percentile(d, 95)), 2),
            "share_gt30": round(float((d > NEAR).mean()), 4), "share_gt100": round(float((d > FAR).mean()), 4)}


def pick(x):
    return None if x is None else (round(float(x), 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snap", required=True, help="snap_assign result directory (districts.gpkg, va_assignment.csv, report.json)")
    ap.add_argument("--tag", required=True, help="output tag: line_consensus_<tag>.json, disputed_vas_<tag>.csv")
    ap.add_argument("--pages", default=None, help="page fixture directory (default: report.json inputs.pages)")
    ap.add_argument("--out", default=str(OUT_DIR))
    a = ap.parse_args()
    t0 = time.time()
    snap, out = Path(a.snap), Path(a.out)
    rep = json.loads((snap / "report.json").read_text(encoding="utf-8"))
    pages_dir = Path(a.pages or rep["inputs"]["pages"])
    nb_dir = Path(rep["inputs"].get("neighbours_dir") or pages_dir)
    which = rep["inputs"]["known"]
    log = lambda m: print(f"[{time.time() - t0:.0f}s] {m}", flush=True)  # noqa: E731

    dist = gpd.read_file(snap / "districts.gpkg").to_crs(3400).sort_values("ed").reset_index(drop=True)
    src = dict(zip(dist.ed, dist.source))
    name = dict(zip(dist.ed, dist.district))
    geom = dict(zip(dist.ed, dist.geometry))
    asg = pd.read_csv(snap / "va_assignment.csv")
    va = load_va()
    va = va.merge(asg[["OBJECTID", "district", "ed", "cut", "cut_partners", "confidence"]], on="OBJECTID", how="left")
    va_area = shapely.area(np.asarray(va.geometry.values, dtype=object))
    va_rep = np.asarray(va.geometry.representative_point().values, dtype=object)
    va_tree = STRtree(np.asarray(va.geometry.values, dtype=object))
    log(f"loaded {len(va)} VAs, {len(dist)} districts ({which} map)")

    polys, pages = A.load_pages(pages_dir, with_rejected=False)
    draws = {}   # ed -> {'poly': Draw|None, 'nb': Draw|None}
    for ed in sorted(set(src)):
        d = {"poly": None, "nb": None}
        if src[ed] == "placed" and ed in polys:
            d["poly"] = Draw(f"poly:{ed}", ed, "poly", "poly_placed", line_parts(shapely.boundary(polys[ed])))
        f = nb_dir / f"ed{ed:02d}_neighbours.gpkg"
        if f.exists():
            g = gpd.read_file(f).to_crs(3400)
            ln = [p for x in g.geometry if x is not None and not x.is_empty for p in line_parts(x)]
            cls = {"known": "grey_known_page", "placed": "grey_placed_page"}.get(src[ed])
            if cls is None:   # filled / split: no page polygon was used; say whether the page fit was rejected
                cls = "grey_rejected_page" if (pages.get(ed) or {}).get("polygon_status") == "rejected" else "grey_unplaced_page"
            if ln:
                d["nb"] = Draw(f"nb:{ed}", ed, "nb", cls, ln)
        draws[ed] = d
    log(f"drawings: {sum(d['poly'] is not None for d in draws.values())} page polygons, "
        f"{sum(d['nb'] is not None for d in draws.values())} neighbour-line files")

    truth = None
    if which == "tuning":
        maj = A.load_majority()
        names = [A.norm(x) for x in json.loads(A.UNCHANGED_56.read_text(encoding="utf-8"))["districts"]]
        names += [A.norm(x) for x in A.FIXED_EXTRA]
        tg = {k: shapely.union_all(list(g.geometry)) for k, g in maj.groupby("key") if k in set(names)}
        truth = {ed: tg[A.norm(name[ed])] for ed in name if A.norm(name[ed]) in tg}
        log(f"calibration truth available for {len(truth)} districts")

    # ---- adjacent pairs ----------------------------------------------------------------------------------
    eds = list(dist.ed)
    tree = STRtree(np.array([geom[e] for e in eds], dtype=object))
    cand = sorted({(min(eds[i], eds[j]), max(eds[i], eds[j]))
                   for i, j in zip(*tree.query(np.array([geom[e] for e in eds], dtype=object), predicate="dwithin", distance=3.0))
                   if i != j})
    pairs, disputed_rows = [], []
    skipped = {"known_known": 0, "short_edge": 0, "no_shared_line": 0}
    for (ea, eb) in cand:
        if src[ea] == "known" and src[eb] == "known":
            skipped["known_known"] += 1
            continue
        sh = shapely.intersection(shapely.boundary(geom[ea]), shapely.buffer(geom[eb], SHARE_TOL))
        parts = line_parts(sh)
        if not parts:
            skipped["no_shared_line"] += 1
            continue
        line = shapely.union_all(parts)
        if line.length < MIN_EDGE:
            skipped["short_edge"] += 1
            continue
        pts, pid, seg = sample_parts(line)
        L = float(seg.sum())
        row = {"a": int(ea), "b": int(eb), "a_name": name[ea], "b_name": name[eb], "a_source": src[ea], "b_source": src[eb],
               "length_m": round(L, 1), "n_samples": int(len(pts))}
        present, dd, xx = [], {}, {}
        info = {}
        for e in (ea, eb):
            for k in ("poly", "nb"):
                d = draws[e][k]
                if d is None:
                    continue
                di, xi = d.nearest(pts)
                cov = float(np.isfinite(di).mean())
                info[d.label] = {"page": int(e), "kind": k, "class": d.cls, "coverage": round(cov, 3), **{
                    kk: v for kk, v in stats(di).items() if kk != "n"}}
                if cov >= PRESENT_MIN:
                    present.append(d)
                    dd[d.label], xx[d.label] = di, xi
        row["drawings"] = info
        row["n_drawings"] = len(present)
        row["n_pages"] = len({d.page for d in present})
        pool = np.concatenate([dd[d.label][np.isfinite(dd[d.label])] for d in present]) if present else np.array([])
        row.update({k: v for k, v in stats(pool).items()})
        row["samples_total"] = int(len(pts))

        # cross-page disagreement and strips
        strips, cross = [], []
        xs_all = np.zeros(max(len(pts), 1), bool)
        for i, di_ in enumerate(present):
            for dj_ in present[i + 1:]:
                if di_.page == dj_.page:
                    continue
                p, q = xx[di_.label], xx[dj_.label]
                with np.errstate(invalid="ignore"):
                    sep = np.hypot(*(p - q).T)
                polys_, ok = ladder(p, q, pid, min_mean=NEAR)
                fin = np.isfinite(sep)
                cross.append({"between": [di_.label, dj_.label], "n": int(fin.sum()),
                              "median_sep_m": pick(np.median(sep[fin])) if fin.any() else None,
                              "p95_sep_m": pick(np.percentile(sep[fin], 95)) if fin.any() else None,
                              "share_sep_gt30": round(float((sep[fin] > NEAR).mean()), 4) if fin.any() else None,
                              "disputed_len_m": round(float(ok.sum() * STEP), 1)})
                if len(polys_):
                    strips.append(polys_)
                    k = np.flatnonzero(ok)
                    xs_all[k] = True
                    xs_all[k + 1] = True
        row["cross_page"] = cross
        row["disputed_len_m"] = round(float(xs_all[:len(pts)].sum() * STEP), 1)
        row["_pts"], row["_pid"], row["_dd"], row["_xx"] = pts, pid, dd, xx
        row["_strips"], row["_present"], row["_seg"], row["_line"] = strips, present, seg, line
        pairs.append(row)
    log(f"{len(pairs)} pairs to check ({skipped}); sampling and nearest points done")

    # ---- disputed VAs --------------------------------------------------------------------------------------
    vcols = va.reset_index(drop=True)
    for row in pairs:
        if not row["_strips"]:
            continue
        strip = shapely.union_all(np.concatenate(row["_strips"]))
        if strip.is_empty:
            continue
        row["strip_area_m2"] = round(float(strip.area), 0)
        pts, pid = row["_pts"], row["_pid"]
        F = shapely.get_coordinates(pts)
        # region between the final line and each present drawing: a rep point inside flips to the other side
        regions = {}
        for d in row["_present"]:
            pl, ok = ladder(F, row["_xx"][d.label], pid)
            regions[d.label] = shapely.union_all(pl) if len(pl) else None
        row["region_area_m2"] = {k: (round(float(rg.area), 0) if rg is not None else None) for k, rg in regions.items()}
        idx = va_tree.query(strip, predicate="intersects")
        want = {row["a_name"], row["b_name"]}
        for v in idx:
            r = vcols.iloc[v]
            if r["district"] not in want:
                continue
            share = float(shapely.intersection(vcols.geometry.iloc[v], strip).area / va_area[v])
            if share <= VA_SENS:
                continue
            flips = [lab for lab, rg in regions.items() if rg is not None and shapely.contains_xy(rg, *shapely.get_coordinates(va_rep[v])[0])]
            disputed_rows.append({
                "pair": f"{row['a']}-{row['b']}", "pair_names": f"{row['a_name']} | {row['b_name']}",
                "OBJECTID": int(r["OBJECTID"]), "VA_NUMBER": r["VA_NUMBER"], "assigned_to": r["district"],
                "cut": bool(r["cut"]), "cut_partners": r["cut_partners"] if isinstance(r["cut_partners"], str) else "",
                "share_in_strip": round(share, 4), "would_change_if_line_followed": ";".join(flips),
                "assignment_would_change": bool(flips),
                "rep_point_in_strip": bool(shapely.contains_xy(strip, *shapely.get_coordinates(va_rep[v])[0])),
                "rep_point_to_strip_m": round(float(shapely.distance(va_rep[v], strip)), 1), "pop_2021": round(float(r["pop_2021"]), 1),
                "ballots_cast": round(float(r["ballots_cast"]), 0), "va_area_km2": round(float(va_area[v] / 1e6), 4)})
    dv_all = pd.DataFrame(disputed_rows)
    dv = dv_all[dv_all.share_in_strip > VA_SHARE].reset_index(drop=True) if len(dv_all) else dv_all
    log(f"{len(dv)} disputed VA rows (>1%), {len(dv_all)} at >0.1%")

    # ---- calibration ---------------------------------------------------------------------------------------
    calib = None
    if truth is not None:
        recs = []
        for row in pairs:
            ea, eb = row["a"], row["b"]
            pts, pid = row["_pts"], row["_pid"]
            if not len(pts):
                continue
            if ea in truth and eb in truth:
                T = shapely.intersection(shapely.boundary(truth[ea]), shapely.buffer(truth[eb], 3.0))
                kind = "both"
            elif ea in truth or eb in truth:
                tt = truth[ea if ea in truth else eb]
                T = shapely.intersection(shapely.boundary(tt), shapely.buffer(row["_line"], TRUTH_CLIP, quad_segs=4))
                kind = "one"
            else:
                continue
            tl = line_parts(T)
            if not tl:
                continue
            tdraw = Draw("truth", 0, "truth", "truth", tl)
            dF, _ = tdraw.nearest(pts, maxd=1e5)
            dT = {}
            for d in row["_present"]:
                xy = row["_xx"][d.label]
                ok = np.isfinite(xy).all(1)
                v = np.full(len(pts), np.nan)
                if ok.any():
                    v[ok], _ = tdraw.nearest(shapely.points(xy[ok]), maxd=1e5)
                dT[d.label] = v
            row["truth"] = {"kind": kind, "final_to_truth": stats(dF), "drawing_to_truth": {k: stats(v) for k, v in dT.items()}}
            recs.append((row, dF, dT, kind))
        # which drawing is closer when two pages disagree by more than 30 m
        cls_of = {}
        win = {}
        allcls, indep = {}, {}
        in60 = {e: ((pages.get(e) or {}).get("diagnostics") or {}).get("in60") for e in src}
        q60 = {"n": 0, "higher_in60_closer": 0, "lower_in60_closer": 0, "within_10m": 0, "hi": [], "lo": []}
        q60a = {"n": 0, "higher_in60_closer": 0, "lower_in60_closer": 0, "within_10m": 0, "hi": [], "lo": []}   # both pages accepted
        bad_cls = ("grey_rejected_page", "grey_unplaced_page")
        for row, dF, dT, kind in recs:
            for d in row["_present"]:
                cls_of[d.label] = d.cls
                allcls.setdefault(d.cls, []).append(dT[d.label][np.isfinite(dT[d.label])])
                if kind == "both" and row["a_source"] != "known" and row["b_source"] != "known":
                    indep.setdefault(d.cls, []).append(dT[d.label][np.isfinite(dT[d.label])])
            P = row["_present"]
            for i, di_ in enumerate(P):
                for dj_ in P[i + 1:]:
                    if di_.page == dj_.page:
                        continue
                    p, q = row["_xx"][di_.label], row["_xx"][dj_.label]
                    with np.errstate(invalid="ignore"):
                        sep = np.hypot(*(p - q).T)
                    m = np.isfinite(sep) & (sep > NEAR) & np.isfinite(dT[di_.label]) & np.isfinite(dT[dj_.label])
                    if not m.any():
                        continue
                    pi_, pj_ = in60.get(di_.page), in60.get(dj_.page)
                    if pi_ is not None and pj_ is not None and pi_ != pj_:
                        hi, lo = (di_, dj_) if pi_ > pj_ else (dj_, di_)
                        th, tl_ = dT[hi.label][m], dT[lo.label][m]
                        q60["n"] += int(m.sum())
                        q60["higher_in60_closer"] += int((th < tl_ - WIN_MARGIN).sum())
                        q60["lower_in60_closer"] += int((th > tl_ + WIN_MARGIN).sum())
                        q60["within_10m"] += int((np.abs(th - tl_) <= WIN_MARGIN).sum())
                        q60["hi"].append(th), q60["lo"].append(tl_)
                        if hi.cls not in bad_cls and lo.cls not in bad_cls:
                            q60a["n"] += int(m.sum())
                            q60a["higher_in60_closer"] += int((th < tl_ - WIN_MARGIN).sum())
                            q60a["lower_in60_closer"] += int((th > tl_ + WIN_MARGIN).sum())
                            q60a["within_10m"] += int((np.abs(th - tl_) <= WIN_MARGIN).sum())
                            q60a["hi"].append(th), q60a["lo"].append(tl_)
                    ci, cj = sorted([di_.cls, dj_.cls])
                    flip = di_.cls != ci
                    ti, tj = (dT[dj_.label][m], dT[di_.label][m]) if flip else (dT[di_.label][m], dT[dj_.label][m])
                    w = win.setdefault((ci, cj), {"n": 0, "first_closer": 0, "second_closer": 0, "tie": 0, "first": [], "second": [], "final": []})
                    w["n"] += int(m.sum())
                    diff = ti - tj
                    w["first_closer"] += int((diff < -WIN_MARGIN).sum())
                    w["second_closer"] += int((diff > WIN_MARGIN).sum())
                    w["tie"] += int((np.abs(diff) <= WIN_MARGIN).sum())
                    w["first"].append(ti), w["second"].append(tj), w["final"].append(dF[m])
        calib = {
            "truth_districts": len(truth), "pairs_with_truth": len(recs),
            "independent_pairs_neither_known": sum(1 for r in recs if r[3] == "both" and r[0]["a_source"] != "known" and r[0]["b_source"] != "known"),
            "pairs_with_truth_by_kind": {k: sum(1 for r in recs if r[3] == k) for k in ("both", "one")},
            "final_line_to_truth": stats(np.concatenate([r[1][np.isfinite(r[1])] for r in recs])) if recs else None,
            "final_line_to_truth_pairs_both_true": stats(np.concatenate([r[1][np.isfinite(r[1])] for r in recs if r[3] == "both"])) if any(r[3] == "both" for r in recs) else None,
            "independent_final_line_to_truth": (lambda v: stats(np.concatenate(v)) if v else None)(
                [r[1][np.isfinite(r[1])] for r in recs if r[3] == "both" and r[0]["a_source"] != "known" and r[0]["b_source"] != "known"]),
            "independent_drawing_class_to_truth": {c: stats(np.concatenate(v)) for c, v in sorted(indep.items())},
            "drawing_class_to_truth": {c: stats(np.concatenate(v)) for c, v in sorted(allcls.items())},
            "disagreements_by_class_pair": {
                f"{k[0]} vs {k[1]}": {
                    "samples_disagreeing_gt30": w["n"], "first_closer_gt10m": w["first_closer"], "second_closer_gt10m": w["second_closer"],
                    "within_10m_of_each_other": w["tie"],
                    "first_median_to_truth_m": pick(np.median(np.concatenate(w["first"]))),
                    "second_median_to_truth_m": pick(np.median(np.concatenate(w["second"]))),
                    "final_median_to_truth_m": pick(np.median(np.concatenate(w["final"])))} for k, w in sorted(win.items())},
            "disagreements_by_page_fit": {k: (v if k not in ("hi", "lo") else None) for k, v in q60.items() if k not in ("hi", "lo")} | {
                "higher_in60_median_to_truth_m": pick(np.median(np.concatenate(q60["hi"]))) if q60["hi"] else None,
                "lower_in60_median_to_truth_m": pick(np.median(np.concatenate(q60["lo"]))) if q60["lo"] else None,
                "note": "in60 = share of the page's layer points within 60 m of the reference (edNN.json diagnostics); drawings from two different pages that differ by more than 30 m"},
            "disagreements_by_page_fit_accepted_pages_only": {k: v for k, v in q60a.items() if k not in ("hi", "lo")} | {
                "higher_in60_median_to_truth_m": pick(np.median(np.concatenate(q60a["hi"]))) if q60a["hi"] else None,
                "lower_in60_median_to_truth_m": pick(np.median(np.concatenate(q60a["lo"]))) if q60a["lo"] else None},
            "note": "class pairs list the lexicographically first class as 'first'; for two drawings of one class the order is arbitrary, use disagreements_by_page_fit",
        }

    # ---- output --------------------------------------------------------------------------------------------
    pubpairs = [{k: v for k, v in r.items() if not k.startswith("_")} for r in pairs]
    pooled = np.concatenate([np.concatenate([r["_dd"][d.label][np.isfinite(r["_dd"][d.label])] for d in r["_present"]])
                             for r in pairs if r["_present"]]) if pairs else np.array([])
    bycls = {}
    for r in pairs:
        for d in r["_present"]:
            bycls.setdefault(d.cls, []).append(r["_dd"][d.label][np.isfinite(r["_dd"][d.label])])
    accepted = [v for c, vs in bycls.items() if c in ("poly_placed", "grey_placed_page", "grey_known_page") for v in vs]
    summ = {"pairs_checked": len(pairs), "pairs_with_drawings": sum(1 for r in pairs if r["n_drawings"]),
            "pairs_with_two_pages": sum(1 for r in pairs if r["n_pages"] >= 2),
            "pairs_skipped": skipped, "total_length_km": round(sum(r["length_m"] for r in pairs) / 1000, 1),
            "pooled_over_pairs_and_drawings": stats(pooled),
            "pooled_by_drawing_class": {c: stats(np.concatenate(v)) for c, v in sorted(bycls.items())},
            "pooled_accepted_pages_only": stats(np.concatenate(accepted)) if accepted else None,
            "pair_median_of_medians_m": pick(np.median([r["median_m"] for r in pairs if r["median_m"] is not None])) if pairs else None,
            "pairs_with_95th_over_100m": sum(1 for r in pairs if r["p95_m"] is not None and r["p95_m"] > FAR),
            "pairs_with_any_disputed_strip": sum(1 for r in pairs if r["disputed_len_m"] > 0),
            "disputed_length_km": round(sum(r["disputed_len_m"] for r in pairs) / 1000, 2)}
    if len(dv):
        u = dv.drop_duplicates("OBJECTID")
        ch = dv[dv.assignment_would_change].drop_duplicates("OBJECTID")
        summ["disputed_vas"] = {"rows": int(len(dv)), "unique_vas": int(len(u)), "cut_flagged": int(u.cut.sum()),
                                "would_change": int(len(ch)), "would_change_cut_flagged": int(ch.cut.sum()),
                                "pop_2021_unique": round(float(u.pop_2021.sum()), 0), "ballots_cast_unique": round(float(u.ballots_cast.sum()), 0),
                                "pop_2021_would_change": round(float(ch.pop_2021.sum()), 0), "ballots_cast_would_change": round(float(ch.ballots_cast.sum()), 0)}
    else:
        summ["disputed_vas"] = {"rows": 0, "unique_vas": 0, "would_change": 0, "pop_2021_unique": 0, "ballots_cast_unique": 0}
    if len(dv_all):
        u = dv_all.drop_duplicates("OBJECTID")
        ch = dv_all[dv_all.assignment_would_change].drop_duplicates("OBJECTID")
        summ["disputed_vas_sensitivity_0p1pct"] = {"unique_vas": int(len(u)), "would_change": int(len(ch)),
                                                   "pop_2021_unique": round(float(u.pop_2021.sum()), 0),
                                                   "pop_2021_would_change": round(float(ch.pop_2021.sum()), 0),
                                                   "ballots_cast_would_change": round(float(ch.ballots_cast.sum()), 0)}

    # ---- item 4a: split districts ------------------------------------------------------------------------
    split = {"merged_holes_in_report": rep.get("merged_holes", []),
             "districts_with_source_split": [int(e) for e in dist.ed if src[e] == "split"]}
    if not split["merged_holes_in_report"] and not split["districts_with_source_split"]:
        split["result"] = "no split districts in this map: merged_holes is empty and no district has source 'split'"
    else:
        lines = []
        for h in split["merged_holes_in_report"]:
            c = sorted(int(x) for x in h["claimants"])
            row = next((r for r in pairs if (r["a"], r["b"]) == tuple(c)), None)
            vas = va[va.confidence == "low_confidence"]
            vas = vas[vas.district.isin([name[x] for x in c])]
            if row is None or vas.empty:
                lines.append({"claimants": c, "result": "pair not among the checked pairs or no split VAs found"})
                continue
            # the split line proper: contact between a hole VA given to one claimant and a hole VA given to the other
            zones = [shapely.buffer(shapely.union_all(np.asarray(vas[vas.district == name[x]].geometry.values, dtype=object)), SHARE_TOL)
                     for x in c]
            inz = shapely.contains(zones[0], row["_pts"]) & shapely.contains(zones[1], row["_pts"])
            ent = {"claimants": c, "names": [name[x] for x in c], "n_vas_in_hole": int(h.get("n_vas", len(vas))),
                   "split_line_samples": int(inz.sum()), "split_line_length_m": round(float(row["_seg"][inz].sum()), 1),
                   "whole_pair_line_length_m": row["length_m"], "drawings": {}}
            for lab, dv_ in row["_dd"].items():
                ent["drawings"][lab] = {"class": next(d.cls for d in row["_present"] if d.label == lab),
                                        **stats(dv_[inz])}
            pool = np.concatenate([dv_[inz][np.isfinite(dv_[inz])] for dv_ in row["_dd"].values()]) if row["_dd"] else np.array([])
            ent["pooled"] = stats(pool)
            xs = [c_ for c_ in row["cross_page"]]
            ent["cross_page_between_pages"] = xs
            lines.append(ent)
        split["split_lines"] = lines
    out_json = {"snap": str(snap), "known": which, "pages": str(pages_dir), "neighbours": str(nb_dir),
                "constants": {"STEP_m": STEP, "CLIP_m": CLIP, "SHARE_TOL_m": SHARE_TOL, "MIN_EDGE_m": MIN_EDGE, "NEAR_m": NEAR,
                              "FAR_m": FAR, "PRESENT_MIN": PRESENT_MIN, "JUMP_m": JUMP, "VA_SHARE": VA_SHARE},
                "method_notes": {"strip": "ladder: quadrilaterals between the nearest points of two drawings on consecutive 25 m samples where the mean separation exceeds 30 m, union",
                                 "would_change": "VA representative point inside the ladder region between the final line and a drawing",
                                 "pop_2021": "area-weighted 2021 DA population proxy of the whole VA (not apportioned for cut VAs)",
                                 "ballots_cast": "sum of the recorded candidate votes of the VA (2023 election-day layer)"},
                "summary": summ, "calibration": calib, "split_districts_item_4a": split, "pairs": pubpairs,
                "seconds": round(time.time() - t0, 1)}
    (out / f"line_consensus_{a.tag}.json").write_text(json.dumps(out_json, indent=1, default=str) + "\n", encoding="utf-8")
    dv.to_csv(out / f"disputed_vas_{a.tag}.csv", index=False, lineterminator="\n")
    log(f"wrote line_consensus_{a.tag}.json and disputed_vas_{a.tag}.csv")
    print(json.dumps({"summary": summ, "calibration": calib, "split": split.get("result", split.get("split_lines"))}, indent=1, default=str))


if __name__ == "__main__":
    main()
