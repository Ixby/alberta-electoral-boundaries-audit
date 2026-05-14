# Version: v0.9
"""v0_9 advance-vote sensitivity: re-score v0_9 majority and minority maps
under (A) Election-Day votes only and (B) Election-Day + smeared advance
votes (advance_vote_splat output).

Substrate A: data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
Substrate B: data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg
             (produced by analysis/scripts/advance_vote_splat.py)

Outputs all four scenarios (2 maps x 2 substrates) and writes a JSON to
data/advance_vote_sensitivity.json with the seats_at_50_50 deltas
between A and B.

Forward: findings/advance_vote_sensitivity.md
Backward:
  data/shapefiles/derived/va_polygons_with_2023_votes.gpkg
  data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg
  data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg
  data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg
  analysis/scripts/mcmc_ensemble.py (seat_results, score_exogenous_map)
"""

# Version: 0.1 series  (last updated 2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

import sys
import json
from pathlib import Path

import geopandas as gpd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mcmc_ensemble import seat_results

ROOT = HERE.parent.parent
DATA = data_loader._resolve_path("data")
DERIVED = DATA / "shapefiles" / "derived"

VA_ED = DERIVED / "va_polygons_with_2023_votes.gpkg"
VA_FULL = DERIVED / "va_polygons_with_full_2023_votes.gpkg"
MAJ_V9 = DATA / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg"
MIN_V9 = DATA / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"

OUT_JSON = DATA / "outputs" / "advance_vote_sensitivity.json"


def load_va(path: Path, ucp_col: str, ndp_col: str, other_col: str) -> gpd.GeoDataFrame:
    va = gpd.read_file(path)
    va["va_ucp"] = va[ucp_col].fillna(0.0).astype(float)
    va["va_ndp"] = va[ndp_col].fillna(0.0).astype(float)
    va["va_other"] = va[other_col].fillna(0.0).astype(float)
    va["total_votes"] = va["va_ucp"] + va["va_ndp"] + va["va_other"]
    return va


def score_map(va: gpd.GeoDataFrame, map_path: Path, id_col: str = "name_2026") -> dict:
    proposed = gpd.read_file(map_path)
    if proposed.crs != va.crs:
        proposed = proposed.to_crs(va.crs)

    centroids = va.copy()
    centroids["geometry"] = centroids.geometry.representative_point()
    joined = gpd.sjoin(
        centroids[["va_ucp", "va_ndp", "va_other", "total_votes", "geometry"]],
        proposed[[id_col, "geometry"]],
        how="left",
        predicate="within",
    )

    covered = joined.dropna(subset=[id_col])
    covered = covered[~covered.index.duplicated(keep="first")]

    agg = (
        covered.groupby(id_col)
        .agg(
            ucp=("va_ucp", "sum"),
            ndp=("va_ndp", "sum"),
            other=("va_other", "sum"),
            total_votes=("total_votes", "sum"),
        )
        .reset_index()
    )

    metrics = seat_results(agg["ucp"].values, agg["ndp"].values)
    metrics["coverage_vas"] = int(len(covered))
    metrics["coverage_vas_total"] = int(len(va))
    return metrics


def main():
    print("loading substrates...")
    va_ed = load_va(VA_ED, "va_ucp", "va_ndp", "va_other")
    va_full = load_va(VA_FULL, "va_ucp_full", "va_ndp_full", "va_other_full")

    print(
        f"  ED-only:  total NDP={va_ed['va_ndp'].sum():,.0f}  UCP={va_ed['va_ucp'].sum():,.0f}  "
        f"two-party total={va_ed['va_ndp'].sum() + va_ed['va_ucp'].sum():,.0f}"
    )
    print(
        f"  Full:     total NDP={va_full['va_ndp'].sum():,.0f}  UCP={va_full['va_ucp'].sum():,.0f}  "
        f"two-party total={va_full['va_ndp'].sum() + va_full['va_ucp'].sum():,.0f}"
    )

    results = {}
    for substrate_name, va in [
        ("election_day_only", va_ed),
        ("with_advance_smear", va_full),
    ]:
        for map_name, map_path in [
            ("v0_9_majority", MAJ_V9),
            ("v0_9_minority", MIN_V9),
        ]:
            m = score_map(va, map_path)
            key = f"{map_name}__{substrate_name}"
            results[key] = m
            print(
                f"  {key}: seats@50/50 = {m['seats_at_50_50']:.4f}  "
                f"ucp_share = {m['ucp_vote_share']:.4f}  "
                f"ucp_seats = {m['ucp_seats']}/{m['n_districts']}  "
                f"EG = {m['efficiency_gap']:+.4f}"
            )

    # Compute deltas
    deltas = {}
    for map_name in ("v0_9_majority", "v0_9_minority"):
        a = results[f"{map_name}__election_day_only"]["seats_at_50_50"]
        b = results[f"{map_name}__with_advance_smear"]["seats_at_50_50"]
        deltas[map_name] = {
            "election_day_only": a,
            "with_advance_smear": b,
            "delta_pp": (b - a) * 100,
        }
        # Other metrics deltas
        for metric in (
            "efficiency_gap",
            "mean_median",
            "declination",
            "ucp_vote_share",
        ):
            ma = results[f"{map_name}__election_day_only"][metric]
            mb = results[f"{map_name}__with_advance_smear"][metric]
            deltas[map_name][f"{metric}_A"] = ma
            deltas[map_name][f"{metric}_B"] = mb
            deltas[map_name][f"{metric}_delta"] = mb - ma

    out = {"results": results, "deltas": deltas}

    # JSON-safe
    def _to_native(obj):
        if isinstance(obj, dict):
            return {k: _to_native(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_to_native(v) for v in obj]
        if hasattr(obj, "item"):
            return obj.item()
        return obj

    with open(OUT_JSON, "w") as f:
        json.dump(_to_native(out), f, indent=2)
    print(f"\nwrote {OUT_JSON}")

    print("\n=== seats@50/50 deltas (B - A, in percentage points) ===")
    for map_name, d in deltas.items():
        print(
            f"  {map_name}: A={d['election_day_only']:.4f}  B={d['with_advance_smear']:.4f}  "
            f"delta = {d['delta_pp']:+.3f} pp"
        )


if __name__ == "__main__":
    main()
