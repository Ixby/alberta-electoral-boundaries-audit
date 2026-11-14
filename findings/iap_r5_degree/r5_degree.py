# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
r5_degree.py

Recommendation 5 by degree, beside the registered X1 result (Amendment 5, Part 13), which stands.
Unregistered. No grade here says whether a departure was necessary; Motion 37 left that to the panel.

Two independent readings of "changed" for each protected division:
  stated   Appendix 7 against the majority's official table: same name, same population, area
           within 0.5 km2 (Appendix 7 prints whole km2). Needs no reconstruction.
  overlay  score_x1's 99%/99% rule on the v3 reconstruction (x1_v3.json).
People moved = stated majority population x (1 - overlay share kept by the largest successor):
an estimate, since the shares are 2021 census overlay by VA representative point.

Reads   data/iap/iap_app7_populations.csv, data/iap/abebc_interim_edmonton_south.csv
        data/shapefiles/canonical/ea_majority_2026_eds.gpkg
        viewer/static/mapdata/lunty_bounds.json, findings/iap_r5_degree/x1_v3.json
Writes  findings/iap_r5_degree/r5_degree.json, zone_a_divisions.csv

Usage: python -W ignore findings/iap_r5_degree/r5_degree.py
"""
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    A = pd.read_csv(ROOT / "data/iap/iap_app7_populations.csv").set_index("district")
    M = gpd.read_file(ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg").set_index("EDName2025")
    X = json.loads((HERE / "x1_v3.json").read_text())
    Z = {z["cond"]: z["eds"] for z in json.loads((ROOT / "viewer/static/mapdata/lunty_bounds.json").read_text())["zones"]}

    def identical(n):
        return n in A.index and A.population[n] == M.PopCensus[n] and abs(A.area_km2[n] - M.Km2[n]) <= 0.5

    def table(key):
        rows = []
        for r in X[key]["divisions"]:
            n = r["division"]
            rows.append({"division": n, "stated_pop": int(M.PopCensus[n]), "stated_identical": bool(identical(n)),
                         "overlay_unchanged": r["unchanged"], "largest_successor": r["best"],
                         "share_kept": r["share_of_old"], "share_of_successor": r["share_of_new"],
                         "people_moved_est": round(M.PopCensus[n] * (1 - r["share_of_old"])),
                         "app7_pop": int(A.population[n]) if n in A.index else None,
                         "app7_km2": float(A.area_km2[n]) if n in A.index else None, "majority_km2": float(M.Km2[n])})
        return pd.DataFrame(rows)

    out = {}
    for key in ("a", "b", "rest"):
        t = table(key)
        same = t[t.stated_identical & t.overlay_unchanged]
        out[key] = {"n": len(t), "identical_both_readings": len(same), "overlay_unchanged": int(t.overlay_unchanged.sum()),
                    "stated_identical": int(t.stated_identical.sum()), "pop": int(t.stated_pop.sum()),
                    "pop_identical": int(same.stated_pop.sum()), "pop_share_identical": round(same.stated_pop.sum() / t.stated_pop.sum(), 4),
                    "people_moved_est": int(t.people_moved_est.sum()), "changed": sorted(set(t.division) - set(same.division))}
        if key == "a":
            t.to_csv(HERE / "zone_a_divisions.csv", index=False)
    I = pd.read_csv(ROOT / "data/iap/abebc_interim_edmonton_south.csv")
    I["app7"] = I.app7_division.map(A.population)
    I["diff"] = I.app7 - I.population
    assert sorted(Z["c"]) != [], "zone c"
    out["c"] = {"n": len(I), "population_identical": int((I["diff"] == 0).sum()),
                "differ": I[I["diff"] != 0][["interim_division", "app7_division", "population", "app7", "diff"]].to_dict("records")}
    out["d"] = X["d"]
    out["registered_X1"] = {"X1": X["X1"], "a": f"{X['a']['n_unchanged']}/{X['a']['n']}", "b": f"{X['b']['n_unchanged']}/{X['b']['n']}", "c": "not scored"}
    (HERE / "r5_degree.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
