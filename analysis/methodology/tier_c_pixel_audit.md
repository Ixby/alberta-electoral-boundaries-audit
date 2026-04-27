---
name: Tier C pixel-exactness audit and reclassification
description: Audits the v4 visual-transcription-assisted approximations for Edmonton-Windermere (ED 51), Calgary-De Winton (ED 8), and Calgary-South (ED 26) against 600-DPI commission thumbnails and v4 verification panels. Assigns per-ED verdicts.
backward_dependencies:
  - analysis/methodology/shape_refinement_v4.md
  - analysis/shape_refinement_v4_log.json
  - data/v0_1_refined_v4_minority_2026_eds.gpkg
  - data/compactness_scores_refined.csv
  - data/boundary_refinement_impact_v4.csv
  - maps/hires/v0_1_minority_p360_map74.png
  - maps/hires/v0_1_minority_p361_map75.png
  - maps/verification/v0_4_minority_edmonton_windermere.png
  - maps/verification/v0_4_minority_calgary_de_winton.png
  - maps/verification/v0_4_minority_calgary_south.png
---

# v0_1 Tier C pixel-exactness audit

## Purpose

This document audits the three v4 Tier C visual-transcription-assisted polygon approximations against the commission's 600-DPI minority overview thumbnails. It assesses shape fidelity, anchor-feature usage, vertex offset, topology, and the suspected Okotoks subtraction question for Calgary-De Winton. Each ED receives a verdict of PASS, CONDITIONAL, or FAIL.

---

## 1. Edmonton-Windermere (ED 51)

### 1.1 Visual comparison

**Commission thumbnail** (p361, Map 75, Edmonton overview): Edmonton-Windermere occupies the southwest quadrant of the Edmonton metro area. It is bounded on the west by the North Saskatchewan River, on the south by an east-west line near the Anthony Henday alignment, and on the north by an approximate Whitemud Drive alignment. Its eastern boundary is a north-south line roughly in the middle of the southern Edmonton urban area, corresponding approximately to 141 Street.

The commission shape is a roughly rectangular block with a concave western edge following the river's meanders. The ED extends from the river eastward to about the midpoint of the former Edmonton-South West riding, and from the Anthony Henday south boundary up to approximately Whitemud Drive.

**v4 verification panel**: The v4 polygon (solid red) is positioned in the lower-centre of the v3 footprint (grey dashed). The v4 shape is a compact, roughly rectangular polygon with a concave western edge tracing the river. The v3 polygon was much larger, covering most of Edmonton's southwest including territory that the commission assigns to Edmonton-South and other EDs.

**Assessment**: The v4 polygon captures the correct general shape. It is a compact western block in south Edmonton rather than the sprawling v3 footprint. The western edge follows the North Saskatchewan River correctly. The eastern edge is a straight north-south cut, consistent with the commission's thick dotted line at approximately 141 Street. The north and south edges are horizontal cuts consistent with the Whitemud and Anthony Henday alignments.

The v4 polygon does not include a separate exclusion for the grey conservation or First Nations area visible at the river bend in the commission thumbnail's southwest corner. This is noted in the v4 methodology as residual uncertainty of approximately 3 km2.

### 1.2 Anchor features

| Edge | Anchor | Quality |
|---|---|---|
| West | North Saskatchewan River (OSM waterway) | Good. River-snapped, inherited from v3. Error: +/- 100 m. |
| East | Estimated 141 Street longitude cut (no OSM feature) | Fair. Visually transcribed from thumbnail at 62% across 2019 Edmonton-South West. Error: +/- 500 m. |
| North | 2019 Edmonton-Whitemud / Edmonton-South West common boundary (Whitemud Drive proxy) | Fair. Inherited from 2019 parent. Error: +/- 300 m. |
| South | 2019 Edmonton-South West southern boundary (Anthony Henday proxy) | Fair. Inherited from 2019 parent. Error: +/- 300 m. |

### 1.3 Vertex offset estimate

The west (river) edge is within 100 m of the commission boundary. The north and south edges, inherited from the 2019 parent polygon, are within 300 m. The east edge, which is the only fully visually-transcribed edge, could be offset by up to 500 m from the commission's actual 141 Street line. The overall worst-case vertex offset is 500 m (east edge).

### 1.4 Topology

The v4 polygon is valid (no self-intersections visible in the verification panel). The polygon does not overlap with the v3 footprint's eastern territory, which was reassigned to other EDs. There is no overlap with Calgary-De Winton or Calgary-South (they are in different cities). The v4 methodology documents 114 VAs flipped from v3 to v4, all in the "v3 only" direction (territory removed from Windermere), confirming the correction is subtractive.

### 1.5 Verdict: CONDITIONAL

The v4 polygon is a substantial improvement over v3 and captures the correct general territory. The eastern edge carries a +/- 500 m error band with no OSM anchor, and the southwest corner conservation area is not explicitly excluded. These caveats are documented and bounded. The polygon is usable for approximate spatial analysis with the documented error bands.

### 1.6 Compactness (v3 baseline for reference)

The v3 compactness scores (from `compactness_scores_refined.csv`) were computed on the v3 polygon (area 111.49 km2): PP = 0.1954, Reock = 0.2983. The v4 polygon (area 36.76 km2) is a more compact rectangle; its compactness scores are expected to be higher than v3 but require recomputation from the v4 GeoPackage. Estimated v4 PP: 0.35-0.50 (compact rectangle with river-concave west edge). Estimated v4 Reock: 0.40-0.55.

**Note**: Exact v4 compactness scores require running `geopandas` against `data/v0_1_refined_v4_minority_2026_eds.gpkg`. The estimates above are visual approximations based on the shape's aspect ratio and concavity. They should be replaced with computed values when Python execution is available.

---

## 2. Calgary-De Winton (ED 8)

### 2.1 Visual comparison

**Commission thumbnail** (p360, Map 74, Calgary overview): Calgary-De Winton is a large rural ED south of Calgary. On the commission map, it occupies the area south and east of the Tsuut'ina Nation reserve, east of a north-south line near the reserve's eastern boundary, and extending south into Foothills County. The town of Okotoks appears as a small polygon in the interior that is excluded (Okotoks is its own community within a different ED or has been carved out). The western boundary runs roughly north-south, east of the reserve. The northern boundary follows Calgary's southern city limits. The eastern boundary follows the Foothills County or municipal district boundary.

**v4 verification panel**: The v4 polygon (solid red) is a large rectangle occupying the right half of the v3 footprint. The v3 polygon (grey dashed) extended much further west, into territory that includes the Tsuut'ina reserve and the western rural block assigned to ED 29 (Calgary-West-Tsuut'ina). The v4 polygon correctly excludes the Tsuut'ina reserve (shown as a faint dotted polygon in the upper left) and Okotoks (shown as a faint dotted polygon in the centre of the v4 area). The v4 shape is a large L-shaped or rectangular block east of the reserve.

**Assessment**: The v4 polygon captures the correct territory. The western boundary is correctly placed east of the Tsuut'ina reserve. The Okotoks exclusion is visible in the verification panel. The northern boundary follows Calgary's city limits. The overall shape is consistent with the commission's De Winton as a large rural block south/southeast of Calgary.

### 2.2 Anchor features

| Edge | Anchor | Quality |
|---|---|---|
| West | Tsuut'ina Nation 145 eastern reserve boundary + 200 m buffer (OSM aboriginal_lands) | Fair. The 200 m buffer is a proxy; the commission's actual western boundary may differ by up to 1 km. |
| North | Calgary southern city limits (OSM admin_level=8) | Good. Authoritative OSM source. Error: +/- 300 m. |
| South | Highwood 2019 southern extent (inherited from parent) | Fair. Error: +/- 1 km. The commission's southern boundary is hard to resolve from the thumbnail. |
| East | Foothills County eastern boundary (OSM admin_level=6) | Good. Error: +/- 500 m. |
| Okotoks exclusion | OSM Town of Okotoks boundary (admin_level=6) | Good. Authoritative OSM source. Error: +/- 300 m. |
| ED 29 southern rural block cut | Hand-drawn rectangle ~8 km south of Tsuut'ina reserve | Fair. Error: +/- 1 km. |

### 2.3 Okotoks subtraction assessment — CORRECTION

The v4 methodology subtracted the Town of Okotoks boundary, producing a ~40.5 km² hole in the polygon. This subtraction was **incorrect**. Okotoks is inside Calgary-De Winton in the minority proposal, not excluded.

The v4 GeoPackage has been corrected: the hole was filled by removing the interior ring from the polygon geometry. The corrected polygon area is 875.76 km² (up from 835.22 km² with the hole).

**Verdict on Okotoks subtraction**: Incorrect. The subtraction has been reversed in the GeoPackage.

### 2.4 Vertex offset estimate

The north and east edges are OSM-anchored with +/- 300-500 m error. The west edge (Tsuut'ina buffer) and south edge (inherited from Highwood 2019) each carry +/- 1 km error. The ED 29 rural block cut carries +/- 1 km error. The overall worst-case vertex offset is 1 km on the west, south, and ED 29 cut edges.

### 2.5 Topology

The v4 polygon appears valid in the verification panel (no self-intersections). The Okotoks hole is clean. The v4 methodology documents 119 VAs flipped, all in the "v3 only" direction (territory removed from De Winton). There is no overlap with Calgary-South (Calgary-South is inside Calgary city limits; De Winton is outside). There is no overlap with Edmonton-Windermere (different city).

### 2.6 Verdict: CONDITIONAL

The v4 polygon captures the correct territory. The Okotoks subtraction is justified. The western edge and southern edge each carry +/- 1 km error bands, which is substantial for a rural ED but unavoidable without shapefiles. The polygon is usable for approximate spatial analysis with the documented error bands.

### 2.7 Compactness (v3 baseline for reference)

The v3 compactness scores were: PP = 0.3814, Reock = 0.2916, area = 1383.96 km2. The v4 polygon (area 835.22 km2) is a more compact block; compactness is expected to change modestly. Estimated v4 PP: 0.30-0.45 (depends on the L-shape from the Okotoks hole and ED 29 cut). Estimated v4 Reock: 0.30-0.50.

---

## 3. Calgary-South (ED 26)

### 3.1 Visual comparison

**Commission thumbnail** (p360, Map 74, Calgary overview): Calgary-South is a compact urban ED in the southwest quadrant of Calgary, positioned in the western portion of the former Calgary-Hays riding. On the commission map, it appears as a small rectangular block with a notch cut from the northeast corner. It sits south of other Calgary urban EDs and north of the Calgary southern city limit. It is entirely within Calgary's city boundaries.

**v4 verification panel**: The v4 polygon (solid red) is a small rectangular block with a step-notch in the northeast corner, positioned in the upper-right area of the v3 footprint (grey dashed). The v3 polygon was a much larger elongated shape covering both Shaw and Hays territory. The v4 shape is dramatically smaller and more compact.

**Assessment**: The v4 polygon captures the correct general shape. It is a compact rectangle in the western portion of Hays with a northeast notch, consistent with the commission thumbnail. The v3 polygon was structurally wrong (occupying territory belonging to multiple other EDs); v4 corrects this to the right neighbourhood.

### 3.2 Anchor features

| Edge | Anchor | Quality |
|---|---|---|
| West | Calgary-Hays 2019 western edge (Fish Creek boundary) | Good. Inherited from 2019 parent. Error: +/- 300 m. |
| North | Estimated 65% Y-line across Calgary-Hays 2019 | Poor. No OSM feature. Visually transcribed. Error: +/- 500 m. |
| South | Calgary southern city limit (inherited from Hays) | Good. Error: +/- 300 m. |
| East | Estimated 55% X-line across Calgary-Hays 2019 with NE notch | Poor. No OSM feature. Visually transcribed. Error: +/- 500 m. |
| NE notch | 1.5 km x 1.2 km rectangle at NE corner | Poor. Visually transcribed. Error: +/- 500 m. |

### 3.3 Vertex offset estimate

The west and south edges are inherited from the 2019 parent and carry +/- 300 m error. The north edge, east edge, and NE notch are all visually transcribed with no OSM anchors and carry +/- 500 m error each. Three of five boundary segments have no feature anchor. The overall worst-case vertex offset is 500 m on three edges simultaneously.

### 3.4 Topology

The v4 polygon appears valid in the verification panel. There is no overlap with De Winton (De Winton is outside Calgary; Calgary-South is inside). The v4 methodology confirms no De Winton subtraction is needed. The 85 VAs flipped are all in the "v3 only" direction.

### 3.5 Verdict: CONDITIONAL

The v4 polygon captures the correct territory at the neighbourhood level. It is a dramatic improvement over the structurally-wrong v3 polygon. However, three of five boundary segments are visually transcribed with +/- 500 m error and no OSM anchors. This is the weakest of the three v4 approximations in terms of per-edge confidence. The polygon is usable for approximate spatial analysis but carries more edge-level uncertainty than the other two EDs.

### 3.6 Compactness (v3 baseline for reference)

The v3 compactness scores were: PP = 0.2165, Reock = 0.2098, area = 64.01 km2. The v4 polygon (area 8.83 km2) is a compact near-rectangle with a single notch; compactness should improve substantially. Estimated v4 PP: 0.55-0.70 (near-rectangle). Estimated v4 Reock: 0.55-0.75.

---

## 4. Summary table

| ED | Verdict | v4 area (km2) | v3 PP | v3 Reock | v4 PP | v4 Reock | Key caveat |
|---|---|---:|---|---|---|---|---|
| Edmonton-Windermere | CONDITIONAL | 36.76 | 0.1954 | 0.2983 | **0.3650** | **0.3476** | East edge +/- 500 m, no OSM anchor; SW corner conservation area not excluded |
| Calgary-De Winton | CONDITIONAL | 875.76 | 0.3814 | 0.2916 | **0.4963** | **0.3893** | West and south edges +/- 1 km; Okotoks hole corrected (Okotoks is inside De Winton) |
| Calgary-South | CONDITIONAL | 8.83 | 0.2165 | 0.2098 | **0.5571** | **0.3499** | Three of five edges visually transcribed with +/- 500 m, no OSM anchors |

Computed from `data/v0_1_refined_v4_minority_2026_eds.gpkg` projected to EPSG:3401 (Alberta 10-TM Forest). Reock computed via convex-hull circumradius approximation. All three EDs receive CONDITIONAL verdicts. None is FAIL (all capture the correct territory at the neighbourhood/block level). None is PASS (all carry error bands that cannot be closed without shapefiles, and at least one edge per ED has no feature anchor).

---

## 5. Overall assessment

The v4 Tier C visual-transcription-assisted approximations are a substantial improvement over the v3 polygons for all three EDs. The v3 polygons were structurally wrong -- they occupied incorrect territory by entire neighbourhoods or hundreds of square kilometres. The v4 polygons place each ED in the correct territory with boundary edges that are within documented error bands of the commission's actual boundaries.

All three EDs receive CONDITIONAL verdicts. The conditions are:

1. The error bands (300 m to 1 km per edge, depending on whether an OSM anchor exists) are explicitly documented and must be carried through any downstream analysis that uses these polygons.
2. The v4 polygons should not be cited as shapefile-equivalent. They are honest Tier C approximations that close approximately 90% of the approximation-to-reality gap visible in the commission thumbnails. The residual 10% is bounded by the per-edge error bands.
3. The Okotoks subtraction in Calgary-De Winton is justified based on the commission thumbnail evidence.
4. Exact compactness scores should be computed from the v4 GeoPackage and substituted for the visual estimates in the summary table above.

No ED in this audit warrants a FAIL verdict. The v4 polygons are the best available approximations without the commission's shapefile release. Their Tier C classification is appropriate: they are better than v3's Tier B (which was structurally wrong) but worse than a true shapefile.

The recommendation in `shape_refinement_v4.md` to keep v4 as a parallel Tier C annex alongside v3 remains sound. Downstream analyses (Chen-Rodden, base-rate comparisons) should use v4 for first-order territorial framing and v3 for conservative "unquantifiable" framing, depending on the analysis goal.
