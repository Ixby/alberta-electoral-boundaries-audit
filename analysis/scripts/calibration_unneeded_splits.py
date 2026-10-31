# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
calibration_unneeded_splits.py
------------------------------

Municipal splits counted by people, for the lane calibration
(analysis/methodology/structural_lane_calibration_design.md). Calibration
only; the registered S2 (Amendment 9) is unchanged.

Municipalities are 2021 CSDs of type CY, T or SM. VAs are assigned to a
municipality and to a real-map district by representative point.

  pieces          districts holding >= 2% of the municipality's people
                  (Amendment 17's piece rule)
  need            ceil(pop / (1.25 x average district population)): the fewest
                  districts the Act's ±25% band allows
  must_split      need >= 2
  unneeded_split  need == 1 and pieces >= 2
  extra_pieces    pieces > need

Scores the 2019 map (VA parent_ed_2019), both 2026 commission maps, and every
plan_*.json under --plans.

Usage
  python analysis/scripts/calibration_unneeded_splits.py --plans DIR --out PATH
"""
import argparse
import glob
import json
import math
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))
CSD = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"
MAPS = {"majority": "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
        "minority": "data/shapefiles/canonical/ea_minority_2026_eds.gpkg"}
KINDS = ("split_any", "must_split", "unneeded_split", "extra_pieces")


def main(a):
    import mcmc_ensemble as me

    va, graph = me.build_va_graph(verbose=False)
    nodes = sorted(graph.nodes())
    va_full = va.loc[nodes].copy()
    pop = np.array([graph.nodes[n]["pop_2021"] for n in nodes], float)
    pts = va_full[["geometry"]].copy()
    pts["geometry"] = va_full.geometry.representative_point()
    csd = gpd.read_file(CSD).to_crs(va_full.crs)
    j = gpd.sjoin(pts, csd[["CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    keep = j["CSDTYPE"].isin(["CY", "T", "SM"]).to_numpy()
    name = j["CSDNAME"].fillna("").to_numpy()
    munis = [(n, np.where(keep & (name == n))[0]) for n in sorted(set(name[keep]))]
    munis = [(n, ix) for n, ix in munis if pop[ix].sum() > 0]

    def kinds(labels):
        uniq, inv = np.unique(np.asarray(labels), return_inverse=True)
        k = len(uniq)
        avg = pop.sum() / k
        out = {key: [] for key in KINDS}
        for n, ix in munis:
            tp = pop[ix].sum()
            pieces = int((np.bincount(inv[ix], weights=pop[ix], minlength=k) >= 0.02 * tp).sum())
            need = math.ceil(tp / (1.25 * avg))
            if pieces >= 2:
                out["split_any"].append(n)
            if need >= 2:
                out["must_split"].append(n)
            if need == 1 and pieces >= 2:
                out["unneeded_split"].append(n)
            if pieces > need:
                out["extra_pieces"].append(n)
        return out

    real = {"2019": kinds(va_full["parent_ed_2019"].fillna("__none__").astype(str).to_numpy())}
    for key, f in MAPS.items():
        g = gpd.read_file(REPO / f).to_crs(va_full.crs)
        jj = gpd.sjoin(pts, g[["EDName2025", "geometry"]], how="left", predicate="within")
        real[key] = kinds(jj[~jj.index.duplicated(keep="first")].reindex(pts.index)["EDName2025"].fillna("__none__").to_numpy())
    rows = []
    for f in sorted(glob.glob(str(Path(a.plans) / "plan_*.json"))):
        asg = json.loads(Path(f).read_text())
        lab = pd.Series({int(k): int(v) for k, v in asg.items()}).reindex(va_full.index).to_numpy()
        rows.append({"plan": Path(f).stem, **{key: len(v) for key, v in kinds(lab).items()}})
    df = pd.DataFrame(rows)
    rank = {m: {key: int((df[key] <= len(o[key])).sum()) for key in KINDS} for m, o in real.items()}
    res = {"n_plans": len(df), "real": real, "computer_as_few_or_fewer": rank,
           "computer_summary": {key: {"min": int(df[key].min()), "median": float(df[key].median()),
                                      "max": int(df[key].max())} for key in KINDS},
           "plans": rows}
    Path(a.out).write_text(json.dumps(res, indent=1))
    for m, o in real.items():
        print(m, {key: len(v) for key, v in o.items()}, "unneeded:", o["unneeded_split"], "| as few or fewer:", rank[m])
    print("computer", res["computer_summary"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans", required=True)
    ap.add_argument("--out", required=True)
    main(ap.parse_args())
