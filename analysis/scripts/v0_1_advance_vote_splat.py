"""
v0_1_advance_vote_splat.py
==========================
Apportions non-Election-Day votes (Advance, Special Ballot, Mobile) from
polls_2023_unified.csv to individual Voting Areas (VAs) using Election-Day
vote shares as splat weights.

Pipeline
--------
Step 1  Read polls_2023_unified.csv; inspect ballot_type breakdown.
Step 2  Build splat weights per (ed_2019, sheet_num) group:
        - Pool all Election-Day VAs in the group to get ED-level weights.
        - Distribute each non-Election-Day poll's votes proportionally.
Step 3  Merge apportioned votes with Election-Day votes from the VA substrate,
        write data/va_polygons_with_full_2023_votes.gpkg.
Step 4  Validate conservation; print province-wide NDP-share comparison.

Outputs
-------
  data/va_polygons_with_full_2023_votes.gpkg
  analysis/v0_1_advance_vote_splat_diagnostics.csv
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd
import geopandas as gpd

warnings.filterwarnings("ignore", category=FutureWarning)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
POLLS_CSV   = os.path.join(HERE, "polls_2023_unified.csv")
VA_GPKG_IN  = os.path.join(ROOT, "data", "va_polygons_with_2023_votes.gpkg")
VA_GPKG_OUT = os.path.join(ROOT, "data", "va_polygons_with_full_2023_votes.gpkg")
DIAG_CSV    = os.path.join(HERE, "v0_1_advance_vote_splat_diagnostics.csv")


# ===========================================================================
# STEP 1 — Read and summarise the polls file
# ===========================================================================
print("=" * 70)
print("STEP 1 — Loading polls file")
print("=" * 70)

polls = pd.read_csv(POLLS_CSV, dtype={"sheet_num": str, "voting_areas": str}, encoding="cp1252")

# Coerce vote columns to numeric (in case of blanks)
for col in ("ndp_votes", "ucp_votes", "other_votes", "valid_votes"):
    polls[col] = pd.to_numeric(polls[col], errors="coerce").fillna(0).astype(int)

print(f"\nTotal rows: {len(polls):,}")
print(f"Distinct ed_2019 values: {polls['ed_2019'].nunique()}")

print("\n--- ballot_type value_counts ---")
bt_counts = polls["ballot_type"].value_counts()
print(bt_counts.to_string())

print("\n--- Total votes by ballot_type ---")
vote_by_type = (
    polls.groupby("ballot_type")[["ndp_votes", "ucp_votes", "other_votes"]]
    .sum()
    .assign(total=lambda df: df.sum(axis=1))
)
vote_by_type["two_party"] = vote_by_type["ndp_votes"] + vote_by_type["ucp_votes"]
print(vote_by_type.to_string())

total_ndp_all   = polls["ndp_votes"].sum()
total_ucp_all   = polls["ucp_votes"].sum()
total_other_all = polls["other_votes"].sum()
total_votes_all = total_ndp_all + total_ucp_all + total_other_all
print(f"\nGrand totals  NDP={total_ndp_all:,}  UCP={total_ucp_all:,}  "
      f"Other={total_other_all:,}  Total={total_votes_all:,}")

# Warning: rows where voting_areas is NaN / empty (expected for non-ED polls)
missing_va = polls["voting_areas"].isna() | (polls["voting_areas"].str.strip() == "")
n_missing = missing_va.sum()
n_elec_missing = (missing_va & (polls["ballot_type"] == "Election Day")).sum()
print(f"\nRows with missing voting_areas: {n_missing:,} "
      f"(of which Election Day: {n_elec_missing})")
if n_elec_missing > 0:
    print("  WARNING: Some Election Day rows have no voting_areas — "
          "those VAs cannot carry weights.")


# ===========================================================================
# STEP 2 — Build splat weights and apportion non-Election-Day votes
# ===========================================================================
print("\n" + "=" * 70)
print("STEP 2 — Building splat weights and apportioning non-ED votes")
print("=" * 70)

# Load the VA substrate (Election-Day votes only)
print("\nLoading VA substrate …")
va_gdf = gpd.read_file(VA_GPKG_IN)
print(f"  VA substrate: {len(va_gdf):,} rows, CRS={va_gdf.crs}")
print(f"  Columns: {list(va_gdf.columns)}")

# Identify vote columns in VA file
# Standard names from v0_1_phase_4c_va_attribution.py: va_ndp, va_ucp, va_other
# Double-check they exist
for col in ("va_ndp", "va_ucp", "va_other"):
    if col not in va_gdf.columns:
        sys.exit(f"ERROR: Column '{col}' not found in VA substrate. "
                 f"Found: {list(va_gdf.columns)}")

# Build a lookup:  (parent_ed_2019, VA_NUMBER_int)  ->  (va_ndp, va_ucp, va_other)
va_lookup = {}
for _, row in va_gdf.iterrows():
    key = (row["parent_ed_2019"], int(row["VA_NUMBER"]))
    va_lookup[key] = {
        "va_ndp":   float(row["va_ndp"]),
        "va_ucp":   float(row["va_ucp"]),
        "va_other": float(row["va_other"]),
    }

print(f"  VA lookup built: {len(va_lookup):,} entries")

# ---------------------------------------------------------------------------
# For each (ed_2019, sheet_num) group:
#   a) Identify the set of Election-Day VA_NUMBERs (and their vote totals)
#   b) For each non-ED poll in the same group, distribute votes by weight
#
# The weight of VA k = va_ndp_k + va_ucp_k  (two-party share)
# If the two-party total is zero, use equal weights across VAs.
# ---------------------------------------------------------------------------

# Accumulators:  va_key -> {apportioned_ndp, apportioned_ucp, apportioned_other}
apportioned = {}   # keyed by (ed_2019, va_num_int)

# Separate ED and non-ED polls
mask_ed  = polls["ballot_type"] == "Election Day"
polls_ed = polls[mask_ed].copy()
polls_non_ed = polls[~mask_ed].copy()

# Build group -> VA list from Election-Day polls
# Group key: (ed_2019, sheet_num)
# Each Election-Day row has voting_areas like "001,002,003"
def parse_vas(va_str):
    """Parse comma-separated VA_NUMBER string to list of ints."""
    if pd.isna(va_str) or str(va_str).strip() == "":
        return []
    return [int(x.strip()) for x in str(va_str).split(",") if x.strip().isdigit()]

# Build group lookup: (ed_2019, sheet_num) -> sorted list of unique VA ints
group_va_map = {}
for _, row in polls_ed.iterrows():
    gk = (row["ed_2019"], row["sheet_num"])
    vas = parse_vas(row["voting_areas"])
    existing = group_va_map.get(gk, set())
    existing.update(vas)
    group_va_map[gk] = existing

# Convert to sorted lists
group_va_map = {gk: sorted(vas) for gk, vas in group_va_map.items()}

# Count groups
n_groups_with_nonED = 0
n_unmatched_vas = 0
n_polls_distributed = 0
n_polls_skipped = 0

for _, non_ed_row in polls_non_ed.iterrows():
    ed   = non_ed_row["ed_2019"]
    snum = non_ed_row["sheet_num"]
    gk   = (ed, snum)

    ndp_poll   = non_ed_row["ndp_votes"]
    ucp_poll   = non_ed_row["ucp_votes"]
    other_poll = non_ed_row["other_votes"]
    total_poll = ndp_poll + ucp_poll + other_poll

    if total_poll == 0:
        # Nothing to distribute
        n_polls_skipped += 1
        continue

    # Get the VAs for this group
    va_nums = group_va_map.get(gk, [])

    if not va_nums:
        # No Election-Day VAs found for this group — fall back to
        # distributing evenly across all VAs in the ed_2019
        # (rare edge case; log and use fallback)
        # Try to find any VA in this ED
        ed_vas = [k[1] for k in va_lookup if k[0] == ed]
        if ed_vas:
            va_nums = sorted(set(ed_vas))
            n_polls_distributed += 1
        else:
            n_polls_skipped += 1
            continue

    n_groups_with_nonED += 1

    # Look up ED weights from VA substrate
    weights = []
    for va_num in va_nums:
        lookup_key = (ed, va_num)
        if lookup_key in va_lookup:
            w = va_lookup[lookup_key]["va_ndp"] + va_lookup[lookup_key]["va_ucp"]
        else:
            w = 0.0
            n_unmatched_vas += 1
        weights.append(w)

    total_weight = sum(weights)

    if total_weight == 0:
        # Equal weights
        eq = 1.0 / len(va_nums)
        weights = [eq] * len(va_nums)
        total_weight = 1.0

    # Distribute votes
    for va_num, w in zip(va_nums, weights):
        share = w / total_weight
        ak = (ed, va_num)
        if ak not in apportioned:
            apportioned[ak] = {"ndp": 0.0, "ucp": 0.0, "other": 0.0}
        apportioned[ak]["ndp"]   += ndp_poll   * share
        apportioned[ak]["ucp"]   += ucp_poll   * share
        apportioned[ak]["other"] += other_poll * share

    n_polls_distributed += 1

print(f"  Non-ED polls distributed: {n_polls_distributed:,}")
print(f"  Non-ED polls skipped (zero votes or no group match): {n_polls_skipped:,}")
print(f"  VA lookup misses during weighting: {n_unmatched_vas:,}")

# Verify apportioned totals
app_ndp   = sum(v["ndp"]   for v in apportioned.values())
app_ucp   = sum(v["ucp"]   for v in apportioned.values())
app_other = sum(v["other"] for v in apportioned.values())
print(f"\n  Apportioned totals:  NDP={app_ndp:,.1f}  UCP={app_ucp:,.1f}  "
      f"Other={app_other:,.1f}")


# ===========================================================================
# STEP 3 — Build full substrate GeoPackage and diagnostics CSV
# ===========================================================================
print("\n" + "=" * 70)
print("STEP 3 — Building full substrate and diagnostics")
print("=" * 70)

# Build new columns on va_gdf
va_gdf = va_gdf.copy()

full_ndp_list   = []
full_ucp_list   = []
full_other_list = []
app_ndp_list    = []
app_ucp_list    = []
app_other_list  = []

for _, row in va_gdf.iterrows():
    ed     = row["parent_ed_2019"]
    va_num = int(row["VA_NUMBER"])
    ak     = (ed, va_num)

    ed_ndp   = float(row["va_ndp"])
    ed_ucp   = float(row["va_ucp"])
    ed_other = float(row["va_other"])

    app  = apportioned.get(ak, {"ndp": 0.0, "ucp": 0.0, "other": 0.0})
    a_ndp   = app["ndp"]
    a_ucp   = app["ucp"]
    a_other = app["other"]

    full_ndp_list.append(ed_ndp + a_ndp)
    full_ucp_list.append(ed_ucp + a_ucp)
    full_other_list.append(ed_other + a_other)
    app_ndp_list.append(a_ndp)
    app_ucp_list.append(a_ucp)
    app_other_list.append(a_other)

va_gdf["va_ndp_full"]   = full_ndp_list
va_gdf["va_ucp_full"]   = full_ucp_list
va_gdf["va_other_full"] = full_other_list

# Write GeoPackage
print(f"\nWriting {VA_GPKG_OUT} …")
va_gdf.to_file(VA_GPKG_OUT, driver="GPKG")
print("  Done.")

# ---- Diagnostics CSV ----
diag_rows = []
for i, row in va_gdf.iterrows():
    ed     = row["parent_ed_2019"]
    va_num = int(row["VA_NUMBER"])

    ed_ndp   = float(row["va_ndp"])
    ed_ucp   = float(row["va_ucp"])
    a_ndp    = app_ndp_list[i]
    a_ucp    = app_ucp_list[i]
    a_other  = app_other_list[i]
    f_ndp    = float(row["va_ndp_full"])
    f_ucp    = float(row["va_ucp_full"])

    pct_adv_ndp = (a_ndp / f_ndp * 100) if f_ndp > 0 else 0.0

    diag_rows.append({
        "parent_ed_2019":        ed,
        "VA_NUMBER":             va_num,
        "election_day_ndp":      ed_ndp,
        "election_day_ucp":      ed_ucp,
        "apportioned_advance_ndp": a_ndp,
        "apportioned_advance_ucp": a_ucp,
        "full_ndp":              f_ndp,
        "full_ucp":              f_ucp,
        "pct_advance_ndp":       round(pct_adv_ndp, 2),
    })

diag_df = pd.DataFrame(diag_rows)
diag_df.to_csv(DIAG_CSV, index=False)
print(f"Diagnostics written: {DIAG_CSV}")
print(f"  Rows: {len(diag_df):,}")


# ===========================================================================
# STEP 4 — Validation
# ===========================================================================
print("\n" + "=" * 70)
print("STEP 4 — Validation")
print("=" * 70)

# Full-substrate totals
sub_full_ndp   = va_gdf["va_ndp_full"].sum()
sub_full_ucp   = va_gdf["va_ucp_full"].sum()
sub_full_other = va_gdf["va_other_full"].sum()
sub_full_total = sub_full_ndp + sub_full_ucp + sub_full_other

# Reference totals from polls CSV (all ballot types)
ref_ndp   = total_ndp_all
ref_ucp   = total_ucp_all
ref_other = total_other_all
ref_total = ref_ndp + ref_ucp + ref_other

print("\n--- Conservation check ---")
print(f"  Polls CSV total  NDP={ref_ndp:,.1f}  UCP={ref_ucp:,.1f}  "
      f"Other={ref_other:,.1f}  Total={ref_total:,.1f}")
print(f"  VA substrate full NDP={sub_full_ndp:,.1f}  UCP={sub_full_ucp:,.1f}  "
      f"Other={sub_full_other:,.1f}  Total={sub_full_total:,.1f}")

delta_ndp   = sub_full_ndp   - ref_ndp
delta_ucp   = sub_full_ucp   - ref_ucp
delta_other = sub_full_other - ref_other
delta_total = sub_full_total - ref_total

print(f"  Delta  NDP={delta_ndp:+.1f}  UCP={delta_ucp:+.1f}  "
      f"Other={delta_other:+.1f}  Total={delta_total:+.1f}")

tol = 1.0   # allow up to 1 vote of floating-point drift
if abs(delta_ndp) <= tol and abs(delta_ucp) <= tol and abs(delta_total) <= tol:
    print("  CONSERVATION PASS: NDP, UCP, and total match within rounding tolerance.")
else:
    print("  CONSERVATION FAIL: Totals do not match — investigate apportionment.")

# Province-wide NDP share comparison
ed_only_ndp = va_gdf["va_ndp"].sum()
ed_only_ucp = va_gdf["va_ucp"].sum()
ed_share = ed_only_ndp / (ed_only_ndp + ed_only_ucp) * 100
full_share = sub_full_ndp / (sub_full_ndp + sub_full_ucp) * 100

print("\n--- Province-wide NDP share ---")
print(f"  Election-Day-only substrate:  {ed_share:.2f}%  "
      f"({ed_only_ndp:,.0f} NDP / {ed_only_ndp + ed_only_ucp:,.0f} two-party)")
print(f"  Full (inc. advance/special):  {full_share:.2f}%  "
      f"({sub_full_ndp:,.0f} NDP / {sub_full_ndp + sub_full_ucp:,.0f} two-party)")
print(f"  Difference: {full_share - ed_share:+.2f} pp")

print("\n" + "=" * 70)
print("DONE")
print(f"  Output GeoPackage: {VA_GPKG_OUT}")
print(f"  Diagnostics CSV:   {DIAG_CSV}")
print("=" * 70)
