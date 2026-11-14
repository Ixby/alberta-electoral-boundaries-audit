# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Government of Alberta (OGL-Alberta) | Statistics Canada (Open Licence)
"""
big_city_lines.py

Companion to the municipal split ratio, which leaves out Calgary and Edmonton because both must be split
on every map. For each human-drawn map: how many divisions cross the Calgary or Edmonton city line
(5-95% of the division's 2021 population in the city) and the share of the city's people living in
them. Unregistered; descriptive only.

Usage: python -W ignore findings/city_weight/big_city_lines.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import real_ratios as RR  # noqa: E402


def main():
    va, graph = RR.cse.me.build_va_graph(verbose=False)
    geo = RR.cse.Geo(va, graph)
    pts = va.loc[geo.nodes].copy()
    pts["geometry"] = pts.geometry.representative_point()
    maps = {k: v for k, v in RR.MAPS.items() if k not in ("2010_commission_EA_file", "2017_commission_GoA_layer")}
    labs = {"2017_commission": va.loc[geo.nodes, "parent_ed_2019"].to_numpy()}
    for n, (f, c) in maps.items():
        e = gpd.read_file(f).to_crs(pts.crs)
        j = gpd.sjoin(pts[["geometry"]], e[[c, "geometry"]], how="left", predicate="within")
        labs[n] = j[~j.index.duplicated(keep="first")].reindex(pts.index)[c].fillna("__u").to_numpy()
    out = {}
    for city, mask in (("Calgary", geo.is_cal), ("Edmonton", geo.is_edm)):
        out[city] = {}
        for n, lab in labs.items():
            df = pd.DataFrame({"d": lab, "p": geo.pop, "c": mask})
            tot = df.groupby("d").p.sum()
            cp = df[df.c].groupby("d").p.sum()
            share = cp / tot.reindex(cp.index)
            cross = sorted(d for d in cp.index if cp[d] >= 0.005 * cp.sum() and 0.05 <= share[d] <= 0.95)
            out[city][n] = {"crossing_divisions": cross, "n_crossing": len(cross),
                            "city_pop_in_crossing_pct": round(100 * float(cp[cross].sum() / cp.sum()), 1)}
    (HERE / "big_city_lines.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
