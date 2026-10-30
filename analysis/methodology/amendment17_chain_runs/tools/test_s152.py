"""s.15(2) mode acceptance test (governance spec AC1, AC2, AC6).

Runs an nk chain in s.15(2) mode in-process, records EVERY plan's assignment,
and checks each plan with an independent pandas implementation of the rule
(no chain code): all divisions within +/-25% except <= 4 that are 25-50% below
average and meet >= 3 criteria.
Usage: test_s152.py <repo> <criteria.csv> <k> <idx> <steps> [chunk]
"""
import hashlib
import random
import sys
import time
from functools import partial
from pathlib import Path

import numpy as np
import pandas as pd

repo, crit, k, idx, steps = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
chunk = int(sys.argv[6]) if len(sys.argv) > 6 else 500
sys.path[:0] = [str(repo / "analysis/scripts"), str(repo / "analysis/utils")]
import close_seats_ensemble as cse  # noqa: E402

me = cse.me
cse.S152_PATH = crit
cse.OPTS.update(proposal_epsilon=0.5, s152=hashlib.sha256(crit.read_bytes()).hexdigest())
va, graph = me.build_va_graph(verbose=False)
cse.GEO = cse.Geo(va, graph)
s = cse.chain_seed(idx)
np.random.seed(s); random.seed(s)
from gerrychain.tree import bipartition_tree, recursive_tree_part  # noqa: E402
total = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
st = np.random.get_state(), random.getstate()
np.random.seed(s + 999); random.seed(s + 999)
state = recursive_tree_part(graph, parts=list(range(k)), pop_target=total / k, pop_col="pop_2021",
                            epsilon=0.25, node_repeats=5, method=partial(bipartition_tree, max_attempts=50000))
np.random.set_state(st[0]); random.setstate(st[1])
me._bpt_global = cse.bipartition_tree_fastfail
cse.set_s152(graph, k)

plans = []
_next = cse.RecordingChain.__next__


KEEP = int(sys.argv[8]) if len(sys.argv) > 8 else 1  # store every KEEP-th plan (memory)
_seen = [0]


def rec(self):
    p = _next(self)
    if _seen[0] % KEEP == 0:
        plans.append(np.array([p.assignment[n] for n in cse.GEO.nodes], dtype=np.int16))
    _seen[0] += 1
    return p


cse.RecordingChain.__next__ = rec
part = cse._partition(graph, state)
t0 = time.time(); per_chunk = []
done = 0
while done < steps:
    t1 = time.time()
    rows, p = me.run_ensemble(graph, part, chunk, pop_deviation=0.5, verbose=False, return_final_partition=True,
                              seed=s, proposal_epsilon=0.5)
    part = cse._partition(graph, {int(n): int(d) for n, d in p.assignment.items()})
    done += chunk; per_chunk.append(time.time() - t1)
    print(f"{done}/{steps} {time.time()-t0:.0f}s", flush=True)

# independent check of every plan
import json  # noqa: E402

c = pd.read_csv(crit, index_col="node", keep_default_na=False).loc[cse.GEO.nodes]
pop = cse.GEO.pop
ideal = pop.sum() / k
if "reserves" in c.columns:
    # registered table: score with the Audit session's own criteria() (s15_2_criteria.py), not chain code
    sys.path.insert(0, sys.argv[7] if len(sys.argv) > 7 else ".")
    import s15_2_criteria_audit as audit  # noqa: E402
    tab = c.copy()
    tab["pop"] = pop
    tab["road_km"] = tab["road_km"].astype(float)
    tab["reserves"] = [json.loads(r) if r else None for r in tab["reserves"]]
    res_area = cse._reserve_areas()

    def met_by_district(lab):
        out = audit.criteria(tab, lab, None, res_area)
        return {d: (v["pop"], v["n"]) for d, v in out.items()}
else:
    area = c.area_km2.to_numpy(); near = (c.road_km <= 150).to_numpy(); big = c.big_town.astype(bool).to_numpy()
    res = c.reserve_or_metis.astype(bool).to_numpy(); bord = c.border.astype(bool).to_numpy()

    def met_by_district(lab):
        df = pd.DataFrame({"lab": lab, "pop": pop, "area": area, "near": near, "big": big, "res": res, "bord": bord})
        a = df.groupby("lab").agg(pop=("pop", "sum"), area=("area", "sum"), near=("near", "any"),
                                  big=("big", "any"), res=("res", "any"), bord=("bord", "any"))
        met = (a.area > 20000).astype(int) + (~a.near) + (~a.big) + a.res + a.bord
        return {d: (a.at[d, "pop"], int(met[d])) for d in a.index}

viol, lows = 0, []
for i, lab in enumerate(plans):
    m = met_by_district(lab)
    dev = {d: p / ideal - 1 for d, (p, n) in m.items()}
    low = [d for d, x in dev.items() if x < -0.25]
    bad = (len(m) != k) or any(x > 0.25 or x < -0.50 for x in dev.values()) \
        or any(m[d][1] < 3 for d in low) or len(low) > 4
    viol += bool(bad); lows.append(len(low))

# constraint rejection checks on synthetic states (Audit item 3)
class _P(dict):
    def __init__(self, pops, parts):
        super().__init__(population=pops); self.parts = parts


final = {int(n): int(d) for n, d in part.assignment.items()}
parts = {}
for n, d in final.items():
    parts.setdefault(d, set()).add(n)
pops = {d: sum(graph.nodes[n]["pop_2021"] for n in ns) for d, ns in parts.items()}
assert cse.s152_constraint(_P(pops, parts)), "final state must pass"


def n_met(nodes):
    a = cse._new_agg()
    for n in nodes:
        cse._add(a, cse.S152["attrs"][n])
    return cse.s152_met(a)


urban = min(parts, key=lambda d: sum(cse.S152["attrs"][n][0] for n in parts[d]))  # smallest-area district
assert n_met(parts[urban]) < 3
qual = [d for d in parts if n_met(parts[d]) >= 3]
checks = {
    "district above +25% rejected": not cse.s152_constraint(_P({**pops, urban: ideal * 1.26}, parts)),
    "district below -50% rejected": not cse.s152_constraint(_P({**pops, urban: ideal * 0.49}, parts)),
    "-30% district with < 3 criteria rejected": not cse.s152_constraint(_P({**pops, urban: ideal * 0.70}, parts)),
}
if qual:
    q = qual[0]
    five = {**parts, **{f"q{i}": parts[q] for i in range(5)}}
    fivep = {**pops, **{f"q{i}": ideal * 0.70 for i in range(5)}}
    four = {**parts, **{f"q{i}": parts[q] for i in range(4)}}
    fourp = {**pops, **{f"q{i}": ideal * 0.70 for i in range(4)}}
    others_low = sum((p / ideal - 1) < -0.25 for p in pops.values())
    if others_low == 0:
        checks["4 qualifying -30% districts accepted"] = cse.s152_constraint(_P(fourp, four))
    checks["5 qualifying -30% districts rejected"] = not cse.s152_constraint(_P(fivep, five))
for name, ok in checks.items():
    print(f"constraint check: {name}: {'PASS' if ok else 'FAIL'}")
lows = np.array(lows)
print(f"plans {len(plans)}; AC1 violations {viol}; s.15(2) divisions per plan: max {lows.max()}, "
      f"share of plans with >=1 {np.mean(lows > 0):.1%}, counts {dict(zip(*np.unique(lows, return_counts=True)))}")
print(f"AC6 seconds per {chunk} steps: median {np.median(per_chunk):.1f}, max {max(per_chunk):.1f}")
print("AC1", "PASS" if viol == 0 else "FAIL", "| AC2", "PASS" if lows.max() > 0 and lows.max() <= 4 else "FAIL",
      "| constraint checks", "PASS" if all(checks.values()) else "FAIL")
