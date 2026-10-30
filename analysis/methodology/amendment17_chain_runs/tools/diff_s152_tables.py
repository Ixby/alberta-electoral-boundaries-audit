"""District-level diff of the two s.15(2) criteria tables on the three real maps.

Registered table (s15_2_va_criteria.csv) is scored with the Audit session's own
criteria(); the cross-check table (s152_va_criteria.csv, s152_criteria.py) with its
own predicates: (a) area > 20,000 km2, (b) min road_km > 150, (c) no VA with a
type-T town over 8,000, (d) any VA touching an IR / S-E / Metis settlement,
(e) any VA on the provincial exterior boundary. Prints every district where a
criterion differs, with the criterion, and writes a CSV.
Usage: diff_s152_tables.py <repo> <dir of s15_2_criteria_audit.py> <out.csv>
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

repo, audit_dir, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path[:0] = [str(repo / "analysis/scripts"), str(repo / "analysis/utils"), audit_dir]
import close_seats_ensemble as cse  # noqa: E402
import mcmc_ensemble as me  # noqa: E402
import s15_2_criteria_audit as audit  # noqa: E402

va, graph = me.build_va_graph(verbose=False)
nodes = [n for n in graph.nodes()]
pop = pd.Series({n: graph.nodes[n]["pop_2021"] for n in nodes})
reg = pd.read_csv(repo / "data/outputs/s15_2_va_criteria.csv", index_col="node", keep_default_na=False).loc[nodes]
own = pd.read_csv(repo / "data/outputs/s152_va_criteria.csv", index_col="node", keep_default_na=False).loc[nodes]
tab = reg.copy()
tab["pop"] = pop.to_numpy()
for col in ("road_km", "area_km2", "border_km"):
    tab[col] = tab[col].astype(float)
tab["reserves"] = [json.loads(r) if r else None for r in tab["reserves"]]
res_area = cse._reserve_areas()

pts = va.loc[nodes].copy()
pts["geometry"] = pts.geometry.representative_point()
maps = {"2019": va.loc[nodes, "parent_ed_2019"].to_numpy()}
for name, f in (("majority", "ea_majority_2026_eds.gpkg"), ("minority", "ea_minority_2026_eds.gpkg")):
    eds = gpd.read_file(repo / "data/shapefiles/canonical" / f).to_crs(pts.crs)
    j = gpd.sjoin(pts[["geometry"]], eds[["EDName2025", "geometry"]], how="left", predicate="within")
    maps[name] = j[~j.index.duplicated(keep="first")].reindex(pts.index)["EDName2025"].fillna("__unassigned__").to_numpy()

why = {"a": "same rule (area > 20,000 km2) - should not differ",
       "b": "same rule (road > 150 km) - differs only if road_km inputs differ",
       "c": "towns: registered = CY + T + specialized-municipality urban areas, counted at >= 2% of the "
            "town's population; cross-check = type T only, any VA",
       "d": "reserves: registered = division holds >= 10% of a reserve's / settlement's area (NRCan IR + "
            "Metis); cross-check = any VA touching one (CSD IRI/S-E + NRCan + Metis)",
       "e": "border: registered = >= 1 km shared with the provincial boundary; cross-check = any VA on "
            "the exterior ring"}
rows = []
for m, lab in maps.items():
    r = audit.criteria(tab, lab, None, res_area)
    df = pd.DataFrame({"lab": lab, "pop": pop.to_numpy(), "area": own.area_km2.astype(float).to_numpy(),
                       "road": own.road_km.astype(float).to_numpy(), "big": own.big_town.astype(int).astype(bool).to_numpy(),
                       "res": own.reserve_or_metis.astype(int).astype(bool).to_numpy(),
                       "bord": own.border.astype(int).astype(bool).to_numpy()})
    g = df.groupby("lab").agg(pop=("pop", "sum"), area=("area", "sum"), road=("road", "min"),
                              big=("big", "any"), res=("res", "any"), bord=("bord", "any"))
    ideal = pop.sum() / len(g)
    for d, x in g.iterrows():
        o = {"a": bool(x.area > 20000), "b": bool(x.road > 150), "c": not x.big, "d": bool(x.res), "e": bool(x.bord)}
        rr = r[d]
        diffs = [c for c in "abcde" if o[c] != rr[c]]
        if diffs:
            for c in diffs:
                rows.append({"map": m, "district": d, "dev_pct": round((x["pop"] / ideal - 1) * 100, 1),
                             "criterion": c, "registered": rr[c], "cross_check": o[c],
                             "n_registered": rr["n"], "n_cross_check": sum(o.values()),
                             "matters": (x["pop"] / ideal - 1) < -0.25 or ((rr["n"] >= 3) != (sum(o.values()) >= 3)),
                             "rule": why[c]})
d = pd.DataFrame(rows)
d.to_csv(out, index=False)
print(f"{len(d)} criterion differences in {d[['map', 'district']].drop_duplicates().shape[0] if len(d) else 0} districts")
if len(d):
    print(d.groupby(["map", "criterion"]).size().unstack(fill_value=0).to_string())
    flip = d[d.matters].drop_duplicates(["map", "district"])
    print(f"\ndistricts where the >= 3 eligibility differs or that sit below -25%: {len(flip)}")
    print(flip[["map", "district", "dev_pct", "n_registered", "n_cross_check"]].to_string(index=False))
