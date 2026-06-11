"""
extended_partisan_metrics_canonical.py — Canonical-substrate Partisan Bias,
Lopsided-t, Proportionality Deviation, Responsiveness.

Re-run of extended_partisan_metrics.py on canonical Elections Alberta substrate.
Replaces the v0_7 DPG + 10k ReCom values that currently land in
findings/extended_partisan_metrics.md and feed §1.1 BH-table rows 5–6
(Lopsided Margins t=3.43 / t=3.05).

Substrate:
  - shapefiles: data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg
                data/shapefiles/reference/alberta_2019_eds/...shp
  - VA layer:   data/shapefiles/canonical/va_2023_election_day_votes.gpkg
                (integer va_ndp / va_ucp; mirrors mcmc_ensemble_canonical.py)
  - attribution: representative_point() centroid-in-polygon
  - ensemble:   data/simulation_checkpoints_canonical/chain*_samples.csv
                (1,010,000-plan canonical ReCom ensemble, seed 1432864451)

Backward:
  analysis/scripts/extended_partisan_metrics.py — original (v0_7 substrate)
  analysis/scripts/packing_cracking_analysis.py — canonical vote attribution
Forward:
  findings/extended_partisan_metrics_canonical.md
  findings/extended_partisan_metrics_canonical.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from extended_partisan_metrics import (  # noqa: E402
    partisan_bias,
    lopsided_margins,
    proportionality_deviation,
    responsiveness,
    pct_rank,
)
from packing_cracking_analysis import score_map_by_spatial_join  # noqa: E402
from canonical_paths import canonical_shapefile, ED_NAME_COL, reference_2019_shapefile  # noqa: E402

VA_PATH = ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg"
ENSEMBLE_DIR = ROOT / "data/simulation_checkpoints_canonical"


def load_ensemble() -> pd.DataFrame:
    parts = []
    for chain in sorted(ENSEMBLE_DIR.glob("chain*_samples.csv")):
        parts.append(pd.read_csv(chain))
    if not parts:
        raise FileNotFoundError(f"No canonical ensemble CSVs in {ENSEMBLE_DIR}")
    df = pd.concat(parts, ignore_index=True)
    return df


def shares_canonical(plan: str, va_gdf: gpd.GeoDataFrame) -> np.ndarray:
    if plan == "enacted_2019":
        shp = reference_2019_shapefile()
        name_col = "EDName2017"
    else:
        shp = canonical_shapefile(plan)
        name_col = ED_NAME_COL
    eds = gpd.read_file(shp)[[name_col, "geometry"]]
    if eds.crs != va_gdf.crs:
        eds = eds.to_crs(va_gdf.crs)
    centroids = va_gdf.copy()
    centroids["geometry"] = va_gdf.geometry.representative_point()
    joined = gpd.sjoin(
        centroids[["va_ucp", "va_ndp", "geometry"]],
        eds,
        how="left",
        predicate="within",
    ).dropna(subset=[name_col])
    joined = joined[~joined.index.duplicated(keep="first")]
    agg = (
        joined.groupby(name_col)
        .agg(ndp=("va_ndp", "sum"), ucp=("va_ucp", "sum"))
        .reset_index()
    )
    shares = []
    for _, r in agg.iterrows():
        total = int(r["ndp"] + r["ucp"])
        if total > 0:
            shares.append(int(r["ucp"]) / total)
    return np.array(shares)


def all_metrics(shares: np.ndarray) -> Dict:
    pb = partisan_bias(shares)
    t, p = lopsided_margins(shares)
    prop_dev = proportionality_deviation(shares)
    resp = responsiveness(shares)
    return {
        "n_districts": int(len(shares)),
        "mean_ucp_vote_share": float(np.nanmean(shares)),
        "ucp_wins": int((shares > 0.5).sum()),
        "partisan_bias": float(pb),
        "lopsided_t": float(t),
        "lopsided_p": float(p),
        "proportionality_deviation": float(prop_dev),
        "responsiveness": float(resp),
    }


def script_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def write_md(out_md: Path, payload: Dict) -> None:
    rows = payload["per_map"]
    lines = [
        "---",
        "name: extended_partisan_metrics_canonical",
        "date: 2026-06-11",
        "substrate: canonical (ea_*_2026_eds.gpkg + va_2023_election_day_votes.gpkg + 1.01M ReCom)",
        f"script_commit: {payload['script_commit']}",
        "supersedes: findings/extended_partisan_metrics.md (v0_7 DPG substrate + 10k ReCom)",
        "---",
        "",
        "> **Backward:**",
        "> - `analysis/scripts/extended_partisan_metrics_canonical.py` — this analysis",
        "> - `findings/extended_partisan_metrics.md` — superseded predecessor (v0_7 substrate)",
        ">",
        "> **Forward:**",
        "> - `reports/academic/report_academic.md` §5.2.9 — canonical numbers now anchor the §5.2.9 reading",
        "> - `reports/academic/report_academic.md` §1.1 BH-table rows 5–6 (Lopsided Margins) — t-values to refresh",
        "",
        "# Extended Partisan Metrics — CANONICAL substrate (Alberta 2026)",
        "",
        "Substrate: official Elections Alberta shapefiles + canonical VA centroid-in-polygon spatial join + 1,010,000-plan canonical ReCom ensemble (4 chains × 252,500, base_seed=1432864451).",
        "",
        "## Results",
        "",
        "| Map | N EDs | UCP wins | Partisan Bias | PB ensemble pct | Lopsided-t | Lopsided-p | Proportionality Deviation | Responsiveness |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, r in rows.items():
        pb_pct = f"{r.get('partisan_bias_percentile', float('nan')):.2f}" if not np.isnan(r.get("partisan_bias_percentile", float("nan"))) else "—"
        lines.append(
            f"| {label} | {r['n_districts']} | {r['ucp_wins']} | "
            f"{r['partisan_bias']:+.4f} | {pb_pct} | "
            f"{r['lopsided_t']:+.3f} | {r['lopsided_p']:.4f} | "
            f"{r['proportionality_deviation']:+.4f} | {r['responsiveness']:.2f} |"
        )
    lines += [
        "",
        "## Provenance compared to v0_7 predecessor",
        "",
        "| Metric | v0_7 majority | canonical majority | v0_7 minority | canonical minority |",
        "|---|---:|---:|---:|---:|",
        f"| Partisan Bias | −0.0402 | {rows['majority_2026']['partisan_bias']:+.4f} | −0.0422 | {rows['minority_2026']['partisan_bias']:+.4f} |",
        f"| Lopsided-t | +3.158 | {rows['majority_2026']['lopsided_t']:+.3f} | +3.491 | {rows['minority_2026']['lopsided_t']:+.3f} |",
        f"| Responsiveness | 1.15 | {rows['majority_2026']['responsiveness']:.2f} | 2.41 | {rows['minority_2026']['responsiveness']:.2f} |",
        "",
        "## §1.1 BH-table refresh (Lopsided Margins rows 5-6)",
        "",
        f"- Row 5 (Majority Lopsided-t = 3.43 → **{rows['majority_2026']['lopsided_t']:+.3f}** on canonical substrate, p = {rows['majority_2026']['lopsided_p']:.4f})",
        f"- Row 6 (Minority Lopsided-t = 3.05 → **{rows['minority_2026']['lopsided_t']:+.3f}** on canonical substrate, p = {rows['minority_2026']['lopsided_p']:.4f})",
        "",
        "The Lopsided Margins finding remains a structural property of Alberta's political geography present on the 2019 enacted baseline (Lopsided-t = "
        f"{rows['enacted_2019']['lopsided_t']:+.3f}) and on both 2026 commission proposals.",
        "",
        "## Reproducibility",
        "",
        "```bash",
        "python analysis/scripts/extended_partisan_metrics_canonical.py",
        "```",
        "",
        f"Script commit: `{payload['script_commit']}`",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-json", type=Path,
                    default=ROOT / "findings/extended_partisan_metrics_canonical.json")
    ap.add_argument("--output-md", type=Path,
                    default=ROOT / "findings/extended_partisan_metrics_canonical.md")
    args = ap.parse_args(argv)

    print("Loading canonical VA layer ...", flush=True)
    va_gdf = gpd.read_file(VA_PATH)

    per_map: Dict[str, Dict] = {}
    for label in ("majority_2026", "minority_2026", "enacted_2019"):
        plan = {"majority_2026": "majority", "minority_2026": "minority", "enacted_2019": "enacted_2019"}[label]
        print(f"[{label}] computing shares + metrics ...", flush=True)
        shares = shares_canonical(plan, va_gdf)
        m = all_metrics(shares)
        per_map[label] = m
        print(f"  {label}: n={m['n_districts']} PB={m['partisan_bias']:+.4f} "
              f"Lopsided-t={m['lopsided_t']:+.3f} (p={m['lopsided_p']:.4f}) "
              f"Resp={m['responsiveness']:.2f}", flush=True)

    print("Loading canonical 1.01M-plan ensemble for PB percentile ...", flush=True)
    ens = load_ensemble()
    ens["partisan_bias_approx"] = ens["seats_at_50_50"] - 0.5
    pb_arr = ens["partisan_bias_approx"].dropna().values
    for label, m in per_map.items():
        m["partisan_bias_percentile"] = pct_rank(pb_arr, m["partisan_bias"])

    payload = {
        "test": "Extended partisan metrics — CANONICAL substrate",
        "script_commit": script_commit(),
        "ensemble_size": int(len(ens)),
        "per_map": per_map,
        "supersedes": "findings/extended_partisan_metrics.md (v0_7 substrate + 10k ReCom)",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2, default=float), encoding="utf-8")
    write_md(args.output_md, payload)
    print(f"\njson -> {args.output_json}")
    print(f"md   -> {args.output_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
