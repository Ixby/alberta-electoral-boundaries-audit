"""
v11_validate.py — Run T1–T5 equivalent on v11 geometry

Compares v11 against official shapefiles using the same test suite
applied to v0_10, producing a side-by-side comparison table.

Tests:
  IoU     — mean/min IoU of v11 vs official (already computed inline in make_v11,
             but re-computed here for consistency and per-ED detail)
  T1      — VA misassignment rate: how many VA centroids land in the wrong ED
             (should be ~0 since v11 was built by official sjoin)
  T2      — Area fidelity: % area error per ED (v11 vs official)
  T3      — Hausdorff distance per ED (v11 vs official)
  T4      — Efficiency gap, municipal anchoring, NW Calgary excess, Airdrie count
  T5      — Adjacency topology: v11 edges vs official edges

Output:
  outputs/v11_validation_summary.csv
  outputs/v11_iou_per_ed.csv
  outputs/v11_t4_metrics.csv
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

VA_PATH = REPO / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
V11_MAJ = REPO / "data/shapefiles/derived/v11_majority_2026_eds.gpkg"
V11_MIN = REPO / "data/shapefiles/derived/v11_minority_2026_eds.gpkg"
OFF_MAJ = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
CSD_PATH = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"

TOUCH_THRESHOLD = 50  # metres for adjacency
BUFFER_ANCHOR = 50  # metres for municipal anchoring

OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)
OUT_SUMMARY = OUT_DIR / "v11_validation_summary.csv"
OUT_IOU = OUT_DIR / "v11_iou_per_ed.csv"
OUT_T4 = OUT_DIR / "v11_t4_metrics.csv"

# v0_10 baseline results (from prior T1–T5 runs) for comparison
V010_BASELINE = {
    "majority": {
        "mean_iou": 37.78,
        "min_iou": 0.0,
        "t1_misassign_pct": 28.71,
        "eg_pct": 0.636,
        "anchoring_pct": 71.0,
        "nw_excess_pct": 2.8,
        "airdrie_count": 2,
        "t3_mean_hausdorff_m": 19070,
        "t3_max_hausdorff_m": 94993,
        "t5_extra_edges": 68,
        "t5_missing_edges": 60,
    },
    "minority": {
        "mean_iou": 36.32,
        "min_iou": 0.0,
        "t1_misassign_pct": 32.91,
        "eg_pct": 0.111,
        "anchoring_pct": 14.5,
        "nw_excess_pct": 11.5,
        "airdrie_count": 4,
        "t3_mean_hausdorff_m": 22564,
        "t3_max_hausdorff_m": 136657,
        "t5_extra_edges": 136,
        "t5_missing_edges": 103,
    },
}

# Official geometry results (from T4 rerun on official) for reference
OFFICIAL_BASELINE = {
    "majority": {
        "eg_pct": 0.083,
        "anchoring_pct": 48.8,
        "nw_excess_pct": 0.8,
        "airdrie_count": 2,
    },
    "minority": {
        "eg_pct": 3.999,
        "anchoring_pct": 41.1,
        "nw_excess_pct": 6.3,
        "airdrie_count": 4,
    },
}


# ── IoU ──────────────────────────────────────────────────────────────────────


def compute_iou(v11_gdf, off_gdf, label):
    rows = []
    for _, off_row in off_gdf.iterrows():
        off_name = off_row["EDName2025"]
        if off_name not in v11_gdf["EDName2025"].values:
            inter_area = 0.0
            union_area = off_row.geometry.area
            v11_name = None
        else:
            v11_row = v11_gdf[v11_gdf["EDName2025"] == off_name].iloc[0]
            inter_area = off_row.geometry.intersection(v11_row.geometry).area
            union_area = off_row.geometry.union(v11_row.geometry).area
            v11_name = off_name
        iou = inter_area / union_area if union_area > 0 else 0.0
        rows.append(
            {
                "map": label,
                "official_ed": off_name,
                "v11_ed": v11_name,
                "iou_pct": round(iou * 100, 2),
            }
        )
    df = pd.DataFrame(rows)
    return df


# ── T1: VA misassignment ──────────────────────────────────────────────────────


def t1_misassignment(va_gdf, v11_gdf, off_gdf, label):
    centroids = va_gdf.copy()
    centroids.geometry = va_gdf.geometry.centroid

    v11_join = gpd.sjoin(
        centroids[["geometry"]],
        v11_gdf[["geometry", "EDName2025"]],
        how="left",
        predicate="within",
    )
    off_join = gpd.sjoin(
        centroids[["geometry"]],
        off_gdf[["geometry", "EDName2025"]],
        how="left",
        predicate="within",
    )

    v11_ed = v11_join["EDName2025"].fillna("UNASSIGNED")
    off_ed = off_join["EDName2025"].fillna("UNASSIGNED")

    n_total = len(va_gdf)
    n_mismatch = (v11_ed.values != off_ed.values).sum()
    pct = 100.0 * n_mismatch / n_total
    print(
        f"  {label} T1: {n_mismatch}/{n_total} VA centroids misassigned in v11 ({pct:.2f}%)"
    )
    return pct, n_mismatch


# ── T2: Area fidelity ─────────────────────────────────────────────────────────


def t2_area(v11_gdf, off_gdf, label):
    rows = []
    for _, off_row in off_gdf.iterrows():
        name = off_row["EDName2025"]
        off_area = off_row.geometry.area
        if name in v11_gdf["EDName2025"].values:
            v11_area = v11_gdf[v11_gdf["EDName2025"] == name].iloc[0].geometry.area
        else:
            v11_area = 0.0
        err_pct = 100.0 * abs(v11_area - off_area) / off_area if off_area > 0 else 0.0
        rows.append(
            {
                "ed": name,
                "off_area_km2": round(off_area / 1e6, 2),
                "v11_area_km2": round(v11_area / 1e6, 2),
                "abs_err_pct": round(err_pct, 2),
            }
        )
    df = pd.DataFrame(rows)
    mean_err = df["abs_err_pct"].mean()
    max_err = df["abs_err_pct"].max()
    n_over3 = (df["abs_err_pct"] > 3).sum()
    print(
        f"  {label} T2: mean area error {mean_err:.1f}%, max {max_err:.1f}%, {n_over3} EDs >3%"
    )
    return mean_err, max_err, n_over3, df


# ── T3: Hausdorff distance ────────────────────────────────────────────────────


def t3_hausdorff(v11_gdf, off_gdf, label):
    rows = []
    for _, off_row in off_gdf.iterrows():
        name = off_row["EDName2025"]
        if name in v11_gdf["EDName2025"].values:
            v11_geom = v11_gdf[v11_gdf["EDName2025"] == name].iloc[0].geometry
            try:
                hd = off_row.geometry.hausdorff_distance(v11_geom)
            except Exception:
                hd = np.nan
        else:
            hd = np.nan
        rows.append(
            {"ed": name, "hausdorff_m": round(hd, 1) if not np.isnan(hd) else None}
        )
    df = pd.DataFrame(rows).dropna()
    mean_hd = df["hausdorff_m"].mean()
    max_hd = df["hausdorff_m"].max()
    n_over2k = (df["hausdorff_m"] > 2000).sum()
    print(
        f"  {label} T3: mean Hausdorff {mean_hd:.0f} m, max {max_hd:.0f} m, {n_over2k} EDs >2 km"
    )
    return mean_hd, max_hd, n_over2k, df


# ── T4: Headline metrics ──────────────────────────────────────────────────────


def agg_votes(va_gdf, ed_gdf):
    centroids = va_gdf.copy()
    centroids.geometry = va_gdf.geometry.centroid
    joined = gpd.sjoin(
        centroids[["geometry", "va_ndp", "va_ucp"]],
        ed_gdf[["geometry", "EDName2025"]],
        how="left",
        predicate="within",
    )
    missed = joined[joined["EDName2025"].isna()].index
    if len(missed):
        nearest = gpd.sjoin_nearest(
            centroids.loc[missed, ["geometry", "va_ndp", "va_ucp"]],
            ed_gdf[["geometry", "EDName2025"]],
            how="left",
        )
        joined.loc[missed, "EDName2025"] = nearest["EDName2025"].values
    agg = joined.groupby("EDName2025")[["va_ndp", "va_ucp"]].sum().reset_index()
    agg.columns = ["ed", "ndp", "ucp"]
    agg["total"] = agg["ndp"] + agg["ucp"]
    agg["ndp_s"] = agg["ndp"] / agg["total"].replace(0, np.nan)
    agg["ucp_s"] = agg["ucp"] / agg["total"].replace(0, np.nan)
    return agg


def efficiency_gap(vote_df):
    total = vote_df["total"].sum()
    if total == 0:
        return np.nan
    ndp_wins = vote_df[vote_df["ndp"] > vote_df["ucp"]]
    ucp_wins = vote_df[vote_df["ucp"] >= vote_df["ndp"]]
    # NDP wasted = all NDP votes in EDs they lost + NDP surplus in EDs they won
    ndp_wasted = (
        ucp_wins["ndp"].sum()
        + (ndp_wins["ndp"] - (ndp_wins["total"] // 2 + 1)).clip(lower=0).sum()
    )
    # UCP wasted = all UCP votes in EDs they lost + UCP surplus in EDs they won
    ucp_wasted = (
        ndp_wins["ucp"].sum()
        + (ucp_wins["ucp"] - (ucp_wins["total"] // 2 + 1)).clip(lower=0).sum()
    )
    # Positive EG = NDP disadvantaged
    return 100.0 * (ndp_wasted - ucp_wasted) / total


def municipal_anchoring(ed_gdf, csd_gdf, buffer_m=BUFFER_ANCHOR):
    ed_proj = ed_gdf.to_crs("EPSG:3400")
    csd_proj = csd_gdf.to_crs("EPSG:3400")
    csd_boundary = unary_union([g.boundary for g in csd_proj.geometry])
    csd_zone = csd_boundary.buffer(buffer_m)
    total_perim = anchored_len = 0.0
    for _, row in ed_proj.iterrows():
        b = row.geometry.boundary
        total_perim += b.length
        try:
            anchored_len += b.intersection(csd_zone).length
        except Exception:
            pass
    return 100.0 * anchored_len / total_perim if total_perim > 0 else 0.0


def nw_calgary_excess(vote_df):
    nw_eds = [
        e
        for e in vote_df["ed"]
        if "Calgary-North West" in e
        or "Calgary-Symons" in e
        or "Calgary-Edgemont" in e
        or "Calgary-Nose Creek" in e
        or "Calgary-North" in e
        and "North East" not in e
    ]
    total_pop = vote_df["total"].sum()
    if total_pop == 0:
        return 0.0
    nw_pop = vote_df[vote_df["ed"].isin(nw_eds)]["total"].sum()
    nw_eds_count = max(len(nw_eds), 1)
    nw_share = nw_pop / total_pop
    expected = nw_eds_count / len(vote_df)
    return 100.0 * (nw_share - expected)


def airdrie_count(v11_gdf):
    return v11_gdf["EDName2025"].str.contains("Airdrie", case=False).sum()


def t4_metrics(va_gdf, v11_gdf, off_gdf, csd_gdf, label):
    votes = agg_votes(va_gdf, v11_gdf)
    eg = efficiency_gap(votes)
    anchor = municipal_anchoring(v11_gdf, csd_gdf)
    nw = nw_calgary_excess(votes)
    airdrie = airdrie_count(v11_gdf)
    print(
        f"  {label} T4: EG={eg:+.3f}%  anchoring={anchor:.1f}%  NW_excess={nw:+.1f}%  Airdrie={airdrie}"
    )
    return {
        "eg_pct": round(eg, 3),
        "anchoring_pct": round(anchor, 1),
        "nw_excess_pct": round(nw, 1),
        "airdrie_count": airdrie,
    }


# ── T5: Adjacency topology ───────────────────────────────────────────────────


def build_adjacency(gdf, name_col, threshold=TOUCH_THRESHOLD):
    gdf = gdf.copy()
    gdf["_name"] = gdf[name_col].str.strip()
    edges = set()
    n = len(gdf)
    for i in range(n):
        for j in range(i + 1, n):
            try:
                shared = gdf.iloc[i].geometry.intersection(gdf.iloc[j].geometry)
                if shared.is_empty:
                    continue
                if shared.geom_type in ("LineString", "MultiLineString"):
                    length = shared.length
                elif shared.geom_type == "GeometryCollection":
                    length = sum(
                        g.length
                        for g in shared.geoms
                        if g.geom_type in ("LineString", "MultiLineString")
                    )
                else:
                    length = 0
                if length >= threshold:
                    edges.add(frozenset([gdf.iloc[i]["_name"], gdf.iloc[j]["_name"]]))
            except Exception:
                pass
    return edges


def t5_adjacency(v11_gdf, off_gdf, label):
    print(f"  {label} T5: building v11 adjacency...")
    v11_adj = build_adjacency(v11_gdf, "EDName2025")
    print(f"  {label} T5: building official adjacency...")
    off_adj = build_adjacency(off_gdf, "EDName2025")
    shared = len(v11_adj & off_adj)
    v11_only = len(v11_adj - off_adj)
    off_only = len(off_adj - v11_adj)
    print(
        f"  {label} T5: v11={len(v11_adj)} official={len(off_adj)} "
        f"shared={shared} v11-only={v11_only} off-only={off_only}"
    )
    return len(v11_adj), len(off_adj), shared, v11_only, off_only


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    print("Loading data...")
    va = gpd.read_file(VA_PATH).to_crs("EPSG:3400")
    csd = gpd.read_file(CSD_PATH).to_crs("EPSG:3400") if CSD_PATH.exists() else None

    if csd is None:
        print("  WARNING: CSD shapefile not found — T4 anchoring will be skipped")

    iou_rows = []
    t4_rows = []
    sum_rows = []

    for label, v11_path, off_path in [
        ("majority", V11_MAJ, OFF_MAJ),
        ("minority", V11_MIN, OFF_MIN),
    ]:
        print(f"\n=== {label} ===")
        v11 = gpd.read_file(v11_path).to_crs("EPSG:3400")
        off = gpd.read_file(off_path).to_crs("EPSG:3400")

        # IoU
        iou_df = compute_iou(v11, off, label)
        mean_iou = iou_df["iou_pct"].mean()
        min_iou = iou_df["iou_pct"].min()
        n_low = (iou_df["iou_pct"] < 90).sum()
        print(f"  {label} IoU: mean={mean_iou:.1f}% min={min_iou:.1f}% n<90%={n_low}")
        iou_rows.append(iou_df)

        # T1
        t1_pct, t1_n = t1_misassignment(va, v11, off, label)

        # T2
        t2_mean, t2_max, t2_n, _ = t2_area(v11, off, label)

        # T3
        t3_mean, t3_max, t3_n, _ = t3_hausdorff(v11, off, label)

        # T4
        t4 = {}
        if csd is not None:
            t4 = t4_metrics(va, v11, off, csd, label)
        else:
            print(f"  {label} T4: skipped (no CSD file)")

        # T5 (slow — adjacency rebuild)
        print(f"  Building adjacency for T5...")
        v11_edges, off_edges, shared, extra, missing = t5_adjacency(v11, off, label)

        # Summary row
        b = V010_BASELINE[label]
        o = OFFICIAL_BASELINE[label]
        row = {
            "map": label,
            # IoU
            "v010_mean_iou": b["mean_iou"],
            "v11_mean_iou": round(mean_iou, 2),
            "v010_min_iou": b["min_iou"],
            "v11_min_iou": round(min_iou, 2),
            # T1
            "v010_t1_misassign_pct": b["t1_misassign_pct"],
            "v11_t1_misassign_pct": round(t1_pct, 2),
            # T2
            "v11_t2_mean_area_err_pct": round(t2_mean, 1),
            "v11_t2_n_over3pct": t2_n,
            # T3
            "v010_t3_mean_hd_m": b["t3_mean_hausdorff_m"],
            "v11_t3_mean_hd_m": round(t3_mean, 0),
            "v010_t3_max_hd_m": b["t3_max_hausdorff_m"],
            "v11_t3_max_hd_m": round(t3_max, 0),
            # T4
            "v010_eg": b["eg_pct"],
            "v11_eg": t4.get("eg_pct"),
            "official_eg": o["eg_pct"],
            "v010_anchor": b["anchoring_pct"],
            "v11_anchor": t4.get("anchoring_pct"),
            "official_anchor": o["anchoring_pct"],
            "v010_nw": b["nw_excess_pct"],
            "v11_nw": t4.get("nw_excess_pct"),
            "official_nw": o["nw_excess_pct"],
            "v010_airdrie": b["airdrie_count"],
            "v11_airdrie": t4.get("airdrie_count"),
            # T5
            "v010_extra_edges": b["t5_extra_edges"],
            "v11_extra_edges": extra,
            "v010_missing_edges": b["t5_missing_edges"],
            "v11_missing_edges": missing,
            "off_edges": off_edges,
        }
        sum_rows.append(row)
        if t4:
            t4_rows.append({"map": label, **t4})

    pd.concat(iou_rows, ignore_index=True).to_csv(OUT_IOU, index=False)
    pd.DataFrame(sum_rows).to_csv(OUT_SUMMARY, index=False)
    if t4_rows:
        pd.DataFrame(t4_rows).to_csv(OUT_T4, index=False)
    print(f"Saved -> {OUT_SUMMARY}")
    print(f"Saved -> {OUT_IOU}")

    print("\n=== v0_10 vs v11 Summary ===")
    for row in sum_rows:
        m = row["map"]
        print(f"\n  {m}:")
        print(
            f"    IoU:       v0_10 {row['v010_mean_iou']:.1f}%  ->  v11 {row['v11_mean_iou']:.1f}%"
        )
        print(
            f"    T1 miss:   v0_10 {row['v010_t1_misassign_pct']:.1f}%  ->  v11 {row['v11_t1_misassign_pct']:.1f}%"
        )
        print(
            f"    T3 Haus:   v0_10 {row['v010_t3_mean_hd_m']:.0f} m  ->  v11 {row['v11_t3_mean_hd_m']:.0f} m"
        )
        if row["v11_eg"] is not None:
            print(
                f"    EG:        v0_10 {row['v010_eg']:+.3f}%  ->  v11 {row['v11_eg']:+.3f}%  (official {row['official_eg']:+.3f}%)"
            )
            print(
                f"    Anchoring: v0_10 {row['v010_anchor']:.1f}%  ->  v11 {row['v11_anchor']:.1f}%  (official {row['official_anchor']:.1f}%)"
            )
        print(
            f"    T5 extra:  v0_10 {row['v010_extra_edges']}  ->  v11 {row['v11_extra_edges']}"
        )
        print(
            f"    T5 miss:   v0_10 {row['v010_missing_edges']}  ->  v11 {row['v11_missing_edges']}"
        )


if __name__ == "__main__":
    main()
