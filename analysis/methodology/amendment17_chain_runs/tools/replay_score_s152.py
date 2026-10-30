"""Per-plan AC1 check for a finished set D chain, by replay.

The samples CSV keeps per-plan metrics, not maps. This reruns the chain's first
<steps> steps through the production entry point (close_seats_ensemble.run, same
seed, same flags), confirms the replayed rows are identical to the production
CSV's first rows (so the replayed maps ARE the production maps), and scores every
<keep>-th replayed map with the Audit session's own criteria() on the registered
table: all divisions within +/-25% except <= 4 that are 25-50% below average and
meet >= 3 criteria.
Usage: replay_score_s152.py <repo> <production samples.csv> <criteria.csv> <k> <idx>
                            <steps> <keep> <dir of s15_2_criteria_audit.py> <scratch dir>
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

repo, prod, crit = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
k, idx, steps, keep = (int(a) for a in sys.argv[4:8])
audit_dir, scratch = sys.argv[8], Path(sys.argv[9])
sys.path[:0] = [str(repo / "analysis/scripts"), str(repo / "analysis/utils"), audit_dir]
import close_seats_ensemble as cse  # noqa: E402
import s15_2_criteria_audit as audit  # noqa: E402

cse.S152_PATH = crit
cse.OPTS.update(s152=hashlib.sha256(crit.read_bytes()).hexdigest(), proposal_epsilon=0.5)
plans, seen = [], [0]
_next = cse.RecordingChain.__next__


def rec(self):
    p = _next(self)
    if seen[0] % keep == 0:
        plans.append({int(n): int(d) for n, d in p.assignment.items()})
    seen[0] += 1
    return p


cse.RecordingChain.__next__ = rec
out = scratch / f"replay_chain{idx}.csv"
cse.run("nk", idx, steps, 500, str(out), "", k)

a = pd.read_csv(out)
b = pd.read_csv(prod, nrows=len(a))
same = a.equals(b)
print(f"replayed {len(a)} rows; identical to production first {len(b)} rows: {same}")

c = pd.read_csv(crit, index_col="node", keep_default_na=False)
nodes = list(cse.GEO.nodes)
tab = c.loc[nodes].copy()
tab["pop"] = np.asarray(cse.GEO.pop)
for col in ("road_km", "area_km2", "border_km"):
    tab[col] = tab[col].astype(float)
tab["reserves"] = [json.loads(r) if r else None for r in tab["reserves"]]
res_area = cse._reserve_areas()
ideal = tab["pop"].sum() / k
viol, lows = 0, []
for asg in plans:
    m = audit.criteria(tab, [asg[n] for n in nodes], None, res_area)
    dev = {d: v["pop"] / ideal - 1 for d, v in m.items()}
    low = [d for d, x in dev.items() if x < -0.25]
    bad = len(m) != k or any(x > 0.25 or x < -0.50 for x in dev.values()) \
        or any(m[d]["n"] < 3 for d in low) or len(low) > 4
    viol += bool(bad)
    lows.append(len(low))
lows = np.array(lows)
print(f"scored {len(plans)} maps with Audit criteria(): AC1 violations {viol}; "
      f"s.15(2) divisions per map max {lows.max()}, share with >=1 {np.mean(lows > 0):.1%}")
print("RESULT", "PASS" if same and viol == 0 else "FAIL")
