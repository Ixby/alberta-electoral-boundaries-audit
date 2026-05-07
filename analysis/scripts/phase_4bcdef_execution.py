"""Phases 4B / 4C / 4D-4E / 4F execution — geometric data-provenance pipeline.

This script executes the remaining "not attempted" / "blocked" phases in
Appendix E of report_academic.md:

  Phase 4B — DA dissolve to 2026 EDs (per-ED 2021-census population)
  Phase 4C — VA-polygon 2023-vote attribution (per-ED 2023 vote totals)
  Phase 4D/4E — SUPERSEDED (no OSM / QGIS execution)
  Phase 4F — Validation against commission-published populations

Methodology follows v0_1_mcmc_full_coverage_rescore_100k.py:
  - Primary assignment: centroid-in-polygon via representative_point().
  - Fallback: parent_ed_2019 -> full-crosswalk -> 2026 ED name.
  - Sources:
    * Majority: approximate polygons (57) + Tier A 2019 identity shapes.
    * Minority: v6 refined polygons (70) + v7 derived polygons (89 with
      84 having geometry) + Tier A 2019 identity shapes.

Outputs:
  data/v0_1_population_2021_majority.csv
  data/v0_1_population_2021_minority.csv
  data/votes_2023_majority.csv
  data/votes_2023_minority.csv
  data/v0_1_validation_deltas.csv
  analysis/v0_1_phase_4bcdef_execution.md  (companion write-up)

Forward: analysis/v0_1_phase_4bcdef_execution.md
Backward:
  data/alberta_2021_das.gpkg
  data/alberta_2021_da_populations.csv
  data/v0_1_approximate_majority_2026_eds.gpkg
  data/v0_1_refined_v6_minority_2026_eds.gpkg
  data/v0_1_derived_v7_minority_2026_eds.gpkg
  data/majority_full_crosswalk.csv
  data/minority_full_crosswalk.csv
  data/va_polygons_with_2023_votes.gpkg
  data/majority_2026_populations.csv
  data/minority_2026_populations.csv
  data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
"""

# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations
import json
import sys
import time
import unicodedata
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"

# --- inputs ---
DAS_GPKG = DATA / "shapefiles" / "reference" / "alberta_2021_das.gpkg"
DA_POPS_CSV = DATA / "alberta_2021_da_populations.csv"
EDS_2019_SHP = (
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)

MAJ_CANON_GPKG = (
    DATA / "shapefiles" / "derived" / "v0_1_canonical_majority_2026_eds.gpkg"
)
MIN_CANON_GPKG = (
    DATA / "shapefiles" / "derived" / "v0_1_canonical_minority_2026_eds.gpkg"
)

MAJ_XWALK_CSV = DATA / "majority_full_crosswalk.csv"
MIN_XWALK_CSV = DATA / "minority_full_crosswalk.csv"

VA_GPKG = DATA / "shapefiles" / "derived" / "va_polygons_with_full_2023_votes.gpkg"

MAJ_POPS_CSV = DATA / "majority_2026_populations.csv"
MIN_POPS_CSV = DATA / "minority_2026_populations.csv"

# --- outputs ---
OUT_4B_MAJ = DATA / "v0_1_population_2021_majority.csv"
OUT_4B_MIN = DATA / "v0_1_population_2021_minority.csv"
OUT_4C_MAJ = DATA / "votes_2023_majority.csv"
OUT_4C_MIN = DATA / "votes_2023_minority.csv"
OUT_4F = DATA / "v0_1_validation_deltas.csv"


def norm(s: str) -> str:
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return ""
    s = str(s).strip()
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    return unicodedata.normalize("NFC", s)


def load_crosswalk(path: Path) -> dict[str, str]:
    df = pd.read_csv(path)
    return {norm(r["current_2019"]): norm(r["proposed_2026"]) for _, r in df.iterrows()}


def load_2019_eds_by_name() -> gpd.GeoDataFrame:
    g = gpd.read_file(EDS_2019_SHP)
    g["name_2019_norm"] = g["EDName2017"].apply(norm)
    return g


def build_coverage_polygons(
    canon: gpd.GeoDataFrame,
    target_names: list[str],
    target_crs,
    map_label: str,
) -> tuple[gpd.GeoDataFrame, dict[str, str]]:
    """Align canonical 2026 ED shapefile to the target name list.

    Session 11 canonical shapefiles deliver 89 EDs with all polygons populated
    and per-ED tier/source metadata under `canon_source`. This function
    reprojects, normalises names, and orders rows against the commission
    `ed_name` list so downstream assign / summarise code can consume
    `polys` + `sources` unchanged.

    Returns: (GeoDataFrame with name_2026 + geometry, source dict)
    """
    canon = canon.to_crs(target_crs).copy()
    canon["_name_norm"] = canon["name_2026"].apply(norm)
    if "canon_source" not in canon.columns:
        canon["canon_source"] = "canonical"

    canon_by_name = {
        n: (row.geometry, row.get("canon_source", "canonical"))
        for n, row in canon.set_index("_name_norm").iterrows()
        if row.geometry is not None and not row.geometry.is_empty
    }

    rows: list[dict] = []
    sources: dict[str, str] = {}
    missing: list[str] = []
    for name in target_names:
        nm = norm(name)
        if nm in canon_by_name:
            geom, src = canon_by_name[nm]
            rows.append(
                {
                    "name_2026": name,
                    "_name_norm": nm,
                    "geometry": geom,
                    "source": str(src),
                }
            )
            sources[nm] = str(src)
        else:
            rows.append(
                {
                    "name_2026": name,
                    "_name_norm": nm,
                    "geometry": None,
                    "source": "none",
                }
            )
            sources[nm] = "none"
            missing.append(name)

    gdf = gpd.GeoDataFrame(rows, crs=target_crs)
    source_counts = {}
    for s in sources.values():
        source_counts[s] = source_counts.get(s, 0) + 1
    print(
        f"  [{map_label}] canonical coverage (n={len(target_names)}): "
        + ", ".join(f"{k}={v}" for k, v in sorted(source_counts.items()))
    )
    if missing:
        print(f"  [{map_label}] missing canonical rows for: {missing}")
    return gdf, sources


def assign_das_to_ed(das: gpd.GeoDataFrame, polys: gpd.GeoDataFrame) -> pd.DataFrame:
    """Assign each DA to a 2026 ED by centroid-in-polygon.

    Returns a DataFrame with columns [DAUID, name_2026] (name may be NaN).
    """
    # use polygons with geometry only
    polys_valid = polys[polys.geometry.notna()].copy()
    polys_valid = polys_valid.to_crs(das.crs)
    centroids = das.copy()
    centroids["geometry"] = das.geometry.representative_point()
    joined = gpd.sjoin(
        centroids[["DAUID", "geometry"]],
        polys_valid[["name_2026", "geometry"]],
        how="left",
        predicate="within",
    )
    joined = joined[~joined.index.duplicated(keep="first")]
    return joined[["DAUID", "name_2026"]].copy()


def run_phase_4b() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Phase 4B — dissolve 2021 DAs into 2026 ED polygons, sum populations."""
    print("[Phase 4B] Loading DAs and DA populations...")
    das = gpd.read_file(DAS_GPKG)
    da_pops = pd.read_csv(DA_POPS_CSV)
    da_pops["DAUID"] = da_pops["DAUID"].astype(str)
    das["DAUID"] = das["DAUID"].astype(str)
    das = das.merge(da_pops[["DAUID", "population_2021"]], on="DAUID", how="left")
    print(f"  DAs: {len(das)}, total pop: {das['population_2021'].sum():,.0f}")

    print("[Phase 4B] Loading crosswalks and canonical polygons...")
    maj_xwalk = load_crosswalk(MAJ_XWALK_CSV)
    min_xwalk = load_crosswalk(MIN_XWALK_CSV)

    maj_canon = gpd.read_file(MAJ_CANON_GPKG)
    min_canon = gpd.read_file(MIN_CANON_GPKG)

    maj_names = pd.read_csv(MAJ_POPS_CSV)["ed_name"].tolist()
    min_names = pd.read_csv(MIN_POPS_CSV)["ed_name"].tolist()

    # Align canonical 89-row coverage to commission name order
    maj_polys, maj_sources = build_coverage_polygons(
        maj_canon, maj_names, das.crs, "majority"
    )
    min_polys, min_sources = build_coverage_polygons(
        min_canon, min_names, das.crs, "minority"
    )

    # Assign DAs to 2026 EDs (polygon-based)
    print("[Phase 4B] Assigning DAs to majority 2026 EDs...")
    maj_assign = assign_das_to_ed(das, maj_polys)
    print("[Phase 4B] Assigning DAs to minority 2026 EDs...")
    min_assign = assign_das_to_ed(das, min_polys)

    # Sum DA populations per ED
    das_maj = das.merge(maj_assign, on="DAUID", how="left")
    das_min = das.merge(min_assign, on="DAUID", how="left")

    def summarize(
        das_w: pd.DataFrame, names: list[str], sources: dict[str, str], label: str
    ) -> pd.DataFrame:
        das_w = das_w.copy()
        das_w["_assigned_norm"] = das_w["name_2026"].apply(
            lambda x: norm(x) if pd.notna(x) else None
        )
        agg = (
            das_w.dropna(subset=["_assigned_norm"])
            .groupby("_assigned_norm")["population_2021"]
            .sum()
            .reset_index()
        )
        agg.columns = ["_name_norm", "pop_4b_sum"]

        rows = []
        unassigned_total = float(
            das_w[das_w["_assigned_norm"].isna()]["population_2021"].sum()
        )
        for name in names:
            nm = norm(name)
            sub = agg[agg["_name_norm"] == nm]
            pop = float(sub["pop_4b_sum"].iloc[0]) if len(sub) > 0 else 0.0
            rows.append(
                {
                    "ed_name": name,
                    "pop_2021_from_das": pop,
                    "polygon_source": sources.get(nm, "none"),
                }
            )
        out = pd.DataFrame(rows)
        n_zero = int((out["pop_2021_from_das"] == 0).sum())
        print(
            f"  [{label}] total assigned pop: {out['pop_2021_from_das'].sum():,.0f}, "
            f"unassigned pop: {unassigned_total:,.0f}, n zero-pop EDs: {n_zero}"
        )
        return out

    maj_out = summarize(das_maj, maj_names, maj_sources, "majority")
    min_out = summarize(das_min, min_names, min_sources, "minority")

    maj_out.to_csv(OUT_4B_MAJ, index=False)
    min_out.to_csv(OUT_4B_MIN, index=False)
    print(f"[Phase 4B] Wrote {OUT_4B_MAJ.name}, {OUT_4B_MIN.name}")
    return maj_out, min_out


def run_phase_4c() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Phase 4C — VA polygons centroid-in-2026-ED, sum 2023 vote totals per ED."""
    print(
        "[Phase 4C] Loading VA polygons with full (Election-Day + splat) 2023 votes..."
    )
    vas = gpd.read_file(VA_GPKG)
    print(
        f"  VAs: {len(vas)}, UCP: {vas['va_ucp_full'].sum():,.0f}, "
        f"NDP: {vas['va_ndp_full'].sum():,.0f}, Other: {vas['va_other_full'].sum():,.0f}, "
        f"two-party: {vas['va_ucp_full'].sum() + vas['va_ndp_full'].sum():,.0f}"
    )

    maj_xwalk = load_crosswalk(MAJ_XWALK_CSV)
    min_xwalk = load_crosswalk(MIN_XWALK_CSV)

    maj_canon = gpd.read_file(MAJ_CANON_GPKG)
    min_canon = gpd.read_file(MIN_CANON_GPKG)

    maj_names = pd.read_csv(MAJ_POPS_CSV)["ed_name"].tolist()
    min_names = pd.read_csv(MIN_POPS_CSV)["ed_name"].tolist()

    maj_polys, maj_sources = build_coverage_polygons(
        maj_canon, maj_names, vas.crs, "majority"
    )
    min_polys, min_sources = build_coverage_polygons(
        min_canon, min_names, vas.crs, "minority"
    )

    def assign_and_summarize(
        polys: gpd.GeoDataFrame,
        xwalk: dict[str, str],
        names: list[str],
        sources: dict[str, str],
        label: str,
    ) -> pd.DataFrame:
        vas_ = vas.copy()
        vas_["_parent2019"] = vas_["parent_ed_2019"].astype(str).apply(norm)

        polys_valid = polys[polys.geometry.notna()].copy().to_crs(vas_.crs)
        centroids = vas_.copy()
        centroids["geometry"] = vas_.geometry.representative_point()
        joined = gpd.sjoin(
            centroids[["OBJECTID", "geometry"]],
            polys_valid[["name_2026", "geometry"]],
            how="left",
            predicate="within",
        )
        joined = joined[~joined.index.duplicated(keep="first")]
        vas_["_assigned_poly"] = (
            joined["name_2026"].apply(lambda x: norm(x) if pd.notna(x) else None).values
        )

        vas_["_assigned_xwalk"] = (
            vas_["_parent2019"].map(xwalk).fillna(vas_["_parent2019"])
        )
        vas_["ed_2026"] = vas_["_assigned_poly"].fillna(vas_["_assigned_xwalk"])

        agg = (
            vas_.groupby("ed_2026")
            .agg(
                ucp=("va_ucp_full", "sum"),
                ndp=("va_ndp_full", "sum"),
                other=("va_other_full", "sum"),
            )
            .reset_index()
        )
        agg["ed_2026_norm"] = agg["ed_2026"].apply(norm)

        rows = []
        for name in names:
            nm = norm(name)
            sub = agg[agg["ed_2026_norm"] == nm]
            if len(sub) == 0:
                rows.append(
                    {
                        "ed_name": name,
                        "ucp_2023": 0,
                        "ndp_2023": 0,
                        "other_2023": 0,
                        "polygon_source": sources.get(nm, "none"),
                        "total_votes": 0,
                    }
                )
            else:
                ucp = int(sub["ucp"].iloc[0])
                ndp = int(sub["ndp"].iloc[0])
                oth = int(sub["other"].iloc[0])
                rows.append(
                    {
                        "ed_name": name,
                        "ucp_2023": ucp,
                        "ndp_2023": ndp,
                        "other_2023": oth,
                        "polygon_source": sources.get(nm, "none"),
                        "total_votes": ucp + ndp + oth,
                    }
                )

        df = pd.DataFrame(rows)
        via_poly = int(vas_["_assigned_poly"].notna().sum())
        via_xwalk = int(vas_["_assigned_poly"].isna().sum())
        print(f"  [{label}] VAs via polygon: {via_poly}, via crosswalk: {via_xwalk}")
        print(
            f"  [{label}] sums: UCP={df['ucp_2023'].sum():,}, "
            f"NDP={df['ndp_2023'].sum():,}, Other={df['other_2023'].sum():,}, "
            f"two-party={df['ucp_2023'].sum() + df['ndp_2023'].sum():,}"
        )
        return df

    maj_out = assign_and_summarize(
        maj_polys, maj_xwalk, maj_names, maj_sources, "majority"
    )
    min_out = assign_and_summarize(
        min_polys, min_xwalk, min_names, min_sources, "minority"
    )

    maj_out.to_csv(OUT_4C_MAJ, index=False)
    min_out.to_csv(OUT_4C_MIN, index=False)
    print(f"[Phase 4C] Wrote {OUT_4C_MAJ.name}, {OUT_4C_MIN.name}")
    return maj_out, min_out


def run_phase_4f(maj_4b: pd.DataFrame, min_4b: pd.DataFrame) -> pd.DataFrame:
    """Phase 4F — validation against commission-published per-ED populations.

    IMPORTANT caveat: the commission's "published population" is drawn from
    Alberta Treasury Board and Finance's July 2024 estimate
    (total 4,888,723), not from the 2021 decennial census
    (total 4,262,635). The per-ED delta therefore measures two effects
    combined: (a) true intercensal population growth per ED (~14.7% on
    average, but uneven — Calgary ring grew faster), and (b) polygon-
    geometry attribution error.

    We report two normalisations:
      - raw delta (my pop − commission pop), which reflects (a)+(b).
      - growth-adjusted delta (my pop × 1.147 − commission pop), which
        removes the average-growth component and surfaces (b).
    """
    print("[Phase 4F] Loading commission populations...")
    maj_pubs = pd.read_csv(MAJ_POPS_CSV)[["ed_name", "population"]].copy()
    maj_pubs.columns = ["ed_name", "pop_commission"]
    min_pubs = pd.read_csv(MIN_POPS_CSV)[["ed_name", "population"]].copy()
    min_pubs.columns = ["ed_name", "pop_commission"]

    # province-wide growth scale factor
    da_pops = pd.read_csv(DA_POPS_CSV)
    province_2021 = da_pops["population_2021"].sum()
    commission_total = maj_pubs["pop_commission"].sum()
    growth_factor = commission_total / province_2021
    print(f"  Province 2021 (DA sum): {province_2021:,.0f}")
    print(f"  Commission total (TBF Jul 2024): {commission_total:,.0f}")
    print(
        f"  Implied growth factor: {growth_factor:.4f} ({100*(growth_factor-1):.2f}%)"
    )

    def prep(df, pubs, label):
        d = df.merge(pubs, on="ed_name", how="left").copy()
        d["pop_scaled_to_commission_total"] = d["pop_2021_from_das"] * growth_factor
        d["delta_raw"] = d["pop_2021_from_das"] - d["pop_commission"]
        d["delta_raw_pct"] = (
            100.0 * d["delta_raw"] / d["pop_commission"].replace({0: np.nan})
        )
        d["delta_scaled"] = d["pop_scaled_to_commission_total"] - d["pop_commission"]
        d["delta_scaled_pct"] = (
            100.0 * d["delta_scaled"] / d["pop_commission"].replace({0: np.nan})
        )
        d["map"] = label
        return d

    maj = prep(maj_4b, maj_pubs, "majority")
    mino = prep(min_4b, min_pubs, "minority")

    combined = pd.concat([maj, mino], ignore_index=True)
    combined["flag_warn_0p5pct_scaled"] = combined["delta_scaled_pct"].abs() > 0.5
    combined["flag_hardstop_2pct_scaled"] = combined["delta_scaled_pct"].abs() > 2.0

    combined_out = combined[
        [
            "map",
            "ed_name",
            "pop_2021_from_das",
            "pop_scaled_to_commission_total",
            "pop_commission",
            "delta_raw",
            "delta_raw_pct",
            "delta_scaled",
            "delta_scaled_pct",
            "flag_warn_0p5pct_scaled",
            "flag_hardstop_2pct_scaled",
            "polygon_source",
        ]
    ].copy()
    combined_out.to_csv(OUT_4F, index=False)
    print(f"[Phase 4F] Wrote {OUT_4F.name}")

    # summary stats per map (use scaled delta for the 2% threshold)
    for label, df in [("majority", maj), ("minority", mino)]:
        d = df.dropna(subset=["delta_scaled"])
        d_nz = d[d["pop_2021_from_das"] > 0]  # exclude zero-pop (no polygon) rows
        print(f"  [{label}] n={len(d)} (nonzero={len(d_nz)}):")
        print(
            f"    RAW delta: mean={d['delta_raw'].mean():.0f}, "
            f"median={d['delta_raw'].median():.0f}, "
            f"max_abs={d['delta_raw'].abs().max():.0f}, "
            f"RMS={np.sqrt((d['delta_raw']**2).mean()):.0f}"
        )
        print(
            f"    SCALED delta: mean={d_nz['delta_scaled'].mean():.0f}, "
            f"median={d_nz['delta_scaled'].median():.0f}, "
            f"max_abs={d_nz['delta_scaled'].abs().max():.0f}, "
            f"RMS={np.sqrt((d_nz['delta_scaled']**2).mean()):.0f}"
        )
        print(
            f"    warn 0.5% (scaled, nonzero): {int(d_nz['delta_scaled_pct'].abs().gt(0.5).sum())}"
        )
        print(
            f"    hardstop 2% (scaled, nonzero): {int(d_nz['delta_scaled_pct'].abs().gt(2.0).sum())}"
        )

    return combined_out


def compute_summary(maj_4b, min_4b, maj_4c, min_4c, combined_4f) -> dict:
    summary = {}

    # Phase 4B stats
    summary["phase_4b"] = {}
    for label, df in [("majority", maj_4b), ("minority", min_4b)]:
        summary["phase_4b"][label] = {
            "n_eds": int(len(df)),
            "total_pop_2021_from_das": float(df["pop_2021_from_das"].sum()),
            "source_counts": df["polygon_source"].value_counts().to_dict(),
        }
    # Province total
    maj_total = maj_4b["pop_2021_from_das"].sum()
    min_total = min_4b["pop_2021_from_das"].sum()
    # Province 2021 census total from DA pop
    da_pops = pd.read_csv(DA_POPS_CSV)
    province_2021 = da_pops["population_2021"].sum()
    summary["phase_4b"]["province_2021_from_das"] = float(province_2021)
    summary["phase_4b"]["majority_sum_vs_province"] = float(maj_total / province_2021)
    summary["phase_4b"]["minority_sum_vs_province"] = float(min_total / province_2021)

    # Phase 4C stats
    summary["phase_4c"] = {}
    for label, df in [("majority", maj_4c), ("minority", min_4c)]:
        ucp = int(df["ucp_2023"].sum())
        ndp = int(df["ndp_2023"].sum())
        oth = int(df["other_2023"].sum())
        summary["phase_4c"][label] = {
            "n_eds": int(len(df)),
            "ucp_total": ucp,
            "ndp_total": ndp,
            "other_total": oth,
            "two_party_total": ucp + ndp,
            "all_votes": ucp + ndp + oth,
        }

    # Phase 4F validation
    summary["phase_4f"] = {}
    da_pops = pd.read_csv(DA_POPS_CSV)
    commission_maj = pd.read_csv(MAJ_POPS_CSV)["population"].sum()
    summary["phase_4f"]["province_2021_from_das"] = float(
        da_pops["population_2021"].sum()
    )
    summary["phase_4f"]["commission_total_tbf_jul2024"] = float(commission_maj)
    summary["phase_4f"]["growth_factor"] = float(
        commission_maj / da_pops["population_2021"].sum()
    )
    for label in ["majority", "minority"]:
        sub = combined_4f[combined_4f["map"] == label].dropna(subset=["delta_scaled"])
        nz = sub[sub["pop_2021_from_das"] > 0]
        summary["phase_4f"][label] = {
            "n": int(len(sub)),
            "n_nonzero_pop": int(len(nz)),
            "mean_delta_raw": float(sub["delta_raw"].mean()),
            "median_delta_raw": float(sub["delta_raw"].median()),
            "max_abs_delta_raw": float(sub["delta_raw"].abs().max()),
            "rms_delta_raw": float(np.sqrt((sub["delta_raw"] ** 2).mean())),
            "mean_delta_scaled_nonzero": float(nz["delta_scaled"].mean()),
            "median_delta_scaled_nonzero": float(nz["delta_scaled"].median()),
            "max_abs_delta_scaled_nonzero": float(nz["delta_scaled"].abs().max()),
            "rms_delta_scaled_nonzero": float(
                np.sqrt((nz["delta_scaled"] ** 2).mean())
            ),
            "max_abs_delta_scaled_pct_nonzero": float(
                nz["delta_scaled_pct"].abs().max()
            ),
            "n_warn_0p5pct_scaled_nonzero": int(
                nz["delta_scaled_pct"].abs().gt(0.5).sum()
            ),
            "n_hardstop_2pct_scaled_nonzero": int(
                nz["delta_scaled_pct"].abs().gt(2.0).sum()
            ),
        }

    return summary


def main():
    t0 = time.time()
    maj_4b, min_4b = run_phase_4b()
    print(f"  [Phase 4B elapsed: {time.time()-t0:.1f}s]")

    t1 = time.time()
    maj_4c, min_4c = run_phase_4c()
    print(f"  [Phase 4C elapsed: {time.time()-t1:.1f}s]")

    t2 = time.time()
    combined_4f = run_phase_4f(maj_4b, min_4b)
    print(f"  [Phase 4F elapsed: {time.time()-t2:.1f}s]")

    summary = compute_summary(maj_4b, min_4b, maj_4c, min_4c, combined_4f)
    summary_path = DATA / "pipeline_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[SUMMARY] Wrote {summary_path.name}")
    print(json.dumps(summary, indent=2, default=str))

    print(f"\n[TOTAL elapsed: {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
