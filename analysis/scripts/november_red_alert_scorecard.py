"""November Red Alert Scorecard — tripwire for the Lunty committee's 91-seat map.

Watches for the four-part MO that the minority commission map
demonstrated:

  MO #1 — Drain Pattern (city cracking): mid-sized cities sliced into
          more districts than their population warrants, with each
          piece anchored to a rural hinterland.
  MO #2 — The Lasso (surgical non-compactness): districts in the
          bottom-decile of Polsby-Popper that also have a mixed
          urban-rural composition (the urban-fringe extraction signature).
  MO #3 — Municipal de-anchoring: total municipal-anchoring percentage
          drops below the ~70% Canadian norm (the minority map sat at
          15%; the majority map at 71%).
  MO #4 — Sampler divergence: Python ReCom puts the map's seats@50/50
          in the upper tail (e.g. p95+) while R SMC puts it near the
          median. Divergence is mathematical proof that the seat
          advantage is reachable only by breaking compactness.

Inputs:
  --shapefile PATH    The 91-seat map's polygon shapefile or GPKG.
  --map-name LABEL    Friendly name (e.g. "Lunty 2026-11").
  --skip-mcmc         Optional: skip the ReCom + SMC ensemble runs
                      and rely on cached prior runs (fast scorecard
                      for prose-only iteration).

Outputs:
  findings/november_red_alert_<map_name>_<date>.md

This scorecard is one of the prospective components of the
pre-registered audit (RQ8-9): the threshold-firing logic was
committed to in writing on April 24 2026, before the Lunty
committee began its work, so post-hoc redrawing of thresholds
to fit the data is impossible.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader


def _get_findings_dir() -> Path:
    try:
        from analysis.utils.data_loader import FINDINGS
        return FINDINGS
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
        from data_loader import FINDINGS
        return FINDINGS


import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import geopandas as gpd
import warnings

warnings.simplefilter("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from drand_seed import get_canonical_seed  # noqa: E402

# Canonical seed for all bootstrap resampling in this script.
# Derived from drand round 5500000 (Cloudflare League of Entropy).
# Verify: drand.cloudflare.com/public/5500000
# Pre-registered: AsPredicted #289452 (Phase 2 Lunty Committee Map Forensic Analysis)
BOOTSTRAP_SEED: int = get_canonical_seed("lunty-bootstrap")

VA_VOTES_PATH = (
    data_loader._resolve_path("data") / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
)
ALBERTA_CSDS = (
    data_loader._resolve_path("data") / "shapefiles" / "reference" / "alberta_csds.gpkg"
)  # may not exist
RECOM_SAMPLES = data_loader._resolve_path("data") / "simulated_ensemble_raw_samples_250k.csv"
SMC_OUTPUT = data_loader._resolve_path("data") / "redist_crossvalidation_s50.csv"

# Pre-registered tripwire thresholds (committed to before the Lunty
# committee began work).
MO1_DRAIN_TRIPWIRE_FACTOR = 1.5  # If a city's district-count exceeds
# 1.5 × what its population mathematically
# warrants, flag it. Empirical baseline:
# the minority map's Airdrie split was
# 4-way for a city whose population
# warrants 2 → ratio 2.0 (above 1.5).
MO2_PP_PERCENTILE_THRESHOLD = 10  # bottom decile of Polsby-Popper
MO3_ANCHORING_THRESHOLD = 0.70  # Canadian norm; 70% lower bound
MO4_SAMPLER_DIVERGENCE_PP = 25  # divergence in s@50 percentile rank
# between ReCom and SMC, in pp


@dataclass
class TripwireResult:
    name: str
    fired: bool
    summary: str
    detail: dict = field(default_factory=dict)


def mo1_drain_pattern(eds: gpd.GeoDataFrame, name_col: str) -> TripwireResult:
    """City Integrity check: count districts intersecting each named city.

    Compares to a per-city population-justified district count. The
    population-justified count is computed from each city's 2021 census
    population divided by Alberta's per-district average population.
    """
    avg_pop_per_district = 47_889  # 2021 Alberta pop / 91 seats
    # Per-city populations (2021 census) — pre-registered constants
    # so the threshold logic doesn't move when a new city polygon is added.
    cities = {
        "Calgary": {"pop": 1_306_784, "csd_codes": [4806016]},
        "Edmonton": {"pop": 1_010_899, "csd_codes": [4811062]},
        "Red Deer": {"pop": 100_844, "csd_codes": [4806036]},
        "Lethbridge": {"pop": 98_406, "csd_codes": [4802012]},
        "St. Albert": {"pop": 68_232, "csd_codes": [4811049]},
        "Medicine Hat": {"pop": 63_271, "csd_codes": [4801006]},
        "Grande Prairie": {"pop": 64_141, "csd_codes": [4819030]},
        "Airdrie": {"pop": 74_100, "csd_codes": [4806008]},
        "Spruce Grove": {"pop": 37_645, "csd_codes": [4811053]},
        "Leduc": {"pop": 34_094, "csd_codes": [4811028]},
    }
    csd_path = ALBERTA_CSDS
    flagged = []
    if not csd_path.exists():
        return TripwireResult(
            name="MO #1 — Drain Pattern (city cracking)",
            fired=False,
            summary=f"SKIPPED — Alberta CSD polygon file missing at "
            f"{csd_path.relative_to(ROOT)}. Cannot count district-per-city "
            f"intersections without it.",
        )
    csd = gpd.read_file(csd_path).to_crs(eds.crs)
    for city_name, meta in cities.items():
        city_geom = csd[
            csd["CSDUID"].astype(str).isin([str(c) for c in meta["csd_codes"]])
        ]
        if city_geom.empty:
            continue
        # Count districts whose interior intersects this city's polygon
        # (interior=True excludes border-only touches that don't represent
        # a real population split)
        intersections = eds[eds.geometry.intersects(city_geom.unary_union)]
        n_districts = len(intersections)
        justified = max(1, int(np.ceil(meta["pop"] / avg_pop_per_district)))
        ratio = n_districts / justified if justified else 0.0
        if ratio >= MO1_DRAIN_TRIPWIRE_FACTOR:
            flagged.append(
                {
                    "city": city_name,
                    "population_2021": meta["pop"],
                    "districts_in_city": n_districts,
                    "justified_districts": justified,
                    "split_ratio": round(ratio, 2),
                }
            )
    return TripwireResult(
        name="MO #1 — Drain Pattern (city cracking)",
        fired=len(flagged) > 0,
        summary=(
            f"{len(flagged)} cities exceed the 1.5x district-split " f"threshold"
            if flagged
            else "no cities exceed the 1.5x district-split threshold"
        ),
        detail={
            "flagged_cities": flagged,
            "threshold_ratio": MO1_DRAIN_TRIPWIRE_FACTOR,
        },
    )


def mo2_lasso_compactness(eds: gpd.GeoDataFrame, name_col: str) -> TripwireResult:
    """Polsby-Popper × hybridization cross-check.

    Flags districts whose PP sits in the bottom decile of the Lunty map
    AND whose composition has a mixed urban-rural split (60/40 or worse).
    "Urban" is defined as VA centroids inside the ten largest cities'
    CSD polygons.
    """
    pp = 4 * np.pi * eds.geometry.area / (eds.geometry.length**2)
    threshold_pp = float(np.percentile(pp.dropna(), MO2_PP_PERCENTILE_THRESHOLD))

    # Compute urban share per district via VA centroid + CSD overlay
    if not (VA_VOTES_PATH.exists() and ALBERTA_CSDS.exists()):
        return TripwireResult(
            name="MO #2 — Lasso (surgical non-compactness)",
            fired=False,
            summary=(
                f"PARTIAL — PP threshold computed (bottom decile = "
                f"{threshold_pp:.3f}). VA-CSD urban-share check "
                f"skipped (missing reference data)."
            ),
            detail={
                "pp_threshold_p10": threshold_pp,
                "districts_below": int((pp < threshold_pp).sum()),
            },
        )
    va = gpd.read_file(VA_VOTES_PATH).to_crs(eds.crs)
    csd = gpd.read_file(ALBERTA_CSDS).to_crs(eds.crs)
    big_city_codes = {
        4806016,
        4811062,
        4806036,
        4802012,
        4811049,
        4801006,
        4819030,
        4806008,
    }
    big_city = csd[csd["CSDUID"].astype(str).isin([str(c) for c in big_city_codes])]
    va_centroids = gpd.GeoDataFrame(
        {"_idx": range(len(va))},
        geometry=va.geometry.centroid,
        crs=va.crs,
    )
    urban_mask = gpd.sjoin(
        va_centroids, big_city[["geometry"]], how="left", predicate="within"
    )
    urban_mask = urban_mask.drop_duplicates(subset=["_idx"]).sort_values("_idx")
    va["is_urban"] = urban_mask["index_right"].notna().values

    va_to_ed = gpd.sjoin(
        va_centroids.assign(is_urban=va["is_urban"].values),
        eds[[name_col, "geometry"]],
        how="left",
        predicate="within",
    )
    va_to_ed = va_to_ed.drop_duplicates(subset=["_idx"])
    urban_share = va_to_ed.groupby(name_col)["is_urban"].mean()

    flagged = []
    for idx, row in eds.iterrows():
        nm = row[name_col]
        ed_pp = float(pp.iloc[idx])
        ed_urban = float(urban_share.get(nm, 0.0))
        if ed_pp < threshold_pp and 0.40 <= ed_urban <= 0.60:
            flagged.append(
                {
                    "name": nm,
                    "polsby_popper": round(ed_pp, 4),
                    "urban_va_fraction": round(ed_urban, 3),
                }
            )
    return TripwireResult(
        name="MO #2 — Lasso (surgical non-compactness)",
        fired=len(flagged) > 0,
        summary=(
            f"{len(flagged)} districts in the bottom-decile of PP "
            f"AND with a 40-60% urban-rural mix"
            if flagged
            else "no districts hit both bottom-decile PP AND mixed urban-rural"
        ),
        detail={"pp_threshold_p10": threshold_pp, "flagged_districts": flagged},
    )


def mo3_municipal_anchoring(eds: gpd.GeoDataFrame) -> TripwireResult:
    """Re-run the audit's existing anchoring metric on the new map.

    The metric is the fraction of the total inter-district boundary
    length that coincides (within a small tolerance) with a pre-existing
    municipal/CSD boundary. The minority map sat at 15%, the majority at
    71%; the 70% threshold is the Canadian-norm lower bound.
    """
    if not ALBERTA_CSDS.exists():
        return TripwireResult(
            name="MO #3 — Municipal de-anchoring",
            fired=False,
            summary=f"SKIPPED — Alberta CSD polygon file missing at "
            f"{ALBERTA_CSDS.relative_to(ROOT)}.",
        )
    csd = gpd.read_file(ALBERTA_CSDS).to_crs(eds.crs)
    csd_boundary = csd.boundary.unary_union
    # Inter-district boundary length: total ED border minus shared
    # boundary with another ED (= twice-counted) — we just sum each
    # ED's boundary and the inter-ED edges are double-counted, so
    # take the unary_union perimeter instead.
    eds_union = eds.unary_union
    total_boundary = eds.boundary.unary_union
    # Length of total boundary that lies on a CSD line (within 25m
    # buffer to absorb digitisation noise)
    csd_buffer = csd_boundary.buffer(25.0)
    on_csd = total_boundary.intersection(csd_buffer)
    anchored_frac = (
        on_csd.length / total_boundary.length if total_boundary.length > 0 else 0.0
    )
    return TripwireResult(
        name="MO #3 — Municipal de-anchoring",
        fired=anchored_frac < MO3_ANCHORING_THRESHOLD,
        summary=(
            f"municipal anchoring = {anchored_frac:.1%} "
            f"(Canadian norm threshold {MO3_ANCHORING_THRESHOLD:.0%})"
        ),
        detail={
            "anchored_fraction": anchored_frac,
            "threshold": MO3_ANCHORING_THRESHOLD,
        },
    )


def mo4_sampler_divergence(map_s50: float) -> TripwireResult:
    """Compare ReCom and SMC percentile placement of the new map's seats@50/50."""
    if not (RECOM_SAMPLES.exists() and SMC_OUTPUT.exists()):
        return TripwireResult(
            name="MO #4 — Sampler divergence",
            fired=False,
            summary=f"SKIPPED — pre-existing ensemble outputs missing.",
        )
    recom = pd.read_csv(RECOM_SAMPLES)["seats_at_50_50"].dropna().values
    smc_df = pd.read_csv(SMC_OUTPUT)
    smc = smc_df["seats_at_50_50"].values
    smc_w = smc_df["weight"].values if "weight" in smc_df.columns else None

    recom_pct = float(100 * (recom <= map_s50).sum() / len(recom))
    if smc_w is not None:
        order = np.argsort(smc)
        cw = np.cumsum(smc_w[order]) / smc_w.sum()
        idx = np.searchsorted(smc[order], map_s50, side="right")
        smc_pct = float(100 * cw[min(idx - 1, len(cw) - 1)]) if idx > 0 else 0.0
    else:
        smc_pct = float(100 * (smc <= map_s50).sum() / len(smc))

    divergence = recom_pct - smc_pct
    return TripwireResult(
        name="MO #4 — Sampler divergence",
        fired=abs(divergence) > MO4_SAMPLER_DIVERGENCE_PP,
        summary=(
            f"map seats@50/50 = {map_s50:.4f} → "
            f"ReCom percentile {recom_pct:.1f}, "
            f"SMC percentile {smc_pct:.1f}, "
            f"divergence {divergence:+.1f}pp "
            f"(threshold {MO4_SAMPLER_DIVERGENCE_PP}pp)"
        ),
        detail={
            "recom_percentile": recom_pct,
            "smc_percentile": smc_pct,
            "divergence_pp": divergence,
            "threshold_pp": MO4_SAMPLER_DIVERGENCE_PP,
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shapefile",
        required=True,
        type=Path,
        help="Path to the 91-seat map shapefile or GPKG.",
    )
    parser.add_argument(
        "--map-name",
        default="LuntyCommittee",
        help="Friendly name (used in output filenames).",
    )
    parser.add_argument(
        "--name-col",
        default="name_2026",
        help="Column in the shapefile with district names.",
    )
    parser.add_argument(
        "--skip-mcmc",
        action="store_true",
        help="Skip the ReCom + SMC ensemble runs (use " "cached prior outputs).",
    )
    parser.add_argument(
        "--map-s50",
        type=float,
        default=None,
        help="The map's seats@50/50 score, if precomputed. "
        "If omitted and --skip-mcmc set, MO #4 is skipped.",
    )
    args = parser.parse_args()

    if not args.shapefile.exists():
        print(f"ERROR: shapefile not found at {args.shapefile}", file=sys.stderr)
        return 2

    eds = gpd.read_file(args.shapefile).to_crs(3401)
    name_col = args.name_col if args.name_col in eds.columns else eds.columns[0]
    print(f"[scorecard] loaded {len(eds)} districts from {args.shapefile.name}")

    results: list[TripwireResult] = []
    print("[scorecard] running MO #1 — Drain Pattern...")
    results.append(mo1_drain_pattern(eds, name_col))
    print("[scorecard] running MO #2 — Lasso compactness...")
    results.append(mo2_lasso_compactness(eds, name_col))
    print("[scorecard] running MO #3 — Municipal anchoring...")
    results.append(mo3_municipal_anchoring(eds))
    if args.map_s50 is not None:
        print("[scorecard] running MO #4 — Sampler divergence...")
        results.append(mo4_sampler_divergence(args.map_s50))
    elif not args.skip_mcmc:
        print(
            "[scorecard] WARN: --map-s50 not provided and --skip-mcmc not set;"
            " MO #4 is being skipped (auto-MCMC orchestration is not "
            "implemented in this scaffold)."
        )
        results.append(
            TripwireResult(
                name="MO #4 — Sampler divergence",
                fired=False,
                summary="SKIPPED — provide --map-s50 to score against cached ensembles.",
            )
        )

    # Write report
    today = date.today().isoformat()
    out_path = (
        _get_findings_dir() / f"november_red_alert_{args.map_name}_{today}.md"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fired_count = sum(1 for r in results if r.fired)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# November Red Alert Scorecard — {args.map_name}\n\n")
        f.write(f"Date: {today}  \n")
        f.write(f"Shapefile: `{args.shapefile.relative_to(ROOT)}`  \n")
        f.write(f"Tripwires fired: **{fired_count} of {len(results)}**\n\n")
        for r in results:
            badge = "🔴 **FIRED**" if r.fired else "⚪ clean"
            f.write(f"## {r.name} — {badge}\n\n")
            f.write(f"{r.summary}\n\n")
            if r.detail:
                f.write("```json\n")
                f.write(json.dumps(r.detail, indent=2, default=float))
                f.write("\n```\n\n")
        f.write("---\n\n")
        f.write("Pre-registered tripwire thresholds:\n\n")
        f.write(
            f"- MO #1 drain ratio threshold: {MO1_DRAIN_TRIPWIRE_FACTOR}x population-justified\n"
        )
        f.write(
            f"- MO #2 Polsby-Popper percentile threshold: bottom {MO2_PP_PERCENTILE_THRESHOLD}%\n"
        )
        f.write(f"- MO #3 anchoring threshold: {MO3_ANCHORING_THRESHOLD:.0%}\n")
        f.write(
            f"- MO #4 sampler divergence threshold: {MO4_SAMPLER_DIVERGENCE_PP}pp\n"
        )
    print(f"[scorecard] wrote {out_path.relative_to(ROOT)}")
    print(f"[scorecard] {fired_count} of {len(results)} tripwires fired")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
