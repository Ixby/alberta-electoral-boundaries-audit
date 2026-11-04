# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a10_stepb_calibrate.py
----------------------

Amendment 10: the third calibration run. It scores the page-by-page reconstruction
(a10_reconstruct_pages.py) after the assembly rules of a10_assemble.py have turned the
reconstructions into a VA-to-district assignment, against the same fixed 34-district sample
and the same gates as the frozen scorer a7_stepb_calibrate.py (Amendment 7).

What is the same as a7_stepb_calibrate.py (constants and name normalisation are imported from it):
  sample      findings/a7_stepb_sample.json, 34 districts; the commission majority map is the truth.
  sample VAs  the canonical VA polygons (mcmc_ensemble.build_va_graph) whose representative point
              lies in a sample district's official geometry.
  T1 gate     share of sample VAs assigned wrongly <= T1_MAX.
  T4 gate     |EG(composite map) - EG(official map)| < T4_MAX, by mcmc_ensemble.score_exogenous_map
              on a temporary gpkg of the composite.

What differs, because the unit of reconstruction is now the assembled VA set:
  known       the 22 tuning districts keep their official geometry in the assembly.
  T1          a VA is wrong when the assembled label (va_district) differs from its truth district's
              name; an unassigned VA (None) counts as wrong. (a7: reconstruction polygon membership.)
  T4          each sample district's geometry is the union of the VAs assigned to it (a7: the raw
              reconstruction polygon). Other districts lose any area those unions cover, as in a7.
              A sample district with no VAs assigned is left out. The lower-ED-keeps-overlap step of
              a7 is not needed: a VA carries exactly one label, so the unions are disjoint.
  T2/T3/IoU   reported over districts with status "placed" (reconstruction survived the assembly
              rules); the same three over every polygon V3 produced, rejected ones included, are
              reported under reconstruction_quality_all_polygons so a rejection cannot hide a bad fit.

Per sample district the output records status (placed / rejected: reason / filled / failed: error),
the V3 diagnostics present in the page json, IoU / area error / Hausdorff distance when a polygon
exists, the VAs assigned, and va_true / va_wrong with the names the wrong VAs went to. A district
that was rejected and later hole-filled has status "filled" and keeps its rejection reason.

The population check of the assembly (pop_within_5pct) is informational: it is copied into each row
and gates nothing here.

Environment: Python 3.12.13 with PyMuPDF 2.1. The script exits non-zero at import under any other
Python or PyMuPDF version. --allow-any-env bypasses that for DEVELOPMENT ONLY; such a run records
environment.registered_environment = false and can never report calibration_passes = true.

Usage: C:/Users/email/.venvs/audit-k91/Scripts/python.exe -W ignore analysis/scripts/a10_stepb_calibrate.py --pages OUT_DIR --out findings/a10_stepb_calibration.json
"""
import argparse
import collections
import inspect
import json
import math
import platform
import sys
import tempfile
import time
from pathlib import Path

REGISTERED_PYTHON = (3, 12, 13)  # the environment the page reconstructions were registered under
REGISTERED_PYMUPDF = "2.1"
ALLOW_ANY_ENV = "--allow-any-env" in sys.argv  # DEVELOPMENT ONLY: bypasses the refusal below; the registered run never uses it


def _pymupdf_version():
    try:
        import pymupdf
        return pymupdf.__version__
    except Exception:  # not importable counts as the wrong environment
        return None


REGISTERED_ENVIRONMENT = bool(sys.version_info[:3] == REGISTERED_PYTHON and _pymupdf_version() == REGISTERED_PYMUPDF)
if not REGISTERED_ENVIRONMENT and not ALLOW_ANY_ENV:  # refuse at import, before any work: a wrong-environment result must not exist
    sys.exit(f"Python {platform.python_version()}, PyMuPDF {_pymupdf_version()}: the registered run needs "
             f"Python {'.'.join(map(str, REGISTERED_PYTHON))} with PyMuPDF {REGISTERED_PYMUPDF} "
             "(--allow-any-env bypasses this for development only)")

import geopandas as gpd  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import mcmc_ensemble as me  # noqa: E402
import a7_stepb_calibrate as C  # noqa: E402  (constants and norm only; its main() is never called)

MAJ, SAMPLE, APP7, norm = C.MAJ, C.SAMPLE, C.APP7, C.norm
T1_MAX = C.T1_MAX   # largest share of sample VAs assigned wrongly (same gate as Amendment 7)
T4_MAX = C.T4_MAX   # largest |EG(composite) - EG(official)| (0.5 points, same gate as Amendment 7)
N_SAMPLE = 34       # size of the fixed sample
V3_DIAGNOSTICS = ("s", "s_area", "theta_deg", "prior", "med_dist_m", "in60", "n_layer_pts")  # copied from the page json when present


# ----------------------------------------------------------------------------------------------
# official geometry and names
# ----------------------------------------------------------------------------------------------

def sample_eds():
    sample = json.loads(Path(SAMPLE).read_text(encoding="utf-8"))
    eds = sorted(int(x) for x in (sample["sample"] if "sample" in sample else sample["sample_eds"]))
    assert len(eds) == N_SAMPLE, eds
    return eds


def tuning_eds():
    import a9_stepb_reconstruct_v3 as V3  # constant only; no page is read and no guard is touched
    return sorted(int(x) for x in V3.TUNING)


def load_context():
    """app7 table, majority map (key = normalised name), sample ED numbers, their names and official geometry."""
    eds = sample_eds()
    app7 = pd.read_csv(APP7).set_index("ed_number")
    maj = gpd.read_file(MAJ).to_crs(3400)
    maj["key"] = maj.EDName2025.map(norm)
    name = {n: norm(app7.loc[n, "district"]) for n in eds}
    assert all(v in set(maj.key) for v in name.values()), name
    truth = {n: maj.loc[maj.key == name[n], "geometry"].union_all() for n in eds}
    return app7, maj, eds, name, truth


def tuning_known(app7, maj):
    """name -> official geometry for the 22 tuning districts (never in the sample)."""
    known = {}
    for n in tuning_eds():
        nm = norm(app7.loc[n, "district"])
        assert nm in set(maj.key), nm
        known[nm] = maj.loc[maj.key == nm, "geometry"].union_all()
    assert len(known) == 22, len(known)
    return known


# ----------------------------------------------------------------------------------------------
# T1
# ----------------------------------------------------------------------------------------------

def clean_labels(va_district, index):
    """Assembled labels as an object Series on the VA index: normalised name, or None."""
    lab = pd.Series(va_district).reindex(index).astype(object)
    return lab.map(lambda s: norm(s) if isinstance(s, str) else None)


def sample_vas(pts, truth):
    """ED -> index of the sample VAs: representative point inside the district's official geometry (a7 definition)."""
    return {n: pts.index[pts.within(g).to_numpy()] for n, g in truth.items()}


def score_t1(labels, inside, name):
    """Per sample district: how many of its sample VAs carry its own name, and where the rest went."""
    rows, wrong, total = {}, 0, 0
    for n, idx in inside.items():
        got = labels.reindex(idx)
        own = (got == name[n]).to_numpy()  # None / NaN compare False, so an unassigned VA is wrong
        dest = collections.Counter(s if isinstance(s, str) else "(unassigned)" for s in got[~own])
        rows[n] = {"va_true": int(len(idx)), "va_wrong": int((~own).sum()),
                   "va_wrong_assigned_to": dict(dest.most_common())}
        wrong += rows[n]["va_wrong"]
        total += rows[n]["va_true"]
    return rows, wrong, total


# ----------------------------------------------------------------------------------------------
# T4
# ----------------------------------------------------------------------------------------------

def composite_map(maj, va_geom, labels, eds, name):
    """The majority map with each sample district replaced by the union of the VAs assigned to it.

    Returns (GeoDataFrame[EDName2025, geometry], {sample name: VAs used}). Other districts lose any
    area the unions cover (a7); a sample district with no VAs is omitted.
    """
    keep = maj[~maj.key.isin(set(name.values()))].copy()
    new, used = [], {}
    for n in eds:
        m = (labels == name[n]).to_numpy()
        if m.any():
            new.append({"EDName2025": name[n], "geometry": va_geom[m].union_all()})
            used[name[n]] = int(m.sum())
    if new:
        cover = unary_union([r["geometry"] for r in new])
        hit = keep.geometry.intersects(cover).to_numpy()  # only these can change; the rest are untouched
        keep.loc[hit, "geometry"] = keep.geometry[hit].difference(cover)
        keep = keep[~keep.geometry.is_empty]
    parts = [keep[["EDName2025", "geometry"]]]
    if new:
        parts.append(gpd.GeoDataFrame(new, crs=3400))
    comp = gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs=3400)
    return comp, used


def score_composite(va, comp):
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "composite.gpkg"
        comp.to_file(f, driver="GPKG")
        return me.score_exogenous_map(va, f)


# ----------------------------------------------------------------------------------------------
# geometry quality, JSON, environment
# ----------------------------------------------------------------------------------------------

def geometry_quality(tr, rc):
    if not rc.is_valid:
        rc = rc.buffer(0)
    return {"iou": tr.intersection(rc).area / tr.union(rc).area,
            "area_err_pct": 100 * (rc.area - tr.area) / tr.area,
            "hausdorff_km": tr.hausdorff_distance(rc) / 1000}


def clean(o):
    """JSON-safe copy: numpy scalars to Python, NaN/inf to None, keys to str."""
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if o is pd.NA or o is pd.NaT:
        return None
    if isinstance(o, Path):
        return str(o)
    return o


def environment():
    env = {"python": platform.python_version(), "pymupdf": _pymupdf_version()}
    for mod in ("geopandas", "shapely", "numpy", "pandas"):
        env[mod] = __import__(mod).__version__
    env["registered_environment"] = REGISTERED_ENVIRONMENT
    env["allow_any_env"] = ALLOW_ANY_ENV  # True only for a development run, which is never the registered run
    return env


def gate_blocks(labels, inside, name, maj, va, va3400, eds, eg_off):
    """T1 and T4 for one assignment: (per-district T1 rows, T1 dict, T4 dict)."""
    t1rows, wrong, total = score_t1(labels, inside, name)
    t1 = wrong / total if total else 1.0
    comp, used = composite_map(maj, va3400.geometry, labels, eds, name)
    eg_comp = score_composite(va, comp)
    d4 = eg_comp["efficiency_gap"] - eg_off["efficiency_gap"]
    t1d = {"wrong": wrong, "total": total, "share": t1, "max": T1_MAX, "pass": bool(total and t1 <= T1_MAX)}
    t4d = {"eg_official": eg_off["efficiency_gap"], "eg_with_reconstructions": eg_comp["efficiency_gap"],
           "delta_points": 100 * d4, "max_points": 100 * T4_MAX, "pass": bool(abs(d4) < T4_MAX),
           "coverage_vas_official": eg_off["coverage_vas"], "coverage_vas_composite": eg_comp["coverage_vas"],
           "sample_districts_in_composite": len(used), "vas_used_per_sample_district": used}
    return t1rows, t1d, t4d


def final_labels(csv_path, va):
    """district name (or None) per VA row from a10_snap_assign's va_assignment.csv; rows are in VA-table order."""
    ids = pd.read_csv(csv_path, dtype={"OBJECTID": str, "VA_NUMBER": str})  # VA_NUMBER is zero-padded text
    if len(ids) != len(va):
        raise ValueError(f"{csv_path}: {len(ids)} rows for {len(va)} VAs")
    for c in ("OBJECTID", "VA_NUMBER"):
        if c in ids.columns and c in va.columns and not (ids[c].to_numpy() == va[c].astype(str).to_numpy()).all():
            raise ValueError(f"{csv_path}: column {c} does not match the VA table")
    lab = pd.Series(ids["district"].to_numpy(dtype=object), index=va.index)
    return clean_labels(lab, va.index)


def mean_or_none(xs):
    return float(np.mean(xs)) if xs else None


# ----------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", required=True, help="directory written by a10_reconstruct_pages.py")
    ap.add_argument("--out", required=True)
    ap.add_argument("--allow-any-env", action="store_true",
                    help="DEVELOPMENT ONLY: run outside Python 3.12.13 + PyMuPDF 2.1; the result is then not a registered run")
    a = ap.parse_args()
    pages_dir = Path(a.pages)
    if not pages_dir.is_dir():
        sys.exit(f"--pages {pages_dir} is not a directory")
    import a10_assemble as A  # imported here so the parts above can be tested before it exists

    t0 = time.time()
    app7, maj, eds, name, truth = load_context()
    known = tuning_known(app7, maj)

    va, graph = me.build_va_graph(verbose=False)
    va3400 = va.to_crs(3400)
    pts = gpd.GeoSeries(va3400.geometry.representative_point(), index=va.index, crs=3400)

    loaded = A.load_pages(pages_dir)  # (polys, pages) or (polys, pages, rejected_polys)
    polys, pages = loaded[0], loaded[1]
    rejected_polys = {int(k): g for k, g in loaded[2].items()} if len(loaded) > 2 else {}
    polys = {int(k): g for k, g in polys.items()}
    pages = {int(k): v for k, v in pages.items()}
    for k in [k for k in polys if (pages.get(k) or {}).get("polygon_status", "accepted") != "accepted"]:
        rejected_polys[k] = polys.pop(k)  # a rejected-status fit is never placed, whichever form load_pages returns
    kw = {"graph": graph} if "graph" in inspect.signature(A.assemble).parameters else {}  # same graph; saves a rebuild
    res = A.assemble(polys, pages, known, va3400, app7, **kw)
    labels = clean_labels(res.va_district, va.index)
    res.rejected = {int(k): v for k, v in res.rejected.items()}
    res.filled = {int(k): v for k, v in res.filled.items()}

    # before snapping: the assembly alone
    inside = sample_vas(pts, truth)
    eg_off = me.score_exogenous_map(va, MAJ)
    t1rows_b, t1_before, t4_before = gate_blocks(labels, inside, name, maj, va, va3400, eds, eg_off)

    # final assignment: assemble -> snap/assign (a10_snap_assign.py), the registered pipeline
    import a10_snap_assign as S
    snap_dir = Path(a.out).with_suffix("")
    snap_dir = snap_dir.with_name(snap_dir.name + "_snap")
    snap = S.run(pages_dir, "tuning", snap_dir)
    final = final_labels(snap_dir / "va_assignment.csv", va)
    t1rows, t1_final, t4_final = gate_blocks(final, inside, name, maj, va, va3400, eds, eg_off)
    wrong, total, t1 = t1_final["wrong"], t1_final["total"], t1_final["share"]
    snap_src = {r["ed"]: r for r in snap.get("districts", [])}

    # per-district rows
    dist_tab = res.districts.set_index("ed") if len(res.districts) else pd.DataFrame()
    rows = []
    for n in eds:
        pg = pages.get(n)
        err = pg.get("error") if pg else "no page json"
        diag = (pg or {}).get("diagnostics") or {}
        row = {"ed": n, "district": name[n]}
        if n in res.filled:
            row["status"] = "filled"
        elif n in res.rejected:
            row["status"] = f"rejected: {res.rejected[n]}"
        elif n in polys:
            row["status"] = "placed"
        else:
            row["status"] = f"failed: {err}"
        if n in res.rejected:
            row["reject_reason"] = res.rejected[n]
        row["filled"] = n in res.filled
        if n in res.filled:
            row["filled_n_vas"] = int(res.filled[n])
        row["anchors"] = (pg or {}).get("anchors")  # the page's own CSD names, used by the hole fill
        if err:
            row["error"] = err
        row.update({k: diag[k] for k in V3_DIAGNOSTICS if k in diag})
        if pg and "sec" in pg:
            row["sec"] = pg["sec"]
        row["polygon_status"] = (pg or {}).get("polygon_status")
        if n in polys or n in rejected_polys:
            try:
                row.update(geometry_quality(truth[n], polys.get(n, rejected_polys.get(n))))
            except Exception as e:  # reported, never retried by hand
                row["geometry_error"] = repr(e)
        if n in dist_tab.index:
            d = dist_tab.loc[n]
            within = d.get("pop_within_5pct", d.get("used"))  # informational only; no gate in this scorer reads it
            row.update(source=d["source"], n_vas_assigned=int(d["n_vas"]), pop_diff_pct=d.get("pop_diff_pct", d.get("diff_pct")),
                       pop_within_5pct=None if pd.isna(within) else bool(within))
        else:
            row["n_vas_assigned"] = 0
        row.update(t1rows[n])
        row["before_snap"] = {k: t1rows_b[n][k] for k in ("va_wrong", "va_wrong_assigned_to")}
        if n in snap_src:
            row["final_source"] = snap_src[n].get("source")
            row["final_n_vas"] = snap_src[n].get("n_vas")
            row["final_low_confidence"] = snap_src[n].get("low_confidence")
        rows.append(row)
        print(f"{n:>3} {name[n]:<28} {row['status']:<44} wrong {row['va_wrong']}/{row['va_true']}"
              + (f"  iou={row['iou']:.4f}" if "iou" in row else "")
              + (f"  -> {dict(list(row['va_wrong_assigned_to'].items())[:3])}" if row["va_wrong"] else ""),
              flush=True)

    placed = [r for r in rows if r["status"] == "placed" and "iou" in r]
    with_poly = [r for r in rows if "iou" in r]
    res_json = {
        "procedure": ("analysis/scripts/a10_reconstruct_pages.py (page reconstruction, version 3 procedure) + "
                      "analysis/scripts/a10_assemble.py (assembly, known = 22 tuning districts); "
                      "scorer analysis/scripts/a10_stepb_calibrate.py, gates as a7_stepb_calibrate.py"),
        "sample": eds,
        "pages_dir": str(pages_dir),
        "placed": len(placed),
        "placed_eds": [r["ed"] for r in rows if r["status"] == "placed"],
        "rejected_eds": [r["ed"] for r in rows if r["status"].startswith("rejected")],
        "filled_eds": [r["ed"] for r in rows if r["status"] == "filled"],
        "failed": [r["ed"] for r in rows if r["status"].startswith("failed")],
        "scored_assignment": "final (assemble -> a10_snap_assign); the assembly alone is under before_snap",
        "T1": t1_final,
        "T4": t4_final,
        "before_snap": {"T1": t1_before, "T4": t4_before},
        "snap": {"drift": snap.get("drift"), "snapping": snap.get("snapping"), "merged_holes": snap.get("merged_holes"),
                 "cut_vas": snap.get("cut_vas"), "sanity": snap.get("sanity"), "constants": snap.get("constants"),
                 "output_dir": str(snap_dir), "seconds": snap.get("seconds")},
        "T2_mean_abs_area_err_pct": mean_or_none([abs(r["area_err_pct"]) for r in placed]),
        "T3_mean_hausdorff_km": mean_or_none([r["hausdorff_km"] for r in placed]),
        "mean_iou": mean_or_none([r["iou"] for r in placed]),
        "reconstruction_quality_all_polygons": {
            "n": len(with_poly),
            "T2_mean_abs_area_err_pct": mean_or_none([abs(r["area_err_pct"]) for r in with_poly]),
            "T3_mean_hausdorff_km": mean_or_none([r["hausdorff_km"] for r in with_poly]),
            "mean_iou": mean_or_none([r["iou"] for r in with_poly]),
        },
        "districts": rows,
        "assembly": {
            "summary": res.summary,
            "parameters": {**{k: v.default for k, v in inspect.signature(A.assemble).parameters.items()
                              if v.kind is inspect.Parameter.KEYWORD_ONLY and k != "graph"},
                           **{k: getattr(A, k) for k in sorted(dir(A))  # every numeric rule constant the assembler declares
                              if k.isupper() and isinstance(getattr(A, k), (int, float)) and not isinstance(getattr(A, k), bool)}},
            "rejected": res.rejected,
            "filled": res.filled,
            "unassigned_components": res.unassigned_components,
            "districts": res.districts.to_dict("records"),
        },
        "pages_loaded": sorted(pages),
        "polygons_loaded": sorted(polys),
        "sec": round(time.time() - t0, 1),
        "environment": environment(),
    }
    sanity = snap.get("sanity") or {}
    res_json["snap_sanity_all_pass"] = bool(sanity and all(v.get("pass") is True for v in sanity.values()))  # reported beside the gates, not one of them
    res_json["gates_pass"] = bool(res_json["T1"]["pass"] and res_json["T4"]["pass"])
    # a run outside the registered environment (--allow-any-env) can never read as a passing calibration
    res_json["calibration_passes"] = bool(res_json["gates_pass"] and REGISTERED_ENVIRONMENT)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(clean(res_json), indent=1), encoding="utf-8")
    brief = {k: v for k, v in res_json.items() if k not in ("districts", "assembly", "pages_loaded", "polygons_loaded")}
    print(json.dumps(clean(brief), indent=1))


if __name__ == "__main__":
    main()
