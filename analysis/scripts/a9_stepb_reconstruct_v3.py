#!/usr/bin/env python
"""Amendment 9, Step B (second attempt): panel map page (vector PDF) -> district polygon, EPSG:3400.

Version 3 of the reconstruction procedure. Version 1 (a7_stepb_reconstruct.py) failed the
Amendment 7 calibration on 2026-11-03. Version 2 (a9_stepb_reconstruct_v2.py) was never run on
the sample: in development it placed the city pages but locked onto only 1 of the 10 changed
pages over 10,000 km2 (findings/a9_stepb_v2_development.md). Development of version 3 used only
the 22 tuning districts and the 35 changed districts; no sample page was opened
(findings/a9_stepb_v3_development.md).

Why version 2 failed on rural pages, found in development:
  - rural pages draw their lines in other styles. The dark-grey 0.92-pt strokes are the full road
    network there (a median 6-16 m from the National Road Network once placed), and the light-grey
    0.37-pt strokes are the township survey grid. Version 2's fixed style rules, set on city pages,
    matched the first against census-subdivision boundaries and the second against roads;
  - prairie roads lie on a one-mile grid, so a road search with no other information finds many
    near-equal placements a whole number of miles apart.

Version 3 keeps version 2's outline reading, references and refinement code, and changes only this:
  1. Prior from the page's municipalities. Village dots, town areas and First Nations reserve
     areas, matched by name to Statistics Canada's 2021 census subdivisions, are fitted to the
     subdivisions' centroids (two-point RANSAC, then least squares on the inliers). The prior is
     used when its rotation is within 1 degree of a multiple of 90 degrees and it has at least 4
     inliers and a scale within 10% of the stated-area scale, or exactly 3 inliers, a scale within
     1.5% and a median residual under max(150 m, 1 pt).
     Without such a prior, version 2's road search (unchanged) supplies it.
  2. Layer identification on each page. Each grey stroke style with at least 150 sample points is
     assigned to the reference it matches best (roads: NRN + OSM highways; boundaries: 2021 CSD
     boundaries), within the prior's error; a style matching neither in at least half its points
     is not used.
  3. Local refinement: the correlation search is restricted to translations within the prior's
     error (municipal prior: max(500 m, 2 x median residual); version 2 prior: 1,500 m), then
     version 2's robust ICP. If that first pass finds no usable layer or no local match, one wide
     retry runs: error max(5,000 m, 3 x the first), scale within +/-1%, layer threshold 0.4.
  4. Acceptance rule, applied before a polygon is returned: the matched page lines must lie a
     median of at most 40 m (ACCEPT_MED_M) from their references, and at least 60% of them
     (ACCEPT_IN60) within 60 m. A page that fails it raises an error and counts as a failure.

Environment: results depend on the PDF library. Development ran on Python 3.12.13 with PyMuPDF
2.1 (MuPDF 1.28.6); PyMuPDF 1.27.2.2 reads some outline strokes without a width. The registered
run must use the pinned environment (findings/a9_stepb_v3_dev/environment.txt).
Deterministic. The RANSAC's generator seed (0) is a fixed algorithm constant, not a sampling seed:
with at most 45 matches a page has at most 990 pairs, and 3,000 draws find the same inlier set
under another seed on every development page (findings/a9_stepb_v3_dev/ransac_seed_check.txt).
"""
import collections
import os
import re
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a9_stepb_reconstruct_v2 as R2  # noqa: E402  (version 2: outline, references, search, ICP)

V1 = R2.V1
TUNING = R2.TUNING
SAMPLE = R2.SAMPLE
TOWNS = {"CY", "T", "VL", "SV"}
RESERVES = {"IRI", "S-E", "MS"}
ACCEPT_MED_M = 40.0   # set from the development results (placed pages: 5.4 to 29.6 m)
ACCEPT_IN60 = 0.60    # (placed pages: 0.72 to 0.94)
last_info = {}


def _guard(n):
    if n in SAMPLE and os.environ.get("STEPB_V3_CALIBRATION_RUN") != "1":
        raise ValueError(f"ED {n} is in the calibration sample (leakage guard); "
                         "STEPB_V3_CALIBRATION_RUN=1 only for the single registered run")


def _page(n):
    if V1._doc is None:
        import pymupdf
        V1._doc = pymupdf.open(V1.PDF)
    return V1._doc[214 + n]


# --- 1. Municipal prior ---------------------------------------------------------------------

def _key(t):
    return V1._norm(re.sub(r"(?i)\bno\.?\s*", "", t))


def _name_spans(n):
    """Text lines, and runs of up to three consecutive lines in a block (wrapped names), with
    their boxes. The page's own title, other districts' labels and survey-grid numbers are skipped."""
    out = []
    for b in _page(n).get_text('dict')['blocks']:
        L = []
        for line in b.get('lines', []):
            if line['spans'][0]['color'] in (0x93241A, 0x828282, 0x4e4e4e):
                continue
            L.append((" ".join(s['text'] for s in line['spans']).strip(), line['bbox']))
        for i in range(len(L)):
            for j in range(i + 1, min(i + 4, len(L) + 1)):
                bb = np.array([x[1] for x in L[i:j]])
                out.append((" ".join(x[0] for x in L[i:j]),
                            (bb[:, 0].min(), bb[:, 1].min(), bb[:, 2].max(), bb[:, 3].max())))
    return out


def _symbols(n):
    """Village dots (dark-grey 3-5 pt fills) and town or reserve areas (grey fills), with centroids."""
    out = []
    for x in _page(n).get_drawings():
        f = x.get('fill'); r = x['rect']
        if not f or max(f) - min(f) > .02:
            continue
        if abs(f[0] - .31) < .03 and 3 < r.width < 5 and 3 < r.height < 5:
            out.append(('dot', np.array([(r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2]), None))
        elif (abs(f[0] - .8) < .03 or abs(f[0] - .61) < .03) and 1 < r.width < 150 and 1 < r.height < 150:
            try:
                poly = V1._evenodd_polygon(V1._flat(x['items']))
                if poly.area > 1:
                    out.append(('fill', np.array(poly.centroid.coords[0]), poly))
            except Exception:
                pass
    return out


def _pairs(n, maxd=15):
    g = V1._csd(); g = g[g.CSDTYPE.isin(TOWNS | RESERVES)]
    ref = {}
    for nm, typ, geom in zip(g.CSDNAME, g.CSDTYPE, g.geometry):
        ref.setdefault(_key(nm), []).append((typ, np.array(geom.centroid.coords[0]), geom.area))
    S = _symbols(n); out = []; used = set()
    for t, bb in _name_spans(n):
        k = _key(t)
        if k not in ref or len(k) < 4:
            continue
        best = None
        mid = Point((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2)
        for i, (kind, c, poly) in enumerate(S):
            if kind == 'dot':
                d = np.hypot(max(bb[0] - c[0], 0, c[0] - bb[2]), max(bb[1] - c[1], 0, c[1] - bb[3]))
            else:
                d = 0.0 if poly.intersects(mid) else poly.distance(mid)
            if d < maxd and (best is None or d < best[0]):
                best = (d, i)
        if best is None or (t, best[1]) in used:
            continue
        kind, c, poly = S[best[1]]
        for typ, rc, ra in ref[k]:
            if kind == 'dot' and typ not in TOWNS:
                continue
            out.append((t, c, rc)); used.add((t, best[1]))
    return out


def _sim_fit(P, Q):
    """Least-squares similarity with the page's y axis flipped: Q ~ s R (x, -y) + t."""
    P = P * np.array([1, -1]); pm, qm = P.mean(0), Q.mean(0); A = P - pm; B = Q - qm
    a = (A[:, 0] * B[:, 0] + A[:, 1] * B[:, 1]).sum() / (A ** 2).sum()
    b = (A[:, 0] * B[:, 1] - A[:, 1] * B[:, 0]).sum() / (A ** 2).sum()
    M = np.array([[a, -b], [b, a]]); t = qm - pm @ M.T
    return M, t, lambda X: (X * np.array([1, -1])) @ M.T + t


def _ransac(pairs, s_exp, tol, iters=3000):
    P = np.array([p[1] for p in pairs]); Q = np.array([p[2] for p in pairs])
    rng = np.random.default_rng(0)
    best = (0, None)
    for _ in range(iters):
        i, j = rng.choice(len(P), 2, replace=False)
        M, t, f = _sim_fit(P[[i, j]], Q[[i, j]]); s = np.hypot(*M[:, 0])
        if s_exp and abs(np.log(s / s_exp)) > 0.2:
            continue
        inl = np.hypot(*(f(P) - Q).T) < tol
        if inl.sum() > best[0]:
            best = (inl.sum(), inl)
    inl = best[1]
    if inl is None or inl.sum() < 2:
        return None
    M, t, f = _sim_fit(P[inl], Q[inl])
    return M, t, f, inl, np.hypot(*(f(P) - Q).T)


def _tf(p, P):
    s, th, tx, ty = p; cs, sn = np.cos(th), np.sin(th); dx = P[:, 0]; dy = -P[:, 1]
    return np.c_[s * (cs * dx - sn * dy) + tx, s * (sn * dx + cs * dy) + ty]


# --- 2-4. Layers, refinement, acceptance -----------------------------------------------------

def _styles(n, last):
    sty = collections.defaultdict(list)
    for i, x in enumerate(_page(n).get_drawings()):
        if i > last or x['type'] != 's' or not x.get('color'):
            continue
        col = tuple(round(v, 2) for v in x['color']); w = round(x.get('width') or 0, 2)
        if max(col) - min(col) > 0.03:
            continue  # greys only (roads, grid, boundaries); colours are water and the outline
        sty[(col, w)] += V1._flat(x['items'])
    return {k: V1._sample_lines(v, 3.0) for k, v in sty.items() if v}


def georeference(n):
    outline, roads, muni, txt, title = R2.extract_page(n)
    poly = V1._evenodd_polygon(outline); c = np.array(poly.centroid.coords[0])
    stated = V1._stated_area(n) * 1e6; s0 = float(np.sqrt(stated / poly.area))
    info = dict(ed=n, s_area=s0)
    src = None
    pr = _pairs(n)
    r = _ransac(pr, s0, tol=max(500, 2 * s0)) if len(pr) >= 3 else None
    if r is not None:
        M, t, f, inl, rr = r
        sr = abs(np.log(np.hypot(*M[:, 0]) / s0)); med = float(np.median(rr[inl]))
        rot = np.degrees(np.arctan2(M[1, 0], M[0, 0])); square = abs((rot + 45) % 90 - 45) < 1.0
        if square and ((inl.sum() >= 4 and sr < 0.1) or (inl.sum() == 3 and sr < 0.015 and med < max(150, s0))):
            p0 = [float(np.hypot(*M[:, 0])), float(np.arctan2(M[1, 0], M[0, 0])), *f(np.zeros((1, 2)))[0]]
            g0 = _tf(p0, c[None])[0]; pc = [p0[0], p0[1], g0[0], g0[1]]
            src = 'municipalities'; err = max(500.0, 2 * med)
            info.update(n_muni=int(inl.sum()), muni_med_m=med)
    if src is None:
        _, pv2, cv2, iv2 = R2.georeference(n)
        assert np.allclose(cv2, c)
        pc = [float(v) for v in pv2]; src = 'v2'; err = 1500.0
        info.update(v2_inlier30=iv2['inlier30'], v2_runner_up=iv2['runner_up_inlier30'], v2_wide_z=iv2['wide_z'])
    info['prior'] = src
    d = _page(n).get_drawings()
    last = max(i for i, x in enumerate(d) if x['type'] in ('s', 'fs') and x.get('color') and (x.get('width') or 0) >= 2
               and x['color'][0] > x['color'][1] + .2)
    S = {k: v for k, v in _styles(n, last).items() if len(v) >= 150}
    try:
        p, part = _refine(S, pc, c, err, (1.0,), 0.5, err / 6)
    except RuntimeError as e:
        # Wide retry, only when the first pass finds no usable layer or no local match: a sparse
        # northern page whose prior is off by more than its error, or slightly off in scale.
        tol = max(60.0, 0.25 * pc[0]); err2 = max(5000.0, 3 * err)
        p, part = _refine(S, pc, c, err2, (0.99, 0.995, 1.0, 1.005, 1.01), 0.4, min(err2 / 6, tol))
        info.update(wide_retry=True, first_pass_error=str(e))
    info.update(part)
    info.update(area_ratio=float(p[0] ** 2 * poly.area / stated), s_ratio=float(p[0] / s0))
    return poly, p, c, info


def _refine(S, pc, c, err, scales, thr, step):
    A = np.vstack([V1._apply(v, pc[0], pc[1], pc[2:], c) for v in S.values()])
    fb = (*(A.min(0) - err - 2000), *(A.max(0) + err + 2000))
    rr_, rm_ = R2._refs(fb); kr = cKDTree(rr_); km = cKDTree(rm_) if len(rm_) else None
    tol = max(60.0, 0.25 * pc[0])
    shifts = [(dx, dy) for dx in np.arange(-err, err + 1, step) for dy in np.arange(-err, err + 1, step)]
    ident = {}
    for k, v in S.items():
        sub = v[::max(1, len(v) // 1500)]; best = {}
        for name, kd in (('roads', kr), ('muni', km)):
            if kd is None:
                continue
            best[name] = float(max((kd.query(V1._apply(sub, pc[0] * q, pc[1], (pc[2] + dx, pc[3] + dy), c))[0] < tol).mean()
                                   for q in scales for dx, dy in shifts))
        nm = max(best, key=best.get); ident[k] = (nm, best[nm])
    use_r = [S[k] for k, (nm, sc) in ident.items() if nm == 'roads' and sc >= thr]
    use_m = [S[k] for k, (nm, sc) in ident.items() if nm == 'muni' and sc >= thr]
    part = {'layers': {f"{k[0][0]}/{k[1]}": (nm, round(sc, 2)) for k, (nm, sc) in ident.items()}}
    page = [np.vstack(use_r) if use_r else np.zeros((0, 2)), np.vstack(use_m) if use_m else np.zeros((0, 2))]
    if len(page[0]) + len(page[1]) < 200:
        raise RuntimeError("no page layer matches a reference")
    layers = list(zip(page, (rr_, rm_)))
    fine = R2._coarse(layers, fb, pc[0] * np.linspace(0.985, 1.015, 7), [pc[1]], c,
                      V1._cap_res(fb, R2.P['coarse_res']), R2.P['coarse_sigma'])
    fine = [x for x in fine if np.hypot(x[3] - pc[2], x[4] - pc[3]) < err]
    if not fine:
        raise RuntimeError("no local match within the prior's error")
    p1 = list(fine[0][1:]); p = R2._icp(layers, p1, c, p1[0])
    dd = np.concatenate([cKDTree(r).query(V1._apply(pp, p[0], p[1], p[2:], c))[0] for pp, r in layers if len(pp) and len(r)])
    part.update(shift_from_prior_m=float(np.hypot(p[2] - pc[2], p[3] - pc[3])), s=float(p[0]),
                theta_deg=float(np.degrees(p[1])), p=[float(v) for v in p], c=[float(v) for v in c],
                med_dist_m=float(np.median(dd)), in30=float((dd < 30).mean()), in60=float((dd < 60).mean()),
                n_layer_pts=int(len(dd)))
    return p, part


def reconstruct(ed_number):
    global last_info
    n = int(ed_number); _guard(n)
    poly, p, c, info = georeference(n)
    last_info = info
    if not (info['med_dist_m'] <= ACCEPT_MED_M and info['in60'] >= ACCEPT_IN60):
        raise RuntimeError(f"fit below the acceptance rule (median {info['med_dist_m']:.1f} m, "
                           f"within 60 m {info['in60']:.2f})")
    geoms = [poly] if poly.geom_type == 'Polygon' else list(poly.geoms)
    return unary_union([Polygon(V1._apply(np.array(g.exterior.coords), p[0], p[1], p[2:], c),
                                [V1._apply(np.array(h.coords), p[0], p[1], p[2:], c) for h in g.interiors]).buffer(0)
                        for g in geoms])
