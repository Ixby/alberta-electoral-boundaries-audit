# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
cut_va_sensitivity.py
---------------------

Amendment 10, extra check 1: how much can the cut voting areas (VAs) matter?

A VA is "cut" when a reconstructed district line runs through it (a10_snap_assign.py, cut=True in
va_assignment.csv). The pipeline gives the whole VA to the district holding its representative point.
Those VAs are the only place where a correct line can still produce a wrong assignment. Reporting only:
nothing here changes a placement or an assignment.

Step 1, inventory (both maps; no partisan measure of any kind)
  For every cut VA: assigned district, partner districts, the share of its area on each side
  (recomputed from the known geometry + snapped_pieces.gpkg with a10_assemble._area_shares, the same
  function a10_snap_assign.assign uses; checked against the cut_partners column of the csv),
  2021 population (pop_2021, area-weighted from DAs, floored at 1 by the loader) and total votes cast
  (the loader's total_votes = sum of the candidate vote columns, summed before the party columns are
  dropped; no party column is kept or printed). Minority share = sum of the area shares of every piece
  except the largest. Cuts are split into "known-known" (assigned district and every partner are
  known districts: commission geometry against the VA layer, identical to the official map) and
  "involves changed" (at least one side is not known: the only cuts that matter for the real map).

Step 2, flip range (calibration map only; refuses to run on any other map unless A10_STEPC=1)
  Uses the scorer's composite map and mcmc_ensemble.score_exogenous_map exactly as
  a10_stepb_calibrate.gate_blocks does. EG (efficiency gap) for: the pipeline assignment; each cut VA
  with minority share >= FLIP_MIN flipped, alone, to its largest partner; and two bounding maps built
  GREEDILY from the single-flip signs (every flip that raised EG applied together, then every flip that
  lowered it applied together). Interactions between flips are not modelled: the bounds are
  heuristic, not exact extremes. T1 (misassigned sample VAs) is also reported under both bounding maps.

Environment: Python 3.12.13 with PyMuPDF 2.1 (a10_stepb_calibrate refuses to import otherwise).

Step C copy of findings/a10_dev/cut_va_sensitivity.py (c264a49e...) with one correction to step 2 on map "fixed";
see findings/a10_stepc/README.md.

Usage: C:/Users/email/.venvs/audit-k91/Scripts/python.exe -W ignore findings/a10_stepc/cut_va_sensitivity_stepc.py \
           --map tuning|fixed --snap-dir DIR --out-prefix findings/a10_dev/cut_va_sensitivity
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import geopandas as gpd  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import shapely  # noqa: E402

import a10_assemble as A  # noqa: E402
import a10_stepb_calibrate as S  # noqa: E402  (loaders and the scorer; its main() is never called)

me = S.me
CUT_SHARE = 0.01                     # a10_snap_assign.CUT_SHARE: another piece holding more than this share marks the VA cut
FLIP_MIN = 0.10                     # step 2: a cut VA is flipped when its minority side holds at least this share
THRESHOLDS = (0.10, 0.25, 0.40)      # step 1: minority-side summaries
PARTY_COLS = ("va_ucp", "va_ndp", "va_other")
CSV_COLS = ["OBJECTID", "VA_NUMBER", "district", "ed", "confidence", "cut_category", "assigned_has_piece",
            "assigned_share", "partners", "top_partner", "top_partner_share", "minority_share",
            "assigned_is_area_majority", "pop_2021", "total_votes", "flip_eligible"]


def step2_allowed(which):
    """Step 2 computes partisan measures: calibration map always, anything else only with A10_STEPC=1."""
    return which == "tuning" or os.environ.get("A10_STEPC") == "1"


def load_vas(which, keep_party):
    """VA layer with pop_2021 and total_votes. For the real map the party columns are dropped on load."""
    va, _graph = me.build_va_graph(verbose=False)
    if not keep_party:
        va = va.drop(columns=[c for c in PARTY_COLS if c in va.columns])
    return va


def shares_for(va3400, pieces, rows):
    """{row position: {piece name: area share}} for the given VA row positions."""
    names = list(pieces)
    geoms = np.asarray(va3400.geometry.values, dtype=object)[rows]
    area = shapely.area(geoms)
    vi, di, sh = A._area_shares(geoms, area, np.array([pieces[n] for n in names], dtype=object))
    out = {int(r): {} for r in rows}
    for v, d, s in zip(vi, di, sh):
        out[int(rows[v])][names[d]] = float(s)
    return out


def inventory(which, snap_dir, va, app7):
    """Step 1. Returns (cut-VA DataFrame, summary dict). No partisan column is read."""
    snap_dir = Path(snap_dir)
    ids = pd.read_csv(snap_dir / "va_assignment.csv", dtype={"OBJECTID": str, "VA_NUMBER": str})
    if len(ids) != len(va):
        raise ValueError(f"{len(ids)} csv rows for {len(va)} VAs")
    for c in ("OBJECTID", "VA_NUMBER"):
        if c in ids.columns and c in va.columns and not (ids[c].to_numpy() == va[c].astype(str).to_numpy()).all():
            raise ValueError(f"column {c} does not match the VA table")
    known = A.known_districts(which, app7)
    sp = gpd.read_file(snap_dir / "snapped_pieces.gpkg").to_crs(3400)
    pieces = {**known, **{r.district: r.geometry for r in sp.itertuples()}}
    va3400 = va.to_crs(3400)
    cutpos = np.flatnonzero(ids["cut"].astype(bool).to_numpy())
    sh = shares_for(va3400, pieces, cutpos)
    rows, worst_csv_gap = [], 0.0
    for r in cutpos:
        rec = ids.iloc[r]
        own = rec["district"]
        s = sh[int(r)]
        csv_partners = {}
        for tok in str(rec["cut_partners"]).split(";"):
            if tok:
                n, _, x = tok.rpartition(":")
                csv_partners[n] = float(x)
        partners = {n: x for n, x in s.items() if n != own and x > CUT_SHARE}
        for n, x in csv_partners.items():  # the csv is the pipeline's own record: it must agree with the recompute
            worst_csv_gap = max(worst_csv_gap, abs(x - partners.get(n, 0.0)))
        order = sorted(partners.items(), key=lambda kv: (-kv[1], kv[0]))
        have = own in s
        a_sh = s.get(own) if have else None
        allv = sorted(s.values(), reverse=True)
        minority = float(sum(allv[1:])) if allv else 0.0
        top = order[0] if order else (None, 0.0)
        cat = "known_known" if (own in known and all(n in known for n in partners)) else "involves_changed"
        rows.append({"OBJECTID": rec.get("OBJECTID"), "VA_NUMBER": rec.get("VA_NUMBER"), "district": own,
                     "ed": rec.get("ed"), "confidence": rec["confidence"], "cut_category": cat,
                     "assigned_has_piece": have, "assigned_share": a_sh,
                     "partners": ";".join(f"{n}:{x:.3f}" for n, x in order), "top_partner": top[0],
                     "top_partner_share": top[1], "minority_share": minority,
                     "assigned_is_area_majority": (a_sh >= top[1]) if have else None,
                     "pop_2021": float(va["pop_2021"].iloc[r]), "total_votes": float(va["total_votes"].iloc[r]),
                     "flip_eligible": bool(minority >= FLIP_MIN and top[0] is not None), "_row": int(r)})
    cut = pd.DataFrame(rows)
    n_cut_csv = int(ids["cut"].astype(bool).sum())
    pop_tot, bal_tot = float(va["pop_2021"].sum()), float(va["total_votes"].sum())

    def block(d):
        if d.empty:
            return {"n": 0}
        out = {"n": int(len(d)), "population": float(d.pop_2021.sum()), "total_votes": float(d.total_votes.sum()),
               "population_share_of_province": float(d.pop_2021.sum() / pop_tot),
               "total_votes_share_of_province": float(d.total_votes.sum() / bal_tot)}
        for t in THRESHOLDS:
            m = d.minority_share >= t
            out[f"minority_ge_{int(t * 100)}pct"] = {"n": int(m.sum()), "population": float(d.pop_2021[m].sum()),
                                                       "total_votes": float(d.total_votes[m].sum())}
        return out

    known_names = set(known)
    table = ids["district"]
    per = []
    for n in sorted(set(table.dropna()) - known_names):
        sel = (table == n).to_numpy()
        mine = cut[(cut.district == n)]
        asp = cut[cut.partners.str.contains(f"{n}:", regex=False) & (cut.district != n)] if len(cut) else cut
        per.append({"district": n, "ed": None if not sel.any() else int(ids["ed"][sel].iloc[0]),
                    "district_population": float(va["pop_2021"][sel].sum()),
                    "district_total_votes": float(va["total_votes"][sel].sum()), "n_vas": int(sel.sum()),
                    "assigned_cut": block(mine), "cut_where_partner": block(asp)})
    summary = {
        "which": which, "snap_dir": str(snap_dir), "n_vas": int(len(va)), "n_known_districts": len(known),
        "cut_flag_in_csv": n_cut_csv, "cut_vas_recomputed": int(len(cut)),
        "worst_gap_vs_csv_partner_share": worst_csv_gap,
        "province": {"population": pop_tot, "total_votes": bal_tot,
                     "note": "pop_2021 = DA-overlay population floored at 1 per VA; total_votes = sum of candidate vote columns"},
        "all_cut_vas": block(cut),
        "involves_changed": block(cut[cut.cut_category == "involves_changed"]),
        "known_known": block(cut[cut.cut_category == "known_known"]),
        "per_changed_district": per,
        "n_flip_eligible": int(cut.flip_eligible.sum()) if len(cut) else 0,
        "n_flip_eligible_involves_changed": int(cut[cut.cut_category == "involves_changed"].flip_eligible.sum()) if len(cut) else 0,
    }
    return cut, summary


def flip_range(which, snap_dir, va, cut):
    """Step 2: EG range from flipping cut VAs. Calibration map only (see step2_allowed)."""
    if not step2_allowed(which):
        sys.exit(f"step 2 computes partisan measures and refuses to run on map {which!r} without A10_STEPC=1")
    t0 = time.time()
    app7, maj, eds, name, truth = S.load_context()
    va3400 = va.to_crs(3400)
    pts = gpd.GeoSeries(va3400.geometry.representative_point(), index=va.index, crs=3400)
    inside = S.sample_vas(pts, truth)
    labels = S.final_labels(Path(snap_dir) / "va_assignment.csv", va)
    eg_off = me.score_exogenous_map(va, S.MAJ)

    def run(lab):
        if which == "fixed":
            # Step C correction (findings/a10_stepc/README.md): the registered code built the calibration
            # composite (majority map with only the sample districts replaced) for every map, so on the
            # panel's map it never scored the changed districts. Here every district is the union of the
            # VAs the assignment gives it, so the EG is the assembled map's own.
            comp = gpd.GeoDataFrame({"EDName2025": lab.to_numpy(dtype=object)}, geometry=va3400.geometry.to_numpy(),
                                    crs=3400).dissolve(by="EDName2025", as_index=False)
        else:
            comp, _ = S.composite_map(maj, va3400.geometry, lab, eds, name)
        eg = S.score_composite(va, comp)["efficiency_gap"]
        _, wrong, total = S.score_t1(lab, inside, name)
        return eg, wrong, total

    def flipped(lab, rows):
        lab = lab.copy()
        for r in rows:
            lab.iloc[r] = S.norm(cut.loc[cut._row == r, "top_partner"].iloc[0])
        return lab

    eg0, w0, tot = run(labels)
    print(f"[{time.time() - t0:.0f}s] pipeline EG {eg0:+.5f}  T1 wrong {w0}/{tot}", flush=True)
    elig = cut[cut.flip_eligible]
    single = {}
    for k, r in enumerate(elig._row):
        eg, w, _ = run(flipped(labels, [r]))
        single[int(r)] = {"eg": eg, "delta_points": 100 * (eg - eg0), "t1_wrong": w}
        if k % 10 == 0:
            print(f"[{time.time() - t0:.0f}s] single flip {k + 1}/{len(elig)}", flush=True)
    up = [r for r, d in single.items() if d["delta_points"] > 0]
    dn = [r for r, d in single.items() if d["delta_points"] < 0]
    eg_up, w_up, _ = run(flipped(labels, up)) if up else (eg0, w0, tot)
    eg_dn, w_dn, _ = run(flipped(labels, dn)) if dn else (eg0, w0, tot)
    big = max(single.items(), key=lambda kv: abs(kv[1]["delta_points"]), default=(None, None))
    d = cut.set_index("_row")
    off = eg_off["efficiency_gap"]
    pts_ = lambda x: 100 * x  # noqa: E731
    out = {
        "eg_official": off, "eg_pipeline": eg0, "pipeline_minus_official_points": pts_(eg0 - off),
        "t4_limit_points": pts_(S.T4_MAX), "t1_limit": S.T1_MAX,
        "flip_min_minority_share": FLIP_MIN, "n_flipped_singly": len(single),
        "bounding_method": "greedy from the single-flip signs; interactions between flips not modelled",
        "largest_single_flip": None if big[0] is None else {
            "OBJECTID": d.loc[big[0], "OBJECTID"], "VA_NUMBER": d.loc[big[0], "VA_NUMBER"],
            "from": d.loc[big[0], "district"], "to": d.loc[big[0], "top_partner"],
            "minority_share": float(d.loc[big[0], "minority_share"]), "pop_2021": float(d.loc[big[0], "pop_2021"]),
            "total_votes": float(d.loc[big[0], "total_votes"]), "delta_points": big[1]["delta_points"]},
        "n_single_flips_raise_eg": len(up), "n_single_flips_lower_eg": len(dn),
        "n_single_flips_zero": len(single) - len(up) - len(dn),
        "bound_up": {"n_flips": len(up), "eg": eg_up, "minus_official_points": pts_(eg_up - off),
                     "minus_pipeline_points": pts_(eg_up - eg0), "t4_pass": bool(abs(eg_up - off) < S.T4_MAX),
                     "t1": {"wrong": w_up, "total": tot, "share": w_up / tot, "pass": bool(w_up / tot <= S.T1_MAX)}},
        "bound_down": {"n_flips": len(dn), "eg": eg_dn, "minus_official_points": pts_(eg_dn - off),
                       "minus_pipeline_points": pts_(eg_dn - eg0), "t4_pass": bool(abs(eg_dn - off) < S.T4_MAX),
                       "t1": {"wrong": w_dn, "total": tot, "share": w_dn / tot, "pass": bool(w_dn / tot <= S.T1_MAX)}},
        "pipeline_t1": {"wrong": w0, "total": tot, "share": w0 / tot, "pass": bool(w0 / tot <= S.T1_MAX)},
        "seconds": round(time.time() - t0, 1),
    }
    return out, single


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True, choices=["tuning", "fixed"])
    ap.add_argument("--snap-dir", required=True)
    ap.add_argument("--out-prefix", required=True, help="writes PREFIX_<map>.json and, beside it, cut_vas_<map>.csv")
    ap.add_argument("--skip-step2", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    do2 = not a.skip_step2 and step2_allowed(a.map)
    va = load_vas(a.map, keep_party=do2)
    app7 = A.load_app7()
    cut, summary = inventory(a.map, a.snap_dir, va, app7)
    print(f"[{time.time() - t0:.0f}s] inventory: {len(cut)} cut VAs", flush=True)
    res = {"step1_inventory": summary}
    if do2:
        res["step2_flip_range"], single = flip_range(a.map, a.snap_dir, va, cut)
        cut["flip_delta_eg_points"] = cut._row.map(lambda r: single.get(int(r), {}).get("delta_points"))
    else:
        res["step2_flip_range"] = {"run": False, "reason": "partisan step; refused for this map without A10_STEPC=1"
                                   if not step2_allowed(a.map) else "skipped by --skip-step2"}
    res["seconds"] = round(time.time() - t0, 1)
    pre = Path(a.out_prefix)
    pre.parent.mkdir(parents=True, exist_ok=True)
    pre.with_name(f"{pre.name}_{a.map}.json").write_text(json.dumps(S.clean(res), indent=1) + "\n", encoding="utf-8")
    cols = CSV_COLS + (["flip_delta_eg_points"] if "flip_delta_eg_points" in cut.columns else [])
    cut[cols].to_csv(pre.parent / f"cut_vas_{a.map}.csv", index=False, lineterminator="\n")
    print(json.dumps(S.clean({k: v for k, v in summary.items() if k != "per_changed_district"}), indent=1))
    if do2:
        print(json.dumps(S.clean(res["step2_flip_range"]), indent=1))
    print(f"done in {res['seconds']}s")


if __name__ == "__main__":
    main()
