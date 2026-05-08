"""
v0_1_extended_partisan_metrics.py
===================================
Computes additional partisan bias metrics beyond the four in the MCMC ensemble:

  - Partisan Bias (seats-votes asymmetry at 50%)
  - Lopsided Margins (t-test: Wang 2016)
  - Partisan Gini (area between seats-votes curve and symmetry line)
  - Responsiveness (slope of seats-votes curve at 50%)
  - Declination variant (already have but included for completeness)

For each metric, computes:
  1. Value on each real map (2019, majority 2026, minority 2026)
  2. Percentile rank against the 10k MCMC ensemble where calculable
  3. For metrics not in the ensemble, reports absolute value + interpretation

Uses v0_7 shapefiles for 2026 maps (89 EDs, full coverage).

Outputs:
  analysis/reports/extended_partisan_metrics.md
  data/extended_partisan_metrics.json

Backward:
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
  data/shapefiles/derived/v0_7_canonical_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_7_canonical_minority_2026_eds.gpkg
  data/simulated_ensemble_raw_samples_100k.csv
Forward:
  analysis/reports/extended_partisan_metrics.md
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

import json, sys, time, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy import stats as scipy_stats

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
RPTS = ROOT / "analysis" / "reports"
RPTS.mkdir(parents=True, exist_ok=True)


def _pick(plan: str):
    base = DATA / "shapefiles" / "derived"
    for fname in (
        f"v0_8_full_refined_{plan}_2026_eds.gpkg",
        f"v0_8_refined_{plan}_2026_eds.gpkg",
        f"v0_8_canonical_{plan}_2026_eds.gpkg",
        f"v0_7_canonical_{plan}_2026_eds.gpkg",
    ):
        p = base / fname
        if p.exists():
            return p
    return base / f"v0_7_canonical_{plan}_2026_eds.gpkg"


VA_PATH = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
MAJ_V7 = _pick("majority")
MIN_V7 = _pick("minority")
ENSEMBLE_CSV = DATA / "simulated_ensemble_raw_samples_100k.csv"

OUT_JSON = DATA / "extended_partisan_metrics.json"
OUT_MD = RPTS / "extended_partisan_metrics.md"


# ---------------------------------------------------------------------------
# District-level vote share builder
# ---------------------------------------------------------------------------


def districts_from_2019(va: gpd.GeoDataFrame) -> pd.DataFrame:
    """Aggregate VA votes to 2019 enacted EDs."""
    agg = (
        va.groupby("parent_ed_2019")
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    agg["total"] = agg["ucp"] + agg["ndp"]
    agg["ucp_share"] = np.where(agg["total"] > 0, agg["ucp"] / agg["total"], np.nan)
    return agg.dropna(subset=["ucp_share"])


def districts_from_v7(
    va: gpd.GeoDataFrame, eds: gpd.GeoDataFrame, label: str
) -> pd.DataFrame:
    """
    Spatial join: assign each VA centroid to an ED, then aggregate votes.
    Uses v0_7 89-ED shapefiles.
    """
    va_proj = va.to_crs(eds.crs)
    va_centroids = va_proj.copy()
    va_centroids["geometry"] = va_proj.geometry.centroid

    joined = gpd.sjoin(
        va_centroids[["va_ucp", "va_ndp", "geometry"]],
        eds[["EDName2025", "geometry"]],
        how="left",
        predicate="within",
    )
    agg = (
        joined.groupby("EDName2025")
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    agg["total"] = agg["ucp"] + agg["ndp"]
    agg["ucp_share"] = np.where(agg["total"] > 0, agg["ucp"] / agg["total"], np.nan)
    assigned = agg.dropna(subset=["ucp_share"])
    total_vas = len(va_centroids)
    assigned_vas = joined["EDName2025"].notna().sum()
    print(
        f"  [{label}] {len(assigned)} EDs, "
        f"{assigned_vas}/{total_vas} VAs assigned ({assigned_vas/total_vas:.1%})"
    )
    return assigned


# ---------------------------------------------------------------------------
# Metric functions
# ---------------------------------------------------------------------------


def seats_votes_curve(ucp_shares: np.ndarray, swing_range: np.ndarray) -> np.ndarray:
    """
    Uniform partisan swing model.
    For each swing value s, compute fraction of districts where ucp_share + s > 0.5.
    """
    seat_fracs = []
    for s in swing_range:
        swung = ucp_shares + s
        wins = (swung > 0.5 + 1e-9).sum()
        ties = (np.abs(swung - 0.5) <= 1e-9).sum()
        seat_fracs.append((wins + 0.5 * ties) / len(swung))
    return np.array(seat_fracs)


def partisan_bias(ucp_shares: np.ndarray) -> float:
    """
    Partisan bias: difference between UCP seat share and 0.5 when UCP vote share = 0.5.
    Uses uniform swing.
    current_ucp_mean = mean(ucp_shares)
    swing_needed = 0.5 - current_ucp_mean
    """
    mean_share = np.nanmean(ucp_shares)
    swing = 0.5 - mean_share
    swung = ucp_shares + swing
    wins = (swung > 0.5 + 1e-9).sum()
    ties = (np.abs(swung - 0.5) <= 1e-9).sum()
    ucp_seats_at_50 = (wins + 0.5 * ties) / len(swung)
    return float(ucp_seats_at_50 - 0.5)


def lopsided_margins(ucp_shares: np.ndarray) -> tuple[float, float]:
    """
    Wang (2016) lopsided margins test.
    Split districts into UCP wins and NDP wins.
    Test: do the two parties win by systematically different margins?
    UCP wins by abnormally large margins → packing signal.
    Returns (t_statistic, p_value). Positive t = UCP wins by larger margins.
    """
    ucp_wins = ucp_shares[ucp_shares > 0.5 + 1e-9] - 0.5  # margins for UCP wins
    ndp_wins = 0.5 - ucp_shares[ucp_shares < 0.5 - 1e-9]  # margins for NDP wins
    if len(ucp_wins) < 3 or len(ndp_wins) < 3:
        return float("nan"), float("nan")
    t, p = scipy_stats.ttest_ind(ucp_wins, ndp_wins, equal_var=False)
    return float(t), float(p)


def partisan_gini(ucp_shares: np.ndarray) -> float:
    """
    Partisan Gini: area between the seats-votes curve and the symmetry line.
    Positive = UCP-favoured asymmetry.
    """
    swings = np.linspace(-0.3, 0.3, 300)
    sv = seats_votes_curve(ucp_shares, swings)
    vote_shares = np.nanmean(ucp_shares) + swings
    # Symmetry line: at vote share v, expected seat share = v (proportionality)
    # Area above symmetry = UCP advantage
    sym = vote_shares
    area = float(np.trapezoid(sv - sym, vote_shares))
    return area


def responsiveness(ucp_shares: np.ndarray) -> float:
    """
    Responsiveness: slope of seats-votes curve at current vote share (50% swing point).
    Higher = more seats change per unit vote change.
    """
    mean_share = np.nanmean(ucp_shares)
    delta = 0.01
    sv_plus = seats_votes_curve(ucp_shares, np.array([0.5 - mean_share + delta]))[0]
    sv_minus = seats_votes_curve(ucp_shares, np.array([0.5 - mean_share - delta]))[0]
    return float((sv_plus - sv_minus) / (2 * delta))


def all_metrics(ucp_shares: np.ndarray, label: str) -> dict:
    """Compute all extended metrics for one map."""
    pb = partisan_bias(ucp_shares)
    t, p = lopsided_margins(ucp_shares)
    gini = partisan_gini(ucp_shares)
    resp = responsiveness(ucp_shares)
    n = len(ucp_shares)
    mean_vs = float(np.nanmean(ucp_shares))
    ucp_wins = int((ucp_shares > 0.5).sum())

    print(
        f"  {label}: n={n}, mean_vote_share={mean_vs:.3f}, "
        f"ucp_wins={ucp_wins}, PB={pb:+.4f}, "
        f"LM_t={t:+.3f}(p={p:.3f}), Gini={gini:+.4f}, Resp={resp:.2f}"
    )
    return {
        "label": label,
        "n_districts": n,
        "mean_ucp_vote_share": mean_vs,
        "ucp_wins": ucp_wins,
        "partisan_bias": pb,
        "lopsided_t": t,
        "lopsided_p": p,
        "partisan_gini": gini,
        "responsiveness": resp,
    }


def pct_rank(arr: np.ndarray, val: float) -> float:
    """Midrank percentile: 100 * (P(X < x) + 0.5 * P(X == x))."""
    if len(arr) == 0:
        return float("nan")
    less = (arr < val - 1e-9).sum()
    equal = (np.abs(arr - val) <= 1e-9).sum()
    return float(100.0 * (less + 0.5 * equal) / len(arr))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    print("[extended partisan metrics] Loading data...")
    va = gpd.read_file(VA_PATH)
    maj = gpd.read_file(MAJ_V7)
    mn = gpd.read_file(MIN_V7)
    ens = pd.read_csv(ENSEMBLE_CSV)

    print("\nBuilding district-level vote shares...")
    d_2019 = districts_from_2019(va)
    d_maj = districts_from_v7(va, maj, "majority v0_7")
    d_min = districts_from_v7(va, mn, "minority v0_7")

    print("\nComputing extended metrics...")
    results = {}
    for label, df in [
        ("2019_enacted", d_2019),
        ("majority_2026", d_maj),
        ("minority_2026", d_min),
    ]:
        shares = df["ucp_share"].dropna().values
        results[label] = all_metrics(shares, label)

    # Ensemble percentile ranks for metrics we can compute from ensemble CSV
    # partisan_bias uses seats_at_50_50 minus 0.5 — approximate from ensemble
    # The ensemble has seats_at_50_50 (UCP seat share at 50/50 vote), so
    # partisan_bias ≈ seats_at_50_50 - 0.5
    ens["partisan_bias_approx"] = ens["seats_at_50_50"] - 0.5

    print("\nEnsemble percentile ranks (where available):")
    for label, res in results.items():
        for metric_key, ens_col in [
            ("partisan_bias", "partisan_bias_approx"),
        ]:
            val = res[metric_key]
            if not np.isnan(val):
                pr = pct_rank(ens[ens_col].dropna().values, val)
                results[label][f"{metric_key}_percentile"] = pr
                print(f"  {label:22s}  {metric_key:20s}  val={val:+.4f}  p={pr:.1f}")

    # Comparison table
    print("\n--- EXTENDED METRICS COMPARISON ---")
    rows = []
    for label, res in results.items():
        rows.append(
            {
                "map": label,
                "n": res["n_districts"],
                "partisan_bias": res["partisan_bias"],
                "pb_pct": res.get("partisan_bias_percentile", float("nan")),
                "lopsided_t": res["lopsided_t"],
                "lopsided_p": res["lopsided_p"],
                "partisan_gini": res["partisan_gini"],
                "responsiveness": res["responsiveness"],
            }
        )
    df_out = pd.DataFrame(rows)
    with pd.option_context(
        "display.float_format", "{:+.4f}".format, "display.width", 140
    ):
        print(df_out.to_string(index=False))

    # Write outputs
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=float)
    print(f"\nWrote {OUT_JSON}")

    # Markdown report
    md_lines = [
        "# Extended Partisan Metrics — Alberta 2026 Electoral Maps",
        "",
        "Computed against v0_7 shapefiles (89 EDs, full province coverage).",
        "Ensemble percentile ranks from 10k ReCom MCMC samples (seed 42, ±25%).",
        "",
        "## Results",
        "",
        "| Map | N EDs | Partisan Bias | PB pct | Lopsided-t | Lopsided-p | Partisan Gini | Responsiveness |",
        "|-----|-------|--------------|--------|-----------|-----------|--------------|----------------|",
    ]
    for r in rows:
        pb_pct = f"{r['pb_pct']:+.1f}" if not np.isnan(r["pb_pct"]) else "—"
        md_lines.append(
            f"| {r['map']} | {r['n']} | {r['partisan_bias']:+.4f} | {pb_pct} "
            f"| {r['lopsided_t']:+.3f} | {r['lopsided_p']:.3f} "
            f"| {r['partisan_gini']:+.4f} | {r['responsiveness']:.2f} |"
        )
    md_lines += [
        "",
        "## Interpretation",
        "",
        "**Partisan Bias**: Positive = UCP gets >50% of seats at 50/50 vote.",
        "**Lopsided Margins t**: Positive = UCP wins by larger margins than NDP (packing signal).",
        "**Partisan Gini**: Positive = asymmetry favours UCP across the full seats-votes curve.",
        "**Responsiveness**: How many extra seats per 1% vote swing. Lower = more entrenched.",
        "",
        f"_Generated {time.strftime('%Y-%m-%d %H:%M')} — elapsed {time.time()-t0:.0f}s_",
    ]
    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"\nDone in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
