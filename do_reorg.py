"""
Reorganization script for alberta_audit project.
Performs Steps 1-4: delete empty nested dir, move shapefiles, move maps, update paths.
"""

import os
import shutil
from pathlib import Path

BASE = Path("C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit")

# ============================================================
# Step 1: Delete empty nested alberta_audit/alberta_audit/
# ============================================================
print("\n=== Step 1: Delete empty nested directory ===")
nested = BASE / "alberta_audit"
if nested.exists():
    # Confirm it has no files
    files = list(nested.rglob("*"))
    actual_files = [f for f in files if f.is_file()]
    print(f"  Nested dir exists. Files found: {len(actual_files)}")
    if actual_files:
        print(f"  WARNING: Found files in nested dir - aborting delete: {actual_files}")
    else:
        shutil.rmtree(nested)
        print(f"  Deleted {nested}")
else:
    print(f"  {nested} does not exist, skipping.")

# ============================================================
# Step 2: Create shapefile subdirs and move files
# ============================================================
print("\n=== Step 2: Organize shapefiles ===")

ref_dir = BASE / "data" / "shapefiles" / "reference"
der_dir = BASE / "data" / "shapefiles" / "derived"
ref_dir.mkdir(parents=True, exist_ok=True)
der_dir.mkdir(parents=True, exist_ok=True)
print(f"  Created {ref_dir}")
print(f"  Created {der_dir}")

data_dir = BASE / "data"

# Reference files/dirs
reference_items = [
    "alberta_2021_csds.gpkg",
    "alberta_2021_das.gpkg",
    "alberta_2019_eds",
    "alberta_2023_vas",
]

for item in reference_items:
    src = data_dir / item
    dst = ref_dir / item
    if src.exists():
        shutil.move(str(src), str(dst))
        print(f"  Moved reference: {item} -> shapefiles/reference/")
    else:
        print(f"  SKIP (not found): {src}")

# Derived: all .gpkg files starting with v0_ or va_polygons
derived_gpkgs = [
    f.name for f in data_dir.glob("*.gpkg")
    if f.stem.startswith("v0_") or f.stem.startswith("va_polygons")
]
derived_gpkgs.sort()
print(f"\n  Found {len(derived_gpkgs)} derived .gpkg files to move:")
for name in derived_gpkgs:
    src = data_dir / name
    dst = der_dir / name
    shutil.move(str(src), str(dst))
    print(f"  Moved derived: {name} -> shapefiles/derived/")

# ============================================================
# Step 3: Move maps/ -> data/maps/
# ============================================================
print("\n=== Step 3: Move maps/ -> data/maps/ ===")
maps_src = BASE / "maps"
maps_dst = BASE / "data" / "maps"

if maps_src.exists():
    if maps_dst.exists():
        print(f"  WARNING: {maps_dst} already exists. Merging...")
        shutil.copytree(str(maps_src), str(maps_dst), dirs_exist_ok=True)
        shutil.rmtree(str(maps_src))
    else:
        shutil.move(str(maps_src), str(maps_dst))
    print(f"  Moved maps/ -> data/maps/")
else:
    print(f"  {maps_src} does not exist, skipping.")

# ============================================================
# Step 4: Update path references in Python scripts
# ============================================================
print("\n=== Step 4: Update path references ===")

scripts_dir = BASE / "analysis" / "scripts"

# Build the complete list of derived gpkg filenames for path replacement
# (from what we just moved)
derived_gpkg_names = derived_gpkgs

def make_replacements(derived_names):
    """Build ordered list of (old, new) string replacements."""
    replacements = []

    # --- Reference shapefiles (Path-style) ---
    ref_path_subs = [
        ('DATA / "alberta_2021_csds.gpkg"',
         'DATA / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"'),
        ('DATA / "alberta_2021_das.gpkg"',
         'DATA / "shapefiles" / "reference" / "alberta_2021_das.gpkg"'),
        ('DATA / "alberta_2019_eds"',
         'DATA / "shapefiles" / "reference" / "alberta_2019_eds"'),
        ('DATA / "alberta_2023_vas"',
         'DATA / "shapefiles" / "reference" / "alberta_2023_vas"'),
        # out_data_dir variants
        ("out_data_dir / 'alberta_2019_eds'",
         "out_data_dir / 'shapefiles' / 'reference' / 'alberta_2019_eds'"),
    ]
    replacements.extend(ref_path_subs)

    # --- Reference shapefiles (raw string paths, e.g. in dependency_graph_build.py) ---
    ref_str_subs = [
        ('"data/alberta_2021_csds.gpkg"',
         '"data/shapefiles/reference/alberta_2021_csds.gpkg"'),
        ('"data/alberta_2021_das.gpkg"',
         '"data/shapefiles/reference/alberta_2021_das.gpkg"'),
        ('"data/alberta_2019_eds/',
         '"data/shapefiles/reference/alberta_2019_eds/'),
        ('"data/alberta_2023_vas/',
         '"data/shapefiles/reference/alberta_2023_vas/'),
    ]
    replacements.extend(ref_str_subs)

    # --- Derived shapefiles (Path-style, DATA / "filename") ---
    for name in derived_names:
        old = f'DATA / "{name}"'
        new = f'DATA / "shapefiles" / "derived" / "{name}"'
        replacements.append((old, new))

    # --- Derived shapefiles (va_polygons explicit) ---
    for va_name in ["va_polygons_with_2023_votes.gpkg", "va_polygons_with_full_2023_votes.gpkg"]:
        old = f'DATA / "{va_name}"'
        new = f'DATA / "shapefiles" / "derived" / "{va_name}"'
        # Already handled above via loop, but add as fallback
        if old not in [r[0] for r in replacements]:
            replacements.append((old, new))

    # --- out_data_dir derived variants ---
    out_dir_subs = [
        ("out_data_dir / 'v0_2_canonical_majority_2026_eds_topoclean.gpkg'",
         "out_data_dir / 'shapefiles' / 'derived' / 'v0_2_canonical_majority_2026_eds_topoclean.gpkg'"),
        ("out_data_dir / 'v0_2_canonical_minority_2026_eds_topoclean.gpkg'",
         "out_data_dir / 'shapefiles' / 'derived' / 'v0_2_canonical_minority_2026_eds_topoclean.gpkg'"),
    ]
    replacements.extend(out_dir_subs)

    # --- Maps paths ---
    maps_subs = [
        ('ROOT / "maps"', 'ROOT / "data" / "maps"'),
        ("'../maps/", "'../data/maps/"),
        # String literal maps references in dependency graph
        ('"maps/majority_calgary.jpg, maps/minority_*.jpg"',
         '"data/maps/majority_calgary.jpg, data/maps/minority_*.jpg"'),
    ]
    replacements.extend(maps_subs)

    return replacements

replacements = make_replacements(derived_gpkg_names)

py_files = list(scripts_dir.glob("*.py"))
print(f"  Found {len(py_files)} Python scripts to process")

total_changes = 0
for py_file in sorted(py_files):
    original = py_file.read_text(encoding="utf-8")
    updated = original
    file_changes = []
    for old, new in replacements:
        if old in updated:
            count = updated.count(old)
            updated = updated.replace(old, new)
            old_short = repr(old)[:60]
            new_short = repr(new)[:60]
            file_changes.append(f"    [{count}x] {old_short} -> {new_short}")
    if updated != original:
        py_file.write_text(updated, encoding="utf-8")
        total_changes += len(file_changes)
        print(f"\n  Updated: {py_file.name}")
        for change in file_changes:
            print(change)

print(f"\n  Total replacements: {total_changes}")

# ============================================================
# Step 4b: Update path references in .md files
# ============================================================
print("\n=== Step 4b: Update path references in .md files ===")

# report_academic.md at root
md_file_replacements = {
    BASE / "report_academic.md": [
        ("maps/hires/", "data/maps/hires/"),
        ("maps/hires_v2/", "data/maps/hires_v2/"),
        ("maps/mcmc/", "data/maps/mcmc/"),
        ("maps/article/", "data/maps/article/"),
        ("maps/verification/", "data/maps/verification/"),
        ("maps/neighbour_drain_", "data/maps/neighbour_drain_"),
        ("maps/audit_dependency_graph.svg", "data/maps/audit_dependency_graph.svg"),
    ],
    BASE / "analysis" / "reports" / "v0_1_neighbour_drain_analysis.md": [
        ("maps/neighbour_drain_phase_space_", "data/maps/neighbour_drain_phase_space_"),
    ],
    BASE / "analysis" / "reports" / "v0_1_max_dpi_extraction_and_rerun.md": [
        ("maps/hires/", "data/maps/hires/"),
        ("maps/hires_v2/", "data/maps/hires_v2/"),
    ],
}

for md_path, subs in md_file_replacements.items():
    if not md_path.exists():
        print(f"  SKIP (not found): {md_path}")
        continue
    original = md_path.read_text(encoding="utf-8")
    updated = original
    file_changes = []
    for old, new in subs:
        if old in updated:
            count = updated.count(old)
            updated = updated.replace(old, new)
            file_changes.append(f"    [{count}x] {old!r} -> {new!r}")
    if updated != original:
        md_path.write_text(updated, encoding="utf-8")
        print(f"\n  Updated: {md_path.name}")
        for change in file_changes:
            print(change)
    else:
        print(f"  No changes needed: {md_path.name}")

# Also scan all .md files in analysis/reports/ for maps/ references
print("\n  Scanning analysis/reports/*.md for maps/ references...")
reports_dir = BASE / "analysis" / "reports"
maps_sub_patterns = [
    ("maps/hires/", "data/maps/hires/"),
    ("maps/hires_v2/", "data/maps/hires_v2/"),
    ("maps/mcmc/", "data/maps/mcmc/"),
    ("maps/article/", "data/maps/article/"),
    ("maps/verification/", "data/maps/verification/"),
    ("maps/neighbour_drain_", "data/maps/neighbour_drain_"),
    ("maps/audit_dependency_graph.svg", "data/maps/audit_dependency_graph.svg"),
]
for md_file in sorted(reports_dir.glob("*.md")):
    original = md_file.read_text(encoding="utf-8")
    updated = original
    file_changes = []
    for old, new in maps_sub_patterns:
        if old in updated:
            count = updated.count(old)
            updated = updated.replace(old, new)
            file_changes.append(f"    [{count}x] {old!r} -> {new!r}")
    if updated != original:
        md_file.write_text(updated, encoding="utf-8")
        print(f"  Updated: {md_file.name}")
        for change in file_changes:
            print(change)

# ============================================================
# Step 5: Verification
# ============================================================
print("\n=== Verification ===")

# Check key files exist in new locations
checks = [
    ref_dir / "alberta_2021_csds.gpkg",
    ref_dir / "alberta_2021_das.gpkg",
    ref_dir / "alberta_2019_eds",
    ref_dir / "alberta_2023_vas",
    BASE / "data" / "maps",
]
for check in checks:
    status = "OK" if check.exists() else "MISSING"
    print(f"  [{status}] {check.relative_to(BASE)}")

# Check some derived gpkgs
for name in ["v0_1_approximate_majority_2026_eds.gpkg", "v0_5_canonical_majority_2026_eds_da_anchored.gpkg"]:
    path = der_dir / name
    status = "OK" if path.exists() else "MISSING"
    print(f"  [{status}] data/shapefiles/derived/{name}")

# Check maps
maps_check = BASE / "data" / "maps" / "hires"
status = "OK" if maps_check.exists() else "MISSING"
print(f"  [{status}] data/maps/hires/")

# Confirm old locations are gone
old_checks = [
    data_dir / "alberta_2021_csds.gpkg",
    data_dir / "alberta_2021_das.gpkg",
    BASE / "maps",
]
for check in old_checks:
    status = "GONE (OK)" if not check.exists() else "STILL EXISTS (problem)"
    print(f"  [{status}] {check.relative_to(BASE)}")

print("\n=== Done ===")
