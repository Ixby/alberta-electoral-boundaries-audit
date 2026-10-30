# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
score_x1.py
-----------

Test X1 (Recommendation 5) for a proposed map, per Amendments 16 and 17.

  (a), (b)  every majority division named in the condition
            (viewer/static/mapdata/lunty_bounds.json) is unchanged: one district
            of the new map holds >= 99% of its 2021 population and that
            district's population is >= 99% from the majority division.
  (c)       the same test against the October 2025 interim map's Edmonton
            divisions south of the river, if --interim is given; otherwise
            "not scored".
  (d)       "adopted" when a district of the new map has >= 50% of its
            population inside the Clearwater County + western Mountain View
            County zone (built as in build_lunty_bounds.py). "Considered with a
            stated reason" and "not shown" come from the committee's report and
            are entered by hand (--d-record).
  rest      the share of the 27 majority divisions outside (a)-(c) that come
            back unchanged (reported, not gating).
  X1        met only if (a), (b) and (c) are met and (d) is adopted or
            considered with a stated reason; "not determinable" when (c) is not
            scored and nothing else fails.

Population is the VA-level 2021 census overlay the canonical ensemble uses
(data/va_pop_from_das.csv); VAs are assigned by representative point.

Usage
  python analysis/scripts/score_x1.py --map PATH [--name-col COL]
         [--interim PATH --interim-name-col COL] [--d-record considered|not_shown]
         [--out results.json]
"""
import argparse
import json
import sys
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
CSD = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"
E19 = REPO / "data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp"
BOUNDS = REPO / "viewer/static/mapdata/lunty_bounds.json"
THRESH = 0.99


def assign(points, gpkg, col):
    g = gpd.read_file(gpkg).to_crs(points.crs)
    j = gpd.sjoin(points[["geometry"]], g[[col, "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(points.index)
    return j[col].fillna("__unassigned__")


def unchanged(old, new, pop, names):
    """For each old division in names: (best new district, share of old in it, share of it from old, unchanged?)."""
    df = pd.DataFrame({"old": old.values, "new": new.values, "pop": pop})
    cross = df.groupby(["old", "new"])["pop"].sum()
    old_tot = df.groupby("old")["pop"].sum()
    new_tot = df.groupby("new")["pop"].sum()
    out = []
    for n in names:
        if n not in cross.index.get_level_values(0):
            out.append({"division": n, "best": None, "share_of_old": 0.0, "share_of_new": 0.0, "unchanged": False})
            continue
        row = cross.loc[n]
        best = row.idxmax()
        a, b = row[best] / old_tot[n], row[best] / new_tot[best]
        out.append({"division": n, "best": best, "share_of_old": round(float(a), 4),
                    "share_of_new": round(float(b), 4), "unchanged": bool(a >= THRESH and b >= THRESH)})
    return out


def zone_d(crs):
    csd = gpd.read_file(CSD)
    e19 = gpd.read_file(E19)
    def g(name):
        return csd[csd["CSDNAME"] == name].to_crs(3400).geometry.iloc[0]
    rmh = e19[e19["EDName2017"] == "Rimbey-Rocky Mountain House-Sundre"].to_crs(3400).geometry.iloc[0]
    z = unary_union([g("Clearwater County"), g("Mountain View County").intersection(rmh)])
    return gpd.GeoSeries([z], crs=3400).to_crs(crs).iloc[0]


def main(a):
    va, graph = me.build_va_graph(verbose=False)
    nodes = sorted(graph.nodes())
    pop = np.array([graph.nodes[n]["pop_2021"] for n in nodes], float)
    pts = va.loc[nodes].copy()
    pts["geometry"] = pts.geometry.representative_point()
    zones = {z["cond"]: z["eds"] for z in json.loads(BOUNDS.read_text())["zones"]}
    old = assign(pts, MAJ, "EDName2025")
    new = assign(pts, Path(a.map), a.name_col)
    res = {"map": str(a.map), "threshold": THRESH}
    for c in ("a", "b"):
        rows = unchanged(old, new, pop, zones[c])
        res[c] = {"met": all(r["unchanged"] for r in rows), "n": len(rows),
                  "n_unchanged": sum(r["unchanged"] for r in rows), "divisions": rows}
    if a.interim:
        interim = assign(pts, Path(a.interim), a.interim_name_col)
        if a.interim_south:
            south = a.interim_south
        else:  # interim divisions with >= 50% of their population in the majority's zone-(c) divisions
            t = pd.DataFrame({"i": interim.values, "inc": old.isin(zones["c"]).values, "pop": pop})
            f = t.assign(p=t["pop"] * t["inc"]).groupby("i")[["p", "pop"]].sum()
            south = sorted(f.index[(f["p"] / f["pop"]) >= 0.5])
        rows = unchanged(interim, new, pop, south)
        res["c"] = {"met": all(r["unchanged"] for r in rows), "n": len(rows),
                    "n_unchanged": sum(r["unchanged"] for r in rows), "divisions": rows,
                    "note": "interim divisions tested: " + ", ".join(south)}
    else:
        res["c"] = {"met": None, "note": "not scored: October 2025 interim map not supplied"}
    zd = zone_d(pts.crs)
    in_d = pts.geometry.within(zd).to_numpy()
    df = pd.DataFrame({"new": new.values, "pop": pop, "in_d": in_d})
    share = df.assign(p_in=df["pop"] * df["in_d"]).groupby("new")[["p_in", "pop"]].sum()
    share["frac"] = share["p_in"] / share["pop"]
    best = share["frac"].idxmax()
    adopted = bool(share.loc[best, "frac"] >= 0.5)
    d_state = "adopted" if adopted else (a.d_record or "not_shown")
    res["d"] = {"state": d_state, "best_district": best, "best_share_in_zone": round(float(share.loc[best, "frac"]), 4)}
    rest_names = sorted(set(old) - set(zones["a"]) - set(zones["b"]) - set(zones["c"]) - {"__unassigned__"})
    rows = unchanged(old, new, pop, rest_names)
    res["rest"] = {"n": len(rows), "n_unchanged": sum(r["unchanged"] for r in rows), "divisions": rows}
    fails = [c for c in ("a", "b", "c") if res[c].get("met") is False]
    d_ok = d_state in ("adopted", "considered")
    if fails or not d_ok:
        x1 = "not met"
    elif res["c"]["met"] is None:
        x1 = "not determinable"
    else:
        x1 = "met"
    res["X1"] = x1
    res["failing"] = fails + ([] if d_ok else ["d"])
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1))
    print(f"X1: {x1}  |  (a) {res['a']['n_unchanged']}/{res['a']['n']}  (b) {res['b']['n_unchanged']}/{res['b']['n']}  "
          f"(c) {res['c'].get('n_unchanged', '-')}/{res['c'].get('n', '-')} {'' if res['c']['met'] is not None else '(not scored)'}  "
          f"(d) {d_state} [{best}: {res['d']['best_share_in_zone']:.0%} in zone]  rest {res['rest']['n_unchanged']}/{res['rest']['n']}")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True)
    ap.add_argument("--name-col", default="EDName2025")
    ap.add_argument("--interim")
    ap.add_argument("--interim-name-col", default="EDName2025")
    ap.add_argument("--interim-south", nargs="*", help="interim divisions south of the river (default: those with >= 50%% of their population in the majority's zone-(c) divisions)")
    ap.add_argument("--d-record", choices=["considered", "not_shown"], help="from the committee's report, if (d) is not adopted")
    ap.add_argument("--out")
    main(ap.parse_args())
