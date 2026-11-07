"""w05: size_matched_results on all-ballots chains (Amendment 12). Rehearsal, provisional, not a registered result.

Overrides SETS suffixes and calls the module's own load/summarize/render for k = 91 only. main() cannot be called as filed:
it always places the 89-district commission maps, which needs an 89-district set, and no all-ballots 89-district set D exists.
Chain whitelists: set A is chains 201, 221-224 as filed (chain201 is in the repo's data/simulation_checkpoints_k91, 47,500 rows).
Sets with unequal chains are cut to their common length and labelled partial. Set D and set A use full chains."""
import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _a12  # noqa: E402
import size_matched_results as sm  # noqa: E402

SUFFIX = {"A": "_allballots", "B": "_eps25_allballots", "C": "_muni_allballots", "D": "_s152a23_allballots"}
WHITELIST = {"A": {201, 221, 222, 223, 224}, "B": {230, 231, 232, 233}, "C": None, "D": {251, 252, 253, 254}}
sm.SETS = {k: (SUFFIX[k], v[1]) for k, v in sm.SETS.items()}

ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--real", required=True)
ap.add_argument("--candidate", nargs="+", required=True)
ap.add_argument("--out-json", required=True)
ap.add_argument("--out-md", required=True)
ap.add_argument("--sets", nargs="+", default=["D", "A", "B", "C"])
a = ap.parse_args()

# Sets A and B are usable only over rows w00 replay-checked (set D is checked in findings/allballots_ranking).
_rc = _a12.OUT / "replay_check_AB.json"
REPLAY = json.loads(_rc.read_text()) if _rc.exists() else {}
REPLAY_SETS = {"A", "B"}

real = json.loads(Path(a.real).read_text())
cand = {m: real[m] for m in a.candidate}
res, notes = {}, {}
for key in a.sets:
    suffix, label = sm.SETS[key]
    d = Path(a.root) / "data" / f"simulation_checkpoints_k91{suffix}"
    files = {int(re.search(r"chain(\d+)_", f.name).group(1)): f for f in sorted(d.glob("chain*_samples.csv"))} if d.exists() else {}
    files = {i: f for i, f in files.items() if WHITELIST[key] is None or i in WHITELIST[key]}
    if not files:
        notes[key] = f"blocked: no chains in {d}"
        print(key, notes[key])
        continue
    cols = set(sm.REGISTERED) | set(sm.REPORTED)
    chains = {i: pd.read_csv(f, usecols=lambda c: c in cols) for i, f in files.items()}
    read = {i: len(df) for i, df in chains.items()}
    lens = dict(read)
    verified = True
    dropped = []
    if key in REPLAY_SETS:
        for i in chains:
            r = REPLAY.get(f"{key}{i}")
            if not r or not r.get("all_equal"):
                verified = False
                lens[i] = 0
                dropped.append(i)
            else:
                lens[i] = min(lens[i], int(r["rows_compared"]))
    elif WHITELIST[key] is None:
        verified = False  # no replay check exists for this set
    # A chain whose replay check is missing or failed is DROPPED (never used); the set is then PARTIAL.
    chains = {i: df for i, df in chains.items() if lens[i] > 0}
    lens = {i: lens[i] for i in chains}
    if not chains:
        notes[key] = f"blocked: replay check missing or failed for {sorted(dropped)}"
        print(key, notes[key])
        continue
    n = min(lens.values())
    complete = (verified and all(lens[i] == 252500 for i in chains)
                and WHITELIST[key] is not None and len(chains) == len(WHITELIST[key]))
    chains = {i: df.iloc[:n] for i, df in chains.items()}
    notes[key] = {"chains": sorted(chains), "rows_each_read": read, "rows_usable_each": lens, "rows_used_each": n,
                  "complete": bool(complete), "dropped_replay_failed_or_missing": sorted(dropped), "label": "complete" if complete else "PARTIAL"}
    res[f"{key}_k91"] = {"set": key, "label": label + ("" if complete else " [PARTIAL: chains incomplete or not fully replay-checked, cut to common checked length]"),
                         "k": 91, "chains": sorted(chains), "placed": list(cand),
                         "measures": sm.summarize(chains, cand), "completeness": notes[key]}
    print(key, notes[key], flush=True)
Path(a.out_json).write_text(json.dumps({"results": res, "notes": notes, "va_file_sha256": _a12.VA_ALL_SHA}, indent=1), encoding="utf-8")
Path(a.out_md).write_text("> Rehearsal on the reconstructed map, provisional, not a registered result. All-ballots chains.\n\n" + sm.render(res), encoding="utf-8")
