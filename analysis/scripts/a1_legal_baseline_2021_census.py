"""
v0.1 A1 Legal-Baseline — 2021-census-direct on the 87 existing 2019 EDs.

forward_dependencies:
  - data/a1_legal_baseline_2019eds_2021census.csv (written)
  - analysis/methodology/appendix_c_legal_baseline.md (consumes printed summary)
  - analysis/v0_1_fortification_a1_a5.md (A4 narrowed-claim appendix spec — F7)
  - report_academic.md — parent session decides whether to integrate as Appendix C
backward_dependencies:
  - data/alberta_2021_csd_populations.csv (2021 Census, 423 CSDs in Alberta)
  - data/alberta_2021_csds.gpkg (CSD boundary polygons, EPSG:3347)
  - data/alberta_2021_da_populations.csv (2021 Census, 6,203 DAs in Alberta)
  - data/alberta_2021_das.gpkg (DA polygons, EPSG:3347)
  - data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp (87 EDs, EPSG:3401)
  - data/alberta_2019_populations.csv (commission's 2017-report 2019-ED values)
  - analysis/reports/plan_b_cross_check.md (data-basis discussion; statutory §12)
  - analysis/v0_1_fortification_a1_a5.md (A4 specification)

Purpose. Compute A1 MAD (Mean Absolute Deviation from the provincial quota)
for the 87 existing (2019-Act) electoral divisions, aggregated directly from
the 2021 Census of Population. This provides the §12(3)-operative
legal-baseline statistic against which the commission's 2024-TBF-derived A1
can be compared. The 2026 proposals cannot be evaluated on the 2021-census
basis because the 2026 ED shapefiles have not been released.

Method. The directive specifies CSD-to-ED overlay (area-weighted) as the
primary method. We ran this and found the area-weighting artifact is
severe: Alberta's rural municipal districts (MD of Foothills, MD of Rocky
View, etc.) contain both small towns and vast empty range-land, and
area-weighting distributes the concentrated population evenly across the
range-land, producing physically impossible per-ED totals (Calgary-Peigan
at +246 % deviation under pure CSD area-weighting). This script therefore
uses a two-level approach:

  - Primary method: DA-level (dissemination area) overlay. DAs are the
    smallest standard Statistics Canada geography (median ~400 people in
    Alberta), and their area-weighting artifacts are small because DA
    polygons are drawn to reflect population concentration. This is the
    methodologically correct way to aggregate 2021 Census population to
    arbitrary non-standard boundaries such as the 87 2019 EDs.
  - Secondary (reported for transparency): the CSD area-weighted approach
    the directive originally specified. We report both so reviewers can
    see the artifact and the refinement.

Both methods project inputs to EPSG:3401 (Alberta 10TM-AEP) for metric
area. Invalid geometries are self-healed via buffer(0).

House voice. No emoji.
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


import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows console.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import pandas as pd
import numpy as np
import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")

CSD_POP_CSV = DATA / "alberta_2021_csd_populations.csv"
CSD_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
DA_POP_CSV = DATA / "alberta_2021_da_populations.csv"
DA_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_das.gpkg"
ED_SHP = (
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)
ED_2019_COMM_CSV = DATA / "alberta_2019_populations.csv"

OUT_CSV = DATA / "a1_legal_baseline_2019eds_2021census.csv"

# Common projection for the spatial overlay — EPSG:3401 is the 10TM AEP
# Forest projection used by Alberta Environment and Parks for the ED
# shapefile; preserves area in metres squared across Alberta.
TARGET_CRS = "EPSG:3401"

# Statutory band boundaries (±25 % of quota).
LEGAL_WINDOW_BAND = 0.25


def load_csd_populations() -> pd.DataFrame:
    """2021 Census CSD population table for Alberta.

    Eight CSDs in the Statistics Canada file have null populations (typically
    Indian Reserves with suppressed counts under StatCan's small-population
    rules). We treat those as zero population for aggregation, which matches
    the commission's own handling in its variance tables: the decennial
    census suppression is the accepted statutory data, and §12(3)(b) permits
    a separate population-on-reserve input that the audit does not have.
    """
    df = pd.read_csv(CSD_POP_CSV)
    # CSDUID is the 7-digit alternate geographic code in this file.
    df = df.rename(columns={"ALT_GEO_CODE": "CSDUID"})
    df["CSDUID"] = df["CSDUID"].astype(int)
    n_null = int(df["population_2021"].isna().sum())
    if n_null:
        print(
            f"  Note: {n_null} CSDs with null 2021 pop (suppressed);"
            " treated as zero."
        )
    df["population_2021"] = df["population_2021"].fillna(0).astype(int)
    return df[["CSDUID", "GEO_NAME", "population_2021"]]


def load_da_populations() -> pd.DataFrame:
    """2021 Census DA population table for Alberta."""
    df = pd.read_csv(DA_POP_CSV)
    df = df.rename(columns={"DAUID": "DAUID_int"})
    df["DAUID_int"] = df["DAUID_int"].astype(int)
    n_null = int(df["population_2021"].isna().sum())
    if n_null:
        print(
            f"  Note: {n_null} DAs with null 2021 pop (suppressed);" " treated as zero."
        )
    df["population_2021"] = df["population_2021"].fillna(0).astype(int)
    return df[["DAUID_int", "population_2021"]].rename(columns={"DAUID_int": "DAUID"})


def load_da_polygons() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(DA_GPKG)
    gdf["DAUID"] = gdf["DAUID"].astype(int)
    gdf = gdf.to_crs(TARGET_CRS)
    invalid = ~gdf.is_valid
    if invalid.any():
        gdf.loc[invalid, "geometry"] = gdf.loc[invalid, "geometry"].buffer(0)
    return gdf[["DAUID", "geometry"]]


def load_csd_polygons() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(CSD_GPKG)
    gdf["CSDUID"] = gdf["CSDUID"].astype(int)
    gdf = gdf.to_crs(TARGET_CRS)
    # Fix any invalid geometries up front.
    invalid = ~gdf.is_valid
    if invalid.any():
        gdf.loc[invalid, "geometry"] = gdf.loc[invalid, "geometry"].buffer(0)
    return gdf[["CSDUID", "CSDNAME", "geometry"]]


def load_ed_polygons() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(ED_SHP)
    gdf = gdf.to_crs(TARGET_CRS)
    invalid = ~gdf.is_valid
    if invalid.any():
        gdf.loc[invalid, "geometry"] = gdf.loc[invalid, "geometry"].buffer(0)
    # Standardise column names.
    gdf = gdf.rename(columns={"EDName2017": "ed_name", "EDNumber20": "ed_number"})
    return gdf[["ed_number", "ed_name", "geometry"]]


def build_csd_to_ed_crosswalk(
    csds: gpd.GeoDataFrame, eds: gpd.GeoDataFrame
) -> pd.DataFrame:
    """Area-weighted spatial overlay producing (CSDUID, ed_name, weight) rows.

    For each CSD, weight is the fraction of the CSD's area that falls within
    each intersecting ED. Weights across a CSD sum (approximately) to 1.0;
    any residual (CSD area outside all 87 Alberta EDs) is normalised out so
    the allocated population equals the CSD's reported population. This
    method is reported for transparency; the DA-level crosswalk below is the
    primary method because area-weighting within CSDs misallocates
    population for CSDs where population is unevenly distributed (e.g., a
    rural municipal district with a town inside it).
    """
    print("  Running spatial overlay (intersection, CSD level)...")
    overlay = gpd.overlay(csds, eds, how="intersection", keep_geom_type=True)
    overlay["intersect_area"] = overlay.geometry.area
    # CSD source area for normalisation.
    csd_area = csds.assign(csd_area=csds.geometry.area)[["CSDUID", "csd_area"]]
    overlay = overlay.merge(csd_area, on="CSDUID", how="left")
    overlay["raw_weight"] = overlay["intersect_area"] / overlay["csd_area"]
    # Normalise so weights per CSD sum to exactly 1.0.
    csd_total = overlay.groupby("CSDUID")["raw_weight"].sum().rename("csd_weight_sum")
    overlay = overlay.join(csd_total, on="CSDUID")
    overlay["weight"] = overlay["raw_weight"] / overlay["csd_weight_sum"]
    return overlay[
        ["CSDUID", "ed_name", "ed_number", "intersect_area", "raw_weight", "weight"]
    ]


def build_da_to_ed_crosswalk(
    das: gpd.GeoDataFrame, eds: gpd.GeoDataFrame
) -> pd.DataFrame:
    """Area-weighted DA-level crosswalk. This is the primary method.

    DAs are ~400-person polygons drawn to reflect population concentration,
    so the area-weighting artifact that affects CSD-level aggregation is
    negligible at this scale. For each DA, weight is the fraction of the
    DA's area intersecting each ED. A DA that lies entirely inside one ED
    contributes its full population to that ED. Any cross-boundary DA is
    split by area share, which is accurate at DA scale (median DA area in
    urban Alberta is small enough that within-DA uniformity is a reasonable
    assumption).
    """
    print("  Running spatial overlay (intersection, DA level)...")
    overlay = gpd.overlay(das, eds, how="intersection", keep_geom_type=True)
    overlay["intersect_area"] = overlay.geometry.area
    da_area = das.assign(da_area=das.geometry.area)[["DAUID", "da_area"]]
    overlay = overlay.merge(da_area, on="DAUID", how="left")
    overlay["raw_weight"] = overlay["intersect_area"] / overlay["da_area"]
    da_total = overlay.groupby("DAUID")["raw_weight"].sum().rename("da_weight_sum")
    overlay = overlay.join(da_total, on="DAUID")
    overlay["weight"] = overlay["raw_weight"] / overlay["da_weight_sum"]
    return overlay[
        ["DAUID", "ed_name", "ed_number", "intersect_area", "raw_weight", "weight"]
    ]


def aggregate_da_to_eds(
    crosswalk: pd.DataFrame, da_pop: pd.DataFrame, eds: gpd.GeoDataFrame
) -> pd.DataFrame:
    merged = crosswalk.merge(da_pop, on="DAUID", how="left")
    merged["allocated_pop"] = merged["weight"] * merged["population_2021"].fillna(0)
    ed_pop = (
        merged.groupby(["ed_number", "ed_name"])["allocated_pop"]
        .sum()
        .reset_index()
        .rename(columns={"allocated_pop": "pop_2021_census"})
    )
    full = eds[["ed_number", "ed_name"]].merge(
        ed_pop, on=["ed_number", "ed_name"], how="left"
    )
    full["pop_2021_census"] = full["pop_2021_census"].fillna(0.0)
    return full.sort_values("ed_name").reset_index(drop=True)


def aggregate_to_eds(
    crosswalk: pd.DataFrame, csd_pop: pd.DataFrame, eds: gpd.GeoDataFrame
) -> pd.DataFrame:
    """Apply weights to CSD populations and sum per ED."""
    merged = crosswalk.merge(csd_pop, on="CSDUID", how="left")
    # CSDs with no population row (shouldn't happen — warn if so).
    missing = merged["population_2021"].isna().sum()
    if missing:
        print(f"  WARN: {missing} overlay rows had no 2021 pop — dropping.")
        merged = merged.dropna(subset=["population_2021"])
    merged["allocated_pop"] = merged["weight"] * merged["population_2021"]
    ed_pop = (
        merged.groupby(["ed_number", "ed_name"])["allocated_pop"]
        .sum()
        .reset_index()
        .rename(columns={"allocated_pop": "pop_2021_census"})
    )
    # Any EDs that had zero CSD coverage — highlight and backfill with 0.
    full = eds[["ed_number", "ed_name"]].merge(
        ed_pop, on=["ed_number", "ed_name"], how="left"
    )
    full["pop_2021_census"] = full["pop_2021_census"].fillna(0.0)
    return full.sort_values("ed_name").reset_index(drop=True)


def compute_a1(ed_pop: pd.DataFrame) -> dict:
    """Per-ED deviation and summary statistics on the 2021-census basis."""
    pop = ed_pop["pop_2021_census"].astype(float)
    n = len(ed_pop)
    provincial_total = float(pop.sum())
    quota = provincial_total / n
    ed_pop = ed_pop.copy()
    ed_pop["dev_from_quota"] = pop - quota
    ed_pop["dev_pct"] = (pop - quota) / quota * 100.0
    ed_pop["outside_legal_window_flag"] = (
        ed_pop["dev_pct"].abs() > LEGAL_WINDOW_BAND * 100.0
    ).astype(int)

    mad = ed_pop["dev_from_quota"].abs().mean()
    outside_count = int(ed_pop["outside_legal_window_flag"].sum())
    max_pos = float(ed_pop["dev_pct"].max())
    max_neg = float(ed_pop["dev_pct"].min())
    max_pos_name = ed_pop.loc[ed_pop["dev_pct"].idxmax(), "ed_name"]
    max_neg_name = ed_pop.loc[ed_pop["dev_pct"].idxmin(), "ed_name"]

    return {
        "n": n,
        "provincial_total": provincial_total,
        "quota": quota,
        "mad": float(mad),
        "outside_legal_window_count": outside_count,
        "max_pos_dev_pct": max_pos,
        "max_pos_dev_name": max_pos_name,
        "max_neg_dev_pct": max_neg,
        "max_neg_dev_name": max_neg_name,
        "ed_table": ed_pop,
    }


def commission_2019_mad() -> dict | None:
    """MAD implied by the commission's 2017 report (2019-ED populations).

    The file is a per-ED table of variance percentages relative to the
    provincial average of ≈45,221 prevailing in 2017. Reconstructing the
    MAD requires the absolute populations; those are in the population
    column. We compute MAD against the mean of the reported populations,
    which reproduces the commission-derived baseline.
    """
    if not ED_2019_COMM_CSV.exists():
        return None
    df = pd.read_csv(ED_2019_COMM_CSV)
    df = df.dropna(subset=["population_2017_report"])
    pop = df["population_2017_report"].astype(float)
    total = float(pop.sum())
    n = len(df)
    quota = total / n
    mad = float((pop - quota).abs().mean())
    return {
        "n": n,
        "provincial_total": total,
        "quota": quota,
        "mad": mad,
        "source": "2017 EBC Final Report — 2019-Act ED table",
    }


def top_extreme(ed_pop: pd.DataFrame, k: int = 10) -> pd.DataFrame:
    df = ed_pop.copy()
    df["abs_dev"] = df["dev_pct"].abs()
    return df.sort_values("abs_dev", ascending=False).head(k)[
        [
            "ed_name",
            "pop_2021_census",
            "dev_from_quota",
            "dev_pct",
            "outside_legal_window_flag",
        ]
    ]


def write_output(ed_pop: pd.DataFrame, path: Path) -> None:
    out = ed_pop[
        [
            "ed_name",
            "pop_2021_census",
            "dev_from_quota",
            "dev_pct",
            "outside_legal_window_flag",
        ]
    ].copy()
    # Round for readability; retain full precision in dev_from_quota as int.
    out["pop_2021_census"] = out["pop_2021_census"].round(0).astype(int)
    out["dev_from_quota"] = out["dev_from_quota"].round(0).astype(int)
    out["dev_pct"] = out["dev_pct"].round(3)
    out.to_csv(path, index=False)


def main() -> None:
    print("=" * 72)
    print("v0.1 A1 Legal-Baseline — 2021 Census direct, 87 2019 EDs")
    print("=" * 72)

    print("\n[1/7] Loading 2021 Census CSD populations...")
    csd_pop = load_csd_populations()
    print(f"  CSDs with 2021 pop: {len(csd_pop)}")
    print(f"  Total 2021 pop (sum of CSDs): {csd_pop['population_2021'].sum():,}")

    print("\n[2/7] Loading 2021 Census DA populations (primary basis)...")
    da_pop = load_da_populations()
    print(f"  DAs with 2021 pop: {len(da_pop)}")
    print(f"  Total 2021 pop (sum of DAs):  {da_pop['population_2021'].sum():,}")

    print("\n[3/7] Loading polygons...")
    csds = load_csd_polygons()
    das = load_da_polygons()
    eds = load_ed_polygons()
    print(
        f"  CSD polygons: {len(csds)}  DA polygons: {len(das)}  "
        f"ED polygons: {len(eds)}"
    )

    print("\n[4/7] Building DA-to-2019-ED crosswalk (primary)...")
    da_crosswalk = build_da_to_ed_crosswalk(das, eds)
    da_ed_counts = da_crosswalk.groupby("DAUID")["ed_name"].nunique()
    split_das = int((da_ed_counts > 1).sum())
    print(f"  DAs split across >=2 EDs: {split_das} / {len(da_ed_counts)}")

    print("\n[5/7] Building CSD-to-2019-ED crosswalk (secondary, per directive)...")
    csd_crosswalk = build_csd_to_ed_crosswalk(csds, eds)
    csd_ed_counts = csd_crosswalk.groupby("CSDUID")["ed_name"].nunique()
    split_csds = int((csd_ed_counts > 1).sum())
    print(f"  CSDs split across >=2 EDs: {split_csds} / {len(csd_ed_counts)}")

    print("\n[6/7] Aggregating...")
    ed_pop_da = aggregate_da_to_eds(da_crosswalk, da_pop, eds)
    ed_pop_csd = aggregate_to_eds(csd_crosswalk, csd_pop, eds)
    a1_da = compute_a1(ed_pop_da)
    a1_csd = compute_a1(ed_pop_csd)

    # Primary reported value uses the DA-level aggregation.
    a1 = a1_da

    print("\n[7/7] Writing output table (DA-level primary)...")
    write_output(a1["ed_table"], OUT_CSV)
    print(f"  Wrote {OUT_CSV.relative_to(ROOT)}")

    # ------------------------------------------------------------------ #
    # Structured summary
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 72)
    print("SUMMARY — 2019 map, 2021 Census direct basis (DA-LEVEL, PRIMARY)")
    print("=" * 72)

    print(f"  N districts:                        {a1['n']}")
    print(f"  Provincial total (census aggr.):    {a1['provincial_total']:,.0f}")
    print(
        "  Expected 2021 Alberta total:        4,262,635  (diff vs aggr.:"
        f" {a1['provincial_total'] - 4_262_635:+,.0f})"
    )
    print(f"  Per-ED quota:                       {a1['quota']:,.1f}")
    print(f"  MAD:                                {a1['mad']:,.0f}")
    print(
        f"  EDs outside +/-25 % window:         " f"{a1['outside_legal_window_count']}"
    )
    print(
        f"  Max positive deviation:             "
        f"+{a1['max_pos_dev_pct']:.2f} %  "
        f"({a1['max_pos_dev_name']})"
    )
    print(
        f"  Max negative deviation:             "
        f"{a1['max_neg_dev_pct']:.2f} %  "
        f"({a1['max_neg_dev_name']})"
    )

    print("\n  Secondary (CSD-level area-weighted, per original directive):")
    print(f"    MAD:                              {a1_csd['mad']:,.0f}")
    print(
        f"    EDs outside +/-25 %:              "
        f"{a1_csd['outside_legal_window_count']}"
    )
    print(
        f"    Max +dev:  +{a1_csd['max_pos_dev_pct']:.2f} %  "
        f"({a1_csd['max_pos_dev_name']})"
    )
    print(
        f"    Max -dev:   {a1_csd['max_neg_dev_pct']:.2f} %  "
        f"({a1_csd['max_neg_dev_name']})"
    )
    print("    CSD-level area-weighting misallocates population from rural")
    print("    MDs (e.g., Rocky View, Foothills) across their full area;")
    print("    DA-level is the methodologically defensible primary basis.")

    # ------------------------------------------------------------------ #
    # Comparison block
    # ------------------------------------------------------------------ #
    print("\n" + "-" * 72)
    print("COMPARISON — MAD across bases and maps")
    print("-" * 72)
    print(f"  2019 map on 2021 Census (this script):           " f"{a1['mad']:>8,.0f}")
    comm = commission_2019_mad()
    if comm is not None:
        print(
            f"  2019 map on 2017 EBC report (commission):        "
            f"{comm['mad']:>8,.0f}"
        )
        print(f"    (quota used: {comm['quota']:,.0f} ; n={comm['n']})")
    else:
        print("  2019 map on 2017 EBC report: file not found.")
    # 2024/2026 values are quoted from the paper's §2.1 for reference only.
    print("  2026 majority map on 2024 TBF (commission §2.1):    3,180")
    print("  2026 minority map on 2024 TBF (commission §2.1):    4,707")
    print("  Note: the 2026 values use a different map AND a different")
    print("  population basis; direct numeric subtraction is not valid.")
    print("  Ordinal comparison is reportable: is the 2019-on-2021 MAD")
    print("  above, below, or between the two 2026-on-2024 values?")

    # ------------------------------------------------------------------ #
    # Top-10 extreme deviations
    # ------------------------------------------------------------------ #
    print("\n" + "-" * 72)
    print("TOP-10 ABSOLUTE DEVIATIONS  (2019 EDs, 2021 Census basis)")
    print("-" * 72)
    top = top_extreme(a1["ed_table"], 10)
    for _, r in top.iterrows():
        flag = "OUT" if r["outside_legal_window_flag"] else "in "
        print(
            f"  {flag}  {r['ed_name']:<36}  "
            f"pop={r['pop_2021_census']:>8,.0f}  "
            f"dev={r['dev_pct']:+6.2f} %"
        )

    # ------------------------------------------------------------------ #
    # Track L comparison (cycle-lag 2025 mid-year estimates)
    # ------------------------------------------------------------------ #
    print("\n" + "-" * 72)
    print("TRACK L CROSS-CHECK — 2019 map, mid-2025 TBF estimate")
    print("-" * 72)
    print("  Track L reports 5 of 87 2019 EDs outside +/-25 % under 2025 TBF.")
    print(
        f"  This script reports {a1['outside_legal_window_count']} of {a1['n']} outside +/-25 %"
    )
    print("  under 2021 Census (decennial-baseline snapshot).")
    print("  If the 2019 map was drawn compliantly against the decennial")
    print("  census at drawing-time vintage, the 2021-Census count should be")
    print("  0 or very small; the 2025-TBF count of 5 reflects four years of")
    print("  differential growth. Delta is the cycle-lag fingerprint.")

    # ------------------------------------------------------------------ #
    # Closing diagnostics
    # ------------------------------------------------------------------ #
    print("\n" + "-" * 72)
    print("DIAGNOSTICS")
    print("-" * 72)
    total_diff = a1["provincial_total"] - 4_262_635
    pct_diff = total_diff / 4_262_635 * 100.0
    print(f"  Aggregation loss vs Alberta 2021 Census total:  " f"{pct_diff:+.4f} %")
    print("  (Any non-zero delta is due to CSD polygons that fall partly")
    print("  outside the province's ED coverage at provincial boundaries,")
    print("  and is normalised per-CSD before ED aggregation.)")

    print("\nDone.")


if __name__ == "__main__":
    main()
