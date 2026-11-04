# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
description_overlay.py
----------------------

Amendment 10, follow-up to description_check.py: for each failing description stretch, say whether the
assembled map is off, the matched feature is not the one named, or the clause is loose.

For each ED given: the final district boundary is drawn back onto its own PDF page through the page's stored
transform (inverse of V1._apply: s, theta, t, c in edNN.json diagnostics), together with the page's own red
outline (the page polygon edNN.gpkg, which is that outline carried to ground by the same transform) and the features
description_check matched. Reports the distance between the red outline and the drawn-back final boundary (page
points converted to metres by the transform scale; densified every 25 m, both directions) and, per stretch of
description_check.D that fails (share within tolerance under 90%):
  d_final_red       final boundary sample -> red outline          (large = the assembled map departs from the page)
  d_red_feature     that red-outline point -> the matched feature  (large = the red outline itself departs from it)
  d_final_feature   final boundary sample -> the matched feature   (what description_check reported)
Rule: median d_final_red > 100 m -> 'map off'; else median d_red_feature > 200 m (5 km for a proximity clause) ->
'loose clause or wrong feature' (the picture decides which); else 'ok on this page'.
No partisan measure. Writes description_overlays/edNN.png and summary.json. Usage:
  python findings/a10_dev/description_overlay.py --snap C:/tmp/a10test/snap_fixed 49 85 62 46 48
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib
import numpy as np
import shapely

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))
import a9_stepb_reconstruct_v3 as V3  # noqa: E402

spec = importlib.util.spec_from_file_location("dc", HERE / "description_check.py")
dc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dc)
DPI = 150
FIX = Path("C:/tmp/a10test/fixture")


def to_page(xy, p, c):
    s, th, tx, ty = p
    cs, sn = np.cos(th), np.sin(th)
    X, Y = xy[:, 0] - tx, xy[:, 1] - ty
    return np.c_[(cs * X + sn * Y) / s + c[0], c[1] - (-sn * X + cs * Y) / s]


def lines_of(g):
    polys = [q for q in shapely.get_parts(g) if q.geom_type == "Polygon"]   # a final geometry can be a GeometryCollection
    return [ln for q in polys for ln in dc.parts(shapely.boundary(q))]


def densify(lines, step=25.0):
    out = []
    for ln in lines:
        n = max(2, int(ln.length / step) + 1)
        out.append(shapely.get_coordinates(shapely.line_interpolate_point(ln, np.linspace(0, ln.length, n))))
    return np.vstack(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snap", default="C:/tmp/a10test/snap_fixed")
    ap.add_argument("--out", default=str(HERE / "description_overlays"))
    ap.add_argument("eds", nargs="+", type=int)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(exist_ok=True)
    dist = gpd.read_file(Path(a.snap) / "districts.gpkg").to_crs(3400).set_index("ed")
    csd = gpd.read_file(dc.CSD).to_crs(3400)
    csd_line = {n: dc.parts(shapely.boundary(shapely.union_all(list(csd[csd.CSDNAME == n].geometry))))
                for n in ["Edmonton", "Lethbridge", "Sturgeon County", "Clearwater County"]}
    province = dc.parts(shapely.boundary(shapely.union_all(list(csd.geometry))))
    riv = gpd.read_file(dc.RIV).to_crs(3400)
    rg = np.asarray(riv.geometry.values, dtype=object)
    rt = shapely.STRtree(rg)
    summary = {}
    for ed in a.eds:
        j = json.loads((FIX / f"ed{ed:02d}.json").read_text(encoding="utf-8"))
        dg = j["diagnostics"]
        p, c = dg["p"], np.array(dg["c"])
        fin = dist.geometry.loc[ed]
        red = gpd.read_file(FIX / f"ed{ed:02d}.gpkg").to_crs(3400).union_all()
        s = p[0]
        fl, rl = lines_of(fin), lines_of(red)
        fpts, rpts = densify(fl), densify(rl)
        d_fr = dc.dist_to(rl, shapely.points(fpts))[0]
        d_rf = dc.dist_to(fl, shapely.points(rpts))[0]
        both = np.concatenate([d_fr, d_rf])
        rec = {"ed": ed, "name": dist.district.loc[ed], "source": dist.source.loc[ed], "page_polygon_status": j.get("polygon_status"),
               "page_error": j.get("error"), "transform_scale_m_per_pt": round(float(s), 3), "page_fit_median_m": round(dg.get("med_dist_m", float("nan")), 1),
               "page_fit_in60": round(dg.get("in60", float("nan")), 3),
               "final_to_red_median_m": round(float(np.median(d_fr)), 1), "final_to_red_p95_m": round(float(np.percentile(d_fr, 95)), 1),
               "red_to_final_median_m": round(float(np.median(d_rf)), 1), "red_to_final_p95_m": round(float(np.percentile(d_rf, 95)), 1),
               "symmetric_median_m": round(float(np.median(both)), 1), "symmetric_p95_m": round(float(np.percentile(both, 95)), 1),
               "red_outline_in_points": "red outline = page polygon edNN.gpkg (page points x scale = metres)", "stretches": []}
        # features
        b = fin.bounds
        bb = (b[0] - 15000, b[1] - 15000, b[2] + 15000, b[3] + 15000)
        nrn = gpd.read_file(dc.NRN, bbox=bb)
        nrn["RTNUMBER1"] = nrn.RTNUMBER1.astype(str)
        rv = [q for x in rg[rt.query(shapely.box(*bb))] for q in dc.parts(x)]

        def feat(kind, arg):
            if kind == "csd":
                return [q for n in arg for q in csd_line[n]]
            if kind == "route":
                return [q for x in nrn[nrn.RTNUMBER1.isin(arg)].geometry for q in dc.parts(x)]
            if kind == "expressway":
                ex = nrn[(nrn.ROADCLASS == "Expressway / Highway") & (nrn.RTNUMBER1 == "None")]
                return [q for x in ex.geometry if shapely.distance(x, fin) <= 2000 for q in dc.parts(x)]
            if kind == "arterial":
                return [q for x in nrn[nrn.ROADCLASS.isin(dc.ARTERIAL)].geometry for q in dc.parts(x)]
            if kind == "river":
                return rv
            return province

        P, B, R, S = dc.ring_samples(fin)
        px, py = shapely.get_x(P), shapely.get_y(P)
        feats_drawn = {}
        for st in dc.D[ed]["stretches"]:
            sel = np.abs((B - dc.BEARING[st["side"]] + 180) % 360 - 180) <= dc.SECTOR
            sel &= {"E": px >= b[2] - dc.OUTER * (b[2] - b[0]), "W": px <= b[0] + dc.OUTER * (b[2] - b[0]),
                    "N": py >= b[3] - dc.OUTER * (b[3] - b[1]), "S": py <= b[1] + dc.OUTER * (b[3] - b[1])}[st["side"]]
            lines = [q for k, ar in st["feature"] for q in feat(k, ar)]
            if not sel.any() or not lines:
                continue
            tol = st.get("tol", dc.TOL)
            d_ff, _ = dc.dist_to(lines, P[sel])
            d_fr_s, xy = dc.dist_to(rl, P[sel])           # nearest red-outline point to each final sample
            d_rf_s, _ = dc.dist_to(lines, shapely.points(xy))
            share = float((d_ff <= tol).mean())
            row = {"side": st["side"], "clause": st["id"], "text": st["text"], "feature": [f"{k}:{'/'.join(ar) if ar else '-'}" for k, ar in st["feature"]],
                   "tol_m": tol, "n": int(sel.sum()), "share_final_within_tol": round(share, 3),
                   "d_final_feature_median_m": round(float(np.median(d_ff)), 1), "d_final_red_median_m": round(float(np.median(d_fr_s)), 1),
                   "d_final_red_p95_m": round(float(np.percentile(d_fr_s, 95)), 1), "d_red_feature_median_m": round(float(np.median(d_rf_s)), 1),
                   "share_red_within_tol": round(float((d_rf_s <= tol).mean()), 3)}
            if share >= 0.9:
                row["verdict"] = "passes"
            elif row["d_final_red_median_m"] > 100:
                row["verdict"] = "map off: final boundary departs from the page's red outline"
            elif row["d_red_feature_median_m"] > tol:
                row["verdict"] = "red outline itself departs from the matched feature: loose clause or wrong feature (see picture)"
            else:
                row["verdict"] = "red outline is on the feature but the final boundary is not (small offsets); see numbers"
            rec["stretches"].append(row)
            for k, ar in st["feature"]:
                feats_drawn.setdefault(k, lines)
        # picture
        pg = V3._page(ed)
        pix = pg.get_pixmap(dpi=DPI)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3]
        k = DPI / 72
        fig, ax = plt.subplots(figsize=(7, 8.5), dpi=100)
        ax.imshow(img, alpha=0.6)
        ax.set_axis_off()

        def plot(lines, col, lw, lab):
            first = True
            for ln in lines:
                xy = shapely.get_coordinates(ln)
                if not len(xy):
                    continue
                q = to_page(xy, p, c) * k
                ax.plot(q[:, 0], q[:, 1], color=col, lw=lw, label=lab if first else None)
                first = False

        cols = {"river": "#00a000", "route": "#ff8c00", "expressway": "#ff8c00", "csd": "#c000c0", "province": "#a0a000", "arterial": "#808080"}
        allp = to_page(np.vstack([shapely.get_coordinates(x) for x in rl + fl]), p, c) * k
        lo, hi = allp.min(0), allp.max(0)
        pad = 0.06 * (hi - lo)
        ax.set_xlim(lo[0] - pad[0], hi[0] + pad[0])
        ax.set_ylim(hi[1] + pad[1], lo[1] - pad[1])
        for kind, lines in feats_drawn.items():
            clip = shapely.box(*(np.r_[lo - pad, hi + pad] / k))   # page points box; test in ground via transformed pts
            plot(lines, cols[kind], 0.7, f"matched feature: {kind}")
        plot(rl, "red", 1.4, "page red outline")
        plot(fl, "blue", 0.9, "assembled boundary")
        ax.set_title(f"ED {ed} {rec['name']} ({rec['source']}); page fit {rec['page_polygon_status']}, in60 {rec['page_fit_in60']}; "
                     f"final vs red median {rec['final_to_red_median_m']} m", fontsize=8)
        ax.legend(loc="lower right", fontsize=6)
        fig.savefig(out / f"ed{ed:02d}.png", bbox_inches="tight", dpi=100)
        plt.close(fig)
        summary[str(ed)] = rec
        print(ed, rec["name"], rec["page_polygon_status"], rec["final_to_red_median_m"], rec["final_to_red_p95_m"], flush=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
