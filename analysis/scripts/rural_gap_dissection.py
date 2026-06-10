# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
rural_gap_dissection.py — Rural-mean population gap dissection
================================================================

Companion to findings/rural_gap_findings.md. Forensic drill-down on the
summary line:
  "Minority rest-of-province mean is 3.9% below majority's (50,336 vs 52,281)."

Question
--------
Is a candidate map's rural-ED mean population concentrated in EDs leaning
toward one party (a "pack-rural-to-overrepresent" signal), or spread across
the partisan spectrum?

Inputs
------
--map PATH              Candidate map shapefile (.gpkg or .shp). Default:
                        canonical minority shapefile.
--populations PATH      Per-ED population CSV (columns: ED_NAME, pop_2021).
                        Default: data/majority_2026_populations.csv for the
                        majority, data/minority_2026_populations.csv for the
                        minority. For a Lunty / third-party map, pass an
                        explicit CSV produced by the population overlay step.
--votes PATH            Per-ED two-party votes CSV (columns: ED_NAME, ucp,
                        ndp). Default: data/outputs/phase4c_per_ed_votes_*.csv
                        (matches the --map argument).
--reference PATH        Reference map (default canonical majority) — for
                        computing the rural-mean gap.
--output PATH           JSON output path.
--label STRING          Map label for the output.

Output
------
JSON shape:

{
  "map_label": "...",
  "n_rural_eds_candidate": int,
  "n_rural_eds_reference": int,
  "candidate_rural_mean_pop": float,
  "reference_rural_mean_pop": float,
  "rural_gap_pct": float,                       # (cand-ref)/ref * 100
  "candidate_partisan_breakdown": {
    "ucp_leaning": {"n": int, "mean_pop": float, "mean_two_party_ucp_share": float},
    "ndp_leaning": {"n": int, "mean_pop": float, "mean_two_party_ucp_share": float},
    "swing":      {"n": int, "mean_pop": float, "mean_two_party_ucp_share": float}
  },
  "signal_classification": "pack_rural_ucp" | "pack_rural_ndp" | "no_partisan_signal",
  "_method_note": "..."
}

Classification rule (frozen 2026-06-10 for November):
  - "pack_rural_ucp": rural mean in UCP-leaning EDs is ≥ 1.5 pp below the
    overall rural mean AND in NDP-leaning EDs is ≥ 0 pp above.
  - "pack_rural_ndp": mirror image.
  - "no_partisan_signal": otherwise.

Reproduction
------------
  # Canonical majority vs minority
  python analysis/scripts/rural_gap_dissection.py \\
    --map data/shapefiles/canonical/ea_minority_2026_eds.gpkg \\
    --populations data/minority_2026_populations.csv \\
    --votes data/outputs/phase4c_per_ed_votes_minority.csv \\
    --label canonical_minority \\
    --output findings/rural_gap_canonical_minority.json

  # November Lunty test
  python analysis/scripts/rural_gap_dissection.py \\
    --map data/shapefiles/lunty/lunty_2026_eds.gpkg \\
    --populations data/outputs/lunty_per_ed_populations.csv \\
    --votes data/outputs/lunty_per_ed_votes.csv \\
    --label lunty_2026 \\
    --output findings/rural_gap_lunty.json

Backward:
  findings/rural_gap_findings.md           (methodology and historical numbers)
  data/{majority,minority}_2026_populations.csv
  data/outputs/phase4c_per_ed_votes_*.csv
  data/shapefiles/canonical/

Forward:
  findings/rural_gap_<label>.json
  reports/academic/report_academic.md §5.1.3 (urban-rural breakdown)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent


# ----- Pre-committed thresholds (frozen 2026-06-10) -----
UCP_SHARE_UPPER_FOR_UCP_LEAN = 0.55     # > 55% UCP two-party share = UCP-leaning
UCP_SHARE_LOWER_FOR_NDP_LEAN = 0.45     # < 45% = NDP-leaning; 45–55 = swing
PACK_RURAL_PP_THRESHOLD = 1.5           # rural mean ≥ 1.5pp below overall rural mean = pack signal

URBAN_ED_KEYWORDS = ("Calgary", "Edmonton")   # any ED whose name starts with these = urban


def is_rural(ed_name: str) -> bool:
    """Heuristic: rural = NOT Calgary/Edmonton-prefixed. Cochrane, Airdrie, etc. are 'rural-edge'.

    For November the candidate map's classification should match its declared
    rural/urban tagging if one is provided. This heuristic falls back to the
    same rule used in findings/rural_gap_findings.md §1.
    """
    return not any(ed_name.startswith(k) for k in URBAN_ED_KEYWORDS)


def lean_class(ucp_two_party: float) -> str:
    if ucp_two_party >= UCP_SHARE_UPPER_FOR_UCP_LEAN:
        return "ucp_leaning"
    if ucp_two_party <= UCP_SHARE_LOWER_FOR_NDP_LEAN:
        return "ndp_leaning"
    return "swing"


def classify_signal(breakdown: dict, overall_rural_mean: float) -> str:
    ucp_mean = breakdown["ucp_leaning"]["mean_pop"]
    ndp_mean = breakdown["ndp_leaning"]["mean_pop"]
    if ucp_mean and overall_rural_mean and (overall_rural_mean - ucp_mean) >= PACK_RURAL_PP_THRESHOLD * overall_rural_mean / 100:
        if ndp_mean and ndp_mean >= overall_rural_mean:
            return "pack_rural_ucp"
    if ndp_mean and overall_rural_mean and (overall_rural_mean - ndp_mean) >= PACK_RURAL_PP_THRESHOLD * overall_rural_mean / 100:
        if ucp_mean and ucp_mean >= overall_rural_mean:
            return "pack_rural_ndp"
    return "no_partisan_signal"


def dissect(populations_csv: Path, votes_csv: Path) -> dict:
    pop = pd.read_csv(populations_csv)
    votes = pd.read_csv(votes_csv)

    # Normalize column names
    pop_cols = {c.lower(): c for c in pop.columns}
    name_col = pop_cols.get("ed_name") or pop_cols.get("edname2025") or pop_cols.get("ed")
    pop_col = pop_cols.get("pop_2021") or pop_cols.get("pop") or pop_cols.get("population")
    if not name_col or not pop_col:
        raise ValueError(f"populations CSV missing ED_NAME / pop_2021 columns: {list(pop.columns)}")
    pop = pop.rename(columns={name_col: "ED_NAME", pop_col: "pop_2021"})

    vote_cols = {c.lower(): c for c in votes.columns}
    name_col_v = vote_cols.get("ed_name") or vote_cols.get("edname2025") or vote_cols.get("ed")
    ucp_col = vote_cols.get("ucp") or vote_cols.get("ucp_votes")
    ndp_col = vote_cols.get("ndp") or vote_cols.get("ndp_votes")
    votes = votes.rename(columns={name_col_v: "ED_NAME", ucp_col: "ucp", ndp_col: "ndp"})

    df = pop.merge(votes[["ED_NAME", "ucp", "ndp"]], on="ED_NAME", how="left")
    df["two_party"] = df["ucp"] + df["ndp"]
    df["ucp_two_party"] = df["ucp"] / df["two_party"].where(df["two_party"] > 0)
    df["is_rural"] = df["ED_NAME"].apply(is_rural)
    df["lean"] = df["ucp_two_party"].apply(lambda x: lean_class(x) if pd.notna(x) else "unknown")

    rural = df[df["is_rural"]].copy()
    overall_rural_mean = float(rural["pop_2021"].mean()) if len(rural) else float("nan")

    breakdown = {}
    for lean in ("ucp_leaning", "ndp_leaning", "swing"):
        sub = rural[rural["lean"] == lean]
        breakdown[lean] = {
            "n": int(len(sub)),
            "mean_pop": float(sub["pop_2021"].mean()) if len(sub) else None,
            "mean_two_party_ucp_share": float(sub["ucp_two_party"].mean()) if len(sub) else None,
        }

    signal = classify_signal(breakdown, overall_rural_mean)

    return {
        "n_rural_eds": int(len(rural)),
        "rural_mean_pop": overall_rural_mean,
        "candidate_partisan_breakdown": breakdown,
        "signal_classification": signal,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--map", type=Path,
                    default=ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg",
                    help="Candidate map shapefile (used only for label/provenance).")
    ap.add_argument("--populations", type=Path, required=True,
                    help="Per-ED population CSV (ED_NAME, pop_2021).")
    ap.add_argument("--votes", type=Path, required=True,
                    help="Per-ED two-party votes CSV (ED_NAME, ucp, ndp).")
    ap.add_argument("--reference", type=Path,
                    default=ROOT / "data/majority_2026_populations.csv",
                    help="Reference population CSV (for gap computation).")
    ap.add_argument("--reference-votes", type=Path,
                    default=ROOT / "data/outputs/phase4c_per_ed_votes_majority.csv")
    ap.add_argument("--output", type=Path,
                    default=ROOT / "findings/rural_gap_dissection_result.json")
    ap.add_argument("--label", type=str, default=None)
    args = ap.parse_args(argv)

    label = args.label or args.map.stem
    print(f"[rural-gap dissection] map={label}")

    candidate = dissect(args.populations, args.votes)
    if args.reference.exists() and args.reference_votes.exists():
        reference = dissect(args.reference, args.reference_votes)
        rural_gap_pct = (
            100.0 * (candidate["rural_mean_pop"] - reference["rural_mean_pop"])
            / reference["rural_mean_pop"]
        )
    else:
        reference = None
        rural_gap_pct = None

    result = {
        "map_label": label,
        "n_rural_eds_candidate": candidate["n_rural_eds"],
        "n_rural_eds_reference": reference["n_rural_eds"] if reference else None,
        "candidate_rural_mean_pop": candidate["rural_mean_pop"],
        "reference_rural_mean_pop": reference["rural_mean_pop"] if reference else None,
        "rural_gap_pct": rural_gap_pct,
        "candidate_partisan_breakdown": candidate["candidate_partisan_breakdown"],
        "signal_classification": candidate["signal_classification"],
        "_method_note": (
            "Rural is heuristic (non-Calgary/Edmonton-prefixed ED names). "
            "UCP-leaning: two-party UCP share > 55%; NDP-leaning: < 45%; swing: 45–55%. "
            "Pack signal: lean-class mean ≥ 1.5pp below overall rural mean AND opposite "
            "lean ≥ overall mean. Thresholds frozen 2026-06-10 in this script."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(f"  candidate rural mean: {candidate['rural_mean_pop']:.0f}  (n={candidate['n_rural_eds']})")
    if reference:
        print(f"  reference rural mean: {reference['rural_mean_pop']:.0f}  (n={reference['n_rural_eds']})")
        print(f"  rural gap: {rural_gap_pct:+.2f}%")
    print(f"  signal classification: {candidate['signal_classification']}")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
