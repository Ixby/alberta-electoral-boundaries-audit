"""Population Consistency Cross-Check (Test B2)
===============================================

Cross-checks the commission's per-ED population figures (from their published
tables) against independent 2021 Census DA totals aggregated by spatial join
to each ED polygon.

Both the commission and the 2021 Census use the same enumeration base.
If an ED boundary aligns cleanly with DA boundaries the two figures should
agree within rounding.  A delta > ±5 % indicates either:
  (a) an ED boundary cuts through a DA (DA population was split), or
  (b) the commission used a different population source or vintage, or
  (c) a data-entry or crosswalk error.

This script does NOT recompute MAD or variance distributions — those are
already computed in electoral_forensics_population.py.  The focus here is
the commission-vs-census consistency check only.

Outputs:
  findings/population_consistency.csv
      per-ED rows: map, ed_name, commission_pop, da_sum_pop,
                   delta_persons, delta_pct, within_tolerance
  data/population_consistency_summary.json
      per-map: mean_delta_pct, max_delta_pct, eds_outside_tolerance,
               provincial_quota, mad_persons, mad_pct

Author: v0.1 audit pipeline — Test B2. Generated 2026-04-24.

Forward deps:
  - findings/population_consistency.csv consumed by
    report_academic.md §B (population data provenance)
  - data/population_consistency_summary.json consumed by summary dashboard

Backward deps:
  - data/majority_2026_populations.csv
  - data/minority_2026_populations.csv
  - data/alberta_2019_populations.csv
  - data/alberta_2021_da_populations.csv   (Census DA totals)
  - data/shapefiles/reference/alberta_2021_das.gpkg
  - data/shapefiles/derived/v0_3_canonical_majority_2026_eds_swept.gpkg
  - data/shapefiles/derived/v0_3_canonical_minority_2026_eds_swept.gpkg
  - data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import json
import sys
from typing import Optional

import numpy as np
import pandas as pd
import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent.parent  # .../alberta_audit
DATA = data_loader._resolve_path("data")
try:
    from analysis.utils.data_loader import FINDINGS as REPORTS
except ImportError:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'utils'))
    from data_loader import FINDINGS as REPORTS
REPORTS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TOLERANCE_PCT = 5.0  # ±5 % consistency gate
PROVINCIAL_QUOTA_2026 = 54929  # 4,888,723 / 89 EDs


# ---------------------------------------------------------------------------
# Shapefile configs
# ---------------------------------------------------------------------------

def _pick_ed_layer(plan: str) -> tuple:
    """Return (path, name_col) preferring canonical shapefiles."""
    canonical = DATA / f"shapefiles/canonical/ea_{plan}_2026_eds.gpkg"
    if canonical.exists():
        return canonical, "EDName2025"
    derived = DATA / f"shapefiles/derived/v0_3_canonical_{plan}_2026_eds_swept.gpkg"
    return derived, "name_2026"


_maj_path, _maj_col = _pick_ed_layer("majority")
_min_path, _min_col = _pick_ed_layer("minority")

ED_LAYERS = {
    "majority_2026": {
        "path": _maj_path,
        "name_col": _maj_col,
        "commission_csv": DATA / "reference" / "majority_2026_populations.csv",
        "commission_name_col": "ed_name",
        "commission_pop_col": "population",
        "provincial_quota": PROVINCIAL_QUOTA_2026,
        "target_crs": None,
    },
    "minority_2026": {
        "path": _min_path,
        "name_col": _min_col,
        "commission_csv": DATA / "reference" / "minority_2026_populations.csv",
        "commission_name_col": "ed_name",
        "commission_pop_col": "population",
        "provincial_quota": PROVINCIAL_QUOTA_2026,
        "target_crs": None,
    },
    "2019": {
        "path": DATA
        / "shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp",
        "name_col": "EDName2017",
        "commission_csv": DATA / "reference" / "alberta_2019_populations.csv",
        "commission_name_col": "ed_name",
        "commission_pop_col": "population_2017_report",
        "provincial_quota": None,  # computed from data
        "target_crs": "EPSG:3347",
    },
}

DA_SHAPEFILE = DATA / "shapefiles/reference/alberta_2021_das.gpkg"
DA_POP_CSV = DATA / "reference" / "alberta_2021_da_populations.csv"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_das_with_population() -> gpd.GeoDataFrame:
    """Merge DA polygons with 2021 Census population totals."""
    das_geo = gpd.read_file(DA_SHAPEFILE)
    da_pop = pd.read_csv(DA_POP_CSV, dtype={"DAUID": str})

    # Detect population column
    pop_col_candidates = [c for c in da_pop.columns if "pop" in c.lower()]
    if not pop_col_candidates:
        raise ValueError(
            f"No population column found in {DA_POP_CSV}. Columns: {list(da_pop.columns)}"
        )
    pop_col = pop_col_candidates[0]
    print(f"  DA population column: '{pop_col}'")

    # Ensure DAUID is string in both
    das_geo["DAUID"] = das_geo["DAUID"].astype(str)
    da_pop["DAUID"] = da_pop["DAUID"].astype(str)

    merged = das_geo.merge(da_pop[["DAUID", pop_col]], on="DAUID", how="left")
    merged = merged.rename(columns={pop_col: "population_2021"})
    merged["population_2021"] = pd.to_numeric(
        merged["population_2021"], errors="coerce"
    ).fillna(0.0)

    print(
        f"  Loaded {len(merged)} DAs  (total pop: {merged['population_2021'].sum():,.0f})"
    )
    return merged


def load_commission_table(cfg: dict) -> Optional[pd.DataFrame]:
    """Load the commission's per-ED population table, if it exists."""
    csv_path = cfg["commission_csv"]
    if not csv_path.exists():
        print(f"  Commission CSV not found: {csv_path} — skipping")
        return None

    df = pd.read_csv(csv_path)
    name_col = cfg["commission_name_col"]
    pop_col = cfg["commission_pop_col"]

    # Validate expected columns exist
    if name_col not in df.columns:
        # Try to find a plausible name column
        candidates = [c for c in df.columns if "name" in c.lower() or "ed" in c.lower()]
        if candidates:
            name_col = candidates[0]
            print(
                f"  WARNING: expected '{cfg['commission_name_col']}' not found; using '{name_col}'"
            )
        else:
            raise ValueError(
                f"Cannot find name column in {csv_path}. Columns: {list(df.columns)}"
            )

    if pop_col not in df.columns:
        candidates = [c for c in df.columns if "pop" in c.lower()]
        if candidates:
            pop_col = candidates[0]
            print(
                f"  WARNING: expected '{cfg['commission_pop_col']}' not found; using '{pop_col}'"
            )
        else:
            raise ValueError(
                f"Cannot find population column in {csv_path}. Columns: {list(df.columns)}"
            )

    result = df[[name_col, pop_col]].copy()
    result.columns = ["ed_name", "commission_pop"]
    result["commission_pop"] = pd.to_numeric(result["commission_pop"], errors="coerce")
    result = result.dropna(subset=["commission_pop"])
    print(
        f"  Commission table: {len(result)} EDs  (total pop: {result['commission_pop'].sum():,.0f})"
    )
    return result


# ---------------------------------------------------------------------------
# Spatial join: aggregate DA populations to ED polygons
# ---------------------------------------------------------------------------


def da_pop_by_ed(
    eds_gdf: gpd.GeoDataFrame,
    name_col: str,
    das_gdf: gpd.GeoDataFrame,
    target_crs: Optional[str],
) -> pd.Series:
    """Spatial join DAs to EDs and sum population_2021 per ED.

    Uses centroid-in-polygon join (each DA centroid assigned to the ED that
    contains it).  This is the standard MAUP approach: avoids area-weighting
    artifacts for DAs that happen to straddle an ED boundary.  Since DAs are
    smaller than EDs by design, most centroids fall cleanly inside one ED.

    Returns a Series indexed by ed_name with values = summed DA population.
    """
    # Reproject DAs to match ED CRS
    eds = eds_gdf.copy()
    if target_crs:
        eds = eds.to_crs(target_crs)
    # Ensure same CRS
    das = das_gdf.to_crs(eds.crs)

    # DA centroids
    da_centroids = das.copy()
    da_centroids["geometry"] = das.geometry.centroid

    # Spatial join: centroid in ED polygon
    joined = gpd.sjoin(
        da_centroids[["DAUID", "population_2021", "geometry"]],
        eds[[name_col, "geometry"]],
        how="left",
        predicate="within",
    )

    # Aggregate
    agg = joined.groupby(name_col)["population_2021"].sum()

    # Any ED with no DAs in it gets 0
    all_eds = eds[name_col].unique()
    agg = agg.reindex(all_eds, fill_value=0.0)

    return agg


# ---------------------------------------------------------------------------
# Per-map analysis
# ---------------------------------------------------------------------------


def analyse_map(
    map_label: str,
    cfg: dict,
    das_gdf: gpd.GeoDataFrame,
) -> tuple[pd.DataFrame, dict]:
    """Run B2 consistency check for one map.

    Returns (per_ed_df, summary_dict).
    """
    print(f"\n{'='*60}")
    print(f"Map: {map_label}")
    print(f"{'='*60}")

    # Load commission table
    commission_df = load_commission_table(cfg)
    if commission_df is None:
        return pd.DataFrame(), {}

    # Load ED polygons
    eds_gdf = gpd.read_file(cfg["path"])
    name_col = cfg["name_col"]
    if cfg.get("target_crs"):
        eds_gdf = eds_gdf.to_crs(cfg["target_crs"])
    eds_gdf["geometry"] = eds_gdf.geometry.buffer(0)
    print(f"  ED polygons: {len(eds_gdf)}")

    # Compute DA-derived population per ED
    da_pop_series = da_pop_by_ed(eds_gdf, name_col, das_gdf, cfg.get("target_crs"))

    # Build per-ED DataFrame
    rows = []
    for _, ed in eds_gdf.iterrows():
        ed_name = ed[name_col]
        da_sum = float(da_pop_series.get(ed_name, 0.0))

        # Look up commission figure
        comm_row = commission_df[commission_df["ed_name"] == ed_name]
        if len(comm_row) == 0:
            # Try partial match (e.g., trailing whitespace)
            comm_row = commission_df[
                commission_df["ed_name"].str.strip() == ed_name.strip()
            ]

        if len(comm_row) == 0:
            commission_pop = np.nan
        else:
            commission_pop = float(comm_row["commission_pop"].values[0])

        delta_persons = (
            da_sum - commission_pop if not np.isnan(commission_pop) else np.nan
        )
        delta_pct = (
            (delta_persons / commission_pop * 100.0)
            if (not np.isnan(commission_pop) and commission_pop != 0)
            else np.nan
        )
        within_tolerance = (
            bool(abs(delta_pct) <= TOLERANCE_PCT) if not np.isnan(delta_pct) else False
        )

        rows.append(
            {
                "map": map_label,
                "ed_name": ed_name,
                "commission_pop": commission_pop,
                "da_sum_pop": round(da_sum, 0),
                "delta_persons": (
                    round(delta_persons, 0) if not np.isnan(delta_persons) else np.nan
                ),
                "delta_pct": round(delta_pct, 3) if not np.isnan(delta_pct) else np.nan,
                "within_tolerance": within_tolerance,
            }
        )

    per_ed_df = pd.DataFrame(rows)

    # Summary stats
    valid = per_ed_df.dropna(subset=["delta_pct"])
    mean_delta = float(valid["delta_pct"].mean()) if len(valid) else np.nan
    max_delta = float(valid["delta_pct"].abs().max()) if len(valid) else np.nan
    eds_outside = int((~valid["within_tolerance"]).sum())
    mad_persons = float(valid["delta_persons"].abs().mean()) if len(valid) else np.nan
    mad_pct = float(valid["delta_pct"].abs().mean()) if len(valid) else np.nan

    prov_quota = cfg.get("provincial_quota") or (
        float(commission_df["commission_pop"].mean()) if len(commission_df) else np.nan
    )

    gate = (
        "PASS"
        if eds_outside == 0
        else f"WARN ({eds_outside} EDs outside +/-{TOLERANCE_PCT}%)"
    )

    print(f"  Consistency gate: {gate}")
    print(f"  Mean delta: {mean_delta:+.2f}%  |  Max |delta|: {max_delta:.2f}%")
    print(f"  MAD: {mad_persons:,.0f} persons  ({mad_pct:.2f}%)")
    print(f"  EDs outside +/-{TOLERANCE_PCT}%: {eds_outside}")

    if eds_outside > 0:
        outliers = valid[~valid["within_tolerance"]].sort_values(
            "delta_pct", key=abs, ascending=False
        )
        print(f"  Top outliers:")
        for _, r in outliers.head(5).iterrows():
            print(
                f"    {r['ed_name']:45s}  commission={r['commission_pop']:,.0f}  "
                f"DA={r['da_sum_pop']:,.0f}  delta={r['delta_pct']:+.1f}%"
            )

    summary = {
        "map": map_label,
        "n_eds": len(per_ed_df),
        "n_matched": int(per_ed_df["commission_pop"].notna().sum()),
        "mean_delta_pct": round(mean_delta, 3) if not np.isnan(mean_delta) else None,
        "max_delta_pct": round(max_delta, 3) if not np.isnan(max_delta) else None,
        "eds_outside_tolerance": eds_outside,
        "tolerance_pct": TOLERANCE_PCT,
        "provincial_quota": prov_quota,
        "mad_persons": round(mad_persons, 1) if not np.isnan(mad_persons) else None,
        "mad_pct": round(mad_pct, 3) if not np.isnan(mad_pct) else None,
        "consistency_gate": "PASS" if eds_outside == 0 else "WARN",
    }

    return per_ed_df, summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("Loading DA polygons with 2021 Census populations …")
    das_gdf = load_das_with_population()

    all_rows = []
    all_summaries = []

    for map_label, cfg in ED_LAYERS.items():
        per_ed_df, summary = analyse_map(map_label, cfg, das_gdf)
        if len(per_ed_df):
            all_rows.append(per_ed_df)
            all_summaries.append(summary)

    if not all_rows:
        print("No maps processed — check file paths.", file=sys.stderr)
        sys.exit(1)

    # Write outputs
    combined = pd.concat(all_rows, ignore_index=True)
    out_csv = REPORTS / "population_consistency.csv"
    combined.to_csv(out_csv, index=False)
    print(f"\nWrote {len(combined)} rows to {out_csv}")

    out_json = DATA / "population_consistency_summary.json"
    with open(out_json, "w") as fh:
        json.dump(all_summaries, fh, indent=2, default=str)
    print(f"Wrote summary to {out_json}")

    # Final gate summary
    print("\n" + "=" * 70)
    print("POPULATION CONSISTENCY GATE RESULTS")
    print("=" * 70)
    print(
        f"{'Map':<22s} {'N EDs':>6s} {'MeanD%':>9s} {'MaxD%':>9s} {'Outside5pct':>12s} {'Gate':>8s}"
    )
    print("-" * 70)
    for s in all_summaries:
        print(
            f"{s['map']:<22s} {s['n_eds']:>6d} "
            f"{(s['mean_delta_pct'] or 0):>+9.2f} "
            f"{(s['max_delta_pct'] or 0):>9.2f} "
            f"{s['eds_outside_tolerance']:>12d} "
            f"{s['consistency_gate']:>8s}"
        )

    print()
    print("Interpretation:")
    print(
        f"  PASS = all EDs within +/-{TOLERANCE_PCT}% of commission figure (DA centroid match)."
    )
    print(
        f"  WARN = one or more EDs differ by >{TOLERANCE_PCT}%; may indicate boundary"
    )
    print(f"         cuts through a DA (DA population split across EDs) or a source")
    print(f"         discrepancy.  Review outliers in {out_csv.name}.")


if __name__ == "__main__":
    main()
