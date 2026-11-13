# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Government of Alberta (OGL-Alberta) | Statistics Canada (Open Licence)
"""
measurable_checks.py

M1-M3 of preregistration/reasons_consistency_2026-11-07.md: is "population to spare" applied alike
to comparable cities; was the population added for "necessary population" the minimum needed; did
divisions defended on shape get more regular. Unregistered. Applies no test of intent.

Usage: python -W ignore findings/reasons_consistency/measurable_checks.py
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
from real_maps import MAPS, assign  # noqa: E402

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
AVG = 4888723 / 91
BAND = (AVG * 0.75, AVG * 1.25)


def csd_2024():
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
    out = {}
    for r in rows[hdr + 1:]:
        if re.fullmatch(r"48\d{5}", str(r.get("B", ""))) and r.get(cols["Type"]) == "CY" and re.fullmatch(r"\d+", str(r.get(cols["2024"], ""))):
            out[r["B"]] = (r[cols["Area Name"]], int(r[cols["2024"]]))
    return out


def pp(geom):
    g = geom.simplify(50)
    return 4 * math.pi * g.area / g.length ** 2


def main():
    b = gpd.read_file(ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg").to_crs(3400)
    pts = b[["geometry"]].copy()
    pts["geometry"] = b.geometry.representative_point()
    pop = pd.read_csv(ROOT / "data/va_pop_from_das.csv").set_index("va_row_idx")["pop_2021"]
    vp = pd.Series(b.index.map(pop).values).fillna(0.0).clip(lower=1.0).to_numpy()
    csd = gpd.read_file(ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(3400)
    j = gpd.sjoin(pts, csd[["CSDUID", "geometry"]], how="left", predicate="within")
    va_csd = j[~j.index.duplicated(keep="first")].CSDUID.astype(str).reindex(pts.index).to_numpy()
    P = assign(pts, *MAPS["panel"]).to_numpy()
    M = assign(pts, *MAPS["majority"]).to_numpy()
    out = {"plan": "preregistration/reasons_consistency_2026-11-07.md", "average_91": round(AVG, 1), "band_25": [round(x) for x in BAND]}

    # M1
    cities = {u: v for u, v in csd_2024().items() if v[1] >= 20000}
    rows = []
    for u, (name, p24) in sorted(cities.items(), key=lambda x: -x[1][1]):
        m = va_csd == u
        tot = pd.Series(vp).groupby(P).sum()
        by = pd.Series(vp[m]).groupby(P[m]).sum()
        pieces = by[by >= 0.02 * by.sum()]
        hybrid_share = float(sum(by[d] for d in pieces.index if by[d] < 0.5 * tot[d]) / by.sum())
        rows.append({"city": name, "pop_2024_estimate": p24, "ratio_to_average": round(p24 / AVG, 2),
                     "panel_divisions_holding": int(len(pieces)), "share_in_divisions_where_city_is_minority": round(hybrid_share, 3)})
    out["M1_population_to_spare"] = rows

    # M2
    app7 = pd.read_csv(ROOT / "data/iap/iap_app7_populations.csv").set_index("district").population
    maj = gpd.read_file(MAPS["majority"][0], ignore_geometry=True).set_index("EDName2025").PopCensus
    out["M2_necessary_population"] = {
        "band_low": round(BAND[0]), "majority_Canmore-Banff": int(maj["Canmore-Banff"]),
        "needed_to_reach_band_before_RMH_transfer": max(0, round(BAND[0] - maj["Canmore-Banff"])),
        "minority_says_unanimous_RMH_transfer_affects": "fewer than 1,000 residents (minority opinion, para 6)",
        "panel_Banff-Canmore-Diamond_Valley": int(app7["Banff-Canmore-Diamond Valley"]),
        "net_added_vs_majority": int(app7["Banff-Canmore-Diamond Valley"] - maj["Canmore-Banff"]),
        "majority_Lethbridge-East_dev_pct_at_91": round(100 * (maj["Lethbridge-East"] / AVG - 1), 1),
        "majority_Lethbridge-West_dev_pct_at_91": round(100 * (maj["Lethbridge-West"] / AVG - 1), 1),
        "panel_Lethbridge_dev_pct": round(100 * (app7["Lethbridge"] / AVG - 1), 1)}

    # M3
    gp = gpd.read_file(MAPS["panel"][0]).to_crs(3400).set_index("district").geometry
    gm = gpd.read_file(MAPS["majority"][0]).to_crs(3400).set_index("EDName2025").geometry
    sets_m = {frozenset(np.where(M == d)[0]) for d in set(M)}
    comp = []
    for d in sorted(set(P)):
        idx = np.where(P == d)[0]
        if frozenset(idx) in sets_m:
            continue
        src = pd.Series(vp[idx]).groupby(M[idx]).sum().idxmax()
        comp.append({"panel": d, "majority_source": src, "pp_panel": round(pp(gp[d]), 3), "pp_majority": round(pp(gm[src]), 3),
                     "change": round(pp(gp[d]) - pp(gm[src]), 3)})
    out["M3_compactness_changed"] = sorted(comp, key=lambda r: r["change"])
    (HERE / "measurable_checks.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    print(json.dumps(out, indent=0)[:5000])


if __name__ == "__main__":
    main()
