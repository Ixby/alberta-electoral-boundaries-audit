"""
v0_1_overlap_zone_diagnostic.py
================================
Diagnoses overlap zones in the canonical 2026 ED shapefiles and quantifies
their impact on VA assignment and the efficiency gap (EG).

Steps:
  1. Identify overlap zones (intersection polygons) between all ED pairs
     where the intersection area > 0.01 km².
  2. Find VAs whose centroids fall inside each overlap zone.
  3. Compute the maximum EG swing if overlap-zone VAs were reassigned from
     the first-in-index ED to the competing ED.
  4. Write a summary report to analysis/v0_1_overlap_zone_report.md.

Inputs:
  data/v0_1_canonical_majority_2026_eds.gpkg
  data/v0_1_canonical_minority_2026_eds.gpkg
  data/va_polygons_with_2023_votes.gpkg
  analysis/assignment_2026_synthetic_totals.csv

Outputs:
  analysis/v0_1_overlap_zone_report.md  (new)
  stdout summary
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)



import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import sys
import warnings
from itertools import combinations
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.errors import GEOSException

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*GEOSException.*")

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
ANALYSIS = ROOT / "analysis"

MAJ_GPKG = DATA / "shapefiles" / "derived" / "v0_1_canonical_majority_2026_eds.gpkg"
MIN_GPKG = DATA / "shapefiles" / "derived" / "v0_1_canonical_minority_2026_eds.gpkg"
VA_GPKG = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
TOTALS_CSV = ANALYSIS / "assignment_2026_synthetic_totals.csv"

REPORT_OUT = ANALYSIS / "v0_1_overlap_zone_report.md"

# Working CRS: Alberta 10-TM Forest (EPSG:3401), units = metres
WORK_CRS = 3401
OVERLAP_THRESHOLD_KM2 = 0.01  # filter out sub-pixel noise
M2_PER_KM2 = 1_000_000.0


# ── Step 1: Find overlap pairs ────────────────────────────────────────────────


def find_overlaps(eds: gpd.GeoDataFrame, map_label: str) -> pd.DataFrame:
    """
    Return a DataFrame of all ED pairs whose intersection area > threshold.
    Columns: ed_a, ed_b, area_km2, intersection_geom
    """
    eds = eds.to_crs(epsg=WORK_CRS).copy()
    eds = eds[eds.geometry.notna() & ~eds.geometry.is_empty].reset_index(drop=True)

    # Use spatial index to find candidate pairs quickly
    sindex = eds.sindex
    records = []

    for i, row_a in eds.iterrows():
        geom_a = row_a.geometry
        name_a = row_a["name_2026"]
        # bounding-box candidates
        candidates = list(sindex.intersection(geom_a.bounds))
        for j in candidates:
            if j <= i:  # avoid duplicates and self
                continue
            row_b = eds.iloc[j]
            geom_b = row_b.geometry
            name_b = row_b["name_2026"]
            try:
                inter = geom_a.intersection(geom_b)
            except GEOSException:
                continue
            if inter is None or inter.is_empty:
                continue
            area_km2 = inter.area / M2_PER_KM2
            if area_km2 < OVERLAP_THRESHOLD_KM2:
                continue
            records.append(
                {
                    "map": map_label,
                    "ed_a": name_a,  # first in index == current assignment
                    "ed_b": name_b,
                    "area_km2": area_km2,
                    "geometry": inter,
                }
            )

    if not records:
        return gpd.GeoDataFrame(
            columns=["map", "ed_a", "ed_b", "area_km2", "geometry"],
            crs=f"EPSG:{WORK_CRS}",
        )

    gdf = gpd.GeoDataFrame(records, crs=f"EPSG:{WORK_CRS}")
    print(f"  [{map_label}] {len(gdf)} overlap pairs found")
    return gdf


# ── Step 2: Count VAs in each overlap zone ────────────────────────────────────


def count_vas_in_overlaps(
    overlaps: gpd.GeoDataFrame,
    va: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """
    For each overlap zone, find VAs whose centroid falls inside it.

    Returns the overlaps DataFrame enriched with:
      va_count, total_ndp, total_ucp, total_other
    plus a 'va_ids' column (list of va_id strings for the affected VAs).
    """
    if overlaps.empty:
        overlaps = overlaps.copy()
        for col in ["va_count", "total_ndp", "total_ucp", "total_other", "va_ids"]:
            overlaps[col] = [] if col == "va_ids" else 0
        return overlaps

    va = va.to_crs(epsg=WORK_CRS).copy()
    # Compute centroids as a separate geometry column
    va_cents = va.copy()
    va_cents["geometry"] = va.geometry.representative_point()

    va_counts = []
    va_ndp_tots = []
    va_ucp_tots = []
    va_other_tots = []
    va_id_lists = []

    for _, ov_row in overlaps.iterrows():
        ov_geom = ov_row["geometry"]
        # Vectorised containment check
        inside_mask = va_cents.geometry.within(ov_geom)
        inside_vas = va_cents[inside_mask]

        va_counts.append(int(inside_mask.sum()))
        va_ndp_tots.append(float(inside_vas["va_ndp"].sum()))
        va_ucp_tots.append(float(inside_vas["va_ucp"].sum()))
        va_other_tots.append(float(inside_vas.get("va_other", pd.Series(0.0)).sum()))
        va_id_lists.append(
            inside_vas["va_id"].tolist() if "va_id" in inside_vas.columns else []
        )

    overlaps = overlaps.copy()
    overlaps["va_count"] = va_counts
    overlaps["total_ndp"] = va_ndp_tots
    overlaps["total_ucp"] = va_ucp_tots
    overlaps["total_other"] = va_other_tots
    overlaps["va_ids"] = va_id_lists

    return overlaps


# ── EG helpers ────────────────────────────────────────────────────────────────


def compute_eg(district_votes: pd.DataFrame) -> float:
    """
    EG = (wasted_NDP - wasted_UCP) / total_votes  (province-wide).

    district_votes columns: ndp, ucp   (vote totals per district)
    """
    total_all = 0.0
    wasted_ndp = 0.0
    wasted_ucp = 0.0

    for _, row in district_votes.iterrows():
        ndp = float(row["ndp"])
        ucp = float(row["ucp"])
        total = ndp + ucp
        if total <= 0:
            continue
        total_all += total
        threshold = total / 2.0 + 0.5  # 50%+1 (fractional votes OK)
        if ndp >= ucp:  # NDP wins
            wasted_ndp += ndp - threshold
            wasted_ucp += ucp
        else:  # UCP wins
            wasted_ucp += ucp - threshold
            wasted_ndp += ndp

    if total_all <= 0:
        return 0.0
    return (wasted_ndp - wasted_ucp) / total_all


def compute_eg_for_eds(
    totals: pd.DataFrame,
    ed_names: list[str],
    map_col: str,
    map_val: str,
) -> float:
    """Compute EG using only rows matching map_val and the listed ed names."""
    subset = totals[(totals[map_col] == map_val) & (totals["ed_2026"].isin(ed_names))]
    return compute_eg(subset)


# ── Step 3: EG swing ─────────────────────────────────────────────────────────


def compute_eg_swing(
    overlap_row: pd.Series,
    totals: pd.DataFrame,
    map_val: str,
) -> dict:
    """
    Compute EG delta if all VAs in this overlap zone were reassigned from ed_a to ed_b.

    We only touch the two affected EDs to isolate the effect.
    """
    ed_a = overlap_row["ed_a"]
    ed_b = overlap_row["ed_b"]
    ndp_shift = overlap_row["total_ndp"]
    ucp_shift = overlap_row["total_ucp"]

    # Filter totals to this map
    t = totals[totals["map"] == map_val].copy()
    affected = t[t["ed_2026"].isin([ed_a, ed_b])].copy()

    if len(affected) < 2:
        # One or both EDs missing from totals — can't compute swing
        return {"eg_before": np.nan, "eg_after": np.nan, "eg_delta_pp": np.nan}

    # Province-wide baseline (all EDs in this map)
    # For the "local" EG change we compute the full-province EG twice, substituting
    # the two modified rows so the denominator is the same in both cases.

    # Build the full ED vote table
    full = t[["ed_2026", "ndp", "ucp"]].copy().set_index("ed_2026")

    # EG before reassignment
    eg_before = compute_eg(full.reset_index())

    # Modify the two affected EDs
    full_after = full.copy()
    if ed_a in full_after.index:
        full_after.at[ed_a, "ndp"] = max(0.0, full_after.at[ed_a, "ndp"] - ndp_shift)
        full_after.at[ed_a, "ucp"] = max(0.0, full_after.at[ed_a, "ucp"] - ucp_shift)
    if ed_b in full_after.index:
        full_after.at[ed_b, "ndp"] = full_after.at[ed_b, "ndp"] + ndp_shift
        full_after.at[ed_b, "ucp"] = full_after.at[ed_b, "ucp"] + ucp_shift

    eg_after = compute_eg(full_after.reset_index())

    return {
        "eg_before": eg_before,
        "eg_after": eg_after,
        "eg_delta_pp": (eg_after - eg_before) * 100,  # percentage points
    }


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    print("=== v0_1 Overlap Zone Diagnostic ===\n")

    # --- Load data ---
    print("Loading canonical ED shapefiles...")
    maj_eds = gpd.read_file(MAJ_GPKG)
    min_eds = gpd.read_file(MIN_GPKG)

    print("Loading VA polygons...")
    va = gpd.read_file(VA_GPKG)

    # Ensure va_id exists
    if "va_id" not in va.columns:
        if "parent_ed_2019" in va.columns and "VA_NUMBER" in va.columns:
            va["va_id"] = (
                va["parent_ed_2019"] + "|" + va["VA_NUMBER"].astype(str).str.zfill(3)
            )
        else:
            va["va_id"] = va.index.astype(str)

    print("Loading synthetic vote totals...")
    totals = pd.read_csv(TOTALS_CSV)
    # Standardise column names (the file uses 'ndp','ucp','other','n_vas','map')
    totals = totals.rename(columns={"ndp": "ndp", "ucp": "ucp"})

    prov_total = totals["ndp"].sum() + totals["ucp"].sum()

    # --- Step 1: Find overlaps ---
    print("\nStep 1 — Finding overlap pairs...")
    maj_overlaps = find_overlaps(maj_eds, "majority")
    min_overlaps = find_overlaps(min_eds, "minority")

    # --- Step 2: Count VAs ---
    print("\nStep 2 — Counting VAs in overlap zones...")
    print("  Processing majority overlaps...")
    maj_overlaps = count_vas_in_overlaps(maj_overlaps, va)
    print("  Processing minority overlaps...")
    min_overlaps = count_vas_in_overlaps(min_overlaps, va)

    # Province-wide summary stats
    def summarise(ov: gpd.GeoDataFrame, label: str):
        n_pairs = len(ov)
        n_va = int(ov["va_count"].sum())
        ndp_tot = float(ov["total_ndp"].sum())
        ucp_tot = float(ov["total_ucp"].sum())
        vote_tot = ndp_tot + ucp_tot
        pct = 100.0 * vote_tot / prov_total if prov_total > 0 else 0.0
        area_tot = float(ov["area_km2"].sum())
        return dict(
            label=label,
            n_pairs=n_pairs,
            n_va=n_va,
            ndp=ndp_tot,
            ucp=ucp_tot,
            vote_total=vote_tot,
            vote_pct=pct,
            area_km2=area_tot,
        )

    maj_sum = summarise(maj_overlaps, "majority")
    min_sum = summarise(min_overlaps, "minority")

    # --- Step 3: EG swing for top-10 pairs ---
    print("\nStep 3 — Computing EG swing for top-10 overlap pairs per map...")

    def top10_eg(ov: gpd.GeoDataFrame, map_val: str) -> pd.DataFrame:
        top = ov.nlargest(10, "area_km2").copy()
        swings = []
        for _, row in top.iterrows():
            sw = compute_eg_swing(row, totals, map_val)
            swings.append(sw)
        sw_df = pd.DataFrame(swings)
        result = pd.concat([top.reset_index(drop=True), sw_df], axis=1)
        return result

    maj_top10 = top10_eg(maj_overlaps, "majority")
    min_top10 = top10_eg(min_overlaps, "minority")

    # Maximum EG swing (absolute pp) across both maps
    all_swings = pd.concat(
        [
            maj_top10[
                [
                    "ed_a",
                    "ed_b",
                    "area_km2",
                    "va_count",
                    "total_ndp",
                    "total_ucp",
                    "eg_delta_pp",
                ]
            ].assign(map="majority"),
            min_top10[
                [
                    "ed_a",
                    "ed_b",
                    "area_km2",
                    "va_count",
                    "total_ndp",
                    "total_ucp",
                    "eg_delta_pp",
                ]
            ].assign(map="minority"),
        ],
        ignore_index=True,
    )

    all_swings["abs_delta_pp"] = all_swings["eg_delta_pp"].abs()
    max_swing_row = all_swings.loc[all_swings["abs_delta_pp"].idxmax()]

    # --- Step 4: Write report ---
    print("\nStep 4 — Writing report...")

    def fmt_table_row(row) -> str:
        va_count = int(row["va_count"])
        votes = row["total_ndp"] + row["total_ucp"]
        delta = row.get("eg_delta_pp", float("nan"))
        delta_str = f"{delta:+.4f} pp" if not np.isnan(delta) else "n/a"
        return (
            f"| {row['ed_a']} × {row['ed_b']} "
            f"| {row['area_km2']:.2f} "
            f"| {va_count} "
            f"| {votes:,.0f} "
            f"| {delta_str} |"
        )

    maj_max_delta = maj_top10["eg_delta_pp"].abs().max() if not maj_top10.empty else 0.0
    min_max_delta = min_top10["eg_delta_pp"].abs().max() if not min_top10.empty else 0.0
    overall_max = float(all_swings["abs_delta_pp"].max())

    conclusion_threshold = 0.1  # pp — material if |EG swing| > 0.1 pp
    noise_threshold = 0.05  # pp — noise if |EG swing| < 0.05 pp

    if overall_max > conclusion_threshold:
        conclusion = (
            f"Overlap zones are a **material source of error**: the largest single-pair "
            f"reassignment shifts the province-wide EG by {overall_max:.4f} pp, "
            f"which exceeds the 0.10 pp materiality threshold. "
            f"These zones should be resolved before publishing EG estimates."
        )
    elif overall_max < noise_threshold:
        conclusion = (
            f"Overlap zones are **noise** (<0.05 pp): the largest single-pair "
            f"reassignment shifts the province-wide EG by only {overall_max:.4f} pp. "
            f"They do not materially affect the published EG."
        )
    else:
        conclusion = (
            f"Overlap zones are **borderline** (0.05–0.10 pp): the largest single-pair "
            f"reassignment shifts the EG by {overall_max:.4f} pp. "
            f"They are unlikely to change qualitative conclusions but should be noted as "
            f"a source of measurement uncertainty."
        )

    report_lines = [
        "# Overlap Zone Diagnostic Report",
        "",
        f"**Generated:** 2026-04-23",
        f"**Script:** `analysis/scripts/v0_1_overlap_zone_diagnostic.py`",
        "",
        "---",
        "",
        "## 1. Overview",
        "",
        "| Map | Overlap pairs (>0.01 km²) | VAs in overlap zones | Overlap votes | % of province |",
        "|---|---|---|---|---|",
        f"| Majority | {maj_sum['n_pairs']} | {maj_sum['n_va']} "
        f"| {maj_sum['vote_total']:,.0f} | {maj_sum['vote_pct']:.3f}% |",
        f"| Minority | {min_sum['n_pairs']} | {min_sum['n_va']} "
        f"| {min_sum['vote_total']:,.0f} | {min_sum['vote_pct']:.3f}% |",
        "",
        "---",
        "",
        "## 2. Top 10 Overlap Pairs — Majority Map",
        "",
        "Current assignment: VAs go to the ED listed first in the spatial join index (ed_a).",
        "EG Δ: change in province-wide EG (percentage points) if all VAs in this zone were "
        "reassigned to ed_b instead.",
        "",
        "| Pair (ed_a × ed_b) | Area (km²) | VA count | Votes | EG Δ |",
        "|---|---|---|---|---|",
    ]

    for _, row in maj_top10.iterrows():
        report_lines.append(fmt_table_row(row))

    report_lines += [
        "",
        f"**Majority max |EG Δ|:** {maj_max_delta:.4f} pp",
        "",
        "---",
        "",
        "## 3. Top 10 Overlap Pairs — Minority Map",
        "",
        "| Pair (ed_a × ed_b) | Area (km²) | VA count | Votes | EG Δ |",
        "|---|---|---|---|---|",
    ]

    for _, row in min_top10.iterrows():
        report_lines.append(fmt_table_row(row))

    report_lines += [
        "",
        f"**Minority max |EG Δ|:** {min_max_delta:.4f} pp",
        "",
        "---",
        "",
        "## 4. Maximum EG Swing",
        "",
        f"The single overlap-pair reassignment producing the largest EG shift is:",
        "",
        f"- **Map:** {max_swing_row['map']}",
        f"- **Pair:** {max_swing_row['ed_a']} × {max_swing_row['ed_b']}",
        f"- **Area:** {max_swing_row['area_km2']:.2f} km²",
        f"- **VAs affected:** {int(max_swing_row['va_count'])}",
        f"- **EG Δ:** {max_swing_row['eg_delta_pp']:+.4f} pp "
        f"(|{max_swing_row['abs_delta_pp']:.4f}| pp)",
        "",
        "---",
        "",
        "## 5. Conclusion",
        "",
        conclusion,
        "",
        "---",
        "",
        "## 6. Methodology Notes",
        "",
        "- Overlap threshold: >0.01 km² intersection area (filters sub-pixel artefacts).",
        "- VA assignment in overlap zones is determined by which ED polygon appears first in "
        "the GeoPackage row order, since `sjoin` returns the first match when multiple "
        "polygons contain the same centroid.",
        "- EG formula: `EG = (wasted_NDP − wasted_UCP) / total_votes` "
        "(Stephanopoulos & McGhee 2014).",
        "  Wasted votes per district = loser's votes + winner's votes beyond 50%+1.",
        "- The EG swing for each pair is computed by modifying just the two affected EDs' "
        "vote totals and recomputing the full province-wide EG. All other EDs are held fixed.",
        "- Vote totals are from `analysis/assignment_2026_synthetic_totals.csv`.",
    ]

    REPORT_OUT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"  Report written to {REPORT_OUT}")

    # --- Stdout summary ---
    print("\n" + "=" * 60)
    print("OVERLAP ZONE DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(
        f"Majority map: {maj_sum['n_pairs']} overlap pairs | "
        f"{maj_sum['n_va']} VAs | "
        f"{maj_sum['vote_pct']:.3f}% of province votes"
    )
    print(
        f"Minority map: {min_sum['n_pairs']} overlap pairs | "
        f"{min_sum['n_va']} VAs | "
        f"{min_sum['vote_pct']:.3f}% of province votes"
    )
    print(f"\nMax EG swing (majority): {maj_max_delta:.4f} pp")
    print(f"Max EG swing (minority): {min_max_delta:.4f} pp")
    print(f"Overall max EG swing   : {overall_max:.4f} pp")
    print(
        f"\nLargest swing pair: "
        f"{max_swing_row['ed_a']} x {max_swing_row['ed_b']} "
        f"({max_swing_row['map']}, "
        f"{max_swing_row['area_km2']:.2f} km², "
        f"{int(max_swing_row['va_count'])} VAs, "
        f"EG Δ = {max_swing_row['eg_delta_pp']:+.4f} pp)"
    )
    print(f"\nConclusion: {conclusion}")
    print("=" * 60)


if __name__ == "__main__":
    main()
