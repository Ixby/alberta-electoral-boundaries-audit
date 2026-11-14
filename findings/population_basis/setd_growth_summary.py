# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence) | Alberta OSI (OGL-Alberta)
"""
setd_growth_summary.py

Set D (91 districts, s.15(2), chains 251-254) rerun on the 2024 growth basis, against the same set D
on the 2021 census (all-ballots replay). Recomputes the city-versus-rest test (city_gap_pct; the
registered size-matched flag is at or above the set's 95th percentile) and the seat counts:
districts at least half Calgary or Edmonton, per city, by plurality region, and UCP seats on all
2023 ballots. Midrank percentiles, as in the canonical harness. Unregistered sensitivity analysis.

Usage: python -I -W ignore findings/population_basis/setd_growth_summary.py
"""
import hashlib
import json
from pathlib import Path

import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
AA = ROOT.parent / "alberta_audit/data"
D21 = AA / "simulation_checkpoints_k91_s152a23_allballots"
D24 = AA / "simulation_checkpoints_k91_s152a23_allballots_growth"
sys.path.insert(0, str(ROOT / "analysis/scripts"))
from size_matched_results import NEFF_FINAL, ess, neff_uncapped  # noqa: E402  (registered estimator)

IDX21 = (251, 252, 253, 254)
# 252 and 255 did not seed on the growth basis; retired and replaced by the next unused index
# (Amendment 11, Part 3; Amendment 5, Part 14 precedent).
IDX24 = (251, 253, 254, 256)
SHARED = (251, 253, 254)
RETIRED = {252: "no seed: recursive_tree_part, no cut after 50000 attempts", 255: "no seed: same"}


def pct(x, v):
    return round(100 * float((x < v).mean() + 0.5 * (x == v).mean()), 2)


def dist(x, real):
    x = np.asarray(x, float)
    out = {"q05": round(float(np.quantile(x, .05)), 3), "q50": round(float(np.quantile(x, .5)), 3),
           "q95": round(float(np.quantile(x, .95)), 3)}
    for k, v in real.items():
        if v is not None:
            out[k] = {"value": v, "pct": pct(x, v)}
    return out


def main():
    gn = json.loads((HERE / "growth_nodes.json").read_text())["real_maps"]
    reals = json.loads((ROOT / "findings/amendment12_rehearsal/iap_assembled_real_maps_allballots.json").read_text())
    panel_ucp = None
    for k, v in (reals.items() if isinstance(reals, dict) else []):
        if isinstance(v, dict) and "ucp_seats" in v and "iap" in k:
            panel_ucp = v["ucp_seats"]
    cols = ["city_gap_pct", "n_city_districts", "ucp_seats", "population_mad", "s152_districts", "step"]
    d21 = {i: pd.read_csv(D21 / f"chain{i}_samples.csv", usecols=cols) for i in IDX21}
    d24 = {i: pd.read_csv(D24 / f"chain{i}_samples.csv") for i in IDX24}
    a21, a24 = pd.concat(d21.values()), pd.concat(d24.values())
    out = {"plan": "preregistration/population_basis_2026-11-07.md (commit c01cbdcd): proposed rerun of set D on the growth basis",
           "status": "unregistered sensitivity analysis", "votes": "all 2023 ballots (primary gpkg), UCP seats only",
           "retired_growth_indices": RETIRED, "chains": {}, "plans": {"2021": int(len(a21)), "growth": int(len(a24))}}
    for i in IDX24:
        f = D24 / f"chain{i}_samples.csv"
        ck = json.loads((D24 / f"chain{i}_samples.csv.ckpt.json").read_text())
        out["chains"][i] = {"rows": int(len(d24[i])), "seed": ck["seed"], "done": ck["done"], "pop_file_sha256": ck.get("pop_file"),
                            "s152_sha256": ck.get("s152"), "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                            "city_gap_median_growth": round(float(d24[i].city_gap_pct.median()), 3),
                            "city_gap_median_2021": round(float(d21[i].city_gap_pct.median()), 3) if i in d21 else None}
    m = {}
    s21 = pd.concat([d21[i] for i in SHARED])
    s24 = pd.concat([d24[i] for i in SHARED])
    for basis, a in (("2021", a21), ("growth", a24), ("2021_shared_251_253_254", s21), ("growth_shared_251_253_254", s24)):
        b = "2021" if basis.startswith("2021") else "growth"
        real_gap = {k: gn[k][b]["city_gap_pct"] for k in ("panel", "para167")}
        if b == "growth":
            real_gap["panel_published"] = gn["panel"]["published"]["city_gap_pct"]
        g = dist(a.city_gap_pct, real_gap)
        g["flag_rule"] = "at or above the set's 95th percentile"
        g["flagged"] = {k: bool(v["pct"] >= 95) for k, v in g.items() if isinstance(v, dict) and "pct" in v}
        chains = d21 if basis == "2021" else d24 if basis == "growth" else None
        if chains is not None:
            ne, capped, per = ess({i: df[["city_gap_pct"]] for i, df in chains.items()}, "city_gap_pct")
            g["n_eff"] = round(ne, 1)
            g["n_eff_per_chain"] = [round(x, 1) for x in per]
            g["lag_cap_bound"] = capped
            g["n_eff_uncapped_diagnostic"] = round(float(sum(neff_uncapped(df.city_gap_pct.to_numpy(float)) for df in chains.values())), 1)
            g["status"] = "final" if ne >= NEFF_FINAL and not capped else "provisional"
            g["panel_pct_per_chain"] = {int(i): pct(df.city_gap_pct.to_numpy(float), real_gap["panel"]) for i, df in chains.items()}
            g["chain_q95"] = {int(i): round(float(np.quantile(df.city_gap_pct, .95)), 3) for i, df in chains.items()}
        m[basis] = {"city_gap_pct": g,
                    "n_city_districts": dist(a.n_city_districts, {"panel": gn["panel"][b]["n_city_districts"]}),
                    "ucp_seats_all_ballots": dist(a.ucp_seats, {"panel": panel_ucp}),
                    "population_mad": dist(a.population_mad, {}),
                    "s152_districts": dist(a.s152_districts, {})}
    for c in [c for c in a24.columns if c.startswith("reg_") or c in ("n_calgary", "n_edmonton")]:
        pv = gn["panel"]["growth"].get(c.replace("n_", "")) if c.startswith("n_") else gn["panel"]["growth"]["reg"].get(c)
        m["growth"][c] = dist(a24[c], {"panel": pv})
        if c.startswith("reg_"):
            m["growth"][c]["panel_minus_neutral_median"] = pv - float(np.median(a24[c]))
    out["measures"] = m
    out["ucp_seats_panel_source"] = "findings/amendment12_rehearsal/iap_assembled_real_maps_allballots.json"
    (HERE / "setd_growth.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
