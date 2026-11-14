# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""Version 4 of the page reconstruction: version 3 with the prior order municipal -> inset -> version 2 road search.

The inset prior is the page's red locator polygon carried to ground by a10_inset (fit to the official outline).
It is used only when the polygon's area is within INSET_AREA_TOL of the stated area (a page whose inset
highlights another district, such as page 53, fails this test and falls through to the road search). It
seeds translation (the polygon's centroid), with the scale from the stated area and rotation 0, and the
same 1,500 m error radius for the local refinement that v3 gives the v2 prior. Everything else (refinement,
acceptance rule, reconstruct) is version 3's, imported unchanged.

Usage (venv python only; long, so run detached through the runner):
  python -W ignore a10_stepb_reconstruct_v4.py OUT_DIR ED [ED ...]
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a10_inset as I  # noqa: E402  (sets STEPB_V3_CALIBRATION_RUN, imports V3)
import a9_stepb_reconstruct_v3 as V3  # noqa: E402

V1, R2 = V3.V1, V3.R2
INSET_AREA_TOL = {'prov': 0.10, 'city': 0.06}   # |inset area / stated area - 1| (provincial / city inset)
_orig_v2 = R2.georeference
last_info = {}
_inset_log = {}


def _kind(n):
    return 'Calgary' if n <= 28 else 'Edmonton' if n <= 49 else 'prov'


def inset_ground(n):
    """The page's red inset polygon on the ground (EPSG:3400) and its fit, or None."""
    e = I.extract(n)
    if e is None or e['red'] is None:
        return None
    kind = _kind(n)
    allp = e['polys'] + [e['red']]
    u = I.unary_union([p.buffer(0.15) for p in allp]).buffer(-0.15)
    f = I.fit(u, I._target(kind))
    return I.to_ground(e['red'], f), f, kind


def _georeference_v2_or_inset(n):
    """Stands in for R2.georeference inside V3.georeference (called only when the municipal prior fails)."""
    outline = R2.extract_page(n)[0]
    c = np.array(V1._evenodd_polygon(outline).centroid.coords[0])
    stated = V1._stated_area(n) * 1e6
    poly = V1._evenodd_polygon(outline); s0 = float(np.sqrt(stated / poly.area))
    try:
        r = inset_ground(n)
    except Exception as ex:   # an unreadable inset only removes this prior
        r = None; _inset_log[n] = dict(error=repr(ex))
    if r is not None:
        g, f, kind = r
        ratio = g.area / stated
        tol = INSET_AREA_TOL['prov' if kind == 'prov' else 'city']
        _inset_log[n] = dict(kind=kind, area_ratio=float(ratio), tol=tol, centroid=[g.centroid.x, g.centroid.y], used=abs(ratio - 1) <= tol)
        if abs(ratio - 1) <= tol:
            pv = [s0, 0.0, g.centroid.x, g.centroid.y]
            return None, pv, c, dict(inlier30=None, runner_up_inlier30=None, wide_z=None)
    return _orig_v2(n)


def reconstruct(ed_number):
    """V3.reconstruct with the inset prior in place; raises as V3 does, with last_info set either way."""
    global last_info
    n = int(ed_number); g = None
    R2.georeference = _georeference_v2_or_inset
    try:
        g = V3.reconstruct(n)
        return g
    finally:
        R2.georeference = _orig_v2
        last_info = dict(V3.last_info); _annotate(n, last_info, g)


def _annotate(n, info, g):
    il = _inset_log.get(n, {})
    if info.get('prior') == 'v2' and il.get('used'):
        info['prior'] = 'inset'
    info['inset'] = il
    if g is not None and il.get('centroid'):
        info['inset_centroid_offset_m'] = float(np.hypot(g.centroid.x - il['centroid'][0], g.centroid.y - il['centroid'][1]))


if __name__ == '__main__':
    import geopandas as gpd
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    maj = gpd.read_file(I.C.MAJ); maj['k'] = maj.EDName2025.map(I.C.norm)
    import pandas as pd
    app7 = pd.read_csv(I.C.APP7).set_index('ed_number')
    for n in map(int, sys.argv[2:]):
        t0 = time.time(); g = None; err = None
        R2.georeference = _georeference_v2_or_inset
        try:
            g = V3.reconstruct(n)
        except Exception as e:
            err = repr(e)
        finally:
            R2.georeference = _orig_v2
        info = dict(V3.last_info); _annotate(n, info, g)
        res = dict(ed=n, error=err, sec=time.time() - t0,
                   diagnostics={k: v for k, v in info.items() if k != 'layers'})
        if g is not None:
            gpd.GeoDataFrame({'ed': [n]}, geometry=[g], crs=3400).to_file(out / f'ed{n:02d}.gpkg', driver='GPKG')
            sel = maj[maj.k == I.C.norm(app7.district[n])]
            if len(sel):
                t = sel.geometry.union_all(); res['iou_vs_majority'] = float(g.intersection(t).area / g.union(t).area)
        with open(out / f'ed{n:02d}.json', 'w', encoding='utf-8', newline='') as fh:
            json.dump(res, fh, indent=1, default=str)
        print(n, res['error'], info.get('prior'), {k: info.get(k) for k in ('med_dist_m', 'in60', 'n_layer_pts', 'inset_centroid_offset_m')},
              res.get('iou_vs_majority'), round(res['sec']), flush=True)
