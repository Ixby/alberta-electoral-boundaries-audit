# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
mark_uncertain_cuts.py
----------------------

Amendment 9, Part 5: on the provisional map, "a cut within this calibration's measured boundary error is
marked as uncertain". Reading fixed in preregistration/a10_stepc_run_sheet_2026-11-04.md, step 9: a cut is
uncertain when at least one side is a changed district (source not "known" in the districts file) and every
part of the VA outside its main district lies within MARGIN_M (the final mean Hausdorff distance of the
registered calibration, 0.031 km) of the main district. Cuts between two known districts are the commission's
geometry and are not marked.

Reads findings/a10_stepc/va_cuts.csv (va_bisection.py output) and the scoring copy; writes
findings/a10_stepc/va_cuts_marked.csv and prints counts.

Usage: python -W ignore findings/a10_stepc/mark_uncertain_cuts.py
"""
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
MAP = REPO / "data/shapefiles/iap_assembled/iap_2026_assembled.gpkg"
CUTS = REPO / "findings/a10_stepc/va_cuts.csv"
OUT = REPO / "findings/a10_stepc/va_cuts_marked.csv"
VAS = {"2023": REPO / "data/shapefiles/reference/alberta_2023_vas/EA_Voting_Area_Boundaries_2023.shp",
       "2026": REPO / "data/reference/ea_vas_2026/EA_Voting_Area_Boundaries_2026.shp"}
MARGIN_M = 31.35  # a10_stepb_calibration.json T3_mean_hausdorff_km = 0.031353
SLIVER_M2 = 1.0   # leftover area below this after removing the margin counts as none


def main():
    eds = gpd.read_file(MAP).to_crs(3400)
    geom = dict(zip(eds.EDName2025, eds.geometry))
    known = set(eds.loc[eds.source == "known", "EDName2025"])
    cuts = pd.read_csv(CUTS, dtype={"va_year": str})
    rows = []
    for year, grp in cuts.groupby("va_year"):
        va = gpd.read_file(VAS[year]).to_crs(3400)
        va["va_id"] = va["ED_NUM"].astype(str).str.zfill(2) + "-" + va["VA_NUMBER"].astype(str).str.zfill(3)
        va = va.set_index("va_id")
        for r in grp.itertuples():
            names = [re.sub(r" \(\d+%\)$", "", s.strip()) for s in r.districts.split(";")]
            main, others = names[0], names[1:]
            involves_changed = any(n not in known for n in names)
            g = va.loc[r.va_id, "geometry"]
            g = g.union_all() if hasattr(g, "union_all") else g
            outside = g.difference(geom[main])
            left = outside.difference(geom[main].buffer(MARGIN_M))
            within = left.area < SLIVER_M2
            rows.append({**r._asdict(), "involves_changed": involves_changed, "outside_beyond_margin_m2": round(left.area, 1),
                         "uncertain": bool(involves_changed and within)})
    out = pd.DataFrame(rows).drop(columns="Index")
    out.to_csv(OUT, index=False)
    for year, grp in out.groupby("va_year"):
        print(f"{year}: {len(grp)} cut; {int(grp.involves_changed.sum())} involve a changed district; "
              f"{int(grp.uncertain.sum())} marked uncertain")


if __name__ == "__main__":
    main()
