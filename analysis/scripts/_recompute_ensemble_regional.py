"""
One-shot helper for the regional-swing robustness check.

Loads the 10k verification ensemble (full per-VA assignments preserved at
data/verification_assignments_raw.npz), recomputes seats@50/50 under
both uniform and regional swing for every plan, and writes the result CSV.
The 10k verification ensemble was generated from the same 2019 baseline /
gerrychain configuration as the 100k production ensemble, so it is a
valid stand-in for percentile rankings (both draw from the same target
distribution; the 100k just has tighter Monte Carlo error).

Output: data/regional_swing_ensemble.csv with columns
    step, s50_uniform, s50_regional

Run:
    PYTHONIOENCODING=utf-8 python \\
        analysis/scripts/_recompute_ensemble_regional.py
"""


import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import geopandas as gpd
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = data_loader._resolve_path("data")

sys.path.insert(0, str(HERE))
from seats_at_50_50_regional import (  # noqa: E402
    derive_regional_swing,
    load_va_with_regions,
    seats_at_50_50_uniform,
    seats_at_50_50_regional,
)

ASSIGN_NPZ = DATA / "verification_assignments_raw.npz"
OUT_CSV = DATA / "regional_swing_ensemble.csv"


def main():
    t0 = time.time()
    print("Loading swing calibration + VA data...")
    swing = derive_regional_swing(verbose=False)
    ratios = swing["ratio_to_provincial"]
    va, ucp, ndp, region = load_va_with_regions()

    print("Loading 10k verification assignments...")
    d = np.load(ASSIGN_NPZ)
    assignments = d["assignments"]  # (10000, 4765) int8
    va_ids = d["va_ids"]  # (4765,)

    # va_ids is a permutation/identity over the VA index. Build a mapping so
    # the assignment row is in the same VA-row order as `ucp`/`ndp`/`region`.
    if not np.array_equal(va_ids, np.arange(len(va))):
        # Reorder to match VA row order
        order = np.argsort(va_ids)
        assignments = assignments[:, order]
        print(f"  reordered assignments by va_ids (max id={va_ids.max()})")
    else:
        print("  va_ids already in row order")

    n_steps = assignments.shape[0]
    rows = []
    last_print = time.time()
    for i in range(n_steps):
        asg = assignments[i].astype(np.int32)
        s50_u, _, _ = seats_at_50_50_uniform(ucp, ndp, asg)
        s50_r, _, _, s_star = seats_at_50_50_regional(ucp, ndp, region, ratios, asg)
        rows.append(
            {
                "step": i,
                "s50_uniform": s50_u,
                "s50_regional": s50_r,
                "applied_s": s_star,
            }
        )
        if time.time() - last_print > 10:
            elapsed = time.time() - t0
            eta = elapsed / (i + 1) * (n_steps - i - 1)
            print(f"  step {i+1}/{n_steps}  elapsed {elapsed:.0f}s  eta {eta:.0f}s")
            last_print = time.time()

    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False)
    print(f"wrote {OUT_CSV}")
    print(
        f"  uniform  s50: mean={df['s50_uniform'].mean():.4f}  "
        f"p5={df['s50_uniform'].quantile(0.05):.4f}  "
        f"p95={df['s50_uniform'].quantile(0.95):.4f}"
    )
    print(
        f"  regional s50: mean={df['s50_regional'].mean():.4f}  "
        f"p5={df['s50_regional'].quantile(0.05):.4f}  "
        f"p95={df['s50_regional'].quantile(0.95):.4f}"
    )


if __name__ == "__main__":
    main()
