# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence) | Government of Alberta (OGL-Alberta)
"""
signals_a_to_e.py

Signals A-E of preregistration/six_signals_2026-11-07.md: other elections and swing, reserve and
settlement splits, city treatment, incumbents (coarse), and growth to 2031 (trend). Unregistered.
Applies no test of intent and no legal test.

Reads   data/shapefiles/derived/va_polygons_with_{2015,2019,2023}_votes.gpkg, va_polygons_all_2023_ballots_primary.gpkg
        map files as in findings/packing_cracking/real_maps.py; data/va_pop_from_das.csv
        data/shapefiles/reference/alberta_2021_csds.gpkg, alberta_2021_das.gpkg; data/census_2021/alberta_da_profile.csv
        data/reference/alberta_2021_csd_populations.csv, alberta_2023_results.csv, alberta_byelections_2019_2026.csv
        data/osi/population-estimates-ab-census-subdivision-municipal-2016-to-current.xlsx
        data/iap/iap_app7_populations.csv; findings/iap_para167/comparison.json
Writes  findings/six_signals/signals_a_to_e.json

Usage: python -W ignore findings/six_signals/signals_a_to_e.py
"""
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "findings/packing_cracking"))
from real_maps import MAPS, NEAR, area, assign  # noqa: E402

DER = ROOT / "data/shapefiles/derived"
VOTES = {"2015": DER / "va_polygons_with_2015_votes.gpkg", "2019": DER / "va_polygons_with_2019_votes.gpkg",
         "2023": DER / "va_polygons_with_2023_votes.gpkg", "2023_all": DER / "va_polygons_all_2023_ballots_primary.gpkg"}
CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
DAS = ROOT / "data/shapefiles/reference/alberta_2021_das.gpkg"
LETHBRIDGE = "4802012"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def seats(lab, u, n):
    t = pd.DataFrame({"d": lab, "u": u, "n": n}).groupby("d")[["u", "n"]].sum()
    return t, int((t.n > t.u).sum())


def eg(t):
    tot = t.u + t.n
    half = tot / 2
    w_n = np.where(t.n > t.u, t.n - half, t.n).sum()
    w_u = np.where(t.u >= t.n, t.u - half, t.u).sum()
    return round(100 * float((w_n - w_u) / tot.sum()), 2)


def csd_estimates():
    z = zipfile.ZipFile(ROOT / "data/osi/population-estimates-ab-census-subdivision-municipal-2016-to-current.xlsx")
    ss = ["".join(t.text or "" for t in si.iter(NS + "t")) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si")]
    rows = []
    for r in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS + "row"):
        row = {}
        for c in r.findall(NS + "c"):
            v = c.find(NS + "v")
            row[re.match(r"[A-Z]+", c.get("r")).group(0)] = ss[int(v.text)] if c.get("t") == "s" and v is not None else (v.text if v is not None else "")
        rows.append(row)
    hdr = next(i for i, r in enumerate(rows) if r.get("B") == "Census Subdivision")
    cols = {v: k for k, v in rows[hdr].items()}
    num = re.compile(r"\d+(\.\d+)?")
    out = {}
    for r in rows[hdr + 1:]:
        a, b = str(r.get(cols["2021"], "")), str(r.get(cols["2025"], ""))
        if re.fullmatch(r"48\d{5}", str(r.get("B", ""))) and num.fullmatch(a) and num.fullmatch(b) and float(a) > 0 and float(b) > 0:
            out[r["B"]] = (float(b) / float(a)) ** 0.25 - 1
    return pd.Series(out)


def main():
    base = gpd.read_file(VOTES["2023"]).to_crs(3400)
    pts = base[["geometry"]].copy()
    pts["geometry"] = base.geometry.representative_point()
    labels = {k: assign(pts, f, col) for k, (f, col) in MAPS.items()}
    pop = pd.read_csv(ROOT / "data/va_pop_from_das.csv").set_index("va_row_idx")["pop_2021"]
    vpop = pd.Series(base.index.map(pop).values).fillna(0.0).clip(lower=1.0).to_numpy()
    csd = gpd.read_file(CSD).to_crs(3400)
    j = gpd.sjoin(pts, csd[["CSDUID", "CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    va_csd = j.CSDUID.astype(str).to_numpy()
    leth = va_csd == LETHBRIDGE
    comp = json.loads((ROOT / "findings/iap_para167/comparison.json").read_text())
    south = labels["panel"].isin(next(g for g in comp["groups"] if "Lethbridge" in g["panel"])["panel"]).to_numpy()
    out = {"plan": "preregistration/six_signals_2026-11-07.md"}

    # A. Other elections and swing
    A = {}
    votes = {}
    for y, f in VOTES.items():
        v = gpd.read_file(f, ignore_geometry=True)
        assert (v.OBJECTID.values == base.OBJECTID.values).all(), y
        votes[y] = (v.va_ucp.to_numpy(float), v.va_ndp.to_numpy(float))
        u, n = votes[y]
        blk = {"ndp_two_party_pct": round(100 * float(n.sum() / (u.sum() + n.sum())), 2)}
        for k, lab in labels.items():
            t, s = seats(lab.values, u, n)
            blk[k] = {"ndp_seats": s, "seats": int(len(t)), "efficiency_gap_pct": eg(t),
                      "lethbridge": area(lab.values, u, n, leth), "south_group": area(lab.values, u, n, south)}
        blk["panel_minus_para167_ndp_seats"] = blk["panel"]["ndp_seats"] - blk["para167"]["ndp_seats"]
        A[y] = blk
    u, n = votes["2023_all"]
    curve = []
    for d in np.arange(-0.10, 0.1001, 0.005):
        row = {"ndp_swing_pts": round(100 * d, 1)}
        flips = {}
        for k, lab in labels.items():
            t = pd.DataFrame({"d": lab.values, "u": u, "n": n}).groupby("d")[["u", "n"]].sum()
            sh = t.n / (t.u + t.n) + d
            row[k] = int((sh > 0.5).sum())
            flips[k] = set(sh.index[sh > 0.5])
        row["panel_minus_para167"] = row["panel"] - row["para167"]
        curve.append(row)
    A["swing_2023_all_ballots"] = curve
    diffs = [r["panel_minus_para167"] for r in curve]
    A["swing_summary"] = {"steps": len(diffs), "panel_fewer_ndp": sum(x < 0 for x in diffs), "equal": sum(x == 0 for x in diffs),
                          "panel_more_ndp": sum(x > 0 for x in diffs), "min": min(diffs), "max": max(diffs)}
    out["A_elections_and_swing"] = A
    print("A", {y: (A[y]["ndp_two_party_pct"], {k: A[y][k]["ndp_seats"] for k in labels}, A[y]["panel_minus_para167_ndp_seats"]) for y in VOTES}, A["swing_summary"])

    # B. Reserves and settlements split
    res = csd[csd.CSDTYPE.isin(["IRI"]) | csd.CSDTYPE.str.startswith("S-")].copy()
    cpop = pd.read_csv(ROOT / "data/reference/alberta_2021_csd_populations.csv", dtype={"ALT_GEO_CODE": str}).set_index("ALT_GEO_CODE").population_2021
    res["pop_2021"] = res.CSDUID.astype(str).map(cpop).fillna(0)
    res["a"] = res.geometry.area
    B = {}
    for k, (f, col) in MAPS.items():
        eds = gpd.read_file(f).to_crs(3400)[[col, "geometry"]]
        ov = gpd.overlay(res[["CSDUID", "CSDNAME", "CSDTYPE", "pop_2021", "a", "geometry"]], eds, how="intersection", keep_geom_type=True)
        ov["share"] = ov.geometry.area / ov.a
        held = ov[ov.share >= 0.01].groupby(["CSDUID", "CSDNAME", "CSDTYPE", "pop_2021"])[col].apply(lambda s: sorted(set(s)))
        split = held[held.map(len) > 1]
        B[k] = {"n_reserves_settlements": int(len(res)), "n_split": int(len(split)),
                "pop_2021_in_split": int(sum(i[3] for i in split.index)),
                "split": {f"{i[1]} ({i[2]})": v for i, v in split.items()}}
    out["B_reserves_settlements"] = B
    print("B", {k: (v["n_split"], v["pop_2021_in_split"]) for k, v in B.items()})

    # C. City treatment
    cities = csd[(csd.CSDTYPE == "CY")].copy()
    cities["pop"] = cities.CSDUID.astype(str).map(cpop)
    cities = cities[cities["pop"] >= 20000]
    C = {}
    for k, lab in labels.items():
        lab_v = lab.values
        dpop = pd.Series(vpop).groupby(lab_v).sum()
        avg = dpop.mean()
        rows = {}
        for _, c in cities.iterrows():
            m = va_csd == str(c.CSDUID)
            by = pd.Series(vpop[m]).groupby(lab_v[m]).sum()
            tp = by.sum()
            pieces = by[by >= 0.02 * tp]
            minority_in = sum(by[d] for d in pieces.index if by[d] < 0.5 * dpop[d])
            rows[c.CSDNAME] = {"pop_2021": int(c["pop"]), "divisions": int(len(pieces)), "justified": int(math.ceil(tp / (1.25 * avg))),
                               "share_in_divisions_where_city_is_minority": round(float(minority_in / tp), 3)}
        C[k] = rows
    out["C_cities"] = C
    print("C panel", {n: (v["divisions"], v["justified"], v["share_in_divisions_where_city_is_minority"]) for n, v in C["panel"].items()})

    # D. Incumbents (coarse)
    r23 = pd.read_csv(ROOT / "data/reference/alberta_2023_results.csv")
    member = dict(zip(r23.ed_name, r23.winner_party))
    by = pd.read_csv(ROOT / "data/reference/alberta_byelections_2019_2026.csv")
    by = by[pd.to_datetime(by.date) > "2023-05-29"]
    later = {}
    for (dt, riding), g in by.groupby(["date", "riding"]):
        w = g.sort_values("votes", ascending=False).iloc[0]
        later[riding] = (dt, w.party)
    for riding, (dt, party) in sorted(later.items(), key=lambda x: x[1][0]):
        member[riding] = party
    old = base.parent_ed_2019.values
    D = {"byelections_applied": {k: v for k, v in later.items()}, "unmatched_old_divisions": sorted(set(old) - set(member))}
    ua, na = votes["2023_all"]
    for k, lab in labels.items():
        t, _ = seats(lab.values, ua, na)
        winner = (t.n > t.u).map({True: "NDP", False: "UCP"})
        succ = pd.DataFrame({"old": old, "new": lab.values, "p": vpop}).groupby(["old", "new"]).p.sum().reset_index()
        succ = succ.sort_values("p").groupby("old").tail(1).set_index("old").new
        placed = pd.DataFrame({"member_party": pd.Series(member).reindex(succ.index).str.upper().str[:3], "new": succ})
        placed["new_winner"] = placed.new.map(winner)
        pairs = placed.groupby("new").filter(lambda g: len(g) > 1)
        D[k] = {"pairings": {n: sorted(f"{o} ({p})" for o, p in zip(g.index, g.member_party)) for n, g in pairs.groupby("new")},
                "members_in_seat_other_party_carries": {p: int(((placed.member_party == p) & (placed.new_winner != p)).sum()) for p in ("NDP", "UCP")},
                "names_ndp_in_ucp_seat": sorted(placed.index[(placed.member_party == "NDP") & (placed.new_winner == "UCP")]),
                "names_ucp_in_ndp_seat": sorted(placed.index[(placed.member_party == "UCP") & (placed.new_winner == "NDP")])}
    out["D_incumbents"] = D
    print("D", {k: (len(D[k]["pairings"]), D[k]["members_in_seat_other_party_carries"], D[k]["names_ndp_in_ucp_seat"]) for k in labels})

    # E. Growth to 2031 (trend)
    g = csd_estimates()
    da = gpd.read_file(DAS).to_crs(3400)
    da["DAUID"] = da.DAUID.astype(str)
    prof = pd.read_csv(ROOT / "data/census_2021/alberta_da_profile.csv", dtype={"DAUID": str}).set_index("DAUID")
    dpts = da[["DAUID", "geometry"]].copy()
    dpts["geometry"] = da.geometry.representative_point()
    jj = gpd.sjoin(dpts, csd[["CSDUID", "geometry"]], how="left", predicate="within")
    jj = jj[~jj.index.duplicated(keep="first")].reindex(dpts.index)
    dg = jj.CSDUID.astype(str).map(g).fillna(float(g.median())).to_numpy()
    dp = prof.pop_2021.reindex(da.DAUID).fillna(0).to_numpy()
    stated = {"panel": pd.read_csv(ROOT / "data/iap/iap_app7_populations.csv").set_index("district").population}
    for k in ("majority", "minority"):
        stated[k] = gpd.read_file(MAPS[k][0], ignore_geometry=True).set_index("EDName2025").PopCensus
    E = {}
    for k in ("majority", "minority", "panel"):
        f, col = MAPS[k]
        eds = gpd.read_file(f).to_crs(3400)[[col, "geometry"]]
        jd = gpd.sjoin(dpts, eds, how="left", predicate="within")
        jd = jd[~jd.index.duplicated(keep="first")].reindex(dpts.index)[col].to_numpy()
        w = pd.DataFrame({"d": jd, "p": dp, "pg": dp * dg}).groupby("d")[["p", "pg"]].sum()
        rate = (w.pg / w.p).reindex(stated[k].index)
        p31 = stated[k] * (1 + rate) ** 7
        dev = 100 * (p31 / p31.mean() - 1)
        t, _ = seats(labels[k].values, ua, na)
        ndp_sh = (t.n / (t.u + t.n)).reindex(stated[k].index)
        E[k] = {"beyond_25_in_2031": {n: round(float(x), 1) for n, x in dev[dev.abs() > 25].items()},
                "within_10_in_2031": int((dev.abs() <= 10).sum()), "stated_within_10": int((100 * (stated[k] / stated[k].mean() - 1)).abs().le(10).sum()),
                "corr_growth_vs_ndp_share": round(float(np.corrcoef(rate, ndp_sh)[0, 1]), 3),
                "fastest": {n: round(100 * float(x), 2) for n, x in rate.sort_values().tail(6).items()},
                "slowest": {n: round(100 * float(x), 2) for n, x in rate.sort_values().head(4).items()}}
    out["E_growth_2031_trend"] = E
    print("E", {k: (len(v["beyond_25_in_2031"]), v["within_10_in_2031"], v["stated_within_10"], v["corr_growth_vs_ndp_share"]) for k, v in E.items()})
    (HERE / "signals_a_to_e.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf8")


if __name__ == "__main__":
    main()
