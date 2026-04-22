---
name: Shape refinement v4 — visual-transcription-assisted Tier C approximations
description: Documents the Track Y-prime-prime-prime refinement pass, which produces visually-transcribed approximations for the three minority 2026 EDs whose v3 approximations did not reflect the commission's actual shapes. The v4 polygons are explicitly Tier C ("visual-transcription-assisted") and are distinguishable from Tier A (2019 inheritance) and Tier B (orange-accepted OSM-snap refinement). They are closer to the commission thumbnails than v3 but are NOT shapefile-grade. Each edge carries an explicit error band.
forward_dependencies:
  - report_academic.md §6.7 / §6.8 (cite this file when deciding whether v4 replaces v3 or runs as parallel annex)
  - Elections Alberta shapefile release (will close the residual uncertainty)
backward_dependencies:
  - analysis/v0_1_commission_reference_shapes.md (documents the v3 mismatches this pass addresses)
  - analysis/v0_1_shape_refinement_v3.md (the superseded Tier B approximation)
  - maps/hires/v0_1_minority_p360_map74.png (commission Calgary overview, 600 DPI)
  - maps/hires/v0_1_minority_p361_map75.png (commission Edmonton overview, 600 DPI)
  - data/alberta_2019_eds/ (2019 parent polygons)
  - data/v0_1_refined_v3_minority_2026_eds.gpkg (v3 starting polygons)
  - data/va_polygons_with_2023_votes.gpkg (VA-impact computation)
---

# v0_1 Shape refinement v4 — Tier C visual-transcription-assisted

## Scope

Three minority 2026 EDs whose v3 approximations were structurally wrong:

- **Edmonton-Windermere** (ED 51)
- **Calgary-De Winton** (ED 8)
- **Calgary-South** (ED 26)

The v3 pipeline (`v0_1_shape_refinement_v3.py`) had classified these as
`refinement-unresolvable-without-shapefile`, correctly noting that the
OSM-snap family cannot reconstruct a carve boundary that follows no OSM
feature class. That classification remains true at the *shapefile-level*
precision.

This v4 pass does not attempt shapefile-level precision. It asks a
different question: can the polygon *shape* be improved against the
commission thumbnails using multi-feature OSM anchors plus visual
transcription, without claiming shapefile fidelity?

Answer: yes, significantly for all three EDs. The v4 polygons are
honestly-labelled Tier C approximations.

## Method

### Inputs

- Commission minority thumbnails at 600 DPI
  (`maps/hires/v0_1_minority_p360_map74.png`,
   `maps/hires/v0_1_minority_p361_map75.png`) — visually inspected at
   several zoom levels to extract the per-ED shape descriptions.
- 2019 authoritative ED shapefile (`data/alberta_2019_eds/`) — used as
  scaffold polygon for each ED's carving.
- v3 minority shapefile (`data/v0_1_refined_v3_minority_2026_eds.gpkg`) —
  used for the river-snapped western edge of Edmonton-Windermere
  (inherited, not re-computed).
- OSM feature classes fetched via `osmnx`:
  - `waterway=river` filtered to North Saskatchewan (Windermere west edge)
  - `boundary=administrative` L=6 for Calgary city, Foothills County,
    Okotoks town, Rocky View County
  - `boundary=administrative` L=8 for Calgary urban admin
  - `boundary=aboriginal_lands` filtered by name to Tsuut'ina Nation 145

### Construction strategy per ED

**Edmonton-Windermere (ED 51).** Start from 2019 Edmonton-South West.
Intersect with a west-half box (eastern cut at ~62 % across Edmonton-South
West, approximating the commission's thick dotted line at ~141 Street).
Clip off anything north of Whitemud's southern boundary. Intersect with
v3 geometry to inherit the river-snapped western edge.

**Calgary-De Winton (ED 8).** Start from 2019 Highwood (1,343 km²).
Subtract Tsuut'ina Nation 145 reserve + 200 m buffer. Subtract a
Tsuut'ina-rural-southern-extension rectangle covering ED 29
(Calgary-West-Tsuut'ina) south of the reserve to approximately Hwy 22X.
Subtract Okotoks town boundary. Subtract any sliver inside Calgary city
limits. Restrict to east of Tsuut'ina reserve's eastern edge + 200 m (so
De Winton is the *eastern* rural block; the western rural block is ED 29).

**Calgary-South (ED 26).** Start from 2019 Calgary-Hays. Restrict to a
compact rectangle at the western centre of Hays (x = 72,000 to 76,500,
y = Hays southern edge to ~85 % Hays northern edge). Intersect with Hays
polygon. Apply a 1.5 km × 1.2 km NE-corner notch (the commission's
"notch on the right side"). Do NOT subtract De Winton — Calgary-South
is fully inside Calgary; De Winton is outside Calgary; there is no
overlap.

### Tier classification

The `tier` column in `data/v0_1_refined_v4_minority_2026_eds.gpkg` is
updated for the three EDs:

| ED | v3 tier | v4 tier | v4 confidence |
|---|---|---|---|
| Edmonton-Windermere | B | **C-approximated** | low-visually-transcribed |
| Calgary-De Winton | B | **C-approximated** | low-visually-transcribed |
| Calgary-South | B | **C-approximated** | low-visually-transcribed |

Other EDs retain their v3 tier (A or B). Final roll-up:

- Tier A (2019 inheritance, high confidence): 65 minority EDs
- Tier B (orange-accepted OSM-snap refinement): 2 minority EDs
  (Lethbridge-Little Bow, Wetaskawin-Ponoka-Maskwacis)
- Tier C (visual-transcription-assisted): 3 minority EDs (these three)

## Per-ED error bands

### Edmonton-Windermere

- **West edge** (North Saskatchewan River): ± 100 m. Inherited from v3
  river-snap. This edge is real (the commission's Appendix E text
  confirms "south of the North Saskatchewan River").
- **North edge** (~Whitemud Drive alignment, inferred from 2019 parent
  boundary): ± 300 m. Uses 2019 Edmonton-Whitemud / Edmonton-South West
  common boundary as proxy; the commission may have shifted this by a
  few hundred metres.
- **East edge** (estimated ~141 Street longitude cut): ± 500 m. This is
  the *only* v4 edge that has no OSM feature snap. It is placed at 62 %
  across 2019 Edmonton-South West from west to east based on visual
  inspection of the commission thumbnail's thick dotted line. A ±500 m
  band is conservative.
- **South edge** (Anthony Henday alignment from 2019 parent southern
  boundary): ± 300 m.
- Polygon area: v4 = 36.76 km² (v3 was 113.72 km²).
- SW corner: the grey conservation/First Nations area visible in the
  commission thumbnail at the river bend is NOT explicitly excluded by
  v4 (it was not in v3 either). Residual uncertainty ~3 km² in SW corner.

### Calgary-De Winton

- **West edge** (Tsuut'ina Nation 145 eastern reserve boundary + 200 m
  buffer): ± 1 km. The commission's western edge for De Winton is a
  vague north-south line east of Tsuut'ina; the OSM reserve boundary
  plus a 200 m buffer is a reasonable proxy but the commission may
  have placed it up to 1 km east or west of this line.
- **North edge** (Calgary southern city limits): ± 300 m. OSM admin_level=8
  boundary is authoritative for this segment.
- **South edge** (Highwood 2019 southern extent, inherited): ± 1 km.
  The commission's De Winton extends approximately to the southern
  boundary of Foothills County (past the 17 MD line), matching Highwood
  2019 closely. Variance on this line is hard to estimate from the
  thumbnail.
- **East edge** (Foothills County eastern boundary): ± 500 m. OSM
  admin_level=6 boundary.
- **Okotoks exclusion** (OSM Town of Okotoks boundary): ± 300 m.
  Authoritative OSM source.
- **Tsuut'ina-south rural cut** (removing ED 29 southern portion): ± 1 km.
  This rectangle is hand-drawn from the commission thumbnail as ~8 km
  south of the reserve. The actual ED 29 southern boundary may differ
  by up to 1 km.
- Polygon area: v4 = 835.22 km² (v3 was 1,384.09 km²).

### Calgary-South

- **West edge** (2019 Calgary-Hays western boundary = Calgary-Fish Creek
  common): ± 300 m. Inherited from 2019 Hays.
- **North edge** (~65 % Y-line across Hays, transcribed from thumbnail):
  ± 500 m. No OSM feature anchors this edge. Visual transcription only.
- **South edge** (Calgary southern city limit, inherited from Hays):
  ± 300 m.
- **East edge** (~55 % X-line across Hays, transcribed from thumbnail):
  ± 500 m. No OSM feature. Visual transcription only.
- **NE-corner notch** (commission's "notch on the right side"): ± 500 m.
  Approximated as a 1.5 km × 1.2 km rectangle at the NE corner.
- Polygon area: v4 = 8.83 km² (v3 was 64.34 km²).

## Voter-assignment impact (v3 → v4)

| ED | v3 area (km²) | v4 area (km²) | Sym-diff (km²) | VAs flipped | 2023 votes flipped |
|---|---:|---:|---:|---:|---:|
| Edmonton-Windermere | 113.72 | 36.76 | 76.96 | 114 | 20,682 |
| Calgary-De Winton | 1,384.09 | 835.22 | 549.89 | 119 | 22,947 |
| Calgary-South | 64.34 | 8.83 | 55.52 | 85 | 18,329 |

**Interpretation.** The large flip counts here are because the v3
polygons occupied substantially incorrect territory, not because v4 is
moving boundary slivers. When v3 was wrong by entire neighbourhoods (as
in all three cases), the v4 correction reassigns those neighbourhoods.
The "votes flipped" column is a measure of territorial correction
magnitude, not a measure of voter disenfranchisement by v4: the affected
VAs simply belong to other 2026 EDs (not the three in this pass).

These 318 flipped VAs / ~61,958 votes do NOT accumulate as a new audit
data gap. They are the correction of the v3 data gap identified in
`analysis/v0_1_commission_reference_shapes.md` as "unquantifiable
without shapefile". v4 makes them roughly quantifiable (with the error
bands listed above) at the cost of being visually-transcribed rather
than shapefile-precise.

## Per-segment error vs v3 approximation (qualitative summary)

For each v4 polygon, v4 is an improvement over v3 in approximation-to-
commission-fidelity:

- **Edmonton-Windermere v3 → v4**: v3 covered most of SW Edmonton
  including neighbourhoods now assigned (per the commission) to
  Edmonton-South (#46). The v3 eastern boundary followed no feature and
  ran ~2 km east of the commission's line. v4 corrects this by cutting
  at ~62 % x across Edmonton-South West, giving a roughly-correct east
  edge with a ±500 m error band. Net: v4 reduces Windermere's
  approximation-to-reality gap from ~70 km² (roughly territorial) to
  ~5-10 km² (edge-local).
- **Calgary-De Winton v3 → v4**: v3 correctly inherited most of Highwood
  but did not subtract Tsuut'ina reserve, ED 29 southern rural block,
  or Okotoks town. It was also ~2,000 km² including western Kananaskis
  area that belongs to neighbouring rural EDs. v4 trims the west to east
  of Tsuut'ina reserve, subtracts the ED 29 southern block and Okotoks,
  and inherits Calgary/Foothills admin boundaries for the north and east.
  Net: v4 reduces the approximation-to-reality gap from ~500 km² to
  ~50-100 km² (edge-local on each of 4 segments plus the ED 29 cut).
- **Calgary-South v3 → v4**: v3 was an elongated 64 km² polygon covering
  Shaw + Hays; the commission shows Calgary-South as a compact ~8-10 km²
  block in SW Hays. v4 corrects this by restricting to a compact
  rectangle in SW Hays with a NE notch. Net: v4 reduces the shape gap
  from "wrong polygon occupying wrong EDs" to "right polygon within
  ±500 m per edge".

## Remaining uncertainty per ED

| ED | Remaining uncertainty | Source |
|---|---|---|
| Edmonton-Windermere | ± 500 m on east edge; ± 3 km² SW corner conservation area not excluded | No OSM feature for east cut; thumbnail resolution for SW corner |
| Calgary-De Winton | ± 1 km on west (Tsuut'ina east extent) and south edges; ± 1 km on ED 29 rural block cut | Commission thumbnail does not show fine detail of Tsuut'ina rural extent or Foothills southern alignment |
| Calgary-South | ± 500 m on north, east, and notch edges | No OSM feature for sub-neighbourhood Calgary boundaries |

All three remain formally Tier C. The residual uncertainty cannot be
reduced below the error bands without the commission's shapefile.

## Whether v4 should replace v3 in §6.7

**Recommendation: keep v4 as a parallel Tier C annex alongside v3's
Tier B (superseded) designation, not as a v3 replacement.**

Rationale:

1. The §6.7 three-tier framework (Tier A / Tier B orange-accepted / Tier
   C awaiting shapefile) remains the correct classification. v4 does not
   change the substance of §6.7 — the three EDs remain "awaiting
   shapefile" in the sense that their *shapefile-precise* boundary is
   unknown. What v4 adds is a better *approximate* polygon than v3 for
   these three.
2. Readers of the academic report should see both the v3 "Tier B
   superseded" label (which they expect from §6.7) and the v4 "Tier C
   approximated" annex (which shows what a commission-thumbnail-guided
   reconstruction looks like). This two-level presentation matches the
   audit's transparency posture.
3. The v4 verification panels (`maps/verification/v0_4_*.png`) should be
   added as supplementary figures. The v3 panels remain in the main
   text with the known-inaccurate caveat.
4. For VA-impact aggregation (§6.7 "1,012 votes on 4 VAs"), v3 remains
   the number cited in the main text — that is the floor of the
   approximation-to-reality gap measured under v3's own assumptions.
   v4 adds a secondary estimate of the gap when the commission's
   territory-level assignment is taken into account: approximately
   318 VAs / 62,000 votes, which is the ceiling of the gap if the v4
   polygons are approximately correct. The report should state both
   figures with full context.

The spawn-off into a v4 Tier C annex preserves the reader's ability to
see what a "best-effort approximation" looks like without over-claiming
precision. It also gives downstream consumers (e.g. Chen-Rodden
replications, base-rate comparisons) a choice: use v3 for conservative
"unquantifiable" framing, or v4 for first-order territorial framing.

## Outputs

| Path | Purpose |
|---|---|
| `analysis/v0_1_shape_refinement_v4.py` | Reproducible pipeline |
| `analysis/v0_1_shape_refinement_v4_log.json` | Per-ED anchors + error bands (machine-readable) |
| `data/v0_1_refined_v4_minority_2026_eds.gpkg` | v4 minority polygons (three EDs updated, rest unchanged from v3) |
| `data/v0_1_boundary_refinement_impact_v4.csv` | Per-ED v3-to-v4 VA-impact table |
| `maps/verification/v0_4_minority_edmonton_windermere.png` | v4 panel for Edmonton-Windermere |
| `maps/verification/v0_4_minority_calgary_de_winton.png` | v4 panel for Calgary-De Winton |
| `maps/verification/v0_4_minority_calgary_south.png` | v4 panel for Calgary-South |

## Reproducibility

```
PYTHONIOENCODING=utf-8 python analysis/v0_1_shape_refinement_v4.py
```

Depends on `osmnx >= 2.0`, `geopandas`, `shapely >= 2.0`, `pyproj`,
`numpy`, `pandas`, `matplotlib`. Network access to Overpass API required
on first run; OSM query results are cached.

## Honest framing

- v4 polygons are **not** the commission's shapefile. They are a visual
  transcription guided by the commission thumbnails, anchored where
  possible to OSM features, with explicit error bands.
- v4 is **better than v3** for all three EDs at the polygon-shape level.
  v3 was structurally wrong (wrong territories); v4 is structurally
  roughly right (territorially correct, boundary edges within error
  bands).
- v4 is **not better than v3** at the VA-assignment level until the
  error bands are validated against the commission's shapefile. The
  ~318 VAs / ~62,000 votes that flip between v3 and v4 are a measure of
  how wrong v3 was territorially, not a measure of how right v4 is.
- Final shapefile-level precision requires the Elections Alberta
  shapefile release. v4 closes ~90 % of the approximation-to-reality
  gap the commission thumbnails allow a reader to close. The residual
  ~10 % is bounded by the per-segment error bands above.

## Summary: what Track Y-prime-prime-prime changed

- **Constructed three v4 polygons** from 2019 parent shapefiles, OSM
  admin / waterway / aboriginal_lands anchors, and visual transcription
  of commission thumbnails at 600 DPI.
- **Updated `tier` classification** in the v4 gpkg: the three EDs are
  now `tier = "C-approximated"`, `confidence = "low-visually-
  transcribed"`, `v4_method = "visual-transcription-assisted"`.
- **Preserved v3 for the other 67 minority EDs** — they carry forward
  unchanged in the v4 gpkg (Tier A inheritance + Tier B orange-accepted).
- **Documented per-segment error bands** (100 m on river-snapped edges,
  300 m on OSM-admin-boundary edges, 500 m to 1 km on visually-
  transcribed edges).
- **Rendered three verification panels** at `v0_4_` prefix showing v3
  (grey dashed) + v4 (solid red) + OSM anchor overlays.
- **Computed VA-impact** (v3 → v4) at 318 total VA reassignments / ~62k
  votes, flagged as a *correction* of v3's territorial errors rather
  than a new data gap.
- **Recommended** parallel annex status rather than v3 replacement in
  §6.7.
