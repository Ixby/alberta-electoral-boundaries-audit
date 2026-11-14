"""w07: R1/R2 on all ballots, by rescoring the FILED Step C territory plans (chains 1, 2, 4, 5, 6).
The plans are partitions of voting areas built from population alone (territory_null.py reads no votes in the
sampler), so they are the plans an all-ballots replay would regenerate. This is a rescore, not the Amendment 12,
Part 2 replay. Code: ../wt-a8 at 569250cd (Step C ran 42b5fda8; the diff is CLI-only, territory_score.py lines 227-243).
Same calls as findings/a10_stepc/territory/score_plans_enacted.py, calibrate_enacted.py and the CLI's `rank` branch,
with mcmc_ensemble.build_va_graph defaulted to the all-ballots VA file. Rehearsal, provisional, not a registered result."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
A8 = ROOT.parent / "wt-a8"
VA_ALL = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
MAP = ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled.gpkg"
SRC = ROOT / "findings/a10_stepc/territory"
DST = HERE / "territory_allballots"
STATED_LOW = 2
assert hashlib.sha256(VA_ALL.read_bytes()).hexdigest() == "c9e21ac90fb97b9ee4a7e4da7c80d44922e5849842fc283344f724bb2711be72"

sys.path.insert(0, str(A8 / "analysis/utils"))
sys.path.insert(0, str(A8 / "analysis/scripts"))
import mcmc_ensemble as me  # noqa: E402  (wt-a8's copy, as Step C used)

_orig = me.build_va_graph
me.build_va_graph = lambda verbose=True, va_path=None: _orig(verbose=verbose, va_path=va_path if va_path is not None else VA_ALL)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import territory_score as ts  # noqa: E402

DST.mkdir(exist_ok=True)
for f in list(SRC.glob("chain*_plans.npy")) + list(SRC.glob("chain*_plans.json")) + [SRC / "territory_nodes.json"]:
    shutil.copy2(f, DST / f.name)
# plans must be byte-identical to the filed ones
filed = {l.split()[1].lstrip("*"): l.split()[0] for l in (SRC / "plans_sha256.txt").read_text().splitlines() if l.strip()}
for name, h in filed.items():
    assert hashlib.sha256((DST / name).read_bytes()).hexdigest() == h, name
print("plans identical to the filed Step C plans (SHA-256):", sorted(filed), flush=True)

S = ts.Substrate(str(MAP), STATED_LOW)
print("territory districts", S.k_terr, "fixed", S.n_fixed, "s152 cap", S.s152_cap, flush=True)
ts.score_plans(S, str(DST))
ts.calibrate(S, str(DST), [1, 2, 4, 6], 5, 200, 2_000, 10_000)

lab, _ = S.map_labels(str(MAP))
obs = S.score(lab, 10_000, ts.shuffle_rng(MAP.stem))
df = pd.read_csv(DST / "scores.csv")
ref = df[(df.step > 10_000) & df.chain.isin([1, 2, 4, 6])]
out = {"map": str(MAP), "va_file": VA_ALL.name, "observed": obs, "n_ref_plans": int(len(ref))}
for v in ("eg", "drain", "mean_median", "declination", "ucp_seats"):
    r = ref[v].to_numpy()
    out[v] = {"observed": obs[v], "p_two_sided": float(min(1, 2 * min(np.mean(r <= obs[v]), np.mean(r >= obs[v])))),
              "null_mean": float(r.mean()), "null_p025": float(np.quantile(r, .025)), "null_p975": float(np.quantile(r, .975))}
(DST / "rank.json").write_text(json.dumps(out, indent=1, default=float))
print(json.dumps(out, indent=1, default=float))
