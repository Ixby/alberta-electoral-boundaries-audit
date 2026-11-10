"""Replay the ensembles on the P vote file, check the replays, and rank every real map (exploratory, not registered).

The ensembles' plans are not stored; only per-plan scores are. A plan can be rebuilt only by rerunning its
chain from its registered seed. ReCom reads population, not votes, so a replay on the P file draws the
same plans, and a replay counts only if every vote-independent column equals the original row for row
(Amendment 12, Part 2; Amendment 13). See REPLAY.md for where each chain must run and why.

Subcommands
  commands               print the exact command for every chain (canonical, set D, sets A-C, forest)
  forest                 run the Forest-ReCom Phase A chains on the P file, writing to
                         data/simulation_checkpoints_forest_recom_phaseA_allballots_p/ (the script's own
                         output paths are redirected so no committed file is touched)
  check                  compare every replayed chain present with its election-day original and with its M0
                         replay where one exists; writes outputs/replay_check_p.json and exits non-zero,
                         naming the chain and column, if any replay is missing or differs in a vote-independent column
  rank                   rank each real map's P score against the replayed chains that passed;
                         writes outputs/ensemble_ranks_p.json

Usage (from the repository root of the machine that holds the chains):
  python findings/advance_vote_profile/10_replay_p.py commands
  python findings/advance_vote_profile/10_replay_p.py check --audit ../alberta_audit
  python findings/advance_vote_profile/10_replay_p.py rank  --audit ../alberta_audit
"""
import argparse
import contextlib
import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from _common import OUT, ROOT, VA_P, rel, sha256, write_json

P_REL = "data/shapefiles/derived/va_polygons_all_2023_ballots_p.gpkg"
VOTE_FREE = ["step", "population_mad", "reock_proxy_median", "reock_proxy_pct_below_030", "n_districts", "n_parts",
             "n_city_districts", "towns_flagged", "city_gap_pct", "s152_districts"]
STATS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50", "ucp_seats", "close4"]
# set: (districts, original dir, root key, flags, chains and steps). Root "repo" = this repository, "audit" = the alberta_audit clone.
SETS = {
    "canonical": (87, "simulation_checkpoints_canonical", "repo", None, {i: 252500 for i in range(4)}),
    "D91": (91, "simulation_checkpoints_k91_s152a23", "audit", ["--s152", "data/outputs/s15_2_va_criteria.csv"], {i: 252500 for i in (251, 252, 253, 254)}),
    "A91": (91, "simulation_checkpoints_k91", "audit", [], {i: 252500 for i in (221, 222, 223, 224)}),
    "A89": (89, "simulation_checkpoints_k89", "audit", [], {120: 252500, 121: 252500}),
    "B91": (91, "simulation_checkpoints_k91_eps25", "audit", ["--proposal-eps", "0.25"], {i: 252500 for i in (230, 231, 232, 233, 236, 237, 238, 239)}),
    "B89": (89, "simulation_checkpoints_k89_eps25", "audit", ["--proposal-eps", "0.25"], {i: 252500 for i in (130, 131, 132, 133)}),
    "C91": (91, "simulation_checkpoints_k91_muni", "audit", ["--proposal-eps", "0.25", "--muni-surcharge", "0.5"], {i: 252500 for i in (241, 243, 244, 245)}),
    "C89": (89, "simulation_checkpoints_k89_muni", "audit", ["--proposal-eps", "0.25", "--muni-surcharge", "0.5"], {i: 252500 for i in (140, 141)}),
    "forest": (87, "outputs/forest_recom_raw_samples_phaseA.csv", "repo", None, {i: 25000 for i in range(4)}),
}
MAPS_BY_K = {87: ["enacted_2019_87"], 89: ["majority_89", "minority_89"], 91: ["panel_v3_91", "para167_91"]}


def new_path(s, idx, roots):
    k, d, root, flags, _ = SETS[s]
    if s == "canonical":
        return roots["repo"] / "data/simulation_checkpoints_allballots_p" / f"chain{idx}_samples.csv"
    if s == "forest":
        return roots["repo"] / "data/simulation_checkpoints_forest_recom_phaseA_allballots_p" / f"chain{idx}_samples.csv"
    return roots["audit"] / "data" / f"{d}_allballots_p" / f"chain{idx}_samples.csv"


def orig_frame(s, idx, roots):
    k, d, root, flags, _ = SETS[s]
    if s == "forest":
        f = roots["repo"] / "data" / d
        df = pd.read_csv(f)
        return df[df.chain == idx].reset_index(drop=True), f
    f = roots[root] / "data" / d / f"chain{idx}_samples.csv"
    return pd.read_csv(f), f


def commands(roots):
    out = []
    for s, (k, d, root, flags, chains) in SETS.items():
        for idx, steps in chains.items():
            o = rel(new_path(s, idx, roots)) if s in ("canonical", "forest") else f"data/{d}_allballots_p/chain{idx}_samples.csv"
            if s == "canonical":
                if idx:
                    continue
                cmd = (f"python analysis/scripts/mcmc_ensemble_canonical.py --n-steps 1010000 --n-chains 4 --chunk-size 5000 "
                       f"--run-id allballots_p --va-file {P_REL} --max-workers 4   (in this repository; writes data/simulation_checkpoints_allballots_p/)")
            elif s == "forest":
                if idx:
                    continue
                cmd = "python findings/advance_vote_profile/10_replay_p.py forest   (in this repository)"
            else:
                cmd = (f"python -I -W ignore analysis/scripts/close_seats_ensemble.py nk --k {k} --idx {idx} --steps {steps} --chunk 500 "
                       f"{' '.join(flags)} --va-file <this repository>/{P_REL} --out {o}   (in the alberta_audit clone)").replace("  ", " ")
            out.append({"set": s, "chain": idx, "command": cmd})
    return out


def forest():
    sys.path.insert(0, str(ROOT / "analysis/scripts"))
    sys.path.insert(0, str(ROOT / "analysis/utils"))
    import forest_recom_ensemble as fr
    dst = ROOT / "data/simulation_checkpoints_forest_recom_phaseA_allballots_p"
    fr.CHECKPOINT_DIR = dst
    for name in ("SAMPLES_CSV", "SCORES_JSON", "PERCENTILES_CSV", "CONVERGENCE_JSON"):
        p = getattr(fr, name)
        setattr(fr, name, dst / Path(p).name)
    _orig = fr.build_va_graph
    fr.build_va_graph = lambda verbose=True, va_path=None: _orig(verbose=verbose, va_path=va_path if va_path is not None else VA_P)
    sys.argv = ["forest_recom_ensemble.py", "--confirm-osf-filed", "--osf-registration-id", "he53s", "--n-steps", "100000"]
    return fr.main()


def m0_path(s, idx, roots):
    """The all-ballots (M0) replay of the same chain, or None where no M0 replay was made (Forest-ReCom)."""
    k, d, root, flags, _ = SETS[s]
    if s == "canonical":
        return roots["repo"] / "data/simulation_checkpoints_allballots" / f"chain{idx}_samples.csv"
    if s == "forest":
        return None
    return roots["audit"] / "data" / f"{d}_allballots" / f"chain{idx}_samples.csv"


def compare(a, b, cols, steps):
    """Row counts and, column by column, the number of rows that differ. Columns missing from either file are named."""
    missing = [c for c in cols if c not in a or c not in b]
    present = [c for c in cols if c in a and c in b]
    same_len = len(a) == len(b)
    diff = {c: int((a[c].values != b[c].values).sum()) for c in present} if same_len else {}
    reasons = []
    if missing:
        reasons.append("missing columns: " + ", ".join(missing))
    if not (len(a) == len(b) == steps):
        reasons.append(f"rows {len(a)} and {len(b)}, expected {steps}")
    bad = [c for c, v in diff.items() if v]
    if bad:
        reasons.append("columns that differ: " + ", ".join(bad))
    return {"rows": [int(len(a)), int(len(b))], "missing_columns": missing, "rows_that_differ": diff, "ok": not reasons, "reasons": reasons}


def check(roots):
    res = []
    for s, (k, d, root, flags, chains) in SETS.items():
        for idx, steps in chains.items():
            f = new_path(s, idx, roots)
            if not f.exists():
                res.append({"set": s, "chain": idx, "status": "not run", "path": rel(f)})
                continue
            a = pd.read_csv(f)
            b, fb = orig_frame(s, idx, roots)
            cols = [c for c in VOTE_FREE if c in b]  # every vote-independent column the original has must be in the replay
            vs_orig = compare(a, b, cols, steps)
            row = {"set": s, "chain": idx, "columns_compared": cols, "rows": vs_orig["rows"], "missing_columns": vs_orig["missing_columns"],
                   "rows_that_differ": vs_orig["rows_that_differ"], "path": rel(f), "sha256": sha256(f), "original": rel(fb)}
            reasons = ["election-day original: " + r for r in vs_orig["reasons"]]
            fm = m0_path(s, idx, roots)
            if fm is None or not fm.exists():
                row["m0_replay"] = None if fm is None else rel(fm)
                row["m0_comparison"] = "no M0 replay of this chain" if fm is None else "M0 replay not found; compared with the original only"
            else:
                vs_m0 = compare(a, pd.read_csv(fm), cols, steps)
                row.update({"m0_replay": rel(fm), "rows_vs_m0": vs_m0["rows"], "missing_columns_vs_m0": vs_m0["missing_columns"],
                            "rows_that_differ_vs_m0": vs_m0["rows_that_differ"]})
                reasons += ["M0 replay: " + r for r in vs_m0["reasons"]]
            row["status"] = "fails" if reasons else "match"
            row["reasons"] = reasons
            res.append(row)
    write_json("replay_check_p.json", {"chains": res, "rule": ("a replay counts only if every vote-independent column the original has is present "
                                                               "and equals the election-day original, and the M0 replay where one exists, row for row")},
               __file__, [VA_P])
    print(json.dumps(res, indent=1))
    failed = [f"{r['set']} {r['chain']}: " + "; ".join(r["reasons"]) for r in res if r["status"] == "fails"]
    if failed:
        print("replay check failed:\n" + "\n".join(failed), file=sys.stderr)
        sys.exit(1)


def rank(roots):
    sys.path.insert(0, str(ROOT / "analysis/scripts"))
    with contextlib.redirect_stdout(io.StringIO()):
        import mcmc_ensemble as me
    chk = json.loads((OUT / "replay_check_p.json").read_text())["chains"]
    ok = {(c["set"], c["chain"]) for c in chk if c["status"] == "match"}
    real = pd.read_csv(OUT / "headline_table.csv")
    real = real[(real.rule == "p") & (real.beta == 1.0)].set_index("map")
    out = []
    for s, (k, d, root, flags, chains) in SETS.items():
        use = [i for i in chains if (s, i) in ok]
        if not use:
            out.append({"set": s, "status": "no replay passed its check; no percentile given"})
            continue
        df = pd.concat([pd.read_csv(new_path(s, i, roots)) for i in use], ignore_index=True)
        maps = [m for kk, ms in MAPS_BY_K.items() for m in ms] if k == 87 else MAPS_BY_K[k]  # 87-district sets rank every map, as canonical_ranking.json does
        rows = []
        for m in maps:
            r = real.loc[m]
            val = {"efficiency_gap": r.efficiency_gap_pct / 100, "mean_median": r.mean_median_pct / 100, "declination": r.declination,
                   "seats_at_50_50": r.ucp_seats_at_tied_vote / r.n_districts, "ucp_seats": r.ucp_seats, "close4": r.close_seats_4pts}
            for st in STATS:
                if st in df:
                    rows.append({"map": m, "statistic": st, "value_p": float(val[st]), "percentile": round(me.pct_rank(df[st].values, float(val[st])), 2),
                                 "ensemble_p50": float(np.nanpercentile(df[st], 50))})
        out.append({"set": s, "chains_used": use, "plans": int(len(df)), "ranks": rows,
                    "note": "seat counts of an 89- or 91-district map against an 87-district ensemble are partly a district-count effect" if k == 87 else ""})
    write_json("ensemble_ranks_p.json", {"sets": out}, __file__, [OUT / "replay_check_p.json", OUT / "headline_table.csv"])
    print(json.dumps(out, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["commands", "forest", "check", "rank"])
    ap.add_argument("--audit", default=str(ROOT.parent / "alberta_audit"), help="the alberta_audit clone that holds the size-matched chains")
    a = ap.parse_args()
    roots = {"repo": ROOT, "audit": Path(a.audit).resolve()}
    if a.cmd == "commands":
        for c in commands(roots):
            print(f"[{c['set']} {c['chain']}] {c['command']}")
    elif a.cmd == "forest":
        sys.exit(forest())
    elif a.cmd == "check":
        check(roots)
    else:
        rank(roots)


if __name__ == "__main__":
    main()
