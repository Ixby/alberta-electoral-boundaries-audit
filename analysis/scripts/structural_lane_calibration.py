# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
structural_lane_calibration.py
------------------------------

How often the November spec's two lanes fire on neutral maps. Calibration
only; it changes no registered rule (Amendment 5, Part 14 keeps the 2x2
verdict).

Neutral maps, sampled with close_seats_ensemble.py at
amendment17-local-runs@2994113c, 10,000 burn-in steps, then one plan every
2,500 steps:
  91 districts  set D (s.15(2), Amendment 5, Part 15 rule), chains 290-293,
                production set-D options
  87 districts  canonical kernel, chains 300-303 (run on the PC)
The script scores whatever plans --plans holds; label each run's output by
the chains that made it.

  structural  run_structural_battery.py on each plan, exactly as registered,
              with the plan's districts dissolved from the VA polygons. S6 is
              name-based (it reads district names such as "Airdrie" or
              "Cochrane" + "Calgary"), so it cannot fire on unnamed plans; the
              registered count is therefore a lower bound. A geometric stand-in
              for S6 is reported beside it: P1 Airdrie and P5 Red Deer split into
              3 or more districts (a district counts when it holds >= 2% of the
              city's people); P2-P4 a district with >= 10% of its people in each
              of Calgary and Cochrane / Chestermere / Rocky View County. The 10%
              cut is this script's choice, not the registered rule.
  partisan    P1-P4 against the 87-district canonical ensemble, from each plan's
              chain row, as spec section 3 sets them (UCP direction).

Usage
  python analysis/scripts/structural_lane_calibration.py --plans DIR --out-json PATH --out-md PATH [--jobs 4]
  python analysis/scripts/structural_lane_calibration.py --check-s6   (geometric S6 on the real maps)
"""
import argparse
import json
import math
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

CSD = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"
PARTISAN = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
P1_EG, PCT = 0.0410, 0.95


def va_frame():
    import geopandas as gpd
    import mcmc_ensemble as me

    va, graph = me.build_va_graph(verbose=False)
    nodes = sorted(graph.nodes())
    va = va.loc[nodes, ["geometry"]].copy()
    va["pop"] = [graph.nodes[n]["pop_2021"] for n in nodes]
    pts = va.copy()
    pts["geometry"] = va.geometry.representative_point()
    csd = gpd.read_file(CSD).to_crs(va.crs)
    j = gpd.sjoin(pts[["geometry"]], csd[["CSDNAME", "geometry"]], how="left", predicate="within")
    va["csd"] = j[~j.index.duplicated(keep="first")].reindex(va.index)["CSDNAME"].fillna("")
    return va


def s6_geometric(labels, va):
    df = pd.DataFrame({"d": np.asarray(labels), "pop": va["pop"].to_numpy(), "csd": va["csd"].to_numpy()})
    tot = df.groupby("d")["pop"].sum()
    by = df.groupby(["d", "csd"])["pop"].sum().unstack(fill_value=0.0)

    def pieces(city):
        if city not in by:
            return 0
        c = by[city]
        return int((c >= 0.02 * c.sum()).sum())

    def hybrid(a, b):
        if a not in by or b not in by:
            return False
        return bool(((by[a] / tot >= 0.10) & (by[b] / tot >= 0.10)).any())

    hits = {"P1_Airdrie_3plus": pieces("Airdrie") >= 3,
            "P2_Cochrane_Calgary": hybrid("Cochrane", "Calgary"),
            "P3_Chestermere_Calgary": hybrid("Chestermere", "Calgary"),
            "P4_RockyView_Calgary": hybrid("Rocky View County", "Calgary"),
            "P5_RedDeer_3plus": pieces("Red Deer") >= 3}
    n = sum(hits.values())
    return {"hits": [k for k, v in hits.items() if v], "count": n, "flag": n >= 3}


def write_plan_gpkg(assign, va, path):
    lab = pd.Series({int(k): int(v) for k, v in assign.items()}).reindex(va.index)
    g = va[["geometry"]].assign(d=lab.to_numpy()).dissolve(by="d").reset_index()
    g["EDName2025"] = [f"N{int(d) + 1:02d}" for d in g["d"]]
    g[["EDName2025", "geometry"]].to_file(path, driver="GPKG")
    return lab.to_numpy()


def run_battery(args):
    gpkg, out = args
    r = subprocess.run([sys.executable, str(REPO / "analysis/scripts/run_structural_battery.py"),
                        "--shapefile", str(gpkg), "--output", str(out), "--label", Path(gpkg).stem],
                       capture_output=True, text=True)
    return out, r.returncode, r.stderr[-500:]


def canonical_sorted():
    can = pd.concat([pd.read_csv(REPO / f"data/simulation_checkpoints_canonical/chain{i}_samples.csv", usecols=PARTISAN)
                     for i in range(4)])
    return {c: np.sort(can[c].to_numpy()) for c in PARTISAN}


def partisan_flags(row, srt):
    def pct(c):
        return np.searchsorted(srt[c], row[c], side="right") / len(srt[c])
    f = {"P1_EG": bool(row["efficiency_gap"] >= P1_EG), "P2_MM": bool(pct("mean_median") >= PCT),
         "P3_DECL": bool(pct("declination") >= PCT), "P4_S50": bool(pct("seats_at_50_50") >= PCT)}
    return f, sum(f.values()) >= 2


def check_s6():
    import geopandas as gpd
    va = va_frame()
    pts = va[["geometry"]].copy()
    pts["geometry"] = va.geometry.representative_point()
    for name in ("majority", "minority"):
        g = gpd.read_file(REPO / f"data/shapefiles/canonical/ea_{name}_2026_eds.gpkg").to_crs(va.crs)
        j = gpd.sjoin(pts, g[["EDName2025", "geometry"]], how="left", predicate="within")
        lab = j[~j.index.duplicated(keep="first")].reindex(va.index)["EDName2025"].fillna("__unassigned__").to_numpy()
        print(name, s6_geometric(lab, va))


def main(a):
    plans = sorted(Path(a.plans).glob("plan_*.json"))
    work = Path(a.plans) / "scored"
    work.mkdir(exist_ok=True)
    va = va_frame()
    srt = canonical_sorted()
    chains = {}
    jobs, meta = [], {}
    for p in plans:
        idx, done = map(int, re.match(r"plan_(\d+)_(\d+)\.json", p.name).groups())
        if idx not in chains:
            chains[idx] = pd.read_csv(Path(a.plans) / f"chain{idx}.csv", usecols=PARTISAN)
        gpkg = work / f"{p.stem}.gpkg"
        labels = write_plan_gpkg(json.loads(p.read_text(encoding="utf-8")), va, gpkg)
        pf, present = partisan_flags(chains[idx].iloc[done - 1], srt)
        meta[p.stem] = {"chain": idx, "step": done, "s6_geometric": s6_geometric(labels, va),
                        "partisan_flags": pf, "partisan_present": present}
        out = work / f"{p.stem}_battery.json"
        if not out.exists():
            jobs.append((gpkg, out))
    with ProcessPoolExecutor(a.jobs) as ex:
        for out, rc, err in ex.map(run_battery, jobs):
            if rc:
                print(f"battery failed: {out.name}: {err}", flush=True)
    rows = []
    for stem, m in meta.items():
        b = json.loads((work / f"{stem}_battery.json").read_text(encoding="utf-8"))
        met = b["metrics"]
        flags = {k: bool(v.get("flag")) for k, v in met.items()}
        reg = sum(flags.get(k, False) for k in ("S1_population_mad", "S2_municipal_split_count",
                                                "S3_anchoring_score", "S5_drain_score", "S6_chair_flag_replication"))
        geo = reg - flags.get("S6_chair_flag_replication", False) + m["s6_geometric"]["flag"]
        rows.append({"plan": stem, **m, "structural_flags": flags, "structural_registered": reg,
                     "structural_registered_replicated": reg >= 3, "structural_with_geometric_s6": geo,
                     "structural_geometric_replicated": geo >= 3})
    df = pd.DataFrame(rows)
    n = len(df)

    def rate(s):
        k = int(s.sum())
        lo, hi = wilson(k, n)
        return {"k": k, "n": n, "rate": k / n, "wilson95": [lo, hi]}

    flag_rates = {f: rate(df["structural_flags"].apply(lambda x: x.get(f, False))) for f in
                  ("S1_population_mad", "S2_municipal_split_count", "S3_anchoring_score", "S4_polsby_popper_median",
                   "S5_drain_score", "S6_chair_flag_replication")}
    flag_rates["S6_geometric_stand_in"] = rate(df["s6_geometric"].apply(lambda x: x["flag"]))
    res = {"n_plans": n, "chains": sorted(df["chain"].unique().tolist()), "flag_rates": flag_rates,
           "structural_replicated_registered": rate(df["structural_registered_replicated"]),
           "structural_replicated_geometric_s6": rate(df["structural_geometric_replicated"]),
           "partisan_present": rate(df["partisan_present"]),
           "both_lanes_registered": rate(df["structural_registered_replicated"] & df["partisan_present"]),
           "both_lanes_geometric_s6": rate(df["structural_geometric_replicated"] & df["partisan_present"]),
           "plans": rows}
    Path(a.out_json).write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    Path(a.out_md).write_text(render(res), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "plans"}, indent=1, default=str))


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def render(res):
    def r(x):
        return f"{100 * x['rate']:.1f}% ({x['k']} of {x['n']}; 95% interval {100 * x['wilson95'][0]:.1f}–{100 * x['wilson95'][1]:.1f}%)"
    lines = ["| Measure | Neutral plans that fire |", "|---|---|"]
    for f, v in res["flag_rates"].items():
        lines.append(f"| {f} | {r(v)} |")
    lines += ["", "| Lane | Neutral plans |", "|---|---|",
              f"| Structural lane replicated (registered battery; S6 cannot fire) | {r(res['structural_replicated_registered'])} |",
              f"| Structural lane replicated (geometric S6 stand-in) | {r(res['structural_replicated_geometric_s6'])} |",
              f"| Partisan lane present | {r(res['partisan_present'])} |",
              f"| Both lanes (registered) | {r(res['both_lanes_registered'])} |",
              f"| Both lanes (geometric S6 stand-in) | {r(res['both_lanes_geometric_s6'])} |", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans")
    ap.add_argument("--out-json")
    ap.add_argument("--out-md")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--check-s6", action="store_true")
    a = ap.parse_args()
    if a.check_s6:
        check_s6()
    else:
        main(a)
