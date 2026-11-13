# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
lethbridge_rerun.py

The rerun owed under preregistration/rural_voice_2026-11-07.md ("Neutral comparison"): the south
region's neutral redraws, city-blind and municipality-aware, replayed with the same seeds and
settings, with the plan's measures 1-2 recorded for every plan. Then the panel's 8,138 (Lethbridge
County rural residents in urban-majority divisions) is ranked among them. Unregistered.

Neither original script is edited. Each variant is replayed through its own generator's loop:
  blind  findings/six_signals/regional_south.py run(): salts regional_south_1..4, total_steps 50,000
         with the first 1,000 discarded inside that (49,000 plans kept per chain). This is the
         city-blind set findings/hybrid_regions/summarize() reads for Lethbridge.
  muni   findings/hybrid_regions/regional_redraw.py run("Lethbridge", "muni", c, 50000): salts
         regional_Lethbridge_muni_1..4, total_steps 51,000, first 1,000 discarded (50,000 kept).
The loop bodies below are copied from those run() functions line for line; the only addition is
the rural measures per plan. Each chain also writes the original measure columns so the replay can
be checked row for row against the committed CSVs (`check`).

Rural = a voting area whose representative point (on build_va_graph's geometry, as rural_voice.py
takes it) lies outside every 2021 city (CY) or town (T) CSD. Votes: all 2023 ballots primary,
election-day beside, UCP and NDP only. Describes population and 2023 votes, not intent.

Usage: python -W ignore findings/rural_voice/lethbridge_rerun.py selfcheck
       python -W ignore findings/rural_voice/lethbridge_rerun.py run blind|muni CHAIN [STEPS]
       python -W ignore findings/rural_voice/lethbridge_rerun.py check
       python -W ignore findings/rural_voice/lethbridge_rerun.py summarize
"""
import json
import random
import sys
from functools import partial
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis/scripts"))
sys.path.insert(0, str(ROOT / "findings/packing_cracking"))
sys.path.insert(0, str(ROOT / "findings/six_signals"))
sys.path.insert(0, str(ROOT / "findings/hybrid_regions"))
import mcmc_ensemble as me  # noqa: E402
from drand_seed import get_canonical_seed  # noqa: E402

CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
OUT = HERE / "lethbridge_chains"
PANEL_8138 = 8138
RCOLS = ["rural_in_urbmaj", "leth_rural_in_urbmaj", "mixed", "urbmaj_mixed",
         "over_div_all", "over_res_all", "over_vot_all", "over_div_ed", "over_res_ed", "over_vot_ed"]


def rural_layer():
    """Rural flag and Lethbridge focus mask, computed exactly as rural_voice.py computes them."""
    va, _ = me.build_va_graph(verbose=False)
    pts = va[["geometry"]].copy()
    pts["geometry"] = va.geometry.representative_point()
    csd = gpd.read_file(CSD).to_crs(pts.crs)
    j = gpd.sjoin(pts, csd[["CSDUID", "CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    name, typ = j.CSDNAME.fillna("").to_numpy(), j.CSDTYPE.fillna("").to_numpy()
    rural = ~np.isin(typ, ["CY", "T"])
    focus = np.isin(name, ["Lethbridge", "Lethbridge County"])
    return rural, focus, va.pop_2021.to_numpy(float)


def rural_measures(nodes, lab, rural, focus, pop, votes):
    """Plan measures 1-2 over the region's divisions. nodes: VA ids; lab: district per node.
    votes: {"all": (ucp, ndp), "ed": (ucp, ndp)} full-length arrays."""
    idx = np.asarray(nodes)
    _, inv = np.unique(lab, return_inverse=True)
    k = inv.max() + 1
    r, f, p = rural[idx], focus[idx], pop[idx]
    P = np.bincount(inv, weights=p, minlength=k)
    RP = np.bincount(inv, weights=p * r, minlength=k)
    share = RP / P
    urbmaj = share < .5
    mixed = (share >= .05) & (share <= .95)
    out = [float(RP[urbmaj].sum()),
           float(np.bincount(inv, weights=p * r * f, minlength=k)[urbmaj].sum()),
           int(mixed.sum()), int((mixed & urbmaj).sum())]
    for key in ("all", "ed"):
        u, n = votes[key][0][idx], votes[key][1][idx]
        U, N = np.bincount(inv, weights=u, minlength=k), np.bincount(inv, weights=n, minlength=k)
        RU, RN = np.bincount(inv, weights=u * r, minlength=k), np.bincount(inv, weights=n * r, minlength=k)
        over = mixed & ((U > N) != (RU > RN))
        out += [int(over.sum()), float(RP[over].sum()), float((RU + RN)[over].sum())]
    return out


def labels(S, lab_by_node):
    return np.array([lab_by_node[n] if n in lab_by_node else lab_by_node[S["anchor"][n]] for n in S["nodes"]])


def variant_setup(variant):
    if variant == "blind":
        import regional_south as gen
        S = gen.setup()
        return gen, S, S["pop"], {"all": S["all"], "ed": S["ed"]}, gen.COLS
    import regional_redraw as gen
    S = gen.setup("Lethbridge")
    B = S["B"]
    return gen, S, B["pop"], {"all": B["all"], "ed": B["ed"]}, gen.COLS


def selfcheck():
    rural, focus, pop = rural_layer()
    res = {}
    for v in ("blind", "muni"):
        gen, S, spop, votes, cols = variant_setup(v)
        assert np.allclose(spop, pop), "population arrays differ between the generator and rural_voice"
        panel = S["panel"] if v == "blind" else S["B"]["panel"]
        panel = np.asarray(panel)
        lab = labels(S, {n: panel[n] for n in S["nodes"]})
        res[v] = dict(zip(RCOLS, rural_measures(S["nodes"], lab, rural, focus, pop, votes)))
        res[v]["focus_rural_total_in_region"] = float(pop[np.asarray(S["nodes"])][(rural & focus)[np.asarray(S["nodes"])]].sum())
        res[v]["focus_rural_total_province"] = float(pop[rural & focus].sum())
    print(json.dumps(res, indent=1))
    for v in res:
        assert round(res[v]["leth_rural_in_urbmaj"]) == PANEL_8138, (v, res[v]["leth_rural_in_urbmaj"])
        assert round(res[v]["focus_rural_total_in_region"]) == round(res[v]["focus_rural_total_province"]), "region does not hold all of Lethbridge County"
    print("SELFCHECK OK: panel gives", PANEL_8138, "on both setups")
    return res


def run(variant, chain, steps=None):
    from gerrychain import MarkovChain, Partition
    from gerrychain.accept import always_accept
    from gerrychain.constraints import contiguous, within_percent_of_ideal_population
    from gerrychain.proposals import recom
    from gerrychain.tree import recursive_tree_part
    from gerrychain.updaters import Tally

    rural, focus, pop = rural_layer()
    gen, S, spop, votes, cols = variant_setup(variant)
    assert np.allclose(spop, pop)
    OUT.mkdir(exist_ok=True)
    stem = f"{variant}_{chain}"
    rows = []
    if variant == "blind":
        steps = steps or 50000
        salt = f"regional_south_{chain}"
        committed = json.loads((ROOT / f"findings/six_signals/regional_south/chain{chain}.json").read_text())
        seed = get_canonical_seed(salt)
        assert seed == committed["seed"], (seed, committed["seed"])
        # ---- copied from regional_south.run() ----
        random.seed(seed)
        np.random.seed(seed % 2**32)
        g = S["graph"]
        for n in g.nodes:
            g.nodes[n]["pop_rs"] = float(S["pop"][n])
        for n, a in S["anchor"].items():
            g.nodes[a]["pop_rs"] += float(S["pop"][n])
        total = sum(g.nodes[n]["pop_rs"] for n in g.nodes)
        k = len(set(S["panel"][n] for n in S["nodes"]))
        assignment = recursive_tree_part(g, range(k), total / k, "pop_rs", gen.BASE_EPS / 2, node_repeats=2)
        part = Partition(g, assignment, updaters={"population": Tally("pop_rs", alias="population")})
        ideal = sum(part["population"].values()) / len(part)
        eps = gen.BASE_EPS
        prop = partial(recom, pop_col="pop_rs", pop_target=ideal, epsilon=eps, node_repeats=2)
        ch = MarkovChain(prop, constraints=[contiguous, within_percent_of_ideal_population(part, eps)],
                         accept=always_accept, initial_state=part, total_steps=steps)
        for i, p in enumerate(ch):
            if i < gen.BURN:
                continue
            rows.append(gen.measures(S, p.assignment) + rural_measures(S["nodes"], labels(S, p.assignment), rural, focus, pop, votes))
            if (i + 1) % 5000 == 0:
                print(f"[{stem}] {i + 1}/{steps}", flush=True)
        # ---- end copy ----
        meta = {"generator": "findings/six_signals/regional_south.py run()", "seed_salt": salt, "seed": seed,
                "total_steps": steps, "burn_in_discarded_within": gen.BURN, "plans_kept": len(rows), "epsilon": eps}
    else:
        steps = steps or 50000
        salt = f"regional_Lethbridge_muni_{chain}"
        committed = json.loads((ROOT / f"findings/hybrid_regions/chains/Lethbridge_muni_{chain}.json").read_text())
        seed = get_canonical_seed(salt)
        assert seed == committed["seed"], (seed, committed["seed"])
        # ---- copied from regional_redraw.run("Lethbridge", "muni", chain, steps) ----
        random.seed(seed)
        np.random.seed(seed % 2**32)
        g = S["graph"]
        for n in g.nodes:
            g.nodes[n]["pop_rs"] = float(S["B"]["pop"][n])
            g.nodes[n]["csduid"] = S["B"]["csduid"][n]
        for n, a in S["anchor"].items():
            g.nodes[a]["pop_rs"] += float(S["B"]["pop"][n])
        k = len(S["R"]["districts"])
        total = sum(g.nodes[n]["pop_rs"] for n in g.nodes)
        surcharge = {"csduid": gen.MUNI_W}
        assignment = recursive_tree_part(g, range(k), total / k, "pop_rs", gen.EPS / 2, node_repeats=2)
        part = Partition(g, assignment, updaters={"population": Tally("pop_rs", alias="population")})
        ideal = total / k
        prop = partial(recom, pop_col="pop_rs", pop_target=ideal, epsilon=gen.EPS, node_repeats=2, region_surcharge=surcharge)
        ch = MarkovChain(prop, constraints=[contiguous, within_percent_of_ideal_population(part, gen.EPS)],
                         accept=always_accept, initial_state=part, total_steps=steps + gen.BURN)
        for i, p in enumerate(ch):
            if i >= gen.BURN:
                rows.append(gen.measures(S, p.assignment) + rural_measures(S["nodes"], labels(S, p.assignment), rural, focus, pop, votes))
                if (i + 1) % 5000 == 0:
                    print(f"[{stem}] {i + 1}/{steps + gen.BURN}", flush=True)
        # ---- end copy ----
        meta = {"generator": "findings/hybrid_regions/regional_redraw.py run('Lethbridge', 'muni', chain, steps)", "seed_salt": salt,
                "seed": seed, "total_steps": steps + gen.BURN, "burn_in_discarded": gen.BURN, "plans_kept": len(rows),
                "epsilon": gen.EPS, "muni_weight": gen.MUNI_W}
    df = pd.DataFrame(rows, columns=list(cols) + RCOLS)
    for c in ("rural_in_urbmaj", "leth_rural_in_urbmaj", "over_res_all", "over_vot_all", "over_res_ed", "over_vot_ed"):
        df[c] = df[c].round(1)
    df.to_csv(OUT / f"{stem}.csv", index=False)
    (OUT / f"{stem}.json").write_text(json.dumps({"variant": variant, "chain": chain, **meta,
                                                  "districts": 8, "n_vas": len(S["nodes"])}, indent=1))
    print(f"[{stem}] done, {len(rows)} plans", flush=True)


def original_csv(variant, chain):
    if variant == "blind":
        return ROOT / f"findings/six_signals/regional_south/chain{chain}.csv"
    return ROOT / f"findings/hybrid_regions/chains/Lethbridge_muni_{chain}.csv"


def check():
    res = {}
    for f in sorted(OUT.glob("*.csv")):
        v, c = f.stem.split("_")
        new = pd.read_csv(f)
        old = pd.read_csv(original_csv(v, int(c)))
        same_len = len(new) == len(old)
        cols = list(old.columns)
        if same_len:
            eq = np.isclose(new[cols].to_numpy(float), old[cols].to_numpy(float), rtol=0, atol=1e-9).all(axis=1)
            res[f.stem] = {"rows": len(new), "rows_equal": int(eq.sum()), "first_mismatch": int(np.argmin(eq)) if not eq.all() else None}
        else:
            res[f.stem] = {"rows": len(new), "original_rows": len(old), "rows_equal": None}
    print(json.dumps(res, indent=1))
    return res


def summarize():
    sc = json.loads((HERE / "lethbridge_rerun_selfcheck.json").read_text())
    rep = check()
    out = {"plan": "preregistration/rural_voice_2026-11-07.md (commit c01cbdcd), 'Neutral comparison'",
           "status": "unregistered", "primary_ballots": "all (election-day beside)",
           "panel": sc["muni"], "replay_check": rep, "variants": {}}
    for v in ("blind", "muni"):
        files = sorted(OUT.glob(f"{v}_*.csv"))
        if not files:
            continue
        d = pd.concat([pd.read_csv(f) for f in files])
        vb = {"chains": [json.loads(f.with_suffix(".json").read_text()) for f in files], "n_plans": int(len(d)), "measures": {}}
        for c in RCOLS:
            x = d[c].to_numpy(float)
            val = float(sc[v][c])
            vb["measures"][c] = {"q05": round(float(np.quantile(x, .05)), 1), "q50": round(float(np.quantile(x, .5)), 1),
                                 "q95": round(float(np.quantile(x, .95)), 1), "mean": round(float(x.mean()), 1),
                                 "share_zero": round(float((x == 0).mean()), 4),
                                 "panel": round(val, 1),
                                 "panel_pct_midrank": round(100 * float((x < val - 0.5).mean() + 0.5 * (np.abs(x - val) <= 0.5).mean()), 2),
                                 "share_at_or_above_panel": round(float((x >= val - 0.5).mean()), 4)}
        x = d["leth_rural_in_urbmaj"].to_numpy(float)
        vb["leth_rural_in_urbmaj_chain_medians"] = [round(float(pd.read_csv(f).leth_rural_in_urbmaj.median()), 1) for f in files]
        vb["leth_rural_in_urbmaj_chain_pct_panel"] = [round(100 * float((pd.read_csv(f).leth_rural_in_urbmaj < PANEL_8138 - .5).mean()
                                                                        + .5 * (np.abs(pd.read_csv(f).leth_rural_in_urbmaj - PANEL_8138) <= .5).mean()), 2) for f in files]
        vb["leth_rural_in_urbmaj_hist_5000"] = {f"{lo}-{lo + 4999}": int(((x >= lo) & (x < lo + 5000)).sum()) for lo in range(0, 15000, 5000)}
        out["variants"][v] = vb
    (HERE / "lethbridge_rerun.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    print(json.dumps({v: out["variants"][v]["measures"]["leth_rural_in_urbmaj"] for v in out["variants"]}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "selfcheck":
        r = selfcheck()
        (HERE / "lethbridge_rerun_selfcheck.json").write_text(json.dumps(r, indent=1))
    elif cmd == "run":
        run(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else None)
    elif cmd == "check":
        check()
    else:
        summarize()
