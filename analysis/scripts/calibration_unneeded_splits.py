# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
calibration_unneeded_splits.py
------------------------------

Municipal splits counted by people, for the lane calibration
(analysis/methodology/structural_lane_calibration_design.md). Calibration
only; the registered S2 (Amendment 5, Part 7) and the registered town-split
measure (Amendment 5, Part 17) are unchanged.

Municipalities are 2021 CSDs of type CY, T or SM. People are 2021 census
dissemination areas (DAs), which nest in CSDs. A DA cut by a district line
is shared out by area. Real maps are overlaid on their official boundaries;
computer-drawn plans, which are unions of voting areas (VAs), through a
DA-by-VA overlay.

  pieces          districts holding >= 2% of the municipality's people
                  (the piece rule in Amendment 5, Part 17)
  need            ceil(pop / (1.25 x average district population)): the fewest
                  districts the Act's ±25% band allows
  must_split      need >= 2
  unneeded_split  need == 1 and pieces >= 2
  extra_pieces    pieces > need

The 2% rule is coarse for small towns (2% of 1,300 people is 26), and area
sharing assumes people are spread evenly within a DA.

Usage
  python analysis/scripts/calibration_unneeded_splits.py --plans DIR --out PATH
"""
import argparse
import glob
import json
import math
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))
REAL = {"2019": ("data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp", "EDName2017"),
        "majority": ("data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
        "minority": ("data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025")}
KINDS = ("must_split", "unneeded_split", "extra_pieces")


def main(a):
    import mcmc_ensemble as me

    warnings.filterwarnings("ignore")
    va, graph = me.build_va_graph(verbose=False)
    nodes = sorted(graph.nodes())
    va = va.loc[nodes, ["geometry"]].copy()
    total = float(sum(graph.nodes[n]["pop_2021"] for n in nodes))
    da = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_das.gpkg").to_crs(va.crs)
    da["pop"] = da["DGUID"].map(pd.read_csv(REPO / "data/reference/alberta_2021_da_populations.csv")
                                .set_index("DGUID")["population_2021"]).fillna(0)
    csd = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(va.crs)
    csd = csd[csd["CSDTYPE"].isin(["CY", "T", "SM"])]
    pt = da[["DGUID", "geometry"]].copy()
    pt["geometry"] = da.geometry.representative_point()
    j = gpd.sjoin(pt, csd[["CSDNAME", "geometry"]], how="inner", predicate="within")
    da = da.merge(j[["DGUID", "CSDNAME"]], on="DGUID")
    da = da[da["pop"] > 0]
    mpop = da.groupby("CSDNAME")["pop"].sum()

    def share_out(zones, key):
        o = gpd.overlay(da[["DGUID", "CSDNAME", "pop", "geometry"]], zones[[key, "geometry"]],
                        how="intersection", keep_geom_type=True)
        o["a"] = o.area
        o["p"] = o["pop"] * o["a"] / o.groupby("DGUID")["a"].transform("sum")
        return o.groupby(["CSDNAME", key])["p"].sum()

    def kinds(by, k):
        avg = total / k
        out = {key: [] for key in KINDS}
        for n, s in by.groupby(level=0):
            tp = mpop[n]
            pieces = int((s >= 0.02 * tp).sum())
            need = math.ceil(tp / (1.25 * avg))
            if need >= 2:
                out["must_split"].append(n)
            if need == 1 and pieces >= 2:
                out["unneeded_split"].append(n)
            if pieces > need:
                out["extra_pieces"].append(n)
        return out

    real = {}
    for m, (f, col) in REAL.items():
        ed = gpd.read_file(REPO / f).to_crs(va.crs)
        real[m] = kinds(share_out(ed, col), ed[col].nunique())
    vz = va.reset_index()
    vz = vz.rename(columns={vz.columns[0]: "node"})
    tv = share_out(vz, "node").reset_index()
    rows = []
    for f in sorted(glob.glob(str(Path(a.plans) / "plan_*.json"))):
        asg = {int(k): int(v) for k, v in json.loads(Path(f).read_text()).items()}
        t = tv.assign(d=tv["node"].map(asg))
        rows.append({"plan": Path(f).stem, **{key: len(v) for key, v in
                                              kinds(t.groupby(["CSDNAME", "d"])["p"].sum(), len(set(asg.values()))).items()}})
    df = pd.DataFrame(rows)
    rank = {m: {key: int((df[key] <= len(o[key])).sum()) for key in KINDS} for m, o in real.items()} if len(df) else {}
    res = {"n_plans": len(df), "real": real, "computer_as_few_or_fewer": rank,
           "computer_summary": {key: {"min": int(df[key].min()), "median": float(df[key].median()),
                                      "max": int(df[key].max())} for key in KINDS} if len(df) else {},
           "plans": rows}
    Path(a.out).write_text(json.dumps(res, indent=1))
    for m, o in real.items():
        print(m, {key: len(v) for key, v in o.items()}, "unneeded:", o["unneeded_split"], "| as few or fewer:", rank.get(m))
    print("computer", res["computer_summary"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans", required=True)
    ap.add_argument("--out", required=True)
    main(ap.parse_args())
