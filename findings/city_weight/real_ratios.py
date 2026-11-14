# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Government of Alberta (OGL-Alberta) | Statistics Canada (Open Licence)
"""
real_ratios.py

preregistration/city_weight_calibration_2026-11-07.md: the municipal split ratio R (Amendment 17, §6;
close_seats_ensemble.Geo.csd_split_ratio, unchanged) for every human-drawn map available.
Unregistered.

Usage: python -W ignore findings/city_weight/real_ratios.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd

HERE = Path(__file__).resolve().parent
WT = HERE.parents[1]
AUDIT = WT.parent / "alberta_audit"
sys.path.insert(0, str(AUDIT / "analysis/scripts"))
import close_seats_ensemble as cse  # noqa: E402

H = WT / "data/shapefiles/historical"
MAPS = {"2003_commission": (H / "goa_ped_2003.geojson", "EDNAME"),
        "2010_commission": (H / "goa_ped_2010.geojson", "EDNAME"),
        "2010_commission_EA_file": ("zip://" + str(H / "EDs_Act2010_FINAL.zip"), "EDName2010"),
        "2017_commission_GoA_layer": (H / "goa_ped_2017.geojson", "EDNAME"),
        "2026_majority": (AUDIT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
        "2026_minority": (AUDIT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025"),
        "2026_panel_v3": (WT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg", "district"),
        "para167": (WT / "findings/iap_para167/para167_map.gpkg", "district")}


def main():
    va, graph = cse.me.build_va_graph(verbose=False)
    geo = cse.Geo(va, graph)
    pts = va.loc[geo.nodes].copy()
    pts["geometry"] = pts.geometry.representative_point()
    out = {"n_csds": len(geo.csd_groups),
           "2017_commission": {"k": 87, "R": geo.csd_split_ratio(va.loc[geo.nodes, "parent_ed_2019"].to_numpy())}}
    for name, (f, col) in MAPS.items():
        eds = gpd.read_file(f).to_crs(pts.crs)
        k = eds[col].nunique()
        j = gpd.sjoin(pts[["geometry"]], eds[[col, "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
        lab = j[col].fillna("__unassigned__").to_numpy()
        out[name] = {"k": int(k), "features": int(len(eds)), "unassigned_vas": int((lab == "__unassigned__").sum()),
                     "R": geo.csd_split_ratio(lab)}
    (HERE / "real_ratios.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    for k, v in out.items():
        print(k, v)


if __name__ == "__main__":
    main()
