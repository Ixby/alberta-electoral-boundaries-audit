"""
v0_1_gerrymetrics_comparison.py
================================
Cross-validates our partisan-bias metric implementations against the
`gerrymetrics` PyPI package (v0.1.3) and adds the EG variant family
(difference gap, loss gap, surplus gap, vote-centric gap x2, tau gap)
plus Mann-Whitney U as a non-parametric alternative to Wang (2016) t-test.

Sign convention note
--------------------
gerrymetrics is calibrated "Dem-favoured positive." We feed
  voteshares = ndp_share = 1 - ucp_share
so NDP plays the role of "Dem."  Under this mapping:

  Metric              gerrymetrics sign → our sign   adjustment
  ─────────────────── ─────────────────────────────── ────────────────
  EG (standard)       positive = NDP wastes less      = UCP-favoured   none
  EG variants         same as EG                      none
  mean_median         pos = median > mean (NDP share) = UCP-favoured   none
  partisan_bias       pos = UCP seats > 0.5 at 50/50 = UCP-favoured   none
  declination         positive = NDP-favoured         negate → ours
  bdec                same as declination             negate → ours
  t_test diff         d_mean > r_mean (NDP)           negate → ours
  mann_whitney_u      test_stat d > r (NDP)           negate → ours

Outputs:
  analysis/reports/gerrymetrics_comparison.md
  data/gerrymetrics_comparison.json

Backward:
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
  data/shapefiles/derived/v0_7_canonical_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_7_canonical_minority_2026_eds.gpkg
Forward:
  report_academic.md §5.2.9 (EG variant table, Mann-Whitney supplement)
"""

# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd

warnings.filterwarnings("ignore")

import gerrymetrics.metrics as gm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ROOT = HERE.parent.parent
DATA = ROOT / "data"
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

OUT_MD = RPTS / "gerrymetrics_comparison.md"
OUT_JSON = DATA / "gerrymetrics_comparison.json"


# ---------------------------------------------------------------------------
# Vote attribution (reuses pattern from v0_1_extended_partisan_metrics)
# ---------------------------------------------------------------------------


def districts_from_2019(va: gpd.GeoDataFrame) -> np.ndarray:
    agg = (
        va.groupby("parent_ed_2019")
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    agg["total"] = agg["ucp"] + agg["ndp"]
    agg["ucp_share"] = np.where(agg["total"] > 0, agg["ucp"] / agg["total"], np.nan)
    return agg.dropna(subset=["ucp_share"])["ucp_share"].values


def districts_from_v7(
    va: gpd.GeoDataFrame, eds: gpd.GeoDataFrame, label: str
) -> np.ndarray:
    va_proj = va.to_crs(eds.crs)
    va_c = va_proj.copy()
    va_c["geometry"] = va_proj.geometry.centroid
    joined = gpd.sjoin(
        va_c[["va_ucp", "va_ndp", "geometry"]],
        eds[["name_2026", "geometry"]],
        how="left",
        predicate="within",
    )
    agg = (
        joined.groupby("name_2026")
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    agg["total"] = agg["ucp"] + agg["ndp"]
    agg["ucp_share"] = np.where(agg["total"] > 0, agg["ucp"] / agg["total"], np.nan)
    assigned = agg.dropna(subset=["ucp_share"])
    assigned_vas = joined["name_2026"].notna().sum()
    print(
        f"  [{label}] {len(assigned)} EDs, "
        f"{assigned_vas}/{len(va)} VAs assigned ({assigned_vas/len(va):.1%})"
    )
    return assigned["ucp_share"].values


# ---------------------------------------------------------------------------
# Our own EG / MM / declination for cross-check (same formulas as ensemble)
# ---------------------------------------------------------------------------


def _our_metrics(ucp_share: np.ndarray) -> dict:
    import math

    total = np.ones_like(ucp_share)  # equal-turnout assumption (like S&M)
    n = len(ucp_share)
    ucp_win = ucp_share > 0.5
    ucp_wasted = np.where(ucp_win, ucp_share - 0.5, ucp_share)
    ndp_wasted = np.where(~ucp_win, (1 - ucp_share) - 0.5, 1 - ucp_share)
    eg = float((ndp_wasted.sum() - ucp_wasted.sum()) / n)
    mm = float(np.median(ucp_share) - np.mean(ucp_share))
    R = int(ucp_win.sum())
    D = n - R
    if R == 0 or D == 0:
        decl = float("nan")
    else:
        ndp_won = np.sort(ucp_share)[:D]
        ucp_won = np.sort(ucp_share)[D:]
        theta_R = math.atan2(float(np.mean(ucp_won)) - 0.5, R / (2 * n))
        theta_D = math.atan2(0.5 - float(np.mean(ndp_won)), D / (2 * n))
        decl = (2.0 / math.pi) * (theta_R - theta_D)
    swing = 0.5 - float(np.mean(ucp_share))
    pb = float(((ucp_share + swing) > 0.5).mean()) - 0.5
    return {"EG_ours": eg, "MM_ours": mm, "Declination_ours": decl, "PB_ours": pb}


# ---------------------------------------------------------------------------
# Run all gerrymetrics functions on ndp_share = 1 - ucp_share
# ---------------------------------------------------------------------------


def _gm_metrics(ucp_share: np.ndarray) -> dict:
    vs = 1 - ucp_share  # NDP share; NDP plays "Dem" role

    eg_std = gm.EG(vs)
    eg_diff = gm.EG_difference(vs)
    eg_loss = gm.EG_loss_only(vs)
    eg_surp = gm.EG_surplus_only(vs)
    eg_vc1 = gm.EG_vote_centric(vs)
    eg_vc2 = gm.EG_vote_centric_two(vs)
    tau_0 = gm.tau_gap(vs, tau=0)  # tau=0 ≈ 2×EG (see Veomett 2018)
    tau_1 = gm.tau_gap(vs, tau=1)
    mm_gm = gm.mean_median(vs)
    pb_gm = gm.partisan_bias(vs)
    # Declination: negate to match our positive = UCP-favoured convention
    decl_gm = -gm.declination(vs)
    bdec_gm = -gm.bdec(vs)

    tt = gm.t_test(vs)  # t_test: d=NDP, r=UCP
    mw = gm.mann_whitney_u(vs)

    # t-test diff is (NDP_mean_margin - UCP_mean_margin); negate → UCP-favoured sign
    t_diff = -(tt["diff"]) if isinstance(tt, dict) else float("nan")
    t_p = tt["p"] if isinstance(tt, dict) else float("nan")
    mw_stat = -(mw["test_statistic"]) if isinstance(mw, dict) else float("nan")
    mw_p = mw["p"] if isinstance(mw, dict) else float("nan")

    return {
        "EG_gm": float(eg_std),
        "EG_diff_gap": float(eg_diff),
        "EG_loss_only": float(eg_loss),
        "EG_surplus": float(eg_surp),
        "EG_vote_centric": float(eg_vc1),
        "EG_vote_centric2": float(eg_vc2),
        "tau_gap_0": float(tau_0),
        "tau_gap_1": float(tau_1),
        "MM_gm": float(mm_gm),
        "PB_gm": float(pb_gm),
        "Declination_gm": float(decl_gm),
        "Bdec_gm": float(bdec_gm),
        "t_diff_UCP_adj": float(t_diff),  # positive = UCP wins by larger margins
        "t_p": float(t_p),
        "mw_stat_UCP_adj": float(mw_stat),  # positive = UCP wins by larger margins
        "mw_p": float(mw_p),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    print("[gerrymetrics comparison] Loading data...")
    va = gpd.read_file(VA_PATH)
    maj = gpd.read_file(MAJ_V7)
    mn = gpd.read_file(MIN_V7)

    print("\nBuilding district vote shares...")
    shares = {
        "2019_enacted": districts_from_2019(va),
        "majority_2026": districts_from_v7(va, maj, "majority v0_7"),
        "minority_2026": districts_from_v7(va, mn, "minority v0_7"),
    }

    print("\n=== CROSS-VALIDATION: our metrics vs gerrymetrics ===")
    results = {}
    for label, ucp_share in shares.items():
        our = _our_metrics(ucp_share)
        them = _gm_metrics(ucp_share)
        results[label] = {**our, **them}

        print(f"\n  {label} (n={len(ucp_share)})")
        print(
            f"    EG:          ours={our['EG_ours']:+.6f}  gm={them['EG_gm']:+.6f}  "
            f"diff={our['EG_ours']-them['EG_gm']:+.2e}"
        )
        print(
            f"    MM:          ours={our['MM_ours']:+.6f}  gm={them['MM_gm']:+.6f}  "
            f"diff={our['MM_ours']-them['MM_gm']:+.2e}"
        )
        print(
            f"    Declination: ours={our['Declination_ours']:+.6f}  "
            f"gm(adj)={them['Declination_gm']:+.6f}  "
            f"diff={our['Declination_ours']-them['Declination_gm']:+.2e}"
        )
        print(
            f"    PB:          ours={our['PB_ours']:+.6f}  gm={them['PB_gm']:+.6f}  "
            f"diff={our['PB_ours']-them['PB_gm']:+.2e}"
        )

    print("\n=== EG VARIANT FAMILY (positive = UCP-favoured) ===")
    col_w = 20
    hdr = f"{'Metric':<{col_w}} {'2019':>10} {'Majority':>10} {'Minority':>10}"
    print(hdr)
    print("-" * len(hdr))
    eg_variants = [
        ("EG_ours", "EG (ours)"),
        ("EG_gm", "EG (gm cross-check)"),
        ("EG_diff_gap", "Difference gap"),
        ("EG_loss_only", "Loss gap"),
        ("EG_surplus", "Surplus gap"),
        ("EG_vote_centric", "Vote-centric gap"),
        ("EG_vote_centric2", "Vote-centric gap 2"),
        ("tau_gap_0", "Tau gap (τ=0, ≈2×EG)"),
        ("tau_gap_1", "Tau gap (τ=1)"),
    ]
    for key, label in eg_variants:
        vals = [
            results[m].get(key, float("nan"))
            for m in ["2019_enacted", "majority_2026", "minority_2026"]
        ]
        print(
            f"  {label:<{col_w-2}} {vals[0]:>+10.4f} {vals[1]:>+10.4f} {vals[2]:>+10.4f}"
        )

    print("\n=== ALL METRICS SIDE-BY-SIDE ===")
    for label in ["2019_enacted", "majority_2026", "minority_2026"]:
        r = results[label]
        print(f"\n  {label}")
        for k, v in r.items():
            print(f"    {k:<22s}: {v:+.6f}")

    # Mann-Whitney summary
    print("\n=== LOPSIDED MARGINS: t-test vs Mann-Whitney ===")
    for label in ["2019_enacted", "majority_2026", "minority_2026"]:
        r = results[label]
        print(
            f"  {label}: t_diff={r['t_diff_UCP_adj']:+.4f}(p={r['t_p']:.4f})  "
            f"mw_stat={r['mw_stat_UCP_adj']:+.1f}(p={r['mw_p']:.4f})"
        )

    # JSON output
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=float)
    print(f"\nWrote {OUT_JSON}")

    # Markdown report
    labels = ["2019_enacted", "majority_2026", "minority_2026"]
    md = [
        "# gerrymetrics Cross-Validation & EG Variant Family",
        "",
        "All metrics computed with equal-turnout assumption. "
        "Sign convention: **positive = UCP-favoured** throughout.",
        "gerrymetrics input: `ndp_share = 1 − ucp_share` (NDP plays 'Dem' role). "
        "Declination and lopsided-margins test statistics negated to match sign convention.",
        "",
        "## Cross-validation: our implementation vs gerrymetrics",
        "",
        "| Metric | Map | Ours | gerrymetrics | Difference |",
        "|---|---|---|---|---|",
    ]
    for label in labels:
        r = results[label]
        for our_k, gm_k, name in [
            ("EG_ours", "EG_gm", "EG"),
            ("MM_ours", "MM_gm", "Mean-median"),
            ("Declination_ours", "Declination_gm", "Declination (adj)"),
            ("PB_ours", "PB_gm", "Partisan bias"),
        ]:
            diff = r[our_k] - r[gm_k]
            md.append(
                f"| {name} | {label} | {r[our_k]:+.5f} | {r[gm_k]:+.5f} "
                f"| {diff:+.2e} |"
            )

    md += [
        "",
        "## EG variant family",
        "",
        "| Metric | 2019 enacted | Majority 2026 | Minority 2026 |",
        "|---|---|---|---|",
    ]
    for key, label_str in eg_variants:
        vals = [results[m].get(key, float("nan")) for m in labels]
        md.append(f"| {label_str} | {vals[0]:+.4f} | {vals[1]:+.4f} | {vals[2]:+.4f} |")

    md += [
        "",
        "## Lopsided margins: t-test (Wang 2016) vs Mann-Whitney U",
        "",
        "| Map | t-test diff (adj) | t-test p | Mann-Whitney stat (adj) | MW p |",
        "|---|---|---|---|---|",
    ]
    for label in labels:
        r = results[label]
        md.append(
            f"| {label} | {r['t_diff_UCP_adj']:+.4f} | {r['t_p']:.4f} "
            f"| {r['mw_stat_UCP_adj']:+.0f} | {r['mw_p']:.4f} |"
        )

    md.append(
        "\n_Note: positive t-diff and MW-stat = UCP wins by larger margins than NDP "
        "(packing/cracking signal if combined with seat asymmetry)._"
    )
    md.append(
        f"\n_Generated {time.strftime('%Y-%m-%d %H:%M')} — elapsed "
        f"{time.time()-t0:.0f}s_"
    )

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"\nDone in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
