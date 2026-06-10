# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
run_structural_battery.py — November 2026 held-out structural test runner
==========================================================================

Companion to preregistration/november_2026_scoring_spec.md §3 (structural-lane
S1–S6 battery). Takes any candidate map shapefile (commission proposal, Lunty
committee output, third-party submission) and produces a uniform structural
scorecard ready for verdict_synthesis.py.

The script is intentionally a thin orchestrator. Every metric is computed by
a previously-validated script in this directory; this file enforces the
pre-committed battery shape, threshold values, and output format. No new
methodology is introduced — only the structural-battery aggregation rule
from the November spec.

Inputs
------
--shapefile PATH       Candidate map shapefile (.gpkg or .shp). Required.
--votes PATH           Optional. VA-level vote shapefile (default:
                       data/shapefiles/canonical/va_2023_election_day_votes.gpkg).
                       Used by S5 (drain) and S1 (per-ED population MAD).
--reference PATH       Reference shapefile for S2 municipal-split baseline
                       (default: the canonical majority shapefile — when scoring
                       a non-commission map, S2's "≥ 1.5× majority's count"
                       reads against this reference).
--output PATH          JSON output path (default:
                       findings/lunty_structural.json).
--label STRING         Human-readable label for the candidate map; e.g.
                       "lunty_2026", "third_party_submission_42". Default:
                       basename of --shapefile.

Output
------
JSON shape:

{
  "candidate_label": "lunty_2026",
  "candidate_shapefile": "...",
  "executed_at_utc": "2026-11-XX...",
  "drand_round_at_execution": null,    # filled by November scoring driver
  "metrics": {
    "S1_population_mad": {"value": ..., "threshold": ..., "flag": bool},
    "S2_municipal_split_count": {...},
    "S3_anchoring_score": {...},
    "S4_polsby_popper_median": {...},
    "S5_drain_score": {...},
    "S6_chair_flag_replication": {...}
  },
  "structural_lane_flags": int,        # 0-6
  "structural_lane_verdict": "replicated" | "not_replicated",
  "thresholds_pre_committed_at": "preregistration/november_2026_scoring_spec.md"
}

Reproduction
------------
  python analysis/scripts/run_structural_battery.py \\
    --shapefile data/shapefiles/canonical/ea_minority_2026_eds.gpkg \\
    --output findings/structural_minority_recheck.json

Verdict rule (pre-committed): ≥ 3 flags = "replicated"; 0–2 = "not_replicated".

Backward:
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg  (reference baseline)
  data/shapefiles/canonical/va_2023_election_day_votes.gpkg
  preregistration/november_2026_scoring_spec.md       (thresholds frozen here)
  analysis/scripts/polsby_popper.py                   (S4)
  analysis/scripts/municipal_splits.py                (S2)
  analysis/scripts/score_anchoring.py                 (S3)
  analysis/scripts/neighbour_drain_adjacency.py       (S5 raw score)
  analysis/scripts/drain_label_shuffle_null.py        (S5 null)

Forward:
  findings/<candidate>_structural.json (consumed by verdict_synthesis.py)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import geopandas as gpd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))


# ----- Pre-committed thresholds (preregistration/november_2026_scoring_spec.md §3) -----

# S1: population MAD threshold = 1.5 × majority commission proposal's MAD.
#     Majority's canonical MAD will be cached in this constant once the
#     S1_BASELINE_MAJORITY_MAD is computed against canonical (currently
#     filled in from data/outputs/simulation_real_map_scores_canonical.json:
#     majority population_mad = 2826.89). Frozen 2026-06-10.
S1_BASELINE_MAJORITY_MAD = 2826.89
S1_MULTIPLIER = 1.5

# S2: municipal split count threshold = 1.5 × majority's count of municipalities
#     split into 3+ EDs. Majority's canonical count: 8 (per municipal_splits.py
#     canonical run). Frozen 2026-06-10.
S2_BASELINE_MAJORITY_TRIPLE_SPLITS = 8
S2_MULTIPLIER = 1.5

# S3: anchoring score band. Within 70–85% Canadian norm = neutral; outside = flag.
S3_BAND_LOW = 0.70
S3_BAND_HIGH = 0.85

# S4: Polsby-Popper compactness median threshold = majority's median − 0.10.
#     Majority's canonical median Polsby-Popper: 0.348 (per polsby_popper.py canonical run).
S4_BASELINE_MAJORITY_MEDIAN_PP = 0.348
S4_DELTA = 0.10

# S5: neighbour-drain score threshold + label-shuffle null p < 0.05.
S5_DRAIN_THRESHOLD = 0.05
S5_NULL_PVALUE_THRESHOLD = 0.05

# S6: chair-flagged boundary patterns replicated.
#     The minority's pre-flagged patterns are listed in findings/chair_recommendation_5_analysis.md.
S6_FLAG_THRESHOLD = 1   # ≥ 1 pattern reproduced = flag

# Verdict rule
STRUCTURAL_REPLICATED_THRESHOLD = 3   # ≥ 3 flags = "replicated"


def compute_S1_population_mad(shapefile: Path, votes_path: Path) -> dict:
    """S1: Per-ED population MAD against the 2021 census baseline.

    Reads the candidate shapefile, computes per-ED population by overlaying
    the canonical 2021-census-on-VA population table. MAD = mean absolute
    deviation from ideal per-district population.

    Threshold: candidate MAD ≥ 1.5 × S1_BASELINE_MAJORITY_MAD = flag.
    """
    # TODO(november-2026): Wire in the per-ED population computation. The
    # canonical pipeline already does this in mcmc_ensemble.py via
    # data/va_pop_from_das.csv overlay. Extract into a helper.
    # Stub returns NaN with the threshold annotation; verdict_synthesis.py
    # treats NaN as "did not execute" rather than as a flag.
    return {
        "value": float("nan"),
        "threshold": S1_BASELINE_MAJORITY_MAD * S1_MULTIPLIER,
        "flag": None,
        "_note": "STUB — wire in per-ED population overlay before November.",
    }


def compute_S2_municipal_splits(shapefile: Path, reference: Path) -> dict:
    """S2: Count of municipalities split into ≥3 EDs.

    Imports the scoring logic from municipal_splits.py rather than shelling out.
    """
    # TODO(november-2026): Refactor municipal_splits.py to expose a callable
    # `count_triple_splits(shapefile_path: Path) -> int` and use it here.
    return {
        "value": None,
        "threshold": int(S2_BASELINE_MAJORITY_TRIPLE_SPLITS * S2_MULTIPLIER),
        "flag": None,
        "_note": "STUB — extract count_triple_splits() from municipal_splits.py.",
    }


def compute_S3_anchoring(shapefile: Path) -> dict:
    """S3: % population in EDs anchored to a single municipality or county.

    Uses score_anchoring.py's compute_anchoring_score().
    """
    try:
        sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
        from score_anchoring import compute_anchoring_score
        score = compute_anchoring_score(shapefile)
        flag = bool(score < S3_BAND_LOW or score > S3_BAND_HIGH)
        return {
            "value": float(score),
            "threshold": [S3_BAND_LOW, S3_BAND_HIGH],
            "flag": flag,
        }
    except (ImportError, AttributeError) as e:
        return {
            "value": None,
            "threshold": [S3_BAND_LOW, S3_BAND_HIGH],
            "flag": None,
            "_note": f"STUB — score_anchoring.compute_anchoring_score not exposed yet ({e}).",
        }


def compute_S4_polsby_popper(shapefile: Path) -> dict:
    """S4: Median Polsby-Popper compactness across the candidate's EDs.

    Reuses polsby_popper.score_map().
    """
    try:
        sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
        from polsby_popper import score_map
        df = score_map(shapefile, "candidate")
        median_pp = float(df["polsby_popper"].median())
        flag = bool(median_pp < (S4_BASELINE_MAJORITY_MEDIAN_PP - S4_DELTA))
        return {
            "value": median_pp,
            "threshold": S4_BASELINE_MAJORITY_MEDIAN_PP - S4_DELTA,
            "flag": flag,
        }
    except Exception as e:
        return {
            "value": None,
            "threshold": S4_BASELINE_MAJORITY_MEDIAN_PP - S4_DELTA,
            "flag": None,
            "_note": f"STUB — polsby_popper.score_map signature drift ({e}).",
        }


def compute_S5_drain(shapefile: Path, votes_path: Path) -> dict:
    """S5: Neighbour-drain adjacency pattern + label-shuffle null p-value."""
    # TODO(november-2026): Refactor neighbour_drain_adjacency.py to expose
    # drain_score(shapefile, votes) → float, and drain_label_shuffle_null.py
    # to expose null_pvalue(score, n_permutations=10000) → float.
    return {
        "drain_score": None,
        "null_pvalue": None,
        "threshold": {"drain": S5_DRAIN_THRESHOLD, "null_p": S5_NULL_PVALUE_THRESHOLD},
        "flag": None,
        "_note": "STUB — wire in drain_score() and label-shuffle null functions.",
    }


def compute_S6_chair_flags(shapefile: Path) -> dict:
    """S6: Count of chair-flagged boundary patterns reproduced.

    The minority's pre-flagged patterns: see findings/chair_recommendation_5_analysis.md
    and chair_flagged_boundaries.json (Justice Miller's anomaly notes).

    This is a structural pattern-match: does the candidate map split Airdrie into
    ≥3 EDs? Does it route a corridor through the Bow Valley north of Banff? Etc.
    """
    # TODO(november-2026): Catalog the patterns from chair_recommendation_5_analysis.md
    # as a JSON predicate list, then evaluate each against the candidate shapefile.
    return {
        "patterns_reproduced": None,
        "threshold": S6_FLAG_THRESHOLD,
        "flag": None,
        "_note": "STUB — chair-flag pattern predicates not yet catalogued.",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--shapefile", type=Path, required=True,
                    help="Candidate map shapefile (.gpkg or .shp).")
    ap.add_argument("--votes", type=Path,
                    default=ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg")
    ap.add_argument("--reference", type=Path,
                    default=ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg")
    ap.add_argument("--output", type=Path,
                    default=ROOT / "findings/structural_battery_result.json")
    ap.add_argument("--label", type=str, default=None)
    args = ap.parse_args(argv)

    label = args.label or args.shapefile.stem
    print(f"[structural battery] candidate={label}  shapefile={args.shapefile}")

    if not args.shapefile.exists():
        print(f"ERROR: shapefile not found: {args.shapefile}", file=sys.stderr)
        return 2

    metrics = {
        "S1_population_mad":         compute_S1_population_mad(args.shapefile, args.votes),
        "S2_municipal_split_count":  compute_S2_municipal_splits(args.shapefile, args.reference),
        "S3_anchoring_score":        compute_S3_anchoring(args.shapefile),
        "S4_polsby_popper_median":   compute_S4_polsby_popper(args.shapefile),
        "S5_drain_score":            compute_S5_drain(args.shapefile, args.votes),
        "S6_chair_flag_replication": compute_S6_chair_flags(args.shapefile),
    }

    # Count flags (None counted as "did not execute" — NOT counted as a flag)
    flag_count = sum(1 for m in metrics.values() if m.get("flag") is True)
    none_count = sum(1 for m in metrics.values() if m.get("flag") is None)
    verdict = "replicated" if flag_count >= STRUCTURAL_REPLICATED_THRESHOLD else "not_replicated"

    result = {
        "candidate_label": label,
        "candidate_shapefile": str(args.shapefile),
        "executed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "drand_round_at_execution": None,
        "metrics": metrics,
        "structural_lane_flags": flag_count,
        "structural_lane_unexecuted": none_count,
        "structural_lane_verdict": verdict,
        "thresholds_pre_committed_at": "preregistration/november_2026_scoring_spec.md",
        "_stub_status": "Stubs in S1, S2, S5, S6 will execute as None until refactor lands.",
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(f"\nStructural battery: {flag_count} flag(s), {none_count} did not execute")
    print(f"Verdict: {verdict}")
    print(f"Wrote {args.output}")

    if none_count > 0:
        print(f"\nWARN: {none_count} metric(s) did not execute (stub state). "
              "Verdict is conditional until refactor lands.", file=sys.stderr)
        return 1   # non-zero so a verdict_synthesis run can flag it
    return 0


if __name__ == "__main__":
    sys.exit(main())
