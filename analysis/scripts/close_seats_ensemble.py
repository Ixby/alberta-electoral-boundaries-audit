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
        j = gpd.sjoin(pts[["geometry"]], csd[["CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
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
    def __next__(self):
        part = super().__next__()
        EXTRA.append(GEO.stats([part.assignment[n] for n in GEO.nodes]))
        return part


me.MarkovChain = RecordingChain

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
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    t0 = time.time()
    done = 0
    while done < n_steps:
        n = min(chunk, n_steps - done)
        EXTRA.clear()
        rows, state = me.run_ensemble(graph, state, n, pop_deviation=0.25, verbose=False,
                                      return_final_partition=True, seed=s)
        assert len(EXTRA) == len(rows), (len(EXTRA), len(rows))
        df = pd.concat([pd.DataFrame(rows), pd.DataFrame(EXTRA)], axis=1)
        df["chain"] = idx
        df["chunk"] = done // chunk
        df.to_csv(out, mode="a", header=(done == 0), index=False)
        done += n
        print(f"[{mode} {idx}] {done}/{n_steps} {time.time()-t0:.0f}s", flush=True)


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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["rep87", "nk", "real"])
    ap.add_argument("--k", type=int, default=89)
    ap.add_argument("--idx", type=int, default=0)
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--chunk", type=int, default=5000)
    ap.add_argument("--out", required=True)
    ap.add_argument("--va-file", default="")
    ap.add_argument("--extra", nargs="*", default=[], help="real mode: more map files (EDName2025 column)")
    a = ap.parse_args()
    if a.mode == "real":
        real(a.out, a.va_file, a.extra)
    else:
        run(a.mode, a.idx, a.steps, a.chunk, a.out, a.va_file, a.k)
