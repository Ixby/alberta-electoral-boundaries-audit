"""Rescore the redraw-test null (R1 and R2, Amendments 8 and 13) under rule P (exploratory, not registered).

The territory null's plans are stored in this repository (findings/a10_stepc/territory/chain*_plans.npy,
SHA-256 in plans_sha256.txt). They were drawn from population alone, so the same plans hold under any vote
file (Amendment 13, Part 1). This script:
  1. checks each plan file's SHA-256 against plans_sha256.txt;
  2. extracts the pinned scoring code (territory_score.py, territory_null.py, mcmc_ensemble.py at commit
     569250cd, the code the all-ballots rehearsal used, findings/amendment12_rehearsal/w07) from git into a
     temporary folder, with data/ linked read-only to this checkout;
  3. scores every plan and the map the null was built for (data/shapefiles/iap_assembled/iap_2026_assembled.gpkg,
     the provisional panel reconstruction, stated_low = 2) on the registered M0 file, and checks the result
     equals the rehearsal's filed rank.json (findings/amendment12_rehearsal/territory_allballots/rank.json);
  4. does the same on the P file (va_polygons_all_2023_ballots_p.gpkg) and reports each statistic's
     two-sided p-value, as the CLI's `rank` branch computes it (reference chains 1, 2, 4, 6; burn-in 10,000).

Seeds: the drain label-shuffle uses the pinned code's own fixed seed (shuffle_rng of the map's file stem).
Writes outputs/territory_null_p.json, outputs/territory_null_scores.csv
Usage: python findings/advance_vote_profile/09_rescore_territory_null.py
"""
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # works under python -I
from _common import M0_SHA256, ROOT, VA_M0, VA_P, rel, sha256, write_csv, write_json

PIN = "569250cd"
PLANS = ROOT / "findings/a10_stepc/territory"
FILED = ROOT / "findings/amendment12_rehearsal/territory_allballots/rank.json"
MAP = ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled.gpkg"
STATED_LOW, REF, BURN = 2, [1, 2, 4, 6], 10_000
STATS = ("eg", "drain", "mean_median", "declination", "ucp_seats")


def main():
    filed = {l.split()[1].lstrip("*"): l.split()[0] for l in (PLANS / "plans_sha256.txt").read_text().splitlines() if l.strip()}
    for name, h in filed.items():
        assert sha256(PLANS / name) == h, name
    assert sha256(VA_M0) == M0_SHA256
    tmp = Path(tempfile.mkdtemp(prefix="avp_territory_"))
    tar = subprocess.run(["git", "archive", PIN, "analysis"], cwd=ROOT, capture_output=True, check=True).stdout
    tarfile.open(fileobj=io.BytesIO(tar)).extractall(tmp, filter="data")
    (tmp / "data").symlink_to(ROOT / "data")
    sys.path.insert(0, str(tmp / "analysis/utils"))
    sys.path.insert(0, str(tmp / "analysis/scripts"))
    import mcmc_ensemble as me  # pinned copy
    _orig = me.build_va_graph
    import territory_score as ts  # pinned copy

    def run(va_file):
        me.build_va_graph = lambda verbose=True, va_path=None: _orig(verbose=verbose, va_path=va_path if va_path is not None else va_file)
        S = ts.Substrate(str(MAP), STATED_LOW)
        rows = []
        for f in sorted(PLANS.glob("chain*_plans.npy")):
            idx = int(f.stem.split("_")[0][5:])
            meta = json.loads(f.with_suffix(".json").read_text())
            for k, plan in enumerate(np.load(f)):
                r = S.score(S.plan_labels(plan))
                r.update(chain=idx, step=meta["plan_step"][k], s152=meta["s152_districts"][k])
                rows.append(r)
        df = pd.DataFrame(rows)
        lab, _ = S.map_labels(str(MAP))
        obs = S.score(lab, 10_000, ts.shuffle_rng(MAP.stem))
        ref = df[(df.step > BURN) & df.chain.isin(REF)]
        out = {"observed": obs, "n_ref_plans": int(len(ref)), "territory_districts": int(S.k_terr), "fixed_districts": int(S.n_fixed)}
        for v in STATS:
            r = ref[v].to_numpy()
            out[v] = {"observed": obs[v], "p_two_sided": float(min(1, 2 * min(np.mean(r <= obs[v]), np.mean(r >= obs[v])))),
                      "null_mean": float(r.mean()), "null_p025": float(np.quantile(r, .025)), "null_p975": float(np.quantile(r, .975)),
                      "percentile_midrank": float(100 * (np.mean(r < obs[v]) + 0.5 * np.mean(r == obs[v])))}
        return out, df

    m0, df0 = run(VA_M0)
    ref_filed = json.loads(FILED.read_text())
    diffs = {v: abs(m0[v]["p_two_sided"] - ref_filed[v]["p_two_sided"]) for v in STATS}
    obs_diff = max(abs(m0["observed"][v] - ref_filed["observed"][v]) for v in ("eg", "mean_median", "declination", "drain"))
    reproduced = max(diffs.values()) < 1e-12 and obs_diff < 1e-12 and m0["observed"]["ucp_seats"] == ref_filed["observed"]["ucp_seats"]
    print("M0 rescore reproduces the filed all-ballots rank.json:", reproduced, diffs, obs_diff, flush=True)
    p, dfp = run(VA_P)
    keep = ["chain", "step", "s152", "eg", "mean_median", "declination", "ucp_seats", "drain"]
    sc = df0[keep].merge(dfp[keep], on=["chain", "step", "s152"], suffixes=("_m0", "_p"), validate="one_to_one")
    sc["in_reference_set"] = (sc.step > BURN) & sc.chain.isin(REF)
    write_csv(sc, "territory_null_scores.csv")
    res = {"what": "Amendment 8 redraw-test null (R1 swing zone uses eg; R2 drain), rescored on M0 and P",
           "map": rel(MAP), "stated_low": STATED_LOW, "reference_chains": REF, "burn_in_steps": BURN, "pinned_code_commit": PIN,
           "plan_files_sha256_match": True, "plans_scored": int(len(sc)),
           "m0_reproduces_filed_rank_json": bool(reproduced), "m0": m0, "p": p,
           "vote_files": {"m0": {"path": rel(VA_M0), "sha256": M0_SHA256}, "p": {"path": rel(VA_P), "sha256": sha256(VA_P)}}}
    tag = f"a8-drain-label-shuffle-{MAP.stem}"
    seed_int = int.from_bytes(hashlib.sha256((ts.tn.RANDOMNESS + tag).encode()).digest()[:4], "big")
    seed = {"value": seed_int, "derivation": f"int(sha256(RANDOMNESS + \"{tag}\")[:4], big-endian), pinned territory_score.shuffle_rng at {PIN}",
            "used_for": "drain label-shuffle of the observed map"}
    write_json("territory_null_p.json", res, __file__, [VA_M0, VA_P, MAP, FILED, PLANS / "plans_sha256.txt"] + sorted(PLANS.glob("chain*_plans.npy")),
               seed=seed)
    print(json.dumps({k: {v: res[k][v]["p_two_sided"] for v in STATS} for k in ("m0", "p")}, indent=1))
    print("observed P:", p["observed"])
    (tmp / "data").unlink()
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
