# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
cfp_lethbridge.py

Runs preregistration/cfp_lethbridge_2026-11-07.md: the Chikina-Frieze-Pegden (2017) local outlier
test of the panel's southern configuration. A reversible single-area flip chain (uniform proposal
over (area, touching district) pairs, Metropolis-Hastings acceptance min(1, B/B')) is walked from
the panel's plan; p = sqrt(2 * eps) for each value. Queen adjacency, +/-25% of the region mean
(2021 population), contiguity. Unregistered. A local test, not a global one.

Usage: python -W ignore findings/hybrid_regions/cfp_lethbridge.py walk W STEPS
       python -W ignore findings/hybrid_regions/cfp_lethbridge.py summarize
"""
import json
import math
import random
import sys
from collections import defaultdict, deque
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis/scripts"))
sys.path.insert(0, str(ROOT / "findings/packing_cracking"))
from drand_seed import get_canonical_seed  # noqa: E402
from real_maps import MAPS, assign  # noqa: E402

EDAY = ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
ALL = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
POP = ROOT / "data/va_pop_from_das.csv"
LETHBRIDGE = "4802012"
EPS, NEAR = 0.25, 0.10
OUT = HERE / "cfp"


def setup():
    b = gpd.read_file(EDAY).to_crs(3400)
    pts = b[["geometry"]].copy()
    pts["geometry"] = b.geometry.representative_point()
    panel = assign(pts, *MAPS["panel"]).to_numpy()
    comp = json.loads((ROOT / "findings/iap_para167/comparison.json").read_text())
    grp = next(g for g in comp["groups"] if "Lethbridge" in g["panel"])["panel"]
    idx = np.where(np.isin(panel, grp))[0]
    sub = b.iloc[idx]
    sidx = sub.sindex
    adj = defaultdict(set)
    for i, geom in zip(idx, sub.geometry):
        for j in sidx.query(geom, predicate="intersects"):
            jj = idx[j]
            if jj != i:
                adj[i].add(jj)
    pop = pd.read_csv(POP).set_index("va_row_idx")["pop_2021"]
    vp = pd.Series(b.index.map(pop).values).fillna(0.0).clip(lower=1.0).to_numpy()
    csd = gpd.read_file(CSD).to_crs(3400)
    j = gpd.sjoin(pts, csd[["CSDUID", "geometry"]], how="left", predicate="within")
    leth = (j[~j.index.duplicated(keep="first")].CSDUID.astype(str).reindex(pts.index) == LETHBRIDGE).to_numpy()
    allb = gpd.read_file(ALL, ignore_geometry=True)
    return {"idx": idx, "adj": adj, "panel": panel, "pop": vp, "leth": leth,
            "u": allb.va_ucp.to_numpy(float), "n": allb.va_ndp.to_numpy(float), "districts": sorted(grp)}


def connected(nodes, adj):
    nodes = set(nodes)
    if not nodes:
        return False
    start = next(iter(nodes))
    seen, q = {start}, deque([start])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y in nodes and y not in seen:
                seen.add(y)
                q.append(y)
    return len(seen) == len(nodes)


class State:
    def __init__(self, S):
        self.S = S
        self.a = {int(i): S["panel"][i] for i in S["idx"]}
        self.members = defaultdict(set)
        for i, d in self.a.items():
            self.members[d].add(i)
        self.dpop = defaultdict(float)
        self.U, self.N, self.LN, self.LP = (defaultdict(float) for _ in range(4))
        for i, d in self.a.items():
            self._add(i, d, 1)
        self.ideal = sum(self.dpop.values()) / len(self.dpop)
        self.lp_total = sum(self.LP.values())
        self.ln_total = sum(self.LN.values())
        main = set(self.a)
        # Pins: areas that cannot reach the rest of the region under queen adjacency. They stay in
        # their district, and contiguity is judged on each district's unpinned areas.
        comps = self._components(main)
        self.pinned = set().union(*comps[1:]) if len(comps) > 1 else set()
        # Deviation from the plan (in the README): two of the panel's districts are not contiguous on the
        # voting-area graph even under queen adjacency (Lethbridge-Little Bow in 3 pieces, Banff-Canmore-
        # Diamond Valley in 2), because a line cuts voting areas that are placed by representative point.
        # So the state space allows each district no more pieces than it has in the panel's plan. That
        # is a property of the state, so the chain stays reversible.
        self.start_comps = {d: len(self._components(m - self.pinned)) for d, m in self.members.items()}
        self.foreign = {i: {self.a[j] for j in S["adj"][i] if self.a[j] != self.a[i]} for i in self.a}
        self.B = sum(len(v) for i, v in self.foreign.items() if i not in self.pinned)

    def _components(self, nodes):
        nodes, out = set(nodes), []
        while nodes:
            s = nodes.pop()
            c, q = {s}, deque([s])
            while q:
                x = q.popleft()
                for y in self.S["adj"][x]:
                    if y in nodes:
                        nodes.discard(y)
                        c.add(y)
                        q.append(y)
            out.append(c)
        return sorted(out, key=len, reverse=True)

    def _add(self, i, d, sgn):
        S = self.S
        self.dpop[d] += sgn * S["pop"][i]
        self.U[d] += sgn * S["u"][i]
        self.N[d] += sgn * S["n"][i]
        if S["leth"][i]:
            self.LN[d] += sgn * S["n"][i]
            self.LP[d] += sgn * S["pop"][i]

    def valid_initial(self):
        ok_pop = all(abs(p / self.ideal - 1) <= EPS for p in self.dpop.values())
        ok_con = {d: c for d, c in self.start_comps.items()}
        return ok_pop, ok_con

    def values(self):
        far = sum(self.LN[d] for d in self.LN if (self.N[d] - self.U[d]) / (self.N[d] + self.U[d]) <= -NEAR)
        pieces = sum(1 for d in self.LP if self.LP[d] >= 0.02 * self.lp_total)
        return far / self.ln_total, pieces

    def pairs(self):
        return [(i, d) for i, fs in self.foreign.items() if i not in self.pinned for d in fs]

    def step(self, rng, pair_list):
        i, new = pair_list[rng.randrange(len(pair_list))]
        old = self.a[i]
        np_old = self.dpop[old] - self.S["pop"][i]
        np_new = self.dpop[new] + self.S["pop"][i]
        if abs(np_old / self.ideal - 1) > EPS or abs(np_new / self.ideal - 1) > EPS:
            return False
        rest = self.members[old] - {i} - self.pinned
        if not rest or len(self._components(rest)) > self.start_comps[old]:
            return False
        touched = {i} | self.S["adj"][i]
        before = sum(len(self.foreign[x]) for x in touched if x not in self.pinned)
        self.a[i] = new
        after_f = {x: {self.a[y] for y in self.S["adj"][x] if self.a[y] != self.a[x]} for x in touched}
        after = sum(len(after_f[x]) for x in touched if x not in self.pinned)
        B_new = self.B - before + after
        if rng.random() >= min(1.0, self.B / B_new):
            self.a[i] = old
            return False
        self.members[old].discard(i)
        self.members[new].add(i)
        self._add(i, old, -1)
        self._add(i, new, 1)
        self.foreign.update(after_f)
        self.B = B_new
        return True


def walk(w, steps):
    S = setup()
    st = State(S)
    ok_pop, ok_con = st.valid_initial()
    salt = f"cfp_lethbridge_{w}"
    seed = get_canonical_seed(salt)
    rng = random.Random(seed)
    v0 = st.values()
    vals = np.empty((steps, 2), dtype=np.float32)
    accepted = 0
    pair_list = st.pairs()
    for t in range(steps):
        if st.step(rng, pair_list):
            accepted += 1
            pair_list = st.pairs()
        vals[t] = st.values()
        if (t + 1) % 100000 == 0:
            print(f"[cfp {w}] {t + 1}/{steps} accepted {accepted}", flush=True)
    moved = sum(1 for i in st.a if st.a[i] != S["panel"][i]) / len(st.a)
    OUT.mkdir(exist_ok=True)
    np.save(OUT / f"walk{w}.npy", vals)
    (OUT / f"walk{w}.json").write_text(json.dumps({"walk": w, "seed_salt": salt, "seed": seed, "steps": steps, "accepted": accepted,
                                                    "start_valid_population": ok_pop, "start_pieces_per_district_queen": ok_con,
                                                    "pinned_areas": len(st.pinned), "n_areas": len(st.a),
                                                    "start_values": {"V1_far_loss_share": float(v0[0]), "V2_pieces": int(v0[1])},
                                                    "share_areas_reassigned_at_end": moved}, indent=1))
    print(f"[cfp {w}] done start_valid pop={ok_pop} pieces={ok_con} accepted={accepted} moved={moved:.3f}", flush=True)


def summarize():
    out = {"plan": "preregistration/cfp_lethbridge_2026-11-07.md", "walks": {}}
    for f in sorted(OUT.glob("walk*.json")):
        meta = json.loads(f.read_text())
        vals = np.load(f.with_suffix(".npy"))
        r = dict(meta)
        for k, col, v0 in (("V1", 0, meta["start_values"]["V1_far_loss_share"]), ("V2", 1, meta["start_values"]["V2_pieces"])):
            eps = float((vals[:, col] >= np.float32(v0) - 1e-7).mean())
            r[k] = {"start": v0, "epsilon": round(eps, 6), "p": round(min(1.0, math.sqrt(2 * eps)), 4),
                    "walk_q05_q50_q95": [round(float(x), 4) for x in np.quantile(vals[:, col], [0.05, 0.5, 0.95])]}
        out["walks"][meta["walk"]] = r
    (HERE / "cfp_lethbridge.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "walk":
        walk(int(sys.argv[2]), int(sys.argv[3]))
    else:
        summarize()
