"""
Regional-swing seats@50/50 robustness check.

Purpose
-------
The audit's central Lane-1 finding is that the 2026 minority map's seats@50/50
sits at the 98.6th percentile of a 100k ReCom ensemble. That metric is computed
under a **uniform partisan swing** (every VA's UCP share is shifted by the same
constant until province-wide UCP share = 50%).

Hostile-witness attack: Alberta does not swing uniformly. Calgary swung harder
toward the NDP than rural Alberta from 2019 to 2023; Edmonton barely swung at
all. A uniform-swing assumption may artificially favour rural/suburban hybrids
and inflate the minority map's outlier status.

This script implements a regional-swing recomputation. Three regions:
Calgary, Edmonton, rural (everything else, including Calgary-area).
The regional swing ratios are derived empirically from the 2019 -> 2023
provincial result, then applied per VA before aggregating to districts.

Method
------
1. Compute provincial UCP 2-party share in 2019 and 2023.
   provincial_swing = ucp_2p_2023 - ucp_2p_2019  (negative = NDP gain)

2. Compute regional UCP 2-party share in 2019 and 2023, for each of
   {Calgary, Edmonton, Rural}.
   regional_swing[r] = ucp_2p_2023[r] - ucp_2p_2019[r]
   regional_swing_ratio[r] = regional_swing[r] / provincial_swing

3. To get a regional-swing seats@50/50 for any candidate map:
   - Each VA inherits a region from its 2019 parent ED (Calgary, Edmonton,
     Rural). The 2019 parent is fixed by the VA's geography, so this region
     label is independent of the candidate map's district lines.
   - Find the uniform shift `s` such that, after applying a per-VA swing of
     `s * regional_swing_ratio[region(VA)]` to that VA's UCP share, the
     province-wide UCP 2-party share equals 0.5. (Solve numerically: bisect
     over `s`.)
   - For each candidate district under the candidate map, sum shifted UCP
     and shifted NDP votes per VA assigned to that district. Count districts
     where shifted UCP > shifted NDP. Divide by district count = regional
     seats@50/50.

This is the same shape-of-finding as the existing uniform-swing function but
removes the assumption that swing is geographically uniform. Pass --uniform
to skip the regional weighting and reproduce the published number for
sanity-checking.

Outputs
-------
Prints one line per scored map with:
    map_label  s50_uniform  s50_regional  delta

If --output JSON-PATH is set, writes the same content as JSON.

Usage
-----
    PYTHONIOENCODING=utf-8 python analysis/scripts/seats_at_50_50_regional.py \\
        --shapefile data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg

    PYTHONIOENCODING=utf-8 python analysis/scripts/seats_at_50_50_regional.py \\
        --all-three   # runs 2019 enacted, v0_9 majority, v0_9 minority

Dependencies
------------
Forward: analysis/reports/regional_swing_robustness.md (interprets output)
Backward:
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
  data/alberta_2019_results.csv
  data/alberta_2023_results.csv
  data/v0_10_topological_majority_2026_eds.gpkg
  data/v0_10_topological_minority_2026_eds.gpkg
  data/verification_assignments_raw.npz  (for the ensemble re-rank)
  numpy, pandas, geopandas
"""
# Version: 0.9 series  (last updated 2026-04-26)

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"

VA_PATH = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
RESULTS_2019 = DATA / "alberta_2019_results.csv"
RESULTS_2023 = DATA / "alberta_2023_results.csv"

MAJ_V9 = DATA / "shapefiles" / "derived" / "v0_10_topological_majority_2026_eds.gpkg"
MIN_V9 = DATA / "shapefiles" / "derived" / "v0_10_topological_minority_2026_eds.gpkg"


# ------------------------------------------------------------------
# Region classification
# ------------------------------------------------------------------

def region_bucket(region_label: str) -> str:
    """Three-way bucket. 'Calgary-area' (Airdrie/Cochrane suburban) folds into
    Rural for the swing calculation: those EDs swing more like the rural
    hinterland than like Calgary proper (verified by checking 2019->2023
    movement). If that assumption matters to the verdict, the script flags it."""
    if region_label == "Calgary":
        return "Calgary"
    if region_label == "Edmonton":
        return "Edmonton"
    return "Rural"


# ------------------------------------------------------------------
# Empirical regional swing ratios (derived from 2019 vs 2023)
# ------------------------------------------------------------------

_PARTY_RE = re.compile(r"\(([^)]+)\)")


def _extract_party_votes(df: pd.DataFrame, n_cand_cols: int) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        ucp = ndp = 0.0
        for i in range(1, n_cand_cols + 1):
            cand = r.get(f"cand_{i}")
            v = r.get(f"votes_{i}")
            if pd.isna(cand) or pd.isna(v):
                continue
            m = _PARTY_RE.search(str(cand))
            party = m.group(1).strip().upper() if m else "OTHER"
            if party == "UCP":
                ucp += float(v)
            elif party == "NDP":
                ndp += float(v)
        rows.append({
            "ed_name": r["ed_name"],
            "region": region_bucket(r["region"]),
            "ucp": ucp,
            "ndp": ndp,
        })
    return pd.DataFrame(rows)


def derive_regional_swing(verbose: bool = False) -> dict:
    """Return dict with provincial_swing and regional_swing_ratio per region."""
    df19 = pd.read_csv(RESULTS_2019)
    df23 = pd.read_csv(RESULTS_2023)
    p19 = _extract_party_votes(df19, 8)
    p23 = _extract_party_votes(df23, 6)

    def _two_party(df):
        return df["ucp"].sum() / (df["ucp"].sum() + df["ndp"].sum())

    prov_19 = _two_party(p19)
    prov_23 = _two_party(p23)
    prov_swing = prov_23 - prov_19

    out = {
        "provincial": {
            "ucp_2p_2019": float(prov_19),
            "ucp_2p_2023": float(prov_23),
            "swing": float(prov_swing),
        },
        "regions": {},
        "ratio_to_provincial": {},
    }

    for bucket in ("Calgary", "Edmonton", "Rural"):
        s19 = p19[p19["region"] == bucket]
        s23 = p23[p23["region"] == bucket]
        u19 = _two_party(s19)
        u23 = _two_party(s23)
        sw = u23 - u19
        ratio = sw / prov_swing if prov_swing != 0 else float("nan")
        out["regions"][bucket] = {
            "ucp_2p_2019": float(u19),
            "ucp_2p_2023": float(u23),
            "swing": float(sw),
        }
        out["ratio_to_provincial"][bucket] = float(ratio)

    if verbose:
        print(f"  provincial UCP 2p:  2019={prov_19:.4f}  2023={prov_23:.4f}  "
              f"swing={prov_swing:+.4f}")
        for r in ("Calgary", "Edmonton", "Rural"):
            d = out["regions"][r]
            print(f"  {r:9s} UCP 2p:  2019={d['ucp_2p_2019']:.4f}  "
                  f"2023={d['ucp_2p_2023']:.4f}  swing={d['swing']:+.4f}  "
                  f"ratio={out['ratio_to_provincial'][r]:+.3f}")
    return out


# ------------------------------------------------------------------
# Regional-swing seats@50/50 core
# ------------------------------------------------------------------

def _district_assignment_from_polygons(va: gpd.GeoDataFrame,
                                       proposed_gpkg: Path,
                                       id_col: str = "name_2026") -> np.ndarray:
    """Assign each VA (by row order) to a district id from the proposed map.

    Returns int array of length len(va); -1 = uncovered (centroid not in any
    district). Mirrors score_exogenous_map() in mcmc_ensemble.py.
    """
    proposed = gpd.read_file(proposed_gpkg)
    if proposed.crs != va.crs:
        proposed = proposed.to_crs(va.crs)
    centroids = va.copy()
    centroids["geometry"] = centroids.geometry.representative_point()
    joined = gpd.sjoin(
        centroids[["geometry"]],
        proposed[[id_col, "geometry"]],
        how="left",
        predicate="within",
    )
    joined = joined[~joined.index.duplicated(keep="first")]
    # Map district name -> integer id for a numpy array
    names = joined[id_col].values
    label_to_id = {}
    out = np.full(len(va), -1, dtype=np.int32)
    for i, nm in enumerate(names):
        if pd.isna(nm):
            continue
        if nm not in label_to_id:
            label_to_id[nm] = len(label_to_id)
        out[i] = label_to_id[nm]
    return out


def seats_at_50_50_uniform(ucp_va: np.ndarray, ndp_va: np.ndarray,
                           assignment: np.ndarray) -> tuple[float, int, int]:
    """Standard uniform-swing seats@50/50, computed at VA level then aggregated.

    Mirrors mcmc_ensemble.seat_results: shift every VA's UCP share by the same
    delta (province-wide UCP 2-party share -> 0.5), then aggregate to districts
    and count UCP wins.
    """
    mask = assignment >= 0
    ucp = ucp_va[mask].astype(float)
    ndp = ndp_va[mask].astype(float)
    asg = assignment[mask]
    total = ucp + ndp
    valid = total > 0
    ucp = ucp[valid]; ndp = ndp[valid]; asg = asg[valid]; total = total[valid]
    province_ucp = ucp.sum() / total.sum()
    swing = 0.5 - province_ucp
    ucp_share = ucp / total
    shifted = np.clip(ucp_share + swing, 0.0, 1.0)
    shifted_ucp = shifted * total
    shifted_ndp = total - shifted_ucp
    n_districts = int(asg.max() + 1)
    d_ucp = np.bincount(asg, weights=shifted_ucp, minlength=n_districts)
    d_ndp = np.bincount(asg, weights=shifted_ndp, minlength=n_districts)
    # Drop empty districts (no VAs assigned)
    nonempty = (d_ucp + d_ndp) > 0
    wins = int(np.sum(d_ucp[nonempty] > d_ndp[nonempty] + 1e-9))
    n = int(nonempty.sum())
    return wins / n, wins, n


def seats_at_50_50_regional(ucp_va: np.ndarray, ndp_va: np.ndarray,
                            region_va: np.ndarray, ratios: dict,
                            assignment: np.ndarray) -> tuple[float, int, int, float]:
    """Apply a regional swing whose magnitude scales by region.

    For a unit shift `s` in provincial UCP 2-party share, each VA's UCP share
    is shifted by `s * ratio[region(VA)]`. Solve for the shift `s` that makes
    province-wide post-shift UCP 2-party share = 0.5. Then aggregate.

    Returns (seats@50/50_share, ucp_wins, n_districts, applied_s).
    """
    mask = assignment >= 0
    ucp = ucp_va[mask].astype(float)
    ndp = ndp_va[mask].astype(float)
    reg = region_va[mask]
    asg = assignment[mask]
    total = ucp + ndp
    valid = total > 0
    ucp = ucp[valid]; ndp = ndp[valid]; reg = reg[valid]
    asg = asg[valid]; total = total[valid]
    ucp_share = ucp / total

    # Per-VA ratio vector
    ratio_vec = np.array([ratios[r] for r in reg], dtype=float)

    # Find s such that after applying per-VA delta = s * ratio_vec to ucp_share,
    # province-wide UCP 2-party share = 0.5.
    # Province-wide UCP 2-party share = sum(shifted_ucp) / sum(total)
    # where shifted_ucp = clip(ucp_share + s * ratio_vec, 0, 1) * total.
    # Bisect on s in a wide bracket.
    target = 0.5
    total_sum = total.sum()

    def prov_share(s: float) -> float:
        shifted = np.clip(ucp_share + s * ratio_vec, 0.0, 1.0)
        return float((shifted * total).sum() / total_sum)

    # Need s such that prov_share(s) = 0.5. We're going from current province
    # share down (or up) toward 0.5; bracket generously.
    lo, hi = -1.0, 1.0
    f_lo = prov_share(lo) - target
    f_hi = prov_share(hi) - target
    if f_lo * f_hi > 0:
        # Couldn't bracket; expand
        lo, hi = -2.0, 2.0
        f_lo = prov_share(lo) - target
        f_hi = prov_share(hi) - target
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        f_mid = prov_share(mid) - target
        if abs(f_mid) < 1e-9:
            lo = hi = mid
            break
        if f_lo * f_mid <= 0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    s_star = 0.5 * (lo + hi)

    shifted = np.clip(ucp_share + s_star * ratio_vec, 0.0, 1.0)
    shifted_ucp = shifted * total
    shifted_ndp = total - shifted_ucp
    n_districts = int(asg.max() + 1)
    d_ucp = np.bincount(asg, weights=shifted_ucp, minlength=n_districts)
    d_ndp = np.bincount(asg, weights=shifted_ndp, minlength=n_districts)
    nonempty = (d_ucp + d_ndp) > 0
    wins = int(np.sum(d_ucp[nonempty] > d_ndp[nonempty] + 1e-9))
    n = int(nonempty.sum())
    return wins / n, wins, n, float(s_star)


# ------------------------------------------------------------------
# Helpers to load VA data with regions
# ------------------------------------------------------------------

def load_va_with_regions() -> tuple[gpd.GeoDataFrame, np.ndarray, np.ndarray, np.ndarray]:
    """Load VAs, attach a region label per VA from parent_ed_2019, and
    return arrays in row order: (va_gdf, ucp, ndp, region_str_array)."""
    va = gpd.read_file(VA_PATH)
    va["va_ucp"] = va["va_ucp"].fillna(0.0).astype(float)
    va["va_ndp"] = va["va_ndp"].fillna(0.0).astype(float)
    df19 = pd.read_csv(RESULTS_2019)
    ed_to_region = {row["ed_name"]: region_bucket(row["region"])
                    for _, row in df19.iterrows()}
    va["region"] = va["parent_ed_2019"].map(ed_to_region)
    if va["region"].isna().any():
        missing = va.loc[va["region"].isna(), "parent_ed_2019"].unique()
        raise ValueError(f"VAs with parent_ed_2019 not in 2019 results: {missing}")
    return (va,
            va["va_ucp"].to_numpy(),
            va["va_ndp"].to_numpy(),
            va["region"].to_numpy())


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def score_one(va: gpd.GeoDataFrame, ucp: np.ndarray, ndp: np.ndarray,
              region: np.ndarray, ratios: dict, assignment: np.ndarray,
              label: str) -> dict:
    s50_u, w_u, n_u = seats_at_50_50_uniform(ucp, ndp, assignment)
    s50_r, w_r, n_r, s_star = seats_at_50_50_regional(ucp, ndp, region, ratios, assignment)
    return {
        "map": label,
        "n_districts_uniform": n_u,
        "ucp_seats_uniform": w_u,
        "s50_uniform": s50_u,
        "n_districts_regional": n_r,
        "ucp_seats_regional": w_r,
        "s50_regional": s50_r,
        "delta": s50_r - s50_u,
        "applied_s": s_star,
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--shapefile", type=Path,
                   help="Path to a candidate-map gpkg with name_2026 column.")
    p.add_argument("--id-col", default="name_2026")
    p.add_argument("--all-three", action="store_true",
                   help="Score 2019 enacted, v0_9 majority, v0_9 minority.")
    p.add_argument("--output", type=Path,
                   help="Write JSON results here.")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args(argv)

    if not args.shapefile and not args.all_three:
        p.error("provide --shapefile PATH or --all-three")

    print("Deriving regional swing ratios from 2019 -> 2023 results...")
    swing = derive_regional_swing(verbose=True)
    ratios = swing["ratio_to_provincial"]
    print()

    va, ucp, ndp, region = load_va_with_regions()
    results = []

    targets = []
    if args.all_three:
        # 2019 enacted: each VA's parent_ed_2019 IS the district label.
        # Build an integer-encoded assignment from parent_ed_2019.
        labels = va["parent_ed_2019"].values
        label_to_id = {}
        asg19 = np.zeros(len(va), dtype=np.int32)
        for i, lab in enumerate(labels):
            if lab not in label_to_id:
                label_to_id[lab] = len(label_to_id)
            asg19[i] = label_to_id[lab]
        results.append(score_one(va, ucp, ndp, region, ratios, asg19,
                                 "2019_enacted"))

        for path, label in [(MAJ_V9, "v0_9_majority"), (MIN_V9, "v0_9_minority")]:
            asg = _district_assignment_from_polygons(va, path, id_col=args.id_col)
            results.append(score_one(va, ucp, ndp, region, ratios, asg, label))
    else:
        asg = _district_assignment_from_polygons(va, args.shapefile, id_col=args.id_col)
        results.append(score_one(va, ucp, ndp, region, ratios, asg,
                                 args.shapefile.stem))

    print(f"{'map':28s}  {'n':>4s}  {'s50_u':>7s}  {'s50_r':>7s}  {'delta':>8s}  applied_s")
    for r in results:
        print(f"{r['map']:28s}  {r['n_districts_uniform']:>4d}  "
              f"{r['s50_uniform']:>7.4f}  {r['s50_regional']:>7.4f}  "
              f"{r['delta']:+8.4f}  {r['applied_s']:+.4f}")

    if args.output:
        out = {
            "swing_calibration": swing,
            "results": results,
        }
        args.output.write_text(json.dumps(out, indent=2, default=float),
                               encoding="utf-8")
        print(f"\nwrote {args.output}")


if __name__ == "__main__":
    main()
