"""Validation pass: rescore against the 10k ensemble using the canonical
shapefiles and the full-vote VA substrate (Election-Day + splat).

Supersedes the earlier v2 which used approximate_majority / refined_v6_minority
polygons and the Election-Day-only VA gpkg. The new inputs close the 52.5%
vote-recovery gap (two-party now sums to ~1,706,249 per map vs the 1,706,304
target) and use the session-11 canonical 89-ED coverage per map.

Writes to data/v0_1_mcmc_real_map_scores_full_v2.json and
data/v0_1_mcmc_ensemble_percentiles_full_v2.csv.
"""
from __future__ import annotations
import json
from pathlib import Path

# Reuse the 100k-targeted script's scoring logic but swap inputs
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from v0_1_mcmc_full_coverage_rescore_100k import (
    assign_vas_to_2026_ed, score_map, compute_percentiles,
    crosswalk_dict, norm,
    MAJ_POPS_CSV, MIN_POPS_CSV,
    MAJ_XWALK_CSV_FULL, MIN_XWALK_CSV_FULL, DATA,
    efficiency_gap, mean_median, declination, seats_at_50_50,
)
import geopandas as gpd
import pandas as pd

MAJ_CANON_GPKG = DATA / "v0_1_canonical_majority_2026_eds.gpkg"
MIN_CANON_GPKG = DATA / "v0_1_canonical_minority_2026_eds.gpkg"
VA_GPKG_FULL = DATA / "va_polygons_with_full_2023_votes.gpkg"

ENSEMBLE_10K = DATA / "v0_1_mcmc_ensemble_samples.csv"
OUT_SCORES_JSON = DATA / "v0_1_mcmc_real_map_scores_full_v2.json"
OUT_PERCENTILES_CSV = DATA / "v0_1_mcmc_ensemble_percentiles_full_v2.csv"


def main():
    print("=== Validation: canonical + full-VA rescore vs 10k ensemble ===\n")
    vas = gpd.read_file(VA_GPKG_FULL)
    # Upstream score_map() reads va_ucp / va_ndp / va_other. The full-VA gpkg
    # also carries the original Election-Day-only columns under those names;
    # drop them and alias the _full columns so scoring is unchanged.
    vas = vas.drop(columns=["va_ucp", "va_ndp", "va_other"], errors="ignore")
    vas = vas.rename(columns={
        "va_ucp_full": "va_ucp",
        "va_ndp_full": "va_ndp",
        "va_other_full": "va_other",
    })
    two_party = float(vas["va_ucp"].sum()) + float(vas["va_ndp"].sum())
    print(f"VA gpkg: {len(vas)} features; two-party total={two_party:,.0f}")

    print("\n--- Majority 2026 (canonical) ---")
    maj_xwalk = crosswalk_dict(MAJ_XWALK_CSV_FULL)
    maj_polys = gpd.read_file(MAJ_CANON_GPKG)
    maj_expected = set(norm(n) for n in pd.read_csv(MAJ_POPS_CSV)["ed_name"])
    maj_assigned = assign_vas_to_2026_ed(vas, maj_polys, "name_2026", maj_xwalk)
    maj_scores = score_map(maj_assigned, maj_expected)

    print("\n--- Minority 2026 (canonical) ---")
    min_xwalk = crosswalk_dict(MIN_XWALK_CSV_FULL)
    min_polys = gpd.read_file(MIN_CANON_GPKG)
    min_expected = set(norm(n) for n in pd.read_csv(MIN_POPS_CSV)["ed_name"])
    min_assigned = assign_vas_to_2026_ed(vas, min_polys, "name_2026", min_xwalk)
    min_scores = score_map(min_assigned, min_expected)

    print("\n--- 2019 enacted (full) ---")
    agg_2019 = vas.groupby(vas["parent_ed_2019"].apply(norm)).agg(
        ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum")).reset_index()
    agg_2019.columns = ["ed_2019", "ucp", "ndp"]
    agg_2019 = agg_2019[(agg_2019["ucp"] + agg_2019["ndp"]) > 0].reset_index(drop=True)
    total_ucp = int(agg_2019["ucp"].sum())
    total_ndp = int(agg_2019["ndp"].sum())
    e2019_scores = {
        "efficiency_gap": efficiency_gap(agg_2019),
        "mean_median": mean_median(agg_2019),
        "declination": declination(agg_2019),
        "seats_at_50_50": seats_at_50_50(agg_2019),
        "ucp_seats": int(((agg_2019["ucp"] / (agg_2019["ucp"] + agg_2019["ndp"])) > 0.5).sum()),
        "n_districts_scored": int(len(agg_2019)),
        "n_expected": 87,
        "n_via_polygon": int(len(vas)),
        "n_via_crosswalk": 0,
        "coverage_polygon_pct": 1.0,
        "eds_missing": [],
        "eds_extra": [],
        "ucp_vote_share": float(total_ucp / (total_ucp + total_ndp)),
    }

    real = {
        "2019 enacted (full)": e2019_scores,
        "majority 2026 (canonical, full-VA)": maj_scores,
        "minority 2026 (canonical, full-VA)": min_scores,
    }

    for lbl, s in real.items():
        print(f"\n{lbl}:")
        print(f"  EG={s['efficiency_gap']:+.4f}  MM={s['mean_median']:+.4f}  "
              f"DECL={s['declination']:+.4f}  S@50/50={s['seats_at_50_50']:+.4f}")
        print(f"  UCP seats {s['ucp_seats']} / {s['n_districts_scored']} scored "
              f"(expected {s['n_expected']})")
        print(f"  VA assign: {s['n_via_polygon']} polygon, "
              f"{s['n_via_crosswalk']} crosswalk  (cov {s['coverage_polygon_pct']*100:.1f}%)")
        if s["eds_missing"]:
            print(f"  MISSING ({len(s['eds_missing'])}): {s['eds_missing'][:5]}")
        if s["eds_extra"]:
            print(f"  EXTRA ({len(s['eds_extra'])}): {s['eds_extra'][:5]}")

    print("\n--- Percentiles vs. 10k ensemble ---")
    pct_df = compute_percentiles(ENSEMBLE_10K, real)
    with pd.option_context("display.float_format", "{:+.4f}".format,
                           "display.max_rows", None, "display.width", 160):
        print(pct_df.to_string(index=False))

    OUT_SCORES_JSON.write_text(json.dumps(real, indent=2, default=float))
    pct_df.to_csv(OUT_PERCENTILES_CSV, index=False)
    print(f"\nWrote: {OUT_SCORES_JSON.name}")
    print(f"Wrote: {OUT_PERCENTILES_CSV.name}")


if __name__ == "__main__":
    main()
