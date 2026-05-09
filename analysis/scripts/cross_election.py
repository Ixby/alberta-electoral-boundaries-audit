# Version: v0.9
from __future__ import annotations
"""
cross_election.py
======================
Three-election (2015 / 2019 / 2023) Lane-1 metric re-computation against
the v0_9 topological substrate, both minority and majority maps.

The pre-registration committed to a cross-election robustness check: does
the minority's outlier status hold when the same map is scored against
2015 and 2019 votes, or is it a 2023-only artefact? Until now the audit
shipped only a 2019/2023 two-election check on the v0_8 substrate
(`cross_election_v8_full.py`); 2015 and v0_9 were silently dropped. This
script fires that gun.

Method
------
For each election year:
  - 2023: VA-centroid attribution from `va_polygons_with_2023_votes.gpkg`
    into v0_9 polygons (same as cross_election_v8_full.py).
  - 2019: ED-level totals from `alberta_2019_results.csv` projected
    onto v0_9 polygons by area-overlap from the 2019 enacted shapefile
    (same area-proportional method as the v0_8 cross-election test).
  - 2015: ED-level 2015 totals from `alberta_2015_results.csv`
    re-attributed to 2019 boundaries via `2015_to_2019_crosswalk.csv`
    (population_weight; same logic as 2015_cross_election.py), then
    area-overlapped onto v0_9 polygons via the 2019 enacted shapefile.

For each (year, map) we compute the four Lane-1 metrics via the same
`seat_results()` shape used by `mcmc_ensemble.py:seat_results()`:
efficiency_gap, mean_median, declination, seats_at_50_50.

For each year we then compute the minority's percentile in the existing
100k 2023-trained ReCom ensemble (data/simulated_ensemble_raw_samples_250k.csv)
on `seats_at_50_50`. The 100k ensemble is trained on 2023 votes — comparing
2015 / 2019 minority s50 against it is *not* a clean significance test
(the ensemble would need to be re-scored under each vote year for that),
but it is the comparison the directive specifies, and we report it
honestly with that caveat.

We also re-run `338canada_historical.py` to capture its outputs, but the
Lane-1 cross-election test does not depend on 338's projections — it uses
real Elections Alberta vote totals. The 338 outputs are referenced in the
verdict memo as a separate stability probe.

Outputs
-------
  data/cross_election_per_map.csv
  data/cross_election_per_map.json

Forward:  analysis/reports/cross_election_robustness.md
Backward:
  data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
  data/alberta_2019_results.csv
  data/alberta_2015_results.csv
  data/2015_to_2019_crosswalk.csv
  data/simulated_ensemble_raw_samples_250k.csv  (100k post-audit ensemble)
"""

# Version: 0.9 series  (last updated 2026-04-26)


import sys
import logging
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


import csv
import json
import math
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
logger = logging.getLogger(__name__)
DATA = data_loader._resolve_path("data")
DERIVED = DATA / "shapefiles" / "derived"

V0_9_MIN = DERIVED / "v0_10_topological_minority_2026_eds.gpkg"
V0_9_MAJ = DERIVED / "v0_10_topological_majority_2026_eds.gpkg"
VA_2023 = DERIVED / "va_polygons_with_2023_votes.gpkg"
ED_2019_SHP = (
    DATA
    / "shapefiles"
    / "reference"
    / "alberta_2019_eds"
    / "EDS_ENACTED_BILL33_15DEC2017.shp"
)

VOTES_2019_CSV = DATA / "alberta_2019_results.csv"
VOTES_2015_CSV = DATA / "alberta_2015_results.csv"
CROSSWALK_2015_TO_2019 = DATA / "2015_to_2019_crosswalk.csv"

ENSEMBLE_SAMPLES = DATA / "simulated_ensemble_raw_samples_250k.csv"

OUT_CSV = DATA / "cross_election_per_map.csv"
OUT_JSON = DATA / "cross_election_per_map.json"


# ---------------------------------------------------------------------
# Lane-1 metrics — clone of mcmc_ensemble.seat_results() exactly so the
# numbers comparable to the ensemble are identical in formula.
# ---------------------------------------------------------------------


def seat_results(ucp: np.ndarray, ndp: np.ndarray) -> dict:
    """Identical metric definitions to mcmc_ensemble.py:seat_results().
    Sign conventions: positive EG = UCP-favoured; positive MM = UCP-
    favoured; NEGATIVE declination = UCP-favoured; seats_at_50_50 is
    UCP fraction of seats under uniform-swing to 50/50.
    """
    ucp = np.asarray(ucp, dtype=float)
    ndp = np.asarray(ndp, dtype=float)
    total = ucp + ndp
    mask = total > 0
    ucp = ucp[mask]
    ndp = ndp[mask]
    total = total[mask]
    n = len(ucp)
    if n == 0:
        return dict(
            efficiency_gap=float("nan"),
            mean_median=float("nan"),
            declination=float("nan"),
            seats_at_50_50=float("nan"),
            ucp_seats=float("nan"),
            n_districts=0,
            ucp_vote_share=float("nan"),
        )

    two_party_total = ucp + ndp
    two_party_total = np.where(two_party_total == 0, 1.0, two_party_total)
    ucp_share = ucp / two_party_total
    ucp_win = ucp > ndp
    ucp_wins = int(ucp_win.sum())

    ucp_wasted = np.where(ucp_win, ucp - two_party_total / 2, ucp)
    ndp_wasted = np.where(~ucp_win, ndp - two_party_total / 2, ndp)
    eg = (ndp_wasted.sum() - ucp_wasted.sum()) / two_party_total.sum()

    mean_median = float(np.median(ucp_share) - np.mean(ucp_share))

    R = ucp_wins
    D = n - R
    if R == 0 or D == 0:
        declination = float("nan")
    else:
        sorted_shares = np.sort(ucp_share)
        ndp_won = sorted_shares[:D]
        ucp_won = sorted_shares[D:]
        mean_ucp_in_ucp_won = float(np.mean(ucp_won))
        mean_ucp_in_ndp_won = float(np.mean(ndp_won))
        theta_R = math.atan2(mean_ucp_in_ucp_won - 0.5, R / (2 * n))
        theta_D = math.atan2(0.5 - mean_ucp_in_ndp_won, D / (2 * n))
        declination = (2.0 / math.pi) * (theta_R - theta_D)

    province_ucp = ucp.sum() / two_party_total.sum()
    swing = 0.5 - province_ucp
    shifted = np.clip(ucp_share + swing, 0.0, 1.0)
    wins = (shifted > 0.5 + 1e-9).sum()
    ties = (np.abs(shifted - 0.5) <= 1e-9).sum()
    ucp_wins_at_50 = float(wins + 0.5 * ties)
    seats_at_50_50 = ucp_wins_at_50 / n

    return dict(
        efficiency_gap=float(eg),
        mean_median=float(mean_median),
        declination=float(declination) if not np.isnan(declination) else float("nan"),
        seats_at_50_50=float(seats_at_50_50),
        ucp_seats=int(ucp_wins),
        n_districts=int(n),
        ucp_vote_share=float(province_ucp),
    )


# ---------------------------------------------------------------------
# Vote-loading helpers
# ---------------------------------------------------------------------


def load_2019_ed_votes() -> dict[str, tuple[float, float]]:
    """Return {ed_2019_name: (ucp, ndp)} from the parsed 2019 CSV."""
    votes = pd.read_csv(VOTES_2019_CSV)
    out: dict[str, tuple[float, float]] = {}
    for _, row in votes.iterrows():
        ed = str(row["ed_name"]).strip()
        ucp = ndp = 0.0
        for i in range(1, 9):
            cand = str(row.get(f"cand_{i}", "")) or ""
            vc = row.get(f"votes_{i}", 0)
            try:
                vc = float(vc) if pd.notna(vc) and vc != "" else 0.0
            except (TypeError, ValueError):
                vc = 0.0
            if "(UCP)" in cand:
                ucp += vc
            elif "(NDP)" in cand:
                ndp += vc
        out[ed] = (ucp, ndp)
    return out


def _clean_2015_ed_name(name: str) -> str:
    if name.startswith("Statement Of Results By Poll - "):
        return name[len("Statement Of Results By Poll - ") :]
    return name


def load_2015_to_2019_attributed() -> dict[str, tuple[float, float]]:
    """Return {ed_2019_name: (ucp_equiv, ndp)} via the 2015->2019
    crosswalk with population_weight as the re-attribution weight.
    UCP-equivalent = PC + Wildrose at the 2015 ED level (per
    parse_2015_results.py and 2015_cross_election.py).
    """
    by_2015: dict[str, dict[str, int]] = {}
    with open(VOTES_2015_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            name = _clean_2015_ed_name(r["ed_2015"])
            by_2015[name] = {
                "ndp": int(r["ndp"]),
                "ucp_equiv": int(r["ucp_equiv"]),
            }

    accum: dict[str, dict[str, float]] = defaultdict(lambda: {"ucp": 0.0, "ndp": 0.0})
    with open(CROSSWALK_2015_TO_2019, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ed_2015 = r["ed_2015_2010boundaries"]
            ed_2019 = r["ed_2019_2017boundaries"]
            w = float(r["population_weight"])
            src = by_2015.get(ed_2015)
            if not src:
                continue
            accum[ed_2019]["ucp"] += src["ucp_equiv"] * w
            accum[ed_2019]["ndp"] += src["ndp"] * w

    return {ed: (vals["ucp"], vals["ndp"]) for ed, vals in accum.items()}


# ---------------------------------------------------------------------
# Spatial attribution
# ---------------------------------------------------------------------


def attribute_va_2023_centroid(
    va: gpd.GeoDataFrame, eds: gpd.GeoDataFrame
) -> tuple[np.ndarray, np.ndarray]:
    """VA-centroid spatial-join into v0_9 polygons; aggregate UCP/NDP."""
    va_pts = gpd.GeoDataFrame(
        {
            "va_ucp": va["va_ucp"].fillna(0).values,
            "va_ndp": va["va_ndp"].fillna(0).values,
        },
        geometry=va.geometry.centroid.values,
        crs=va.crs,
    )
    if va_pts.crs != eds.crs:
        va_pts = va_pts.to_crs(eds.crs)
    name_col = "name_2026"
    joined = gpd.sjoin(
        va_pts, eds[[name_col, "geometry"]], how="inner", predicate="within"
    )
    agg = (
        joined.groupby(name_col)
        .agg(ucp=("va_ucp", "sum"), ndp=("va_ndp", "sum"))
        .reset_index()
    )
    # Reindex to map order so ED ordering is canonical
    eds_order = eds[name_col].values
    by_name = agg.set_index(name_col)
    by_name = by_name.reindex(eds_order, fill_value=0.0)
    return by_name["ucp"].values.astype(float), by_name["ndp"].values.astype(float)


def attribute_2019_ed_to_v0_9_by_area(
    eds_2019: gpd.GeoDataFrame,
    votes_by_2019_ed: dict,
    target: gpd.GeoDataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    """Apportion 2019-ED-level (UCP, NDP) totals to v0_9 polygons by
    area-overlap fraction of the 2019 ED that falls inside each target
    polygon.
    """
    if eds_2019.crs != target.crs:
        eds_2019 = eds_2019.to_crs(target.crs)
    target_name_col = "name_2026"
    ed_2019_name_col = "ed_name" if "ed_name" in eds_2019.columns else "EDName2017"

    eds_2019 = eds_2019.copy()
    eds_2019["_area_2019"] = eds_2019.geometry.area

    ucp_per: dict[str, float] = {n: 0.0 for n in target[target_name_col]}
    ndp_per: dict[str, float] = {n: 0.0 for n in target[target_name_col]}

    sindex = eds_2019.sindex
    for v_row in target.itertuples():
        v_geom = v_row.geometry
        v_name = getattr(v_row, target_name_col)
        for cand_idx in sindex.intersection(v_geom.bounds):
            ed_2019 = eds_2019.iloc[int(cand_idx)]
            try:
                inter = v_geom.intersection(ed_2019.geometry)
            except Exception as e:
                logger.debug("geometry intersection skipped: %s", e)
                continue
            if inter.is_empty:
                continue
            frac = inter.area / max(ed_2019["_area_2019"], 1)
            ed_2019_name = ed_2019[ed_2019_name_col]
            v = votes_by_2019_ed.get(ed_2019_name)
            if v is None:
                continue
            ucp_per[v_name] += frac * v[0]
            ndp_per[v_name] += frac * v[1]

    eds_order = target[target_name_col].values
    ucp = np.array([ucp_per[n] for n in eds_order], dtype=float)
    ndp = np.array([ndp_per[n] for n in eds_order], dtype=float)
    return ucp, ndp


# ---------------------------------------------------------------------
# Ensemble percentile
# ---------------------------------------------------------------------


def ensemble_percentile(value: float, ensemble_values: np.ndarray) -> float:
    """Return percentile of value in the ensemble (fraction of ensemble
    samples strictly less than value, * 100)."""
    if math.isnan(value):
        return float("nan")
    return float((ensemble_values < value).mean() * 100.0)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def maybe_run_338_historical() -> None:
    """Re-run the 338canada_historical.py pipeline to refresh outputs.
    Failures are non-fatal — the cross-election test does not depend on
    338's projections — but we attempt the run so the directive's
    capture-the-outputs requirement is met.
    """
    script = ROOT / "analysis" / "scripts" / "338canada_historical.py"
    print("\n--- attempting to re-run 338canada_historical.py ---")
    if not script.exists():
        print(f"  script missing at {script}")
        return
    import subprocess

    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=600,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        if proc.returncode != 0:
            print(f"  338 re-run exit code {proc.returncode}")
        # Show only the last 40 lines of stdout for log brevity
        out_tail = "\n".join((proc.stdout or "").splitlines()[-40:])
        print(out_tail)
    except subprocess.TimeoutExpired:
        print("  338 re-run timed out (10 min) — using existing cached outputs")
    except Exception as e:
        print(f"  338 re-run errored: {e}")


def main() -> int:
    t_start = time.time()
    print("=" * 72)
    print(" v0_9 CROSS-ELECTION (2015 / 2019 / 2023) — Lane 1 metrics")
    print("=" * 72)

    # Load v0_9 polygons
    print(f"\nLoading {V0_9_MIN.name} ...")
    v9_min = gpd.read_file(V0_9_MIN)
    print(f"  {len(v9_min)} EDs, CRS={v9_min.crs}")
    print(f"Loading {V0_9_MAJ.name} ...")
    v9_maj = gpd.read_file(V0_9_MAJ)
    print(f"  {len(v9_maj)} EDs, CRS={v9_maj.crs}")

    # Load 2019 enacted shapefile (used for 2015 + 2019 area attribution)
    print(f"\nLoading 2019 enacted polygons ({ED_2019_SHP.name}) ...")
    eds_2019 = gpd.read_file(ED_2019_SHP)
    if eds_2019.crs != v9_min.crs:
        eds_2019 = eds_2019.to_crs(v9_min.crs)
    print(f"  {len(eds_2019)} 2019 enacted polygons")

    # Load 2023 VA polygons
    print(f"\nLoading 2023 VA polygons ({VA_2023.name}) ...")
    va_2023 = gpd.read_file(VA_2023)
    print(f"  {len(va_2023)} VAs")

    # Load vote tables
    print(f"\nLoading 2019 ED-level votes ...")
    votes_2019 = load_2019_ed_votes()
    print(f"  {len(votes_2019)} 2019 EDs with vote totals")

    print(f"Loading 2015 votes (re-attributed to 2019 boundaries via crosswalk) ...")
    votes_2015_on_2019 = load_2015_to_2019_attributed()
    n_eds_2015 = len(votes_2015_on_2019)
    print(f"  {n_eds_2015} 2019-boundary EDs after 2015 re-attribution")

    # Compute per (year, map)
    results: list[dict] = []
    metric_cols = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]

    for plan, target in (("majority", v9_maj), ("minority", v9_min)):
        print(f"\n=== {plan} (v0_9) ===")

        # 2015
        t0 = time.time()
        ucp15, ndp15 = attribute_2019_ed_to_v0_9_by_area(
            eds_2019, votes_2015_on_2019, target
        )
        m15 = seat_results(ucp15, ndp15)
        m15.update(
            {
                "map": plan,
                "election": "2015",
                "attribution": "2015->2019 crosswalk -> area-overlap to v0_9",
            }
        )
        print(
            f"  2015 -> seats={m15['ucp_seats']}/{m15['n_districts']} "
            f"EG={m15['efficiency_gap']:+.4f} MM={m15['mean_median']:+.4f} "
            f"decl={m15['declination']:+.4f} s50={m15['seats_at_50_50']:.3f} "
            f"({time.time()-t0:.1f}s)"
        )
        results.append(m15)

        # 2019
        t0 = time.time()
        ucp19, ndp19 = attribute_2019_ed_to_v0_9_by_area(eds_2019, votes_2019, target)
        m19 = seat_results(ucp19, ndp19)
        m19.update(
            {
                "map": plan,
                "election": "2019",
                "attribution": "area-overlap from 2019 enacted polygons to v0_9",
            }
        )
        print(
            f"  2019 -> seats={m19['ucp_seats']}/{m19['n_districts']} "
            f"EG={m19['efficiency_gap']:+.4f} MM={m19['mean_median']:+.4f} "
            f"decl={m19['declination']:+.4f} s50={m19['seats_at_50_50']:.3f} "
            f"({time.time()-t0:.1f}s)"
        )
        results.append(m19)

        # 2023
        t0 = time.time()
        ucp23, ndp23 = attribute_va_2023_centroid(va_2023, target)
        m23 = seat_results(ucp23, ndp23)
        m23.update(
            {
                "map": plan,
                "election": "2023",
                "attribution": "VA-centroid in v0_9 polygon",
            }
        )
        print(
            f"  2023 -> seats={m23['ucp_seats']}/{m23['n_districts']} "
            f"EG={m23['efficiency_gap']:+.4f} MM={m23['mean_median']:+.4f} "
            f"decl={m23['declination']:+.4f} s50={m23['seats_at_50_50']:.3f} "
            f"({time.time()-t0:.1f}s)"
        )
        results.append(m23)

    # ----- Ensemble percentile (minority s50 vs 100k 2023 ensemble) -----
    print(f"\nLoading 100k 2023 ensemble samples for percentile placement ...")
    ens = pd.read_csv(ENSEMBLE_SAMPLES, usecols=["seats_at_50_50"])
    s50_ens = ens["seats_at_50_50"].values.astype(float)
    print(
        f"  ensemble n={len(s50_ens)}  mean s50={s50_ens.mean():.4f} "
        f"std={s50_ens.std():.4f} min={s50_ens.min():.4f} max={s50_ens.max():.4f}"
    )

    for r in results:
        r["s50_pct_in_2023_ensemble"] = ensemble_percentile(
            r["seats_at_50_50"], s50_ens
        )
        r["ensemble_n"] = int(len(s50_ens))

    # Save
    df = pd.DataFrame(results)
    cols = [
        "map",
        "election",
        "n_districts",
        "ucp_seats",
        "ucp_vote_share",
        "efficiency_gap",
        "mean_median",
        "declination",
        "seats_at_50_50",
        "s50_pct_in_2023_ensemble",
        "ensemble_n",
        "attribution",
    ]
    df = df[cols]
    df.to_csv(OUT_CSV, index=False)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=float)
    print(f"\nWrote {OUT_CSV}")
    print(f"Wrote {OUT_JSON}")

    # ----- Summary table -----
    print("\n" + "=" * 72)
    print(" SUMMARY TABLE")
    print("=" * 72)
    print(
        f"  {'year':<5s} {'maj_s50':>9s} {'min_s50':>9s} "
        f"{'min_pct_in_ens':>15s} {'maj_eg':>9s} {'min_eg':>9s} "
        f"{'maj_decl':>10s} {'min_decl':>10s}"
    )
    for year in ("2015", "2019", "2023"):
        row_maj = next(
            (r for r in results if r["map"] == "majority" and r["election"] == year),
            None,
        )
        row_min = next(
            (r for r in results if r["map"] == "minority" and r["election"] == year),
            None,
        )
        if row_maj is None or row_min is None:
            continue
        print(
            f"  {year:<5s} {row_maj['seats_at_50_50']:>9.4f} "
            f"{row_min['seats_at_50_50']:>9.4f} "
            f"{row_min['s50_pct_in_2023_ensemble']:>14.2f}% "
            f"{row_maj['efficiency_gap']:>+9.4f} "
            f"{row_min['efficiency_gap']:>+9.4f} "
            f"{row_maj['declination']:>+10.4f} "
            f"{row_min['declination']:>+10.4f}"
        )

    # ----- 338 historical re-run (best-effort, side outputs) -----
    maybe_run_338_historical()

    print(f"\nTotal time: {time.time()-t_start:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
