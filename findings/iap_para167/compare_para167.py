# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
compare_para167.py

Scores the panel's map (v3) beside the para 167 map, as set out in
preregistration/r5_comparator_2026-11-07.md. Unregistered; both maps rest on the reconstruction.
Gives no conclusion on whether any map is a gerrymander.

Groups are found, not assumed: two districts belong together if voting areas move between them, so
each connected group covers the same voting areas on both maps and can be switched alone.

Reads   findings/iap_para167/para167_map.gpkg, va_assignment.csv, real_maps_*.json
        data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg
        data/shapefiles/derived/va_polygons_with_2023_votes.gpkg (election-day ballots)
        data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg (all ballots)
        ALBERTA_AUDIT/data/simulation_checkpoints_k91_s152a23[_allballots]/chain25[1-4]_samples.csv
Writes  findings/iap_para167/comparison.json

Usage: python -W ignore findings/iap_para167/compare_para167.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis/scripts"))
from close_seats_ensemble import seat_results_close  # noqa: E402
from mcmc_ensemble import pct_rank  # noqa: E402

V3 = ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg"
PARA = HERE / "para167_map.gpkg"
BALLOTS = {"election_day": ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg",
           "all_ballots": ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"}
CHAINS = {"election_day": "simulation_checkpoints_k91_s152a23", "all_ballots": "simulation_checkpoints_k91_s152a23_allballots"}
AUDIT = ROOT.parent / "alberta_audit"
MEASURES = ["ucp_seats", "efficiency_gap", "mean_median", "declination", "seats_at_50_50", "close4",
            "population_mad", "city_gap_pct", "towns_flagged"]
SLIGHT, CUT = 0.01, 0.99


def assign(pts, f):
    eds = gpd.read_file(f).to_crs(pts.crs)
    j = gpd.sjoin(pts, eds[["district", "geometry"]], how="left", predicate="within")
    return j[~j.index.duplicated(keep="first")]["district"].reindex(pts.index)


def tally(v, labels):
    g = v[["va_ucp", "va_ndp", "va_other"]].groupby(labels.values).sum()
    g["winner"] = np.where(g.va_ucp > g.va_ndp, "ucp", "ndp")
    assert (g.va_other < g[["va_ucp", "va_ndp"]].max(axis=1)).all()
    t = g.va_ucp + g.va_ndp + g.va_other
    g["margin_pts"] = 100 * (g.va_ucp - g.va_ndp).abs() / t
    return g


def score(v, labels):
    g = v[["va_ucp", "va_ndp"]].groupby(labels.values).sum().sort_index()
    return seat_results_close(g.va_ucp.values, g.va_ndp.values)


def ranks(ballot, real):
    d = AUDIT / "data" / CHAINS[ballot]
    cols = set(MEASURES)
    frames = [pd.read_csv(d / f"chain{i}_samples.csv", usecols=lambda c: c in cols) for i in (251, 252, 253, 254)]
    df = pd.concat(frames)
    out = {"n_plans": len(df)}
    for m in MEASURES:
        v = df[m].to_numpy(float)
        v = v[~np.isnan(v)]
        out[m] = {"q05": float(np.quantile(v, 0.05)), "q50": float(np.quantile(v, 0.5)), "q95": float(np.quantile(v, 0.95))}
        for k in ("iap_2026_assembled_v3", "para167_map"):
            out[m][k] = {"value": float(real[k][m]), "pct": round(float(pct_rank(v, float(real[k][m]))), 2)}
    return out


def main():
    base = gpd.read_file(BALLOTS["election_day"]).to_crs(3400)
    pts = base[["geometry"]].copy()
    pts["geometry"] = base.geometry.representative_point()
    panel, para = assign(pts, V3), assign(pts, PARA)
    a = pd.read_csv(HERE / "va_assignment.csv")["district"]
    assert (a.values == para.values).all() and panel.notna().all() and para.notna().all()

    votes = {}
    for k, f in BALLOTS.items():
        d = gpd.read_file(f, ignore_geometry=True)
        assert (d.OBJECTID.values == base.OBJECTID.values).all()
        votes[k] = d

    moved = panel.values != para.values
    G = nx.Graph()
    G.add_edges_from({("P:" + p, "R:" + r) for p, r in zip(panel, para)})
    groups = []
    for comp in nx.connected_components(G):
        if len(comp) == 2 and {x[2:] for x in comp} == {next(iter(comp))[2:]}:
            continue  # same name, same voting areas on both maps
        P = sorted(x[2:] for x in comp if x.startswith("P:"))
        R = sorted(x[2:] for x in comp if x.startswith("R:"))
        groups.append({"panel": P, "para167": R})
    groups.sort(key=lambda g: g["panel"][0])

    gdf_p = gpd.read_file(V3).to_crs(3400).set_index("district").geometry
    gdf_r = gpd.read_file(PARA).to_crs(3400).set_index("district").geometry

    def cut_votes(v, geom):
        sub = base[base.intersects(geom)]
        share = sub.geometry.intersection(geom).area / sub.geometry.area
        idx = share[(share > SLIGHT) & (share < CUT)].index
        return float(v.loc[idx, ["va_ucp", "va_ndp", "va_other"]].to_numpy().sum())

    out = {"plan": "preregistration/r5_comparator_2026-11-07.md", "vas_moved": int(moved.sum()), "groups": groups}
    for k, v in votes.items():
        tp, tr = tally(v, panel), tally(v, para)
        rp = json.loads((HERE / f"real_maps_{k}.json").read_text())
        sp, sr = score(v, panel), score(v, para)
        assert sp["ucp_seats"] == rp["iap_2026_assembled_v3"]["ucp_seats"] and sr["ucp_seats"] == rp["para167_map"]["ucp_seats"]
        check = tally(v, v.parent_ed_2019)
        block = {"method_check_2019": {"UCP": int((check.winner == "ucp").sum()), "NDP": int((check.winner == "ndp").sum())},
                 "panel": {x: sp[x] for x in ("ucp_seats", "efficiency_gap", "mean_median", "declination", "seats_at_50_50", "close4")},
                 "para167": {x: sr[x] for x in ("ucp_seats", "efficiency_gap", "mean_median", "declination", "seats_at_50_50", "close4")},
                 "ranks_set_D": ranks(k, rp)}
        rows, undecided = [], []
        for g in groups:
            lab = panel.copy()
            members = set(g["panel"])
            mask = panel.isin(members)
            lab[mask] = para[mask]
            s = score(v, lab)
            wp = tp.loc[g["panel"]]
            wr = tr.loc[g["para167"]]
            rows.append({"group": g["panel"], "para167": g["para167"],
                         "panel_ucp_ndp": [int((wp.winner == "ucp").sum()), int((wp.winner == "ndp").sum())],
                         "para167_ucp_ndp": [int((wr.winner == "ucp").sum()), int((wr.winner == "ndp").sum())],
                         "ucp_seats_if_only_this_group_is_undone": s["ucp_seats"],
                         "efficiency_gap_if_only_this_group_is_undone": s["efficiency_gap"]})
            for tbl, names, geoms, tag in ((tp, g["panel"], gdf_p, "panel"), (tr, g["para167"], gdf_r, "para167")):
                for n in names:
                    margin = float(abs(tbl.va_ucp[n] - tbl.va_ndp[n]))
                    cv = cut_votes(v, geoms[n])
                    if margin < cv:
                        undecided.append({"map": tag, "district": n, "winner": tbl.winner[n], "margin_votes": round(margin, 1),
                                          "margin_pts": round(float(tbl.margin_pts[n]), 2), "cut_votes": round(cv, 1)})
        block["groups"] = rows
        block["undecided"] = undecided
        block["districts_changed"] = {
            "panel": tp.loc[sorted(set(sum((g["panel"] for g in groups), [])))][["winner", "margin_pts"]].round(2).to_dict("index"),
            "para167": tr.loc[sorted(set(sum((g["para167"] for g in groups), [])))][["winner", "margin_pts"]].round(2).to_dict("index")}
        out[k] = block
    (HERE / "comparison.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf8")
    print(json.dumps({k: (out[k]["method_check_2019"], out[k]["panel"], out[k]["para167"]) for k in BALLOTS}, indent=0, default=float))
    print("VAs moved", out["vas_moved"], "groups", len(groups))
    for k in BALLOTS:
        print("==", k)
        for r in out[k]["groups"]:
            print(r)
        print("undecided", out[k]["undecided"])
        for m, x in out[k]["ranks_set_D"].items():
            if m != "n_plans":
                print(m, round(x["q50"], 4), x["iap_2026_assembled_v3"], x["para167_map"])


if __name__ == "__main__":
    main()
