"""
DPG Perturbation Sensitivity v2 — Tier-aware sigma
====================================================

Sibling of ``v0_1_dpg_perturbation_sensitivity.py`` (flat ±500 m). v2 draws
the per-polygon (dx, dy) offsets from a sigma keyed to each polygon's
``canon_source`` metadata, so authoritative Tier-A polygons (2019 parents)
aren't over-perturbed and noisy Tier-C v7-raw polygons aren't
under-perturbed.

**Per-tier sigma (meters, halfwidth of Uniform[-sigma, +sigma]):**

    2019-parent              0    (authoritative Elections Alberta shapefile)
    sweep                   50    (population-calibrated, DA-snapped)
    osm-municipal-buffered  50    (CSD-snapped on anchored segments)
    v7                     300    (visual transcription, feature-snapped)
    (anything else/missing) 300    (conservative fallback)

The --profile CLI flag picks a sigma dict. ``central`` is the default
(table above). ``tight`` is an optional third layer (sweep/osm=20, v7=200)
to test CI sensitivity to sigma choice. ``flat-500`` reproduces the v1
behaviour for regression testing.

Inputs are identical to v1 (same topoclean substrate). Outputs are
sibling files with the suffix ``_v2_tiered`` so v1 artefacts are preserved.

Forward: analysis/reports/dpg_perturbation_tiered_analysis.md
Backward:
  analysis/scripts/v0_1_dpg_perturbation_sensitivity.py  (v1 flat-sigma run)
  analysis/scripts/v0_1_assignment_va_attribution_maup.py  (MAUP helpers)
  data/v0_2_canonical_{majority,minority}_2026_eds_topoclean.gpkg
"""

# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
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

# Reuse v1 machinery wholesale.
v1_spec = importlib.util.spec_from_file_location(
    "dpg_v1", SCRIPTS / "v0_1_dpg_perturbation_sensitivity.py"
)
_v1 = importlib.util.module_from_spec(v1_spec)
sys.modules["dpg_v1"] = _v1
v1_spec.loader.exec_module(_v1)

m1 = _v1.m1  # MAUP helpers from v0_1_assignment_va_attribution_maup.py
compute_declination = _v1.compute_declination
compute_seats_at_50 = _v1.compute_seats_at_50
summarise_metric = _v1.summarise_metric

VA_GPKG = _v1.VA_GPKG
MAJ_CLEAN_GPKG = _v1.MAJ_CLEAN_GPKG
MIN_CLEAN_GPKG = _v1.MIN_CLEAN_GPKG
MAJ_XWALK_CSV = _v1.MAJ_XWALK_CSV
MIN_XWALK_CSV = _v1.MIN_XWALK_CSV
MAJ_POPS_CSV = _v1.MAJ_POPS_CSV
MIN_POPS_CSV = _v1.MIN_POPS_CSV

# MAUP-v2 point-estimate references (same as v1).
MAUP_V2_MAJORITY_EG = _v1.MAUP_V2_MAJORITY_EG
MAUP_V2_MINORITY_EG = _v1.MAUP_V2_MINORITY_EG
MAUP_V2_MAJORITY_MM = _v1.MAUP_V2_MAJORITY_MM
MAUP_V2_MINORITY_MM = _v1.MAUP_V2_MINORITY_MM
MAUP_V2_MAJORITY_NDP_SEATS = _v1.MAUP_V2_MAJORITY_NDP_SEATS
MAUP_V2_MINORITY_NDP_SEATS = _v1.MAUP_V2_MINORITY_NDP_SEATS
MAUP_V2_ASYMMETRY_PP = _v1.MAUP_V2_ASYMMETRY_PP

# Tier-aware sigma profiles (metres). Uniform[-sigma, +sigma] per axis.
SIGMA_PROFILES: dict[str, dict[str, float]] = {
    "central": {
        "2019-parent": 0.0,
        "sweep": 50.0,
        "osm-municipal-buffered": 50.0,
        "v7": 300.0,
        "_default": 300.0,
    },
    "tight": {
        "2019-parent": 0.0,
        "sweep": 20.0,
        "osm-municipal-buffered": 20.0,
        "v7": 200.0,
        "_default": 200.0,
    },
    "flat-500": {
        "2019-parent": 500.0,
        "sweep": 500.0,
        "osm-municipal-buffered": 500.0,
        "v7": 500.0,
        "_default": 500.0,
    },
}


def polygon_sigmas(
    canon_gdf: gpd.GeoDataFrame, profile: dict[str, float]
) -> np.ndarray:
    """Return per-polygon sigma (m) for the given tier profile."""
    src = canon_gdf.get("canon_source")
    if src is None:
        return np.full(len(canon_gdf), profile["_default"], dtype=float)
    out = np.array(
        [
            (
                profile.get(str(s), profile["_default"])
                if pd.notna(s)
                else profile["_default"]
            )
            for s in src.tolist()
        ],
        dtype=float,
    )
    return out


def perturb_map_tiered(
    canon_gdf: gpd.GeoDataFrame, rng: np.random.Generator, sigmas: np.ndarray
) -> gpd.GeoDataFrame:
    """Apply per-polygon (dx, dy) offset with polygon-specific sigma.

    dx, dy independently ~ Uniform[-sigma_i, +sigma_i] for each polygon i.
    """
    out = canon_gdf.copy()
    u = rng.uniform(-1.0, 1.0, size=len(out))
    v = rng.uniform(-1.0, 1.0, size=len(out))
    dxs = u * sigmas
    dys = v * sigmas
    new_geoms = [
        translate(g, xoff=dx, yoff=dy) for g, dx, dy in zip(out.geometry, dxs, dys)
    ]
    out["geometry"] = new_geoms
    return out


def run_one_realisation_tiered(
    i: int,
    vas: gpd.GeoDataFrame,
    maj_canon: gpd.GeoDataFrame,
    min_canon: gpd.GeoDataFrame,
    maj_sigmas: np.ndarray,
    min_sigmas: np.ndarray,
    maj_xwalk: dict,
    min_xwalk: dict,
    maj_names: list,
    min_names: list,
    rng: np.random.Generator,
    silent: bool = True,
) -> dict:
    maj_p = perturb_map_tiered(maj_canon, rng, maj_sigmas)
    min_p = perturb_map_tiered(min_canon, rng, min_sigmas)

    buf = io.StringIO()
    redirect = contextlib.redirect_stdout(buf) if silent else contextlib.nullcontext()
    with redirect:
        maj = m1.run_one_map(vas, maj_p, maj_xwalk, maj_names, f"maj_p{i}")
        mino = m1.run_one_map(vas, min_p, min_xwalk, min_names, f"min_p{i}")

    maj_ed = maj["ed_totals"]
    min_ed = mino["ed_totals"]
    maj_ndp = maj_ed["ndp_2023"].to_numpy(dtype=float)
    maj_ucp = maj_ed["ucp_2023"].to_numpy(dtype=float)
    min_ndp = min_ed["ndp_2023"].to_numpy(dtype=float)
    min_ucp = min_ed["ucp_2023"].to_numpy(dtype=float)

    return {
        "perturbation_idx": i,
        "majority_eg_pct": float(maj["eg"]) * 100,
        "minority_eg_pct": float(mino["eg"]) * 100,
        "asymmetry_pp": float(mino["eg"] - maj["eg"]) * 100,
        "majority_mm_pp": float(maj["mm_gap"]) * 100,
        "minority_mm_pp": float(mino["mm_gap"]) * 100,
        "majority_declination": float(compute_declination(maj_ndp, maj_ucp)),
        "minority_declination": float(compute_declination(min_ndp, min_ucp)),
        "majority_seats_at_50_ndp": int(compute_seats_at_50(maj_ndp, maj_ucp)),
        "minority_seats_at_50_ndp": int(compute_seats_at_50(min_ndp, min_ucp)),
        "majority_ndp_seats": int(maj["ndp_seats"]),
        "minority_ndp_seats": int(mino["ndp_seats"]),
        "majority_conservation_pass": bool(maj["conservation"]["pass"]),
        "minority_conservation_pass": bool(mino["conservation"]["pass"]),
        "majority_coverage_frac": float(
            maj["coverage"]["va_area_weighted_coverage_frac"]
        ),
        "minority_coverage_frac": float(
            mino["coverage"]["va_area_weighted_coverage_frac"]
        ),
    }


def tier_breakdown(canon_gdf: gpd.GeoDataFrame, sigmas: np.ndarray) -> list[dict]:
    src = canon_gdf.get("canon_source")
    if src is None:
        return [
            {
                "canon_source": "MISSING",
                "n": len(canon_gdf),
                "sigma_m": float(sigmas[0]) if len(sigmas) else None,
            }
        ]
    rows = []
    vc = src.fillna("MISSING").value_counts()
    for s, n in vc.items():
        mask = (src.fillna("MISSING") == s).to_numpy()
        sig = float(sigmas[mask][0]) if mask.any() else None
        rows.append({"canon_source": str(s), "n": int(n), "sigma_m": sig})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--n", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--profile",
        type=str,
        default="central",
        choices=list(SIGMA_PROFILES.keys()),
        help="Tier-aware sigma profile (default central).",
    )
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument(
        "--suffix",
        type=str,
        default=None,
        help="Filename suffix (default: '_v2_tiered' for central, "
        "'_v3_tight' for tight, '_v2_flat500' for flat-500).",
    )
    args = parser.parse_args()

    profile = SIGMA_PROFILES[args.profile]
    default_suffixes = {
        "central": "_v2_tiered",
        "tight": "_v3_tight",
        "flat-500": "_v2_flat500",
    }
    suffix = args.suffix or default_suffixes[args.profile]

    out_samples = DATA / f"v0_1_dpg_perturbation_samples{suffix}.csv"
    out_summary = DATA / f"v0_1_dpg_perturbation_summary{suffix}.json"

    print("=" * 72)
    print(f"  DPG Perturbation Sensitivity v2 — tier-aware (profile={args.profile})")
    print("=" * 72)
    for k in ["2019-parent", "sweep", "osm-municipal-buffered", "v7", "_default"]:
        print(f"    sigma[{k:24s}] = {profile[k]:.0f} m")
    print(f"  N   : {args.n}   seed: {args.seed}")
    print(f"  out : {out_samples.name}")
    print(f"        {out_summary.name}")

    print("\n[load] inputs...")
    t0 = time.time()
    vas = gpd.read_file(VA_GPKG)
    maj_canon = m1.load_canonical(MAJ_CLEAN_GPKG, vas.crs)
    min_canon = m1.load_canonical(MIN_CLEAN_GPKG, vas.crs)
    # load_canonical may drop the canon_source column; re-attach from raw read.
    if "canon_source" not in maj_canon.columns:
        raw = gpd.read_file(MAJ_CLEAN_GPKG)
        key = "name_2026" if "name_2026" in raw.columns else raw.columns[0]
        maj_canon = maj_canon.merge(raw[[key, "canon_source"]], on=key, how="left")
    if "canon_source" not in min_canon.columns:
        raw = gpd.read_file(MIN_CLEAN_GPKG)
        key = "name_2026" if "name_2026" in raw.columns else raw.columns[0]
        min_canon = min_canon.merge(raw[[key, "canon_source"]], on=key, how="left")
    maj_xwalk = m1.load_crosswalk(MAJ_XWALK_CSV)
    min_xwalk = m1.load_crosswalk(MIN_XWALK_CSV)
    maj_names = pd.read_csv(MAJ_POPS_CSV)["ed_name"].tolist()
    min_names = pd.read_csv(MIN_POPS_CSV)["ed_name"].tolist()

    maj_sigmas = polygon_sigmas(maj_canon, profile)
    min_sigmas = polygon_sigmas(min_canon, profile)

    maj_breakdown = tier_breakdown(maj_canon, maj_sigmas)
    min_breakdown = tier_breakdown(min_canon, min_sigmas)
    print(f"  load time: {time.time()-t0:.1f}s")
    print("  MAJORITY tier breakdown:")
    for r in maj_breakdown:
        print(f"    {r['canon_source']:26s} n={r['n']:3d}  sigma={r['sigma_m']:.0f} m")
    print("  MINORITY tier breakdown:")
    for r in min_breakdown:
        print(f"    {r['canon_source']:26s} n={r['n']:3d}  sigma={r['sigma_m']:.0f} m")

    rng = np.random.default_rng(args.seed)
    rows: list[dict] = []
    t_loop = time.time()
    for i in range(args.n):
        t_i = time.time()
        try:
            result = run_one_realisation_tiered(
                i,
                vas,
                maj_canon,
                min_canon,
                maj_sigmas,
                min_sigmas,
                maj_xwalk,
                min_xwalk,
                maj_names,
                min_names,
                rng,
                silent=True,
            )
        except Exception as e:
            print(f"  [perturbation {i}] ERROR: {e}")
            continue
        rows.append(result)
        if (i + 1) % args.progress_every == 0 or (i + 1) == args.n:
            elapsed = time.time() - t_loop
            avg = elapsed / (i + 1)
            remaining = avg * (args.n - (i + 1))
            print(
                f"  [{i+1}/{args.n}] last={time.time()-t_i:.1f}s  "
                f"avg={avg:.1f}s  elapsed={elapsed/60:.1f}m  "
                f"ETA={remaining/60:.1f}m  "
                f"asym_last={result['asymmetry_pp']:+.3f}pp"
            )
        if (i + 1) % max(args.progress_every, 20) == 0:
            pd.DataFrame(rows).to_csv(out_samples, index=False)

    df = pd.DataFrame(rows)
    df.to_csv(out_samples, index=False)
    print(f"\n[write] raw samples: {out_samples} ({len(df)} rows)")

    both_pass = df["majority_conservation_pass"] & df["minority_conservation_pass"]
    n_cons_pass = int(both_pass.sum())
    conservation_pass_rate = n_cons_pass / len(df) if len(df) else 0.0

    metric_keys = [
        "majority_eg_pct",
        "minority_eg_pct",
        "asymmetry_pp",
        "majority_mm_pp",
        "minority_mm_pp",
        "majority_declination",
        "minority_declination",
        "majority_seats_at_50_ndp",
        "minority_seats_at_50_ndp",
        "majority_ndp_seats",
        "minority_ndp_seats",
    ]
    summary_metrics = {k: summarise_metric(df[k].tolist()) for k in metric_keys}

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
            if len(asym)
            else None
        ),
    }

    summary = {
        "method": {
            "profile": args.profile,
            "sigma_profile_m": profile,
            "n_perturbations_requested": args.n,
            "n_perturbations_collected": int(len(df)),
            "seed": args.seed,
            "perturbation": (
                "per-polygon independent translate(dx, dy) with "
                "dx, dy ~ Uniform(-sigma_i, +sigma_i); sigma_i keyed to "
                "canon_source metadata."
            ),
            "inputs": {
                "va_gpkg": str(VA_GPKG),
                "majority_canonical_clean": str(MAJ_CLEAN_GPKG),
                "minority_canonical_clean": str(MIN_CLEAN_GPKG),
            },
            "tier_breakdown_majority": maj_breakdown,
            "tier_breakdown_minority": min_breakdown,
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
            "samples_csv": str(out_samples),
            "summary_json": str(out_summary),
        },
    }

    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[write] summary: {out_summary}")
    print(f"\n[DONE] total elapsed: {(time.time()-t_loop)/60:.1f} min")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
