# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
va_bisection.py
---------------

Which voting areas (polls) does a district map cut? Descriptive, not a test.

A voting area is cut when more than CUT_SHARE of its area, and more than
CUT_KM2, lies outside the district holding most of it. The two floors keep
digitising slivers out. They are calibrated on Elections Alberta's own
nesting: its voting areas nest exactly in the divisions in force, so the
2019 map against the 2023 and 2026 voting areas should show none, and
whatever it shows is the noise floor.

Voting areas: Elections Alberta 2023 (data/shapefiles/reference/alberta_2023_vas/)
and 2026 (data/reference/ea_vas_2026/, EA_Voting_Area_Boundaries_2026.zip).

Usage
  python analysis/scripts/va_bisection.py --map MAP.gpkg [--name-col EDName2025]
         --label NAME [--out-csv PATH] [--vas 2023 2026]
"""
import argparse
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
VAS = {"2023": REPO / "data/shapefiles/reference/alberta_2023_vas/EA_Voting_Area_Boundaries_2023.shp",
       "2026": REPO / "data/reference/ea_vas_2026/EA_Voting_Area_Boundaries_2026.shp"}
CUT_SHARE, CUT_KM2 = 0.01, 0.01


def cuts(va, eds, col):
    va = va.to_crs(3400).copy()
    eds = eds.to_crs(3400)[[col, "geometry"]]
    va["va_id"] = va["ED_NUM"].astype(str).str.zfill(2) + "-" + va["VA_NUMBER"].astype(str).str.zfill(3)
    va["va_km2"] = va.geometry.area / 1e6
    ov = gpd.overlay(va[["va_id", "ED_NAME", "va_km2", "geometry"]], eds, how="intersection", keep_geom_type=True)
    ov["km2"] = ov.geometry.area / 1e6
    g = ov.groupby(["va_id", col], as_index=False).agg(km2=("km2", "sum"))
    rows = []
    for vid, grp in g.groupby("va_id"):
        tot = float(va.loc[va.va_id == vid, "va_km2"].iloc[0])
        grp = grp.sort_values("km2", ascending=False)
        out = tot - float(grp.km2.iloc[0])
        if out > CUT_SHARE * tot and out > CUT_KM2:
            pieces = grp[grp.km2 > max(CUT_KM2, CUT_SHARE * tot)]
            rows.append({"va_id": vid, "va_ed_2019": va.loc[va.va_id == vid, "ED_NAME"].iloc[0],
                         "va_km2": round(tot, 3), "outside_main_km2": round(out, 3),
                         "outside_share": round(out / tot, 3), "n_districts": int(len(pieces)),
                         "districts": "; ".join(f"{r[col]} ({r.km2 / tot:.0%})" for _, r in pieces.iterrows())})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True)
    ap.add_argument("--name-col", default="EDName2025")
    ap.add_argument("--label", required=True)
    ap.add_argument("--vas", nargs="+", default=["2023", "2026"])
    ap.add_argument("--out-csv")
    a = ap.parse_args()
    eds = gpd.read_file(a.map)
    summary, frames = {"map": a.label, "rule": f"cut when > {CUT_SHARE:.0%} and > {CUT_KM2} km2 outside the main district"}, []
    for y in a.vas:
        va = gpd.read_file(VAS[y])
        df = cuts(va, eds, a.name_col)
        df.insert(0, "va_year", y)
        frames.append(df)
        summary[f"vas_{y}"] = {"total": int(len(va)), "cut": int(len(df))}
    out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if a.out_csv:
        out.to_csv(a.out_csv, index=False)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
