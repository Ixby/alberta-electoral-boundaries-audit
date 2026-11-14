# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
"""Measure 4 support: each real map's count of districts at least half Calgary or Edmonton (2021
population), the definition close_seats_ensemble.py uses for n_city_districts."""
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

va, _ = me.build_va_graph(verbose=False)
pts = va[["geometry"]].copy()
pts["geometry"] = va.geometry.representative_point()
csd = gpd.read_file(ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(pts.crs)
j = gpd.sjoin(pts, csd[["CSDNAME", "geometry"]], how="left", predicate="within")
name = j[~j.index.duplicated(keep="first")].reindex(pts.index).CSDNAME.fillna("").to_numpy()
pop = va.pop_2021.to_numpy(float)
out = {}
for k, (f, col) in MAPS.items():
    d = assign(pts, f, col).to_numpy()
    df = pd.DataFrame({"d": d, "p": pop, "cal": pop * (name == "Calgary"), "edm": pop * (name == "Edmonton")}).groupby("d").sum()
    out[k] = {"districts": len(df), "n_city_districts": int(((df.cal >= .5 * df.p) | (df.edm >= .5 * df.p)).sum()),
              "calgary": int((df.cal >= .5 * df.p).sum()), "edmonton": int((df.edm >= .5 * df.p).sum())}
print(json.dumps(out, indent=1))
(HERE / "city_counts.json").write_text(json.dumps(out, indent=1))

# City-versus-rest gap (close_seats_ensemble.py's definition) on 2021 census and on the published figures.
sys.path.insert(0, str(ROOT / "findings/osi_rebuild"))
from rebuild_da_2024 import maps  # noqa: E402

pubs = {k: g.set_index("division").total for k, g in maps().items()}
for k, (f, col) in MAPS.items():
    if k not in pubs:
        continue
    d = assign(pts, f, col).to_numpy()
    df = pd.DataFrame({"d": d, "p": pop, "cal": pop * (name == "Calgary"), "edm": pop * (name == "Edmonton")}).groupby("d").sum()
    city = (df.cal >= .5 * df.p) | (df.edm >= .5 * df.p)
    df["pub"] = pubs[k].reindex(df.index)
    for b in ("p", "pub"):
        out[k][f"city_gap_pct_{'2021' if b == 'p' else 'published'}"] = round(float((df[b][city].mean() - df[b][~city].mean()) / df[b][~city].mean() * 100), 2)
print(json.dumps(out, indent=1))
(HERE / "city_counts.json").write_text(json.dumps(out, indent=1))
