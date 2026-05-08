"""
T4 — Headline Metric Rerun on Official Geometry

Recomputes the four vote-independent headline metrics using official shapefiles
and compares them to the DPG-derived values published in the audit.

Metrics:
  1. Population MAD  — mean absolute deviation from provincial quota
     (official PopCensus column, no geometry needed)
  2. Municipal anchoring — % of total perimeter that follows CSD boundaries
     (requires CSD shapefile + official ED polygons)
  3. Calgary NW zone excess — mean pop of NW Calgary EDs vs provincial mean
  4. Airdrie partition count — how many 2026 EDs intersect Airdrie CSD

Audit-reported DPG values (from report_academic.md §§5.1, 5.8.5):
  Population MAD:       majority 3,180  minority 4,707
  Municipal anchoring:  majority 71.0%  minority 14.5%
  Calgary NW excess:    majority +2.8%  minority +11.5%
  Airdrie partitions:   majority 2      minority 4
"""

from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

OFF_MAJ = ROOT / "data/official/majority/EBC2025_Boundaries_Apr092026.shp"
OFF_MIN = ROOT / "data/official/minority/Minority_Report_Boundaries.shp"
CSD_PATH = REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg"
OUT = ROOT / "outputs/t4_metric_delta.csv"
OUT.parent.mkdir(exist_ok=True)

# Audit-reported DPG values
DPG_VALUES = {
    "majority": {
        "pop_mad": 3180,
        "muni_anchor_pct": 71.0,
        "nw_excess_pct": 2.8,
        "airdrie_partitions": 2,
    },
    "minority": {
        "pop_mad": 4707,
        "muni_anchor_pct": 14.5,
        "nw_excess_pct": 11.5,
        "airdrie_partitions": 4,
    },
}

# Calgary NW zone EDs — the same set used in the original audit (§5.1 A2)
# These are the EDs in the northwest Calgary geographic zone
NW_CALGARY_EDS = {
    "Calgary-Bow",
    "Calgary-Beddington",
    "Calgary-Edgemont",
    "Calgary-Klein",
    "Calgary-North",
    "Calgary-North West",
    "Calgary-Nose Creek",
    "Calgary-Symons Valley",
    # minority-specific names for the same geographic zone
    "Calgary-North West-Bearspaw",
    "Calgary-Nolan Hill-Cochrane",
}


def pop_mad(gdf):
    """Mean absolute deviation from provincial quota (persons)."""
    pops = gdf["PopCensus"].astype(float)
    quota = pops.mean()
    return float((pops - quota).abs().mean()), float(quota)


def municipal_anchoring(ed_gdf, csd_gdf, buffer_m=50):
    """
    % of total ED perimeter that lies within buffer_m metres of a CSD boundary.

    Uses a buffer rather than exact intersection because official ED and CSD
    shapefiles come from different digitization sources — exact line coincidence
    cannot be assumed even when boundaries conceptually follow CSD edges.
    The DPG used VA polygon edges (which ARE aligned to CSDs), so exact
    intersection worked there but not here.
    """
    ed_proj = ed_gdf.to_crs("EPSG:3400")
    csd_proj = csd_gdf.to_crs("EPSG:3400")

    # Union of individual CSD boundaries preserves internal edges between CSDs
    csd_boundary = unary_union([g.boundary for g in csd_proj.geometry])
    csd_zone = csd_boundary.buffer(buffer_m)

    total_perim = 0.0
    anchored_len = 0.0

    for _, row in ed_proj.iterrows():
        ed_boundary = row.geometry.boundary
        total_perim += ed_boundary.length
        try:
            overlap = ed_boundary.intersection(csd_zone)
            anchored_len += overlap.length
        except Exception:
            pass

    return 100.0 * anchored_len / total_perim if total_perim > 0 else 0.0


def calgary_nw_excess(gdf, nw_names):
    """
    Mean population of NW Calgary zone EDs as % above/below provincial mean.
    Returns the signed % difference: +X means X% above mean.
    """
    pops = gdf["PopCensus"].astype(float)
    prov_mean = pops.mean()

    nw_mask = gdf["EDName2025"].isin(nw_names)
    if nw_mask.sum() == 0:
        return np.nan, 0
    nw_mean = pops[nw_mask].mean()
    excess_pct = 100.0 * (nw_mean - prov_mean) / prov_mean
    return float(excess_pct), int(nw_mask.sum())


def airdrie_count(ed_gdf, csd_gdf):
    """How many 2026 EDs intersect the City of Airdrie CSD?"""
    ed_proj = ed_gdf.to_crs("EPSG:3400")
    csd_proj = csd_gdf.to_crs("EPSG:3400")

    airdrie_candidates = csd_proj[
        csd_proj["CSDNAME"].str.contains("Airdrie", case=False, na=False)
    ]
    if airdrie_candidates.empty:
        print("  WARNING: Airdrie not found in CSD layer")
        return np.nan

    airdrie_geom = unary_union(airdrie_candidates.geometry)
    count = sum(
        1
        for _, row in ed_proj.iterrows()
        if row.geometry.intersects(airdrie_geom)
        and row.geometry.intersection(airdrie_geom).area > 1e4
    )  # >1 ha
    return count


def run_map(label, off_path, csd_gdf):
    print(f"\n=== {label} ===")
    off = gpd.read_file(off_path).to_crs("EPSG:3400")
    dpg_vals = DPG_VALUES[label]

    # 1. Population MAD
    mad, quota = pop_mad(off)
    mad_delta = mad - dpg_vals["pop_mad"]
    print(
        f"  Population MAD:  official={mad:.0f}  DPG={dpg_vals['pop_mad']}  delta={mad_delta:+.0f}"
    )

    # 2. Municipal anchoring
    print("  Computing municipal anchoring (may take ~30s)...")
    anchor = municipal_anchoring(off, csd_gdf)
    anchor_delta = anchor - dpg_vals["muni_anchor_pct"]
    print(
        f"  Muni anchoring:  official={anchor:.1f}%  DPG={dpg_vals['muni_anchor_pct']}%  delta={anchor_delta:+.1f}pp"
    )

    # 3. Calgary NW zone
    excess, n_nw = calgary_nw_excess(off, NW_CALGARY_EDS)
    excess_delta = (
        excess - dpg_vals["nw_excess_pct"] if not np.isnan(excess) else np.nan
    )
    print(
        f"  Calgary NW excess: official={excess:.1f}%  DPG={dpg_vals['nw_excess_pct']}%  delta={excess_delta:+.1f}pp  (n={n_nw} EDs)"
    )

    # 4. Airdrie count
    airdrie = airdrie_count(off, csd_gdf)
    airdrie_delta = (
        (airdrie - dpg_vals["airdrie_partitions"]) if not np.isnan(airdrie) else np.nan
    )
    print(
        f"  Airdrie EDs:     official={airdrie}  DPG={dpg_vals['airdrie_partitions']}  delta={airdrie_delta:+}"
    )

    return {
        "map": label,
        "pop_mad_official": round(mad),
        "pop_mad_dpg": dpg_vals["pop_mad"],
        "pop_mad_delta": round(mad_delta),
        "muni_anchor_official_pct": round(anchor, 2),
        "muni_anchor_dpg_pct": dpg_vals["muni_anchor_pct"],
        "muni_anchor_delta_pp": round(anchor_delta, 2),
        "nw_excess_official_pct": round(excess, 2) if not np.isnan(excess) else None,
        "nw_excess_dpg_pct": dpg_vals["nw_excess_pct"],
        "nw_excess_delta_pp": (
            round(excess_delta, 2) if not np.isnan(excess_delta) else None
        ),
        "airdrie_official": airdrie,
        "airdrie_dpg": dpg_vals["airdrie_partitions"],
        "airdrie_delta": airdrie_delta,
    }


def main():
    if not CSD_PATH.exists():
        print(f"ERROR: CSD file not found at {CSD_PATH}")
        return

    print("Loading CSD boundaries...")
    csd = gpd.read_file(CSD_PATH)
    print(f"  {len(csd)} CSDs loaded  CRS: {csd.crs}")
    if "CSDNAME" not in csd.columns:
        print(f"  CSD columns: {list(csd.columns)}")

    rows = []
    rows.append(run_map("majority", OFF_MAJ, csd))
    rows.append(run_map("minority", OFF_MIN, csd))

    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print(f"\nSaved -> {OUT}")


if __name__ == "__main__":
    main()
