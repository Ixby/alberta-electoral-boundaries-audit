"""
v0.9 MAUP comparison — centroid vs area-weighted attribution.

For both 2026 maps (majority, minority), score Lane 1 metrics
(seats@50/50, efficiency_gap, mean_median, declination) under:
  (a) centroid-in-polygon attribution (existing baseline; uses
      mcmc_ensemble.score_exogenous_map → seat_results)
  (b) area-weighted attribution (this commit's
      va_attribution_area_weighted.py output CSVs)

Both branches converge on `seat_results(ucp, ndp)` from mcmc_ensemble.py
so the metric math is identical — only the per-ED ucp/ndp inputs change.

Output: prints a 4-row delta table and writes a JSON summary.

Type: project
Forward: analysis/reports/maup_centroid_sensitivity.md
Backward:
  analysis/scripts/va_attribution_area_weighted.py
  analysis/scripts/mcmc_ensemble.py
  data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg
  data/votes_2023_majority_area_weighted.csv
  data/votes_2023_minority_area_weighted.csv
"""


import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = data_loader._resolve_path("data")

sys.path.insert(0, str(HERE))
from mcmc_ensemble import seat_results, score_exogenous_map  # type: ignore

VA_PATH = DATA / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
MAJ_GPKG = DATA / "shapefiles" / "derived" / "v0_10_topological_majority_2026_eds.gpkg"
MIN_GPKG = DATA / "shapefiles" / "derived" / "v0_10_topological_minority_2026_eds.gpkg"
MAJ_AW_CSV = DATA / "votes_2023_majority_area_weighted.csv"
MIN_AW_CSV = DATA / "votes_2023_minority_area_weighted.csv"

OUT_JSON = DATA / "maup_centroid_sensitivity.json"


def metrics_centroid(va: gpd.GeoDataFrame, gpkg: Path) -> dict:
    m = score_exogenous_map(va, gpkg, id_col="name_2026")
    return {
        "seats_at_50_50": float(m["seats_at_50_50"]),
        "efficiency_gap": float(m["efficiency_gap"]),
        "mean_median": float(m["mean_median"]),
        "declination": float(m["declination"]),
        "ucp_seats": int(m["ucp_seats"]),
        "n_districts": int(m["n_districts"]),
        "ucp_vote_share": float(m["ucp_vote_share"]),
        "source": str(gpkg.name),
        "method": "centroid",
    }


def metrics_area_weighted(csv_path: Path) -> dict:
    df = pd.read_csv(csv_path)
    # Drop any districts with zero two-party total (shouldn't happen).
    ucp = df["ucp"].astype(float).values
    ndp = df["ndp"].astype(float).values
    m = seat_results(ucp, ndp)
    return {
        "seats_at_50_50": float(m["seats_at_50_50"]),
        "efficiency_gap": float(m["efficiency_gap"]),
        "mean_median": float(m["mean_median"]),
        "declination": float(m["declination"]),
        "ucp_seats": int(m["ucp_seats"]),
        "n_districts": int(m["n_districts"]),
        "ucp_vote_share": float(m["ucp_vote_share"]),
        "source": str(csv_path.name),
        "method": "area_weighted",
    }


def main():
    print("[v0.9 MAUP centroid vs area-weighted comparison]")
    print(f"  VA substrate    : {VA_PATH.name}")
    print(f"  Majority gpkg   : {MAJ_GPKG.name}")
    print(f"  Minority gpkg   : {MIN_GPKG.name}")

    va = gpd.read_file(VA_PATH)
    va["va_ndp"] = va["va_ndp"].fillna(0.0).astype(float)
    va["va_ucp"] = va["va_ucp"].fillna(0.0).astype(float)
    va["va_other"] = va["va_other"].fillna(0.0).astype(float)
    va["total_votes"] = va["va_ndp"] + va["va_ucp"] + va["va_other"]
    print(f"  loaded {len(va)} VAs")

    print("\n  scoring centroid attribution ...")
    maj_c = metrics_centroid(va, MAJ_GPKG)
    min_c = metrics_centroid(va, MIN_GPKG)

    print("  scoring area-weighted attribution ...")
    maj_a = metrics_area_weighted(MAJ_AW_CSV)
    min_a = metrics_area_weighted(MIN_AW_CSV)

    rows = []
    for label, c, a in [
        ("majority_2026", maj_c, maj_a),
        ("minority_2026", min_c, min_a),
    ]:
        for k in ["seats_at_50_50", "efficiency_gap", "mean_median", "declination"]:
            rows.append(
                {
                    "map": label,
                    "metric": k,
                    "centroid": c[k],
                    "area_weighted": a[k],
                    "delta": a[k] - c[k],
                }
            )
    table = pd.DataFrame(rows)

    # Print friendly table.
    print("\n" + "=" * 78)
    print("  4-ROW DELTA TABLE  (centroid vs area-weighted, both v0_9 maps)")
    print("=" * 78)
    print(
        f"  {'map':<14s} {'metric':<18s} {'centroid':>12s} {'area_wgt':>12s} {'Δ':>12s}"
    )
    for _, r in table.iterrows():
        c, a, d = r["centroid"], r["area_weighted"], r["delta"]
        if r["metric"] == "seats_at_50_50":
            print(
                f"  {r['map']:<14s} {r['metric']:<18s} {c*100:>11.3f}% {a*100:>11.3f}% {d*100:>+11.4f}pp"
            )
        elif r["metric"] in ("efficiency_gap", "mean_median"):
            print(
                f"  {r['map']:<14s} {r['metric']:<18s} {c*100:>+11.4f}% {a*100:>+11.4f}% {d*100:>+11.4f}pp"
            )
        else:
            print(
                f"  {r['map']:<14s} {r['metric']:<18s} {c:>+12.5f} {a:>+12.5f} {d:>+12.5f}"
            )

    # s50 verdict per map.
    s50_deltas = {
        "majority_2026": (maj_a["seats_at_50_50"] - maj_c["seats_at_50_50"]) * 100,
        "minority_2026": (min_a["seats_at_50_50"] - min_c["seats_at_50_50"]) * 100,
    }
    threshold_pp = 1.0
    survives = all(abs(d) < threshold_pp for d in s50_deltas.values())
    print(
        f"\n  threshold for centroid defensibility: |Δ s50| < {threshold_pp:.1f} pp on both maps"
    )
    print(f"  Δ s50 majority: {s50_deltas['majority_2026']:+.4f} pp")
    print(f"  Δ s50 minority: {s50_deltas['minority_2026']:+.4f} pp")
    print(
        f"  VERDICT: centroid attribution {'SURVIVES' if survives else 'FAILS'} the MAUP attack"
    )

    out = {
        "centroid_majority": maj_c,
        "centroid_minority": min_c,
        "area_weighted_majority": maj_a,
        "area_weighted_minority": min_a,
        "deltas_pp": {
            "majority_2026": {
                k: (maj_a[k] - maj_c[k]) * 100
                for k in ["seats_at_50_50", "efficiency_gap", "mean_median"]
            }
            | {"declination": maj_a["declination"] - maj_c["declination"]},
            "minority_2026": {
                k: (min_a[k] - min_c[k]) * 100
                for k in ["seats_at_50_50", "efficiency_gap", "mean_median"]
            }
            | {"declination": min_a["declination"] - min_c["declination"]},
        },
        "threshold_pp": threshold_pp,
        "survives_maup_attack": survives,
        "table_long": rows,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str))
    print(f"\n  wrote: {OUT_JSON}")


if __name__ == "__main__":
    main()
