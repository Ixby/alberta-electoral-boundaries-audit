---
name: reock_verdict
description: Reock compactness per district for both 2026 maps. Contains results for both v0_9 derived substrate and canonical EA shapefiles.
type: project
---

# Reock verdict

## Canonical EA shapefiles (authoritative, 2026-05-18)

**Inputs:** `ea_minority_2026_eds.gpkg`, `ea_majority_2026_eds.gpkg` (official Elections Alberta, received 2026-05-06).
**Script:** `analysis/scripts/reock.py` (canonical path preference via `_pick_gpkg()`).
**Data:** `data/reock_per_district.csv` (178 rows, 89 minority + 89 majority).
**CRS:** EPSG:3401 (Alberta 10-degree TM).
**Algorithm:** `shapely.minimum_bounding_circle` (GEOS, Shapely 2.0+) with Welzl fallback.

| Metric | Minority | Majority |
|---|---|---|
| EDs scored | 89/89 | 89/89 |
| Mean Reock | **0.465** | 0.453 |
| Median Reock | 0.463 | 0.458 |
| Reock < 0.30 | **4/89 = 4.5%** | 6/89 = 6.7% |

**Bottom 5 by Reock (minority):** Calgary-Mountainview 0.227, Calgary-Hays 0.229, Calgary-De Winton 0.285, Calgary-Peigan-Chestermere 0.300, Canmore-Kananaskis 0.305.

**Bottom 5 by Reock (majority):** Calgary-McKenzie 0.168, Calgary-West-Elbow Valley 0.178, Canmore-Banff 0.219, Calgary-Glenmore-Tsuut'ina 0.251, Okotoks-Diamond Valley 0.287.

**Named lasso districts (canonical):**

| District (minority) | Reock (canonical) | Flag (Reock < 0.30) |
|---|---|---|
| Calgary-Nolan Hill-Cochrane | 0.357 | not flagged |
| Calgary-Foothills-Airdrie West | 0.345 | not flagged |
| Edmonton-Enoch-Devon | 0.562 | not flagged |
| Stony Plain-Drayton Valley | 0.411 | not flagged |
| Rocky Mountain House-Banff Park | 0.640 | not flagged |
| majority Stony Plain-Drayton Valley | 0.347 | not flagged |

**Interpretation.** Under canonical EA geometry, the majority map has more below-threshold districts (6 vs 4) and a lower mean Reock. The direction from the v0_9 derived analysis (minority less compact, ~2.58× asymmetry) does not hold under official geometry. None of the named lasso districts are flagged by Reock on canonical EA shapefiles. The canonical Reock metric does not independently support a "minority systematically less compact" conclusion.

**Why canonical differs from v0_9.** The v0_9 substrate dissolved VA polygons to produce ED shapes — VA polygon boundaries contribute to the perimeter and bounding-circle, creating granular geometry that penalises elongated corridors more severely. The canonical EA shapefiles use clean administrative boundary lines and have fewer perimeter vertices. Compactness scores are generally higher (better) on canonical geometry, and the minority's corridor-shaped EDs are less penalised at this resolution.

---

# v0_9 Reock verdict (historical — derived substrate)

**Status: SUPERSEDED by canonical EA results above. Retained for delta comparison.**

**Status at writing:** claim survives, and survives more cleanly than under Polsby-Popper. Reock is the metric on which the chair's "lasso-shaped corridor" framing actually has teeth.

## Headline

Four of the five publicly-named lasso districts in the **minority** are below the conventional Reock < 0.30 flag threshold under the v0_9 substrate; the fifth is above. The one outlier is the rural Rocky Mountain House-Banff Park district, where the minimum bounding circle is dominated by a single linear corridor along the eastern Rockies — the geometry is non-compact under PP (perimeter), but its enclosing circle is not pathologically large relative to its area.

**Status: claim survives, and survives more cleanly than under Polsby-Popper.** Reock is the metric on which the chair's "lasso-shaped corridor" framing actually has teeth.

## Headline

Four of the five publicly-named lasso districts in the **minority** are below the conventional Reock < 0.30 flag threshold under the v0_9 substrate; the fifth is above. The one outlier is the rural Rocky Mountain House-Banff Park district, where the minimum bounding circle is dominated by a single linear corridor along the eastern Rockies — the geometry is non-compact under PP (perimeter), but its enclosing circle is not pathologically large relative to its area.

| District (minority) | PP (v0_9) | Reock (v0_9) | Reock flag |
|---|---|---|---|
| Calgary-Foothills-Airdrie West | 0.140 | **0.051** | flagged |
| Edmonton-Enoch-Devon | 0.065 | **0.082** | flagged |
| Stony Plain-Drayton Valley | 0.175 | **0.210** | flagged |
| Calgary-Nolan Hill-Cochrane | 0.402 | **0.230** | flagged |
| Rocky Mountain House-Banff Park | 0.414 | 0.569 | NOT flagged |

The Calgary-Nolan Hill-Cochrane row is the most consequential: this is the chair's named lasso. **PP scored it 0.402 (moderate)**, prompting the v0_9 PP verdict to caveat that the lasso descriptor had to rest on visual judgement rather than a metric. **Reock scores it 0.230 — well below the 0.30 flag threshold.** The two metrics disagree because PP penalises perimeter wiggle (Calgary-Nolan Hill-Cochrane has fairly clean boundaries), whereas Reock penalises elongation — and an elongated narrow-waist corridor is *exactly* what a "lasso" shape looks like to the bounding-circle test. Reock is the right metric for this claim.

For comparison: the **majority's** Stony Plain-Drayton Valley scores Reock 0.419 — comfortably above the threshold, mirroring the PP result. Same name, different geometry, opposite verdict in both metrics.

## Asymmetry

v0_9 (full 89/89 coverage, both maps):

| Metric | Minority below threshold | Majority below threshold | Asymmetry |
|---|---|---|---|
| PP < 0.25 | 27 / 89 = 30.3 % | 20 / 89 = 22.5 % | ~1.35× |
| **Reock < 0.30** | **31 / 89 = 34.8 %** | **12 / 89 = 13.5 %** | **~2.58×** |

Means: minority Reock 0.371 vs majority Reock 0.408 (38 thousandths apart, similar magnitude to the PP gap of 22 thousandths). The share-below-threshold gap, however, is ~2.6× rather than PP's ~1.35× — Reock is a more discriminating metric here because it penalises the long-thin corridor pattern that the minority disproportionately uses to glue Calgary-suburban polygons to ex-urban rural municipalities.

Bottom-10 by Reock on the minority is dominated by Calgary EDs with elongated bounding circles (Calgary-Foothills-Airdrie West 0.051, Calgary-Falconridge 0.054, Calgary-De Winton 0.059, Calgary-South 0.059, Calgary-Currie 0.073). The majority's bottom-10 is shorter and tops out at higher values (worst is Edmonton-Glenora-Riverview at 0.082; only 12 EDs are below 0.30 vs 31 for the minority).

## Did the claim survive?

**Yes — directionally clearer than PP.** The pre-registered prediction was that the minority is less compact than the majority and that the named lasso districts are flagged by a compactness metric. Reock confirms both, with the asymmetry larger and the chair's named district *correctly flagged* (PP did not flag it). The remaining caveat is Rocky Mountain House-Banff Park, which fails neither metric well — its shape is rural-corridor-as-natural-feature rather than gerrymander-by-design, which is consistent with a real-world geographic constraint.

Reporting recommendation: lead with Reock for the lasso framing in `report_public.md` and `report_academic.md`, retain PP as the secondary perimeter-based metric, and note the ~2.6× asymmetry under Reock as the headline number.

## Data

`data/reock_per_district.csv` (178 rows: 89 minority + 89 majority). Script: `analysis/scripts/reock.py`. Implementation uses `shapely.minimum_bounding_circle` (GEOS, Shapely 2.0+) with a Welzl fallback for older Shapely; both reproduce.
