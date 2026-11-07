# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
changed_redraw.py

Runs preregistration/changed_districts_2026-11-07.md: neutral regional redraws of each group of
districts that changed between the commission majority's map and the panel's, at each map's own
district count, city-blind and city-aware (weight 0.5). Measures where the group's NDP votes land:
packed surplus, near-miss losses, submerged losses, and seats; plus the UCP packed surplus. All
ballots primary. Unregistered. Describes, does not show intent.

Usage: python -W ignore findings/changed_districts/changed_redraw.py groups
       python -W ignore findings/changed_districts/changed_redraw.py worker W NW
       python -W ignore findings/changed_districts/changed_redraw.py summarize
"""
import json
import random
import sys
from functools import partial
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "findings/hybrid_regions"))
import regional_redraw as RR  # noqa: E402

EPS, BURN, MUNI_W, NEAR = 0.25, 1000, 0.5, 0.10
OUT = HERE / "chains"
COLS = [f"{m}_{b}" for b in ("all", "ed") for m in ("ndp_seats", "ndp_packed", "ndp_near", "ndp_far", "ucp_packed")]


def groups():
    B = RR.base()
    p, m = B["panel"], B["majority"]
    G = nx.Graph()
    G.add_edges_from({("P:" + a, "M:" + c) for a, c in zip(p, m)})
    out = {}
    for comp in nx.connected_components(G):
        P = sorted(x[2:] for x in comp if x.startswith("P:"))
        M = sorted(x[2:] for x in comp if x.startswith("M:"))
        mask = np.isin(p, P)
        if len(P) == 1 and len(M) == 1 and (mask == np.isin(m, M)).all() and P == M:
            continue
        if len(P) == 1 and len(M) == 1 and (mask == np.isin(m, M)).all():
            continue
        name = "west_calgary" if any("Calgary" in x for x in P) else ("south_central" if any("Lethbridge" in x for x in P) else "north_edmonton")
        assert (np.isin(m, M) == mask).all()
        out[name] = {"panel": P, "majority": M, "n_vas": int(mask.sum())}
    (HERE / "groups.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    return out


def setup(group):
    B = RR.base()
    g = json.loads((HERE / "groups.json").read_text())[group]
    mask = np.isin(B["panel"], g["panel"])
    nodes = [n for n in B["graph"].nodes if mask[n]]
    sub = B["graph"].subgraph(nodes).copy()
    comps = sorted(nx.connected_components(sub), key=len, reverse=True)
    cen = B["geom"].centroid
    anchor = {}
    for c in comps[1:]:
        cc = gpd.GeoSeries([cen[n] for n in c]).union_all().centroid
        a = min(comps[0], key=lambda q: cen[q].distance(cc))
        for n in c:
            anchor[n] = a
    return {"B": B, "g": g, "graph": sub.subgraph(comps[0]).copy(), "nodes": nodes, "anchor": anchor}


def measures(S, lab_by_node):
    B = S["B"]
    idx = np.array(S["nodes"])
    lab = np.array([lab_by_node[n] if n in lab_by_node else lab_by_node[S["anchor"][n]] for n in S["nodes"]])
    _, inv = np.unique(lab, return_inverse=True)
    out = []
    for key in ("all", "ed"):
        u, n = B[key][0][idx], B[key][1][idx]
        U, N = np.bincount(inv, weights=u), np.bincount(inv, weights=n)
        T = U + N
        m = (N - U) / T
        ndp_win = N > U
        nt, ut = N.sum(), U.sum()
        out += [int(ndp_win.sum()), float((N - T / 2)[ndp_win].sum() / nt), float(N[(~ndp_win) & (m > -NEAR)].sum() / nt),
                float(N[(~ndp_win) & (m <= -NEAR)].sum() / nt), float((U - T / 2)[~ndp_win].sum() / ut)]
    return out


def run(group, k, variant, chain, steps):
    from gerrychain import MarkovChain, Partition
    from gerrychain.accept import always_accept
    from gerrychain.constraints import contiguous, within_percent_of_ideal_population
    from gerrychain.proposals import recom
    from gerrychain.tree import recursive_tree_part
    from gerrychain.updaters import Tally

    S = setup(group)
    salt = f"changed_{group}_{k}_{variant}_{chain}"
    seed = RR.get_canonical_seed(salt)
    random.seed(seed)
    np.random.seed(seed % 2**32)
    g = S["graph"]
    for n in g.nodes:
        g.nodes[n]["pop_rs"] = float(S["B"]["pop"][n])
        g.nodes[n]["csduid"] = S["B"]["csduid"][n]
    for n, a in S["anchor"].items():
        g.nodes[a]["pop_rs"] += float(S["B"]["pop"][n])
    total = sum(g.nodes[n]["pop_rs"] for n in g.nodes)
    ideal = total / k
    assignment = recursive_tree_part(g, range(k), ideal, "pop_rs", EPS / 2, node_repeats=2)
    part = Partition(g, assignment, updaters={"population": Tally("pop_rs", alias="population")})
    surcharge = {"csduid": MUNI_W} if variant == "muni" else None
    prop = partial(recom, pop_col="pop_rs", pop_target=ideal, epsilon=EPS, node_repeats=2, region_surcharge=surcharge)
    ch = MarkovChain(prop, constraints=[contiguous, within_percent_of_ideal_population(part, EPS)],
                     accept=always_accept, initial_state=part, total_steps=steps + BURN)
    rows = [measures(S, p.assignment) for i, p in enumerate(ch) if i >= BURN]
    OUT.mkdir(exist_ok=True)
    stem = f"{group}_k{k}_{variant}_{chain}"
    pd.DataFrame(rows, columns=COLS).to_csv(OUT / f"{stem}.csv", index=False)
    (OUT / f"{stem}.json").write_text(json.dumps({"group": group, "k": k, "variant": variant, "chain": chain, "seed_salt": salt,
                                                   "seed": seed, "steps_kept": steps, "burn_in": BURN, "n_vas": len(S["nodes"])}, indent=1))
    print(f"[{stem}] done", flush=True)


def jobs():
    gs = json.loads((HERE / "groups.json").read_text())
    js = []
    for name, g in gs.items():
        ks = sorted({len(g["panel"]), len(g["majority"])})
        for k in ks:
            for v in ("blind", "muni"):
                js += [(name, k, v, c, 25000) for c in (1, 2)]
    return js


def worker(w, nw):
    for i, (gname, k, v, c, s) in enumerate(jobs()):
        if i % nw == w and not (OUT / f"{gname}_k{k}_{v}_{c}.csv").exists():
            print(f"[worker {w}] start {gname} k{k} {v} {c}", flush=True)
            run(gname, k, v, c, s)


def summarize():
    gs = json.loads((HERE / "groups.json").read_text())
    out = {"plan": "preregistration/changed_districts_2026-11-07.md", "primary_ballots": "all", "groups": {}}
    for name, g in gs.items():
        S = setup(name)
        real = {"panel": (len(g["panel"]), dict(zip(COLS, measures(S, {n: S["B"]["panel"][n] for n in S["nodes"]})))),
                "majority": (len(g["majority"]), dict(zip(COLS, measures(S, {n: S["B"]["majority"][n] for n in S["nodes"]}))))}
        blk = {"panel_divisions": g["panel"], "majority_divisions": g["majority"], "n_vas": g["n_vas"], "maps": {}}
        for mp, (k, vals) in real.items():
            blk["maps"][mp] = {"k": k, "values_all": {c: vals[c] for c in COLS if c.endswith("_all")}, "variants": {}}
            for v in ("blind", "muni"):
                files = sorted(OUT.glob(f"{name}_k{k}_{v}_*.csv"))
                if not files:
                    continue
                d = pd.concat([pd.read_csv(f) for f in files])
                vb = {"n_plans": int(len(d))}
                for c in ("ndp_seats_all", "ndp_packed_all", "ndp_near_all", "ndp_far_all", "ucp_packed_all"):
                    x = d[c].to_numpy(float)
                    val = float(vals[c])
                    pct = round(100 * float((x < val).mean() + 0.5 * (x == val).mean()), 2)
                    vb[c] = {"q05": round(float(np.quantile(x, 0.05)), 4), "q50": round(float(np.quantile(x, 0.5)), 4),
                             "q95": round(float(np.quantile(x, 0.95)), 4), "value": round(val, 4), "pct": pct, "flag": pct >= 95 or pct <= 5}
                vb["chain_medians_ndp_far"] = [round(float(pd.read_csv(f).ndp_far_all.median()), 4) for f in files]
                blk["maps"][mp]["variants"][v] = vb
        out["groups"][name] = blk
    (HERE / "summary.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    for name, blk in out["groups"].items():
        for mp, mb in blk["maps"].items():
            for v, vb in mb["variants"].items():
                print(name, mp, f"k{mb['k']}", v, {c[:-4]: (vb[c]["value"], vb[c]["pct"]) for c in vb if c.endswith("_all")})


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "groups":
        print(json.dumps(groups(), indent=1))
    elif cmd == "worker":
        RR.base()
        worker(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "run":
        run(sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6]))
    else:
        summarize()
