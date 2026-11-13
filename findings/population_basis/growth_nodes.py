# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Statistics Canada 2021 Census (Open Licence) | Alberta Office of Statistics and Information (OGL-Alberta)
"""
growth_nodes.py

Input for the set D rerun on the 2024 growth basis (proposed in
preregistration/population_basis_2026-11-07.md). Writes, per voting-area graph node, the 2021
census population and the municipal-growth population, computed with population_basis.py's exact
formula (CSD factor, else census-division factor, else province; total scaled to the panel's
4,888,723). Checks the result reproduces population_basis.json's regional entitlements. Also scores
the real maps' city-versus-rest gap and city-division counts on the growth basis, with
close_seats_ensemble.py's definitions. Unregistered. Describes population only, not intent.

Usage: python -I -W ignore findings/population_basis/growth_nodes.py
"""
import hashlib
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
sys.path.insert(0, str(HERE))
import mcmc_ensemble as me  # noqa: E402
from population_basis import CSD, K, region  # noqa: E402
from rebuild_da_2024 import csd_2024, maps  # noqa: E402
from real_maps import MAPS, assign  # noqa: E402


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
    # ---- same formula as population_basis.main() ----
    est = csd_2024()
    g_csd = (est.est_2024 / est.est_2021).to_dict()
    cd = est.groupby(est.index.str[:4]).sum()
    g_cd = (cd.est_2024 / cd.est_2021).to_dict()
    g_prov = float(est.est_2024.sum() / est.est_2021.sum())
    factor = np.array([g_csd.get(u, g_cd.get(u[:4], g_prov)) for u in uid])
    pop24 = pop21 * factor
    total24 = 4888723
    pop24 *= total24 / pop24.sum()
    csdpop = pd.Series(pop21).groupby(uid).sum()
    reg = np.array([region(n, t, csdpop.get(u, 0)) for n, t, u in zip(name, typ, uid)])
    # ---- end ----
    ent = pd.DataFrame({"region": reg, "p21": pop21, "p24": pop24}).groupby("region").sum()
    ref = json.loads((HERE / "population_basis.json").read_text())["entitlement"]
    for r in ent.index:
        s24 = ent.p24[r] / ent.p24.sum() * K
        assert abs(s24 - ref[r]["seats_2024"]) < 1e-3, (r, s24, ref[r]["seats_2024"])
    assert list(va.index) == sorted(graph.nodes())
    nodes = pd.DataFrame({"node": va.index, "pop_2021": pop21, "pop_growth": pop24, "region": reg,
                          "csdname": name})
    f = HERE / "growth_nodes.csv"
    nodes.to_csv(f, index=False, float_format="%.6f")
    sha = hashlib.sha256(f.read_bytes()).hexdigest()

    # Real maps on both bases, close_seats_ensemble.Geo.stats definitions.
    pubs = {k: g.set_index("division").total for k, g in maps().items()}
    real = {}
    for k, (fm, col) in MAPS.items():
        d = assign(pts, fm, col).to_numpy()
        row = {}
        for b, p in (("2021", pop21), ("growth", pop24)):
            df = pd.DataFrame({"d": d, "p": p, "cal": p * (name == "Calgary"), "edm": p * (name == "Edmonton")}).groupby("d").sum()
            city = (df.cal >= .5 * df.p) | (df.edm >= .5 * df.p)
            row[b] = {"districts": len(df), "n_city_districts": int(city.sum()), "calgary": int((df.cal >= .5 * df.p).sum()),
                      "edmonton": int((df.edm >= .5 * df.p).sum()),
                      "city_gap_pct": round(float((df.p[city].mean() - df.p[~city].mean()) / df.p[~city].mean() * 100), 4)}
            # Districts by plurality region (the copy's reg_<region> definition), for plan measure 4.
            rp = pd.DataFrame({"d": d, "r": reg, "p": p}).groupby(["d", "r"]).p.sum().unstack(fill_value=0)
            top = rp.idxmax(axis=1).value_counts()
            row[b]["reg"] = {"reg_" + r.replace(" ", "_").replace(",", "").replace("+", "plus"): int(top.get(r, 0)) for r in sorted(set(reg))}
            if b == "2021" and k in pubs:
                pub = pubs[k].reindex(df.index)
                row["published"] = {"city_gap_pct": round(float((pub[city].mean() - pub[~city].mean()) / pub[~city].mean() * 100), 4)}
        real[k] = row
    out = {"plan": "preregistration/population_basis_2026-11-07.md", "growth_nodes_csv": "growth_nodes.csv", "growth_nodes_sha256": sha,
           "n_nodes": len(nodes), "total_2021": round(float(pop21.sum()), 1), "total_growth": round(float(pop24.sum()), 1),
           "entitlement_check": "reproduces population_basis.json seats_2024 within 0.001 for every region", "real_maps": real}
    (HERE / "growth_nodes.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
