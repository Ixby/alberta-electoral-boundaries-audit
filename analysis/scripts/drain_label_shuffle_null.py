"""drain_label_shuffle_null.py — Continuous drain_score + 10,000 label-shuffle null.

Pre-registered in AsPredicted #289451 (Neighbour-Drain: A Local Pack-Crack
Adjacency Metric).

Continuous intensity formula:
  intensity(X, Y) = max(0, s_X - 0.15) * max(0, 0.05 - m_Y)

drain_score per map = sum over all coupled directed adjacent pairs (X, Y)
  where coupled means losing_party(X) == losing_party(Y).

Null distribution: 10,000 label-shuffle permutations — vote vectors
(ndp, ucp) are randomly reassigned across EDs; adjacency graph is fixed.

Seed: drand round 5500000, salt='drain-label-shuffle'
(any reviewer can verify via https://drand.cloudflare.com/public/5500000)

Pre-registered predictions (AsPredicted #289451):
  A: drain_score(majority) > drain_score(minority)
  B: both maps within null distribution (p > 0.05 two-tailed)
  C: qualitative — after specificity weighting, NW Calgary cluster
     downweighted vs Strathcona cluster (exploratory, Phase E)

Forward deps: analysis/reports/drain_label_shuffle_null.md
Backward deps:
  - analysis/scripts/neighbour_drain_adjacency.py (adjacency + vote loading)
  - analysis/scripts/drand_seed.py (canonical seed)
  - data/alberta_2023_results.csv
  - data/v0_2_canonical_majority_2026_eds_topoclean.gpkg (or v0_8 series)
  - data/v0_2_canonical_minority_2026_eds_topoclean.gpkg (or v0_8 series)
"""
from __future__ import annotations


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent / "utils"))
    import data_loader


import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent.parent  # .../alberta_audit
sys.path.insert(0, str(Path(__file__).resolve().parent))

from drand_seed import get_canonical_seed  # noqa: E402
from neighbour_drain_adjacency import (  # noqa: E402
    build_adjacency,
    compute_ed_metrics,
    S_THRESHOLD,
    M_THRESHOLD,
)
from packing_cracking_analysis import (  # noqa: E402
    load_2023_results,
    estimate_2026,
    MAJORITY_2026_MAPPING,
    MINORITY_2026_MAPPING,
)

SALT = "drain-label-shuffle"
N_PERMUTATIONS = 10_000


def drain_score(
    pair_df: pd.DataFrame,
    ed_lookup: Dict[str, Dict],
    s_thresh: float = S_THRESHOLD,
    m_thresh: float = M_THRESHOLD,
) -> float:
    """Continuous drain_score: sum of intensity over all coupled directed pairs.

    intensity(X, Y) = max(0, s_X - s_thresh) * max(0, m_thresh - m_Y)
    Only sums coupled pairs (losing_party(X) == losing_party(Y)).
    """
    total = 0.0
    for _, row in pair_df.iterrows():
        X, Y = row["X"], row["Y"]
        if X not in ed_lookup or Y not in ed_lookup:
            continue
        eX = ed_lookup[X]
        eY = ed_lookup[Y]
        if eX["losing_party"] != eY["losing_party"]:
            continue
        intensity = max(0.0, eX["s"] - s_thresh) * max(0.0, m_thresh - eY["m"])
        total += intensity
    return total


def directed_pairs_from_undirected(
    undirected: List[Tuple[str, str]],
) -> List[Tuple[str, str]]:
    """Expand undirected (a, b) pairs to directed (a→b) + (b→a)."""
    result = []
    for a, b in undirected:
        result.append((a, b))
        result.append((b, a))
    return result


def label_shuffle_null(
    ed_names: List[str],
    vote_vectors: np.ndarray,
    directed_pairs: List[Tuple[str, str]],
    n_perm: int,
    rng: np.random.Generator,
    s_thresh: float = S_THRESHOLD,
    m_thresh: float = M_THRESHOLD,
) -> np.ndarray:
    """Run label-shuffle null. vote_vectors: shape (n_eds, 2) — (ndp, ucp) per ED.
    Returns array of drain_scores for n_perm permutations.
    """
    n = len(ed_names)
    scores = np.zeros(n_perm)
    for i in range(n_perm):
        perm_idx = rng.permutation(n)
        shuffled = vote_vectors[perm_idx]
        shuffled_votes = {
            ed_names[j]: (int(shuffled[j, 0]), int(shuffled[j, 1])) for j in range(n)
        }
        perm_ed_df = compute_ed_metrics(shuffled_votes)
        perm_lookup = perm_ed_df.set_index("ed").to_dict("index")
        pairs_df = pd.DataFrame(directed_pairs, columns=["X", "Y"])
        scores[i] = drain_score(pairs_df, perm_lookup, s_thresh, m_thresh)
        if (i + 1) % 1000 == 0:
            print(f"    permutation {i+1}/{n_perm}...")
    return scores


def run_map_null(
    label: str,
    votes: Dict[str, Tuple[int, int]],
    undirected_pairs: List[Tuple[str, str]],
    seed: int,
    n_perm: int = N_PERMUTATIONS,
) -> Dict:
    print(f"\n--- {label} ---")
    rng = np.random.default_rng(seed)
    ed_df = compute_ed_metrics(votes)
    ed_lookup = ed_df.set_index("ed").to_dict("index")
    directed = directed_pairs_from_undirected(undirected_pairs)
    pairs_df = pd.DataFrame(directed, columns=["X", "Y"])

    observed = drain_score(pairs_df, ed_lookup)
    print(f"  observed drain_score = {observed:.6f}")

    # Prepare ordered arrays for shuffling
    ed_names = ed_df["ed"].tolist()
    vote_vectors = np.array(
        [(votes[ed][0], votes[ed][1]) for ed in ed_names], dtype=float
    )

    print(f"  running {n_perm} label-shuffle permutations...")
    null_scores = label_shuffle_null(ed_names, vote_vectors, directed, n_perm, rng)

    mean_null = float(np.mean(null_scores))
    std_null = float(np.std(null_scores, ddof=1))
    z = (observed - mean_null) / std_null if std_null > 0 else float("nan")
    pct_rank = float(np.mean(null_scores <= observed))
    # Two-tailed p: probability of being as extreme or more extreme in either direction
    p_two_tailed = 2 * min(pct_rank, 1.0 - pct_rank)

    print(f"  null mean={mean_null:.6f}  std={std_null:.6f}")
    print(
        f"  z={z:.3f}  percentile_rank={pct_rank*100:.2f}%  p(two-tailed)={p_two_tailed:.4f}"
    )

    return {
        "label": label,
        "observed": observed,
        "null_mean": mean_null,
        "null_std": std_null,
        "z": z,
        "percentile_rank": pct_rank,
        "p_two_tailed": p_two_tailed,
        "n_perm": n_perm,
        "null_scores_p5": float(np.percentile(null_scores, 5)),
        "null_scores_p95": float(np.percentile(null_scores, 95)),
        "null_scores_p025": float(np.percentile(null_scores, 2.5)),
        "null_scores_p975": float(np.percentile(null_scores, 97.5)),
    }


def main() -> None:
    seed = get_canonical_seed(SALT)
    print(f"Drand seed (salt='{SALT}'): {seed}")
    print(f"Drand round: 5500000  (verify: drand.cloudflare.com/public/5500000)")

    out_reports = ROOT / "analysis" / "reports"
    out_data = data_loader._resolve_path("data")
    out_reports.mkdir(parents=True, exist_ok=True)

    # Load votes
    print("\nLoading 2023 two-party results...")
    dists_2019 = load_2023_results()
    votes_2019 = {d["ed"]: (d["ndp"], d["ucp"]) for d in dists_2019}
    rural = [d for d in dists_2019 if d["region"] == "Rest of Alberta"]
    rural_ndp = sum(d["ndp"] for d in rural) / sum(d["ndp"] + d["ucp"] for d in rural)

    print("Estimating 2023 votes on 2026 majority EDs...")
    maj_list = estimate_2026(dists_2019, MAJORITY_2026_MAPPING, rural_ndp)
    votes_maj = {d["ed"]: (d["ndp"], d["ucp"]) for d in maj_list}

    print("Estimating 2023 votes on 2026 minority EDs...")
    min_list = estimate_2026(dists_2019, MINORITY_2026_MAPPING, rural_ndp)
    votes_min = {d["ed"]: (d["ndp"], d["ucp"]) for d in min_list}

    # Load shapefiles (use best available)
    def _pick_shp(plan: str):
        # Prefer official canonical shapefiles
        canonical = out_data / "shapefiles" / "canonical" / f"ea_{plan}_2026_eds.gpkg"
        if canonical.exists():
            return canonical, "EDName2025"
        # Fall back to derived versions
        base = out_data / "shapefiles" / "derived"
        for fname in (
            f"v11_{plan}_2026_eds.gpkg",
            f"v0_8_full_refined_{plan}_2026_eds.gpkg",
            f"v0_8_refined_{plan}_2026_eds.gpkg",
            f"v0_8_canonical_{plan}_2026_eds.gpkg",
            f"v0_2_canonical_{plan}_2026_eds_topoclean.gpkg",
        ):
            p = base / fname
            if p.exists():
                return p, "name_2026"
        return base / f"v0_2_canonical_{plan}_2026_eds_topoclean.gpkg", "name_2026"

    print("\nLoading shapefiles...")
    shp_maj_path, col_maj = _pick_shp("majority")
    shp_min_path, col_min = _pick_shp("minority")
    shp_maj = gpd.read_file(shp_maj_path)
    shp_min = gpd.read_file(shp_min_path)
    print(f"  majority: {shp_maj_path.name}  col={col_maj}")
    print(f"  minority: {shp_min_path.name}  col={col_min}")

    print("Building adjacency graphs...")
    undirected_maj, _, _ = build_adjacency(shp_maj, col_maj)
    undirected_min, _, _ = build_adjacency(shp_min, col_min)
    print(f"  majority: {len(undirected_maj)} undirected pairs")
    print(f"  minority: {len(undirected_min)} undirected pairs")

    # Use same RNG seed for both maps (derived from same root, different by label)
    seed_maj = get_canonical_seed(SALT + "-majority")
    seed_min = get_canonical_seed(SALT + "-minority")
    print(f"\nPer-map seeds: majority={seed_maj}  minority={seed_min}")

    results = {}
    results["majority"] = run_map_null("majority", votes_maj, undirected_maj, seed_maj)
    results["minority"] = run_map_null("minority", votes_min, undirected_min, seed_min)

    # Evaluate pre-registered predictions
    print("\n" + "=" * 60)
    print("  PRE-REGISTERED PREDICTIONS (AsPredicted #289451)")
    print("=" * 60)

    score_maj = results["majority"]["observed"]
    score_min = results["minority"]["observed"]

    pred_a = score_maj > score_min
    print(f"\nPrediction A: drain_score(majority) > drain_score(minority)")
    print(f"  majority={score_maj:.6f}  minority={score_min:.6f}")
    print(f"  RESULT: {'CONFIRMED' if pred_a else 'NOT CONFIRMED'}")

    pred_b_maj = results["majority"]["p_two_tailed"] > 0.05
    pred_b_min = results["minority"]["p_two_tailed"] > 0.05
    print(f"\nPrediction B: both maps within null (p > 0.05 two-tailed)")
    print(
        f"  majority p={results['majority']['p_two_tailed']:.4f} "
        f"({'within' if pred_b_maj else 'OUTSIDE'} null)"
    )
    print(
        f"  minority p={results['minority']['p_two_tailed']:.4f} "
        f"({'within' if pred_b_min else 'OUTSIDE'} null)"
    )
    if not pred_b_maj:
        print(f"  FLAG: majority map is outside null distribution (p < 0.05)")
    if not pred_b_min:
        print(f"  FLAG: minority map is outside null distribution (p < 0.05)")

    print(f"\nPrediction C: qualitative specificity-weighting (exploratory Phase E)")
    print(f"  Not computed here — requires per-pair null frequency from this run.")
    print(f"  See analysis/reports/drain_label_shuffle_null.md for guidance.")

    # Write summary JSON
    summary_path = out_data / "drain_label_shuffle_null.json"
    output = {
        "seed_salt": SALT,
        "drand_round": 5500000,
        "seed_majority": seed_maj,
        "seed_minority": seed_min,
        "n_permutations": N_PERMUTATIONS,
        "majority": results["majority"],
        "minority": results["minority"],
        "predictions": {
            "A_majority_gt_minority": bool(pred_a),
            "B_majority_in_null": bool(pred_b_maj),
            "B_minority_in_null": bool(pred_b_min),
        },
    }
    with open(summary_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote: {summary_path}")

    # Write markdown report
    _write_report(out_reports / "drain_label_shuffle_null.md", output, results)
    print(f"Wrote: {out_reports / 'drain_label_shuffle_null.md'}")


def _write_report(path: Path, output: Dict, results: Dict) -> None:
    r_maj = results["majority"]
    r_min = results["minority"]
    pred = output["predictions"]

    def fmt_pred(v: bool) -> str:
        return "**CONFIRMED**" if v else "**NOT CONFIRMED**"

    content = f"""# Drain Label-Shuffle Null (Phase B)

*Generated by `analysis/scripts/drain_label_shuffle_null.py`*
*Pre-registered: AsPredicted #289451*

## Seed

Drand round {output['drand_round']} (Cloudflare League of Entropy).
Salt: `'{output['seed_salt']}'`.
Majority seed: `{output['seed_majority']}`. Minority seed: `{output['seed_minority']}`.
Verify: `drand.cloudflare.com/public/{output['drand_round']}`

## Method

Continuous drain_score = Σ intensity(X, Y) over all coupled directed adjacent
pairs (X, Y) where losing_party(X) = losing_party(Y).

  intensity(X, Y) = max(0, s_X − 0.15) × max(0, 0.05 − m_Y)

Null: {output['n_permutations']:,} label-shuffle permutations — vote vectors
(NDP, UCP) randomly reassigned across EDs; adjacency graph fixed.

## Results

| Map | drain_score | Null mean | Null std | z-score | Percentile rank | p (two-tailed) |
|---|---|---|---|---|---|---|
| Majority | {r_maj['observed']:.6f} | {r_maj['null_mean']:.6f} | {r_maj['null_std']:.6f} | {r_maj['z']:.3f} | {r_maj['percentile_rank']*100:.1f}% | {r_maj['p_two_tailed']:.4f} |
| Minority | {r_min['observed']:.6f} | {r_min['null_mean']:.6f} | {r_min['null_std']:.6f} | {r_min['z']:.3f} | {r_min['percentile_rank']*100:.1f}% | {r_min['p_two_tailed']:.4f} |

Null 95% CI (majority): [{r_maj['null_scores_p025']:.6f}, {r_maj['null_scores_p975']:.6f}]
Null 95% CI (minority): [{r_min['null_scores_p025']:.6f}, {r_min['null_scores_p975']:.6f}]

## Pre-registered Predictions

**Prediction A**: drain_score(majority) > drain_score(minority)
  {fmt_pred(pred['A_majority_gt_minority'])}
  majority = {r_maj['observed']:.6f}, minority = {r_min['observed']:.6f}

**Prediction B**: both maps within null distribution (p > 0.05 two-tailed)
  Majority: p = {r_maj['p_two_tailed']:.4f} → {fmt_pred(pred['B_majority_in_null'])}
  Minority: p = {r_min['p_two_tailed']:.4f} → {fmt_pred(pred['B_minority_in_null'])}

**Prediction C** (exploratory Phase E): qualitative specificity weighting.
  Specificity weight(X,Y) = 1 − P(pair fires | null).
  Per-pair null frequency requires post-hoc computation from null permutation
  logs. To be computed in Phase E after B predictions evaluated.

## Notes

- Adjacency graph is the same buffered-intersection graph as Test 3A
  (neighbour_drain_adjacency.py, 600 m half-buffer + K-nearest fallback).
- Vote substrate: 2023 two-party (NDP + UCP) via §5.3 blending pipeline.
- Two-tailed p = 2 × min(rank, 1 − rank) where rank = P(null ≤ observed).
"""
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
