# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Statistics Canada 2021 Census (Open Licence) | Alberta Office of Statistics and Information (OGL-Alberta)
"""
population_basis.py

Runs preregistration/population_basis_2026-11-07.md: how much the neutral maps' 2021 census basis
differs from the 2024 estimates the real maps were balanced on. Each voting area's 2021 population is
scaled by its CSD's 2021-to-2024 growth in the province's municipal estimates (fallback: its census
division's, then the province's). Unregistered. Describes population only, not intent.

Usage: python -I -W ignore findings/population_basis/population_basis.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis/scripts"))
sys.path.insert(0, str(ROOT / "findings/osi_rebuild"))
sys.path.insert(0, str(ROOT / "findings/packing_cracking"))
import mcmc_ensemble as me  # noqa: E402
from rebuild_da_2024 import csd_2024, maps  # noqa: E402
from real_maps import assign  # noqa: E402

CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
SETD = ROOT.parent / "alberta_audit/data/simulation_checkpoints_k91_s152a23_allballots"
K = 91
CAL_RING = {"Airdrie", "Chestermere", "Cochrane", "Okotoks", "Rocky View County", "Foothills County"}
EDM_RING = {"St. Albert", "Strathcona County", "Spruce Grove", "Stony Plain", "Leduc", "Beaumont",
            "Fort Saskatchewan", "Parkland County", "Sturgeon County", "Leduc County"}


def region(name, typ, cpop):
    if name == "Calgary":
        return "Calgary"
    if name == "Edmonton":
        return "Edmonton"
    if name in CAL_RING:
        return "Calgary ring"
    if name in EDM_RING:
        return "Edmonton ring"
    if typ == "CY" and cpop >= 20000:
        return "Other cities 20,000+"
    return "Everything else"


def main():
    va, graph = me.build_va_graph(verbose=False)
    pop21 = va.pop_2021.to_numpy(float)
    pts = va[["geometry"]].copy()
    pts["geometry"] = va.geometry.representative_point()
    csd = gpd.read_file(CSD).to_crs(pts.crs)
    j = gpd.sjoin(pts, csd[["CSDUID", "CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    uid = j.CSDUID.astype("string").fillna("").to_numpy()
    name = j.CSDNAME.fillna("").to_numpy()
    typ = j.CSDTYPE.fillna("").to_numpy()

    est = csd_2024()
    g_csd = (est.est_2024 / est.est_2021).to_dict()
    cd = est.groupby(est.index.str[:4]).sum()
    g_cd = (cd.est_2024 / cd.est_2021).to_dict()
    g_prov = float(est.est_2024.sum() / est.est_2021.sum())
    src = np.where([u in g_csd for u in uid], "csd", np.where([u[:4] in g_cd for u in uid], "cd", "province"))
    factor = np.array([g_csd.get(u, g_cd.get(u[:4], g_prov)) for u in uid])
    pop24 = pop21 * factor
    # Scale to the province total the panel used (App. 7 sums to 4,888,723), so both bases split the same 91 seats.
    total24 = 4888723
    pop24 *= total24 / pop24.sum()

    csdpop = pd.Series(pop21).groupby(uid).sum()
    reg = np.array([region(n, t, csdpop.get(u, 0)) for n, t, u in zip(name, typ, uid)])
    ent = pd.DataFrame({"region": reg, "p21": pop21, "p24": pop24}).groupby("region").sum()
    ent["seats_2021"] = ent.p21 / ent.p21.sum() * K
    ent["seats_2024"] = ent.p24 / ent.p24.sum() * K
    ent["shift"] = ent.seats_2024 - ent.seats_2021

    # Validation and real maps on both bases.
    real = {}
    valid = {}
    for k, g in maps().items():
        tmp = HERE / f"_{k}.gpkg"
        g.to_file(tmp, driver="GPKG")
        lab = assign(pts, tmp, "division").to_numpy()
        tmp.unlink()
        df = pd.DataFrame({"d": lab, "p21": pop21, "p24": pop24}).groupby("d").sum()
        df["published"] = g.set_index("division").total.reindex(df.index)
        n = len(df)
        row = {"divisions": n}
        for b in ("p21", "p24", "published"):
            avg = df[b].sum() / n
            dev = (df[b] - avg) / avg * 100
            row[b] = {"mad": round(float((df[b] - avg).abs().mean())), "max_abs_dev_pct": round(float(dev.abs().max()), 1),
                      "outside_25": int((dev.abs() > 25).sum())}
        real[k] = row
        e24 = ((df.p24 - df.published) / df.published * 100)
        e21 = ((df.p21 * total24 / df.p21.sum() - df.published) / df.published * 100)
        valid[k] = {"growth_basis_mean_abs_err_pct": round(float(e24.abs().mean()), 2),
                    "growth_basis_max_abs_err_pct": round(float(e24.abs().max()), 2),
                    "growth_basis_worst": str(e24.abs().idxmax()),
                    "census_2021_scaled_mean_abs_err_pct": round(float(e21.abs().mean()), 2),
                    "census_2021_scaled_max_abs_err_pct": round(float(e21.abs().max()), 2)}

    # Measure 4: Calgary + Edmonton city districts, the only region count the chain files record.
    setd = []
    for f in sorted(SETD.glob("chain*_samples.csv")):
        setd.append(pd.read_csv(f, usecols=["n_city_districts"]).n_city_districts)
    nc = pd.concat(setd) if setd else pd.Series(dtype=float)
    big = ent.loc[["Calgary", "Edmonton"]]
    out = {
        "plan": "preregistration/population_basis_2026-11-07.md",
        "growth_factor_source_share_of_pop": {s: round(float(pop21[src == s].sum() / pop21.sum()), 4) for s in ("csd", "cd", "province")},
        "province_growth_2021_2024": round(g_prov, 4),
        "entitlement": {r: {k: round(float(v), 3) for k, v in row.items()} for r, row in ent.iterrows()},
        "max_abs_shift_seats": round(float(ent["shift"].abs().max()), 3),
        "decision": "at least one region shifts by 0.5 seats or more" if (ent["shift"].abs() >= 0.5).any() else "no region shifts by 0.5 seats",
        "validation_vs_published": valid,
        "real_maps": real,
        "setD_city_districts": {"plans": int(len(nc)), "median": float(nc.median()) if len(nc) else None,
                                "p5": float(nc.quantile(.05)) if len(nc) else None, "p95": float(nc.quantile(.95)) if len(nc) else None,
                                "note": "n_city_districts counts districts at least half Calgary or Edmonton; balanced on 2021"},
        "calgary_edmonton_seats": {"2021": round(float(big.seats_2021.sum()), 3), "2024": round(float(big.seats_2024.sum()), 3)},
    }
    (HERE / "population_basis.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
