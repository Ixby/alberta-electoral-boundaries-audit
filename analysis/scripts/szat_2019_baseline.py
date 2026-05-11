"""
szat_2019_baseline.py
---------------------
SZAT (Swing-Zone Allocation Test) applied to the 2019 enacted map as baseline.

Runs two comparisons:
  A) 2019 enacted  ->  majority 2026   (SZAT score = EG_maj − EG_2019)
  B) 2019 enacted  ->  minority 2026   (SZAT score = EG_min − EG_2019)

The 2019 ED assignment is encoded directly in the VA shapefile as the
ED_NAME column (= parent_ed_2019 in the MCMC ensemble).  No 2019 boundary
shapefile is required.

Methodology
-----------
Swing zone: a VA whose centroid is assigned to a different ED under the 2019
map than under the 2026 map being tested.

Null hypothesis: given that VAs needed to be moved from 2019 positions, the
specific boundary choices were partisan-neutral.  Bootstrap permutation test:
for each permutation, each swing-zone VA is randomly assigned to either its
2019 ED or its 2026 ED (Bernoulli 0.5); EG recomputed from scratch; SZAT_perm
= EG_perm − EG_2019_fixed.

Note: the pre-registered SZAT (szat.py) tests minority vs majority 2026.
This script tests 2019 vs each 2026 proposal — an exploratory diagnostic for
the "measuring the void" analysis.  Results are not pre-registered.

Inputs
------
  data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg
    (ED_NAME column = 2019 ED assignment; va_ndp, va_ucp = 2023 votes)
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/canonical/ea_minority_2026_eds.gpkg

Outputs
-------
  analysis/reports/szat_2019_baseline.json

Usage
-----
    python analysis/scripts/szat_2019_baseline.py
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

try:
    import data_loader
    from eg_utils import compute_eg
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader
    from eg_utils import compute_eg

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
REPORTS = ROOT / "analysis" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

VA_FILE = DATA / "shapefiles" / "derived" / "va_polygons_with_full_2023_votes.gpkg"
MAJ_FILE = DATA / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg"
MIN_FILE = DATA / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"
OUT_JSON = REPORTS / "szat_2019_baseline.json"

N_BOOT = 10_000


def _assign(va_gdf: gpd.GeoDataFrame, ed_gdf: gpd.GeoDataFrame) -> pd.Series:
    """Centroid-in-polygon assignment; nearest-ED fallback for gaps."""
    centroids = va_gdf[["geometry"]].copy()
    centroids["geometry"] = va_gdf.geometry.representative_point()
    joined = gpd.sjoin(
        centroids, ed_gdf[["EDName2025", "geometry"]], how="left", predicate="within"
    )
    unresolved = joined["EDName2025"].isna()
    if unresolved.sum() > 0:
        nearest = gpd.sjoin_nearest(
            centroids.loc[unresolved.values],
            ed_gdf[["EDName2025", "geometry"]],
            how="left",
        )
        joined.loc[unresolved.values, "EDName2025"] = nearest["EDName2025"].values
        print(f"    Nearest-ED fallback: {int(unresolved.sum())} centroids")
    return joined["EDName2025"]


def _ed_totals(df: pd.DataFrame, ed_col: str) -> pd.DataFrame:
    g = df.groupby(ed_col, as_index=False).agg(ndp=("va_ndp", "sum"), ucp=("va_ucp", "sum"))
    return g.rename(columns={ed_col: "ed_name"})


def _eg_from_agg(ed_ndp: np.ndarray, ed_ucp: np.ndarray, total_prov: float) -> float:
    ed_total = ed_ndp + ed_ucp
    threshold = ed_total / 2.0
    ndp_wins = ed_ndp >= ed_ucp
    w_ndp = np.where(ndp_wins, np.maximum(0.0, ed_ndp - threshold), ed_ndp)
    w_ucp = np.where(ndp_wins, ed_ucp, np.maximum(0.0, ed_ucp - threshold))
    return (w_ndp.sum() - w_ucp.sum()) / total_prov


def run_szat_pair(
    va: pd.DataFrame,
    baseline_col: str,
    proposal_col: str,
    pair_label: str,
    n_boot: int = N_BOOT,
    seed: int = 20260511,
) -> dict:
    """
    Run SZAT for baseline_col vs proposal_col.
    SZAT score = EG_proposal − EG_baseline.
    """
    va = va.dropna(subset=[baseline_col, proposal_col]).copy()
    va["is_swing"] = va[baseline_col] != va[proposal_col]
    n_swing = int(va["is_swing"].sum())
    total_prov = float((va["va_ndp"] + va["va_ucp"]).sum())

    base_totals = _ed_totals(va, baseline_col)
    prop_totals = _ed_totals(va, proposal_col)

    eg_base = compute_eg(base_totals)
    eg_prop = compute_eg(prop_totals)
    szat_score = eg_prop - eg_base

    print(f"\n  {pair_label}")
    print(f"    EG baseline (2019):    {eg_base:+.6f}")
    print(f"    EG proposal:           {eg_prop:+.6f}")
    print(f"    SZAT score (prop-base): {szat_score:+.6f}")
    print(f"    Swing zones:           {n_swing:,} / {len(va):,}")

    # Bootstrap
    all_eds = np.unique(
        np.concatenate([va[baseline_col].values, va[proposal_col].values])
    )
    ed_to_idx = {e: i for i, e in enumerate(all_eds)}
    n_eds = len(all_eds)

    swing_mask = va["is_swing"].values.astype(bool)
    sw_base_idx = np.array([ed_to_idx[e] for e in va.loc[swing_mask, baseline_col].values])
    sw_prop_idx = np.array([ed_to_idx[e] for e in va.loc[swing_mask, proposal_col].values])
    sw_ndp = va.loc[swing_mask, "va_ndp"].values
    sw_ucp = va.loc[swing_mask, "va_ucp"].values
    nsw_idx = np.array([ed_to_idx[e] for e in va.loc[~swing_mask, baseline_col].values])
    nsw_ndp = va.loc[~swing_mask, "va_ndp"].values
    nsw_ucp = va.loc[~swing_mask, "va_ucp"].values

    nsw_ndp_agg = np.bincount(nsw_idx, weights=nsw_ndp, minlength=n_eds)
    nsw_ucp_agg = np.bincount(nsw_idx, weights=nsw_ucp, minlength=n_eds)

    n_sw = int(swing_mask.sum())
    rng = np.random.default_rng(seed)
    boot_scores = np.empty(n_boot)
    for i in range(n_boot):
        flip = rng.random(n_sw) < 0.5
        perm_idx = np.where(flip, sw_prop_idx, sw_base_idx)
        ed_ndp = nsw_ndp_agg + np.bincount(perm_idx, weights=sw_ndp, minlength=n_eds)
        ed_ucp = nsw_ucp_agg + np.bincount(perm_idx, weights=sw_ucp, minlength=n_eds)
        boot_scores[i] = _eg_from_agg(ed_ndp, ed_ucp, total_prov) - eg_base

    p_value = float(np.mean(np.abs(boot_scores) >= abs(szat_score)))
    ci_lo = float(np.percentile(boot_scores, 2.5))
    ci_hi = float(np.percentile(boot_scores, 97.5))

    print(f"    Bootstrap p (two-tailed): {p_value:.4f}")
    print(f"    Null 95% CI:              [{ci_lo:+.6f}, {ci_hi:+.6f}]")

    # Regional breakdown (using proposal_col for region labeling)
    def _region(ed_name: str) -> str:
        if ed_name.startswith(("Calgary-", "Calgary–")):
            return "Calgary"
        if ed_name.startswith(("Edmonton-", "Edmonton–")):
            return "Edmonton"
        return "Rest of Alberta / Mountain-West"

    swing_va = va[va["is_swing"]]
    regional = {}
    for r in ("Calgary", "Edmonton", "Rest of Alberta / Mountain-West"):
        def _in_region(row, r=r):
            return _region(row[baseline_col]) == r or _region(row[proposal_col]) == r
        mask = swing_va.apply(_in_region, axis=1)
        # EG delta per VA = EG contribution under proposal − under baseline
        # Simplified: just report swing-VA EG totals by region
        regional[r] = int(mask.sum())

    return {
        "pair": pair_label,
        "eg_baseline_2019": round(eg_base, 6),
        "eg_proposal": round(eg_prop, 6),
        "szat_score": round(szat_score, 6),
        "n_swing": n_swing,
        "n_total_va": len(va),
        "bootstrap_p_value": round(p_value, 4),
        "bootstrap_n": n_boot,
        "bootstrap_seed": seed,
        "bootstrap_ci_95": [round(ci_lo, 6), round(ci_hi, 6)],
        "swing_va_by_region": regional,
        "note": (
            "Exploratory (not pre-registered). Tests whether boundary choices "
            "made in moving from 2019 to this 2026 proposal were partisan-neutral."
        ),
    }


def main():
    from drand_seed import get_canonical_seed
    seed_maj = get_canonical_seed("szat-2019-majority")
    seed_min = get_canonical_seed("szat-2019-minority")

    print("Loading VA shapefile...", flush=True)
    va_gdf = gpd.read_file(VA_FILE)
    print(f"  VAs: {len(va_gdf)}")

    print("Loading 2026 canonical shapefiles...", flush=True)
    maj_gdf = gpd.read_file(MAJ_FILE)
    min_gdf = gpd.read_file(MIN_FILE)
    for gdf in (maj_gdf, min_gdf):
        if gdf.crs != va_gdf.crs:
            gdf.to_crs(va_gdf.crs, inplace=True)

    print("Assigning VAs to 2026 majority EDs...", flush=True)
    majority_ed = _assign(va_gdf, maj_gdf)
    print("Assigning VAs to 2026 minority EDs...", flush=True)
    minority_ed = _assign(va_gdf, min_gdf)

    va = pd.DataFrame({
        "va_id": va_gdf["ED_NAME"].astype(str) + "|" + va_gdf["VA_NUMBER"].astype(str),
        "parent_ed_2019": va_gdf["ED_NAME"].astype(str),
        "va_ndp": va_gdf["va_ndp"].fillna(0.0).astype(float),
        "va_ucp": va_gdf["va_ucp"].fillna(0.0).astype(float),
        "majority_ed": majority_ed.values,
        "minority_ed": minority_ed.values,
    })

    swing_2019_maj = int((va["parent_ed_2019"] != va["majority_ed"]).sum())
    swing_2019_min = int((va["parent_ed_2019"] != va["minority_ed"]).sum())
    print(f"\n2019->majority swing zones: {swing_2019_maj:,} / {len(va):,}")
    print(f"2019->minority swing zones: {swing_2019_min:,} / {len(va):,}")

    result_maj = run_szat_pair(
        va, "parent_ed_2019", "majority_ed",
        "2019 enacted -> majority 2026",
        seed=seed_maj,
    )
    result_min = run_szat_pair(
        va, "parent_ed_2019", "minority_ed",
        "2019 enacted -> minority 2026",
        seed=seed_min,
    )

    print("\n" + "=" * 70)
    print("SZAT 2019 BASELINE SUMMARY")
    print("=" * 70)
    print(f"  {'Comparison':<32}  {'SZAT score':>12}  {'p-value':>8}  {'swing VAs':>10}")
    print("-" * 70)
    for r in (result_maj, result_min):
        print(
            f"  {r['pair']:<32}  {r['szat_score']:>+12.6f}  "
            f"{r['bootstrap_p_value']:>8.4f}  {r['n_swing']:>10,}"
        )

    summary = {
        "description": (
            "SZAT 2019 baseline: 2023 votes reallocated to 2019 EDs "
            "vs each 2026 proposal.  Tests whether the commission's "
            "boundary movements from 2019 were partisan-neutral."
        ),
        "canonical_shapefiles": {
            "majority": str(MAJ_FILE.relative_to(ROOT)),
            "minority": str(MIN_FILE.relative_to(ROOT)),
        },
        "results": {
            "2019_to_majority": result_maj,
            "2019_to_minority": result_min,
        },
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=float)
    print(f"\nResults written: {OUT_JSON}")


if __name__ == "__main__":
    main()
