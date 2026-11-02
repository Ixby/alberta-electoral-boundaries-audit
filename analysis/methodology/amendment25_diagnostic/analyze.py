"""Diagnostic: special (s.15(2)) districts per plan, and those that qualify only under the status reading of (c)."""
import sys, json, glob, re, warnings
warnings.filterwarnings("ignore")
from collections import Counter
import numpy as np, pandas as pd
R = "/home/user/alberta-electoral-boundaries-audit"
sys.path.insert(0, R + "/analysis/scripts"); sys.path.insert(0, R + "/analysis/utils")
sys.path.insert(0, "/tmp/claude-0/-home-user-alberta-electoral-boundaries-audit/9af3a5a2-4682-51b8-9140-74f10ed8aad4/scratchpad/calib")
import s15_2_criteria as sc
import cse_s152 as cse
def load(p):
    t = pd.read_csv(p, index_col="node", keep_default_na=False)
    t["reserves"] = t["reserves"].apply(lambda r: json.loads(r) if r else np.nan)
    t["road_km"] = t["road_km"].astype(float); t["town"] = t["town"].astype(str)
    return t
P = load(R + "/data/outputs/s15_2_va_criteria.csv"); S = load(R + "/data/outputs/s15_2_va_criteria_status.csv")
res_area = cse._reserve_areas()
def scan(d):
    files = sorted(glob.glob(d + "/plan_*.json")); rows = []
    for f in files:
        a = {int(k): int(v) for k, v in json.load(open(f)).items()}
        lab = np.array([a[n] for n in P.index]); k = len(set(lab))
        cp = sc.criteria(P, lab, None, res_area); cs = sc.criteria(S, lab, None, res_area)
        avg = P["pop"].sum() / k
        spec = [d_ for d_, v in cp.items() if v["pop"] / avg - 1 < -0.25]
        so = [(d_, round(100 * (cp[d_]["pop"] / avg - 1), 1), cp[d_]["towns_over_8000"]) for d_ in spec if cs[d_]["n"] >= 3 and cp[d_]["n"] < 3]
        bad = [d_ for d_ in spec if cs[d_]["n"] < 3 and cp[d_]["n"] < 3]
        rows.append({"plan": f.split("/")[-1], "k": k, "special": len(spec), "status_only": so, "neither": len(bad)})
    return rows
for name, d in [(a.split("=")[0], a.split("=")[1]) for a in sys.argv[1:]]:
    rows = scan(d)
    n = len(rows); so = [r for r in rows if r["status_only"]]
    print(f"\n{name}: {n} plans; special districts per plan {Counter(r['special'] for r in rows)}; plans with a special district that qualifies only under the status reading: {len(so)} of {n}; plans with a special district meeting neither reading: {sum(1 for r in rows if r['neither'])}")
    c = Counter(t for r in so for _, _, ts in r["status_only"] for t in ts)
    print("  cities in those districts:", dict(c))
    for r in so[:5]: print("  e.g.", r["plan"], r["status_only"])
