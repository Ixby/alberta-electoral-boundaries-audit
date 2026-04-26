#!/bin/bash
# recompute_against_official_shapefiles.sh
#
# Single-command re-run of every geometry-dependent finding in the
# audit against newly-released Elections Alberta official shapefiles.
# Honors the audit's pre-registered sunset clause (recompute within
# two weeks of release; this wrapper aims for one afternoon).
#
# Usage:
#   bash analysis/scripts/recompute_against_official_shapefiles.sh \
#       /path/to/official_majority_2026.gpkg \
#       /path/to/official_minority_2026.gpkg
#
# What it does:
#   1. Validates the input files (exist, readable, expected geometry)
#   2. Snapshots the current authoritative outputs to archive/ for
#      delta computation later
#   3. Stages the official files into data/shapefiles/derived/ with
#      filenames that the existing pipeline reads
#   4. Re-runs the audit:
#        a. MCMC ensemble (1,000,000 maps; 1M is sufficient for a
#           shapefile-grade re-run, 2M is overkill)
#        b. Targeted-burst hill-climb (UCP and NDP directions, for
#           symmetry per the audit's discipline)
#        c. Verification subset (10,000 steps with full assignments)
#        d. Article figures
#        e. PDF rebuild
#   5. Computes deltas between the re-run and the previously published
#      values, with explicit flags for any change above the
#      pre-registered sensitivity thresholds
#   6. Generates a stub pre-registration amendment file with the
#      deltas pre-filled (maintainer reviews and adds commentary)
#   7. Prints a summary of what changed and what the maintainer
#      needs to review before publishing
#
# What it does NOT do:
#   - Auto-commit or auto-push (maintainer reviews everything first)
#   - Update the public-facing report prose (maintainer rewrites the
#     few paragraphs that need new numbers)
#   - Touch the pre-registered prospective component (RQ8-9; that's
#     bound to the November Lunty committee map, not these files)
#
# Run time: 60-90 minutes on a 13th-gen i7-1360P laptop; less on
# modern cloud hardware. Most of the time is the MCMC re-run.

set -euo pipefail

# ----- Argument validation -----
if [ $# -ne 2 ]; then
    echo "ERROR: expected 2 arguments, got $#"
    echo "Usage: $0 <official_majority.gpkg> <official_minority.gpkg>"
    exit 2
fi

MAJORITY_INPUT="$1"
MINORITY_INPUT="$2"

if [ ! -r "$MAJORITY_INPUT" ]; then
    echo "ERROR: cannot read majority shapefile: $MAJORITY_INPUT"
    exit 2
fi
if [ ! -r "$MINORITY_INPUT" ]; then
    echo "ERROR: cannot read minority shapefile: $MINORITY_INPUT"
    exit 2
fi

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

TIMESTAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
SNAPSHOT_DIR="$REPO_ROOT/archive/recompute_$TIMESTAMP"
mkdir -p "$SNAPSHOT_DIR"

echo "==============================================================="
echo " AUDIT RE-RUN AGAINST OFFICIAL SHAPEFILES"
echo "==============================================================="
echo " Started:           $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo " Repo root:         $REPO_ROOT"
echo " Majority input:    $MAJORITY_INPUT"
echo " Minority input:    $MINORITY_INPUT"
echo " Snapshot dir:      $SNAPSHOT_DIR"
echo "==============================================================="

# ----- Step 1: Validate input geometry -----
echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 1/7: Validating input shapefiles"

PYTHONIOENCODING=utf-8 python - "$MAJORITY_INPUT" "$MINORITY_INPUT" <<'PY'
import sys
import geopandas as gpd

majority_path, minority_path = sys.argv[1], sys.argv[2]
ok = True
for label, path in [("majority", majority_path), ("minority", minority_path)]:
    g = gpd.read_file(path)
    n = len(g)
    has_name = any(c in g.columns for c in ["name_2026", "EDName", "ED_NAME", "name"])
    crs = g.crs
    print(f"  {label}: {n} polygons, CRS={crs}, has_name_column={has_name}")
    if n != 89:
        print(f"  WARN: expected 89 polygons for the 2026 maps, got {n}")
        # Not a hard fail — audit can still re-run, but flag for review
    if not has_name:
        print(f"  ERROR: no name column found; cannot proceed without district names")
        ok = False

if not ok:
    sys.exit(1)
PY

if [ $? -ne 0 ]; then
    echo "ERROR: input validation failed"
    exit 3
fi

# ----- Step 2: Snapshot current outputs -----
echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 2/7: Snapshotting current outputs to $SNAPSHOT_DIR"

cp -v data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv "$SNAPSHOT_DIR/" 2>/dev/null || true
cp -v data/v0_1_mcmc_real_map_scores_250k_v0_8.json "$SNAPSHOT_DIR/" 2>/dev/null || true
cp -v data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.json "$SNAPSHOT_DIR/" 2>/dev/null || true
cp -v data/v0_1_targeted_burst_best.json "$SNAPSHOT_DIR/" 2>/dev/null || true
cp -v data/v0_1_targeted_burst_ndp_best.json "$SNAPSHOT_DIR/" 2>/dev/null || true
cp -v data/shapefiles/derived/v0_8_full_refined_majority_2026_eds.gpkg "$SNAPSHOT_DIR/" 2>/dev/null || true
cp -v data/shapefiles/derived/v0_8_full_refined_minority_2026_eds.gpkg "$SNAPSHOT_DIR/" 2>/dev/null || true

echo "  snapshot complete"

# ----- Step 3: Stage official files into the pipeline location -----
echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 3/7: Staging official shapefiles into pipeline"

OFFICIAL_MAJ="data/shapefiles/derived/official_majority_2026_eds.gpkg"
OFFICIAL_MIN="data/shapefiles/derived/official_minority_2026_eds.gpkg"

cp "$MAJORITY_INPUT" "$OFFICIAL_MAJ"
cp "$MINORITY_INPUT" "$OFFICIAL_MIN"

# Backup the v0_8 reconstructions before overwriting
cp data/shapefiles/derived/v0_8_full_refined_majority_2026_eds.gpkg \
   data/shapefiles/derived/v0_8_full_refined_majority_2026_eds.gpkg.pre-official-backup
cp data/shapefiles/derived/v0_8_full_refined_minority_2026_eds.gpkg \
   data/shapefiles/derived/v0_8_full_refined_minority_2026_eds.gpkg.pre-official-backup

# Now overwrite so the existing pipeline picks them up without code changes
cp "$OFFICIAL_MAJ" data/shapefiles/derived/v0_8_full_refined_majority_2026_eds.gpkg
cp "$OFFICIAL_MIN" data/shapefiles/derived/v0_8_full_refined_minority_2026_eds.gpkg

echo "  official files staged at v0_8_full_refined_*.gpkg paths"
echo "  v0_8 reconstructions backed up to .pre-official-backup"

# ----- Step 4: Re-run the audit -----
echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 4a/7: MCMC ensemble re-run (1,000,000 maps)"
PYTHONIOENCODING=utf-8 python analysis/scripts/mcmc_ensemble_250k_v0_8.py \
    --n-steps 1000000 --n-chains 4 --chunk-size 5000 --seed 88 \
    > "analysis/reports/v0_1_mcmc_official_$TIMESTAMP.log" 2>&1

echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 4b/7: Targeted-burst (UCP-maximization)"
PYTHONIOENCODING=utf-8 python analysis/scripts/targeted_gerrymander_burst.py \
    > "analysis/reports/v0_1_targeted_burst_official_$TIMESTAMP.log" 2>&1

echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 4c/7: Targeted-burst (NDP-maximization, symmetric)"
PYTHONIOENCODING=utf-8 python analysis/scripts/targeted_gerrymander_burst_ndp.py \
    > "analysis/reports/v0_1_targeted_burst_ndp_official_$TIMESTAMP.log" 2>&1

echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 4d/7: Verification subset (10,000 steps with full assignments)"
PYTHONIOENCODING=utf-8 python analysis/scripts/mcmc_verification_subset.py \
    > "analysis/reports/v0_1_mcmc_verification_official_$TIMESTAMP.log" 2>&1

echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 5/7: Regenerating article figures"
PYTHONIOENCODING=utf-8 python analysis/scripts/article_figures.py \
    > "analysis/reports/v0_1_figures_official_$TIMESTAMP.log" 2>&1

# ----- Step 6: Compute deltas -----
echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 6/7: Computing deltas vs published values"

DELTA_REPORT="analysis/reports/v0_1_official_recompute_deltas_$TIMESTAMP.md"

PYTHONIOENCODING=utf-8 python - "$SNAPSHOT_DIR" "$DELTA_REPORT" <<'PY'
import json
import sys
from pathlib import Path
import pandas as pd

snapshot_dir = Path(sys.argv[1])
out_path = Path(sys.argv[2])

# Pre-registered sensitivity thresholds (from amendment 2026-04-23)
THRESHOLDS = {
    "efficiency_gap": 0.005,    # 0.5pp
    "mean_median": 0.005,
    "declination": 0.005,
    "seats_at_50_50": 0.005,
}

new_scores = json.loads(Path("data/v0_1_mcmc_real_map_scores_250k_v0_8.json").read_text())
old_scores_path = snapshot_dir / "v0_1_mcmc_real_map_scores_250k_v0_8.json"
if not old_scores_path.exists():
    print(f"WARN: no snapshot file at {old_scores_path}; skipping delta calculation")
    sys.exit(0)
old_scores = json.loads(old_scores_path.read_text())

lines = ["# Official-shapefile re-run delta report", ""]
lines.append(f"Generated: {sys.argv[2].split('_')[-1].rsplit('.', 1)[0]}")
lines.append("")
lines.append("## Per-metric, per-map deltas (re-run minus previously published)")
lines.append("")
lines.append("| Map | Metric | Previously published | Re-run (official) | Delta | Above 0.5pp threshold? |")
lines.append("|---|---|---|---|---|---|")

flags = []
for map_key in ("2019_enacted", "majority_2026", "minority_2026"):
    if map_key not in new_scores or map_key not in old_scores:
        continue
    new_m = new_scores[map_key]
    old_m = old_scores[map_key]
    for metric in ("efficiency_gap", "mean_median", "declination", "seats_at_50_50"):
        if metric not in new_m or metric not in old_m:
            continue
        old_v = old_m[metric]
        new_v = new_m[metric]
        delta = new_v - old_v
        threshold = THRESHOLDS[metric]
        flagged = abs(delta) > threshold
        if flagged:
            flags.append((map_key, metric, old_v, new_v, delta))
        flag_marker = " **YES**" if flagged else " no"
        lines.append(f"| {map_key} | {metric} | {old_v:+.4f} | {new_v:+.4f} | {delta:+.4f} |{flag_marker} |")

lines.append("")
lines.append("## Summary")
lines.append("")
if flags:
    lines.append(f"**{len(flags)} flagged delta(s) require disclosure** in a dated pre-registration amendment per the audit's standing commitment to publicly disclose any sign-flip or magnitude change > 0.5pp on partisan-bias metrics.")
    lines.append("")
    lines.append("Flagged metrics:")
    for map_key, metric, old_v, new_v, delta in flags:
        sign_flip = (old_v > 0 and new_v < 0) or (old_v < 0 and new_v > 0)
        sign_flip_marker = " — **SIGN FLIP**" if sign_flip else ""
        lines.append(f"- {map_key} / {metric}: {old_v:+.4f} -> {new_v:+.4f} (Δ {delta:+.4f}){sign_flip_marker}")
else:
    lines.append("**No deltas exceed the 0.5pp threshold.** Re-run confirms previously published findings within the pre-registered sensitivity tolerance. A brief note acknowledging the recompute (without a substantive amendment) is the appropriate disclosure.")

out_path.write_text("\n".join(lines), encoding="utf-8")
print(f"  delta report written to {out_path}")
print(f"  flagged deltas: {len(flags)}")
PY

# ----- Step 7: Rebuild PDF + generate amendment stub -----
echo ""
echo "[$(date -u +%H:%M:%SZ)] Step 7/7: Rebuilding report_public.pdf + amendment stub"
PYTHONIOENCODING=utf-8 python analysis/scripts/build_cover.py \
    > "analysis/reports/v0_1_pdf_rebuild_official_$TIMESTAMP.log" 2>&1

AMENDMENT_PATH="analysis/reports/v0_1_pre_registration_amendment_$(date -u +%Y-%m-%d)-official-shapefiles.md"
DATE_TODAY="$(date -u +%Y-%m-%d)"

cat > "$AMENDMENT_PATH" <<EOF
---
name: Pre-registration amendment — $DATE_TODAY (official Elections Alberta shapefiles)
description: Documents the audit's recomputation of all geometry-dependent metrics against Elections Alberta's official 2026 shapefiles. Honors the standing sunset-clause commitment from the 2026-04-23 amendment (revised duration from 2026-04-26 amendment Change 11). Submitted alongside the updated authoritative output files.
type: project
---

# Pre-registration amendment — $DATE_TODAY

**Registration:** Pre-registered signature-detection checklist for the Alberta MLA Special Select Committee's 91-seat electoral boundary map.
**Author:** Will Conner.
**Original upload:** 2026-04-23, 06:22 PM MT (OSF Registrations).
**Prior amendments:**
  - \`v0_1_pre_registration_amendment_2026-04-23.md\` (DPG sunset clause + 5 other changes)
  - \`v0_1_pre_registration_amendment_2026-04-26.md\` (11 changes including window relaxation)
**This amendment filed:** $DATE_TODAY.
**Reason for amendment:** Recomputation of all geometry-dependent metrics against Elections Alberta's official 2026 shapefiles, per the standing sunset-clause commitment.

---

## What was recomputed

[MAINTAINER: review the delta report at \`analysis/reports/v0_1_official_recompute_deltas_$TIMESTAMP.md\` and write the change summary here. Document each metric whose value moved, and explicitly flag any sign-flip or magnitude change exceeding the pre-registered 0.5pp threshold.]

## What did not change

[MAINTAINER: confirm that the pre-registered prospective component (RQ8-9) — the 17-test grid that will be applied to the November 2026 Lunty committee map — remains unchanged. The shapefile recompute affects retrospective findings only.]

## Public disclosure status

[MAINTAINER: note whether the public report has been updated to reflect the recomputed numbers, and where (which paragraphs).]

## Reproducibility chain

- Official majority shapefile: provided by Elections Alberta, hash: [maintainer to compute and record]
- Official minority shapefile: provided by Elections Alberta, hash: [maintainer to compute and record]
- Re-run wall time: $(date -u +%Y-%m-%dT%H:%M:%SZ) (snapshot dir: \`$SNAPSHOT_DIR\`)
- Snapshot of pre-recompute outputs: \`$SNAPSHOT_DIR\` (preserved for delta verification)
- All re-run logs: \`analysis/reports/*_official_$TIMESTAMP.log\`
EOF

echo "  amendment stub written to $AMENDMENT_PATH"

# ----- Final summary -----
echo ""
echo "==============================================================="
echo " RE-RUN COMPLETE"
echo "==============================================================="
echo " Finished:          $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo " Snapshot dir:      $SNAPSHOT_DIR"
echo " Delta report:      $DELTA_REPORT"
echo " Amendment stub:    $AMENDMENT_PATH"
echo " Re-run logs:       analysis/reports/*_official_$TIMESTAMP.log"
echo ""
echo " NEXT STEPS for the maintainer:"
echo "   1. Review the delta report"
echo "   2. Fill in the amendment stub with substantive commentary"
echo "   3. Update report_public.md prose where headline numbers moved"
echo "   4. Rebuild PDF: PYTHONIOENCODING=utf-8 python analysis/scripts/build_cover.py"
echo "   5. Commit and push the official-shapefile artefacts and amendment"
echo "   6. File the amendment to OSF"
echo "==============================================================="
