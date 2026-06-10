# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
verdict_synthesis.py — November 2026 held-out test verdict synthesizer
========================================================================

Companion to preregistration/november_2026_scoring_spec.md §3 (combined verdict
rule). Consumes structural-battery output (run_structural_battery.py) and joint-
outlier output (joint_outlier_score_canonical.py against the candidate map),
applies the pre-committed 2×2 verdict surface, writes the final
lunty_verdict.json.

There is no methodology in this script. Every decision in it is fixed by the
November spec. If a future analyst is tempted to add a "qualitative override"
or "edge-case adjustment" here, the right answer is to amend the November spec
via a dated, signed entry in findings/pre_registration_amendment_log.md — not
to modify this script.

Inputs
------
--structural PATH       Output of run_structural_battery.py.
--joint PATH            Output of joint_outlier_score_canonical.py (when
                        re-run with the candidate map as a substitute for
                        majority/minority; see November spec §7).
--label STRING          Human-readable label echoed into the output.
--output PATH           JSON output path.

Output (one of four pre-committed strings)
------------------------------------------
{
  "candidate_label": "lunty_2026",
  "structural_verdict": "replicated" | "not_replicated",
  "partisan_verdict": "present" | "absent",
  "combined_verdict": "Lunty map replicates the minority-style signature on both lanes"
                    | "Lunty map replicates the structural signature only; partisan-bias lane is neutral"
                    | "Lunty map does not replicate the structural signature; partisan-bias signature present"
                    | "Lunty map breaks from the minority-style signature on both lanes",
  "headline_to_publish": "<full sentence for the 72-hour public update>",
  "publishable_72h": true | false,        # false only if a structural metric did not execute
  "thresholds_pre_committed_at": "preregistration/november_2026_scoring_spec.md"
}

Verdict rules (frozen 2026-06-10)
---------------------------------

Partisan-bias verdict (from joint outlier output): "present" iff ≥ 2 of P1–P4
flag in the UCP direction.

Combined verdict, per the November spec §3:

  structural    partisan       headline
  ----------    --------       --------
  replicated    present        "replicates on both lanes"
  replicated    absent         "replicates structural signature only"
  not_repl.     present        "no structural replication; partisan-bias present"
  not_repl.     absent         "breaks from minority-style on both lanes"
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Partisan thresholds from November spec §3 (frozen 2026-06-10)
P1_EG_THRESHOLD = 0.0410        # 4.10% Alberta-calibrated
P2_MM_PERCENTILE = 0.95
P3_DECL_LOWER = 0.05            # tail flag
P3_DECL_UPPER = 0.95
P4_S50_PERCENTILE = 0.95
PARTISAN_PRESENT_THRESHOLD = 2  # ≥ 2 of P1–P4 fire = "present"

HEADLINES = {
    ("replicated", "present"):
        "Lunty map replicates the minority-style signature on both the structural and partisan-bias lanes.",
    ("replicated", "absent"):
        "Lunty map replicates the minority-style structural signature; partisan-bias lane is neutral.",
    ("not_replicated", "present"):
        "Lunty map does not replicate the minority-style structural signature; "
        "partisan-bias signature is present.",
    ("not_replicated", "absent"):
        "Lunty map breaks from the minority-style signature on both the structural "
        "and partisan-bias lanes.",
}


def partisan_verdict_from_joint(joint: dict) -> tuple[str, dict]:
    """Apply the P1–P4 flag rule to a joint_outlier_score JSON for the candidate map.

    Expected structure (see analysis/scripts/joint_outlier_score_canonical.py):
        joint["maps"]["candidate"]["marginals"]["efficiency_gap"]["observed"]
        joint["maps"]["candidate"]["marginals"]["mean_median"]["marginal_tail_p"]
        ... etc.

    The November spec freezes the candidate map as a third entry alongside the
    May commission's majority and minority.
    """
    try:
        m = joint["maps"]["candidate"]["marginals"]
    except KeyError:
        # Fall back to checking against a "lunty_2026" key
        m = joint["maps"].get("lunty_2026", {}).get("marginals", {})
        if not m:
            return "absent", {"_note": "candidate map not present in joint outlier output."}

    flags = {
        "P1_EG": float(m["efficiency_gap"]["observed"]) >= P1_EG_THRESHOLD,
        "P2_MM": (1.0 - float(m["mean_median"]["marginal_tail_p"])) >= P2_MM_PERCENTILE,
        "P3_DECL": (
            float(m["declination"]["marginal_tail_p"]) <= P3_DECL_LOWER
            or float(m["declination"]["marginal_tail_p"]) >= (1.0 - P3_DECL_LOWER)
        ),
        "P4_S50": (1.0 - float(m["seats_at_50_50"]["marginal_tail_p"])) >= P4_S50_PERCENTILE,
    }
    n_flags = sum(1 for f in flags.values() if f)
    verdict = "present" if n_flags >= PARTISAN_PRESENT_THRESHOLD else "absent"
    return verdict, {"flags": flags, "n_flags": n_flags}


def synthesize(structural: dict, joint: dict) -> dict:
    structural_verdict = structural.get("structural_lane_verdict")
    structural_unexecuted = structural.get("structural_lane_unexecuted", 0)
    partisan_verdict, partisan_detail = partisan_verdict_from_joint(joint)

    key = (structural_verdict, partisan_verdict)
    headline = HEADLINES.get(key, "VERDICT FORMATTING ERROR — combination not in pre-committed table.")

    publishable = (
        structural_verdict in ("replicated", "not_replicated")
        and partisan_verdict in ("present", "absent")
        and structural_unexecuted == 0
    )

    return {
        "candidate_label": structural.get("candidate_label"),
        "structural_verdict": structural_verdict,
        "structural_lane_flags": structural.get("structural_lane_flags"),
        "structural_lane_unexecuted": structural_unexecuted,
        "partisan_verdict": partisan_verdict,
        "partisan_detail": partisan_detail,
        "combined_verdict": key,
        "headline_to_publish": headline,
        "publishable_72h": publishable,
        "thresholds_pre_committed_at": "preregistration/november_2026_scoring_spec.md",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--structural", type=Path, required=True,
                    help="Output of run_structural_battery.py (JSON).")
    ap.add_argument("--joint", type=Path, required=True,
                    help="Output of joint_outlier_score_canonical.py for the candidate map (JSON).")
    ap.add_argument("--output", type=Path,
                    default=ROOT / "findings/verdict_result.json")
    args = ap.parse_args(argv)

    structural = json.loads(args.structural.read_text())
    joint = json.loads(args.joint.read_text())
    verdict = synthesize(structural, joint)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(verdict, indent=2))
    print(f"\nstructural: {verdict['structural_verdict']}  "
          f"({verdict['structural_lane_flags']} flag(s))")
    print(f"partisan:   {verdict['partisan_verdict']}  "
          f"({verdict['partisan_detail'].get('n_flags', '?')} flag(s))")
    print(f"\nHEADLINE: {verdict['headline_to_publish']}")
    if not verdict["publishable_72h"]:
        print("\nNOT PUBLISHABLE: a structural metric did not execute. "
              "Re-run run_structural_battery.py after the stubs land.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
