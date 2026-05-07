"""
Phase 4C preparation pipeline.

Produces:
  - data/va_polygons_with_2023_votes.gpkg
  - data/hybrid_adjacent_vas.csv
  - analysis/reports/va_spatial_integrity_report.md

Input:
  - data/alberta_2023_vas/                      (VA polygons, EPSG:3400)
  - data/alberta_2019_eds/EDS_ENACTED...shp     (2019 EDs, EPSG:3401)
  - analysis/polls_2023_unified.csv             (poll-level votes, EPSG:4326 lat/lon)
  - data/majority_hybrid_crosswalk.csv
  - data/minority_hybrid_crosswalk.csv
"""

from __future__ import annotations

import io
import os
import sys
import math
from pathlib import Path

import geopandas as gpd
import pandas as pd

# Force UTF-8 output on Windows
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent.parent
DATA = BASE / "data"
ANALYSIS = BASE / "analysis"


# MED-03: guard the top-level pipeline so importing this module for a
# constant or helper does not trigger full execution. The previous
# version ran the entire pipeline on `import`. We early-return before
# any pipeline work when the module is imported rather than executed.
if __name__ != "__main__":
    raise ImportError(
        "assignment_prep.py is a script, not a library module. "
        "Run it directly via: python analysis/scripts/assignment_prep.py. "
        "If you need a helper from this file, extract it to its own "
        "module first."
    )

# ------------------------------------------------------------------
# Load inputs
# ------------------------------------------------------------------
print("[1/5] Loading inputs...")
vas = gpd.read_file(DATA / "shapefiles" / "reference" / "alberta_2023_vas")
eds19 = gpd.read_file(
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)
polls = pd.read_csv(ANALYSIS / "polls_2023_unified.csv", encoding="latin-1")
maj_cw = pd.read_csv(DATA / "majority_hybrid_crosswalk.csv")
mino_cw = pd.read_csv(DATA / "minority_hybrid_crosswalk.csv")

print(f"  VAs: {len(vas)}  |  2019 EDs: {len(eds19)}  |  polls: {len(polls)}")

# Normalize VA keys. VA_NUMBER is zero-padded string like '024'.
vas["VA_NUMBER"] = vas["VA_NUMBER"].astype(str).str.strip().str.zfill(3)

# ------------------------------------------------------------------
# Task 1: Attach Election Day NDP/UCP/Other totals to each VA polygon.
#
# Strategy: votes are recorded at the (ed_2019, sheet_num, poll_letter)
# level with a comma-separated 'voting_areas' list. Distribute evenly
# across the listed VAs (equal-weight split) - this is the standard
# polling-place-to-VA attribution method when the poll serves multiple
# VAs. Sum per (ed_2019, VA) across all Election Day polls that list it.
# ------------------------------------------------------------------
print("[2/5] Attributing poll votes to VA polygons...")

eday = polls[polls["ballot_type"] == "Election Day"].copy()
eday = eday[eday["voting_areas"].notna()].copy()

records = []
for _, row in eday.iterrows():
    va_list = [
        v.strip().zfill(3) for v in str(row["voting_areas"]).split(",") if v.strip()
    ]
    if not va_list:
        continue
    n = len(va_list)
    ndp = (row["ndp_votes"] or 0) / n
    ucp = (row["ucp_votes"] or 0) / n
    oth = (row["other_votes"] or 0) / n
    for va in va_list:
        records.append((row["ed_2019"], va, ndp, ucp, oth))

attr = pd.DataFrame(records, columns=["ed_2019", "VA_NUMBER", "ndp", "ucp", "other"])
va_totals = attr.groupby(["ed_2019", "VA_NUMBER"], as_index=False).agg(
    va_ndp=("ndp", "sum"),
    va_ucp=("ucp", "sum"),
    va_other=("other", "sum"),
)
print(f"  Distributed votes across {len(va_totals)} (ED, VA) pairs")

# Merge onto polygon frame
vas_out = vas.merge(
    va_totals,
    left_on=["ED_NAME", "VA_NUMBER"],
    right_on=["ed_2019", "VA_NUMBER"],
    how="left",
)
vas_out["va_ndp"] = vas_out["va_ndp"].fillna(0.0)
vas_out["va_ucp"] = vas_out["va_ucp"].fillna(0.0)
vas_out["va_other"] = vas_out["va_other"].fillna(0.0)
vas_out["parent_ed_2019"] = vas_out["ED_NAME"]

unmatched = vas_out[vas_out["ed_2019"].isna()]
print(f"  VAs with no matching poll record: {len(unmatched)} / {len(vas_out)}")

# Drop merge artefact
vas_out = vas_out.drop(columns=["ed_2019"])

gpkg_path = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
vas_out.to_file(gpkg_path, driver="GPKG", layer="va_2023_votes")
print(f"  Wrote {gpkg_path}")

# ------------------------------------------------------------------
# Task 2: 2019 ED spatial containment check (VA centroid -> 2019 ED).
# ------------------------------------------------------------------
print("[3/5] Spatial integrity check (VA centroid in 2019 ED)...")

# Reproject 2019 EDs to VA CRS (3400) for consistency.
eds19_proj = eds19.to_crs(vas.crs)
va_centroids = vas_out[["VA_NUMBER", "ED_NAME", "parent_ed_2019", "geometry"]].copy()
va_centroids["centroid"] = va_centroids.geometry.centroid
va_centroids = va_centroids.set_geometry("centroid", crs=vas.crs)

joined = gpd.sjoin(
    va_centroids[["VA_NUMBER", "ED_NAME", "parent_ed_2019", "centroid"]].set_geometry(
        "centroid", crs=vas.crs
    ),
    eds19_proj[["EDName2017", "geometry"]],
    how="left",
    predicate="within",
)
# Handle rare duplicates from overlapping boundaries
joined = joined.drop_duplicates(subset=["VA_NUMBER", "ED_NAME"])

total = len(joined)
matches = (joined["EDName2017"] == joined["parent_ed_2019"]).sum()
match_rate = matches / total if total else 0.0
mismatches = joined[joined["EDName2017"] != joined["parent_ed_2019"]][
    ["VA_NUMBER", "parent_ed_2019", "EDName2017"]
]
print(f"  match rate: {match_rate:.4f}  ({matches}/{total})")

# ------------------------------------------------------------------
# Task 4: Vote-conservation checksum (Election Day two-party totals).
# ------------------------------------------------------------------
print("[4/5] Vote-conservation checksum...")

eday_ndp_source = eday["ndp_votes"].sum()
eday_ucp_source = eday["ucp_votes"].sum()
eday_other_source = eday["other_votes"].sum()

va_ndp_agg = vas_out["va_ndp"].sum()
va_ucp_agg = vas_out["va_ucp"].sum()
va_other_agg = vas_out["va_other"].sum()


def pct_diff(a, b):
    return abs(a - b) / b * 100 if b else float("nan")


ndp_diff = pct_diff(va_ndp_agg, eday_ndp_source)
ucp_diff = pct_diff(va_ucp_agg, eday_ucp_source)
other_diff = pct_diff(va_other_agg, eday_other_source)

print(f"  NDP diff: {ndp_diff:.4f}%")
print(f"  UCP diff: {ucp_diff:.4f}%")
print(f"  Other diff: {other_diff:.4f}%")

# ------------------------------------------------------------------
# Task 3: Hybrid-adjacent VA list.
# Logic: a 2019-ED's VAs are "hybrid-adjacent" if that 2019 ED's boundary
# is likely to be split/absorbed by a hybrid 2026 ED. We approximate this
# with the crosswalk: for each 2019 ED, if its crosswalk entry maps to a
# hybrid 2026 ED (name change, merge, or split), all of its VAs are
# candidates for Vision assignment.
#
# Majority hybrids: rows in maj_cw where current_2019 != proposed_2026.
# Minority hybrids: rows in mino_cw where is_hybrid == 'yes'.
#   (Rows marked 'new' have no current_2019 -> those 2026 EDs are built
#   from slices of multiple 2019 EDs. We capture candidates by looking
#   for any 2019 ED whose proposed_2026 prefix appears in the 'new' name
#   - approximate but adequate for scoping.)
# ------------------------------------------------------------------
print("[5/5] Hybrid-adjacent VAs...")

# Majority hybrids = 2019 EDs whose name changes in crosswalk
maj_hybrids = maj_cw[maj_cw["current_2019"] != maj_cw["proposed_2026"]]
maj_hybrid_map = dict(zip(maj_hybrids["current_2019"], maj_hybrids["proposed_2026"]))
print(f"  Majority hybrid 2019 EDs: {len(maj_hybrid_map)}")

# Minority hybrids
mino_hybrids = mino_cw[mino_cw["is_hybrid"] == "yes"].copy()
# For rows where current_2019 is a real ED, attach directly.
mino_hybrid_direct = mino_hybrids[mino_hybrids["current_2019"] != "(NEW)"]
mino_hybrid_map = dict(
    zip(mino_hybrid_direct["current_2019"], mino_hybrid_direct["proposed_2026"])
)
print(f"  Minority hybrid 2019 EDs (direct): {len(mino_hybrid_map)}")

# For (NEW) minority EDs - find candidate 2019 EDs by *distinctive* token
# overlap. Tokens appearing in >= 5 different 2019 EDs (e.g. 'Calgary',
# 'Edmonton') are treated as generic city prefixes and ignored.
mino_new = mino_hybrids[mino_hybrids["current_2019"] == "(NEW)"][
    "proposed_2026"
].tolist()
all_2019_eds = set(vas_out["ED_NAME"].unique())

STOP_TOKENS = {"North", "South", "East", "West", "Central", "Centre", "City"}

# Frequency of each token across 2019 ED names
from collections import Counter

token_freq: Counter = Counter()
for ed in all_2019_eds:
    for t in ed.replace("-", " ").replace(".", "").split():
        token_freq[t] += 1
generic_tokens = {t for t, c in token_freq.items() if c >= 5} | STOP_TOKENS

new_candidates: dict[str, list[str]] = {}  # 2019 ED -> list of new 2026 names
for new_name in mino_new:
    tokens = {
        t.strip()
        for t in new_name.replace("-", " ").replace(".", "").split()
        if t.strip() and t not in generic_tokens
    }
    if not tokens:
        continue
    for ed in all_2019_eds:
        ed_tokens = {
            t.strip()
            for t in ed.replace("-", " ").replace(".", "").split()
            if t.strip()
        }
        # require a distinctive (non-generic) overlap
        if tokens & ed_tokens:
            new_candidates.setdefault(ed, []).append(new_name)

# Build hybrid_adjacent_vas rows
rows = []
for _, v in vas_out.iterrows():
    ed = v["ED_NAME"]
    maj_cand = maj_hybrid_map.get(ed)
    mino_cand = mino_hybrid_map.get(ed)
    if not mino_cand and ed in new_candidates:
        mino_cand = ";".join(new_candidates[ed])
    if maj_cand or mino_cand:
        rows.append(
            {
                "va_id": f"{ed}|{v['VA_NUMBER']}",
                "parent_ed_2019": ed,
                "va_number": v["VA_NUMBER"],
                "majority_hybrid_candidate": maj_cand or "",
                "minority_hybrid_candidate": mino_cand or "",
            }
        )

hybrid_adj = pd.DataFrame(rows)
hybrid_adj_path = DATA / "hybrid_adjacent_vas.csv"
hybrid_adj.to_csv(hybrid_adj_path, index=False, encoding="utf-8")
print(f"  Hybrid-adjacent VAs: {len(hybrid_adj)}")
print(f"  Wrote {hybrid_adj_path}")

# ------------------------------------------------------------------
# Write integrity report
# ------------------------------------------------------------------
print("Writing integrity report...")

report_path = ANALYSIS / "va_spatial_integrity_report.md"
n_mismatch = len(mismatches)
s3b_pass = "YES" if match_rate >= 0.95 else "NO"
s3c_pass = "YES" if all(d <= 0.1 for d in [ndp_diff, ucp_diff, other_diff]) else "NO"

with open(report_path, "w", encoding="utf-8") as f:
    f.write("# VA Spatial Integrity Report (Phase 4C prep)\n\n")
    f.write("Generated by `analysis/scripts/assignment_prep.py`.\n\n")

    f.write("## Gate S3b - VA centroid-in-2019-ED containment\n\n")
    f.write(f"- Total VAs tested: {total}\n")
    f.write(f"- Centroid-in-declared-ED matches: {matches}\n")
    f.write(f"- Match rate: **{match_rate:.4f}**\n")
    f.write(f"- Mismatches: {n_mismatch}\n")
    f.write(f"- 95% threshold achievable: **{s3b_pass}**\n\n")

    if n_mismatch > 0:
        f.write("### Mismatch list (VA | declared ED | spatial-containing ED)\n\n")
        f.write("| VA | declared (parent_ed_2019) | spatial (2019 shapefile) |\n")
        f.write("|---|---|---|\n")
        for _, r in mismatches.head(200).iterrows():
            f.write(
                f"| {r['VA_NUMBER']} | {r['parent_ed_2019']} | {r['EDName2017']} |\n"
            )
        if n_mismatch > 200:
            f.write(f"\n_{n_mismatch - 200} additional mismatches omitted._\n")
        f.write("\n")

    f.write(
        "## Gate S3c - Vote-conservation checksum (Election Day, 2-party + other)\n\n"
    )
    f.write("| party | poll CSV (EDay) | VA aggregate | diff % |\n")
    f.write("|---|---|---|---|\n")
    f.write(f"| NDP | {eday_ndp_source:,.0f} | {va_ndp_agg:,.2f} | {ndp_diff:.4f}% |\n")
    f.write(f"| UCP | {eday_ucp_source:,.0f} | {va_ucp_agg:,.2f} | {ucp_diff:.4f}% |\n")
    f.write(
        f"| Other | {eday_other_source:,.0f} | {va_other_agg:,.2f} | {other_diff:.4f}% |\n"
    )
    f.write(f"\n0.1% threshold met for all three parties: **{s3c_pass}**\n\n")
    f.write(
        "Attribution method: equal-weight split of each Election Day poll's "
        "votes across all VAs listed in its `voting_areas` field. Advance, "
        "Mobile, and Special Ballot rows excluded.\n\n"
    )

    f.write("## Task 3 - hybrid-adjacent VA counts\n\n")
    f.write(f"- Total VAs flagged for Vision review: {len(hybrid_adj)}\n")
    f.write(
        f"- Majority-hybrid-only: "
        f"{((hybrid_adj['majority_hybrid_candidate'] != '') & (hybrid_adj['minority_hybrid_candidate'] == '')).sum()}\n"
    )
    f.write(
        f"- Minority-hybrid-only: "
        f"{((hybrid_adj['majority_hybrid_candidate'] == '') & (hybrid_adj['minority_hybrid_candidate'] != '')).sum()}\n"
    )
    f.write(
        f"- Both (majority AND minority candidate): "
        f"{((hybrid_adj['majority_hybrid_candidate'] != '') & (hybrid_adj['minority_hybrid_candidate'] != '')).sum()}\n\n"
    )
    f.write("By parent 2019 ED:\n\n")
    counts = hybrid_adj.groupby("parent_ed_2019").size().sort_values(ascending=False)
    f.write("| parent_ed_2019 | VA count |\n|---|---|\n")
    for ed, c in counts.items():
        f.write(f"| {ed} | {c} |\n")
    f.write("\n")

print(f"  Wrote {report_path}")
print("DONE.")
