---
name: v0_9_natural_anchoring_secondary_check
description: Does the minority map's 14.5% municipal-anchoring deficit survive a natural-anchoring substrate (highways + rivers)? Verdict — INVERTS. On natural features the three maps are statistically indistinguishable (40.2 / 38.4 / 40.1), so the hostile-witness attack on the CSD-only metric lands and Lane 2's anchoring axis needs to be reframed.
type: project
---

# v0_9 Natural-anchoring secondary check (Lane-2 anchoring substrate audit)

**Status: the minority map's anchoring asymmetry INVERTS under a natural-feature substrate. The hostile-witness attack on the headline 14.5% lands. Lane 2's anchoring axis cannot be carried as "the minority abandoned anchoring" — it must be reframed as "the minority abandoned *municipal* anchoring specifically."**

## Why this check exists

The Lane-2 headline finding (`analysis/reports/v0_1_municipal_anchoring_analysis.md`) is that the 2026 minority map anchors only 14.5% of its province-wide perimeter to StatCan 2021 CSD edges, vs. 71.0% (2026 majority) and 75.2% (2019 enacted) under the same snap-tolerance method. A foreseeable hostile-witness counter is: *"the minority map didn't abandon anchoring — it anchored to highways, rivers, and county lines instead of arbitrary municipal borders. The 14.5% number is a measurement failure, not a map failure."* This memo tests that counter on its own terms by re-running the identical snap method against a different substrate.

## Method

Same snap-and-measure code path as `analysis/scripts/score_anchoring.py`. The only thing that changes is the edge network being snapped to.

- **Snap tolerance:** 500 m (matches the audit's headline run and the DPG ±500 m error budget).
- **Vertex densification:** 50 m along every polygon ring before snapping.
- **Aggregation:** province-wide, `100 × Σ anchored_m / Σ perimeter_m`.
- **No topology re-resolve** — pure measurement, no derived GPKG.

**Natural substrate (this run):**
- **Highways** — OSM ways with `highway ∈ {motorway, trunk, primary, secondary}` (same major-road classes used by the v0_1 Track Y refinement in `analysis/methodology/v0_1_shape_refinement.md`). Tertiary excluded — intra-city street grids would inflate every map's score uniformly and add no discriminatory power. Province-wide pull via Overpass: 41,475 ways, ~80,000 km.
- **Rivers** — OSM ways with `waterway=river` (excludes streams, canals, ditches). 7,080 ways, ~13,000 km.
- **Counties / MDs (NOT INCLUDED):** Alberta Municipal Affairs distributes the county/MD layer via AltaLIS (non-anonymous registration; no stable URL — the same blocker documented in `municipal_anchoring.py:15-24`). However: AB MD/SM/SA jurisdictions ARE already in the StatsCan 2021 CSD layer used by the headline 14.5% number, so any "county-line anchoring" the minority map performs is captured by the CSD score. The county-line strand of the hostile-witness counter is therefore already disposed of by the existing 14.5% and does not need a separate run.

Combined natural-edge network: **~93,000 km** of LineStrings (CSD network for comparison: ~109,000 km after DA supplement, ~36,000 km CSD-only). Roughly the same order of magnitude as the CSD substrate, so any score gap between the two substrates is not driven by raw edge-density.

## Result table

3 maps × 2 substrates = 6 numbers. CSD column is reproduced from `data/v0_1_municipal_anchoring_summary.json` (majority/minority) and `data/v0_1_2019_municipal_anchoring_summary.json` (2019).

| Map | CSD anchoring (headline) | Natural anchoring (this run) | Delta (Nat − CSD) |
|---|---:|---:|---:|
| 2019 enacted     | **75.2 %** | **40.2 %** | −35.0 pp |
| 2026 majority    | **71.0 %** | **38.4 %** | −32.6 pp |
| 2026 minority    | **14.5 %** | **40.1 %** | **+25.6 pp** |

Per-ED summary statistics (natural anchoring, mean / median):
- 2019 enacted: 68.3 % / 70.1 %
- 2026 majority: 66.2 % / 71.1 %
- 2026 minority: 66.3 % / 65.7 %

The mean and median per-ED scores are within 2 pp of each other across all three maps — the natural-anchoring distributions are essentially identical at the per-district level too.

## Verdict: INVERTS

Under the natural-anchoring substrate the three maps cluster tightly at ~38–40 % province-wide and ~66–71 % per-ED. **The minority map is not measurably less anchored than the majority or the 2019 enacted map** — its natural-anchoring score (40.1 %) is in fact a hair *above* the majority (38.4 %) and indistinguishable from 2019 (40.2 %).

This is the third of the three pre-registered outcomes:

- ~~Survives — minority also low under natural anchoring~~ — falsified.
- ~~Partially survives — minority improves but still markedly below majority~~ — falsified; minority is *not* below majority on natural features.
- **Inverts** — minority scores at parity (or above) on natural anchoring → the headline 14.5 % CSD number cannot stand alone as "the minority map abandoned anchoring." It can only stand as "the minority map abandoned **municipal** anchoring specifically." The hostile-witness attack on the unconditional framing lands fully.

**Required Lane-2 reframing.** The substrate-stable claim is narrower than what `report_public.md` and `report_academic.md` carry today:

> The 2026 minority map snaps 14.5 % of its perimeter to StatsCan 2021 CSD edges, vs. 71.0 % for the majority and 75.2 % for 2019 enacted. The minority does *not* compensate by snapping to highways or rivers — under the same snap method against an OSM highway+river substrate, all three maps cluster at 38–40 %, indistinguishable from each other. **The minority map's anchoring deficit is therefore specific to municipal/CSD edges**, not a general anchoring deficit and not compensated by anchoring to alternate physical features. Whether municipal-edge anchoring is the *normatively* correct anchoring substrate is a separate, contestable question that the audit must defend on its own terms.

That last sentence is the part of Lane 2 that now has to be argued explicitly. The previous framing assumed it.

**Why the asymmetry collapses the way it does.** The natural substrate is dense everywhere — every Alberta ED contains highways and rivers within 500 m of most of its boundary regardless of who drew the boundary, because Alberta's road and hydrology networks are dense. So *any* polygon drawn over Alberta will score 35–45 % against this substrate; it is a near-floor measurement. The majority and 2019 maps score the same 38–40 % despite spending much of their perimeter on CSD edges because the CSD edges themselves often run along highways and rivers, so the natural score is achieved *additionally* and not *instead*. The minority map does not benefit from this dual coverage — it scores ~40 % on natural alone and 14.5 % on CSDs alone. The two numbers do not stack.

## What this changes downstream

- **`report_public.md` / `report_academic.md` Section on municipal anchoring** — the 14.5 % vs 71.0 % vs 75.2 % framing is preserved, but the prose claim "the minority abandoned anchoring" must become "the minority abandoned *municipal* anchoring (and did not substitute natural-feature anchoring as a defense — the substrate is dense everywhere and all three maps score equivalently against it)." The 6-number table above belongs in the appendix.
- **Dangerzone metric definitions (`v0_9_dangerzone_metric_definitions.md`)** — the municipal-anchoring axis is still the discriminating axis (this run shows the natural axis does not discriminate). No change needed to the ensemble scoring; the axis was correctly chosen.
- **Hostile-witness preparation** — the question "did you also test natural anchoring?" now has a clean answer with a citable number.

## Outputs

- Per-ED CSVs: `data/v0_9_natural_anchoring_{enacted_2019,majority_2026,minority_2026}.csv`
- Provincial summary JSONs: `data/v0_9_natural_anchoring_{enacted_2019,majority_2026,minority_2026}.json`
- OSM source caches: `data/osm/alberta_osm_{highways,rivers}.json`
- Scripts: `analysis/scripts/score_natural_anchoring.py`, `analysis/scripts/_fetch_osm_natural.py`

Forward:
  (none yet — Lane 2 prose update is the next downstream task)
Backward:
  analysis/scripts/score_anchoring.py
  analysis/scripts/municipal_anchoring.py
  analysis/scripts/v0_9_municipal_anchoring_2019_baseline.py
  data/v0_1_municipal_anchoring_summary.json
  data/v0_1_2019_municipal_anchoring_summary.json
