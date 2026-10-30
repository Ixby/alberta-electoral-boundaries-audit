# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
close_seats_ensemble.py
-----------------------

Size-matched neutral ensembles and the Amendment 17 measures (2026-10-29).

Reuses analysis/scripts/mcmc_ensemble.py unchanged. Two read-only hooks add
per-plan measures without touching any random draw, so each chain is the
canonical harness's chain:
  - seat_results is wrapped to count close seats (two-party gap within 2, 4
    and 6 points on the 2023 election-day votes);
  - MarkovChain.__next__ is wrapped to record, for each plan, the cities and
    towns split into more pieces than their population requires and the
    Calgary/Edmonton-versus-rest population gap.
A third hook (2026-10-29, nk mode only) wraps the bipartition method so a district pair whose
merged population cannot be split within the band is reselected at once
instead of after 100,000 failed spanning trees. In nk mode each chunk restarts
from a Partition rebuilt from its assignment and a checkpoint is written after
every chunk, so --resume continues a killed chain with the rows an unbroken run
would have written. Both change the sample path for a given idx (not the
distribution), so nk output from this version is not row-identical to earlier
versions.

Measures (Amendment 17 items 3-5; the same function scores real maps):
  town split   cities and towns (Statistics Canada 2021 CSD types CY and T)
               of 20,000-150,000 people; pieces = districts holding >= 2% of
               the town's population; flagged when pieces > ceil(pop /
               (1.25 x average district population)).
  city gap     a district is a Calgary or Edmonton district when >= 50% of its
               population lives in that city; gap = (mean population of city
               districts - mean of the rest) / mean of the rest, in percent.
  close seats  districts whose UCP-NDP two-party gap is within 4 points.
Population is the VA-level 2021 census overlay the canonical harness uses;
VAs are assigned to towns and to real-map districts by representative point.

Modes
  rep87  replays canonical chain <idx> (87 districts, 2019 seed).
  nk     K-district chain (--k), seeded the way the canonical harness seeds
         its own fallback (recursive_tree_part at epsilon = pop_deviation);
         chain seeds (base_seed * 100000 + idx * 1000) mod 2**32 with
         base_seed = get_canonical_seed("mcmc_ensemble_250k").
  real   scores the 2019, majority and minority maps (and --extra maps).

Exploratory unless named in the amendment log.
"""
import argparse
import json
import math
import os
import random
import sys
import time
from functools import partial
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import mcmc_ensemble as me  # noqa: E402
from drand_seed import get_canonical_seed  # noqa: E402

CSD_GPKG = REPO / "data" / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
TOWN_MIN, TOWN_MAX = 20_000, 150_000

_orig_seat_results = me.seat_results


def seat_results_close(ucp, ndp):
    m = _orig_seat_results(ucp, ndp)
    ucp = np.asarray(ucp, float)
    ndp = np.asarray(ndp, float)
    tot = ucp + ndp
    ok = tot > 0
    gap = np.zeros_like(tot)
    gap[ok] = (ucp[ok] - ndp[ok]) / tot[ok]
    for t in (2, 4, 6):
        c = ok & (np.abs(gap) <= t / 100)
        m[f"close{t}"] = int(c.sum())
        m[f"close{t}_ucp"] = int((c & (ucp > ndp)).sum())
        m[f"close{t}_ndp"] = int((c & (ndp > ucp)).sum())
    m["n_parts"] = int(len(tot))
    return m


me.seat_results = seat_results_close


class Geo:
    """VA-level population, city and town membership, in graph-node order."""

    def __init__(self, va, graph):
        import geopandas as gpd

        self.nodes = sorted(graph.nodes())
        self.pop = np.array([graph.nodes[n]["pop_2021"] for n in self.nodes], float)
        pts = va.loc[self.nodes].copy()
        pts["geometry"] = pts.geometry.representative_point()
        csd = gpd.read_file(CSD_GPKG).to_crs(pts.crs)
        j = gpd.sjoin(pts[["geometry"]], csd[["CSDUID", "CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
        self.csduid = j["CSDUID"].to_numpy()
        name = j["CSDNAME"].fillna("").to_numpy()
        typ = j["CSDTYPE"].fillna("").to_numpy()
        self.is_cal = name == "Calgary"
        self.is_edm = name == "Edmonton"
        tpop = pd.Series(self.pop).groupby(name).sum()
        towns = sorted(
            n for n in tpop.index
            if n and n not in ("Calgary", "Edmonton")
            and set(typ[name == n]) & {"CY", "T"}
            and TOWN_MIN <= tpop[n] <= TOWN_MAX
        )
        self.towns = [(n, name == n, float(tpop[n])) for n in towns]
        # Municipal split ratio (municipality-aware calibration): every 2021 CSD
        # other than Calgary and Edmonton that spans >= 2 VAs (a one-VA CSD
        # cannot be split at VA resolution).
        uid = pd.Series(self.csduid).fillna("")
        self.csd_groups = []
        for u, idx in uid.groupby(uid).groups.items():
            ix = np.asarray(idx)
            tp = float(self.pop[ix].sum())
            if u and len(ix) >= 2 and tp > 0 and name[ix[0]] not in ("Calgary", "Edmonton"):
                self.csd_groups.append((ix, tp))

    def csd_split_ratio(self, labels):
        """Share of those CSDs split into more pieces than their population
        requires (same piece and need rules as the town-split measure)."""
        uniq, inv = np.unique(np.asarray(labels), return_inverse=True)
        k = len(uniq)
        avg = self.pop.sum() / k
        over = 0
        for ix, tp in self.csd_groups:
            by = np.bincount(inv[ix], weights=self.pop[ix], minlength=k)
            if int((by >= 0.02 * tp).sum()) > math.ceil(tp / (1.25 * avg)):
                over += 1
        return over / len(self.csd_groups)

    def stats(self, labels):
        """labels: district label per node (same order as self.nodes)."""
        uniq, inv = np.unique(np.asarray(labels), return_inverse=True)
        k = len(uniq)
        dpop = np.bincount(inv, weights=self.pop, minlength=k)
        avg = self.pop.sum() / k
        cal = np.bincount(inv, weights=self.pop * self.is_cal, minlength=k)
        edm = np.bincount(inv, weights=self.pop * self.is_edm, minlength=k)
        city = (cal >= 0.5 * dpop) | (edm >= 0.5 * dpop)
        gap = (dpop[city].mean() - dpop[~city].mean()) / dpop[~city].mean() * 100 if city.any() and (~city).any() else float("nan")
        flagged = []
        for n, mask, tp in self.towns:
            by = np.bincount(inv[mask], weights=self.pop[mask], minlength=k)
            pieces = int((by >= 0.02 * tp).sum())
            need = math.ceil(tp / (1.25 * avg))
            if pieces > need:
                flagged.append(f"{n}:{pieces}/{need}")
        return {
            "city_gap_pct": float(gap),
            "n_city_districts": int(city.sum()),
            "towns_flagged": len(flagged),
            "towns_flagged_list": ";".join(flagged),
        }


EXTRA = []
GEO = None
_OrigMC = me.MarkovChain


class RecordingChain(_OrigMC):
    def __init__(self, *args, **kwargs):
        if S152 is not None:  # s.15(2) mode replaces run_ensemble's population constraint
            kwargs["constraints"] = [s152_constraint]
        super().__init__(*args, **kwargs)

    def __next__(self):
        part = super().__next__()
        row = GEO.stats([part.assignment[n] for n in GEO.nodes])
        if S152 is not None:
            ideal = S152["ideal"]
            row["s152_districts"] = sum((p - ideal) / ideal < -S152_BAND for p in part["population"].values())
        EXTRA.append(row)
        return part


me.MarkovChain = RecordingChain

_orig_bpt = me._bpt_global
from gerrychain.tree import ReselectException  # noqa: E402

INFEASIBLE_PAIRS = 0
MUNI = None  # {"csduid": weight} for municipality-aware chains (--muni-surcharge), else None
# Chain-kernel options (nk mode); recorded in every checkpoint and checked on resume.
#   proposal_epsilon  None = canonical half-band (+/-12.5%); 0.25 = the s.15(1) band
#   muni_surcharge    0 = population-only; > 0 = municipality-aware (see set_muni)
#   s152              None = off; else SHA-256 of the per-VA criteria table (--s152 PATH);
#                     proposal_epsilon is then 0.5 so gerrychain's post-check admits a -50% side
#                     (the real s.15(1)/s.15(2) bands are enforced by find_balanced_edge_cuts_s152)
OPTS_DEFAULT = {"proposal_epsilon": None, "muni_surcharge": 0.0, "s152": None}
S152_PATH = None
OPTS = dict(OPTS_DEFAULT)


def set_muni(graph, weight):
    """Municipality-aware ReCom: tag every VA with its 2021 CSD (city, town,
    village, county/MD, reserve...; Metis settlements are not CSDs in this
    layer) and pass region_surcharge to
    bipartition_tree, so spanning trees cross CSD boundaries last and cuts
    prefer CSD boundaries. A VA in no CSD gets None, which gerrychain treats as
    crossing. weight 0 = off (the population-only baseline)."""
    global MUNI
    if not weight:
        MUNI = None
        return
    for n, uid in zip(GEO.nodes, GEO.csduid):
        graph.nodes[n]["csduid"] = None if pd.isna(uid) else str(uid)
    MUNI = {"csduid": float(weight)}


def bipartition_tree_fastfail(graph, pop_col, pop_target, epsilon, *args, **kwargs):
    """A pair whose merged population is outside 2 x pop_target x (1 +/- epsilon)
    has no balanced split: the original would spend all max_attempts (100,000
    spanning trees) and then raise ReselectException. Raise it at once. The
    1e-9 slack keeps a pair that could be split (populations are non-integer)
    from ever being rejected here. Same transition distribution; fewer random
    draws, so a different sample path from the unpatched script for one idx."""
    global INFEASIBLE_PAIRS
    if S152 is not None:
        if s152_pair_infeasible(graph, pop_col, pop_target):
            INFEASIBLE_PAIRS += 1
            raise ReselectException("no s.15(1)/s.15(2)-valid split of this pair is possible")
        kwargs["balance_edge_fn"] = find_balanced_edge_cuts_s152
        return _orig_bpt(graph, pop_col, pop_target, epsilon, *args, **kwargs)
    total = sum(graph.nodes[n][pop_col] for n in graph.nodes)
    if abs(total - 2 * pop_target) > 2 * pop_target * epsilon * (1 + 1e-9):
        INFEASIBLE_PAIRS += 1
        raise ReselectException("merged pair population outside the balanced band")
    if MUNI is not None:
        # This wrapper's signature has no region_surcharge, so recom never
        # overrides it; inject it here.
        kwargs["region_surcharge"] = MUNI
    return _orig_bpt(graph, pop_col, pop_target, epsilon, *args, **kwargs)

# ---- EBCA s.15(2) mode (--s152 <criteria csv>) ------------------------------
# governance/GOVERNANCE-s15-2-chain-model.md. A division may be 25-50% BELOW the
# average, for at most 4 divisions, when it meets >= 3 of the s.15(2) criteria
# (a)-(e), computed as sums/counts over its VAs from a per-VA criteria table
# (s152_criteria.py or the registered equivalent). Criteria met => permitted,
# never required. Everything else stays within +/-25% (s.15(1)).
S152 = None  # {"attrs": {node: (area_km2, near, big_town, reserve, border)}, "ideal": float}
S152_LOW, S152_BAND, S152_MAX = 0.50, 0.25, 4


def load_s152(graph, path, k):
    """Per-VA s.15(2) inputs as (area_km2, near, border, towns, reserves) plus
    district-level thresholds. Two table formats:
      registered (Amendment 21, s15_2_criteria.py): columns road_km, town,
        reserves (JSON {name: overlap km2}), border_km. A town counts when the
        division holds >= 2% of its population; a reserve or Metis settlement
        when the division holds >= 10% of its area; the border when the
        division's VAs share >= 1 km with the provincial boundary.
      cross-check (s152_criteria.py): columns big_town, town_name,
        reserve_or_metis, border (any VA counts)."""
    df = pd.read_csv(path, index_col="node", keep_default_na=False)
    pops = {n: graph.nodes[n]["pop_2021"] for n in graph.nodes()}
    attrs = {}
    if "reserves" in df.columns:
        town_tot = {}
        for n in graph.nodes():
            t = df.at[int(n), "town"]
            if t:
                town_tot[t] = town_tot.get(t, 0.0) + pops[n]
        for n in graph.nodes():
            r = df.loc[int(n)]
            t = r["town"]
            res = json.loads(r["reserves"]) if r["reserves"] else {}
            attrs[n] = (float(r["area_km2"]), int(float(r["road_km"]) <= 150), float(r["border_km"]),
                        ((t, pops[n]),) if t else (), tuple(res.items()))
        rules = {"town_tot": town_tot, "town_share": 0.02, "res_tot": _reserve_areas(),
                 "res_share": 0.10, "border_min": 1.0}
    else:
        town_tot = {}
        for n in graph.nodes():
            if bool(df.at[int(n), "big_town"]):
                t = df.at[int(n), "town_name"]
                town_tot[t] = town_tot.get(t, 0.0) + pops[n]
        for n in graph.nodes():
            r = df.loc[int(n)]
            big = bool(r["big_town"])
            attrs[n] = (float(r["area_km2"]), int(float(r["road_km"]) <= 150), 1.0 if bool(r["border"]) else 0.0,
                        ((r["town_name"], pops[n]),) if big else (),
                        (("any", 1.0),) if bool(r["reserve_or_metis"]) else ())
        rules = {"town_tot": town_tot, "town_share": 1e-12, "res_tot": {"any": 1.0},
                 "res_share": 1e-12, "border_min": 1.0}
    return {"attrs": attrs, "ideal": sum(pops.values()) / k, **rules}


def _reserve_areas():
    """Total area (km2) of each reserve and Metis settlement, computed exactly as
    s15_2_criteria.reserves() does (NRCan IR polygons + GoA Metis, dissolved by name, EPSG:3400)."""
    import geopandas as gpd

    root = REPO / "data/shapefiles/reference"
    r = gpd.read_file(root / "aboriginal_lands_nrcan_dl/aboriginal_lands_alberta.geojson").to_crs("EPSG:3400")
    r = r[r["distributionType"] == "IR"][["adminAreaNameEng", "geometry"]].rename(columns={"adminAreaNameEng": "name"})
    m = gpd.read_file(root / "metis_settlements_dl/metis_settlements_goa.geojson").to_crs("EPSG:3400")
    m = m[["METIS_NAME", "geometry"]].rename(columns={"METIS_NAME": "name"})
    m["name"] = m["name"] + " (Metis settlement)"
    r = pd.concat([r, m], ignore_index=True).dissolve(by="name").reset_index()
    return (r.set_index("name").geometry.area / 1e6).to_dict()


def set_s152(graph, k):
    global S152
    S152 = load_s152(graph, S152_PATH, k) if OPTS["s152"] else None


def _new_agg():
    return [0.0, 0, 0.0, {}, {}]


def _add(agg, rec):
    agg[0] += rec[0]; agg[1] += rec[1]; agg[2] += rec[2]
    for key, v in rec[3]:
        agg[3][key] = agg[3].get(key, 0.0) + v
    for key, v in rec[4]:
        agg[4][key] = agg[4].get(key, 0.0) + v


def _merge(agg, other):
    agg[0] += other[0]; agg[1] += other[1]; agg[2] += other[2]
    for i in (3, 4):
        d = agg[i]
        for key, v in other[i].items():
            d[key] = d.get(key, 0.0) + v


def _minus(tot, sub):
    return [tot[0] - sub[0], tot[1] - sub[1], tot[2] - sub[2],
            {key: v - sub[3].get(key, 0.0) for key, v in tot[3].items()},
            {key: v - sub[4].get(key, 0.0) for key, v in tot[4].items()}]


def s152_met(agg):
    """Number of s.15(2) criteria (a)-(e) a division with these aggregates meets."""
    s = S152
    big_town = any(v >= s["town_share"] * s["town_tot"][t] for t, v in agg[3].items() if v > 0)
    reserve = any(v >= s["res_share"] * s["res_tot"][r] for r, v in agg[4].items() if v > 0)
    return (agg[0] > 20_000) + (agg[1] == 0) + (not big_town) + reserve + (agg[2] >= s["border_min"])


def _side_ok(pop, ideal, agg):
    dev = (pop - ideal) / ideal
    if abs(dev) <= S152_BAND:
        return True
    return -S152_LOW <= dev < -S152_BAND and s152_met(agg) >= 3


def find_balanced_edge_cuts_s152(h, one_sided_cut=False, choice=random.choice):
    """gerrychain's find_balanced_edge_cuts_memoization (same root draw, same
    traversal, same per-cut random weight) with the s.15(2) side test in place
    of the symmetric epsilon band. Two-sided cuts only (as ReCom uses)."""
    from gerrychain.tree import Cut, _calc_pops, _part_nodes, predecessors, successors

    root = choice([x for x in h if h.degree(x) > 1])
    pred = predecessors(h.graph, root)
    succ = successors(h.graph, root)
    total_pop = h.tot_pop
    subtree_pops = _calc_pops(succ, root, h)
    attrs = S152["attrs"]
    agg = {}
    for node in reversed(nx_bfs_order(succ, root)):  # children before parents
        a = _new_agg()
        _add(a, attrs[node])
        for c in succ.get(node, ()):
            _merge(a, agg[c])
        agg[node] = a
    tot = agg[root]
    ideal = h.ideal_pop
    cuts = []
    for node, tree_pop in subtree_pops.items():
        sub = agg[node]
        if _side_ok(tree_pop, ideal, sub) and _side_ok(total_pop - tree_pop, ideal, _minus(tot, sub)):
            e = (node, pred[node])
            wt = random.random()
            cuts.append(Cut(edge=e, weight=h.graph.edges[e].get("random_weight", wt),
                            subset=frozenset(set(h.graph.nodes) - _part_nodes(node, succ))))
    return cuts


def nx_bfs_order(succ, root):
    out = [root]
    i = 0
    while i < len(out):
        out.extend(succ.get(out[i], ()))
        i += 1
    return out


def s152_pair_infeasible(graph, pop_col, pop_target):
    """Exact fast-fail for s.15(2) mode: no split can work when the merged total
    cannot be two valid sides, or when an s.15(2) side is needed (total below
    1.5 x target) but no part of the pair could meet 3 criteria (an upper bound:
    area of the whole pair, any VA beyond 150 km, any VA outside a counted town,
    any reserve the pair holds enough of, the pair's whole border length)."""
    nodes = list(graph.nodes)
    total = sum(graph.nodes[n][pop_col] for n in nodes)
    if total < 2 * pop_target * (1 - S152_LOW) * (1 - 1e-9) or total > 2 * pop_target * (1 + S152_BAND) * (1 + 1e-9):
        return True
    if total < 2 * pop_target * (1 - S152_BAND) * (1 - 1e-9):
        s, attrs = S152, S152["attrs"]
        a = _new_agg()
        for n in nodes:
            _add(a, attrs[n])
        best = ((a[0] > 20_000) + any(attrs[n][1] == 0 for n in nodes) + any(not attrs[n][3] for n in nodes)
                + any(v >= s["res_share"] * s["res_tot"][r] for r, v in a[4].items() if v > 0)
                + (a[2] >= s["border_min"]))
        if best < 3:
            return True
    return False


def s152_constraint(partition):
    """Every division within +/-25%, except at most 4 that are 25-50% below the
    average and meet >= 3 s.15(2) criteria."""
    ideal = S152["ideal"]
    attrs = S152["attrs"]
    special = 0
    for part, pop in partition["population"].items():
        dev = (pop - ideal) / ideal
        if abs(dev) <= S152_BAND:
            continue
        if not (-S152_LOW <= dev < -S152_BAND):
            return False
        a = _new_agg()
        for n in partition.parts[part]:
            _add(a, attrs[n])
        if s152_met(a) < 3:
            return False
        special += 1
    return special <= S152_MAX


BASE_SEED = get_canonical_seed("mcmc_ensemble_250k")


def chain_seed(idx):
    return (BASE_SEED * 100_000 + idx * 1_000) % (2**32)


def run(mode, idx, n_steps, chunk, out, va_file, k=89):
    global GEO
    va, graph = me.build_va_graph(verbose=False, va_path=Path(va_file) if va_file else None)
    GEO = Geo(va, graph)
    s = chain_seed(idx)
    np.random.seed(s)
    random.seed(s)
    if mode == "rep87":
        state = me.initial_assignment_2019(va)
    else:
        from gerrychain.tree import bipartition_tree, recursive_tree_part

        total = sum(graph.nodes[n]["pop_2021"] for n in graph.nodes())
        st_np, st_py = np.random.get_state(), random.getstate()
        np.random.seed(s + 999)
        random.seed(s + 999)
        state = recursive_tree_part(
            graph, parts=list(range(k)), pop_target=total / k, pop_col="pop_2021",
            epsilon=0.25, node_repeats=5, method=partial(bipartition_tree, max_attempts=50000),
        )
        np.random.set_state(st_np)
        random.setstate(st_py)
    print(f"[{mode} {idx}] seed ready ({len(set(state.values()))} parts; {len(GEO.towns)} towns tracked)", flush=True)
    if mode == "nk":
        state = _partition(graph, state)
        me._bpt_global = bipartition_tree_fastfail  # rep87 keeps the canonical replay exact
        set_muni(graph, OPTS["muni_surcharge"])
        set_s152(graph, k)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    _chunks(mode, idx, graph, state, 0, n_steps, chunk, out, s)


def _partition(graph, assignment):
    """nk chains restart every chunk from a Partition rebuilt from the assignment
    alone, so the chain state at a chunk boundary is exactly what the checkpoint
    holds: (assignment, numpy RNG state, Python RNG state). recom draws its edge
    with random.choice(tuple(partition["cut_edges"])), so a carried Partition's
    set order would otherwise make a resumed chain differ from an unbroken one.
    The updaters match run_ensemble's. (run_ensemble reseeds any initial state
    with a district beyond +/-25%; nk states never have one, since the seed is
    within 25% and every recom split is within the proposal epsilon <= 25%.)"""
    u = me.updaters
    return me.Partition(graph, {n: assignment[n] for n in sorted(graph.nodes())}, {
        "population": u.Tally("pop_2021", alias="population"),
        "ucp": u.Tally("va_ucp", alias="ucp"),
        "ndp": u.Tally("va_ndp", alias="ndp"),
        "area": u.Tally("va_area", alias="area"),
        "cut_edges": u.cut_edges,
    })


def _ckpt_path(out):
    return out.with_name(out.name + ".ckpt.json")


def _chunks(mode, idx, graph, state, done, n_steps, chunk, out, s):
    ckpt = _ckpt_path(out)
    t0 = time.time()
    while done < n_steps:
        n = min(chunk, n_steps - done)
        EXTRA.clear()
        # s.15(2) mode: pop_deviation 0.5 only keeps run_ensemble from reseeding a
        # state that holds a legal -25..-50% division; its own constraint is
        # replaced (RecordingChain) and the proposal epsilon is passed explicitly.
        rows, part = me.run_ensemble(graph, state, n, pop_deviation=0.5 if OPTS["s152"] else 0.25, verbose=False,
                                     return_final_partition=True, seed=s,
                                     proposal_epsilon=OPTS["proposal_epsilon"])
        assert len(EXTRA) == len(rows), (len(EXTRA), len(rows))
        df = pd.concat([pd.DataFrame(rows), pd.DataFrame(EXTRA)], axis=1)
        df["chain"] = idx
        df["chunk"] = done // chunk
        df.to_csv(out, mode="a", header=(done == 0), index=False)
        done += n
        if mode == "nk":
            assign = {int(node): int(d) for node, d in part.assignment.items()}
            _write_ckpt(ckpt, {"version": 1, "mode": mode, "idx": idx, "k": len(set(assign.values())),
                               "n_steps": n_steps, "chunk": chunk, "seed": s, "done": done, **OPTS,
                               "assignment": assign, "np_state": _np_state_out(),
                               "py_state": random.getstate()})
            state = _partition(graph, assign)
        else:
            state = part
        print(f"[{mode} {idx}] {done}/{n_steps} {time.time()-t0:.0f}s", flush=True)


def _np_state_out():
    name, keys, pos, has_gauss, cached = np.random.get_state()
    return [name, keys.tolist(), int(pos), int(has_gauss), float(cached)]


def _np_state_in(st):
    name, keys, pos, has_gauss, cached = st
    return (name, np.array(keys, dtype=np.uint32), pos, has_gauss, cached)


def _py_state_in(st):
    version, internal, gauss = st
    return (version, tuple(internal), gauss)


def _write_ckpt(ckpt, payload):
    tmp = ckpt.with_name(ckpt.name + ".tmp")
    with open(tmp, "w") as f:
        json.dump(payload, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, ckpt)


def _trim_csv(out, n_rows):
    """Keep the header and the first n_rows data lines (a crash between the CSV
    append and the checkpoint write can leave one extra chunk)."""
    with open(out, "rb") as f:
        lines = f.readlines()
    if len(lines) - 1 < n_rows:
        raise SystemExit(f"{out} has {len(lines) - 1} rows, checkpoint says {n_rows}; not resuming")
    if len(lines) - 1 > n_rows:
        with open(out, "wb") as f:
            f.writelines(lines[: n_rows + 1])
            f.flush()
            os.fsync(f.fileno())
        print(f"trimmed {len(lines) - 1 - n_rows} rows past the checkpoint", flush=True)


def resume(idx, n_steps, chunk, out, va_file, k):
    """Continue an nk chain from its checkpoint. The rows it appends are the rows
    an unbroken run would have written."""
    global GEO
    out = Path(out)
    ckpt = _ckpt_path(out)
    with open(ckpt) as f:
        c = json.load(f)
    want = {"mode": "nk", "idx": idx, "k": k, "n_steps": n_steps, "chunk": chunk, "seed": chain_seed(idx), **OPTS}
    # checkpoints written before these options existed ran with the defaults
    have = {**OPTS_DEFAULT, **c}
    bad = {key: (have.get(key), v) for key, v in want.items() if have.get(key) != v}
    if bad:
        raise SystemExit(f"checkpoint {ckpt} does not match this run (checkpoint, requested): {bad}")
    va, graph = me.build_va_graph(verbose=False, va_path=Path(va_file) if va_file else None)
    GEO = Geo(va, graph)
    _trim_csv(out, c["done"])
    np.random.set_state(_np_state_in(c["np_state"]))
    random.setstate(_py_state_in(c["py_state"]))
    assign = {int(node): d for node, d in c["assignment"].items()}
    me._bpt_global = bipartition_tree_fastfail
    set_muni(graph, OPTS["muni_surcharge"])
    set_s152(graph, k)
    print(f"[nk {idx}] resumed at {c['done']}/{n_steps}", flush=True)
    _chunks("nk", idx, graph, _partition(graph, assign), c["done"], n_steps, chunk, out, c["seed"])


def real(out, va_file, extra_maps=()):
    import geopandas as gpd

    va, graph = me.build_va_graph(verbose=False, va_path=Path(va_file) if va_file else None)
    geo = Geo(va, graph)
    res = {}
    agg = va.groupby("parent_ed_2019")[["va_ucp", "va_ndp"]].sum()
    res["2019_enacted"] = {**seat_results_close(agg["va_ucp"].values, agg["va_ndp"].values),
                           **geo.stats(va.loc[geo.nodes, "parent_ed_2019"].to_numpy())}
    maps = [("majority_2026", REPO / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"),
            ("minority_2026", REPO / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg")]
    maps += [(Path(p).stem, Path(p)) for p in extra_maps]
    pts = va.loc[geo.nodes].copy()
    pts["geometry"] = pts.geometry.representative_point()
    for name, f in maps:
        m = me.score_exogenous_map(va, f, id_col="EDName2025")
        eds = gpd.read_file(f).to_crs(pts.crs)
        j = gpd.sjoin(pts[["geometry"]], eds[["EDName2025", "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
        labels = j["EDName2025"].fillna("__unassigned__").to_numpy()
        res[name] = {**m, **geo.stats(labels)}
    Path(out).write_text(json.dumps(res, indent=1, default=float))
    for k, v in res.items():
        print(k, {x: v.get(x) for x in ("n_parts", "ucp_seats", "close4", "close4_ucp", "close4_ndp",
                                        "city_gap_pct", "n_city_districts", "towns_flagged", "towns_flagged_list")})


def _no_power_throttling():
    """Windows 11 marks windowless background processes for EcoQoS, which
    parks them on efficiency cores at low clocks (2026-10-29: 12 chains on the
    8 E-cores of an i7-1360P with the P-cores idle). Opt this process out.
    Affects speed only, never results; no-op elsewhere."""
    if sys.platform != "win32":
        return
    import ctypes

    class _State(ctypes.Structure):
        _fields_ = [("Version", ctypes.c_ulong), ("ControlMask", ctypes.c_ulong), ("StateMask", ctypes.c_ulong)]

    st = _State(1, 1, 0)  # PROCESS_POWER_THROTTLING_EXECUTION_SPEED, explicitly off
    k32 = ctypes.windll.kernel32
    k32.GetCurrentProcess.restype = ctypes.c_void_p
    k32.SetProcessInformation.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_ulong]
    k32.SetProcessInformation(k32.GetCurrentProcess(), 4, ctypes.byref(st), ctypes.sizeof(st))


if __name__ == "__main__":
    _no_power_throttling()
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["rep87", "nk", "real"])
    ap.add_argument("--k", type=int, default=89)
    ap.add_argument("--idx", type=int, default=0)
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--chunk", type=int, default=5000)
    ap.add_argument("--out", required=True)
    ap.add_argument("--va-file", default="")
    ap.add_argument("--extra", nargs="*", default=[], help="real mode: more map files (EDName2025 column)")
    ap.add_argument("--resume", action="store_true",
                    help="nk mode: continue from <out>.ckpt.json if it exists, else start fresh")
    ap.add_argument("--proposal-eps", type=float, default=None,
                    help="nk mode: ReCom split band; default = half of pop_deviation (+/-12.5%%); 0.25 = s.15(1)")
    ap.add_argument("--muni-surcharge", type=float, default=0.0,
                    help="nk mode: region_surcharge weight on 2021 CSDs (municipality-aware sensitivity); 0 = off")
    ap.add_argument("--s152", default="",
                    help="nk mode: EBCA s.15(2) mode using this per-VA criteria CSV (s152_criteria.py output)")
    a = ap.parse_args()
    OPTS.update(proposal_epsilon=a.proposal_eps, muni_surcharge=a.muni_surcharge)
    if a.s152:
        import hashlib

        S152_PATH = Path(a.s152)
        OPTS.update(s152=hashlib.sha256(S152_PATH.read_bytes()).hexdigest(), proposal_epsilon=0.5)
    if a.mode == "real":
        real(a.out, a.va_file, a.extra)
    elif a.resume and a.mode == "nk" and _ckpt_path(Path(a.out)).exists():
        resume(a.idx, a.steps, a.chunk, a.out, a.va_file, a.k)
    else:
        run(a.mode, a.idx, a.steps, a.chunk, a.out, a.va_file, a.k)
