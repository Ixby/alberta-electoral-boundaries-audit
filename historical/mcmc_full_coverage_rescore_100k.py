"""Full-coverage rescore against the 100k ensemble.

Follow-up to analysis/scripts/v0_1_mcmc_full_coverage_rescore.py (which used the
10k ensemble and a 19-row majority crosswalk). This version uses the
augmented 87-row full crosswalks built by
analysis/scripts/v0_1_build_full_crosswalks.py and compares against the 100k
ensemble.

Outputs:
  - data/simulation_real_map_scores_full_100k.json
  - data/simulated_ensemble_percentiles_full_100k.csv

Assignment logic (per VA):
  1. Primary: centroid-in-polygon over the 2026 gpkg (v6 for minority,
     approximate for majority).
  2. Fallback: parent_ed_2019 -> full crosswalk -> 2026 ED name.

This preserves all VAs in the province (4,765 of them), so the metric
is computed over 100% of 2023 votes under the commission's own
population assignment (from the 89-ED populations CSV).

Forward: analysis/methodology/mcmc_100k_and_full_coverage.md
Backward:
  data/majority_full_crosswalk.csv
  data/minority_full_crosswalk.csv
  data/v0_1_approximate_majority_2026_eds.gpkg
  data/v0_1_refined_v6_minority_2026_eds.gpkg
  data/va_polygons_with_2023_votes.gpkg
  data/simulated_ensemble_raw_samples_100k.csv  (must exist)
  data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
"""

# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations
import json
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"

EDS_2019_SHP = (
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)
MAJ_APPROX_GPKG = (
    DATA / "shapefiles" / "derived" / "v0_9_topological_majority_2026_eds.gpkg"
)
MIN_V6_GPKG = (
    DATA / "shapefiles" / "derived" / "v0_9_topological_minority_2026_eds.gpkg"
)
MAJ_POPS_CSV = DATA / "majority_2026_populations.csv"
MIN_POPS_CSV = DATA / "minority_2026_populations.csv"
MAJ_XWALK_CSV_FULL = DATA / "majority_full_crosswalk.csv"
MIN_XWALK_CSV_FULL = DATA / "minority_full_crosswalk.csv"
VA_GPKG = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
ENSEMBLE_CSV_100K = DATA / "simulated_ensemble_raw_samples_100k.csv"

OUT_SCORES_JSON = DATA / "simulation_real_map_scores_full_100k.json"
OUT_PERCENTILES_CSV = DATA / "simulated_ensemble_percentiles_full_100k.csv"


def norm(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip()
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    return unicodedata.normalize("NFC", s)


# --- metric implementations matching v0_1_mcmc_ensemble.py conventions ---


def efficiency_gap(per_district: pd.DataFrame) -> float:
    total = per_district["ucp"] + per_district["ndp"]
    ucp_share = per_district["ucp"] / total
    ucp_wins = (ucp_share > 0.5 + 1e-9).sum()
    ucp_ties = (np.abs(ucp_share - 0.5) <= 1e-9).sum()
    ucp_wins = int(ucp_wins + ucp_ties * 0.5)
    ucp_wasted = np.where(
        ucp_wins, per_district["ucp"] - (total / 2), per_district["ucp"]
    )
    ndp_wasted = np.where(
        ~ucp_wins, per_district["ndp"] - (total / 2), per_district["ndp"]
    )
    return float((ndp_wasted.sum() - ucp_wasted.sum()) / total.sum())


def mean_median(per_district: pd.DataFrame) -> float:
    total = per_district["ucp"] + per_district["ndp"]
    ucp_share = per_district["ucp"] / total
    return float(ucp_share.median() - ucp_share.mean())


def declination(per_district: pd.DataFrame) -> float:
    total = per_district["ucp"] + per_district["ndp"]
    ucp_share = per_district["ucp"] / total
    ucp_wins_mask = ucp_share > 0.5 + 1e-9
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
    swung = ucp_share + swing
    wins = (swung > 0.5 + 1e-9).sum()
    ties = (np.abs(swung - 0.5) <= 1e-9).sum()
    return float((wins + ties * 0.5) / len(per_district))


def crosswalk_dict(xwalk_csv: Path) -> dict[str, str]:
    df = pd.read_csv(xwalk_csv)
    return {norm(r["current_2019"]): norm(r["proposed_2026"]) for _, r in df.iterrows()}


def assign_vas_to_2026_ed(
    vas: gpd.GeoDataFrame, polys: gpd.GeoDataFrame, name_col: str, xwalk: dict[str, str]
) -> gpd.GeoDataFrame:
    """Assign each VA to a 2026 ED: polygon first, crosswalk fallback."""
    vas = vas.copy()
    vas["_parent2019"] = vas["parent_ed_2019"].astype(str).apply(norm)

    if polys.crs != vas.crs:
        polys = polys.to_crs(vas.crs)
    centroids = vas.copy()
    centroids["geometry"] = vas.geometry.representative_point()
    joined = gpd.sjoin(
        centroids, polys[[name_col, "geometry"]], how="left", predicate="within"
    )
    joined = joined[~joined.index.duplicated(keep="first")]
    vas["_assigned_poly"] = (
        joined[name_col].apply(lambda x: norm(x) if pd.notna(x) else None).values
    )

    vas["_assigned_xwalk"] = vas["_parent2019"].map(xwalk).fillna(vas["_parent2019"])
    vas["ed_2026"] = vas["_assigned_poly"].fillna(vas["_assigned_xwalk"])
    return vas


def score_map(vas_assigned: gpd.GeoDataFrame, expected_eds: set[str]) -> dict:
    agg = (
        vas_assigned.groupby("ed_2026")
        .agg(
            ucp=("va_ucp", "sum"),
            ndp=("va_ndp", "sum"),
            total_votes=("va_ucp", "sum"),  # overwritten below
        )
        .reset_index()
    )
    # Recompute total votes
    agg["total_votes"] = agg["ucp"] + agg["ndp"]
    agg = agg[agg["total_votes"] > 0].reset_index(drop=True)

    n_via_poly = int(vas_assigned["_assigned_poly"].notna().sum())
    n_via_xwalk = int(vas_assigned["_assigned_poly"].isna().sum())
    eds_present = set(norm(x) for x in agg["ed_2026"])
    eds_missing = expected_eds - eds_present
    eds_extra = eds_present - expected_eds

    total_ucp = int(agg["ucp"].sum())
    total_ndp = int(agg["ndp"].sum())
    swung = agg["ucp"] / (agg["ucp"] + agg["ndp"])
    wins = (swung > 0.5 + 1e-9).sum()
    ties = (np.abs(swung - 0.5) <= 1e-9).sum()
    ucp_wins = int(wins + ties * 0.5)
    return {
        "efficiency_gap": efficiency_gap(agg),
        "mean_median": mean_median(agg),
        "declination": declination(agg),
        "seats_at_50_50": seats_at_50_50(agg),
        "ucp_seats": ucp_wins,
        "n_districts_scored": int(len(agg)),
        "n_expected": int(len(expected_eds)),
        "n_via_polygon": n_via_poly,
        "n_via_crosswalk": n_via_xwalk,
        "coverage_polygon_pct": (
            float(n_via_poly / (n_via_poly + n_via_xwalk))
            if (n_via_poly + n_via_xwalk)
            else 0.0
        ),
        "eds_missing": sorted(eds_missing)[:20],
        "eds_extra": sorted(eds_extra)[:20],
        "ucp_vote_share": (
            float(total_ucp / (total_ucp + total_ndp))
            if (total_ucp + total_ndp)
            else 0.0
        ),
        "total_votes": int(total_ucp + total_ndp),
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
            if np.isnan(v):
                pct = float("nan")
            else:
                below = (ens_vals < v).sum()
                equal = (ens_vals == v).sum()
                pct = float(100.0 * (below + 0.5 * equal) / len(ens_vals))
            rows.append(
                {
                    "metric": metric,
                    "map": mp_label,
                    "value": v,
                    "percentile": pct,
                    "ensemble_p5": p5,
                    "ensemble_p50": p50,
                    "ensemble_p95": p95,
                    "n_ensemble": int(len(ens_vals)),
                }
            )
    return pd.DataFrame(rows)


def main():
    if not ENSEMBLE_CSV_100K.exists():
        print(
            f"ERROR: {ENSEMBLE_CSV_100K} missing. Run v0_1_mcmc_ensemble_100k.py first."
        )
        sys.exit(1)

    print("=== Full-coverage MCMC rescore — 100k ensemble ===\n")
    vas = gpd.read_file(VA_GPKG)
    print(f"VA gpkg: {len(vas)} features, CRS {vas.crs}")

    # Majority
    print("\n--- Majority 2026 (full coverage) ---")
    maj_xwalk = crosswalk_dict(MAJ_XWALK_CSV_FULL)
    maj_polys = gpd.read_file(MAJ_APPROX_GPKG)
    maj_expected = set(norm(n) for n in pd.read_csv(MAJ_POPS_CSV)["ed_name"])
    maj_assigned = assign_vas_to_2026_ed(vas, maj_polys, "name_2026", maj_xwalk)
    maj_scores = score_map(maj_assigned, maj_expected)

    # Minority
    print("\n--- Minority 2026 v6 (full coverage) ---")
    min_xwalk = crosswalk_dict(MIN_XWALK_CSV_FULL)
    min_polys = gpd.read_file(MIN_V6_GPKG)
    min_expected = set(norm(n) for n in pd.read_csv(MIN_POPS_CSV)["ed_name"])
    min_assigned = assign_vas_to_2026_ed(vas, min_polys, "name_2026", min_xwalk)
    min_scores = score_map(min_assigned, min_expected)

    # 2019 enacted (full by definition)
    print("\n--- 2019 enacted (full coverage via VA parent labels) ---")
    agg_2019 = (
        vas.groupby(vas["parent_ed_2019"].apply(norm))
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    agg_2019.columns = ["ed_2019", "ucp", "ndp"]
    agg_2019["total_votes"] = agg_2019["ucp"] + agg_2019["ndp"]
    agg_2019 = agg_2019[agg_2019["total_votes"] > 0].reset_index(drop=True)
    total_ucp = int(agg_2019["ucp"].sum())
    total_ndp = int(agg_2019["ndp"].sum())
    e2019_scores = {
        "efficiency_gap": efficiency_gap(agg_2019),
        "mean_median": mean_median(agg_2019),
        "declination": declination(agg_2019),
        "seats_at_50_50": seats_at_50_50(agg_2019),
        "ucp_seats": int(
            ((agg_2019["ucp"] / (agg_2019["ucp"] + agg_2019["ndp"])) > 0.5 + 1e-9).sum()
            + ((agg_2019["ucp"] / (agg_2019["ucp"] + agg_2019["ndp"])) == 0.5).sum()
            * 0.5
        ),
        "n_districts_scored": int(len(agg_2019)),
        "n_expected": 87,
        "n_via_polygon": int(len(vas)),
        "n_via_crosswalk": 0,
        "coverage_polygon_pct": 1.0,
        "eds_missing": [],
        "eds_extra": [],
        "ucp_vote_share": float(total_ucp / (total_ucp + total_ndp)),
        "total_votes": int(total_ucp + total_ndp),
    }

    real = {
        "2019 enacted (full)": e2019_scores,
        "majority 2026 (full coverage)": maj_scores,
        "minority 2026 v6 (full coverage)": min_scores,
    }

    for lbl, s in real.items():
        print(f"\n{lbl}:")
        print(
            f"  EG={s['efficiency_gap']:+.4f}  MM={s['mean_median']:+.4f}  "
            f"DECL={s['declination']:+.4f}  S@50/50={s['seats_at_50_50']:+.4f}"
        )
        print(
            f"  UCP seats {s['ucp_seats']} / {s['n_districts_scored']} scored "
            f"(expected {s['n_expected']})"
        )
        print(
            f"  VA assignment: {s['n_via_polygon']} via polygon, "
            f"{s['n_via_crosswalk']} via crosswalk  "
            f"(polygon coverage {s['coverage_polygon_pct']*100:.1f}%)"
        )
        if s["eds_missing"]:
            print(f"  MISSING EDs ({len(s['eds_missing'])}): {s['eds_missing'][:5]}")
        if s["eds_extra"]:
            print(f"  EXTRA EDs ({len(s['eds_extra'])}): {s['eds_extra'][:5]}")

    # Percentiles
    print("\n--- Percentiles vs. 100k-plan ensemble ---")
    pct_df = compute_percentiles(ENSEMBLE_CSV_100K, real)
    with pd.option_context(
        "display.float_format",
        "{:+.4f}".format,
        "display.max_rows",
        None,
        "display.width",
        160,
    ):
        print(pct_df.to_string(index=False))

    # Flag outliers
    print("\n--- OUTLIER FLAGS (>=95th or <=5th percentile) ---")
    flagged = pct_df[(pct_df["percentile"] >= 95) | (pct_df["percentile"] <= 5)]
    if len(flagged):
        for _, r in flagged.iterrows():
            print(
                f"    {r['map']:<36s} {r['metric']:<18s} value={r['value']:+.4f}  p={r['percentile']:.1f}"
            )
    else:
        print("    (none)")

    OUT_SCORES_JSON.write_text(json.dumps(real, indent=2, default=float))
    pct_df.to_csv(OUT_PERCENTILES_CSV, index=False)
    print(f"\nWrote: {OUT_SCORES_JSON.name}")
    print(f"Wrote: {OUT_PERCENTILES_CSV.name}")


if __name__ == "__main__":
    main()
