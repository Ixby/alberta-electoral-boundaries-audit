# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
local_perturbation_chain.py — Issue #13 local-perturbation null
=================================================================

Named retractor for retraction condition 2.3A in
preregistration/retraction_conditions.md:

  "If a local-perturbation null (single-VA swaps only, contiguity preserved)
  shows the audit's Lane-1 outlier flags fire for ≥ 5% of perturbed minority
  variants, the headline Lane-1 result is retracted."

The full canonical 1.01M ReCom ensemble is the headline null. The local-
perturbation chain is a *complementary* null at the opposite end of the
neutrality spectrum: minimal, structure-preserving variations of the real
minority map that test whether the metric outliers are robust to "tiny
unintended differences" rather than to wholesale neutral redrawing. If the
flags fire for many neighborhoods of the real map, that suggests the outlier
status is fragile.

Construction
------------
1. Start from the canonical minority map (89 EDs).
2. For each VA at an ED boundary, propose moving it to the neighboring ED.
3. Reject the proposal if it violates contiguity OR pushes either ED outside
   the ±25% population deviation envelope.
4. Accept N = 10,000 accepted single-VA swaps as the chain.
5. Score every accepted variant on the four partisan-bias metrics + Mahalanobis
   joint distance vs the canonical 1.01M ensemble distribution.

Inputs
------
--shapefile PATH      Start shapefile (default: canonical minority).
--votes PATH          VA-level vote shapefile (default: canonical).
--n-perturbations N   Number of accepted single-VA swaps (default: 10,000).
--pop-tolerance F     Per-ED population deviation envelope (default: 0.25).
--ensemble PATH       Canonical ensemble for percentile placement.
--seed N              drand-pinned base seed (REQUIRED for retraction-grade run).
--output PATH         JSON output path.

Output
------
JSON with:
  {
    "n_perturbations_accepted": int,
    "n_perturbations_attempted": int,
    "acceptance_rate": float,
    "perturbation_metric_distribution": {EG: [...], MM: [...], decl: [...], s50: [...]},
    "fraction_perturbations_with_at_least_one_flag_at_p95": float,
    "retraction_condition_2_3_a_fired": bool,    # True iff fraction >= 0.05
    "real_map_metrics": {...},
    "seed": int,
  }

Retraction rule (frozen):
  retraction_condition_2_3_a_fired = (
    fraction_perturbations_with_at_least_one_flag_at_p95 >= 0.05
  )

If True, the audit retracts the Lane-1 headline per
preregistration/retraction_conditions.md §2.3.

Status: STUB
------------
Wire-in points marked with TODO(issue-13). The framework is fixed by the
issue spec; the implementation reuses:
  - analysis/scripts/mcmc_ensemble.py::build_va_graph (start state)
  - analysis/scripts/mcmc_ensemble.py::score_partition (metric computation)
  - data/simulation_checkpoints_canonical/chain*_samples.csv (percentile placement)

The single-VA swap proposal kernel is novel to this test; see the
"single_va_swap" function below for the spec.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))


# ----- Retraction threshold (frozen 2026-06-10) -----
RETRACTION_FRACTION_THRESHOLD = 0.05
P95_TAIL_THRESHOLD = 0.95
DEFAULT_N_PERTURBATIONS = 10_000
DEFAULT_POP_TOLERANCE = 0.25


def single_va_swap(graph, partition, rng):
    """One step of the local-perturbation chain.

    Proposal:
      1. Choose a random VA at an ED boundary uniformly.
      2. Choose one of its neighboring EDs uniformly.
      3. Propose moving the VA to that ED.

    Acceptance:
      - Reject if moving breaks contiguity of the source ED (the donating ED).
      - Reject if the destination ED's population would exceed ideal × (1 + tol).
      - Reject if the source ED's population would drop below ideal × (1 - tol).
      - Accept otherwise.

    Returns: (accepted, new_partition).
    """
    # TODO(issue-13): implement against gerrychain.GeographicPartition.
    raise NotImplementedError("Issue #13 perturbation kernel not yet implemented.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--shapefile", type=Path,
                    default=ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg")
    ap.add_argument("--votes", type=Path,
                    default=ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg")
    ap.add_argument("--n-perturbations", type=int, default=DEFAULT_N_PERTURBATIONS)
    ap.add_argument("--pop-tolerance", type=float, default=DEFAULT_POP_TOLERANCE)
    ap.add_argument("--ensemble", type=Path,
                    default=ROOT / "data/simulation_checkpoints_canonical")
    ap.add_argument("--seed", type=int, required=False,
                    help="drand-pinned base seed (REQUIRED for retraction-grade run).")
    ap.add_argument("--output", type=Path,
                    default=ROOT / "findings/local_perturbation_chain.json")
    args = ap.parse_args(argv)

    if args.seed is None:
        print(
            "WARN: --seed not provided. Retraction-grade runs require a drand-pinned seed "
            "filed in preregistration/seed_commitments.md. Proceeding in dev mode.",
            file=sys.stderr,
        )

    print(f"[local-perturbation chain] STUB — Issue #13 implementation pending.")
    print(f"  start shapefile: {args.shapefile.name}")
    print(f"  n_perturbations: {args.n_perturbations}")
    print(f"  pop_tolerance:   ±{args.pop_tolerance*100:.0f}%")
    print(f"  seed:            {args.seed}")

    result = {
        "_status": "STUB — Issue #13 implementation pending",
        "_blocker": "single_va_swap() not implemented; see issue tracker.",
        "shapefile": str(args.shapefile),
        "n_perturbations_target": args.n_perturbations,
        "pop_tolerance": args.pop_tolerance,
        "seed": args.seed,
        "retraction_condition_2_3_a_fired": None,
        "_retraction_rule_frozen": (
            "Lane-1 headline is retracted if "
            f">= {RETRACTION_FRACTION_THRESHOLD*100:.0f}% of accepted perturbations "
            f"produce >= 1 metric flag at p>={P95_TAIL_THRESHOLD*100:.0f} against the "
            f"canonical 1,010,000-plan ReCom ensemble."
        ),
        "executed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(f"\nWrote stub output to {args.output}")
    print("\nNext steps:")
    print("  1. Implement single_va_swap() per Issue #13 spec.")
    print("  2. Implement the perturbation loop using gerrychain.GeographicPartition.")
    print("  3. Score each accepted variant against the canonical 1.01M ensemble percentiles.")
    print("  4. drand-pin a seed and file in preregistration/seed_commitments.md before the run.")
    return 1   # non-zero because this is a stub


if __name__ == "__main__":
    sys.exit(main())
