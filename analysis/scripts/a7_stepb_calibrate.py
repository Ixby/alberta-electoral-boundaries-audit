# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a7_stepb_calibrate.py
---------------------

Amendment 7, Part 3, Step B: the single calibration run on the fixed sample.

Reconstructs each of the 34 sample districts (findings/a7_stepb_sample.json)
from its own Appendix 8 page with analysis/scripts/a7_stepb_reconstruct.py,
unchanged from the tuning set, and compares them with the commission
majority's official geometry. Rules fixed before the run (also in
findings/a7_stepb_calibration_protocol.md):

  VAs        the canonical VA polygons (mcmc_ensemble.build_va_graph), placed
             by representative point.
  T1 gate    a sample VA is one whose point lies in a sample district's
             official geometry. It is correct when the point lies in that
             district's reconstruction and in no other sample reconstruction.
             A district whose page cannot be placed (the procedure raises)
             counts all its VAs as wrong. Pass: at most 10% wrong.
  T4 gate    the commission majority map with each sample district replaced by
             its reconstruction: other districts lose any area a
             reconstruction covers; where reconstructions overlap, the lower
             ED number keeps the overlap; a district that could not be placed
             is left out (its VAs fall in no district). The efficiency gap of
             that map (mcmc_ensemble.score_exogenous_map, 2023 election-day
             votes) is compared with the official map's. Pass: |delta| < 0.5
             points.
  Reported   T2 mean |area error|, T3 mean Hausdorff distance, mean IoU, and
             the procedure's own diagnostics (inlier30, wide_z) per district.
             Nothing is tuned or hand-corrected after the run; any later change
             is disclosed with a rerun.

Usage: python analysis/scripts/a7_stepb_calibrate.py --out findings/a7_stepb_calibration.json
"""
import argparse
import json
import os
import sys
import tempfile
import time
import traceback
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.ops import unary_union

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import mcmc_ensemble as me  # noqa: E402

MAJ = REPO / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"
SAMPLE = REPO / "findings/a7_stepb_sample.json"
APP7 = REPO / "data/iap/iap_app7_populations.csv"
T1_MAX, T4_MAX = 0.10, 0.005


def norm(s):
    return s.replace("’", "'").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.environ["STEPB_ALLOW_ANY"] = "1"  # the post-tuning run, on the fixed sample only
    import a7_stepb_reconstruct as R

    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    eds = sorted(int(x) for x in (sample["sample"] if "sample" in sample else sample["sample_eds"]))
    assert len(eds) == 34, eds
    app7 = pd.read_csv(APP7).set_index("ed_number")
    maj = gpd.read_file(MAJ).to_crs(3400)
    maj["key"] = maj.EDName2025.map(norm)
    name = {n: norm(app7.loc[n, "district"]) for n in eds}
    assert all(v in set(maj.key) for v in name.values()), name

    va, _ = me.build_va_graph(verbose=False)
    pts = gpd.GeoSeries(va.to_crs(3400).geometry.representative_point(), index=va.index, crs=3400)

    rec, rows = {}, []
    for n in eds:
        t0 = time.time()
        row = {"ed": n, "district": name[n]}
        try:
            rec[n] = R.reconstruct(n)
            row.update({k: v for k, v in R.last_info.items()
                        if k in ("s", "s_area", "theta_deg", "inlier30", "runner_up_inlier30", "wide_z", "anchors")})
        except Exception as e:  # counted as a failure, never retried by hand
            row["error"] = repr(e)
            row["trace"] = traceback.format_exc()[-800:]
        row["sec"] = round(time.time() - t0, 1)
        rows.append(row)
        print(n, name[n], row.get("error", f"inlier30={row.get('inlier30', 0):.3f}"), flush=True)

    truth = {n: maj.loc[maj.key == name[n], "geometry"].union_all() for n in eds}
    # T1
    wrong = total = 0
    rec_tree = {n: g for n, g in rec.items()}
    for row in rows:
        n = row["ed"]
        inside = pts[pts.within(truth[n])]
        nt = len(inside)
        if n in rec_tree:
            own = inside.within(rec_tree[n]).to_numpy()
            other = np.zeros(nt, bool)
            for m, g in rec_tree.items():
                if m != n:
                    other |= inside.within(g).to_numpy()
            bad = int((~own | other).sum())
            tr, rc = truth[n], rec_tree[n]
            row.update(iou=tr.intersection(rc).area / tr.union(rc).area,
                       area_err_pct=100 * (rc.area - tr.area) / tr.area,
                       hausdorff_km=tr.hausdorff_distance(rc) / 1000)
        else:
            bad = nt
        row.update(va_true=nt, va_wrong=bad)
        wrong += bad
        total += nt
    t1 = wrong / total

    # T4
    keep = maj[~maj.key.isin(set(name.values()))].copy()
    cover = unary_union(list(rec.values())) if rec else None
    if cover is not None:
        keep["geometry"] = keep.geometry.difference(cover)
    taken, new = None, []
    for n in sorted(rec):
        g = rec[n] if taken is None else rec[n].difference(taken)
        taken = g if taken is None else taken.union(g)
        new.append({"EDName2025": name[n], "geometry": g})
    comp = pd.concat([keep[["EDName2025", "geometry"]], gpd.GeoDataFrame(new, crs=3400)], ignore_index=True)
    comp = gpd.GeoDataFrame(comp, crs=3400)
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "composite.gpkg"
        comp.to_file(f, driver="GPKG")
        eg_comp = me.score_exogenous_map(va, f)
    eg_off = me.score_exogenous_map(va, MAJ)
    d4 = eg_comp["efficiency_gap"] - eg_off["efficiency_gap"]

    ok = [r for r in rows if "iou" in r]
    res = {
        "procedure": "analysis/scripts/a7_stepb_reconstruct.py", "sample": eds,
        "placed": len(ok), "failed": [r["ed"] for r in rows if "error" in r],
        "T1": {"wrong": wrong, "total": total, "share": t1, "max": T1_MAX, "pass": t1 <= T1_MAX},
        "T4": {"eg_official": eg_off["efficiency_gap"], "eg_with_reconstructions": eg_comp["efficiency_gap"],
               "delta_points": 100 * d4, "max_points": 100 * T4_MAX, "pass": abs(d4) < T4_MAX,
               "coverage_vas_official": eg_off["coverage_vas"], "coverage_vas_composite": eg_comp["coverage_vas"]},
        "T2_mean_abs_area_err_pct": float(np.mean([abs(r["area_err_pct"]) for r in ok])) if ok else None,
        "T3_mean_hausdorff_km": float(np.mean([r["hausdorff_km"] for r in ok])) if ok else None,
        "mean_iou": float(np.mean([r["iou"] for r in ok])) if ok else None,
        "districts": rows,
    }
    res["calibration_passes"] = bool(res["T1"]["pass"] and res["T4"]["pass"])
    Path(a.out).write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "districts"}, indent=1, default=float))


if __name__ == "__main__":
    main()
