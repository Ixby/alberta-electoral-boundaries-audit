# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
build_para167.py

Builds the 91 divisions the panel minority lists at para 167 (IAP report, PDF pp. 161-163), as set
out in preregistration/r5_comparator_2026-11-07.md. Unregistered; rests on the v3 reconstruction.
Holds no votes: the fit check and the map come first, and no seat or vote figure is read here.

Reads   evidence/legislature/iap_report_2026_hires_text/p161-p163.txt
        data/shapefiles/canonical/ea_majority_2026_eds.gpkg
        data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg
        data/shapefiles/reference/alberta_2021_csds.gpkg
        data/shapefiles/derived/va_polygons_with_2023_votes.gpkg (VA polygons), data/va_pop_from_das.csv
Writes  findings/iap_para167/para167_map.gpkg, fit_check.json, va_assignment.csv

Usage: python -W ignore findings/iap_para167/build_para167.py
"""
import json
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TXT = ROOT / "evidence/legislature/iap_report_2026_hires_text"
MAJ = ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"
V3 = ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg"
CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
VAS = ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
APP7 = ROOT / "data/iap/iap_app7_populations.csv"
HEADS = ("As Mapped by the ABEBC Majority Final Report:", "As Mapped by the ABEBC Interim Report:",
         "As Mapped in the IAP Majority Report, for a Unanimous IAP:",
         "Where We Recommend Minor Amendments that Can Be Easily Described:")
MIN_PIECE_M2 = 1e5  # 0.1 km2, the plan's reporting floor


def read_list():
    txt = "".join((TXT / f"p{p}.txt").read_text(encoding="utf8") for p in (161, 162, 163))
    parts = re.split("|".join(map(re.escape, HEADS)), txt)[1:]
    out = [[x.strip() for x in re.findall(r"^\s*\d+\)\s+([^\n(:]+)", s, flags=re.M)] for s in parts]
    assert [len(x) for x in out] == [68, 8, 12, 3], [len(x) for x in out]
    return out


def main():
    maj_list, interim, iap, amended = read_list()
    assert amended == ["Canmore-Banff", "Blackfalds-Innisfail", "Olds-Didsbury-Three Hills"]
    M = gpd.read_file(MAJ).to_crs(3400).set_index("EDName2025").geometry
    G = gpd.read_file(V3).to_crs(3400).set_index("district").geometry
    csd = gpd.read_file(CSD).to_crs(3400)
    wheat = csd[csd.CSDNAME.str.contains("Wheatland")]
    print("Wheatland CSDs:", wheat.CSDNAME.tolist())

    geom = {n: M[n] for n in maj_list}
    geom.update({n: G[n] for n in interim + iap})
    geom["Canmore-Banff"] = M["Canmore-Banff"].difference(G["Rocky Mountain House-Sundre"])
    geom["Blackfalds-Innisfail"] = G["Blackfalds-Innisfail"].difference(unary_union([M["Red Deer-North"], M["Red Deer-South"]]))
    geom["Olds-Didsbury-Three Hills"] = G["Olds-Didsbury-Three Hills"].difference(unary_union(wheat.geometry.values))
    assert len(geom) == 91
    source = {**{n: "majority" for n in maj_list}, **{n: "interim_via_v3" for n in interim},
              **{n: "iap_v3" for n in iap}, **{n: "amended" for n in amended}}

    # Fit check: every overlap and gap over the floor, in area and VAs.
    va = gpd.read_file(VAS).to_crs(3400)
    pop_col = "pop_2021"
    popdf = pd.read_csv(ROOT / "data/va_pop_from_das.csv").set_index("va_row_idx")[pop_col]
    va[pop_col] = pd.Series(va.index.map(popdf).values).fillna(0.0).clip(lower=1.0).values
    pts = va[["geometry"]].copy()
    pts["geometry"] = va.geometry.representative_point()
    gdf = gpd.GeoDataFrame({"district": list(geom), "source": [source[n] for n in geom]},
                           geometry=list(geom.values()), crs=3400)
    j = gpd.sjoin(pts, gdf[["district", "geometry"]], how="left", predicate="within")
    hits = j.groupby(level=0)["district"].apply(lambda s: [x for x in s if isinstance(x, str)])

    def largest(i, names):
        return max(names, key=lambda n: va.geometry[i].intersection(geom[n]).area)

    assign, overlap_rows, gap_rows = {}, [], []
    near = gdf.sindex
    for i, names in hits.items():
        if len(names) == 1:
            assign[i] = names[0]
        elif len(names) > 1:
            on_list = [n for n in names if source[n] == "majority"]
            pick = on_list[0] if len(on_list) == 1 else largest(i, names)
            assign[i] = pick
            overlap_rows.append({"va": int(i), "claimed_by": names, "assigned": pick, "pop": float(va.loc[i, pop_col])})
        else:
            cand = gdf.iloc[near.query(va.geometry[i], predicate="intersects")].district.tolist()
            pick = largest(i, cand) if cand else None
            assign[i] = pick
            gap_rows.append({"va": int(i), "touches": cand, "assigned": pick, "pop": float(va.loc[i, pop_col])})
    total = float(va[pop_col].sum())
    a = pd.Series(assign, name="district").reindex(va.index)
    pop = va[pop_col].groupby(a).sum()

    pieces = []
    names = list(geom)
    for x in range(len(names)):
        for y in near.query(geom[names[x]], predicate="intersects"):
            if y > x:
                ov = geom[names[x]].intersection(geom[names[y]])
                if ov.area > MIN_PIECE_M2:
                    pieces.append({"a": names[x], "b": names[y], "src": [source[names[x]], source[names[y]]],
                                   "km2": round(ov.area / 1e6, 3)})
    union = unary_union(list(geom.values()))
    alberta = unary_union(list(M.values))
    gaps = alberta.difference(union)
    gap_list = sorted((round(g.area / 1e6, 3) for g in getattr(gaps, "geoms", [gaps]) if g.area > MIN_PIECE_M2), reverse=True)

    stated = pd.read_csv(APP7).set_index("district").population
    maj_pop = gpd.read_file(MAJ).set_index("EDName2025").PopCensus
    rows = []
    for n in geom:
        s = maj_pop[n] if source[n] == "majority" else stated.get(n)
        rows.append({"district": n, "source": source[n], "stated_pop": None if pd.isna(s) else int(s),
                     "rebuilt_overlay_pop": round(float(pop.get(n, 0))), "km2": round(geom[n].area / 1e6, 1)})
    report = {"n_districts": len(geom), "pop_col": pop_col, "total_overlay_pop": total,
              "stated_total_on_list": int(sum(r["stated_pop"] or 0 for r in rows)),
              "stated_total_app7": int(stated.sum()),
              "polygon_overlaps_over_0_1km2": sorted(pieces, key=lambda p: -p["km2"]),
              "polygon_gaps_km2": gap_list,
              "va_points_in_two": overlap_rows, "va_points_in_none": gap_rows,
              "pop_in_overlaps": sum(r["pop"] for r in overlap_rows), "pop_in_gaps": sum(r["pop"] for r in gap_rows),
              "share_of_population_resolved": (sum(r["pop"] for r in overlap_rows) + sum(r["pop"] for r in gap_rows)) / total,
              "districts": rows}
    (HERE / "fit_check.json").write_text(json.dumps(report, indent=1, default=float), encoding="utf8")
    pd.DataFrame({"va_index": va.index, "district": a.values}).to_csv(HERE / "va_assignment.csv", index=False)
    # The map file holds no overlaps, so anything placing VAs by representative point agrees with the
    # assignment above. High River-Vulcan-Siksika is on the majority list (the plan's rule); West Yellowhead
    # is the unanimous panel's line, and Canmore-Banff is defined by what that panel moved.
    out = dict(geom)
    out["Olds-Didsbury-Three Hills"] = out["Olds-Didsbury-Three Hills"].difference(out["High River-Vulcan-Siksika"])
    out["Canmore-Banff"] = out["Canmore-Banff"].difference(out["West Yellowhead"])
    res = gpd.GeoDataFrame({"district": list(out), "EDName2025": list(out), "source": [source[n] for n in out]},
                           geometry=list(out.values()), crs=3400)
    res.to_file(HERE / "para167_map.gpkg", driver="GPKG")
    jr = gpd.sjoin(pts, res[["district", "geometry"]], how="left", predicate="within")
    jr = jr[~jr.index.duplicated(keep="first")]["district"].reindex(va.index)
    n_diff = int((jr.values != a.values).sum())
    print("VAs where the map file and the plan's assignment disagree:", n_diff)
    assert n_diff == 0
    print({k: report[k] for k in ("total_overlay_pop", "stated_total_on_list", "stated_total_app7", "pop_in_overlaps", "pop_in_gaps", "share_of_population_resolved")})
    print("overlaps", len(pieces), sorted(pieces, key=lambda p: -p["km2"])[:15])
    print("gaps km2", gap_list[:15], "VAs in two", len(overlap_rows), "VAs in none", len(gap_rows))
    print(pd.DataFrame(rows).assign(diff=lambda d: d.rebuilt_overlay_pop - d.stated_pop).sort_values("diff", key=abs, ascending=False).head(14).to_string())


if __name__ == "__main__":
    main()
