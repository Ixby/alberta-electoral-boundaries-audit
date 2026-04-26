"""
DPG Perturbation Sensitivity — Monte Carlo CIs on §5 headline numbers
=====================================================================

Precision Option E. Quantifies the contribution of DPG-perimeter tracing
uncertainty to every headline §5 claim by generating N random perturbed
realisations of the topology-clean canonical DPG files and recomputing
the MAUP-v2 metric stack on each realisation.

**Method.**
For each perturbation i ∈ {1..N}:
  1. Draw independent per-polygon (dx, dy) offsets from Uniform[-500, +500] m
     and apply `shapely.affinity.translate` to each polygon's geometry.
  2. Normalise the resulting overlapping DPG via the MAUP pipeline's
     built-in per-VA weight-renormalisation (which is the VA-side
     equivalent of the topology-cleanup precedence resolver — any VA whose
     overlap-sum exceeds 1.0 has its fractional weights rescaled so that
     it contributes exactly 1.0 × its full votes across the covered EDs).
     This preserves per-VA vote conservation regardless of perturbation
     topology and is equivalent in effect to re-running the precedence-
     based cleanup before MAUP.
  3. Run the standard MAUP-v2 pipeline (area-weighted intersection +
     crosswalk-fallback for uncovered area + per-ED aggregation) and
     compute for each map (majority, minority):
         - B2 efficiency gap (%)
         - B3 mean-median (pp)
         - B6 declination (Warrington 2018)
         - Seats at 50/50 uniform swing (NDP seats)
     plus the minority − majority EG asymmetry (pp).
  4. Record the conservation-gate flag.

After N realisations, report per-metric p5 / p50 / p95 across the Monte
Carlo sample (honest-bounded 90 % interval) plus mean, standard deviation,
and signed-direction consistency.

Reproducibility: hard-coded SEED=42. CLI exposes --seed, --n, --offset-m
for reviewer replication and alternate stress tests.

Inputs (read-only):
  data/va_polygons_with_full_2023_votes.gpkg
  data/v0_2_canonical_majority_2026_eds_topoclean.gpkg
  data/v0_2_canonical_minority_2026_eds_topoclean.gpkg
  data/v0_1_majority_full_crosswalk.csv
  data/v0_1_minority_full_crosswalk.csv
  data/v0_1_majority_2026_populations.csv
  data/v0_1_minority_2026_populations.csv

Outputs:
  data/v0_1_dpg_perturbation_samples.csv
  data/v0_1_dpg_perturbation_summary.json
  analysis/reports/v0_1_dpg_perturbation_analysis.md

Forward: analysis/reports/v0_1_dpg_perturbation_analysis.md
Backward:
  analysis/scripts/v0_1_phase_4c_va_attribution_maup.py  (MAUP helpers)
  analysis/scripts/v0_1_phase_4c_va_attribution_maup_v2.py (topoclean MAUP)
  analysis/scripts/v0_1_topology_cleanup.py  (precedence resolver)
  data/v0_2_canonical_{majority,minority}_2026_eds_topoclean.gpkg
"""
# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import math
import os
import statistics
import sys
import time
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.affinity import translate

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*GEOS.*")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
SCRIPTS = ANALYSIS / "scripts"
REPORTS = ANALYSIS / "reports"

# Reuse the MAUP helpers from v0_1_phase_4c_va_attribution_maup.py.
v1_path = SCRIPTS / "v0_1_phase_4c_va_attribution_maup.py"
spec = importlib.util.spec_from_file_location("maup_v1", v1_path)
m1 = importlib.util.module_from_spec(spec)
sys.modules["maup_v1"] = m1
spec.loader.exec_module(m1)

VA_GPKG = DATA / "shapefiles" / "derived" / "va_polygons_with_full_2023_votes.gpkg"
MAJ_CLEAN_GPKG = DATA / "shapefiles" / "derived" / "v0_2_canonical_majority_2026_eds_topoclean.gpkg"
MIN_CLEAN_GPKG = DATA / "shapefiles" / "derived" / "v0_2_canonical_minority_2026_eds_topoclean.gpkg"
MAJ_XWALK_CSV = DATA / "v0_1_majority_full_crosswalk.csv"
MIN_XWALK_CSV = DATA / "v0_1_minority_full_crosswalk.csv"
MAJ_POPS_CSV = DATA / "v0_1_majority_2026_populations.csv"
MIN_POPS_CSV = DATA / "v0_1_minority_2026_populations.csv"

OUT_SAMPLES_CSV = DATA / "v0_1_dpg_perturbation_samples.csv"
OUT_SUMMARY_JSON = DATA / "v0_1_dpg_perturbation_summary.json"
OUT_WRITEUP = REPORTS / "v0_1_dpg_perturbation_analysis.md"

# §5.2.7 / MAUP-v2 point-estimate reference values (fifth measurement
# layer compares to these).
MAUP_V2_MAJORITY_EG = -0.02346182160488602
MAUP_V2_MINORITY_EG = +0.01002107484453266
MAUP_V2_MAJORITY_MM = -0.013621963732590225
MAUP_V2_MINORITY_MM = -0.01593104719367827
MAUP_V2_MAJORITY_NDP_SEATS = 40
MAUP_V2_MAJORITY_UCP_SEATS = 49
MAUP_V2_MINORITY_NDP_SEATS = 33
MAUP_V2_MINORITY_UCP_SEATS = 56
MAUP_V2_ASYMMETRY_PP = 3.348289644941868


def compute_declination(ndp_totals: np.ndarray, ucp_totals: np.ndarray) -> float:
    """Warrington (2018) declination from per-ED two-party totals.

    Positive = pro-NDP, negative = pro-UCP. NaN if one party sweeps.
    """
    two = ndp_totals + ucp_totals
    mask = two > 0
    if mask.sum() == 0:
        return float("nan")
    shares = ndp_totals[mask] / two[mask]
    n = int(mask.sum())
    ndp_won = shares[shares > 0.5]
    ucp_won = shares[shares < 0.5]
    if len(ndp_won) == 0 or len(ucp_won) == 0:
        return float("nan")
    n_ndp_wins = len(ndp_won)
    n_ucp_wins = len(ucp_won)
    mean_ndp_won = float(np.mean(ndp_won))
    mean_ucp_won = float(np.mean(ucp_won))
    theta_ndp = math.atan2(mean_ndp_won - 0.5, n_ndp_wins / n)
    theta_ucp = math.atan2(0.5 - mean_ucp_won, n_ucp_wins / n)
    return (theta_ndp - theta_ucp) * 2 / math.pi


def compute_seats_at_50(ndp_totals: np.ndarray, ucp_totals: np.ndarray) -> int:
    """Number of NDP seats under a uniform-swing 50/50 two-party scenario."""
    two = ndp_totals + ucp_totals
    mask = two > 0
    if mask.sum() == 0:
        return 0
    shares = ndp_totals[mask] / two[mask]
    prov = float(np.sum(ndp_totals[mask]) / np.sum(two[mask]))
    swing = 0.5 - prov
    swung = shares + swing
    return int(np.sum(swung > 0.5))


def perturb_map(canon_gdf: gpd.GeoDataFrame, rng: np.random.Generator,
                offset_m: float) -> gpd.GeoDataFrame:
    """Apply an independent random (dx, dy) offset to every polygon.

    Offsets drawn per polygon from Uniform[-offset_m, +offset_m] on each axis.
    """
    out = canon_gdf.copy()
    dxs = rng.uniform(-offset_m, offset_m, size=len(out))
    dys = rng.uniform(-offset_m, offset_m, size=len(out))
    new_geoms = [translate(g, xoff=dx, yoff=dy)
                 for g, dx, dy in zip(out.geometry, dxs, dys)]
    out["geometry"] = new_geoms
    return out


def run_one_realisation(
    i: int,
    vas: gpd.GeoDataFrame,
    maj_canon: gpd.GeoDataFrame,
    min_canon: gpd.GeoDataFrame,
    maj_xwalk: dict,
    min_xwalk: dict,
    maj_names: list,
    min_names: list,
    rng: np.random.Generator,
    offset_m: float,
    silent: bool = True,
) -> dict:
    """Run one perturbation + MAUP realisation; return metrics dict."""
    # Perturb both maps with independent draws (same rng, different draws).
    maj_p = perturb_map(maj_canon, rng, offset_m)
    min_p = perturb_map(min_canon, rng, offset_m)

    # Suppress the MAUP pipeline's verbose prints.
    buf = io.StringIO()
    if silent:
        redirect = contextlib.redirect_stdout(buf)
    else:
        redirect = contextlib.nullcontext()

    with redirect:
        maj = m1.run_one_map(vas, maj_p, maj_xwalk, maj_names, f"maj_p{i}")
        mino = m1.run_one_map(vas, min_p, min_xwalk, min_names, f"min_p{i}")

    maj_ed = maj["ed_totals"]
    min_ed = mino["ed_totals"]
    maj_ndp = maj_ed["ndp_2023"].to_numpy(dtype=float)
    maj_ucp = maj_ed["ucp_2023"].to_numpy(dtype=float)
    min_ndp = min_ed["ndp_2023"].to_numpy(dtype=float)
    min_ucp = min_ed["ucp_2023"].to_numpy(dtype=float)

    maj_decl = compute_declination(maj_ndp, maj_ucp)
    min_decl = compute_declination(min_ndp, min_ucp)
    maj_seats50 = compute_seats_at_50(maj_ndp, maj_ucp)
    min_seats50 = compute_seats_at_50(min_ndp, min_ucp)

    return {
        "perturbation_idx": i,
        "majority_eg_pct": float(maj["eg"]) * 100,
        "minority_eg_pct": float(mino["eg"]) * 100,
        "asymmetry_pp": float(mino["eg"] - maj["eg"]) * 100,
        "majority_mm_pp": float(maj["mm_gap"]) * 100,
        "minority_mm_pp": float(mino["mm_gap"]) * 100,
        "majority_declination": float(maj_decl),
        "minority_declination": float(min_decl),
        "majority_seats_at_50_ndp": int(maj_seats50),
        "minority_seats_at_50_ndp": int(min_seats50),
        "majority_ndp_seats": int(maj["ndp_seats"]),
        "minority_ndp_seats": int(mino["ndp_seats"]),
        "majority_conservation_pass": bool(maj["conservation"]["pass"]),
        "minority_conservation_pass": bool(mino["conservation"]["pass"]),
        "majority_coverage_frac": float(maj["coverage"]["va_area_weighted_coverage_frac"]),
        "minority_coverage_frac": float(mino["coverage"]["va_area_weighted_coverage_frac"]),
    }


def summarise_metric(values: list[float]) -> dict:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return {"n": 0, "mean": None, "std": None, "p5": None, "p50": None,
                "p95": None, "min": None, "max": None}
    return {
        "n": int(len(arr)),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "p5": float(np.quantile(arr, 0.05)),
        "p50": float(np.quantile(arr, 0.50)),
        "p95": float(np.quantile(arr, 0.95)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--n", type=int, default=200,
                        help="Number of perturbation realisations (default 200).")
    parser.add_argument("--seed", type=int, default=42,
                        help="Reproducibility seed (default 42).")
    parser.add_argument("--offset-m", type=float, default=500.0,
                        help="±offset (metres) for per-polygon translation (default 500).")
    parser.add_argument("--progress-every", type=int, default=10,
                        help="Print progress every N perturbations.")
    args = parser.parse_args()

    print("=" * 72)
    print("  DPG Perturbation Sensitivity — Monte Carlo CIs on §5 metrics")
    print("=" * 72)
    print(f"  N perturbations : {args.n}")
    print(f"  seed            : {args.seed}")
    print(f"  offset (metres) : ±{args.offset_m}")
    print(f"  outputs         : {OUT_SAMPLES_CSV.name}, {OUT_SUMMARY_JSON.name},")
    print(f"                    {OUT_WRITEUP.relative_to(ROOT)}")

    # Load inputs once.
    print("\n[load] inputs...")
    t0 = time.time()
    vas = gpd.read_file(VA_GPKG)
    print(f"  VAs: {len(vas)}")

    maj_canon = m1.load_canonical(MAJ_CLEAN_GPKG, vas.crs)
    min_canon = m1.load_canonical(MIN_CLEAN_GPKG, vas.crs)
    print(f"  DPG majority: {len(maj_canon)}   minority: {len(min_canon)}")

    maj_xwalk = m1.load_crosswalk(MAJ_XWALK_CSV)
    min_xwalk = m1.load_crosswalk(MIN_XWALK_CSV)
    maj_names = pd.read_csv(MAJ_POPS_CSV)["ed_name"].tolist()
    min_names = pd.read_csv(MIN_POPS_CSV)["ed_name"].tolist()
    print(f"  load time: {time.time()-t0:.1f}s")

    # Monte Carlo loop.
    rng = np.random.default_rng(args.seed)
    rows: list[dict] = []
    t_loop = time.time()
    for i in range(args.n):
        t_i = time.time()
        try:
            result = run_one_realisation(
                i, vas, maj_canon, min_canon,
                maj_xwalk, min_xwalk, maj_names, min_names,
                rng, args.offset_m, silent=True,
            )
        except Exception as e:
            print(f"  [perturbation {i}] ERROR: {e}")
            continue
        rows.append(result)
        if (i + 1) % args.progress_every == 0 or (i + 1) == args.n:
            elapsed = time.time() - t_loop
            avg = elapsed / (i + 1)
            remaining = avg * (args.n - (i + 1))
            print(f"  [{i+1}/{args.n}] last={time.time()-t_i:.1f}s  "
                  f"avg={avg:.1f}s  elapsed={elapsed/60:.1f}m  "
                  f"ETA={remaining/60:.1f}m  "
                  f"asym_last={result['asymmetry_pp']:+.3f}pp")
        # Incremental checkpoint so a crash at hour 0:30 doesn't lose everything.
        if (i + 1) % max(args.progress_every, 20) == 0:
            pd.DataFrame(rows).to_csv(OUT_SAMPLES_CSV, index=False)

    # Write raw samples table.
    df = pd.DataFrame(rows)
    df.to_csv(OUT_SAMPLES_CSV, index=False)
    print(f"\n[write] raw samples: {OUT_SAMPLES_CSV} ({len(df)} rows)")

    # Conservation gate — fraction of realisations that passed on both maps.
    both_pass = df["majority_conservation_pass"] & df["minority_conservation_pass"]
    n_cons_pass = int(both_pass.sum())
    conservation_pass_rate = n_cons_pass / len(df) if len(df) else 0.0
    print(f"  conservation gate: {n_cons_pass}/{len(df)} realisations passed "
          f"({conservation_pass_rate*100:.1f}%)")

    # Summarise each metric.
    metric_keys = [
        "majority_eg_pct", "minority_eg_pct", "asymmetry_pp",
        "majority_mm_pp", "minority_mm_pp",
        "majority_declination", "minority_declination",
        "majority_seats_at_50_ndp", "minority_seats_at_50_ndp",
        "majority_ndp_seats", "minority_ndp_seats",
    ]
    summary_metrics = {k: summarise_metric(df[k].tolist()) for k in metric_keys}

    # Direction consistency on asymmetry (key §5.2.7 headline claim).
    asym = df["asymmetry_pp"].to_numpy(dtype=float)
    asym = asym[np.isfinite(asym)]
    direction_stats = {
        "n_samples": int(len(asym)),
        "n_positive": int(np.sum(asym > 0)),
        "n_negative": int(np.sum(asym < 0)),
        "n_near_zero_abs_lt_0p05": int(np.sum(np.abs(asym) < 0.05)),
        "fraction_positive": float(np.mean(asym > 0)) if len(asym) else None,
        "p5_asymmetry": float(np.quantile(asym, 0.05)) if len(asym) else None,
        "p95_asymmetry": float(np.quantile(asym, 0.95)) if len(asym) else None,
        "ci90_crosses_zero": (
            bool(np.quantile(asym, 0.05) < 0 < np.quantile(asym, 0.95))
            if len(asym) else None
        ),
    }

    summary = {
        "method": {
            "n_perturbations_requested": args.n,
            "n_perturbations_collected": int(len(df)),
            "seed": args.seed,
            "offset_meters": args.offset_m,
            "perturbation": (
                "per-polygon independent translate(dx, dy) with "
                "dx, dy ~ Uniform(-offset_m, +offset_m); topology overlap "
                "handled by MAUP per-VA weight renormalisation."
            ),
            "inputs": {
                "va_gpkg": str(VA_GPKG),
                "majority_canonical_clean": str(MAJ_CLEAN_GPKG),
                "minority_canonical_clean": str(MIN_CLEAN_GPKG),
            },
        },
        "conservation_gate": {
            "n_pass": n_cons_pass,
            "n_total": int(len(df)),
            "pass_rate": conservation_pass_rate,
            "all_realisations_conserved": bool(n_cons_pass == len(df)),
        },
        "point_estimates_maup_v2": {
            "majority_eg_pct": MAUP_V2_MAJORITY_EG * 100,
            "minority_eg_pct": MAUP_V2_MINORITY_EG * 100,
            "asymmetry_pp": MAUP_V2_ASYMMETRY_PP,
            "majority_mm_pp": MAUP_V2_MAJORITY_MM * 100,
            "minority_mm_pp": MAUP_V2_MINORITY_MM * 100,
            "majority_ndp_seats": MAUP_V2_MAJORITY_NDP_SEATS,
            "minority_ndp_seats": MAUP_V2_MINORITY_NDP_SEATS,
        },
        "metrics": summary_metrics,
        "direction_stats": direction_stats,
        "outputs": {
            "samples_csv": str(OUT_SAMPLES_CSV),
            "summary_json": str(OUT_SUMMARY_JSON),
            "writeup": str(OUT_WRITEUP),
        },
    }

    with open(OUT_SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[write] summary: {OUT_SUMMARY_JSON}")

    # Writeup (markdown).
    write_markdown(summary, args)
    print(f"[write] writeup: {OUT_WRITEUP}")

    print("\n[DONE]  total elapsed:", f"{(time.time()-t_loop)/60:.1f} min")


def _fmt_ci(s: dict, unit: str = "") -> str:
    if s["n"] == 0:
        return "n=0 (no valid samples)"
    return (f"p50={s['p50']:+.3f}{unit}  "
            f"[p5, p95]=[{s['p5']:+.3f}, {s['p95']:+.3f}]{unit}  "
            f"mean={s['mean']:+.3f}{unit}  sd={s['std']:.3f}")


def write_markdown(summary: dict, args: argparse.Namespace) -> None:
    m = summary["metrics"]
    pt = summary["point_estimates_maup_v2"]
    d = summary["direction_stats"]

    def row(label: str, key: str, unit: str, point: float | int | None,
            fmt: str = "{:+.3f}"):
        s = m[key]
        if s["n"] == 0:
            return f"| {label} | n=0 | – | – | – | – |"
        point_str = fmt.format(point) if point is not None else "–"
        return (f"| {label} | "
                f"{fmt.format(s['p5'])} | "
                f"{fmt.format(s['p50'])} | "
                f"{fmt.format(s['p95'])} | "
                f"{fmt.format(s['mean'])} | "
                f"{point_str} |")

    asym_ci_crosses = d.get("ci90_crosses_zero")
    p5_asym = d.get("p5_asymmetry")
    p95_asym = d.get("p95_asymmetry")

    if asym_ci_crosses:
        direction_verdict = (
            "The 90% CI for the minority-vs-majority EG asymmetry **crosses zero** "
            f"([p5={p5_asym:+.3f}, p95={p95_asym:+.3f}] pp), so under ±"
            f"{int(args.offset_m)} m per-polygon boundary-tracing uncertainty the "
            "directional §5.2.7 claim (minority more NDP-favourable) is "
            "**not robust to DPG perimeter error alone**."
        )
    else:
        side = "positive (minority more NDP-favourable)" if p5_asym and p5_asym > 0 else "negative"
        direction_verdict = (
            f"The 90% CI for the asymmetry is entirely {side} "
            f"([p5={p5_asym:+.3f}, p95={p95_asym:+.3f}] pp), so the §5.2.7 "
            "direction **survives** DPG perimeter-tracing uncertainty."
        )

    cons = summary["conservation_gate"]
    cons_line = (
        f"{cons['n_pass']} / {cons['n_total']} realisations "
        f"({cons['pass_rate']*100:.1f}%) passed per-VA conservation on both maps."
    )

    content = f"""# DPG Perturbation Sensitivity — Monte Carlo CIs on §5 Headline Numbers

*Generated by `analysis/scripts/v0_1_dpg_perturbation_sensitivity.py`.*
*This is the fifth measurement layer on top of §5.2.7's four point-estimate
layers (centroid-spatial, blended-crosswalk, MAUP-v1 raw canonical, MAUP-v2
topology-cleaned).*

## 1. Motivation

§5's headline numbers — the efficiency-gap asymmetry, the mean-median gap,
the declination, and the seats-at-50/50 counts — are single point estimates
produced from a single canonical DPG (Derived Provisional Geometry) traced
from 600-DPI commission thumbnails. Tracing precision is approximately
one pixel, which at the published map scale is roughly ±300–500 m on the
ground. A reviewer who asks "how much does one pixel of tracing error move
the asymmetry?" deserves an honest interval, not a fresh point estimate.

## 2. Method

For each of the two topology-clean DPG files
(`data/v0_2_canonical_{{majority,minority}}_2026_eds_topoclean.gpkg`, the
outputs of Precision Option A) we generate **N = {summary['method']['n_perturbations_collected']}** perturbed realisations
by drawing an independent (dx, dy) pair per polygon from
Uniform[-{int(args.offset_m)}, +{int(args.offset_m)}] m and applying
`shapely.affinity.translate`. This mimics a reviewer wiggling every
polygon by up to one pixel of tracing uncertainty on each axis.

After perturbation, overlap with neighbours inevitably appears. Rather
than re-running the full precedence-based topology resolver on every
realisation (which would add ~30 s of O(n²) work per sample), we rely on
the **per-VA weight-renormalisation** already baked into the MAUP pipeline
(`compute_area_weights` in `v0_1_phase_4c_va_attribution_maup.py`): any
VA whose summed area-weight across intersecting EDs exceeds 1.0001 has
its weights rescaled so the sum equals 1.0. This guarantees per-VA vote
conservation regardless of perturbation-induced DPG overlap, and for
small offsets (≤ 500 m) is semantically equivalent to a centroid-proximity
tiebreak — each VA's votes still go only to the EDs that actually cover it.

For each perturbed realisation we compute, on both maps:

- **B2 efficiency gap** (%)
- **B3 mean-median gap** (pp, NDP share)
- **B6 declination** (Warrington 2018; positive = pro-NDP)
- **Seats at 50/50** (NDP seats under uniform-swing to provincial 50/50)
- **Minority − Majority EG asymmetry** (pp)

Seed = {args.seed} (reviewer-reproducible via `--seed`).
CLI also exposes `--n` and `--offset-m` for stress tests at alternate
tracing-uncertainty assumptions.

## 3. Validation — Conservation Gate

{cons_line}

A realisation is counted as passing if the MAUP-pipeline per-VA
conservation check (max |Δ_votes| < 1.0 for every party) returns PASS on
both majority and minority maps.

## 4. Results — Per-Metric 90% Confidence Intervals

Values below are computed across the {summary['method']['n_perturbations_collected']} realisations. `point` is the
§5.2.7 MAUP-v2 (fourth-layer) point estimate for comparison.

| metric | p5 | p50 | p95 | mean | MAUP-v2 point |
|---|---:|---:|---:|---:|---:|
{row('Majority EG (%)', 'majority_eg_pct', '', pt['majority_eg_pct'])}
{row('Minority EG (%)', 'minority_eg_pct', '', pt['minority_eg_pct'])}
{row('Minority − Majority asymmetry (pp)', 'asymmetry_pp', '', pt['asymmetry_pp'])}
{row('Majority mean-median (pp)', 'majority_mm_pp', '', pt['majority_mm_pp'])}
{row('Minority mean-median (pp)', 'minority_mm_pp', '', pt['minority_mm_pp'])}
{row('Majority declination', 'majority_declination', '', None)}
{row('Minority declination', 'minority_declination', '', None)}
{row('Majority seats@50/50 (NDP)', 'majority_seats_at_50_ndp', '', None, '{:.1f}')}
{row('Minority seats@50/50 (NDP)', 'minority_seats_at_50_ndp', '', None, '{:.1f}')}
{row('Majority NDP seats (actual)', 'majority_ndp_seats', '', pt['majority_ndp_seats'], '{:.1f}')}
{row('Minority NDP seats (actual)', 'minority_ndp_seats', '', pt['minority_ndp_seats'], '{:.1f}')}

## 5. Headline-Claim Verdict — Does the §5.2.7 Direction Survive?

Of {d['n_samples']} valid realisations: {d['n_positive']} produced a positive
asymmetry (minority more NDP-favourable, matching the §5.2.7 headline),
{d['n_negative']} produced a negative asymmetry (minority more UCP-favourable),
and {d['n_near_zero_abs_lt_0p05']} fell within ±0.05 pp of zero.

{direction_verdict}

## 6. Paper-Ready Paragraph (Fifth Measurement Layer)

*Drop-in paragraph for insertion after the §5.2.7 topology-cleanup paragraph
as the fifth measurement layer.*

> **Fifth measurement — DPG perturbation sensitivity CI.** To quantify how
> much of the asymmetry shown by the fourth (topology-cleaned MAUP) layer
> is an artefact of one-pixel tracing uncertainty on the canonical DPGs,
> we generated {summary['method']['n_perturbations_collected']} perturbed realisations of each map by applying
> an independent per-polygon translation drawn from Uniform[±{int(args.offset_m)}] m
> (one 600-DPI-thumbnail pixel at published map scale) and re-ran the
> MAUP-v2 area-weighted pipeline on each. Per-VA conservation held on
> {cons['pass_rate']*100:.1f}% of realisations. Across the ensemble, the
> minority-majority EG asymmetry had median **{m['asymmetry_pp']['p50']:+.3f} pp**
> with a 90 % CI of **[{m['asymmetry_pp']['p5']:+.3f}, {m['asymmetry_pp']['p95']:+.3f}] pp**
> around the fourth-layer point estimate of {pt['asymmetry_pp']:+.3f} pp. The
> mean-median gap and declination intervals for both maps are reported in
> Table X. Under ±{int(args.offset_m)} m per-polygon DPG-perimeter
> uncertainty, the §5.2.7 directional claim (minority map measurably more
> NDP-favourable than majority map on the 2023 substrate) is
> {"**preserved**: the 90 % CI lies entirely on the positive side of zero" if not asym_ci_crosses else "**not robust**: the 90 % CI crosses zero, meaning DPG tracing error alone is sufficient to erase the sign of the asymmetry"}.
> Reviewer-reproducible via `python analysis/scripts/v0_1_dpg_perturbation_sensitivity.py --seed {args.seed} --n {args.n} --offset-m {int(args.offset_m)}`.

## 7. Reproducibility

```bash
python analysis/scripts/v0_1_dpg_perturbation_sensitivity.py \\
    --n {args.n} --seed {args.seed} --offset-m {int(args.offset_m)}
```

Runtime ≈ {summary['method']['n_perturbations_collected']} × 10 s = ~35 min on a 2024 laptop. Outputs:
- `{OUT_SAMPLES_CSV.relative_to(ROOT)}` — raw per-realisation metrics
- `{OUT_SUMMARY_JSON.relative_to(ROOT)}` — per-metric p5/p50/p95 summary
- `{OUT_WRITEUP.relative_to(ROOT)}` — this writeup
"""

    with open(OUT_WRITEUP, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    # Windows cp1252 console encoding mangles our Δ / ± prints. Force UTF-8
    # stdout so the pipeline's verbose output (captured + discarded) can't
    # raise UnicodeEncodeError if the user runs with --progress-every 1.
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
