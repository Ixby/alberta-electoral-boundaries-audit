# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
territory_null.py
-----------------

Amendment 8 (draft): a neutral-redraw null for the territory the Independent
Advisory Panel changed.

The panel kept 56 of the commission majority's districts exactly (Amendment 7,
Step A, findings/iap_unchanged_districts.md) and redrew the rest. This script
holds those 56 at their official geometry and draws neutral plans of the rest
of Alberta with the set D sampler (close_seats_ensemble.py: ReCom, EBCA
s.15(1) +/-25%, s.15(2) mode on the Amendment 23 criteria table), so the
panel's choices in that territory can be ranked against neutral choices made
under the same fixed districts and the same statute.

Territory. VAs are assigned to majority districts by representative point (the
audit's convention). Nodes outside the 56 form two components on the VA graph:
  - Calgary-Acadia alone (one district; the panel changed it by 2 people), which
    can only ever hold one district, so it is fixed too;
  - everything else (K_TERR = 34 districts in the panel's map).
The chain runs on that main component only.

Statute, as strict as the statute:
  - the s.15(1) band is +/-25% of the PROVINCIAL average (2021 VA overlay total
    / 91), not the territory's own average;
  - s.15(2): at most 4 divisions province-wide. Two unchanged districts already
    use it (Central Peace-Notley, Lesser Slave Lake), so at most 2 in the
    territory; criteria as in set D (Amendment 21/23), counted over the whole
    province (town totals use the full graph).

Output per chain (--out DIR): chain<idx>_plans.npy (int8, plans x territory
nodes, district index per node, node order = territory_nodes.json) and
chain<idx>_plans.json (steps, s.15(2) counts). Scoring is territory_score.py.

Seeds: drand round 6606642 (pinned 2026-11-02, seed_commitments.md), salt
"a8-territory-null-chain<idx>"; seeding RNG +999 as in close_seats_ensemble.

No November map data is read. Exploratory until Amendment 8 is filed.
"""
import argparse
import hashlib
import json
import random

import sys
import time
from functools import partial
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import close_seats_ensemble as cse  # noqa: E402  (installs the set D hooks)
import mcmc_ensemble as me  # noqa: E402

MAJ = REPO / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"
UNCHANGED = REPO / "analysis/a8/unchanged_56.json"
CRITERIA = REPO / "data/outputs/s15_2_va_criteria.csv"
CRITERIA_SHA = "48c928b8716f6ed218065e01a912ecabd11518917ac9e312376e4d603ee2fafc"
RANDOMNESS = "8093cc614f39474aeb08e80a8a63eb04053d5fd3c5942524ea0ce54a4541d70f"  # round 6606642
K_PROV, K_TERR, S152_USED_OUTSIDE = 91, 34, 2


def seed_for(idx):
    h = hashlib.sha256((RANDOMNESS + f"a8-territory-null-chain{idx}").encode()).digest()
    return int.from_bytes(h[:4], "big")


def territory(va, graph):
    """(fixed labels per node, sorted main-component node list)."""
    import geopandas as gpd
    import networkx as nx

    norm = lambda s: s.replace("’", "'").strip()  # noqa: E731
    keep = {norm(n) for n in json.loads(UNCHANGED.read_text(encoding="utf-8"))["districts"]}
    assert len(keep) == 56
    nodes = sorted(graph.nodes())
    pts = va.loc[nodes, ["geometry"]].copy()
    pts["geometry"] = pts.geometry.representative_point()
    maj = gpd.read_file(MAJ).to_crs(va.crs)
    j = gpd.sjoin(pts, maj[["EDName2025", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    lab = {n: norm(s) for n, s in zip(nodes, j["EDName2025"])}
    assert all(isinstance(v, str) for v in lab.values()), "a VA falls outside every majority district"
    rest = [n for n in nodes if lab[n] not in keep]
    comps = sorted(nx.connected_components(graph.subgraph(rest)), key=len, reverse=True)
    assert len(comps) == 2 and {lab[n] for n in comps[1]} == {"Calgary-Acadia"}, [len(c) for c in comps]
    return lab, sorted(comps[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--idx", type=int, required=True)
    ap.add_argument("--steps", type=int, default=100_000)
    ap.add_argument("--thin", type=int, default=250)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cse._no_power_throttling()
    assert hashlib.sha256(CRITERIA.read_bytes()).hexdigest() == CRITERIA_SHA, "criteria table changed"
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    va, graph = me.build_va_graph(verbose=False)
    _, terr = territory(va, graph)
    (out / "territory_nodes.json").write_text(json.dumps([int(n) for n in terr]))
    prov_ideal = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes()) / K_PROV

    # s.15(2) inputs over the whole province (town totals), then the cap.
    cse.S152_PATH = CRITERIA
    cse.OPTS.update(s152=CRITERIA_SHA, proposal_epsilon=0.5)
    cse.S152 = cse.load_s152(graph, CRITERIA, K_PROV)
    assert abs(cse.S152["ideal"] - prov_ideal) < 1e-6
    cse.S152_MAX = 4 - S152_USED_OUTSIDE

    # run_ensemble indexes per-node arrays by node id, so the territory graph is relabelled
    # 0..n-1 in sorted original order (territory_nodes.json maps back).
    import networkx as nx

    H0 = graph.subgraph(terr).copy()
    geo = cse.Geo(va, H0)
    H = nx.relabel_nodes(H0, {n: i for i, n in enumerate(terr)}, copy=True)
    geo.nodes = list(range(len(terr)))
    cse.GEO = geo
    cse.S152["attrs"] = {i: cse.S152["attrs"][n] for i, n in enumerate(terr)}
    # Every split is judged against the provincial average, not the territory's.
    me._bpt_global = lambda g, pop_col, pop_target, epsilon, *x, **kw: cse.bipartition_tree_fastfail(
        g, pop_col, prov_ideal, epsilon, *x, **kw)

    s = seed_for(a.idx)
    np.random.seed(s)
    random.seed(s)
    from gerrychain.tree import bipartition_tree, recursive_tree_part

    st_np, st_py = np.random.get_state(), random.getstate()
    np.random.seed((s + 999) % 2**32)
    random.seed(s + 999)
    # The seed is cut around the territory's own average (its population is not 34 provincial
    # averages), with a band narrow enough that every seed district is within +/-25% of the
    # provincial average. The chain itself judges every split against the provincial average.
    terr_ideal = sum(H.nodes[n]["pop_2021"] for n in H.nodes()) / K_TERR
    eps = 0.25 - abs(terr_ideal / prov_ideal - 1) - 0.01
    state = recursive_tree_part(H, parts=list(range(K_TERR)), pop_target=terr_ideal, pop_col="pop_2021",
                                epsilon=eps, node_repeats=5, method=partial(bipartition_tree, max_attempts=50000))
    np.random.set_state(st_np)
    random.setstate(st_py)
    print(f"[a8 {a.idx}] seed {s} ready: {len(set(state.values()))} districts on {len(terr)} VAs", flush=True)

    part = cse._partition(H, state)
    plans, meta = [], {"idx": a.idx, "seed": s, "steps": a.steps, "thin": a.thin, "criteria_sha": CRITERIA_SHA,
                       "prov_ideal": prov_ideal, "s152_max_in_territory": cse.S152_MAX, "plan_step": [],
                       "s152_districts": []}
    t0 = time.time()
    done = 0
    while done < a.steps:
        cse.EXTRA.clear()
        rows, part = me.run_ensemble(H, part, a.thin, pop_deviation=0.5, verbose=False,
                                     return_final_partition=True, seed=s, proposal_epsilon=0.5)
        done += a.thin
        assign = {int(n): int(d) for n, d in part.assignment.items()}
        lut = {d: i for i, d in enumerate(sorted(set(assign.values())))}
        plans.append(np.array([lut[assign[i]] for i in range(len(terr))], dtype=np.int8))
        pops = part["population"].values()
        meta["plan_step"].append(done)
        meta["s152_districts"].append(int(sum((p - prov_ideal) / prov_ideal < -0.25 for p in pops)))
        assert len(lut) == K_TERR and all((p - prov_ideal) / prov_ideal <= 0.25 for p in pops)
        if len(plans) % 20 == 0 or done >= a.steps:
            np.save(out / f"chain{a.idx}_plans.npy", np.stack(plans))
            (out / f"chain{a.idx}_plans.json").write_text(json.dumps(meta))
            print(f"[a8 {a.idx}] {done}/{a.steps} {time.time() - t0:.0f}s", flush=True)
        part = cse._partition(H, assign)


if __name__ == "__main__":
    main()
