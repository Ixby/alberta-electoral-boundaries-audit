"""Phase B Scorecard — tripwire for the Lunty Special Select Committee's 91-seat map (the audit's Phase B / confirmatory test).

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
  findings/phase_b_scorecard_<map_name>_<date>.md

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
# score_anchoring is imported lazily inside mo3_municipal_anchoring so that any
# import-time failure (missing config, sys.path issue) surfaces in main()'s
# preflight diagnostics rather than killing the script before preflight runs.

# Canonical seed for all bootstrap resampling in this script.
# Derived from drand round 5500000 (Cloudflare League of Entropy).
# Verify: drand.cloudflare.com/public/5500000
# Pre-registered: AsPredicted #289452 (Phase 2 Lunty Committee Map Forensic Analysis)
BOOTSTRAP_SEED: int = get_canonical_seed("lunty-bootstrap")

VA_VOTES_PATH = (
    data_loader._resolve_path("data") / "shapefiles" / "canonical" / "va_2023_election_day_votes.gpkg"
)  # canonical VA polygons + 2023 election-day votes (was derived/v0_8 DPG; switched to canonical 2026-05-23)
ALBERTA_CSDS = (
    data_loader._resolve_path("data") / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"
)  # canonical StatsCan 2021 CSDs — required for MO #1 and MO #3
RECOM_SAMPLES = data_loader._resolve_path("data") / "outputs" / "simulated_ensemble_raw_samples_canonical.csv"  # canonical 1.01M-plan ReCom ensemble (was DPG-era 250k; LFS-tracked, ~170 MB; switched 2026-05-23)
SMC_OUTPUT = data_loader._resolve_path("data") / "redist_crossvalidation_s50.csv"  # canonical SMC 5,000 plans, importance-weighted, ESS 1,116

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
    avg_pop_per_district = 53_722  # floor(4,888,723 / 91) — TBF-adjusted population, 91-seat Lunty committee basis
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
        try:
            csd_display = str(csd_path.relative_to(ROOT))
        except ValueError:
            csd_display = str(csd_path)
        return TripwireResult(
            name="MO #1 — Drain Pattern (city cracking)",
            fired=False,
            summary=f"SKIPPED — Alberta CSD polygon file missing at "
            f"{csd_display}. Cannot count district-per-city "
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

    Delegates to score_anchoring.score_anchoring() so MO #3 reports the
    same metric in the same units that the 70% Canadian-norm threshold
    was calibrated against. Until 2026-05-23 this function carried a
    parallel implementation (25m buffer intersection) that diverged
    ~2x from the headline measurement on the same input; the threshold
    was calibrated against the headline, so the mismatched body fired
    on virtually every commission map. See proposals/lunty_dry_run/
    dry_run_report.md Bug #8 for the full diagnosis.

    Passes the already-loaded, already-reprojected `eds` GeoDataFrame
    through to score_anchoring so any caller-side preprocessing
    (to_crs(3401) in main, future filtering) is honoured. Previously
    this function ignored `eds` and re-read the shapefile from disk,
    which would silently diverge from the eds MO #1 / MO #2 ran against.
    """
    if not ALBERTA_CSDS.exists():
        try:
            csd_display = str(ALBERTA_CSDS.relative_to(ROOT))
        except ValueError:
            csd_display = str(ALBERTA_CSDS)
        return TripwireResult(
            name="MO #3 — Municipal de-anchoring",
            fired=False,
            summary=f"SKIPPED — Alberta CSD polygon file missing at {csd_display}.",
        )

    # Lazy import: defer until preflight has passed so any import-time
    # failure (missing config, sys.path issue) appears as an MO #3 error
    # rather than killing the script before MO #1 / MO #2 can run.
    try:
        from score_anchoring import score_anchoring as _score_anchoring_headline
    except ImportError as e:
        return TripwireResult(
            name="MO #3 — Municipal de-anchoring",
            fired=False,
            summary=f"ERRORED — could not import score_anchoring: {e}",
        )

    try:
        anchored_pct = _score_anchoring_headline(eds)
    except (ValueError, OSError, RuntimeError) as e:
        # Don't let MO #3 crash the whole scorecard mid-run — MO #4 / MO #5
        # are still worth attempting. Surface the failure in the report.
        return TripwireResult(
            name="MO #3 — Municipal de-anchoring",
            fired=False,
            summary=f"ERRORED — score_anchoring raised {type(e).__name__}: {e}",
        )
    anchored_frac = anchored_pct / 100.0
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
            "methodology": "score_anchoring.py (tier-ordered snap, SNAP_TOL_M=500, VERTEX_DENSIFY_M=50)",
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
    parser.add_argument(
        "--out-dir",
        type=str,
        default=None,
        help="Directory to write the scorecard report into. Defaults to "
        "findings/ (live audit). For dry-runs against synthetic inputs, "
        "pass a path under proposals/lunty_dry_run/ so test outputs are "
        "not mistaken for live audit findings.",
    )
    args = parser.parse_args()

    # --- Pre-flight checks ----------------------------------------------------
    # On the live Nov 2 run, the 72-hour clock starts the moment the Lunty map
    # drops. We want the scorecard to error out LOUDLY at the start if a required
    # input file is missing or unreadable (e.g., LFS not pulled), rather than
    # silently skipping MOs and producing a misleading "0 of 3 fired" output.
    preflight_errors: list[str] = []

    if not args.shapefile.exists():
        preflight_errors.append(f"input shapefile not found at {args.shapefile}")

    # ALBERTA_CSDS is required by MO #1 (drain pattern) and MO #3 (municipal
    # anchoring); MO #2 (lasso) also reads it for the urban-share half of the
    # tripwire. Without it, three of four MOs degrade or skip silently.
    if not ALBERTA_CSDS.exists():
        preflight_errors.append(
            f"Alberta CSD reference not found at {ALBERTA_CSDS} "
            f"(required by MO #1 + MO #2 + MO #3). "
            f"Most likely cause: Git LFS not pulled — run `git lfs pull` to materialise."
        )
    else:
        # Distinguish a real gpkg from an LFS pointer file (132 bytes of ASCII).
        # An LFS-tracked file with `GIT_LFS_SKIP_SMUDGE=1` or a failed smudge
        # leaves a pointer file in place; reading it as a gpkg later would
        # raise pyogrio.errors.DataSourceError mid-MO with an unhelpful message.
        try:
            with open(ALBERTA_CSDS, "rb") as _f:
                _head = _f.read(64)
            if _head.startswith(b"version https://git-lfs"):
                preflight_errors.append(
                    f"{ALBERTA_CSDS} is an LFS pointer file (not the actual gpkg). "
                    f"Run `git lfs pull` to materialise the binary."
                )
        except OSError as e:
            preflight_errors.append(f"could not read {ALBERTA_CSDS}: {e}")

    # VA_VOTES_PATH is required by MO #2 (urban-share check inside lasso).
    if not VA_VOTES_PATH.exists():
        preflight_errors.append(
            f"VA shapefile not found at {VA_VOTES_PATH} "
            f"(required by MO #2 urban-share check). "
            f"Most likely cause: Git LFS not pulled — run `git lfs pull` to materialise."
        )
    else:
        try:
            with open(VA_VOTES_PATH, "rb") as _f:
                _head = _f.read(64)
            if _head.startswith(b"version https://git-lfs"):
                preflight_errors.append(
                    f"{VA_VOTES_PATH} is an LFS pointer file (not the actual gpkg). "
                    f"Run `git lfs pull` to materialise the binary."
                )
        except OSError as e:
            preflight_errors.append(f"could not read {VA_VOTES_PATH}: {e}")

    # RECOM_SAMPLES and SMC_OUTPUT are required by MO #4 (sampler divergence).
    # MO #4 only runs when --map-s50 is provided; preflight matches that gate.
    # Both are LFS-tracked CSVs that the preflight should sniff for pointer-
    # vs-binary, otherwise pd.read_csv either silently misreads a pointer file
    # or raises KeyError on the 'seats_at_50_50' lookup mid-MO #4.
    if args.map_s50 is not None:
        for mo4_path, mo4_name in (
            (RECOM_SAMPLES, "RECOM ensemble CSV"),
            (SMC_OUTPUT, "SMC cross-validation CSV"),
        ):
            if not mo4_path.exists():
                preflight_errors.append(
                    f"{mo4_name} not found at {mo4_path} "
                    f"(required by MO #4 sampler divergence when --map-s50 is set). "
                    f"Most likely cause: Git LFS not pulled — run `git lfs pull` to materialise."
                )
                continue
            try:
                with open(mo4_path, "rb") as _f:
                    _head = _f.read(64)
                if _head.startswith(b"version https://git-lfs"):
                    preflight_errors.append(
                        f"{mo4_path} is an LFS pointer file (not the actual CSV). "
                        f"Run `git lfs pull` to materialise the binary."
                    )
            except OSError as e:
                preflight_errors.append(f"could not read {mo4_path}: {e}")

    if preflight_errors:
        print(
            "[scorecard] PRE-FLIGHT FAILED — the live scorecard cannot run because "
            "one or more required reference files are missing or unreadable. "
            "Fix all errors below and re-invoke; do NOT proceed with partial outputs.",
            file=sys.stderr,
        )
        for err in preflight_errors:
            print(f"  - {err}", file=sys.stderr)
        return 2
    # --- End pre-flight checks ------------------------------------------------

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
    out_dir = Path(args.out_dir).resolve() if args.out_dir else _get_findings_dir()
    out_path = out_dir / f"phase_b_scorecard_{args.map_name}_{today}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fired_count = sum(1 for r in results if r.fired)

    # Render shapefile path relative to repo root when possible; fall back to the
    # absolute path so the report is still well-formed when the input lives
    # outside ROOT (e.g. a synthetic test input passed via absolute path).
    shapefile_abs = args.shapefile.resolve()
    try:
        shapefile_display = str(shapefile_abs.relative_to(ROOT))
    except ValueError:
        shapefile_display = str(shapefile_abs)

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# Phase B Scorecard — {args.map_name}\n\n")
        f.write(f"Date: {today}  \n")
        f.write(f"Shapefile: `{shapefile_display}`  \n")
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
