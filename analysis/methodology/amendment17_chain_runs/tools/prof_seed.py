"""Replay an nk seed (recursive_tree_part) exactly and profile where/why it fails.

The counting wrapper calls the same balance-edge function with the same args, so
the RNG stream (and so the failure) is reproduced exactly.
"""
import json, random, sys, time
from functools import partial
from pathlib import Path

import networkx as nx
import numpy as np

REPO = Path(sys.argv[1]); K = int(sys.argv[2]); IDX = int(sys.argv[3])
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
import close_seats_ensemble as cse  # noqa: E402
from gerrychain.tree import bipartition_tree, recursive_tree_part, find_balanced_edge_cuts_memoization, random_spanning_tree

me = cse.me
va, graph = me.build_va_graph(verbose=False)
s = cse.chain_seed(IDX)
total = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
ideal = total / K

calls = []          # one entry per bipartition_tree call
cur = {"tries": 0}


def counting_balance(h, one_sided_cut=False, choice=random.choice):
    cur["tries"] += 1
    return find_balanced_edge_cuts_memoization(h, one_sided_cut=one_sided_cut, choice=choice)


def method(g, **kw):
    cur["tries"] = 0
    cur["graph"] = g
    cur["kw"] = kw
    t = time.time()
    try:
        out = bipartition_tree(g, max_attempts=50000, balance_edge_fn=counting_balance, **kw)
        calls.append({"n_nodes": g.number_of_nodes(), "tries": cur["tries"], "secs": round(time.time() - t, 3)})
        return out
    except Exception:
        calls.append({"n_nodes": g.number_of_nodes(), "tries": cur["tries"], "secs": round(time.time() - t, 3), "FAILED": True})
        raise


np.random.seed(s + 999); random.seed(s + 999)
t0 = time.time()
failed = None
try:
    recursive_tree_part(graph, parts=list(range(K)), pop_target=ideal, pop_col="pop_2021",
                        epsilon=0.25, node_repeats=5, method=method)
except RuntimeError as e:
    failed = str(e)
print(f"seed idx={IDX} k={K}: {'FAILED: ' + failed if failed else 'ok'} in {time.time()-t0:.0f}s, {len(calls)} bipartition calls")
tries = np.array([c["tries"] for c in calls]); secs = np.array([c["secs"] for c in calls])
print(f"tries per call: median {np.median(tries):.0f}, p90 {np.percentile(tries,90):.0f}, max {tries.max()} (call #{tries.argmax()+1})")
print(f"time: {secs.sum():.0f}s total; slowest calls:", sorted(calls, key=lambda c: -c['secs'])[:5])

if failed:
    g = cur["graph"]; kw = cur["kw"]
    T, eps = kw["pop_target"], kw["epsilon"]
    pops = {n: g.nodes[n]["pop_2021"] for n in g.nodes}
    tot = sum(pops.values())
    print(f"\nFAILING SUBPROBLEM (final 2-way split): {g.number_of_nodes()} VAs, {g.number_of_edges()} edges")
    print(f"  merged pop {tot:,.0f} = {tot/T:.4f} x target {T:,.0f}; needs each side in [{T*(1-eps):,.0f}, {T*(1+eps):,.0f}]")
    print(f"  total within 2T(1±eps)? {abs(tot-2*T) <= 2*T*eps}")
    big = sorted(pops.items(), key=lambda kv: -kv[1])[:5]
    print("  biggest VAs:", [(n, round(p), va.loc[n].get('va_name', '') if hasattr(va.loc[n], 'get') else '') for n, p in big])
    print(f"  connected: {nx.is_connected(g)}; articulation points: {len(list(nx.articulation_points(g)))}")
    # best achievable split over every edge of many random spanning trees
    best = []
    random.seed(12345)
    for _ in range(3000):
        tree = random_spanning_tree(g)
        root = next(iter(tree.nodes))
        order = list(nx.dfs_postorder_nodes(tree, root))
        parent = dict(nx.bfs_predecessors(tree, root))
        sub = dict(pops)
        for n in order:
            if n in parent:
                sub[parent[n]] += sub[n]
        worst = min(max(abs(sub[n] - T), abs(tot - sub[n] - T)) / T for n in parent)
        best.append(worst)
    best = np.array(best)
    print(f"  over 3000 random trees, best cut's worse side is {best.min():.2%} off target (need <= {eps:.0%}); median tree best {np.median(best):.2%}")
    # cut-vertex check: does removing any single articulation point leave a component too big for one side?
    worst_ap = []
    for ap in nx.articulation_points(g):
        h = g.copy(); h.remove_node(ap)
        comps = sorted((sum(pops[n] for n in c) for c in nx.connected_components(h)), reverse=True)
        worst_ap.append((comps[0] / T, ap, len(comps)))
    worst_ap.sort(reverse=True)
    print("  largest component after removing one articulation point (x target):", [(round(a, 3), ap, nc) for a, ap, nc in worst_ap[:5]])
    json.dump({"nodes": sorted(int(n) for n in g.nodes)}, open(Path(sys.argv[4]), "w"))
