# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
iap_reconstruction_check.py
---------------------------

Post-registration check of the assembled 91-district map (data/shapefiles/iap_assembled/), made
2026-11-05 after Step C had been run and seen. Unregistered; sensitivity only. The registered map
and the Step C reading stand unchanged.

Every district is checked against the panel's own evidence, not against the commission's map
(a changed district is meant to differ from it):

  1. Stated area   each district's area against Appendix 7 (whole km2, so +-0.5 km2). On the 57
                   districts copied from the majority map, the official areas sit within 0.5 km2 of
                   the stated figure in 56 cases (the 57th, Chestermere-Strathmore, is a real change).
  2. Unchanged     every VA the majority map puts (by representative point, the audit's
                   convention) in an unchanged district is in the same district here, and the
                   reverse.
  3. Pages         every VA in a placed district against the page polygons (C:/tmp/a10reg/pages):
                   agrees, contradicts, or has no accepted page (hole-filled districts).
  4. References    Fort McMurray-Lac La Biche and Fort McMurray-Wood Buffalo against their 2017
                   borders (the minority's text, PDF p126 para 24, says they return to them; the
                   stated areas match the 2017 areas); Edmonton-Meadows (40) and
                   Edmonton-Windermere (49) against the Version 4 placements (C:/tmp/a10test/v4),
                   which were made independently of the hole fill.

Correction (writes iap_2026_assembled_v2.gpkg): each unchanged district gets the official
majority geometry exactly (except a copied district whose stated area differs from the official
area by more than 0.5 km2: that is a real change, and it keeps its assembled geometry); any
area it held beyond that goes to the changed district it touches.
A correction that moves a VA's representative point is refused (exit 1).

Reads   data/shapefiles/iap_assembled/iap_2026_assembled.gpkg
        data/shapefiles/canonical/ea_majority_2026_eds.gpkg, va_2023_election_day_votes.gpkg
        data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
        data/iap/iap_app7_populations.csv
        findings/a10_stepb_run/va_assignment_real_map.csv
        C:/tmp/a10reg/pages/edNN.gpkg, C:/tmp/a10test/v4/ed40.gpkg, ed49.gpkg (not in the repo)
Writes  data/shapefiles/iap_assembled/iap_2026_assembled_v2.gpkg
        findings/iap_reconstruction_check/check.json

Usage: python -W ignore analysis/scripts/iap_reconstruction_check.py
"""
import json
import os
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ASM = ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled.gpkg"
OUT_GPKG = ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v2.gpkg"
OUT_JSON = ROOT / "findings/iap_reconstruction_check/check.json"
MAJ = ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"
VAS = ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg"
ED2017 = ROOT / "data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp"
APP7 = ROOT / "data/iap/iap_app7_populations.csv"
ASSIGN = ROOT / "findings/a10_stepb_run/va_assignment_real_map.csv"
PAGES = Path("C:/tmp/a10reg/pages")
V4 = Path("C:/tmp/a10test/v4")
CRS = 3400


def iou(a, b):
    return a.intersection(b).area / a.union(b).area


def rep_assign(points, districts, col):
    j = gpd.sjoin(points, districts[[col, "geometry"]], predicate="within")
    return j.groupby("OBJECTID")[col].first()


def main():
    I = gpd.read_file(ASM)
    M = gpd.read_file(MAJ).set_index("EDName2025")
    app7 = pd.read_csv(APP7).set_index("ed_number")
    V = gpd.read_file(VAS)
    V["votes"] = V.va_ndp + V.va_ucp + V.va_other
    P = V[["OBJECTID", "votes"]].copy()
    P = gpd.GeoDataFrame(P, geometry=V.representative_point(), crs=CRS)
    A = pd.read_csv(ASSIGN).set_index("OBJECTID")
    known = set(I.loc[I.source == "known", "district"])
    # a copied district whose stated area is not the official one is a real change in unpopulated
    # land (same population); it keeps its assembled geometry
    st = I.set_index("district").ed.map(app7.area_km2)
    real = {n for n in known if abs(M.loc[n].geometry.area / 1e6 - st[n]) > 0.5}
    out = {"copied_but_area_changed": sorted(real)}
    fixed = known - real

    # 2. unchanged districts, VA by VA
    maj_of = rep_assign(P, M.reset_index(), "EDName2025")
    d = A.join(maj_of.rename("maj"))
    bad = d[(d.maj.isin(known) | d.district.isin(known)) & (d.district != d.maj)]
    out["unchanged_va_mismatches"] = bad[["VA_NUMBER", "district", "maj"]].reset_index().to_dict("records")

    # correction: official geometry for every unchanged district, overflow to the changed neighbour
    G = I.set_index("district").geometry.copy()
    moved = []
    for n in sorted(fixed):
        extra = G[n].difference(M.loc[n].geometry)
        G[n] = M.loc[n].geometry
        for q in gpd.GeoSeries([extra], crs=CRS).explode(index_parts=False):
            if q.is_empty or q.area < 1.0:
                continue
            nb = [x for x in G.index if x not in fixed and G[x].intersection(q.buffer(1)).area > 0]
            to = max(nb, key=lambda x: G[x].intersection(q.buffer(1)).area) if nb else None
            if to is None:
                continue
            G[to] = G[to].union(q)
            moved.append({"from": n, "to": to, "km2": round(q.area / 1e6, 4)})
    big = [m for m in moved if m["km2"] >= 0.01]
    out["correction_pieces_ge_0_01_km2"] = big
    out["correction_pieces_total"] = len(moved)
    v2 = I.copy()
    v2["geometry"] = v2.district.map(G)
    v2 = gpd.GeoDataFrame(v2, geometry="geometry", crs=CRS)
    before = rep_assign(P, I, "district")
    after = rep_assign(P, v2, "district")
    changed = (before != after.reindex(before.index)).sum()
    out["vas_changed_by_correction"] = int(changed)
    if changed:
        print(f"FAIL: the correction moves {changed} VAs; nothing written")
        sys.exit(1)

    # 1. stated area, before and after
    rows = []
    for _, r in v2.iterrows():
        st = float(app7.loc[r.ed, "area_km2"])
        a0 = I.loc[I.district == r.district].geometry.iloc[0].area / 1e6
        rows.append({"ed": int(r.ed), "district": r.district, "source": r.source, "stated_km2": st,
                     "v1_km2": round(a0, 2), "v2_km2": round(r.geometry.area / 1e6, 2),
                     "v1_off": round(a0 - st, 2), "v2_off": round(r.geometry.area / 1e6 - st, 2)})
    area = pd.DataFrame(rows)
    out["stated_area"] = {"v1_outside_0_5": int((area.v1_off.abs() > 0.5).sum()),
                          "v2_outside_0_5": int((area.v2_off.abs() > 0.5).sum()),
                          "v2_outside": area[area.v2_off.abs() > 0.5].to_dict("records")}

    # 3. placed districts, VA by VA against the page polygons
    src = I.set_index("ed").source
    pg = []
    for ed in I.ed:
        f = PAGES / f"ed{ed:02d}.gpkg"
        if src[ed] == "placed" and f.exists():
            pg.append((ed, gpd.read_file(f).to_crs(CRS).union_all()))
    pgs = gpd.GeoDataFrame({"page_ed": [e for e, _ in pg]}, geometry=[g for _, g in pg], crs=CRS)
    claims = gpd.sjoin(P, pgs, predicate="within").groupby("OBJECTID").page_ed.apply(set)
    ch = A[A.ed.map(src) != "known"].join(claims.rename("pages")).join(P.set_index("OBJECTID").votes)

    def status(r):
        p = r.pages if isinstance(r.pages, set) else set()
        if not p:
            return "no accepted page"
        if r.ed in p:
            return "agrees" if len(p) == 1 else "agrees, overlaps another page"
        return "contradicts"
    ch["status"] = ch.apply(status, axis=1)
    out["pages"] = {s: {"vas": int(len(g)), "votes": round(float(g.votes.sum()))}
                    for s, g in ch.groupby("status")}
    out["pages_no_accepted_page_by_district"] = ch[ch.status == "no accepted page"].groupby("district").size().to_dict()

    # 4. outside references
    E = gpd.read_file(ED2017).to_crs(CRS).set_index("EDName2017")
    Gv2 = v2.set_index("district").geometry
    out["fort_mcmurray_vs_2017"] = {n: round(iou(Gv2[n], E.loc[n].geometry), 5)
                                    for n in ["Fort McMurray-Lac La Biche", "Fort McMurray-Wood Buffalo"]}
    v4 = {}
    for ed in (40, 49):
        f = V4 / f"ed{ed:02d}.gpkg"
        if not f.exists():
            continue
        g4 = gpd.read_file(f).to_crs(CRS).union_all()
        n = I.loc[I.ed == ed, "district"].iloc[0]
        in4 = set(P[P.within(g4)].OBJECTID)
        ours = set(after[after == n].index)
        v4[n] = {"iou_v1": round(iou(I.loc[I.ed == ed].geometry.iloc[0], g4), 4),
                 "iou_v2": round(iou(Gv2[n], g4), 4),
                 "vas_only_ours": len(ours - in4), "vas_only_v4": len(in4 - ours)}
    out["version4_vs_hole_fill"] = v4

    OUT_GPKG.parent.mkdir(parents=True, exist_ok=True)
    if OUT_GPKG.exists():
        os.remove(OUT_GPKG)
    v2.to_file(OUT_GPKG, driver="GPKG")
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("vas_changed_by_correction", "correction_pieces_ge_0_01_km2",
                                          "unchanged_va_mismatches", "pages", "fort_mcmurray_vs_2017",
                                          "version4_vs_hole_fill")}, indent=1, default=str))
    print("stated area outside +-0.5 km2: v1", out["stated_area"]["v1_outside_0_5"],
          "v2", out["stated_area"]["v2_outside_0_5"])


if __name__ == "__main__":
    main()
