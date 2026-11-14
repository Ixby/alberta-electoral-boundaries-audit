# Step C: territory_score.py at 42b5fda8 builds its Substrate without the enacted map for the `plans`
# subcommand (only `rank` passes it), so a rerun's plans cannot be scored by the CLI. This calls the pinned
# module's own Substrate and score_plans with the enacted map, as `rank` does. No scoring code is changed.
import sys
sys.path.insert(0, "analysis/scripts"); sys.path.insert(0, "analysis/utils")
import territory_score as ts
S = ts.Substrate(sys.argv[1], int(sys.argv[3]))
print("territory districts", S.k_terr, "fixed", S.n_fixed, "s152 cap", S.s152_cap, flush=True)
ts.score_plans(S, sys.argv[2])
