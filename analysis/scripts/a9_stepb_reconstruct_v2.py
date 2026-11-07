#!/usr/bin/env python
"""Amendment 9, Step B (second attempt): panel map page (vector PDF) -> district polygon, EPSG:3400.

Version 2 of analysis/scripts/a7_stepb_reconstruct.py. The first version (frozen at 2a1aa42b)
failed the Amendment 7 calibration on 2026-11-03 (findings/a7_stepb_calibration.md):
  - it matched only the city pages' arterial-road style, so 12 rural and small-city pages had no
    usable strokes;
  - it accepted the district outline only at 2.76 pt, so a page drawn at another width failed, and
    a page could fall back to the small locator inset's outline.
Version 2 changes exactly these things, and nothing that the tuning set did not need:
  1. Outline: the page's own outline is the reddish stroke (R > G + 0.2, R > B + 0.2), at least
     2.0 pt wide, with the largest extent; strokes of that style smaller than a quarter of it are
     dropped (the locator inset is drawn after the main map and is excluded as before).
  2. Two matched layers instead of one, each against its own reference:
       roads      grey 0.70 strokes, 0.30-1.60 pt (arterial and local roads)
                  -> Statistics Canada National Road Network, Alberta, edition 17.0 (all road
                     segments; data/reference/nrn/), plus the OpenStreetMap highways used before;
       boundaries grey 0.45-0.55 strokes, 0.85-1.00 pt, and the dark brown 2.76-pt stroke
                  (municipal and county lines, established on tuning pages only)
                  -> Statistics Canada 2021 census-subdivision boundaries.
     The coarse search sums the two layers' correlations; the ICP fits both layers at once.
  3. Scale from the panel's stated area (App. 7): the search runs over +/-15% of the scale at
     which the outline's area equals the stated area, and the chosen transform must give an area
     within 10% of it. (Version 1 searched 3-40 m/pt with no prior; on city pages its recovered
     scale agreed with the stated area within 2.5%. With the denser road reference a prior-free
     scale search locks onto wrong scales.) A page with no candidate passing raises an error
     (counted as a failure), never a guess.
Everything else (window from place names, FFT search over scale and the four rotations,
two-way robust ICP, choice by inlier share) is version 1's.

Development used only the 22 tuning districts (with their official geometry) and the 35
changed districts' pages (which have no official geometry). No sample page was opened.
Deterministic: no random numbers are used.
"""
import os
import sys
from pathlib import Path

import numpy as np
import geopandas as gpd
from shapely.geometry import box, LineString
from shapely.ops import unary_union
from scipy.signal import fftconvolve
from scipy.ndimage import distance_transform_edt
from scipy.spatial import cKDTree
from scipy.optimize import least_squares

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a7_stepb_reconstruct as V1  # noqa: E402  (shared helpers, unchanged)

ROOT = V1.ROOT
NRN = ROOT + "data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg"
OSM = ROOT + "data/osm/alberta_osm_highways.gpkg"
CSD = ROOT + "data/shapefiles/reference/alberta_2021_csds.gpkg"
TUNING = V1.TUNING
SAMPLE = [2, 6, 8, 10, 11, 13, 14, 18, 26, 27, 31, 34, 35, 36, 39, 41, 44, 47, 50, 51, 55, 56, 57, 59,
          64, 66, 70, 75, 77, 78, 82, 83, 86, 89]

P = dict(V1.P)
P.update(
    road_grey=0.70, road_tol=0.03, road_wmin=0.30, road_wmax=1.60,
    muni_grey_min=0.45, muni_grey_max=0.55, muni_wmin=0.85, muni_wmax=1.00,
    muni_brown=(0.43, 0.38, 0.29), muni_brown_w=2.76,
    outline_wmin=2.0, outline_keep=0.25,
    area_tol=0.10, area_span=0.15, ref_step_m=20.0,
)
last_info = {}


def _guard(n):
    if n in SAMPLE and os.environ.get("STEPB_V2_CALIBRATION_RUN") != "1":
        raise ValueError(f"ED {n} is in the calibration sample (leakage guard); "
                         "STEPB_V2_CALIBRATION_RUN=1 only for the single registered run")


def _grey(c, lo, hi, tol=0.02):
    return c is not None and max(c) - min(c) < tol and lo <= c[0] <= hi


def extract_page(n):
    if V1._doc is None:
        import pymupdf
        V1._doc = pymupdf.open(V1.PDF)
    pg = V1._doc[214 + n]
    d = pg.get_drawings()
    red = [i for i, x in enumerate(d) if x['type'] in ('s', 'fs') and x.get('color') and (x.get('width') or 0) >= P['outline_wmin']
           and x['color'][0] > x['color'][1] + .2 and x['color'][0] > x['color'][2] + .2]
    if not red:
        raise RuntimeError("no outline stroke found")
    ext = {i: d[i]['rect'].width + d[i]['rect'].height for i in red}
    top = max(ext.values())
    oidx = [i for i in red if ext[i] >= P['outline_keep'] * top]
    last = max(oidx)
    outline, roads, muni = [], [], []
    for i, x in enumerate(d):
        if i in oidx:
            outline += V1._flat(x['items']); continue
        if i > last or x['type'] != 's':
            continue
        c, w = x.get('color'), x.get('width') or 0
        if _grey(c, P['road_grey'] - P['road_tol'], P['road_grey'] + P['road_tol']) and P['road_wmin'] <= w <= P['road_wmax']:
            roads += V1._flat(x['items'])
        elif ((_grey(c, P['muni_grey_min'], P['muni_grey_max']) and P['muni_wmin'] <= w <= P['muni_wmax'])
              or (c is not None and max(abs(a - b) for a, b in zip(c, P['muni_brown'])) < 0.02
                  and abs(w - P['muni_brown_w']) < 0.05)):
            muni += V1._flat(x['items'])
    txt, title = [], []
    for b in pg.get_text('dict')['blocks']:
        for line in b.get('lines', []):
            for s in line['spans']:
                txt.append(s['text'])
                if s['font'].startswith('Arial-Bold') and s['color'] == 0x93241A and not s['text'].strip().isdigit():
                    title.append(s['text'])
    return outline, roads, muni, txt, " ".join(title)


def _lines_in(path, bounds, boundary=False):
    crs = gpd.read_file(path, rows=1).crs
    bb = gpd.GeoSeries([box(*bounds)], crs=3400).to_crs(crs).total_bounds
    g = gpd.read_file(path, bbox=tuple(bb))
    if not len(g):
        return []
    g = g.to_crs(3400)
    geoms = g.geometry.boundary if boundary else g.geometry
    out = []
    for geom in geoms:
        for part in getattr(geom, "geoms", [geom]):
            if part.length > 0:
                out.append(np.array(part.coords))
    return out


def _refs(wb):
    roads = _lines_in(NRN, wb) + _lines_in(OSM, wb)
    muni = _lines_in(CSD, wb, boundary=True)
    return (V1._sample_lines(roads, P['ref_step_m']) if roads else np.zeros((0, 2)),
            V1._sample_lines(muni, P['ref_step_m']) if muni else np.zeros((0, 2)))


def _field(pts, wb, res, sigma):
    x0, y0, x1, y1 = wb
    nx = int((x1 - x0) / res) + 1; ny = int((y1 - y0) / res) + 1
    R = np.zeros((ny, nx), bool)
    if len(pts):
        ix = ((pts[:, 0] - x0) / res).astype(int); iy = ((pts[:, 1] - y0) / res).astype(int)
        m = (ix >= 0) & (ix < nx) & (iy >= 0) & (iy < ny); R[iy[m], ix[m]] = True
    if not R.any():
        return np.zeros((ny, nx), np.float32)
    return np.exp(-distance_transform_edt(~R) * res / sigma).astype(np.float32)


def _coarse(layers, wb, s_list, th_list, c, res, sigma, zscore=False):
    """layers: [(page pts, ref pts)]; correlation summed over layers, each normalised by its points."""
    F = [_field(r, wb, res, sigma) for _, r in layers]
    allp = np.vstack([p for p, _ in layers])
    best = []
    for s in s_list:
        for th in th_list:
            cs, sn = np.cos(th), np.sin(th)
            def grid(pp):
                dx = pp[:, 0] - c[0]; dy = -(pp[:, 1] - c[1])
                return s * (cs * dx - sn * dy), s * (sn * dx + cs * dy)
            qx, qy = grid(allp)
            ox, oy = np.floor(qx / res).astype(int).min(), np.floor(qy / res).astype(int).min()
            C = None; ok = True
            for (pp, _), f in zip(layers, F):
                if not len(pp):
                    continue
                gx, gy = grid(pp)
                ax = np.floor(gx / res).astype(int) - ox; ay = np.floor(gy / res).astype(int) - oy
                shp = (int(np.floor(qy / res).astype(int).max() - oy) + 1, int(np.floor(qx / res).astype(int).max() - ox) + 1)
                if shp[0] >= f.shape[0] or shp[1] >= f.shape[1]:
                    ok = False; break
                T = np.zeros(shp, np.float32); np.add.at(T, (ay, ax), 1)
                Ci = fftconvolve(f, T[::-1, ::-1], mode='valid') / len(pp)
                C = Ci if C is None else C + Ci
            if not ok or C is None:
                continue
            j = np.unravel_index(np.argmax(C), C.shape)
            z = float((C[j] - C.mean()) / (C.std() + 1e-9)) if zscore else float(C[j])
            best.append((z, s, th, wb[0] + j[1] * res - ox * res, wb[1] + j[0] * res - oy * res))
    best.sort(reverse=True)
    return best


def _icp(layers, p0, c, s0):
    trees = [cKDTree(r) if len(r) else None for _, r in layers]
    p = np.array(p0, float)
    for rad in P['icp_radii']:
        for _ in range(P['icp_iters']):
            subs = []
            for (pp, r), kd in zip(layers, trees):
                if kd is None or not len(pp):
                    continue
                G = V1._apply(pp, p[0], p[1], p[2:], c)
                keep = kd.query(G)[0] < rad
                keepr = cKDTree(G).query(r)[0] < rad
                subs.append((pp, pp[keep], kd, r[keepr]))
            if sum(len(s[1]) for s in subs) < 20:
                break
            fs = P['icp_fscale']

            def res(q):
                out = []
                for pp, sub, kd, subr in subs:
                    if len(sub):
                        out.append(kd.query(V1._apply(sub, q[0], q[1], q[2:], c))[0])
                    if len(subr) > 20:
                        out.append(cKDTree(V1._apply(pp, q[0], q[1], q[2:], c)).query(subr)[0])
                out.append([(q[0] / s0 - 1) / P['icp_sprior'] * fs])
                out.append([(q[1] - p0[1]) / np.radians(0.5) * fs])
                return np.concatenate(out)
            p = least_squares(res, p, loss='soft_l1', f_scale=fs, x_scale=[0.1, 0.001, 10, 10]).x
    return p


def _inliers(layers, p, c):
    n = hit = 0
    for pp, r in layers:
        if len(pp) and len(r):
            d = cKDTree(r).query(V1._apply(pp, p[0], p[1], p[2:], c))[0]
            n += len(d); hit += int((d < 30).sum())
    return hit / max(n, 1)


def georeference(n, window=None):
    outline, roads, muni, txt, title = extract_page(n)
    poly = V1._evenodd_polygon(outline)
    c = np.array(poly.centroid.coords[0])
    page = [V1._sample_lines(a, P['page_step_pt']) if a else np.zeros((0, 2)) for a in (roads, muni)]
    if sum(len(x) for x in page) < 50:
        raise RuntimeError("too few road or boundary strokes on the page")
    hits, anchors = V1._window(txt, title)
    stated = V1._stated_area(n) * 1e6
    info = dict(ed=n, title=title, n_road_pts=len(page[0]), n_muni_pts=len(page[1]), anchors=anchors,
                csd_hits=[h[0] for h in hits][:10])
    if hits:
        wb = unary_union([h[1] for h in hits]).envelope.buffer(P['window_buf']).bounds
    elif window is not None:
        wb = tuple(window); info['window_given'] = True
    else:
        raise RuntimeError("no CSD name found on the page")
    # The window must hold the whole drawn map at the candidate scales (version 1 matched only
    # the arterial roads, a smaller footprint): extend it by the page footprint at the largest scale.
    allp0 = np.vstack([x for x in page if len(x)])
    span = (allp0.max(0) - allp0.min(0)).max() * float(np.sqrt(stated / poly.area)) * (1 + P['area_span'])
    wb = (wb[0] - span / 2, wb[1] - span / 2, wb[2] + span / 2, wb[3] + span / 2)
    rr, rm = _refs(wb)
    layers = list(zip(page, (rr, rm)))
    res = V1._cap_res(wb, P['wide_res'])
    # Scale: the panel's stated area fixes it to within a few percent (the tuning set recovered it
    # within 2.5%), so the wide search runs over +/-15% of the stated-area scale.
    s_area = float(np.sqrt(stated / poly.area))
    s_wide = s_area * np.exp(np.arange(np.log(1 - P['area_span']), np.log(1 + P['area_span']) + 1e-9, P['s_step'] / 2))
    wide = _coarse(layers, wb, s_wide, np.radians(P['angles_deg']), c, res, max(P['wide_sigma'], 1.5 * res), zscore=True)
    cands, used = [], []
    for z, s, th, tx, ty in wide:
        if len(used) >= P['n_cand']:
            break
        if any(abs(th - u[1]) < 1e-6 and abs(np.log(s / u[0])) < 1.5 * P['s_step'] and np.hypot(tx - u[2], ty - u[3]) < 1500 for u in used):
            continue
        used.append((s, th, tx, ty))
        allp = np.vstack([x for x in page if len(x)])
        foot = V1._apply(allp, s, th, (tx, ty), c)
        fb = (foot[:, 0].min() - 2000, foot[:, 1].min() - 2000, foot[:, 0].max() + 2000, foot[:, 1].max() + 2000)
        sl = s * np.linspace(1 - P['scale_span'], 1 + P['scale_span'], P['scale_n'])
        fine = _coarse(layers, fb, sl, [th], c, V1._cap_res(fb, P['coarse_res']), P['coarse_sigma'])
        if not fine:
            continue
        _, s2, th2, tx2, ty2 = fine[0]
        p = _icp(layers, [s2, th2, tx2, ty2], c, s2)
        area_ratio = p[0] ** 2 * poly.area / stated
        cands.append((_inliers(layers, p, c), p, z, area_ratio))
    ok = [x for x in cands if abs(x[3] - 1) <= P['area_tol']]
    if not ok:
        raise RuntimeError(f"no candidate consistent with the stated area ({len(cands)} candidates)")
    ok.sort(key=lambda a: -a[0])
    inl, p, z, ar = ok[0]
    info.update(wide_z=z, inlier30=inl, area_ratio=float(ar), s=float(p[0]), theta_deg=float(np.degrees(p[1])),
                tx=float(p[2]), ty=float(p[3]), runner_up_inlier30=(ok[1][0] if len(ok) > 1 else None),
                n_candidates=len(cands))
    return poly, p, c, info


def reconstruct(ed_number, window=None):
    global last_info
    from shapely.geometry import Polygon
    n = int(ed_number); _guard(n)
    poly, p, c, info = georeference(n, window)

    def tf(g):
        return Polygon(V1._apply(np.array(g.exterior.coords), p[0], p[1], p[2:], c),
                       [V1._apply(np.array(h.coords), p[0], p[1], p[2:], c) for h in g.interiors])
    geoms = [poly] if poly.geom_type == 'Polygon' else list(poly.geoms)
    out = unary_union([tf(g).buffer(0) for g in geoms])
    last_info = info
    return out
