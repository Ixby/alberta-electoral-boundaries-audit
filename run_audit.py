"""
v0_9 topological shapefiles audit — 10 checks
"""
import json
import warnings
warnings.filterwarnings("ignore")

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.validation import explain_validity

BASE = r"C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit"

MAJ_PATH  = BASE + r"\data\shapefiles\derived\v0_9_topological_majority_2026_eds.gpkg"
MIN_PATH  = BASE + r"\data\shapefiles\derived\v0_9_topological_minority_2026_eds.gpkg"
VA_PATH   = BASE + r"\data\shapefiles\derived\va_polygons_with_2023_votes.gpkg"
REF_PATH  = BASE + r"\data\shapefiles\reference\alberta_2019_eds\EDS_ENACTED_BILL33_15DEC2017.shp"
SCORES_PATH = BASE + r"\data\outputs\final_real_map_scores.json"

with open(SCORES_PATH) as f:
    scores = json.load(f)

print("Loading files ...")
maj = gpd.read_file(MAJ_PATH)
minn = gpd.read_file(MIN_PATH)
va  = gpd.read_file(VA_PATH)
ref = gpd.read_file(REF_PATH)
print(f"  majority: {len(maj)} rows | minority: {len(minn)} rows | va: {len(va)} rows | ref2019: {len(ref)} rows")
print()

results = []

# ── CHECK 1 — District count ─────────────────────────────────────────────────
expected_n = 89
maj_n = len(maj)
min_n = len(minn)
if maj_n == expected_n and min_n == expected_n:
    results.append(("1. District count", "PASS", f"majority={maj_n}, minority={min_n}"))
else:
    results.append(("1. District count", "FAIL",
                    f"majority={maj_n} (expected {expected_n}), minority={min_n} (expected {expected_n})"))

# ── CHECK 2 — Geometry validity ──────────────────────────────────────────────
issues = {}
for label, gdf in [("majority", maj), ("minority", minn)]:
    null_geom   = gdf.geometry.isna().sum()
    empty_geom  = gdf.geometry.is_empty.sum()
    invalid_geom = (~gdf.geometry.is_valid).sum()
    if null_geom or empty_geom or invalid_geom:
        bad = []
        if null_geom:   bad.append(f"{null_geom} null")
        if empty_geom:  bad.append(f"{empty_geom} empty")
        if invalid_geom:
            msgs = gdf.loc[~gdf.geometry.is_valid, "geometry"].apply(explain_validity).tolist()
            bad.append(f"{invalid_geom} invalid ({'; '.join(set(msgs[:3]))})")
        issues[label] = ", ".join(bad)

if not issues:
    results.append(("2. Geometry validity", "PASS", "no null/empty/invalid in either map"))
else:
    results.append(("2. Geometry validity", "FAIL", str(issues)))

# ── CHECK 3 — Duplicate names ────────────────────────────────────────────────
dups = {}
for label, gdf in [("majority", maj), ("minority", minn)]:
    col = "name_2026" if "name_2026" in gdf.columns else gdf.columns[0]
    vc = gdf[col].value_counts()
    d = vc[vc > 1]
    if len(d):
        dups[label] = d.to_dict()

if not dups:
    results.append(("3. Duplicate names", "PASS", "all name_2026 values unique in both maps"))
else:
    results.append(("3. Duplicate names", "FAIL", str(dups)))

# ── CHECK 4 — Name completeness ──────────────────────────────────────────────
blanks = {}
for label, gdf in [("majority", maj), ("minority", minn)]:
    col = "name_2026" if "name_2026" in gdf.columns else None
    if col:
        n_null  = gdf[col].isna().sum()
        n_blank = (gdf[col].str.strip() == "").sum() if gdf[col].dtype == object else 0
        if n_null or n_blank:
            blanks[label] = f"{n_null} null, {n_blank} blank"

if not blanks:
    results.append(("4. Name completeness", "PASS", "no null/blank name_2026 in either map"))
else:
    results.append(("4. Name completeness", "FAIL", str(blanks)))

# ── CHECK 5 — Topology: internal overlaps ────────────────────────────────────
OVERLAP_THRESH = 1000  # m²
overlap_results = {}
for label, gdf in [("majority", maj), ("minority", minn)]:
    gdf_proj = gdf.to_crs(epsg=3400)
    pairs_found = []
    geoms = list(gdf_proj.geometry)
    names_col = "name_2026" if "name_2026" in gdf_proj.columns else gdf_proj.columns[0]
    names = list(gdf_proj[names_col])
    for i in range(len(geoms)):
        for j in range(i+1, len(geoms)):
            if geoms[i].intersects(geoms[j]):
                ov = geoms[i].intersection(geoms[j])
                if ov.area > OVERLAP_THRESH:
                    pairs_found.append((names[i], names[j], round(ov.area, 1)))
    overlap_results[label] = pairs_found

all_clean = all(len(v) == 0 for v in overlap_results.values())
if all_clean:
    results.append(("5. Topology: internal overlaps", "PASS",
                    f"no overlapping pairs > {OVERLAP_THRESH} m² in either map"))
else:
    detail = {k: f"{len(v)} overlapping pairs" for k, v in overlap_results.items() if v}
    worst  = {k: v[:5] for k, v in overlap_results.items() if v}
    results.append(("5. Topology: internal overlaps", "FAIL",
                    f"overlapping pairs: {detail} | sample: {worst}"))

# ── CHECK 6 — Topology: coverage gaps vs VA union ────────────────────────────
va_proj  = va.to_crs(epsg=3400)
va_union = va_proj.geometry.union_all()

gap_results = {}
for label, gdf in [("majority", maj), ("minority", minn)]:
    gdf_proj  = gdf.to_crs(epsg=3400)
    ed_union  = gdf_proj.geometry.union_all()
    uncovered = va_union.difference(ed_union)
    uncov_area = uncovered.area
    va_area    = va_union.area
    frac_uncov = uncov_area / va_area if va_area > 0 else 0
    gap_results[label] = (frac_uncov, uncov_area, va_area)

threshold = 0.0001  # 0.01%
if all(v[0] < threshold for v in gap_results.values()):
    detail = {k: f"{v[0]*100:.4f}% uncovered ({v[1]/1e6:.3f} km²)" for k, v in gap_results.items()}
    results.append(("6. Topology: coverage gaps", "PASS", str(detail)))
else:
    detail = {k: f"{v[0]*100:.4f}% uncovered ({v[1]/1e6:.3f} km²)" for k, v in gap_results.items()}
    failed = {k: v for k, v in detail.items() if gap_results[k][0] >= threshold}
    results.append(("6. Topology: coverage gaps", "FAIL", str(detail)))

# ── CHECK 7 — VA attribution completeness ────────────────────────────────────
va_attr = {}
for label, gdf in [("majority", maj), ("minority", minn)]:
    gdf_reproj = gdf.to_crs(va.crs)
    joined = gpd.sjoin(va, gdf_reproj[["geometry"]], how="left", predicate="intersects")
    # count matches per VA (by original index)
    match_counts = joined.groupby(joined.index).size()
    n_zero  = (match_counts == 0).sum() + (va.index.isin(match_counts[match_counts > 0].index) == False).sum()
    # simpler: count VAs with index not appearing at all in joined
    va_in_joined = set(joined.index.unique())
    n_unmatched = len(va) - len(va_in_joined)
    n_multi  = (match_counts > 1).sum()
    n_exact1 = (match_counts == 1).sum()
    frac_exact1 = n_exact1 / len(va)
    va_attr[label] = {"n_va": len(va), "exact_1": n_exact1, "frac": round(frac_exact1, 6),
                      "multi": n_multi, "unmatched": n_unmatched}

all_full = all(v["frac"] == 1.0 for v in va_attr.values())
if all_full:
    results.append(("7. VA attribution completeness", "PASS",
                    f"all {list(va_attr.values())[0]['n_va']} VAs get exactly one match in both maps"))
else:
    results.append(("7. VA attribution completeness", "FAIL", str(va_attr)))

# ── CHECK 8 — Vote totals consistency ────────────────────────────────────────
# Sum from VA file
ucp_col   = next((c for c in va.columns if "ucp" in c.lower()), None)
ndp_col   = next((c for c in va.columns if "ndp" in c.lower()), None)
other_col = next((c for c in va.columns if "other" in c.lower()), None)

if ucp_col and ndp_col and other_col:
    va_total = (va[ucp_col].fillna(0) + va[ndp_col].fillna(0) + va[other_col].fillna(0)).sum()
    # From scores JSON — both v0_9 maps should have the same covered_votes
    score_votes = scores["v0_9_majority"]["covered_votes"]
    diff = abs(va_total - score_votes)
    if diff < 1.0:
        results.append(("8. Vote totals consistency", "PASS",
                        f"VA sum={va_total:,.0f}, scores.json={score_votes:,.0f}, diff={diff:.1f}"))
    else:
        results.append(("8. Vote totals consistency", "FAIL",
                        f"VA sum={va_total:,.0f}, scores.json={score_votes:,.0f}, diff={diff:,.0f}"))
else:
    # try to find columns
    va_cols = list(va.columns)
    results.append(("8. Vote totals consistency", "SKIP",
                    f"Could not find va_ucp/va_ndp/va_other columns. Available: {va_cols}"))

# ── CHECK 9 — Column schema ───────────────────────────────────────────────────
maj_cols = sorted(maj.columns.tolist())
min_cols = sorted(minn.columns.tolist())
if maj_cols == min_cols:
    results.append(("9. Column schema", "PASS",
                    f"identical columns: {maj_cols}"))
else:
    only_maj = set(maj_cols) - set(min_cols)
    only_min = set(min_cols) - set(maj_cols)
    results.append(("9. Column schema", "FAIL",
                    f"only in majority={only_maj}, only in minority={only_min}"))

# ── CHECK 10 — CRS ───────────────────────────────────────────────────────────
crses = {
    "majority_2026": maj.crs,
    "minority_2026": minn.crs,
    "va_polygons":   va.crs,
    "ref_2019":      ref.crs,
}
crs_strs = {k: (str(v) if v else "None") for k, v in crses.items()}
unique_crs = set(str(v) for v in crses.values())
# Check authority codes specifically
auth_codes = {}
for k, v in crses.items():
    if v:
        auth_codes[k] = v.to_authority() if hasattr(v, "to_authority") else str(v)
    else:
        auth_codes[k] = None

results.append(("10. CRS", "INFO",
                f"majority={auth_codes['majority_2026']}, minority={auth_codes['minority_2026']}, "
                f"va={auth_codes['va_polygons']}, ref2019={auth_codes['ref_2019']}"))

# ── PRINT REPORT ─────────────────────────────────────────────────────────────
print("=" * 90)
print("v0_9 TOPOLOGICAL SHAPEFILE AUDIT REPORT")
print("=" * 90)
for check, status, detail in results:
    marker = "✓" if status == "PASS" else ("✗" if status == "FAIL" else "i")
    print(f"\n[{status:4s}] {check}")
    print(f"       {detail}")
print()
print("=" * 90)
print("VA columns:", sorted(va.columns.tolist()))
print("Majority columns:", sorted(maj.columns.tolist()))
print("Minority columns:", sorted(minn.columns.tolist()))
print("Ref 2019 columns:", sorted(ref.columns.tolist()))
