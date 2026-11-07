# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
rural_voice.py

Runs preregistration/rural_voice_2026-11-07.md: rural residents in mixed city-and-rural divisions on
the commission majority, minority, panel (reconstruction v3) and ¶167 maps. Rural = a voting area
outside every 2021 city (CY) or town (T) CSD. All ballots are the primary votes; election-day votes
are reported beside. Unregistered. Describes population and 2023 votes, not intent.

Usage: python -I -W ignore findings/rural_voice/rural_voice.py
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
sys.path.insert(0, str(ROOT / "findings/packing_cracking"))
import mcmc_ensemble as me  # noqa: E402
from real_maps import MAPS, assign  # noqa: E402

ALL = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
RURAL_MUNI = {"MD", "SA", "ID", "SV", "VL", "IRI", "MS", "S-É", "NO", "CM", "SNO"}  # reported for measure 3: MD/county types only


def main():
    va, _ = me.build_va_graph(verbose=False)
    allb = gpd.read_file(ALL, ignore_geometry=True)
    assert len(allb) == len(va)
    pts = va[["geometry"]].copy()
    pts["geometry"] = va.geometry.representative_point()
    csd = gpd.read_file(CSD).to_crs(pts.crs)
    j = gpd.sjoin(pts, csd[["CSDUID", "CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    name, typ = j.CSDNAME.fillna("").to_numpy(), j.CSDTYPE.fillna("").to_numpy()
    rural = ~np.isin(typ, ["CY", "T"])
    pop = va.pop_2021.to_numpy(float)
    votes = {"all": (allb.va_ucp.to_numpy(float), allb.va_ndp.to_numpy(float)),
             "election_day": (va.va_ucp.to_numpy(float), va.va_ndp.to_numpy(float))}
    x = pts.geometry.x.to_numpy()
    y = pts.geometry.y.to_numpy()
    cal = name == "Calgary"
    cal_cx = x[cal].mean()
    ylo, yhi = y[cal].min(), y[cal].max()
    focus_vas = {"lethbridge": np.isin(name, ["Lethbridge", "Lethbridge County"]),
                 "springbank": (name == "Rocky View County") & (x < cal_cx) & (y >= ylo) & (y <= yhi)}

    out = {"plan": "preregistration/rural_voice_2026-11-07.md", "rural_share_of_province": round(float(pop[rural].sum() / pop.sum()), 4), "maps": {}}
    for k, (f, col) in MAPS.items():
        d = assign(pts, f, col).to_numpy()
        df = pd.DataFrame({"d": d, "p": pop, "rp": pop * rural})
        for v, (u, n) in votes.items():
            df[f"u_{v}"], df[f"n_{v}"] = u, n
            df[f"ru_{v}"], df[f"rn_{v}"] = u * rural, n * rural
        g = df.groupby("d").sum()
        g["rshare"] = g.rp / g.p
        mixed = (g.rshare >= .05) & (g.rshare <= .95)
        m = {"divisions": len(g), "mixed_divisions": int(mixed.sum()),
             "rural_residents_in_urban_majority_divisions": int(round(g.rp[g.rshare < .5].sum())),
             "divisions_urban_majority_with_rural_5pct_plus": int(((g.rshare < .5) & mixed).sum())}
        for v in votes:
            win_u = g[f"u_{v}"] > g[f"n_{v}"]
            rwin_u = g[f"ru_{v}"] > g[f"rn_{v}"]
            over = mixed & (win_u != rwin_u)
            m[f"overridden_{v}"] = {"divisions": sorted(g.index[over].tolist()),
                                    "rural_residents": int(round(g.rp[over].sum())),
                                    "rural_two_party_voters": int(round((g[f"ru_{v}"] + g[f"rn_{v}"])[over].sum()))}
        # Measure 3: municipal districts and counties split (>= 5% of their population in each piece).
        mdx = pd.DataFrame({"m": name, "t": typ, "d": d, "p": pop})
        mdx = mdx[mdx.t == "MD"]
        sp = mdx.groupby(["m", "d"]).p.sum()
        tot = mdx.groupby("m").p.sum()
        pieces = (sp / tot.reindex(sp.index.get_level_values(0)).to_numpy() >= .05).groupby(level=0).sum()
        m["counties_split"] = {"counties": int(len(pieces)), "split_2plus": int((pieces >= 2).sum()),
                               "split_3plus": int((pieces >= 3).sum()), "max_pieces": int(pieces.max()),
                               "split_3plus_names": sorted(pieces.index[pieces >= 3].tolist())}
        # Measure 4: focus areas, division by division.
        for fa, mask in focus_vas.items():
            ds = sorted(set(d[mask]) - {None})
            rows = []
            for dd in ds:
                r = g.loc[dd]
                rows.append({"division": dd, "pop_2021": int(round(r.p)), "rural_share": round(float(r.rshare), 3),
                             "rural_residents": int(round(r.rp)),
                             "ucp_share_all": round(float(r.u_all / (r.u_all + r.n_all)), 3),
                             "rural_ucp_share_all": round(float(r.ru_all / (r.ru_all + r.rn_all)), 3) if r.ru_all + r.rn_all else None,
                             "urban_ucp_share_all": round(float((r.u_all - r.ru_all) / (r.u_all - r.ru_all + r.n_all - r.rn_all)), 3) if (r.u_all - r.ru_all + r.n_all - r.rn_all) else None})
            focus_rural = float(pop[mask & rural].sum())
            in_urban_maj = sum(pop[(d == dd) & mask & rural].sum() for dd in ds if g.loc[dd].rshare < .5)
            m[f"focus_{fa}"] = {"divisions": rows, "focus_rural_residents": int(round(focus_rural)),
                                "focus_rural_in_urban_majority_divisions": int(round(in_urban_maj))}
        out["maps"][k] = m
    (HERE / "rural_voice.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
