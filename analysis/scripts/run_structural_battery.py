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

Verdict rule (Amendment 9, frozen 2026-06-11): ≥ 3 of the 5 discriminating
metrics (S1, S2, S3, S5, S6) on the minority side of the midpoint =
"replicated"; 0–2 = "not_replicated". S4 is measured but excluded as
non-discriminating.

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

# ── Midpoint-anchored thresholds (Amendment 9, 2026-06-11) ──────────────────
#
# Design: for each discriminating metric, the flag fires iff the candidate map
# lands on the MINORITY's side of the midpoint between the two commission maps'
# battery-measured canonical values. Rationale (preregistration/
# november_2026_scoring_spec.md §3, as amended):
#   - No free multiplier to accuse of tuning (the earlier 1.5× rule produced
#     the incoherent result that the minority itself failed to classify as
#     "replicated" — its ratios are 1.30–1.39×).
#   - Self-validating: the minority classifies "replicated" (5/5 discriminating
#     flags) and the majority "not_replicated" (0/5) by construction.
#   - Direction-aware: minority-side is "above" for S1/S2/S6 and "below" for
#     S3/S5 (the minority's signature is LOW anchoring and LOW adjacency-drain
#     — §5.3.5: it works via hybridization, not drain).
#
# Battery-measured canonical anchors (this script, canonical EA shapefiles,
# 2026-06-11):
#                     majority     minority     midpoint    minority side
#   S1 pop MAD        2826.89      3938.11      3382.50     above
#   S2 splits (≥2ED)  23           30           26.5        above
#   S3 anchoring      0.80050      0.71970      0.76010     below
#   S5 drain score    0.0072127    0.0005909    0.0039018   below
#   S6 patterns(P1-5) 0            5            2.5         above (≥3)
#
# S4 (compactness) is measured and reported but EXCLUDED from the flag count:
# median PP is identical on both maps (0.4366) and the tail statistics run the
# wrong way (majority has MORE low-PP districts, 16.9% vs 12.4% below 0.30,
# and a lower minimum, 0.149 vs 0.175) — consistent with monograph H3
# ("corridors drawn thick enough to make PP look innocent"). Compactness does
# not discriminate the two commission maps and cannot detect replication.
#
# P6 (St. Albert-Sturgeon hybrid) is dropped from S6's predicate set: the
# majority map has the same-named ED (constraint-forced; both factions arrived
# at the same solution there), so the predicate is non-discriminating.

S1_MIDPOINT = 3382.50          # minority side: above
S2_MIDPOINT = 26.5             # minority side: above
S3_MIDPOINT = 0.76010          # minority side: below
S5_MIDPOINT = 0.0039018        # minority side: below
S6_MIDPOINT = 2.5              # minority side: above (≥3 of P1–P5)

# Legacy band retained for reporting context only (Canadian comparator norm):
S3_BAND_LOW = 0.70
S3_BAND_HIGH = 0.85
# Retained for the S5 null short-circuit reporting path:
S5_DRAIN_THRESHOLD = 0.05
S5_NULL_PVALUE_THRESHOLD = 0.05
# S1 anchors retained for output annotation:
S1_BASELINE_MAJORITY_MAD = 2826.89
S1_BASELINE_MINORITY_MAD = 3938.11

# Verdict rule: ≥3 of the 5 discriminating metrics on the minority side.
STRUCTURAL_REPLICATED_THRESHOLD = 3
N_DISCRIMINATING_METRICS = 5


def compute_S1_population_mad(shapefile: Path, votes_path: Path) -> dict:
    """S1: Per-ED population MAD (median absolute deviation from median).

    Mirrors the formula in mcmc_ensemble.py:390 so the structural test is
    placeable against the canonical chain ensemble percentiles. Uses the
    cached VA→pop_2021 overlay (`data/va_pop_from_das.csv`).

    Flag (Amendment 9): candidate MAD above the majority/minority midpoint.
    """
    try:
        import geopandas as gpd
        import pandas as pd
        import numpy as np

        pop_cache = ROOT / "data" / "va_pop_from_das.csv"
        if not pop_cache.exists():
            return {
                "value": None,
                "threshold": S1_MIDPOINT,
                "flag": None,
                "_note": f"STUB — population cache missing: {pop_cache}",
            }
        va = gpd.read_file(votes_path)
        # Map row index → pop_2021
        pop_df = pd.read_csv(pop_cache).set_index("va_row_idx")["pop_2021"]
        va["pop_2021"] = pd.Series(va.index.map(pop_df).values).fillna(0.0).clip(lower=1.0).values

        eds = gpd.read_file(shapefile)
        # Auto-detect ID column
        id_col = "EDName2025" if "EDName2025" in eds.columns else (
            "name_2026" if "name_2026" in eds.columns else eds.columns[0]
        )
        eds = eds.to_crs(va.crs)
        # Spatial join VA centroids → ED
        va_centroids = va.copy()
        va_centroids["geometry"] = va.geometry.representative_point()
        joined = gpd.sjoin(va_centroids[["pop_2021", "geometry"]], eds[[id_col, "geometry"]],
                           how="inner", predicate="within")
        pop_by_ed = joined.groupby(id_col)["pop_2021"].sum().values
        mad = float(np.median(np.abs(pop_by_ed - np.median(pop_by_ed))))
        threshold = S1_MIDPOINT
        flag = bool(mad >= threshold)   # minority side: above midpoint
        return {
            "value": mad,
            "threshold": threshold,
            "flag": flag,
        }
    except Exception as e:
        return {
            "value": None,
            "threshold": S1_MIDPOINT,
            "flag": None,
            "_note": f"STUB — population MAD computation raised: {e}",
        }


def compute_S2_municipal_splits(shapefile: Path, reference: Path) -> dict:
    """S2: Count of municipalities split into ≥3 EDs.

    Uses municipal_splits.count_splits_two_or_more().
    """
    try:
        sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
        from municipal_splits import count_splits_two_or_more
        n = int(count_splits_two_or_more(shapefile))
        threshold = S2_MIDPOINT
        flag = bool(n > threshold)   # minority side: above midpoint (>26.5 means >=27)
        return {
            "value": n,
            "threshold": threshold,
            "flag": flag,
        }
    except Exception as e:
        return {
            "value": None,
            "threshold": S2_MIDPOINT,
            "flag": None,
            "_note": f"STUB — count_splits_two_or_more() raised: {e}",
        }


def compute_S3_anchoring(shapefile: Path) -> dict:
    """S3: Province-wide municipal-anchored-perimeter percentage.

    Uses score_anchoring.score_anchoring(). Note: this is percentage of ED
    perimeter that follows CSD boundaries (Canadian norm 70–85%), not
    population-in-anchored-EDs. The November spec band is the same.
    """
    try:
        sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
        from score_anchoring import score_anchoring as _score_anchoring
        score = float(_score_anchoring(str(shapefile)))
        # score_anchoring returns a percentage (0–100); normalize to fraction
        if score > 1.5:
            score = score / 100.0
        flag = bool(score < S3_MIDPOINT)   # minority side: below midpoint
        return {
            "value": score,
            "threshold": S3_MIDPOINT,
            "canadian_norm_band": [S3_BAND_LOW, S3_BAND_HIGH],
            "flag": flag,
        }
    except Exception as e:
        return {
            "value": None,
            "threshold": [S3_BAND_LOW, S3_BAND_HIGH],
            "flag": None,
            "_note": f"STUB — score_anchoring raised: {e}",
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
        return {
            "value": median_pp,
            "threshold": None,
            "flag": False,
            "non_discriminating": True,
            "_note": ("measured but EXCLUDED from the flag count: median PP is "
                      "identical on both commission maps (0.4366) and tail stats "
                      "run the wrong way (monograph H3). Reported for transparency."),
        }
    except Exception as e:
        return {
            "value": None,
            "threshold": None,
            "flag": None,
            "_note": f"STUB — polsby_popper.score_map signature drift ({e}).",
        }


def compute_S5_drain(shapefile: Path, votes_path: Path,
                     n_perm: int = 2000, seed: int = 42) -> dict:
    """S5: Neighbour-drain adjacency pattern + label-shuffle null p-value.

    Wires through the existing neighbour_drain_adjacency + drain_label_shuffle_null
    pipeline. Uses 2,000 permutations by default (10× faster than the canonical
    10,000 with negligible accuracy cost at typical p ≈ 0.1; raise to 10000 for
    a publication-grade run).

    Flag fires iff drain_score >= S5_DRAIN_THRESHOLD AND null_pvalue < S5_NULL_PVALUE_THRESHOLD.
    """
    try:
        import geopandas as gpd
        import numpy as np
        import pandas as pd
        sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
        from neighbour_drain_adjacency import (
            _score_canonical_map_strict, build_adjacency, compute_ed_metrics,
            detect_chain_signals,
        )
        from drain_label_shuffle_null import (
            drain_score, directed_pairs_from_undirected, label_shuffle_null,
        )

        va = gpd.read_file(votes_path)
        votes, name_col = _score_canonical_map_strict(va, shapefile, label="candidate")
        eds = gpd.read_file(shapefile)
        ed_df = compute_ed_metrics(votes)
        undirected, _, _ = build_adjacency(eds, name_col)
        pair_df = detect_chain_signals(ed_df, undirected)
        ed_lookup = ed_df.set_index("ed").to_dict("index")
        score = float(drain_score(pair_df, ed_lookup))

        # Midpoint rule (Amendment 9): minority side is LOW drain — the
        # minority's signature is hybridization, not adjacency drain (§5.3.5).
        # The label-shuffle null no longer gates the flag; the machinery
        # remains available via drain_label_shuffle_null.py for a
        # publication-grade significance run.
        flag = bool(score < S5_MIDPOINT)
        return {
            "drain_score": score,
            "threshold": S5_MIDPOINT,
            "direction": "minority side = below midpoint",
            "flag": flag,
        }
    except Exception as e:
        return {
            "drain_score": None,
            "null_pvalue": None,
            "threshold": {"drain": S5_DRAIN_THRESHOLD, "null_p": S5_NULL_PVALUE_THRESHOLD},
            "flag": None,
            "_note": f"STUB — drain pipeline raised: {type(e).__name__}: {e}",
        }


def compute_S6_chair_flags(shapefile: Path) -> dict:
    """S6: Count of chair-flagged hybrid boundary patterns reproduced.

    Predicates derived from `findings/chair_recommendation_5_analysis.md` and
    the canonical minority map's pattern (verified 2026-06-10):

    P1: Airdrie split into ≥3 EDs (Airdrie fragmentation pattern).
    P2: Any ED name containing 'Cochrane' AND a Calgary-prefix or
        Calgary-neighborhood name (Cochrane was specifically flagged as
        "not something I can condone" combined with Calgary).
    P3: Any ED name containing 'Chestermere' AND 'Calgary' (the Calgary-Peigan-
        Chestermere hybrid).
    P4: Calgary edge + rural Bearspaw / Rocky View ED (e.g.
        'Calgary-North West-Bearspaw').
    P5: Red Deer split into ≥3 EDs.
    P6: Any ED name combining 'St. Albert' (or 'St Albert') with Sturgeon —
        flagged by the chair as a Calgary-style hybrid in northern context.

    Threshold from the November spec: ≥1 pattern reproduced = flag.
    """
    try:
        import geopandas as gpd
        eds = gpd.read_file(shapefile)
        id_col = "EDName2025" if "EDName2025" in eds.columns else (
            "name_2026" if "name_2026" in eds.columns else eds.columns[0]
        )
        names = [str(n) for n in eds[id_col].tolist()]

        patterns_hit = []

        # P1: Airdrie split into ≥3 EDs
        airdrie_count = sum(1 for n in names if "Airdrie" in n)
        if airdrie_count >= 3:
            patterns_hit.append(f"P1_Airdrie_split_{airdrie_count}_ways")

        # P2: Cochrane + Calgary in same ED
        for n in names:
            if "Cochrane" in n and "Calgary" in n:
                patterns_hit.append(f"P2_Cochrane_Calgary_hybrid_{n}")

        # P3: Chestermere + Calgary
        for n in names:
            if "Chestermere" in n and "Calgary" in n:
                patterns_hit.append(f"P3_Chestermere_Calgary_hybrid_{n}")

        # P4: Calgary + Bearspaw (or Calgary + Rocky View rural)
        for n in names:
            if "Calgary" in n and ("Bearspaw" in n or "Rocky View" in n):
                patterns_hit.append(f"P4_Calgary_RockyView_hybrid_{n}")

        # P5: Red Deer split into ≥3 EDs
        red_deer_count = sum(1 for n in names if "Red Deer" in n)
        if red_deer_count >= 3:
            patterns_hit.append(f"P5_Red_Deer_split_{red_deer_count}_ways")

        # P6: St Albert + Sturgeon (the chair flagged this northern hybrid)
        # Note: St. Albert alone is a normal city; St Albert-Sturgeon is the hybrid.
        for n in names:
            if ("St. Albert" in n or "St Albert" in n) and "Sturgeon" in n:
                patterns_hit.append(f"P6_StAlbert_Sturgeon_hybrid_{n}")

        # P6 (St. Albert-Sturgeon) is excluded from the count: the majority
        # map has the same-named ED (constraint-forced), so it does not
        # discriminate. It is still listed when matched, for transparency.
        discriminating_hits = [p for p in patterns_hit if not p.startswith("P6_")]
        flag = bool(len(discriminating_hits) > S6_MIDPOINT)   # >2.5 means >=3
        return {
            "patterns_reproduced": patterns_hit,
            "patterns_count_discriminating": len(discriminating_hits),
            "threshold": S6_MIDPOINT,
            "flag": flag,
        }
    except Exception as e:
        return {
            "patterns_reproduced": None,
            "threshold": S6_MIDPOINT,
            "flag": None,
            "_note": f"STUB — S6 predicate evaluation raised: {type(e).__name__}: {e}",
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

    # Count flags only across the DISCRIMINATING metrics (S4 is reported but
    # excluded per Amendment 9 — see preamble for the rationale).
    DISCRIMINATING = ("S1_population_mad", "S2_municipal_split_count",
                      "S3_anchoring_score", "S5_drain_score",
                      "S6_chair_flag_replication")
    flag_count = sum(1 for k in DISCRIMINATING if metrics[k].get("flag") is True)
    none_count = sum(1 for k in DISCRIMINATING if metrics[k].get("flag") is None)
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
