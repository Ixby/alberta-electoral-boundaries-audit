# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
sorted_vs_neutral.py

Part 2 of preregistration/packing_cracking_2026-11-07.md: each map's seats sorted by NDP two-party
share, position by position, against set D's neutral plans replayed with sorted shares
(alberta_audit/analysis/scripts/sorted_shares_replay.py). Unregistered. Describes, does not show intent.

Reads   findings/packing_cracking/real_maps.json
        ALBERTA_AUDIT/data/simulation_checkpoints_k91_s152a23_sorted[_allballots]/chain25[1-4]_samples.csv.sorted.f32
Writes  findings/packing_cracking/sorted_vs_neutral_<ballots>.json

Usage: python -W ignore findings/packing_cracking/sorted_vs_neutral.py election_day|all_ballots
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
AUDIT = ROOT.parent / "alberta_audit" / "data"
DIRS = {"election_day": "simulation_checkpoints_k91_s152a23_sorted", "all_ballots": "simulation_checkpoints_k91_s152a23_sorted_allballots"}
K = 91


def pct(v, x):
    return round(100 * float((v < x).mean() + 0.5 * (v == x).mean()), 2)


def main(ballots):
    recs = np.concatenate([np.fromfile(AUDIT / DIRS[ballots] / f"chain{i}_samples.csv.sorted.f32", dtype=np.float32).reshape(-1, 96)
                           for i in (251, 252, 253, 254)])
    sh = recs[:, 1:1 + K].astype(float)
    leth = recs[:, 1 + K:1 + K + 3].astype(float)
    leth = leth / leth.sum(axis=1, keepdims=True)
    q05, q50, q95 = (np.quantile(sh, q, axis=0) for q in (0.05, 0.5, 0.95))
    real = json.loads((HERE / "real_maps.json").read_text())[ballots]
    out = {"plan": "preregistration/packing_cracking_2026-11-07.md", "ballots": ballots, "n_plans": int(len(sh)),
           "neutral_band": {"q05": q05.round(4).tolist(), "q50": q50.round(4).tolist(), "q95": q95.round(4).tolist()}}
    n4050 = ((sh >= 0.40) & (sh < 0.50)).sum(axis=1)
    n30 = (sh < 0.30).sum(axis=1)
    nwin = (sh > 0.5).sum(axis=1)
    out["neutral_counts"] = {"seats_40_to_50": [float(np.quantile(n4050, q)) for q in (0.05, 0.5, 0.95)],
                             "seats_under_30": [float(np.quantile(n30, q)) for q in (0.05, 0.5, 0.95)],
                             "ndp_seats": [float(np.quantile(nwin, q)) for q in (0.05, 0.5, 0.95)]}
    for k in ("panel", "para167"):
        s = np.array(real[k]["sorted_ndp_share"])
        names = real[k]["sorted_names"]
        above = [i for i in range(K) if s[i] > q95[i]]
        below = [i for i in range(K) if s[i] < q05[i]]
        lr = real[k]["lethbridge"]
        out[k] = {"positions_above_q95": [{"rank": i + 1, "seat": names[i], "share": round(float(s[i]), 4), "q95": round(float(q95[i]), 4)} for i in above],
                  "positions_below_q05": [{"rank": i + 1, "seat": names[i], "share": round(float(s[i]), 4), "q05": round(float(q05[i]), 4)} for i in below],
                  "top_ndp_seats_packed": [names[i] for i in above if s[i] > 0.5],
                  "seats_40_to_50": {"value": int(((s >= 0.40) & (s < 0.50)).sum()), "pct": pct(n4050, ((s >= 0.40) & (s < 0.50)).sum())},
                  "seats_under_30": {"value": int((s < 0.30).sum()), "pct": pct(n30, (s < 0.30).sum())},
                  "ndp_seats": {"value": int((s > 0.5).sum()), "pct": pct(nwin, (s > 0.5).sum())},
                  "lethbridge_ndp_in_won_pct": pct(leth[:, 0], lr["in_ndp_won"] / 100),
                  "lethbridge_ndp_in_far_loss_pct": pct(leth[:, 2], lr["in_lost_far"] / 100)}
    out["neutral_lethbridge"] = {"won": [round(float(np.quantile(leth[:, 0], q)), 3) for q in (0.05, 0.5, 0.95)],
                                 "far_loss": [round(float(np.quantile(leth[:, 2], q)), 3) for q in (0.05, 0.5, 0.95)],
                                 "pieces": {int(v): round(float((recs[:, -1] == v).mean()), 3) for v in np.unique(recs[:, -1])}}
    (HERE / f"sorted_vs_neutral_{ballots}.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    print(json.dumps({k: v for k, v in out.items() if k != "neutral_band"}, indent=0)[:4000])


if __name__ == "__main__":
    main(sys.argv[1])
