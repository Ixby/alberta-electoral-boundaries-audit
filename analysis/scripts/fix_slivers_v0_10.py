"""
fix_slivers_v0_10.py
--------------------
Resolves topology slivers in the v0_9 majority and minority maps and produces
v0_10 canonical shapefiles.

Resolution rule:
  For each overlapping pair (A, B), subtract the sliver from whichever district
  contributes the SMALLER FRACTION of its own area to the overlap -- i.e. the
  sliver is a tiny piece of that district, so we take it away from it and leave
  it entirely inside the other.  The district for which the sliver represents a
  LARGER fraction "needs" it more and wins it.

  Tie-break: assign to the LARGER district (by area).

Key implementation notes:
  - Uses a convergence loop: re-scan for overlaps after every resolution step
    until none remain, handling cases where one district overlaps multiple
    neighbours.
  - Deletes destination file before writing to avoid stale layers in gpkg.
  - Specifies explicit layer names on read and write.
"""

import os
import warnings
import geopandas as gpd
import pandas as pd
from shapely.validation import make_valid

warnings.filterwarnings("ignore")

DERIVED = (
    r"C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis"
    r"\alberta_audit\data\shapefiles\derived"
)
SRC_MAJ   = f"{DERIVED}\\v0_9_topological_majority_2026_eds.gpkg"
SRC_MIN   = f"{DERIVED}\\v0_9_topological_minority_2026_eds.gpkg"
DST_MAJ   = f"{DERIVED}\\v0_10_topological_majority_2026_eds.gpkg"
DST_MIN   = f"{DERIVED}\\v0_10_topological_minority_2026_eds.gpkg"
LAYER_MAJ = "v0_10_topological_majority_2026_eds"
LAYER_MIN = "v0_10_topological_minority_2026_eds"
THRESHOLD = 100  # m2


def find_overlaps(gdf, name_col="name_2026", threshold=THRESHOLD):
    """Return list of dicts describing all overlapping pairs above threshold."""
    geoms = list(gdf.geometry)
    names = list(gdf[name_col])
    idxs  = list(gdf.index)
    pairs = []
    for ii in range(len(geoms)):
        for jj in range(ii + 1, len(geoms)):
            gi, gj = geoms[ii], geoms[jj]
            if not gi.intersects(gj):
                continue
            inter = gi.intersection(gj)
            area  = inter.area
            if area > threshold:
                fi = area / gi.area
                fj = area / gj.area
                pairs.append(dict(
                    ii=ii, jj=jj,
                    idx_i=idxs[ii], idx_j=idxs[jj],
                    name_i=names[ii], name_j=names[jj],
                    sliver_area=area,
                    frac_i=fi, frac_j=fj,
                    geom_i_area=gi.area, geom_j_area=gj.area,
                    inter=inter,
                ))
    return pairs


def resolve_one_pass(geom_dict, pairs, label=""):
    """Apply one resolution pass over pairs. Returns list of action strings."""
    actions = []
    for p in pairs:
        fi, fj = p["frac_i"], p["frac_j"]
        ni, nj = p["name_i"], p["name_j"]
        ai, aj = p["geom_i_area"], p["geom_j_area"]

        # Recompute current intersection from the (possibly already trimmed) geoms
        current_gi = geom_dict[p["idx_i"]]
        current_gj = geom_dict[p["idx_j"]]
        current_inter = current_gi.intersection(current_gj)
        current_area  = current_inter.area
        if current_area <= THRESHOLD:
            actions.append(f"    {ni} vs {nj}: already resolved (area now {current_area:.1f} m2)")
            continue

        # Re-compute fractions from current areas
        fi = current_area / current_gi.area
        fj = current_area / current_gj.area

        if fi < fj:
            loser, winner = p["idx_i"], p["idx_j"]
            loser_name, winner_name = ni, nj
            reason = f"frac_i={fi:.6f} < frac_j={fj:.6f}"
        elif fj < fi:
            loser, winner = p["idx_j"], p["idx_i"]
            loser_name, winner_name = nj, ni
            reason = f"frac_j={fj:.6f} < frac_i={fi:.6f}"
        else:
            cur_ai = current_gi.area
            cur_aj = current_gj.area
            if cur_ai >= cur_aj:
                loser, winner = p["idx_j"], p["idx_i"]
                loser_name, winner_name = nj, ni
                reason = f"tie -> larger wins ({ni}: {cur_ai:.0f} m2)"
            else:
                loser, winner = p["idx_i"], p["idx_j"]
                loser_name, winner_name = ni, nj
                reason = f"tie -> larger wins ({nj}: {cur_aj:.0f} m2)"

        msg = (
            f"    {ni} vs {nj}:"
            f"  LOSER={loser_name} (loses {current_area:.1f} m2),"
            f"  WINNER={winner_name}  [{reason}]"
        )
        actions.append(msg)
        new_geom = make_valid(geom_dict[loser].difference(current_inter))
        geom_dict[loser] = new_geom
    return actions


def fix_map(gdf, label, name_col="name_2026"):
    """Find and resolve all slivers with a convergence loop. Returns fixed GDF."""
    print(f"\n  --- Fixing {label} map ---")
    geom_dict = dict(zip(gdf.index, gdf.geometry))
    all_actions = []
    iteration = 0
    while True:
        iteration += 1
        # Rebuild a temporary GDF from current geom_dict to scan
        tmp = gdf.copy()
        tmp["geometry"] = pd.Series(geom_dict).reindex(tmp.index).values
        tmp = tmp.set_geometry("geometry")
        pairs = find_overlaps(tmp, name_col=name_col)
        if not pairs:
            break
        print(f"  Iteration {iteration}: {len(pairs)} overlapping pair(s)")
        actions = resolve_one_pass(geom_dict, pairs, label=label)
        for a in actions:
            print(a)
        all_actions.extend(actions)
        if iteration > 20:
            print("  WARNING: convergence not reached after 20 iterations; stopping.")
            break

    fixed = gdf.copy()
    fixed["geometry"] = pd.Series(geom_dict).reindex(fixed.index).values
    fixed = fixed.set_geometry("geometry")

    # Repair any invalid geometries introduced by the difference operation
    n_invalid = (~fixed.geometry.is_valid).sum()
    if n_invalid:
        print(f"  Repairing {n_invalid} invalid geometries...")
        fixed.geometry = fixed.geometry.apply(make_valid)

    print(f"  Converged after {iteration} iteration(s). Total actions: {len(all_actions)}")
    return fixed


def save_gpkg(gdf, path, layer):
    """Delete existing file then write fresh, avoiding stale layers."""
    if os.path.exists(path):
        os.remove(path)
    gdf.to_file(path, driver="GPKG", layer=layer)
    print(f"  Saved {len(gdf)} features -> {path}  (layer={layer})")


def verify(path, layer, name_col="name_2026"):
    """Read back and verify: count, validity, name uniqueness, zero overlaps."""
    df = gpd.read_file(path, layer=layer)
    n  = len(df)
    n_invalid = int((~df.geometry.is_valid).sum())
    n_unique  = int(df[name_col].nunique())
    n_dupes   = n - n_unique
    pairs = find_overlaps(df, name_col=name_col)
    n_overlaps = len(pairs)
    print(f"    District count : {n}")
    print(f"    Geometry valid : {'PASS' if n_invalid == 0 else 'FAIL (' + str(n_invalid) + ' invalid)'}")
    print(f"    Name uniqueness: {'PASS' if n_dupes == 0 else 'FAIL (' + str(n_dupes) + ' dupes)'}  ({n_unique} unique)")
    print(f"    Zero overlaps  : {'PASS' if n_overlaps == 0 else 'FAIL (' + str(n_overlaps) + ' pairs)'}")
    print(f"    CRS            : {df.crs}")
    if pairs:
        for p in pairs:
            print(f"      still overlapping: {p['name_i']} vs {p['name_j']}: {p['sliver_area']:.1f} m2")
    return n_overlaps == 0 and n_invalid == 0 and n_dupes == 0


# ─────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("STEP 1 -- Load v0_9 majority map")
maj_gdf = gpd.read_file(SRC_MAJ)
print(f"  Loaded {len(maj_gdf)} districts, CRS={maj_gdf.crs}")
print(f"  Columns: {list(maj_gdf.columns)}")

print()
print("STEP 2 -- Identify overlapping pairs in majority (area > 100 m2)")
maj_pairs_initial = find_overlaps(maj_gdf)
print(f"  Found {len(maj_pairs_initial)} overlapping pair(s):")
for p in maj_pairs_initial:
    print(f"    {p['name_i']} vs {p['name_j']}: sliver={p['sliver_area']:.1f} m2, frac_i={p['frac_i']:.6f}, frac_j={p['frac_j']:.6f}")

print()
print("STEP 3 -- Resolve majority overlaps")
maj_fixed = fix_map(maj_gdf, "MAJORITY")

print()
print("STEP 4 -- Verify majority in-memory (before save)")
pairs_check = find_overlaps(maj_fixed)
print(f"  In-memory check: {len(pairs_check)} overlapping pairs.")
if not pairs_check:
    print("  PASS -- zero overlaps in fixed majority.")
else:
    for p in pairs_check:
        print(f"  STILL: {p['name_i']} vs {p['name_j']}: {p['sliver_area']:.1f} m2")

print()
print("STEP 5 -- Save majority v0_10")
save_gpkg(maj_fixed, DST_MAJ, LAYER_MAJ)

print()
print("STEP 6 -- Load v0_9 minority map and check for overlaps")
min_gdf = gpd.read_file(SRC_MIN)
print(f"  Loaded {len(min_gdf)} districts, CRS={min_gdf.crs}")
min_pairs_initial = find_overlaps(min_gdf)
print(f"  Found {len(min_pairs_initial)} overlapping pair(s) in minority:")
for p in min_pairs_initial:
    print(f"    {p['name_i']} vs {p['name_j']}: sliver={p['sliver_area']:.1f} m2, frac_i={p['frac_i']:.6f}, frac_j={p['frac_j']:.6f}")

if not min_pairs_initial:
    print("  Minority is clean -- copying verbatim.")
    import shutil
    if os.path.exists(DST_MIN):
        os.remove(DST_MIN)
    shutil.copy2(SRC_MIN, DST_MIN)
    print(f"  Copied to {DST_MIN}")
else:
    print()
    print("  Resolving minority overlaps...")
    min_fixed = fix_map(min_gdf, "MINORITY")
    print()
    print("  Verify minority in-memory (before save)")
    pairs_check_min = find_overlaps(min_fixed)
    if not pairs_check_min:
        print("  PASS -- zero overlaps in fixed minority.")
    else:
        for p in pairs_check_min:
            print(f"  STILL: {p['name_i']} vs {p['name_j']}: {p['sliver_area']:.1f} m2")
    print()
    print("  Save minority v0_10")
    save_gpkg(min_fixed, DST_MIN, LAYER_MIN)

print()
print("=" * 70)
print("STEP 7 -- Final verification: both v0_10 files")

print()
print(f"  [MAJORITY]  {DST_MAJ}")
ok_maj = verify(DST_MAJ, LAYER_MAJ)

print()
print(f"  [MINORITY]  {DST_MIN}")
# minority layer name: if copied verbatim it keeps old layer name
import pyogrio
layers_min = pyogrio.list_layers(DST_MIN)
actual_layer_min = layers_min[0][0]  # first layer name
ok_min = verify(DST_MIN, actual_layer_min)

print()
print("=" * 70)
overall = "ALL PASS" if (ok_maj and ok_min) else "SOME CHECKS FAILED"
print(f"Result: {overall}")
print("Done.")
