"""
Phase 4C (MAUP) — Area-weighted VA-level vote attribution for 2026 ED maps
===========================================================================
MAUP (Modifiable Areal Unit Problem) alternative to the centroid-in-polygon
attribution used in `v0_1_assignment_va_attribution.py` /
`v0_1_phase_4bcdef_execution.py`.

**Motivation.** The existing Phase 4C pipeline assigns each VA wholesale
to a single 2026 ED based on the VA polygon's representative_point()
(centroid). When a VA polygon straddles a DPG ED boundary, 100 % of its
votes go to whichever side the centroid lands on — even if only 30 % of
the VA's area is in that ED. That systematically biases vote attribution
for boundary-straddling VAs.

**Method.** For each VA, intersect the VA polygon with every 2026 ED
polygon, compute the fractional overlap (intersection_area / va_area),
and apportion the VA's full 2023 votes to each ED by that fractional
weight. A VA entirely inside one ED contributes 1.0 × votes to that ED;
a VA split 60/40 between two EDs contributes 0.6 × and 0.4 × votes
respectively. Crosswalk fallback (parent_ed_2019 → proposed_2026) is
applied for the uncovered area fraction — VAs falling in DPG gaps
(Tier-C transcription artifacts) or extending outside Alberta.

Inputs (read-only):
  data/va_polygons_with_full_2023_votes.gpkg
  data/v0_1_canonical_majority_2026_eds.gpkg
  data/v0_1_canonical_minority_2026_eds.gpkg
  data/majority_full_crosswalk.csv
  data/minority_full_crosswalk.csv
  data/majority_2026_populations.csv   (for canonical ED name order)
  data/minority_2026_populations.csv

Outputs:
  data/v0_1_votes_2023_majority_maup.csv
  data/v0_1_votes_2023_minority_maup.csv
  analysis/reports/assignment_va_to_2026_assignments_maup.csv
  analysis/reports/v0_1_phase4c_maup_summary.json

Forward: analysis/reports/maup_area_weighted_analysis.md
Backward:
  analysis/scripts/v0_1_assignment_va_attribution.py    (centroid pipeline)
  analysis/scripts/v0_1_phase_4bcdef_execution.py     (centroid pipeline)
  data/va_polygons_with_full_2023_votes.gpkg
  data/v0_1_canonical_majority_2026_eds.gpkg
  data/v0_1_canonical_minority_2026_eds.gpkg
"""
# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
import unicodedata
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"

VA_GPKG = DATA / "shapefiles" / "derived" / "va_polygons_with_full_2023_votes.gpkg"
MAJ_CANON_GPKG = DATA / "shapefiles" / "derived" / "v0_1_canonical_majority_2026_eds.gpkg"
MIN_CANON_GPKG = DATA / "shapefiles" / "derived" / "v0_1_canonical_minority_2026_eds.gpkg"
MAJ_XWALK_CSV = DATA / "majority_full_crosswalk.csv"
MIN_XWALK_CSV = DATA / "minority_full_crosswalk.csv"
MAJ_POPS_CSV = DATA / "majority_2026_populations.csv"
MIN_POPS_CSV = DATA / "minority_2026_populations.csv"

OUT_MAJ = DATA / "v0_1_votes_2023_majority_maup.csv"
OUT_MIN = DATA / "v0_1_votes_2023_minority_maup.csv"
OUT_PER_VA = ANALYSIS / "reports" / "assignment_va_to_2026_assignments_maup.csv"
OUT_SUMMARY = ANALYSIS / "reports" / "v0_1_phase4c_maup_summary.json"

# §5.2.7 centroid-based EG (headline measurement) — for direct comparison
CENTROID_MAJORITY_EG = -0.0233
CENTROID_MINORITY_EG = +0.0182
CENTROID_ASYMMETRY_PP = +4.15


def norm(s) -> str:
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return ""
    s = str(s).strip()
    s = s.replace("‘", "'").replace("’", "'")
    return unicodedata.normalize("NFC", s)


def load_crosswalk(path: Path) -> dict[str, str]:
    df = pd.read_csv(path)
    return {norm(r["current_2019"]): norm(r["proposed_2026"]) for _, r in df.iterrows()}


def load_canonical(path: Path, target_crs) -> gpd.GeoDataFrame:
    g = gpd.read_file(path)
    if g.crs != target_crs:
        g = g.to_crs(target_crs)
    g = g[g.geometry.notna() & ~g.geometry.is_empty].copy()
    # Clean up any invalid polygons with zero-buffer trick
    g["geometry"] = g.geometry.buffer(0)
    g["name_2026_norm"] = g["name_2026"].apply(norm)
    return g[["name_2026", "name_2026_norm", "geometry"]]


def compute_area_weights(
    vas: gpd.GeoDataFrame,
    eds: gpd.GeoDataFrame,
    label: str,
) -> tuple[pd.DataFrame, dict]:
    """Compute per-(VA, ED) area-weighted overlap fractions.

    Steps
    -----
    1. Intersect VAs with ED polygons via gpd.overlay(how='intersection').
    2. Compute intersection_area / va_total_area = area weight.
    3. Ensure sum of weights per VA ≤ 1.0 (remainder = uncovered by DPG).
    4. Normalise column names and return (weights_df, coverage_stats).

    Parameters
    ----------
    vas : GeoDataFrame with OBJECTID, VA_NUMBER, parent_ed_2019, geometry,
           va_{ndp,ucp,other}_full.
    eds : GeoDataFrame with name_2026 + geometry.
    label : map label for logging.

    Returns
    -------
    weights_df : DataFrame of (OBJECTID, VA_NUMBER, parent_ed_2019,
                 name_2026, area_weight, va_area, intersection_area).
    stats : dict with coverage metrics.
    """
    print(f"  [{label}] Computing VA × ED intersection ({len(vas)} VAs × {len(eds)} EDs)...")
    t0 = time.time()

    # Pre-compute VA total area
    va_areas = vas.geometry.area
    if not (va_areas > 0).all():
        n_zero = int((va_areas <= 0).sum())
        print(f"    WARNING: {n_zero} VAs have zero/negative area; they will get weight 0.")

    va_slim = vas[["OBJECTID", "VA_NUMBER", "parent_ed_2019", "geometry"]].copy()
    va_slim["va_area"] = va_areas.values

    # Intersect. gpd.overlay is O(n_va * n_eds_touching) with spatial index.
    inter = gpd.overlay(
        va_slim,
        eds[["name_2026", "geometry"]],
        how="intersection",
        keep_geom_type=False,
    )
    # Keep polygonal components only (overlay may yield linestrings/points on edges)
    inter = inter[inter.geometry.geom_type.isin(["Polygon", "MultiPolygon"])].copy()
    inter["intersection_area"] = inter.geometry.area
    inter = inter[inter["intersection_area"] > 0].copy()
    inter["area_weight"] = inter["intersection_area"] / inter["va_area"]

    print(f"  [{label}] overlay returned {len(inter):,} (VA, ED) intersection rows "
          f"in {time.time()-t0:.1f}s")

    # Per-VA coverage = sum of weights (bounded by 1.0). Anything < 1 = uncovered area.
    per_va_cover = inter.groupby("OBJECTID", as_index=False)["area_weight"].sum()
    per_va_cover.rename(columns={"area_weight": "dpg_coverage_frac"}, inplace=True)

    # Clamp: sum of weights can exceed 1.0 by tiny numeric noise. Clip in the
    # conservation step, not here, so that per-row weights stay faithful to the
    # actual geometric overlap.
    if (per_va_cover["dpg_coverage_frac"] > 1.0001).any():
        over = per_va_cover[per_va_cover["dpg_coverage_frac"] > 1.0001]
        print(f"    WARNING: {len(over)} VAs have total DPG coverage > 1.0001 "
              f"(max = {over['dpg_coverage_frac'].max():.4f}). "
              f"Likely due to overlapping DPG polygons — normalising weights.")
        # Normalise those specific VAs' weights so they sum to ≤ 1.0
        over_ids = set(over["OBJECTID"].tolist())
        if over_ids:
            mask = inter["OBJECTID"].isin(over_ids)
            inter.loc[mask, "area_weight"] = (
                inter.loc[mask].groupby("OBJECTID")["area_weight"]
                .transform(lambda w: w / w.sum() if w.sum() > 0 else w)
            )
            # Re-compute coverage after normalisation (will equal 1.0 for those)
            per_va_cover = inter.groupby("OBJECTID", as_index=False)["area_weight"].sum()
            per_va_cover.rename(columns={"area_weight": "dpg_coverage_frac"}, inplace=True)

    # Attach full VA geometry area as total denominator (already available)
    inter_df = inter[[
        "OBJECTID", "VA_NUMBER", "parent_ed_2019", "name_2026",
        "va_area", "intersection_area", "area_weight",
    ]].copy()

    # Coverage stats — use post-normalisation per-VA weight sums, clamped at 1.0
    va_area_total = float(vas.geometry.area.sum())
    per_va_cov = pd.merge(
        vas[["OBJECTID"]].assign(va_area=vas.geometry.area),
        per_va_cover, on="OBJECTID", how="left",
    ).fillna({"dpg_coverage_frac": 0.0})
    # Clamp per-VA coverage at 1.0 (overlapping DPG polygons can push raw sum >1)
    per_va_cov["dpg_coverage_frac"] = per_va_cov["dpg_coverage_frac"].clip(upper=1.0)
    # VA-area-weighted coverage fraction (what fraction of total VA area is covered by DPG)
    va_area_weighted_cov = float(
        (per_va_cov["va_area"] * per_va_cov["dpg_coverage_frac"]).sum() / va_area_total
    )
    coverage_area_frac = va_area_weighted_cov  # same thing, by definition
    n_full = int((per_va_cov["dpg_coverage_frac"] >= 0.9999).sum())
    n_zero = int((per_va_cov["dpg_coverage_frac"] < 1e-6).sum())
    n_partial = len(per_va_cov) - n_full - n_zero

    stats = {
        "n_vas": len(vas),
        "n_rows_overlay": len(inter_df),
        "dpg_area_coverage_frac": coverage_area_frac,
        "va_area_weighted_coverage_frac": va_area_weighted_cov,
        "n_vas_fully_covered": n_full,
        "n_vas_partial_cover": n_partial,
        "n_vas_zero_cover": n_zero,
    }
    print(f"  [{label}] DPG area coverage (of VA substrate): "
          f"{coverage_area_frac*100:.2f}%")
    print(f"  [{label}] n VAs fully covered: {n_full}  partial: {n_partial}  "
          f"zero cover: {n_zero}")

    return inter_df, stats


def apply_crosswalk_fallback(
    inter_df: pd.DataFrame,
    vas: gpd.GeoDataFrame,
    xwalk: dict[str, str],
    ed_names: set[str],
    label: str,
) -> pd.DataFrame:
    """For VA area not covered by any DPG polygon, add a crosswalk-fallback row.

    For each VA, (1 - sum(area_weight)) is the uncovered fraction. If > 1e-6,
    add a row with that weight assigned to parent_ed_2019 → crosswalk'd 2026 ED.
    This ensures conservation: per-VA weights always sum to 1.0.
    """
    per_va_cover = inter_df.groupby("OBJECTID", as_index=False)["area_weight"].sum()
    per_va_cover.rename(columns={"area_weight": "dpg_coverage_frac"}, inplace=True)

    merged = vas[["OBJECTID", "VA_NUMBER", "parent_ed_2019"]].merge(
        per_va_cover, on="OBJECTID", how="left",
    ).fillna({"dpg_coverage_frac": 0.0})
    merged["uncovered"] = 1.0 - merged["dpg_coverage_frac"]
    need_fb = merged[merged["uncovered"] > 1e-6].copy()

    # Crosswalk parent_ed_2019 → 2026 ED
    need_fb["_pkey"] = need_fb["parent_ed_2019"].apply(norm)
    need_fb["name_2026"] = need_fb["_pkey"].map(xwalk)
    # Fallback to parent itself if not in crosswalk (some 1:1 renames may miss)
    need_fb["name_2026"] = need_fb["name_2026"].fillna(need_fb["_pkey"])

    # Count crosswalk targets outside the valid 2026 ED name set
    norm_ed_names = {norm(n) for n in ed_names}
    bad = need_fb[~need_fb["name_2026"].apply(norm).isin(norm_ed_names)]
    if len(bad) > 0:
        print(f"    [{label}] WARNING: {len(bad)} fallback rows point to a "
              f"2026 ED name not in canonical list. Examples: "
              f"{bad['name_2026'].unique()[:5].tolist()}")

    # Build fallback rows matching the inter_df schema
    vas_idx = vas.set_index("OBJECTID")
    need_fb["va_area"] = need_fb["OBJECTID"].map(lambda o: vas_idx.loc[o].geometry.area)
    need_fb["intersection_area"] = need_fb["va_area"] * need_fb["uncovered"]
    need_fb["area_weight"] = need_fb["uncovered"]
    need_fb["fallback"] = True

    fb_rows = need_fb[[
        "OBJECTID", "VA_NUMBER", "parent_ed_2019", "name_2026",
        "va_area", "intersection_area", "area_weight",
    ]].copy()
    fb_rows["fallback"] = True
    inter_df = inter_df.copy()
    inter_df["fallback"] = False
    combined = pd.concat([inter_df, fb_rows], ignore_index=True)

    n_fb = len(fb_rows)
    fb_mass = float(fb_rows["area_weight"].sum())
    total_mass = float(combined["area_weight"].sum())
    print(f"  [{label}] crosswalk-fallback rows: {n_fb}  "
          f"fallback weight mass: {fb_mass:.2f}  "
          f"total weight mass (should be ~{len(vas)}): {total_mass:.2f}")
    return combined


def apportion_votes(
    weights_df: pd.DataFrame,
    vas: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """Apportion each VA's full votes to (VA, ED) rows by area_weight.

    Input:  weights_df with area_weight (each VA's weights should sum to 1.0
            after fallback). vas with va_{ndp,ucp,other}_full.

    Returns: weights_df augmented with va_ndp_full_share / va_ucp_full_share /
             va_other_full_share (raw vote counts = weight × full vote).
    """
    votes = vas[["OBJECTID", "va_ndp_full", "va_ucp_full", "va_other_full"]].copy()
    df = weights_df.merge(votes, on="OBJECTID", how="left")
    df["va_ndp_full_share"] = df["area_weight"] * df["va_ndp_full"].fillna(0)
    df["va_ucp_full_share"] = df["area_weight"] * df["va_ucp_full"].fillna(0)
    df["va_other_full_share"] = df["area_weight"] * df["va_other_full"].fillna(0)
    return df


def conservation_gate(apportioned: pd.DataFrame, vas: gpd.GeoDataFrame,
                      label: str) -> dict:
    """Verify per-VA conservation: sum of apportioned votes == original VA votes."""
    gb = apportioned.groupby("OBJECTID").agg(
        ndp_sum=("va_ndp_full_share", "sum"),
        ucp_sum=("va_ucp_full_share", "sum"),
        other_sum=("va_other_full_share", "sum"),
        w_sum=("area_weight", "sum"),
    ).reset_index()
    orig = vas[["OBJECTID", "va_ndp_full", "va_ucp_full", "va_other_full"]].copy()
    m = gb.merge(orig, on="OBJECTID", how="outer")
    # Fill any missing (VA with zero area or zero weight) with 0 on apportioned side
    m = m.fillna({"ndp_sum": 0, "ucp_sum": 0, "other_sum": 0, "w_sum": 0})
    m["delta_ndp"] = m["ndp_sum"] - m["va_ndp_full"].fillna(0)
    m["delta_ucp"] = m["ucp_sum"] - m["va_ucp_full"].fillna(0)
    m["delta_other"] = m["other_sum"] - m["va_other_full"].fillna(0)
    m["delta_w"] = m["w_sum"] - 1.0

    max_delta_ndp = float(m["delta_ndp"].abs().max())
    max_delta_ucp = float(m["delta_ucp"].abs().max())
    max_delta_other = float(m["delta_other"].abs().max())
    max_delta_w = float(m["delta_w"].abs().max())

    worst_va = m.loc[m["delta_ucp"].abs().idxmax()]
    passed = (max_delta_ndp < 1.0 and max_delta_ucp < 1.0 and max_delta_other < 1.0)
    print(f"  [{label}] Conservation gate: "
          f"max |Δndp|={max_delta_ndp:.4f}, "
          f"max |Δucp|={max_delta_ucp:.4f}, "
          f"max |Δother|={max_delta_other:.4f}, "
          f"max |Δw|={max_delta_w:.6f}  "
          f"{'PASS' if passed else 'FAIL'}")
    if not passed:
        print(f"    worst VA: OBJECTID={int(worst_va['OBJECTID'])}, "
              f"Δucp={worst_va['delta_ucp']:.2f}")
    return {
        "pass": bool(passed),
        "max_delta_ndp": max_delta_ndp,
        "max_delta_ucp": max_delta_ucp,
        "max_delta_other": max_delta_other,
        "max_delta_weight": max_delta_w,
    }


def aggregate_to_ed(apportioned: pd.DataFrame, ed_names: list[str]) -> pd.DataFrame:
    """Sum apportioned votes by 2026 ED, in canonical name order."""
    apportioned = apportioned.copy()
    apportioned["_name_norm"] = apportioned["name_2026"].apply(norm)
    agg = apportioned.groupby("_name_norm", as_index=False).agg(
        ucp=("va_ucp_full_share", "sum"),
        ndp=("va_ndp_full_share", "sum"),
        other=("va_other_full_share", "sum"),
    )
    rows = []
    for n in ed_names:
        nm = norm(n)
        sub = agg[agg["_name_norm"] == nm]
        if len(sub) == 0:
            rows.append({"ed_name": n, "ucp_2023": 0.0, "ndp_2023": 0.0,
                         "other_2023": 0.0, "total_votes": 0.0})
        else:
            u, d, o = float(sub["ucp"].iloc[0]), float(sub["ndp"].iloc[0]), float(sub["other"].iloc[0])
            rows.append({"ed_name": n, "ucp_2023": u, "ndp_2023": d,
                         "other_2023": o, "total_votes": u + d + o})
    df = pd.DataFrame(rows)
    return df


def compute_eg(districts_df: pd.DataFrame) -> float:
    """Compute efficiency gap from per-district (ndp, ucp) totals.

    Matches the formula in v0_1_phase_4c_va_attribution.compute_metrics:
      - per-district threshold = floor(two-party / 2) + 1
      - winner wasted = votes - threshold
      - loser wasted = votes
      - EG = (NDP_wasted - UCP_wasted) / total_two_party
    """
    ndp_wasted = 0.0
    ucp_wasted = 0.0
    total = 0.0
    for _, d in districts_df.iterrows():
        n_ = float(d["ndp"])
        u_ = float(d["ucp"])
        tt = n_ + u_
        if tt <= 0:
            continue
        thr = tt // 2 + 1  # integer-style threshold (matches centroid pipeline)
        if n_ > u_:
            ndp_wasted += max(0.0, n_ - thr)
            ucp_wasted += u_
        else:
            ucp_wasted += max(0.0, u_ - thr)
            ndp_wasted += n_
        total += tt
    return (ndp_wasted - ucp_wasted) / total if total > 0 else float("nan")


def compute_mm_gap(districts_df: pd.DataFrame) -> float:
    shares = [float(d["ndp"]) / (float(d["ndp"]) + float(d["ucp"]))
              for _, d in districts_df.iterrows()
              if float(d["ndp"]) + float(d["ucp"]) > 0]
    if not shares:
        return float("nan")
    return statistics.mean(shares) - statistics.median(shares)


def compute_seats(districts_df: pd.DataFrame) -> tuple[int, int]:
    ndp_wins = int(((districts_df["ndp"] > districts_df["ucp"])).sum())
    ucp_wins = int(((districts_df["ucp"] >= districts_df["ndp"])).sum())
    return ndp_wins, ucp_wins


def run_one_map(vas: gpd.GeoDataFrame, eds: gpd.GeoDataFrame,
                xwalk: dict[str, str], ed_names: list[str],
                label: str, smoke_n: int | None = None) -> dict:
    if smoke_n is not None:
        vas_run = vas.iloc[:smoke_n].copy()
        print(f"  [{label}] SMOKE MODE: running on first {len(vas_run)} VAs")
    else:
        vas_run = vas

    # 1. Area-weighted intersection
    weights_df, cov_stats = compute_area_weights(vas_run, eds, label)

    # 2. Crosswalk fallback for uncovered area
    weights_full = apply_crosswalk_fallback(weights_df, vas_run, xwalk,
                                            set(ed_names), label)

    # 3. Apportion votes
    apportioned = apportion_votes(weights_full, vas_run)

    # 4. Conservation gate
    cons = conservation_gate(apportioned, vas_run, label)

    # 5. Aggregate to 2026 EDs
    ed_totals = aggregate_to_ed(apportioned, ed_names)
    two_party = float(ed_totals["ucp_2023"].sum() + ed_totals["ndp_2023"].sum())
    print(f"  [{label}] per-ED aggregated: UCP={ed_totals['ucp_2023'].sum():,.1f}  "
          f"NDP={ed_totals['ndp_2023'].sum():,.1f}  "
          f"two-party={two_party:,.1f}")

    # 6. Metrics
    eg = compute_eg(ed_totals.rename(columns={"ndp_2023": "ndp", "ucp_2023": "ucp"}))
    mm = compute_mm_gap(ed_totals.rename(columns={"ndp_2023": "ndp", "ucp_2023": "ucp"}))
    ndp_seats, ucp_seats = compute_seats(ed_totals.rename(columns={"ndp_2023": "ndp", "ucp_2023": "ucp"}))
    print(f"  [{label}] EG (area-weighted) = {eg*100:+.4f}%   "
          f"mean-median = {mm*100:+.4f} pp   seats NDP/UCP = {ndp_seats}/{ucp_seats}")

    return {
        "label": label,
        "coverage": cov_stats,
        "conservation": cons,
        "two_party_total": two_party,
        "ed_totals": ed_totals,
        "apportioned": apportioned,
        "eg": float(eg),
        "mm_gap": float(mm),
        "ndp_seats": int(ndp_seats),
        "ucp_seats": int(ucp_seats),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", type=int, default=None,
                        help="If set, run on first N VAs only (for debugging).")
    args = parser.parse_args()

    print("=" * 72)
    print("  Phase 4C (MAUP) — Area-weighted VA vote attribution for 2026 EDs")
    print("  Alternative to centroid-in-polygon (preserves boundary-straddling mass)")
    print("=" * 72)

    print("\n[load] VA polygons with full 2023 votes...")
    vas = gpd.read_file(VA_GPKG)
    print(f"  VAs: {len(vas)}  "
          f"UCP_full={vas['va_ucp_full'].sum():,.0f}  "
          f"NDP_full={vas['va_ndp_full'].sum():,.0f}  "
          f"other_full={vas['va_other_full'].sum():,.0f}  "
          f"two-party={vas['va_ucp_full'].sum() + vas['va_ndp_full'].sum():,.0f}")

    print("\n[load] canonical 2026 ED shapefiles...")
    maj_eds = load_canonical(MAJ_CANON_GPKG, vas.crs)
    min_eds = load_canonical(MIN_CANON_GPKG, vas.crs)
    print(f"  Majority: {len(maj_eds)} EDs    Minority: {len(min_eds)} EDs")

    print("\n[load] crosswalks + canonical ED name order...")
    maj_xwalk = load_crosswalk(MAJ_XWALK_CSV)
    min_xwalk = load_crosswalk(MIN_XWALK_CSV)
    maj_names = pd.read_csv(MAJ_POPS_CSV)["ed_name"].tolist()
    min_names = pd.read_csv(MIN_POPS_CSV)["ed_name"].tolist()

    # ==== MAJORITY ====
    print("\n" + "=" * 72)
    print("  MAJORITY map")
    print("=" * 72)
    t0 = time.time()
    maj = run_one_map(vas, maj_eds, maj_xwalk, maj_names, "majority",
                      smoke_n=args.smoke)
    print(f"  [majority elapsed: {time.time()-t0:.1f}s]")

    # ==== MINORITY ====
    print("\n" + "=" * 72)
    print("  MINORITY map")
    print("=" * 72)
    t1 = time.time()
    mino = run_one_map(vas, min_eds, min_xwalk, min_names, "minority",
                       smoke_n=args.smoke)
    print(f"  [minority elapsed: {time.time()-t1:.1f}s]")

    # ==== OUTPUTS ====
    print("\n" + "=" * 72)
    print("  WRITE OUTPUTS")
    print("=" * 72)

    # Per-ED vote total CSVs (match Phase 4C format)
    maj_out = maj["ed_totals"].copy()
    maj_out.to_csv(OUT_MAJ, index=False)
    mino_out = mino["ed_totals"].copy()
    mino_out.to_csv(OUT_MIN, index=False)
    print(f"  wrote: {OUT_MAJ}")
    print(f"  wrote: {OUT_MIN}")

    # Per-VA attribution table
    maj_ap = maj["apportioned"].assign(map="majority")
    min_ap = mino["apportioned"].assign(map="minority")
    per_va_out = pd.concat([maj_ap, min_ap], ignore_index=True)
    per_va_out = per_va_out[[
        "map", "OBJECTID", "parent_ed_2019", "VA_NUMBER", "name_2026",
        "area_weight", "va_ndp_full_share", "va_ucp_full_share",
        "va_other_full_share", "fallback",
    ]].rename(columns={"name_2026": "ed_2026"})
    per_va_out.to_csv(OUT_PER_VA, index=False)
    print(f"  wrote: {OUT_PER_VA}  ({len(per_va_out):,} rows)")

    # ==== COMPARISON with centroid-based (§5.2.7 headline) ====
    print("\n" + "=" * 72)
    print("  EG COMPARISON: centroid-in-polygon vs MAUP area-weighted")
    print("=" * 72)
    maj_eg = maj["eg"]
    min_eg = mino["eg"]
    asym = (min_eg - maj_eg) * 100  # percentage points
    print(f"  §5.2.7 centroid (headline):  "
          f"majority={CENTROID_MAJORITY_EG*100:+.2f}%  "
          f"minority={CENTROID_MINORITY_EG*100:+.2f}%  "
          f"asym={CENTROID_ASYMMETRY_PP:+.2f} pp (NDP-favourable)")
    print(f"  MAUP area-weighted:          "
          f"majority={maj_eg*100:+.4f}%  "
          f"minority={min_eg*100:+.4f}%  "
          f"asym={asym:+.4f} pp")

    delta_maj = (maj_eg - CENTROID_MAJORITY_EG) * 100
    delta_min = (min_eg - CENTROID_MINORITY_EG) * 100
    delta_asym = asym - CENTROID_ASYMMETRY_PP
    print(f"  Δ vs centroid:               "
          f"Δmajority={delta_maj:+.4f} pp  "
          f"Δminority={delta_min:+.4f} pp  "
          f"Δasym={delta_asym:+.4f} pp")

    # Verdict on §5.2.7 disagreement
    # Blended-crosswalk gives majority EG −1.29%, minority −2.71%, asym −1.42pp
    # Centroid-spatial gives majority EG −2.33%, minority +1.82%, asym +4.15pp
    # Does MAUP bring these closer or not?
    abs_gap_centroid = abs(CENTROID_ASYMMETRY_PP - (-1.42))  # 5.57 pp
    abs_gap_maup = abs(asym - (-1.42))
    print(f"\n  §5.2.7 disagreement gap (spatial asym vs crosswalk asym of -1.42 pp):")
    print(f"    centroid-spatial ↔ crosswalk: {abs_gap_centroid:.2f} pp")
    print(f"    MAUP-spatial    ↔ crosswalk: {abs_gap_maup:.2f} pp")
    if abs_gap_maup < abs_gap_centroid - 0.25:
        verdict = "MAUP narrows the §5.2.7 disagreement"
    elif abs_gap_maup > abs_gap_centroid + 0.25:
        verdict = "MAUP widens the §5.2.7 disagreement"
    else:
        verdict = "MAUP preserves the §5.2.7 disagreement"
    print(f"    verdict: {verdict}")

    # ==== SUMMARY JSON ====
    summary = {
        "inputs": {
            "va_gpkg": str(VA_GPKG),
            "majority_canonical": str(MAJ_CANON_GPKG),
            "minority_canonical": str(MIN_CANON_GPKG),
            "majority_crosswalk": str(MAJ_XWALK_CSV),
            "minority_crosswalk": str(MIN_XWALK_CSV),
        },
        "outputs": {
            "majority_votes_csv": str(OUT_MAJ),
            "minority_votes_csv": str(OUT_MIN),
            "per_va_attribution_csv": str(OUT_PER_VA),
            "summary_json": str(OUT_SUMMARY),
        },
        "centroid_baseline_527": {
            "majority_eg": CENTROID_MAJORITY_EG,
            "minority_eg": CENTROID_MINORITY_EG,
            "asymmetry_pp": CENTROID_ASYMMETRY_PP,
            "direction": "minority_more_NDP_favourable",
        },
        "maup_area_weighted": {
            "majority": {
                "eg": maj["eg"],
                "mm_gap": maj["mm_gap"],
                "ndp_seats": maj["ndp_seats"],
                "ucp_seats": maj["ucp_seats"],
                "two_party_total": maj["two_party_total"],
                "coverage": maj["coverage"],
                "conservation": maj["conservation"],
            },
            "minority": {
                "eg": mino["eg"],
                "mm_gap": mino["mm_gap"],
                "ndp_seats": mino["ndp_seats"],
                "ucp_seats": mino["ucp_seats"],
                "two_party_total": mino["two_party_total"],
                "coverage": mino["coverage"],
                "conservation": mino["conservation"],
            },
            "asymmetry_pp": asym,
        },
        "delta_vs_centroid_pp": {
            "majority": delta_maj,
            "minority": delta_min,
            "asymmetry": delta_asym,
        },
        "section_527_verdict": {
            "abs_gap_centroid_vs_crosswalk_pp": abs_gap_centroid,
            "abs_gap_maup_vs_crosswalk_pp": abs_gap_maup,
            "verdict": verdict,
        },
    }
    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n  wrote: {OUT_SUMMARY}")

    print("\n[DONE]")


if __name__ == "__main__":
    main()
