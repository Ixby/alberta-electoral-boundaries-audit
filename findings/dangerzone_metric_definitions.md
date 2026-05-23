---
name: Dangerzone metric definitions (Lane-2 substrate-stable axes)
description: Operational definitions and validation for the two scoring functions (municipal-anchoring %, hybrid-ED count) that will plot the Nov 2 Lunty 91-seat map against the 100,000-plan ReCom ensemble. Anchoring reproduces the published 71.0/14.5/75.2 numbers exactly on the DPG v0_2 substrate (now SUPERSEDED — see banner; canonical equivalents are majority 80.0% / minority 72.0%). Hybridization cannot reproduce the published 9/25/8 - those are a manual taxonomy, not a computable rule. The directional finding survives on canonical geometry only as hybridization; the anchoring half was retracted.
type: project
---

> **Status — partially SUPERSEDED on canonical geometry. Read this first.**
> The script-validation table below confirms that the anchoring scorer reproduces the **published DPG-era numbers (71.0% majority / 14.5% minority / 75.2% 2019-enacted)** exactly on the v0_2 DPG substrate it was developed against. Those *published* numbers were retracted on canonical recomputation: on official Elections Alberta shapefiles (received 2026-05-06), the same methodology produces **majority 80.0% / minority 72.0%** — both within the 70–85% Canadian comparator norm — and the 4.9× DPG-era asymmetry **does not survive** (see README §"What the audit finds" and methods-paper §7.1, Stage 9).
>
> What this file still validly demonstrates: (i) the scorer is deterministic and reproduces *its* substrate's anchoring number to ±0.2 pp; (ii) the methodology transfers across substrates. What this file should **not** be read as: a claim that 71.0% / 14.5% / 75.2% are live numbers — they are DPG-era validation targets only. The hybrid-count axis (the second scoring function) is unaffected by the canonical recomputation and remains a live Lane-2 leg.

> **Backward:**
> - `analysis/scripts/score_anchoring.py` — companion CLI scorer (municipal-anchoring %)
> - `analysis/scripts/score_hybridization.py` — companion CLI scorer (hybrid ED count)
> - `analysis/scripts/municipal_anchoring.py` — headline anchoring methodology source
> - `analysis/scripts/packing_cracking_analysis.py` — manual MAJORITY/MINORITY mapping reference
> - `data/shapefiles/reference/alberta_2021_csds.gpkg` — StatsCan 2021 CSD reference layer
> - `data/shapefiles/derived/v0_2_canonical_majority_2026_eds_topoclean.gpkg`, `data/shapefiles/derived/v0_2_canonical_minority_2026_eds_topoclean.gpkg`
> - `data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`
> - 100,000-plan ReCom ensemble for Nov 2 distribution comparison
>
> **Forward:**
> - November 2 Lunty 91-seat classification — uses both metrics on the new map
> - `findings/municipal_anchoring_analysis.md` — anchoring leg
> - `reports/public/report_public.md`, `reports/academic/report_academic.md` — checklist sources
> - `findings/README.md` — indexes this finding

# Dangerzone metric definitions (Lane-2 substrate-stable axes)

**Pipeline step 1 of 3.** Pre-registers the two axes the November classification framework will use. The Nov 2 Lunty 91-seat map will be scored on both metrics, plotted against the 100,000-plan ReCom ensemble's distribution on the same metrics, and classified by where it lands relative to a pre-registered threshold line drawn before the Nov 2 release.

**Companion scripts:**
- `analysis/scripts/score_anchoring.py` (CLI: `--shapefile PATH` -> float)
- `analysis/scripts/score_hybridization.py` (CLI: `--shapefile PATH` -> int)

Both scripts take a single polygon shapefile (ED-level, any CRS) and emit a single number. Identical reference layer (StatsCan 2021 CSDs) for both, so the two axes share substrate.

## Metric 1: Municipal anchoring %

**Operational definition.** Load the input shapefile; load the StatsCan 2021 CSD boundaries (`data/shapefiles/reference/alberta_2021_csds.gpkg`) and reproject to the input CRS; union all CSD boundaries into one MultiLineString edge network. For every polygon in the input, walk its boundary at 50 m vertex spacing; for each densified vertex, snap to the nearest CSD edge if and only if the edge is within 500 m. Sum the original-densified segment length whose head-vertex was snapped (the "anchored" perimeter). Return `100.0 * total_anchored_m / total_perimeter_m` rounded to one decimal.

**Parameters held identical to the audit's headline run** (`analysis/scripts/municipal_anchoring.py`): `SNAP_TOL_M = 500.0`, `VERTEX_DENSIFY_M = 50.0`, `USE_DA_SUPPLEMENT = False`. No topology re-resolve pass (we are computing a metric, not producing a v0_4 GPKG). The headline numbers in `findings/municipal_anchoring_analysis.md` were produced from `v0_2_canonical_*_topoclean.gpkg` substrates with `USE_DA_SUPPLEMENT = False`; same substrate is used for validation here.

## Metric 2: Hybrid ED count

**Operational definition.** An electoral division is HYBRID iff its territorial area intersects:
1. at least one StatsCan 2021 CSD of type `CY` (City) or `SM` (Specialized Municipality e.g. Strathcona County, Wood Buffalo) contributing **>= 5%** of the ED's area, AND
2. at least one CSD of any non-(`CY`|`SM`) type (`T`, `MD`, `IRI`, `VL`, `SV`, `ID`, `SA`) contributing **>= 5%** of the ED's area.

Equivalently: the ED's territory bridges a Census-defined city and at least one non-city administrative unit, with each side holding at least 5% of the ED's land. Treating SM as city-equivalent matches the audit's narrative usage (Sherwood Park / Fort McMurray are SMs but are never described as "rural hybrids").

**Why an operational definition was needed.** The published 9/25/8 hybrid counts (`report_public.md:248`, `report_academic.md:2156`, `REPRODUCING.md:132`) are NOT computed by any script in the repository. Verified: no Python script in `analysis/scripts/` produces 9, 25, or 8 directly; the closest taxonomies (`is_hybrid` boolean in `data/majority_2026_populations.csv` = 19 majority hybrids; `region_type` `-hybrid`/`-merged` in `data/minority_2026_populations.csv` = 21 minority hybrids; the manual `MAJORITY_2026_MAPPING` / `MINORITY_2026_MAPPING` "blend" entries in `analysis/scripts/packing_cracking_analysis.py` = 14 majority / 17 minority blends, or 15/21 with merges) all give different totals. The 9/25/8 numbers are a manual narrative classification by the audit author, enumerated in prose at `report_public.md:252-255`. **This is the most important finding in this memo:** the published hybrid count cannot be re-implemented from the geometry without a manual taxonomy step, so a different operational definition is required for the 100k-ensemble run.

## Validation results (3 maps x 2 metrics = 6 numbers)

Validation substrates: 2026 maps from `data/shapefiles/derived/v0_2_canonical_{majority,minority}_2026_eds_topoclean.gpkg` (the same v0_2 substrates that produced the headline 71.0%/14.5% numbers); 2019 enacted from `data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`.

| Map | Metric | This script | Published | Delta | Within tolerance? |
|---|---|---:|---:|---:|---|
| 2026 majority | Anchoring % | **71.0** | 71.0 | 0.0 pp | YES (tol +/- 0.2 pp) |
| 2026 minority | Anchoring % | **14.5** | 14.5 | 0.0 pp | YES (tol +/- 0.2 pp) |
| 2019 enacted | Anchoring % | **75.2** | 75.2 | 0.0 pp | YES (tol +/- 0.2 pp) |
| 2026 majority | Hybrid count | **14** | 9 | +5 | NO (tol +/- 2 EDs) |
| 2026 minority | Hybrid count | **17** | 25 | -8 | NO (tol +/- 2 EDs) |
| 2019 enacted | Hybrid count | **8** | 8 | 0 | YES (tol +/- 2 EDs) |

**Anchoring: clean.** All three numbers reproduce the published headline to one decimal, no rounding needed. The script is a faithful CLI wrapper of the existing pipeline and is ensemble-ready.

**Hybridization: divergent on 2 of 3 maps.** The operational definition exactly matches the published 2019 = 8 baseline. It diverges on the 2026 maps in opposite directions: my rule overcounts majority (+5) and undercounts minority (-8). The qualitative finding is preserved (Min > Maj > 2019 in both my measurement: 17 > 14 > 8; and the published: 25 > 9 > 8) but the absolute integers differ.

### Why hybridization diverges from the published narrative

I tested ~15 threshold/measure combinations (area-share, population-share via DA centroids, single-CSD vs. CSD-pair rules, name-pattern rules). **No single computable rule simultaneously matches the published 9/25/8 within +/- 2 EDs on all three maps.** The closest hits:

- City/non-city area-share, both >= 5% (CHOSEN): yields 14/17/8 - exact match on 2019.
- City-pop-share in [10%, 95%]: yields 18/26/17 - within +/-1 on minority but +9 on 2019.
- 2+ distinct CSDs each >= 25% pop: yields 9/12/11 - exact match on majority, but minority way off.

The pattern of misses tells us what the published taxonomy is doing that no computable rule does: **the audit author hand-classified each ED based on intent** ("did the commission draw this district to fuse a city neighbourhood with rural-edge territory, or is it a clean urban subdivision that happens to clip a CSD edge?"). Lasso configurations with thin corridors into adjacent CSDs (Calgary-Nolan Hill-Cochrane, Calgary-Bow-Springbank) carry tiny territorial spillover even though they are the canonical published examples of minority hybridization. The author counted them; an area-share rule does not.

### Recommendation on framework readiness

**Anchoring metric: GO.** It reproduces the published headline exactly across all three maps and is computable on a 100k-plan ensemble at standard wall-clock cost (the pipeline already ran on 89-ED 2026 maps in approximately 60 s per map; ensemble-mode batched runs are mechanically straightforward).

**Hybridization metric: CONDITIONAL GO.** The operational definition (city/non-city area-share, 5%/5%) is computable, defensible in writing, and preserves the directional rank that is the substrate-stable feature of interest. Recommend pre-registering the operational definition as the audit's *measure-of-record for the ensemble run* and adopting the published 9/25/8 as a *narrative footnote* whose values are a separate manual classification - not the same metric, not directly comparable to ensemble percentiles. The Nov 2 map will be scored under the operational definition; its position in the ensemble distribution will use ensemble values, not the published-prose values. This avoids the trap of trying to reproduce a manual taxonomy at scale.

If the PO prefers a hybridization metric that more closely matches the published minority count (25), the alternative city-pop-share-in-[10%, 95%] rule yields 26 minority and 18 majority - within +/-1 on minority but +9 on 2019. That trade is worse, not better, for ensemble use because it inflates the 2019 baseline against which the November map will be benchmarked.

## Threshold-line pre-registration (next step)

Step 2 of the pipeline (separate directive) will draw a pre-registered threshold line in (anchoring %, hybrid count) space from the 100k-ensemble percentiles, before the Nov 2 map is released. Step 3 will plot the Nov 2 map against that distribution and classify it. This memo locks in the axes; the threshold line is a separate decision.
