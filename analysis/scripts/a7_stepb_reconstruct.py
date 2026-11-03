#!/usr/bin/env python
"""Amendment 7, Step B reconstruction (frozen copy of the tuning-set procedure; see
findings/a7_stepb_tuning_results.md).

Step B reconstruction: panel map page (vector PDF) -> district polygon in EPSG:3400.

reconstruct(ed_number) -> shapely Polygon/MultiPolygon (EPSG:3400)
CLI: python reconstruct.py 3 5 7 ... [--out out.gpkg]

Method (see tuning_results.md):
 1. Extract the page's own district outline (2.76 pt reddish stroke) and its main-map linework
    (all drawings painted before the outline; the inset locator + labels come after).
 2. Page->3400 transform: g = s * R(theta) * (x-cx, -(y-cy)) + t, theta in {0,90,180,270} (+ fine ICP).
    Page CRS is 10-TM-compatible (verified on tuning pages), so no projective term.
 3. Search window from CSD names found in the page text (city / county polygons).
 4. Coarse: FFT cross-correlation of page arterial strokes vs OSM-highway proximity field over
    scale (area prior) x 4 rotations; top candidates ICP-refined (robust, both directions); keep best.
Deterministic: no random numbers are used anywhere (no RNG, no sampling).
This module reads NO electoral-district geometry; truth is only touched by evaluate.py.
"""
import os, sys, re, argparse
import numpy as np
import geopandas as gpd
import pandas as pd
import pymupdf
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union, polygonize
from scipy.signal import fftconvolve
from scipy.ndimage import distance_transform_edt
from scipy.spatial import cKDTree
from scipy.optimize import least_squares

from pathlib import Path as _Path
ROOT = _Path(__file__).resolve().parents[2].as_posix() + "/"
PDF = ROOT + "evidence/legislature/iap_report_2026_hires.pdf"
STATED = ROOT + "data/iap/iap_app7_populations.csv"  # App. 7, transcribed at stage 1
TUNING = [3, 5, 7, 9, 12, 15, 16, 17, 19, 20, 21, 23, 24, 25, 29, 30, 32, 37, 38, 43, 65, 88]

# ---- parameters (all of them) ----
P = dict(
    road_color=(0.7, 0.7, 0.7), road_wmin=0.88, road_wmax=1.45,   # arterial strokes on the page
    page_step_pt=3.0, osm_step_m=15.0,
    s_min=3.0, s_max=40.0, s_step=0.08,    # prior-free wide scale search (m/pt, log-spaced)
    wide_res=100.0, wide_sigma=150.0, max_cells=25e6, cluster_km=25.0,
    scale_span=0.07, scale_n=15,           # local fine scale search around each wide candidate
    angles_deg=(0, 90, 180, 270),
    coarse_res=25.0, coarse_sigma=60.0,
    window_buf=6000.0, n_cand=6,
    icp_radii=(120, 60, 30, 15), icp_iters=3, icp_fscale=10.0, icp_sprior=0.04,
)

_doc = None; _csd_df = None; _stated = None
last_info = {}


def _guard(n):
    if n not in TUNING and os.environ.get("STEPB_ALLOW_ANY") != "1":
        raise ValueError(f"ED {n} is not a tuning district (leakage guard); "
                         "set STEPB_ALLOW_ANY=1 only for the post-calibration run")


def _flat(items):
    out = []; cur = None
    for it in items:
        if it[0] == 'l':
            segs = [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] == 'c':
            Pq = np.array([[q.x, q.y] for q in it[1:5]]); t = np.linspace(0, 1, 6)[:, None]
            B = (1-t)**3*Pq[0] + 3*(1-t)**2*t*Pq[1] + 3*(1-t)*t**2*Pq[2] + t**3*Pq[3]
            segs = [tuple(r) for r in B]
        elif it[0] == 're':
            r = it[1]; segs = [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x0, r.y0)]
        else:
            continue
        if cur is not None and np.hypot(cur[0]-segs[0][0], cur[1]-segs[0][1]) < 1e-3:
            out[-1].extend(segs[1:])
        else:
            out.append(list(segs))
        cur = segs[-1]
    return [np.array(o) for o in out if len(o) >= 2]


def _r2(t):
    return tuple(round(float(v), 2) for v in t) if t is not None else None


def extract_page(n):
    global _doc
    if _doc is None:
        _doc = pymupdf.open(PDF)
    pg = _doc[214+n]
    d = pg.get_drawings()
    oidx = [i for i, x in enumerate(d) if x['type'] in ('s', 'fs') and x.get('color') and x.get('width')
            and abs(x['width']-2.76) < .05 and x['color'][0] > x['color'][1]+.2 and x['color'][0] > x['color'][2]+.2]
    if not oidx:
        raise RuntimeError("no outline stroke found")
    outline = []; roads = []
    for i, x in enumerate(d):
        if i in oidx:
            outline += _flat(x['items']); continue
        if i > max(oidx):
            continue
        c = x.get('color'); w = x['width'] or 0
        if (x['type'] == 's' and c is not None and max(abs(a-b) for a, b in zip(c, P['road_color'])) < 0.02
                and P['road_wmin'] <= w <= P['road_wmax']):
            roads += _flat(x['items'])
    txt = []; title = []
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                txt.append(s['text'])
                # the page's own district-name label: Arial-Bold, red #93241A, not a bare number
                if s['font'].startswith('Arial-Bold') and s['color'] == 0x93241A and not s['text'].strip().isdigit():
                    title.append(s['text'])
    return outline, roads, txt, " ".join(title)


def _evenodd_polygon(paths):
    """Even-odd fill of the closed outline path(s) -> Polygon/MultiPolygon (handles self-touching / enclaves)."""
    lines = unary_union([LineString(p) for p in paths if len(p) > 1])
    faces = list(polygonize(lines))
    S = np.vstack([np.c_[p[:-1], p[1:]] for p in paths])
    keep = []
    x1, y1, x2, y2 = S[:, 0], S[:, 1], S[:, 2], S[:, 3]
    dy = np.where(y2 == y1, 1, y2-y1)
    for f in faces:
        q = f.representative_point(); x, y = q.x, q.y
        cond = ((y1 > y) != (y2 > y)) & (x < (x2-x1)*(y-y1)/dy+x1)
        if cond.sum() % 2 == 1:
            keep.append(f)
    return unary_union(keep)


def _csd():
    global _csd_df
    if _csd_df is None:
        g = gpd.read_file(ROOT + "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(3400)
        g['nm'] = g.CSDNAME.map(_norm)
        _csd_df = g
    return _csd_df


def _norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def _window(txt, title):
    """Search window from CSD names. Anchor = CSDs named in the page's own red title label; keep only CSD hits
    within P['cluster_km'] of the anchor (drops spurious far-away name matches). No anchor -> densest cluster
    of hits (ties by name). No hits -> None (caller falls back to the province at capped resolution)."""
    g = _csd()
    blob = " | ".join(_norm(t) for t in txt)
    tblob = " " + _norm(title.replace("-", " ")) + " "
    hits = []; anchors = []
    for nm, geom, nmo in zip(g.nm, g.geometry, g.CSDNAME):
        if len(nm) < 4:
            continue
        if re.search(r"(^|[ |])" + re.escape(nm) + r"($|[ |])", blob):
            hits.append((nmo, geom))
            if (" " + nm + " ") in tblob:
                anchors.append((nmo, geom))
    if not hits:
        return [], []
    hits.sort(key=lambda h: h[0])
    r = P['cluster_km']*1000
    if not anchors:
        cnt = [(sum(h2[1].distance(h[1]) <= r for h2 in hits), -i) for i, h in enumerate(hits)]
        anchors = [hits[-max(cnt)[1]]]
    au = unary_union([a[1] for a in anchors])
    keep = [h for h in hits if h[1].distance(au) <= r]
    return keep, [a[0] for a in anchors]


def _sample_lines(arrs, step):
    out = []
    for a in arrs:
        ls = LineString(a); L = ls.length
        if L <= 0:
            continue
        n = max(2, int(L/step)+1)
        out.append(np.array([ls.interpolate(d).coords[0] for d in np.linspace(0, L, n)]))
    return np.vstack(out)


def _osm(bounds):
    bb = gpd.GeoSeries([box(*bounds)], crs=3400).to_crs(4326).total_bounds
    g = gpd.read_file(ROOT + "data/osm/alberta_osm_highways.gpkg", bbox=tuple(bb)).to_crs(3400)
    return list(g.geometry.explode(index_parts=False))


def _apply(Q, s, th, t, c):
    cs, sn = np.cos(th), np.sin(th)
    dx = Q[:, 0]-c[0]; dy = -(Q[:, 1]-c[1])
    return np.c_[s*(cs*dx-sn*dy)+t[0], s*(sn*dx+cs*dy)+t[1]]


def _coarse(ppts, osm_pts, wb, s_list, th_list, c, res, sigma, zscore=False):
    x0, y0, x1, y1 = wb
    nx = int((x1-x0)/res)+1; ny = int((y1-y0)/res)+1
    R = np.zeros((ny, nx), bool)
    ix = ((osm_pts[:, 0]-x0)/res).astype(int); iy = ((osm_pts[:, 1]-y0)/res).astype(int)
    m = (ix >= 0) & (ix < nx) & (iy >= 0) & (iy < ny); R[iy[m], ix[m]] = True
    F = np.exp(-distance_transform_edt(~R)*res/sigma).astype(np.float32)
    best = []
    for s in s_list:
        for th in th_list:
            cs, sn = np.cos(th), np.sin(th)
            dx = ppts[:, 0]-c[0]; dy = -(ppts[:, 1]-c[1])
            qx = s*(cs*dx-sn*dy); qy = s*(sn*dx+cs*dy)
            ax = np.floor(qx/res).astype(int); ay = np.floor(qy/res).astype(int)
            ox, oy = ax.min(), ay.min(); ax -= ox; ay -= oy
            T = np.zeros((ay.max()+1, ax.max()+1), np.float32); np.add.at(T, (ay, ax), 1)
            if T.shape[0] >= F.shape[0] or T.shape[1] >= F.shape[1]:
                continue
            C = fftconvolve(F, T[::-1, ::-1], mode='valid')/len(ppts)
            j = np.unravel_index(np.argmax(C), C.shape)
            z = float((C[j]-C.mean())/(C.std()+1e-9)) if zscore else float(C[j])
            best.append((z, s, th, x0+j[1]*res-ox*res, y0+j[0]*res-oy*res))
    best.sort(reverse=True)
    return best


def _icp(ppts, osm_pts, p0, c, s0):
    kd = cKDTree(osm_pts); p = np.array(p0, float)
    for rad in P['icp_radii']:
        for _ in range(P['icp_iters']):
            G = _apply(ppts, p[0], p[1], p[2:], c)
            keep = kd.query(G)[0] < rad
            if keep.sum() < 20:
                break
            sub = ppts[keep]
            keepr = cKDTree(G).query(osm_pts)[0] < rad
            subr = osm_pts[keepr]
            fs = P['icp_fscale']

            def res(q):
                out = [kd.query(_apply(sub, q[0], q[1], q[2:], c))[0]]
                if keepr.sum() > 20:
                    out.append(cKDTree(_apply(ppts, q[0], q[1], q[2:], c)).query(subr)[0])
                out.append([(q[0]/s0-1)/P['icp_sprior']*fs])
                out.append([(q[1]-p0[1])/np.radians(0.5)*fs])
                return np.concatenate(out)
            p = least_squares(res, p, loss='soft_l1', f_scale=fs, x_scale=[0.1, 0.001, 10, 10]).x
    return p


def _stated_area(n):
    """Diagnostic only (agreement check). NOT used as a prior by default."""
    global _stated
    if _stated is None:
        _stated = pd.read_csv(STATED).set_index('ed_number')
    return float(_stated.loc[n, 'area_km2'])


def _cap_res(wb, res):
    """Coarsen resolution until the grid has <= P['max_cells'] cells."""
    w, h = wb[2]-wb[0], wb[3]-wb[1]
    return max(res, float(np.ceil(np.sqrt(w*h/P['max_cells']))))


def georeference(n, window=None):
    outline, roads, txt, title = extract_page(n)
    poly = _evenodd_polygon(outline)
    c = np.array(poly.centroid.coords[0])
    ppts = _sample_lines(roads, P['page_step_pt'])
    hits, anchors = _window(txt, title)
    info = dict(ed=n, title=title, n_roadpts=len(ppts), anchors=anchors, csd_hits=[h[0] for h in hits][:10])
    if hits:
        wb = unary_union([h[1] for h in hits]).envelope.buffer(P['window_buf']).bounds
    elif window is not None:
        wb = tuple(window); info['window_given'] = True
    else:
        raise RuntimeError("no CSD name found on the page; pass reconstruct(ed, window=(x0,y0,x1,y1)) in EPSG:3400 "
                           "(whole-province search is deliberately not attempted: memory/time)")
    res = _cap_res(wb, P['wide_res'])
    osm_pts = _sample_lines([np.array(g.coords) for g in _osm(wb)], P['osm_step_m'])
    kd = cKDTree(osm_pts)
    # stage 1: prior-free wide search (log-spaced scales), z-scored correlation
    s_wide = np.exp(np.arange(np.log(P['s_min']), np.log(P['s_max']), P['s_step']))
    wide = _coarse(ppts, osm_pts, wb, s_wide, np.radians(P['angles_deg']), c, res, max(P['wide_sigma'], 1.5*res), zscore=True)
    cands = []; used = []
    for z, s, th, tx, ty in wide:
        if len(used) >= P['n_cand']:
            break
        if any(abs(th-u[1]) < 1e-6 and abs(np.log(s/u[0])) < 1.5*P['s_step'] and np.hypot(tx-u[2], ty-u[3]) < 1500 for u in used):
            continue
        used.append((s, th, tx, ty))
        # stage 2: local fine search around the wide candidate, then ICP
        foot = _apply(ppts, s, th, (tx, ty), c)
        fb = (foot[:, 0].min()-2000, foot[:, 1].min()-2000, foot[:, 0].max()+2000, foot[:, 1].max()+2000)
        sl = s*np.linspace(1-P['scale_span'], 1+P['scale_span'], P['scale_n'])
        fine = _coarse(ppts, osm_pts, fb, sl, [th], c, _cap_res(fb, P['coarse_res']), P['coarse_sigma'])
        if not fine:
            continue
        sc, s2, th2, tx2, ty2 = fine[0]
        p = _icp(ppts, osm_pts, [s2, th2, tx2, ty2], c, s2)
        inl = float((kd.query(_apply(ppts, p[0], p[1], p[2:], c))[0] < 30).mean())
        cands.append((inl, p, z))
    if not cands:
        raise RuntimeError("georeferencing failed: no candidate transform")
    cands.sort(key=lambda a: -a[0])
    inl, p, z = cands[0]
    s_area = float(np.sqrt(_stated_area(n)*1e6/poly.area))
    info.update(wide_z=z, inlier30=inl, s=float(p[0]), s_area=s_area, theta_deg=float(np.degrees(p[1])), tx=float(p[2]), ty=float(p[3]),
                runner_up_inlier30=(cands[1][0] if len(cands) > 1 else None))
    return poly, p, c, info


def reconstruct(ed_number, window=None):
    """Reconstruct ED boundary as shapely geometry in EPSG:3400."""
    global last_info
    n = int(ed_number); _guard(n)
    poly, p, c, info = georeference(n, window)

    def tf(g):
        ext = _apply(np.array(g.exterior.coords), p[0], p[1], p[2:], c)
        holes = [_apply(np.array(h.coords), p[0], p[1], p[2:], c) for h in g.interiors]
        return Polygon(ext, holes)
    geoms = [poly] if poly.geom_type == 'Polygon' else list(poly.geoms)
    out = unary_union([tf(g).buffer(0) for g in geoms])
    last_info = info
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ed", type=int, nargs="+"); ap.add_argument("--out")
    a = ap.parse_args(); rows = []
    for n in a.ed:
        g = reconstruct(n)
        print(n, g.geom_type, round(g.area/1e6, 2), "km2",
              {k: (round(v, 3) if isinstance(v, float) else v) for k, v in last_info.items()}, flush=True)
        rows.append(dict(ed_number=n, geometry=g))
    if a.out:
        gpd.GeoDataFrame(rows, crs=3400).to_file(a.out, driver="GPKG")
