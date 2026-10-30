"""Municipality-aware calibration.
  real            -> municipal split ratio for the 2019, majority and minority maps
  tune W IDX N K  -> run an nk chain (proposal eps 0.25, muni surcharge W) for N steps,
                     print mean ratio over the second half
"""
import json, random, sys, time
from functools import partial
from pathlib import Path

import numpy as np

REPO = Path(sys.argv[1])
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
import close_seats_ensemble as cse  # noqa: E402
import geopandas as gpd  # noqa: E402

me = cse.me
va, graph = me.build_va_graph(verbose=False)
cse.GEO = geo = cse.Geo(va, graph)
print(f"CSDs in ratio: {len(geo.csd_groups)}", flush=True)

if sys.argv[2] == "real":
    out = {"2019_enacted": geo.csd_split_ratio(va.loc[geo.nodes, "parent_ed_2019"].to_numpy())}
    pts = va.loc[geo.nodes].copy(); pts["geometry"] = pts.geometry.representative_point()
    for name in ("majority", "minority"):
        f = REPO / f"data/shapefiles/canonical/ea_{name}_2026_eds.gpkg"
        eds = gpd.read_file(f).to_crs(pts.crs)
        j = gpd.sjoin(pts[["geometry"]], eds[["EDName2025", "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
        out[f"{name}_2026"] = geo.csd_split_ratio(j["EDName2025"].fillna("__unassigned__").to_numpy())
    out["mean_of_three"] = float(np.mean(list(out.values())))
    print(json.dumps(out, indent=1))
    sys.exit()

W, IDX, N, K = float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
cse.OPTS.update(proposal_epsilon=0.25, muni_surcharge=W)
s = cse.chain_seed(IDX)
np.random.seed(s); random.seed(s)
from gerrychain.tree import bipartition_tree, recursive_tree_part  # noqa: E402
total = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
st = np.random.get_state(), random.getstate()
np.random.seed(s + 999); random.seed(s + 999)
state = recursive_tree_part(graph, parts=list(range(K)), pop_target=total / K, pop_col="pop_2021",
                            epsilon=0.25, node_repeats=5, method=partial(bipartition_tree, max_attempts=50000))
np.random.set_state(st[0]); random.setstate(st[1])
me._bpt_global = cse.bipartition_tree_fastfail
cse.set_muni(graph, W)
part = cse._partition(graph, state)
ratios = []
_orig_stats = cse.Geo.stats
t0 = time.time()
done = 0
while done < N:
    rows, p = me.run_ensemble(graph, part, 500, pop_deviation=0.25, verbose=False, return_final_partition=True,
                              seed=s, proposal_epsilon=0.25)
    ratios.append(geo.csd_split_ratio([p.assignment[n] for n in geo.nodes]))
    part = cse._partition(graph, {int(n): int(d) for n, d in p.assignment.items()})
    done += 500
half = ratios[len(ratios) // 2:]
print(json.dumps({"W": W, "idx": IDX, "k": K, "steps": N, "secs": round(time.time() - t0),
                  "ratio_by_500": [round(r, 4) for r in ratios],
                  "mean_second_half": round(float(np.mean(half)), 4)}))
