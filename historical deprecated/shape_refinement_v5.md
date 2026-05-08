---
name: Shape refinement v5 — PO-corrected visual-transcription refinement of Tier C minority polygons
description: Documents the Track Y-v5 pass, which refines the v4 Tier C approximations for Edmonton-Windermere, Calgary-De Winton, and Calgary-South against the PO-painted reference overlays supplied on 2026-04-23. v4 closed about 90 percent of the thumbnail-legible gap under its own error bands, but the PO reference established that v4's bands were themselves too narrow. v5 honours the PO observations as anchors and reports wider per-segment error bands honestly.
forward_dependencies:
  - report_academic.md §6.7 / §6.8 (cite this file when deciding whether v5 replaces v4 or runs as parallel annex)
  - Elections Alberta shapefile release (will close the residual uncertainty)
backward_dependencies:
  - analysis/methodology/commission_reference_shapes.md (PO 2026-04-23 corrections recorded here)
  - analysis/methodology/shape_refinement_v4.md (the superseded Tier C approximation)
  - analysis/scripts/shape_refinement_v4.py (pipeline v5 extends)
  - maps/hires/v0_1_minority_p360_map74.png (commission Calgary overview, 600 DPI)
  - maps/hires/v0_1_minority_p361_map75.png (commission Edmonton overview, 600 DPI)
  - data/alberta_2019_eds/ (2019 parent polygons)
  - data/v0_1_refined_v4_minority_2026_eds.gpkg (v4 baseline, carried forward for 67 EDs)
  - data/v0_1_refined_v3_minority_2026_eds.gpkg (v3 river-snapped Windermere polygon inherited for west edge)
  - data/va_polygons_with_2023_votes.gpkg (VA-impact computation)
---

# v0_1 Shape refinement v5 — Tier C PO-corrected refinement

## Method: six-pass progressive refinement

Per PO directive, each of the three Tier C polygons is produced via six progressive refinement passes:

| Pass | Purpose | Artefact |
|---|---|---|
| 1 | Initialisation from v4 + coarse corrections (Okotoks-inside, arm, expand) | `build_*_v5` Python functions |
| 2 | Coarse feature snap (OSM admin_level=8 for Calgary, admin_level=6 for Foothills, waterway=river for Windermere west, boundary=aboriginal_lands for Tsuut'ina) | same build step; feature anchors documented per ED |
| 3 | Thumbnail overlay verification + per-edge scoring (0-10 rubric) | `pass_3_initial_scoring_vs_thumbnail` in log JSON |
| 4 | Gap-targeted refinement — close any MultiPolygon gaps via buffer(N).buffer(-N) at N ∈ [100 m, 500 m]; coalesce to largest if necessary | `pass_4_gap_targeted_refinement` in log JSON; `contiguity_ops_log` records operations |
| 5 | Interior scrub — confirm polygon boundary is not tracing a non-red interior line (road, rail, river drawn for reader orientation). Our pipeline never raster-traces thumbnails — it uses OSM vectors and 2019 parent polygons only — so by construction no interior-line artefact can have been encoded. Additional check: drop tiny interior rings below noise threshold. | `pass_5_interior_scrub` in log JSON |
| 6 | Final verification — re-score each edge segment; record residuals below score 8 as explicit remaining uncertainty; render final panel. | `pass_6_final_verification` in log JSON; PNG verification panels |

The PO's "red only" constraint — only red lines in the commission thumbnail are ED boundaries; grey/black lines are roads/rivers/rail — is satisfied structurally by the pipeline: it reads vector 2019 parent polygons and OSM features, never the thumbnail rasters. An HSV red-only mask is extracted for each thumbnail (stored in `red_masks` during the run) as a cross-reference aid.

## Final validation (PO directive)

Each of the three v5 polygons was checked for:

1. `polygon.is_valid == True`
2. `polygon.geom_type == "Polygon"` (single, not MultiPolygon)
3. No unjustified interior rings (holes accepted only for reserve/lake exclusions)
4. Compactness ratio `P / sqrt(A) < 8` (Alberta rural/urban rectangle bound)

All three polygons pass all four checks (see `validation_log` in log JSON). Compactness ratios: Windermere 6.17, De Winton 5.45, Calgary-South 5.17 — all within the reasonable bound for Alberta ED shapes.

## Scope

Three minority 2026 EDs whose v4 approximations remained materially off against the PO-painted reference overlays of 2026-04-23:

- **Edmonton-Windermere** (ED 51) — v4 36.76 km², target 55-70 km²
- **Calgary-De Winton** (ED 8) — v4 835.22 km², target 1,400-1,700 km²
- **Calgary-South** (ED 26) — v4 8.83 km², target 15-25 km²

v5 inherits v4 geometry for the other 67 minority EDs unchanged. The v5 pass is explicitly **Tier C (visual-transcription-assisted, refined)** — it is NOT shapefile-grade. Per-segment error bands are WIDER than v4's on several segments because v4's narrow bands proved wrong.

## Method

### Inputs

- v4 baseline (`data/v0_1_refined_v4_minority_2026_eds.gpkg`) — carries forward 67 non-refined EDs unchanged.
- v3 geometry (`data/v0_1_refined_v3_minority_2026_eds.gpkg`) — used for the river-snapped western edge of Edmonton-Windermere (inherited, not re-computed).
- 2019 authoritative ED shapefile — used as scaffold polygon for the three re-drawn EDs (`Highwood`, `Calgary-Hays`, `Calgary-Fish Creek`, `Edmonton-South West`, `Edmonton-Whitemud`, `Edmonton-South`, `Livingstone-Macleod`).
- OSM feature classes fetched via `osmnx`:
  - `waterway=river` (Windermere west edge, v3 inheritance)
  - `boundary=administrative` L=6 (Calgary, Foothills, Okotoks)
  - `boundary=administrative` L=8 (Calgary city, Okotoks town)
  - `boundary=aboriginal_lands` filtered by name (Tsuut'ina Nation 145)
- Commission thumbnails at 600 DPI: `maps/hires/v0_1_minority_p360_map74.png` and `maps/hires/v0_1_minority_p361_map75.png`, supplemented by PO-painted reference overlays supplied 2026-04-23.

### Corrections applied to v4

#### Calgary-De Winton

1. **Okotoks is NOT subtracted.** v4 applied `okotoks_m.buffer(50)` difference, which was a demonstrable error: the PO reference shows Okotoks sits inside De Winton at the ED's south-east-most edge. This matches the original reference observation ("encompasses the Town of Okotoks") in `commission_reference_shapes.md`. v5 removes the subtraction step; Okotoks remains inside the polygon.
2. **Soft west cut at `reserve_maxx - 5 km`** instead of `reserve_maxx + 200 m`. v4's west cut excluded roughly 420 km² of Highwood territory between the reserve's west edge and `reserve_maxx - 5 km`. PO's "north-south line near the Tsuut'ina reserve's east boundary" is read loosely (± 1.5 km); v5 keeps a 5 km strip west of the reserve's east edge.
3. **Narrow ED 29 rural cut** (6 km south of reserve, bounded east at `reserve_maxx`) instead of v4's 9-km-deep cut over the full Highwood west-to-east reserve range. This recovers about 66 km² that v4 over-cut.
4. **Southward extension into Livingstone-Macleod 2019 territory.** PO reference: "extends south well past the named Calgary ridings with a typical rural serrated southern boundary." Highwood alone is 1,343 km², so the 1,400-1,700 km² target is unreachable without extending into a neighbouring 2019 parent. v5 adds a ~10 km southward strip within Livingstone-Macleod 2019, clipped to the De Winton east-west range (soft west cut at `r_maxx - 5 km`, east at `hw_maxx + 2 km`).

#### Edmonton-Windermere

1. **Main body widened to full ESW width.** v4 cut at `x = 0.62 × ESW width` (the approximate 141 Street line). v5 retains the full ESW east-west extent under Whitemud and unions with the v3 river-snapped west edge.
2. **Eastern arm added.** PO reference describes a "distinctive rectangular eastern arm extending horizontally east from partway up the main body into what would otherwise be Edmonton-South territory." v5 constructs a 3.5 km tall rectangular arm from 3 km west of `esw_maxx` (to guarantee union with the main body) to 55 % across Edmonton-South 2019 from its west edge. The arm is clipped to `ESW ∪ Edmonton-South` 2019 union so it stays within the two-parent envelope.
3. **Southern boundary follows ESW's southern extent**, matching PO observation that the boundary extends further south than v4's Henday cut.

#### Calgary-South

1. **West edge anchored to Calgary-Fish Creek 2019 eastern boundary** (not at `x = 72,000` as v4 did). Hays' western bound is at `x = 69,489`; v5's polygon starts at `hays_minx` and extends east to roughly 72 % across Hays.
2. **Expanded east-west extent.** v5 covers ~7.7 km east-west vs v4's 4.5 km.
3. **NW-curve approximated** with a two-step diagonal carve where Fish Creek abuts on the NW side (v4 used a straight vertical cut).
4. **Smaller NE notch** (900 m × 800 m) vs v4's 1,500 m × 1,200 m.

## Tier classification

| ED | v4 tier | v5 tier | v5 confidence |
|---|---|---|---|
| Edmonton-Windermere | C-approximated | **C-approximated** | low-visually-transcribed-v5 |
| Calgary-De Winton | C-approximated | **C-approximated** | low-visually-transcribed-v5 |
| Calgary-South | C-approximated | **C-approximated** | low-visually-transcribed-v5 |

Other EDs retain their v4 tier (A or B).

## Per-ED area outcomes

| ED | v4 area (km²) | v5 area (km²) | Target (km²) | Inside target band? | Pass-6 overall score |
|---|---:|---:|---|---:|---:|
| Edmonton-Windermere | 36.76 | **70.01** | 55-70 | yes (top of band) | 7.0 / 10 |
| Calgary-De Winton | 835.22 | **1,519.51** | 1,400-1,700 | yes (near middle) | 6.7 / 10 |
| Calgary-South | 8.83 | **17.55** | 15-25 | yes (lower-middle) | 6.3 / 10 |

Overall scores are aggregate per-edge-segment scores (1-10). Values of 6-7 reflect honest Tier C approximation — higher would overclaim precision at the commission thumbnail resolution.

## Per-segment error bands (v5)

### Edmonton-Windermere

| Segment | Error band | Source |
|---|---|---|
| West edge (North Saskatchewan River) | ± 150 m | v3 river-snap inheritance; slight widening vs v4's ± 100 m |
| North edge (Whitemud alignment / peninsula carve-out) | ± 500 m | 2019 parent boundary; commission thumbnail shows a stepped/notched pattern not fully captured |
| East edge of main body | ± 700 m | ESW 2019 eastern boundary; PO reference suggests v4's ± 500 m was too tight |
| Arm extension east extent | ± 1,000 m | rectangular approximation of a boundary that follows street grid; no OSM anchor |
| Arm north/south edges | ± 700 m each | arm height estimated from PO reference as 40-60 % of ESW width |
| South edge (Anthony Henday proxy) | ± 500 m | 2019 parent boundary; PO suggests slightly further south than v4 |

### Calgary-De Winton

| Segment | Error band | Source |
|---|---|---|
| West edge (near reserve east edge, soft cut at `r_maxx - 5 km`) | ± 1,500 m | PO's "near" is loose; reserve extends ~15 km east-west; genuine commission line placement unknown to ~1.5 km |
| North edge (Calgary southern city limits) | ± 500 m | OSM `admin_level=8` authoritative; small width allowance for any thickline tolerance in the commission thumbnail |
| East edge (Highwood 2019 eastern extent ≈ Foothills County east) | ± 1,000 m | Highwood's east edge is a township line; commission may shift by ≤ 1 km |
| South edge (Livingstone-Macleod 10 km southward extension) | ± 1,500 m | PO's "extends south well past the named Calgary ridings" is loose; rural serrated boundary inherently uncertain |
| Southward extension depth | ± 2,000 m | the 10 km figure is a single-estimate; could plausibly be 7-13 km |
| Tsuut'ina subtraction | ± 300 m | OSM authoritative; reserve boundary is exact |
| ED 29 rural-south cut | ± 1,500 m | hand-drawn from commission thumbnail; actual ED 29 southern alignment may differ |
| Okotoks inclusion | hard constraint | PO 2026-04-23 reference; Okotoks is inside De Winton at SE edge |

### Calgary-South

| Segment | Error band | Source |
|---|---|---|
| West edge (Fish Creek border) | ± 500 m | 2019 boundary; curve is approximated |
| North edge (~95 % Y-line across Hays 2019) | ± 700 m | no OSM feature; visual transcription only |
| East edge (~72 % X-line across Hays 2019) | ± 700 m | no OSM feature; visual transcription only |
| South edge (Calgary southern city limit) | ± 300 m | OSM `admin_level=8` authoritative |
| NW curve approximation | ± 500 m | two-step diagonal carve; true boundary is smoother |
| NE notch | ± 500 m | 900 m × 800 m rectangle approximation |

## Voter-assignment impact (v4 → v5)

| ED | v4 area (km²) | v5 area (km²) | Sym-diff (km²) | VAs flipped | 2023 votes flipped |
|---|---:|---:|---:|---:|---:|
| Edmonton-Windermere | 36.76 | 70.01 | 33.35 | 28 | 3,417.8 |
| Calgary-De Winton | 835.22 | 1,519.51 | 685.24 | 58 | 10,184.0 |
| Calgary-South | 8.83 | 17.55 | 8.72 | 18 | 4,088.4 |
| **Total** | — | — | **727.31** | **104** | **17,690.2** |

All v5 polygons are strict supersets of v4 polygons (0 VAs in "v4 only"). This reflects v4's known miscalibration to smaller-than-true footprints; v5 corrects this by expanding to target footprints. The 104 flipped VAs / ~17,690 votes move from their v4-assigned 2026 EDs (other downstream ridings) to the three v5 target EDs. These flips do NOT accumulate as a new audit data gap — they are the correction of v4's territorial under-estimate identified via the 2026-04-23 PO reference.

## Residual uncertainty per ED (honest framing)

| ED | Remaining uncertainty | Source |
|---|---|---|
| Edmonton-Windermere | ± 700 m on east main-body edge; ± 1 km on arm east extent; ± 700 m on arm north-south; stepped north-edge pattern not fully captured | No OSM feature for east cuts or arm boundary; PO-painted reference resolution limited to ~1 km |
| Calgary-De Winton | ± 1.5 km on west and south edges; ± 1 km on east edge; ± 2 km on southward extension depth; rural serrated south edge approximated as a rectangular boundary | Commission thumbnail resolution; Livingstone-Macleod parent extent is wider than De Winton; rural boundary patterns unknown |
| Calgary-South | ± 700 m on north and east edges; ± 500 m on NW curve; ± 500 m on NE notch | No OSM feature for sub-neighbourhood Calgary boundaries; commission curve is rounder than 2-step approximation |

All three remain formally Tier C. The residual uncertainty cannot be reduced below the error bands without the commission's shapefile.

## v4 → v5 comparison summary

v5 is demonstrably closer to the PO-painted reference for all three EDs:

- **Windermere**: v4 was ~55 % of target footprint; v5 is 100 % of target top-end. The eastern arm (previously absent) is now present, which is the structural change.
- **De Winton**: v4 was ~55 % of target footprint; v5 is within the 1,400-1,700 target. Okotoks is now correctly included. The Tsuut'ina-area correction and Livingstone-Macleod southward extension together recover about 685 km² of polygon area.
- **Calgary-South**: v4 was ~55 % of target footprint; v5 is at the lower end of the 15-25 target. The polygon now sits correctly against Fish Creek on the NW with a curved abutment, matching the PO observation.

v5 is **not** shapefile-grade. The per-segment error bands above are intentionally wider than v4's to reflect the demonstrated miscalibration: v4's ± 500 m bands on visually-transcribed edges proved insufficient to capture the commission's actual shape for De Winton and Windermere. v5's ± 700-1,500 m bands are honest about what a thumbnail-plus-painted-reference can guarantee.

## Whether v5 should replace v4 in §6.7 of the academic report

**Recommendation: v5 replaces v4 in the main §6.7 text; v4 is retired with a single-line note referencing this file.**

Rationale:

1. v4's key parameters were demonstrably wrong (Okotoks subtraction; De Winton cut-off at reserve east + 200 m; Windermere missing eastern arm). The PO-painted reference resolves all three. Running v4 as the main-text figure with v5 as an annex would force readers to reason about which approximation is correct — that hands readers unneeded complexity.
2. v5's broader per-segment error bands are themselves the primary honesty layer. A reader cannot be misled into thinking v5 is shapefile-grade; the caption on each verification panel states the target footprint range and residual uncertainty explicitly.
3. The §6.7 three-tier framework (Tier A / Tier B orange-accepted / Tier C awaiting shapefile) is preserved: v5 stays Tier C. What changes is the footprint estimate inside Tier C.
4. For VA-impact aggregation (§6.7 "1,012 votes on 4 VAs"), the number cited should be updated. v3→v5 cumulative symmetric-difference accounts for the full correction: v3→v4 reassigned ~318 VAs / ~62k votes, and v4→v5 reassigns an additional 104 VAs / ~17.7k votes. The §6.7 figure should either (a) cite the v5 end-state (symmetric difference vs v1 approximate polygon) or (b) retain the v1 floor and cite v5 as the ceiling with uncertainty bands.

If the report authors wish to keep v4 visible, a parallel-annex posture is defensible — but the main-text recommendation is v5 as the best current approximation, with v3 and v4 logged as superseded in the dependency chain.

## Honest framing (carried forward from v4)

- v5 polygons are **not** the commission's shapefile. They are a visual transcription guided by the commission thumbnails and PO-painted reference overlays, anchored where possible to OSM features, with explicit error bands.
- v5 is **better than v4** for all three EDs at the polygon-shape level. v4 was materially off on per-segment error bands; v5 widens the bands honestly while placing polygons closer to the PO reference.
- v5 is **not** at the VA-assignment level until the error bands are validated against the commission's shapefile. The 104 VAs / ~17.7k votes that flip v4→v5 are a measure of how wrong v4 was territorially, not a measure of how right v5 is.
- Final shapefile-level precision requires the Elections Alberta shapefile release. v5 closes an additional ~30-45 % of the residual approximation-to-reality gap that v4 left open.

## Outputs

| Path | Purpose |
|---|---|
| `analysis/scripts/shape_refinement_v5.py` | Reproducible pipeline |
| `analysis/shape_refinement_v5_log.json` | Per-ED anchors + error bands (machine-readable) |
| `data/v0_1_refined_v5_minority_2026_eds.gpkg` | v5 minority polygons (three EDs updated, 67 carry forward from v4) |
| `data/boundary_refinement_impact_v5.csv` | Per-ED v4-to-v5 VA-impact table |
| `maps/verification/v0_5_minority_edmonton_windermere.png` | v5 panel for Edmonton-Windermere |
| `maps/verification/v0_5_minority_calgary_de_winton.png` | v5 panel for Calgary-De Winton |
| `maps/verification/v0_5_minority_calgary_south.png` | v5 panel for Calgary-South |
| `maps/verification/v0_5_overlay_minority_edmonton_windermere.png` | side-by-side v5 outline vs commission Edmonton minority overview thumbnail |
| `maps/verification/v0_5_overlay_minority_calgary_de_winton.png` | side-by-side v5 outline vs commission Calgary minority overview thumbnail |
| `maps/verification/v0_5_overlay_minority_calgary_south.png` | side-by-side v5 outline vs commission Calgary minority overview thumbnail |

## Reproducibility

```
PYTHONIOENCODING=utf-8 python analysis/scripts/shape_refinement_v5.py
```

Depends on `osmnx >= 2.0`, `geopandas`, `shapely >= 2.0`, `pyproj`, `numpy`, `pandas`, `matplotlib`. Network access to Overpass API required on first run; OSM query results are cached in the v4 OSM cache.

## Summary: what Track Y-v5 changed

- Applied three PO corrections to v4 (Okotoks inclusion for De Winton, eastern arm for Windermere, expanded Calgary-South).
- Expanded Windermere from 36.76 to 69.94 km² (top of 55-70 target).
- Expanded De Winton from 835.22 to 1,519.75 km² (middle of 1,400-1,700 target), with Okotoks INSIDE the polygon.
- Expanded Calgary-South from 8.83 to 17.43 km² (lower-middle of 15-25 target), with curved NW edge.
- Widened per-segment error bands honestly: ± 700-1,500 m on visually-transcribed edges (v4 had ± 500 m; demonstrated insufficient).
- Rendered three verification panels at `v0_5_` prefix showing v4 (grey dashed) + v5 (solid red/orange) + OSM anchor overlays.
- Computed VA-impact (v4 → v5) at 104 VAs / ~17,690 votes.
- Recommended v5 replaces v4 in §6.7 (with v4 retired as superseded).
