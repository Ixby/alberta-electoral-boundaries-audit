# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
lethbridge_at_w.py

preregistration/city_weight_calibration_2026-11-07.md, "Use": rerun the Lethbridge regional city-aware
redraw (findings/hybrid_regions/regional_redraw.py, same region, chains, seeds and reading rule) at the
lowest and highest city-boundary weight implied by the commission-drawn maps (implied_w.json,
commission_range). Only the weight changes: the seed salts are the original regional_Lethbridge_muni_{1..4},
so each chain differs from the W = 0.5 chain of the same number only in W. Unregistered.

Usage: python -W ignore findings/city_weight/lethbridge_at_w.py worker W NW
       python -W ignore findings/city_weight/lethbridge_at_w.py summarize
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "findings/hybrid_regions"))
import regional_redraw as RR  # noqa: E402

RANGE = json.loads((HERE / "implied_w.json").read_text())["commission_range"]
WS = (RANGE["min"], RANGE["max"])
STEPS, CHAINS = 50000, (1, 2, 3, 4)


def out_dir(w):
    return HERE / f"lethbridge_W{w:.3f}"


def jobs():
    return [(w, c) for w in WS for c in CHAINS]


def worker(i, n):
    for j, (w, c) in enumerate(jobs()):
        if j % n != i or (out_dir(w) / f"Lethbridge_muni_{c}.csv").exists():
            continue
        RR.MUNI_W, RR.OUT = w, out_dir(w)
        print(f"[worker {i}] start W={w} chain {c}", flush=True)
        RR.run("Lethbridge", "muni", c, STEPS)


def summarize():
    S = RR.setup("Lethbridge")
    real = {"panel": dict(zip(RR.COLS, RR.measures(S, {n: S["B"]["panel"][n] for n in S["nodes"]})))}
    if S["maj_closed"]:
        real["majority"] = dict(zip(RR.COLS, RR.measures(S, {n: S["B"]["majority"][n] for n in S["nodes"]})))
    res = {"plan": "preregistration/city_weight_calibration_2026-11-07.md", "commission_range": RANGE, "weights": {}}
    for w in (WS[0], 0.5, WS[1]):
        d_ = out_dir(w) if w != 0.5 else RR.HERE / "chains"
        files = sorted(d_.glob("Lethbridge_muni_*.csv"))
        if len(files) != len(CHAINS):
            res["weights"][str(w)] = f"incomplete: {len(files)} of {len(CHAINS)} chains"
            continue
        d = pd.concat([pd.read_csv(f) for f in files])
        vb = {"n_plans": int(len(d)), "source": str(d_.relative_to(ROOT))}
        for c in ("ndp_seats_all", "city_won_all", "city_near_all", "city_far_all", "city_pieces"):
            x = d[c].to_numpy(float)
            row = {"q05": round(float(np.quantile(x, 0.05)), 3), "q50": round(float(np.quantile(x, 0.5)), 3), "q95": round(float(np.quantile(x, 0.95)), 3)}
            for k, rr in real.items():
                val = float(rr[c])
                tie = np.isclose(x, val, rtol=0, atol=1e-9)
                row[k] = {"value": round(val, 3), "pct": round(100 * float((x < val - 1e-9).mean() + 0.5 * tie.mean()), 2)}
            vb[c] = row
        vb["pieces_share"] = {int(p): round(float((d.city_pieces == p).mean()), 4) for p in sorted(d.city_pieces.unique())}
        vb["unusual"] = {k: bool(vb["city_far_all"][k]["pct"] > 95 or vb["city_far_all"][k]["pct"] < 5) for k in real}
        vb["chain_medians_city_far_all"] = [round(float(pd.read_csv(f).city_far_all.median()), 3) for f in files]
        res["weights"][str(w)] = vb
    (HERE / "lethbridge_at_w.json").write_text(json.dumps(res, indent=1), encoding="utf8")
    for w, vb in res["weights"].items():
        if isinstance(vb, str):
            print(w, vb)
            continue
        print(f"W={w}: far panel {vb['city_far_all']['panel']} pieces panel {vb['city_pieces']['panel']} shares {vb['pieces_share']} unusual {vb['unusual']}")


if __name__ == "__main__":
    if sys.argv[1] == "worker":
        RR.base()
        worker(int(sys.argv[2]), int(sys.argv[3]))
    else:
        summarize()
