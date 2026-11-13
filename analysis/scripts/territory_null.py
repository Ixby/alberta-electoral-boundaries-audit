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

Territory (territory()). VAs are assigned to districts by representative point
(the audit's convention). Before an enacted map exists, the fixed set is Step A's
56; nodes outside it form two components on the VA graph:
  - Calgary-Acadia alone (the panel changed it by 2 people), which can only
    ever hold one district, so it is fixed too;
  - everything else (34 districts in the panel's map).
With an enacted map (--enacted, Amendment 8, Part 5), a majority district is
fixed when an enacted district holds exactly its VAs, and the territory's
district count and s.15(2) cap come from the enacted map. On the Step A fixed
set the generalised code reproduces the first plans of chain 1 byte for byte.

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
K_PROV = 91


def seed_for(idx):
    h = hashlib.sha256((RANDOMNESS + f"a8-territory-null-chain{idx}").encode()).digest()
    return int.from_bytes(h[:4], "big")


def _rep_labels(va, nodes, gpkg, col):
    import geopandas as gpd

    norm = lambda s: s.replace("’", "'").strip()  # noqa: E731
    pts = va.loc[nodes, ["geometry"]].copy()
    pts["geometry"] = pts.geometry.representative_point()
    g = gpd.read_file(gpkg).to_crs(va.crs)
    j = gpd.sjoin(pts, g[[col, "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    lab = {n: norm(v) for n, v in zip(nodes, j[col])}
    assert all(isinstance(v, str) for v in lab.values()), f"a VA falls outside every district of {gpkg}"
    return lab


def territory(va, graph, enacted=None, enacted_col="EDName2025", stated_low=None):
    """Split the province into fixed districts and the redrawn territory.

    A commission-majority district is fixed when the map being scored keeps it
    unchanged: with an enacted map (enacted=gpkg), when some enacted district
    holds exactly the same voting areas (by representative point); before one
    exists, when it is one of Amendment 7 Step A's 56 (unchanged_56.json).
    The rest of the graph splits into connected components. A component the
    scored map fills with one district is fixed too. The chain redraws the
    component(s) holding more than one: with an enacted map, as many districts
    as the enacted map puts there; before one exists, all 35 changed districts
    in the one remaining component.

    stated_low: how many fixed districts the scored map's own population table
    puts more than 25% below its average (s.15(2) districts already used).
    Before an enacted map: 2 (App. 7: Central Peace-Notley, Lesser Slave Lake).

    Returns (fixed label per non-territory node, sorted territory nodes,
    districts in the territory, s.15(2) cap in the territory).
    """
    import networkx as nx

    nodes = sorted(graph.nodes())
    maj = _rep_labels(va, nodes, MAJ, "EDName2025")
    sets = {}
    for n in nodes:
        sets.setdefault(maj[n], set()).add(n)
    if enacted is None:
        keep = {n.replace("’", "'").strip() for n in json.loads(UNCHANGED.read_text(encoding="utf-8"))["districts"]}
        assert len(keep) == 56
        fixed = {d for d in sets if d in keep}
        n_changed, enl = K_PROV - len(fixed), None
        stated_low = 2 if stated_low is None else stated_low
    else:
        enl = _rep_labels(va, nodes, enacted, enacted_col)
        esets = {}
        for n in nodes:
            esets.setdefault(enl[n], set()).add(n)
        same = {frozenset(v) for v in esets.values()}
        fixed = {d for d, v in sets.items() if frozenset(v) in same}
        assert stated_low is not None, "give the enacted map's count of districts below -25%"
    lab = {n: maj[n] for n in nodes if maj[n] in fixed}
    rest = [n for n in nodes if maj[n] not in fixed]
    comps = sorted((sorted(c) for c in nx.connected_components(graph.subgraph(rest))), key=len, reverse=True)
    multi = []
    for c in comps:
        cs = set(c)
        if enl is not None:
            k = len({enl[n] for n in c})
            assert all(esets[enl[n]] <= cs for n in c), "an enacted district straddles a fixed district"
        else:
            k = 1 if any(cs == v for v in sets.values()) else None
        if k == 1:
            for n in c:
                lab[n] = (enl or maj)[n]
        else:
            multi.append((c, k))
    assert len(multi) == 1, f"{len(multi)} multi-district components; this code redraws exactly one"
    c, k = multi[0]
    if k is None:
        k = n_changed - (len(comps) - 1)
    return lab, c, k, 4 - stated_low


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--idx", type=int, required=True)
    ap.add_argument("--steps", type=int, default=100_000)
    ap.add_argument("--thin", type=int, default=250)
    ap.add_argument("--out", required=True)
    ap.add_argument("--enacted", default=None, help="enacted map gpkg (rerun under Amendment 8, Part 5)")
    ap.add_argument("--enacted-col", default="EDName2025")
    ap.add_argument("--stated-low", type=int, default=None,
                    help="with --enacted: fixed districts its own table puts > 25%% below average")
    a = ap.parse_args()
    cse._no_power_throttling()
    assert hashlib.sha256(CRITERIA.read_bytes()).hexdigest() == CRITERIA_SHA, "criteria table changed"
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    va, graph = me.build_va_graph(verbose=False)
    _, terr, K_TERR, cap = territory(va, graph, a.enacted, a.enacted_col, a.stated_low)
    (out / "territory_nodes.json").write_text(json.dumps([int(n) for n in terr]))
    prov_ideal = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes()) / K_PROV

    # s.15(2) inputs over the whole province (town totals), then the cap.
    cse.S152_PATH = CRITERIA
    cse.OPTS.update(s152=CRITERIA_SHA, proposal_epsilon=0.5)
    cse.S152 = cse.load_s152(graph, CRITERIA, K_PROV)
    assert abs(cse.S152["ideal"] - prov_ideal) < 1e-6
    cse.S152_MAX = cap

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
    # The seed is cut around the territory's own average (its population is not K_TERR provincial
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
