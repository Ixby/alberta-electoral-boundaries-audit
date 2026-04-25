"""
v0_1_cross_election_v8_full.py

2019-vote cross-election re-check against v0_8 full-coverage geometry.

The earlier cross-election test (v0_1_2015_cross_election.py) ran against
the v0_7 partial-coverage geometry and produced an EG sign-flip when 2019
votes were used instead of 2023 votes. The §1.2 caveat 3 in the monograph
records this as evidence the EG direction is sensitive to which electorate
is asked.

This script re-runs the same test against the v0_8 full-coverage geometry
(89/89 EDs both maps via 2019-Tier-A inheritance fill). The hypothesis is
that the direction-flip might persist (genuine vote-distribution
sensitivity) or disappear (was a partial-coverage artefact).

Methodology:
  1. Load v0_8_full_refined for both 2026 maps + 2019 enacted shapefile.
  2. Spatial-attribute 2023 VA votes to each map.
  3. Spatial-attribute 2019 VA votes to each map (same VAs, different
     vote totals).
  4. Compute EG, MM, declination, seats@50/50 for each (map, election)
     combination.
  5. Report direction stability per metric.

Outputs:
  data/v0_1_cross_election_v8_full.csv
  data/v0_1_cross_election_v8_full.json

Forward:  monograph §1.2 caveat 3 (cross-election direction reversal)
Backward: gerrychain ensemble script + va_polygons_with_2023_votes.gpkg +
          va_polygons_with_2019_votes.gpkg
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _perf_utils import Timer, ts  # noqa: E402

ROOT = HERE.parent.parent
DATA = ROOT / "data"
DERIVED = DATA / "shapefiles" / "derived"

VA_2023 = DERIVED / "va_polygons_with_2023_votes.gpkg"
ED_2019_SHP = DATA / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp"
VOTES_2019_CSV = DATA / "v0_1_alberta_2019_results.csv"

OUT_CSV = DATA / "v0_1_cross_election_v8_full.csv"
OUT_JSON = DATA / "v0_1_cross_election_v8_full.json"


def _pick_v8(plan: str) -> Path:
    for fname in (
        f"v0_8_full_refined_{plan}_2026_eds.gpkg",
        f"v0_8_refined_{plan}_2026_eds.gpkg",
        f"v0_8_canonical_{plan}_2026_eds.gpkg",
    ):
        p = DERIVED / fname
        if p.exists():
            return p
    raise FileNotFoundError(f"No v0_8 GPKG for {plan}")


def seat_results(ucp: np.ndarray, ndp: np.ndarray) -> dict:
    """Compute the four primary partisan-bias metrics."""
    total = ucp + ndp
    ucp_share_per_d = np.where(total > 0, ucp / total, 0.5)
    won = ucp > ndp
    n = len(ucp)
    ucp_seats = int(won.sum())
    margin_majority = (n + 1) // 2

    # Efficiency gap: wasted-vote definition
    wasted_ucp = np.where(won, ucp - ((total // 2) + 1), ucp)
    wasted_ndp = np.where(won, ndp, ndp - ((total // 2) + 1))
    total_votes = total.sum()
    eg = (wasted_ndp.sum() - wasted_ucp.sum()) / max(total_votes, 1)

    # Mean-median (UCP share)
    mm = float(np.mean(ucp_share_per_d) - np.median(ucp_share_per_d))

    # Declination (Warrington 2018)
    win_shares = ucp_share_per_d[won]
    loss_shares = ucp_share_per_d[~won]
    if len(win_shares) > 0 and len(loss_shares) > 0:
        win_mean = float(np.mean(win_shares))
        loss_mean = float(np.mean(loss_shares))
        n_win = len(win_shares)
        n_loss = len(loss_shares)
        if n_win + n_loss > 0:
            theta_w = np.arctan((win_mean - 0.5) / (n_win / (n_win + n_loss)))
            theta_l = np.arctan((0.5 - loss_mean) / (n_loss / (n_win + n_loss)))
            declination = float(2 * (theta_w - theta_l) / np.pi)
        else:
            declination = float("nan")
    else:
        declination = float("nan")

    # Seats @ 50/50: simulate uniform shift to provincial 50/50
    ucp_share_global = float(ucp.sum() / max(total_votes, 1))
    shift = 0.5 - ucp_share_global
    shifted_share = np.clip(ucp_share_per_d + shift, 0, 1)
    s50 = float((shifted_share > 0.5).sum() / n)

    return {
        "ucp_seats": ucp_seats,
        "n_districts": n,
        "ucp_vote_share": ucp_share_global,
        "efficiency_gap": float(eg),
        "mean_median": mm,
        "declination": declination,
        "seats_at_50_50": s50,
    }


def attribute_va_to_eds(va: gpd.GeoDataFrame, eds: gpd.GeoDataFrame,
                        ucp_col: str, ndp_col: str) -> tuple:
    """Spatial-join VA centroids into ED polygons; aggregate UCP/NDP per ED."""
    va_pts = gpd.GeoDataFrame(
        {ucp_col: va[ucp_col].fillna(0).values,
         ndp_col: va[ndp_col].fillna(0).values},
        geometry=va.geometry.centroid.values,
        crs=va.crs,
    )
    if va_pts.crs != eds.crs:
        va_pts = va_pts.to_crs(eds.crs)
    name_col = "name_2026" if "name_2026" in eds.columns else eds.columns[0]
    joined = gpd.sjoin(va_pts, eds[[name_col, "geometry"]],
                       how="inner", predicate="within")
    agg = joined.groupby(name_col).agg(
        ucp=(ucp_col, "sum"), ndp=(ndp_col, "sum")
    ).reset_index()
    return agg["ucp"].values.astype(float), agg["ndp"].values.astype(float)


def attribute_2019_to_v8_by_area(eds_2019: gpd.GeoDataFrame,
                                  votes_by_2019_ed: dict,
                                  v8: gpd.GeoDataFrame) -> tuple:
    """For each v0_8 ED, sum 2019 votes weighted by the area-overlap
    fraction with each 2019 ED whose UCP/NDP totals we have."""
    if eds_2019.crs != v8.crs:
        eds_2019 = eds_2019.to_crs(v8.crs)
    name_col = "name_2026" if "name_2026" in v8.columns else v8.columns[0]
    ed_2019_name_col = "ed_name" if "ed_name" in eds_2019.columns else "EDName2017"

    # Area of each 2019 ED (used as denominator for the fraction)
    eds_2019 = eds_2019.copy()
    eds_2019["_area_2019"] = eds_2019.geometry.area

    ucp_per_v8 = {n: 0.0 for n in v8[name_col]}
    ndp_per_v8 = {n: 0.0 for n in v8[name_col]}

    sindex = eds_2019.sindex
    for v8_row in v8.itertuples():
        v8_geom = v8_row.geometry
        v8_name = getattr(v8_row, name_col)
        for cand_idx in sindex.intersection(v8_geom.bounds):
            ed_2019 = eds_2019.iloc[int(cand_idx)]
            try:
                inter = v8_geom.intersection(ed_2019.geometry)
            except Exception:
                continue
            if inter.is_empty:
                continue
            frac = inter.area / max(ed_2019["_area_2019"], 1)
            ed_2019_name = ed_2019[ed_2019_name_col]
            v = votes_by_2019_ed.get(ed_2019_name)
            if v is None:
                continue
            ucp_per_v8[v8_name] += frac * v[0]
            ndp_per_v8[v8_name] += frac * v[1]

    ucp = np.array([ucp_per_v8[n] for n in v8[name_col]])
    ndp = np.array([ndp_per_v8[n] for n in v8[name_col]])
    return ucp, ndp


def main() -> int:
    with Timer("[v0_8 cross-election re-check]"):
        # Load 2023 (VA-level)
        print(f"  loading 2023 VA votes from {VA_2023.name}", flush=True)
        va_2023 = gpd.read_file(VA_2023)

        # Load 2019 (ED-level) — apportion via area-overlap to v0_8 polygons
        print(f"  loading 2019 ED-level votes from {VOTES_2019_CSV.name} + "
              f"{ED_2019_SHP.name}", flush=True)
        votes_2019 = pd.read_csv(VOTES_2019_CSV)
        # Sum candidate votes by party — UCP and NDP columns are spread across cand_1..8
        votes_by_2019_ed = {}
        for _, row in votes_2019.iterrows():
            ed = str(row["ed_name"]).strip()
            ucp = 0.0
            ndp = 0.0
            for i in range(1, 9):
                cand = str(row.get(f"cand_{i}", ""))
                vc = row.get(f"votes_{i}", 0)
                vc = float(vc) if pd.notna(vc) and vc != "" else 0.0
                if "(UCP)" in cand:
                    ucp += vc
                elif "(NDP)" in cand:
                    ndp += vc
            votes_by_2019_ed[ed] = (ucp, ndp)
        print(f"  loaded 2019 votes for {len(votes_by_2019_ed)} 2019 EDs",
              flush=True)

        eds_2019 = gpd.read_file(ED_2019_SHP)
        if eds_2019.crs.to_epsg() != 3401:
            eds_2019 = eds_2019.to_crs(3401)
        print(f"  loaded {len(eds_2019)} 2019 enacted polygons CRS={eds_2019.crs}",
              flush=True)

        results = []
        for plan in ("majority", "minority"):
            v8_path = _pick_v8(plan)
            print(f"\n  === {plan} (source: {v8_path.name}) ===", flush=True)
            eds = gpd.read_file(v8_path)
            if eds.crs.to_epsg() != 3401:
                eds = eds.to_crs(3401)

            # 2019: area-proportional attribution from 2019 enacted polygons
            t0 = time.time()
            ucp19, ndp19 = attribute_2019_to_v8_by_area(eds_2019, votes_by_2019_ed, eds)
            m19 = seat_results(ucp19, ndp19)
            m19["map"] = plan
            m19["election"] = "2019"
            m19["attribution"] = "area-proportional from 2019 enacted polygons"
            results.append(m19)
            print(f"    2019 → seats={m19['ucp_seats']}/{m19['n_districts']}  "
                  f"EG={m19['efficiency_gap']:+.4f}  MM={m19['mean_median']:+.4f}  "
                  f"decl={m19['declination']:+.4f}  s50={m19['seats_at_50_50']:.3f}  "
                  f"({time.time()-t0:.1f}s)", flush=True)

            # 2023: VA-centroid attribution
            t0 = time.time()
            ucp23, ndp23 = attribute_va_to_eds(va_2023, eds, "va_ucp", "va_ndp")
            m23 = seat_results(ucp23, ndp23)
            m23["map"] = plan
            m23["election"] = "2023"
            m23["attribution"] = "VA-centroid in v0_8 polygon"
            results.append(m23)
            print(f"    2023 → seats={m23['ucp_seats']}/{m23['n_districts']}  "
                  f"EG={m23['efficiency_gap']:+.4f}  MM={m23['mean_median']:+.4f}  "
                  f"decl={m23['declination']:+.4f}  s50={m23['seats_at_50_50']:.3f}  "
                  f"({time.time()-t0:.1f}s)", flush=True)

        df = pd.DataFrame(results)
        df.to_csv(OUT_CSV, index=False)
        with open(OUT_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=float)
        print(f"\n  wrote {OUT_CSV.name} and {OUT_JSON.name}", flush=True)

        # Direction-stability summary
        print("\n=== DIRECTION STABILITY (2019 vs 2023, per map per metric) ===")
        for plan in ("majority", "minority"):
            for metric in ("efficiency_gap", "mean_median", "declination", "seats_at_50_50"):
                rows = [r for r in results if r["map"] == plan]
                if len(rows) < 2:
                    continue
                v_2019 = next((r[metric] for r in rows if r["election"] == "2019"), None)
                v_2023 = next((r[metric] for r in rows if r["election"] == "2023"), None)
                if v_2019 is None or v_2023 is None:
                    continue
                same_sign = (v_2019 >= 0) == (v_2023 >= 0)
                tag = "STABLE" if same_sign else "DIRECTION-FLIP"
                print(f"  {plan:<10s} {metric:<18s} 2019={v_2019:+.4f}  "
                      f"2023={v_2023:+.4f}  {tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
