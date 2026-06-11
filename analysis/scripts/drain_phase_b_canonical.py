"""
drain_phase_b_canonical.py — Canonical-substrate Phase B label-shuffle null.

Re-run of drain_label_shuffle_null.py on the canonical Elections Alberta substrate
(ea_*_2026_eds.gpkg + va_2023_election_day_votes.gpkg). Replaces the DPG-era /
blended-vote substrate Phase B run whose numbers turned out substrate-stale
(see findings/drain_metric_validation.md, 2026-06-11).

Same drain_score formula and label-shuffle null procedure as the original Phase B;
only the vote-attribution substrate changes:
  - votes per ED: score_map_by_spatial_join(va_gdf, ea_shp, EDName2025)
  - adjacency: build_adjacency on canonical EA polygons (600 m half-buffer)
  - N_PERMUTATIONS = 10_000
  - Salt: 'drain-label-shuffle' (same as original; canonical-substrate recomputation)

Backward:
  analysis/scripts/drain_label_shuffle_null.py — original (stale-substrate)
  analysis/scripts/neighbour_drain_adjacency.py — drain helpers
  analysis/scripts/packing_cracking_analysis.py — canonical vote attribution
  data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg
  data/shapefiles/canonical/va_2023_election_day_votes.gpkg
Forward:
  findings/drain_label_shuffle_null_canonical.md  — published result
  findings/drain_label_shuffle_null_canonical.json — machine-readable
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from neighbour_drain_adjacency import (  # noqa: E402
    build_adjacency,
    compute_ed_metrics,
    S_THRESHOLD,
    M_THRESHOLD,
)
from packing_cracking_analysis import score_map_by_spatial_join  # noqa: E402
from canonical_paths import canonical_shapefile, ED_NAME_COL, reference_2019_shapefile  # noqa: E402

SALT = "drain-label-shuffle-canonical-2026-06-11"
N_PERMUTATIONS = 10_000

VA_PATH = ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg"


def drain_score_from_lookup(directed_pairs, ed_lookup) -> Tuple[float, int]:
    total = 0.0
    coupled = 0
    for X, Y in directed_pairs:
        eX = ed_lookup.get(X)
        eY = ed_lookup.get(Y)
        if not eX or not eY:
            continue
        if eX["losing_party"] != eY["losing_party"]:
            continue
        if eX["s"] >= S_THRESHOLD and eY["m"] <= M_THRESHOLD:
            coupled += 1
        total += max(0.0, eX["s"] - S_THRESHOLD) * max(0.0, M_THRESHOLD - eY["m"])
    return total, coupled


def lookup_from_metrics(df) -> Dict[str, Dict]:
    return {
        r["ed"]: {
            "s": r["s"],
            "m": r["m"],
            "losing_party": r["losing_party"],
            "winner_party": r["winner_party"],
        }
        for _, r in df.iterrows()
    }


def load_map_canonical(plan: str, va_gdf: gpd.GeoDataFrame) -> Tuple[Dict, List]:
    if plan == "enacted_2019":
        shp = reference_2019_shapefile()
        name_col = "EDName2017"
    else:
        shp = canonical_shapefile(plan)
        name_col = ED_NAME_COL
    gdf = gpd.read_file(shp)
    if va_gdf.crs != gdf.crs:
        va_gdf = va_gdf.to_crs(gdf.crs)
    rows = score_map_by_spatial_join(va_gdf, shp, name_col)
    votes = {r["ed"]: (int(r["ndp"]), int(r["ucp"])) for r in rows}

    pairs_undirected, _, _ = build_adjacency(gdf, name_col)
    directed = [(a, b) for a, b in pairs_undirected] + [(b, a) for a, b in pairs_undirected]
    return votes, directed


def run_null(votes: Dict, directed_pairs: List, rng: np.random.Generator) -> Tuple[float, np.ndarray]:
    df_obs = compute_ed_metrics(votes)
    lookup_obs = lookup_from_metrics(df_obs)
    obs_score, _ = drain_score_from_lookup(directed_pairs, lookup_obs)

    ed_names = list(votes.keys())
    vote_pairs = np.array([votes[n] for n in ed_names])  # shape (n, 2)
    null_scores = np.empty(N_PERMUTATIONS, dtype=float)

    for i in range(N_PERMUTATIONS):
        perm = rng.permutation(len(ed_names))
        perm_votes = {ed_names[k]: tuple(vote_pairs[perm[k]]) for k in range(len(ed_names))}
        df_perm = compute_ed_metrics(perm_votes)
        lookup_perm = lookup_from_metrics(df_perm)
        score, _ = drain_score_from_lookup(directed_pairs, lookup_perm)
        null_scores[i] = score

    return obs_score, null_scores


def script_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def write_md(out_md: Path, payload: Dict) -> None:
    lines = [
        "---",
        "name: drain_label_shuffle_null_canonical",
        "date: 2026-06-11",
        f"substrate: canonical (ea_*_2026_eds.gpkg + va_2023_election_day_votes.gpkg)",
        f"script_commit: {payload['script_commit']}",
        f"salt: {SALT}",
        f"n_permutations: {N_PERMUTATIONS}",
        "supersedes: findings/drain_label_shuffle_null.md (DPG-era / blended-vote substrate)",
        "---",
        "",
        "> **Backward:**",
        "> - `analysis/scripts/drain_phase_b_canonical.py` — this analysis",
        "> - `findings/drain_label_shuffle_null.md` — superseded predecessor (DPG / blended substrate)",
        "> - `findings/drain_metric_validation.md` — the substrate-staleness discovery that motivated this re-run",
        ">",
        "> **Forward:**",
        "> - `reports/academic/report_academic.md` §5.3.5 — canonical numbers now anchor the §5.3.5 continuous-score reading",
        "> - `findings/joint_outlier_score.json` — `neighbour_drain` block can drop its SUBSTRATE_STATUS retraction now this rerun is published",
        "",
        "# Drain Phase B label-shuffle null — CANONICAL substrate",
        "",
        "## Method (unchanged from original Phase B)",
        "",
        "Continuous `drain_score = Σ intensity(X, Y)` over coupled directed adjacent pairs where",
        "",
        "```",
        "intensity(X, Y) = max(0, s_X − 0.15) × max(0, 0.05 − m_Y)",
        "coupled iff losing_party(X) == losing_party(Y)",
        "```",
        "",
        f"Null: {N_PERMUTATIONS:,} label-shuffle permutations — (NDP, UCP) vote vectors randomly reassigned across EDs; adjacency graph fixed.",
        "",
        "## Substrate (this is the canonical version)",
        "",
        "- Shapefiles: `data/shapefiles/canonical/ea_majority_2026_eds.gpkg` + `ea_minority_2026_eds.gpkg` + 2019 enacted reference.",
        "- VA vote layer: `data/shapefiles/canonical/va_2023_election_day_votes.gpkg`, integer columns `va_ndp` / `va_ucp` (mirrors `mcmc_ensemble_canonical.py`).",
        "- Attribution: `representative_point()` centroid-in-polygon spatial join.",
        "- Adjacency: queen-contiguity via `neighbour_drain_adjacency.build_adjacency` (600 m half-buffer, K-nearest fallback for isolates).",
        "",
        "## Results",
        "",
        "| Map | observed drain_score | null mean | null std | z-score | percentile rank | p (two-tailed) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for m in ("majority_2026", "minority_2026", "enacted_2019"):
        r = payload["per_map"][m]
        lines.append(
            f"| {m} | {r['observed']:.6f} | {r['null_mean']:.6f} | {r['null_std']:.6f} | "
            f"{r['z']:.3f} | {r['percentile']:.2f}% | {r['p_two_tailed']:.4f} |"
        )
    lines += [
        "",
        "## Pre-registered Prediction A revisited",
        "",
        f"- Prediction A (drain(majority) > drain(minority)): {'CONFIRMED' if payload['prediction_A_confirmed'] else 'NOT CONFIRMED'} on canonical substrate.",
        f"- Observed: majority = {payload['per_map']['majority_2026']['observed']:.6f}, minority = {payload['per_map']['minority_2026']['observed']:.6f}.",
        "- The original Phase B numbers (majority = 0.000179, minority = 0.006176; majority z = −2.915 \"anomalously low\") were computed on a DPG-era / blended-vote substrate. They are now superseded by this canonical run.",
        "",
        "## Reproducibility",
        "",
        "```bash",
        "python analysis/scripts/drain_phase_b_canonical.py",
        "```",
        "",
        f"Script commit: `{payload['script_commit']}`",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-json", type=Path,
                    default=ROOT / "findings/drain_label_shuffle_null_canonical.json")
    ap.add_argument("--output-md", type=Path,
                    default=ROOT / "findings/drain_label_shuffle_null_canonical.md")
    ap.add_argument("--seed", type=int, default=460508741)
    args = ap.parse_args(argv)

    print(f"Loading canonical VA layer …", flush=True)
    va_gdf = gpd.read_file(VA_PATH)

    per_map: Dict[str, Dict] = {}
    rng = np.random.default_rng(args.seed)
    for plan in ("majority_2026", "minority_2026", "enacted_2019"):
        plan_key = plan.replace("_2026", "").replace("_2019", "") if plan != "enacted_2019" else "enacted_2019"
        # Re-key for load function
        load_key = {"majority_2026": "majority", "minority_2026": "minority", "enacted_2019": "enacted_2019"}[plan]
        print(f"[{plan}] loading + scoring …", flush=True)
        votes, directed = load_map_canonical(load_key, va_gdf)
        print(f"[{plan}] running {N_PERMUTATIONS:,} label-shuffle permutations …", flush=True)
        obs, null = run_null(votes, directed, rng)
        mean = float(null.mean())
        std = float(null.std() or 1e-30)
        z = (obs - mean) / std
        rank = float((null <= obs).sum() / N_PERMUTATIONS)
        p_two = 2.0 * min(rank, 1.0 - rank)
        per_map[plan] = {
            "n_eds": len(votes),
            "n_directed_pairs": len(directed),
            "observed": float(obs),
            "null_mean": mean,
            "null_std": std,
            "z": float(z),
            "percentile": float(rank * 100.0),
            "p_two_tailed": float(p_two),
        }
        print(f"[{plan}] observed={obs:.6f} null_mean={mean:.6f} z={z:.3f} p_two={p_two:.4f}", flush=True)

    confirmed = per_map["majority_2026"]["observed"] > per_map["minority_2026"]["observed"]

    payload = {
        "test": "Drain Phase B label-shuffle null — CANONICAL substrate",
        "salt": SALT,
        "n_permutations": N_PERMUTATIONS,
        "seed": args.seed,
        "script_commit": script_commit(),
        "per_map": per_map,
        "prediction_A_confirmed": bool(confirmed),
        "supersedes": "findings/drain_label_shuffle_null.md (DPG / blended substrate)",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_md(args.output_md, payload)
    print(f"\nPrediction A confirmed: {confirmed}")
    print(f"json -> {args.output_json}")
    print(f"md   -> {args.output_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
