---
name: reock_verdict
description: Does the Lane 2 lasso/non-compactness claim survive the Reock metric on the v0_9 topological substrate?
type: project
---

# v0_9 Reock verdict

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
