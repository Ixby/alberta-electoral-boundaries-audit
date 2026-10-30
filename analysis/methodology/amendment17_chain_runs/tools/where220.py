import json, sys
sys.path[:0] = ["analysis/scripts", "analysis/utils"]
import mcmc_ensemble as me
import networkx as nx
va, g = me.build_va_graph(verbose=False)
nodes = json.load(open(sys.argv[1]))["nodes"]
sub = va.loc[nodes]
print(sub["parent_ed_2019"].value_counts().to_string())
h = g.subgraph(nodes)
pops = {n: g.nodes[n]["pop_2021"] for n in nodes}
area = sub.geometry.area.sum() / 1e6
print(f"area {area:,.0f} km2, pop {sum(pops.values()):,.0f}")
# population-weighted spread: how much pop sits in the densest few VAs' neighbourhood
import numpy as np
p = np.array(sorted(pops.values(), reverse=True)); print("top-10 VAs hold", round(p[:10].sum() / p.sum() * 100, 1), "% of pop")
# diameter and two-lobe check
print("graph diameter", nx.diameter(h))
# best single-edge 'bridge-ish' cut: min edge cut between halves via Fiedler ordering
L = nx.laplacian_matrix(h, nodelist=nodes).toarray().astype(float)
w, v = np.linalg.eigh(L); f = v[:, 1]
order = [nodes[i] for i in np.argsort(f)]
cum = np.cumsum([pops[n] for n in order]); T = 46841.0
best = min(range(len(order) - 1), key=lambda i: max(abs(cum[i] - T), abs(cum[-1] - cum[i] - T)))
left = set(order[: best + 1])
print("Fiedler sweep best split: sides", round(cum[best] / T, 3), round((cum[-1] - cum[best]) / T, 3), "x target; left connected", nx.is_connected(h.subgraph(left)), "right connected", nx.is_connected(h.subgraph(set(nodes) - left)))
