# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence) | Government of Alberta (OGL-Alberta)
"""
rebuild_da_2024.py

Runs preregistration/osi_da_rebuild_2026-11-07.md: rebuilds dissemination-area (DA) population figures
for July 1, 2024 that reproduce the published division totals, holds each map out in turn as the
pass/fail check, and (only if all pass) totals the para 167 map and reruns the eligibility check.
Unregistered. A reconstruction, not the Office of Statistics and Information's file.

Prior weight: the plan says "in proportion to each prior"; implemented as a chi-square scale,
(x - p) / sqrt(p * mean division total), so a new neighbourhood with a small prior can still grow.

Reads   data/shapefiles/reference/alberta_2021_das.gpkg, data/census_2021/alberta_da_profile.csv
        data/osi/population-estimates-ab-census-subdivision-municipal-2016-to-current.xlsx
        data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg, data/iap/iap_app7_populations.csv
        data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg, findings/iap_para167/para167_map.gpkg
        data/shapefiles/reference/alberta_2021_csds.gpkg, findings/referendum_electors/division_table.csv
Writes  findings/osi_rebuild/holdout.json, fit_all.json, da_2024_rebuilt.csv, para167_totals.csv,
        eligibility_rebuilt.csv

Usage: python -W ignore findings/osi_rebuild/rebuild_da_2024.py
"""
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.optimize import lsq_linear

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DAS = ROOT / "data/shapefiles/reference/alberta_2021_das.gpkg"
PROFILE = ROOT / "data/census_2021/alberta_da_profile.csv"
CSD_XLSX = ROOT / "data/osi/population-estimates-ab-census-subdivision-municipal-2016-to-current.xlsx"
CSD_POLY = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
PARA = ROOT / "findings/iap_para167/para167_map.gpkg"
TOTAL = 4888723
W_DIV, W_CSD, W_PRIOR, W_TOTAL = 1.0, 0.1, 0.01, 100.0
PRIOR_FLOOR = 50.0
PASS_MEAN, PASS_MAX = 2.0, 6.0
SAME_IOU = 0.99
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def maps():
    maj = gpd.read_file(ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg").to_crs(3400)
    mino = gpd.read_file(ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg").to_crs(3400)
    pan = gpd.read_file(ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg").to_crs(3400)
    app7 = pd.read_csv(ROOT / "data/iap/iap_app7_populations.csv").set_index("district").population
    out = {}
    for k, g, col, tot in (("majority", maj, "EDName2025", None), ("minority", mino, "EDName2025", None), ("panel", pan, "district", app7)):
        g = g[[col, "geometry"] + (["PopCensus"] if tot is None else [])].rename(columns={col: "division"})
        g["total"] = g.PopCensus if tot is None else g.division.map(tot)
        assert g.total.notna().all() and abs(g.total.sum() - TOTAL) < 5, (k, g.total.sum())
        out[k] = g[["division", "total", "geometry"]].reset_index(drop=True)
    return out


def csd_2024():
    z = zipfile.ZipFile(CSD_XLSX)
    ss = ["".join(t.text or "" for t in si.iter(NS + "t")) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si")]
    rows = []
    for r in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS + "row"):
        row = {}
        for c in r.findall(NS + "c"):
            v = c.find(NS + "v")
            row[re.match(r"[A-Z]+", c.get("r")).group(0)] = ss[int(v.text)] if c.get("t") == "s" and v is not None else (v.text if v is not None else "")
        rows.append(row)
    hdr = next(i for i, r in enumerate(rows) if r.get("B") == "Census Subdivision")
    cols = rows[hdr]
    y21 = next(k for k, v in cols.items() if v == "2021")
    y24 = next(k for k, v in cols.items() if v == "2024")
    num = re.compile(r"\d+(\.\d+)?")
    # "--" marks a municipality with no estimate for that year; it is left out, not set to zero.
    d = [(r["B"], float(r[y21]), float(r[y24])) for r in rows[hdr + 1:]
         if re.fullmatch(r"48\d{5}", str(r.get("B", ""))) and num.fullmatch(str(r.get(y21, ""))) and num.fullmatch(str(r.get(y24, "")))]
    out = pd.DataFrame(d, columns=["csduid", "est_2021", "est_2024"]).set_index("csduid")
    # Municipalities estimated at zero (dissolved or merged) give no growth rate and no usable constraint.
    return out[(out.est_2021 > 0) & (out.est_2024 > 0)]


def weights(da, g):
    """Sparse matrix (divisions x DAs) of each DA's area share in each division."""
    ov = gpd.overlay(da[["i", "geometry"]], g[["division", "geometry"]].assign(k=range(len(g))), how="intersection", keep_geom_type=True)
    area = da.area.values[ov.i.values]
    ov["share"] = np.where(area > 0, ov.geometry.area / np.where(area > 0, area, 1), np.nan)
    ov = ov[ov.share.notna() & (ov.share > 1e-4)]
    s = ov.groupby("i").share.transform("sum")
    ov["share"] = ov.share / s
    # A DA counts as split if a second division holds at least 1% of it; smaller pieces are line slivers.
    split = ov[ov.share >= 0.01].groupby("i").k.nunique()
    return sparse.csr_matrix((ov.share.values, (ov.k.values, ov.i.values)), shape=(len(g), len(da))), split


def fit(A_blocks, T_blocks, C, E, prior, n):
    tbar = np.mean(np.concatenate(T_blocks))
    rows, rhs = [], []
    for A, T in zip(A_blocks, T_blocks):
        rows.append(sparse.diags(W_DIV / T) @ A)
        rhs.append(W_DIV * np.ones(len(T)))
    rows.append(sparse.diags(W_CSD / E) @ C)
    rhs.append(W_CSD * np.ones(len(E)))
    sc = W_PRIOR / np.sqrt(prior * tbar)
    rows.append(sparse.diags(sc))
    rhs.append(sc * prior)
    rows.append(sparse.csr_matrix(np.full((1, n), W_TOTAL / TOTAL)))
    rhs.append(np.array([W_TOTAL]))
    M = sparse.vstack(rows).tocsr()
    r = lsq_linear(M, np.concatenate(rhs), bounds=(0, np.inf), method="trf", lsmr_tol="auto", max_iter=400, verbose=0)
    return r.x, r.status


def same_polygons(g, others):
    out = set()
    for o in others:
        sidx = o.sindex
        for i, geom in enumerate(g.geometry):
            for j in sidx.query(geom, predicate="intersects"):
                a = geom.intersection(o.geometry.iloc[j]).area
                if a / geom.union(o.geometry.iloc[j]).area > SAME_IOU:
                    out.add(i)
    return out


def main():
    da = gpd.read_file(DAS).to_crs(3400).reset_index(drop=True)
    da["DAUID"] = da.DAUID.astype(str)
    da["i"] = np.arange(len(da))
    prof = pd.read_csv(PROFILE, dtype={"DAUID": str}).set_index("DAUID").reindex(da.DAUID)
    p21 = prof.pop_2021.fillna(0).to_numpy(float)

    csd = gpd.read_file(CSD_POLY).to_crs(3400)
    ucol = next(c for c in csd.columns if c.upper() == "CSDUID")
    pts = da[["geometry"]].copy()
    pts["geometry"] = da.geometry.representative_point()
    j = gpd.sjoin(pts, csd[[ucol, "geometry"]], how="left", predicate="within")
    da["csduid"] = j[~j.index.duplicated(keep="first")][ucol].astype(str).reindex(da.index).values
    est = csd_2024()
    growth = (est.est_2024 / est.est_2021).reindex(da.csduid).fillna(TOTAL / p21.sum()).to_numpy()
    prior = np.maximum(p21 * growth, PRIOR_FLOOR)
    prior *= TOTAL / prior.sum()
    present = sorted(set(da.csduid) & set(est.index))
    cidx = {c: k for k, c in enumerate(present)}
    keep = da.csduid.isin(cidx)
    C = sparse.csr_matrix((np.ones(int(keep.sum())), (da.csduid[keep].map(cidx).values, da.i[keep].values)), shape=(len(present), len(da)))
    E = est.est_2024.reindex(present).to_numpy()

    M = maps()
    W, split = {}, {}
    cache = HERE / ".weights_cache"
    cache.mkdir(exist_ok=True)
    for k, g in M.items():
        f = cache / f"{k}.npz"
        if f.exists():
            W[k] = sparse.load_npz(f)
            split[k] = pd.read_pickle(cache / f"{k}_split.pkl")
        else:
            W[k], split[k] = weights(da, g)
            sparse.save_npz(f, W[k])
            split[k].to_pickle(cache / f"{k}_split.pkl")
    print("DAs with zero area:", int((da.area == 0).sum()), "DAs in no division per map:", {k: int((np.asarray(W[k].sum(axis=0)).ravel() == 0).sum()) for k in W})
    info = {"plan": "preregistration/osi_da_rebuild_2026-11-07.md", "n_das": len(da),
            "csd_estimates_2024_total": float(E.sum()), "csd_matched": len(present),
            "share_pop_2021_in_split_das": {k: round(float(p21[s[s > 1].index.values].sum() / p21.sum()), 4) for k, s in split.items()}}
    print(info)

    hold = {}
    for out_k in M:
        fit_k = [k for k in M if k != out_k]
        x, status = fit([W[k] for k in fit_k], [M[k].total.to_numpy(float) for k in fit_k], C, E, prior, len(da))
        pred = W[out_k] @ x
        T = M[out_k].total.to_numpy(float)
        bad = ~np.isfinite(pred)
        if bad.any() or not np.isfinite(x).all():
            print("non-finite:", int(bad.sum()), "divisions;", int((~np.isfinite(x)).sum()), "DAs", list(M[out_k].division[bad])[:5])
        err = 100 * (pred / T - 1)
        same = same_polygons(M[out_k], [M[k] for k in fit_k])
        test = np.array([i not in same for i in range(len(T))])
        prior_err = 100 * ((W[out_k] @ prior) / T - 1)
        worst = np.argsort(-np.abs(np.where(test, err, 0)))[:8]
        hold[out_k] = {"solver_status": int(status), "n_divisions": int(len(T)), "n_identical_excluded": int((~test).sum()),
                       "n_tested": int(test.sum()), "mean_abs_err_pct": round(float(np.abs(err[test]).mean()), 2),
                       "max_abs_err_pct": round(float(np.abs(err[test]).max()), 2),
                       "prior_alone_mean_abs_err_pct": round(float(np.abs(prior_err[test]).mean()), 2),
                       "pass": bool(np.abs(err[test]).mean() <= PASS_MEAN and np.abs(err[test]).max() <= PASS_MAX),
                       "worst": {M[out_k].division[i]: {"published": int(T[i]), "predicted": round(float(pred[i])), "err_pct": round(float(err[i]), 2)} for i in worst}}
        print(out_k, {k: v for k, v in hold[out_k].items() if k != "worst"})
    passed = all(h["pass"] for h in hold.values())
    (HERE / "holdout.json").write_text(json.dumps({"info": info, "holdout": hold, "all_pass": passed}, indent=1), encoding="utf8")
    if not passed:
        print("FAIL: the rebuilt figures do not reproduce the source; not used for new boundaries")
        for k, h in hold.items():
            print(k, h["worst"])
        return

    x, status = fit([W[k] for k in M], [M[k].total.to_numpy(float) for k in M], C, E, prior, len(da))
    fitted = {k: {"mean_abs_err_pct": round(float(np.abs(100 * ((W[k] @ x) / M[k].total.to_numpy() - 1)).mean()), 3),
                  "max_abs_err_pct": round(float(np.abs(100 * ((W[k] @ x) / M[k].total.to_numpy() - 1)).max()), 3)} for k in M}
    (HERE / "fit_all.json").write_text(json.dumps({"solver_status": int(status), "fit_to_published": fitted, "total": float(x.sum())}, indent=1), encoding="utf8")
    pd.DataFrame({"DAUID": da.DAUID, "pop_2021": p21, "prior_2024": prior.round(1), "rebuilt_2024": x.round(1)}).to_csv(HERE / "da_2024_rebuilt.csv", index=False)
    print("fit all", fitted, x.sum())

    para = gpd.read_file(PARA).to_crs(3400)[["district", "source", "geometry"]].rename(columns={"district": "division"})
    Wp, _ = weights(da, para)
    tot = Wp @ x
    avg = tot.mean()
    pt = para.drop(columns="geometry").assign(rebuilt_2024=tot.round(), dev_pct=(100 * (tot / avg - 1)).round(1))
    pt.to_csv(HERE / "para167_totals.csv", index=False)
    print(pt.sort_values("dev_pct").head(6).to_string(), pt.sort_values("dev_pct").tail(3).to_string())
    print(pt[pt.source == "amended"].to_string())

    t = pd.read_csv(ROOT / "findings/referendum_electors/division_table.csv")
    share = (prof.citizens_18_plus / prof.citizenship_total).to_numpy()
    share = np.where(np.isfinite(share), share, np.nan)
    csd_share = pd.Series(share).groupby(da.csduid.values).transform(lambda s: s.fillna(s.mean())).to_numpy()
    share = np.where(np.isnan(share), csd_share, share)
    share = np.where(np.isnan(share), np.nanmean(share), share)
    rows = []
    for k in ("majority", "panel"):
        x_ = t[t["map"] == k].set_index("division")
        g = M[k].set_index("division")
        elig = W[k] @ (share * x)
        rebuilt = W[k] @ x
        s_ = pd.Series(elig / rebuilt, index=g.index).reindex(x_.index)
        exp = s_ * x_.stated_pop
        exp *= x_.electors_2026.sum() / exp.sum()
        rows.append(pd.DataFrame({"map": k, "electors_2026": x_.electors_2026, "stated_pop": x_.stated_pop,
                                  "eligible_share_weighted_2024": s_.round(3), "expected_electors": exp.round(),
                                  "left_over": (x_.electors_2026 / exp).round(3)}).reset_index())
    el = pd.concat(rows)
    el.to_csv(HERE / "eligibility_rebuilt.csv", index=False)
    print(el[el.division.isin(["Calgary-North East", "Calgary-Bhullar-McCall", "Calgary-Falconridge-Conrich", "Calgary-Buffalo", "Edmonton-Meadows"])].to_string())
    for k in ("majority", "panel"):
        e = el[el["map"] == k]
        print(k, "mean abs miss", round(100 * float((e.left_over - 1).abs().mean()), 1))


if __name__ == "__main__":
    main()
