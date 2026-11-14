# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""How noisy is the Step C population check on districts whose geometry is known?

For each panel district whose name is also a commission-majority district, the 2021
voting-area population inside the commission geometry (representative point), scaled to
the App. 7 provincial total, is compared with the panel's stated population. Only the
'tuning' and 'unchanged' rows have known geometry; the others share a name but were changed.
Usage: python findings/a10_dev/population_check_noise.py > findings/a10_dev/population_check_noise.csv
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis/scripts"))
import a7_stepb_calibrate as C  # noqa: E402
import a9_stepb_reconstruct_v3 as V3  # noqa: E402
import mcmc_ensemble as me  # noqa: E402

va, _ = me.build_va_graph(verbose=False)
va = va.to_crs(3400)
pts = gpd.GeoSeries(va.geometry.representative_point(), crs=3400)
app7 = pd.read_csv(C.APP7)
scale = app7.population.sum() / va.pop_2021.sum()
maj = gpd.read_file(C.MAJ).to_crs(3400)
maj["key"] = maj.EDName2025.map(C.norm)
unch = {C.norm(n) for n in json.loads((REPO / "analysis/a8/unchanged_56.json").read_text(encoding="utf-8"))["districts"]} | {"Calgary-Acadia"}
tun = {C.norm(app7.set_index("ed_number").loc[n, "district"]) for n in V3.TUNING}
print("district,set,stated,va2021_scaled,diff_pct")
for _, r in app7.sort_values("ed_number").iterrows():
    k = C.norm(r.district)
    if k not in set(maj.key):
        continue
    g = maj.loc[maj.key == k, "geometry"].union_all()
    p = va.pop_2021[pts.within(g)].sum() * scale
    s = "tuning" if k in tun else ("unchanged" if k in unch else "changed_same_name")
    print(f'"{k}",{s},{r.population},{round(p)},{100 * (p - r.population) / r.population:.1f}')
