"""Attribution Sensitivity Check — partial vs full VA vote coverage.

Scores both 2026 canonical maps under:
  - PARTIAL coverage (va_ndp / canonical run basis)
  - FULL coverage (va_ndp_full / area-weighted full allocation)

Computes percentile placement of each real-map value against the canonical
ensemble distribution (loaded from 4 checkpoint chains). Flags any metric
where the percentile shifts by >= 3 pp between attribution variants.

Run from repo root:
    python analysis/scripts/attribution_sensitivity_check.py

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""

import sys
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from mcmc_ensemble import score_exogenous_map  # noqa: E402

MAJORITY_GPKG = ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"
MINORITY_GPKG = ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg"
VA_FULL_GPKG = ROOT / "data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg"
POP_CSV = ROOT / "data/outputs/va_pop_from_das.csv"
CHAIN_DIR = ROOT / "data/simulation_checkpoints_canonical"

CHAIN_FILES = [
    CHAIN_DIR / "chain0_samples.csv",
    CHAIN_DIR / "chain1_samples.csv",
    CHAIN_DIR / "chain2_samples.csv",
    CHAIN_DIR / "chain3_samples.csv",
]

METRICS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
MATERIAL_THRESHOLD_PP = 3.0  # percentile-point shift that warrants attention
ID_COL = "EDName2025"


def load_va(use_full: bool) -> gpd.GeoDataFrame:
    """Load VA geodataframe with appropriate vote columns and pop_2021."""
    va = gpd.read_file(VA_FULL_GPKG)

    if use_full:
        va["va_ndp"] = va["va_ndp_full"]
        va["va_ucp"] = va["va_ucp_full"]
        va["va_other"] = va["va_other_full"]

    va["total_votes"] = va["va_ndp"] + va["va_ucp"] + va["va_other"]

    # Attach population so population_mad is meaningful
    pop_df = pd.read_csv(POP_CSV).set_index("va_row_idx")["pop_2021"]
    va["pop_2021"] = va.index.map(pop_df).fillna(0.0)
    va["pop_2021"] = np.maximum(va["pop_2021"], 1.0)

    return va


def load_ensemble() -> pd.DataFrame:
    """Concatenate all 4 canonical checkpoint chains into one distribution."""
    frames = []
    for f in CHAIN_FILES:
        if f.exists():
            frames.append(pd.read_csv(f, usecols=METRICS))
        else:
            warnings.warn(f"Missing checkpoint: {f}")
    if not frames:
        raise FileNotFoundError("No canonical checkpoint files found.")
    return pd.concat(frames, ignore_index=True)


def percentile_in_distribution(value: float, distribution: np.ndarray) -> float:
    """Return the percentile rank (0–100) of value within distribution."""
    return float(np.mean(distribution <= value) * 100.0)


def score_maps(va: gpd.GeoDataFrame, label: str) -> dict:
    """Score both canonical maps and return metrics keyed by map name."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        maj = score_exogenous_map(va, MAJORITY_GPKG, id_col=ID_COL)
        min_ = score_exogenous_map(va, MINORITY_GPKG, id_col=ID_COL)
    print(
        f"  [{label}] majority ndp_total={va['va_ndp'].sum():,.0f}  "
        f"coverage={maj['coverage_pct']:.2%}"
    )
    return {"majority": maj, "minority": min_}


def main():
    print("Loading canonical ensemble distribution...")
    ensemble = load_ensemble()
    print(f"  {len(ensemble):,} simulated plans loaded.")

    print("\nScoring with PARTIAL attribution (va_ndp)...")
    va_partial = load_va(use_full=False)
    scores_partial = score_maps(va_partial, "partial")

    print("\nScoring with FULL attribution (va_ndp_full)...")
    va_full = load_va(use_full=True)
    scores_full = score_maps(va_full, "full")

    print("\n" + "=" * 72)
    print("ATTRIBUTION SENSITIVITY — PERCENTILE COMPARISON")
    print("=" * 72)

    any_material = False
    rows = []

    for map_name in ("majority", "minority"):
        for metric in METRICS:
            val_p = scores_partial[map_name][metric]
            val_f = scores_full[map_name][metric]
            dist = ensemble[metric].values
            ptile_p = percentile_in_distribution(val_p, dist)
            ptile_f = percentile_in_distribution(val_f, dist)
            delta = ptile_f - ptile_p
            material = abs(delta) >= MATERIAL_THRESHOLD_PP
            if material:
                any_material = True
            rows.append(
                {
                    "map": map_name,
                    "metric": metric,
                    "val_partial": val_p,
                    "val_full": val_f,
                    "ptile_partial": ptile_p,
                    "ptile_full": ptile_f,
                    "delta_pp": delta,
                    "material": material,
                }
            )

    results = pd.DataFrame(rows)

    # Print results table
    fmt = "{:<10} {:<22} {:>10.4f} {:>10.4f} {:>12.2f} {:>12.2f} {:>10.2f}  {}"
    header = "{:<10} {:<22} {:>10} {:>10} {:>12} {:>12} {:>10}  {}"
    print(
        header.format(
            "Map", "Metric", "val_partial", "val_full",
            "ptile_partial", "ptile_full", "delta_pp", "MATERIAL?"
        )
    )
    print("-" * 92)
    for _, r in results.iterrows():
        flag = "*** MATERIAL ***" if r["material"] else ""
        print(
            fmt.format(
                r["map"], r["metric"],
                r["val_partial"], r["val_full"],
                r["ptile_partial"], r["ptile_full"],
                r["delta_pp"], flag,
            )
        )

    print("=" * 72)
    if any_material:
        print(
            "\nRESULT: MATERIAL SHIFT DETECTED (>= 3 pp). "
            "Headline findings need re-evaluation before further report work."
        )
    else:
        print(
            "\nRESULT: No material shift (all delta_pp < 3 pp). "
            "Canonical percentile placements are attribution-stable."
        )

    out_path = ROOT / "data/outputs/attribution_sensitivity_check.json"
    results.to_json(out_path, orient="records", indent=2)
    print(f"\nDetailed results written to {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
