# Step C: as score_plans_enacted.py, for territory_score.calibrate (the CLI builds its Substrate without the
# enacted map). Pinned code at 42b5fda8; no scoring code is changed.
import sys
sys.path.insert(0, "analysis/scripts"); sys.path.insert(0, "analysis/utils")
import territory_score as ts
S = ts.Substrate(sys.argv[1], int(sys.argv[3]))
ts.calibrate(S, sys.argv[2], [1, 2, 4, 6], 5, 200, 2_000, 10_000)
