# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""Locator-inset georeferencing for the Elections Alberta district pages (Amendment 10).

Every district page carries a small locator map with all districts drawn and the page's own district filled
red. Pages 1-28 (Calgary) and 29-49 (Edmonton) carry a city inset; pages 50-91 carry a provincial one.
This script reads the inset, fits it to the official outline (similarity transform), and carries the page's
red district to ground (EPSG:3400) as a coarse, independent location for that district.

Usage (venv python only):
  python -W ignore a10_inset.py extract            # survey of every page's inset (json)
  python -W ignore a10_inset.py fit  OUT_DIR       # all pages -> OUT_DIR/inset_districts.gpkg + inset_fit.json
  python -W ignore a10_inset.py check --inset inset_districts.gpkg --districts DISTRICTS.gpkg --out crosscheck.json
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("STEPB_V3_CALIBRATION_RUN", "1")  # only page drawings are read; no sample leakage
sys.path.insert(0, str(Path(__file__).resolve().parent))
import a9_stepb_reconstruct_v3 as V3  # noqa: E402
import a7_stepb_calibrate as C  # noqa: E402
from scipy.spatial import cKDTree  # noqa: E402
from shapely.geometry import LinearRing, Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

GREY = 0.31      # inset district stroke colour (all three channels)
GREY_W = 1.38    # inset district stroke width
PROV_PAGES = range(50, 92)   # provincial inset; 1-28 Calgary, 29-49 Edmonton (checked in the survey)
SAMPLE_M = 2000.0           # spacing of outline sample points on the ground (m)
RED_MARGIN = 45.0           # the own district is drawn red instead of grey, so it may lie outside the grey set's box (pt)
CHECK_OFFSET_KM = 3.0       # an assembled district must have its centroid within this of its inset shape ...
CHECK_WIDTH_FRAC = 0.5      # ... and within this share of the inset's width, whichever is smaller
CHECK_IOU = 0.45            # IoU floor, applied only to districts at least SMALL_KM across
SMALL_KM = 5.0              # below this width the inset's resolution makes IoU unreliable: reported, not tested
TRIM = 0.95                 # share of inset boundary points used in the refinement (robust to outliers)


def _rings(items):
    """Split a drawing's items into closed rings (sub-paths start where an item does not continue the last)."""
    rings, cur = [], []
    for it in items:
        if it[0] == 'l':
            seg = [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] == 'c':
            p0, p1, p2, p3 = [np.array((q.x, q.y)) for q in it[1:5]]
            t = np.linspace(0, 1, 9)[:, None]
            seg = list(map(tuple, (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3))
        elif it[0] == 're':
            r = it[1]; seg = [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x0, r.y0)]
        else:
            continue
        if cur and np.hypot(cur[-1][0] - seg[0][0], cur[-1][1] - seg[0][1]) > 0.05:
            rings.append(cur); cur = []
        cur += seg if not cur else seg[1:]
    if cur:
        rings.append(cur)
    return [r for r in rings if len(r) >= 4]


def _poly(items, union=False):
    """Polygon from a drawing's items: even-odd, or (union=True) every ring filled. The red district is drawn as
    a band (outer ring plus an inner white ring), so it needs the union; even-odd would keep only the band."""
    g = None
    for r in _rings(items):
        q = Polygon(r).buffer(0)
        g = q if g is None else (g.union(q) if union else g.symmetric_difference(q))
    return g


def _is_grey(x):
    c = x.get('color')
    return bool(c) and all(abs(v - GREY) < 0.01 for v in c) and abs((x.get('width') or 0) - GREY_W) < 0.02


def _is_red(c):
    return bool(c) and c[0] > c[1] + 0.2 and c[0] > c[2] + 0.2


def extract(n):
    """The page's inset: district polygons (page points, y down), the red polygon, and bookkeeping."""
    d = V3._page(n).get_drawings()
    # as in V3.georeference: the main-map outline is the last reddish stroke of width >= 2; the inset follows it
    last = max(i for i, x in enumerate(d) if x['type'] in ('s', 'fs') and x.get('color') and (x.get('width') or 0) >= 2
               and _is_red(x['color']))
    gi = [i for i, x in enumerate(d) if i > last and x['type'] in ('fs', 's') and _is_grey(x) and len(x['items']) > 3]
    if not gi:
        return None
    # the inset is the last contiguous-ish run of grey items before the red fill; items of the main map's
    # grey boundary use other widths, so the run is already specific, but guard against stray earlier hits
    first, lastg = gi[0], gi[-1]
    polys = [_poly(d[i]['items']) for i in gi]
    keep, seen = [], set()
    for i, p in zip(gi, polys):
        if p is None or p.is_empty:
            continue
        key = tuple(np.round(p.bounds, 1)) + (round(p.area, 0),)   # some pages stroke a polygon twice
        if key not in seen:
            seen.add(key); keep.append((i, p))
    u = unary_union([p for _, p in keep])
    x0, y0, x1, y1 = u.bounds
    red = [i for i in range(lastg + 1, min(len(d), lastg + 60))
           if d[i]['type'] in ('fs', 'f') and _is_red(d[i].get('fill'))
           and x0 - RED_MARGIN <= d[i]['rect'].x0 and d[i]['rect'].x1 <= x1 + RED_MARGIN
           and y0 - RED_MARGIN <= d[i]['rect'].y0 and d[i]['rect'].y1 <= y1 + RED_MARGIN]
    rg = unary_union([_poly(d[i]['items'], union=True) for i in red]) if red else None
    return dict(n=n, polys=[p for _, p in keep], red=rg, idx=(first, lastg), red_idx=red, bounds=(x0, y0, x1, y1))


def _R(th):
    return np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])


def _boundary_pts(geom, step):
    out = []
    g = geom if geom.geom_type == 'MultiPolygon' else [geom]
    for q in (g.geoms if hasattr(g, 'geoms') else g):
        for ring in [q.exterior]:
            L = ring.length
            out.append(np.array([ring.interpolate(t).coords[0] for t in np.arange(0, L, step)]))
    return np.vstack(out)


def _outer(polys):
    """Outer boundary of the union of the inset polygons (slightly buffered so shared edges fuse)."""
    u = unary_union([p.buffer(0.15) for p in polys]).buffer(-0.15)
    return u


def fit(src_poly, target_poly, trim=TRIM):
    """Similarity (s, theta, t) with ground = s * R(theta) @ (x, -y) + t, mapping the inset's outer boundary
    onto the target outline. Tries the four right-angle rotations, then trimmed ICP on s, theta, t."""
    S = _boundary_pts(src_poly, 0.5) * [1, -1]
    T = _boundary_pts(target_poly, SAMPLE_M)
    tree = cKDTree(T)
    best = None
    tb = target_poly.bounds; sb = (S.min(0), S.max(0))
    for k in range(4):
        th = k * np.pi / 2
        Sr = S @ _R(th).T
        ext = Sr.max(0) - Sr.min(0)
        s = float(np.mean([(tb[2] - tb[0]) / ext[0], (tb[3] - tb[1]) / ext[1]]))
        t = np.array([(tb[0] + tb[2]) / 2, (tb[1] + tb[3]) / 2]) - s * (Sr.max(0) + Sr.min(0)) / 2
        for _ in range(60):
            Q = s * (S @ _R(th).T) + t
            dist, j = tree.query(Q)
            cut = np.quantile(dist, trim); m = dist <= cut
            P, R_ = S[m], T[j[m]]
            # least-squares similarity (Umeyama, 2-D)
            mp, mr = P.mean(0), R_.mean(0)
            A = (P - mp).T @ (R_ - mr)
            a = A[0, 0] + A[1, 1]; b = A[0, 1] - A[1, 0]   # sum of p.r and p x r
            th = float(np.arctan2(b, a))
            s = float(np.hypot(a, b) / ((P - mp) ** 2).sum())
            t = mr - s * (_R(th) @ mp)
        Q = s * (S @ _R(th).T) + t
        dist, _ = tree.query(Q)
        med = float(np.median(dist))
        if best is None or med < best['med_m']:
            best = dict(s=s, th=th, t=t, med_m=med, mean_m=float(dist.mean()), p90_m=float(np.quantile(dist, .9)),
                        max_m=float(dist.max()), k=k)
    return best


def to_ground(geom, f):
    """Apply a fit to a page-coordinate shapely geometry."""
    from shapely import affinity
    c, sn = np.cos(f['th']), np.sin(f['th']); s = f['s']
    # R(th) @ (x, -y) = (c x + sn y, sn x - c y), scaled by s and shifted by t
    return affinity.affine_transform(geom, [s * c, s * sn, s * sn, -s * c, f['t'][0], f['t'][1]])


def survey():
    out = {}
    for n in range(1, 92):
        e = extract(n)
        if e is None:
            out[n] = None; continue
        x0, y0, x1, y1 = e['bounds']
        out[n] = dict(n_polys=len(e['polys']), bbox=[x0, y0, x1, y1], has_red=e['red'] is not None,
                      red_area=float(e['red'].area) if e['red'] is not None else None)
    return out


def _target(kind):
    """Official outline (EPSG:3400): the province, or the Calgary / Edmonton districts of the majority map."""
    import geopandas as gpd
    m = gpd.read_file(C.MAJ)
    nm = m.EDName2025.map(C.norm)
    if kind == 'prov':
        sel = m
    else:
        sel = m[nm.str.startswith(kind + '-')]
    u = unary_union(list(sel.geometry))
    return u.buffer(200).buffer(-200)   # fuse slivers between districts


def _pages(kind):
    return {'prov': range(50, 92), 'Calgary': range(1, 29), 'Edmonton': range(29, 50)}[kind]


def run(out_dir):
    import geopandas as gpd
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    rows, stats = [], {}
    for kind in ('prov', 'Calgary', 'Edmonton'):
        tgt = _target(kind)
        for n in _pages(kind):
            e = extract(n)
            if e is None:
                stats[n] = dict(kind=kind, error='no inset'); continue
            allp = e['polys'] + ([e['red']] if e['red'] is not None else [])
            u = unary_union([p.buffer(0.15) for p in allp]).buffer(-0.15)
            f = fit(u, tgt)
            st = dict(kind=kind, n_polys=len(e['polys']), has_red=e['red'] is not None, rot_deg=float(np.degrees(f['th'])),
                      km_per_pt=f['s'] / 1000, med_km=f['med_m'] / 1000, p90_km=f['p90_m'] / 1000, max_km=f['max_m'] / 1000,
                      bbox=list(e['bounds']))
            stats[n] = st
            if e['red'] is not None:
                g = to_ground(e['red'], f)
                rows.append(dict(ed=n, geometry=g))
            print(n, kind, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in st.items() if k != 'bbox'}, flush=True)
    gdf = gpd.GeoDataFrame(rows, crs=3400)
    gdf.to_file(out / 'inset_districts.gpkg', driver='GPKG')
    with open(out / 'inset_fit.json', 'w', encoding='utf-8', newline='') as fh:
        json.dump({str(k): v for k, v in stats.items()}, fh, indent=1)
    return gdf, stats


def check(inset_path, districts_path, out_path):
    """Per district: does the assembled shape coincide with the inset's red polygon (see the constants above)?
    A page whose red polygon matches another district better than its own is an inset source error: reported,
    not counted as a failure."""
    import geopandas as gpd
    ins = gpd.read_file(inset_path).set_index('ed').geometry
    dis = gpd.read_file(districts_path).set_index('ed').geometry.buffer(0)
    rows = {}
    for ed, g in ins.items():
        g = g.buffer(0); b = g.bounds; w = max(b[2] - b[0], b[3] - b[1]) / 1000
        r = dict(ed=int(ed), inset_width_km=w, offset_km=None, iou=None, status='fail', inset_source_error=False)
        if ed not in dis.index or dis[ed].is_empty:
            r['status'] = 'fail_missing'; rows[int(ed)] = r; continue
        a = dis[ed]
        iou = lambda x: x.intersection(g).area / x.union(g).area if x.union(g).area else 0.0
        r['offset_km'] = a.centroid.distance(g.centroid) / 1000; r['iou'] = iou(a)
        best = max(dis.index, key=lambda k: iou(dis[k]))
        if best != ed and iou(dis[best]) > r['iou']:
            r['inset_source_error'] = True; r['better_match_ed'] = int(best); r['status'] = 'inset_source_error'
        else:
            ok = r['offset_km'] <= min(CHECK_OFFSET_KM, CHECK_WIDTH_FRAC * w) and (w < SMALL_KM or r['iou'] >= CHECK_IOU)
            r['status'] = 'pass' if ok else 'fail'
        rows[int(ed)] = r
    n = lambda st: sum(v['status'] == st for v in rows.values())
    res = dict(rule=dict(offset_km=CHECK_OFFSET_KM, width_frac=CHECK_WIDTH_FRAC, iou=CHECK_IOU, small_km=SMALL_KM),
               n_pass=n('pass'), n_fail=n('fail') + n('fail_missing'), n_source_error=n('inset_source_error'),
               failed=[k for k, v in rows.items() if v['status'].startswith('fail')], districts={str(k): v for k, v in rows.items()})
    with open(out_path, 'w', encoding='utf-8', newline='') as fh:
        json.dump(res, fh, indent=1)
    return res


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'extract':
        print(json.dumps(survey(), indent=1))
    elif mode == 'fit':
        run(sys.argv[2])
    elif mode == 'check':
        import argparse
        ap = argparse.ArgumentParser(); ap.add_argument('mode')
        ap.add_argument('--inset', required=True); ap.add_argument('--districts', required=True); ap.add_argument('--out', required=True)
        a = ap.parse_args()
        r = check(a.inset, a.districts, a.out)
        print({k: r[k] for k in ('n_pass', 'n_fail', 'n_source_error', 'failed')})
