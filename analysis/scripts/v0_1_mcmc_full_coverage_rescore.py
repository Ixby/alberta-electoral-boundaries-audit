"""MCMC re-score on full 89-district coverage via crosswalk fallback.

The initial MCMC run (analysis/scripts/v0_1_mcmc_ensemble.py) scored each real
2026 map exogenously against the 10,000-sample ensemble distribution
using centroid-in-polygon assignment. Coverage was partial because the
approximate / v6 gpkgs only contained 57 / 70 polygons (out of 89) —
the unchanged Tier A EDs and some Tier B EDs were simply not written
to the artifacts.

This script closes the coverage gap by using the hybrid crosswalks
(`data/v0_1_majority_hybrid_crosswalk.csv` and
`data/v0_1_minority_hybrid_crosswalk.csv`) plus Tier-A identity
fallback: every VA has a `parent_ed_2019` label, and for every 2019 ED
the crosswalk tells us what 2026 ED it maps to under each map. EDs not
in the crosswalk are Tier A and keep their 2019 name under both 2026
maps. This gives 100% VA coverage without needing the missing polygons.

For EDs that DO have polygon coverage in the approximate / v6 gpkgs
(the Tier B/C redraws where the boundary matters), the script uses
centroid-in-polygon assignment as before — so the v6 pixel-exact shapes
for Calgary-De Winton, Calgary-South, Edmonton-Windermere, etc. still
inform the score. Only the UNCOVERED VAs fall back to crosswalk
assignment.

Outputs:
  - data/v0_1_mcmc_real_map_scores_full.json — per-map scores at full
    89-district coverage
  - data/v0_1_mcmc_ensemble_percentiles_full.csv — percentile table
    against the original 10,000-plan ensemble
  - analysis/v0_1_mcmc_full_coverage_rescore.md — report summarizing
    shift in findings under full coverage
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"

EDS_2019_SHP = DATA / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
MAJ_APPROX_GPKG = DATA / "v0_1_approximate_majority_2026_eds.gpkg"
MIN_V6_GPKG = DATA / "v0_1_refined_v6_minority_2026_eds.gpkg"
MAJ_POPS_CSV = DATA / "v0_1_majority_2026_populations.csv"
MIN_POPS_CSV = DATA / "v0_1_minority_2026_populations.csv"
MAJ_XWALK_CSV = DATA / "v0_1_majority_hybrid_crosswalk.csv"
MIN_XWALK_CSV = DATA / "v0_1_minority_hybrid_crosswalk.csv"
VA_GPKG = DATA / "va_polygons_with_2023_votes.gpkg"
ENSEMBLE_CSV = DATA / "v0_1_mcmc_ensemble_samples.csv"

OUT_SCORES_JSON = DATA / "v0_1_mcmc_real_map_scores_full.json"
OUT_PERCENTILES_CSV = DATA / "v0_1_mcmc_ensemble_percentiles_full.csv"


# --- Metric implementations (match v0_1_mcmc_ensemble.py conventions) ---

def efficiency_gap(per_district: pd.DataFrame) -> float:
    """Positive = UCP-favoured."""
    total = per_district["ucp"] + per_district["ndp"]
    ucp_share = per_district["ucp"] / total
    ucp_wins = ucp_share > 0.5
    ucp_wasted = np.where(ucp_wins,
                          per_district["ucp"] - (total / 2 + 0.5),
                          per_district["ucp"])
    ndp_wasted = np.where(~ucp_wins,
                          per_district["ndp"] - (total / 2 + 0.5),
                          per_district["ndp"])
    return float((ndp_wasted.sum() - ucp_wasted.sum()) / total.sum())


def mean_median(per_district: pd.DataFrame) -> float:
    """Positive = UCP-favoured. median − mean UCP share."""
    total = per_district["ucp"] + per_district["ndp"]
    ucp_share = per_district["ucp"] / total
    return float(ucp_share.median() - ucp_share.mean())


def declination(per_district: pd.DataFrame) -> float:
    """Warrington (2018)."""
    total = per_district["ucp"] + per_district["ndp"]
    ucp_share = per_district["ucp"] / total
    ucp_wins_mask = ucp_share > 0.5
    ucp_wins = ucp_share[ucp_wins_mask].sort_values().values
    ndp_wins = ucp_share[~ucp_wins_mask].sort_values().values
    if len(ucp_wins) == 0 or len(ndp_wins) == 0:
        return float("nan")
    r_d = float(np.mean(ndp_wins))
    r_r = float(np.mean(ucp_wins))
    n = len(per_district)
    n_d = len(ndp_wins)
    theta_d = np.arctan2(0.5 - r_d, n_d / n / 2)
    theta_r = np.arctan2(r_r - 0.5, (n - n_d) / n / 2)
    return float(2 * (theta_r - theta_d) / np.pi)


def seats_at_50_50(per_district: pd.DataFrame) -> float:
    total = per_district["ucp"] + per_district["ndp"]
    ucp_share = per_district["ucp"] / total
    province_ucp = per_district["ucp"].sum() / total.sum()
    swing = 0.5 - province_ucp
    return float(((ucp_share + swing) > 0.5).sum() / len(per_district))


# --- Map-specific assignment ---

def crosswalk_dict(xwalk_csv: Path, curr_col: str, prop_col: str) -> dict[str, str]:
    df = pd.read_csv(xwalk_csv)
    return dict(zip(df[curr_col].astype(str).str.strip(),
                    df[prop_col].astype(str).str.strip()))


def assign_vas_to_2026_ed(vas: gpd.GeoDataFrame, polys: gpd.GeoDataFrame | None,
                          name_col: str,
                          xwalk: dict[str, str]) -> gpd.GeoDataFrame:
    """Assign each VA to a 2026 ED name.

    Primary: centroid-in-polygon over available polys.
    Fallback for any VA not covered: parent_ed_2019 → crosswalk lookup
    → 2026 name; if the 2019 parent is not in the crosswalk, 2026 name
    = 2019 name (Tier A).
    """
    vas = vas.copy()
    # Normalise parent_ed_2019 strings
    vas["_parent2019"] = vas["parent_ed_2019"].astype(str).str.strip()

    if polys is not None and len(polys) > 0:
        if polys.crs != vas.crs:
            polys = polys.to_crs(vas.crs)
        # Use representative points to avoid edge artefacts
        centroids = vas.copy()
        centroids["geometry"] = vas.geometry.representative_point()
        joined = gpd.sjoin(centroids, polys[[name_col, "geometry"]],
                           how="left", predicate="within")
        # sjoin may produce duplicates when a centroid lies on shared
        # boundary; keep the first match.
        joined = joined[~joined.index.duplicated(keep="first")]
        vas["_assigned_poly"] = joined[name_col].values
    else:
        vas["_assigned_poly"] = None

    # Apply fallback
    def fallback(row):
        p = row["_parent2019"]
        return xwalk.get(p, p)
    vas["_assigned_xwalk"] = vas.apply(fallback, axis=1)
    # Final assignment: polygon if present, else crosswalk
    vas["ed_2026"] = vas["_assigned_poly"].fillna(vas["_assigned_xwalk"])
    return vas


def score_map_full(vas_assigned: gpd.GeoDataFrame, expected_eds: set[str]) -> dict:
    """Aggregate votes per 2026 ED; compute metrics on full coverage."""
    agg = vas_assigned.groupby("ed_2026").agg(
        ucp=("va_ucp", "sum"),
        ndp=("va_ndp", "sum"),
    ).reset_index()
    agg = agg[(agg["ucp"] + agg["ndp"]) > 0].reset_index(drop=True)

    n_via_poly = int(vas_assigned["_assigned_poly"].notna().sum())
    n_via_xwalk = int(vas_assigned["_assigned_poly"].isna().sum())
    eds_present = set(agg["ed_2026"].astype(str).str.strip())
    eds_missing = expected_eds - eds_present
    eds_extra = eds_present - expected_eds

    return {
        "efficiency_gap": efficiency_gap(agg),
        "mean_median": mean_median(agg),
        "declination": declination(agg),
        "seats_at_50_50": seats_at_50_50(agg),
        "ucp_seats": int(((agg["ucp"] / (agg["ucp"] + agg["ndp"])) > 0.5).sum()),
        "n_districts_scored": int(len(agg)),
        "n_expected": int(len(expected_eds)),
        "n_via_polygon": n_via_poly,
        "n_via_crosswalk": n_via_xwalk,
        "coverage_vas": float(n_via_poly / (n_via_poly + n_via_xwalk)) if (n_via_poly + n_via_xwalk) else 0.0,
        "eds_missing": sorted(eds_missing)[:20],
        "eds_extra": sorted(eds_extra)[:20],
        "ucp_vote_share": float(agg["ucp"].sum() / (agg["ucp"].sum() + agg["ndp"].sum())),
    }


def compute_percentiles(ensemble_csv: Path, real_scores: dict) -> pd.DataFrame:
    ens = pd.read_csv(ensemble_csv)
    rows = []
    for metric in ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]:
        ens_vals = ens[metric].dropna().values
        p5 = float(np.percentile(ens_vals, 5))
        p50 = float(np.percentile(ens_vals, 50))
        p95 = float(np.percentile(ens_vals, 95))
        for mp_label, mp in real_scores.items():
            v = mp[metric]
            pct = float(100.0 * (ens_vals < v).sum() / len(ens_vals))
            rows.append({
                "metric": metric,
                "map": mp_label,
                "value": v,
                "percentile": pct,
                "ensemble_p5": p5,
                "ensemble_p50": p50,
                "ensemble_p95": p95,
            })
    return pd.DataFrame(rows)


def main():
    print("=== Full-coverage MCMC rescore (crosswalk-fallback method) ===\n")
    vas = gpd.read_file(VA_GPKG)
    print(f"VA gpkg: {len(vas)} features, CRS {vas.crs}")

    # Majority
    print("\n--- Majority 2026 ---")
    maj_xwalk = crosswalk_dict(MAJ_XWALK_CSV, "current_2019", "proposed_2026")
    maj_polys = gpd.read_file(MAJ_APPROX_GPKG).to_crs(vas.crs)
    maj_expected = set(pd.read_csv(MAJ_POPS_CSV)["ed_name"].astype(str).str.strip())
    maj_assigned = assign_vas_to_2026_ed(vas, maj_polys, "name_2026", maj_xwalk)
    maj_scores = score_map_full(maj_assigned, maj_expected)

    # Minority
    print("\n--- Minority 2026 v6 ---")
    min_xwalk = crosswalk_dict(MIN_XWALK_CSV, "current_2019", "proposed_2026")
    min_polys = gpd.read_file(MIN_V6_GPKG).to_crs(vas.crs)
    min_expected = set(pd.read_csv(MIN_POPS_CSV)["ed_name"].astype(str).str.strip())
    min_assigned = assign_vas_to_2026_ed(vas, min_polys, "name_2026", min_xwalk)
    min_scores = score_map_full(min_assigned, min_expected)

    # 2019 enacted (baseline, via polygons only; no crosswalk needed)
    print("\n--- 2019 enacted ---")
    e2019 = gpd.read_file(EDS_2019_SHP).to_crs(vas.crs).rename(columns={"EDName2017": "name_2026"})
    empty_xwalk: dict[str, str] = {}
    e_assigned = assign_vas_to_2026_ed(vas, e2019, "name_2026", empty_xwalk)
    e2019_expected = set(e2019["name_2026"].astype(str).str.strip())
    e2019_scores = score_map_full(e_assigned, e2019_expected)

    real = {
        "2019 enacted (full)": e2019_scores,
        "majority 2026 (full coverage)": maj_scores,
        "minority 2026 v6 (full coverage)": min_scores,
    }
    for lbl, s in real.items():
        print(f"\n{lbl}:")
        print(f"  EG={s['efficiency_gap']:+.4f}  MM={s['mean_median']:+.4f}  "
              f"DECL={s['declination']:+.4f}  S@50/50={s['seats_at_50_50']:+.4f}")
        print(f"  UCP seats {s['ucp_seats']} / {s['n_districts_scored']} scored "
              f"(expected {s['n_expected']})")
        print(f"  VA assignment: {s['n_via_polygon']} via polygon, "
              f"{s['n_via_crosswalk']} via crosswalk  "
              f"(polygon coverage {s['coverage_vas']*100:.1f}%)")
        if s["eds_missing"]:
            print(f"  MISSING EDs ({len(s['eds_missing'])}): {s['eds_missing'][:5]}")
        if s["eds_extra"]:
            print(f"  EXTRA EDs (not in expected list) ({len(s['eds_extra'])}): {s['eds_extra'][:5]}")

    # Percentiles
    print("\n--- Percentiles vs. 10,000-plan ensemble ---")
    pct_df = compute_percentiles(ENSEMBLE_CSV, real)
    print(pct_df.to_string(index=False))

    OUT_SCORES_JSON.write_text(json.dumps(real, indent=2))
    pct_df.to_csv(OUT_PERCENTILES_CSV, index=False)
    print(f"\nWrote: {OUT_SCORES_JSON.name}")
    print(f"Wrote: {OUT_PERCENTILES_CSV.name}")


if __name__ == "__main__":
    main()
