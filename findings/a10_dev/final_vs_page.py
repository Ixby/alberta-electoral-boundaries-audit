# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
final_vs_page.py
----------------

Amendment 10, extra check: does each placed district's final voting-area set match its own page?

For every district placed from its own page, compares the voting areas (VAs) whose representative point
lies inside the page's polygon (edNN.gpkg) with the VAs the final assignment gives that district.
"lost" = inside the page outline but assigned elsewhere; "gained" = assigned to it but outside the
outline. Population only; no votes. Reporting only.

Usage: python -W ignore findings/a10_dev/final_vs_page.py PAGES_DIR SNAP_DIR OUT_JSON
"""
import json
import sys

sys.path.insert(0, "analysis/scripts")
import geopandas as gpd  # noqa: E402
import pandas as pd  # noqa: E402

import a10_assemble as A  # noqa: E402

PAGES, SNAP, OUT = sys.argv[1:4]

va, _ = A.C.me.build_va_graph(verbose=False)
va = va[[c for c in va.columns if c in ("OBJECTID", "VA_NUMBER", "pop_2021", "geometry")]].to_crs(3400)
rp = va.geometry.representative_point()
asg = pd.read_csv(f"{SNAP}/va_assignment.csv")
assert len(asg) == len(va)
with open(f"{SNAP}/report.json", encoding="utf-8") as f:
    rep = json.load(f)
src = {r["ed"]: r["source"] for r in rep["districts"]}
out = []
for ed, s in sorted(src.items()):
    if s != "placed":
        continue
    red = gpd.read_file(f"{PAGES}/ed{ed:02d}.gpkg").to_crs(3400).union_all()
    inside = rp.within(red).to_numpy()
    mine = (asg.ed == ed).to_numpy()
    lost, gained = inside & ~mine, mine & ~inside
    out.append(dict(ed=ed, vas=int(mine.sum()),
                    lost=int(lost.sum()), lost_pop=float(va.pop_2021[lost].sum()),
                    lost_to={int(k): int(v) for k, v in asg.loc[lost, "ed"].value_counts().items()},
                    gained=int(gained.sum()), gained_pop=float(va.pop_2021[gained].sum()),
                    gained_ids=asg.loc[gained, "OBJECTID"].astype(int).tolist(),
                    gained_conf=asg.loc[gained, "confidence"].value_counts().to_dict(),
                    gained_rep_point_to_page_m=[round(float(red.distance(p)), 1) for p in rp[gained]]))
summary = dict(placed=len(out), with_mismatch=sum(1 for o in out if o["lost"] or o["gained"]),
               vas_lost=sum(o["lost"] for o in out), vas_gained=sum(o["gained"] for o in out))
for o in out:
    if o["lost"] or o["gained"]:
        print(o)
print(summary)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump({"pages": PAGES, "snap": SNAP, "summary": summary, "districts": out}, f, indent=1)
