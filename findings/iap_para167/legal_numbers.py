# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
legal_numbers.py

The measurable inputs to the Carter and EBCA scorecard (legal_scorecard.md): stated population
deviations (EBCA s.15(1)), s.15(2) criteria per division, and urban and rural population means.
Unregistered. Measures only: it applies no legal test and reaches no conclusion on any map.

Reads   data/iap/iap_app7_populations.csv (panel's stated populations)
        data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg (commission's stated populations)
        data/outputs/s15_2_va_criteria.csv (per-VA criteria, s15_2_criteria.py)
        data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg, findings/iap_para167/para167_map.gpkg
        data/shapefiles/derived/va_polygons_with_2023_votes.gpkg (VA polygons)
Writes  findings/iap_para167/legal_numbers.json

Usage: python -W ignore findings/iap_para167/legal_numbers.py
"""
import ast
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis/scripts"))
import s15_2_criteria as S  # noqa: E402

MAPS = {"majority": ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
        "minority": ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg",
        "panel": ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg",
        "para167": HERE / "para167_map.gpkg"}
VAS = ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"


def spread(names, pop):
    avg = pop.mean()
    dev = 100 * (pop / avg - 1)
    urban = names.str.startswith(("Calgary-", "Edmonton-"))
    return {"n": len(pop), "total": int(pop.sum()), "average": round(float(avg), 1),
            "band_25": [round(avg * 0.75), round(avg * 1.25)], "floor_50": round(avg * 0.5),
            "above_plus_25": names[dev > 25].tolist(),
            "below_minus_25": {n: round(float(d), 1) for n, d in zip(names[dev < -25], dev[dev < -25])},
            "lowest_outside_s15_2": round(float(dev[dev >= -25].min()), 1), "highest": round(float(dev.max()), 1),
            "within_5": int((dev.abs() <= 5).sum()), "within_10": int((dev.abs() <= 10).sum()),
            "share_within_10": round(float((dev.abs() <= 10).mean()), 3),
            "mad_people": round(float((pop - avg).abs().mean())),
            "mean_calgary_edmonton": round(float(pop[urban].mean())), "mean_rest": round(float(pop[~urban].mean())),
            "n_calgary_edmonton": int(urban.sum())}


def s152(tab, res_area, labels, names):
    got = S.criteria(tab, labels, {}, res_area)
    return {n: got[n] for n in names}


def main():
    out = {"stated": {}}
    a = pd.read_csv(ROOT / "data/iap/iap_app7_populations.csv")
    out["stated"]["panel"] = spread(a.district, a.population)
    for k in ("majority", "minority"):
        m = gpd.read_file(MAPS[k], ignore_geometry=True)
        out["stated"][k] = spread(m.EDName2025, m.PopCensus)

    tab = pd.read_csv(ROOT / "data/outputs/s15_2_va_criteria.csv").set_index("node")
    tab["town"] = tab["town"].fillna("")
    tab["reserves"] = tab["reserves"].map(lambda x: json.loads(x) if isinstance(x, str) else None)
    res_area = {}
    for r in tab["reserves"].dropna():
        for k, v in r.items():
            res_area[k] = res_area.get(k, 0.0) + v

    va = gpd.read_file(VAS).to_crs(3400)
    pts = va[["geometry"]].copy()
    pts["geometry"] = va.geometry.representative_point()
    out["s15_2"], out["overlay_2021"] = {}, {}
    for k, f in MAPS.items():
        col = "district" if k in ("panel", "para167") else "EDName2025"
        lab = S.assign(pts, f, col).reindex(tab.index).to_numpy()
        pop = tab["pop"].groupby(lab).sum()
        out["overlay_2021"][k] = spread(pop.index.to_series().reset_index(drop=True), pop.reset_index(drop=True))
        low = list(out["overlay_2021"][k]["below_minus_25"])
        stated_low = list(out["stated"][k]["below_minus_25"]) if k in out["stated"] else []
        out["s15_2"][k] = s152(tab, res_area, lab, sorted(set(low) | set(stated_low)))
    (HERE / "legal_numbers.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf8")
    print(json.dumps(out, indent=0, default=float)[:6500])


if __name__ == "__main__":
    main()
