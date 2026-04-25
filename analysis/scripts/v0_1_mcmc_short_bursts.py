"""
v0_1_mcmc_short_bursts.py
==========================
Short-burst analysis: 500 independent 10-step ReCom chains starting from the
2019 enacted assignment. Each burst endpoint is scored on all four partisan
metrics. The distribution of burst-endpoint scores characterises the
*reachable neighbourhood* of the 2019 starting point and lets us answer:
"Is the minority/majority map score achievable within 10 ReCom steps from
the 2019 baseline, or does it require an unusually long random walk?"

References: DeFord et al. (2021) "Recombination: A family of Markov chains
for redistricting." Short-burst evaluation of maps against the ensemble is
discussed in MGGG workshop notes and Chikina et al. (2017).

Outputs:
  data/v0_1_mcmc_short_bursts.csv        — 5,000 burst-endpoint rows
  data/v0_1_mcmc_short_bursts_summary.json
  analysis/reports/v0_1_mcmc_short_bursts.md

Backward:
  data/shapefiles/derived/v0_7_canonical_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_7_canonical_minority_2026_eds.gpkg
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
Forward:
  report_academic.md §5.4 (MCMC Run #3 supplement)
"""
from __future__ import annotations

import json
import random as _random
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v0_1_mcmc_ensemble import (
    build_va_graph,
    initial_assignment_2019,
    run_ensemble,
    seat_results,
    score_exogenous_map,
    pct_rank,
    MAJ_V7_PATH,
    MIN_V7_PATH,
    MAJ_V8_PATH,
    MIN_V8_PATH,
    MAJ_V8_CANON_PATH,
    MIN_V8_CANON_PATH,
)


def _pick_path(plan: str):
    """Prefer v0_8 refined, then v0_8 canonical, then v0_7 canonical."""
    if plan == "majority":
        for p in (MAJ_V8_PATH, MAJ_V8_CANON_PATH, MAJ_V7_PATH):
            if p.exists():
                return p
        return MAJ_V7_PATH
    else:
        for p in (MIN_V8_PATH, MIN_V8_CANON_PATH, MIN_V7_PATH):
            if p.exists():
                return p
        return MIN_V7_PATH

ROOT = HERE.parent.parent
DATA = ROOT / "data"
RPTS = ROOT / "analysis" / "reports"

OUT_CSV  = DATA / "v0_1_mcmc_short_bursts.csv"
OUT_JSON = DATA / "v0_1_mcmc_short_bursts_summary.json"
OUT_MD   = RPTS / "v0_1_mcmc_short_bursts.md"

N_BURSTS    = 500
BURST_LEN   = 10
POP_DEV     = 0.25


def run_bursts(graph, assignment, n_bursts: int, burst_len: int,
               pop_deviation: float, seed: int) -> pd.DataFrame:
    """
    Run `n_bursts` independent ReCom chains of `burst_len` steps each,
    all starting from `assignment`. Each burst uses a different seed so chains
    are independent. Returns a DataFrame of the burst-endpoint scores.
    """
    all_rows = []
    rng = np.random.default_rng(seed)
    burst_seeds = rng.integers(0, 2**31 - 1, size=n_bursts).tolist()

    for i, bs in enumerate(burst_seeds):
        if i % 50 == 0:
            print(f"  burst {i}/{n_bursts}...", flush=True)
        # Seed global RNG state before each burst so chains are independent
        np.random.seed(int(bs) % (2**32))
        _random.seed(int(bs) % (2**32))
        rows = run_ensemble(graph, assignment, burst_len,
                            pop_deviation=pop_deviation, verbose=False)
        if rows:
            last = rows[-1]
            last["burst"] = i
            last["burst_seed"] = int(bs)
            all_rows.append(last)

    return pd.DataFrame(all_rows)


def main(n_bursts: int = N_BURSTS, burst_len: int = BURST_LEN,
         pop_deviation: float = POP_DEV, seed: int = 42):
    t0 = time.time()
    print(f"[short bursts] {n_bursts} × {burst_len} steps  seed={seed}")

    va, graph = build_va_graph()
    assignment = initial_assignment_2019(va)

    # Real-map scores for comparison
    print("Scoring real maps...")
    agg_2019 = va.groupby("parent_ed_2019").agg(
        ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum")
    ).reset_index()
    m_2019 = seat_results(agg_2019["ucp"].values, agg_2019["ndp"].values)

    maj_path = _pick_path("majority")
    min_path = _pick_path("minority")
    print(f"  using majority: {maj_path.name}")
    print(f"  using minority: {min_path.name}")
    m_maj = score_exogenous_map(va, maj_path) if maj_path.exists() else None
    m_min = score_exogenous_map(va, min_path) if min_path.exists() else None

    # Run bursts
    print(f"\nRunning {n_bursts} bursts × {burst_len} steps...")
    df = run_bursts(graph, assignment, n_bursts, burst_len, pop_deviation, seed)
    df.to_csv(OUT_CSV, index=False)
    print(f"  Wrote {OUT_CSV} ({len(df)} burst endpoints)")

    metrics = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]

    print("\n--- BURST-ENDPOINT DISTRIBUTION ---")
    summary = {}
    for m in metrics:
        vals = df[m].dropna().values
        p5, p50, p95 = np.percentile(vals, [5, 50, 95])
        mn, mx = vals.min(), vals.max()
        summary[m] = {
            "n": len(vals),
            "mean": float(vals.mean()),
            "p5": float(p5),
            "p50": float(p50),
            "p95": float(p95),
            "min": float(mn),
            "max": float(mx),
        }
        print(f"  {m:<22s}  mean={vals.mean():+.4f}  "
              f"[p5={p5:+.4f} p50={p50:+.4f} p95={p95:+.4f}]  "
              f"range=[{mn:+.4f}, {mx:+.4f}]")

    # Percentile ranks of real maps within burst distribution
    print("\n--- REAL MAP RANKS WITHIN BURST DISTRIBUTION ---")
    ranks = {}
    for label, m_real in [("2019_enacted", m_2019),
                           ("majority_2026_v7", m_maj),
                           ("minority_2026_v7", m_min)]:
        if m_real is None:
            continue
        ranks[label] = {}
        for met in metrics:
            val = m_real.get(met, float("nan"))
            if np.isnan(val):
                continue
            vals = df[met].dropna().values
            pr = float(100.0 * (vals < val).mean())
            ranks[label][met] = {"value": val, "burst_pct_rank": pr}
            print(f"  {label:25s}  {met:<22s}  val={val:+.4f}  burst_pct={pr:.1f}")

    # JSON output
    payload = {
        "config": {
            "n_bursts": n_bursts,
            "burst_len": burst_len,
            "pop_deviation": pop_deviation,
            "seed": seed,
        },
        "burst_distribution": summary,
        "real_map_ranks": ranks,
        "elapsed_seconds": round(time.time() - t0, 1),
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=float)
    print(f"\nWrote {OUT_JSON}")

    # Markdown report
    md = [
        "# MCMC Short-Burst Analysis — Alberta 2026 Electoral Maps",
        "",
        f"**Config:** {n_bursts} bursts × {burst_len} steps each; "
        f"pop deviation ±{pop_deviation:.0%}; seed {seed}.",
        "Starting point: 2019 enacted assignment. Each burst is an independent "
        "ReCom chain with a unique seed.",
        "",
        "## Burst-endpoint distribution",
        "",
        "| Metric | Mean | p5 | p50 | p95 | Min | Max |",
        "|---|---|---|---|---|---|---|",
    ]
    for met, s in summary.items():
        md.append(
            f"| {met} | {s['mean']:+.4f} | {s['p5']:+.4f} | "
            f"{s['p50']:+.4f} | {s['p95']:+.4f} | "
            f"{s['min']:+.4f} | {s['max']:+.4f} |"
        )
    md += [
        "",
        "## Real map percentile ranks within burst distribution",
        "",
        "A high rank means the real map score is more extreme than most "
        "10-step neighbourhood walks can reach from the 2019 starting point.",
        "",
        "| Map | Metric | Value | Burst pct rank |",
        "|---|---|---|---|",
    ]
    for label, mranks in ranks.items():
        for met, r in mranks.items():
            md.append(
                f"| {label} | {met} | {r['value']:+.4f} | {r['burst_pct_rank']:.1f} |"
            )
    md.append(f"\n_Generated {time.strftime('%Y-%m-%d %H:%M')} — elapsed "
              f"{time.time()-t0:.0f}s_")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"\nDone in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
