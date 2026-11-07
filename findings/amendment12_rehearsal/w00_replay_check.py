"""w00: Amendment 12, Part 2 replay check for sets A and B (set D is checked in findings/allballots_ranking).
A replay counts only if every vote-independent column equals the original run, row for row, over the rows both have."""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _a12  # noqa: E402

AUD = _a12.ROOT.parent / "alberta_audit" / "data"
INDEP = ["step", "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030", "n_districts",
         "n_parts", "n_city_districts", "towns_flagged", "s152_districts"]
SETS = {"A": ("simulation_checkpoints_k91", "simulation_checkpoints_k91_allballots", [201, 221, 222, 223, 224]),
        "B": ("simulation_checkpoints_k91_eps25", "simulation_checkpoints_k91_eps25_allballots", [230, 231, 232, 233])}
res = {}
for key, (orig, new, chains) in SETS.items():
    for c in chains:
        fo, fn = AUD / orig / f"chain{c}_samples.csv", AUD / new / f"chain{c}_samples.csv"
        if not fo.exists():
            fo = _a12.ROOT / "data" / orig / f"chain{c}_samples.csv"  # chain201 is in the repo, not the clone
        ho, hn = set(pd.read_csv(fo, nrows=0).columns), set(pd.read_csv(fn, nrows=0).columns)
        cols = [x for x in INDEP if x in ho and x in hn]
        a, b = pd.read_csv(fo, usecols=cols), pd.read_csv(fn, usecols=cols)
        n_o, n_b = len(a), len(b)
        n = min(n_o, n_b)
        a, b = a.iloc[:n].reset_index(drop=True), b.iloc[:n].reset_index(drop=True)
        eq = {k: bool((a[k].values == b[k].values).all()) for k in cols}
        # default red: nothing compared is not a pass ("a command that cannot fail is a report, not a check")
        ok = bool(cols) and "step" in cols and n > 0 and all(eq.values())
        res[f"{key}{c}"] = {"rows_original": int(n_o), "rows_allballots": int(n_b), "rows_compared": int(n),
                            "columns": eq, "columns_missing": [x for x in INDEP if x not in cols], "all_equal": ok}
        print(key, c, n_b, "rows; compared", n, "missing", res[f"{key}{c}"]["columns_missing"], "all_equal", ok, flush=True)
(_a12.OUT / "replay_check_AB.json").write_text(json.dumps(res, indent=1))
bad = [k for k, v in res.items() if not v["all_equal"]]
if bad:
    sys.exit(f"replay check FAILED for {bad}")
