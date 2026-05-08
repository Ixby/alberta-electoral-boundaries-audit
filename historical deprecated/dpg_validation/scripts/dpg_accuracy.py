"""
DPG Accuracy — How close were the v0_10 derived geometries to the official shapefiles?

For each ED, computes Jaccard similarity (Intersection over Union) between the
DPG polygon and its matched official polygon, expressed as a percentage.
  100% = geometrically identical
  0%   = no overlap at all

EDs whose DPG polygon matches the 2019 enacted map to >= 99.5% IoU are flagged
as '2019_inherited' (the commission made no change there; the DPG just copied
the enacted boundary). These are noted but EXCLUDED from the aggregate accuracy
figures — they would inflate the score and don't test the reconstruction method.

Output:
  outputs/dpg_accuracy.csv   — per-ED detail for both maps
  outputs/dpg_accuracy_summary.md — plain-text result card
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

DPG_MAJ = REPO / "data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg"
DPG_MIN = REPO / "data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg"
OFF_MAJ = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
ED_2019 = REPO / "data/shapefiles/reference/alberta_2019_eds"
OUT_CSV = ROOT / "outputs/dpg_accuracy.csv"
OUT_MD = ROOT / "outputs/dpg_accuracy_summary.md"
OUT_CSV.parent.mkdir(exist_ok=True)

INHERITED_THRESHOLD = 99.5  # IoU % above which we call an ED "2019-inherited"


def jaccard(geom_a, geom_b):
    """Intersection-over-union as a percentage."""
    try:
        inter = geom_a.intersection(geom_b).area
        union = geom_a.union(geom_b).area
        return 100.0 * inter / union if union > 0 else 0.0
    except Exception:
        return np.nan


import re


def normalize_name(s):
    """Lowercase, remove punctuation, collapse whitespace."""
    s = s.lower()
    s = re.sub(r"[.\-']", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build_name_index(off_gdf):
    return {normalize_name(row["EDName2025"]): idx for idx, row in off_gdf.iterrows()}


def best_match(dpg_row, off_gdf, name_index=None):
    """
    Match by normalized name first; fall back to max-area spatial overlap.
    Returns (official_row, match_method).
    """
    if name_index is not None:
        dpg_norm = normalize_name(dpg_row["name_2026"].strip())
        if dpg_norm in name_index:
            return off_gdf.loc[name_index[dpg_norm]], "name"
        print(f"  NAME MISS: '{dpg_row['name_2026'].strip()}' -> spatial fallback")

    off_copy = off_gdf.copy()
    off_copy["_iarea"] = off_gdf.geometry.intersection(dpg_row.geometry).area
    best_idx = off_copy["_iarea"].idxmax()
    return off_gdf.loc[best_idx], "spatial_fallback"


def run_map(label, dpg_path, off_path, enacted_2019):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")

    dpg = gpd.read_file(dpg_path).to_crs("EPSG:3400")
    off = gpd.read_file(off_path).to_crs("EPSG:3400")
    off_idx = build_name_index(off)

    # Build 2019 name index using the name column that exists
    enacted_idx = None
    if enacted_2019 is not None:
        e_name_col = next(
            (c for c in enacted_2019.columns if "name" in c.lower()), None
        )
        if e_name_col:
            enacted_idx = {
                normalize_name(r[e_name_col]): i for i, r in enacted_2019.iterrows()
            }

    rows = []
    for _, dpg_row in dpg.iterrows():
        dpg_name = dpg_row["name_2026"].strip()
        official, match_method = best_match(dpg_row, off, off_idx)
        iou_off = jaccard(dpg_row.geometry, official.geometry)

        # Check against 2019 enacted (spatial only — names differ between 2019/2026)
        if enacted_2019 is not None:
            enacted_row, _ = best_match(dpg_row, enacted_2019, None)
            iou_2019 = jaccard(dpg_row.geometry, enacted_row.geometry)
            is_inherited = iou_2019 >= INHERITED_THRESHOLD
            e_name_col = next(
                (c for c in enacted_2019.columns if "name" in c.lower()), None
            )
            enacted_name = enacted_row[e_name_col] if e_name_col else ""
        else:
            iou_2019 = np.nan
            is_inherited = False
            enacted_name = ""

        rows.append(
            {
                "map": label,
                "dpg_name": dpg_name,
                "official_name": official["EDName2025"],
                "official_ed_num": official["EDNum2025"],
                "official_pop": official["PopCensus"],
                "match_method": match_method,
                "iou_vs_official_pct": round(iou_off, 2),
                "iou_vs_2019_pct": (
                    round(iou_2019, 2) if not np.isnan(iou_2019) else None
                ),
                "is_2019_inherited": is_inherited,
                "enacted_2019_name": enacted_name,
            }
        )

    df = pd.DataFrame(rows)

    # Separate inherited vs reconstructed
    reconstructed = df[~df["is_2019_inherited"]]
    inherited = df[df["is_2019_inherited"]]

    n_total = len(df)
    n_inh = len(inherited)
    n_recon = len(reconstructed)

    mean_all = df["iou_vs_official_pct"].mean()
    mean_recon = reconstructed["iou_vs_official_pct"].mean() if n_recon > 0 else np.nan
    min_recon = reconstructed["iou_vs_official_pct"].min() if n_recon > 0 else np.nan
    worst_ed = (
        reconstructed.loc[reconstructed["iou_vs_official_pct"].idxmin(), "dpg_name"]
        if n_recon > 0
        else "—"
    )

    under90 = (reconstructed["iou_vs_official_pct"] < 90).sum()
    under95 = (reconstructed["iou_vs_official_pct"] < 95).sum()
    under99 = (reconstructed["iou_vs_official_pct"] < 99).sum()

    print(f"  Total EDs:             {n_total}")
    print(
        f"  2019-inherited (excl): {n_inh}  (IoU >= {INHERITED_THRESHOLD}% vs enacted)"
    )
    print(f"  Reconstructed (test):  {n_recon}")
    print()
    print(f"  Mean IoU (all):        {mean_all:.2f}%")
    print(f"  Mean IoU (recon only): {mean_recon:.2f}%")
    print(f"  Min  IoU (recon):      {min_recon:.2f}%  ({worst_ed})")
    print()
    print(f"  Reconstructed EDs below 99%: {under99}")
    print(f"  Reconstructed EDs below 95%: {under95}")
    print(f"  Reconstructed EDs below 90%: {under90}")

    if under95 > 0:
        print("\n  EDs below 95% IoU:")
        cols = ["dpg_name", "official_name", "iou_vs_official_pct"]
        sub = reconstructed[reconstructed["iou_vs_official_pct"] < 95][
            cols
        ].sort_values("iou_vs_official_pct")
        print(sub.to_string(index=False))

    return df, {
        "map": label,
        "n_total": n_total,
        "n_inherited": n_inh,
        "n_reconstructed": n_recon,
        "mean_iou_all": round(mean_all, 2),
        "mean_iou_reconstructed": (
            round(mean_recon, 2) if not np.isnan(mean_recon) else None
        ),
        "min_iou_reconstructed": (
            round(min_recon, 2) if not np.isnan(min_recon) else None
        ),
        "worst_ed": worst_ed,
        "n_below_99pct": int(under99),
        "n_below_95pct": int(under95),
        "n_below_90pct": int(under90),
    }


def write_summary(summaries, out_path):
    lines = ["# DPG Accuracy — Summary", ""]
    lines.append(
        f"*Metric: Jaccard IoU (intersection / union × 100). "
        f"2019-inherited EDs excluded from reconstructed aggregate.*"
    )
    lines.append("")
    for s in summaries:
        lines.append(f"## {s['map'].title()}")
        lines.append(
            f"- EDs total: {s['n_total']}  |  2019-inherited (excluded): {s['n_inherited']}  |  Reconstructed: {s['n_reconstructed']}"
        )
        lines.append(f"- **Mean IoU (reconstructed): {s['mean_iou_reconstructed']}%**")
        lines.append(f"- Min IoU: {s['min_iou_reconstructed']}%  ({s['worst_ed']})")
        lines.append(
            f"- Below 99%: {s['n_below_99pct']}  |  Below 95%: {s['n_below_95pct']}  |  Below 90%: {s['n_below_90pct']}"
        )
        lines.append("")
    out_path.write_text("\n".join(lines))
    print(f"\nSummary -> {out_path}")


def main():
    # Load 2019 enacted shapefile for inheritance detection
    ed_2019_path = ED_2019
    enacted_2019 = None
    for ext in ["", "/EDS_ENACTED_BILL33_15DEC2017.shp"]:
        candidate = Path(str(ed_2019_path) + ext)
        if candidate.exists():
            enacted_2019 = gpd.read_file(candidate).to_crs("EPSG:3400")
            print(f"Loaded 2019 enacted: {candidate}  ({len(enacted_2019)} EDs)")
            break
    if enacted_2019 is None:
        print(
            "WARNING: 2019 enacted shapefile not found — inheritance detection disabled"
        )

    all_rows = []
    summaries = []

    df_maj, s_maj = run_map("majority", DPG_MAJ, OFF_MAJ, enacted_2019)
    all_rows.append(df_maj)
    summaries.append(s_maj)

    df_min, s_min = run_map("minority", DPG_MIN, OFF_MIN, enacted_2019)
    all_rows.append(df_min)
    summaries.append(s_min)

    combined = pd.concat(all_rows, ignore_index=True)
    combined.to_csv(OUT_CSV, index=False)
    print(f"\nPer-ED detail -> {OUT_CSV}")

    write_summary(summaries, OUT_MD)


if __name__ == "__main__":
    main()
