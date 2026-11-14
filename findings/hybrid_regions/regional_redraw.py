# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
regional_redraw.py

Runs preregistration/hybrid_regions_2026-11-07.md: neutral ReCom redraws of each region where the
panel's map has a hybrid riding, city-blind and municipality-aware (region surcharge 0.5 on 2021
CSDs). All other divisions are held fixed. All ballots are the primary figures; election-day figures
are recorded but not read. Unregistered. Describes where votes land, not intent.

Usage: python -W ignore findings/hybrid_regions/regional_redraw.py regions
       python -W ignore findings/hybrid_regions/regional_redraw.py worker W NW
       python -W ignore findings/hybrid_regions/regional_redraw.py summarize
"""
import json
import random
import sys
from functools import partial
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis/scripts"))
sys.path.insert(0, str(ROOT / "findings/packing_cracking"))
import mcmc_ensemble as me  # noqa: E402
from drand_seed import get_canonical_seed  # noqa: E402
from real_maps import MAPS, assign  # noqa: E402

ALL = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
EDAY = ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
CSD = ROOT / "data/shapefiles/reference/alberta_2021_csds.gpkg"
CPOP = ROOT / "data/reference/alberta_2021_csd_populations.csv"
NEAR, EPS, BURN, MUNI_W = 0.10, 0.25, 1000, 0.5
OUT = HERE / "chains"
_CACHE = {}


def base():
    if "b" in _CACHE:
        return _CACHE["b"]
    va, graph = me.build_va_graph(verbose=False)
    b = gpd.read_file(EDAY).to_crs(3400)
    assert len(va) == len(b)
    pts = b[["geometry"]].copy()
    pts["geometry"] = b.geometry.representative_point()
    panel = assign(pts, *MAPS["panel"]).to_numpy()
    major = assign(pts, *MAPS["majority"]).to_numpy()
    csd = gpd.read_file(CSD).to_crs(3400)
    j = gpd.sjoin(pts, csd[["CSDUID", "CSDNAME", "CSDTYPE", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    allb = gpd.read_file(ALL, ignore_geometry=True)
    _CACHE["b"] = {"va": va, "graph": graph, "geom": b.geometry, "panel": panel, "majority": major,
                   "csduid": j.CSDUID.astype(str).where(j.CSDUID.notna(), None).to_numpy(), "csdname": j.CSDNAME.fillna("").to_numpy(),
                   "csdtype": j.CSDTYPE.fillna("").to_numpy(), "pop": va.pop_2021.to_numpy(float),
                   "ed": (va.va_ucp.to_numpy(float), va.va_ndp.to_numpy(float)),
                   "all": (allb.va_ucp.to_numpy(float), allb.va_ndp.to_numpy(float))}
    return _CACHE["b"]


def define_regions():
    B = base()
    cpop = pd.read_csv(CPOP, dtype={"ALT_GEO_CODE": str}).set_index("ALT_GEO_CODE").population_2021
    big = {u for u, t in zip(B["csduid"], B["csdtype"]) if u and t == "CY" and cpop.get(u, 0) >= 20000}
    df = pd.DataFrame({"d": B["panel"], "u": B["csduid"], "n": B["csdname"], "p": B["pop"]})
    tot = df.groupby("d").p.sum()
    adj = {}
    for a, b2 in B["graph"].edges:
        da, db = B["panel"][a], B["panel"][b2]
        if da != db:
            adj.setdefault(da, set()).add(db)
            adj.setdefault(db, set()).add(da)
    hybrids = {}
    for (d, u), v in df[df.u.isin(big)].groupby(["d", "u"]).p.sum().items():
        if 0.05 <= v / tot[d] <= 0.95:
            hybrids.setdefault(u, []).append(d)
    comp = json.loads((ROOT / "findings/iap_para167/comparison.json").read_text())
    south = next(g for g in comp["groups"] if "Lethbridge" in g["panel"])["panel"]
    name = dict(zip(df.u, df.n))
    regions = {}
    for u, hyb in hybrids.items():
        city = name[u]
        if city == "Lethbridge":
            regions["Lethbridge"] = {"cities": [u], "districts": sorted(south)}
            continue
        cityp = df[df.u == u].groupby("d").p.sum()
        holders = set(cityp[cityp >= 0.02 * cityp.sum()].index)
        ds = set(hyb) | set().union(*(adj.get(h, set()) for h in hyb))
        if city not in ("Calgary", "Edmonton"):
            ds |= holders
        key = city
        regions.setdefault(key, {"cities": [], "districts": []})
        regions[key]["cities"] = sorted(set(regions[key]["cities"]) | {u})
        regions[key]["districts"] = sorted(set(regions[key]["districts"]) | ds)
        regions[key]["hybrids"] = sorted(set(regions[key].get("hybrids", [])) | set(hyb))
    if "Leduc" in regions and "Beaumont" in regions:
        a, b2 = regions.pop("Leduc"), regions.pop("Beaumont")
        regions["Leduc and Beaumont"] = {"cities": sorted(set(a["cities"]) | set(b2["cities"])), "districts": sorted(set(a["districts"]) | set(b2["districts"])),
                                         "hybrids": sorted(set(a.get("hybrids", [])) | set(b2.get("hybrids", [])))}
    for k, r in regions.items():
        r["n_vas"] = int(np.isin(B["panel"], r["districts"]).sum())
    HERE.mkdir(exist_ok=True)
    (HERE / "regions.json").write_text(json.dumps(regions, indent=1), encoding="utf8")
    return regions


def setup(region):
    B = base()
    R = json.loads((HERE / "regions.json").read_text())[region]
    mask = np.isin(B["panel"], R["districts"])
    nodes = [n for n in B["graph"].nodes if mask[n]]
    sub = B["graph"].subgraph(nodes).copy()
    comps = sorted(nx.connected_components(sub), key=len, reverse=True)
    cen = B["geom"].centroid
    anchor = {}
    for c in comps[1:]:
        cc = gpd.GeoSeries([cen[n] for n in c]).union_all().centroid
        a = min(comps[0], key=lambda m: cen[m].distance(cc))
        for n in c:
            anchor[n] = a
    city = np.isin(B["csduid"].astype(str), R["cities"])
    maj = sorted(set(B["majority"][mask]))
    maj_closed = bool(np.isin(B["majority"], maj).sum() == mask.sum() and np.isin(B["majority"][mask], maj).all())
    return {"B": B, "R": R, "graph": sub.subgraph(comps[0]).copy(), "nodes": nodes, "anchor": anchor, "city": city, "maj_closed": maj_closed}


COLS = [f"{m}_{b}" for b in ("all", "ed") for m in ("ndp_seats", "city_won", "city_near", "city_far")] + ["city_pieces"]


def measures(S, lab_by_node):
    B = S["B"]
    idx = np.array(S["nodes"])
    lab = np.array([lab_by_node[n] if n in lab_by_node else lab_by_node[S["anchor"][n]] for n in S["nodes"]])
    _, inv = np.unique(lab, return_inverse=True)
    C = S["city"][idx]
    out = []
    for key in ("all", "ed"):
        u, n = B[key][0][idx], B[key][1][idx]
        U, N = np.bincount(inv, weights=u), np.bincount(inv, weights=n)
        m = (N - U) / (N + U)
        cn = np.bincount(inv[C], weights=n[C], minlength=len(U))
        t = cn.sum()
        out += [int((m > 0).sum()), cn[m > 0].sum() / t, cn[(m <= 0) & (m > -NEAR)].sum() / t, cn[m <= -NEAR].sum() / t]
    cp = np.bincount(inv[C], weights=B["pop"][idx][C], minlength=len(U))
    out.append(int((cp >= 0.02 * cp.sum()).sum()))
    return out


def run(region, variant, chain, steps):
    from gerrychain import MarkovChain, Partition
    from gerrychain.accept import always_accept
    from gerrychain.constraints import contiguous, within_percent_of_ideal_population
    from gerrychain.proposals import recom
    from gerrychain.tree import recursive_tree_part
    from gerrychain.updaters import Tally

    S = setup(region)
    salt = f"regional_{region.replace(' ', '_')}_{variant}_{chain}"
    seed = get_canonical_seed(salt)
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
    surcharge = {"csduid": MUNI_W} if variant == "muni" else None
    assignment = recursive_tree_part(g, range(k), total / k, "pop_rs", EPS / 2, node_repeats=2)
    part = Partition(g, assignment, updaters={"population": Tally("pop_rs", alias="population")})
    ideal = total / k
    prop = partial(recom, pop_col="pop_rs", pop_target=ideal, epsilon=EPS, node_repeats=2, region_surcharge=surcharge)
    ch = MarkovChain(prop, constraints=[contiguous, within_percent_of_ideal_population(part, EPS)],
                     accept=always_accept, initial_state=part, total_steps=steps + BURN)
    rows = []
    for i, p in enumerate(ch):
        if i >= BURN:
            rows.append(measures(S, p.assignment))
    OUT.mkdir(exist_ok=True)
    stem = f"{region.replace(' ', '_')}_{variant}_{chain}"
    pd.DataFrame(rows, columns=COLS).to_csv(OUT / f"{stem}.csv", index=False)
    (OUT / f"{stem}.json").write_text(json.dumps({"region": region, "variant": variant, "chain": chain, "seed_salt": salt, "seed": seed,
                                                   "steps_kept": steps, "burn_in": BURN, "districts": k, "n_vas": len(S["nodes"]),
                                                   "muni_weight": MUNI_W if surcharge else 0}, indent=1))
    print(f"[{stem}] done", flush=True)


def jobs():
    regions = json.loads((HERE / "regions.json").read_text())
    js = [("Lethbridge", "muni", c, 50000) for c in (1, 2, 3, 4)]
    for r in regions:
        if r == "Lethbridge":
            continue
        for v in ("blind", "muni"):
            js += [(r, v, c, 25000) for c in (1, 2)]
    return js


def worker(w, nw):
    for i, (r, v, c, s) in enumerate(jobs()):
        if i % nw == w and not (OUT / f"{r.replace(' ', '_')}_{v}_{c}.csv").exists():
            print(f"[worker {w}] start {r} {v} {c}", flush=True)
            run(r, v, c, s)


def summarize():
    regions = json.loads((HERE / "regions.json").read_text())
    out = {"plan": "preregistration/hybrid_regions_2026-11-07.md", "primary_ballots": "all", "regions": {}}
    south_blind = ROOT / "findings/six_signals/regional_south"
    for r in regions:
        S = setup(r)
        real = {"panel": dict(zip(COLS, measures(S, {n: S["B"]["panel"][n] for n in S["nodes"]})))}
        if S["maj_closed"]:
            real["majority"] = dict(zip(COLS, measures(S, {n: S["B"]["majority"][n] for n in S["nodes"]})))
        block = {"districts": S["R"]["districts"], "hybrids": S["R"].get("hybrids"), "n_vas": len(S["nodes"]), "majority_closed": S["maj_closed"], "variants": {}}
        for v in ("blind", "muni"):
            files = sorted(OUT.glob(f"{r.replace(' ', '_')}_{v}_*.csv"))
            if r == "Lethbridge" and v == "blind":
                d = pd.concat([pd.read_csv(f) for f in sorted(south_blind.glob("chain*.csv"))]).rename(columns={
                    "ndp_seats_all": "ndp_seats_all", "leth_won_all": "city_won_all", "leth_near_all": "city_near_all", "leth_far_all": "city_far_all",
                    "leth_pieces": "city_pieces"})
            elif files:
                d = pd.concat([pd.read_csv(f) for f in files])
            else:
                continue
            vb = {"n_plans": int(len(d))}
            for c in ("ndp_seats_all", "city_won_all", "city_near_all", "city_far_all", "city_pieces"):
                x = d[c].to_numpy(float)
                row = {"q05": round(float(np.quantile(x, 0.05)), 3), "q50": round(float(np.quantile(x, 0.5)), 3), "q95": round(float(np.quantile(x, 0.95)), 3)}
                for k, rr in real.items():
                    val = float(rr[c])
                    row[k] = {"value": round(val, 3), "pct": round(100 * float((x < val).mean() + 0.5 * (x == val).mean()), 2)}
                vb[c] = row
            vb["unusual"] = {k: bool(vb["city_far_all"][k]["pct"] > 95 or vb["city_far_all"][k]["pct"] < 5) for k in real}
            if files:
                vb["chain_medians_city_far_all"] = [round(float(pd.read_csv(f).city_far_all.median()), 3) for f in files]
            block["variants"][v] = vb
        out["regions"][r] = block
    (HERE / "summary.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    for r, b in out["regions"].items():
        for v, vb in b["variants"].items():
            f = vb["city_far_all"]
            pz = vb["city_pieces"]
            print(f"{r:20s} {v:5s} n={vb['n_plans']:6d} far q50 {f['q50']:.2f} panel {f['panel']['value']:.2f} (p{f['panel']['pct']})"
                  + (f" maj {f['majority']['value']:.2f} (p{f['majority']['pct']})" if 'majority' in f else "")
                  + f" | pieces q50 {pz['q50']} panel {pz['panel']['value']} (p{pz['panel']['pct']}) | unusual {vb['unusual']}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "regions":
        print(json.dumps(define_regions(), indent=1))
    elif cmd == "worker":
        base()
        worker(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "run":
        run(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    else:
        summarize()
