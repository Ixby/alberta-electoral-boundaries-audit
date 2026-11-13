# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
regional_south.py

Signal F of preregistration/six_signals_2026-11-07.md: a neutral ReCom redraw of only the panel's
southern group (8 divisions), every other division held fixed. Records, per plan, the region's NDP
seats and where Lethbridge's NDP votes land, on both ballot sets, then places the panel's and the
para 167 configurations against that distribution. Unregistered. Seeds from drand (salt
regional_south_<chain>). Measures where votes land, not intent.

Usage: python -W ignore findings/six_signals/regional_south.py run CHAIN STEPS
       python -W ignore findings/six_signals/regional_south.py summarize
"""
import json
import random
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
from drand_seed import get_canonical_seed  # noqa: E402
from real_maps import MAPS, assign  # noqa: E402

ALL = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
LETHBRIDGE = "4802012"
NEAR = 0.10
BASE_EPS = 0.25
BURN = 1000
OUT = HERE / "regional_south"


def setup():
    va, graph = me.build_va_graph(verbose=False)
    base = gpd.read_file(ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg").to_crs(3400)
    assert len(va) == len(base) and (va.index == base.index).all()
    pts = base[["geometry"]].copy()
    pts["geometry"] = base.geometry.representative_point()
    panel = assign(pts, *MAPS["panel"])
    para = assign(pts, *MAPS["para167"])
    comp = json.loads((ROOT / "findings/iap_para167/comparison.json").read_text())
    grp = next(g for g in comp["groups"] if "Lethbridge" in g["panel"])
    region = panel.isin(grp["panel"]).to_numpy()
    assert (para[region].isin(grp["para167"])).all() and (~para[~region].isin(grp["para167"])).all()
    csd = gpd.read_file(CSD).to_crs(3400)
    j = gpd.sjoin(pts, csd[["CSDUID", "geometry"]], how="left", predicate="within")
    leth = (j[~j.index.duplicated(keep="first")].CSDUID.astype(str).reindex(pts.index) == LETHBRIDGE).to_numpy()
    allb = gpd.read_file(ALL, ignore_geometry=True)
    nodes = [n for n in graph.nodes if region[n]]
    sub = graph.subgraph(nodes).copy()
    # The region's voting-area graph has one small piece (6 VAs of Banff-Canmore-Diamond Valley) that
    # touches the region only through outside VAs. It is held with the region node nearest to it: its
    # people count toward that node's district and its votes go wherever that node goes.
    import networkx as nx
    comps = sorted(nx.connected_components(sub), key=len, reverse=True)
    main = comps[0]
    cen = base.geometry.centroid
    anchor = {}
    for c in comps[1:]:
        cc = gpd.GeoSeries([cen[n] for n in c]).unary_union.centroid
        a = min(main, key=lambda m: cen[m].distance(cc))
        for n in c:
            anchor[n] = a
    graph_main = sub.subgraph(main).copy()
    return {"graph": graph_main, "nodes": nodes, "anchor": anchor, "panel": panel, "para": para, "leth": leth,
            "ed": (va.va_ucp.to_numpy(float), va.va_ndp.to_numpy(float)),
            "all": (allb.va_ucp.to_numpy(float), allb.va_ndp.to_numpy(float)), "pop": va.pop_2021.to_numpy(float)}


def measures(S, lab_by_node):
    idx = np.array(S["nodes"])
    # Real maps label every VA; chain plans omit the held piece, which takes its anchor's district.
    lab = np.array([lab_by_node[n] if n in lab_by_node else lab_by_node[S["anchor"][n]] for n in S["nodes"]])
    _, inv = np.unique(lab, return_inverse=True)
    out = []
    for key in ("ed", "all"):
        u, n = S[key][0][idx], S[key][1][idx]
        U, N = np.bincount(inv, weights=u), np.bincount(inv, weights=n)
        m = (N - U) / (N + U)
        L = S["leth"][idx]
        ln = np.bincount(inv[L], weights=n[L], minlength=len(U))
        tot = ln.sum()
        out += [int((m > 0).sum()), ln[m > 0].sum() / tot, ln[(m <= 0) & (m > -NEAR)].sum() / tot, ln[m <= -NEAR].sum() / tot]
    lp = np.bincount(inv[S["leth"][idx]], weights=S["pop"][idx][S["leth"][idx]], minlength=len(U))
    out.append(int((lp >= 0.02 * lp.sum()).sum()))
    return out


COLS = ["ndp_seats_ed", "leth_won_ed", "leth_near_ed", "leth_far_ed", "ndp_seats_all", "leth_won_all", "leth_near_all", "leth_far_all", "leth_pieces"]


def run(chain, steps):
    from gerrychain import MarkovChain, Partition
    from gerrychain.accept import always_accept
    from gerrychain.constraints import contiguous, within_percent_of_ideal_population
    from gerrychain.proposals import recom
    from gerrychain.updaters import Tally
    from functools import partial

    S = setup()
    seed = get_canonical_seed(f"regional_south_{chain}")
    random.seed(seed)
    np.random.seed(seed % 2**32)
    g = S["graph"]
    for n in g.nodes:
        g.nodes[n]["pop_rs"] = float(S["pop"][n])
    for n, a in S["anchor"].items():
        g.nodes[a]["pop_rs"] += float(S["pop"][n])
    # Deviation from the plan (recorded in the README): the plan started from the panel's assignment.
    # On the voting-area graph two of the panel's districts are not contiguous, and repairing them
    # pushed one district to +62%, which would have forced a +/-62% band. So each chain starts from
    # a random plan drawn within the +/-25% band, and the first BURN steps are discarded.
    from gerrychain.tree import recursive_tree_part
    repaired = 0
    total = sum(g.nodes[n]["pop_rs"] for n in g.nodes)
    k = len(set(S["panel"][n] for n in S["nodes"]))
    assignment = recursive_tree_part(g, range(k), total / k, "pop_rs", BASE_EPS / 2, node_repeats=2)
    part = Partition(g, assignment, updaters={"population": Tally("pop_rs", alias="population")})
    ideal = sum(part["population"].values()) / len(part)
    start_dev = max(abs(p / ideal - 1) for p in part["population"].values())
    eps = BASE_EPS
    prop = partial(recom, pop_col="pop_rs", pop_target=ideal, epsilon=eps, node_repeats=2)
    ch = MarkovChain(prop, constraints=[contiguous, within_percent_of_ideal_population(part, eps)],
                     accept=always_accept, initial_state=part, total_steps=steps)
    rows = []
    for i, p in enumerate(ch):
        if i < BURN:
            continue
        rows.append(measures(S, p.assignment))
        if (i + 1) % 5000 == 0:
            print(f"[south {chain}] {i + 1}/{steps}", flush=True)
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(rows, columns=COLS).to_csv(OUT / f"chain{chain}.csv", index=False)
    (OUT / f"chain{chain}.json").write_text(json.dumps({"seed_salt": f"regional_south_{chain}", "seed": seed, "steps": steps,
                                                         "epsilon": eps, "start_max_dev": start_dev, "ideal_pop_2021": ideal,
                                                         "n_vas": len(S["nodes"]), "districts": len(part), "start": "random plan within the band (recursive_tree_part)", "burn_in_discarded": BURN}, indent=1))
    print(f"[south {chain}] done eps={eps} start_dev={start_dev:.3f}", flush=True)


def summarize():
    S = setup()
    real = {"panel": dict(zip(COLS, measures(S, {n: S["panel"][n] for n in S["nodes"]}))),
            "para167": dict(zip(COLS, measures(S, {n: S["para"][n] for n in S["nodes"]})))}
    df = pd.concat([pd.read_csv(f) for f in sorted(OUT.glob("chain*.csv"))])
    out = {"plan": "preregistration/six_signals_2026-11-07.md", "n_plans": len(df),
           "chains": [json.loads(f.read_text()) for f in sorted(OUT.glob("chain*.json"))], "measures": {}}
    for c in COLS:
        v = df[c].to_numpy(float)
        row = {"q05": float(np.quantile(v, 0.05)), "q50": float(np.quantile(v, 0.5)), "q95": float(np.quantile(v, 0.95))}
        for k, r in real.items():
            x = float(r[c])
            row[k] = {"value": x, "pct": round(100 * float((v < x).mean() + 0.5 * (v == x).mean()), 2)}
        out["measures"][c] = row
    for k in ("ed", "all"):
        far = out["measures"][f"leth_far_{k}"]
        out[f"unusual_{k}"] = {m: bool(far[m]["pct"] > 95 or far[m]["pct"] < 5) for m in real}
    (HERE / "regional_south.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    print(json.dumps(out, indent=0)[:3000])


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(int(sys.argv[2]), int(sys.argv[3]))
    else:
        summarize()
