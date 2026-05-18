"""
phase4c_canonical_attribution.py — Phase 4C: Canonical VA-polygon attribution
==============================================================================

Lane 1 (Statistical), Step 1 of 3: Spatial attribution
Chain: phase4c_canonical_attribution → packing_cracking_analysis → mcmc_ensemble_canonical

Assigns each 2023 Voting Area (VA) centroid to its 2026 Electoral District
under both canonical Elections Alberta shapefiles (received 2026-05-06). Uses
representative_point() to guarantee the centroid lies inside concave polygons,
matching the assignment method in szat.py and mcmc_ensemble_canonical.py.

This is the "Phase 4C" attribution referenced in §5.2.7 and §7.1.  It replaces
the blended-crosswalk Reading A with a direct spatial Reading B computed entirely
from official Elections Alberta geometry.

Inputs
------
data/shapefiles/canonical/va_2023_election_day_votes.gpkg   official EA VA polygons
data/shapefiles/canonical/ea_majority_2026_eds.gpkg          official EA majority EDs
data/shapefiles/canonical/ea_minority_2026_eds.gpkg          official EA minority EDs

Outputs
-------
data/outputs/phase4c_per_ed_votes_majority.csv   per-ED vote totals (majority)
data/outputs/phase4c_per_ed_votes_minority.csv   per-ED vote totals (minority)
data/outputs/phase4c_canonical_results.json      metric summary (EG, MM, d, s50)

Backward:
  data/shapefiles/canonical/va_2023_election_day_votes.gpkg
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/canonical/ea_minority_2026_eds.gpkg

Forward:
  data/outputs/phase4c_per_ed_votes_majority.csv
  data/outputs/phase4c_per_ed_votes_minority.csv
  data/outputs/phase4c_canonical_results.json
"""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
OUT = DATA / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

CANONICAL = DATA / "shapefiles" / "canonical"
VA_FILE   = CANONICAL / "va_2023_election_day_votes.gpkg"
MAJ_FILE  = CANONICAL / "ea_majority_2026_eds.gpkg"
MIN_FILE  = CANONICAL / "ea_minority_2026_eds.gpkg"


# ── Spatial join ─────────────────────────────────────────────────────────────


def _assign(va_gdf: gpd.GeoDataFrame, ed_gdf: gpd.GeoDataFrame) -> pd.Series:
    """Centroid-in-polygon assignment with nearest-ED fallback.

    Uses representative_point() (guaranteed inside polygon) consistent with
    szat.py and mcmc_ensemble_canonical.py.  Returns a Series of EDName2025
    values indexed like va_gdf.
    """
    cents = va_gdf[["geometry"]].copy()
    cents["geometry"] = va_gdf.geometry.representative_point()

    joined = gpd.sjoin(
        cents, ed_gdf[["EDName2025", "geometry"]], how="left", predicate="within"
    )

    unresolved = joined["EDName2025"].isna()
    n_unresolved = int(unresolved.sum())
    if n_unresolved > 0:
        nearest = gpd.sjoin_nearest(
            cents.loc[unresolved.values],
            ed_gdf[["EDName2025", "geometry"]],
            how="left",
        )
        joined.loc[unresolved.values, "EDName2025"] = nearest["EDName2025"].values
        print(f"    Nearest-ED fallback: {n_unresolved} centroids")

    return joined["EDName2025"]


# ── Metric computation ────────────────────────────────────────────────────────


def _eg(ed: pd.DataFrame) -> float:
    """Efficiency gap (continuous threshold = total/2).

    Sign: positive = NDP wastes more votes = UCP structural advantage.
    """
    total_prov = (ed["ndp"] + ed["ucp"]).sum()
    if total_prov == 0:
        return 0.0
    wn = wu = 0.0
    for _, row in ed.iterrows():
        n, u = float(row["ndp"]), float(row["ucp"])
        t = n + u
        if t == 0:
            continue
        thresh = t / 2.0
        if n >= u:
            wn += max(0.0, n - thresh)
            wu += u
        else:
            wu += max(0.0, u - thresh)
            wn += n
    return (wn - wu) / total_prov


def _mm(ed: pd.DataFrame) -> float:
    """Mean-median gap on NDP two-party share.

    Positive = mean > median = NDP voters packed / cracked against.
    """
    total = ed["ndp"] + ed["ucp"]
    mask = total > 0
    shares = (ed.loc[mask, "ndp"] / total[mask]).values
    if len(shares) == 0:
        return 0.0
    return float(np.mean(shares) - np.median(shares))


def _declination(ed: pd.DataFrame) -> float:
    """Warrington (2018) declination.

    Matches the packing_cracking_analysis.py implementation exactly:
      theta_ndp = atan2(mean_ndp_won - 0.5, n_ndp_wins / n)
      theta_ucp = atan2(0.5 - mean_ucp_won, n_ucp_wins / n)
      delta     = (theta_ndp - theta_ucp) * 2/pi

    Positive = pro-NDP (NDP wins with tighter margins = less packing).
    """
    total = ed["ndp"] + ed["ucp"]
    mask = total > 0
    shares = (ed.loc[mask, "ndp"] / total[mask]).values
    n = len(shares)
    if n == 0:
        return float("nan")

    ndp_won = shares[shares > 0.5]
    ucp_won = shares[shares < 0.5]
    n_ndp = len(ndp_won)
    n_ucp = len(ucp_won)

    if n_ndp == 0 or n_ucp == 0:
        return float("nan")

    mean_ndp_won = float(np.mean(ndp_won))
    mean_ucp_won = float(np.mean(ucp_won))

    theta_ndp = np.arctan2(mean_ndp_won - 0.5, n_ndp / n)
    theta_ucp = np.arctan2(0.5 - mean_ucp_won, n_ucp / n)
    return float((theta_ndp - theta_ucp) * 2.0 / np.pi)


def _seats_at_50(ed: pd.DataFrame) -> float:
    """Uniform-swing seats fraction at exact 50/50 provincial split.

    Delta is calibrated to the *provincial* NDP two-party share (vote-weighted),
    not the equal-weight mean of per-ED shares.  The two differ because
    Alberta's rural districts are more numerous and more UCP-heavy than the
    population-weighted average.  Using the provincial total matches the
    packing_cracking_analysis.py and MCMC scoring convention.

    Returns NDP seat fraction (0.0 – 1.0).

    Convention note: this function returns the *NDP* seat fraction.
    data/outputs/simulation_real_map_scores_canonical.json uses the *UCP*
    seat fraction.  For majority 2026: Phase 4C NDP=0.5393 = 1 − canonical
    UCP=0.4607.  The two are consistent; they use opposite party references.
    """
    total = ed["ndp"] + ed["ucp"]
    mask = total > 0
    shares = (ed.loc[mask, "ndp"] / total[mask]).values
    if len(shares) == 0:
        return 0.5
    # Provincial (vote-weighted) NDP two-party share:
    prov_ndp_share = float(ed["ndp"].sum() / total.sum())
    delta = 0.5 - prov_ndp_share
    shifted = np.clip(shares + delta, 0.0, 1.0)
    return float((shifted > 0.5).sum() / len(shares))


def _compute_all(per_ed: pd.DataFrame) -> dict:
    return {
        "eg":           round(_eg(per_ed), 6),
        "mean_median":  round(_mm(per_ed), 6),
        "declination":  round(_declination(per_ed), 6),
        "seats_at_50":  round(_seats_at_50(per_ed), 6),
        "n_eds":        int(len(per_ed)),
        "total_ndp":    int(per_ed["ndp"].sum()),
        "total_ucp":    int(per_ed["ucp"].sum()),
        "total_other":  int(per_ed["other"].sum()),
    }


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    t0 = time.time()
    for f in (VA_FILE, MAJ_FILE, MIN_FILE):
        if not f.exists():
            sys.exit(f"ERROR: {f} not found — check canonical shapefile directory.")

    print("Phase 4C canonical attribution")
    print(f"  VA file:       {VA_FILE.name}")
    print(f"  Majority EDs:  {MAJ_FILE.name}")
    print(f"  Minority EDs:  {MIN_FILE.name}")
    print()

    va  = gpd.read_file(VA_FILE)
    maj = gpd.read_file(MAJ_FILE)
    min_ = gpd.read_file(MIN_FILE)

    print(f"  VAs: {len(va)}  |  Majority EDs: {len(maj)}  |  Minority EDs: {len(min_)}")
    print()

    results = {}
    for label, ed_gdf, out_csv in (
        ("majority", maj, OUT / "phase4c_per_ed_votes_majority.csv"),
        ("minority", min_, OUT / "phase4c_per_ed_votes_minority.csv"),
    ):
        print(f"Assigning VAs -> {label} EDs ...")
        t1 = time.time()
        assignment = _assign(va, ed_gdf)
        print(f"  done in {time.time()-t1:.1f}s")

        va_copy = va.copy()
        va_copy["ed_2026"] = assignment.values

        per_ed = (
            va_copy.groupby("ed_2026")
            .agg(
                ndp=("va_ndp", "sum"),
                ucp=("va_ucp", "sum"),
                other=("va_other", "sum"),
                n_vas=("VA_NUMBER", "count"),
            )
            .reset_index()
            .rename(columns={"ed_2026": "ed_name"})
        )

        # Add population from canonical ED file for reference
        pop_map = dict(zip(ed_gdf["EDName2025"], ed_gdf["PopCensus"]))
        per_ed["pop_census"] = per_ed["ed_name"].map(pop_map).fillna(0).astype(int)
        per_ed["ndp_share"] = (per_ed["ndp"] / (per_ed["ndp"] + per_ed["ucp"])).round(6)

        per_ed.to_csv(out_csv, index=False)
        print(f"  -> {out_csv.name}  ({len(per_ed)} EDs, {int(per_ed['ndp'].sum()+per_ed['ucp'].sum()):,} two-party votes)")

        metrics = _compute_all(per_ed)
        results[label] = metrics
        print(f"  EG={metrics['eg']:+.4f}  MM={metrics['mean_median']:+.4f}  "
              f"declination={metrics['declination']:+.4f}  seats@50={metrics['seats_at_50']:.4f}")
        print()

    # Derived comparison
    results["comparison"] = {
        "eg_gap_minority_minus_majority":        round(results["minority"]["eg"]          - results["majority"]["eg"],         6),
        "mm_gap_minority_minus_majority":        round(results["minority"]["mean_median"] - results["majority"]["mean_median"], 6),
        "seats50_gap_minority_minus_majority":   round(results["minority"]["seats_at_50"] - results["majority"]["seats_at_50"], 6),
        "note": (
            "positive gap = minority more UCP-favourable than majority "
            "(EG convention: positive EG = UCP structural advantage)"
        ),
    }

    out_json = OUT / "phase4c_canonical_results.json"
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Summary -> {out_json.name}")
    print(f"Total elapsed: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
