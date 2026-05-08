"""Chen-Rodden geography-vs-drawing decomposition for Alberta's 2019 / 2026
maps against the 100,000-plan MCMC neutral ensemble.

T3.2 of the remediation track. Gemini Phase E.3 flagged the audit's headline
partisan-bias asymmetry between the minority and majority 2026 maps
(central-weight −1.42 pp at w=0.85 under the blended crosswalk;
+4.15 pp under the high-resolution spatial reading) as requiring a
geography-vs-drawing decomposition in the Chen-Rodden (2013) frame.

Decomposition logic
-------------------
For a metric M and a real map R:
    M(R) = M_geography + M_drawing
where
    M_geography = ensemble_median(M)
    M_drawing   = M(R) − ensemble_median(M)

The geography component captures what any "neutral" drawing of Alberta
would produce under the ensemble's substrate (2023 election-day votes, 87
ReCom-reachable districts seeded at the 2019 enacted plan, ±25% population
band). The drawing component captures how far the real map departs from
that neutral centre.

For a pairwise gap between maps A and B:
    Δ_M(A,B)   = M(A) − M(B)
              = (M_geography_A − M_geography_B) + (M_drawing_A − M_drawing_B)
              = 0 + (M_drawing_A − M_drawing_B)
when A and B share the same ensemble (same province, same voter geography,
same ensemble substrate). So for the minority-vs-majority gap, the
decomposition reduces to: 100% drawing, 0% geography by construction.

When A and B do NOT share the same ensemble (e.g., 2019 on 87 districts vs
2026 on 89 districts; same province but different substrate), the
geography component is the difference in ensemble medians across the two
substrates. For this audit, a 89-district ensemble is not available, so
the 2019 (87) → 2026 (89) comparison is made at the 87-ensemble and the
substrate-shift is flagged as a residual that the decomposition cannot
resolve.

Sign conventions
----------------
The 100k ensemble samples CSV uses the script-native convention:
  positive EG = NDP wastes more than UCP (ensemble's "UCP-favoured" label
  per §5.4 line 540).

The paper (§4.3) uses the reader-facing convention:
  "negative EG = UCP advantage", reconciled with S-M literature in
  `analysis/methodology/sign_convention_resolution.md`.

For THIS decomposition, we use the ensemble-native convention throughout
because that is the substrate the decomposition lives on. All numbers
are reported in ensemble convention; a reader-facing line is added at
the end showing the sign-flipped paper convention for EG.

Inputs
------
- data/simulated_ensemble_raw_samples_100k.csv (100,000 ensemble samples)
- data/simulation_real_map_scores_full_v2.json (session-12 canonical + full-VA
  rescore; PRIMARY per task spec, but the ensemble substrate is
  election-day-only so strictly speaking the decomposition is
  cross-substrate for this input)
- data/simulation_real_map_scores_full_100k.json (pre-remediation
  election-day-only rescore; SUBSTRATE-MATCHED to the ensemble and used as
  cross-check)

Outputs
-------
- analysis/reports/chen_rodden_decomposition.md (writeup)
- data/chen_rodden_decomposition.csv (decomposition table,
  machine-readable)
- data/chen_rodden_decomposition.json (structured summary)

Forward: analysis/reports/chen_rodden_decomposition.md
Backward:
  data/simulated_ensemble_raw_samples_100k.csv
  data/simulation_real_map_scores_full_v2.json
  data/simulation_real_map_scores_full_100k.json
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")

ENSEMBLE_CSV = DATA / "simulated_ensemble_raw_samples_100k.csv"
SCORES_V2 = DATA / "simulation_real_map_scores_full_v2.json"
SCORES_FULL100K = DATA / "simulation_real_map_scores_full_100k.json"

OUT_CSV = DATA / "chen_rodden_decomposition.csv"
OUT_JSON = DATA / "chen_rodden_decomposition.json"

METRICS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
METRIC_LABELS = {
    "efficiency_gap": "Efficiency gap",
    "mean_median": "Mean-median",
    "declination": "Declination",
    "seats_at_50_50": "Seats at 50/50",
}


def ensemble_summary(df: pd.DataFrame) -> dict:
    """Ensemble distribution statistics per metric, ensemble-native sign."""
    out = {}
    for m in METRICS:
        x = df[m].dropna()
        out[m] = {
            "mean": float(x.mean()),
            "median": float(x.median()),
            "std": float(x.std()),
            "p05": float(x.quantile(0.05)),
            "p50": float(x.quantile(0.50)),
            "p95": float(x.quantile(0.95)),
            "n": int(len(x)),
        }
    return out


def decompose_real_map(scores: dict, ens: dict) -> dict:
    """Geography + drawing decomposition for one real map."""
    out = {}
    for m in METRICS:
        real_val = scores[m]
        geography = ens[m]["median"]
        drawing = real_val - geography
        out[m] = {
            "real": real_val,
            "geography": geography,
            "drawing": drawing,
            "real_reconstructed": geography + drawing,
        }
    return out


def decompose_gap(decomp_a: dict, decomp_b: dict) -> dict:
    """Decomposition of the gap (A - B) into geography and drawing shares.

    When A and B share the same ensemble, the geography component is 0
    by construction and the drawing component equals the full gap.
    """
    out = {}
    for m in METRICS:
        real_gap = decomp_a[m]["real"] - decomp_b[m]["real"]
        geography_gap = decomp_a[m]["geography"] - decomp_b[m]["geography"]
        drawing_gap = decomp_a[m]["drawing"] - decomp_b[m]["drawing"]
        pct_drawing = (
            100.0 if abs(real_gap) < 1e-12 else (100.0 * drawing_gap / real_gap)
        )
        out[m] = {
            "real_gap": real_gap,
            "geography_gap": geography_gap,
            "drawing_gap": drawing_gap,
            "pct_drawing": pct_drawing,
        }
    return out


def fmt_pct(x: float, digits: int = 2) -> str:
    return f"{x*100:+.{digits}f}%"


def fmt_plain(x: float, digits: int = 4) -> str:
    return f"{x:+.{digits}f}"


def main():
    print("=== Chen-Rodden geography-vs-drawing decomposition (T3.2) ===\n")

    # --- Ensemble ---
    ens_df = pd.read_csv(ENSEMBLE_CSV)
    ens = ensemble_summary(ens_df)
    print(
        f"Ensemble: {len(ens_df)} samples, n_districts={sorted(ens_df.n_districts.unique())}, "
        f"UCP vote share={ens_df.ucp_vote_share.iloc[0]:.4f}"
    )
    for m, s in ens.items():
        print(
            f"  {m:16s}  p05/p50/p95 = {s['p05']:+.4f} / {s['p50']:+.4f} / {s['p95']:+.4f}  "
            f"(mean {s['mean']:+.4f}, std {s['std']:.4f})"
        )

    # --- Real maps: v2 (PRIMARY per task spec; substrate = full VA + splat) ---
    scores_v2 = json.loads(SCORES_V2.read_text())
    print("\n--- Real map scores (session-12 canonical + full-VA, v2) ---")
    for label, s in scores_v2.items():
        print(f"  {label}")
        for m in METRICS:
            print(f"    {m:16s} = {s[m]:+.4f}")

    # --- Real maps: full_100k (substrate-matched to ensemble; election-day only) ---
    scores_ed = json.loads(SCORES_FULL100K.read_text())
    print(
        "\n--- Real map scores (election-day-only, substrate-matched to ensemble) ---"
    )
    for label, s in scores_ed.items():
        print(f"  {label}")
        for m in METRICS:
            print(f"    {m:16s} = {s[m]:+.4f}")

    # --- Decomposition under PRIMARY (v2) substrate ---
    # Remap keys to consistent labels
    v2_keys = {
        "2019 enacted (full)": "2019",
        "majority 2026 (canonical, full-VA)": "majority",
        "minority 2026 (canonical, full-VA)": "minority",
    }
    ed_keys = {
        "2019 enacted (full)": "2019",
        "majority 2026 (full coverage)": "majority",
        "minority 2026 v6 (full coverage)": "minority",
    }

    decomp_v2 = {v2_keys[k]: decompose_real_map(v, ens) for k, v in scores_v2.items()}
    decomp_ed = {ed_keys[k]: decompose_real_map(v, ens) for k, v in scores_ed.items()}

    # Gaps
    gaps_v2 = {
        "2019_to_majority": decompose_gap(decomp_v2["majority"], decomp_v2["2019"]),
        "2019_to_minority": decompose_gap(decomp_v2["minority"], decomp_v2["2019"]),
        "majority_to_minority": decompose_gap(
            decomp_v2["minority"], decomp_v2["majority"]
        ),
    }
    gaps_ed = {
        "2019_to_majority": decompose_gap(decomp_ed["majority"], decomp_ed["2019"]),
        "2019_to_minority": decompose_gap(decomp_ed["minority"], decomp_ed["2019"]),
        "majority_to_minority": decompose_gap(
            decomp_ed["minority"], decomp_ed["majority"]
        ),
    }

    # --- Decomposition table (machine-readable CSV) ---
    rows = []
    for substrate_label, decomp, gaps in [
        ("v2_full_va_splat", decomp_v2, gaps_v2),
        ("election_day_only", decomp_ed, gaps_ed),
    ]:
        for map_label in ["2019", "majority", "minority"]:
            for m in METRICS:
                d = decomp[map_label][m]
                rows.append(
                    {
                        "substrate": substrate_label,
                        "kind": "map",
                        "target": map_label,
                        "metric": m,
                        "real": d["real"],
                        "geography": d["geography"],
                        "drawing": d["drawing"],
                        "real_gap": None,
                        "geography_gap": None,
                        "drawing_gap": None,
                        "pct_drawing": None,
                    }
                )
        for gap_label, gap in gaps.items():
            for m in METRICS:
                g = gap[m]
                rows.append(
                    {
                        "substrate": substrate_label,
                        "kind": "gap",
                        "target": gap_label,
                        "metric": m,
                        "real": None,
                        "geography": None,
                        "drawing": None,
                        "real_gap": g["real_gap"],
                        "geography_gap": g["geography_gap"],
                        "drawing_gap": g["drawing_gap"],
                        "pct_drawing": g["pct_drawing"],
                    }
                )
    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)
    print(f"\nWrote: {OUT_CSV.name} ({len(rows)} rows)")

    # --- JSON summary ---
    summary = {
        "ensemble": ens,
        "substrate_v2_full_va": {
            "per_map": decomp_v2,
            "gaps": gaps_v2,
            "note": (
                "Session-12 canonical polygons + full-VA (Election-Day + Vote-Anywhere "
                "splat) substrate. Ensemble is on Election-Day-only substrate; this "
                "decomposition is therefore CROSS-SUBSTRATE and the geography baseline "
                "is imperfect. Reported per task spec; see ed-only cross-check."
            ),
        },
        "substrate_election_day": {
            "per_map": decomp_ed,
            "gaps": gaps_ed,
            "note": (
                "Pre-remediation Election-Day-only VA substrate. SUBSTRATE-MATCHED to "
                "ensemble; decomposition is apples-to-apples here. Cross-check for the "
                "v2 primary."
            ),
        },
        "paper_sign_note": (
            "All values use the ensemble-native convention (positive EG = NDP wastes "
            "more than UCP, which §5.4 labels 'UCP-favoured'). The paper (§4.3) "
            "reader-facing convention flips EG sign (negative = UCP advantage in "
            "seat-outcome terms); the sign-flip affects labelling only. Ordinal "
            "rankings and decomposition proportions are invariant."
        ),
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2, default=float))
    print(f"Wrote: {OUT_JSON.name}")

    # --- Print summary to console ---
    print("\n" + "=" * 70)
    print("DECOMPOSITION TABLE - v2 (session-12 canonical, full-VA + splat) - PRIMARY")
    print("=" * 70)
    print(
        f"\n{'Map':12s} {'Metric':16s} {'Real':>9s} {'Geography':>11s} {'Drawing':>9s}"
    )
    for map_label in ["2019", "majority", "minority"]:
        for m in METRICS:
            d = decomp_v2[map_label][m]
            print(
                f"{map_label:12s} {m:16s} {d['real']:+.4f}  {d['geography']:+.4f}    "
                f"{d['drawing']:+.4f}"
            )

    print(
        f"\n{'Gap':25s} {'Metric':16s} {'d Real':>9s} {'d Geo':>9s} {'d Draw':>9s} {'% Drawing':>11s}"
    )
    for gap_label in ["2019_to_majority", "2019_to_minority", "majority_to_minority"]:
        for m in METRICS:
            g = gaps_v2[gap_label][m]
            print(
                f"{gap_label:25s} {m:16s} {g['real_gap']:+.4f}  {g['geography_gap']:+.4f}  "
                f"{g['drawing_gap']:+.4f}   {g['pct_drawing']:+.1f}%"
            )

    print("\n" + "=" * 70)
    print("DECOMPOSITION TABLE - election-day-only (substrate-matched) - CROSS-CHECK")
    print("=" * 70)
    print(
        f"\n{'Map':12s} {'Metric':16s} {'Real':>9s} {'Geography':>11s} {'Drawing':>9s}"
    )
    for map_label in ["2019", "majority", "minority"]:
        for m in METRICS:
            d = decomp_ed[map_label][m]
            print(
                f"{map_label:12s} {m:16s} {d['real']:+.4f}  {d['geography']:+.4f}    "
                f"{d['drawing']:+.4f}"
            )

    print(
        f"\n{'Gap':25s} {'Metric':16s} {'d Real':>9s} {'d Geo':>9s} {'d Draw':>9s} {'% Drawing':>11s}"
    )
    for gap_label in ["2019_to_majority", "2019_to_minority", "majority_to_minority"]:
        for m in METRICS:
            g = gaps_ed[gap_label][m]
            print(
                f"{gap_label:25s} {m:16s} {g['real_gap']:+.4f}  {g['geography_gap']:+.4f}  "
                f"{g['drawing_gap']:+.4f}   {g['pct_drawing']:+.1f}%"
            )


if __name__ == "__main__":
    main()
