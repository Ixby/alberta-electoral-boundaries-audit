# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
territory_score.py
------------------

Scores territory_null.py plans, and real maps, on one substrate, for the two
Amendment 8 (draft) tests and their calibration.

Substrate (identical for neutral plans and real maps):
  - the canonical VA graph (mcmc_ensemble.build_va_graph) and its 2023
    election-day two-party votes (va_ucp, va_ndp);
  - a real map's districts are assigned to VAs by representative point;
  - district adjacency = two districts share a VA-graph edge.

Measures per full 91-district map:
  eg, mean_median, declination, ucp_seats   mcmc_ensemble.seat_results (UCP-positive)
  drain                                      the registered neighbour-drain score
      (drain_label_shuffle_null.drain_score: sum over coupled directed adjacent
      pairs of max(0, s_X - 0.15) * max(0, 0.05 - m_Y)), vectorised here and
      checked against the original function by --selftest.
  drain_shuffle_p                            two-sided p of the registered
      label-shuffle null (vote vectors permuted across districts, adjacency fixed).

Subcommands
  selftest           vectorised drain == original drain_score on the majority map
  plans DIR          score every chain*_plans.npy in DIR -> DIR/scores.csv
  real MAP.gpkg ...  score real maps (EDName2025 column) -> stdout JSON
  calibrate DIR      chain diagnostics, holdout false-positive rates -> DIR/calibration.json
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import mcmc_ensemble as me  # noqa: E402
import territory_null as tn  # noqa: E402

S_T, M_T = 0.15, 0.05
_orig_seat_results = me.seat_results


class Substrate:
    def __init__(self, enacted=None, stated_low=None):
        self.va, self.graph = me.build_va_graph(verbose=False)
        self.nodes = sorted(self.graph.nodes())
        self.pos = {n: i for i, n in enumerate(self.nodes)}
        self.ucp = np.array([self.graph.nodes[n]["va_ucp"] for n in self.nodes], float)
        self.ndp = np.array([self.graph.nodes[n]["va_ndp"] for n in self.nodes], float)
        e = np.array([(self.pos[a], self.pos[b]) for a, b in self.graph.edges()])
        self.ea, self.eb = e[:, 0], e[:, 1]
        lab, terr, self.k_terr, self.s152_cap = tn.territory(self.va, self.graph, enacted, stated_low=stated_low)
        self.terr_idx = np.array([self.pos[n] for n in terr])
        fixed_names = sorted(set(lab.values()))
        self.n_fixed = len(fixed_names)
        assert self.n_fixed + self.k_terr == tn.K_PROV, (self.n_fixed, self.k_terr)
        fid = {s: i for i, s in enumerate(fixed_names)}
        self.base = np.array([fid[lab[n]] if n in lab else -1 for n in self.nodes])

    def plan_labels(self, plan):
        lab = self.base.copy()
        lab[self.terr_idx] = self.n_fixed + plan.astype(int)
        assert (lab >= 0).all()
        return lab

    def map_labels(self, gpkg):
        import geopandas as gpd

        pts = self.va.loc[self.nodes, ["geometry"]].copy()
        pts["geometry"] = pts.geometry.representative_point()
        g = gpd.read_file(gpkg).to_crs(pts.crs)
        j = gpd.sjoin(pts, g[["EDName2025", "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
        names = j["EDName2025"]
        if names.isna().any():
            raise SystemExit(f"{gpkg}: {int(names.isna().sum())} VAs fall outside every district")
        uniq = sorted(names.unique())
        return np.array([uniq.index(s) for s in names]), uniq

    def tallies(self, lab):
        k = lab.max() + 1
        return np.bincount(lab, self.ucp, k), np.bincount(lab, self.ndp, k)

    def pairs(self, lab):
        a, b = lab[self.ea], lab[self.eb]
        d = a != b
        u = np.unique(np.sort(np.c_[a[d], b[d]], axis=1), axis=0)
        return np.r_[u[:, 0], u[:, 1]], np.r_[u[:, 1], u[:, 0]]  # directed X -> Y

    def score(self, lab, n_shuffle=0, rng=None):
        ucp, ndp = self.tallies(lab)
        m = _orig_seat_results(ucp, ndp)
        X, Y = self.pairs(lab)
        out = {"eg": m["efficiency_gap"], "mean_median": m["mean_median"], "declination": m["declination"],
               "ucp_seats": m["ucp_seats"], "n_districts": int(len(ucp)), "drain": drain(ndp, ucp, X, Y)}
        if n_shuffle:
            null = drain_shuffle(ndp, ucp, X, Y, n_shuffle, rng)
            r = float(np.mean(null <= out["drain"]))
            out["drain_shuffle_p"] = 2 * min(r, 1 - r)
        return out


def _sm(ndp, ucp):
    tot = ndp + ucp
    thr = np.floor(tot / 2) + 1
    s = np.maximum(np.maximum(ndp, ucp) - thr, 0) / tot
    m = np.abs(ndp - ucp) / tot
    loser = np.sign(ucp - ndp)  # +1: NDP lost, -1: UCP lost, 0: tie (ties couple with ties, as the original)
    return s, m, loser


def drain(ndp, ucp, X, Y):
    s, m, loser = _sm(ndp, ucp)
    c = loser[X] == loser[Y]
    return float(np.sum(np.maximum(0, s[X] - S_T) * np.maximum(0, M_T - m[Y]) * c))


def drain_shuffle(ndp, ucp, X, Y, n, rng):
    """The registered label-shuffle null, vectorised: each permutation reassigns the
    districts' (ndp, ucp) vectors; the adjacency pairs stay fixed. Votes are cast to
    int, as drain_label_shuffle_null.label_shuffle_null does."""
    v = np.c_[ndp, ucp].astype(int).astype(float)
    out = np.empty(n)
    for i0 in range(0, n, 500):
        b = min(500, n - i0)
        P = np.argsort(rng.random((b, len(v))), axis=1)
        s, m, loser = _sm(v[P, 0], v[P, 1])
        c = loser[:, X] == loser[:, Y]
        out[i0:i0 + b] = np.sum(np.maximum(0, s[:, X] - S_T) * np.maximum(0, M_T - m[:, Y]) * c, axis=1)
    return out


def shuffle_rng(tag):
    h = hashlib.sha256((tn.RANDOMNESS + f"a8-drain-label-shuffle-{tag}").encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:4], "big"))


def selftest(S):
    from drain_label_shuffle_null import drain_score, directed_pairs_from_undirected
    from neighbour_drain_adjacency import compute_ed_metrics

    lab, names = S.map_labels(tn.MAJ)
    ucp, ndp = S.tallies(lab)
    X, Y = S.pairs(lab)
    votes = {names[i]: (ndp[i], ucp[i]) for i in range(len(names))}
    look = compute_ed_metrics(votes).set_index("ed").to_dict("index")
    und = sorted({tuple(sorted((names[x], names[y]))) for x, y in zip(X, Y)})
    ref = drain_score(pd.DataFrame(directed_pairs_from_undirected(und), columns=["X", "Y"]), look)
    mine = drain(ndp, ucp, X, Y)
    print(json.dumps({"majority_drain_original_fn": ref, "majority_drain_vectorised": mine,
                      "n_undirected_pairs": len(und)}))
    assert abs(ref - mine) < 1e-12


def score_plans(S, d):
    rows = []
    for f in sorted(Path(d).glob("chain*_plans.npy")):
        idx = int(f.stem.split("_")[0][5:])
        meta = json.loads(f.with_suffix(".json").read_text())
        for k, plan in enumerate(np.load(f)):
            r = S.score(S.plan_labels(plan))
            r.update(chain=idx, step=meta["plan_step"][k], s152=meta["s152_districts"][k])
            rows.append(r)
    df = pd.DataFrame(rows)
    df.to_csv(Path(d) / "scores.csv", index=False)
    print(df.groupby("chain")[["eg", "drain", "mean_median", "ucp_seats", "s152"]].mean())


def rhat(chains):
    """Split-R-hat (Gelman et al. 2013) over equal-length chains."""
    n = min(len(c) for c in chains) // 2 * 2
    xs = [c[:n] for c in chains]
    xs = [h for c in xs for h in (c[: n // 2], c[n // 2:])]
    m, L = len(xs), n // 2
    means = np.array([x.mean() for x in xs])
    W = np.mean([x.var(ddof=1) for x in xs])
    B = L * means.var(ddof=1)
    return float(np.sqrt(((L - 1) / L * W + B / L) / W))


def calibrate(S, d, ref_chains, holdout, n_shuffle_plans, n_shuffle, burn):
    df = pd.read_csv(Path(d) / "scores.csv")
    df = df[df.step > burn]
    ref = df[df.chain.isin(ref_chains)]
    hold = df[df.chain == holdout]
    res = {"burn_in_steps": burn, "ref_chains": ref_chains, "holdout_chain": holdout,
           "n_ref_plans": int(len(ref)), "n_holdout_plans": int(len(hold))}
    for v in ("eg", "drain", "mean_median", "declination"):
        r = ref[v].to_numpy()
        h = hold[v].to_numpy()
        lo = np.array([np.mean(r <= x) for x in h])
        hi = np.array([np.mean(r >= x) for x in h])
        p = np.minimum(1, 2 * np.minimum(lo, hi))
        res[v] = {"rhat_ref": rhat([ref[ref.chain == c][v].to_numpy() for c in ref_chains]),
                  "ref_mean": float(r.mean()), "ref_p025": float(np.quantile(r, .025)),
                  "ref_p975": float(np.quantile(r, .975)),
                  "holdout_fpr_two_sided_005": float(np.mean(p < 0.05)),
                  "holdout_fpr_two_sided_001": float(np.mean(p < 0.01))}
    # The registered label-shuffle drain null, applied to neutral plans: how often does it flag one?
    plans = {}
    for c in ref_chains + [holdout]:
        plans[c] = np.load(Path(d) / f"chain{c}_plans.npy")
    pick = hold.iloc[np.linspace(0, len(hold) - 1, n_shuffle_plans).astype(int)]
    meta = json.loads((Path(d) / f"chain{holdout}_plans.json").read_text())
    step_to_k = {s: k for k, s in enumerate(meta["plan_step"])}
    rng = shuffle_rng("calibration")
    ps = [S.score(S.plan_labels(plans[holdout][step_to_k[s]]), n_shuffle, rng)["drain_shuffle_p"]
          for s in pick.step]
    res["drain_label_shuffle"] = {"n_plans": n_shuffle_plans, "n_permutations": n_shuffle,
                                  "fpr_two_sided_005": float(np.mean(np.array(ps) < 0.05)),
                                  "p_values": ps}
    (Path(d) / "calibration.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != "drain_label_shuffle"}, indent=1))
    print("label-shuffle FPR:", res["drain_label_shuffle"]["fpr_two_sided_005"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    p = sp.add_parser("plans"); p.add_argument("dir")
    p.add_argument("--enacted", help="the scored map, for a rerun under Amendment 8, Part 5 (as rank takes it)")
    p.add_argument("--stated-low", type=int)
    p = sp.add_parser("real"); p.add_argument("maps", nargs="+"); p.add_argument("--shuffle", type=int, default=10_000)
    p = sp.add_parser("rank", help="R1/R2: rank a map against scored plans (DIR/scores.csv)")
    p.add_argument("map"); p.add_argument("dir"); p.add_argument("--ref", type=int, nargs="+", default=[1, 2, 3, 4])
    p.add_argument("--burn", type=int, default=10_000); p.add_argument("--stated-low", type=int, required=True)
    p = sp.add_parser("calibrate"); p.add_argument("dir"); p.add_argument("--ref", type=int, nargs="+", required=True)
    p.add_argument("--holdout", type=int, required=True); p.add_argument("--shuffle-plans", type=int, default=200)
    p.add_argument("--shuffle", type=int, default=2_000); p.add_argument("--burn", type=int, default=10_000)
    p.add_argument("--enacted"); p.add_argument("--stated-low", type=int)
    a = ap.parse_args()
    if getattr(a, "enacted", None) and a.stated_low is None:
        ap.error("--enacted needs --stated-low")
    S = Substrate(a.map if a.cmd == "rank" else getattr(a, "enacted", None), getattr(a, "stated_low", None))
    if a.cmd == "selftest":
        selftest(S)
    elif a.cmd == "plans":
        score_plans(S, a.dir)
    elif a.cmd == "real":
        out = {}
        for f in a.maps:
            lab, _ = S.map_labels(f)
            out[Path(f).stem] = S.score(lab, a.shuffle, shuffle_rng(Path(f).stem))
        print(json.dumps(out, indent=1))
    elif a.cmd == "rank":
        lab, _ = S.map_labels(a.map)
        obs = S.score(lab, 10_000, shuffle_rng(Path(a.map).stem))
        df = pd.read_csv(Path(a.dir) / "scores.csv")
        ref = df[(df.step > a.burn) & df.chain.isin(a.ref)]
        out = {"map": a.map, "observed": obs, "n_ref_plans": int(len(ref))}
        for v in ("eg", "drain", "mean_median", "declination", "ucp_seats"):
            r = ref[v].to_numpy()
            out[v] = {"observed": obs[v], "p_two_sided": float(min(1, 2 * min(np.mean(r <= obs[v]), np.mean(r >= obs[v])))),
                      "null_mean": float(r.mean())}
        print(json.dumps(out, indent=1, default=float))
    else:
        calibrate(S, a.dir, a.ref, a.holdout, a.shuffle_plans, a.shuffle, a.burn)
