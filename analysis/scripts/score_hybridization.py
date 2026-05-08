"""
score_hybridization.py - Lane-2 Dangerzone metric #2 (hybrid ED count)
======================================================================

The audit's published prose (e.g. `report_public.md:248`,
`report_academic.md:2156`, `REPRODUCING.md:132`) reports three hybrid-ED
counts:

    2019 enacted  =  8 hybrid EDs
    2026 majority =  9 hybrid EDs
    2026 minority = 25 hybrid EDs

Those numbers are NOT computed by any script in the repository. They come

import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

from a manual narrative classification by the author (compare the lists
in `report_public.md:252-255` and the `MAJORITY_2026_MAPPING` /
`MINORITY_2026_MAPPING` "blend" tags in
`analysis/scripts/packing_cracking_analysis.py`, neither of which
yields 9/25/8 directly). This is documented as a critical finding in
`analysis/reports/dangerzone_metric_definitions.md`.

For the 100,000-plan ReCom ensemble we need a COMPUTABLE rule. This
script implements one and validates that it preserves the qualitative
finding (minority > majority > 2019) even though it does not reproduce
the published integers exactly.

Operational definition
----------------------

An electoral division is HYBRID iff its territorial area intersects:
  (a) at least one Statistics Canada 2021 CSD of type 'CY' (City) or
      'SM' (Specialized Municipality - functionally city-equivalent
      e.g. Strathcona County, Wood Buffalo) contributing >= 5% of the
      ED's area, AND
  (b) at least one CSD of any non-(CY|SM) type (T town, MD municipal
      district, IRI Indian reserve, VL village, SV summer village,
      ID improvement district, SA special area) contributing >= 5% of
      the ED's area.

Equivalently: the ED's territory bridges a Census-defined city and at
least one non-city administrative unit, with each side holding at least
5% of the ED's land.

Why CY+SM together: Strathcona County (CSDUID 4811052) and Wood Buffalo
(CSDUID 4816037) are SMs that are functionally cities (Sherwood Park,
Fort McMurray) under Alberta's specialized-municipality framework. Treating
them as cities matches the audit's narrative, where Sherwood Park and
Fort McMurray are not described as "rural hybrids."

Why a 5% area threshold: lower (1-3%) admits boundary-tracing slivers as
"hybrids"; higher (>=10%) loses the thin-corridor lasso configurations
the minority map is criticised for.

Reference layer: `data/shapefiles/reference/alberta_2021_csds.gpkg`
(StatsCan 2021 CSDs - identical to the layer used by the municipal-
anchoring metric so both metrics share a single substrate).

Validation result (also captured in v0_9 verdict memo):

  Map           This script    Published    Delta
  ------------  -------------  -----------  -------
  Maj 2026      14             9            +5
  Min 2026      17             25           -8
  2019 enacted  8              8             0   (exact)

Direction preserved (Min > Maj > 2019), but absolute integers diverge
materially on Maj 2026 and Min 2026. Published 9/25/8 numbers reflect
the audit author's manual taxonomy (which districts they considered
"genuinely" urban-rural hybrids by intent) rather than any computable
rule on geometry. For ensemble work the directional rank matters; the
absolute integer does not.

CLI
---
    python analysis/scripts/score_hybridization.py --shapefile PATH

Output: a single integer on stdout (the hybrid-ED count for the input
shapefile under the operational definition above).

Forward:
    analysis/reports/dangerzone_metric_definitions.md
Backward:
    analysis/scripts/score_anchoring.py
    data/shapefiles/reference/alberta_2021_csds.gpkg
"""
from __future__ import annotations

# Version: 0.9 (2026-04-26)


import argparse
import sys
import warnings
from pathlib import Path

import geopandas as gpd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
CSD_GPKG = data_loader._resolve_path("data") / "shapefiles" / "reference" / "alberta_2021_csds.gpkg"

CITY_CSDTYPES: set[str] = {"CY", "SM"}  # City + Specialized Municipality
AREA_SHARE_THRESHOLD: float = 0.05  # 5% of ED area on each side


def score_hybridization(shapefile_path: Path) -> int:
    """Return the count of hybrid EDs in the input shapefile."""
    eds = gpd.read_file(shapefile_path)
    if eds.crs is None:
        raise ValueError(f"{shapefile_path} has no CRS")

    csd = gpd.read_file(CSD_GPKG).to_crs(eds.crs)
    csd["is_city"] = csd["CSDTYPE"].isin(CITY_CSDTYPES)

    # Pre-compute spatial index on CSDs
    sindex = csd.sindex

    n_hybrid = 0
    for _, ed in eds.iterrows():
        ed_geom = ed.geometry
        if ed_geom is None or ed_geom.is_empty:
            continue
        ed_area = ed_geom.area
        if ed_area <= 0:
            continue

        # Candidate CSDs via bbox prefilter
        cand_idxs = list(sindex.query(ed_geom, predicate="intersects"))
        city_share = 0.0
        noncity_share = 0.0
        for ci in cand_idxs:
            c = csd.iloc[ci]
            try:
                inter = ed_geom.intersection(c.geometry)
                if inter.is_empty:
                    continue
                share = inter.area / ed_area
                if c["is_city"]:
                    city_share += share
                else:
                    noncity_share += share
            except Exception:
                continue

        if city_share >= AREA_SHARE_THRESHOLD and noncity_share >= AREA_SHARE_THRESHOLD:
            n_hybrid += 1

    return n_hybrid


def main():
    ap = argparse.ArgumentParser(
        description="Compute hybrid-ED count for a single map shapefile",
    )
    ap.add_argument(
        "--shapefile",
        required=True,
        type=Path,
        help="Path to .shp or .gpkg containing electoral-division polygons",
    )
    args = ap.parse_args()
    if not args.shapefile.exists():
        print(f"ERROR: shapefile not found: {args.shapefile}", file=sys.stderr)
        sys.exit(2)
    if not CSD_GPKG.exists():
        print(f"ERROR: CSD reference layer missing: {CSD_GPKG}", file=sys.stderr)
        sys.exit(2)
    n = score_hybridization(args.shapefile)
    print(n)


if __name__ == "__main__":
    main()
