# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
replay_queue.py

Amendment 12, Part 2: replays size-matched sets A, B and C from their registered seeds on the
all-ballots substrate, one chain at a time per worker, then checks each replay against its original
(every vote-independent column equal, row for row). Workers claim jobs with an exclusive claim file,
so any number can run. Chains are run by alberta_audit's close_seats_ensemble.py, unchanged.

Usage: python findings/amendment12_replays/replay_queue.py worker      (run detached, one per slot)
       python findings/amendment12_replays/replay_queue.py check
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
WT = HERE.parents[1]
AUDIT = WT.parent / "alberta_audit"
PY = Path(sys.executable).with_name("python.exe")
AB = WT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
SETS = {  # set: (k, original dir, root holding it, kernel flags, chain idx and steps)
    "A91": (91, "simulation_checkpoints_k91", AUDIT, [], {221: 252500, 222: 252500, 223: 252500, 224: 252500}),
    "A91_early": (91, "simulation_checkpoints_k91", WT, [], {201: 47500}),
    "A89": (89, "simulation_checkpoints_k89", AUDIT, [], {120: 252500, 121: 252500}),
    "A89_early": (89, "simulation_checkpoints_k89", WT, [], {100: 36500}),
    "B91": (91, "simulation_checkpoints_k91_eps25", AUDIT, ["--proposal-eps", "0.25"], {i: 252500 for i in (230, 231, 232, 233, 236, 237, 238, 239)}),
    "B89": (89, "simulation_checkpoints_k89_eps25", AUDIT, ["--proposal-eps", "0.25"], {i: 252500 for i in (130, 131, 132, 133)}),
    "C91": (91, "simulation_checkpoints_k91_muni", AUDIT, ["--proposal-eps", "0.25", "--muni-surcharge", "0.5"], {i: 252500 for i in (241, 243, 244, 245)}),
    "C89": (89, "simulation_checkpoints_k89_muni", AUDIT, ["--proposal-eps", "0.25", "--muni-surcharge", "0.5"], {i: 252500 for i in (140, 141)}),
}
VOTE_FREE = ["step", "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030", "n_districts", "n_parts",
             "n_city_districts", "towns_flagged", "city_gap_pct"]
CLAIMS = HERE / "claims"


def jobs():
    for s, (k, d, root, flags, chains) in SETS.items():
        for idx, steps in chains.items():
            out = AUDIT / "data" / f"{d}_allballots" / f"chain{idx}_samples.csv"
            yield s, k, idx, steps, flags, out, root / "data" / d / f"chain{idx}_samples.csv"


def worker():
    CLAIMS.mkdir(exist_ok=True)
    for s, k, idx, steps, flags, out, _ in jobs():
        try:
            fd = os.open(CLAIMS / f"{s}_{idx}.claim", os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
        except FileExistsError:
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [str(PY), "-I", "-W", "ignore", str(AUDIT / "analysis/scripts/close_seats_ensemble.py"), "nk", "--k", str(k), "--idx", str(idx),
               "--steps", str(steps), "--chunk", "500", *flags, "--va-file", str(AB), "--out", str(out)]
        print(f"[queue] start {s} {idx}: {' '.join(cmd[3:])}", flush=True)
        with open(out.with_suffix(".log"), "w", encoding="utf-8") as log:
            rc = subprocess.call(cmd, cwd=str(AUDIT), stdout=log, stderr=subprocess.STDOUT, creationflags=0x08000000)
        print(f"[queue] done {s} {idx} rc={rc}", flush=True)


def check():
    out = {}
    for s, k, idx, steps, flags, new, orig in jobs():
        key = f"{s}_{idx}"
        if not new.exists():
            out[key] = "not run"
            continue
        a = pd.read_csv(new, usecols=lambda c: c in VOTE_FREE)
        b = pd.read_csv(orig, usecols=lambda c: c in VOTE_FREE)
        cols = [c for c in VOTE_FREE if c in a and c in b]
        same = len(a) == len(b) and all(np.array_equal(a[c].values, b[c].values) for c in cols)
        out[key] = {"rows": [len(a), len(b)], "columns_compared": cols, "replay_matches": bool(same)}
    (HERE / "replay_check.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    print(json.dumps(out, indent=0))


if __name__ == "__main__":
    worker() if sys.argv[1] == "worker" else check()
