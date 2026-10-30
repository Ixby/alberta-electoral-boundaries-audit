"""Independent post-hoc check of an s.15(2)-mode chain (AC1, AC2).

Replays nothing: reads the per-step CSV's s152_districts column and, for the
final state in the checkpoint, re-derives every division's deviation and
criteria count from the per-VA table with plain pandas (no chain code).
For the registered table (s15_2_va_criteria.csv: road_km, town, reserves, border_km)
the final state is scored with the Audit session's own criteria() instead.
The samples CSV holds per-plan counts, not maps, so only the final state can be
re-scored from scratch; earlier plans are checked through the count column.
Usage: check_s152_run.py <repo> <samples.csv> <criteria.csv> <k> [dir of s15_2_criteria_audit.py]
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
c = pd.read_csv(crit, index_col="node", keep_default_na=False)
lab = pd.Series({int(n): v for n, v in ck["assignment"].items()})
ideal = pop.sum() / k
if "reserves" in c.columns:
    # registered table: Audit's criteria() (thresholds and town reading live there)
    sys.path.insert(0, sys.argv[5] if len(sys.argv) > 5 else ".")
    import close_seats_ensemble as cse  # noqa: E402  (only for the reserve areas)
    import s15_2_criteria_audit as audit  # noqa: E402
    nodes = list(pop.index)
    tab = c.loc[nodes].copy()
    tab["pop"] = pop.loc[nodes].to_numpy()
    tab["road_km"] = tab["road_km"].astype(float)
    for col in ("area_km2", "border_km"):
        tab[col] = tab[col].astype(float)
    tab["reserves"] = [json.loads(r) if r else None for r in tab["reserves"]]
    out = audit.criteria(tab, lab.loc[nodes].to_numpy(), None, cse._reserve_areas())
    agg = pd.DataFrame({d: {"pop": v["pop"], "met": v["n"]} for d, v in out.items()}).T
    agg["dev"] = agg["pop"] / ideal - 1
else:
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
