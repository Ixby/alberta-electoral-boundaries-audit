"""Independent post-hoc check of an s.15(2)-mode chain (AC1, AC2).

Replays nothing: reads the per-step CSV's s152_districts column and, for the
final state in the checkpoint, re-derives every division's deviation and
criteria count from the per-VA table with plain pandas (no chain code).
Usage: check_s152_run.py <repo> <samples.csv> <criteria.csv> <k>
"""
import json
import sys
from pathlib import Path

import pandas as pd

repo, csv, crit, k = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
sys.path[:0] = [str(repo / "analysis/scripts"), str(repo / "analysis/utils")]
import mcmc_ensemble as me  # noqa: E402

d = pd.read_csv(csv)
print(f"rows {len(d)}; s152_districts per plan: max {d.s152_districts.max()}, "
      f"plans with >=1: {(d.s152_districts > 0).sum()} ({(d.s152_districts > 0).mean():.1%}); "
      f"value counts {d.s152_districts.value_counts().sort_index().to_dict()}")
assert d.s152_districts.max() <= 4, "AC1 FAIL: more than 4 s.15(2) divisions"

ck = json.loads(Path(str(csv) + ".ckpt.json").read_text())
va, graph = me.build_va_graph(verbose=False)
pop = pd.Series({n: graph.nodes[n]["pop_2021"] for n in graph.nodes()})
c = pd.read_csv(crit, index_col="node")
lab = pd.Series({int(n): v for n, v in ck["assignment"].items()})
ideal = pop.sum() / k
g = pd.DataFrame({"pop": pop, "lab": lab, "area": c.area_km2, "near": c.road_km <= 150,
                  "big": c.big_town.astype(bool), "res": c.reserve_or_metis.astype(bool), "bord": c.border.astype(bool)})
agg = g.groupby("lab").agg(pop=("pop", "sum"), area=("area", "sum"), near=("near", "any"),
                           big=("big", "any"), res=("res", "any"), bord=("bord", "any"))
agg["dev"] = agg["pop"] / ideal - 1
agg["met"] = (agg.area > 20000).astype(int) + (~agg.near) + (~agg.big) + agg.res + agg.bord
bad_band = agg[(agg.dev > 0.25) | (agg.dev < -0.50)]
low = agg[agg.dev < -0.25]
bad_low = low[low.met < 3]
print(f"final state: {len(agg)} divisions; dev range {agg.dev.min():+.1%}..{agg.dev.max():+.1%}; "
      f"s.15(2) divisions {len(low)} (criteria met: {sorted(low.met.tolist())})")
ok = len(agg) == k and bad_band.empty and bad_low.empty and len(low) <= 4
print("AC1 final-state check:", "PASS" if ok else f"FAIL band={len(bad_band)} lowcrit={len(bad_low)}")
