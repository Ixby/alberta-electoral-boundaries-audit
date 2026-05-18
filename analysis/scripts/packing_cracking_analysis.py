# Version: v0.3
"""
Alberta Electoral Boundaries — Packing/Cracking Analysis (v0.3)
===============================================================

Lane 1 (Statistical), Step 2 of 3: Partisan-bias metrics (B1–B6)
Chain: phase4c_canonical_attribution → packing_cracking_analysis → mcmc_ensemble_canonical

Phase 4C (v0.3): replaces the v0.2 70/30 urban/rural blend with exact VA-level
spatial attribution. Vote totals for each 2026 ED are computed by spatially
joining VA polygon centroids to the official Elections Alberta shapefiles and
summing va_ndp / va_ucp per ED — identical to the approach used by
mcmc_ensemble_canonical.py. No estimation or blending is applied.

Tests computed (Stephanopoulos & McGhee 2014; McDonald & Best 2015):

  B1: Vote distribution histogram by ED margin
  B2: Efficiency gap = (W_NDP - W_UCP) / N
  B3: Mean-median difference in NDP vote share
  B4: Seats-votes curve at 50/50 under uniform swing
  B6: Declination (Warrington 2018)

Vote columns: va_ndp / va_ucp (integer counts; consistent with mcmc_ensemble_canonical.py).
Note: config.yaml lists va_ndp_full / va_ucp_full as the substrate columns — those are
the fractional-allocation variants (~1.8x larger). This script uses the integer columns
to stay consistent with the canonical MCMC pipeline whose real-map scores are the
primary published values.

Backward:
  data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/canonical/ea_minority_2026_eds.gpkg
  data/alberta_2023_results.csv  (2019 baseline only)
Forward:
  findings/partisan_bias_summary.md
  findings/extended_partisan_metrics.md
"""

import csv
import sys
import statistics
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from analysis.utils.eg_utils import InsufficientDataError
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    from eg_utils import InsufficientDataError

try:
    from analysis.scripts.canonical_paths import canonical_shapefile, ED_NAME_COL
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from canonical_paths import canonical_shapefile, ED_NAME_COL

# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------


def _find_data(filename: str) -> str:
    here = Path(__file__).resolve().parent
    root = here.parent.parent / "data"
    for candidate in (root / filename, root / "reference" / filename):
        if candidate.exists():
            return str(candidate)
    raise FileNotFoundError(f"Missing required data file: {root / filename}")


def load_2023_results() -> List[Dict]:
    """Load 87 EDs with 2023 NDP+UCP totals per ED, plus region."""
    out = []
    with open(_find_data("alberta_2023_results.csv")) as f:
        for r in csv.DictReader(f):
            ndp = ucp = 0
            for i in range(1, 7):
                cand = r.get(f"cand_{i}", "") or ""
                votes_str = r.get(f"votes_{i}", "") or ""
                if not cand or not votes_str:
                    continue
                try:
                    votes = int(votes_str)
                except ValueError:
                    continue

                import re

                # Exact matches for party affilation, preventing "Independent - UCP" false positives
                # Regex anchors to end of string or matches exact parentheticals
                cand_upper = cand.strip().upper()
                is_ndp = re.search(
                    r"(\(NDP\)$|\bNDP$|ALBERTA NDP|NEW DEMOCRATIC PARTY)", cand_upper
                )
                is_ucp = re.search(
                    r"(\(UCP\)$|\bUCP$|UNITED CONSERVATIVE PARTY)", cand_upper
                )

                # Exclude independent candidates who happen to have the letters
                if "INDEPENDENT" in cand_upper:
                    continue

                if is_ndp:
                    ndp = votes
                elif is_ucp:
                    ucp = votes

            # Critical validation: We MUST have detected a valid 2-party race
            if not (ndp + ucp > 0):
                raise InsufficientDataError(
                    f"Failed to parse votes for 2023 ED: {r['ed_name']}. NDP={ndp}, UCP={ucp}"
                )

            out.append(
                {
                    "ed": r["ed_name"],
                    "region": r["region"],
                    "ndp": ndp,
                    "ucp": ucp,
                }
            )
    return out


# ---------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------


def compute_metrics(districts: List[Dict], label: str, *, verbose: bool = True) -> Dict:
    n = len(districts)
    total_ndp = sum(d["ndp"] for d in districts)
    total_ucp = sum(d["ucp"] for d in districts)
    total = total_ndp + total_ucp
    prov_ndp = total_ndp / total

    n_ndp_wins = sum(1 for d in districts if d["ndp"] > d["ucp"])
    n_ucp_wins = n - n_ndp_wins

    margins = [(d["ndp"] - d["ucp"]) / (d["ndp"] + d["ucp"]) * 100 for d in districts]
    bins = [
        (-100, -25),
        (-25, -15),
        (-15, -10),
        (-10, -5),
        (-5, 0),
        (0, 5),
        (5, 10),
        (10, 15),
        (15, 25),
        (25, 100),
    ]
    bin_counts = [sum(1 for m in margins if lo <= m < hi) for lo, hi in bins]

    # B2: Efficiency gap
    ndp_wasted = ucp_wasted = 0
    for d in districts:
        tt = d["ndp"] + d["ucp"]
        thr = tt // 2 + 1
        if d["ndp"] > d["ucp"]:
            ndp_wasted += max(0, d["ndp"] - thr)
            ucp_wasted += d["ucp"]
        else:
            ucp_wasted += max(0, d["ucp"] - thr)
            ndp_wasted += d["ndp"]
    eg = (ndp_wasted - ucp_wasted) / total

    # B3: Mean-median
    shares = [d["ndp"] / (d["ndp"] + d["ucp"]) for d in districts]
    mn = statistics.mean(shares)
    md = statistics.median(shares)
    mm_gap = mn - md

    # B4: 50/50 uniform swing
    swing = 0.5 - prov_ndp
    swung = [s + swing for s in shares]
    ndp_at_50 = sum(1 for s in swung if s > 0.5)
    ucp_at_50 = n - ndp_at_50

    # B6: Declination (Warrington 2018)
    # Measure asymmetry in winning-district distributions by computing
    # the angle between two reference points (mean NDP-won share, mean
    # UCP-won share) relative to the 50/50 line, normalized to [-1, 1].
    ndp_won_shares = [s for s in shares if s > 0.5]
    ucp_won_shares = [s for s in shares if s < 0.5]
    if ndp_won_shares and ucp_won_shares:
        import math

        mean_ndp_won = statistics.mean(ndp_won_shares)
        mean_ucp_won = statistics.mean(ucp_won_shares)
        # Declination (Warrington 2018): theta_UCP - theta_NDP, normalized by pi/2.
        # Positive = pro-UCP (UCP wins many seats by small margins while NDP votes
        # are packed into a few high-share districts). Negative = pro-NDP.
        # Sign convention matches mcmc_ensemble.py line 206 (theta_R - theta_D).
        theta_ndp = math.atan2(mean_ndp_won - 0.5, n_ndp_wins / n)
        theta_ucp = math.atan2(0.5 - mean_ucp_won, n_ucp_wins / n)
        declination = (theta_ucp - theta_ndp) * 2 / math.pi
    else:
        declination = float("nan")  # one party swept

    if verbose:
        print(f"\n{'='*60}\n  {label}\n{'='*60}")
        print(f"  Districts: {n}")
        print(
            f"  Province two-party: NDP {prov_ndp*100:.2f}%, UCP {(1-prov_ndp)*100:.2f}%"
        )
        print(f"  Actual seats: NDP {n_ndp_wins}, UCP {n_ucp_wins}")
        labels = [
            "UCP +25%+",
            "UCP 15-25",
            "UCP 10-15",
            "UCP 5-10",
            "UCP 0-5",
            "NDP 0-5",
            "NDP 5-10",
            "NDP 10-15",
            "NDP 15-25",
            "NDP +25%+",
        ]
        print(f"\n  B1: Vote distribution (margin in two-party share)")
        for lbl, count in zip(labels, bin_counts):
            print(f"    {lbl:>12s}: {'#' * count} {count}")
        print(
            f"\n  B2: Efficiency gap = {eg*100:+.2f}%  "
            f"({'within' if abs(eg) < 0.07 else 'EXCEEDS'} 7% threshold)"
        )
        print(
            f"  B3: Mean-median (NDP) = {mm_gap*100:+.2f} pp  "
            f"({'within' if abs(mm_gap) < 0.03 else 'EXCEEDS'} 3 pp threshold)"
        )
        print(
            f"  B4: At 50/50 vote: NDP {ndp_at_50}, UCP {ucp_at_50} "
            f"(asymmetry: {abs(ndp_at_50-ucp_at_50)} seats)"
        )
        dec_str = f"{declination:+.4f}" if declination == declination else "N/A"
        print(
            f"  B6: Declination (Warrington 2018) = {dec_str}  "
            f"(positive = pro-UCP, negative = pro-NDP)"
        )

    return {
        "label": label,
        "n": n,
        "prov_ndp": prov_ndp,
        "ndp_seats": n_ndp_wins,
        "ucp_seats": n_ucp_wins,
        "eg": eg,
        "mm_gap": mm_gap,
        "ndp_at_50": ndp_at_50,
        "ucp_at_50": ucp_at_50,
        "bin_counts": bin_counts,
        "declination": declination,
    }


# ---------------------------------------------------------------------
# Phase 4C — exact VA-level spatial attribution
# ---------------------------------------------------------------------
def _load_va_gpkg():
    """Load VA polygon GeoDataFrame with va_ndp / va_ucp integer vote columns."""
    import geopandas as gpd
    ROOT = Path(__file__).resolve().parent.parent.parent
    candidates = [
        ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_full_2023_votes.gpkg",
        ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_votes.gpkg",
    ]
    va_path = next((p for p in candidates if p.exists()), None)
    if va_path is None:
        raise FileNotFoundError(
            "VA polygon file not found. Checked: " + "; ".join(str(p) for p in candidates)
        )
    gdf = gpd.read_file(va_path)
    gdf["va_ndp"] = gdf["va_ndp"].fillna(0).astype(int)
    gdf["va_ucp"] = gdf["va_ucp"].fillna(0).astype(int)
    return gdf


def score_map_by_spatial_join(va_gdf, ed_gpkg: Path, ed_name_col: str) -> List[Dict]:
    """Score a 2026 map by spatially joining VA centroids to ED polygons.

    Mirrors mcmc_ensemble_canonical.py exactly: representative_point() centroid,
    within-predicate sjoin, per-ED aggregation of va_ndp / va_ucp.
    """
    import geopandas as gpd
    eds = gpd.read_file(str(ed_gpkg))[[ed_name_col, "geometry"]]
    centroids = va_gdf.copy()
    centroids["geometry"] = centroids.geometry.representative_point()
    joined = gpd.sjoin(
        centroids[["va_ucp", "va_ndp", "geometry"]],
        eds,
        how="left",
        predicate="within",
    )
    joined = joined.dropna(subset=[ed_name_col])
    joined = joined[~joined.index.duplicated(keep="first")]
    agg = (
        joined.groupby(ed_name_col)
        .agg(ndp=("va_ndp", "sum"), ucp=("va_ucp", "sum"))
        .reset_index()
    )
    return [
        {"ed": row[ed_name_col], "ndp": int(row["ndp"]), "ucp": int(row["ucp"])}
        for _, row in agg.iterrows()
    ]


# ---------------------------------------------------------------------
# Falsifiability gates
# ---------------------------------------------------------------------


def validate_2026_estimate(
    estimates: List[Dict], label: str, expected_n: int = 89
) -> Tuple[bool, str]:
    """Gate: refuse to proceed if estimate set is incomplete or sums implausibly."""
    n = len(estimates)
    total = sum(d["ndp"] + d["ucp"] for d in estimates)
    total_ndp = sum(d["ndp"] for d in estimates)
    ok = True
    msgs = []
    if n != expected_n:
        msgs.append(f"FAIL: {label} has {n} EDs, expected {expected_n}")
        ok = False
    # va_ndp + va_ucp integer columns sum to ~893k province-wide (not the
    # 1.706M actual vote count — the integer columns are a downscaled
    # representation). Accept any total in [700k, 1.1M] to catch gross errors
    # (wrong file, empty join) while accommodating this column's scale.
    if not (700_000 <= total <= 1_100_000):
        msgs.append(f"FAIL: {label} total votes {total:,} outside plausible range")
        ok = False
    ndp_share = total_ndp / total if total else 0
    if not (0.40 <= ndp_share <= 0.50):
        msgs.append(f"FAIL: {label} NDP share {ndp_share:.3f} outside plausible range")
        ok = False
    return ok, "; ".join(msgs) if msgs else "PASS"


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def main():
    print("=" * 60)
    print("  Alberta Packing/Cracking Analysis v0.3")
    print("  Phase 4C — exact VA-level spatial attribution")
    print("=" * 60)

    dists_2019 = load_2023_results()

    # 2019 baseline (from CSV; no shapefile needed)
    m_2019 = compute_metrics(
        dists_2019, "2019 BOUNDARIES (CURRENT) under 2023 vote shares"
    )

    # Load VA polygons once — shared between both map scorings
    va_gdf = _load_va_gpkg()
    va_ndp_total = int(va_gdf["va_ndp"].sum())
    va_ucp_total = int(va_gdf["va_ucp"].sum())
    print(
        f"\nVA file: {va_ndp_total:,} NDP + {va_ucp_total:,} UCP = {va_ndp_total + va_ucp_total:,} total"
    )

    # Majority 2026 — exact spatial attribution
    map_a_dists = score_map_by_spatial_join(
        va_gdf, canonical_shapefile("majority"), ED_NAME_COL
    )
    ok, msg = validate_2026_estimate(map_a_dists, "Majority 2026")
    print(f"\n[GATE] Majority 2026 validation: {msg}")
    if not ok:
        print("Aborting majority metrics — gate failed.")
        m_map_a = None
    else:
        m_map_a = compute_metrics(map_a_dists, "MAJORITY 2026 PROPOSAL (Phase 4C, exact)")

    # Minority 2026 — exact spatial attribution
    map_b_dists = score_map_by_spatial_join(
        va_gdf, canonical_shapefile("minority"), ED_NAME_COL
    )
    ok, msg = validate_2026_estimate(map_b_dists, "Minority 2026")
    print(f"\n[GATE] Minority 2026 validation: {msg}")
    if not ok:
        print("Aborting minority metrics — gate failed.")
        m_map_b = None
    else:
        m_map_b = compute_metrics(map_b_dists, "MINORITY 2026 PROPOSAL (Phase 4C, exact)")

    # Three-way comparison
    if m_map_a and m_map_b:
        print("\n" + "=" * 60)
        print("  THREE-MAP COMPARISON")
        print("=" * 60)
        print(f"  Metric              | 2019    | Majority | Minority")
        print(
            f"  Districts            | {m_2019['n']:>7d} | {m_map_a['n']:>8d} | {m_map_b['n']:>8d}"
        )
        print(
            f"  Actual seats NDP/UCP | {m_2019['ndp_seats']}/{m_2019['ucp_seats']}   | {m_map_a['ndp_seats']}/{m_map_a['ucp_seats']}    | {m_map_b['ndp_seats']}/{m_map_b['ucp_seats']}"
        )
        print(
            f"  B2 Efficiency gap    | {m_2019['eg']*100:+6.2f}% | {m_map_a['eg']*100:+7.2f}% | {m_map_b['eg']*100:+7.2f}%"
        )
        print(
            f"  B3 Mean-median       | {m_2019['mm_gap']*100:+6.2f}pp| {m_map_a['mm_gap']*100:+7.2f}pp| {m_map_b['mm_gap']*100:+7.2f}pp"
        )
        print(
            f"  B4 NDP @ 50/50       | {m_2019['ndp_at_50']:>7d} | {m_map_a['ndp_at_50']:>8d} | {m_map_b['ndp_at_50']:>8d}"
        )
        print(
            f"  B6 Declination       | {m_2019['declination']:+7.4f} | {m_map_a['declination']:+8.4f} | {m_map_b['declination']:+8.4f}"
        )

    # Falsifiability gate — directional claim check
    if m_map_a and m_map_b:
        print("\n" + "=" * 60)
        print("  FALSIFIABILITY GATE — directional claim check")
        print("=" * 60)
        delta_map_a = m_map_a["eg"] - m_2019["eg"]
        delta_map_b = m_map_b["eg"] - m_2019["eg"]
        print(f"  Delta from 2019 EG (majority): {delta_map_a*100:+.2f} pp")
        print(f"  Delta from 2019 EG (minority): {delta_map_b*100:+.2f} pp")
        print(f"  Minority-Majority asymmetry:   {(delta_map_b-delta_map_a)*100:+.2f} pp")
        if abs(delta_map_b - delta_map_a) < 0.005:
            print(
                "  VERDICT: maps within 0.5 pp of each other — NO asymmetry detected."
            )
        else:
            print(
                f"  VERDICT: minority shifts {(delta_map_b-delta_map_a)*100:+.2f} pp relative to majority."
            )


if __name__ == "__main__":
    main()
