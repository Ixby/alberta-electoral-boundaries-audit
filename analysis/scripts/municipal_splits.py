"""
v0_1_municipal_splits.py
=========================
Counts how many times each Alberta municipality is split across multiple
electoral districts in the 2019 enacted, majority 2026, and minority 2026 maps.

A municipality is "split" if its area overlaps with ≥2 EDs.
Significance threshold: cities (CY), towns (T), and specialized municipalities
(SM) with ≥500 VA votes (proxy for ~5,000+ residents).

Reports:
  - Per-municipality split count across all three maps
  - Total splits per map (fragmentation score)
  - Change from 2019 baseline

Outputs:
  analysis/reports/municipal_splits.md
  data/municipal_splits.json

Backward:
  data/shapefiles/reference/alberta_2021_csds.gpkg
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
  data/shapefiles/derived/v0_7_canonical_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_7_canonical_minority_2026_eds.gpkg
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent / "utils"))
    import data_loader

import json, sys, time, warnings
import numpy as np
import pandas as pd
import geopandas as gpd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
RPTS = ROOT / "analysis" / "reports"
RPTS.mkdir(parents=True, exist_ok=True)

CSD_PATH = DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
VA_PATH = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
MAJ_V7 = DATA / "shapefiles" / "derived" / "v0_7_canonical_majority_2026_eds.gpkg"
MIN_V7 = DATA / "shapefiles" / "derived" / "v0_7_canonical_minority_2026_eds.gpkg"

OUT_JSON = DATA / "municipal_splits.json"
OUT_MD = RPTS / "municipal_splits.md"

# CSD types to include: Cities, Towns, Specialized Municipalities, Villages
INCLUDE_TYPES = {"CY", "T", "SM", "SV", "IM"}
MIN_VOTES = 300  # ~3,000 residents; excludes tiny villages


def ed_name_for_2019(va: gpd.GeoDataFrame) -> pd.Series:
    """Return a Series mapping VA index → 2019 ED name."""
    return va["parent_ed_2019"]


def count_splits(
    csds: gpd.GeoDataFrame,
    eds: gpd.GeoDataFrame,
    label: str,
    min_overlap_m2: float = 50000.0,
) -> pd.DataFrame:
    """
    For each CSD, count how many EDs it intersects with non-trivially.
    min_overlap_m2: minimum intersection area (m²) to count as a real split (default 5 ha).
    """
    csds_proj = csds.to_crs(eds.crs)

    rows = []
    for _, csd in csds_proj.iterrows():
        csd_geom = csd.geometry
        if csd_geom is None or csd_geom.is_empty:
            continue

        ed_hits = []
        for _, ed in eds.iterrows():
            if ed.geometry is None or ed.geometry.is_empty:
                continue
            try:
                inter = csd_geom.intersection(ed.geometry)
            except Exception:
                continue
            if inter.is_empty:
                continue
            area = inter.area
            if area >= min_overlap_m2:
                ed_hits.append(ed["name_2026"])

        rows.append(
            {
                "csd_name": csd["CSDNAME"],
                "csd_type": csd["CSDTYPE"],
                "n_eds": len(ed_hits),
                "eds": "; ".join(sorted(ed_hits)),
            }
        )

    return pd.DataFrame(rows)


def count_splits_2019(
    csds: gpd.GeoDataFrame, va: gpd.GeoDataFrame, min_overlap_m2: float = 50000.0
) -> pd.DataFrame:
    """
    For 2019, use VA spatial join to determine which EDs each CSD overlaps.
    """
    csds_proj = csds.to_crs(va.crs)
    va_proj = va.copy()

    # Spatial join: which VA centroids fall in each CSD
    va_c = va_proj.copy()
    va_c["geometry"] = va_proj.geometry.centroid
    joined = gpd.sjoin(
        va_c[["va_ucp", "va_ndp", "parent_ed_2019", "geometry"]],
        csds_proj[["CSDNAME", "CSDTYPE", "geometry"]],
        how="right",
        predicate="within",
    )

    rows = []
    for _, group in joined.groupby(["CSDNAME", "CSDTYPE"]):
        csd_name, csd_type = _[0], _[1]
        eds_in_csd = group["parent_ed_2019"].dropna().unique().tolist()
        rows.append(
            {
                "csd_name": csd_name,
                "csd_type": csd_type,
                "n_eds": len(eds_in_csd),
                "eds": "; ".join(sorted(str(e) for e in eds_in_csd)),
            }
        )
    return pd.DataFrame(rows)


def va_votes_per_csd(csds: gpd.GeoDataFrame, va: gpd.GeoDataFrame) -> dict:
    """Map CSDNAME → total votes (UCP+NDP) as population proxy."""
    csds_proj = csds.to_crs(va.crs)
    va_c = va.copy()
    va_c["geometry"] = va.geometry.centroid
    joined = gpd.sjoin(
        va_c[["va_ucp", "va_ndp", "geometry"]],
        csds_proj[["CSDNAME", "geometry"]],
        how="left",
        predicate="within",
    )
    agg = joined.groupby("CSDNAME").agg(
        total_votes=pd.NamedAgg(
            column="va_ucp",
            aggfunc=lambda x: x.sum() + joined.loc[x.index, "va_ndp"].sum(),
        )
    )
    return agg["total_votes"].to_dict()


def main():
    t0 = time.time()
    print("[municipal splits] Loading data...")
    csds = gpd.read_file(CSD_PATH)
    va = gpd.read_file(VA_PATH)
    maj = gpd.read_file(MAJ_V7)
    mn = gpd.read_file(MIN_V7)

    # Compute VA votes per CSD (population proxy)
    print("  Computing VA votes per CSD...")
    votes_map = va_votes_per_csd(csds, va)
    csds["va_votes"] = csds["CSDNAME"].map(votes_map).fillna(0)

    # Filter to significant municipalities
    sig_csds = csds[
        (csds["CSDTYPE"].isin(INCLUDE_TYPES)) & (csds["va_votes"] >= MIN_VOTES)
    ].copy()
    print(
        f"  Significant municipalities: {len(sig_csds)} "
        f"(types {INCLUDE_TYPES}, ≥{MIN_VOTES} VA votes)"
    )

    print("\nCounting splits — 2019...")
    df_2019 = count_splits_2019(sig_csds, va)
    df_2019 = df_2019.rename(columns={"n_eds": "n_eds_2019", "eds": "eds_2019"})

    print("Counting splits — majority 2026...")
    df_maj = count_splits(sig_csds, maj, "majority")
    df_maj = df_maj.rename(columns={"n_eds": "n_eds_maj", "eds": "eds_maj"})

    print("Counting splits — minority 2026...")
    df_min = count_splits(sig_csds, mn, "minority")
    df_min = df_min.rename(columns={"n_eds": "n_eds_min", "eds": "eds_min"})

    # Merge
    df = df_2019.merge(
        df_maj[["csd_name", "n_eds_maj", "eds_maj"]], on="csd_name", how="outer"
    )
    df = df.merge(
        df_min[["csd_name", "n_eds_min", "eds_min"]], on="csd_name", how="outer"
    )
    df = df.fillna({"n_eds_2019": 0, "n_eds_maj": 0, "n_eds_min": 0})
    df["n_eds_2019"] = df["n_eds_2019"].astype(int)
    df["n_eds_maj"] = df["n_eds_maj"].astype(int)
    df["n_eds_min"] = df["n_eds_min"].astype(int)
    df["split_2019"] = df["n_eds_2019"] > 1
    df["split_maj"] = df["n_eds_maj"] > 1
    df["split_min"] = df["n_eds_min"] > 1
    df["delta_maj"] = df["n_eds_maj"] - df["n_eds_2019"]
    df["delta_min"] = df["n_eds_min"] - df["n_eds_2019"]

    # Add VA votes
    votes_df = pd.DataFrame(list(votes_map.items()), columns=["csd_name", "va_votes"])
    df = df.merge(votes_df, on="csd_name", how="left")
    df["va_votes"] = df["va_votes"].fillna(0).astype(int)
    df = df.sort_values("va_votes", ascending=False)

    print("\n--- MUNICIPAL SPLIT SUMMARY ---")
    split_2019 = df["split_2019"].sum()
    split_maj = df["split_maj"].sum()
    split_min = df["split_min"].sum()
    print(f"  2019 enacted:  {split_2019} municipalities split across ≥2 EDs")
    print(
        f"  Majority 2026: {split_maj} municipalities split "
        f"({'+'  if split_maj>=split_2019 else ''}{split_maj-split_2019:+d} vs 2019)"
    )
    print(
        f"  Minority 2026: {split_min} municipalities split "
        f"({'+'  if split_min>=split_2019 else ''}{split_min-split_2019:+d} vs 2019)"
    )

    print(
        "\n--- TOP MUNICIPALITIES BY SPLIT (showing those with any split in any map) ---"
    )
    changed = df[(df["split_2019"] | df["split_maj"] | df["split_min"])].head(30)
    print(
        changed[
            [
                "csd_name",
                "csd_type",
                "va_votes",
                "n_eds_2019",
                "n_eds_maj",
                "n_eds_min",
                "delta_maj",
                "delta_min",
            ]
        ].to_string(index=False)
    )

    # Municipalities that are MORE split in 2026 than 2019
    worse_maj = df[df["delta_maj"] > 0]
    worse_min = df[df["delta_min"] > 0]
    print(f"\nNew splits introduced by majority 2026: {len(worse_maj)}")
    for _, r in worse_maj.iterrows():
        print(
            f"  {r['csd_name']:30s} 2019={r['n_eds_2019']} → maj={r['n_eds_maj']} "
            f"(+{r['delta_maj']:.0f})"
        )
    print(f"\nNew splits introduced by minority 2026: {len(worse_min)}")
    for _, r in worse_min.iterrows():
        print(
            f"  {r['csd_name']:30s} 2019={r['n_eds_2019']} → min={r['n_eds_min']} "
            f"(+{r['delta_min']:.0f})"
        )

    # JSON output
    out = {
        "summary": {
            "2019_enacted": {"n_splits": int(split_2019)},
            "majority_2026": {
                "n_splits": int(split_maj),
                "delta_vs_2019": int(split_maj - split_2019),
            },
            "minority_2026": {
                "n_splits": int(split_min),
                "delta_vs_2019": int(split_min - split_2019),
            },
        },
        "new_splits_majority": worse_maj[
            ["csd_name", "csd_type", "va_votes", "n_eds_2019", "n_eds_maj"]
        ].to_dict("records"),
        "new_splits_minority": worse_min[
            ["csd_name", "csd_type", "va_votes", "n_eds_2019", "n_eds_min"]
        ].to_dict("records"),
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nWrote {OUT_JSON}")

    # Markdown
    md = [
        "# Municipal Splits — Alberta 2026 Electoral Maps",
        "",
        f"Significant municipalities: Cities, Towns, Specialized Municipalities "
        f"with ≥{MIN_VOTES} VA votes (~{MIN_VOTES*10:,} residents).",
        "",
        "## Summary",
        "",
        f"| Map | Municipalities split (≥2 EDs) | Change vs 2019 |",
        f"|-----|-------------------------------|----------------|",
        f"| 2019 enacted  | {split_2019} | baseline |",
        f"| Majority 2026 | {split_maj}  | {split_maj-split_2019:+d} |",
        f"| Minority 2026 | {split_min}  | {split_min-split_2019:+d} |",
        "",
        "## New Splits — Majority 2026",
        "",
    ]
    if len(worse_maj):
        md.append("| Municipality | Type | 2019 EDs | Majority EDs | +splits |")
        md.append("|---|---|---|---|---|")
        for _, r in worse_maj.iterrows():
            md.append(
                f"| {r['csd_name']} | {r['csd_type']} | "
                f"{r['n_eds_2019']:.0f} | {r['n_eds_maj']:.0f} | "
                f"+{r['delta_maj']:.0f} |"
            )
    else:
        md.append("_No new splits vs 2019._")

    md += ["", "## New Splits — Minority 2026", ""]
    if len(worse_min):
        md.append("| Municipality | Type | 2019 EDs | Minority EDs | +splits |")
        md.append("|---|---|---|---|---|")
        for _, r in worse_min.iterrows():
            md.append(
                f"| {r['csd_name']} | {r['csd_type']} | "
                f"{r['n_eds_2019']:.0f} | {r['n_eds_min']:.0f} | "
                f"+{r['delta_min']:.0f} |"
            )
    else:
        md.append("_No new splits vs 2019._")

    md.append(f"\n_Generated {time.strftime('%Y-%m-%d %H:%M')}_")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"\nDone in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
